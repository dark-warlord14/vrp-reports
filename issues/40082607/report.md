# Stack-buffer-overflow in SkIntersections::removeOne

| Field | Value |
|-------|-------|
| **Issue ID** | [40082607](https://issues.chromium.org/issues/40082607) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Reporter** | at...@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2015-08-03 |
| **Bounty** | $3,000.00 |

## Description


Tested on:

OS: Ubuntu 14.04

Chromium: linux-release-asan-symbolized-linux-release-340078


Repro-file as an attachment.

ASAN-trace:

==10881==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7f2258bf01d0 at pc 0x7f23b191af42 bp 0x7ffcac1bd450 sp 0x7ffcac1bcc10
READ of size 3824 at 0x7f2258bf01d0 thread T0 (chrome)
    #0 0x7f23b191af41 in __asan_memmove ??:?
    #1 0x7f23b3b70c1c in SkIntersections::removeOne(int) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/pathops/SkIntersections.cpp:151
    #2 0x7f23b3bc7426 in SkTSect<SkDCubic, SkDCubic>::BinarySearch(SkTSect<SkDCubic, SkDCubic>*, SkTSect<SkDCubic, SkDCubic>*, SkIntersections*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/pathops/SkPathOpsTSect.h:2084
    #3 0x7f23b3bc55e2 in SkIntersections::intersect(SkDCubic const&, SkDCubic const&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/pathops/SkPathOpsTSect.cpp:48
    #4 0x7f23b3b56df4 in AddIntersectTs(SkOpContour*, SkOpContour*, SkOpCoincidence*, SkChunkAlloc*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/pathops/SkAddIntersections.cpp:489
    #5 0x7f23b389682a in OpDebug(SkPath const&, SkPath const&, SkPathOp, SkPath*, bool) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/pathops/SkPathOpsOp.cpp:280
    #6 0x7f23c113209a in SkOpBuilder::resolve(SkPath*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/pathops/SkOpBuilder.cpp:145
    #7 0x7f23b9ea6005 in blink::LayoutSVGResourceClipper::tryPathOnlyClipping(blink::LayoutObject const&, blink::GraphicsContext*, blink::AffineTransform const&, blink::FloatRect const&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/layout/svg/LayoutSVGResourceClipper.cpp:130
    #8 0x7f23b95780bd in blink::SVGClipPainter::applyClippingToContext(blink::LayoutObject const&, blink::FloatRect const&, blink::FloatRect const&, blink::GraphicsContext*, blink::SVGClipPainter::ClipperState&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/paint/SVGClipPainter.cpp:63
    #9 0x7f23b9577c82 in blink::SVGClipPainter::applyStatefulResource(blink::LayoutObject const&, blink::GraphicsContext*, blink::SVGClipPainter::ClipperState&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/paint/SVGClipPainter.cpp:30
    #10 0x7f23c29ec9e7 in blink::SVGPaintContext::applyClipIfNecessary(blink::SVGResources*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/paint/SVGPaintContext.cpp:126
.
.
.

Address 0x7f2258bf01d0 is located in stack of thread T0 (chrome) at offset 464 in frame
    #0 0x7f23b3b5588f in AddIntersectTs(SkOpContour*, SkOpContour*, SkOpCoincidence*, SkChunkAlloc*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/patho
ps/SkAddIntersections.cpp:258

  This frame has 14 object(s):
    [32, 40) 'wt'
    [64, 72) 'wn'
    [96, 464) 'ts'
    [528, 576) 'quad1' <== Memory access at offset 464 partially underflows this variable
    [608, 656) 'quad2' <== Memory access at offset 464 partially underflows this variable
    [688, 744) 'conic1' <== Memory access at offset 464 partially underflows this variable
    [784, 840) 'conic2' <== Memory access at offset 464 partially underflows this variable
    [880, 944) 'cubic1' <== Memory access at offset 464 partially underflows this variable
    [976, 1040) 'cubic2' <== Memory access at offset 464 partially underflows this variable
    [1072, 1088) 'coinPtT' <== Memory access at offset 464 partially underflows this variable
    [1104, 1112) 'testTAt' <== Memory access at offset 464 partially underflows this variable
    [1136, 1144) 'coerce' <== Memory access at offset 464 partially underflows this variable
    [1168, 1176) 'nextTAt' <== Memory access at offset 464 partially underflows this variable
    [1200, 1208) 'coerce260' <== Memory access at offset 464 partially underflows this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism or swapcontext
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-buffer-overflow (/home/attekett/Downloads/chrome/chrome+0x29d8f41)
Shadow bytes around the buggy address:
.
.
.

## Attachments

- [chrome-stack-buffer-overflow-asanmemmove10-min.html](attachments/chrome-stack-buffer-overflow-asanmemmove10-min.html) (text/html, 1.3 KB)

## Timeline

### cl...@chromium.org (2015-08-03)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6264423688175616

### cl...@chromium.org (2015-08-03)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6264423688175616

Uploader: mbarbella@google.com
Job Type: linux_asan_chrome_mp
Crash Type: Stack-buffer-overflow READ {*}
Crash Address: 0x7f01d5f5c2f0
Crash State:
  SkIntersections::removeOne
  SkTSect<SkDCubic, SkDCubic>::BinarySearch
  SkIntersections::intersect
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=340068:340078

Minimized Testcase (0.88 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94uoFSWAd1FE9hht3p7yvFVW_oW1GGOM1m5k197Ih6xkcl6T12tSoc6xTH_OcyyMbtgkz6ceB-gGfxr-3HK7PNRjEk5XtpAII60BrMvBe6IvxkZPrtBGFgvzYZFon9ZLChCt9UXZORr4evbXcx4o3eq7lC5gQ



### mb...@chromium.org (2015-08-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-08-03)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-08-03)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-08-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-08-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-08-04)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### ca...@chromium.org (2015-08-17)

Isolated problem; have a fix. Testing to ensure no further regression.

### bu...@chromium.org (2015-08-18)

The following revision refers to this bug:
  https://skia.googlesource.com/skia.git/+/94c902e63d77641cadd76155c2b248d04f63b560

commit 94c902e63d77641cadd76155c2b248d04f63b560
Author: caryclark <caryclark@google.com>
Date: Tue Aug 18 14:12:43 2015

fix pathops fuzz failures

If a curve has the identical start and control points, the
initial or final tangent can't be trivally determined. The
perpendicular to the tangent is used to measure coincidence.

Add logic for cubics, quadratics, and conics, to use the
secondary control points or the end points if the initial
control point alone can't determine the tangent.

Add debugging (currently untriggered by exhaustive testing)
to detect zero-length tangents which are not at the curve
endpoints.

Increase the number of temporary intersecions gathered from
10 to 12 but reduce the max passed in by cubic intersection from
27 to 12. Also, add checks if the max passed exceeds the
storage allocated.

When cleaning up parallel lines, choose the intersection which
is on the end of both segments over the intersection which
is on the end of a single segment.

TBR=reed@google.com
BUG=425140,516266

Review URL: https://codereview.chromium.org/1288863004

[modify] http://crrev.com/94c902e63d77641cadd76155c2b248d04f63b560/src/pathops/SkDLineIntersection.cpp
[modify] http://crrev.com/94c902e63d77641cadd76155c2b248d04f63b560/src/pathops/SkIntersections.cpp
[modify] http://crrev.com/94c902e63d77641cadd76155c2b248d04f63b560/src/pathops/SkIntersections.h
[modify] http://crrev.com/94c902e63d77641cadd76155c2b248d04f63b560/src/pathops/SkPathOpsConic.cpp
[modify] http://crrev.com/94c902e63d77641cadd76155c2b248d04f63b560/src/pathops/SkPathOpsCubic.cpp
[modify] http://crrev.com/94c902e63d77641cadd76155c2b248d04f63b560/src/pathops/SkPathOpsQuad.cpp
[modify] http://crrev.com/94c902e63d77641cadd76155c2b248d04f63b560/src/pathops/SkPathOpsTSect.h
[modify] http://crrev.com/94c902e63d77641cadd76155c2b248d04f63b560/tests/PathOpsCubicIntersectionTest.cpp
[modify] http://crrev.com/94c902e63d77641cadd76155c2b248d04f63b560/tests/PathOpsOpTest.cpp


### cl...@chromium.org (2015-08-20)

ClusterFuzz has detected this issue as fixed in range 343936:344352.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6264423688175616

Uploader: mbarbella@google.com
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Stack-buffer-overflow READ {*}
Crash Address: 0x7f01d5f5c2f0
Crash State:
  SkIntersections::removeOne
  SkTSect<SkDCubic, SkDCubic>::BinarySearch
  SkIntersections::intersect
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=340068:340078
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=343936:344352

Minimized Testcase (0.88 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94uoFSWAd1FE9hht3p7yvFVW_oW1GGOM1m5k197Ih6xkcl6T12tSoc6xTH_OcyyMbtgkz6ceB-gGfxr-3HK7PNRjEk5XtpAII60BrMvBe6IvxkZPrtBGFgvzYZFon9ZLChCt9UXZORr4evbXcx4o3eq7lC5gQ

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### ca...@chromium.org (2015-08-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-08-20)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### ti...@google.com (2015-08-30)

No merge required - fix landed prior to M46 branch point.

### ti...@google.com (2015-08-31)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-11-26)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2016-06-24)

Updating old bug - $3,000 here

### aw...@chromium.org (2016-07-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/516266?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082607)*
