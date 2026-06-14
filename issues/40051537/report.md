# Security: PDFium (XFA) Use-after-free in CXFA_FFTextEdit::UpdateFWLData

| Field | Value |
|-------|-------|
| **Issue ID** | [40051537](https://issues.chromium.org/issues/40051537) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2020-02-17 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

CXFA\_FFTextEdit object use-after-free in function CXFA\_FFTextEdit::UpdateFWLData

**VERSION**  

Operating System: Windows 10 64bit  

Chrome with enabled XFA PDFium

**REPRODUCTION CASE**  

Open file `poc.pdf` in chrome.exe

DETAIL INFORMATION

The bug is in function CXFA\_FFTextEdit::UpdateFWLData()

```
bool CXFA_FFTextEdit::UpdateFWLData() {  
  if (!GetNormalWidget())  
    return false;  
  
  CFWL_Edit\* pEdit = ToEdit(GetNormalWidget());  
  XFA_VALUEPICTURE eType = XFA_VALUEPICTURE_Display;  
  if (IsFocused())  
    eType = XFA_VALUEPICTURE_Edit;  
  
...  
  WideString wsText = m_pNode->GetValue(eType);  
  WideString wsOldText = pEdit->GetText();  
  if (wsText != wsOldText || (eType == XFA_VALUEPICTURE_Edit && bUpdate)) {  
    pEdit->SetTextSkipNotify(wsText);       // ==>  callback to JS function by using `full` event  
                                            // ==> free |this| object in JS callback function  
    bUpdate = true;  
  }  
  if (bUpdate)  
    GetNormalWidget()->Update();            // ==> |this| object is used after is freed in JS callback!  
  
  return true;  
}  

```

We can trigger JS callback when function `pEdit->SetTextSkipNotify()` is called. By setting up `full` event  

for a `textEdit` field like this

```
<field name="choiceList1" h="10mm" w="1mm" x="5mm" y="50mm">  
  <ui>  
    <textEdit hScrollPolicy="off" vScrollPolicy="off" multiLine="0"/>  
  </ui>  
  <value>  
    <text maxChars="6">pdfium</text>  
  </value>  
  <event activity="full">  
    <script contentType="application/x-javascript">  
      full_count += 1;  
      if (full_count == 2)  
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

This JS code in 'full' event will be executed when command `pEdit->SetTextSkipNotify()` is executed  

and it'll free the object CXFA\_FFTextEdit.

After JS event handler, it backs to function `CXFA_FFTextEdit::UpdateFWLData()`, the object will be used again in  

function `CXFA_FFField::GetNormalWidget()`.

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 9.0 KB)
- [log_crash.txt](attachments/log_crash.txt) (text/plain, 27.9 KB)

## Timeline

### rs...@chromium.org (2020-02-17)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### rs...@chromium.org (2020-02-17)

Tom: AFAICT, XFA is disabled for Chromium, so I'm not sure I've got the Severity set correctly, or if we even treat it as a security bug? However, I'm guessing the fact that we've got the build option means someone might set the build flags.

Are you good to check out the XFA issues? I didn't see a more specific OWNERS file.

### rs...@chromium.org (2020-02-17)

[Empty comment from Monorail migration]

### ts...@chromium.org (2020-02-18)

Yes, XFA=> Sev High, Impact None.  Thanks!

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-19)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/d15d718e8d5e8d664454625f2b0c51ed71a2b10e

commit d15d718e8d5e8d664454625f2b0c51ed71a2b10e
Author: Tom Sepez <tsepez@chromium.org>
Date: Wed Feb 19 22:12:51 2020

Protect owning layout item in all UpdateFWLData() overrides.

Also observe |this| in CFWL_DateTimePicker::SetEditText() and
ProcessSelChanged().

Bug: chromium:1053617,chromium:1052786,chromium:1040329
Change-Id: Icb4afcd7e5432787668355102b3b36faf5572894
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/66630
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/d15d718e8d5e8d664454625f2b0c51ed71a2b10e/xfa/fxfa/cxfa_fflistbox.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/d15d718e8d5e8d664454625f2b0c51ed71a2b10e/xfa/fxfa/cxfa_ffcheckbutton.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/d15d718e8d5e8d664454625f2b0c51ed71a2b10e/xfa/fwl/cfwl_datetimepicker.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/d15d718e8d5e8d664454625f2b0c51ed71a2b10e/xfa/fxfa/cxfa_fftextedit.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/d15d718e8d5e8d664454625f2b0c51ed71a2b10e/xfa/fxfa/cxfa_ffdatetimeedit.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/d15d718e8d5e8d664454625f2b0c51ed71a2b10e/xfa/fxfa/cxfa_ffcombobox.cpp


### ts...@chromium.org (2020-02-19)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/eca24f9ecc907c4bfd7a4a2ce36b4ac863155066

commit eca24f9ecc907c4bfd7a4a2ce36b4ac863155066
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Feb 20 00:35:24 2020

Roll src/third_party/pdfium 1217cd17daba..d15d718e8d5e (5 commits)

https://pdfium.googlesource.com/pdfium.git/+log/1217cd17daba..d15d718e8d5e

git log 1217cd17daba..d15d718e8d5e --date=short --first-parent --format='%ad %ae %s'
2020-02-19 tsepez@chromium.org Protect owning layout item in all UpdateFWLData() overrides.
2020-02-19 nigi@chromium.org Roll third_party/binutils/ 01aa7745b..ffd1fdb90 (1 commit)
2020-02-19 nigi@chromium.org Roll tools/memory/ f7b00daf4..89552acb6 (1 commit)
2020-02-19 nigi@chromium.org Roll third_party/instrumented_libraries/ 4dca59c6a..bb3f1802c (1 commit)
2020-02-19 tsepez@chromium.org Pass spans to UTF8Decode() in cfx_seekablestreamproxy.cpp

Created with:
  gclient setdep -r src/third_party/pdfium@d15d718e8d5e

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:1040329,chromium:1052786,chromium:1053617
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I38b0499a67c4f681302621455ddd7dca9011c4ea
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2065391
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#742885}

[modify] https://crrev.com/eca24f9ecc907c4bfd7a4a2ce36b4ac863155066/DEPS


### [Deleted User] (2020-02-20)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-24)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-02-27)

Congrats the Panel decided to award $7,500 for this report!

### na...@google.com (2020-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-05-28)

This issue was migrated from crbug.com/chromium/1052786?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051537)*
