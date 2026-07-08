from datetime import datetime, timezone

from radar.scoring import label_for_score, score_candidate


def test_scores_candidate():
    score = score_candidate(
        source_count=4,
        new_url_count=9,
        page_types={"codes", "tier_list", "wiki"},
        source_priority_sum=20,
        first_seen_at=datetime.now(timezone.utc).isoformat(),
        name_confidence="clear",
    )
    assert score == 100
    assert label_for_score(score) == "HOT - manual review immediately"

