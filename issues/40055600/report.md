# Security: Double-free when extension is uninstalled while uninstall dialog is being shown

| Field | Value |
|-------|-------|
| **Issue ID** | [40055600](https://issues.chromium.org/issues/40055600) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | rd...@chromium.org |
| **Created** | 2021-04-20 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

When the user selects the "Remove from Chrome..." option from an extension's context menu, an uninstall dialog will be shown. If the extension is uninstalled while the dialog is being shown (e.g. because the extension uninstalls itself), a double-free will occur in the browser process.

**VERSION**  

Chrome Version: Tested on 92.0.4484.0 (latest asan build)  

Operating System: Windows 10, version 20H2

**REPRODUCTION CASE**

1. Install the attached extension.
2. Once installed, the extension will open page.html in a new tab. Once this has happened, click anywhere on the page.
3. From the extensions toolbar, bring up the context menu for the extension, then select the "Remove from Chrome..." option. Leave the uninstall dialog open.
4. Ten seconds after being clicked, page.html will uninstall the extension using chrome.management.uninstallSelf. This will result in a double-free in the browser process, which you can verify by going through these steps in an asan build.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [asan_output_874108.txt](attachments/asan_output_874108.txt) (text/plain, 12.4 KB)
- [background.js](attachments/background.js) (text/plain, 39 B)
- manifest.json (text/plain, 169 B)
- page.html (text/plain, 98 B)
- page.js (text/plain, 135 B)

## Timeline

### [Deleted User] (2021-04-20)

[Empty comment from Monorail migration]

### de...@gmail.com (2021-04-20)

The issue here is that the UninstallDialogHelper instance is freed twice.

The first time is when the extension is uninstalled and ExtensionUninstallDialog::OnExtensionUninstalled is called, which calls UninstallDialogHelper::OnExtensionUninstallDialogClosed. That method then calls "delete this":

https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/extensions/extension_context_menu_model.cc;l=181;drc=924f8039f6896058207961afaa2ee56550be817c

The second is when the UninstallDialogHelper instance is deleted and the corresponding view is destroyed. That results in a call to BubbleDialogModelHost::Close, which ultimately results in another call to UninstallDialogHelper::OnExtensionUninstallDialogClosed, which deletes the instance for a second time.

### ca...@chromium.org (2021-04-21)

Triaging as medium severity due to the extended user interaction required.

rdevlin.cronin: Can you help find a good owner for this bug? Thanks.

[Monorail components: Platform>Extensions]

### rd...@chromium.org (2021-04-21)

Thank you for the report!

ghazale@, do you have the bandwidth to take a look at this one?  karandeepb@, do you think you can help ghazale@ with a couple pointers here?  (Feel free to ping me if you have any questions!)

### gh...@chromium.org (2021-04-21)

rdevlin.cronin@ Yes, I will work on it. Thanks!

### gh...@chromium.org (2021-04-21)

rdevlin.cronin@ I followed https://chromium.googlesource.com/chromium/src/+/master/docs/asan.md and build asan. But I do not see any logs when reproducing the bug. These are my build variables:

use_goma = true            # Googlers: Use build farm, compiles faster.
is_asan = true
is_debug = false           # Release build, runs faster.
enable_full_stack_frames_for_profiling = true
 
Am I missing a variable?

### [Deleted User] (2021-04-21)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ka...@chromium.org (2021-04-21)

Re c#6, I think as long as you can verify that the asan build is working by running a test (as referenced at https://chromium.googlesource.com/chromium/src/+/master/docs/asan.md), you have most likely set up the build environment correctly.

Another thing to try would be to add logging statements to the code paths indicated in c#2 to verify that you are repro-ing correctly.

### [Deleted User] (2021-05-05)

ghazale: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gh...@chromium.org (2021-05-05)

[Empty comment from Monorail migration]

### rd...@chromium.org (2021-05-06)

I think that ExtensionUninstaller here [1] has the potential for an almost-identical UAF.  We should fix both in this bug, if we can.

[1] https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/apps/app_service/extension_uninstaller.cc;l=21-52;drc=f27844b66622d607944c54ec9021e896d6dc823a

### gh...@chromium.org (2021-05-11)

[Empty comment from Monorail migration]

### rd...@chromium.org (2021-05-17)

ghazale@ is out this week, so I'll take this on to make sure we get a fix in before branch.

### gi...@appspot.gserviceaccount.com (2021-05-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e7cc11190df75100a775ca4c7215022a275cc094

commit e7cc11190df75100a775ca4c7215022a275cc094
Author: Devlin Cronin <rdevlin.cronin@chromium.org>
Date: Tue May 18 01:20:42 2021

[Extensions] Fix duplicate call of OnExtensionUninstallDialogClosed()

ExtensionUninstallDialog could call OnExtensionUninstallDialogClosed()
twice if the extension was uninstalled while the dialog was showing:
- Once in response to OnExtensionUninstalled(), and
- Again in response to the dialog closing.

In addition to this being wrong, it can cause lifetime issues since
the delegate on which OnExtensionUninstallDialogClosed() was called
could be deleted after it was notified of the dialog closing.

Fix this by closing the dialog programmatically in response to
OnExtensionUninstalled(). This results in OnDialogClosed() being
called and the delegate being properly notified, but ensures that the
OnExtensionUninstallDialogClosed() method is only called once.

Add a regression test as well.

Bug: 1200679
Change-Id: I0f874eb1d3419755de794d820ba84dda35179627
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2901617
Reviewed-by: Peter Boström <pbos@chromium.org>
Commit-Queue: Devlin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#883744}

[modify] https://crrev.com/e7cc11190df75100a775ca4c7215022a275cc094/chrome/browser/extensions/extension_uninstall_dialog.cc
[modify] https://crrev.com/e7cc11190df75100a775ca4c7215022a275cc094/chrome/browser/extensions/extension_uninstall_dialog.h
[modify] https://crrev.com/e7cc11190df75100a775ca4c7215022a275cc094/chrome/browser/ui/views/extensions/extension_uninstall_dialog_view.cc
[modify] https://crrev.com/e7cc11190df75100a775ca4c7215022a275cc094/chrome/browser/ui/views/extensions/extension_uninstall_dialog_view_browsertest.cc


### rd...@chromium.org (2021-05-18)

This should be fixed by c#14.  I've confirmed locally that running an ASAN build and having the extension uninstall itself while the dialog is being shown now doesn't crash (and just closes the uninstall dialog).  derceg86@, please feel free to verify as well! : )

Since this is a security bug, we'll probably want to merge this to 91.  We'll want this to bake for an extra day or so (as a sanity check), but I think the change is fairly safe.  Pre-emptively requesting merge to start the process, since 91 goes to stable soon.

### [Deleted User] (2021-05-18)

This bug requires manual review: We are only 6 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rd...@chromium.org (2021-05-18)

1) Yes
2) https://chromium-review.googlesource.com/c/chromium/src/+/2901617
3) Yes, but we can give it another day to bake before merging
4) I think probably just 91, given the current release schedule (CL landed in 92).  Potentially we could merge to 90, but I don't think it's worth it at this stage.
5) Security fix
6) No
7) N/A


