# UAF in v8_inspector

| Field | Value |
|-------|-------|
| **Issue ID** | [40063469](https://issues.chromium.org/issues/40063469) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Android, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2023-03-09 |
| **Bounty** | $1,000.00 |

## Description

**Steps to reproduce the problem:**  

Will attach details soon.

**Problem Description:**  

use after free

**Additional Comments:**

\*\*Chrome version: \*\* 113.0.5638.0 \*\*Channel: \*\* Canary

**OS:** Linux

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 26.3 KB)
- [background.js](attachments/background.js) (text/plain, 840.8 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 494 B)

## Timeline

### [Deleted User] (2023-03-09)

[Empty comment from Monorail migration]

### he...@gmail.com (2023-03-09)

I found this UAF by loading the extension. However, seems that the reproduction rate is a little bit low, I'm still investigating it.

### ma...@chromium.org (2023-03-10)

Thank you for this report. We will wait for you to provide a PoC or more detailed steps to reproduce this issue.
Without those, we may not be able to perform validation or root cause of this issue in a timely manner and may greatly increase the time to resolution and fix.

Based on the asan trace it appears to be a devtools debugger/inspector issue, setting component.
Tentatively assigned to jarin who changed some code in that area somewhat recently.
jarin – the Security Team is unable to reproduce this issue based on information provided. If you can diagnose and fix the issue based on information provided, please proceed accordingly. Please provide a comment about when this issue may have been introduced or which active release branches of Chrome may be impacted. 
This information is critical so that we can ensure fixes are released urgently to help protect against n-day exploitation of newly landed security fixes, and so that we can avoid release of security regressions.

Based on information provided it is unclear what severity should be, leaving unset for now.

[Monorail components: Platform>DevTools>JavaScript]

### ya...@google.com (2023-03-10)

This looks like we are iterating the list of scripts in m_scripts [0] after we have disabled the Debugger domain, where we clear m_scripts [1].

That seems somewhat unlikely since we check whether the domain is enabled when entering setBreakpointByUrl [2].

The only way I currently can see this happen is if we run a nested event loop within setBreakpointByUrl. So we enter setBreakpointByUrl first, check that the Debugger domain is enabled, and continue further into the function. Within the function we run the event loop, and handle a message that disables the Debugger domain. When we return back to setBreakpointByUrl, we continue to the point of iterating m_scripts and here is when the UAF happens.


[0] https://source.chromium.org/chromium/chromium/src/+/main:v8/src/inspector/v8-debugger-agent-impl.cc;l=653;drc=a286a3f191ffb9ffa36c502a24ed4b0bce0115fb
[1] https://source.chromium.org/chromium/chromium/src/+/main:v8/src/inspector/v8-debugger-agent-impl.cc;l=500;drc=a286a3f191ffb9ffa36c502a24ed4b0bce0115fb
[2] https://source.chromium.org/chromium/chromium/src/+/main:v8/src/inspector/v8-debugger-agent-impl.cc;l=593;drc=a286a3f191ffb9ffa36c502a24ed4b0bce0115fb

### he...@gmail.com (2023-03-10)

Hello, to reproduce it, just load the attached extension. 

However, I only successfully repro it with the ChromeOS on Linux. The reproduction rate is about 1/10, it may depends on the machine environment.

### ja...@chromium.org (2023-03-10)

Unfortunately, this can happen at session shutdown (see crrev.com/c/4110931, crrev.com/c/4085143), where we first disable the session on an interrupt, and do the full tear-down on the main thread.

The bad scenario here is calling setBreakpointByUrl with a regexp and then immediately closing the session.

What happens here is that setBreakpointByUrl runs v8 regexp, the regexp is interrupted with the session stop call, the session stop removes the script, and returns back to setBreakpointByUrl.

One can fix this by some protection from re-entrancy. For example, avoiding processing messages from IO thread if we are in the middle of running such a message.

Another possible protection is checking if the debugger is still enable after calling the regexp in setBreakpointByUrl.

### ja...@chromium.org (2023-03-10)

[Empty comment from Monorail migration]

### ya...@google.com (2023-03-10)

It looks like setBreakPointByUrl can be provided with a regexp parameter to match URL by regexp, which is checked in the call to `matches` [0]. That calls through V8Regex::match, which does something suspicious: it gets the "exec" method from the RegExp object and calls it [1].

If the "exec" method can be overridden by the user, it could be used to run a nested event loop. We should use V8::RegExp::Exec instead, which is protected against monkeypatching.

I have not verified this theory.

