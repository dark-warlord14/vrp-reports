# Security: about:blank origin shown in Bluetooth and other permission dialogs

| Field | Value |
|-------|-------|
| **Issue ID** | [40066643](https://issues.chromium.org/issues/40066643) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Bluetooth, Blink>HID, Blink>Serial, Blink>USB, UI>Browser>Permissions>Prompts |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@gmail.com |
| **Assignee** | ze...@chromium.org |
| **Created** | 2023-06-29 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

In Chorme Desktop API the access dialog should use permission delegation and should always show the top level page origin.  

But I tried to bypass on Chrome Desktop, on Android Chrome there is already security to show page origin.

iframe. sandbox = 'allow-scripts allow-popups allow-same-origin';

I tested the location dialog, camera, etc. The domain appears,but the dialogue on bluetooth,USB,Serial Port,HID does not appear domain

<https://huntertoday18.000webhostapp.com/coba.html>

**VERSION**

Chrome Version: Version 114.0.5735.199 (Official Build) (64-bit)  

Operating System: Windows 11

Reference :

<https://bugs.chromium.org/p/chromium/issues/detail?id=1226909>  

<https://bugs.chromium.org/p/chromium/issues/detail?id=1375132>  

<https://sites.google.com/a/chromium.org/dev/Home/chromium-security/deprecating-permissions-in-cross-origin-iframes>

Thanks

## Attachments

- [POC.mp4](attachments/POC.mp4) (video/mp4, 865.5 KB)

## Timeline

### [Deleted User] (2023-06-29)

[Empty comment from Monorail migration]

### es...@chromium.org (2023-06-30)

Balazs, could you please help triage? It looks like the Bluetooth chooser and some other permission dialogs show "about:blank" rather than the actual origin. Triaging as Medium severity following https://crbug.com/chromium/1375132 (since the user does not see the actual origin they are granting the permission to).

[Monorail components: Blink>Bluetooth Blink>HID Blink>Serial Blink>USB UI>Browser>Permissions>Prompts]

### es...@chromium.org (2023-06-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-30)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@gmail.com (2023-07-01)

hii this also impact  in 
Chromium : Version 116.0.5810.0 (Developer Build) (64-bit)

Why haven't the priorities changed for this report?

### re...@chromium.org (2023-07-01)

Can someone from the Security team describe the scenario here? The address bar of the popup window shows "about:blank" so I'm surprised that some permission prompts are showing an origin instead.

### al...@gmail.com (2023-07-06)

any update for this why priorities changed for this report ? 

### [Deleted User] (2023-07-10)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### re...@chromium.org (2023-07-10)

It looks like there is a proposed fix to this issue attached to https://crbug.com/chromium/1463149. I've asked the reporter there to add a test case to their patch demonstrating the scenario.

### re...@chromium.org (2023-07-10)

[Empty comment from Monorail migration]

### re...@chromium.org (2023-07-10)

Zelin, can you take over the proposed fix in https://chromium-review.googlesource.com/c/chromium/src/+/4672069 and add the necessary test coverage to make sure this doesn't regress (again).

### re...@chromium.org (2023-07-10)

[Empty comment from Monorail migration]

### ze...@chromium.org (2023-07-11)

Sure, I will look into this.

### ze...@chromium.org (2023-07-12)

As discussed with reillyg@. The proposed fix looks good, I will help add test coverage.

### gi...@appspot.gserviceaccount.com (2023-07-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/313891e4ee57cf42d1ae46a0de1cef6e3f607070

commit 313891e4ee57cf42d1ae46a0de1cef6e3f607070
Author: Zelin Liu <zelin@chromium.org>
Date: Wed Jul 19 01:36:43 2023

Create browser test to use frame origin instead of URL

RFH GetLastCommittedOrigin() is not always the origin of
GetLastCommittedUrl(). In the case of a pop up window. The origin will
be the parent's origin, but URL will be initialized to about::blank.

In this CL, we add a test to ensure CreateChooserTitle uses the frame's
origin instead of URL. This test is done using a browsertest as it is
difficult to recreate this scenario in a unit test setup.

Bug: 1459281
Change-Id: If6d92760f30d09c704ec6f78f6aa531b6f12d7e8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4692263
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Commit-Queue: Zelin Liu <zelin@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1172114}

[modify] https://crrev.com/313891e4ee57cf42d1ae46a0de1cef6e3f607070/chrome/test/BUILD.gn
[add] https://crrev.com/313891e4ee57cf42d1ae46a0de1cef6e3f607070/chrome/browser/chooser_controller/title_util_browsertest.cc


### gi...@appspot.gserviceaccount.com (2023-07-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5fb01bbdacd8fd2c2d3a59885092fdf69c40c84e

commit 5fb01bbdacd8fd2c2d3a59885092fdf69c40c84e
Author: Alesandro Ortiz <alesandro@alesandroortiz.com>
Date: Wed Jul 19 22:40:10 2023

Use committed origin instead of committed URL in device chooser dialogs

Bug: 1463149,1459281
Change-Id: Ia1d81b82b654d22d44215ecde73d8d24d27ce983
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4672069
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Commit-Queue: Zelin Liu <zelin@chromium.org>
Commit-Queue: Reilly Grant <reillyg@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1172637}

[modify] https://crrev.com/5fb01bbdacd8fd2c2d3a59885092fdf69c40c84e/chrome/browser/chooser_controller/title_util_browsertest.cc
[modify] https://crrev.com/5fb01bbdacd8fd2c2d3a59885092fdf69c40c84e/chrome/browser/chooser_controller/title_util.cc


### al...@alesandroortiz.com (2023-07-21)

Verified as fixed on 117.0.5901.0 Canary on Windows 10 using minimal PoCs in https://crbug.com/1463149#c0

### al...@gmail.com (2023-07-23)

Thank you for the fix
are the planning to add a CVE on this issue ?

If yes, please add name : Kang Ali 

Thanks

### am...@chromium.org (2023-07-24)

Closing this as fixed based on the CLs in comments #16 and #17. 


### [Deleted User] (2023-07-25)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-25)

[Empty comment from Monorail migration]

### al...@gmail.com (2023-07-27)

after Fixed and add Labels: reward-topanel

Any update for reward ?

Thanks 

### al...@alesandroortiz.com (2023-07-28)

Thanks for marking as fixed, Amy.

Does the fix need to be backmerged? If so, can someone take care of those since I don't have commit permissions?

### am...@chromium.org (2023-07-31)

re: https://crbug.com/chromium/1459281#c23: the label reward-topanel is updated automatically once an externally reported issue is closed as fixed, this issue will be assessed by the VRP Panel at a forthcoming panel discussion. A reward amount will be updated directly on the bug and communicated here after a reward decision has been made. 

### am...@google.com (2023-08-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-02)

Congratulations, Kang Ali! The Chrome VRP Panel has decided to award you $3,000 for this report of a UI spoof. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and taking the time to discover and reporting this issue to us! 

### am...@google.com (2023-08-05)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-08-08)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-09-09)

[Empty comment from Monorail migration]

### pg...@google.com (2023-09-12)

[Empty comment from Monorail migration]

### pg...@google.com (2023-09-12)

[Empty comment from Monorail migration]

### na...@google.com (2023-10-19)

[Empty comment from Monorail migration]

### na...@google.com (2023-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1459281?no_tracker_redirect=1

[Multiple monorail components: Blink>Bluetooth, Blink>HID, Blink>Serial, Blink>USB, UI>Browser>Permissions>Prompts]
[Monorail mergedwith: crbug.com/chromium/1463149, crbug.com/chromium/1463811]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40066643)*
