# Security: use after free in AccountReconcilor

| Field | Value |
|-------|-------|
| **Issue ID** | [40060165](https://issues.chromium.org/issues/40060165) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | wx...@gmail.com |
| **Assignee** | ms...@chromium.org |
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

- [0001-trigger-uaf.patch](attachments/0001-trigger-uaf.patch) (text/plain, 1.3 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 33.0 KB)
- [0001-fix-uaf.patch](attachments/0001-fix-uaf.patch) (text/plain, 1.3 KB)

## Timeline

### [Deleted User] (2022-07-05)

[Empty comment from Monorail migration]

### wx...@gmail.com (2022-07-05)

https://source.chromium.org/chromium/chromium/src/+/main:components/signin/core/browser/account_reconcilor.cc;l=612
```c++
  if (chrome_accounts_changed_) {
    chrome_accounts_changed_ = false;
    SetState(AccountReconcilorState::ACCOUNT_RECONCILOR_SCHEDULED);
    base::ThreadTaskRunnerHandle::Get()->PostTask(
        FROM_HERE, base::BindOnce(&AccountReconcilor::StartReconcile,
                                  base::Unretained(this),  // use base::unretain(this)
                                  Trigger::kTokenChangeDuringReconcile));
```

AccountReconcilor is KeyedService, will be destoryed when profile destoryed.

I use my patch to win race condition, and I didn't see any check in this class.
If you have any questions, please tell me, thanks.



### da...@chromium.org (2022-07-05)

This patch is injecting code into the browser process, at which point the browser would already be compromised. Can you provide a way to reproduce this without changing the browser process code?

### wx...@gmail.com (2022-07-05)

You can see the comments（https://bugs.chromium.org/p/chromium/issues/detail?id=1337676#c11）  and cc the developer 

### [Deleted User] (2022-07-05)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@chromium.org (2022-07-05)

Ok I have looked again. I see that AccountReconcilor is posting a task with `this` bound as the receiver, via Unretained. Posting a task loses all control of what happens next.

The owner of AccountReconcilor is KeyedServiceFactory, which is a general container and has no means to watch for the posted callback and wait for it to complete.

With BRP raw_ptr, the `this` object will be poisoned but not freed (where BRP is enabled).

The post-task was last changed in early 2021:

Commit b9e210c : droger@chromium.org @ 2021-05-04 6:59 AM
[signin] Add per-trigger histograms for AccountReconcilor


[Monorail components: Services>SignIn]

### [Deleted User] (2022-07-05)

[Empty comment from Monorail migration]

### da...@chromium.org (2022-07-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-06)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ms...@chromium.org (2022-07-07)

[Empty comment from Monorail migration]

### ms...@chromium.org (2022-07-07)

I do not think we have a real attack (or am I wrong) - it is a UAF that we need to fix though. Note that this crash occurs when a profile is destroyed, so in general on browser shut-down.

I think we should just fix it for the next release branch.

danakj@chromium.org: Do you agree?

### dr...@chromium.org (2022-07-07)

I agree that it's a bug.
It's really not new, it was already here in 2014 (e.g. https://codereview.chromium.org/197283019/diff/280001/chrome/browser/signin/account_reconcilor.cc).
It happens at profile destruction (if it ever happens at all, it seems it would be super hard to trigger in practice), which means mostly at shutdown.

I don't think this is urgent at all, fixing it on trunk should be enough.

### dr...@chromium.org (2022-07-07)

tentatively assigning to msalama. I suspect we can fix it by using weak ptr instead.

### gi...@appspot.gserviceaccount.com (2022-07-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f65ea3435ff2a10b4e1ce1f855863e8eaa127a04

commit f65ea3435ff2a10b4e1ce1f855863e8eaa127a04
Author: Monica Basta <msalama@chromium.org>
Date: Fri Jul 08 14:29:30 2022

[Signin] Use WeakPtr in AccountReconcilor to avoid UAF

Bug: 1341907
Change-Id: I14e8d263e3a5f073d61677fedd53c67395382742
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3749680
Commit-Queue: David Roger <droger@chromium.org>
Reviewed-by: David Roger <droger@chromium.org>
Commit-Queue: Monica Basta <msalama@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1022147}

[modify] https://crrev.com/f65ea3435ff2a10b4e1ce1f855863e8eaa127a04/components/signin/core/browser/account_reconcilor.cc


### ms...@chromium.org (2022-07-10)

Thank you, Monica, for fixing this security bug so quickly!

### ms...@chromium.org (2022-07-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-12)

Requesting merge to extended stable M102 because latest trunk commit (1022147) appears to be after extended stable branch point (992738).

