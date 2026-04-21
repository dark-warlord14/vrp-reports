# Security: Use after free in Payments

| Field | Value |
|-------|-------|
| **Issue ID** | [40052949](https://issues.chromium.org/issues/40052949) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>Payments |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | np...@chromium.org |
| **Created** | 2020-07-28 |
| **Bounty** | $20,000.00 |

## Description

Chrome Version: 86.0.4214.3 (Official Build) canary (x86\_64)  

Operating System: MacOS

**REPRODUCTION CASE**

1. Go to <https://lbstyle.github.io/payments.html> and click on "Continue"
2. Then open <https://lbstyle.github.io/crash-payments.html> on another tab and try to close the first tab => Crash

This is similar to <https://crbug.com/chromium/1065298>.

Crash/a86f7e0bd3a209aa

## Attachments

- [screen_.mp4](attachments/screen_.mp4) (video/mp4, 2.8 MB)
- [poc.html](attachments/poc.html) (text/plain, 1.2 KB)

## Timeline

### ch...@gmail.com (2020-07-28)

Still repro this on 86.0.4215.0 (Official Build) canary (x86_64). Can someone please paste the stack trace by crash/1d00dbcfd8e146a1. - thanks!

### rs...@chromium.org (2020-07-28)

[Empty comment from Monorail migration]

### rs...@chromium.org (2020-07-28)

nburris: Could you look at this? This may be a regression from https://crrev.com/5012d3ea1d61bc163ed1135644b3931a5282a519

It looks like you're already working on the systemic issues in https://crbug.com/chromium/1075687 and may already have an in-progress fix? The pattern (of posting the WebContents to the ServiceWorker thread, as per https://source.chromium.org/chromium/chromium/src/+/master:content/browser/payments/payment_app_provider_impl.cc;l=939;drc=cde04c8156e1a18218257efdede4fde8d776c41c?originalUrl=https:%2F%2Fcs.chromium.org%2F , seems inherently risky.

As this is in the Browser process, I'm inclined to mark this as Security-Critical, but the user-gesture requirement has me flagging this as High. If there's a way to trigger this event without necessitating the user gesture, a severity bump would likely be warranted.

[Monorail components: Blink>Payments]

### np...@chromium.org (2020-07-28)

[Empty comment from Monorail migration]

### np...@chromium.org (2020-07-28)

The crash appears to be the AbortInvokePaymentApp task executing after the WebContents is destroyed. AbortInvokePaymentApp actually only needs a BrowserContext, so my change to make the methods in PaymentAppProviderImpl take a WebContents caused this regression. I'll change that function back to taking a BrowserContext to fix the regression, but yes, https://crbug.com/chromium/1075687 is tracking the wider project of improving memory management in this area in general.

### np...@chromium.org (2020-07-28)

Uploaded https://chromium-review.googlesource.com/c/chromium/src/+/2324041. I can't repro yet but this should fix the crash. The original patch landed in 85.0.4176.0 so the fix will need a merge to Beta.

@Reporter, can you confirm you can also repro the crash on Beta? Does it repro consistently for you? If I can't get it to repro then we can land this and confirm the fix on your end in Canary before merging to Beta.

### ch...@gmail.com (2020-07-28)

This crash doesn't repro consistently, and I couldn't repro it on Beta. Looks like it can take several tries to repro the crash on Beta. but I can confirm the fix on Canary.

### [Deleted User] (2020-07-28)

Setting milestone and target because of Security_Impact=Beta and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-28)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-28)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@gmail.com (2020-07-29)

I have a new testcase which makes repro this more easily than in https://crbug.com/chromium/1110207#c0, the attacker would not need to convince the victim to click Continue.

