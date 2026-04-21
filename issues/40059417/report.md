# Security: Select dropdown able to overlap fullscreen notification toast

| Field | Value |
|-------|-------|
| **Issue ID** | [40059417](https://issues.chromium.org/issues/40059417) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>FullScreen |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | su...@gmail.com |
| **Assignee** | xi...@chromium.org |
| **Created** | 2022-04-20 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

After invoke requestFullScreen and append multiple option to select element, when browser goes into fullscreen and tab temporarily unresponsive, interestingly the fullscreen notification toast will be overlapped with the black select dropdown menu.

I able to reproduce the overlap fullscreen toast on Linux distro including Ubuntu, Debian and Arch Linux (KDE).

**VERSION**

- Chromium 100.0.4896.127 (Official Build) Arch Linux (64-bit)
- Chrome 100.0.4896.127 (Official Build) (64-bit) on Ubuntu 21.10 (X11 and Wayland)
- Chrome Dev 102.0.4997.0 (Official Build) dev (64-bit) on Ubuntu 21.10 (X11 and Wayland)

**REPRODUCTION CASE**

1. Visit attached testcase.html
2. Click anywhere on the page
3. Fullscreen notification toast will be overlapped by black select dropdown menu  
   
   (If the testcase doesn't work as on PoC video, try to change the selectElement[641811] array index to lower or higher value)

**CREDIT INFORMATION**  

Reporter credit: Irvan Kurniawan (sourc7)

## Attachments

- [testcase.html](attachments/testcase.html) (text/plain, 653 B)
- [Chrome - Select dropdown overlap fullscreen notification toast.mp4](attachments/Chrome - Select dropdown overlap fullscreen notification toast.mp4) (video/mp4, 459.5 KB)
- [testcase-cros.html](attachments/testcase-cros.html) (text/plain, 704 B)
- [Chrome OS Flex - Select dropdown overlap fullscreen notification toast.webm](attachments/Chrome OS Flex - Select dropdown overlap fullscreen notification toast.webm) (video/webm, 791.6 KB)

## Timeline

### [Deleted User] (2022-04-20)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-04-20)

avi, looks like you've handled a few of these in the past. Feel free to re-assign as appropriate.

[Monorail components: UI>Browser>FullScreen]

### av...@chromium.org (2022-04-20)

I’ve handled the Mac side, but don’t have the Linux knowledge here.

+Views, +Linux folks

### [Deleted User] (2022-04-20)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-21)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-21)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2022-04-22)

I'm not sure if it's feasible to fix this on Linux.  The "Press <esc> to exit fullscreen" bubble isn't a native window, so things like right-click menus or select dropdowns will cover it.  We can make it a native window by removing `params.parent` in [1], but we have little control over how the window manager will stack the windows.  Even less so on Wayland.

robliao@ do you have any ideas?

[1] https://source.chromium.org/chromium/chromium/src/+/main:components/fullscreen_control/fullscreen_control_popup.cc;drc=e5a38eddbdf45d7563a00d019debd11b803af1bb;l=31

### ro...@chromium.org (2022-04-24)

@thomasanderson: That sounds like Aura may have miswired TYPE_POPUP, as I would have expected that to result in a native window, even with a parent. Is this what you're seeing?

### su...@gmail.com (2022-04-25)

Here I attach the testcase that also works to overlap fullscreen toast on Chrome OS Flex (as on attached PoC video).

### th...@chromium.org (2022-04-27)

re c#8:  It's not creating a native window because of this:
https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/chrome_views_delegate_linux.cc;drc=edab26bf11e993e5069d433e8c2186ad2dee012e;l=45
It will create a NativeWidgetAura instead of a DesktopNativeWidgetAura.

Anyway, even if it is a native window, it doesn't help to solve this issue for Linux.

Also adding ChromeOS based on c#9.

### [Deleted User] (2022-05-11)

thomasanderson: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2022-05-11)

Unassigning this issue since this is infeasible to fix on Linux in the general case.

It may be possible to solve on ChromeOS by
1. Using a native window
2. Ensuring that notification windows always appear on top

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### ad...@google.com (2022-05-26)

Sorry thomasanderson@, security bugs can't lurk unassigned in the backlog. We need to drive it to conclusion:
a) a fix, even if it's multiple quarters of work and involves getting it on OKRs (if the whole Linux window structure needs redesign)
b) declare that this can't be fixed, which might require us to take extreme measures such as removing full-screen mode on Linux.
c) determine that this, somehow, can't be used as an effective spoof, for example because the black box is always so huge that it wouldn't allow an attacker to draw a realistic spoof browser.

### [Deleted User] (2022-05-26)

thomasanderson: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2022-05-26)

Re c#14: I believe this is (c) an effective spoof

Reason: The bubble being covered (which just says "press ESC to exit fullscreen") appears over the web contents.  So the page can just create an identical-looking bubble and display any text they want (which is effectively a much better spoof than covering).  Additionally, I don't think it's a spoof to cover "press ESC to exit fullscreen".  Firefox, for example, doesn't even show a message when entering fullscreen.

