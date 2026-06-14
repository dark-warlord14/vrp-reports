# Heap-buffer-overflow in SkOpContour::operand

| Field | Value |
|-------|-------|
| **Issue ID** | [40083937](https://issues.chromium.org/issues/40083937) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Skia |
| **CVE IDs** | CVE-2016-1691 |
| **Reporter** | at...@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2016-03-25 |
| **Bounty** | $500.00 |

## Description




Tested on:

OS: Ubuntu 14.04

Chromium: linux-release-asan-symbolized-linux-release-382848



ASAN-trace:

==24024==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x623000006d2d at pc 0x5594e6c08456 bp 0x7fffba372170 sp 0x7fffba372168
READ of size 1 at 0x623000006d2d thread T0 (chrome)
    #0 0x5594e6c08455 in SkOpContour::operand() const /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/pathops/SkOpContour.h:296
    #1 0x5594e6beed81 in SkOpCoincidence::apply() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/pathops/SkOpCoincidence.cpp:391 (discriminator 2)
    #2 0x5594e6c128f2 in HandleCoincidence(SkOpContourHead*, SkOpCoincidence*, SkChunkAlloc*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/pathops/SkPathOpsCommon.cpp:514
    #3 0x5594e68882c9 in OpDebug(SkPath const&, SkPath const&, SkPathOp, SkPath*, bool) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/pathops/SkPathOpsOp.cpp:310
    #4 0x5594e9bfedf8 in clipPath /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/modules/canvas2d/ClipList.cpp:24
    #5 0x5594e9bf28fa in blink::CanvasRenderingContext2DState::clipPath(SkPath const&, blink::AntiAliasingMode) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/modules/canvas2d/CanvasRenderingContext2DState.cpp:256 (discriminator 1)
    #6 0x5594ea3d1cf9 in blink::BaseRenderingContext2D::clipInternal(blink::Path const&, WTF::String const&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/modules/canvas2d/BaseRenderingContext2D.cpp:702 (discriminator 1)
.
.
.


## Attachments

- [chrome-heap-buffer-overflow-SkOpContouroperand-min.html](attachments/chrome-heap-buffer-overflow-SkOpContouroperand-min.html) (text/plain, 1.7 KB)

## Timeline

### cl...@chromium.org (2016-03-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6346720362889216

### wf...@chromium.org (2016-03-25)

[Empty comment from Monorail migration]

[Monorail components: Internals>Skia]

### wf...@chromium.org (2016-03-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-03-26)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6346720362889216

Uploader: wfh@chromium.org
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x62300000a52d
Crash State:
  SkOpSegment::operand
  SkOpCoincidence::apply
  HandleCoincidence
  
Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=375259:376290

Minimized Testcase (0.99 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96lhUb3_2xsN72F5HAPLAXvKA1ypWytTMbYK4DMP0bzewiWM5YI9_NIjywaA1kMd4OuFbbsOIb-qNRg_pQpIqsQy78XsAs0UpjTn0jhS_TfnVBqko0prOU6Ck6khO2apkskN4THjKcGuVFvuLptH7ABGTjm1A

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

The recommended severity is different from what was assigned to the bug. Please double check the accuracy of the assigned severity.


### cl...@chromium.org (2016-03-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-03-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-03-26)

[Empty comment from Monorail migration]

### wf...@chromium.org (2016-03-26)

caryclark@ - can you take a look at this Heap-buffer-overflow READ in skia?

### cl...@chromium.org (2016-03-27)

[Empty comment from Monorail migration]

### ca...@chromium.org (2016-03-28)

I am on vacation this week but will attend to this when I return

### go...@chromium.org (2016-03-28)

A friendly reminder that M50 Stable is launching soon! Your bug is labelled as Stable ReleaseBlock, pls make sure to land the fix and get it merged into the release branch by Apr-5. All changes MUST be merged into the release branch by 5pm on Apr-8 to make into the desktop Stable final build cut. Thanks!

### go...@chromium.org (2016-04-04)

M50 Stable is launching very soon! Your bug is labelled as Stable ReleaseBlock, pls make sure to land the fix and get it merged ASAP. All changes MUST be merged into the release branch by 5pm on Apr-8 to make into the desktop Stable final build cut. Thanks!

### bu...@chromium.org (2016-04-05)

The following revision refers to this bug:
  https://skia.googlesource.com/skia.git/+/5c5cfe24efe4c728e787447dabffe345080d1fb9

commit 5c5cfe24efe4c728e787447dabffe345080d1fb9
Author: caryclark <caryclark@google.com>
Date: Tue Apr 05 14:28:48 2016

give up if huge paths have unresolvable coincidence

This fuzzy test has enormous curves with coincidence runs that break numerics.
If the computed intersections identify that the span of coincidence has been deleted,
give up and return that the path op failed.

TBR=reed@google.com
BUG=597926
GOLD_TRYBOT_URL= https://gold.skia.org/search2?unt=true&query=source_type%3Dgm&master=false&issue=1854333002

Review URL: https://codereview.chromium.org/1854333002

[modify] https://crrev.com/5c5cfe24efe4c728e787447dabffe345080d1fb9/src/pathops/SkOpCoincidence.cpp
[modify] https://crrev.com/5c5cfe24efe4c728e787447dabffe345080d1fb9/src/pathops/SkOpCoincidence.h
[modify] https://crrev.com/5c5cfe24efe4c728e787447dabffe345080d1fb9/src/pathops/SkPathOpsCommon.cpp
[modify] https://crrev.com/5c5cfe24efe4c728e787447dabffe345080d1fb9/tests/PathOpsOpTest.cpp


### go...@chromium.org (2016-04-07)

Please request a merge to M50 ASAP if CL listed at https://crbug.com/chromium/597926#c13 is baked in Canary and it is a safe merge. Thank you.

### ca...@chromium.org (2016-04-07)

[Empty comment from Monorail migration]

### hc...@chromium.org (2016-04-07)

I will cherry-pick to Skia's M50 today and update the bug when it's in.

### bu...@chromium.org (2016-04-07)

The following revision refers to this bug:
  https://skia.googlesource.com/skia.git/+/f7c89fd393453407abf76175eabccd482ffc9ddf

commit f7c89fd393453407abf76175eabccd482ffc9ddf
Author: hcm <hcm@google.com>
Date: Thu Apr 07 17:57:11 2016

give up if huge paths have unresolvable coincidence

This fuzzy test has enormous curves with coincidence runs that break numerics.
If the computed intersections identify that the span of coincidence has been deleted,
give up and return that the path op failed.

TBR=reed@google.com, caryclark@google.com
BUG=597926
GOLD_TRYBOT_URL= https://gold.skia.org/search2?unt=true&query=source_type%3Dgm&master=false&issue=1854333002

Review URL: https://codereview.chromium.org/1854333002
NOTREECHECKS=true
NOTRY=true
NOPRESUBMIT=true

Review URL: https://codereview.chromium.org/1872523002

[modify] https://crrev.com/f7c89fd393453407abf76175eabccd482ffc9ddf/src/pathops/SkOpCoincidence.cpp
[modify] https://crrev.com/f7c89fd393453407abf76175eabccd482ffc9ddf/src/pathops/SkOpCoincidence.h
[modify] https://crrev.com/f7c89fd393453407abf76175eabccd482ffc9ddf/src/pathops/SkPathOpsCommon.cpp
[modify] https://crrev.com/f7c89fd393453407abf76175eabccd482ffc9ddf/tests/PathOpsOpTest.cpp


### hc...@chromium.org (2016-04-07)

The change is in Skia's M50 branch linked in the Chrome 50 DEPS and will be picked up by the next build.

### cl...@chromium.org (2016-04-08)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-24)

We'll note this in the M51 release notes

### ti...@google.com (2016-05-25)

Updating severity - this appears to be a one-byte read.

### ti...@google.com (2016-05-26)

Atte - only $500 for this one, but I'll add it to your tab.

Panel notes: 1 byte read, it's difficult to see how this could be useful in an exploit.

CVE-ID is CVE-2016-1691

### cl...@chromium.org (2016-06-08)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6346720362889216

Uploader: wfh@chromium.org
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x62300000a52d
Crash State:
  SkOpSegment::operand
  SkOpCoincidence::apply
  HandleCoincidence
  
Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=375259:376290

Minimized Testcase (0.99 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96L4CsYkBuuXVCGPLp23hhoDzBFwoQ9_GvLqCkwluzwKKnGz4E5YyCQ5S0-snRVPiOBT4aamNF2TpnNkzG4gSdVdJKrRynbVgcgraFURjpE0HAps1EPfcmHhOkKP8tap6WbP-LMZ5Dx9makvB8Ln7zFWJ0lgw

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

The recommended severity is different from what was assigned to the bug. Please double check the accuracy of the assigned severity.


### cl...@chromium.org (2016-06-09)

ClusterFuzz has detected this issue as fixed in range 384695:385240.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6346720362889216

Uploader: wfh@chromium.org
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x62300000a52d
Crash State:
  SkOpSegment::operand
  SkOpCoincidence::apply
  HandleCoincidence
  
Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=375259:376290
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=384695:385240

Minimized Testcase (0.99 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96L4CsYkBuuXVCGPLp23hhoDzBFwoQ9_GvLqCkwluzwKKnGz4E5YyCQ5S0-snRVPiOBT4aamNF2TpnNkzG4gSdVdJKrRynbVgcgraFURjpE0HAps1EPfcmHhOkKP8tap6WbP-LMZ5Dx9makvB8Ln7zFWJ0lgw

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### aw...@chromium.org (2016-07-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-15)

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

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/597926?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083937)*
