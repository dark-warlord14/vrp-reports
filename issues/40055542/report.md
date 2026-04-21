# Security: OOB write after extension pins tab during drag

| Field | Value |
|-------|-------|
| **Issue ID** | [40055542](https://issues.chromium.org/issues/40055542) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | so...@chromium.org |
| **Created** | 2021-04-13 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

When the user is dragging a tab that was initially in a group, an extension can mark the tab as pinned. If the drag is then cancelled, the tab will be moved back into its original group, resulting in a tab that's both pinned and in a group. Moving the group to a different index will then also move the pinned tab. This then breaks the constraint that pinned tabs are always at the start of the tab strip. Finally, attempting to move the pinned tab to a different index will result in an out-of-bounds write in the browser process.

**VERSION**  

Chrome Version: Tested on 92.0.4477.0 (latest asan build)  

Operating System: Windows 10, version 20H2

**REPRODUCTION CASE**

1. Install the attached extension.
2. Move a tab into a new group, then start dragging the tab within its tab strip.
3. Once the extension detects that a tab has been moved (using chrome.tabs.onMoved), the extension will mark the tab as pinned and navigate it.  
   
   On Windows, the tab will be navigated to "mailto:". This will cause the drag to be cancelled, at least on Windows 10, when the application chooser dialog is shown.  
   
   On other platforms, the tab will be navigated to about:blank (simply to make it easy to tell when the drag should be cancelled) and you'll need to manually cancel the drag by pressing ESC.  
   
   The updated tab will now be both pinned and in a group.
4. Five seconds later, the extension will call chrome.tabGroups.move to move the group to index 1. This will move the pinned tab, meaning that there's now a pinned tab that's not at the start of the tab strip.
5. Finally, the extension will use chrome.tabs.move to move the pinned tab to index 0. This will result in an OOB write in the browser process.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [asan_output_872117.txt](attachments/asan_output_872117.txt) (text/plain, 11.3 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 196 B)
- [service_worker.js](attachments/service_worker.js) (text/plain, 1.1 KB)

## Timeline

### [Deleted User] (2021-04-13)

[Empty comment from Monorail migration]

### de...@gmail.com (2021-04-13)

Ultimately, the end result of this issue is similar to the result described in https://crbug.com/chromium/1196309. However. the core problem here is that when a drag is cancelled, the group of each dragged tab is restored, regardless of whether or not any of the tabs have been pinned. That's something that's done at the end of TabDragController::RevertDragAt:

https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/views/tabs/tab_drag_controller.cc;l=1742;drc=a9cc926063ef9fad68351d9c24d7e26b00c634c7

In this case, the to_position value passed to TabStripModel::MoveWebContentsAtImpl is -1 and the element is written just before the start of the contents_data_ vector.

### es...@chromium.org (2021-04-15)

Triaging to match https://crbug.com/chromium/1196309 and friends

[Monorail components: UI>Browser>TabStrip]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### co...@chromium.org (2021-04-21)

[Empty comment from Monorail migration]

### ad...@google.com (2021-04-29)

collinbaker@ could we have an update here? This is getting fairly old for a High severity security bug.

### co...@chromium.org (2021-04-29)

solomonkinard@ is working on https://crbug.com/chromium/1196309 which is similar. We are waiting on that fix before proceeding with this.

### so...@chromium.org (2021-04-30)

[Empty comment from Monorail migration]

### so...@chromium.org (2021-05-05)

crrev.com/c/2873364

### so...@chromium.org (2021-05-12)

cc cl reviewer

### ka...@chromium.org (2021-05-12)

We decided to prevent the extensions code from modifying the tab strip while a tab drag was in progress to prevent these security issues. (Another CL: https://chromium-review.googlesource.com/c/chromium/src/+/2891080)

Can we add (or have we already added) some validation to the tab strip code as well to ensure clients don't modify the tab strip while a tab drag is in progress? Said differently, even if the extensions code tries to modify the tab strip during a tab drag, it shouldn't result in an out-of-bounds and the tab strip code should handle it gracefully (either the operation should be a no-op or result in a DCHECK failure I think, with the former preferred IMO).

### so...@chromium.org (2021-05-13)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-05-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/33109f1824b9ae3d488b7372f9aca68f611be606

commit 33109f1824b9ae3d488b7372f9aca68f611be606
Author: Solomon Kinard <solomonkinard@chromium.org>
Date: Mon May 17 19:28:43 2021

[Extensions][Tabs] Ensure tab strip is editable before editing

Bug: 1198717,1197146,1197888,1196309,1202598
Change-Id: Ic51669a7f7b17a35cd2c0ed018abcfeddf068a26
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2891080
Commit-Queue: Solomon Kinard <solomonkinard@chromium.org>
Reviewed-by: Taylor Bergquist <tbergquist@chromium.org>
Reviewed-by: Karan Bhatia <karandeepb@chromium.org>
Cr-Commit-Position: refs/heads/master@{#883567}

[modify] https://crrev.com/33109f1824b9ae3d488b7372f9aca68f611be606/chrome/browser/extensions/api/tab_groups/tab_groups_api.cc
[modify] https://crrev.com/33109f1824b9ae3d488b7372f9aca68f611be606/chrome/browser/extensions/api/tab_groups/tab_groups_api_unittest.cc
[modify] https://crrev.com/33109f1824b9ae3d488b7372f9aca68f611be606/chrome/browser/extensions/api/tabs/tabs_api.cc
[modify] https://crrev.com/33109f1824b9ae3d488b7372f9aca68f611be606/chrome/browser/extensions/api/tabs/tabs_api_unittest.cc
[modify] https://crrev.com/33109f1824b9ae3d488b7372f9aca68f611be606/chrome/browser/extensions/api/tabs/tabs_constants.cc
[modify] https://crrev.com/33109f1824b9ae3d488b7372f9aca68f611be606/chrome/browser/extensions/api/tabs/tabs_constants.h
[modify] https://crrev.com/33109f1824b9ae3d488b7372f9aca68f611be606/chrome/browser/extensions/extension_tab_util.cc
[modify] https://crrev.com/33109f1824b9ae3d488b7372f9aca68f611be606/chrome/browser/extensions/extension_tab_util.h
[modify] https://crrev.com/33109f1824b9ae3d488b7372f9aca68f611be606/chrome/test/base/test_browser_window.cc
[modify] https://crrev.com/33109f1824b9ae3d488b7372f9aca68f611be606/chrome/test/base/test_browser_window.h


### so...@chromium.org (2021-05-17)

crrev.com/c/2891080 merged.

### [Deleted User] (2021-05-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-18)

Requesting merge to stable M90 because latest trunk commit (883567) appears to be after stable branch point (857950).

Requesting merge to beta M91 because latest trunk commit (883567) appears to be after beta branch point (965).

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

Approving merge to M91. Please merge to branch 4472. M91 stable cut is today, so this will almost certainly miss the initial release of M91, but we'll pick it up in the first stable refresh.

### so...@chromium.org (2021-05-18)

Thanks.

### gi...@appspot.gserviceaccount.com (2021-05-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f5ae8693fcb042797de12b6b9cc055da0090a80a

commit f5ae8693fcb042797de12b6b9cc055da0090a80a
Author: Solomon Kinard <solomonkinard@chromium.org>
Date: Wed May 19 00:09:39 2021

[M91][Extensions][Tabs] Ensure tab strip is editable before editing

(cherry picked from commit 33109f1824b9ae3d488b7372f9aca68f611be606)

Bug: 1198717,1197146,1197888,1196309,1202598
Change-Id: Ic51669a7f7b17a35cd2c0ed018abcfeddf068a26
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2891080
Commit-Queue: Solomon Kinard <solomonkinard@chromium.org>
Reviewed-by: Taylor Bergquist <tbergquist@chromium.org>
Reviewed-by: Karan Bhatia <karandeepb@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#883567}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2904568
Auto-Submit: Solomon Kinard <solomonkinard@chromium.org>
Cr-Commit-Position: refs/branch-heads/4472@{#1169}
Cr-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}

[modify] https://crrev.com/f5ae8693fcb042797de12b6b9cc055da0090a80a/chrome/browser/extensions/api/tab_groups/tab_groups_api.cc
[modify] https://crrev.com/f5ae8693fcb042797de12b6b9cc055da0090a80a/chrome/browser/extensions/api/tab_groups/tab_groups_api_unittest.cc
[modify] https://crrev.com/f5ae8693fcb042797de12b6b9cc055da0090a80a/chrome/browser/extensions/api/tabs/tabs_api.cc
[modify] https://crrev.com/f5ae8693fcb042797de12b6b9cc055da0090a80a/chrome/browser/extensions/api/tabs/tabs_api_unittest.cc
[modify] https://crrev.com/f5ae8693fcb042797de12b6b9cc055da0090a80a/chrome/browser/extensions/api/tabs/tabs_constants.cc
[modify] https://crrev.com/f5ae8693fcb042797de12b6b9cc055da0090a80a/chrome/browser/extensions/api/tabs/tabs_constants.h
[modify] https://crrev.com/f5ae8693fcb042797de12b6b9cc055da0090a80a/chrome/browser/extensions/extension_tab_util.cc
[modify] https://crrev.com/f5ae8693fcb042797de12b6b9cc055da0090a80a/chrome/browser/extensions/extension_tab_util.h
[modify] https://crrev.com/f5ae8693fcb042797de12b6b9cc055da0090a80a/chrome/test/base/test_browser_window.cc
[modify] https://crrev.com/f5ae8693fcb042797de12b6b9cc055da0090a80a/chrome/test/base/test_browser_window.h


### gi...@appspot.gserviceaccount.com (2021-05-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7260804a2f0823fdec95e69de0e449bb9fed1f35

commit 7260804a2f0823fdec95e69de0e449bb9fed1f35
Author: Solomon Kinard <solomonkinard@chromium.org>
Date: Wed May 19 19:41:28 2021

[Extensions][Tabs] Include error message if not model isn't editable

See crrev.com/c/2904568.

Bug: 1198717,1197146,1197888,1196309,1202598
Change-Id: Idc6f1a1e336e08926de75226debcff799d703d00
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2903572
Reviewed-by: Karan Bhatia <karandeepb@chromium.org>
Commit-Queue: Solomon Kinard <solomonkinard@chromium.org>
Cr-Commit-Position: refs/heads/master@{#884626}

[modify] https://crrev.com/7260804a2f0823fdec95e69de0e449bb9fed1f35/chrome/browser/extensions/api/tabs/tabs_api.cc


### ad...@google.com (2021-05-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2021-05-24)

[Empty comment from Monorail migration]

### ja...@google.com (2021-05-26)

[Empty comment from Monorail migration]

### ja...@google.com (2021-05-26)

Not applicable to LTS since tab groups API was added after LTS branch. 

### ja...@google.com (2021-05-26)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-06-03)

Congrats, David on another one! The VRP panel has decided to award you $10,000 for this report. 

### am...@google.com (2021-06-04)

[Empty comment from Monorail migration]

### as...@google.com (2021-06-07)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-08)

[Empty comment from Monorail migration]

### gi...@google.com (2021-06-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-06-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7aeab825dc9b93ba302d1c124c572213c4967b53

commit 7aeab825dc9b93ba302d1c124c572213c4967b53
Author: Solomon Kinard <solomonkinard@chromium.org>
Date: Wed Jun 09 15:54:57 2021

[M90-LTS][Extensions][Tabs] Ensure tab strip is editable before editing

(cherry picked from commit 33109f1824b9ae3d488b7372f9aca68f611be606)

(cherry picked from commit f5ae8693fcb042797de12b6b9cc055da0090a80a)

Bug: 1198717,1197146,1197888,1196309,1202598
Change-Id: Ic51669a7f7b17a35cd2c0ed018abcfeddf068a26
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2891080
Commit-Queue: Solomon Kinard <solomonkinard@chromium.org>
Reviewed-by: Taylor Bergquist <tbergquist@chromium.org>
Reviewed-by: Karan Bhatia <karandeepb@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#883567}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2904568
Auto-Submit: Solomon Kinard <solomonkinard@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4472@{#1169}
Cr-Original-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2944872
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Artem Sumaneev <asumaneev@google.com>
Owners-Override: Artem Sumaneev <asumaneev@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1503}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/7aeab825dc9b93ba302d1c124c572213c4967b53/chrome/browser/extensions/api/tab_groups/tab_groups_api.cc
[modify] https://crrev.com/7aeab825dc9b93ba302d1c124c572213c4967b53/chrome/browser/extensions/api/tab_groups/tab_groups_api_unittest.cc
[modify] https://crrev.com/7aeab825dc9b93ba302d1c124c572213c4967b53/chrome/browser/extensions/api/tabs/tabs_api.cc
[modify] https://crrev.com/7aeab825dc9b93ba302d1c124c572213c4967b53/chrome/browser/extensions/api/tabs/tabs_api_unittest.cc
[modify] https://crrev.com/7aeab825dc9b93ba302d1c124c572213c4967b53/chrome/browser/extensions/api/tabs/tabs_constants.cc
[modify] https://crrev.com/7aeab825dc9b93ba302d1c124c572213c4967b53/chrome/browser/extensions/api/tabs/tabs_constants.h
[modify] https://crrev.com/7aeab825dc9b93ba302d1c124c572213c4967b53/chrome/browser/extensions/extension_tab_util.cc
[modify] https://crrev.com/7aeab825dc9b93ba302d1c124c572213c4967b53/chrome/browser/extensions/extension_tab_util.h
[modify] https://crrev.com/7aeab825dc9b93ba302d1c124c572213c4967b53/chrome/test/base/test_browser_window.cc
[modify] https://crrev.com/7aeab825dc9b93ba302d1c124c572213c4967b53/chrome/test/base/test_browser_window.h


### as...@google.com (2021-06-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1198717?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055542)*
