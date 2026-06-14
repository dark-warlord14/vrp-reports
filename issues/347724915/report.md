# Segfault in v8 in Builtins_JSConstructStubGeneric

| Field | Value |
|-------|-------|
| **Issue ID** | [347724915](https://issues.chromium.org/issues/347724915) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Turbofan, Blink>JavaScript>Runtime |
| **Platforms** | Linux |
| **Reporter** | s0...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2024-06-17 |
| **Bounty** | $7,000.00 |

## Description

## VULNERABILITY DETAILS

Fuzzing revealed a segmentation fault in LTS version of V8. Please find details below. It can be reproduced easily by running the file attached against d8 using the command: d8 --expose-gc --omit-quit --future --harmony --assert-types --harmony-struct --allow-natives-syntax --interrupt-budget=1000 --fuzzing program\_20240616125405\_DD3686A2-ED9F-413D-AAE3-0D69F7A03569\_deterministic.js

Compiled v8 with: `gn gen out/fuzzbuild --args='is_debug=false dcheck_always_on=true v8_static_library=true v8_enable_verify_heap=true v8_fuzzilli=true sanitizer_coverage_flags="trace-pc-guard" target_cpu="x64"'`

## VERSION

Chrome Version: LTS
Operating System: Ubuntu 22.04

## REPRODUCTION CASE

```
for (let v0 = 0; v0 < 83; v0++) {
    function F1(a3, a4, a5, a6) {
        if (!new.target) { throw 'must be called with new'; }
        const v8 = ("number").source;
        function F9(a11, a12, ...a13) {
            if (!new.target) { throw 'must be called with new'; }
            a13[0];
            try {
                const v15 = new F9(a12, ...a13, F9);
            } catch(e16) {
            }
        }
        const v17 = new F9(F9, v8, v8);
    }
    const v18 = new F1();
}

```
## FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: browser

### Crash State:

```
// CRASH INFO
// ==========
// TERMSIG: 11
// STDERR:
// [COV] edge counters initialized. Shared memory: shm_id_1188638_23 with 1366912 edges
// V8 is running with experimental features enabled. Stability and security will suffer.
// Received signal 11 SEGV_ACCERR 22e4beadbef6
//
// ==== C stack trace ===============================
//
//  [0x55f77b30553d]
//  [0x7fea9490b520]
//  [0x55f77eae86a1]
// [end of stack trace]


```

Client ID (if relevant): N/A

## CREDIT INFORMATION

Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: 2ourc3 | Salim Largo

## Attachments

- [program_20240617070556_F7F6F4E5-F138-431A-BC27-3D3FE1A25E51_deterministic.fuzzil.protobuf](attachments/program_20240617070556_F7F6F4E5-F138-431A-BC27-3D3FE1A25E51_deterministic.fuzzil.protobuf) (application/octet-stream, 847 B)
- [program_20240617070556_F7F6F4E5-F138-431A-BC27-3D3FE1A25E51_deterministic.js](attachments/program_20240617070556_F7F6F4E5-F138-431A-BC27-3D3FE1A25E51_deterministic.js) (text/javascript, 1.2 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-06-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5080645083529216.

### 24...@project.gserviceaccount.com (2024-06-17)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2024-06-17)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/3ecb8552efcc92b7a443b10939d99e04d5ba4cd6 ([turboshaft] Enable late load elimination by default

Bug: 42202729
Change-Id: I0f65c7662c057fb599addf661ca888318aaefc61
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5522500
Auto-Submit: Darius Mercadier <dmercadier@chromium.org>
Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Cr-Commit-Position: refs/heads/main@{#93789}
).

If this is incorrect, please let us know why and apply the hotlistid:5433122. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### 24...@project.gserviceaccount.com (2024-06-17)

Detailed Report: https://clusterfuzz.com/testcase?key=5080645083529216

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7e9ebeadbeec
Crash State:
  void v8::internal::Print<
  v8::internal::CheckObjectType
  Builtins_TestTurbofanType
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=93788:93789

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5080645083529216

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### dm...@chromium.org (2024-06-18)

Some explanations of what's happening:

We start with a graph that looks like:

```
x = LoadStackArgument(a, 40)
...
Allocate()
...
y = LoadStackArgument(a, 40)

```

This was then lowered to

```
x1 = Load<WordPtr>(...)
x2 = TaggedBitcast(x1, WordPtr->Tagged)
...
Allocate()
...
y1 = Load<WordPtr>(...)
y2 = TaggedBitcast(y1, WordPtr->Tagged)

```

Then, Turboshaft's Load Elimination removed the second Load (since it's identical to the 1st one), and we ended up with:

```
x1 = Load<WordPtr>(...)
x2 = TaggedBitcast(x1, WordPtr->Tagged)
...
Allocate()
...
y2 = TaggedBitcast(x1, WordPtr->Tagged)

```

And now we are in trouble: if the allocation in the middle triggers a GC, then `x1` could move, and thus `y2` could refer to a stale pointer. In theory, Turbofan knows where tagged values are, and can thus update them when the GC moves things, but here, `x1` is not marked as Tagged (but rather as a raw WordPtr).

The fix is to do a Tagged load from the start (rather than doing a WordPtr load + a Tagged bitcast), since anyways we are clearly loading a tagged thing. CL in progress...

Regarding exploitability: this bug leads to some kind of type confusion in Turbofan, and I'm guessing that it's exploitable. We'll need to backmerge the fix (this has always been broken, so we can backmerge as far as possible).

### pe...@google.com (2024-06-18)

Setting milestone because of s2 severity.

### pe...@google.com (2024-06-18)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ap...@google.com (2024-06-19)

Project: v8/v8
Branch: main

commit cdbc1d9684a3602c77c39d23b4e95a8522a0cc90
Author: Darius Mercadier <dmercadier@chromium.org>
Date:   Tue Jun 18 16:10:26 2024

    [turboshaft] Lower LoadStackArgument to a Tagged load
    
    If we start with a graph that looks like
    
    ```
    x = LoadStackArgument(a, 40)
    ...
    Allocate()
    ...
    y = LoadStackArgument(a, 40)
    ```
    
    This used to be lowered to
    
    ```
    x1 = Load<WordPtr>(a, 40)
    x2 = TaggedBitcast(x1, WordPtr->Tagged)
    ...
    Allocate()
    ...
    y1 = Load<WordPtr>(a, 40)
    y2 = TaggedBitcast(y1, WordPtr->Tagged)
    ```
    
    And then, Load Elimination would remove the second Load, and we'd get:
    
    ```
    x1 = Load<WordPtr>(a, 40)
    x2 = TaggedBitcast(x1, WordPtr->Tagged)
    ...
    Allocate()
    ...
    y2 = TaggedBitcast(x1, WordPtr->Tagged)
    ```
    
    And now we would be in trouble: if the allocation in the middle
    triggers a GC, then `x1` could move, and thus `y2` could refer to a
    stale pointer. In theory, Turbofan knows where tagged values are, and
    can thus update them when the GC moves things, but here, `x1` is not
    marked as Tagged (but rather as a raw WordPtr).
    
    This CL fixes this issue by doing a Tagged load from the start, since
    the value we're loading is clearly tagged.
    
    Fixed: chromium:347724915
    Change-Id: Ia659155fbc602907ab9a50fb992c79df6ccdaa44
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5630530
    Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
    Auto-Submit: Darius Mercadier <dmercadier@chromium.org>
    Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#94527}

M       src/compiler/access-builder.cc
M       src/compiler/access-builder.h
M       src/compiler/turboshaft/machine-lowering-reducer-inl.h
A       test/mjsunit/compiler/regress-347724915.js

https://chromium-review.googlesource.com/5630530


### s0...@gmail.com (2024-06-19)

Dears, thanks for your prompt investigation. Is this eligible for CVE/reward? Cheers!

### ap...@google.com (2024-06-19)

Project: v8/v8
Branch: main

commit 715dcc9905fc5d4647cb8817d467a591bc21eace
Author: Leszek Swirski <leszeks@chromium.org>
Date:   Wed Jun 19 11:02:59 2024

    Revert "[turboshaft] Lower LoadStackArgument to a Tagged load"
    
    This reverts commit cdbc1d9684a3602c77c39d23b4e95a8522a0cc90.
    
    Reason for revert: New test breaks on single generation bot: https://ci.chromium.org/ui/p/v8/builders/ci/V8%20Linux64%20-%20debug%20-%20single%20generation/15458/overview
    
    Original change's description:
    > [turboshaft] Lower LoadStackArgument to a Tagged load
    >
    > If we start with a graph that looks like
    >
    > ```
    > x = LoadStackArgument(a, 40)
    > ...
    > Allocate()
    > ...
    > y = LoadStackArgument(a, 40)
    > ```
    >
    > This used to be lowered to
    >
    > ```
    > x1 = Load<WordPtr>(a, 40)
    > x2 = TaggedBitcast(x1, WordPtr->Tagged)
    > ...
    > Allocate()
    > ...
    > y1 = Load<WordPtr>(a, 40)
    > y2 = TaggedBitcast(y1, WordPtr->Tagged)
    > ```
    >
    > And then, Load Elimination would remove the second Load, and we'd get:
    >
    > ```
    > x1 = Load<WordPtr>(a, 40)
    > x2 = TaggedBitcast(x1, WordPtr->Tagged)
    > ...
    > Allocate()
    > ...
    > y2 = TaggedBitcast(x1, WordPtr->Tagged)
    > ```
    >
    > And now we would be in trouble: if the allocation in the middle
    > triggers a GC, then `x1` could move, and thus `y2` could refer to a
    > stale pointer. In theory, Turbofan knows where tagged values are, and
    > can thus update them when the GC moves things, but here, `x1` is not
    > marked as Tagged (but rather as a raw WordPtr).
    >
    > This CL fixes this issue by doing a Tagged load from the start, since
    > the value we're loading is clearly tagged.
    >
    > Fixed: chromium:347724915
    > Change-Id: Ia659155fbc602907ab9a50fb992c79df6ccdaa44
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5630530
    > Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
    > Auto-Submit: Darius Mercadier <dmercadier@chromium.org>
    > Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#94527}
    
    Change-Id: Iedbcd9eaa867b379b54a9f16ed6cd3dd1bc96f2b
    No-Presubmit: true
    No-Tree-Checks: true
    No-Try: true
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5641334
    Auto-Submit: Leszek Swirski <leszeks@chromium.org>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#94531}

M       src/compiler/access-builder.cc
M       src/compiler/access-builder.h
M       src/compiler/turboshaft/machine-lowering-reducer-inl.h
D       test/mjsunit/compiler/regress-347724915.js

https://chromium-review.googlesource.com/5641334


### ap...@google.com (2024-06-19)

Project: v8/v8
Branch: main

commit 96493c74c092f53c876d2e2944ff73edeea4f1bb
Author: Darius Mercadier <dmercadier@chromium.org>
Date:   Wed Jun 19 13:54:35 2024

    Reland "[turboshaft] Lower LoadStackArgument to a Tagged load"
    
    This is a reland of https://crrev.com/c/5630530.
    
    The reland disables the new unit tests when the single_generation
    variant is used, since SimulateNewspaceFull needs to young
    generation.
    
    Original CL description:
    > [turboshaft] Lower LoadStackArgument to a Tagged load
    >
    > If we start with a graph that looks like
    >
    > ```
    > x = LoadStackArgument(a, 40)
    > ...
    > Allocate()
    > ...
    > y = LoadStackArgument(a, 40)
    > ```
    >
    > This used to be lowered to
    >
    > ```
    > x1 = Load<WordPtr>(a, 40)
    > x2 = TaggedBitcast(x1, WordPtr->Tagged)
    > ...
    > Allocate()
    > ...
    > y1 = Load<WordPtr>(a, 40)
    > y2 = TaggedBitcast(y1, WordPtr->Tagged)
    > ```
    >
    > And then, Load Elimination would remove the second Load, and we'd get:
    >
    > ```
    > x1 = Load<WordPtr>(a, 40)
    > x2 = TaggedBitcast(x1, WordPtr->Tagged)
    > ...
    > Allocate()
    > ...
    > y2 = TaggedBitcast(x1, WordPtr->Tagged)
    > ```
    >
    > And now we would be in trouble: if the allocation in the middle
    > triggers a GC, then `x1` could move, and thus `y2` could refer to a
    > stale pointer. In theory, Turbofan knows where tagged values are, and
    > can thus update them when the GC moves things, but here, `x1` is not
    > marked as Tagged (but rather as a raw WordPtr).
    >
    > This CL fixes this issue by doing a Tagged load from the start, since
    > the value we're loading is clearly tagged.
    >
    > Fixed: chromium:347724915
    > Change-Id: Ia659155fbc602907ab9a50fb992c79df6ccdaa44
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5630530
    > Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
    > Auto-Submit: Darius Mercadier <dmercadier@chromium.org>
    > Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#94527}
    
    Change-Id: Icee612e84b5f160ff7b5e61bd9b0211561d9eebc
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5640925
    Auto-Submit: Darius Mercadier <dmercadier@chromium.org>
    Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
    Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#94541}

M       src/compiler/access-builder.cc
M       src/compiler/access-builder.h
M       src/compiler/turboshaft/machine-lowering-reducer-inl.h
A       test/mjsunit/compiler/regress-347724915.js
M       test/mjsunit/mjsunit.status

https://chromium-review.googlesource.com/5640925


### pe...@google.com (2024-06-19)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M127. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Merge review required: a reverted commit was detected after the merge request.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [127].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### dm...@chromium.org (2024-06-20)

Answers to [Comment #13](https://issues.chromium.org/issues/347724915#comment13):

1. <https://crrev.com/c/5640925>
2. Not yet. This landed in V8 yesterday, and is in Chrome 128.0.6547.0 (not yet Canary as of writing this).
3. no
4. no
5. no

### dm...@chromium.org (2024-06-20)

This has been broken pretty much forever (since at least 2020), and it's potentially exploitable, so we should probably also backmerge to Stable.
(I've tried to update the labels accordingly)

### 24...@project.gserviceaccount.com (2024-06-20)

ClusterFuzz testcase 5080645083529216 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=94540:94541

If this is incorrect, please add the hotlistid:5432646 and re-open the issue.

### am...@chromium.org (2024-06-20)

Since this was landed yesterday, I'd like this fix to get a bit more bake time on Canary for merge approval.
I'll revisit tomorrow or Monday for merge review.

### am...@chromium.org (2024-06-20)

re c#10, thank you for the report, Salim. Now that this issue is resolved, it will be assessed for a potential reward at a future VRP Panel session. There are some forthcoming holidays in the US, so please forgive us if there is a bit of delay in this.

I've noticed you have submitted other reports over the last couple of days and they all have the common trait of specifying an issue as impacting an LTS version of Chrome. Please note that LTS is not considered an active Chrome release channel. Only Dev, Beta, Stable, and Extended Stable are considered active release channels. If an issue *only* impacts LTS and not other, current active release channels (such as it was fixed between M120 (current LTS) and M126 (current Stable / Extended Stable) it would not be considered in scope for VRP, CVE, or as an active security issue.
In this case, this bug impacts other active release channels.

It would be helpful in future reports if you could please specify the active release channel version you used to find the bug and it can be reproduced on.
Thank you!

### s0...@gmail.com (2024-06-24)

Hi Amy, thanks for the feedback on my report. I'll definitely investigate further everything related to Google product so my future report are even better! Any ETA regarding the reward panel? Cheers!

### am...@chromium.org (2024-06-25)

Since there is an expressed potential for type confusion, elevating this to S1
Merges approved for <https://crrev.com/c/5640925>
please merge this fix to M126 Stable (branch 12.6) and M127 Beta (branch 12.7) at soonest by EOD tomorrow (25 June) so this fix can be included in the next Beta update.

This week's Stable update has already been released. Please merge this fix to 12.6 at soonest so this fix can be included in the next Stable update (following the forthcoming release freeze)

### ap...@google.com (2024-06-25)

Project: v8/v8
Branch: refs/branch-heads/12.7

commit 9ee8ef0a6b93078a705525c86a41c1d68adbf8f3
Author: Darius Mercadier <dmercadier@chromium.org>
Date:   Wed Jun 19 13:54:35 2024

    Merged: Reland "[turboshaft] Lower LoadStackArgument to a Tagged load"
    
    This is a reland of https://crrev.com/c/5630530.
    
    The reland disables the new unit tests when the single_generation
    variant is used, since SimulateNewspaceFull needs to young
    generation.
    
    Original CL description:
    > [turboshaft] Lower LoadStackArgument to a Tagged load
    >
    > If we start with a graph that looks like
    >
    > ```
    > x = LoadStackArgument(a, 40)
    > ...
    > Allocate()
    > ...
    > y = LoadStackArgument(a, 40)
    > ```
    >
    > This used to be lowered to
    >
    > ```
    > x1 = Load<WordPtr>(a, 40)
    > x2 = TaggedBitcast(x1, WordPtr->Tagged)
    > ...
    > Allocate()
    > ...
    > y1 = Load<WordPtr>(a, 40)
    > y2 = TaggedBitcast(y1, WordPtr->Tagged)
    > ```
    >
    > And then, Load Elimination would remove the second Load, and we'd get:
    >
    > ```
    > x1 = Load<WordPtr>(a, 40)
    > x2 = TaggedBitcast(x1, WordPtr->Tagged)
    > ...
    > Allocate()
    > ...
    > y2 = TaggedBitcast(x1, WordPtr->Tagged)
    > ```
    >
    > And now we would be in trouble: if the allocation in the middle
    > triggers a GC, then `x1` could move, and thus `y2` could refer to a
    > stale pointer. In theory, Turbofan knows where tagged values are, and
    > can thus update them when the GC moves things, but here, `x1` is not
    > marked as Tagged (but rather as a raw WordPtr).
    >
    > This CL fixes this issue by doing a Tagged load from the start, since
    > the value we're loading is clearly tagged.
    >
    > Fixed: chromium:347724915
    > Change-Id: Ia659155fbc602907ab9a50fb992c79df6ccdaa44
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5630530
    > Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
    > Auto-Submit: Darius Mercadier <dmercadier@chromium.org>
    > Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#94527}
    
    Bug: chromium:347724915
    (cherry picked from commit 96493c74c092f53c876d2e2944ff73edeea4f1bb)
    
    Change-Id: I2448728ac75b026f396af51b7caa3bdbc17b09c8
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5644921
    Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
    Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
    Auto-Submit: Darius Mercadier <dmercadier@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.7@{#16}
    Cr-Branched-From: 35cc908918d3f8083955ed8328506f964e17ae40-refs/heads/12.7.224@{#1}
    Cr-Branched-From: 6d60e6734b32211215c8410db6fe2b84b13abe0e-refs/heads/main@{#94324}

M       src/compiler/access-builder.cc
M       src/compiler/access-builder.h
M       src/compiler/turboshaft/machine-lowering-reducer-inl.h
A       test/mjsunit/compiler/regress-347724915.js
M       test/mjsunit/mjsunit.status

https://chromium-review.googlesource.com/5644921


### ap...@google.com (2024-06-25)

Project: v8/v8
Branch: refs/branch-heads/12.6

commit 5518d09994ebc7ffe18177d49bc787eddb396c75
Author: Darius Mercadier <dmercadier@chromium.org>
Date:   Wed Jun 19 13:54:35 2024

    Merged: Reland "[turboshaft] Lower LoadStackArgument to a Tagged load"
    
    This is a reland of https://crrev.com/c/5630530.
    
    The reland disables the new unit tests when the single_generation
    variant is used, since SimulateNewspaceFull needs to young
    generation.
    
    Original CL description:
    > [turboshaft] Lower LoadStackArgument to a Tagged load
    >
    > If we start with a graph that looks like
    >
    > ```
    > x = LoadStackArgument(a, 40)
    > ...
    > Allocate()
    > ...
    > y = LoadStackArgument(a, 40)
    > ```
    >
    > This used to be lowered to
    >
    > ```
    > x1 = Load<WordPtr>(a, 40)
    > x2 = TaggedBitcast(x1, WordPtr->Tagged)
    > ...
    > Allocate()
    > ...
    > y1 = Load<WordPtr>(a, 40)
    > y2 = TaggedBitcast(y1, WordPtr->Tagged)
    > ```
    >
    > And then, Load Elimination would remove the second Load, and we'd get:
    >
    > ```
    > x1 = Load<WordPtr>(a, 40)
    > x2 = TaggedBitcast(x1, WordPtr->Tagged)
    > ...
    > Allocate()
    > ...
    > y2 = TaggedBitcast(x1, WordPtr->Tagged)
    > ```
    >
    > And now we would be in trouble: if the allocation in the middle
    > triggers a GC, then `x1` could move, and thus `y2` could refer to a
    > stale pointer. In theory, Turbofan knows where tagged values are, and
    > can thus update them when the GC moves things, but here, `x1` is not
    > marked as Tagged (but rather as a raw WordPtr).
    >
    > This CL fixes this issue by doing a Tagged load from the start, since
    > the value we're loading is clearly tagged.
    >
    > Fixed: chromium:347724915
    > Change-Id: Ia659155fbc602907ab9a50fb992c79df6ccdaa44
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5630530
    > Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
    > Auto-Submit: Darius Mercadier <dmercadier@chromium.org>
    > Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#94527}
    
    Bug: chromium:347724915
    (cherry picked from commit 96493c74c092f53c876d2e2944ff73edeea4f1bb)
    
    Change-Id: Ib4cfc65a7b1fecd6b74ab522cf6765114e315a41
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5652660
    Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
    Auto-Submit: Darius Mercadier <dmercadier@chromium.org>
    Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.6@{#40}
    Cr-Branched-From: 3c9fa12db3183a6f4ea53d2675adb66ea1194529-refs/heads/12.6.228@{#2}
    Cr-Branched-From: 981bb15ba4dbf9e2381dfc94ec2c4af0b9c6a0b6-refs/heads/main@{#93835}

M       src/compiler/access-builder.cc
M       src/compiler/access-builder.h
M       src/compiler/turboshaft/machine-lowering-reducer-inl.h
A       test/mjsunit/compiler/regress-347724915.js
M       test/mjsunit/mjsunit.status

https://chromium-review.googlesource.com/5652660


### sp...@google.com (2024-06-28)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
report of memory corruption in a sandboxed process / renderer 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-28)

Congratulations Salim! Thank you for your efforts and reporting this issue to us -- nice work! 

### s0...@gmail.com (2024-06-28)

Yoohoo! Many thanks all :)

### pe...@google.com (2024-06-28)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dm...@chromium.org (2024-06-28)

All merges already done. I've removed the Merge-Approved labels.

### pe...@google.com (2024-09-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/347724915)*
