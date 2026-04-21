# Security: UAF in TabStrip

| Field | Value |
|-------|-------|
| **Issue ID** | [40053627](https://issues.chromium.org/issues/40053627) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Linux, Windows, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | tb...@chromium.org |
| **Created** | 2020-10-15 |
| **Bounty** | $15,000.00 |

## Description

**VULNERABILITY DETAILS**

|TabStrip| could be destroyed during the |Drag()|[1], TabStrip::TabDragContextImpl also will be destroyed. And the UAF will be triggered when accessing its member variables[2].

[1]. <https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/views/tabs/tab_strip.cc;l=480;drc=28adce1e4972f26aad0f9ca31daac0c4d8a1bc7e;bpv=0;bpt=0>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/views/tabs/tab_strip.cc;l=484;drc=28adce1e4972f26aad0f9ca31daac0c4d8a1bc7e;bpv=0;bpt=0>

**VERSION**  

Chrome Version: M86 stable  

Operating System: All

**REPRODUCTION CASE**  

$ python -m SimpleHTTPServer  

$ out/asan/chrome --user-data-dir=/tmp/xxxx "<http://localhost:8000/poc.html>" "about:blank"  

Click the button. Continue to drag the |about:blank| tab out of the current tab strip until the |poc.html| tab is closed.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Alpha Lab working with 360 BugCloud

## Attachments

- [asan](attachments/asan) (text/plain, 17.2 KB)
- [poc.html](attachments/poc.html) (text/plain, 176 B)
- [drag.mp4](attachments/drag.mp4) (video/mp4, 6.3 MB)
- [extension_poc.zip](attachments/extension_poc.zip) (application/octet-stream, 2.1 KB)
- [Drag2.mp4](attachments/Drag2.mp4) (video/mp4, 1.8 MB)

## Timeline

### pa...@chromium.org (2020-10-15)

dfried, can you please take a look or send this to another likely person? Thank you.

Although this is a browser UAF, which is normally severe, I am not sure it's likely to be reliably exploitable since it relies on the user to do specific actions at specific times. If you can find an automatic or otherwise more reliable way to exploit this, that would make it higher severity.

[Monorail components: UI>Browser>TabStrip]

### le...@gmail.com (2020-10-16)

Thanks for your quick reply. Since the UAF is triggered during the Tab-dragging, I think the drag behavior is inevitable. But the attacker can control the destruction timing of TabStrip by monitoring the dragging behavior. 

For example, poc1.html detects dragging behavior by discovering that its windowId has been changed, then it sends a message to poc2.html to close itself to destroy the TabStrip. The attacker can complete further exploits by spraying some blobs through poc1.html to occupy the free space, and the UAF will be triggered after dragging and dropping. 

All those operations can be done through compromised renderer or extension. I don't know whether the normal renderer can detect whether it is in a dragging state through some property similar to windowId, but if it can, it can also notify poc2.html through the webserver.

### tb...@chromium.org (2020-10-16)

I'll take this while Dana's out.

### tb...@chromium.org (2020-10-16)

I could reproduce this on my cloudtop - here's a fix: https://chromium-review.googlesource.com/c/chromium/src/+/2481074
Adding pbos@ to cc so he can see the bug while reviewing

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ca837c8423cef4cd6ad362ba830b7182cd25bf4c

commit ca837c8423cef4cd6ad362ba830b7182cd25bf4c
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Mon Oct 19 20:20:21 2020

Fix UAF in TabDragContext::ContinueDrag.

Bug: 1138911
Change-Id: I134cf9837c141e77155573574125b27e01c3728f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2481074
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Reviewed-by: Peter Boström <pbos@chromium.org>
Cr-Commit-Position: refs/heads/master@{#818610}

[modify] https://crrev.com/ca837c8423cef4cd6ad362ba830b7182cd25bf4c/chrome/browser/ui/views/tabs/tab_strip.cc


### tb...@chromium.org (2020-10-19)

Landed the fix! It should be in the next canary.

### [Deleted User] (2020-10-20)

[Empty comment from Monorail migration]

### le...@gmail.com (2020-10-23)

palmer@: Friendly ping. Could you assign a Security-Severity for this issue according to https://crbug.com/chromium/1138911#c2 for further process? Thanks.

### ad...@google.com (2020-10-26)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-26)

palmer@ I agree with https://crbug.com/chromium/1138911#c8, we need a severity here so we can assess merges etc. I'm going to go with high, because it's a browser process UaF which does not _require_ a compromised renderer, but does require user interaction.

### [Deleted User] (2020-10-26)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-26)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-26)

Requesting merge to stable M86 because latest trunk commit (818610) appears to be after stable branch point (800218).

Requesting merge to beta M87 because latest trunk commit (818610) appears to be after beta branch point (812852).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-26)

This bug requires manual review: M87's targeted beta branch promotion date has already passed, so this requires manual review
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

### ad...@google.com (2020-10-27)

Approving merge to M86, branch 4240, and M87, branch 4280, assuming things are still looking good in Canary.

### ad...@google.com (2020-10-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-10-28)

Congratulations, the VRP panel has decided to award $15,000 for this report.

### ad...@google.com (2020-10-29)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ff7615f708f8ed50f32dcb2497cd414a109c9a21

commit ff7615f708f8ed50f32dcb2497cd414a109c9a21
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Thu Oct 29 19:04:40 2020

Fix UAF in TabDragContext::ContinueDrag.

(cherry picked from commit ca837c8423cef4cd6ad362ba830b7182cd25bf4c)

Bug: 1138911
Change-Id: I134cf9837c141e77155573574125b27e01c3728f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2481074
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Reviewed-by: Peter Boström <pbos@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#818610}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2508171
Reviewed-by: Taylor Bergquist <tbergquist@chromium.org>
Cr-Commit-Position: refs/branch-heads/4280@{#895}
Cr-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}

[modify] https://crrev.com/ff7615f708f8ed50f32dcb2497cd414a109c9a21/chrome/browser/ui/views/tabs/tab_strip.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/155403e0ef9d02f952b9ee7d37c1f7be9979d6fe

commit 155403e0ef9d02f952b9ee7d37c1f7be9979d6fe
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Thu Oct 29 20:31:41 2020

Fix UAF in TabDragContext::ContinueDrag.

(cherry picked from commit ca837c8423cef4cd6ad362ba830b7182cd25bf4c)

Bug: 1138911
Change-Id: I134cf9837c141e77155573574125b27e01c3728f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2481074
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Reviewed-by: Peter Boström <pbos@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#818610}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2508349
Reviewed-by: Taylor Bergquist <tbergquist@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1354}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/155403e0ef9d02f952b9ee7d37c1f7be9979d6fe/chrome/browser/ui/views/tabs/tab_strip.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/efacff3dd8b235a3e668ba17d9580bf8167bd815

commit efacff3dd8b235a3e668ba17d9580bf8167bd815
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Fri Oct 30 19:18:30 2020

Fix UAF in TabDragContext::ContinueDrag.

(cherry picked from commit ca837c8423cef4cd6ad362ba830b7182cd25bf4c)

(cherry picked from commit 155403e0ef9d02f952b9ee7d37c1f7be9979d6fe)

Bug: 1138911
Change-Id: I134cf9837c141e77155573574125b27e01c3728f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2481074
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Reviewed-by: Peter Boström <pbos@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#818610}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2508349
Reviewed-by: Taylor Bergquist <tbergquist@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4240@{#1354}
Cr-Original-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2509042
Commit-Queue: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240_112@{#11}
Cr-Branched-From: 427c00d3874b6abcf4c4c2719768835fc3ef26d6-refs/branch-heads/4240@{#1291}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/efacff3dd8b235a3e668ba17d9580bf8167bd815/chrome/browser/ui/views/tabs/tab_strip.cc


### ad...@google.com (2020-10-30)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-30)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1138911?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053627)*
