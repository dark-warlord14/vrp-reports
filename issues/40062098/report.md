# Security: Android - Bypass the Protection of input fields cache (Autofill) 

| Field | Value |
|-------|-------|
| **Issue ID** | [40062098](https://issues.chromium.org/issues/40062098) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Android |
| **Reporter** | el...@gmail.com |
| **Assignee** | fr...@chromium.org |
| **Created** | 2022-12-07 |
| **Bounty** | $5,000.00 |

## Description

## **VULNERABILITY DETAILS** this is a report to a security vulnerability in google chrome/chromium browser as high-quality report with functional exploit. this vulnerability allows attackers to steal the cache of input fields like usernames, e-mail addresses, telephone numbers from any site like twitter, google and any others (Chrome Autofill Saved Data).

## **VERSION** Exploit tested with the following properties: Google Chrome (Android) Version 108.0.5359.79 /Google Pixel6 Android 13.

**REPRODUCTION CASE**

the exploit use a vulnerability in showing of cache of input fields. your browser suggests the saved entries of input fields like saved user logins (username, email, phone number...) or cached search word any similar entered things.

nobody will send critical information to unknown sites. but this can be hide by full bypassing the visibility of all fields and suggests. in this case nobody are able to notice that they are sending their data to unknown attackers.

## REPRODUCTION STEPS

(Play a little Fire Game(Sniper) to get hijacked any cached input of fieldname "username",email,telephone,address,card-number,.....)

\*\*Before Repro you can add some data under chrome://settings/addresses and add some records

1-visit <https://vrphunt.com/chrome/autofill-leak-android.html>

\*\* Back Button/Gesture to Hide Keyboard\*\*

2- Tab on Game Body (White) , Then Tab on Sniper Cross point(+) to fire Moving Part.

3-Scroll Left to see Green Box with Autofill Data will be sent to Attacker Side

Autofill data Will be shown in the Green Box

# ========= Observed:

Autofill popup can be docked as a Horizontal narrow line because there is no space to expand to it's normal size

# Expected:

Sensitive browser UI is always visible to user ,so Hide Autofill popup can't be Docked/ or made hidden as a line and user should see

# Fix:

Hide Autofill Popup while it's Height is too narrow to see its content/nature , as user can't see it and expect it's ahorizontal line.

Poc Video shows the behavior and How attack works with two Clicks

======  

Notes:

This is Similar to

## <https://crbug.com/chromium/1358647> and <https://crbug.com/chromium/1108181>

**CREDIT INFORMATION**  

Reporter credit: Ahmed ElMasry

---

Thank you for your attention. with kind Regards

## Attachments

- deleted (application/octet-stream, 0 B)
- [autofill-leak-android.html](attachments/autofill-leak-android.html) (text/plain, 5.4 KB)
- [autofill-leak-android-nogame.html](attachments/autofill-leak-android-nogame.html) (text/plain, 4.2 KB)
- [minimal-PoC_07122022_224825.mp4](attachments/minimal-PoC_07122022_224825.mp4) (video/mp4, 1.1 MB)
- [autofill-leak-android-dynamic.html](attachments/autofill-leak-android-dynamic.html) (text/plain, 4.5 KB)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2022-12-07)

[Empty comment from Monorail migration]

### ad...@google.com (2022-12-07)

I can't reproduce this on my Pixel 5, with Chrome 108. I think the screen layout just ends up being different: the grey bar doesn't line up with the green ellipse as shown in your video. Moreover, the autofill pop up always appears on my screen, so I am always consciously making a decision to input a given address.

Do you think you could come up with a simpler example that doesn't involve a game, and has no dependencies on screen layout?

### el...@gmail.com (2022-12-07)

adetaylor@

Ok, I'll refine the poc yo match size of Pixel5 .., as pixel5 has smaller screen than pixel6

>>the grey bar doesn't line up with the green ellipse as shown in your video

++Okay , i'll match the two colors.

>>Do you think you could come up with a simpler example that doesn't involve a game

++Ok , I'll do plain one for you ,i've used a game to be more convincing, and shows how the attack happens .

Thanks 


### ad...@google.com (2022-12-07)

