# UAF in DevToolsAgentHostImpl::ForceDetachAllSessions(with headless mode and puppeteer) 

| Field | Value |
|-------|-------|
| **Issue ID** | [40063589](https://issues.chromium.org/issues/40063589) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>DevTools |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2023-03-14 |
| **Bounty** | $2,000.00 |

## Description

UAF in DevToolsAgentHostImpl::ForceDetachAllSessions(with headless mode and puppeteer) 
chrome version:
Chromium 113.0.5651.0(gsutil ls -l gs://chromium-browser-asan/linux-release/asan-linux-release-1116741.zip)
Chromium 112.0.5615.20

This issue will repro when using automated tools, such as puppeteer, to run headless mode.
repro steps:
1.Setup environment:
    sudo apt-get install nodejs npm
    sudo npm install puppeteer -g

2.Put all the files in the attachment into a directory.
    -   test.js (You need to modify the chrome path inside)
    -   ws-poc.py
    -   sw.js
    
3.  Setup simple http server to get poc:
    python3 ./ws-poc.py
    
4.  It may output a lot of irrelevant logs, use grep to filter it.
    node ./test.js  2>&1 |grep -E 'use-after-free'
5.puppeteer opens 5 browsers, waits for two minutes and then closes the browser, and use-after-free will repro. If there is no repro after two minutes, you can continue to wait for a few minutes or increase the number of browsers.When testing locally, it can usually be reproduced after two minutes.

notes:
-   During testing, I accidentally reproduced another use-after-free error in non-headless mode, but it has not been reproduced since then. After checking the logs, it seems to be related to DevTools and not related to Puppeteer. I submitted it together, but I am not sure if it is helpful



Analysis:
bisects:
This issue exists in versions after this CL:：
https://chromium-review.googlesource.com/c/chromium/src/+/4010556
```
diff --git a/content/browser/devtools/service_worker_devtools_agent_host.cc b/content/browser/devtools/service_worker_devtools_agent_host.cc
index 2cf2596..47d2d16 100644
--- a/content/browser/devtools/service_worker_devtools_agent_host.cc
+++ b/content/browser/devtools/service_worker_devtools_agent_host.cc
 void ServiceWorkerDevToolsAgentHost::RenderProcessHostDestroyed(
     RenderProcessHost* host) {
+  if (context_wrapper_->process_manager()->IsShutdown())
+    ForceDetachAllSessions();
   GetRendererChannel()->SetRenderer(mojo::NullRemote(), mojo::NullReceiver(),
                                     ChildProcessHost::kInvalidUniqueID);
   process_observation_.Reset();
```

The reference count of DevToolsAgentHostImpl increases and decreases when attaching and detaching sessions. Therefore, sessions_[a] should be empty when the reference count of DevToolsAgentHostImpl is 1.

However, under certain edge conditions, when the reference count of DevToolsAgentHostImpl is 1, sessions_ is not empty. When it reaches [b], the reference count decreases, and when out of scope of |ForceDetachAllSessions| , |DevToolsAgentHostImpl| is released, causing a use-after-free.

Initially, I suspected that agent_host_ in the client was not the same object as this, but debugging showed that they were the same object before the use-after-free error occurred. I have not yet found the root cause, but I will provide further information if I discover anything.

void DevToolsAgentHostImpl::ForceDetachAllSessions() {
  scoped_refptr<DevToolsAgentHostImpl> protect(this); //refcount=2
  while (!sessions_.empty()) {    [a]
    DevToolsAgentHostClient* client = (*sessions_.begin())->GetClient();
    DetachClient(client);
    client->AgentHostClosed(this);[b] //refcount=1
  }
}  //refcount=0
https://source.chromium.org/chromium/chromium/src/+/main:content/browser/devtools/devtools_agent_host_impl.cc;drc=79bb66cf71ad8038b36faa4bf742a42c0a300a0b;l=360


## Attachments

- [sw.js](attachments/sw.js) (text/plain, 4.8 KB)
- [test.js](attachments/test.js) (text/plain, 1.1 KB)
- [ws-poc.py](attachments/ws-poc.py) (text/plain, 1.6 KB)
- [headless-asan.log](attachments/headless-asan.log) (text/plain, 39.3 KB)
- [without-headless-asan.log](attachments/without-headless-asan.log) (text/plain, 59.0 KB)

## Timeline

### [Deleted User] (2023-03-14)

[Empty comment from Monorail migration]

### ts...@chromium.org (2023-03-14)

Based on the quality of the report and the reporter's bisect, this goes back to M109, assigning to CL owner.

[Monorail components: Platform>DevTools]

### [Deleted User] (2023-03-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-15)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### em...@gmail.com (2023-03-23)

is there any active progress? 

### [Deleted User] (2023-03-28)

caseq: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2023-03-28)

+@dgozman for review context

### gi...@appspot.gserviceaccount.com (2023-03-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8c4aee2a90d08535cfb1bf0a59e00cae956b1762

commit 8c4aee2a90d08535cfb1bf0a59e00cae956b1762
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Wed Mar 29 19:44:42 2023

Retain DevToolsAgentHost after ForceDetachAllSessions()

Bug: 1424337
Change-Id: Ie0ebe2a49ffbd2356b896c39446b93e09cd81f5a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4378100
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1123772}

