# Security: V8: Incorrect type information on SpeculativeSafeIntegerSubtract

| Field | Value |
|-------|-------|
| **Issue ID** | [40093360](https://issues.chromium.org/issues/40093360) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ja...@gmail.com |
| **Assignee** | na...@google.com |
| **Created** | 2018-12-10 |
| **Bounty** | $5,000.00 |

## Description

== VULNERABILITY DETAILS ==

The typer sets the type of SpeculativeSafeIntegerSubtract to an
intersection with kSafeInteger. This is missing the -0 case. In
particular, ((-0) - 0) should return (-0), but due to the
intersection, the typer ignores this return value. This can be used to
perform buggy range calculations, which can be used to perform a
"standard" exploit (explained below) using CheckBounds elimination to
obtain an OOB RW primitive.

Suggested Security Severity: High (at least as per my understanding of
the severity guidelines at [SevGuid]).

== VERSION ==

This bug has been in v8 since Nov 2017 or earlier (see [specAddfix]),
and can be triggered on practically all recent versions of v8 (i.e.,
any release in the past year or so).

== REPRODUCTION CASE ==

Run via `d8 --allow-natives-syntax`:

```
function foo(trigger) {
  return Object.is((trigger ? -0 : 0) - 0, -0);
}

console.log(foo(false));
%OptimizeFunctionOnNextCall(foo);
console.log(foo(true)); // expected: true, got: false
```

To test on Chrome instead:

```
function foo(trigger) {
  return Object.is((trigger ? -0 : 0) - 0, -0);
}

console.log(foo(false));
for(var i=10000000;i>0;--i){foo(false);}
console.log(foo(true)); // expected: true, got: false
```

== EXPLOITATION ==

As demonstrated by the bug discovered by Project Zero at [p0bug],
incorrect handling of minus-zero within the typer can be used (via the
simplified lowering phase, after moving past the typer and load
elimination phases which also perform typing), to create a SameValue
node (via Object.is) which will propagate the feedback type which will
then be used for (buggy) range calculations. We can then use this
result for the standard exploit using CheckBounds elimination to
obtain an OOB RW primitive, via a JS array.

== PROPOSED FIX ==

The fix for this is a one-line change:

```
--- a/src/compiler/operation-typer.cc
+++ b/src/compiler/operation-typer.cc
@@ -684,3 +684,3 @@ Type OperationTyper::SpeculativeSafeIntegerSubtract(Type lhs, Type rhs) {
   // SimplifiedLowering::VisitSpeculativeAdditiveOp.
-  return result = Type::Intersect(result, cache_.kSafeInteger, zone());
+  return result = Type::Intersect(result, cache_.kSafeIntegerOrMinusZero, zone());
 }
```

PS: I believe the `result =` is not necessary and can be removed (but
I didn't include it in the diff, since it is irrelevant to the
discussion).

== HOW BUG WAS FOUND + HISTORICAL ANALYSIS ==

The bug described above was found during a source-review, when I
noticed that there was a discrepancy between the preceding function
(for addition) and this. Upon looking at the git history, I noticed a
relevant fix made in the preceding function
(i.e. `OperationTyper::SpeculativeSafeIntegerAdd`) on Nov 16, 2017
(see [specAddFix]). The commit message indicated that the aim was to
have also fixed `SpeculativeSafeIntegerSubtract`, but this seems to
have been missed somehow, and this bug has been lying dormant for at
least a year.

== CREDIT INFORMATION ==

Reporter Credit: Jay Bosamiya

== LINKS ==

+ [SevGuid] https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md
+ [p0bug] https://bugs.chromium.org/p/project-zero/issues/detail?id=1710
+ [specAddFix] https://chromium.googlesource.com/v8/v8/+/82271defd67347c146a3f71d3aad313f00658b48


## Timeline

### cl...@chromium.org (2018-12-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5653527340515328.

### cl...@chromium.org (2018-12-10)

Testcase 5653527340515328 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5653527340515328.

### cl...@chromium.org (2018-12-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6258808692932608.

### mm...@chromium.org (2018-12-10)

Thanks for your report. I'm having troubles reproducing it. Could you please specify a particular build / revision which it can be reproduced on?

### cl...@chromium.org (2018-12-10)

Testcase 6258808692932608 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6258808692932608.

### mm...@chromium.org (2018-12-10)

While waiting for the feedback from the reporting, assigning V8 component to pass this over to V8 sheriff. Also CC'd some folks who were mentioned in the bug / CL from c#0.

[Monorail components: Blink>JavaScript]

### mm...@chromium.org (2018-12-10)

[Empty comment from Monorail migration]

### ja...@gmail.com (2018-12-11)

I believe that the reason ClusterFuzz was unable to reproduce it is
because I used `console.log` to demonstrate the values, rather than
using `assertEquals` which the test-case format expects.

I have thus rewritten the testcase in a format that can be used within
the `v8/test/` directory to demonstrate the bug:

```
function foo(trigger) {
  return (trigger ? -0 : 0) - 0;
}

assertEquals(0, foo(false));
%OptimizeFunctionOnNextCall(foo);
assertEquals(-0, foo(true)); // Failure: expected <-0> found <0>
```

For the above (as well as what I had provided in my original report),
I annotated with a comment demonstrating the point of failure.

As I mentioned in my original report, the particular build / revision
should not be relevant, since this bug has been around since 2017. In
fact, I am able to reproduce this both on master, as well as the
default Chromium build on Debian Stretch (71.0.3578.80 ; with v8
7.1.302.28).

To clarify, my testcase does NOT produce a crash, and is minimized to
highlight the actual issue itself. In order to produce a crash and
build an exploit, one would need to follow the exploit steps as
written in my original report.

I hope that helps understand this better. Please do not hesitate to
ask for further clarification.

### sh...@chromium.org (2018-12-11)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@google.com (2018-12-11)

Thanks for the clarifications, Jay!

### mm...@google.com (2018-12-11)

[Empty comment from Monorail migration]

### bm...@chromium.org (2018-12-11)

Great catch! And also thanks for digging into this already. The fix is correct, but it needs an additional update to SimplifiedLowering handling of SpeculativeSafeIntegerSubtract. I've uploaded a fix at https://chromium-review.googlesource.com/c/v8/v8/+/1370042

[Monorail components: -Blink>JavaScript Blink>JavaScript>Compiler]

### bu...@chromium.org (2018-12-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/e3c923962677908c183121644c945777cdb31570

commit e3c923962677908c183121644c945777cdb31570
Author: Benedikt Meurer <bmeurer@chromium.org>
Date: Tue Dec 11 10:21:35 2018

[turbofan] Fix wrong typing of SpeculativeSafeIntegerSubtract.

The typing of SpeculativeSafeIntegerSubtract didn't include -0, and the
SimplifiedLowering rules for SpeculativeSafeIntegerSubtract didn't
properly handle the case of `-0 - 0`, but would always pass Word32
truncations.

Bug: chromium:913296
Change-Id: I0e5a401f075db8b349a5579e1e294df97378ea49
Reviewed-on: https://chromium-review.googlesource.com/c/1370042
Reviewed-by: Tobias Tebbi <tebbi@chromium.org>
Commit-Queue: Benedikt Meurer <bmeurer@chromium.org>
Cr-Commit-Position: refs/heads/master@{#58147}
[modify] https://crrev.com/e3c923962677908c183121644c945777cdb31570/src/compiler/operation-typer.cc
[modify] https://crrev.com/e3c923962677908c183121644c945777cdb31570/src/compiler/simplified-lowering.cc
[add] https://crrev.com/e3c923962677908c183121644c945777cdb31570/test/mjsunit/regress/regress-crbug-913296.js


### bm...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-11)

This bug requires manual review: Request affecting a post-stable build
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-12-11)

+ awhalley@ & hablich@ (Security TPM and V8 TPM) for M71 & M72 merge review. This change is not yet baked in canary, landed 5 hrs back. So we won't be able to take for this week M71 stable respin.

### sh...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-12)

Your change meets the bar and is auto-approved for M72. Please go ahead and merge the CL to branch 3626 manually. Please contact milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), djmm@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2018-12-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/413c2e787197063abd8435d9692355eb8693ad39

