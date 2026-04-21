# Security: Bypass and Semi Regression of Issue 1472404 fix  which Bypass the Protection of input fields cache (Autofill) 

| Field | Value |
|-------|-------|
| **Issue ID** | [40075980](https://issues.chromium.org/issues/40075980) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P3 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | el...@gmail.com |
| **Assignee** | jk...@google.com |
| **Created** | 2023-10-31 |
| **Bounty** | $2,000.00 |

## Description

# **VULNERABILITY DETAILS**

this is a report to a security vulnerability in google chrome/chromium browser as high-quality report with functional exploit.

`This Bug has a Bypass for the Mitigation done at Main https://crbug.com/chromium/1472404`

this vulnerability impact similar to (<https://crbug.com/chromium/1108181),(https://crbug.com/chromium/1358647>) and (<https://crbug.com/chromium/1449874>) which allows attackers to steal the cache of input fields like usernames, e-mail addresses, telephone numbers from any site like twitter, google and any others (Chrome Autofill Saved Data).

-Please Add Same Folks of <https://crbug.com/chromium/1472404> , please add Jan [jkeitel@google.com](mailto:jkeitel@google.com) as owner to Complete the Fix and for Better tracking.Thx

# Root Cause Analysis and Bug Exist History:

## History:

Main Bug <https://crbug.com/chromium/1472404> Fixed at Aug 22, 2023 and Tested with Google Chrome: 118.0.5967.0 (Official Build) canary (64-bit) (cohort: Clang-64), Now there is a regression in Chrome V120 .

## Bisection:

Actually this bug found because of the two Commits(<https://crbug.com/chromium/1472404>) at

[1]- <https://chromium-review.googlesource.com/c/chromium/src/+/4798089>  

[2]- <https://chromium-review.googlesource.com/c/chromium/src/+/4793752>

## Bug Analysis:

## Bypass Analysis: **-------------------------** This Bug has a Bypass for the Mitigation done at Main <https://crbug.com/chromium/1472404> especially Commit[2] ,as while researching in chrome extensions APIs i Found 'chrome.side Panel' at <https://developer.chrome.com/docs/extensions/reference/sidePanel/> , and found one of it's features: -`The side panel remains open when navigating between tabs (if set to do so).` which we can benefit to make a very convincing Game extension , and with Side Panel Api, i've found that Autofill have some strange Behaviors and gave it a try and made the side panel extension page called `sidepanel-tab.html` embedded an Iframe of online web page which has a focused input field and Custom Cursor like main issue, and found a surprise , Side panel Broke the Mitigation at Commit[2], and Custom Cursor can Be shown and Cover the Autofill popup "this is the idea behind the exploitation".

## While Testing the Main Bug POC at <https://vrphunt.com/chrome/1PxScreen/online-poc-win.html> the Bug is Fixed and Mitigation Works well so i made this Part as a Bypass with Side panel Api behavior with Autofill Popup.

Semi-Regression Analysis:  

**-------------------------** -  

at commit [2] which introduce `Disable large custom cursors while Autofill/PWM popup is showing.` , this should fix the problem but doesn't take effect due to Side panel Behavior mentioned Above.

Semi Regression because the commit[2] is not working with Side panel Api .

**-------------------------** --

from here we can have a complete exploit to make the user interact and send autofill data without seeing the data he/she select "or make the user will not notice the presence of the popup"

as when user clicks the cookie icon Custom-Css Cursor layout appears with instructions on it (ArrowDown,Enter), when the user press arrow down the selection going underneath but nothing shown to the user because the Autofill is totally hidden behind the css cursor in this case.

## ===================== **VERSION**

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

## Google Chrome Version: 120.0.6051.2 Channel: Dev Milestone: 120 Branch:6051 Branch Base Position: 1206341 Google Chrome: 120.0.6051.2 (Official Build) dev (64-bit) 0 Revision: 75e545cf7ce76506ad3d2a5736ef28053af4a7f7-refs/branch- heads/6051@{#4} OS: Linux

# **REPRODUCTION CASE**

the exploit use a vulnerability in showing of cache of input fields. your browser suggests the saved entries of input fields like saved user logins (username, email, phone number...) or cached search word any similar entered things.

nobody will send critical information to unknown sites. but this can be hide by full bypassing the visibility of all fields and suggests. in this case nobody are able to notice that they are sending their data to unknown attackers.

# REPRODUCTION STEPS

(Play a little Battle game like in <https://crbug.com/chromium/1358647> to get hijacked any cached input of field name "username",email,telphone,address,cardnumber,.....), I've made the extension to show game window and use side panel to always show the game instruction beside playing game as this is one of the good features of side panel.

\*\*Before Repro you can add some data under chrome://settings/addresses and add some records

1- Load the simple Extension , enable developer mode and load extension

2-New Window of Game Instructions will be shown ,click button to open side panel , Click the cookie as instructed , you will see rest of instruction overlay shown.

3- Press Arrow Down/UP then Enter

## Autofill data Will be shown in Alert Popup, it can be sent directly to attacker C&C server.

PTAL for Poc Videos for Easy Repro and to show You the Full Impact.

- Extension Files attached and the Online POC File is also attached.
- Online File embedded at the Iframe at side panel named 'autofillpop-cursor-win-ref.html' attached below.
- Just use extension and Online File is working well.
- if you want to repro again and again just reload extension.

==================  

**CREDIT INFORMATION**

Reporter credit: Ahmed ElMasry

==================  

Thank you for your attention. with kind Regards

## Attachments

- [content-script.js](attachments/content-script.js) (text/plain, 275 B)
- [script.js](attachments/script.js) (text/plain, 434 B)
- [manifest.json](attachments/manifest.json) (text/plain, 528 B)
- [sidepanel-tab.html](attachments/sidepanel-tab.html) (text/plain, 594 B)
- [service-worker.js](attachments/service-worker.js) (text/plain, 959 B)
- [page.html](attachments/page.html) (text/plain, 2.0 KB)
- [Bypass-Linux-Dev-V120-NG-2023-10-31_14-24-12.mp4](attachments/Bypass-Linux-Dev-V120-NG-2023-10-31_14-24-12.mp4) (video/mp4, 1.4 MB)
- [Bypass-Linux-DEV-V120-SideNG-2023-10-31_14-07-59.mp4](attachments/Bypass-Linux-DEV-V120-SideNG-2023-10-31_14-07-59.mp4) (video/mp4, 1.6 MB)
- [autofillpop-cursor-win-ref.html](attachments/autofillpop-cursor-win-ref.html) (text/plain, 2.9 KB)
- [cursor-128x128-autoXY.png](attachments/cursor-128x128-autoXY.png) (image/png, 2.9 KB)

## Timeline

### [Deleted User] (2023-10-31)

[Empty comment from Monorail migration]

### xi...@chromium.org (2023-10-31)

Thanks for the detailed report. Looping in the original owner of https://crbug.com/1472404 to take a look.

Reporter, does this regression apply to versions earlier than V120? Looks like the side panel extension API was introduced before V118. This will help us set the right FoundIn- label. Thanks!

[Monorail components: UI>Browser>Autofill]

### [Deleted User] (2023-10-31)

[Empty comment from Monorail migration]

### el...@gmail.com (2023-10-31)

Hello Xinghui xinghuilu@

Thanks for first triage.!

>>does this regression apply to versions earlier than V120?

Chrome 116 introduces sidePanel.open(). It allows extensions to open the side panel through an extension user gesture, such as clicking on the action icon. Or a user interaction on an extension page or content script.

So , FoundIn-118 label is appropriate for this as the main bug commits introduced at V 118.0.5967.0 .

One More thing:
-------------------------
While doing my tests with Main Bug https://crbug.com/chromium/1472404 PoC at https://vrphunt.com/chrome/1PxScreen/online-poc-win.html the Bug is Fixed and Mitigation Works well in current both (Stable V118 and Dev V120) chrome versions ,so i made in analysis Bypass part and regression part ,this Side panel Api behavior  Break these mitigation and bug back again with this api .
But if you tried to repro the main bug poc as mentioned the bug is fixed and commits prevent hiding Autofill popup under Custom Cursor overlay at the same time.

Hope this info helps you, and i'am here ready for any info needed help fixing this.

Thanks 


### [Deleted User] (2023-11-01)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jk...@google.com (2023-11-06)

[Empty comment from Monorail migration]

### jk...@google.com (2023-11-10)

Ken, could you PTAL? I am divided on what the right approach is here. Should we *always* disallow custom cursors in content that's shown in the side panel? It seems to me that the benefit of custom cursors in a side panel should be pretty limited.

### jk...@google.com (2023-11-13)

Wrote a one-pager with options: go/autofill-custom-cursor-suppression-for-extensions

### el...@gmail.com (2023-11-15)

[Comment Deleted]

### el...@gmail.com (2023-11-15)

Hi Jan  jkeitel@,.
have you figured out the right approach to fix this issue? , if you don't mind share this  in a comment ,so i could  have a look  as  go/autofill-custom-cursor-suppression-for-extensions  is for internal googlers  only ?  ,  i think sharing will help digging further for better mitigation to stop producing other variants :)   , Thank you

### gi...@appspot.gserviceaccount.com (2023-11-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b538fa86076f4b0baa35c4eea2576dec2c1348e6

commit b538fa86076f4b0baa35c4eea2576dec2c1348e6
Author: Jan Keitel <jkeitel@google.com>
Date: Tue Nov 28 13:32:30 2023

Include extension hosts in custom cursor suppression.

Prior to this CL, the CustomCursorSuppressor suppressed custom cursors
in all WebContents that belonged to a Browser object, but not
WebContents that host extension content. This CL extends the custom
cursor suppression to all WebContents that belong to an extension
for any of the profiles for which Browser objects exist.

Bug: 1497985
Change-Id: I9648cd735cc2969ee9b08e814230574ab75134e2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5023870
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
Reviewed-by: Ken Buchanan <kenrb@chromium.org>
Commit-Queue: Jan Keitel <jkeitel@google.com>
Cr-Commit-Position: refs/heads/main@{#1229867}

[modify] https://crrev.com/b538fa86076f4b0baa35c4eea2576dec2c1348e6/components/autofill/core/common/autofill_features.cc
[modify] https://crrev.com/b538fa86076f4b0baa35c4eea2576dec2c1348e6/extensions/browser/extension_host_registry.cc
[modify] https://crrev.com/b538fa86076f4b0baa35c4eea2576dec2c1348e6/chrome/browser/ui/views/autofill/popup/custom_cursor_suppressor.cc
[modify] https://crrev.com/b538fa86076f4b0baa35c4eea2576dec2c1348e6/chrome/test/BUILD.gn
[modify] https://crrev.com/b538fa86076f4b0baa35c4eea2576dec2c1348e6/extensions/browser/extension_host_registry.h
[modify] https://crrev.com/b538fa86076f4b0baa35c4eea2576dec2c1348e6/components/autofill/core/common/autofill_features.h
[add] https://crrev.com/b538fa86076f4b0baa35c4eea2576dec2c1348e6/chrome/browser/ui/views/autofill/popup/custom_cursor_suppressor_browsertest.cc
[modify] https://crrev.com/b538fa86076f4b0baa35c4eea2576dec2c1348e6/chrome/browser/ui/views/autofill/popup/custom_cursor_suppressor.h


### jk...@google.com (2023-12-01)

Ahmed,

Could you please check whether the issue is now resolved on Canary? Any build 121.0.6154.0 and newer should have the fix included.

Thanks,
Jan

### el...@gmail.com (2023-12-03)

Hello Jan .,

Thank you for your great efforts solving this bug as well !

** From my side i see that the bug is now fully fixed  by the commit you introduced here**

This is the the properties of the chrome version  which i tested the bug in 
-------------------
Google Chrome Version : 121.0.6156.3 (Official Build) dev (64-bit) 
Revision: 751dc6522a1400e897d089e1e02bfec30ea9eaf7-refs/branch-heads/6156@{#7}
Channel:Dev
Milestone: 121
Branch: 6156
Branch Base Position: 1230501
OS: Linux
-----------------

**Feel Free to Mark this as Verified**  

** I have found another Bug Which is quite similar to this root cause , and asked to CC you there , if you would like to take a look https://crbug.com/chromium/1507659  , I think  this is Quite Similar Root Cause But with different  measure Bypassed. ** 

Thank you 


### jk...@google.com (2023-12-04)

Hi Ahmed,

Please cc me on that bug.

Thanks,
Jan

### el...@gmail.com (2023-12-04)

Hello Jan .,

This https://crbug.com/chromium/1507659 still in triage queue and not assigned yet as it was submitted yesterday, and asked to cc you, as i don't have a permission to cc you there, could you ask internally for  being Cc'd  there , i already asked there too.

-for this Current Bug  here , this Bug is fixed and Verified as per C13  .

Thank you


### jk...@google.com (2023-12-04)

[Empty comment from Monorail migration]

### jk...@google.com (2023-12-04)

Thank you!

### [Deleted User] (2023-12-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-04)

[Empty comment from Monorail migration]

### el...@gmail.com (2024-01-21)

Hello, Any updates about reward decision as it is in panel queue since December?

Friendly Ping:
amyressler@ , mlerman@ , jkeitel@

Thank you 

### ml...@chromium.org (2024-01-22)

Including Amy on CC to address c#20

### am...@chromium.org (2024-01-22)

Hi Ahmed, there is a small backlog following the winter festive period as well as some of the panel (like me) dealing with illness, impacting panel sessions. Since this is a low-severity issue, it is lower in the list and is taking longer to get to. We'll certainly be reviewing this bug in a forthcoming panel session. We appreciate your patience in the meantime. 

### el...@gmail.com (2024-01-22)

Hi Amy, thank you for the update. Wishing you a swift recovery. 
I understand the backlog after the festive period. and looking forward to the forthcoming panel session. Take care!

Thank you

### pg...@google.com (2024-01-22)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2024-01-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8809fa2058b48157015354d3893170a191afdab3

commit 8809fa2058b48157015354d3893170a191afdab3
Author: Jan Keitel <jkeitel@google.com>
Date: Tue Jan 23 13:48:33 2024

Clean up kAutofillPopupExtensionCursorSuppression.

This feature was default-enabled in M121 and can now be cleaned up.

Bug: 1497985
Change-Id: Ia7208eff1eef7271d2d00fce13e52ebaf641ebf3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5222523
Auto-Submit: Jan Keitel <jkeitel@google.com>
Commit-Queue: Jan Keitel <jkeitel@google.com>
Reviewed-by: Timofey Chudakov <tchudakov@google.com>
Cr-Commit-Position: refs/heads/main@{#1250782}

[modify] https://crrev.com/8809fa2058b48157015354d3893170a191afdab3/components/autofill/core/common/autofill_features.cc
[modify] https://crrev.com/8809fa2058b48157015354d3893170a191afdab3/chrome/browser/ui/views/autofill/popup/custom_cursor_suppressor.cc
[modify] https://crrev.com/8809fa2058b48157015354d3893170a191afdab3/components/autofill/core/common/autofill_features.h


### pg...@google.com (2024-01-23)

[Empty comment from Monorail migration]

### pg...@google.com (2024-01-23)

[Empty comment from Monorail migration]

### am...@google.com (2024-02-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-02)

Congratulations Ahmed! The Chrome VRP Panel has decided to award you $2,000 for this report. The reward amount was determine based on the precondition of the malicious extension and the amount of UI interaction a user would need to be convinced to perform to achieve this bypass. Thank you for your efforts and reporting this issue to us, as well as for your patience while we caught up on our VRP backlog! 

### el...@gmail.com (2024-02-02)

Thank you Amy for the reward!

### am...@google.com (2024-02-02)

[Empty comment from Monorail migration]

### is...@google.com (2024-02-02)

This issue was migrated from crbug.com/chromium/1497985?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-12)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40075980)*
