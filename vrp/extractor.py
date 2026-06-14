"""Phase 2: Extract data from individual issues.

Handles both live scraping (via Playwright) and offline reprocessing
of existing raw JSON files.
"""

import asyncio
import json
import shutil
from pathlib import Path

import aiohttp
from playwright.async_api import BrowserContext, async_playwright

from vrp.config import (
    BROWSER_RESTART_INTERVAL,
    CONCURRENCY_LIMIT,
    CORPUS_DIR,
    DELAY_BETWEEN_ISSUES,
    HEADLESS,
    ISSUES_DIR,
    NO_BOUNTY_FILE,
    QUEUE_FILE,
    TIMEOUT,
    USER_AGENT,
)
from vrp.corpus import write_issue_corpus
from vrp.parser import build_issue, parse_updates
from vrp.utils import (
    create_progress,
    download_file,
    load_json,
    logger,
    sanitize_filename,
    save_json,
    save_json_if_changed,
)


def _issue_dir(issue_id: str) -> Path:
    return ISSUES_DIR / issue_id


def _has_raw_data(issue_id: str) -> bool:
    d = _issue_dir(issue_id)
    return (d / "raw_updates.json").exists()


def _has_report(issue_id: str) -> bool:
    return (_issue_dir(issue_id) / "report.json").exists()


def _is_permission_denied(data) -> bool:
    """True if a captured response is an access-denied error rather than issue data.

    Restricted security issues return {"message": "...PermissionDenied...does not
    have permission to view issue..."}. These must NOT be treated as "no bounty"
    (which would cache them in the no-bounty checkpoint and skip them forever):
    Chrome opens many security bugs to the public weeks later, so they should
    stay retryable.
    """
    return (
        isinstance(data, dict)
        and "permission" in str(data.get("message", "")).lower()
    )


def _unique_attachment_name(att, used: set[str]) -> str:
    """Return a collision-free on-disk filename for an attachment.

    Two distinct attachments (different ids) can carry the same filename. Without
    disambiguation the second would map onto the first's downloaded file, so its
    own content is silently dropped. On a clash we append the attachment id,
    preserving the extension. Deterministic given the (stable) attachment order,
    so the scrape and offline-reprocess paths agree on the same names.
    """
    fname = sanitize_filename(att.filename)
    if fname in used:
        stem, dot, ext = fname.rpartition(".")
        fname = f"{stem}_{att.id}.{ext}" if dot else f"{fname}_{att.id}"
    used.add(fname)
    return fname


async def _extract_cookies(context: BrowserContext) -> dict:
    """Extract cookies from browser context for authenticated downloads."""
    cookies = await context.cookies()
    return {c["name"]: c["value"] for c in cookies}


