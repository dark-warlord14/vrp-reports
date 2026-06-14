# Use-after-free in WebCore::TimerBase::stop

| Field | Value |
|-------|-------|
| **Issue ID** | [40077931](https://issues.chromium.org/issues/40077931) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Media>Video, Internals>Media |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ac...@chromium.org |
| **Created** | 2013-08-14 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

The attached testcase crashes the latest ASAN build of chrome. The issue seems to be timing depended, however it crashes for me reliable after a few reloads. I am using the following command line switches (note: gc has to be enabled):

--no-sandbox --incognito --allow-file-access-from-files --js-flags=--expose\_gc

**VERSION**  

Chrome Version: asan-symbolized-linux-release-217165  

Operating System: Linux 64bit

**REPRODUCTION CASE**  

The testcase is attached as a zip file, as it requires multiple files to reproduce.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: See attached stack.txt for ASAN output

10th bug report \o/

## Attachments

- [crash.zip](attachments/crash.zip) (application/zip; charset=binary, 33.9 KB)
- [stack.txt](attachments/stack.txt) (text/plain; charset=us-ascii, 11.7 KB)

## Timeline

### cl...@gmail.com (2013-08-14)

[Comment Deleted]

### cl...@gmail.com (2013-08-14)

Forgot to attached stack.txt

### cl...@chromium.org (2013-08-14)

ClusterFuzz is now working on this testcase. See https://cluster-fuzz.appspot.com/testcase?key=5521532713435136

### cl...@chromium.org (2013-08-14)

ClusterFuzz is now working on this testcase. See https://cluster-fuzz.appspot.com/testcase?key=5848049012178944

### cl...@chromium.org (2013-08-14)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5848049012178944

Uploader: inferno@chromium.org
Job Type: Windows_syzyasan_chrome

Crash Type: Use-after-free WRITE 8
Crash Address: 0x081409e7
Crash State:
  - crash stack -
  WebCore::TimerBase::stop
  WebCore::HTMLMediaElement::clearMediaPlayer
  - free stack -
  WebCore::HTMLVideoElement::`scalar deleting destructor'
  WebCore::ContainerNode::removeDetachedChildren
  




### in...@chromium.org (2013-08-14)

Reproduces under SyzyASAN reliably. does not reproduce reliably on linux.

### pa...@chromium.org (2013-08-14)

Adding fischman, who has touched HTMLMediaElement::clearMediaPlayer.

### pa...@chromium.org (2013-08-14)

[Empty comment from Monorail migration]

### fi...@chromium.org (2013-08-14)

Aaron's been messing with this stuff lately.  Might need a merge.

### in...@chromium.org (2013-09-03)

Aaron, friendly ping. I think you fixed almost similar bug some time back.

### cl...@chromium.org (2013-09-04)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5848049012178944

Uploader: inferno@chromium.org
Job Type: Windows_syzyasan_chrome

Crash Type: Use-after-free WRITE 8
Crash Address: 0x081409e7
Crash State:
  - crash stack -
  WebCore::TimerBase::stop
  WebCore::HTMLMediaElement::clearMediaPlayer
  - free stack -
  WebCore::HTMLVideoElement::`scalar deleting destructor'
  WebCore::ContainerNode::removeDetachedChildren
  




### ac...@chromium.org (2013-09-05)

I'll take a look later today or possibly tomorrow. I've got a code review backlog to dig out from.

### in...@chromium.org (2013-09-05)

Thanks Aaron.

### la...@google.com (2013-09-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-18)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### fi...@chromium.org (2013-09-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-27)

acolwell@: you haven't provided any bug update or come up with a fix for this issue in the last 7 days. Please note that this is a medium+ severity security vulnerability that needs your immediate response. If you have a patch in progress and don't want future nags, please add a codereview link and a WIP label. If the issue is already fixed or you can't reproduce it, please close the bug.

### ac...@chromium.org (2013-09-30)

Uploaded a potential fix but still need to write the LayoutTest. (https://codereview.chromium.org/25362002/)

### cl...@chromium.org (2013-10-01)

Fixing impact labels.

### ac...@chromium.org (2013-10-07)

The fix has landed in Blink. https://src.chromium.org/viewvc/blink?revision=159031&view=revision 

### in...@chromium.org (2013-10-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-10-07)

Adding Merge-Requested label.

Please do not merge your fix without first checking with the release manager. 

Once the merge is approved by the release manager, make sure to merge the fix to all the affected branches, i.e stable, beta and trunk (near branch point). You can find branch information on omahaproxy.appspot.com.

If the fix does not merge cleanly or is too risky on uptake on these branches, please change the M-* label to indicate the next milestone.

- Your friendly ClusterFuzz

### cl...@chromium.org (2013-10-07)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-10-08)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=159031

------------------------------------------------------------------------
r159031 | acolwell@chromium.org | 2013-10-07T16:27:25.426223Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/HTMLMediaElement.cpp?r1=159031&r2=159030&pathrev=159031
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/media/video-in-iframe-crash.html?r1=159031&r2=159030&pathrev=159031
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/media/video-in-iframe-crash-expected.txt?r1=159031&r2=159030&pathrev=159031

Block load event dispatching on old document when an HTMLMediaElement is moved between documents.

BUG=272786
TEST=LayoutTests/http/tests/media/video-in-iframe-crash.html

Review URL: https://codereview.chromium.org/25362002
------------------------------------------------------------------------

### in...@chromium.org (2013-10-11)

[Comment Deleted]

### cl...@chromium.org (2013-10-11)

[Comment Deleted]

### cl...@chromium.org (2013-10-11)

[Comment Deleted]

### cl...@chromium.org (2013-10-11)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone labels first. Make sure to re-request merge for every milestone in the Merge-To-M-* label. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### in...@chromium.org (2013-10-18)

[Empty comment from Monorail migration]

### la...@google.com (2013-10-18)

[Empty comment from Monorail migration]

### mb...@chromium.org (2013-10-22)

Thanks for the report! This one qualifies for a $2000 reward since there is control between the free and use.

### bu...@chromium.org (2013-10-23)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=160354

------------------------------------------------------------------------
r160354 | acolwell@chromium.org | 2013-10-23T18:35:24.046100Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1650/Source/core/html/HTMLMediaElement.cpp?r1=160354&r2=160353&pathrev=160354
   A http://src.chromium.org/viewvc/blink/branches/chromium/1650/LayoutTests/http/tests/media/video-in-iframe-crash.html?r1=160354&r2=160353&pathrev=160354
   A http://src.chromium.org/viewvc/blink/branches/chromium/1650/LayoutTests/http/tests/media/video-in-iframe-crash-expected.txt?r1=160354&r2=160353&pathrev=160354

Merge 159031 "Block load event dispatching on old document when ..."

> Block load event dispatching on old document when an HTMLMediaElement is moved between documents.
> 
> BUG=272786
> TEST=LayoutTests/http/tests/media/video-in-iframe-crash.html
> 
> Review URL: https://codereview.chromium.org/25362002

TBR=acolwell@chromium.org

Review URL: https://codereview.chromium.org/34313005
------------------------------------------------------------------------

### aa...@google.com (2013-10-23)

[Empty comment from Monorail migration]

### ac...@chromium.org (2013-10-23)

aarya: Does the label change mean that I shouldn't merge to M30?

### in...@chromium.org (2013-10-23)

yes there is no more m30 patches, so merge is not required anymore.

### ac...@chromium.org (2013-10-23)

ok. Thanks.

### mb...@chromium.org (2013-11-08)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-11-12)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-14)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-12-18)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-12-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-06)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### ss...@google.com (2016-03-21)

Renaming Blink>Video to Blink>Media>Video for better characterization

[Monorail components: -Blink>Video Blink>Media>Video]

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

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/272786?no_tracker_redirect=1

[Multiple monorail components: Blink>Media>Video, Internals>Media]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077931)*
