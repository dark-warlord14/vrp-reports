# DCHECK failure at blink::WebFrameWidgetImpl::DragTargetDragEnter

| Field | Value |
|-------|-------|
| **Issue ID** | [40059378](https://issues.chromium.org/issues/40059378) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>DataTransfer |
| **Platforms** | Android, Windows |
| **Reporter** | rz...@gmail.com |
| **Assignee** | mu...@chromium.org |
| **Created** | 2022-04-14 |
| **Bounty** | $1,500.00 |

## Description

**VULNERABILITY DETAILS**

UAF in blink::WebFrameWidgetImpl::DragTargetDragEnter [1].

The copy of the web drop data object (which is v8's `Member` object) received  

from the browser been accessed upon destroying.

[1] <https://source.chromium.org/chromium/chromium/src/+/refs/tags/102.0.4962.0:third_party/blink/renderer/core/frame/web_frame_widget_impl.cc;l=379;bpv=1;bpt=1>

**VERSION**

Chrome Version: 102.0.4962.0  

Operating System: Android - API 11  

Build: Debug

**REPRODUCTION CASE**

1. Lauch the poc.html in chromium android.
2. Click and hold the link for a second or atleast till the "here" message is  
   
   visible on console window (if opened via chrome://inspect) and drag the link.
3. Observe the crash.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

Type of crash: Renderer  

Crash State: crash.log

**CREDIT INFORMATION**  

Reporter credit: Sri

## Attachments

- [crash.log](attachments/crash.log) (text/plain, 16.1 KB)
- [poc.html](attachments/poc.html) (text/plain, 787 B)
- [crash.log](attachments/crash.log) (text/plain, 16.2 KB)
- [asan-lib-crash.log](attachments/asan-lib-crash.log) (text/plain, 4.0 KB)

## Timeline

### [Deleted User] (2022-04-14)

[Empty comment from Monorail migration]

### rz...@gmail.com (2022-04-14)

Didn't have the necessary resources to build the `userdebug` and flash the same on Pixel. However tried something in this direction on Samsung Galaxy but didn't succeed. However, attached is the log that was reproduced a couple of days ago.

### mp...@chromium.org (2022-04-19)

This appears to be a DCHECK failure. Can you demonstrate how this would lead to UAF?

(FWIW I could not reproduce this on an Android emulator with M101).

### mp...@chromium.org (2022-04-19)

xiaochengh@ would you mind triaging this and assessing severity? I'm not sure assigning any clipboard content to innerHTML should ever be considered secure, but perhaps I'm wrong?

[Monorail components: Blink>DataTransfer]

### [Deleted User] (2022-04-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-19)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-19)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xi...@chromium.org (2022-04-21)

I don't see how this is a UAF. rzintct@, could you elaborate?

I'm not familiar with this part of code, either. Unassigning myself to allow finding a better owner.

### mp...@google.com (2022-04-21)

Oh, I most certainly posted on the wrong bug. That comment was supposed to go on https://crbug.com/chromium/1315563.

wenyufu@ can you PTAL at this bug?

### mp...@google.com (2022-04-21)

[Empty comment from Monorail migration]

### we...@chromium.org (2022-04-21)

mustaq@ can you help evaluate how this should be fixed? It seems Blink is not handling Android drop data lifecycle

### rz...@gmail.com (2022-04-22)

Re https://crbug.com/chromium/1316301#c8: Shall try it on an asan build. But, I'm afriad it would take another 4 days to find some time to spend on this. 

### [Deleted User] (2022-04-28)

mustaq: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@gmail.com (2022-04-30)

seems like this issue is getting triggered when there's an attempt to process the input event after input event receiver has already been destroyed - during the process of dropping event (`MotionEvent`) due to the root view being removed. 

### mu...@chromium.org (2022-05-06)

The bug does not repro for me on Chrome 103.0.5043.0 on Android 12.  I tried turning on/off "simultaneous touch drag and context menu" in chrome://flags.

rzintct@gmail.com: Could you please confirm if changing this flag affects your repro?

### mu...@chromium.org (2022-05-11)

rzintct@gmail.com: I can't still repro.  Please check if your repro changes with the flag mentioned in https://crbug.com/chromium/1316301#c15.

### rz...@gmail.com (2022-05-12)

Yes, same at my end. In 103.0.5043.0 on Android 12, crash is not reproduced if we turn the "simultaneous touch drag and context menu" flag off. 

Also, tried to reproduce the same on an asan build. Unfortunately, there is a bug in asan library - triggering heap-buffer-overflow. Not allowing me proceed and test effectively. Please check the attachment. 

 

### mu...@chromium.org (2022-05-12)

Sorry still can't repro!

rzintct@gmail.com: Want to clarify the repro steps again.  Is this a sequence of steps that reproduces the bug for you?
1'. Long-press on the link => context-menu appears.
2'. Keep the finger steady until the iframe disappears after 3.1 seconds.
3'. Start dragging.

Assuming this is the sequence, do you see the crash after Step 2' or Step 3'?

### rz...@gmail.com (2022-05-12)

Crash is happening in 102.0.4962.0, Android 11. didn't check in other versions. 

1. Yes. Select and Long press the link till context menu appears.
2. Yes. Not presicely for 3 seconds. But till you find "here" on console.
3. Yes. Drag / move the link slightly, in which ever the way you want - this is to simulate MotionEvent.


This is still happening at my end. 


### mu...@chromium.org (2022-05-12)

Thanks rzintct@gmail.com for being super-responsive.

While I can't still repro, I can see how the the DCHECK may not hold after a child-frame is nuked.  Sending out a tentative fix for review, hopefully it will work for you.

### mu...@chromium.org (2022-05-24)

After investing further, I failed to find a convincing reason for the crash.  I still believe it's a DCHECK failure but can't confirm without a repro.

Most importantly, I didn't see a UAF issue here, correcting the bug summary and priority accordingly.

For records, I noticed that (in side iframe or not) a long-press fires a DragTargetDragEnter+DragTargetDragOver call sequence at WebFrameWidgetImpl, then when the finger is moved there is a sequence of DragTargetDragEnter+DragTargetDragOver*+DragTargetDragLeave calls.  Apparently WFWI gets two separate drag sequences which are valid as a whole but not quite correct.

### mu...@chromium.org (2022-05-24)

Correction on the call sequence above:
- Longpress fires: DragTargetDragEnter+DragTargetDragOver
- Then finger drag fires: DragTargetDragLeave+DragTargetDragEnter+DragTargetDragOver*+DragTargetDragLeave


### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-08)

mustaq: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mu...@chromium.org (2022-06-08)

I don't think this is a security bug, see https://crbug.com/chromium/1316301#c21.  I am changing the bug type, but leaving the labels unchanged for the security team to review.

### mu...@chromium.org (2022-10-21)

A regression somewhere has exposed the DCHECK failure, see https://crbug.com/chromium/1367848.  This answers my query in https://crbug.com/chromium/1316301#c21 above.

This new data point proves the downgrading in https://crbug.com/chromium/1316301#c25 wrong!  Moving the bug back to the original state.

### [Deleted User] (2022-10-21)

[Empty comment from Monorail migration]

### mu...@chromium.org (2022-11-03)

[Comment Deleted]

### mu...@chromium.org (2022-11-03)

[Empty comment from Monorail migration]

### mu...@chromium.org (2022-11-08)

https://crbug.com/chromium/1367848 is on Windows.

### mu...@chromium.org (2022-11-08)

This looks very similar to https://crbug.com/chromium/1380759.  Not sure, so not merging them yet.

### mu...@chromium.org (2022-11-14)

#31 is not correct, that other bug is a recent regression.

### gi...@appspot.gserviceaccount.com (2022-11-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/88da1e1c25b97c0e40e5fe9dbe60e00c9d66b0f5

commit 88da1e1c25b97c0e40e5fe9dbe60e00c9d66b0f5
Author: Mustaq Ahmed <mustaq@google.com>
Date: Wed Nov 23 15:24:33 2022

Ensure WFWI::current_drag_data_ is null at the end of a drag.

This is a tentative fix for the DCHECK bugs below.  The bugs appeared at
two different times, but they share the common symptom that
WebFrameWidgetImpl::DragTargetDragEnter very infrequently encounters a
non-null current_drag_data_.  We were not able to repro the problem.

This tentative fix assumes that an early return on a drag-leave may
be accidentally skipping setting the state to null.

Bug: 1316301, 1367848
Change-Id: Ib6e9e000271515a0659a6780a59467db149d3b3f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3645670
Commit-Queue: Mustaq Ahmed <mustaq@chromium.org>
Reviewed-by: Robert Flack <flackr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1075157}

[modify] https://crrev.com/88da1e1c25b97c0e40e5fe9dbe60e00c9d66b0f5/third_party/blink/renderer/core/frame/web_frame_widget_impl.cc


### mu...@chromium.org (2022-11-23)

rzintct@gmail.com: Hopefully the bug is fixed for you now.  If the bug reproduces for you on a Debug build on ToT now, please let us know and we will reopen the bug.

### [Deleted User] (2022-11-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-23)

[Empty comment from Monorail migration]

### am...@google.com (2022-12-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-02)

Congratulations, Sri! The VRP Panel has decided to award you $1,500 for this moderately mitigated security bug. Thank you for your efforts and reporting this issue to us! 

### rz...@gmail.com (2022-12-02)

Thank you :)

### am...@google.com (2022-12-05)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-02-03)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-07)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1316301?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1367848]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059378)*
