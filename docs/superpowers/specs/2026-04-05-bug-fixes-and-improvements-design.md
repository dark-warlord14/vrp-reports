# VRP Reports — Bug Fixes & Improvements Design

**Date:** 2026-04-05  
**Scope:** Option B — fix 5 confirmed bugs + 4 targeted improvements  
**Files touched:** `vrp/index_builder.py`, `vrp/extractor.py`, `vrp/parser.py`, `vrp/server.py`, `vrp/markdown_gen.py`, `vrp/cli.py`, relevant test files

---

## Bug Fixes

### Bug 1 — `index_builder.py`: Falsy `bounty_amount` exclusion
**Location:** `vrp/index_builder.py` ~line 90  
**Problem:** `entry.get("bounty_amount") or 0` silently drops entries where `bounty_amount == 0.0` because `0.0` is falsy in Python.  
**Fix:** Replace all truthiness checks on `bounty_amount` with explicit `is not None` checks:
```python
# Before
if entry.get("bounty_amount"):
# After
if entry.get("bounty_amount") is not None:
```
Applies in both the filtering loop and the stats accumulation in `build_stats`.

---

### Bug 2 — `extractor.py`: Browser context race condition
**Location:** `vrp/extractor.py` ~lines 200–209  
**Problem:** `context.close()` is called at the browser-restart interval while in-flight async tasks may still hold a reference to the closing context, causing `playwright` errors on the next page navigation.  
**Fix:** Before `context.close()`, wait for all currently-running tasks in the batch to complete. Use `asyncio.gather(*pending_tasks)` to await them before closing. The existing semaphore already limits concurrency; add a `tasks: list` that tracks the current batch and await it fully before the context close + recreate sequence.

---

### Bug 3 — `index_builder.py`: Silent year extraction failure
**Location:** `vrp/index_builder.py` ~lines 31–35  
**Problem:** `int(created[:4])` silently produces a wrong or crashing result if `created_date` is not ISO-formatted (e.g., `None`, empty string, or differently formatted).  
**Fix:** Use `datetime.fromisoformat(created).year` inside a `try/except ValueError`, log a warning on failure, default `year` to `None`.

---

### Bug 4 — `server.py`: Full file read into memory
**Location:** `vrp/server.py` ~line 73  
**Problem:** `filepath.read_bytes()` loads the entire file into memory before sending. For large attachments (videos, archives), this can exhaust memory under concurrent requests.  
**Fix:** Replace with a chunked read loop:
```python
CHUNK = 8192
with open(filepath, "rb") as f:
    while chunk := f.read(CHUNK):
        self.wfile.write(chunk)
```
No change in behavior for clients.

---

### Bug 5 — `parser.py`: Silent parse failures
**Location:** `vrp/parser.py`, `build_issue` function ~lines 238–309  
**Problem:** If `parse_updates` or `parse_metadata` raise an unexpected exception (e.g., due to API structure changes), `build_issue` propagates it silently or crashes without identifying the issue ID.  
**Fix:** Wrap both calls in `try/except Exception`, log the issue ID and full traceback at `ERROR` level, return `None` to allow the pipeline to continue processing other issues.

---

## Improvements

### Improvement 6 — `parser.py`: Logging for unrecognized API fields
**Location:** `vrp/parser.py`, `parse_metadata` custom field loop  
**Problem:** When a custom field ID doesn't match FIELD_COMPONENT, FIELD_CHROME_VERSION, FIELD_OS, or FIELD_BOUNTY, it is silently ignored. API drift goes undetected.  
**Fix:** Add `logger.debug("Unrecognized custom field id=%s value=%s issue=%s", field_id, value, issue_id)` for unmatched field IDs. This surfaces in logs when run with debug verbosity without adding noise to normal operation.

---

### Improvement 7 — `parser.py`: Regex rationale extraction
**Location:** `vrp/parser.py`, `extract_bounty_info` ~lines 200–209  
**Problem:** `str.find()` slicing is fragile when "Rationale for this decision:" or "Important:" appear multiple times or in unexpected casing.  
**Fix:** Compile and use a regex:
```python
_RATIONALE_RE = re.compile(
    r'Rationale for this decision:\s*(.*?)(?=\bImportant:|$)',
    re.DOTALL | re.IGNORECASE
)
```
Use `_RATIONALE_RE.search(text)` and take group 1, stripped. Falls back to `None` if no match. Existing tests updated to cover edge cases.

---

### Improvement 8 — `markdown_gen.py`: Incremental generation
**Location:** `vrp/markdown_gen.py`, `generate_all_markdown`; `vrp/cli.py`, `markdown` command  
**Problem:** Every `markdown` run regenerates all `.md` files even when `report.json` hasn't changed — slow on large datasets.  
**Fix:**
- In `generate_all_markdown`, skip if `report.md` exists and `report.md.mtime >= report.json.mtime`.
- Add `force: bool = False` parameter; when `True`, skip the mtime check.
- Add `--force` flag to the `markdown` CLI command that passes `force=True`.

---

## What Is Not Changing
- Discovery and scraping logic (Playwright, pagination, checkpointing)
- Pydantic data models
- UI/frontend (app.js, components.js, CSS)
- Test fixture structures
- Build pipeline (build.sh, _headers, pyproject.toml)

## Testing Strategy
- Update `test_index_builder.py`: add test for `bounty_amount=0.0` being counted
- Update `test_parser.py`: add test for `extract_bounty_info` with repeated markers; add test for `build_issue` logging on exception
- Update `test_server.py`: verify chunked response for large files
- Update `test_markdown_gen.py`: add test for incremental skip; add test for `--force` override
- All existing tests must continue to pass
