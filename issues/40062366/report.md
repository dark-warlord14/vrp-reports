# Security: PaymentRequest dialog susceptible to clickjacking

| Field | Value |
|-------|-------|
| **Issue ID** | [40062366](https://issues.chromium.org/issues/40062366) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Payments |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | np...@chromium.org |
| **Created** | 2022-12-24 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The "Continue" button of a payment dialog can be clickjacked to reveal the saved address, email and phone number.

**VERSION**  

Chrome Version: 108.0.5359.125 + stable  

Operating System: Windows 11

**REPRODUCTION CASE**

1. python3 -m http.server 9000
2. <http://localhost:9000/poc.html>
3. Double-click the button on the page

Relevant info from the docs about possible mitigations (docs/security/security-considerations-for-browser-ui.md):

> # Introduce a short delay before the UI's call-to-action activates
> 
> If multiple clicks/gestures aren't feasible, consider introducing a short delay between when the browser UI is shown and the call-to-action activates. For example, if the user must click a button to grant a permission, introduce a delay before the button becomes active once the permission prompt is shown. Three seconds is typically considered a delay that is long enough to let the user notice that some security-sensitive browser UI is showing without being too disruptive to the typical user experience.

**CREDIT INFORMATION**  

Reporter credit: Thomas Orlita

## Attachments

- [app.js](attachments/app.js) (text/plain, 215 B)
- [manifest.json](attachments/manifest.json) (text/plain, 384 B)
- [payment-manifest.json](attachments/payment-manifest.json) (text/plain, 151 B)
- [poc.html](attachments/poc.html) (text/plain, 1.3 KB)
- [poc.webm](attachments/poc.webm) (video/webm, 899.3 KB)
- [Screen Recording 2023-01-16 at 10.33.18 AM.mov](attachments/Screen Recording 2023-01-16 at 10.33.18 AM.mov) (video/quicktime, 1.9 MB)

## Timeline

### [Deleted User] (2022-12-24)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-12-24)

Thanks for the report. I'm able to reproduce. It seems that a second confirmation dialog is needed to avoid such clickjacking attack. +smcgruer@, could you help triage the issue? Thanks!

[Monorail components: Blink>Payments]

### xi...@chromium.org (2022-12-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-25)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-25)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sm...@google.com (2022-12-28)

This would be fixed by our long term plan to remove shipping/contact info from the browser sheet, as well as being partially addressed by our plan to enforce a minimal show time for payment apps.

In the meantime, we should add some anti-clickjacking protection. We won't introduce a new dialog, but we should adopt the existing Views infrastructure for deduping double clicks on the continue button (I'll dig it up later and link it in a comment). We probably also need to do the same on Android for double tap.

It's unclear to me what the right priority is for this bug, given that click jacking was not previously raised in the security model when this feature launched years ago. For now, leaving as P1 and assigned to me to look at in Q1 - but Rouslan or Nick, if you feel inspired to tackle this in a quicker timeframe feel free to takeover the bug.

### [Deleted User] (2023-01-07)

smcgruer: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sm...@chromium.org (2023-01-09)

I have a WIP patch for this -  https://chromium-review.googlesource.com/c/chromium/src/+/4143819

As above, not convinced it should be Severity-Medium given its for newly introduced UX design guidance, but we should have it fixed in the coming few weeks anyway :)

### ro...@google.com (2023-01-13)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-01-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/839bd5909b7ef0b698e1c386dc9ea3eb07c16121

commit 839bd5909b7ef0b698e1c386dc9ea3eb07c16121
Author: Stephen McGruer <smcgruer@chromium.org>
Date: Fri Jan 13 18:50:39 2023

[PaymentRequest] Avoid accidental clicks on the [Continue] button

This CL puts the primary button action for the main browser sheet
behind a views::InputEventActivationProtector, which will ignore any
click that occurs within 500ms of the view being created. Only the
initial creation is measured and not any later visibility change, as
any later show/hide of the view requires the user to have navigated
to a sub-view - and thus they should be aware that the sheet is present.