[modify] https://crrev.com/8c4aee2a90d08535cfb1bf0a59e00cae956b1762/content/browser/devtools/web_contents_devtools_agent_host.cc
[modify] https://crrev.com/8c4aee2a90d08535cfb1bf0a59e00cae956b1762/content/browser/devtools/worker_devtools_agent_host.cc
[modify] https://crrev.com/8c4aee2a90d08535cfb1bf0a59e00cae956b1762/content/browser/devtools/auction_worklet_devtools_agent_host.cc
[modify] https://crrev.com/8c4aee2a90d08535cfb1bf0a59e00cae956b1762/content/browser/devtools/service_worker_devtools_agent_host.cc
[modify] https://crrev.com/8c4aee2a90d08535cfb1bf0a59e00cae956b1762/content/browser/devtools/render_frame_devtools_agent_host.cc
[modify] https://crrev.com/8c4aee2a90d08535cfb1bf0a59e00cae956b1762/content/browser/devtools/devtools_agent_host_impl.cc
[modify] https://crrev.com/8c4aee2a90d08535cfb1bf0a59e00cae956b1762/content/browser/devtools/devtools_agent_host_impl.h


### ca...@chromium.org (2023-03-29)

The above is a speculative fix for the problem -- unfortunately, I haven't been able to reproduce this locally with the provided script. @emilykim8708, may I ask you to  verify if this fixes the problem?

### em...@gmail.com (2023-03-29)

I confirmed that the issue has been fixed.
tested version:Chromium 113.0.5653.0(with patch:8c4aee2a90d08535cfb1bf0a59e00cae956b1762)

### [Deleted User] (2023-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-30)

Requesting merge to extended stable M110 because latest trunk commit (1123772) appears to be after extended stable branch point (1084008).

Requesting merge to other stable M111 because latest trunk commit (1123772) appears to be after other stable branch point (1097615).

Requesting merge to stable M112 because latest trunk commit (1123772) appears to be after stable branch point (1109224).

Requesting merge to dev M113 because latest trunk commit (1123772) appears to be after dev branch point (1121455).

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-30)

Merge approved: your change passed merge requirements and is auto-approved for M113. Please go ahead and merge the CL to branch 5672 (refs/branch-heads/5672) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-30)

Merge review required: M112 has already been cut for stable release.

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
Owners: govind (Android), govind (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-30)

Merge review required: M111 is already shipping to stable.

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
Owners: harrysouders (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-30)

Merge review required: M110 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), ceb (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-03-31)

Since this fix was landed not quite fully 48 hours ago, let's let this continue to bake over the weekend. 
Will revisit for merge approval early next week. RC for Stable/112 has already been cut for release on Tuesday. No further planned releases of M110/extended and M111/Stable. 


### pb...@google.com (2023-04-03)

Your merge has been approved for M113 Branch, please help complete your merges asap (before 3pm PST) today, so the change can be included in this week's RC build for dev/beta releases.`

We would like to get the changes as much beta time as possible, so please complete your merges asap to M113 branch(go/chrome-branches).


### [Deleted User] (2023-04-03)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-04-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/473f65d9adb188efd7e0eb4ad648428c7a474696

commit 473f65d9adb188efd7e0eb4ad648428c7a474696
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Mon Apr 03 20:30:52 2023

[m113] Retain DevToolsAgentHost after ForceDetachAllSessions()

(cherry picked from commit 8c4aee2a90d08535cfb1bf0a59e00cae956b1762)

