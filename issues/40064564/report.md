# Security:  Use-after-free in CPWL_ComboBox::OnKeyDown

| Field | Value |
|-------|-------|
| **Issue ID** | [40064564](https://issues.chromium.org/issues/40064564) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | qu...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2023-05-15 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**  

Use-after-free in CPWL\_ComboBox::OnKeyDown function.

**VERSION**  

Chrome Version: Version 103.0.5052.0 (Developer Build) (64-bit)

Build: <https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/win32-release_x64%2Fasan-win32-release_x64-1000829.zip?generation=1652053640869754&alt=media>

Operating System: Microsoft Windows [Version 10.0.19045.2965]

**REPRODUCTION CASE**

1. Run process `chrome.exe --no-sandbox --enable-logging=stderr`
2. open file poc.pdf
3. click to anywhere on the first page then press `KeyDown` key

DETAIL

In function CPWL\_ComboBox::OnKeyDown

```
    case FWL_VKEY_Down:  
      if (m_pList->GetCurSel() < m_pList->GetCount() - 1) {  
        if (GetFillerNotify()->OnPopupPreOpen(GetAttachedData(), nFlag))  
          return false;  
        if (GetFillerNotify()->OnPopupPostOpen(GetAttachedData(), nFlag))  
          return false;  
        if (m_pList->IsMovementKey(nKeyCode)) {  
          if (m_pList->OnMovementKeyDown(nKeyCode, nFlag))  
            return false;  
          SetSelectText();  
        }  
      }  

```

This section is a handler when KeyDown button is pressed to ComboBox field. Then function `CPWL_CBListBox::OnMovementKeyDown` is called

```
bool CPWL_CBListBox::OnMovementKeyDown(FWL_VKEYCODE nKeyCode,  
                                       Mask<FWL_EVENTFLAG> nFlag) {  
  switch (nKeyCode) {  
    case FWL_VKEY_Up:  
      m_pListCtrl->OnVK_UP(IsSHIFTKeyDown(nFlag), IsCTRLKeyDown(nFlag));  
      break;  
    case FWL_VKEY_Down:  
      m_pListCtrl->OnVK_DOWN(IsSHIFTKeyDown(nFlag), IsCTRLKeyDown(nFlag));  
      break;  
        
  ...  
  
    default:  
      NOTREACHED_NORETURN();  
      break;  
  }  
  return OnNotifySelectionChanged(true, nFlag);  
}    

```

At the end of this function, there is a call to `OnNotifySelectionChanged`

```
bool CPWL_ListBox::OnNotifySelectionChanged(bool bKeyDown,  
                                            Mask<FWL_EVENTFLAG> nFlag) {  
  ObservedPtr<CPWL_Wnd> thisObserved(this);  
  
  WideString swChange = GetText();  
  WideString strChangeEx;  
  int nSelStart = 0;  
  int nSelEnd = pdfium::base::checked_cast<int>(swChange.GetLength());  
  bool bRC;  
  bool bExit;  
  std::tie(bRC, bExit) = GetFillerNotify()->OnBeforeKeyStroke(  
      GetAttachedData(), swChange, strChangeEx, nSelStart, nSelEnd, bKeyDown,  
      nFlag);  
  
  if (!thisObserved)  
    return false;  

```

This `OnNotifySelectionChanged` in this turn call to `CFFL_InteractiveFormFiller::OnBeforeKeyStroke`. In this function, we can trigger a JS callback via Keystroke event of Combobox field. In pdf language, we can add an `/K` tag to combobox field object like:

```
% Fields  
13 0 obj <<  
  /Parent 12 0 R  
  /Type /Annot  
  /Subtype /Widget  
  /Rect [0 0 612 792]  
  /AA << /K 20 0 R >>  
>>  
20 0 obj <<  
  /S /JavaScript  
  /JS 21 0 R  
>>  
endobj  
% JS program to exexute  
21 0 obj <<  
>>  
stream  
var t = this.filesize;  
endstream  
endobj  

```

When JS callback is called, we can manage to trigger freeing of object `CPWL_ComboBox` then this object will be used again when return to function `CPWL_ComboBox::OnKeyDown`. We can see that, browser crash in function `CPWL_ComboBox::SetSelectText()` when it tried to get a variable field in freed object `CPWL_ComboBox`

Note that this bug does not need XFA enabled.

BISECT  

I will provide further information later

PATCH  

We need to watch a state of `CPWL_ComboBox` object after `OnMovementKeyDown` function

```
bool CPWL_ComboBox::OnKeyDown(FWL_VKEYCODE nKeyCode,  
                              Mask<FWL_EVENTFLAG> nFlag) {  
    
  ObservedPtr<CPWL_Wnd> thisObserved(this);  
    
  if (!m_pList)  
    return false;  
  if (!m_pEdit)  
    return false;  
  
  m_nSelectItem = -1;  
  
  switch (nKeyCode) {  
    case FWL_VKEY_Up:  
      if (m_pList->GetCurSel() > 0) {  
        if (GetFillerNotify()->OnPopupPreOpen(GetAttachedData(), nFlag))  
          return false;  
        if (GetFillerNotify()->OnPopupPostOpen(GetAttachedData(), nFlag))  
          return false;  
        if (m_pList->IsMovementKey(nKeyCode)) {  
          if (m_pList->OnMovementKeyDown(nKeyCode, nFlag))  
            return false;  
              
          if (!thisObserved)  
            return false;              
              
          SetSelectText();  
        }  
      }  
      return true;  
    case FWL_VKEY_Down:  
      if (m_pList->GetCurSel() < m_pList->GetCount() - 1) {  
        if (GetFillerNotify()->OnPopupPreOpen(GetAttachedData(), nFlag))  
          return false;  
        if (GetFillerNotify()->OnPopupPostOpen(GetAttachedData(), nFlag))  
          return false;  
        if (m_pList->IsMovementKey(nKeyCode)) {  
          if (m_pList->OnMovementKeyDown(nKeyCode, nFlag))  
            return false;  
            
          if (!thisObserved)  
            return false;  
            
          SetSelectText();  
        }  
      }  
      return true;  
    default:  
      break;  
  }  
  
  if (HasFlag(PCBS_ALLOWCUSTOMTEXT))  
    return m_pEdit->OnKeyDown(nKeyCode, nFlag);  
  
  return false;  
}  

```

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 2.7 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 17.2 KB)

