# Security: UAF in PasswordProtectionRequest

| Field | Value |
|-------|-------|
| **Issue ID** | [40054147](https://issues.chromium.org/issues/40054147) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | xi...@chromium.org |
| **Created** | 2020-12-11 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**

If the Help-Improve-Security feature is enabled, a sampled\_ping request[1] will be sent when checking the whitelist. And if the serialized information is too large, the request will finish immediately[2]. This will erase the request from |pending\_requests\_|[3], and then the UAF will be triggered when the |finish()|[4] is called.

[1]. <https://source.chromium.org/chromium/chromium/src/+/master:components/safe_browsing/content/password_protection/password_protection_request.cc;l=195;drc=4e69945675d6aa53455a418ffc764b313842a3ee>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/master:components/safe_browsing/content/password_protection/password_protection_request.cc;l=490;drc=4e69945675d6aa53455a418ffc764b313842a3ee>  

[3]. <https://source.chromium.org/chromium/chromium/src/+/master:components/safe_browsing/content/password_protection/password_protection_service.cc;l=304;drc=4e69945675d6aa53455a418ffc764b313842a3ee>  

[4]. <https://source.chromium.org/chromium/chromium/src/+/master:components/safe_browsing/content/password_protection/password_protection_request.cc;l=197;drc=4e69945675d6aa53455a418ffc764b313842a3ee>

**VERSION**  

Chrome Version: stable  

Operating System: All

**REPRODUCTION CASE**

1. Apply the attached patch.diff (\*)
2. Enable "Help improve security on the web for everyone" or "Enhanced protection" in the security setting
3. $ python -m SimpleHTTPServer  
   
   $ out/asan/chrome --user-data-dir=/tmp/xxxx "<http://localhost:8000/poc.html>"  
   
   click "Trigger" button

\*: Renderer patch to emulates a compromised renderer. And the byte\_size patch is to trigger the vulnerability more easily, otherwise, you need to increase the request length through |host\_to\_ip\_map\_|[1] combined with DNS hijacking.  

[1]. <https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/safe_browsing/safe_browsing_navigation_observer_manager.cc;l=617;drc=88e61553f87f7cd0a44ef84c77158af975317e49>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Alpha Lab

## Attachments

- [asan](attachments/asan) (text/plain, 21.9 KB)
- [patch.diff](attachments/patch.diff) (text/plain, 4.8 KB)
- [poc.html](attachments/poc.html) (text/plain, 441 B)

## Timeline

### [Deleted User] (2020-12-11)

[Empty comment from Monorail migration]

### wf...@chromium.org (2020-12-11)

Thanks for your report. xinghuilu I wonder if you could look at this bug?

[Monorail components: Services>Safebrowsing]

### xi...@chromium.org (2020-12-11)

Thanks for the report. I think the root cause of the issue is that "FillRequestProto(/*is_sampled_ping=*/true)" has an implicit branch[1] that causes "delete this", so any code that is added after "FillRequestProto" can cause potential UAF.

Here "Finish()"[2] is called after "FillRequestProto", which can cause UAF.

I think the easiest fix would be to remove the following check: https://source.chromium.org/chromium/chromium/src/+/master:components/safe_browsing/content/password_protection/password_protection_request.cc;l=490-493;drc=58ff9e17fba96d56e68842b570b37d88a70d7f73.
I think this is safe because according to the metric[3], REQUEST_MALFORMED is never triggered. And removing this check could eliminate the branch that causes "delete this".

bdea@/vakh@, as the owner of this file, would you agree with the above fix, or do you have other thoughts?

[1] FillRequestProto -> SendRequest -> Finish -> pasword_protection_service_.RequestFinished -> pending_requests.erase(this).
[2] https://source.chromium.org/chromium/chromium/src/+/master:components/safe_browsing/content/password_protection/password_protection_request.cc;l=197;drc=4e69945675d6aa53455a418ffc764b313842a3ee
[3] https://uma.googleplex.com/p/chrome/timeline_v2?sid=912dee79884b24e7fdd184eaf78741c6

### [Deleted User] (2020-12-12)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xi...@chromium.org (2020-12-14)

[Empty comment from Monorail migration]

### va...@chromium.org (2020-12-14)

Thanks for the report! The fix proposed in https://crbug.com/chromium/1157814#c3 is reasonable to mitigate the issue at hand for now (thanks for investigating), but the long term fix may be slightly different.

I'll review https://crrev.com/c/2589016 for now, but would you mind creating a separate restricted bug for the follow-up discussion?

### xi...@chromium.org (2020-12-14)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/70519702552b9edef59bd6478629ea41c00c4d7e

commit 70519702552b9edef59bd6478629ea41c00c4d7e
Author: Xinghui Lu <xinghuilu@chromium.org>
Date: Tue Dec 15 02:36:47 2020

Remove request malformed check in password_protection_request

See https://crbug.com/1157814#c3 for the reasoning of this change.

Bug: 1157814
Change-Id: I33a81991fd108ddaf23f5d796941d1347f17ca9b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2589016
Reviewed-by: Varun Khaneja <vakh@chromium.org>
Commit-Queue: Xinghui Lu <xinghuilu@chromium.org>
Cr-Commit-Position: refs/heads/master@{#836930}

[modify] https://crrev.com/70519702552b9edef59bd6478629ea41c00c4d7e/components/safe_browsing/content/password_protection/password_protection_request.cc


### ad...@google.com (2020-12-15)

xinghuilu@ is the commit in https://crbug.com/chromium/1157814#c8 complete? If so please mark this as Fixed so that sheriffbot initiates merge proceedings. Thanks!

### xi...@chromium.org (2020-12-15)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-16)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-16)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-16)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M87. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M88. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-16)

This bug requires manual review: M88's targeted beta branch promotion date has already passed, so this requires manual review
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
Owners: govind@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xi...@chromium.org (2020-12-16)

1 Yes
2 https://crrev.com/c/2589016
3 Yes
4 Yes, also needs to be merged into M87.
5 Security bug identified after branch point.
6 No
7 N/A

### bi...@google.com (2020-12-17)

[Empty comment from Monorail migration]

### go...@chromium.org (2020-12-17)

+adetaylor@ (Security TPM) for M87 and M88 merge review. 

### ad...@chromium.org (2020-12-17)

Approving merge to M88, branch 4324.

I'm not going to approve merge to M87 at this point without a few more days in Canary, and given the impending break, I'm not sure we'll be able to get that before the next and final M87 release on ~4th Jan. So I suspect we'll ship this in M88.

### xi...@chromium.org (2020-12-17)

Thanks Adrian. Created https://crrev.com/c/2597876. CQ is running.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0936c2b8c112b007573d740d1eb8513b56c6888e

commit 0936c2b8c112b007573d740d1eb8513b56c6888e
Author: Xinghui Lu <xinghuilu@chromium.org>
Date: Thu Dec 17 23:35:25 2020

[M88] Remove request malformed check in password_protection_request

See https://crbug.com/1157814#c3 for the reasoning of this change.

(cherry picked from commit 70519702552b9edef59bd6478629ea41c00c4d7e)

Bug: 1157814
Change-Id: I33a81991fd108ddaf23f5d796941d1347f17ca9b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2589016
Reviewed-by: Varun Khaneja <vakh@chromium.org>
Commit-Queue: Xinghui Lu <xinghuilu@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#836930}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2597876
Reviewed-by: Xinghui Lu <xinghuilu@chromium.org>
Cr-Commit-Position: refs/branch-heads/4324@{#1039}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/0936c2b8c112b007573d740d1eb8513b56c6888e/components/safe_browsing/content/password_protection/password_protection_request.cc


### ad...@google.com (2020-12-30)

OK, assuming this is looking good in Canary, I'm approving merge to M87, branch 4280.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fa472699f1c5879d650eeb2b88a49988755a497c

commit fa472699f1c5879d650eeb2b88a49988755a497c
Author: Xinghui Lu <xinghuilu@chromium.org>
Date: Wed Dec 30 03:42:16 2020

[M87] Remove request malformed check in password_protection_request

See https://crbug.com/1157814#c3 for the reasoning of this change.

(cherry picked from commit 70519702552b9edef59bd6478629ea41c00c4d7e)

Bug: 1157814
Change-Id: I33a81991fd108ddaf23f5d796941d1347f17ca9b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2589016
Reviewed-by: Varun Khaneja <vakh@chromium.org>
Commit-Queue: Xinghui Lu <xinghuilu@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#836930}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2606629
Reviewed-by: Xinghui Lu <xinghuilu@chromium.org>
Cr-Commit-Position: refs/branch-heads/4280@{#1965}
Cr-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}

[modify] https://crrev.com/fa472699f1c5879d650eeb2b88a49988755a497c/components/safe_browsing/content/password_protection/password_protection_request.cc


### ad...@google.com (2021-01-05)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-06)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-07)

[Empty comment from Monorail migration]

### ac...@chromium.org (2021-01-08)

[Empty comment from Monorail migration]

### ke...@google.com (2021-01-08)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ecc347a9acddb7886c0e7b68a07b0fa9364a4a05

commit ecc347a9acddb7886c0e7b68a07b0fa9364a4a05
Author: Xinghui Lu <xinghuilu@chromium.org>
Date: Sat Jan 09 20:35:54 2021

[M86-LTS] Remove request malformed check in password_protection_request

See https://crbug.com/1157814#c3 for the reasoning of this change.

(cherry picked from commit 70519702552b9edef59bd6478629ea41c00c4d7e)

(cherry picked from commit fa472699f1c5879d650eeb2b88a49988755a497c)

Bug: 1157814
Change-Id: I33a81991fd108ddaf23f5d796941d1347f17ca9b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2589016
Reviewed-by: Varun Khaneja <vakh@chromium.org>
Commit-Queue: Xinghui Lu <xinghuilu@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#836930}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2606629
Reviewed-by: Xinghui Lu <xinghuilu@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4280@{#1965}
Cr-Original-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2617032
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1508}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/ecc347a9acddb7886c0e7b68a07b0fa9364a4a05/components/safe_browsing/content/password_protection/password_protection_request.cc


### [Deleted User] (2021-01-12)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-01-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-01-14)

Congratulations! The VRP panel has decided to award you $20,000 for this report! Great job and thank you!

### ad...@google.com (2021-01-14)

[Empty comment from Monorail migration]

### ja...@google.com (2021-01-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-15)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-01-15)

[Empty comment from Monorail migration]

### ja...@google.com (2021-01-19)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### xi...@chromium.org (2021-02-09)

[Empty comment from Monorail migration]

### ad...@google.com (2021-02-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2021-03-24)

Hi leecraso@ - we consider attachments/pocs included with reports to be an integral part of the report, so I've un-deleted them. Thanks!


### xi...@chromium.org (2021-03-24)

This issue should not affect iOS because PasswordProtectionRequest is built on iOS in https://crrev.com/c/2654426 (02/01/2021) and the fix of this bug is in https://crrev.com/c/2589016 (12/14/2020).

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1157814?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/1158582]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054147)*