Bug: 1403493
Change-Id: I55147100f55da85de0c05c98c4c5d8172c122297
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4143819
Reviewed-by: Keren Zhu <kerenzhu@chromium.org>
Commit-Queue: Stephen McGruer <smcgruer@chromium.org>
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1092524}

[modify] https://crrev.com/839bd5909b7ef0b698e1c386dc9ea3eb07c16121/chrome/browser/ui/views/payments/payment_request_browsertest_base.h
[modify] https://crrev.com/839bd5909b7ef0b698e1c386dc9ea3eb07c16121/chrome/browser/ui/views/payments/payment_request_browsertest_base.cc
[add] https://crrev.com/839bd5909b7ef0b698e1c386dc9ea3eb07c16121/ui/views/test/mock_input_event_activation_protector.cc
[modify] https://crrev.com/839bd5909b7ef0b698e1c386dc9ea3eb07c16121/chrome/test/payments/payment_request_test_controller_desktop.cc
[modify] https://crrev.com/839bd5909b7ef0b698e1c386dc9ea3eb07c16121/ui/views/BUILD.gn
[modify] https://crrev.com/839bd5909b7ef0b698e1c386dc9ea3eb07c16121/chrome/browser/ui/views/payments/payment_sheet_view_controller_browsertest.cc
[modify] https://crrev.com/839bd5909b7ef0b698e1c386dc9ea3eb07c16121/ui/views/input_event_activation_protector.h
[modify] https://crrev.com/839bd5909b7ef0b698e1c386dc9ea3eb07c16121/chrome/browser/ui/views/payments/payment_sheet_view_controller.h
[modify] https://crrev.com/839bd5909b7ef0b698e1c386dc9ea3eb07c16121/chrome/browser/ui/views/payments/payment_request_sheet_controller.cc
[modify] https://crrev.com/839bd5909b7ef0b698e1c386dc9ea3eb07c16121/chrome/browser/ui/views/payments/payment_sheet_view_controller.cc
[modify] https://crrev.com/839bd5909b7ef0b698e1c386dc9ea3eb07c16121/components/payments/content/payment_request.cc
[modify] https://crrev.com/839bd5909b7ef0b698e1c386dc9ea3eb07c16121/chrome/browser/ui/views/payments/payment_request_sheet_controller.h
[add] https://crrev.com/839bd5909b7ef0b698e1c386dc9ea3eb07c16121/ui/views/test/mock_input_event_activation_protector.h
[modify] https://crrev.com/839bd5909b7ef0b698e1c386dc9ea3eb07c16121/components/payments/content/payment_request.h


### sm...@chromium.org (2023-01-16)

This should be fixed as of Chrome 111.0.5538.0; we now de-dupe double-clicks using the same infrastructure as other Views. See attached screencast, where fast-paced clicking is ignored until the user take a pause.

### [Deleted User] (2023-01-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-16)

[Empty comment from Monorail migration]

### sm...@chromium.org (2023-01-24)

Reopening as we have realized that Android may also be vulnerable. Investigating now.

### sm...@chromium.org (2023-01-24)

Confirmed that it sort-of reproduces on Android. The UI animates in, so you cannot immediately double-tap to cause the clickjacking. However if you keep tapping it will register on the third or fourth tap, so I think that's bad enough that I'll look at mitigations.

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### sm...@chromium.org (2023-03-02)

Nick will be fixing the Android side. Thanks Nick!

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### np...@google.com (2023-04-13)

[Empty comment from Monorail migration]

### np...@google.com (2023-04-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### rs...@chromium.org (2023-08-11)

nburris: Is there an ETA for the Android fix, or an (internal) reference that can be tracked here?

### np...@google.com (2023-08-16)

