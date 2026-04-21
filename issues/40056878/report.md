# use after free in DiceTurnSyncOnHelperDelegateImpl::ShowEnterpriseAccountConfirmation(

| Field | Value |
|-------|-------|
| **Issue ID** | [40056878](https://issues.chromium.org/issues/40056878) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | wx...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2021-08-13 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36

Steps to reproduce the problem:
1.in the function  DiceTurnSyncOnHelperDelegateImpl::ShowEnterpriseAccountConfirmation , it will send browser_ to a callback, and the browser will enter the function DiceTurnSyncOnHelper::Delegate::
    ShowEnterpriseAccountConfirmationForBrowser to use the view, before we enter the callback, we close the borwser_'s view , it will show use after free.
2.the root reason I think is the same as https://crbug.com/chromium/1239516
3.

What is the expected behavior?

What went wrong?
above all,
the fix is easy, change it to weak_ptr; 

Did this work before? N/A 

Chrome version: 92.0.4515.131  Channel: stable
OS Version: 10.0

## Timeline

### [Deleted User] (2021-08-13)

[Empty comment from Monorail migration]

### wf...@chromium.org (2021-08-13)

I concur from code inspection alone it looks possible that the view held by the raw ptr to Browser might be invalidated before the callback runs, but in a practical sense I'm not sure how it would be possible for this to happen during the signin confirmation helper being shown, thus I'm not sure how an attacker could make use of this.

I'm adding some of the signin folks to take a look, it's certainly probably something we should fix. I'll triage this High priority until we're sure there is no way to reproduce this.

In the meantime if you have a proof of concept or steps you suggest to reproduce this, that would be helpful.

[Monorail components: Services>SignIn]

### dr...@chromium.org (2021-08-13)

Jan is working on this code, assigning to him.

### [Deleted User] (2021-08-14)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-14)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wx...@gmail.com (2021-08-16)

I can not trigger it. Feel free to close it,.

### jk...@chromium.org (2021-08-16)

Thanks for the report.

Looking into it, it likely *is* possible to repro. This code gets called after the user clicks on "Enable sync" but before we display any modal dialog. So there's nothing that blocks closing the window, e.g. by Cmd+W.

I tried to repro but it's not easy as you need to hit a narrow time window between the call and the callback (50 microseconds to 2 milliseconds in my testing). However, I succeded to close the window both before the call+callback and after the call+callback so it should also be possible to close it in between.

Uploaded a fix for review.

### jk...@chromium.org (2021-08-16)

That being said, I am still not sure if an attacker can make use of that.

This is the pending fix: https://chromium-review.googlesource.com/c/chromium/src/+/3097837

### wx...@gmail.com (2021-08-16)

>I tried to repro but it's not easy as you need to hit a narrow time window between the call and the callback (50 microseconds to 2 milliseconds in my testing

Can we add the time from the code to trigger it? I don't know how to add the time..(Use the function Sleep? or other ways?)

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-08-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d710b5cdbb18ac8e880afd3c9340106006a9f744

commit d710b5cdbb18ac8e880afd3c9340106006a9f744
Author: Jan Krcal <jkrcal@chromium.org>
Date: Mon Aug 16 19:20:01 2021

[Sync consent] Make enterprise checks more robust

This CL passes a WeakPtr instead a raw pointer to one async callback in
the process of enabling sync.

Bug: 1239595
Change-Id: I5f79456a153a1be52dcac692b59b4322af35893c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3097837
Auto-Submit: Jan Krcal <jkrcal@chromium.org>
Commit-Queue: Yann Dago <ydago@chromium.org>
Reviewed-by: Yann Dago <ydago@chromium.org>
Cr-Commit-Position: refs/heads/master@{#912287}

[modify] https://crrev.com/d710b5cdbb18ac8e880afd3c9340106006a9f744/chrome/browser/ui/webui/signin/dice_turn_sync_on_helper_delegate_impl.cc


### rs...@chromium.org (2021-08-16)

[Empty comment from Monorail migration]

### jk...@chromium.org (2021-08-17)

Can anyone from the security team please instruct me what needs to be done with the fix in #11?

For the record, the bug is in Chrome since "forever" (despite in a different place), e.g.
 - M88: https://source.chromium.org/chromium/chromium/src/+/refs/tags/88.0.4324.96:chrome/browser/ui/views/sync/profile_signin_confirmation_dialog_views.cc;l=118-121;drc=79fe037f09aac97391439c178cb861e6874727fa
 - M80: https://source.chromium.org/chromium/chromium/src/+/refs/tags/80.0.3987.87:chrome/browser/ui/views/sync/profile_signin_confirmation_dialog_views.cc;l=106-109;drc=9038c8dbc97ca15d4ef9d192d342582133e5cdd6
 - M70: https://source.chromium.org/chromium/chromium/src/+/refs/tags/70.0.3538.67:chrome/browser/ui/views/sync/profile_signin_confirmation_dialog_views.cc;l=82-90;drc=f01dd3f528ad685c6a607b7380084d6c48385fb4

### rs...@chromium.org (2021-08-17)

Marking a bug as Fixed will kick off merge procedures. Given that this is Sev-High we’ll likely merge it. Sheriffbot will handle labeling for the right MStones.

### [Deleted User] (2021-08-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-18)

Requesting merge to stable M92 because latest trunk commit (912287) appears to be after stable branch point (885287).

Requesting merge to beta M93 because latest trunk commit (912287) appears to be after beta branch point (902210).

Requesting merge to dev M94 because latest trunk commit (912287) appears to be after dev branch point (911515).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-18)

This bug requires manual review: We are only 12 days from stable.
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

### jk...@chromium.org (2021-08-19)

Re #18:

1. It fits the guidelines as the security team marked it as severity-high. The CL lacks unit-tests as the change is completely trivial (and the tests would be non-trivial to build up) and I prioritized speed of fixing it. If that's a major issue, I can revert and reland with a unit-test (likely early next week). I also did not understand well the scope of merging for this patch.
2. https://chromium-review.googlesource.com/c/chromium/src/+/3097837
3. Yes, I verified that the flow still works. It's hard to verify the actual fix as no-one managed to trigger the crash before the fix.
4. As detailed in #17, yes.
5. Security bug with high severity.
6. No
7. No, this is fully launched since forever.

I don't think this code affects ChromeOS (Ash), thus removing the label.

### [Deleted User] (2021-08-19)

Your change meets the bar and is auto-approved for M94. Please go ahead and merge the CL to branch 4606 (refs/branch-heads/4606) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: govind@(Android), harrysouders@(iOS), matthewjoseph@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-08-19)

