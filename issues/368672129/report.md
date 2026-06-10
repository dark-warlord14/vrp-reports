# heap-use-after-free in blink::InspectorPageAgent::EvaluateScriptOnNewDocument

| Field | Value |
|-------|-------|
| **Issue ID** | [368672129](https://issues.chromium.org/issues/368672129) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | as...@gmail.com |
| **Assignee** | sz...@google.com |
| **Created** | 2024-09-21 |
| **Bounty** | $4,000.00 |

## Description

VULNERABILITY DETAILS
UAF in blink::InspectorPageAgent::EvaluateScriptOnNewDocument

VERSION
Chrome Version: 131.0.6724.0（Developer Build）
Operating System: Ubuntu

Chrome Version: 130.0.6688.0（Developer Build）
Operating System: Windows 11 23H2 (OS Build 22631.4037)

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

- [background.js](attachments/background.js) (text/javascript, 968 B)
- [manifest.json](attachments/manifest.json) (application/json, 160 B)
- [asan.log](attachments/asan.log) (text/plain, 52.1 KB)

## Timeline

### as...@gmail.com (2024-09-21)

I forgot to upload the asan.log file.

### as...@gmail.com (2024-09-22)

Bisect

This problem is introduced in this commit: 5a69a36e332590f18782b0669f25a28a829cf244
https://chromium-review.googlesource.com/c/chromium/src/+/5104799

### sk...@google.com (2024-09-23)

Thank you for the bug report! I was not able to reproduce, but with the stack trace provided in the first comment, I can assign to the relevant code editors

### sz...@google.com (2024-09-24)

Looks like this is another case where we tear down the DevTools session during the nested run-loop of a debugger pause, while the probe::DidCreateMainWorldContext still fires for the detached session and this causes us to access the freed `v8_session_` in `inspector_page_agent.cc:1084`: <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/inspector/inspector_page_agent.cc;l=1084;drc=35f2c2d656975fab1589ba289ab04949f451ecc7>.

So in the end the probe runs on a disposed agent. A cheap solution would be to reset `v8_session_` to `nullptr` in `Dispose` and check for it before calling evaluate. I don't have a better idea how to solve this, as the `EvaluateScriptsOnNewDocument` can always cause a pause, that then subsequently causes a session tear down, while we are still processing other `EvaluteScriptsOnNewDocument` scripts.

### pf...@google.com (2024-09-24)

+1 on resetting the session on dispose.

### pe...@google.com (2024-09-24)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-09-24)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### ap...@google.com (2024-09-25)

Project: chromium/src
Branch: main

commit 622d2fd964161261c4a5afeaad7df547bb04e0aa
Author: Simon Zünd <szuend@chromium.org>
Date:   Wed Sep 25 04:29:39 2024

    [inspector] Fix accessing disposed V8 session in page agent
    
    Scripts running as part of Page.evaluateScriptOnNewDocument can pause
    the page. During a pause we can detach the DevTools session, but the
    page agent is still in the middle of running the
    "DidCreateMainWorldContext" probe. This means any additional
    Page.evaluateScriptOnNewDocument scripts would attempt to eval on
    a detached V8 session.
    
    This CL fixes this by overriding InspectorBaseAgent::Dispose in the
    page agent and resetting `v8_session_` to a nullptr which we can
    check for before evaling more scripts.
    
    This check is only necessary for page agent methods that execute
    more than one JS script as for all the others we wouldn't call
    the probes on a disposed agent in the first place.
    
    R=caseq@chromium.org, dsv@chromium.org
    
    Fixed: 368672129
    Change-Id: I4c3361c8116a64343206da991e503aaa6bd917f6
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5886170
    Reviewed-by: Danil Somsikov <dsv@chromium.org>
    Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
    Commit-Queue: Simon Zünd <szuend@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1359730}

M       third_party/blink/renderer/core/inspector/inspector_page_agent.cc
M       third_party/blink/renderer/core/inspector/inspector_page_agent.h
A       third_party/blink/web_tests/http/tests/inspector-protocol/page/addScriptToEvaluateOnNewDocument-reload-pause-expected.txt
A       third_party/blink/web_tests/http/tests/inspector-protocol/page/addScriptToEvaluateOnNewDocument-reload-pause.js

https://chromium-review.googlesource.com/5886170


### pe...@google.com (2024-09-25)

Security Merge Request Consideration: Requesting merge to beta (M130) because latest trunk commit (1359730) appears to be after beta branch point (1356013).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### am...@chromium.org (2024-09-25)

This issue looks to have been around well before M130; updating to M128 since it's current Extended Stable / current oldest active release channel and updating SI accordingly.
Since this fix was landed < 24 hours ago, letting it get a bit more bake time and will be revisit tomorrow for potential merge

### sz...@google.com (2024-09-26)

1. <https://crrev.com/c/5886170>
2. No, it would require ASAN canary
3. No
4. No
5. No

