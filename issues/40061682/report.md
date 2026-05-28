# Security: UAF in content::RenderFrameDevToolsAgentHost::RenderProcessExited

| Field | Value |
|-------|-------|
| **Issue ID** | [40061682](https://issues.chromium.org/issues/40061682) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Headless |
| **Platforms** | Android, Linux, Mac, Windows |
| **Reporter** | et...@gmail.com |
| **Assignee** | kv...@chromium.org |
| **Created** | 2022-11-10 |
| **Bounty** | $31,000.00 |

## Description

**VULNERABILITY DETAILS**  

This vulnerability was found by my fuzzer, I will do a vulnerability analysis as soon as possible, but I will submit a poc to you here first

**VERSION**  

Chrome Version: [109.0.5412.0] + [dev]  

Operating System: linux and unknown

**REPRODUCTION CASE**  

0. Note that this issue is currently only reproducible under \*\*--headless\*\*, but otherwise does not require any flag.

1. Download chromium with asan from here:  
   
   <https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-release-1069497.zip?generation=1668045906082534&alt=media>
2. Make sure testharness.js and poc.html are in the same directory, or modify poc.html to reference it with script
3. asan-linux-release-1069497/chrome-wrapper --headless poc.html

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan log

**CREDIT INFORMATION**  

Reporter credit: Nan Wang(@eternalsakura13) and Guang Gong of 360 Vulnerability Research Institute

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 25.8 KB)
- [testharness.js](attachments/testharness.js) (text/plain, 180.3 KB)
- [repro.mp4](attachments/repro.mp4) (video/mp4, 2.3 MB)
- [asan.txt](attachments/asan.txt) (text/plain, 25.8 KB)

## Timeline

### et...@gmail.com (2022-11-10)

asan log here

### [Deleted User] (2022-11-10)

[Empty comment from Monorail migration]

### et...@gmail.com (2022-11-10)

- poc
<script>
    let o1 = new Array(2**32-1);
    o1.fill(1.1);
</script>

I re-simplified the poc and confirmed that this uaf will be triggered as long as the render is crashed in a similar way as oom, so the simplest poc should be like this. At present, I can trigger the UAF on both linux and mac.

### et...@gmail.com (2022-11-10)

hello, I can confirm that the introduction commit of this vulnerability is（2days before）:
https://chromium-review.googlesource.com/c/chromium/src/+/4006837

From the UAF log, the root cause of this vulnerability is clear, I will not repeat.
Simply put, this commit incorrectly modifies the startup and shutdown logic of chrome headless.

### et...@gmail.com (2022-11-10)

I would like to understand if `--headless` is part of chrome's security model?
Because as far as I know this is a commonly used crawler parameter with a wide range of usage scenarios.

I have tested that this vulnerability exists on windows/linux/mac and is a generic problem :)

### wf...@chromium.org (2022-11-10)

Thanks for your report and your bisect. I'll add some headless folks while I work to reproduce. Seems any abnormal renderer termination will cause this crash in browser, which isn't ideal.

[Monorail components: Internals>Headless]

### [Deleted User] (2022-11-10)

[Empty comment from Monorail migration]

### kv...@chromium.org (2022-11-10)

[Empty comment from Monorail migration]

### kv...@chromium.org (2022-11-10)

The problem is with this line: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/devtools/render_frame_devtools_agent_host.cc;drc=5e124986e8b3eb701f630b95bd12f096a8418de4;l=612

|this| is destroyed while in NotifyCrashed(...); and the code is trying to update this.render_frame_crashed_

i'll submit a fix shortly.

### gi...@appspot.gserviceaccount.com (2022-11-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/749309138d2ebb5878b238f9aee15046fe7b3fcb

commit 749309138d2ebb5878b238f9aee15046fe7b3fcb
Author: Peter Kvitek <kvitekp@chromium.org>
Date: Fri Nov 11 01:17:50 2022

[headless] Added async callback option to Simple CDP protocol.

DevTools backend assumes that response and event handling is
asynchronous, and not respecting this assumption causes use after
free problems, see the associated bug.

This CL introduces async response/event callback option for
the Simple CDP client.

Drive by: Provide cleaner headless_shell shutdown routine.

Bug: 1382993
Change-Id: I14b37079f1b7488777ebcf20a808b3bfb9eb44c5
Cq-Include-Trybots: luci.chromium.try:linux-headless-shell-rel
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4021401
Commit-Queue: Peter Kvitek <kvitekp@chromium.org>
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1070102}