hi jkrcal@, if there have been no stability or other issues since landing this fix on Canary, please go ahead and merge to M94 and M93. 
Please merge to M93, branch 4577 asap, by 5pm PDT tomorrow (Friday, 20 August) so that this fix can be in next week's M93 beta. 



### jk...@chromium.org (2021-08-20)

Thanks, will do!

A clean merge to M94 should land soon.
I need a real review for the merge to M93 as there were minor merge conflicts. It should also land safely before the deadline you mention in #21.

### gi...@appspot.gserviceaccount.com (2021-08-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/47aafec6a63fb33855fc044a963ea1d98582b4d4

commit 47aafec6a63fb33855fc044a963ea1d98582b4d4
Author: Jan Krcal <jkrcal@chromium.org>
Date: Fri Aug 20 10:14:24 2021

[Sync consent] Make enterprise checks more robust

This CL passes a WeakPtr instead a raw pointer to one async callback in
the process of enabling sync.

(cherry picked from commit d710b5cdbb18ac8e880afd3c9340106006a9f744)

Bug: 1239595
Change-Id: I5f79456a153a1be52dcac692b59b4322af35893c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3097837
Auto-Submit: Jan Krcal <jkrcal@chromium.org>
Commit-Queue: Yann Dago <ydago@chromium.org>
Reviewed-by: Yann Dago <ydago@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#912287}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3109985
Commit-Queue: Jan Krcal <jkrcal@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4606@{#162}
Cr-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}

[modify] https://crrev.com/47aafec6a63fb33855fc044a963ea1d98582b4d4/chrome/browser/ui/webui/signin/dice_turn_sync_on_helper_delegate_impl.cc


### gi...@appspot.gserviceaccount.com (2021-08-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e6287018f202c1f29533c04fe2acef8682969c43

commit e6287018f202c1f29533c04fe2acef8682969c43
Author: Jan Krcal <jkrcal@chromium.org>
Date: Fri Aug 20 14:20:31 2021

[Sync consent] Make enterprise checks more robust

This CL passes a WeakPtr instead a raw pointer to one async callback in
the process of enabling sync.

Compared to the original CL, this CL includes a trivial conflict
resolution (not affecting the code at all). The functions in M93 pass
around |email| instead of encapsulating struct |account_info| in M94+.

(cherry picked from commit d710b5cdbb18ac8e880afd3c9340106006a9f744)

