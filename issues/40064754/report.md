# Security: Spoofing Permission Prompts UI behind PIP overlay-Bypass of 1394410 

| Field | Value |
|-------|-------|
| **Issue ID** | [40064754](https://issues.chromium.org/issues/40064754) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Media>PictureInPicture, UI>Browser>Permissions>Prompts |
| **Platforms** | Linux |
| **Reporter** | el...@gmail.com |
| **Assignee** | st...@chromium.org |
| **Created** | 2023-05-23 |
| **Bounty** | $2,000.00 |

## Description

# **VULNERABILITY DETAILS**

This issue is similar to <https://crbug.com/chromium/1237310> and bypass of <https://crbug.com/chromium/1394410> and Exploitation way is similar to <https://crbug.com/chromium/1358647>

This is a report to a security vulnerability in google chrome/chromium browser as high-quality report with functional exploit. here this vulnerability allows attackers to

1-Spoof All Permission Prompts, which is totally hidden , and Attacker can gain super permissions for his website Like:

(Clipboard Data & Mic & Camera & Location & Screen Sharing,..etc)

2-Attacker Can Read the Data (text,images) copied to the clipboard that also can be chained with CTRL+A CTRL+C ,this could leak Google/Facebook/Twitter username and passwords ,...etc

3-Attacker Can trick user to do harmful actions in Sensitive pages (Like Chrome Flags or Reset all Config , Stop Sync,..etc)

> > chrome://flags/ using (TAB and ENTER) Similar to what POC Video Shown  
> > 
> > chrome://settings/resetProfileSettings?origin=userclick (TAB TAB TAB ENTER),... same idea of POC Video

4-Attacker Can Navigate the hidden Window with any website that contain token or sensitive data and use CTRL+A CTRL+C to steal usernames, e-mail addresses, telephone numbers from any site like twitter, google and any others or Navigate the hidden window and resize it to get the data with Screen Sharing that was permitted in step 1

==================================  

Root cause and Behavior Analysis:  

**-------------------------** ---------

The <https://crbug.com/chromium/1394410> was fixed by this commit(<https://chromium.googlesource.com/chromium/src/+/073278eae6d6ce07cc40107567907e545ec56157>)

(Ignore button pressed event if button row intersects with PiP window) , which isn't sufficient in this case ,because there are two different behaviors for permission prompt while showing:

[A]-Windows: after popup windows opened and popup shown asking permission ,there is a good behavior in showing the prompt which is "if the permission prompt popup size isn't fitted/or larger than content-area of the popup window it will re-allocate it's position automatically to show permission prompt above this window because it doesn't fit it"  

[B]-Linux: in Linux if the permission prompt is larger than the content-area of the popup windos it will be fitted and content area can cover part of the permission prompt and the prompt keeps in content-area unlike in windows, make this more likely to be spoofed ,if the popup window is docked to narrow size the permission prompt is clipped and still remains inside ,so the bypass can be triggered from this point[1].

## How Attack works?

from Point[1] we can try to dock the size of the popup window to make the permission prompt clipped and making the raw of buttons hidden down in the clipped area of "content-area" bypassing the intersection check made by the commit above (073278eae6d6ce07cc40107567907e545ec56157), so there is no intersection and attack(bypass) happens.

Here in the POC,i have Demonstrated Clipboard Permission (as simple case) but i tested all other scenarios Dialogs in the previous one, but one is sufficient to show the case.

Victim Play War Game , Just Pick your Weapons 1ST to Start Game and Attacker Got Sensitive Data and User Allow Permissions Without Being aware

# on Video PoC

User Asked to Pick Weapons before Start Game and behind the Scene these actions take effect

Attacker Website Asks for Clipboard Permission (user accept with TAB TAB TAB ENTER) ,this is totally hidden behind Picture in Picture Black Window

---

## Version:

## Old Bug Fixed in this version

Google Chrome Canary:115.0.5764.0  

Version:115.0.5764.0  

Milestone:115  

Branch:5764  

Branch Base Position:1142443  

Branch Base Commit:<https://chromium.googlesource.com/chromium/src/+/886736784d414d3a4c5b8d503a0043ba00ac7f94>  

OS:Linux  

**-------------------------** ----------------  

1st Commit introduced the Bug by as below:  

**-------------------------** ----------------  

Commit:<https://crrev.com/073278eae6d6ce07cc40107567907e545ec56157>  

Cr-Commit-Position: refs/heads/main@{#1141985}  

Description:Ignore button pressed event if button row intersects with PiP window  

**-------------------------** ----------------  

Bug Tested With the Following Properties:  

**-------------------------** ----------------  

Google Chrome:115.0.5773.4 (Official Build) dev (64-bit)  

Revision:f255fbf1fbd3eceb020c09db1d8e65f381700040-refs/branch-heads/5773@{#8}  

Version:115.0.5773.4  

Milestone:115  

Branch:5773  

Branch Base Position:1143970  

OS:Linux  

**-------------------------** ----------------  

Chromium:115.0.5773.0 (Developer Build) (64-bit)  

Revision:6db637d10240aa61c6c01450f0ae542d2f2652b1-refs/heads/main@{#1143952}  

asan-linux-release-1143952  

OS:Linux

# **-------------------------** ---------------- **REPRODUCTION CASE**

the exploit use a vulnerability in showing

nobody will send critical information to unknown sites /Share Screen with , or allow to read Clipboard Sensitive data or Allow any Permissions to unknown Website. but this can be hide by full bypassing the visibility of all Prompts. in this case nobody are able to notice that they are sending their data to unknown attackers or allowing them to use Power Permissions for their Websites.

# REPRODUCTION STEPS

"Host the attached files on your Server and test , or simply Use Online Poc as below"

(Play a War Game , Just Pick your Weapons 1ST to Start Game and Attacker Got Sensitive Data and Victim Allow Critical Permissions Without Being aware

1-Visit <https://vrphunt.com/chrome/spoof-leak/canvasautofill-modx-linux-doooh-dev.html> (for Linux Only)

2- Follow Instructions of the Game to Pickup Weapons once shown (TAB -TAB -TAB -Enter).

3-Check Site Permissions to see the permissions you have allowed attacker to use.

4-Close PIP (Picture in Picture Overlay) Right Bottom Corner and Check Permissions of the website like in POC Videos.

# ==================== Observed:

Permission Prompts can be totally hidden as discussed in root cause analysis above, as popup window not visible to user and fully Covered by Picture in Picture (PIP) Overlay,This Obscured active window accepts keyboard input in sensitive browser UI and web pages that can be used to steal user data through Clipboard and attacker control the navigation for this popup or let user do harmful actions like discussed above.

# Expected:

Sensitive browser UI is always visible to user so Hide Permission Prompts popup if it overlaps with picture-in-picture window.

# ===================== Mitigation:

# Fix1:

# Add Another CL to Hide Permission Prompts popup if it overlaps with picture-in-picture window. Fix2:

## Add CL for getting permission prompt size and compare it with content-area size if the permission prompt can be fitted in content area it's okay if not i suggest the behavior like in Windows ,showing the prompt above the popup window this make the previous CL <https://chromium.googlesource.com/chromium/src/+/073278eae6d6ce07cc40107567907e545ec56157> still valid just need a few changes in compare of size.

# \*\*Poc Videos of Linux Tests Directly Attached \*\*Local Offline Files (Poc) Directly Attached \*\*simple short video for Behavior causing the Bug(as stated in Root cause analysis) Directly Attached.

# **CREDIT INFORMATION**

# Reporter credit: Ahmed ElMasry

Thank you for your attention. with kind Regards

## Attachments

- [canvasautofill-modx-linux-doooh-dev.html](attachments/canvasautofill-modx-linux-doooh-dev.html) (text/plain, 6.9 KB)
- [share-me-doooh.html](attachments/share-me-doooh.html) (text/plain, 2.8 KB)
- [giphy.webm](attachments/giphy.webm) (video/webm, 5.6 KB)
- [pickup-weapons.jpeg](attachments/pickup-weapons.jpeg) (image/jpeg, 196.5 KB)
- [Spoofing-permissions-DEV-115-linux-2023-05-23_18-14-50.mp4](attachments/Spoofing-permissions-DEV-115-linux-2023-05-23_18-14-50.mp4) (video/mp4, 2.3 MB)
- [Spoofing-Developer-115-ASAN-2023-05-23_18-10-09.mp4](attachments/Spoofing-Developer-115-ASAN-2023-05-23_18-10-09.mp4) (video/mp4, 2.4 MB)
- [Linux-behavior-2023-05-23_18-17-45.mp4](attachments/Linux-behavior-2023-05-23_18-17-45.mp4) (video/mp4, 540.7 KB)

## Timeline

### [Deleted User] (2023-05-23)

[Empty comment from Monorail migration]

### wf...@chromium.org (2023-05-23)

Thanks for your report. I'm triaging this to the same folks as the last bugs, and then I will look in more detail at the reproduction case in secondary triage. This doesn't look like a new regression but another variant of the report in https://crbug.com/chromium/1394410 so I am setting foundin to pre-extended-stable. I assess the severity of this to Medium to match the other report but could be convinced this was Low severity given the number of interactions required to trigger.

[Monorail components: Blink>Media>PictureInPicture UI>Browser>Permissions>Prompts]

### [Deleted User] (2023-05-23)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-23)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-31)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-06)

tungnh: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tu...@chromium.org (2023-06-07)

I did not have a chance to take a look at this new variant, but in general, hiding the prompt is a bad idea, it might cause user confusion and increase code complexity.
The new variant requires too many user interactions, and only has effect to Linux. I will reduce the pri to 2 and low severity.



### el...@gmail.com (2023-06-07)

Hello Thomas tungnh@ , thanks for your feedback.,
I'd like to mention some important notes about  this:

>>hiding the prompt is a bad idea, it might cause user confusion and increase code complexity.
Rep:/  I think the confusion if the prompt is seen by the user and was dismissed, but in this case the user didn't see any prompts at all because it is totally hidden behind the PIP overlay , i remember Autofill bug that was resolved before by dismissing the Autofill popup if it intersect with PIP overlay , which i think the same case here.

>>The new variant requires too many user interactions, and only has effect to Linux. I will reduce the pri to 2 and low severity

Rep:/ About the user interaction: this variant user interaction is same as the main https://crbug.com/chromium/1394410 , and i just reproduced this on the Linux environment and made the poc fit this environment testing , but can be works if i changes the size of aspect ratio of the pip video "black" which running in PIP overlay which could cover all the popup and the permission prompt shown, or another way for any os it could be exploited if the user enabled #document-picture-in-picture-api flag , this flag allow user to open pip with any size without aspect ratio restrictions making this bug  have a hight probability of exploitation without user awareness, so could you please "pump this prio up" ,and also "assign different OS labels as before", because it may be bypassed if it's fixed by another way than dismiss the prompt if it was covered by PIP overlay.

Another Hint : i've made the poc for linux as fast as possible to show the vulnerability exploitation and avoid duplicates:).

Thanks Thomas 


### tu...@chromium.org (2023-06-12)

Thanks for reporting the issue.
I have not started looking at the details/code/security measures, just tried to reproduce on Mac and Windows and it does not work for me. Am I missing anything? One of your suggestion is `to fix the behavior the same as Windows` (indicates it does not work on Windows).




### el...@gmail.com (2023-06-12)

Hello Thomas., Yah here the repro focused on 'Linux'  as shown on poc Video above, because of the behavior of the prompt for being clipped without pop up out of the web content area.

I don't have MacOs Machine, but what i believe that,"Hide Permission Prompts popup if it overlaps with picture-in-picture window" it will be fine and cover all the variations that may fork from this .
Thanks Thomas for taking care and working on this .


### el...@gmail.com (2023-06-28)

Hi.,tungnh@ This is a friendly reminder to be sure that this report under your radar,and check if there is any updates here?!, Will you address this issue soon?!.
Thanks 

### tu...@chromium.org (2023-07-04)

I can confirm that the issue will not happen on Mac and Windows, because the prompt will not be clipped out and will be visible on screen (key pressing will be ignored if the prompt intersects with PiP)
I am not in favor of hiding the prompt, as we have come to rely on it as an input for prompt intervention, such as putting the permission request on embargo to decline automatically.
In this case of linux, I think, we would ignore any input event if the view is not visible on the viewport or screen, hopefully I can find sometime on it next 2 weeks

### el...@gmail.com (2023-07-04)

Hi ..
>we would ignore any input event if the view is not visible on the viewport or screen
R/ this seems good fix as you mentioned.
>hopefully I can find sometime on it next 2 weeks
R/ thanks for your attention Thomas , and your time working on this !



### el...@gmail.com (2023-07-19)

Hello Thomas.. ,
tungnh@, have you found some time slots to work on this?!

Thanks for your attention and working on this.

### el...@gmail.com (2023-08-02)

Hi tungnh@ .., 
Will you work on the suggested fix at https://crbug.com/chromium/1448132#c12 soon ?!! , It will be nice if you found some time to fix this 
Thanks 

### tu...@chromium.org (2023-08-02)

Sorry, I was a bit slow on this and don't have time slot in the next several weeks.
@engedy, I will be on vacation soon, maybe can we find someone to take over it?

### el...@gmail.com (2023-08-02)

Could you CC engedy@chromium.org to this One too .., Thanks Thomas

### el...@google.com (2023-08-08)

[Empty comment from Monorail migration]

### el...@gmail.com (2023-08-21)

Hi. engedy@ , elklm@
friendly reminder to be sure that this report under your radar,and check if there is any updates here?!, Could you please take a look.
Thanks

### el...@gmail.com (2023-09-11)

Hello there..,
tungnh@ : any Updates on this one and the new variant  at https://crbug.com/1473762?
will you start working on this soon ?
this is a friendly reminder to be sure these still under your radar .
Thanks for your attention ..!

### el...@gmail.com (2023-10-02)

Hi tungnh@ .., 
Just wanted to check, Is this issue still under your radar? 
Will you work on the suggested fix at https://crbug.com/chromium/1448132#c12 soon ?!
, please follow up.
Thanks 

### el...@google.com (2023-11-15)

Reassigning to steimel@ to find a better owner as we should find a general solution for the PiP window.

### is...@google.com (2023-11-15)

This issue was migrated from crbug.com/chromium/1448132?no_tracker_redirect=1

[Multiple monorail components: Blink>Media>PictureInPicture, UI>Browser>Permissions>Prompts]
[Monorail components added to Component Tags custom field.]

### el...@gmail.com (2024-02-21)

Hello,

friendly reminder: Any further progress on this one? , don't hear back back from you for a long time , just wanted to check if this issue got some attention from the owner.

Thank you

### ap...@google.com (2024-02-23)

Project: chromium/src
Branch: main

commit 77cfa22d7ff196ba21ca866982c7715c27321c2e
Author: Tommy Steimel <steimel@chromium.org>
Date:   Fri Feb 23 19:12:01 2024

    [picture-in-picture] Disable permission prompt buttons when occluded
    
    Currently, permission prompts check whether a picture-in-picture window
    occludes the button row before allowing keyboard input to click a
    button. However, there are still ways in which this can be abused by a
    nefarious website.
    
    This CL strengthens that check to not allow any input to click a button
    as long as any of the prompt is occluded by a picture-in-picture
    window.
    
    Bug: 40064754, 40069864
    Change-Id: I212b98838d5242982db483cd77c63625ff5a1a0e
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5315611
    Commit-Queue: Tommy Steimel <steimel@chromium.org>
    Reviewed-by: Elias Klim <elklm@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1264670}

M       chrome/browser/BUILD.gn
M       chrome/browser/picture_in_picture/picture_in_picture_occlusion_tracker.cc
M       chrome/browser/picture_in_picture/picture_in_picture_occlusion_tracker.h
M       chrome/browser/ui/permission_bubble/permission_bubble_browser_test_util.cc
M       chrome/browser/ui/permission_bubble/permission_bubble_browser_test_util.h
A       chrome/browser/ui/permission_bubble/permission_bubble_test_util.cc
A       chrome/browser/ui/permission_bubble/permission_bubble_test_util.h
M       chrome/browser/ui/views/permissions/permission_prompt_base_view.cc
M       chrome/browser/ui/views/permissions/permission_prompt_base_view.h
A       chrome/browser/ui/views/permissions/permission_prompt_base_view_unittest.cc
M       chrome/test/BUILD.gn

https://chromium-review.googlesource.com/5315611


### st...@chromium.org (2024-02-26)

I believe this should be fixed by the CL in comment 26, which is in version 124.0.6319.0 and later. Please reopen if this is still reproducible after that version

### am...@google.com (2024-03-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-03-07)

Congratulations Ahmed! The Chrome VRP Panel has decided to award you $2,000 for this report. The reward amount was determined based on the security impact and potential for user harm, but also taking into account the high degree of user interaction to fully exploit this issue as well as a user being reasonably convinced to engage in the ways required by this POC. Thank you for your efforts and reporting this issue to us!

### el...@gmail.com (2024-03-13)

**`Thanks for the reward Amy`** 🙂

### pe...@google.com (2024-06-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064754)*
