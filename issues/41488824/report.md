# Heap-use-after-free in webrtc::JsepTransportController::ValidateAndMaybeUpdateBundleGroups

| Field | Value |
|-------|-------|
| **Issue ID** | [41488824](https://issues.chromium.org/issues/41488824) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>WebRTC |
| **Platforms** | Linux |
| **Reporter** | m....@gmail.com |
| **Assignee** | to...@webrtc.org |
| **Created** | 2024-01-05 |
| **Bounty** | $9,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=5162171615346688

Fuzzer: b0ring_webidl_fuzzer
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x50d0000b05b0
Crash State:
  webrtc::JsepTransportController::ValidateAndMaybeUpdateBundleGroups
  webrtc::JsepTransportController::ApplyDescription_n
  webrtc::JsepTransportController::SetRemoteDescription
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=960390:960394

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5162171615346688

Issue filed automatically.

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Timeline

### [Deleted User] (2024-01-05)

[Empty comment from Monorail migration]

### dt...@chromium.org (2024-01-05)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-05)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fl...@google.com (2024-01-05)

[Empty comment from Monorail migration]

[Monorail components: Blink>WebRTC]

### fl...@google.com (2024-01-05)

Hi Tomas, I'm assigning this to you since, of the CLs within the regerssion range indicated by ClusterFuzz, https://webrtc-review.googlesource.com/c/src/+/245641 looked like a *possible* culprit—but, I'm not very familiar with WebRTC, so I could be very wrong.  Please reassign this bug to someone more appropriate if so!

### fl...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### m....@gmail.com (2024-01-10)

It seems that Tomas may have been absent for a long time, so we should find someone else to handle the issue.

### to...@webrtc.org (2024-01-11)

Taking a look, sorry about the delay.

Patch up for review: https://webrtc-review.googlesource.com/c/src/+/334061

### cl...@chromium.org (2024-01-13)

ClusterFuzz testcase 5162171615346688 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1246318:1246323

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2024-01-13)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-13)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M120. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M121. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [120, 121].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-14)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M120. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M121. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [120, 121].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### to...@chromium.org (2024-01-15)

1. Which CLs should be backmerged? (Please include Gerrit links.)

https://webrtc-review.googlesource.com/c/src/+/334061

2. Has this fix been verified on Canary to not pose any stability regressions?

Yes

3. Does this fix pose any potential non-verifiable stability risks?

No

4. Does this fix pose any known compatibility risks?

No

5. Does it require manual verification by the test team? If so, please describe required testing.

Aside from regular functionality which is verified with regular testing, the attached test case from https://crbug.com/chromium/1515832#c1, can be used to verify the fix.

### [Deleted User] (2024-01-15)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M120. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M121. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [120, 121].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### to...@chromium.org (2024-01-15)

Re: Is there a fix in some other repo which should be merged?

