# Security: CSS Paint API leaks visited status of links (up to ~3k/sec)

| Field | Value |
|-------|-------|
| **Issue ID** | [40091172](https://issues.chromium.org/issues/40091172) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Paint, Privacy |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | md...@gmail.com |
| **Assignee** | xi...@chromium.org |
| **Created** | 2018-04-21 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**

An attacker can determine whether a link is visited or not by observing if  

a `paint` method call has been invoked.

In the attached attack, we set a custom painter from a CSS Paint API worklet as  

the background of a link element. If we use the DOM to switch the link's href  

from a visited URL to an unvisited URL (or vice versa), the `paint` method of  

the custom painter is invoked. On the other hand, if we switch it from one  

unvisited URL to another unvisited URL (or visited to visited), the `paint`  

method is not invoked. We can observe the presence or absence of this extra  

`paint` call in order to determine the visited status of an arbitrary target  

URL.

We amplify this attack by using an array of helper link elements to concurrently  

scan for visited URLs. Abusing the `registerPaint` function to store state  

between paintlet invocations, the attached amplified exploit can probe up to 3k  

URLs/sec for visited status. For comparison, the entire Alexa Top 100,000 can be  

scanned in 30-40 seconds.

**VERSION** (tested on 3 systems)

Chrome Version: 66.0.3359.117 stable  

Operating System: Windows 10 Pro Version 1709 (OS Build 16299.371)

Chrome Version: 65.0.3325.181 stable  

Operating System: macOS 10.10.5

Chrome Version: 66.0.3359.117 stable  

(`chromium 66.0.3359.117-1` package from Arch repo)  

Operating System: Arch Linux

**REPRODUCTION CASE**

`basic-attack.html` demonstrates the attack in its simplest form.  

`amplified-attack.html` demonstrates the amplified version.

## Attachments

- [amplified-attack.html](attachments/amplified-attack.html) (text/plain, 15.5 KB)
- [basic-attack.html](attachments/basic-attack.html) (text/plain, 3.9 KB)

## Timeline

### va...@chromium.org (2018-04-22)

This looks like a privacy bug, instead of a security bug to me so setting Security_Severity-Low for now.

[Monorail components: Blink>Paint]

### va...@chromium.org (2018-04-22)

[Empty comment from Monorail migration]

### va...@chromium.org (2018-04-22)

[Empty comment from Monorail migration]

[Monorail components: Privacy]

### el...@chromium.org (2018-04-23)

While a bit squishy, an equivalent case is an example in our Security Severity Medium bucket as "Reliably read or infer browser history" https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md#Medium-severity

### md...@gmail.com (2018-04-23)

I wrote in earlier to make the same point, but it seems that replying to the notification email didn't work to add a comment. I think https://bugs.chromium.org/p/chromium/issues/detail?id=381808 is a good comparison, and that was classified as medium-severity.

### va...@chromium.org (2018-04-23)

Yes, I agree. Thanks for pointing it out.

### sh...@chromium.org (2018-04-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-23)

[Empty comment from Monorail migration]

### ik...@chromium.org (2018-04-23)

Thanks for the research,

Xida - I dug into this a little bit, basically with the Paint API we are exposing invalidation, which is what this is using.

There are variants of this people could use I think, e.g. 
<a style="display: block">
  <div id=painter></div>
</div>

I think the safest approach here is to switch off Paint for any subtree which is within a link, e.g.

CSSPaintValue::GetImage() {
  if (style.InsideLink() != EInsideLink::kNotInsideLink)
    return nullptr;
}

// above attack doesn't strictly require this, but might be able to time invalidation for an excessively large input properties or similar.
ComputedStyle::DiffNeedsPaintInvalidationObjectForPaintImage() {
  if (InsideLink() != EInsideLink::kNotInsideLink)
    return false;
}

### fl...@chromium.org (2018-04-23)

I suppose the geometry could change when you switch :visited style so we couldn't fix this with caching?

### ik...@chromium.org (2018-04-23)

So geometry can't change based on visited styles, so we could potentially fix this with caching, but we'd have to be more careful.

### fl...@chromium.org (2018-04-23)

Okay, so we can fix this for now by not supporting it as you've suggested in #9 and then fix it longterm with caching such that it would never invalidate for strictly a visited invalidation.

### fl...@chromium.org (2018-04-23)

We can discuss all the requirements for that in a separate bug - but naively we would need to filter out any of the "visited" specific styling information or ensure that we paint with both visited and unvisited style.

### ik...@chromium.org (2018-04-23)

Sounds good, I think it'll be easier once we have the machinery for off-thread, as at the moment my sense is that it'll add too much technical-debt to add caching at the moment.

But we should quickly explore caching properly just to check. 

### xi...@chromium.org (2018-04-23)

I agree that we should have a quick fix as suggested in #9, and explore caching.

### bu...@chromium.org (2018-05-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/67d9b414fa64448abc398ae9fc57c3ddf5de5998

commit 67d9b414fa64448abc398ae9fc57c3ddf5de5998
Author: Xida Chen <xidachen@chromium.org>
Date: Thu May 03 17:31:46 2018

[PaintWorklet] Do not paint when paint target is associated with a link

When the target element of a paint worklet has an associated link, then
the 'paint' function will be invoked when the link's href is changed
from a visited URL to an unvisited URL (or vice versa).

This CL changes the behavior by detecting whether the target element
of a paint worklet has an associated link or not. If it does, then don't
paint.

TBR=haraken@chromium.org

Bug: 835589
Change-Id: I5fdf85685f863c960a6f48cc9a345dda787bece1
Reviewed-on: https://chromium-review.googlesource.com/1035524
Reviewed-by: Xida Chen <xidachen@chromium.org>
Reviewed-by: Ian Kilpatrick <ikilpatrick@chromium.org>
Reviewed-by: Stephen McGruer <smcgruer@chromium.org>
Commit-Queue: Xida Chen <xidachen@chromium.org>
Cr-Commit-Position: refs/heads/master@{#555788}
[modify] https://crrev.com/67d9b414fa64448abc398ae9fc57c3ddf5de5998/third_party/blink/renderer/controller/BUILD.gn
[modify] https://crrev.com/67d9b414fa64448abc398ae9fc57c3ddf5de5998/third_party/blink/renderer/core/BUILD.gn
[modify] https://crrev.com/67d9b414fa64448abc398ae9fc57c3ddf5de5998/third_party/blink/renderer/core/css/css_custom_ident_value.h
[modify] https://crrev.com/67d9b414fa64448abc398ae9fc57c3ddf5de5998/third_party/blink/renderer/core/css/css_paint_value.cc
[modify] https://crrev.com/67d9b414fa64448abc398ae9fc57c3ddf5de5998/third_party/blink/renderer/core/css/css_paint_value.h
[add] https://crrev.com/67d9b414fa64448abc398ae9fc57c3ddf5de5998/third_party/blink/renderer/core/css/css_paint_value_test.cc
[add] https://crrev.com/67d9b414fa64448abc398ae9fc57c3ddf5de5998/third_party/blink/renderer/core/css/test_data/csspaint-do-not-paint-for-link-descendant.html
[add] https://crrev.com/67d9b414fa64448abc398ae9fc57c3ddf5de5998/third_party/blink/renderer/core/css/test_data/csspaint-do-not-paint-for-link.html
[modify] https://crrev.com/67d9b414fa64448abc398ae9fc57c3ddf5de5998/third_party/blink/renderer/core/style/computed_style.cc


### xi...@chromium.org (2018-05-03)

This is now fixed, should we request to merge back?

### xi...@chromium.org (2018-05-07)

[Empty comment from Monorail migration]

### xi...@chromium.org (2018-05-07)

cc govind@ for merge request.

### sh...@chromium.org (2018-05-07)

This bug requires manual review: M67 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-05-07)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-05-07)

