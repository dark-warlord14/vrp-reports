# use-after-poison in blink::DevToolsSession::DispatchProtocolCommandImpl

| Field | Value |
|-------|-------|
| **Issue ID** | [384844003](https://issues.chromium.org/issues/384844003) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | as...@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2024-12-18 |
| **Bounty** | $2,000.00 |

## Description

VULNERABILITY DETAILS
UAP in blink::DevToolsSession::DispatchProtocolCommandImpl

VERSION
Chrome Version: 133.0.6889.0（Developer Build）
Operating System: Ubuntu 24.04

REPRODUCTION CASE
1. put manifest.json/background.js into the extension_path
2. run the command:
 ./chrome --user-data-dir=./noexist --no-sandbox --load-extension="extension_path"

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: renderer
Crash State: see asan.log file

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: Sakana.S

## Attachments

- [manifest.json](attachments/manifest.json) (application/json, 160 B)
- [background.js](attachments/background.js) (text/javascript, 506 B)
- [asan.log](attachments/asan.log) (text/plain, 9.2 KB)

## Timeline

### dc...@chromium.org (2024-12-19)

I've confirmed this repros in M130 and trunk. At ToT, something like the following should work:

```
out/asan/chrome --user-data-dir=$(mktemp -d) --load-extension=$HOME/src/chrome/src/repro/ext --no-first-run --skip-first-run |& tools/valgrind/asan/asan_symbolize.py

```

Where the extension from the original report is in `~/src/chrome/src/repro/ext`

### pe...@google.com (2024-12-19)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-12-24)

This Chrome DevTools issue has `Found In` milestone information, but is still on the Unconfirmed hotlist. Assuming that this issue is therefore considered confirmed, please provide any additional information that is still missing and remove it from the Unconfirmed hotlist so that it can be further triaged by the product team.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-12-30)

This Chrome DevTools issue has `Found In` milestone information, but is still on the Unconfirmed hotlist. Assuming that this issue is therefore considered confirmed, please provide any additional information that is still missing and remove it from the Unconfirmed hotlist so that it can be further triaged by the product team.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### aj...@google.com (2024-12-30)

