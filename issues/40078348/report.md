# Security: ASAN heap-use-after-free in AnimationController::endAnimationUpdate

| Field | Value |
|-------|-------|
| **Issue ID** | [40078348](https://issues.chromium.org/issues/40078348) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Animation |
| **Reporter** | cl...@gmail.com |
| **Assignee** | mi...@chromium.org |
| **Created** | 2013-11-06 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

The attached testcase crashes the latest chrome asan build.

**VERSION**  

Chrome Version: asan-symbolized-linux-release-232951  

Operating System: Linux 64-bit

**REPRODUCTION CASE**  

Attached in crash.zip as it requires multiple files to trigger.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: ASAN output attached in stack.txt

## Attachments

- [crash.zip](attachments/crash.zip) (application/zip; charset=binary, 713 B)
- [stack.txt](attachments/stack.txt) (text/plain; charset=us-ascii, 13.6 KB)

## Timeline

### cl...@chromium.org (2013-11-06)

ClusterFuzz is now working on this testcase. See https://cluster-fuzz.appspot.com/testcase?key=5642767879372800

### cl...@chromium.org (2013-11-07)

Adding area label based on an intelligent guess!

dstockwell: Can you please take a look or find someone else to own it.

- Your friendly ClusterFuzz

### ae...@chromium.org (2013-11-08)

Reproduces on about half of the runs on 32.0.1701.0.

### cl...@chromium.org (2013-11-09)

[Comment Deleted]

### cl...@chromium.org (2013-11-11)

[Comment Deleted]

### ts...@chromium.org (2013-11-12)

[Comment Deleted]

### ts...@chromium.org (2013-11-12)

We know it hits beta. Retrying CF regression range to see if it hits stable.

### cl...@chromium.org (2013-11-15)

dstockwell@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!)

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### in...@chromium.org (2013-11-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-11-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-11-24)

mikelawther@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

- Your friendly ClusterFuzz

### mi...@chromium.org (2013-11-25)

I cannot repro with the supplied testcase in 33.0.1718.0 (Official Build 236956) canary on MacOS.

Clusterfuzz is showing 'unreproducible'. Or is it only flakily reproducible?

### in...@chromium.org (2013-11-25)

ClusterFuzz did try it 20-30 times before reaching the conclusion of not reproducible. If it reproduced atleast once, it would put the stacktrace in report and confirmed:no in report.

cloudfuzzer@, are you still able to repro it. Can you please try to make it more reproduceable. Thanks!

### cl...@gmail.com (2013-11-25)

Still reproduces reliably for me in asan-symbolized-linux-release-237021.

Both from the local file system (--allow-file-access-from-files) and from a web server (after a reload).

Have tried to reproduce it with different window sizes?

mikelawther@: Is your MacOS build an ASAN build?

### cl...@chromium.org (2013-11-26)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-11-26)

[Empty comment from Monorail migration]

### mi...@chromium.org (2013-12-02)

No - it was a standard build.

### mi...@chromium.org (2013-12-04)

OK - I've built content_shell with ASAN on linux at Chromium r238234 (Blink r162991) and I can repro (4 times out of 5) the use-after-free.

### ka...@google.com (2013-12-04)

so one step closer :)

### in...@chromium.org (2013-12-06)

Does this look like https://cluster-fuzz.appspot.com/testcase?key=5068686729674752. If yes, then this would be fixed with http://code.google.com/p/chromium/issues/detail?id=265889. Marty, can you please check and if the same, please dupe it. I think http://src.chromium.org/viewvc/blink?view=rev&revision=163261 fixed it. Also clicked redo on CF to confirm.

### tk...@chromium.org (2013-12-09)

I don't think this issue is related to https://crbug.com/chromium/265889 and r163261.
Looks like we just need "RefPtr<Frame> protector(m_frame)" in Document::updateStyleIfNeeded.


### cl...@chromium.org (2013-12-12)

mikelawther@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### in...@chromium.org (2013-12-16)

Assigning to tkent@ based on c#21.

### in...@chromium.org (2013-12-16)

ah! didnt see https://codereview.chromium.org/109263007/

### ka...@google.com (2013-12-16)

so we're pretty close to the end of M32 just heads up. next spin will be for stable.

### bu...@chromium.org (2013-12-17)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=164006

