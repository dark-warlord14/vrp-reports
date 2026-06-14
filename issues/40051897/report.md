# Security: tel: URL scheme reference origin spoof on Android Chrome

| Field | Value |
|-------|-------|
| **Issue ID** | [40051897](https://issues.chromium.org/issues/40051897) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Loader, Mobile, UI>Browser>Navigation |
| **Platforms** | Android, Linux, Windows, ChromeOS |
| **Reporter** | ri...@gmail.com |
| **Assignee** | mt...@chromium.org |
| **Created** | 2020-03-31 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**  

Hello,  

This bug has a similar concept with <https://crbug.com/chromium/1005596>: <https://bugs.chromium.org/p/chromium/issues/detail?id=1005596>  

However, contrast to Mac, Android calls an native phone UI instead of dialog.  

When back to Android Chrome app, normal Contacting Apple web page is loaded, thus the victim would think the number is legit.

**VERSION**  

Chrome Version: 80.0.3987.149  

Operating System: Android 10; SM-N976N Build/QP1A.190711.020

**REPRODUCTION CASE**  

Proof of Concept: <https://lavender204.000webhostapp.com/ChromeExploit/contactspoof.html>

1. The victim opens the page.
2. Click "Contact Apple"
3. Chrome loads normal page, and shows native phone app UI with the number filled in.

<Possible Solutions to Solve the Bug>
1. When user clicks "tel:" link, pop-up warning dialog.
2. Disable location.href script when the link is "tel:" URL scheme.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: 강우진

Thank you for reading my bug report. If you have any questions, feel free to comment down. Have a nice day.

## Attachments

- [contactspoof.html](attachments/contactspoof.html) (text/plain, 511 B)
- [spoof_video.mp4](attachments/spoof_video.mp4) (video/mp4, 2.3 MB)
- [more_than_two.jpg](attachments/more_than_two.jpg) (image/jpeg, 220.2 KB)
- [chrome_spoof_video.mp4](attachments/chrome_spoof_video.mp4) (video/mp4, 1.0 MB)
- [contactspoof_2.html](attachments/contactspoof_2.html) (text/plain, 693 B)
- [Screenshot from 2020-04-07 10-43-49.png](attachments/Screenshot from 2020-04-07 10-43-49.png) (image/png, 54.1 KB)

## Timeline

### ri...@gmail.com (2020-03-31)

It looks that the attached video does not play well, so I will comment YouTube link, thanks.
https://youtu.be/B68B9Qs0fUo

### li...@chromium.org (2020-04-02)

I don't currently have an Android device, so tentatively assigning labels (similar to https://crbug.com/chromium/1005596) and punting over to the Android team to triage this. Would someone be able to help take a look? Thanks!

[Monorail components: Mobile]

### tw...@chromium.org (2020-04-02)

I don't think #1 ("pop-up warning dialog.") is the right solution since this would be an interruption to the normal flow and I'm also not sure what it would say apart from "You're leaving Chrome"... unless we're trying to warn about the specific scenario described here (webpage navigates at the same time we intent out of the app).

#2 Sounds like something we would handle in the Blink layer perhaps? Certainly below the browser UI layer that my team owns (#1 actually sounds out of my wheel house too... but maybe I'm missing something).

fwiw, this is also somewhat of an issue on desktop since click-to-call shows a Chrome popup prompting the user to send the # to their phone (if signed-in/synced). The navigation dismissed the bubble so perhaps less of an issue.


### te...@chromium.org (2020-04-02)

I'm not convinced this is an issue.

mthiesse@ please correct me, but I believe we also add FLAG_ACTIVITY_NEW_TASK for external intents, so you wouldn't be in a situation where you can see the old page at the same time as the phone number.

The attack vector requires switching back to the app while in the phone call, which seems like a very low severity issue.

I can also imagine a legitimate use case of a navigating to a different site after clicking a tel: link (e.g. thank you for calling, here are some things you can do yourself...or something like that).

I'm sending back to livvielin@ to understand the severity justification.


### ri...@gmail.com (2020-04-02)

Hello,
I added a screenshot: When your Android has more than two phone dialer apps, background Chrome page is still loading while an Android dialog "Open With..." keeps showing.
In this case, victim does not need to switch back to see normal page. Is it intended? tedc...@

### li...@chromium.org (2020-04-02)

Fair point, changing to low for now, but we can also consider marking as WontFix if this is a functionality that makes sense to keep around

### ri...@gmail.com (2020-04-03)

Hello,
I found another way to spoof, it is almost same method but a little different.
New tab is open, and the phone call UI is showing up at the new tab which is normal site.
The victim does not need to have more than two phone dialer app nor to switch back to the app to see normal page.
PoC and demo video are attached.
Poc (contactspoof_2.html): https://lavender204.000webhostapp.com/ChromeExploit/contactspoof_2.html
Demo Video(YouTube link): https://youtu.be/X2ncX_9jz_0

I guess applying "Same-Origin Policy" to tel: URL scheme same as javascript: scheme, can be a solution to solve this.
I can't imagine a legitimate use case of "Opening new tab with different origin site and after a few time, open the phone call UI", if you have, please correct me.

Would you please review the security severity for this? Thanks a lot :)
livvielin@ tedc...@

