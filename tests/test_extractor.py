"""Tests for vrp/extractor.py."""

import asyncio
import json
from unittest.mock import AsyncMock, patch

import pytest

from tests.fixtures import ISSUE_ID, make_raw_metadata, make_raw_updates

_real_sleep = asyncio.sleep


class _FakeResponse:
    def __init__(self, url: str, data):
        self.url = url
        self.headers = {"content-type": "application/json"}
        self._body = ")]}'\n" + json.dumps(data)

    async def text(self):
        return self._body


class _FakePage:
    def __init__(self, responses):
        self._responses = responses
        self._handler = None

    def on(self, event, handler):
        assert event == "response"
        self._handler = handler

    async def goto(self, url, wait_until=None, timeout=None):
        assert self._handler is not None
        for response in self._responses:
            self._handler(response)

    async def close(self):
        return None


class _FakeContext:
    def __init__(self, page):
        self._page = page

    async def new_page(self):
        return self._page


@pytest.mark.asyncio
async def test_metadata_only_reward_is_not_rejected_by_preparse_gate(tmp_path):
    issue_dir = tmp_path / "issues"
    issue_dir.mkdir(parents=True)

    raw_updates = make_raw_updates(bounty_text="No public award text.")
    raw_metadata = make_raw_metadata(bounty_amount=3000)
    page = _FakePage(
        [
            _FakeResponse("https://issues.chromium.org/action/issues/123/updates", raw_updates),
            _FakeResponse("https://issues.chromium.org/action/issues/123/getIssue", raw_metadata),
        ]
    )
    context = _FakeContext(page)

    with patch("vrp.extractor.ISSUES_DIR", issue_dir), \
         patch("vrp.extractor.CORPUS_DIR", tmp_path / "corpus"), \
         patch("vrp.extractor._extract_cookies", AsyncMock(return_value={})), \
         patch("vrp.extractor.write_issue_corpus"), \
         patch("vrp.extractor.aiohttp.ClientSession"), \
         patch("vrp.extractor.asyncio.sleep", AsyncMock()):
        from vrp.extractor import scrape_issue

        result = await scrape_issue(ISSUE_ID, context)

    assert result == "bounty"
    assert (issue_dir / ISSUE_ID / "raw_updates.json").exists()
    assert (issue_dir / ISSUE_ID / "raw_metadata.json").exists()
    assert (issue_dir / ISSUE_ID / "report.json").exists()


class _SlowResponse(_FakeResponse):
    """Response whose body read is still in flight when goto() returns."""

    async def text(self):
        for _ in range(3):
            await _real_sleep(0)
        return self._body


@pytest.mark.asyncio
async def test_in_flight_response_body_is_drained_before_capture_check(tmp_path):
    issue_dir = tmp_path / "issues"
    issue_dir.mkdir(parents=True)

    raw_updates = make_raw_updates(bounty_text="No public award text.")
    raw_metadata = make_raw_metadata(bounty_amount=3000)
    page = _FakePage(
        [
            _SlowResponse("https://issues.chromium.org/action/issues/123/updates", raw_updates),
            _SlowResponse("https://issues.chromium.org/action/issues/123/getIssue", raw_metadata),
        ]
    )
    context = _FakeContext(page)

    with patch("vrp.extractor.ISSUES_DIR", issue_dir), \
         patch("vrp.extractor.CORPUS_DIR", tmp_path / "corpus"), \
         patch("vrp.extractor._extract_cookies", AsyncMock(return_value={})), \
         patch("vrp.extractor.write_issue_corpus"), \
         patch("vrp.extractor.aiohttp.ClientSession"), \
         patch("vrp.extractor.asyncio.sleep", AsyncMock()):
        from vrp.extractor import scrape_issue

        result = await scrape_issue(ISSUE_ID, context)

    assert result == "bounty"
    assert (issue_dir / ISSUE_ID / "raw_updates.json").exists()
    assert (issue_dir / ISSUE_ID / "report.json").exists()


