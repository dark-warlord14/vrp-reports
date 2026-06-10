# chrome.debugger 'Page.navigate' can navigate iframes to file:// when not enabled.

| Field | Value |
|-------|-------|
| **Issue ID** | [40060173](https://issues.chromium.org/issues/40060173) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>DevTools>Privacy and Security |
| **Platforms** | Windows |
| **Reporter** | nd...@protonmail.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2022-07-06 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**  

chrome.debugger.attach({tabId: <TARGET>}, '1.3', console.log);  

chrome.debugger.sendCommand({tabId: <TARGET>}, 'Page.navigate', {frameId: <FRAME ID AS SEEN FROM EVENTS), url: 'file:///d:/demo.txt'}, console.log);  

chrome.pageCapture.saveAsMHTML({tabId: 800972627}, console.log);

**Problem Description:**  

Extensions with both the pageCapture and debugger can read local file contents.  

This is because its possible to use Page.navigate to navigate an iframe to file:// when "Allow access to file URLs" is disabled exposing the files contents to the pageCapture API.

**Additional Comments:**

\*\*Chrome version: \*\* 103.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Windows

## Attachments

- [background.js](attachments/background.js) (text/plain, 826 B)
- [iframe.html](attachments/iframe.html) (text/plain, 24 B)
- [manifest.json](attachments/manifest.json) (text/plain, 179 B)

## Timeline

### [Deleted User] (2022-07-06)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2022-07-06)

[Comment Deleted]

### da...@chromium.org (2022-07-06)

debugger is a powerful permission, but presumably it should not give local filesystem access?

https://developer.chrome.com/docs/extensions/reference/debugger/

Extension access to the filesystem would sound like a critical severity to me. However the debugger permission is powerful and I would like to hope is not granted to extensions often. So I am guessing at High sev for this.

I am not good at devtools so reproducing this locally is not obvious for me. I need a <TabID>, <TARGET> and <FRAME ID> to try this out and not sure how to get those. I'd like to determine what versions of Chrome this reproduces in.



[Monorail components: Platform>DevTools>Security]

### ya...@google.com (2022-07-06)

It seems to me that what we really want to prevent is to give the permission to extensions.

### ya...@google.com (2022-07-06)

I meant remove permission to extensions.

### [Deleted User] (2022-07-06)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### nd...@protonmail.com (2022-07-06)

I think I know what you mean, chrome.debugger seems to be an overly powerful API for extensions and something as simple as changing navigator.userAgent requires <all_urls>

### nd...@protonmail.com (2022-07-07)

PoC

### nd...@protonmail.com (2022-07-07)

With chrome.tabs.captureVisibleTab its possible to do this without the pageCapture permission.
Im not sure if theirs a usage for allowing embeds of file:/// on other websites anyway does not allow chrome://

### gi...@appspot.gserviceaccount.com (2022-07-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/925a1926434ee8e71b7adac47989df27e64b69d6

commit 925a1926434ee8e71b7adac47989df27e64b69d6
Author: Danil Somsikov <dsv@chromium.org>
Date: Fri Jul 08 08:51:45 2022

Don't allow Page.navigate to file:// URLs for extensions w/o file system
access.

Bug: 1342104
Change-Id: I271258d6b43bec3f43890e9b7d6fdecd9c00e75e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3748645
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Auto-Submit: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1022060}

[modify] https://crrev.com/925a1926434ee8e71b7adac47989df27e64b69d6/content/browser/devtools/protocol/page_handler.cc
[modify] https://crrev.com/925a1926434ee8e71b7adac47989df27e64b69d6/content/public/test/test_devtools_protocol_client.cc
[modify] https://crrev.com/925a1926434ee8e71b7adac47989df27e64b69d6/content/browser/devtools/protocol/devtools_protocol_browsertest.cc
[modify] https://crrev.com/925a1926434ee8e71b7adac47989df27e64b69d6/content/browser/devtools/protocol/page_handler.h
[modify] https://crrev.com/925a1926434ee8e71b7adac47989df27e64b69d6/chrome/test/data/extensions/api_test/debugger_file_access/background.js
[modify] https://crrev.com/925a1926434ee8e71b7adac47989df27e64b69d6/content/public/test/test_devtools_protocol_client.h
[modify] https://crrev.com/925a1926434ee8e71b7adac47989df27e64b69d6/content/browser/devtools/render_frame_devtools_agent_host.cc