## Timeline

### [Deleted User] (2023-05-15)

[Empty comment from Monorail migration]

### ts...@chromium.org (2023-05-15)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### qu...@gmail.com (2023-05-15)

update: please enable XFA

### ts...@chromium.org (2023-05-15)

Thanks for the patch, no need to bisect as this is old code and goes far back.

### gi...@appspot.gserviceaccount.com (2023-05-15)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/29c665ea4c61b089746c3f502c30fcb5f4b11486

commit 29c665ea4c61b089746c3f502c30fcb5f4b11486
Author: Tom Sepez <tsepez@chromium.org>
Date: Mon May 15 23:20:51 2023

Observe CPWL_ComboBox across all On* methods

Bug: chromium:1445426
Change-Id: I1d7ebf66fe170ca016c27a0df3ac4574e75c763c
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/107650
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[add] https://pdfium.googlesource.com/pdfium/+/29c665ea4c61b089746c3f502c30fcb5f4b11486/testing/resources/javascript/bug_1445426.evt
[modify] https://pdfium.googlesource.com/pdfium/+/29c665ea4c61b089746c3f502c30fcb5f4b11486/fpdfsdk/pwl/cpwl_combo_box.cpp
[add] https://pdfium.googlesource.com/pdfium/+/29c665ea4c61b089746c3f502c30fcb5f4b11486/testing/resources/javascript/bug_1445426.in


### ts...@chromium.org (2023-05-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-16)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-16)

This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M112. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M113. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M114. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [112, 113, 114].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-05-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/87ecb04886fb79c132f2d68fb29387850323b0d3

commit 87ecb04886fb79c132f2d68fb29387850323b0d3
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue May 16 21:37:24 2023

Manual roll PDFium from 7884587b9605 to 2c2634093e0f (14 revisions)

Manual roll requested by tsepez@google.com

https://pdfium.googlesource.com/pdfium.git/+log/7884587b9605..2c2634093e0f

2023-05-16 tsepez@chromium.org Fix duplicate shim symbols in chromium build
2023-05-16 tsepez@chromium.org Fix GN visibility checks when building with chromium.
2023-05-16 awscreen@chromium.org Roll build/ 64c99419f..3c9055956 (93 commits)
2023-05-15 tsepez@chromium.org Use malloc shim for testing on all platforms (except win)
2023-05-15 thestig@chromium.org Make Retaintable subclass's ctors/dtor non-public
2023-05-15 tsepez@chromium.org Rename local thisObserved to this_observed
2023-05-15 tsepez@chromium.org Observe CPWL_ComboBox across all On* methods
2023-05-15 thestig@chromium.org Clean up CPDF_StructElement
2023-05-15 tsepez@chromium.org Make PDFium tests compatible with BRP-enabled allocators.
2023-05-15 tsepez@chromium.org Avoid redundant calls to get CFXJSE_Engine in CJX_Object::RunMethod()
2023-05-15 thestig@chromium.org Prevent dangling pointer in CPDF_StructTree::AddPageNode()
2023-05-15 thestig@chromium.org Remove CollectionSize() use in CPDF_StructTree::LoadPageTree()
2023-05-15 tsepez@chromium.org Support BackupRefPtr in PDFium.
2023-05-15 pdfium-autoroll@skia-public.iam.gserviceaccount.com Roll Catapult from ac30cc4bc7d3 to 730ebc3ef2f3 (44 revisions)

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC dhoss@chromium.org,pdfium-deps-rolls@chromium.org,thestig@chromium.org,tsepez@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in PDFium: https://bugs.chromium.org/p/pdfium/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1443021,chromium:1443100,chromium:1445426
Tbr: pdfium-deps-rolls@chromium.org,tsepez@google.com
Change-Id: Id191e707fd6f8dab36d0d8bcfeaabd5d317edbfc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4540104
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1144942}

