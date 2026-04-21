# [webrtc]UAF in RTCPeerConnectionHandler::OnIceCandidate

| Field | Value |
|-------|-------|
| **Issue ID** | [41487330](https://issues.chromium.org/issues/41487330) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC, Blink>WebRTC>PeerConnection |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | gu...@chromium.org |
| **Created** | 2023-12-29 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**  

tested os version:  

ubuntu 22.04  

tested chrome version:  

Chromium 122.0.6182.0  

Chromium 122.0.6208.0

repro steps:  

1 git apply force-gc.patch  

2 ./chrome --user-data-dr=/tmp/xx <http://localhost:8000/crash.html>

**Problem Description:**  

analyze:  

This issue is similar to the issue (<https://bugs.chromium.org/p/chromium/issues/detail?id=1405256>) that I submitted almost a year ago (Jan 6, 2023).

Let’s first take a look at the fix[a] of the previous issue (this part of the code was changed during the period, so the latest code is listed here, which is a little different from the cl at that time):

```
void RTCPeerConnectionHandler::OnIceCandidate(const String& sdp,  
                                              const String& sdp_mid,  
                                              int sdp_mline_index,  
                                              int component,  
                                              int address_family) {  
  // In order to ensure that the RTCPeerConnection is not garbage collected  
  // from under the function, we keep a pointer to it on the stack.  
  auto\* client_on_stack = client_.Get();                                         --->[0] Get nullptr        
  DCHECK(task_runner_->RunsTasksInCurrentSequence());  
  TRACE_EVENT0("webrtc", "RTCPeerConnectionHandler::OnIceCandidateImpl");  
  // This line can cause garbage collection.  
  auto\* platform_candidate = MakeGarbageCollected<RTCIceCandidatePlatform>(      --->[1] Trigger gc to free this  
      sdp, sdp_mid, sdp_mline_index);     
  if (peer_connection_tracker_) {                                                --->[2] Trigger UAF                      
    peer_connection_tracker_->TrackAddIceCandidate(  
        this, platform_candidate, PeerConnectionTracker::kSourceLocal, true);  
  }  
  
  if (!is_closed_ && client_on_stack) {  
    client_on_stack->DidGenerateICECandidate(platform_candidate);  
  }  
}  
[a]https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc;l=2056  

```

In the above code snippet, client\_(RTCPeerConnection) is stored in the stack to avoid garbage collection. But there are edge scenarios here. For example, client\_ has been set to nullptr, but has not been triggered by garbage collection. At this time, client\_on\_stack is also nullptr. Therefore, it is still possible to trigger garbage collection after [1] is called, calling RTCPeerConnection::Dispose[b] to release RTCPeerConnectionHandler, and eventually cause UAF.

[b]<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc;l=672>

However, the repro is unstable. When testing locally, the original chrome (not patched) ran for several hours to repro once. In order to facilitate repro and testing, I modified the source code. Below [0], if client\_on\_stack is nullptr,trigger forces garbage collection. Once garbage collection is triggered, uaf will be reproduced immediately. Please see the patch code for detailed instructions and debug message.  

The POC used here is also copied from 1405256 without any changes. I could'nt confirm whether this issue is caused by changes in the internal garbage collection mechanism or whether it is caused by incomplete cl before.

**Additional Comments:**

\*\*Chrome version: \*\* 122.0.6182.0 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [force-gc.patch](attachments/force-gc.patch) (text/plain, 3.1 KB)
- [crash.html](attachments/crash.html) (text/plain, 1.3 KB)
- [asan.log](attachments/asan.log) (text/plain, 33.9 KB)

## Timeline

### [Deleted User] (2023-12-29)

[Empty comment from Monorail migration]

### em...@gmail.com (2023-12-31)

I used the same method(patch force-gc.patch) in the old release version of Chromium 110.0.5481.77 (after fixing the issue: 1405256), and it can still be reproduced.
It can be confirmed that this bug has existed for more than a year and was not completely fixed at that time.
Because the UAF can only be reproduced when client_ is nullpt and has not been garbage collected, it increases the difficulty of repro.

### am...@chromium.org (2024-01-02)

Thanks for the good report, Cassidy Kim. Due to the difficulty to repro here, I'm going to just go ahead and get this issue over to the correct team. 
Sev-High -- renderer memory corruption
FoundIn-120 -- current extended Stable though the bug has been around longer 


[Monorail components: Blink>WebRTC Blink>WebRTC>PeerConnection]

### am...@chromium.org (2024-01-02)

+mlippautz for potential input on GC side of things here 

### [Deleted User] (2024-01-02)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-03)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-12)

hta: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ja...@chromium.org (2024-01-16)

Hi hta, can you take a look and provide an update? I've also drafted an email and scheduled it to send to you later today with a similar request.

Thanks!

### gu...@chromium.org (2024-01-17)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2024-01-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8755f76bec326c654370de6dd68eea693df74ede

commit 8755f76bec326c654370de6dd68eea693df74ede
Author: Guido Urdaneta <guidou@chromium.org>
Date: Thu Jan 18 16:47:18 2024

[RTCPeerConnection] Exit early from RTCPeerConnectionHandler

For certain operations that require a live client
(i.e., RTCPeerConnection, which is garbage collected),
PeerConnectionHandler keeps a pointer to the client on the stack
to prevent garbage collection.

In some cases, the client may have already been garbage collected
(the client is null). In that case, there is no point in doing the
operation and it should exit early to avoid UAF/crashes.

This CL adds early exit to the cases that do not already have it.

Bug: 1514777
Change-Id: I27e9541cfaa74d978799c03e2832a0980f9e5710
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5210359
Reviewed-by: Tomas Gunnarsson <tommi@chromium.org>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1248826}

[modify] https://crrev.com/8755f76bec326c654370de6dd68eea693df74ede/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler_test.cc
[modify] https://crrev.com/8755f76bec326c654370de6dd68eea693df74ede/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc


### gu...@chromium.org (2024-01-19)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-19)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-19)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-19)

Requesting merge to extended stable M120 because latest trunk commit (1248826) appears to be after extended stable branch point (1217362).

Requesting merge to stable M121 because latest trunk commit (1248826) appears to be after stable branch point (1233107).

Merge review required: M120 is already shipping to stable.

Merge review required: M121 has already been cut for stable release.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [120, 121].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-20)