### [Deleted User] (2020-04-03)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-04-03)

[Empty comment from Monorail migration]

### mt...@chromium.org (2020-04-06)

#7 Seems like a real issue to me. I think the bug is that this tel: navigation shouldn't be considered to have a user gesture. If the user clicks something that opens a new window, that should consume the gesture from the original site, and then the new window should only be able to redirect itself to an external URL. If the original page navigates the window to an external URL that second navigation of the window should clear the gesture or something.

cc mustaq for thoughts.

### mu...@chromium.org (2020-04-06)

I completely agree with #10 that it's a real problem.  And it reproduces easily in Linux, and the UI is clearly misleading:

1. Go to any site, say www.example.com.
2. Through devtools console, add the following event listener:
    window.onclick = () => {
      setTimeout(() => location.href="tel:+1800", 1000);
      setTimeout(() => window.open("https://www.google.com"), 900);
    };
3. Click anywhere in the window, wait a second.

What happens: the new tab shows the phone dialog.

It seems href="tel:..." is not blocked by transient user activation, which seems to be a bug to me.  (But surprisingly it still consumes the user activation...if the delays above are switched, the popup fails!)

This looks like a navigation bug to me.  csharrison@: any idea who owns "tel:" URL handling?


### mu...@chromium.org (2020-04-06)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Navigation]

### mu...@chromium.org (2020-04-06)

Can someone with a Windows device confirm if #11 repros on Window or not?

### mt...@chromium.org (2020-04-06)

Well I think this is slightly complicated, as you want to allow the navigation for transient user activation, as a site could want to redirect itself to an external protocol like tel:, right? So this doesn't seem like a tel: specific bug, I think the bug is that navigating a frame from the host doesn't clear the transient activation in the frame that was granted to it by creating the frame.

### mt...@chromium.org (2020-04-06)

To be clearer, what I mean is that the host should only be able to take one gesture-consuming action on the window, like the initial navigation. A second navigation initiated by the host shouldn't have a transient or non-transient gesture unless the host received another gesture.

### mt...@chromium.org (2020-04-06)

Actually, one more thing to clarify here Mustaq. The issue you point out is Desktop-specific, as on Desktop backgrounded pages can launch external protocols. However, that's not the case on Android so you need a more clever setup like https://crbug.com/chromium/1066555#c7 provides.

Desktop UI also tells you where the external protocol was launched from, at least on linux, so the spoof isn't as effective as it says it's coming from the wrong domain.


### ri...@gmail.com (2020-04-07)

Hello,
mustag@: I can confirm https://crbug.com/chromium/1066555#c11 repros on Windows Chrome.

### mu...@chromium.org (2020-04-07)

