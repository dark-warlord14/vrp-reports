# Security: Use after free in WebRTC

| Field | Value |
|-------|-------|
| **Issue ID** | [40051946](https://issues.chromium.org/issues/40051946) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC>PeerConnection |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | zh...@gmail.com |
| **Assignee** | ht...@chromium.org |
| **Created** | 2020-04-06 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

UAF in WebRTC.  

<https://cs.chromium.org/chromium/src/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc?g=0&l=724>  

handler\_->OnSignalingChange(signaling\_state);

<https://cs.chromium.org/chromium/src/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc?g=0&l=2192>

void RTCPeerConnectionHandler::OnSignalingChange(  

webrtc::PeerConnectionInterface::SignalingState new\_state) {  

DCHECK(task\_runner\_->RunsTasksInCurrentSequence());  

TRACE\_EVENT0("webrtc", "RTCPeerConnectionHandler::OnSignalingChange");

if (previous\_signaling\_state\_ ==  

webrtc::PeerConnectionInterface::kHaveLocalOffer &&  

new\_state == webrtc::PeerConnectionInterface::kHaveRemoteOffer) {  

// Inject missing kStable in case of implicit rollback.  

auto stable\_state = webrtc::PeerConnectionInterface::kStable;  

if (peer\_connection\_tracker\_)  

peer\_connection\_tracker\_->TrackSignalingStateChange(this, stable\_state);  

if (!is\_closed\_)  

client\_->DidChangeSignalingState(stable\_state);//will call js callback  

}  

previous\_signaling\_state\_ = new\_state;//uaf occurs  

if (peer\_connection\_tracker\_)  

peer\_connection\_tracker\_->TrackSignalingStateChange(this, new\_state);  

if (!is\_closed\_)  

client\_->DidChangeSignalingState(new\_state);  

}

In function RTCPeerConnectionHandler::OnSignalingChange, DidChangeSignalingState will dispatch event and call a js callback, remove the frame in the callback will free the handler\_ and cause uaf.

**VERSION**  

Chrome Version: Version 80.0.3987.163 (Official Build) (64-bit), stable  

Operating System: win10 x64  

**REPRODUCTION CASE**  

open index.html

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

## Attachments

- [index.html](attachments/index.html) (text/plain, 383 B)
- [i.html](attachments/i.html) (text/plain, 582 B)
- [windbg.txt](attachments/windbg.txt) (text/plain, 9.8 KB)

## Timeline

### zh...@gmail.com (2020-04-06)

[Empty comment from Monorail migration]

### zh...@gmail.com (2020-04-06)

Reporter credit: [Anonymous]

### li...@chromium.org (2020-04-06)

Tentatively assigning labels. hbos@, would you be able to help take a look? Thanks!

[Monorail components: Blink>WebRTC]

### hb...@chromium.org (2020-04-07)

This is another example of forcing GC of the object in a callback while code is still running on the object. Similar issue https://crbug.com/1005251 was fixed with https://chromium-review.googlesource.com/c/chromium/src/+/1832277. We should do something similar here to ensure we don't reference any of the objects after the callback.

In the case of onsignalingstatechanged though there is the requirement of "callback" that we may invoke onsignalingstatechanged twice... For that to be safe against GC in the middle, I suppose we have to fire event followed by PostTask with a weak reference or something, ensuring the second one only happens if GC didn't happen? Or add some reference counted object holding a boolean that we set at destruction, then we can check it for if destruction happened without using the "this" pointer...

But as I am not on the WebRTC Chrome team anymore, Harald can you take a look?

[Monorail components: -Blink>WebRTC Blink>WebRTC>PeerConnection]

### hb...@chromium.org (2020-04-07)

The requirement of "rollback" is what it meant to say there. When we go from kHaveLocalOffer to kHaveRemoteOffer we have to fire kStable in-between have-local and have-remote to ensure the signaling state transition graph is not violated. 

### ht...@chromium.org (2020-04-15)

OP: Thanks for the great repro!
I think I have found a solution that seems to prevent the root cause of this problem. CL coming.


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/919dd0c1244afdb269d023dd178bec8caec372ab

commit 919dd0c1244afdb269d023dd178bec8caec372ab
Author: Harald Alvestrand <hta@chromium.org>
Date: Wed Apr 15 14:03:03 2020

Onstate handler is allowed to close a PeerConnection.

Bug: chromium:1068084
Change-Id: Icd3f70b6784ac22ef4e3bc1c99233f51145a917f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2146542
Commit-Queue: Harald Alvestrand <hta@chromium.org>
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/heads/master@{#759242}

[modify] https://crrev.com/919dd0c1244afdb269d023dd178bec8caec372ab/third_party/blink/renderer/modules/peerconnection/mock_rtc_peer_connection_handler_client.h
[modify] https://crrev.com/919dd0c1244afdb269d023dd178bec8caec372ab/third_party/blink/renderer/modules/peerconnection/mock_rtc_peer_connection_handler_platform.cc
[modify] https://crrev.com/919dd0c1244afdb269d023dd178bec8caec372ab/third_party/blink/renderer/modules/peerconnection/mock_rtc_peer_connection_handler_platform.h
[modify] https://crrev.com/919dd0c1244afdb269d023dd178bec8caec372ab/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc
[modify] https://crrev.com/919dd0c1244afdb269d023dd178bec8caec372ab/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.h
[modify] https://crrev.com/919dd0c1244afdb269d023dd178bec8caec372ab/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc
[modify] https://crrev.com/919dd0c1244afdb269d023dd178bec8caec372ab/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.h
[modify] https://crrev.com/919dd0c1244afdb269d023dd178bec8caec372ab/third_party/blink/renderer/platform/peerconnection/rtc_peer_connection_handler_client.h
[modify] https://crrev.com/919dd0c1244afdb269d023dd178bec8caec372ab/third_party/blink/renderer/platform/peerconnection/rtc_peer_connection_handler_platform.h
[add] https://crrev.com/919dd0c1244afdb269d023dd178bec8caec372ab/third_party/blink/web_tests/fast/peerconnection/resources/statechange-iframe-destroy-child.html
[add] https://crrev.com/919dd0c1244afdb269d023dd178bec8caec372ab/third_party/blink/web_tests/fast/peerconnection/statechange-iframe-destroy-parent.html


### ht...@chromium.org (2020-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-15)

This bug requires manual review: To minimize risk and increase branch stability, all merge requests are being reviewed manually by the release team.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2020-04-15)

pls help answer the questions in https://crbug.com/chromium/1068084#c9. 

+adetaylor@ to chime in for merge review( you can approve if u think it is good from security perspective)

### ad...@google.com (2020-04-15)

Approving merge to M83, branch 4103.

hta@ please mark this bug as fixed if the commit in https://crbug.com/chromium/1068084#c7 is the full fix. As this is a high severity security bug, Sheriffbot would normally also add Merge-Request-81. But I'm not entirely comfortable merging this to the current stable branch. My concern is that it's changing the semantics of client_ and it would be easy to introduce stability regressions. As such I am leaning towards not merging this back to M81, even though this is potentially exploitable by patch-gappers in the mean time. Any thoughts hta@? Can you convince me that the fix is 100% safe? :)

### [Deleted User] (2020-04-15)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-04-15)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2020-04-16)

The CL : https://chromium.googlesource.com/chromium/src/+/919dd0c1244afdb269d023dd178bec8caec372ab  has caused a huge renderer crash on latest Chrome Canary which is being tracked in issue#1071327.

I think we should wait until we have good canary coverage to fix this crash before merging to M83 and M81.

### go...@chromium.org (2020-04-16)

Agree with #14, no merge to M81 for next wee security respin per comment and revoking merge approval for M83 per https://crbug.com/chromium/1068084#c14. 

Sorry adetaylor@, we can't take this merge into M81 & M83 as it caused a huge renderer crash on latest Chrome Canary which is being tracked in issue#1071327.


### ad...@chromium.org (2020-04-17)

OK! Sorry about that. At least I didn't approve merge to M81 (because I was paranoid that *exactly this bug* might happen - gawd, C++ makes it so easy to shoot yourself in the foot.)

### go...@chromium.org (2020-04-17)

Yeah, no worries at all adetaylor@. Thank you.



### ht...@chromium.org (2020-04-17)

We now have a fix for the crasher - https://chromium-review.googlesource.com/c/chromium/src/+/2153325

Once that's been verified in canary, I'll re-request merge to M83 (on both the original fix and the fix-fix).


### sr...@google.com (2020-04-17)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-18)

[Empty comment from Monorail migration]

### ht...@chromium.org (2020-04-20)

This seems to have baked well over the weekend. Please re-process merge requests (with #1071327).


### ht...@chromium.org (2020-04-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-04-20)

Testcase 5704197585043456 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5704197585043456.

### sr...@google.com (2020-04-20)

Merge approved for M83 branch:4103 pls merge your changes asap to branch so we can include in this week's beta release

### na...@google.com (2020-04-20)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9a2bc8e9cf63e70d47a443c673ae00d2b03ffc4f

commit 9a2bc8e9cf63e70d47a443c673ae00d2b03ffc4f
Author: Harald Alvestrand <hta@chromium.org>
Date: Tue Apr 21 08:41:32 2020

Onstate handler is allowed to close a PeerConnection.

(cherry picked from commit 919dd0c1244afdb269d023dd178bec8caec372ab)

Bug: chromium:1068084
Change-Id: Icd3f70b6784ac22ef4e3bc1c99233f51145a917f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2146542
Commit-Queue: Harald Alvestrand <hta@chromium.org>
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#759242}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2156993
Reviewed-by: Harald Alvestrand <hta@chromium.org>
Cr-Commit-Position: refs/branch-heads/4103@{#250}
Cr-Branched-From: 8ad47e8d21f6866e4a37f47d83a860d41debf514-refs/heads/master@{#756066}

[modify] https://crrev.com/9a2bc8e9cf63e70d47a443c673ae00d2b03ffc4f/third_party/blink/renderer/modules/peerconnection/mock_rtc_peer_connection_handler_client.h
[modify] https://crrev.com/9a2bc8e9cf63e70d47a443c673ae00d2b03ffc4f/third_party/blink/renderer/modules/peerconnection/mock_rtc_peer_connection_handler_platform.cc
[modify] https://crrev.com/9a2bc8e9cf63e70d47a443c673ae00d2b03ffc4f/third_party/blink/renderer/modules/peerconnection/mock_rtc_peer_connection_handler_platform.h
[modify] https://crrev.com/9a2bc8e9cf63e70d47a443c673ae00d2b03ffc4f/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc
[modify] https://crrev.com/9a2bc8e9cf63e70d47a443c673ae00d2b03ffc4f/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.h
[modify] https://crrev.com/9a2bc8e9cf63e70d47a443c673ae00d2b03ffc4f/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc
[modify] https://crrev.com/9a2bc8e9cf63e70d47a443c673ae00d2b03ffc4f/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.h
[modify] https://crrev.com/9a2bc8e9cf63e70d47a443c673ae00d2b03ffc4f/third_party/blink/renderer/platform/peerconnection/rtc_peer_connection_handler_client.h
[modify] https://crrev.com/9a2bc8e9cf63e70d47a443c673ae00d2b03ffc4f/third_party/blink/renderer/platform/peerconnection/rtc_peer_connection_handler_platform.h
[add] https://crrev.com/9a2bc8e9cf63e70d47a443c673ae00d2b03ffc4f/third_party/blink/web_tests/fast/peerconnection/resources/statechange-iframe-destroy-child.html
[add] https://crrev.com/9a2bc8e9cf63e70d47a443c673ae00d2b03ffc4f/third_party/blink/web_tests/fast/peerconnection/statechange-iframe-destroy-parent.html


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/94b16e2f5a5e99aec0c62754c31de2d297becf2d

commit 94b16e2f5a5e99aec0c62754c31de2d297becf2d
Author: Carlos Knippschild <carlosk@chromium.org>
Date: Tue Apr 21 20:53:45 2020

Revert "Onstate handler is allowed to close a PeerConnection."

This reverts commit 9a2bc8e9cf63e70d47a443c673ae00d2b03ffc4f.

Reason for revert: https://crbug.com/1073213

Original change's description:
> Onstate handler is allowed to close a PeerConnection.
> 
> (cherry picked from commit 919dd0c1244afdb269d023dd178bec8caec372ab)
> 
> Bug: chromium:1068084
> Change-Id: Icd3f70b6784ac22ef4e3bc1c99233f51145a917f
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2146542
> Commit-Queue: Harald Alvestrand <hta@chromium.org>
> Reviewed-by: Guido Urdaneta <guidou@chromium.org>
> Cr-Original-Commit-Position: refs/heads/master@{#759242}
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2156993
> Reviewed-by: Harald Alvestrand <hta@chromium.org>
> Cr-Commit-Position: refs/branch-heads/4103@{#250}
> Cr-Branched-From: 8ad47e8d21f6866e4a37f47d83a860d41debf514-refs/heads/master@{#756066}

TBR=hta@chromium.org

Change-Id: If7400e9b7d02898bfadb31d31da2bf1a5df39801
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: chromium:1068084, chromium:1073213
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2159619
Reviewed-by: Carlos Knippschild <carlosk@chromium.org>
Commit-Queue: Carlos Knippschild <carlosk@chromium.org>
Cr-Commit-Position: refs/branch-heads/4103@{#262}
Cr-Branched-From: 8ad47e8d21f6866e4a37f47d83a860d41debf514-refs/heads/master@{#756066}

[modify] https://crrev.com/94b16e2f5a5e99aec0c62754c31de2d297becf2d/third_party/blink/renderer/modules/peerconnection/mock_rtc_peer_connection_handler_client.h
[modify] https://crrev.com/94b16e2f5a5e99aec0c62754c31de2d297becf2d/third_party/blink/renderer/modules/peerconnection/mock_rtc_peer_connection_handler_platform.cc
[modify] https://crrev.com/94b16e2f5a5e99aec0c62754c31de2d297becf2d/third_party/blink/renderer/modules/peerconnection/mock_rtc_peer_connection_handler_platform.h
[modify] https://crrev.com/94b16e2f5a5e99aec0c62754c31de2d297becf2d/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc
[modify] https://crrev.com/94b16e2f5a5e99aec0c62754c31de2d297becf2d/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.h
[modify] https://crrev.com/94b16e2f5a5e99aec0c62754c31de2d297becf2d/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc
[modify] https://crrev.com/94b16e2f5a5e99aec0c62754c31de2d297becf2d/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.h
[modify] https://crrev.com/94b16e2f5a5e99aec0c62754c31de2d297becf2d/third_party/blink/renderer/platform/peerconnection/rtc_peer_connection_handler_client.h
[modify] https://crrev.com/94b16e2f5a5e99aec0c62754c31de2d297becf2d/third_party/blink/renderer/platform/peerconnection/rtc_peer_connection_handler_platform.h
[delete] https://crrev.com/930a0ec8c7cf937a82345e36d99debfa48992b5e/third_party/blink/web_tests/fast/peerconnection/resources/statechange-iframe-destroy-child.html
[delete] https://crrev.com/930a0ec8c7cf937a82345e36d99debfa48992b5e/third_party/blink/web_tests/fast/peerconnection/statechange-iframe-destroy-parent.html


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a3345beb33439ab18fb8fbcad1d41ad40bb73290

commit a3345beb33439ab18fb8fbcad1d41ad40bb73290
Author: Harald Alvestrand <hta@chromium.org>
Date: Wed Apr 22 08:05:36 2020

Reland "Onstate handler is allowed to close a PeerConnection."

This reverts commit 94b16e2f5a5e99aec0c62754c31de2d297becf2d.

Reason for revert: Also landing fix from crbug.com/1071329
Original change's description:
> Revert "Onstate handler is allowed to close a PeerConnection."
> 
> This reverts commit 9a2bc8e9cf63e70d47a443c673ae00d2b03ffc4f.
> 
> Reason for revert: https://crbug.com/1073213
> 
> Original change's description:
> > Onstate handler is allowed to close a PeerConnection.
> > 
> > (cherry picked from commit 919dd0c1244afdb269d023dd178bec8caec372ab)
> > 
> > Bug: chromium:1068084
> > Change-Id: Icd3f70b6784ac22ef4e3bc1c99233f51145a917f
> > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2146542
> > Commit-Queue: Harald Alvestrand <hta@chromium.org>
> > Reviewed-by: Guido Urdaneta <guidou@chromium.org>
> > Cr-Original-Commit-Position: refs/heads/master@{#759242}
> > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2156993
> > Reviewed-by: Harald Alvestrand <hta@chromium.org>
> > Cr-Commit-Position: refs/branch-heads/4103@{#250}
> > Cr-Branched-From: 8ad47e8d21f6866e4a37f47d83a860d41debf514-refs/heads/master@{#756066}
> 
> TBR=hta@chromium.org
> 
> Change-Id: If7400e9b7d02898bfadb31d31da2bf1a5df39801
> No-Presubmit: true
> No-Tree-Checks: true
> No-Try: true
> Bug: chromium:1068084, chromium:1073213
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2159619
> Reviewed-by: Carlos Knippschild <carlosk@chromium.org>
> Commit-Queue: Carlos Knippschild <carlosk@chromium.org>
> Cr-Commit-Position: refs/branch-heads/4103@{#262}
> Cr-Branched-From: 8ad47e8d21f6866e4a37f47d83a860d41debf514-refs/heads/master@{#756066}

TBR=hta@chromium.org,carlosk@chromium.org

Change-Id: I7b6f58a11a83accc3cb14dcf3df637ea295a8d6e
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: chromium:1068084, chromium:1073213
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2159715
Reviewed-by: Harald Alvestrand <hta@chromium.org>
Commit-Queue: Harald Alvestrand <hta@chromium.org>
Cr-Commit-Position: refs/branch-heads/4103@{#271}
Cr-Branched-From: 8ad47e8d21f6866e4a37f47d83a860d41debf514-refs/heads/master@{#756066}

[modify] https://crrev.com/a3345beb33439ab18fb8fbcad1d41ad40bb73290/third_party/blink/renderer/modules/peerconnection/mock_rtc_peer_connection_handler_client.h
[modify] https://crrev.com/a3345beb33439ab18fb8fbcad1d41ad40bb73290/third_party/blink/renderer/modules/peerconnection/mock_rtc_peer_connection_handler_platform.cc
[modify] https://crrev.com/a3345beb33439ab18fb8fbcad1d41ad40bb73290/third_party/blink/renderer/modules/peerconnection/mock_rtc_peer_connection_handler_platform.h
[modify] https://crrev.com/a3345beb33439ab18fb8fbcad1d41ad40bb73290/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc
[modify] https://crrev.com/a3345beb33439ab18fb8fbcad1d41ad40bb73290/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.h
[modify] https://crrev.com/a3345beb33439ab18fb8fbcad1d41ad40bb73290/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc
[modify] https://crrev.com/a3345beb33439ab18fb8fbcad1d41ad40bb73290/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.h
[modify] https://crrev.com/a3345beb33439ab18fb8fbcad1d41ad40bb73290/third_party/blink/renderer/platform/peerconnection/rtc_peer_connection_handler_client.h
[modify] https://crrev.com/a3345beb33439ab18fb8fbcad1d41ad40bb73290/third_party/blink/renderer/platform/peerconnection/rtc_peer_connection_handler_platform.h
[add] https://crrev.com/a3345beb33439ab18fb8fbcad1d41ad40bb73290/third_party/blink/web_tests/fast/peerconnection/resources/statechange-iframe-destroy-child.html
[add] https://crrev.com/a3345beb33439ab18fb8fbcad1d41ad40bb73290/third_party/blink/web_tests/fast/peerconnection/statechange-iframe-destroy-parent.html


### na...@google.com (2020-04-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-04-23)

Congrats the Panel decided to award $7,500 for this report!

### na...@google.com (2020-04-23)

[Empty comment from Monorail migration]

### ad...@google.com (2020-04-27)

Given that there has been some complexity here, I'm not going to suggest merge to M81 and this can wait for the initial M83 release.

### ad...@google.com (2020-05-15)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-05-18)

[Empty comment from Monorail migration]

### ke...@google.com (2020-05-18)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/955b58ac6182ae85f33f9d684aae1de4502d8253

commit 955b58ac6182ae85f33f9d684aae1de4502d8253
Author: Harald Alvestrand <hta@chromium.org>
Date: Wed May 20 12:41:36 2020

Onstate handler is allowed to close a PeerConnection.

This merge is intended for Chrome OS M81 refresh.

(cherry picked from commit 919dd0c1244afdb269d023dd178bec8caec372ab)

Bug: chromium:1068084
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2146542
Commit-Queue: Harald Alvestrand <hta@chromium.org>
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#759242}
Cr-Original-Branched-From: 8ad47e8d21f6866e4a37f47d83a860d41debf514-refs/heads/master@{#756066}
Change-Id: I1c4be7bff6391457492aa016818f5d72bd7aa6be
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2209064
Commit-Queue: Mattias Nissler <mnissler@chromium.org>
Reviewed-by: Harald Alvestrand <hta@chromium.org>
Cr-Commit-Position: refs/branch-heads/4044@{#1017}
Cr-Branched-From: a6d9daf149a473ceea37f629c41d4527bf2055bd-refs/heads/master@{#737173}

[modify] https://crrev.com/955b58ac6182ae85f33f9d684aae1de4502d8253/third_party/blink/renderer/modules/peerconnection/mock_rtc_peer_connection_handler_client.h
[modify] https://crrev.com/955b58ac6182ae85f33f9d684aae1de4502d8253/third_party/blink/renderer/modules/peerconnection/mock_rtc_peer_connection_handler_platform.cc
[modify] https://crrev.com/955b58ac6182ae85f33f9d684aae1de4502d8253/third_party/blink/renderer/modules/peerconnection/mock_rtc_peer_connection_handler_platform.h
[modify] https://crrev.com/955b58ac6182ae85f33f9d684aae1de4502d8253/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc
[modify] https://crrev.com/955b58ac6182ae85f33f9d684aae1de4502d8253/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.h
[modify] https://crrev.com/955b58ac6182ae85f33f9d684aae1de4502d8253/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc
[modify] https://crrev.com/955b58ac6182ae85f33f9d684aae1de4502d8253/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.h
[modify] https://crrev.com/955b58ac6182ae85f33f9d684aae1de4502d8253/third_party/blink/renderer/platform/peerconnection/rtc_peer_connection_handler_client.h
[modify] https://crrev.com/955b58ac6182ae85f33f9d684aae1de4502d8253/third_party/blink/renderer/platform/peerconnection/rtc_peer_connection_handler_platform.h
[add] https://crrev.com/955b58ac6182ae85f33f9d684aae1de4502d8253/third_party/blink/web_tests/fast/peerconnection/resources/statechange-iframe-destroy-child.html
[add] https://crrev.com/955b58ac6182ae85f33f9d684aae1de4502d8253/third_party/blink/web_tests/fast/peerconnection/statechange-iframe-destroy-parent.html


### ad...@chromium.org (2020-05-21)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-06-30)

hta@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### [Deleted User] (2020-07-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-07-23)

This issue was migrated from crbug.com/chromium/1068084?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1072261]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051946)*
