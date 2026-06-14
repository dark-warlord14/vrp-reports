# Crash in FixWinding

| Field | Value |
|-------|-------|
| **Issue ID** | [40084479](https://issues.chromium.org/issues/40084479) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ca...@chromium.org |
| **Created** | 2016-06-06 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4656132446748672

Fuzzer: attekett_dom_fuzzer
Job Type: linux_asan_chrome_v8_arm
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x0001078d
Crash State:
  FixWinding
  SkOpBuilder::resolve
  blink::LayoutSVGResourceClipper::calculateClipContentPathIfNeeded
  
Recommended Security Severity: Medium


Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96c51hKmtMH0ZxOGbxf6AUb2v7SgB5w9sFUOOABZPEnLGdElyG1hcPvCMVyGhdaeeYn_Tw0QGNYOz1TR-clTnv2WxP8gtvY51XgxyRNxynETURhwLIGH2IRxuz2zvU-oq5Y7uJIc4jlMyipRVHCHZNi14D7lw


Filer: aarya

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### in...@chromium.org (2016-06-06)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-06-06)

[Empty comment from Monorail migration]

### fe...@chromium.org (2016-06-06)

caryclark, would you be a good owner for this bug?

[Monorail components: Internals>Skia]

### fe...@chromium.org (2016-06-06)

[Empty comment from Monorail migration]

### ca...@chromium.org (2016-06-06)

Investigating

### ca...@chromium.org (2016-06-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-07)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2016-06-08)

The following revision refers to this bug:
  https://skia.googlesource.com/skia.git/+/dae6b97705fde08958b1a36fa6ce685d28fc692c

commit dae6b97705fde08958b1a36fa6ce685d28fc692c
Author: caryclark <caryclark@google.com>
Date: Wed Jun 08 11:28:19 2016

fix pathops fuzz bugs

Fail out in a couple of new places when the input data is very
large and exceeds the limits of the pathops machinery.

Most of the change here plumbs in a way to exclude an assert in
one of these exceptional cases. The current SkAddIntersection
implementation and the inner functions it calls has no way to
report an error to the root caller for an early exit, so rather
than add that in, exclude the assert when the test that would
trigger it runs (allowing the test to otherwise ensure that it
properly fails).

TBR=reed@google.com
BUG=617586,617635
GOLD_TRYBOT_URL= https://gold.skia.org/search?issue=2046713003

Review-Url: https://codereview.chromium.org/2046713003

[modify] https://crrev.com/dae6b97705fde08958b1a36fa6ce685d28fc692c/src/pathops/SkAddIntersections.cpp
[modify] https://crrev.com/dae6b97705fde08958b1a36fa6ce685d28fc692c/src/pathops/SkDConicLineIntersection.cpp
[modify] https://crrev.com/dae6b97705fde08958b1a36fa6ce685d28fc692c/src/pathops/SkIntersections.h
[modify] https://crrev.com/dae6b97705fde08958b1a36fa6ce685d28fc692c/src/pathops/SkOpBuilder.cpp
[modify] https://crrev.com/dae6b97705fde08958b1a36fa6ce685d28fc692c/src/pathops/SkOpCoincidence.cpp
[modify] https://crrev.com/dae6b97705fde08958b1a36fa6ce685d28fc692c/src/pathops/SkPathOpsCommon.cpp
[modify] https://crrev.com/dae6b97705fde08958b1a36fa6ce685d28fc692c/src/pathops/SkPathOpsCommon.h
[modify] https://crrev.com/dae6b97705fde08958b1a36fa6ce685d28fc692c/src/pathops/SkPathOpsOp.cpp
[modify] https://crrev.com/dae6b97705fde08958b1a36fa6ce685d28fc692c/src/pathops/SkPathOpsSimplify.cpp
[modify] https://crrev.com/dae6b97705fde08958b1a36fa6ce685d28fc692c/src/pathops/SkPathOpsTightBounds.cpp
[modify] https://crrev.com/dae6b97705fde08958b1a36fa6ce685d28fc692c/src/pathops/SkPathOpsTypes.cpp
[modify] https://crrev.com/dae6b97705fde08958b1a36fa6ce685d28fc692c/src/pathops/SkPathOpsTypes.h
[modify] https://crrev.com/dae6b97705fde08958b1a36fa6ce685d28fc692c/tests/PathOpsAngleIdeas.cpp
[modify] https://crrev.com/dae6b97705fde08958b1a36fa6ce685d28fc692c/tests/PathOpsAngleTest.cpp
[modify] https://crrev.com/dae6b97705fde08958b1a36fa6ce685d28fc692c/tests/PathOpsBuilderTest.cpp
[modify] https://crrev.com/dae6b97705fde08958b1a36fa6ce685d28fc692c/tests/PathOpsExtendedTest.cpp
[modify] https://crrev.com/dae6b97705fde08958b1a36fa6ce685d28fc692c/tests/PathOpsExtendedTest.h
[modify] https://crrev.com/dae6b97705fde08958b1a36fa6ce685d28fc692c/tests/PathOpsOpTest.cpp


### bu...@chromium.org (2016-06-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/27c0233b9d759b06b3e4e551a892e9613032198e

commit 27c0233b9d759b06b3e4e551a892e9613032198e
Author: skia-deps-roller <skia-deps-roller@chromium.org>
Date: Wed Jun 08 12:54:04 2016

Roll src/third_party/skia/ 2af4599b5..dae6b9770 (1 commit).

https://chromium.googlesource.com/skia.git/+log/2af4599b5c51..dae6b97705fd

$ git log 2af4599b5..dae6b9770 --date=short --no-merges --format='%ad %ae %s'
2016-06-08 caryclark fix pathops fuzz bugs

BUG=617586,617635

CQ_INCLUDE_TRYBOTS=tryserver.blink:linux_blink_rel
TBR=mtklein@google.com

Review-Url: https://codereview.chromium.org/2048983003
Cr-Commit-Position: refs/heads/master@{#398532}

[modify] https://crrev.com/27c0233b9d759b06b3e4e551a892e9613032198e/DEPS


### cl...@chromium.org (2016-06-09)

ClusterFuzz has detected this issue as fixed in range 397961:397971.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4656132446748672

Fuzzer: attekett_dom_fuzzer
Job Type: linux_asan_chrome_v8_arm
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x0001078d
Crash State:
  FixWinding
  SkOpBuilder::resolve
  blink::LayoutSVGResourceClipper::calculateClipContentPathIfNeeded
  
Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=377544:377564
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=397961:397971

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96c51hKmtMH0ZxOGbxf6AUb2v7SgB5w9sFUOOABZPEnLGdElyG1hcPvCMVyGhdaeeYn_Tw0QGNYOz1TR-clTnv2WxP8gtvY51XgxyRNxynETURhwLIGH2IRxuz2zvU-oq5Y7uJIc4jlMyipRVHCHZNi14D7lw


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### ca...@chromium.org (2016-06-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-06-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-06)

Congratulations, $3,500 for this.  The panel noted they wouldn't be surprised if this lead to memory corruption.

### aw...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-26)

Fix already in M53, removing ReleaseBlock-Beta.

### sh...@chromium.org (2016-09-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/617635?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084479)*
