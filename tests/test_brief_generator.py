from radar.brief_generator import generate_brief
from radar.models import WritingSettings


class Row(dict):
    def __getitem__(self, key):
        return dict.__getitem__(self, key)


def test_codes_brief_has_verification_fields():
    project = Row(display_game_name="Ice Tycoon 2")
    page = Row(
        page_type="codes",
        target_keyword="Ice Tycoon 2 codes",
        slug="/ice-tycoon-2-codes",
        intent="Find code status.",
        title="Ice Tycoon 2 Codes",
        meta_description="Check code status.",
        h1="Ice Tycoon 2 Codes",
    )
    brief = generate_brief(project, page, WritingSettings())
    assert "Current working codes" in brief["facts_to_verify"]
    assert brief["status"] == "draft_needs_review"

