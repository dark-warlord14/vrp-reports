# Security: Universal XSS using OOPIF

| Field | Value |
|-------|-------|
| **Issue ID** | [40085388](https://issues.chromium.org/issues/40085388) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Sandbox>SiteIsolation |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | se...@gmail.com |
| **Assignee** | dc...@chromium.org |
| **Created** | 2016-09-13 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

This bug is related to <https://crbug.com/chromium/628942> (even the repro cases are similar).

When an <iframe> element is about to be removed from the document tree, |ChildFrameDisconnector| calls |Frame::detach()|,  

which may fire the "unload" event. |SubframeLoadingDisabler| prevents the event handler from attaching another frame to  

the element while |ChildFrameDisconnector| is alive. However, it's possible to perform the local-to-remote frame swap.  

It's also important that |ScopedPageLoadDeferrer| doesn't defer cross-process navigations. As a result, the <iframe> element  

is left in an inconsistent state.

**VERSION**  

Google Chrome 53.0.2785.101 (64-bit)  

Google Chrome 55.0.2853.0 dev (64-bit)  

Google Chrome 55.0.2859.0 canary (64-bit)

**REPRODUCTION CASE**  

The --isolate-extensions flag is required on stable.

## Attachments

- [uxss.html](attachments/uxss.html) (text/plain, 2.0 KB)

## Timeline

### el...@chromium.org (2016-09-13)

[Empty comment from Monorail migration]

[Monorail components: Internals>Sandbox>SiteIsolation]

### na...@chromium.org (2016-09-13)

[Empty comment from Monorail migration]

### pe...@chromium.org (2016-09-13)

Feel free to adjust the labels Daniel.

### pe...@chromium.org (2016-09-13)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-09-14)

Some notes for future me:

1) Is print() the only remaining way to enter a nested message loop in unload? If so, we should consider blocking it and merging that to stable. Nested message loops + the extension runAsync primitive has led to nothing but trouble.

2) Even without the UXSS, you can crash the renderer by calling print() in unload, see https://crbug.com/chromium/646671

3) The trigger for swapping out should come via an IPC. Why is this IPC being dispatched inside print()'s nested message loop?

4) (I think) we can also block this by having swap() return if the frame is in the middle of detach. Unfortunately, the correct logic for doing so isn't so clear. Need to figure out if this UXSS can only happen on a local -> remote transition; if so, maybe SubframeLoadingDisabler::canLoadFrame(document()) is good enough. Otherwise, we'll need to figure something else out.

### sh...@chromium.org (2016-09-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-28)

dcheng: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2016-09-28)

[Empty comment from Monorail migration]

### cr...@chromium.org (2016-09-28)

Daniel mentioned that we're waiting on a fix from rdevlin.cronin@ here (presumably for runAsync?).

### dc...@chromium.org (2016-09-28)

To be more exact, I'm not blocked on devlin, it's in review, and it's probably blocked on me more than anything else. =(

### sh...@chromium.org (2016-10-13)

dcheng: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dc...@chromium.org (2016-10-18)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-10-19)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-10-19)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-10-19)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-10-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/29226a0dcd5ff17b04a0a92bb52ea5c88b29decb

commit 29226a0dcd5ff17b04a0a92bb52ea5c88b29decb
Author: dcheng <dcheng@chromium.org>
Date: Wed Oct 19 18:16:46 2016

Disallow frame swap during frame detach.

Otherwise, the swapped-in frame is never detached, resulting in general
confusion and mayhem.

BUG=646610

