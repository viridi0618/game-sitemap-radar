from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path

from .brief_generator import brief_to_markdown
from .utils import PROJECT_ROOT, ensure_dirs
from .writing_planner import slugify_game


def project_output_dir(game: str) -> Path:
    ensure_dirs()
    today = datetime.now().strftime("%Y-%m-%d")
    path = PROJECT_ROOT / "outputs" / "writing" / today / slugify_game(game)
    path.mkdir(parents=True, exist_ok=True)
    return path


def export_plan(plan) -> tuple[Path, Path]:
    out = project_output_dir(plan.display_game_name)
    data = {
        "normalized_candidate_game": plan.normalized_candidate_game,
        "display_game_name": plan.display_game_name,
        "score": plan.score,
        "page_types": plan.page_types,
        "sample_urls": plan.sample_urls,
        "pages": [page.__dict__ for page in plan.pages],
        "status": "planned",
    }
    json_path = out / "writing-plan.json"
    md_path = out / "writing-plan.md"
    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [f"# Writing Plan: {plan.display_game_name}", "", f"Candidate score: {plan.score}", "", "## Pages"]
    for page in plan.pages:
        lines.append(f"- {page.title} ({page.page_type}) - {page.slug}")
    lines.extend(["", "## Signal URLs"])
    lines.extend(f"- {url}" for url in plan.sample_urls)
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path


def export_brief(brief: dict) -> tuple[Path, Path]:
    out = project_output_dir(brief["game"]) / brief["slug"].strip("/").replace("/", "-")
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "brief.json"
    md_path = out / "brief.md"
    json_path.write_text(json.dumps(brief, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(brief_to_markdown(brief), encoding="utf-8")
    return json_path, md_path


def export_draft(game: str, slug: str, markdown: str) -> Path:
    drafts = project_output_dir(game) / "drafts"
    drafts.mkdir(parents=True, exist_ok=True)
    path = drafts / f"{slug.strip('/').replace('/', '-')}.md"
    path.write_text(markdown, encoding="utf-8")
    return path


def export_task_list(game: str, pages) -> Path:
    out = project_output_dir(game)
    path = out / "task-list.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["page_type", "target_keyword", "slug", "title", "priority", "status"])
        for page in pages:
            writer.writerow([page["page_type"], page["target_keyword"], page["slug"], page["title"], page["priority"], page["status"]])
    return path

