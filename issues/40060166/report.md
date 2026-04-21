# Security: use after free in DiceWebSigninInterceptor

| Field | Value |
|-------|-------|
| **Issue ID** | [40060166](https://issues.chromium.org/issues/40060166) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Fuchsia, Linux, Mac, Windows |
| **Reporter** | wx...@gmail.com |
| **Assignee** | yd...@chromium.org |
| **Created** | 2022-07-05 |
| **Bounty** | $5,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**

**VERSION**  

**Chrome Version: [x.x.x.x] + [stable, beta, or dev]**  

**Operating System: [Please indicate OS, version, and service pack level]**  

windows

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug, or any personal or confidential information.**

**Please attach files directly, not in zip or other archive formats, and if**  

**you've created a demonstration site please also attach the files needed to**  

**reproduce the demonstration locally.**

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

**Reporter credit: [goes here]**

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 28.4 KB)
- [0001-trigger.patch](attachments/0001-trigger.patch) (text/plain, 1.3 KB)

## Timeline

### wx...@gmail.com (2022-07-05)

```c++
class ForcedProfileSwitchInterceptionHandle
    : public ScopedDiceWebSigninInterceptionBubbleHandle {
 public:
  explicit ForcedProfileSwitchInterceptionHandle(
      base::OnceCallback<void(SigninInterceptionResult)> callback) {
    DCHECK(callback);
    base::ThreadTaskRunnerHandle::Get()->PostTask(
        FROM_HERE, base::BindOnce(std::move(callback), // post the callback
                                  SigninInterceptionResult::kAccepted));
  }
  ~ForcedProfileSwitchInterceptionHandle() override = default;
};
```

the callback from -->DiceWebSigninInterceptorDelegate::ShowSigninInterceptionBubble 
--> DiceWebSigninInterceptor::ShowSigninInterceptionBubble 
--> DiceWebSigninInterceptor::OnInterceptionReadyToBeProcessed
```
  base::OnceCallback<void(SigninInterceptionResult)> callback;
  switch (*interception_type) {
    case SigninInterceptionType::kProfileSwitch:
    case SigninInterceptionType::kProfileSwitchForced:
      callback = base::BindOnce(
          &DiceWebSigninInterceptor::OnProfileSwitchChoice,
          base::Unretained(this), info.email, switch_to_entry->GetPath()); // our callback 
```

DiceWebSigninInterceptor is a keyed serivce, when profile destoryed, base::unretain(this) callback will be uaf.

### [Deleted User] (2022-07-05)

[Empty comment from Monorail migration]

### da...@chromium.org (2022-07-05)

This patch is injecting code into the browser process, at which point the browser would already be compromised. Can you provide a way to reproduce this without changing the browser process code?


### wx...@gmail.com (2022-07-05)

You can see the comments（https://bugs.chromium.org/p/chromium/issues/detail?id=1337676#c11）  and cc the developer

### [Deleted User] (2022-07-05)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@chromium.org (2022-07-05)

Ok, it would help a lot if you can provide a POC that isn't changing the code, and itself introducing the bug. Obviously introducing a bug doesn't indicate Chrome has a bug.

From what I can see, the point here is:

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/signin/dice_web_signin_interceptor.cc;l=595-597;drc=da646affa40e760be86f075dd5f0e7a0b7ebc766

DiceWebSigninInterceptor::ShowSigninInterceptionBubble() binds itself with Unretained into a callback.

DiceWebSigninInterceptor's lifetime is tied to the profile. But the callback is not cancelled if the profile is gone.

It's not obvious to me that you can indeed cause the callback to run after the profile is gone without injecting C++. Can you please provide evidence of this?

### wx...@gmail.com (2022-07-05)

Ok, I can't provide a poc without charge its code, because the flow is complex. But you can see the code flow, it will post the task to thread without any check.

### [Deleted User] (2022-07-05)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@chromium.org (2022-07-05)

I don't see the callback being posted in this call stack, I see it being stored in ForcedEnterpriseSigninInterceptionHandle.

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/signin/dice_web_signin_interceptor_delegate.cc;drc=da646affa40e760be86f075dd5f0e7a0b7ebc766;l=55

And later it is run from that class synchronously, not posted.

If this is a UAF we should address it, but I can't confirm how it would be one, without adding a call to a function that doesn't really happen.

If you can find more information here to explain how it would occur, then we can work on this bug.

[Monorail components: Services>SignIn]