async def scrape_issue(
    issue_id: str,
    context: BrowserContext,
    force: bool = False,
) -> str:
    """Scrape a single issue from the Chromium Issue Tracker.

    Returns an outcome string describing what happened:
      - "exists":     already scraped, skipped
      - "bounty":     bounty report found and saved
      - "no_capture": page loaded but no updates JSON was captured
      - "no_bounty":  data captured/parsed but no bounty award present
      - "error":      an exception occurred while scraping
    """
    idir = _issue_dir(issue_id)

    # Skip if already processed (unless force)
    if not force and _has_report(issue_id):
        return "exists"

    url = f"https://issues.chromium.org/issues/{issue_id}"
    captured = {"updates": None, "metadata": None}
    pending: set[asyncio.Task] = set()

    async def _capture(response):
        try:
            body = await response.text()
            if body.startswith(")]}'"):
                body = body[4:].strip()
            data = json.loads(body)
            if "updates" in response.url:
                captured["updates"] = data
            else:
                captured["metadata"] = data
        except Exception as e:
            logger.warning(f"Response handler error for {issue_id}: {e}")

    def on_response(response):
        ct = response.headers.get("content-type", "")
        if "json" in ct and ("updates" in response.url or "getIssue" in response.url):
            task = asyncio.create_task(_capture(response))
            pending.add(task)
            task.add_done_callback(pending.discard)

    page = await context.new_page()
    page.on("response", on_response)

    try:
        await page.goto(url, wait_until="networkidle", timeout=TIMEOUT)

        # Both XHRs (updates + getIssue metadata) can fire after networkidle, and
        # their body reads can still be in flight; poll until BOTH are captured
        # rather than breaking on the first. The metadata holds the authoritative
        # numeric reward field, so breaking as soon as `updates` arrived (the old
        # behavior) meant a lagging/throttled metadata response was missed and a
        # reward-field-only bounty got mis-classified as no-bounty — then cached
        # stickily. Waiting for both prevents that false negative.
        for _ in range(20):
            if pending:
                await asyncio.gather(*pending, return_exceptions=True)
            if captured["updates"] and captured["metadata"]:
                break
            await asyncio.sleep(0.5)
        if pending:
            await asyncio.gather(*pending, return_exceptions=True)

        # Extract cookies after navigation so auth cookies are populated
        cookies = await _extract_cookies(context)

        if not captured["updates"]:
            logger.warning(
                f"{issue_id}: no updates JSON captured "
                f"(metadata captured: {captured['metadata'] is not None})"
            )
            return "no_capture"

        if _is_permission_denied(captured["updates"]) or _is_permission_denied(captured["metadata"]):
            # Access-restricted issue: keep it retryable (do NOT record no-bounty)
            # since it may be opened to the public later.
            logger.warning(f"{issue_id}: access-restricted (not public) — leaving retryable")
            return "no_capture"

        if not captured["metadata"]:
            # Without the metadata response we can't read the authoritative reward
            # field, so we cannot safely conclude "no bounty". Keep it retryable
            # rather than risk a sticky false-negative.
            logger.warning(f"{issue_id}: metadata not captured — leaving retryable (not no-bounty)")
            return "no_capture"

        logger.debug(
            f"{issue_id}: captured updates (metadata: "
            f"{captured['metadata'] is not None}), parsing..."
        )

        # Save raw data first (for reprocessing later)
        idir.mkdir(parents=True, exist_ok=True)
        save_json(idir / "raw_updates.json", captured["updates"])
        if captured["metadata"]:
            save_json(idir / "raw_metadata.json", captured["metadata"])

        # Parse and build structured report
        issue = build_issue(issue_id, captured["updates"], captured["metadata"])
        if not issue:
            # Clean up raw files for non-bounty issues
            for f in idir.iterdir():
                f.unlink()
            idir.rmdir()
            return "no_bounty"

        logger.info(f"BOUNTY: {issue_id} - ${issue.bounty_amount or '?'} - {issue.title[:60]}")

        # Download attachments using a shared session for connection reuse
        att_dir = idir / "attachments"
        used_names: set[str] = set()
        async with aiohttp.ClientSession() as dl_session:
            for att in issue.attachments:
                fname = _unique_attachment_name(att, used_names)
                local_path = att_dir / fname
                if not local_path.exists():
                    ok = await download_file(
                        att.url, str(local_path), cookies=cookies,
                        expected_mime=att.mime_type, session=dl_session,
                    )
                    if not ok:
                        att.local_path = None
                        continue
                att.local_path = f"attachments/{fname}"

        # Save enriched report
        save_json(idir / "report.json", issue.model_dump())
        write_issue_corpus(issue, idir, CORPUS_DIR)

        return "bounty"

    except Exception as e:
        logger.error(f"Error scraping {issue_id}: {e}")
        return "error"
    finally:
        await page.close()


