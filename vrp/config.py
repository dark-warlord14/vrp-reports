"""Configuration for VRP Reports scraper."""

import os
import re
from datetime import datetime
from pathlib import Path

# --- Paths ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
ISSUES_DIR = DATA_DIR / "issues"
CORPUS_DIR = DATA_DIR / "corpus" / "js"
INDEX_FILE = DATA_DIR / "index.json"
STATS_FILE = DATA_DIR / "stats.json"
QUEUE_FILE = DATA_DIR / "discovery_queue.json"
# Issue IDs that were scraped and confirmed to carry no bounty. No-bounty issues
# leave no report.json (their dir is removed), so without this record they'd be
# re-scraped via the browser on every run. Persisting them lets re-runs skip the
# work; --refresh-discovery re-evaluates them in case a reward was added later.
NO_BOUNTY_FILE = DATA_DIR / "no_bounty.json"
UI_DIR = PROJECT_ROOT / "ui"

# --- Search ---
# Reward-detection qualifiers. Discovery runs ONE search per qualifier and
# UNIONS the results (see discover_ids_for_year), so a single field rename on
# the tracker can never silently make us miss rewarded issues — the other nets
# still catch them. This is deliberately redundant for resilience: as the
# tracker's schema evolves over the years, add/adjust qualifiers here.
#
#   customfield1223135>0  the numeric VRP reward field the parser reads
#                         (FIELD_BOUNTY below) — the precise, authoritative net.
#   Reward>0              broad reward qualifier; a superset that also catches
#                         pending/variant rewards. The parser re-validates every
#                         hit, so over-inclusion costs scrape time, never data.
#   vrp-reward>0          legacy reward tag; kept purely as a safety net.
#
# Each entry is URL-encoded (%3E == '>', %20 == ' ').
REWARD_SEARCH_QUALIFIERS = [
    "customfield1223135%3E0",
    "Reward%3E0",
    "vrp-reward%3E0",
]

CANDIDATE_SEARCH_TEMPLATES = [
    "https://issues.chromium.org/issues?q=allpublic%20"
    + qualifier
    + "%20modified%3E{start_date}%20modified%3C{end_date}"
    for qualifier in REWARD_SEARCH_QUALIFIERS
]
SEARCH_SORT = "&s=modified_time:desc"
MAX_SEARCH_PAGES = 200


def build_search_url(year: int) -> str:
    """Build the primary search URL for a specific year."""
    return build_search_urls(year)[0]


def build_search_urls(year: int) -> list[str]:
    """Build candidate search URLs for a specific year."""
    start = f"{year}-01-01"
    end = f"{year + 1}-01-01"
    return [
        template.format(start_date=start, end_date=end) + SEARCH_SORT
        for template in CANDIDATE_SEARCH_TEMPLATES
    ]


def get_all_years() -> list[int]:
    """Get list of years from 2015 to current year."""
    return list(range(2015, datetime.now().year + 1))


# --- Bounty Detection ---
# Captures the dollar amount across the common award phrasings the panel uses:
#   "award you $5,000", "award $500", "awarded $1,000", "a VRP reward of $20,000"
BOUNTY_AWARD_PATTERN = re.compile(
    r'(?:award(?:ed)?(?:\s+you)?|reward of)\s+\$([\d,]+(?:\.\d+)?)', re.IGNORECASE
)
# Positive award signals.
# IMPORTANT: do NOT add the bare panel header "Chrome Vulnerability Rewards
# Program (VRP) Panel" here — the panel's automated emails use that exact header
# for DENIALS too ("...has decided that ... does not meet the criteria to qualify
# for a reward"), which previously mis-flagged ~22 denied reports as confirmed
# bounties. Keep indicators specific to an actual award action.
BOUNTY_INDICATORS = [
    "decided to award you",
    "decided to award",
    "VRP Panel has decided",
    "award you $",
    "Congratulations!",
]
# Hard-negative phrases from the panel's denial email. If any appears in an
# update, that update is a rejection — never an award — and overrides any
# positive indicator above. Guards against future header-phrasing changes.
BOUNTY_DENIAL_INDICATORS = [
    "does not meet the criteria",
    "does not meet the bar",
    "not eligible for",
    "does not qualify",
]

# --- Enum Mappings ---
STATUS_MAP = {
    1: "New",
    2: "Assigned",
    3: "Accepted",
    4: "Fixed",
    5: "Verified",
    6: "Not Reproducible",
    7: "Infeasible",
    8: "Intended Behavior",
    9: "Obsolete",
    10: "Duplicate",
}

SEVERITY_MAP = {
    0: "Unspecified",
    1: "S0-Critical",
    2: "S1-High",
    3: "S2-Medium",
    4: "S3-Low",
    5: "S4-Minimal",
}

PRIORITY_MAP = {
    0: "Unspecified",
    1: "P0",
    2: "P1",
    3: "P2",
    4: "P3",
    5: "P4",
}

# --- Custom Field IDs (from Chromium Issue Tracker) ---
FIELD_COMPONENT = 1222907
FIELD_CHROME_VERSION = 1223033
FIELD_OS = 1223084
FIELD_BOUNTY = 1223135

# --- Scraper Settings (env var overrides) ---
CONCURRENCY_LIMIT = int(os.environ.get("VRP_CONCURRENCY", "5"))
HEADLESS = os.environ.get("VRP_HEADLESS", "true").lower() == "true"
TIMEOUT = int(os.environ.get("VRP_TIMEOUT", "60000"))
DELAY_BETWEEN_ISSUES = float(os.environ.get("VRP_DELAY", "2"))
BROWSER_RESTART_INTERVAL = int(os.environ.get("VRP_BROWSER_RESTART", "100"))

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)
