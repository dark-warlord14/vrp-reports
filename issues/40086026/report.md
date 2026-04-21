# Security: Multiple issues in GTK+ file picker / gdk-pixbuf

| Field | Value |
|-------|-------|
| **Issue ID** | [40086026](https://issues.chromium.org/issues/40086026) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Images>Codecs |
| **Platforms** | Linux |
| **Reporter** | ha...@hboeck.de |
| **Assignee** | ts...@google.com |
| **Created** | 2016-11-20 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Chrome on Linux uses the GTK+ library, therefore security issues in GTK+ and its dependencies may affect Chrome.  

The file picker that gets used e.g. for file uploads uses the gdk-pixbuf library to parse images.

All these issues have been reported to the GNOME developers as well.

I have reported two issues back in July that are fixed in the 2.36.0 version. Both are Integer Overflows subsequently leading to invalid memory reads.

I have just discovered a third bug in the ico parser that exposes undefined behavior. I'll paste the full bug reports I reported to gnome below.

The ico bug can be tested most easily: Open any site with a file upload form (e.g. virustotal), look for the sample .ico and click on it. Chrome will immediately crash.

**VERSION**  

Chrome Version: 54.0.2840.100 stable  

Operating System: Linux

**REPRODUCTION CASE**  

I'll attach all sample files plus their asan output.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: File picker  

Crash State: Should be obvious based on asan traces.

---

<https://crbug.com/chromium/1>: Integer overflow in DecodeHeader (bmp)

A BMP image with a large image width can cause an overflow in the  

calculation of State->LineWidth in the function DecodeHeader().

This is the code:  

if (State->Type == 32)  

State->LineWidth = State->Header.width \* 4;  

else if (State->Type == 24)  

State->LineWidth = State->Header.width \* 3;  

[...] (more lines for other bits per pixel sizes)

If State->Header.width \* [whatever] is bigger than 2^32 this will cause  

an overflow, subsequently skipping sanity checks and causing invalid  

memory reads in Oneline32.

I have attached a BMP sample file that will trigger this bug.  

gdk-pixbuf needs to be compiled with address sanitizer to show the bug.  

I'll also attack the address sanitizer error message.

Also attached is a proposed patch to fix the issue. I have unified the  

if-block for all cases where the bits per pixel are one byte or more,  

introduce a temporary variable bytesPerPixel and will do an overflow  

check. If that fails an error is returned.

Upstream commit:  

<https://git.gnome.org/browse/gdk-pixbuf/commit/gdk-pixbuf/io-bmp.c?id=779429ce34e439c01d257444fe9d6739e72a2024>

---

<https://crbug.com/chromium/2>: Integer overflow in DecodeColormap (bmp)

I want to report a potential security issue in gdk-pixbuf. It's an  

integer overflow in the function DecodeColormap leading to a large  

number of invalid memory reads.

The attached bmp image will trigger this bug. Just clicking on it in a  

gtk file open dialog may lead to a crash.

Here's the problematic code:  

if (State->BufferSize < State->Header.n\_colors \* samples) {

If n\_colors is set to a very large value then State->Header.n\_colors \*  

samples can become larger than 2^32, thus leading to an integer  

overflow. In this case this check will be false. However later down  

there is a loop iterating State->Header.n\_colors times, which will then  

lead to invalid memory reads.

I have attached a bmp image triggering the bug and a proposed patch  

that checks the overflow and also sets a correct error. (This is  

strictly speaking another bug - if DecodeColormap fails there is  

currently no error set and it will lead to a warning.)

<https://git.gnome.org/browse/gdk-pixbuf/commit/?id=b69009f2a2de151103ed87e9594615ba0fe72daf>

---

<https://crbug.com/chromium/3>: Integer Overflow in DecodeHeader (ico)

I have discovered an interesting bug in gdk-pixbuf that shows some of  

the weird behaviors that can happen with undefined C.

The bug is this line:  

State->HeaderSize = entry->DIBoffset + 40;

entry->DIBoffset is a signed integer. If it's an insane large number  

close to INT\_MAX then the addition can overflow.  

Looking at the code one might assume this shouldn't matter, because  

right after that there's a check if State->HeaderSize is smaller than  

zero. However when compiling gdk-pixbuf with address sanitizer this  

check is bypassed and an invalid memory read happens later on.

An Integer Overflow is undefined behavior in C, therefore what the  

compiler does here is legal.

Whether this bug appears seems to depend on the compiler switches used,  

but I've seen it both with an address sanitizer compile with clang and  

with my local installation resulting in a crash (that is gcc based).

## Attachments

- [gdk-pixbuf-crashers-and-asan-errors.zip](attachments/gdk-pixbuf-crashers-and-asan-errors.zip) (application/octet-stream, 4.6 KB)

## Timeline

### me...@chromium.org (2016-11-21)

hanno@hboeck.de: Thanks for the detailed report.

thestig: CC'ing you based on your response https://crbug.com/chromium/495327.

[Monorail components: UI]

### sh...@chromium.org (2016-11-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-26)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-13)

[Empty comment from Monorail migration]

### mb...@chromium.org (2017-02-22)

Hanno, has there been any progress on the third issue upstream?

### sh...@chromium.org (2017-03-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-07-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### ha...@hboeck.de (2019-03-06)

FYI all of these bugs have been fixed in gdk-pixbuf long ago.

https://bugzilla.gnome.org/show_bug.cgi?id=768688
https://bugzilla.gnome.org/show_bug.cgi?id=768738
https://bugzilla.gnome.org/show_bug.cgi?id=776040

You can unrestrict this and consider it as resolved upstream.

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-16)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### ch...@chromium.org (2022-05-27)

[Empty comment from Monorail migration]

[Monorail components: -UI Security]

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-04)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-11)

This issue was migrated from crbug.com/chromium/667106?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### ts...@google.com (2024-10-31)

Closing per c25. Please re-open if this is still an issue.

### sp...@google.com (2024-11-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
thank you for your report that resulted in upstream changes for inclusion in Chrome


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-11-20)

Thank you for the report. Sorry this issue fell through the cracks for some time. Hopefully you will accept this token of our gratitude for reporting it to us, as we do appreciate your efforts.

### pe...@google.com (2025-02-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> thank you for your report that resulted in upstream changes for inclusion in Chrome

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086026)*
