# Security: Possible for extension to escape sandbox via Target.setAutoAttach and Target.sendMessageToTarget

| Field | Value |
|-------|-------|
| **Issue ID** | [40053041](https://issues.chromium.org/issues/40053041) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>DevTools>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2020-08-10 |
| **Bounty** | $15,000.00 |

## Description

**VULNERABILITY DETAILS**  

When using the chrome.debugger API, one of the methods an extension can call is Target.setAutoAttach. That method will attach all cross-process subframes (of the currently debugged page) to the debugger.

Once that's been done, an extension can call Target.sendMessageToTarget to dispatch a protocol message to an attached frame. Because the frame will have been attached in a higher privileged access mode (kRegular vs kAutoAttachOnly), additional protocol methods will be available to it.

By forwarding the appropriate protocol messages through the frame, an extension can attach to chrome://downloads and open a downloaded executable, which allows the extension to escape the sandbox.

**VERSION**  

Chrome Version: Tested on 84.0.4147.105 (stable) and 86.0.4229.0 (canary)  

Operating System: Windows 10, version 1909

**REPRODUCTION CASE**

1. Install the attached extension.
2. After a couple of seconds, the target executable (in this case, Process Explorer) should be started.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [background.js](attachments/background.js) (text/plain, 5.2 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 244 B)
- [page.html](attachments/page.html) (text/plain, 304 B)

## Timeline

### de...@gmail.com (2020-08-10)

The demonstration extension here performs a few steps:

1. The extension downloads the target executable.
2. It then opens chrome://downloads in a new tab.
3. Once chrome://downloads has loaded, the extension opens page.html in a new tab.
4. Once page.html has loaded, the extension attaches to it using chrome.debugger.attach.
5. It then calls Target.setAutoAttach. This will result in the subframe on the page being attached to the debugger in kRegular mode.
6. It then requests that the subframe attach to the chrome://downloads page. This is done by sending a Target.attachToTarget message to the subframe via Target.sendMessageToTarget.
7. The extension then sends a key event to the downloads page, by relaying Input.dispatchKeyEvent through the suframe using Target.sendMessageToTarget. This input event is needed to ensure that the downloaded file can be opened (which is something that requires a recent user gesture).
8. The extension then calls Runtime.evaluate via Target.sendMessageToTarget. The expression passed to the Runtime.evaluate call will run within the context of the chrome://downloads page and open the executable downloaded in step 1.

One thing worth noting is that I don't think these steps will work in the same way under Linux, since any file the extension downloads won't be marked as executable.

However, another devtools protocol method the extension can call through an auto attached subframe is Browser.setDownloadBehavior. That allows a custom downloads directory to be set.

So an extension on Linux could first determine the path to the user's home directory (by attaching to a file:///home/ page and examining the contents) then overwrite something like /home/{user}/.profile. That file may then be sourced and any embedded commands executed when the user next logs in graphically.

Overwriting an existing file will work, since when the "behavior" parameter passed to Browser.setDownloadBehavior is "allow", existing files will be overwritten when downloading.

### de...@gmail.com (2020-08-10)

When an extension calls chrome.debugger.attach, ExtensionDevToolsClientHost::MayAttachToBrowser returns false and the TargetHandler is constructed in kAutoAttachOnly mode:

https://source.chromium.org/chromium/chromium/src/+/master:content/browser/devtools/render_frame_devtools_agent_host.cc;l=334;drc=f2cfa81dcdb4ede16a8b637158a0e0c5b21672af

When calling Target.setAutoAttach, all cross-process subframes are attached:

https://source.chromium.org/chromium/chromium/src/+/master:content/browser/devtools/protocol/target_auto_attacher.cc;l=184;drc=74a68a32bb8cc4f5db3abe45d8243637db1aaa40

When attaching the frames, the following MayAttachToBrowser call:

https://source.chromium.org/chromium/chromium/src/+/master:content/browser/devtools/render_frame_devtools_agent_host.cc;l=327;drc=f2cfa81dcdb4ede16a8b637158a0e0c5b21672af

resolves to:

https://source.chromium.org/chromium/chromium/src/+/master:content/public/browser/devtools_agent_host_client.cc;l=13;drc=0788b1d419f78050f1114fffefd1f68cd88d1dab

Which always returns true.

That then means that when TargetHandler is constructed, the access mode is set to kRegular:

https://source.chromium.org/chromium/chromium/src/+/master:content/browser/devtools/render_frame_devtools_agent_host.cc;l=333;drc=f2cfa81dcdb4ede16a8b637158a0e0c5b21672af

So a number of methods within the Target namespace that are blocked when the access mode is kAutoAttachOnly can then be called.

Note that although all cross-process subframes will be attached to the debugger, it's not possible to interact with them via chrome.debugger.sendCommand. This is because the agent hosts associated with the subframes won't be represented in the list of attached client hosts that are maintained for extensions:

https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/extensions/api/debugger/debugger_api.cc;l=499;drc=6ac77aad9d92fc74fbba600c817fae15c30c5697

On the other hand, when using Target.sendMessageToTarget, the lookup is performed against the set of attached sessions:

https://source.chromium.org/chromium/chromium/src/+/master:content/browser/devtools/protocol/target_handler.cc;l=709;drc=6cf20e7892749db10432df68cfe7a6d16f629c67

This set is updated via the following call when attaching via Target.setAutoAttach or Target.attachToTarget:

https://source.chromium.org/chromium/chromium/src/+/master:content/browser/devtools/protocol/target_handler.cc;l=360;drc=6cf20e7892749db10432df68cfe7a6d16f629c67

### xi...@chromium.org (2020-08-10)

Thanks for the detailed report! dgozman@, could you take a look at this issue and evaluate if https://crbug.com/chromium/1114636#c2 is the root cause? Thanks!

[Monorail components: Platform>DevTools>Platform]

### dg...@chromium.org (2020-08-11)

[Empty comment from Monorail migration]

### si...@chromium.org (2020-08-11)

[Empty comment from Monorail migration]

### si...@chromium.org (2020-08-11)

Dmitry, could you explain the security design behind the attach modes kRegular and kAutoAttachOnly?

From the description above, it seems a lot is going wrong:
 - Why does the attach in step (5) get mode kRegular?
 - It seems strange that sendMessageToTarget can send a "Target.attachToTarget" message

What is the proper fix?

I think Target.sendMessageToTarget should only be allowed for targets the session can also attach to.
Additonally, I would forbid Target.attachToTarget via sendMessageToTarget, but I don't know the implications.

In general, looking at the three recent security bugs in this area we might be in for a redesign of our security here.


### si...@chromium.org (2020-08-11)

[Empty comment from Monorail migration]

### si...@chromium.org (2020-08-11)

This particular repro also relies on non-flattened auto attach mode. Maybe we should go forward and deprecate non-flattened mode right now?

### dg...@chromium.org (2020-08-11)

re https://crbug.com/chromium/1114636#c6:

> Why does the attach in step (5) get mode kRegular?
This is a bug. At the time we introduced security checks, targets infrastructure was already in place, so this particular place was missed.

> It seems strange that sendMessageToTarget can send a "Target.attachToTarget" message
Well, if you are attached to the target, you should be able to send any messages to it, in particular to attach to its subtargets. I think this is overall fine, as long as we properly handle specific restrictions like MayAttachToBrowser.

> In general, looking at the three recent security bugs in this area we might be in for a redesign of our security here.
This area definitely needs some love :)

