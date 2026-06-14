# Heap-use-after-free in content::WebMediaPlayerImpl::paint

| Field | Value |
|-------|-------|
| **Issue ID** | [40077784](https://issues.chromium.org/issues/40077784) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ac...@chromium.org |
| **Created** | 2013-07-14 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The attached testcase crashes the ASAN build of chrome. Seems like a vector is RuleSet vector is reallocated, a reference to the old vector might still exist.

**VERSION**  

Chrome Version: asan-symbolized-linux-release-211418  

Operating System: Linux 64-bit

**REPRODUCTION CASE**  

The testcase is attached as a zip file as it requires multiple files. Loading crash.html will crash the browser tab.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: ASAN output attached in crash.log

## Attachments

- [crash.zip](attachments/crash.zip) (application/zip; charset=binary, 32.0 KB)
- [crash.log](attachments/crash.log) (text/plain; charset=us-ascii, 19.0 KB)

## Timeline

### cl...@chromium.org (2013-07-15)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4768666486833152

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x612000025400
Crash State:
  - crash stack -
  content::WebMediaPlayerImpl::paint
  WebKit::WebMediaPlayerClientImpl::paintCurrentFrameInContext
  - free stack -
  WebCore::FrameLoader::~FrameLoader
  WebCore::Frame::~Frame
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=173501:173658

Minimized Testcase (32.12 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95M3pP6nV6Kt3Z2E6tstMxmAbB9-nJVIq0ZGhTlDpmbPIn3NeAJJcq3ibLrSswnGkwyt86DWCzCupoQb8yh6S9HJjHAghEq4-iBQg6Lp_0fCtIQq6FTG09Ye3CQKhEtkm-gp7CA3otIG2N57gLYswqTBfsO70P6sEPBm7u6qGM_1Aq1ywM



### in...@chromium.org (2013-07-15)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-07-15)

Regression from one of encrypted media changes
http://src.chromium.org/viewvc/chrome?view=rev&revision=173640
http://src.chromium.org/viewvc/chrome?view=rev&revision=173562

### xh...@chromium.org (2013-07-15)

It seems like WebMediaPlayerImpl::paint() tries to use the WebCore::Frame after it has been deleted. I can investigate more on this. But I don't understand why my CLs that are committed 6 months ago are marked as regressing CLs. AFAICT they are totally irrelevant to this issue. 

### in...@chromium.org (2013-07-15)

Those regression CLs were a guess from the regression range, i didn't see anything else that could be related to the media.

Thanks for taking a look. Can you own this or have ideas of an owner ?

### ac...@chromium.org (2013-07-15)

This reminds me of an issues I remember seeing a while ago. I haven't looked deeply at this particular repro case, but if the HTMLMediaElement some gets removed from an iframe and placed in the document w/o destroying WMPI you can run into problems. I thought one of my previous security fixes addressed this problem, but perhaps there is another code path that was missed.

### xh...@chromium.org (2013-07-16)

Yeah, this looks more like a Blink issue than a media/ issue.

I will be on vacation and won't be able to look into this. Remove myself as the owner for now.

acolwell@: Would you like to take a look since you seem to be more familiar with the issue?

### in...@chromium.org (2013-07-18)

Aaron, can you please take a look. This is the same stack as the bug you fixed in https://code.google.com/p/chromium/issues/detail?id=230117

### ac...@chromium.org (2013-07-18)

Yes. I'll take a look at this today.

### bu...@chromium.org (2013-07-22)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=154696

------------------------------------------------------------------------
r154696 | acolwell@chromium.org | 2013-07-22T23:46:57.533178Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/HTMLMediaElement.cpp?r1=154696&r2=154695&pathrev=154696

Prevent WebMediaPlayerImpl from dereferencing stale Frame pointers on Document changes.

Temporary fix to prevent dereferencing stale Frame pointers when an HTMLMediaElement is
moved from one document to another. (e.g., Lifting it out of an iframe into the
main document.)

BUG=260156

Review URL: https://chromiumcodereview.appspot.com/19693009
------------------------------------------------------------------------

### in...@chromium.org (2013-07-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-07-23)

ClusterFuzz has detected this issue as fixed in range 213073:213078.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4768666486833152

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x612000025400
Crash State:
  - crash stack -
  content::WebMediaPlayerImpl::paint
  WebKit::WebMediaPlayerClientImpl::paintCurrentFrameInContext
  - free stack -
  WebCore::FrameLoader::~FrameLoader
  WebCore::Frame::~Frame
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=173501:173658
Fixed: https://cluster-fuzz.appspot.com/revisions?range=213073:213078

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95M3pP6nV6Kt3Z2E6tstMxmAbB9-nJVIq0ZGhTlDpmbPIn3NeAJJcq3ibLrSswnGkwyt86DWCzCupoQb8yh6S9HJjHAghEq4-iBQg6Lp_0fCtIQq6FTG09Ye3CQKhEtkm-gp7CA3otIG2N57gLYswqTBfsO70P6sEPBm7u6qGM_1Aq1ywM

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2013-07-31)

@acolwell: I wonder if it's worth adding a test for this case?

M29: http://src.chromium.org/viewvc/blink?view=rev&rev=155210

### bu...@chromium.org (2013-07-31)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=155210

------------------------------------------------------------------------
r155210 | cevans@chromium.org | 2013-07-31T02:45:33.112721Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1547/Source/core/html/HTMLMediaElement.cpp?r1=155210&r2=155209&pathrev=155210

Merge 154696 "Prevent WebMediaPlayerImpl from dereferencing stal..."

> Prevent WebMediaPlayerImpl from dereferencing stale Frame pointers on Document changes.
> 
> Temporary fix to prevent dereferencing stale Frame pointers when an HTMLMediaElement is
> moved from one document to another. (e.g., Lifting it out of an iframe into the
> main document.)
> 
> BUG=260156
> 
> Review URL: https://chromiumcodereview.appspot.com/19693009

TBR=acolwell@chromium.org

Review URL: https://codereview.chromium.org/21317003
------------------------------------------------------------------------

### sc...@gmail.com (2013-08-11)

Nice, $1000, etc.!

### pa...@chromium.org (2013-08-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-08-19)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-08-19)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/260156?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077784)*
