# Draw the image outside of the inline frame

| Field | Value |
|-------|-------|
| **Issue ID** | [40080274](https://issues.chromium.org/issues/40080274) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Layout |
| **Platforms** | Android |
| **Reporter** | kh...@gmail.com |
| **Assignee** | vo...@chromium.org |
| **Created** | 2014-08-22 |
| **Bounty** | $1,500.00 |

## Description

Steps to reproduce the problem:
1. Open the attached HTML file repro1.html

What is the expected behavior?

What went wrong?

Did this work before? N/A 

Chrome version: 37.0.2062.94  Channel: beta
OS Version: 4.4.2
Flash Version: 

This seems to be the same issue discussed here: [https://crbug.com/chromium/331168]


## Attachments

- [repro2.html](attachments/repro2.html) (text/html, 258 B)
- [repro1.html](attachments/repro1.html) (text/html, 80 B)
- [victim.html](attachments/victim.html) (text/html, 76 B)
- [repro.html](attachments/repro.html) (text/html, 798 B)
- [trace.zip](attachments/trace.zip) (application/zip, 7.4 MB)
- [Screenshot from 2014-08-28 13:45:59.png](attachments/Screenshot from 2014-08-28 13_45_59.png) (image/png, 190.2 KB)

## Timeline

### cl...@chromium.org (2014-08-25)

[Empty comment from Monorail migration]

### kh...@gmail.com (2014-08-26)

[Empty comment from Monorail migration]

### wf...@chromium.org (2014-08-26)

Hi - thank you for your report.  I am unsure what the reproduction step here is, can you describe in more detail the vulnerability you are reporting, and how to verify it locally?  Does this only affect Android?

### kh...@gmail.com (2014-08-26)

Hi. Thanks for your reply. This will work only on Android.

The first attached POC (repro1.html, repro2.html) is the simple repro, the second (repro.html, victim.html) is more effective and fun.

Steps to reproduce:
1. Serve the attached HTML files from a local http server (in my case, Python 3.4's builtin HTTP Server)
2. Go to http://[ADDR]/{repro1,victim}.html
3. Click anywhere on page

Thanks.

### kh...@gmail.com (2014-08-26)

Add to explanation: The second POC is use https://crbug.com/chromium/406559 to hijack the click event.

### cl...@chromium.org (2014-08-28)

[Empty comment from Monorail migration]

### wf...@chromium.org (2014-08-28)

Thanks for the update.  Still trying to replicate this issue.

### wa...@chromium.org (2014-08-28)

Reproduced on Linux with DevTools device emulation enabled. It doesn't need a web server to reproduce.

Modified 102400 to 1024 in the test to easy tracing. Attached a trace containing the frame dumps and a screen shot of trace viewer.

Seems something wrong with composited scrollbars.


### kh...@gmail.com (2014-08-28)

I'm glad you can reproduce it!

### wf...@chromium.org (2014-08-29)

wangxianzhu@ I'm assigning you as owner as you're able to reproduce this.  Can you triage and/or reassign as necessary.

### cl...@chromium.org (2014-08-29)

[Empty comment from Monorail migration]

### wa...@chromium.org (2014-08-29)

vollick@ could you take a look or reassign?

The issue seems that the customized scrollbar layers is not clipped by the scrolling layer.

### cl...@chromium.org (2014-08-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-31)

[Empty comment from Monorail migration]

### wf...@chromium.org (2014-09-02)

[Empty comment from Monorail migration]

### pa...@chromium.org (2014-09-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-06)

vollick@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### vo...@chromium.org (2014-09-08)

[Empty comment from Monorail migration]

### vo...@chromium.org (2014-09-08)

I'm going to be ooo for a week, but I've cc'd Glenn in case he has time to look at this (or delegate it) before I come back.

### bu...@chromium.org (2014-09-16)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=182021

------------------------------------------------------------------
r182021 | vollick@chromium.org | 2014-09-15T23:56:46.631624Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/TestExpectations?r1=182021&r2=182020&pathrev=182021
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/compositing/RenderLayerCompositor.cpp?r1=182021&r2=182020&pathrev=182021

Clip iframe overflow controls.

Clips overflow controls via m_overflowControlsHostLayer.

BUG=406593

Review URL: https://codereview.chromium.org/564983003
-----------------------------------------------------------------

### vo...@chromium.org (2014-09-16)

Above fix is trivial.

Requesting a merge to both M38 and M37

### vo...@chromium.org (2014-09-17)

[Empty comment from Monorail migration]

### ke...@google.com (2014-09-17)

No more 37s.

### bu...@chromium.org (2014-09-18)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=182216

------------------------------------------------------------------
r182216 | vollick@chromium.org | 2014-09-18T03:51:24.186156Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2125/LayoutTests/TestExpectations?r1=182216&r2=182215&pathrev=182216
   M http://src.chromium.org/viewvc/blink/branches/chromium/2125/Source/core/rendering/compositing/RenderLayerCompositor.cpp?r1=182216&r2=182215&pathrev=182216

Merge 182021 "Clip iframe overflow controls."

> Clip iframe overflow controls.
> 
> Clips overflow controls via m_overflowControlsHostLayer.
> 
> BUG=406593
> 
> Review URL: https://codereview.chromium.org/564983003

TBR=vollick@chromium.org

Review URL: https://codereview.chromium.org/579073002
-----------------------------------------------------------------

### vo...@chromium.org (2014-09-18)

[Empty comment from Monorail migration]

### vo...@chromium.org (2014-09-19)

+amineer for 37

### vo...@chromium.org (2014-09-19)

Only P0's for 37. So I'm removing the merge request.

### cl...@chromium.org (2014-09-19)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-10-03)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-10-07)

Congratulations - $1500 for this report ($1000 for the bug + $500 for the high-quality proof of concept).

### kh...@gmail.com (2014-10-08)

Thanks!

### ti...@google.com (2014-12-09)

Payment in progress.

### ti...@google.com (2014-12-09)

[Empty comment from Monorail migration]

### ti...@google.com (2014-12-22)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2014-12-26)

Bulk update: removing view restriction from closed bugs.

### la...@google.com (2015-01-09)

Migrate from Cr-Blink-Rendering to Cr-Blink-Layout

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/406593?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080274)*
