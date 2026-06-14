# Security: chrome.runtime.setUninstallURL does not validate its URL parameter

| Field | Value |
|-------|-------|
| **Issue ID** | [40082658](https://issues.chromium.org/issues/40082658) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Platform>Apps, Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | ro...@robwu.nl |
| **Created** | 2015-08-10 |
| **Bounty** | $3,000.00 |

## Description

chrome.runtime.setUninstallURL only checks whether the given parameter is a syntactically valid URL, but it does not enforce the blacklist of disallowed URLs.
This allows extensions and apps (without requiring any install permissions) to open any URL, including special chrome://-URLs.

In the worst case, this bug could be used to exploit a memory bug in the browser process (e.g. UAF in a browser thread upon shutdown).

I've attached a proof of concept. Upon start-up, it will set the uninstall URL and uninstall itself. That will immediately close the browser.

## Attachments

- [background.js](attachments/background.js) (text/javascript, 84 B)
- [manifest.json](attachments/manifest.json) (application/json, 145 B)

## Timeline

### ro...@robwu.nl (2015-08-10)

After uninstalling an extension, the user doesn't expect privileged actions (opening chrome:-URLs) any more. So restricting the uninstall URL to http(s) seems the best solution here.

### [Deleted User] (2015-08-10)

I agree that we should limit this to http[s]. I don't see any problem with chrome: or chrome-extension: or whatever but nevertheless I don't see any use case for this and we may as well limit this.

### ro...@robwu.nl (2015-08-10)

The patch is up for review at https://codereview.chromium.org/1282263002/, by the way.

### bu...@chromium.org (2015-08-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/28fc5b095a1d19eb104a76a08d55292831dce9fa

commit 28fc5b095a1d19eb104a76a08d55292831dce9fa
Author: rob <rob@robwu.nl>
Date: Tue Aug 11 00:27:36 2015

Restrict chrome.runtime.setUninstallURL to http(s)

Disallow URLs other than http(s) in chrome.runtime.setUninstallURL.
And allow empty URLs to be set to clear the uninstallation URL.
Added an optional callback, to know when setting the URL finished (or
failed).

BUG=518827
TEST=browser_tests --gtest_filter=ExtensionApiTest.ChromeRuntimeUninstallURL
R=kalman@chromium.org

Review URL: https://codereview.chromium.org/1282263002

Cr-Commit-Position: refs/heads/master@{#342752}

[modify] http://crrev.com/28fc5b095a1d19eb104a76a08d55292831dce9fa/chrome/test/data/extensions/api_test/runtime/uninstall_url/test.js
[modify] http://crrev.com/28fc5b095a1d19eb104a76a08d55292831dce9fa/extensions/browser/api/runtime/runtime_api.cc
[modify] http://crrev.com/28fc5b095a1d19eb104a76a08d55292831dce9fa/extensions/common/api/runtime.json


### ro...@robwu.nl (2015-08-11)

Merging the patch is low-risk, so I'd like to push the above patch to 45 (and 44, if deemed acceptable). The impact for not merging is that malicious extensions could abuse the method to exploit 0-days related to shutdown of Chrome (e.g. https://crbug.com/chromium/518749). This bug has been in Chrome since version 41.

To verify that the bug is fixed:
1. Download manifest.json and background.js from the initial report.
2. Visit chrome://extensions
3. Click on the "Load unpacked extension" button at the left.
4. Select the folder containing the files from step 1.
5. Verify that the browser does not quit after confirming step 4.

Security team, could you apply the appropriate security labels?

### pe...@google.com (2015-08-11)

Approved for M45 (branch: 2454)

### bu...@chromium.org (2015-08-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d6a6acd6f7155136dc1263a671012eded73955d9

commit d6a6acd6f7155136dc1263a671012eded73955d9
Author: Rob Wu <rob@robwu.nl>
Date: Wed Aug 12 13:56:55 2015

Restrict chrome.runtime.setUninstallURL to http(s)

Disallow URLs other than http(s) in chrome.runtime.setUninstallURL.
And allow empty URLs to be set to clear the uninstallation URL.
Added an optional callback, to know when setting the URL finished (or
failed).

BUG=518827
TEST=browser_tests --gtest_filter=ExtensionApiTest.ChromeRuntimeUninstallURL
R=kalman@chromium.org

Review URL: https://codereview.chromium.org/1282263002

Cr-Commit-Position: refs/heads/master@{#342752}
(cherry picked from commit 28fc5b095a1d19eb104a76a08d55292831dce9fa)

Review URL: https://codereview.chromium.org/1283193003 .

Cr-Commit-Position: refs/branch-heads/2454@{#294}
Cr-Branched-From: 12bfc3360892ec53cd00fc239a47e5298beb063b-refs/heads/master@{#338390}

[modify] http://crrev.com/d6a6acd6f7155136dc1263a671012eded73955d9/chrome/test/data/extensions/api_test/runtime/uninstall_url/test.js
[modify] http://crrev.com/d6a6acd6f7155136dc1263a671012eded73955d9/extensions/browser/api/runtime/runtime_api.cc
[modify] http://crrev.com/d6a6acd6f7155136dc1263a671012eded73955d9/extensions/common/api/runtime.json


### bu...@chromium.org (2015-08-12)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/d6a6acd6f7155136dc1263a671012eded73955d9

commit d6a6acd6f7155136dc1263a671012eded73955d9
Author: Rob Wu <rob@robwu.nl>
Date: Wed Aug 12 13:56:55 2015


### aa...@google.com (2015-08-22)

No M-44 merge required. Will go in M-45.

### ti...@google.com (2015-08-31)

[Empty comment from Monorail migration]

### ti...@google.com (2015-08-31)

[Empty comment from Monorail migration]

### ti...@google.com (2015-08-31)

Congrats Rob - $3,000 for this bug report.

Panel notes: $1,000 for the underlying issue + $2,000 for the quality report. patch and POC.

We'll credit you as "Rob Wu" as usual and start payment this week. You can expect the funds in your account in 2-3 weeks from today.

### ti...@google.com (2015-09-04)

[Empty comment from Monorail migration]

### ti...@google.com (2015-09-10)

Processing via our e-payment system takes ~7 days, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2015-09-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-11-18)

Bulk update: removing view restriction from closed bugs.

### pa...@chromium.org (2016-01-19)

[Empty comment from Monorail migration]

### pa...@chromium.org (2016-01-19)

[Empty comment from Monorail migration]

### as...@chromium.org (2016-02-16)

[Empty comment from Monorail migration]

### pa...@chromium.org (2016-02-29)

[Empty comment from Monorail migration]

### pa...@chromium.org (2016-05-13)

bulk verified

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/518827?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>Apps, Platform>Extensions]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082658)*
