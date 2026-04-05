# VRP Reports — Bug Fixes & Improvements Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix 5 confirmed bugs and 4 targeted improvements across `vrp/index_builder.py`, `vrp/parser.py`, `vrp/server.py`, `vrp/markdown_gen.py`, `vrp/cli.py`, and `vrp/extractor.py`.

**Architecture:** Each task is self-contained — fix one bug or improvement per commit. All existing tests must continue to pass. New tests written before implementation (TDD). Run tests from the repo root with `python -m pytest tests/ -v`.

**Tech Stack:** Python 3.14, pytest, Pydantic v2, aiohttp, Playwright, Click, Rich, markdownify

---

## File Map

| File | What Changes |
|------|-------------|
| `vrp/index_builder.py` | Fix `bounty_amount or 0` falsy bug; fix year extraction to use `datetime.fromisoformat` |
| `vrp/parser.py` | Add `logger` import; wrap `build_issue` parse calls in try/except; add debug log for unrecognized custom fields; replace string `find()` rationale extraction with compiled regex |
| `vrp/server.py` | Replace `filepath.read_bytes()` with chunked streaming loop |
| `vrp/markdown_gen.py` | Add `force: bool = False` parameter; skip regeneration when `report.md` is newer than `report.json` |
| `vrp/cli.py` | Add `--force` flag to `markdown` command |
| `vrp/extractor.py` | Add clarifying comment about batch safety (no logic change) |
| `tests/test_index_builder.py` | Add tests for `bounty_amount=0.0` and malformed `created_date` |
| `tests/test_parser.py` | Add tests for `build_issue` exception handling, unknown field logging, case-insensitive rationale extraction |
| `tests/test_server.py` | Add test that large files are served correctly via chunked streaming |
| `tests/test_markdown_gen.py` | Add tests for incremental skip and `--force` override |

---

## Task 1: Fix `index_builder.py` — `bounty_amount` falsy bug

**Files:**
- Modify: `vrp/index_builder.py:89-93`
- Test: `tests/test_index_builder.py`

- [ ] **Step 1: Write the failing test**

Add to `tests/test_index_builder.py` inside `class TestBuildStats:`:

```python
def test_zero_bounty_amount_counted_in_avg_and_histogram(self, tmp_path):
    """bounty_amount=0.0 is falsy; confirm it's not excluded from stats."""
    issues_dir = tmp_path / "issues"
    issues_dir.mkdir()
    # One issue with $0 bounty (confirmed), one with $5000
    _write_report(issues_dir, "1", {"bounty_amount": 0.0, "created_date": "2024-01-01T00:00:00+00:00"})
    _write_report(issues_dir, "2", {"bounty_amount": 5000.0, "created_date": "2024-01-01T00:00:00+00:00"})

    with patch("vrp.index_builder.ISSUES_DIR", issues_dir), \
         patch("vrp.index_builder.INDEX_FILE", tmp_path / "index.json"), \
         patch("vrp.index_builder.STATS_FILE", tmp_path / "stats.json"):
        from vrp.index_builder import rebuild_index, build_stats
        rebuild_index()
        stats = build_stats()

    assert stats["total_bounty"] == 5000.0
    # avg should be (0.0 + 5000.0) / 2 = 2500.0, not 5000.0 / 1 = 5000.0
    assert stats["avg_bounty"] == 2500.0
    # $0 should appear in the $0-500 histogram bucket
    zero_bucket = next(b for b in stats["bounty_histogram"] if b["range"] == "$0-500")
    assert zero_bucket["count"] == 1
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd /Users/shantanughumade/workspace/AI-Fuzzing/VRP-REPORTS && \
python -m pytest tests/test_index_builder.py::TestBuildStats::test_zero_bounty_amount_counted_in_avg_and_histogram -v
```

Expected: FAIL — `assert stats["avg_bounty"] == 2500.0` fails (actual: 5000.0)

- [ ] **Step 3: Fix `vrp/index_builder.py` lines 89–93**

Replace:
```python
    for entry in index:
        amount = entry.get("bounty_amount") or 0
        stats["total_bounty"] += amount
        if amount:
            bounty_amounts.append(amount)
```

With:
```python
    for entry in index:
        raw_amount = entry.get("bounty_amount")
        amount = raw_amount if raw_amount is not None else 0.0
        stats["total_bounty"] += amount
        if raw_amount is not None:
            bounty_amounts.append(raw_amount)
```