Yes, I've got a fix in progress targeting M118.

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-10-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f7c6ff28c4bf829d5337a8714108f9ef47e2a5be

commit f7c6ff28c4bf829d5337a8714108f9ef47e2a5be
Author: Nick Burris <nburris@chromium.org>
Date: Wed Oct 04 20:31:57 2023

[PaymentRequest] Implement accidental input protection on Android

Add an InputProtector to PaymentHandlerCoordinator and
PaymentRequestUI to prevent accidental input before a time threshold.
This only applies to the payment UI itself, more work is required to
add input protection to the payment handler web contents.

Bug: 1403493
Change-Id: I5cc395168dc80cee82444c3c09b81319b04ac67b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4317108
Reviewed-by: Stephen McGruer <smcgruer@chromium.org>
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
Commit-Queue: Nick Burris <nburris@chromium.org>
Reviewed-by: Boris Sazonov <bsazonov@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1205441}

[modify] https://crrev.com/f7c6ff28c4bf829d5337a8714108f9ef47e2a5be/chrome/android/java/src/org/chromium/chrome/browser/payments/handler/PaymentHandlerMediator.java
[modify] https://crrev.com/f7c6ff28c4bf829d5337a8714108f9ef47e2a5be/components/payments/content/android/BUILD.gn
[modify] https://crrev.com/f7c6ff28c4bf829d5337a8714108f9ef47e2a5be/chrome/android/javatests/src/org/chromium/chrome/browser/payments/PaymentRequestTestRule.java
[modify] https://crrev.com/f7c6ff28c4bf829d5337a8714108f9ef47e2a5be/chrome/android/javatests/src/org/chromium/chrome/browser/payments/ExpandablePaymentHandlerTest.java
[modify] https://crrev.com/f7c6ff28c4bf829d5337a8714108f9ef47e2a5be/chrome/android/javatests/DEPS
[modify] https://crrev.com/f7c6ff28c4bf829d5337a8714108f9ef47e2a5be/chrome/android/BUILD.gn
[modify] https://crrev.com/f7c6ff28c4bf829d5337a8714108f9ef47e2a5be/chrome/android/java/src/org/chromium/chrome/browser/payments/handler/PaymentHandlerCoordinator.java
[modify] https://crrev.com/f7c6ff28c4bf829d5337a8714108f9ef47e2a5be/chrome/android/java/src/org/chromium/chrome/browser/payments/ui/PaymentRequestUI.java
[add] https://crrev.com/f7c6ff28c4bf829d5337a8714108f9ef47e2a5be/chrome/android/javatests/src/org/chromium/chrome/browser/payments/PaymentRequestInputProtectionTest.java
[modify] https://crrev.com/f7c6ff28c4bf829d5337a8714108f9ef47e2a5be/chrome/android/chrome_test_java_sources.gni


### gi...@appspot.gserviceaccount.com (2023-10-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9bfe549b6d18fa15f17474ebebe185def34db879

commit 9bfe549b6d18fa15f17474ebebe185def34db879
Author: Nick Burris <nburris@chromium.org>
Date: Fri Oct 06 17:21:40 2023

[PaymentHandler] Avoid accidental input on Android PH WebView

Add an InputProtector to a new PaymentHandlerContentFrameLayout view
which wraps the payment handler web contents view on Android, in order
to intercept accidental input before a time threshold.

Bug: 1403493
Change-Id: If9e11d89473055483b4f389d959205c419d8805d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4907874
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
Reviewed-by: Stephen McGruer <smcgruer@chromium.org>
Commit-Queue: Nick Burris <nburris@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1206497}

