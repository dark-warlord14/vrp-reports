# Security DCHECK failure: !object || (object->IsText()) in layout_text.h

| Field | Value |
|-------|-------|
| **Issue ID** | [40094988](https://issues.chromium.org/issues/40094988) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Layout |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ko...@chromium.org |
| **Created** | 2019-05-12 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=6231084554125312

Fuzzer: attekett_dom_fuzzer
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: Security DCHECK failure
Crash Address: 
Crash State:
  !object || (object->IsText()) in layout_text.h
  blink::LayoutNGListItem::UpdateMarkerText
  blink::NGBlockNode::PrepareForLayout
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_media&range=658681:658686

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6231084554125312

Issue filed automatically.

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

## Timeline

### cl...@chromium.org (2019-05-12)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>Layout]

### sh...@chromium.org (2019-05-13)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-05-13)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-05-13)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ea...@chromium.org (2019-05-13)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-05-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c86fcb0b0dc6094523739f4f4efad57f981a74e0

commit c86fcb0b0dc6094523739f4f4efad57f981a74e0
Author: Koji Ishii <kojii@chromium.org>
Date: Tue May 14 03:14:10 2019

[LayoutNG] Check first-line anonymous more correctly

When |LayoutBlockFlow| adds a child, it assumed all anonymous
|LayoutInline|s are anoymous wrappers for ::first-line, but
there are two other usage of anonymous |LayoutInline|.

This patch checks if it is really an anonymous |LayoutInline|
for ::first-line.

Bug: 962275
Change-Id: Ibbde37297e4636e4f0c51f0ed8249e3166639d76
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1610657
Reviewed-by: Aleks Totic <atotic@chromium.org>
Reviewed-by: Emil A Eklund <eae@chromium.org>
Commit-Queue: Koji Ishii <kojii@chromium.org>
Cr-Commit-Position: refs/heads/master@{#659369}

[modify] https://crrev.com/c86fcb0b0dc6094523739f4f4efad57f981a74e0/third_party/blink/renderer/core/BUILD.gn
[modify] https://crrev.com/c86fcb0b0dc6094523739f4f4efad57f981a74e0/third_party/blink/renderer/core/layout/layout_block_flow.cc
[modify] https://crrev.com/c86fcb0b0dc6094523739f4f4efad57f981a74e0/third_party/blink/renderer/core/layout/layout_inline.cc
[modify] https://crrev.com/c86fcb0b0dc6094523739f4f4efad57f981a74e0/third_party/blink/renderer/core/layout/layout_inline.h
[modify] https://crrev.com/c86fcb0b0dc6094523739f4f4efad57f981a74e0/third_party/blink/renderer/core/layout/layout_object.cc
[modify] https://crrev.com/c86fcb0b0dc6094523739f4f4efad57f981a74e0/third_party/blink/renderer/core/layout/layout_object.h
[modify] https://crrev.com/c86fcb0b0dc6094523739f4f4efad57f981a74e0/third_party/blink/renderer/core/layout/ng/list/layout_ng_inside_list_marker.h
[modify] https://crrev.com/c86fcb0b0dc6094523739f4f4efad57f981a74e0/third_party/blink/renderer/core/layout/ng/list/layout_ng_list_item.cc
[add] https://crrev.com/c86fcb0b0dc6094523739f4f4efad57f981a74e0/third_party/blink/renderer/core/layout/ng/list/layout_ng_list_item_test.cc


### ko...@chromium.org (2019-05-14)

Should be fixed now.

### sh...@chromium.org (2019-05-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-05-14)

ClusterFuzz has detected this issue as fixed in range 659368:659369.

Detailed report: https://clusterfuzz.com/testcase?key=6231084554125312

Fuzzer: attekett_dom_fuzzer
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: Security DCHECK failure
Crash Address: 
Crash State:
  !object || (object->IsText()) in layout_text.h
  blink::LayoutNGListItem::UpdateMarkerText
  blink::NGBlockNode::PrepareForLayout
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_media&range=658681:658686
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_media&range=659368:659369

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6231084554125312

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2019-05-14)

ClusterFuzz testcase 6231084554125312 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### na...@google.com (2019-05-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-05-29)

Congrats! The Panel decided to reward $3,500 for this report 

### aw...@google.com (2019-05-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/962275?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094988)*