Also fix the `top_bounties` sort key on line 143 — replace:
```python
    top = sorted(index, key=lambda x: x.get("bounty_amount") or 0, reverse=True)[:20]
```
With:
```python
    top = sorted(index, key=lambda x: (x.get("bounty_amount") or 0) if x.get("bounty_amount") is not None else 0, reverse=True)[:20]
```

Simplify: just replace the lambda with:
```python
    top = sorted(index, key=lambda x: x.get("bounty_amount") if x.get("bounty_amount") is not None else -1, reverse=True)[:20]
```

- [ ] **Step 4: Run test to verify it passes**

```bash
python -m pytest tests/test_index_builder.py::TestBuildStats::test_zero_bounty_amount_counted_in_avg_and_histogram -v
```

Expected: PASS

- [ ] **Step 5: Run full test suite to check no regressions**

```bash
python -m pytest tests/test_index_builder.py -v
```

Expected: All PASS

- [ ] **Step 6: Commit**

```bash
git add vrp/index_builder.py tests/test_index_builder.py
git commit -m "fix: use is not None for bounty_amount to handle \$0 correctly"
```

---

## Task 2: Fix `index_builder.py` — Safe year extraction

**Files:**
- Modify: `vrp/index_builder.py:1-5` (imports) and `:29-35` (year extraction)
- Test: `tests/test_index_builder.py`

- [ ] **Step 1: Write the failing test**

Add to `tests/test_index_builder.py` inside `class TestRebuildIndex:`:

```python
def test_malformed_created_date_does_not_crash(self, tmp_path):
    """Year extraction must not crash on bad created_date values."""
    issues_dir = tmp_path / "issues"
    issues_dir.mkdir()
    # Report with a non-ISO created_date
    _write_report(issues_dir, "bad_date", {"created_date": "not-a-date"})
    index_file = tmp_path / "index.json"

    with patch("vrp.index_builder.ISSUES_DIR", issues_dir), \
         patch("vrp.index_builder.INDEX_FILE", index_file), \
         patch("vrp.index_builder.STATS_FILE", tmp_path / "stats.json"):
        from vrp.index_builder import rebuild_index
        count = rebuild_index()  # Must not raise

    assert count == 1
    import json
    entries = json.loads(index_file.read_text())
    assert entries[0]["year"] is None

def test_none_created_date_handled(self, tmp_path):
    issues_dir = tmp_path / "issues"
    issues_dir.mkdir()
    _write_report(issues_dir, "no_date", {"created_date": None})
    index_file = tmp_path / "index.json"

    with patch("vrp.index_builder.ISSUES_DIR", issues_dir), \
         patch("vrp.index_builder.INDEX_FILE", index_file), \
         patch("vrp.index_builder.STATS_FILE", tmp_path / "stats.json"):
        from vrp.index_builder import rebuild_index
        rebuild_index()

    import json
    entries = json.loads(index_file.read_text())
    assert entries[0]["year"] is None
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
python -m pytest tests/test_index_builder.py::TestRebuildIndex::test_malformed_created_date_does_not_crash tests/test_index_builder.py::TestRebuildIndex::test_none_created_date_handled -v
```

Expected: FAIL — `test_malformed_created_date_does_not_crash` fails because `int("not"[:4])` raises `ValueError` (caught by existing try/except but `year` remains None correctly... actually this might pass already). Verify behavior and proceed.

> **Note:** The existing code already has `try/except ValueError`, so `"not-a-date"` would just produce `year=None` without crashing. The tests may already pass. If so, move to Step 3 anyway to improve robustness.

- [ ] **Step 3: Improve year extraction in `vrp/index_builder.py`**

Add `from datetime import datetime` to the imports at the top of the file (line 4, after existing imports):

```python
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
```

Replace lines 29–35:
```python
                # Extract year from created_date
                year = None
                created = report.get("created_date")
                if created and len(created) >= 4:
                    try:
                        year = int(created[:4])
                    except ValueError:
                        pass
```

With:
```python
                # Extract year from created_date (ISO format)
                year = None
                created = report.get("created_date")
                if created:
                    try:
                        year = datetime.fromisoformat(created).year
                    except (ValueError, TypeError):
                        logger.warning("Could not parse created_date %r for issue %s", created, report.get("id"))
```

