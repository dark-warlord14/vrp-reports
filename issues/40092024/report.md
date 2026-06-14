# Security: Talos Security Advisory for Google PDFium (TALOS-2018-0639)

| Field | Value |
|-------|-------|
| **Issue ID** | [40092024](https://issues.chromium.org/issues/40092024) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | [Deleted User] |
| **Assignee** | ts...@chromium.org |
| **Created** | 2018-07-25 |
| **Bounty** | $2,000.00 |

## Description

### Summary

An exploitable out-of-bounds read on the heap vulnerability exists in the JBIG2 parsing code of Google Chrome version 67.0.3396.99. A specially crafted PDF document can trigger an out-of-bounds read, which can possibly lead to an information leak that could be used as part of an exploit. An attacker needs to trick the user into visiting a malicious site to trigger the vulnerability.### Summary

An exploitable out-of-bounds read on the heap vulnerability exists in the JBIG2 parsing code of Google Chrome version 67.0.3396.99. A specially crafted PDF document can trigger an out-of-bounds read, which can possibly lead to an information leak that could be used as part of an exploit. An attacker needs to trick the user into visiting a malicious site to trigger the vulnerability.

## Attachments

- [Google Vulnerability Report.TALOS 2018 0639.zip](attachments/Google Vulnerability Report.TALOS 2018 0639.zip) (application/octet-stream, 8.4 KB)

## Timeline

### cl...@chromium.org (2018-07-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5804313709117440.

### mb...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### hn...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### th...@chromium.org (2018-07-25)

I can repro with ASAN pdfium_test at ToT.

### cl...@chromium.org (2018-07-25)

Detailed report: https://clusterfuzz.com/testcase?key=5804313709117440

Job Type: linux_asan_pdfium
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x609000014908
Crash State:
  CJBig2_Image::ComposeToOpt2WithRect
  CJBig2_Context::ParseGenericRegion
  CJBig2_Context::ProcessingParseSegmentData
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_pdfium&range=487701:487743

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5804313709117440

See https://github.com/google/clusterfuzz-tools for more information.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.


### sh...@chromium.org (2018-07-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-26)

[Empty comment from Monorail migration]

### ts...@chromium.org (2018-07-31)

CL at https://pdfium-review.googlesource.com/c/pdfium/+/39310 to check the immediate issue at hand,

### bu...@chromium.org (2018-08-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0cb45daf738064de834f2c048e37dafffc700ae3

commit 0cb45daf738064de834f2c048e37dafffc700ae3
Author: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Date: Wed Aug 01 22:37:45 2018

Roll src/third_party/pdfium 2563fc3895f2..0562ff4f6e2e (2 commits)

https://pdfium.googlesource.com/pdfium.git/+log/2563fc3895f2..0562ff4f6e2e


git log 2563fc3895f2..0562ff4f6e2e --date=short --no-merges --format='%ad %ae %s'
2018-08-01 tsepez@chromium.org Bounds check lineSrc in JBig2_Image.cpp.
2018-08-01 rharrison@chromium.org Add in support for using .evt in make_expected.sh


Created with:
  gclient setdep -r src/third_party/pdfium@0562ff4f6e2e

The AutoRoll server is located here: https://pdfium-roll.skia.org

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:867501
TBR=dsinclair@chromium.org

Change-Id: I9e03617e8c2be4be678a25c82fac6bff19e722ae
Reviewed-on: https://chromium-review.googlesource.com/1159241
Reviewed-by: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Commit-Queue: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#579968}
[modify] https://crrev.com/0cb45daf738064de834f2c048e37dafffc700ae3/DEPS


### cl...@chromium.org (2018-08-02)

ClusterFuzz has detected this issue as fixed in range 579967:579969.

Detailed report: https://clusterfuzz.com/testcase?key=5804313709117440

Job Type: linux_asan_pdfium
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x609000014908
Crash State:
  CJBig2_Image::ComposeToOpt2WithRect
  CJBig2_Context::ParseGenericRegion
  CJBig2_Context::ProcessingParseSegmentData
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_pdfium&range=487701:487743
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_pdfium&range=579967:579969

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5804313709117440

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2018-08-02)

ClusterFuzz testcase 5804313709117440 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2018-08-02)

[Empty comment from Monorail migration]

### [Deleted User] (2018-08-02)

Thanks for the update on the issue. Is there a planned public disclosure date?

### ts...@chromium.org (2018-08-02)

Not yet. 

### [Deleted User] (2018-08-03)

As soon as a release date is planned, please let us know. We prefer 1-2 business days notice. Please also send CVE when assigned.  Thank you.

### sh...@chromium.org (2018-08-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-04)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), kariahda@(iOS), cindyb@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-08-04)

+awhalley@ (Security TPM) for M69 merge review

### go...@chromium.org (2018-08-04)

Is this also need a merge to M68?

### aw...@chromium.org (2018-08-06)

69 is fine.

### go...@chromium.org (2018-08-06)

Approving merge to M69 branch 3497 based on https://crbug.com/chromium/867501#c20 and per offline chat with awhalley@. Pls merge ASAP. Thank you.

### ts...@chromium.org (2018-08-07)

[Empty comment from Monorail migration]

### go...@chromium.org (2018-08-07)

[Empty comment from Monorail migration]

### th...@chromium.org (2018-08-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-08-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-08-13)

Thanks for the report regiwils@! The VRP panel decided to award $2,000 for this report. A member of our finance team will be in touch to arrange next steps.  Would you confirm how you'd like to be credited in the release notes?

### [Deleted User] (2018-08-13)

Please mark credit as follows:
Discovered by Aleksandar Nikolic of Cisco Talos.


### aw...@google.com (2018-08-13)

[Empty comment from Monorail migration]

### aw...@google.com (2018-08-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-04)

[Empty comment from Monorail migration]

### [Deleted User] (2018-09-05)

Is there a release date or this issue?

### [Deleted User] (2018-09-05)

*for this issue


### aw...@google.com (2018-09-05)

The automation will open the bug up on Thu Nov 08 2018. We could open it up sooner if you wish, but ideally after September 25th.

### [Deleted User] (2018-09-05)

The issue reaches 90 days on Oct 25 2018. If a timeframe is set after Sept 25th but prior to Oct 25th, that would be good.


### aw...@google.com (2018-09-05)

Sounds good - let's say 1st October. I've set the next action date to then.

### [Deleted User] (2018-09-05)

Confirmed. Thanks for the update.

### aw...@google.com (2018-10-03)

[Empty comment from Monorail migration]

### [Deleted User] (2018-10-03)

Any updates for the public disclosure timeline?

### aw...@google.com (2018-10-03)

It's now public!

### [Deleted User] (2018-10-03)

Thanks for the update. We will prepare for public disclosure on our end.

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/867501?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/873042]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092024)*
