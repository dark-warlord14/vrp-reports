# Security: UAF when WebContents being dragged is destroyed

| Field | Value |
|-------|-------|
| **Issue ID** | [40055439](https://issues.chromium.org/issues/40055439) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions, UI>Browser>TopChrome>TabStrip |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | tb...@chromium.org |
| **Created** | 2021-04-03 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

When a tab is being dragged by the user, an extension can discard it using the chrome.tabs API. This may then result in a use-after-free in the browser process when the drag is finished and the freed WebContents are accessed.

The issue can also be triggered by a webpage that activates a portal during a drag (note that the portal functionality is currently behind a flag).

**VERSION**  

Chrome Version: Tested on 89.0.4389.114 (stable) and 91.0.4467.0 (latest asan build)  

Operating System: Windows 10, version 20H2

**REPRODUCTION CASE**  

This demonstrates that an extension can trigger the UAF.

1. Install the attached extension.
2. Start dragging a tab. When the extension detects that a tab has moved (using chrome.tabs.onMoved) or has been attached to another window (using chrome.tabs.onAttached), it will discard the tab two seconds later.
3. Wait until the tab has been discarded, then end the drag. The exact effect depends on how the drag is ended:

- If the tab is dragged to a new window and the drag is completed or cancelled, a use-after-free will occur in the browser process.
- If the drag is cancelled when the tab is still in its original tab strip, an invalid vector element (index -1) will be accessed in TabStripModel::IsTabPinned.
- If the tab is dropped within its original tab strip, it will be moved to index 0, but won't otherwise trigger any errors, as far as I'm aware.

You can verify the above by going through these steps in an asan build.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [asan_output_869045.txt](attachments/asan_output_869045.txt) (text/plain, 17.9 KB)
- [background.js](attachments/background.js) (text/plain, 292 B)
- [manifest.json](attachments/manifest.json) (text/plain, 150 B)
- [index.html](attachments/index.html) (text/plain, 408 B)

## Timeline

### [Deleted User] (2021-04-03)

[Empty comment from Monorail migration]

### de...@gmail.com (2021-04-03)

As mentioned in the summary, the issue can also be triggered by a webpage that activates a portal. As portals are currently experimental, you'll first need to enable the following flag:

chrome://flags/#enable-portals

Then go through the following steps:

1. Download index.html into a directory and start a web server:

python3 -m http.server 8080

2. Navigate to:

http://localhost:8080/index.html

3. Click anywhere on the page, then then start dragging the tab.
4. Four seconds after being clicked, the page will activate a portal it embeds.
5. Wait until the portal has been activated, then end the drag. The possible effects are the same as those listed above.

### de...@gmail.com (2021-04-03)

The core issue here is that TabDragController holds a few pieces of information on each item being dragged, one of which is a WebContents pointer:

https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/views/tabs/tab_drag_controller.h;l=229;drc=fb3e4bd6d00d552482f121dbad255c903ed4bf78

When an extension calls chrome.tabs.discard or a web page activates a portal, the associated WebContents is destroyed.

When a tab is dragged to another window, the TabDragController will access the WebContents for the source view that the user started dragging:

https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/views/tabs/tab_drag_controller.cc;l=769;drc=2dec91b522928e8e2c12ead897d491d27a6b7f6a

This then results in a use-after-free.

### dr...@chromium.org (2021-04-05)

Thank you for the report and the root cause analysis. This does reproduce as claimed. Triaging as medium due to the requirement of installing an extension (since portals are not enabled by default). 

connily@, cyan@ - can you take a look?

[Monorail components: UI>Browser>TabStrip]

### [Deleted User] (2021-04-06)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### co...@chromium.org (2021-04-08)

Passing to Taylor for now, since Taylor has looked into several close-while-dragging scenarios.

[Monorail components: -UI>Browser>TabStrip Platform>Extensions UI>Browser>TopChrome>TabStrip]

### [Deleted User] (2021-04-17)

tbergquist: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-04-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/06f331563e7c767767600c34cc0c0b1d721d24d1

commit 06f331563e7c767767600c34cc0c0b1d721d24d1
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Wed Apr 21 19:21:20 2021

Handle replacing WebContents during a drag session.

Bug: 1195573
Change-Id: I5091bb83929e5a618a6949c2189cdd5287535b68
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2837478
Reviewed-by: Caroline Rising <corising@chromium.org>
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Cr-Commit-Position: refs/heads/master@{#874810}

[modify] https://crrev.com/06f331563e7c767767600c34cc0c0b1d721d24d1/chrome/browser/ui/views/tabs/tab_drag_controller.cc
[modify] https://crrev.com/06f331563e7c767767600c34cc0c0b1d721d24d1/chrome/browser/ui/views/tabs/tab_drag_controller.h


### tb...@chromium.org (2021-04-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-22)

Requesting merge to beta M90 because latest trunk commit (874810) appears to be after beta branch point (857950).

Requesting merge to future beta M91 because latest trunk commit (874810) appears to be after future beta branch point (870763).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-22)

This bug requires manual review: M91's targeted beta branch promotion date has already passed, so this requires manual review
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
Owners: benmason@(Android), bindusuvarna@(iOS), kbleicher@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tb...@chromium.org (2021-04-22)

1) yes
2) https://chromium-review.googlesource.com/c/chromium/src/+/2837478
3) I verified the fix locally as I was working on it, not on tip of tree
4) That's up to security people but I think this has the right labels so I'll leave that up to their process
5) They fix a security issue
6) No
7) N/A

