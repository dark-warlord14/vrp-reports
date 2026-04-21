# Security: UAF in DiscardsGraphDumpImpl

| Field | Value |
|-------|-------|
| **Issue ID** | [40059569](https://issues.chromium.org/issues/40059569) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>PerformanceManager |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | wg...@gmail.com |
| **Assignee** | jo...@google.com |
| **Created** | 2022-05-05 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

DiscardsGraphDumpImpl::StartFrameFaviconRequest() will post a task to UIThreadTaskRunner, and then call FaviconRequestHelper::RequestFavicon()[1], using raw pointer returned from EnsureFaviconRequestHelper()[2]. DiscardsGraphDumpImpl owns FaviconRequestHelper instance[3]. However, before RequestFavicon() called, DiscardsGraphDumpImpl could already be deleted, which cause FaviconRequestHelper be deleted, that will cause UAF in browser process. The same bug exists in DiscardsGraphDumpImpl::StartPageFaviconRequest() as well[4].

[1]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/discards/graph_dump_impl.cc;l=439;drc=07c2037cd88e792e7d3d7ab03d98100d98d19b1d>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/discards/graph_dump_impl.cc;drc=07c2037cd88e792e7d3d7ab03d98100d98d19b1d;l=411>  

[3]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/discards/graph_dump_impl.h;drc=07c2037cd88e792e7d3d7ab03d98100d98d19b1d;l=247>  

[4]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/discards/graph_dump_impl.cc;l=429;drc=07c2037cd88e792e7d3d7ab03d98100d98d19b1d>

**VERSION**  

Chrome Version: stable  

Operating System: test in Linux

**REPRODUCTION CASE**

1. Start HTTP server  
   
   $ python3 -m http.server 8000
2. Start Chrome, open chrome://discards and POC page, close chrome://discards during loading POC page.  
   
   For easier reproduce, you can apply the patch.diff first, which only makes RequestFavicon() executes slower.

For build with DCHECK, there will be a DCHECK crash in lock\_impl.h. For ASAN build without DCHECK, there will be a heap-use-after-free crash.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see attached file

## Attachments

- [patch.diff](attachments/patch.diff) (text/plain, 1.9 KB)
- [dcheck.txt](attachments/dcheck.txt) (text/plain, 7.4 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 16.0 KB)
- [POC.html](attachments/POC.html) (text/plain, 156 B)
- [rep.mp4](attachments/rep.mp4) (video/mp4, 4.9 MB)

## Timeline

### [Deleted User] (2022-05-05)

[Empty comment from Monorail migration]

### wg...@gmail.com (2022-05-05)

[Empty comment from Monorail migration]

### me...@google.com (2022-05-06)

Thanks for the report. Assigning high severity since this is a UAF in the browser process, but on a non-web accessible webui page.

joenotcharles: Could you PTAL?

[Monorail components: Internals>PerformanceManager]

### [Deleted User] (2022-05-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-06)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-05-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b883adeb89b526ca1a668596f9ca0f22c5fc010f

commit b883adeb89b526ca1a668596f9ca0f22c5fc010f
Author: Joe Mason <joenotcharles@google.com>
Date: Fri May 06 20:41:21 2022

Use SequenceBound for chrome://discards favicon requests

Favicon requests must be performed on the UI sequence. This wraps
DiscardsGraphDumpImpl::FaviconRequestHelper in a SequenceBound object
to automatically send cross-sequence requests, instead of managing
tasks and lifetimes manually.

Also uses base::BindPostTask to send the reply back to the originating
sequence to reduce boilerplate.

R=meacer

Bug: 1322744
Change-Id: I064cfb35386d3ae8ae47490b0506f092d00052ff
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3632524
Reviewed-by: Mustafa Emre Acer <meacer@chromium.org>
Commit-Queue: Joe Mason <joenotcharles@google.com>
Auto-Submit: Joe Mason <joenotcharles@google.com>
Commit-Queue: Mustafa Emre Acer <meacer@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1000546}

[modify] https://crrev.com/b883adeb89b526ca1a668596f9ca0f22c5fc010f/chrome/browser/ui/webui/discards/graph_dump_impl.h
[modify] https://crrev.com/b883adeb89b526ca1a668596f9ca0f22c5fc010f/chrome/browser/ui/webui/discards/graph_dump_impl.cc


### jo...@google.com (2022-05-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-07)

Requesting merge to extended stable M100 because latest trunk commit (1000546) appears to be after extended stable branch point (972766).

Requesting merge to stable M101 because latest trunk commit (1000546) appears to be after stable branch point (982481).

Requesting merge to beta M102 because latest trunk commit (1000546) appears to be after beta branch point (992738).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-07)

Merge review required: M102 is already shipping to beta.

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

### [Deleted User] (2022-05-07)

Merge review required: M101 is already shipping to stable.

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
Owners: benmason (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-07)

Merge review required: M100 is already shipping to stable.

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

### jo...@google.com (2022-05-07)

1. Why does your merge fit within the merge criteria for these milestones?

Fixes a High severity security issue.

2. What changes specifically would you like to merge? Please link to Gerrit.

