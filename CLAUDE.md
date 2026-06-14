# VRP Reports — Claude Code Guide

## What this project does
Scrapes Chromium Vulnerability Reward Program (VRP) bug bounty reports from the Chromium Issue Tracker, processes them into structured JSON/Markdown, and serves a local SPA dashboard.

## Setup
```bash
pip install -e ".[dev]" && playwright install chromium
```

## Common commands
```bash
make test          # run all tests
make lint          # ruff linter
make format        # ruff formatter
vrp run            # run full pipeline (discover → scrape → reprocess → markdown → index)
vrp serve          # start dashboard at http://localhost:8080
vrp status         # show current project state
```

## Pipeline stages (internal, all run via `vrp run`)
1. discover — finds issue IDs from Chromium Issue Tracker (year-by-year, checkpointed). Runs multiple independent reward searches (`REWARD_SEARCH_QUALIFIERS` in `config.py`) and unions them so a renamed tracker field can't silently drop reports.
2. scrape — scrapes each issue with Playwright, downloads attachments. No-bounty determinations are recorded in `no_bounty.json` and skipped on later runs (they leave no `report.json`, so without this they'd be re-scraped every run); `--refresh-discovery` re-checks them. Access-restricted issues stay retryable (never cached as no-bounty).
3. reprocess — re-parses raw JSON without re-scraping (offline). Writes are content-aware (unchanged reports aren't rewritten, so the markdown stage's mtime-skip holds). Self-healing: a report that no longer qualifies under current detection is removed and recorded no-bounty.
4. markdown — generates report.md for each issue (skips when report.json is unchanged)
5. index — builds index.json + stats.json

## Bounty detection (`config.py` + `parser.py`)
An update counts as an award only if a positive `BOUNTY_INDICATORS` phrase is present AND no `BOUNTY_DENIAL_INDICATORS` phrase is. The VRP panel's automated grant and denial emails share boilerplate (e.g. the bare panel name), so never treat a generic header as a positive signal — that previously mis-flagged denials as bounties. The numeric reward metadata field is the authoritative path; award-text detection is the fallback.

## Key directories
- `vrp/` — Python package (source)
- `tests/` — pytest test suite (all browser interactions are mocked)
- `ui/` — frontend SPA (HTML/CSS/JS, vendored Chart.js + markdown-it)
- `data/` — gitignored runtime data; lives on separate `data` branch in CI

## Configuration
All scraper settings are in `vrp/config.py` and overridable via env vars. See `.env.example`.

## Test patterns
- Tests use `unittest.mock.patch` to redirect `vrp.config.*` paths to temp directories
- No Playwright install needed to run tests — browser interactions are mocked
- `tests/fixtures.py` has helpers for building fake API response structures
