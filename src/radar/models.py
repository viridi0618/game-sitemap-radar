from dataclasses import dataclass, field


@dataclass
class Source:
    name: str
    domain: str
    sitemap_url: str | None = None
    site_type: str = "general"
    language: str = "en"
    priority: int = 3


@dataclass
class Settings:
    request_timeout_seconds: int = 20
    max_sitemaps_per_source: int = 50
    max_urls_per_sitemap: int = 50000
    delay_seconds_per_source: float = 1
    user_agent: str = "GameSitemapRadar/0.1 (+keyword research; respects robots.txt)"
    report_window_hours: int = 72


@dataclass
class AppConfig:
    sources: list[Source] = field(default_factory=list)
    settings: Settings = field(default_factory=Settings)


@dataclass
class SitemapEntry:
    loc: str
    lastmod: str | None = None

