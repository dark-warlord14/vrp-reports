# Security: Bypass the Protection of input fields cache (Autofill) Similar to (1358647 ,1395164 ,1108181) with Different Vector

| Field | Value |
|-------|-------|
| **Issue ID** | [40074918](https://issues.chromium.org/issues/40074918) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | el...@gmail.com |
| **Assignee** | sy...@google.com |
| **Created** | 2023-10-14 |
| **Bounty** | $3,000.00 |

## Description

# **VULNERABILITY DETAILS**

This Issue is identical to the Recently Resolved Ones <https://crbug.com/chromium/1108181> , <https://crbug.com/chromium/1358647> , <https://crbug.com/chromium/1395164>

But With Different Attack Vector , as the Solved Ones <https://crbug.com/chromium/1358647> , <https://crbug.com/chromium/1395164> the attack vector is Hiding Autofill Popup behind Picture in Picture Overlay (PIP) , and here in this Case the Attack Vector is : Hiding the Autofill popup behind Live Caption Bubble Overlay.

as you know most of us uses live Caption features espicially in getting Transcripted instructions in Noisy environment or while playing war games and there is a shoots in , also this is mostly used by deaf /hard hearing people and sometimes it can be used to understand what someone is saying but can't turn on your speaker.., that's really nice feature i love it so tried to test it with some good ideas .

\*\*  

(so Please Add Same Folks of 1358647 1395164 to take the ownership of this issue)  

Owner: [vidhanj@google.com](mailto:vidhanj@google.com) , Could You Also Add [schwering@google.com](mailto:schwering@google.com) and [jkeitel@google.com](mailto:jkeitel@google.com)  

Thanks  

\*\*

This is a report to a security vulnerability in google chrome/chromium browser as high-quality report with functional exploit. this vulnerability allows attackers to steal the cache of input fields like usernames, e-mail addresses, telephone numbers from any site like twitter, google and any others (Chrome Autofill Saved Data).

# Bug History and Commits that contains Same Logic of Mitigation:

## <https://crbug.com/chromium/1358647>

[1]-<https://chromium-review.googlesource.com/c/chromium/src/+/3921456>

Add GetWindowBounds for PictureInPicture

The window bounds would be used to check for any overlaps with the  

Autofill popup in the next CLs.

[2]-<https://chromium-review.googlesource.com/c/chromium/src/+/3959939>

Hide Autofill popup if it overlaps with picture-in-picture window

This CL introduces BoundsOverlapWithPictureInPictureWindow used in  

autofill\_popup\_view\_native\_views.cc to determine whether there is an  

overlap between the picture-in-picture window and the autofill popup.  

If it does, it hides the autofill popup.

## <https://crbug.com/chromium/1395164>:

[3]-<https://chromium-review.googlesource.com/c/chromium/src/+/4738656>

Add Observer class to PictureInPictureWindowManager

This CL adds an observer class to PictureInPictureWindowManager  

alongwith the logic to send events to notify the observers whenever  

a pip window is shown for the video element or the document  

picture-in-picture.

[4]-<https://chromium-review.googlesource.com/c/chromium/src/+/4737994>

# Hide Autofill Popup if hidden behind Pip window Cont..

## Bug Mitigation Logic:

After Reading code part of Live Caption Controller i found that this logic isn't introduced there, so from Above Commits we need same logic here in this case , and this logic can be as below:

1-Add code to observe the live caption bubble presence

2-Add GetWindowBounds for live\_caption\_bubble so The bubble bounds would be used to check for any overlaps with the Autofill popup in the next CLs as in commit[1] above.

3-Add another CL to implement Hide Autofill popup if it overlaps with live caption bubble Bounds.

and Observer Code may be placed at CreateUI() at

<https://source.chromium.org/chromium/chromium/src/+/main:components/live_caption/live_caption_controller.cc;l=187>

as after StartLiveCaption() is called , the SodaInstaller determines whether SODA is already on the device and whether or not to download. Once SODA is on the device and ready, the SODAInstaller calls OnSodaInstalled on its observers. The UI is created at that time , and this time of creating UI of live caption Bubble is the reasonable place to add our check.

# =================================== **VERSION**

Exploit tested with the following properties:

# Google Chrome Version: 118.0.5993.70 Channel: Stable Release (Official Build) (64-bit) Milestone:118 Branch: 5993 Branch Base Position:1192594 Google Chrome: 118.0.5993.70 (Official Build) (64-bit) Revision: e52f33f30b91b4ddfad649acddc39ab570473b86-refs/branch-heads/5993@{#1216} OS:Linux **-------------------------** ------- Google Chrome: 120.0.6051.2 (Official Build) dev (64-bit) Revision: 75e545cf7ce76506ad3d2a5736ef28053af4a7f7-refs/branch-heads/6051@{#4} Chrome Version: 120.0.6051.2 Channel: DEV (Official Build) dev (64-bit) Milestone: 120 Branch: 6051 Branch Base Position: 1206341 OS:Linux **-------------------------** ------ Chrome Version: 120.0.6062.2 Channel: DEV (Official Build) dev (64-bit) Milestone: 120 Branch: 6062 Branch Base Position: 1208568 OS:Linux

## **REPRODUCTION CASE**

the exploit use a vulnerability in showing of cache of input fields. your browser suggests the saved entries of input fields like saved user logins (username, email, phone number...) or cached search word any similar entered things.

nobody will send critical information to unknown sites. but this can be hide by full bypassing the visibility of all fields and suggests. in this case nobody are able to notice that they are sending their data to unknown attackers.

# REPRODUCTION STEPS

(Play a Battle War game to get hijacked any cached input of field-name "username",email,telephone,address,card-number,.....)

\*\*Before Repro you can add some data under chrome://settings/addresses and add at least one or two records\*\*

## \*\*Before Repro You should Enable Live Caption from chrome://settings/captions\*\*

1-visit <https://vrphunt.com/chrome/viewport/show-me-out3-caption.html>

2-Press Enter to Show Instructions Bubble for the Game

3-Press (Arrow DOWN) then (ENTER) to start Game.

4- Alert Popup appears with (Autofill data Will be sent to remote attacker)

what is likely happens here is that:  

**-------------------------** -----------  

1- once landed on the game page and 1st enter is pressed the audio that simulate game instructions is playing and Live Captions Start Showing up at the Bottom of screen \*\* This Step in Real live Game Isn't necessary as i made this POC more Simple and used this TTS audio file to simulate game Environment\*\*

2- on Arrow Down >> user will select 1st index (record) of Autofill popup as the input field is initially focused and pressing arrow down drop the autofill popup.

3- pressing Enter which Confirm the selecting of Autofill record , and Alert popup will be shown with the value of the input.

# ========================== Observed (What's Go wrong):

Autofill popup can be hidden, as popup not visible to user and fully Covered by Live Caption Bubble Overlay and this bypasses chrome security measures in sensetive data (Autofill).

# Expected:

Sensitive browser UI is always visible to user ,so Hide Autofill popup if it overlaps with Live Caption Bubble Overlay.

# ===================== Mitigation:

1-Add code to observe the live caption bubble presence

2-Add GetWindowBounds for live\_caption\_bubble so The bubble bounds would be used to check for any overlaps with the Autofill popup in the next CLs as in commit[1] above.

3-Add another CL to implement Hide Autofill popup if it overlaps with live caption bubble Bounds.

## \*\* -All POC Videos Attached -All POc Files Attached -Feel free to Use Online Version as attaching Games Photos in attachments isn't a good idea. \*\*

**CREDIT INFORMATION**  

Reporter credit: Ahmed ElMasry

---

Thank you for your attention. with kind Regards

## Attachments

- [Bypass-AutofillCap-DEV-V120-2023-10-14_23-44-16.mp4](attachments/Bypass-AutofillCap-DEV-V120-2023-10-14_23-44-16.mp4) (video/mp4, 1.7 MB)
- [Bypass-Autofill-Cap-StableV118-2023-10-14_23-40-24.mp4](attachments/Bypass-Autofill-Cap-StableV118-2023-10-14_23-40-24.mp4) (video/mp4, 1.3 MB)
- [show-me-out3-caption.html](attachments/show-me-out3-caption.html) (text/plain, 2.2 KB)
- [tts-game-instructions.mp3](attachments/tts-game-instructions.mp3) (application/octet-stream, 112.7 KB)
- [wargame.webp](attachments/wargame.webp) (image/webp, 191.2 KB)
- [CanaryWin-V120-2023-10-16 21-25-04-382.mp4](attachments/CanaryWin-V120-2023-10-16 21-25-04-382.mp4) (video/mp4, 3.0 MB)
- [Screenshot from 2025-04-07 13-50-37.png](attachments/Screenshot from 2025-04-07 13-50-37.png) (image/png, 507.0 KB)

## Timeline

### [Deleted User] (2023-10-14)

[Empty comment from Monorail migration]

### el...@gmail.com (2023-10-16)

Additional info:

Today i've  Created a new POC  for Windows Platform [1],  and Continued testing against All Win Platforms Releases in different Channels as Below:

[1] - https://vrphunt.com/chrome/viewport/show-me-out3-caption-win.html

Google Chrome	120.0.6070.0 (Official Build) canary (64-bit) (cohort: Clang-64) 
Revision	165e73b1ec1e7907eca1bb54555b2026ef6c2113-refs/branch-heads/6070@{#1}
OS	Windows 11 Version 22H2 (Build 22621.2361)

**Before Repro you can add some data under chrome://settings/addresses and add at least one or two records**

**Before Repro You should Enable Live Caption from chrome://settings/captions**

Same Repro Steps As 

1-visit https://vrphunt.com/chrome/viewport/show-me-out3-caption-win.html

2-Press Enter to Show Instructions Bubble for the Game 

3-Press (Arrow DOWN) then (ENTER) to start Game.

4- Alert Popup appears with (Autofill data Will be sent to remote attacker)

Thanks

### ct...@chromium.org (2023-10-16)

Thanks for the report. Looping in folks for this variation on the previous https://crbug.com/chromium/1358647 and https://crbug.com/chromium/1395164.

Conceptually this seems reminiscent of https://crbug.com/chromium/1431043 and https://crbug.com/chromium/1433581 (but for autofill instead of fullscreen). The fix on Windows there was crrev.com/c/4508964 to explicitly force z-ordering to put security-sensitive UIs on top (the semi-transparent background of the live captions view is not sufficient).

[Monorail components: UI>Browser>Autofill]

### [Deleted User] (2023-10-16)

[Empty comment from Monorail migration]

### ma...@chromium.org (2023-10-17)

FWIW, in crrev.com/c/4508964 
it seems it was planned to have a better fix, and there is a TODO
https://chromium-review.googlesource.com/c/chromium/src/+/4508964/comments/7ff26e6a_4ce34f67

Maybe that will fixed for this bug too?


### [Deleted User] (2023-10-17)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vi...@google.com (2023-10-26)

[Empty comment from Monorail migration]

### ke...@chromium.org (2023-10-26)

It is possible that the popup window is using a NativeWidgetAura. That means, it shares the canvas with the browser window, and therefore it will be always behind other top-level widgets like the live caption bubble. If that is the case,  the TODO in https://chromium-review.googlesource.com/c/chromium/src/+/4508964/comments/7ff26e6a_4ce34f67 won't fix the issue. The only solution would be to close one of the conflicting dialogs.

I don't think this is a bug on Mac, can you confirm?

### vi...@google.com (2023-10-26)

Assigning to Dima who knows more about the Autofill popup window

### [Deleted User] (2023-10-29)

vykochko: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vy...@google.com (2023-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-01)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@gmail.com (2023-11-08)

friendly ping : vykochko@ Hello Dima ., is this issue under your radar? , will you start working on this soon? , could you please follow up , Thank you!

### [Deleted User] (2023-11-15)

vykochko: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@gmail.com (2023-11-20)

vykochko@
Hello Dima ..,
Just wanted to check if there is a progress on this issue so
Since I don't see any updates or opened CL yet since submission. 
Could you prioritize this , hope this fixed soon,  just keep me posted with new updates, Thank you

### ml...@chromium.org (2023-11-27)

vykochko@ and vidhanj@ both have work underway towards this issue.

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### el...@gmail.com (2023-12-11)

Hello Dmitry vykochko@ ..,

Don't see any opened CL for this Bug yet , is there any progress here , just let me informed with new updates , appreciate your time and efforts solving this one.

Thank you.

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### el...@gmail.com (2024-01-09)

Hello mlerman@,vykochko@
This is a friendly reminder to check if there is any updates here , 
vykochko@: will you start working on this issue soon?

mlerman@ Mike: could you please follow up this?
Thank you!

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-11)

This issue was migrated from crbug.com/chromium/1492758?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### el...@gmail.com (2024-02-15)

Hello vykochko@,mlerman@

friendly reminder: Is there any update regarding this bug or the planned timeline?

Thank you

### el...@gmail.com (2024-03-13)

Hello Mike mlerman@
Any further updates since this comment?
As I don't see any activity here
<https://issues.chromium.org/issues/40074918#comment17>

Please keep me posted with new updates.
Thank you

### ml...@chromium.org (2024-03-18)

Hi Dima, have you had a chance to explore this?

### el...@gmail.com (2024-04-04)

Hello., Mike mlerman@, Dima vykochko@,

I see this one doesn't got more attention from your side since Oct2023 , and now we near to pas 2024 Q1 without any progress or activity.

Please give this more attention ,or if Dima isn't the right owner please pass this over
Thank you

### ml...@chromium.org (2024-04-08)

vykochko@ is spending a bit of time exploring the issue and is working internally to propose some alternatives.

### el...@gmail.com (2024-05-27)

Hello.,
just looking for new updates on this one
Thank you

### vy...@google.com (2024-05-31)

Hi, there is no direct progress on this issue so far, but we are currently working on more generic solution and the issue is on our radar. Thanks again for reporting and your patience!

### el...@gmail.com (2024-10-09)

Hi,

**Friendly reminder**

Is there any update regarding this bug?

Thanks

### pe...@google.com (2024-10-26)

vykochko: Uh oh! This issue still open and hasn't been updated in the last 79 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-11-15)

brunobraga: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### el...@gmail.com (2025-02-27)

Hello there..,

@Mike: any further progress towards the fix here , any plan to be worked soon?

just keep me updated

Thanks

### sy...@google.com (2025-04-03)

I reproduced this bug on Beta 135.0.7049.41.

I verified that enabling the feature `AutofillPopupZOrderSecuritySurface` resolves the issue for me. @reporter could you check if enabling this flag `AutofillPopupZOrderSecuritySurface` (`--enable-features=AutofillPopupZOrderSecuritySurface`) makes the autofill popup visible to you as well?

### el...@gmail.com (2025-04-07)

Hello,

I've tested the POC in chrome with the following properties

Google Chrome: 137.0.7106.2 (Official Build) dev (64-bit)

Revision: 1c747abcf0d36711842a757c0be59b92e69d2012-refs/branch-heads/7106@{#6}

with `(--enable-features=AutofillPopupZOrderSecuritySurface)` enabled , and the autofill popup now visible, and bug is now fixed , the attachment show the fix

- so feel free to Mark this as Fixed, please provide the commit of the fix here so the automation can go through without problems.

Thank you for your time providing the fix

### el...@gmail.com (2025-05-17)

Hello,
just wanted to check if there's any more work left to do here
Thanks

### am...@chromium.org (2025-06-23)

AIUI this issue is resolved by enabling --AutofillPopupZOrderSecuritySurface, which is disabled by default. Because this is disabled by default, this is not considered fixed in shipped, production versions of Chrome. I understand this issue may not be prioritized given that there is a solution here, and it seems unnecessary to craft a bespoke fix for this issue. 
We cannot, however, close this issue out as Fixed at this time. 
Do we have a timeline for AutofillPopupZOrderSecuritySurface being enabled by default? 

### ml...@chromium.org (2025-06-27)

Re: c#40, we're in final stages of experimentation, and should be weeks away from enabling by default (assuming the experimentation doesn't reveal any problems).

### sy...@google.com (2025-07-14)

I'm happy to share that AutofillPopupZOrderSecuritySurface got enabled by [default](https://chromium-review.googlesource.com/c/chromium/src/+/6722253)

Please reopen in case you are still able to reproduce this issue.

### ch...@google.com (2025-07-14)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2025-07-24)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
$2,000 for report of lower impact user information disclosure + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### el...@gmail.com (2025-07-27)

Thanks for the reward and Bonus

### ch...@google.com (2025-10-21)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> $2,000 for report of lower impact user information disclosure + $1,000 bisect bonus

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40074918)*
