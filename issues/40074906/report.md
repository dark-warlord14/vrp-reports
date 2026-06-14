# Security: No Origin For PresentAPI

| Field | Value |
|-------|-------|
| **Issue ID** | [40074906](https://issues.chromium.org/issues/40074906) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Internals>Cast>UI |
| **Platforms** | Linux, Mac, ChromeOS |
| **Reporter** | ia...@gmail.com |
| **Assignee** | ah...@google.com |
| **Created** | 2023-10-14 |
| **Bounty** | $500.00 |

## Description

Based on my idea its look like similar to 1374518 (Thanks to alesa) where the window does not show Origin of PresenterAPI.


I found that this is not affecting Chrome on Mac and Windows and Android but it is only affecting Chrome Running Chrome OS. Tested On Chrome only.


1. Please browse the https://egghunter.shop/cross.html which have an iframe to DomainB (Crossdomain) from Chrome Running on Chrome OS.
2. Click within iframe and it will not show any origin.

Tested On
Chrome OS Version 117.0.5938.157
Chrome Version 117.0.5938.157

POC Video attached.




## Attachments

- [Screen recording 2023 10 14 2 43 59 PM.mp4](attachments/Screen recording 2023 10 14 2 43 59 PM.mp4) (video/mp4, 227.3 KB)
- [Chrome On ChromeOS.jpg](attachments/Chrome On ChromeOS.jpg) (image/jpeg, 250.2 KB)
- [Chrome on MacOS.jpg](attachments/Chrome on MacOS.jpg) (image/jpeg, 103.7 KB)

## Timeline

### [Deleted User] (2023-10-14)

[Empty comment from Monorail migration]

### ct...@chromium.org (2023-10-17)

Reporter could you please attach the site source to this bug?

Also, are you able to reproduce if you have a Cast target available? In https://crbug.com/chromium/1374518 the proof-of-concept involved the case where a potential cast target exists, and the title was being used instead of the URL. In this case, it looks like just an error message is being shown ("No devices found").

### am...@chromium.org (2023-10-19)

Hello OP, thank you for the report. When you have a moment, can you please respond to https://crbug.com/chromium/1492705#c2. At this time, there is not enough information to continue to triage this as a security issue.  
Setting a next action date of next week. If not further information is provided before that time, we'll need to close this issue as a WontFix / WAI. Thank you. 

### ia...@gmail.com (2023-10-23)

Hello Team,

Can you please set next date of action to the next 7 days. I am looking for a cast device where I can conclude this bug.

Thanks in advance. 

### [Deleted User] (2023-10-23)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ct...@chromium.org (2023-10-23)

Thanks for the update -- let us know if you're able to test.

[Monorail components: Internals>Cast>UI]

### pa...@chromium.org (2023-10-26)

[security shepherd] setting Needs-Feedback again so that we better keep track of this.

### ia...@gmail.com (2023-10-30)

@pal I tested on a real casting device scenario and found that ONLY in ChormeOS chrome browser "If the initiator origin is opaque, the presentation API dialog does not display the origin."

Attaching screenshot of Chrome Running on MacOS where Presentation API shows Origin
Attaching screenshot of Chrome Running on ChromeOS where Presentation API does not shows any Origin..

Ideally the Origin should be shown to the user while casting from an iframed domain, please correct me If am wrong some where.

### [Deleted User] (2023-10-30)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ta...@chromium.org (2023-10-30)

It's possible that this is not a security issue if we're somehow failing to trigger the Presentation API on Chrome OS (and we're falling back to just tab mirroring, which shows that "Cast tab"). But if we are invoking Presentation API without an origin display then it is.

This may be similar to iframe/origin issues Ahmed has looked at in the past.

### ia...@gmail.com (2023-11-06)

Hello Team, have you got a chance to look into the additional details I have provided?

### ch...@google.com (2023-11-07)

[Comment Deleted]

### am...@chromium.org (2023-11-08)

As per https://crbug.com/chromium/1492705#c10, it appears that while this may be specific to the origin is presented on ChromeOS, this appears is potentially a case in which the Presentation API isn't being appropriately triggered on ChromeOS, not an issue in core ChromeOS code. And this may be a functional issue rather than a security issue. I've removed the above comment from ChromeOS regarding bug trackers as this is not a correct process. 

This issue has been assigned to another engineer for an assessment. Let's leave this issue in this tracker as is for now. 
ahmedmoussa@ can you PTAL at soonest to provide an initial evaluation of this issue as a follow on to https://crbug.com/chromium/1492705#c10? 


### ia...@gmail.com (2023-11-08)

@am @ah Fyi, if you browse the report 1374518

The similar problem was mentioned in that report as well where “ if a page with an opaque origin calls the Presentation API, no origin information is shown in the Presentation API dialog”

In my report similar observation I have, If origin called from opaque origin then Chrome Browser Is not showing origin information only on ChromeOS.





### ah...@google.com (2023-11-08)

[Empty comment from Monorail migration]

### ia...@gmail.com (2023-11-21)

Hello Team, have you got a chance to look into this report?

### ia...@gmail.com (2023-12-30)

Hello Team, have you got a chance to look into this report?


### ia...@gmail.com (2024-01-11)

Hello Team, have you got a chance to look into this report?


### ia...@gmail.com (2024-01-20)

Hello Team, have you got a chance to look into this report?


### ia...@gmail.com (2024-01-29)

Hello Team,

Is there any progress on this report?

### is...@google.com (2024-01-29)

This issue was migrated from crbug.com/chromium/1492705?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### ia...@gmail.com (2024-02-13)

Hello Team,

This bug is pending from a long time, Is there any progress on this report?

### ah...@google.com (2024-02-16)

Hello Narendra,
Thanks for waiting. I took a look at the bug, and currently have a [fix CL](https://chromium-review.googlesource.com/c/chromium/src/+/5302328) under review.

By the way, this issue is not specific to ChromeOS, it happens on all platforms when this flag `global-media-controls-cast-start-stop` is disabled. Currently, it is enabled by default.

### ap...@google.com (2024-02-16)

Project: chromium/src
Branch: main

commit fb19f1ba2ae207e82a82ac3bfc4981eebfae39da
Author: Ahmed Moussa <ahmedmoussa@google.com>
Date:   Fri Feb 16 19:38:33 2024

    Fix PresentationRequest Origin not shown issue when Opaque
    
    When `global-media-controls-cast-start-stop` is disabled, the origin
    info from the PresentationRequest is not shown when the origin is
    opaque. This CL fixes that issue.
    
    Bug: b:40074906
    Change-Id: I2c471b0f72fefa5c316d2025790e0510c6e7eaae
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5302328
    Commit-Queue: Ahmed Moussa <ahmedmoussa@google.com>
    Reviewed-by: Muyao Xu <muyaoxu@google.com>
    Cr-Commit-Position: refs/heads/main@{#1261825}

M       chrome/browser/ui/media_router/media_route_starter.cc

https://chromium-review.googlesource.com/5302328


### dr...@chromium.org (2024-02-16)

[security shepherd] A little late, but a missing origin sounds like a medium severity bug, and based on the age of the code involved in the fix, assuming it reproduces in M121 (though I'm struggling to repro myself)

### ah...@google.com (2024-02-16)

You probably should be able to repro if you disable this flag `chrome://flags/#global-media-controls-cast-start-stop`.

### ia...@gmail.com (2024-02-17)

I have learned from a previous mistake where I failed to provide a comprehensive bug description along with its impact. This oversight required additional time and effort from the VRP panel to understand and address the issue, ultimately impacting the bug bounty reward amount. To avoid such situations in the future, I am now including a thorough description along with the impact, ensuring that the VRP panel can efficiently assess and address the issue without unnecessary efforts on their part.

*Description*
The detected issue concerns an iframe-embedded cross-domain website that does not show the PresenterAPI (Casting) origin in the browser window. A key element of casting functionality is the PresenterAPI, which enables smooth communication and interaction between several web domains. When a website from a different domain is embedded inside an iframe, the browser window fails to deliver the required information about the PresenterAPI's origin, which could lead to issues for both developers and users. They don't know from which origin the screen casting is happening.

**Possible Impact**
The issue of not displaying the origin of the PresenterAPI in a cross-domain iframe scenario poses significant security and functionality challenges:

1. **Security Risks:**
   The inability to determine the PresenterAPI origin raises security concerns, hindering the validation and authorisation of communication between embedded content and casting functionalities. This could result in unauthorised access or data manipulation.
2. **Casting Functionality Disruption:**
   The absence of origin information disrupts the secure communication channel between the web application and casting device. This compromises the casting experience, potentially causing interruptions, authentication issues, and overall usability problems for users attempting to stream content to compatible devices.
3. **User Experience Impairment:**
   End-users utilising casting features on websites with cross-domain content may face a degraded experience, including interrupted sessions and unforeseen problems. Authentication issues further impact the usability of the web application, diminishing user satisfaction.

### am...@google.com (2024-03-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-03-07)

Thank you for the report. It appears that an origin is simply not presented rather there being the potential for incorrect security UI and origin spoofing. I've reduced severity to reflect the low risk and potential security implications to users. Since we were able to make a beneficial change based on your report, the Chrome VRP Panel has decided to extend a $500 thank you reward for this report. Thank you for your efforts and reporting this issue to us.

### ia...@gmail.com (2024-03-07)

Thanks Team :)

### am...@chromium.org (2024-03-09)

I was remiss in fully reducing severity and converting this to a bug the first time around, since we do not consider the absence of an origin to be a security vulnerability the severity.

### pe...@google.com (2024-05-31)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40074906)*
