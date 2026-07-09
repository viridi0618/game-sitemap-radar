from __future__ import annotations

import argparse
import csv
import json
import shutil
import sys
import time
from pathlib import Path

from .config import init_config_files, load_config, load_rules
from .db import (
    add_manual_research_note,
    bulk_insert_or_update_urls,
    connect,
    finish_run,
    init_db,
    insert_candidate_signal,
    insert_candidate_signals,
    insert_or_update_url,
    start_run,
    upsert_writing_brief,
    upsert_writing_draft,
    upsert_writing_page,
    upsert_writing_project,
    upsert_sitemap,
    upsert_source,
)
from .brief_generator import generate_brief
from .draft_generator import generate_draft
from .exporter import export_brief, export_draft, export_plan, export_task_list
from .fetcher import Fetcher
from .game_extractor import extract_candidate_game
from .report import build_candidates, write_reports
from .review import check_draft
from .roblox_provider import RobloxGameProvider, enrich_missing_details, merge_details, read_roblox_chart_csv
from .roblox_report import store_and_score_roblox_snapshot, write_roblox_report
from .robots import discover_sitemap_urls
from .sitemap_parser import parse_sitemap_xml
from .url_classifier import classify_page_type
from .utils import PROJECT_ROOT, ensure_dirs
from .fusion_report import write_fusion_report
from .writing_planner import candidate_from_db_row, create_writing_plan, slugify_game


LAST_CRAWL_STATS: dict | None = None


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
        with Fetcher(config.settings.user_agent, config.settings.request_timeout_seconds) as fetcher:
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


def _url_allowed(url: str, source_row) -> bool:
    lowered = url.lower()
    include = json.loads(source_row["include_url_keywords"] or "[]") if "include_url_keywords" in source_row.keys() else []
    exclude = json.loads(source_row["exclude_url_keywords"] or "[]") if "exclude_url_keywords" in source_row.keys() else []
    if include and not any(token.lower() in lowered for token in include):
        return False
    if exclude and any(token.lower() in lowered for token in exclude):
        return False
    return True


def _crawl_source(conn, source_row, settings, rules, fetcher, run_state: dict) -> tuple[int, int, int, int, int, bool]:
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
    filtered_count = 0
    cap_hit = False

    while queue and sitemap_count < settings.max_sitemaps_per_source:
        if run_state["sitemaps"] >= settings.max_total_sitemaps_per_run or run_state["urls"] >= settings.max_total_urls_per_run:
            cap_hit = True
            break
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
        run_state["sitemaps"] += 1
        upsert_sitemap(conn, source_row["id"], sitemap_url, sitemap_type, result.status_code, None)
        if sitemap_type == "index":
            for entry in entries:
                if len(seen_sitemaps) + len(queue) < settings.max_sitemaps_per_source and run_state["sitemaps"] + len(queue) < settings.max_total_sitemaps_per_run:
                    queue.append(entry.loc)
        elif sitemap_type == "urlset":
            rows = []
            for entry in entries[: settings.max_urls_per_sitemap]:
                if run_state["urls"] + len(rows) >= settings.max_total_urls_per_run:
                    cap_hit = True
                    break
                if not _url_allowed(entry.loc, source_row):
                    filtered_count += 1
                    continue
                page_type = classify_page_type(entry.loc, rules)
                candidate = extract_candidate_game(entry.loc)
                rows.append(
                    {
                        "source_id": source_row["id"],
                        "url": entry.loc,
                        "lastmod": entry.lastmod,
                        "page_type": page_type,
                        "candidate_game": candidate.display,
                        "normalized_candidate_game": candidate.normalized,
                        "name_confidence": candidate.confidence,
                    }
                )
            processed, new_count = bulk_insert_or_update_urls(conn, rows)
            url_count += processed
            new_url_count += new_count
            run_state["urls"] += processed
            if cap_hit:
                break
    return sitemap_count, url_count, new_url_count, error_count, filtered_count, cap_hit


