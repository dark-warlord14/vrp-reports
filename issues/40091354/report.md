# Heap-use-after-free in blink::SVGResources::LayoutIfNeeded

| Field | Value |
|-------|-------|
| **Issue ID** | [40091354](https://issues.chromium.org/issues/40091354) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Layout, Blink>SVG |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | fs...@opera.com |
| **Created** | 2018-05-10 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=5192902813417472

Fuzzer: miaubiz_svg_fuzzer
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x611000041bc0
Crash State:
  blink::SVGResources::LayoutIfNeeded
  blink::LayoutSVGRoot::UpdateLayout
  blink::LayoutBlockFlow::PositionAndLayoutOnceIfNeeded
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=556742:556743

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5192902813417472

Issue filed automatically.

See https://github.com/google/clusterfuzz-tools for more information.

## Timeline

### cl...@chromium.org (2018-05-10)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>Layout Blink>SVG]

### cl...@chromium.org (2018-05-10)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/3431b89c8be2d7b1a60f5eb135b1d27ce432ce9b ([CI] Convert SVG resources to use SVGResource).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### cl...@chromium.org (2018-05-10)

ClusterFuzz has detected this issue as fixed in range 557119:557122.

Detailed report: https://clusterfuzz.com/testcase?key=5192902813417472

Fuzzer: miaubiz_svg_fuzzer
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x611000041bc0
Crash State:
  blink::SVGResources::LayoutIfNeeded
  blink::LayoutSVGRoot::UpdateLayout
  blink::LayoutBlockFlow::PositionAndLayoutOnceIfNeeded
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=556742:556743
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=557119:557122

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5192902813417472

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2018-05-10)

ClusterFuzz testcase 5192902813417472 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2018-05-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-06-04)

Nice one miaubiz! $3,500 for this one

### aw...@chromium.org (2018-06-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-08-16)

This issue was migrated from crbug.com/chromium/841705?no_tracker_redirect=1

[Multiple monorail components: Blink>Layout, Blink>SVG]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091354)*
