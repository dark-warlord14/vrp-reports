# Security: chrome.devtools.inspectedWindow.getResources allows resources from enterprise policy-blocked hosts

| Field | Value |
|-------|-------|
| **Issue ID** | [40068091](https://issues.chromium.org/issues/40068091) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions>API |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2023-07-26 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Extensions shouldn't be able to interact with enterprise policy-blocked hosts

According to <https://support.google.com/chrome/a/answer/9031935?hl=en>,  

"For example, if your developers host code in a third-party code repository, you can block the repository's webpage URL to make sure that Chrome extensions can't steal or modify that code."

But chrome.devtools.inspectedWindow.getResources allows resources from enterprise policy-blocked hosts, which means a devtools extension can steal data from enterprise policy-blocked hosts.

**VERSION**  

Chrome Version: 115.0.5790.102 (Official Build) (64-bit) (cohort: M115\_Early\_stable)  

Operating System: Windows 10

**REPRODUCTION CASE**

1. Add <https://example.org> to runtime\_blocked\_hosts
2. Install the extension.
3. Open devtools and the alert with <https://example.org> contents should have popped up.

## HTML in <https://foregoing-ballistic-brand.glitch.me/devtools.html>:

<script>
//# sourceMappingURL=data:application/json,{"version":3,"sources":["https://example.org"]}
</script>

---

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Axel Chong

## Attachments

- [manifest.json](attachments/manifest.json) (text/plain, 201 B)
- [devtools.js](attachments/devtools.js) (text/plain, 230 B)
- [devtools.html](attachments/devtools.html) (text/plain, 35 B)
- [background.js](attachments/background.js) (text/plain, 94 B)

## Timeline

### [Deleted User] (2023-07-26)

[Empty comment from Monorail migration]

### ha...@gmail.com (2023-07-26)

To add runtime_blocked_hosts 

Go to regedit.exe on windows,

Computer\HKEY_CURRENT_USER\SOFTWARE\Policies\Google\Chrome

and add a new key 

ExtensionSettings

with value 

{"*":{"runtime_blocked_hosts":["*://example.org"]}}


### ha...@gmail.com (2023-07-26)

Also works on latest canary Chrome Version 117.0.5910.0 (Official Build) canary (64-bit)

### ma...@google.com (2023-07-26)

rdevlin.cronin@, should the DevTools API respect runtime_blocked_hosts? Also see 1467751 for the same question.

[Monorail components: Platform>Extensions>API]

### ma...@google.com (2023-07-26)

[Empty comment from Monorail migration]

### ha...@gmail.com (2023-07-26)

martinkr@, reporter here. To help answer your question, I just saw https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4684217 which fixes the runtime_blocked_hosts issue for Devtools API. So this is essentially a bypass of that fix (since it also works on Canary version.)

### rd...@chromium.org (2023-07-27)

-> dsv@ , +pfaffe@ for devtools

### ha...@gmail.com (2023-07-27)

Should also add them to 1467751 as well

### ma...@google.com (2023-07-27)

I'll set security labels here for now. DevTools folks, please confirm whether we should consider this a security issue.


### [Deleted User] (2023-07-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-28)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-28)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-08-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/1b4c7f814524c8a96499273734b2595338d1d941

commit 1b4c7f814524c8a96499273734b2595338d1d941
Author: Philip Pfaffe <pfaffe@chromium.org>
Date: Wed Aug 02 15:59:19 2023

Check page resources against extension permissions

When accessing the contents of page resources or network requests, check
against extension permissions. It's still possible to enumerate
resources or requests including those for unpermitted URLs, but
accessing their content is prevented.

Fixed: 1467743
Change-Id: I36d0ed38da4429eb1d064f3483efdee9d5565482
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4738687
Reviewed-by: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Philip Pfaffe <pfaffe@chromium.org>

[modify] https://crrev.com/1b4c7f814524c8a96499273734b2595338d1d941/front_end/models/extensions/ExtensionServer.ts
[modify] https://crrev.com/1b4c7f814524c8a96499273734b2595338d1d941/test/unittests/front_end/models/extensions/ExtensionServer_test.ts


### [Deleted User] (2023-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-03)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M116. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [116].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-04)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M116. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [116].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-05)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M116. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [116].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-06)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M116. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [116].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pf...@chromium.org (2023-08-07)

1. https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4738687
2. Yes (117.0.5928.0)
3. No (restricted to devtools extensions)
4. No
5. No

### am...@chromium.org (2023-08-07)

https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4738687 approved for merge to M116
please merge this fix to branch 5845 by EOD today (Monday) so this fix can be included in M116 Stable cut -- thanks! 

### gi...@appspot.gserviceaccount.com (2023-08-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/b08875a73231d5ef270313ce894eaa831cc6fd08

commit b08875a73231d5ef270313ce894eaa831cc6fd08
Author: Philip Pfaffe <pfaffe@chromium.org>
Date: Wed Aug 02 15:59:19 2023

Check page resources against extension permissions

When accessing the contents of page resources or network requests, check
against extension permissions. It's still possible to enumerate
resources or requests including those for unpermitted URLs, but
accessing their content is prevented.

Fixed: 1467743
Change-Id: I36d0ed38da4429eb1d064f3483efdee9d5565482
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4738687
Reviewed-by: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Philip Pfaffe <pfaffe@chromium.org>
(cherry picked from commit 1b4c7f814524c8a96499273734b2595338d1d941)
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4757141
Reviewed-by: Yang Guo <yangguo@chromium.org>
Reviewed-by: Eric Leese <leese@chromium.org>

[modify] https://crrev.com/b08875a73231d5ef270313ce894eaa831cc6fd08/front_end/models/extensions/ExtensionServer.ts
[modify] https://crrev.com/b08875a73231d5ef270313ce894eaa831cc6fd08/test/unittests/front_end/models/extensions/ExtensionServer_test.ts


### [Deleted User] (2023-08-07)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pf...@chromium.org (2023-08-08)

1. No
2. Yes

### am...@google.com (2023-08-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-10)

Thank you for this report, Axel! We have decided to award you a total of $1,000 reward across this issue and 1467743 for the combined information that you have shared across both reports. While we have begun considering bypasses of enterprise policy as security issues, security impact and reward amounts are based on the policy being bypassed and the consequences of the bypass being reporting. The reward amount, therefore, is based on the limited security impact to users. Thank you for your efforts and reporting this issue to us. 

### am...@chromium.org (2023-08-11)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-14)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### vo...@google.com (2023-08-17)

[Empty comment from Monorail migration]

### rz...@google.com (2023-08-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1467743?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40068091)*
