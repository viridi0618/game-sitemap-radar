from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path

from .matrix import calculate_matrix_score
from .roblox_report import latest_roblox_signals
from .utils import PROJECT_ROOT, ensure_dirs, utc_now


def build_fusion_candidates(conn) -> list[dict]:
    roblox = {row["normalized_name"]: row for row in latest_roblox_signals(conn)}
    sitemap_rows = conn.execute(
        """
        SELECT *
        FROM candidate_signals
        WHERE run_id = (SELECT MAX(run_id) FROM candidate_signals)
        """
    ).fetchall()
    sitemap = {}
    for row in sitemap_rows:
        page_types = set(json.loads(row["page_types"] or "[]"))
        matrix_score = row["matrix_score"]
        matrix_reasoning = row["matrix_reasoning"]
        suggested_site_size = row["suggested_site_size"]
        if matrix_score is None:
            matrix = calculate_matrix_score(page_types, int(row["source_count"] or 0), "clear")
            matrix_score = matrix["matrix_score"]
            matrix_reasoning = matrix["matrix_reasoning"]
            suggested_site_size = matrix["suggested_site_size"]
        sitemap[row["normalized_candidate_game"]] = {
            "name": row["display_game_name"],
            "sitemap_score": row["score"] or 0,
            "source_count": row["source_count"] or 0,
            "page_types": sorted(page_types),
            "matrix_score": matrix_score or 0,
            "matrix_reasoning": matrix_reasoning or "",
            "suggested_site_size": suggested_site_size or "",
        }
    candidates = []
    for normalized in sorted(set(roblox) | set(sitemap)):
        r = roblox.get(normalized)
        s = sitemap.get(normalized)
        roblox_score = int(r["score"]) if r else 0
        sitemap_score = int(s["sitemap_score"]) if s else 0
        matrix_score = int(s["matrix_score"]) if s else 0
        fusion_score = round(roblox_score * 0.55 + sitemap_score * 0.25 + matrix_score * 0.20, 2)
        candidates.append(
            {
                "normalized_name": normalized,
                "name": (r or s)["name"],
                "fusion_score": fusion_score,
                "interpretation": interpretation_for_fusion_score(fusion_score),
                "roblox_score": roblox_score,
                "sitemap_score": sitemap_score,
                "matrix_score": matrix_score,
                "roblox_label": r["label"] if r else "",
                "sitemap_sources": s["source_count"] if s else 0,
                "sitemap_page_types": ",".join(s["page_types"]) if s else "",
                "suggested_site_size": s["suggested_site_size"] if s else "test_site_3_5_pages",
                "opportunity": opportunity_note(roblox_score, sitemap_score, int(s["source_count"]) if s else 0),
                "url": r.get("url") if r else "",
                "matrix_reasoning": s["matrix_reasoning"] if s else "no sitemap matrix signals yet",
            }
        )
    candidates.sort(key=lambda item: (-item["fusion_score"], -item["roblox_score"], item["name"]))
    return candidates


def write_fusion_report(conn) -> tuple[Path, Path, list[dict]]:
    ensure_dirs()
    candidates = build_fusion_candidates(conn)
    today = datetime.now().strftime("%Y-%m-%d")
    md_path = PROJECT_ROOT / "outputs" / f"fusion-report-{today}.md"
    csv_path = PROJECT_ROOT / "outputs" / f"fusion-candidates-{today}.csv"
    lines = [
        "# Fusion Report",
        "",
        f"Generated at: {utc_now()}",
        "",
        "Fusion score = roblox_score * 0.55 + sitemap_score * 0.25 + matrix_score * 0.20",
        "",
    ]
    if not candidates:
        lines.append("No fusion candidates yet. Run `roblox-snapshot` or `import-roblox-chart`, then run sitemap radar.")
    display_candidates = candidates[:200]
    if len(candidates) > len(display_candidates):
        lines.append(f"Showing top {len(display_candidates)} of {len(candidates)} candidates. Full candidate list is in the CSV export.")
        lines.append("")
    for idx, item in enumerate(display_candidates, start=1):
        lines.extend(
            [
                f"## {idx}. {item['name']}",
                "",
                f"Fusion score: {item['fusion_score']}",
                f"Interpretation: {item['interpretation']}",
                f"Roblox score: {item['roblox_score']}",
                f"Sitemap score: {item['sitemap_score']}",
                f"Matrix score: {item['matrix_score']}",
                f"Sitemap sources: {item['sitemap_sources']}",
                f"Sitemap page types: {item['sitemap_page_types']}",
                f"Suggested site size: {item['suggested_site_size']}",
                f"Opportunity: {item['opportunity']}",
                f"Matrix reasoning: {item['matrix_reasoning']}",
                f"URL: {item['url']}",
                "",
            ]
        )
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(candidates[0].keys()) if candidates else ["name", "fusion_score"])
        writer.writeheader()
        writer.writerows(candidates)
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return md_path, csv_path, candidates


def interpretation_for_fusion_score(score: float) -> str:
    if score >= 80:
        return "build test site immediately"
    if score >= 60:
        return "manual review today"
    if score >= 40:
        return "watch 24-48h"
    return "ignore"


def opportunity_note(roblox_score: int, sitemap_score: int, source_count: int) -> str:
    if roblox_score >= 60 and sitemap_score == 0:
        return "Strong Roblox growth + no sitemap coverage: potential content vacuum. Verify search demand."
    if roblox_score >= 60 and source_count <= 2:
        return "Strong Roblox growth + light sitemap coverage: best opportunity window."
    if roblox_score >= 60:
        return "Strong Roblox growth + heavy sitemap coverage: hot but competitive. Target long tails."
    if sitemap_score >= 60 and roblox_score < 40:
        return "Strong sitemap coverage + weak Roblox growth: late signal or old trend. Be cautious."
    return "Mixed or early signal. Watch for another snapshot."
