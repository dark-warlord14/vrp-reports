# Security: Code Injection in WebUI page leading to sandbox escape

| Field | Value |
|-------|-------|
| **Issue ID** | [40060348](https://issues.chromium.org/issues/40060348) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools, Platform>Extensions |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | jt...@gmail.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2022-07-21 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

When a tab which is attached by extension debugger API starts to navigate to another url, it calls RenderFrameDevToolsAgentHost::OnNavigationRequestWillBeSent to check if the debugger is still allowed to attach to the new url [1]. If the new url belongs to webui, the debugging session would be terminated and an onDetach event would be fired. However, the extension is able to re-attach the tab in the onDetach event listener immediately and has a chance to inject JavaScript code into the webui page. This leads to sandbox escape with the help of some powerful functions in webui pages.

When attaching to a tab, it calls DebuggerAttachFunction::Run and then goes to ExtensionMayAttachToWebContents. This function calls ExtensionMayAttachToURL to check permission, using web\_contents.GetLastCommittedURL() as parameter [2]. If the navigation has not been committed yet, GetLastCommittedURL() would return the original url. So \*I think\* the root cause here is the check for attaching happens before navigation is committed, which result in the check is performed on the wrong url.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/devtools/render_frame_devtools_agent_host.cc;l=640;drc=610603f89f0dd4da794848e4f8670a179efbcf38>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/extensions/api/debugger/debugger_api.cc;l=216;drc=6aea6e2a8a3b9a0ca7e8b60190acd9542593cafb>

**VERSION**  

Chrome Version: 103.0.5060.134 stable + dev

**REPRODUCTION CASE**  

On windows 10 platform:

1. Download the attached files to <dir>
2. Setup HTTPServer  
   
   cd path/to/dir && python -m SimpleHTTPServer 8000
3. Run  
   
   out/release/chrome --load-extension=path/to/dir

Wait about 8 seconds and the executable should be started. Note that the calc.exe is calculator program which is copied from windows 10 C:\Windows\System32\calc.exe, and it would be executed on your local machine. If you do not trust the file, please replace it with your own version or run the poc in virtual machine.

## Attachments

- [manifest.json](attachments/manifest.json) (text/plain, 181 B)
- [page.html](attachments/page.html) (text/plain, 163 B)
- [bg.js](attachments/bg.js) (text/plain, 1.2 KB)
- [calc.exe](attachments/calc.exe) (application/octet-stream, 27.0 KB)

## Timeline

### [Deleted User] (2022-07-21)

[Empty comment from Monorail migration]

### rs...@chromium.org (2022-07-21)

Thanks for the report. I was able to repro most of this on macOS. But the specific attack to launch a downloaded executable does not work on macOS because the downloaded file has the quarantine bit set, which prevents it from actually running the executable (but seeing the OS prompt does confirm that it can try to launch the downloaded file).

[Monorail components: Platform>DevTools Platform>Extensions]

### [Deleted User] (2022-07-21)

[Empty comment from Monorail migration]

### ca...@chromium.org (2022-07-22)

Danil, would you be interested in this one by a chance?

### [Deleted User] (2022-07-22)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-07-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ed2f22edcc37054ba176154179a3fce8521da0bb

commit ed2f22edcc37054ba176154179a3fce8521da0bb
Author: Danil Somsikov <dsv@chromium.org>
Date: Fri Jul 22 17:56:57 2022

Also check pending navigation entry ExtensionMayAttachToWebContents

Bug: 1346236
Change-Id: I2634a7bee919d4b9f4b5c70c699b96e3c02a1f42
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3780487
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
Auto-Submit: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Devlin Cronin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1027321}

[modify] https://crrev.com/ed2f22edcc37054ba176154179a3fce8521da0bb/chrome/browser/extensions/api/debugger/debugger_api.cc
[modify] https://crrev.com/ed2f22edcc37054ba176154179a3fce8521da0bb/chrome/test/data/extensions/api_test/debugger/background.js


### ds...@chromium.org (2022-07-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-26)

Requesting merge to beta M104 because latest trunk commit (1027321) appears to be after beta branch point (1012729).

Requesting merge to dev M105 because latest trunk commit (1027321) appears to be after dev branch point (1027018).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-26)

Merge approved: your change passed merge requirements and is auto-approved for M105. Please go ahead and merge the CL to branch 5195 (refs/branch-heads/5195) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), harrysouders (iOS),  matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-26)

Merge review required: M104 has already been cut for stable release.

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
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2022-07-27)

[Bulk Edit] We are planning to cut M105 Dev RC build later this afternoon around 2Pm PST and would request to get the change merged to M105 Branch asap so that it would be part of tomorrow's Dev release.

### gi...@appspot.gserviceaccount.com (2022-07-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/95b3d8e50de42a15d39528f154c85a8335a4088d

commit 95b3d8e50de42a15d39528f154c85a8335a4088d
Author: Danil Somsikov <dsv@chromium.org>
Date: Fri Jul 29 12:55:40 2022

[M104] Also check pending navigation entry ExtensionMayAttachToWebContents