Thanks! Yep I can see how the game makes it more convincing, but a really simple POC with the minimum possible code, which works on any device, would be really useful.

### ad...@google.com (2022-12-07)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Autofill]

### el...@gmail.com (2022-12-07)

Hi..,
adetaylor@

I've created a minimal code for the poc without game part at  https://vrphunt.com/chrome/autofill-leak-android-nogame.html

and I've set opacity for the input to 1 to be visible for you , and also i've attached a poc video that show you the docked Auofill popup between the end of the maximized input field height (red border) and the top margin of android keyboard itself which makes the autofill popup docked in size ,, also i have  put a comment beside the line of CSS that control that difference .

height:575px; /**this line to control Height og autofill popup to be like a Line for the sniper 577 tested for pixel6**/

Sorry for the delay .., i've found my android studio stucked  while opening chrome, so i've updated 
width=device-width,height=device-height in meta tag hopefully it works on different devices well

if you found any problems you can change the height of  element name mentioned above 

decrease it bit lower by 5px to see difference yourself .,

i'll work on another Poc that Get window inner width -height of android keyboard which near 453px .

the attached poc works well on pixel6 with different screen size /font size  so i hope it works and fits any device 

please let me know ,if any info needed

Thanks

### el...@gmail.com (2022-12-07)

dynamic Poc  that uses screen.height dynamically

Online version 

https://vrphunt.com/chrome/autofill-leak-android-dynamic.html

offline  version attached both versions with comments inside .

Poc video also attached







### ad...@google.com (2022-12-08)

Thanks for the updated POCs.

I still can't reproduce the behavior you see. I think that's partly because I have a different sized phone screen, and partly because I have so many addresses in my addressbook that I get a very obvious autofill prompt.

Nevertheless I think I see what you're trying to achieve, so I'm going to pass this over to battre@ and vidhanj@ for further comment.

battre@ do you think you could add an FAQ to https://chromium.googlesource.com/chromium/src/+/main/docs/security/faq.md stating the expected defenses which autofill has against filling invisible/obscured fields? Is that even a security principle which you aim to uphold? An FAQ will help us to triage future such bugs better without just passing them straight over to you.

### [Deleted User] (2022-12-08)

[Empty comment from Monorail migration]

### el...@gmail.com (2022-12-08)

 adetaylor@ , Thank you for  your feedback , 

>>I have so many addresses in my addressbook that I get a very obvious autofill prompt.

Rep+/ it doesn't matter how much records saved  it depends how much space between the end of input field and keyboard , if there is very large space it will cover keyboard, it should be near 20px to dock it without being maximized.

actually I've Re-pro 'ed  this and sent the report  very fast with the device i already have to avoid being reported before , the main poc works well on pixel 6, because i have done all my inspection and getting view-port size for this device.

Pixel 6 have default View-port size 412 w * 915 H 
Pixel 5 have 393 w * 851 H

you have  requested a poc to be generic on all devices   which i'am already works on  because it have more dependencies to reach to be Optimal Poc without any errors 

I've  realized all dependencies that can affect the PoC accuracy  and I've  figured out  steps that i'll Achieve to  make the PoC more precise in  layout adaption 

