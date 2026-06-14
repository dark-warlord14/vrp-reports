# Out of bound read when using modified webp file

| Field | Value |
|-------|-------|
| **Issue ID** | [40085594](https://issues.chromium.org/issues/40085594) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Reporter** | ch...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2010-12-03 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

Attached random.html file displays a webp image which will cause an assert failiure on third\_party/libwebp/dsp.c at

static inline uint8\_t clip\_8b(int v) {  

assert(v >= -255 && v <= 255 + 255);  

return clip1[255 + v];  

}  

Without the assert it will read values out of the boundaries of clip1 array.

**VERSION**  

Chrome Version: [9.0.600.0 (65624)] + [dev]  

Operating System: [Ubuntu 10.04]

**REPRODUCTION CASE**  

Please run random.html

Type of crash: tab  

Crash State: stack trace

58 clip\_8b() /media/Data/chromium/home/chrome-svn/tarball/chromium/src/third\_party/libwebp/dsp.c:54 0x0a65fbe1  

57 Transform() /media/Data/chromium/home/chrome-svn/tarball/chromium/src/third\_party/libwebp/dsp.c:93 0x0a65fdf8  

56 VP8ReconstructBlock() /media/Data/chromium/home/chrome-svn/tarball/chromium/src/third\_party/libwebp/frame.c:354 0x0a662e29  

55 ParseFrame() /media/Data/chromium/home/chrome-svn/tarball/chromium/src/third\_party/libwebp/vp8.c:537 0x0a65f4d0  

54 VP8Decode() /media/Data/chromium/home/chrome-svn/tarball/chromium/src/third\_party/libwebp/vp8.c:589 0x0a65f6e3  

53 DecodeInto() /media/Data/chromium/home/chrome-svn/tarball/chromium/src/third\_party/libwebp/webp.c:366 0x0a65d3be  

52 WebPDecodeBGRInto() /media/Data/chromium/home/chrome-svn/tarball/chromium/src/third\_party/libwebp/webp.c:410 0x0a65d4e9

## Attachments

- [random.html](attachments/random.html) (text/html; charset=us-ascii, 85 B)
- [test_random.webp](attachments/test_random.webp) (application/octet-stream; charset=binary, 4.8 KB)

## Timeline

### [Deleted User] (2010-12-03)

I can't repro renderer crash with Chromium 10.0.602.0 (Developer Build 68176) and Google Chrome 9.0.597.4 (Official Build 67950) on Win 7.

What OS is this on?

### ch...@gmail.com (2010-12-04)

OS is Ubuntu 10.04. Renderer crash happens only in debug build due to assert fail.

### sc...@gmail.com (2010-12-16)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-12-17)

Seems to be the same as 66591. With the fix for 66591, this file decodes OK and is also clean under valgrind (as is the repro for 66591 now).

### sc...@gmail.com (2010-12-17)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-12-20)

Actually, let's track this properly as a separate issue.

---
Fixed in internal repository: CL 18681876
Needs to be imported into Chromium.
---

### bu...@chromium.org (2010-12-21)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=69824

------------------------------------------------------------------------
r69824 | cevans@chromium.org | Tue Dec 21 05:52:27 PST 2010

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libwebp/README.chromium?r1=69824&r2=69823&pathrev=69824
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libwebp/dsp.c?r1=69824&r2=69823&pathrev=69824
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libwebp/bits.h?r1=69824&r2=69823&pathrev=69824
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libwebp/webp.c?r1=69824&r2=69823&pathrev=69824
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libwebp/tree.c?r1=69824&r2=69823&pathrev=69824
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libwebp/vp8i.h?r1=69824&r2=69823&pathrev=69824
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libwebp/frame.c?r1=69824&r2=69823&pathrev=69824
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libwebp/vp8.c?r1=69824&r2=69823&pathrev=69824
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libwebp/bits.c?r1=69824&r2=69823&pathrev=69824

Update libwebp from upstream repository.
Start to track an accurate lineage in README.chromium.

BUG=62276,64945,65299
TEST=added upstream

Review URL: http://codereview.chromium.org/6013003
------------------------------------------------------------------------

### bu...@chromium.org (2010-12-21)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=69826

------------------------------------------------------------------------
r69826 | cevans@chromium.org | Tue Dec 21 06:57:20 PST 2010

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/597/src/third_party/libwebp/dsp.c?r1=69826&r2=69825&pathrev=69826
 M http://src.chromium.org/viewvc/chrome/branches/597/src/third_party/libwebp/README.chromium?r1=69826&r2=69825&pathrev=69826
 M http://src.chromium.org/viewvc/chrome/branches/597/src/third_party/libwebp/bits.c?r1=69826&r2=69825&pathrev=69826
 M http://src.chromium.org/viewvc/chrome/branches/597/src/third_party/libwebp/bits.h?r1=69826&r2=69825&pathrev=69826
 M http://src.chromium.org/viewvc/chrome/branches/597/src/third_party/libwebp/webp.c?r1=69826&r2=69825&pathrev=69826
 M http://src.chromium.org/viewvc/chrome/branches/597/src/third_party/libwebp/tree.c?r1=69826&r2=69825&pathrev=69826
 M http://src.chromium.org/viewvc/chrome/branches/597/src/third_party/libwebp/vp8i.h?r1=69826&r2=69825&pathrev=69826
 M http://src.chromium.org/viewvc/chrome/branches/597/src/third_party/libwebp/frame.c?r1=69826&r2=69825&pathrev=69826
 M http://src.chromium.org/viewvc/chrome/branches/597/src/third_party/libwebp/vp8.c?r1=69826&r2=69825&pathrev=69826

Merge 69824 - Update libwebp from upstream repository.
Start to track an accurate lineage in README.chromium.

BUG=62276,64945,65299
TEST=added upstream

Review URL: http://codereview.chromium.org/6013003

TBR=cdn@chromium.org
Review URL: http://codereview.chromium.org/6002004
------------------------------------------------------------------------

### sc...@gmail.com (2010-12-21)

Fix will be in the next Beta version.

### sc...@gmail.com (2010-12-22)

@chamal.desilva -- congratulations! This bug provisionally qualifies for a $500 Chromium Security Reward.
We do not normally reward SecSeverity-Medium issues, but in this case there are a couple of factors to consider:
1) You gave a great, reliable repro and included details of the exact code fault involved.
2) The panel was particularly impressed with your performance in https://crbug.com/chromium/66591 -- especially the ninja debug skills. It's a shame that bug was a duplicate and that the bug had already been fixed.

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### ch...@gmail.com (2010-12-22)

Wow. This is really great. Thanks a lot! :)

### sc...@gmail.com (2010-12-22)

@chamal.desilva: you're welcome! I hope this is the first but not the last reward :)

E-mail cevans@chromium.org to collect the reward.

### sc...@gmail.com (2011-01-18)

Invoice finalized; payment is in e-payment system.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update: assuming these security changes did not impact stable based on some fuzzy filtering.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/65299?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085594)*
