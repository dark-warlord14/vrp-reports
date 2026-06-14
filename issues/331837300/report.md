# Crash in v8::internal::Heap::InYoungGeneration

| Field | Value |
|-------|-------|
| **Issue ID** | [331837300](https://issues.chromium.org/issues/331837300) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>JavaScript, Blink>JavaScript>GarbageCollection |
| **Platforms** | Linux |
| **Reporter** | de...@googlemail.com |
| **Assignee** | om...@chromium.org |
| **Created** | 2024-03-28 |
| **Bounty** | $9,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=5145935524331520

Fuzzer: decoder_langfuzz
Job Type: linux_cfi_d8
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x246900d40000
Crash State:
  v8::internal::Heap::InYoungGeneration
  void v8::internal::RememberedSetUpdatingItem::CheckAndUpdateOldToNewSlot<v8::int
  void v8::internal::RememberedSetUpdatingItem::UpdateUntypedOldToNewPointers<
  
Sanitizer: cfi (CFI)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_cfi_d8&range=93037:93038

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5145935524331520

Issue filed automatically.

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Timeline

### 24...@project.gserviceaccount.com (2024-03-28)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2024-03-28)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/2fa2cff7f8c896f23d5dd28550ae0f39ac92239e ([heap] Minor changes around postponing page release).

If this is incorrect, please let us know why and apply the hotlistid:5433122. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### pe...@google.com (2024-03-29)

Setting milestone because of s2 severity.

### pe...@google.com (2024-03-29)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### pe...@google.com (2024-03-29)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ap...@google.com (2024-04-02)

Project: v8/v8
Branch: main

commit 3e7a20bad547b82fe64f717b7587b564799c9730
Author: Omer Katz <omerkatz@chromium.org>
Date:   Tue Apr 02 08:20:26 2024

    [heap] Postpone releasing shared space pages
    
    Old-to-new can be overwritten with refs to shared objects. Thus
    releasing shared pages should be delayed, same as we do for young pages.
    
    Bug: 331837300
    Change-Id: If99d700729724e74392257e9cf92f7bf447fe24c
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5403890
    Commit-Queue: Michael Lippautz <mlippautz@chromium.org>
    Auto-Submit: Omer Katz <omerkatz@chromium.org>
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#93101}

M       src/heap/mark-compact.cc
M       src/heap/paged-spaces.cc
M       src/heap/paged-spaces.h

https://chromium-review.googlesource.com/5403890


### 24...@project.gserviceaccount.com (2024-04-03)

ClusterFuzz testcase 5145935524331520 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_cfi_d8&range=93100:93101

If this is incorrect, please add the hotlistid:5432646 and re-open the issue.

### am...@google.com (2024-04-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-04-11)

Congratulations! The Chrome VRP Panel has decided to award you $7,000 for this report of memory corruption in a sandboxed process + $2,000 fuzzer bonus. Thank you for your past fuzzing contributions that resulted in this report!

### pe...@google.com (2024-04-17)

This is sufficiently serious that it should be merged to dev. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M125. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Merge approved: your change passed merge requirements and is auto-approved for M125. Please go ahead and merge the CL to branch 6422 (refs/branch-heads/6422) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [125].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### am...@chromium.org (2024-04-17)

This fix was landed on 125; no merge needed

### pe...@google.com (2024-07-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/331837300)*