Bug: 1239595
Change-Id: I5f79456a153a1be52dcac692b59b4322af35893c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3097837
Auto-Submit: Jan Krcal <jkrcal@chromium.org>
Commit-Queue: Yann Dago <ydago@chromium.org>
Reviewed-by: Yann Dago <ydago@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#912287}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3110045
Reviewed-by: Marc Treib <treib@chromium.org>
Commit-Queue: Marc Treib <treib@chromium.org>
Cr-Commit-Position: refs/branch-heads/4577@{#988}
Cr-Branched-From: 761ddde228655e313424edec06497d0c56b0f3c4-refs/heads/master@{#902210}

[modify] https://crrev.com/e6287018f202c1f29533c04fe2acef8682969c43/chrome/browser/ui/webui/signin/dice_turn_sync_on_helper_delegate_impl.cc


### am...@chromium.org (2021-08-25)

Thank you! And apologies - one last one since this was FoundIn-92, please go ahead and merge to branch 4515. M92 will be the Extended Stable release as M93 gets promoted to Stable and we transition to the 4W stable channel release cycle. Thanks!

### am...@google.com (2021-08-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-08-25)

Thank you for this report! The VRP panel has decided to award you $5000 for this report. Nice finding and we appreciate you reporting it to us! 

### wx...@gmail.com (2021-08-26)

Thanks a lot 😊

### wx...@gmail.com (2021-08-26)

Oh, I found that the fix is not complete, I submit a new https://crbug.com/chromium/1243556.
Feel free to merge into this.

### gi...@appspot.gserviceaccount.com (2021-08-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b9aac92988ade33b262ab46bbf7727cc2f7207da

commit b9aac92988ade33b262ab46bbf7727cc2f7207da
Author: Jan Krcal <jkrcal@chromium.org>
Date: Fri Aug 27 07:01:15 2021

[Sync consent] Make enterprise checks more robust

This CL passes a WeakPtr instead a raw pointer to one async callback in
the process of enabling sync.

Compared to the original CL, this CL includes two trivial conflict
resolution (not affecting the code at all):
 - The functions in M92 pass around |email| instead of encapsulating
   struct |account_info| in M94+.
 - M94+ has a new piece of code behind a feature toggle that the original
   CL is also touching; this change is obviously omitted for M92.

(cherry picked from commit d710b5cdbb18ac8e880afd3c9340106006a9f744)

Bug: 1239595
Change-Id: I5f79456a153a1be52dcac692b59b4322af35893c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3097837
Auto-Submit: Jan Krcal <jkrcal@chromium.org>
Commit-Queue: Yann Dago <ydago@chromium.org>
Reviewed-by: Yann Dago <ydago@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#912287}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3122986
Reviewed-by: Marc Treib <treib@chromium.org>
Commit-Queue: Marc Treib <treib@chromium.org>
Cr-Commit-Position: refs/branch-heads/4515@{#2088}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[modify] https://crrev.com/b9aac92988ade33b262ab46bbf7727cc2f7207da/chrome/browser/ui/webui/signin/dice_turn_sync_on_helper_delegate_impl.cc


### am...@google.com (2021-08-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-08-30)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-31)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-03)

[Empty comment from Monorail migration]

### as...@google.com (2021-09-08)

[Empty comment from Monorail migration]

### as...@google.com (2021-09-08)

[Empty comment from Monorail migration]

### ma...@google.com (2021-09-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f0c435c669c0ec2536b6ffa432d2c26179bbc051

commit f0c435c669c0ec2536b6ffa432d2c26179bbc051
Author: Jan Krcal <jkrcal@chromium.org>
Date: Fri Sep 10 12:42:19 2021

[M90-LTS][Sync consent] Make enterprise checks more robust

This CL passes a WeakPtr instead a raw pointer to one async callback in
the process of enabling sync.

Compared to the original CL, this CL includes two trivial conflict
resolution (not affecting the code at all):
 - The functions in M92 pass around |email| instead of encapsulating
   struct |account_info| in M94+.
 - M94+ has a new piece of code behind a feature toggle that the original
   CL is also touching; this change is obviously omitted for M92.

(cherry picked from commit d710b5cdbb18ac8e880afd3c9340106006a9f744)

(cherry picked from commit b9aac92988ade33b262ab46bbf7727cc2f7207da)

Bug: 1239595
Change-Id: I5f79456a153a1be52dcac692b59b4322af35893c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3097837
Auto-Submit: Jan Krcal <jkrcal@chromium.org>
Commit-Queue: Yann Dago <ydago@chromium.org>
Reviewed-by: Yann Dago <ydago@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#912287}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3122986
Reviewed-by: Marc Treib <treib@chromium.org>
Commit-Queue: Marc Treib <treib@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4515@{#2088}
Cr-Original-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3147750
Reviewed-by: Jana Grill <janagrill@google.com>
Reviewed-by: Jan Krcal <jkrcal@chromium.org>
Owners-Override: Jana Grill <janagrill@google.com>
Commit-Queue: Artem Sumaneev <asumaneev@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1593}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/f0c435c669c0ec2536b6ffa432d2c26179bbc051/chrome/browser/ui/webui/signin/dice_turn_sync_on_helper_delegate_impl.cc


### as...@google.com (2021-09-10)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1239595?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056878)*
