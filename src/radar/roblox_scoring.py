from __future__ import annotations

from datetime import datetime, timezone

from .utils import parse_dt


def label_for_roblox_score(score: int) -> str:
    if score >= 80:
        return "HOT - check immediately"
    if score >= 60:
        return "WATCH - manual review"
    if score >= 40:
        return "LOW - observe"
    return "IGNORE"


def score_roblox_game(game, previous=None, first_seen_at: str | None = None, now: datetime | None = None) -> dict:
    now = now or datetime.now(timezone.utc)
    is_new_entry = previous is None
    days_since_first_seen = _days_since(first_seen_at, now)
    days_since_created = _days_since(game.created, now)
    previous_playing = previous["playing"] if previous else None
    previous_visits = previous["visits"] if previous else None
    previous_favorites = previous["favorited_count"] if previous else None
    previous_rank = previous["rank"] if previous else None
    playing_delta = _delta(game.playing, previous_playing)
    visits_delta = _delta(game.visits, previous_visits)
    favorite_delta = _delta(game.favorited_count, previous_favorites)
    playing_growth_rate = _growth_rate(game.playing, previous_playing)
    visits_growth_rate = _growth_rate(game.visits, previous_visits)
    rank_delta = (previous_rank - game.rank) if previous_rank else None

    parts = []
    score = 0
    new_score = 20 if is_new_entry else 15 if days_since_first_seen is not None and days_since_first_seen <= 3 else 0
    score += new_score
    parts.append(f"new entry {new_score}")

    playing_score = _playing_score(game.playing)
    score += playing_score
    parts.append(f"playing {playing_score}")

    growth_score = _playing_growth_score(playing_growth_rate)
    score += growth_score
    parts.append("First snapshot; growth unavailable." if previous is None else f"playing growth {growth_score}")

    visits_score = _visits_growth_score(visits_delta)
    score += visits_score
    parts.append("visits growth unavailable" if previous is None else f"visits growth {visits_score}")

    launch_score = _launch_window_score(days_since_created)
    score += launch_score
    parts.append(f"launch window {launch_score}")

    movement_score = _rank_movement_score(rank_delta, is_new_entry)
    score += movement_score
    parts.append(f"rank movement {movement_score}")

    score = min(100, score)
    return {
        "universe_id": game.universe_id,
        "name": game.name,
        "normalized_name": game.normalized_name,
        "current_rank": game.rank,
        "previous_rank": previous_rank,
        "rank_delta": rank_delta,
        "playing": game.playing,
        "previous_playing": previous_playing,
        "playing_delta": playing_delta,
        "playing_growth_rate": playing_growth_rate,
        "visits": game.visits,
        "previous_visits": previous_visits,
        "visits_delta": visits_delta,
        "visits_growth_rate": visits_growth_rate,
        "favorited_count": game.favorited_count,
        "previous_favorited_count": previous_favorites,
        "favorite_delta": favorite_delta,
        "days_since_created": days_since_created,
        "is_new_entry": is_new_entry,
        "score": score,
        "label": label_for_roblox_score(score),
        "reasoning": "; ".join(parts),
        "url": game.url,
    }


def _playing_score(playing: int) -> int:
    if playing >= 10000:
        return 20
    if playing >= 3000:
        return 15
    if playing >= 1000:
        return 10
    if playing >= 300:
        return 5
    return 0


def _playing_growth_score(rate: float | None) -> int:
    if rate is None:
        return 0
    if rate >= 3:
        return 20
    if rate >= 1:
        return 15
    if rate >= 0.3:
        return 10
    if rate >= 0.1:
        return 5
    return 0


def _visits_growth_score(delta: int | None) -> int:
    if delta is None:
        return 0
    if delta >= 1_000_000:
        return 20
    if delta >= 300_000:
        return 15
    if delta >= 100_000:
        return 10
    if delta >= 30_000:
        return 5
    return 0


def _launch_window_score(days: int | None) -> int:
    if days is None:
        return 0
    if days <= 14:
        return 12
    if days <= 60:
        return 15
    if days <= 180:
        return 8
    return 2


def _rank_movement_score(delta: int | None, is_new_entry: bool) -> int:
    if is_new_entry:
        return 5
    if delta is None or delta <= 0:
        return 0
    if delta >= 50:
        return 5
    if delta >= 10:
        return 3
    return 0


def _growth_rate(current: int, previous: int | None) -> float | None:
    if previous is None or previous <= 0:
        return None
    return (current - previous) / previous


def _delta(current: int, previous: int | None) -> int | None:
    return None if previous is None else current - previous


def _days_since(value: str | None, now: datetime) -> int | None:
    parsed = parse_dt(value)
    if not parsed:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return max(0, int((now - parsed).total_seconds() // 86400))
