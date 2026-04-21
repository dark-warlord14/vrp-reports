# Android Chrome Incognito Mode Leaving Alert Dialog Box Origin Confusion

| Field | Value |
|-------|-------|
| **Issue ID** | [352516283](https://issues.chromium.org/issues/352516283) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Mobile>Intents, UI>Browser>Navigation |
| **Platforms** | Android |
| **Chrome Version** | 126.0.6478.122 |
| **Reporter** | sh...@gmail.com |
| **Assignee** | mt...@chromium.org |
| **Created** | 2024-07-11 |
| **Bounty** | $2,000.00 |

## Description

# Steps to reproduce the problem

1. Open Android Chrome and inside Incognito Mode visit - <https://poorly-compiler.000webhostapp.com/inpoc.html>
2. Click on the ‘Home’ icon of chrome
3. Notice that the address bar is blank and a leaving alert dialog box is prompted on homepage.

# Problem Description

Incognito Mode Leaving Alert Dialog Box can be triggered on the Chrome's homepage to trick user's into leaving the Incognito Mode.

When any user will try to go on homepage by clicking on the home icon from attacker's webpage, the popup to Leave Incognito Mode will appear on Chrome's homepage which will be confusing to users as the address bar is totally blank in that case and the user's will think Chrome is asking to exit Incognito and the user's may click on Leave button and end up executing any malicious INTENT Redirects.

# Summary

Android Chrome Incognito Mode Leaving Alert Dialog Box Origin Confusion

# Custom Questions

#### Reporter credit:

Mohit Raj (shadow2639)

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A

## Attachments

- [Screenrecorder-2024-07-11-23-51-39-347_756x1638.mp4](attachments/Screenrecorder-2024-07-11-23-51-39-347_756x1638.mp4) (video/mp4, 6.1 MB)
- [inpoc.html](attachments/inpoc.html) (text/html, 232 B)
- [Screenrecorder-2024-07-13-15-44-37-420.mp4](attachments/Screenrecorder-2024-07-13-15-44-37-420.mp4) (video/mp4, 4.4 MB)

## Timeline

### fl...@google.com (2024-07-12)

I've verified that I can reproduce this on Android Chrome 126.

I'm assigning to mthiesse@ since you seem to have worked on issues of this sort before. Let me know if you're the right person.

Out of an abundance of caution, I have assigned a provisional severity of Low, seeing as this is a somewhat niche thing requiring a decent amount of human interaction.

However, mthiesse@, I'd be curious for your feedback, as I think this might not be a security bug?

The fact that the Home button click can wind up redirecting to somewhere else is pretty weird for me, but this is my first time learning about intents, so I'm wondering if this is expected behavior or not. (I thought the address bar area + stuff around it wasn't supposed to be touched by websites but I don't know the UX expectations there.)

The rest of this report doesn't seem of a security concern, though. If it were e.g. just a link on the page, instead of the Home button, then, yeah, it's a little confusing to be leaving Incognito... but it does warn you're about to go to some other site right there in the Incognito window, so.

Anyway, let me know, mthiesse@, and feel free to change the type from Vulnerability to Bug if this isn't a security concern in your mind.

### mt...@chromium.org (2024-07-12)

I think we should consider this a duplicate of b/40075907. The repro steps are different but the cause is the same. We should probably cancel the incognito dialog when the tab changes.

### sh...@gmail.com (2024-07-13)

Hi team, 
I have updated the PoC and this time the user just have to click on the webpage for this exploit to work. No Home button click is required. Please let me know if it’s still considered duplicate.

PoC Link - https://poorly-compiler.000webhostapp.com/update.html

### mt...@chromium.org (2024-07-15)

I don't think that changes anything. The bug is the same, tab switches without cancelling the dialog.

Also, that only works if the previous page was the new incognito window (which incidentally means a user would have to manually type or copy/paste the URL to get there).

### mt...@chromium.org (2024-07-16)

Actually, this is a separate issue, didn't realize the NTP wasn't actually changing the tab. This happens because the NTP URL gets filtered before our external navigation code runs so it doesn't see the navigation or something. Looking into it.

### pe...@google.com (2024-07-16)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### mt...@chromium.org (2024-07-17)

Nasko or Rakina (feel free to redirect) - I could use some help here trying to understand how Navigation works and how I might fix this bug.

The page in question navigates with history.back() to the NTP, then navigates to an external URL. The navigation to the NTP completes without canceling or preventing the subsequent navigation so if the external navigation causes any dialogs to show, they show over top of the NTP. At the time we show the dialog the NTP navigation isn't yet committed, so the External Navigation code doesn't see the current URL being the NTP yet. I'm not sure what signal I might use to block the external navigation in this case (maybe track that a previous navigation was started but not yet finished, so I should block external navigation on any new navigations? That might break things...). Any fixes in External Navigation code kind of feel like a hack - this seems like a bug that should instead be fixed in Navigation code.

What I'm seeing is that as soon as the navigation is Ready To Commit, the Frame Tree Node doesn't own the NavigationRequest anymore and any new navigations won't cancel the Ready To Commit navigation and they'll essentially race? I think this could also cause the dialog to show up over an arbitrary other URL instead of the NTP, but it's easier to get it to show over the NTP as the NTP is always Ready To Commit immediately so the race is easy to create. Why do we even allow multiple main frame navigations to race against each other like this? Is it intentional? If one navigation is already Ready To Commit, should we ignore future navigations from the frame that's about to go away?

### ra...@chromium.org (2024-07-26)

Sorry for the late response. What signals does the external navigation detector use to show the dialog? Does it make sense to dismiss the dialog and automatically cancel the navigation when another navigation committed (so, listening to DidFinishNavigation)?

Navigations that are already past ReadyToCommit shouldn't be canceled because at that point we're already.. "committed" to the navigation. If the navigation changes RenderFrameHost, it would also lead to crashes in the renderer (see also <https://docs.google.com/document/d/1VNmvEVuaiNH3ypt6YfrYPsJJp8okCTYjooekarOiWN8/edit#heading=h.go7cmxgiohp7>). So I think we should try to think how to handle the external navigation & dialog with concurrent navigations.

### mt...@chromium.org (2024-07-29)

If we're already committed to the navigation, should the same page even be allowed to commit another navigation after that? Maybe only if a new user gesture has come in since the last navigation was kicked off? Otherwise we basically guarantee weird races will happen.

We can work around by listening to DidFinishNavigation and cancelling if it's a different navigation from the one that caused the dialog to appear, but I'm still worried about this as a security bug factory.

### mt...@chromium.org (2024-08-02)

ping Rakina/Nasko

### ra...@chromium.org (2024-08-05)

Sorry, forgot to reply! The general concern of changing navigations is the risk that there's going to be some random site that depends on the old behavior by e.g. doing a navigation soon after an earlier navigation, and hoping that the newer navigation will win (cancels the old navigation) or at least still be committed in the end. These kind of bugs usually don't manifest until we're in Stable and might not happen reliably, making it hard to pin them down to the behavior change. So we need to be very careful if we want to do that change.

I think generally dialogs should be listening to navigations/primary page changes, since it's important for it to be dismissed timely and is consistent with what the currently shown content is, so I think it's best if we do the change on the external navigation detector code, at least for now.

### ap...@google.com (2024-08-09)

Project: chromium/src
Branch: main

commit 63cadda6b9e2283708c187ed5bb3c35e86f0c6c2
Author: Michael Thiessen <mthiesse@chromium.org>
Date:   Fri Aug 09 14:24:53 2024

    Cancel incognito dialog when another navigation starts/finishes
    
    Navigation is racy and can result in the following sequence:
    Navigation A starts
    Navigation B starts and is canceled by external nav
    Navigation A finishes
    
    This can confuse the External Navigation and show dialogs from B for A.
    Messages handles this correctly, but the Incognito dialog does not, so
    we should cancel it when a new navigation is started or finished.
    
    Bug: 352516283
    Change-Id: Idfc4f77f12025780b72e6c70484b43cd19d5e94d
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5770032
    Commit-Queue: Michael Thiessen <mthiesse@chromium.org>
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Reviewed-by: Yaron Friedman <yfriedman@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1339626}

M       components/external_intents/android/BUILD.gn
M       components/external_intents/android/java/src/org/chromium/components/external_intents/ExternalNavigationHandler.java
M       components/external_intents/android/java/src/org/chromium/components/external_intents/ExternalNavigationParams.java
M       components/external_intents/android/java/src/org/chromium/components/external_intents/InterceptNavigationDelegateImpl.java
M       components/external_intents/android/javatests/src/org/chromium/components/external_intents/ExternalNavigationHandlerTest.java

https://chromium-review.googlesource.com/5770032


### am...@chromium.org (2024-09-12)

Thank you for the report. We don not consider this a security boundary. The `leaving incognito` alert isn't our external intent protection mechanism. As such, we are unable to extend a Chrome VRP reward for this report.

### sp...@google.com (2024-09-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
report of lower impact web platform privilege escalation / security UI bug


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-09-19)

Congratulations Mohit! Apologies for the incorrect assessment the first time around. It was brought to our attention that in this case, this dialog is in place of a chooser dialog that would be a security boundary, so this dialog should actually be considered a security boundary.
Thank you for your efforts and reporting this issue to us!

### sh...@gmail.com (2024-09-19)

Thank you very much team for the bounty decision.

### pe...@google.com (2024-11-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of lower impact web platform privilege escalation / security UI bug

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/352516283)*
