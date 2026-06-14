# DCHECK failure in !array_buffer_transfer_map_.Find(array_buffer) in value-serializer.cc

| Field | Value |
|-------|-------|
| **Issue ID** | [40092446](https://issues.chromium.org/issues/40092446) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | bi...@chromium.org |
| **Created** | 2018-09-12 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=4692396494028800

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  !array_buffer_transfer_map_.Find(array_buffer) in value-serializer.cc
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=42748:42749

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4692396494028800

Issue filed automatically.

See https://github.com/google/clusterfuzz-tools for more information.

## Timeline

### cl...@chromium.org (2018-09-12)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/966355585bb3e6e21c063c2b670045f5a75e5aa5 ([d8] Use ValueSerializer for postMessage (instead of ad-hoc serializer)).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### sh...@chromium.org (2018-09-13)

[Empty comment from Monorail migration]

### rs...@chromium.org (2018-09-13)

[Empty comment from Monorail migration]

### bi...@chromium.org (2018-09-13)

I was able to repro this DCHECK locally in d8 with the following repro:

    const worker = new Worker("onmessage = function(){}");
    const buffer = new ArrayBuffer();
    worker.postMessage(buffer, [buffer, buffer]);

This is a misuse of the ValueSerializer API in d8.cc only, not in blink.

The bug occurs because ValueSerializer::TransferArrayBuffer is expecting that it will only be given buffers which have already been deduped. See the equivalent code in blink that validates this: https://cs.chromium.org/chromium/src/third_party/blink/renderer/bindings/core/v8/serialization/serialized_script_value.cc?type=cs&sq=package:chromium&g=0&l=490

In d8, this transferables array is passed directly: https://cs.chromium.org/chromium/src/v8/src/d8.cc?q=d8.cc&sq=package:chromium&dr&l=3193

### sh...@chromium.org (2018-09-14)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2018-09-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/0de680bd21d7316a27e909ff9dee9e1dbe6012cc

commit 0de680bd21d7316a27e909ff9dee9e1dbe6012cc
Author: Ben Smith <binji@chromium.org>
Date: Fri Sep 14 17:33:19 2018

[d8] Fix DCHECK when transferring ArrayBuffer twice

Bug: chromium:883492
Change-Id: I69e76eb51c635d092918a3cb9a8fa94a86f58f2a
Reviewed-on: https://chromium-review.googlesource.com/1226410
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
Commit-Queue: Ben Smith <binji@chromium.org>
Cr-Commit-Position: refs/heads/master@{#55923}
[modify] https://crrev.com/0de680bd21d7316a27e909ff9dee9e1dbe6012cc/src/d8.cc
[modify] https://crrev.com/0de680bd21d7316a27e909ff9dee9e1dbe6012cc/test/mjsunit/d8/d8-worker.js


### bi...@chromium.org (2018-09-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-09-15)

ClusterFuzz has detected this issue as fixed in range 55922:55923.

Detailed report: https://clusterfuzz.com/testcase?key=4692396494028800

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  !array_buffer_transfer_map_.Find(array_buffer) in value-serializer.cc
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=42748:42749
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=55922:55923

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4692396494028800

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2018-09-15)

ClusterFuzz testcase 4692396494028800 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2018-09-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-10-04)

$3,000 for the bug and $500 cluserfuzz bonus :-)

### aw...@chromium.org (2018-10-04)

[Empty comment from Monorail migration]

### aw...@google.com (2018-11-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-12-22)

This issue was migrated from crbug.com/chromium/883492?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092446)*
