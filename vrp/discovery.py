"""Phase 1: Discover issue IDs from Chromium Issue Tracker search results."""

import asyncio
import csv
import io
import json
import re
from pathlib import Path

from playwright.async_api import async_playwright

from vrp.config import (
    DATA_DIR,
    HEADLESS,
    MAX_SEARCH_PAGES,
    QUEUE_FILE,
    TIMEOUT,
    USER_AGENT,
    build_search_urls,
    get_all_years,
)
from vrp.utils import load_json, logger, save_json


def _checkpoint_path(year: int) -> Path:
    return DATA_DIR / f"discovery_{year}.json"


def extract_issue_ids_from_links(links: list[str]) -> set[str]:
    """Extract unique issue IDs from a list of links."""
    issue_ids: set[str] = set()
    for link in links:
        match = re.search(r"/issues/(\d+)", link)
        if match:
            iid = match.group(1)
            if iid != "0":
                issue_ids.add(iid)
    return issue_ids


async def discover_ids_for_year(year: int, headless: bool = HEADLESS, resume: bool = True) -> set[str]:
    """Discover all issue IDs for a specific year."""
    checkpoint = _checkpoint_path(year)

    # Load existing checkpoint (unless caller explicitly disables resume)
    if resume:
        existing = load_json(checkpoint)
        if existing:
            logger.info(f"[{year}] Loaded {len(existing)} IDs from checkpoint")
            return set(existing)

    search_urls = build_search_urls(year)
    logger.info(f"[{year}] Discovering issues across {len(search_urls)} candidate searches")

    issue_ids: set[str] = set()

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=headless)
        context = await browser.new_context(user_agent=USER_AGENT)
        page = await context.new_page()

        try:
            for search_idx, search_url in enumerate(search_urls, start=1):
                await page.goto(search_url, wait_until="networkidle", timeout=TIMEOUT)
                page_count = 0

                while page_count < MAX_SEARCH_PAGES:
                    await asyncio.sleep(3)

                    links = await page.locator("a").evaluate_all(
                        "elements => elements.map(e => e.href)"
                    )
                    found_ids = extract_issue_ids_from_links(links)
                    found_new = 0
                    for iid in found_ids:
                        if iid not in issue_ids:
                            issue_ids.add(iid)
                            found_new += 1

                    logger.info(
                        f"[{year}] Search {search_idx}/{len(search_urls)} "
                        f"page {page_count + 1}: +{found_new} new, "
                        f"{len(issue_ids)} total"
                    )

                    next_btn = page.locator("button[aria-label='Go to next page']")
                    if await next_btn.is_visible() and await next_btn.is_enabled():
                        await next_btn.click()
                        await page.wait_for_load_state("networkidle")
                        page_count += 1
                    else:
                        logger.info(
                            f"[{year}] Search {search_idx}/{len(search_urls)} "
                            f"reached end at page {page_count + 1}"
                        )
                        break

        except Exception as e:
            logger.error(f"[{year}] Discovery error: {e}")
        finally:
            await page.close()
            await browser.close()

    # Save checkpoint
    if issue_ids:
        save_json(checkpoint, sorted(issue_ids))
        logger.info(f"[{year}] Saved checkpoint: {len(issue_ids)} IDs")

    return issue_ids


async def discover_all(
    years: list[int] | None = None,
    resume: bool = True,
    headless: bool = HEADLESS,
    seed_ids: list[str] | None = None,
) -> list[str]:
    """Run discovery for all years and merge into master queue.

    Args:
        years: Specific years to discover. Defaults to all years (2015-current).
        resume: Skip years that already have checkpoints.
        headless: Run browser in headless mode.

    Returns:
        Sorted list of all discovered issue IDs.
    """
    if years is None:
        years = get_all_years()

    all_ids: set[str] = set()

    if years == get_all_years():
        existing_queue = load_json(QUEUE_FILE)
        if existing_queue:
            all_ids.update(existing_queue)
            logger.info(f"Loaded {len(existing_queue)} IDs from existing queue")

    for year in sorted(years):
        checkpoint = _checkpoint_path(year)
        if resume and checkpoint.exists():
            cached = load_json(checkpoint) or []
            all_ids.update(cached)
            logger.info(f"[{year}] Skipped (checkpoint exists: {len(cached)} IDs)")
            continue

        year_ids = await discover_ids_for_year(year, headless=headless, resume=resume)
        all_ids.update(year_ids)

    if seed_ids:
        normalized = {str(iid) for iid in seed_ids if str(iid).isdigit()}
        all_ids.update(normalized)
        logger.info(f"Added {len(normalized)} seeded issue IDs")

    # Save master queue
    sorted_ids = sorted(all_ids)
    save_json(QUEUE_FILE, sorted_ids)
    logger.info(f"Master queue updated: {len(sorted_ids)} total IDs")

    return sorted_ids


def load_seed_issue_ids(seed_file: Path) -> list[str]:
    """Load explicit issue IDs from a JSON list or newline-delimited text file."""
    text = seed_file.read_text(encoding="utf-8")
    if seed_file.suffix.lower() == ".json":
        data = json.loads(text)
        if not isinstance(data, list):
            raise ValueError("seed JSON must be a list of issue IDs")
        return [str(item) for item in data if str(item).isdigit()]

    if seed_file.suffix.lower() == ".csv":
        reader = csv.DictReader(io.StringIO(text))
        ids: list[str] = []
        for row in reader:
            for value in row.values():
                if not value:
                    continue
                ids.extend(re.findall(r"crbug\.com/(\d+)", value))
        return sorted(set(ids))

    return [line.strip() for line in text.splitlines() if line.strip().isdigit()]