[modify] https://crrev.com/749309138d2ebb5878b238f9aee15046fe7b3fcb/headless/app/headless_shell.cc
[modify] https://crrev.com/749309138d2ebb5878b238f9aee15046fe7b3fcb/components/devtools/simple_devtools_protocol_client/simple_devtools_protocol_client.h
[modify] https://crrev.com/749309138d2ebb5878b238f9aee15046fe7b3fcb/components/devtools/simple_devtools_protocol_client/simple_devtools_protocol_client.cc


### et...@gmail.com (2022-11-11)

thanks for the quick fix ：）

### et...@gmail.com (2022-11-11)

Can you mark it as fixed?

### wf...@chromium.org (2022-11-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-11)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-12)

Requesting merge to dev M109 because latest trunk commit (1070102) appears to be after dev branch point (1070088).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-12)

Merge approved: your change passed merge requirements and is auto-approved for M109. Please go ahead and merge the CL to branch 5414 (refs/branch-heads/5414) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kv...@chromium.org (2022-11-14)

The original fix works, however it is sub-optimal and also has a potential use-after-move.  CL https://crrev.com/c/4026625 addresses both issues and is currently under review.  The plan is to cherry pick both changes as soon as the follow up change lands.

### gi...@appspot.gserviceaccount.com (2022-11-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3acd45eb60c0635754573b34c75977f0de943138

commit 3acd45eb60c0635754573b34c75977f0de943138
Author: Peter Kvitek <kvitekp@chromium.org>
Date: Mon Nov 14 23:33:21 2022

[headless] Improved Simple CDP Client callback handling.

Previous implementation of the asynchronous callbacks posted a task
for each result and event which is suboptimal. This CL changes logic
so that all the result and event callbacks are called from a single
task posted on the browser UI thread.

Drive by: fixed occasional use-after-move in event handler.

Bug: 1382993
Change-Id: I031044a5bfdaab2b88455d1649f53e4adf053140
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4026625
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Commit-Queue: Peter Kvitek <kvitekp@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1071300}

[modify] https://crrev.com/3acd45eb60c0635754573b34c75977f0de943138/components/devtools/simple_devtools_protocol_client/DEPS
[modify] https://crrev.com/3acd45eb60c0635754573b34c75977f0de943138/headless/app/headless_shell.cc
[modify] https://crrev.com/3acd45eb60c0635754573b34c75977f0de943138/components/devtools/simple_devtools_protocol_client/BUILD.gn
[modify] https://crrev.com/3acd45eb60c0635754573b34c75977f0de943138/components/devtools/simple_devtools_protocol_client/simple_devtools_protocol_client.h
[modify] https://crrev.com/3acd45eb60c0635754573b34c75977f0de943138/components/devtools/simple_devtools_protocol_client/simple_devtools_protocol_client_unittest.cc
[modify] https://crrev.com/3acd45eb60c0635754573b34c75977f0de943138/components/devtools/simple_devtools_protocol_client/simple_devtools_protocol_client.cc


### gi...@appspot.gserviceaccount.com (2022-11-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fd4c293c8eba667753e4ab8fc862103a46dacf71

commit fd4c293c8eba667753e4ab8fc862103a46dacf71
Author: Peter Kvitek <kvitekp@chromium.org>
Date: Tue Nov 15 18:42:22 2022

[headless] Added async callback option to Simple CDP protocol.

DevTools backend assumes that response and event handling is
asynchronous, and not respecting this assumption causes use after
free problems, see the associated bug.

This CL introduces async response/event callback option for
the Simple CDP client.

Drive by: Provide cleaner headless_shell shutdown routine.

(cherry picked from commit 749309138d2ebb5878b238f9aee15046fe7b3fcb)

