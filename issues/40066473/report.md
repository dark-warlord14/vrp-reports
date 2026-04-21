# Security: V8: Fatal error in ../../src/api/api-inl.h, line 55

| Field | Value |
|-------|-------|
| **Issue ID** | [40066473](https://issues.chromium.org/issues/40066473) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Linux |
| **Reporter** | sw...@gmail.com |
| **Assignee** | ol...@chromium.org |
| **Created** | 2023-06-27 |
| **Bounty** | $7,000.00 |

## Description

deleted

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2023-06-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-06-27)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4801004941541376.

### cl...@chromium.org (2023-06-27)

ClusterFuzz testcase 4801004941541376 is closed as invalid, so closing issue.

### cl...@chromium.org (2023-06-27)

Testcase 4801004941541376 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=4801004941541376.

### sa...@google.com (2023-06-28)

Managed to reproduce this on clusterfuzz with --single-threaded. Probably Clusterfuzz shouldn't automatically close issues when it can't reproduce bugs the first time...

### cl...@chromium.org (2023-06-28)

Detailed Report: https://clusterfuzz.com/testcase?key=6305502893637632

Fuzzer: None
Job Type: linux_asan_d8_v8_arm64_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  obj.is_null() || (obj->IsSmi() || !obj->IsTheHole()) in api-inl.h
  v8::Local<v8::Value> v8::Utils::Convert<v8::internal::Object, v8::Value>
  v8::Script::Run
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_d8_v8_arm64_dbg&revision=88536

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6305502893637632

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2023-06-28)

[Empty comment from Monorail migration]

### es...@chromium.org (2023-06-28)

Note: severity is provisional, please adjust if incorrect.

### [Deleted User] (2023-06-28)

[Empty comment from Monorail migration]

### sa...@google.com (2023-06-29)

Clusterfuzz bisects this to https://chromium.googlesource.com/v8/v8/+/7813cd11ec6c11ac045b18aa509190db176a0f39 "[maglev] Enable OSR-in"

[Monorail components: Blink>JavaScript>Compiler>Maglev]

### sa...@google.com (2023-06-30)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-06-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/20ee17b96b04d5083f872327702c31a7b56ca4b8

commit 20ee17b96b04d5083f872327702c31a7b56ca4b8
Author: Olivier Flückiger <olivf@chromium.org>
Date: Fri Jun 30 10:12:36 2023

[maglev] Fix for inlined derived constructor

Handle the case where the inlined derived constructor returns an invalid
receiver.

Drive-By: Fix dcheck in graph builder when a block has no phis.

Bug: chromium:1458291
Bug: v8:7700
Change-Id: Ib7752e67ef1cf86d3cd2760a668a2784a1676b76
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4660402
Commit-Queue: Olivier Flückiger <olivf@chromium.org>
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Cr-Commit-Position: refs/heads/main@{#88583}

[modify] https://crrev.com/20ee17b96b04d5083f872327702c31a7b56ca4b8/src/maglev/maglev-graph-printer.cc
[modify] https://crrev.com/20ee17b96b04d5083f872327702c31a7b56ca4b8/src/maglev/maglev-graph-builder.cc


### ol...@chromium.org (2023-06-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-06-30)

ClusterFuzz testcase 6305502893637632 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_v8_arm64_dbg&range=88582:88583

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2023-06-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-30)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-30)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-01)

Merge approved: your change passed merge requirements and is auto-approved for M116. Please go ahead and merge the CL to branch 5845 (refs/branch-heads/5845) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-07-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/e5daecc522fc93e2a63e898b3cda7a4c9b96e39c

commit e5daecc522fc93e2a63e898b3cda7a4c9b96e39c
Author: Olivier Flückiger <olivf@chromium.org>
Date: Mon Jul 03 07:50:22 2023

Merged: [maglev] Fix for inlined derived constructor

Revision: 20ee17b96b04d5083f872327702c31a7b56ca4b8

Bug: chromium:1458291
Bug: v8:7700
Change-Id: Idf2a2b188309d9fcb366b9fcbd56f218391c522a
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4660490
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Commit-Queue: Olivier Flückiger <olivf@chromium.org>
Cr-Commit-Position: refs/branch-heads/11.6@{#10}
Cr-Branched-From: e29c028f391389a7a60ee37097e3ca9e396d6fa4-refs/heads/11.6.189@{#3}
Cr-Branched-From: 95cbef20e2aa556a1ea75431a48b36c4de6b9934-refs/heads/main@{#88340}

[modify] https://crrev.com/e5daecc522fc93e2a63e898b3cda7a4c9b96e39c/src/maglev/maglev-graph-printer.cc
[modify] https://crrev.com/e5daecc522fc93e2a63e898b3cda7a4c9b96e39c/src/maglev/maglev-graph-builder.cc


### gi...@appspot.gserviceaccount.com (2023-07-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8455181dc8fcb7a7883243f8523859c62e53f770

commit 8455181dc8fcb7a7883243f8523859c62e53f770
Author: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Date: Mon Jul 03 12:18:14 2023

Roll v8 11.6 from 6162fee75b0a to 114ee23f16da (2 revisions)

https://chromium.googlesource.com/v8/v8.git/+log/6162fee75b0a..114ee23f16da

2023-07-03 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.6.189.8
2023-07-03 olivf@chromium.org Merged: [maglev] Fix for inlined derived constructor

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/v8-11-6-chromium-m116
Please CC liviurau@google.com,v8-waterfall-sheriff@grotations.appspotmail.com,vahl@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in v8 11.6: https://bugs.chromium.org/p/v8/issues/entry
To file a bug in Chromium m116: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1458291
Tbr: v8-waterfall-sheriff@grotations.appspotmail.com
Change-Id: I4290a83261b41e31773e0262444aae2f0b3d05c9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4664239
Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5845@{#285}
Cr-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}

[modify] https://crrev.com/8455181dc8fcb7a7883243f8523859c62e53f770/DEPS


### ol...@chromium.org (2023-07-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-07-11)

ClusterFuzz testcase 5130999576592384 is still reproducing on tip-of-tree build (trunk).

Please re-test your fix against this testcase and if the fix was incorrect or incomplete, please re-open the bug. Otherwise, ignore this notification and add the ClusterFuzz-Wrong label.

### am...@chromium.org (2023-07-24)

re-opening for reverification -- clusterfuzz reports this issue to still be reproducible here and via https://crbug.com/chromium/1462809 

### [Deleted User] (2023-07-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-25)

olivf: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ol...@chromium.org (2023-07-25)

This is fixed. clusterfuzz 5130999576592384 which is still open is not a security issue.

### sw...@gmail.com (2023-07-26)

Is there any update regarding VRP information?

### am...@google.com (2023-07-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-07-27)

Congratulations, Zhenjiang Zhao! The VRP Panel has decided to award you $7,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-08-03)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/v8/v8-internal/+/fa07505ebeac74cc4a708c6178c6db2f32cf1e60

commit fa07505ebeac74cc4a708c6178c6db2f32cf1e60
Author: Olivier Flückiger <olivf@chromium.org>
Date: Fri Jun 30 10:05:10 2023


### [Deleted User] (2023-10-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-11-11)

Hello! We consider attachments/POCs and all analysis included with reports to be an integral part of the report (https://g.co/chrome/vrp/#investigating-and-reporting-bugs), even when included in comments, so I have undeleted them. Thanks! 

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1458291?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1459506, crbug.com/chromium/1462809]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40066473)*
