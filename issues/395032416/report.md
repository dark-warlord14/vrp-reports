# heap-use-after-free in blink::LegacyDOMSnapshotAgent::VisitNode

| Field | Value |
|-------|-------|
| **Issue ID** | [395032416](https://issues.chromium.org/issues/395032416) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | as...@gmail.com |
| **Assignee** | pf...@google.com |
| **Created** | 2025-02-10 |
| **Bounty** | $3,000.00 |

## Description

VULNERABILITY DETAILS
UAF in blink::LegacyDOMSnapshotAgent::VisitNode

VERSION
Chrome Version: 134.0.6986.0（Developer Build）
Operating System: Ubuntu

REPRODUCTION CASE
1. put manifest.json/background.js into the extension_path
2. run the command:
 ./chrome --user-data-dir=./noexist --no-sandbox --load-extension="extension_path"

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab
Crash State: see asan.log file

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: Sakana.S

## Attachments

- background.js (text/javascript, 1.3 KB)
- manifest.json (application/json, 160 B)
- asan.log (text/plain, 36.1 KB)
- background.js (text/javascript, 1.4 KB)

## Timeline

### as...@gmail.com (2025-02-10)

I have found that "chrome.windows.remove" is not needed for this bug.

### ma...@chromium.org (2025-02-10)

repro'd on 132 and 135.
Setting S2 per "Memory corruption that requires a specific extension to be installed".
Assigning based on blame, please reassign if there is a better owner.
Assuming this is not platform specific.

### pe...@google.com (2025-02-11)

Setting milestone because of s2 severity.

### pe...@google.com (2025-02-11)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### pe...@google.com (2025-02-16)

This Chrome DevTools issue has `Found In` milestone information, but is still on the Unconfirmed hotlist. Assuming that this issue is therefore considered confirmed, please provide any additional information that is still missing and remove it from the Unconfirmed hotlist so that it can be further triaged by the product team.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pf...@google.com (2025-02-25)

I managed to reproduce and I think I have a fix, I'm fighting CQ to get it landed since the sequence of CDP commands triggers a DCHECK flakily (related to the UAF actually).

### ap...@google.com (2025-02-26)

Project: chromium/src  

Branch: main  

Author: Philip Pfaffe <[pfaffe@chromium.org](mailto:pfaffe@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6297444>

Fix crash in DOM snapshot agent

---


Expand for full commit details
```
Fix crash in DOM snapshot agent 
 
When taking as snapshot, the DOM snapshot agent holds a pointer to a 
hashmap on the stack. The hashmap is destroyed when the devtools session 
detaches, so if that happens while taking a snapshot we run into a 
crash. 
 
Fixed: 395032416 
Change-Id: I4b784cb3105f6a760ca5b1d3dcbe1ea254b3ad3a 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6297444 
Reviewed-by: Alex Rudenko <alexrudenko@chromium.org> 
Commit-Queue: Philip Pfaffe <pfaffe@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1425198}

```

---

Files:

- M `third_party/blink/renderer/core/inspector/inspector_dom_snapshot_agent.cc`
- M `third_party/blink/renderer/core/inspector/inspector_dom_snapshot_agent.h`
- M `third_party/blink/renderer/core/inspector/legacy_dom_snapshot_agent.cc`
- M `third_party/blink/renderer/core/inspector/legacy_dom_snapshot_agent.h`

---

Hash: 4fa8d897f83ab2ee66dc3505409a6e44936d7e4c  

Date:  Wed Feb 26 09:16:42 2025


---

### ch...@google.com (2025-02-27)

Merge review required: M134 has already been cut for stable release.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### pf...@google.com (2025-02-28)

1. S2 UAF
2. <https://chromium-review.googlesource.com/6297444>
3. Yes, released in 135.0.7039.0
4. No
5. N/A
6. N/A

### pg...@google.com (2025-02-28)

Hello, thanks for fixing this security issue and being proactive for the merges! In the future, please let the automation mark security bugs for back merges appropriately based on schedules and severities (:

we've missed approval cut for M134 and normally S2 bugs do not get merged to the stable branch. But the fix has been merged for more than two days now with no relevant errors as far as I can tell (there seems to be a skia gold test that hasnt been triaged, but appears to be irrelevant), looks straight forward, and snapshotting in an extension seems like a easy and benign task for extensions to do/be able to convince users to do. Please re-check for any stability issues, and merge to branch M134 before Monday March 3 10am PST MTV time, if possible, to get this fix into the next M134 release! If not, it can roll out in the following M134 release.

### ap...@google.com (2025-03-03)

Project: chromium/src  

Branch: refs/branch-heads/6998  

Author: Philip Pfaffe <[pfaffe@chromium.org](mailto:pfaffe@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6316728>

Fix crash in DOM snapshot agent

---


Expand for full commit details
```
Fix crash in DOM snapshot agent 
 
When taking as snapshot, the DOM snapshot agent holds a pointer to a 
hashmap on the stack. The hashmap is destroyed when the devtools session 
detaches, so if that happens while taking a snapshot we run into a 
crash. 
 
(cherry picked from commit 4fa8d897f83ab2ee66dc3505409a6e44936d7e4c) 
 
Fixed: 395032416 
Change-Id: I4b784cb3105f6a760ca5b1d3dcbe1ea254b3ad3a 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6297444 
Reviewed-by: Alex Rudenko <alexrudenko@chromium.org> 
Commit-Queue: Philip Pfaffe <pfaffe@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1425198} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6316728 
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
Cr-Commit-Position: refs/branch-heads/6998@{#1765} 
Cr-Branched-From: de9c6fafd8ae5c6ea0438764076ca7d04a0b165d-refs/heads/main@{#1415337}

```

---

Files:

- M `third_party/blink/renderer/core/inspector/inspector_dom_snapshot_agent.cc`
- M `third_party/blink/renderer/core/inspector/inspector_dom_snapshot_agent.h`
- M `third_party/blink/renderer/core/inspector/legacy_dom_snapshot_agent.cc`
- M `third_party/blink/renderer/core/inspector/legacy_dom_snapshot_agent.h`

---

Hash: bc09b6ac393563ab66f32388bd2468eb584b1c1a  

Date:  Mon Mar 03 05:47:51 2025


---

### pe...@google.com (2025-03-03)

LTS Milestone M132

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### sp...@google.com (2025-03-06)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
report of mildly mitigated memory corruption in a sandboxed process / renderer, mitigated by precondition to install malicious extension with debugger permissions 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-03-06)

Congratulations Sakana.S! Thank you for your efforts and reporting this issue to us.

### pe...@google.com (2025-03-06)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2025-03-06)

1. https://chromium-review.googlesource.com/c/chromium/src/+/6320854
2. Low - There was no conflict.
3. 134
4. Yes. According to comment #3, this issue happened on M132 as well. So we need to merge back the fix to M132.

### qk...@google.com (2025-03-11)

Labelling as not applicable for LTS 126, because the bug has reproduced since M132 according to the comment #3.

### dx...@google.com (2025-04-08)

Project: chromium/src  

Branch: refs/branch-heads/6834  

Author: Philip Pfaffe [pfaffe@chromium.org](mailto:pfaffe@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6320854>

[M132-LTS] Fix crash in DOM snapshot agent

---


Expand for full commit details
```
     
    When taking as snapshot, the DOM snapshot agent holds a pointer to a 
    hashmap on the stack. The hashmap is destroyed when the devtools session 
    detaches, so if that happens while taking a snapshot we run into a 
    crash. 
     
    (cherry picked from commit 4fa8d897f83ab2ee66dc3505409a6e44936d7e4c) 
     
    Fixed: 395032416 
    Change-Id: I4b784cb3105f6a760ca5b1d3dcbe1ea254b3ad3a 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6297444 
    Reviewed-by: Alex Rudenko <alexrudenko@chromium.org> 
    Commit-Queue: Philip Pfaffe <pfaffe@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1425198} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6320854 
    Commit-Queue: Michael Ershov <miersh@google.com> 
    Reviewed-by: Michael Ershov <miersh@google.com> 
    Cr-Commit-Position: refs/branch-heads/6834@{#5543} 
    Cr-Branched-From: 47a3549fac11ee8cb7be6606001ede605b302b9f-refs/heads/main@{#1381561}

```

---

Files:

- M `third_party/blink/renderer/core/inspector/inspector_dom_snapshot_agent.cc`
- M `third_party/blink/renderer/core/inspector/inspector_dom_snapshot_agent.h`
- M `third_party/blink/renderer/core/inspector/legacy_dom_snapshot_agent.cc`
- M `third_party/blink/renderer/core/inspector/legacy_dom_snapshot_agent.h`

---

Hash: 763582509c827063a5daccad48f9b2d3a3542ce4  

Date:  Tue Apr 8 09:21:19 2025


---

### dx...@google.com (2025-05-29)

Project: chromium/src  

Branch: refs/branch-heads/6834\_160  

Author: Philip Pfaffe [pfaffe@chromium.org](mailto:pfaffe@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6604440>

[CfM-R132] [M132-LTS] Fix crash in DOM snapshot agent

---


Expand for full commit details
```
     
    When taking as snapshot, the DOM snapshot agent holds a pointer to a 
    hashmap on the stack. The hashmap is destroyed when the devtools session 
    detaches, so if that happens while taking a snapshot we run into a 
    crash. 
     
    (cherry picked from commit 4fa8d897f83ab2ee66dc3505409a6e44936d7e4c) 
     
    (cherry picked from commit 763582509c827063a5daccad48f9b2d3a3542ce4) 
     
    Fixed: 395032416 
    Change-Id: I4b784cb3105f6a760ca5b1d3dcbe1ea254b3ad3a 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6297444 
    Reviewed-by: Alex Rudenko <alexrudenko@chromium.org> 
    Commit-Queue: Philip Pfaffe <pfaffe@chromium.org> 
    Cr-Original-Original-Commit-Position: refs/heads/main@{#1425198} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6320854 
    Commit-Queue: Michael Ershov <miersh@google.com> 
    Reviewed-by: Michael Ershov <miersh@google.com> 
    Cr-Original-Commit-Position: refs/branch-heads/6834@{#5543} 
    Cr-Original-Branched-From: 47a3549fac11ee8cb7be6606001ede605b302b9f-refs/heads/main@{#1381561} 
    Signed-off-by: Kyle Williams <kdgwill@google.com> 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6604440 
    Commit-Queue: Kyle Williams <kdgwill@chromium.org> 
    Auto-Submit: Kyle Williams <kdgwill@chromium.org> 
    Owners-Override: Kyle Williams <kdgwill@chromium.org> 
    Reviewed-by: Niko Tsirakis <ntsirakis@google.com> 
    Cr-Commit-Position: refs/branch-heads/6834_160@{#69} 
    Cr-Branched-From: cdae089eab830291f81deb011febbbdc520a019e-refs/branch-heads/6834@{#4409} 
    Cr-Branched-From: 47a3549fac11ee8cb7be6606001ede605b302b9f-refs/heads/main@{#1381561}

```

---

Files:

- M `third_party/blink/renderer/core/inspector/inspector_dom_snapshot_agent.cc`
- M `third_party/blink/renderer/core/inspector/inspector_dom_snapshot_agent.h`
- M `third_party/blink/renderer/core/inspector/legacy_dom_snapshot_agent.cc`
- M `third_party/blink/renderer/core/inspector/legacy_dom_snapshot_agent.h`

---

Hash: 93157dc842d985203778fde13a3d77172127b31f  

Date:  Thu May 29 20:15:53 2025


---

### ch...@google.com (2025-06-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/395032416)*
