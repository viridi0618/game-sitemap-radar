# Game Sitemap Radar

Game Sitemap Radar is a lightweight CLI tool for keyword discovery and writing preparation. It monitors configured gaming sites' `robots.txt` and sitemap XML files, detects newly seen URLs, extracts likely game names from URL slugs, scores the signals, and writes a daily Markdown report plus CSV export.

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
python -m radar.cli discover
python -m radar.cli crawl
python -m radar.cli report
python -m radar.cli export
```

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

Recommended workflow:

1. Add seed sites.
2. Run radar.
3. Review candidate report.
4. Select a candidate.
5. Generate a writing plan.
6. Add manual research notes.
7. Generate briefs.
8. Generate drafts.
9. Run draft quality checks.
10. Human-review and fact-check.
11. Only then move content into a real site manually.

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

Generated drafts are not ready for automatic publishing. Codes, values, event schedules, rankings, player counts, update dates, and game mechanics must be verified with trusted sources before publishing.

## Legal And Ethical Notes

This tool fetches only `robots.txt` and sitemap XML files. Keep request rates low, respect site owners, avoid article body scraping, and use the resulting signals only for keyword research.
