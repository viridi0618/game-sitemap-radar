from radar.review import check_draft


def test_quality_checker_warns_on_overclaim_words():
    draft = """---
title: "Test"
description: "Test"
slug: "/test"
page_type: "codes"
game: "Test"
status: draft_needs_review
needs_fact_check: true
---

# Test

This is a complete and guaranteed guide.

## Sources to verify

- Official game page:
"""
    result = check_draft(draft, ["complete", "verified", "guaranteed", "all", "every"])
    assert result["passed"]
    assert "Uses overclaim word: complete" in result["warnings"]
    assert "Uses overclaim word: guaranteed" in result["warnings"]

