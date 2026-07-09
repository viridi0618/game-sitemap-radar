from __future__ import annotations

import csv
from pathlib import Path

import httpx

from .roblox_models import RobloxChartGame, RobloxGameDetails


class RobloxGameProvider:
    def __init__(self, user_agent: str, timeout: int = 20):
        self.client = httpx.Client(
            headers={"User-Agent": user_agent},
            timeout=httpx.Timeout(timeout),
            follow_redirects=True,
        )
        self.last_error: str | None = None

    def close(self) -> None:
        self.client.close()

    def __enter__(self) -> "RobloxGameProvider":
        return self

    def __exit__(self, *_exc) -> None:
        self.close()

    def fetch_chart_games(self, limit: int = 200) -> list[RobloxChartGame]:
        self.last_error = None
        try:
            url = "https://games.roblox.com/v1/games/list"
            params = {"sortToken": "Popular", "maxRows": min(limit, 200)}
            response = self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            raw_games = data.get("games") or data.get("data") or []
            games = []
            for index, item in enumerate(raw_games[:limit], start=1):
                universe_id = _int(item.get("universeId") or item.get("universe_id") or item.get("id"))
                root_place_id = _int(item.get("placeId") or item.get("rootPlaceId") or item.get("root_place_id"))
                name = str(item.get("name") or item.get("title") or f"Roblox Universe {universe_id}")
                games.append(
                    RobloxChartGame(
                        rank=index,
                        universe_id=universe_id,
                        root_place_id=root_place_id,
                        name=name,
                        playing=_int(item.get("playing") or item.get("playerCount")),
                        visits=_int(item.get("visits") or item.get("totalVisits")),
                        favorited_count=_int(item.get("favoritedCount") or item.get("favorited_count")),
                        created=item.get("created"),
                        updated=item.get("updated"),
                        url=_game_url(root_place_id),
                    )
                )
            return [game for game in games if game.universe_id]
        except Exception as exc:
            self.last_error = str(exc)
            return []

    def fetch_game_details(self, universe_ids: list[int]) -> list[RobloxGameDetails]:
        details = []
        for start in range(0, len(universe_ids), 100):
            chunk = universe_ids[start : start + 100]
            try:
                response = self.client.get("https://games.roblox.com/v1/games", params={"universeIds": ",".join(map(str, chunk))})
                response.raise_for_status()
                for item in response.json().get("data", []):
                    universe_id = _int(item.get("id") or item.get("universeId"))
                    root_place_id = _int(item.get("rootPlaceId"))
                    details.append(
                        RobloxGameDetails(
                            universe_id=universe_id,
                            root_place_id=root_place_id,
                            name=item.get("name"),
                            playing=_int(item.get("playing")),
                            visits=_int(item.get("visits")),
                            favorited_count=_int(item.get("favoritedCount")),
                            created=item.get("created"),
                            updated=item.get("updated"),
                            url=_game_url(root_place_id),
                        )
                    )
            except Exception as exc:
                self.last_error = str(exc)
        return details


def merge_details(games: list[RobloxChartGame], details: list[RobloxGameDetails]) -> list[RobloxChartGame]:
    by_universe = {detail.universe_id: detail for detail in details}
    merged = []
    for game in games:
        detail = by_universe.get(game.universe_id)
        if not detail:
            merged.append(game)
            continue
        root_place_id = detail.root_place_id or game.root_place_id
        merged.append(
            RobloxChartGame(
                rank=game.rank,
                universe_id=game.universe_id,
                root_place_id=root_place_id,
                name=detail.name or game.name,
                playing=detail.playing if detail.playing is not None else game.playing,
                visits=detail.visits if detail.visits is not None else game.visits,
                favorited_count=detail.favorited_count if detail.favorited_count is not None else game.favorited_count,
                created=detail.created or game.created,
                updated=detail.updated or game.updated,
                url=detail.url or game.url or _game_url(root_place_id),
            )
        )
    return merged


def read_roblox_chart_csv(path: Path) -> list[RobloxChartGame]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        games = []
        for row in reader:
            root_place_id = _int(row.get("root_place_id"))
            games.append(
                RobloxChartGame(
                    rank=_int(row.get("rank")),
                    universe_id=_int(row.get("universe_id")),
                    root_place_id=root_place_id,
                    name=row.get("name") or "",
                    playing=_int(row.get("playing")),
                    visits=_int(row.get("visits")),
                    favorited_count=_int(row.get("favorited_count")),
                    created=row.get("created") or None,
                    updated=row.get("updated") or None,
                    url=row.get("url") or _game_url(root_place_id),
                )
            )
    return [game for game in games if game.universe_id and game.name]


def _int(value) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _game_url(root_place_id: int | None) -> str | None:
    return f"https://www.roblox.com/games/{root_place_id}" if root_place_id else None
