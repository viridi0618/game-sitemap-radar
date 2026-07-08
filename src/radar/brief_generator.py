from __future__ import annotations


OUTLINES = {
    "homepage": ["What is {game}?", "Why players are searching for it", "Beginner starting points", "Main guides", "Current status / update notes", "FAQ"],
    "codes": ["Current code status", "Working codes table placeholder", "Expired codes table placeholder", "How to redeem", "Where new codes are usually announced", "Troubleshooting", "FAQ"],
    "beginner_guide": ["What to do first", "Early progression", "Best beginner upgrades/items/units", "Common mistakes", "Next guides", "FAQ"],
    "wiki": ["Database overview", "Main systems", "Items / units / upgrades", "Events / updates", "Recommended guide order", "FAQ"],
    "tier_list": ["Ranking criteria", "Best choices summary", "Tier table placeholder", "Beginner picks", "Late-game picks", "What to verify", "FAQ"],
    "how_to": ["Quick answer", "Requirements", "Step-by-step method", "Common problems", "Alternatives", "FAQ"],
    "values": ["Value status", "Value table placeholder", "What affects value", "Trading safety", "FAQ"],
    "calculator": ["What the calculator should estimate", "Required inputs", "Formula placeholder", "Limitations", "Future implementation notes"],
}


def generate_brief(project_row, page_row, writing_settings) -> dict:
    game = project_row["display_game_name"]
    page_type = page_row["page_type"]
    outline = [
        {
            "heading": heading.format(game=game),
            "notes": _notes_for_heading(page_type, heading),
        }
        for heading in OUTLINES.get(page_type, OUTLINES["homepage"])
    ]
    return {
        "game": game,
        "page_type": page_type,
        "target_keyword": page_row["target_keyword"],
        "slug": page_row["slug"],
        "intent": page_row["intent"],
        "title": page_row["title"],
        "meta_description": page_row["meta_description"],
        "h1": page_row["h1"],
        "outline": outline,
        "facts_to_verify": _facts_to_verify(page_type),
        "internal_links": _internal_links(game, page_type),
        "source_placeholders": _source_placeholders(page_type),
        "risk_notes": _risk_notes(page_type),
        "status": writing_settings.draft_status,
    }


def _notes_for_heading(page_type: str, heading: str) -> str:
    if page_type == "codes":
        return "Do not invent codes. Mark code status as needs verification unless manually confirmed."
    if "table" in heading.lower():
        return "Use placeholders only until trusted research provides data."
    if page_type == "calculator":
        return "Describe the concept and required inputs; do not invent formulas."
    return "Write original guidance and flag facts that require trusted verification."


def _facts_to_verify(page_type: str) -> list[str]:
    base = ["Official game URL", "Platform", "Recent update date", "Core gameplay systems"]
    extras = {
        "codes": ["Whether codes exist", "Current working codes", "Expired codes", "Where redemption is located"],
        "values": ["Current value source", "Trading rules", "Recent market changes"],
        "tier_list": ["Ranking criteria", "Current balance changes", "Player-tested choices"],
        "calculator": ["Inputs", "Formula", "Data source", "Known limitations"],
    }
    return base + extras.get(page_type, [])


def _internal_links(game: str, page_type: str) -> list[str]:
    base = game.lower().replace(" ", "-")
    links = [f"/{base}", f"/{base}-beginner-guide", f"/{base}-faq"]
    if page_type != "codes":
        links.append(f"/{base}-codes")
    return list(dict.fromkeys(links))


def _source_placeholders(page_type: str) -> list[str]:
    sources = ["Official game page", "Official Discord or community page", "Developer update notes", "In-game check date"]
    if page_type == "codes":
        sources.append("Manual code redemption test")
    return sources


def _risk_notes(page_type: str) -> list[str]:
    notes = ["Do not copy competitor content.", "Do not publish unverified mechanics as facts."]
    if page_type == "codes":
        notes.extend(["Do not publish fake codes.", "Do not use 'working' unless verified on the current date."])
    if page_type in {"values", "tier_list"}:
        notes.append("Avoid pretending rankings or values are final without current evidence.")
    return notes


def brief_to_markdown(brief: dict) -> str:
    lines = [
        f"# Brief: {brief['title']}",
        "",
        f"- Game: {brief['game']}",
        f"- Page type: {brief['page_type']}",
        f"- Target keyword: {brief['target_keyword']}",
        f"- Slug: {brief['slug']}",
        f"- Status: {brief['status']}",
        "",
        "## Intent",
        brief["intent"],
        "",
        "## Outline",
    ]
    for item in brief["outline"]:
        lines.append(f"- {item['heading']}: {item['notes']}")
    lines.extend(["", "## Facts To Verify"])
    lines.extend(f"- {fact}" for fact in brief["facts_to_verify"])
    lines.extend(["", "## Source Placeholders"])
    lines.extend(f"- {source}" for source in brief["source_placeholders"])
    lines.extend(["", "## Risk Notes"])
    lines.extend(f"- {note}" for note in brief["risk_notes"])
    return "\n".join(lines) + "\n"

