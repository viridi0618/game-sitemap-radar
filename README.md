# Game Sitemap Radar

Game Sitemap Radar is a lightweight CLI tool for keyword discovery. It monitors configured gaming sites' `robots.txt` and sitemap XML files, detects newly seen URLs, extracts likely game names from URL slugs, scores the signals, and writes a daily Markdown report plus CSV export.

It does not crawl article bodies, copy content, bypass `robots.txt`, buy domains, generate websites, or use paid APIs.

## Install

```bash
cd game-sitemap-radar
python -m pip install -e .
```

The MVP runs with the Python standard library. Optional dependencies are listed in `requirements.txt`.

## Configure

Initialize the project:

```bash
python -m radar.cli init
```

Edit `config/seeds.yaml` and add game-related domains:

```yaml
sources:
  - name: Example Roblox Codes Site
    domain: example-codes.com
    sitemap_url:
    site_type: codes
    language: en
    priority: 4
```

If `sitemap_url` is empty, the tool checks `robots.txt` for `Sitemap:` lines and then tries common sitemap paths.

## Run

```bash
python -m radar.cli run
```

This executes discovery, sitemap crawling, SQLite storage, scoring, and report generation.

Useful commands:

```bash
python -m radar.cli discover
python -m radar.cli crawl
python -m radar.cli report
python -m radar.cli export
```

## Output

Reports are written to:

- `outputs/report-YYYY-MM-DD.md`
- `outputs/candidates-YYYY-MM-DD.csv`

History is stored in `data/radar.sqlite`. A second run updates existing URLs and only marks never-before-seen URLs as new.

## Scores

Candidates are scored out of 100 using:

- unique source count
- number of new URLs
- quality of page types such as `codes`, `wiki`, `guide`, `tier_list`, `how_to`, `values`, and `calculator`
- configured source priority
- recency
- game-name extraction confidence

Labels:

- `HOT`: manual review immediately
- `WATCH`: verify with Google Trends and SERP
- `LOW`: observe only
- `IGNORE`: weak signal

## Manual Review

Use the report as a signal list, not an automatic decision engine. Manually check top candidates with Google Trends, search suggestions, SERP competition, Roblox or Steam activity, and YouTube activity in the last 24 hours.

## Legal And Ethical Notes

This tool fetches only `robots.txt` and sitemap XML files. Keep request rates low, respect site owners, avoid article body scraping, and use the resulting signals only for keyword research.