Requesting merge to extended stable M120 because latest trunk commit (1248826) appears to be after extended stable branch point (1217362).

Requesting merge to stable M121 because latest trunk commit (1248826) appears to be after stable branch point (1233107).

Merge review required: M120 is already shipping to stable.

Merge review required: M121 has already been cut for stable release.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [120, 121].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gu...@chromium.org (2024-01-21)

1. Which CLs should be backmerged? (Please include Gerrit links.)
https://crrev.com/c/5210359

2. Has this fix been verified on Canary to not pose any stability regressions?
Yes

3. Does this fix pose any potential non-verifiable stability risks?
No

4. Does this fix pose any known compatibility risks?
No

5. Does it require manual verification by the test team? If so, please describe required testing.
No


### [Deleted User] (2024-01-21)

Requesting merge to extended stable M120 because latest trunk commit (1248826) appears to be after extended stable branch point (1217362).

Requesting merge to stable M121 because latest trunk commit (1248826) appears to be after stable branch point (1233107).

Merge review required: M120 is already shipping to stable.

Merge review required: M121 has already been cut for stable release.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [120, 121].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-22)

Requesting merge to extended stable M120 because latest trunk commit (1248826) appears to be after extended stable branch point (1217362).

Requesting merge to stable M121 because latest trunk commit (1248826) appears to be after stable branch point (1233107).

Merge review required: M120 is already shipping to stable.

Merge review required: M121 has already been cut for stable release.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [120, 121].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2024-01-23)

M121 and M120 merges approved for https://crrev.com/c/5210359 
please merge this fix to M121 Stable (branch 6167) and M120 Extended (branch 6099) by EOD Thursday 25 January so this fix can be included in the next Stable and Extended Stable security updates. 

### gi...@appspot.gserviceaccount.com (2024-01-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/99594f835966499aa58005b0f11594caa92447c8

commit 99594f835966499aa58005b0f11594caa92447c8
Author: Guido Urdaneta <guidou@chromium.org>
Date: Wed Jan 24 18:23:23 2024

[RTCPeerConnection] Exit early from RTCPeerConnectionHandler

For certain operations that require a live client
(i.e., RTCPeerConnection, which is garbage collected),
PeerConnectionHandler keeps a pointer to the client on the stack
to prevent garbage collection.

In some cases, the client may have already been garbage collected
(the client is null). In that case, there is no point in doing the
operation and it should exit early to avoid UAF/crashes.

This CL adds early exit to the cases that do not already have it.

(cherry picked from commit 8755f76bec326c654370de6dd68eea693df74ede)

Bug: 1514777
Change-Id: I27e9541cfaa74d978799c03e2832a0980f9e5710
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5210359
Reviewed-by: Tomas Gunnarsson <tommi@chromium.org>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1248826}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5231507
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/branch-heads/6167@{#1631}
Cr-Branched-From: 222e786949e76e342d325ea0d008b4b6273f3a89-refs/heads/main@{#1233107}

[modify] https://crrev.com/99594f835966499aa58005b0f11594caa92447c8/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler_test.cc
[modify] https://crrev.com/99594f835966499aa58005b0f11594caa92447c8/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc


### [Deleted User] (2024-01-24)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2024-01-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ee0b8769f428a72f90c880f4c28f4069d0574344

commit ee0b8769f428a72f90c880f4c28f4069d0574344
Author: Guido Urdaneta <guidou@chromium.org>
Date: Wed Jan 24 18:40:01 2024

[RTCPeerConnection] Exit early from RTCPeerConnectionHandler

For certain operations that require a live client
(i.e., RTCPeerConnection, which is garbage collected),
PeerConnectionHandler keeps a pointer to the client on the stack
to prevent garbage collection.

In some cases, the client may have already been garbage collected
(the client is null). In that case, there is no point in doing the
operation and it should exit early to avoid UAF/crashes.

This CL adds early exit to the cases that do not already have it.

(cherry picked from commit 8755f76bec326c654370de6dd68eea693df74ede)

Bug: 1514777
Change-Id: I27e9541cfaa74d978799c03e2832a0980f9e5710
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5210359
Reviewed-by: Tomas Gunnarsson <tommi@chromium.org>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1248826}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5233883
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/6099@{#1867}
Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

[modify] https://crrev.com/ee0b8769f428a72f90c880f4c28f4069d0574344/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler_test.cc
[modify] https://crrev.com/ee0b8769f428a72f90c880f4c28f4069d0574344/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc


### am...@google.com (2024-01-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-01-25)

Congratulations Cassidy Kim! The Chrome VRP Panel has decided to award you $3,000 for this report of a moderately mitigated security bug. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2024-01-27)

[Empty comment from Monorail migration]

### pg...@google.com (2024-01-30)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-30)

This issue was migrated from crbug.com/chromium/1514777?no_tracker_redirect=1

[Multiple monorail components: Blink>WebRTC, Blink>WebRTC>PeerConnection]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-06)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