> Maybe we should go forward and deprecate non-flattened mode right now?
Sure, we can go ahead and deprecate it. There is an issue for that [1]. However, we cannot remove it any time soon, unfortunately, due to heavy usage in legacy clients.

[1] https://bugs.chromium.org/p/chromium/issues/detail?id=991325



### [Deleted User] (2020-08-11)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-11)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ya...@chromium.org (2020-08-12)

Dmitry, do you have more details on these legacy clients, and whether they have plans to migrate? If not, waiting them indefinitely does not sound like a good path forward.

### dg...@chromium.org (2020-08-12)

Well, Target domain is public, so we don't know what do the clients in the wild do with it.

I know that Telemetry, ChromeDriver, Puppeteer, Playwright, Visual Studio Code, Lighthouse - all use Target domain, but some of these might be already using the flatten version. Extensions with chrome.debugger permission can be using it as well, and we don't support flatten mode there, IIRC.

Github search [1] brings some usages in mozilla remote, nwjs, a Go client called web-exfiltration, and 100 more search result pages. I don't know whether they are actually using Target domain, in legacy or flatten mode.

[1] https://github.com/search?q=Target.attachedToTarget&type=Code

### si...@chromium.org (2020-08-17)

I think Target.sendMessageToTarget should only be possible for targets the client can attach to.

