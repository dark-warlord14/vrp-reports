"""Tests for vrp/discovery.py and discovery-related config."""

from vrp.config import build_search_urls
from vrp.discovery import extract_issue_ids_from_links


def test_build_search_urls_targets_candidate_searches():
    urls = build_search_urls(2025)
    assert len(urls) == 1
    assert any("vrp-reward%3E0" in url for url in urls)
    assert any("allpublic" in url for url in urls)
    assert all("modified%3E2025-01-01" in url for url in urls)
    assert all("modified%3C2026-01-01" in url for url in urls)
    assert all("Type:Vulnerability" not in url for url in urls)


def test_extract_issue_ids_from_links_dedupes_and_ignores_zero():
    links = [
        "https://issues.chromium.org/issues/123",
        "https://issues.chromium.org/issues/0",
        "https://issues.chromium.org/issues/123?pli=1",
        "https://example.com/not-an-issue",
        "https://issues.chromium.org/issues/456",
    ]
    assert extract_issue_ids_from_links(links) == {"123", "456"}