This is also (b) infeasible to fix on Linux (see https://crbug.com/chromium/1317904#c7).

adetaylor: please let me know if you agree and we can close this issue.


### su...@gmail.com (2022-05-26)

> c) determine that this, somehow, can't be used as an effective spoof, for example because the black box is always so huge that it wouldn't allow an attacker to draw a realistic spoof browser.

The select element width can be resized so it can only cover the fullscreen notification bubble. 

> Reason: The bubble being covered (which just says "press ESC to exit fullscreen") appears over the web contents.  So the page can just create an identical-looking bubble and display any text they want (which is effectively a much better spoof than covering).  Additionally, I don't think it's a spoof to cover "press ESC to exit fullscreen".  Firefox, for example, doesn't even show a message when entering fullscreen.

Firefox is showing fullscreen notification spoof "permission.site is now full screen" with button "Exit Fullscreen (Esc)" following the WhatWG Fullscreen API Standard https://fullscreen.spec.whatwg.org/#security-and-privacy-considerations "User agents should ensure, e.g. by means of an overlay, that the end user is aware something is displayed fullscreen...". I've also reported several full-screen notification spoofs to Firefox in the past e.g. https://www.mozilla.org/en-US/security/advisories/mfsa2022-02.

### th...@chromium.org (2022-06-13)

Security marshal here. adetaylor@ and thomasanderson@, did either of you have any followups on the latest comments (#c16 / https://crbug.com/chromium/1317904#c17)?

### ad...@google.com (2022-06-13)

Sorry I missed https://crbug.com/chromium/1317904#c16 and thanks for the ping thefrog@.

thomasanderson@ I am confused by https://crbug.com/chromium/1317904#c16. I think you're saying that this _is_ an effective spoof but you want to close the issue anyway?

I don't think we can do that. As I say in https://crbug.com/chromium/1317904#c14, the "fix" might be something really extreme such as removing full-screen mode on Linux. Is that the only option here?

### th...@chromium.org (2022-06-13)

CL: https://chromium-review.googlesource.com/c/chromium/src/+/3704421

### gi...@appspot.gserviceaccount.com (2022-06-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/df6fcb6f2ff6a8c734cfbc6b8dafc1d091bc4042

commit df6fcb6f2ff6a8c734cfbc6b8dafc1d091bc4042
Author: Tom Anderson <thomasanderson@chromium.org>
Date: Tue Jun 14 04:36:51 2022

Ensure fullscreen notification toast always appears on top

R=sky

Bug: 1317904
Change-Id: I40ef4a7f0438f12919c04dbfa574cf577c08c413
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3704421
Auto-Submit: Thomas Anderson <thomasanderson@chromium.org>
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: Thomas Anderson <thomasanderson@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1013800}

[modify] https://crrev.com/df6fcb6f2ff6a8c734cfbc6b8dafc1d091bc4042/ui/ozone/platform/x11/x11_window.cc
[modify] https://crrev.com/df6fcb6f2ff6a8c734cfbc6b8dafc1d091bc4042/ui/platform_window/platform_window_init_properties.h
[modify] https://crrev.com/df6fcb6f2ff6a8c734cfbc6b8dafc1d091bc4042/components/fullscreen_control/subtle_notification_view.cc
[modify] https://crrev.com/df6fcb6f2ff6a8c734cfbc6b8dafc1d091bc4042/ui/views/widget/desktop_aura/desktop_window_tree_host_platform.cc
[modify] https://crrev.com/df6fcb6f2ff6a8c734cfbc6b8dafc1d091bc4042/ui/ozone/platform/x11/x11_window.h
[modify] https://crrev.com/df6fcb6f2ff6a8c734cfbc6b8dafc1d091bc4042/chrome/browser/ui/views/chrome_views_delegate_linux.cc


### th...@chromium.org (2022-06-14)

This should be fixed on Linux/X11 now.  Assigning to aninak@ (author of ash/session/fullscreen_notification_bubble.cc) to investigate the issue on ChromeOS or assign to a more appropriate owner.

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-29)

aninak@, can you PTAL from an ash/ChromeOS perspective as this issue has been reassigned to you since 14 June. 
cc'ing xiyuan@ as ash/session owner to see if there might be anyone else that could/should be assigned here instead. Thanks! 

### xi...@chromium.org (2022-08-30)

Let me grab this.
https://chromium-review.googlesource.com/c/chromium/src/+/3863590

### gi...@appspot.gserviceaccount.com (2022-08-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9e6a38e9941058f837b3b25677a9166b9e5fb4de

commit 9e6a38e9941058f837b3b25677a9166b9e5fb4de
Author: Xiyuan Xia <xiyuan@google.com>
Date: Tue Aug 30 21:48:12 2022

ash: Use DragImageAndTooltipContainer for security surfaces

Use DragImageAndTooltipContainer show security surfaces on top of
top-level windows, menus (web pop-ups), and bubbles.

