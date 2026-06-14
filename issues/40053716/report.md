# Security: Chromium doesn't conform to SMS Verification APIs leading to potential Access to app protected components vulnerability

| Field | Value |
|-------|-------|
| **Issue ID** | [40053716](https://issues.chromium.org/issues/40053716) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebOTP |
| **Platforms** | Android |
| **Reporter** | se...@oversecured.com |
| **Assignee** | mt...@chromium.org |
| **Created** | 2020-10-25 |
| **Bounty** | $1,000.00 |

## Description

Hey, I scanned multiple apps internally using Oversecured scanner and noticed that the most of them doesn't conform to official guidelines https://developers.google.com/identity/sms-retriever/user-consent/request#2_start_listening_for_incoming_messages

The guidelines require to ask the broadcast sender to have SmsRetriever.SEND_PERMISSION. However it's registered without any required permissions:
https://chromium.googlesource.com/chromium/src/+/refs/heads/master/content/public/android/java/src/org/chromium/content/browser/sms/SmsUserConsentReceiver.java#60

It may lead to Access to app protected components vulnerability (https://oversecured.com/vulnerabilities#Ability_to_start_arbitrary_components).

I tried to reproduce this issue in Google Chrome on Samsung Galaxy S8 Android 7.0 and an Emulator with Android 10. Chrome on the device crashes with NullPointerException (on this line https://chromium.googlesource.com/chromium/src/+/refs/heads/master/content/public/android/java/src/org/chromium/content/browser/sms/SmsUserConsentReceiver.java#108), because `mWindowAndroid` is null (`SmsUserConsentReceiver.listen(WindowAndroid)` is never called). And nothing happens on the emulator.

The received intent in `SmsRetriever.EXTRA_CONSENT_INTENT` is launched then without any security checks in the app's context (e.g. in Google Chrome). I'd like to bring your attention to this issue.

Thanks,
Sergey Toshin
Oversecured Inc.

## Timeline

### oc...@google.com (2020-10-26)

goto, could you please take a look at this?

[Monorail components: Blink>WebOTP]

### [Deleted User] (2020-10-26)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-02-03)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-02-03)

Raising severity to high because it allows any app on the device to send arbitrary intents to non-exported components within Chrome.

### [Deleted User] (2022-02-03)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-02-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f42f9f333a4e0f8c69f9d8c1e2bd52f08897b2bc

commit f42f9f333a4e0f8c69f9d8c1e2bd52f08897b2bc
Author: Michael Thiessen <mthiesse@chromium.org>
Date: Thu Feb 03 22:23:06 2022

Check Broadcast permissions in SmsUserConsentReceiver

In order to avoid any app sending us an
SmsRetriever.SMS_RETRIEVED_ACTION broadcast, we need to check that the
sender has the SmsRetriever.SEND_PERMISSION permission. This permission
ensures that only Google Play Services can send the broadcast.

The unit tests were also failing when run locally due to
LifetimeAssertions in Java because the WindowAndroid wasn't being
destroyed correctly, so I fixed it in all of the unit tests that create
WindowAndroids from c++.

Bug: 1142269
Change-Id: I3278919c566e1fc344ed0f4adce74fbf93a85c53
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3434025
Reviewed-by: Yi Gu <yigu@chromium.org>
Commit-Queue: Michael Thiessen <mthiesse@chromium.org>
Auto-Submit: Michael Thiessen <mthiesse@chromium.org>
Reviewed-by: Bo Liu <boliu@chromium.org>
Commit-Queue: Bo Liu <boliu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#966953}

[modify] https://crrev.com/f42f9f333a4e0f8c69f9d8c1e2bd52f08897b2bc/content/public/android/java/src/org/chromium/content/browser/sms/SmsUserConsentReceiver.java
[modify] https://crrev.com/f42f9f333a4e0f8c69f9d8c1e2bd52f08897b2bc/ui/android/resources/resource_manager_impl_unittest.cc
[modify] https://crrev.com/f42f9f333a4e0f8c69f9d8c1e2bd52f08897b2bc/content/public/android/java/src/org/chromium/content/browser/sms/Wrappers.java
[modify] https://crrev.com/f42f9f333a4e0f8c69f9d8c1e2bd52f08897b2bc/ui/android/BUILD.gn
[modify] https://crrev.com/f42f9f333a4e0f8c69f9d8c1e2bd52f08897b2bc/ui/android/java/src/org/chromium/ui/base/WindowAndroid.java
[rename] https://crrev.com/f42f9f333a4e0f8c69f9d8c1e2bd52f08897b2bc/ui/android/view_android_unittest.cc
[modify] https://crrev.com/f42f9f333a4e0f8c69f9d8c1e2bd52f08897b2bc/ui/android/window_android.cc
[modify] https://crrev.com/f42f9f333a4e0f8c69f9d8c1e2bd52f08897b2bc/ui/android/window_android.h
[modify] https://crrev.com/f42f9f333a4e0f8c69f9d8c1e2bd52f08897b2bc/content/browser/sms/sms_provider_gms_unittest.cc
[modify] https://crrev.com/f42f9f333a4e0f8c69f9d8c1e2bd52f08897b2bc/content/browser/renderer_host/render_widget_host_view_android_unittest.cc


### mt...@chromium.org (2022-02-03)

[Empty comment from Monorail migration]

### mt...@chromium.org (2022-02-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-05)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-17)

Hello, thank you for this report. The Chrome VRP would like to extend a $1000 reward to thank you for taking this time to report this issue to us. A member of our finance team will be in touch soon to arrange payment. 

### am...@google.com (2022-02-18)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-03-28)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-29)

[Empty comment from Monorail migration]

### ay...@chromium.org (2022-03-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-22)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/1142269?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1293506]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053716)*
