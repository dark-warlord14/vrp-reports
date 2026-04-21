# Security: Possible for extension to escape sandbox via devtools_page and intentionally crashed renderer

| Field | Value |
|-------|-------|
| **Issue ID** | [40053357](https://issues.chromium.org/issues/40053357) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2020-09-15 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

When the debugger is attached to a target and that target crashes, any pending commands will be re-run once the target has been loaded again.

Using this behavior, an extension with a devtools\_page entry can crash a target page via an (indirect) Runtime.evaluate call, then navigate that page to a privileged location. When the target page loads after the crash, the Runtime.evaluate call will be re-run, though this time (effectively) within the context of the privileged page. By running code within the context of chrome://downloads, an extension can open an executable it downloads and escape the sandbox.

Because an extension can currently open the devtools by itself (using the behavior described in <https://crbug.com/chromium/1115460>), this allows an extension to escape the sandbox without any user interaction post extension install.

**VERSION**  

Chrome Version: Tested on 85.0.4183.102 (stable) and 87.0.4263.3 (canary)  

Operating System: Windows 10, version 2004

**REPRODUCTION CASE**

1. Install the attached extension.
2. Wait about 5 seconds.
3. The target executable (in this case, Process Explorer) should be started.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [background.js](attachments/background.js) (text/plain, 7.2 KB)
- [devtools_page.html](attachments/devtools_page.html) (text/plain, 107 B)
- [devtools_page.js](attachments/devtools_page.js) (text/plain, 3.2 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 280 B)

## Timeline

### de...@gmail.com (2020-09-15)

The demonstration extension works because of the following:

Firstly, it's that when debugging a page, if that page crashes, any pending debugging commands will be re-sent once the page has been loaded again:

https://source.chromium.org/chromium/chromium/src/+/master:content/browser/devtools/devtools_session.cc;l=204;drc=dda5b70c005af869ec6f5850bd46d83e8008bff5

In this case, the devtools_page entry defined by the extension calls chrome.devtools.inspectedWindow.eval, which ultimately results in a call to Runtime.evaluate. The target page is intentionally crashed during that call, meaning that whenever the page is loaded, the command will be re-sent.

By using that behavior, the extension can call Runtime.evaluate (indirectly, via chrome.devtools.inspectedWindow.eval) on a non-privileged page. The page will crash during the call and the extension can then navigate the target to a privileged location (chrome://downloads/).

When the privileged page loads, the Runtime.evaluate command will be re-sent and run again.

Note that for the command to be re-sent, the debugger needs to remain attached. That's true for the devtools (since it can attach to any page), but it wouldn't be true for pages attached using the chrome.debugger API (since extensions can't attach to privileged pages).

Also, it's important to note that once the debugged page has been navigated to chrome://downloads/, any extensions embedded within the devtools will be disabled. The Runtime.evaluate call is re-run at a lower level, however, so it doesn't matter whether embedded extensions are disabled.

A complicating factor in the behavior described above is that the debugging command is re-sent when the navigation to the privileged page is initiated. That means that the command will be run before the navigation to the privileged page has committed.

In practice, however, that's not a problem.

When the navigation to the privileged page is initiated, a new renderer process will be created. When the devtools session is reattached, a default context will be initialized:

https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/core/inspector/main_thread_debugger.cc;l=301;drc=52bc92da6df065ff12ee81563e23fde2e8db94f9

The Runtime.evaluate code then runs in that context.

Additionally, code run via chrome.devtools.inspectedWindow.eval has access to the devtools command line API functions. One of those functions is debug. That function will cause the debugger to break when a specific function is called. Also, it accepts a condition argument and the debugger will only break if the condition evaluates to true.

Because that function works across contexts within a renderer, it means that calling debug from within the default context that's initialized will affect any other contexts created within that renderer process (e.g. the context for the privileged page).

Therefore, what the demonstration extension does is call debug with addEventListener and a condition argument that contains some necessary code. When the chrome://downloads/ page loads, it will call addEventListener repeatedly. The condition statement passed to debug will be evaluated to determine whether the debugger should break. In this case, the condition statement opens a file that was downloaded.

### li...@chromium.org (2020-09-15)

Setting as medium severity because it requires an extension install, but no user interaction after that. It does, however, require the debugger permission and devtools_page entry, so those are further potential mitigating factors. Adding DevTools team to take a look.

[Monorail components: Platform>DevTools]

### [Deleted User] (2020-09-16)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-09-16)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-09-29)

caseq: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-14)

caseq: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### ca...@chromium.org (2020-12-08)

[Empty comment from Monorail migration]

### ca...@chromium.org (2020-12-12)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9e73e9768d7bc7fca41818f323a0bd6cf06beb82

commit 9e73e9768d7bc7fca41818f323a0bd6cf06beb82
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Mon Dec 14 21:32:28 2020

Discard pending commands once target is reloaded after crash

Bug: 1128206
Change-Id: I7bc10beb585f07b6f49e61faae9cd8ab35eaa5b7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2587606
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/heads/master@{#836789}

[modify] https://crrev.com/9e73e9768d7bc7fca41818f323a0bd6cf06beb82/content/browser/devtools/devtools_session.h
[modify] https://crrev.com/9e73e9768d7bc7fca41818f323a0bd6cf06beb82/content/browser/devtools/render_frame_devtools_agent_host.cc
[modify] https://crrev.com/9e73e9768d7bc7fca41818f323a0bd6cf06beb82/content/browser/devtools/protocol/devtools_protocol_browsertest.cc
[modify] https://crrev.com/9e73e9768d7bc7fca41818f323a0bd6cf06beb82/content/browser/devtools/protocol/devtools_protocol_test_support.cc
[modify] https://crrev.com/9e73e9768d7bc7fca41818f323a0bd6cf06beb82/content/browser/devtools/devtools_session.cc


### ad...@google.com (2020-12-21)

caseq@ is https://crbug.com/chromium/1128206#c11 a complete fix? If so, could you mark this bug as Fixed so that Sheriffbot initiates merge proceedings.

### ca...@chromium.org (2020-12-21)

This is a sufficient fix for the current exploit technique. I was keeping this open as I'm working on a more generic and future-proof solution, which should also take care of https://crbug.com/chromium/1101897. We can close this one if you want this merged.

### [Deleted User] (2020-12-22)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-22)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-22)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M88. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-22)

This bug requires manual review: M88's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-12-30)

Approving merge to M88, branch 4324. Regarding https://crbug.com/chromium/1128206#c13 caseq@ yeah - thanks for closing this one - please feel free to raise another crbug for the more generic fix, or just track it using https://crbug.com/chromium/1101897.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/45916164be260ee4f36ecafb62f31e6251ddc88c

commit 45916164be260ee4f36ecafb62f31e6251ddc88c
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Sat Jan 09 07:39:42 2021

Discard pending commands once target is reloaded after crash

(cherry picked from commit 9e73e9768d7bc7fca41818f323a0bd6cf06beb82)

TBR: dgozman@chromium.org
Bug: 1128206
Change-Id: I7bc10beb585f07b6f49e61faae9cd8ab35eaa5b7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2587606
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#836789}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2619341
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/branch-heads/4324@{#1576}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/45916164be260ee4f36ecafb62f31e6251ddc88c/content/browser/devtools/devtools_session.h
[modify] https://crrev.com/45916164be260ee4f36ecafb62f31e6251ddc88c/content/browser/devtools/render_frame_devtools_agent_host.cc
[modify] https://crrev.com/45916164be260ee4f36ecafb62f31e6251ddc88c/content/browser/devtools/protocol/devtools_protocol_browsertest.cc
[modify] https://crrev.com/45916164be260ee4f36ecafb62f31e6251ddc88c/content/browser/devtools/protocol/devtools_protocol_test_support.cc
[modify] https://crrev.com/45916164be260ee4f36ecafb62f31e6251ddc88c/content/browser/devtools/devtools_session.cc


### ac...@chromium.org (2021-01-10)

[Empty comment from Monorail migration]

### ke...@google.com (2021-01-11)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c7ce80628782117c4044a8a4f20d50ff58bba7fb

commit c7ce80628782117c4044a8a4f20d50ff58bba7fb
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Mon Jan 11 18:15:56 2021

Discard pending commands once target is reloaded after crash

(cherry picked from commit 9e73e9768d7bc7fca41818f323a0bd6cf06beb82)

(cherry picked from commit 45916164be260ee4f36ecafb62f31e6251ddc88c)

TBR: dgozman@chromium.org
Bug: 1128206
Change-Id: I7bc10beb585f07b6f49e61faae9cd8ab35eaa5b7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2587606
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#836789}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2619341
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4324@{#1576}
Cr-Original-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2619971
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1514}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/c7ce80628782117c4044a8a4f20d50ff58bba7fb/content/browser/devtools/devtools_session.h
[modify] https://crrev.com/c7ce80628782117c4044a8a4f20d50ff58bba7fb/content/browser/devtools/render_frame_devtools_agent_host.cc
[modify] https://crrev.com/c7ce80628782117c4044a8a4f20d50ff58bba7fb/content/browser/devtools/protocol/devtools_protocol_browsertest.cc
[modify] https://crrev.com/c7ce80628782117c4044a8a4f20d50ff58bba7fb/content/browser/devtools/protocol/devtools_protocol_test_support.cc
[modify] https://crrev.com/c7ce80628782117c4044a8a4f20d50ff58bba7fb/content/browser/devtools/devtools_session.cc


### ad...@google.com (2021-01-13)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-14)

[Empty comment from Monorail migration]

### ja...@google.com (2021-01-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-19)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-01-21)

Congratulations, David! The VRP Panel has decided to award you $10,000 for this report. Nice job!

### am...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### am...@google.com (2021-02-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1128206?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053357)*