- [ ] **Step 4: Run all index_builder tests**

```bash
python -m pytest tests/test_index_builder.py -v
```

Expected: All PASS

- [ ] **Step 5: Commit**

```bash
git add vrp/index_builder.py tests/test_index_builder.py
git commit -m "fix: use datetime.fromisoformat for year extraction with warning on bad dates"
```

---

## Task 3: Fix `parser.py` — Error handling in `build_issue`

**Files:**
- Modify: `vrp/parser.py:1-16` (add logger import), `:238-309` (build_issue)
- Test: `tests/test_parser.py`

- [ ] **Step 1: Write the failing test**

Add to `tests/test_parser.py` inside `class TestBuildIssue:`:

```python
def test_build_issue_returns_none_when_parse_updates_raises(self):
    """build_issue must not propagate exceptions from parse_updates."""
    from unittest.mock import patch
    with patch("vrp.parser.parse_updates", side_effect=RuntimeError("API structure changed")):
        result = build_issue(ISSUE_ID, [], {})
    assert result is None

def test_build_issue_returns_none_when_parse_metadata_raises(self):
    """build_issue must not propagate exceptions from parse_metadata."""
    from unittest.mock import patch
    with patch("vrp.parser.parse_metadata", side_effect=RuntimeError("Unexpected metadata shape")):
        result = build_issue(ISSUE_ID, make_raw_updates(), make_raw_metadata())
    assert result is None
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
python -m pytest "tests/test_parser.py::TestBuildIssue::test_build_issue_returns_none_when_parse_updates_raises" "tests/test_parser.py::TestBuildIssue::test_build_issue_returns_none_when_parse_metadata_raises" -v
```

Expected: FAIL — `RuntimeError: API structure changed` propagates (ERROR, not FAIL assertion)

- [ ] **Step 3: Add logger import to `vrp/parser.py`**

Change the imports block (top of file) from:
```python
from vrp.config import (
    BOUNTY_AWARD_PATTERN, BOUNTY_INDICATORS, STATUS_MAP, SEVERITY_MAP,
    PRIORITY_MAP, FIELD_COMPONENT, FIELD_CHROME_VERSION, FIELD_OS, FIELD_BOUNTY,
)
from vrp.models import Attachment, Update, Issue
```

To:
```python
from vrp.config import (
    BOUNTY_AWARD_PATTERN, BOUNTY_INDICATORS, STATUS_MAP, SEVERITY_MAP,
    PRIORITY_MAP, FIELD_COMPONENT, FIELD_CHROME_VERSION, FIELD_OS, FIELD_BOUNTY,
)
from vrp.models import Attachment, Update, Issue
from vrp.utils import logger
```

- [ ] **Step 4: Wrap parse calls in `build_issue` with try/except**

In `vrp/parser.py`, replace lines 243–244 (the two bare parse calls at the start of `build_issue`):
```python
    updates = parse_updates(raw_updates, issue_id)
    metadata = parse_metadata(raw_metadata)
```

With:
```python
    try:
        updates = parse_updates(raw_updates, issue_id)
    except Exception:
        logger.error("parse_updates failed for issue %s", issue_id, exc_info=True)
        return None

    try:
        metadata = parse_metadata(raw_metadata)
    except Exception:
        logger.error("parse_metadata failed for issue %s", issue_id, exc_info=True)
        return None
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
python -m pytest "tests/test_parser.py::TestBuildIssue::test_build_issue_returns_none_when_parse_updates_raises" "tests/test_parser.py::TestBuildIssue::test_build_issue_returns_none_when_parse_metadata_raises" -v
```

Expected: PASS

- [ ] **Step 6: Run full parser test suite**

```bash
python -m pytest tests/test_parser.py -v
```

Expected: All PASS

- [ ] **Step 7: Commit**

```bash
git add vrp/parser.py tests/test_parser.py
git commit -m "fix: catch and log exceptions in build_issue instead of propagating"
```

---

## Task 4: Improve `parser.py` — Log unrecognized custom fields

**Files:**
- Modify: `vrp/parser.py:159-181` (parse_metadata custom fields loop)
- Test: `tests/test_parser.py`

