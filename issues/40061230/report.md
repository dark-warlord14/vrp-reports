# Security: Forced user interaction for permission prompts by freezing the browser

| Field | Value |
|-------|-------|
| **Issue ID** | [40061230](https://issues.chromium.org/issues/40061230) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Permissions>Prompts |
| **Platforms** | Windows |
| **Reporter** | re...@gmail.com |
| **Assignee** | tu...@chromium.org |
| **Created** | 2022-10-04 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

This issue is similar to the <https://crbug.com/chromium/1371207> I reported, but I figured it was different enough for a separate report.

It is possible to trick a user into accepting a permission prompt (eg microphone/webcam) by tricking them into clicking rapidly in a window, and freezing the browser with the window.resizeBy() function. Usually, this attack is stopped because the user has to wait half a second before clicking the accept button, or else it will receive a temporary cooldown; but by freezing the browser with rapid window.resizeBy() calls, this security measure can be bypassed.

Sometimes, the permission prompt won't be shown to the user at all, and it seems like nothing happened, but this isn't reliable.

**VERSION**  

Chrome Version: 106.0.5249.91 Stable, 107.0.5304.18 Beta, 108.0.5327.0 Dev  

Operating System: Windows 10/11

**REPRODUCTION CASE**  

This PoC works only with Windows. I was able to get this bug to work with macOS intermittently, but not consistently enough to create a static PoC.

1. Open the attached poc.html file from a secure context (not file:///).
2. Click on 'Click to play!'
3. Rapidly click the cookie.
4. The window should freeze and force you into accepting the microphone permission.

If the PoC did not work correctly, open the HTML file and edit the "waitPerResize" variable to 2. If it still doesn't work, try values 4 and 6.

The demo1 video demonstrates the above PoC working perfectly with no prompt showing up at all.  

The demo2 video shows the PoC not working initially, then changing the "waitPerResize" variable to make it work so that the prompt only appears for a frame or two.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Jasper Rebane (popstonia)

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 2.1 KB)
- [demo1.mp4](attachments/demo1.mp4) (video/mp4, 969.2 KB)
- [demo2.mp4](attachments/demo2.mp4) (video/mp4, 2.1 MB)
- [poc.html](attachments/poc.html) (text/plain, 2.1 KB)
- [demo3.mp4](attachments/demo3.mp4) (video/mp4, 193.9 KB)

## Timeline

### [Deleted User] (2022-10-04)

[Empty comment from Monorail migration]

### re...@gmail.com (2022-10-05)

I can't add them myself, but I believe the affected components are: 
Blink>WindowDialog 
UI>Browser>Permissions>Prompts

### an...@chromium.org (2022-10-05)

Hi rebane2002@gmail.com! Thanks for the detailed report, PoC and videos. 
So, as I understand it, it looks like the user is tricked into clicking Accept of the permissions prompt window when they are rapidly clicking the cookie button in the game window, correct?

I have added the component suggested so we can get more eyes on this.

[Monorail components: Blink>WindowDialog UI>Browser>Permissions>Prompts]

### re...@gmail.com (2022-10-05)

Thank you, and yes, that's correct.

There seems to be a typo in my e-mail address in your comment - I thought I'd mention it just so nobody accidentally uses/copies it from there.

### an...@chromium.org (2022-10-05)

Thanks rebane2001@gmail.com and sorry for the typo.
Setting Severity to Medium based on Security FAQ example (https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md#i-can-hijack-a-user-gesture-and-trick-a-user-into-accepting-a-permission-or-downloading-a-file-is-this-a-security-bug).

masonf@, can you take a look and assign to an owner as appropriate? Thanks!

 

### [Deleted User] (2022-10-05)

[Empty comment from Monorail migration]

### ma...@chromium.org (2022-10-05)

So the repro uses setTimeout(...,1) with `window.resizeBy(1, 1);window.resizeBy(-1, -1)` to trigger a heavy workload. But I don't think there's a "bug" or something that should be done to change that really.

The issue seems to be that the 0.5s cooldown on the permissions prompt needs to be made more robust to a fully-pinned CPU. Perhaps the 0.5s timer should be started once it we get CC swap confirmation for the frame with the permissions prompt? I.e. make sure the prompt is confirmed to be visible before starting the timer?

I this this belongs only in the Browser>Permissions component, if I'm correct about the above. I'm also going to move it back to Untriaged, since it does seem like something we should try to mitigate.


[Monorail components: -Blink>WindowDialog]

### re...@gmail.com (2022-10-05)

I'd argue that being able to freeze the entire browser UI through the resizeBy() function is on its own a bug, but it might be more appropriate to make it into a separate non-security issue. I agree that the root cause of this security bug is in the Permissions component and it can be left as the only component on this issue.

I think the suggested solution (verifying the prompt is completely opaque before timer) would work great as a fix.

### an...@chromium.org (2022-10-06)

Thanks for looking at the issue masonf@. 
CCing PERMISSIONS OWNERS to take a look regarding suggested permissions prompt cooldown timer change.

### [Deleted User] (2022-10-06)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-06)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### an...@chromium.org (2022-10-07)

[Empty comment from Monorail migration]

### an...@chromium.org (2022-10-07)

Setting tungnh@chromium.org as owner assuming we have routed this issue correctly. Please re-route if necessary. Thanks!

### tu...@chromium.org (2022-10-12)

[Empty comment from Monorail migration]

### pb...@chromium.org (2022-10-18)

[Empty comment from Monorail migration]

### tu...@chromium.org (2022-10-25)

[Empty comment from Monorail migration]

### mo...@google.com (2022-10-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-10-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bb3a1c14a836b1c169a8535adeeb14e6fcd3a393

commit bb3a1c14a836b1c169a8535adeeb14e6fcd3a393
Author: Thomas Nguyen <tungnh@google.com>
Date: Thu Oct 27 18:42:05 2022

Update view shown time stamp after compositor presents a frame of view

Bug: 1371215,1371207
Change-Id: I71810e7e16df556bcfca0eea90adddc70a6d23c6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3961015
Reviewed-by: Allen Bauer <kylixrd@chromium.org>
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: Thomas Nguyen <tungnh@google.com>
Cr-Commit-Position: refs/heads/main@{#1064454}

[modify] https://crrev.com/bb3a1c14a836b1c169a8535adeeb14e6fcd3a393/ui/views/window/dialog_client_view.h
[modify] https://crrev.com/bb3a1c14a836b1c169a8535adeeb14e6fcd3a393/ui/views/bubble/bubble_frame_view.cc
[modify] https://crrev.com/bb3a1c14a836b1c169a8535adeeb14e6fcd3a393/chrome/browser/ui/views/sync/one_click_signin_dialog_view_unittest.cc
[modify] https://crrev.com/bb3a1c14a836b1c169a8535adeeb14e6fcd3a393/ui/views/window/dialog_client_view.cc
[modify] https://crrev.com/bb3a1c14a836b1c169a8535adeeb14e6fcd3a393/ui/views/input_event_activation_protector.h
[modify] https://crrev.com/bb3a1c14a836b1c169a8535adeeb14e6fcd3a393/ui/views/input_event_activation_protector.cc
[modify] https://crrev.com/bb3a1c14a836b1c169a8535adeeb14e6fcd3a393/ui/views/bubble/bubble_frame_view.h
[modify] https://crrev.com/bb3a1c14a836b1c169a8535adeeb14e6fcd3a393/ui/views/bubble/bubble_frame_view_unittest.cc
[modify] https://crrev.com/bb3a1c14a836b1c169a8535adeeb14e6fcd3a393/chrome/browser/ui/views/intent_picker_bubble_view_unittest.cc
[modify] https://crrev.com/bb3a1c14a836b1c169a8535adeeb14e6fcd3a393/chrome/browser/ui/views/bookmarks/bookmark_bar_view_test.cc
[modify] https://crrev.com/bb3a1c14a836b1c169a8535adeeb14e6fcd3a393/ui/views/window/dialog_client_view_unittest.cc
[modify] https://crrev.com/bb3a1c14a836b1c169a8535adeeb14e6fcd3a393/ui/views/window/dialog_delegate_unittest.cc
[modify] https://crrev.com/bb3a1c14a836b1c169a8535adeeb14e6fcd3a393/chrome/test/base/in_process_browser_test.cc


### tu...@chromium.org (2022-10-27)

[Empty comment from Monorail migration]

### tu...@chromium.org (2022-10-28)

[Empty comment from Monorail migration]

### tu...@chromium.org (2022-10-28)

This is Severity-Medium, I think it's not enough to request merging to 107, remove this flag

### [Deleted User] (2022-10-28)

Merge review required: M108 is already shipping to beta.

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
Owners: govind (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tu...@chromium.org (2022-10-29)

Thank you very much.

1. Why does your merge fit within the merge criteria for these milestones?
The changes have fixed a security which can be exploited in Windows following https://crbug.com/chromium/1371215#c1. The bug was triaged as Severity-Medium, which is something we should push to beta (but not strong reason enough to push to stable)

2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/chromium/src/+/3961015

3. Have the changes been released and tested on canary?
Not yet

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
We added automation test, but it would be good to be verified again, with PoC in https://crbug.com/chromium/1371215#c1



### sr...@google.com (2022-10-31)

who can verify this is working on canary as expected?

### re...@gmail.com (2022-10-31)

[Comment Deleted]

### re...@gmail.com (2022-10-31)

Disregard my last comment. It seems like my original PoC is fixed in the latest Windows Canary, but it is possible to increase the waitBefore variable to still use the lag in a problematic way.

I have attached a copy of my original poc, with the waitBefore value changed to 128, as well as a screen recording of what the vulnerability looks like now. When ran with the higher waitBefore value, it is obvious to the user, that a permissions prompt appeared, but they can still be tricked into clicking accept due to it taking just one or two extra clicks, which is not enough time to react to the prompt appearing.

### am...@chromium.org (2022-10-31)

thanks for fixing this issue tungnh@, to address https://crbug.com/chromium/1371215#c21, in the future, please simply updated security bugs as Fixed as soon as the resolving CL is landed. Sheriffbot will add the appropriate merge request/review labels based on severity and impact. :) 
Updating as fixed accordingly. 

### am...@chromium.org (2022-10-31)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-10-31)

https://crbug.com/chromium/1371207 (merged into this report as duplicate) is same issue/root cause and was reported by the same external security reporter as this report. Since merge reviews / merge threads were already happening here, merge the older issue into the newer one (which ordinarily should not be the case). 

### am...@chromium.org (2022-10-31)

reopening as I completely missed https://crbug.com/chromium/1371215#c26 while reviewing both reports
tungnh@ PTAL as it appears this issue is still reproducing based on the POC and info in https://crbug.com/chromium/1371215#c26 

### tu...@chromium.org (2022-11-02)

Interesting, the new POC showed that the parent window/widget changed its status (bound or visibility). Parent is repainted, but the clientview would not be re-painted and keeps the last "shown timestamp" which is long enough to by pass the input protector.

I think we also need to reset the timestamp if the parent is repainted


### tu...@chromium.org (2022-11-03)

@pbos, @mohsen. The new poc is showing an interesting case, the dialog is keeping a stable state of presenting (visible + drawn) while its widget (or window) is continuously changing. In this case, the input protector does not have any effect. 
It means, we might have to avoid repeated-clicking from the parent view (widget), in the same way. Looks like it might cause many UI breakages.
Or, sending some reset events from the widget (when the widget is successfully presented due to window.resize() call) to the dialog client view. Is it something we can do at current view-compositor infrastructure? What do you think about that, or do you have any idea how to mitigate it?

### tu...@chromium.org (2022-11-03)

FYI, I've just received some UI report, that in-progress dialog clicking will not work (it is really the case we cause with this change we will no longer accept clicking in the dialog if it's not drawn "stable" to the screen).

### gi...@appspot.gserviceaccount.com (2022-11-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3a79bb0104526b27c66c227fad766ba029972706

commit 3a79bb0104526b27c66c227fad766ba029972706
Author: Roger Tawa <rogerta@chromium.org>
Date: Thu Nov 03 21:00:22 2022

Revert "Update view shown time stamp after compositor presents a frame of view"

This reverts commit bb3a1c14a836b1c169a8535adeeb14e6fcd3a393.

Reason for revert: This causes problems with content analysis tab modal dialogs, see the details in b/257031944

Original change's description:
> Update view shown time stamp after compositor presents a frame of view
>
> Bug: 1371215,1371207
> Change-Id: I71810e7e16df556bcfca0eea90adddc70a6d23c6
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3961015
> Reviewed-by: Allen Bauer <kylixrd@chromium.org>
> Reviewed-by: Scott Violet <sky@chromium.org>
> Commit-Queue: Thomas Nguyen <tungnh@google.com>
> Cr-Commit-Position: refs/heads/main@{#1064454}

Bug: 1371215,1371207
Change-Id: I99840f5978acf1f99abc944c8d73fb9699fc5b41
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4003011
Reviewed-by: Scott Violet <sky@chromium.org>
Reviewed-by: Peter Boström <pbos@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Roger Tawa <rogerta@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1067219}

[modify] https://crrev.com/3a79bb0104526b27c66c227fad766ba029972706/ui/views/window/dialog_client_view.h
[modify] https://crrev.com/3a79bb0104526b27c66c227fad766ba029972706/chrome/browser/ui/views/sync/one_click_signin_dialog_view_unittest.cc
[modify] https://crrev.com/3a79bb0104526b27c66c227fad766ba029972706/ui/views/bubble/bubble_frame_view.cc
[modify] https://crrev.com/3a79bb0104526b27c66c227fad766ba029972706/ui/views/window/dialog_client_view.cc
[modify] https://crrev.com/3a79bb0104526b27c66c227fad766ba029972706/ui/views/input_event_activation_protector.h
[modify] https://crrev.com/3a79bb0104526b27c66c227fad766ba029972706/ui/views/input_event_activation_protector.cc
[modify] https://crrev.com/3a79bb0104526b27c66c227fad766ba029972706/ui/views/bubble/bubble_frame_view_unittest.cc
[modify] https://crrev.com/3a79bb0104526b27c66c227fad766ba029972706/ui/views/bubble/bubble_frame_view.h
[modify] https://crrev.com/3a79bb0104526b27c66c227fad766ba029972706/chrome/browser/ui/views/intent_picker_bubble_view_unittest.cc
[modify] https://crrev.com/3a79bb0104526b27c66c227fad766ba029972706/ui/views/window/dialog_client_view_unittest.cc
[modify] https://crrev.com/3a79bb0104526b27c66c227fad766ba029972706/chrome/browser/ui/views/bookmarks/bookmark_bar_view_test.cc
[modify] https://crrev.com/3a79bb0104526b27c66c227fad766ba029972706/ui/views/window/dialog_delegate_unittest.cc
[modify] https://crrev.com/3a79bb0104526b27c66c227fad766ba029972706/chrome/test/base/in_process_browser_test.cc


### tu...@chromium.org (2022-11-04)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-11-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0040cb967d7469250444603bdf1aa6e4d2ae822e

commit 0040cb967d7469250444603bdf1aa6e4d2ae822e
Author: Thomas Nguyen <tungnh@google.com>
Date: Mon Nov 14 09:43:50 2022

Bind dialog input protector to it's anchor widget changed event.

Bug: 1371215

Change-Id: I39b9ea632447e1e7d4ba1b1d57f67a293c751b62
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4016874
Reviewed-by: Allen Bauer <kylixrd@chromium.org>
Commit-Queue: Thomas Nguyen <tungnh@google.com>
Cr-Commit-Position: refs/heads/main@{#1070921}

[modify] https://crrev.com/0040cb967d7469250444603bdf1aa6e4d2ae822e/ui/views/bubble/bubble_dialog_delegate_view.h
[modify] https://crrev.com/0040cb967d7469250444603bdf1aa6e4d2ae822e/ui/views/window/dialog_client_view.h
[modify] https://crrev.com/0040cb967d7469250444603bdf1aa6e4d2ae822e/ui/views/bubble/bubble_frame_view.cc
[modify] https://crrev.com/0040cb967d7469250444603bdf1aa6e4d2ae822e/ui/views/bubble/bubble_frame_view.h
[modify] https://crrev.com/0040cb967d7469250444603bdf1aa6e4d2ae822e/ui/views/bubble/bubble_frame_view_unittest.cc
[modify] https://crrev.com/0040cb967d7469250444603bdf1aa6e4d2ae822e/ui/views/window/dialog_client_view.cc
[modify] https://crrev.com/0040cb967d7469250444603bdf1aa6e4d2ae822e/ui/views/bubble/bubble_dialog_delegate_view.cc
[modify] https://crrev.com/0040cb967d7469250444603bdf1aa6e4d2ae822e/ui/views/window/dialog_delegate.cc
[modify] https://crrev.com/0040cb967d7469250444603bdf1aa6e4d2ae822e/ui/views/input_event_activation_protector.h
[modify] https://crrev.com/0040cb967d7469250444603bdf1aa6e4d2ae822e/ui/views/window/dialog_delegate.h
[modify] https://crrev.com/0040cb967d7469250444603bdf1aa6e4d2ae822e/ui/views/input_event_activation_protector.cc


### tu...@chromium.org (2022-11-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-14)

[Empty comment from Monorail migration]

### tu...@chromium.org (2022-11-17)

@rebane2001@gmail.com Do you still see further configs or another way to exploit it?


### re...@gmail.com (2022-11-17)

I played around with various settings and setups for a bit, seems to be completely fixed on the latest Canary build 🔥

### tu...@chromium.org (2022-11-17)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-17)

Merge approved: your change passed merge requirements and is auto-approved for M109. Please go ahead and merge the CL to branch 5414 (refs/branch-heads/5414) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-11-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-18)

Congratulations, Jasper! The VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts and reporting this issue to us! 

### re...@gmail.com (2022-11-18)

That's awesome, thank you for the reward and great communication!

### am...@google.com (2022-11-19)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-11-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/764cdb906a602c684f70e381e90f964cd0ac78af

commit 764cdb906a602c684f70e381e90f964cd0ac78af
Author: Thomas Nguyen <tungnh@google.com>
Date: Mon Nov 21 11:42:19 2022

Bind dialog input protector to it's anchor widget changed event.

Bug: 1371215

(cherry picked from commit 0040cb967d7469250444603bdf1aa6e4d2ae822e)

Change-Id: I39b9ea632447e1e7d4ba1b1d57f67a293c751b62
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4016874
Reviewed-by: Allen Bauer <kylixrd@chromium.org>
Commit-Queue: Thomas Nguyen <tungnh@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1070921}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4030554
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Thomas Nguyen <tungnh@google.com>
Cr-Commit-Position: refs/branch-heads/5414@{#158}
Cr-Branched-From: 4417ee59d7bf6df7a9c9ea28f7722d2ee6203413-refs/heads/main@{#1070088}

[modify] https://crrev.com/764cdb906a602c684f70e381e90f964cd0ac78af/ui/views/bubble/bubble_dialog_delegate_view.h
[modify] https://crrev.com/764cdb906a602c684f70e381e90f964cd0ac78af/ui/views/window/dialog_client_view.h
[modify] https://crrev.com/764cdb906a602c684f70e381e90f964cd0ac78af/ui/views/bubble/bubble_frame_view.cc
[modify] https://crrev.com/764cdb906a602c684f70e381e90f964cd0ac78af/ui/views/bubble/bubble_frame_view.h
[modify] https://crrev.com/764cdb906a602c684f70e381e90f964cd0ac78af/ui/views/bubble/bubble_frame_view_unittest.cc
[modify] https://crrev.com/764cdb906a602c684f70e381e90f964cd0ac78af/ui/views/window/dialog_client_view.cc
[modify] https://crrev.com/764cdb906a602c684f70e381e90f964cd0ac78af/ui/views/bubble/bubble_dialog_delegate_view.cc
[modify] https://crrev.com/764cdb906a602c684f70e381e90f964cd0ac78af/ui/views/window/dialog_delegate.cc
[modify] https://crrev.com/764cdb906a602c684f70e381e90f964cd0ac78af/ui/views/input_event_activation_protector.h
[modify] https://crrev.com/764cdb906a602c684f70e381e90f964cd0ac78af/ui/views/window/dialog_delegate.h
[modify] https://crrev.com/764cdb906a602c684f70e381e90f964cd0ac78af/ui/views/input_event_activation_protector.cc


### am...@chromium.org (2023-01-09)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-10)

[Empty comment from Monorail migration]

### pg...@google.com (2023-01-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1371215?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1371207]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061230)*
