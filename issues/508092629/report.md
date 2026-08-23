# V8 Sandbox Escape: Stale MicrotaskQueue cache leads to OOS write

| Field | Value |
|-------|-------|
| **Issue ID** | [508092629](https://issues.chromium.org/issues/508092629) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sm...@gmail.com |
| **Assignee** | is...@chromium.org |
| **Created** | 2026-04-30 |
| **Bounty** | $20,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

# VULNERABILITY DETAILS

`Builtins_EnqueueMicrotask` can cache a raw `MicrotaskQueue*` that was loaded from an in-sandbox `NativeContext::microtask_queue` external-pointer slot. Under the V8 sandbox attacker model, an attacker with in-sandbox memory corruption can temporarily replace that slot with another valid `MicrotaskQueue` external-pointer handle, make the builtin cache the borrowed raw pointer in isolate data, then restore the slot.

The attached PoC borrows a `MicrotaskQueue` handle from a main-thread `PaintWorklet` global scope, poisons the cached raw pointer, tears the worklet iframe down, and reclaims the freed native `MicrotaskQueue` allocation with controlled WebAssembly module bytes. A later Promise enqueue uses the stale cached `MicrotaskQueue*` and writes through attacker-controlled `ring_buffer`/`capacity`/`size` fields.

This gives a controlled out-of-sandbox write primitive from in-sandbox corruption. In the saved crash log, the final write targets `0x424242424240` and V8 reports a sandbox violation in `Builtins_EnqueueMicrotask`.

Relevant code paths:

- `v8/src/builtins/builtins-microtask-queue-gen.cc`: `GetMicrotaskQueue()` and `TF_BUILTIN(EnqueueMicrotask)`
- `v8/src/objects/contexts-inl.h`: `NativeContext::microtask_queue` external-pointer accessor
- Blink PaintWorklet main-thread global-scope creation/teardown is used only to get a reclaimable `MicrotaskQueue` lifetime.

# VERSION

Chrome Version: 149.0.7815.0
Operating System: Linux

# REPRODUCTION CASE

1. Build chrome with sandbox-testing tool

```
is_debug = false
is_component_build = false
symbol_level = 2
blink_symbol_level = 2
v8_symbol_level = 2
dcheck_always_on = false
v8_enable_sandbox = true
v8_enable_memory_corruption_api = true
is_asan = false
use_remoteexec = false
use_siso = false

```

2. Run

```
/path/to/chrome \
  --headless=new \
  --disable-gpu \
  --no-sandbox \
  --js-flags="--sandbox-testing --expose-gc" \
  file:///path/to/poc.html

```

Type of crash: v8 sandbox violation

## Attachments

- [crash.log](attachments/crash.log) (text/plain, 1.3 KB)
- [poc.html](attachments/poc.html) (text/html, 9.9 KB)
- [fix.diff](attachments/fix.diff) (text/x-diff, 1.9 KB)
- [crash.log](attachments/crash_76180600.log) (text/plain, 15.2 KB)
- [poc.html](attachments/poc_76181731.html) (text/html, 10.1 KB)
- [aaw.html](attachments/aaw.html) (text/html, 39.8 KB)
- [exp.mp4](attachments/exp.mp4) (video/mp4, 11.7 MB)
- [exp.html](attachments/exp.html) (text/html, 129.9 KB)
- [exploit.tar.gz](attachments/exploit.tar.gz) (application/x-gzip, 27.7 KB)
- [aaw.html](attachments/aaw_78623096.html) (text/html, 121.4 KB)
- [aaw-gdb.png](attachments/aaw-gdb.png) (image/png, 185.5 KB)
- [exp.html](attachments/exp_78600177.html) (text/html, 121.4 KB)
- [exp-sandbox.mkv](attachments/exp-sandbox.mkv) (video/x-matroska, 980.7 KB)

## Timeline

### sm...@gmail.com (2026-04-30)

## Bisect

[5f0a2f4eb9de](https://chromium-review.googlesource.com/c/v8/v8/+/7706944) (2026-03-31), `[microtask] Cache MicrotaskQueue pointer in EnqueueMicrotask builtin`.

The vulnerable raw `MicrotaskQueue*` cache in `EnqueueMicrotask` has existed since this commit. Before this change, `EnqueueMicrotask` reloaded `NativeContext::microtask_queue` on every call, so restoring the slot before the final enqueue prevented reuse of a borrowed/stale queue pointer.

### sm...@gmail.com (2026-04-30)

## Patch

(If you've confirmed the vulnerability is valid and patch looks good, I wanna upload this as a CL.)

`fix.diff` removes the raw `MicrotaskQueue*` cache from `Builtins_EnqueueMicrotask`.

Vulnerable path cached a native `MicrotaskQueue*` in isolate state and reused it when the cached native context matched the current native context. The pointer itself was resolved from the in-sandbox `NativeContext::microtask_queue` external-pointer slot, so an attacker could temporarily substitute that slot, poison the cached raw pointer, restore the slot, and later make `EnqueueMicrotask` use the stale queue pointer.

Patch makes `EnqueueMicrotask` resolve the queue from the current `NativeContext` on every call instead of reusing the cached raw pointer:

```
TNode<NativeContext> native_context = LoadNativeContext(context);
TNode<RawPtrT> microtask_queue = GetMicrotaskQueue(native_context);

```

This blocks the bug because the final enqueue no longer depends on a previously cached raw `MicrotaskQueue*`. After the attacker restores `NativeContext::microtask_queue`, the builtin reloads the current queue from the restored external-pointer slot, so the transient substituted queue cannot survive as stale trusted state.

### cl...@appspot.gserviceaccount.com (2026-04-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4838880142458880.

### ch...@google.com (2026-05-01)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### sm...@gmail.com (2026-05-01)

Hello,

I noticed that ClusterFuzz was unable to reproduce this issue. The Chrome revision used by ClusterFuzz appears to be 1582644, which predates the inclusion of this bug, so the vulnerable code path is not present in that build.

This issue should reproduce on ToT builds after CL 7706944 was merged. If reproduction is needed, please use a build from after that CL.

I also prepared a simpler PoC that directly accesses the stale cached `MicrotaskQueue*` and produces an ASan report without exploit steps. (Tested checkout 346d60b9d1cc07f3972869e029d409b11cc62a09)

```
ASAN_SYMBOLIZER_PATH="$PWD/third_party/llvm-build/Release+Asserts/bin/llvm-symbolizer" \
ASAN_OPTIONS="alloc_dealloc_mismatch=0:allocator_may_return_null=1:allow_user_segv_handler=1:check_malloc_usable_size=0:detect_leaks=0:detect_odr_violation=0:detect_stack_use_after_return=1:fast_unwind_on_fatal=0:handle_abort=1:handle_segv=1:handle_sigbus=1:handle_sigfpe=1:handle_sigill=1:print_scariness=1:print_summary=1:print_suppressions=0:redzone=128:strict_memcmp=0:symbolize=1:use_sigaltstack=1" \
./chrome \
  --headless=new --disable-gpu --no-sandbox \
  --js-flags="--sandbox-testing --expose-gc" \
  file:///path/to/poc_asan_report_only.html

```

### cl...@chromium.org (2026-05-04)

Michael, what's the status of the `linux_asan_chrome_v8_sandbox_testing` job on Clusterfuzz? The last revision (1582644) is from February. Is this job deprecated? So we have some other chrome sandbox testing job?

### ma...@google.com (2026-05-04)

Filed [issue 509380872](https://issues.chromium.org/issues/509380872) to investigate.

### jg...@chromium.org (2026-05-05)

So the summary of this is "the <https://chromium-review.googlesource.com/c/v8/v8/+/7706944> optimization is invalid" since the cached MicrotaskQueue ptr is not protected by `LoadExternalPointerFromObject` <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/builtins/builtins-microtask-queue-gen.cc;l=66;drc=855e1a2fe32809337ac15db5ce1a21737b57e366>.

The fix would be to revert the optimization. Igor, concur?

### is...@chromium.org (2026-05-05)

Thank you for the report! Very nice!

So, we have a UAF here. We could certainly revert the optimization but I think the fix would be to:

1. cache the MQ EPT handle in Isolate in addition to MQ value,
2. make GC visit the cached MQ EPT entry (this will keep the MQ object alive even if NC looses the link to the MQ),
3. make NC::set\_MQ(..) clear the MQ cache in the Isolate (just in case this store is updating the cached MQ EPT entry).

Let me try this.

### is...@chromium.org (2026-05-12)

I'm going to disable the optimization for now and land the full CL with `d8` testing harness in a follow-up CL.

### dx...@google.com (2026-05-12)

Project: v8/v8  

Branch:  main  

Author:  Igor Sheludko [ishell@chromium.org](mailto:ishell@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7843152>

[microtask] Disable MicrotaskQueue pointer caching in EnqueueMicrotask

---


Expand for full commit details
```
     
    ... builtin until the issue is resolved for real. 
     
    Fixed: 508092629 
    Bug: 497675623 
    Change-Id: I15ddb3110c37d84c4e9cb83da0b6c1b81baa7784 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7843152 
    Commit-Queue: Igor Sheludko <ishell@chromium.org> 
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    Commit-Queue: Michael Lippautz <mlippautz@chromium.org> 
    Auto-Submit: Igor Sheludko <ishell@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#107277}

```

---

Files:

- M `src/builtins/builtins-microtask-queue-gen.cc`

---

Hash: [c2eab5ee184d928140d72cfd4156c570913fa6ae](https://chromiumdash.appspot.com/commit/c2eab5ee184d928140d72cfd4156c570913fa6ae)  

Date: Tue May 12 19:17:21 2026


---

### sm...@gmail.com (2026-05-13)

Thank you for handling this issue, Igor. I’ll be waiting for your follow-up CL :D

### ch...@google.com (2026-05-13)

**M148** merge request created. **Please update [crbug/512729632](https://crbug.com/512729632) to have this merge reviewed.**

### ch...@google.com (2026-05-13)

**M149** merge request created. **Please update [crbug/512729201](https://crbug.com/512729201) to have this merge reviewed.**

### dx...@google.com (2026-05-13)

Project: v8/v8  

Branch:  refs/branch-heads/14.9  

Author:  Igor Sheludko [ishell@chromium.org](mailto:ishell@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7844894>

Merged: [microtask] Disable MicrotaskQueue pointer caching in EnqueueMicrotask

---


Expand for full commit details
```
     
    ... builtin until the issue is resolved for real. 
     
    (cherry picked from commit c2eab5ee184d928140d72cfd4156c570913fa6ae) 
     
    Fixed: 512729201 
    Bug: 508092629 
    Bug: 497675623 
    Change-Id: I15ddb3110c37d84c4e9cb83da0b6c1b81baa7784 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7843152 
    Commit-Queue: Igor Sheludko <ishell@chromium.org> 
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    Commit-Queue: Michael Lippautz <mlippautz@chromium.org> 
    Auto-Submit: Igor Sheludko <ishell@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#107277} 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7844894 
    Cr-Commit-Position: refs/branch-heads/14.9@{#12} 
    Cr-Branched-From: 8f08364a351ad38a60421137a09ef23953ecdd56-refs/heads/14.9.207@{#1} 
    Cr-Branched-From: 8de67b11924d5e8c0032029165a52d800cf05f1f-refs/heads/main@{#106999}

```

---

Files:

- M `src/builtins/builtins-microtask-queue-gen.cc`

---

Hash: [7406fa9ce1c99835cf5a7423ea1559752bae4372](https://chromiumdash.appspot.com/commit/7406fa9ce1c99835cf5a7423ea1559752bae4372)  

Date: Tue May 12 19:17:21 2026


---

### dx...@google.com (2026-05-13)

Project: v8/v8  

Branch:  refs/branch-heads/14.8  

Author:  Igor Sheludko [ishell@chromium.org](mailto:ishell@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7843195>

Merged: [microtask] Disable MicrotaskQueue pointer caching in EnqueueMicrotask

---


Expand for full commit details
```
     
    ... builtin until the issue is resolved for real. 
     
    (cherry picked from commit c2eab5ee184d928140d72cfd4156c570913fa6ae) 
     
    Fixed: 512729632 
    Bug: 508092629 
    Bug: 497675623 
    Change-Id: I15ddb3110c37d84c4e9cb83da0b6c1b81baa7784 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7843152 
    Commit-Queue: Igor Sheludko <ishell@chromium.org> 
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    Commit-Queue: Michael Lippautz <mlippautz@chromium.org> 
    Auto-Submit: Igor Sheludko <ishell@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#107277} 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7843195 
    Cr-Commit-Position: refs/branch-heads/14.8@{#44} 
    Cr-Branched-From: f9659283a5f8d42b3c09228cf5df606fcaf47a3d-refs/heads/14.8.178@{#1} 
    Cr-Branched-From: 141232520dc4910401240c531db3af36910a0fd1-refs/heads/main@{#106240}

```

---

Files:

- M `src/builtins/builtins-microtask-queue-gen.cc`

---

Hash: [6401439f2aa2d99de9128c656e7336a163aadb9c](https://chromiumdash.appspot.com/commit/6401439f2aa2d99de9128c656e7336a163aadb9c)  

Date: Tue May 12 19:17:21 2026


---

### sm...@gmail.com (2026-05-19)

This is my full out-of-sandbox AAW PoC for this vulnerability. (Tested checkout `346d60b9d1cc07f3972869e029d409b11cc62a09` on Ubuntu 22.04)

This poc chains a few controlled handoffs. First, poc turns the stale queue into a native write surface. After the queue owner is released, a later Promise microtask enqueue still goes through the cached stale pointer. The freed queue memory is then reclaimed with valid WebAssembly modules whose custom-section bytes double as a fake `MicrotaskQueue` layout, giving control over `size_`, `capacity_`, `start_`, and `ring_buffer_`.

Next, poc stabilizes this write surface instead of using the first stale write directly. Reclaim cycles leak a native ring-buffer pointer, and a cache-pivot reclaim redirects the cached queue pointer to a selected Promise reaction task. That task is then treated as the fake queue, allowing the poc to program queue grow/free operations through sandbox-visible fields and create a controlled native ring-buffer free.

The final free is reclaimed with small Wasm GC modules whose code section is padded so the exported function body lands at a predictable offset. The module imports a post-write hook and defines a struct type with one mutable i64 field. During JSON.stringify, a toJSON callback emits byte-safe characters that become the replacement Wasm body. When the reclaimed module is instantiated and executed, that body materializes where - 7 for the struct-field access and what as the value, then performs the struct-field store that completes the out-of-sandbox write.

Run with:

```
/path/to/chrome \
  --headless=new \
  --disable-gpu \
  --no-sandbox \
  --js-flags="--sandbox-testing" \
  file:///path/to/aaw.html

```

### qk...@google.com (2026-06-09)

Add LTS-NotApplicable-144 label because M144 doesn't have the culprit CL[1]

[1] https://chromium-review.git.corp.google.com/c/v8/v8/+/7706944

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
v8 sandbox


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### sm...@gmail.com (2026-06-15)

Hello, wasn't my AAW PoC reproducible? I wanna get v8 sandbox controlled write bounty :(...

### sm...@gmail.com (2026-06-20)

# Renderer RCE

Hello,

I chained [b/508092629](https://issues.chromium.org/issues/508092629) with [b/516833326](https://issues.chromium.org/issues/516833326)(I also used this initial primitive in my M149 V8CTF exploit; see [b/522336734](https://issues.chromium.org/issues/522336734)) to build a Renderer RCE primitive on Chrome version 149.0.7819.0(<https://storage.googleapis.com/chrome-for-testing-public/149.0.7819.0/linux64/chrome-linux64.zip>).

The attached video, `exp.mp4`, shows the exploit obtaining the flag using the Dockerfile provided in the V8 CTF environment. From the provided files, I only modified two values: the Chrome version and the timeout. The `exploit.tar.gz` used in the video is simply the attached `exp.html` compressed as an archive.

Please let me know if the exploit does not reproduce, or if there are any additional requirements I should satisfy for a VRP re-evaluation.

Thank you.

### aj...@google.com (2026-06-25)

Thanks, while the exploit is interesting, it is not clear that it changes what is in the initial report, and proving exploitation of another issue is not in scope for the VRP. The initial report received a reward for a v8 sandbox escape.

### sm...@gmail.com (2026-06-25)

[#comment23](https://issues.chromium.org/issues/508092629#comment23) Hello, my exploit in [#comment21](https://issues.chromium.org/issues/508092629#comment21) is not exploitation of another issue. That exploit used this report's bad MQ optimization vulnerability as V8 SBX(I chained [b/516833326](https://issues.chromium.org/issues/516833326) just for obtain caged AAR/W Since I don't know there's any sandbox-testing API enabled Non-ASan official chrome build).

May I ask about why my initial report received just v8 sandbox reward($5k), not v8 sandbox controlled write($20k) reward + bisection bonus? Is it able to re-evaluate as controlled write reprot? Is there anything I can do more...?

### sm...@gmail.com (2026-06-26)

exploit (`id; uname -a`) & AAW PoC(write 0x434343... to addr 0x424242...) with Sandbox Testing API. Since this exploit uses uses libc/Chrome ROP gadgets from my locally built chrome binary so it may not be portable to other environments. For reproducing full renderer-RCE chain, I recommend using the exploit from [#comment22](https://issues.chromium.org/issues/508092629#comment22) instead.

### dx...@google.com (2026-07-01)

Project: v8/v8  

Branch:  main  

Author:  Igor Sheludko [ishell@chromium.org](mailto:ishell@chromium.org)  

Link:    <https://chromium-review.googlesource.com/8016725>

[runtime] Fix MicrotaskQueue liveness and serialization issues

---


Expand for full commit details
```
[runtime] Fix MicrotaskQueue liveness and serialization issues 
 
This fixes a Use-After-Free (UAF) vulnerability where the CppGC-managed 
MicrotaskQueue in NativeContext was not traced by the V8 GC, allowing 
it to be prematurely reclaimed. 
 
In addition, this CL adds infrastructure in d8 and sandbox testing 
tools to verify custom MicrotaskQueue lifecycle and isolation across 
native contexts. 
 
1. Extend Realm.create() with an option bag argument for requesting a 
   new realm to be created with its own MicrotaskQueue. 
2. Extend SandboxTesting::GetFieldOffsetMap() and GetInstanceTypeMap() 
   with offsets for NativeContext's microtask_queue and JSFunction's 
   context fields, and export cppgc_microtask_queue in build config. 
3. Add regression mjsunit tests verifying microtask queue separation 
   and triggering UAF via sandbox memory corruption Api. 
 
TAG=agy 
CONV=4bb71540-afc9-4de3-8c14-b9a4b213d916 
 
Bug: 515252150 
Bug: 508092629 
Change-Id: I8a694a92bd0d3de618ff02deb0fb7c7bff27cc61 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/8016725 
Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
Commit-Queue: Igor Sheludko <ishell@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#108380}

```

---

Files:

- M `BUILD.gn`
- M `bazel/defs.bzl`
- M `include/v8-internal.h`
- M `include/v8-sandbox.h`
- M `src/api/api.cc`
- M `src/builtins/builtins-microtask-queue-gen.cc`
- M `src/codegen/code-stub-assembler.cc`
- M `src/codegen/code-stub-assembler.h`
- M `src/d8/d8.cc`
- M `src/d8/d8.h`
- M `src/objects/contexts-inl.h`
- M `src/objects/contexts.cc`
- M `src/objects/contexts.h`
- M `src/objects/cpp-heap-object-wrapper.h`
- M `src/objects/object-macros.h`
- M `src/objects/objects-body-descriptors-inl.h`
- M `src/objects/slots-inl.h`
- M `src/objects/slots.h`
- M `src/sandbox/cppheap-pointer-table.h`
- M `src/sandbox/testing.cc`
- M `src/snapshot/context-serializer.cc`
- M `src/snapshot/serializer.cc`
- A `test/mjsunit/d8/d8-realm-microtask-queue.js`
- M `test/mjsunit/mjsunit.status`
- A `test/mjsunit/regress/regress-515252150.js`
- A `test/mjsunit/sandbox/regress/regress-508092629.js`

---

Hash: [6ecd7e195d8f773eacc10039075f93d1dc83999a](https://chromiumdash.appspot.com/commit/6ecd7e195d8f773eacc10039075f93d1dc83999a)  

Date: Wed Jul 1 16:01:39 2026


---

### sp...@google.com (2026-07-01)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided to issue a reward of
**$15000.00** for your report. Congratulations!

Rationale for this decision:

Controlled v8 sandbox bypass.

Important payment guidance:

- **Bugcrowd**: This payment will be issued by Bugcrowd. You will receive an
  email from Bugcrowd in the next 24 hours which contains a submission you
  must claim to be rewarded.
  
  If you do not receive an email from Bugcrowd, please check your spam folder
  and then reach out to us via a comment here. For issues related to Bugcrowd
  itself, please contact them via <https://bugcrowd.com/support>.

Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot

P.S. One other thing we'd like to mention:

- Please do NOT publicly disclose details until a fix has been released to all
  our users. Early public disclosure may cancel the provisional reward. Also,
  please be considerate about disclosure when the bug affects a core library
  that may be used by other products. Please do NOT share this information
  with third parties who are not directly involved in fixing the bug. Doing so
  may cancel the provisional reward. Please be honest if you have already
  disclosed anything publicly or to third parties. Lastly, we understand that
  some of you are not interested in money. We offer the option to donate your
  reward to an eligible charity. Any rewards that are unclaimed after 12
  months will be donated to a charity of our choosing.

Please contact [security-vrp@chromium.org](mailto:security-vrp@chromium.org) with any questions.

### sm...@gmail.com (2026-07-02)

Thank you!!!

### ch...@google.com (2026-08-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/508092629)*
