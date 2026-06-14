# Heap-use-after-free in blink::LargeTextFirst

| Field | Value |
|-------|-------|
| **Issue ID** | [40095490](https://issues.chromium.org/issues/40095490) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Paint |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ma...@chromium.org |
| **Created** | 2019-06-24 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=5183421999087616

Fuzzer: miaubiz_svg_fuzzer
Job Type: linux_asan_chrome_v8_arm
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0xf399e398
Crash State:
  blink::LargeTextFirst
  blink::TextPaintTimingDetector::RecordAggregatedText
  blink::ScopedPaintTimingDetectorBlockPaintHook::~ScopedPaintTimingDetectorBlockP
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_v8_arm&range=670082:670083

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5183421999087616

Issue filed automatically.

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

## Timeline

### cl...@chromium.org (2019-06-24)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/92b0ccff3b4bd00c60e5276b3e865a918db94b37 ([content] Ensure that file:// URL can be opened without BEST_EFFORT tasks.).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### cl...@chromium.org (2019-06-24)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>Paint]

### sh...@chromium.org (2019-06-24)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-06-24)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-06-24)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sc...@chromium.org (2019-06-24)

Seems like a metrics issue. Assigning to someone who might know what's going on (the suggested owner doesn't seem right). I can't see the bug on clusterfuzz.

[Monorail components: -Blink>Paint Speed>Metrics]

### ma...@chromium.org (2019-06-24)

This is caused by https://chromium-review.googlesource.com/c/chromium/src/+/1649467. We are working on a fix -  https://chromium-review.googlesource.com/c/chromium/src/+/1672113.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-06-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fbbdff52a8153168e3ad5a23f7b4462a8473f934

commit fbbdff52a8153168e3ad5a23f7b4462a8473f934
Author: Liquan(Max) Gu <maxlg@chromium.org>
Date: Tue Jun 25 03:17:18 2019

[LCP] Text: wrap largest text paint in a class

Currently, we are using flags (is_reporting_lcp_) to stop the
largest-text-paint pipeline in TextPaintTimingDetector. However,
the flag is hard to maintain and is error-prone. To fix this issue,
we introduce a wrapper for the largest-text-paint part of code.
Once we stop largest-text-paint, we set the wrapper instance to null.
This way, any data structure and functions of this pipeline would no
longer be accessible.

In this patch, we also remove the timer. The removal is included in
this patch because it's part of the largest-text-paint pipeline.
Although the removal is a relatively separate part, we suggest
including it here because making it two steps would complicate the
middle state.

The removal of timer has several benefits:
1) can avoid the complicated control logic of timer.
2) can make the metric result more precise, because we move the result
update from the 1s-timer callback to the swap-time assignment callback.

Bug:977181,977926,977952

Change-Id: I01821517ee9a01c70ad65dd901b0f3d687bbb1de
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1672113
Commit-Queue: Liquan (Max) Gu <maxlg@chromium.org>
Reviewed-by: Liquan (Max) Gu <maxlg@chromium.org>
Reviewed-by: Nicolás Peña Moreno <npm@chromium.org>
Reviewed-by: Xianzhu Wang <wangxianzhu@chromium.org>
Cr-Commit-Position: refs/heads/master@{#671941}

[modify] https://crrev.com/fbbdff52a8153168e3ad5a23f7b4462a8473f934/third_party/blink/renderer/core/paint/largest_contentful_paint_calculator_test.cc
[modify] https://crrev.com/fbbdff52a8153168e3ad5a23f7b4462a8473f934/third_party/blink/renderer/core/paint/paint_timing_detector.cc
[modify] https://crrev.com/fbbdff52a8153168e3ad5a23f7b4462a8473f934/third_party/blink/renderer/core/paint/text_element_timing.cc
[modify] https://crrev.com/fbbdff52a8153168e3ad5a23f7b4462a8473f934/third_party/blink/renderer/core/paint/text_element_timing.h
[modify] https://crrev.com/fbbdff52a8153168e3ad5a23f7b4462a8473f934/third_party/blink/renderer/core/paint/text_paint_timing_detector.cc
[modify] https://crrev.com/fbbdff52a8153168e3ad5a23f7b4462a8473f934/third_party/blink/renderer/core/paint/text_paint_timing_detector.h
[modify] https://crrev.com/fbbdff52a8153168e3ad5a23f7b4462a8473f934/third_party/blink/renderer/core/paint/text_paint_timing_detector_test.cc


### ma...@chromium.org (2019-06-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-07-02)

ClusterFuzz testcase 5183421999087616 is still reproducing on tip-of-tree build (trunk).

Please re-test your fix against this testcase and if the fix was incorrect or incomplete, please re-open the bug. Otherwise, ignore this notification and add ClusterFuzz-Wrong label.

### ma...@chromium.org (2019-07-02)

[Empty comment from Monorail migration]

### ma...@chromium.org (2019-07-02)

[Empty comment from Monorail migration]

### ma...@chromium.org (2019-07-02)

[Empty comment from Monorail migration]

### ma...@chromium.org (2019-07-03)

Tested locally. Cannot reproduced. This is the logs:

New crash type: 
New crash state:
  

Original crash type: Heap-use-after-free READ 8
Original crash state:
  blink::LargeTextFirst
  blink::TextRecordsManager::RecordVisibleObject
  blink::TextPaintTimingDetector::RecordAggregatedText

The stacktrace doesn't match the original stacktrace.
Try again (3 times). Press Ctrl+C to stop trying to reproduce.

### na...@google.com (2019-07-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-07-17)

Congrats! The Panel decided to reward $3,500 for this report!

### na...@google.com (2019-07-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ac...@chromium.org (2020-02-19)

[Empty comment from Monorail migration]

[Monorail components: -Speed>Metrics Blink>Paint]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/977926?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095490)*
