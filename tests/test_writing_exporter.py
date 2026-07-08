from radar.brief_generator import generate_brief
from radar.exporter import export_brief
from radar.models import WritingSettings


class Row(dict):
    def __getitem__(self, key):
        return dict.__getitem__(self, key)


def test_export_writes_markdown_and_json(tmp_path, monkeypatch):
    import radar.exporter as exporter

    monkeypatch.setattr(exporter, "PROJECT_ROOT", tmp_path)
    brief = generate_brief(
        Row(display_game_name="Ice Tycoon 2"),
        Row(
            page_type="codes",
            target_keyword="Ice Tycoon 2 codes",
            slug="/ice-tycoon-2-codes",
            intent="Find code status.",
            title="Ice Tycoon 2 Codes",
            meta_description="Check code status.",
            h1="Ice Tycoon 2 Codes",
        ),
        WritingSettings(),
    )
    json_path, md_path = export_brief(brief)
    assert json_path.exists()
    assert md_path.exists()

