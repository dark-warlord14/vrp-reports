# Security: chrome.devtools.inspectedWindow.eval can bypass enterprise-policy blocked hosts using subframes

| Field | Value |
|-------|-------|
| **Issue ID** | [40068096](https://issues.chromium.org/issues/40068096) |
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

Currently, devtools extensions should not able to interact with enterprise-policy blocked hosts.

However, it can be trivially bypassed by using a subframe with the enterprise-policy blocked hosts.

This allows devtools extenstion to steal and modify data in the policy blocked hosts.

This is because in <https://source.chromium.org/chromium/chromium/src/+/main:third_party/devtools-frontend/src/front_end/models/extensions/ExtensionServer.ts;l=1214> we do not further check for runtime blocked hosts

REPRO:

1. Add <https://example.org> to runtime blocked hosts
2. Add

## Code in <https://foregoing-ballistic-brand.glitch.me/devtools-iframe.html>:

<iframe src="https://example.org"></iframe>
---
\*\*VERSION\*\*
Chrome Version: 115.0.5790.102 (Official Build) (64-bit) (cohort: M115\_Early\_stable)
Operating System: Windows 10

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Axel Chong

## Attachments

- [background.js](attachments/background.js) (text/plain, 101 B)
- [devtools.html](attachments/devtools.html) (text/plain, 35 B)
- [manifest.json](attachments/manifest.json) (text/plain, 201 B)
- [devtools.js](attachments/devtools.js) (text/plain, 106 B)

## Timeline

### ha...@gmail.com (2023-07-26)

REPRO:
1. Add https://example.org to runtime blocked hosts
2. Install extension
3. Open devtools on https://foregoing-ballistic-brand.glitch.me/devtools-iframe.html

### [Deleted User] (2023-07-26)

[Empty comment from Monorail migration]

### ha...@gmail.com (2023-07-26)

Also works on latest canary Chrome Version 117.0.5910.0 (Official Build) canary (64-bit)

### ma...@google.com (2023-07-26)

rdevlin.cronin@, same question as 1467743: Should the DevTools API respect runtime_blocked_hosts? 


[Monorail components: Platform>Extensions>API]

### ma...@google.com (2023-07-26)

[Empty comment from Monorail migration]

### ma...@google.com (2023-07-27)

+dsv, +pfaffe for DevTools

(Note that 1467743 is a similar issue. Should we dup them?)

### ha...@gmail.com (2023-07-27)

Hello, reporter here. In my opinion, these 2 reports are similar impact but they talk about different root cause. 

Here this talks about a bypass in latest Chrome Canary as only the main frame is checked against the host policy. While the checks are missing in the subframe -- https://source.chromium.org/chromium/chromium/src/+/main:third_party/devtools-frontend/src/front_end/models/extensions/ExtensionServer.ts;l=1214

1467743 talks about the missing checks for the other chrome.devtools methods such as getResource which allow intercepting of data from runtime blocked hosts.



### ma...@google.com (2023-07-27)

Setting same labels as 1467743 here for now.

### [Deleted User] (2023-07-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-28)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-28)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@gmail.com (2023-07-31)

Draft patch: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4729725

### gi...@appspot.gserviceaccount.com (2023-08-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/27078e36b599a20c33570c94f2e388ef90321fb5

commit 27078e36b599a20c33570c94f2e388ef90321fb5
Author: Philip Pfaffe <pfaffe@chromium.org>
Date: Tue Aug 01 10:54:23 2023

Check subframes against extension permissions

Fixed: 1467751
Change-Id: Iee04d8fa9dfd84ac4ed4b8f4ffb6334fff922c71
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4735433
Reviewed-by: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Philip Pfaffe <pfaffe@chromium.org>

[modify] https://crrev.com/27078e36b599a20c33570c94f2e388ef90321fb5/front_end/models/extensions/ExtensionServer.ts
[modify] https://crrev.com/27078e36b599a20c33570c94f2e388ef90321fb5/test/unittests/front_end/models/extensions/ExtensionServer_test.ts


### ha...@gmail.com (2023-08-01)

Just an additional note to the security team: This bug allows extension to eval() (obtain script access) in the context of the hostnames in subframe which shouldn't be allowed for policy blocked hosts according to

According to https://support.google.com/chrome/a/answer/9031935?hl=en,
"For example, if your developers host code in a third-party code repository, you can block the repository's webpage URL to make sure that Chrome extensions can't steal or modify that code."

which I also mentioned in https://bugs.chromium.org/p/chromium/issues/detail?id=1467743.

### [Deleted User] (2023-08-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-01)

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

### am...@chromium.org (2023-08-03)

116 merge approved for https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4735433; please merge this fix to branch 5845 at your earliest convenience / before EOD Monday 7 August so this fix can be included in the M116/Stable cut 

### gi...@appspot.gserviceaccount.com (2023-08-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/f68d41bbe1536c7e54ba9a5460bf1ca3b943fad6

commit f68d41bbe1536c7e54ba9a5460bf1ca3b943fad6
Author: Philip Pfaffe <pfaffe@chromium.org>
Date: Tue Aug 01 10:54:23 2023

Check subframes against extension permissions

Fixed: 1467751
Change-Id: Iee04d8fa9dfd84ac4ed4b8f4ffb6334fff922c71
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4735433
Reviewed-by: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Philip Pfaffe <pfaffe@chromium.org>
(cherry picked from commit 27078e36b599a20c33570c94f2e388ef90321fb5)
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4748502

[modify] https://crrev.com/f68d41bbe1536c7e54ba9a5460bf1ca3b943fad6/front_end/models/extensions/ExtensionServer.ts
[modify] https://crrev.com/f68d41bbe1536c7e54ba9a5460bf1ca3b943fad6/test/unittests/front_end/models/extensions/ExtensionServer_test.ts


### [Deleted User] (2023-08-07)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pf...@chromium.org (2023-08-07)

1. No.
2. Yes.

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

### [Deleted User] (2023-11-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1467751?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40068096)*