async def scrape_all(
    issue_ids: list[str] | None = None,
    force: bool = False,
    headless: bool = HEADLESS,
    recheck_empty: bool = False,
) -> int:
    """Scrape all queued issues.

    Args:
        issue_ids: Specific IDs to scrape. Defaults to discovery queue.
        force: Re-scrape even if report already exists.
        headless: Run browser in headless mode.
        recheck_empty: Re-scrape issues previously recorded as no-bounty. By
            default those are skipped (they leave no report.json, so without the
            no_bounty checkpoint they'd be browser-scraped every run). Set when
            re-evaluating in case a reward was added since the last scrape.

    Returns:
        Number of bounty reports found.
    """
    if issue_ids is None:
        queue = load_json(QUEUE_FILE)
        if not queue:
            logger.error("No discovery queue found. Run 'vrp discover' first.")
            return 0
        issue_ids = queue

    no_bounty_ids: set[str] = set(load_json(NO_BOUNTY_FILE) or [])

    # Filter out already-processed unless force
    if not force:
        # Skip both issues we already have a report for AND issues previously
        # confirmed to carry no bounty — re-scraping the latter every run via a
        # full browser load was the dominant cost of a no-change re-run.
        skip_empty = set() if recheck_empty else no_bounty_ids
        pending = [
            iid for iid in issue_ids
            if not _has_report(iid) and iid not in skip_empty
        ]
        skipped_empty = sum(1 for iid in issue_ids if iid in skip_empty and not _has_report(iid))
        logger.info(
            f"Queue: {len(issue_ids)} total, {len(pending)} pending "
            f"({skipped_empty} known no-bounty skipped)"
        )
        issue_ids = pending
    else:
        logger.info(f"Queue: {len(issue_ids)} total (force mode)")

    if not issue_ids:
        logger.info("Nothing to scrape.")
        # Persist the (possibly unchanged) checkpoint so the file always exists
        # for downstream consumers, e.g. the CI commit step.
        save_json(NO_BOUNTY_FILE, sorted(no_bounty_ids))
        return 0

    bounty_count = 0
    # Tally every per-issue outcome so the run summary explains *why* issues
    # were or weren't included (visible in CI logs and locally).
    outcomes: dict[str, int] = {
        "exists": 0,
        "bounty": 0,
        "no_capture": 0,
        "no_bounty": 0,
        "error": 0,
    }
    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=headless)
        context = await browser.new_context(user_agent=USER_AGENT)

        processed = 0
        with create_progress() as progress:
            task = progress.add_task("Scraping issues", total=len(issue_ids))

            async def process_one(iid: str):
                nonlocal bounty_count, processed
                async with semaphore:
                    result = await scrape_issue(iid, context, force=force)
                    outcomes[result] = outcomes.get(result, 0) + 1
                    if result == "bounty":
                        bounty_count += 1
                        # A previously-empty issue that now has a bounty must
                        # leave the skip list so it isn't filtered out later.
                        no_bounty_ids.discard(iid)
                    elif result == "no_bounty":
                        no_bounty_ids.add(iid)
                    processed += 1
                    progress.update(task, advance=1)
                    await asyncio.sleep(DELAY_BETWEEN_ISSUES)

            # Process in batches to allow periodic browser restart.
            # asyncio.gather(*tasks) fully awaits ALL tasks in the batch
            # (including their DELAY_BETWEEN_ISSUES sleeps) before we proceed,
            # so context.close() is only called after every task has released
            # its semaphore and completed. This prevents use-after-close races.
            batch_size = BROWSER_RESTART_INTERVAL
            for i in range(0, len(issue_ids), batch_size):
                batch = issue_ids[i : i + batch_size]
                tasks = [process_one(iid) for iid in batch]
                await asyncio.gather(*tasks)  # all batch tasks finish here

                # Safe to restart context — no in-flight tasks remain
                if i + batch_size < len(issue_ids):
                    logger.info("Restarting browser context...")
                    await context.close()
                    context = await browser.new_context(user_agent=USER_AGENT)

        await browser.close()

    # Persist the no-bounty determinations so subsequent runs can skip them.
    save_json(NO_BOUNTY_FILE, sorted(no_bounty_ids))

    logger.info(
        f"Scraping complete: {bounty_count} bounty reports found out of "
        f"{len(issue_ids)} processed"
    )
    logger.info(
        "Outcome breakdown: "
        f"bounty={outcomes['bounty']}, "
        f"no_bounty={outcomes['no_bounty']}, "
        f"no_capture={outcomes['no_capture']}, "
        f"error={outcomes['error']}, "
        f"already_had_report={outcomes['exists']}"
    )
    if outcomes["no_capture"] or outcomes["error"]:
        logger.warning(
            f"{outcomes['no_capture']} issues yielded no captured data and "
            f"{outcomes['error']} errored — these were NOT inspected for bounties. "
            "Run with VRP_LOG_LEVEL=DEBUG to see per-issue detail."
        )
    return bounty_count


