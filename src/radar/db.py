from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from .utils import PROJECT_ROOT, ensure_dirs, url_hash, utc_now


DB_PATH = PROJECT_ROOT / "data" / "radar.sqlite"


def connect(path: Path | None = None) -> sqlite3.Connection:
    ensure_dirs()
    db_path = path or DB_PATH
    if db_path.exists() and 0 < db_path.stat().st_size <= 8:
        db_path.write_bytes(b"")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS sources (
          id INTEGER PRIMARY KEY,
          name TEXT,
          domain TEXT UNIQUE,
          sitemap_url TEXT,
          site_type TEXT,
          language TEXT,
          priority INTEGER,
          created_at TEXT,
          updated_at TEXT
        );
        CREATE TABLE IF NOT EXISTS sitemaps (
          id INTEGER PRIMARY KEY,
          source_id INTEGER,
          sitemap_url TEXT,
          sitemap_type TEXT,
          status_code INTEGER,
          last_fetched_at TEXT,
          error TEXT,
          UNIQUE(source_id, sitemap_url)
        );
        CREATE TABLE IF NOT EXISTS urls (
          id INTEGER PRIMARY KEY,
          source_id INTEGER,
          url TEXT UNIQUE,
          url_hash TEXT UNIQUE,
          lastmod TEXT,
          first_seen_at TEXT,
          last_seen_at TEXT,
          page_type TEXT,
          candidate_game TEXT,
          normalized_candidate_game TEXT,
          name_confidence TEXT
        );
        CREATE TABLE IF NOT EXISTS runs (
          id INTEGER PRIMARY KEY,
          started_at TEXT,
          finished_at TEXT,
          source_count INTEGER,
          sitemap_count INTEGER,
          url_count INTEGER,
          new_url_count INTEGER,
          error_count INTEGER
        );
        CREATE TABLE IF NOT EXISTS candidate_signals (
          id INTEGER PRIMARY KEY,
          run_id INTEGER,
          normalized_candidate_game TEXT,
          display_game_name TEXT,
          new_url_count INTEGER,
          source_count INTEGER,
          page_types TEXT,
          score INTEGER,
          first_seen_at TEXT,
          latest_seen_at TEXT,
          sample_urls TEXT
        );
        """
    )
    conn.commit()


def upsert_source(conn: sqlite3.Connection, source) -> int:
    now = utc_now()
    conn.execute(
        """
        INSERT INTO sources(name, domain, sitemap_url, site_type, language, priority, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(domain) DO UPDATE SET
          name=excluded.name,
          sitemap_url=excluded.sitemap_url,
          site_type=excluded.site_type,
          language=excluded.language,
          priority=excluded.priority,
          updated_at=excluded.updated_at
        """,
        (source.name, source.domain, source.sitemap_url, source.site_type, source.language, source.priority, now, now),
    )
    row = conn.execute("SELECT id FROM sources WHERE domain = ?", (source.domain,)).fetchone()
    conn.commit()
    return int(row["id"])


def upsert_sitemap(
    conn: sqlite3.Connection,
    source_id: int,
    sitemap_url: str,
    sitemap_type: str = "unknown",
    status_code: int | None = None,
    error: str | None = None,
) -> None:
    conn.execute(
        """
        INSERT INTO sitemaps(source_id, sitemap_url, sitemap_type, status_code, last_fetched_at, error)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(source_id, sitemap_url) DO UPDATE SET
          sitemap_type=excluded.sitemap_type,
          status_code=excluded.status_code,
          last_fetched_at=excluded.last_fetched_at,
          error=excluded.error
        """,
        (source_id, sitemap_url, sitemap_type, status_code, utc_now(), error),
    )
    conn.commit()


def insert_or_update_url(
    conn: sqlite3.Connection,
    source_id: int,
    url: str,
    lastmod: str | None,
    page_type: str,
    candidate_game: str,
    normalized_candidate_game: str,
    name_confidence: str,
) -> bool:
    now = utc_now()
    digest = url_hash(url)
    existing = conn.execute("SELECT id FROM urls WHERE url_hash = ?", (digest,)).fetchone()
    if existing:
        conn.execute(
            """
            UPDATE urls SET last_seen_at=?, lastmod=?, page_type=?, candidate_game=?,
              normalized_candidate_game=?, name_confidence=? WHERE url_hash=?
            """,
            (now, lastmod, page_type, candidate_game, normalized_candidate_game, name_confidence, digest),
        )
        conn.commit()
        return False
    conn.execute(
        """
        INSERT INTO urls(source_id, url, url_hash, lastmod, first_seen_at, last_seen_at,
                         page_type, candidate_game, normalized_candidate_game, name_confidence)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (source_id, url, digest, lastmod, now, now, page_type, candidate_game, normalized_candidate_game, name_confidence),
    )
    conn.commit()
    return True


def start_run(conn: sqlite3.Connection, source_count: int) -> int:
    cur = conn.execute(
        "INSERT INTO runs(started_at, source_count, sitemap_count, url_count, new_url_count, error_count) VALUES (?, ?, 0, 0, 0, 0)",
        (utc_now(), source_count),
    )
    conn.commit()
    return int(cur.lastrowid)


def finish_run(conn: sqlite3.Connection, run_id: int, sitemap_count: int, url_count: int, new_url_count: int, error_count: int) -> None:
    conn.execute(
        """
        UPDATE runs SET finished_at=?, sitemap_count=?, url_count=?, new_url_count=?, error_count=?
        WHERE id=?
        """,
        (utc_now(), sitemap_count, url_count, new_url_count, error_count, run_id),
    )
    conn.commit()


def insert_candidate_signal(conn: sqlite3.Connection, run_id: int, candidate: dict) -> None:
    conn.execute(
        """
        INSERT INTO candidate_signals(run_id, normalized_candidate_game, display_game_name, new_url_count,
          source_count, page_types, score, first_seen_at, latest_seen_at, sample_urls)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            run_id,
            candidate["normalized_candidate_game"],
            candidate["display_game_name"],
            candidate["new_url_count"],
            candidate["source_count"],
            json.dumps(candidate["page_types"]),
            candidate["score"],
            candidate["first_seen_at"],
            candidate["latest_seen_at"],
            json.dumps(candidate["sample_urls"]),
        ),
    )
    conn.commit()
