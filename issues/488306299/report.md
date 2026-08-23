# Turboshaft WLE correctness bug: stale StringPrepareForGetCodeUnit result survives calls, leaks V8 heap pointers via charCodeAt

| Field | Value |
|-------|-------|
| **Issue ID** | [488306299](https://issues.chromium.org/issues/488306299) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>JavaScript |
| **Platforms** | Linux, Windows, ChromeOS |
| **Reporter** | fl...@outlook.com |
| **Assignee** | aj...@chromium.org |
| **Created** | 2026-02-27 |
| **Bounty** | $1,000.00 |

## Description

Title: Turboshaft WLE correctness bug: stale StringPrepareForGetCodeUnit
       result survives calls, leaks V8 heap pointers via charCodeAt

Vulnerability Type: JIT Compiler Correctness Bug / Information Leak
Severity:          High
Component:         Blink>JavaScript>WebAssembly (Turboshaft WLE)
Affected:          Chrome 130+ (all versions with shipped js-string builtins)
Tested:            V8 13.6.233.10 (x86_64, Linux), Chrome 145.0.7632.117 (Win)
Trigger:           Standard web content, NO Chrome flags required

NOTE TO TRIAGE:
This is a JIT compiler correctness bug causing a deterministic V8 heap
pointer leak. It is NOT a hang or resource exhaustion. Please reproduce
using d8 (V8 developer shell) to confirm the output divergence:
  d8 --no-liftoff wle_stale_ptr_d8.js           -> leaks pointer (BUG)
  d8 --liftoff --no-wasm-tier-up wle_stale_ptr_d8.js  -> correct values
ASAN will NOT trigger because the stale read is in-bounds (reading internal
ThinString fields instead of SeqString char data due to stale optimization).
See section 3 for details.

================================================================================
1. REPRODUCTION
================================================================================

Attached files:
  - wle_stale_ptr_d8.js  (d8 PoC, self-contained, no dependencies)
  - verify_leak.js       (verification script, requires --allow-natives-syntax)

  # Turboshaft — produces WRONG charCodeAt values (BUG):
  d8 --no-liftoff --no-wasm-lazy-compilation wle_stale_ptr_d8.js

  # Liftoff — produces CORRECT charCodeAt values (baseline):
  d8 --liftoff --no-wasm-tier-up wle_stale_ptr_d8.js

Output with --no-liftoff (Turboshaft):

  Before callback (WLE cache populated - should be correct):
    charCodeAt(0) = 0x4100  expected 0x4100  OK
    charCodeAt(1) = 0x4200  expected 0x4200  OK

  After callback (SPFGCU cache survives -> stale base+offset):
    charCodeAt(0) = 0xa5c5  expected 0x4100  STALE
    charCodeAt(1) = 0x0019  expected 0x4200  STALE
    charCodeAt(2) = 0x0969  expected 0x4300  STALE
    charCodeAt(3) = 0x0000  expected 0x4400  STALE
    charCodeAt(4) = 0x0018  expected 0x4500  STALE
    charCodeAt(5) = 0x0000  expected 0x4600  STALE
    charCodeAt(6) = 0x4700  expected 0x4700  OK
    charCodeAt(7) = 0x4800  expected 0x4800  OK

  Leaked 32-bit values (composed from 16-bit stale reads):
    ThinString.actual (compressed ptr): 0x0019a5c5

  Stale reads: 100 / 100

Output with --liftoff --no-wasm-tier-up (Liftoff):

  Stale reads: 0 / 100

The same Wasm function produces different results depending on compilation
tier. Turboshaft returns V8-internal ThinString fields as character data.
Liftoff returns correct character values. This is a compiler correctness bug.

================================================================================
2. VERIFICATION: LEAKED VALUES ARE V8 HEAP POINTERS
================================================================================

Attached: verify_leak.js (run with --allow-natives-syntax --no-liftoff)

The following five lines of evidence prove the stale charCodeAt values are
real V8 compressed heap pointers, not JavaScript-level artifacts.

--- 2.1 In-place type mutation confirmed via %DebugPrint ---

  Fresh string (BEFORE internalization):
  0x04ff0004d359 <String[8]: u"\x4100\x4200\x4300\x4400\x4500\x4600\x4700\x4800">

  Same string (AFTER internalization via obj[s]=42):
  0x04ff0004d359 <String[8]: u>"\x4100\x4200\x4300\x4400\x4500\x4600\x4700\x4800">

  Same address (0x04ff0004d359), type changes from u"..." (SeqTwoByteString)
  to u>"..." (internalized). The > marker confirms in-place mutation to
  ThinString. The object was NOT freed and reallocated — it was mutated.

--- 2.2 Stale read pattern matches ThinString+Filler layout byte-for-byte ---

  SeqTwoByteString (8 two-byte chars = 28 bytes):
    Byte 0-11:  Header (Map + Hash + Length)
    Byte 12-27: Character data

  After internalization -> ThinString (16 bytes) + Filler (12 bytes):
    Byte 0-11:  Header (Map changed, Hash/Length preserved)
    Byte 12-15: ThinString.actual (compressed ptr to interned string)
    Byte 16-19: Filler map pointer
    Byte 20-23: Filler size field
    Byte 24-27: ORIGINAL char data (never overwritten!)

  Stale charCodeAt reads (base still points to byte 12):
    charCodeAt(0) = 0xabb1  STALE  <- byte 12-13: ThinString.actual
    charCodeAt(1) = 0x0019  STALE  <- byte 14-15: ThinString.actual
    charCodeAt(2) = 0x0969  STALE  <- byte 16-17: Filler map
    charCodeAt(3) = 0x0000  STALE  <- byte 18-19: Filler map
    charCodeAt(4) = 0x0018  STALE  <- byte 20-21: Filler size
    charCodeAt(5) = 0x0000  STALE  <- byte 22-23: Filler size
    charCodeAt(6) = 0x4700  OK     <- byte 24-25: original char data
    charCodeAt(7) = 0x4800  OK     <- byte 26-27: original char data

  charCodeAt(6) and charCodeAt(7) return CORRECT values because bytes 24-27
  were never overwritten: ThinString (16 bytes) + Filler header (8 bytes)
  only occupies bytes 0-23, leaving the trailing character data intact.
  This pattern is impossible to explain as a JavaScript-level artifact.

--- 2.3 Leaked pointer has V8 compressed heap pointer properties ---

  Composed from charCodeAt(0,1): 0x0019abb1

  - Tagged (LSB=1): YES (V8 HeapObject tag)
  - Non-zero: YES
  - 32-bit range: YES (V8 compressed pointer space)
  - Full address: cage_base + 0x0019abb1

  The cage base is derived from %DebugPrint output (0x04ff00000000).
  Full address 0x04ff0019abb1 is in the same V8 heap cage as all other
  objects in this isolate.

--- 2.4 Different string content -> different leaked pointer ---

  String A (0x4100,0x4200,...):  leaked pointer = 0x0019abb1
  String B (0x6100,0x6200,...):  leaked pointer = 0x0019ac21

  Pointers DIFFER. Each ThinString.actual points to a different string
  table entry. The leaked value depends on which interned string the
  ThinString references — exactly the behavior expected for reading
  ThinString.actual from the V8 heap.

--- 2.5 Same content, two runs -> same leaked pointer ---

  String A run 1: leaked 0x0019abb1
  String A run 2: leaked 0x0019abb1

  Pointers MATCH. Both ThinStrings point to the same string table entry.
  The leak is deterministic and consistent within an isolate.

--- 2.6 Summary of evidence ---

  Five independent lines of evidence confirm: charCodeAt returns the
  V8-internal ThinString.actual field (a compressed heap pointer to the
  interned string in V8's string table). This is not a JavaScript-level
  artifact, rounding error, or coincidence. It is a deterministic V8 heap
  address leak exposing internal object graph pointers to untrusted code.

================================================================================
3. NOTE ON ASAN (re: previous closure of this bug)
================================================================================

This bug was previously filed as https://issues.chromium.org/issues/487336019
and closed as
"not reproducible in ASAN". ASAN cannot detect this bug by design:

The stale reads occur WITHIN the original heap allocation. V8's string
internalization converts SeqString to ThinString IN-PLACE (same memory,
no free/realloc). There is no out-of-bounds access and no use-after-free.
ASAN only detects OOB and UAF.

The security issue is that V8-internal compressed heap pointers (the
ThinString.actual field) become visible to untrusted Wasm/JS code as
charCodeAt return values. This is a type confusion within valid memory.

The attached d8 repro demonstrates clear tier divergence with --no-liftoff
vs --liftoff --no-wasm-tier-up, confirming a Turboshaft optimization bug
independent of ASAN detection.

================================================================================
4. SUMMARY
================================================================================

The Turboshaft Wasm Load Elimination (WLE) pass caches the result of
StringPrepareForGetCodeUnitOp as immutable. This cached result contains
the base pointer and offset to a string's character data. When a JS callback
internalizes the string in-place (SeqString -> ThinString), the cached
pointer becomes stale. Subsequent charCodeAt calls reuse the stale result
and read ThinString header fields (including compressed heap pointers)
instead of character data.

The trigger path requires NO Chrome flags. The "wasm:js-string" charCodeAt
builtin is shipped since Chrome 130 and is intrinsically inlined by
Turboshaft into StringPrepareForGetCodeUnit IR nodes.

================================================================================
5. ROOT CAUSE
================================================================================

Two issues combine to create this bug:

--- 5.1 Missing .CanReadMemory() effect (necessary but NOT sufficient) ---

File: src/compiler/turboshaft/operations.h

  StringPrepareForGetCodeUnitOp (lines 8000-8005) declares:

    static constexpr OpEffects effects =
        OpEffects().CanDependOnChecks();

  It reads string internals (map, instance_type, character data pointer) but
  does NOT declare .CanReadMemory(). For comparison, StringAsWtf16Op
  (lines 7975-7984) correctly declares BOTH:

    static constexpr OpEffects effects =
        OpEffects().CanDependOnChecks().CanReadMemory();

  However, fixing this alone is INSUFFICIENT — see 5.2.

--- 5.2 Structural disconnect: WLE ignores OpEffects for LoadLike entries ---

File: src/compiler/turboshaft/wasm-load-elimination-reducer.h

  The WLE caching logic is completely independent of OpEffects. This means
  adding .CanReadMemory() to SPFGCU would not fix the bug:

  1) InsertLoadLike (line 276) hardcodes mutability=false:

       static constexpr bool mutability = false;  // IMMUTABLE

     This is used for ALL LoadLike operations regardless of their effects.

  2) ProcessStringAsWtf16 (line 844) and ProcessStringPrepareForGetCodeUnit
     (line 857) both cache via InsertLoadLike → both get mutability=false.

  3) InvalidateMaybeAliasing (line 197) skips all immutable entries:

       if (key.data().mem.mutability == false) {
         ++it;
         continue;  // <--- SKIPS IMMUTABLE
       }

  4) ProcessCall (line 896) only checks the CALL's effects:

       if (!op.Effects().can_write()) return;

     It never consults the effects of the cached operations themselves.
     After the check, it calls InvalidateMaybeAliasing, which skips all
     immutable entries per (3).

  Proof that OpEffects are ignored: StringAsWtf16Op DOES declare
  .CanReadMemory() (operations.h:7979), yet its cached entry is still
  immutable (via InsertLoadLike) and survives calls. The effects system
  and the WLE cache are structurally decoupled.

