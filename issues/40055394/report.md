# Security: UAF in TracingHandler

| Field | Value |
|-------|-------|
| **Issue ID** | [40055394](https://issues.chromium.org/issues/40055394) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools, Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2021-03-31 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

When the devtools is shown for an extension's background page, the devtools window won't be closed when the extension is reloaded (which first involves unloading the extension). This is a special case, as the devtools window will typically be closed when the target is destroyed.

That means that if an extension is reloaded while a devtools window is open for that extension's background page, the FrameTreeNode pointer passed to the TracingHandler instance will become stale. Attempts to use that pointer will then result in a use-after-free in the browser process.

**VERSION**  

Chrome Version: Tested on 89.0.4389.114 (stable) and 91.0.4463.1 (canary)  

Operating System: Windows 10, version 20H2

**REPRODUCTION CASE**  

The use-after-free described above can be triggered by an extension with a devtools\_page entry, provided the user opens the devtools for an extension's background page. If the user has installed a devtools extension, this is perhaps more likely than normal, since the extension would only be useful when opening the devtools.

1. Install the attached extension.
2. Navigate to chrome://extensions/ and open the devtools for an extension's background page (any extension will do).
3. Once the devtools has been opened, devtools\_page.html will first reload the extension being debugged. It will then select the "Performance" panel and attempt to start recording (by forwarding the Ctrl+E shortcut). This will result in a use-after-free in the browser process. You can verify that by going through the steps above in an asan build.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [devtools_page.html](attachments/devtools_page.html) (text/plain, 107 B)
- [devtools_page.js](attachments/devtools_page.js) (text/plain, 728 B)
- [manifest.json](attachments/manifest.json) (text/plain, 134 B)

## Timeline

### [Deleted User] (2021-03-31)

[Empty comment from Monorail migration]

### de...@gmail.com (2021-03-31)

As mentioned in the summary, this issue occurs because the FrameTreeNode pointer passed to the TracingHandler instance becomes stale when the extension being debugged is reloaded. Since reloading an extension first involves unloading the extension, the FrameTreeNode is destroyed when the ExtensionHost is destroyed.

However, the devtools window remains open and the debugging session remains attached.

When attempting to start recording performance information, the FrameTreeNode pointer will be used:

https://source.chromium.org/chromium/chromium/src/+/master:content/browser/devtools/protocol/tracing_handler.cc;l=861;drc=34d355d0e47c4b77c60737afe605876f4d5278c5

However, because the FrameTreeNode was destroyed when the extension was unloaded, this results in a use-after-free.

### dr...@chromium.org (2021-04-01)

I had to manually reload the extension to get this to trigger, but I did get the UaF (stack trace below). Due to the extreme mitigating factors (the malicious extension being installed and the devtools for another extension being open), assigning medium severity.

I'm not sure whether root cause here is in devtools or extensions, adding an owner for both.

[Monorail components: Platform>DevTools Platform>Extensions]

### [Deleted User] (2021-04-01)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-14)

caseq: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-28)

caseq: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-05-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a30ebdbe821193b398f1843ebf38a20ecec5cbc5

commit a30ebdbe821193b398f1843ebf38a20ecec5cbc5
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Fri May 14 00:48:39 2021

DevTools: fix UAF in tracig handler

