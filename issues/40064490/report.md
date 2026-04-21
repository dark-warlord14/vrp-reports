# Security: PDFium (XFA) Use-after-free in CFFL_ListBox::SaveData

| Field | Value |
|-------|-------|
| **Issue ID** | [40064490](https://issues.chromium.org/issues/40064490) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2023-05-10 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**  

Use-after-free in function CFFL\_ListBox::SaveData

**VERSION**  

Chrome Version: Version 114.0.5733.0 (Developer Build) (64-bit)  

Operating System: Windows 11

**REPRODUCTION CASE**

1. Enable XFA in chrome://flags
2. open file poc.pdf
3. click to List box on the first page then press `Tab` key

DETAIL

In function `CFFL_ListBox::SaveData`

```
void CFFL_ListBox::SaveData(const CPDFSDK_PageView\* pPageView) {  
  CPWL_ListBox\* pListBox = GetPWLListBox(pPageView);  
  if (!pListBox) {  
    return;  
  }  
  int32_t nNewTopIndex = pListBox->GetTopVisibleIndex();  
  ObservedPtr<CPWL_ListBox> observed_box(pListBox);  
  m_pWidget->ClearSelection();  
  if (!observed_box) {  
    return;  
  }  
  if (m_pWidget->GetFieldFlags() & pdfium::form_flags::kChoiceMultiSelect) {  
    for (int32_t i = 0, sz = pListBox->GetCount(); i < sz; i++) {  
      if (pListBox->IsItemSelected(i))  
        m_pWidget->SetOptionSelection(i);  
  } else {  
    m_pWidget->SetOptionSelection(pListBox->GetCurSel());  
  }  

```

We can trigger JS callback by calling function `m_pWidget->SetOptionSelection(i);` ==> free object `pListBox` ==> use again in next round of for loop.

BISECT  

The vulnerable code was added at the first commit of this file. The oldest version i get is <https://codereview.chromium.org/1185843005/> (since 2015) when the file had name  `fpdfsdk/include/formfiller/FFL_ListBox.c`. The bug is still there.

PATCH  

We should add check whether `pListBox` is freed or not after calling to `m_pWidget->SetOptionSelection(i);`

```
void CFFL_ListBox::SaveData(const CPDFSDK_PageView\* pPageView) {  
  CPWL_ListBox\* pListBox = GetPWLListBox(pPageView);  
  if (!pListBox) {  
    return;  
  }  
  int32_t nNewTopIndex = pListBox->GetTopVisibleIndex();  
  ObservedPtr<CPWL_ListBox> observed_box(pListBox);  
  m_pWidget->ClearSelection();  
  if (!observed_box) {  
    return;  
  }  
  if (m_pWidget->GetFieldFlags() & pdfium::form_flags::kChoiceMultiSelect) {  
    for (int32_t i = 0, sz = pListBox->GetCount(); i < sz; i++) {  
      if (pListBox->IsItemSelected(i)) {  
        m_pWidget->SetOptionSelection(i);  
        if (!observed_box) {  
          return;  
        }  
      }  
  } else {  
    m_pWidget->SetOptionSelection(pListBox->GetCurSel());  
  }  

```

CRASH INFORMATION

(44f0.1ec4): Access violation - code c0000005 (first chance)  

First chance exceptions are reported before any exception handling.  

This exception may be expected and handled.  

\*\*\* WARNING: Unable to verify checksum for D:\build-chrome\chromium\_25\_04\_23\src\out\xfa\_64bit\pdfium.dll  

pdfium!std::Cr::unique\_ptr<CPWL\_ListCtrl,std::Cr::default\_delete<CPWL\_ListCtrl> >::operator->+0x13:  

00007ffa`b3548883 488b00 mov rax,qword ptr [rax] ds:0000018d`61240fe8=????????????????  

\*\*\* WARNING: Unable to verify checksum for D:\build-chrome\chromium\_25\_04\_23\src\out\xfa\_64bit\chrome.dll  

\*\*\* WARNING: Unable to verify checksum for D:\build-chrome\chromium\_25\_04\_23\src\out\xfa\_64bit\blink\_core.dll  

\*\*\* WARNING: Unable to verify checksum for D:\build-chrome\chromium\_25\_04\_23\src\out\xfa\_64bit\blink\_platform.dll  

\*\*\* WARNING: Unable to verify checksum for D:\build-chrome\chromium\_25\_04\_23\src\out\xfa\_64bit\base.dll  

\*\*\* WARNING: Unable to verify checksum for D:\build-chrome\chromium\_25\_04\_23\src\out\xfa\_64bit\content.dll  

\*\*\* WARNING: Unable to verify checksum for chrome.exe  

7:199> kp

# Child-SP RetAddr Call Site

00 00000030`fc7fb7b0 00007ffa`b356594e pdfium!std::Cr::unique\_ptr<CPWL\_ListCtrl,std::Cr::default\_delete<CPWL\_ListCtrl> >::operator->(void)+0x13 [D:\build-chrome\chromium\_25\_04\_23\src\buildtools\third\_party\libc++\trunk\include\_*memory\unique\_ptr.h @ 274]  

01 00000030`fc7fb7e0 00007ffa`b2f90410 pdfium!CPWL\_ListBox::IsItemSelected(int nItemIndex = 0n6)+0x1e [D:\build-chrome\chromium\_25\_04\_23\src\third\_party\pdfium\fpdfsdk\pwl\cpwl\_list\_box.cpp @ 326]  

02 00000030`fc7fb820 00007ffa`b2f83c36 pdfium!CFFL\_ListBox::SaveData(class CPDFSDK\_PageView \* pPageView = 0x0000018d`6180cf70)+0x140 [D:\build-chrome\chromium_25_04_23\src\third_party\pdfium\fpdfsdk\formfiller\cffl_listbox.cpp @ 119] 03 00000030`fc7fb8c0 00007ffa`b2f839aa pdfium!CFFL_FormField::CommitData(class CPDFSDK_PageView \* pPageView = 0x0000018d`6180cf70, class fxcrt::Mask<FWL\_EVENTFLAG> nFlag = class fxcrt::Mask<FWL\_EVENTFLAG>)+0x1d6 [D:\build-chrome\chromium\_25\_04\_23\src\third\_party\pdfium\fpdfsdk\formfiller\cffl\_formfield.cpp @ 499]  

04 00000030`fc7fb940 00007ffa`b2f89dd1 pdfium!CFFL\_FormField::KillFocusForAnnot(class fxcrt::Mask<FWL\_EVENTFLAG> nFlag = class fxcrt::Mask<FWL\_EVENTFLAG>)+0xaa [D:\build-chrome\chromium\_25\_04\_23\src\third\_party\pdfium\fpdfsdk\formfiller\cffl\_formfield.cpp @ 286]  

05 00000030`fc7fb9b0 00007ffa`b2f29a1f pdfium!CFFL\_InteractiveFormFiller::OnKillFocus(class fxcrt::ObservedPtr<CPDFSDK\_Widget> \* pWidget = 0x00000030`fc7fbab8, class fxcrt::Mask<FWL_EVENTFLAG> nFlag = class fxcrt::Mask<FWL_EVENTFLAG>)+0xb1 [D:\build-chrome\chromium_25_04_23\src\third_party\pdfium\fpdfsdk\formfiller\cffl_interactiveformfiller.cpp @ 409] 06 00000030`fc7fba70 00007ffa`b2edb204 pdfium!CPDFSDK_Widget::OnKillFocus(class fxcrt::Mask<FWL_EVENTFLAG> nFlags = class fxcrt::Mask<FWL_EVENTFLAG>)+0xcf [D:\build-chrome\chromium_25_04_23\src\third_party\pdfium\fpdfsdk\cpdfsdk_widget.cpp @ 849] 07 00000030`fc7fbae0 00007ffa`b2f086bb pdfium!CPDFSDK_Annot::OnKillFocus(class fxcrt::ObservedPtr<CPDFSDK_Annot> \* pAnnot = 0x00000030`fc7fbba8, class fxcrt::Mask<FWL\_EVENTFLAG> nFlags = class fxcrt::Mask<FWL\_EVENTFLAG>)+0x44 [D:\build-chrome\chromium\_25\_04\_23\src\third\_party\pdfium\fpdfsdk\cpdfsdk\_annot.cpp @ 112]  

08 00000030`fc7fbb30 00007ffa`b2f099d1 pdfium!CPDFSDK\_FormFillEnvironment::KillFocusAnnot(class fxcrt::Mask<FWL\_EVENTFLAG> nFlags = class fxcrt::Mask<FWL\_EVENTFLAG>)+0xab [D:\build-chrome\chromium\_25\_04\_23\src\third\_party\pdfium\fpdfsdk\cpdfsdk\_formfillenvironment.cpp @ 779]  

09 00000030`fc7fbbd0 00007ffa`b2f1f183 pdfium!CPDFSDK\_FormFillEnvironment::SetFocusAnnot(class fxcrt::ObservedPtr<CPDFSDK\_Annot> \* pAnnot = 0x00000030`fc7fbcd0)+0xb1 [D:\build-chrome\chromium_25_04_23\src\third_party\pdfium\fpdfsdk\cpdfsdk_formfillenvironment.cpp @ 739] 0a 00000030`fc7fbc40 00007ffa`b2f57707 pdfium!CPDFSDK_PageView::OnKeyDown(<unnamed-tag> nKeyCode = FWL_VKEY_Tab (0n9), class fxcrt::Mask<FWL_EVENTFLAG> nFlags = class fxcrt::Mask<FWL_EVENTFLAG>)+0x1b3 [D:\build-chrome\chromium_25_04_23\src\third_party\pdfium\fpdfsdk\cpdfsdk_pageview.cpp @ 511] 0b 00000030`fc7fbd10 00007ffa`dfb8816b pdfium!FORM_OnKeyDown(struct fpdf_form_handle_t__ \* hHandle = 0x0000018d`54c44f60, struct fpdf\_page\_t*\_ \* page = 0x0000018d`63f24fd0, int nKeyCode = 0n9, int modifier = 0n0)+0x87 [D:\build-chrome\chromium_25_04_23\src\third_party\pdfium\fpdfsdk\fpdf_formfill.cpp @ 485] 0c 00000030`fc7fbd80 00007ffa`dfb780ca chrome!chrome_pdf::PDFiumEngine::HandleTabForward(int modifiers = 0n0)+0xfb [D:\build-chrome\chromium_25_04_23\src\pdf\pdfium\pdfium_engine.cc @ 4207] 0d 00000030`fc7fbde0 00007ffa`dfb72572 chrome!chrome_pdf::PDFiumEngine::HandleTabEvent(int modifiers = 0n0)+0xca [D:\build-chrome\chromium_25_04_23\src\pdf\pdfium\pdfium_engine.cc @ 4178] 0e 00000030`fc7fbe30 00007ffa`dfb7174d chrome!chrome_pdf::PDFiumEngine::OnKeyDown(class blink::WebKeyboardEvent \* \*\*\* WARNING: Unable to verify checksum for D:\build-chrome\chromium_25_04_23\src\out\xfa_64bit\blink_common.dll event = 0x0000018d`0fd98f90)+0x52 [D:\build-chrome\chromium\_25\_04\_23\src\pdf\pdfium\pdfium\_engine.cc @ 1692]  

0f 00000030`fc7fbf40 00007ffa`e41ef4ec chrome!chrome\_pdf::PDFiumEngine::HandleInputEvent(class blink::WebInputEvent \* event = 0x0000018d`0fd98f90)+0x15d [D:\build-chrome\chromium_25_04_23\src\pdf\pdfium\pdfium_engine.cc @ 961] 10 00000030`fc7fc040 00007ffa`e41ef61b chrome!chrome_pdf::PdfViewWebPlugin::HandleWebInputEvent(class blink::WebInputEvent \* event = 0x0000018d`0fd98f90)+0x17c [D:\build-chrome\chromium\_25\_04\_23\src\pdf\pdf\_view\_web\_plugin.cc @ 2018]  

11 00000030`fc7fc0f0 00007ffa`c25036a8 chrome!chrome\_pdf::PdfViewWebPlugin::HandleInputEvent(class blink::WebCoalescedInputEvent \* event = 0x00000030`fc7fc240, class ui::Cursor \* cursor = 0x00000030`fc7fc2c0)+0x5b [D:\build-chrome\chromium\_25\_04\_23\src\pdf\pdf\_view\_web\_plugin.cc @ 545]  

12 00000030`fc7fc1b0 00007ffa`c2502da0 blink\_core!blink::WebPluginContainerImpl::HandleKeyboardEvent(class blink::KeyboardEvent \* event = 0x0000389d`00442e08)+0x118 [D:\build-chrome\chromium_25_04_23\src\third_party\blink\renderer\core\exported\web_plugin_container_impl.cc @ 902] 13 00000030`fc7fc390 00007ffa`bfb6834c blink_core!blink::WebPluginContainerImpl::HandleEvent(class blink::Event \* event = 0x0000389d`00442e08)+0xd0 [D:\build-chrome\chromium\_25\_04\_23\src\third\_party\blink\renderer\core\exported\web\_plugin\_container\_impl.cc @ 269]  

14 00000030`fc7fc430 00007ffa`c14e7dee blink\_core!blink::HTMLPlugInElement::DefaultEventHandler(class blink::Event \* event = 0x0000389d`00442e08)+0xdc [D:\build-chrome\chromium_25_04_23\src\third_party\blink\renderer\core\html\html_plugin_element.cc @ 481] 15 00000030`fc7fc490 00007ffa`c14e70a8 blink_core!blink::EventDispatcher::DispatchEventPostProcess(class blink::Node \* activation_target = 0x00000000`00000000, class blink::EventDispatchHandlingState \* pre\_dispatch\_event\_handler\_result = 0x00000000`00000000)+0x31e [D:\build-chrome\chromium_25_04_23\src\third_party\blink\renderer\core\dom\events\event_dispatcher.cc @ 406] 16 00000030`fc7fc560 00007ffa`beef7188 blink\_core!blink::EventDispatcher::Dispatch(void)+0xb88 [D:\build-chrome\chromium\_25\_04\_23\src\third\_party\blink\renderer\core\dom\events\event\_dispatcher.cc @ 264]

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 4.0 KB)

## Timeline

### [Deleted User] (2023-05-10)

[Empty comment from Monorail migration]

### me...@chromium.org (2023-05-11)

Thanks for the report, reproduced in M112.

tsepez, could you PTAL?

[Monorail components: Internals>Plugins>PDF]

### [Deleted User] (2023-05-11)

[Empty comment from Monorail migration]

### ts...@chromium.org (2023-05-11)

Yep, reproduces under chrome but hard to do under standalone pdfium_test because it requires chrome to process the tab as advance to next page.

### gi...@appspot.gserviceaccount.com (2023-05-11)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/a9ff918a86d700c3bdf9b5820faed35490c0cd25

commit a9ff918a86d700c3bdf9b5820faed35490c0cd25
Author: Tom Sepez <tsepez@chromium.org>
Date: Thu May 11 20:57:21 2023

Observe widget across SetOptionSelection() calls.

Call may re-enter JavaScript.

Bug: chromium:1444581
Change-Id: Id7a2f17b3b81f822ca8f4496ac08c19b7794c48a
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/107394
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/a9ff918a86d700c3bdf9b5820faed35490c0cd25/fpdfsdk/formfiller/cffl_listbox.cpp


### ts...@chromium.org (2023-05-11)

[Empty comment from Monorail migration]

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

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

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

1. https://pdfium-review.googlesource.com/c/pdfium/+/107394
2. Y
3. Y
4. N
5. N


### [Deleted User] (2023-05-17)

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

### am...@chromium.org (2023-05-17)

M114 merge approved, please merge this fix to branch 5735 at your earliest convenience 

There are not further planned releases of M113/Stable and M112/Extended Stable; removing merge labels those 

### gi...@appspot.gserviceaccount.com (2023-05-18)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/e35d8f8de67ad1d5b73e7da00c897b7b492dd423

commit e35d8f8de67ad1d5b73e7da00c897b7b492dd423
Author: Tom Sepez <tsepez@chromium.org>
Date: Thu May 18 18:37:17 2023

[M114] Observe widget across SetOptionSelection() calls.

Call may re-enter JavaScript.

Bug: chromium:1444581
Change-Id: Id7a2f17b3b81f822ca8f4496ac08c19b7794c48a
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/107394
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>
(cherry picked from commit a9ff918a86d700c3bdf9b5820faed35490c0cd25)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/107735
Auto-Submit: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/e35d8f8de67ad1d5b73e7da00c897b7b492dd423/fpdfsdk/formfiller/cffl_listbox.cpp


### am...@google.com (2023-05-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-05-19)

Congratulations on another one, Huyna! The VRP Panel has decided to award you $7,000 for this report + $1,000 patch bonus + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us -- nice work! 

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

1. Only https://pdfium-review.googlesource.com/c/pdfium/+/108171
2. Low, no conflicts
3. 114
4. Yes

### gm...@google.com (2023-05-31)

[Empty comment from Monorail migration]

### na...@google.com (2023-06-14)

[Empty comment from Monorail migration]

### na...@google.com (2023-06-14)

Approved for LTS-108

### gi...@appspot.gserviceaccount.com (2023-06-15)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/027cbf10093d6ac18a3558bf3c289179f1c0f0e1

commit 027cbf10093d6ac18a3558bf3c289179f1c0f0e1
Author: Tom Sepez <tsepez@chromium.org>
Date: Thu Jun 15 17:09:39 2023

[M108-LTS] Observe widget across SetOptionSelection() calls.

Call may re-enter JavaScript.

Bug: chromium:1444581
Change-Id: Id7a2f17b3b81f822ca8f4496ac08c19b7794c48a
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/107394
Commit-Queue: Tom Sepez <tsepez@chromium.org>
(cherry picked from commit a9ff918a86d700c3bdf9b5820faed35490c0cd25)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/108171
Reviewed-by: Lei Zhang <thestig@chromium.org>
Auto-Submit: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>

[modify] https://pdfium.googlesource.com/pdfium/+/027cbf10093d6ac18a3558bf3c289179f1c0f0e1/fpdfsdk/formfiller/cffl_listbox.cpp


### rz...@google.com (2023-06-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1444581?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064490)*
