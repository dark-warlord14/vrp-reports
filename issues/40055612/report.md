# Security: Use-after-free in extension install dialog

| Field | Value |
|-------|-------|
| **Issue ID** | [40055612](https://issues.chromium.org/issues/40055612) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Extensions |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | kk...@gmail.com |
| **Assignee** | la...@chromium.org |
| **Created** | 2021-04-21 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**

I report two vulnerabilities (Use-After-Free) which have the same root cause.  

Please see the attachments for details.

**VERSION**

See the attachments.

**REPRODUCTION CASE**

See the attachments.

## Attachments

- [patch.diff](attachments/patch.diff) (text/plain, 738 B)
- [report_vuln1.txt](attachments/report_vuln1.txt) (text/plain, 24.4 KB)
- [report_vuln2.txt](attachments/report_vuln2.txt) (text/plain, 20.8 KB)

## Timeline

### [Deleted User] (2021-04-21)

[Empty comment from Monorail migration]

### ca...@chromium.org (2021-04-22)

Thanks for the report. In both of those cases the user would need to manually run JS from devtools while on the extensions page. Do you have a PoC where this can be triggered without devtools interaction? Thanks

### kk...@gmail.com (2021-04-22)

No, I don't have a PoC without devtools interaction. I think that if you want to trigger these vulnerabilities without devtools, you need a compromised renderer.
Thanks

### [Deleted User] (2021-04-22)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2021-04-23)

Assigning high severity as this requires a compromised renderer to exploit.

lazyboy: Can you help further triage this and reassign as appropriate? Thanks

[Monorail components: Platform>Extensions]

### [Deleted User] (2021-04-23)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-23)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-05)

lazyboy: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@chromium.org (2021-05-05)

Starting to take a look.

### la...@chromium.org (2021-05-11)

[Empty comment from Monorail migration]

### la...@chromium.org (2021-05-20)

I submitted one CL for ExtensionInstallDialogView UaF, it linked a wrong bug#.

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/52f8fecd8b0c30560d0ebbccfe5179c4c838a3cf

commit 52f8fecd8b0c30560d0ebbccfe5179c4c838a3cf
Author: Istiaque Ahmed <lazyboy@chromium.org>
Date: Wed May 19 20:15:39 2021

Fix navigator access from ExtensionInstallDialogView::LinkClicked

This CL changes how PageNavigator is/was structured within
ExtensionInstallDialogView: PageNavigator can go stale in certain
circumstances (see bug) upon WebContents's destruction.
ExtensionInstallDialogView now owns ExtensionInstallPromptShowParams.
The dialog view can query the "show params" to figure out its
associated PageNavigator to use — eliminating UaF.
Also note that ExtensionInstallPromptShowParams (already) tracks
WebContents’s lifetime.

This CL also adds a regression test for the bug:
ExtensionInstallDialogViewTest.\
TabClosureClearsWebContentsFromDialogView

Bug: 1201060
Test: See https://crbug.com/1201060
Change-Id: Iedfcf1183d7906ffd18cd009939591bc92a0872c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2881314
Commit-Queue: Istiaque Ahmed <lazyboy@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#884654}

[modify] https://crrev.com/52f8fecd8b0c30560d0ebbccfe5179c4c838a3cf/chrome/browser/extensions/extension_install_prompt.cc
[modify] https://crrev.com/52f8fecd8b0c30560d0ebbccfe5179c4c838a3cf/chrome/browser/extensions/extension_install_prompt.h
[modify] https://crrev.com/52f8fecd8b0c30560d0ebbccfe5179c4c838a3cf/chrome/browser/extensions/extension_install_prompt_unittest.cc
[modify] https://crrev.com/52f8fecd8b0c30560d0ebbccfe5179c4c838a3cf/chrome/browser/extensions/external_install_error.cc
[modify] https://crrev.com/52f8fecd8b0c30560d0ebbccfe5179c4c838a3cf/chrome/browser/extensions/external_install_error.h
[modify] https://crrev.com/52f8fecd8b0c30560d0ebbccfe5179c4c838a3cf/chrome/browser/ui/views/extensions/extension_install_dialog_view.cc
[modify] https://crrev.com/52f8fecd8b0c30560d0ebbccfe5179c4c838a3cf/chrome/browser/ui/views/extensions/extension_install_dialog_view.h
[modify] https://crrev.com/52f8fecd8b0c30560d0ebbccfe5179c4c838a3cf/chrome/browser/ui/views/extensions/extension_install_dialog_view_browsertest.cc
[modify] https://crrev.com/52f8fecd8b0c30560d0ebbccfe5179c4c838a3cf/chrome/browser/ui/views/extensions/extension_install_dialog_view_supervised_browsertest.cc


### gi...@appspot.gserviceaccount.com (2021-05-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0486a5d1ced3701593746cd1e7428d5dc88c9086

commit 0486a5d1ced3701593746cd1e7428d5dc88c9086
Author: Istiaque Ahmed <lazyboy@chromium.org>
Date: Thu May 20 21:09:57 2021

Fix navigator access from ExtensionInstallFrictionDialogView

This CL changes how PageNavigator is/was structured within
ExtensionInstallFrictionDialogView: PageNavigator can go stale in
certain circumstances (see bug) upon WebContents's destruction.
ExtensionInstallFrictionDialogView now tracks the WC's lifetime so
it can safely use it from OnLearnMoreLinkClicked() method.

This CL also uses ScopedTabbedBrowserDisplayer from
ExtensionInstallFrictionDialogView::OnLearnMoreLinkClicked when
there is not WC available in it. This brings it into parity
with ExtensionInstallDialogView::OnLinkClicked.

This CL also adds a regression test for the bug:
ExtensionInstallFrictionDialogViewTest.\
TabClosureClearsWebContentsFromDialogView

Bug: 1201031
Change-Id: I31a8aa3e3b92c73cd3ea236f75dcf0e4083d74c9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2909412
Commit-Queue: Istiaque Ahmed <lazyboy@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#885217}

[modify] https://crrev.com/0486a5d1ced3701593746cd1e7428d5dc88c9086/chrome/browser/ui/views/extensions/extension_install_friction_dialog_view.cc
[modify] https://crrev.com/0486a5d1ced3701593746cd1e7428d5dc88c9086/chrome/browser/ui/views/extensions/extension_install_friction_dialog_view.h
[modify] https://crrev.com/0486a5d1ced3701593746cd1e7428d5dc88c9086/chrome/browser/ui/views/extensions/extension_install_friction_dialog_view_browsertest.cc


### gi...@appspot.gserviceaccount.com (2021-05-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/588865f0da8c9754889812d7c9b6811cc4230e4d

commit 588865f0da8c9754889812d7c9b6811cc4230e4d
Author: Istiaque Ahmed <lazyboy@chromium.org>
Date: Thu May 20 22:20:27 2021

Fix incorrect bug reference in TabClosureClearsWebContents* test.

It accidentally pointed to a wrong https://crbug.com/chromium/1201060. This CL fixes that.

Bug: 1201031
Test: None
Change-Id: Idf63bccd8bfa2bb5a2bb42249454eab938728dc4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2910137
Auto-Submit: Istiaque Ahmed <lazyboy@chromium.org>
Reviewed-by: David Bertoni <dbertoni@chromium.org>
Reviewed-by: Istiaque Ahmed <lazyboy@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Commit-Queue: Devlin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#885253}

[modify] https://crrev.com/588865f0da8c9754889812d7c9b6811cc4230e4d/chrome/browser/ui/views/extensions/extension_install_dialog_view_browsertest.cc


### la...@chromium.org (2021-05-21)

Should be fixed now.

### [Deleted User] (2021-05-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-21)

Requesting merge to stable M90 because latest trunk commit (885253) appears to be after stable branch point (857950).

Requesting merge to beta M91 because latest trunk commit (885253) appears to be after beta branch point (870763).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-21)