### wx...@gmail.com (2022-07-05)

```c++
DiceWebSigninInterceptorDelegate::ShowSigninInterceptionBubble(
    content::WebContents* web_contents,
    const BubbleParameters& bubble_parameters,
    base::OnceCallback<void(SigninInterceptionResult)> callback) {
  if (bubble_parameters.interception_type ==
      DiceWebSigninInterceptor::SigninInterceptionType::kProfileSwitchForced) {
    return std::make_unique<ForcedProfileSwitchInterceptionHandle>(
        std::move(callback));  --->>>>> ForcedProfileSwitchInterceptionHandle
  }
```

then it will enter into 
https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/signin/dice_web_signin_interceptor_delegate.cc;l=35



### wx...@gmail.com (2022-07-05)

you can read the comment https://bugs.chromium.org/p/chromium/issues/detail?id=1341918#c1, I think my analysis is right.

### [Deleted User] (2022-07-05)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@chromium.org (2022-07-05)

I see, thank you. This will happen only when DiceWebSigninInterceptor::ShouldEnforceEnterpriseProfileSeparation() is true. AFAICT this is on in production.

it also requires enable_dice_support in GN, which appears to be enabled on 4 platforms: `enable_dice_support = is_linux || is_mac || is_win || is_fuchsia`

https://source.chromium.org/chromium/chromium/src/+/main:components/signin/features.gni;drc=d73c9038c508528cb2b0c0aef0b94483e0420259;l=8

Since at least:
Commit efab967 : droger@chromium.org @ 2021-12-07 6:50 PM
[Lacros] Define ENABLE_MIRROR and undefine ENABLE_DICE_SUPPORT

The PostTask of the callback was introduced in

Commit ca6c1e3 : ydago@chromium.org @ 2021-07-15 8:34 PM
Use ScopedDiceWebSigninInterceptionBubbleHandle for all interceptions

And the use of the kProfileSwitchForced was last changed in

Commit b30e6d3 : ydago@chromium.org @ Mar 25 5:45 PM
ManagedAccountsSigninRestrictions bypass SigninInterceptionEnabled

Which was part of M102

### [Deleted User] (2022-07-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-06)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dr...@chromium.org (2022-07-13)

Is it somehow a duplicate of https://crbug.com/chromium/1337676?

### wx...@gmail.com (2022-07-13)

similar but not the same

### [Deleted User] (2022-07-20)

ydago: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yd...@chromium.org (2022-07-27)

[Empty comment from Monorail migration]

### yd...@chromium.org (2022-07-28)

This was fixed by https://crrev.com/c/3788885 but did not show up here automatically

### [Deleted User] (2022-07-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-28)

This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M102. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M103. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M104. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M105. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-28)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-28)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-28)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-28)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-08-01)

The original commit for this issue (5e105f0bc3443e873924b92778574ffbb792c645) landed on 105, so merge to 105 is not necessary. 
There are no further planned releases of 103/Stable or 102/Extended, so merge not needed to those branches either. 

This issue should be backmerge to M104 (branch 5112) at your earliest convenience. M104 stable cut has already occurred so this fix should ship in the M104 stable respin. Please be sure to link the CP to M104 with this bug number as that was missed in the initial fix for this issue. Bug fixes being linked to the bugs helps ensure more efficient security and release processes, thank you. 

### am...@google.com (2022-08-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-05)

Congratulations! The VRP Panel has decided to reward you $5,000 for this report. The reward amount was decided upon based on this issue being mitigated by profile destruction. Thank you for your efforts and reporting this issue to us. 

### [Deleted User] (2022-08-05)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-08-08)

[Empty comment from Monorail migration]

### sr...@google.com (2022-08-12)

I have CP'ed the change to M104 here - https://chromium-review.googlesource.com/c/chromium/src/+/3828426 

Please help +1 the CL and land it, I have run it through dry-run CQ, so help with the process

### dr...@chromium.org (2022-08-12)

 srinivassista: I think you pasted the wrong CL above, it seems related to another bug.

### sr...@google.com (2022-08-12)

thanks droger@ i took the CL from amy's https://crbug.com/chromium/1341918#c28 above, which is not the right one, I will revert it now - Revert here - https://chromium-review.googlesource.com/c/chromium/src/+/3829082

Here is the right CL with fix - https://chromium-review.googlesource.com/c/chromium/src/+/3829509 Please confirm this is good

### gi...@appspot.gserviceaccount.com (2022-08-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b672bfdd1a6c1777d9889b449a1049bbcd7c5b70

