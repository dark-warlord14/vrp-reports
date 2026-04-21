# Security: Bypass the Protection of  PaymentRequest dialog saved chrome Data, Bypass of Issue 1403539

| Field | Value |
|-------|-------|
| **Issue ID** | [40940854](https://issues.chromium.org/issues/40940854) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media>PictureInPicture, Blink>Payments |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | el...@gmail.com |
| **Assignee** | ro...@google.com |
| **Created** | 2023-11-08 |
| **Bounty** | $2,000.00 |

## Description

# **VULNERABILITY DETAILS** :

This Issue is an interesting Bypass for (<https://crbug.com/chromium/1403539>) and i've used same attack vector of (<https://crbug.com/chromium/1358647>) that recently fixed , and made a very convincing PoC , which is similar to real life attack scenario.

\*\*(so Please Add Same Folks of 1403539 to take the ownership of this issue)\*\*

\*\*Please Add Meduim Severity as per Severity Guidelines for Security Issues `https://www.chromium.org/developers/severity-guidelines/#medium-severity`,referencing to Main Issue Bypassed before <https://crbug.com/chromium/1403539> \*\*

This is a report to a security vulnerability in google chrome/chromium browser as high-quality report with functional exploit. this vulnerability allows attackers to steal saved data which is used in payment sheet dialog UI (shipping Address Saved data) like addresses, e-mail addresses, telephone numbers,...etc from Chrome (Chrome Saved Data).

## ===================== **VERSION** :

Exploit tested with the following properties:

Google Chrome Version: 120.0.6090.0  

Channel:Dev  

Milestone: 120  

Branch: 6090  

Branch Base Position: 1215263  

Google Chrome: 120.0.6090.0 (Official Build) dev (64-bit)  

Revision: 6ddf75e883b7682c7c4f262b00ba04df8bd1e35e-refs/branch-heads/6090@{#1}  

OS: Linux

---

# Google Chrome Version: 120.0.6051.2 Channel: Dev Milestone: 120 Branch:6051 Branch Base Position: 1206341 Google Chrome: 120.0.6051.2 (Official Build) dev (64-bit) 0 Revision: 75e545cf7ce76506ad3d2a5736ef28053af4a7f7-refs/branch- heads/6051@{#4} OS: Linux

## Bisection:

[1]- <https://chromium.googlesource.com/chromium/src/+/87cf1589bb30dde902d74657840c8486b605a9b1>  

`which introduced at https://crbug.com/chromium/1358647 as a part of fix there but we can benfit from this CL here` , this Commit introduces

Add GetWindowBounds for PictureInPicture  

The window bounds would be used to check for any overlaps with the  

Autofill popup in the next CLs.

this Commit is a part of fixing this issue , as we need to check intersection between picture in picture window bounds and payment Sheet dialog UI , if there is intersection between them we should dismiss this Dialog immediately to protect user from interacting with the UI without being aware, or seeing it at all.

the above Commit used in Hiding Autofill popup while intersection with picture in picture overlay as introduced in the following commit which may help you how commit [1] is used there

[2]- <https://chromium-review.googlesource.com/c/chromium/src/+/4737994>  

`Hide Autofill Popup if hidden behind Pip window`

## ==================== Root Cause Analysis:

Idea of Attack and How Attack works:  

**-------------------------** -----------  

after landing to main Poc at <https://vrphunt.com/chrome/payment-spf/payment-poc-spoofing.html> this poc simulates an online gaming website for different games , and user can scroll and select any of them , and once user select(click on) any game image this what likely happening in details:

1-Document PIP Window appears with the Clicked Game (selected by user), which have consistent UI to Payment Sheet Color , and user will feel that he/she near playing the game (I made it very convincing) :) to match real life attack.

2-The Game PIP document shown have a `Click to start` button to let user Start loading this game , and Once this button Clicked  

A) popup window will appear under this Document-PIP Overlay with same Style , and seems to be a part of this overlay, and at same time Loading progress bar start loading game for another convincing step.  

B) at the time of showing progress bar there are some game Instruction shown to Start (Press ENTER , ans Click Continue )  

, at this point the popup behind the PIP overlay is always focused and listen fot the key events , so when user press enter it will trigger Payment sheet to be Shown behind the PIP overlay, and clicking Continue will accept the payment information selected inside the payment sheet, and sending them to attacker Side.

