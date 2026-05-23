# Security: Use-after-free in Field::UpdateFormControl

| Field | Value |
|-------|-------|
| **Issue ID** | [40089224](https://issues.chromium.org/issues/40089224) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | hu...@gmail.com |
| **Assignee** | rh...@chromium.org |
| **Created** | 2017-10-05 |
| **Bounty** | $3,000.00 |

## Description

VULNERABILITY DETAILS
Use-after-free in Field::UpdateFormControl

VERSION
Operating System: Windows 10
PDFium with XFA enabled

Steps to reproduce the problem:
1. Build PDFIUm with XFA
2. run ./pdfium_test ./poc.pdf

Details

In function `Field::UpdateFormControl`, there is a call to `pWidget->OnFormat`

void Field::UpdateFormControl(CPDFSDK_FormFillEnvironment* pFormFillEnv,
                              CPDF_FormControl* pFormControl,
                              bool bChangeMark,
                              bool bResetAP,
                              bool bRefresh) {
...
  if (pWidget) {
    if (bResetAP) {
      int nFieldType = pWidget->GetFieldType();
      if (nFieldType == FIELDTYPE_COMBOBOX ||
          nFieldType == FIELDTYPE_TEXTFIELD) {
        bool bFormatted = false;
        CFX_WideString sValue = pWidget->OnFormat(bFormatted);			<--- call to JS script 
        pWidget->ResetAppearance(bFormatted ? &sValue : nullptr, false);
      } else {
        pWidget->ResetAppearance(nullptr, false);
      }
    }
...

This function `pWidget->OnFormat` call to JS script that set for handler format action of a field. If in this JS script, i remove that field with JS function `removeField`, it will free object `pWidget`. After that, object `pWidget` is used again (after be freed) in `pWidget->ResetAppearance(bFormatted ? &sValue : nullptr, false);` ==> so it's a use-after-free bug!

To trigger `Field::UpdateFormControl`, I use function `Field::lineWidth` (by using JS Field property `lineWidth`). In property setting `lineWidth` function `Field::SetLineWidth`

void Field::SetLineWidth(CPDFSDK_FormFillEnvironment* pFormFillEnv,
                         const WideString& swFieldName,
                         int nControlIndex,
                         int number) {
  CPDFSDK_InterForm* pInterForm = pFormFillEnv->GetInterForm();
  std::vector<CPDF_FormField*> FieldArray =
      GetFormFields(pFormFillEnv, swFieldName);
  for (CPDF_FormField* pFormField : FieldArray) {
    if (nControlIndex < 0) {
	...
    } else {
      if (nControlIndex >= pFormField->CountControls())
        return;
      if (CPDF_FormControl* pFormControl =
              pFormField->GetControl(nControlIndex)) {
        if (CPDFSDK_Widget* pWidget = pInterForm->GetWidget(pFormControl)) {
          if (number != pWidget->GetBorderWidth()) {
            pWidget->SetBorderWidth(number);
            UpdateFormControl(pFormFillEnv, pFormControl, true, true, true);
          }
        }
      }
    }
  }
}	

To get a call to `UpdateFormControl`, we need `nControlIndex` >= 0. From the function `Field::lineWidth`, we know `nControlIndex` is `m_nFormControlIndex` 


bool Field::lineWidth(CJS_Runtime* pRuntime,
                      CJS_PropValue& vp,
                      WideString& sError) {
...
    if (m_bDelay) {
      AddDelay_Int(FP_LINEWIDTH, iWidth);
    } else {
      Field::SetLineWidth(m_pFormFillEnv.Get(), m_FieldName,
                          m_nFormControlIndex, iWidth);
...					  


==> so we need to choose a field that has `m_nFormControlIndex` >= 0

In my poc, i have a text field with name `Calc1_Rslt`. This field has 2 child fields that have the same name `Calc1_Rslt_Sub1`. With this setup, when i get the parent field with command `ff = this.getField('Calc1_Rslt.Calc1_Rslt_Sub1..1')`, the `ff` object is the Field object with `m_nFormControlIndex` > 0

In the end, i setup 2 format actions for 2 fields: parent field `Calc1_Rslt` and child field `Calc1_Rslt_Sub1` with this JS code 

app.alert('[begin] format ... ')
this.aaa += 1;
if (this.aaa == 3)
{
    app.alert('[inside] format ... ')
    this.removeField("Calc1_Rslt.Calc1_Rslt_Sub1")
    this.removeField("Calc1_Rslt")
    //gc
    app.alert('=================== GC')
    tmp = [];
    for (var i = 0; i < 0x200000; i++)
    {
        tmp.push(new Uint8Array(10));
    }
    tmp = null;
}


Run the attachment pdf file with `pdfium_test`, we get a use-after-free crash.



## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 512.0 KB)
- [stacktrace.txt](attachments/stacktrace.txt) (text/plain, 7.3 KB)

## Timeline

### el...@chromium.org (2017-10-05)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### oc...@chromium.org (2017-10-05)

rharrison, could you please take a look at this?

### ds...@chromium.org (2017-10-05)

Just to be clear, this only reproduces with XFA enabled correct?

### rh...@chromium.org (2017-10-05)

I have confirmed the PoC only works with XFA enabled.

### cl...@chromium.org (2017-10-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6543708379152384.

### ds...@chromium.org (2017-10-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-10-05)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/569817cfffe7410765c97c6deebef3a795bac0f6

commit 569817cfffe7410765c97c6deebef3a795bac0f6
Author: Ryan Harrison <rharrison@chromium.org>
Date: Thu Oct 05 18:41:55 2017

Add ObservedPtr to catch Widget being killed by JS

Another case of a call causing JS to run, which can remove a widget
that is called later.

BUG=chromium:771979

Change-Id: I5f25a38097662b70cfb777f76f0e3d50e7c11b1b
Reviewed-on: https://pdfium-review.googlesource.com/15610
Commit-Queue: Ryan Harrison <rharrison@chromium.org>
Reviewed-by: Henrique Nakashima <hnakashima@chromium.org>

[modify] https://crrev.com/569817cfffe7410765c97c6deebef3a795bac0f6/fpdfsdk/javascript/Field.cpp


### rh...@chromium.org (2017-10-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-10-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d4e1b8bcc5cfd9038eb81b4d5d79b724d505c0c2

commit d4e1b8bcc5cfd9038eb81b4d5d79b724d505c0c2
Author: pdfium-deps-roller@chromium.org <pdfium-deps-roller@chromium.org>
Date: Thu Oct 05 21:06:24 2017

Roll src/third_party/pdfium/ 4ce4f5f8a..480ca10f7 (12 commits)

https://pdfium.googlesource.com/pdfium.git/+log/4ce4f5f8ab0b..480ca10f7a20

$ git log 4ce4f5f8a..480ca10f7 --date=short --no-merges --format='%ad %ae %s'
2017-10-05 dsinclair Remove unused CPVT_SecProps
2017-10-05 dsinclair Remove more unused params
2017-10-05 dsinclair Remove unused parameters
2017-10-05 rharrison Add ObservedPtr to catch Widget being killed by JS
2017-10-05 rharrison Add ObservedPtrs to catch issues in SaveData
2017-10-05 npm Create FreeType roll script
2017-10-04 rharrison Make GIF decoder more standards complaint
2017-10-05 dsinclair Move CPDF_RenderOptions members to private
2017-10-05 dsinclair Remove friend from CPDF_ApSettings
2017-10-05 npm Roll FT to ae7dc1f62d826083d418e86cce3f66a76dff038a
2017-10-05 dsinclair Remove friends from form code
2017-10-05 dsinclair Remove friends from CPDF_VariableText

Created with:
  roll-dep src/third_party/pdfium
BUG=771979,756427,770337


Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, see:
http://www.chromium.org/developers/tree-sheriffs/sheriff-details-chromium#TOC-Failures-due-to-DEPS-rolls


TBR=dsinclair@chromium.org

Change-Id: I875e810e00b7d619534e2dc24519c27088423e15
Reviewed-on: https://chromium-review.googlesource.com/703198
Reviewed-by: <pdfium-deps-roller@chromium.org>
Commit-Queue: <pdfium-deps-roller@chromium.org>
Cr-Commit-Position: refs/heads/master@{#506857}
[modify] https://crrev.com/d4e1b8bcc5cfd9038eb81b4d5d79b724d505c0c2/DEPS


### sh...@chromium.org (2017-10-06)

[Empty comment from Monorail migration]

### hu...@gmail.com (2018-01-05)

Hi guys, 

I just wonder this report is elegant for your bug bounty program? 

Thank you! 

### ds...@chromium.org (2018-01-08)

[Empty comment from Monorail migration]

### aw...@google.com (2018-01-08)

Sending to the panel for consideration.

### sh...@chromium.org (2018-01-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-01-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-01-22)

Congratulations huyna89@, the VRP Panel has decided to award $3,000 for this report. A member of our finance team will be in touch shortly to arrange payment. Also, how would you like to be credited in our release notes?

### aw...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### hu...@gmail.com (2018-01-24)

Hi awhalley,  

Thank you for the reward. You can credit as "huyna at Viettel Cyber Security".   

### is...@google.com (2018-01-24)

This issue was migrated from crbug.com/chromium/771979?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/62400]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089224)*