def cmd_crawl(_args) -> int:
    global LAST_CRAWL_STATS
    config = load_config()
    rules = load_rules()
    with connect() as conn:
        init_db(conn)
        for source in config.sources:
            upsert_source(conn, source)
        sources = conn.execute("SELECT * FROM sources").fetchall()
        run_id = start_run(conn, len(sources))
        totals = [0, 0, 0, 0, 0]
        run_state = {"sitemaps": 0, "urls": 0}
        started = time.perf_counter()
        cap_hit = False
        with Fetcher(config.settings.user_agent, config.settings.request_timeout_seconds) as fetcher:
            for index, source_row in enumerate(sources, start=1):
                source_started = time.perf_counter()
                print(f"[crawl {index}/{len(sources)}] {source_row['domain']}", flush=True)
                sitemap_count, url_count, new_url_count, error_count, filtered_count, source_cap_hit = _crawl_source(
                    conn, source_row, config.settings, rules, fetcher, run_state
                )
                elapsed = time.perf_counter() - source_started
                print(
                    f"  done: {sitemap_count} sitemaps, {url_count} URLs, {new_url_count} new, {error_count} errors, {filtered_count} filtered, {elapsed:.2f}s",
                    flush=True,
                )
                totals[0] += sitemap_count
                totals[1] += url_count
                totals[2] += new_url_count
                totals[3] += error_count
                totals[4] += filtered_count
                cap_hit = cap_hit or source_cap_hit
                if cap_hit:
                    print(
                        f"  stopping gracefully: crawl cap hit ({run_state['sitemaps']} sitemaps, {run_state['urls']} URLs).",
                        flush=True,
                    )
                    break
                time.sleep(config.settings.delay_seconds_per_source)
        finish_run(conn, run_id, totals[0], totals[1], totals[2], totals[3])
    elapsed = time.perf_counter() - started
    urls_per_second = totals[1] / elapsed if elapsed else 0
    print(f"Crawled {totals[0]} sitemaps, saw {totals[1]} URLs, found {totals[2]} new URLs.")
    print(f"Total elapsed: {elapsed:.2f}s; average URLs/second: {urls_per_second:.2f}; total errors: {totals[3]}; filtered URLs: {totals[4]}.")
    if cap_hit:
        print("Crawl cap was hit; increase max_total_urls_per_run or max_total_sitemaps_per_run if needed.")
    LAST_CRAWL_STATS = {
        "elapsed_seconds": elapsed,
        "urls_per_second": urls_per_second,
        "error_count": totals[3],
        "filtered_url_count": totals[4],
    }
    return 0


def cmd_report(_args) -> int:
    config = load_config()
    with connect() as conn:
        init_db(conn)
        run = conn.execute("SELECT id FROM runs ORDER BY id DESC LIMIT 1").fetchone()
        run_id = int(run["id"]) if run else None
        md_path, csv_path, candidates = write_reports(conn, config.settings.report_window_hours, run_id, LAST_CRAWL_STATS)
        if run_id:
            insert_candidate_signals(conn, run_id, candidates)
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


def _find_candidate(conn, name: str) -> dict | None:
    normalized = " ".join(name.lower().split())
    row = conn.execute(
        """
        SELECT * FROM candidate_signals
        WHERE lower(display_game_name)=lower(?) OR normalized_candidate_game=?
        ORDER BY score DESC, id DESC LIMIT 1
        """,
        (name, normalized),
    ).fetchone()
    if row:
        return candidate_from_db_row(row)
    url_row = conn.execute(
        """
        SELECT normalized_candidate_game, candidate_game AS display_game_name,
               COUNT(*) AS new_url_count, COUNT(DISTINCT source_id) AS source_count,
               '[' || group_concat(DISTINCT '"' || page_type || '"') || ']' AS page_types,
               0 AS score, MIN(first_seen_at) AS first_seen_at, MAX(first_seen_at) AS latest_seen_at,
               '[' || group_concat('"' || url || '"') || ']' AS sample_urls
        FROM urls
        WHERE lower(candidate_game)=lower(?) OR normalized_candidate_game=?
        GROUP BY normalized_candidate_game, candidate_game
        LIMIT 1
        """,
        (name, normalized),
    ).fetchone()
    return candidate_from_db_row(url_row) if url_row else None


def _find_project(conn, name: str):
    normalized = " ".join(name.lower().split())
    return conn.execute(
        "SELECT * FROM writing_projects WHERE lower(display_game_name)=lower(?) OR normalized_candidate_game=? ORDER BY id DESC LIMIT 1",
        (name, normalized),
    ).fetchone()


def cmd_plan_writing(args) -> int:
    config = load_config()
    with connect() as conn:
        init_db(conn)
        candidate = _find_candidate(conn, args.candidate)
        if not candidate:
            candidate = {
                "normalized_candidate_game": " ".join(args.candidate.lower().split()),
                "display_game_name": args.candidate,
                "score": 0,
                "page_types": [],
                "sample_urls": [],
            }
        if candidate["score"] < config.writing.min_candidate_score_for_writing and not args.force:
            print(
                f"Candidate score {candidate['score']} is below writing threshold {config.writing.min_candidate_score_for_writing}. Use --force to create a writing project."
            )
            return 2
        plan = create_writing_plan(candidate, config.writing)
        project_id = upsert_writing_project(conn, candidate, status="planned")
        for page in plan.pages:
            upsert_writing_page(conn, project_id, page.__dict__, status="planned")
        json_path, md_path = export_plan(plan)
    print(f"Created writing project: {plan.display_game_name}")
    print(f"Wrote plan JSON: {json_path}")
    print(f"Wrote plan Markdown: {md_path}")
    return 0


