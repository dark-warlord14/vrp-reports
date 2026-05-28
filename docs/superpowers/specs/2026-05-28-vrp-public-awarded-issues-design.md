# VRP Public Awarded Issues Coverage Redesign

## Goal

Redesign the scraper so the archive includes exactly the Chromium issues that are both public and publicly show evidence that a bounty was awarded.

For the current audit scope, the target is correctness for 2025-2026 and elimination of the verified misses in that window.

## Scope Definition

An issue is in scope only if all of the following are true:

1. The Chromium issue page is publicly accessible without authentication.
2. The public issue data shows bounty evidence:
   - a positive numeric reward in metadata, or
   - public award text in the issue updates.
3. The issue is a Chromium issue, not an external sheet row, summary row, or companion reference without public award evidence.

Out of scope:

- private or partially private issues
- public issues referenced by external sources but lacking public bounty evidence
- companion or sandbox issues without independent public bounty evidence
- duplicate or related issues unless they independently satisfy the inclusion rule

## Verified Failure Modes

### 1. Discovery misses valid candidates

Current discovery relies on a search URL constrained to:

- `Type:Vulnerability`
- a created-date year window
- DOM link scraping from the rendered search results page

This is too brittle and missed at least these verified in-scope public awarded issues:

- `351327767` -> public, reward field `20000`
- `384186547` -> public, reward field `20000`
- `386565144` -> public, reward field `50000`
- `481074858` -> public, reward field `11000`

Three of those were created in late 2024 but surfaced in 2025 reward activity, which shows that created-year discovery is not sufficient for coverage validation against rewarded reports.

### 2. Extraction rejects metadata-only awards

The extractor currently performs an early text-based bounty gate before full parsing. If award text is absent from public updates, the issue is dropped even when metadata exposes a positive reward amount.

This directly conflicts with the parser, which already accepts metadata reward fields as valid bounty evidence.

### 3. Coverage accounting conflates created year with reward evidence

The index is built around `created_date` year. That is acceptable as one reporting dimension, but it is not a safe measure of reward-year coverage. It makes the current dashboard and audit workflow harder to reason about.

### 4. Rejection paths are not auditable

Today, a missed issue can fail in discovery, fail in extraction, or be dropped as non-bounty without a durable explanation. That makes coverage analysis expensive and fragile.

## Design Principles

1. Separate candidate discovery from inclusion verdict.
2. Prefer structured public metadata over free-text heuristics.
3. Preserve enough raw evidence to explain why an issue was included or excluded.
4. Keep the existing project shape where possible. This is a targeted pipeline redesign, not a ground-up rewrite.

## Proposed Architecture

The pipeline remains five stages at a high level, but the middle stages change meaning:

1. discover candidates
2. fetch raw public issue data
3. verify public award evidence
4. generate reports for included issues
5. rebuild index and stats

### Candidate Discovery

Discovery should no longer try to return only final bounty issues. It should return a superset of public candidate IDs.

Candidate discovery sources:

1. Chromium issue tracker search results
2. optional seed lists for audit and reconciliation

The primary redesign is to stop scraping rendered anchor tags from the search UI. Instead, discovery should intercept and parse the underlying search response payload or another stable machine-readable response used by the page.

The candidate query should be broadened enough to avoid false negatives. False positives are acceptable because later verification becomes authoritative.

### Public Issue Fetch

For each candidate ID, fetch:

- raw metadata response
- raw updates response
- public accessibility verdict

Raw files should be saved before final inclusion is decided whenever the issue is public and fetchable. That gives us a stable offline corpus for reprocessing and audit.

For non-public issues, store a lightweight rejection artifact with the reason `not_public` instead of silently losing the candidate.

### Inclusion Verifier

Introduce an explicit verifier that produces a structured decision:

- `include`
- `exclude`
- `reason`

Decision rules:

1. If the issue is not public: exclude, `reason=not_public`
2. Else if metadata reward amount exists and is greater than zero: include, `reason=reward_amount_meta`
3. Else if public award-text evidence exists in updates: include, `reason=award_text`
4. Else: exclude, `reason=no_public_award_evidence`

This verifier becomes the only source of truth for `bounty_confirmed`.

### Report Model Extensions

The structured issue/report output should preserve how inclusion was determined.

Add fields such as:

- `public_issue: bool`
- `inclusion_reason: str`
- `reward_amount_meta: float | null`
- `award_text_found: bool`
- `award_text_source_update: int | null`