Based on [comment #2](https://issues.chromium.org/issues/384844003#comment2), removing Unconfirmed hotlist from this bug for further triaging.

### pa...@chromium.org (2025-01-10)

[secondary] Hi caseq@, would you have any update on this bug?

### ap...@google.com (2025-01-15)

Project: chromium/src  

Branch: main  

Author: Andrey Kosyakov <[caseq@chromium.org](mailto:caseq@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6175790>

Make DevToolsAgent::Client a GCMixin, since the implementation is GCed

---


Expand for full commit details
```
Make DevToolsAgent::Client a GCMixin, since the implementation is GCed 
 
We used to keep a raw pointer to Client in DevToolsAgent, which does 
not play well when the implementation is getting collected. 
 
Bug: 384844003 
Change-Id: Id34886635955133f0be746a9e6e910f9e6891dbf 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6175790 
Commit-Queue: Andrey Kosyakov <caseq@chromium.org> 
Reviewed-by: Daniel Cheng <dcheng@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1406819}

```

---

Files:

- M `third_party/blink/renderer/core/exported/web_dev_tools_agent_impl.h`
- M `third_party/blink/renderer/core/inspector/devtools_agent.cc`
- M `third_party/blink/renderer/core/inspector/devtools_agent.h`
- M `third_party/blink/renderer/core/inspector/worker_inspector_controller.h`

---

Hash: bc43bccd60f6d79d329ed70231547d75ac57bd4b  

Date:  Wed Jan 15 10:17:13 2025


---

### pe...@google.com (2025-01-16)

Security Merge Request Consideration: Requesting merge to stable (M132) because latest trunk commit (1406819) appears to be after stable branch point (1381561).
Security Merge Request Consideration: Requesting merge to beta (M133) because latest trunk commit (1406819) appears to be after beta branch point (1402768).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### am...@chromium.org (2025-01-16)

This fix just landed < 24 hours ago, therefore there's not yet sufficient canary bake time for a merge. We'll need to revisit this issue tomorrow at the earliest for merge review / approval.

### pe...@google.com (2025-01-16)

**Merge approved:** your change passed merge requirements and is auto-approved for M133. Please go ahead and merge the CL to branch 6943 (refs/branch-heads/6943) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: andywu (ChromeOS), pbommana (Desktop US), danielyip (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### pe...@google.com (2025-01-16)

Merge review required: M132 is already shipping to stable.

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
Owners: govind (Android), govind (iOS), alonbajayo (ChromeOS), srinivassista (Desktop)

### ap...@google.com (2025-01-16)

Project: chromium/src  

Branch: refs/branch-heads/6943  

Author: Andrey Kosyakov <[caseq@chromium.org](mailto:caseq@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6179740>

Make DevToolsAgent::Client a GCMixin, since the implementation is GCed

---


Expand for full commit details
```
Make DevToolsAgent::Client a GCMixin, since the implementation is GCed 
 
We used to keep a raw pointer to Client in DevToolsAgent, which does 
not play well when the implementation is getting collected. 
 
(cherry picked from commit bc43bccd60f6d79d329ed70231547d75ac57bd4b) 
 
Bug: 384844003 
Change-Id: Id34886635955133f0be746a9e6e910f9e6891dbf 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6175790 
Commit-Queue: Andrey Kosyakov <caseq@chromium.org> 
Reviewed-by: Daniel Cheng <dcheng@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1406819} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6179740 
Commit-Queue: Nate Chapin <japhet@chromium.org> 
Reviewed-by: Nate Chapin <japhet@chromium.org> 
Auto-Submit: Andrey Kosyakov <caseq@chromium.org> 
Cr-Commit-Position: refs/branch-heads/6943@{#342} 
Cr-Branched-From: 72dd0b377c099e1e0230cc7345d5a5125b46ae7d-refs/heads/main@{#1402768}

```

---

Files:

- M `third_party/blink/renderer/core/exported/web_dev_tools_agent_impl.h`
- M `third_party/blink/renderer/core/inspector/devtools_agent.cc`
- M `third_party/blink/renderer/core/inspector/devtools_agent.h`
- M `third_party/blink/renderer/core/inspector/worker_inspector_controller.h`

---

Hash: 9044bcbe4e163ad98a293dbd402ebc1081dd2cd3  

Date:  Thu Jan 16 13:41:30 2025


---

### pe...@google.com (2025-01-16)

LTS Milestone M132

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### am...@chromium.org (2025-01-17)

Thanks for doing the merge to 133 based on the bot approval. In terms of backmerge to 132, I'd like to pause until early next week.
Deadline for merges for 132 are EOD today and this only has just over a day on Canary.
Given that this is a renderer memory corruption that requires installation of an extension with debugger permissions, I don't think rushing to backmerge is warranted yet. Let's keep this in the queue until next week.

### am...@chromium.org (2025-01-23)

This is a read in the renderer, which also requires an extension which qualifies as medium severity.

### sp...@google.com (2025-01-23)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
report of moderately mitigated memory corruption in a sandboxed process / renderer 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-01-23)

Thank you for your efforts and reporting this issue to us!

### as...@gmail.com (2025-01-23)

Thank you very much!

### am...@chromium.org (2025-01-23)

<https://crrev.com/c/6175790> approved for merge to M132, please merge this fix to branch 6834 at your earliest convenience

### sr...@chromium.org (2025-01-24)



Please complete your merge before EOD today Jan 24, so it can be part of next week respin for m132

### ap...@google.com (2025-01-24)

Project: chromium/src  

Branch: refs/branch-heads/6834  

Author: Andrey Kosyakov <[caseq@chromium.org](mailto:caseq@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6198801>

[m132] Make DevToolsAgent::Client a GCMixin, since the implementation is GCed

---


Expand for full commit details
```
[m132] Make DevToolsAgent::Client a GCMixin, since the implementation is GCed 
 
We used to keep a raw pointer to Client in DevToolsAgent, which does 
not play well when the implementation is getting collected. 
 
(cherry picked from commit bc43bccd60f6d79d329ed70231547d75ac57bd4b) 
 
Bug: 384844003 
Change-Id: Id34886635955133f0be746a9e6e910f9e6891dbf 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6175790 
Commit-Queue: Andrey Kosyakov <caseq@chromium.org> 
Reviewed-by: Daniel Cheng <dcheng@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1406819} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6198801 
Commit-Queue: Nate Chapin <japhet@chromium.org> 
Reviewed-by: Nate Chapin <japhet@chromium.org> 
Auto-Submit: Andrey Kosyakov <caseq@chromium.org> 
Cr-Commit-Position: refs/branch-heads/6834@{#4261} 
Cr-Branched-From: 47a3549fac11ee8cb7be6606001ede605b302b9f-refs/heads/main@{#1381561}

```

---

Files:

- M `third_party/blink/renderer/core/exported/web_dev_tools_agent_impl.h`
- M `third_party/blink/renderer/core/inspector/devtools_agent.cc`
- M `third_party/blink/renderer/core/inspector/devtools_agent.h`
- M `third_party/blink/renderer/core/inspector/worker_inspector_controller.h`

---

Hash: ae4161ad75f7b1876b4e3b984a0dc6e9aa9ec770  

Date:  Fri Jan 24 13:16:21 2025


---

### pe...@google.com (2025-01-29)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### rz...@google.com (2025-01-29)

Re #23

1. <https://crrev.com/c/6206909>
2. Low, no conflcits
3. 132, 133
4. Yes

### pe...@google.com (2025-01-29)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### ap...@google.com (2025-01-31)

Project: chromium/src  

Branch: refs/branch-heads/6478  

Author: Andrey Kosyakov <[caseq@chromium.org](mailto:caseq@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6206909>

[M126-LTS] Make DevToolsAgent::Client a GCMixin, since the implementation is GCed

---


Expand for full commit details
```
[M126-LTS] Make DevToolsAgent::Client a GCMixin, since the implementation is GCed 
 
We used to keep a raw pointer to Client in DevToolsAgent, which does 
not play well when the implementation is getting collected. 
 
(cherry picked from commit bc43bccd60f6d79d329ed70231547d75ac57bd4b) 
 
Bug: 384844003 
Change-Id: Id34886635955133f0be746a9e6e910f9e6891dbf 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6175790 
Commit-Queue: Andrey Kosyakov <caseq@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1406819} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6206909 
Reviewed-by: Nate Chapin <japhet@chromium.org> 
Reviewed-by: Andrey Kosyakov <caseq@chromium.org> 
Cr-Commit-Position: refs/branch-heads/6478@{#2027} 
Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

```

---

Files:

- M `third_party/blink/renderer/core/exported/web_dev_tools_agent_impl.h`
- M `third_party/blink/renderer/core/inspector/devtools_agent.cc`
- M `third_party/blink/renderer/core/inspector/devtools_agent.h`
- M `third_party/blink/renderer/core/inspector/worker_inspector_controller.h`

---

Hash: 502e6a62070103a1cbef50ea9ccbf50699ec814e  

Date:  Thu Jan 30 17:43:26 2025


---

### ch...@google.com (2025-04-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/384844003)*