================================================================================
6. EXPLOIT SEQUENCE
================================================================================

  1. Pre-intern a string S_INTERN by using it as a property key.

  2. Compile a Wasm module that imports "wasm:js-string" "charCodeAt" with
     WebAssembly.compile(bytes, { builtins: ['js-string'] }).
     Turboshaft inlines charCodeAt as SPFGCU + raw loads.

  3. The Wasm exploit function:
     a) Calls charCodeAt(s, 0) and charCodeAt(s, 1) on a fresh SeqString s.
        -> WLE caches StringPrepareForGetCodeUnit(s) as immutable.
     b) Calls a JS callback that does obj[s] = 42.
        -> V8 internalizes s in-place: SeqString -> ThinString.
        -> WLE's InvalidateMaybeAliasing skips the immutable SPFGCU entry.
     c) Calls charCodeAt(s, 0..7) again.
        -> WLE reuses stale cached SPFGCU result.
        -> Reads ThinString.actual (compressed heap pointer) as char data.
        -> Leaked pointer visible to Wasm/JS.

  4. With --no-liftoff: 100/100 stale reads (deterministic).
     With --liftoff --no-wasm-tier-up: 0/100 stale reads (correct).

  In a browser context (no flags), ~50k warmup calls trigger Turboshaft
  tier-up, after which the bug triggers deterministically.