### ds...@chromium.org (2022-07-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-08)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ds...@chromium.org (2022-07-08)

[Empty comment from Monorail migration]

### ds...@chromium.org (2022-07-08)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2022-07-08)

[Comment Deleted]

### [Deleted User] (2022-07-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-08)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-08)

Requesting merge to extended stable M102 because latest trunk commit (1022060) appears to be after extended stable branch point (992738).

Requesting merge to stable M103 because latest trunk commit (1022060) appears to be after stable branch point (1002911).

Requesting merge to beta M104 because latest trunk commit (1022060) appears to be after beta branch point (1012729).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### nd...@protonmail.com (2022-07-08)

[Comment Deleted]

### [Deleted User] (2022-07-09)

Merge review required: M104 is already shipping to beta.

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
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-09)

Merge review required: M103 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-09)

Merge review required: M102 is already shipping to stable.

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
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-12)

M104 merge approved, please merge this fix to branch 5112 at your earliest convenience -- thank you!

### am...@google.com (2022-07-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### nd...@protonmail.com (2022-07-13)

May as well try :)

It seems other bugs like this got $5000 was the amount decided based of report quality?
https://bugs.chromium.org/p/chromium/issues/detail?id=1116444 File read $5000
https://bugs.chromium.org/p/chromium/issues/detail?id=1113565 File read $5000
https://bugs.chromium.org/p/chromium/issues/detail?id=1236325 URLs read $7000
Apart from https://bugs.chromium.org/p/chromium/issues/detail?id=893087 that got $500

### nd...@protonmail.com (2022-07-13)

Correction URLs one was also $5000 not sure where I got that from.

### am...@chromium.org (2022-07-13)

You got here before I could follow up after the automation. Hello, and thanks for your question! Yes, as per all of our reports the reward amount is decided primarily based on the intersection of impact+report quality, which is the outcome of this reward amount. 
Thanks for your efforts and reporting this issue to us! 


### nd...@protonmail.com (2022-07-13)

This report is not any worse then https://crbug.com/chromium/1116444 as its the same bug that was not fixed so providing more then the working PoC would waste peoples time.
"Thanks :)"

### nd...@protonmail.com (2022-07-14)

To clarify its https://bugs.chromium.org/p/chromium/issues/detail?id=1113565 that was not fixed since that used Page.navigate to go to file:// but instead of blocking the navigation it only kept the debugger detached.

Teaching developers how to use devtools was not an option at the time of the report and it got triaged to quick PoC was provided next day.

### am...@chromium.org (2022-07-14)

Thanks for that information. It is helpful to understand that we don't generally compare similar reports to determine reward amounts. Reports are reviewed individually on their own merits and based on the bug class and impact and report quality as laid out in our rules and policies [1]. I'm happy to have us review this for a potential reassessment. 
For comparison sake, the POC and a very thorough analysis was provided in the original reports of the other reports you linked, which assisted with repro, RCA, and fix for those developers, which is why those reports received those reward amounts at those times. 
Again, happy to re-review this at a future VRP Panel session, but that's the insight I can offer at this time. 

### am...@chromium.org (2022-07-14)

Hi Danil, thanks for the quick fix on this one. Unless there are any issues or concerns you have with backmerging this fix, please merge the fix to this to all active release branches. Previously approved for merge to M104 (branch 5112) in https://crbug.com/chromium/1342104#c24. 

