# Security: PaymentRequest dialog selects an accept button by default

| Field | Value |
|-------|-------|
| **Issue ID** | [40062377](https://issues.chromium.org/issues/40062377) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Payments |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | sm...@chromium.org |
| **Created** | 2022-12-24 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

The payment dialog has the "Continue" button focused by default. This presents an issue as this makes the dialog keyjackable.

In a regular keyjacking attack (also works in this case), the Enter key would have to be pressed twice or held for half a second.

For some reason, however, **a single Enter keypress** is able to both open the dialog and confirm it as well in one go. This works only when listening for the `keydown` event.

What is likely happening (if key events are propagated `keydown`->`keypress`->`keyup`):

1. The page listens for the Enter `keydown` event.
2. The page opens a payment dialog.
3. The payment dialog receives an Enter `keypress`/`keyup`, and the default confirm button is pressed.

**Impact:**  

If the user has an address/email/phone saved in the browser, pressing Enter once in the page will reveal this to the attacker's page.

**VERSION**  

Chrome Version: 108.0.5359.125 + stable  

Operating System: Windows 11

**REPRODUCTION CASE**

1. python3 -m http.server 9000
2. <http://localhost:9000/poc.html>
3. Press Enter

**Docs** (docs/security/security-considerations-for-browser-ui.md):

> # Don't have a default-selected accept button
> 
> If your dialog or UI has a call-to-action triggered by a button that is default-selected, the dialog is subject to keyjacking. An evil webpage can trick a user into mashing or repeatedly hitting the Enter key, and then trigger your dialog to show, causing the user to unknowingly accept.

**CREDIT INFORMATION**  

Reporter credit: Thomas Orlita

## Attachments

- [app.js](attachments/app.js) (text/plain, 215 B)
- [manifest.json](attachments/manifest.json) (text/plain, 384 B)
- [payment-manifest.json](attachments/payment-manifest.json) (text/plain, 151 B)
- [poc.html](attachments/poc.html) (text/plain, 1011 B)
- [poc.webm](attachments/poc.webm) (video/webm, 532.1 KB)
- [key-event-timeline.png](attachments/key-event-timeline.png) (image/png, 48.6 KB)

## Timeline

### [Deleted User] (2022-12-24)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-12-26)

Thanks for the report. Triaged the same way as https://crbug.com/1403493.

[Monorail components: Blink>Payments]

### [Deleted User] (2022-12-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-26)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sm...@chromium.org (2022-12-29)

Thanks for the report. Given that again this is new guidance for a long-existing UI (when this UI was implemented, UX/a11y guidance was to have the default action default-selected afaik!), not 100% clear on priority, but we will aim to tackle this in early Q1.

### gi...@appspot.gserviceaccount.com (2023-01-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/57d342625c581190ac9b845fafeae6b1c7cae7dc

commit 57d342625c581190ac9b845fafeae6b1c7cae7dc
Author: Stephen McGruer <smcgruer@chromium.org>
Date: Wed Jan 04 15:31:20 2023

PaymentRequest: Don't auto-focus 'Continue' button

Per new security guidelines in
docs/security/security-considerations-for-browser-ui.md:

"# Don't have a default-selected accept button

If your dialog or UI has a call-to-action triggered by a button that is
default-selected, the dialog is subject to keyjacking. An evil webpage
can trick a user into mashing or repeatedly hitting the Enter key, and
then trigger your dialog to show, causing the user to unknowingly
accept. Users should have to make an explicit selection on security- or
privacy-sensitive browser UI surfaces."

Bug: 1403539
Change-Id: I67791955574dd9ba97705c4e979a353e70a4e8e6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4130374
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Commit-Queue: Stephen McGruer <smcgruer@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1088729}

[modify] https://crrev.com/57d342625c581190ac9b845fafeae6b1c7cae7dc/chrome/browser/ui/views/payments/payment_sheet_view_controller_browsertest.cc
[modify] https://crrev.com/57d342625c581190ac9b845fafeae6b1c7cae7dc/chrome/browser/ui/views/payments/payment_request_sheet_controller.cc


### sm...@chromium.org (2023-01-04)

The above CL should fix this, though I want to wait until it gets into Canary and do some verification first.

### sm...@chromium.org (2023-01-05)

Fix in https://crbug.com/chromium/1403539#c6 did NOT work. The initial focus is no longer on the 'Continue' button and a single enter does not fast-forward through both launch+accept, but pressing Enter again still causes the continue action to happen. Something funky is going on, we're capturing enter somehow and making it always continue no matter the focus.


