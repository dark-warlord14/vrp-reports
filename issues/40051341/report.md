# PDF-reader tab-crash with editable crash address.

| Field | Value |
|-------|-------|
| **Issue ID** | [40051341](https://issues.chromium.org/issues/40051341) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Internals>Plugins>PDF |
| **Reporter** | at...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-11-16 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**

In the attached PDF-file editing the line with content 1 1 1 will control the crash address following way.

1 1 1 -> chrome: segfault at 3e8000003e8 ip 00007f76f9ae1762 sp 00007fff30e459f8 error 4 in libpdf.so

1 2 1 -> chrome: segfault at 7d0000003e8 ip 00007f76f9ae1762 sp 00007fff30e459f8 error 4 in libpdf.so

2 1 1 -> chrome: segfault at 3e8000007d0 ip 00007f76f9ae1762 sp 00007fff30e459f8 error 4 in libpdf.so

So the most left 1 changes the low-bits and second 1 changes high-bits. Last 1 doesn't change the crash address but changing it into 0 will cause trap divide error because of division by zero.

12 0 obj  

<</FontBBox []  

/Widths [  

0 ...  

0 0 0 0 0 0 0 0 0 0

1 1 1 <--

0 0 0 0 0 0 0 0  

]  

/FontMatrix [  

]  

/FirstChar 22  

/Subtype /Type3  

/Type /Font

endobj

**VERSION**

Google Chrome 17.0.938.0 (Official Build 109848) dev  

16.0.912.41 (Official Build 110024) beta  

Operating System: Address change verified on Ubuntu 11.04 x64 crash also occurs on Windows 7 SP1 x64

## Attachments

- [reduced_min.pdf](attachments/reduced_min.pdf) (application/pdf; charset=iso-8859-1, 1.0 KB)

## Timeline

### sc...@gmail.com (2011-11-16)

Thanks! I fix PDF bugs, I'm excited to take a look!

### at...@gmail.com (2011-11-16)

Also reproducible in Ubuntu x64 Stable Chrome version: 15.0.874.120 (Official Build 108895)

### at...@gmail.com (2011-11-16)

It seems that you can even use decimal numbers to get more precise control for the address.

1.1   1 1 -> segfault at 3e80000044c
1.11  1 1 -> segfault at 3e800000456
1.111 1 1 -> segfault at 3e800000457

### [Deleted User] (2011-11-16)

[Empty comment from Monorail migration]

### [Deleted User] (2011-11-16)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-11-17)

This is actually a buffer overflow within a heap object, so definitely SecSeverity-High.
Thanks very much for the report. I've fixed the issue and will merge the fix into Chrome 16.

Fixed in PDF r1167

With what name would you like to be credited in our release notes?

### at...@gmail.com (2011-11-17)

That was quick. And I thought I would have time to check this with Valgrind after few hours of sleep. :) About the name... I think that the right format would be, Atte Kettunen of OUSPG

### sc...@gmail.com (2011-11-17)

Merged to M16 branch at PDF r1169

### sc...@gmail.com (2011-11-18)

@attekett: thanks for a great bug! The PDF component is believed to be pretty robust, so I'm impressed. This is clearly worth a $1000 Chromium Security Reward.

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### at...@gmail.com (2011-11-18)

Thanks. :) This was the most interesting issue I have found this far. PDF-files are bit harder to reduce and handle than normal html and js I have worked with before.

### sc...@gmail.com (2011-12-20)

Payment in system.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### sc...@gmail.com (2012-07-09)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-08-06)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-08-16)

Increasing reward by $1000 to $2000 as per http://blog.chromium.org/2012/08/chromium-vulnerability-rewards-program.html

### sc...@gmail.com (2012-09-12)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-14)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/104529?no_tracker_redirect=1

[Multiple monorail components: Blink, Internals>Plugins>PDF]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051341)*
