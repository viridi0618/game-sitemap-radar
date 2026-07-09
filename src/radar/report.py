from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .matrix import calculate_matrix_score
from .scoring import label_for_score, score_candidate
from .utils import PROJECT_ROOT, ensure_dirs, parse_dt, utc_now
from .writing_planner import create_writing_plan
from .models import WritingSettings


def build_candidates(conn, window_hours: int, run_id: int | None = None) -> list[dict]:
    since = (datetime.now(timezone.utc) - timedelta(hours=window_hours)).isoformat()
    rows = conn.execute(
        """
        SELECT urls.*, sources.domain, sources.priority
        FROM urls JOIN sources ON sources.id = urls.source_id
        WHERE urls.first_seen_at >= ? AND urls.normalized_candidate_game IS NOT NULL
        """,
        (since,),
    ).fetchall()
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["normalized_candidate_game"]].append(row)

    candidates = []
    for normalized, items in grouped.items():
        sources = {row["source_id"] for row in items}
        priorities = {}
        page_types = {row["page_type"] or "unknown" for row in items}
        first_seen = min(row["first_seen_at"] for row in items)
        latest_seen = max(row["first_seen_at"] for row in items)
        for row in items:
            priorities[row["source_id"]] = int(row["priority"] or 0)
        confidence = "clear"
        if any(row["name_confidence"] == "low" for row in items):
            confidence = "low"
        elif any(row["name_confidence"] == "medium" for row in items):
            confidence = "medium"
        score = score_candidate(
            source_count=len(sources),
            new_url_count=len(items),
            page_types=page_types,
            source_priority_sum=sum(priorities.values()),
            first_seen_at=first_seen,
            name_confidence=confidence,
        )
        matrix = calculate_matrix_score(page_types, len(sources), confidence)
        candidates.append(
            {
                "normalized_candidate_game": normalized,
                "display_game_name": items[0]["candidate_game"],
                "new_url_count": len(items),
                "source_count": len(sources),
                "page_types": sorted(page_types),
                "score": score,
                "label": label_for_score(score),
                "first_seen_at": first_seen,
                "latest_seen_at": latest_seen,
                "sample_urls": [row["url"] for row in items[:5]],
                **matrix,
            }
        )
    candidates.sort(key=lambda item: (-item["score"], -item["new_url_count"], item["display_game_name"]))
    return candidates


