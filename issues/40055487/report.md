# Security: UAF when extension removes tab group during drag

| Field | Value |
|-------|-------|
| **Issue ID** | [40055487](https://issues.chromium.org/issues/40055487) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>TopChrome>TabStrip, UI>Browser>TopChrome>TabStrip>TabGroups |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | so...@chromium.org |
| **Created** | 2021-04-08 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

When a tab group is being dragged, if an extension removes that group (e.g. by moving all tabs in the group to another group), a use-after-free will occur in the browser process.

**VERSION**  

Chrome Version: Tested on 91.0.4472.0 (latest asan build)  

Operating System: Windows 10, version 20H2

**REPRODUCTION CASE**

1. Install the attached extension.
2. Move at least one tab into a group and start dragging the group (by dragging the group header).
3. Once the extension detects that a tab has moved (using chrome.tabs.onMoved) and is part of a group, it will move all the tabs in the group to a new group using chrome.tabs.group. This will then cause a use-after-free in the browser process. You can verify that by going through these steps in an asan build.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [asan_output_870481.txt](attachments/asan_output_870481.txt) (text/plain, 18.2 KB)
- [background.js](attachments/background.js) (text/plain, 1.1 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 156 B)

## Timeline

### [Deleted User] (2021-04-08)

[Empty comment from Monorail migration]

### ct...@chromium.org (2021-04-08)

Thanks for the report and the ASAN logs. I've confirmed on Chrome 90 ASAN and Chrome 89 ASAN.

dfried@ this bug is similar to https://crbug.com/chromium/1196309 that I sent your way before, although it appears to have a different root cause. Could you take a look at this one as well or help redirect it to a good owner? Thanks.

I think we should also do some variant analysis for underlying architectural issues here with unexpected interactions with the chrome.tabs API.

[Monorail components: UI>Browser>TopChrome>TabStrip UI>Browser>TopChrome>TabStrip>TabGroups]

### co...@chromium.org (2021-04-08)

This actually looks similar to crbug.com/1195573, and likely has the same repro. Assigning to Taylor as well

### [Deleted User] (2021-04-09)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### co...@chromium.org (2021-04-13)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### co...@chromium.org (2021-04-21)

[Empty comment from Monorail migration]

### so...@chromium.org (2021-04-30)

[Comment Deleted]

### so...@chromium.org (2021-04-30)

[Empty comment from Monorail migration]

### so...@chromium.org (2021-04-30)

crrev.com/c/2859671

### so...@chromium.org (2021-04-30)

cc cl reviewer

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

Handling merges on https://crbug.com/chromium/1198717.

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

### ja...@google.com (2021-05-26)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-06-02)

Congratulations, David! The VRP Panel has decided to award you $10,000 for this report. (And a couple of others this week, too!) 

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

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1197146?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>TopChrome>TabStrip, UI>Browser>TopChrome>TabStrip>TabGroups]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055487)*