This bug requires manual review: We are only 3 days from stable.
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

### ad...@google.com (2021-05-21)

[Empty comment from Monorail migration]

### la...@chromium.org (2021-05-22)

re https://bugs.chromium.org/p/chromium/issues/detail?id=1201031#c18:

1. I think so, but chrome-security can weigh in
2. CLs:
    * https://chromium-review.googlesource.com/c/chromium/src/+/2881314 for case #1
    * https://chromium-review.googlesource.com/c/chromium/src/+/2909412 for case #2
3. Landed: yes, Verified: Only by me on mac canary for case#1. Case #2 depends on EnforceSafeBrowsingExtensionAllowlist feature (now SafeBrowsingCrxAllowlistShowWarnings?) which I couldn't figure out how to toggle for Canary.
4. Based on https://bugs.chromium.org/p/chromium/issues/detail?id=1201031#c19, probably not.
5. The bug isn't new, but was filed and fixed recently.
6. No
7. No

8. No (This isn't ChromeOS specific bug).


### am...@google.com (2021-06-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2021-06-03)

Approving merge to M91. Please merge to branch 4472. We'll be cutting a security refresh tomorrow.

### pb...@google.com (2021-06-03)

Your change has been approved for M91. Please go ahead and merge the CL to M91 branch : 4472 (refs/branch-heads/4472) manually asap.

### am...@chromium.org (2021-06-03)

Congratulations, kkwon! The VRP Panel has decided to award you $20,000 for this report. Please let me know if you'd like to include others for credit in release notes. 

### gi...@appspot.gserviceaccount.com (2021-06-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/500a93d2535a1f6c9eaea8dd278f5057e54afda0

commit 500a93d2535a1f6c9eaea8dd278f5057e54afda0
Author: Istiaque Ahmed <lazyboy@chromium.org>
Date: Thu Jun 03 23:42:08 2021

[M91] Fix navigator access from ExtensionInstallFrictionDialogView

This CL changes how PageNavigator is/was structured within
ExtensionInstallFrictionDialogView: PageNavigator can go stale in
certain circumstances (see bug) upon WebContents's destruction.
ExtensionInstallFrictionDialogView now tracks the WC's lifetime so
it can safely use it from OnLearnMoreLinkClicked() method.

This CL also uses ScopedTabbedBrowserDisplayer from
ExtensionInstallFrictionDialogView::OnLearnMoreLinkClicked when
there is not WC available in it. This brings it into parity
with ExtensionInstallDialogView::OnLinkClicked.

This CL also adds a regression test for the bug:
ExtensionInstallFrictionDialogViewTest.\
TabClosureClearsWebContentsFromDialogView

(cherry picked from commit 0486a5d1ced3701593746cd1e7428d5dc88c9086)

Bug: 1201031
Change-Id: I31a8aa3e3b92c73cd3ea236f75dcf0e4083d74c9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2909412
Commit-Queue: Istiaque Ahmed <lazyboy@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#885217}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2937290
Cr-Commit-Position: refs/branch-heads/4472@{#1424}
Cr-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}

[modify] https://crrev.com/500a93d2535a1f6c9eaea8dd278f5057e54afda0/chrome/browser/ui/views/extensions/extension_install_friction_dialog_view.cc
[modify] https://crrev.com/500a93d2535a1f6c9eaea8dd278f5057e54afda0/chrome/browser/ui/views/extensions/extension_install_friction_dialog_view.h
[modify] https://crrev.com/500a93d2535a1f6c9eaea8dd278f5057e54afda0/chrome/browser/ui/views/extensions/extension_install_friction_dialog_view_browsertest.cc


### la...@chromium.org (2021-06-03)

Note: there are two CLs I'm merging for this bug (see https://bugs.chromium.org/p/chromium/issues/detail?id=1201031#c20):

1)
The first one mentioned incorrect bug in the original CL & in the merge CL: https://bugs.chromium.org/p/chromium/issues/detail?id=1201060#c11

