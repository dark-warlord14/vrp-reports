# SameSite Lax bypass with multiple-nested scenarios

| Field | Value |
|-------|-------|
| **Issue ID** | [40091123](https://issues.chromium.org/issues/40091123) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>DOM, Blink>SecurityFeature, Internals>Network>Cookies |
| **Platforms** | Windows |
| **Reporter** | s....@gmail.com |
| **Assignee** | mk...@chromium.org |
| **Created** | 2018-04-17 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36

Steps to reproduce the problem:
1. Go to https://test.shhnjk.com/SameSite.php (this sets SameSite Strict and Lax)
2. Go to https://test.shhnjk.com/sandbox.php?url=https://shhnjk.azurewebsites.net/iframer.php?url=https://test.shhnjk.com/SameSite.php

What is the expected behavior?
SameSite Lax cookie is not sent.

What went wrong?
Per spec: https://tools.ietf.org/html/draft-ietf-httpbis-cookie-same-site-00#section-2.1.1
`For documents which are displayed in nested browsing contexts, we need to audit the origins of each of a document's ancestor browsing contexts' active documents in order to account for the "multiple- nested scenarios" described in Section 4 of [RFC7034]. These document's "site for cookies" is the top-level site if and only if the document and each of its ancestor documents' origins have the same registrable domain as the top-level site. Otherwise its "site for cookies" is the empty string.`

For clarity, visit https://shhnjk.azurewebsites.net/iframer.php?url=https://test.shhnjk.com/SameSite.php. This does not send SameSite Lax cookie. But above PoC sends Lax cookie. It worth nothing that Lax cookie is sent whenever navigation happens at top-level browsing context. But there is still a case requires protection where attacker site is inside iframe sandbox without "allow-top-navigation" or "allow-popups" flag set. This scenario is demonstrated in the PoC.

Did this work before? N/A 

Chrome version: 65.0.3325.181  Channel: stable
OS Version: 10.0
Flash Version:

## Timeline

### va...@chromium.org (2018-04-17)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature Internals>Network>Cookies]

### va...@chromium.org (2018-04-18)

[Empty comment from Monorail migration]

### va...@chromium.org (2018-04-19)

caseq@: gentle ping from the security 👮 -- can you please take a quick look and help triage this? Thanks.

### va...@chromium.org (2018-04-19)

[Empty comment from Monorail migration]

[Monorail components: Blink>DOM]

### sh...@chromium.org (2018-04-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-20)

[Empty comment from Monorail migration]

### mk...@chromium.org (2018-04-23)

I'm pretty sure this is the TODO in https://cs.chromium.org/chromium/src/content/browser/frame_host/navigation_request.cc?l=1202. Will look in more detail tomorrow.

### mk...@chromium.org (2018-04-24)

Initial pass at this in https://chromium-review.googlesource.com/c/chromium/src/+/1025772.

### bu...@chromium.org (2018-04-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/07fbae50670ea44e35e1d554db1bbece7fe3711f

commit 07fbae50670ea44e35e1d554db1bbece7fe3711f
Author: Mike West <mkwst@chromium.org>
Date: Thu Apr 26 07:27:27 2018

Check ancestors when setting an <iframe> navigation's "site for cookies".

Currently, we're setting the "site for cookies" only by looking at the
top-level document. We ought to be verifying that the ancestor frames
are same-site before doing so. We do this correctly in Blink (see
`Document::SiteForCookies`), but didn't do so when navigating in the
browser.

This patch addresses the majority of the problem by walking the ancestor
chain when processing a NavigationRequest. If all the ancestors are
same-site, we set the "site for cookies" to the top-level document's URL.
If they aren't all same-site, we set it to an empty URL to ensure that
we don't send SameSite cookies.

Bug: 833847
Change-Id: Icd77f31fa618fa9f8b59fc3b15e1bed6ee05aabd
Reviewed-on: https://chromium-review.googlesource.com/1025772
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Commit-Queue: Mike West <mkwst@chromium.org>
Cr-Commit-Position: refs/heads/master@{#553942}
[modify] https://crrev.com/07fbae50670ea44e35e1d554db1bbece7fe3711f/content/browser/frame_host/navigation_request.cc
[add] https://crrev.com/07fbae50670ea44e35e1d554db1bbece7fe3711f/third_party/WebKit/LayoutTests/http/tests/cookies/resources/frame.php
[add] https://crrev.com/07fbae50670ea44e35e1d554db1bbece7fe3711f/third_party/WebKit/LayoutTests/http/tests/cookies/resources/post-cookies-to-top.php
[add] https://crrev.com/07fbae50670ea44e35e1d554db1bbece7fe3711f/third_party/WebKit/LayoutTests/http/tests/cookies/same-site/framed.html


### sh...@chromium.org (2018-05-08)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-05-22)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-05-30)

[Empty comment from Monorail migration]

### s....@gmail.com (2018-06-15)

Seems like this bug has been fixed?

### ar...@chromium.org (2018-06-15)

I can no more reproduce the bug on your test case. It is fixed.

In https://crbug.com/chromium/833847#c9: mkwst@ wrote "this patch addresses the majority of the problem". Maybe he knows other kind of similar problems that could happens. Maybe he wants to keep this bug open until they got fixed. He is OOO, let's wait for his confirmation to close this bug.

### s....@gmail.com (2018-07-20)

Please mark this bug as fixed. mkwst@'s OOO message is made in such a way that it never comes (No month specified).

More details at: 
https://bugs.chromium.org/u/mkwst@chromium.org/updates

### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### me...@google.com (2018-07-27)

I pinged Mike offline.

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### s....@gmail.com (2018-09-12)

Someone, please mark this bug as fixed!!!

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-01)

This bug requires manual review: M71 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-11-01)

+awhalley@ (Security TPM) for M71 merge review.

### aw...@google.com (2018-11-01)

Fixed in 68, no 71 merge needed.

### aw...@chromium.org (2018-11-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-11-02)

And $1,000 for this one :-)

### aw...@google.com (2018-11-02)

[Empty comment from Monorail migration]

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/833847?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>DOM, Blink>SecurityFeature, Internals>Network>Cookies]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091123)*
