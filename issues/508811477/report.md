# V8 Turboshaft late load elimination reuses stale map load after aliased map transition

| Field | Value |
|-------|-------|
| **Issue ID** | [508811477](https://issues.chromium.org/issues/508811477) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Turboshaft |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | mu...@winfunc.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2026-05-02 |
| **Bounty** | $500.00 |

## Description

Security Bug

VULNERABILITY DETAILS

V8 Turboshaft Late Load Elimination can reuse a stale `LoadMapField` across an aliased map transition. The root cause is in `LateLoadEliminationAnalyzer::ProcessStore()`:

```
v8/src/compiler/turboshaft/late-load-elimination-reducer.cc

// Updates known stored values first.
if (!invalidate_maybe_aliasing) memory_.Invalidate(store);
memory_.Insert(store);

// Clears map facts only after invalidation already used them.
if (store.offset == HeapObject::kMapOffset && !store.index().valid()) {
  WipeAllMaps();
}

```

`memory_.Invalidate(store)` calls `InvalidateAtOffset()`, which uses `object_maps_` through `BasesCouldAlias()` to decide whether a cached load's base can alias the store base. Separately, `ProcessCall()` invalidates memory but does not clear `object_maps_`:

```
// The call could modify arbitrary memory, so we invalidate every
// potentially-aliasing object.
memory_.InvalidateMaybeAliasing();

```

A JavaScript caller can therefore create this sequence in optimized code:

1. `x.x` emits `CheckMaps(x, A)` / `AssumeMap(x, A)`.
2. An opaque callback transitions `x` from map A to map B. `ProcessCall()` wipes cached memory but leaves `object_maps_[x] = A` stale.
3. `y.x` emits `CheckMaps(y, B)` / `AssumeMap(y, B)`.
4. `x == sentinel` lowers to a receiver check that performs a post-call `LoadMapField(x)` without `AssumeMap(x, B)`, caching the B map load while `object_maps_[x]` is still A.
5. `y.z = 99` transitions `y` from B to C. During `ProcessStore()`, `InvalidateAtOffset(kMapOffset, y)` sees `object_maps_[y] = B` and stale `object_maps_[x] = A`, concludes the bases cannot alias, and does not invalidate the cached `LoadMapField(x)`.
6. A later `x.y` `CheckMaps(x, B)` reuses the stale cached map load. The Turboshaft load-elimination verifier confirms that the replacement differs from the actual runtime load when `x === y`.

This bypasses the `WrongMap` deoptimization that should guard optimized code after the map transition. The attached d8 harness deterministically aborts under `--turboshaft-verify-load-elimination` with:

```
abort: Turboshaft's load elimination wrongly eliminated a Load

```

Without the verifier, the same optimized aliased call completes without the `WrongMap` deopt that occurs in safe variants, demonstrating that the stale map check is accepted.

VERSION

Chrome Version: 149.0.7821.0, local V8/Chromium ASan d8 build from Chromium checkout

Operating System: Ubuntu 22.04.5 LTS x86\_64

Build target: `out/asan/d8`

REPRODUCTION CASE

Attachments:

- `poc.html` — Chrome browser PoC for direct local reproduction
- `chrome_parent_lle_browser.log` — direct Chrome run showing browser console milestones, LLE trace, verifier abort, and renderer crash signal
- `poc_d8.js` — deterministic d8 trigger for faster compiler triage
- `lle_verifier_crash.log` — full d8 verifier crash and LateLoadElimination trace
- `lle_noverify.log` — same d8 harness without verifier, showing no `WrongMap` deopt on the aliased call

Browser repro steps:

1. Build local ASan Chrome from the Chromium checkout:

```
gn gen out/asan --args='is_asan=true is_debug=false symbol_level=1 use_sysroot=true treat_warnings_as_errors=false'
autoninja -C out/asan chrome

```

2. Serve the attached `poc.html` locally:

```
python3 -m http.server 8123 --bind 127.0.0.1

```

3. Run Chrome directly against the PoC. The `--js-flags` enable deterministic optimization and the Turboshaft load-elimination verifier; the source tree/binary are otherwise unmodified.

```
ASAN_OPTIONS='detect_leaks=0:abort_on_error=1:symbolize=1' \
  out/asan/chrome \
    --user-data-dir=/tmp/chrome-lle-poc \
    --no-first-run \
    --no-default-browser-check \
    --disable-background-networking \
    --disable-sync \
    --enable-logging=stderr \
    --js-flags='--allow-natives-syntax --turboshaft --no-maglev --turboshaft-load-elimination --turboshaft-verify-load-elimination --turboshaft-trace-load-elimination --trace-deopt' \
    http://127.0.0.1:8123/poc.html

```

Observed browser result:

```
[poc] starting warmup
[poc] optimizing victim on non-aliased call
[poc] non-aliased result: 1142
[poc] triggering aliased call; verifier should abort vulnerable renderer
[poc] target before: {"x":1337}

>>>> InvalidateAtOffset: not invalidating thanks for maps: MemoryAddress{base=0, index=<invalid OpIndex>, offset=0, elem_size_log2=0, size=4}
>> Found potential replacement at offset 72
>>> Confirming replacement
abort: Turboshaft's load elimination wrongly eliminated a Load
Received signal 4 ILL_ILLOPN

```

The attached `chrome_parent_lle_browser.log` contains the complete direct browser run.

D8 repro steps:

1. Build d8 from the Chromium checkout:

```
gn gen out/asan --args='is_asan=true is_debug=false symbol_level=1 use_sysroot=true treat_warnings_as_errors=false'
autoninja -C out/asan d8

```

2. Run the deterministic verifier repro:

```
ASAN_OPTIONS=detect_leaks=0:abort_on_error=1 \
  out/asan/d8 \
    --allow-natives-syntax \
    --turboshaft \
    --no-maglev \
    --turboshaft-load-elimination \
    --turboshaft-trace-load-elimination \
    --turboshaft-verify-load-elimination \
    --trace-deopt \
    poc_d8.js

```

Observed result:

```
>>>> InvalidateAtOffset: not invalidating thanks for maps: MemoryAddress{base=0, index=<invalid OpIndex>, offset=0, elem_size_log2=0, size=4}
>>>> InvalidateAtOffset: invalidating MemoryAddress{base=4, index=<invalid OpIndex>, offset=0, elem_size_log2=0, size=4}
>> Wiping all maps

> ProcessLoad(93)
>> Found potential replacement at offset 72
>>> Confirming replacement
...
[before] {"x":1337}
abort: Turboshaft's load elimination wrongly eliminated a Load

```

3. Optional confirmation without the verifier:

```
out/asan/d8 \
  --allow-natives-syntax \
  --turboshaft \
  --no-maglev \
  --turboshaft-load-elimination \
  --trace-deopt \
  poc_d8.js

```

Observed result:

```
[test] 1142 status=41
[before] {"x":1337}
[attack] 2716 status=41
[after] {"x":1337,"y":42,"z":99}

```

There is no `wrong map` deopt for the aliased `[attack]` call in this run, whereas safe variants deopt at the post-transition access.

Type of crash: Renderer/V8 JIT verifier abort in optimized Turboshaft code.

Crash State:

```
abort: Turboshaft's load elimination wrongly eliminated a Load

==== JS stack trace =========================================

    0: ExitFrame
    1: victim [.../poc_d8.js:~6]
    2: /* anonymous */ [.../poc_d8.js:31]

```

Relevant LLE trace excerpt:

```
ProcessCall(40)
  InvalidateMaybeAliasing
  Invalidating MemoryAddress{base=0, offset=12}
  Invalidating MemoryAddress{base=0, offset=0}

ProcessLoad(59)
ProcessAssumeMap(63)        // y has B
ProcessLoad(72)             // bare post-call LoadMapField(x), no AssumeMap(x,B)

ProcessStore(89)            // y.z map transition B -> C
  InvalidateAtOffset: not invalidating thanks for maps: MemoryAddress{base=0, offset=0}
  InvalidateAtOffset: invalidating MemoryAddress{base=4, offset=0}
  Wiping all maps            // too late

ProcessLoad(93)
  Found potential replacement at offset 72
  Confirming replacement

```

SECURITY IMPACT

The PoC proves that optimized code can accept a stale object map after an aliased map transition and bypass the `WrongMap` deoptimization guard. The attached named-property harness uses a layout where the read remains benign, so the verifier is the deterministic signal. The same stale-CheckMaps primitive applied to elements-kind or layout-specialized accesses can produce type confusion (for example, double-elements code operating after an object-elements transition). The V8 sandbox does not make stale map-specialized optimized code semantically safe; it only constrains follow-on exploitation primitives.

RECOMMENDED FIX

For map-offset stores, clear map facts before any invalidation routine can consult them:

```
const bool is_map_store =
    store.offset == HeapObject::kMapOffset && !store.index().valid();
if (is_map_store) {
  WipeAllMaps();
}
if (!invalidate_maybe_aliasing) memory_.Invalidate(store);
memory_.Insert(store);

```

Also consider clearing map facts across arbitrary effectful calls:

```
WipeAllMaps();
memory_.InvalidateMaybeAliasing();

```

If the call-site precision cost is too high, add a dedicated map-store invalidation mode that never relies on `object_maps_` to preserve active map-offset loads.

CREDIT INFORMATION

Reporter credit: Mufeed VH from Winfunc Research (winfunc.com)

## Attachments

- [poc_d8.js](attachments/poc_d8.js) (text/javascript, 1.1 KB)
- [lle_verifier_crash.log](attachments/lle_verifier_crash.log) (text/plain, 12.1 KB)
- [lle_noverify.log](attachments/lle_noverify.log) (text/plain, 187 B)
- [poc.html](attachments/poc.html) (text/html, 1.8 KB)
- [chrome_parent_lle_browser.log](attachments/chrome_parent_lle_browser.log) (text/plain, 17.6 KB)
- [poc_missing_property_wrong_result.js](attachments/poc_missing_property_wrong_result.js) (text/javascript, 1.1 KB)
- [poc_missing_property.html](attachments/poc_missing_property.html) (text/html, 1.6 KB)
- [chrome_missing_property_noverify.log](attachments/chrome_missing_property_noverify.log) (text/plain, 3.7 KB)
- [chrome_missing_property_verify.log](attachments/chrome_missing_property_verify.log) (text/plain, 17.1 KB)
- [lle_missing_property_noverify.log](attachments/lle_missing_property_noverify.log) (text/plain, 218 B)
- [lle_missing_property_verify.log](attachments/lle_missing_property_verify.log) (text/plain, 12.0 KB)
- [lle_missing_property_interp.log](attachments/lle_missing_property_interp.log) (text/plain, 221 B)

## Timeline

### ch...@google.com (2026-05-05)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-05-05)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### cl...@google.com (2026-05-05)

This analysis is AI-generated using the `v8-security-triaging` skill (Conversation ID: `03ea45e2-446a-4f7b-b70b-da4c68d247b6`).

- **Status:** Reproduced.
- **Classification:** Vulnerability.
- **Rationale:**
  Turboshaft's Late Load Elimination (LLE) reuses a stale `LoadMapField` across an aliased map transition. The root cause is twofold:
  
  1. In `LateLoadEliminationAnalyzer::ProcessStore`, `memory_.Invalidate(store)` is called *before* `WipeAllMaps()`. `Invalidate` relies on `BasesCouldAlias`, which uses the potentially stale map facts in `object_maps_`. Because the maps are not yet wiped, LLE may wrongly conclude that two objects cannot alias and fail to invalidate a cached map load.
  2. `LateLoadEliminationAnalyzer::ProcessCall` invalidates memory but fails to wipe map facts, allowing stale map info to persist across arbitrary effectful calls.
- **Local Reproduction Findings:**
  
  - **Reproduced:** Yes (using `out/x64.debug/d8` and `out/x64.release/d8`).
  - **Build Configuration:** `x64.debug`, `x64.release`.
  - **Verified Impact:** Confirmed that optimized Turboshaft code reuses a stale map and bypasses the `WrongMap` deoptimization guard when an aliased map transition occurs. In a debug build with `--turboshaft-verify-load-elimination`, the engine correctly aborts with `abort: Turboshaft's load elimination wrongly eliminated a Load`.
  - **GDB Backtrace Snippet:**
    ```
    #0  v8::base::OS::Abort()
    #1  v8::internal::__RT_impl_Runtime_Abort
    #2  v8::internal::Runtime_Abort
    #3  Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit
    #4  <optimized Turboshaft code for victim>
    
    ```
- **Security Impact:** S1. Stale map checks in optimized code are a classic source of type confusion (e.g., using layout-specialized code after an elements kind transition), which can be leveraged for memory corruption.
- **Reproduction:**
  `out/x64.debug/d8 --allow-natives-syntax --turboshaft --no-maglev --turboshaft-load-elimination --turboshaft-verify-load-elimination poc_508811477.js`
- **Proposed Owner:** [dmercadier@chromium.org](mailto:dmercadier@chromium.org)

### cl...@appspot.gserviceaccount.com (2026-05-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6481296658300928.

### cl...@appspot.gserviceaccount.com (2026-05-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6495690301669376.

### cl...@chromium.org (2026-05-05)

Still waiting for Clusterfuzz to reproduce.

Darius, do you want to take a look already?

### cl...@chromium.org (2026-05-06)

Clusterfuzz bisected to `c390b66 [turboshaft] Add verification for LateLoadElimination by Darius Mercadier · 11 months ago`

### dm...@chromium.org (2026-05-06)

Thanks for the report, very good find.

I've considered this issue before but concluded that it was safe, because 1) Calls wipe (pretty much) all memory (which then will force reloading the map), and 2) Turbofan should assume that non-stable maps aren't preserved across calls and should insert CheckMaps where needed after calls. However, what I was missing (and what your repro is exploiting) is that we can have a map load after the call that doesn't check a specific map (here it's because it checks that the object is a JSReceiver).