Navigation is complicated...one of the complication is that _some types_ of navigations don't consume user activation for web compat.  My suggestion was that href="tel:..." should perhaps consume, but the web compat implication is not clear to me.  Finally adding csharrison@ to the bug (I meant to add you in https://crbug.com/chromium/1066555#c11).

mthiesse@: Two things:
- The repro in #7 seems to be launching the phone activity from a background tab (1.5 seconds after apple.com tab opens).  Wondering why you are considering it different from the desktop repro.

- I found the UI in desktop more confusing than in Android...the desktop UI clearly associates the popup with the address bar (see the attached screenshot where www.example.com is barely noticeable).  This it not the case in Android: the phone activity has no link to any of the two tabs.  So I am slightly biased to cover the desktop case here.  Feel free to separate out the desktop bug if you like.


### mu...@chromium.org (2020-04-07)

I can repro the bug in CrOS as well.

### mt...@chromium.org (2020-04-07)

Not sure how it would help to have tel: consume the gesture if the tel: navigation itself is considered to have a gesture, maybe I'm missing something.

Re #7, the phone activity is being launched from the foreground tab - the window open to apple.com is navigated by the host to tel:, so it's the foreground tab that's navigating. Android doesn't allow backgrounded tabs to launch external protocols like tel:, so your sample in #11 doesn't repro on Android.

### ri...@gmail.com (2020-04-14)

Hello,
It looks the bug that I reported also affects to the Chrome Desktop version but works a little different from Android version.
Please tell me if I should make/separate a new issue for the desktop version.
And if you have any questions about this bug, feel free to comment. I hope this will be fixed soon, and I'll try my best to give quality information about this bug.

Thanks.

### ri...@gmail.com (2020-05-09)

Hello,
Is there any other evaluations or fixes about this bug? It's been a long time without any further evaluation or fixes.
Please consider this report if this is evaluated as a security bug.

Thanks.

### oc...@google.com (2020-05-11)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-15)

[Empty comment from Monorail migration]

### mu...@chromium.org (2020-08-25)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### mt...@chromium.org (2020-12-01)

[Empty comment from Monorail migration]

### ct...@chromium.org (2020-12-01)

A similar report was made in https://crbug.com/chromium/1103119. Keeping the Android-related discussion here sounds good.

mthiesse@ can you take this bug? livvielin@ is no longer on Chrome, but I can help from the Security-UX side.

### mt...@chromium.org (2020-12-01)

Just want to call attention to c#7, which might warrant adjusting the priority/severity of this spoof.

### mt...@chromium.org (2020-12-01)

> mthiesse@ can you take this bug? livvielin@ is no longer on Chrome, but I can help from the Security-UX side.

It depends on how we want to solve this issue, I still think this is an issue with gesture tokens and navigation, not with external intent dispatch, which would make mustaq@ a better owner.

### aj...@chromium.org (2020-12-02)

[Empty comment from Monorail migration]

### mt...@chromium.org (2020-12-10)

Passing over to csharrison for questions in c#11 and general thoughts.

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### cs...@chromium.org (2021-01-22)

I think the navigation to the tel: URL in #11 is _not_ expected to be gated on user gesture since normal navigations aren't gated (they just consume). So I don't think this is a navigation bug.

We could make tel: URLs gated by user activation (and maybe we should). To do this would be a web visible breakage and involve the blink process. The first step would be to log some UseCounter of how often tel: navigations take place with no user activation. If it is infrequent this could be an easy fix.

Unfortunately I don't think I can own this as I am quite overloaded.

### mt...@chromium.org (2021-01-22)

To be clear, I don't think navigating to tel: should be gated on user gesture, but launching external apps, including through tel: is already gated on a user gesture. I think the bug here is that the tel: navigation is considered to have a user gesture when it shouldn't have one.

### cs...@chromium.org (2021-01-25)

Ah I see I didn't catch that launching external apps is already gated on user gesture. I think this is governed by the external intents / intercepting navigation throttle?

mthiesse@ how exactly is the user gesture gating implemented for external intents? I see us pulling from two sources:
 - the user gesture bit in the navigation handle
 - the "user gesture carryover" bit that comes from the resource dispatcher