[modify] https://crrev.com/87ecb04886fb79c132f2d68fb29387850323b0d3/DEPS


### [Deleted User] (2023-05-17)

Requesting merge to extended stable M112 because latest trunk commit (1144942) appears to be after extended stable branch point (1109224).

Requesting merge to stable M113 because latest trunk commit (1144942) appears to be after stable branch point (1121455).

Requesting merge to beta M114 because latest trunk commit (1144942) appears to be after beta branch point (1135570).

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

Thanks for your quick work on this tsepez@ -- M114 merge approved, please merge this fix to branch 5735 at your earliest convenience. 

There are no further planned releases of M113/Stable and M112/Extended, so removing labels for those merges. 

### gi...@appspot.gserviceaccount.com (2023-05-19)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/9505810f66cc3dde86c30d072de53ca6fc8a45de

commit 9505810f66cc3dde86c30d072de53ca6fc8a45de
Author: Tom Sepez <tsepez@chromium.org>
Date: Fri May 19 20:05:10 2023

[M114] Observe CPWL_ComboBox across all On* methods

Bug: chromium:1445426
Change-Id: I1d7ebf66fe170ca016c27a0df3ac4574e75c763c
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/107650
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>
(cherry picked from commit 29c665ea4c61b089746c3f502c30fcb5f4b11486)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/107811

[add] https://pdfium.googlesource.com/pdfium/+/9505810f66cc3dde86c30d072de53ca6fc8a45de/testing/resources/javascript/bug_1445426.evt
[modify] https://pdfium.googlesource.com/pdfium/+/9505810f66cc3dde86c30d072de53ca6fc8a45de/fpdfsdk/pwl/cpwl_combo_box.cpp
[add] https://pdfium.googlesource.com/pdfium/+/9505810f66cc3dde86c30d072de53ca6fc8a45de/testing/resources/javascript/bug_1445426.in


### am...@google.com (2023-05-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-05-25)

Congratulations, Quang! The VRP Panel has decided to award you $7,000 + $1,000 patch bonus + $1,000 bisect bonus (since you report clearly presented where this issue was and the owner knew how far back this issue goes and conveyed your bisect, while welcome, wasn't needed). Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@chromium.org (2023-05-25)

[Empty comment from Monorail migration]

### qu...@gmail.com (2023-05-26)

That's great! Thanks a million for bounty. I really appreciate it.

### am...@google.com (2023-05-27)

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

1. Just https://pdfium-review.googlesource.com/c/pdfium/+/108170
2. Low, no conflicts
3. 114
4. Yes

### gm...@google.com (2023-05-31)

[Empty comment from Monorail migration]

### pg...@google.com (2023-05-31)

cc'ing xrosado for UI fuzzing knowledge

### am...@chromium.org (2023-06-14)

[Empty comment from Monorail migration]

### na...@google.com (2023-06-14)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-06-15)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/49cfa407428a46e473579ba7cb5a8453047d2048

commit 49cfa407428a46e473579ba7cb5a8453047d2048
Author: Tom Sepez <tsepez@chromium.org>
Date: Thu Jun 15 17:04:32 2023

[M108-LTS] Observe CPWL_ComboBox across all On* methods

Bug: chromium:1445426
Change-Id: I1d7ebf66fe170ca016c27a0df3ac4574e75c763c
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/107650
Commit-Queue: Tom Sepez <tsepez@chromium.org>
(cherry picked from commit 29c665ea4c61b089746c3f502c30fcb5f4b11486)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/108170
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Lei Zhang <thestig@chromium.org>
Auto-Submit: Roger Felipe Zanoni da Silva <rzanoni@google.com>

[add] https://pdfium.googlesource.com/pdfium/+/49cfa407428a46e473579ba7cb5a8453047d2048/testing/resources/javascript/bug_1445426.evt
[modify] https://pdfium.googlesource.com/pdfium/+/49cfa407428a46e473579ba7cb5a8453047d2048/fpdfsdk/pwl/cpwl_combo_box.cpp
[add] https://pdfium.googlesource.com/pdfium/+/49cfa407428a46e473579ba7cb5a8453047d2048/testing/resources/javascript/bug_1445426.in


### rz...@google.com (2023-06-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1445426?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064564)*