@pytest.mark.asyncio
async def test_non_bounty_issue_returns_no_bounty_and_cleans_up(tmp_path):
    issue_dir = tmp_path / "issues"
    issue_dir.mkdir(parents=True)

    # No award text in updates and no reward amount in metadata -> not a bounty.
    raw_updates = make_raw_updates(bounty_text="Thanks, but this is not eligible for a reward.")
    raw_metadata = make_raw_metadata(bounty_amount=None)
    page = _FakePage(
        [
            _FakeResponse("https://issues.chromium.org/action/issues/123/updates", raw_updates),
            _FakeResponse("https://issues.chromium.org/action/issues/123/getIssue", raw_metadata),
        ]
    )
    context = _FakeContext(page)

    with patch("vrp.extractor.ISSUES_DIR", issue_dir), \
         patch("vrp.extractor.CORPUS_DIR", tmp_path / "corpus"), \
         patch("vrp.extractor._extract_cookies", AsyncMock(return_value={})), \
         patch("vrp.extractor.write_issue_corpus"), \
         patch("vrp.extractor.aiohttp.ClientSession"), \
         patch("vrp.extractor.asyncio.sleep", AsyncMock()):
        from vrp.extractor import scrape_issue

        result = await scrape_issue(ISSUE_ID, context)

    assert result == "no_bounty"
    # Raw files for non-bounty issues are cleaned up, leaving no report behind.
    assert not (issue_dir / ISSUE_ID).exists()


# ---------------------------------------------------------------------------
# _unique_attachment_name — collision-safe attachment filenames
# ---------------------------------------------------------------------------

class _Att:
    """Minimal stand-in with the .filename / .id attributes the helper reads."""
    def __init__(self, id, filename):
        self.id = id
        self.filename = filename


def test_unique_attachment_name_disambiguates_collisions():
    from vrp.extractor import _unique_attachment_name

    used: set[str] = set()
    a = _unique_attachment_name(_Att(101, "poc.html"), used)
    b = _unique_attachment_name(_Att(202, "poc.html"), used)
    c = _unique_attachment_name(_Att(303, "poc.html"), used)

    # First keeps the bare name; later clashes get the attachment id, extension preserved.
    assert a == "poc.html"
    assert b == "poc_202.html"
    assert c == "poc_303.html"
    assert len({a, b, c}) == 3


def test_unique_attachment_name_handles_no_extension():
    from vrp.extractor import _unique_attachment_name

    used: set[str] = set()
    first = _unique_attachment_name(_Att(1, "README"), used)
    second = _unique_attachment_name(_Att(2, "README"), used)
    assert first == "README"
    assert second == "README_2"


# ---------------------------------------------------------------------------
# scrape_all — no-bounty checkpoint skips repeat browser scrapes
# ---------------------------------------------------------------------------

class _FakeBrowser:
    async def new_context(self, **kw):
        return _FakeContext(None)

    async def close(self):
        return None


class _FakeChromium:
    async def launch(self, **kw):
        return _FakeBrowser()


class _FakePlaywright:
    def __init__(self):
        self.chromium = _FakeChromium()


class _FakePlaywrightCM:
    async def __aenter__(self):
        return _FakePlaywright()

    async def __aexit__(self, *a):
        return False


