# Security: Use-After-Free in SelectFileDialog

| Field | Value |
|-------|-------|
| **Issue ID** | [40055613](https://issues.chromium.org/issues/40055613) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Views |
| **Platforms** | Windows |
| **Reporter** | kk...@gmail.com |
| **Assignee** | pm...@chromium.org |
| **Created** | 2021-04-21 |
| **Bounty** | $25,000.00 |

## Description

**VULNERABILITY DETAILS**  

This report includes 5 Use-After-Free vulnerabilities related with 'ui::SelectFileDialog::Create'.

All vulnerabilities have similar root cause.

Please see the details on attachments.

**VERSION**  

Chrome Version: stable, master  

Operating System: Windows

**REPRODUCTION CASE**  

Please see the details on attachments.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Please see the details on attachments.

## Attachments

- [1. DownloadsHandler UAF Report.txt](attachments/1. DownloadsHandler UAF Report.txt) (text/plain, 19.4 KB)
- [1. DownloadsHandler UAF.patch](attachments/1. DownloadsHandler UAF.patch) (text/plain, 693 B)
- [2. ImportDataHandler UAF Report.txt](attachments/2. ImportDataHandler UAF Report.txt) (text/plain, 19.5 KB)
- [2. ImportDataHandler UAF.patch](attachments/2. ImportDataHandler UAF.patch) (text/plain, 636 B)
- [3. SearchTabHelper UAF Report.txt](attachments/3. SearchTabHelper UAF Report.txt) (text/plain, 18.3 KB)
- [3. SearchTabHelper UAF.patch](attachments/3. SearchTabHelper UAF.patch) (text/plain, 651 B)
- [4. NewTabPageHandler UAF Report.txt](attachments/4. NewTabPageHandler UAF Report.txt) (text/plain, 19.2 KB)
- [4. NewTabPageHandler.patch](attachments/4. NewTabPageHandler.patch) (text/plain, 725 B)
- [5. PolicyUIHandler UAF Report.txt](attachments/5. PolicyUIHandler UAF Report.txt) (text/plain, 18.4 KB)
- [5. PolicyUIHandler UAF.patch](attachments/5. PolicyUIHandler UAF.patch) (text/plain, 728 B)
- [1. DownloadsHandler UAF.patch](attachments/1. DownloadsHandler UAF.patch) (text/plain, 1.9 KB)
- [2. ImportDataHandler UAF.patch](attachments/2. ImportDataHandler UAF.patch) (text/plain, 2.2 KB)
- [3. SearchTabHelper UAF.patch](attachments/3. SearchTabHelper UAF.patch) (text/plain, 1.7 KB)
- [4. NewTabPageHandler.patch](attachments/4. NewTabPageHandler.patch) (text/plain, 1.8 KB)
- [5. PolicyUIHandler UAF.patch](attachments/5. PolicyUIHandler UAF.patch) (text/plain, 1.7 KB)
- [3. SearchTabHelper UAF ASAN.log](attachments/3. SearchTabHelper UAF ASAN.log) (text/plain, 29.0 KB)
- [1.DownloadsHandler_uaf_demo.mp4](attachments/1.DownloadsHandler_uaf_demo.mp4) (video/mp4, 4.0 MB)
- [2.ImportDataHandler_uaf_demo.mp4](attachments/2.ImportDataHandler_uaf_demo.mp4) (video/mp4, 3.3 MB)
- [3.SearchTabHelper_uaf_demo.mp4](attachments/3.SearchTabHelper_uaf_demo.mp4) (video/mp4, 2.7 MB)
- [4.NewTabPageHandler_uaf_demo.mp4](attachments/4.NewTabPageHandler_uaf_demo.mp4) (video/mp4, 3.8 MB)
- [5.PolicyUIHandler_uaf_demo.mp4](attachments/5.PolicyUIHandler_uaf_demo.mp4) (video/mp4, 2.6 MB)
- [poc_extension.zip](attachments/poc_extension.zip) (application/octet-stream, 2.9 KB)

## Timeline

### [Deleted User] (2021-04-21)

[Empty comment from Monorail migration]

### ca...@chromium.org (2021-04-22)

Thanks for the report. It seems all those cases involve going to a chrome:// scheme page and manually running JS in DevTools. Do you have a proof of concept where this can be done with no DevTools interaction?

### kk...@gmail.com (2021-04-22)

No I don't. If you do without DevTools, you can modify html files related with chrome:// scheme.

### [Deleted User] (2021-04-22)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2021-04-23)

Assigning high severity since this would require a compromised renderer

[Monorail components: UI]

### ca...@chromium.org (2021-04-23)

robliao: Passing to you since you are listed as a windows owner for the relevant directory. Can you PTAL and further triage/reassign as appropriate? Thanks

### [Deleted User] (2021-04-23)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-23)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-04-29)

pkasting@, hi, robliao@ is OOO so I'm wondering if you can help determine the correct assignee here?

### pk...@chromium.org (2021-04-29)

I have no idea.

Bruce, do you know who can help with things in components like SelectFileDialog?

### br...@chromium.org (2021-04-30)

Possible candidates would include me, davidbienvenu@, or pmonette@. I'm particularly interested in pmonette@'s thoughts because in crrev.com/c/1241563 they moved file dialogs out-of-process and this vulnerability seems to be happening in the browser process.

While I assume this needs to be fixed, I am wondering about the reachability of this. Is there a POC that doesn't involve chrome: pages or devtools? i.e.; can this be reached through an arbitrary page on the internet? That would be helpful to know, and would simplify testing of a fix.


### pm...@chromium.org (2021-04-30)

It's totally normal that the crash is happening in the browser process, because the issue is with the class used to start the select file dialog process from the browser process. I didn't touch the interface of SelectFileDialog when I made the out-of-process file dialogs change.

I am definitely not a security expert so don't take this at face value but I think there's no real exploit here. It is my understanding that the "getDownloadLocationText" javascript function is only exposed to WebUI pages,  and there's no way to have third-party code running in those pages, short of using DevTools, which I don't think we're explicitely guarding agaisnt. 

I don't fully understand the downloads page code, so I'm not sure if this is a real bug that can be hit with some sequence of action on the part of the user, but I've taken a look at the SelectFileDialog interface and I think its design is somewhat flawed, making it very easy to misuse it.

This is how it's supposed to be used:
You make your class extend SelectFileDialog::Listener. You call SelectFileDialog::Create() that takes "this" as a parameter which returns a scoped_refptr to a ref-counted SelectFileDialog instance. The object is ref-counted so even if you get rid of the one reference you own, the instance will still exist and complete its work. You are supposed to manually call OnListenerDestroyed() when you are done with the SelectFileDialog instance, presumably because this usually only happens when your class gets destroyed.

This manual step should actually be called everytime you get rid of your reference to the SelectFileDialog, not just when the listener is destroyed. I think this is error-prone and the name of the method is misleading.

My opinion is that the solution would be to make SelectFileDialog::Create return a unique_ptr instead of a ref-counted object which, when deleted, would itself tell the ref-counted object that the listener is no longer listening. The implementation could still use a ref-counted object internally. This will require a little bit of refactoring to the SelectFileDialog code and its users.


### pm...@chromium.org (2021-04-30)

I've done more digging to understand if this is possible to hit without devtools and I definitely think the answer is no. That's because the functions are all bounded to a button, which cannot be hit again while the file dialog is open. That's because the SelectFileDialog code ensures that the window is disabled for the duration of the select file operation (at least on Windows, using https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-enablewindow). Using code to trigger the function bypasses this restriction.



### pm...@chromium.org (2021-04-30)

One last comment. The proposed patch for the ImportDataHandler is not adequate because it breakes the "Choose File" button after the first click. So if the user clicks on Choose File, cancels the dialog, and then tries again, the button will simply not do anything. This is certainly not the intended behavior.

Each other case would need to be analyzed to figure out if if the proposed solution is correct or note.

### kk...@gmail.com (2021-05-03)

pmonette@, the uaf cannot be triggered with user-interaction like you analyzed. However if an attacker combines vulnerabilities such as UXSS(https://research.google/pubs/pub48028/), I think it can be possible.

### kk...@gmail.com (2021-05-03)

I uploaded the modified patches. The original patches were only intended to prevent the UAF vulnerabilities. I haven't considered all scenarios.

### kk...@gmail.com (2021-05-03)

I found that the asan-log was wrong in the report - "3. SearchTabHelper UAF Report.txt". I correct the asan-log tested on win32-release_x64_90.0.4430.93.


### ro...@chromium.org (2021-05-03)

Assigning to pmonette@ as the subject matter expert. Happy to answer any general CFD questions here as well.

### ch...@chromium.org (2021-05-12)

[Empty comment from Monorail migration]

[Monorail components: -UI Internals>Views]

### [Deleted User] (2021-05-15)

pmonette: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-05-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5469e0bb11b5bbb957c658415f341d0fb71a27b6

commit 5469e0bb11b5bbb957c658415f341d0fb71a27b6
Author: Patrick Monette <pmonette@chromium.org>
Date: Mon May 17 08:00:22 2021

Notify the select file dialog when PolicyUIHandler is destroyed.

Bug: 1201032
Change-Id: I06699dbe7bc1d795d52cff9772152c17bfabb31b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2896567
Commit-Queue: calamity <calamity@chromium.org>
Auto-Submit: Patrick Monette <pmonette@chromium.org>
Reviewed-by: calamity <calamity@chromium.org>
Cr-Commit-Position: refs/heads/master@{#883387}

[modify] https://crrev.com/5469e0bb11b5bbb957c658415f341d0fb71a27b6/chrome/browser/ui/webui/policy/policy_ui_handler.cc


### pm...@chromium.org (2021-05-17)

Adding the people that will be reviewing my CLs, as the CLs themselves intentionally have very little context.



### gi...@appspot.gserviceaccount.com (2021-05-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d956f59da4c85cd114ca1cfdc2ff0ba77f13c736

commit d956f59da4c85cd114ca1cfdc2ff0ba77f13c736
Author: Patrick Monette <pmonette@chromium.org>
Date: Mon May 17 18:53:25 2021

Prevent the creation of a duplicate dialog in NewTabPageHandler

Bug: 1201032
Change-Id: I8031ead770c25d6bf537560e45099eb450779e19
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2896566
Commit-Queue: Moe Ahmadi <mahmadi@chromium.org>
Auto-Submit: Patrick Monette <pmonette@chromium.org>
Reviewed-by: Moe Ahmadi <mahmadi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#883547}

[modify] https://crrev.com/d956f59da4c85cd114ca1cfdc2ff0ba77f13c736/chrome/browser/ui/webui/new_tab_page/new_tab_page_handler.cc


### gi...@appspot.gserviceaccount.com (2021-05-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a8c6b3c222360d7e037046221bebe5e336cc2595

commit a8c6b3c222360d7e037046221bebe5e336cc2595
Author: Patrick Monette <pmonette@chromium.org>
Date: Tue May 18 19:08:54 2021

Notify the select file dialog when SearchTabHelper is destroyed.

Bug: 1201032
Change-Id: I444f9f691db1acaf21cee30a297d74d11ba7a2eb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2896565
Reviewed-by: Moe Ahmadi <mahmadi@chromium.org>
Commit-Queue: Patrick Monette <pmonette@chromium.org>
Cr-Commit-Position: refs/heads/master@{#884075}

[modify] https://crrev.com/a8c6b3c222360d7e037046221bebe5e336cc2595/chrome/browser/ui/search/search_tab_helper.cc


### gi...@appspot.gserviceaccount.com (2021-05-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b65414c4e42168d5e93c09f1681d59943ec8273f

commit b65414c4e42168d5e93c09f1681d59943ec8273f
Author: Patrick Monette <pmonette@chromium.org>
Date: Fri May 21 00:26:27 2021

Prevent the creation of a duplicate dialog in DownloadsHandler

Bug: 1201032
Change-Id: Ibad418d6cc0771934912046bcd315565a20b53ed
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2898617
Auto-Submit: Patrick Monette <pmonette@chromium.org>
Commit-Queue: Zentaro Kavanagh <zentaro@chromium.org>
Reviewed-by: Zentaro Kavanagh <zentaro@chromium.org>
Cr-Commit-Position: refs/heads/master@{#885304}

[modify] https://crrev.com/b65414c4e42168d5e93c09f1681d59943ec8273f/chrome/browser/ui/webui/settings/downloads_handler.cc
[modify] https://crrev.com/b65414c4e42168d5e93c09f1681d59943ec8273f/chrome/browser/ui/webui/settings/downloads_handler.h


### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-31)

pmonette: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-05-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7f82805a9aa3c06ea5c8699d5ea69609520a3a05

commit 7f82805a9aa3c06ea5c8699d5ea69609520a3a05
Author: Patrick Monette <pmonette@chromium.org>
Date: Mon May 31 17:39:01 2021

Prevent the creation of a duplicate dialog in ImportDataHandler

Bug: 1201032
Change-Id: Ib0b9c4f18a9f8139f3078372cea798c2aa8d5802
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2898618
Auto-Submit: Patrick Monette <pmonette@chromium.org>
Reviewed-by: dpapad <dpapad@chromium.org>
Commit-Queue: Patrick Monette <pmonette@chromium.org>
Cr-Commit-Position: refs/heads/master@{#887793}

[modify] https://crrev.com/7f82805a9aa3c06ea5c8699d5ea69609520a3a05/chrome/browser/ui/webui/settings/import_data_handler.cc
[modify] https://crrev.com/7f82805a9aa3c06ea5c8699d5ea69609520a3a05/chrome/browser/ui/webui/settings/import_data_handler.h


### pm...@chromium.org (2021-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-31)

Requesting merge to stable M91 because latest trunk commit (887793) appears to be after stable branch point (870763).

Requesting merge to beta M91 because latest trunk commit (887793) appears to be after beta branch point (870763).

Requesting merge to future beta M92 because latest trunk commit (887793) appears to be after future beta branch point (56).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-31)

This bug requires manual review: Request affecting a post-stable build
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

### [Deleted User] (2021-06-01)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-01)

Your change meets the bar and is auto-approved for M92. Please go ahead and merge the CL to branch 4515 (refs/branch-heads/4515) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: govind@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-06-03)

Discussed with carlosil@ and per https://crbug.com/chromium/1201032#c15 we think this likely needs to be chained with a separate bug. As such we're going to rate this as Medium and not take any stability risk by merging these changes to the current stable branch, M91.

But pmonette@ please do go ahead and merge to M92 per https://crbug.com/chromium/1201032#c34.

### gi...@appspot.gserviceaccount.com (2021-06-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/28d8966227803f0eb7d35b0b0d79272b6eaf9ca8

commit 28d8966227803f0eb7d35b0b0d79272b6eaf9ca8
Author: Patrick Monette <pmonette@chromium.org>
Date: Thu Jun 10 19:46:00 2021

Prevent the creation of a duplicate dialog in DownloadsHandler

(cherry picked from commit b65414c4e42168d5e93c09f1681d59943ec8273f)

Bug: 1201032
Change-Id: Ibad418d6cc0771934912046bcd315565a20b53ed
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2898617
Auto-Submit: Patrick Monette <pmonette@chromium.org>
Commit-Queue: Zentaro Kavanagh <zentaro@chromium.org>
Reviewed-by: Zentaro Kavanagh <zentaro@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#885304}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2953780
Cr-Commit-Position: refs/branch-heads/4515@{#502}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[modify] https://crrev.com/28d8966227803f0eb7d35b0b0d79272b6eaf9ca8/chrome/browser/ui/webui/settings/downloads_handler.cc
[modify] https://crrev.com/28d8966227803f0eb7d35b0b0d79272b6eaf9ca8/chrome/browser/ui/webui/settings/downloads_handler.h


### gi...@appspot.gserviceaccount.com (2021-06-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ed949ac7201726530fd29d848ce14073ec0f8b5b

commit ed949ac7201726530fd29d848ce14073ec0f8b5b
Author: Patrick Monette <pmonette@chromium.org>
Date: Mon Jun 21 08:43:42 2021

Prevent the creation of a duplicate dialog in ImportDataHandler

(cherry picked from commit 7f82805a9aa3c06ea5c8699d5ea69609520a3a05)

Bug: 1201032
Change-Id: Ib0b9c4f18a9f8139f3078372cea798c2aa8d5802
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2898618
Auto-Submit: Patrick Monette <pmonette@chromium.org>
Reviewed-by: dpapad <dpapad@chromium.org>
Commit-Queue: Patrick Monette <pmonette@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#887793}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2950422
Reviewed-by: Patrick Monette <pmonette@chromium.org>
Commit-Queue: dpapad <dpapad@chromium.org>
Cr-Commit-Position: refs/branch-heads/4515@{#811}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[modify] https://crrev.com/ed949ac7201726530fd29d848ce14073ec0f8b5b/chrome/browser/ui/webui/settings/import_data_handler.cc
[modify] https://crrev.com/ed949ac7201726530fd29d848ce14073ec0f8b5b/chrome/browser/ui/webui/settings/import_data_handler.h


### am...@chromium.org (2021-06-23)

Hi kkomdal@, thank you for this report. Apologies, but the VRP Panel declines to reward this issue given that it requires access to dev tools to trigger these vulnerabilities. If you can demonstrate remote exploitation, such as similar to the scenario you discussed in https://crbug.com/chromium/1201032#c15, we would be happy to revisit this issue and reconsider for a reward. Thank you! 

### kk...@gmail.com (2021-06-28)

Hi amyressler@, these vulnerabilities can be triggered without additional vulnerabilities and dev tools, I've attached videos to prove it. The extension used in the video is also attached. Please review the submitted demo carefully. Thank you.

### kk...@gmail.com (2021-06-28)

The extension is only required for the three vulnerabilities "1.DownloadsHandler_uaf_demo", "2.ImportDataHandler_uaf_demo" and "4.NewTabPageHandler_uaf_demo". The remaining "3.SearchTabHelper_uaf_demo" and "5.PolicyUIHandler_uaf_demo" do not require the extension.

### am...@chromium.org (2021-07-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-07-19)

[Empty comment from Monorail migration]

### kk...@gmail.com (2021-07-20)

Hi amyressler@, additional explanations of the new POCs in https://crbug.com/chromium/1201032#c39 are below.

In "1.DownloadsHandler_uaf_demo", "2.ImportDataHandler_uaf_demo" and "4.NewTabPageHandler_uaf_demo", the extension api chrome.tabs.move was used to trigger vulnerabilities without dev tools.
In https://crbug.com/chromium/1201032#c13, pmonette@ described that the SelectFileDialog code ensures that the window is disabled for the duration of the select file operation. To bypass the disabled window, the tab existing in the disabled window is moved to another window using the "chrome.tabs.move" api so that the select file operation can be performed again.

In "3.SearchTabHelper_uaf_demo" and "5.PolicyUIHandler_uaf_demo", Chrome's "tab-search" function was used to close the tabs in the disabled window by the select file operation.

The explanation of root causes for all vulnerabilities is the same as in the original report.

### dp...@chromium.org (2021-07-22)

[Comment Deleted]

### dp...@chromium.org (2021-07-22)

Re-opening this bug for now to ensure that the exploits mentioned #39 and #43 are addressed.

### ad...@google.com (2021-07-23)

[Empty comment from Monorail migration]

### am...@google.com (2021-07-23)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

This bug is a regression and does not impact stable. Removing incorrectly added Release- labels.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### ad...@google.com (2021-08-07)

Apologies for label change spam - this was a bug in our changes to make Sheriffbot work with the Extended Stable branch.

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### rz...@google.com (2021-08-25)

[Empty comment from Monorail migration]

### ma...@google.com (2021-08-30)

It seems that this bug only affected Windows, why do we need this fix in LTS?

### ma...@google.com (2021-09-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b187409ad241428340f7815eab8bedefb4d661b4

commit b187409ad241428340f7815eab8bedefb4d661b4
Author: Patrick Monette <pmonette@chromium.org>
Date: Mon Sep 13 17:08:49 2021

[M90-LTS] Notify the select file dialog when PolicyUIHandler is destroyed.

(cherry picked from commit 5469e0bb11b5bbb957c658415f341d0fb71a27b6)

Bug: 1201032
Change-Id: I06699dbe7bc1d795d52cff9772152c17bfabb31b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2896567
Commit-Queue: calamity <calamity@chromium.org>
Auto-Submit: Patrick Monette <pmonette@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#883387}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3116270
Commit-Queue: Jana Grill <janagrill@google.com>
Reviewed-by: Jana Grill <janagrill@google.com>
Owners-Override: Jana Grill <janagrill@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1599}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/b187409ad241428340f7815eab8bedefb4d661b4/chrome/browser/ui/webui/policy/policy_ui_handler.cc


### gi...@appspot.gserviceaccount.com (2021-09-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/53d7465b50ab5fb0b4c43fbae906da8dcd5bb945

commit 53d7465b50ab5fb0b4c43fbae906da8dcd5bb945
Author: Patrick Monette <pmonette@chromium.org>
Date: Mon Sep 13 21:36:25 2021

[M90-LTS] Prevent the creation of a duplicate dialog in NewTabPageHandler

(cherry picked from commit d956f59da4c85cd114ca1cfdc2ff0ba77f13c736)

Bug: 1201032
Change-Id: I8031ead770c25d6bf537560e45099eb450779e19
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2896566
Commit-Queue: Moe Ahmadi <mahmadi@chromium.org>
Auto-Submit: Patrick Monette <pmonette@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#883547}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3114455
Commit-Queue: Jana Grill <janagrill@google.com>
Reviewed-by: Jana Grill <janagrill@google.com>
Owners-Override: Jana Grill <janagrill@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1600}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/53d7465b50ab5fb0b4c43fbae906da8dcd5bb945/chrome/browser/ui/webui/new_tab_page/new_tab_page_handler.cc


### gi...@appspot.gserviceaccount.com (2021-09-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4c55393d55b2c2517179062b24dd47113cd383c7

commit 4c55393d55b2c2517179062b24dd47113cd383c7
Author: Patrick Monette <pmonette@chromium.org>
Date: Tue Sep 14 08:38:28 2021

[M90-LTS] Notify the select file dialog when SearchTabHelper is destroyed.

(cherry picked from commit a8c6b3c222360d7e037046221bebe5e336cc2595)

Bug: 1201032
Change-Id: I444f9f691db1acaf21cee30a297d74d11ba7a2eb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2896565
Commit-Queue: Patrick Monette <pmonette@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#884075}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3114938
Commit-Queue: Jana Grill <janagrill@google.com>
Reviewed-by: Jana Grill <janagrill@google.com>
Owners-Override: Jana Grill <janagrill@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1601}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/4c55393d55b2c2517179062b24dd47113cd383c7/chrome/browser/ui/search/search_tab_helper.cc


### gi...@appspot.gserviceaccount.com (2021-09-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/408cfe0d81d9a46f962ab677994d734a3e8744e0

commit 408cfe0d81d9a46f962ab677994d734a3e8744e0
Author: Patrick Monette <pmonette@chromium.org>
Date: Tue Sep 14 09:12:45 2021

[M90-LTS] Prevent the creation of a duplicate dialog in DownloadsHandler

(cherry picked from commit b65414c4e42168d5e93c09f1681d59943ec8273f)

Bug: 1201032
Change-Id: Ibad418d6cc0771934912046bcd315565a20b53ed
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2898617
Auto-Submit: Patrick Monette <pmonette@chromium.org>
Commit-Queue: Zentaro Kavanagh <zentaro@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#885304}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3114676
Commit-Queue: Jana Grill <janagrill@google.com>
Reviewed-by: Jana Grill <janagrill@google.com>
Owners-Override: Jana Grill <janagrill@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1602}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/408cfe0d81d9a46f962ab677994d734a3e8744e0/chrome/browser/ui/webui/settings/downloads_handler.cc
[modify] https://crrev.com/408cfe0d81d9a46f962ab677994d734a3e8744e0/chrome/browser/ui/webui/settings/downloads_handler.h


### ja...@google.com (2021-09-14)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/53ac954c4dac94969d9ac7680d27473bd1ede987

commit 53ac954c4dac94969d9ac7680d27473bd1ede987
Author: Artem Orlovskii <orlovskiia@yandex-team.ru>
Date: Thu Sep 16 17:19:37 2021

Prevent dangling reference possibility

SelectFileDialog::Listener interface receives selected file path
as const reference in FileSelected(). Depending on implementation
of particular SelectFileDialog it may or may not be reference to dialog
object field.

DownloadsHandler creates select_folder_dialog_, receives selected file
path reference and destroys dialog before passing reference further.
It might cause dangling ref in case dialog implementation changes and
it prevents from using current implementation of FakeSelectFileDialog
with DownloadsHandler.

Dialog destruction is introduced in crbug.com/1201032

It isn't the first time dangilng reference issue resurfaces: check
crbug.com/1216395 and crbug.com/919800 Passing variable by value
to listeners rather than by reference should eliminate root cause, so
neither dialog nor its listener need to worry about variable scope.

R=zentaro@chromium.org

Bug: 1201032
Change-Id: Ib73d9884c5942ebdc520e56873ce8a4cdd1bf2ee
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3076570
Auto-Submit: Артем Орловский <orlovskiia@yandex-team.ru>
Commit-Queue: Scott Violet <sky@chromium.org>
Reviewed-by: Scott Violet <sky@chromium.org>
Reviewed-by: Charlie Reis <creis@chromium.org>
Reviewed-by: Austin Sullivan <asully@chromium.org>
Reviewed-by: Patrick Monette <pmonette@chromium.org>
Cr-Commit-Position: refs/heads/main@{#922191}

[modify] https://crrev.com/53ac954c4dac94969d9ac7680d27473bd1ede987/content/browser/file_system_access/file_system_chooser_test_helpers.cc


### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### kk...@gmail.com (2021-11-01)

I would like to know the progress of the re-evaluation mentioned in https://crbug.com/chromium/1201032#c45.

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-11-24)

Hi pmonette@; I see there was a newer CL introduced on this issue in September. Does this fix this issue being triggerable when the malicious extension is installed? Just want to get a status of when this aspect can be addressed and/or this issue can be resolved. Thanks! 

### pm...@chromium.org (2021-11-24)

Re https://crbug.com/chromium/1201032#c45: The new POCs are still mitigated by the fixes I made. I think the reporter only wanted to show that the original exploit could be made without using Devtools. 

So nothing additional to do for the reported issue, beside maybe the ability to "bypass" the disabled Window when a select file dialog is open using the Tabs API. I don't know if there's a way to exploit this but I'm not very creative :)

### am...@chromium.org (2021-11-30)

yes, I concur with that; just wanted to make sure there were not additional fixes needed to mitigate this being triggerable via the extensions before we would reassess for VRP eligibility. Thanks for your insight, super appreciate it and I'll button this back up as fixed. Thanks again! 

### [Deleted User] (2021-12-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-12-01)

Congratulations, kkomdal! The VRP Panel has been able to reassess this issue and has decided to award you $25000 for this report based on the updated POCs. Thank you for your patience while the POCs were evaluated and for this report to be reassessed. 

### am...@google.com (2021-12-06)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-12-20)

Hello, kkomdal@- we consider attachments/pocs included with reports to be an integral part of the report (and part of the VRP eligibility criteria), so I've undeleted them. Thanks! 

### [Deleted User] (2022-03-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1201032?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055613)*
