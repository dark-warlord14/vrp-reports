# crash in  SkSweepGradient::SweepGradientContext::shadeSpan

| Field | Value |
|-------|-------|
| **Issue ID** | [40083189](https://issues.chromium.org/issues/40083189) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Skia |
| **CVE IDs** | CVE-2016-1637 |
| **Reporter** | ke...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2015-11-13 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

The testcase crashes 64 bit filter\_fuzz\_stub :  

Looks the same as <https://code.google.com/p/chromium/issues/detail?id=492263>

==23208==ERROR: AddressSanitizer: SEGV on unknown address 0x62120001b900 (pc 0x0000009e05ea bp 0x7fff78941490 sp 0x7fff789413e0 T0)  

#0 0x9e05e9 in SkSweepGradient::SweepGradientContext::shadeSpan(int, int, unsigned int\*, int) third\_party/skia/src/effects/gradients/SkSweepGradient.cpp:113:23  

#1 0x7e09c9 in SkARGB32\_Shader\_Blitter::blitRect(int, int, int, int) third\_party/skia/src/core/SkBlitter\_ARGB32.cpp:448:17  

#2 0x62c0f9 in blitrect third\_party/skia/src/core/SkScan.cpp:15:5  

#3 0x62c0f9 in SkScan::FillIRect(SkIRect const&, SkRegion const\*, SkBlitter\*) third\_party/skia/src/core/SkScan.cpp:43  

#4 0x62cf0a in FillRect third\_party/skia/src/core/SkScan.cpp:61:5  

#5 0x62cf0a in SkScan::FillRect(SkRect const&, SkRasterClip const&, SkBlitter\*) third\_party/skia/src/core/SkScan.cpp:103  

#6 0x569deb in SkDraw::drawRect(SkRect const&, SkPaint const&, SkMatrix const\*, SkRect const\*) const third\_party/skia/src/core/SkDraw.cpp:872:21  

#7 0x545561 in SkCanvas::onDrawRect(SkRect const&, SkPaint const&) third\_party/skia/src/core/SkCanvas.cpp:2031:9  

#8 0x9b3a7a in SkRectShaderImageFilter::onFilterImage(SkImageFilter::Proxy\*, SkBitmap const&, SkImageFilter::Context const&, SkBitmap\*, SkIPoint\*) const third\_party/skia/src/effects/SkRectShaderImageFilter.cpp:74:5  

#9 0x57f7ad in SkImageFilter::filterImage(SkImageFilter::Proxy\*, SkBitmap const&, SkImageFilter::Context const&, SkBitmap\*, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:250:9  

#10 0x539f4e in SkCanvas::internalDrawDevice(SkBaseDevice\*, int, int, SkPaint const\*, bool) third\_party/skia/src/core/SkCanvas.cpp:1341:17  

#11 0x5365b9 in SkCanvas::internalRestore() third\_party/skia/src/core/SkCanvas.cpp:1187:13  

#12 0x53c301 in AutoDrawLooper::~AutoDrawLooper() third\_party/skia/src/core/SkCanvas.cpp:479:13  

#13 0x53ac8b in SkCanvas::internalDrawBitmap(SkBitmap const&, SkMatrix const&, SkPaint const\*) third\_party/skia/src/core/SkCanvas.cpp:1316:1  

#14 0x54a4a3 in SkCanvas::onDrawBitmap(SkBitmap const&, float, float, SkPaint const\*) third\_party/skia/src/core/SkCanvas.cpp:2215:5  

#15 0x4d05dc in RunTestCase skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:47:5  

#16 0x4d05dc in ReadAndRunTestCase skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:66  

#17 0x4d05dc in main skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:85  

#18 0x7f1bb1c55ec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: SEGV third\_party/skia/src/effects/gradients/SkSweepGradient.cpp:113:23 in SkSweepGradient::SweepGradientContext::shadeSpan(int, int, unsigned int\*, int)

**VERSION**  

Chrome Version: asan-linux-stable-46.0.2490.86  

Operating System: Ubuntu 64

**REPRODUCTION CASE**  

Attached file.

## Attachments

- [cr.fil](attachments/cr.fil) (application/octet-stream, 168 B)

## Timeline

### in...@chromium.org (2015-11-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-11-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5150795097440256

### cl...@chromium.org (2015-11-13)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5150795097440256

Uploader: aarya@google.com
Job Type: linux_asan_filter_fuzz_stub
Platform Id: linux

Crash Type: UNKNOWN
Crash Address: 0x62120001b900
Crash State:
  SkSweepGradient::SweepGradientContext::shadeSpan
  SkARGB32_Shader_Blitter::blitRect
  SkScan::FillIRect
  

Minimized Testcase (0.16 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96CobkRr6AIk1GCX9ZoUFVsm08JQuNcRF9BTmDWf92qTcjWJIKIktjMNpz5Am4eVSb9gCh9wuwtKc1LYT5FBXNUbF1VxgVthCxWrmGpMqgFq978vvUOxW6nWbW1uMC_iAGBeP4qs9XmMBHAu0vW0-ELwtPi6Q

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### ji...@chromium.org (2015-11-13)

Can anyone update the Cr- component label please? Thanks!

### mb...@chromium.org (2015-11-13)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-11-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-11-13)

[Empty comment from Monorail migration]

### [Deleted User] (2015-11-16)

In this case the view matrix is:

-0.5 0.5 0.0
-1.70133415e+038 1.70133415e+038 0.999969602
1.0 0.0 0.0

The Persp_xy matrix proc is selected and maps:

2.5, 2.5 -> 0 -1.#IND 2.5 -> 0.0, -1.#IND0000

This is then fed to SkATan2_255 which calls sk_float_atan2 to get a result of: -1.#IND0000

This, in turn, yields an integer index of -2147483648

which is where the bad address access comes from.

One possible "solution" is to perform a hard pin to [0 .. 255] in SkATan2_255.

Other thoughts Mike?

### [Deleted User] (2015-11-16)

Another thought:

Inside all shaders, when we create our context, we are given the CTM, so we can compute a custom version (typically we invert it). At this stage, we could check that the matrix is "nice" (i.e. is finite). If not, we can return false/null and just not draw.

### cl...@chromium.org (2015-12-01)

robertphillips@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### [Deleted User] (2015-12-01)

The matrix itself seems okay so I don't know if we could weed this case out in the context creation step.

### bu...@chromium.org (2015-12-07)

The following revision refers to this bug:
  https://skia.googlesource.com/skia.git/+/1d265ca85f51ea1ba087ca4d0f80b008c256a47d

commit 1d265ca85f51ea1ba087ca4d0f80b008c256a47d
Author: robertphillips <robertphillips@google.com>
Date: Mon Dec 07 17:54:02 2015

Pin result in SkATan2_255

BUG=555544

Review URL: https://codereview.chromium.org/1506913002

[modify] http://crrev.com/1d265ca85f51ea1ba087ca4d0f80b008c256a47d/src/effects/gradients/SkSweepGradient.cpp


### [Deleted User] (2015-12-08)

This rolled into Chrome in https://codereview.chromium.org/1507553003/ at r363607.

This should be safe to cherry pick as far back as we like.

### ti...@google.com (2015-12-08)

[Automated comment] Request affecting a post-stable build (M47), manual review required.

### cl...@chromium.org (2015-12-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-12-09)

ClusterFuzz has detected this issue as fixed in range 363565:363834.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5150795097440256

Uploader: aarya@google.com
Job Type: linux_asan_filter_fuzz_stub
Platform Id: linux

Crash Type: UNKNOWN
Crash Address: 0x62120001b900
Crash State:
  SkSweepGradient::SweepGradientContext::shadeSpan
  SkARGB32_Shader_Blitter::blitRect
  SkScan::FillIRect
  
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub&range=363565:363834

Minimized Testcase (0.16 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96CobkRr6AIk1GCX9ZoUFVsm08JQuNcRF9BTmDWf92qTcjWJIKIktjMNpz5Am4eVSb9gCh9wuwtKc1LYT5FBXNUbF1VxgVthCxWrmGpMqgFq978vvUOxW6nWbW1uMC_iAGBeP4qs9XmMBHAu0vW0-ELwtPi6Q

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### ti...@google.com (2015-12-10)

[Automated comment] There appears to be on-going work (i.e. bugroid changes), needs manual review.

### ti...@google.com (2015-12-11)

Merge approved for M48 (branch 2564). Pls go ahead merge.

### bu...@chromium.org (2015-12-14)

The following revision refers to this bug:
  https://skia.googlesource.com/skia.git/+/3b109a5f2ce4db1c712ee6b1c28b397ff524b2b9

commit 3b109a5f2ce4db1c712ee6b1c28b397ff524b2b9
Author: Robert Phillips <robertphillips@google.com>
Date: Mon Dec 14 17:17:21 2015

Cherry pick back to m48 of (Pin result in SkATan2_255)

Original CL: https://codereview.chromium.org/1506913002

BUG=555544
NOTREECHECKS=true
NOTRY=true
NOPRESUBMIT=true

Review URL: https://codereview.chromium.org/1524783002 .

[modify] http://crrev.com/3b109a5f2ce4db1c712ee6b1c28b397ff524b2b9/src/effects/gradients/SkSweepGradient.cpp


### ss...@google.com (2015-12-29)

M47 is post stable and the bar is very high for merges into this branch. Can we punt this to M48? I don't see anything here suggesting that this is critical or very high-impact. Please let me know if that's not the case. 

### [Deleted User] (2016-01-04)

#20 - sgtm

### go...@chromium.org (2016-01-05)

[Empty comment from Monorail migration]

### ti...@google.com (2016-02-29)

Tagging for M49 release notes (provided it meets the bar for reward).

### ti...@google.com (2016-03-02)

Congrats Keve - $2000 for this report. We'll list you in the M49 release notes as "Keve Nagy"  and a CVE-ID will follow shortly.

### ti...@google.com (2016-03-02)

CVE-2016-1637

### kc...@chromium.org (2016-03-05)

Kevin, is it possible to write a fuzz target that will cover this code? 
(And that will reproduce this bug if the fix is reverted)

### kj...@chromium.org (2016-03-06)

Yes.  I've already done some work on this to use afl-fuzz. https://codereview.chromium.org/1710183002 Changing the end point to use libfuzzer should be fine.  I just need to work out if the preliminary results I saw are legitimate problems or a bad testcase.

### ti...@google.com (2016-03-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-03-15)

This security bug has been closed for more than 14 weeks. Removing view restrictions.

For more details visit https://sites.google.com/a/chromium.org/dev/issue-tracking/autotriage - Your friendly Sheriffbot

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

This issue was migrated from crbug.com/chromium/555544?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083189)*
