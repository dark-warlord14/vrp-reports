# Security: Use-after-free in CPWL_Edit::OnKillFocus()

| Field | Value |
|-------|-------|
| **Issue ID** | [40088870](https://issues.chromium.org/issues/40088870) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | rh...@chromium.org |
| **Created** | 2017-08-30 |
| **Bounty** | $3,000.00 |

## Description

Tested on

Chromium	62.0.3197.0 (Developer Build) (64-bit)
Revision	e5aab5c2b9d9e85ffccbdb3571e9f7d218e95601-refs/heads/master@{#497322}
/w ASAN

It should work on M60 61 as well.

----------------------------------------------------------

relevant report you may want to check: https://bugs.chromium.org/p/chromium/issues/detail?id=737023


https://cs.chromium.org/chromium/src/third_party/pdfium/fpdfsdk/pwl/cpwl_edit.cpp?q=cpwl_edit.cpp:351&sq=package:chromium&l=342

[...]
void CPWL_Edit::OnKillFocus() {
  CPWL_ScrollBar* pScroll = GetVScrollBar();
  if (pScroll && pScroll->IsVisible()) {
    pScroll->SetVisible(false);
    Move(m_rcOldWindow, true, true);
  }

  m_pEdit->SelectNone();
  SetCaret(false, CFX_PointF(), CFX_PointF()); <--- I've managed to run AAction, to destroy the pdfwindow in middle of |SetCaret|. then uaf occurs at the next lines.
  SetCharSet(FX_CHARSET_ANSI);
  m_bFocus = false;
}
[...]

To destroy the pdf window |ResetPDFWindow|, I've been using |setFocus()|
https://cs.chromium.org/chromium/src/third_party/pdfium/fpdfsdk/formfiller/cffl_interactiveformfiller.cpp?type=cs&q=CFFL_InteractiveFormFiller::OnSetFocus&sq=package:chromium&l=399






## Attachments

- deleted (application/octet-stream, 0 B)
- [poc.pdf](attachments/poc.pdf) (application/pdf, 4.0 KB)
- [asan](attachments/asan) (text/plain, 21.2 KB)
- [Screenshot from 2017-08-28 15-54-45.png](attachments/Screenshot from 2017-08-28 15-54-45.png) (image/png, 337.2 KB)
- [poc_2.pdf](attachments/poc_2.pdf) (application/pdf, 4.2 KB)
- [poc_gdb.txt](attachments/poc_gdb.txt) (text/plain, 7.1 KB)

## Timeline

### ma...@gmail.com (2017-08-30)

The following is another PoC, which I spray heap to take over freed object, with arbitrary value.

Tested on Chromium local build on Linux.

### ma...@gmail.com (2017-08-30)

Just clarify it,

|SetCaret| invokes |InvalidateRect| later, which calls |Form_Invalidate| -> |GetVisiblePages| -> |GetPage| (assume: page X) -> |LoadFXAnnots| -> so I run AAction script at here on |OnFormat| of any annot on the page X.

### el...@chromium.org (2017-08-30)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### ds...@chromium.org (2017-08-30)

rharrison@ can you take a look? We probably need to add an ObservedPtr on this in there or something ....

As a note, does this require XFA enabled to trigger?

### ma...@gmail.com (2017-08-30)

No, It doesn't need XFA enabled.

### do...@chromium.org (2017-08-30)

Assigning high severity and impact on stable across desktop.

### sh...@chromium.org (2017-08-31)

[Empty comment from Monorail migration]

### rh...@chromium.org (2017-09-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-06)

[Empty comment from Monorail migration]

### rh...@chromium.org (2017-09-12)

I have looked at this a bit. It is relatively easy to use ObservedPtr to resolve the issue in the specific location that it was reported, but that then causes new locations to appear due to them being masked by the first one.

Getting this nailed down so that all of the underlying locations are caught is going to be non-trivial.

### rh...@chromium.org (2017-09-15)

[Empty comment from Monorail migration]

### ma...@gmail.com (2017-09-15)

[Comment Deleted]

### ma...@gmail.com (2017-09-15)

@rharrison

You may want to take a look at my latest report

https://bugs.chromium.org/p/chromium/issues/detail?id=765384

### bu...@chromium.org (2017-09-15)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/022d13b85408beb400ce703bb5c59736adea208f

commit 022d13b85408beb400ce703bb5c59736adea208f
Author: Ryan Harrison <rharrison@chromium.org>
Date: Fri Sep 15 18:45:55 2017

Add ObservedPtrs to KillFocus path

This is to prevent use after free issues due to these calls causing
reloads of content that have the side of effect of destroying windows.

BUG=chromium:760455

Change-Id: I3f3947be8b32964783abf5577a24ba6a713b3476
Reviewed-on: https://pdfium-review.googlesource.com/14150
Commit-Queue: Ryan Harrison <rharrison@chromium.org>
Reviewed-by: Tom Sepez <tsepez@chromium.org>

[modify] https://crrev.com/022d13b85408beb400ce703bb5c59736adea208f/fpdfsdk/pwl/cpwl_wnd.cpp
[modify] https://crrev.com/022d13b85408beb400ce703bb5c59736adea208f/fpdfsdk/pwl/cpwl_edit.cpp


### rh...@chromium.org (2017-09-15)

Should this be merged anywhere?

### bu...@chromium.org (2017-09-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/517d4150a14d42f32bfc6bcdafce172ab3a47ff4

commit 517d4150a14d42f32bfc6bcdafce172ab3a47ff4
Author: pdfium-deps-roller@chromium.org <pdfium-deps-roller@chromium.org>
Date: Fri Sep 15 21:21:48 2017

Roll src/third_party/pdfium/ 574756152..bb2f7e73b (2 commits)

https://pdfium.googlesource.com/pdfium.git/+log/574756152de8..bb2f7e73bef4

$ git log 574756152..bb2f7e73b --date=short --no-merges --format='%ad %ae %s'
2017-09-15 thestig Simplify a couple of CXFA_Node methods.
2017-09-15 rharrison Add ObservedPtrs to KillFocus path

Created with:
  roll-dep src/third_party/pdfium
BUG=760455


Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, see:
http://www.chromium.org/developers/tree-sheriffs/sheriff-details-chromium#TOC-Failures-due-to-DEPS-rolls


TBR=dsinclair@chromium.org

Change-Id: I5fd7a96a9eaa061fe2efe63434646c9edcb22ecc
Reviewed-on: https://chromium-review.googlesource.com/669307
Reviewed-by: <pdfium-deps-roller@chromium.org>
Commit-Queue: <pdfium-deps-roller@chromium.org>
Cr-Commit-Position: refs/heads/master@{#502381}
[modify] https://crrev.com/517d4150a14d42f32bfc6bcdafce172ab3a47ff4/DEPS


### sh...@chromium.org (2017-09-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-18)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2017-09-18)

+awhalley@ - can you please confirm if this is okay to take for M62?

### aw...@chromium.org (2017-09-18)

abdulsyed@ - yep, good for 62

### ab...@chromium.org (2017-09-18)

Thanks for checking - approving merge to M62. Branch: 3202

### bu...@chromium.org (2017-09-19)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/6f7bd9fdc4f4d7f21e468c47ee3e5616330541a6

commit 6f7bd9fdc4f4d7f21e468c47ee3e5616330541a6
Author: Ryan Harrison <rharrison@chromium.org>
Date: Tue Sep 19 14:36:02 2017

[Merge M62] Add ObservedPtrs to KillFocus path

This is to prevent use after free issues due to these calls causing
reloads of content that have the side of effect of destroying windows.

BUG=chromium:760455

Change-Id: I3f3947be8b32964783abf5577a24ba6a713b3476
Reviewed-on: https://pdfium-review.googlesource.com/14150
Commit-Queue: Ryan Harrison <rharrison@chromium.org>
Reviewed-by: Tom Sepez <tsepez@chromium.org>
(cherry picked from commit 022d13b85408beb400ce703bb5c59736adea208f)
Reviewed-on: https://pdfium-review.googlesource.com/14310
Reviewed-by: dsinclair <dsinclair@chromium.org>

[modify] https://crrev.com/6f7bd9fdc4f4d7f21e468c47ee3e5616330541a6/fpdfsdk/pwl/cpwl_wnd.cpp
[modify] https://crrev.com/6f7bd9fdc4f4d7f21e468c47ee3e5616330541a6/fpdfsdk/pwl/cpwl_edit.cpp


### aw...@chromium.org (2017-09-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-09-22)

Nice one! The panel decided to award $3,000 for this report. Thanks!

### aw...@chromium.org (2017-09-22)

[Empty comment from Monorail migration]

### ma...@gmail.com (2017-09-22)

[Comment Deleted]

### aw...@google.com (2017-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-10-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/760455?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088870)*