I wonder if one of those pieces has regressed

### mt...@chromium.org (2021-01-25)

We disable PageTransition.LINK without a user gesture opening apps here: https://source.chromium.org/chromium/chromium/src/+/master:components/external_intents/android/java/src/org/chromium/components/external_intents/RedirectHandler.java;drc=ce8d17ff494cf684f35c8ff64cb6bd0947adcf46;l=233

We define having a user gesture for this purpose as either a carryover or regular gesture bit: https://source.chromium.org/chromium/chromium/src/+/master:components/external_intents/android/java/src/org/chromium/components/external_intents/InterceptNavigationDelegateImpl.java;drc=ce8d17ff494cf684f35c8ff64cb6bd0947adcf46;l=128

AFAIK we're required to allow carryover gesture bits because external navigations often go through a site that redirects to the external navigation.

Maybe the ideal solution would be to detect when the navigation originates from a non-visible frame. In https://crbug.com/chromium/1066555#c7 it's the background tab that's re-navigating the foreground window within the gesture timeout, making it look like the window is doing the navigation. If we knew that the navigation originated from the background, we could block external navigation.

### cs...@chromium.org (2021-01-26)

mthiesse I think your proposal to exclude backgrounded navigations is reasonable, but I still think it's worth investigating why the user gesture bit is not sufficient.

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### aj...@google.com (2021-09-17)

Assigning to mthiesse as we like security bugs to have owners. Feel free to assign to someone else, or CC in others who might be able to help with a fix.

### [Deleted User] (2021-09-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### mt...@chromium.org (2023-02-02)

Circling back here...

> mthiesse I think your proposal to exclude backgrounded navigations is reasonable, but I still think it's worth investigating why the user gesture bit is not sufficient.

My previous explanation was bad. The real explanation is that the window.open navigation has a user gesture and so is allowed to redirect to an app. On the Chrome side (AFAIK) we have no way to differentiate between the frame's owner re-navigating the frame vs the frame itself redirecting to an app. We allow pages loaded with a gesture to do client or server redirects to apps, so when the window is re-navigated it looks to the browser like the page is doing a redirect, and we allow the navigation to the app.

The re-navigation doesn't have a user gesture associated with it, so it would be sufficient to somehow let us know that this is a *new* navigation, and not a redirect by the page. Can we get some sort of signal plumbed into the NavigationHandle for this, if one doesn't already exist?

creis can you please triage this?


[Monorail components: Blink>Loader]

### cr...@chromium.org (2023-02-03)

From https://crbug.com/chromium/1066555#c42, it sounds like you're looking for a way to tell if a navigation in the popup was initiated by a different frame (possibly from a different page or origin).  NavigationHandle::GetInitiatorFrameToken() can tell you if a different frame (in any renderer process) initiated the navigation.  It may be empty (e.g., browser-initiated navigations, which is fine), or may point to a frame that has been closed (which is also fine, since that still means it wasn't the current one).  If it's non-empty and doesn't point to the current frame, you can probably block the external navigation.

You can also look at GetInitiatorOrigin(), but I'm not sure you need to.

Hopefully that's enough for you to make progress?  I am not familiar with the external protocol dialog logic or the throttles involved with that.

### mt...@chromium.org (2023-02-03)

[Empty comment from Monorail migration]

### mt...@chromium.org (2023-02-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-02-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/884e6177a3f53141ccc9d8d496766e70164d3de7

commit 884e6177a3f53141ccc9d8d496766e70164d3de7
Author: Michael Thiessen <mthiesse@chromium.org>
Date: Mon Feb 13 17:50:31 2023

Block external navigation for re-navigated windows.

If a page opens a window to a URL, the re-navigates that window, we
should block external navigation to avoid it looking like the URL in
the window triggered the external navigation.

Bug: 1066555
Change-Id: Iafbc7e4e9ebb30b4edcfec9acdd9e0310ace97c5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4219042
Commit-Queue: Michael Thiessen <mthiesse@chromium.org>
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Reviewed-by: Bo Liu <boliu@chromium.org>
Reviewed-by: Yaron Friedman <yfriedman@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1104547}

