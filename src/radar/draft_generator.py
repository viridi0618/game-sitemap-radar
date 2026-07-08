from __future__ import annotations


def generate_draft(brief: dict) -> str:
    lines = [
        "---",
        f"title: \"{brief['title']}\"",
        f"description: \"{brief['meta_description']}\"",
        f"slug: \"{brief['slug']}\"",
        f"page_type: \"{brief['page_type']}\"",
        f"game: \"{brief['game']}\"",
        f"status: {brief['status']}",
        "needs_fact_check: true",
        "---",
        "",
        f"# {brief['h1']}",
        "",
        f"This draft is a preparation document for {brief['game']}. It uses sitemap signals only to choose the topic and page type. Facts, codes, values, mechanics, and dates need manual verification before publishing.",
        "",
    ]
    for item in brief["outline"]:
        lines.extend([f"## {item['heading']}", "", _section_text(brief, item["heading"]), ""])
    lines.extend(["## Sources to verify", ""])
    for source in brief["source_placeholders"]:
        lines.append(f"- {source}:")
    lines.extend(["", "## Review notes", "", "- Status: draft_needs_review", "- Do not publish until the verification checklist is done."])
    return "\n".join(lines) + "\n"


def _section_text(brief: dict, heading: str) -> str:
    page_type = brief["page_type"]
    game = brief["game"]
    lower = heading.lower()
    if page_type == "codes" and "working codes" in lower:
        return "Add a manually verified codes table here. Do not invent code strings, rewards, or expiration dates."
    if page_type == "codes" and "expired codes" in lower:
        return "Add expired codes only after checking reliable records or testing them in game."
    if "faq" in lower:
        return "Draft cautious answers here. Mark uncertain details as needs confirmation."
    if "table" in lower:
        return "Add a table only after manual research provides trustworthy data."
    if page_type == "calculator":
        return "Describe the intended inputs and limitations. Leave formula details as placeholders until verified."
    return f"Draft original guidance for {game}. Keep claims cautious and add facts only after checking trusted sources."
