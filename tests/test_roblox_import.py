import sqlite3

from radar.db import init_db, start_run
from radar.roblox_provider import read_roblox_chart_csv
from radar.roblox_report import store_and_score_roblox_snapshot


def test_csv_import_creates_snapshot_rows(tmp_path):
    csv_path = tmp_path / "roblox-chart.csv"
    csv_path.write_text(
        "rank,universe_id,root_place_id,name,playing,visits,favorited_count,created,updated,url\n"
        "1,100,200,Ice Tycoon 2,5000,100000,1000,2026-01-01T00:00:00+00:00,2026-01-02T00:00:00+00:00,https://www.roblox.com/games/200\n",
        encoding="utf-8",
    )
    games = read_roblox_chart_csv(csv_path)
    conn = sqlite3.connect(tmp_path / "radar.sqlite")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    run_id = start_run(conn, 1)
    signals = store_and_score_roblox_snapshot(conn, run_id, games, "manual-csv")
    assert len(signals) == 1
    assert conn.execute("SELECT COUNT(*) AS c FROM roblox_snapshots").fetchone()["c"] == 1
    conn.close()


def test_second_snapshot_calculates_deltas(tmp_path):
    csv_path = tmp_path / "roblox-chart.csv"
    csv_path.write_text(
        "rank,universe_id,root_place_id,name,playing,visits,favorited_count,created,updated,url\n"
        "1,100,200,Ice Tycoon 2,1000,100000,1000,2026-01-01T00:00:00+00:00,2026-01-02T00:00:00+00:00,https://www.roblox.com/games/200\n",
        encoding="utf-8",
    )
    conn = sqlite3.connect(tmp_path / "radar.sqlite")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    first = start_run(conn, 1)
    store_and_score_roblox_snapshot(conn, first, read_roblox_chart_csv(csv_path), "manual-csv")
    csv_path.write_text(
        "rank,universe_id,root_place_id,name,playing,visits,favorited_count,created,updated,url\n"
        "1,100,200,Ice Tycoon 2,3000,250000,1400,2026-01-01T00:00:00+00:00,2026-01-02T00:00:00+00:00,https://www.roblox.com/games/200\n",
        encoding="utf-8",
    )
    second = start_run(conn, 1)
    signals = store_and_score_roblox_snapshot(conn, second, read_roblox_chart_csv(csv_path), "manual-csv")
    assert signals[0]["playing_delta"] == 2000
    assert signals[0]["visits_delta"] == 150000
    conn.close()


def test_csv_import_requires_minimum_columns(tmp_path):
    csv_path = tmp_path / "bad-roblox-chart.csv"
    csv_path.write_text("rank,name\n1,Ice Tycoon 2\n", encoding="utf-8")
    try:
        read_roblox_chart_csv(csv_path)
    except ValueError as exc:
        assert "missing required columns" in str(exc)
        assert "universe_id" in str(exc)
    else:
        raise AssertionError("Expected missing required columns error")


def test_csv_import_allows_minimum_columns(tmp_path):
    csv_path = tmp_path / "minimal-roblox-chart.csv"
    csv_path.write_text("rank,universe_id,name\n1,100,Ice Tycoon 2\n", encoding="utf-8")
    games = read_roblox_chart_csv(csv_path)
    assert games[0].playing == 0
    assert games[0].visits == 0
    assert games[0].favorited_count == 0
