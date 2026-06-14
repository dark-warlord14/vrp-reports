# Security: PDFium (XFA) Use-after-free in function CFDE_TextEditEngine::ReplaceSelectedText

| Field | Value |
|-------|-------|
| **Issue ID** | [40051619](https://issues.chromium.org/issues/40051619) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2020-02-25 |
| **Bounty** | $5,000.00 |

## Description

**VERSION**

Operating System: Windows 10 64bit  

Chrome with enabled XFA PDFium

**REPRODUCTION CASE**

Open file `poc.pdf` in chrome.exe  

Double-click to a edit box to select the text of this edit box and type Ctrl+V to paste and replace old text of the edit box

**VULNERABILITY DETAILS**

The bug is in function CFDE\_TextEditEngine::ReplaceSelectedText()

```
void CFDE_TextEditEngine::ReplaceSelectedText(const WideString& requested_rep) {  
  WideString rep = requested_rep;  
  
  if (delegate_) {  
    TextChange change;  
    change.selection_start = selection_.start_idx;  
    change.selection_end = selection_.start_idx + selection_.count;  
    change.text = rep;  
    change.previous_text = GetText();  
    change.cancelled = false;  
  
    delegate_->OnTextWillChange(&change);             // ==> trigger JS callback => free |this| object  
    if (change.cancelled)  
      return;  
  
    rep = change.text;  
    selection_.start_idx = change.selection_start;    // ==> use again freed object  
    selection_.count = change.selection_end - change.selection_start;  
  }  
  
  size_t start_idx = selection_.start_idx;  
  WideString txt = DeleteSelectedText(RecordOperation::kSkipRecord);  
  Insert(gap_position_, rep, RecordOperation::kSkipRecord);  
  
  AddOperationRecord(  
      pdfium::MakeUnique<ReplaceOperation>(this, start_idx, txt, rep));  
}  

```

We can trigger JS callback when function `OnTextWillChange()` is called. By setting up `change` event for a text edit  

field like this

```
  <field name="choiceList1" h="200mm" w="200mm" x="1mm" y="1mm">  
    <ui>  
      <textEdit/>  
    </ui>  
    <value>  
      <text>pdfium</text>  
    </value>  
    <event activity="change">  
      <script contentType="application/x-javascript">  
        change_count += 1;  
        if (change_count == 2)  
        {  
            f1 = xfa.resolveNode("xfa.form..choiceList0");  
            xfa.host.setFocus(f1);  
            xfa.template.remerge();  
            xfa.host.openList(f1);  
        }  
      </script>  
    </event>  
  </field>  

```

This JS code in 'change' event will be executed when command `delegate_->OnTextWillChange(&change);`  is executed  

and it'll free the object `CXFA_FFTextEdit`. This leads to `CFWL_Edit` object is freed => finally leads to  

`CFDE_TextEditEngine` object is freed.

After JS event handler, it backs to function `CFDE_TextEditEngine::ReplaceSelectedText()`, the object will be used again  

by instruction that accesses to class `CFDE_TextEditEngine`'s field |selection\_|.

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 6.4 KB)
- [log_crash.txt](attachments/log_crash.txt) (text/plain, 16.6 KB)

## Timeline

### va...@chromium.org (2020-02-26)

Security_Impact-None: Requires XFA

[Monorail components: Internals>Plugins>PDF]

### [Deleted User] (2020-02-26)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-03-04)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/bdfec55676eb4e8e6a78c711dca8be6e8a7872f1

commit bdfec55676eb4e8e6a78c711dca8be6e8a7872f1
Author: Tom Sepez <tsepez@chromium.org>
Date: Wed Mar 04 17:49:35 2020

Retain layout item in a few more places where text changes.

Although these methods are not explicitly called On*(), they have
the same inplications for triggering callbacks.

Bug: chromium:1055869
Change-Id: I6bb8f31bf94cf414e14b09201a3f58340b260866
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/67170
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/bdfec55676eb4e8e6a78c711dca8be6e8a7872f1/fpdfsdk/fpdf_formfill_embeddertest.cpp
[add] https://pdfium.googlesource.com/pdfium/+/bdfec55676eb4e8e6a78c711dca8be6e8a7872f1/testing/resources/bug_1055869.in
[modify] https://pdfium.googlesource.com/pdfium/+/bdfec55676eb4e8e6a78c711dca8be6e8a7872f1/xfa/fxfa/cxfa_fftextedit.h
[modify] https://pdfium.googlesource.com/pdfium/+/bdfec55676eb4e8e6a78c711dca8be6e8a7872f1/xfa/fxfa/cxfa_ffwidget.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/bdfec55676eb4e8e6a78c711dca8be6e8a7872f1/xfa/fxfa/cxfa_ffwidget.h
[modify] https://pdfium.googlesource.com/pdfium/+/bdfec55676eb4e8e6a78c711dca8be6e8a7872f1/xfa/fxfa/cxfa_fftextedit.cpp
[add] https://pdfium.googlesource.com/pdfium/+/bdfec55676eb4e8e6a78c711dca8be6e8a7872f1/testing/resources/bug_1055869.pdf


### ts...@chromium.org (2020-03-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-04)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-03-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/dc9689a6738e7dd7e2ee93dad052c1e07abdad48

commit dc9689a6738e7dd7e2ee93dad052c1e07abdad48
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Mar 05 23:04:59 2020

Roll src/third_party/pdfium a40862f237fc..8ecb862ae74d (5 commits)

https://pdfium.googlesource.com/pdfium.git/+log/a40862f237fc..8ecb862ae74d

git log a40862f237fc..8ecb862ae74d --date=short --first-parent --format='%ad %ae %s'
2020-03-05 tsepez@chromium.org Retain layout item in all CFXA_FF.*::Paste() method overrides.
2020-03-05 nigi@chromium.org Add FXSYS_IsLowerASCII().
2020-03-05 nigi@chromium.org Add a caller for FXSYS_ToUpperASCII() to simplify code.
2020-03-04 tsepez@chromium.org Retain layout item in a few more places where text changes.
2020-03-04 nigi@chromium.org Add FXSYS_IsUpperASCII().

Created with:
  gclient setdep -r src/third_party/pdfium@8ecb862ae74d

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:1055869,chromium:1058653
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I221c2f725aa0dce901bf6c3c8f2fd91c0aea28a3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2090223
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#747461}

[modify] https://crrev.com/dc9689a6738e7dd7e2ee93dad052c1e07abdad48/DEPS


### na...@google.com (2020-03-09)

[Empty comment from Monorail migration]

### na...@google.com (2020-03-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-03-11)

Congrats! The Panel decided to award $5,000 for this report!

### na...@google.com (2020-03-11)

[Empty comment from Monorail migration]

### [Deleted User] (2020-06-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-06-10)

This issue was migrated from crbug.com/chromium/1055869?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051619)*