PTL to Poc Video Attached for Repro.

## ===================== **REPRODUCTION CASE** :

the exploit use a vulnerability in showing of cache of input fields. your browser suggests the saved entries of input fields like saved user logins (username, email, phone number...) or cached search word any similar entered things.

nobody will send critical information to unknown sites. but this can be hide by full bypassing the visibility of all fields and suggests. in this case nobody are able to notice that they are sending their data to unknown attackers.

# ===================== REPRODUCTION STEPS:

(Play an Online game to get hijacked any saved payment shipping info like Addresses ,email,telephone,address,etc.....)

\*\*Before Repro you can add some data under chrome://settings/addresses and add some records

1- Visit <https://vrphunt.com/chrome/payment-spf/payment-poc-spoofing.html> (Scroll and select your GAME)

2- Game Window (PIP document) will shown ,Click `Click to Start` button to start loading

3- Follow Game Instructions (Press Enter and Continue).

\*\* Payment sheet data (Saved in chrome) Will be shown in the hidden popup window , Which Could be sent to Attacker Remote Side \*\*

---

- Feel free to test with Online POC , Also Offline File is also attached.  
  
  ==========================  
  
  Observed (What's Go wrong):  
  
  ===========================  
  
  Payment dialog sheet (UI) can be hidden, as popup not visible to user and fully Covered by Doument-Picture-in-Picture Overlay and this bypasses chrome security measures in sensetive data UI (Payment sheet UI), which contains user Sensitive data saved in Chrome.

# Expected:

Sensitive browser UI (Payment dialog sheet (UI)) is always visible to user ,so Hide Payment sheet if it overlaps with Picture in Picture Overlay.

# ===================== Mitigation:

We need to Check whether Payment dialog sheet (UI) overlaps with picture-in-picture window , and if so Hide the Payment dialog sheet (UI) immediately , with help of mentioned `Commit[1]` above.

-All POC Videos Attached, Stable and DEV Channels  

-All POc Files Attached , Feel free to test with Online POC.  

-if you want to test with your server you need to host the file at https server (Online is Better).

# ===================== **CREDIT INFORMATION** Reporter credit: Ahmed ElMasry

Thank you for your attention. with kind Regards

## Attachments

- [Payments-Leak-Info-Linux-DEV-V120-2023-11-08_13-55-43.mp4](attachments/Payments-Leak-Info-Linux-DEV-V120-2023-11-08_13-55-43.mp4) (video/mp4, 2.2 MB)
- [Payments-Leak-Info-Linux-Stable-V118-2023-11-08_13-50-52.mp4](attachments/Payments-Leak-Info-Linux-Stable-V118-2023-11-08_13-50-52.mp4) (video/mp4, 2.1 MB)
- [payment-poc-spoofing.html](attachments/payment-poc-spoofing.html) (text/plain, 6.9 KB)
- [payment-pop.html](attachments/payment-pop.html) (text/plain, 2.0 KB)
- [Repro-V120-DEV-Linux--2023-11-09_09-24-10.mp4](attachments/Repro-V120-DEV-Linux--2023-11-09_09-24-10.mp4) (video/mp4, 5.3 MB)
- [Repro-V118-Stable -Linux2023-11-09_09-21-44.mp4](attachments/Repro-V118-Stable -Linux2023-11-09_09-21-44.mp4) (video/mp4, 5.1 MB)
- [Screenshot 2023-11-09 at 3.08.40 PM.png](attachments/Screenshot 2023-11-09 at 3.08.40 PM.png) (image/png, 3.2 MB)
- [Screenshot_20241029-172947.png](attachments/Screenshot_20241029-172947.png) (image/png, 527.4 KB)
- [Screenshot_20241029-184710.png](attachments/Screenshot_20241029-184710.png) (image/png, 415.5 KB)

## Timeline

### [Deleted User] (2023-11-08)

[Empty comment from Monorail migration]

### es...@chromium.org (2023-11-09)

This sounds plausible, however I can't reproduce on Mac or Linux. I don't get the little popup with the Continue button. Are there any further instructions you can provide for reproducing?

### el...@gmail.com (2023-11-09)

Hello  est...@ ,
thanks for trying to repro the issue, and hope this info will help you again in repro.

>>I don't get the little popup with the Continue button.
Rep:/  this popup is showing on my repro and i tested it again  one more time , if this popup (which contains continue button of payment dialog) isn't showing , may be you have (popup blocker) or you need to reset site permissions  (by pressing Lock icon in omnibox beside site name and click site settings and reset permissions), by in normal state it is showing without any problems.

In normal Repro the following steps which mentioned in main comment is sufficient to repro the case without problems , 

PLEASE : Use the online Version to Repro the Case because payment request  manifest should be hosted on https website with origin restriction , Don't go for this ```Just Use the Online Version to Repro  is sufficient and good```

--------------------------------
**Before Repro you can add some data under chrome://settings/addresses and add some records   ```You need to add full details here```

1- Visit https://vrphunt.com/chrome/payment-spf/payment-poc-spoofing.html ( select any GAME image)

2- Game Window (PIP document) will shown with the selected game image and have button ``Click to Start``   Click that button to start loading game

**once the button clicked  the popup will be shown  behind the PIP Overlay as it it triggers window.open "straight forward"

3- Follow Game Instructions (Press Enter and Continue). ( pressing Enter will trigger the PaymentRequest dialog to be shown and Continue button is the button of the payement dialog itself but behind the overlay of PIP 'picture in picture ').

-------------------------------

I've attached  another POC Video Reproducing the Case in ``Ubuntu Linux Machine``  Showing Mouse Cursor interaction from my video recorder to help you in repro , PTL.

---------------
-Also if you have any problems with Repro Just Send me  screen recording from your side to show what is the problems facing you.
----------------
Thanks
 

### [Deleted User] (2023-11-09)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### es...@chromium.org (2023-11-09)

I still can't reproduce; on Mac I get no popup and on Linux I have another dialog that doesn't have a Continue button (see screenshot).

Nevertheless, I'll tentatively triage this and pass it to PiP and PaymentRequest owners to see if they understand what's going on. I'm not sure if the dialog with the "Continue" button is a Payment Request thing or a PiP thing.

### [Deleted User] (2023-11-09)

[Empty comment from Monorail migration]

### sm...@chromium.org (2023-11-09)

[Empty comment from Monorail migration]

### sm...@chromium.org (2023-11-10)

This looks roughly feasible to me, but Rouslan can you take a look as well? From the video (Payments-Leak-Info-Linux-DEV-V120-2023-11-08_13-55-43.mp4) what I think is happening is: 

1. [0:33] Main frame opens a PiP
2. [0:36] When the user clicks on the PiP, the main frame (?) then opens a pop-up window, positioned at the same location as the PiP, that (somehow?) appears *underneath* the PiP but above the main frame. (Maybe this is expected behavior for a pop-up window?).
3. [0:39] Pop-up window frame then executes a PaymentRequest call.
4. [0:39] The majority of the PaymentRequest UI is hidden behind the PiP, but the dialog is taller than the PiP so the bottom section of the PaymentRequest dialog sticks out the bottom of the PiP.
5. [0:42] The user clicks on the Continue button from the PaymentRequest dialog that is mostly behind the PiP. This resolves the PaymentRequest and returns user info to the pop-up window.

If PiPs are 'meant' to obscure pop-up windows, it's not clear to me in general how we should be protecting against this. Instead of a browser API like PaymentRequest, I could instead open a pop-up window to (for example) an oauth URL getting you to sign-in to my site with your Google Account and share your details with me - again the continue button (this time website HTML on the oauth dialog) is often at the bottom and so could be made to 'stick out' the bottom of the PiP.

One known issue that might make Payment Request more vulnerable is https://crbug.com/chromium/1283234, where Payment Request escapes the pop-up bounds on Mac and Linux (it gets cropped on Windows). If we had Windows behavior everywhere this *might* be a bit safer, BUT I'm not convinced you couldn't just have a slightly taller pop-up window and still do this attack?

Can anyone from PictureInPicture team explain the security model wrt PiP overlaying pop-up windows?

[Monorail components: Blink>Media>PictureInPicture Blink>Payments]

### ro...@chromium.org (2023-11-10)

This could be related to https://crbug.com/chromium/1476497 - "Picture-in-picture can display on top of payment sheets". According to that bug report, our plan is to dismiss PaymentRequest when picture-in-picture shows (and do not allow PaymentRequest when picture-in-picture shows.)

### [Deleted User] (2023-11-10)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-11-10)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@gmail.com (2023-11-20)

Hello rouslan@ Rouslan.,
This is a friendly reminder to check if there is any updates here , have you started working on this issue?
Could you please prioritize and hope this fixed soon.
Thank you!

### ro...@google.com (2023-11-20)

Waiting for crrev.com/c/5041595 and crrev.com/c/5041437 to land, so I can use their features to observe PiP.

### [Deleted User] (2023-11-24)

rouslan: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ro...@google.com (2023-11-27)

Waiting for crrev.com/c/5041437 to land.

### ro...@google.com (2023-11-27)

(also, the issue was updated 7 days ago, sooo...)

### el...@gmail.com (2023-12-03)

Hello rouslan@ Rouslan.,
Just a friendly reminder, 
crrev.com/c/5041595
crrev.com/c/5041437
Was landed and merged successfully, will start working on this soon :)