> **Note:** This task requires the `logger` import added in Task 3. Do Task 3 first.

- [ ] **Step 1: Write the failing test**

Add to `tests/test_parser.py` inside `class TestParseMetadata:`:

```python
def test_unrecognized_field_emits_debug_log(self, caplog):
    """Unknown custom field IDs should be logged at DEBUG level."""
    import logging
    from vrp.config import FIELD_COMPONENT  # known field ID
    # Build metadata with an extra unknown field ID
    raw = make_raw_metadata()
    # Inject an unknown field into the custom_fields list
    # raw[0][1][22][2][14] is the custom_fields list
    unknown_field_id = 999999
    # Reach into the fixture structure to append an unknown field
    raw[0][1][22][2][14].append([unknown_field_id, "somevalue"] + [None] * 8)

    with caplog.at_level(logging.DEBUG, logger="vrp.parser"):
        from vrp.parser import parse_metadata
        parse_metadata(raw)

    assert any("999999" in r.message or str(unknown_field_id) in r.message
               for r in caplog.records if r.levelno == logging.DEBUG)
```

- [ ] **Step 2: Run test to verify it fails**

```bash
python -m pytest "tests/test_parser.py::TestParseMetadata::test_unrecognized_field_emits_debug_log" -v
```

Expected: FAIL — no debug log emitted for unknown field ID

- [ ] **Step 3: Add `else` clause to the custom fields loop in `vrp/parser.py`**

In `parse_metadata`, find the custom fields loop (lines ~169-180). Add an `else` clause after the final `elif field_id == FIELD_BOUNTY:` block:

```python
            if field_id == FIELD_COMPONENT:
                result["component"] = display_val or "Unknown"
            elif field_id == FIELD_CHROME_VERSION:
                result["chrome_version"] = str_val or display_val
            elif field_id == FIELD_OS:
                os_str = display_val or ""
                result["os_platforms"] = [
                    s.strip() for s in os_str.split(",") if s.strip()
                ]
            elif field_id == FIELD_BOUNTY:
                if isinstance(int_val, (int, float)):
                    result["bounty_amount_meta"] = float(int_val)
            else:
                logger.debug(
                    "Unrecognized custom field id=%s display=%s str=%s",
                    field_id, display_val, str_val,
                )
```

- [ ] **Step 4: Run test to verify it passes**

```bash
python -m pytest "tests/test_parser.py::TestParseMetadata::test_unrecognized_field_emits_debug_log" -v
```

Expected: PASS

- [ ] **Step 5: Run full parser test suite**

```bash
python -m pytest tests/test_parser.py -v
```

Expected: All PASS

- [ ] **Step 6: Commit**

```bash
git add vrp/parser.py tests/test_parser.py
git commit -m "feat: log unrecognized custom field IDs at DEBUG level in parse_metadata"
```

---

## Task 5: Improve `parser.py` — Regex rationale extraction

**Files:**
- Modify: `vrp/parser.py:7` (imports), `:185-213` (extract_bounty_info)
- Test: `tests/test_parser.py`

- [ ] **Step 1: Write the failing test**

Add to `tests/test_parser.py` inside `class TestExtractBountyInfo:`:

```python
def test_rationale_extracted_case_insensitive(self):
    """Rationale markers should match regardless of casing."""
    bounty_text = (
        "Chrome VRP Panel has decided to award you $1,000.\n\n"
        "RATIONALE FOR THIS DECISION: sandbox escape via type confusion.\n\n"
        "IMPORTANT: Please confirm receipt."
    )
    raw = make_raw_updates(bounty_text=bounty_text)
    updates = parse_updates(raw, ISSUE_ID)
    _, _, rationale = extract_bounty_info(updates)
    assert rationale is not None
    assert "sandbox escape" in rationale

def test_rationale_extracted_when_important_absent(self):
    """Rationale extraction works when 'Important:' is not present."""
    bounty_text = (
        "Chrome VRP Panel has decided to award you $2,000.\n\n"
        "Rationale for this decision: buffer overflow in audio decoder."
    )
    raw = make_raw_updates(bounty_text=bounty_text)
    updates = parse_updates(raw, ISSUE_ID)
    _, _, rationale = extract_bounty_info(updates)
    assert rationale is not None
    assert "buffer overflow" in rationale
```

- [ ] **Step 2: Run tests to verify the case-insensitive test fails**