================================================================================
7. IMPACT
================================================================================

  - Deterministic leak of V8 compressed heap pointers to Wasm/JS
  - Breaks V8 pointer compression / heap ASLR
  - 100% reproducible, no user interaction beyond page load
  - Reachable from standard web content (shipped js-string builtins)
  - Strong addressof primitive for RCE exploit chains

================================================================================
8. SUGGESTED FIX
================================================================================

IMPORTANT: Adding .CanReadMemory() to StringPrepareForGetCodeUnitOp alone
is NOT sufficient because WLE's InsertLoadLike ignores OpEffects entirely
(see section 5.2). The fix must address the WLE caching logic directly.

Option A (targeted fix):
  Remove StringPrepareForGetCodeUnit and StringAsWtf16 from the LoadLike
  cache in WLE, since their results depend on mutable string internals
  (internalization, flattening, external string migration).

Option B (minimal fix):
  Change InsertLoadLike to use mutability=true for SPFGCU and StringAsWtf16
  entries so they are correctly invalidated by InvalidateMaybeAliasing
  during calls:

    // In wasm-load-elimination-reducer.h, InsertLoadLike:
    // Change mutability to true for string operations, or pass it
    // as a parameter instead of hardcoding false.

Option C (structural fix):
  Refactor InsertLoadLike to consult the operation's OpEffects before
  setting the mutability flag. Operations declaring .CanReadMemory()
  should not be cached as immutable. This would also fix the latent
  issue with StringAsWtf16Op (which declares .CanReadMemory() but is
  currently cached as immutable and vulnerable to the same class of bug).

