from __future__ import annotations


PAGE_TYPE_POINTS = {
    "codes": 10,
    "wiki": 15,
    "database": 15,
    "beginner_guide": 10,
    "guide": 10,
    "tier_list": 10,
    "best": 10,
    "how_to": 15,
    "items": 20,
    "units": 20,
    "pets": 20,
    "characters": 20,
    "traits": 15,
    "mutations": 15,
    "classes": 15,
    "values": 15,
    "trading": 15,
    "calculator": 15,
    "map": 10,
    "boss": 10,
    "quests": 10,
    "recipes": 10,
    "event": 10,
    "update": 10,
}


def suggested_site_size(score: int) -> str:
    if score < 30:
        return "test_site_3_5_pages"
    if score < 50:
        return "small_site_6_10_pages"
    if score < 75:
        return "matrix_site_20_50_pages"
    return "large_matrix_50_plus_pages"


def calculate_matrix_score(page_types: set[str], source_count: int, name_confidence: str = "clear") -> dict:
    score = 0
    reasons = []
    if page_types <= {"news", "release"}:
        score -= 20
        reasons.append("only news/release signals")
    for page_type in sorted(page_types):
        points = PAGE_TYPE_POINTS.get(page_type, 0)
        if points:
            score += points
            reasons.append(f"{page_type} +{points}")
    if source_count >= 3:
        score += 15
        reasons.append("3+ sources +15")
    elif source_count == 2:
        score += 10
        reasons.append("2 sources +10")
    elif source_count == 1:
        score += 5
        reasons.append("1 source +5")
    confidence_points = {"clear": 10, "medium": 5, "low": 0}.get(name_confidence, 0)
    score += confidence_points
    reasons.append(f"{name_confidence} name +{confidence_points}")
    score = max(0, min(100, score))
    return {
        "matrix_score": score,
        "suggested_site_size": suggested_site_size(score),
        "matrix_reasoning": "; ".join(reasons) if reasons else "no matrix signals",
    }
