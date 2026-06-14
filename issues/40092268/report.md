# Regression(89733): Use after free in fast/forms/text-control-intrinsic-widths.html

| Field | Value |
|-------|-------|
| **Issue ID** | [40092268](https://issues.chromium.org/issues/40092268) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-06-28 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free invalid read

**VERSION**  

Chrome Version:  

Chromium 14.0.805.0 (Developer Build 90701) Ubuntu 11.04  

WebKit 535.1 (trunk@89816)

not affected: beta and stable

Operating System: linux 64bit

**REPRODUCTION CASE**  

third\_party/WebKit/LayoutTests/fast/forms/text-control-intrinsic-widths.html

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: asan/vg  

Crash State:

Invalid read of size 2  

at 0x178FF10: WebCore::Font::codePath(WebCore::TextRun const&) const (TextRun.h:99)

Address 0x366f4410 is 32 bytes inside a block of size 34 free'd  

at 0x4C29146: free (vg\_replace\_malloc.c:913)  

by 0x1CF9B5F: WebCore::RenderTextControl::getAvgCharWidth(WTF::AtomicString) (StringImplBase.h:34)

## Attachments

- [vg.txt](attachments/vg.txt) (text/plain; charset=us-ascii, 18.0 KB)

## Timeline

### [Deleted User] (2011-06-28)

[Empty comment from Monorail migration]

### [Deleted User] (2011-06-28)

Filed upstream as https://bugs.webkit.org/show_bug.cgi?id=63543

### ma...@google.com (2011-06-28)

Removing security@ from ownership.

### in...@chromium.org (2011-06-28)

I have a fix.

### in...@chromium.org (2011-06-28)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-06-28)

http://trac.webkit.org/changeset/89950

### in...@chromium.org (2011-06-28)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-07-01)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-23)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-24)

Haha! A use-after-free in a stock layout test. Cheeky but fair :)
$1000

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

### sc...@gmail.com (2011-09-23)

Payment in system.

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### bu...@chromium.org (2012-10-13)

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

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

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

This issue was migrated from crbug.com/chromium/87728?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092268)*
