from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

from .db import insert_roblox_candidate_signals, insert_roblox_snapshots, latest_previous_roblox_snapshots, upsert_roblox_games
from .roblox_scoring import score_roblox_game
from .utils import PROJECT_ROOT, ensure_dirs, utc_now


def store_and_score_roblox_snapshot(conn, run_id: int, games: list, source: str) -> list[dict]:
    upsert_roblox_games(conn, games)
    insert_roblox_snapshots(conn, run_id, games, source)
    previous = latest_previous_roblox_snapshots(conn, run_id)
    signals = []
    for game in games:
        game_row = conn.execute("SELECT first_seen_at FROM roblox_games WHERE universe_id=?", (game.universe_id,)).fetchone()
        signals.append(score_roblox_game(game, previous.get(game.universe_id), game_row["first_seen_at"] if game_row else None))
    signals.sort(key=lambda item: (-item["score"], item["current_rank"] or 999999, item["name"]))
    insert_roblox_candidate_signals(conn, run_id, signals)
    return signals


def latest_roblox_signals(conn) -> list[dict]:
    run = conn.execute("SELECT MAX(run_id) AS run_id FROM roblox_candidate_signals").fetchone()
    if not run or run["run_id"] is None:
        return []
    rows = conn.execute(
        """
        SELECT roblox_candidate_signals.*, roblox_games.url
        FROM roblox_candidate_signals
        LEFT JOIN roblox_games ON roblox_games.universe_id = roblox_candidate_signals.universe_id
        WHERE run_id=?
        ORDER BY score DESC, current_rank ASC
        """,
        (run["run_id"],),
    ).fetchall()
    return [dict(row) for row in rows]


def write_roblox_report(conn, signals: list[dict] | None = None) -> tuple[Path, Path, list[dict]]:
    ensure_dirs()
    signals = signals if signals is not None else latest_roblox_signals(conn)
    today = datetime.now().strftime("%Y-%m-%d")
    md_path = PROJECT_ROOT / "outputs" / f"roblox-report-{today}.md"
    csv_path = PROJECT_ROOT / "outputs" / f"roblox-candidates-{today}.csv"
    lines = ["# Roblox Chart Watcher Report", "", f"Generated at: {utc_now()}", ""]
    if not signals:
        lines.append("No Roblox snapshot signals found. Try `python -m radar.cli import-roblox-chart --csv path/to/roblox-chart.csv`.")
    for idx, signal in enumerate(signals, start=1):
        name = signal["name"]
        lines.extend(
            [
                f"## {idx}. {name}",
                "",
                f"Score: {signal['score']}",
                f"Label: {signal['label']}",
                f"Current rank: {signal['current_rank']}",
                f"Previous rank: {signal.get('previous_rank')}",
                f"Rank delta: {signal.get('rank_delta')}",
                f"Playing: {signal['playing']}",
                f"Previous playing: {signal.get('previous_playing')}",
                f"Playing growth: {_fmt_rate(signal.get('playing_growth_rate'))}",
                f"Visits: {signal['visits']}",
                f"Visits delta: {signal.get('visits_delta')}",
                f"Favorites: {signal['favorited_count']}",
                f"Days since created: {signal.get('days_since_created')}",
                f"Is new entry: {bool(signal.get('is_new_entry'))}",
                f"URL: {signal.get('url') or ''}",
                f"Reasoning: {signal['reasoning']}",
                "",
                "Manual checks:",
                f"- Google Trends: {name} roblox",
                f"- Google Search: {name} codes",
                f"- Google Search: {name} wiki",
                f'- site:fandom.com "{name}"',
                f'- site:progameguides.com "{name}"',
                f'- site:tryhardguides.com "{name}"',
                f'- site:wiki.gg "{name}"',
                "- YouTube last 24h",
                "",
            ]
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    fieldnames = [
        "name",
        "normalized_name",
        "score",
        "label",
        "current_rank",
        "previous_rank",
        "rank_delta",
        "playing",
        "previous_playing",
        "playing_growth_rate",
        "visits",
        "visits_delta",
        "favorited_count",
        "days_since_created",
        "is_new_entry",
        "url",
        "reasoning",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(signals)
    return md_path, csv_path, signals


def _fmt_rate(value) -> str:
    if value is None:
        return "unavailable"
    return f"{value * 100:.1f}%"
