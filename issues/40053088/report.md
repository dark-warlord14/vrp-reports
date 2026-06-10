# Security: Extensions can capture contents of local files using Page.captureScreenshot

| Field | Value |
|-------|-------|
| **Issue ID** | [40053088](https://issues.chromium.org/issues/40053088) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools, Platform>Extensions |
| **Platforms** | Windows |
| **Reporter** | de...@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2020-08-14 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

When using the chrome.debugger API, one of the methods an extension can call is Page.captureScreenshot. That method allows a screenshot of the frame being debugged to be captured.

Using the fact that a frame can always navigate its descendants, an extension can open a file: page (one that it creates) and have that page navigate a nested frame to another file: location. The extension can then capture the contents of the nested frame using Page.captureScreenshot.

**VERSION**  

Chrome Version: Tested on 84.0.4147.125 (stable) and 86.0.4233.0 (canary)  

Operating System: Windows 10, version 1909

**REPRODUCTION CASE**

1. Install the attached extension. Ensure that "Allow access to file URLs" isn't checked.
2. Once installed, the extension will download local\_file.html.
3. Once the download has completed, the extension will open local\_file.html in a new tab.
4. A script within local\_file.html will add an iframe to the page, with the source being set to iframe.html in the extension (this file is listed under web\_accessible\_resources to ensure that it can be loaded).
5. local\_file.html will then navigate a nested frame contained within iframe.html to file:///c:/.
6. The extension will then attach the debugger to iframe.html and call Page.captureScreenshot.
7. Once the extension has received the screenshot data, it will make the following call:

chrome.tabs.create({url: "data:image/png;base64," + screenshotData});

The resulting tab should show that the contents of the nested file:///c:/ frame have been captured.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [background.js](attachments/background.js) (text/plain, 2.8 KB)
- [iframe.html](attachments/iframe.html) (text/plain, 215 B)
- [iframe.js](attachments/iframe.js) (text/plain, 313 B)
- [local_file.html](attachments/local_file.html) (text/plain, 1.0 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 302 B)

## Timeline

### va...@chromium.org (2020-08-15)

1116444, 1116450 are similar to 1113565 so assigning to caseq@ and adding some other folks as well.

[Monorail components: Platform>DevTools Platform>Extensions]

### [Deleted User] (2020-08-15)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-15)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-28)

caseq: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-09-11)

caseq: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2020-09-16)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-09-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/62c286d1bda3c26b838daef9ec0cfee05e08090d

commit 62c286d1bda3c26b838daef9ec0cfee05e08090d
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Sat Sep 19 01:38:53 2020

Do not execute global commands on non-root targets

Bug: 1116444
Change-Id: Ic50dfc144f8024870131e7586b9dce2dff591e42
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2419712
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/heads/master@{#808635}

[modify] https://crrev.com/62c286d1bda3c26b838daef9ec0cfee05e08090d/content/browser/devtools/protocol/page_handler.cc
[add] https://crrev.com/62c286d1bda3c26b838daef9ec0cfee05e08090d/third_party/blink/web_tests/http/tests/inspector-protocol/main-target-commands-expected.txt
[add] https://crrev.com/62c286d1bda3c26b838daef9ec0cfee05e08090d/third_party/blink/web_tests/http/tests/inspector-protocol/main-target-commands.js


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-09-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fa3dd0b347a6505ec96c9a7875e47695f8a49570

commit fa3dd0b347a6505ec96c9a7875e47695f8a49570
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Sat Sep 19 06:02:05 2020

chrome.debugger extentsions: check permissions to attach to parent targets

... when client attempts to attach to a subframe.

Bug: 1116444
Change-Id: I74bd06cf9b91482a35c035d2e4d064b8ac66adf6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2412799
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#808669}

[modify] https://crrev.com/fa3dd0b347a6505ec96c9a7875e47695f8a49570/chrome/browser/extensions/api/debugger/debugger_api.cc
[modify] https://crrev.com/fa3dd0b347a6505ec96c9a7875e47695f8a49570/chrome/browser/extensions/api/debugger/debugger_apitest.cc
[add] https://crrev.com/fa3dd0b347a6505ec96c9a7875e47695f8a49570/chrome/test/data/extensions/api_test/parent_target_permissions/background.js
[add] https://crrev.com/fa3dd0b347a6505ec96c9a7875e47695f8a49570/chrome/test/data/extensions/api_test/parent_target_permissions/manifest.json
[add] https://crrev.com/fa3dd0b347a6505ec96c9a7875e47695f8a49570/chrome/test/data/extensions/api_test/parent_target_permissions/subframe.html
[add] https://crrev.com/fa3dd0b347a6505ec96c9a7875e47695f8a49570/chrome/test/data/extensions/api_test/parent_target_permissions/subframe.js
[add] https://crrev.com/fa3dd0b347a6505ec96c9a7875e47695f8a49570/chrome/test/data/extensions/api_test/parent_target_permissions/top_page.html


### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### ca...@chromium.org (2020-11-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-03)

Not requesting merge to beta (M87) because latest trunk commit (808669) appears to be prior to beta branch point (812852). If this is incorrect, please replace the Merge-na label with Merge-Request-87. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-11-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-11-11)

