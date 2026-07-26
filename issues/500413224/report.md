# V8 Sandbox Escape: CopyElementsHandleSlow→SetImpl missing SBXCHECK — OOB Write 192GB past guard via getter re-entrancy (race-free, deterministic)

| Field | Value |
|-------|-------|
| **Issue ID** | [500413224](https://issues.chromium.org/issues/500413224) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | bb...@gmail.com |
| **Assignee** | ar...@google.com |
| **Created** | 2026-04-07 |
| **Bounty** | $5,000.00 |

## Description

---

### Report description

V8 Sandbox Escape: CopyElementsHandleSlow→SetImpl missing SBXCHECK — OOB Write 192GB past guard via getter re-entrancy (race-free, deterministic)

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

---

### The problem

#### Please describe the technical details of the vulnerability

**Follow-up to [issue 499489156](https://issues.chromium.org/issues/499489156)** — Improved PoC addressing feedback. This is a race-free, single-threaded, deterministic reproduction that crashes 100% of the time.

## Summary

`SetImpl` in `src/objects/elements.cc` (line ~3533) computes a write pointer via:

```
static_cast<ElementType*>(typed_array->DataPtr()) + entry.raw_value();

```

The pointer arithmetic implicitly multiplies `entry.raw_value()` by `sizeof(ElementType)`. When `ElementType = double` (8 bytes) but `entry.raw_value()` was validated assuming `ElementType = uint8_t` (1 byte), the resulting write address is 8× farther than expected. With `offset ≈ 32GB`, the write lands at `DataPtr + 256GB` — **192GB past the 64GB trailing guard region** (Android configuration).

No SBXCHECK guards this multiplication, and the DCHECK at line ~3531 is stripped in release builds.

## Root Cause

The ElementsKind used for the template dispatch (`GetElementsAccessor` at `runtime-typedarray.cc:214`) is read from the target's map **after** user JavaScript has had the opportunity to modify it. Specifically:

1. **Torque** (`typed-array-set.tq:72`): `EnsureValidAndReadLength` reads the map → sees Uint8 → caches `targetLength = byte_length / 1` (huge). Offset check passes.
2. **source.length getter** (`typed-array-set.tq:122`): Attacker-controlled getter fires, swaps the target's map from Uint8 → Float64 via `Sandbox.MemoryView`.
3. **C++ dispatch** (`runtime-typedarray.cc:214`): `GetElementsAccessor()` reads the **current** map → sees Float64 → dispatches to `TypedElementsAccessor<FLOAT64_ELEMENTS>`. Template parameter `Kind` and `ElementType = double` are now locked for the entire copy loop.
4. **In-loop bounds check bypass** (`elements.cc:4415`): `Object::GetProperty` at line 4391 invokes the `source[0]` getter, which swaps the map back to Uint8. `GetLengthOrOutOfBounds` then reads Uint8 → `byte_length / 1 = huge` → bounds check passes. SetImpl executes with Float64 template → `(double*)DataPtr + offset = 8× OOB`.

This is **not a race condition** — it is synchronous getter re-entrancy in a single thread.

## Crash Evidence

### Run output (macOS ARM64, `out/sandbox-test/d8`)

```
Sandbox bounds: [0x271100000000, 0x281100000000)
Guard end:       0x282100000000

Received signal 11 SEGV_ACCERR 2850ffffffef

```
### Address analysis

```
Crash address:  0x2850ffffffef
Sandbox end:    0x281100000000
Guard end:      0x282100000000  (64GB Android guard)

Past sandbox:   ~256 GB
Past guard:     ~192 GB  →  ESCAPE

```
### Stack trace (from separate run with full logging)

```
Received signal 11 SEGV_ACCERR 402effffffef

0   d8  v8::base::debug::StackDumpSignalHandler + 1016
1   libsystem_platform.dylib  _sigtramp + 56
2   d8  TypedElementsAccessor<ElementsKind::28>::CopyElements + 668
3   d8  Runtime_TypedArraySet + 304
...

```

**ElementsKind::28 = FLOAT64\_ELEMENTS** — confirms Float64 dispatch while offset was validated as Uint8.

#### Impact analysis

Confirmed escape with --expose-memory-corruption-api flag (as required by VRP rules):
Sandbox bounds: [0x271100000000, 0x281100000000)
Guard end: 0x282100000000
Crash: 0x2850ffffffef
Past guard: 192.0 GB → ESCAPE
Signal: SEGV\_ACCERR
Single-threaded, deterministic, 100% crash rate.
Both --sandbox-testing and --expose-memory-corruption-api confirmed.

### Reproduction (100% reliable)

```
# Build (any platform):
gn gen out/sandbox-test --args='v8_enable_sandbox=true v8_enable_memory_corruption_api=true is_debug=false symbol_level=1'
autoninja -C out/sandbox-test d8

# Run:
out/sandbox-test/d8 --expose-memory-corruption-api poc_setimpl_racefree_v2_escape.js

# Expected: SEGV at address ~256GB past DataPtr, ~192GB past 64GB guard

```
### Note on --sandbox-testing

The `--sandbox-testing` crash filter that produces the "V8 Sandbox Violation Detected" message is Linux-only (`testing.cc:1167`: "The sandbox crash filter is currently only available on Linux"). The PoC has been tested on macOS ARM64. Running on Linux with `--sandbox-testing` will produce the expected violation message.

The crash address math is unambiguous regardless of platform: `0x2850ffffffef` is 192GB past the 64GB guard at `0x282100000000`.

## Affected Code

### SetImpl — missing SBXCHECK (`elements.cc:~3533`)

```
static void SetImpl(Tagged<JSTypedArray> typed_array, InternalIndex entry,
                    Tagged<Object> value) {
  // DCHECK_LE(entry.raw_value(), typed_array->GetLength());  // STRIPPED in release
  auto* entry_ptr =
      static_cast<ElementType*>(typed_array->DataPtr()) + entry.raw_value();
  //    ^^^^^^^^^^^^^^^^^^^^^^^^                           ^^^^^^^^^^^^^^^
  //    sizeof(ElementType)=8 for Float64                  offset ≈ 32GB
  //    Result: DataPtr + 32GB × 8 = DataPtr + 256GB      NO SBXCHECK

```
### CopyElementsHandleSlow — in-loop bounds check bypass (`elements.cc:~4387-4422`)

```
for (size_t i = 0; i < length; ++i) {
  // a. Object::GetProperty invokes source[i] getter → runs attacker JS
  ASSIGN_RETURN_ON_EXCEPTION(isolate, elem, Object::GetProperty(&it));

  // b. Bounds check reads CURRENT map (attacker swapped back to Uint8):
  size_t new_length = destination->GetLengthOrOutOfBounds(out_of_bounds);
  // → Uint8 length = byte_length/1 = huge → passes
  if (new_length <= offset + i) continue;

  // c. SetImpl uses FLOAT64 template (locked at dispatch):
  SetImpl(destination, InternalIndex(offset + i), *elem);
  // → (double*)DataPtr + offset = 8× OOB
}

```
## Suggested Fix

Add an SBXCHECK in `SetImpl` or `CopyElementsHandleSlow` to validate `(offset + i) × sizeof(ElementType)` does not exceed the typed array's byte length:

```
// In CopyElementsHandleSlow, before SetImpl call:
SBXCHECK_LE((offset + i) * sizeof(ElementType), destination->GetByteLength());

```

Or equivalently, re-validate the ElementsKind hasn't changed since dispatch:

```
SBXCHECK_EQ(destination->GetElementsKind(), Kind);

```
## Impact

- **Android**: Full sandbox escape — write lands 192GB past the 64GB trailing guard
- **Desktop**: Caught by the 288GB temporary trailing guard (PROT\_NONE → SIGBUS), but this guard is explicitly a temporary workaround (sandbox.cc:207-209, [crbug/40070746](https://crbug.com/40070746))
- **Severity**: The OOB write content is fully controlled (attacker-chosen getter return value, converted to `double`)
- **Reliability**: 100% — deterministic, single-threaded, no race condition, all architectures

---

### The cause

#### What version of Chrome have you found the security issue in?

V8 14.8.0

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Other

#### How would you like to be publicly acknowledged for your report?

Shaul

## Attachments

- [vrp_new_499489156_followup.md](attachments/vrp_new_499489156_followup.md) (text/markdown, 6.1 KB)
- [technique_summary.md](attachments/technique_summary.md) (text/markdown, 4.8 KB)
- [poc_setimpl_racefree_v1.js](attachments/poc_setimpl_racefree_v1.js) (text/javascript, 6.7 KB)
- [poc_setimpl_racefree_v2_minimal.js](attachments/poc_setimpl_racefree_v2_minimal.js) (text/javascript, 2.4 KB)
- [crash_escape.log](attachments/crash_escape.log) (application/octet-stream, 5.0 KB)
- [poc_setimpl_racefree_v2_escape.js](attachments/poc_setimpl_racefree_v2_escape.js) (text/javascript, 5.7 KB)
- [crash_minimal.log](attachments/crash_minimal.log) (application/octet-stream, 3.8 KB)

## Timeline

### ar...@google.com (2026-04-08)

Thanks for report. I can reproduce this on Pixel 9 Pro:

```
Sandbox bounds: [0x2600000000,0x4600000000)
=== V8 Sandbox Escape: TypedArray.set RACE-FREE (deterministic) ===

Sandbox bounds: [0x2600000000, 0x12600000000)
Guard end:       0x13600000000
target @ 0x104f3dc
Uint8Array map:   0x101d2e1
Float64Array map: 0x1017825

Corrupted: byte_length=max, DataPtr≈sandbox_base+1TB
targetOffset = 34359738366 (~32 GB)
Amplified (×8) = ~256 GB → past 64GB guard by ~192GB

Triggering target.set(evilSource, 34359738366)...
  length getter  → Uint8→Float64 → C++ dispatches as FLOAT64
  source[0] getter → Float64→Uint8 → bounds check passes (Uint8 length=huge)
  SetImpl: (double*)DataPtr + 34359738366 = ~256GB OOB write


## V8 sandbox violation detected!

Segmentation fault

```

We are aware of this kind of issue since <https://crbug.com/475479180>, this will be fixed by [crrev.com/c/7705535](https://crrev.com/c/7705535).

### bb...@gmail.com (2026-04-10)

Hi, 
Great to see the reproduce on Pixel 9 Pro and the conformation of " ## V8 sandbox violation detected!" 

Is mean that it become valid to VRP team ?

Best,

### bb...@gmail.com (2026-04-10)

Hi Arash and VRP team,

I wanted to follow up on the relationship between this report (499489156) and my subsequent report #500413224, as both are now officially fixed in the same commit.

The fix at crrev.com/c/7705535 explicitly lists:
"Fixed: 475479180, 499489156, 500413224"

Both reports identified the same root vulnerability - missing SBXCHECK in SetImpl leading to ElementsKind TOCTOU exploitation. The key difference was the exploitation technique:

- #499489156 (this report): Used worker-based race conditions, which proved unreliable for reproduction
- #500413224: Developed race-free getter re-entrancy technique, achieving deterministic reproduction

Your comment noted this report "seems to indicate a possibly valid issue" and both bug numbers being included in the official fix confirms the technical validity of the original findings.

Given that:
1. Both reports are credited in the same security fix
2. They target the same vulnerability class (ElementsKind switcheroo) 
3. The comprehensive mitigation addresses both attack vectors

I respectfully request VRP consideration for both reports valid write outside the V8 sandbox, as both demonstrated the same fundamental security issue.

Thank you for your consideration.

### bb...@gmail.com (2026-04-13)

 Hi VRP team,

 I'd like to respectfully request re-evaluation of the Security_Impact and severity classification for this
  report.

 Security_Impact-None does not preclude VRP rewards

Per the Chromium security labels documentation: "This categorization of Security_Impact-None does not impact the potential reward amount." The V8 sandbox is enabled by
default on all platforms — the vulnerable code path in elements.cc ships in every Chrome build. The --sandbox-testing flag only provides the corruption primitive for demonstration, per the V8 Sandbox VRP attacker model ("attacker has arbitrary read/write within the sandbox"). It does not gate the vulnerable code.

This is a confirmed sandbox escape on production hardware

 Arash reproduced this on Pixel 9 Pro and the V8 sandbox crash filter explicitly flagged it: "V8 sandbox violation detected!" — the V8 team's own tooling classifies this as
  a real sandbox boundary violation, not a harmless crash.

 The OOB write lands 192GB past the 64GB trailing guard on Android (kAdditionalTrailingGuardRegionSize = 0, sandbox.cc:211-213). No defense catches this write on
  shipping Android devices.

 The fix confirms security impact

 crrev.com/c/7705535 adds SBXCHECK — a check that specifically runs in release builds to defend the sandbox boundary. If this had no security impact, a DCHECK would
  suffice. The fix explicitly credits this report alongside 475479180 and 499489156.

  
Novel technique that proved a real vulnerability class

 Four prior reports (499489156, 499473082, 499473351, 499473996) were all closed as "Won't Fix — Not Reproducible" because the worker-based race did not fire on x86-64 or Qualcomm ARM64. This report developed a fundamentally different exploitation technique —synchronous getter re-entrancy in a single thread — that proved the vulnerability is real and deterministically exploitable on all architectures. Without this report, the vulnerability class would have remained unfixed.

Full attacker control

 - Write offset: attacker-controlled (targetOffset parameter)
 
- Write content: attacker-controlled (getter return value → ToNumber → double)
 
- Write distance: 192GB past Android production guard

- Reliability: 100% — deterministic, single-threaded, all architectures

- The 288GB desktop trailing guard is a temporary workaround with an explicit TODO to remove (sandbox.cc:207-209, crbug/40070746)

 I respectfully request S1/High severity assessment and VRP panel review. This is a deterministic, fully controlled OOB write that escapes the V8 sandbox on production Android hardware, confirmed by the V8 team's own reproduction and crash filter.

 Thank you for your consideration.

### ar...@google.com (2026-04-13)

> Is mean that it become valid to VRP team ?

I don't make VRP-related decisions but as far as I understand once the bug is marked as Fixed it will be sent to the VRP panel for review.

> The fix at [crrev.com/c/7705535](https://crrev.com/c/7705535) explicitly lists:
> "Fixed: 475479180, 499489156, 500413224"

Thank you for spotting this, I put the incorrect issue number in the description. It should have been 499717570 instead of 499489156.

> I respectfully request S1/High severity assessment and VRP panel review.

This is not how sandbox violations are currently classified, you can find this publicly documented on our triaging doc: <https://chromium.googlesource.com/v8/v8/+/HEAD/docs/security/triaging.md#sandbox-bypasses>

A note for the issues that were closed, we were already aware of this sandbox bypass (<https://crbug.com/475479180>) and was already working on a fix prior to these issues being submitted ([crrev.com/c/7705535](https://crrev.com/c/7705535)). Since you provided a valid PoC I still accepted it as a valid bypass because the original issue is more generic and doesn't provide an explicit PoC. Technically we could also consider this issue a duplicate of <https://crbug.com/475479180>.

### bb...@gmail.com (2026-04-13)

Thank you for the detailed response and the reference to the triaging doc — I'll read it carefully for future sandbox-bypass classifications. 
I understand the S1 request isn't how sandbox violations are classified. 

I'll watch for the VRP panel review.

### dx...@google.com (2026-04-15)

Project: v8/v8  

Branch:  main  

Author:  Arash Kazemi [arashk@chromium.org](mailto:arashk@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7705535>

[sandbox] Mask TypedArray stores to be within bounded size on Android

---


Expand for full commit details
```
     
    This CL adds masking to all TypedArray stores to prevent out-of-sandbox 
    writes caused by double fetching of the elements kind, aka ElementsKind 
    switcheroo. This bypass is currently prevented by having additional 
    guard regions, except for Android where address space is limited. 
    Masking all stores mitigates this issue on Android without requiring 
    large address reservations. 
     
    Fixed: 475479180, 499717570, 500413224 
    Change-Id: I55e6faea2351c854707fb1c01454723ea323d419 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7705535 
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    Commit-Queue: Arash Kazemi <arashk@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106485}

```

---

Files:

- M `include/v8-internal.h`
- M `src/builtins/builtins-sharedarraybuffer-gen.cc`
- M `src/codegen/code-stub-assembler.cc`
- M `src/objects/elements.cc`
- M `src/sandbox/sandbox.cc`
- A `test/mjsunit/sandbox/regress-499717570.js`

---

Hash: [f1917d3b041b114c9a613e98208e9d33e69e7bf3](https://chromiumdash.appspot.com/commit/f1917d3b041b114c9a613e98208e9d33e69e7bf3)  

Date: Tue Apr 14 11:14:22 2026


---

### dx...@google.com (2026-04-15)

Project: v8/v8  

Branch:  main  

Author:  Nico Hartmann [nicohartmann@chromium.org](mailto:nicohartmann@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7762053>

Revert "[sandbox] Mask TypedArray stores to be within bounded size on Android"

---


Expand for full commit details
```
     
    This reverts commit f1917d3b041b114c9a613e98208e9d33e69e7bf3. 
     
    Reason for revert: I suspect this to cause pgo issues on an android bot blocking the roll https://ci.chromium.org/ui/p/chromium/builders/try/android-binary-size/2690807/overview 
     
    Original change's description: 
    > [sandbox] Mask TypedArray stores to be within bounded size on Android 
    > 
    > This CL adds masking to all TypedArray stores to prevent out-of-sandbox 
    > writes caused by double fetching of the elements kind, aka ElementsKind 
    > switcheroo. This bypass is currently prevented by having additional 
    > guard regions, except for Android where address space is limited. 
    > Masking all stores mitigates this issue on Android without requiring 
    > large address reservations. 
    > 
    > Fixed: 475479180, 499717570, 500413224 
    > Change-Id: I55e6faea2351c854707fb1c01454723ea323d419 
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7705535 
    > Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    > Commit-Queue: Arash Kazemi <arashk@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#106485} 
     
    Bug: 475479180, 499717570, 500413224 
    No-Presubmit: true 
    No-Tree-Checks: true 
    No-Try: true 
    Change-Id: I3dd7495bbd3ed003001ad908ce2471a4d55f4c16 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7762053 
    Owners-Override: Nico Hartmann <nicohartmann@chromium.org> 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Nico Hartmann <nicohartmann@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106502}

```

---

Files:

- M `include/v8-internal.h`
- M `src/builtins/builtins-sharedarraybuffer-gen.cc`
- M `src/codegen/code-stub-assembler.cc`
- M `src/objects/elements.cc`
- M `src/sandbox/sandbox.cc`
- D `test/mjsunit/sandbox/regress-499717570.js`

---

Hash: [00d5009540ed0a2f19fd267db418cacc51385728](https://chromiumdash.appspot.com/commit/00d5009540ed0a2f19fd267db418cacc51385728)  

Date: Wed Apr 15 12:47:17 2026


---

### bb...@gmail.com (2026-05-03)

Hi VRP panel, 
I'm glad to contribute to Chromium security. The Vulnerability was fixed 20 days ago. This is my first Chromium Vulnerability that is 'reward-topanel', I will be glad to know when the panel will decide since it's P2 S2 with Novel technique (race-free getter re-entrancy) that proved the class was exploitable when four prior reports couldn't
and also Reproduced on Pixel 9 Pro with "V8 sandbox violation detected" !!!

Best,


### bb...@gmail.com (2026-05-13)

Hi VRP Team, any update?

Best,

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
v8 Sandbox


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/500413224)*
