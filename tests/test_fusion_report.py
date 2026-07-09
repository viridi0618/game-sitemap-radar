import json
import sqlite3

from radar.db import init_db
from radar.fusion_report import build_fusion_candidates


def test_fusion_score_favors_strong_roblox_with_light_sitemap_coverage(tmp_path):
    conn = sqlite3.connect(tmp_path / "radar.sqlite")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    conn.execute(
        """
        INSERT INTO roblox_candidate_signals(run_id, universe_id, name, normalized_name, current_rank, playing, visits,
          favorited_count, is_new_entry, score, label, reasoning, created_at)
        VALUES (1, 100, 'Ice Tycoon 2', 'ice tycoon 2', 5, 12000, 100000, 1000, 1, 90, 'HOT - check immediately', 'test', 'now')
        """
    )
    conn.execute(
        """
        INSERT INTO candidate_signals(run_id, normalized_candidate_game, display_game_name, new_url_count, source_count,
          page_types, score, first_seen_at, latest_seen_at, sample_urls, matrix_score, suggested_site_size, matrix_reasoning)
        VALUES (2, 'ice tycoon 2', 'Ice Tycoon 2', 1, 1, ?, 45, 'now', 'now', '[]', 35, 'small_site_6_10_pages', 'light coverage')
        """,
        (json.dumps(["codes"]),),
    )
    conn.commit()
    candidates = build_fusion_candidates(conn)
    assert candidates[0]["name"] == "Ice Tycoon 2"
    assert candidates[0]["fusion_score"] > 60
    assert "light sitemap coverage" in candidates[0]["opportunity"]
    conn.close()