Merges also approved for M103/stable (branch 5060) and M102/Extended (branch 5005), please merge by 10am PST tomorrow so this fix can be included in the stable and ES cut for the next security respin tomorrow. Thank you! 

### am...@google.com (2022-07-15)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-07-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3d34ceb1716e0c2aabb7fcdfcf10a1094b230c5c

commit 3d34ceb1716e0c2aabb7fcdfcf10a1094b230c5c
Author: Danil Somsikov <dsv@chromium.org>
Date: Fri Jul 15 11:52:11 2022

Cherry pick crrev.com/c/3748645 to M103

Don't allow Page.navigate to file:// URLs for extensions w/o file system access.

Bug: 1342104
Change-Id: I2656fe3d671cde281851ff2d337a8003b3b4c034
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3762619
Reviewed-by: Yang Guo <yangguo@chromium.org>
Cr-Commit-Position: refs/branch-heads/5060@{#1233}
Cr-Branched-From: b83393d0f4038aeaf67f970a024d8101df7348d1-refs/heads/main@{#1002911}

[modify] https://crrev.com/3d34ceb1716e0c2aabb7fcdfcf10a1094b230c5c/content/browser/devtools/protocol/page_handler.cc
[modify] https://crrev.com/3d34ceb1716e0c2aabb7fcdfcf10a1094b230c5c/content/public/test/test_devtools_protocol_client.cc
[modify] https://crrev.com/3d34ceb1716e0c2aabb7fcdfcf10a1094b230c5c/content/browser/devtools/protocol/devtools_protocol_browsertest.cc
[modify] https://crrev.com/3d34ceb1716e0c2aabb7fcdfcf10a1094b230c5c/content/browser/devtools/protocol/page_handler.h
[modify] https://crrev.com/3d34ceb1716e0c2aabb7fcdfcf10a1094b230c5c/chrome/test/data/extensions/api_test/debugger_file_access/background.js
[modify] https://crrev.com/3d34ceb1716e0c2aabb7fcdfcf10a1094b230c5c/content/public/test/test_devtools_protocol_client.h
[modify] https://crrev.com/3d34ceb1716e0c2aabb7fcdfcf10a1094b230c5c/content/browser/devtools/render_frame_devtools_agent_host.cc


### sr...@google.com (2022-07-15)

pls complete your merge to M102 branch asap .

### ds...@chromium.org (2022-07-18)

Sorry, there were some issues with merging to M102. M103 and M104 got the patch. Should I still try to merge to 102 or is it too late already?

### ds...@chromium.org (2022-07-18)

[Empty comment from Monorail migration]

### ds...@chromium.org (2022-07-18)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-07-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/46f18e778967900c595c8142deade138333c0a7c

commit 46f18e778967900c595c8142deade138333c0a7c
Author: Danil Somsikov <dsv@chromium.org>
Date: Mon Jul 18 15:54:30 2022

Cherry pick crrev.com/c/3748645 to M102

Don't allow Page.navigate to file:// URLs for extensions w/o file system access.

Bug: 1342104
Change-Id: I6865fc86edb20e0e599e0f71335d9c614c23a69c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3762633
Reviewed-by: Srinivas Sista <srinivassista@chromium.org>
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Cr-Commit-Position: refs/branch-heads/5005@{#1261}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/46f18e778967900c595c8142deade138333c0a7c/content/browser/devtools/protocol/page_handler.cc
[modify] https://crrev.com/46f18e778967900c595c8142deade138333c0a7c/content/browser/devtools/protocol/page_handler.h
[modify] https://crrev.com/46f18e778967900c595c8142deade138333c0a7c/chrome/test/data/extensions/api_test/debugger_file_access/background.js
[modify] https://crrev.com/46f18e778967900c595c8142deade138333c0a7c/content/browser/devtools/render_frame_devtools_agent_host.cc


### [Deleted User] (2022-10-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1342104?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060173)*
