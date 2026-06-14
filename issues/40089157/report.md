# Security: UAF in CPWL_ComboBox::KillFocus

| Field | Value |
|-------|-------|
| **Issue ID** | [40089157](https://issues.chromium.org/issues/40089157) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | hn...@chromium.org |
| **Created** | 2017-09-29 |
| **Bounty** | $5,000.00 |

## Description

VULNERABILITY DETAILS

https://cs.chromium.org/chromium/src/third_party/pdfium/fpdfsdk/pwl/cpwl_combo_box.cpp?type=cssq=package:chromium&l=175

void CPWL_ComboBox::KillFocus() {
  SetPopup(false);
  CPWL_Wnd::KillFocus();
}

----------------------------------------------------------------------

https://cs.chromium.org/chromium/src/third_party/pdfium/fpdfsdk/pwl/cpwl_combo_box.cpp?type=cssq%3Dpackage:chromium&l=380

void CPWL_ComboBox::SetPopup(bool bPopup) {
...
  if (!bPopup) {
    m_bPopup = bPopup;
    Move(m_rcOldWindow, true, true); <------ (1)
    return;
  }



When it's trying to kill focus a combobox, it will invoke |CPWL_ComboBox::KillFocus| instead of |CPWL_Wnd::KillFocus|.

At (1) |Move| ends up calling |Form_Invalidate| which possible to run a script then trigger a UAF by destroying the widget's pdf window in the middle of KillFocus processing. Please see https://crbug.com/chromium/766957 https://crbug.com/chromium/765921 https://crbug.com/chromium/760455 for more explanation/details.

Please find attached PoC/asan/...


VERSION
Chrome Version: 61.0.3163.100 (Official Build) (64-bit)
Operating System: OS X / Win / Linux

REPRODUCTION CASE
Open the pdf file, click on scrollbar which has textbox printing "a".


## Attachments

- [asan](attachments/asan) (text/plain, 22.9 KB)
- [poc.in](attachments/poc.in) (application/octet-stream, 3.5 KB)
- [poc.pdf](attachments/poc.pdf) (application/pdf, 4.3 KB)
- [poc_mv.mov](attachments/poc_mv.mov) (application/octet-stream, 5.5 MB)
- [combox_killfocus.in](attachments/combox_killfocus.in) (application/octet-stream, 3.7 KB)
- [combox_killfocus.pdf](attachments/combox_killfocus.pdf) (application/pdf, 4.5 KB)
- [gdb_btfull](attachments/gdb_btfull) (text/plain, 14.9 KB)
- [Screenshot from 2017-09-29 17-54-08.png](attachments/Screenshot from 2017-09-29 17-54-08.png) (image/png, 367.8 KB)

## Timeline

### ma...@gmail.com (2017-09-29)

This is PoC controlling register [rdx], right at instruction calling function pointer. 

along with backtrace full from gdb.





### in...@chromium.org (2017-09-29)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### th...@chromium.org (2017-09-29)

[Empty comment from Monorail migration]

### ds...@chromium.org (2017-10-02)

[Empty comment from Monorail migration]

### hn...@chromium.org (2017-10-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-10-04)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/55469aed5acffcce3259d37418ba9e8b8e60d801

commit 55469aed5acffcce3259d37418ba9e8b8e60d801
Author: Henrique Nakashima <hnakashima@chromium.org>
Date: Wed Oct 04 16:02:44 2017

Fix UAF in SetVisible().

SetVisible() may be called during Destroy() which may be called
during SetVisible().

This fixes the latest in a family of bugs that happen after an
instance is freed by code triggered by JS code while it's executing
a method.

The CL has a lot of protection for many of these points where JS
may be executed and potentially destroy objects. The return types
of many methods that may execute JS have been changed to bool,
indicating whether the instance is still alive after the call.

Bug: chromium:770148
Change-Id: If5a9db4d8d6aac10f4dd6b645922bb96c116684d
Reviewed-on: https://pdfium-review.googlesource.com/15190
Reviewed-by: dsinclair <dsinclair@chromium.org>
Commit-Queue: Henrique Nakashima <hnakashima@chromium.org>

[modify] https://crrev.com/55469aed5acffcce3259d37418ba9e8b8e60d801/fpdfsdk/pwl/cpwl_combo_box.cpp
[modify] https://crrev.com/55469aed5acffcce3259d37418ba9e8b8e60d801/fpdfsdk/pwl/cpwl_wnd.cpp
[modify] https://crrev.com/55469aed5acffcce3259d37418ba9e8b8e60d801/fpdfsdk/pwl/cpwl_scroll_bar.cpp
[modify] https://crrev.com/55469aed5acffcce3259d37418ba9e8b8e60d801/fpdfsdk/pwl/cpwl_list_box.cpp
[modify] https://crrev.com/55469aed5acffcce3259d37418ba9e8b8e60d801/fpdfsdk/pwl/cpwl_edit.h
[modify] https://crrev.com/55469aed5acffcce3259d37418ba9e8b8e60d801/fpdfsdk/pwl/cpwl_edit_ctrl.h
[modify] https://crrev.com/55469aed5acffcce3259d37418ba9e8b8e60d801/fpdfsdk/pwl/cpwl_caret.h
[modify] https://crrev.com/55469aed5acffcce3259d37418ba9e8b8e60d801/fpdfsdk/pwl/cpwl_edit_ctrl.cpp
[modify] https://crrev.com/55469aed5acffcce3259d37418ba9e8b8e60d801/fpdfsdk/pwl/cpwl_combo_box.h
[modify] https://crrev.com/55469aed5acffcce3259d37418ba9e8b8e60d801/fpdfsdk/pwl/cpwl_wnd.h
[modify] https://crrev.com/55469aed5acffcce3259d37418ba9e8b8e60d801/fpdfsdk/pwl/cpwl_caret.cpp
[modify] https://crrev.com/55469aed5acffcce3259d37418ba9e8b8e60d801/fpdfsdk/pwl/cpwl_edit.cpp
[modify] https://crrev.com/55469aed5acffcce3259d37418ba9e8b8e60d801/fpdfsdk/pwl/cpwl_list_box.h
[modify] https://crrev.com/55469aed5acffcce3259d37418ba9e8b8e60d801/fpdfsdk/pwl/cpwl_scroll_bar.h
[modify] https://crrev.com/55469aed5acffcce3259d37418ba9e8b8e60d801/fpdfsdk/pwl/cpwl_appstream.cpp


### hn...@chromium.org (2017-10-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-05)

[Empty comment from Monorail migration]

### as...@chromium.org (2017-10-09)

[Empty comment from Monorail migration]

### mb...@chromium.org (2017-10-09)

[Empty comment from Monorail migration]

### ma...@gmail.com (2017-10-10)

[Comment Deleted]

### aw...@chromium.org (2017-10-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-10-11)

Nice one! The VRP panel awarded $5,000 for this. Cheers!

### aw...@chromium.org (2017-10-14)

[Empty comment from Monorail migration]

### aw...@google.com (2017-10-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-27)

This bug requires manual review: M63 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), gkihumba@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-10-27)

+awhalley@ (Security TPM) for M63 merge review

### aw...@chromium.org (2017-10-30)

govind@ good for 63 if commit in #6 isn't already there.

### go...@chromium.org (2017-10-30)

#6 is already in M63 branch (M63 was branched on Oct 12th). 

### aw...@google.com (2017-12-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-12-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### is...@google.com (2018-10-05)

This issue was migrated from crbug.com/chromium/770148?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089157)*
