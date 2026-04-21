# Security: UAF after adding undocked DevTools tab to a group

| Field | Value |
|-------|-------|
| **Issue ID** | [40058650](https://issues.chromium.org/issues/40058650) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>TopChrome>TabStrip>TabGroups |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | dp...@chromium.org |
| **Created** | 2022-02-01 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

On Mac, the top-level "Tab" menu includes an item that allows tabs to be added to a group. That menu item is enabled for all windows except app windows. If the user adds an undocked DevTools tab to a group, an extension can then move the tab to another window and trigger a UAF in the browser process.

Additionally, if the user adds a tab in a popup window to a group, then selects the "New Tab in Group" option, an OOB read will occur in the browser process.

**VERSION**  

Chrome Version: 97.0.4692.99 (stable)  

Operating System: macOS 12.1

**REPRODUCTION CASE**  

The first demonstration shows how an extension can trigger a UAF if the user adds an undocked DevTools tab to a group:

1. Install the attached extension.
2. Open an undocked DevTools window.
3. From the top-level "Tab" menu, select the "Group tab" item.
4. Once the DevTools tab has been added to a group, the extension will move the tab to a new window. It will then crash the tab, which will trigger the same UAF described in <https://crbug.com/chromium/1194896>.

The second demonstration here shows how an OOB read will be triggered if the user adds the tab in a popup window to a group, then selects the "New tab in group" option:

1. From an existing tab, open a popup window:

open("", "", "height=200,width=200");

2. From the top-level "Tab" menu, select the "Group tab" item.
3. From the group editor bubble, select the "New tab in group" option. This should then trigger an OOB read in the browser process.

An asan log for this second case is attached. Note that the log indicates a UAF, though that's because the memory location being read happened to be previously allocated.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [manifest.json](attachments/manifest.json) (text/plain, 189 B)
- [service_worker.js](attachments/service_worker.js) (text/plain, 3.0 KB)
- [asan_output_961421_oob_read.txt](attachments/asan_output_961421_oob_read.txt) (text/plain, 15.8 KB)
- [group_tab.patch](attachments/group_tab.patch) (text/plain, 1.5 KB)

## Timeline

### [Deleted User] (2022-02-01)

[Empty comment from Monorail migration]

### de...@gmail.com (2022-02-01)

The issue here is that the "Group tab" menu item is currently enabled for all windows except app windows:

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/browser_command_controller.cc;l=1268;drc=e81f4f4f7c8c2248d4c5a270f3458c721a171c5c

That's an issue for DevTools windows, since adding a DevTools tab to a group then allows an extension to move the tab to another window and trigger a UAF, as demonstrated above.

It's also an issue for windows that don't have a tab strip and only contain a single tab (such as popup windows and undocked DevTools windows). When you select the "New Tab in Group" option, a new tab will be added to the current tab strip:

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/tabs/tab_group_editor_bubble_view.cc;l=536;drc=cf8c2149de648a9f581da5ff2adb7f5b44a978cc

When starting the navigation, Navigate will call GetBrowserAndTabForDisposition to determine an appropriate Browser for the navigation:

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/browser_navigator.cc;l=578;drc=55ae2c012d628b68bacc7c3cdbc4434b08ddfc22

If the specified Browser doesn't have a tab strip, an existing instance will be used instead or one will be created:

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/browser_navigator.cc;l=105;drc=55ae2c012d628b68bacc7c3cdbc4434b08ddfc22

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/browser_navigator.cc;l=249;drc=55ae2c012d628b68bacc7c3cdbc4434b08ddfc22

Finally, when the tab is being created, it will be added to the group that's specified:

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/tabs/tab_strip_model.cc;l=988;drc=c2fe04dcc3bcf122d9a9909b4367739b5bde33ad

However, if the tab has been created in a different window (because the original window doesn't have a tab strip), the group won't exist, which means TabGroupModel::GetTabGroup will perform an OOB read:

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/tabs/tab_group_model.cc;l=43;drc=46bbb9795fcc1934c6cfbec096764f888c4d400a

Note that this issue is specific to Mac, since that's the only platform where the top-level "Group tab" menu item is shown.

### de...@gmail.com (2022-02-01)

There's a small proposed patch attached here that makes two simple changes:

1. It updates BrowserCommandController::UpdateCommandsForTabState so that the "Group tab" menu item is only enabled for normal windows. That should work at the moment, since I don't think there are currently any other situations where a window that's not of type normal has a tab strip and allows tabs to be grouped.

However, I don't think that will hold true in the future. There's currently work underway in https://crbug.com/chromium/897314 to add support for tabbed PWAs. That would then create a situation where an app window has a tab strip and allows tabs to be grouped.

I think the proposed change should be ok for now, though, given that it's in line with some of the restrictions placed on extensions. For instance, extensions can only move groups to normal windows:

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/extensions/api/tab_groups/tab_groups_api.cc;l=262;drc=a6dba25659702847866ae636d6e334cb4096c4dc

If tabbed PWAs are supported in the future, both pieces of code will need to be updated (for example, extensions may need to be able to move groups from one tabbed PWA window to another).

2. The following DCHECK is changed to a CHECK:

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/tabs/tab_group_model.cc;l=42;drc=46bbb9795fcc1934c6cfbec096764f888c4d400a

That function unconditionally dereferences the iterator returned by find(). It makes no sense to do that or proceed in any way if the group isn't contained within the map.

### de...@gmail.com (2022-02-01)

Note that it is also possible to trigger the same OOB read described above on other platforms by going through the following steps:

1. Open an incognito window.
2. Load a chrome:// page that can be opened in incognito mode - e.g. chrome://version.
3. Add the tab to a group.
4. Ensure there are no existing chrome://settings tabs open, then drop a chrome://settings link onto the page. As the current tab is in a group, the new tab will be grouped as well. However, chrome://settings can't be opened in incognito mode, so it will instead be opened in a normal window. When the tab is created, it will be added to the group that's specified. However, as with the case above, the group won't exist in the window, which will cause an OOB read to occur.

The proposed patch will fix the security issue here as well, since the DCHECK in TabGroupModel::GetTabGroup is changed to a CHECK. However, it seems like it may be worth updating this code in future to avoid adding a tab to a group if the tab is going to be created in a different window. In general, the assumption that a tab will always be created in the window that's specified doesn't hold. There are several reasons why a tab might be created in a different window and the tab shouldn't be grouped in that case.

### de...@gmail.com (2022-02-01)

Following on from the previous comment, chrome::ConfigureTabGroupForNavigation is used to determine whether a new tab should be added to a group, and if so, which group it should be added to:

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/browser_tabstrip.cc;l=96;drc=cee531bc6bd543471e31da85dd8ffed26895f025

That method uses the specified source browser to determine whether a tab should be grouped:

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/browser_tabstrip.cc;l=105;drc=cee531bc6bd543471e31da85dd8ffed26895f025

However, when that method is called within Browser::OpenURLFromTab, it can be seen that it's done right before calling Navigate:

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/browser.cc;l=1555;drc=8015afcf8e3730c33a518bed3e7c31ba77d5a814

As noted in https://crbug.com/chromium/1292870#c2, Navigate can change the browser used for the navigation. In the case of attempting to open chrome://settings in an incognito window, AdjustNavigateParamsForURL will select a browser associated with the original profile:

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/browser_navigator.cc;l=148;drc=55ae2c012d628b68bacc7c3cdbc4434b08ddfc22

That means that chrome::ConfigureTabGroupForNavigation groups tabs based on the source browser, but Navigate can select another browser, one in which the group doesn't exist.

One simple solution might be to update Navigate to clear the group data if the target browser is changed (i.e. if source_browser != params->browser).

As mentioned in https://crbug.com/chromium/1292870#c4, the proposed patch fixes the security issue when going through this code path, but clearing the group data in Navigate when the target browser is changed would prevent a crash.

### xi...@chromium.org (2022-02-01)

Thanks for the detailed report! +dpenning@, could you take a look? It looks similar to https://crbug.com/1270539, but with a different triggering PoC.

[Monorail components: UI>Browser>TopChrome>TabStrip>TabGroups]

### [Deleted User] (2022-02-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-02)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-15)

dpenning: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-01)

dpenning: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2022-03-10)

