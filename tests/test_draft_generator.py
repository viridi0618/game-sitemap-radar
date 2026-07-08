from radar.draft_generator import generate_draft


def test_codes_draft_does_not_invent_codes_and_has_frontmatter():
    brief = {
        "game": "Ice Tycoon 2",
        "page_type": "codes",
        "target_keyword": "Ice Tycoon 2 codes",
        "slug": "/ice-tycoon-2-codes",
        "title": "Ice Tycoon 2 Codes",
        "meta_description": "Check code status.",
        "h1": "Ice Tycoon 2 Codes",
        "status": "draft_needs_review",
        "outline": [{"heading": "Working codes table placeholder", "notes": ""}],
        "source_placeholders": ["Official game page", "In-game check date"],
    }
    draft = generate_draft(brief)
    assert draft.startswith("---")
    assert "status: draft_needs_review" in draft
    assert "Do not invent code strings" in draft
    assert "## Sources to verify" in draft

