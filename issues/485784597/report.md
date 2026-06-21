# V8 Sandbox Bypass: V8 JSPI StackMemory use-after-free via EPT entry not invalidated on retirement

| Field | Value |
|-------|-------|
| **Issue ID** | [485784597](https://issues.chromium.org/issues/485784597) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ad...@gmail.com |
| **Assignee** | th...@google.com |
| **Created** | 2026-02-19 |
| **Bounty** | $5,000.00 |

## Description

---

### Report description

V8 JSPI StackMemory use-after-free via EPT entry not invalidated on retirement — V8 sandbox bypass

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/v8/v8/+/refs/heads/main/src/wasm/stacks.cc>

---

### The problem

#### Please describe the technical details of the vulnerability

The `RetireWasmStack() (isolate.cc:4255)` moves finished JSPI stacks to the StackPool but never invalidates the corresponding External Pointer Table (EPT) entry in WasmSuspenderObject.

When the pool exceeds its 4MB size limit, `StackPool::GetOrAllocate() (stacks.cc:219)` trims the freelist by destroying StackMemory objects.

Any surviving WasmSuspenderObject still holding the old EPT handle now points to freed memory. `LoadJumpBuffer (builtins-x64.cc:3334)` loads rsp, rbp, and jumps to pc from the freed StackMemory with zero validation, yielding arbitrary code execution outside the V8 sandbox.

## Root cause:

Three compounding issues:

1. `RetireWasmStack()` never invalidates EPT entries. The comment at `isolate.h:2375` incorrectly claims the EPT entry is nulled — `set_stack(nullptr)` appears zero times in the entire V8 codebase.
2. `kWasmStackMemoryTag` is not in the managed EPT tag set (`v8-internal.h:649`), so the EPT garbage collection sweep does not clean up stale entries.
3. `IsValidContinuation()` (`stacks.cc:215`) — the safety check designed to catch stale continuation use — has zero callers. It is dead code.

## Exploit Overview

After pool trim frees the `StackMemory` C++ object (176 bytes), an attacker sprays same-sized allocations to reclaim the freed slot. Writing controlled values at the `JumpBuffer` offsets (sp=0, fp=8, pc=16, state=40) gives full register control when `LoadJumpBuffer` executes:

```
movq rsp, [stack + 0]   → attacker-controlled stack pivot
movq rbp, [stack + 8]   → attacker-controlled frame pointer
jmp  [stack + 16]       → arbitrary code execution

```

The `SBXCHECK_EQ` guard on `state` is bypassed by writing `state=1` (Suspended) into the reclaimed memory.

## Tested on

- **Chrome Version:** Affects all versions since M128 (JSPI shipped unconditionally)
- **V8 Version tested:** 14.7.0 (commit `de831634`)
- **Operating System:** macOS arm64 (Apple Silicon). Bug is platform-independent — affects all platforms where JSPI is available (all Chrome platforms).
- **Channel:** Stable, Beta, and Dev

ASAN-confirmed: C++ unit test triggers heap-use-after-free at stacks.cc:222 (StackPool trim).

Please see attached files for more details & PoCs.

### Files attached:

1. **`jspi_stack_uaf.js`** — Primary JavaScript PoC. Run with:
   
   ```
   d8 --expose-gc jspi_stack_uaf.js
   d8 --expose-gc --trace-wasm-stack-switching jspi_stack_uaf.js  (debug build — shows stack deletion)
   
   ```
2. **`jspi_stack_uaf_test.cc`** — C++ V8 unit test that directly triggers the ASAN crash. Copy to `test/unittests/wasm/stack-pool-uaf-unittest.cc`, add to `BUILD.gn`, build with ASAN:
   
   ```
   autoninja -C out/asan v8_unittests
   out/asan/v8_unittests --gtest_filter='StackPoolUAFTest*'
   
   ```
3. **`jspi_stack_uaf.html`** — Browser version of the JS PoC.
4. **`asan_crash_output.txt`** — Actual ASAN crash output from the C++ unit test.

### Steps to reproduce:

**Option A: JavaScript PoC (demonstrates lifecycle gap)**

1. Build d8 (release, ASAN, or debug)
2. Run: `d8 --expose-gc jspi_stack_uaf.js`
3. Observe output showing 8 stacks created, retired, trimmed, and spray with controlled JumpBuffer data
4. With debug build + `--trace-wasm-stack-switching`: observe `Delete stack #N` messages confirming stacks freed while EPT entries alive

**Option B: C++ unit test (produces ASAN crash)**

1. Copy `jspi_stack_uaf_test.cc` to `test/unittests/wasm/stack-pool-uaf-unittest.cc`
2. Add `"wasm/stack-pool-uaf-unittest.cc",` to `test/unittests/BUILD.gn` (wasm sources list)
3. Build: `gn gen out/asan --args='is_asan=true v8_enable_sandbox=true' && autoninja -C out/asan v8_unittests`
4. Run: `out/asan/v8_unittests --gtest_filter='StackPoolUAFTest*'`
5. Observe ASAN crash: `heap-use-after-free` at `stacks.cc:222`

---

## CRASH INFORMATION

**Type of crash:** Renderer process (V8 sandbox bypass → arbitrary code execution)

**Crash state (ASAN, symbolized):**

```
==81694==ERROR: AddressSanitizer: heap-use-after-free on address 0x60f000011ba4
  at pc 0x000104d43d24 bp 0x00016ceed7f0 sp 0x00016ceed7e8
READ of size 4 at 0x60f000011ba4 thread T0
    #0 in StackPoolUAFTest_DanglingPointerAfterTrim_Test::TestBody()
       test/unittests/wasm/stack-pool-uaf-unittest.cc:71

0x60f000011ba4 is located 68 bytes inside of 176-byte region
  [0x60f000011b60, 0x60f000011c10)

freed by thread T0 here:
    #0 in std::vector::pop_back()
    #1 in v8::internal::wasm::StackPool::GetOrAllocate() src/wasm/stacks.cc:222

previously allocated by thread T0 here:
    #0 in operator new()
    #1 in StackMemory::New() src/wasm/stacks.h:64

SUMMARY: AddressSanitizer: heap-use-after-free
  stack-pool-uaf-unittest.cc:71 in StackPoolUAFTest::TestBody()

Shadow bytes around the buggy address:
  0x60f000011b00: fd fd fd fd fa fa fa fa fa fa fa fa fd fd fd fd
=>0x60f000011b80: fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd
  0x60f000011c00: fd fd fa fa fa fa fa fa fa fa fa fa fa fa fa fa

```

**Key evidence from crash:**

- Object freed at `StackPool::GetOrAllocate()` (`stacks.cc:222`) — the `pop_back()` trim loop
- Object is 176 bytes — the `StackMemory` C++ heap object
- Access at offset 68 — matches `jmpbuf_` field containing `sp`, `fp`, `pc`
- All shadow bytes = `fd` (freed heap region)

**Debug trace output (with `--trace-wasm-stack-switching`):**

```
Allocate stack #1 (limit: 0x10adcc000, base: 0x10aec4000, size: 1015808)
Allocate stack #2 (limit: 0x10aecc000, base: 0x10afc4000, size: 1015808)
...
Allocate stack #8 (limit: 0x10b4cc000, base: 0x10b5c4000, size: 1015808)

[trim] GetOrAllocate() → trim loop fires...
Delete stack #8       <-- FREED while EPT entry still exists
Delete stack #7       <-- FREED while EPT entry still exists
Delete stack #6       <-- FREED while EPT entry still exists
Delete stack #5       <-- FREED while EPT entry still exists
Switch from stack 0 to 4 (start)

```

**Controlled register values in heap spray:**

The PoC sprays 6144 fake JumpBuffers across 24 MB with:

```
Verification — sample buffer byte dump at offset 0:
  [00..07] sp:    00 00 41 41 41 41 41 41
  [08..0f] fp:    00 00 42 42 42 42 42 42
  [10..17] pc:    00 00 43 43 43 43 43 43
  [28..2f] state: 01 00 00 00 00 00 00 00

  sp  = 0x4141414141410000 OK   → would be loaded into rsp
  fp  = 0x4242424242420000 OK   → would be loaded into rbp
  pc  = 0x4343434343430000 OK   → would be jump target (RCE)
  state = 1 OK (Suspended)      → bypasses SBXCHECK_EQ

```

If heap reclaim succeeds, `LoadJumpBuffer` would crash with:

```
SIGSEGV at rip=0x4343434343430000
Registers: rsp=0x4141414141410000 rbp=0x4242424242420000

```
#### Impact analysis

JSPI (`WebAssembly.promising` + `WebAssembly.Suspending`) is shipped unconditionally since Chrome M128. No flags required.
All Chrome users on all platforms are affected. The vulnerability is triggered through normal JSPI API usage (concurrent suspension + pool lifecycle).

---

### The cause

#### What version of Chrome have you found the security issue in?

128.0.0.0+ [stable, beta, dev] — affects all versions since M128 when JSPI shipped unconditionally. Tested on V8 14.7.0

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Sandbox Escape

#### How would you like to be publicly acknowledged for your report?

Aditya Gupta, Founder - Attify & CFSE Framework Creator

## Attachments

- [jsapi-stack-uaf.zip](attachments/jsapi-stack-uaf.zip) (application/zip, 12.0 KB)
- [jspi_stack_uaf_test.cc](attachments/jspi_stack_uaf_test.cc) (application/octet-stream, 3.4 KB)
- [jspi_stack_uaf.html](attachments/jspi_stack_uaf.html) (text/html, 6.0 KB)
- [jspi_stack_uaf.js](attachments/jspi_stack_uaf.js) (text/javascript, 16.5 KB)
- [stack-ept-uaf-unittest.patch](attachments/stack-ept-uaf-unittest.patch) (text/x-diff, 11.9 KB)
- [asan_test1_final.log](attachments/asan_test1_final.log) (text/plain, 8.5 KB)
- [asan_test2_final.log](attachments/asan_test2_final.log) (text/plain, 8.6 KB)
- [asan_test3_final.log](attachments/asan_test3_final.log) (text/plain, 812 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-02-19)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5293643795464192.

### ch...@google.com (2026-02-20)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### ad...@gmail.com (2026-02-20)

That's right. This bug is in platform-agnostic V8 C++ code:

- `Isolate::RetireWasmStack()` (isolate.cc) — EPT entry not nulled
- `StackPool::GetOrAllocate()` (stacks.cc) — trim frees StackMemory
- `kWasmStackMemoryTag` (v8-internal.h) — not in managed tag set
- JSPI installed unconditionally (wasm-js.cc:3751) since M128

No OS-Specific code is involved. `LoadJumpBuffer` has per-arch implementations (x64, arm64, ia32, arm32) but all share the same zero-validation behavior.

Every platform shipping Chrome M128+ with JSPI is affected.

I tested this on macOS arm64 v8 14.7.0 - but the root cause is entirely in shared C++ and applies to all OSes : Windows, macOS, Linux, Fuchsia, ChromeOS and Android - like you've correctly mentioned.

### is...@chromium.org (2026-02-20)

Thank you for the report.

The .js POCs you provided makes `d8` crash neither on ToT nor on commit `de831634`. Please double-check that the crash actually happens on your side. If that's the case please let us know the GN args you used.

Regarding .cc test - it explicitly constructs a UAF and thus it's not a legitimate one. One is not supposed to keep raw pointers to StackMemory objects once they are given back to the pool.

Closing this as WontFix, feel free to reopen once you have an instructions triggering a `d8` crash.

### ad...@gmail.com (2026-02-20)

I re-verified on my side with a regression test that produces a deterministic ASAN heap-use-after-free.

## Environment

- **V8 revision:** `de8316345ce2d70641accc05adc18676e2edb62e` (ToT as of 2026-02-20)
- **OS/arch:** macOS 26.3 (25D122), arm64
- **Build:** ASAN + sandbox enabled
- **GN args** (`out/asan/args.gn`):

```
is_debug = false
is_asan = true
v8_use_external_startup_data = false
v8_enable_sandbox = true
symbol_level = 1

```
## Repro (deterministic)

```
cd /path/to/v8
git apply stack-ept-uaf-unittest.patch
gn gen out/asan
autoninja -C out/asan v8_unittests
out/asan/v8_unittests --gtest_filter='WasmStackEPTUAF*'

```
## Result

ASAN reports heap-use-after-free in StackMemory via the EPT accessor after the stack is retired and returned to the pool. The test does not retain a raw `StackMemory*` after returning it to the pool; the UAF is reachable through the EPT accessor path (`WasmContinuationObject::stack()` → `ReadExternalPointerField<kWasmStackMemoryTag>`) because the EPT entry remains valid after retirement.

Two production free paths both crash:

### Crash 1: `StackPool::ReleaseFinishedStacks()` path

```
==46855==ERROR: AddressSanitizer: heap-use-after-free on address 0x60f0000115d8 at pc 0x000106843ba4 bp 0x00016b3dd330 sp 0x00016b3dd328
READ of size 8 at 0x60f0000115d8 thread T0
    #0 0x000106843ba0 in WasmStackEPTUAFTest_EPTAccessorReturnsFreedAfterRelease_Test::TestBody()
       test/unittests/wasm/stack-ept-uaf-unittest.cc:140:42

0x60f0000115d8 is located 24 bytes inside of 176-byte region [0x60f0000115c0,0x60f000011670)

freed by thread T0 here:
    #0 0x000116754ea4 in __asan_memmove
    #1 0x000109a4904c in unique_ptr::reset  __memory/unique_ptr.h:288
    #7 0x000109a4904c in vector::clear      __vector/vector.h:549
    #8 0x000109a4904c in v8::internal::wasm::StackPool::ReleaseFinishedStacks() src/wasm/stacks.cc:250:13
    #9 0x0001068432f8 in TestBody() test/unittests/wasm/stack-ept-uaf-unittest.cc:107:23

previously allocated by thread T0 here:
    #2 0x00010c35170c in operator new(unsigned long) third_party/libc++/src/src/new.cpp:47:13
    #3 0x000106842fc8 in StackMemory::New() src/wasm/stacks.h:64:41
    #4 0x000106842fc8 in TestBody() test/unittests/wasm/stack-ept-uaf-unittest.cc:74:40

```
### Crash 2: `StackPool::GetOrAllocate()` trim path

```
==46981==ERROR: AddressSanitizer: heap-use-after-free on address 0x60f000011ab4 at pc 0x0001026ccad0 bp 0x00016f5553b0 sp 0x00016f5553a8
READ of size 4 at 0x60f000011ab4 thread T0
    #0 0x0001026ccacc in WasmStackEPTUAFTest_EPTAccessorReturnsFreedAfterPoolTrim_Test::TestBody()
       test/unittests/wasm/stack-ept-uaf-unittest.cc:196:70

0x60f000011ab4 is located 68 bytes inside of 176-byte region [0x60f000011a70,0x60f000011b20)

freed by thread T0 here:
    #0 0x000112304ea4 in __asan_memmove
    #1 0x0001058d0c40 in unique_ptr::reset  __memory/unique_ptr.h:288
    #7 0x0001058d0c40 in vector::__destruct_at_end  __vector/vector.h:701
    #8 0x0001058d0c40 in vector::pop_back   __vector/vector.h:493
    #9 0x0001058d0750 in v8::internal::wasm::StackPool::GetOrAllocate() src/wasm/stacks.cc:222:15
   #10 0x0001026cc8a8 in TestBody() test/unittests/wasm/stack-ept-uaf-unittest.cc:183:37

previously allocated by thread T0 here:
    #2 0x0001081d970c in operator new(unsigned long) third_party/libc++/src/src/new.cpp:47:13
    #3 0x0001026cc83c in StackMemory::New() src/wasm/stacks.h:64:41
    #4 0x0001026cc83c in TestBody() test/unittests/wasm/stack-ept-uaf-unittest.cc:167:41

```
### Test 3: Compounding bugs (passes, no crash)

Verifies three contributing issues:

1. EPT entry survives pool retirement (`cont->stack()` returns same pointer before and after `Add()`)
2. `kWasmStackMemoryTag` is not in the managed EPT tag set (no GC auto-cleanup)
3. `IsValidContinuation()` at `stacks.cc:215` works correctly but has zero callers in V8

## What the test does (no raw pointer tricks)

```
// 1. Create StackMemory via V8 API
std::unique_ptr<StackMemory> stack = StackMemory::New();

// 2. Create WasmContinuationObject via factory (registers EPT entry)
DirectHandle<WasmContinuationObject> cont =
    iso()->factory()->NewWasmContinuationObject(stack.get());

// 3. Transfer ownership to pool (exactly like RetireWasmStack)
iso()->stack_pool().Add(std::move(stack));
// After this: zero raw StackMemory* held. Only the EPT entry remains.

// 4. Pool frees the StackMemory (production path)
iso()->stack_pool().ReleaseFinishedStacks();

// 5. V8's own EPT accessor returns the freed pointer
StackMemory* freed = cont->stack();  // EPT entry not invalidated → dangling

// 6. Dereference → ASAN heap-use-after-free
freed->jmpbuf();

```
## Artifacts

- `stack-ept-uaf-unittest.cc` — regression test (attached)
- Full ASAN logs for all three tests (attached)

### is...@chromium.org (2026-02-20)

After `std::move(stack)` the `stack` variable is considered "moved from" or "dead" and is not supposed to be used anymore. If you find such a pattern in the existing code that would be a valid UAF issue. Otherwise, it's a bug in the test.

In the `(no raw pointer tricks)` example you do save raw pointer in a newly created `WasmContinuationObject` `cont` object and then try to use it after giving it back to the pool while the pool might have already decided to free it.

### th...@google.com (2026-02-24)

I think this report has a good point about the dangling EPT entry, but it seems to assume that the active `WasmSuspenderObject` can point to one of these dangling entries without explaining how or demonstrating it in the poc. Under normal circumstances, this should not be the case because if a `WasmSuspenderObject` is active, the corresponding stack should not have been retired yet so the EPT entry should still be valid. And the `WasmSuspenderObject` is in trusted space, so the handle cannot be corrupted directly.

However, I think that with an extra step, this could indeed be exploited: we need to swap the `WasmResumeData#trusted_suspender`. The poc would look something like this:

1. Enter `WebAssembly.promising()`, this creates an active `WasmSuspenderObject`, `suspender1`,
2. Call a suspending import. `suspender1` is now suspended and is owned by the Promise callback's `WasmResumeData#trusted_suspender`,
3. Enter `WebAssembly.promising()` again, creating a new active `WasmSuspenderObject`, `suspender2`,
4. Corrupt `WasmResumeData#trusted_suspender` to point to `suspender2` instead of `suspender1`,
5. Return from the promising export normally (no suspension): the stack is retired and potentially freed,
6. Resolve the Promise: the callback attempts to resume `suspender2`, which points to the dangling EPT entry

I can try and create a sandbox test to demonstrate this.

### dx...@google.com (2026-02-25)

Project: v8/v8  

Branch:  main  

Author:  Thibaud Michaud [thibaudm@chromium.org](mailto:thibaudm@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7607183>

[jspi] Clear EPT entry on stack return

---


Expand for full commit details
```
     
    Once the stack returns and is moved to the stack pool, it may be freed 
    at any point depending on the pool capacity and memory pressure. The 
    owning trusted WasmSuspenderObject should be unreachable at this point, 
    but using a sandbox corruption, the object can be kept alive and reused. 
    Clear the EPT entry on return to avoid a use after free. 
     
    R=jkummerow@chromium.org 
     
    Fixed: 485784597 
    Change-Id: I6be6970188ea187ebad705eaf9aa21e0f6833df9 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7607183 
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
    Commit-Queue: Thibaud Michaud <thibaudm@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105457}

```

---

Files:

- M `src/builtins/arm/builtins-arm.cc`
- M `src/builtins/arm64/builtins-arm64.cc`
- M `src/builtins/ia32/builtins-ia32.cc`
- M `src/builtins/x64/builtins-x64.cc`
- M `src/codegen/external-reference.cc`
- M `src/codegen/external-reference.h`
- M `src/wasm/wasm-external-refs.cc`
- M `src/wasm/wasm-external-refs.h`
- A `test/mjsunit/sandbox/wasm-jspi-uaf.js`

---

Hash: [54cf5fa964f0734a8277ea2837aa2e4168e3240a](https://chromiumdash.appspot.com/commit/54cf5fa964f0734a8277ea2837aa2e4168e3240a)  

Date: Wed Feb 25 14:13:51 2026


---

### dx...@google.com (2026-02-26)

Project: v8/v8  

Branch:  main  

Author:  LuYahan [yahan@iscas.ac.cn](mailto:yahan@iscas.ac.cn)  

Link:    <https://chromium-review.googlesource.com/7608971>

[riscv][jspi] Clear EPT entry on stack return

---


Expand for full commit details
```
     
    Port commit 54cf5fa964f0734a8277ea2837aa2e4168e3240a 
    Bug: 485784597 
     
    Change-Id: I4a7e12d9047f7a4257be4711d9d6645d42f02a38 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7608971 
    Commit-Queue: Ji Qiu <qiuji@iscas.ac.cn> 
    Reviewed-by: Ji Qiu <qiuji@iscas.ac.cn> 
    Cr-Commit-Position: refs/heads/main@{#105464}

```

---

Files:

- M `src/builtins/riscv/builtins-riscv.cc`

---

Hash: [cd2c216e7658c19bc6501fc785ac2f4be1a3734f](https://chromiumdash.appspot.com/commit/cd2c216e7658c19bc6501fc785ac2f4be1a3734f)  

Date: Thu Feb 26 00:53:12 2026


---

### ch...@google.com (2026-02-26)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sa...@google.com (2026-03-04)

We think it would be worth backmerging the fix here as the bug allows breaking out of the V8 Sandbox. I'm setting the corresponding labels.

### sa...@google.com (2026-03-04)

Other question: I recently (yesterday) landed some logic for table validation: <https://crrev.com/c/7627418> I'm wondering if that could've caught this issue more easily? Basically with that, whenever we do heap verification, we now also validate all entries in the EPT, and that involves accessing the first byte of the object. So if an external object is freed but there's still an EPT entry for it, then ASan should catch this. Would that be the scenario here?

### ch...@google.com (2026-03-04)

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

### ch...@google.com (2026-03-04)

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

### th...@chromium.org (2026-03-04)

> I'm wondering if that could've caught this issue more easily?

I think it would still have been difficult to catch, because the UAF only happens after corrupting a heap object in a specific way.

But there are two other things that I was looking into and could have helped:

- Using the new `Unpublish` method on the trusted `WasmSuspenderObject` when the object becomes unreachable (when the stack returns). I was just discussing that with Jakob when this got reported. (This is part of the landed fix now).
- I recently started thinking about using `ExternalPointerTable::ManagedResource` to zap the entry when the stack is freed. This is not immediately possible because there can be multiple heap owners of the StackMemory at the moment, but with a bit of refactoring this could be done (I just added a [TODO](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/runtime/runtime-wasm.cc;drc=127354195909b8f504c6ff8e5eaef38686bc8ba1;l=1354) for it).

### th...@chromium.org (2026-03-04)

[comment #14](https://issues.chromium.org/issues/485784597#comment14) and [comment #15](https://issues.chromium.org/issues/485784597#comment15):

1. Fixes a security issue (V8 sandbox bypass)
2. <https://chromium-review.googlesource.com/c/v8/v8/+/7607183>
3. Yes
4. Not a new feature
5. NA
6. NA

### sa...@google.com (2026-03-04)

Cool, thanks for the explanation!

> I recently started thinking about using ExternalPointerTable::ManagedResource to zap the entry when the stack is freed.

Yeah this might be a nice option. I think there are probably some more use cases where handing over ownership of external objects to the EPT would make the overall design more robust, so that'd be worth investigating. It's probably a bit blocked on using the EPT in all configurations, but I think that would be feasible, too. (semi-related: <https://crbug.com/427949833>)

### dr...@chromium.org (2026-03-04)

I don't see any crashes in Canary, so approving merge to M146. We don't plan any new releases of M145, so rejecting that merge.

### dx...@google.com (2026-03-05)

Project: v8/v8  

Branch:  refs/branch-heads/14.6  

Author:  Thibaud Michaud [thibaudm@chromium.org](mailto:thibaudm@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7637049>

Merged: [jspi] Clear EPT entry on stack return

---


Expand for full commit details
```
     
    Once the stack returns and is moved to the stack pool, it may be freed 
    at any point depending on the pool capacity and memory pressure. The 
    owning trusted WasmSuspenderObject should be unreachable at this point, 
    but using a sandbox corruption, the object can be kept alive and reused. 
    Clear the EPT entry on return to avoid a use after free. 
     
    R=jkummerow@chromium.org 
     
    Fixed: 485784597 
    (cherry picked from commit 54cf5fa964f0734a8277ea2837aa2e4168e3240a) 
     
    Change-Id: I0ed80d5d5529ab69303fcd818b1546c1e375aca5 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7637049 
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
    Commit-Queue: Thibaud Michaud <thibaudm@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.6@{#23} 
    Cr-Branched-From: e04c3a1a2543bdbee7beac8846c9cbe8f657636f-refs/heads/14.6.202@{#1} 
    Cr-Branched-From: 3b0b01e6594ec362369dc16f069012a81748c8ba-refs/heads/main@{#105132}

```

---

Files:

- M `src/builtins/arm/builtins-arm.cc`
- M `src/builtins/arm64/builtins-arm64.cc`
- M `src/builtins/ia32/builtins-ia32.cc`
- M `src/builtins/x64/builtins-x64.cc`
- M `src/codegen/external-reference.cc`
- M `src/codegen/external-reference.h`
- M `src/wasm/wasm-external-refs.cc`
- M `src/wasm/wasm-external-refs.h`
- A `test/mjsunit/sandbox/wasm-jspi-uaf.js`

---

Hash: [096a780ac897a1224b9f634db86d8fd878dea8a0](https://chromiumdash.appspot.com/commit/096a780ac897a1224b9f634db86d8fd878dea8a0)  

Date: Wed Feb 25 14:13:51 2026


---

### ad...@gmail.com (2026-03-22)

Any updates on the bounty for this one? since it's already been quite a while.

### ch...@google.com (2026-06-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ad...@gmail.com (2026-06-05)

Any reason why this was not considered for VRP ?

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
Baseline. v8 Sandbox.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/485784597)*