def cmd_generate_briefs(args) -> int:
    config = load_config()
    with connect() as conn:
        init_db(conn)
        project = _find_project(conn, args.project)
        if not project:
            print(f"Writing project not found: {args.project}. Run plan-writing first.")
            return 2
        pages = conn.execute("SELECT * FROM writing_pages WHERE project_id=? ORDER BY priority DESC", (project["id"],)).fetchall()
        for page in pages:
            brief = generate_brief(project, page, config.writing)
            upsert_writing_brief(conn, page["id"], brief)
            export_brief(brief)
        conn.execute("UPDATE writing_projects SET status='drafting', updated_at=datetime('now') WHERE id=?", (project["id"],))
        conn.commit()
    print(f"Generated briefs for {len(pages)} pages.")
    return 0


def cmd_generate_drafts(args) -> int:
    config = load_config()
    with connect() as conn:
        init_db(conn)
        project = _find_project(conn, args.project)
        if not project:
            print(f"Writing project not found: {args.project}.")
            return 2
        rows = conn.execute(
            """
            SELECT writing_pages.id AS page_id, writing_pages.slug, writing_briefs.brief_json
            FROM writing_pages JOIN writing_briefs ON writing_briefs.page_id = writing_pages.id
            WHERE writing_pages.project_id=? ORDER BY writing_pages.priority DESC
            """,
            (project["id"],),
        ).fetchall()
        for row in rows:
            brief = json.loads(row["brief_json"])
            draft = generate_draft(brief)
            flags = check_draft(draft, config.writing.avoid_overclaim_words)["warnings"]
            upsert_writing_draft(conn, row["page_id"], draft, flags, brief["source_placeholders"])
            export_draft(project["display_game_name"], row["slug"], draft)
        conn.execute("UPDATE writing_projects SET status='draft_needs_review', updated_at=datetime('now') WHERE id=?", (project["id"],))
        conn.commit()
    print(f"Generated drafts for {len(rows)} pages. Status: draft_needs_review")
    return 0


def cmd_add_note(args) -> int:
    with connect() as conn:
        init_db(conn)
        project = _find_project(conn, args.project)
        if not project:
            print(f"Writing project not found: {args.project}.")
            return 2
        add_manual_research_note(conn, project["id"], args.source_name, args.source_url, args.note)
    print("Added manual research note.")
    return 0


def cmd_export_writing(args) -> int:
    with connect() as conn:
        init_db(conn)
        project = _find_project(conn, args.project)
        if not project:
            print(f"Writing project not found: {args.project}.")
            return 2
        pages = conn.execute("SELECT * FROM writing_pages WHERE project_id=? ORDER BY priority DESC", (project["id"],)).fetchall()
        task_path = export_task_list(project["display_game_name"], pages)
    print(f"Exported writing task list: {task_path}")
    return 0


def cmd_check_drafts(args) -> int:
    config = load_config()
    any_errors = False
    with connect() as conn:
        init_db(conn)
        project = _find_project(conn, args.project)
        if not project:
            print(f"Writing project not found: {args.project}.")
            return 2
        rows = conn.execute(
            """
            SELECT writing_pages.title, writing_drafts.draft_markdown
            FROM writing_pages JOIN writing_drafts ON writing_drafts.page_id = writing_pages.id
            WHERE writing_pages.project_id=? ORDER BY writing_pages.priority DESC
            """,
            (project["id"],),
        ).fetchall()
        for row in rows:
            result = check_draft(row["draft_markdown"], config.writing.avoid_overclaim_words)
            print(f"{row['title']}: {'passed' if result['passed'] else 'failed'}")
            for warning in result["warnings"]:
                print(f"  warning: {warning}")
            for error in result["errors"]:
                print(f"  error: {error}")
            any_errors = any_errors or bool(result["errors"])
    return 1 if any_errors else 0