### [Deleted User] (2020-08-24)

caseq: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/814a27f8522b6ccddcce1a8f6a3b8fb37128ecf9

commit 814a27f8522b6ccddcce1a8f6a3b8fb37128ecf9
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Fri Aug 28 18:55:17 2020

Delegate TargetHandler::Session permission checks to the root client

Bug: 1114636
Change-Id: Iba3865206d7e80b363ec69180ac05e20b56aade2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2380855
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/heads/master@{#802736}

[modify] https://crrev.com/814a27f8522b6ccddcce1a8f6a3b8fb37128ecf9/chrome/browser/extensions/api/debugger/debugger_apitest.cc
[add] https://crrev.com/814a27f8522b6ccddcce1a8f6a3b8fb37128ecf9/chrome/test/data/extensions/api_test/debugger_auto_attach_permissions/background.js
[add] https://crrev.com/814a27f8522b6ccddcce1a8f6a3b8fb37128ecf9/chrome/test/data/extensions/api_test/debugger_auto_attach_permissions/manifest.json
[add] https://crrev.com/814a27f8522b6ccddcce1a8f6a3b8fb37128ecf9/chrome/test/data/extensions/api_test/debugger_auto_attach_permissions/page.html
[modify] https://crrev.com/814a27f8522b6ccddcce1a8f6a3b8fb37128ecf9/content/browser/devtools/protocol/target_handler.cc


### ca...@chromium.org (2020-08-28)

Fixed by the commit referenced above. Thanks for the report, David, a very impressive work as usually!

Some random comments on the discussion above:
- (re https://crbug.com/chromium/1114636#c6) "Target.sendMessageToTarget should only be allowed for targets the session can also attach to" -- that's already the case. Actually, we only send it to the targets we previously attached to; the bug is in that DevToolsAgentHostClient implemented by DevToolsTargetHandler::Session is a more permission than the original one;
- it would be nice to deprecate non-flat mode for extensions (and it is generally deprecated already), but it turns out we actually don't support flat mode for extensions right now -- so this should be fixed first (crbug.com/1123159)


### [Deleted User] (2020-08-29)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-29)

Requesting merge to stable M85 because latest trunk commit (802736) appears to be after stable branch point (782793).

Requesting merge to beta M85 because latest trunk commit (802736) appears to be after beta branch point (782793).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-29)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-08-31)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-31)

caseq@ please could you comment on any stability or compatibility risks from merging this back to stable? As a high severity security bug we'd normally merge this back to M86 and M85 so long as you think it's nearly zero risk. If there's any chance this could break compatibility, perhaps merging to M86 is a good compromise?

### ad...@google.com (2020-08-31)

[Empty comment from Monorail migration]

### [Deleted User] (2020-09-01)

Your change meets the bar and is auto-approved for M86. Please go ahead and merge the CL to branch 4240 (refs/branch-heads/4240) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: govind@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS),  pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2020-09-01)

I wouldn't be too concerned about breaking compatibility for the extensions that are doing *this* :-) Let's start with m86 anyway, and follow up with a merge to m85, in a while, provided it caused no regression and you think this is useful.


### ad...@chromium.org (2020-09-01)

SGTM.

### ad...@google.com (2020-09-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-09-02)

Congratulations! The VRP panel has decided to award $15,000 for this report.

