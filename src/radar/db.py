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
          include_url_keywords TEXT,
          exclude_url_keywords TEXT,
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
        CREATE TABLE IF NOT EXISTS writing_projects (
          id INTEGER PRIMARY KEY,
          normalized_candidate_game TEXT UNIQUE,
          display_game_name TEXT,
          source_signal_score INTEGER,
          created_at TEXT,
          updated_at TEXT,
          status TEXT,
          notes TEXT
        );
        CREATE TABLE IF NOT EXISTS writing_pages (
          id INTEGER PRIMARY KEY,
          project_id INTEGER,
          page_type TEXT,
          target_keyword TEXT,
          slug TEXT,
          title TEXT,
          meta_description TEXT,
          h1 TEXT,
          intent TEXT,
          priority INTEGER,
          status TEXT,
          created_at TEXT,
          updated_at TEXT,
          UNIQUE(project_id, page_type)
        );
        CREATE TABLE IF NOT EXISTS writing_briefs (
          id INTEGER PRIMARY KEY,
          page_id INTEGER UNIQUE,
          brief_json TEXT,
          created_at TEXT,
          updated_at TEXT
        );
        CREATE TABLE IF NOT EXISTS writing_drafts (
          id INTEGER PRIMARY KEY,
          page_id INTEGER UNIQUE,
          draft_markdown TEXT,
          quality_flags TEXT,
          source_placeholders TEXT,
          created_at TEXT,
          updated_at TEXT
        );
        CREATE TABLE IF NOT EXISTS manual_research_notes (
          id INTEGER PRIMARY KEY,
          project_id INTEGER,
          source_name TEXT,
          source_url TEXT,
          note TEXT,
          created_at TEXT
        );
        """
    )
    _ensure_column(conn, "sources", "include_url_keywords", "TEXT")
    _ensure_column(conn, "sources", "exclude_url_keywords", "TEXT")
    conn.commit()


def _ensure_column(conn: sqlite3.Connection, table: str, column: str, decl: str) -> None:
    columns = {row["name"] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()}
    if column not in columns:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {decl}")


def upsert_source(conn: sqlite3.Connection, source) -> int:
    now = utc_now()
    conn.execute(
        """
        INSERT INTO sources(name, domain, sitemap_url, site_type, language, priority, include_url_keywords, exclude_url_keywords, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(domain) DO UPDATE SET
          name=excluded.name,
          sitemap_url=excluded.sitemap_url,
          site_type=excluded.site_type,
          language=excluded.language,
          priority=excluded.priority,
          include_url_keywords=excluded.include_url_keywords,
          exclude_url_keywords=excluded.exclude_url_keywords,
          updated_at=excluded.updated_at
        """,
        (
            source.name,
            source.domain,
            source.sitemap_url,
            source.site_type,
            source.language,
            source.priority,
            json.dumps(source.include_url_keywords),
            json.dumps(source.exclude_url_keywords),
            now,
            now,
        ),
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


def upsert_writing_project(conn: sqlite3.Connection, candidate: dict, status: str = "planned", notes: str | None = None) -> int:
    now = utc_now()
    conn.execute(
        """
        INSERT INTO writing_projects(normalized_candidate_game, display_game_name, source_signal_score, created_at, updated_at, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(normalized_candidate_game) DO UPDATE SET
          display_game_name=excluded.display_game_name,
          source_signal_score=excluded.source_signal_score,
          updated_at=excluded.updated_at,
          status=excluded.status,
          notes=COALESCE(excluded.notes, writing_projects.notes)
        """,
        (
            candidate["normalized_candidate_game"],
            candidate["display_game_name"],
            int(candidate.get("score", 0)),
            now,
            now,
            status,
            notes,
        ),
    )
    row = conn.execute(
        "SELECT id FROM writing_projects WHERE normalized_candidate_game=?",
        (candidate["normalized_candidate_game"],),
    ).fetchone()
    conn.commit()
    return int(row["id"])


def upsert_writing_page(conn: sqlite3.Connection, project_id: int, page: dict, status: str = "planned") -> int:
    now = utc_now()
    conn.execute(
        """
        INSERT INTO writing_pages(project_id, page_type, target_keyword, slug, title, meta_description, h1, intent, priority, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(project_id, page_type) DO UPDATE SET
          target_keyword=excluded.target_keyword,
          slug=excluded.slug,
          title=excluded.title,
          meta_description=excluded.meta_description,
          h1=excluded.h1,
          intent=excluded.intent,
          priority=excluded.priority,
          status=excluded.status,
          updated_at=excluded.updated_at
        """,
        (
            project_id,
            page["page_type"],
            page["target_keyword"],
            page["slug"],
            page["title"],
            page["meta_description"],
            page["h1"],
            page["intent"],
            int(page["priority"]),
            status,
            now,
            now,
        ),
    )
    row = conn.execute("SELECT id FROM writing_pages WHERE project_id=? AND page_type=?", (project_id, page["page_type"])).fetchone()
    conn.commit()
    return int(row["id"])


def upsert_writing_brief(conn: sqlite3.Connection, page_id: int, brief: dict) -> None:
    now = utc_now()
    conn.execute(
        """
        INSERT INTO writing_briefs(page_id, brief_json, created_at, updated_at)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(page_id) DO UPDATE SET brief_json=excluded.brief_json, updated_at=excluded.updated_at
        """,
        (page_id, json.dumps(brief, ensure_ascii=False, indent=2), now, now),
    )
    conn.commit()


def upsert_writing_draft(conn: sqlite3.Connection, page_id: int, draft_markdown: str, quality_flags: list[str], source_placeholders: list[str]) -> None:
    now = utc_now()
    conn.execute(
        """
        INSERT INTO writing_drafts(page_id, draft_markdown, quality_flags, source_placeholders, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(page_id) DO UPDATE SET
          draft_markdown=excluded.draft_markdown,
          quality_flags=excluded.quality_flags,
          source_placeholders=excluded.source_placeholders,
          updated_at=excluded.updated_at
        """,
        (page_id, draft_markdown, json.dumps(quality_flags), json.dumps(source_placeholders), now, now),
    )
    conn.commit()


def add_manual_research_note(conn: sqlite3.Connection, project_id: int, source_name: str, source_url: str, note: str) -> None:
    conn.execute(
        "INSERT INTO manual_research_notes(project_id, source_name, source_url, note, created_at) VALUES (?, ?, ?, ?, ?)",
        (project_id, source_name, source_url, note, utc_now()),
    )
    conn.commit()
