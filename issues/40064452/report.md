# Heap-use-after-free in v8::internal::TracedHandles::Destroy

| Field | Value |
|-------|-------|
| **Issue ID** | [40064452](https://issues.chromium.org/issues/40064452) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>API, Blink>JavaScript>Runtime |
| **Platforms** | Linux, Mac |
| **Reporter** | m....@gmail.com |
| **Assignee** | bi...@chromium.org |
| **Created** | 2023-05-09 |
| **Bounty** | $7,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=6346768680419328

Fuzzer: b0ring_webidl_fuzzer
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: Heap-use-after-free READ 2
Crash Address: 0x50c0001a267a
Crash State:
  v8::internal::TracedHandles::Destroy
  blink::ScriptValue::~ScriptValue
  blink::v8_readable_stream::ConstructorCallback
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_media&range=1137634:1137649

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6346768680419328

Issue filed automatically.

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Timeline

### [Deleted User] (2023-05-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-05-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-05-09)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript>API Blink>JavaScript>Runtime]

### cl...@chromium.org (2023-05-09)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/bc6efe2501723737aa541bc0e4833a2e0622a4d9 (Reland "Parallelize young wrapper reclamation").

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### [Deleted User] (2023-05-09)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-09)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bi...@chromium.org (2023-05-09)

I managed to reproduce the issue. However, printf-debugging makes it irreproducable. I'll revert the original CL to unblock the release.

### bi...@chromium.org (2023-05-09)

Actually, looks like the issue is that the parallel reclamizer preliminary destroys nodes with `nullptr` forwarding pointers, which could actually correspond to `TracedReference<> v(Smi(0))`. I'll prepare a fix.

### gi...@appspot.gserviceaccount.com (2023-05-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/caf7eb1c1b6651c4577c722dd2db5019cce1050a

commit caf7eb1c1b6651c4577c722dd2db5019cce1050a
Author: Anton Bikineev <bikineev@chromium.org>
Date: Tue May 09 18:35:34 2023

[traced handles] Use a separate bit to mark to-be-freed traced nodes

Marking a forwarding pointer as nullptr is not correct, since it breaks
for SMIs.

Bug: chromium:1444025
Change-Id: I5b89cae978a9119481da1234b2af21b048e73b41
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4517982
Commit-Queue: Anton Bikineev <bikineev@chromium.org>
Commit-Queue: Michael Lippautz <mlippautz@chromium.org>
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Auto-Submit: Anton Bikineev <bikineev@chromium.org>
Cr-Commit-Position: refs/heads/main@{#87544}

[modify] https://crrev.com/caf7eb1c1b6651c4577c722dd2db5019cce1050a/src/handles/traced-handles.cc


### cl...@chromium.org (2023-05-10)

ClusterFuzz testcase 6346768680419328 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_media&range=1141766:1141779

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2023-05-13)

[Empty comment from Monorail migration]

### am...@google.com (2023-05-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-05-18)

Congratulations! The VRP Panel has decided to award you $7,000 for this report + $2,000 fuzzer bonus. Thank you for your contributions to Chrome fuzzing that resulted in this finding -- great work! 

### am...@google.com (2023-05-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-26)

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M115. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge approved: your change passed merge requirements and is auto-approved for M115. Please go ahead and merge the CL to branch 5790 (refs/branch-heads/5790) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), govind (iOS), dgagnon (ChromeOS), pbommana (Desktop)

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2023-05-26)

Your merge request has been approved for M115 branch, please help complete your merges asap (before Noon PST) Tuesday, so the change can be included in Beta RC build for for next week.

We would like to get the changes as much beta time as possible, so please complete your merges asap to M115 branch(go/chrome-branches).


### pb...@google.com (2023-05-30)

[Bulk Edit] Your CL has been approved for M115 merge, please help complete your merges asap (before 1Pm PST) today, so the change can be included in this week's RC build for M115 beta release.`

### [Deleted User] (2023-05-30)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-05)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-06-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1444025?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript>API, Blink>JavaScript>Runtime]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064452)*