+awhalley@ (Security TPM) for M67 merge review.

### aw...@google.com (2018-05-07)

govind@ - good for 67

### xi...@chromium.org (2018-05-07)

+awhalley@: please let me know the branch number.

### go...@chromium.org (2018-05-07)

Approving merge to M67 branch 3396 based on https://crbug.com/chromium/835589#c23. Please merge ASAP so we can pick it up for this week Beta release. Thank you.

### aw...@google.com (2018-05-07)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-05-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/53c53adc17c964fa4f5410b2a2610f1ebde7f118

commit 53c53adc17c964fa4f5410b2a2610f1ebde7f118
Author: Xida Chen <xidachen@chromium.org>
Date: Mon May 07 18:32:41 2018

[PaintWorklet] Do not paint when paint target is associated with a link

When the target element of a paint worklet has an associated link, then
the 'paint' function will be invoked when the link's href is changed
from a visited URL to an unvisited URL (or vice versa).

This CL changes the behavior by detecting whether the target element
of a paint worklet has an associated link or not. If it does, then don't
paint.

TBR=haraken@chromium.org

Bug: 835589
Change-Id: I5fdf85685f863c960a6f48cc9a345dda787bece1
Reviewed-on: https://chromium-review.googlesource.com/1035524
Reviewed-by: Xida Chen <xidachen@chromium.org>
Reviewed-by: Ian Kilpatrick <ikilpatrick@chromium.org>
Reviewed-by: Stephen McGruer <smcgruer@chromium.org>
Commit-Queue: Xida Chen <xidachen@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#555788}(cherry picked from commit 67d9b414fa64448abc398ae9fc57c3ddf5de5998)
Reviewed-on: https://chromium-review.googlesource.com/1048059
Cr-Commit-Position: refs/branch-heads/3396@{#502}
Cr-Branched-From: 9ef2aa869bc7bc0c089e255d698cca6e47d6b038-refs/heads/master@{#550428}
[modify] https://crrev.com/53c53adc17c964fa4f5410b2a2610f1ebde7f118/third_party/blink/renderer/controller/BUILD.gn
[modify] https://crrev.com/53c53adc17c964fa4f5410b2a2610f1ebde7f118/third_party/blink/renderer/core/BUILD.gn
[modify] https://crrev.com/53c53adc17c964fa4f5410b2a2610f1ebde7f118/third_party/blink/renderer/core/css/css_custom_ident_value.h
[modify] https://crrev.com/53c53adc17c964fa4f5410b2a2610f1ebde7f118/third_party/blink/renderer/core/css/css_paint_value.cc
[modify] https://crrev.com/53c53adc17c964fa4f5410b2a2610f1ebde7f118/third_party/blink/renderer/core/css/css_paint_value.h
[add] https://crrev.com/53c53adc17c964fa4f5410b2a2610f1ebde7f118/third_party/blink/renderer/core/css/css_paint_value_test.cc
[add] https://crrev.com/53c53adc17c964fa4f5410b2a2610f1ebde7f118/third_party/blink/renderer/core/css/test_data/csspaint-do-not-paint-for-link-descendant.html
[add] https://crrev.com/53c53adc17c964fa4f5410b2a2610f1ebde7f118/third_party/blink/renderer/core/css/test_data/csspaint-do-not-paint-for-link.html
[modify] https://crrev.com/53c53adc17c964fa4f5410b2a2610f1ebde7f118/third_party/blink/renderer/core/style/computed_style.cc


### sh...@chromium.org (2018-05-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-05-09)

Nice one mdsmtp@ - the Chrome VRP panel decided to award $2,000 for this report. A member of our finance team will be in touch to arrange payment.  Also, how would you like to be credited in the Chrome release notes?

### aw...@chromium.org (2018-05-09)

[Empty comment from Monorail migration]

### md...@gmail.com (2018-05-09)

Thanks! Glad to see this fixed. You can credit me as "Michael Smith (spinda.net)".

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### aa...@chromium.org (2022-08-15)

[Empty comment from Monorail migration]

### is...@google.com (2022-08-15)

This issue was migrated from crbug.com/chromium/835589?no_tracker_redirect=1

[Multiple monorail components: Blink>Paint, Privacy]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091172)*