[modify] https://crrev.com/884e6177a3f53141ccc9d8d496766e70164d3de7/android_webview/java/src/org/chromium/android_webview/AwContents.java
[add] https://crrev.com/884e6177a3f53141ccc9d8d496766e70164d3de7/chrome/test/data/android/url_overriding/renavigate_frame.html
[modify] https://crrev.com/884e6177a3f53141ccc9d8d496766e70164d3de7/components/external_intents/android/java/src/org/chromium/components/external_intents/ExternalIntentsFeatures.java
[modify] https://crrev.com/884e6177a3f53141ccc9d8d496766e70164d3de7/components/navigation_interception/android/java/src/org/chromium/components/navigation_interception/InterceptNavigationDelegate.java
[modify] https://crrev.com/884e6177a3f53141ccc9d8d496766e70164d3de7/chrome/android/java/src/org/chromium/chrome/browser/dom_distiller/ReaderModeManager.java
[modify] https://crrev.com/884e6177a3f53141ccc9d8d496766e70164d3de7/components/external_intents/android/java/src/org/chromium/components/external_intents/ExternalNavigationHandler.java
[modify] https://crrev.com/884e6177a3f53141ccc9d8d496766e70164d3de7/components/external_intents/android/external_intents_features.h
[modify] https://crrev.com/884e6177a3f53141ccc9d8d496766e70164d3de7/components/external_intents/android/external_intents_features.cc
[modify] https://crrev.com/884e6177a3f53141ccc9d8d496766e70164d3de7/chrome/android/javatests/src/org/chromium/chrome/browser/tab/InterceptNavigationDelegateTest.java
[modify] https://crrev.com/884e6177a3f53141ccc9d8d496766e70164d3de7/components/external_intents/android/javatests/src/org/chromium/components/external_intents/ExternalNavigationHandlerTest.java
[modify] https://crrev.com/884e6177a3f53141ccc9d8d496766e70164d3de7/chrome/android/java/src/org/chromium/chrome/browser/compositor/bottombar/OverlayPanelContent.java
[modify] https://crrev.com/884e6177a3f53141ccc9d8d496766e70164d3de7/components/external_intents/android/java/src/org/chromium/components/external_intents/ExternalNavigationParams.java
[modify] https://crrev.com/884e6177a3f53141ccc9d8d496766e70164d3de7/components/navigation_interception/intercept_navigation_delegate.cc
[modify] https://crrev.com/884e6177a3f53141ccc9d8d496766e70164d3de7/chrome/android/javatests/src/org/chromium/chrome/browser/externalnav/UrlOverridingTest.java
[modify] https://crrev.com/884e6177a3f53141ccc9d8d496766e70164d3de7/chrome/android/javatests/src/org/chromium/chrome/browser/contextualsearch/ContextualSearchManagerTest.java
[modify] https://crrev.com/884e6177a3f53141ccc9d8d496766e70164d3de7/components/external_intents/android/java/src/org/chromium/components/external_intents/RedirectHandler.java
[modify] https://crrev.com/884e6177a3f53141ccc9d8d496766e70164d3de7/components/external_intents/android/java/src/org/chromium/components/external_intents/InterceptNavigationDelegateImpl.java


### mt...@chromium.org (2023-02-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-14)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-02-17)

Thank you for this report, 강우진! The VRP Panel had decided to reward you $500 as a thank you for this finding. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-02-18)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-31)

[Empty comment from Monorail migration]

### pg...@google.com (2023-04-04)

[Empty comment from Monorail migration]

### pg...@google.com (2023-04-04)

[Empty comment from Monorail migration]

### mt...@chromium.org (2023-04-20)

This fix caused a regression in M112: https://bugs.chromium.org/p/chromium/issues/detail?id=1433137#c17

I think we'll have to turn it off via the kill switch.

### mt...@chromium.org (2023-04-21)

Re-opening for a second attempt at fixing.