Bug: 1382993
Change-Id: I14b37079f1b7488777ebcf20a808b3bfb9eb44c5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4021401
Commit-Queue: Peter Kvitek <kvitekp@chromium.org>
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1070102}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4027032
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Cr-Commit-Position: refs/branch-heads/5414@{#47}
Cr-Branched-From: 4417ee59d7bf6df7a9c9ea28f7722d2ee6203413-refs/heads/main@{#1070088}

[modify] https://crrev.com/fd4c293c8eba667753e4ab8fc862103a46dacf71/headless/app/headless_shell.cc
[modify] https://crrev.com/fd4c293c8eba667753e4ab8fc862103a46dacf71/components/devtools/simple_devtools_protocol_client/simple_devtools_protocol_client.h
[modify] https://crrev.com/fd4c293c8eba667753e4ab8fc862103a46dacf71/components/devtools/simple_devtools_protocol_client/simple_devtools_protocol_client.cc


### kv...@chromium.org (2022-11-16)

Requesting merge for https://crrev.com/c/4026625.

While the previous fix fixes the main issue it is sub-optimal and introduces a use-after-move. The follow up CL addresses both issues.

### [Deleted User] (2022-11-16)

Merge review required: a commit with DEPS changes was detected.

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
Owners: govind (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kv...@chromium.org (2022-11-16)

1. The change addresses a use-after-move regression introduced by the previous fix (https://crrev.com/c/4021401)
2. Change to merge: https://crrev.com/c/4026625
3. The change has been released and tested on win and mac canary 110.0.5422.0
4. No, this is not a new feature.
5. N/A
6. No manual testing required, component_unittests and headless_browsertests targets provide adequate test coverage, including the use-after-move issue that is being fixed.


### kv...@chromium.org (2022-11-16)

> Merge review required: a commit with DEPS changes was detected.
This DEPS is related to the new unit tests dependency on "+content/public/test" which is necessary because they now test asynchronous callback handling and thus require content::BrowserTaskEnvironment.

### am...@google.com (2022-11-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-18)

Congratulations, Nan Wang and Guang Gong -- nice work! The VRP Panel has decided to award you $30,000 for this report +$1,000 bisect bonus. Thank you for your efforts discovering and reporting this issue to us! 

### et...@gmail.com (2022-11-18)

Thank you :)

### am...@chromium.org (2022-11-18)

Hi Peter, thank you for updating and taking the time to work on a comprehensive fix can catching the move after use introduced earlier! 
Please merge the fix landed in https://ccrev.com/c/4026625 M109/branch 5414 at your earliest availability. Thank you! 

### gi...@appspot.gserviceaccount.com (2022-11-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c2d40e29fca29aecc25ef1171d100ea754f0d44a

commit c2d40e29fca29aecc25ef1171d100ea754f0d44a
Author: Peter Kvitek <kvitekp@chromium.org>
Date: Fri Nov 18 22:42:21 2022

[headless/m109] Improved Simple CDP Client callback handling.

Previous implementation of the asynchronous callbacks posted a task
for each result and event which is suboptimal. This CL changes logic
so that all the result and event callbacks are called from a single
task posted on the browser UI thread.

Drive by: fixed occasional use-after-move in event handler.

(cherry picked from commit 3acd45eb60c0635754573b34c75977f0de943138)

Bug: 1382993
Change-Id: I031044a5bfdaab2b88455d1649f53e4adf053140
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4026625
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Commit-Queue: Peter Kvitek <kvitekp@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1071300}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4035384
Reviewed-by: Scott Violet <sky@chromium.org>
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/branch-heads/5414@{#142}
Cr-Branched-From: 4417ee59d7bf6df7a9c9ea28f7722d2ee6203413-refs/heads/main@{#1070088}

[modify] https://crrev.com/c2d40e29fca29aecc25ef1171d100ea754f0d44a/components/devtools/simple_devtools_protocol_client/DEPS
[modify] https://crrev.com/c2d40e29fca29aecc25ef1171d100ea754f0d44a/headless/app/headless_shell.cc
[modify] https://crrev.com/c2d40e29fca29aecc25ef1171d100ea754f0d44a/components/devtools/simple_devtools_protocol_client/simple_devtools_protocol_client.h
[modify] https://crrev.com/c2d40e29fca29aecc25ef1171d100ea754f0d44a/components/devtools/simple_devtools_protocol_client/BUILD.gn
[modify] https://crrev.com/c2d40e29fca29aecc25ef1171d100ea754f0d44a/components/devtools/simple_devtools_protocol_client/simple_devtools_protocol_client_unittest.cc
[modify] https://crrev.com/c2d40e29fca29aecc25ef1171d100ea754f0d44a/components/devtools/simple_devtools_protocol_client/simple_devtools_protocol_client.cc


### am...@google.com (2022-11-19)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-11-21)

already merged to 109

### [Deleted User] (2023-02-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-02-20)

Hello Nan Wang, we consider attachments/POCs included with reports to be an integral part of the report (https://g.co/chrome/vrp), so I've undeleted them. 

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1382993?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061682)*
