from radar.models import WritingSettings
from radar.writing_planner import create_writing_plan


def test_candidate_with_codes_wiki_guide_creates_core_pages():
    candidate = {
        "normalized_candidate_game": "ice tycoon 2",
        "display_game_name": "Ice Tycoon 2",
        "score": 88,
        "page_types": ["codes", "wiki", "guide"],
        "sample_urls": [],
    }
    plan = create_writing_plan(candidate, WritingSettings())
    page_types = {page.page_type for page in plan.pages}
    assert {"homepage", "codes", "wiki", "beginner_guide", "faq"} <= page_types


def test_news_only_candidate_stays_small():
    candidate = {
        "normalized_candidate_game": "small update",
        "display_game_name": "Small Update",
        "score": 42,
        "page_types": ["news", "release"],
        "sample_urls": [],
    }
    plan = create_writing_plan(candidate, WritingSettings())
    assert [page.page_type for page in plan.pages] == ["homepage", "faq", "update"]

