# Security: Use-After-Free in chrome_pdf::PdfViewWebPlugin::PrintEnd

| Field | Value |
|-------|-------|
| **Issue ID** | [40930463](https://issues.chromium.org/issues/40930463) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Printing |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | pw...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2023-09-10 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

Use-After-Free in PDF printing

**VERSION**  

Chrome Version: 116.0.5845.179 (Official Build) (arm64)  

Operating System: MacOS 13.4.1 (c) (22F770820d)

**REPRODUCTION CASE**

1. Open the "poc.pdf" file.
2. Click the "Print" button.
3. Open the Inspector and navigate to the "Performance" tab.
4. Click the "Reload" button.

**CREDIT INFORMATION**  

Reporter credit: [pwn2car]

## Attachments

- [repro.mov](attachments/repro.mov) (video/quicktime, 9.0 MB)
- [poc.pdf](attachments/poc.pdf) (application/pdf, 90.4 KB)
- [asan.log](attachments/asan.log) (text/plain, 20.8 KB)

## Timeline

### [Deleted User] (2023-09-10)

[Empty comment from Monorail migration]

### th...@chromium.org (2023-09-11)

[Empty comment from Monorail migration]

[Monorail components: Internals>Printing]

### th...@chromium.org (2023-09-11)

I can repro this locally. Waiting for security triage to do the initial triage though.

### th...@chromium.org (2023-09-11)

FWIW, there is a known crash in PdfViewWebPlugin::PrintEnd() in https://crbug.com/chromium/1297625. Though there is no known repro for that bug.

### th...@chromium.org (2023-09-11)

Also, there's nothing special about poc.pdf. Likely printing any PDF can trigger this issue by following the steps and reloading in Devtools.

### th...@chromium.org (2023-09-11)

Normally, there is a PrintPreviewUI::SetInitialParams() call that sets a few values in PrintPreviewUI. The unexpected reload via Devtools does not trigger the PrintPreviewUI::SetInitialParams() call, and then the browser sends the renderer the wrong print parameters, and the renderer misbehaves.

It would be interesting to know if there's a way to trigger with without Devtools. As-is, there are many ways one can use Devtools to mess with chrome://print and trigger unexpected behavior. Since chrome:// URLs are privledged WebUI surfaces, doing changes to it via Devtools is like a user-friendly way of modifying some browser process's in-memory values.

### th...@chromium.org (2023-09-12)

Created a fix: https://crrev.com/c/4857212

### li...@chromium.org (2023-09-12)

Thanks for repro-ing this and starting on a fix, I'm going to assign this to you since you have a fix out already.
I confirmed I can also repro this locally..

Going to mark this as medium severity for now since it does look like a victim would have to use Devtools to trigger this.



### [Deleted User] (2023-09-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-12)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2023-09-12)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-09-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/79fc6aa09e7c3c502fb15befac2a140b65672888

commit 79fc6aa09e7c3c502fb15befac2a140b65672888
Author: Lei Zhang <thestig@chromium.org>
Date: Wed Sep 13 05:37:27 2023

Stop storing Print Preview request data in PrintPreviewUI

Since the Print Preview UI can be reloaded in some rare cases, the
PrintPreviewUI instance that runs the UI can get destroyed and
recreated. If this happens, PrintPreviewUI will lose track of some
values and hand out potentially incorrect values.

Prevent this situation from happening by storing the Print Preview
request data in PrintPreviewDialogController instead. Divert all data
getters/setters to use the new data source. PrintPreviewDialogController
already keeps track of all print preview requests, and it is immune to
Print Preview UI reloads.

To keep the existing PrintPreviewHandlerTest working, add some test-only
calls to (dis)associate WebContentses, as the test manually creates its
own.

To keep tests that navigate directly to chrome://print working, allow
PrintPreviewHandler to use dummy request data when
PrintPreviewDialogController does not know about the Print Preview.

Do some cleanups along the way, to tidy things up. In particular,
avoid including Print Preview headers when Print Preview is not
available.

Bug: 1480852
Change-Id: I47754f769a143a9fcd5794144106cd6351e51d0f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4857212
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
Reviewed-by: Alan Screen <awscreen@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1195813}

[modify] https://crrev.com/79fc6aa09e7c3c502fb15befac2a140b65672888/chrome/browser/printing/print_test_utils.cc
[modify] https://crrev.com/79fc6aa09e7c3c502fb15befac2a140b65672888/chrome/browser/ui/blocked_content/popup_blocker_browsertest.cc
[modify] https://crrev.com/79fc6aa09e7c3c502fb15befac2a140b65672888/chrome/browser/printing/print_preview_dialog_controller.h
[modify] https://crrev.com/79fc6aa09e7c3c502fb15befac2a140b65672888/chrome/browser/ui/webui/print_preview/print_preview_handler.h
[modify] https://crrev.com/79fc6aa09e7c3c502fb15befac2a140b65672888/chrome/browser/printing/print_test_utils.h
[modify] https://crrev.com/79fc6aa09e7c3c502fb15befac2a140b65672888/chrome/browser/printing/print_preview_dialog_controller.cc
[modify] https://crrev.com/79fc6aa09e7c3c502fb15befac2a140b65672888/chrome/browser/ui/webui/print_preview/print_preview_ui.h
[modify] https://crrev.com/79fc6aa09e7c3c502fb15befac2a140b65672888/chrome/browser/ui/webui/print_preview/print_preview_handler.cc
[modify] https://crrev.com/79fc6aa09e7c3c502fb15befac2a140b65672888/chrome/test/BUILD.gn
[modify] https://crrev.com/79fc6aa09e7c3c502fb15befac2a140b65672888/chrome/browser/printing/print_view_manager.cc
[modify] https://crrev.com/79fc6aa09e7c3c502fb15befac2a140b65672888/chrome/browser/browser_process_impl.cc
[modify] https://crrev.com/79fc6aa09e7c3c502fb15befac2a140b65672888/chrome/browser/BUILD.gn
[modify] https://crrev.com/79fc6aa09e7c3c502fb15befac2a140b65672888/chrome/browser/ui/webui/print_preview/print_preview_ui.cc
[modify] https://crrev.com/79fc6aa09e7c3c502fb15befac2a140b65672888/chrome/browser/ui/webui/print_preview/print_preview_handler_unittest.cc


