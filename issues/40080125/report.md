# Security: Crash in memcpy in chrome_pdf::CopyImage

| Field | Value |
|-------|-------|
| **Issue ID** | [40080125](https://issues.chromium.org/issues/40080125) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2014-07-29 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase with the attached example.pdf crashes chrome on Windows and Linux. The latest ASAN build and the current release version are affected. The example.pdf file is not corrupted as far as I am aware.

**VERSION**  

Chrome Version: All current versions  

Operating System: Linux and Windows

**REPRODUCTION CASE**

<script>
function start() {
ifr=document.createElement("iframe");
try{ifr.setAttribute('src','example.pdf');}catch(e){}
try{document.body.appendChild(ifr)}catch(e){}
try{ifr.width='55';}catch(e){}
try{ifr.height='47';}catch(e){}
}
</script>
<body onload="start()"></body>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: ASAN output attached in debug.txt (the top frame seems to be bogus)

## Attachments

- [example.pdf](attachments/example.pdf) (application/pdf, 13.7 KB)
- [crash.html](attachments/crash.html) (text/html, 272 B)
- [debug.txt](attachments/debug.txt) (text/plain, 3.9 KB)

## Timeline

### in...@chromium.org (2014-07-29)

This looks same stack as https://code.google.com/p/chromium/issues/detail?id=350782. Chris, can you please check. Has your change rolled to chromium yet ?

### cl...@chromium.org (2014-07-29)

[Empty comment from Monorail migration]

### ke...@chromium.org (2014-08-01)

I can confirm that this is not fixed by Chris' patch. It is the same line crashing -- the memcpy in CopyImage(), but the destination address is bad. It's not immediately obvious to me how this is happening, but this might be useful, inspecting the input parameters:
dest_rc.width() = 40
dest_rc.height() = 47
src_rc.width() = 40
src_rc.height() = 47
dest_rc.point() = {x = -31, y = 0}
src_rc.point() = {x = 0, y = 0}

### cl...@chromium.org (2014-08-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-08-05)

Bo, can you please take a look.

### pa...@chromium.org (2014-08-05)

I looked around at this bug a bit yesterday, and the problem seems to occur only when dest_rc.point() = {x = -31, y = 0} (or perhaps more generally when either x or y are negative). A negative |x| causes this line:

    uint32_t* dest_origin_pixel = dest->GetAddr32(dest_rc.point());

to fetch a bad |dest_origin_pixel|. The explosion then happens immediately on this line:

    memcpy(dest_origin_pixel, src_origin_pixel, width_bytes.ValueOrDie());

I don't know the code well enough to know if negative x, y coordinates are expected, or should have been stopped earlier in the call stack, or what. jam seems to be the owner of that code.

### cl...@chromium.org (2014-08-12)

bo_xu@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-08-18)

[Empty comment from Monorail migration]

### bo...@foxitsoftware.com (2014-08-19)

@Jam, can you take a look at this one? Thanks.

### cl...@chromium.org (2014-08-26)

jam@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### in...@chromium.org (2014-08-26)

I don't think John has any cycles for fixing bugs. Chris, Tom, can you please pick this one up, this is hitting a lot.

### pa...@chromium.org (2014-08-28)

I'll take it.

### pa...@chromium.org (2014-08-29)

tsepez is even more on it.

### ts...@chromium.org (2014-08-29)

CL at https://codereview.chromium.org/519873002/

### ts...@chromium.org (2014-08-29)

The CL in #14 add necessary protection from bad callers, but the underlying math bug appears to be at or around control.cc:56
   pp::Rect ctrl_rc = pp::Rect(rect().point() - draw_rc.point(), draw_rc.size())

Most of the time rect().point() == draw_rc.point(), the exceptions being when the control starts (even partially) before the image bounds or starts completely after the image bounds. In the later case, nothing is drawn, so that doesn't affect the results either.  But in the former case, we've done the subtraction the wrong way, and what we really want is:
  pp::Rect ctrl_rc = pp::Rect(draw_rc.point() - rect().point(), draw_rc.size())



### bu...@chromium.org (2014-09-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d734d197bb5462a65c37b17594a8c8d07dd79bc1

commit d734d197bb5462a65c37b17594a8c8d07dd79bc1
Author: tsepez <tsepez@chromium.org>
Date: Wed Sep 03 23:17:49 2014

Avoid OOB memcpy in chrome_pdf::CopyImage.

This is a re-work of palmer's patch at https://codereview.chromium.org/515023002/ which has more context, but comes down to stricter bounds checking.

We also correct an arithmetic bug when copying the image behind a control that is positioned before the origin of the image.

BUG=398384

Review URL: https://codereview.chromium.org/519873002

Cr-Commit-Position: refs/heads/master@{#293213}

[modify] https://chromium.googlesource.com/chromium/src.git/+/d734d197bb5462a65c37b17594a8c8d07dd79bc1/pdf/control.cc
[modify] https://chromium.googlesource.com/chromium/src.git/+/d734d197bb5462a65c37b17594a8c8d07dd79bc1/pdf/draw_utils.cc


### ts...@chromium.org (2014-09-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-04)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@chromium.org (2014-09-23)

Matthew - Merge Requested for M38 (Branch 2125)

### [Deleted User] (2014-09-24)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-09-24)

tsepez@ - please merge to M38 / branch 2125

### bu...@chromium.org (2014-09-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4c4ee16baaba129a883d38b819ca637139665d93

commit 4c4ee16baaba129a883d38b819ca637139665d93
Author: Tom Sepez <tsepez@chromium.org>
Date: Thu Sep 25 19:07:13 2014

Avoid OOB memcpy in chrome_pdf::CopyImage.

This is a re-work of palmer's patch at https://codereview.chromium.org/515023002/ which has more context, but comes down to stricter bounds checking.

We also correct an arithmetic bug when copying the image behind a control that is positioned before the origin of the image.

BUG=398384
TBR=gene@chromium.org

Review URL: https://codereview.chromium.org/519873002

Cr-Commit-Position: refs/heads/master@{#293213}
(cherry picked from commit d734d197bb5462a65c37b17594a8c8d07dd79bc1)

Review URL: https://codereview.chromium.org/602173003

Cr-Commit-Position: refs/branch-heads/2125@{#483}
Cr-Branched-From: b68026d94bda36dd106a3d91a098719f952a9477-refs/heads/master@{#290040}

[modify] https://chromium.googlesource.com/chromium/src.git/+/4c4ee16baaba129a883d38b819ca637139665d93/pdf/control.cc
[modify] https://chromium.googlesource.com/chromium/src.git/+/4c4ee16baaba129a883d38b819ca637139665d93/pdf/draw_utils.cc


### ti...@chromium.org (2014-10-03)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-10-03)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-10-07)

Congrats - $3000 for this under our new pricing structure. Notes from the reward panel: "nice control over memcopy argmument with setting width and height".

### ti...@google.com (2014-12-08)

Payment in progress

### ti...@google.com (2014-12-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-11)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2014-12-22)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

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

This issue was migrated from crbug.com/chromium/398384?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080125)*
