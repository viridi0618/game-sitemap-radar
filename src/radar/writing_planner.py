from __future__ import annotations

import json
import re

from .writing_models import WritingPagePlan, WritingProjectPlan


BASE_PAGE_TYPES = ["homepage", "beginner_guide", "faq"]
SIGNAL_TO_PAGE_TYPE = {
    "codes": "codes",
    "wiki": "wiki",
    "guide": "beginner_guide",
    "tier_list": "tier_list",
    "best": "tier_list",
    "how_to": "how_to",
    "values": "values",
    "calculator": "calculator",
    "traits": "traits",
    "mutations": "mutations",
    "items": "items",
    "map": "map",
    "boss": "boss",
    "update": "update",
    "release": "update",
    "news": "update",
}


def slugify_game(game: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", game.lower())).strip("-")


def _page_copy(game: str, page_type: str) -> tuple[str, str, str, str, str]:
    base = slugify_game(game)
    mapping = {
        "homepage": (game, f"/{base}", game, f"{game}", f"Learn what to verify about {game}, where to start, and which guides may be useful."),
        "codes": (f"{game} codes", f"/{base}-codes", f"{game} Codes", f"{game} Codes", f"Check {game} code status, redemption steps, and sources to verify before publishing any code list."),
        "beginner_guide": (f"{game} beginner guide", f"/{base}-beginner-guide", f"{game} Beginner Guide", f"{game} Beginner Guide", f"Plan a beginner-friendly guide for starting {game} without making unverified gameplay claims."),
        "wiki": (f"{game} wiki", f"/{base}-wiki", f"{game} Wiki", f"{game} Wiki Hub", f"Outline a database hub for {game} systems, items, updates, and guide paths."),
        "tier_list": (f"{game} tier list", f"/{base}-tier-list", f"{game} Tier List", f"{game} Tier List", f"Prepare ranking criteria and placeholders that require manual gameplay verification."),
        "how_to": (f"{game} how to", f"/{base}-how-to", f"{game} How-To Guide", f"{game} How-To Guide", f"Create a cautious how-to page with requirements and steps to verify."),
        "values": (f"{game} values", f"/{base}-values", f"{game} Values", f"{game} Value List", f"Prepare a value page with trading safety notes and verification placeholders."),
        "calculator": (f"{game} calculator", f"/{base}-calculator", f"{game} Calculator", f"{game} Calculator", f"Define a calculator concept and required inputs before implementation."),
        "traits": (f"{game} traits", f"/{base}-traits", f"{game} Traits", f"{game} Traits Guide", f"Plan a traits guide with effects and sources to verify."),
        "mutations": (f"{game} mutations", f"/{base}-mutations", f"{game} Mutations", f"{game} Mutations Guide", f"Plan a mutations guide with cautious mechanics placeholders."),
        "items": (f"{game} items", f"/{base}-items", f"{game} Items", f"{game} Items Guide", f"Prepare an item database page that requires manual stat verification."),
        "map": (f"{game} map", f"/{base}-map", f"{game} Map", f"{game} Map and Locations", f"Plan a map page with location placeholders and verification needs."),
        "boss": (f"{game} boss guide", f"/{base}-boss-guide", f"{game} Boss Guide", f"{game} Boss Guide", f"Prepare a boss guide with requirements, strategies, and source placeholders."),
        "update": (f"{game} update", f"/{base}-update", f"{game} Update", f"{game} Update Notes", f"Track update signals without inventing patch details or dates."),
        "faq": (f"{game} FAQ", f"/{base}-faq", f"{game} FAQ", f"{game} FAQ", f"Answer common questions cautiously and flag facts that need verification."),
    }
    return mapping[page_type]


def create_writing_plan(candidate: dict, writing_settings) -> WritingProjectPlan:
    detected = candidate.get("page_types") or []
    desired = list(BASE_PAGE_TYPES)
    for signal in detected:
        page_type = SIGNAL_TO_PAGE_TYPE.get(signal)
        if page_type and page_type not in desired:
            desired.append(page_type)
    if set(detected) <= {"news", "release", "update"}:
        desired = ["homepage", "faq", "update"]

    priorities = writing_settings.page_type_priority
    desired.sort(key=lambda page_type: -priorities.get(page_type, 30))
    desired = desired[: writing_settings.max_pages_per_candidate]

    game = candidate["display_game_name"]
    pages = []
    for page_type in desired:
        target_keyword, slug, title, h1, meta = _page_copy(game, page_type)
        pages.append(
            WritingPagePlan(
                page_type=page_type,
                target_keyword=target_keyword,
                slug=slug,
                title=title,
                meta_description=meta[:155],
                h1=h1,
                intent=_intent_for_page_type(game, page_type),
                priority=priorities.get(page_type, 30),
            )
        )
    return WritingProjectPlan(
        normalized_candidate_game=candidate["normalized_candidate_game"],
        display_game_name=game,
        score=int(candidate.get("score", 0)),
        page_types=list(detected),
        sample_urls=list(candidate.get("sample_urls") or []),
        pages=pages,
    )


def _intent_for_page_type(game: str, page_type: str) -> str:
    intents = {
        "homepage": f"Understand what {game} is and where to go next.",
        "codes": f"Find whether {game} codes exist and how to verify redemption details.",
        "beginner_guide": f"Learn safe starting points for {game} after manual fact checking.",
        "wiki": f"Navigate {game} systems and database-style reference pages.",
        "tier_list": f"Compare best options in {game} using criteria that still need verification.",
        "how_to": f"Solve a specific {game} task with verified steps.",
        "values": f"Check {game} value signals and trading context without fake numbers.",
        "calculator": f"Define what a {game} calculator should estimate.",
        "faq": f"Answer common {game} questions cautiously.",
    }
    return intents.get(page_type, f"Prepare a cautious {game} {page_type.replace('_', ' ')} page.")


def candidate_from_db_row(row) -> dict:
    return {
        "normalized_candidate_game": row["normalized_candidate_game"],
        "display_game_name": row["display_game_name"],
        "score": row["score"],
        "page_types": json.loads(row["page_types"] or "[]"),
        "sample_urls": json.loads(row["sample_urls"] or "[]"),
    }