I'm copy pasting the CL desc here:

commit f0a63116e91bc89acfd53bbf7a640edbcdc9b471
Author: Istiaque Ahmed <lazyboy@chromium.org>
Date: Thu Jun 03 23:50:48 2021

[M91] Fix navigator access from ExtensionInstallDialogView::LinkClicked

This CL changes how PageNavigator is/was structured within
ExtensionInstallDialogView: PageNavigator can go stale in certain
circumstances (see bug) upon WebContents's destruction.
ExtensionInstallDialogView now owns ExtensionInstallPromptShowParams.
The dialog view can query the "show params" to figure out its
associated PageNavigator to use — eliminating UaF.
Also note that ExtensionInstallPromptShowParams (already) tracks
WebContents’s lifetime.

This CL also adds a regression test for the bug:
ExtensionInstallDialogViewTest.\
TabClosureClearsWebContentsFromDialogView

Bug: 1201060
Test: See https://crbug.com/1201060
Change-Id: Iedfcf1183d7906ffd18cd009939591bc92a0872c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2881314
Commit-Queue: Istiaque Ahmed <lazyboy@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#884654}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2937288
Cr-Commit-Position: refs/branch-heads/4472@{#1426}
Cr-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}

[modify] https://crrev.com/f0a63116e91bc89acfd53bbf7a640edbcdc9b471/chrome/browser/extensions/extension_install_prompt.cc
[modify] https://crrev.com/f0a63116e91bc89acfd53bbf7a640edbcdc9b471/chrome/browser/extensions/extension_install_prompt.h
[modify] https://crrev.com/f0a63116e91bc89acfd53bbf7a640edbcdc9b471/chrome/browser/extensions/extension_install_prompt_unittest.cc
[modify] https://crrev.com/f0a63116e91bc89acfd53bbf7a640edbcdc9b471/chrome/browser/extensions/external_install_error.cc
[modify] https://crrev.com/f0a63116e91bc89acfd53bbf7a640edbcdc9b471/chrome/browser/extensions/external_install_error.h
[modify] https://crrev.com/f0a63116e91bc89acfd53bbf7a640edbcdc9b471/chrome/browser/ui/views/extensions/extension_install_dialog_view.cc
[modify] https://crrev.com/f0a63116e91bc89acfd53bbf7a640edbcdc9b471/chrome/browser/ui/views/extensions/extension_install_dialog_view.h
[modify] https://crrev.com/f0a63116e91bc89acfd53bbf7a640edbcdc9b471/chrome/browser/ui/views/extensions/extension_install_dialog_view_browsertest.cc
[modify] https://crrev.com/f0a63116e91bc89acfd53bbf7a640edbcdc9b471/chrome/browser/ui/views/extensions/extension_install_dialog_view_supervised_browsertest.cc


2)
https://bugs.chromium.org/p/chromium/issues/detail?id=1201031#c25

### am...@google.com (2021-06-04)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-06-08)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-08)

[Empty comment from Monorail migration]

### vs...@google.com (2021-06-09)

[Empty comment from Monorail migration]

### gi...@google.com (2021-06-09)

[Empty comment from Monorail migration]

### vs...@google.com (2021-06-11)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### le...@gmail.com (2021-09-10)

[Comment Deleted]

### am...@chromium.org (2021-09-10)

Hello reporter, the comment above is correct- we consider attachments/pocs included with reports to be an integral part of the report, so I've un-deleted them. Thanks!

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1201031?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055612)*
