from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class WritingPagePlan:
    page_type: str
    target_keyword: str
    slug: str
    title: str
    meta_description: str
    h1: str
    intent: str
    priority: int


@dataclass
class WritingProjectPlan:
    normalized_candidate_game: str
    display_game_name: str
    score: int
    page_types: list[str]
    sample_urls: list[str] = field(default_factory=list)
    pages: list[WritingPagePlan] = field(default_factory=list)

