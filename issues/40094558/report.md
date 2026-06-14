# Security: IntersectionObserver V2 fails for CSS property scale transform

| Field | Value |
|-------|-------|
| **Issue ID** | [40094558](https://issues.chromium.org/issues/40094558) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Layout |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ue...@gmail.com |
| **Assignee** | sz...@chromium.org |
| **Created** | 2019-04-10 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

If a DOM element is overlapping another element because of a scale transformation the IntersectionObserver V2 fails to detect the overlap. Thus, clickjacking is not mitigated as intended.

**VERSION**  

Chrome Version: 75.0.3759.4 (Official Build) dev (64-bit)  

Operating System: macOS 10.14.4 (18E226)

**REPRODUCTION CASE**  

PoC: <https://io-v2--pwnd.glitch.me/>  

Code: <https://glitch.com/edit/#!/io-v2--pwnd?path=index.html:1:0>  

This PoC is based on <https://io-v2.glitch.me/> found here in the Google Chrome Developers channel: <https://www.youtube.com/watch?v=EIH6IQgwdAc>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

No crash.

**CREDIT INFORMATION**  

Reporter credit: Robin Linus ( robinlinus.com )

## Timeline

### ct...@chromium.org (2019-04-10)

[Empty comment from Monorail migration]

### ct...@chromium.org (2019-04-10)

Setting this as Severity-Low for now (placing it similar to a CSP bypass with limitations). szager@ could you take a look?

One question for the reporter: Do you think this POC would be reasonably extendable to have no visually noticeable artifact?

If you let the scale transform fully complete and then refresh the page, the page is rendered as is _after_ the scale, which makes me think that a more involved malicious page could potentially avoid visual notice while doing this.

Bisecting gives:
https://chromium.googlesource.com/chromium/src/+log/8b74e636cac47cd8dbb5f6133014866f80b24276..0b65cb95ed32a8737c3cf4e82d7f602ac6624987

Of which it seems that this started with https://chromium.googlesource.com/chromium/src/+/0b65cb95ed32a8737c3cf4e82d7f602ac6624987 (which makes sense), which landed in 74.0.3685.0



[Monorail components: Blink>Layout]

### ue...@gmail.com (2019-04-10)

>> Do you think this POC would be reasonably extendable to have no visually noticeable artifact?

The PoC would be easily extendable into a stealth exploit. Actually the noticeable artifacts are there only to visualize the bug better. The transition/animation is not needed. A scale transform without transition works, too.

Here's a "stealth" version with no visually noticeable artifact: 

PoC: https://io-v2-pwnd-stealth.glitch.me/
Code: https://glitch.com/edit/#!/io-v2-pwnd-stealth?path=style.css:57:2



### sz...@chromium.org (2019-04-11)

The underlying issue is that IntersectionObserver uses the target's layout size when hit testing for occlusion:

https://cs.chromium.org/chromium/src/third_party/blink/renderer/core/intersection_observer/intersection_geometry.cc?rcl=2519dc69493fe74332ff09133c6bd91e75be8c42&l=182

It should use the target's visual rect instead, just like we do in the hit test code:

https://cs.chromium.org/chromium/src/third_party/blink/renderer/core/layout/layout_box.cc?rcl=4179c0e6d921ad9c0e9d5b748594a1a441486be1&l=1650

### ue...@gmail.com (2019-04-11)

>> Setting this as Severity-Low for now (placing it similar to a CSP bypass with limitations). 

Developers probably expect this API to behave like described here: https://developers.google.com/web/updates/2019/02/intersectionobserver-v2 
"False positives are not permitted under any circumstances (that is, setting isVisible to true when the target element is not completely visible and unmodified)." 

@chrishtr Are you sure about the low severity? If I understand correctly, this bug lets you break the main security guarantee of the IntersectionObserverV2 and thus, renders it useless.

### sz...@chromium.org (2019-04-11)

I think the security-severity label is fine, because no sites are yet relying on the feature, and there is no impact on the security of the browser itself.

Don't worry, this will get fixed soon :)

### sz...@chromium.org (2019-04-18)

The reproduction for this bug relies on a compositor-driven animation, which updates the display without re-rendering on the main thread.

However, if you interact with the page at all while the animation is running, then the main thread will update its state synchronously, and IntersectionObserver V2 will generated the proper notification. Try running the reproduction, and move the mouse or press a key; you should see the "like" button transition to red/"not visible" as it intersects with the "clickbait" box.

For this reason, I don't believe the bug is exploitable; if the user clicks on an element, an IntersectionObserver V2 notification will be processed before the click event arrives.

In playing with the demo, I was unable to get a click accepted by the iframe while the like button was occluded. So my inclination is to mark this bug "WontFix". Please let me know if I'm missing something.

### ue...@gmail.com (2019-04-18)

No, the animation is not related to the bug. A scale transform without transition works, too. Again, here's a "stealth" version of the PoC with no animation:

PoC: https://io-v2-pwnd-stealth.glitch.me/
Code: https://glitch.com/edit/#!/io-v2-pwnd-stealth?path=style.css:57:2


This PoC shows the bug is very easily exploitable and it renders the IntersectionObserver V2 completely useless.

### sz...@chromium.org (2019-04-23)

[Empty comment from Monorail migration]

### sz...@chromium.org (2019-04-23)

OK, I can see the issue now, and I have a fix in progress.

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-04-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/497840011525b41c4fc51397eddceb42d67c84ae

commit 497840011525b41c4fc51397eddceb42d67c84ae
Author: Stefan Zager <szager@chromium.org>
Date: Wed Apr 24 21:56:43 2019

[IntersectionObserver] Correctly handle a scaled target

If a target is inside an iframe, and the iframe (or one if its
ancestors in the parent document) has a scale applied, then we need to
apply the scale to the hit test rect when checking for occlusion. The
default LocalFrameView coordinate conversion routines don't do that.
Use LocalToAncestorQuad instead.

BUG=951525
R=chrishtr@chromium.org

Change-Id: I1107f0bd3c6d262a392fbafe430897cc09068623
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1578100
Reviewed-by: Chris Harrelson <chrishtr@chromium.org>
Commit-Queue: Stefan Zager <szager@chromium.org>
Cr-Commit-Position: refs/heads/master@{#653774}

[modify] https://crrev.com/497840011525b41c4fc51397eddceb42d67c84ae/third_party/blink/renderer/core/input/event_handler.cc
[add] https://crrev.com/497840011525b41c4fc51397eddceb42d67c84ae/third_party/blink/web_tests/external/wpt/intersection-observer/resources/scaled-target-subframe.html
[add] https://crrev.com/497840011525b41c4fc51397eddceb42d67c84ae/third_party/blink/web_tests/external/wpt/intersection-observer/v2/scaled-target.html
[modify] https://crrev.com/497840011525b41c4fc51397eddceb42d67c84ae/third_party/blink/web_tests/external/wpt/lint.whitelist


### ue...@gmail.com (2019-05-14)

Does this report qualify for the Chrome Vulnerability Reward Program? If so, how shall I proceed? 

### ko...@chromium.org (2019-05-20)

[Empty comment from Monorail migration]

### ue...@gmail.com (2019-05-25)

any updates? 

### ea...@chromium.org (2019-05-31)

Stefan?

### sz...@chromium.org (2019-05-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-01)

[Empty comment from Monorail migration]

### na...@google.com (2019-06-03)

[Empty comment from Monorail migration]

### aw...@google.com (2019-06-04)

[Empty comment from Monorail migration]

### ue...@gmail.com (2019-06-13)

Hey guys, I understand you guys are very busy and this is just a low severity issue but it would be very nice to get an update from you such that I can tick this off my list. Thank you for your time!

### ch...@chromium.org (2019-06-13)

Hi,

The bug was marked as fixed on May 31. Are you saying you think it might not actually be fixed?

### ue...@gmail.com (2019-06-14)

Hi Chris, 
No my question from May 14 was: "Does this report qualify for the Chrome Vulnerability Reward Program? If so, how shall I proceed?" 


### ct...@chromium.org (2019-06-14)

ueberlego@: This is marked "reward-topanel" now, which means it will go to our VRP panel soon. Once that happens, they'll reach out for next steps.

### ue...@gmail.com (2019-07-10)

Hi, this has been marked as “reward-topanel” for five weeks. Are there any news?

### ct...@chromium.org (2019-07-10)

+awhalley to help check on status of VRP panel stuff.

### aw...@google.com (2019-07-10)

+natashapabrai for VRP things these days :-)

Sorry this is taking a while ueberlego@, we've skipped a few VRP panel meetings with the US 4th July holidays and folk being out, so we're working through a backlog. And I'm afraid we tend to give  Security_Severity-Low bugs lower priority (we used not to consider them at all by default) so it might take a few more weeks to get to it, I'm sorry to say.

### ad...@google.com (2019-07-29)

[Empty comment from Monorail migration]

### ad...@google.com (2019-07-29)

ueberlego@gmail.com - thanks for the report. How would you like to be credited in release notes?

### ad...@google.com (2019-07-29)

[Empty comment from Monorail migration]

### ad...@google.com (2019-07-29)

Sorry - spotted the credit information in the original bug report, please ignore!

### ad...@chromium.org (2019-07-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2019-09-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-09-30)

Congrats! The Panel decided to reward $500 for this report :) 

### na...@google.com (2019-09-30)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### is...@google.com (2019-11-23)

This issue was migrated from crbug.com/chromium/951525?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/951526, crbug.com/chromium/953265]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094558)*