def write_reports(conn, window_hours: int, run_id: int | None = None, crawl_stats: dict | None = None) -> tuple[Path, Path, list[dict]]:
    ensure_dirs()
    candidates = build_candidates(conn, window_hours, run_id)
    today = datetime.now().strftime("%Y-%m-%d")
    md_path = PROJECT_ROOT / "outputs" / f"report-{today}.md"
    csv_path = PROJECT_ROOT / "outputs" / f"candidates-{today}.csv"

    run = conn.execute("SELECT * FROM runs ORDER BY id DESC LIMIT 1").fetchone()
    errors = conn.execute("SELECT sitemap_url, error FROM sitemaps WHERE error IS NOT NULL AND error != '' ORDER BY last_fetched_at DESC LIMIT 50").fetchall()
    new_by_source = conn.execute(
        """
        SELECT sources.domain, urls.url, urls.page_type, urls.candidate_game, urls.first_seen_at
        FROM urls JOIN sources ON sources.id = urls.source_id
        WHERE urls.first_seen_at >= ?
        ORDER BY sources.domain, urls.first_seen_at DESC
        LIMIT 5000
        """,
        ((datetime.now(timezone.utc) - timedelta(hours=window_hours)).isoformat(),),
    ).fetchall()

    lines = [
        "# Game Sitemap Radar Report",
        "",
        f"Generated at: {utc_now()}",
        f"Sources checked: {run['source_count'] if run else 0}",
        f"Sitemaps fetched: {run['sitemap_count'] if run else 0}",
        f"Total URLs seen: {conn.execute('SELECT COUNT(*) AS c FROM urls').fetchone()['c']}",
        f"New URLs: {run['new_url_count'] if run else len(new_by_source)}",
        f"Errors: {run['error_count'] if run else len(errors)}",
    ]
    if crawl_stats:
        lines.extend(
            [
                f"Crawl elapsed seconds: {crawl_stats.get('elapsed_seconds', 0):.2f}",
                f"URLs per second: {crawl_stats.get('urls_per_second', 0):.2f}",
                f"Total fetch errors: {crawl_stats.get('error_count', 0)}",
                f"Filtered URLs: {crawl_stats.get('filtered_url_count', 0)}",
            ]
        )
    lines.extend(["", "## Top Candidate Games", ""])
    if not candidates:
        lines.append("No new candidate games found in the configured window.")
    display_candidates = candidates[:100]
    if len(candidates) > len(display_candidates):
        lines.append(f"Showing top {len(display_candidates)} of {len(candidates)} candidates. Full candidate list is in the CSV export.")
        lines.append("")
    for idx, candidate in enumerate(display_candidates, start=1):
        lines.extend(
            [
                f"### {idx}. {candidate['display_game_name']}",
                "",
                f"Score: {candidate['score']}",
                f"Label: {candidate['label']}",
                f"New URLs: {candidate['new_url_count']}",
                f"Sources: {candidate['source_count']}",
                f"Page types: {', '.join(candidate['page_types'])}",
                f"Matrix score: {candidate['matrix_score']}",
                f"Suggested site size: {candidate['suggested_site_size']}",
                f"Matrix reasoning: {candidate['matrix_reasoning']}",
                f"First seen: {candidate['first_seen_at']}",
                f"Latest seen: {candidate['latest_seen_at']}",
                "",
                "Sample URLs:",
            ]
        )
        lines.extend(f"- {url}" for url in candidate["sample_urls"])
        name = candidate["display_game_name"]
        lines.extend(
            [
                "",
                "Suggested manual checks:",
                f"- Google Trends: {name}",
                f"- Google Search: {name} codes",
                f"- Google Search: {name} wiki",
                f"- Google Search: {name} tier list",
                "- Roblox / Steam platform check",
                "- YouTube last 24h check",
                "",
            ]
        )
        if candidate["score"] >= 60:
            plan = create_writing_plan(candidate, WritingSettings())
            lines.extend(["Suggested writing plan:", ""])
            lines.extend(f"- {page.title}" for page in plan.pages)
            lines.extend(
                [
                    "",
                    "Manual verification checklist:",
                    "- Official game URL",
                    "- Platform",
                    "- Launch date",
                    "- Current player count",
                    "- Recent update date",
                    "- YouTube activity",
                    "- Google Trends check",
                    "- SERP competition",
                    "- Whether codes exist",
                    "- Whether game has enough systems for 5+ pages",
                    "",
                    "Writing commands:",
                    f'```bash\npython -m radar.cli plan-writing --candidate "{name}"\npython -m radar.cli generate-briefs --project "{name}"\npython -m radar.cli generate-drafts --project "{name}"\n```',
                    "",
                ]
            )

    lines.extend(["## New URLs By Source", ""])
    by_domain = defaultdict(list)
    for row in new_by_source:
        by_domain[row["domain"]].append(row)
    for domain, rows in by_domain.items():
        lines.append(f"### {domain}")
        for row in rows[:50]:
            lines.append(f"- [{row['page_type']}] {row['candidate_game']} - {row['url']}")
        lines.append("")

    lines.extend(["## Fetch Errors", ""])
    if not errors:
        lines.append("No fetch errors recorded.")
    for row in errors:
        lines.append(f"- {row['sitemap_url']}: {row['error']}")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "display_game_name",
                "normalized_candidate_game",
                "score",
                "label",
                "new_url_count",
                "source_count",
                "page_types",
                "first_seen_at",
                "latest_seen_at",
                "sample_urls",
                "matrix_score",
                "suggested_site_size",
                "matrix_reasoning",
            ],
        )
        writer.writeheader()
        for candidate in candidates:
            row = dict(candidate)
            row["page_types"] = ",".join(row["page_types"])
            row["sample_urls"] = json.dumps(row["sample_urls"], ensure_ascii=False)
            writer.writerow(row)
    return md_path, csv_path, candidates
