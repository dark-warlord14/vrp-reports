# Security: Use of conditionally uninitialised stack variable may leak stack state

| Field | Value |
|-------|-------|
| **Issue ID** | [40054459](https://issues.chromium.org/issues/40054459) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Mac |
| **Reporter** | zh...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2021-01-15 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36

Steps to reproduce the problem:
1.
2.
3.

What is the expected behavior?

What went wrong?
.

Did this work before? N/A 

Chrome version: 87.0.4280.141  Channel: stable
OS Version: OS X 10.15.7
Flash Version:

## Timeline

### [Deleted User] (2021-01-15)

[Empty comment from Monorail migration]

### zh...@gmail.com (2021-01-15)

In the PDFiumEngine::UpdateFocus function in pdf/pdfium/pdfium_engine.cc, the return value of FORM_GetFocusedAnnot is not validated such that stack variables(last_focused_page_) may not be initialised before subsequent use. These values are then returned and may leak into v8 either in the renderer or the plugin engine.

Though last_focused_page_ is initialization to -1 in the master/pdf/pdfium/pdfium_engine.h#753, but may be reassigned to other values, such as: 
master/pdf/pdfium/pdfium_engine.cc#1257, master/pdf/pdfium/pdfium_engine.cc#4132, master/pdf/pdfium/pdfium_engine.cc#4160 , etc.


https://chromium.googlesource.com/chromium/src/+/master/pdf/pdfium/pdfium_engine.cc#1064

Please note that this was found statically using Semmle, as such i do not have a repro case.



fix:
(1)either:
--- cut ---
    } else if (focus_item_type_ == FocusElementType::kPage) {
+    last_focused_page_ = -1;
      FPDF_ANNOTATION last_focused_annot = nullptr;
      FPDF_BOOL ret = FORM_GetFocusedAnnot(form(), &last_focused_page_,
                                           &last_focused_annot);
      DCHECK(ret);

(2)or
--- cut ---
    } else if (focus_item_type_ == FocusElementType::kPage) {
      FPDF_ANNOTATION last_focused_annot = nullptr;
      FPDF_BOOL ret = FORM_GetFocusedAnnot(form(), &last_focused_page_,
                                           &last_focused_annot);
-     DCHECK(ret);
+     if(!ret){
+           return;
+     }

### xi...@chromium.org (2021-01-15)

Thanks for  the report. This is another similar report of https://crbug.com/1166091. +tsepez, could you take a look? Thanks!

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2021-01-15)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/076f1175481dff3f8c5e9ca93c21cafcd718b3d6

commit 076f1175481dff3f8c5e9ca93c21cafcd718b3d6
Author: Tom Sepez <tsepez@chromium.org>
Date: Fri Jan 15 22:48:42 2021

Check yet another return code from FORM_GetFocusedAnnot()

Bug: 1166972
Change-Id: I258c25573d5900e8dae2d3f26bde5eeb200fd8b1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2633964
Reviewed-by: K. Moon <kmoon@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Cr-Commit-Position: refs/heads/master@{#844268}

[modify] https://crrev.com/076f1175481dff3f8c5e9ca93c21cafcd718b3d6/pdf/pdfium/pdfium_engine.cc


### ts...@chromium.org (2021-01-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-16)

[Empty comment from Monorail migration]

### zh...@gmail.com (2021-02-01)

Hello,

Can anyone tell me when I can get CVE and rewards?
It's been half a month.

### zh...@gmail.com (2021-02-26)

[Comment Deleted]

### am...@google.com (2021-02-26)

Hello, zhouat2017@. Our apologies for the delay on an outcome on this. Since this issue is of low security severity, it has not yet come up in the VRP Panel for decision on reward eligibility. Priority and decision are based on exploitability and security impact so it's taking a little extra time on this one.

I've noticed that this one has been marked as a duplicate of one of the other issues you've inquired about - https://crbug.com/1166091, so this one is unlikely to result in a reward or CVE. 

There will be an update on this issue when a VRP panel decision has been made on this issue, so no effort is required on your part to check in. Thank you for your patience! 

### zh...@gmail.com (2021-02-26)

[Comment Deleted]

### am...@google.com (2021-02-26)

zhouat2017@ - you are correct, my apologies. I did an incorrect association while I was responding to the inquiries on your four issues simultaneously. 
These will be reviewed as separate issues.

### am...@google.com (2021-02-26)

I am realizing that I didn't address your CVE question in my responses, so I wanted to update you about that. CVE assignment occurs when the fix for that bug is released. That will also be updated on each issue, so you will get an update when that occurs. Thank you. 

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-31)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-03-31)

Congratulations, zhouat2017@ - one more! The VRP Panel has decided to award you $500 for this report. Thanks for reporting these issues. 

### am...@google.com (2021-04-02)

[Empty comment from Monorail migration]

### ad...@google.com (2021-04-07)

[Empty comment from Monorail migration]

### ad...@google.com (2021-04-09)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@gmail.com (2021-12-16)

Can someone undelete the pocs and bug details? Thanks.

### is...@google.com (2021-12-16)

This issue was migrated from crbug.com/chromium/1166972?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054459)*