```bash
python -m pytest "tests/test_parser.py::TestExtractBountyInfo::test_rationale_extracted_case_insensitive" "tests/test_parser.py::TestExtractBountyInfo::test_rationale_extracted_when_important_absent" -v
```

Expected: `test_rationale_extracted_case_insensitive` FAIL (current `str.find()` is case-sensitive); `test_rationale_extracted_when_important_absent` may pass already (existing fallback handles missing "Important:").

- [ ] **Step 3: Replace string find() with compiled regex in `vrp/parser.py`**

`re` is already imported at the top. Add the compiled pattern as a module-level constant after the existing imports (before `def safe_get`):

```python
# Compiled once at import time for efficiency
_RATIONALE_RE = re.compile(
    r'Rationale for this decision:\s*(.*?)(?=Important:|$)',
    re.DOTALL | re.IGNORECASE,
)
```

Replace the rationale extraction block in `extract_bounty_info` (lines ~198-209):
```python
        # Extract rationale (text between "Rationale for this decision:" and "Important:")
        rationale = None
        text = update.text_plain
        rat_start = text.find("Rationale for this decision:")
        if rat_start != -1:
            rat_text = text[rat_start + len("Rationale for this decision:"):]
            rat_end = rat_text.find("Important:")
            if rat_end == -1:
                rat_end = rat_text.find("\n\n\n")
            if rat_end != -1:
                rationale = rat_text[:rat_end].strip()
            else:
                rationale = rat_text[:500].strip()
```

With:
```python
        # Extract rationale using regex (case-insensitive, stops at "Important:")
        rationale = None
        text = update.text_plain
        rat_match = _RATIONALE_RE.search(text)
        if rat_match:
            rationale = rat_match.group(1).strip()[:500]
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
python -m pytest "tests/test_parser.py::TestExtractBountyInfo::test_rationale_extracted_case_insensitive" "tests/test_parser.py::TestExtractBountyInfo::test_rationale_extracted_when_important_absent" -v
```

Expected: Both PASS

- [ ] **Step 5: Run full parser test suite**

```bash
python -m pytest tests/test_parser.py -v
```

Expected: All PASS

- [ ] **Step 6: Commit**

```bash
git add vrp/parser.py tests/test_parser.py
git commit -m "feat: replace fragile str.find rationale extraction with compiled regex"
```

---

## Task 6: Fix `server.py` — Chunked file streaming

**Files:**
- Modify: `vrp/server.py:72-80`
- Test: `tests/test_server.py`

- [ ] **Step 1: Write the failing test**

Add to `tests/test_server.py` inside `class TestServerRouting:`:

```python
def test_large_file_served_correctly(self, dirs):
    """Server must correctly serve files larger than a single chunk (8192 bytes)."""
    ui, data = dirs
    # 64KB file — larger than the 8192-byte chunk size
    large_content = b"A" * 65536
    (data / "large.bin").write_bytes(large_content)
    with ServerFixture(ui, data, port=19890) as srv:
        status, headers, body = srv.get("/data/large.bin")
    assert status == 200
    assert len(body) == 65536
    assert body == large_content
```

- [ ] **Step 2: Run test to verify it passes already (baseline)**

```bash
python -m pytest "tests/test_server.py::TestServerRouting::test_large_file_served_correctly" -v
```

Expected: PASS (current code works correctly, just loads into memory). This establishes a regression baseline.

- [ ] **Step 3: Replace `filepath.read_bytes()` with chunked streaming in `vrp/server.py`**

Replace lines 72–80:
```python
        try:
            content = filepath.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, str(e))
```

With:
```python
        try:
            file_size = filepath.stat().st_size
            self.send_response(200)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", str(file_size))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            _CHUNK = 8192
            with open(filepath, "rb") as f:
                while True:
                    chunk = f.read(_CHUNK)
                    if not chunk:
                        break
                    self.wfile.write(chunk)
        except Exception as e:
            self.send_error(500, str(e))
```

- [ ] **Step 4: Run test to verify it still passes**

```bash
python -m pytest "tests/test_server.py::TestServerRouting::test_large_file_served_correctly" -v
```

Expected: PASS

- [ ] **Step 5: Run full server test suite**

```bash
python -m pytest tests/test_server.py -v
```

