# Security: Bypass the Protection of input fields cache (Autofill) 1395164

| Field | Value |
|-------|-------|
| **Issue ID** | [40076065](https://issues.chromium.org/issues/40076065) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | el...@gmail.com |
| **Assignee** | vi...@google.com |
| **Created** | 2023-11-01 |
| **Bounty** | $5,000.00 |

## Description

# **VULNERABILITY DETAILS** :

This Issue is an interesting Bypass for (<https://crbug.com/chromium/1395164>) which was a Bypass of (<https://crbug.com/chromium/1358647>) that recently fixed.

But This case mainly clear bypass for the two commits introduced in last bypass at 1395164 to trick the observer class at PictureInPictureWindowManager which discussed below in details.

\*\*(so Please Add Same Folks of 1395164 to take the ownership of this issue)\*\*

\*\*Please Add Meduim Severity as per Severity Guidelines for Security Issues `https://www.chromium.org/developers/severity-guidelines/#medium-severity` referencing to Main Issue Bypassed before <https://crbug.com/chromium/1358647> \*\*

This is a report to a security vulnerability in google chrome/chromium browser as high-quality report with functional exploit. this vulnerability allows attackers to steal the cache of input fields like usernames, e-mail addresses, telephone numbers from any site like twitter, google and any others (Chrome Autofill Saved Data).

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

## Bisection (Commits introduced the bug):

Actually this bug found because of the two Commits(<https://crbug.com/chromium/1395164>) at

[1]- <https://chromium-review.googlesource.com/c/chromium/src/+/4738656>  

`Add Observer class to PictureInPictureWindowManager`

[2]- <https://chromium-review.googlesource.com/c/chromium/src/+/4737994>  

`Hide Autofill Popup if hidden behind Pip window`

-This Bug Bypass Was Tested in V120 DEV at Linux and works , But while testing it to Stable V118 at Linux the behavior is different a little bit.

## ==================== Root Cause Analysis:

Idea of Attack and How Attack works:  

**-------------------------** -----------  

the main Bug <https://crbug.com/chromium/1395164> root cause was showing the autofill popup at the same time of PIP Overlay at OnEnterPictureInPicture() event, so the fix was adding Observer class to PictureInPictureWindowManager and some code to Hide Autofill Popup if hidden behind Pip window,which prevent showing autofill popup while entering picture in picture mode.

But Actually after looking at Observer code in commit [1] as discussed below , an idea came to my mind to trick the observer and force it to return non real value so Autofill Won't be dismissed while presence and also after presence of pip ovelay which also bypass the CL code that checks the intersection between autofill popup and pip overlay, the popup showing and accepts user events from keyboard selecting the autofill popup indexes means that  `the observer really returns false value for `bool ExitPictureInPicture();` and feels it is in Exit picture in picture mode "this what i guess from behaviors i saw while testing , may be can be confirmed with some debugging and traces , but it is clear"`

so i played on this idea and tried to make the code function as below:

1- when user press key down , there are two delayed piciture in picture requests to do the race of observer  

setTimeout(() => {video.requestPictureInPicture();}, 60);  

setTimeout(() => {video.requestPictureInPicture();}, 40);

1st setTimeout make the observer to be added but the 2nd setTimeout calls the observer again (re-initiate the process) , and here the observer invoke and re-added at this time Autofill Was Already Shown and accepts user inputs , and observer was raced and autofill will be behind.

Explain with Code as Below:  

**-------------------------** ---  

Race Observer releated code

void AddObserver(Observer\* observer) { observers\_.AddObserver(observer); }  

void RemoveObserver(Observer\* observer) {  

observers\_.RemoveObserver(observer);  

}

-In the following code part t the observer class check PictureInPictureWindowManager events while OnEnterPictureInPicture().

// Observer for PictureInPictureWindowManager events.  

class Observer : public base::CheckedObserver {  

public:  

virtual void OnEnterPictureInPicture() {}  

};

So due to the race haapened the observer wasn't able to notice the presence of Autofill popup as EnterPictureInPictureWithController  

doesn't return the real value at `bool ExitPictureInPicture();`

---

`bool ExitPictureInPicture();`  

// Returns true if a picture-in-picture window was closed, and false if there  

// were no picture-in-picture windows to close..

**-------------------------** ---------------------------------------------  

Very Important info noticed while testing to proof the analysis above:  

**-------------------------** ---------------------------------------------

-While Repro the case when you open new fresh tab and put the url and go the race happen and attack works as in POC video Attached Below.  

-If you Reloaded the Page the PIP Overlay will be exited But the flag of bool ExitPictureInPicture(); should be reset and the observer should observe that , so in the nest time the flag value will be initiated correctly , so when reload the page the flag gets it last value from the previous state of showing the overlay at 1st time , but if you close the current tab and opened new one all things in reset and fresh (this is important key point noticed during tests , and i tested this many times and i confirm that behavior)

so `NotifyObservers(&Observer::OnEnterPictureInPicture);` which is in `PictureInPictureWindowManager::EnterVideoPictureInPicture`  

may need to be implemented same and notify observer in `PictureInPictureWindowManager::ExitPictureInPicture()` ,which is in M  

chrome/browser/picture\_in\_picture/picture\_in\_picture\_window\_manager.cc

## ===================== **REPRODUCTION CASE** :

the exploit use a vulnerability in showing of cache of input fields. your browser suggests the saved entries of input fields like saved user logins (username, email, phone number...) or cached search word any similar entered things.

nobody will send critical information to unknown sites. but this can be hide by full bypassing the visibility of all fields and suggests. in this case nobody are able to notice that they are sending their data to unknown attackers.

# ===================== REPRODUCTION STEPS:

(Play a little jump and run game (Dino) to get hijacked any cached input of field-name "username",email,telephone,address,card-number,.....)

\*\*Before Repro you can add some data under chrome://settings/addresses and add some records

1- Visit <https://vrphunt.com/chrome/autofill-dbl-bypass-cve-mod.html>

2- Press (DOWN Arrow) then (ENTER) to start Game

\*\* Autofill data Will be shown in the Green Box , Which Could be sent to Attacker Remote Side \*\*

---

## Important Note: if you tested the POC and want to test it again, please close the opened tab and Re open a new one `Don't reload` . "discussed above in detail why"

+Feel free to test with Online POC , Also Offline File is also attached.

# ========================== Observed (What's Go wrong):

Autofill popup can be hidden, as popup not visible to user and fully Covered by Picture in Picture (PIP) Overlay and this bypasses the CL made on previous issues:  

<https://chromium.googlesource.com/chromium/src/+/4e7da365c93558d6d13e1a682ce9cf3de1ce0922>  

<https://chromium.googlesource.com/chromium/src/+/3722137e2168a6df67f4fa519ad4d9728605a1bb>  

<https://chromium.googlesource.com/chromium/src/+/d2e718e05d222bfb1c7df8e462b0eb7ca4f4c202>

Reason for that: Autofill popup shown at the same time of PIP transition racing the observer and keeps behind this bypass the previous CL.

# Expected:

Sensitive browser UI is always visible to user ,so Hide Autofill popup if it overlaps with picture-in-picture window.

# ===================== Mitigation:

Maybe the Fix can Be from Autofill side 1st , as while drawing Autofill Popup , it should send bool falg like "AutofillShown" true or false to the pip observer, and if true the observer prevent showing the pip overlay so this will guarantee that autofill popup will not be shown while PIP Overlay is Present (Just need add Check from opposite side (Autofill side) not from `PIP` Side).

# ===================== **CREDIT INFORMATION** Reporter credit: Ahmed ElMasry

Thank you for your attention. with kind Regards

## Attachments

- [autofill-dbl-bypass-cve-mod.html](attachments/autofill-dbl-bypass-cve-mod.html) (text/plain, 6.9 KB)
- [inst-overlay.mp4](attachments/inst-overlay.mp4) (video/mp4, 22.6 KB)
- [Bypass-Autofill-Dev-V120-Linux-2023-11-01_15-34-00.mp4](attachments/Bypass-Autofill-Dev-V120-Linux-2023-11-01_15-34-00.mp4) (video/mp4, 871.4 KB)
- [Bypass-Autofill-Dev-V120-Incognato-Linux-2023-11-01_15-36-06.mp4](attachments/Bypass-Autofill-Dev-V120-Incognato-Linux-2023-11-01_15-36-06.mp4) (video/mp4, 903.9 KB)
- [Bypass-Autofill-Win-Canary-V121- 2023-11-03 22-29-27-524.mp4](attachments/Bypass-Autofill-Win-Canary-V121- 2023-11-03 22-29-27-524.mp4) (video/mp4, 2.1 MB)
- [bypass-Autofill-Win-Dev-V120- 2023-11-03 22-35-50-541.mp4](attachments/bypass-Autofill-Win-Dev-V120- 2023-11-03 22-35-50-541.mp4) (video/mp4, 2.0 MB)
- [Canary-V123-WIN 2024-01-25 22-39-08-325.mp4](attachments/Canary-V123-WIN 2024-01-25 22-39-08-325.mp4) (video/mp4, 2.5 MB)

## Timeline

### [Deleted User] (2023-11-01)

[Empty comment from Monorail migration]

### xi...@chromium.org (2023-11-01)

Thanks for the detailed report. Triaged the same way as https://crbug.com/1395164. Keeping it the same severity as the previous bug since this also leverages the Picture in Picture API with a more crafted timing. +vidhanj@ to take a look.

[Monorail components: UI>Browser>Autofill]

### [Deleted User] (2023-11-01)

[Empty comment from Monorail migration]

### el...@gmail.com (2023-11-03)

Hello vidhanj@

Additional Info:
--------------------
Today i've tested the main poc url in Windows platform  to confirm that the bug repro in  chrome for windows too 

Exploit tested with the following properties:
----------------
latest canary Build of Today

Google Chrome:121.0.6105.0 (Official Build) canary (64-bit) (cohort: Clang-64) 
Revision: e16a807bbf30a988a480f036fc05275c191f4bd0-refs/branch-heads/6105@{#1}
Channel: canary (64-bit) (cohort: Clang-64) 
Version:121.0.6105.0
Milestone: 121
Branch: 6105
Branch Base Position:1219441
OS: Windows 11 Version 22H2 (Build 22621.2428)

----------
Google Chrome:120.0.6090.0 (Official Build) dev (64-bit) (cohort: Dev) 
Revision: 6ddf75e883b7682c7c4f262b00ba04df8bd1e35e-refs/branch-heads/6090@{#1}
Channel: Dev (Official Build) (64-bit) (cohort: Dev) 
Version: 120.0.6090.0
Milestone: 120
Branch: 6090
Branch Base Position: 1215263
OS:Windows 11 Version 22H2 (Build 22621.2428)
----------
Thank you

### el...@gmail.com (2023-11-03)

[Empty comment from Monorail migration]

### el...@gmail.com (2024-01-21)

Hello Vidhan 	vidhanj@ , Mike mlerman@, Frank liberato@

Additional Information that may help you here , since there is  a new  CLs [1] , [2]  landed and merged recently and related to this area and introduced new OcclusionTracker for PIP window , so you can benifit and use their features to observe PiP and fix this issue .

[1] https://crrev.com/c/5041595 

picture-in-picture: Add PictureInPictureOcclusionTracker

This CL adds a PictureInPictureOcclusionTracker, which keeps track of
picture-in-picture widgets and widgets that need to know when they're
occluded by a picture-in-picture window, and notifies observers when
the occlusion state changes.

This will be used to ensure that security-sensitive UI does not get
covered up by a picture-in-picture window, which would leave the user
vulnerable to spoofing.

This CL just adds the tracker, but does not register any
picture-in-picture widgets to it nor any observers.
--------------

[2] https://crrev.com/c/5041437

picture-in-picture: Inform occlusion tracker of PiP widgets

This CL registers video and document picture-in-picture widgets with
the PictureInPictureOcclusionTracker. The tracker can then inform
observers when their widgets are occluded by a picture-in-picture
widget.
---------------

Thank You 


### el...@gmail.com (2024-01-25)

Hello vidhanj@

Additional Info:
--------------------
another test on Windows platform Chrome Canary M123

Exploit tested with the following properties:
----------------
latest canary Build of Today

Google Chrome: 123.0.6265.0 (Official Build) canary (64-bit) (cohort: Clang-64) 
Revision: 41844629858e9f4868a8630ad69282d7ab5c2682-refs/branch-heads/6265@{#1}
Version: 123.0.6265.0
Milestone: 123
Branch: 6265
Branch Base Position: 1252026
OS: Windows 11 Version 22H2 (Build 22621.3007)
---------------------
**Poc Video Repro Attached for M123**

**Same Repro Steps but with this URL `` https://vrphunt.com/chrome/autofill-bypass-cve-mod-restricted.html ``

1- Visit  https://vrphunt.com/chrome/autofill-bypass-cve-mod-restricted.html

2- Press (DOWN Arrow) then (ENTER) to start Game

Exfiltrated data will be shown in the green box as in poc video 
-------------------

Thank you for your attention and working on this.



### is...@google.com (2024-01-25)

This issue was migrated from crbug.com/chromium/1498460?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### ap...@google.com (2024-02-20)

Project: chromium/src
Branch: main

commit 6f47893479118f73e9df78558057387c7f09bdb0
Author: Vidhan <vidhanj@google.com>
Date:   Tue Feb 20 18:23:40 2024

    Notify PictureInPicture observers once the window has been created
    
    Before this CL, PictureInPictureWindowManager would inform the observers
    mainly EnterPictureInPicture on
    PictureInPictureWindowManager::EnterVideoPictureInPicture. But, the
    window load is asynchronous to this function. When autofill would try to
    get the bounds of the picture-in-picture window, they would be null due
    to the asynchronicity. As a result, the autofill popup won't get hidden
    due to an overlap of bounds.
    
    This CL fixes this issue by notifying the observers once the
    picture-in-picture window has been created.
    
    Bug: 1498460
    Change-Id: Iecb1a4067aaf6f2112d29f65ce9a34bf5ad05eb6
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5185800
    Reviewed-by: Avi Drissman <avi@chromium.org>
    Reviewed-by: Frank Liberato <liberato@chromium.org>
    Commit-Queue: Vidhan Jain <vidhanj@google.com>
    Cr-Commit-Position: refs/heads/main@{#1262795}

M       chrome/browser/picture_in_picture/picture_in_picture_window_manager.cc
M       chrome/browser/picture_in_picture/picture_in_picture_window_manager.h
M       chrome/browser/picture_in_picture/picture_in_picture_window_manager_unittest.cc
M       chrome/browser/picture_in_picture/video_picture_in_picture_window_controller_browsertest.cc
M       chrome/browser/ui/autofill/autofill_popup_controller_impl_unittest.cc
M       chrome/browser/ui/views/overlay/video_overlay_window_views_unittest.cc
M       content/browser/picture_in_picture/video_picture_in_picture_window_controller_impl.cc
M       content/browser/picture_in_picture/video_picture_in_picture_window_controller_impl.h
M       content/public/browser/video_picture_in_picture_window_controller.h
M       content/public/test/DEPS
A       content/public/test/mock_video_picture_in_picture_window_controller_impl.cc
A       content/public/test/mock_video_picture_in_picture_window_controller_impl.h
M       content/test/BUILD.gn

https://chromium-review.googlesource.com/5185800


### el...@gmail.com (2024-03-13)

Hello Vidhan,
Just wanted to check if there is any other work to do here?

`From my side i can confirm that the behavior is fixed by the committed CL above and i've tested this against different versions after landing fix` .

**If you feel that there no more work to do here from your side ,please Mark this as `Fixed/Verified`** to let automation bot add appropriate labels .

Thank you

### am...@google.com (2024-03-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-03-22)

Congratulations Ahmed! The Chrome VRP Panel has decided to award you $5,000 for this report. Thank you for your efforts in discovering and reporting this issue to us -- nice work!

### el...@gmail.com (2024-03-23)

Thank you for the reward

### pe...@google.com (2024-06-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076065)*
