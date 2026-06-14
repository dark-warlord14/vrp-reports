# Referrer policy bypass with about:blank and document.write()

| Field | Value |
|-------|-------|
| **Issue ID** | [40088951](https://issues.chromium.org/issues/40088951) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature>Referrer |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | s....@gmail.com |
| **Assignee** | jo...@chromium.org |
| **Created** | 2017-09-08 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36

Steps to reproduce the problem:
1. Go to https://test.shhnjk.com/refpol.php
2. Click Go.

What is the expected behavior?
Referrer shouldn't send to shhnjk.com

What went wrong?
Referrer sent.
I made sure this time that I have referrer policy set with header + meta.

Did this work before? N/A 

Chrome version: 61.0.3163.79  Channel: stable
OS Version: 10.0
Flash Version:

## Timeline

### el...@chromium.org (2017-09-08)

The Referrer Policy specification doesn't directly answer the question of whether a Referrer Policy should be inherited by a new window spawned to about:blank.

Emily?

https://www.w3.org/TR/referrer-policy/#referrer-policy-delivery-nested

4.4. Nested browsing contexts
The HTML Standard and Fetch Standard define how nested browsing contexts that are not created from responses, such as iframe elements with their srcdoc attribute set, or created from a blob URL, inherit their referrer policy from the creator browsing context or blob URL.

[Monorail components: Blink>SecurityFeature>Referrer]

### es...@chromium.org (2017-09-08)

Yep, this is a bug, it's specified in step 10 of https://html.spec.whatwg.org/#creating-a-new-browsing-context.

We should write a web platform test for this as well.

### s....@gmail.com (2017-09-08)

Made small modification. This also works with document.write()-ing any same-origin page inside iframe.

https://test.shhnjk.com/refpol.php

So this is not issue of about:blank, But document.write(). Since it also work with any other element (img, link, etc) this could occur with normal website thus I think severity of issue is bit higher.

### el...@chromium.org (2017-09-09)

I'm not an expert on this topic, but as far as I understand things, if you document.write on a document in ReadyState==Done, it's equivalent to first navigating to about:blank, then performing the write.

### jo...@chromium.org (2017-09-11)

[Empty comment from Monorail migration]

### jo...@chromium.org (2017-10-19)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-10-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/931711135c90568f677cf42d94f2591a7eeced2e

commit 931711135c90568f677cf42d94f2591a7eeced2e
Author: Jochen Eisinger <jochen@chromium.org>
Date: Tue Oct 24 18:19:37 2017

Inherit referrer and policy when creating a nested browsing context

BUG=763194
R=estark@chromium.org

Change-Id: Ide3950269adf26ba221f573dfa088e95291ab676
Reviewed-on: https://chromium-review.googlesource.com/732652
Reviewed-by: Emily Stark <estark@chromium.org>
Commit-Queue: Jochen Eisinger <jochen@chromium.org>
Cr-Commit-Position: refs/heads/master@{#511211}
[add] https://crrev.com/931711135c90568f677cf42d94f2591a7eeced2e/third_party/WebKit/LayoutTests/external/wpt/referrer-policy/generic/iframe-inheritance.html
[modify] https://crrev.com/931711135c90568f677cf42d94f2591a7eeced2e/third_party/WebKit/Source/core/dom/Document.cpp


### jo...@chromium.org (2017-10-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-10-31)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-11-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-11-06)

$500 for this report - thanks as ever!

### s....@gmail.com (2017-11-06)

oh wow!Thanks!

### aw...@chromium.org (2017-11-09)

[Empty comment from Monorail migration]

### aw...@google.com (2017-12-04)

[Empty comment from Monorail migration]

### aw...@google.com (2018-01-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### is...@google.com (2018-10-05)

This issue was migrated from crbug.com/chromium/763194?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088951)*
