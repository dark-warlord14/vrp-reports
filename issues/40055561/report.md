# missing the -0 case in VisitSpeculativeIntegerAdditiveOp

| Field | Value |
|-------|-------|
| **Issue ID** | [40055561](https://issues.chromium.org/issues/40055561) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | l....@gmail.com |
| **Assignee** | ne...@chromium.org |
| **Created** | 2021-04-15 |
| **Bounty** | $15,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36

Steps to reproduce the problem:
function foo(a) {
    var x = -0;
    if (a) {
        x = 0;
    }
    return x + (x - 0);
}
%PrepareFunctionForOptimization(foo);
console.log(Object.is(foo(true),0));
%OptimizeFunctionOnNextCall(foo);
console.log(Object.is(foo(false),-0));

./d8 --allow-natives-syntax --jitless test.js
true
true

./d8 --allow-natives-syntax test.js
true
false

What is the expected behavior?

What went wrong?
In the Simplified Lowering phase VisitSpeculativeIntegerAdditiveOp ignore the case where the right operand is -0.

The faulty code is within the simplified-lowering.cc file here:

https://source.chromium.org/chromium/chromium/src/+/master:v8/src/compiler/simplified-lowering.cc;l=1517

No distinction is made between 0 and -0 for the right operand.

Did this work before? N/A 

Chrome version: 89.0.4389.114  Channel: n/a
OS Version: OS X 11.2.3
Flash Version:

## Timeline

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### es...@chromium.org (2021-04-15)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript>Compiler]

### ne...@google.com (2021-04-16)

[Empty comment from Monorail migration]

### ne...@google.com (2021-04-16)

[Empty comment from Monorail migration]

### ne...@google.com (2021-04-16)

[Empty comment from Monorail migration]

### ne...@google.com (2021-04-16)

Thanks for the report. This bug is very subtle.

### ne...@google.com (2021-04-16)

It is closely related to https://crbug.com/chromium/1150649.

### gi...@appspot.gserviceaccount.com (2021-04-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/9313c4ce3f32ad81df1c65becccec7e129181ce3

commit 9313c4ce3f32ad81df1c65becccec7e129181ce3
Author: Georg Neis <neis@chromium.org>
Date: Fri Apr 16 12:31:27 2021

[compiler] Fix a bug in VisitSpeculativeIntegerAdditiveOp

Bug: chromium:1199345
Change-Id: I33bf71b33f43919fec4684054b5bf0a0787930ca
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2831478
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Commit-Queue: Georg Neis <neis@chromium.org>
Cr-Commit-Position: refs/heads/master@{#74008}

[modify] https://crrev.com/9313c4ce3f32ad81df1c65becccec7e129181ce3/src/compiler/simplified-lowering.cc


### [Deleted User] (2021-04-16)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ne...@chromium.org (2021-04-19)

[Empty comment from Monorail migration]

### ne...@chromium.org (2021-04-19)

Fix is in today's canary.

### [Deleted User] (2021-04-19)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-19)

[Empty comment from Monorail migration]

### go...@chromium.org (2021-04-19)

+adetaylor@ (Security TPM) for M90 and M91 merge review. Thank you.

### [Deleted User] (2021-04-19)

[Empty comment from Monorail migration]

### ad...@google.com (2021-04-19)

Approving merge to M91.

### gi...@appspot.gserviceaccount.com (2021-04-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/f45c842fe1b011f7fde237112067dcc999b71dd3

commit f45c842fe1b011f7fde237112067dcc999b71dd3
Author: Georg Neis <neis@chromium.org>
Date: Tue Apr 20 11:39:28 2021

Merged: [compiler] Fix a bug in VisitSpeculativeIntegerAdditiveOp

Revision: 9313c4ce3f32ad81df1c65becccec7e129181ce3

BUG=chromium:1199345
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=nicohartmann@chromium.org

Change-Id: Ibfd303d48319f3996d85234514681068a8691497
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2839558
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Commit-Queue: Georg Neis <neis@chromium.org>
Cr-Commit-Position: refs/branch-heads/9.1@{#24}
Cr-Branched-From: 0e4ac64a8cf298b14034a22f9fe7b085d2cb238d-refs/heads/9.1.269@{#1}
Cr-Branched-From: f565e72d5ba88daae35a59d0f978643e2343e912-refs/heads/master@{#73847}

[modify] https://crrev.com/f45c842fe1b011f7fde237112067dcc999b71dd3/src/compiler/simplified-lowering.cc


### ne...@chromium.org (2021-04-20)

[Empty comment from Monorail migration]

### ne...@chromium.org (2021-04-20)

Re https://crbug.com/chromium/1199345#c12:
1) yes
2) https://chromium.googlesource.com/v8/v8/+/9313c4ce3f32ad81df1c65becccec7e129181ce3
3) yes
4) yes
5) security bug fix
6) no