Thank you 

### [Deleted User] (2023-12-08)

rouslan: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### el...@gmail.com (2024-01-09)

Hello rouslan@ Rouslan.,
This is a friendly reminder to check if there is any updates here , will you start working on this issue soon?
Thank you!

### ro...@chromium.org (2024-01-16)

This is on my radar. Thank you for the reminder.

### is...@google.com (2024-01-16)

This issue was migrated from crbug.com/chromium/1500602?no_tracker_redirect=1

[Multiple monorail components: Blink>Media>PictureInPicture, Blink>Payments]
[Monorail components added to Component Tags custom field.]

### ps...@google.com (2024-02-13)

Hello rouslan@,

Is there any updates regarding the progress of this bug?

[Secondary security shepherd]
 

### ro...@chromium.org (2024-02-13)

There have been no updates, sorry. Thank you for checking.

### el...@gmail.com (2024-02-13)

Hello rouslan@,

Any plans for working on this soon?
The CLs that you will use to fix this is was rolled since December as per `#comment18`
Hope you have some empty cycles to work on this soon

Thank you

### ro...@google.com (2024-02-14)

Yes, I hope to work on this in Q1.

### el...@gmail.com (2024-03-13)

Friendly reminder Rouslan , hope this will be worked on soon
Thank you

### ro...@google.com (2024-03-13)