These fields are not just for debugging. They let the archive explain itself and support future reconciliation work.

### Audit Ledger

Add a candidate-level audit artifact, for example `data/candidate_audit.json` or per-issue audit metadata, to record:

- issue id
- discovered from which source
- public or not
- reward metadata value if present
- award text evidence if present
- final decision
- rejection reason when excluded

This must be generated as part of normal runs so coverage analysis does not require ad hoc scripts.

### Index and Stats

Keep `created_date` as an index field because it is still useful. Do not treat it as the archive's only temporal interpretation.

For now:

- keep existing created-year stats for compatibility
- add inclusion evidence fields to index entries

Future reward-year reporting can be layered on later if the raw data supports it cleanly.

## File-Level Changes

### `vrp/config.py`

- Replace the current narrow search template with candidate-oriented search configuration.
- Add configuration for optional audit seed inputs.
- Keep year scoping, but decouple it from final inclusion logic.

### `vrp/discovery.py`

- Replace DOM anchor scraping with parsing of the search response payload.
- Support merging candidate IDs from tracker search and optional seed files.
- Preserve discovery provenance per issue.

### `vrp/extractor.py`

- Remove the early raw-text bounty gate.
- Persist raw metadata and updates before final award verification when public data is available.
- Record explicit non-public and no-evidence exclusions.

### `vrp/parser.py`

- Refactor bounty verification into an explicit public award verifier.
- Treat positive metadata reward as first-class evidence.
- Preserve award detection details in the returned issue model.

### `vrp/models.py`

- Extend models to represent inclusion reason and public accessibility.
- Add any audit-specific structures needed for candidate decisions.

### `vrp/index_builder.py`

- Carry inclusion evidence fields into `index.json`.
- Keep backward-compatible created-year stats while exposing evidence metadata for auditability.

### `vrp/cli.py`

- Optionally support audit seed files and verification-only reruns.
- Improve status output so excluded candidates are visible.

### Tests

Add or update tests for:

1. metadata-only reward inclusion
2. award-text inclusion without metadata reward
3. public no-award exclusion
4. non-public exclusion
5. discovery ingestion from machine-readable search responses
6. preservation of audit reasons in output artifacts
7. regression covering the verified real-world misses represented as fixtures

## Recommended External Input Handling

External sources such as the published v8CTF sheet should be treated as audit seeds, not as authority.

Rules:

- external seeds may introduce candidate IDs
- external seeds do not themselves prove inclusion
- the public Chromium issue data remains authoritative for final inclusion

This matches the desired dataset definition and prevents the scraper from drifting into "externally referenced VRP-related issues" rather than "public Chromium issues with public award evidence."

## Migration Strategy

### Phase 1

Fix correctness with the least behavioral ambiguity:

- broaden candidate discovery
- remove early text gate
- add explicit verifier
- add tests for metadata-only rewards

### Phase 2

Add auditability:

- candidate audit ledger
- discovery provenance
- explicit exclusion reasons

### Phase 3

Backfill and verify:

- rerun 2025-2026
- confirm inclusion of verified misses
- reconcile with audit seeds and classify any remaining gaps

## Risks and Tradeoffs

### More candidate IDs

Broader discovery increases fetch volume and false positives. That is acceptable because verifier cost is lower than missing rewarded public issues.

### Search endpoint coupling

Moving from DOM scraping to search-response parsing changes what we couple to. That is still the better tradeoff because response payloads are more stable and testable than UI structure.

### Artifact growth

Keeping raw data and audit decisions for excluded public candidates increases storage. This is justified because the project goal is archival coverage, not minimal footprint.

## Success Criteria

The redesign is successful when all of the following are true:

1. The scraper includes the verified in-scope misses:
   - `351327767`
   - `384186547`
   - `386565144`
   - `481074858`
2. Metadata-only rewarded public issues are no longer dropped.
3. Public but unawarded issues are excluded with explicit reasons.
4. Non-public issues are excluded with explicit reasons.
5. Coverage audits can be explained from saved artifacts without one-off reverse engineering.

## Implementation Recommendation

Proceed with a targeted rewrite of discovery and award verification while preserving the existing CLI, markdown generation, and dashboard structure.

This is the highest-leverage change. The current failures come from discovery assumptions and premature bounty gating, not from the downstream rendering pipeline.
