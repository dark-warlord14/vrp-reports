# Incognito Mode Leaving Alert Dialog Box Tapjacking on DoubleClick

| Field | Value |
|-------|-------|
| **Issue ID** | [40066828](https://issues.chromium.org/issues/40066828) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Incognito |
| **Platforms** | Android |
| **Reporter** | sh...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2023-07-04 |
| **Bounty** | $2,000.00 |

## Description

**Steps to reproduce the problem:**

1. Open Incognito Mode in Android Chrome and visit : <http://lnmi.unaux.com/ptap.html>
2. Double click on Cookie Image
3. You will notice the Incognito mode leaving alert dialog box LEAVE button is clicked accidentally.

**Problem Description:**  

Normally Incognito mode of Chrome shows a `Leaving Alert Dialog Box` whenever any webpage wants to open URL Schemes or INTENTS or simply wants to communicate outside of the browser. This leaving alert dialog box helps users to know that they are going outside of the Incognito Mode or the Incognito Mode is about to be closed.  

Chrome fails to protect against double click action which can result in clicking on LEAVE button accidentally and users will be tricked into opening any installed apps or intents.

**Additional Comments:**  

This issue is similar to :  

<https://bugs.chromium.org/p/chromium/issues/detail?id=1413586>

\*\*Chrome version: \*\* 114.0.0.0 \*\*Channel: \*\* Stable

**OS:** Android

## Attachments

- [ptap.html](attachments/ptap.html) (text/plain, 478 B)
- [cookie.png](attachments/cookie.png) (image/png, 4.0 KB)
- [Screenrecorder-2023-07-04-15-28-31-591.mp4](attachments/Screenrecorder-2023-07-04-15-28-31-591.mp4) (video/mp4, 5.0 MB)

## Timeline

### [Deleted User] (2023-07-04)

[Empty comment from Monorail migration]

### pm...@chromium.org (2023-07-05)

Hi there,

I was able to reproduce on 114.0.5735.196.
another one, that I think will fall under your  purview as well. A relatively low security, but still worth considering since a user could be tricked into leaving incognito.

thanks

[Monorail components: UI>Browser>Incognito UI>Browser>Mobile]

### [Deleted User] (2023-07-05)

[Empty comment from Monorail migration]

### tw...@chromium.org (2023-07-05)

Rerouting to incognito owner to consider whether leaving incognito dialog should use the new button protection param added for permission dialogs in https://chromium-review.googlesource.com/c/chromium/src/+/4242477 and cc'ing Lijin to consult if needed

[Monorail components: -UI>Browser>Mobile]

### ro...@chromium.org (2023-07-05)

Re https://crbug.com/chromium/1462104#c4: Thanks for sharing crrev/c/4242477. I don't see any reason on the top of my head what can go wrong with introducing the button protection for the "Leave Incognito mode ?" dialog, overall it seems like a good idea.

 I found 2 references to the dialog [1] [2], and they seem to be using the native AlertDialog. We might need to first add support of `ModalDialogManager`  there so we can pass the new properties. `PermissionDialogController` in components/*  seems to rely on getting the `ModalDialogManager` from the `WindowAndroid` [3]. Perhaps, we can somehow pass the WindowAndroid in [1] and [2] and then migrate the existing properties in use of AlertDialog to `ModalDialogProperties`.  

Lijin, do you expect any UX changes if we migrate from AlertDialog to ModalDialogProperties? I'm asking because this _may_ require an UX review.

[1] https://source.chromium.org/chromium/chromium/src/+/main:components/payments/content/android/java/src/org/chromium/components/payments/AndroidPaymentApp.java;l=133

[2] https://source.chromium.org/chromium/chromium/src/+/main:components/external_intents/android/java/src/org/chromium/components/external_intents/ExternalNavigationHandler.java;l=1372 

[3] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:components/permissions/android/java/src/org/chromium/components/permissions/PermissionDialogController.java;l=196;

### ro...@chromium.org (2023-07-05)

In the meantime to resolve this issue perhaps we can probably add an artificial delay in the positive button in [1] [2] that doesn't rely on ModalDialogProperty? lazzzis@ wdyt?

### la...@chromium.org (2023-07-05)

SG to migrate to ModalDialog. The style of ModalDialog extends AlertDialog's style. I don't expect there will be much UX difference.

### ro...@chromium.org (2023-07-07)

[Empty comment from Monorail migration]

### ro...@chromium.org (2023-07-07)

[Empty comment from Monorail migration]

### an...@google.com (2023-07-11)

[Empty comment from Monorail migration]

### ro...@chromium.org (2023-07-13)

[Empty comment from Monorail migration]

### ro...@chromium.org (2023-07-13)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-07-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e5d62ba06f8af010799b746244d3e66bdc05b7c8

commit e5d62ba06f8af010799b746244d3e66bdc05b7c8
Author: Rohit Agarwal <roagarwal@chromium.org>
Date: Thu Jul 13 19:13:55 2023

Android: Migrate Leave Incognito mode from alert dialog to Modal dialog

This CL migrates the usage of AlertDialog to Modal dialog for
ExternalNavigationHandler which solely used it for the
"Leave Incognito mode?" confirmation dialog.

The use of AlertDialog had limitations which resulted in issue stated
in crbug.com/1462104, around click-jacking. The click-jacking issue
has been solved elsewhere for permission dialogs (which are powered
by Chrome's modal dialog framework) by introducing some
delay when the buttons in the dialog becomes functional.

Following the same, this CL upgrades the AlertDialog to use Chrome's
Modal dialog support instead.

Demo: https://drive.google.com/file/d/1dkOr2hQodrjS4Ogy7qjiQZPWfAXGtqcN/view?usp=sharing
Bug: 1462104, 1422272, b/291039251
Change-Id: I51d53492f2aca3a5642ea794652997537a3273e5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4681767
Reviewed-by: Theresa Sullivan <twellington@chromium.org>
Commit-Queue: Rohit Agarwal <roagarwal@chromium.org>
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Reviewed-by: Lijin Shen <lazzzis@google.com>
Cr-Commit-Position: refs/heads/main@{#1170075}

[modify] https://crrev.com/e5d62ba06f8af010799b746244d3e66bdc05b7c8/components/external_intents/android/javatests/src/org/chromium/components/external_intents/ExternalNavigationHandlerTest.java
[modify] https://crrev.com/e5d62ba06f8af010799b746244d3e66bdc05b7c8/components/external_intents/android/java/src/org/chromium/components/external_intents/ExternalNavigationHandler.java
[modify] https://crrev.com/e5d62ba06f8af010799b746244d3e66bdc05b7c8/chrome/android/javatests/src/org/chromium/chrome/browser/externalnav/UrlOverridingTest.java


### ro...@chromium.org (2023-07-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-14)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-10)

Congratulations! The VRP Panel has decided to award you $2,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-08-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-09-09)

[Empty comment from Monorail migration]

### pg...@google.com (2023-09-12)

[Empty comment from Monorail migration]

### pg...@google.com (2023-09-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-10-20)

This issue was migrated from crbug.com/chromium/1462104?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40066828)*
