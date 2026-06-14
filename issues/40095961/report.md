# Security: URL bar spoofing on Android with a very long URL

| Field | Value |
|-------|-------|
| **Issue ID** | [40095961](https://issues.chromium.org/issues/40095961) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | Android |
| **Reporter** | ch...@gmail.com |
| **Assignee** | te...@chromium.org |
| **Created** | 2019-08-12 |
| **Bounty** | $3,000.00 |

## Description

Chrome Version: All  

Operating System: Android

This is same bug as 989497.

**REPRODUCTION CASE**

1. Go to lbstyle.github.io/content.html
2. Click on the button
3. Observe

Actual: Observe that ..tform.accounts.google.com URL displayed.

Expected: The bar URL should be displayed as about:blank

## Attachments

- [screen.jpeg](attachments/screen.jpeg) (image/jpeg, 23.7 KB)
- [content.html](attachments/content.html) (text/plain, 289 B)

## Timeline

### ke...@chromium.org (2019-08-12)

Thanks for the report. It looks like a flaw in the elision code from r503824.

tedchoc@: PTAL?

[Monorail components: UI>Browser>Omnibox]

### es...@chromium.org (2019-08-19)

tedchoc, have you had a chance to look at this yet?

### te...@chromium.org (2019-08-19)

Shamefully no.  I missed this last week.  My hope is that this is a one liner fix, but I'll try that out now.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/cb2479d07021b4772582a20a70124fa395e4fd38

commit cb2479d07021b4772582a20a70124fa395e4fd38
Author: Ted Choc <tedchoc@chromium.org>
Date: Mon Aug 19 22:02:23 2019

Fix URL bar scrolling logic for about: URLs.

BUG=992838

Change-Id: Idc6ab38c6f40224188312f9f6804857fcf48828f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1757299
Commit-Queue: Ted Choc <tedchoc@chromium.org>
Reviewed-by: Ender <ender@google.com>
Cr-Commit-Position: refs/heads/master@{#688290}

[modify] https://crrev.com/cb2479d07021b4772582a20a70124fa395e4fd38/chrome/android/java/src/org/chromium/chrome/browser/omnibox/UrlBarData.java
[modify] https://crrev.com/cb2479d07021b4772582a20a70124fa395e4fd38/chrome/android/javatests/src/org/chromium/chrome/browser/omnibox/OmniboxTest.java
[modify] https://crrev.com/cb2479d07021b4772582a20a70124fa395e4fd38/chrome/android/junit/src/org/chromium/chrome/browser/omnibox/UrlBarDataTest.java
[modify] https://crrev.com/cb2479d07021b4772582a20a70124fa395e4fd38/chrome/android/junit/src/org/chromium/chrome/browser/omnibox/UrlBarMediatorUnitTest.java


### es...@chromium.org (2019-08-20)

Thanks for the quick fix, Ted! Can we close this bug now, or is there more work to do?

### te...@google.com (2019-08-21)

Nope, it is all addressed. Just verified in Canary.

### sh...@chromium.org (2019-08-22)

[Empty comment from Monorail migration]

### na...@google.com (2019-08-26)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-09-05)

Congrats! The Panel decided to reward $3,000 for this report

### na...@google.com (2019-09-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-20)

Not requesting merge to beta (M78) because latest trunk commit (688290) appears to be prior to beta branch point (693954). If this is incorrect, please replace the Merge-na label with Merge-Request-78. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2019-10-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-10-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-11-28)

This issue was migrated from crbug.com/chromium/992838?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095961)*