I think that the fix should be to call `WipeAllMaps()` on Calls. If we can reach ProcessStore in a state that 2 objects aliases but have different recorded maps in object\_maps\_, then something wrong already happened.

### dm...@chromium.org (2026-05-06)

It's really unclear whether this is exploitable btw. It can certainly lead to correctness issues, but in order to be exploitable this would need to either OOB field loads, or type confusion around field types, etc. and I don't see how any of these could happen.

Still, I'm really not convinced either that this isn't exploitable, so I'll keep this bug as severity S1 out of caution.

### dm...@chromium.org (2026-05-06)

And impact=extended sounds right: this was probably introduced in <https://crrev.com/c/5522500> (M126).

(the bisect of Commit #8 doesn't point to the real culprit, it only points to the verification pass that enabled the repro to crash because of this issue instead of silently producing a wrong result)

### dx...@google.com (2026-05-06)

[Details redacted due to bug visibility]

Change-Id: I125b35b4192149cfcd92c5f619005bd6fb701b41  

<https://chrome-internal-review.git.corp.google.com/9271320>

### mu...@winfunc.com (2026-05-06)

deleted

### dx...@google.com (2026-05-06)

Project: v8/v8  

Branch:  main  

Author:  Darius Mercadier [dmercadier@chromium.org](mailto:dmercadier@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7823059>

[turboshaft] Load elimination: invalidate known maps on Calls

---


Expand for full commit details
```
     
    Fixed: 508811477 
    Change-Id: I090877c8babd5102319d7b3f5b63fefd5af941a9 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7823059 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Auto-Submit: Darius Mercadier <dmercadier@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#107101}

```

---

Files:

- M `src/compiler/turboshaft/late-load-elimination-reducer.cc`

---

Hash: [df948e6725883d290998e99343a7ef093f781c13](https://chromiumdash.appspot.com/commit/df948e6725883d290998e99343a7ef093f781c13)  

Date: Wed May 6 15:29:39 2026


---

### ch...@google.com (2026-05-06)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### dm...@chromium.org (2026-05-07)

If anyone reads this and is in a position to fix this stupid bot, please do :'(
The CL that fixed this issue is *obviously* the one from [Comment #14](https://issues.chromium.org/issues/508811477#comment14), which marked the bug as Fixed.............

### ch...@google.com (2026-05-07)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### dm...@chromium.org (2026-05-07)

PLEASE STOP IT

### sp...@google.com (2026-05-14)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
Other Processes -	v8 logic


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-20)

Requesting merge to M148 because latest trunk commit is in 150.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to M149 because latest trunk commit is in 150.

### ch...@google.com (2026-05-20)

**M148** merge request created. **Please update [crbug/514925314](https://crbug.com/514925314) to have this merge reviewed.**

### ch...@google.com (2026-05-20)

**M149** merge request created. **Please update [crbug/514929391](https://crbug.com/514929391) to have this merge reviewed.**

### dx...@google.com (2026-05-26)

Project: v8/v8  

Branch:  refs/branch-heads/14.9  

Author:  Darius Mercadier [dmercadier@chromium.org](mailto:dmercadier@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7870081>

[M149] [turboshaft] Load elimination: invalidate known maps on Calls

---


Expand for full commit details
```
     
    Original change's description: 
    > [turboshaft] Load elimination: invalidate known maps on Calls 
    > 
    > Fixed: 508811477 
    > Change-Id: I090877c8babd5102319d7b3f5b63fefd5af941a9 
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7823059 
    > Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    > Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    > Auto-Submit: Darius Mercadier <dmercadier@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#107101} 
     
    (cherry picked from commit df948e6725883d290998e99343a7ef093f781c13) 
     
    Bug: 514929391,508811477 
    Change-Id: I090877c8babd5102319d7b3f5b63fefd5af941a9 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7870081 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Commit-Queue: Darius Mercadier <dmercadier@chromium.org> 
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.9@{#32} 
    Cr-Branched-From: 8f08364a351ad38a60421137a09ef23953ecdd56-refs/heads/14.9.207@{#1} 
    Cr-Branched-From: 8de67b11924d5e8c0032029165a52d800cf05f1f-refs/heads/main@{#106999}

```

---

Files:

- M `src/compiler/turboshaft/late-load-elimination-reducer.cc`

---

Hash: [153cde957906ed22f3169a64422f63e6df7c131d](https://chromiumdash.appspot.com/commit/153cde957906ed22f3169a64422f63e6df7c131d)  

Date: Wed May 6 15:29:39 2026


---

### pe...@google.com (2026-05-26)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dx...@google.com (2026-05-29)

Project: v8/v8  

Branch:  main  

Author:  Michael Lippautz [mlippautz@chromium.org](mailto:mlippautz@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7883043>

[test] Last batch of regression tests

---


Expand for full commit details
```
     
    TAG=AGY 
     
    Bug: 517688821 
     
    Bug: 40061466 
    Bug: 40066473 
    Bug: 342456991 
    Bug: 343507800 
    Bug: 366381662 
    Bug: 368311899 
    Bug: 372269618 
    Bug: 383647255 
    Bug: 392521083 
    Bug: 398999390 
    Bug: 40059920 
    Bug: 40060821 
    Bug: 40064370 
    Bug: 40065138 
    Bug: 40282100 
    Bug: 40892749 
    Bug: 41484971 
    Bug: 420636529 
    Bug: 42203224 
    Bug: 423459708 
    Bug: 450328966 
    Bug: 452296415 
    Bug: 469143679 
    Bug: 476233066 
    Bug: 478659010 
    Bug: 485267831 
    Bug: 508811477 
    Change-Id: I692cb14ebeac04eaa77c867e9377ebd19b4b909b 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7883043 
    Auto-Submit: Michael Lippautz <mlippautz@chromium.org> 
    Commit-Queue: Michael Lippautz <mlippautz@chromium.org> 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#107659}

```

---

Files:

- A `test/mjsunit/compiler/regress-40061466.js`
- A `test/mjsunit/maglev/regress-40066473.js`
- A `test/mjsunit/regress/regress-342456991.js`
- A `test/mjsunit/regress/regress-343507800.js`
- A `test/mjsunit/regress/regress-366381662.js`
- A `test/mjsunit/regress/regress-368311899.js`
- A `test/mjsunit/regress/regress-372269618.js`
- A `test/mjsunit/regress/regress-383647255.js`
- A `test/mjsunit/regress/regress-392521083.js`
- A `test/mjsunit/regress/regress-398999390.js`
- A `test/mjsunit/regress/regress-40059920.js`
- A `test/mjsunit/regress/regress-40060821.js`
- A `test/mjsunit/regress/regress-40064370.js`
- A `test/mjsunit/regress/regress-40065138.js`
- A `test/mjsunit/regress/regress-40282100.js`
- A `test/mjsunit/regress/regress-40892749.js`
- A `test/mjsunit/regress/regress-41484971.js`
- A `test/mjsunit/regress/regress-420636529.js`
- A `test/mjsunit/regress/regress-42203224.js`
- A `test/mjsunit/regress/regress-423459708.js`
- A `test/mjsunit/regress/regress-450328966.js`
- A `test/mjsunit/regress/regress-452296415.js`
- A `test/mjsunit/regress/regress-469143679.js`
- A `test/mjsunit/regress/regress-476233066-1.js`
- A `test/mjsunit/regress/regress-476233066-2.js`
- A `test/mjsunit/regress/regress-478659010.js`
- A `test/mjsunit/regress/regress-485267831.js`
- A `test/mjsunit/regress/regress-508811477.js`

---

Hash: [a5d1a1cc6911f1d1c7f30da136c8f252b05a58dc](https://chromiumdash.appspot.com/commit/a5d1a1cc6911f1d1c7f30da136c8f252b05a58dc)  

Date: Fri May 29 12:59:59 2026


---

### qk...@google.com (2026-07-30)

Add `LTS-NotApplicable-144`, as the patch required additional dependent CLs[1], which in turn necessitated further changes. Consequently, it is not safe to merge all of them back into the M144 LTS.

[1] <https://chromium-review.git.corp.google.com/c/v8/v8/+/7789510>

### ch...@google.com (2026-08-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/508811477)*
