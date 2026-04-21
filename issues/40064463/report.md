# Security: PDFium (XFA) Use-after-free in CPWL_ComboBox::OnChar

| Field | Value |
|-------|-------|
| **Issue ID** | [40064463](https://issues.chromium.org/issues/40064463) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2023-05-09 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**  

Use-after-free in function CPWL\_ComboBox::OnChar

**VERSION**  

Chrome Version: Version 114.0.5733.0 (Developer Build) (64-bit)  

Operating System: Windows 11

**REPRODUCTION CASE**

1. Enable XFA in chrome://flags
2. open file poc.pdf
3. click to ComboBox on the first page and press `Space` key

DETAIL INFORMATION  

In function `CPWL_ComboBox::OnChar`

```
bool CPWL_ComboBox::OnChar(uint16_t nChar, Mask<FWL_EVENTFLAG> nFlag) {  
  if (!m_pList)  
    return false;  
  
  if (!m_pEdit)  
    return false;  
  
  // In a combo box if the ENTER/SPACE key is pressed, show the combo box  
  // options.  
  switch (nChar) {  
    case pdfium::ascii::kReturn:  
      SetPopup(!IsPopup());  
      SetSelectText();  
      return true;  
    case pdfium::ascii::kSpace:  
      // Show the combo box options with space only if the combo box is not  
      // editable  
      if (!HasFlag(PCBS_ALLOWCUSTOMTEXT)) {  
        if (!IsPopup()) {  
          SetPopup(/\*bPopUp=\*/true);  
          SetSelectText();  
        }  
        return true;  
      }  
      break;  
    default:  
      break;  
...  
}  

```

We can setup to run JS callback by calling to function `SetPopup`. In JS function, we can free `CPWL_ComboBox` object and it is used again when back to function `CPWL_ComboBox::OnChar`.  

We can see that application crash in function `SetSelectText`, when it tries to get a field inside freed `CPWL_ComboBox` object.

BISECT  

The vulnerable code was added in this commit: <https://pdfium-review.googlesource.com/c/pdfium/+/68614>  

It tried to add enter/space key press events on ComboBox but forgot that function `SetPopup` need to check returned value to avoid UAF.

PATCH  

Should add a check returned value after calling function `SetPopup`, like in function `CPWL_ComboBox::KillFocus()`:

```
void CPWL_ComboBox::KillFocus() {  
  if (!SetPopup(false))  
    return;  
  
  CPWL_Wnd::KillFocus();  
}  

```

CRASH INFORMATION

(794c.74e0): Access violation - code c0000005 (first chance)  

First chance exceptions are reported before any exception handling.  

This exception may be expected and handled.  

\*\*\* WARNING: Unable to verify checksum for D:\build-chrome\chromium\_25\_04\_23\src\out\xfa\_64bit\pdfium.dll  

pdfium!fxcrt::UnownedPtr<CPWL\_Edit>::operator->+0x9:  

00007ffa`b3548ef9 488b00 mov rax,qword ptr [rax] ds:0000012d`c8c86fc8=????????????????  

\*\*\* WARNING: Unable to verify checksum for D:\build-chrome\chromium\_25\_04\_23\src\out\xfa\_64bit\chrome.dll  

\*\*\* WARNING: Unable to verify checksum for D:\build-chrome\chromium\_25\_04\_23\src\out\xfa\_64bit\blink\_core.dll  

7:199> kp

# Child-SP RetAddr Call Site

00 00000010`959fbe00 00007ffa`b354b2ae pdfium!fxcrt::UnownedPtr<CPWL\_Edit>::operator->(void)+0x9 [D:\build-chrome\chromium\_25\_04\_23\src\third\_party\pdfium\core\fxcrt\unowned\_ptr.h @ 157]  

01 00000010`959fbe10 00007ffa`b354b468 pdfium!CPWL\_ComboBox::SetSelectText(void)+0x2e [D:\build-chrome\chromium\_25\_04\_23\src\third\_party\pdfium\fpdfsdk\pwl\cpwl\_combo\_box.cpp @ 453]  

02 00000010`959fbe60 00007ffa`b2f83214 pdfium!CPWL\_ComboBox::OnChar(unsigned short nChar = 0x20, class fxcrt::Mask<FWL\_EVENTFLAG> nFlag = class fxcrt::Mask<FWL\_EVENTFLAG>)+0x108 [D:\build-chrome\chromium\_25\_04\_23\src\third\_party\pdfium\fpdfsdk\pwl\cpwl\_combo\_box.cpp @ 408]  

03 00000010`959fbee0 00007ffa`b2f7ff28 pdfium!CFFL\_FormField::OnChar(class CPDFSDK\_Widget \* pWidget = 0x0000012c`eadebfa0, unsigned int nChar = 0x20, class fxcrt::Mask<FWL_EVENTFLAG> nFlags = class fxcrt::Mask<FWL_EVENTFLAG>)+0xa4 [D:\build-chrome\chromium_25_04_23\src\third_party\pdfium\fpdfsdk\formfiller\cffl_formfield.cpp @ 179] 04 00000010`959fbf50 00007ffa`b2f898ed pdfium!CFFL_ComboBox::OnChar(class CPDFSDK_Widget \* pWidget = 0x0000012c`eadebfa0, unsigned int nChar = 0x20, class fxcrt::Mask<FWL\_EVENTFLAG> nFlags = class fxcrt::Mask<FWL\_EVENTFLAG>)+0x48 [D:\build-chrome\chromium\_25\_04\_23\src\third\_party\pdfium\fpdfsdk\formfiller\cffl\_combobox.cpp @ 64]  

05 00000010`959fbfb0 00007ffa`b2f2976e pdfium!CFFL\_InteractiveFormFiller::OnChar(class CPDFSDK\_Widget \* pWidget = 0x0000012c`eadebfa0, unsigned int nChar = 0x20, class fxcrt::Mask<FWL_EVENTFLAG> nFlags = class fxcrt::Mask<FWL_EVENTFLAG>)+0x9d [D:\build-chrome\chromium_25_04_23\src\third_party\pdfium\fpdfsdk\formfiller\cffl_interactiveformfiller.cpp @ 349] 06 00000010`959fc020 00007ffa`b2edb0be pdfium!CPDFSDK_Widget::OnChar(unsigned int nChar = 0x20, class fxcrt::Mask<FWL_EVENTFLAG> nFlags = class fxcrt::Mask<FWL_EVENTFLAG>)+0x6e [D:\build-chrome\chromium_25_04_23\src\third_party\pdfium\fpdfsdk\cpdfsdk_widget.cpp @ 820] 07 00000010`959fc080 00007ffa`b2f1ef8b pdfium!CPDFSDK_Annot::OnChar(class fxcrt::ObservedPtr<CPDFSDK_Annot> \* pAnnot = 0x00000010`959fc118, unsigned int nChar = 0x20, class fxcrt::Mask<FWL\_EVENTFLAG> nFlags = class fxcrt::Mask<FWL\_EVENTFLAG>)+0x4e [D:\build-chrome\chromium\_25\_04\_23\src\third\_party\pdfium\fpdfsdk\cpdfsdk\_annot.cpp @ 93]  

08 00000010`959fc0d0 00007ffa`b2f577d7 pdfium!CPDFSDK\_PageView::OnChar(unsigned int nChar = 0x20, class fxcrt::Mask<FWL\_EVENTFLAG> nFlags = class fxcrt::Mask<FWL\_EVENTFLAG>)+0x8b [D:\build-chrome\chromium\_25\_04\_23\src\third\_party\pdfium\fpdfsdk\cpdfsdk\_pageview.cpp @ 493]  

09 00000010`959fc140 00007ffa`dfb72969 pdfium!FORM\_OnChar(struct fpdf\_form\_handle\_t\_\_ \* hHandle = 0x0000012c`e291af60, struct fpdf_page_t__ \* page = 0x0000012d`377fcfd0, int nChar = 0n32, int modifier = 0n0)+0x87 [D:\build-chrome\chromium\_25\_04\_23\src\third\_party\pdfium\fpdfsdk\fpdf\_formfill.cpp @ 503]  

0a 00000010`959fc1b0 00007ffa`dfb71781 chrome!chrome\_pdf::PDFiumEngine::OnChar(class blink::WebKeyboardEvent \* \*\*\* WARNING: Unable to verify checksum for D:\build-chrome\chromium\_25\_04\_23\src\out\xfa\_64bit\blink\_common.dll  

event = 0x0000012c`e152ef90)+0xa9 [D:\build-chrome\chromium_25_04_23\src\pdf\pdfium\pdfium_engine.cc @ 1744] 0b 00000010`959fc210 00007ffa`e41ef4ec chrome!chrome_pdf::PDFiumEngine::HandleInputEvent(class blink::WebInputEvent \* event = 0x0000012c`e152ef90)+0x191 [D:\build-chrome\chromium\_25\_04\_23\src\pdf\pdfium\pdfium\_engine.cc @ 967]  

0c 00000010`959fc310 00007ffa`e41ef61b chrome!chrome\_pdf::PdfViewWebPlugin::HandleWebInputEvent(class blink::WebInputEvent \* event = 0x0000012c`e152ef90)+0x17c [D:\build-chrome\chromium_25_04_23\src\pdf\pdf_view_web_plugin.cc @ 2018] 0d 00000010`959fc3c0 00007ffa`c25036a8 chrome!chrome_pdf::PdfViewWebPlugin::HandleInputEvent(class blink::WebCoalescedInputEvent \* event = 0x00000010`959fc510, class ui::Cursor \* cursor = 0x00000010`959fc590)+0x5b [D:\build-chrome\chromium\_25\_04\_23\src\pdf\pdf\_view\_web\_plugin.cc @ 545]

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 3.6 KB)

## Timeline

### [Deleted User] (2023-05-09)

[Empty comment from Monorail migration]

### me...@chromium.org (2023-05-10)

Thanks for the report. I can repro on M112 Linux without having to press the space bar: Simply clicking the combo box triggers the UAF.

tsepez, could you PTAL? Thanks. (Added labels assuming XFA is enabled on stable, but please adjust them if that's not the case)

[Monorail components: Internals>Plugins>PDF]

### [Deleted User] (2023-05-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-10)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ts...@chromium.org (2023-05-10)

CL at https://pdfium-review.googlesource.com/c/pdfium/+/107390

### gi...@appspot.gserviceaccount.com (2023-05-11)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/3eb3c4d77d4f9372f77aa4895b85a1d4e4755c89

commit 3eb3c4d77d4f9372f77aa4895b85a1d4e4755c89
Author: Tom Sepez <tsepez@chromium.org>
Date: Thu May 11 19:48:37 2023

Always check return code from CPWL_ComboBox::SetPopup().

Operation must not continue when false is returned.

Bug: chromium:1444238
Change-Id: Ic8c29653ac185ac80b6248203649ce05d0e10f06
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/107390
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>

[add] https://pdfium.googlesource.com/pdfium/+/3eb3c4d77d4f9372f77aa4895b85a1d4e4755c89/testing/resources/javascript/xfa_specific/bug_1444238.evt
[modify] https://pdfium.googlesource.com/pdfium/+/3eb3c4d77d4f9372f77aa4895b85a1d4e4755c89/fpdfsdk/pwl/cpwl_combo_box.h
[add] https://pdfium.googlesource.com/pdfium/+/3eb3c4d77d4f9372f77aa4895b85a1d4e4755c89/testing/resources/javascript/xfa_specific/bug_1444238.in
[modify] https://pdfium.googlesource.com/pdfium/+/3eb3c4d77d4f9372f77aa4895b85a1d4e4755c89/fpdfsdk/pwl/cpwl_combo_box.cpp


### ts...@chromium.org (2023-05-11)

Thanks for bisect and suggested patch, which is essentially what I've landed with a few improvements.

### gi...@appspot.gserviceaccount.com (2023-05-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e6b75a8b4900535ea72775af93178e32f2e602be

commit e6b75a8b4900535ea72775af93178e32f2e602be
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri May 12 18:56:04 2023

Roll PDFium from 4c16842f61a1 to e60fa0d7d773 (6 revisions)

https://pdfium.googlesource.com/pdfium.git/+log/4c16842f61a1..e60fa0d7d773

2023-05-12 thestig@chromium.org Remove struct CFX_CTTGSUBTable::TLangSysRecord
2023-05-11 thestig@chromium.org Stop storing `CFX_Font::m_pSubData`
2023-05-11 thestig@chromium.org Improve error handling in CPDF_CIDFont::GetGlyphIndex()
2023-05-11 tsepez@chromium.org Observe widget across SetOptionSelection() calls.
2023-05-11 tsepez@chromium.org Always check return code from CPWL_ComboBox::SetPopup().
2023-05-11 dorianrudo97@gmail.com Save dash array and phase of GraphState in CPDF_PageContentGenerator

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC dhoss@chromium.org,pdfium-deps-rolls@chromium.org,thestig@chromium.org on the revert to ensure that a human
is aware of the problem.

To file a bug in PDFium: https://bugs.chromium.org/p/pdfium/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1444238,chromium:1444581
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I48188bbffa2048b5adf6abaeadd097dcd331fcb0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4527458
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1143435}

[modify] https://crrev.com/e6b75a8b4900535ea72775af93178e32f2e602be/DEPS


### [Deleted User] (2023-05-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-13)

Requesting merge to extended stable M112 because latest trunk commit (1143435) appears to be after extended stable branch point (1109224).

Requesting merge to stable M113 because latest trunk commit (1143435) appears to be after stable branch point (1121455).

Requesting merge to beta M114 because latest trunk commit (1143435) appears to be after beta branch point (1135570).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [112, 113, 114].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-14)

Requesting merge to extended stable M112 because latest trunk commit (1143435) appears to be after extended stable branch point (1109224).

Requesting merge to stable M113 because latest trunk commit (1143435) appears to be after stable branch point (1121455).

Requesting merge to beta M114 because latest trunk commit (1143435) appears to be after beta branch point (1135570).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [112, 113, 114].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-15)

Requesting merge to extended stable M112 because latest trunk commit (1143435) appears to be after extended stable branch point (1109224).

Requesting merge to stable M113 because latest trunk commit (1143435) appears to be after stable branch point (1121455).

Requesting merge to beta M114 because latest trunk commit (1143435) appears to be after beta branch point (1135570).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [112, 113, 114].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-16)

Requesting merge to extended stable M112 because latest trunk commit (1143435) appears to be after extended stable branch point (1109224).

Requesting merge to stable M113 because latest trunk commit (1143435) appears to be after stable branch point (1121455).

Requesting merge to beta M114 because latest trunk commit (1143435) appears to be after beta branch point (1135570).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [112, 113, 114].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ts...@chromium.org (2023-05-16)

1. https://pdfium-review.googlesource.com/c/pdfium/+/107390
2. Y
3. Y
4. N
5. N

### gi...@appspot.gserviceaccount.com (2023-05-16)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/56480ab74b691e9f7c8819f852e2ce7cdc5e53ec

commit 56480ab74b691e9f7c8819f852e2ce7cdc5e53ec
Author: Tom Sepez <tsepez@chromium.org>
Date: Tue May 16 21:59:16 2023

[M114] Always check return code from CPWL_ComboBox::SetPopup().

Operation must not continue when false is returned.

Bug: chromium:1444238
Change-Id: Ic8c29653ac185ac80b6248203649ce05d0e10f06
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/107390
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>
(cherry picked from commit 3eb3c4d77d4f9372f77aa4895b85a1d4e4755c89)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/107732
Auto-Submit: Tom Sepez <tsepez@chromium.org>

[add] https://pdfium.googlesource.com/pdfium/+/56480ab74b691e9f7c8819f852e2ce7cdc5e53ec/testing/resources/javascript/xfa_specific/bug_1444238.evt
[modify] https://pdfium.googlesource.com/pdfium/+/56480ab74b691e9f7c8819f852e2ce7cdc5e53ec/fpdfsdk/pwl/cpwl_combo_box.h
[add] https://pdfium.googlesource.com/pdfium/+/56480ab74b691e9f7c8819f852e2ce7cdc5e53ec/testing/resources/javascript/xfa_specific/bug_1444238.in
[modify] https://pdfium.googlesource.com/pdfium/+/56480ab74b691e9f7c8819f852e2ce7cdc5e53ec/fpdfsdk/pwl/cpwl_combo_box.cpp


### gi...@appspot.gserviceaccount.com (2023-05-16)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/5712847690eb998c07ee00748eabbc1a38ccc1ed

commit 5712847690eb998c07ee00748eabbc1a38ccc1ed
Author: Tom Sepez <tsepez@chromium.org>
Date: Tue May 16 22:50:41 2023

Revert "[M114] Always check return code from CPWL_ComboBox::SetPopup()."

This reverts commit 56480ab74b691e9f7c8819f852e2ce7cdc5e53ec.

Reason for revert: Wait for merge approval

Original change's description:
> [M114] Always check return code from CPWL_ComboBox::SetPopup().
>
> Operation must not continue when false is returned.
>
> Bug: chromium:1444238
> Change-Id: Ic8c29653ac185ac80b6248203649ce05d0e10f06
> Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/107390
> Commit-Queue: Tom Sepez <tsepez@chromium.org>
> Reviewed-by: Lei Zhang <thestig@chromium.org>
> (cherry picked from commit 3eb3c4d77d4f9372f77aa4895b85a1d4e4755c89)
> Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/107732
> Auto-Submit: Tom Sepez <tsepez@chromium.org>

TBR=thestig@chromium.org,tsepez@chromium.org

Change-Id: Iac48f933c05a2ff47848b09088e1f6f7671ed841
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: chromium:1444238
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/107738
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>

[delete] https://pdfium.googlesource.com/pdfium/+/56480ab74b691e9f7c8819f852e2ce7cdc5e53ec/testing/resources/javascript/xfa_specific/bug_1444238.evt
[modify] https://pdfium.googlesource.com/pdfium/+/5712847690eb998c07ee00748eabbc1a38ccc1ed/fpdfsdk/pwl/cpwl_combo_box.h
[delete] https://pdfium.googlesource.com/pdfium/+/56480ab74b691e9f7c8819f852e2ce7cdc5e53ec/testing/resources/javascript/xfa_specific/bug_1444238.in
[modify] https://pdfium.googlesource.com/pdfium/+/5712847690eb998c07ee00748eabbc1a38ccc1ed/fpdfsdk/pwl/cpwl_combo_box.cpp


### am...@chromium.org (2023-05-17)

Drats! Sorry you reverted because I was slow to do merge approvals here. :(
M114 merge approved, please go ahead and merge this fix for branch 5735 at your earliest convenience! 

There are no further planned releases of M113/Stable and M112/Extended Stable, so removing merge labels for each. 

### am...@google.com (2023-05-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-05-18)

Congratulations, Huyna! The VRP Panel has decided to award you $7,000 for this report + $1,000 patch bonus + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us -- nice work! 

### gi...@appspot.gserviceaccount.com (2023-05-19)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/8f3cb6304e719d9ee26290f2cf2d91ddc5657ed4

commit 8f3cb6304e719d9ee26290f2cf2d91ddc5657ed4
Author: Tom Sepez <tsepez@chromium.org>
Date: Fri May 19 18:41:31 2023

[M114] Always check return code from CPWL_ComboBox::SetPopup().

Operation must not continue when false is returned.

Bug: chromium:1444238
Change-Id: Ic8c29653ac185ac80b6248203649ce05d0e10f06
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/107390
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>
(cherry picked from commit 3eb3c4d77d4f9372f77aa4895b85a1d4e4755c89)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/107812

[add] https://pdfium.googlesource.com/pdfium/+/8f3cb6304e719d9ee26290f2cf2d91ddc5657ed4/testing/resources/javascript/xfa_specific/bug_1444238.evt
[modify] https://pdfium.googlesource.com/pdfium/+/8f3cb6304e719d9ee26290f2cf2d91ddc5657ed4/fpdfsdk/pwl/cpwl_combo_box.h
[add] https://pdfium.googlesource.com/pdfium/+/8f3cb6304e719d9ee26290f2cf2d91ddc5657ed4/testing/resources/javascript/xfa_specific/bug_1444238.in
[modify] https://pdfium.googlesource.com/pdfium/+/8f3cb6304e719d9ee26290f2cf2d91ddc5657ed4/fpdfsdk/pwl/cpwl_combo_box.cpp


### am...@google.com (2023-05-19)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-05-25)

[Empty comment from Monorail migration]

### am...@google.com (2023-05-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-30)

LTS Milestone M108

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2023-05-30)

[Empty comment from Monorail migration]

### rz...@google.com (2023-05-31)

[Empty comment from Monorail migration]

### rz...@google.com (2023-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-05-31)

1. Just https://pdfium-review.googlesource.com/c/pdfium/+/108190
2. Low, no conflicts
3. 114
4. Yes

### gm...@google.com (2023-05-31)

[Empty comment from Monorail migration]

### na...@google.com (2023-06-14)

[Empty comment from Monorail migration]

### na...@google.com (2023-06-14)

Merge approved for LTS-108

### gi...@appspot.gserviceaccount.com (2023-06-15)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/752df364098bb89ec20edf7755873f8db9c5b04a

commit 752df364098bb89ec20edf7755873f8db9c5b04a
Author: Tom Sepez <tsepez@chromium.org>
Date: Thu Jun 15 17:10:08 2023

[M108-LTS] Always check return code from CPWL_ComboBox::SetPopup().

Operation must not continue when false is returned.

Bug: chromium:1444238
Change-Id: Ic8c29653ac185ac80b6248203649ce05d0e10f06
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/107390
Commit-Queue: Tom Sepez <tsepez@chromium.org>
(cherry picked from commit 3eb3c4d77d4f9372f77aa4895b85a1d4e4755c89)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/108190
Reviewed-by: Lei Zhang <thestig@chromium.org>
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Auto-Submit: Roger Felipe Zanoni da Silva <rzanoni@google.com>

[add] https://pdfium.googlesource.com/pdfium/+/752df364098bb89ec20edf7755873f8db9c5b04a/testing/resources/javascript/xfa_specific/bug_1444238.evt
[modify] https://pdfium.googlesource.com/pdfium/+/752df364098bb89ec20edf7755873f8db9c5b04a/fpdfsdk/pwl/cpwl_combo_box.h
[add] https://pdfium.googlesource.com/pdfium/+/752df364098bb89ec20edf7755873f8db9c5b04a/testing/resources/javascript/xfa_specific/bug_1444238.in
[modify] https://pdfium.googlesource.com/pdfium/+/752df364098bb89ec20edf7755873f8db9c5b04a/fpdfsdk/pwl/cpwl_combo_box.cpp


### rz...@google.com (2023-06-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1444238?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064463)*
