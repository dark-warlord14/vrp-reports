# Security: UAF in  CSSLayout worklet

| Field | Value |
|-------|-------|
| **Issue ID** | [40053129](https://issues.chromium.org/issues/40053129) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Layout |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ra...@gmail.com |
| **Assignee** | ik...@chromium.org |
| **Created** | 2020-08-20 |
| **Bounty** | $5,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/master/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

resolve can call user-defined function.  

when running Layout function or intrinsicSizes function, custom\_layout\_scope->Queue() is poped to take task in iterator.[1][2]  

the task process each algorithm. and its result is sent to resolve.[3][4]  

however, we can modify custom\_layout\_scope->Queue() using layoutNextFragment.  

as a result, the iterator use UAF task.  

[1]: <https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/core/layout/ng/custom/css_layout_definition.cc;drc=1562cab3f1eda927938f8f4a5a91991fefde66d3;l=147>  

[2]: <https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/core/layout/ng/custom/css_layout_definition.cc;drc=1562cab3f1eda927938f8f4a5a91991fefde66d3;l=273>  

[3]:<https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/core/layout/ng/custom/custom_layout_work_task.cc;drc=1562cab3f1eda927938f8f4a5a91991fefde66d3;l=157>  

[4]:<https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/core/layout/ng/custom/custom_layout_work_task.cc;drc=1562cab3f1eda927938f8f4a5a91991fefde66d3;l=140>  

**VERSION**  

Chrome Version: chrome stable, behind Experimental Web Platform features flag  

Operating System: all

**REPRODUCTION CASE**

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: WOOJIN OH

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 1.2 KB)
- [poc.html](attachments/poc.html) (text/plain, 2.2 KB)

## Timeline

### mp...@chromium.org (2020-08-21)

Thanks for the report. ikilpatrick@ can you PTAL?

[Monorail components: Blink>Layout]

### ik...@chromium.org (2020-08-26)

Thanks I'll take a look

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-09-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0a874553eadc802e406f555d3d065a32845fd13f

commit 0a874553eadc802e406f555d3d065a32845fd13f
Author: Ian Kilpatrick <ikilpatrick@chromium.org>
Date: Tue Sep 22 06:12:58 2020

[css-layout-api] Fix using an object which has been reallocated.

Per: crbug.com/1119873

It was possible to mutate the work queue while iterating over it. Using
this it was possible to trigger a UAF.

This patch converts CustomLayoutWorkTask to oilpan (not strictly
required as a copy of the CustomLayoutWorkTask would have also
sufficed), and now copies the Member<CustomLayoutWorkTask> before using
it.

Bug: 1119873
Change-Id: I3c66859af8c9a0f33fe8c7df7c30efd2913c2985
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2380135
Reviewed-by: Alison Maher <almaher@microsoft.com>
Reviewed-by: Matthew Denton <mpdenton@chromium.org>
Commit-Queue: Ian Kilpatrick <ikilpatrick@chromium.org>
Cr-Commit-Position: refs/heads/master@{#809215}

[modify] https://crrev.com/0a874553eadc802e406f555d3d065a32845fd13f/third_party/blink/renderer/core/layout/ng/custom/css_layout_definition.cc
[modify] https://crrev.com/0a874553eadc802e406f555d3d065a32845fd13f/third_party/blink/renderer/core/layout/ng/custom/custom_layout_child.cc
[modify] https://crrev.com/0a874553eadc802e406f555d3d065a32845fd13f/third_party/blink/renderer/core/layout/ng/custom/custom_layout_scope.h
[modify] https://crrev.com/0a874553eadc802e406f555d3d065a32845fd13f/third_party/blink/renderer/core/layout/ng/custom/custom_layout_work_task.cc
[modify] https://crrev.com/0a874553eadc802e406f555d3d065a32845fd13f/third_party/blink/renderer/core/layout/ng/custom/custom_layout_work_task.h


### ra...@gmail.com (2020-10-29)

when is closed? :)

### ik...@chromium.org (2020-10-29)

Apologies - marked as Fixed. Thanks for following up and your patience. Please let us know if you don't believe the issue is fixed, or if there are other issues.

Ian

### ra...@gmail.com (2020-10-29)

this fix seem to be good :)


### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-31)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-11-05)

Congratulations, the VRP panel has awarded $5,000 for this report. Thanks!

### ad...@google.com (2020-11-05)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-02-05)

This issue was migrated from crbug.com/chromium/1119873?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053129)*
