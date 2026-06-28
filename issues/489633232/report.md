# V8 Sandbox Bypass: AAW/PC Control via major GC between codegen and Code object creation

| Field | Value |
|-------|-------|
| **Issue ID** | [489633232](https://issues.chromium.org/issues/489633232) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | kr...@gmail.com |
| **Assignee** | vi...@chromium.org |
| **Created** | 2026-03-04 |
| **Bounty** | $20,000.00 |

## Description

### VULNERABILITY DETAILS

#### Details

Recall [crbug/443772809](https://crbug.com/443772809) worked by triggering major GC after removing all in-sandbox dispatch handle references of some target dispatch entry to free and reclaim dispatch entries while they were being used by other Code. This was fixed by [marking Code that was dependent on the entry for deopt](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/heap/mark-compact.cc;l=3508-3516;drc=64820206068b8feaf4b9d4de22362cfcf047b8b6) and [clearing the Code's embedded objects and dispatch handles](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/heap/mark-compact.cc;l=3495;drc=84e9f8cb8ba9621be941c81af04d33df743f7de4).

However, if a major GC were to occur after dispatch entry call instructions are emitted as part of codegen (eg. [after here in Maglev](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/maglev/maglev-ir.cc;l=6785;drc=affe1525dc39265a2062a9fccdb2977371878455)) and before the actual Code object is made (eg. [before here in Maglev](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/maglev/maglev-code-generator.cc;l=1750-1751;drc=eef55251831ddc57279faad9442925750a99adaa)), there is no Code object yet that the GC can find to mark for deopt. So, when the Code is eventually created later, it's made with a stale instruction stream that calls via a dispatch entry that should no longer be used.

This leads to AAW/PC control as in the past as the freed dispatch entry can be reclaimed with a higher formal parameter count leading to under-application that imbalances the stack when called via the stale Code.

**Note:** This is different from [crbug/481295170](https://crbug.com/481295170) as there is no Code yet to even mark for deoptimization.

#### Details

### VERSION

V8 commit: 2acd56ce93233d544ca40002ef5da871722940c8

#### REPRODUCTION CASE

**NOTE (for the shepherd):** To hopefully reproduce in CF, the `linux_asan_d8_sandbox_testing` job type with the below shell args should hopefully do the trick.

**Shell args**: `--allow-natives-syntax --sandbox-testing --expose-gc`

**Build args**:

```
is_debug=false
is_asan=true
v8_enable_sandbox=true
v8_enable_memory_corruption_api=true
dcheck_always_on=false
target_cpu="x64"

```

**Sample output (`--disable-in-process-stack-traces` used to show PC)**:

```
$ ./d8 --allow-natives-syntax --sandbox-testing --expose-gc --disable-in-process-stack-traces ./doa-code-poc.js 
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x79d600000000,0x7ad600000000)

## V8 sandbox violation detected!

AddressSanitizer:DEADLYSIGNAL
=================================================================
==5769==ERROR: AddressSanitizer: SEGV on unknown address 0x424242424242 (pc 0x424242424242 bp 0x424242424242 sp 0x7ffd085670b8 T0)
==5769==The signal is caused by a READ memory access.
    #0 0x424242424242  (<unknown module>)

==5769==Register values:
rax = 0x000079d600000011  rbx = 0x000079d600000011  rcx = 0x0000000000000002  rdx = 0x0000424242424242  
rdi = 0x0000000000000000  rsi = 0x0000000000000000  rbp = 0x0000424242424242  rsp = 0x00007ffd085670b8  
 r8 = 0x0000000000000000   r9 = 0x0000000000000000  r10 = 0x00005588e00c0145  r11 = 0x00007ffd08566e81  
r12 = 0x00007ffd08566da0  r13 = 0x00007e27875e1080  r14 = 0x000079d600000000  r15 = 0x00007de7875e0849  
AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV (<unknown module>) 
==5769==ABORTING

```
### FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: Sandbox violation

### CREDIT INFORMATION

Reporter credit: Krishna Ravishankar (@krsh732)

## Attachments

- [doa-code-poc.js](attachments/doa-code-poc.js) (text/javascript, 2.9 KB)
- [doa-code-poc-v2.js](attachments/doa-code-poc-v2.js) (text/javascript, 3.7 KB)
- [doa-code-insufficient-fix-poc.js](attachments/doa-code-insufficient-fix-poc.js) (text/javascript, 4.4 KB)

## Timeline

### kr...@gmail.com (2026-03-04)

Ah, this PoC unfortunately won't repro on CF because `%StartMaglevJob` isn't enabled with `--fuzzing`. I can try to look at alternate ways to write the PoC if necessary.

### kr...@gmail.com (2026-03-04)

Attached a CF friendly version in this comment. Please ignore the one in [comment#1](https://issues.chromium.org/issues/489633232#comment1).

### ch...@google.com (2026-03-05)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### cl...@appspot.gserviceaccount.com (2026-03-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6550482524766208.

### me...@google.com (2026-03-05)

Thanks for the report. mlippautz@, proactively adding you while CF works on the PoC, thanks.

### kr...@gmail.com (2026-03-05)

Re [comment#5](https://issues.chromium.org/issues/489633232#comment5): I think that run is using the wrong job and won't repro. It needs to use the `linux_asan_d8_sandbox_testing` job.

### cl...@appspot.gserviceaccount.com (2026-03-06)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5234106119946240.

### kr...@gmail.com (2026-03-06)

Re [comment#8](https://issues.chromium.org/issues/489633232#comment8): ~~I *think* this one failed cause the file name is wrong. Should be `doa-code-poc-v2.js` instead of `doa-code-poc-v21.js`?~~ It failed because the timing was always off in CF (gc either happens too soon/late and/or pwn was called before background compilation finishes)

### ch...@google.com (2026-03-06)

Setting milestone because of s0/s1 severity.

### ml...@google.com (2026-03-11)

From talking to Leszek last week: We should probably only create the dispatch handles on the main thread during code finalization right now.

### dx...@google.com (2026-03-18)

Project: v8/v8  

Branch:  main  

Author:  Victor Gomes [victorgomes@chromium.org](mailto:victorgomes@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7665890>

[sandbox] Check dispatch handle in code finalization

---


Expand for full commit details
```
     
    Bug: 489633232 
    Change-Id: I7baca7a9aeebabb241afb9c15e264db96f116210 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7665890 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Victor Gomes <victorgomes@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105866}

```

---

Files:

- M `src/codegen/assembler.cc`
- M `src/codegen/assembler.h`
- M `src/compiler/backend/arm/code-generator-arm.cc`
- M `src/compiler/backend/arm64/code-generator-arm64.cc`
- M `src/compiler/backend/x64/code-generator-x64.cc`
- M `src/maglev/maglev-graph-builder.cc`
- M `src/maglev/maglev-graph-builder.h`
- M `src/maglev/maglev-ir-inl.h`
- M `src/maglev/maglev-ir.cc`
- M `src/maglev/maglev-ir.h`
- M `src/objects/instruction-stream-inl.h`
- M `src/objects/instruction-stream.cc`
- M `src/objects/instruction-stream.h`

---

Hash: [920ca4b1c8d424fdbffd1921825dd7f0ba67c6d1](https://chromiumdash.appspot.com/commit/920ca4b1c8d424fdbffd1921825dd7f0ba67c6d1)  

Date: Wed Mar 18 10:07:45 2026


---

### dx...@google.com (2026-03-18)

Project: v8/v8  

Branch:  main  

Author:  Nico Hartmann [nicohartmann@chromium.org](mailto:nicohartmann@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7680030>

Revert "[sandbox] Check dispatch handle in code finalization"

---


Expand for full commit details
```
     
    This reverts commit 920ca4b1c8d424fdbffd1921825dd7f0ba67c6d1. 
     
    Reason for revert: https://ci.chromium.org/ui/p/v8/builders/ci/V8%20Linux64%20-%20PKU%20-%20debug/7840/overview 
     
    Original change's description: 
    > [sandbox] Check dispatch handle in code finalization 
    > 
    > Bug: 489633232 
    > Change-Id: I7baca7a9aeebabb241afb9c15e264db96f116210 
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7665890 
    > Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    > Commit-Queue: Victor Gomes <victorgomes@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#105866} 
     
    Bug: 489633232 
    No-Presubmit: true 
    No-Tree-Checks: true 
    No-Try: true 
    Change-Id: I42b9da920540bc19770dbf0a56e8073dab68f64a 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7680030 
    Owners-Override: Nico Hartmann <nicohartmann@chromium.org> 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: Nico Hartmann <nicohartmann@chromium.org> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#105874}

```

---

Files:

- M `src/codegen/assembler.cc`
- M `src/codegen/assembler.h`
- M `src/compiler/backend/arm/code-generator-arm.cc`
- M `src/compiler/backend/arm64/code-generator-arm64.cc`
- M `src/compiler/backend/x64/code-generator-x64.cc`
- M `src/maglev/maglev-graph-builder.cc`
- M `src/maglev/maglev-graph-builder.h`
- M `src/maglev/maglev-ir-inl.h`
- M `src/maglev/maglev-ir.cc`
- M `src/maglev/maglev-ir.h`
- M `src/objects/instruction-stream-inl.h`
- M `src/objects/instruction-stream.cc`
- M `src/objects/instruction-stream.h`

---

Hash: [785d70e90ab333ae43b3fb5db903a9266971a054](https://chromiumdash.appspot.com/commit/785d70e90ab333ae43b3fb5db903a9266971a054)  

Date: Wed Mar 18 12:55:42 2026


---

### kr...@gmail.com (2026-03-18)

Hey Victor, I saw that this issue was marked as fixed once [crrev/c/7665890](https://crrev.com/c/7665890) landed. While it got reverted anyway due to some test failures, heads up, it is/was insufficient to fix the issue by itself. To beat the checks in `InstructionStream::ValidateJSDispatchHandles` it simply suffices to corrupt the original dispatch handle back in while GC collects the dispatch entry:

```
diff --git a/./doa-code-poc-v2.js b/./doa-code-insufficient-fix-poc.js
index f0fddf3..9940b6c 100644
--- a/./doa-code-poc-v2.js
+++ b/./doa-code-insufficient-fix-poc.js
@@ -64,6 +64,7 @@ const ta = new Int32Array(new SharedArrayBuffer(0x8));
 // Trigger and race pwn's background compilation such that a major GC clearing victim's dispatch entry 
 // occurs after victim's CallKnownJSFunction::GenerateCode runs and before the Code object for pwn 
 // is created.
+const handle = memory.getUint32(Sandbox.getAddressOf(victim) + kDispatchHandleOffset, true);
 pwn();
 Atomics.wait(ta, 0, 0, 300); // synchronous wait hack (random number out of a hat)
 Sandbox.corruptObjectField(victim, "dispatch_handle", 0);
@@ -73,6 +74,13 @@ memory.setUint32(
   true
 );
 gc({type: "major"});
+Atomics.wait(ta, 0, 0, 100); // no science feel good random number out of a hat as usual
+// For convenience and to avoid further fiddling with timing, clobber victim's map and force 
+// InstructionStream::Verify to assume it's a FeedbackCell. This way, even if GC was still active and
+// marking, it wouldn't visit the dispatch entry through what was once the victim JSFunction to mark
+// the entry as being alive.
+memory.setUint32(Sandbox.getAddressOf(victim), /* kMapOffset */ 0, true);
+memory.setUint32(Sandbox.getAddressOf(victim) + kDispatchHandleOffsetInFeedbackCell, handle, true);
 
 Atomics.wait(ta, 0, 0, 3000); // synchronous wait hack (random number out of a hat)
 const victim_aliasing_imbalancer = eval("(a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14) => {}");

```

### kr...@gmail.com (2026-03-20)

I posted [crrev/c/7686890](https://crrev.com/c/7686890) which is based on [crrev/c/7665890](https://crrev.com/c/7665890) but instead checks that the argument count of the dispatch entry is the same as it originally was instead of checking that the dispatch handle on the JSFunction is the same as it originally was.

### dx...@google.com (2026-03-20)

Project: v8/v8  

Branch:  main  

Author:  Krishna Ravishankar [krishna.ravi732@gmail.com](mailto:krishna.ravi732@gmail.com)  

Link:    <https://chromium-review.googlesource.com/7686890>

[sandbox] Check dispatch entry in code finalization

---


Expand for full commit details
```
     
    Bug: 489633232 
    Change-Id: I7f4c29de15e37b77cf64a1cf7b976bdadc762537 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7686890 
    Reviewed-by: Victor Gomes <victorgomes@chromium.org> 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Auto-Submit: Krishna Ravishankar <krishna.ravi732@gmail.com> 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105930}

```

---

Files:

- M `src/codegen/assembler.cc`
- M `src/codegen/assembler.h`
- M `src/compiler/backend/arm/code-generator-arm.cc`
- M `src/compiler/backend/arm64/code-generator-arm64.cc`
- M `src/compiler/backend/x64/code-generator-x64.cc`
- M `src/maglev/maglev-ir.cc`
- M `src/objects/instruction-stream-inl.h`
- M `src/objects/instruction-stream.cc`
- M `src/objects/instruction-stream.h`

---

Hash: [b5db50f99bc02b1713a28c1718c4bd666264c9e7](https://chromiumdash.appspot.com/commit/b5db50f99bc02b1713a28c1718c4bd666264c9e7)  

Date: Fri Mar 20 03:50:34 2026


---

### sa...@google.com (2026-03-20)

Thanks for the report and the work on this issue! I think it would be worth backmerging a fix here as this bug allows breaking out of the V8 Sandbox. Do we have a minimal fix for the issue that could be backported? Then I can set the necessary labels. Also, do we want to track any follow-up work/hardening in this bug or a separate one?

### kr...@gmail.com (2026-03-20)

Thank you for the kind words! Regarding [comment#17](https://issues.chromium.org/issues/489633232#comment17), not sure if the following were meant for me but:

> Do we have a minimal fix for the issue that could be backported?

[crrev/c/7686890](https://crrev.com/c/7686890) is a small patch and likely isn't too invasive, so maybe it could be backported, but I'll defer to others to answer this more definitively.

> Also, do we want to track any follow-up work/hardening in this bug or a separate one?

Leszek mentioned the following in [crrev/c/7686890](https://crrev.com/c/7686890): "long term I would like the dispatch handle vector to be an actual edge in the GC graph."

Maybe this could be tracked somewhere if it hasn't already been.

### vi...@chromium.org (2026-03-23)

It can be cleanly merged to M146 (<https://chromium-review.git.corp.google.com/c/v8/v8/+/7689157>) and M147 (<https://chromium-review.git.corp.google.com/c/v8/v8/+/7691495>).

### sa...@google.com (2026-03-23)

Great, thanks! I'll request the merges then.

### ch...@google.com (2026-03-23)

Merge review required: M147 is already shipping to beta.

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
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-03-23)

Merge review required: M146 is already shipping to stable.

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

### dr...@chromium.org (2026-03-23)

No crashes in Canary, approved to merge to M146 and M147.

### dx...@google.com (2026-03-24)

Project: v8/v8  

Branch:  main  

Author:  Liu Yu [liuyu@loongson.cn](mailto:liuyu@loongson.cn)  

Link:    <https://chromium-review.googlesource.com/7695804>

[loong64][sandbox] Check dispatch entry in code finalization

---


Expand for full commit details
```
     
    Port commit b5db50f99bc02b1713a28c1718c4bd666264c9e7 
     
    Bug: 489633232 
    Change-Id: Id12cc76ddd55bb5147f7a7d14e67df5930be6fe3 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7695804 
    Reviewed-by: Zhao Jiazhong <zhaojiazhong-hf@loongson.cn> 
    Auto-Submit: Liu Yu <liuyu@loongson.cn> 
    Commit-Queue: Zhao Jiazhong <zhaojiazhong-hf@loongson.cn> 
    Cr-Commit-Position: refs/heads/main@{#105988}

```

---

Files:

- M `src/compiler/backend/loong64/code-generator-loong64.cc`

---

Hash: [01f03c952c7274fd1bb7169a40df1400c047668e](https://chromiumdash.appspot.com/commit/01f03c952c7274fd1bb7169a40df1400c047668e)  

Date: Tue Mar 24 06:20:13 2026


---

### dx...@google.com (2026-03-24)

Project: v8/v8  

Branch:  refs/branch-heads/14.7  

Author:  Krishna Ravishankar [krishna.ravi732@gmail.com](mailto:krishna.ravi732@gmail.com)  

Link:    <https://chromium-review.googlesource.com/7691495>

Merged: [sandbox] Check dispatch entry in code finalization

---


Expand for full commit details
```
     
    Bug: 489633232 
     
    (cherry picked from commit b5db50f99bc02b1713a28c1718c4bd666264c9e7) 
     
    Change-Id: I6b43c67e7f0aa4f93643aa2f7966afe14b16f0e8 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7691495 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Victor Gomes <victorgomes@chromium.org> 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Auto-Submit: Victor Gomes <victorgomes@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.7@{#14} 
    Cr-Branched-From: 723547b98d2e75cb85556ab85479688c9fbe2f1e-refs/heads/14.7.173@{#1} 
    Cr-Branched-From: 3fc49d4c4cd9e6202fe21f5925899292ffadb20a-refs/heads/main@{#105661}

```

---

Files:

- M `src/codegen/assembler.cc`
- M `src/codegen/assembler.h`
- M `src/compiler/backend/arm/code-generator-arm.cc`
- M `src/compiler/backend/arm64/code-generator-arm64.cc`
- M `src/compiler/backend/x64/code-generator-x64.cc`
- M `src/maglev/maglev-ir.cc`
- M `src/objects/instruction-stream-inl.h`
- M `src/objects/instruction-stream.cc`
- M `src/objects/instruction-stream.h`

---

Hash: [0194241de6c097c8f77a7421ecfa54efd98d4ad8](https://chromiumdash.appspot.com/commit/0194241de6c097c8f77a7421ecfa54efd98d4ad8)  

Date: Fri Mar 20 03:50:34 2026


---

### dx...@google.com (2026-03-24)

Project: v8/v8  

Branch:  refs/branch-heads/14.6  

Author:  Krishna Ravishankar [krishna.ravi732@gmail.com](mailto:krishna.ravi732@gmail.com)  

Link:    <https://chromium-review.googlesource.com/7689157>

Merged: [sandbox] Check dispatch entry in code finalization

---


Expand for full commit details
```
     
    Bug: 489633232 
     
    (cherry picked from commit b5db50f99bc02b1713a28c1718c4bd666264c9e7) 
     
    Change-Id: I1af1eea617a51226652cc883434c3c1f4a06ae1f 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7689157 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Auto-Submit: Victor Gomes <victorgomes@chromium.org> 
    Commit-Queue: Victor Gomes <victorgomes@chromium.org> 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.6@{#53} 
    Cr-Branched-From: e04c3a1a2543bdbee7beac8846c9cbe8f657636f-refs/heads/14.6.202@{#1} 
    Cr-Branched-From: 3b0b01e6594ec362369dc16f069012a81748c8ba-refs/heads/main@{#105132}

```

---

Files:

- M `src/codegen/assembler.cc`
- M `src/codegen/assembler.h`
- M `src/compiler/backend/arm/code-generator-arm.cc`
- M `src/compiler/backend/arm64/code-generator-arm64.cc`
- M `src/compiler/backend/x64/code-generator-x64.cc`
- M `src/maglev/maglev-ir.cc`
- M `src/objects/instruction-stream-inl.h`
- M `src/objects/instruction-stream.cc`
- M `src/objects/instruction-stream.h`

---

Hash: [5fc1531adc3bfb61d08ae850eed408c2aa40fa2c](https://chromiumdash.appspot.com/commit/5fc1531adc3bfb61d08ae850eed408c2aa40fa2c)  

Date: Fri Mar 20 03:50:34 2026


---

### pe...@google.com (2026-03-24)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dx...@google.com (2026-03-25)

Project: v8/v8  

Branch:  main  

Author:  LuYahan [yahan@iscas.ac.cn](mailto:yahan@iscas.ac.cn)  

Link:    <https://chromium-review.googlesource.com/7695807>

[riscv][turboshaft] Direct call for known functions

---


Expand for full commit details
```
     
    Port commit 5d6a71b10abe3348f6efd1428ef5d29da9bf79af 
    Port commit b5db50f99bc02b1713a28c1718c4bd666264c9e7 
     
    Bug: 489633232 
    Change-Id: I9b259f36b5befba78b2f2dc5f0c846e63d294b2a 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7695807 
    Reviewed-by: Ji Qiu <qiuji@iscas.ac.cn> 
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    Commit-Queue: Yahan Lu (LuYahan) <yahan@iscas.ac.cn> 
    Cr-Commit-Position: refs/heads/main@{#106015}

```

---

Files:

- M `src/compiler/backend/instruction-selector.cc`
- M `src/compiler/backend/riscv/code-generator-riscv.cc`

---

Hash: [b46324c506362f4fcb2f8f761dbaaf8be145812f](https://chromiumdash.appspot.com/commit/b46324c506362f4fcb2f8f761dbaaf8be145812f)  

Date: Tue Mar 24 08:11:00 2026


---

### dx...@google.com (2026-03-27)

Project: v8/v8  

Branch:  refs/branch-heads/14.7  

Author:  Liu Yu [liuyu@loongson.cn](mailto:liuyu@loongson.cn)  

Link:    <https://chromium-review.googlesource.com/7707472>

Merged:[loong64][sandbox] Check dispatch entry in code finalization

---


Expand for full commit details
```
     
    Port commit b5db50f99bc02b1713a28c1718c4bd666264c9e7 
     
    Bug: 489633232 
     
    (cherry picked from commit 01f03c952c7274fd1bb7169a40df1400c047668e) 
     
    Change-Id: I3a44607cac30d77c60eb0647e800a0e44da203a9 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7707472 
    Auto-Submit: Liu Yu <liuyu@loongson.cn> 
    Commit-Queue: Liu Yu <liuyu@loongson.cn> 
    Reviewed-by: Victor Gomes <victorgomes@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.7@{#18} 
    Cr-Branched-From: 723547b98d2e75cb85556ab85479688c9fbe2f1e-refs/heads/14.7.173@{#1} 
    Cr-Branched-From: 3fc49d4c4cd9e6202fe21f5925899292ffadb20a-refs/heads/main@{#105661}

```

---

Files:

- M `src/compiler/backend/loong64/code-generator-loong64.cc`

---

Hash: [0d1a9068008a710dd4d3201a8110700d4d74803c](https://chromiumdash.appspot.com/commit/0d1a9068008a710dd4d3201a8110700d4d74803c)  

Date: Tue Mar 24 06:20:13 2026


---

### dx...@google.com (2026-03-27)

Project: v8/v8  

Branch:  refs/branch-heads/14.6  

Author:  Liu Yu [liuyu@loongson.cn](mailto:liuyu@loongson.cn)  

Link:    <https://chromium-review.googlesource.com/7707473>

Merged:[loong64][sandbox] Check dispatch entry in code finalization

---


Expand for full commit details
```
     
    Port commit b5db50f99bc02b1713a28c1718c4bd666264c9e7 
     
    Bug: 489633232 
     
    (cherry picked from commit 01f03c952c7274fd1bb7169a40df1400c047668e) 
     
    Change-Id: I10a1fb9a0137be867d7a015df6130ed923076e4e 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7707473 
    Auto-Submit: Liu Yu <liuyu@loongson.cn> 
    Reviewed-by: Victor Gomes <victorgomes@chromium.org> 
    Commit-Queue: Liu Yu <liuyu@loongson.cn> 
    Cr-Commit-Position: refs/branch-heads/14.6@{#57} 
    Cr-Branched-From: e04c3a1a2543bdbee7beac8846c9cbe8f657636f-refs/heads/14.6.202@{#1} 
    Cr-Branched-From: 3b0b01e6594ec362369dc16f069012a81748c8ba-refs/heads/main@{#105132}

```

---

Files:

- M `src/compiler/backend/loong64/code-generator-loong64.cc`

---

Hash: [4d9e52ffe8b3c96539b1b9025b7ebe820795bdbf](https://chromiumdash.appspot.com/commit/4d9e52ffe8b3c96539b1b9025b7ebe820795bdbf)  

Date: Tue Mar 24 06:20:13 2026


---

### vi...@google.com (2026-03-31)

For M138 LTS, the two CLs containing the fix introduce conflicts that would require a large number of dependent CLs to resolve, including the fix for [processing of JSDispatch handle through RelocInfo](https://chromium-review.googlesource.com/c/v8/v8/+/6939390) which appears to be a substantial work. Given that this dependency chain is unsafe to merge into LTS, I’m labeling it as not applicable for the M138 LTS.

### vi...@google.com (2026-04-17)

I’ve labeled as not applicable also for M144 LTS because “Check dispatch entry in code finalization” introduces conflicts related to the conversion of [JSDispatchTable from per-isolate-group to per-isolate](https://chromium-review.git.corp.google.com/c/v8/v8/+/7486426) that might bring a instability for the LTS version.

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $20000.00 for this report.

Rationale for this decision:
Controlled v8 sandbox escape.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/489633232)*
