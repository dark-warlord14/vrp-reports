# Security: Bypass the Protection of input fields cache (Autofill) due to inappropriate code design (Bypass 1472404),Similar to(1449874)

| Field | Value |
|-------|-------|
| **Issue ID** | [40071255](https://issues.chromium.org/issues/40071255) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P3 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | el...@gmail.com |
| **Assignee** | jk...@google.com |
| **Created** | 2023-09-03 |
| **Bounty** | $2,000.00 |

## Description

# **VULNERABILITY DETAILS**

this is a report to a security vulnerability in google chrome/chromium browser as high-quality report with functional exploit. this vulnerability (Straight forward Bypass of <https://crbug.com/chromium/1472404)which> is similar to <https://crbug.com/chromium/1449874> I've reported before which allows attackers to steal the cache of input fields like usernames, e-mail addresses, telephone numbers from any site like twitter, google and any others (Chrome Autofill Saved Data).

-Please Add Same Folks of 1472404 /1449874 , and assign this to [jkeitel@google.com](mailto:jkeitel@google.com) for better tracking, as Jan Fixed the Main One 9 days ago and works on this area nowadays.

# Root Cause Analysis and Bug Exist History & Bisection:

Main Bug Fixed By the following two commits and this Bug found due to miss-checking in these commits:  

[1]- <https://chromium-review.googlesource.com/c/chromium/src/+/4798089>  

[2]- <https://chromium-review.googlesource.com/c/chromium/src/+/4793752>

and fix shipped to chrome with the following properties:

# Google Chrome: 118.0.5966.0 (Official Build) canary (64-bit) (cohort: Clang-64) Channel:Canary Version:118.0.5966.0 Milestone: 118 Branch: 5966 Branch Base Position: 1187151 OS: Windows 10 Version 22H2 (Build 19045.3208)

# Google Chrome: 118.0.5967.0 (Official Build) canary (64-bit) (cohort: Clang-64) Channel: Canary Version: 118.0.5967.0 Milestone:118 Branch: 5967 Branch Base Position: 1187488 Revision: c2868899a533a22f76c91b9332cffd958014f2b0-refs/branch-heads/5967@{#1} OS: Windows 10 Version 22H2 (Build 19045.3208)

## Analysis part:

<https://crbug.com/chromium/1472404> Fixed By

<https://chromium-review.googlesource.com/c/chromium/src/+/4798089>

which introduce:

Add a dimension parameter to CreateDisallowCustomCursorScope.

## This CL extends CursorManager::CreateDisallowCustomCursorScope by adding a dimension parameter that allows controlling the maximum size of custom cursors.

and also <https://chromium-review.googlesource.com/c/chromium/src/+/4793752>  

which introduce:  

Disable large custom cursors while Autofill/PWM popup is showing.

## This CL disallows custom cursors for which max(height, width) > 24 px to avoid that they overlap with the Autofill and PW generation popups too much to obscure significant parts of it.

from commit 1 and 2 the fix guarantee that the autofill will not be shown if Custom cursor is present , if custom cursor is present from the current focused web-content and autofill manger observer observes that , it immediately prevent the autofill popup to be shown.

but how it could be bypassed.?  

**-------------------------** -----  

Actually after looking to code i got an idea to trick the autofill manger observer ,what about showing the custom cursor from parent window not from the popup window? point (1)  

what about showing autofill popup from the popup window point(2), and bind the mouse cursor on bottom-border of popup window .  

merge all together ,and the trick works and with a perfect UI Overlay and add funtion to bind the popup window to mouse cursor overlay and also function to position the overlay precisely, Autofill popup can be fully hidden and user can interact without notice.

---

Attacker can get Autofill data from Victim using 150px\*150px instruction popup window , and Autofill popup can be made totally hidden behind Cursor as shown in the poc video attached.

from here we can have a complete exploit to make the user interact and send autofill data without seeing the data he/she select "or make the user will not notice the presence of the popup"  

as when user clicks the cookie icon Custom-Css Cursor layout appears with instructions on it (ArrowDown,Enter), when the user press arrow down the selection going underneath but nothing shown to the user because the Autofill is totally hidden behind the css curor in this case.

# Explained Good Points Help in Fix/Mitigation:

Suggested fix:

- we need to get the web-content area and check the intersection between it and cursor size , if this is greater than 24px don't show autofill popup , and if it was shown dismiss it immediately.  
  
  ++ another check we can check the intersected area in px between Autofill popup area and Cursor area if it exceeds 24 px hide autofill-popup / reset cursor to be 24px.  
  
  ++This Fix will guarantee that there is no presence for Autofill popup while Custom Cursor is present and intersection is larger than 24px as introduced in <https://chromium-review.googlesource.com/c/chromium/src/+/4793752> , making user more secure.

## ===================== **VERSION**

## Exploit tested with the following properties:

Google Chrome: 118.0.5979.0 (Official Build) dev (64-bit)  

Channel: Dev  

Version: 118.0.5979.0  

Milestone: 118  

Branch: 5979  

Branch Base Position: 1189757  

Revision: db97447ae7a784e100c07ed675b2bd57b518e689-refs/branch-heads/5979@{#1}  

OS: Linux

---

## Google Chrome: 118.0.5966.0 (Official Build) canary (64-bit) (cohort: Clang-64) Channel:Canary Version:118.0.5966.0 Milestone: 118 Branch: 5966 Branch Base Position: 1187151 OS: Windows 10 Version 22H2 (Build 19045.3208)

# Google Chrome: 118.0.5967.0 (Official Build) canary (64-bit) (cohort: Clang-64) Channel: Canary Version: 118.0.5967.0 Milestone:118 Branch: 5967 Branch Base Position: 1187488 Revision: c2868899a533a22f76c91b9332cffd958014f2b0-refs/branch-heads/5967@{#1} OS: Windows 10 Version 22H2 (Build 19045.3208)

++The Bug Exists since <https://crbug.com/chromium/1472404> was born because of the two commits mentioned above (Fix of 1472404).  

++Feel free to add Found-In :118  

++ Tests only done With New Versions since the main bug was fixed 9 days only.

# **REPRODUCTION CASE**

the exploit use a vulnerability in showing of cache of input fields. your browser suggests the saved entries of input fields like saved user logins (username, email, phone number...) or cached search word any similar entered things.

nobody will send critical information to unknown sites. but this can be hide by full bypassing the visibility of all fields and suggests. in this case nobody are able to notice that they are sending their data to unknown attackers.

# REPRODUCTION STEPS

(Play a little jump and run game (Dino) like in <https://crbug.com/chromium/1472404> and <https://crbug.com/chromium/1358647> to get hijacked any cached input of field name "username",email,telphone,address,cardnumber,.....), but here i have made the PoC More simple(without game)

P.S : This Bug Can be also exploited using chrome Extension as main issue also discussed that , But if any information needed let me know.

\*\*Before Repro you can add some data under chrome://settings/addresses and add some records

1- Visit <https://vrphunt.com/chrome/1PxScreen/bypass1472404/bypass1472404-poc.html>

2- Click "Open Game Config Popup Instructions" popup will be shown , you will see keyboard conf instructions overlay shown and centerd on the popup.

> > if the overlay isn't centered just move to right or left to trigger the code "refine of event may be needed"

3- Press Arrow Down/UP then Enter

4- open developper console for the popup window as i used Console.log to log the autofill data .

You can Take a look to the poc video for Reproduction.

+Feel free to Use online version of "bypass1472404-poc.html".

++Please Assign this one to Jan as well , so he can keep an eye on the variations that may arise from it and ensure better mitigation, Thanks.

# +++Any further Info needed I'am here and happy to assist.

**CREDIT INFORMATION**

Reporter credit: Ahmed ElMasry

==================  

Thank you for your attention. with kind Regards

## Attachments

- [bypass1472404-poc.html](attachments/bypass1472404-poc.html) (text/plain, 5.7 KB)
- [cursor-128x128-auto.png](attachments/cursor-128x128-auto.png) (image/png, 2.8 KB)
- [bypass1472404-poc-DEV-LINUX-V118-2023-09-03_17-10-00.mp4](attachments/bypass1472404-poc-DEV-LINUX-V118-2023-09-03_17-10-00.mp4) (video/mp4, 1.6 MB)
- [Linux-dev-Official-v118-2023-09-13_10-11-38.mp4](attachments/Linux-dev-Official-v118-2023-09-13_10-11-38.mp4) (video/mp4, 1.1 MB)
- [bandicam 2023-09-22 23-45-32-386.mp4](attachments/bandicam 2023-09-22 23-45-32-386.mp4) (video/mp4, 2.4 MB)
- [Win-Canary-withShowMove-2023-09-22 23-53-49-720.mp4](attachments/Win-Canary-withShowMove-2023-09-22 23-53-49-720.mp4) (video/mp4, 2.3 MB)
- [Full-Autofill-Game-Poc2023-10-09 23-45-14-398.mp4](attachments/Full-Autofill-Game-Poc2023-10-09 23-45-14-398.mp4) (video/mp4, 1.1 MB)
- [Full-Game-Autofill-Exploit 2023-10-09 23-46-52-946.mp4](attachments/Full-Game-Autofill-Exploit 2023-10-09 23-46-52-946.mp4) (video/mp4, 2.0 MB)

## Timeline

### [Deleted User] (2023-09-03)

[Empty comment from Monorail migration]

### ke...@chromium.org (2023-09-07)

Thanks for the report. This is clever.

jkeitel@: Do you want to handle this one as well?

The trick here is that the parent window sets the custom cursor, while the popup does the autofill shenanigans.

[Monorail components: UI>Browser>Autofill]

### [Deleted User] (2023-09-07)

[Empty comment from Monorail migration]

### jk...@google.com (2023-09-08)

Thank you for the report!

I just took a look at it and I can't properly reproduce it (neither on Mac nor on Linux test machines) because the popup positioning is off. On Mac the popup always ends up in a corner and on Windows it follows the cursor so aggressively that the cursor overlaps the popup window and no custom cursor is shown.

However, I think I understand what the idea behind the exploit is.

Ken, it looks to me like we should disallow custom cursors (% size restrictions) for all tabs/windows. However, it's not obvious to me what the right level of abstraction for that would be. I shared some thoughts in a doc with you - I think it might take a bit of discussion.

### el...@gmail.com (2023-09-13)

Hello ..,
 kenrb@ Thanks for your kind words and triage Ken..!

I'd Like to mention that the Poc Works Very Well on Linux as Demonstrated in the poc attached and also tested  it with Version 118.0.5993.3 (Official Build) dev (64-bit)  , and in Windows Platform Also works well, But i don't have Mac Machine to test it on Chrome in Mac , also i'd like to add note about ```so aggressively that the cursor overlaps the popup window and no custom cursor is shown``` , this is very easy to avoid  just by giving  some space between the cursor and the popup window so that when moving the cursor the popup will be always far from the cursor son the overlap with popup Web-content will not happen and presistant cursor overlay still remains , the popup followup  the cursor works good in slow mouse move from outside toward inside the popup web-content  but what you faced aggressively that the cursor is very near to the edge to  the popup and  fast mouse move towards inside of popup web-content so the Javascript calculation and positioning can't handle it very efficiently  so the solution for this is to give the cursor much more space under the popup windows with some refine of ``const yOffset value at poc code``  and re-customize the overlay to be fully consistent with autofill popup  style  to be fully hidden.

The Idea of exploit chain is straightforward, as previously mentioned, and it appears that you grasp it well. However,Creating a POC within a tight timeframe and submitting a fully detailed report before others catch onto the idea can indeed be quite challenging. Furthermore, it may not encompass all the nuances and issues that may arise during the actual implementation or potential issues of the user experience."

 jkeitel@  Thanks Jan for your prompt response and taking a closer look to this one and getting the idea behind the exploit..!

Thanks Again Jan  for your attention and working on this one.!

 

### el...@gmail.com (2023-09-22)

Hello Jan jkeitel@

This is a Poc for Windows 

https://vrphunt.com/chrome/1PxScreen/bypass1472404/bypass1472404-poc-win-00.html
Same Repro steps 
open the link 
and press Cog icon to set Game controls (open popup window)  then Arrow-down , Enter

Check the De console log 
Repro Video for this poc (Windows) Attached


Thanks for your attention , working on this in advance..!




### jk...@google.com (2023-09-25)

Thanks!

I think we're aligned on a solution that I have tested locally - hoping to merge the code in a couple of days. Once it's landed, I'll ask you to verify that it's working as expected.

### el...@gmail.com (2023-09-25)

Thanks Jan for your efforts solving this one , sure i'am happy to assist and verify the fix once landed .


### jk...@google.com (2023-09-29)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-10-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a0bcfb563692002bb5aff732c81fb042749f4104

commit a0bcfb563692002bb5aff732c81fb042749f4104
Author: Jan Keitel <jkeitel@google.com>
Date: Fri Oct 06 06:54:01 2023

Add support for suppressing custom cursors across all browser windows.

Custom cursors (in particular large custom images) set via CSS by a
web page can obscure elements in other browser windows if the
browser windows are positioned on top of each other. In those cases,
calling WebContents::CreateDisallowCustomCursorScope for the currently
focused WebContents is not sufficient to block custom cursors.

This CL adds a helper class to disallow custom cursor across all active
WebContents of all browser windows. Its current only use case is
Autofill popups, which is why the helper class is placed there. Should
it turn out to be needed elsewhere, it can still be moved.

One-pager (design discussions there, please):
go/disallow-custom-cursors-across-windows

Bug: 1478613
Change-Id: Iab45831799e037d626bf3ecc9f5f51fc7cf2656a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4874027
Reviewed-by: Ken Buchanan <kenrb@chromium.org>
Reviewed-by: Dana Fried <dfried@chromium.org>
Commit-Queue: Jan Keitel <jkeitel@google.com>
Cr-Commit-Position: refs/heads/main@{#1206256}

[add] https://crrev.com/a0bcfb563692002bb5aff732c81fb042749f4104/chrome/browser/ui/views/autofill/popup/custom_cursor_suppressor.cc
[modify] https://crrev.com/a0bcfb563692002bb5aff732c81fb042749f4104/chrome/test/BUILD.gn
[add] https://crrev.com/a0bcfb563692002bb5aff732c81fb042749f4104/chrome/browser/ui/views/autofill/popup/custom_cursor_suppressor_unittest.cc
[modify] https://crrev.com/a0bcfb563692002bb5aff732c81fb042749f4104/chrome/browser/ui/BUILD.gn
[add] https://crrev.com/a0bcfb563692002bb5aff732c81fb042749f4104/chrome/browser/ui/views/autofill/popup/custom_cursor_suppressor.h


### gi...@appspot.gserviceaccount.com (2023-10-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b3471ed2d043466d4fbaf7e11d7edde81d5c4d02

commit b3471ed2d043466d4fbaf7e11d7edde81d5c4d02
Author: Jan Keitel <jkeitel@google.com>
Date: Fri Oct 06 07:50:48 2023

Add support for suppressing custom cursors across navigations.

This CL adds observations of the WebContents that have been active
while custom cursor suppression is on. If the RenderFrameHost of the
primary main frame changes, the new RenderFrameHost will also have
custom cursors suppressed.

Bug: 1478613
Change-Id: I2ebe50d8caaf2f52c3ba7c957391595d34d9ac50
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4898211
Reviewed-by: Ken Buchanan <kenrb@chromium.org>
Commit-Queue: Jan Keitel <jkeitel@google.com>
Cr-Commit-Position: refs/heads/main@{#1206271}

[modify] https://crrev.com/b3471ed2d043466d4fbaf7e11d7edde81d5c4d02/chrome/browser/ui/views/autofill/popup/custom_cursor_suppressor.cc
[modify] https://crrev.com/b3471ed2d043466d4fbaf7e11d7edde81d5c4d02/chrome/browser/ui/views/autofill/popup/custom_cursor_suppressor_unittest.cc
[modify] https://crrev.com/b3471ed2d043466d4fbaf7e11d7edde81d5c4d02/chrome/browser/ui/views/autofill/popup/custom_cursor_suppressor.h


### gi...@appspot.gserviceaccount.com (2023-10-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/368421cadfffaf3bbcdd7da2640018dc8c52f2f2

commit 368421cadfffaf3bbcdd7da2640018dc8c52f2f2
Author: Jan Keitel <jkeitel@google.com>
Date: Fri Oct 06 09:20:35 2023

Use multi-window custom cursor suppression in Autofill popup.

Bug: 1478613
Change-Id: I3014096a98b571d2d9f7e08b2d7a7ca9bae01476
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4891730
Reviewed-by: Christoph Schwering <schwering@google.com>
Reviewed-by: Bruno Braga <brunobraga@google.com>
Commit-Queue: Jan Keitel <jkeitel@google.com>
Cr-Commit-Position: refs/heads/main@{#1206303}

[modify] https://crrev.com/368421cadfffaf3bbcdd7da2640018dc8c52f2f2/components/autofill/core/common/autofill_features.cc
[modify] https://crrev.com/368421cadfffaf3bbcdd7da2640018dc8c52f2f2/chrome/browser/ui/views/autofill/popup/popup_base_view.cc
[modify] https://crrev.com/368421cadfffaf3bbcdd7da2640018dc8c52f2f2/chrome/browser/ui/views/autofill/popup/popup_base_view.h
[modify] https://crrev.com/368421cadfffaf3bbcdd7da2640018dc8c52f2f2/components/autofill/core/common/autofill_features.h


### el...@gmail.com (2023-10-07)

Hello Jan jkeitel@ ..,

Thanks for your Efforts working and producing tight fix for this one.!

-From My Side I can Confirm that this Bug is Fixed well by the following Three Commits:

[1]- https://chromium-review.googlesource.com/c/chromium/src/+/4874027
[2]- https://chromium-review.googlesource.com/c/chromium/src/+/4898211
[3]-https://chromium-review.googlesource.com/c/chromium/src/+/4891730

and Now Autofill popup can't Be shown while Custom Cursor is present even the custom cursor was triggered from main page or another popup , This Fix make the total fix for this issue is Now Complete as you implemented the check while navigation which i was thinking about this, now Observer support suppressing custom cursors across navigations (very interesting).

- I've tested / played around the fix at  Latest Chrome Canary Build  with the following properties:
====================
Google Chrome: 120.0.6052.0 (Official Build) canary (64-bit) (cohort: Clang-64) 
Revision: 59b6199190394a6c2dd3155c58289b1fc2e37d28-refs/branch-heads/6052@{#1}
Milestone: 120
Branch: 6052
Branch Base Position: 1206727
OS: Windows 11 Version 22H2 (Build 22621.2361)
------------
Google Chrome: 120.0.6053.0 (Official Build) canary (64-bit) (cohort: Clang-64) 
Revision: fd07450c1386fe3f208e4398692cb232261ff477-refs/branch-heads/6053@{#1}
Milestone: 120
Branch: 6053
Branch Base Position: 1206788
OS: Windows 11 Version 22H2 (Build 22621.2361)
-------------

-Feel Free to Mark this as [Fixed /Verified] .

Again ,Thanks for All your Great efforts working and fixing this one , Have a Great Day.

### jk...@google.com (2023-10-08)

Thank you for the swift verification!

### [Deleted User] (2023-10-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-08)

[Empty comment from Monorail migration]

### el...@gmail.com (2023-10-09)

Hello..,

Additional Info:
--------------------
I've made new Poc with Dino Game with precise Positioning JavaScript Code , this poc can show you how the Attack Really Happen in Real Life Scenario as https://crbug.com/chromium/1108181 and Issue1449874 .

Full Poc with Game :"https://vrphunt.com/chrome/1PxScreen/bypass1472404/bypass1472404-poc-win-game-full.html"

Case Reproduction:
----------------------------
**Before Repro you can add some data under chrome://settings/addresses and add some records

1- Visit https://vrphunt.com/chrome/1PxScreen/bypass1472404/bypass1472404-poc-win-game-full.html

2- Click "Cog Icon"  Controls Instructions popup will be shown.

3- Press Arrow Down then Enter 

To see Autofill data that will be Sent to attacker website Just "open developer console for the popup window as i used Console.log to log the autofill data ."

**Repro Videos for full Poc On Beta attached **
--------------------------------

- For VRP Assessment, Please Consider All Info Provided  in  https://crbug.com/chromium/1478613#c0 ,  https://crbug.com/chromium/1478613#c5, https://crbug.com/chromium/1478613#c17, and follow-up info at https://crbug.com/chromium/1478613#c13.

Thank you 



### am...@google.com (2023-10-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-10-11)

Congratulations Ahmed! The Chrome VRP Panel has decided to award you $2,000 for this report. The reward amount was decided upon based on the interaction preconditions and less likely path to be able to trick a user in engaging this way even with a "convincing" game given both the cursor hold / positioning preconditions and the keyboard selection requirements. To help reduce the reporting time on your part in the future, when an issue is specifically a bypass of another not fully resolved issue, multiple recreations across versions is not necessary. Thank you for your efforts and reporting this issue to us! 

### el...@gmail.com (2023-10-12)

Thanks Amy.!

### am...@google.com (2023-10-13)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-12-04)

[Empty comment from Monorail migration]

### pg...@google.com (2023-12-06)

[Empty comment from Monorail migration]

### pg...@google.com (2023-12-06)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2024-01-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4bd47e3c8209186ae89d6145b88cbba472a999d5

commit 4bd47e3c8209186ae89d6145b88cbba472a999d5
Author: Jan Keitel <jkeitel@google.com>
Date: Mon Jan 22 13:08:46 2024

Clean up kAutofillPopupMultiWindowCursorSuppression feature.

The feature was default-enabled on M120 and can be cleaned up. It only
served as a kill-switch in the first place.

Bug: 1478613
Change-Id: I2eff5cb232ed99d135169d2daf493e5474f0dd49
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5222563
Auto-Submit: Jan Keitel <jkeitel@google.com>
Reviewed-by: Bruno Braga <brunobraga@google.com>
Commit-Queue: Bruno Braga <brunobraga@google.com>
Cr-Commit-Position: refs/heads/main@{#1250130}

[modify] https://crrev.com/4bd47e3c8209186ae89d6145b88cbba472a999d5/components/autofill/core/common/autofill_features.cc
[modify] https://crrev.com/4bd47e3c8209186ae89d6145b88cbba472a999d5/chrome/browser/ui/views/autofill/popup/popup_base_view.cc
[modify] https://crrev.com/4bd47e3c8209186ae89d6145b88cbba472a999d5/chrome/browser/ui/views/autofill/popup/popup_base_view.h
[modify] https://crrev.com/4bd47e3c8209186ae89d6145b88cbba472a999d5/components/autofill/core/common/autofill_features.h


### is...@google.com (2024-01-22)

This issue was migrated from crbug.com/chromium/1478613?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40071255)*
