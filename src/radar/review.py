from __future__ import annotations

import re


def check_draft(markdown: str, avoid_words: list[str]) -> dict[str, list[str]]:
    warnings = []
    errors = []
    if "title:" not in markdown:
        errors.append("Missing title frontmatter.")
    if "description:" not in markdown:
        errors.append("Missing meta description frontmatter.")
    if not re.search(r"^#\s+", markdown, flags=re.MULTILINE):
        errors.append("Missing H1.")
    if "## Sources to verify" not in markdown:
        errors.append("Missing source placeholder block.")
    if "status: draft_needs_review" not in markdown:
        errors.append("Draft status is not draft_needs_review.")
    lowered = markdown.lower()
    for word in avoid_words:
        if word.lower() == "official" and "official game page:" in lowered:
            continue
        if re.search(rf"\b{re.escape(word.lower())}\b", lowered):
            warnings.append(f"Uses overclaim word: {word}")
    if "working codes" in lowered and "manually verified codes table here" not in lowered:
        warnings.append("Mentions working codes without a verified code list placeholder.")
    if "official" in lowered and "official game page:" not in lowered:
        warnings.append("Uses official without an official source placeholder.")
    if len(markdown.split()) < 120:
        warnings.append("Draft is short and may need more useful detail.")
    repeated = _repeated_phrases(markdown)
    if repeated:
        warnings.append(f"Repeated phrase: {repeated}")
    return {"passed": not errors, "warnings": warnings, "errors": errors}


def _repeated_phrases(markdown: str) -> str | None:
    words = re.findall(r"[a-zA-Z]{4,}", markdown.lower())
    phrases = [" ".join(words[i : i + 4]) for i in range(max(0, len(words) - 3))]
    seen = set()
    for phrase in phrases:
        if phrase in seen:
            return phrase
        seen.add(phrase)
    return None
