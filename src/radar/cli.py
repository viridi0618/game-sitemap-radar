from __future__ import annotations

import argparse
import csv
import shutil
import sys
import time
from pathlib import Path

from .config import init_config_files, load_config, load_rules
from .db import (
    connect,
    finish_run,
    init_db,
    insert_candidate_signal,
    insert_or_update_url,
    start_run,
    upsert_sitemap,
    upsert_source,
)
from .fetcher import Fetcher
from .game_extractor import extract_candidate_game
from .report import build_candidates, write_reports
from .robots import discover_sitemap_urls
from .sitemap_parser import parse_sitemap_xml
from .url_classifier import classify_page_type
from .utils import PROJECT_ROOT, ensure_dirs


def cmd_init(_args) -> int:
    ensure_dirs()
    init_config_files()
    with connect() as conn:
        init_db(conn)
    print(f"Initialized database at {PROJECT_ROOT / 'data' / 'radar.sqlite'}")
    print(f"Seed config ready at {PROJECT_ROOT / 'config' / 'seeds.yaml'}")
    return 0


def cmd_discover(_args) -> int:
    config = load_config()
    with connect() as conn:
        init_db(conn)
        fetcher = Fetcher(config.settings.user_agent, config.settings.request_timeout_seconds)
        for index, source in enumerate(config.sources, start=1):
            print(f"[discover {index}/{len(config.sources)}] {source.domain}", flush=True)
            source_id = upsert_source(conn, source)
            sitemap_urls, robots_result = discover_sitemap_urls(source.domain, fetcher, source.sitemap_url)
            if robots_result and robots_result.error:
                upsert_sitemap(conn, source_id, robots_result.url, "robots", robots_result.status_code, robots_result.error)
            for url in sitemap_urls[: config.settings.max_sitemaps_per_source]:
                upsert_sitemap(conn, source_id, url)
            time.sleep(config.settings.delay_seconds_per_source)
    print(f"Discovered sitemap candidates for {len(config.sources)} sources.")
    return 0


def _crawl_source(conn, source_row, settings, rules, fetcher) -> tuple[int, int, int]:
    sitemap_rows = conn.execute(
        "SELECT sitemap_url FROM sitemaps WHERE source_id=? AND sitemap_type != 'robots'",
        (source_row["id"],),
    ).fetchall()
    queue = [row["sitemap_url"] for row in sitemap_rows]
    seen_sitemaps = set()
    sitemap_count = 0
    url_count = 0
    new_url_count = 0
    error_count = 0

    while queue and sitemap_count < settings.max_sitemaps_per_source:
        sitemap_url = queue.pop(0)
        if sitemap_url in seen_sitemaps:
            continue
        seen_sitemaps.add(sitemap_url)
        print(f"  fetching sitemap {len(seen_sitemaps)}/{settings.max_sitemaps_per_source}: {sitemap_url}", flush=True)
        result = fetcher.fetch(sitemap_url)
        if result.error or result.status_code >= 400 or result.status_code == 0:
            upsert_sitemap(conn, source_row["id"], sitemap_url, "unknown", result.status_code, result.error or f"HTTP {result.status_code}")
            error_count += 1
            continue
        try:
            sitemap_type, entries = parse_sitemap_xml(result.body)
        except Exception as exc:
            upsert_sitemap(conn, source_row["id"], sitemap_url, "unknown", result.status_code, str(exc))
            error_count += 1
            continue
        sitemap_count += 1
        upsert_sitemap(conn, source_row["id"], sitemap_url, sitemap_type, result.status_code, None)
        if sitemap_type == "index":
            for entry in entries:
                if len(seen_sitemaps) + len(queue) < settings.max_sitemaps_per_source:
                    queue.append(entry.loc)
        elif sitemap_type == "urlset":
            for entry in entries[: settings.max_urls_per_sitemap]:
                page_type = classify_page_type(entry.loc, rules)
                candidate = extract_candidate_game(entry.loc)
                is_new = insert_or_update_url(
                    conn,
                    source_row["id"],
                    entry.loc,
                    entry.lastmod,
                    page_type,
                    candidate.display,
                    candidate.normalized,
                    candidate.confidence,
                )
                url_count += 1
                if is_new:
                    new_url_count += 1
    return sitemap_count, url_count, new_url_count + 0, error_count


def cmd_crawl(_args) -> int:
    config = load_config()
    rules = load_rules()
    with connect() as conn:
        init_db(conn)
        for source in config.sources:
            upsert_source(conn, source)
        sources = conn.execute("SELECT * FROM sources").fetchall()
        run_id = start_run(conn, len(sources))
        totals = [0, 0, 0, 0]
        fetcher = Fetcher(config.settings.user_agent, config.settings.request_timeout_seconds)
        for index, source_row in enumerate(sources, start=1):
            print(f"[crawl {index}/{len(sources)}] {source_row['domain']}", flush=True)
            sitemap_count, url_count, new_url_count, error_count = _crawl_source(conn, source_row, config.settings, rules, fetcher)
            print(
                f"  done: {sitemap_count} sitemaps, {url_count} URLs, {new_url_count} new, {error_count} errors",
                flush=True,
            )
            totals[0] += sitemap_count
            totals[1] += url_count
            totals[2] += new_url_count
            totals[3] += error_count
            time.sleep(config.settings.delay_seconds_per_source)
        finish_run(conn, run_id, totals[0], totals[1], totals[2], totals[3])
    print(f"Crawled {totals[0]} sitemaps, saw {totals[1]} URLs, found {totals[2]} new URLs.")
    return 0


def cmd_report(_args) -> int:
    config = load_config()
    with connect() as conn:
        init_db(conn)
        run = conn.execute("SELECT id FROM runs ORDER BY id DESC LIMIT 1").fetchone()
        run_id = int(run["id"]) if run else None
        md_path, csv_path, candidates = write_reports(conn, config.settings.report_window_hours, run_id)
        if run_id:
            for candidate in candidates:
                insert_candidate_signal(conn, run_id, candidate)
    print(f"Wrote report: {md_path}")
    print(f"Wrote CSV: {csv_path}")
    return 0


def cmd_run(args) -> int:
    print("== init ==", flush=True)
    cmd_init(args)
    print("== discover ==", flush=True)
    cmd_discover(args)
    print("== crawl ==", flush=True)
    cmd_crawl(args)
    print("== report ==", flush=True)
    cmd_report(args)
    return 0


def cmd_export(_args) -> int:
    ensure_dirs()
    path = PROJECT_ROOT / "outputs" / "all-new-urls.csv"
    with connect() as conn, path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["domain", "url", "first_seen_at", "page_type", "candidate_game"])
        rows = conn.execute(
            """
            SELECT sources.domain, urls.url, urls.first_seen_at, urls.page_type, urls.candidate_game
            FROM urls JOIN sources ON sources.id = urls.source_id
            ORDER BY urls.first_seen_at DESC
            """
        ).fetchall()
        for row in rows:
            writer.writerow([row["domain"], row["url"], row["first_seen_at"], row["page_type"], row["candidate_game"]])
    print(f"Exported URLs: {path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Game Sitemap Radar")
    sub = parser.add_subparsers(dest="command", required=True)
    for name, func in {
        "init": cmd_init,
        "discover": cmd_discover,
        "crawl": cmd_crawl,
        "report": cmd_report,
        "run": cmd_run,
        "export": cmd_export,
    }.items():
        cmd = sub.add_parser(name)
        cmd.set_defaults(func=func)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
