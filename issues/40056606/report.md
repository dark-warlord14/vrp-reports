# UAF in PrintViewManager

| Field | Value |
|-------|-------|
| **Issue ID** | [40056606](https://issues.chromium.org/issues/40056606) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Printing |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2021-07-20 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**  

The PrintViewManager will run a nested message loop[1] for printer settings initialization. If the PrintViewManager or other related instances are destroyed, the UAF will be triggered when its member variable quit\_inner\_loop\_[2] gets accessed after the nested message loops exit.

[1]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/printing/print_view_manager_base.cc;l=836;drc=34da4407648871eca12e13e607545c0a64a83c1c>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/printing/print_view_manager_base.cc;l=969;drc=34da4407648871eca12e13e607545c0a64a83c1c>

**VERSION**  

Chrome Version: stable  

Operating System: test in Linux

**REPRODUCTION CASE**

$ python -m SimpleHTTPServer  

$ out/asan/chrome --user-data-dir=/tmp/xxxx "<http://localhost:8000/poc.html>"

Choose "Print using system dialog" in "More settings", wait a while and print to file.

Then because the file is too large, it will prompt that the page is unresponsive. Click "Exit page" to crash the page, and refresh the page.

Finally, choose "Print using system dialog" in "More settings" again and close the page.

The UAF will be triggered after 1min[\*]. (You can modify it to 5 seconds to shorten this time)

[\*] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/printing/print_view_manager_base.cc;l=958;bpv=1;bpt=0;drc=472292f33644dd79187450d612af04f8a71802fb>

It’s just one of the triggering paths, there may be other simpler paths or it can be triggered more easily through a compromised renderer.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Alpha Lab

## Attachments

- [asan](attachments/asan) (text/plain, 24.3 KB)
- [poc.html](attachments/poc.html) (text/plain, 201 B)
- [demo.mp4](attachments/demo.mp4) (video/mp4, 2.3 MB)
- [patch.diff](attachments/patch.diff) (text/plain, 2.4 KB)
- [poc.html](attachments/poc.html) (text/plain, 31 B)
- [demo2.mp4](attachments/demo2.mp4) (video/mp4, 1.7 MB)

## Timeline

### [Deleted User] (2021-07-20)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-07-21)

+thestig +weili, can you take a look at this please? I'm tentatively assigning a medium severity since this needs an explicit print command from the user.

[Monorail components: Internals>Printing]

### [Deleted User] (2021-07-21)

[Empty comment from Monorail migration]

### le...@gmail.com (2021-07-21)

Thanks for the quick reply. I think the severity should be high. A compromised renderer could greatly simplify user gesture, you can try this patch.


REPRODUCTION CASE:
Choose "Print using system dialog", close the page, and the UAF will be triggered.


With compromised renderer, other user gestures may not be necessary, I did not study it further.

### do...@chromium.org (2021-07-21)

Thanks for the clarification. A UaF in the browser process that needs a compromised renderer is indeed high severity.

### [Deleted User] (2021-07-21)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2021-07-22)

I'm having a bit of trouble reproducing this based on the original steps. I'll try out the patch in patch set 4 next.

### le...@gmail.com (2021-07-27)

Hi thestig@, can you reproduce it now?

### th...@chromium.org (2021-07-28)

Yes, I can reproduce it using the patch in https://crbug.com/chromium/1231134#c4. The patch is slightly out of date and requires minor adjustments to compile.

### th...@chromium.org (2021-07-28)

I landed r906269 for this bug, but messed up the associated bug number.

### [Deleted User] (2021-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-29)

This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M91. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M92. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M93. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-07-29)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
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
Owners: govind@(Android), benmason@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2021-07-29)

leecraso@: Have you able to try a newer Chromium build with the fix to verify it works?

We should probably start with a M93 merge. Not sure why sheriffbot started with M92 in https://crbug.com/chromium/1231134#c14.

### am...@chromium.org (2021-07-29)

thestig@ we're cutting an M92 security refresh (and an M91 extended stable release) today. Seems like this makes sense to leave this for a few more days of Canary time before merging. I can check back and, as long as there are no issues, approve in a couple of day and it can go into the next refresh in a couple of weeks. Please feel free to let me know if you disagree. :) Thanks!

