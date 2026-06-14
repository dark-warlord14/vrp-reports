# Security: Use-after-free in CPDFSDK_WidgetHandler::OnLoad

| Field | Value |
|-------|-------|
| **Issue ID** | [40088036](https://issues.chromium.org/issues/40088036) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2017-06-10 |
| **Bounty** | $3,000.00 |

## Description


with PDFIUM with XFA enabled, there is a function `DeleteAnnot` which can be triggered by `Field::removeField`.

*** SNIP ***

bool Document::removeField(CJS_Runtime* pRuntime,
                           const std::vector<CJS_Value>& params,
                           CJS_Value& vRet,
                           CFX_WideString& sError) {
...

...

#if PDF_ENABLE_XFA
      pPageView->DeleteAnnot(pWidget);
...
*** SNIP ***


We can delete annot (widget) while its processing, cause to UAF.

// Details

At `LoadFXAnnots`, it's calling |Annot_OnLoad| which later will call |OnLoad| and leads to |OnFormat|.

void CPDFSDK_PageView::LoadFXAnnots() {
...
    while (CXFA_FFWidget* pXFAAnnot = pWidgetHander->MoveToNext()) {
      CPDFSDK_Annot* pAnnot = pAnnotHandlerMgr->NewAnnot(pXFAAnnot, this);
      if (!pAnnot)
        continue;
      m_SDKAnnotArray.push_back(pAnnot);
      pAnnotHandlerMgr->Annot_OnLoad(pAnnot);
    }
}



void CPDFSDK_WidgetHandler::OnLoad(CPDFSDK_Annot* pAnnot) {
...
  int nFieldType = pWidget->GetFieldType();
  if (nFieldType == FIELDTYPE_TEXTFIELD || nFieldType == FIELDTYPE_COMBOBOX) {
    bool bFormatted = false;
    CFX_WideString sValue = pWidget->OnFormat(bFormatted); <--- Here we can run script
...

}

we can define a v8 script like this:
```
this.removeField("MyField3");
```
to trigger |DeleteAnnot| -> free Widget.

Later, at |cpdfsdk_widgethandler.cpp:238:41| it will use |pWidget| while it's already been freed earlier.



## Attachments

- [test_6.pdf](attachments/test_6.pdf) (application/pdf, 4.9 KB)
- [asan](attachments/asan) (text/plain, 22.7 KB)
- [poc.pdf](attachments/poc.pdf) (application/pdf, 2.1 KB)

## Timeline

### ma...@gmail.com (2017-06-10)

Document JS Action script should be like this as well:
```
    var f = this.getField("MyField3");
    f.borderStyle = "inset";
```

### ma...@gmail.com (2017-06-11)

This file is simplified POC, not including other Annots.



### el...@chromium.org (2017-06-12)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### cl...@chromium.org (2017-06-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=4750817730232320

### el...@chromium.org (2017-06-13)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### lg...@chromium.org (2017-06-13)

ClusterFuzz is showing "not reproducible. :-(

### th...@chromium.org (2017-06-13)

CF didn't repro https://crbug.com/chromium/732051 either but I did locally. Perhaps because CF doesn't have XFA enabled? (I didn't check)

I'll add it to my queue.

### th...@chromium.org (2017-06-13)

Repros locally with XFA enabled.

### th...@chromium.org (2017-06-13)

https://pdfium-review.googlesource.com/6531

### es...@chromium.org (2017-06-14)

Guessing Security_Impact-Stable based on the other similar reports that came in in the same batch, but please correct if that's not the case.

### th...@chromium.org (2017-06-14)

XFA is disabled on stable.

### es...@chromium.org (2017-06-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-06-15)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/cd8ff7e9eb651a2ab78bd17a7d8a6cc6d9cce9c4

commit cd8ff7e9eb651a2ab78bd17a7d8a6cc6d9cce9c4
Author: Lei Zhang <thestig@chromium.org>
Date: Thu Jun 15 18:42:52 2017

Check for destroyed annotations in CPDFSDK_WidgetHandler::OnLoad().

BUG=chromium:732039

Change-Id: I0bc6b24cb41f093eae7bd0a96bcdd441ec8322d7
Reviewed-on: https://pdfium-review.googlesource.com/6531
Commit-Queue: dsinclair <dsinclair@chromium.org>
Reviewed-by: dsinclair <dsinclair@chromium.org>

[modify] https://crrev.com/cd8ff7e9eb651a2ab78bd17a7d8a6cc6d9cce9c4/fpdfsdk/cpdfsdk_widgethandler.cpp


### th...@chromium.org (2017-06-15)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-06-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a1d936022aea1afbfb396cc01da7ce031e08102f

commit a1d936022aea1afbfb396cc01da7ce031e08102f
Author: pdfium-deps-roller@chromium.org <pdfium-deps-roller@chromium.org>
Date: Thu Jun 15 20:24:26 2017

Roll src/third_party/pdfium/ 65a55343e..b7384b5b9 (3 commits)

https://pdfium.googlesource.com/pdfium.git/+log/65a55343e623..b7384b5b9979

$ git log 65a55343e..b7384b5b9 --date=short --no-merges --format='%ad %ae %s'
2017-06-13 thestig Improve ObserverPtr usage in CFFL_InteractiveFormFiller.
2017-06-13 thestig Check for destroyed annotations in CPDFSDK_WidgetHandler::OnLoad().
2017-06-13 thestig Add more checks for destroyed annotations in CFFL_FormFiller.

Created with:
  roll-dep src/third_party/pdfium
BUG=732322,732039,732051


Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, see:
http://www.chromium.org/developers/tree-sheriffs/sheriff-details-chromium#TOC-Failures-due-to-DEPS-rolls


TBR=dsinclair@chromium.org

Change-Id: I294c193c4276262e5503c4168254bef5ceb8577e
Reviewed-on: https://chromium-review.googlesource.com/537339
Reviewed-by: <pdfium-deps-roller@chromium.org>
Commit-Queue: <pdfium-deps-roller@chromium.org>
Cr-Commit-Position: refs/heads/master@{#479811}
[modify] https://crrev.com/a1d936022aea1afbfb396cc01da7ce031e08102f/DEPS


### sh...@chromium.org (2017-06-16)

[Empty comment from Monorail migration]

### ma...@gmail.com (2017-07-10)

[Comment Deleted]

### mb...@chromium.org (2017-08-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-08-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-08-28)

Thanks! The VRP PAnel decided to award $3,000 for this one - cheers!

### aw...@chromium.org (2017-08-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-09-22)

This issue was migrated from crbug.com/chromium/732039?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088036)*