### th...@chromium.org (2023-09-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-19)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2023-09-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-21)

Congratulations, pwn2car! The Chrome VRP Panel has decided to award you $2,000 for this report of a moderately mitigated security bug in a sandboxed process. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-09-22)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-30)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-01)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-01)

[Empty comment from Monorail migration]

### na...@google.com (2023-11-01)

[Empty comment from Monorail migration]

### na...@google.com (2023-11-01)

[Empty comment from Monorail migration]

### vo...@google.com (2023-11-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-09)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vo...@google.com (2023-11-09)

1. one https://crrev.com/c/4999725
2. Medium - medium size change with several conflicts
3. Not merged anywhere, first landed in M119
4. Yes

### gm...@google.com (2023-11-14)

[Empty comment from Monorail migration]

### na...@google.com (2023-12-11)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-12-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0f361f3dcc64883f3d4bff5a51affbe450e2ce97

commit 0f361f3dcc64883f3d4bff5a51affbe450e2ce97
Author: Zakhar Voit <voit@google.com>
Date: Thu Dec 14 12:33:06 2023

[M114-LTS] Stop storing Print Preview request data in PrintPreviewUI

M114 conflict resolution:
- Include SetProfileForInitialSettings for all platforms (not just lacros)
- Fix namespaces and includes in print_test_utils
- Get rid of dialog_controller singleton access in print_manager

Since the Print Preview UI can be reloaded in some rare cases, the
PrintPreviewUI instance that runs the UI can get destroyed and
recreated. If this happens, PrintPreviewUI will lose track of some
values and hand out potentially incorrect values.

Prevent this situation from happening by storing the Print Preview
request data in PrintPreviewDialogController instead. Divert all data
getters/setters to use the new data source. PrintPreviewDialogController
already keeps track of all print preview requests, and it is immune to
Print Preview UI reloads.

To keep the existing PrintPreviewHandlerTest working, add some test-only
calls to (dis)associate WebContentses, as the test manually creates its
own.

To keep tests that navigate directly to chrome://print working, allow
PrintPreviewHandler to use dummy request data when
PrintPreviewDialogController does not know about the Print Preview.

Do some cleanups along the way, to tidy things up. In particular,
avoid including Print Preview headers when Print Preview is not
available.

(cherry picked from commit 79fc6aa09e7c3c502fb15befac2a140b65672888)

Bug: 1480852
Change-Id: I47754f769a143a9fcd5794144106cd6351e51d0f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4857212
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
Commit-Queue: Lei Zhang <thestig@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1195813}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4999725
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Zakhar Voit <voit@google.com>
Owners-Override: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/5735@{#1650}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/0f361f3dcc64883f3d4bff5a51affbe450e2ce97/chrome/browser/printing/print_test_utils.cc
[modify] https://crrev.com/0f361f3dcc64883f3d4bff5a51affbe450e2ce97/chrome/browser/ui/blocked_content/popup_blocker_browsertest.cc
[modify] https://crrev.com/0f361f3dcc64883f3d4bff5a51affbe450e2ce97/chrome/browser/printing/print_preview_dialog_controller.h
[modify] https://crrev.com/0f361f3dcc64883f3d4bff5a51affbe450e2ce97/chrome/browser/ui/webui/print_preview/print_preview_handler.h
[modify] https://crrev.com/0f361f3dcc64883f3d4bff5a51affbe450e2ce97/chrome/browser/printing/print_test_utils.h
[modify] https://crrev.com/0f361f3dcc64883f3d4bff5a51affbe450e2ce97/chrome/browser/printing/print_preview_dialog_controller.cc
[modify] https://crrev.com/0f361f3dcc64883f3d4bff5a51affbe450e2ce97/chrome/browser/ui/webui/print_preview/print_preview_ui.h
[modify] https://crrev.com/0f361f3dcc64883f3d4bff5a51affbe450e2ce97/chrome/browser/ui/webui/print_preview/print_preview_handler.cc
[modify] https://crrev.com/0f361f3dcc64883f3d4bff5a51affbe450e2ce97/chrome/test/BUILD.gn
[modify] https://crrev.com/0f361f3dcc64883f3d4bff5a51affbe450e2ce97/chrome/browser/printing/print_view_manager.cc
[modify] https://crrev.com/0f361f3dcc64883f3d4bff5a51affbe450e2ce97/chrome/browser/browser_process_impl.cc
[modify] https://crrev.com/0f361f3dcc64883f3d4bff5a51affbe450e2ce97/chrome/browser/BUILD.gn
[modify] https://crrev.com/0f361f3dcc64883f3d4bff5a51affbe450e2ce97/chrome/browser/ui/webui/print_preview/print_preview_ui.cc
[modify] https://crrev.com/0f361f3dcc64883f3d4bff5a51affbe450e2ce97/chrome/browser/ui/webui/print_preview/print_preview_handler_unittest.cc


### vo...@google.com (2023-12-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1480852?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40930463)*
