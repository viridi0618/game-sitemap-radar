from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import urlparse


STOP_WORDS = {
    "roblox",
    "game",
    "games",
    "guide",
    "wiki",
    "codes",
    "code",
    "tier",
    "tierlist",
    "list",
    "best",
    "units",
    "unit",
    "characters",
    "character",
    "how",
    "to",
    "get",
    "unlock",
    "where",
    "find",
    "in",
    "value",
    "values",
    "calculator",
    "update",
    "release",
    "map",
    "boss",
    "tips",
    "working",
    "active",
    "redeem",
}

ANCHORS = {"in", "for"}


@dataclass
class CandidateName:
    display: str
    normalized: str
    confidence: str


def _slug_segments(url: str) -> list[str]:
    path = urlparse(url).path
    return [seg for seg in path.strip("/").split("/") if seg and not seg.endswith(".xml")]


def _tokens(slug: str) -> list[str]:
    cleaned = re.sub(r"[^a-zA-Z0-9-]+", "-", slug.lower())
    return [part for part in cleaned.split("-") if part]


def _title(tokens: list[str]) -> str:
    return " ".join(token.upper() if len(token) == 1 and token.isalpha() else token.capitalize() for token in tokens)


def normalize_game_name(name: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", name.lower())).strip()


def extract_candidate_game(url: str) -> CandidateName:
    segments = _slug_segments(url)
    slug = max(segments, key=len) if segments else urlparse(url).netloc
    toks = _tokens(slug)

    for anchor in ANCHORS:
        if anchor in toks:
            idx = len(toks) - 1 - toks[::-1].index(anchor)
            tail = [tok for tok in toks[idx + 1 :] if tok not in STOP_WORDS]
            if tail:
                display = _title(tail)
                return CandidateName(display, normalize_game_name(display), "medium" if len(tail) < 2 else "clear")

    filtered = [tok for tok in toks if tok not in STOP_WORDS]
    if not filtered:
        filtered = toks[:4]

    display = _title(filtered)
    normalized = normalize_game_name(display)
    confidence = "clear" if len(filtered) >= 2 else "low"
    if any(tok in {"post", "page", "category", "tag"} for tok in toks):
        confidence = "low"
    return CandidateName(display or "Unknown", normalized or "unknown", confidence)

