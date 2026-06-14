# Heap-use-after-free in blink::EventHandler::SelectAutoCursor

| Field | Value |
|-------|-------|
| **Issue ID** | [40087358](https://issues.chromium.org/issues/40087358) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>Input, Internals>Input |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cl...@chromium.org |
| **Assignee** | dt...@chromium.org |
| **Created** | 2017-04-17 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=6044738269741056

Fuzzer: miaubiz_svg_fuzzer
Job Type: windows_asan_chrome_no_sandbox
Platform Id: windows

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x083217e0
Crash State:
  blink::EventHandler::selectAutoCursor
  blink::EventHandler::selectCursor
  blink::EventHandler::handleMouseMoveOrLeaveEvent
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=windows_asan_chrome_no_sandbox&range=450347:450395

Reproducer Testcase: https://clusterfuzz.com/download/AMIfv95HWJoOerZOzUXiITqMJz-n_XUhLE3oN_YHhi-cQ46ADA9tJ-hfq5WcIJfIZ2dO9OOgd45H9Bk9DNn53dSug4IZFnmHWBHqFkuGYvb8fwA0HkXibqI0s24zyW98Wo5miGRMC3Ve8AM167M95dv3GXAwDaQXjCh4n2brmTC-qe8TBEq1MtQgNpPVPgxObEzwBRprWhkf0hw_BMKVIdDp1DlooYIsbFahpgRb8hFeli_oWfdnnJkD0MaG7g57QE0MApS_TGaXheg_9LdFs8he3ERUCf_Qhh7eH_KqcqdveNoxh8etEsIJe8swcKq-yThmQbiGgMd8KrCJt2bfZvISZKeX8bFD02wiUs40FQkxB1VjZ65JwK4?testcase_id=6044738269741056


Additional requirements: Requires Gestures

Issue filed automatically.

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### es...@chromium.org (2017-04-18)

yosin, could you please take a look? Maybe possibly related to d892f959 (it's in the regression range)?

[Monorail components: Internals>Input]

### sh...@chromium.org (2017-04-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-19)

[Empty comment from Monorail migration]

### go...@chromium.org (2017-04-19)

[Empty comment from Monorail migration]

### aw...@google.com (2017-04-19)

Too late for M58, pushing to 59.

### yo...@chromium.org (2017-04-27)

[Empty comment from Monorail migration]

### yo...@chromium.org (2017-04-27)

Lower to Pri-2, since this issue caused by unusual HTML.

### sh...@chromium.org (2017-04-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-27)

[Empty comment from Monorail migration]

### go...@chromium.org (2017-04-27)

+awhalley@, will this be a blocker for M58 Stable AU ramp up or respin?

### aw...@chromium.org (2017-04-27)

Nope - moving to 59.

### pa...@chromium.org (2017-04-28)

lanwei, any chance you could take a look? +some input/events OWNERS too.

[Monorail components: Blink>Input]

### dt...@chromium.org (2017-04-28)

Looks like https://cs.chromium.org/chromium/src/third_party/WebKit/Source/core/input/EventHandler.cpp?q=selectAutoCursor+package:%5Echromium$&l=564 can invalidate the LayoutObject ptr on the stack.

### dt...@chromium.org (2017-04-28)

[Empty comment from Monorail migration]

### dt...@chromium.org (2017-04-28)

This is caused by https://chromium.googlesource.com/chromium/src/+/d892f9592860691ae9a782c12260c94ed6bd1a63%5E%21/#F30

who added a layout inside the method EventHandler is using.

### dt...@chromium.org (2017-04-28)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-04-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9d6b6c40b933564260a0a70567b90ac30656222a

commit 9d6b6c40b933564260a0a70567b90ac30656222a
Author: dtapuska <dtapuska@chromium.org>
Date: Fri Apr 28 17:34:06 2017

Cleanup determining ibeam for node.

Change
https://chromium.googlesource.com/chromium/src/+/d892f9592860691ae9a782c12260c94ed6bd1a63%5E%21/#F30

caused the layout object to possibly be invalidated. Collapse the code
so that LayoutObject is correclty scoped so we don't run this risk.

BUG=712459

Review-Url: https://codereview.chromium.org/2849883002
Cr-Commit-Position: refs/heads/master@{#468045}

[modify] https://crrev.com/9d6b6c40b933564260a0a70567b90ac30656222a/third_party/WebKit/Source/core/input/EventHandler.cpp


### cl...@chromium.org (2017-04-28)

Detailed report: https://clusterfuzz.com/testcase?key=5494570986242048

Job Type: linux_asan_chrome_mp
Crash Type: 
Crash Address: 
Crash State:
  
Sanitizer: address (ASAN)

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5494570986242048


Additional requirements: Requires Gestures

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### cl...@chromium.org (2017-04-29)

ClusterFuzz has detected this issue as fixed in range 468030:468057.

Detailed report: https://clusterfuzz.com/testcase?key=6044738269741056

Fuzzer: miaubiz_svg_fuzzer
Job Type: windows_asan_chrome_no_sandbox
Platform Id: windows

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x083217e0
Crash State:
  blink::EventHandler::selectAutoCursor
  blink::EventHandler::selectCursor
  blink::EventHandler::handleMouseMoveOrLeaveEvent
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=windows_asan_chrome_no_sandbox&range=450347:450395
Fixed: https://clusterfuzz.com/revisions?job=windows_asan_chrome_no_sandbox&range=468030:468057

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6044738269741056


Additional requirements: Requires Gestures

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2017-04-29)

ClusterFuzz testcase 6044738269741056 is verified as fixed, so closing issue.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2017-04-29)

[Empty comment from Monorail migration]

### dt...@chromium.org (2017-04-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-29)

Your change meets the bar and is auto-approved for M59. Please go ahead and merge the CL to branch 3071 manually. Please contact milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), gkihumba@(ChromeOS), Abdul Syed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2017-05-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1dcdc127c1463d62c3e57a260e5a03869eab6024

commit 1dcdc127c1463d62c3e57a260e5a03869eab6024
Author: Dave Tapuska <dtapuska@chromium.org>
Date: Mon May 01 13:51:23 2017

Cleanup determining ibeam for node.

Change
https://chromium.googlesource.com/chromium/src/+/d892f9592860691ae9a782c12260c94ed6bd1a63%5E%21/#F30

caused the layout object to possibly be invalidated. Collapse the code
so that LayoutObject is correclty scoped so we don't run this risk.

BUG=712459

Review-Url: https://codereview.chromium.org/2849883002
Cr-Commit-Position: refs/heads/master@{#468045}
(cherry picked from commit 9d6b6c40b933564260a0a70567b90ac30656222a)

Review-Url: https://codereview.chromium.org/2856553002 .
Cr-Commit-Position: refs/branch-heads/3071@{#318}
Cr-Branched-From: a106f0abbf69dad349d4aaf4bcc4f5d376dd2377-refs/heads/master@{#464641}

[modify] https://crrev.com/1dcdc127c1463d62c3e57a260e5a03869eab6024/third_party/WebKit/Source/core/input/EventHandler.cpp


### aw...@chromium.org (2017-05-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-05)

[Empty comment from Monorail migration]

### aw...@google.com (2017-05-05)

The VRP panel decided to award $1,000 for this bug, and of course $500 for the clusterfuzz bonus.

### aw...@chromium.org (2017-05-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-08-05)

This issue was migrated from crbug.com/chromium/712459?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Input, Internals>Input]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087358)*