def reprocess_existing() -> int:
    """Re-parse all existing raw JSON files to generate enriched reports.

    This does NOT re-scrape -- it only processes already-downloaded data.
    Returns count of successfully reprocessed reports.
    """
    if not ISSUES_DIR.exists():
        logger.error("No issues directory found.")
        return 0

    issue_dirs = sorted([d for d in ISSUES_DIR.iterdir() if d.is_dir()])
    logger.info(f"Reprocessing {len(issue_dirs)} existing issues...")

    no_bounty_ids: set[str] = set(load_json(NO_BOUNTY_FILE) or [])
    count = 0
    removed = 0
    with create_progress() as progress:
        task = progress.add_task("Reprocessing", total=len(issue_dirs))

        for idir in issue_dirs:
            issue_id = idir.name

            raw_updates = load_json(idir / "raw_updates.json")
            raw_metadata = load_json(idir / "raw_metadata.json")

            if not raw_updates:
                progress.update(task, advance=1)
                continue

            issue = build_issue(issue_id, raw_updates, raw_metadata)
            if (
                issue is None
                and raw_metadata
                and (idir / "report.json").exists()
                and parse_updates(raw_updates, issue_id)
            ):
                # Previously stored as a bounty, but re-evaluation with the
                # current parser finds none. The raw updates parsed cleanly (a
                # non-empty list), so this is a genuine de-qualification — e.g. a
                # report the detection logic no longer counts — not a parse
                # failure. Remove the stale report so the dataset self-heals when
                # detection is tightened, and remember it as no-bounty.
                shutil.rmtree(idir, ignore_errors=True)
                for cf in CORPUS_DIR.glob(f"{issue_id}_*.js"):
                    cf.unlink()
                no_bounty_ids.add(issue_id)
                removed += 1
                progress.update(task, advance=1)
                continue
            if issue:
                # Update local_path for any existing attachment files
                att_dir = idir / "attachments"
                if att_dir.exists():
                    existing_files = {f.name for f in att_dir.iterdir() if f.is_file()}
                    used_names: set[str] = set()
                    for att in issue.attachments:
                        # Mirror the scrape path's disambiguation so colliding
                        # filenames resolve to the same on-disk names here.
                        fname = _unique_attachment_name(att, used_names)
                        if fname in existing_files:
                            att.local_path = f"attachments/{fname}"
                        else:
                            # If file isn't downloaded, clear local_path to avoid broken links
                            att.local_path = None

                # Only rewrite when the parsed result actually changed. This
                # keeps report.json's mtime stable on no-change re-runs, so the
                # markdown stage's mtime-skip isn't defeated and a re-run stays
                # cheap instead of regenerating everything. Corpus derives from
                # the same data, so skip it too when nothing changed.
                if save_json_if_changed(idir / "report.json", issue.model_dump()):
                    write_issue_corpus(issue, idir, CORPUS_DIR)
                    count += 1

            progress.update(task, advance=1)

    if removed:
        save_json(NO_BOUNTY_FILE, sorted(no_bounty_ids))
        logger.info(f"Removed {removed} reports that no longer qualify as bounties")
    logger.info(f"Reprocessed: {count} reports changed (of {len(issue_dirs)} scanned)")
    return count