Additionally (defense in depth):
  Add .CanReadMemory() to StringPrepareForGetCodeUnitOp in operations.h
  to match StringAsWtf16Op. This is correct regardless of the WLE fix
  and would protect against similar issues in other optimization passes.

================================================================================
9. AFFECTED CODE
================================================================================

All paths relative to v8/src/compiler/turboshaft/:

  operations.h:8000-8005
    StringPrepareForGetCodeUnitOp - missing .CanReadMemory()

  operations.h:7975-7984
    StringAsWtf16Op - declares .CanReadMemory() but WLE ignores it
    (latent vulnerability: same class of bug, same InsertLoadLike path)

  wasm-load-elimination-reducer.h:273-278
    InsertLoadLike() - hardcodes mutability=false for ALL LoadLike ops

  wasm-load-elimination-reducer.h:197
    InvalidateMaybeAliasing() - skips all immutable entries

  wasm-load-elimination-reducer.h:834-844
    ProcessStringAsWtf16() - caches via InsertLoadLike (also vulnerable)

  wasm-load-elimination-reducer.h:847-858
    ProcessStringPrepareForGetCodeUnit() - caches via InsertLoadLike

Trigger path (v8/src/wasm/):

  turboshaft-graph-interface.cc:2095-2101
    HandleWellKnownImport kStringCharCodeAt - inlines charCodeAt

  turboshaft-graph-interface.cc:5954-6008
    GetCodeUnitImpl() - emits SPFGCU + Immutable() loads


## Attachments

- [wle_stale_ptr_d8.js](attachments/wle_stale_ptr_d8.js) (text/javascript, 14.4 KB)
- [verify_leak.js](attachments/verify_leak.js) (text/javascript, 11.0 KB)

## Timeline

### [Deleted User] (2026-03-18)

deleted

### aj...@chromium.org (2026-05-11)

First report of something that was considered a vulnerability. See [issue 493099941](https://issues.chromium.org/issues/493099941) for discussion.

### sp...@google.com (2026-05-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Baseline. Heavily mitigated (sandboxed) 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-08-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/488306299)*
