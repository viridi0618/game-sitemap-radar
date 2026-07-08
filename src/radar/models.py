from dataclasses import dataclass, field


@dataclass
class Source:
    name: str
    domain: str
    sitemap_url: str | None = None
    site_type: str = "general"
    language: str = "en"
    priority: int = 3
    include_url_keywords: list[str] = field(default_factory=list)
    exclude_url_keywords: list[str] = field(default_factory=list)


@dataclass
class Settings:
    request_timeout_seconds: int = 20
    max_sitemaps_per_source: int = 50
    max_urls_per_sitemap: int = 50000
    delay_seconds_per_source: float = 1
    user_agent: str = "GameSitemapRadar/0.1 (+keyword research; respects robots.txt)"
    report_window_hours: int = 72


@dataclass
class WritingSettings:
    default_language: str = "en"
    min_candidate_score_for_writing: int = 60
    max_pages_per_candidate: int = 8
    require_manual_research_before_final_export: bool = True
    draft_status: str = "draft_needs_review"
    include_source_placeholders: bool = True
    avoid_overclaim_words: list[str] = field(
        default_factory=lambda: ["complete", "verified", "guaranteed", "all", "every", "official"]
    )
    page_type_priority: dict[str, int] = field(
        default_factory=lambda: {
            "codes": 90,
            "wiki": 85,
            "homepage": 82,
            "beginner_guide": 80,
            "guide": 75,
            "tier_list": 75,
            "how_to": 70,
            "values": 65,
            "calculator": 60,
            "items": 55,
            "traits": 55,
            "mutations": 55,
            "faq": 50,
            "map": 50,
            "boss": 50,
            "update": 40,
            "release": 35,
            "news": 25,
        }
    )


@dataclass
class AppConfig:
    sources: list[Source] = field(default_factory=list)
    settings: Settings = field(default_factory=Settings)
    writing: WritingSettings = field(default_factory=WritingSettings)


@dataclass
class SitemapEntry:
    loc: str
    lastmod: str | None = None
