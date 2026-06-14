# Security: UAF in CPWL_Caret::SetCaret

| Field | Value |
|-------|-------|
| **Issue ID** | [40089030](https://issues.chromium.org/issues/40089030) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2017-09-16 |
| **Bounty** | $5,000.00 |

## Description

This bug affects on stable Chrome /w XFA disabled.



https://cs.chromium.org/chromium/src/third_party/pdfium/fpdfsdk/pwl/cpwl_caret.cpp?sq=package:chromium&l=86

---------------------------------------------
void CPWL_Caret::SetCaret(bool bVisible,
                          const CFX_PointF& ptHead,
                          const CFX_PointF& ptFoot) {
  if (bVisible) {
    if (IsVisible()) {
      if (m_ptHead != ptHead || m_ptFoot != ptFoot) {
        m_ptHead = ptHead;
        m_ptFoot = ptFoot;
        m_bFlash = true;
        Move(m_rcInvalid, false, true);
      }
    } else {
      m_ptHead = ptHead;
      m_ptFoot = ptFoot;
      EndTimer();
      BeginTimer(PWL_CARET_FLASHINTERVAL);
      CPWL_Wnd::SetVisible(true); <---------- (1)
      m_bFlash = true;
      Move(m_rcInvalid, false, true);
    }
  } else {
    m_ptHead = CFX_PointF();
    m_ptFoot = CFX_PointF();
    m_bFlash = false;
    if (IsVisible()) {
      EndTimer();
      CPWL_Wnd::SetVisible(false);
    }
  }
}





At (1), |SetEditCaret| calls |SetCaret| -> ... ends up at |Invalidate| which invokes |Form_Invalidate| may call |GetPage| -> |LoadFXAnnots|. Then we can destroy pdf window |this| (CPWL_Edit) in the middle of this function -> UAF occurs.

It's kinda complex to trigger it, but I managed to do that.







## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [asan_noui](attachments/asan_noui) (text/plain, 22.0 KB)
- [onsetfocus_noui.in](attachments/onsetfocus_noui.in) (application/octet-stream, 3.6 KB)
- [onsetfocus_noui.pdf](attachments/onsetfocus_noui.pdf) (application/pdf, 4.4 KB)
- [poc_noui.mov](attachments/poc_noui.mov) (application/octet-stream, 5.0 MB)
- [control_reg.pdf](attachments/control_reg.pdf) (application/pdf, 4.7 KB)
- [control_reg.in](attachments/control_reg.in) (application/octet-stream, 3.9 KB)
- [Screenshot from 2017-09-18 11-59-10.png](attachments/Screenshot from 2017-09-18 11-59-10.png) (image/png, 373.4 KB)
- [poc_gdb](attachments/poc_gdb) (text/plain, 3.4 KB)

## Timeline

### el...@chromium.org (2017-09-16)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### ma...@gmail.com (2017-09-16)

Heyy good news

I've managed to make a PoC without user interaction.

I probably can take control registers, but let me get back my Linux build on Monday.

Cheers.

### me...@chromium.org (2017-09-17)

[Empty comment from Monorail migration]

### ma...@gmail.com (2017-09-18)

You can see that |rdx| is overwritten by arbitrary value, so it's definitely possible to take over RIP as well since it operating |call   QWORD PTR [rdx+0x28]|



### th...@chromium.org (2017-09-18)

[Empty comment from Monorail migration]

### ds...@chromium.org (2017-09-19)

[Empty comment from Monorail migration]

### ds...@chromium.org (2017-09-19)

https://pdfium-review.googlesource.com/c/pdfium/+/14290

### ts...@chromium.org (2017-09-19)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-09-19)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/6f960347f8474a202d8dd99063bf8ce584896baf

commit 6f960347f8474a202d8dd99063bf8ce584896baf
Author: Dan Sinclair <dsinclair@chromium.org>
Date: Tue Sep 19 17:57:30 2017

Setting focus on a widget may destroy the widget

When a widget has focus set, this can trigger an Invalidation call which
can trigger a page and annotation reload. This reload can destroy the
current widget we're handling.

This CL adds ObservedPtrs as needed so we can make sure the widgets are
still alive after we've done the Invalidation.

Bug: chromium:765921
Change-Id: I51cd24aa1ebd96abe9478efef5130a4e568dac1a
Reviewed-on: https://pdfium-review.googlesource.com/14290
Commit-Queue: dsinclair <dsinclair@chromium.org>
Reviewed-by: Tom Sepez <tsepez@chromium.org>

[modify] https://crrev.com/6f960347f8474a202d8dd99063bf8ce584896baf/fpdfsdk/pwl/cpwl_caret.cpp
[modify] https://crrev.com/6f960347f8474a202d8dd99063bf8ce584896baf/fpdfsdk/pwl/cpwl_wnd.cpp
[modify] https://crrev.com/6f960347f8474a202d8dd99063bf8ce584896baf/fpdfsdk/pwl/cpwl_edit.cpp


### ds...@chromium.org (2017-09-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-20)

[Empty comment from Monorail migration]

### as...@chromium.org (2017-09-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-10-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-10-06)

Congrats! The VRP panel decided to award $5,000 for this report. Thank you!

### aw...@chromium.org (2017-10-06)

[Empty comment from Monorail migration]

### aw...@google.com (2017-12-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-12-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### is...@google.com (2018-10-05)

This issue was migrated from crbug.com/chromium/765921?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089030)*
