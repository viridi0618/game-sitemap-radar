from __future__ import annotations

from urllib.parse import urljoin

from .fetcher import Fetcher, FetchResult
from .utils import domain_base_url


COMMON_SITEMAP_PATHS = [
    "/sitemap.xml",
    "/sitemap_index.xml",
    "/post-sitemap.xml",
    "/page-sitemap.xml",
    "/news-sitemap.xml",
]


def robots_url_for_domain(domain: str) -> str:
    return urljoin(domain_base_url(domain), "/robots.txt")


def parse_sitemaps_from_robots(text: str) -> list[str]:
    urls = []
    for line in text.splitlines():
        if line.lower().startswith("sitemap:"):
            value = line.split(":", 1)[1].strip()
            if value:
                urls.append(value)
    return urls


def discover_sitemap_urls(domain: str, fetcher: Fetcher, explicit_sitemap: str | None = None) -> tuple[list[str], FetchResult | None]:
    found = []
    if explicit_sitemap:
        found.append(explicit_sitemap)
    robots_result = fetcher.fetch(robots_url_for_domain(domain))
    if robots_result.status_code == 200 and robots_result.body:
        found.extend(parse_sitemaps_from_robots(robots_result.body.decode("utf-8", errors="replace")))
    base = domain_base_url(domain)
    found.extend(urljoin(base, path) for path in COMMON_SITEMAP_PATHS)
    deduped = list(dict.fromkeys(found))
    return deduped, robots_result

