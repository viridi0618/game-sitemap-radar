#!/usr/bin/env python3
"""Scrape Roblox Charts: Top Trending, Up-and-Coming, Top Playing Now.

Opens each list's See All page, scrolls to load, extracts game data from
accessibility tree snapshots (no per-game ref queries), enriches via API.
"""

import subprocess, json, re, time, csv, os
from datetime import datetime, timezone
from collections import Counter

ROBLOX_CHARTS_URL = "https://www.roblox.com/charts?device=computer&country=all"
LIST_NAMES = ["Top Trending", "Up-and-Coming", "Top Playing Now"]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "data")
ARCHIVE_DIR = os.path.join(OUTPUT_DIR, "archive")

CSV_FIELDS = ["rank", "universe_id", "root_place_id", "name", "playing",
              "visits", "favorited_count", "created", "updated", "url", "list"]


def run_agent(cmd, timeout=30):
    result = subprocess.run(f"agent-browser {cmd}", shell=True,
                            capture_output=True, text=True, timeout=timeout)
    return result.stdout.strip()


def run_curl(url, timeout=15):
    result = subprocess.run(
        ["curl", "-s", "--connect-timeout", str(timeout),
         "--max-time", str(timeout + 5), url],
        capture_output=True, text=True)
    if result.returncode == 0 and result.stdout:
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            pass
    return None


def get_snapshot():
    raw = run_agent("snapshot -i --json", timeout=15)
    return json.loads(raw)["data"]["snapshot"]