Expected: All PASS

- [ ] **Step 6: Commit**

```bash
git add vrp/server.py tests/test_server.py
git commit -m "fix: stream files in 8KB chunks instead of loading entire file into memory"
```

---

## Task 7: Improve `markdown_gen.py` + `cli.py` — Incremental markdown generation

**Files:**
- Modify: `vrp/markdown_gen.py:153-176` (generate_all_markdown)
- Modify: `vrp/cli.py:61-67` (markdown command)
- Test: `tests/test_markdown_gen.py`

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_markdown_gen.py` inside `class TestGenerateAllMarkdown:`:

```python
def test_skips_report_md_newer_than_report_json(self, tmp_path):
    """When report.md is newer than report.json, skip regeneration."""
    import time
    issues_dir = tmp_path / "issues"
    _setup_issue(issues_dir, ISSUE_ID)
    idir = issues_dir / ISSUE_ID

    with patch("vrp.markdown_gen.ISSUES_DIR", issues_dir):
        from vrp.markdown_gen import generate_all_markdown
        # First run: generates report.md
        count1 = generate_all_markdown()
    assert count1 == 1

    # Touch report.md so its mtime is strictly newer than report.json
    time.sleep(0.01)
    (idir / "report.md").touch()

    # Overwrite report.md with sentinel content to detect if regenerated
    sentinel = "SENTINEL_DO_NOT_OVERWRITE"
    (idir / "report.md").write_text(sentinel)
    # Set report.md mtime after report.json
    time.sleep(0.01)
    (idir / "report.md").touch()

    with patch("vrp.markdown_gen.ISSUES_DIR", issues_dir):
        from vrp.markdown_gen import generate_all_markdown
        count2 = generate_all_markdown()

    # Should be skipped (count=0), sentinel should still be there
    assert count2 == 0
    assert (idir / "report.md").read_text() == sentinel

def test_force_flag_regenerates_even_if_up_to_date(self, tmp_path):
    """force=True bypasses the mtime check."""
    import time
    issues_dir = tmp_path / "issues"
    _setup_issue(issues_dir, ISSUE_ID)
    idir = issues_dir / ISSUE_ID

    with patch("vrp.markdown_gen.ISSUES_DIR", issues_dir):
        from vrp.markdown_gen import generate_all_markdown
        generate_all_markdown()

    # Stamp report.md as newer, write sentinel
    time.sleep(0.01)
    (idir / "report.md").touch()
    sentinel = "SENTINEL"
    (idir / "report.md").write_text(sentinel)
    time.sleep(0.01)
    (idir / "report.md").touch()

    with patch("vrp.markdown_gen.ISSUES_DIR", issues_dir):
        from vrp.markdown_gen import generate_all_markdown
        count = generate_all_markdown(force=True)

    # Should regenerate
    assert count == 1
    assert (idir / "report.md").read_text() != sentinel
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
python -m pytest "tests/test_markdown_gen.py::TestGenerateAllMarkdown::test_skips_report_md_newer_than_report_json" "tests/test_markdown_gen.py::TestGenerateAllMarkdown::test_force_flag_regenerates_even_if_up_to_date" -v
```

Expected: FAIL — `generate_all_markdown` doesn't accept `force` parameter; always regenerates.

- [ ] **Step 3: Update `generate_all_markdown` in `vrp/markdown_gen.py`**

Replace lines 153–176 (the entire `generate_all_markdown` function):
```python
def generate_all_markdown() -> int:
    """Generate report.md for all issues that have report.json.

    Returns count of generated files.
    """
    if not ISSUES_DIR.exists():
        logger.error("No issues directory found.")
        return 0

    issue_dirs = sorted([d for d in ISSUES_DIR.iterdir() if d.is_dir()])
    logger.info(f"Generating markdown for {len(issue_dirs)} issues...")

    count = 0
    with create_progress() as progress:
        task = progress.add_task("Generating markdown", total=len(issue_dirs))

        for idir in issue_dirs:
            if (idir / "report.json").exists():
                if generate_report_markdown(idir.name):
                    count += 1
            progress.update(task, advance=1)

    logger.info(f"Generated {count} markdown files")
    return count
