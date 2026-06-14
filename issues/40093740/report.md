# Security: Hostname not elided securely (URL spoofing on iOS)

| Field | Value |
|-------|-------|
| **Issue ID** | [40093740](https://issues.chromium.org/issues/40093740) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Omnibox, UI>Browser>Omnibox>SecurityIndicators |
| **Platforms** | iOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | rk...@google.com |
| **Created** | 2019-01-13 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: 72.0.3626.51  

Operating System: iOS 12.1.2

**REPRODUCTION CASE**

1. Load the testcase
2. Click on "Click here to go to Google.com"
3. Click on the omnibox quickly, then you will see an alert
4. Click on 'OK' or 'Cancel'
5. Wait >> You will see :

<http://wwww.manage-myaccount.paypal.com>....

instead of showing:

http://....bntk.pl

## Attachments

- [9D3458ED-D984-4B21-A837-C451E24DF476.MOV](attachments/9D3458ED-D984-4B21-A837-C451E24DF476.MOV) (video/quicktime, 836.8 KB)
- [testcase.html](attachments/testcase.html) (text/plain, 676 B)

## Timeline

### ch...@gmail.com (2019-01-13)

[Empty comment from Monorail migration]

### ch...@gmail.com (2019-01-13)

this is similar to https://crbug.com/chromium/798224

### rs...@chromium.org (2019-01-14)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Omnibox UI>Browser>Omnibox>SecurityIndicators]

### st...@chromium.org (2019-01-14)

It seems like the toolbar is stuck in expanded mode when the JS alert fires. 

### sh...@chromium.org (2019-01-15)

[Empty comment from Monorail migration]

### st...@chromium.org (2019-01-24)

To rkgibson@ for evaluation. Also, this won't be fixed in 72 given the low severity.  

### sh...@chromium.org (2019-01-28)

rkgibson: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### no...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### rk...@google.com (2019-01-28)

I have a CL out for this. One question I have is whether we should merge this into M73. I don't think the security impact is that large, as the steps to trigger this are pretty specific, but I'm not sure what the general protocol for this is.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-01-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/df5b958678c91506562ccea5088ebefe473fc785

commit df5b958678c91506562ccea5088ebefe473fc785
Author: Robbie Gibson <rkgibson@google.com>
Date: Mon Jan 28 18:24:13 2019

[iOS] Fixed omnibox state being corrupted after presenting js alert

This CL fixes a bug where the omnibox state would be incorrect after
presenting a javascript alert in the middle of opening a new tab.
The root cause is that the omnibox focus methods are called in the
middle of a previous animation, so they were ignored. To fix this, we
store the expected final state of the omnibox, and set the state to that
after the animations finish.

Bug: 921390
Change-Id: Ibd4e8e857621344e4397153400e6dc4b43617c5c
Reviewed-on: https://chromium-review.googlesource.com/c/1434285
Commit-Queue: Robbie Gibson <rkgibson@google.com>
Reviewed-by: Stepan Khapugin <stkhapugin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#626618}


### rk...@google.com (2019-01-28)

This fix is a bit complicated to verify, as the triggering behavior requires some quick actions in a specific order. It took me a few tries to be able to reproduce it consistently.

### aw...@google.com (2019-01-28)

[Empty comment from Monorail migration]

### na...@google.com (2019-01-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-29)

[Empty comment from Monorail migration]

### na...@google.com (2019-01-31)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-01-31)

Congrats! The Panel decided to reward $500 for this report :)

### na...@google.com (2019-01-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-09)

This bug requires manual review: Less than 27 days to go before AppStore submit on M73
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ka...@google.com (2019-02-11)

rkgibson per c11, can we try reproducing on canary at least? I think it's worth a few tries to verifiy this fix before merging.

### rk...@google.com (2019-02-12)

I was just trying on canary and I believe it looks fine there. Let me know what the next steps should be before merging.

### ka...@chromium.org (2019-02-13)

Thank you. Approved, please merge asap.

### cr...@appspot.gserviceaccount.com (2019-02-15)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/45bb31aaecdc93c8a1f1bb16abf57adc44dfd2b7

Commit: 45bb31aaecdc93c8a1f1bb16abf57adc44dfd2b7
Author: rkgibson@google.com
Commiter: stkhapugin@chromium.org
Date: 2019-02-15 14:01:32 +0000 UTC

[iOS] Fixed omnibox state being corrupted after presenting js alert

This CL fixes a bug where the omnibox state would be incorrect after
presenting a javascript alert in the middle of opening a new tab.
The root cause is that the omnibox focus methods are called in the
middle of a previous animation, so they were ignored. To fix this, we
store the expected final state of the omnibox, and set the state to that
after the animations finish.

Bug: 921390
Change-Id: Ibd4e8e857621344e4397153400e6dc4b43617c5c
Reviewed-on: https://chromium-review.googlesource.com/c/1434285
Commit-Queue: Robbie Gibson <rkgibson@google.com>
Reviewed-by: Stepan Khapugin <stkhapugin@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#626618}(cherry picked from commit df5b958678c91506562ccea5088ebefe473fc785)
Reviewed-on: https://chromium-review.googlesource.com/c/1475435
Cr-Commit-Position: refs/branch-heads/3683@{#455}
Cr-Branched-From: e51029943e0a38dd794b73caaf6373d5496ae783-refs/heads/master@{#625896}

### rk...@google.com (2019-02-15)

Ok, this should have been merged.

### aw...@google.com (2019-03-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-05-22)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/921390?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Omnibox, UI>Browser>Omnibox>SecurityIndicators]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093740)*
