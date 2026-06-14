# Use-of-uninitialized-value in SkPreMultiplyARGB

| Field | Value |
|-------|-------|
| **Issue ID** | [40081228](https://issues.chromium.org/issues/40081228) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Reporter** | cl...@chromium.org |
| **Assignee** | jb...@chromium.org |
| **Created** | 2015-01-20 |
| **Bounty** | $1,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6591874927165440

Fuzzer: Cdiehl_peach
Job Type: Linux_msan_chrome

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  SkPreMultiplyARGB
  blink::DragImage::dissolveToFraction
  blink::DragController::startDrag
  

Minimized Testcase (140.23 Kb): https://cluster-fuzz.appspot.com/download/AMIfv973XGp6T64nR7jcPnXZwESf68zTs0v1FsOJ0Due059Ereeuacct8aq3O47mSgu7rPvEf9K3NHSC-J_ch0nkG9Z980bwBme5okAb5sxUmek74xBCbPPkEiNCaZ6SAEngyrPpHQhr3-PyLEfw_cXBABPckCi_sfoGI2_2qhi3f0byqa7FGAM

Additional requirements: Requires Gestures

Filer: inferno

## Timeline

### in...@chromium.org (2015-01-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-21)

[Empty comment from Monorail migration]

### ri...@chromium.org (2015-01-22)

Hey Reed, would you mind taking a look at this? I did some initial reading through the code. It looks like when a DragImage is created (https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/platform/DragImage.cpp&l=71), an SkBitmap is returned with uninitialized image data. I did not debug precisely what causes this in the above test case, but glancing through the code, it looks like the canvas.drawBitmapRect call leads to https://code.google.com/p/chromium/codesearch#chromium/src/third_party/skia/src/core/SkCanvas.cpp&l=1949, where I see at least one code path that looks like it can cause the function to return early - maybe that's something to explore?

In terms of security impact, If an attacker could somehow read the DragImage, this could be used to leak addresses. I'd be surprised if it were possible to read the DragImage, but perhaps there are other instances where a controlled image is copied with drawBitmapRect and could be read back.

### ri...@chromium.org (2015-01-22)

[Empty comment from Monorail migration]

### [Deleted User] (2015-01-22)

canvas.draw for any primitive (rect, bitmap, path, text) can always end up not drawing (based on the current clip, transform, etc). This is correct behavior in SkCanvas.

If there is uninitialized data in the bitmap, and the bitmap was originally a backing for a canvas, then it is the responsibility of the client of that canvas to initialize the memory first.

I am happy to help, but I think the owners of DragImage need to trace back and find where and how that image was created.

### in...@chromium.org (2015-01-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-01-25)

Author: jbroman@chromium.org
Component: blink
Changelist: https://chromium.googlesource.com/chromium/blink.git/+/8b8808547955c2f1286af29b851ae6e83ec01c50
Time: Wed Jun 19 02:57:21 2013
The CL last changed line 284 of file DragImage.cpp, which is stack frame 1.

Author: dcheng@chromium.org
Component: blink
Changelist: https://chromium.googlesource.com/chromium/blink.git/+/6d7f62a42228dc2a7d68b636b7a37e0330f298c2
Time: Tue Jul 02 23:20:30 2013
The CL last changed line 835 of file DragController.cpp, which is stack frame 2.

### jb...@chromium.org (2015-01-25)

This looks likely to be similar to another bug I fixed, https://crbug.com/chromium/431418 (reported by the same fuzzer). I think what's happening is that it's trying to drag an image which fails to decode.

This is another example of a call site (of which I'd previously found and fixed two) where we assume that SkBitmap always decodes successfully -- but in fact, it is possible for locking the pixels to result in failed decode. In that case, accessing the pixels is still illegal.

I'll take care of this.

### jb...@chromium.org (2015-02-05)

[Empty comment from Monorail migration]

### dc...@chromium.org (2015-02-05)

[Empty comment from Monorail migration]

### jb...@chromium.org (2015-02-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-02-05)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=189585

------------------------------------------------------------------
r189585 | jbroman@chromium.org | 2015-02-05T20:57:03.396164Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/DragImage.cpp?r1=189585&r2=189584&pathrev=189585

Clear SkBitmap used to draw DragImage.

SkBitmap::allocN32Pixels does not initialize the pixel memory, and we
may not draw to all of it (if, for example, an image decode fails,
nothing will be drawn).

BUG=450389

Review URL: https://codereview.chromium.org/901223002
-----------------------------------------------------------------

### jb...@chromium.org (2015-02-05)

I'd like to merge r189585 to M41 (beta). I'm not convinced this is critical enough to merge to stable, as in the worst case garbage pixels from the renderer are in the drag image, which doesn't seem easily exploitable.

### pe...@chromium.org (2015-02-06)

Has the fix been verified in trunk/canary?  As long as you're confident, I'll approve it for now for M41 branch 2272.

(Changing your status to Fixed/Verified, and allowing soak time in at least one canary will help make merge requests easier.)

### jb...@chromium.org (2015-02-09)

It's trivial, and it has now been in canary for awhile. Merging.

### bu...@chromium.org (2015-02-09)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=189816

------------------------------------------------------------------
r189816 | jbroman@chromium.org | 2015-02-09T17:13:17.354646Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/graphics/BitmapImage.cpp?r1=189816&r2=189815&pathrev=189816
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/DragImageTest.cpp?r1=189816&r2=189815&pathrev=189816
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/graphics/BitmapImage.h?r1=189816&r2=189815&pathrev=189816

Unit test for non-default orientation images which don't produce pixels.

This is a unit test based on the fuzzer-reported bug, which fails in an
MSAN build. This set of conditions is somewhat odd, but it's required to
trigger the code path in question.

BUG=450389

Review URL: https://codereview.chromium.org/877553011
-----------------------------------------------------------------

### bu...@chromium.org (2015-02-09)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=189824

------------------------------------------------------------------
r189824 | jbroman@chromium.org | 2015-02-09T18:20:26.366949Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2272/Source/platform/DragImage.cpp?r1=189824&r2=189823&pathrev=189824

Merge 189585 "Clear SkBitmap used to draw DragImage."

> Clear SkBitmap used to draw DragImage.
> 
> SkBitmap::allocN32Pixels does not initialize the pixel memory, and we
> may not draw to all of it (if, for example, an image decode fails,
> nothing will be drawn).
> 
> BUG=450389
> 
> Review URL: https://codereview.chromium.org/901223002

TBR=fmalita@chromium.org

Review URL: https://codereview.chromium.org/872923003
-----------------------------------------------------------------

### jb...@chromium.org (2015-02-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-10)

[Empty comment from Monorail migration]

### ti...@google.com (2015-02-26)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-03)

Congrats - $1000 for this report.

Notes from reward panel: $500 for the bug + $500 ClusterFuzz bonus.

### ti...@google.com (2015-03-11)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-11)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-17)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2015-05-18)

Bulk update: removing view restriction from closed bugs.

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

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/450389?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081228)*