```

With:
```python
def generate_all_markdown(force: bool = False) -> int:
    """Generate report.md for all issues that have report.json.

    Skips issues where report.md already exists and is newer than report.json,
    unless force=True.

    Returns count of generated (or regenerated) files.
    """
    if not ISSUES_DIR.exists():
        logger.error("No issues directory found.")
        return 0

    issue_dirs = sorted([d for d in ISSUES_DIR.iterdir() if d.is_dir()])
    logger.info(f"Generating markdown for {len(issue_dirs)} issues...")

    count = 0
    with create_progress() as progress:
        task = progress.add_task("Generating markdown", total=len(issue_dirs))

        for idir in issue_dirs:
            json_path = idir / "report.json"
            md_path = idir / "report.md"

            if not json_path.exists():
                progress.update(task, advance=1)
                continue

            if not force and md_path.exists():
                if md_path.stat().st_mtime >= json_path.stat().st_mtime:
                    progress.update(task, advance=1)
                    continue

            if generate_report_markdown(idir.name):
                count += 1
            progress.update(task, advance=1)

    logger.info(f"Generated {count} markdown files")
    return count
```

- [ ] **Step 4: Add `--force` flag to the `markdown` command in `vrp/cli.py`**

Replace lines 61–67:
```python
@cli.command()
def markdown():
    """Generate/regenerate markdown for all reports."""
    from vrp.markdown_gen import generate_all_markdown

    count = generate_all_markdown()
    console.print(f"[green]Generated {count} markdown files[/green]")
```

With:
```python
@cli.command()
@click.option("--force", is_flag=True, help="Regenerate all markdown even if already up-to-date")
def markdown(force):
    """Generate/regenerate markdown for all reports."""
    from vrp.markdown_gen import generate_all_markdown

    count = generate_all_markdown(force=force)
    console.print(f"[green]Generated {count} markdown files[/green]")
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
python -m pytest "tests/test_markdown_gen.py::TestGenerateAllMarkdown::test_skips_report_md_newer_than_report_json" "tests/test_markdown_gen.py::TestGenerateAllMarkdown::test_force_flag_regenerates_even_if_up_to_date" -v
```

Expected: Both PASS

- [ ] **Step 6: Run full markdown and CLI test suites**

```bash
python -m pytest tests/test_markdown_gen.py tests/test_cli.py -v
```

Expected: All PASS

- [ ] **Step 7: Commit**

```bash
git add vrp/markdown_gen.py vrp/cli.py tests/test_markdown_gen.py
git commit -m "feat: incremental markdown generation — skip up-to-date files, add --force flag"
```

---

## Task 8: Clarify `extractor.py` — Document batch safety

**Files:**
- Modify: `vrp/extractor.py:198-209` (batch loop comment)

> **Investigation finding:** The browser context race condition (Bug 2) is NOT present in the current code. `asyncio.gather(*tasks)` already ensures all tasks in a batch — including their `DELAY_BETWEEN_ISSUES` sleeps — complete fully before `context.close()` is called. The existing code is safe. This task adds a comment to make the intent explicit so future developers don't inadvertently break the pattern.

- [ ] **Step 1: Add clarifying comment in `vrp/extractor.py`**

Find lines 198–209 (the batch loop):
```python
            # Process in batches to allow browser restart
            batch_size = BROWSER_RESTART_INTERVAL
            for i in range(0, len(issue_ids), batch_size):
                batch = issue_ids[i : i + batch_size]
                tasks = [process_one(iid) for iid in batch]
                await asyncio.gather(*tasks)

                # Restart browser between batches
                if i + batch_size < len(issue_ids):
                    logger.info("Restarting browser context...")
                    await context.close()
                    context = await browser.new_context(user_agent=USER_AGENT)
```

Replace with:
```python
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
```

- [ ] **Step 2: Run full test suite to confirm nothing broke**

```bash
python -m pytest tests/ -v
```

Expected: All PASS

- [ ] **Step 3: Commit**

```bash
git add vrp/extractor.py
git commit -m "docs: clarify that asyncio.gather ensures safe browser context restart"
```

---

## Final Verification

- [ ] **Run the entire test suite**

```bash
python -m pytest tests/ -v --tb=short
```

Expected: All tests pass, 0 failures.

- [ ] **Verify CLI help shows --force flag**

```bash
python -m vrp.cli markdown --help
```

Expected output includes `--force  Regenerate all markdown even if already up-to-date`
