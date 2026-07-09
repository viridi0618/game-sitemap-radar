# Game Sitemap Radar

Game Sitemap Radar is a lightweight CLI tool for Roblox discovery, sitemap signal monitoring, fusion reporting, and writing preparation. It can track Roblox chart snapshots as a leading player-growth signal, monitor configured gaming sites' `robots.txt` and sitemap XML files as competitor coverage signals, and combine both into a daily decision report.

The upgraded workflow can also turn a strong candidate into a writing project with page plans, structured briefs, Markdown drafts, quality checks, and task exports.

It does not crawl article bodies, copy competitor content, rewrite competitor articles, bypass `robots.txt`, buy domains, auto-publish pages, generate production-ready content, or use paid APIs.

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
python -m radar.cli roblox-csv-template
python -m radar.cli import-roblox-chart --csv data/roblox-chart.csv
python -m radar.cli import-roblox-chart --csv data/roblox-chart.csv --enrich
python -m radar.cli roblox-snapshot
python -m radar.cli roblox-report
python -m radar.cli discover
python -m radar.cli crawl
python -m radar.cli report
python -m radar.cli export
python -m radar.cli fusion-report
```

CSV import is the primary Roblox workflow. Roblox live chart pages require JavaScript and the public chart endpoints may fail or disappear, so `roblox-snapshot` is experimental and should not be the main daily source.

Create a template with:

```bash
python -m radar.cli roblox-csv-template
```

Then manually prepare or export Roblox top games into `data/roblox-chart.csv` with these columns:

```csv
rank,universe_id,root_place_id,name,playing,visits,favorited_count,created,updated,url
```

Example row:

```csv
1,123456789,987654321,Example Roblox Game,12000,45000000,250000,2026-06-20T00:00:00Z,2026-07-09T00:00:00Z,https://www.roblox.com/games/987654321
```

The minimum required CSV columns are `rank`, `universe_id`, and `name`. Optional numeric columns default to `0`. Use `--enrich` to try filling missing details from `https://games.roblox.com/v1/games?universeIds=<ids>`; enrichment is best-effort and never required.

## Writing Workflow

Competitor sitemap URLs are used only as discovery, page type, keyword intent, and timing signals. They are not used as article sources.

After reviewing the report, select a candidate and create writing materials:

```bash
python -m radar.cli plan-writing --candidate "Ice Tycoon 2" --force
python -m radar.cli generate-briefs --project "Ice Tycoon 2"
python -m radar.cli generate-drafts --project "Ice Tycoon 2"
python -m radar.cli check-drafts --project "Ice Tycoon 2"
python -m radar.cli export-writing --project "Ice Tycoon 2"
```

The output goes to:

- `outputs/writing/YYYY-MM-DD/<game>/writing-plan.json`
- `outputs/writing/YYYY-MM-DD/<game>/writing-plan.md`
- `outputs/writing/YYYY-MM-DD/<game>/<page>/brief.json`
- `outputs/writing/YYYY-MM-DD/<game>/<page>/brief.md`
- `outputs/writing/YYYY-MM-DD/<game>/drafts/*.md`
- `outputs/writing/YYYY-MM-DD/<game>/task-list.csv`

Every generated draft includes frontmatter:

```yaml
status: draft_needs_review
needs_fact_check: true
```

Manual research notes can be stored with:

```bash
python -m radar.cli add-note --project "Ice Tycoon 2" --source-name "Official Roblox" --source-url "..." --note "..."
```

Recommended daily workflow:

1. Prepare `data/roblox-chart.csv`.
2. Run `python -m radar.cli import-roblox-chart --csv data/roblox-chart.csv`.
3. Run `python -m radar.cli roblox-report`.
4. Open `outputs/roblox-report-YYYY-MM-DD.md`.
5. Run sitemap radar with `python -m radar.cli run`.
6. Run `python -m radar.cli fusion-report`.
7. Manually verify HOT / WATCH candidates with Google Trends, Google Search suggestions, Semrush KD, recent YouTube videos, and content vacuum checks.
8. If a candidate passes, run `python -m radar.cli plan-writing --candidate "Game Name" --force`.
9. Add manual research notes.
10. Generate briefs.
11. Generate drafts.
12. Run draft quality checks.
13. Human-review and fact-check.
14. Only then move content into a real site manually.

Signal roles:

- Roblox Watcher = leading player-growth signal, preferably from stable CSV imports.
- Sitemap Radar = competitor coverage signal.
- Fusion Report = decision support.
- Writing Module = draft preparation only.

Broad gaming, codes, and guide sites should use `include_url_keywords` and `exclude_url_keywords` in `config/seeds.yaml`. These filters reduce noise, speed up crawling/report generation, and keep the candidate list focused on Roblox-style opportunities. Wiki-only domains should not be over-filtered because useful reference pages often have varied URL patterns.

## Output

Reports are written to:

- `outputs/report-YYYY-MM-DD.md`
- `outputs/candidates-YYYY-MM-DD.csv`
- `outputs/roblox-report-YYYY-MM-DD.md`
- `outputs/roblox-candidates-YYYY-MM-DD.csv`
- `outputs/fusion-report-YYYY-MM-DD.md`
- `outputs/fusion-candidates-YYYY-MM-DD.csv`

History is stored in `data/radar.sqlite`. A second run updates existing URLs and only marks never-before-seen URLs as new.

## Scores

Candidates are scored out of 100 using:

- unique source count
- number of new URLs
- quality of page types such as `codes`, `wiki`, `guide`, `tier_list`, `how_to`, `values`, and `calculator`
- configured source priority
- recency
- game-name extraction confidence
- candidate matrix potential

Labels:

- `HOT`: manual review immediately
- `WATCH`: verify with Google Trends and SERP
- `LOW`: observe only
- `IGNORE`: weak signal

## Manual Review

Use the report as a signal list, not an automatic decision engine. Manually check top candidates with Google Trends, search suggestions, SERP competition, Roblox or Steam activity, and YouTube activity in the last 24 hours.

Generated drafts are not ready for automatic publishing. Codes, values, event schedules, rankings, player counts, update dates, and game mechanics must be verified with trusted sources before publishing.

## Legal And Ethical Notes

This tool fetches only `robots.txt` and sitemap XML files. Keep request rates low, respect site owners, avoid article body scraping, and use the resulting signals only for keyword research.