[modify] https://crrev.com/9bfe549b6d18fa15f17474ebebe185def34db879/components/payments/content/android/java/res/layout/payment_handler_content.xml
[modify] https://crrev.com/9bfe549b6d18fa15f17474ebebe185def34db879/components/test/data/payments/maxpay.test/payment_handler_window.html
[modify] https://crrev.com/9bfe549b6d18fa15f17474ebebe185def34db879/chrome/android/java/src/org/chromium/chrome/browser/payments/handler/PaymentHandlerView.java
[modify] https://crrev.com/9bfe549b6d18fa15f17474ebebe185def34db879/chrome/android/chrome_java_sources.gni
[modify] https://crrev.com/9bfe549b6d18fa15f17474ebebe185def34db879/chrome/android/javatests/src/org/chromium/chrome/browser/payments/ExpandablePaymentHandlerTest.java
[add] https://crrev.com/9bfe549b6d18fa15f17474ebebe185def34db879/chrome/android/java/src/org/chromium/chrome/browser/payments/handler/PaymentHandlerContentFrameLayout.java
[modify] https://crrev.com/9bfe549b6d18fa15f17474ebebe185def34db879/chrome/android/java/src/org/chromium/chrome/browser/payments/handler/PaymentHandlerCoordinator.java


### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-11)

This issue was migrated from crbug.com/chromium/1403493?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-21)

nburris: Uh oh! This issue still open and hasn't been updated in the last 355 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sm...@chromium.org (2024-10-24)

Remaining work: click-jacking prevention on Payment Handler web contents area on Desktop. This is theoretically attackable, but I think low severity because:

1. The web contents has to load before it can be click-jacked, so there's likely some lower bound time being added automatically just by network latency.
2. The HTML/CSS/JS within the web content itself could add its own click jacking preventions if the given payment app so desired.

[A Chrome-side fix was investigated](https://chromium-review.googlesource.com/c/chromium/src/+/4904780) and found to be non-trivial, may need coordination with the Views team and/or Web Contents folks to figure out a solution. One thought - how do pop-up windows avoid click-jacking within the web contents?

### st...@gmail.com (2024-10-24)

Just to make is everyone is on the same page (...), this bug is about clickjacking the Continue button of the PaymentRequest dialog, which is part of the browser UI. This bug has been fixed.

---

Clickjacking of the web contents can definitely also be a problem, but I think this is a wider issue not limited to PaymentRequest.

> One thought - how do pop-up windows avoid click-jacking within the web contents?

As far as I am aware (please correct me if this has changed), there are currently no browser-side protections against temporal clickjacking of web contents.

An example of such attack could be opening a new tab / popup / PaymentRequest dialog to a page with an OAuth Confirm button.

For example, GitHub protects against this attack on the OAuth dialog page by disabling buttons for the first 500ms. However, there are websites that do not implement this protection and are therefore vulnerable to these temporal clickjacking attacks.

If there are efforts to protect against this class of attacks (and if this is feasible to fix), I believe it should rather be a standardized solution encompassing all affected web contents surfaces (tabs, popups, etc.), rather than specific to the PaymentRequest dialog.

### sm...@chromium.org (2024-10-24)

> If there are efforts to protect against this class of attacks (and if this is feasible to fix), I believe it should rather be a standardized solution encompassing all affected web contents surfaces (tabs, popups, etc.), rather than specific to the PaymentRequest dialog.

This seems reasonable to me, as long as our security folks agree :).

@adetaylor (please feel free to redirect) - does it seem reasonable to close this Fixed? Feel free to ping me internally if you want quick context :)

### ad...@google.com (2024-10-25)

Yes - I agree that this specific issue should be marked fixed and I'll do so. I've raised [issue 375543391](https://issues.chromium.org/issues/375543391) to consider the more general point of web contents clickjacking.

### sm...@chromium.org (2024-10-28)

Thanks Adrian! Reassigning to Nick just to recognize who did all the hard work of fixing this :)

### sp...@google.com (2024-11-14)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower-impact web platform privilege escalation


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-11-14)

Congratulations Thomas! Thank you for your efforts and reporting this issue to us.

### pe...@google.com (2025-02-01)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062366)*