### [Deleted User] (2023-04-22)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-04-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/dc7818c3f538fb7554976368f2a74994b4c1f15f

commit dc7818c3f538fb7554976368f2a74994b4c1f15f
Author: Michael Thiessen <mthiesse@chromium.org>
Date: Mon Apr 24 16:19:42 2023

Fix BlockFrameRenavigations

This kill switch for this was turned off in M112 because server
redirects are considered as having the same InitiatorFrameToken as the
navigation that preceeded them, so we were detecting them as cross-frame
re-navigations even through it's really the frame navigating itself.

This change excludes redirects from being considered as cross-frame
re-navigations and tracks whether something along the redirect chain was
previously considered a re-navigation to avoid client redirects allowing
external navigation after a cross-frame re-navigation.

Bug: 1066555
Change-Id: Ief97ec8d88ef9ec50b1d8dfc393b93db62378e8f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4456971
Reviewed-by: Yaron Friedman <yfriedman@chromium.org>
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Commit-Queue: Michael Thiessen <mthiesse@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1134649}

[modify] https://crrev.com/dc7818c3f538fb7554976368f2a74994b4c1f15f/components/external_intents/android/java/src/org/chromium/components/external_intents/ExternalIntentsFeatures.java
[modify] https://crrev.com/dc7818c3f538fb7554976368f2a74994b4c1f15f/components/external_intents/android/java/src/org/chromium/components/external_intents/ExternalNavigationHandler.java
[modify] https://crrev.com/dc7818c3f538fb7554976368f2a74994b4c1f15f/components/external_intents/android/external_intents_features.cc
[modify] https://crrev.com/dc7818c3f538fb7554976368f2a74994b4c1f15f/chrome/android/javatests/src/org/chromium/chrome/browser/externalnav/UrlOverridingTest.java
[modify] https://crrev.com/dc7818c3f538fb7554976368f2a74994b4c1f15f/components/external_intents/android/java/src/org/chromium/components/external_intents/RedirectHandler.java
[add] https://crrev.com/dc7818c3f538fb7554976368f2a74994b4c1f15f/chrome/test/data/android/url_overriding/navigation_from_window_redirect.html
[add] https://crrev.com/dc7818c3f538fb7554976368f2a74994b4c1f15f/chrome/test/data/android/url_overriding/renavigate_frame_with_redirect.html
[modify] https://crrev.com/dc7818c3f538fb7554976368f2a74994b4c1f15f/components/external_intents/android/java/src/org/chromium/components/external_intents/InterceptNavigationDelegateImpl.java


### mt...@chromium.org (2023-04-26)

Verified on Canary. Requesting merge for #79 to M113. The change is flag guarded and fixes the issue with the previous change that required the kill switch to be flipped.

### [Deleted User] (2023-04-26)

Merge rejected: M113 has already been cut for stable release and this issue is marked as a Pri-2, Pri-3, or Type-Feature.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mt...@chromium.org (2023-04-26)

/shrug probably fine to leave for 114

### yf...@chromium.org (2023-07-25)

I'm going to re-open this and re-disable pending an issue with ads. It might be that they need to update client side but I'd rather mthiesse@ assess that. This is the easiest path forward.

### [Deleted User] (2023-07-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-08-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/41821c987bf153f7de60baaaf2320c228762faae

commit 41821c987bf153f7de60baaaf2320c228762faae
Author: Michael Thiessen <mthiesse@chromium.org>
Date: Mon Aug 14 21:45:54 2023

Fix and re-enable BlockFrameRenavigations

The previous attempt to land this mitigation failed to account for
subframes navigating top frames to external protocols (common in ad
frames).

This reland now restricts this to the case where the initiator frame is
not visible, which is the case when a new window is opened and then
re-navigated by the background tab. This should be safer to land as
there should be no legitimate reason for a tab that isn't visible to
launch an app.

Bug: 1066555, b/294371191
Change-Id: I9c1f5603e3c67242ab94a1ec826e7d85842f712e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4770997
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
Reviewed-by: Yaron Friedman <yfriedman@chromium.org>
Reviewed-by: Richard Coles <torne@chromium.org>
Commit-Queue: Michael Thiessen <mthiesse@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1183352}

