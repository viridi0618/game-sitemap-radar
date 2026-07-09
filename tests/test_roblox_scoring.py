from datetime import datetime, timedelta, timezone

from radar.roblox_models import RobloxChartGame
from radar.roblox_scoring import score_roblox_game


def test_new_roblox_entry_with_high_playing_gets_watch_or_hot():
    game = RobloxChartGame(
        rank=5,
        universe_id=1,
        root_place_id=10,
        name="Ice Tycoon 2",
        playing=12000,
        visits=500000,
        created=(datetime.now(timezone.utc) - timedelta(days=20)).isoformat(),
    )
    signal = score_roblox_game(game)
    assert signal["score"] >= 60
    assert signal["label"] in {"WATCH - manual review", "HOT - check immediately"}
    assert "First snapshot; growth unavailable." in signal["reasoning"]


def test_old_flat_game_gets_low_score():
    game = RobloxChartGame(
        rank=100,
        universe_id=2,
        root_place_id=20,
        name="Old Flat Game",
        playing=200,
        visits=1000,
        created=(datetime.now(timezone.utc) - timedelta(days=400)).isoformat(),
    )
    previous = {"rank": 100, "playing": 200, "visits": 1000, "favorited_count": 50}
    signal = score_roblox_game(game, previous)
    assert signal["score"] < 40


def test_game_created_twenty_days_ago_gets_strong_launch_window_score():
    game = RobloxChartGame(
        rank=10,
        universe_id=3,
        root_place_id=30,
        name="Launch Window Game",
        playing=1000,
        visits=100000,
        created=(datetime.now(timezone.utc) - timedelta(days=20)).isoformat(),
    )
    signal = score_roblox_game(game)
    assert "launch window 15" in signal["reasoning"]
