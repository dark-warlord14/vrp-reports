# UAF in aura::Window

| Field | Value |
|-------|-------|
| **Issue ID** | [40062988](https://issues.chromium.org/issues/40062988) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Aura |
| **Platforms** | ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | sk...@chromium.org |
| **Created** | 2023-02-09 |
| **Bounty** | $1,000.00 |

## Description

**Steps to reproduce the problem:**  

Will attach details later.

**Problem Description:**  

Browser UAF

**Additional Comments:**

\*\*Chrome version: \*\* 112.0.5584.0 \*\*Channel: \*\* Canary

**OS:** Chrome OS

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 15.1 KB)

## Timeline

### [Deleted User] (2023-02-09)

[Empty comment from Monorail migration]

### he...@gmail.com (2023-02-09)

## Reproduction

1. Launch ChromeOS chrome with SnapGroup and Jellyroll features enabled:

./chrome --enable-features=SnapGroup,Jellyroll

2. Have any app pinned at the split screen. Click any widget (e.g., system tray, calendar, phone hub, recent downloads, etc.), we just need any widget shown.

3. Sign out, and the UAF happens.

### he...@gmail.com (2023-02-09)

The root cause may related that the DesksBarSlideAnimation may destroyed the animation/widget without removing it from the parent ChildWindow. Hence when the aura window is destroyed, it destroyed the freed child window again.

### he...@gmail.com (2023-02-09)

[Comment Deleted]

### he...@gmail.com (2023-02-14)

[Comment Deleted]

### pa...@chromium.org (2023-02-15)

[Empty comment from Monorail migration]

[Monorail components: Internals>Aura]

### [Deleted User] (2023-02-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-16)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-16)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pa...@chromium.org (2023-02-16)

[Empty comment from Monorail migration]

### sk...@chromium.org (2023-02-17)

This uaf is during sign out, which is basically chrome shutting down. Because of this, I think this is a low priority. I'm going to lower the prioerti. If someone on security feels otherwise, please bump the priority.

### sk...@chromium.org (2023-02-17)

It looks like what's happening is RootWindowController is deleting a window (because it's shutting down). Deleting the window cancels animations, which triggers DesksBarSlideAnimation  to delete itself and the window being deleted. This leads to the use-after-free.

### sk...@chromium.org (2023-02-18)

https://chromium-review.googlesource.com/c/chromium/src/+/4266053 might be a generic fix for this sort of crash. Will see what the bots think.

### sk...@chromium.org (2023-02-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-18)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-02-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/40fcb8212ee016cea8f043f07d128788bb98e6ac

commit 40fcb8212ee016cea8f043f07d128788bb98e6ac
Author: Scott Violet <sky@chromium.org>
Date: Tue Feb 21 17:33:53 2023

ash: changes to explicitly complete animations before deleting

When closing all the windows of a display (which is generally
during shutdown) ash may explicitly delete some windows. Deleting
a window implicitly cancels any animations, which may result in
notifing animation observers, which could potentially delete the
window. If this happens, we end up in a double delete.

As it's likely other places may encounter this situation, this
patch makes RootWindowController explicitly cancel animations and
then check if the window has been deleted before deleting it.
This makes a scenario like I described not result in a double
delete.

Bug: 1414278

Change-Id: I1fce11d16237c091fd66e8ea6ed110acc106709d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4266053
Commit-Queue: Scott Violet <sky@chromium.org>
Reviewed-by: Mitsuru Oshima <oshima@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1107804}

[modify] https://crrev.com/40fcb8212ee016cea8f043f07d128788bb98e6ac/ash/root_window_controller.cc


### sk...@chromium.org (2023-02-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-25)

Not requesting merge to dev (M112) because latest trunk commit (1107804) appears to be prior to dev branch point (1109224). If this is incorrect, please replace the Merge-NA-112 label with Merge-Request-112. If other changes are required to fix this bug completely, please request a merge if necessary.

Merge review required: M112 is already shipping to stable.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [112].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2023-03-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-02)

Congratulations! The VRP Panel has decided to award you $1,000 for this report of a heavily mitigated security bug. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-03-03)

[Empty comment from Monorail migration]

### ob...@google.com (2023-03-27)

Hello sky@chromium.org amyressler@google.com for this is there any review you want considered by the Release team?

### am...@chromium.org (2023-03-27)

hi obenedict@, it looks like this issue was foundin- / impacts only as far back as 112 and the fix was landed in 112, so no merge would be needed here. 
It also appears that this is a ChromeOS issue;  I am on the Chrome browser security team, so merge review conversations for issues that impact ChromeOS should probably be deferred to someone on the ChromeOS security team, such as palmer@, roxabee@, &| chmiel@ in the future. Thanks! 

### ob...@google.com (2023-03-28)

[Empty comment from Monorail migration]

### ob...@google.com (2023-03-28)

Thank you!

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1414278?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062988)*
