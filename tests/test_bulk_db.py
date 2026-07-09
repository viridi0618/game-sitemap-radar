import sqlite3

from radar.db import bulk_insert_or_update_urls, init_db


def test_bulk_url_insert_preserves_first_seen_and_updates_last_seen(tmp_path):
    conn = sqlite3.connect(tmp_path / "radar.sqlite")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    conn.execute("INSERT INTO sources(name, domain, priority) VALUES ('Example', 'example.com', 3)")
    rows = [
        {
            "source_id": 1,
            "url": "https://example.com/ice-tycoon-2-codes/",
            "lastmod": None,
            "page_type": "codes",
            "candidate_game": "Ice Tycoon 2",
            "normalized_candidate_game": "ice tycoon 2",
            "name_confidence": "clear",
        }
    ]
    processed, new_count = bulk_insert_or_update_urls(conn, rows)
    first = conn.execute("SELECT * FROM urls WHERE url=?", (rows[0]["url"],)).fetchone()
    rows[0]["lastmod"] = "2026-01-01"
    rows[0]["page_type"] = "wiki"
    processed_again, new_count_again = bulk_insert_or_update_urls(conn, rows)
    updated = conn.execute("SELECT * FROM urls WHERE url=?", (rows[0]["url"],)).fetchone()
    assert (processed, new_count) == (1, 1)
    assert (processed_again, new_count_again) == (1, 0)
    assert updated["first_seen_at"] == first["first_seen_at"]
    assert updated["lastmod"] == "2026-01-01"
    assert updated["page_type"] == "wiki"
    conn.close()
