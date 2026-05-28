"""Tests for vrp/extractor.py."""

import json
from unittest.mock import AsyncMock, patch

import pytest

from tests.fixtures import ISSUE_ID, make_raw_metadata, make_raw_updates


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
            await self._handler(response)

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

    assert result is True
    assert (issue_dir / ISSUE_ID / "raw_updates.json").exists()
    assert (issue_dir / ISSUE_ID / "raw_metadata.json").exists()
    assert (issue_dir / ISSUE_ID / "report.json").exists()
