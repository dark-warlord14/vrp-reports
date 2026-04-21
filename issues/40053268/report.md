# Security: Possible for extension to escape sandbox via chrome.debugger API and error page

| Field | Value |
|-------|-------|
| **Issue ID** | [40053268](https://issues.chromium.org/issues/40053268) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Extensions>API |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2020-09-06 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

A recent change for <https://crbug.com/chromium/1113558> updated the way in which access checks are performed when a frame attached to the debugger is navigated. Previously, checks would only be run against the frame itself; now, checks are run against subframes as well.

One subtle, but important, consequence of the change is that when navigating, checks are now run against the original site instance URL, rather than the new site instance URL. That allows the debugger to stay attached, even when navigating to a privileged location.

By taking advantage of that behavior, an extension can attach to a frame that's in the same site instance as a chrome://downloads/ page and use that frame to run code within the context of the downloads page. The extension can then open a downloaded executable and escape the sandbox.

**VERSION**  

Chrome Version: Tested on 87.0.4252.0 (dev) and 87.0.4256.0 (canary)  

Operating System: Windows 10, version 2004

**REPRODUCTION CASE**

1. Install the attached extension.
2. Wait about 10 seconds.
3. The target executable (in this case, Process Explorer) should be started.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [background.js](attachments/background.js) (text/plain, 14.8 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 223 B)
- [page.html](attachments/page.html) (text/plain, 478 B)

## Timeline

### de...@gmail.com (2020-09-06)

As mentioned in the summary, the extension here aims to take advantage of some recent changes. Therefore, it will work in Chrome dev and canary, but not in earlier versions of Chrome.

There are a couple of reasons why the behavior described above works overall:

Firstly, when navigating the https://www.google.com/non-existent subframe in page.html to filesystem:chrome://downloads/non-existent/, RenderFrameDevToolsAgentHost::UpdateFrameHost will first be called by RenderFrameDevToolsAgentHost::ReadyToCommitNavigation:

https://source.chromium.org/chromium/chromium/src/+/master:content/browser/devtools/render_frame_devtools_agent_host.cc;l=428;drc=baeb23f1d7ef50f046a2eb666e2f1bc365afc9cb

It's important to note that at that point the navigation won't yet have completed.

When RenderFrameDevToolsAgentHost::UpdateFrameHost is called, it will first update the frame_host_ reference that it holds:

https://source.chromium.org/chromium/chromium/src/+/master:content/browser/devtools/render_frame_devtools_agent_host.cc;l=468;drc=baeb23f1d7ef50f046a2eb666e2f1bc365afc9cb

It will then perform a set of access checks:

https://source.chromium.org/chromium/chromium/src/+/master:content/browser/devtools/render_frame_devtools_agent_host.cc;l=842;drc=baeb23f1d7ef50f046a2eb666e2f1bc365afc9cb

An important point here is that the access checks are performed on each node in the frame tree. As mentioned above, this method is being called before the navigation has completed. Therefore, the frame tree will still be the original frame tree. That is, the access checks will be performed against the frame tree as it currently exists, not as it will exist once the navigation has completed.

Because the extension has access to each of the original frame tree nodes, the access checks performed will succeed.

There is a subtle difference here to the access checks that were being performed previously:

https://source.chromium.org/chromium/chromium/src/+/master:content/browser/devtools/render_frame_devtools_agent_host.cc;l=832;drc=f2cfa81dcdb4ede16a8b637158a0e0c5b21672af

As can be seen, it used to be that the access checks were performed against the site instance URL for the new frame host, which would be chrome://downloads/. The updated version of the code additionally checks each subframe, but because the checks are performed against the frame tree, the site instance URLs will be for the current frames.

This is the reason why the extension doesn't work in earlier versions of Chrome - the site instance URL check that was previously being performed would result in the debugger being detached.

RenderFrameDevToolsAgentHost::UpdateFrameHost is also called several more times during navigation (e.g. by RenderFrameDevToolsAgentHost::RenderFrameHostChanged and RenderFrameDevToolsAgentHost::DidFinishNavigation), however, it will simply return early because there hasn't been a frame host change:

https://source.chromium.org/chromium/chromium/src/+/master:content/browser/devtools/render_frame_devtools_agent_host.cc;l=458;drc=baeb23f1d7ef50f046a2eb666e2f1bc365afc9cb

The second reason why the behavior described works is that it's possible to navigate to filesystem:chrome://downloads/non-existent/ using the Page.navigate devtools protocol method.

In https://crbug.com/chromium/1113558, there's a discussion of restricting Page.navigate so that it can only navigate to URLs for which MayAttachToURL would return true:

https://bugs.chromium.org/p/chromium/issues/detail?id=1113558#c11

Although that check hasn't been implemented yet, I don't think it would prevent this behavior, for the reason that ExtensionDevToolsClientHost::MayAttachToURL returns true when passed the URL filesystem:chrome://downloads/non-existent/.

That method does ultimately contain a check to determine whether the scheme of the provided URL is "chrome":

https://source.chromium.org/chromium/chromium/src/+/master:extensions/common/permissions/permissions_data.cc;l=136;drc=5adb77404837e4e4275bd3687b4d7f4ed8aafdaa

However, the scheme of filesystem:chrome://downloads/non-existent/ is "filesystem", not "chrome".

So that check will pass.

Therefore, even if Page.navigate was updated to call MayAttachToURL before performing the navigation, that wouldn't prevent the behavior described here.

The fact that MayAttachToURL returns true when passed filesystem:chrome://downloads/non-existent/ is also the reason why the debugger isn't detached when initiating the navigation.

When the navigation is initially requested, OnNavigationRequestWillBeSent will be called. That method first retrieves the URL associated with the navigation:

https://source.chromium.org/chromium/chromium/src/+/master:content/browser/devtools/render_frame_devtools_agent_host.cc;l=621;drc=baeb23f1d7ef50f046a2eb666e2f1bc365afc9cb

It then passes that URL to MayAttachToURL:

https://source.chromium.org/chromium/chromium/src/+/master:content/browser/devtools/render_frame_devtools_agent_host.cc;l=627;drc=baeb23f1d7ef50f046a2eb666e2f1bc365afc9cb

The URL associated with the navigation will be filesystem:chrome://downloads/non-existent/. Additionally, is_webui will be retrieved from the current frame_host_ and will be false (though since filesystem:chrome://downloads/non-existent/ will load an error page, is_webui would be false for that as well). Ultimately, that means that MayAttachToURL will return true and the debugger won't be detached.

The demonstration extension also relies on some other specific behavior and there are comments describing that within the code.

### de...@gmail.com (2020-09-06)

To summarize, it's possible to attach the debugger to a filesystem:chrome://downloads/non-existent/ page (which ultimately enables the rest of the demonstrated behavior) because:

- OnNavigationRequestWillBeSent calls MayAttachToURL with filesystem:chrome://downloads/non-existent/. MayAttachToURL returns true, which means the debugger won't be detached.
- RenderFrameDevToolsAgentHost::UpdateFrameHost is first called by RenderFrameDevToolsAgentHost::ReadyToCommitNavigation. At this point, the stored frame_host_ is updated and access checks are performed, but the checks are run against the current frame tree, to which the extension has access.
- RenderFrameDevToolsAgentHost::UpdateFrameHost is called several more times during navigation, but returns early because the frame host hasn't changed (from when it was updated during the first call to RenderFrameDevToolsAgentHost::UpdateFrameHost).

### rs...@chromium.org (2020-09-07)

Thanks for the report; I can verify this in 87.0.4253.0.

[Monorail components: Platform>DevTools>JavaScript Platform>Extensions>API]

### [Deleted User] (2020-09-08)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-09-20)

caseq: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-05)

