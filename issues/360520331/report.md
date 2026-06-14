# Clickjacking Exploit Leading to Unintentional Credit Card Submission in Chrome iOS

| Field | Value |
|-------|-------|
| **Issue ID** | [360520331](https://issues.chromium.org/issues/360520331) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Autofill>Payments |
| **Platforms** | Android, iOS |
| **Chrome Version** | 127.0.6533.103 |
| **Reporter** | ia...@gmail.com |
| **Assignee** | vi...@google.com |
| **Created** | 2024-08-18 |
| **Bounty** | $1,000.00 |

## Description

Edit by smcgruer@:

After an investigation on Clank by darwinyang@, it seems that we already have [input protection for touch to fill](https://crsrc.org/c/chrome/browser/touch_to_fill/autofill/android/internal/java/src/org/chromium/chrome/browser/touch_to_fill/payments/TouchToFillPaymentMethodMediator.java;l=275;drc=6756f16ee57221562256ea15296217f9da09878b). The timeout is 500ms, and according to documentation this is the expected timeout even including the animation time for the bottomsheet to appear. As such, Clank appears to be WAI for Chrome's views on click-jacking.

iOS still needs investigation and possibly to be addressed.

---

# Steps to reproduce the problem

*Tested On*
Google Pixel 7A, Android OS 14, Security Update August 5th 2024
Chrome Android Version 127.0.6533.103
*ReProduction Steps*

Before going ahead, please ensure that you have a Credit Card already set on Chrome > Settings > Payment Method

1. Host attached card.html file or use ready available POC at <https://g00gle.in/card.html>
2. Continue click on Submit button and your card data will get posted to cross origin website and preview back.
3. Once the

# Problem Description

The design of the web page requires the user to click multiple times to activate the credit card input fields. This behavior can be exploited by an attacker to trick the user into repeatedly clicking, potentially leading them to unknowingly submit saved credit card form data. This could be leveraged to automatically submit sensitive information without the user's explicit intent, posing a risk of unauthorized data submission

# Summary

Clickjacking Exploit Leading to Unintentional Credit Card Submission in Chrome Android

# Custom Questions

#### Reporter credit:

Narendra Bhati - Manager of Cyber Security at Suma Soft Pvt. Ltd - Pune (India)

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A

## Attachments

- [card.html](attachments/card.html) (text/html, 3.2 KB)
- [Chrome_AndroidPOC.mp4](attachments/Chrome_AndroidPOC.mp4) (video/mp4, 17.6 MB)
- [input-protection-3-seconds.mp4](attachments/input-protection-3-seconds.mp4) (video/mp4, 3.0 MB)

## Timeline

### xi...@chromium.org (2024-08-19)

Thanks for the report. I'm able to reproduce. +nburris, could you check if your fix on <https://crbug.com/40062366> will resolve this issue here? Triaging the same way as <https://crbug.com/40062366> (setting the OS field to Android only since this report focuses on Android). Feel free to dedupe.

### ia...@gmail.com (2024-08-19)

@xi & @pe - Please update the OS label for Chrome iOS as well, I tried and it working on iOS also.

### sm...@chromium.org (2024-08-19)

From the reproduction video, this is clickjacking on the Autofill bottom sheet, and has nothing to do with Payment Request or [issue 40062366](https://issues.chromium.org/issues/40062366) . Moving the component, and cc-ing Jan to check - Jan, do you know if we have done any anti-clicking work on the autofill filling bottom sheet on Android? (I think you were looking at similar clickjacking bugs recently-ish?)

### pe...@google.com (2024-08-19)

Setting milestone because of s2 severity.

### pe...@google.com (2024-08-19)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ia...@gmail.com (2024-08-19)

Dear Team, You might have missed out but this issue is also reproducible on chrome iOS.

### xi...@chromium.org (2024-08-19)

Stephen, thanks for re-triaging. Reporter, thanks for calling out that iOS may have the same issue. I can reproduce on iOS too.

### ia...@gmail.com (2024-08-19)

Team, just for my information. Can you please confirm it’s not a duplicate of existing report! :)

### jk...@google.com (2024-08-20)

Stephen,

We've got click jacking protections in the keyboard accessory, where we enforce that a suggestion has been seen for at least 500ms. AFAIK we don't have that in the bottomsheets. Happy to provide pointers / review CLs to add it there, too.

### sm...@chromium.org (2024-08-20)

Thanks Jan - then I think there's pretty obvious click-jacking attack against the filling bottom sheets on both Android and iOS. The mitigation should hopefully be straight-forward, we've done similar work for SPC on Android before (<https://chromium-review.googlesource.com/c/chromium/src/+/4294488>).

I'll working on finding someone on my team with cycles to tackle this. Can security confirm that this should be treated as a P1 security vulnerability?

(cc Tommy for fyi)

### ia...@gmail.com (2024-08-21)

@Sm / @Team - I wanted to mention one more thing: In the provided POC, the input fields are hidden, meaning they aren’t visible in the UI. However, Chrome still prompts to autofill credit card information. Do you think this is good approach? I suggest that if the fields are hidden, Chrome should not prompt for autofill, especially when it involves payment information like credit card details.

### tm...@google.com (2024-08-21)

So just to make sure I understand the root cause, can anyone confirm that this is what's happening:

1. User taps on (what appears to be) the continue button
2. User's tap is captured by an invisible (zero-opacity) input field that's covering the continue button
3. The invisible field is focused
4. The credit card bottom sheet appears, with the continue button at the same coordinates as the button from (1)

(2) and (3) are the parts I'm least confident I understand just from looking at the attached source, so let me know if I missed something there.

Then the proposed mitigation would be for the continue button in the bottom sheet to start disabled and then become enabled on a 500ms timer?

### ia...@gmail.com (2024-08-22)

@tm - I've reported this bug, and I agree with your what you mentioned. Any else may share their feedback as well on this!

### jk...@google.com (2024-08-22)

Narendra, just a note on the suggestion re visibility: Yes, ideally we do not trigger on visible fields. In practice, reliably judging visibility is near impossible. A few sample questions that are hard to answer in full generality: What's a degree of transparency that counts as visible? What if the colors of the field and the background match? What if it's overlayed by an element of higher z-level? What's the minimum size that still counts as visible?

### ia...@gmail.com (2024-08-22)

@jk - Understood. Thanks.

### sm...@chromium.org (2024-08-23)

tmartino@ - your understanding is correct! Having a delay before accepting input on a newly visible UX is fairly standard practice in Chrome as far as I know.

Desktop has a standard class for it (ui/views/input\_event\_activation\_protector.h) which not only waits ~500ms (platform dependent) but also tries to de-bounce rapid clicking - as long as the user is spamming, the 500ms timeout doesn't start.

Android doesn't have a centralized class that I know of, but we built components/payments/content/android/java/src/org/chromium/components/payments/InputProtector.java for PaymentRequest/SPC, and it could perhaps be generalized now that we want to do things in Autofill too.

iOS, I have no idea about the state of the world today in terms of other UIs and their protection from click-jacking.

### jk...@google.com (2024-08-23)

FWIW, at least on Desktop, the timing check is not reliable - see [this presentation](https://docs.google.com/presentation/d/1zL07Jcw7Ky0_PgFcTaRzrQNHx9w8B7oufqdeD0nwPtw/edit?resourcekey=0-XbxXVVaUUJNI5drf3ljwEQ#slide=id.g2c0e815f2c3_0_117) and [this doc](https://docs.google.com/document/d/1zRA_f56WZph4uF79RONccwgmvliK2ytWU5vCaj780VE/edit?tab=t.0#heading=h.xzcjimurk42y). I haven't seen an exploit for bottomsheets yet that manages to spoof the timing information.

[This class](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/autofill/next_idle_barrier.h;l=14?q=nextidle&sq=&ss=chromium%2Fchromium%2Fsrc) can be used to prevent timing spoofing. Happy to talk more elsewhere.

### sm...@chromium.org (2024-08-23)

Jan - that's really cool, thanks! Have you spoken to the //views folks about integrating NextIdleBarrier into the Desktop input protector by default?

### jk...@google.com (2024-08-23)

They (in particular kerenzhu@) were involved in the original troubleshooting and problem solving on how to address the issue, but no, we've not discussed integrating it into the protector.

It might be worth a discussion.

### ke...@google.com (2024-08-23)

NextIdleBarrier is new to me. It looks to me like a simple and effective tool. Jan, is NextIdleBarrier fixing autofill attacks as expected? Otherwise, I don't see a reason why it can't be used more broadly.

### sm...@chromium.org (2024-08-23)

Not withstanding the nice conversation on making clickjacking even harder on desktop; assigning this *Clank* and *iOS* bug to Darwin as the incoming Chrome Payments on-call.

Darwin - will you have cycles in your on-call rotation to tackle this bug at least on Clank? See comments #1 and #11 for details. This issue definitely skips the priority on other product excellence work this quarter (and should also be considered as progress on that OKR).

### da...@google.com (2024-08-23)

I can definitely take a look into this next week.

### jk...@google.com (2024-08-25)

Keren, yes, `NextIdleBarrier` turned out to be the solution to the timing spoofing issues that you could get on a congested UI thread - you helped problem solve the issues with those at some point last year. :)

### da...@google.com (2024-08-28)

After an investigation on Clank, it seems that we already have [input protection for touch to fill](https://crsrc.org/c/chrome/browser/touch_to_fill/autofill/android/internal/java/src/org/chromium/chrome/browser/touch_to_fill/payments/TouchToFillPaymentMethodMediator.java;l=275;drc=6756f16ee57221562256ea15296217f9da09878b). I created a build that just extended [the threshold to 3 seconds](https://crsrc.org/c/components/payments/content/android/java/src/org/chromium/components/payments/InputProtector.java;l=15;drc=692118410481affde547c276fdcdc4313688a7c4) and it seems to be working as expected (see attached video).

Should we consider increasing the 500ms threshold?

### ia...@gmail.com (2024-08-29)

In my opinion, the current threshold is sufficient for a user to observe and verify the information being filled in.

### da...@google.com (2024-08-29)

Setting back to new for someone else to pickup in a future oncall rotation. Note that bling still requires investigation (and a fix).

### vi...@google.com (2024-08-30)

iiuc we just need to add a latency of 500ms before accepting user inputs on the sheet

I guess this could specifically target the fill button which is the one that can leak the info, where other interactions are about dismissing the sheet or showing the keyboard

### sm...@chromium.org (2024-08-30)

vincb@ - that's correct; the minimal protection is to wait at least 500ms before accepting user input on the fill button, from when the sheet first begins to show (to give the user a chance to visually process that something is happening). Desktop has some additional improvements over this to avoid 'spam clicking' and load-attacks, but they're not minimally required here.

Are you interested in driving this work for iOS?

### vi...@google.com (2024-08-30)

I can try, doesn't seem that hard

### vi...@google.com (2024-09-03)

Do we disable the button visually?, since it is a short period of time, I was considering just ignoring the filling action during the buffer period, without showing the button as disabled

What do we do on Android?

### vi...@google.com (2024-09-03)

If we disable => enable the view, this may look like flickering, so just ignoring the action seems better

### sm...@chromium.org (2024-09-03)

On Android we simply ignore inputs during the delay, we do not disable the button.

### jk...@google.com (2024-09-04)

Same on Desktop - there's no visual indicator in the UI, we just ignore the event.

### vi...@google.com (2024-09-04)

Do we have something similar for passwords?

### jk...@google.com (2024-09-04)

On Desktop, we do (because we have it for everything in the popup), but I don't think it's necessarily needed on mobile: You can only fill the information for the origin of the attacker anyway (% affiliations, but they should be very hard to tamper with).

### vi...@google.com (2024-09-04)

Good point

### ap...@google.com (2024-09-17)

Project: chromium/src
Branch: main

commit a26cb5368c44f879381ac70d1b4ee7a78ee5ed2d
Author: vincb <vincb@google.com>
Date:   Tue Sep 17 17:43:12 2024

    [ios] Delay before accepting suggestion from the payments bottom sheet
    
    Add a delay 500ms before accepting suggestions from the payments
    bottom sheet.
    
    Any attempt made before the delay is reached will be ignored.
    
    The state of the UI isn't changed which aligns with the approach
    used on Android.
    
    Change-Id: I0c87e3c1b4dc8263cbc3aa6f1b65c2b89a95ea86
    Bug: 360520331
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5836985
    Reviewed-by: Sebastien Seguin-Gagnon <sebsg@chromium.org>
    Commit-Queue: Vincent Boisselle <vincb@google.com>
    Cr-Commit-Position: refs/heads/main@{#1356588}

M       ios/chrome/browser/autofill/ui_bundled/authentication/card_unmask_authentication_egtest.mm
M       ios/chrome/browser/autofill/ui_bundled/authentication/otp_input_dialog_egtest.mm
M       ios/chrome/browser/autofill/ui_bundled/bottom_sheet/payments_suggestion_bottom_sheet_consumer.h
M       ios/chrome/browser/autofill/ui_bundled/bottom_sheet/payments_suggestion_bottom_sheet_delegate.h
M       ios/chrome/browser/autofill/ui_bundled/bottom_sheet/payments_suggestion_bottom_sheet_egtest.mm
M       ios/chrome/browser/autofill/ui_bundled/bottom_sheet/payments_suggestion_bottom_sheet_mediator.mm
M       ios/chrome/browser/autofill/ui_bundled/bottom_sheet/payments_suggestion_bottom_sheet_mediator_unittest.mm
M       ios/chrome/browser/autofill/ui_bundled/bottom_sheet/payments_suggestion_bottom_sheet_view_controller.mm
M       tools/metrics/histograms/metadata/ios/histograms.xml

https://chromium-review.googlesource.com/5836985


### ia...@gmail.com (2024-09-23)

Dear Team,

Thanks for fixing out this, can we conclude/close this report if the issues is fixed!

### ia...@gmail.com (2024-09-25)

Dear Team,

Just a reminder! Can we conclude/close this report if the issues is fixed!

### sp...@google.com (2024-10-03)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact information disclosure achieved through click-jacking


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-10-03)

Congratulations Narendra! Thank you for your efforts and reporting this issue to us.

### pe...@google.com (2025-01-02)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/360520331)*
