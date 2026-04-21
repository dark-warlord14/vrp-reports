# Security: heap-buffer-overflow in extension

| Field | Value |
|-------|-------|
| **Issue ID** | [40054376](https://issues.chromium.org/issues/40054376) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Extensions>API |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ga...@gmail.com |
| **Assignee** | co...@chromium.org |
| **Created** | 2021-01-06 |
| **Bounty** | $10,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/master/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

Need certain times of iteration, May crash at second group or 99th group

**VERSION**  

Chrome Version: stable  

Operating System: All

**REPRODUCTION CASE**

1. Install the attached extension.
2. It will crash in several times of iteration.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see attached file

**CREDIT INFORMATION**  

Reporter credit: Allen Parker & Alex Morgan of MU

## Attachments

- [background.js](attachments/background.js) (text/plain, 46 B)
- [asan](attachments/asan) (text/plain, 15.4 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 194 B)
- [poc.html](attachments/poc.html) (text/plain, 43 B)
- [poc.js](attachments/poc.js) (text/plain, 630 B)

## Timeline

### [Deleted User] (2021-01-06)

[Empty comment from Monorail migration]

### bd...@chromium.org (2021-01-06)

@connily, can you take a look at this (as this is related to extensions + tabs) or help find another owner for this? 

[Monorail components: Platform>Extensions>API UI>Browser>TabStrip>TabGroups]

### co...@chromium.org (2021-01-06)

[Empty comment from Monorail migration]

### co...@chromium.org (2021-01-06)

[Empty comment from Monorail migration]

### co...@chromium.org (2021-01-07)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a8728eead1b427868420b003180f17a85e88554b

commit a8728eead1b427868420b003180f17a85e88554b
Author: Connie Wan <connily@chromium.org>
Date: Thu Jan 07 22:05:27 2021

Make grouping and pinning cause less tab movement

Grouping was originally causing two tab movements: one to unpin the tab,
then another to group. Reducing this to a single movement reduces the
potential for race conditions when rapidly pinning and grouping/unpinning
tabs.

Tested manually and via existing unit tests:
https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/tabs/tab_strip_model_unittest.cc;l=3175

Bug: 1163504
Change-Id: Id2dd3a682afe0d6c8798a7f8f287c5431cd22805
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2613520
Reviewed-by: Charlene Yan <cyan@chromium.org>
Commit-Queue: Connie Wan <connily@chromium.org>
Cr-Commit-Position: refs/heads/master@{#841212}

[modify] https://crrev.com/a8728eead1b427868420b003180f17a85e88554b/chrome/browser/ui/tabs/tab_strip_model.cc


### co...@chromium.org (2021-01-07)

Thanks for this report! I believe the change I just made should address this particular issue in MoveWebContents from the conflict of pinning vs. grouping.

However, I haven't been able to test the repro directly because loading infinite-looping extensions in a test understandably causes other issues.

The change should be available with the next Canary, so I may be able to test more then to verify a fix.

### [Deleted User] (2021-01-08)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-01-08)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### co...@chromium.org (2021-01-15)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-15)

Requesting merge to beta M88 because latest trunk commit (841212) appears to be after beta branch point (827102).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-01-15)

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
Owners: govind@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### co...@chromium.org (2021-01-15)

1. Yes, since this was automatically slated for merge as a security bug.
2. https://chromium-review.googlesource.com/c/chromium/src/+/2613520
3. Yes.
4. No.
5. I'm personally not sure if it is, but since it's a medium-level security issue it was automatically slated for merge.
6. No.
7. No.

### [Deleted User] (2021-01-16)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-01-21)

Congratulations! The VRP Panel has decided to award you $10,000 for this report! A member of our finance team will be reaching out to you soon to arrange payment. Thank you for your report and excellent work! 

### am...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-26)

(note to self: landed before M89 branch). I'll likely go through and approve M88 merges for the next security refresh on Thursday.

### ad...@google.com (2021-01-27)

I think this is High severity, as a browser crash mitigated only by the need for an extension.

Approving merge to M88, branch 4324. Please merge, assuming no problems have shown up in Canary.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/162ae5bc9da32003f1e4009edb09a3a7a3eb76a9

commit 162ae5bc9da32003f1e4009edb09a3a7a3eb76a9
Author: Connie Wan <connily@chromium.org>
Date: Wed Jan 27 20:53:18 2021

Make grouping and pinning cause less tab movement (merge)

Grouping was originally causing two tab movements: one to unpin the tab,
then another to group. Reducing this to a single movement reduces the
potential for race conditions when rapidly pinning and grouping/unpinning
tabs.

Tested manually and via existing unit tests:
https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/tabs/tab_strip_model_unittest.cc;l=3175

(cherry picked from commit a8728eead1b427868420b003180f17a85e88554b)

Bug: 1163504
Change-Id: Id2dd3a682afe0d6c8798a7f8f287c5431cd22805
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2613520
Reviewed-by: Charlene Yan <cyan@chromium.org>
Commit-Queue: Connie Wan <connily@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#841212}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2653711
Cr-Commit-Position: refs/branch-heads/4324@{#2032}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/162ae5bc9da32003f1e4009edb09a3a7a3eb76a9/chrome/browser/ui/tabs/tab_strip_model.cc


### ad...@google.com (2021-01-29)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-31)

[Empty comment from Monorail migration]

### as...@google.com (2021-02-02)

[Empty comment from Monorail migration]

### as...@google.com (2021-02-02)

Marking as not applicable for LTS since introducing code landed in M88.
connily@, please confirm.

### co...@chromium.org (2021-02-02)

Yes I believe this should just be targeting M88. Thanks!

### am...@google.com (2021-02-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1163504?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054376)*