### ad...@google.com (2020-09-03)

[Empty comment from Monorail migration]

### pb...@google.com (2020-09-05)

Please merge your change to M86 branch 4240 ASAP. Thank you.

### [Deleted User] (2020-09-07)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@google.com (2020-09-08)

[Comment Deleted]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/845cf2d928ea18078eebe9b25be4b14776c7e5ec

commit 845cf2d928ea18078eebe9b25be4b14776c7e5ec
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Tue Sep 08 22:32:50 2020

Delegate TargetHandler::Session permission checks to the root client

(cherry picked from commit 814a27f8522b6ccddcce1a8f6a3b8fb37128ecf9)

TBR: rdevlin.cronin@chromium.org
Bug: 1114636
Change-Id: Iba3865206d7e80b363ec69180ac05e20b56aade2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2380855
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#802736}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2387414
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#539}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/845cf2d928ea18078eebe9b25be4b14776c7e5ec/chrome/browser/extensions/api/debugger/debugger_apitest.cc
[add] https://crrev.com/845cf2d928ea18078eebe9b25be4b14776c7e5ec/chrome/test/data/extensions/api_test/debugger_auto_attach_permissions/background.js
[add] https://crrev.com/845cf2d928ea18078eebe9b25be4b14776c7e5ec/chrome/test/data/extensions/api_test/debugger_auto_attach_permissions/manifest.json
[add] https://crrev.com/845cf2d928ea18078eebe9b25be4b14776c7e5ec/chrome/test/data/extensions/api_test/debugger_auto_attach_permissions/page.html
[modify] https://crrev.com/845cf2d928ea18078eebe9b25be4b14776c7e5ec/content/browser/devtools/protocol/target_handler.cc


### sr...@google.com (2020-09-11)

Is the issue looking good on Beta ? If so is it ready for Merge to M85 , we can wait for more beta coverage until middle of next week before merging to M85 for more data

### ad...@google.com (2020-09-15)

Approving merge to M85, branch 4183. Please merge, assuming things are looking good in Canary and beta.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-09-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/503e8d49042e964487d479adbcf00748a489915b

commit 503e8d49042e964487d479adbcf00748a489915b
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Thu Sep 17 05:28:26 2020

[m85] Delegate TargetHandler::Session permission checks to the root client

(cherry picked from commit 814a27f8522b6ccddcce1a8f6a3b8fb37128ecf9)

(cherry picked from commit 845cf2d928ea18078eebe9b25be4b14776c7e5ec)

TBR: rdevlin.cronin@chromium.org
Bug: 1114636
Change-Id: Iba3865206d7e80b363ec69180ac05e20b56aade2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2380855
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#802736}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2387414
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4240@{#539}
Cr-Original-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2413347
Cr-Commit-Position: refs/branch-heads/4183@{#1847}
Cr-Branched-From: 740e9e8a40505392ba5c8e022a8024b3d018ca65-refs/heads/master@{#782793}

[modify] https://crrev.com/503e8d49042e964487d479adbcf00748a489915b/chrome/browser/extensions/api/debugger/debugger_apitest.cc
[add] https://crrev.com/503e8d49042e964487d479adbcf00748a489915b/chrome/test/data/extensions/api_test/debugger_auto_attach_permissions/background.js
[add] https://crrev.com/503e8d49042e964487d479adbcf00748a489915b/chrome/test/data/extensions/api_test/debugger_auto_attach_permissions/manifest.json
[add] https://crrev.com/503e8d49042e964487d479adbcf00748a489915b/chrome/test/data/extensions/api_test/debugger_auto_attach_permissions/page.html
[modify] https://crrev.com/503e8d49042e964487d479adbcf00748a489915b/content/browser/devtools/protocol/target_handler.cc


### ad...@google.com (2020-09-21)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### Ju...@microsoft.com (2020-12-08)

lukasza@, isn't it possible to distrust `Input.dispatchKeyEvent` from WebUI renderer and check actual user click in the browser process?

### Ju...@microsoft.com (2020-12-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1114636?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053041)*
