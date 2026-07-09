from radar.config import load_config


def test_load_config_handles_utf8_bom(tmp_path):
    config_path = tmp_path / "seeds.yaml"
    config_path.write_text(
        "\ufeffsources:\n"
        "  - name: Example Codes\n"
        "    domain: example.com\n"
        "    site_type: codes\n"
        "    language: en\n"
        "    priority: 4\n",
        encoding="utf-8",
    )
    config = load_config(config_path)
    assert len(config.sources) == 1
    assert config.sources[0].domain == "example.com"
    assert config.sources[0].priority == 4
