# Use-after-poison in content::InspectorMediaEventHandler::SendQueuedMediaEvents

| Field | Value |
|-------|-------|
| **Issue ID** | [40059870](https://issues.chromium.org/issues/40059870) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Media |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | tm...@chromium.org |
| **Created** | 2022-06-05 |
| **Bounty** | $6,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=5643524016111616

Fuzzer: b0ring_webidl_fuzzer
Job Type: linux_asan_content_shell_drt
Platform Id: linux

Crash Type: Use-after-poison READ 8
Crash Address: 0x7e830024abb0
Crash State:
  content::InspectorMediaEventHandler::SendQueuedMediaEvents
  content::BatchingMediaLog::SendQueuedMediaEvents
  content::BatchingMediaLog::~BatchingMediaLog
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_content_shell_drt&range=1009655:1009670

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5643524016111616

Issue filed automatically.

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Timeline

### [Deleted User] (2022-06-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-06-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-06-05)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Media]

### cl...@chromium.org (2022-06-05)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/cfe0c45075ae34fb7b0f7cb2b2a3b1fb72ae86bf ([task] Expose CreateJob()).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### et...@chromium.org (2022-06-06)

Re-assigning to original author of the code.

### [Deleted User] (2022-06-06)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-06)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ct...@chromium.org (2022-06-06)

FYI https://crbug.com/chromium/1332504 from the fuzzer contributor has what should be a more useful repro test case. I'll CC you all onto that bug as well for visibility.

### tm...@chromium.org (2022-06-06)

@CC Eugene so you can see the bug for code review

### tm...@chromium.org (2022-06-06)

[Empty comment from Monorail migration]

### tm...@chromium.org (2022-06-06)

Patch here, FYI: https://chromium-review.googlesource.com/c/chromium/src/+/3689639

### ct...@chromium.org (2022-06-06)

Quick question for m.cooolie@: With your test case from https://crbug.com/chromium/1332504 were you able to repro in Chrome 102 (Stable)? I want to make sure we have the appropriate impact labels set for this. Thanks!

### tm...@chromium.org (2022-06-06)

@cthomp good news and bad news, this regression was caused by a fix for a different issue here: https://bugs.chromium.org/p/chromium/issues/detail?id=1317714#c29

which I just merged the patch back to 102 this morning, before seeing this bug (ie, i first noticed the chat messages this morning to get it merged and just did that)

This will almost certainly have to also be merged back

### tm...@chromium.org (2022-06-06)

[Empty comment from Monorail migration]

### tm...@chromium.org (2022-06-06)

[Empty comment from Monorail migration]

### ct...@chromium.org (2022-06-06)

Thanks tmathmeyer@ and no worries -- adding the FoundIn-102 label so all the proper tooling kicks in for merges :-)

### [Deleted User] (2022-06-06)

[Empty comment from Monorail migration]

### tm...@chromium.org (2022-06-06)

also just noting for myself when I merge this back to 102 that https://bugs.chromium.org/p/chromium/issues/detail?id=1317714#c29 also needs that same merge back

### gi...@appspot.gserviceaccount.com (2022-06-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1bbfaf23cd8a1e977cb445a82a4caae107632a59

commit 1bbfaf23cd8a1e977cb445a82a4caae107632a59
Author: Ted Meyer <tmathmeyer@chromium.org>
Date: Tue Jun 07 02:54:55 2022

Add Stop method to BatchingMediaLog

Now that ~MediaLog is posted for a later destruction due to garbage
collector ownership of CodecLogger, it's possible for the
SendQueuedMediaEvents call from ~BatchingMediaLog to reference
InspectorMediaEventHandler::inspector_context_ after it has been freed.

This fix forces BatchingMediaLog to shut down it's logging capabilities
when the destruction call is caused by the garbage collector deletion
phase

R=liberato

Bug: 1333333
Change-Id: I0bdca72a71177c4c5a6a9dc692aad3de4c25f4e2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3689639
Commit-Queue: Ted (Chromium) Meyer <tmathmeyer@chromium.org>
Reviewed-by: Eugene Zemtsov <eugene@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1011247}