1. Open PoC.html
2. Click somewhere (it will open https://lbstyle.github.io/crash-payments.html)
3. Then try to close PoC.html tab

### np...@chromium.org (2020-07-29)

Thanks, though I still can't reproduce it with poc.html... I'm landing my fix now, so we'll confirm on the next Canary version whether it's fixed.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/98fa6b892d7d8b0c74f8d9311d1403e1883c1838

commit 98fa6b892d7d8b0c74f8d9311d1403e1883c1838
Author: Nick Burris <nburris@chromium.org>
Date: Wed Jul 29 22:08:24 2020

[Web Payment] Avoid sending WebContents* to service worker

PaymentAppProviderImpl was recently changed[1] to use WebContents*
instead of BrowserContext*, in preparation for making the object owned
by WebContents. However, the service worker logic still needs to use a
BrowserContext* to register callbacks in case it outlives the
WebContents, which is possible in the current state where it's a
singleton. This patch makes it so all service worker logic uses a
BrowserContext*.

Bug: 1110207
Change-Id: Iee16d9cdfc81e2f186226e11be379890d6d66eef
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2324041
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Commit-Queue: Nick Burris <nburris@chromium.org>
Cr-Commit-Position: refs/heads/master@{#792901}

[modify] https://crrev.com/98fa6b892d7d8b0c74f8d9311d1403e1883c1838/content/browser/payments/payment_app_provider_impl.cc


### sr...@google.com (2020-07-30)

This bug is marked as RBS for M85. M85 has been promoted to beta. Please help review this bug if this indeed should block the stable release for M85, if not please remove RBS label, If it is a RBS , please help get a fix ready for merge to M85 asap so we can bake the fix on beta channel asap.

Beta release happens every wednesday and beta RC gets cut on Tuesday afternoon 3pm PST. Please help get the fixes landed and verified on canary so that the changes can be merged in time for beta release.

### np...@chromium.org (2020-07-30)

Reporter, can you confirm with your new test case that this crash is on M85 as well? If we have the correct culprit CL then it should be M85.

The fix in https://crbug.com/chromium/1110207#c13 has landed and will be in the next canary release, which should be available by tomorrow. Once we confirm the fix I'll merge to M85 branch by Tuesday afternoon for the next beta release.

### ch...@gmail.com (2020-07-30)

I can now repro this crash with using the test case in https://crbug.com/chromium/1110207#c11 on 85.0.4183.48 beta.

### ch...@gmail.com (2020-07-31)

I couldn't repro this crash on Chromium 86.0.4219.0. This seems like fixed.

### np...@chromium.org (2020-07-31)

Great, thanks for verifying!

Requesting to merge to M85 Beta branch https://chromium-review.googlesource.com/c/chromium/src/+/2324041

### [Deleted User] (2020-07-31)

This bug requires manual review: M85's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### np...@chromium.org (2020-07-31)

1. Does your merge fit within the Merge Decision Guidelines?

Yes, this is a high severity bug fix.

2. Links to the CLs you are requesting to merge.

https://chromium-review.googlesource.com/c/chromium/src/+/2324041

3. Has the change landed and been verified on master/ToT?

Yes, bugfix verified in latest Canary build.

4. Why are these changes required in this milestone after branch?

Bug discovered after branch

5. Is this a new feature?

No

6. If it is a new feature, is it behind a flag using finch?

N/A

### ch...@gmail.com (2020-07-31)

Thanks @nburris for the fix! - I think you forgot to mark this bug as fixed before requesting merge. 

### np...@chromium.org (2020-07-31)

Marking "fixed" closes the bug, I will wait until the merge lands in beta and the fix is confirmed in the next beta release before marking fixed. I would appreciate your help with verifying the next beta release as well, I'll ping this bug when it rolls out :)

### sr...@google.com (2020-07-31)

Merge approved for M85 branch:4183 please merge asap

### sr...@google.com (2020-08-03)

Please complete your merges to M85 branch before 2pm PST tuesday Aug 4th 2020, so they can be included in this week's beta release.

### [Deleted User] (2020-08-04)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c982753ac36aa16b8983198a18b3a5eebe9fd8a1

commit c982753ac36aa16b8983198a18b3a5eebe9fd8a1
Author: Nick Burris <nburris@chromium.org>
Date: Tue Aug 04 17:30:10 2020

[Web Payment] Avoid sending WebContents* to service worker

PaymentAppProviderImpl was recently changed[1] to use WebContents*
instead of BrowserContext*, in preparation for making the object owned
by WebContents. However, the service worker logic still needs to use a
BrowserContext* to register callbacks in case it outlives the
WebContents, which is possible in the current state where it's a
singleton. This patch makes it so all service worker logic uses a
BrowserContext*.

(cherry picked from commit 98fa6b892d7d8b0c74f8d9311d1403e1883c1838)

Bug: 1110207
Change-Id: Iee16d9cdfc81e2f186226e11be379890d6d66eef
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2324041
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Commit-Queue: Nick Burris <nburris@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#792901}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2332693
Cr-Commit-Position: refs/branch-heads/4183@{#1199}
Cr-Branched-From: 740e9e8a40505392ba5c8e022a8024b3d018ca65-refs/heads/master@{#782793}

[modify] https://crrev.com/c982753ac36aa16b8983198a18b3a5eebe9fd8a1/content/browser/payments/payment_app_provider_impl.cc


### np...@chromium.org (2020-08-04)

NextAction later this week to verify the fix on the next Beta release.

### ch...@gmail.com (2020-08-06)

I'm no longer able to reproduce Beta on 85.0.4183.59.

### np...@chromium.org (2020-08-06)

Great, thanks for confirming the fix!

### [Deleted User] (2020-08-06)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-10)

[Empty comment from Monorail migration]

### mm...@google.com (2020-08-11)

nburris@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### wf...@chromium.org (2020-08-13)

chromium.khalil@gmail.com please do not put PoCs for security bugs on publically accessible websites, please instead attach the entire PoC and reproduction steps so we can reproduce locally, if it requires a local webserver you can state that in the report and we can be sure to run your PoC on a webserver.

### ad...@google.com (2020-08-13)

Discussion at the VRP panel - we think that the POC in https://crbug.com/chromium/1110207#c11 involves little human/manual interaction so this counts as a Critical severity bug.

### ad...@google.com (2020-08-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-08-13)

Congratulations! The VRP panel decided to award $20,000 for this report.

### ad...@google.com (2020-08-13)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-14)

Setting Pri-0 to match security severity Critical. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@chromium.org (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1110207?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/1075687]
[Monorail mergedwith: crbug.com/chromium/1110248]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052949)*