Thank you for the reminder :-)

### el...@gmail.com (2024-04-08)

Hello.

One more friendly ping rouslan.

Thank you

### ro...@google.com (2024-04-09)

Thank you for the ping. Still on my radar.

### el...@gmail.com (2024-05-27)

Hello.,

Is there any update regarding this bug? , Just wanted to bring this back to your attention.

Thank you

### el...@gmail.com (2024-10-09)

Hi,

**Friendly reminder**

Is there any update regarding this bug?

Thanks

### ap...@google.com (2024-10-25)

Project: chromium/src  

Branch: main  

Author: Rouslan Solomakhin <[rouslan@chromium.org](mailto:rouslan@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5955634>

Close PaymentRequest UI when picture-in-picture occludes it.

---


Expand for full commit details
```
Close PaymentRequest UI when picture-in-picture occludes it. 
 
Before this patch, picture-in-picture video could be displayed on top of 
the PaymentRequest UI (including SPC) which could confuse users. 
 
This patch adds a picture-in-picture occlusion observer to the desktop 
PaymentRequest UI, SPC authentication UI, and SPC no-credentials UI. 
When a UI is occluded, it is immediately disabled and a task to close 
the UI is posted. Posting the task is necessary because the occlusion 
could happen when initially showing the UI, when closing the UI is not 
supported. 
 
After this patch, PaymentRequest desktop UI is hidden when a 
picture-in-picture video occludes it. 
 
Bug: 40940854, 297885233, 40280009 
Change-Id: I4430e573227d746a9a246f727b48798e4590198d 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5955634 
Commit-Queue: Rouslan Solomakhin <rouslan@chromium.org> 
Reviewed-by: Nick Navarro <npnavarro@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1373855}

```

---

Files:

- M `chrome/browser/ui/views/payments/payment_request_dialog_view.cc`
- M `chrome/browser/ui/views/payments/payment_request_dialog_view.h`
- A `chrome/browser/ui/views/payments/payment_request_picture_in_picture_occlusion_browsertest.cc`
- M `chrome/browser/ui/views/payments/secure_payment_confirmation_dialog_view.cc`
- M `chrome/browser/ui/views/payments/secure_payment_confirmation_dialog_view.h`
- M `chrome/browser/ui/views/payments/secure_payment_confirmation_dialog_view_browsertest.cc`
- M `chrome/browser/ui/views/payments/secure_payment_confirmation_no_creds_dialog_view.cc`
- M `chrome/browser/ui/views/payments/secure_payment_confirmation_no_creds_dialog_view.h`
- M `chrome/browser/ui/views/payments/secure_payment_confirmation_no_creds_dialog_view_browsertest.cc`
- M `chrome/test/BUILD.gn`

---

Hash: 399b9db4d1f3dcd34554ba54cf2c54400ad4053a  

Date:  Fri Oct 25 13:08:17 2024


---

### ro...@google.com (2024-10-25)

The fix in <https://crrev.com/c/5955634> is for the desktop platforms. Although this bug report is for Linux, should it be assumed that the same issue should be fixed on Android?

### el...@gmail.com (2024-10-29)

Hello Rouslan..,

Thank you for getting back and putting fix for this one.

> For Android it's different and the attack not working , as the method (Api) used for desktop platforms is `Document Picture-in-Picture API` which isn't supported for android.
> 
> > Reference here: <https://developer.mozilla.org/en-US/docs/Web/API/Document_Picture-in-Picture_API#browser_compatibility>
> > I'll double Check and Verify the fix after landing in Dev version at Linux Once landed.
> > **if there is no more work to do here feel free to mark this fixed**

btw T-shirt sizes XL would be fine M or L :) :) .

