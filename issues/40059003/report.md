# Security: HeapOverflow in CertificatesHandler

| Field | Value |
|-------|-------|
| **Issue ID** | [40059003](https://issues.chromium.org/issues/40059003) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>WebUI |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | dp...@chromium.org |
| **Created** | 2022-03-07 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

When doing operation [] for |selected\_cert\_list\_|[1], there is no check whether the size is equal to 1. The out of bounds will occur when using |selected\_cert\_list\_[0]|.

[1]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/certificates_handler.cc;l=538;drc=ca4b47d1034408a70ad7a7b7ad1a8355ec1d4993>

Fix suggestion:

diff --git a/chrome/browser/ui/webui/certificates\_handler.cc b/chrome/browser/ui/webui/certificates\_handler.cc  

index 17dd716d462cd..24ce83e93090b 100644  

--- a/chrome/browser/ui/webui/certificates\_handler.cc  

+++ b/chrome/browser/ui/webui/certificates\_handler.cc  

@@ -535,6 +535,8 @@ void CertificatesHandler::HandleExportPersonalPasswordSelected(  

// this would need to either change this to use UnlockSlotsIfNecessary or  

// change UnlockCertSlotIfNecessary to take a CertificateList.  

DCHECK\_EQ(selected\_cert\_list\_.size(), 1U);

- if (selected\_cert\_list\_.size() != 1)
- return;

// TODO(mattm): do something smarter about non-extractable keys  

chrome::UnlockCertSlotIfNecessary(

**VERSION**  

Chrome Version: stable  

Operating System: ChromeOS

**REPRODUCTION CASE**

browsing `chrome://certificate-manager` and open devtools

execute `chrome.send("exportPersonalCertificatePasswordSelected",["1","0"]);` in console.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Vulnerability Research Institute

## Attachments

- [asan](attachments/asan) (text/plain, 13.6 KB)

## Timeline

### [Deleted User] (2022-03-07)

[Empty comment from Monorail migration]

### dc...@chromium.org (2022-03-07)

Though I would suggest we should probably be using content::ReceivedBadMessage() (since this isn't Mojo yet).

[Monorail components: UI>Browser>WebUI]

### [Deleted User] (2022-03-07)

[Empty comment from Monorail migration]

### dc...@chromium.org (2022-03-07)

This UI appears to be CrOS specific so tagging as such.

(LaCrOS may also make this even harder to reach in the future too, even in the presence of other bugs, due to ash-chrome vs lacros-chrome)

### [Deleted User] (2022-03-08)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### le...@gmail.com (2022-03-09)

This issue also applies to other platform (test in linux and win), execute code in `chrome://settings` instead of `chrome://certificate-manager`

### dp...@chromium.org (2022-03-09)

Candidate fix at [1], converting the DCHECK at [2] to a CHECK. AFAIU it is OK to crash when unexpected/bad messages are received from the frontend. We already do this in plenty of C++ handlers where we CHECK() for the correct number of arguments for example.

[1] https://chromium-review.googlesource.com/c/chromium/src/+/3514540
[2] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/certificates_handler.cc;l=534;drc=ca4b47d1034408a70ad7a7b7ad1a8355ec1d4993

### gi...@appspot.gserviceaccount.com (2022-03-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e782490c1b0b5d500b9aca3bd21c15fd486d1c28

commit e782490c1b0b5d500b9aca3bd21c15fd486d1c28
Author: dpapad <dpapad@chromium.org>
Date: Thu Mar 10 00:31:15 2022

Convert DCHECK to CHECK in CertificatesHandler.

This prevents a heap overflow in case of bad arguments passed from the
frontend.

Bug: 1303615
Change-Id: If02534117cb4a7e442ac8a9d91f005d41fda8959
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3514540
Auto-Submit: Demetrios Papadopoulos <dpapad@chromium.org>
Reviewed-by: John Lee <johntlee@chromium.org>
Commit-Queue: John Lee <johntlee@chromium.org>
Cr-Commit-Position: refs/heads/main@{#979531}

[modify] https://crrev.com/e782490c1b0b5d500b9aca3bd21c15fd486d1c28/chrome/browser/ui/webui/certificates_handler.cc


### dp...@chromium.org (2022-03-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-10)

Requesting merge to beta M100 because latest trunk commit (979531) appears to be after beta branch point (972766).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-11)

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

### sr...@google.com (2022-03-14)

Merge approved for M100 branch:please refer to go/chrome-branches for info.

Please merge your changes to M100 branch before 12pm PST tomorrow ( tuesday March 15) so they can be included in this weeks beta release.

### gi...@appspot.gserviceaccount.com (2022-03-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7f3b9f790969d8a566cf30270760e7ba5d5414fc

commit 7f3b9f790969d8a566cf30270760e7ba5d5414fc
Author: dpapad <dpapad@chromium.org>
Date: Mon Mar 14 19:52:55 2022

[M100 merge] Convert DCHECK to CHECK in CertificatesHandler.

This prevents a heap overflow in case of bad arguments passed from the
frontend.

(cherry picked from commit e782490c1b0b5d500b9aca3bd21c15fd486d1c28)

Bug: 1303615
Change-Id: If02534117cb4a7e442ac8a9d91f005d41fda8959
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3514540
Auto-Submit: Demetrios Papadopoulos <dpapad@chromium.org>
Reviewed-by: John Lee <johntlee@chromium.org>
Commit-Queue: John Lee <johntlee@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#979531}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3522125
Commit-Queue: Demetrios Papadopoulos <dpapad@chromium.org>
Cr-Commit-Position: refs/branch-heads/4896@{#527}
Cr-Branched-From: 1f63ff4bc27570761b35ffbc7f938f6586f7bee8-refs/heads/main@{#972766}

[modify] https://crrev.com/7f3b9f790969d8a566cf30270760e7ba5d5414fc/chrome/browser/ui/webui/certificates_handler.cc


### [Deleted User] (2022-03-14)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dp...@chromium.org (2022-03-15)

> 1. Was this issue a regression for the milestone it was found in?

No, AFAICT.

> 2. Is this issue related to a change or feature merged after the latest LTS Milestone?

No.

### vo...@google.com (2022-03-15)

[Empty comment from Monorail migration]

### rz...@google.com (2022-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-17)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-03-17)

1. Just https://crrev.com/c/3528393
2. Low, no conflicts
3. 100
4. Yes

### gm...@google.com (2022-03-17)

Delaying merge approval until it gets pushed on beta.

### gm...@google.com (2022-03-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-03-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/790bfdaeb734054c419628e70fd6408e593ffb9d

commit 790bfdaeb734054c419628e70fd6408e593ffb9d
Author: dpapad <dpapad@chromium.org>
Date: Mon Mar 28 15:58:25 2022

[M96-LTS] Convert DCHECK to CHECK in CertificatesHandler.

This prevents a heap overflow in case of bad arguments passed from the
frontend.

(cherry picked from commit e782490c1b0b5d500b9aca3bd21c15fd486d1c28)

Bug: 1303615
Change-Id: If02534117cb4a7e442ac8a9d91f005d41fda8959
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3514540
Auto-Submit: Demetrios Papadopoulos <dpapad@chromium.org>
Commit-Queue: John Lee <johntlee@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#979531}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3528393
Reviewed-by: Demetrios Papadopoulos <dpapad@chromium.org>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1558}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/790bfdaeb734054c419628e70fd6408e593ffb9d/chrome/browser/ui/webui/certificates_handler.cc


### rz...@google.com (2022-03-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-03-28)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-29)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-31)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-31)

Hello, Leecraso and Guang Gong. The VRP Panel has decided to award you $3,000 for this report. In assessing this issue for security impact and exploitability, the reward amount was impacted by this bug not being web accessible and the direct user interaction with DevTools required to trigger this issue. If you can demonstrate a web-accessible exploitation of this issue or a simple path to execution, we would be happy to reassess. Thanks for your efforts and reporting this issue to us! 

### am...@google.com (2022-04-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-22)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1303615?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059003)*
