# UNKNOWN in SkSweepGradient::SweepGradientContext::shadeSpan

| Field | Value |
|-------|-------|
| **Issue ID** | [40082168](https://issues.chromium.org/issues/40082168) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Reporter** | cl...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2015-05-26 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

The attached testcase crashes the 64-bit of filter\_fuzz\_stub as follows:

=================================================================  

==31860==ERROR: AddressSanitizer: SEGV on unknown address 0x62120001b900 (pc 0x000000a7c290 bp 0x7fff0dda1970 sp 0x7fff0dda18c0 T0)  

#0 0xa7c28f in SkSweepGradient::SweepGradientContext::shadeSpan(int, int, unsigned int\*, int) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/effects/gradients/SkSweepGradient.cpp:128  

#1 0x83edab in SkARGB32\_Shader\_Blitter::blitRect(int, int, int, int) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkBlitter\_ARGB32.cpp:448  

#2 0x63d341 in SkScan::FillIRect(SkIRect const&, SkRegion const\*, SkBlitter\*) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkScan.cpp:43  

#3 0x63daf5 in SkScan::FillRect(SkRect const&, SkRegion const\*, SkBlitter\*) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkScan.cpp:61  

#4 0x63e230 in SkScan::FillRect(SkRect const&, SkRasterClip const&, SkBlitter\*) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkScan.cpp:103  

#5 0x57a583 in SkDraw::drawRect(SkRect const&, SkPaint const&, SkMatrix const\*, SkRect const\*) const /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkDraw.cpp:875  

#6 0x7f06d9 in SkBitmapDevice::drawRect(SkDraw const&, SkRect const&, SkPaint const&) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkBitmapDevice.cpp:189  

#7 0x550a4f in SkCanvas::onDrawRect(SkRect const&, SkPaint const&) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:1856  

#8 0xa4e13b in SkRectShaderImageFilter::onFilterImage(SkImageFilter::Proxy\*, SkBitmap const&, SkImageFilter::Context const&, SkBitmap\*, SkIPoint\*) const /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/effects/SkRectShaderImageFilter.cpp:74  

#9 0x5964a9 in SkImageFilter::filterImage(SkImageFilter::Proxy\*, SkBitmap const&, SkImageFilter::Context const&, SkBitmap\*, SkIPoint\*) const /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkImageFilter.cpp:189  

#10 0x546929 in SkCanvas::internalDrawDevice(SkBaseDevice\*, int, int, SkPaint const\*, bool) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:1233  

#11 0x5430ab in SkCanvas::internalRestore() /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:1098  

#12 0x548fc8 in AutoDrawLooper::~AutoDrawLooper() /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:402  

#13 0x547740 in SkCanvas::internalDrawBitmap(SkBitmap const&, SkMatrix const&, SkPaint const\*) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:1208  

#14 0x55441e in SkCanvas::onDrawBitmap(SkBitmap const&, float, float, SkPaint const\*) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:2039  

#15 0x54a3d5 in SkCanvas::drawBitmap(SkBitmap const&, float, float, SkPaint const\*) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:1753  

#16 0x4c9806 in RunTestCase /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:47  

#17 0x4c8bb9 in ReadAndRunTestCase /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:66  

#18 0x4c8713 in main /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:85  

#19 0x7fc16c658ec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: SEGV (/home/nils/MonkeyChrome/asan-symbolized-linux-release-331246/filter\_fuzz\_stub+0xa7c28f)  

==31860==ABORTING

**VERSION**  

Chrome Version: asan-symbolized-linux-release-331246  

Operating System: Linux

**REPRODUCTION CASE**  

Attached as repro.fil

## Attachments

- [repro.fil](attachments/repro.fil) (application/octet-stream, 164 B)

## Timeline

### cl...@gmail.com (2015-05-26)

Testcase

### cl...@chromium.org (2015-05-26)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5749760426770432

### cl...@chromium.org (2015-05-26)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5749760426770432

Uploader: mbarbella@google.com
Job Type: Linux_asan_filter_fuzz_stub

Crash Type: UNKNOWN
Crash Address: 0x62120001b900
Crash State:
  SkSweepGradient::SweepGradientContext::shadeSpan
  SkARGB32_Shader_Blitter::blitRect
  SkScan::FillIRect
  

Minimized Testcase (0.16 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95R8HcrLewy9GFSj-FsBtPppyEvSP1TIy9O2SzYrF1ELNhuQPKtkjH8mNziL1TDi2kynW7Sq5jUuZtuFSC_sbDNDNAD2NYc3BFxXSqWRFW0ZQaptn2n9i6iVmO1ceLq11BzVnmsqJEKj5z1HFbAY3B8czF6Zw



### cl...@chromium.org (2015-05-26)

[Empty comment from Monorail migration]

### np...@chromium.org (2015-05-29)

reed@ -- Can you take a look, or find someone who can?  Thanks.

mbarbella@ -- What's the best approach when clusterfuzz says "AddressSanitizer can not provide additional info?"  The report seems vague.

cc'ing those with related CLs.

### mb...@chromium.org (2015-05-29)

It means that the access didn't land at an address that ASan is tracking (and the report is from ASan itself). Probably an OOB access that's so far off that it didn't land in a redzone.

You can try running with larger redzones (ASAN_OPTIONS=redzone=XXXX), but in general there's not a good way to squeeze extra information out of ASan in the case of a wild read or write.

### cl...@chromium.org (2015-05-30)

[Empty comment from Monorail migration]

### np...@chromium.org (2015-06-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-13)

reed@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### bu...@chromium.org (2015-06-19)

The following revision refers to this bug:
  https://skia.googlesource.com/skia.git/+/20eee3f047f56b7715b311313b2998daaaf08a96

commit 20eee3f047f56b7715b311313b2998daaaf08a96
Author: robertphillips <robertphillips@google.com>
Date: Fri Jun 19 12:14:26 2015

Added check for ill-conditioned invert

sk_inv_determinant has a guard that the determinant can't get too big so this CL only checks if the determinant gets too small.

BUG=492263

Review URL: https://codereview.chromium.org/1188433011

[modify] http://crrev.com/20eee3f047f56b7715b311313b2998daaaf08a96/include/core/SkMatrix.h
[modify] http://crrev.com/20eee3f047f56b7715b311313b2998daaaf08a96/src/core/SkMatrix.cpp
[modify] http://crrev.com/20eee3f047f56b7715b311313b2998daaaf08a96/tests/MatrixTest.cpp


### in...@chromium.org (2015-06-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-21)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-06-22)

ClusterFuzz has detected this issue as fixed in range 335153:335500.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5749760426770432

Uploader: mbarbella@google.com
Job Type: Linux_asan_filter_fuzz_stub

Crash Type: UNKNOWN
Crash Address: 0x62120001b900
Crash State:
  SkSweepGradient::SweepGradientContext::shadeSpan
  SkARGB32_Shader_Blitter::blitRect
  SkScan::FillIRect
  
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub&range=335153:335500

Minimized Testcase (0.16 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95R8HcrLewy9GFSj-FsBtPppyEvSP1TIy9O2SzYrF1ELNhuQPKtkjH8mNziL1TDi2kynW7Sq5jUuZtuFSC_sbDNDNAD2NYc3BFxXSqWRFW0ZQaptn2n9i6iVmO1ceLq11BzVnmsqJEKj5z1HFbAY3B8czF6Zw

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### ti...@google.com (2015-07-08)

This doesn't look like it's in the M44 skia branch, so requesting a merge to M44 just to make sure it is.

Merge-Request to M44 (branch 2403).

### pe...@google.com (2015-07-08)

[Automated comment] Less than 2 weeks to go before stable on M44, manual review required.

### [Deleted User] (2015-07-08)

The CL in question (https://codereview.chromium.org/1188433011 Added check for ill-conditioned invert) should be pretty safe to cherry pick.

### pe...@google.com (2015-07-10)

Approved for merge to m44 (2403) skia branch.  Please get the merge done before end of business PST Monday.

### bu...@chromium.org (2015-07-13)

The following revision refers to this bug:
  https://skia.googlesource.com/skia.git/+/1c7bee66e0c3fd4fdbe021f34364786e18f94d6d

commit 1c7bee66e0c3fd4fdbe021f34364786e18f94d6d
Author: Robert Phillips <robertphillips@google.com>
Date: Mon Jul 13 21:23:33 2015

M44 cherry pick of: Added check for ill-conditioned invert

sk_inv_determinant has a guard that the determinant can't get too big so this CL only checks if the determinant gets too small.

BUG=492263

Review URL: https://codereview.chromium.org/1188433011
NOTREECHECKS=true
NOTRY=true
NOPRESUBMIT=true
TBR=bsalomon@google.com, reed@google.com

Review URL: https://codereview.chromium.org/1235863005 .

[modify] http://crrev.com/1c7bee66e0c3fd4fdbe021f34364786e18f94d6d/include/core/SkMatrix.h
[modify] http://crrev.com/1c7bee66e0c3fd4fdbe021f34364786e18f94d6d/src/core/SkMatrix.cpp
[modify] http://crrev.com/1c7bee66e0c3fd4fdbe021f34364786e18f94d6d/tests/MatrixTest.cpp


### mb...@chromium.org (2015-07-16)

[Empty comment from Monorail migration]

### la...@google.com (2015-08-28)

Clearing approvals older than 60 days

### ti...@google.com (2015-08-31)

Making sure that this is captured in the M45 release notes, even though it landed and shipped earlier.

### ti...@google.com (2015-08-31)

Congrats - $5000 for this report! You should receive the payment in 2-3 weeks from today.

### ti...@google.com (2015-09-04)

[Empty comment from Monorail migration]

### ti...@google.com (2015-09-10)

Processing via our e-payment system takes ~7 days, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2015-09-27)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/492263?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082168)*