[Empty comment from Monorail migration]

### dp...@chromium.org (2022-03-15)

Taking a look now.

### gi...@appspot.gserviceaccount.com (2022-03-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/77119fc2859decac2584ff7284090cd00d8e51ea

commit 77119fc2859decac2584ff7284090cd00d8e51ea
Author: David Pennington <dpenning@chromium.org>
Date: Mon Mar 21 19:17:17 2022

Remove group/pin tabs options for devtools windows

The tab dropdown browser commands were updated last year to only check
that the command was not being run in an app. Here we replace that check
with a more complete check of is_normal_window for pinning and grouping.

Bug: 1292870
Change-Id: I34dc1ba150d68e71987f02037d4c2f15f63224c2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3526563
Reviewed-by: Caroline Rising <corising@chromium.org>
Reviewed-by: Dana Fried <dfried@chromium.org>
Commit-Queue: David Pennington <dpenning@chromium.org>
Cr-Commit-Position: refs/heads/main@{#983438}

[modify] https://crrev.com/77119fc2859decac2584ff7284090cd00d8e51ea/chrome/browser/ui/browser_command_controller.cc


### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### dp...@chromium.org (2022-04-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-05)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-04-14)

Congratulations, David! The VRP Panel has decided to award you $5,000 for this report. While is issue is fairly mitigated by requiring an extension to be installed and some significant user interaction, we also wanted to reward you for the significant analysis you provided and the potential patch that was very close to what we employed. Thanks for your efforts and reporting is this issue to us! 

### am...@google.com (2022-04-16)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### gm...@google.com (2022-05-25)

[Empty comment from Monorail migration]

### rz...@google.com (2022-05-26)

[Empty comment from Monorail migration]

### rz...@google.com (2022-05-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-27)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-05-27)

1. Just https://crrev.com/c/3669246
2. Low, no conflicts
3. Merged to main on Mar 21
4. Yes

### gm...@google.com (2022-05-31)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-06-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8d48a1a542ab65c9d73fddce4fee629b0783cf28

commit 8d48a1a542ab65c9d73fddce4fee629b0783cf28
Author: David Pennington <dpenning@chromium.org>
Date: Wed Jun 01 11:10:06 2022

[M96-LTS] Remove group/pin tabs options for devtools windows

The tab dropdown browser commands were updated last year to only check
that the command was not being run in an app. Here we replace that check
with a more complete check of is_normal_window for pinning and grouping.

(cherry picked from commit 77119fc2859decac2584ff7284090cd00d8e51ea)

Bug: 1292870
Change-Id: I34dc1ba150d68e71987f02037d4c2f15f63224c2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3526563
Commit-Queue: David Pennington <dpenning@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#983438}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3669246
Owners-Override: Simon Hangl <simonha@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Simon Hangl <simonha@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1640}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/8d48a1a542ab65c9d73fddce4fee629b0783cf28/chrome/browser/ui/browser_command_controller.cc


### rz...@google.com (2022-06-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1292870?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058650)*