[modify] https://crrev.com/41821c987bf153f7de60baaaf2320c228762faae/android_webview/java/src/org/chromium/android_webview/AwContents.java
[modify] https://crrev.com/41821c987bf153f7de60baaaf2320c228762faae/components/navigation_interception/android/java/src/org/chromium/components/navigation_interception/InterceptNavigationDelegate.java
[modify] https://crrev.com/41821c987bf153f7de60baaaf2320c228762faae/components/external_intents/android/java/src/org/chromium/components/external_intents/ExternalIntentsFeatures.java
[modify] https://crrev.com/41821c987bf153f7de60baaaf2320c228762faae/chrome/android/java/src/org/chromium/chrome/browser/dom_distiller/ReaderModeManager.java
[modify] https://crrev.com/41821c987bf153f7de60baaaf2320c228762faae/components/external_intents/android/java/src/org/chromium/components/external_intents/ExternalNavigationHandler.java
[modify] https://crrev.com/41821c987bf153f7de60baaaf2320c228762faae/components/external_intents/android/external_intents_features.cc
[modify] https://crrev.com/41821c987bf153f7de60baaaf2320c228762faae/chrome/android/javatests/src/org/chromium/chrome/browser/tab/InterceptNavigationDelegateTest.java
[modify] https://crrev.com/41821c987bf153f7de60baaaf2320c228762faae/components/external_intents/android/javatests/src/org/chromium/components/external_intents/ExternalNavigationHandlerTest.java
[modify] https://crrev.com/41821c987bf153f7de60baaaf2320c228762faae/chrome/android/java/src/org/chromium/chrome/browser/compositor/bottombar/OverlayPanelContent.java
[modify] https://crrev.com/41821c987bf153f7de60baaaf2320c228762faae/components/external_intents/android/java/src/org/chromium/components/external_intents/ExternalNavigationParams.java
[modify] https://crrev.com/41821c987bf153f7de60baaaf2320c228762faae/components/navigation_interception/intercept_navigation_delegate.cc
[modify] https://crrev.com/41821c987bf153f7de60baaaf2320c228762faae/chrome/android/javatests/src/org/chromium/chrome/browser/externalnav/UrlOverridingTest.java
[modify] https://crrev.com/41821c987bf153f7de60baaaf2320c228762faae/components/external_intents/android/java/src/org/chromium/components/external_intents/RedirectHandler.java
[add] https://crrev.com/41821c987bf153f7de60baaaf2320c228762faae/chrome/test/data/android/url_overriding/subframe_navigation_child_top.html
[modify] https://crrev.com/41821c987bf153f7de60baaaf2320c228762faae/components/external_intents/android/java/src/org/chromium/components/external_intents/InterceptNavigationDelegateImpl.java


### mt...@chromium.org (2023-08-15)

[Empty comment from Monorail migration]

### mt...@chromium.org (2023-08-15)

[Empty comment from Monorail migration]

### mt...@chromium.org (2023-08-15)

[Empty comment from Monorail migration]

### mt...@chromium.org (2023-10-02)

[Empty comment from Monorail migration]

### mt...@chromium.org (2023-10-11)

[Empty comment from Monorail migration]

### mt...@chromium.org (2023-10-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ji...@navercorp.com (2023-11-27)

Does this patch work in android webview?

### mt...@chromium.org (2023-11-27)

I don't believe this was ever broken in WebView, which if I understand correctly defers to the host app to decide whether to launch an app in response to a navigation.

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1066555?no_tracker_redirect=1

[Multiple monorail components: Blink>Loader, Mobile, UI>Browser>Navigation]
[Monorail mergedwith: crbug.com/chromium/1080611, crbug.com/chromium/1120234, crbug.com/chromium/1443158, crbug.com/chromium/1472573, crbug.com/chromium/1488301, crbug.com/chromium/1491492, crbug.com/chromium/1491496]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051897)*
