# Security: Bypass the Protection of input fields cache (Autofill)  due to inappropriate code design (Bypass 1108181)

| Field | Value |
|-------|-------|
| **Issue ID** | [40065003](https://issues.chromium.org/issues/40065003) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P3 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | el...@gmail.com |
| **Assignee** | vy...@google.com |
| **Created** | 2023-05-30 |
| **Bounty** | $6,000.00 |

## Description

# **VULNERABILITY DETAILS**

this is a report to a security vulnerability in google chrome/chromium browser as high-quality report with functional exploit. this vulnerability (Bypass of <https://crbug.com/chromium/1108181)and> similar to <https://crbug.com/chromium/1358647> which allows attackers to steal the cache of input fields like usernames, e-mail addresses, telephone numbers from any site like twitter, google and any others (Chrome Autofill Saved Data).

# Root Cause Analysis and Bug Exist History:

Actually this bug found because of the commit for (<https://crbug.com/chromium/1108181>) at <https://crrev.com/65bbe7edda8c9065c9c254ada2da1af7cd5776b6> which was landed in chrome version 85.0.4183.0 , this commit introduces "Suppress autofill dropdown when there is insufficient space"  

and in this file there is a test for that <https://chromium-review.googlesource.com/c/chromium/src/+/2323392/15/chrome/browser/ui/views/autofill/autofill_popup_view_utils_unittest.cc> which check at least one row height to be shown to the user if not the auto-fill popup will be dismissed and in <https://chromium-review.googlesource.com/c/chromium/src/+/2323392/15/chrome/browser/ui/views/autofill/autofill_popup_base_view.cc> ther is this code part for this check

```
 // area so that the user notices the presence of the popup.  
 int item_height =  
     children().size() > 0 ? children()[0]->GetPreferredSize().height() : 0;  
 if (!HasEnoughHeightForOneRow(item_height, GetContentAreaBounds(),  
                               element_bounds)) {  
   HideController(PopupHidingReason::kInsufficientSpace);  
   return false;  
 }  

```
# , from here we can set point one to chain to have a complete exploit to make the user interact and send auto fill without seeing the data he/she select "or make the user will not notice the presence of the popup" how can we hide this one row data? we can make the data of auto-fill be hidden and only show (Mange...) and merge this with the game/menu style to be not seen at all, the behavior behind this is that if we make "autocomplete=''" null the auto fill data that the user will interact will be shown and user will not fall in this attack , so we make the autocomplete have a value of the data we need to extract from user autofill records for example autocomplete="tel" so this attribute will override name attribute and also hide the data and only show (Manage...) make this unnoticeable if it was put in same style game menu like in poc , and when the user press arrow down the selection going underneath but nothing shown to the user because Manage word is fixed and no gesture/select hover color change in this case line of code in poc "<input type="text" name="tel" id="name" autofocus="" autocomplete="tel" dir="rtl" onchange="alert(this.value);">" , and the poc video attached shows up full exploit.

## **VERSION**

Exploit tested with the following properties:

## Google Chrome:115.0.5790.3 (Official Build) dev (64-bit) Revision:32c8fb09897da1b8f8dde49364e9a589403ad9bf-refs/branch-heads/5790@{#10} OS:Linux

## Google Chrome:113.0.5672.126 (Official Build) (64-bit) Revision:c541687b21a73452ab403e2dced7033ddc97ee9d-refs/branch-heads/5672@{#1202} OS:Linux

# **REPRODUCTION CASE**

the exploit use a vulnerability in showing of cache of input fields. your browser suggests the saved entries of input fields like saved user logins (username, email, phone number...) or cached search word any similar entered things.

nobody will send critical information to unknown sites. but this can be hide by full bypassing the visibility of all fields and suggests. in this case nobody are able to notice that they are sending their data to unknown attackers.

# REPRODUCTION STEPS

(Play a little jump and run game (Dino) like in <https://crbug.com/chromium/1358647> to get hijacked any cached input of field name "username",email,telphone,address,cardnumber,.....), but here i have made the poc More simple(without game)

\*\*Before Repro you can add some data under chrome://settings/addresses and add some records

1-visit <https://vrphunt.com/chrome/viewport/show-me-out3.html>

2-Press Arrow Down/UP then Enter

Autofill data Will be shown in the alert Popup, it can be sent directly to attacker C&C server and this poc could be modified to ex-filtrate all user data by simply "after each ENTER key press event we can change autocomplete="tel" value to different ones like email,creditcard,username,....etc".

==================  

**CREDIT INFORMATION**

Reporter credit: Ahmed ElMasry

==================  

Thank you for your attention. with kind Regards

## Attachments

- [poc-01-2023-05-30_10-49-57.mp4](attachments/poc-01-2023-05-30_10-49-57.mp4) (video/mp4, 938.5 KB)
- [poc-02-2023-05-30_10-46-23.mp4](attachments/poc-02-2023-05-30_10-46-23.mp4) (video/mp4, 682.9 KB)
- [show-me-out3.html](attachments/show-me-out3.html) (text/plain, 3.1 KB)
- [V115.0.5790.3-dev-linux-2023-05-31_13-29-08.mp4](attachments/V115.0.5790.3-dev-linux-2023-05-31_13-29-08.mp4) (video/mp4, 1.1 MB)
- deleted (application/octet-stream, 0 B)
- [show-me-out3-dynamic.html](attachments/show-me-out3-dynamic.html) (text/plain, 4.0 KB)
- [Autofill-Stable-Win- 2023-06-02 19-28-51-136.mp4](attachments/Autofill-Stable-Win- 2023-06-02 19-28-51-136.mp4) (video/mp4, 4.2 MB)
- [Autofill-Canary-Win 2023-06-02 19-34-20-606.mp4](attachments/Autofill-Canary-Win 2023-06-02 19-34-20-606.mp4) (video/mp4, 2.8 MB)
- [canary5819-2023-06-08 14-42-18-347.mp4](attachments/canary5819-2023-06-08 14-42-18-347.mp4) (video/mp4, 1.6 MB)
- [canary-5818-2023-06-08 14-41-05-523.mp4](attachments/canary-5818-2023-06-08 14-41-05-523.mp4) (video/mp4, 1.3 MB)

## Timeline

### [Deleted User] (2023-05-30)

[Empty comment from Monorail migration]

### el...@gmail.com (2023-05-30)

Another note about fix/Mitigation:
at 
https://chromium-review.googlesource.com/c/chromium/src/+/2323392/15/chrome/browser/ui/views/autofill/autofill_popup_view_utils.cc#90 ,
````
bool HasEnoughHeightForOneRow(int item_height,
                              const gfx::Rect& content_area_bounds,
                              const gfx::Rect& element_bounds) {
  // Ensure that at least one row of the popup can be displayed within the
  // bounds of the content area so that the user notices the presence of the
  // popup.
  bool enough_space_for_one_item_in_content_area_above_element =
      element_bounds.y() - content_area_bounds.y() >= item_height;
  bool enough_space_for_one_item_in_content_area_below_element =
      content_area_bounds.bottom() - element_bounds.bottom() >= item_height;
  return enough_space_for_one_item_in_content_area_above_element ||
         enough_space_for_one_item_in_content_area_below_element;
}
`````
Fix:
------
we need to  mitigate this at least showing up 2 or three rows instead of only one row  which is not sufficient to the user to know what he dealing with , so when the check becomes two rows or three  we minus one row for mange so the result one/two rows of data will be shown and when the user using up/down arrow he will notice the change due to hover or key interaction on rows of data(in blue)

### el...@gmail.com (2023-05-30)

offline poc file attached, you can host on your web server if you want to test it in your environment. Online Poc url is sufficient ,this is simple poc to show how exploitation work.
thanks

### el...@gmail.com (2023-05-31)

today i have updated chrome to
-------------------
Google Chrome:115.0.5790.3 (Official Build) dev (64-bit) 
Revision:32c8fb09897da1b8f8dde49364e9a589403ad9bf-refs/branch-heads/5790@{#10}
OS:Linux
-------------------
i've noticed slight change in omnibox sizing so i've updated the poc to optimize the height of input field to have the poc working properly , the change is in style of class called ` #name`  change the height value from height:628px; to height:620px;  which make this working like the other versions i tested with  , also you can have a look at the poc-video for this.

also i've created a new poc for this online at  https://vrphunt.com/chrome/viewport/show-me-out3-opt.html


### ct...@chromium.org (2023-06-02)

Thanks for the report. I don't think I was able to get the attached proof-of-concept to repro (loading over localhost serving using `python3 -m http.server`). Could you upload your updated poc from https://crbug.com/chromium/1449874#c4?

### el...@gmail.com (2023-06-02)

Hello cthomp@
Thanks for your time reproducing and triaging this!

I've uploaded it and the main change as mentioned in https://crbug.com/chromium/1449874#c4 is:
in style of class called ` #name`  change the height value from height:628px; to height:620px;

##the main idea is to give some little space for one row ##
If you faced and problem in repro , could you tell me what problem you face exactly?!

## if the problem is the one row not shown this is because the space isn't enough due to different screen webview size change ,you can try changing the height value from height:620px; to height:618px;  for example.

## i've made the poc more simple by static value of height of input field , but if you need i'll work on it to get the viewport size to  make the poc generic for all devices/screens.

Thanks 

### [Deleted User] (2023-06-02)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@gmail.com (2023-06-02)

Hello cthomp@

I've optimized the poc to Automatically Adapt viewportscreen sizes Automatically to be more Generic , and this can also cover any changes in the user view preferences/configuration like(showing bookmarks bar, or showing consoleDev panel,entering fullscreen,...etc) and change height accrordingly.

**Important thing before Repro as mentioned before in Reproduction Steps**

-------------------------------------------------------------------------------------------------------------------------------------
|**Before Repro you can add some data under chrome://settings/addresses and add some records**|
-------------------------------------------------------------------------------------------------------------------------------------

1-visit https://vrphunt.com/chrome/viewport/show-me-out3-dynamic.html

2-Press Arrow Down/UP then Enter , popup will be shown with autofill data.

**You can have a look for Repro POC for any help**

=========
I've Tested the Attached POC/Online Version  with the following properties
----------------
Versions:
----------------
Google Chrome:116.0.5807.0 (Official Build) canary (64-bit) (cohort: Clang-64) 
Revision:928383560316ada4bec60044e4cddbdf55b8cc5e-refs/branch-heads/5807@{#1}
Version:116.0.5807.0
Milestone:116
Branch:5807
Branch Base Position:1152177
OS:Windows 11 Version 22H2 (Build 22621.1702)
-----------------------
Google Chrome:114.0.5735.91 (Official Build) (64-bit) (cohort: Stable Installs & Version Pins) 
Revision:386bc09e8f4f2e025eddae123f36f6263096ae49-refs/branch-heads/5735@{#1052}
Channel: Stable-Extended
Version:114.0.5735.91
Milestone:114
Branch:5735
Branch Base Position:1135570
OS:Windows 11 Version 22H2 (Build 22621.1702)
------------------------
Google Chrome:116.0.5803.2 (Official Build) dev (64-bit) (cohort: Dev) 
Revision:d4a30b184e5a72542dbfc7fda5be619d6921bc0a-refs/branch-heads/5803@{#4}
Channel:Dev
Version:116.0.5803.2
Milestone:116
Branch:5803
Branch Base Position:1150927
OS:Windows 11 Version 22H2 (Build 22621.1702)
----------------------------
Google Chrome:115.0.5790.13 (Official Build) beta (64-bit) (cohort: Beta) 
Revision:5f740d00e862007bdf092401a21f54a6e735c3f3-refs/branch-heads/5790@{#158}
Channel:Beta
Milestone:115
Branch:5790
Branch Base Position:1148114
OS:Windows 11 Version 22H2 (Build 22621.1702)
-----------------------------------------

Thanks for your time and patience, Hope this helps you.

### aj...@google.com (2023-06-06)

-> mamir & some autofill folks following https://crbug.com/chromium/1108181

[Monorail components: UI>Browser>Autofill]

### [Deleted User] (2023-06-06)

[Empty comment from Monorail migration]

### ba...@chromium.org (2023-06-06)

Mohamed, did https://chromium-review.googlesource.com/c/chromium/src/+/4584748 fix this?

### ma...@chromium.org (2023-06-07)

Yes, AFAICT, this should be fixed by https://crrev.com/c/4584748 which landed 116.0.5815.0 already.

I am tempted to mark this as duplicate of https://crbug.com/1450610, but this has been filed first.
So I am not sure which should be a duplicate of the other!

### el...@gmail.com (2023-06-07)

Thanks Mohamed mamir@
https://crbug.com/chromium/1450610  was filled after my report , and according to chromium bug bounty rule  the reward goes to first report am i right?

Thanks for your Fix , hope you consider my reply for reward decision at VRP panel and CVE assignment,and Credit.

Thanks 


### [Deleted User] (2023-06-07)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@google.com (2023-06-07)

[Empty comment from Monorail migration]

### aj...@google.com (2023-06-07)

Fixed by https://bugs.chromium.org/p/chromium/issues/detail?id=1450610#c11

### el...@gmail.com (2023-06-08)

Hello there..,Important Update for this , After digging more around the fix at  https://bugs.chromium.org/p/chromium/issues/detail?id=1449874#c12 which  landed 116.0.5815.0 as stated in https://crbug.com/chromium/1449874#c12 , The Bug still Not Fixed Please Reopen this again and re-check  . mamir@ schwering@  ajgo@

**I've Attached POC Video Shows the Bug **

Reproduction Steps:

-------------------------------------------------------------------------------------------------------------------------------------
|**Before Repro you can add some data under chrome://settings/addresses and add some records**|
-------------------------------------------------------------------------------------------------------------------------------------

1-visit https://vrphunt.com/chrome/viewport/show-me-out3-dynamic-vert.html  "which is same as in https://crbug.com/chromium/1449874#c8 "  https://vrphunt.com/chrome/viewport/show-me-out3-dynamic.html

2-Press Arrow Down/UP then Enter , popup will be shown with autofill data.

==========================================================
The Bug Tested Again with two Newer versions after the fix version ,using following properties:
=============
Google Chrome: 116.0.5819.0 (Official Build) canary (64-bit) (cohort: Clang-64) 
Revision: 659667dd7cdfea820709ecc2bc91c82e88c80a6d-refs/branch-heads/5819@{#1}
Channel: Canary
Milestone:116
Branch:5819
Branch Base Position:1154567
OS: Windows 10 Version 22H2 (Build 19045.2965)
------------------------
Google Chrome:116.0.5818.0 (Official Build) cangry (64-bit) (cohort:Clang-64)
Revision: 0cc6d2d344a8551f73d28dd537e3bb757348aec2-refs/branch-heads/5818@(#1}
Channel:Canary
Milestone:116
Branch:5818
Branch Base Position:1154341
OS: Windows 10 Version 22H2 (Build 19045.2965)
---------------------
Thanks 

### am...@chromium.org (2023-06-08)

Hi mamir@, this issue seems to still be able to be reproduced. Can you PTAL? 

Hi Ahmed, thanks for brining this to our attention. Since this is a low severity issue, so it may not get immediate attention. 

### sc...@google.com (2023-06-15)

Thanks for the update, Ahmed.
Mohamed is out at the moment, I'll take a look.

### el...@gmail.com (2023-06-15)

Thanks Christoph for your attention and working on this!, 
Have a great day.

### sc...@google.com (2023-06-15)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-06-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2f9a40ef6bb45e10c24020cb07a78df5003ec0e9

commit 2f9a40ef6bb45e10c24020cb07a78df5003ec0e9
Author: Dmitry Vykochko <vykochko@google.com>
Date: Mon Jun 26 07:52:59 2023

Fix the autofill popup sufficient space check.

The footer height was not taken into account. Fixed by adding
its full height into the min_height restrictions, as it is not
scrollable.

Bug: 1449874
Change-Id: I69954550d2e7b2e516c6de89830c3d28133b6501
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4624570
Reviewed-by: Vasilii Sukhanov <vasilii@chromium.org>
Commit-Queue: Dmitry Vykochko <vykochko@google.com>
Reviewed-by: Christoph Schwering <schwering@google.com>
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1162273}

[modify] https://crrev.com/2f9a40ef6bb45e10c24020cb07a78df5003ec0e9/chrome/browser/autofill/mock_autofill_popup_controller.h
[modify] https://crrev.com/2f9a40ef6bb45e10c24020cb07a78df5003ec0e9/chrome/browser/ui/views/autofill/popup/popup_view_views.cc
[modify] https://crrev.com/2f9a40ef6bb45e10c24020cb07a78df5003ec0e9/chrome/browser/ui/views/autofill/popup/popup_view_views_unittest.cc
[modify] https://crrev.com/2f9a40ef6bb45e10c24020cb07a78df5003ec0e9/chrome/browser/ui/views/autofill/popup/popup_view_utils.cc
[modify] https://crrev.com/2f9a40ef6bb45e10c24020cb07a78df5003ec0e9/chrome/browser/ui/views/autofill/popup/popup_view_views.h


### el...@gmail.com (2023-06-26)

Hello Dmitry vykochko@ , Christoph schwering@ ..,

Thanks for Getting attention and working on this..!
----------------------

- From My Side I can Confirm that this Bug is Fixed by the two commits Below [1] , [2] 
1- https://chromium-review.googlesource.com/c/chromium/src/+/4584748 
2- https://chromium-review.googlesource.com/c/chromium/src/+/4624570

which Cover the fix well , because the check for dismissing the autofill popup becomes checking (one row) Plus (Footer Row (Manage...)) , making this noticeable to user , as mentioned in suggested fix at https://crbug.com/chromium/1449874#c2.

- I've tested the fix at Chrome  with the following properties:
Google Chrome:117.0.5854.0 (Official Build) canary (64-bit) (cohort: Clang-64) 
Revision:00258882885385bb4f8a885925f21c6a363393c1-refs/branch-heads/5854@{#2}
OS:Windows 11 Version 22H2 (Build 22621.1848)

- Feel Free to Mark this as [Fixed /Verified].

- As per https://crbug.com/chromium/1449874#c12 feel free to mark Issue1450610 as duplicate of this one , as this has been filed first , Also Please  issue CVE here when the fix landed.

- For VRP Assessment, Please Consider All Info Provided  in  https://crbug.com/chromium/1449874#c0 ,  https://crbug.com/chromium/1449874#c2, https://crbug.com/chromium/1449874#c3, https://crbug.com/chromium/1449874#c4, https://crbug.com/chromium/1449874#c6, https://crbug.com/chromium/1449874#c8  , and follow-up info at https://crbug.com/chromium/1449874#c17 .

Thanks for All your efforts working and fixing this one

### el...@gmail.com (2023-07-19)

Hello there ..,

Dmitry vykochko@ ,Is there any further work to do here ?!, If there's no more work , please mark this as fixed and verified as per https://crbug.com/chromium/1449874#c23

Thanks 

### vy...@google.com (2023-07-23)

Hi, right, the work is done now, thanks again for the report!

### [Deleted User] (2023-07-23)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-23)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-10)

Congratulations, Ahmed! The VRP Panel has decided to award you $5,000 for this report + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us! 

### el...@gmail.com (2023-08-11)

Thanks Amy for the reward and Bonus.

### am...@google.com (2023-08-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-09-09)

[Empty comment from Monorail migration]

### pg...@google.com (2023-09-12)

[Empty comment from Monorail migration]

### pg...@google.com (2023-09-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-10-29)

This issue was migrated from crbug.com/chromium/1449874?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1450610]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065003)*
