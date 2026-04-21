# Security: HeapOverflow in ScanningHandler

| Field | Value |
|-------|-------|
| **Issue ID** | [40059001](https://issues.chromium.org/issues/40059001) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>WebUI |
| **Platforms** | ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | ga...@chromium.org |
| **Created** | 2022-03-07 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

When making a search in |string\_id\_map\_|[1], there is no check whether the query result is end(). The out of bounds will occur when using |string\_id\_map\_.end()|.

[1]. <https://source.chromium.org/chromium/chromium/src/+/main:ash/webui/scanning/scanning_handler.cc;l=197;drc=354945de1fb564ef04c07cf8bfedf434d2d81747>

Fix suggestion:

diff --git a/ash/webui/scanning/scanning\_handler.cc b/ash/webui/scanning/scanning\_handler.cc  

index 52aafdd8b820b..e71f8c18259ae 100644  

--- a/ash/webui/scanning/scanning\_handler.cc  

+++ b/ash/webui/scanning/scanning\_handler.cc  

@@ -193,6 +193,9 @@ void ScanningHandler::HandleGetPluralString(const base::ListValue\* args) {  

const std::string name = args->GetListDeprecated()[1].GetString();  

const int count = args->GetListDeprecated()[2].GetInt();

- if (string\_id\_map\_.find(name) == string\_id\_map\_.end())
- return;
- const std::u16string localized\_string = l10n\_util::GetPluralStringFUTF16(  
  
  string\_id\_map\_.find(name)->second, count);  
  
  ResolveJavascriptCallback(base::Value(callback),

**VERSION**  

Chrome Version: stable  

Operating System: ChromeOS

**REPRODUCTION CASE**

browsing `chrome://scanning` and open devtools

execute `chrome.send("getPluralString",["","",0]);` in console.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Vulnerability Research Institute

## Attachments

- [asan](attachments/asan) (text/plain, 13.5 KB)

## Timeline

### [Deleted User] (2022-03-07)

[Empty comment from Monorail migration]

### dc...@chromium.org (2022-03-07)

Similar to https://crbug.com/chromium/1303614, this would benefit from a ReceivedBadMessage() method for non-mojo WebUI handlers. ReceivedBadMessage() would be more appropriate here rather than silently ignoring with early return.

Putting this under WebUI because the OS>Systems>Scanning component does not exist.

[Monorail components: UI>Browser>WebUI]

### [Deleted User] (2022-03-07)

[Empty comment from Monorail migration]

### ga...@chromium.org (2022-03-08)

[Empty comment from Monorail migration]

### ze...@chromium.org (2022-03-08)

[Comment Deleted]

### [Deleted User] (2022-03-08)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-03-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a1a288da0646237bc161c0145cb35018767def38

commit a1a288da0646237bc161c0145cb35018767def38
Author: Gavin Williams <gavinwill@chromium.org>
Date: Wed Mar 09 23:18:43 2022

Scanning: PluralHandler fix

Fixed: 1303613
Change-Id: Ib8f84687519e8741576f989c02ab3e5c5f712891
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3510769
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Gavin Williams <gavinwill@chromium.org>
Cr-Commit-Position: refs/heads/main@{#979477}

[modify] https://crrev.com/a1a288da0646237bc161c0145cb35018767def38/ash/webui/scanning/scanning_handler.cc
[modify] https://crrev.com/a1a288da0646237bc161c0145cb35018767def38/ash/webui/scanning/scanning_handler_unittest.cc


### [Deleted User] (2022-03-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-10)

Requesting merge to beta M100 because latest trunk commit (979477) appears to be after beta branch point (972766).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-10)

Merge review required: M100 is already shipping to beta.

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

### ga...@chromium.org (2022-03-14)

kalin@ please review this change for Beta merge https://crrev.com/c/3510769

### dg...@google.com (2022-03-15)

[Empty comment from Monorail migration]

### dg...@google.com (2022-03-21)

[Empty comment from Monorail migration]

### ka...@google.com (2022-03-21)

Was the change reviewed and approved by the Eng Prod Representative?
Yes,  LGTM.

### ka...@google.com (2022-03-21)

[Empty comment from Monorail migration]

### ga...@chromium.org (2022-03-21)

1. Why does your merge fit within the merge criteria for these milestones? Yes
2. What changes specifically would you like to merge? https://crrev.com/c/3510769
3. Have the changes been released and tested on canary? Yes
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels? No
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? Yes
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? No

### dg...@google.com (2022-03-22)

Merge approved for M100

### gi...@appspot.gserviceaccount.com (2022-03-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c630c62d4bfd4a07078a51226a1149efe43795d6

commit c630c62d4bfd4a07078a51226a1149efe43795d6
Author: Gavin Williams <gavinwill@chromium.org>
Date: Tue Mar 22 21:30:25 2022

[M100] Scanning: PluralHandler fix

(cherry picked from commit a1a288da0646237bc161c0145cb35018767def38)

Fixed: 1303613
Change-Id: Ib8f84687519e8741576f989c02ab3e5c5f712891
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3510769
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Gavin Williams <gavinwill@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#979477}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3543322
Auto-Submit: Gavin Williams <gavinwill@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4896@{#795}
Cr-Branched-From: 1f63ff4bc27570761b35ffbc7f938f6586f7bee8-refs/heads/main@{#972766}

[modify] https://crrev.com/c630c62d4bfd4a07078a51226a1149efe43795d6/ash/webui/scanning/scanning_handler.cc
[modify] https://crrev.com/c630c62d4bfd4a07078a51226a1149efe43795d6/ash/webui/scanning/scanning_handler_unittest.cc


### [Deleted User] (2022-03-22)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ga...@chromium.org (2022-03-22)

1. Was this issue a regression for the milestone it was found in? No
2. Is this issue related to a change or feature merged after the latest LTS Milestone? No

### rz...@google.com (2022-03-23)

[Empty comment from Monorail migration]

### rz...@google.com (2022-03-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-23)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-03-23)

1. Just https://crrev.com/c/3545246
2. Low, now conflicts
3. 100
4. Yes

### gm...@google.com (2022-03-24)

LTS Merge Approval delayed until latest M100 completes test and gets pushed.

### am...@chromium.org (2022-03-28)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-29)

[Empty comment from Monorail migration]

### gm...@google.com (2022-03-29)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-03-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c87440239c897d7ec86b3e5d28c498f590df7032

commit c87440239c897d7ec86b3e5d28c498f590df7032
Author: Gavin Williams <gavinwill@chromium.org>
Date: Thu Mar 31 17:11:01 2022

[M96-LTS] Scanning: PluralHandler fix

(cherry picked from commit a1a288da0646237bc161c0145cb35018767def38)

Fixed: 1303613
Change-Id: Ib8f84687519e8741576f989c02ab3e5c5f712891
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3510769
Commit-Queue: Gavin Williams <gavinwill@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#979477}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3545246
Reviewed-by: Michael Ershov <miersh@google.com>
Owners-Override: Michael Ershov <miersh@google.com>
Commit-Queue: Michael Ershov <miersh@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1564}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/c87440239c897d7ec86b3e5d28c498f590df7032/ash/webui/scanning/scanning_handler.cc
[modify] https://crrev.com/c87440239c897d7ec86b3e5d28c498f590df7032/ash/webui/scanning/scanning_handler_unittest.cc


### vo...@google.com (2022-04-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-04-15)

Hello leecraso and thank you for this report. As this issue requires user interaction and appears to result in a read, the VRP Panel has decided to award you $3,000 for this report. If you can demonstrate more impactful memory corruption resulting from this issue, we would be happy to reassess. Thanks again for your efforts and reporting this issue to us! 

### am...@google.com (2022-04-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-22)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1303613?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059001)*
