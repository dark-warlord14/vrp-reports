# Security: Extension Has Access to File URL Despite Access is Disabled

| Field | Value |
|-------|-------|
| **Issue ID** | [40067954](https://issues.chromium.org/issues/40067954) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | fa...@gmail.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2023-07-24 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

Extensions are not allowed to execute scripts in File URLs when 'Allow access to file URLs' is disabled. However, using chrome.devtools.inspectedWindow.eval, an extension can execute a script inside a File URL. Below is a proof-of-concept demonstrating this.

**VERSION**  

Chrome Version: 117.0.5897.4 (Official Build) dev (64-bit) (cohort: Dev experiment)  

Operating System: Windows 11

**REPRODUCTION CASE**

1. Load the attached extension.
2. Observe an alert on file URL (Allow access to file URLs is disabled).

**CREDIT INFORMATION**  

Reporter credit: Shaheen Fazim

## Attachments

- [devtools.js](attachments/devtools.js) (text/plain, 116 B)
- [manifest.json](attachments/manifest.json) (text/plain, 181 B)
- [background.js](attachments/background.js) (text/plain, 82 B)
- [devtools.html](attachments/devtools.html) (text/plain, 35 B)
- [background.js](attachments/background.js) (text/plain, 141 B)
- [devtools.js](attachments/devtools.js) (text/plain, 298 B)
- [devtools.html](attachments/devtools.html) (text/plain, 35 B)
- [manifest.json](attachments/manifest.json) (text/plain, 181 B)
- [poc.mp4](attachments/poc.mp4) (video/mp4, 2.6 MB)

## Timeline

### fa...@gmail.com (2023-07-24)

[Comment Deleted]

### [Deleted User] (2023-07-24)

[Empty comment from Monorail migration]

### fa...@gmail.com (2023-07-24)

Here, an attacker could modify the proof-of-concept to lure the victim into launching inspect via shortcut or from the menu and then execute the script on restricted file URLs. Additionally, the attacker could exploit the XMLHttpRequest() function to send the data to a remote host.

### fa...@gmail.com (2023-07-24)

[Empty comment from Monorail migration]

### fa...@gmail.com (2023-07-24)

similar issues: crbug.com/1428743, crbug.com/1349146

### fl...@google.com (2023-07-24)

Thanks for the PoC +  the link to similar issues in the past; they're very helpful for triage.

I think there's indeed a bug here, quite similar to 1349146 (both in terms of what it's exploiting + what that's mitigated by).  I'm assigning to rdevlin—can you confirm my assessment here?  (Want a second opinion since this is an extensions thing.)  And if so, can you assign someone to fix?

(cc'ing in dsv@ since they fixed the last similar issue).

[Monorail components: Platform>Extensions]

### [Deleted User] (2023-07-24)

[Empty comment from Monorail migration]

### rd...@chromium.org (2023-07-24)

If this still repros (I know we've fixed a few similar issues lately), it is indeed a bug.  Assigning to dsv@ to investigate.

### gi...@appspot.gserviceaccount.com (2023-07-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/21a7422d80485d1157e5ca84d75c605c4cb75f35

commit 21a7422d80485d1157e5ca84d75c605c4cb75f35
Author: Danil Somsikov <dsv@chromium.org>
Date: Tue Jul 25 08:24:44 2023

Do not allow extensions without file access on file: URLs

Bug: 1467169
Change-Id: Ic663af79bc9a2b6b60368e59515735f6cba57a1c
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4714725
Auto-Submit: Danil Somsikov <dsv@chromium.org>
Reviewed-by: Philip Pfaffe <pfaffe@chromium.org>
Commit-Queue: Danil Somsikov <dsv@chromium.org>

[modify] https://crrev.com/21a7422d80485d1157e5ca84d75c605c4cb75f35/front_end/models/extensions/ExtensionServer.ts
[modify] https://crrev.com/21a7422d80485d1157e5ca84d75c605c4cb75f35/front_end/core/host/InspectorFrontendHostAPI.ts
[modify] https://crrev.com/21a7422d80485d1157e5ca84d75c605c4cb75f35/test/unittests/front_end/models/extensions/helpers.ts


### [Deleted User] (2023-07-25)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-25)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ds...@chromium.org (2023-07-26)

[Empty comment from Monorail migration]

### ds...@chromium.org (2023-07-26)

[Empty comment from Monorail migration]

### be...@google.com (2023-07-26)

Adding Hotlist-RBS-Removed for tracking purposes.

### [Deleted User] (2023-07-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-28)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-08-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8e7c54daa7fc3691cf7a15df5f384f82b787ea73

commit 8e7c54daa7fc3691cf7a15df5f384f82b787ea73
Author: Danil Somsikov <dsv@chromium.org>
Date: Thu Aug 03 09:32:08 2023

Test for devtool extension access to file target without file access.

Bug: 1467169
Change-Id: I59eba062e5636db1b3a4e5ec7c2ea0dccd5422af
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4711731
Auto-Submit: Danil Somsikov <dsv@chromium.org>
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1178912}

[modify] https://crrev.com/8e7c54daa7fc3691cf7a15df5f384f82b787ea73/chrome/browser/devtools/devtools_browsertest.cc
[modify] https://crrev.com/8e7c54daa7fc3691cf7a15df5f384f82b787ea73/chrome/test/data/devtools/extensions/can_inspect_url/devtools.js


### am...@google.com (2023-08-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-03)

Congratulations Shaheen! The VRP Panel has decided to award you $5,000 for this report of a web platform privilege escalation / exploit mitigation bypass. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us -- nice work! 

### fa...@gmail.com (2023-08-03)

Thank you for the prompt fix and reward. :D

### ds...@chromium.org (2023-08-04)

[Empty comment from Monorail migration]

### ds...@chromium.org (2023-08-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-04)

Merge review required: M116 is already shipping to beta.

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
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-08-04)

M116 merge approved for https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4714725
Please merge this fix to branch 5435 before EOD Monday, 7 August so this fix can be included in M116 Stable RC 

### am...@chromium.org (2023-08-04)

Typo in branch number above, should be 5845 for M116! 

### gi...@appspot.gserviceaccount.com (2023-08-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/b4b5024f5cf13be00561eeac7e1541c287e6265a

commit b4b5024f5cf13be00561eeac7e1541c287e6265a
Author: Danil Somsikov <dsv@chromium.org>
Date: Tue Jul 25 08:24:44 2023

[M116] Do not allow extensions without file access on file: URLs

Bug: 1467169
Change-Id: Ic663af79bc9a2b6b60368e59515735f6cba57a1c
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4714725
Auto-Submit: Danil Somsikov <dsv@chromium.org>
Reviewed-by: Philip Pfaffe <pfaffe@chromium.org>
Commit-Queue: Danil Somsikov <dsv@chromium.org>
(cherry picked from commit 21a7422d80485d1157e5ca84d75c605c4cb75f35)
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4752853
Reviewed-by: Yang Guo <yangguo@chromium.org>

[modify] https://crrev.com/b4b5024f5cf13be00561eeac7e1541c287e6265a/front_end/models/extensions/ExtensionServer.ts
[modify] https://crrev.com/b4b5024f5cf13be00561eeac7e1541c287e6265a/front_end/core/host/InspectorFrontendHostAPI.ts
[modify] https://crrev.com/b4b5024f5cf13be00561eeac7e1541c287e6265a/test/unittests/front_end/models/extensions/helpers.ts


### [Deleted User] (2023-08-04)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2023-08-05)

[Empty comment from Monorail migration]

### ds...@chromium.org (2023-08-07)

No to both for LTS M114 questions

### vo...@google.com (2023-08-24)

[Empty comment from Monorail migration]

### rz...@google.com (2023-08-30)

Labelling as not applicable because of the comment in https://crrev.com/c/4788031

### rz...@google.com (2023-08-30)

[Empty comment from Monorail migration]

### vo...@google.com (2023-09-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-05)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vo...@google.com (2023-09-07)

1. One - https://crrev.com/c/4788032 but depends on 5 more changes from https://crbug.com/1451146 and https://crbug.com/1429353
2. Medium - no conflicts but depends on 5 more changes (they are already in review or approved for M114 LTS)
3. M116
4. Yes, after we merge the previous changes

### gm...@google.com (2023-09-18)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-09-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/60b0f14f4cf3bef06c3f1a9deb43c38002145ba1

commit 60b0f14f4cf3bef06c3f1a9deb43c38002145ba1
Author: Danil Somsikov <dsv@chromium.org>
Date: Tue Jul 25 08:24:44 2023

[M114-LTS] Do not allow extensions without file access on file: URLs

Bug: 1467169
Change-Id: Ic663af79bc9a2b6b60368e59515735f6cba57a1c
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4714725
Auto-Submit: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Danil Somsikov <dsv@chromium.org>
(cherry picked from commit 21a7422d80485d1157e5ca84d75c605c4cb75f35)
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4752853
(cherry picked from commit b4b5024f5cf13be00561eeac7e1541c287e6265a)
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4788032
Reviewed-by: Victor Gabriel Savu <vsavu@google.com>
Reviewed-by: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Zakhar Voit <voit@google.com>

[modify] https://crrev.com/60b0f14f4cf3bef06c3f1a9deb43c38002145ba1/front_end/models/extensions/ExtensionServer.ts
[modify] https://crrev.com/60b0f14f4cf3bef06c3f1a9deb43c38002145ba1/front_end/core/host/InspectorFrontendHostAPI.ts
[modify] https://crrev.com/60b0f14f4cf3bef06c3f1a9deb43c38002145ba1/test/unittests/front_end/models/extensions/helpers.ts


### vo...@google.com (2023-09-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1467169?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40067954)*