Bug: 1194431
Change-Id: Id697f2fc35a18af7de30aa668cc0c8669c2d1813
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2886624
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Reviewed-by: Peter Kvitek <kvitekp@chromium.org>
Cr-Commit-Position: refs/heads/master@{#882780}

[modify] https://crrev.com/a30ebdbe821193b398f1843ebf38a20ecec5cbc5/chrome/browser/devtools/protocol/devtools_protocol_browsertest.cc
[modify] https://crrev.com/a30ebdbe821193b398f1843ebf38a20ecec5cbc5/chrome/browser/devtools/protocol/devtools_protocol_test_support.h
[add] https://crrev.com/a30ebdbe821193b398f1843ebf38a20ecec5cbc5/chrome/test/data/devtools/extensions/simple_background_page/background.js
[add] https://crrev.com/a30ebdbe821193b398f1843ebf38a20ecec5cbc5/chrome/test/data/devtools/extensions/simple_background_page/manifest.json
[modify] https://crrev.com/a30ebdbe821193b398f1843ebf38a20ecec5cbc5/content/browser/devtools/browser_devtools_agent_host.cc
[modify] https://crrev.com/a30ebdbe821193b398f1843ebf38a20ecec5cbc5/content/browser/devtools/protocol/tracing_handler.cc
[modify] https://crrev.com/a30ebdbe821193b398f1843ebf38a20ecec5cbc5/content/browser/devtools/protocol/tracing_handler.h
[modify] https://crrev.com/a30ebdbe821193b398f1843ebf38a20ecec5cbc5/content/browser/devtools/protocol/tracing_handler_unittest.cc
[modify] https://crrev.com/a30ebdbe821193b398f1843ebf38a20ecec5cbc5/content/browser/devtools/render_frame_devtools_agent_host.cc


### ca...@chromium.org (2021-05-14)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-05-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0e3238d1a245adf68756d9f6bd616512fa2eda1e

commit 0e3238d1a245adf68756d9f6bd616512fa2eda1e
Author: Ian Clelland <iclelland@chromium.org>
Date: Fri May 14 13:25:11 2021

Revert "DevTools: fix UAF in tracig handler"

This reverts commit a30ebdbe821193b398f1843ebf38a20ecec5cbc5.

Reason for revert: New test failing on several Win7 bots:
Failures seem to have started with this CL on four separate bots:
https://ci.chromium.org/ui/p/chromium/builders/ci/Win%207%20Tests%20x64%20(1)/79349
https://ci.chromium.org/p/chromium/builders/ci/Win7%20Tests%20%281%29/116310
https://ci.chromium.org/p/chromium/builders/ci/Win7%20Tests%20%28dbg%29%281%29/89801
https://ci.chromium.org/p/chromium/builders/ci/Win7%20%2832%29%20Tests/70849

Original change's description:
> DevTools: fix UAF in tracig handler
>
> Bug: 1194431
> Change-Id: Id697f2fc35a18af7de30aa668cc0c8669c2d1813
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2886624
> Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
> Reviewed-by: Peter Kvitek <kvitekp@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#882780}

Bug: 1194431
Change-Id: I9466af070995c73ad233153111fc65272e6c3389
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2897340
Auto-Submit: Ian Clelland <iclelland@chromium.org>
Owners-Override: Ian Clelland <iclelland@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#882937}

[modify] https://crrev.com/0e3238d1a245adf68756d9f6bd616512fa2eda1e/chrome/browser/devtools/protocol/devtools_protocol_browsertest.cc
[modify] https://crrev.com/0e3238d1a245adf68756d9f6bd616512fa2eda1e/chrome/browser/devtools/protocol/devtools_protocol_test_support.h
[delete] https://crrev.com/e17f34fc306e858796d703116955d0b9eacf8feb/chrome/test/data/devtools/extensions/simple_background_page/background.js
[delete] https://crrev.com/e17f34fc306e858796d703116955d0b9eacf8feb/chrome/test/data/devtools/extensions/simple_background_page/manifest.json
[modify] https://crrev.com/0e3238d1a245adf68756d9f6bd616512fa2eda1e/content/browser/devtools/browser_devtools_agent_host.cc
[modify] https://crrev.com/0e3238d1a245adf68756d9f6bd616512fa2eda1e/content/browser/devtools/protocol/tracing_handler.cc
[modify] https://crrev.com/0e3238d1a245adf68756d9f6bd616512fa2eda1e/content/browser/devtools/protocol/tracing_handler.h
[modify] https://crrev.com/0e3238d1a245adf68756d9f6bd616512fa2eda1e/content/browser/devtools/protocol/tracing_handler_unittest.cc
[modify] https://crrev.com/0e3238d1a245adf68756d9f6bd616512fa2eda1e/content/browser/devtools/render_frame_devtools_agent_host.cc


### ad...@chromium.org (2021-05-14)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-05-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5b231fef0de22da883445fe1a3464ea5bbb7508e

commit 5b231fef0de22da883445fe1a3464ea5bbb7508e
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Sat May 15 00:07:51 2021

Reland "DevTools: fix UAF in tracig handler"

This reverts commit 0e3238d1a245adf68756d9f6bd616512fa2eda1e.

Reason for revert: [WIP on fix]

Original change's description:
> Revert "DevTools: fix UAF in tracig handler"
>
> This reverts commit a30ebdbe821193b398f1843ebf38a20ecec5cbc5.
>
> Reason for revert: New test failing on several Win7 bots:
> Failures seem to have started with this CL on four separate bots:
> https://ci.chromium.org/ui/p/chromium/builders/ci/Win%207%20Tests%20x64%20(1)/79349
> https://ci.chromium.org/p/chromium/builders/ci/Win7%20Tests%20%281%29/116310
> https://ci.chromium.org/p/chromium/builders/ci/Win7%20Tests%20%28dbg%29%281%29/89801
> https://ci.chromium.org/p/chromium/builders/ci/Win7%20%2832%29%20Tests/70849
>
> Original change's description:
> > DevTools: fix UAF in tracig handler
> >
> > Bug: 1194431
> > Change-Id: Id697f2fc35a18af7de30aa668cc0c8669c2d1813
> > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2886624
> > Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
> > Reviewed-by: Peter Kvitek <kvitekp@chromium.org>
> > Cr-Commit-Position: refs/heads/master@{#882780}
>
> Bug: 1194431
> Change-Id: I9466af070995c73ad233153111fc65272e6c3389
> No-Presubmit: true
> No-Tree-Checks: true
> No-Try: true
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2897340
> Auto-Submit: Ian Clelland <iclelland@chromium.org>
> Owners-Override: Ian Clelland <iclelland@chromium.org>
> Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
> Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
> Cr-Commit-Position: refs/heads/master@{#882937}

Bug: 1194431
Change-Id: I7e6190b2db8adf2974403bc6463ba39b55448395
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2895453
Reviewed-by: Peter Kvitek <kvitekp@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/heads/master@{#883216}

[modify] https://crrev.com/5b231fef0de22da883445fe1a3464ea5bbb7508e/chrome/browser/devtools/protocol/devtools_protocol_browsertest.cc
[modify] https://crrev.com/5b231fef0de22da883445fe1a3464ea5bbb7508e/chrome/browser/devtools/protocol/devtools_protocol_test_support.h
[add] https://crrev.com/5b231fef0de22da883445fe1a3464ea5bbb7508e/chrome/test/data/devtools/extensions/simple_background_page/background.js
[add] https://crrev.com/5b231fef0de22da883445fe1a3464ea5bbb7508e/chrome/test/data/devtools/extensions/simple_background_page/manifest.json
[modify] https://crrev.com/5b231fef0de22da883445fe1a3464ea5bbb7508e/content/browser/devtools/browser_devtools_agent_host.cc
[modify] https://crrev.com/5b231fef0de22da883445fe1a3464ea5bbb7508e/content/browser/devtools/protocol/tracing_handler.cc
[modify] https://crrev.com/5b231fef0de22da883445fe1a3464ea5bbb7508e/content/browser/devtools/protocol/tracing_handler.h
[modify] https://crrev.com/5b231fef0de22da883445fe1a3464ea5bbb7508e/content/browser/devtools/protocol/tracing_handler_unittest.cc
[modify] https://crrev.com/5b231fef0de22da883445fe1a3464ea5bbb7508e/content/browser/devtools/render_frame_devtools_agent_host.cc


### ca...@chromium.org (2021-05-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-18)

Requesting merge to beta M91 because latest trunk commit (882780) appears to be after beta branch point (965).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-18)

This bug requires manual review: We are only 6 days from stable.
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
Owners: benmason@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-05-18)

This is a fairly complex change for a medium severity bug - I'm going to reject Sheriffbot's suggestion to merge to M91, and let this be released in M92 instead.

### am...@google.com (2021-06-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-06-10)

Congratulations- the VRP Panel has decided to award you $5,000 for this report. Nice work on another one! 

### am...@google.com (2021-06-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-07-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-07-19)

[Empty comment from Monorail migration]

### rz...@google.com (2021-07-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-30)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-03)

[Empty comment from Monorail migration]

### gi...@google.com (2021-08-05)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-08-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/48f5ff14d4fa39452e1be7ce0d44aeb17bc490f4

commit 48f5ff14d4fa39452e1be7ce0d44aeb17bc490f4
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Thu Aug 05 14:01:28 2021

[M90-LTS] DevTools: fix UAF in tracig handler

(cherry picked from commit a30ebdbe821193b398f1843ebf38a20ecec5cbc5)

Bug: 1194431
Change-Id: Id697f2fc35a18af7de30aa668cc0c8669c2d1813
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2886624
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#882780}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3062943
Reviewed-by: Jana Grill <janagrill@google.com>
Owners-Override: Jana Grill <janagrill@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1557}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/48f5ff14d4fa39452e1be7ce0d44aeb17bc490f4/chrome/browser/devtools/protocol/devtools_protocol_browsertest.cc
[modify] https://crrev.com/48f5ff14d4fa39452e1be7ce0d44aeb17bc490f4/chrome/browser/devtools/protocol/devtools_protocol_test_support.h
[add] https://crrev.com/48f5ff14d4fa39452e1be7ce0d44aeb17bc490f4/chrome/test/data/devtools/extensions/simple_background_page/background.js
[add] https://crrev.com/48f5ff14d4fa39452e1be7ce0d44aeb17bc490f4/chrome/test/data/devtools/extensions/simple_background_page/manifest.json
[modify] https://crrev.com/48f5ff14d4fa39452e1be7ce0d44aeb17bc490f4/content/browser/devtools/browser_devtools_agent_host.cc
[modify] https://crrev.com/48f5ff14d4fa39452e1be7ce0d44aeb17bc490f4/content/browser/devtools/protocol/tracing_handler.cc
[modify] https://crrev.com/48f5ff14d4fa39452e1be7ce0d44aeb17bc490f4/content/browser/devtools/protocol/tracing_handler.h
[modify] https://crrev.com/48f5ff14d4fa39452e1be7ce0d44aeb17bc490f4/content/browser/devtools/protocol/tracing_handler_unittest.cc
[modify] https://crrev.com/48f5ff14d4fa39452e1be7ce0d44aeb17bc490f4/content/browser/devtools/render_frame_devtools_agent_host.cc


### rz...@google.com (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1194431?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>DevTools, Platform>Extensions]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055394)*
