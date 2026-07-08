from radar.db import init_db, insert_or_update_url


def test_duplicate_url_detection(tmp_path):
    import sqlite3

    conn = sqlite3.connect(tmp_path / "radar.sqlite")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    conn.execute(
        "INSERT INTO sources(name, domain, priority) VALUES ('Example', 'example.com', 3)"
    )
    assert insert_or_update_url(conn, 1, "https://example.com/dead-rails-codes/", None, "codes", "Dead Rails", "dead rails", "clear")
    assert not insert_or_update_url(conn, 1, "https://example.com/dead-rails-codes/", None, "codes", "Dead Rails", "dead rails", "clear")
    conn.close()
