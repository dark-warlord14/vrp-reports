# Heap-use-after-free in blink::DisplayItemRasterInvalidator::Generate

| Field | Value |
|-------|-------|
| **Issue ID** | [40091909](https://issues.chromium.org/issues/40091909) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Paint |
| **Platforms** | Windows |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ch...@chromium.org |
| **Created** | 2018-07-11 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=5280137512484864

Fuzzer: miaubiz_svg_fuzzer
Job Type: windows_asan_chrome_no_sandbox
Platform Id: windows

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x12516e19bda8
Crash State:
  blink::DisplayItemRasterInvalidator::Generate
  blink::RasterInvalidator::Generate
  blink::RasterInvalidator::Generate
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=windows_asan_chrome_no_sandbox&range=572427:572428

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5280137512484864

Issue filed automatically.

See https://github.com/google/clusterfuzz-tools for more information.

## Attachments

- [test.html](attachments/test.html) (text/plain, 177 B)

## Timeline

### es...@chromium.org (2018-07-11)

chrishtr, could you please take a look? Thanks!

[Monorail components: Blink>Paint]

### es...@chromium.org (2018-07-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-12)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-07-12)

[Empty comment from Monorail migration]

### ch...@chromium.org (2018-07-13)

Reduced testcase attached.

### ch...@chromium.org (2018-07-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-07-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d0f45007eac9033c8480329e88922e36b8c098fa

commit d0f45007eac9033c8480329e88922e36b8c098fa
Author: Chris Harrelson <chrishtr@chromium.org>
Date: Tue Jul 17 19:02:58 2018

Ignore auto z-index when determining IsReplacedNormalFlowStacking.

<foreignObject> is the only element which can be replaced normal flow stacking,
and this element cannot be z-indexed.

Bug: 862635

Cq-Include-Trybots: luci.chromium.try:linux_layout_tests_slimming_paint_v2;master.tryserver.blink:linux_trusty_blink_rel
Change-Id: Ia82a7c648da1d407b38330b7daa280d2baf39d49
Reviewed-on: https://chromium-review.googlesource.com/1137351
Commit-Queue: Chris Harrelson <chrishtr@chromium.org>
Reviewed-by: vmpstr <vmpstr@chromium.org>
Cr-Commit-Position: refs/heads/master@{#575743}
[add] https://crrev.com/d0f45007eac9033c8480329e88922e36b8c098fa/third_party/WebKit/LayoutTests/svg/foreignObject/z-index-crash.html
[modify] https://crrev.com/d0f45007eac9033c8480329e88922e36b8c098fa/third_party/blink/renderer/core/paint/paint_layer.cc


### ch...@chromium.org (2018-07-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-07-18)

ClusterFuzz has detected this issue as fixed in range 575742:575743.

Detailed report: https://clusterfuzz.com/testcase?key=5280137512484864

Fuzzer: miaubiz_svg_fuzzer
Job Type: windows_asan_chrome_no_sandbox
Platform Id: windows

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x12516e19bda8
Crash State:
  blink::DisplayItemRasterInvalidator::Generate
  blink::RasterInvalidator::Generate
  blink::RasterInvalidator::Generate
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=windows_asan_chrome_no_sandbox&range=572427:572428
Fixed: https://clusterfuzz.com/revisions?job=windows_asan_chrome_no_sandbox&range=575742:575743

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5280137512484864

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2018-07-18)

ClusterFuzz testcase 5280137512484864 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2018-07-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-07-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-07-30)

$3,000 for the bug, and a $500 cluserfuzz bonus.  Thanks!

### aw...@chromium.org (2018-07-30)

[Empty comment from Monorail migration]

### aw...@google.com (2018-08-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-10-24)

This issue was migrated from crbug.com/chromium/862635?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/863158]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091909)*