### sr...@google.com (2021-04-23)

+adetaylor@ for review

### ad...@chromium.org (2021-04-23)

Approving merge to M91, branch 4472.

We'll wait a while to approve to M90. As it's medium severity I'm comfortable waiting for this to get some bake time.

### am...@chromium.org (2021-04-23)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-04-23)

[Comment Deleted]

### am...@chromium.org (2021-04-23)

Note for myself/VRP: https://crbug.com/chromium/1193362 has been merged into this issue since the work was done and fix landed via this issue. However, this issue is a duplicate of the earlier reported 1193362, which should be the issue that is considered for VRP reward and credit. 

Apologies derceg@ that is just now being discovered by us!

### [Deleted User] (2021-04-24)

The older reward-topanel https://crbug.com/chromium/1193362 has been merged into this one. Please manually review this issue to see if the duplicate is potentially eligible for a reward.



### [Deleted User] (2021-04-27)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2021-04-27)

[Bulk Edit] Your change has been approved for M91 Branch. Please go ahead and merge the CL to branch 4472 (/refs/branch-heads/4472) manually, asap so that it would be part of tomorrow's Beta release.

### gi...@appspot.gserviceaccount.com (2021-04-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6c21f5f659a5d3107e56cbb29a1da7aa37a6374b

commit 6c21f5f659a5d3107e56cbb29a1da7aa37a6374b
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Tue Apr 27 20:19:06 2021

Handle replacing WebContents during a drag session.

(cherry picked from commit 06f331563e7c767767600c34cc0c0b1d721d24d1)

Bug: 1195573
Change-Id: I5091bb83929e5a618a6949c2189cdd5287535b68
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2837478
Reviewed-by: Caroline Rising <corising@chromium.org>
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#874810}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2854999
Auto-Submit: Taylor Bergquist <tbergquist@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4472@{#482}
Cr-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}

[modify] https://crrev.com/6c21f5f659a5d3107e56cbb29a1da7aa37a6374b/chrome/browser/ui/views/tabs/tab_drag_controller.cc
[modify] https://crrev.com/6c21f5f659a5d3107e56cbb29a1da7aa37a6374b/chrome/browser/ui/views/tabs/tab_drag_controller.h


### am...@google.com (2021-04-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-04-28)