[0] https://source.chromium.org/chromium/chromium/src/+/main:v8/src/inspector/v8-debugger-agent-impl.cc;l=654;drc=26d5a0721a1b21ded47b31a3fc0a5ef4928d5b80
[1] https://source.chromium.org/chromium/chromium/src/+/main:v8/src/inspector/v8-regex.cc;l=72;drc=26d5a0721a1b21ded47b31a3fc0a5ef4928d5b80

### ya...@google.com (2023-03-10)

[Empty comment from Monorail migration]

### ja...@google.com (2023-03-10)

At the end, I wrote a very targeted patch that avoids touching sensitive fields (such as m_scripts or the cookie objects) while creating the V8 regexp object. We should perhaps think harder how we could eliminate the interrupt inside the V8 regexp altogether.

Patch (v8): http://crrev.com/c/4329135
Test (Blink): http://crrev.com/c/4329299

### gi...@appspot.gserviceaccount.com (2023-03-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/20eab6ec54a6f5361d5ee1b78502c8615a9ae8e1

commit 20eab6ec54a6f5361d5ee1b78502c8615a9ae8e1
Author: Jaroslav Sevcik <jarin@chromium.org>
Date: Fri Mar 10 15:40:11 2023

[inspector] Create shared regexp object for regex breakpoints

The patch hoists creation of regex object out of the script loop (when
setting breakpoints via an url regexp).