def parse_game_line(line):
    """Parse a snapshot line like:
    - link "🪣 Drain the Lake 🪣 Drain the Lake 95% 66.2K" [ref=e18]
    Returns dict or None.
    """
    m = re.search(r'link "([^"]+)" \[ref=(e\d+)\]', line)
    if not m:
        return None
    text = m.group(1)
    # Must have "%" to be a game
    if "%" not in text:
        return None

    # Game name is double-label format: "DisplayName DisplayName rating% playingK"
    # The duplicated name part ends before the rating %
    pct_idx = text.find("%")
    if pct_idx == -1:
        return None

    # The game name repeats twice before stats
    # e.g. "Animal Hospital (Anomaly) 🧪 Animal Hospital (Anomaly) 🧪 95% 439.3K"
    # or "[🌴] Dress To Impress [🌴] Dress To Impress 90% 86.1K"
    # Strategy: find the last occurrence of a word boundary before % to split
    before_pct = text[:pct_idx]
    # The last space before pct separates the repeated name from rating
    # Find a natural split: the name repeats - find the mid-point
    # Use a simpler approach: split on "%NUMBER" and take the first half
    # Actually: the text is "NAME NAME RATING% PLAYING"
    # NAME repeats. RATING is digits before %.
    rating_match = re.search(r'(\d+)%', text)
    if not rating_match:
        return None
    rating_pos = rating_match.start()
    repeated = text[:rating_pos].strip()
    # The actual game name is the first half of the repeated string
    mid = len(repeated) // 2
    game_name = repeated[:mid].strip()
    # Fallback: if mid split looks wrong, use first half of words
    if not game_name or len(game_name) < 2:
        words = repeated.split()
        game_name = " ".join(words[:len(words)//2])

    # Playing count
    after_pct = text[pct_idx + 1:].strip()
    pm = re.search(r"([\d.]+)([KM]?)", after_pct)
    playing = 0
    if pm:
        raw_val = float(pm.group(1))
        unit = pm.group(2)
        playing = int(raw_val * 1000) if unit == "K" else (
            int(raw_val * 1000000) if unit == "M" else int(raw_val))

    return {
        "name": game_name,
        "playing": playing,
        "ref": m.group(2),
    }


def click_see_all_for(label):
    """Find and click the 'See All' link for the given list label."""
    snap = get_snapshot()
    lines = snap.split("\n")
    see_all_ref = None
    for i, line in enumerate(lines):
        if "See All" in line and "ref=e" in line:
            # Look backward for heading containing the label
            for j in range(i - 1, max(0, i - 10), -1):
                if "heading" in lines[j] and label in lines[j]:
                    see_all_ref = re.search(r"ref=(e\d+)", line).group(1)
                    break
        if see_all_ref:
            break
    if not see_all_ref:
        print(f"  WARNING: Could not find See All for {label}")
        return False
    run_agent(f"click @{see_all_ref}", timeout=10)
    run_agent("wait --load networkidle", timeout=45)
    run_agent("wait 4000", timeout=10)
    return True


def scroll_and_collect_games(label):
    """Scroll until stable, then parse all game entries from final snapshot."""
    prev_count = 0
    for r in range(30):
        for _ in range(5):
            run_agent("scroll down 800", timeout=5)
            time.sleep(0.3)
        run_agent("wait 2000", timeout=5)
        snap = get_snapshot()
        current = sum(1 for l in snap.split("\n") if parse_game_line(l))
        if r % 5 == 0:
            print(f"  [{label}] scroll round {r+1}: {current} games")
        if current == prev_count:
            print(f"  [{label}] stabilized at {current} games")
            break
        prev_count = current

    # Final extraction
    snap = get_snapshot()
    games = []
    for line in snap.split("\n"):
        info = parse_game_line(line)
        if info:
            info["list"] = label
            games.append(info)

    print(f"  [{label}] extracted {len(games)} games")
    return games


def get_game_details_via_ref(games, label):
    """Get href (contains universeId/placeId) for each game via its ref."""
    total = len(games)
    for i, g in enumerate(games):
        try:
            href_raw = run_agent(f'get attr @{g["ref"]} "href" --json', timeout=5)
            href_data = json.loads(href_raw)
            href = href_data.get("data", {}).get("value", "")
            uid = re.search(r"universeId=(\d+)", href)
            pid = re.search(r"placeId=(\d+)", href)
            g["universe_id"] = uid.group(1) if uid else ""
            g["root_place_id"] = pid.group(1) if pid else ""
            g["url"] = f"https://www.roblox.com/games/{pid.group(1)}" if pid else ""
            del g["ref"]
        except Exception:
            g["universe_id"] = ""
            g["root_place_id"] = ""
            g["url"] = ""
            del g["ref"]
        if (i + 1) % 50 == 0:
            print(f"  [{label}] got details for {i+1}/{total}")

    # Clean up: remove ref key from any remaining
    for g in games:
        g.pop("ref", None)
    return games


def enrich_games(games):
    """Fetch visits, favorites, created from Roblox API."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    uids = list(set(g.get("universe_id", "") for g in games if g.get("universe_id")))
    print(f"\nEnriching {len(uids)} unique universe IDs via API...")

    detail_map = {}
    for i in range(0, len(uids), 50):
        batch = uids[i:i + 50]
        url = f"https://games.roblox.com/v1/games?universeIds={','.join(batch)}"
        api_data = run_curl(url)
        if api_data:
            for d in api_data.get("data", []):
                detail_map[str(d["id"])] = d
        print(f"  batch {i // 50 + 1}: {len(batch)} -> {len(detail_map)} total")

    for g in games:
        uid = g.get("universe_id", "")
        if uid in detail_map:
            d = detail_map[uid]
            g["visits"] = str(d.get("visits", ""))
            g["favorited_count"] = str(d.get("favoritedCount", ""))
            g["created"] = d.get("created", "") or ""
            g["updated"] = d.get("updated", "") or today
        g.setdefault("visits", ""); g.setdefault("favorited_count", ""); g.setdefault("created", ""); g.setdefault("updated", today)
    return games


def deduplicate(games):
    seen = set()
    result = []
    for g in games:
        key = re.sub(r"[^a-z0-9]", "", g.get("name", "").strip().lower())
        if key and key not in seen:
            seen.add(key)
            result.append(g)
    for i, g in enumerate(result, 1):
        g["rank"] = i
    return result


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(ARCHIVE_DIR, exist_ok=True)

    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    output_path = os.path.join(OUTPUT_DIR, f"roblox-chart-{today_str}.csv")

    print(f"=== Roblox Daily Scraper ({today_str}) ===")

    # Navigate to charts
    run_agent(f'open "{ROBLOX_CHARTS_URL}"', timeout=30)
    run_agent("wait --load networkidle", timeout=30)
    run_agent("wait 4000", timeout=10)

    all_games = []

    for label in LIST_NAMES:
        print(f"\n>>> {label}")
        if not click_see_all_for(label):
            print(f"  Skipping {label}: See All link not found")
            run_agent("back", timeout=10)
            run_agent("wait --load networkidle", timeout=30)
            run_agent("wait 3000", timeout=10)
            continue

        games = scroll_and_collect_games(label)

        if games:
            games = get_game_details_via_ref(games, label)

        all_games.extend(games)

        # Go back to main charts page
        run_agent("back", timeout=10)
        run_agent("wait --load networkidle", timeout=30)
        run_agent("wait 3000", timeout=10)

    print(f"\n=== Raw total: {len(all_games)} games ===")

    all_games = enrich_games(all_games)
    all_games = deduplicate(all_games)

    # Save
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for g in all_games:
            w = {}
            for k in CSV_FIELDS:
                w[k] = str(g.get(k, ""))
            writer.writerow(w)

    # Latest symlink
    latest = os.path.join(OUTPUT_DIR, "roblox-chart-latest.csv")
    if os.path.exists(latest):
        os.unlink(latest)
    os.symlink(os.path.basename(output_path), latest)

    # Archive
    archive_path = os.path.join(ARCHIVE_DIR, f"roblox-chart-{today_str}.csv")
    with open(archive_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for g in all_games:
            w = {}
            for k in CSV_FIELDS:
                w[k] = str(g.get(k, ""))
            writer.writerow(w)

    # Summary
    print(f"\n=== Final: {len(all_games)} unique games ===")
    lc = Counter(g.get("list", "?") for g in all_games)
    for lbl, cnt in lc.most_common():
        print(f"  {lbl}: {cnt}")

    print(f"\nSaved: {output_path}")
    print(f"Latest: {latest}")
    print(f"Archive: {archive_path}")

    print("\nTop 10 by playing:")
    for g in sorted(all_games, key=lambda x: int(x.get("playing", "0") or 0), reverse=True)[:10]:
        c = (g.get("created", "") or "")[:10]
        n = (g.get("name","") or "")[:40]; p = str(g.get("playing","")); l = g.get("list","")
        print(f'  {n:<40s} playing={p:>8s} created={c} [{l}]')


if __name__ == "__main__":
    main()