commit b672bfdd1a6c1777d9889b449a1049bbcd7c5b70
Author: Yann Dago <ydago@chromium.org>
Date: Sat Aug 13 00:15:53 2022

Use CancelableCallback in ForcedProfileSwitchInterceptionHandle to avoid use-after-free

(cherry picked from commit fec4acb18f371436e6dc34d40b73aff3d7bba037)

Bug: 1341918
Change-Id: Ic1cce9b149ba38a9b1d02c2d7568a75ecbed674f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3788885
Auto-Submit: Yann Dago <ydago@chromium.org>
Reviewed-by: David Roger <droger@chromium.org>
Commit-Queue: Yann Dago <ydago@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1028784}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3829509
Reviewed-by: Harry Souders <harrysouders@google.com>
Owners-Override: Srinivas Sista <srinivassista@chromium.org>
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Cr-Commit-Position: refs/branch-heads/5112@{#1462}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[modify] https://crrev.com/b672bfdd1a6c1777d9889b449a1049bbcd7c5b70/chrome/browser/ui/signin/dice_web_signin_interceptor_delegate.cc


### am...@chromium.org (2022-08-16)

commit b672bfdd1a6c1777d9889b449a1049bbcd7c5b70 was merge to 104, however, this fix did not get merged to 105 beta, thanks to the confusion I created in https://crbug.com/chromium/1341918#c28 by using the wrong CL, adding merge labels accordingly -- please merge this fix to branch 5195 asap 

### am...@chromium.org (2022-08-16)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-16)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1c8edb000a393699b1e04519607e623d09db7c5c

commit 1c8edb000a393699b1e04519607e623d09db7c5c
Author: Yann Dago <ydago@chromium.org>
Date: Tue Aug 23 16:27:13 2022

Use CancelableCallback in ForcedProfileSwitchInterceptionHandle to avoid use-after-free

(cherry picked from commit fec4acb18f371436e6dc34d40b73aff3d7bba037)

Bug: 1341918
Change-Id: Ic1cce9b149ba38a9b1d02c2d7568a75ecbed674f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3788885
Auto-Submit: Yann Dago <ydago@chromium.org>
Reviewed-by: David Roger <droger@chromium.org>
Commit-Queue: Yann Dago <ydago@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1028784}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3850701
Owners-Override: Prudhvikumar Bommana <pbommana@google.com>
Commit-Queue: Prudhvikumar Bommana <pbommana@google.com>
Cr-Commit-Position: refs/branch-heads/5195@{#846}
Cr-Branched-From: 7aa3f074a7907975b001346cc0288d0214af8451-refs/heads/main@{#1027018}

[modify] https://crrev.com/1c8edb000a393699b1e04519607e623d09db7c5c/chrome/browser/ui/signin/dice_web_signin_interceptor_delegate.cc


### gm...@google.com (2022-08-30)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-31)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-31)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-31)

 gmpritchard, the bot isn't adding the questionnaire, but here are the answers:

1. Just https://crrev.com/c/3865007
2. Low, no conflicts
3. 104, 105
4. Yes

### [Deleted User] (2022-08-31)

[Empty comment from Monorail migration]

### gm...@google.com (2022-09-06)

[Empty comment from Monorail migration]

### ja...@google.com (2022-09-07)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-09-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/50237fe51fe43611d78751244a15d0684f7dacfc

commit 50237fe51fe43611d78751244a15d0684f7dacfc
Author: Yann Dago <ydago@chromium.org>
Date: Wed Sep 07 10:03:40 2022

[M102-LTS] Use CancelableCallback in ForcedProfileSwitchInterceptionHandle to avoid use-after-free

(cherry picked from commit fec4acb18f371436e6dc34d40b73aff3d7bba037)

Bug: 1341918
Change-Id: Ic1cce9b149ba38a9b1d02c2d7568a75ecbed674f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3788885
Auto-Submit: Yann Dago <ydago@chromium.org>
Commit-Queue: Yann Dago <ydago@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1028784}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3865007
Owners-Override: Jana Grill <janagrill@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Jana Grill <janagrill@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1339}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/50237fe51fe43611d78751244a15d0684f7dacfc/chrome/browser/ui/signin/dice_web_signin_interceptor_delegate.cc


### rz...@google.com (2022-09-07)

[Empty comment from Monorail migration]

### rz...@google.com (2022-09-13)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1341918?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060166)*
