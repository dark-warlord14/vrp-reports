# Security: Incognito Mode-specific external protocol prompts can be overlaid on other origins on Android.

| Field | Value |
|-------|-------|
| **Issue ID** | [40062470](https://issues.chromium.org/issues/40062470) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Mobile>Intents, UI>Browser>Incognito |
| **Platforms** | Android |
| **Reporter** | ha...@gmail.com |
| **Assignee** | mt...@chromium.org |
| **Created** | 2023-01-03 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

In incognito mode, the external protocol prompt that exists is different than non-incognito mode.

This prompt can be overlaid over other origins and continued to, which can cause potential user confusion.

**VERSION**  

Chrome Version: 108.0.5359.128 Stable  

Operating System: Android 13

**REPRODUCTION CASE**

1. Go to <https://spice-flicker-squirrel.glitch.me/apple-spoof.html> in incognito mode

apple-spoof.html

```
<script>  
location.href = "tel:1"  
setTimeout('location.href = "https://apple.com"', 500)  
</script>  

```

2. You should see the prompt overlaid on apple.com as shown in the screenshot
3. Clicking "Leave" will open the Phone app.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Axel Chong

## Attachments

- [Screenshot_20230103_135334_Chrome.jpg](attachments/Screenshot_20230103_135334_Chrome.jpg) (image/jpeg, 456.4 KB)

## Timeline

### [Deleted User] (2023-01-03)

[Empty comment from Monorail migration]

### da...@chromium.org (2023-01-04)

PTAL Android folks. And could you confirm if this occurs in M108 for the FoundIn-108 label?

[Monorail components: Mobile>Intents UI>Browser>Incognito]

### [Deleted User] (2023-01-04)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mt...@chromium.org (2023-01-05)

Yep, this has existed for ~forever.

We should probably cancel the leaving incognito dialog when you redirect.

### [Deleted User] (2023-01-05)

[Empty comment from Monorail migration]

### mt...@chromium.org (2023-01-20)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-01-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7bcc68456cea2ebea8fcfec925708ee25ef02bc6

commit 7bcc68456cea2ebea8fcfec925708ee25ef02bc6
Author: Michael Thiessen <mthiesse@chromium.org>
Date: Thu Jan 26 03:11:55 2023

Dismiss Incognito alert dialog when the page navigates

When the leaving Incognito Alert Dialog is displayed, the page can
still navigate, which ends up showing the Alert Dialog over an origin
that didn't initiate it. This change dismisses the Alert Dialog when
another navigation occurs in the tab.

Bug: 1404621
Change-Id: Ia3084ec8e2413a8f2d658b0433db072f7286e141
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4174407
Reviewed-by: Yaron Friedman <yfriedman@chromium.org>
Commit-Queue: Michael Thiessen <mthiesse@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1097220}

[modify] https://crrev.com/7bcc68456cea2ebea8fcfec925708ee25ef02bc6/components/external_intents/android/javatests/src/org/chromium/components/external_intents/ExternalNavigationHandlerTest.java
[modify] https://crrev.com/7bcc68456cea2ebea8fcfec925708ee25ef02bc6/components/external_intents/android/java/src/org/chromium/components/external_intents/ExternalNavigationHandler.java


### mt...@chromium.org (2023-01-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-27)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-02-03)

Congratulations on another one, Axel! The VRP Panel has decided to award you $1,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-02-04)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-06)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-07)

[Empty comment from Monorail migration]

### pg...@google.com (2023-03-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-05-05)

This issue was migrated from crbug.com/chromium/1404621?no_tracker_redirect=1

[Multiple monorail components: Mobile>Intents, UI>Browser>Incognito]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062470)*
