from pathlib import Path
import tempfile
import unittest

from tools.check_site import check_site


class SiteCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.config = {"site_origin": "https://thejhomecare.com", "phone": "01081680205"}
        self.write("index.html", '''<html><head>
<link rel="stylesheet" href="/styles/main.css?v=1">
<script src="/site.js"></script></head><body id="main">
<a href="/pricing/?source=home#prices">가격 안내</a>
<a href="https://thejhomecare.com/pricing/#prices">가격</a>
<a href="#">맨 위로</a><a href="tel:010-8168-0205">010-8168-0205</a>
<a href="sms:+821081680205?body=hello">문자</a>
<a href="https://example.com/no-such-page">외부 링크</a>
<img src="/images/screen%20photo.webp" alt="시공 사진"
 srcset="/images/screen%20photo.webp 1x, /images/screen%20photo.webp 2x">
</body></html>''')
        self.write("pricing/index.html", '<h1 id="prices">시공 가격</h1><a href="/#main">홈</a>')
        self.write("styles/main.css", '/* url(missing-comment.webp) */ body {background:url(../images/screen%20photo.webp)}')
        self.write("images/screen photo.webp", "fixture")
        self.write("site.js", "// fixture")

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def replace(self, old, new):
        path = self.root / "index.html"
        path.write_text(path.read_text().replace(old, new), encoding="utf-8")

    def errors(self):
        return check_site(self.root, self.config)[0]

    def test_valid_site_handles_queries_fragments_encoded_paths_and_international_phone(self):
        self.assertEqual(self.errors(), [])

    def test_deleted_page_is_reported(self):
        (self.root / "pricing/index.html").unlink()
        self.assertTrue(any("missing file" in e and "pricing" in e for e in self.errors()))

    def test_deleted_image_is_reported(self):
        (self.root / "images/screen photo.webp").unlink()
        self.assertTrue(any("img[src]" in e and "missing file" in e for e in self.errors()))

    def test_wrong_anchor_is_reported(self):
        self.replace("#prices", "#unknown")
        self.assertTrue(any("missing anchor #unknown" in e for e in self.errors()))

    def test_wrong_tel_and_sms_are_reported(self):
        self.replace("tel:010-8168-0205", "tel:010-8168-0206")
        self.replace("sms:+821081680205", "sms:+821081680206")
        errors = self.errors()
        self.assertTrue(any("wrong tel number" in e for e in errors))
        self.assertTrue(any("wrong sms number" in e for e in errors))

    def test_correct_link_with_wrong_visible_phone_is_reported(self):
        self.replace(">010-8168-0205</a>", ">010-8168-0206</a>")
        self.assertTrue(any("wrong displayed phone" in e for e in self.errors()))

    def test_missing_srcset_variant_is_reported(self):
        self.replace("/images/screen%20photo.webp 2x", "/images/missing.webp 2x")
        self.assertTrue(any("img[srcset]" in e and "missing.webp" in e for e in self.errors()))

    def test_missing_css_asset_is_reported(self):
        self.write("styles/main.css", "body{background:url('../images/missing.webp')}")
        self.assertTrue(any("CSS url" in e and "missing.webp" in e for e in self.errors()))

    def test_duplicate_id_is_reported(self):
        self.replace('<body id="main">', '<body id="main"><div id="main"></div>')
        self.assertTrue(any("duplicate id #main" in e for e in self.errors()))

    def test_inline_script_and_style_phone_values_are_not_visible_content(self):
        self.replace("</head>", '<script>const sample="010-1111-2222";</script><style>/*010-1111-2222*/</style></head>')
        self.assertEqual(self.errors(), [])

    def test_missing_image_alt_is_reported(self):
        self.replace(' alt="시공 사진"', '')
        self.assertTrue(any("image has no alt attribute" in e for e in self.errors()))

    def test_same_domain_absolute_missing_link_is_checked(self):
        self.replace("https://thejhomecare.com/pricing/#prices", "https://thejhomecare.com/missing/")
        self.assertTrue(any("missing file" in e and "/missing/" in e for e in self.errors()))


if __name__ == "__main__":
    unittest.main()
