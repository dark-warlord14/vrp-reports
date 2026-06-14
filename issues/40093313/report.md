# heap-use-after-free on RTCPeerConnectionHandler

| Field | Value |
|-------|-------|
| **Issue ID** | [40093313](https://issues.chromium.org/issues/40093313) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC>PeerConnection |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cd...@gmail.com |
| **Assignee** | gu...@chromium.org |
| **Created** | 2018-12-05 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36

Steps to reproduce the problem:
1. Install Node.js include npm and express(cuz there is a node webserver)
2. Make a dirctory named "www" in the same dir with sw.js and put crash.html and other three js resource files(testharness.js testharnessreport.js RTCPeerConnection-helper.js) into the "www" dir.
3. Run node ws.js and,if every thing setting up correctly,nothing will echo from console.
4.Download latest chromium asan build. asan-linux-release-613801 tested to be fine.
5.Run ./chrome http://127.0.0.1:8605/crash.html

What is the expected behavior?

What went wrong?
Can get UAF stably.
The log sees in asan.log.

Did this work before? N/A 

Chrome version: 73.0.3631.0  Channel: stable
OS Version: 16.04
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### mm...@chromium.org (2018-12-05)

I've managed to reproduce the issue locally with asan-linux-release-613801 as well as asan-linux-release-599034 (which is the Stable branch).

orphis@, could you please take a look?

[Monorail components: Blink>WebRTC>PeerConnection]

### ca...@chromium.org (2018-12-17)

Friendly security sheriff ping, this is a high severity vulnerability affecting stable, are there any updates?

### sh...@chromium.org (2018-12-19)

orphis: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-01-02)

orphis: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rs...@chromium.org (2019-01-14)

Friendly ping from the security sheriff - this is a high-severity issue that hasn't been updated in more than a month.

### hb...@chromium.org (2019-01-14)

[Empty comment from Monorail migration]

### hb...@chromium.org (2019-01-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2019-01-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3514a77e7fa2e5b8bfe5d98af22964bbd69d680f

commit 3514a77e7fa2e5b8bfe5d98af22964bbd69d680f
Author: Guido Urdaneta <guidou@chromium.org>
Date: Wed Jan 16 00:47:25 2019

Check weak pointers in RTCPeerConnectionHandler::WebRtcSetDescriptionObserverImpl

Bug: 912074
Change-Id: I8ba86751f5d5bf12db51520f985ef0d3dae63ed8
Reviewed-on: https://chromium-review.googlesource.com/c/1411916
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Reviewed-by: Henrik Boström <hbos@chromium.org>
Cr-Commit-Position: refs/heads/master@{#622945}
[modify] https://crrev.com/3514a77e7fa2e5b8bfe5d98af22964bbd69d680f/content/renderer/media/webrtc/rtc_peer_connection_handler.cc


### gu...@chromium.org (2019-01-16)

[Empty comment from Monorail migration]

### gu...@chromium.org (2019-01-16)

Requesting merge to 72 after Canary verification.

### sh...@chromium.org (2019-01-16)

This bug requires manual review: We are only 12 days from stable.
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), djmm@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-01-16)

+awhalley@ for M72 merge review, change is not in canary yet.

### sh...@chromium.org (2019-01-16)

[Empty comment from Monorail migration]

### gu...@chromium.org (2019-01-18)

Change is now in canary and working well.

### ab...@google.com (2019-01-18)

[Empty comment from Monorail migration]

### go...@chromium.org (2019-01-18)

Pls merge your change to M72 branch 3626 by 1:00 PM PT Monday, 01/21 so we can pick it up for next week beta. Thank you.

### cr...@appspot.gserviceaccount.com (2019-01-19)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/b39e2d471a671e7834fcdd227cc6ffffbcca86a4

Commit: b39e2d471a671e7834fcdd227cc6ffffbcca86a4
Author: guidou@chromium.org
Commiter: guidou@chromium.org
Date: 2019-01-19 06:21:32 +0000 UTC

Check weak pointers in RTCPeerConnectionHandler::WebRtcSetDescriptionObserverImpl

Bug: 912074
Change-Id: I8ba86751f5d5bf12db51520f985ef0d3dae63ed8
Reviewed-on: https://chromium-review.googlesource.com/c/1411916
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Reviewed-by: Henrik Boström <hbos@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#622945}(cherry picked from commit 3514a77e7fa2e5b8bfe5d98af22964bbd69d680f)
Reviewed-on: https://chromium-review.googlesource.com/c/1412028
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/branch-heads/3626@{#741}
Cr-Branched-From: d897fb137fbaaa9355c0c93124cc048824eb1e65-refs/heads/master@{#612437}

### bu...@chromium.org (2019-01-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b39e2d471a671e7834fcdd227cc6ffffbcca86a4

commit b39e2d471a671e7834fcdd227cc6ffffbcca86a4
Author: Guido Urdaneta <guidou@chromium.org>
Date: Sat Jan 19 06:21:32 2019

Check weak pointers in RTCPeerConnectionHandler::WebRtcSetDescriptionObserverImpl

Bug: 912074
Change-Id: I8ba86751f5d5bf12db51520f985ef0d3dae63ed8
Reviewed-on: https://chromium-review.googlesource.com/c/1411916
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Reviewed-by: Henrik Boström <hbos@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#622945}(cherry picked from commit 3514a77e7fa2e5b8bfe5d98af22964bbd69d680f)
Reviewed-on: https://chromium-review.googlesource.com/c/1412028
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/branch-heads/3626@{#741}
Cr-Branched-From: d897fb137fbaaa9355c0c93124cc048824eb1e65-refs/heads/master@{#612437}
[modify] https://crrev.com/b39e2d471a671e7834fcdd227cc6ffffbcca86a4/content/renderer/media/webrtc/rtc_peer_connection_handler.cc


### na...@google.com (2019-01-22)

[Empty comment from Monorail migration]

### na...@google.com (2019-01-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-01-24)

Congrats! The Panel has decided to reward $3,000 for this report. 

### na...@google.com (2019-01-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-02-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-04-24)

This issue was migrated from crbug.com/chromium/912074?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093313)*