(cherry picked from commit ed2f22edcc37054ba176154179a3fce8521da0bb)

Bug: 1346236
Change-Id: I2634a7bee919d4b9f4b5c70c699b96e3c02a1f42
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3780487
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
Auto-Submit: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Devlin Cronin <rdevlin.cronin@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1027321}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3789770
Cr-Commit-Position: refs/branch-heads/5195@{#109}
Cr-Branched-From: 7aa3f074a7907975b001346cc0288d0214af8451-refs/heads/main@{#1027018}

[modify] https://crrev.com/95b3d8e50de42a15d39528f154c85a8335a4088d/chrome/browser/extensions/api/debugger/debugger_api.cc
[modify] https://crrev.com/95b3d8e50de42a15d39528f154c85a8335a4088d/chrome/test/data/extensions/api_test/debugger/background.js


### [Deleted User] (2022-07-29)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-07-29)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-01)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-08-01)

1. Just https://crrev.com/c/3793834
2. Low, only include conflicts
3. 104
4. Yes

### am...@chromium.org (2022-08-04)

M104 merge approved, please merge this fix to branch 5112 at your earliest convenience -- thanks! 

### gi...@appspot.gserviceaccount.com (2022-08-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4a1fbcac80618ce4e8cf55bd812d827a36ead2cd

commit 4a1fbcac80618ce4e8cf55bd812d827a36ead2cd
Author: Danil Somsikov <dsv@chromium.org>
Date: Mon Aug 08 08:32:54 2022

[M104] Also check pending navigation entry ExtensionMayAttachToWebContents

(cherry picked from commit ed2f22edcc37054ba176154179a3fce8521da0bb)

Bug: 1346236
Change-Id: I2634a7bee919d4b9f4b5c70c699b96e3c02a1f42
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3780487
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
Auto-Submit: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Devlin Cronin <rdevlin.cronin@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1027321}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3810555
Cr-Commit-Position: refs/branch-heads/5112@{#1413}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[modify] https://crrev.com/4a1fbcac80618ce4e8cf55bd812d827a36ead2cd/chrome/browser/extensions/api/debugger/debugger_api.cc
[modify] https://crrev.com/4a1fbcac80618ce4e8cf55bd812d827a36ead2cd/chrome/test/data/extensions/api_test/debugger/background.js


### rz...@google.com (2022-08-09)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-09)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-09)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-08-09)

1. Just https://crrev.com/c/3816932
2. Low, only include conflicts
3. 104
4. Yes

### gm...@google.com (2022-08-11)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/52b5a4bd7df3ad5ca25417aa076a70a2f4e8e665

commit 52b5a4bd7df3ad5ca25417aa076a70a2f4e8e665
Author: Danil Somsikov <dsv@chromium.org>
Date: Fri Aug 12 15:53:13 2022

[M102-LTS] Also check pending navigation entry ExtensionMayAttachToWebContents

M102 merge issues:
  chrome/browser/extensions/api/debugger/debugger_api.cc:
    include conflicts

(cherry picked from commit ed2f22edcc37054ba176154179a3fce8521da0bb)

Bug: 1346236
Change-Id: I2634a7bee919d4b9f4b5c70c699b96e3c02a1f42
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3780487
Auto-Submit: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Devlin Cronin <rdevlin.cronin@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1027321}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3816932
Owners-Override: Oleh Lamzin <lamzin@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1300}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/52b5a4bd7df3ad5ca25417aa076a70a2f4e8e665/chrome/browser/extensions/api/debugger/debugger_api.cc
[modify] https://crrev.com/52b5a4bd7df3ad5ca25417aa076a70a2f4e8e665/chrome/test/data/extensions/api_test/debugger/background.js


### rz...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/aed84d50115981de94eaa75d8697dd65d5c79ae2

commit aed84d50115981de94eaa75d8697dd65d5c79ae2
Author: Danil Somsikov <dsv@chromium.org>
Date: Fri Aug 12 16:35:33 2022

[M96-LTS] Also check pending navigation entry ExtensionMayAttachToWebContents

M96 merge issues:
  chrome/browser/extensions/api/debugger/debugger_api.cc:
    include conflicts

(cherry picked from commit ed2f22edcc37054ba176154179a3fce8521da0bb)

Bug: 1346236
Change-Id: I2634a7bee919d4b9f4b5c70c699b96e3c02a1f42
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3780487
Auto-Submit: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Devlin Cronin <rdevlin.cronin@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1027321}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3793834
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Owners-Override: Oleh Lamzin <lamzin@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1682}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/aed84d50115981de94eaa75d8697dd65d5c79ae2/chrome/browser/extensions/api/debugger/debugger_api.cc
[modify] https://crrev.com/aed84d50115981de94eaa75d8697dd65d5c79ae2/chrome/test/data/extensions/api_test/debugger/background.js


### rz...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-16)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-16)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-17)

Congratulations, Rong Jian! The VRP Panel has decided to award you $5,000 for this report. Thank you for reporting this issue to us -- nice work! 

### am...@google.com (2022-08-19)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1346236?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>DevTools, Platform>Extensions]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060348)*