Congratulations, the VRP panel has awarded $5,000 for this report.

### ad...@google.com (2020-11-12)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-16)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-16)

[Empty comment from Monorail migration]

### vs...@google.com (2020-12-10)

[Empty comment from Monorail migration]

### vs...@google.com (2020-12-10)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-10)

[Empty comment from Monorail migration]

### ke...@google.com (2020-12-11)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d4fe96b8a84276312f999fbcc9696409cf8f4be5

commit d4fe96b8a84276312f999fbcc9696409cf8f4be5
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Wed Dec 16 18:55:59 2020

chrome.debugger extentsions: check permissions to attach to parent targets

... when client attempts to attach to a subframe.

(cherry picked from commit fa3dd0b347a6505ec96c9a7875e47695f8a49570)

Bug: 1116444
Change-Id: I74bd06cf9b91482a35c035d2e4d064b8ac66adf6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2412799
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#808669}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2584807
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1491}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[add] https://crrev.com/d4fe96b8a84276312f999fbcc9696409cf8f4be5/chrome/test/data/extensions/api_test/parent_target_permissions/background.js
[add] https://crrev.com/d4fe96b8a84276312f999fbcc9696409cf8f4be5/chrome/test/data/extensions/api_test/parent_target_permissions/manifest.json
[modify] https://crrev.com/d4fe96b8a84276312f999fbcc9696409cf8f4be5/chrome/browser/extensions/api/debugger/debugger_api.cc
[add] https://crrev.com/d4fe96b8a84276312f999fbcc9696409cf8f4be5/chrome/test/data/extensions/api_test/parent_target_permissions/subframe.js
[add] https://crrev.com/d4fe96b8a84276312f999fbcc9696409cf8f4be5/chrome/test/data/extensions/api_test/parent_target_permissions/subframe.html
[add] https://crrev.com/d4fe96b8a84276312f999fbcc9696409cf8f4be5/chrome/test/data/extensions/api_test/parent_target_permissions/top_page.html
[modify] https://crrev.com/d4fe96b8a84276312f999fbcc9696409cf8f4be5/chrome/browser/extensions/api/debugger/debugger_apitest.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ec2d20b477337a42f9e1251ade2956dfa460938b

commit ec2d20b477337a42f9e1251ade2956dfa460938b
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Wed Dec 16 19:15:09 2020

Do not execute global commands on non-root targets

(cherry picked from commit 62c286d1bda3c26b838daef9ec0cfee05e08090d)

Bug: 1116444
Change-Id: Ic50dfc144f8024870131e7586b9dce2dff591e42
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2419712
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#808635}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2584806
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1495}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[add] https://crrev.com/ec2d20b477337a42f9e1251ade2956dfa460938b/third_party/blink/web_tests/http/tests/inspector-protocol/main-target-commands.js
[modify] https://crrev.com/ec2d20b477337a42f9e1251ade2956dfa460938b/content/browser/devtools/protocol/page_handler.cc
[add] https://crrev.com/ec2d20b477337a42f9e1251ade2956dfa460938b/third_party/blink/web_tests/http/tests/inspector-protocol/main-target-commands-expected.txt


### ad...@google.com (2021-01-07)

[Empty comment from Monorail migration]

### ja...@google.com (2021-01-19)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2021-09-13)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1116444?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>DevTools, Platform>Extensions]
[Monorail mergedwith: crbug.com/chromium/1116450]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053088)*
