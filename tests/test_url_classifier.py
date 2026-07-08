from radar.url_classifier import classify_page_type


def test_classifies_page_types():
    assert classify_page_type("https://x.test/ice-tycoon-2-codes/") == "codes"
    assert classify_page_type("https://x.test/roblox-ice-tycoon-2-guide/") == "guide"
    assert classify_page_type("https://x.test/best-units-in-anime-rangers-x/") == "tier_list"
    assert classify_page_type("https://x.test/how-to-get-taco-trait-in-steal-a-brainrot/") == "how_to"

