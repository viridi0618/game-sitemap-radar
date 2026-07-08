from __future__ import annotations

import gzip
import xml.etree.ElementTree as ET

from .models import SitemapEntry


def decode_xml(body: bytes) -> str:
    if body.startswith(b"\x1f\x8b"):
        body = gzip.decompress(body)
    return body.decode("utf-8", errors="replace")


def _ns_tag(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def parse_sitemap_xml(body: bytes | str) -> tuple[str, list[SitemapEntry]]:
    text = decode_xml(body) if isinstance(body, bytes) else body
    root = ET.fromstring(text)
    root_tag = _ns_tag(root.tag)
    if root_tag == "sitemapindex":
        entries = []
        for sm in root:
            if _ns_tag(sm.tag) != "sitemap":
                continue
            loc = None
            lastmod = None
            for child in sm:
                if _ns_tag(child.tag) == "loc":
                    loc = (child.text or "").strip()
                if _ns_tag(child.tag) == "lastmod":
                    lastmod = (child.text or "").strip()
            if loc:
                entries.append(SitemapEntry(loc=loc, lastmod=lastmod))
        return "index", entries
    if root_tag == "urlset":
        entries = []
        for url in root:
            if _ns_tag(url.tag) != "url":
                continue
            loc = None
            lastmod = None
            for child in url:
                if _ns_tag(child.tag) == "loc":
                    loc = (child.text or "").strip()
                if _ns_tag(child.tag) == "lastmod":
                    lastmod = (child.text or "").strip()
            if loc:
                entries.append(SitemapEntry(loc=loc, lastmod=lastmod))
        return "urlset", entries
    return "unknown", []