Review-Url: https://chromiumcodereview.appspot.com/2429133002
Cr-Commit-Position: refs/heads/master@{#426245}

[modify] https://crrev.com/29226a0dcd5ff17b04a0a92bb52ea5c88b29decb/content/renderer/render_frame_impl.cc
[modify] https://crrev.com/29226a0dcd5ff17b04a0a92bb52ea5c88b29decb/third_party/WebKit/Source/core/frame/Frame.h
[modify] https://crrev.com/29226a0dcd5ff17b04a0a92bb52ea5c88b29decb/third_party/WebKit/Source/core/frame/LocalFrame.cpp
[modify] https://crrev.com/29226a0dcd5ff17b04a0a92bb52ea5c88b29decb/third_party/WebKit/Source/core/frame/LocalFrame.h
[modify] https://crrev.com/29226a0dcd5ff17b04a0a92bb52ea5c88b29decb/third_party/WebKit/Source/core/frame/RemoteFrame.cpp
[modify] https://crrev.com/29226a0dcd5ff17b04a0a92bb52ea5c88b29decb/third_party/WebKit/Source/web/WebFrame.cpp
[modify] https://crrev.com/29226a0dcd5ff17b04a0a92bb52ea5c88b29decb/third_party/WebKit/Source/web/WebLocalFrameImpl.cpp


### dc...@chromium.org (2016-10-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-20)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-10-21)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-24)

[Empty comment from Monorail migration]

### di...@google.com (2016-10-24)

[Automated comment] There appears to be on-going work (i.e. bugroid changes), needs manual review.

### aw...@chromium.org (2016-10-24)

This is good for M55 assuming that the relevant feature is enabled for a high percentage of dev users. Somebody mind confirming?

### aw...@chromium.org (2016-10-24)

It's at 90% per creis@ - sounds good.

### go...@chromium.org (2016-10-24)

Approving merge to M55 branch 2883 based on https://crbug.com/chromium/646610#c23. Please merge ASAP. Thank you.

### bu...@chromium.org (2016-10-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1f9024c0866fa32cab4b8ca39010564e23f30d9d

commit 1f9024c0866fa32cab4b8ca39010564e23f30d9d
Author: Daniel Cheng <dcheng@chromium.org>
Date: Mon Oct 24 20:37:44 2016

Disallow frame swap during frame detach.

Otherwise, the swapped-in frame is never detached, resulting in general
confusion and mayhem.

BUG=646610

Review-Url: https://codereview.chromium.org/2429133002
Cr-Commit-Position: refs/heads/master@{#426245}
(cherry picked from commit 29226a0dcd5ff17b04a0a92bb52ea5c88b29decb)

R=japhet@chromium.org

Review URL: https://codereview.chromium.org/2446563003 .

Cr-Commit-Position: refs/branch-heads/2883@{#257}
Cr-Branched-From: 614d31daee2f61b0180df403a8ad43f20b9f6dd7-refs/heads/master@{#423768}

[modify] https://crrev.com/1f9024c0866fa32cab4b8ca39010564e23f30d9d/content/renderer/render_frame_impl.cc
[modify] https://crrev.com/1f9024c0866fa32cab4b8ca39010564e23f30d9d/third_party/WebKit/Source/core/frame/Frame.h
[modify] https://crrev.com/1f9024c0866fa32cab4b8ca39010564e23f30d9d/third_party/WebKit/Source/core/frame/LocalFrame.cpp
[modify] https://crrev.com/1f9024c0866fa32cab4b8ca39010564e23f30d9d/third_party/WebKit/Source/core/frame/RemoteFrame.cpp
[modify] https://crrev.com/1f9024c0866fa32cab4b8ca39010564e23f30d9d/third_party/WebKit/Source/web/WebFrame.cpp


### aw...@chromium.org (2016-10-27)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-10-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1f9024c0866fa32cab4b8ca39010564e23f30d9d

commit 1f9024c0866fa32cab4b8ca39010564e23f30d9d
Author: Daniel Cheng <dcheng@chromium.org>
Date: Mon Oct 24 20:37:44 2016

Disallow frame swap during frame detach.

Otherwise, the swapped-in frame is never detached, resulting in general
confusion and mayhem.

BUG=646610

Review-Url: https://codereview.chromium.org/2429133002
Cr-Commit-Position: refs/heads/master@{#426245}
(cherry picked from commit 29226a0dcd5ff17b04a0a92bb52ea5c88b29decb)

R=japhet@chromium.org

Review URL: https://codereview.chromium.org/2446563003 .

Cr-Commit-Position: refs/branch-heads/2883@{#257}
Cr-Branched-From: 614d31daee2f61b0180df403a8ad43f20b9f6dd7-refs/heads/master@{#423768}

[modify] https://crrev.com/1f9024c0866fa32cab4b8ca39010564e23f30d9d/content/renderer/render_frame_impl.cc
[modify] https://crrev.com/1f9024c0866fa32cab4b8ca39010564e23f30d9d/third_party/WebKit/Source/core/frame/Frame.h
[modify] https://crrev.com/1f9024c0866fa32cab4b8ca39010564e23f30d9d/third_party/WebKit/Source/core/frame/LocalFrame.cpp
[modify] https://crrev.com/1f9024c0866fa32cab4b8ca39010564e23f30d9d/third_party/WebKit/Source/core/frame/RemoteFrame.cpp
[modify] https://crrev.com/1f9024c0866fa32cab4b8ca39010564e23f30d9d/third_party/WebKit/Source/web/WebFrame.cpp


### aw...@chromium.org (2016-10-27)

$7,500 from the panel - nice bug!

### aw...@chromium.org (2016-10-28)

[Empty comment from Monorail migration]

### di...@google.com (2016-11-04)

[Automated comment] removing mislabelled merge-merged-2840

### aw...@chromium.org (2016-11-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-29)

[Empty comment from Monorail migration]

### mm...@chromium.org (2016-12-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2019-02-16)

[Empty comment from Monorail migration]

### is...@google.com (2019-02-16)

This issue was migrated from crbug.com/chromium/646610?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085388)*
