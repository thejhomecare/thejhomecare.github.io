"""Offline search metadata and sitemap checks for the static website."""

from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import quote
import xml.etree.ElementTree as ET


class SearchMetadata(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.titles, self.headings, self.descriptions = [], [], []
        self.canonicals, self.robots, self.json_blocks = [], [], []
        self.capture = None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {'title', 'h1'}:
            values = self.titles if tag == 'title' else self.headings
            values.append([])
            self.capture = (tag, values[-1])
        elif tag == 'script' and attrs.get('type', '').lower() == 'application/ld+json':
            self.json_blocks.append([])
            self.capture = (tag, self.json_blocks[-1])
        elif tag == 'meta':
            name = attrs.get('name', '').lower()
            if name == 'description':
                self.descriptions.append(attrs.get('content') or '')
            elif name in {'robots', 'googlebot', 'bingbot'}:
                self.robots.append(attrs.get('content') or '')
        elif tag == 'link' and 'canonical' in attrs.get('rel', '').lower().split():
            self.canonicals.append(attrs.get('href') or '')

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if self.capture and self.capture[0] == tag:
            self.capture = None

    def handle_data(self, data):
        if self.capture:
            self.capture[1].append(data)


def page_url(origin, relative):
    path = relative.as_posix()
    if path == 'index.html':
        path = ''
    elif path.endswith('/index.html'):
        path = path[:-len('index.html')]
    return origin.rstrip('/') + '/' + quote(path, safe='/')


def reject_json_constant(value):
    raise ValueError(f'Invalid JSON constant {value}')


def check_search_metadata(root, origin):
    root = Path(root).resolve()
    ignored = {'.git', 'node_modules', 'tools', 'tests'}
    errors, expected_urls = [], set()
    titles, descriptions = {}, {}
    counts = {'search_pages': 0, 'sitemap_urls': 0}
    for path in sorted(root.rglob('*.html')):
        relative = path.relative_to(root)
        if ignored.intersection(relative.parts) or relative.as_posix() == '404.html':
            continue
        metadata = SearchMetadata(path.read_text(encoding='utf-8'))
        if any('noindex' in value.lower().replace(',', ' ').split() for value in metadata.robots):
            continue
        counts['search_pages'] += 1
        expected_url = page_url(origin, relative)
        expected_urls.add(expected_url)
        fields = {
            'title': [' '.join(''.join(v).split()) for v in metadata.titles],
            'meta description': [' '.join(v.split()) for v in metadata.descriptions],
            'H1': [' '.join(''.join(v).split()) for v in metadata.headings],
        }
        for label, values in fields.items():
            if len(values) != 1 or not values[0]:
                errors.append(f'{relative}: expected one nonempty {label}')
        if len(metadata.canonicals) != 1 or metadata.canonicals[0] != expected_url:
            errors.append(f'{relative}: canonical must be {expected_url}')
        for label, values, seen in (
            ('title', fields['title'], titles),
            ('meta description', fields['meta description'], descriptions),
        ):
            if len(values) == 1 and values[0]:
                key = values[0]
                if key in seen:
                    errors.append(f'{relative}: duplicate {label} with {seen[key]}')
                else:
                    seen[key] = relative
        for index, block in enumerate(metadata.json_blocks, 1):
            try:
                json.loads(''.join(block), parse_constant=reject_json_constant)
            except ValueError as exc:
                errors.append(f'{relative}: invalid JSON-LD block {index}: {exc}')

    try:
        tree = ET.parse(root / 'sitemap.xml')
        ns = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
        if tree.getroot().tag != ns + 'urlset':
            raise ValueError('expected sitemap urlset with standard namespace')
        urls = [(element.text or '').strip() for element in tree.findall(ns + 'url/' + ns + 'loc')]
        counts['sitemap_urls'] = len(urls)
        errors.extend(f'sitemap.xml: duplicate URL {url}' for url, n in Counter(urls).items() if n > 1)
        for url in urls:
            if url not in expected_urls:
                errors.append(f'sitemap.xml: unexpected URL {url!r}')
        for url in sorted(expected_urls - set(urls)):
            errors.append(f'sitemap.xml: missing page {url}')
        for element in tree.findall(ns + 'url'):
            if len(element.findall(ns + 'loc')) != 1:
                errors.append('sitemap.xml: every url must contain one loc')
    except (OSError, ET.ParseError, ValueError) as exc:
        errors.append(f'sitemap.xml: {exc}')
    return errors, counts