[modify] https://crrev.com/1bbfaf23cd8a1e977cb445a82a4caae107632a59/third_party/blink/renderer/modules/webcodecs/codec_logger.h
[modify] https://crrev.com/1bbfaf23cd8a1e977cb445a82a4caae107632a59/media/base/media_log.h
[modify] https://crrev.com/1bbfaf23cd8a1e977cb445a82a4caae107632a59/content/renderer/media/batching_media_log.cc
[modify] https://crrev.com/1bbfaf23cd8a1e977cb445a82a4caae107632a59/media/base/media_log.cc
[modify] https://crrev.com/1bbfaf23cd8a1e977cb445a82a4caae107632a59/content/renderer/media/batching_media_log.h


### tm...@chromium.org (2022-06-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-06-07)

ClusterFuzz testcase 5643524016111616 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_content_shell_drt&range=1011240:1011248

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### ad...@google.com (2022-06-07)

We discussed merging this into M103 over on https://crbug.com/chromium/1317714, so adding a merge request. (Sheriffbot would have done this tomorrow anyway).

### ad...@google.com (2022-06-07)

Approving merge to M103, branch 5060, because this should go along with the fix for https://crbug.com/chromium/1317714.

### gi...@appspot.gserviceaccount.com (2022-06-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ecad352cd61420d6bf8c9c39041b5369372ecf94

commit ecad352cd61420d6bf8c9c39041b5369372ecf94
Author: Ted Meyer <tmathmeyer@chromium.org>
Date: Wed Jun 08 04:33:20 2022

Add Stop method to BatchingMediaLog

Now that ~MediaLog is posted for a later destruction due to garbage
collector ownership of CodecLogger, it's possible for the
SendQueuedMediaEvents call from ~BatchingMediaLog to reference
InspectorMediaEventHandler::inspector_context_ after it has been freed.

This fix forces BatchingMediaLog to shut down it's logging capabilities
when the destruction call is caused by the garbage collector deletion
phase

R=​liberato

(cherry picked from commit 1bbfaf23cd8a1e977cb445a82a4caae107632a59)

Bug: 1333333
Change-Id: I0bdca72a71177c4c5a6a9dc692aad3de4c25f4e2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3689639
Commit-Queue: Ted (Chromium) Meyer <tmathmeyer@chromium.org>
Reviewed-by: Eugene Zemtsov <eugene@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1011247}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3694435
Auto-Submit: Ted (Chromium) Meyer <tmathmeyer@chromium.org>
Reviewed-by: Eugene Zemtsov <ezemtsov@google.com>
Commit-Queue: Eugene Zemtsov <eugene@chromium.org>
Cr-Commit-Position: refs/branch-heads/5060@{#672}
Cr-Branched-From: b83393d0f4038aeaf67f970a024d8101df7348d1-refs/heads/main@{#1002911}

[modify] https://crrev.com/ecad352cd61420d6bf8c9c39041b5369372ecf94/third_party/blink/renderer/modules/webcodecs/codec_logger.h
[modify] https://crrev.com/ecad352cd61420d6bf8c9c39041b5369372ecf94/media/base/media_log.h
[modify] https://crrev.com/ecad352cd61420d6bf8c9c39041b5369372ecf94/content/renderer/media/batching_media_log.cc
[modify] https://crrev.com/ecad352cd61420d6bf8c9c39041b5369372ecf94/media/base/media_log.cc
[modify] https://crrev.com/ecad352cd61420d6bf8c9c39041b5369372ecf94/content/renderer/media/batching_media_log.h


### am...@chromium.org (2022-06-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-06-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-06-24)

Congratulations on another one! The VRP Panel has decided to award you $5,000 for this report + $1,000 fuzzer bonus. Thank you for your efforts in Chrome Fuzzing and nice work! 

### am...@chromium.org (2022-07-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mo...@microsoft-edge-infrastructure.iam.gserviceaccount.com (2022-10-31)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1333333?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1332504]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059870)*
