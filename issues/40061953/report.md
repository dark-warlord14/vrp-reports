# Security: Permission Prompts can be made totally hidden and user can Accept and interact with sensitive data without being aware Similar to (1358647)

| Field | Value |
|-------|-------|
| **Issue ID** | [40061953](https://issues.chromium.org/issues/40061953) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Permissions>Prompts |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | el...@gmail.com |
| **Assignee** | tu...@chromium.org |
| **Created** | 2022-11-29 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**

this is a report to a security vulnerability in google chrome/chromium browser as high-quality report with functional exploit , which similar to 1358647. here this vulnerability allows attackers to

1-Spoof All Permission Prompts, which is totally hidden , and Attacker can gain super permissions for his website Like:

(Clipboard Data & Mic & Camera & Location & Screen Sharing,..etc)

2-Attacker Can Read the Data (text,images) copied to the clipboard that also can be chained with CTRL+A CTRL+C ,this could leak Google/Facebook/Twitter username and passwords ,...etc

3-Attacker Can trick user to do harmful actions in Sensitive pages (Like Chrome Flags or Reset all Config , Stop Sync,..etc)

> > chrome://flags/ using (TAB and ENTER) Similar to what POC Video Shown  
> > 
> > chrome://settings/resetProfileSettings?origin=userclick (TAB TAB TAB ENTER),... same idea of POC Video

4-Attacker Can Navigate the hidden Window with any website that contain token or sensitive data and use CTRL+A CTRL+C to steal usernames, e-mail adresses, telephone numbers from any site like twitter, google and any others or Navigate the hidden window and resize it to get the data with Screen Sharing that was permited in step 1

Here in the POC, i have Demonstrated The Most Critical scenarios

Victim Play War Game , Just Pick your Weapons 1ST to Start Game and Attacker Got Sensitive Data and User Allow Permissions Without Being aware

# on Video PoC

User Asked to Pick Weapons before Start Game and behind the Scene these actions take effect

A) Attacker Website Asks for Clipboard Permission (user accept with TAB TAB TAB ENTER) ,this is totally hidden behind Picture in Picture Black Window

B) Permission Prompt for for MediaDevices appear (Mic & Camera) ,(user accept with TAB TAB TAB ENTER)

C)Permission for "Screen Sharing" appears (user accept with TAB TAB ENTER)

D)Share screen small toast appears (user can hide with TAB TAB ENTER)

---

**VERSION**

Exploit tested with the following properties:

Google Chrome Version 107.0.5304.121 (Official Build)(64-bit) Stable ,(linux Ubuntu 21.10)

Google Chrome Version 109.0.5414.10 (Official Build) dev (64-bit) ,(linux Ubuntu 21.10)

Google Chrome (windows 10) Version 107.0.5304.122 (Official Build) (64-bit)

---

**REPRODUCTION CASE**

the exploit use a vulnerability in showing

nobody will send critical information to unknown sites /Share Screen with , or allow to read Clipboard Sensitve data or Allow any Permissions to unknown Website. but this can be hide by full bypassing the visibility of all Prompts. in this case nobody are able to notice that they are sending their data to unknown attackers or allowing them to use Power Permissions for their Websites.

## REPRODUCTION STEPS

(Play a War Game , Just Pick your Weapons 1ST to Start Game and Attacker Got Sensitive Data and Victim Allow Critical Permissions Without Being aware

1-Visit  

A) <https://vrphunt.com/chrome/spoof-leak/canvasautofill-modx-linux.html> for Linux

B)<https://vrphunt.com/chrome/spoof-leak/canvasautofill-modx.html>  

for Windows

2- Follow Instructions of the Game to Pickup Weapons

3-Check Site Permissions to see the permissions you have allowed attacker to use.

4-Close PIP (Picture in Picture Overlay) Right Bottom Corner and Click inspect to see Base64 DataURL for screen images logged to the Console (Can Send to Attacker C&C Server).

# ==================== Observed:

Permission Prompts can be totally hidden, as popup window not visible to user and fully Covered by Picture in Picture (PIP) Overlay,This Obscured active window accepts keyboard input in sensitive browser UI and web pages that can be used to steal user data throught Clipboard and attacker control the navigation for this popup or let user do harmful actions like discussed above.

# Expected:

Sensitive browser UI is always visible to user so Hide Permission Prompts popup if it overlaps with picture-in-picture window.

# ===================== Mitigation:

After my Previous <https://crbug.com/chromium/1358647> has been fixed in 108 Release , one the the commits that should be used here to mitigate this issue is this

<https://bugs.chromium.org/p/chromium/issues/detail?id=1358647#c47>

<https://chromium.googlesource.com/chromium/src/+/87cf1589bb30dde902d74657840c8486b605a9b1>

this Commit Introduces:

Add GetWindowBounds for PictureInPicture

The window bounds would be used to check for any overlaps with the  

Autofill popup in the next CLs.

# Fix:

Add Another CL to Hide Permission Prompts popup if it overlaps with picture-in-picture window.  

Add CL for checking Popup window Bounds also , and if it covered by PIP overlay Cancel it, to prevent Different Types of Attacks

