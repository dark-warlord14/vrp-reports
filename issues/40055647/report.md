# Security: UAF when attempting to move tab group in restored window

| Field | Value |
|-------|-------|
| **Issue ID** | [40055647](https://issues.chromium.org/issues/40055647) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>TopChrome>TabStrip>TabGroups |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | em...@chromium.org |
| **Created** | 2021-04-23 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

When a session is restored, the tab groups within that session are restored as well, with the original IDs. Using that behavior, an extension with the "sessions" permission can restore two session entries such that there are two groups in different windows with the same ID.

The extension can do that by first creating a group with two tabs, closing one  

of the tabs, then closing the window containing the second tab. Next, the extension can restore the tab, then restore the window. Both the first tab and the second tab will be in a group with the original group ID, though they'll now be in different windows.

Attempting to move the duplicated group will then result in the same effect described in <https://crbug.com/chromium/1197888> (a UAF in the browser process).

**VERSION**  

Chrome Version: Tested on 92.0.4487.0 (latest asan build)  

Operating System: Windows 10, version 20H2

**REPRODUCTION CASE**

1. Install the attached extension.
2. Once installed, the extension will create a window with three tabs and add two of the tabs to a group.
3. Next, the extension will close one of the grouped tabs, then close the window.
4. Using chrome.sessions.restore, the extension will then restore the first tab it closed. The tab will be restored with its original group. The window will then be restored. The second tab that was in the original group will also be restored with its original group. This results in two groups in different windows with the same ID.
5. Using chrome.tabGroups.move, the extension will attempt to move the duplicate group to the restored window. This will result in a use-after-free in the browser process.

As mentioned in the summary, the end effect here is the same as that described in <https://crbug.com/chromium/1197888>, though the method used is different and doesn't involve drag and drop at all. If the fix for <https://crbug.com/chromium/1197888> also ends up resolving this issue, feel free to mark it as a duplicate.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [asan_output_875538.txt](attachments/asan_output_875538.txt) (text/plain, 18.7 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 222 B)
- [service_worker.js](attachments/service_worker.js) (text/plain, 2.0 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 222 B)
- [service_worker.js](attachments/service_worker.js) (text/plain, 2.7 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 258 B)
- [service_worker.js](attachments/service_worker.js) (text/plain, 3.2 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 235 B)
- [service_worker.js](attachments/service_worker.js) (text/plain, 1.7 KB)

## Timeline

### [Deleted User] (2021-04-23)

[Empty comment from Monorail migration]

### ca...@chromium.org (2021-04-24)

collinbaker: Passing this to you since you are working on the other similar bugs, feel free to reassign as appropriate. Thanks

[Monorail components: UI>Browser>TopChrome>TabStrip>TabGroups]

### [Deleted User] (2021-04-24)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-24)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-07)

collinbaker: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### co...@chromium.org (2021-05-20)

Sorry for letting this slip.

This can be reproduced without an extension. Simply follow the same steps as the extension:
1. Open 2 windows, open 3 tabs in one of them
2. Group 2 of the 3 tabs
3. Close 1st grouped tab
4. Close window with group
5. Restore 1st tab in remaining window using History menu
6. Restore closed window using History menu
7. Observe both windows have identical group
8. Drag one window's group into the other, observe crash

After (6) you're left with two windows containing groups of the same ID. I think this is unintended. Moving a group between windows doesn't take this case into account.

I'm not sure the right way to fix this. Routing to Tab Groups team since this is not just an implementation bug: it requires more thought about restoring groups.

### cy...@chromium.org (2021-05-20)

[Empty comment from Monorail migration]

### co...@chromium.org (2021-05-20)

Thanks for the repro steps! It looks like we'd either need to update this logic or add something similar elsewhere: https://source.chromium.org/chromium/chromium/src/+/main:components/sessions/core/tab_restore_service_helper.cc;l=783-788

### co...@chromium.org (2021-05-20)

In this case the tab is restored first, then the window. At the time the tab is restored the original group does not exist, so it can be restored anywhere.

Similar logic could be applied when restoring a window: simply move all the window's grouped tabs into the appropriate group, if it already exists. However this seems unintuitive to me.

### co...@chromium.org (2021-05-20)

[Empty comment from Monorail migration]

### co...@chromium.org (2021-05-20)

Ah, gotcha, yeah the group within the window is the issue there. Hrm. One thing we could maybe do is check for an existing group and change the ID under the hood?

We might want to pull in some UX/PM attention here, but for now assigning directly to Emily who is looking at the group restore space

### [Deleted User] (2021-05-21)

emshack: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### co...@chromium.org (2021-05-21)

[Empty comment from Monorail migration]

### co...@chromium.org (2021-05-21)

+sky@ for code review

### de...@gmail.com (2021-05-24)

I'm aware of the work in progress CL for this issue (crrev.com/c/2911467), but the assumption given in the commit message doesn't hold. That is, it's possible to restore the same window more than once and if that window contains tabs in a group, that group will be duplicated.

I've attached an extension here that demonstrates that. To test it, go through the following steps:

1. Ensure the browser is set to reopen the last set of tabs on startup.
2. Install the extension.
3. Once installed, the extension will open manifest.json in a popup.
4. The extension will then close every normal window.
5. It will then create a new window with two tabs and add one of the tabs to a group, before closing the window.
6. A new tab will then be created. As there are no normal windows open, the previous window will be restored and the tab will be added to that.
7. Crucially, the previous window will still also be in the session history. The extension will restore the window from there as well, which will mean there are now two groups in different windows with the same ID. The extension will then use chrome.tabGroups.move to move the group, which will result in the same UAF described in the initial message.

It's also possible to see similar behavior by going through a simple set of steps manually:

1. Ensure the browser is set to reopen the last set of tabs on startup.
2. Exit the browser.
3. Open the browser again. Each window will be restored. Note that the previous windows are also still in the session history and can be restored for a second time (which can create duplicate groups if there are any).

To summarize, it's possible to restore a window a second time, even if it's already been (implicitly) restored once - either because a tab has been created and there are no normal windows open, or because the browser has just been started.

### co...@chromium.org (2021-05-25)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-05-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b21775d121bda1fb5084487547a63dccb5429b74

commit b21775d121bda1fb5084487547a63dccb5429b74
Author: Collin Baker <collinbaker@chromium.org>
Date: Thu May 27 20:09:16 2021

Regenerate group IDs when restoring closed window

As currently designed, tabs and windows can be restored in ways that
split the same group ID across multiple windows. For example,
restoring the same window twice, or restoring a tab from a group then
a window with the same group

Regenerating group IDs when restoring a window solves this
problem. When restoring a tab, it is always put into its group if it's
open in any window.

Bug: 1202102
Change-Id: Id07cd92f87fd48f019e38993322d4a335f2a3801
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2911467
Commit-Queue: Collin Baker <collinbaker@chromium.org>
Reviewed-by: Scott Violet <sky@chromium.org>
Reviewed-by: Charlene Yan <cyan@chromium.org>
Cr-Commit-Position: refs/heads/master@{#887307}

[modify] https://crrev.com/b21775d121bda1fb5084487547a63dccb5429b74/chrome/browser/sessions/tab_restore_browsertest.cc
[modify] https://crrev.com/b21775d121bda1fb5084487547a63dccb5429b74/components/sessions/core/tab_restore_service_helper.cc


### co...@chromium.org (2021-05-27)

I think this is fixed: neither extension causes a UAF with my CL.

I created https://crbug.com/chromium/1214075 to track a long term fix

### de...@gmail.com (2021-05-28)

I'm not sure the fix is sufficient in its current form. Although it updates the group IDs when a window is explicitly restored, it doesn't update the IDs when a window is restored as part of a session restore (as session restores are performed by a different section of the code). That means that if an extension can restore a grouped tab before a session restore, that group can still be duplicated.

I've created an extension that demonstrates that. To test:

1. Install the extension.
2. Once installed, the extension will create a new window with two tabs and add those tabs to a group, before closing one of the tabs.
3. The extension will then crash the browser.
4. Reopen the browser.
5. Once the browser starts again, the extension will find the tab it closed in the session history and restore it. Once this has happened, click "Restore" in the session crashed bubble.
6. Each of the previous windows will be restored, including the window the extension created in step 2. This means that there will now be two groups in different windows with the same ID.
7. The extension will then use chrome.tabGroups.move to move the group, which will result in the same UAF described in the initial message.

While this does require some more user interaction, I don't think it's implausible. Primarily, the user needs to reopen the browser once it's crashed and click restore. Which they probably will do if they were actively using the browser.

### de...@gmail.com (2021-05-28)

RestoreTabsToBrowser is responsible for restoring a window during a session restore:

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/sessions/session_restore.cc;l=634;drc=46bbb9795fcc1934c6cfbec096764f888c4d400a

That method will probably also need to be updated to generate new group IDs.

### [Deleted User] (2021-05-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-28)

Requesting merge to stable M91 because latest trunk commit (887307) appears to be after stable branch point (870763).

Requesting merge to beta M91 because latest trunk commit (887307) appears to be after beta branch point (870763).

Requesting merge to future beta M92 because latest trunk commit (887307) appears to be after future beta branch point (56).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-28)

This bug requires manual review: Request affecting a post-stable build
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

### [Deleted User] (2021-05-29)

Your change meets the bar and is auto-approved for M92. Please go ahead and merge the CL to branch 4515 (refs/branch-heads/4515) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: govind@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### be...@google.com (2021-06-01)

Applying desktop labels since this affects extensions

### co...@chromium.org (2021-06-01)

Reopening for c#20 and for https://crbug.com/chromium/1214197

### gi...@appspot.gserviceaccount.com (2021-06-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e0da18b57966c19f909bbf0e80220928c7567ab7

commit e0da18b57966c19f909bbf0e80220928c7567ab7
Author: Collin Baker <collinbaker@chromium.org>
Date: Tue Jun 01 19:35:08 2021

Revert "Regenerate group IDs when restoring closed window"

This reverts commit b21775d121bda1fb5084487547a63dccb5429b74.

Original change's description:
> Regenerate group IDs when restoring closed window
>
> As currently designed, tabs and windows can be restored in ways that
> split the same group ID across multiple windows. For example,
> restoring the same window twice, or restoring a tab from a group then
> a window with the same group
>
> Regenerating group IDs when restoring a window solves this
> problem. When restoring a tab, it is always put into its group if it's
> open in any window.
>
> Bug: 1202102
> Change-Id: Id07cd92f87fd48f019e38993322d4a335f2a3801
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2911467
> Commit-Queue: Collin Baker <collinbaker@chromium.org>
> Reviewed-by: Scott Violet <sky@chromium.org>
> Reviewed-by: Charlene Yan <cyan@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#887307}

Bug: 1202102, 1214197
Change-Id: Ib3a9109fde673e83856e01f67a736ee6e816d436
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2930270
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Reviewed-by: Collin Baker <collinbaker@chromium.org>
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: Collin Baker <collinbaker@chromium.org>
Cr-Commit-Position: refs/heads/master@{#888092}

[modify] https://crrev.com/e0da18b57966c19f909bbf0e80220928c7567ab7/chrome/browser/sessions/tab_restore_browsertest.cc
[modify] https://crrev.com/e0da18b57966c19f909bbf0e80220928c7567ab7/components/sessions/core/tab_restore_service_helper.cc


### co...@chromium.org (2021-06-01)

Undoing merge request/approval

### gi...@appspot.gserviceaccount.com (2021-06-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cbe2ec51f6607fc4891bf1d44392d8264c29ab2f

commit cbe2ec51f6607fc4891bf1d44392d8264c29ab2f
Author: Collin Baker <collinbaker@chromium.org>
Date: Wed Jun 02 22:34:29 2021

Reland "Regenerate group IDs when restoring closed window"

This is a reland of b21775d121bda1fb5084487547a63dccb5429b74

Changes from original:

Fixes crash caused by tab group IDs referenced by individual Tab
objects in TabRestoreService, but not listed in the Window's tab
groups.

Adds group ID regeneration to session restore to prevent bad
interaction betwee nsession restore and tab restore.

Original change's description:
> Regenerate group IDs when restoring closed window
>
> As currently designed, tabs and windows can be restored in ways that
> split the same group ID across multiple windows. For example,
> restoring the same window twice, or restoring a tab from a group then
> a window with the same group
>
> Regenerating group IDs when restoring a window solves this
> problem. When restoring a tab, it is always put into its group if it's
> open in any window.
>
> Bug: 1202102
> Change-Id: Id07cd92f87fd48f019e38993322d4a335f2a3801
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2911467
> Commit-Queue: Collin Baker <collinbaker@chromium.org>
> Reviewed-by: Scott Violet <sky@chromium.org>
> Reviewed-by: Charlene Yan <cyan@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#887307}

Bug: 1202102, 1214197
Change-Id: Ibc6df547160e5ad23cf4f69ec5bca8329b728497
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2928804
Auto-Submit: Collin Baker <collinbaker@chromium.org>
Commit-Queue: Scott Violet <sky@chromium.org>
Reviewed-by: Scott Violet <sky@chromium.org>
Cr-Commit-Position: refs/heads/master@{#888641}

[modify] https://crrev.com/cbe2ec51f6607fc4891bf1d44392d8264c29ab2f/chrome/browser/sessions/session_restore.cc
[modify] https://crrev.com/cbe2ec51f6607fc4891bf1d44392d8264c29ab2f/chrome/browser/sessions/session_restore_browsertest.cc
[modify] https://crrev.com/cbe2ec51f6607fc4891bf1d44392d8264c29ab2f/chrome/browser/sessions/tab_restore_browsertest.cc
[modify] https://crrev.com/cbe2ec51f6607fc4891bf1d44392d8264c29ab2f/components/sessions/core/tab_restore_service_helper.cc


### co...@chromium.org (2021-06-02)

David, do you see any issues with the above fix?

### co...@chromium.org (2021-06-03)

Tentatively marking as fixed

### co...@chromium.org (2021-06-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-04)

This bug requires manual review: Reverts referenced in bugdroid comments after merge request.
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
Owners: govind@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2021-06-04)

pls answer https://crbug.com/chromium/1202102#c35 for merge review. 

### co...@chromium.org (2021-06-04)

I'll defer to the security team to answer this

### de...@gmail.com (2021-06-06)

Re https://crbug.com/chromium/1202102#c32: The only other issue I can think of is when a tab is restored during a drag operation on Windows. Essentially, if a tab is created while a drag is in process, the drag will be cancelled (on Windows) and that can result in a situation where a group is split over two windows. There's some more discussion of the specifics of that in https://crbug.com/chromium/1197888. That issue is currently still open, though I'm not sure what the planned fix is right now. Depending on precisely how that issue is fixed, that might also fix the case of restoring a tab during a drag operation, but it might not.

I've attached an extension here to demonstrate the issue. To test:

1. Install the attached extension. Ensure you're using Windows.
2. Once installed, the extension will create a new window with three tabs: two that are in a group and one that's not.
3. The extension will then close one of the grouped tabs.
4. Once that's happened, start dragging the group (by dragging the group header) out of its current tab strip.
5. Once the extension detects that the tab has been attached to another window, the extension will restore the tab it closed in step 3. The restored tab will be created in the new window and the drag will be cancelled.
6. Because the drag was cancelled, the group that was being dragged will be moved back to its original window, while the restored tab will remain in the second window.
7. The extension will then use chrome.tabGroups.move to move the group, resulting in the same UAF described in the original message.

Ultimately, that behavior is at the intersection of this issue and https://crbug.com/chromium/1197888.

Aside from that, I can't see any other issues with the fix.

### am...@chromium.org (2021-06-07)

Hi Collin, we really need the owner to address the questions in https://crbug.com/chromium/1202102#c35. We are doing a respin for M91 this week and based on not being in Canary and the opened questions, I'm going to go ahead and reject for m91 merge for this week and we can get this in the next security refresh. 


### co...@chromium.org (2021-06-08)

Merge review:
1. Change has automated test coverage and has been in Canary for a week. I cannot determine whether it meets the criticality bar
2. https://chromium-review.googlesource.com/c/chromium/src/+/2928804
3. Yes
4. Yes
5. Security bug was discovered after release
6. No
7. No

### sr...@google.com (2021-06-08)

Merge approved for M92 branch:4515 pls merge asap

### co...@chromium.org (2021-06-08)

Forgot to re-add the label

### gi...@appspot.gserviceaccount.com (2021-06-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0055a99f116c2ed22d66ef0918168b18c946fbe7

commit 0055a99f116c2ed22d66ef0918168b18c946fbe7
Author: Collin Baker <collinbaker@chromium.org>
Date: Wed Jun 09 00:05:15 2021

Reland "Regenerate group IDs when restoring closed window"

This is a reland of b21775d121bda1fb5084487547a63dccb5429b74

Changes from original:

Fixes crash caused by tab group IDs referenced by individual Tab
objects in TabRestoreService, but not listed in the Window's tab
groups.

Adds group ID regeneration to session restore to prevent bad
interaction betwee nsession restore and tab restore.

Original change's description:
> Regenerate group IDs when restoring closed window
>
> As currently designed, tabs and windows can be restored in ways that
> split the same group ID across multiple windows. For example,
> restoring the same window twice, or restoring a tab from a group then
> a window with the same group
>
> Regenerating group IDs when restoring a window solves this
> problem. When restoring a tab, it is always put into its group if it's
> open in any window.
>
> Bug: 1202102
> Change-Id: Id07cd92f87fd48f019e38993322d4a335f2a3801
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2911467
> Commit-Queue: Collin Baker <collinbaker@chromium.org>
> Reviewed-by: Scott Violet <sky@chromium.org>
> Reviewed-by: Charlene Yan <cyan@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#887307}

(cherry picked from commit cbe2ec51f6607fc4891bf1d44392d8264c29ab2f)

Bug: 1202102, 1214197
Change-Id: Ibc6df547160e5ad23cf4f69ec5bca8329b728497
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2928804
Auto-Submit: Collin Baker <collinbaker@chromium.org>
Commit-Queue: Scott Violet <sky@chromium.org>
Reviewed-by: Scott Violet <sky@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#888641}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2947744
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4515@{#437}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[modify] https://crrev.com/0055a99f116c2ed22d66ef0918168b18c946fbe7/chrome/browser/sessions/session_restore.cc
[modify] https://crrev.com/0055a99f116c2ed22d66ef0918168b18c946fbe7/chrome/browser/sessions/session_restore_browsertest.cc
[modify] https://crrev.com/0055a99f116c2ed22d66ef0918168b18c946fbe7/chrome/browser/sessions/tab_restore_browsertest.cc
[modify] https://crrev.com/0055a99f116c2ed22d66ef0918168b18c946fbe7/components/sessions/core/tab_restore_service_helper.cc


### am...@google.com (2021-06-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-06-10)

Congrats, David! The VRP Panel has decided to award you $10,000 for this report. Nice work!

### am...@google.com (2021-06-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-06-15)

merge approved for M91; please merge to brach 4472 asap/before EOD Wednesday for this fix to be included in the M91 security respin. Thank you! 

### am...@chromium.org (2021-06-15)

[Comment Deleted]

### am...@chromium.org (2021-06-15)

> please merge to *branch 4472 asap/before EOD Wednesday for this fix to be included in the M91 security respin. 
EOD Wednesday (16 June 2021) - I felt that was important to stipulate. Apologies for the extra comments!

### co...@chromium.org (2021-06-15)

Emily, sorry to add this last-minute, but could you look into the merge logistics here? Collin is out this whole week, but we want to make the hard deadline. Feel free to reach out for help! Thanks!

### em...@chromium.org (2021-06-16)

Sent out a CL for review here: https://chromium-review.googlesource.com/c/chromium/src/+/2965641

### gi...@appspot.gserviceaccount.com (2021-06-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6a55e7b2ea6dae726430626cc7cf85517f6268b0

commit 6a55e7b2ea6dae726430626cc7cf85517f6268b0
Author: Collin Baker <collinbaker@chromium.org>
Date: Wed Jun 16 15:53:57 2021

Reland "Regenerate group IDs when restoring closed window"

This is a reland of b21775d121bda1fb5084487547a63dccb5429b74

Changes from original:

Fixes crash caused by tab group IDs referenced by individual Tab
objects in TabRestoreService, but not listed in the Window's tab
groups.

Adds group ID regeneration to session restore to prevent bad
interaction betwee nsession restore and tab restore.

Original change's description:
> Regenerate group IDs when restoring closed window
>
> As currently designed, tabs and windows can be restored in ways that
> split the same group ID across multiple windows. For example,
> restoring the same window twice, or restoring a tab from a group then
> a window with the same group
>
> Regenerating group IDs when restoring a window solves this
> problem. When restoring a tab, it is always put into its group if it's
> open in any window.
>
> Bug: 1202102
> Change-Id: Id07cd92f87fd48f019e38993322d4a335f2a3801
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2911467
> Commit-Queue: Collin Baker <collinbaker@chromium.org>
> Reviewed-by: Scott Violet <sky@chromium.org>
> Reviewed-by: Charlene Yan <cyan@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#887307}

(cherry picked from commit cbe2ec51f6607fc4891bf1d44392d8264c29ab2f)

Bug: 1202102, 1214197
Change-Id: Ibc6df547160e5ad23cf4f69ec5bca8329b728497
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2928804
Auto-Submit: Collin Baker <collinbaker@chromium.org>
Commit-Queue: Scott Violet <sky@chromium.org>
Reviewed-by: Scott Violet <sky@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#888641}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2965641
Auto-Submit: Emily Shack <emshack@chromium.org>
Cr-Commit-Position: refs/branch-heads/4472@{#1490}
Cr-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}

[modify] https://crrev.com/6a55e7b2ea6dae726430626cc7cf85517f6268b0/chrome/browser/sessions/session_restore.cc
[modify] https://crrev.com/6a55e7b2ea6dae726430626cc7cf85517f6268b0/chrome/browser/sessions/session_restore_browsertest.cc
[modify] https://crrev.com/6a55e7b2ea6dae726430626cc7cf85517f6268b0/chrome/browser/sessions/tab_restore_browsertest.cc
[modify] https://crrev.com/6a55e7b2ea6dae726430626cc7cf85517f6268b0/components/sessions/core/tab_restore_service_helper.cc


### am...@chromium.org (2021-06-17)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-17)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-06-17)

[Empty comment from Monorail migration]

### as...@google.com (2021-06-21)

Marking as not applicable for M86-LTS since tab groups are not in M86.

### as...@google.com (2021-06-21)

[Empty comment from Monorail migration]

### gi...@google.com (2021-06-22)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-06-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/65bacf7718f4da9a0ed1770b1649b813f6fdf7a7

commit 65bacf7718f4da9a0ed1770b1649b813f6fdf7a7
Author: Collin Baker <collinbaker@chromium.org>
Date: Tue Jun 22 13:47:45 2021

[M90-LTS] Reland "Regenerate group IDs when restoring closed window"

This is a reland of b21775d121bda1fb5084487547a63dccb5429b74

Changes from original:

Fixes crash caused by tab group IDs referenced by individual Tab
objects in TabRestoreService, but not listed in the Window's tab
groups.

Adds group ID regeneration to session restore to prevent bad
interaction betwee nsession restore and tab restore.

Original change's description:
> Regenerate group IDs when restoring closed window
>
> As currently designed, tabs and windows can be restored in ways that
> split the same group ID across multiple windows. For example,
> restoring the same window twice, or restoring a tab from a group then
> a window with the same group
>
> Regenerating group IDs when restoring a window solves this
> problem. When restoring a tab, it is always put into its group if it's
> open in any window.
>
> Bug: 1202102
> Change-Id: Id07cd92f87fd48f019e38993322d4a335f2a3801
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2911467
> Commit-Queue: Collin Baker <collinbaker@chromium.org>
> Reviewed-by: Scott Violet <sky@chromium.org>
> Reviewed-by: Charlene Yan <cyan@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#887307}

(cherry picked from commit cbe2ec51f6607fc4891bf1d44392d8264c29ab2f)

(cherry picked from commit 6a55e7b2ea6dae726430626cc7cf85517f6268b0)

Bug: 1202102, 1214197
Change-Id: Ibc6df547160e5ad23cf4f69ec5bca8329b728497
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2928804
Auto-Submit: Collin Baker <collinbaker@chromium.org>
Commit-Queue: Scott Violet <sky@chromium.org>
Reviewed-by: Scott Violet <sky@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#888641}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2965641
Auto-Submit: Emily Shack <emshack@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4472@{#1490}
Cr-Original-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2975454
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Jana Grill <janagrill@google.com>
Commit-Queue: Artem Sumaneev <asumaneev@google.com>
Owners-Override: Artem Sumaneev <asumaneev@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1534}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/65bacf7718f4da9a0ed1770b1649b813f6fdf7a7/chrome/browser/sessions/session_restore.cc
[modify] https://crrev.com/65bacf7718f4da9a0ed1770b1649b813f6fdf7a7/chrome/browser/sessions/session_restore_browsertest.cc
[modify] https://crrev.com/65bacf7718f4da9a0ed1770b1649b813f6fdf7a7/chrome/browser/sessions/tab_restore_browsertest.cc
[modify] https://crrev.com/65bacf7718f4da9a0ed1770b1649b813f6fdf7a7/components/sessions/core/tab_restore_service_helper.cc


### as...@google.com (2021-06-22)

[Empty comment from Monorail migration]

### am...@google.com (2021-07-02)

[Empty comment from Monorail migration]

### tb...@chromium.org (2021-07-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1202102?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055647)*
