# Security UI Spoofing on Android Chrome Due to Picture in Picture PIP Fullscreen 

| Field | Value |
|-------|-------|
| **Issue ID** | [338254612](https://issues.chromium.org/issues/338254612) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Media>UI, UI>Browser>FullScreen |
| **Platforms** | Android |
| **Reporter** | pu...@gmail.com |
| **Assignee** | li...@google.com |
| **Created** | 2024-05-01 |
| **Bounty** | $1,000.00 |

## Description

VULNERABILITY DETAILS
When a User Double Tap on the attacker page it activates PIP Picture in Picture Dialog and at the same time Request the page to Enter Fullscreen Mode 

the Fullscreen alert messages Shows in PIP Picture in Picture dialog it does not Cleary display to user. due to small Fullscreen alert notification message in Picture in Picture dialog, and it disappear Fullscreen alert Messages very Quickly in PIP Picture in Picture dialog. 

because of this the user is not capable to know that they entered Fullscreen, which allows an attacker to spoof the entire screen with attacker content.

attached a video reproducing the attack.

VERSION
Chrome Version: [125.0.6422.14] + [beta]
Operating System: [Android 14]

REPRODUCTION CASE
1. Load Attacked HTML File & Video File in Your Localhost or Server
2. Access the Page and Double Tap on Gmail Image
3. Picture in Picture Will Show up and In Background it Changes to Spoof Page
4. Fullscreen Messages Shows in PIP-Picture in Picture and Hides Fullscreen Messages Quickly
5. You can Close the PIP-Picture in Picture dialog and the page will remain spoofed.

CREDIT INFORMATION
Reporter credit: [Puf]

## Attachments

- [POC.html](attachments/POC.html) (text/html, 2.0 KB)
- [Reproduce Video.mp4](attachments/Reproduce Video.mp4) (video/mp4, 170.5 KB)
- [video.mp4](attachments/video.mp4) (video/mp4, 24.9 KB)
- [New POC.html](attachments/New POC.html) (text/html, 2.0 KB)
- [#1.PNG](attachments/#1.PNG) (image/png, 105.7 KB)
- [#2.PNG](attachments/#2.PNG) (image/png, 46.7 KB)
- [screen-20240507-140956.mp4](attachments/screen-20240507-140956.mp4) (video/mp4, 4.1 MB)
- [Latest Reproduce.mp4](attachments/Latest Reproduce.mp4) (video/mp4, 363.3 KB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [mailvideo.mp4](attachments/mailvideo.mp4) (video/mp4, 65.5 KB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [mailvideo.mp4](attachments/mailvideo.mp4) (video/mp4, 65.5 KB)
- [New Latest Reproduce.mp4](attachments/New Latest Reproduce.mp4) (video/mp4, 388.4 KB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [Latest Reproduce.mp4.mp4](attachments/Latest Reproduce.mp4.mp4) (video/mp4, 330.5 KB)
- [POC.html](attachments/POC.html) (text/html, 2.9 KB)
- [football.mp4](attachments/football.mp4) (video/mp4, 46.7 KB)
- deleted (application/octet-stream, 0 B)
- [Latest Repro .mp4](attachments/Latest Repro .mp4) (video/mp4, 1.1 MB)

## Timeline

### th...@chromium.org (2024-05-02)

I'm not able to reproduce this. Reporter - is this a stable POC? I get into one of two states when I try to reproduce this: 1) it doesn't enter full screen at all, or 2) it enters full screen but the message is not restricted to the PIP window.

Looking at your repro video, I'm not convinced we'd consider this a security bug, since the full screen message is still shown; it's just constrained to within the PIP window. Looping in some full screen folks -- based on the repro video ("Reproduce Video.mp4"), do you think this is a security concern?

### pu...@gmail.com (2024-05-02)

I Have Attached Updated POC

1. Please Double tap on Gmail Logo it will Activate Fullscreen Mode

Q: since the full screen message is still shown

Ans: But it Shown in small Text in PIP Window & Quickly Disappear Fullscreen alert message.

User is unable to identify full screen alert message in PIP Window.

### pu...@gmail.com (2024-05-06)

I Have Attached Screenshot In portrait & landscape

Fullscreen Notification alert Quickly Disappear in just 2-3 Seconds in PIP Window

### ch...@chromium.org (2024-05-07)

Thanks for the report.

I could not get it to work on Android 10 with Chrome 125, nor Android 14 with Chrome 113 (was having trouble with my emulator, so I did not get to try other versions -- it's possible I just didn't have a version with PiP enabled). The PiP does not show up for me. I just get the fullscreen "login page" image with the correctly-sized banner. Same as what thefrog@ noted above.

Hopefully someone with an Android device with PiP enabled can check.

I'm going to set the labels provisionally based on the information provided here. Assigning High severity assuming the attacker can control the whole screen without the user realizing they're in fullscreen.

### ch...@chromium.org (2024-05-07)

cc liberato: Would be great if you could take a look from the PiP side of things. Thanks!

### ta...@chromium.org (2024-05-07)

I also wasn't able to repro with a physical device (Pixel 6, Android 14) and Chrome beta 125.0.6422.26.

> I'm not convinced we'd consider this a security bug, since the full screen message is still shown; it's just constrained to within the PIP window.

I agree although I'm not a security expert.

### pe...@google.com (2024-05-07)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### pu...@gmail.com (2024-05-08)

I Have Attached New Updated POC Code

REPRODUCTION CASE

1. Load POC File & mailvideo.mp4 file into Your Localhost or Server
2. Open the page
3. Click on [Open]
4. Now click again [1] more time on same button
5. Fullscreen Messages Shows in PIP-Picture in Picture and Hides Fullscreen Messages Quickly move to portrait mode
6. and the page will remain spoofed.

see <https://issues.chromium.org/issues/338254612#comment20> for Latest Poc

### li...@chromium.org (2024-05-09)

I'll try to repro this locally later today.

When one uses `requestPictureInPicture` to open a video pip window, chrome starts a new activity to hold the pip window.  I don't know how android maps toasts to activities, but it sounds like that's not happening the way we'd expect.

I tend to agree with c#2 since the alert is shown, just in a different place.

### el...@chromium.org (2024-05-09)

Shepherd: setting FoundIn & Impact based on original report.

### pu...@gmail.com (2024-05-10)

Latest POC Video Attached with this New Technique attacker can control the whole screen without user knowing they're in Fullscreen.

I agree alert is shown here but the alert is showing " inside the pip window "

this gives to attacker an opportunity to take control the whole screen by using pip window, attacker can use this to trick user open pip window, and in the background attacker take the control of screen while the user does not know they are in Fullscreen

I Have attached two videos reproducing the attacks.

see <https://issues.chromium.org/issues/338254612#comment20> for Latest Poc

### pe...@google.com (2024-05-10)

Setting milestone because of s0/s1 severity.

### li...@chromium.org (2024-05-13)

For what it's worth, here [1] is where we create the full screen toast.  We explicitly set the activity, which makes me think that it's potentially an android framework issue unless we're somehow sending the wrong activity in.  The latter isn't impossible, but it's unlikely, since the fullscreen handler is usually handed out by the chrome activity that created it.  Unclear how the pip activity, which doesn't have a webcontents, would end up involved when a site tries to enter fullscreen.

With a local repro and some logging, this would be much easier to rule out :)

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandlerBase.java;drc=90c05a47db79d579e95625a4138619b814dd8683;l=297

### pe...@google.com (2024-05-21)

takumif: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### li...@chromium.org (2024-05-31)

Secondary shepherd chiming in!

I think this should still be a security bug as the PiP window is smaller and a user could potentially miss/be confused by the fullscreen message even though it's still visible. I do think because the message is visible the severity should be a medium, however.

I similarly have not been able to repro this locally. Reporter, what type of Android device are you using to reproduce?

### pu...@gmail.com (2024-05-31)

Operating System: [Android 14]

Device Name: [Vivo V27]

### pu...@gmail.com (2024-05-31)

Operating System: [Android 14]

Device Name: [Vivo V27]

Chrome Version: [126.0.6478.26]

### pu...@gmail.com (2024-05-31)

> even though it's still visible. I do think because the message is visible the severity should be a medium

Attacker Can still Hide visibility of Fullscreen Message Through PIP Window By dragging pip window to sides of the screen, this only possible if user drag PIP window to side of the screen in Android

because of this the user is not capable to know that they entered Fullscreen, which allows an attacker to spoof the entire screen with attacker content.

attached a video reproducing the attack.

### pu...@gmail.com (2024-05-31)

I Have attached Latest POC Video Attached

in this POC reproduce you can see in PIP window very small Fullscreen message is showing it is very small and a user can easily miss it

I have added the football.mp4 video here because of this video the pip window changes to square shape window, this will make Fullscreen message very small, and user is not capable of reading the Fullscreen message because of very small words and can easily miss it

kindly Consider this High severity because the attacker can control the whole screen without the user realizing they're in Fullscreen.

REPRODUCTION CASE

- 1.Load POC File & football.mp4 file into Your Localhost or Server
- 2.Open the page
- 3.Click on [Open]
- 4.Now click again [1] more time on same button
- 5.very small Fullscreen Messages Shows in PIP-Picture in Picture and Hides Fullscreen
  Messages Quickly and the page will remain spoofed, and the user can easily miss the Fullscreen message.

Operating System: [Android 14]

Device Name: [Vivo V27]

Chrome Version: [126.0.6478.26]

### pe...@google.com (2024-06-05)

takumif: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pu...@gmail.com (2024-06-21)

Would you kindly give me an update?

What’s the current status of this Issue.

Thank you!

### pu...@gmail.com (2024-07-02)

Would you kindly give me an update?

What’s the current status of this Issue.

Thank you!

### pu...@gmail.com (2024-07-11)

Hello, any updates here?

### li...@chromium.org (2024-07-12)

=> me for tracking.

This particular case looks like an android framework bug, so it's likely not actionable on the chrome side. => P2

More generally, toasts are fairly easy for the user to miss, even if the site isn't actively trying to obscure them.  If the site does want to obscure them, then there are multiple approaches that it can use.  Fixing the larger problem is something we're actively looking at.

### pu...@gmail.com (2024-10-16)

Hello, any updates here?

### pu...@gmail.com (2024-12-13)

friendly ping

### pu...@gmail.com (2025-02-18)

Friendly Ping :) Thanks

any update on this issue

### li...@google.com (2026-02-06)

This one doesn't repro locally anymore. The toast is visible.

### pu...@gmail.com (2026-02-07)

deleted

### pu...@gmail.com (2026-02-19)

doesn't repro anymore. The toast is visible. in Latest Version 147.0.7681.2

Kindly Please mark this as Fixed

### dr...@chromium.org (2026-02-19)

Adjusting labels since this was fixed by something in the framework.

### sp...@google.com (2026-03-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Low impact security UI spoof


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Low impact security UI spoof

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/338254612)*
