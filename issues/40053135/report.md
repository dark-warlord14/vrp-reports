# Security: UAF in the DevTools  of the Presentation Cast causes RCE.

| Field | Value |
|-------|-------|
| **Issue ID** | [40053135](https://issues.chromium.org/issues/40053135) |
| **Status** | Accepted |
| **Severity** | Unknown |
| **Priority** | P3 |
| **Component** | Platform>DevTools |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | pb...@chromium.org |
| **Created** | 2020-08-21 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

UAF in the DevTools of the Presentation Cast causes RCE.

**VERSION**  

Chrome Version 84.0.4147.135 (Official Build) (64-bit)  

Operating System: [Windows10 1909]

**REPRODUCTION CASE** :

1. open <http://localhost/presentation.html> with Chrome.exe
2. click and open the cast in the Display 2
3. click right mouse in the Display2 and choose the Inspect. Now you can get the DevTools of "<https://www.google.com>"
4. copy

```
a = document.createElement('a');  
a.href = 'foo'  
a.innerHTML = 'bar'  
document.body.appendChild(a)  
a.click();  

```

to the console and excute it.  

5. the chrome browser crash.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [browser]

## Attachments

- [presentation.html](attachments/presentation.html) (text/plain, 274 B)
- [windbg_crash.log](attachments/windbg_crash.log) (text/plain, 7.8 KB)
- [poc.gif](attachments/poc.gif) (image/gif, 4.7 MB)
- [presentation_UAF_asan.txt](attachments/presentation_UAF_asan.txt) (text/plain, 17.7 KB)
- [presentation_devtools.gif](attachments/presentation_devtools.gif) (image/gif, 4.1 MB)
- [p1.html](attachments/p1.html) (text/plain, 370 B)
- [p2.html](attachments/p2.html) (text/plain, 117 B)
- p2.html (text/plain, 420 B)
- [presentation_poc.gif](attachments/presentation_poc.gif) (image/gif, 3.8 MB)
- presentation.html (text/plain, 359 B)
- [poc.html](attachments/poc.html) (text/plain, 386 B)

## Timeline

### mp...@chromium.org (2020-08-24)

Thanks for the report. mfoltz@ and wolfi@, I'm not sure if the bug here is in DevTools or the Presentation API, can you PTAL?

[Monorail components: Platform>DevTools]

### mp...@chromium.org (2020-08-24)

mfoltz@ on vacation.

### ml...@google.com (2020-08-24)

Assigning to atadres@ for triage given that mfoltz@ is away.

### [Deleted User] (2020-08-25)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-25)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### 0x...@gmail.com (2020-11-13)

Hi, this vulnearability can cause  Sandbox Escape and also exited in the latest chromium version.

See the asan log.

### mp...@chromium.org (2020-11-13)

This can be a sandbox escape? Is there some sequence of IPCs that can be sent from a renderer to cause this?

That would make this bug medium severity since I think it requires DevTools. If you can provide a PoC of these IPCs, or better yet a PoC that doesn't require DevTools, we can upgrade the severity here.

### 0x...@gmail.com (2020-11-14)

I test this case in the latest asan-win32-release_x64-827532 version.
It needn't input any content in the devtools console.
1. Start the presentation frame window.
2. click the Inspect button in the frame window.
3. Wait for a moment 
Then it will triger the UAF.


### 0x...@gmail.com (2020-11-14)

Update the p2.html

Monitor if the user open the DevTools with js.
If the user open the DevTools ,then close the presentation frame window and triger the UAF automatically.

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### 0x...@gmail.com (2021-03-17)

Hi, this issue is a process crash and affects the presentation components~
I submit another poc to reproduce this issue more easily.


### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### 0x...@gmail.com (2021-07-15)

Hi, it is a UAF issue in the browser process. It seems that this issue still exists in the stable version,but it has been fixed in the dev version.

### am...@google.com (2021-07-21)

[Empty comment from Monorail migration]

### ml...@google.com (2021-07-21)

Swapping mfoltz@ and me as I no longer work on this.

### pb...@chromium.org (2021-07-21)

Copying this off an email I just sent:

For me the suspect bits in the free part of this is profile destruction before BrowserView destructs:

    #7 0x7ffbf3118eb1 in ProfileDestroyer::DestroyProfileWhenAppropriate C:\chromium_source_code\chromium\src\chrome\browser\profiles\profile_destroyer.cc:61
    #8 0x7ffbff6d1308 in PresentationReceiverWindowController::~PresentationReceiverWindowController C:\chromium_source_code\chromium\src\chrome\browser\ui\media_router\presentation_receiver_window_controller.cc:56

They're suspect because they seem to end up destroying the Profile before BrowserView::SaveWindowPlacement and BrowserView destructs. BrowserView and a bunch of things inside it expect the Profile to be valid during their lifetime, so this UAF is reasonable to me. I don't know how Profile lifetimes are supposed to be managed.


### mf...@chromium.org (2021-07-21)

I am not sure how/why BrowserView is referencing this particular profile which is owned by the presentation receiver controller.  CCing rhalavati@chromium.org who has fixed some profiles/devtools issues in the past.

### mf...@chromium.org (2021-07-21)

[Empty comment from Monorail migration]

### rh...@chromium.org (2021-07-22)

I have to get deeper to make sure, but this seems very similar to (if not a duplicate of) https://crbug.com/chromium/1120880, which was fixed and merged into M90.

Re #15,
Can you reproduce the issue on M90+ stable?

### mp...@chromium.org (2021-07-22)

For the purposes of the VRP please do not mark this as a duplicate, even though it may not be rewarded under the VRP anyway.

### 0x...@gmail.com (2021-07-23)

Hi, this issue exited in the Chrome stable version 91.0.4472.164.However it seems to be fixed in the latest stable version 92.0.4515.107.
I see some devtools uaf issues in the Chrome release of the stable channel update.However I cannot see the details.
If I submitted earlier than them, can I get the CVE or reward?


### rh...@chromium.org (2021-07-23)

Thank you for the confirmation that the issue is now fixed.

I don't know about the reward program policies, let's wait for them to reply on the bug.

### mp...@chromium.org (2021-07-26)

Normally this needs to be marked as fixed for the VRP to get involved but I'll just loop in adetaylor@ and amyressler@.

### am...@google.com (2021-07-26)

Hi, Matt is correct. Once this issue is marked as fixed, automation will kick off and the 'bot will add the appropriate labels that result in this going into the VRP pipeline for potential reward consideration. I cannot guarantee this will be rewardable due to the need to drop and execute code from within Dev Tools, but the Panel will certainly review it for consideration. 
Now that we are aware that this issue was fixed by the work done on https://crbug.com/chromium/1120880 and the CL for the fix is landed on that issue, you can merge/dupe this bug into that one and I can now manually track this issue to ensure we get it into the workflow for VRP consideration. 

### 0x...@gmail.com (2021-07-26)

It doesn't need drop code to execute in the DevTools. What you only  need to do is just click the right mouse button to open the devtools. I have submitted the new poc in the comment.




### am...@google.com (2021-07-26)

Oh right, thanks for the reminder about the new POC! I was looking at the original report and comparing it to the other issue. We would still fully review it for potential reward regardless, but I appreciate the reminder. :) 