Yes, WebRTC.
I can manually cherry pick the CL to the right branches (https://webrtc-review.googlesource.com/c/src/+/334061).

### [Deleted User] (2024-01-16)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M120. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M121. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [120, 121].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2024-01-18)

Thank you for the fix!! The change has been in Canary for 5+ days, and canary data shows no stability issues seem to have been introduced with the fix.

Merge approved for M120 - please cherry pick to branch by Thursday Jan 18 EOD MTV time to get this fix into the next extended release!
Merge approved for M121 - please cherry pick to branch by Thursday Jan 18 EOD MTV time to get this fix into the next stable release!

### am...@google.com (2024-01-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-01-19)

Congratulations! The Chrome VRP Panel has decided to award you $7,000 for this fuzzing report + $2,000 fuzzing bonus. Thank you for your fuzzing contributions to Chrome fuzzing that resulted in this report -- nice work! 

### da...@google.com (2024-01-19)

[Empty comment from Monorail migration]

### am...@google.com (2024-01-20)

[Empty comment from Monorail migration]

### pg...@google.com (2024-01-22)

Hi tommi@! I've confused the merge schedules, and this was not ready to be merge approved for M120 - this release will be recut this morning in MTV time. Could you revert the M120 cherry pick (https://webrtc-review.googlesource.com/c/src/+/335180) for now to re-merge later on? Sorry for the bother and trouble!!

### gi...@appspot.gserviceaccount.com (2024-01-22)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/bf2e30678e0e5b21f2a2d49180a13225fdcfaa1a

commit bf2e30678e0e5b21f2a2d49180a13225fdcfaa1a
Author: Tomas Gunnarsson <tommi@webrtc.org>
Date: Mon Jan 22 09:24:19 2024

Revert "[M120] JsepTransportController: Remove raw pointers to description objects"

This reverts commit e79a99060f70a356b131d9f2f7497914984944d1.

Reason for revert: Merged too early. Will re-land for the next spin.

Original change's description:
> [M120] JsepTransportController: Remove raw pointers to description objects
>
> Remove member variables that point to objects owned externally (in practice by SdpOfferAnswerHandler). The objects also live on the
> signaling thread whereas JsepTransportController performs
> operations on the network thread. Removing the raw pointers avoids
> the risk of referencing the description objects after they've been
> deleted or if the state is inconsistent across threads.
>
> (cherry picked from commit c56052001dd747ae37c0cf7bab604791fe7912b0)
>
> Bug: webrtc:1515832
> No-Try: true
> Change-Id: I852b2a3993964be817f93c46b5bc4b03121cde86
> Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/334061
> Commit-Queue: Tomas Gunnarsson <tommi@webrtc.org>
> Reviewed-by: Harald Alvestrand <hta@webrtc.org>
> Cr-Original-Commit-Position: refs/heads/main@{#41505}
> Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/335180
> Reviewed-by: Mirko Bonadei <mbonadei@webrtc.org>
> Cr-Commit-Position: refs/branch-heads/6099@{#2}
> Cr-Branched-From: 507f1cc3270d0577f79882acbd78e63e66008f3d-refs/heads/main@{#41042}

Change-Id: Id4bd21fbc8b7306de1aba0854815ada5c9333468
No-Try: true
Bug: chromium:1515832
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/335620
Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Tomas Gunnarsson <tommi@webrtc.org>
Reviewed-by: Mirko Bonadei <mbonadei@webrtc.org>
Cr-Commit-Position: refs/branch-heads/6099@{#3}
Cr-Branched-From: 507f1cc3270d0577f79882acbd78e63e66008f3d-refs/heads/main@{#41042}

[modify] https://crrev.com/bf2e30678e0e5b21f2a2d49180a13225fdcfaa1a/pc/jsep_transport_controller_unittest.cc
[modify] https://crrev.com/bf2e30678e0e5b21f2a2d49180a13225fdcfaa1a/test/peer_scenario/scenario_connection.cc
[modify] https://crrev.com/bf2e30678e0e5b21f2a2d49180a13225fdcfaa1a/pc/jsep_transport_controller.cc
[modify] https://crrev.com/bf2e30678e0e5b21f2a2d49180a13225fdcfaa1a/pc/sdp_offer_answer.cc
[modify] https://crrev.com/bf2e30678e0e5b21f2a2d49180a13225fdcfaa1a/pc/jsep_transport_controller.h


### am...@chromium.org (2024-01-23)

now that M121 Stable has shipped and this fix will be included in the next M121 update, please go ahead and reland the M120 merge for https://webrtc-review.googlesource.com/c/src/+/334061 to 6099 at your earliest convenience (before EOD Thursday 25 January) so this fix can be included in the next M120 Extended Stable update along site the next M121 Stable update next week -- thank you! 

### gi...@appspot.gserviceaccount.com (2024-01-26)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/5ab829e4ca8f63be6b4ed1d98eee382d7307d34e

commit 5ab829e4ca8f63be6b4ed1d98eee382d7307d34e
Author: Tomas Gunnarsson <tommi@webrtc.org>
Date: Fri Jan 26 12:01:53 2024

Revert^2 "[M120] JsepTransportController: Remove raw pointers to description objects"

This reverts commit bf2e30678e0e5b21f2a2d49180a13225fdcfaa1a.

Reason for revert: Time to reland the fix for M120 now.

Original change's description:
> Revert "[M120] JsepTransportController: Remove raw pointers to description objects"
>
> This reverts commit e79a99060f70a356b131d9f2f7497914984944d1.
>
> Reason for revert: Merged too early. Will re-land for the next spin.
>
> Original change's description:
> > [M120] JsepTransportController: Remove raw pointers to description objects
> >
> > Remove member variables that point to objects owned externally (in practice by SdpOfferAnswerHandler). The objects also live on the
> > signaling thread whereas JsepTransportController performs
> > operations on the network thread. Removing the raw pointers avoids
> > the risk of referencing the description objects after they've been
> > deleted or if the state is inconsistent across threads.
> >
> > (cherry picked from commit c56052001dd747ae37c0cf7bab604791fe7912b0)
> >
> > Bug: webrtc:1515832
> > No-Try: true
> > Change-Id: I852b2a3993964be817f93c46b5bc4b03121cde86
> > Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/334061
> > Commit-Queue: Tomas Gunnarsson <tommi@webrtc.org>
> > Reviewed-by: Harald Alvestrand <hta@webrtc.org>
> > Cr-Original-Commit-Position: refs/heads/main@{#41505}
> > Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/335180
> > Reviewed-by: Mirko Bonadei <mbonadei@webrtc.org>
> > Cr-Commit-Position: refs/branch-heads/6099@{#2}
> > Cr-Branched-From: 507f1cc3270d0577f79882acbd78e63e66008f3d-refs/heads/main@{#41042}
>
> Change-Id: Id4bd21fbc8b7306de1aba0854815ada5c9333468
> No-Try: true
> Bug: chromium:1515832
> Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/335620
> Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com>
> Commit-Queue: Tomas Gunnarsson <tommi@webrtc.org>
> Reviewed-by: Mirko Bonadei <mbonadei@webrtc.org>
> Cr-Commit-Position: refs/branch-heads/6099@{#3}
> Cr-Branched-From: 507f1cc3270d0577f79882acbd78e63e66008f3d-refs/heads/main@{#41042}

No-Try: true
Bug: chromium:1515832
Change-Id: I13a24182908d7a616234d9c701bf7000a162df8e
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/336282
Commit-Queue: Tomas Gunnarsson <tommi@webrtc.org>
Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com>
Reviewed-by: Mirko Bonadei <mbonadei@webrtc.org>
Cr-Commit-Position: refs/branch-heads/6099@{#4}
Cr-Branched-From: 507f1cc3270d0577f79882acbd78e63e66008f3d-refs/heads/main@{#41042}

[modify] https://crrev.com/5ab829e4ca8f63be6b4ed1d98eee382d7307d34e/pc/jsep_transport_controller_unittest.cc
[modify] https://crrev.com/5ab829e4ca8f63be6b4ed1d98eee382d7307d34e/test/peer_scenario/scenario_connection.cc
[modify] https://crrev.com/5ab829e4ca8f63be6b4ed1d98eee382d7307d34e/pc/jsep_transport_controller.cc
[modify] https://crrev.com/5ab829e4ca8f63be6b4ed1d98eee382d7307d34e/pc/sdp_offer_answer.cc
[modify] https://crrev.com/5ab829e4ca8f63be6b4ed1d98eee382d7307d34e/pc/jsep_transport_controller.h


### is...@google.com (2024-01-26)

This issue was migrated from crbug.com/chromium/1515832?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1515756]
[Monorail components added to Component Tags custom field.]

### am...@chromium.org (2024-02-09)

tommi@ has relanded a CP for M120: <https://webrtc-review.googlesource.com/c/src/+/338701> as per the request of the Chromebox-for-meetings team

### am...@chromium.org (2024-02-09)

upon request, I've reviewed the original fix (<https://webrtc-review.googlesource.com/c/src/+/334061>) and see no regressions or stability issues since it was landed, please go ahead and merge the new CP to M120 (branch 6099) at your convenience

### sr...@google.com (2024-02-12)

adjusting Merge-approved-120 label as the merge is complete 

### pe...@google.com (2024-04-21)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41488824)*
