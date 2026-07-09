from __future__ import annotations

from dataclasses import dataclass

from .game_extractor import normalize_game_name


@dataclass
class RobloxChartGame:
    rank: int
    universe_id: int
    root_place_id: int | None
    name: str
    playing: int = 0
    visits: int = 0
    favorited_count: int = 0
    created: str | None = None
    updated: str | None = None
    url: str | None = None

    @property
    def normalized_name(self) -> str:
        return normalize_game_name(self.name)


@dataclass
class RobloxGameDetails:
    universe_id: int
    root_place_id: int | None = None
    name: str | None = None
    playing: int | None = None
    visits: int | None = None
    favorited_count: int | None = None
    created: str | None = None
    updated: str | None = None
    url: str | None = None