Thank you.

### ro...@google.com (2024-10-29)

What about the https://developer.mozilla.org/en-US/docs/Web/API/Picture-in-Picture_API for `<video>` elements? Can that be used for the attack? That is supported on Android.

### el...@gmail.com (2024-10-29)

Hello.,

Yah i'am aware of this and tested this , Android uses pip api like you mentioned, and it has many restrictions on size and position which is default at bottom right corner with fixed aspect ratio calculated base on screen , on the other hand if this pip window opened at the same time of payment sheet (UI), all the payment sheet will be visible except small part of pip , and also it requires user to select address to show the next Sheet of payment which is called 'Complete your Purchase' to select visa and so on , and if user cancel the complete your purchase sheet he will found the main UI is maximized full , so no way to be realistic attack , as user can see everything unlike desktop, as demonstrated before i was able to play with document pip and its size position to fully cover the payment ui.

### ro...@google.com (2024-10-29)

Hi,

Thank you for testing on https://rsolomakhin.github.io/pr/picture-in-picture/payment-ui/.

What do you think about the demo in https://rsolomakhin.github.io/pr/picture-in-picture/payment-handler/, which opens the payment handler directly, instead of showing the address chooser.

Sincerely,
Rouslan

### el...@gmail.com (2024-10-29)

Hi Rouslan.,

Thank you for your prompt response:)

Yah i took a look most of these methods before in this great website.

The method you mentioned make steps on ui easy but
-if we skipped that it needs installing the handler from malicious website, it's ok lets consider this and the handler was installed by user or by JIT (just in time)method, there are another important security measures here

1-android should open payment link in app preview method which almost take half of screen which is fully visible to user even if pip was open.

2-the preview window contain the full address of the website and security 🔐 icon , like in attachment below , do you think that website (blahblah.com) asking you to pay would you?, i think no :)

These security measures is good and sufficient as the payment window still fully shown in android.

### ro...@google.com (2024-10-29)

Sounds good. Closing this bug report as fixed in <https://crrev.com/c/5955634>. If the security team disagrees with this outcome, please re-open.

### sp...@google.com (2024-11-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Thank you reward for helping also demonstrate security implications of known, on-going, previously documented work (crbug.com/40280009 and b/297885233 -- security bug in internal component) in this feature.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-11-15)

Congratulations Ahmed! Thank you for your efforts and reporting this issue to us!

### el...@gmail.com (2024-11-15)

Thank you Amy!

### pe...@google.com (2025-02-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Thank you reward for helping also demonstrate security implications of known, on-going, previously documented work (crbug.com/40280009 and b/297885233 -- security bug in internal component) in this feature.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40940854)*
