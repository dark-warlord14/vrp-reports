# Security: Bypass the Protection of input fields cache (Autofill) ,and Autofill popup can be made hidden

| Field | Value |
|-------|-------|
| **Issue ID** | [40068001](https://issues.chromium.org/issues/40068001) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Linux, Windows |
| **Reporter** | el...@gmail.com |
| **Assignee** | jk...@google.com |
| **Created** | 2023-07-24 |
| **Bounty** | $1,000.00 |

## Description

# VVULNERABILITY DETAILS

This is a report to a security vulnerability in google chrome/chromium browser as high-quality report with functional exploit. this vulnerability allows attackers to steal the cache of input fields like usernames, e-mail addresses, telephone numbers Credit-Card Nums from any site like twitter, google and any others (Chrome Autofill Saved Data) without seeing the autofill popup at all which presents an issue (Bypassing Google Security measures in Chrome UI sensitive area) `Showing Autofill popup` which lead to (user information disclosure without being aware).

+Similar to <https://crbug.com/chromium/1358647> and <https://crbug.com/chromium/1108181> with different Attack Vector(Totally hide Autofill popup with rapid resize in Y direction).

+Feel free to Add some folks from these two similar issues to this one."thanks"

# What is likely happening here?

1. The page(Game popup window)listens for the `mousedown` event while clicking the cookie icon.
2. The page(Game popup window) start resizing in x and y very rapidly with max interval 5000ms , and while the page content start shaking up/down and background becomes red the attack becomes ready why?

- BECAUSE while page content shaking up and down and user was asked to press arrow down and enter in this state , what actually happens is that Autofill popup wanted to be shown but the web-content moves up/down make this disappear quickly without seeing it ,while the Enter button pressed interestingly the hidden dismissed popup choice selected and shown as alert this is the idea of attack  
  
  3-Once keyboard Arrow Down Pressed Autofill data got Selected without being shown to the user.  
  
  4- and after Enter button the alert with all Autofill Data popes up and written to html paragraph.

## Idea In Short:

(trigger showing autofill popup while web-content is resizing in `y` direction because y direction force popup to recalculate it's new position making this also always hide as the resize change is so fast, and what is go wrong is that the autofill popup accept input events Although the popup UI is totally hidden)

# ======== Impact:

User Can be Tricked to visit Attacker malicious website for Playing Game , with only 2 Key press (ArrowDown -Enter)user can select Autofill data and provide passwords and sensitive data to attacker as this data can be sent to to Attacker C&C server without suspect,nobody will send critical information to unknown sites. but this can be done here, in this case nobody are able to notice that they are sending their data to unknown attackers(user information disclosure without being aware) as Autofill popup not shown at all and ( Bypassing Google Security measures in Chrome UI sensitive area `Showing Autofill popup`) as the exploit use a vulnerability in showing of cache of input fields. your browser suggests the saved entries of input fields like saved user logins (username, email, phone number, Credit Cards,...,etc).

# ======== **VERSION**

## Exploit tested with the following properties:

## Google Chrome: 114.0.5735.198 (Official Build) (64-bit) Revision: c3029382d11c5f499e4fc317353a43d411a5ce1c-refs/branch-heads/5735@{#1394} Commit: 9fd9f7d42efeb8e92ee62a904814cec987a4b5a8 Branch Base Commit: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67 Channel:Stable Milestone: 114 Branch: 5735 Branch Base Position: 1135570 OS: Linux

## Google Chrome:114.0.5735.90 (Official Build) (64-bit) Revision:386bc09e8f4f2e025eddae123f36f6263096ae49-refs/branch-heads/5735@{#1052} Channel:Stable Milestone: 114 Branch:5735 Branch Base Position:1135570 OS:Linux

## Google Chrome: 115.0.5780.0 (official Build) canary (64-bit) (cohort:Clang-64) Revision: b9b861af96d1bbe1829520365844acc541e6b848-refs/branch-heads/5780@{#1} Branch:5780 Branch Base Position:1146239 OS: Windows 11 Version 22H2 (Build 22621.1702)

## Google Chrome:115.0.5790.3 (Official Build) dev (64-bit) Revision:32c8fb09897da1b8f8dde49364e9a589403ad9bf-refs/branch-heads/5790@{#10} Channel: Dev Branch:5790 Branch Base Position:1148114 OS:Linux

## Google Chrome: 115.0.5747.0 (Official Build) canary (64-bit) (cohort: Clang-64) Revision: bfbf32ed7b1be2d640ce1be293d964700e1b56e2-refs/branch-heads/5747@{#1} OS: Windows 11 Version 22H2 (Build 22621.1635)

## Google Chrome: 114.0.5735.6(Official Build)dev(64-bit) Channel: Dev Branch:5735 Branch Base Position: 1135570 OS: Linux

Google Chrome: 116.0.5845.32 (Official Build) dev (64-bit)  

Revision: 7fc4c1ca19f2dde309796e9dfd6149e5d41887d7-refs/branch-heads/5845@{#453}  

Channel: Dev  

Milestone: 116  

Branch: 5845  

Branch Base Position: 1160321  

OS: Linux

# ================== **REPRODUCTION CASE**

1. simply Use Online Poc ,or Host the attached files of Poc on your Server and test.
2. Navigate <https://vrphunt.com/chrome/autofill-newwork/accept-permissions.html> on Linux as Poc Show
3. Press `Click to play` button ,you will see Game popup
4. Click on the Cookie to Start Game and Follow instructions (While Page becomes RED press ArrowDown then Enter).
5. popup alert with Autofill secret data pops and written to html page (Which can be sent to Remote C&C of Attacker).

# ============== Observed:

Autofill poupup isn't shown to the user and Accepts User input events Although it's fully hidden , which make user with 2 Clicks send his sensitive data to Attacker and also Bypassing Google Security Measures in Chrome UI sensitive Areas that should be visible to user.

# Expected:

-Autofill popup shouldn't Accept User input Events while being hidden, and this sensitive Chrome UI should be visible and protected from being made fully hidden.

# Fix/Mitigation:

-Add CL to prevent Accepting User input events `before` Autofill popup shown and `after` shown .  

Before: to prevent this attack and also check popup Visibility  

After: to prevent Force user interaction or attack with double click "which already introduced".

\*\*Poc Videos of Windows/Linux Tests Directly Attached  

\*\*Local Offline POc Files Directly Attached

## =================== **CREDIT INFORMATION**

## Reporter credit: Ahmed ElMasry

Thank you for your attention. with kind Regards

## Attachments

- [accept-permissions.html](attachments/accept-permissions.html) (text/plain, 7.1 KB)
- [Autofill-Leak-Chrome-116-0-5845-32-dev-2023-07-24_18-14-34.mp4](attachments/Autofill-Leak-Chrome-116-0-5845-32-dev-2023-07-24_18-14-34.mp4) (video/mp4, 1.2 MB)
- [Autofill-Leak-Chrome-116-0-5845-32-dev-2023-07-24_18-14-34.mp4](attachments/Autofill-Leak-Chrome-116-0-5845-32-dev-2023-07-24_18-14-34.mp4) (video/mp4, 1.2 MB)
- [AutoFillLeakPoC-ChromeStableV114-Linux.mp4](attachments/AutoFillLeakPoC-ChromeStableV114-Linux.mp4) (video/mp4, 1.4 MB)
- [V115-Linux-Stable-2023-07-26_12-03-25.mp4](attachments/V115-Linux-Stable-2023-07-26_12-03-25.mp4) (video/mp4, 1.4 MB)
- [select1st-IndexHiddenRecord-2023-07-26_13-35-47.mp4](attachments/select1st-IndexHiddenRecord-2023-07-26_13-35-47.mp4) (video/mp4, 1.0 MB)
- [select-2nd-indexHiddenRecord-2023-07-26_13-39-22.mp4](attachments/select-2nd-indexHiddenRecord-2023-07-26_13-39-22.mp4) (video/mp4, 895.3 KB)
- [Linux-Dev-117-2023-08-01_17-21-17.mp4](attachments/Linux-Dev-117-2023-08-01_17-21-17.mp4) (video/mp4, 1.1 MB)
- [vokoscreenNG-2024-01-28_09-50-11.mp4](attachments/vokoscreenNG-2024-01-28_09-50-11.mp4) (video/mp4, 4.2 MB)
- [POC-down4x-2024-01-28_14-13-42.mp4](attachments/POC-down4x-2024-01-28_14-13-42.mp4) (video/mp4, 1.1 MB)
- [AfterFIX-2024-07-15_16-06-36.mp4](attachments/AfterFIX-2024-07-15_16-06-36.mp4) (video/mp4, 1.7 MB)

## Timeline

### [Deleted User] (2023-07-24)

[Empty comment from Monorail migration]

### fl...@google.com (2023-07-25)

Thank you for the detailed report; I was able to reproduce.

smcgruer@, hope it's okay to assign this for you—noticed that you've already been looking at a similar bug.

Setting a severity of medium here because of user information exfiltration, though let me know if you think the "needing the window to be resized a specific way" is a substantial enough mitigation to reduce to low.

[Monorail components: UI>Browser>Autofill]

### [Deleted User] (2023-07-25)

[Empty comment from Monorail migration]

### sm...@chromium.org (2023-07-25)

Based on the description, I think this is a general attack on the desktop autofill pop-up rather than something specific to payments, so passing over to Mike to triage + assign.

### sm...@chromium.org (2023-07-25)

[Empty comment from Monorail migration]

### ml...@chromium.org (2023-07-25)

Assigning to Jan to triage. Chris as CC for vis.

### [Deleted User] (2023-07-25)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jk...@google.com (2023-07-26)

I can reproduce on Windows , but I do not manage to reproduce on Linux or on Mac. In all cases, I see the popup UI at least temporarily.

On Linux and on Mac, the attack fails if there are less than 500 ms between cursor down and return (and the popup UI is shown in the interim).
On Windows, the EyeDropper API seems to confuse the timing.

flowerhack@: Can you reproduce on non-Windows platforms/ without the popup UI showing?

### jk...@google.com (2023-07-26)

Let me correct that: I can reproduce in Linux on an official build (developer build does not work), but it is not reliable: It may take several attempts at cursor down/ enter. (Still a problem, though).

All of the above seem to rely on the EyeDropper API confusing the counter for how long the Autofill popup has been shown.

### jk...@google.com (2023-07-26)

[Empty comment from Monorail migration]

### el...@gmail.com (2023-07-26)

Hello Jan  jkeitel@..,

Thanks for your attention and working on this Isuue..! , 

Additional Info  may help in Fixing the root cause of this:
===========================================
**I think the Autofill Popup UI is not fully protected by input event protector , Since it can Accept input events from user although being Hidden , which in fact real security lack here.**

Good Suggestions may help in Fix::
===========================
1- Autofill Popup Shouldn't Accept Input events  without being fully shown to user with at least 500ms  , this will guarantee security for this UI. 

Explain:
======
1(A):- ( "I've attached  a Poc Video to show this partial underneath behavior without pressing Enter"), after clicking the cookie icon and when popup page becomes red (shaking up and down, Press ArrowDown only ) ,you will notice that input event accepted and popup index record got selected  although autofill popup was hidden.  **select1st-IndexHiddenRecord-2023-07-26_13-35-47.mp4**

1(B):-  to show you this behavior very clear `if you have multiple  records in chrome://settings/addresses`  Repeat Step (A) But Press (ArrowDown Twice), you will see that Second Index Recod of Autofill popup got selected while the popup was hidden. **select-2nd-indexHiddenRecord-2023-07-26_13-39-22.mp4**

From Point 1 there is should be some mitigation to prevent Bypassing user geastures to select Autofill Records in this point, which can be used for another attack.

2:- Autofill Popup should be Visible and intersect web-content for 500ms , and Do not accept input events during this period.
 
I've used Same trick of subtle resizing in another issue affecting new permission prompt (other surface) and fixed by this commit 
https://chromium-review.googlesource.com/c/chromium/src/+/4604326 

==================================
About Repro and Idea of How Attack Works Explained with code :
=======
As you Know , and as i experienced after playing around this issue here and previous one in Permission prompt Surface , This is very Subtle timing Action Interruption  and it may have different behavior on each environment (Linux,Windows, and Mac"i don't have mac") , and also the behavior changes from Chrome to Chrome Version in same environment , i saw that in permission prompt and here a little bit , it rely on the behavior how the browser deal with resizing , so i have refactored the poc to mainely work on Linux as this is my main Machine  and provided the test Properties for Chrome versions above

+ Forgot to Upload stable 114 Video poc and uploaded the dev version twice by mistake ,Provided in Attachment

+ Also After Today's Update Tested with :

Google Chrome: 115.0.5790.102 (Official Build) (64-bit) 
Revision: 90efd4b0ad6aa15eeafcdabd5817ae939f7ba059-refs/branch-heads/5790_90@{#9}
OS: Linux

and Provided also Poc Video. **V115-Linux-Stable-2023-07-26_12-03-25.mp4**

+The Attack Parameters is Very Critical  Specially
 const waitBefore = 4;
const waitPerResize = 6; 

Which controls the ` waitFor()` function that do the job of resize , and as i mentioned in main description the aim to achieve the exploit here is:

with help of CalculatePopupYAndHeight we need to enter between each time doing calculation while the Y size  rapidly changes , so this function always try to calculate if there is sufficient space to show or not the popup ``as In this function, top_growth_end and bottom_growth_start are calculated to find the top and bottom positions where the popup can grow, respectively. Then, top_available and bottom_available are calculated to find the available space for the popup to grow both above and below the element, respectively.`` , and it found sufficient space and try to show popup but there are many other concequitive checks and tries to show  making no chance for the popup to be visible and underneath it accept the User input (Key press) 

**This what came to my mind after reading the function below and after testing X direction that doesn't affect the behavior , But Y is very effective as Code Show**

Code Snippet for Function

``````void CalculatePopupYAndHeight(int popup_preferred_height,
                              const gfx::Rect& window_bounds,
                              const gfx::Rect& element_bounds,
                              gfx::Rect* popup_bounds) {
  // Calculate the top and bottom positions where the popup can grow.
  int top_growth_end = NormalizeValueBasedOnBounds(
      window_bounds.y(), window_bounds.bottom(), element_bounds.y());
  int bottom_growth_start = NormalizeValueBasedOnBounds(
      window_bounds.y(), window_bounds.bottom(), element_bounds.bottom());

  // Calculate the available space for the popup to grow both above and below the element.
  int top_available = top_growth_end - window_bounds.y();
  int bottom_available = window_bounds.bottom() - bottom_growth_start;

  // Set the height of the popup to the preferred height.
  popup_bounds->set_height(popup_preferred_height);
  // Set the initial Y position of the popup to the top growth end.
  popup_bounds->set_y(top_growth_end);

  // Check if there is enough space below the element to fit the popup.
  if (bottom_available >= popup_preferred_height ||
      bottom_available >= top_available) {
    // If there is enough space below the element, adjust the popup's Y position and height
    // to fit within the available space below the element.
    popup_bounds->AdjustToFit(
        gfx::Rect(popup_bounds->x(), element_bounds.bottom(),
                  popup_bounds->width(), bottom_available));
  } else {
    // If there is not enough space below the element, adjust the popup's Y position and height
    // to fit within the available space above the element.
    popup_bounds->AdjustToFit(gfx::Rect(popup_bounds->x(), window_bounds.y(),
                                        popup_bounds->width(), top_available));
  }
}

``````
Thanks for your Attention and your time working on this.





### jk...@google.com (2023-07-27)

[Empty comment from Monorail migration]

### jk...@google.com (2023-07-28)

Hi elmasry.elec@,

I just realized that I had only tested this on stable. After trying to reproduce locally in my build (and failing), it seems to me that the measures enabled in https://chromium-review.googlesource.com/c/chromium/src/+/4613765 a few weeks seem to be working already. I therefore cannot reproduce it anymore on Canary. Yes, a popup is shown, but all enter actions are ignored until the popup has been shown for a sufficiently long time.

Can you try and reproduce it on 117.0.5876.0 and above? That means either current Dev or current Canary.

Thanks,
Jan

### el...@gmail.com (2023-08-01)

Hello Jan jkeitel@ ..,
Thanks for following up and working on this,

--I'am Happy to see this  new feature "AutofillPopupUseThresholdForKeyboardAndMobileAccept" at https://chromium-review.googlesource.com/c/chromium/src/+/4613765 got introduced in Version "117" .

--Till Report Submission date  the feature still not pushed to users as the latest Dev Version was  Google Chrome: 116.0.5845.32 (Official Build) dev (64-bit)  as mentioned in  Vesions  https://crbug.com/chromium/1467351#c0 main issue description shows and i,ve played with different version behind this too and bug Exist as shown in https://crbug.com/chromium/1467351#c0 poc Videos.

-- Today i've tested the behavior in Windows and Linux Machines  and Results as follows:

Version:
Google Chrome 117.0.5911.2 (Official Build) dev (64-bit) 
Revision	9e4d08ed29fb6458cf49ad934326dc527df5a1d0-refs/branch-heads/5911@{#4}
OS:Linux


Version
Google Chrome 117.0.5922.2
Channel: Canary
OS:Windows 10

+Windows Results:
--------------------------
-The Behavior of resize totally changed as i noticed that the popup-window stopped resizing at the state of background in RED . 
- the selection doesn't take effect in windows , after some code mod.

Win-Result: the behavior seems to be fully fixed.

++Linux Results:
-----------------------
--The Behavior of resize is same as shown before in Poc Videos.
-- While the Page in freeze at Background got in RED color the selection takes place and can select hidden (Autofill-popup) indexes 
-- so it is partially fixed why..?
Because while the AutofillPopup index selected Although the popup is fully hidden and the window in freeze time , there are many threats here How 

1-The Attacker can trigger ``requestPictureInPicture();``  at this state to cover the Autofill-popup selected index  and with pressing enter the data got leaked to attacker server.
2- Attacker Can Trick User By Merging this Technique in Playing DINO jumping Game and User could be convinced to continuous Press Enter button at the time of freeze (Autofill-Popup hidden and index selected)  for higher jump leaking user data.
==============
Suggestion for Enhancing the Experimented feature :
==============
--Key Events shouldn't be Accepted from User while there in no intersection for (Autofillpopup) and  (web-contents) to make sure that the autofill popup shown to user then accept the key inputs from user to select indexes , as selecting security data should be done while being visible to user .

-After Doing the protection at ``Input level protection`` User can be safe , as selected indexes underneath without being shown  make user exploitation achieved by 50% , but after doing the check the exploit will be harder to be done.

-- Also for Security Measures "User gestures" shouldn't be skipped or bypassed with hidden ui.


**This Serious Issue need to Be Back-merged asap to help user protection as it is reproduciable in Current (stable  , extended , beta ) versions**

Thanks for Your Work and  Attention ..


 

### jk...@google.com (2023-08-23)

[Empty comment from Monorail migration]

### jk...@google.com (2023-08-24)

Ahmed, could you try and see whether this is fixed on Chrome Canary for you? Any version that's at least 118.0.5965.0 should do it.

### el...@gmail.com (2023-08-24)

Hello Jan jkeitel@ ..,

Thanks for Getting attention and working on this..!

- From My Side I can Confirm that this Bug is Fixed.

- I've tested / play around the fix at  Latest Chrome Canary Build  with the following properties:

Google Chrome: 118.0.5967.0 (Official Build) canary (64-bit) (cohort: Clang-64) 
Revision: c2868899a533a22f76c91b9332cffd958014f2b0-refs/branch-heads/5967@{#1}
OS: Windows 10 Version 22H2 (Build 19045.3208)

- Bug Also Tested  with Some Latest Developer Builds (Snapshots) , and Seems to be Fully Fixed .

- Feel Free to Mark this as [Fixed /Verified] .

Again ,Thanks for All your efforts working and fixing this one , Have a Great Day.

### el...@gmail.com (2023-08-27)

Hello jan  jkeitel@ ..,

Continuing Testing in ,Linux Environment:
-------------------------------------------------------
-Today After Official Chrome has been released (Version 118.0.5966.0 (Official Build) dev (64-bit)) , I've tested the Bug and Results as Explained in https://crbug.com/chromium/1467351#c14  in Linux  , But in Windows it is fully fixed , so Please Double Check in Linux .
Thanks Jan 


### el...@gmail.com (2023-09-11)

Hi Jan jkeitel@ 
Friendly reminder:
any further updates/progress on this one after version mentioned in  https://crbug.com/chromium/1467351#c16 ?
I'am Ready to test any changes..,  but till Version 118.0.5993.3 (Official Build) dev (64-bit) at Linux , the behavior is same no changes were made. 
Thanks 

### el...@gmail.com (2023-10-02)

Hello Jan jkeitel@ ..,
Just wanted to check:  is this still under your radar?
Don't hear back from you since your last comment https://crbug.com/chromium/1467351#c16,Could you please check and followup?

Thanks for getting attention to this.

### jk...@google.com (2023-10-02)

I've not forgotten about this.

### el...@gmail.com (2023-10-02)

Nice to hear that, appreciate your efforts,thanks :)

### [Deleted User] (2023-10-02)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### el...@gmail.com (2023-11-08)

friendly reminder:Hello Jan jkeitel@ ..,
Just wanted to check:  is this still under your radar? , will you continue addressing this soon? 
Let me updated with progress, thank you.

### jk...@google.com (2023-11-09)

It is, but it (and other, similar reports) is currently blocked on another issue.

### jk...@google.com (2024-01-16)

Gab, this is the bug with the moving popup.

### jk...@google.com (2024-01-23)

Ahmed,

Could you ask you for your help in checking whether starting Chrome with the additional command line parameter --enable-features=AutofillPopupImprovedTimingChecks fixes the issue for you? I have never been able to actually reproduce the issue and I can therefore not test it properly.

Note that you'll need Chrome version 122.0.6260.0 or newer.

Thanks,
Jan

### el...@gmail.com (2024-01-23)

Hello Jan .,

I appreciate your swift response and working on this one. However, as of today, the specified Chrome version 122.0.6260.0  has not been rolled out on my end "Linux DEV Versions".

I will promptly conduct the suggested test using the provided command line parameter (--enable-features=AutofillPopupImprovedTimingChecks) as advised once the update becomes available and I will keep you informed of the results.

Thank you





### jk...@google.com (2024-01-23)

Hi Ahmed,

Thanks for the prompt update. I just realized that the Canary channel may not be available on Linux. It should hit Dev in a few days, though.

Jan

### el...@gmail.com (2024-01-28)

Hello Jan  jkeitel@ .,
Today After Testing the new feature in https://crbug.com/chromium/1467351#c28 i have found that the Partial behavior of https://crbug.com/chromium/1467351#c11  Still the Same nothing Changed
As per https://crbug.com/chromium/1467351#c11 and https://crbug.com/chromium/1467351#c14 explanation 

Test  Properties:
----------------------
Google Chrome: 123.0.6262.5 (Official Build) dev (64-bit) 
Revision	9dc6c13abeee0c81e5541c21f3222e5fee85e51d-refs/branch-heads/6262@{#12}
OS	Linux
JavaScript: V8 12.2.281
User Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36
Command Line: /usr/bin/google-chrome-unstable --enable-features=AutofillPopupImprovedTimingChecks

----------------------

I saw  this CL https://chromium-review.googlesource.com/c/chromium/src/+/5145027 which introduces the new feature ``AutofillPopupImprovedTimingChecks``in c28 , which seems to be not sufficient to fix this well

**I Suggest to mitigate this well , we need to go back to https://crbug.com/chromium/1467351#c0 at this part **

```
Idea In Short:
--------------
(trigger showing autofill popup while web-content is resizing in `y` direction because y direction force popup to recalculate it's new position making this also always hide as the resize change is so fast, and what is go wrong is that the autofill popup accept input events Although the popup UI is totally hidden)
```
====================
So , the main part here is resizing in y direction , so what we can do here is to monitor change in web-content size and if there is  a resize or (change) we should  dismiss the autofill popup immediately (may be this solution will have some performance issue due to the freeze of renderer at the time of  fast resizing) .
====================
Note: the resize if faster than it appears in the poc video  attached , also  the poc video showing one arrow down select 1st index in autofill and another try to select 2nd index in autofill
 

Thank you  Jan 


### jk...@google.com (2024-02-02)

Hi Ahmed,

I don't think I understand - from what I can see in your video, the Autofill UI shows, but is never accepted. Am I missing anything? We do not want to block the UI from showing, we just want to make sure that it does not get accepted unknowingly.

Thanks,
Jan

### is...@google.com (2024-02-02)

This issue was migrated from crbug.com/chromium/1467351?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/chromium/1475902]
[Monorail components added to Component Tags custom field.]

### el...@gmail.com (2024-02-06)

Hello jan,

Thank you for all your efforts working on this one

`the Autofill UI shows, but is never accepted. Am I missing anything? We do not want to block the UI from showing, we just want to make sure that it does not get accepted unknowingly.`

> > In my previous Comments , I've mentioned that while renderer freezes at the time of resizing , of course the autofill have no chance to be visible at this state but after the freeze time ended up the autofill will be shown and execute the received key strokes for example arrow up/down make the autofill indexes will be selected , also i mentioned that while the freeze state of renderer user can trigger Video Pip to cover this and after that request user to press enter .

after doing some other experiments on this , and made another poc , i found another way to accept the autofill ui and bypassing the fix of threshold made here in this commit which is "500ms" before accepting Enter

> > <https://chromium-review.googlesource.com/c/chromium/src/+/4613765>

`so , i suggest monitoring change in web-content size and if there is a resize or (change) we should dismiss the autofill popup immediately` 

i've attached a poc video for this bypass which need to be fixed also.

---

#### Stpes for the new bypass:

---

1- Visit <https://vrphunt.com/chrome/rend-autofill/online-poc-autofill-exf.html>

2- try to make the mouse move in X direction ( right to left ) one more time as you play Floppy Ping Game :) `the renderer starts to be busy and no autofill is shown` 

3- Press Arrow Down three or four times and Enter `nothing will be shown but after freeze time ended the selected index of autofill will be selected underneath and Enter key event is accepted`

> > from this we can conclude that the queue still have the key events and clculate the time of threshold if if the autofill isn't really shown on UI , and this threshold time for accepting key events which is "500 ms" is passed and bypass happen .

I'll be happy to experiment it again and again to help you fixing this with tight fix , just let me know if any further info needed.

Thanks

### el...@gmail.com (2024-02-21)

Hello,

friendly reminder: Any further updates on this one?

Thank you

### jk...@google.com (2024-02-21)

Hi Ahmed,

I am sorry, but I cannot open the videos that you sent and I still cannot reproduce what you are describing on my machines. For me, once I enable the flags, the popup is always shown for at least 500ms before any suggestions are accepted.
For what it's worth: Could you write once more with --enable-features=AutofillPopupImprovedTimingChecksV2 on the latest dev build?

Thank you,
Jan

### el...@gmail.com (2024-02-21)

Hello jan,

Thank you for your prompt response and great follow up!

---

**`First:`**

> Replying to your concern about viewing the video attached at [#Comment35](https://issues.chromium.org/issues/40068001#comment35) which show the test results of commit <https://chromium-review.googlesource.com/c/chromium/src/+/4613765> (feature : `AutofillPopupImprovedTimingChecks`) , i've uploded it to this Drive Link for better view experience
> 
> > <https://drive.google.com/file/d/1JEifxzgm_uMmZUxd20dpqrwpiEQ8Yb_G/view?usp=sharing>

---

**`Second:`**

> For [#comment37](https://issues.chromium.org/issues/40068001#comment37) , yah i saw this code change but wasn't completed yet , and was in vacation so don't have chance to test it at the time of release and also waiting your reply here to confirm end of some work to retest , but it's okay
> Now after testing the new feature improvement
> 
> > `AutofillPopupImprovedTimingChecksV2` at <https://chromium-review.googlesource.com/c/chromium/src/+/5246032> , i've found that it enhances the behavior a little bit unlike before , as the acceptance of autofill selected index becomes shown unlike before `which is fine` , but i see there is a little freeze period which cause the accumelated key events take effect at same time `sometimes` .

`Sometimes` means here it is an Edge case which could be tackled by increasing the time of threashold 600ms instead of 500ms (i've tested the key event time delay) which in opinion and tests will solve the issue

`how test happens:`
Base Case : we have 500ms between 1st key press and the seconed key press(which is ENTER in this case to accept)

> Link to test press time delay `https://jsfiddle.net/philfreo/56qGM`

The Edge Case or Previous behavior with feature flag enabled both need at least `4 times Arrowdown press` and one `ENTER` to accept.

> > Edge Case Repro Link at drive: <https://drive.google.com/file/d/1LZyC-IeKf6KaILRw629WiaXo5h6Ay0sr/view?usp=sharing>

> **For example :** `t1` is first key press start activating 500ms threshold timer ,
> `t2,t3,t4` consecutive presses are ~ +120 ms to +145ms
> and total time will be `~650ms` , as after the consequitive presses there is the Acceptance ENTER , so if the delay with 650 the Enter Press will be neglected so, this will work together with new update of the feature which i agree that it improved showing the popup unlike before.

I Just Sharing my thoughts and tests which may help you , But if You feel that there is no more work to do here just let me know and mark this as Fixed, Again i'am very happy for any further Experiments on this until reaching to Complete Fix.

Thank you

### pe...@google.com (2024-03-07)

jkeitel: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### el...@gmail.com (2024-03-13)

Hello jan jkeitel@

Any further updates on this one?

Thank you

### jk...@google.com (2024-03-13)

Hi Ahmed,

The fix from above is currently rolling out as an experiment. We're being more careful with this one than most other fixes to make sure nobody is impacted negatively. I'd expect it to be on 100% by mid-April.

Jan

### pe...@google.com (2024-03-27)

jkeitel: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### jk...@google.com (2024-05-02)

Hi Ahmed,

This should now have reached 100% stable on the current stable build. Could you please verify that it is working as expected?

Thanks,
Jan

### el...@gmail.com (2024-05-08)

Hello Jan .,

Thank you for your time working on this one.

After doing some tests on this >>version 126.0.6452.3 >> 1294836 @ May 3 2024

I've found that the Issue is partially Fixed and the new behavior that was mentioned in [#comment38](https://issues.chromium.org/issues/40068001#comment38) is still working .

Any Further info required i'am here ready to dig more if you like .

Thanks

### jk...@google.com (2024-07-09)

Hi Ahmed,

I have recently made another change that should prevent this attack. It is included in `128.0.6562.0` and newer. Could I ask you to try again? I still fail to reproduce it locally (on any OS), which makes it impossible for me to verify.

Thank you,
Jan

### el...@gmail.com (2024-07-09)

Hello Jan,

I noticed some of your recent changes a few days ago testing and producing this Feature `kAutofillPopupMeasureTimeAfterPaint` , and have been waiting for your feedback after you complete your work. 😊

- Version `128.0.6562.0` hasn't been released for Linux yet, so I'll wait for it to land and will certainly give it a try. I'll explore it further and share my findings here.

Your efforts are much appreciated, Jan. Thank you!

### jk...@google.com (2024-07-09)

Oh, sorry, I should have checked channels before - I had assumed that it was on dev by now. It should arrive soonish.

Thank you Ahmed!

### el...@gmail.com (2024-07-15)

Hello Jan.,

`Update:`

- After Testing the last Update on Dev Channel for Linux @Version 128.0.6585.0
- `Result`: now It's hard to Achieve the Exploit again on Linux as Shown in the attached video,after Fix.

---

CL which i took a look for future tests and retrace as a reference:

> Add feature to delay popup shown measurement until view is painted
> 
> <https://chromium-review.googlesource.com/c/chromium/src/+/5645183>

> Treat AutofillPopupMeasureTimeAfterPaint as kill switch.
> 
> <https://chromium-review.googlesource.com/c/chromium/src/+/5657114>

---

Thank You Jan for your hard work which is much appreciated.

### jk...@google.com (2024-07-16)

Hi Ahmed,

Unfortunately, I cannot open your video. Are you saying that the exploit is now prevented? The popup should be showing for 500 ms before any suggestions become acceptable.

Thanks,
Jan

### el...@gmail.com (2024-07-16)

Hi Jan,

> No problem, Uploaded the video to my drive at the link below
> 
> <https://drive.google.com/file/d/1VbtVfLiGhCpSq5-mMCwDJ1fV5dWguS6Y/view?usp=sharing>

> Are you saying that the exploit is now prevented?
> 
> - for now ,`Yes it is prevented.`
> - I'll keep my eye on it testing again and again and if something new found I'll Ping you here .

Thank you

### jk...@google.com (2024-07-16)

Ahmed,

Thank you for sharing the video - I was able to open it. One more question: At 0:40 it very briefly shows your name in the input field - how did that happen?

Thanks,
Jan

### el...@gmail.com (2024-07-16)

Aha, i saw that and still searching code to know why ,autofill 1st record index is shown for a second without popup but not accepted (it is false positive) as i tested many times and this not happened ,so that i mentioned I'll keep my eye on it testing again and again.

> - I'll try to load more and more on the browser renderer (simulating a heavy game) to observe how it behaves.

### el...@gmail.com (2024-08-05)

`Info:` This is a good logic made By Dima , hope it works well, waiting for it to re-test

> <https://chromium-review.googlesource.com/c/chromium/src/+/5748574>

### el...@gmail.com (2024-10-09)

Hello Jan,

**Friendly reminder**

Is there any update regarding this bug?

Thanks

### ph...@chromium.org (2025-01-02)

[Secondary security shepherd] Hi jkeitel@: Do you have any updates for this bug? What can we do to bring this bug closer to resolution? [will schedule a direct ping too]

### jk...@google.com (2025-01-07)

I have not been able to reproduce the issue - I'd therefore mark this as fixed. The spurious name that appeared (see my comment in #51) still confuses me, though.

### pe...@google.com (2025-01-07)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### jk...@google.com (2025-01-07)

Since this bug appears to have had the same root cause, I am marking it as a duplicate of [crbug.com/40279821](https://crbug.com/40279821). The rewards panel should determine whether it deserves an independent reward.

### am...@chromium.org (2025-01-21)

We'll need to un-dupe this issue for a bit to allow our automation to keep this tagged as `reward-topanel` which allows it to be in our queue and make assess it for VRP. I will re-merge it as a duplicate once that process has been completed, likely sometime next week (since this missed the cutoff for inclusion this week).

### pe...@google.com (2025-01-21)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2025-02-27)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2025-03-06)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of highly mitigated user information disclosure / exploitation mitigation bypass, mitigated by precondition of specific resizing conditions and sufficient user gesture to allow an attacker to take advantage of this issue and result in harm to someone using Chrome


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-03-06)

Congratulations Ahmed! Thank you for your efforts and reporting this issue to us!

### el...@gmail.com (2025-03-06)

Thank you Amy

### ch...@google.com (2025-06-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40068001)*
