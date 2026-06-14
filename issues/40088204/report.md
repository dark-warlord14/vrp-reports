# Security: Use-after-free in ResetPDFWindow();

| Field | Value |
|-------|-------|
| **Issue ID** | [40088204](https://issues.chromium.org/issues/40088204) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2017-06-27 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36

Steps to reproduce the problem:
the poc will cause crashes on Chrome and Chromium ASAN as well.

What is the expected behavior?

What went wrong?
At | CFFL_FormFiller::GetPDFWindow | , it invokes |ResetPDFWindow| and get a return as its return value itself as well.

https://cs.chromium.org/chromium/src/third_party/pdfium/fpdfsdk/formfiller/cffl_formfiller.cpp?sq=package:chromium&l=364 

For example, |MyField3| is a TextField box so it is defined at here: https://cs.chromium.org/chromium/src/third_party/pdfium/fpdfsdk/formfiller/cffl_textfield.cpp?sq=package:chromium&l=235

It's trying to make a new |CPWL_Wnd|, destroy the old one at line 240th, then make a new one at 246th line then call |UpdateField| <-- where the problems occur.

|UpdateField| is defined here: https://cs.chromium.org/chromium/src/third_party/pdfium/fpdfsdk/cpdfsdk_interform.cpp?sq=package:chromium&l=324

is responsible for updating fields on various pages. 

It calls |GetWidget| at https://cs.chromium.org/chromium/src/third_party/pdfium/fpdfsdk/cpdfsdk_interform.cpp?sq=package:chromium&l=330

which invokes |GetPageView| at https://cs.chromium.org/chromium/src/third_party/pdfium/fpdfsdk/cpdfsdk_interform.cpp?sq=package:chromium&l=110

|GetPageView| -> |GetPage| -> |Form_GetPage| (pdfium_engine) -> ... which later ends up at |OnLoad| |OnFormat| <-- we can run script here.

So what could we do at this place ?

We run:
  this.getField("MyField3").borderStyle  = "dashed";
  this.getField("MyField3").setFocus();
  gc();

to trigger |GetPDFWindow| , we changed its borderstyle, so Age will change, then calls |ResetPDFWindow| -> |DestroyPDFWindow|... after it's done.  |UpdateField| returns back to |ResetPDFWindow| at 
https://cs.chromium.org/chromium/src/third_party/pdfium/fpdfsdk/formfiller/cffl_textfield.cpp?sq=package:chromium&l=248

but... the PDFWindow has been freed earlier.

UAF occurs.

I would like to use `gc();` to can see the crash on Chrome Mac OSX.

Did this work before? N/A 

Chrome version: 58.0.3029.110  Channel: n/a
OS Version: OS X 10.12.5
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)
- [poc.pdf](attachments/poc.pdf) (application/pdf, 3.6 KB)
- [asan](attachments/asan) (text/plain, 34.1 KB)

## Timeline

### ma...@gmail.com (2017-06-27)

[Comment Deleted]

### ma...@gmail.com (2017-06-27)

[Comment Deleted]

### ma...@gmail.com (2017-06-27)

This bug and the previous ones are found by code review though.

### el...@chromium.org (2017-06-27)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### cl...@chromium.org (2017-06-27)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6198274011955200.

### ds...@chromium.org (2017-06-27)

[Empty comment from Monorail migration]

### th...@chromium.org (2017-06-28)

No UAFs for me on Linux with pdfium_test. Does this require the Chrome PDF Viewer?

### th...@chromium.org (2017-06-28)

But regular Linux builds crash, so let me test with Chromium + ASAN.

### th...@chromium.org (2017-06-28)

I'll add it to my queue. Can someone add the appropriate security flags?

### ma...@gmail.com (2017-06-28)

[Comment Deleted]

### ma...@gmail.com (2017-06-28)

[Comment Deleted]

### ma...@gmail.com (2017-06-28)

[Comment Deleted]

### ma...@gmail.com (2017-07-02)

[Comment Deleted]

### ji...@chromium.org (2017-07-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-07-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-07-12)

thestig: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@gmail.com (2017-07-19)

Hi folks
Any updates ? It's been nearly a month.
Thanks.

### ts...@chromium.org (2017-07-19)

Ah, the assignee has been out for a few weeks. Let me see if I can take a stab at it in the mean time.

### ts...@chromium.org (2017-07-19)

CL at https://pdfium-review.googlesource.com/c/8350

### ts...@chromium.org (2017-07-19)

This is a nice bit of deductive work, by the way.  The CL just hits it with a big hammer for the time being.

### ts...@chromium.org (2017-07-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-07-21)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-07-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-07-31)

[Empty comment from Monorail migration]

### aw...@google.com (2017-07-31)

Congratulations manhluat93.php@! The VRP Panel decided to award $5,000 for this report!  A member of our finance team will be in touch to arrange for payment.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-07-31)

[Empty comment from Monorail migration]

### ma...@gmail.com (2017-08-01)

Thank you for the bounty!

Please credit to "Luật Nguyễn (@l4wio) of KeenLab, Tencent";

Regards.

### sh...@chromium.org (2017-08-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-05)

This bug requires manual review: M61 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), ketakid@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-08-06)

+ awhalley@ (Security TPM) for M61 merge review.

### aw...@chromium.org (2017-08-07)

govind@ - good for 61

### ke...@chromium.org (2017-08-07)

Approving merge to M61 Chrome OS.

### ts...@chromium.org (2017-08-08)

77417ec9e already in chromium/3163 branch.

### go...@chromium.org (2017-08-08)

Removing "Merge-Approved-61" label per https://crbug.com/chromium/737023#c33.

### aw...@google.com (2017-09-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-09-06)

[Empty comment from Monorail migration]

### ts...@chromium.org (2017-09-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### ch...@gmail.com (2018-06-13)

[Comment Deleted]

### is...@google.com (2018-06-13)

This issue was migrated from crbug.com/chromium/737023?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088204)*
