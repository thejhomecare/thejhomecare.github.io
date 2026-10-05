from pathlib import Path
import tempfile
import unittest

from tools.check_search_metadata import check_search_metadata
from tools.check_site import check_site


class SearchMetadataTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.origin = 'https://thejhomecare.com'
        self.write('index.html', self.page('홈', '홈페이지 안내', '/'))
        self.write('pricing/index.html', self.page('시공 가격', '가격 안내', '/pricing/'))
        self.write('404.html', '<h1>페이지를 찾을 수 없습니다</h1>')
        self.write('private/index.html', '<meta name="robots" content="noindex,follow">')
        self.sitemap(['/', '/pricing/'])

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding='utf-8')

    def page(self, title, description, path):
        return f'''<html><head><title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{self.origin}{path}">
<script type="application/ld+json">{{"@type":"WebPage"}}</script>
</head><body><h1><strong>{title}</strong></h1></body></html>'''

    def sitemap(self, paths):
        entries = ''.join(f'<url><loc>{self.origin}{path}</loc></url>' for path in paths)
        self.write('sitemap.xml', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + entries + '</urlset>')

    def replace(self, old, new):
        target = self.root / 'index.html'
        target.write_text(target.read_text(encoding='utf-8').replace(old, new), encoding='utf-8')

    def errors(self):
        return check_search_metadata(self.root, self.origin)[0]

    def test_valid_metadata_with_nested_heading_excludes_404_and_noindex(self):
        errors, counts = check_search_metadata(self.root, self.origin)
        self.assertEqual(errors, [])
        self.assertEqual(counts, {'search_pages': 2, 'sitemap_urls': 2})

    def test_missing_empty_and_multiple_search_fields_are_reported(self):
        self.replace('<title>홈</title>', '')
        self.replace('content="홈페이지 안내"', 'content="  "')
        self.replace('</body>', '<h1>추가 제목</h1></body>')
        errors = self.errors()
        for label in ('title', 'meta description', 'H1'):
            self.assertTrue(any('expected one nonempty ' + label in e for e in errors))

    def test_duplicate_titles_and_descriptions_are_reported(self):
        self.write('pricing/index.html', self.page('홈', '홈페이지 안내', '/pricing/'))
        errors = self.errors()
        self.assertTrue(any('duplicate title' in e for e in errors))
        self.assertTrue(any('duplicate meta description' in e for e in errors))

    def test_wrong_canonical_is_reported(self):
        self.replace('href="https://thejhomecare.com/"', 'href="https://example.com/"')
        self.assertTrue(any('canonical must be' in e for e in self.errors()))

    def test_invalid_json_ld_is_reported(self):
        self.replace('{"@type":"WebPage"}', '{"@type":}')
        self.assertTrue(any('invalid JSON-LD' in e for e in self.errors()))

    def test_non_json_script_is_not_treated_as_json_ld(self):
        self.replace('</head>', '<script>const sample = undefined;</script></head>')
        self.assertEqual(self.errors(), [])

    def test_new_page_missing_from_sitemap_is_reported(self):
        self.write('cases/new/index.html', self.page('새 사례', '새 현장 설명', '/cases/new/'))
        self.assertTrue(any('missing page https://thejhomecare.com/cases/new/' in e for e in self.errors()))

    def test_duplicate_and_deleted_sitemap_urls_are_reported(self):
        self.sitemap(['/', '/pricing/', '/pricing/', '/deleted/'])
        errors = self.errors()
        self.assertTrue(any('duplicate URL' in e for e in errors))
        self.assertTrue(any('unexpected URL' in e and '/deleted/' in e for e in errors))

    def test_invalid_xml_and_namespace_are_reported(self):
        for value in ('<urlset', '<urlset><url><loc>https://thejhomecare.com/</loc></url></urlset>'):
            with self.subTest(value=value):
                self.write('sitemap.xml', value)
                self.assertTrue(any('sitemap.xml:' in e for e in self.errors()))

    def test_noindex_page_cannot_remain_in_sitemap(self):
        self.sitemap(['/', '/pricing/', '/private/'])
        self.assertTrue(any('unexpected URL' in e and '/private/' in e for e in self.errors()))

    def test_search_checks_run_through_main_checker(self):
        config = {'site_origin': self.origin, 'phone': '01081680205', 'check_search_metadata': True}
        self.assertEqual(check_site(self.root, config)[0], [])
        self.replace('<title>홈</title>', '')
        self.assertTrue(any('expected one nonempty title' in e for e in check_site(self.root, config)[0]))


if __name__ == '__main__':
    unittest.main()