### pe...@google.com (2024-02-20)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



### vo...@google.com (2024-02-20)

1. Two CLs: <https://crrev.com/c/5273751> and <https://crrev.com/c/5308573>, the second CL is required to avoid conflicts and test failures
2. Low - no conflicts after including a precursor CL
3. 120, 121
4. Yes

### na...@google.com (2024-02-27)

Approving merge for LTS-114

### ap...@google.com (2024-02-28)

Project: chromium/src
Branch: refs/branch-heads/5735

commit fdf34e4c62585df43ebf0de858b3d6d1312629ba
Author: Guido Urdaneta <guidou@chromium.org>
Date:   Wed Feb 28 16:52:02 2024

    [M114-LTS][RTCPeerConnection] Exit early from RTCPeerConnectionHandler
    
    For certain operations that require a live client
    (i.e., RTCPeerConnection, which is garbage collected),
    PeerConnectionHandler keeps a pointer to the client on the stack
    to prevent garbage collection.
    
    In some cases, the client may have already been garbage collected
    (the client is null). In that case, there is no point in doing the
    operation and it should exit early to avoid UAF/crashes.
    
    This CL adds early exit to the cases that do not already have it.
    
    (cherry picked from commit 8755f76bec326c654370de6dd68eea693df74ede)
    
    (cherry picked from commit ee0b8769f428a72f90c880f4c28f4069d0574344)
    
    Bug: 1514777
    Change-Id: I27e9541cfaa74d978799c03e2832a0980f9e5710
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5210359
    Commit-Queue: Guido Urdaneta <guidou@chromium.org>
    Cr-Original-Original-Commit-Position: refs/heads/main@{#1248826}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5233883
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Auto-Submit: Guido Urdaneta <guidou@chromium.org>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Original-Commit-Position: refs/branch-heads/6099@{#1867}
    Cr-Original-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5273751
    Reviewed-by: Guido Urdaneta <guidou@chromium.org>
    Commit-Queue: Zakhar Voit <voit@google.com>
    Owners-Override: Mohamed Omar <mohamedaomar@google.com>
    Cr-Commit-Position: refs/branch-heads/5735@{#1704}
    Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

M       third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc
M       third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler_test.cc

https://chromium-review.googlesource.com/5273751


### ap...@google.com (2024-03-27)

Project: chromium/src
Branch: refs/branch-heads/6099_225

commit fb0a07d7f657f476825d6993aee5bcbae64c3017
Author: Guido Urdaneta <guidou@chromium.org>
Date:   Wed Mar 27 03:01:39 2024

    [CfM-R120] [RTCPeerConnection] Exit early from RTCPeerConnectionHandler
    
    For certain operations that require a live client
    (i.e., RTCPeerConnection, which is garbage collected),
    PeerConnectionHandler keeps a pointer to the client on the stack
    to prevent garbage collection.
    
    In some cases, the client may have already been garbage collected
    (the client is null). In that case, there is no point in doing the
    operation and it should exit early to avoid UAF/crashes.
    
    This CL adds early exit to the cases that do not already have it.
    
    Bug: 1514777
    Change-Id: I27e9541cfaa74d978799c03e2832a0980f9e5710
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5210359
    Reviewed-by: Tomas Gunnarsson <tommi@chromium.org>
    Commit-Queue: Guido Urdaneta <guidou@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1248826}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5284756
    Reviewed-by: Steve Anton <steveanton@chromium.org>
    Auto-Submit: Richard Yeh <rcy@google.com>
    Commit-Queue: Steve Anton <steveanton@chromium.org>
    Reviewed-by: Guido Urdaneta <guidou@chromium.org>
    Owners-Override: Richard Yeh <rcy@google.com>
    Cr-Commit-Position: refs/branch-heads/6099_225@{#16}
    Cr-Branched-From: 6d3cc0dac5057925e096b1329680124b19f35842-refs/branch-heads/6099@{#1762}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

M       third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc
M       third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler_test.cc

https://chromium-review.googlesource.com/5284756


### pe...@google.com (2024-04-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41487330)*
