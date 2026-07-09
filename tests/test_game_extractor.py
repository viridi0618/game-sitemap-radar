from radar.game_extractor import extract_candidate_game


def test_extracts_candidate_games():
    assert extract_candidate_game("https://x.test/ice-tycoon-2-codes/").display == "Ice Tycoon 2"
    assert extract_candidate_game("https://x.test/roblox-ice-tycoon-2-guide/").display == "Ice Tycoon 2"
    assert extract_candidate_game("https://x.test/best-units-in-anime-rangers-x/").display == "Anime Rangers X"
    assert extract_candidate_game("https://x.test/how-to-get-taco-trait-in-steal-a-brainrot/").display == "Steal A Brainrot"
    assert extract_candidate_game("https://x.test/dead-rails-codes/").display == "Dead Rails"
    assert extract_candidate_game("https://x.test/roblox/codes/games/ice-tycoon-2/working-codes/").display == "Ice Tycoon 2"
    assert extract_candidate_game("https://x.test/guides/roblox/ice-tycoon-2-codes/").display == "Ice Tycoon 2"
    assert extract_candidate_game("https://x.test/games/ice-tycoon-2/how-to-rebirth-fast/").display == "Ice Tycoon 2"
    assert extract_candidate_game("https://x.test/how-to-get-dragon-sword-in-anime-rangers-x/").display == "Anime Rangers X"
    assert extract_candidate_game("https://x.test/roblox/games/dead-rails/codes/").display == "Dead Rails"

