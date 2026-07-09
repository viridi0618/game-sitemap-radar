#!/usr/bin/env python3
"""Scrape Roblox Charts page, enrich with API details, output CSV.

Requires: agent-browser CLI (npm install -g agent-browser)
Run: python3 roblox_daily.py
Output: data/roblox-chart-YYYY-MM-DD.csv
"""

import subprocess, json, csv, os, re
from datetime import datetime, timezone
from pathlib import Path

ROBLOX_CHARTS_URL = "https://www.roblox.com/charts?device=computer&country=all"
OUTPUT_DIR = Path(__file__).resolve().parent / "data"
ARCHIVE_DIR = OUTPUT_DIR / "archive"

CSV_FIELDS = ["rank", "universe_id", "root_place_id", "name", "playing",
              "visits", "favorited_count", "created", "updated", "url"]


def run_agent(cmd: str, timeout: int = 30) -> str:
    result = subprocess.run(f"agent-browser {cmd}", shell=True,
                            capture_output=True, text=True, timeout=timeout)
    return result.stdout.strip()


def run_curl(url: str, timeout: int = 15) -> dict | None:
    result = subprocess.run(
        ["curl", "-s", "--connect-timeout", str(timeout), "--max-time", str(timeout + 5), url],
        capture_output=True, text=True
    )
    if result.returncode == 0 and result.stdout:
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            pass
    return None


def fetch_chart_games(limit: int = 250) -> list[dict]:
    """Open Roblox Charts, scroll to load games, extract refs and hrefs."""
    run_agent(f'open "{ROBLOX_CHARTS_URL}"', timeout=30)
    run_agent("wait --load networkidle", timeout=30)
    run_agent("wait 3000", timeout=10)

    # Scroll to load more games until count stabilizes
    prev_count = 0
    for _round in range(20):
        for _ in range(6):
            run_agent("scroll down 800", timeout=5)
            import time; time.sleep(0.5)
        run_agent("wait 1500", timeout=5)
        raw = run_agent("snapshot -i --json")
        data = json.loads(raw)
        snap = data["data"]["snapshot"]
        current = sum(1 for l in snap.split("\n") if 'link "' in l and '%' in l and "ref=e" in l)
        print(f"  Scrolling round {_round+1}: {current} games loaded")
        if current == prev_count or current >= limit:
            break
        prev_count = current

    # Get final snapshot
    raw = run_agent("snapshot -i --json")
    data = json.loads(raw)
    snap = data["data"]["snapshot"]

    # Find game link refs
    game_refs = []
    for line in snap.split("\n"):
        if 'link "' not in line or '%' not in line:
            continue
        ref_match = re.search(r"ref=(e\d+)", line)
        if ref_match:
            game_refs.append(ref_match.group(1))

    games = []
    for rank, ref in enumerate(game_refs, 1):
        try:
            name_text = run_agent(f"get text @{ref} --json")
            href_text = run_agent(f'get attr @{ref} "href" --json')
            name_data = json.loads(name_text)
            href_data = json.loads(href_text)
            name = name_data["data"]["text"]
            href = href_data["data"]["value"]

            # Parse name lines: first line = game name, second = "%rating playing"
            lines = name.strip().split("\n")
            game_name = lines[0].strip()
            stats = lines[1].strip() if len(lines) > 1 else ""

            # Parse playing count
            stats_after_pct = stats[stats.find("%")+1:].strip() if "%" in stats else stats
            playing_match = re.search(r"([\d.]+)([KM]?)", stats_after_pct)
            playing_raw = float(playing_match.group(1)) if playing_match else 0
            unit = playing_match.group(2) if playing_match else ""
            playing = int(playing_raw * 1000) if unit == "K" else (int(playing_raw * 1000000) if unit == "M" else int(playing_raw))

            # Parse IDs from href
            universe_id = re.search(r"universeId=(\d+)", href)
            place_id = re.search(r"placeId=(\d+)", href)
            url = f"https://www.roblox.com/games/{place_id.group(1)}" if place_id else ""

            games.append({
                "rank": rank, "name": game_name, "playing": playing,
                "universe_id": universe_id.group(1) if universe_id else "",
                "root_place_id": place_id.group(1) if place_id else "",
                "url": url,
            })
        except Exception as e:
            print(f"  [{rank}] parse error: {e}")
    return games


def enrich_with_api(games: list[dict]) -> list[dict]:
    """Fetch game details from Roblox API to fill visits, favorites, created."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    uids = [g["universe_id"] for g in games if g["universe_id"]]
    if not uids:
        return games

    detail_map = {}
    for i in range(0, len(uids), 50):
        batch = uids[i:i+50]
        url = f"https://games.roblox.com/v1/games?universeIds={','.join(batch)}"
        api_data = run_curl(url)
        if api_data:
            for g in api_data.get("data", []):
                detail_map[str(g["id"])] = g
        print(f"  API enrich batch {i//50 + 1}: {len(batch)} -> {len(detail_map)} total")

    for g in games:
        uid = g["universe_id"]
        if uid in detail_map:
            d = detail_map[uid]
            g["visits"] = str(d.get("visits", ""))
            g["favorited_count"] = str(d.get("favoritedCount", ""))
            g["created"] = d.get("created", "") or ""
            g["updated"] = d.get("updated", "") or today
        else:
            g["updated"] = today
        g.setdefault("visits", ""); g.setdefault("favorited_count", ""); g.setdefault("created", "")
    return games


def deduplicate(games: list[dict]) -> list[dict]:
    seen = set()
    result = []
    for g in games:
        key = re.sub(r"[^a-z0-9]", "", g["name"].strip().lower())
        if key not in seen:
            seen.add(key)
            result.append(g)
    return result


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    output_path = OUTPUT_DIR / f"roblox-chart-{today}.csv"

    print(f"=== Roblox Daily Scraper ({today}) ===")
    print("Fetching Roblox Charts...")
    games = fetch_chart_games()
    print(f"Found {len(games)} chart entries")

    print("Enriching with API details...")
    games = enrich_with_api(games)

    games = deduplicate(games)
    for i, g in enumerate(games, 1):
        g["rank"] = i

    # Write daily CSV
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for g in games:
            writer.writerow({k: g.get(k, "") for k in CSV_FIELDS})

    # Symlink latest
    latest_path = OUTPUT_DIR / "roblox-chart-latest.csv"
    if latest_path.exists():
        latest_path.unlink()
    latest_path.symlink_to(output_path.name)

    # Archive copy
    archive_path = ARCHIVE_DIR / f"roblox-chart-{today}.csv"
    with open(archive_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for g in games:
            writer.writerow({k: g.get(k, "") for k in CSV_FIELDS})

    print(f"\nDone: {len(games)} unique games saved to:")
    print(f"  {output_path}")
    print(f"  {latest_path} -> {output_path.name}")
    print(f"  Archive: {archive_path}")

    # Show top 5
    print("\nTop 5:")
    for g in games[:5]:
        c = g.get("created", "N/A")[:10]
        print(f"  {g['rank']}. {g['name'][:45]:45s} playing={str(g['playing']):>8s} visits={str(g.get('visits','')):>14s} created={c}")


if __name__ == "__main__":
    main()
