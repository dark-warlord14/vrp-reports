# Security: Use of conditionally uninitialised stack variable may leak stack state

| Field | Value |
|-------|-------|
| **Issue ID** | [40054438](https://issues.chromium.org/issues/40054438) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Mac |
| **Reporter** | zh...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2021-01-14 |
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

### zh...@gmail.com (2021-01-14)

In the PDFiumPage::CalculateImages function in pdf/pdfium/pdfium_page.cc, the return value of FPDFPageObj_GetBounds is not validated such that stack variables(left、top、right、bottom) may not be initialised before subsequent use. These values are then returned and may leak into v8 either in the renderer or the plugin engine.

https://chromium.googlesource.com/chromium/src/+/master/pdf/pdfium/pdfium_page.cc#1079

Please note that this was found statically using Semmle, as such i do not have a repro case.

### zh...@gmail.com (2021-01-14)

patch.diff
    FPDF_BOOL ret =
        FPDFPageObj_GetBounds(page_object, &left, &bottom, &right, &top);
 -   DCHECK(ret);
+   if (!ret){
+  return ;
+ }

### [Deleted User] (2021-01-14)

[Empty comment from Monorail migration]

### xi...@chromium.org (2021-01-14)

Thanks for the report. This is similar to https://crbug.com/1166091 and https://crbug.com/1166462. We can probably fix all the DCHECK issue in one fix. tsepez@, could you look at this bug as well? Thanks!

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2021-01-14)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/744e99712643db838f62c638d58604749d958134

commit 744e99712643db838f62c638d58604749d958134
Author: Tom Sepez <tsepez@chromium.org>
Date: Fri Jan 15 01:08:30 2021

Check still more return codes from FPDF_ functions.

There are a few more spots similar to
  https://chromium-review.googlesource.com/c/chromium/src/+/2628044

Either check the return code, or pre-initialize the out parameters
so that uninitialized reads are avoided should false someday be
returned.

-- tidy one multiple-assignment encountered while looking for
   other occurences.

Bug: 1166478,1166462
Change-Id: I2aef090f87aac0cd393e977809c8a24eb8d36de8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2630735
Reviewed-by: K. Moon <kmoon@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Cr-Commit-Position: refs/heads/master@{#843842}

[modify] https://crrev.com/744e99712643db838f62c638d58604749d958134/pdf/pdfium/pdfium_page.cc
[modify] https://crrev.com/744e99712643db838f62c638d58604749d958134/pdf/pdfium/pdfium_engine.cc


### ts...@chromium.org (2021-01-15)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-16)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### zh...@gmail.com (2021-02-01)

[Comment Deleted]

### zh...@gmail.com (2021-02-26)

[Comment Deleted]

### am...@google.com (2021-02-26)

[Comment Deleted]

### am...@google.com (2021-02-26)

Hello, zhouat2017@. Our apologies for the delay on an outcome on this. Since this issue is of low security severity, it has not yet come up in the VRP Panel for decision on reward eligibility. Priority and decision are based on exploitability and security impact so it's taking a little extra time on this one.

Additionally, it seems this one has been marked as a duplicate as one of the other issues you recently reported and about which you inquired: https://crbug.com/1166462 so this is unlikely to result in reward or CVE.

There will be an update on this issue when a VRP panel decision has been made on this issue, so no effort is required on your part to check in. Thank you for your patience! 


### zh...@gmail.com (2021-02-26)

[Comment Deleted]

### am...@google.com (2021-02-26)

hello, zhouat2017@ after reviewing with my colleague they agree with you that fixing the same class of error in multiple cases are individual bugs. 

Also, I am realizing that I didn't address your CVE question in my responses, so I wanted to update you about that. CVE assignment occurs when the fix for that bug is released. That will also be updated on each issue, so you will get an update when that occurs. Thank you. 

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

Hello zhouat2017@ - here's another one! The VRP Panel has decided to award you $500 for this report. 

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

### am...@chromium.org (2021-06-28)

Hello zhouat- we consider attachments/pocs included with reports to be an integral part of the report, so I've un-deleted them. Thanks!

### is...@google.com (2021-06-28)

This issue was migrated from crbug.com/chromium/1166478?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054438)*