@pytest.mark.asyncio
async def test_scrape_all_skips_known_no_bounty_on_rerun(tmp_path, monkeypatch):
    issue_dir = tmp_path / "issues"
    issue_dir.mkdir(parents=True)
    no_bounty_file = tmp_path / "no_bounty.json"

    scraped = []

    async def fake_scrape_issue(iid, context, force=False):
        scraped.append(iid)
        # "200" is a bounty (keeps a report), "300" is no-bounty (no trace)
        if iid == "200":
            (issue_dir / iid).mkdir(parents=True, exist_ok=True)
            (issue_dir / iid / "report.json").write_text("{}")
            return "bounty"
        return "no_bounty"

    with patch("vrp.extractor.ISSUES_DIR", issue_dir), \
         patch("vrp.extractor.NO_BOUNTY_FILE", no_bounty_file), \
         patch("vrp.extractor.async_playwright", lambda: _FakePlaywrightCM()), \
         patch("vrp.extractor.scrape_issue", fake_scrape_issue), \
         patch("vrp.extractor.asyncio.sleep", AsyncMock()):
        from vrp.extractor import scrape_all

        # First run: both issues scraped; "300" recorded as no-bounty.
        await scrape_all(issue_ids=["200", "300"], headless=True)
        assert sorted(scraped) == ["200", "300"]
        assert json.loads(no_bounty_file.read_text()) == ["300"]

        # Second run: "200" skipped (has report.json), "300" skipped (no-bounty).
        scraped.clear()
        await scrape_all(issue_ids=["200", "300"], headless=True)
        assert scraped == []

        # recheck_empty re-scrapes the no-bounty issue.
        scraped.clear()
        await scrape_all(issue_ids=["200", "300"], headless=True, recheck_empty=True)
        assert scraped == ["300"]


# ---------------------------------------------------------------------------
# Access-restricted issues must stay retryable (not cached as no-bounty)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_permission_denied_returns_no_capture(tmp_path):
    issue_dir = tmp_path / "issues"
    issue_dir.mkdir(parents=True)
    denied = {"message": "com.google.apps.framework.auth.IamPermissionDeniedException: "
                         "Unsigned-in user does not have permission to view issue 123."}
    page = _FakePage([
        _FakeResponse("https://issues.chromium.org/action/issues/123/updates", denied),
        _FakeResponse("https://issues.chromium.org/action/issues/123/getIssue", denied),
    ])
    context = _FakeContext(page)
    with patch("vrp.extractor.ISSUES_DIR", issue_dir), \
         patch("vrp.extractor.CORPUS_DIR", tmp_path / "corpus"), \
         patch("vrp.extractor._extract_cookies", AsyncMock(return_value={})), \
         patch("vrp.extractor.write_issue_corpus"), \
         patch("vrp.extractor.aiohttp.ClientSession"), \
         patch("vrp.extractor.asyncio.sleep", AsyncMock()):
        from vrp.extractor import scrape_issue
        result = await scrape_issue(ISSUE_ID, context)
    # Not "no_bounty" — so it won't be recorded in the no-bounty checkpoint.
    assert result == "no_capture"
    assert not (issue_dir / ISSUE_ID).exists()


# ---------------------------------------------------------------------------
# reprocess_existing self-heals: a now-disqualified report is removed
# ---------------------------------------------------------------------------

def test_reprocess_removes_disqualified_report(tmp_path):
    import json as _json

    from tests.fixtures import make_raw_metadata, make_raw_updates
    issue_dir = tmp_path / "issues"
    iid = "555000111"
    d = issue_dir / iid
    d.mkdir(parents=True)
    # Raw data is a panel DENIAL (parses cleanly, but no bounty under current logic)
    denial = ("Hello, Chrome Vulnerability Rewards Program (VRP) Panel has decided that "
              "the security impact of this issue does not meet the criteria to qualify "
              "for a reward.")
    (d / "raw_updates.json").write_text(_json.dumps(make_raw_updates(bounty_text=denial)))
    (d / "raw_metadata.json").write_text(_json.dumps(make_raw_metadata(bounty_amount=0)))
    # A stale report.json from when the old parser mis-flagged it as a bounty
    (d / "report.json").write_text(_json.dumps({"id": iid, "bounty_confirmed": True}))
    nb = tmp_path / "no_bounty.json"

    with patch("vrp.extractor.ISSUES_DIR", issue_dir), \
         patch("vrp.extractor.CORPUS_DIR", tmp_path / "corpus"), \
         patch("vrp.extractor.NO_BOUNTY_FILE", nb), \
         patch("vrp.extractor.write_issue_corpus"):
        from vrp.extractor import reprocess_existing
        reprocess_existing()

    assert not d.exists(), "stale false-positive report should be removed"
    assert iid in set(_json.loads(nb.read_text()))
