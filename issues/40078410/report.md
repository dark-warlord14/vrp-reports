# Heap-use-after-free in WebCore::ChannelProvider::provideInput

| Field | Value |
|-------|-------|
| **Issue ID** | [40078410](https://issues.chromium.org/issues/40078410) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media>Audio |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ha...@chromium.org |
| **Created** | 2013-11-16 |
| **Bounty** | $500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5123869056696320

Fuzzer: Attekett_webaudio_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61100000a0f8
Crash State:
  - crash stack -
  WebCore::ChannelProvider::provideInput
  WebCore::SincResampler::consumeSource
  - free stack -
  WebCore::HTMLMediaElement::clearMediaPlayer
  WebCore::HTMLMediaElement::userCancelledLoad
  


Fully reproducible crash found using linux_tsan_chrome_mp job type (history_size=6).
Additional requirements: Requires Interaction Gestures

## Timeline

### in...@chromium.org (2013-11-16)

Haraken@, this looks like similar data races bug you fixed in webaudio. Can you please fix this one too. Thanks!

### cl...@chromium.org (2013-11-17)

Adding milestone and impact labels.

### cl...@chromium.org (2013-11-17)

Fixing bug priority based on security_severity-* and releaseblock-* labels.

### cl...@chromium.org (2013-11-26)

haraken@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

- Your friendly ClusterFuzz

### ha...@chromium.org (2013-11-26)

Sorry, I noticed the bug now.

Uploaded a CL:
https://codereview.chromium.org/88183002/


### ha...@chromium.org (2013-11-26)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-11-27)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=162730

------------------------------------------------------------------------
r162730 | haraken@chromium.org | 2013-11-27T02:59:17.746720Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/HTMLMediaElement.h?r1=162730&r2=162729&pathrev=162730
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/HTMLMediaElement.cpp?r1=162730&r2=162729&pathrev=162730

HTMLMediaElement::clearMediaPlayer should acquire MediaElementAudioSourceNode::lock()

Crash report: https://cluster-fuzz.appspot.com/testcase?key=5123869056696320

There is threading race between HTMLMediaElement::clearMediaPlayer and other methods which try to use HTMLMediaElement::m_player. clearMediaPlayer has to acquire a lock before clearing m_player, just like createMediaPlayer is acquiring the lock before clearing m_player.

c.f., https://chromiumcodereview.appspot.com/23691033/ is a CL that added the lock to createMediaPlayer.

BUG=320344

Review URL: https://codereview.chromium.org/88183002
------------------------------------------------------------------------

### in...@chromium.org (2013-11-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-11-27)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### in...@chromium.org (2013-11-27)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-12-02)

Not much bake time for M31. We should just merge to m32. Adding Merge-Requested.

### ka...@google.com (2013-12-05)

let's let this bake more. haraken any fall out from it?

### ha...@chromium.org (2013-12-05)

I haven't seen anything harmful caused by the fix.

### ka...@google.com (2013-12-09)

haraken this is all ok?

### ha...@chromium.org (2013-12-10)

Merged into m32.

### bu...@chromium.org (2013-12-10)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=163479

------------------------------------------------------------------------
r163479 | haraken@chromium.org | 2013-12-10T01:32:01.675381Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1700/Source/core/html/HTMLMediaElement.cpp?r1=163479&r2=163478&pathrev=163479
   M http://src.chromium.org/viewvc/blink/branches/chromium/1700/Source/core/html/HTMLMediaElement.h?r1=163479&r2=163478&pathrev=163479

Merge 162730 "HTMLMediaElement::clearMediaPlayer should acquire ..."

> HTMLMediaElement::clearMediaPlayer should acquire MediaElementAudioSourceNode::lock()
> 
> Crash report: https://cluster-fuzz.appspot.com/testcase?key=5123869056696320
> 
> There is threading race between HTMLMediaElement::clearMediaPlayer and other methods which try to use HTMLMediaElement::m_player. clearMediaPlayer has to acquire a lock before clearing m_player, just like createMediaPlayer is acquiring the lock before clearing m_player.
> 
> c.f., https://chromiumcodereview.appspot.com/23691033/ is a CL that added the lock to createMediaPlayer.
> 
> BUG=320344
> 
> Review URL: https://codereview.chromium.org/88183002

TBR=haraken@chromium.org

Review URL: https://codereview.chromium.org/111163002
------------------------------------------------------------------------

### mb...@chromium.org (2013-12-10)

Thanks for the report! This one qualifies for a $500 reward. Race conditions usually qualify at this reward level because they can be difficult to exploit reliably.

### pa...@chromium.org (2013-12-18)

[Empty comment from Monorail migration]

### dh...@google.com (2014-01-08)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-28)

Bulk update: removing view restriction from closed bugs.

### gl...@chromium.org (2015-06-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### ss...@google.com (2016-03-21)

Renaming Blink>Audio to Blink>Media>Audio for better characterization

[Monorail components: -Blink>Audio Blink>Media>Audio]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/320344?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078410)*
