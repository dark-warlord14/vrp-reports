# Security: UAF in CFFL_InteractiveFormFiller::OnBeforeKeyStroke

| Field | Value |
|-------|-------|
| **Issue ID** | [40089008](https://issues.chromium.org/issues/40089008) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2017-09-14 |
| **Bounty** | $3,000.00 |

## Description

Notice: this PoC works on stable chrome (XFA disabled)

To repro, open pdf file on Chromium ASAN then click anywhere on page 0.

It even crash on Stable Chrome (MacOS) since I'm using gc();



https://cs.chromium.org/chromium/src/third_party/pdfium/fpdfsdk/formfiller/cffl_interactiveformfiller.cpp?q=CFFL_InteractiveFormFiller::OnBeforeKeyStroke&sq=package:chromium&l=909

std::pair<bool, bool> CFFL_InteractiveFormFiller::OnBeforeKeyStroke(

[...]

  CPDFSDK_Annot::ObservedPtr pObserved(pData->pWidget);
  if (!pData->pWidget->OnAAction(CPDF_AAction::KeyStroke, fa,
                                 pData->pPageView)) { <---- run JS script here
    if (!IsValidAnnot(pData->pPageView, pData->pWidget))
      bExit = true;
    return {bRC, bExit};
  }

  if (!pObserved || !IsValidAnnot(pData->pPageView, pData->pWidget))
    return {bRC, true};

  if (nAge != pData->pWidget->GetAppearanceAge()) {
    CPWL_Wnd* pWnd = pFormFiller->ResetPDFWindow(
        pData->pPageView, nValueAge == pData->pWidget->GetValueAge());
    pData = reinterpret_cast<CFFL_PrivateData*>(pWnd->GetAttachedData());
    bExit = true;
  }

[...]



Root cause:

We can run JS script at 909th line, we can destroy this widget's pdf window,
later it uses |pData| (which is element in PDFWindow class |CPWL_Listbox|)

UAF occurs.

To destroy pdf window:

I killfocus on this annot, then setfocus again (with m_Age has been changed), it will invoke |ResetPDFWindow| afterwards.



                                                    


## Attachments

- [asan](attachments/asan) (text/plain, 10.6 KB)
- deleted (application/octet-stream, 0 B)
- [onbeforekeystroke.pdf](attachments/onbeforekeystroke.pdf) (application/pdf, 2.5 KB)
- [poc.mov](attachments/poc.mov) (application/octet-stream, 16.4 MB)

## Timeline

### ma...@gmail.com (2017-09-14)

Do we have some way to record properly a chrome window ?

Cause I see some PoC attaching .mp4 video with high quality.

Thanks.



### me...@chromium.org (2017-09-14)

Thanks for the report, I can reproduce the crash. Chrome doesn't have a builtin way of recording windows, but your PoC video is very clear. 

Tom: Can you please take a look? Thanks.
 

[Monorail components: Internals>Plugins>PDF]

### me...@chromium.org (2017-09-14)

[Empty comment from Monorail migration]

### ts...@chromium.org (2017-09-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-15)

[Empty comment from Monorail migration]

### ts...@chromium.org (2017-09-15)

[Empty comment from Monorail migration]

### ts...@chromium.org (2017-09-15)

https://pdfium-review.googlesource.com/c/pdfium/+/14050

### sh...@chromium.org (2017-09-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-18)

This bug requires manual review: M62 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2017-09-18)

+awhalley@

I'm approving merge to M62. Branch:3202

### aw...@chromium.org (2017-09-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-09-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-09-22)

Nice one! The VRP panel decided to award $3,000 for this report!

### aw...@chromium.org (2017-09-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-22)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-09-25)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2017-09-29)

Reminder to please merge to M62 branch 3202.

### th...@chromium.org (2017-09-29)

Will merge.

### th...@chromium.org (2017-09-29)

https://pdfium.googlesource.com/pdfium/+/effa1b15ae2ab34ae15892787d5c1caa015bd2d4

### aw...@google.com (2017-10-16)

[Empty comment from Monorail migration]

### aw...@google.com (2017-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-10-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2018-01-04)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/df0a749452d933e4f434e2a33112667f1880db34

commit df0a749452d933e4f434e2a33112667f1880db34
Author: Dan Sinclair <dsinclair@chromium.org>
Date: Thu Jan 04 20:19:21 2018

Remove allocations from JS test

This CL removes the millions of allocations from the test case for bug
765384. This takes the test execution from ~20s to ~400ms when run in
Debug.

Bug: chromium:765384
Change-Id: Ib1e9d3c6fb9853e541189e1a16f765d05202cdcc
Reviewed-on: https://pdfium-review.googlesource.com/22011
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: dsinclair <dsinclair@chromium.org>

[modify] https://crrev.com/df0a749452d933e4f434e2a33112667f1880db34/testing/resources/bug_765384.in
[modify] https://crrev.com/df0a749452d933e4f434e2a33112667f1880db34/testing/resources/bug_765384.pdf


### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/765384?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089008)*