### th...@chromium.org (2021-07-29)

I'm fine with letting it bake for a bit longer and then merge.

### [Deleted User] (2021-07-29)

This bug requires manual review: M93's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
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
Owners: benmason@(Android), govind@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### le...@gmail.com (2021-07-30)

Hi thestig@, the patch looks good in my test.

### th...@chromium.org (2021-08-02)

re: https://crbug.com/chromium/1231134#c19 - Thanks for the feedback!

amyressler@: Are you handling M93 merges as well? Between the positive feedback and no reports of the fix having unintended side effects, shall we start with the M93 merge?

### am...@chromium.org (2021-08-02)

I am indeed and this one was next on my list! I concur, based on good bake time on Canary and patch confirmation, sounds like this is indeed good to go for M93 merge. Please merge to branch 4577 before 2pm PDT tomorrow (Tuesday, 3 August) so it can be in this week's beta release. Thanks!!

### th...@chromium.org (2021-08-03)

Cherrypicked in https://chromium-review.googlesource.com/c/chromium/src/+/3068160, but I once again had the wrong Bug: field. :-\

### am...@google.com (2021-08-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-08-04)

Congratulations, Leecraso and Guang Gong! The VRP Panel has decided to award you $20,000 for this report. Nice work! 

### am...@google.com (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-10)

Merge approved to M92, please merge to branch 4515 by 5pm PDT Thursday (12 August) so this fix can be included in next week's stable channel refresh. Thank you! 

### th...@chromium.org (2021-08-10)

M92 merge in progress, with the right bug # this time: https://chromium-review.googlesource.com/c/chromium/src/+/3086110

We probably should drop the Merge-Request-91 label, given M92 is the current Stable channel.

### am...@google.com (2021-08-10)

M91 was/is going to become the Extended Stable release channel. That may have potentially shifted only as of very late last week, which is why I kept the label on. 

### gi...@appspot.gserviceaccount.com (2021-08-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/774dea8b445cb51cd2dccc560e4514369e197de6

commit 774dea8b445cb51cd2dccc560e4514369e197de6
Author: Lei Zhang <thestig@chromium.org>
Date: Tue Aug 10 21:38:36 2021

M92: Do more class validity checks in PrintViewManagerBase.

PrintViewManagerBase runs a nested loop. In some situations,
PrintViewManagerBase and related classes like PrintViewManager and
PrintPreviewHandler can get deleted while the nested loop is running.
When this happens, the nested loop exists to a PrintViewManagerBase
that is no longer valid.

Use base::WeakPtrs liberally to check for this condition and exit
safely.

(cherry picked from commit a2cb1fb333d2faacb2fe1380f8d2621b5ee6af7e)

