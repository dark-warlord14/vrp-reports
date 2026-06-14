# Heap-buffer-overflow in blink::FindBuffer::RangeFromBufferIndex

| Field | Value |
|-------|-------|
| **Issue ID** | [40093972](https://issues.chromium.org/issues/40093972) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>Editing |
| **Platforms** | Linux, Mac |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ra...@chromium.org |
| **Created** | 2019-02-06 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=6231480191811584

Fuzzer: jesse_avalanche
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 8
Crash Address: 0x60500016a068
Crash State:
  blink::FindBuffer::RangeFromBufferIndex
  blink::FindBuffer::FindMatchInRange
  blink::FindStringBetweenPositions
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=628681:628683

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6231480191811584

Issue filed automatically.

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

## Timeline

### cl...@chromium.org (2019-02-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-02-06)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>Editing]

### cl...@chromium.org (2019-02-06)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/1cf15c7f5ed50ba69cba650092a73d619199f9a7 (Make FindStringBetweenPositions use FindBuffer and activate invisible matches).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### ra...@chromium.org (2019-02-07)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-02-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9b6dfe1bc55f2e453a7f9254b3bc76def8931bea

commit 9b6dfe1bc55f2e453a7f9254b3bc76def8931bea
Author: Rakina Zata Amni <rakina@chromium.org>
Date: Thu Feb 07 07:13:40 2019

Make TextSearcherICU skip results with zero length

In some cases TextSearcherICU might find result with zero length.
Example case from ClusterFuzz:

<script>
function go(){
setup()
}
window.onload=go;
function setup(){
window.find('\u0080')
}
</script>
<hr id='id9' contenteditable='true'</noscript>
>

Bug: 929217
Change-Id: Ic13b3a3595ae2feb83a7d54a2e8e532f7717e33b
Reviewed-on: https://chromium-review.googlesource.com/c/1457798
Commit-Queue: Rakina Zata Amni <rakina@chromium.org>
Reviewed-by: Yoshifumi Inoue <yosin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#629894}
[modify] https://crrev.com/9b6dfe1bc55f2e453a7f9254b3bc76def8931bea/third_party/blink/renderer/core/editing/iterators/text_searcher_icu.cc
[modify] https://crrev.com/9b6dfe1bc55f2e453a7f9254b3bc76def8931bea/third_party/blink/renderer/core/editing/iterators/text_searcher_icu_test.cc


### sh...@chromium.org (2019-02-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-07)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ra...@chromium.org (2019-02-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-02-07)

ClusterFuzz has detected this issue as fixed in range 629893:629894.

Detailed report: https://clusterfuzz.com/testcase?key=6231480191811584

Fuzzer: jesse_avalanche
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 8
Crash Address: 0x60500016a068
Crash State:
  blink::FindBuffer::RangeFromBufferIndex
  blink::FindBuffer::FindMatchInRange
  blink::FindStringBetweenPositions
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=628681:628683
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=629893:629894

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6231480191811584

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2019-02-07)

ClusterFuzz testcase 6231480191811584 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### na...@google.com (2019-02-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-02-13)

Congrats! The Panel decided to reward $1000 + $500 fuzzer bonus for this report  :) 

### aw...@chromium.org (2019-02-14)

[Empty comment from Monorail migration]

### aw...@google.com (2019-02-20)

[Empty comment from Monorail migration]

### aw...@google.com (2019-04-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/929217?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093972)*