Hi David! While it was unfortunate that your report was the duplicate of an earlier reported one, the VRP Panel would like to extend to you a $1000 award to thank you for efforts (and the additional exploitation scenarios and POCs) and communications as the team worked towards repro and fix of this issue. Thank you!! 

### am...@google.com (2021-04-30)

[Empty comment from Monorail migration]

### ad...@google.com (2021-05-04)

Approving merge to M90, branch 4430. Please merge by EOD PST Thursday for inclusion in next week's security refresh.

### gi...@appspot.gserviceaccount.com (2021-05-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/147017e2f91ab2650cc3f0cce583dbe1011a4466

commit 147017e2f91ab2650cc3f0cce583dbe1011a4466
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Tue May 04 19:41:44 2021

Handle replacing WebContents during a drag session.

(cherry picked from commit 06f331563e7c767767600c34cc0c0b1d721d24d1)

Bug: 1195573
Change-Id: I5091bb83929e5a618a6949c2189cdd5287535b68
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2837478
Reviewed-by: Caroline Rising <corising@chromium.org>
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#874810}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2872545
Auto-Submit: Taylor Bergquist <tbergquist@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1392}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/147017e2f91ab2650cc3f0cce583dbe1011a4466/chrome/browser/ui/views/tabs/tab_drag_controller.cc
[modify] https://crrev.com/147017e2f91ab2650cc3f0cce583dbe1011a4466/chrome/browser/ui/views/tabs/tab_drag_controller.h


### am...@chromium.org (2021-05-07)

While the fix in this issue is shipping in this release, note to CVE and credit https://crbug.com/chromium/1193362 

### vs...@google.com (2021-05-10)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-05-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/90edb165d13540a41cc45d82c06c2ef4cca7bc7c

commit 90edb165d13540a41cc45d82c06c2ef4cca7bc7c
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Wed May 12 11:40:29 2021

Handle replacing WebContents during a drag session.

(cherry picked from commit 06f331563e7c767767600c34cc0c0b1d721d24d1)

(cherry picked from commit 147017e2f91ab2650cc3f0cce583dbe1011a4466)

Bug: 1195573
Change-Id: I5091bb83929e5a618a6949c2189cdd5287535b68
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2837478
Reviewed-by: Caroline Rising <corising@chromium.org>
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#874810}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2872545
Auto-Submit: Taylor Bergquist <tbergquist@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Original-Commit-Position: refs/branch-heads/4430@{#1392}
Cr-Original-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2884073
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4430_101@{#25}
Cr-Branched-From: 3e9034a21f4b1f6707146b1309e001c3321ab48a-refs/branch-heads/4430@{#1364}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/90edb165d13540a41cc45d82c06c2ef4cca7bc7c/chrome/browser/ui/views/tabs/tab_drag_controller.cc
[modify] https://crrev.com/90edb165d13540a41cc45d82c06c2ef4cca7bc7c/chrome/browser/ui/views/tabs/tab_drag_controller.h


### gi...@google.com (2021-05-12)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-05-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2accab56152b3890473024585376ab231268c015

commit 2accab56152b3890473024585376ab231268c015
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Wed May 12 18:35:04 2021

Handle replacing WebContents during a drag session.

(cherry picked from commit 06f331563e7c767767600c34cc0c0b1d721d24d1)

Bug: 1195573
Change-Id: I5091bb83929e5a618a6949c2189cdd5287535b68
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2837478
Reviewed-by: Caroline Rising <corising@chromium.org>
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#874810}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2883761
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1638}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/2accab56152b3890473024585376ab231268c015/chrome/browser/ui/views/tabs/tab_drag_controller.cc
[modify] https://crrev.com/2accab56152b3890473024585376ab231268c015/chrome/browser/ui/views/tabs/tab_drag_controller.h


### tb...@google.com (2021-07-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1195573?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>Extensions, UI>Browser>TopChrome>TabStrip]
[Monorail mergedwith: crbug.com/chromium/1193362, crbug.com/chromium/1215988]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055439)*
