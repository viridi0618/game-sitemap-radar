from __future__ import annotations

from datetime import datetime, timezone

from .utils import parse_dt


HIGH_VALUE_TYPES = {
    "codes",
    "wiki",
    "guide",
    "tier_list",
    "how_to",
    "values",
    "calculator",
    "traits",
    "mutations",
    "items",
}


def score_source_count(count: int) -> int:
    if count >= 4:
        return 30
    return {1: 8, 2: 18, 3: 25}.get(count, 0)


def score_url_count(count: int) -> int:
    if count >= 8:
        return 20
    if count >= 4:
        return 15
    if count >= 2:
        return 10
    return 5 if count == 1 else 0


def score_page_types(page_types: set[str]) -> int:
    high = len(page_types & HIGH_VALUE_TYPES)
    if high >= 3:
        return 20
    if high == 2:
        return 15
    if high == 1:
        return 10
    if page_types & {"news", "release", "update"}:
        return 5
    return 0


def score_recency(first_seen_at: str, now: datetime | None = None) -> int:
    now = now or datetime.now(timezone.utc)
    first_seen = parse_dt(first_seen_at)
    if not first_seen:
        return 0
    hours = (now - first_seen).total_seconds() / 3600
    if hours <= 24:
        return 10
    if hours <= 72:
        return 7
    if hours <= 168:
        return 3
    return 0


def score_name_quality(confidence: str) -> int:
    return {"clear": 5, "medium": 3, "low": 1}.get(confidence, 1)


def label_for_score(score: int) -> str:
    if score >= 80:
        return "HOT - manual review immediately"
    if score >= 60:
        return "WATCH - verify with Google Trends and SERP"
    if score >= 40:
        return "LOW - observe only"
    return "IGNORE"


def score_candidate(
    source_count: int,
    new_url_count: int,
    page_types: set[str],
    source_priority_sum: int,
    first_seen_at: str,
    name_confidence: str = "clear",
    now: datetime | None = None,
) -> int:
    return min(
        100,
        score_source_count(source_count)
        + score_url_count(new_url_count)
        + score_page_types(page_types)
        + min(source_priority_sum, 15)
        + score_recency(first_seen_at, now=now)
        + score_name_quality(name_confidence),
    )

