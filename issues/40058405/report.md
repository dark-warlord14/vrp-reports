# Security: UAF in safe_browsing::DownloadRequestMaker::Start

| Field | Value |
|-------|-------|
| **Issue ID** | [40058405](https://issues.chromium.org/issues/40058405) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | dy...@gmail.com |
| **Assignee** | xi...@chromium.org |
| **Created** | 2022-01-05 |
| **Bounty** | $20,000.00 |

## Description

redacted

## Attachments

- [chooser.html](attachments/chooser.html) (text/plain, 1.6 KB)
- [download.html](attachments/download.html) (text/plain, 503 B)
- [copy_mojo_js_bindings.py](attachments/copy_mojo_js_bindings.py) (text/plain, 512 B)
- [crash-0.asan](attachments/crash-0.asan) (text/plain, 26.2 KB)
- [crash-1.asan](attachments/crash-1.asan) (text/plain, 37.0 KB)
- [crash-1-non-incognito.asan](attachments/crash-1-non-incognito.asan) (text/plain, 22.1 KB)
- [crash-2.asan](attachments/crash-2.asan) (text/plain, 29.0 KB)

## Timeline

### [Deleted User] (2022-01-05)

[Empty comment from Monorail migration]

### dr...@chromium.org (2022-01-05)

I was able to reproduce this crash in M96 as well. As a renderer sandbox escape, marking High Severity. xinghuilu@ - can you take a look?

[Monorail components: Services>Safebrowsing]

### [Deleted User] (2022-01-05)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-01-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-07)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-01-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1d9300c6ec561931739e5e756a15b81c0e775139

commit 1d9300c6ec561931739e5e756a15b81c0e775139
Author: Xinghui Lu <xinghuilu@chromium.org>
Date: Fri Jan 14 01:35:00 2022

Remove pending download requests before the profile is destroyed.

Currently, CheckClientDownloadRequestBase holds a raw pointer of
browser_context. If the function is triggered after the profile is
destroyed, it will cause UAF.

In this CL, let SafeBrowsingService notify DownloadProtectionService
that the profile is going to be destroyed, and DownloadProtectionService
will delete all pending requests that are associated with this profile.

A long term fix would be making the DownloadProtectionService a keyed
service and removing the pending requests directly during shutdown. This
fix will be addressed in a future CL.

Bug: 1284584
Change-Id: I540735a0ca522c98db34d4bb8c766601d4e41a8a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3381677
Reviewed-by: Daniel Rubery <drubery@chromium.org>
Commit-Queue: Xinghui Lu <xinghuilu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#958965}

[modify] https://crrev.com/1d9300c6ec561931739e5e756a15b81c0e775139/chrome/browser/safe_browsing/download_protection/download_protection_service_unittest.cc
[modify] https://crrev.com/1d9300c6ec561931739e5e756a15b81c0e775139/chrome/browser/safe_browsing/services_delegate_desktop.h
[modify] https://crrev.com/1d9300c6ec561931739e5e756a15b81c0e775139/chrome/browser/safe_browsing/services_delegate.h
[modify] https://crrev.com/1d9300c6ec561931739e5e756a15b81c0e775139/chrome/browser/safe_browsing/safe_browsing_service.cc
[modify] https://crrev.com/1d9300c6ec561931739e5e756a15b81c0e775139/chrome/browser/safe_browsing/download_protection/download_protection_service.h
[modify] https://crrev.com/1d9300c6ec561931739e5e756a15b81c0e775139/chrome/browser/safe_browsing/download_protection/download_protection_service.cc
[modify] https://crrev.com/1d9300c6ec561931739e5e756a15b81c0e775139/chrome/browser/safe_browsing/services_delegate_desktop.cc


### xi...@chromium.org (2022-01-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-14)

Requesting merge to extended stable M96 because latest trunk commit (958965) appears to be after extended stable branch point (929512).

Requesting merge to stable M97 because latest trunk commit (958965) appears to be after stable branch point (938553).

Requesting merge to beta M98 because latest trunk commit (958965) appears to be after beta branch point (950365).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-15)

Merge review required: M98 is already shipping to beta.

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-15)

Merge review required: M97 is already shipping to stable.

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
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-15)

Merge review required: M96 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xi...@chromium.org (2022-01-15)

1. Security fix.
2. https://crrev.com/c/3381677
3. Yes.
4. No.
5. N/A
6. No.

### am...@chromium.org (2022-01-18)

[Comment Deleted]

### am...@chromium.org (2022-01-18)

upon further review, there was insufficient canary coverage to approve for merge review at this time, will revisit tomorrow or Thursday for merge approval 

### am...@google.com (2022-01-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-20)

Congratulations! The VRP Panel has decided to award you $20,000 for this report. A member of our finance team will be in touch soon to arrange payment. In the meantime, please let us know what name/handle/other identifier you would like us to use to publicly acknowledge you for this issue. 
Thank you for your efforts and excellent report! 

### dy...@gmail.com (2022-01-21)

Thanks a lot, please credit to 'avaue at S.S.L'.

### am...@chromium.org (2022-01-21)

Merge approved for M98, please go ahead and merge this fix to branch 4758 before 11am PST, Tuesday, 25 January 2021 so this fix can be included in the stable cut for M98 -- thank you! 

### am...@google.com (2022-01-22)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-01-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/524b01441d1acbca385df54d82720fccbd48f168

commit 524b01441d1acbca385df54d82720fccbd48f168
Author: Xinghui Lu <xinghuilu@chromium.org>
Date: Sat Jan 22 03:23:36 2022

[M98] Remove pending download requests before the profile is destroyed.

Currently, CheckClientDownloadRequestBase holds a raw pointer of
browser_context. If the function is triggered after the profile is
destroyed, it will cause UAF.

