from pathlib import Path

from radar.sitemap_parser import parse_sitemap_xml


FIXTURES = Path(__file__).parent / "fixtures"


def test_parse_sitemap_index():
    sitemap_type, entries = parse_sitemap_xml((FIXTURES / "sitemap_index.xml").read_text())
    assert sitemap_type == "index"
    assert entries[0].loc == "https://example.com/post-sitemap.xml"


def test_parse_urlset():
    sitemap_type, entries = parse_sitemap_xml((FIXTURES / "sitemap.xml").read_text())
    assert sitemap_type == "urlset"
    assert len(entries) == 2
    assert entries[0].loc.endswith("/ice-tycoon-2-codes/")

