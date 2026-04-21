# Security: Use of conditionally uninitialised stack variable may leak stack state

| Field | Value |
|-------|-------|
| **Issue ID** | [40054427](https://issues.chromium.org/issues/40054427) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Mac |
| **Reporter** | zh...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2021-01-13 |
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

### zh...@gmail.com (2021-01-13)

[Comment Deleted]

### [Deleted User] (2021-01-13)

[Empty comment from Monorail migration]

### zh...@gmail.com (2021-01-13)

[Comment Deleted]

### xi...@chromium.org (2021-01-13)

Thanks for the report. I think DCHECKs are in place to make sure stack variables are initialized. Tentatively set severity to high. +tsepez,  could you take a look? Thanks!

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2021-01-13)

Agreed.  DCHECKS() are generally useless.  Will put together a simple patch.

### ts...@chromium.org (2021-01-13)

Marking sev-low because there would need to show a way to trigger this path from actual content.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2355c635ab7c530c0191c12d4e191861055d696b

commit 2355c635ab7c530c0191c12d4e191861055d696b
Author: Tom Sepez <tsepez@chromium.org>
Date: Wed Jan 13 23:56:00 2021

Validate return code from FPDF_PageToDevice()

A DCHECK() here isn't sufficient to prevent the use of uninitialized
memory should this someday return false.

Bug: 1166091
Change-Id: I4cfd28653f2e6882f227299d68605be706b75b44
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2628044
Reviewed-by: K. Moon <kmoon@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Cr-Commit-Position: refs/heads/master@{#843247}

[modify] https://crrev.com/2355c635ab7c530c0191c12d4e191861055d696b/pdf/pdfium/pdfium_page.cc


### zh...@gmail.com (2021-01-14)

[Comment Deleted]

### xi...@chromium.org (2021-01-14)

You're right, I think it should be Security_Impact-Stable.

### ts...@chromium.org (2021-01-14)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-15)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-21)

[Empty comment from Monorail migration]

### zh...@gmail.com (2021-01-29)

[Comment Deleted]

### zh...@gmail.com (2021-02-26)

[Comment Deleted]

### am...@google.com (2021-02-26)

Hello, zhouat2017@. Our apologies for the delay on an outcome on this. Since this issue is of low security severity, it has not yet come up in the VRP Panel for decision on reward eligibility. Priority and decision are based on exploitability and security impact so it's taking a little extra time on this one.

There will be an update on this issue when a VRP panel decision has been made on this issue, so no effort is required on your part to check in. Thank you for your patience! 

### am...@google.com (2021-02-26)

I am realizing that I didn't address your CVE question in my four responses, so I wanted to update you about that. CVE assignment occurs when the fix for that bug is released. That will also be updated on each issue, so you will get an update when that occurs. Thank you. 

### ad...@google.com (2021-02-26)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-02)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-09)

[Empty comment from Monorail migration]

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

Hello, zhouat2017@ - the VRP Panel has decided to reward you $500 for this report. 

### am...@google.com (2021-04-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-06-28)

Hello zhouat- we consider attachments/pocs in comments as part of the reports to be an integral part of the report, so I've un-deleted them. Thanks!

### is...@google.com (2021-06-28)

This issue was migrated from crbug.com/chromium/1166091?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054427)*