Requesting merge to stable M103 because latest trunk commit (1022147) appears to be after stable branch point (1002911).

Requesting merge to beta M104 because latest trunk commit (1022147) appears to be after beta branch point (1012729).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-12)

Merge review required: M104 is already shipping to beta.

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

### [Deleted User] (2022-07-12)

Merge review required: M103 is already shipping to stable.

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

### [Deleted User] (2022-07-12)

Merge review required: M102 is already shipping to stable.

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

### am...@chromium.org (2022-07-12)

reducing to medium severity given race condition and is a shutdown bug 

### am...@chromium.org (2022-07-12)

M104 merge approved, please merge this fix to branch 5112 at your earliest convenience 

### am...@chromium.org (2022-07-12)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-07-13)

Congratulations on another one! The VRP Panel has decided to award you $5,000 for this report. The reward amount was decided upon due to this issue being fairly mitigated by race condition and being a shutdown bug. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-07-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-18)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-07-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b12a45a640cdb7f4c28b1a27cb950858566df238

commit b12a45a640cdb7f4c28b1a27cb950858566df238
Author: Monica Basta <msalama@chromium.org>
Date: Tue Jul 19 07:49:03 2022

[Signin] Use WeakPtr in AccountReconcilor to avoid UAF

(cherry picked from commit f65ea3435ff2a10b4e1ce1f855863e8eaa127a04)

Bug: 1341907
Change-Id: I14e8d263e3a5f073d61677fedd53c67395382742
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3749680
Commit-Queue: David Roger <droger@chromium.org>
Reviewed-by: David Roger <droger@chromium.org>
Commit-Queue: Monica Basta <msalama@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1022147}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3770271
Reviewed-by: Monica Basta <msalama@chromium.org>
Cr-Commit-Position: refs/branch-heads/5112@{#1011}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[modify] https://crrev.com/b12a45a640cdb7f4c28b1a27cb950858566df238/components/signin/core/browser/account_reconcilor.cc


### [Deleted User] (2022-07-19)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ms...@chromium.org (2022-07-19)

1. No it was already here in 2014
2. No

### rz...@google.com (2022-07-20)

[Empty comment from Monorail migration]

### rz...@google.com (2022-07-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-21)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-07-21)

1. https://crrev.com/c/3776596
2. Low, no conflicts
3. 104
4. Yes

### gm...@google.com (2022-07-25)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-02)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-09)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-09)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-08-09)

1. Just https://crrev.com/c/3818943
2. Low, no conflicts
3. 104
4. Yes

### gm...@google.com (2022-08-11)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/845f4235571d244b420d5d0a716d1e6d03c8faa9

commit 845f4235571d244b420d5d0a716d1e6d03c8faa9
Author: Monica Basta <msalama@chromium.org>
Date: Fri Aug 12 15:02:43 2022

[M96-LTS][Signin] Use WeakPtr in AccountReconcilor to avoid UAF

(cherry picked from commit f65ea3435ff2a10b4e1ce1f855863e8eaa127a04)

Bug: 1341907
Change-Id: I14e8d263e3a5f073d61677fedd53c67395382742
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3749680
Commit-Queue: David Roger <droger@chromium.org>
Commit-Queue: Monica Basta <msalama@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1022147}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3776596
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Owners-Override: Oleh Lamzin <lamzin@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1680}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/845f4235571d244b420d5d0a716d1e6d03c8faa9/components/signin/core/browser/account_reconcilor.cc


### gi...@appspot.gserviceaccount.com (2022-08-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/86c9cf088dc89aad2a8253034207a6fdf6fa0498

commit 86c9cf088dc89aad2a8253034207a6fdf6fa0498
Author: Monica Basta <msalama@chromium.org>
Date: Fri Aug 12 15:21:53 2022

[M102-LTS][Signin] Use WeakPtr in AccountReconcilor to avoid UAF

(cherry picked from commit f65ea3435ff2a10b4e1ce1f855863e8eaa127a04)

Bug: 1341907
Change-Id: I14e8d263e3a5f073d61677fedd53c67395382742
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3749680
Commit-Queue: David Roger <droger@chromium.org>
Commit-Queue: Monica Basta <msalama@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1022147}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3818943
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Owners-Override: Oleh Lamzin <lamzin@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1299}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/86c9cf088dc89aad2a8253034207a6fdf6fa0498/components/signin/core/browser/account_reconcilor.cc


### rz...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-12)

[Empty comment from Monorail migration]

### lz...@google.com (2022-10-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1341907?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1342197, crbug.com/chromium/1371844]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060165)*