### [Deleted User] (2021-05-18)

[Empty comment from Monorail migration]

### ad...@google.com (2021-05-18)

Per https://crbug.com/chromium/1200679#c14 this may be a browser process UaF, but as it's mitigated by UI gestures and the need for an extension I think it's reasonable to stick with the existing medium severity. As such, let's not rush to approve this merge into M91 for the stable cut today. It can land in the first security refresh. I'll approve merge to M91 at a suitable time for that refresh.

### rd...@chromium.org (2021-05-18)

One clarification:

> but as it's mitigated by UI gestures and the need for an extension

I haven't tried this under ASAN, but I think you could maybe do this without needing the user to try to uninstall the extension directly: Extensions can call management.uninstallSelf() with showConfirmDialog: true or false.  If true, the uninstall prompt is shown.  So I think an extension could do something like:

setTimeout(() => { chrome.management.uninstallSelf({showConfirmDialog: false}); }, 5000);
chrome.management.uninstallSelf({showConfirmDialog: true});

That would display the uninstall prompt, and then uninstall the extension - I think triggering this same UAF.

The call to that includes "showConfirmDialog" does need _a_ user gesture (such as clicking on the browser action), but is much simpler to trigger than the original steps here.

(Not saying this should make today's stable cut; just highlighting)

### [Deleted User] (2021-05-19)

[Empty comment from Monorail migration]

### de...@gmail.com (2021-05-20)

Re https://crbug.com/chromium/1200679#c15: The fix works fine for me as well.

Also, regarding the fact that extensions can call chrome.management.uninstallSelf, there is the same issue, where OnExtensionUninstallDialogClosed is called twice. However, in that case, the underlying object is reference counted:

https://source.chromium.org/chromium/chromium/src/+/main:extensions/browser/api/management/management_api.cc;l=652;drc=57d3bbe012daaa928e0cf41107a2942d7d85a8e2

Although Release will be called twice, the object will only be deleted when the reference count is 0, not when it's negative.

### rd...@chromium.org (2021-05-20)

https://crbug.com/chromium/1200679#c22: Correct me if I'm wrong, but I think that should be fixed with the CL, as well?  The CL changed it such that OnExtensionUninstallDialogClosed() is only called once from the ExtensionUninstallDialog, so any callers that were assuming that should now be safe (including the management API and extension_uninstaller from https://crbug.com/chromium/1200679#c11).

### de...@gmail.com (2021-05-20)

Yes, that's true, it was more a response to https://crbug.com/chromium/1200679#c20. That is, it triggered the same sort of issue (before the fix), but wouldn't result in a UAF.

### ad...@google.com (2021-06-03)

Approving merge to M91, please merge to branch 4472 for tomorrow's security refresh cut.

### pb...@google.com (2021-06-03)

Your change has been approved for M91. Please go ahead and merge the CL to M91 branch : 4472 (refs/branch-heads/4472) manually asap.

### rd...@chromium.org (2021-06-03)

On it!  CL to merge to 91 up at https://chromium-review.googlesource.com/c/chromium/src/+/2937286.

### rd...@chromium.org (2021-06-04)

Quick update: CL has been up and trying to go in, but the mac bot seems flaky.  I'll see if I can kick it again tonight if it doesn't move, but I'm OOO tomorrow.  Feel free to push the +2 button there if I'm not around.

### gi...@appspot.gserviceaccount.com (2021-06-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/05197ae4bce83ed5ad45b3c63a7c1af86da33f6d

commit 05197ae4bce83ed5ad45b3c63a7c1af86da33f6d
Author: Devlin Cronin <rdevlin.cronin@chromium.org>
Date: Fri Jun 04 00:52:38 2021

[M91][Extensions] Fix duplicate call of OnExtensionUninstallDialogClosed()

ExtensionUninstallDialog could call OnExtensionUninstallDialogClosed()
twice if the extension was uninstalled while the dialog was showing:
- Once in response to OnExtensionUninstalled(), and
- Again in response to the dialog closing.

In addition to this being wrong, it can cause lifetime issues since
the delegate on which OnExtensionUninstallDialogClosed() was called
could be deleted after it was notified of the dialog closing.

Fix this by closing the dialog programmatically in response to
OnExtensionUninstalled(). This results in OnDialogClosed() being
called and the delegate being properly notified, but ensures that the
OnExtensionUninstallDialogClosed() method is only called once.

Add a regression test as well.

-- Manual merge notes --
Resolved trivial conflict in extension_uninstall_dialog.cc triggered by
subsequent removal of ASCIIToUTF16() calls.
--

(cherry picked from commit e7cc11190df75100a775ca4c7215022a275cc094)

Bug: 1200679
Change-Id: I47c4f25c9eb2b3725bfb78f0bad69748a119fe49
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2901617
Reviewed-by: Peter Boström <pbos@chromium.org>
Commit-Queue: Devlin <rdevlin.cronin@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#883744}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2937286
Auto-Submit: Devlin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/branch-heads/4472@{#1431}
Cr-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}

[modify] https://crrev.com/05197ae4bce83ed5ad45b3c63a7c1af86da33f6d/chrome/browser/extensions/extension_uninstall_dialog.cc
[modify] https://crrev.com/05197ae4bce83ed5ad45b3c63a7c1af86da33f6d/chrome/browser/extensions/extension_uninstall_dialog.h
[modify] https://crrev.com/05197ae4bce83ed5ad45b3c63a7c1af86da33f6d/chrome/browser/ui/views/extensions/extension_uninstall_dialog_view.cc
[modify] https://crrev.com/05197ae4bce83ed5ad45b3c63a7c1af86da33f6d/chrome/browser/ui/views/extensions/extension_uninstall_dialog_view_browsertest.cc


### rd...@chromium.org (2021-06-04)

There we go! : )