In this CL, let SafeBrowsingService notify DownloadProtectionService
that the profile is going to be destroyed, and DownloadProtectionService
will delete all pending requests that are associated with this profile.

A long term fix would be making the DownloadProtectionService a keyed
service and removing the pending requests directly during shutdown. This
fix will be addressed in a future CL.

(cherry picked from commit 1d9300c6ec561931739e5e756a15b81c0e775139)

Bug: 1284584
Change-Id: I540735a0ca522c98db34d4bb8c766601d4e41a8a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3381677
Reviewed-by: Daniel Rubery <drubery@chromium.org>
Commit-Queue: Xinghui Lu <xinghuilu@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#958965}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3399612
Auto-Submit: Xinghui Lu <xinghuilu@chromium.org>
Cr-Commit-Position: refs/branch-heads/4758@{#825}
Cr-Branched-From: 4a2cf4baf90326df19c3ee70ff987960d59a386e-refs/heads/main@{#950365}

[modify] https://crrev.com/524b01441d1acbca385df54d82720fccbd48f168/chrome/browser/safe_browsing/download_protection/download_protection_service_unittest.cc
[modify] https://crrev.com/524b01441d1acbca385df54d82720fccbd48f168/chrome/browser/safe_browsing/services_delegate_desktop.h
[modify] https://crrev.com/524b01441d1acbca385df54d82720fccbd48f168/chrome/browser/safe_browsing/services_delegate.h
[modify] https://crrev.com/524b01441d1acbca385df54d82720fccbd48f168/chrome/browser/safe_browsing/safe_browsing_service.cc
[modify] https://crrev.com/524b01441d1acbca385df54d82720fccbd48f168/chrome/browser/safe_browsing/download_protection/download_protection_service.h
[modify] https://crrev.com/524b01441d1acbca385df54d82720fccbd48f168/chrome/browser/safe_browsing/download_protection/download_protection_service.cc
[modify] https://crrev.com/524b01441d1acbca385df54d82720fccbd48f168/chrome/browser/safe_browsing/services_delegate_desktop.cc


### [Deleted User] (2022-01-22)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xi...@chromium.org (2022-01-25)

1. No. AFAICT, this issue can be introduced as early as 2019, when native file system API was integrated with Safe Browsing.
2. No. This is a non-regression issue.

### am...@chromium.org (2022-01-31)

[Empty comment from Monorail migration]

### vo...@google.com (2022-02-01)

[Empty comment from Monorail migration]

### vo...@google.com (2022-02-01)

[Empty comment from Monorail migration]

### vo...@google.com (2022-02-01)

[Empty comment from Monorail migration]

### vo...@google.com (2022-02-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-01)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-01)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vo...@google.com (2022-02-01)

1. Just one https://crrev.com/c/3427761
2. Low - no conflicts
3. Stable - M98
4. Yes

### gm...@google.com (2022-02-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-01)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-02-01)

[Empty comment from Monorail migration]

### gm...@google.com (2022-02-04)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-02-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5491d2bacedc0eae10318b57675a1e98e230fb68

commit 5491d2bacedc0eae10318b57675a1e98e230fb68
Author: Xinghui Lu <xinghuilu@chromium.org>
Date: Mon Feb 21 15:18:50 2022

[M96-LTS] Remove pending download requests before the profile is destroyed.

Currently, CheckClientDownloadRequestBase holds a raw pointer of
browser_context. If the function is triggered after the profile is
destroyed, it will cause UAF.

In this CL, let SafeBrowsingService notify DownloadProtectionService
that the profile is going to be destroyed, and DownloadProtectionService
will delete all pending requests that are associated with this profile.

A long term fix would be making the DownloadProtectionService a keyed
service and removing the pending requests directly during shutdown. This
fix will be addressed in a future CL.

(cherry picked from commit 1d9300c6ec561931739e5e756a15b81c0e775139)

(cherry picked from commit 524b01441d1acbca385df54d82720fccbd48f168)

Bug: 1284584
Change-Id: I540735a0ca522c98db34d4bb8c766601d4e41a8a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3381677
Commit-Queue: Xinghui Lu <xinghuilu@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/main@{#958965}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3399612
Auto-Submit: Xinghui Lu <xinghuilu@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4758@{#825}
Cr-Original-Branched-From: 4a2cf4baf90326df19c3ee70ff987960d59a386e-refs/heads/main@{#950365}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3427761
Reviewed-by: Jana Grill <janagrill@google.com>
Owners-Override: Jana Grill <janagrill@google.com>
Commit-Queue: Zakhar Voit <voit@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1493}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/5491d2bacedc0eae10318b57675a1e98e230fb68/chrome/browser/safe_browsing/download_protection/download_protection_service_unittest.cc
[modify] https://crrev.com/5491d2bacedc0eae10318b57675a1e98e230fb68/chrome/browser/safe_browsing/services_delegate.h
[modify] https://crrev.com/5491d2bacedc0eae10318b57675a1e98e230fb68/chrome/browser/safe_browsing/services_delegate_desktop.h
[modify] https://crrev.com/5491d2bacedc0eae10318b57675a1e98e230fb68/chrome/browser/safe_browsing/safe_browsing_service.cc
[modify] https://crrev.com/5491d2bacedc0eae10318b57675a1e98e230fb68/chrome/browser/safe_browsing/download_protection/download_protection_service.h
[modify] https://crrev.com/5491d2bacedc0eae10318b57675a1e98e230fb68/chrome/browser/safe_browsing/download_protection/download_protection_service.cc
[modify] https://crrev.com/5491d2bacedc0eae10318b57675a1e98e230fb68/chrome/browser/safe_browsing/services_delegate_desktop.cc


### vo...@google.com (2022-02-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1284584?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058405)*