------------------------------------------------------------------------
r164006 | mikelawther@chromium.org | 2013-12-17T11:00:48.720059Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/frames/freed-frame.html?r1=164006&r2=164005&pathrev=164006
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/frames/resources/freed-frame-helper.html?r1=164006&r2=164005&pathrev=164006
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/frames/freed-frame-expected.txt?r1=164006&r2=164005&pathrev=164006
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/Document.cpp?r1=164006&r2=164005&pathrev=164006

Ensure the current frame is not lost during testing of whether a style
update is needed.

BUG=315889

Review URL: https://codereview.chromium.org/109263007
------------------------------------------------------------------------

### mi...@chromium.org (2013-12-17)

Requesting merge to m32, although I know it's probably too late in the cycle.

### in...@chromium.org (2013-12-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-12-24)

[Empty comment from Monorail migration]

### ka...@google.com (2014-01-02)

[Empty comment from Monorail migration]

### mi...@chromium.org (2014-01-09)

Merged to the 1700 branch in r164818.

### bu...@chromium.org (2014-01-10)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=164818

------------------------------------------------------------------------
r164818 | mikelawther@chromium.org | 2014-01-09T23:49:31.265771Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/1700/LayoutTests/fast/frames/resources/freed-frame-helper.html?r1=164818&r2=164817&pathrev=164818
   A http://src.chromium.org/viewvc/blink/branches/chromium/1700/LayoutTests/fast/frames/freed-frame-expected.txt?r1=164818&r2=164817&pathrev=164818
   M http://src.chromium.org/viewvc/blink/branches/chromium/1700/Source/core/dom/Document.cpp?r1=164818&r2=164817&pathrev=164818
   A http://src.chromium.org/viewvc/blink/branches/chromium/1700/LayoutTests/fast/frames/freed-frame.html?r1=164818&r2=164817&pathrev=164818

Merge 164006 "Ensure the current frame is not lost during testin..."

> Ensure the current frame is not lost during testing of whether a style
> update is needed.
> 
> BUG=315889
> 
> Review URL: https://codereview.chromium.org/109263007

TBR=mikelawther@chromium.org

Review URL: https://codereview.chromium.org/132883002
------------------------------------------------------------------------

### in...@chromium.org (2014-01-10)

This needs to be merged to m-33 as well (1750 branch). 

### la...@google.com (2014-01-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-01-16)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=165176

------------------------------------------------------------------------
r165176 | mikelawther@chromium.org | 2014-01-16T00:30:09.577184Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/1750/LayoutTests/fast/frames/freed-frame.html?r1=165176&r2=165175&pathrev=165176
   A http://src.chromium.org/viewvc/blink/branches/chromium/1750/LayoutTests/fast/frames/resources/freed-frame-helper.html?r1=165176&r2=165175&pathrev=165176
   A http://src.chromium.org/viewvc/blink/branches/chromium/1750/LayoutTests/fast/frames/freed-frame-expected.txt?r1=165176&r2=165175&pathrev=165176
   M http://src.chromium.org/viewvc/blink/branches/chromium/1750/Source/core/dom/Document.cpp?r1=165176&r2=165175&pathrev=165176

Merge 164006 "Ensure the current frame is not lost during testin..."

> Ensure the current frame is not lost during testing of whether a style
> update is needed.
> 
> BUG=315889
> 
> Review URL: https://codereview.chromium.org/109263007

TBR=mikelawther@chromium.org

Review URL: https://codereview.chromium.org/136033008
------------------------------------------------------------------------

### dh...@google.com (2014-01-23)

[Empty comment from Monorail migration]

### dh...@google.com (2014-01-23)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-01-27)

Thanks for the report! This one qualifies for a $3000 reward. There seems to be control between the free and use, and the freed object is not in a heap partition.

### ti...@chromium.org (2014-02-28)

Processing via our e-payment system can take a few weeks, but reward should be on its way to you. Please do NOT publicly disclose details until a fix has been released to all our users. Thanks again for your help!

### ti...@chromium.org (2014-03-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-04-01)

Bulk update: removing view restriction from closed bugs.

### cl...@chromium.org (2014-05-16)

This bug is a regression and does not impact stable. Removing incorrectly added Release-1-M32 label.

- Your friendly ClusterFuzz

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

This issue was migrated from crbug.com/chromium/315889?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078348)*