Thank you again for the report, derceg86!

### am...@chromium.org (2021-06-08)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-08)

[Empty comment from Monorail migration]

### vs...@google.com (2021-06-09)

[Empty comment from Monorail migration]

### gi...@google.com (2021-06-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-06-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/89a513b7ca54f80a2ff0b7b8d0aa0595e9bfa094

commit 89a513b7ca54f80a2ff0b7b8d0aa0595e9bfa094
Author: Devlin Cronin <rdevlin.cronin@chromium.org>
Date: Mon Jun 14 11:21:53 2021

[M90-LTS][Extensions] Fix duplicate call of OnExtensionUninstallDialogClosed()

ExtensionUninstallDialog could call OnExtensionUninstallDialogClosed()
twice if the extension was uninstalled while the dialog was showing:
- Once in response to OnExtensionUninstalled(), and
- Again in response to the dialog closing.

In addition to this being wrong, it can cause lifetime issues since
the delegate on which OnExtensionUninstallDialogClosed() was called
could be deleted after it was notified of the dialog closing.

Fix this by closing the dialog programmatically in response to
OnExtensionUninstalled(). This results in OnDialogClosed() being
called and the delegate being properly notified, but ensures that the
OnExtensionUninstallDialogClosed() method is only called once.

Add a regression test as well.