### pe...@google.com (2024-09-26)

Merge review required: M130 is already shipping to beta.

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
Owners: eakpobaro (Android), eakpobaro (iOS), gmpritchard (ChromeOS), danielyip (Desktop)

### sz...@google.com (2024-09-26)

1. Security issue.
2. <https://crrev.com/c/5886170>
3. Released yes, tested no since it requires an ASAN build of Canary.
4. No
5. No

### am...@chromium.org (2024-09-26)

Triggering this UAF requires a compromised renderer + an extension with the debugger permission; lowering severity to medium severity.

As such, I'm reviewing this fix only for backmerge to M130 Beta rather than to also Stable (M129) and Extended Stable (M128), which would be consistent with sev-high issues.

<https://crrev.com/c/5886170> approved for merge to M130, please merge this fix to branch 6723 at your earliest convenience so this fix can be included in the next M130 beta update.

### ap...@google.com (2024-09-26)

Project: chromium/src
Branch: refs/branch-heads/6723

commit 0cba41b67f772c1ee3f153d739fb08e09ba3aef0
Author: Simon Zünd <szuend@chromium.org>
Date:   Thu Sep 26 10:17:56 2024

    [inspector] Fix accessing disposed V8 session in page agent
    
    Scripts running as part of Page.evaluateScriptOnNewDocument can pause
    the page. During a pause we can detach the DevTools session, but the
    page agent is still in the middle of running the
    "DidCreateMainWorldContext" probe. This means any additional
    Page.evaluateScriptOnNewDocument scripts would attempt to eval on
    a detached V8 session.
    
    This CL fixes this by overriding InspectorBaseAgent::Dispose in the
    page agent and resetting `v8_session_` to a nullptr which we can
    check for before evaling more scripts.
    
    This check is only necessary for page agent methods that execute
    more than one JS script as for all the others we wouldn't call
    the probes on a disposed agent in the first place.
    
    R=caseq@chromium.org, dsv@chromium.org
    
    (cherry picked from commit 622d2fd964161261c4a5afeaad7df547bb04e0aa)
    
    Fixed: 368672129
    Change-Id: I4c3361c8116a64343206da991e503aaa6bd917f6
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5886170
    Reviewed-by: Danil Somsikov <dsv@chromium.org>
    Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
    Commit-Queue: Simon Zünd <szuend@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1359730}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5890836
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Commit-Queue: Danil Somsikov <dsv@chromium.org>
    Auto-Submit: Simon Zünd <szuend@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6723@{#498}
    Cr-Branched-From: 985f2961df230630f9cbd75bd6fe463009855a11-refs/heads/main@{#1356013}

M       third_party/blink/renderer/core/inspector/inspector_page_agent.cc
M       third_party/blink/renderer/core/inspector/inspector_page_agent.h
A       third_party/blink/web_tests/http/tests/inspector-protocol/page/addScriptToEvaluateOnNewDocument-reload-pause-expected.txt
A       third_party/blink/web_tests/http/tests/inspector-protocol/page/addScriptToEvaluateOnNewDocument-reload-pause.js

https://chromium-review.googlesource.com/5890836


### pe...@google.com (2024-09-26)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### sz...@google.com (2024-09-27)

1. The regression happened with M122.
2. No

### pe...@google.com (2024-10-02)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2024-10-02)

1. https://chromium-review.googlesource.com/c/chromium/src/+/5901054
2. Low, no conflicts
3. 130
4. Yes

### sp...@google.com (2024-10-03)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $4000.00 for this report.

Rationale for this decision:
$3,000 for report of moderately mitigated memory corruption + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-10-03)

Congratulations Sakana.S! Thank you for your efforts and reporting this issue to us!

### as...@gmail.com (2024-10-03)

Thank you very much, cheers! 🥂

### ap...@google.com (2024-11-07)

Project: chromium/src  

Branch: refs/branch-heads/6478  

Author: Simon Zünd <[szuend@chromium.org](mailto:szuend@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5901054>

[M126-LTS][inspector] Fix accessing disposed V8 session in page agent

---


Expand for full commit details
```
[M126-LTS][inspector] Fix accessing disposed V8 session in page agent 
 
Scripts running as part of Page.evaluateScriptOnNewDocument can pause 
the page. During a pause we can detach the DevTools session, but the 
page agent is still in the middle of running the 
"DidCreateMainWorldContext" probe. This means any additional 
Page.evaluateScriptOnNewDocument scripts would attempt to eval on 
a detached V8 session. 
 
This CL fixes this by overriding InspectorBaseAgent::Dispose in the 
page agent and resetting `v8_session_` to a nullptr which we can 
check for before evaling more scripts. 
 
This check is only necessary for page agent methods that execute 
more than one JS script as for all the others we wouldn't call 
the probes on a disposed agent in the first place. 
 
R=caseq@chromium.org, dsv@chromium.org 
 
(cherry picked from commit 622d2fd964161261c4a5afeaad7df547bb04e0aa) 
 
Fixed: 368672129 
Change-Id: I4c3361c8116a64343206da991e503aaa6bd917f6 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5886170 
Reviewed-by: Danil Somsikov <dsv@chromium.org> 
Reviewed-by: Andrey Kosyakov <caseq@chromium.org> 
Commit-Queue: Simon Zünd <szuend@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1359730} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5901054 
Reviewed-by: Mohamed Omar <mohamedaomar@google.com> 
Reviewed-by: Alex Rudenko <alexrudenko@chromium.org> 
Owners-Override: Mohamed Omar <mohamedaomar@google.com> 
Commit-Queue: Alex Rudenko <alexrudenko@chromium.org> 
Cr-Commit-Position: refs/branch-heads/6478@{#1993} 
Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

```

---

Files:

- M `third_party/blink/renderer/core/inspector/inspector_page_agent.cc`
- M `third_party/blink/renderer/core/inspector/inspector_page_agent.h`
- A `third_party/blink/web_tests/http/tests/inspector-protocol/page/addScriptToEvaluateOnNewDocument-reload-pause-expected.txt`
- A `third_party/blink/web_tests/http/tests/inspector-protocol/page/addScriptToEvaluateOnNewDocument-reload-pause.js`

---

Hash: 9b7b18d1447c09c8326435e5a0529899dc9eb0e0  

Date:  Thu Nov 07 07:46:44 2024


---

### ap...@google.com (2024-11-11)

Project: chromium/src  

Branch: refs/branch-heads/6478\_182  

Author: Simon Zünd <[szuend@chromium.org](mailto:szuend@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6011315>

[CfM-R126][inspector] Fix accessing disposed V8 session in page agent

---


Expand for full commit details
```
[CfM-R126][inspector] Fix accessing disposed V8 session in page agent 
 
Scripts running as part of Page.evaluateScriptOnNewDocument can pause 
the page. During a pause we can detach the DevTools session, but the 
page agent is still in the middle of running the 
"DidCreateMainWorldContext" probe. This means any additional 
Page.evaluateScriptOnNewDocument scripts would attempt to eval on 
a detached V8 session. 
 
This CL fixes this by overriding InspectorBaseAgent::Dispose in the 
page agent and resetting `v8_session_` to a nullptr which we can 
check for before evaling more scripts. 
 
This check is only necessary for page agent methods that execute 
more than one JS script as for all the others we wouldn't call 
the probes on a disposed agent in the first place. 
 
R=caseq@chromium.org, dsv@chromium.org 
 
(cherry picked from commit 622d2fd964161261c4a5afeaad7df547bb04e0aa) 
 
(cherry picked from commit 9b7b18d1447c09c8326435e5a0529899dc9eb0e0) 
 
Fixed: 368672129 
Change-Id: I4c3361c8116a64343206da991e503aaa6bd917f6 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5886170 
Reviewed-by: Danil Somsikov <dsv@chromium.org> 
Reviewed-by: Andrey Kosyakov <caseq@chromium.org> 
Commit-Queue: Simon Zünd <szuend@chromium.org> 
Cr-Original-Original-Commit-Position: refs/heads/main@{#1359730} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5901054 
Reviewed-by: Mohamed Omar <mohamedaomar@google.com> 
Reviewed-by: Alex Rudenko <alexrudenko@chromium.org> 
Owners-Override: Mohamed Omar <mohamedaomar@google.com> 
Commit-Queue: Alex Rudenko <alexrudenko@chromium.org> 
Cr-Original-Commit-Position: refs/branch-heads/6478@{#1993} 
Cr-Original-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6011315 
Owners-Override: Kyle Williams <kdgwill@chromium.org> 
Auto-Submit: Kyle Williams <kdgwill@chromium.org> 
Commit-Queue: Kyle Williams <kdgwill@chromium.org> 
Reviewed-by: Niko Tsirakis <ntsirakis@google.com> 
Cr-Commit-Position: refs/branch-heads/6478_182@{#103} 
Cr-Branched-From: 5b5d8292ddf182f8b2096fa665b473b6317906d5-refs/branch-heads/6478@{#1776} 
Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

```

---

Files:

- M `third_party/blink/renderer/core/inspector/inspector_page_agent.cc`
- M `third_party/blink/renderer/core/inspector/inspector_page_agent.h`
- A `third_party/blink/web_tests/http/tests/inspector-protocol/page/addScriptToEvaluateOnNewDocument-reload-pause-expected.txt`
- A `third_party/blink/web_tests/http/tests/inspector-protocol/page/addScriptToEvaluateOnNewDocument-reload-pause.js`

---

Hash: a092b80eb48a4fbbc1c0c4cb5ac08be6ef02d660  

Date:  Mon Nov 11 19:46:24 2024


---

### pe...@google.com (2025-01-02)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/368672129)*
