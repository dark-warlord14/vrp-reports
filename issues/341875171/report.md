# Sandbox escape from extensions due to insufficent checks in chrome.devtools.inspectedWindow.reload and chrome://policy

| Field | Value |
|-------|-------|
| **Issue ID** | [341875171](https://issues.chromium.org/issues/341875171) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>DevTools |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ad...@gmail.com |
| **Assignee** | yd...@google.com |
| **Created** | 2024-05-21 |
| **Bounty** | $20,000.00 |

## Description

As requested, I am submitting this as a separate issue. The original bug report (with the full chain leading to a sandbox escape) is located at <https://issues.chromium.org/issues/338248595>

Note that this bug was already fixed in the original issue. I was just asked to submit this as a separate report for tracking purposes.

## VULNERABILITY DETAILS

A race condition in the devtools API server and chrome.devtools.inspectedWindow.reload, along with insufficient permissions checks, allows an extension with the devtools\_page permission to run arbitrary JS on any privileged page.

## EXPLANATION

The `chrome.devtools.inspectedWindow.reload` function has [no checks](https://source.chromium.org/chromium/chromium/src/+/main:third_party/devtools-frontend/src/front_end/models/extensions/ExtensionServer.ts;l=812-826) to see if the extension is actually allowed to execute scripts on the inspected page. The only thing preventing this from being used normally is having the devtools extension server [block access](https://source.chromium.org/chromium/chromium/src/+/main:third_party/devtools-frontend/src/front_end/models/extensions/ExtensionServer.ts;l=456-459) once the URL of the inspected page changes.

Unfortunately, since [only the URL is checked](https://source.chromium.org/chromium/chromium/src/+/main:third_party/devtools-frontend/src/front_end/models/extensions/ExtensionServer.ts;l=1367-1405;drc=6f3f85b321146cfc0f9eb81a74c7c2257821461e) rather than the page's origin, so there is a small window of time after a navigation occurs where the origin is set to the new page but the URL is unchanged. If `chrome.devtools.inspectedWindow.reload` is called during this period, then it will execute arbitrary JS on the page that is being navigated to.

This window of time can be fairly reliably hit by spamming `chrome.devtools.inspectedWindow.reload` calls, then using `chrome.tabs.update(chrome.devtools.inspectedWindow.tabId, {url: "chrome://settings"});` to perform the navigation. Now we can run arbitrary JS on any `chrome://` page, bypassing any permissions checks.

## BISECT

Injecting scripts on `inspectedWindow.reload` was added [13 years ago](https://chromium.googlesource.com/chromium/blink/+/183eb96ce9836c3f1ccfd7ec82fcd7eac740319c%5E%21/#F8), so its likely that this part of the bug works on nearly every version of Chrome.

## VERSION

Chrome Version: 125.0.6422.60 stable
Operating System: Debian 12

## REPRODUCTION CASE

1. Download the files attached to this report and place them in the same folder
2. Open Chromium and load the files as an extension
3. Open devtools on about:blank or any other unprivileged page

A video is attached which demonstrates this.

## CREDIT INFORMATION

Reporter credit: Allen Ding

## Attachments

- [chrome_devtools_bug.mp4](attachments/chrome_devtools_bug.mp4) (video/mp4, 591.2 KB)
- [worker.js](attachments/worker.js) (text/javascript, 149 B)
- [manifest.json](attachments/manifest.json) (application/json, 243 B)
- [devtools.html](attachments/devtools.html) (text/html, 73 B)
- [index.html](attachments/index.html) (text/html, 191 B)
- [devtools.js](attachments/devtools.js) (text/javascript, 1.4 KB)

## Timeline

### ps...@google.com (2024-05-21)

As requested in https://g-issues.chromium.org/issues/338248595 assigning bug for tracking purposes, the fix should have already landed but keeping status as assigned for assignee to validate 

### pe...@google.com (2024-05-21)

Setting milestone because of s0/s1 severity.

### pf...@chromium.org (2024-05-21)

This is fixed by <https://crrev.com/c/5542082>, <https://crrev.com/c/5546062>, and <https://crrev.com/c/5546065>. Requesting merge >= 124

### pe...@google.com (2024-05-21)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

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
Owners: govind (Android), govind (iOS), ceb (ChromeOS), srinivassista (Desktop)

### pe...@google.com (2024-05-21)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

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
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

### pe...@google.com (2024-05-21)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

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

### pf...@chromium.org (2024-05-23)

1. S1 Vulnerability
2. <https://crrev.com/c/5542082>, <https://crrev.com/c/5546062>, and <https://crrev.com/c/5546065>
3. 127.0.6486.0
4. no
5. Automation set milestone to 124 so I assume yes? See #1 for reproduction steps

### am...@chromium.org (2024-05-28)

This is a set of non-trivial changes for this part of a high severity issues. In balancing the impact from this segment of this issue with the overall changes, I'm approving merge to M126 Beta only. M126 is being cut for Stable RC next week so these fixes can be included there as well.
It seems a bit risky to backmerge these set of changes when we are 3/4 through M125 Stable and M124 Extended Stable lifecycles.
Please merges the changes in c#8 item 2 to branch 6478 at your earliest availability and please let me know if there are any issues with this plan.

### ap...@google.com (2024-05-29)

Project: chromium/src
Branch: refs/branch-heads/6478

commit bdb10c5dca22b339f1075564e3623675eedf9e82
Author: Philip Pfaffe <pfaffe@chromium.org>
Date:   Wed May 29 09:25:19 2024

    Add loaderId argument to Page.reload
    
    By passing the loaderId, clients can prevent accidentally reloading
    unintended targets when Page.reload is racing with a navigiation.
    
    (cherry picked from commit beb3a0dab4470df7fb927c13935777f6d5228ec3)
    
    Bug: 338248595, 341875171
    Change-Id: I68883658a2112bba2a4cb428b4c3c33314c5e894
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5542082
    Commit-Queue: Alex Rudenko <alexrudenko@chromium.org>
    Auto-Submit: Philip Pfaffe <pfaffe@chromium.org>
    Reviewed-by: Alex Rudenko <alexrudenko@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1302488}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5576938
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6478@{#802}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       content/browser/devtools/protocol/page_handler.cc
M       content/browser/devtools/protocol/page_handler.h
M       third_party/blink/public/devtools_protocol/browser_protocol.pdl
M       third_party/blink/renderer/core/inspector/inspector_page_agent.cc
M       third_party/blink/renderer/core/inspector/inspector_page_agent.h
M       third_party/blink/web_tests/inspector-protocol/page/reload-dataurl.js
A       third_party/blink/web_tests/inspector-protocol/page/reload-loaderId-expected.txt
A       third_party/blink/web_tests/inspector-protocol/page/reload-loaderId.js
M       third_party/blink/web_tests/inspector-protocol/page/reload-on-breakpoint.js

https://chromium-review.googlesource.com/5576938


### pe...@google.com (2024-05-29)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### ap...@google.com (2024-05-29)

Project: devtools/devtools-frontend
Branch: chromium/6478

commit 3c74763045f44bea6319164593b4d6a0ed34990a
Author: Philip Pfaffe <pfaffe@chromium.org>
Date:   Wed May 29 08:21:01 2024

    Ensure inspectedWindow.reload reloads the correct page
    
    This prevents unintended reloads when racing with navigations.
    
    Drive-by: Check extension allowlist when loading page resources.
    
    Bug: 338248595, 341875171
    Change-Id: Ibbac5bbd45b1db0d05e32fe8e384740933ee4639
    Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/5546062
    Reviewed-by: Danil Somsikov <dsv@chromium.org>
    Commit-Queue: Philip Pfaffe <pfaffe@chromium.org>
    (cherry picked from commit 33a09fb44a6f593270589acfac482d9b275b389c)
    Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/5580037
    Reviewed-by: Ergün Erdoğmuş <ergunsh@chromium.org>

M       front_end/core/sdk/ResourceTreeModel.test.ts
M       front_end/core/sdk/ResourceTreeModel.ts
M       front_end/models/extensions/ExtensionServer.test.ts
M       front_end/models/extensions/ExtensionServer.ts

https://chromium-review.googlesource.com/5580037


### pe...@google.com (2024-05-31)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



### vo...@google.com (2024-05-31)

1. <https://crrev.com/c/5542082>, <https://crrev.com/c/5546062>, <https://crrev.com/c/5546065> + likely some precursors to solve the merge conflicts
2. High - large amount of changes with conflicts
3. M126
4. No

### gm...@google.com (2024-06-05)

Rejecting the merge for LTS-120. We will get the fix in LTC/LTS 126.

### am...@chromium.org (2024-06-10)

Hi OP, this issue has been updated with the reward-topanel label, meaning it will be reviewed at a future VRP Panel session, once the primary report ([crbug.com/338248595](https://crbug.com/338248595)) has been closed as fixed and is ready for VRP assessment. Thanks for your patience in the meantime.

### am...@chromium.org (2024-07-17)

The Chrome VRP panel has decided to award [crbug.com/338248595](https://crbug.com/338248595), the parent bug for this issue, a VRP reward of $20,000, because the reward has already been communicated and updated on [issue 338248595](https://issues.chromium.org/issues/338248595), updating the reward tag on this issue as 0.
Congratulations Allen and nice work!

### pe...@google.com (2024-08-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/341875171)*
