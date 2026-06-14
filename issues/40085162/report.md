# Chrome for Android - Quickly entering and exiting fullscreen allows for URL Spoofing

| Field | Value |
|-------|-------|
| **Issue ID** | [40085162](https://issues.chromium.org/issues/40085162) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>FullScreen, UI>Browser>Omnibox |
| **Platforms** | Android |
| **Reporter** | he...@gmail.com |
| **Assignee** | te...@chromium.org |
| **Created** | 2016-08-22 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

If you quickly enter and exit fullscreen, the omnibox slides up  

automatically and then disappears (without any warning). This allows the attacker to insert an image of a fake omnibox in its place, thus spoofing it.

**VERSION**  

I tested on:  

Chrome 52.0.2743.98 / Android 6.0.1  

Chrome 52.0.2743.98 / Android 4.3.0  

Chrome 52.0.2743.98 / Android 4.4.2

**REPRODUCTION CASE**

1. Access <http://lbherrera.me/fullspoof.html>
2. Click on the "Sign in" button.
3. The image of a fake omnibox and login page will show up.

\* Given I use an image to spoof all the page, because of different screen resolution the image may be misaligned. A dedicated attacker could easily fix this, as he would know the users' screen resolution.

## Timeline

### ji...@chromium.org (2016-08-22)

That's a nice spoof! Definitely reproducible on Android. 
Let me route it to the right team to see if this is an known issue. 
Thanks for reporting!

+spqchan@, could you help me triage this bug since you're quite active in both components?

Thanks!

[Monorail components: UI>Browser>FullScreen UI>Browser>Omnibox]

### ji...@chromium.org (2016-08-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2016-08-23)

[Empty comment from Monorail migration]

### sp...@chromium.org (2016-08-24)

Sorry jialiul, while I'm active in both the omnibox and fullscreen, I'm only active on Mac. I have no idea how to triage for Android

### ji...@chromium.org (2016-08-24)

+tedchoc@, could you help triage this issue since you have worked on omnibox related issues on Android? Please feel free to suggest other owner. Thanks!

### sh...@chromium.org (2016-08-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-24)

[Empty comment from Monorail migration]

### te...@chromium.org (2016-08-24)

Yeah, I'll take a look at this.

### sh...@chromium.org (2016-09-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-08)

tedchoc: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-09-22)

tedchoc: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2016-09-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a55c2fdf48fb379f994e21768f517b53837ea663

commit a55c2fdf48fb379f994e21768f517b53837ea663
Author: tedchoc <tedchoc@chromium.org>
Date: Tue Sep 27 06:11:07 2016

Keep top controls visible if SHOW is called right after HIDE.

Currently, we early exit if the visibility amount matches our
desired ending amount.  But when you set HIDDEN as the current,
it will start an animation, and a immediate call to SHOWN will
see that the ending condition is met and return, but does not
clear the animation.

Now, clear the animation if the current value matches our
desired ending value to ensure it doesn't move.

BUG=639702
CQ_INCLUDE_TRYBOTS=master.tryserver.blink:linux_precise_blink_rel

Review-Url: https://codereview.chromium.org/2372713004
Cr-Commit-Position: refs/heads/master@{#421125}

[modify] https://crrev.com/a55c2fdf48fb379f994e21768f517b53837ea663/cc/input/top_controls_manager.cc
[modify] https://crrev.com/a55c2fdf48fb379f994e21768f517b53837ea663/cc/input/top_controls_manager_unittest.cc


### te...@chromium.org (2016-09-27)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-09-27)

Your change meets the bar and is auto-approved for M54 (branch: 2840)

### bu...@chromium.org (2016-09-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0f76844ee3219d0e3990216b5dd657aac4d36f7b

commit 0f76844ee3219d0e3990216b5dd657aac4d36f7b
Author: Ted Choc <tedchoc@google.com>
Date: Tue Sep 27 17:05:25 2016

Keep top controls visible if SHOW is called right after HIDE.

Currently, we early exit if the visibility amount matches our
desired ending amount.  But when you set HIDDEN as the current,
it will start an animation, and a immediate call to SHOWN will
see that the ending condition is met and return, but does not
clear the animation.

Now, clear the animation if the current value matches our
desired ending value to ensure it doesn't move.

BUG=639702
CQ_INCLUDE_TRYBOTS=master.tryserver.blink:linux_precise_blink_rel

Review URL: https://codereview.chromium.org/2371223002 .

Review-Url: https://codereview.chromium.org/2372713004
Cr-Original-Commit-Position: refs/heads/master@{#421125}
Cr-Commit-Position: refs/branch-heads/2840@{#546}
Cr-Branched-From: 1ae106dbab4bddd85132d5b75c670794311f4c57-refs/heads/master@{#414607}

[modify] https://crrev.com/0f76844ee3219d0e3990216b5dd657aac4d36f7b/cc/input/top_controls_manager.cc
[modify] https://crrev.com/0f76844ee3219d0e3990216b5dd657aac4d36f7b/cc/input/top_controls_manager_unittest.cc


### te...@chromium.org (2016-09-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-28)

[Empty comment from Monorail migration]

### aw...@google.com (2016-10-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-15)

Congratulations - $1,000 for this one!

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-10-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0f76844ee3219d0e3990216b5dd657aac4d36f7b

commit 0f76844ee3219d0e3990216b5dd657aac4d36f7b
Author: Ted Choc <tedchoc@google.com>
Date: Tue Sep 27 17:05:25 2016

Keep top controls visible if SHOW is called right after HIDE.

Currently, we early exit if the visibility amount matches our
desired ending amount.  But when you set HIDDEN as the current,
it will start an animation, and a immediate call to SHOWN will
see that the ending condition is met and return, but does not
clear the animation.

Now, clear the animation if the current value matches our
desired ending value to ensure it doesn't move.

BUG=639702
CQ_INCLUDE_TRYBOTS=master.tryserver.blink:linux_precise_blink_rel

Review URL: https://codereview.chromium.org/2371223002 .

Review-Url: https://codereview.chromium.org/2372713004
Cr-Original-Commit-Position: refs/heads/master@{#421125}
Cr-Commit-Position: refs/branch-heads/2840@{#546}
Cr-Branched-From: 1ae106dbab4bddd85132d5b75c670794311f4c57-refs/heads/master@{#414607}

[modify] https://crrev.com/0f76844ee3219d0e3990216b5dd657aac4d36f7b/cc/input/top_controls_manager.cc
[modify] https://crrev.com/0f76844ee3219d0e3990216b5dd657aac4d36f7b/cc/input/top_controls_manager_unittest.cc


### sh...@chromium.org (2017-01-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/639702?no_tracker_redirect=1

[Multiple monorail components: UI>Browser>FullScreen, UI>Browser>Omnibox]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085162)*
