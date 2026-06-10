# V8 Sandbox Bypass: controlled OOB write to `Isolate` via RegExp source corruption during tier-up.

| Field | Value |
|-------|-------|
| **Issue ID** | [486084137](https://issues.chromium.org/issues/486084137) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Regexp |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 145.0.7632.46 |
| **Reporter** | ma...@advert.com.au |
| **Assignee** | jg...@chromium.org |
| **Created** | 2026-02-20 |
| **Bounty** | $20,000.00 |

## Description

# Steps to reproduce the problem

Deterministic, 100% reliable on Linux arm64.

```
d8 --sandbox-testing clusterfuzz_regexp_oob_write.js
d8 --sandbox-testing poc_standalone.js
d8 --sandbox-testing poc_per_register.js

```

Both PoCs assume in-cage R/W (simulated via `Sandbox.MemoryView` with `--sandbox-testing`).

1. `new RegExp('a'.repeat(998), 'g')` — 998-char pattern, 0 captures
2. First `exec` with subject `'a'.repeat(998)` — bytecodes compiled, tier-up tick → 0
3. Corrupt source in sandbox heap: each `aa` pair → `()` (499 captures, same byte length)
4. Set `re.lastIndex` to desired value (controls overflow value written to all registers)
5. Second `exec` → tier-up re-parses corrupted source → native code with 1000 registers
6. Native code writes 1000 int32 registers to 128-element `Isolate::jsregexp_static_offsets_vector_` → 3488 bytes OOB on C++ heap outside sandbox

`poc_standalone.js` Phase 1 confirms re-parse: 300-char `'a'` pattern corrupted to `(a)` × 100. After tier-up, `match[0].length` changes from 300 to 100, proving the source was re-parsed.

Phase 2 demonstrates OOB write: 998-char pattern corrupted to `()` × 499 with `lastIndex = 1337`. Sandbox violations at `0x053900000539` confirm the crash address is controlled by `lastIndex`. Compare with `clusterfuzz_regexp_oob_write.js` which uses `lastIndex = 500` and crashes at `0x01f4000001f4`.

`poc_per_register.js` demonstrates per-register value control: corrupts source to `()` × 442 + `(a)` × 38. Non-empty `(a)` groups advance the match position by 1 per group, producing different start/end values per register pair. Crash at `0x271300002712` — upper half (10003) ≠ lower half (10002), proving arbitrary 64-bit pointer construction.

# Problem Description

V8 Sandbox Bypass: controlled OOB write to `Isolate` via RegExp source corruption during tier-up.

RegExp tier-up re-parses the source string from the sandbox heap without re-validating `IrRegExpData::capture_count` (trusted space). An attacker with in-cage R/W can corrupt the source `String` to add capture groups, then trigger tier-up. The native code writes `num_saved_registers_` int32 values into `Isolate::jsregexp_static_offsets_vector_` (128 elements, 512 bytes, C++ heap outside sandbox). The overflow corrupts adjacent Isolate fields including raw pointers and function pointers.

**Root cause:** `IrRegExpData::capture_count` is set once in `IrregexpInitialize()` and never updated during subsequent re-compilations:

- Set only at: <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/heap/factory.cc;l=4353> and <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/heap/factory.cc;l=4391>
- `CompileIrregexpFromSource()` re-parses the corrupted source for tier-up: <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/regexp/regexp.cc;l=665>
- Called from `EnsureCompiledIrregexp`: <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/regexp/regexp.cc;l=598>
- The stale `capture_count` passes CHECK\_EQ: <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/regexp/regexp.cc;l=1064>
- No bounds check on register writes (arm64): <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/regexp/arm64/regexp-macro-assembler-arm64.cc;l=1393>
- Static buffer size (128 elements): <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/execution/isolate.h;l=1517>
- `RegExpData::source` is a `String` on the sandbox heap: <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/js-regexp.tq;l=18>

**Overflow math:** 499 captures → (499+1)×2 = 1000 registers. Static buffer = 128 registers. Overflow = 872 registers × 4 bytes = 3488 bytes past `static_offsets_vector_`. This is 456 bytes past the Boyer-Moore tables into Isolate pointer fields:

- Array macro expansion: <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/execution/isolate.h;l=2730>
- `optimizing_compile_dispatcher_`: <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/execution/isolate.h;l=2747>
- `persistent_handles_list_`: <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/execution/isolate.h;l=2749>

**Value control:** With empty `()` captures, all overflow registers = match position V (controlled via `lastIndex`). Two adjacent int32 values form one 64-bit pointer: `(V << 32) | V`. The two PoCs use different V values to prove control:

- `clusterfuzz_regexp_oob_write.js`: V=500 → crash at `0x01f4000001f4` and `0x01f4000001fc`
- `poc_standalone.js`: V=1337 → crash at `0x053900000539` and `0x053900000541`

**Per-register control:** Non-empty `(a)` captures advance the match position by 1 per group, giving each register pair a different value. `poc_per_register.js` uses `()` × 442 + `(a)` × 38 so the overflow region has incrementing values. Crash at `0x271300002712` — upper half (10003) differs from lower half (10002) by exactly 1. This proves per-register control: by varying capture group lengths, an attacker can construct arbitrary 64-bit pointer values in the overflow region.

**Amplification:** Scales to 10240 captures (80KB overflow) via the `kRegExpTooLargeToOptimize` limit by using `a*` patterns (2 chars per capture instead of 4 for `(a)`).

Controlled write to C++ heap `Isolate` fields outside the V8 sandbox. Chains with <https://issues.chromium.org/issues/485669951> (in-cage R/W) and <https://issues.chromium.org/issues/485669937> (READ escape) to corrupt raw pointers and function pointers in the `Isolate` class.

# Additional Comments

Attached:

- `clusterfuzz_regexp_oob_write.js` — ClusterFuzz PoC (499 captures, 3488 byte overflow)
- `poc_standalone.js` — Detailed PoC with source re-parse confirmation + OOB write
- `poc_per_register.js` — Per-register control: `(a)` groups produce different upper/lower halves

Suggested fix:

1. Re-validate `capture_count` after re-compilation in `CompileIrregexpFromSource()`.
2. Move `IrRegExpData::source` to trusted space so it cannot be corrupted from the sandbox.
3. Add bounds check in native macro assembler before writing registers to `static_offsets_vector_`.

# Summary

V8 Sandbox Bypass: controlled OOB write to `Isolate` via RegExp source corruption during tier-up.

# Custom Questions

#### Type of crash:

tab

#### Crash state:

V8 sandbox violation. Release build, `d8 --sandbox-testing`, arm64.

Both PoCs use different `lastIndex` values to prove the write is fully controlled. Changing `lastIndex` changes the crash address: `(V << 32) | V`.

`clusterfuzz_regexp_oob_write.js` (`lastIndex = 500`, V=0x1F4):

```
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0xfebe00000000,0xffbe00000000)

## V8 sandbox violation detected!

Received signal 11 SEGV_MAPERR 01f4000001f4

## V8 sandbox violation detected!

Received signal 11 SEGV_MAPERR 01f4000001fc

==== C stack trace ===============================

d8(+0x1ba257c)
d8(+0xccb948)
linux-vdso.so.1(__kernel_rt_sigreturn+0x0)
d8(+0x11bb060)
d8(+0x890db8)
d8(+0xdb2918)
d8(+0xdce700)
d8(+0x1ba39fc)
d8(+0x1ba6a90)
d8(+0x1b9fd58)
libc.so.6(+0x82030)
libc.so.6(+0xebf1c)
[end of stack trace]

```

`poc_standalone.js` (`lastIndex = 1337`, V=0x539):

```
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0xfebe00000000,0xffbe00000000)

## V8 sandbox violation detected!

Received signal 11 SEGV_MAPERR 053900000541

==== C stack trace ===============================

d8(+0x1ba257c)
d8(+0xccb948)
linux-vdso.so.1(__kernel_rt_sigreturn+0x0)
d8(+0x6ee83c)
d8(+0x6eff30)
libc.so.6(+0x27744)
libc.so.6(__libc_start_main+0x98)
d8(_start+0x30)
[end of stack trace]

```

`poc_per_register.js` (`lastIndex = 10000`, `(a)` groups — per-register control):

```
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0xfebe00000000,0xffbe00000000)

## V8 sandbox violation detected!

Received signal 11 SEGV_MAPERR 271300002712

==== C stack trace ===============================

d8(+0x1ba257c)
linux-vdso.so.1(__kernel_rt_sigreturn+0x0)
d8(+0xa74ca0)
d8(+0x86258c)
d8(+0x86240c)
d8(+0x86233c)
d8(+0x6e1eac)
d8(+0x6f00c8)
libc.so.6(+0x27744)
libc.so.6(__libc_start_main+0x98)
d8(_start+0x30)
[end of stack trace]

```

Upper half `0x2713` (10003) ≠ lower half `0x2712` (10002). Halves differ by 1, proving per-register value control via capture group structure.

#### Reporter credit:

Mark Blaszczyk

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A \

## Attachments

- [clusterfuzz_regexp_oob_write.js](attachments/clusterfuzz_regexp_oob_write.js) (text/javascript, 1.8 KB)
- [poc_standalone.js](attachments/poc_standalone.js) (text/javascript, 6.1 KB)
- [poc_per_register.js](attachments/poc_per_register.js) (text/javascript, 3.1 KB)
- [poc_controlled_write.js](attachments/poc_controlled_write.js) (text/javascript, 4.4 KB)

## Timeline

### an...@chromium.org (2026-02-20)

[security shepherd] provisionally setting severity and assigning to V8 shepherd.

### ma...@advert.com.au (2026-02-20)

attached is a controlled write Linux/arm64 poc

first at cafe0000cafe (during exec)
second at cafe0000cb06 (during cleanup)

```
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0xfebe00000000,0xffbe00000000)
External strings cage bounds: [0xfeafc0000000,0xfeb400000000)
RegExp tier-up OOB write -> V8 sandbox escape
V8 14.5.201.8 / Chrome 145.0.7632.46

Buffer capacity: 128 registers (512 bytes)
Registers written: 1000 (4000 bytes)
Overflow: 3488 bytes past buffer into C++ heap
Controlled value: V=0xCAFE
Corrupted pointer: 0x0000CAFE0000CAFE

[*] Triggering tier-up re-parse with corrupted source...

## V8 sandbox violation detected!

Received signal 11 SEGV_MAPERR cafe0000cafe
[+] Overflow complete
[+] 3488 bytes written past buffer into Isolate fields
[+] Corrupted pointer at 0x0000CAFE0000CAFE (outside V8 sandbox)

[*] V8 will dereference corrupted pointer during cleanup
[*] Expected: sandbox violation at address 0xcafe0000cafe

## V8 sandbox violation detected!

Received signal 11 SEGV_MAPERR cafe0000cb06

==== C stack trace ===============================

/v8/v8/out/release-sandbox/d8(+0x1ba257c)[0xaaaabbaf257c]
/v8/v8/out/release-sandbox/d8(+0xccb948)[0xaaaabac1b948]
linux-vdso.so.1(__kernel_rt_sigreturn+0x0)[0xffff9d2bc7d0]
/v8/v8/out/release-sandbox/d8(+0x6ee83c)[0xaaaaba63e83c]
/v8/v8/out/release-sandbox/d8(+0x6eff30)[0xaaaaba63ff30]
/lib/aarch64-linux-gnu/libc.so.6(+0x27744)[0xffff9d007744]

==== C stack trace ===============================

/lib/aarch64-linux-gnu/libc.so.6(__libc_start_main+0x98)[0xffff9d007818]
/v8/v8/out/release-sandbox/d8(_start+0x30)[0xaaaaba610030]
[end of stack trace]
/v8/v8/out/release-sandbox/d8(+0x1ba257c)[0xaaaabbaf257c]
/v8/v8/out/release-sandbox/d8(+0xccb948)[0xaaaabac1b948]
linux-vdso.so.1(__kernel_rt_sigreturn+0x0)[0xffff9d2bc7d0]
/v8/v8/out/release-sandbox/d8(+0x11bb060)[0xaaaabb10b060]
/v8/v8/out/release-sandbox/d8(+0x890db8)[0xaaaaba7e0db8]
/v8/v8/out/release-sandbox/d8(+0xdb2918)[0xaaaabad02918]
/v8/v8/out/release-sandbox/d8(+0xdce700)[0xaaaabad1e700]
/v8/v8/out/release-sandbox/d8(+0x1ba39fc)[0xaaaabbaf39fc]
/v8/v8/out/release-sandbox/d8(+0x1ba6a90)[0xaaaabbaf6a90]

```

### ch...@google.com (2026-02-21)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### is...@chromium.org (2026-02-23)

Thank you for the report.

Unfortunately, I can't reproduce the sandbox violation with any of the POCs you provided. Most likely the issue is already fixed on tip of tree.

Please let us know the V8 revision you were using and the GN arguments.

Closing as NotReproducible for now, feel free to reopen once you provide working instructions.

### is...@chromium.org (2026-02-23)

I managed to reproduce the issue with the first two POCs with the following command line `out/x64.debug/d8 --sandbox-testing --noregexp_assemble_from_bytecode poc.js`.

### ma...@advert.com.au (2026-02-23)

hello, 

Docker image: v8-d8:14.5
  - Platform: arm64/aarch64
  - OS: Debian 12 (bookworm)
  - V8: 14.5.201.8 (commit 196c9fce68105531bf6d06e632fb3241d70b6526)
                                                                                                 
 V8 commit: 196c9fce68105531bf6d06e632fb3241d70b6526                                                                                                                                                                                                 
  V8 version: 14.5.201.8                                                                                                                                                                                                                              
  GN args:                                                                                                                                                                                                                                            
    is_debug = false                                                                                                                                                                                                                                  
    v8_enable_sandbox = true                                                                                                                                                                                                                          
    v8_enable_memory_corruption_api = true                                                                               
    v8_enable_sandbox_testing = true

i've also tested x86 however will require some work for recent poc (demonstrating controlled write)
  V8 commit: 96efdf318f993429edee4fb5062eff62b2ed567d
  V8 version: 14.7.62
  GN args:
    is_debug = false
    v8_enable_sandbox = true
    v8_enable_memory_corruption_api = true
    v8_enable_sandbox_testing = true

### jg...@chromium.org (2026-02-23)

The issue needs recompilation via CompileIrregexpFromSource. This used to be the default behavior, but since recently we switched to recompilation from bytecode instead.

There are ways around this, notably <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/regexp/regexp.cc;l=841-843;drc=8b3cdb2cec78482a46337fc2a53db52974a2920a>, so I believe this is still exploitable.

A fix is in flight.

### sa...@google.com (2026-02-23)

Maybe somewhat related: <https://crbug.com/427392572>
We generally try to avoid writing to out-of-sandbox memory from JIT-generated (or otherwise "sandboxed") code, but we currently still allow writing to the Isolate, which is presumably why this issue wasn't caught earlier.

### dx...@google.com (2026-02-23)

Project: v8/v8  

Branch:  main  

Author:  Jakob Linke [jgruber@chromium.org](mailto:jgruber@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7594586>

[regexp] Validate capture\_count during tier-up recompilation

---


Expand for full commit details
```
     
    During RegExp tier-up, `CompileIrregexpFromSource` may re-parse the 
    RegExp source string from the sandbox heap (note this no longer happens 
    in the common case since we recompile from bytecode now). If an attacker 
    with in-sandbox read/write primitives corrupts this source string to add 
    extra capture groups, the newly parsed `capture_count` would differ from 
    the original trusted count. 
     
    This mismatch leads to native code being generated that writes more 
    registers than expected, overflowing the fixed-size 
    `Isolate::jsregexp_static_offsets_vector_` buffer on the C++ heap. 
     
    This CL adds a `SBXCHECK_EQ` to ensure the newly parsed `capture_count` 
    exactly matches the trusted `capture_count` stored in the 
    `IrRegExpData` object, safely aborting if corruption is detected. 
     
    Fixed: 486084137 
    Change-Id: If6a8a2f157e9b2aed4caec5702f03a40db998bf4 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7594586 
    Commit-Queue: Jakob Linke <jgruber@chromium.org> 
    Reviewed-by: Patrick Thier <pthier@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105371}

```

---

Files:

- M `src/regexp/regexp.cc`

---

Hash: [ce4bc856e02c06fd7d7854d2cf625630191d0043](https://chromiumdash.appspot.com/commit/ce4bc856e02c06fd7d7854d2cf625630191d0043)  

Date: Mon Feb 23 11:44:01 2026


---

### ma...@advert.com.au (2026-02-23)

Solid work, anything else you need from my side?

### jg...@chromium.org (2026-02-23)

I think we've got everything we need. Thanks for the report!

### sa...@google.com (2026-02-24)

As the fix seems pretty trivial, we think it would be worth backmerging it as the bug allows breaking out of the V8 Sandbox.

### jg...@chromium.org (2026-02-24)

The fix is in 147.0.7701.0 (<https://chromiumdash.appspot.com/commit/ce4bc856e02c06fd7d7854d2cf625630191d0043>). No good coverage yet though.

### ch...@google.com (2026-02-24)

Merge review required: M146 has already been cut for stable release.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-02-24)

Merge review required: M145 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: andywu (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### dr...@chromium.org (2026-02-25)

No crashes in Canary. Merge approved.

### dx...@google.com (2026-02-26)

Project: v8/v8  

Branch:  refs/branch-heads/14.5  

Author:  Jakob Linke [jgruber@chromium.org](mailto:jgruber@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7611407>

Merged: [regexp] Validate capture\_count during tier-up recompilation

---


Expand for full commit details
```
     
    During RegExp tier-up, `CompileIrregexpFromSource` may re-parse the 
    RegExp source string from the sandbox heap (note this no longer happens 
    in the common case since we recompile from bytecode now). If an attacker 
    with in-sandbox read/write primitives corrupts this source string to add 
    extra capture groups, the newly parsed `capture_count` would differ from 
    the original trusted count. 
     
    This mismatch leads to native code being generated that writes more 
    registers than expected, overflowing the fixed-size 
    `Isolate::jsregexp_static_offsets_vector_` buffer on the C++ heap. 
     
    This CL adds a `SBXCHECK_EQ` to ensure the newly parsed `capture_count` 
    exactly matches the trusted `capture_count` stored in the 
    `IrRegExpData` object, safely aborting if corruption is detected. 
     
    (cherry picked from commit ce4bc856e02c06fd7d7854d2cf625630191d0043) 
     
    Bug: 486084137 
    Change-Id: If6a8a2f157e9b2aed4caec5702f03a40db998bf4 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7611407 
    Commit-Queue: Jakob Linke <jgruber@chromium.org> 
    Reviewed-by: Patrick Thier <pthier@chromium.org> 
    Auto-Submit: Jakob Linke <jgruber@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.5@{#26} 
    Cr-Branched-From: f09d67c66114951c0ea3dc9d4b025461670a9557-refs/heads/14.5.201@{#2} 
    Cr-Branched-From: 3f006438f768659ed9776359a421dc432edce53f-refs/heads/main@{#104623}

```

---

Files:

- M `src/regexp/regexp.cc`

---

Hash: [7fc265d78da9425848de1dc823f15411c6d9aec7](https://chromiumdash.appspot.com/commit/7fc265d78da9425848de1dc823f15411c6d9aec7)  

Date: Mon Feb 23 11:44:01 2026


---

### dx...@google.com (2026-02-26)

Project: v8/v8  

Branch:  refs/branch-heads/14.6  

Author:  Jakob Linke [jgruber@chromium.org](mailto:jgruber@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7611408>

Merged: [regexp] Validate capture\_count during tier-up recompilation

---


Expand for full commit details
```
     
    During RegExp tier-up, `CompileIrregexpFromSource` may re-parse the 
    RegExp source string from the sandbox heap (note this no longer happens 
    in the common case since we recompile from bytecode now). If an attacker 
    with in-sandbox read/write primitives corrupts this source string to add 
    extra capture groups, the newly parsed `capture_count` would differ from 
    the original trusted count. 
     
    This mismatch leads to native code being generated that writes more 
    registers than expected, overflowing the fixed-size 
    `Isolate::jsregexp_static_offsets_vector_` buffer on the C++ heap. 
     
    This CL adds a `SBXCHECK_EQ` to ensure the newly parsed `capture_count` 
    exactly matches the trusted `capture_count` stored in the 
    `IrRegExpData` object, safely aborting if corruption is detected. 
     
    (cherry picked from commit ce4bc856e02c06fd7d7854d2cf625630191d0043) 
     
    Bug: 486084137 
    Change-Id: If6a8a2f157e9b2aed4caec5702f03a40db998bf4 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7611408 
    Reviewed-by: Patrick Thier <pthier@chromium.org> 
    Auto-Submit: Jakob Linke <jgruber@chromium.org> 
    Commit-Queue: Jakob Linke <jgruber@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.6@{#13} 
    Cr-Branched-From: e04c3a1a2543bdbee7beac8846c9cbe8f657636f-refs/heads/14.6.202@{#1} 
    Cr-Branched-From: 3b0b01e6594ec362369dc16f069012a81748c8ba-refs/heads/main@{#105132}

```

---

Files:

- M `src/regexp/regexp.cc`

---

Hash: [8244e41264d6b304c6f93987b91278a25cf2dca7](https://chromiumdash.appspot.com/commit/8244e41264d6b304c6f93987b91278a25cf2dca7)  

Date: Mon Feb 23 11:44:01 2026


---

### sp...@google.com (2026-03-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $20000.00 for this report.

Rationale for this decision:
Controlled write outside the V8 sandbox


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-02)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/486084137)*