https://chromium-review.googlesource.com/q/3632524

3. Have the changes been released and tested on canary?

Yes, in 103.0.5048.0

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No, bugfix to existing feature.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

NA

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

No

### sr...@google.com (2022-05-09)

Merge approved for M102 branch: pls refer to go/chrome-branches for more info

### gi...@appspot.gserviceaccount.com (2022-05-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/326bff8dab3c221e8b1aaf3856877e393ec6b995

commit 326bff8dab3c221e8b1aaf3856877e393ec6b995
Author: Joe Mason <joenotcharles@google.com>
Date: Mon May 09 19:38:32 2022

Use SequenceBound for chrome://discards favicon requests

Favicon requests must be performed on the UI sequence. This wraps
DiscardsGraphDumpImpl::FaviconRequestHelper in a SequenceBound object
to automatically send cross-sequence requests, instead of managing
tasks and lifetimes manually.

Also uses base::BindPostTask to send the reply back to the originating
sequence to reduce boilerplate.

R=​meacer

(cherry picked from commit b883adeb89b526ca1a668596f9ca0f22c5fc010f)

Bug: 1322744
Change-Id: I064cfb35386d3ae8ae47490b0506f092d00052ff
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3632524
Reviewed-by: Mustafa Emre Acer <meacer@chromium.org>
Commit-Queue: Joe Mason <joenotcharles@google.com>
Auto-Submit: Joe Mason <joenotcharles@google.com>
Commit-Queue: Mustafa Emre Acer <meacer@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1000546}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3635679
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5005@{#585}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/326bff8dab3c221e8b1aaf3856877e393ec6b995/chrome/browser/ui/webui/discards/graph_dump_impl.h
[modify] https://crrev.com/326bff8dab3c221e8b1aaf3856877e393ec6b995/chrome/browser/ui/webui/discards/graph_dump_impl.cc


### [Deleted User] (2022-05-09)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jo...@google.com (2022-05-09)

1. Was this issue a regression for the milestone it was found in?

No, it was a pre-existing security issue.

2. Is this issue related to a change or feature merged after the latest LTS Milestone?

No.

### vo...@google.com (2022-05-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-05-14)

merge-na M101/M100- date/time of fix landing just missed M101/M100 cut for last planned M101 Stable/M100 Extended releases, this fix has been merged to M102 and will be included in M102 stable release 

### am...@google.com (2022-05-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-05-16)

Hello and thank you for this report. Due to this issue not being web accessible and the substantial amount of user interaction required to trigger this issue, the exploitation potential is very low. The VRP Panel has decided to award you $1,000 as thank you for your efforts and reporting this issue to us. A member of our finance team will be in touch soon to arrange payment. 
In the meantime, please let us know the name/tag/handle/other identifier you would like us to use in acknowledging you for this issue. 


### wg...@gmail.com (2022-05-17)

Thanks! Reporter credit: Guannan Wang (@Keenan7310) of Tencent Security Xuanwu Lab

### vo...@google.com (2022-05-17)

1. Just one CL https://crrev.com/c/3651920
2. Low - trivial conflicts
3. Yes, M102
4. Yes

### vo...@google.com (2022-05-17)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-17)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gm...@google.com (2022-05-17)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-05-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/312fbf4ee3c7a479644076d80ea3ecb73f1c102b

commit 312fbf4ee3c7a479644076d80ea3ecb73f1c102b
Author: Zakhar Voit <voit@google.com>
Date: Wed May 18 10:17:32 2022

[M96-LTS] Use SequenceBound for chrome://discards favicon requests

Favicon requests must be performed on the UI sequence. This wraps
DiscardsGraphDumpImpl::FaviconRequestHelper in a SequenceBound object
to automatically send cross-sequence requests, instead of managing
tasks and lifetimes manually.

Also uses base::BindPostTask to send the reply back to the originating
sequence to reduce boilerplate.

(cherry picked from commit b883adeb89b526ca1a668596f9ca0f22c5fc010f)

Bug: 1322744
Change-Id: I064cfb35386d3ae8ae47490b0506f092d00052ff
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3632524
Commit-Queue: Joe Mason <joenotcharles@google.com>
Auto-Submit: Joe Mason <joenotcharles@google.com>
Commit-Queue: Mustafa Emre Acer <meacer@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1000546}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3651920
Reviewed-by: Jana Grill <janagrill@google.com>
Commit-Queue: Zakhar Voit <voit@google.com>
Owners-Override: Jana Grill <janagrill@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1633}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/312fbf4ee3c7a479644076d80ea3ecb73f1c102b/chrome/browser/ui/webui/discards/graph_dump_impl.h
[modify] https://crrev.com/312fbf4ee3c7a479644076d80ea3ecb73f1c102b/chrome/browser/ui/webui/discards/graph_dump_impl.cc


### vo...@google.com (2022-05-18)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-08-18)

Hi Guannan Wang, we consider attachments/POCs included with reports to be an integral part of the report (https://g.co/chrome/vrp), so I've undeleted them. Thank you!

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1322744?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059569)*