### 0x...@gmail.com (2021-08-03)

Hi, the https://crbug.com/chromium/1175058 is the same with this one . Exactly the same way to reproduce this issue .
And I submitted earlier than https://crbug.com/chromium/1175058.
Can I get the bug bounty or a new CVE?
Thanks~

### 0x...@gmail.com (2021-08-04)

It seems that the fix for https://crbug.com/chromium/1175058 also fixed this issue.

### 0x...@gmail.com (2021-08-04)

See the new submittion which I have submitted that needn't access to devtool on Sat, Nov 14, 2020  
https://bugs.chromium.org/p/chromium/issues/detail?id=1120238#c9 .


### 0x...@gmail.com (2021-08-05)

I continue to observe the presentation function for a period of time.
When I first submitted this vulnerability, it seems that the presentation frame page would keep the page unchanged when you click on the navagation.Some months later when you click on the navigation,presentation frame page will be closed automatically(https://crbug.com/chromium/1175085).So In the initial report, I try to input the "location.href='https://google.com'" in the Devtools console instead of the presentation frame page.That's why I need access to the Devtools and the https://crbug.com/chromium/1175085 need not. Obviously the presentation frame has changed the method to deal with the navigation.
(My initial report is almost the same as the https://crbug.com/chromium/1175085).

Days later I wanted to found a easier way to trigger this vulnerability. I found that if only the Devtools is opened and then you close the presentation frame, the UAF will be triggered.In fact there are a few method to close the presentation frame such as window.close(),task manager,presentationRequest.start() in tha main page and so on.
I also thought about submitting a new report,but I thought it was the same to add the new poc in the comment area directly.

I continued to submit some new comments, just hoped this issue would be paid attention to.

And I understand that due to the initial reporting security severity is low and the new comment was ignored.


### pb...@chromium.org (2021-08-05)

Sorry that this got missed. Because the bug didn't get marked as fixed the rest of the VRP didn't kick in automatically.

I think crrev.com/c/2772983 is a likely fix for this, and per rhalavati@ suspecting this as fixed in #21 and you confirming in #23 I think it's safe to say that this is Fixed. I'll mark myself as owner in case this needs merging to any channels and we can let it get to the VRP for potential reward consideration.

### [Deleted User] (2021-08-05)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-08-05)

credit on release notes with CVE ID updated here: https://chromereleases.googleblog.com/2021/04/stable-channel-update-for-desktop_26.html

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-08-11)

Congratulations, the VRP Panel has decided to award you $10,000 for this report! Thank you for this report, the updates, and your patience as we worked through getting this addressed.  

### am...@chromium.org (2021-08-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-08-11)

merging into later submitted duplicate now that this issue has been reviewed by the VRP Panel and appropriately credited; fix for this issue landed on https://crbug.com/chromium/1175058

### am...@google.com (2021-08-13)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-11-12)

This issue was migrated from crbug.com/chromium/1120238?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedinto: crbug.com/chromium/1175058]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053135)*
