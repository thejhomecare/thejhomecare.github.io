#!/usr/bin/env python3
"""Offline checks for the static site. Uses only Python's standard library."""

import argparse
from collections import Counter
from dataclasses import dataclass
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

if __package__:
    from .check_search_metadata import check_search_metadata
else:
    from check_search_metadata import check_search_metadata


@dataclass(frozen=True)
class Reference:
    value: str
    line: int
    kind: str


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.references = []
        self.ids = []
        self.text = []
        self.images = 0
        self.problems = []
        self.hidden_text = 0
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        line = self.getpos()[0]
        if tag in {"script", "style"}:
            self.hidden_text += 1
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        fields = {
            "a": ("href",), "img": ("src",), "script": ("src",),
            "source": ("src",), "video": ("src", "poster"),
            "audio": ("src",), "iframe": ("src",),
        }.get(tag, ())
        if tag == "link" and set(attrs.get("rel", "").lower().split()) & {
            "stylesheet", "icon", "apple-touch-icon", "manifest", "preload",
        }:
            fields = ("href",)
        for field in fields:
            if field in attrs:
                value = attrs[field] or ""
                if value:
                    self.references.append(Reference(value, line, f"{tag}[{field}]"))
                else:
                    self.problems.append(f"line {line}: empty {tag}[{field}]")
        if tag in {"img", "source"} and attrs.get("srcset"):
            # Data URLs contain commas and cannot be split this way.
            value = attrs["srcset"]
            if not value.lstrip().startswith("data:"):
                for candidate in value.split(","):
                    parts = candidate.strip().split()
                    if parts:
                        self.references.append(Reference(parts[0], line, f"{tag}[srcset]"))
        if tag == "img":
            self.images += 1
            if not attrs.get("src") and not attrs.get("srcset"):
                self.problems.append(f"line {line}: image has no source")
            if "alt" not in attrs:
                self.problems.append(f"line {line}: image has no alt attribute")

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in {"script", "style"}:
            self.hidden_text = max(0, self.hidden_text - 1)

    def handle_data(self, data):
        if not self.hidden_text:
            self.text.append(data)


def normalize_phone(value):
    digits = re.sub(r"\D", "", unquote(value))
    if digits.startswith("82"):
        digits = "0" + digits[2:]
    return digits


def local_target(root, source, value, origin):
    """Return (local path, fragment), or None for external/non-file URLs."""
    url = urlsplit(value)
    site = urlsplit(origin)
    if url.netloc:
        if url.hostname != site.hostname:
            return None
        if url.scheme and url.scheme not in {"http", "https"}:
            return None
        raw = root / unquote(url.path).lstrip("/")
    elif url.scheme:
        return None
    elif not url.path:
        raw = source
    elif url.path.startswith("/"):
        raw = root / unquote(url.path).lstrip("/")
    else:
        raw = source.parent / unquote(url.path)
    target = raw.resolve()
    if not target.is_relative_to(root):
        raise ValueError("reference escapes the site directory")
    if target.is_dir():
        target /= "index.html"
    return target, unquote(url.fragment)


def check_site(root, config):
    root = Path(root).resolve()
    origin = config["site_origin"]
    expected_phone = normalize_phone(config["phone"])
    if not re.fullmatch(r"010\d{8}", expected_phone):
        raise ValueError("site_check.json phone must be a Korean mobile number")
    errors = []
    pages = {}
    ignored = {".git", "node_modules", "tools", "tests"}
    for path in sorted(root.rglob("*.html")):
        if ignored.intersection(path.relative_to(root).parts):
            continue
        pages[path] = Page(path.read_text(encoding="utf-8"))
    if not pages:
        errors.append("No HTML pages found")
    counts = {"pages": len(pages), "images": 0, "local_references": 0, "phone_links": 0}

    def check_reference(source, ref):
        label = f"{source.relative_to(root)}:{ref.line} ({ref.kind})"
        try:
            result = local_target(root, source, ref.value, origin)
        except ValueError as exc:
            errors.append(f"{label}: {exc}: {ref.value}")
            return
        if result is None:
            return
        target, fragment = result
        counts["local_references"] += 1
        if not target.is_file():
            errors.append(f"{label}: missing file: {ref.value}")
        elif fragment and target.suffix.lower() == ".html":
            page = pages.get(target)
            if page is None:
                page = Page(target.read_text(encoding="utf-8"))
            if fragment not in page.ids:
                errors.append(f"{label}: missing anchor #{fragment}: {ref.value}")

    for path, page in pages.items():
        counts["images"] += page.images
        errors.extend(f"{path.relative_to(root)}: {p}" for p in page.problems)
        errors.extend(f"{path.relative_to(root)}: duplicate id #{i}"
                      for i, n in Counter(page.ids).items() if n > 1)
        for ref in page.references:
            url = urlsplit(ref.value)
            if url.scheme.lower() in {"tel", "sms"}:
                counts["phone_links"] += 1
                number = url.path.split(";", 1)[0]
                if normalize_phone(number) != expected_phone:
                    errors.append(f"{path.relative_to(root)}:{ref.line}: wrong {url.scheme} number: {ref.value}")
            check_reference(path, ref)
        for match in re.finditer(r"(?<!\d)010(?:[\s-]?\d){8}(?!\d)", " ".join(page.text)):
            if normalize_phone(match.group()) != expected_phone:
                errors.append(f"{path.relative_to(root)}: wrong displayed phone: {match.group()}")

    for path in sorted(root.rglob("*.css")):
        if ignored.intersection(path.relative_to(root).parts):
            continue
        css = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group().count("\n"),
                     path.read_text(encoding="utf-8"), flags=re.S)
        for match in re.finditer(r"url\(\s*(['\"]?)(.*?)\1\s*\)", css, re.I):
            value = match.group(2).strip()
            if not value or value.startswith("#"):
                continue
            check_reference(path, Reference(value, css[:match.start()].count("\n") + 1, "CSS url"))
    if config.get('check_search_metadata', False):
        search_errors, search_counts = check_search_metadata(root, origin)
        errors.extend(search_errors)
        counts.update(search_counts)
    return errors, counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--config", type=Path, default=Path(__file__).with_name("site_check.json"))
    args = parser.parse_args()
    try:
        config = json.loads(args.config.read_text(encoding="utf-8"))
        errors, counts = check_site(args.root, config)
    except (OSError, ValueError, KeyError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print("Checked: " + ", ".join(f"{k}={v}" for k, v in counts.items()))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"FAIL: {len(errors)} issue(s)", file=sys.stderr)
        return 1
    print("PASS: all configured site checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
