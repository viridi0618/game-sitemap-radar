from __future__ import annotations

import ast
import shutil
from pathlib import Path

from .models import AppConfig, Settings, Source
from .utils import PROJECT_ROOT, ensure_dirs


def _coerce_scalar(value: str):
    value = value.strip()
    if value == "":
        return None
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return ast.literal_eval(value)
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


def _minimal_yaml_load(text: str) -> dict:
    """Small YAML reader for this project's seeds/rules shape."""
    data: dict = {}
    section = None
    current_item = None
    current_map_key = None
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        stripped = line.strip()
        indent = len(line) - len(line.lstrip(" "))
        if indent == 0 and stripped.endswith(":"):
            section = stripped[:-1]
            data[section] = [] if section == "sources" else {}
            current_item = None
            current_map_key = None
            continue
        if section == "sources":
            if stripped.startswith("- "):
                current_item = {}
                data["sources"].append(current_item)
                rest = stripped[2:]
                if rest:
                    key, value = rest.split(":", 1)
                    current_item[key.strip()] = _coerce_scalar(value)
            elif current_item is not None and ":" in stripped:
                key, value = stripped.split(":", 1)
                current_item[key.strip()] = _coerce_scalar(value)
        elif isinstance(data.get(section), dict):
            if indent == 2 and stripped.endswith(":"):
                current_map_key = stripped[:-1]
                data[section][current_map_key] = []
            elif indent == 2 and ":" in stripped:
                key, value = stripped.split(":", 1)
                data[section][key.strip()] = _coerce_scalar(value)
                current_map_key = None
            elif indent >= 4 and stripped.startswith("- ") and current_map_key:
                data[section][current_map_key].append(_coerce_scalar(stripped[2:]))
    return data


def load_yaml(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore

        return yaml.safe_load(text) or {}
    except ModuleNotFoundError:
        return _minimal_yaml_load(text)


def load_config(path: Path | None = None) -> AppConfig:
    path = path or PROJECT_ROOT / "config" / "seeds.yaml"
    raw = load_yaml(path)
    sources = [
        Source(
            name=item.get("name") or item.get("domain"),
            domain=item["domain"],
            sitemap_url=item.get("sitemap_url"),
            site_type=item.get("site_type", "general"),
            language=item.get("language", "en"),
            priority=int(item.get("priority", 3)),
        )
        for item in raw.get("sources", [])
        if item.get("domain")
    ]
    settings = Settings(**{**Settings().__dict__, **raw.get("settings", {})})
    return AppConfig(sources=sources, settings=settings)


def load_rules(path: Path | None = None) -> dict[str, list[str]]:
    raw = load_yaml(path or PROJECT_ROOT / "config" / "rules.yaml")
    return raw.get("page_types", {})


def init_config_files() -> None:
    ensure_dirs()
    example = PROJECT_ROOT / "config" / "seeds.example.yaml"
    seeds = PROJECT_ROOT / "config" / "seeds.yaml"
    if not seeds.exists():
        shutil.copyfile(example, seeds)

