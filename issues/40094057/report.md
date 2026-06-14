# Heap-use-after-free in aura::EventObserverAdapter::~EventObserverAdapter

| Field | Value |
|-------|-------|
| **Issue ID** | [40094057](https://issues.chromium.org/issues/40094057) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Aura |
| **Platforms** | ChromeOS |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ms...@chromium.org |
| **Created** | 2019-02-16 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=5101997038632960

Fuzzer: attekett_dom_fuzzer
Job Type: linux_asan_chrome_chromeos
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x613000177f28
Crash State:
  aura::EventObserverAdapter::~EventObserverAdapter
  views::EventMonitorAura::~EventMonitorAura
  BrowserView::~BrowserView
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_chromeos&range=628877:628880

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5101997038632960

Additional requirements: Requires Gestures

Issue filed automatically.

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

## Timeline

### sh...@chromium.org (2019-02-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-17)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-02-17)

[Empty comment from Monorail migration]

### xz...@chromium.org (2019-02-19)

msw@, there is a heap use after free bug in the code https://chromium.googlesource.com/chromium/src/+/4310fc145ccae10b1dfb9f6c9aa284e08ad93478, could you please take a look. Please let me know if you need any help. Thanks.

[Monorail components: UI>Aura]

### ms...@chromium.org (2019-02-22)

It looks like FullscreenControlHost's EventMonitor on the browser window is destroyed after the window itself is destroyed. I suspect that we'll want something in FullscreenControlHost that explicitly destroys the EventMonitor when the window is closing. +CC directory owners.

### ms...@chromium.org (2019-02-22)

I added the current pattern in https://chromium-review.googlesource.com/c/chromium/src/+/1258217
I was able to repro the ClusterFuzz test case locally, I'll try to draft a fix.

### sk...@chromium.org (2019-02-22)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-02-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9406979e93f08ccec156d91698a09f551611ffc2

commit 9406979e93f08ccec156d91698a09f551611ffc2
Author: Mike Wasserman <msw@chromium.org>
Date: Mon Feb 25 22:22:42 2019

Fix event monitoring teardown on window destruction

Add WindowMonitorAura; removes pre-target handler in OnWindowDestroying.
Fixes UAF when EventMonitors are destroyed late in window destruction.
(avoid EventTarget::RemovePreTargetHandler calls later in destruction)

Add a simple unit test.

Bug: 932922
Test: No crash when quitting Chrome with a fullscreen tab.
Change-Id: I2ace83b9de127d8fa70a57021dda94561f5bd4c4
Reviewed-on: https://chromium-review.googlesource.com/c/1487353
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: Michael Wasserman <msw@chromium.org>
Cr-Commit-Position: refs/heads/master@{#635284}
[modify] https://crrev.com/9406979e93f08ccec156d91698a09f551611ffc2/ui/views/event_monitor_aura.cc
[modify] https://crrev.com/9406979e93f08ccec156d91698a09f551611ffc2/ui/views/event_monitor_aura.h
[modify] https://crrev.com/9406979e93f08ccec156d91698a09f551611ffc2/ui/views/event_monitor_unittest.cc


### cl...@chromium.org (2019-02-26)

ClusterFuzz has detected this issue as fixed in range 635283:635284.

Detailed report: https://clusterfuzz.com/testcase?key=5101997038632960

Fuzzer: attekett_dom_fuzzer
Job Type: linux_asan_chrome_chromeos
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x613000177f28
Crash State:
  aura::EventObserverAdapter::~EventObserverAdapter
  views::EventMonitorAura::~EventMonitorAura
  BrowserView::~BrowserView
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_chromeos&range=628877:628880
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_chromeos&range=635283:635284

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5101997038632960

Additional requirements: Requires Gestures

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2019-02-26)

ClusterFuzz testcase 5101997038632960 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2019-02-26)

[Empty comment from Monorail migration]

### ms...@chromium.org (2019-02-26)

Requesting merge of change #635284 to M-73, branch 3683.
The cause of the UAF, change #599303, landed before the branch point.

### sh...@chromium.org (2019-02-26)

This bug requires manual review: We are only 13 days from stable.
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), cindyb@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ci...@chromium.org (2019-02-26)

Merge request in #12, link doesn't work. Are you asking to merge the CL in #8?

### ms...@chromium.org (2019-02-26)

Yes, I'd like to merge the CL from https://crbug.com/chromium/932922#c8:
 https://chromium-review.googlesource.com/c/1487353

### sh...@chromium.org (2019-02-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-27)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ci...@chromium.org (2019-02-27)

Merge approved, M73.

### cr...@appspot.gserviceaccount.com (2019-02-27)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/9f780d40f093385f738cfd76dbd368fcb6a225f5

Commit: 9f780d40f093385f738cfd76dbd368fcb6a225f5
Author: msw@chromium.org
Commiter: msw@chromium.org
Date: 2019-02-27 22:42:57 +0000 UTC

Fix event monitoring teardown on window destruction

Add WindowMonitorAura; removes pre-target handler in OnWindowDestroying.
Fixes UAF when EventMonitors are destroyed late in window destruction.
(avoid EventTarget::RemovePreTargetHandler calls later in destruction)

Add a simple unit test.

Bug: 932922
Test: No crash when quitting Chrome with a fullscreen tab.
Change-Id: I2ace83b9de127d8fa70a57021dda94561f5bd4c4
Reviewed-on: https://chromium-review.googlesource.com/c/1487353
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: Michael Wasserman <msw@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#635284}(cherry picked from commit 9406979e93f08ccec156d91698a09f551611ffc2)
Reviewed-on: https://chromium-review.googlesource.com/c/1493159
Reviewed-by: Michael Wasserman <msw@chromium.org>
Cr-Commit-Position: refs/branch-heads/3683@{#678}
Cr-Branched-From: e51029943e0a38dd794b73caaf6373d5496ae783-refs/heads/master@{#625896}

### na...@google.com (2019-03-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-03-07)

Congrats! The Panel decided to reward $1,000 + $500 fuzzer bonus for this report. 

### aw...@google.com (2019-03-07)

[Empty comment from Monorail migration]

### at...@gmail.com (2019-03-08)

Great. Thanks.

### aw...@google.com (2019-04-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/932922?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094057)*