Bug: chromium:1422830
Change-Id: I700fcf5f3cf20e73ab87f978b464fc7a9955d9d5
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4329135
Reviewed-by: Simon Zünd <szuend@chromium.org>
Commit-Queue: Jaroslav Sevcik <jarin@chromium.org>
Cr-Commit-Position: refs/heads/main@{#86368}

[modify] https://crrev.com/20eab6ec54a6f5361d5ee1b78502c8615a9ae8e1/src/inspector/v8-debugger-agent-impl.cc


### ja...@chromium.org (2023-03-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-14)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### he...@gmail.com (2023-03-14)

Thanks for the fix. I could verify that it is no longer reproducible on the latest chromium.

### ja...@chromium.org (2023-03-15)

Setting security severity to medium because this needs an extension with the chrome.debugger permission to trigger.

This particular path to the UAF was introduced in M110, but I believe it was always possible to get the UAF through a more elaborate path (invoking then debugger pause during setBreakpointByUrl and then disabling the debugger while paused with the Debugger.disable CDP method).



### [Deleted User] (2023-03-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-15)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-15)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M112. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge rejected: M112 is already shipping to beta and this issue is marked as a Pri-2, Pri-3, or Type-Feature.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), obenedict (ChromeOS), srinivassista (Desktop)

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ja...@chromium.org (2023-03-16)

1. CL to backmerge: https://chromium-review.googlesource.com/c/v8/v8/+/4329135
2. Yes, the fix has been tested on Canary.
3. The fix has been verified, also by the original reporter. The stability risk is tiny (the fix is small and local to the debugger).
4. No known compatibility risk.
5. No manual verification is necessary - we do not change any observable behavior, the bug can only be triggered programmatically from an extension.

### ja...@chromium.org (2023-03-16)

Clarification: The CL (https://crrev.com/c/4329135) needs to backmerged from/via v8.

### [Deleted User] (2023-03-16)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M112. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: M112 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [112].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-03-17)

Thanks for landing this fix and all the helpful updates in https://crbug.com/chromium/1422830#c15 and #20, jarin@ 
M112 merge approved, please merge this fix to branch 5615 at your earliest convenience.

### gi...@appspot.gserviceaccount.com (2023-03-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/79b94e860d153d82449aaaceb7f2362e9200d077

commit 79b94e860d153d82449aaaceb7f2362e9200d077
Author: Jaroslav Sevcik <jarin@chromium.org>
Date: Fri Mar 10 15:40:11 2023

Merged: [inspector] Create shared regexp object for regex breakpoints

The patch hoists creation of regex object out of the script loop (when
setting breakpoints via an url regexp).

Bug: chromium:1422830
Change-Id: Ifc6117ad6c9de41844c2531c6c7d9f8fa4b27627
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4350697
Reviewed-by: Simon Zünd <szuend@chromium.org>
Commit-Queue: Jaroslav Sevcik <jarin@chromium.org>
Cr-Commit-Position: refs/branch-heads/11.2@{#19}
Cr-Branched-From: 755511a138609ac5939449a8ac615c15603a4454-refs/heads/11.2.214@{#1}
Cr-Branched-From: e6b1ccefb0f0f1ff8d310578878130dc53d73749-refs/heads/main@{#86014}

[modify] https://crrev.com/79b94e860d153d82449aaaceb7f2362e9200d077/src/inspector/v8-debugger-agent-impl.cc


### gi...@appspot.gserviceaccount.com (2023-03-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d6359e2726736ca75174114d87e93f3996a572e6

commit d6359e2726736ca75174114d87e93f3996a572e6
Author: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Date: Mon Mar 20 10:26:21 2023

Roll v8 11.2 from 43cb6db9fffe to 1b8efd0abd55 (2 revisions)

https://chromium.googlesource.com/v8/v8.git/+log/43cb6db9fffe..1b8efd0abd55

2023-03-20 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.2.214.8
2023-03-20 jarin@chromium.org Merged: [inspector] Create shared regexp object for regex breakpoints

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/v8-chromium-release-0
Please CC liviurau@google.com,v8-waterfall-sheriff@grotations.appspotmail.com,vahl@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in v8 11.2: https://bugs.chromium.org/p/v8/issues/entry
To file a bug in Chromium m112: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1422830
Tbr: v8-waterfall-sheriff@grotations.appspotmail.com
Change-Id: Ia59edcc6d9c44cd173acf77e81c740d8dca294e5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4352748
Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5615@{#651}
Cr-Branched-From: 9c6408ef696e83a9936b82bbead3d41c93c82ee4-refs/heads/main@{#1109224}

[modify] https://crrev.com/d6359e2726736ca75174114d87e93f3996a572e6/DEPS


### gi...@appspot.gserviceaccount.com (2023-03-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2c2ab12eb3c16446e5235ab69e56a6425bba0dc5

commit 2c2ab12eb3c16446e5235ab69e56a6425bba0dc5
Author: Jaroslav Sevcik <jarin@chromium.org>
Date: Tue Mar 21 08:48:10 2023

[test] Test disconnecting while setting a breakpoint

Bug: chromium:1422830
Change-Id: Ia4137e54e74403352f98d3fbd43e0d4a1ea62d47
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4329299
Reviewed-by: Simon Zünd <szuend@chromium.org>
Commit-Queue: Jaroslav Sevcik <jarin@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1119818}

[add] https://crrev.com/2c2ab12eb3c16446e5235ab69e56a6425bba0dc5/third_party/blink/web_tests/http/tests/inspector-protocol/debugger/set-breakpoint-regex-close.js
[add] https://crrev.com/2c2ab12eb3c16446e5235ab69e56a6425bba0dc5/third_party/blink/web_tests/http/tests/inspector-protocol/debugger/set-breakpoint-regex-close-expected.txt


### am...@google.com (2023-03-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-22)

Congratulations! The VRP Panel has decided to award you $1,000 for this report of a significantly mitigated security bug. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2023-03-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-07-06)

Hello Chaoyuan Peng -- we consider attachments/POCs and all analysis included with reports to be an integral part of the report (https://g.co/chrome/vrp/#investigating-and-reporting-bugs), including those added in comments, so I've undeleted them. Please refrain from deleting these in the future -- thank you! 

### gm...@google.com (2023-07-06)

[Empty comment from Monorail migration]

### vo...@google.com (2023-07-17)

[Empty comment from Monorail migration]

### vo...@google.com (2023-07-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-17)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vo...@google.com (2023-07-17)

1. https://crrev.com/c/4685219
2. Low - small change, simple conflicts
3. M112
4. Yes

### gm...@google.com (2023-07-18)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-07-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/8364240a3b8c82a90645ff30da6f5b28ed0c7f6f

commit 8364240a3b8c82a90645ff30da6f5b28ed0c7f6f
Author: Zakhar Voit <voit@google.com>
Date: Mon Jul 17 02:51:29 2023

[M108-LTS][inspector] Create shared regexp object for regex breakpoints

The patch hoists creation of regex object out of the script loop (when
setting breakpoints via an url regexp).

(cherry picked from commit 79b94e860d153d82449aaaceb7f2362e9200d077)

Bug: chromium:1422830
Change-Id: Ifc6117ad6c9de41844c2531c6c7d9f8fa4b27627
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4350697
Commit-Queue: Jaroslav Sevcik <jarin@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/11.2@{#19}
Cr-Original-Branched-From: 755511a138609ac5939449a8ac615c15603a4454-refs/heads/11.2.214@{#1}
Cr-Original-Branched-From: e6b1ccefb0f0f1ff8d310578878130dc53d73749-refs/heads/main@{#86014}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4685219
Reviewed-by: Victor Gabriel Savu <vsavu@google.com>
Reviewed-by: Jaroslav Sevcik <jarin@chromium.org>
Commit-Queue: Zakhar Voit <voit@google.com>
Cr-Commit-Position: refs/branch-heads/10.8@{#76}
Cr-Branched-From: f1bc03fd6b4c201abd9f0fd9d51fb989150f97b9-refs/heads/10.8.168@{#1}
Cr-Branched-From: 237de893e1c0a0628a57d0f5797483d3add7f005-refs/heads/main@{#83672}

[modify] https://crrev.com/8364240a3b8c82a90645ff30da6f5b28ed0c7f6f/src/inspector/v8-debugger-agent-impl.cc


### gi...@appspot.gserviceaccount.com (2023-07-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/dcb722779b7d5824f7832f0a3678a9d8bb1e4074

commit dcb722779b7d5824f7832f0a3678a9d8bb1e4074
Author: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Jul 21 12:00:35 2023

Roll v8 10.8 from 6bc81d02ad77 to 9953b1208ffb (2 revisions)

https://chromium.googlesource.com/v8/v8.git/+log/6bc81d02ad77..9953b1208ffb

2023-07-21 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 10.8.168.39
2023-07-21 voit@google.com [M108-LTS][inspector] Create shared regexp object for regex breakpoints

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/v8-10-8-chromium-m108
Please CC liviurau@google.com,v8-waterfall-sheriff@grotations.appspotmail.com,vahl@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in v8 10.8: https://bugs.chromium.org/p/v8/issues/entry
To file a bug in Chromium m108: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1422830
Tbr: v8-waterfall-sheriff@grotations.appspotmail.com
Change-Id: I168323b1f26ab36bf5be448581980e9fdc800cdf
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4706980
Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5359@{#1493}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/dcb722779b7d5824f7832f0a3678a9d8bb1e4074/DEPS


### vo...@google.com (2023-07-21)

One more change is needed for M108 LTS: https://crrev.com/c/4707112

### gm...@google.com (2023-07-21)

Approve the CL. Please go ahead to merge in LTS-108

### gi...@appspot.gserviceaccount.com (2023-07-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/33fd4142481b73810b023cdfe9851e36c936a958

commit 33fd4142481b73810b023cdfe9851e36c936a958
Author: Zakhar Voit <voit@google.com>
Date: Fri Jul 21 12:09:12 2023

[M108-LTS][inspector] Prevent regex breakpoints from re-entering the debugger

This patch uses the postpone-interrupts scope to prevent regexes
from re-entering the debugger when matching regex breakpoints
(while setting or removing regex breakpoints).

The test is separate in a Blink CL: crrev.com/c/4355146

(cherry picked from commit 92a918e10bd36c1045b2f750b56fdab4b4148ae4)

Bug: chromium:1426163, chromium:1422830
Change-Id: I4eb7873645a02c286664e0b6ddb53b9fb7db64f6
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4355440
Commit-Queue: Jaroslav Sevcik <jarin@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#86621}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4707112
Reviewed-by: Jaroslav Sevcik <jarin@chromium.org>
Reviewed-by: Jana Grill <janagrill@google.com>
Commit-Queue: Zakhar Voit <voit@google.com>
Cr-Commit-Position: refs/branch-heads/10.8@{#78}
Cr-Branched-From: f1bc03fd6b4c201abd9f0fd9d51fb989150f97b9-refs/heads/10.8.168@{#1}
Cr-Branched-From: 237de893e1c0a0628a57d0f5797483d3add7f005-refs/heads/main@{#83672}

[modify] https://crrev.com/33fd4142481b73810b023cdfe9851e36c936a958/src/inspector/v8-regex.cc
[modify] https://crrev.com/33fd4142481b73810b023cdfe9851e36c936a958/src/inspector/v8-debugger-agent-impl.cc


### gi...@appspot.gserviceaccount.com (2023-07-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2a582243a438309ea27d8aabd2a3c1a3c28a207c

commit 2a582243a438309ea27d8aabd2a3c1a3c28a207c
Author: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Date: Mon Jul 24 15:23:42 2023

Roll v8 10.8 from 9953b1208ffb to 7aa26911296b (2 revisions)

https://chromium.googlesource.com/v8/v8.git/+log/9953b1208ffb..7aa26911296b

2023-07-24 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 10.8.168.40
2023-07-24 voit@google.com [M108-LTS][inspector] Prevent regex breakpoints from re-entering the debugger

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/v8-10-8-chromium-m108
Please CC liviurau@google.com,v8-waterfall-sheriff@grotations.appspotmail.com,vahl@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in v8 10.8: https://bugs.chromium.org/p/v8/issues/entry
To file a bug in Chromium m108: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1422830,chromium:1426163
Tbr: v8-waterfall-sheriff@grotations.appspotmail.com
Change-Id: I30d081a33802184bead3431ee2cceda83d6b671d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4711528
Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5359@{#1494}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/2a582243a438309ea27d8aabd2a3c1a3c28a207c/DEPS


### vo...@google.com (2023-07-25)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1422830?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063469)*
