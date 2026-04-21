# Heap-use-after-free in blink::PropertyTreeManager::EnsureCompositorTransformNode

| Field | Value |
|-------|-------|
| **Issue ID** | [40056274](https://issues.chromium.org/issues/40056274) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Paint |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | cl...@chromium.org |
| **Assignee** | wa...@chromium.org |
| **Created** | 2021-06-19 |
| **Bounty** | $6,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=5389199505948672

Fuzzer: attekett_dom_fuzzer
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free WRITE 8
Crash Address: 0x6180000687f8
Crash State:
  blink::PropertyTreeManager::EnsureCompositorTransformNode
  blink::PropertyTreeManager::EnsureCompositorTransformNode
  blink::LocalFrameView::PushPaintArtifactToCompositor
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=893939:893994

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5389199505948672

Issue filed automatically.

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5389199505948672 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Timeline

### [Deleted User] (2021-06-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-06-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-06-19)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>Paint]

### cl...@chromium.org (2021-06-19)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/c38fc5198354c14091550eb0dfcfaa7144fb4917 (Don't create cc::ScrollNode for leaf non-composited blink scroll nodes).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### [Deleted User] (2021-06-20)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-06-20)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-06-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/21be9d5f805b90586ac32a03484a03162fd21d81

commit 21be9d5f805b90586ac32a03484a03162fd21d81
Author: Xianzhu Wang <wangxianzhu@chromium.org>
Date: Tue Jun 22 23:30:34 2021

Fix reference into realloacated vector in EnsureCompositorTransformNode()

We must call recursive EnsureCompositorTransformNode() before getting
a reference to the new transform node.

Bug: 1221840
Change-Id: I3eb28aea900805162195ee0ca879b1d87352833c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2981033
Reviewed-by: Philip Rogers <pdr@chromium.org>
Commit-Queue: Xianzhu Wang <wangxianzhu@chromium.org>
Cr-Commit-Position: refs/heads/master@{#894915}

[modify] https://crrev.com/21be9d5f805b90586ac32a03484a03162fd21d81/third_party/blink/renderer/platform/graphics/compositing/property_tree_manager.cc


### cl...@chromium.org (2021-06-23)

ClusterFuzz testcase 5389199505948672 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=894913:894915

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2021-06-23)

[Empty comment from Monorail migration]

### am...@google.com (2021-07-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-07-02)

Congratulations, attekett! The VRP Panel has decided to award you $6000 for this issue - $5000 for the bug + $1000 patch bonus. Thanks again for your contributions to Chrome fuzzing!

### at...@gmail.com (2021-07-02)

@amyressler: What is the reason for the patch bonus? I didn't fix the issue. 

### am...@chromium.org (2021-07-02)

attekett@ - sorry, I meant fuzzer bonus, not patch bonus! $1k fuzzer bonus. :) 

### at...@gmail.com (2021-07-02)

Awesome. I was already sweating, that the reward went to wrong issue  Thanks. :)

### am...@google.com (2021-07-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1221840?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056274)*
