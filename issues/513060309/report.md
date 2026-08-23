# Improper handling of side-effects of CopyFastSmiOrObjectElements in LateLoadElimination leads to a fake object / arbitrary write primitive

| Field | Value |
|-------|-------|
| **Issue ID** | [513060309](https://issues.chromium.org/issues/513060309) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | bj...@neodyme.io |
| **Assignee** | ni...@chromium.org |
| **Created** | 2026-05-14 |
| **Bounty** | $11,000.00 |

## Description

---

### Report description

V8 TurboShaft LateLoadElimination: AllocateOp and JSStackCheck Bypass Map Invalidation Fix

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

v8/src/compiler/turboshaft/late-load-elimination-reducer.cc

---

### The problem

#### Please describe the technical details of the vulnerability

## Summary

Two code-level variants of [bug 480438199](https://issues.chromium.org/issues/480438199) bypass the fix via early `break` statements.

**File:** `v8/src/compiler/turboshaft/late-load-elimination-reducer.cc`

**Original bug:** LateLoadElimination caches string maps but fails to invalidate them when GC scavenge occurs, causing type confusion.

**Original fix (commit af59a517e78, line 297-304):**

```
if (op.Effects().can_allocate && v8_flags.turbolev) {
  memory_.InvalidatePotentialLoadedStringMaps();
  WipeAllMaps();
}

```

**Variants:** `AllocateOp` (line 199-202) and `JSStackCheck` (line 260) break before reaching line 297, bypassing the fix.

**Reproduction:** Cannot reproduce crash on either version:

- V8 commit bdc8f396b7d (Jan 29, 2026) - same date as original [bug 480438199](https://issues.chromium.org/issues/480438199)
- V8 commit 05fdb31f32a (May 14, 2026) - current HEAD

Build config: is\_debug=true, is\_component\_build=true, v8\_optimized\_debug=false

Tested approaches:

- Original PoC from [bug 480438199](https://issues.chromium.org/issues/480438199) (no crash)
- AllocateOp via float operations
- JSStackCheck via deep recursion
- Various GC pressure patterns
- ThinString creation methods
- IC feedback manipulation
- 10,000+ retry loops

Result: 0 crashes on both versions.

Likely requires timing/environment specific conditions (specific GC timing, memory state, or hardware) not reproduced in our test environment. Google may be able to reproduce on internal infrastructure.

## Variant 1: AllocateOp Bypass

**Root cause:** `AllocateOp` case breaks at line 202, before reaching fix at line 297.

```
// Line 199-202: AllocateOp case
case Opcode::kAllocate:
  ProcessAllocate(op_idx, op.Cast<AllocateOp>());
  break;  // ← EXITS HERE, never reaches line 297

// Line 297-304: Fix that gets bypassed
if (op.Effects().can_allocate && v8_flags.turbolev) {
  memory_.InvalidatePotentialLoadedStringMaps();
  WipeAllMaps();
}

// Line 620-624: ProcessAllocate has NO invalidation
void LateLoadEliminationAnalyzer::ProcessAllocate(OpIndex op_idx,
                                                  const AllocateOp&) {
  non_aliasing_objects_.Set(op_idx, true);
  // NO map invalidation
}

```

**Verified:** AllocateOp has `CanAllocate()` effect (operations.h:3698-3706), breaks before fix, ProcessAllocate lacks invalidation.

## Variant 2: JSStackCheck Bypass

**Root cause:** JSStackCheck breaks at line 260, before reaching fix at line 297.

```
case Opcode::kJSStackCheck:
  break;  // ← Exits before line 297

```

**Verified:** JSStackCheck can allocate during stack overflow handling, breaks before fix, no invalidation.

## Why No Working PoC

IC feedback mechanism requires both comparison operands to be InternalizedStrings at runtime to emit `CheckedInternalizedString` nodes.

**Code location:** `v8/src/codegen/code-stub-assembler.cc:15856-15865`

```
TNode<Smi> CodeStubAssembler::CollectFeedbackForString(
    TNode<Int32T> instance_type) {
  TNode<Smi> feedback = SelectSmiConstant(
      Word32Equal(
          Word32And(instance_type, Int32Constant(kIsNotInternalizedMask)),
          Int32Constant(kInternalizedTag)),
      CompareOperationFeedback::kInternalizedString,  // IF internalized
      CompareOperationFeedback::kString);              // ELSE string
  return feedback;
}

```

**The problem:**

1. Warmup: `pwn("literal")` → both operands internalized → IC feedback = kInternalizedString
2. Maglev compiles with kInternalizedString hint → emits GetInternalizedString nodes
3. Turbolev lowers to CheckedInternalizedString → LateLoadElimination caches maps
4. Exploit: `pwn(thinString)` → ThinString NOT internalized → IC feedback = kString
5. No CheckedInternalizedString nodes → no cached maps → no bug path

**Unable to identify conditions to maintain kInternalizedString feedback while passing ThinString.**

## PoC

**File:** `poc-aggressive.js` (attached)

**Config:** V8 commit bdc8f396b7d, is\_debug=true, is\_component\_build=true, v8\_optimized\_debug=false  

**Command:** `d8 --turbolev poc-aggressive.js`  

**Result:** No crash after 10,000 attempts

## Verification

**Confirmed (code-level):**

- AllocateOp bypasses fix (line 199-202 breaks before line 297)
- JSStackCheck bypasses fix (line 260 breaks before line 297)
- ProcessAllocate has no invalidation (line 620-624)
- AllocateOp has CanAllocate() effect (operations.h:3698-3706)

**Not confirmed:**

- Exploitability (cannot reproduce crash)

## References

1. Original bug: Chromium [bug 480438199](https://issues.chromium.org/issues/480438199) (Jan 29, 2026)
2. Original fix: <https://chromium.googlesource.com/v8/v8/+/af59a517e78>

## Disclosure Timeline

- **Jan 29, 2026:** Original [bug 480438199](https://issues.chromium.org/issues/480438199) reported
- **Apr 23, 2026:** Original bug fixed (commit af59a517e78)
- **May 14, 2026:** Variants discovered and reported

#### Impact analysis

## Impact

**Severity:** High (similar to original [bug 480438199](https://issues.chromium.org/issues/480438199))

**Attack vector:**

- Web-reachable via JavaScript
- Renderer process (sandboxed)
- High complexity (requires specific IC feedback state)

**Potential impact:**

- Type confusion in V8 sandbox
- OOB write to controlled address
- Sandbox escape potential

**Note:** Impact is theoretical - exploitability not verified.

## Affected Versions

- V8 commit bdc8f396b7d (Jan 29, 2026) - tested
- V8 commit 05fdb31f32a (May 14, 2026) - tested
- All versions between original fix (af59a517e78, Apr 23, 2026) and present

**Status:** Unfixed as of May 14, 2026

---

### The cause

#### What version of Chrome have you found the security issue in?

Last version Stable Chrome

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Memory Corruption

#### How would you like to be publicly acknowledged for your report?

Quac Tran

## Attachments

- [poc-aggressive.js](attachments/poc-aggressive.js) (text/javascript, 2.2 KB)

## Timeline

### tr...@gmail.com (2026-05-14)

I think the problem is with my test environment, not with Vuln. I can't even reproduce the original Vuln with the same config and D8 version as the original Vuln with the poc in the original report.

### dm...@chromium.org (2026-05-15)

The `break`s break out of the `switch`, not out of the `for` loop. The map invalidation will thus happen as expected.

### ch...@google.com (2026-05-15)

This issue has been closed as an incomplete or invalid report and we will not respond to further comments. If you can improve your report please open a fresh issue that addresses any feedback provided.

For more information on our vulnerability policies, please refer to <https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md>

### ch...@google.com (2026-05-16)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### ch...@google.com (2026-08-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/513060309)*
