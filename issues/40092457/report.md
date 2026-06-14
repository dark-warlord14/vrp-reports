# Security: http authentication spoof on chrome android

| Field | Value |
|-------|-------|
| **Issue ID** | [40092457](https://issues.chromium.org/issues/40092457) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Network>Auth, UI>Browser>Mobile, UI>Browser>Navigation |
| **Platforms** | Android |
| **Reporter** | ma...@gmail.com |
| **Assignee** | te...@chromium.org |
| **Created** | 2018-09-14 |
| **Bounty** | $1,000.00 |

## Description

online demo : <http://www.applestore.ac.cn/r/spoof.html>

see 401\_spoof.jpg

the popup should be closed after navigation

**VERSION**  

Chrome Version: chrome 69  

Operating System: android

## Attachments

- [401_spoof.jpg](attachments/401_spoof.jpg) (image/jpeg, 65.3 KB)

## Timeline

### rs...@chromium.org (2018-09-14)

I can confirm this on Android. On Desktop, the auth dialog is dismissed on the redirect, but on mobile it isn't.

yfriedman: According to git log, you upstreamed LoginPrompt.java and there've only been mechanical changes since. Can you take a look or suggest an owner for this bug?

[Monorail components: Internals>Network>Auth UI>Browser>Mobile UI>Browser>Navigation]

### yf...@chromium.org (2018-09-14)

Have we tried repoing in Chrome 68? It's possible that some auto-dismissing logic doesn't trigger anymore? 

Although a quick look doesn't suggest this would ever have been dismissed. That is unless we had some global dialog dismisser but I don't know if that's even possible, +ted?

Looks like a legitimate issue. What's the turnaround expected, rsesek? Would we want to try and include in a m69-respin or m70? Not sure how to verify whether the auth credentials end up getting used or are invalidated at a later stage?

### bu...@chromium.org (2018-09-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f40a8c947f6f13ea97baa3d7967e033f75587b41

commit f40a8c947f6f13ea97baa3d7967e033f75587b41
Author: Ted Choc <tedchoc@chromium.org>
Date: Mon Sep 17 18:31:56 2018

Auto-dismiss http auth dialogs on navigation for Android.

BUG=884179

Change-Id: I18287e9c641045d5a74f3804e06ca17485e38957
Reviewed-on: https://chromium-review.googlesource.com/1227482
Commit-Queue: Ted Choc <tedchoc@chromium.org>
Reviewed-by: Yaron Friedman <yfriedman@chromium.org>
Cr-Commit-Position: refs/heads/master@{#591747}
[modify] https://crrev.com/f40a8c947f6f13ea97baa3d7967e033f75587b41/chrome/android/java/src/org/chromium/chrome/browser/ChromeHttpAuthHandler.java
[modify] https://crrev.com/f40a8c947f6f13ea97baa3d7967e033f75587b41/chrome/android/java/src/org/chromium/chrome/browser/LoginPrompt.java
[modify] https://crrev.com/f40a8c947f6f13ea97baa3d7967e033f75587b41/chrome/android/java_sources.gni
[add] https://crrev.com/f40a8c947f6f13ea97baa3d7967e033f75587b41/chrome/android/javatests/src/org/chromium/chrome/browser/ChromeHttpAuthHandlerTest.java
[modify] https://crrev.com/f40a8c947f6f13ea97baa3d7967e033f75587b41/chrome/browser/ui/android/chrome_http_auth_handler.cc
[modify] https://crrev.com/f40a8c947f6f13ea97baa3d7967e033f75587b41/chrome/browser/ui/android/chrome_http_auth_handler.h
[modify] https://crrev.com/f40a8c947f6f13ea97baa3d7967e033f75587b41/chrome/browser/ui/android/login_handler_android.cc


### te...@chromium.org (2018-09-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-10-04)

Nice one, ma7h1as.l@ - $1,000 for this report.

### aw...@chromium.org (2018-10-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-26)

This bug requires manual review: M71 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### te...@chromium.org (2018-10-26)

The CL already landed in M70 (71.0.3555.0), removing spurious merge bits.

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-12-25)

This issue was migrated from crbug.com/chromium/884179?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Network>Auth, UI>Browser>Mobile, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092457)*