Bug: 1317904
Change-Id: Iff942e5776623aac8c3398f45c65648ae2421290
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3863590
Reviewed-by: Xiaoqian Dai <xdai@chromium.org>
Commit-Queue: Xiyuan Xia <xiyuan@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1041191}

[modify] https://crrev.com/9e6a38e9941058f837b3b25677a9166b9e5fb4de/ash/public/cpp/shell_window_ids.h
[modify] https://crrev.com/9e6a38e9941058f837b3b25677a9166b9e5fb4de/ash/wm/container_finder.cc


### xi...@chromium.org (2022-08-30)

Requesting for M106 merge. Not sure whether it meets the bar for M105 stable.

### am...@chromium.org (2022-08-31)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-31)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-06)

Merge review required: M106 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xi...@chromium.org (2022-09-06)

> 1. Why does your merge fit within the merge criteria for these milestones?

This bug is marked as a security bug and the CL is a security fix.

> 2. What changes specifically would you like to merge? Please link to Gerrit.

https://chromium-review.googlesource.com/c/chromium/src/+/3863590

> 3. Have the changes been released and tested on canary?

Yes. CL is included in 107.0.5272.0. ChromeOS 15085.0.0 picks up chrome 107.0.5273.0 should have the fix.

> 4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No. It is a recently found problem that a web page could hide full screen notification bubble as demonstrated in #9.

> 5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

N/A.

> 6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

No.


### [Deleted User] (2022-09-07)

[Empty comment from Monorail migration]

### sr...@google.com (2022-09-08)

Merge approved for M106 branch: pls refer to go/chrome-branches for more info

### sr...@google.com (2022-09-12)

Merge for M106 is approved, Please complete your merges asap so these changes can be included in this weeks beta release. Beta RC will be cut on Sept 13 (tuesday) at 3pm PST. 

Next week is M106 stable RC, so I would like to ensure all these CL's have good coverage before RC cut

If the merge is compelete and not linked to this bug, please drop the merge-approved-106 label 

### xi...@chromium.org (2022-09-12)

Missed the merge approve comments.
Prepared the M106 merge CL now: https://chromium-review.googlesource.com/c/chromium/src/+/3892430

### gi...@appspot.gserviceaccount.com (2022-09-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8545f1c2111547a81a4c3e958e52c0fa35926993

commit 8545f1c2111547a81a4c3e958e52c0fa35926993
Author: Xiyuan Xia <xiyuan@google.com>
Date: Mon Sep 12 18:38:42 2022

[M106] ash: Use DragImageAndTooltipContainer for security surfaces

> Use DragImageAndTooltipContainer show security surfaces on top of
> top-level windows, menus (web pop-ups), and bubbles.
>
> Bug: 1317904
> Change-Id: Iff942e5776623aac8c3398f45c65648ae2421290
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3863590
> Reviewed-by: Xiaoqian Dai <xdai@chromium.org>
> Commit-Queue: Xiyuan Xia <xiyuan@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1041191}

(cherry picked from commit 9e6a38e9941058f837b3b25677a9166b9e5fb4de)

Change-Id: Ia82af1d684e3fb375e00ae23e6d9309d55af0ee4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3892430
Reviewed-by: Xiaoqian Dai <xdai@chromium.org>
Auto-Submit: Xiyuan Xia <xiyuan@chromium.org>
Commit-Queue: Xiaoqian Dai <xdai@chromium.org>
Cr-Commit-Position: refs/branch-heads/5249@{#403}
Cr-Branched-From: 4f7bea5de862aaa52e6bde5920755a9ef9db120b-refs/heads/main@{#1036826}

[modify] https://crrev.com/8545f1c2111547a81a4c3e958e52c0fa35926993/ash/public/cpp/shell_window_ids.h
[modify] https://crrev.com/8545f1c2111547a81a4c3e958e52c0fa35926993/ash/wm/container_finder.cc


### [Deleted User] (2022-09-12)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-09-13)

[Empty comment from Monorail migration]

### rz...@google.com (2022-09-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-14)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-09-14)

1. 2 CLs https://chromium-review.googlesource.com/q/topic:5005_1317904
2. Low, only include conflicts
3. 107
4. Yes

### gm...@google.com (2022-09-20)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-21)

Marking as being included in the initial release of M106 for release notes purposes . As far as I can tell, the commit in https://crbug.com/chromium/1317904#c21 landed in 105.0.5195.52, while the commit in https://crbug.com/chromium/1317904#c26 has been merged to M106 so I think that's correct.

### am...@google.com (2022-09-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-09-22)

Congratulations, Irvan! The VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-09-23)

[Empty comment from Monorail migration]

### am...@google.com (2022-09-27)

[Empty comment from Monorail migration]

### gm...@google.com (2022-10-18)

Removing LTS labels

### [Deleted User] (2022-10-18)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2022-11-01)

[Empty comment from Monorail migration]

### gm...@google.com (2022-11-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1317904?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059417)*
