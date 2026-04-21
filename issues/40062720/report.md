# Crash in blink::HTMLFastPathParser<unsigned char>::ParseAttributes

| Field | Value |
|-------|-------|
| **Issue ID** | [40062720](https://issues.chromium.org/issues/40062720) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>HTML>Parser |
| **Platforms** | Linux, Mac |
| **Reporter** | cl...@chromium.org |
| **Assignee** | sk...@chromium.org |
| **Created** | 2023-01-18 |
| **Bounty** | $4,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=4813536265175040

Fuzzer: attekett_dom_fuzzer
Job Type: linux_tsan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7b1400030000
Crash State:
  blink::HTMLFastPathParser<unsigned char>::ParseAttributes
  blink::Element* blink::HTMLFastPathParser<unsigned char>::ParseContainerElement<
  blink::Element* blink::HTMLFastPathParser<unsigned char>::ParseElement<false>
  
Sanitizer: thread (TSAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_tsan_chrome_mp&range=1093398:1093402

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4813536265175040

Issue filed automatically.

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Timeline

### [Deleted User] (2023-01-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-01-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-01-18)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>HTML>Parser]

### cl...@chromium.org (2023-01-18)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/088bf2684bba356c054451201d6834e6f04578ad (blink: adds a fast-path parser for html parsing).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### [Deleted User] (2023-01-18)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-18)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sk...@chromium.org (2023-01-18)

[Empty comment from Monorail migration]

### sk...@chromium.org (2023-01-18)

I will fix this shortly.
I'm going to remove RBS as this is behind a feature, which isn't enabled via finch yet, so no need to block stable.

### [Deleted User] (2023-01-19)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-01-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/77c59444db9c1e8e4017eab305e1340ae7bc8bd2

commit 77c59444db9c1e8e4017eab305e1340ae7bc8bd2
Author: Scott Violet <sky@chromium.org>
Date: Fri Jan 20 00:20:35 2023

blink: ensures html fast path parser doesnt read past end

This fixes a couple of places where it was possible to go
beyond the end of input. This also adds a DCHECK to GetNext()
to ensure haven't gone past end of input.

Bug: 1407201, 1408467
Change-Id: I36394e558b3e62f825399f4de8e30ff64e6c920a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4179036
Reviewed-by: Mason Freed <masonf@chromium.org>
Commit-Queue: Scott Violet <sky@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1094782}

[modify] https://crrev.com/77c59444db9c1e8e4017eab305e1340ae7bc8bd2/third_party/blink/renderer/core/html/parser/html_document_parser_fastpath.cc


### sk...@chromium.org (2023-01-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-01-20)

ClusterFuzz testcase 4813536265175040 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_tsan_chrome_mp&range=1094776:1094782

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### sk...@chromium.org (2023-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-21)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-27)

Congratulations! The VRP Panel has decided to award you $4,000 for this report + fuzzer bonus. Thank you for your efforts toward Chrome Fuzzing! 

### [Deleted User] (2023-01-27)

Not requesting merge to dev (M111) because latest trunk commit (1094782) appears to be prior to dev branch point (1097615). If this is incorrect, please replace the Merge-NA-111 label with Merge-Request-111. If other changes are required to fix this bug completely, please request a merge if necessary.

Merge approved: your change passed merge requirements and is auto-approved for M111. Please go ahead and merge the CL to branch 5563 (refs/branch-heads/5563) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: harrysouders (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-01-27)

this fix landed on M111, no merge needed here 

### am...@google.com (2023-01-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1408467?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1408943]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062720)*