def cmd_roblox_snapshot(_args) -> int:
    config = load_config()
    with connect() as conn:
        init_db(conn)
        run_id = start_run(conn, 1)
        with RobloxGameProvider(config.settings.user_agent, config.settings.request_timeout_seconds) as provider:
            games = provider.fetch_chart_games(limit=200)
            if not games:
                finish_run(conn, run_id, 0, 0, 0, 1)
                print("Roblox live chart fetch failed or returned no games.")
                if provider.last_error:
                    print(f"Details: {provider.last_error}")
                print("This endpoint is experimental and may be deprecated. Use CSV fallback instead:")
                print("python -m radar.cli import-roblox-chart --csv data/roblox-chart.csv")
                return 0
            details = provider.fetch_game_details([game.universe_id for game in games])
            games = merge_details(games, details)
        signals = store_and_score_roblox_snapshot(conn, run_id, games, "roblox-live")
        md_path, csv_path, _signals = write_roblox_report(conn, signals)
        finish_run(conn, run_id, 0, len(games), len(signals), 0)
    print(f"Wrote Roblox report: {md_path}")
    print(f"Wrote Roblox CSV: {csv_path}")
    return 0


def cmd_roblox_report(_args) -> int:
    with connect() as conn:
        init_db(conn)
        md_path, csv_path, _signals = write_roblox_report(conn)
    print(f"Wrote Roblox report: {md_path}")
    print(f"Wrote Roblox CSV: {csv_path}")
    return 0


def cmd_import_roblox_chart(args) -> int:
    try:
        games = read_roblox_chart_csv(Path(args.csv))
    except ValueError as exc:
        print(str(exc))
        return 2
    config = load_config()
    if args.enrich:
        with RobloxGameProvider(config.settings.user_agent, config.settings.request_timeout_seconds) as provider:
            games = enrich_missing_details(provider, games)
            if provider.last_error:
                print(f"Roblox detail enrichment warning: {provider.last_error}")
    with connect() as conn:
        init_db(conn)
        run_id = start_run(conn, 1)
        signals = store_and_score_roblox_snapshot(conn, run_id, games, "manual-csv")
        md_path, csv_path, _signals = write_roblox_report(conn, signals)
        finish_run(conn, run_id, 0, len(games), len(signals), 0)
    print(f"Imported {len(games)} Roblox chart rows.")
    print(f"Wrote Roblox report: {md_path}")
    print(f"Wrote Roblox CSV: {csv_path}")
    return 0


def cmd_roblox_csv_template(_args) -> int:
    ensure_dirs()
    path = PROJECT_ROOT / "data" / "roblox-chart-template.csv"
    headers = ["rank", "universe_id", "root_place_id", "name", "playing", "visits", "favorited_count", "created", "updated", "url"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)
    print(f"Wrote Roblox CSV template: {path}")
    return 0


def cmd_fusion_report(_args) -> int:
    with connect() as conn:
        init_db(conn)
        md_path, csv_path, _candidates = write_fusion_report(conn)
    print(f"Wrote fusion report: {md_path}")
    print(f"Wrote fusion CSV: {csv_path}")
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
        "roblox-snapshot": cmd_roblox_snapshot,
        "roblox-report": cmd_roblox_report,
        "roblox-csv-template": cmd_roblox_csv_template,
        "fusion-report": cmd_fusion_report,
    }.items():
        cmd = sub.add_parser(name)
        cmd.set_defaults(func=func)
    import_roblox = sub.add_parser("import-roblox-chart")
    import_roblox.add_argument("--csv", required=True)
    import_roblox.add_argument("--enrich", action="store_true")
    import_roblox.set_defaults(func=cmd_import_roblox_chart)
    plan = sub.add_parser("plan-writing")
    plan.add_argument("--candidate", required=True)
    plan.add_argument("--force", action="store_true")
    plan.set_defaults(func=cmd_plan_writing)
    briefs = sub.add_parser("generate-briefs")
    briefs.add_argument("--project", required=True)
    briefs.set_defaults(func=cmd_generate_briefs)
    drafts = sub.add_parser("generate-drafts")
    drafts.add_argument("--project", required=True)
    drafts.set_defaults(func=cmd_generate_drafts)
    note = sub.add_parser("add-note")
    note.add_argument("--project", required=True)
    note.add_argument("--source-name", required=True)
    note.add_argument("--source-url", default="")
    note.add_argument("--note", required=True)
    note.set_defaults(func=cmd_add_note)
    export_writing = sub.add_parser("export-writing")
    export_writing.add_argument("--project", required=True)
    export_writing.set_defaults(func=cmd_export_writing)
    check = sub.add_parser("check-drafts")
    check.add_argument("--project", required=True)
    check.set_defaults(func=cmd_check_drafts)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