Bug: 1424337
Change-Id: Ie0ebe2a49ffbd2356b896c39446b93e09cd81f5a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4378100
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1123772}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4395370
Auto-Submit: Andrey Kosyakov <caseq@chromium.org>
Commit-Queue: Dmitry Gozman <dgozman@chromium.org>
Cr-Commit-Position: refs/branch-heads/5672@{#227}
Cr-Branched-From: 5f2a72468eda1eb945b3b5a2298b5d1cd678521e-refs/heads/main@{#1121455}

[modify] https://crrev.com/473f65d9adb188efd7e0eb4ad648428c7a474696/content/browser/devtools/web_contents_devtools_agent_host.cc
[modify] https://crrev.com/473f65d9adb188efd7e0eb4ad648428c7a474696/content/browser/devtools/worker_devtools_agent_host.cc
[modify] https://crrev.com/473f65d9adb188efd7e0eb4ad648428c7a474696/content/browser/devtools/auction_worklet_devtools_agent_host.cc
[modify] https://crrev.com/473f65d9adb188efd7e0eb4ad648428c7a474696/content/browser/devtools/service_worker_devtools_agent_host.cc
[modify] https://crrev.com/473f65d9adb188efd7e0eb4ad648428c7a474696/content/browser/devtools/render_frame_devtools_agent_host.cc
[modify] https://crrev.com/473f65d9adb188efd7e0eb4ad648428c7a474696/content/browser/devtools/devtools_agent_host_impl.cc
[modify] https://crrev.com/473f65d9adb188efd7e0eb4ad648428c7a474696/content/browser/devtools/devtools_agent_host_impl.h


### [Deleted User] (2023-04-03)

LTS Milestone M108

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-04-04)

[Empty comment from Monorail migration]

### am...@google.com (2023-04-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-04-05)

Congratulations, Emily Kim! The VRP Panel has decided to award you $2,000 for this report of a heavily mitigated security bug + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us! 

### rz...@google.com (2023-04-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-06)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-04-06)

1. https://crrev.com/c/4396055
2. Low, skipped the change on RenderProcessHostDestroyed because the changed code isn't present in 108
3. 113
4. Yes

### am...@chromium.org (2023-04-08)

M112 merge approved, please merge this fix to branch 5615 at your earliest convenience so this fix can be included in the next M112/Stable security respin 

### am...@google.com (2023-04-08)

[Empty comment from Monorail migration]

### sr...@google.com (2023-04-12)

Please complete merge to M112 branch asap, so they can be included in the planned re-spin ( RC cut this friday)

### sr...@google.com (2023-04-12)

CP in dryrun CQ - https://chromium-review.googlesource.com/c/chromium/src/+/4420271

### gi...@appspot.gserviceaccount.com (2023-04-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f098ff0d123079690e53e64877bc2d814214b0f3

commit f098ff0d123079690e53e64877bc2d814214b0f3
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Thu Apr 13 03:55:24 2023

[m112] Retain DevToolsAgentHost after ForceDetachAllSessions()

(cherry picked from commit 8c4aee2a90d08535cfb1bf0a59e00cae956b1762)

Bug: 1424337
Change-Id: Ie0ebe2a49ffbd2356b896c39446b93e09cd81f5a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4378100
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1123772}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4420271
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Cr-Commit-Position: refs/branch-heads/5615@{#1244}
Cr-Branched-From: 9c6408ef696e83a9936b82bbead3d41c93c82ee4-refs/heads/main@{#1109224}

[modify] https://crrev.com/f098ff0d123079690e53e64877bc2d814214b0f3/content/browser/devtools/web_contents_devtools_agent_host.cc
[modify] https://crrev.com/f098ff0d123079690e53e64877bc2d814214b0f3/content/browser/devtools/worker_devtools_agent_host.cc
[modify] https://crrev.com/f098ff0d123079690e53e64877bc2d814214b0f3/content/browser/devtools/auction_worklet_devtools_agent_host.cc
[modify] https://crrev.com/f098ff0d123079690e53e64877bc2d814214b0f3/content/browser/devtools/service_worker_devtools_agent_host.cc
[modify] https://crrev.com/f098ff0d123079690e53e64877bc2d814214b0f3/content/browser/devtools/render_frame_devtools_agent_host.cc
[modify] https://crrev.com/f098ff0d123079690e53e64877bc2d814214b0f3/content/browser/devtools/devtools_agent_host_impl.cc
[modify] https://crrev.com/f098ff0d123079690e53e64877bc2d814214b0f3/content/browser/devtools/devtools_agent_host_impl.h


### gm...@google.com (2023-04-13)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-04-17)

[Empty comment from Monorail migration]

### am...@google.com (2023-04-17)

[Empty comment from Monorail migration]

### pg...@google.com (2023-04-19)

[Empty comment from Monorail migration]

### gm...@google.com (2023-04-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-04-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c85b2a472dde48b29a8cc15e2f67d9cda8df1fe8

commit c85b2a472dde48b29a8cc15e2f67d9cda8df1fe8
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Wed Apr 26 12:09:02 2023

[M108-LTS] Retain DevToolsAgentHost after ForceDetachAllSessions()

M108 merge issues:
  content/browser/devtools/service_worker_devtools_agent_host.cc:
      Changed code in RenderProcessHostDestroyed() doesn't exist in 108

(cherry picked from commit 8c4aee2a90d08535cfb1bf0a59e00cae956b1762)

Bug: 1424337
Change-Id: Ie0ebe2a49ffbd2356b896c39446b93e09cd81f5a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4378100
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1123772}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4396055
Owners-Override: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/5359@{#1450}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/c85b2a472dde48b29a8cc15e2f67d9cda8df1fe8/content/browser/devtools/web_contents_devtools_agent_host.cc
[modify] https://crrev.com/c85b2a472dde48b29a8cc15e2f67d9cda8df1fe8/content/browser/devtools/worker_devtools_agent_host.cc
[modify] https://crrev.com/c85b2a472dde48b29a8cc15e2f67d9cda8df1fe8/content/browser/devtools/auction_worklet_devtools_agent_host.cc
[modify] https://crrev.com/c85b2a472dde48b29a8cc15e2f67d9cda8df1fe8/content/browser/devtools/render_frame_devtools_agent_host.cc
[modify] https://crrev.com/c85b2a472dde48b29a8cc15e2f67d9cda8df1fe8/content/browser/devtools/devtools_agent_host_impl.cc
[modify] https://crrev.com/c85b2a472dde48b29a8cc15e2f67d9cda8df1fe8/content/browser/devtools/devtools_agent_host_impl.h


### rz...@google.com (2023-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1424337?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063589)*