-- Manual merge notes --
Resolved trivial conflict in extension_uninstall_dialog.cc triggered by
subsequent removal of ASCIIToUTF16() calls.
--

[M90] Moved to using older string constructs

(cherry picked from commit e7cc11190df75100a775ca4c7215022a275cc094)

(cherry picked from commit 05197ae4bce83ed5ad45b3c63a7c1af86da33f6d)

Bug: 1200679
Change-Id: I47c4f25c9eb2b3725bfb78f0bad69748a119fe49
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2901617
Reviewed-by: Peter Boström <pbos@chromium.org>
Commit-Queue: Devlin <rdevlin.cronin@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#883744}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2937286
Auto-Submit: Devlin <rdevlin.cronin@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4472@{#1431}
Cr-Original-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2944942
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1521}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/89a513b7ca54f80a2ff0b7b8d0aa0595e9bfa094/chrome/browser/extensions/extension_uninstall_dialog.cc
[modify] https://crrev.com/89a513b7ca54f80a2ff0b7b8d0aa0595e9bfa094/chrome/browser/extensions/extension_uninstall_dialog.h
[modify] https://crrev.com/89a513b7ca54f80a2ff0b7b8d0aa0595e9bfa094/chrome/browser/ui/views/extensions/extension_uninstall_dialog_view.cc
[modify] https://crrev.com/89a513b7ca54f80a2ff0b7b8d0aa0595e9bfa094/chrome/browser/ui/views/extensions/extension_uninstall_dialog_view_browsertest.cc


### vs...@google.com (2021-06-14)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-15)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-06-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/61fc7ad1eb230141fe82313c199189f64938ddde

commit 61fc7ad1eb230141fe82313c199189f64938ddde
Author: Devlin Cronin <rdevlin.cronin@chromium.org>
Date: Wed Jun 16 07:57:38 2021

[M86-LTS][Extensions] Fix duplicate call of OnExtensionUninstallDialogClosed()

ExtensionUninstallDialog could call OnExtensionUninstallDialogClosed()
twice if the extension was uninstalled while the dialog was showing:
- Once in response to OnExtensionUninstalled(), and
- Again in response to the dialog closing.

In addition to this being wrong, it can cause lifetime issues since
the delegate on which OnExtensionUninstallDialogClosed() was called
could be deleted after it was notified of the dialog closing.

Fix this by closing the dialog programmatically in response to
OnExtensionUninstalled(). This results in OnDialogClosed() being
called and the delegate being properly notified, but ensures that the
OnExtensionUninstallDialogClosed() method is only called once.

Add a regression test as well.

-- Manual merge notes --
Resolved trivial conflict in extension_uninstall_dialog.cc triggered by
subsequent removal of ASCIIToUTF16() calls.
--

[M86]: Moved to using older string types.
       Used older API for closing the dialog.

(cherry picked from commit e7cc11190df75100a775ca4c7215022a275cc094)

(cherry picked from commit 05197ae4bce83ed5ad45b3c63a7c1af86da33f6d)

Bug: 1200679
Change-Id: I47c4f25c9eb2b3725bfb78f0bad69748a119fe49
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2901617
Reviewed-by: Peter Boström <pbos@chromium.org>
Commit-Queue: Devlin <rdevlin.cronin@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#883744}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2937286
Auto-Submit: Devlin <rdevlin.cronin@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4472@{#1431}
Cr-Original-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2948747
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1673}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/61fc7ad1eb230141fe82313c199189f64938ddde/chrome/browser/extensions/extension_uninstall_dialog.cc
[modify] https://crrev.com/61fc7ad1eb230141fe82313c199189f64938ddde/chrome/browser/extensions/extension_uninstall_dialog.h
[modify] https://crrev.com/61fc7ad1eb230141fe82313c199189f64938ddde/chrome/browser/ui/views/extensions/extension_uninstall_dialog_view.cc
[modify] https://crrev.com/61fc7ad1eb230141fe82313c199189f64938ddde/chrome/browser/ui/views/extensions/extension_uninstall_dialog_view_browsertest.cc


### vs...@google.com (2021-06-16)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-06-16)

Congrats, David! The VRP Panel has decided to award you $10,000 for this report. Nice work. 

### am...@google.com (2021-06-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1200679?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055600)*