---

**CREDIT INFORMATION**  

Reporter credit: Ahmed ElMasry

---

Thank you for your attention. with kind Regards

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2022-11-29)

[Empty comment from Monorail migration]

### el...@gmail.com (2022-11-29)

[Comment Deleted]

### el...@gmail.com (2022-11-29)

Note : ( Follow Instructions of the Game to Pickup Weapons) as Mentioned  in Game as Windows accept Prompts with only  >>  TAB TAB ENTER ,
so please follow REPRODUCTION STEPS  in both windows and Linux  PoCs for Good Repro.

Thanks 


### ca...@chromium.org (2022-11-29)

I was able to reproduce this in M106, ravjit: Can you PTAL (and re-assign as appropriate). Thanks!

[Monorail components: UI>Browser>Permissions>Prompts]

### [Deleted User] (2022-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-30)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-30)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@gmail.com (2022-12-09)

carlosil@
ravjit@

Any further updates on this issue , could you please follow up, and fix?


### [Deleted User] (2022-12-13)

ravjit: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@gmail.com (2022-12-21)

ravjit@ 
Friendly Ping: will you work on this soon?
thanks 

### el...@gmail.com (2022-12-28)

carlosil@

Could you add  mlerman@chromium.org to CC list thanks 

### [Deleted User] (2022-12-28)

ravjit: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### en...@chromium.org (2023-01-04)

We likely want to fix this at the input protector level so that all kinds of security-relevant dialogs can benefit. Tentatively scheduling work on this (alongside https://crbug.com/chromium/1369103) for M113.

### el...@gmail.com (2023-03-14)

Hi engedy@ 
any further updates on this? is this under your radar?
Thanks 

### en...@chromium.org (2023-03-15)

Thanks for the ping. Routing to Thomas who has already addressed number of similar issues recently.

### el...@gmail.com (2023-03-27)

Hello tungnh@ Thomas,
Friendly Ping:  any further updates on this? is this under your radar?
Thanks

### tu...@chromium.org (2023-03-30)

Thanks for the ping, I'd added this ticket to my list. 

I took a quick look on 1358647 and a naive approach for us : disable key events handler of the permission prompt if there is intersection with PiP window.

### el...@gmail.com (2023-04-28)

Hey Thomas (tungnh@),  just wanted to check in and see if you had some free time to work on this, in case it slipped your radar.If you have any availability to work on it soon, that would be great.Appreciate your help! Thanks!

### tu...@chromium.org (2023-05-02)

I took a look and will start it soon, maybe next week. The fix might require a bit refactoring, due to chromium structure build's requirement. The event handler is located in UI, and PiP code is in Chrome (where UI/views could not add a build dependency to).



### tu...@chromium.org (2023-05-08)

[Empty comment from Monorail migration]

### tu...@chromium.org (2023-05-08)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-05-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/073278eae6d6ce07cc40107567907e545ec56157

commit 073278eae6d6ce07cc40107567907e545ec56157
Author: Thomas Nguyen <tungnh@google.com>
Date: Wed May 10 10:38:26 2023

Ignore button pressed event if button row intersects with PiP window

Bug: 1394410

Change-Id: I215826daabe6476f57613ec4f53417e4b16659fe
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4498354
Reviewed-by: Elias Klim <elklm@chromium.org>
Reviewed-by: Thomas Lukaszewicz <tluk@chromium.org>
Commit-Queue: Thomas Nguyen <tungnh@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1141985}

[modify] https://crrev.com/073278eae6d6ce07cc40107567907e545ec56157/chrome/browser/ui/views/permissions/permission_prompt_bubble_base_view.cc
[modify] https://crrev.com/073278eae6d6ce07cc40107567907e545ec56157/ui/views/window/dialog_client_view.cc
[modify] https://crrev.com/073278eae6d6ce07cc40107567907e545ec56157/chrome/browser/ui/views/permissions/permission_prompt_bubble_base_view.h
[modify] https://crrev.com/073278eae6d6ce07cc40107567907e545ec56157/ui/views/window/dialog_delegate.cc
[modify] https://crrev.com/073278eae6d6ce07cc40107567907e545ec56157/ui/views/window/dialog_delegate.h


### tu...@chromium.org (2023-05-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-10)

[Empty comment from Monorail migration]

### am...@google.com (2023-05-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-05-19)

Congratulations, Ahmed! The VRP Panel has decided to award you $2,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-05-19)

[Empty comment from Monorail migration]

### el...@gmail.com (2023-05-22)

[Comment Deleted]

### el...@gmail.com (2023-05-23)

[Comment Deleted]

### am...@chromium.org (2023-07-15)

[Empty comment from Monorail migration]

### am...@google.com (2023-07-18)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@gmail.com (2023-08-17)

Hi.., 
Local-Files-spoof-leak.zip is Deleted until https://crbug.com/chromium/1448132 is fixed , and it will be un-deleted  again once fixed to prevent potential security implications.
Thanks


### is...@google.com (2023-08-17)

This issue was migrated from crbug.com/chromium/1394410?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061953)*