### gi...@appspot.gserviceaccount.com (2023-01-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3e3782335fd99b85218feb2cbf0a388950d90d6c

commit 3e3782335fd99b85218feb2cbf0a388950d90d6c
Author: Stephen McGruer <smcgruer@chromium.org>
Date: Fri Jan 06 13:17:12 2023

[PaymentRequest] Don't install enter-key accelerator for all sheets

Most notably, the main payment sheet should not accelerate the enter
key, for the same reason as in https://crrev.com/57d342625c .

This CL attempts to keep the acceleration as it was on all other sheets,
and adds browsertests for those sheets that did not previously have
them.

Bug: 1403539
Change-Id: I5a98818e9fa7782a8cf28f20abe82d87ce4df83c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4133533
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Commit-Queue: Stephen McGruer <smcgruer@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1089689}

[modify] https://crrev.com/3e3782335fd99b85218feb2cbf0a388950d90d6c/chrome/browser/ui/views/payments/error_message_view_controller_browsertest.cc
[modify] https://crrev.com/3e3782335fd99b85218feb2cbf0a388950d90d6c/chrome/browser/ui/views/payments/editor_view_controller.cc
[modify] https://crrev.com/3e3782335fd99b85218feb2cbf0a388950d90d6c/chrome/browser/ui/views/payments/payment_request_dialog_view_ids.h
[modify] https://crrev.com/3e3782335fd99b85218feb2cbf0a388950d90d6c/chrome/browser/ui/views/payments/order_summary_view_controller.h
[modify] https://crrev.com/3e3782335fd99b85218feb2cbf0a388950d90d6c/chrome/browser/ui/views/payments/order_summary_view_controller.cc
[modify] https://crrev.com/3e3782335fd99b85218feb2cbf0a388950d90d6c/chrome/browser/ui/views/payments/payment_sheet_view_controller_browsertest.cc
[modify] https://crrev.com/3e3782335fd99b85218feb2cbf0a388950d90d6c/chrome/browser/ui/views/payments/contact_info_editor_view_controller_browsertest.cc
[modify] https://crrev.com/3e3782335fd99b85218feb2cbf0a388950d90d6c/chrome/browser/ui/views/payments/shipping_address_editor_view_controller_browsertest.cc
[modify] https://crrev.com/3e3782335fd99b85218feb2cbf0a388950d90d6c/chrome/browser/ui/views/payments/payment_sheet_view_controller.h
[modify] https://crrev.com/3e3782335fd99b85218feb2cbf0a388950d90d6c/chrome/browser/ui/views/payments/payment_request_sheet_controller.cc
[modify] https://crrev.com/3e3782335fd99b85218feb2cbf0a388950d90d6c/chrome/browser/ui/views/payments/order_summary_view_controller_browsertest.cc
[modify] https://crrev.com/3e3782335fd99b85218feb2cbf0a388950d90d6c/chrome/browser/ui/views/payments/error_message_view_controller.cc
[modify] https://crrev.com/3e3782335fd99b85218feb2cbf0a388950d90d6c/chrome/browser/ui/views/payments/payment_sheet_view_controller.cc
[modify] https://crrev.com/3e3782335fd99b85218feb2cbf0a388950d90d6c/chrome/browser/ui/views/payments/payment_request_sheet_controller.h
[modify] https://crrev.com/3e3782335fd99b85218feb2cbf0a388950d90d6c/chrome/browser/ui/views/payments/editor_view_controller.h
[modify] https://crrev.com/3e3782335fd99b85218feb2cbf0a388950d90d6c/chrome/browser/ui/views/payments/error_message_view_controller.h


### sm...@chromium.org (2023-01-11)

This should be fix as of the commit in https://crbug.com/chromium/1403539#c9. The default focus is now the first row of the UI (will which depend on the payment options passed in). The UI is a little uglier with this initial focus ring, but it is hopefully passable until we deprecate the remaining browser sheet reasons.

### [Deleted User] (2023-01-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-12)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-26)

Congratulations, Thomas! The VRP Panel has decided to award you $5,000 for this report. Thank you for your efforts in discovering and reporting this issue to us -- nice work! 

### am...@google.com (2023-01-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-06)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-07)

[Empty comment from Monorail migration]

### pg...@google.com (2023-03-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1403539?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062377)*