Sequence:
=========
1-make  user tab on a hidden field to just show the keyboard  this tab  will get Keyboard Boundaries width , height  to use height later  (Keyboard_height)
2-getting Viewport Height using screen.height (device_viewport_height)
3- construct Equation for Dynamic Settle UI (setting the Height of #name input field precisely "Input_height_name" ) to dock the autofill row between keyboard and the end of input field.

Equation will be like
=================

Input_height_name=device_viewport_height - (Keyboard_height + Desired_autofill_height) 

**where Desired_autofill_height is  how much we want to show the height of Autofill row **

this Sequence /Equation Guarantee change layout adaption for different devices ,Guarantee this also if user uses (navigation Buttons home back)/(navigation Gestures) , and also guarantee the change if user uses Gboard keyboard or using Microsoft Swiftkey Keyboard,...etc

Sorry for not having Pixel5 device to refine the poc for you to repro the case from yourside but i'am working on that  with the sequence and avoid the dependencies on correct way .

Mitigation :
=========
**We Should Force Autofill data minimum Height to not being Obscured , if the height isn't Sufficient to see at least one Row  Dismiss it immediately , to protect User as user Should see what he select  ,and avoid sending data to attackers without being aware.**


Thanks for your time and Triage, hope this fixed .


### ba...@chromium.org (2022-12-08)

[Empty comment from Monorail migration]

### ba...@chromium.org (2022-12-08)

I chatted with fhorschig@. The replacement of the autofill dropdown, the keyboard accessory, is currently at 1% stable. In ~1 week we will know whether we can roll it out fully.

### ba...@chromium.org (2022-12-08)

https://source.chromium.org/chromium/chromium/src/+/main:ui/android/java/src/org/chromium/ui/widget/AnchoredPopupWindow.java;l=452;drc=fcc13b7aa51f368288cef07876d95567a0e16125 may be a choke point - either by closing the dropdown if there is not enough space or by closing it in onPreLayoutChange.

If we do this, we still need to be careful about the double-tap attack that we had on desktop.

### [Deleted User] (2022-12-08)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ml...@chromium.org (2022-12-14)

[Empty comment from Monorail migration]

### ml...@chromium.org (2022-12-14)

[Empty comment from Monorail migration]

### el...@gmail.com (2022-12-19)

Hi  
adetaylor@  , battre@

As per Request in Comment C4  

>>Yep I can see how the game makes it more convincing, but a really simple POC with the minimum possible code, which works on any device, would be really useful.

And My Explanation  for the seqence for a  generic Poc  works for all devices at Comment C10, i've finished  it and tested it in many devices (Realme XT , Pixel6 , Huawei Nova7i ) with different ViewPort size and screen ratios , and i have also tested with different Keyboards than G-board , like Microsoft Swiftkey with it's height expansion and the poc adapts very well, also i have tested G-voice Keyboard.


**I have made all elements opacity 1to be shown to see how it adapts and works ,for easy debugging also removed Game **

Apis used in the Seqence mentioned before:
====================
1-Virtual Keyboard Api ,to get Keyboard Boundaries width , height as we need height.

2-Visual Viewport API to get the exact viewport height for different devices and some other offsets (VisualViewport.height)

Sequence:
=========
1-make  user tab on a hidden field to just show the keyboard  this tab  will get Keyboard Boundaries width , height  to use height later  (Keyboard_height)

2-getting Viewport Height using VisualViewport.height (device_viewport_height)

3- construct Equation for Dynamic Settle UI (setting the Height of #name input field precisely "Input_height_name" ) to dock the autofill row between keyboard and the end of input field.

Equation will be like
=================

Input_height_name=device_Visual_viewport_height - (Keyboard_height + Desired_autofill_height) 

I've attached a PoC Video showing all mentioned tests to proof that the poc works efficient and smooth, last min in poc shows different keyboard transition tests and how the poc also adapt with.

Poc Repro Video Url
=================
https://drive.google.com/file/d/1N0AQzR7geo0EsRbS8wQLkuLrs76WHcp-/view?usp=drivesdk

Poc Url 
======
https://vrphunt.com/chrome/dyn-autofill/plain-dynamic.html

Instructions to Repro
============
1-Visit PoC URL above 

2-Tab on Green Box (dummy input field)  to Get keyboard boundaries and set height for name field.

3-Tab on Red Box (name input field)

4-horizontal docked autofill row will be shown as video shows (Sniper horizontal line for game )

Sorry for the delay , but i need to figure out all dependancies with right way  to produce best PoC that fit all Devices with different orientations and screen size.

Hope this helps you and hope this fixed as soon as possible, and if any further information required just let me know..

Thanks

### [Deleted User] (2022-12-22)

lizapopova: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-02)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@gmail.com (2023-01-09)

Friendly Ping: lizapopova@ mlerman@  any further updates?, Is this under your radar?

Thanks

### fr...@chromium.org (2023-01-10)

It's on our radar and potential fixes are in flight — https://crrev.com/c/4123739 is in review but it's a bit chaotic (a colleague took it over, now I take it back).
It addresses several issues at once and should fix this by enforcing a minimum height.

### el...@gmail.com (2023-01-10)


Thanks for your feedback, appreciate your hard work in advance, have a great day.

### gi...@appspot.gserviceaccount.com (2023-01-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ecb69170adf18eee62195b931b83da8d0f5554d1

commit ecb69170adf18eee62195b931b83da8d0f5554d1
Author: Friedrich Horschig <fhorschig@chromium.org>
Date: Fri Jan 20 14:32:50 2023

[Android] Fix popup bounds to honor top and bottom controls

(Copy and continuation of https://crrev.com/c/4101981)

This CL makes the anchored popup view check the webcontents rect
if one is available.
This prevents overlay of the keyboard or the Omnibox as shown in
https://crbug.com/856040#c9 and reacts to live changes of the
available space (e.g. after rotation or accessory animation).

Additionally, it ensures a minimal Popup size of 50x50dip which
prevents the popup to show up and be selectable when contents are
not readable.

Known issues:
- Fairly large for a potential merge.
- If web contents scroll, the popup disappears; seems pre-existing.

Images and video in https://crbug.com/856040#c10 and https://crbug.com/chromium/1398579#c9

Fixed: 856040, 1274887, 1398579
Change-Id: I0f4f2f3091392dddfb309d4abd405ad8df49cd40
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4123739
Reviewed-by: David Trainor <dtrainor@chromium.org>
Reviewed-by: Dominic Battré <battre@chromium.org>
Commit-Queue: Friedrich Horschig <fhorschig@chromium.org>
Reviewed-by: Bo Liu <boliu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1095024}

[modify] https://crrev.com/ecb69170adf18eee62195b931b83da8d0f5554d1/chrome/android/javatests/src/org/chromium/chrome/browser/autofill/AutofillUnitTest.java
[modify] https://crrev.com/ecb69170adf18eee62195b931b83da8d0f5554d1/ui/android/junit/src/org/chromium/ui/widget/AnchoredPopupWindowTest.java
[modify] https://crrev.com/ecb69170adf18eee62195b931b83da8d0f5554d1/android_webview/java/src/org/chromium/android_webview/AwAutofillClient.java
[modify] https://crrev.com/ecb69170adf18eee62195b931b83da8d0f5554d1/ui/android/java/src/org/chromium/ui/widget/AnchoredPopupWindow.java
[modify] https://crrev.com/ecb69170adf18eee62195b931b83da8d0f5554d1/chrome/android/chrome_java_sources.gni
[modify] https://crrev.com/ecb69170adf18eee62195b931b83da8d0f5554d1/components/android_autofill/browser/java/src/org/chromium/components/autofill/AutofillProvider.java
[modify] https://crrev.com/ecb69170adf18eee62195b931b83da8d0f5554d1/ui/android/java/src/org/chromium/ui/DropdownPopupWindow.java
[add] https://crrev.com/ecb69170adf18eee62195b931b83da8d0f5554d1/chrome/android/java/src/org/chromium/chrome/browser/autofill/WebContentsViewRectProvider.java
[modify] https://crrev.com/ecb69170adf18eee62195b931b83da8d0f5554d1/ui/android/java/src/org/chromium/ui/DropdownPopupWindowImpl.java
[modify] https://crrev.com/ecb69170adf18eee62195b931b83da8d0f5554d1/chrome/android/java/src/org/chromium/chrome/browser/autofill/AutofillPopupBridge.java
[modify] https://crrev.com/ecb69170adf18eee62195b931b83da8d0f5554d1/components/autofill/android/java/src/org/chromium/components/autofill/AutofillPopup.java
[modify] https://crrev.com/ecb69170adf18eee62195b931b83da8d0f5554d1/components/browser_ui/widget/android/java/src/org/chromium/components/browser_ui/widget/ContextMenuDialogUnitTest.java


### [Deleted User] (2023-01-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-21)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-26)

Congratulations on another one, Ahmed! The VRP Panel has decided to award you $5,000 for this report. Thank you for your efforts in reporting this issue to us -- great work! 

### el...@gmail.com (2023-01-27)

Thank You so much Amy for the Reward🙂

### am...@google.com (2023-01-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-06)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-07)

[Empty comment from Monorail migration]

### pg...@google.com (2023-03-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1398579?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062098)*
