# Security: Heap-use-after-free in TabGroupModel::GetTabGroup

| Field | Value |
|-------|-------|
| **Issue ID** | [40063617](https://issues.chromium.org/issues/40063617) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>TopChrome>TabStrip>TabGroups |
| **Platforms** | Linux |
| **Reporter** | me...@gmail.com |
| **Assignee** | dl...@chromium.org |
| **Created** | 2023-03-16 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**

1. download asan-linux-release-1117591.zip and unzip
2. start a http server at the folder of poc.html
3. run `./asan-linux-release-1117591/chrome --user-data-dir=/tmp/noexist --enable-features=TabGroupsSave http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html`
4. add the first tab to TabGroup and then save it. Right click the SavedTabGroup Button to move the TabGroup to new window and repeat again.

**Problem Description:**

1. Analysis

After we move the SavedTabGroup, the TabGroup saved in `groups_`[1] will be removed but the SavedTabGroup button is still here, we could call the `MoveGroupToNewWindowPressed`[2] again to use the freed TabGroup.

```
TabGroup\* TabGroupModel::GetTabGroup(const tab_groups::TabGroupId& id) const {  
  DCHECK(ContainsTabGroup(id));  
  return groups_.find(id)->second.get();  
}  

```
```
void SavedTabGroupButton::MoveGroupToNewWindowPressed(int event_flags) {  
  if (!local_group_id_.has_value()) {  
    service_->OpenSavedTabGroupInBrowser(base::to_address(browser_), guid_);  
  }  
  
  const SavedTabGroup\* group = service_->model()->Get(guid_);  
  browser_->tab_strip_model()->delegate()->MoveGroupToNewWindow(  
      group->local_group_id().value());  
}  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/tabs/tab_group_model.cc;l=48;drc=4a8573cb240df29b0e4d9820303538fb28e31d84;bpv=0;bpt=0>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/bookmarks/saved_tab_groups/saved_tab_group_button.cc;l=281;drc=adce575cb2e089a3a1c0d326db96ae16389fc525;bpv=0;bpt=0>

2. Bisect

This problem is introduced in this commit: adce575cb2e089a3a1c0d326db96ae16389fc525  

<https://chromium-review.googlesource.com/c/chromium/src/+/4237451>

3. Suggested Patch

Change the `DCHECK` to `CHECK` in function `GetTabGroup`:

```
TabGroup\* TabGroupModel::GetTabGroup(const tab_groups::TabGroupId& id) const {  
-  DCHECK(ContainsTabGroup(id));  
+  CHECK(ContainsTabGroup(id));  
  return groups_.find(id)->second.get();  
}  

```

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/tabs/tab_group_model.cc;l=47;drc=4a8573cb240df29b0e4d9820303538fb28e31d84;bpv=0;bpt=0>

**Additional Comments:**

\*\*Chrome version: \*\* \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 12 B)
- [asan.txt](attachments/asan.txt) (text/plain, 20.4 KB)
- [video.webm](attachments/video.webm) (video/webm, 773.3 KB)

## Timeline

### [Deleted User] (2023-03-16)

[Empty comment from Monorail migration]

### ts...@chromium.org (2023-03-16)

DNR on ToT (branch position 1118117) probably because I'm not exactly following the user gestures, which gives a strong hint that it is unlikely to be able to social engineer folks into doing this in practice.  Nonetheless, assigning based on attached asan trace, and setting impact based on reporter's bisect, which indicates this is recent trunk churn.

[Monorail components: UI>Browser>TopChrome>TabStrip>TabGroups]

### [Deleted User] (2023-03-16)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dl...@chromium.org (2023-03-16)

Taking a look, thanks!

### [Deleted User] (2023-03-16)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dl...@chromium.org (2023-03-16)

Putting out a CL which fixes this issue. I boiled it down to two smaller problems:

1) If the group is closed (the button has no outline), we can open the group in a new browser window.
2) If the group is already open, find the browser which contains the tab group id, and move that group into a new window.

Removing the release blocker label since this is behind an experimental feature flag and resetting the priority to 2 for the same reason.

Thanks for catching this! 

### gi...@appspot.gserviceaccount.com (2023-03-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2f8993cd7e47e00451a08c5c8a5cba1701eefac8

commit 2f8993cd7e47e00451a08c5c8a5cba1701eefac8
Author: dljames <dljames@google.com>
Date: Thu Mar 16 18:45:02 2023

Fix move group to new window context menu UAF

Fixes a bug where clicking the "Move group to new window" button in the
Saved Tab Group button context menu would cause a use after free,
causing the browser to crash.

Change-Id: I4a71f911dde126ba57d6f9f81d65d5adf43177d0
Bug: 1424995
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4345092
Reviewed-by: Taylor Bergquist <tbergquist@chromium.org>
Commit-Queue: Darryl James <dljames@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1118246}

[modify] https://crrev.com/2f8993cd7e47e00451a08c5c8a5cba1701eefac8/chrome/browser/ui/views/bookmarks/saved_tab_groups/saved_tab_group_button.cc


### dl...@chromium.org (2023-03-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-18)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-22)

Congratulations on another one, Krace! The VRP Panel has decided to award you $3,000 for this report + follow-up via 1425338 regarding the incomplete patch, as this issue is significantly mitigated + bisect bonus. Thank you for your efforts and reporting this issue to us! 

In the future, when discovering an incomplete patch on an issue you reported, we would greatly appreciate if you could convey that in the same report rather than opening a new bug -- thank you! 

### am...@chromium.org (2023-03-22)

[Empty comment from Monorail migration]

### me...@gmail.com (2023-03-23)

> In the future, when discovering an incomplete patch on an issue you reported, we would greatly appreciate if you could convey that in the same report rather than opening a new bug 
Got it :P

### [Deleted User] (2023-03-23)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-24)

Not requesting merge to dev (M113) because latest trunk commit (1118246) appears to be prior to dev branch point (1121455). If this is incorrect, please replace the Merge-NA-113 label with Merge-Request-113. If other changes are required to fix this bug completely, please request a merge if necessary.

Merge approved: your change passed merge requirements and is auto-approved for M113. Please go ahead and merge the CL to branch 5672 (refs/branch-heads/5672) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-03-24)

fix landed in M113, no merge needed here 

### am...@google.com (2023-03-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-07-06)

Hello Krace -- we consider attachments/POCs and all analysis included with reports to be an integral part of the report (https://g.co/chrome/vrp/#investigating-and-reporting-bugs), so I've undeleted them. Please refrain from deleting these attachments (or comments with attachments) -- thank you! 

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1424995?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063617)*