Bug: 1231134
Change-Id: I21ec131574331ce973d22594c11e70088147e149
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3057880
Reviewed-by: Alan Screen <awscreen@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#906269}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3086110
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4515@{#2024}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[modify] https://crrev.com/774dea8b445cb51cd2dccc560e4514369e197de6/chrome/browser/printing/print_view_manager.cc
[modify] https://crrev.com/774dea8b445cb51cd2dccc560e4514369e197de6/chrome/browser/printing/print_view_manager.h
[modify] https://crrev.com/774dea8b445cb51cd2dccc560e4514369e197de6/chrome/browser/printing/print_view_manager_base.cc
[modify] https://crrev.com/774dea8b445cb51cd2dccc560e4514369e197de6/chrome/browser/printing/print_view_manager_base.h
[modify] https://crrev.com/774dea8b445cb51cd2dccc560e4514369e197de6/chrome/browser/ui/webui/print_preview/print_preview_handler.cc


### am...@google.com (2021-08-16)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-16)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-08-17)

removing merge-request-91 label as M91 is no longer going to be extended stable 

### rz...@google.com (2021-08-19)

[Empty comment from Monorail migration]

### rz...@google.com (2021-08-20)

[Empty comment from Monorail migration]

### gi...@google.com (2021-08-20)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-08-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f4db5691eed7a664249639ed4f0b4c93c254a7a8

commit f4db5691eed7a664249639ed4f0b4c93c254a7a8
Author: Lei Zhang <thestig@chromium.org>
Date: Mon Aug 23 13:42:51 2021

[M90-LTS] Do more class validity checks in PrintViewManagerBase.

PrintViewManagerBase runs a nested loop. In some situations,
PrintViewManagerBase and related classes like PrintViewManager and
PrintPreviewHandler can get deleted while the nested loop is running.
When this happens, the nested loop exists to a PrintViewManagerBase
that is no longer valid.

Use base::WeakPtrs liberally to check for this condition and exit
safely.

(cherry picked from commit a2cb1fb333d2faacb2fe1380f8d2621b5ee6af7e)

Bug: 1231134
Change-Id: I21ec131574331ce973d22594c11e70088147e149
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3057880
Commit-Queue: Lei Zhang <thestig@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#906269}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3100154
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Owners-Override: Artem Sumaneev <asumaneev@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1574}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/f4db5691eed7a664249639ed4f0b4c93c254a7a8/chrome/browser/printing/print_view_manager.cc
[modify] https://crrev.com/f4db5691eed7a664249639ed4f0b4c93c254a7a8/chrome/browser/printing/print_view_manager.h
[modify] https://crrev.com/f4db5691eed7a664249639ed4f0b4c93c254a7a8/chrome/browser/printing/print_view_manager_base.cc
[modify] https://crrev.com/f4db5691eed7a664249639ed4f0b4c93c254a7a8/chrome/browser/printing/print_view_manager_base.h
[modify] https://crrev.com/f4db5691eed7a664249639ed4f0b4c93c254a7a8/chrome/browser/ui/webui/print_preview/print_preview_handler.cc


### rz...@google.com (2021-08-23)

[Empty comment from Monorail migration]

### rz...@google.com (2021-08-23)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-26)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d2758e3fc7e0b51b4b6e172aca312e499b0b7d4b

commit d2758e3fc7e0b51b4b6e172aca312e499b0b7d4b
Author: Lei Zhang <thestig@chromium.org>
Date: Wed Sep 22 22:41:35 2021

M92: Do more class validity checks in PrintViewManagerBase.

PrintViewManagerBase runs a nested loop. In some situations,
PrintViewManagerBase and related classes like PrintViewManager and
PrintPreviewHandler can get deleted while the nested loop is running.
When this happens, the nested loop exists to a PrintViewManagerBase
that is no longer valid.

Use base::WeakPtrs liberally to check for this condition and exit
safely.

(cherry picked from commit a2cb1fb333d2faacb2fe1380f8d2621b5ee6af7e)

(cherry picked from commit 774dea8b445cb51cd2dccc560e4514369e197de6)

Bug: 1231134
Change-Id: I21ec131574331ce973d22594c11e70088147e149
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3057880
Reviewed-by: Alan Screen <awscreen@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#906269}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3086110
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Original-Commit-Position: refs/branch-heads/4515@{#2024}
Cr-Original-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3171578
Auto-Submit: Joe Tessler <jrt@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>
Cr-Commit-Position: refs/branch-heads/4515_132@{#9}
Cr-Branched-From: 8e089f9dc0d240f50afd19b527a90447b90ca5bb-refs/branch-heads/4515@{#1934}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[modify] https://crrev.com/d2758e3fc7e0b51b4b6e172aca312e499b0b7d4b/chrome/browser/printing/print_view_manager_base.cc
[modify] https://crrev.com/d2758e3fc7e0b51b4b6e172aca312e499b0b7d4b/chrome/browser/ui/webui/print_preview/print_preview_handler.cc
[modify] https://crrev.com/d2758e3fc7e0b51b4b6e172aca312e499b0b7d4b/chrome/browser/printing/print_view_manager.cc
[modify] https://crrev.com/d2758e3fc7e0b51b4b6e172aca312e499b0b7d4b/chrome/browser/printing/print_view_manager_base.h
[modify] https://crrev.com/d2758e3fc7e0b51b4b6e172aca312e499b0b7d4b/chrome/browser/printing/print_view_manager.h


### [Deleted User] (2021-11-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1231134?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056606)*
