# Cloudflare Pages Deployment

Live site: https://vrp-reports.aivault.securityjunky.com/

## How it works

Two-branch setup:
- `main` — source code (Python pipeline + `ui/` SPA + `build.sh`)
- `data` — scraped output (`index.json`, `stats.json`, `issues/<id>/report.{json,md}`)

The GitHub Actions workflow `.github/workflows/deploy.yml` checks out **both** branches, runs `build.sh` to assemble `dist/`, and deploys via `wrangler pages deploy` (direct upload — Cloudflare does no building of its own).

Cloudflare Pages project `vrp-reports` has auto-builds **disabled** (build command cleared, branch deployments off). All deploys come from the Actions workflow.

## Triggers

- **Manual**: Actions tab → `Deploy VRP Reports` → Run workflow
- **Auto**: push to `main` that touches `ui/**`, `build.sh`, or the workflow file itself
- **Weekly scrape**: `.github/workflows/scrape.yml` runs every Sunday, pushes lightweight updates to `data`, and deploys when data changed

## Updating content (new scraped reports)

The scheduled scraper runs weekly on GitHub Actions. It refreshes discovery for the latest/current UTC year, scrapes only missing reports, regenerates markdown/index/stats, pushes lightweight files to the `data` branch, and deploys when data changed.

You can still scrape locally:

```bash
vrp run                           # discover → scrape → markdown → index
```

Then push the lightweight files to `data` branch (skip `attachments/` and `raw_*.json`):

```bash
cd /tmp && rm -rf vrp-data-push
git clone --branch data --single-branch https://github.com/dark-warlord14/vrp-reports.git vrp-data-push
cd vrp-data-push
cp <repo>/data/{index,stats}.json .
cp <repo>/data/discovery_*.json .
rsync -a --include='*/' --include='report.json' --include='report.md' --exclude='*' <repo>/data/issues/ ./issues/
git add -A && git commit -m "chore: update data $(date -u +%Y-%m-%d)" && git push origin data
```

Then trigger the deploy workflow manually.

## Updating UI / code

Push to `main`. If the change touches `ui/**` or `build.sh`, deploy runs automatically.

## Secrets (GitHub → Settings → Secrets → Actions)

- `CLOUDFLARE_API_TOKEN` — token with `Cloudflare Pages: Edit` permission
- `CLOUDFLARE_ACCOUNT_ID` — from Cloudflare dash sidebar

## Rotating the API token

1. Cloudflare dash → avatar → My Profile → API Tokens → create new token (template: "Edit Cloudflare Workers")
2. GitHub repo → Settings → Secrets → update `CLOUDFLARE_API_TOKEN`
3. Revoke the old token in Cloudflare

## Agent / programmatic access

Static JSON exposed at these stable URLs (CORS enabled):

- `/data/index.json` — all reports summary (≈900KB). IDs + metadata for filtering.
- `/data/stats.json` — aggregates.
- `/data/issues/<id>/report.json` — full report.
- `/data/issues/<id>/report.md` — markdown version.
- `/schema.json` — JSON Schema for a report.
- `/skill.md` — agent usage guide (drop into a Claude Code skill).
- `/llms.txt` — site manifest for LLM discoverability.

Point any agent at `https://vrp-reports.aivault.securityjunky.com/skill.md` for the full usage contract.

## Changing the Cloudflare project name

Update `--project-name=vrp-reports` in `.github/workflows/deploy.yml` and create the matching project in the Cloudflare dash.
