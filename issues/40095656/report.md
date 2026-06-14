# PDFium (XFA) Use-after-free in CPDFSDK_XFAWidgetHandler::OnXFAChangedFocus

| Field | Value |
|-------|-------|
| **Issue ID** | [40095656](https://issues.chromium.org/issues/40095656) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | my...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-07-09 |
| **Bounty** | $5,500.00 |

## Description

Steps to reproduce the problem:
1. Compile the latest chromium with enabled XFA PDFium
2. Open file test.pdf with chrome
3. Double-click to any place in page (MUST BE double-click)

What is the expected behavior?

What went wrong?
CXFA_FFPageView object use-after-free in function CPDFSDK_XFAWidgetHandler::OnXFAChangedFocus

Did this work before? N/A 

Chrome version: Lasted  Channel: n/a
OS Version: Windows 10 
Flash Version:

The bug is in |CPDFSDK_XFAWidgetHandler::OnXFAChangedFocus| function

bool CPDFSDK_XFAWidgetHandler::OnXFAChangedFocus(
    ObservedPtr<CPDFSDK_Annot>* pOldAnnot,
    ObservedPtr<CPDFSDK_Annot>* pNewAnnot) {
  CXFA_FFWidgetHandler* pWidgetHandler = nullptr;
  if (pOldAnnot->HasObservable())
    pWidgetHandler = GetXFAWidgetHandler(pOldAnnot->Get());
  else if (pNewAnnot->HasObservable())
    pWidgetHandler = GetXFAWidgetHandler(pNewAnnot->Get());

  if (!pWidgetHandler)
    return true;

  CXFA_FFWidget* hWidget = *pNewAnnot ? (*pNewAnnot)->GetXFAWidget() : nullptr;
  if (!hWidget)
    return true;

  CXFA_FFPageView* pXFAPageView = hWidget->GetPageView();
  if (!pXFAPageView)
    return true;

  bool bRet = pXFAPageView->GetDocView()->SetFocus(hWidget);		
  if (pXFAPageView->GetDocView()->GetFocusWidget() == hWidget)
    bRet = true;

  return bRet;
}

Function |SetFocus| can trigger to JS code by setting an 'enter' event to field. Like in proof-of-concept file, i have a field like this

<exclGroup name="exclGroup1" x="0mm" y="0mm" h="300mm" w="300mm">
	<field h="300mm" w="300mm" x="0mm" y="0mm" name="field1">
		<ui>
			<checkButton shape="round">
			</checkButton>
		</ui>
		<items>
			<text>Single</text>
		</items>
	</field>
	<event activity="enter">
		<script contentType="application/x-javascript">
			f2 = xfa.resolveNode("field2");
			xfa.host.setFocus(f2);
			xfa.form.remerge();    
			xfa.host.openList(f2);
		</script>
	</event>
</exclGroup>

JS code in 'enter' event will be executed when function  and it'll free the object |pXFAPageView|. After JS code and back to function |OnXFAChangedFocus|, the object |pXFAPageView| will be used again => use-after-free bug



## Attachments

- [test.pdf](attachments/test.pdf) (application/pdf, 9.3 KB)
- [log_crash.txt](attachments/log_crash.txt) (text/plain, 12.4 KB)

## Timeline

### pa...@chromium.org (2019-07-09)

[Empty comment from Monorail migration]

### pa...@chromium.org (2019-07-09)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-29)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/0e71ce2b1e725da7919c201cb9e8cf3095194b1c

commit 0e71ce2b1e725da7919c201cb9e8cf3095194b1c
Author: Minh Tran <myoki.crystal@gmail.com>
Date: Mon Jul 29 22:28:49 2019

Observe CXFA_FFPageView across OnSetFocus() events.

CXFA_FFPageView object is destroyed by JS code of enter event.
Use ObservedPtr to catch this destruction.

Bug: chromium:982397
Change-Id: Ie7cd472f561eec410c9ccd5a25319fbd8e63b5ec
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/58390
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/0e71ce2b1e725da7919c201cb9e8cf3095194b1c/xfa/fxfa/cxfa_ffpageview.h
[modify] https://pdfium.googlesource.com/pdfium/+/0e71ce2b1e725da7919c201cb9e8cf3095194b1c/fpdfsdk/cpdfsdk_formfillenvironment.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/0e71ce2b1e725da7919c201cb9e8cf3095194b1c/fpdfsdk/cpdfsdk_xfawidgethandler.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/0e71ce2b1e725da7919c201cb9e8cf3095194b1c/AUTHORS


### ts...@chromium.org (2019-07-29)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/cbac3d9b7a1ddfea74d556bd69cb5b86bb3a55cd

commit cbac3d9b7a1ddfea74d556bd69cb5b86bb3a55cd
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Jul 30 01:15:06 2019

Roll src/third_party/pdfium fee18fe49862..d31c667503bc (4 commits)

https://pdfium.googlesource.com/pdfium.git/+log/fee18fe49862..d31c667503bc


git log fee18fe49862..d31c667503bc --date=short --no-merges --format='%ad %ae %s'
2019-07-29 benjamin.beaudry@microsoft.com Get the rotation angle of a character.
2019-07-29 myoki.crystal@gmail.com Observe CXFA_FFPageView across OnSetFocus() events.
2019-07-29 thestig@chromium.org Roll third_party/freetype/src/ b110acba9..12af46b64 (2 commits)
2019-07-29 thestig@chromium.org Fix some nits in FPDFDOC_InitFormFillEnvironment().


Created with:
  gclient setdep -r src/third_party/pdfium@d31c667503bc

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



TBR=pdfium-deps-rolls@chromium.org

Bug: chromium:985604,chromium:982397
Change-Id: I0bcdc5298da26dc5baaa1e1556c78d4e42a8b900
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1725216
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#682083}

[modify] https://crrev.com/cbac3d9b7a1ddfea74d556bd69cb5b86bb3a55cd/DEPS


### na...@google.com (2019-07-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-30)

[Empty comment from Monorail migration]

### na...@google.com (2019-08-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-08-01)

Congrats! The Panel decided to reward you $5,500 for this report! 

### na...@google.com (2019-08-01)

[Empty comment from Monorail migration]

### pa...@chromium.org (2019-08-01)

 myoki.crystal@gmail.com - please let me know how you would like to be credited in our release notes

### my...@gmail.com (2019-08-01)

Thank you for the reward, I would like to be credited as "tictactoe" if possible.

### sh...@chromium.org (2019-11-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-11-05)

This issue was migrated from crbug.com/chromium/982397?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095656)*