commit 413c2e787197063abd8435d9692355eb8693ad39
Author: Benedikt Meurer <bmeurer@google.com>
Date: Wed Dec 12 11:55:03 2018

Merged: [turbofan] Fix wrong typing of SpeculativeSafeIntegerSubtract.

Revision: e3c923962677908c183121644c945777cdb31570

BUG=chromium:913296
LOG=N
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=jarin@chromium.org

Change-Id: I8580f60c6ae6ee586c65714afebf0d8c3ae2e973
Reviewed-on: https://chromium-review.googlesource.com/c/1373772
Reviewed-by: Jaroslav Sevcik <jarin@chromium.org>
Cr-Commit-Position: refs/branch-heads/7.2@{#21}
Cr-Branched-From: 6acd03c9b8a8232aee95f25fbf6ae822aaedae75-refs/heads/7.2.502@{#1}
Cr-Branched-From: b03041de094610ef24e0e4fb6bf4c700fa1553ed-refs/heads/master@{#57910}
[modify] https://crrev.com/413c2e787197063abd8435d9692355eb8693ad39/src/compiler/operation-typer.cc
[modify] https://crrev.com/413c2e787197063abd8435d9692355eb8693ad39/src/compiler/simplified-lowering.cc
[add] https://crrev.com/413c2e787197063abd8435d9692355eb8693ad39/test/mjsunit/regress/regress-crbug-913296.js


### go...@chromium.org (2018-12-13)

Pls merge your change to M72 branch 3626 ASAP. Thank you.

### go...@chromium.org (2018-12-13)

Pls merge your change to M72 branch 3626 ASAP so we can pick it up for next M72 Beta release. Thank you.

### sh...@chromium.org (2018-12-17)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-12-17)

Pls merge your change to M72 branch 3626 ASAP so we can pick it up for this week beta release, RC cut tomorrow, Tuesday @ 1:00 PM PT.

### aw...@google.com (2018-12-17)

Merged in https://crbug.com/chromium/913296#c19

### na...@google.com (2018-12-17)

[Empty comment from Monorail migration]

### bm...@chromium.org (2018-12-17)

M71 merge review pending. Assigning to jarin@ since I'm OOO.

### go...@chromium.org (2018-12-17)

Removing "Merge-Approved-72" label per https://crbug.com/chromium/913296#c24.

### na...@google.com (2018-12-20)

delphick@chromium.org - Please take a look 

### de...@chromium.org (2018-12-20)

Not sure why you've assigned this to me.

### go...@chromium.org (2019-01-02)

hablich@/awhalley@ for M71 merge review (Note: At the moment there is no plan for M71 respin for Desktop).

### na...@google.com (2019-01-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### pa...@chromium.org (2019-01-10)

Thanks for your report. The panel has decided to reward $5,000 :) 

Since you are a new reporter a member of our finance will be in touch. 

Additionally, how would you like to be credited in release notes?


### na...@google.com (2019-01-10)

[Empty comment from Monorail migration]

### ja...@gmail.com (2019-01-10)

Thanks for the reward :)

"Reported by Jay Bosamiya" should be sufficient for credit in release notes.

### go...@chromium.org (2019-01-18)




We're not planning any further M71 release, rejecting merge to M71.


### aw...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-02-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-03-19)

This issue was migrated from crbug.com/chromium/913296?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-07)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/chrome-blintz-user-guide

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093360)*
