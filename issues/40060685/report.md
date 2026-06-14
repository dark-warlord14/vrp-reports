# Security: External notifications from external apps (such as Telegram) can block Android fullscreen notification. (Testes on latest Chrome stable)

| Field | Value |
|-------|-------|
| **Issue ID** | [40060685](https://issues.chromium.org/issues/40060685) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Fullscreen, UI>Browser>FullScreen |
| **Platforms** | Android |
| **Reporter** | ha...@gmail.com |
| **Assignee** | ji...@chromium.org |
| **Created** | 2022-08-26 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

When entering fullscreen, the fullscreen notification is essential to warn users that they are entering fullscreen on the site to prevent spoofing attacks as the fullscreen mode lacks the omnibox. See <https://bugs.chromium.org/p/chromium/issues/detail?id=1311683>, for instance.

When a external notification popups from a message app, such as Telegram, it can block the fullscreen toast. This is because the fullscreen toast is situated near the top of the Android screen, so when the external notification pop-up it blocks the toast.

A recommended fix would be to shift the fullscreen notification lower so that external notifications will not obscure it.

**VERSION**  

Chrome Version: 104.0.5112.97 (Latest Stable version)  

Operating System: Android 11

**REPRODUCTION CASE**

1. Enable external notification popups on Android.
2. Using another phone message your victim phone on an chatting app such as Telegram / WhatsApp
3. On the victim phone, with the notification still on the screen, click on the button. The phone will enter fullscreen, with the external Telegram notification blocking the fullscreen toast. See the video for the PoC

Here is how an attacker can fully exploit it:

1. Attacker knows a victim phone number, sends a link to the victim.
2. The link contains the fullscreen button with a code that interfaces with a Telegram bot. When the victim presses the fullscreen button, the victim sends a fetch to a server which will in turn send an API request to Telegram bot. Since the attacker knows the victim phone number, he can program the bot to send a message to the victim which will result in a external notification.
3. The requestFullscreen is delayed via a setTimeout, until approximately after the notification arrives. After the external Telegram notification arrives, the victim will launch into the app with the external Telegram notification blocking the fullscreen toast.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Axel Chong

## Attachments

- [poc-fullscreen-chrome.mp4](attachments/poc-fullscreen-chrome.mp4) (video/mp4, 1.9 MB)
- [poc-external-notif.html](attachments/poc-external-notif.html) (text/plain, 358 B)
- [fs-bottom.png](attachments/fs-bottom.png) (image/png, 50.5 KB)

## Timeline

### [Deleted User] (2022-08-26)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-08-26)

A note here that the attackers does not even need a phone number, they can also send an external notification to a user via a Discord message for example where you only need a person's username to message someone (I think Telegram supports this feature too, but I am not too sure.)

### es...@chromium.org (2022-08-27)

twellington, do you know who (if anyone) owns the fullscreen bubble on Clank?

cc avi@ as this is further motivation for putting fullscreen behind a permission

[Monorail components: Blink>Fullscreen]

### [Deleted User] (2022-08-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-27)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tw...@chromium.org (2022-08-30)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>FullScreen]

### tw...@chromium.org (2022-08-30)

> do you know who (if anyone) owns the fullscreen bubble on Clank?

Yes, my team (Jinsuk specifically) has been doing work with this bubble. We switched from an OS Toast last year to address a security issue, but that also has caused a ripple effect of issues.

-> Jinsuk to consider the best approach here.

### ha...@gmail.com (2022-08-30)

I recommend shifting the toast to the middle to fix the problem, I don't think external app notifications can reach there. It also would make this important notification more prominent and hence noticed more easily.

### [Deleted User] (2022-09-09)

jinsukkim: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ji...@chromium.org (2022-09-09)

[Empty comment from Monorail migration]

### es...@chromium.org (2022-09-09)

[Empty comment from Monorail migration]

### es...@chromium.org (2022-09-09)

I don't think we have a fullscreen-on-Android security expert specifically to comment on #8. avi@, do you see any issue with moving the fullscreen bubble to the middle of the screen? I'm not sure if there's a historical reason why we put it on the top of the screen instead of the middle. I'm also not confident that a notification from another app wouldn't be able to cover the middle of the screen, I'm not sure if Android constrains notifications in some way.

### av...@chromium.org (2022-09-09)

Who knows Android stuff? I’d be OK moving it to the center of the screen, but better would be finding someone who can figure out the nuance of avoiding the situation if possible.

### ha...@gmail.com (2022-09-09)

Hi reporter here, I think the prompt in https://crbug.com/chromium/1356987#c12 might be better. The main problem here is that any user gesture can cause fullscreen to be triggered without the user knowing. Maybe a prompt that says "This site XXX is launching you into fullscreen", with a button to "acknowledge" or "go back", with the prompt only launching once a time per origin if "acknowledge" is chosen, and every time after, the standard fullscreen notification shows? Also, there could be a list of trusted sites which do not show this prompt by default, (maybe youtube.com?), I think it will eliminate this whole class of issues related to fullscreen.

It may be too complex but its just an idea that popped in my head :)

### [Deleted User] (2022-09-24)

jinsukkim: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@google.com (2022-09-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-24)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@google.com (2022-09-25)

Thanks for identifying this! We will prioritize this in Q4 with the following solution: relocate to the bottom of the screen where native OS toasts are placed.

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### ji...@chromium.org (2022-10-28)

A CL up for review https://chromium-review.googlesource.com/c/chromium/src/+/3990410

### ji...@chromium.org (2022-10-31)

elvinhu@ Would you mind taking a look at the screenshot above? Let me know how it is from UX standpoint, or whether any tweak is necessary.

### gi...@appspot.gserviceaccount.com (2022-10-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fc53d6b3f92e0b188f8bac43d6dbf220b642903d

commit fc53d6b3f92e0b188f8bac43d6dbf220b642903d
Author: Jinsuk Kim <jinsukkim@chromium.org>
Date: Mon Oct 31 22:23:32 2022

Android: Display fullscreen toast at the bottom

Positions the fullscreen toast at the bottom of the screen in order to
avoid being blocked by notifications from external apps.

Bug: 1356987
Change-Id: I0870fde82b66eaa3079339a715a2b7d1f25eab0f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3990410
Reviewed-by: Theresa Sullivan <twellington@chromium.org>
Commit-Queue: Jinsuk Kim <jinsukkim@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1065688}

[modify] https://crrev.com/fc53d6b3f92e0b188f8bac43d6dbf220b642903d/chrome/android/java/res/layout/fullscreen_notification.xml
[modify] https://crrev.com/fc53d6b3f92e0b188f8bac43d6dbf220b642903d/chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandler.java


### ji...@chromium.org (2022-10-31)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-02)

[Empty comment from Monorail migration]

### am...@google.com (2022-11-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-11)

Congratulations, Axel! The VRP Panel has decided to award you $2,000 for this report. Thank you for your efforts in discovering and reporting this issue to us! 

### am...@google.com (2022-11-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-01-09)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-10)

[Empty comment from Monorail migration]

### pg...@google.com (2023-01-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1356987?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Fullscreen, UI>Browser>FullScreen]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060685)*
