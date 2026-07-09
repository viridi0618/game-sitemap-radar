from __future__ import annotations

from urllib.parse import urlparse


DEFAULT_RULES: dict[str, list[str]] = {
    "codes": ["codes", "redeem", "working-codes", "active-codes"],
    "wiki": ["wiki", "database"],
    "guide": ["guide", "walkthrough"],
    "tier_list": ["tier-list", "tierlist", "best-units", "best-characters", "rankings"],
    "best": ["best"],
    "how_to": ["how-to", "how-to-get", "how-to-unlock", "where-to-find"],
    "items": ["items", "item"],
    "units": ["units", "unit"],
    "pets": ["pets", "pet"],
    "characters": ["characters", "character"],
    "traits": ["traits", "trait"],
    "mutations": ["mutations", "mutation"],
    "classes": ["classes", "class"],
    "values": ["values", "value-list", "worth"],
    "trading": ["trading", "trade"],
    "calculator": ["calculator"],
    "map": ["map"],
    "boss": ["boss"],
    "quests": ["quests", "quest"],
    "recipes": ["recipes", "recipe"],
    "event": ["event"],
    "update": ["update"],
    "release": ["release"],
    "news": ["news"],
}

ORDER = [
    "codes",
    "how_to",
    "tier_list",
    "wiki",
    "guide",
    "values",
    "calculator",
    "traits",
    "mutations",
    "classes",
    "items",
    "units",
    "pets",
    "characters",
    "trading",
    "map",
    "boss",
    "quests",
    "recipes",
    "event",
    "release",
    "update",
    "news",
    "best",
]


def classify_page_type(url: str, rules: dict[str, list[str]] | None = None) -> str:
    rules = rules or DEFAULT_RULES
    path = urlparse(url).path.lower().strip("/")
    slug = path.replace("_", "-")
    for page_type in ORDER:
        for token in rules.get(page_type, []):
            needle = token.lower().replace("_", "-")
            if needle in slug:
                return page_type
    return "unknown"