### ad...@google.com (2021-04-20)

Approving merge to M90.

### gi...@appspot.gserviceaccount.com (2021-04-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/aa2154a9c1383a07511d9d56dcd7accbb5d9d00d

commit aa2154a9c1383a07511d9d56dcd7accbb5d9d00d
Author: Georg Neis <neis@chromium.org>
Date: Tue Apr 20 11:48:07 2021

Merged: [compiler] Fix a bug in VisitSpeculativeIntegerAdditiveOp

Revision: 9313c4ce3f32ad81df1c65becccec7e129181ce3

BUG=chromium:1199345
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=nicohartmann@chromium.org

Change-Id: I0ee9f13815b1a7d248d4caa506c6930697e1866c
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2839559
Commit-Queue: Georg Neis <neis@chromium.org>
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Cr-Commit-Position: refs/branch-heads/9.0@{#41}
Cr-Branched-From: bd0108b4c88e0d6f2350cb79b5f363fbd02f3eb7-refs/heads/9.0.257@{#1}
Cr-Branched-From: 349bcc6a075411f1a7ce2d866c3dfeefc2efa39d-refs/heads/master@{#73001}

[modify] https://crrev.com/aa2154a9c1383a07511d9d56dcd7accbb5d9d00d/src/compiler/simplified-lowering.cc


### ne...@chromium.org (2021-04-20)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-04-23)

Congratulations! The VRP Panel has decided to award you $15,000 for this report. Nice work and thank for reporting this issue to us!

### l....@gmail.com (2021-04-23)

[Comment Deleted]

### am...@chromium.org (2021-04-23)

Thanks for the info - I've updated our records accordingly! 

### am...@chromium.org (2021-04-23)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-23)

[Empty comment from Monorail migration]

### as...@google.com (2021-04-26)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-26)

[Empty comment from Monorail migration]

### gi...@google.com (2021-04-27)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-04-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/ab2340a9b99409c94553eea0f79eed0e19903107

commit ab2340a9b99409c94553eea0f79eed0e19903107
Author: Georg Neis <neis@chromium.org>
Date: Fri Apr 16 12:31:27 2021

M86-LTS: [compiler] Fix a bug in VisitSpeculativeIntegerAdditiveOp

(cherry picked from commit 9313c4ce3f32ad81df1c65becccec7e129181ce3)

No-Try: true
No-Presubmit: true
No-Tree-Checks: true
Bug: chromium:1199345
Change-Id: I33bf71b33f43919fec4684054b5bf0a0787930ca
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2831478
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Commit-Queue: Georg Neis <neis@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#74008}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2848412
Commit-Queue: Artem Sumaneev <asumaneev@google.com>
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/8.6@{#86}
Cr-Branched-From: a64aed2333abf49e494d2a5ce24bbd14fff19f60-refs/heads/8.6.395@{#1}
Cr-Branched-From: a626bc036236c9bf92ac7b87dc40c9e538b087e3-refs/heads/master@{#69472}

[modify] https://crrev.com/ab2340a9b99409c94553eea0f79eed0e19903107/src/compiler/simplified-lowering.cc


### as...@google.com (2021-04-27)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-30)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-06-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/928da8091fc9612a22f64015938f692a2bae8bb7

commit 928da8091fc9612a22f64015938f692a2bae8bb7
Author: Georg Neis <neis@chromium.org>
Date: Fri Jun 04 07:49:34 2021

[compiler] Add a few regression tests

Tbr: nicohartmann@chromium.org
Bug: chromium:1198705, chromium:1199345, chromium:1200490
Change-Id: I4a486df636e084279423e6cd3b867137bfe3fd6f
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2939984
Reviewed-by: Georg Neis <neis@chromium.org>
Commit-Queue: Georg Neis <neis@chromium.org>
Cr-Commit-Position: refs/heads/master@{#74945}

[add] https://crrev.com/928da8091fc9612a22f64015938f692a2bae8bb7/test/mjsunit/compiler/regress-1198705.js
[add] https://crrev.com/928da8091fc9612a22f64015938f692a2bae8bb7/test/mjsunit/compiler/regress-1199345.js
[add] https://crrev.com/928da8091fc9612a22f64015938f692a2bae8bb7/test/mjsunit/compiler/regress-1200490.js


### [Deleted User] (2021-08-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1199345?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055561)*