caseq: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### va...@chromium.org (2020-10-22)

Friendly ping from the security 👮 for this High severity bug. Any updates?

For high severity vulnerabilities, we aim to deploy the patch to all Chrome
users in under 60 days.

### ca...@chromium.org (2020-10-27)

[Empty comment from Monorail migration]

### la...@google.com (2020-10-27)

This bug is marked as Release Block Stable for M87 which is scheduled for Stable Release cut on November 10th. Please address this bug at the earliest. If this is no longer targeting M87 then please update the milestone target.



### ca...@chromium.org (2020-10-28)

[Empty comment from Monorail migration]

### ca...@chromium.org (2020-10-29)

Thanks for the catch, David, and the exploit is a really elaborate one!
https://chromium-review.googlesource.com/c/chromium/src/+/2506354 fixes two of the problems on DevTools side that, in combination, make this possible. However,  I think nasko@ may want to check whether any of the site isolation logic may be tightened.

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1ca6a4e6f1506c9f8cad9e3151608582e145b923

commit 1ca6a4e6f1506c9f8cad9e3151608582e145b923
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Mon Nov 02 19:26:33 2020

chrome.debugger: add more access checks

- check inner URL for nested URLs;
- check actual RFH of RenderFrameDevToolsAgentHost;

Bug: 1125362
Change-Id: I6d593d45d749b2a34d7711a983e2bda730027117
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2506354
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/heads/master@{#823249}

[modify] https://crrev.com/1ca6a4e6f1506c9f8cad9e3151608582e145b923/chrome/browser/extensions/api/debugger/debugger_api.cc
[modify] https://crrev.com/1ca6a4e6f1506c9f8cad9e3151608582e145b923/chrome/browser/extensions/api/debugger/debugger_apitest.cc
[add] https://crrev.com/1ca6a4e6f1506c9f8cad9e3151608582e145b923/chrome/test/data/extensions/api_test/debugger_check_inner_url/background.js
[add] https://crrev.com/1ca6a4e6f1506c9f8cad9e3151608582e145b923/chrome/test/data/extensions/api_test/debugger_check_inner_url/manifest.json
[add] https://crrev.com/1ca6a4e6f1506c9f8cad9e3151608582e145b923/chrome/test/data/extensions/api_test/debugger_check_inner_url/page.html
[modify] https://crrev.com/1ca6a4e6f1506c9f8cad9e3151608582e145b923/content/browser/devtools/render_frame_devtools_agent_host.cc


### ca...@chromium.org (2020-11-02)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-03)

This bug requires manual review: We are only 13 days from stable.
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
Owners: benmason@(Android), bindusuvarna @(iOS), cindyb@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@chromium.org (2020-11-03)

lukasza@ and acolwell@ have been working on site isolation protections and can also help look into whether the checks can be improved.

### [Deleted User] (2020-11-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-03)

[Empty comment from Monorail migration]

### la...@google.com (2020-11-03)

caseq@ - please address the merge questionnaire in c#16 to consider the merge request.

### ca...@chromium.org (2020-11-03)

> 1. Does your merge fit within the Merge Decision Guidelines?
> - Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge

Yes, as a P1 security regression.

> 2. Links to the CLs you are requesting to merge.

 https://chromium-review.googlesource.com/c/chromium/src/+/2506354 as referred above

> 3. Has the change landed and been verified on ToT?

Yes

> 4. Does this change need to be merged into other active release branches (M-1, M+1)?

No (regressed in m87)

> 5. Why are these changes required in this milestone after branch?

Timing of the fix.

> 6. Is this a new feature?

No.

> 7. If it is a new feature, is it behind a flag using finch?

N/A


### la...@google.com (2020-11-03)

merge approved for M87 branch 4280

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3b5e8a329109fa33d154fef1d57226b43dac6ed3

commit 3b5e8a329109fa33d154fef1d57226b43dac6ed3
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Tue Nov 03 22:49:49 2020

[m87] chrome.debugger: add more access checks

- check inner URL for nested URLs;
- check actual RFH of RenderFrameDevToolsAgentHost;

(cherry picked from commit 1ca6a4e6f1506c9f8cad9e3151608582e145b923)

TBR: rdevlin.cronin@chromium.org
Bug: 1125362
Change-Id: I6d593d45d749b2a34d7711a983e2bda730027117
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2506354
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#823249}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2518123
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/branch-heads/4280@{#1098}
Cr-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}

[modify] https://crrev.com/3b5e8a329109fa33d154fef1d57226b43dac6ed3/chrome/browser/extensions/api/debugger/debugger_api.cc
[modify] https://crrev.com/3b5e8a329109fa33d154fef1d57226b43dac6ed3/chrome/browser/extensions/api/debugger/debugger_apitest.cc
[add] https://crrev.com/3b5e8a329109fa33d154fef1d57226b43dac6ed3/chrome/test/data/extensions/api_test/debugger_check_inner_url/background.js
[add] https://crrev.com/3b5e8a329109fa33d154fef1d57226b43dac6ed3/chrome/test/data/extensions/api_test/debugger_check_inner_url/manifest.json
[add] https://crrev.com/3b5e8a329109fa33d154fef1d57226b43dac6ed3/chrome/test/data/extensions/api_test/debugger_check_inner_url/page.html
[modify] https://crrev.com/3b5e8a329109fa33d154fef1d57226b43dac6ed3/content/browser/devtools/render_frame_devtools_agent_host.cc


### ad...@google.com (2020-11-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-11-11)

Congratulations! The VRP panel has decided to award $10,000 for this report.

### ad...@google.com (2020-11-12)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-02-09)

This issue was migrated from crbug.com/chromium/1125362?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>DevTools>JavaScript, Platform>Extensions>API]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053268)*
