# Security: UAF in CFFL_FormFiller::GetPDFWindow()

| Field | Value |
|-------|-------|
| **Issue ID** | [40088038](https://issues.chromium.org/issues/40088038) |
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

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36

Steps to reproduce the problem:
1. Build PDFIUm with XFA
2. run ./pdfium_test ./test_7.pdf
3. ASAN crash

What is the expected behavior?

What went wrong?
Notice: XFA must be enabled.

Page 0 includes "MyField3" textbox. 

Document JS Action:
```
this.getField("MyField3").setFocus();
```

MyField3 has its own "Validate" AAction as: 
```
  if(this.baseURL == "1"){
    app.alert("validate field3");
    this.removeField("MyField3");
  }
  this.baseURL="1";
```

Page 0 also got "Close" AAction:
```
this.getField('MyField3').value = "123";
app.alert("close page");
```

Explain:
Firstly, we setFocus the textbox |MyField3| to set |pFocusAnnot|.

then when "Closing" Page 0, it will trigger `app::alert("close page")`, later it calls `CPDFSDK_FormFillEnvironment::KillFocusAnnot` as the below snip:

//

bool app::alert(CJS_Runtime* pRuntime,
                const std::vector<CJS_Value>& params,
                CJS_Value& vRet,
                CFX_WideString& sError) {
...
  pRuntime->BeginBlock();
  pFormFillEnv->KillFocusAnnot(0);
...
}

//

`CPDFSDK_FormFillEnvironment::KillFocusAnnot` calls `CPDFSDK_AnnotHandlerMgr::Annot_OnKillFocus` which calls `CPDFSDK_WidgetHandler::OnKillFocus` -> `CFFL_InteractiveFormFiller::OnKillFocus` and ends up with `CFFL_FormFiller::KillFocusForAnnot` 

//

void CFFL_FormFiller::KillFocusForAnnot(CPDFSDK_Annot* pAnnot, uint32_t nFlag) {
  if (!IsValid())
    return;

  CPDFSDK_PageView* pPageView = GetCurPageView(false);
  if (!pPageView)
    return;

  CommitData(pPageView, nFlag);
  if (CPWL_Wnd* pWnd = GetPDFWindow(pPageView, false))
    pWnd->KillFocus();
...

bool CFFL_FormFiller::CommitData(CPDFSDK_PageView* pPageView, uint32_t nFlag) {
 if (IsDataChanged(pPageView)) {
...
pFormFiller->OnValidate(&pObserved, pPageView, bRC, bExit, nFlag);
...

//

It's trying to kill the focus Annot |MyField3|, in `CommitData`, this function is responsible for committing data to a textField, because while the widget is focusing, its data may be changed. If data has been changed (we did change it from "my_field3" to "123") , it will call defined AAction of the widget (Validate && Format). I choose to inject the script at OnValidate.
```
  if(this.baseURL == "1"){
    app.alert("validate field3");
    this.removeField("MyField3");
  }
  this.baseURL="1";
```

because |removeField| calls |DeleteAnnot| later, it will free |CPDFSDK_PageView| |CPDFSDK_Widget| ...

Results in:

at |cffl_formfiller.cpp:263:24| , it tries to access violation CPDFSDK_PageView* which has been freed, UAF occurs.

Because  it triggers |OnValidate| once when its values has been changed, so I need to avoid 1st time call (by using this.baseURL), just trigger |removeField| when 2nd call happens.

Did this work before? N/A 

Chrome version: 58.0.3029.110  Channel: n/a
OS Version: OS X 10.12.5
Flash Version:

## Attachments

- [asan](attachments/asan) (text/plain, 24.0 KB)
- [test_7.pdf](attachments/test_7.pdf) (application/pdf, 3.8 KB)
- [poc.pdf](attachments/poc.pdf) (application/pdf, 2.5 KB)

## Timeline

### ma...@gmail.com (2017-06-10)

Actually, ObservePtr is been used in |CommitData|:

bool CFFL_FormFiller::CommitData(CPDFSDK_PageView* pPageView, uint32_t nFlag) {
  if (IsDataChanged(pPageView)) {
...

    pFormFiller->OnValidate(&pObserved, pPageView, bRC, bExit, nFlag);
    if (!pObserved || bExit)
      return true;

so |pObserved| will turn to null, when free-ing occurs, then `return true;`

But there is no checking afterwards, when returns to |KillFocusForAnnot|.

### ma...@gmail.com (2017-06-10)

There are also |OnCalculate| and |OnFormat| which we can run the script in there.

### ma...@gmail.com (2017-06-12)

[Comment Deleted]

### ma...@gmail.com (2017-06-12)

This is simplified POC.

### cl...@chromium.org (2017-06-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6310206941429760

### el...@chromium.org (2017-06-12)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### th...@chromium.org (2017-06-13)

I'll take a look tomorrow.

### th...@chromium.org (2017-06-13)

There's also the fun fact that CFFL_FormFiller::CommitData() always returns true. Sigh.

### th...@chromium.org (2017-06-13)

https://pdfium-review.googlesource.com/c/6530/

### es...@chromium.org (2017-06-14)

[Empty comment from Monorail migration]

### th...@chromium.org (2017-06-14)

This is XFA only. I don't think it impacts stable. CPDFSDK_PageView::DeleteAnnot() is used to trigger the free, and only exists with XFA enabled. Same for https://crbug.com/chromium/732039.

### es...@chromium.org (2017-06-14)

Thanks for the correction, thestig.

### ma...@gmail.com (2017-06-14)

[Comment Deleted]

### ma...@gmail.com (2017-06-14)

Yes, thestig is right.

Basically, it is same kind of this one https://bugs.chromium.org/p/chromium/issues/detail?id=679642.

I've been using AAction instead of C++ bindings javascript

### bu...@chromium.org (2017-06-15)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/6a3fc45b9e238d9b7b601cb13be664391d393b42

commit 6a3fc45b9e238d9b7b601cb13be664391d393b42
Author: Lei Zhang <thestig@chromium.org>
Date: Thu Jun 15 18:28:02 2017

Add more checks for destroyed annotations in CFFL_FormFiller.

CFFL_FormFiller::CommitData() should check more rigorously and so should
its callers.

BUG=chromium:732051

Change-Id: If0cee8fb61de10dc7678dad89c330d75bee55aa4
Reviewed-on: https://pdfium-review.googlesource.com/6530
Commit-Queue: dsinclair <dsinclair@chromium.org>
Reviewed-by: dsinclair <dsinclair@chromium.org>

[modify] https://crrev.com/6a3fc45b9e238d9b7b601cb13be664391d393b42/fpdfsdk/formfiller/cffl_interactiveformfiller.cpp
[modify] https://crrev.com/6a3fc45b9e238d9b7b601cb13be664391d393b42/fpdfsdk/formfiller/cffl_checkbox.cpp
[modify] https://crrev.com/6a3fc45b9e238d9b7b601cb13be664391d393b42/fpdfsdk/formfiller/cffl_formfiller.cpp
[modify] https://crrev.com/6a3fc45b9e238d9b7b601cb13be664391d393b42/fpdfsdk/formfiller/cffl_radiobutton.cpp


### th...@chromium.org (2017-06-15)

Thanks for finding more issues with PDFium's XFA code.

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

### ma...@gmail.com (2017-06-21)

Hi folks,
just noticed Security_Severity is removed. According to 679642 & 679643, I think these are worth for High severity too,  aren't they ? Just saying.

### aw...@chromium.org (2017-06-22)

Thanks for spotting! Yep, Security_Severity should still be set for Security_Impact-None bugs. Reapplying label.

### ma...@gmail.com (2017-06-22)

[Comment Deleted]

### aw...@google.com (2017-08-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-09-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-09-11)

Nice one! The VRP Panel decided to award $3,000 for this report.  Many thanks!

### aw...@chromium.org (2017-09-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-09-22)

This issue was migrated from crbug.com/chromium/732051?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088038)*
