# Leaking window.length without opener reference. 

| Field | Value |
|-------|-------|
| **Issue ID** | [40059056](https://issues.chromium.org/issues/40059056) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature>COOP, Internals>Sandbox>SiteIsolation, UI>Browser>Navigation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | nd...@protonmail.com |
| **Assignee** | ah...@chromium.org |
| **Created** | 2022-03-10 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36

Steps to reproduce the problem:
1. https://example.com/ run open(); // cross origin page
2. opener.location = 'https://first-party-test.glitch.me/?coop=same-origin'; // Page with COOP
3. let frame = document.createElement('iframe'); f.src = "https://example.org"; document.body.appendChild(f); // Must be cross origin
4. In context of iframe do parent.opener.length to get a new length just create a new cross origin iframe.

You can replace example.com, example.org first-party-test.glitch.me (coop page) with any other origin.

What is the expected behavior?
parent.opener.closed = true (when opener has coop)
It allows leaking the window.length from a coop protected page and after the user has changed the url in the address bar.

What went wrong?
parent.opener.closed = false (when opener has coop)

Did this work before? N/A 

Chrome version: 99.0.4844.51  Channel: stable
OS Version: 10.0

## Timeline

### [Deleted User] (2022-03-10)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2022-03-11)

By frame I mean f
I noticed sometimes length is not correct if that happens just create a new cross-origin iframe.


### bo...@google.com (2022-03-14)

Thanks for the report! Could you please elaborate on the security impact? In other words, what would a malicious website do with this behavior to the detriment of web users? 

[Monorail components: UI>Browser>Navigation]

### cr...@chromium.org (2022-03-14)

Sounds like this might be a small data leak for COOP?  When the opener is navigated to a COOP page, it should go to a new browsing context group (BrowsingInstance), making it inaccessible to the popup.  It does look like an injected iframe in the popup can see iframes in the opener (via RemoteFrames / RenderFrameProxies), though, which shouldn't happen.  Maybe there's an issue with creating proxies across BrowsingInstances?

This doesn't seem particularly severe unless you can do things with those frames, but it is an information leak that COOP was designed to prevent.  Arthur, can you take a look and help triage or find an owner?  Thanks!

[Monorail components: Blink>SecurityFeature>COOP Internals>Sandbox>SiteIsolation]

### ar...@chromium.org (2022-03-14)

Thank you for the reproducer! I was skeptical, but this is indeed reproducible.
Here is a video (see attachment)

When you check from the parent "opener" you get null.
However when you check from the child: "parent.opener" you get something not null.
This is not expected.

It looks like when the iframe is same-site with the opener, it is able to "reconstruct" proxies, even if we previously cleared them.

+ahemery@ since you did the implementation, this might be something you would like to take? Happy to help or discuss it.

### [Deleted User] (2022-03-14)

[Empty comment from Monorail migration]

### ah...@chromium.org (2022-03-16)

Having a look! I am able to reproduce and that's indeed very weird...

### gi...@appspot.gserviceaccount.com (2022-03-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e465928a544ccec77e292cd46720f3d1122aa832

commit e465928a544ccec77e292cd46720f3d1122aa832
Author: Arthur Hemery <ahemery@chromium.org>
Date: Mon Mar 28 08:36:15 2022

Fix COOP-based opener removal on FrameTreeNodes.

When a page A opens a page B, B can access A via window.opener. If
either of these pages navigate causing a BrowsingInstance swap, the
links need to be severed. Currently it only works well if B navigates.

If A navigates, we do not find the frames that were opened by it and
remove their openers on the browser side. This is now done in the
RenderFrameHostManager.

We also clarify how this information is carried to the renderer, which
was quite obscure and maybe even involuntary. Explains that the
RenderView suppression will trigger an opener clear.

BUG=1305394

Change-Id: I4bb2a9733c523dac78ffb270877ba07aba6984a4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3532010
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Commit-Queue: Arthur Hemery <ahemery@chromium.org>
Cr-Commit-Position: refs/heads/main@{#985876}

[modify] https://crrev.com/e465928a544ccec77e292cd46720f3d1122aa832/content/browser/renderer_host/render_frame_host_manager.cc
[modify] https://crrev.com/e465928a544ccec77e292cd46720f3d1122aa832/content/browser/renderer_host/frame_tree_node.h
[modify] https://crrev.com/e465928a544ccec77e292cd46720f3d1122aa832/content/browser/renderer_host/frame_tree_node.cc
[modify] https://crrev.com/e465928a544ccec77e292cd46720f3d1122aa832/content/browser/cross_origin_opener_policy_browsertest.cc


### [Deleted User] (2022-03-29)

[Empty comment from Monorail migration]

### ah...@chromium.org (2022-04-04)

Note for myself: this is fixed but I need to write WPTs to make sure the behavior is implemented by other browsers as well.

### gi...@appspot.gserviceaccount.com (2022-04-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b465304f25945922b9cf68b7e8bf74c056871ecf

commit b465304f25945922b9cf68b7e8bf74c056871ecf
Author: Arthur Hemery <ahemery@chromium.org>
Date: Mon Apr 11 19:53:56 2022

WPT for opener navigations with COOP.

COOP is used to sever relationships with openers, protecting from
side-channel attacks. This can happen both when opening popups and when
navigating, and that essentially relies on the same mechanism.

When a popup navigates, we do all the opener clearing very nicely and
everything ends up in a good state. When the page that opened the popup
navigates instead, we do not have as much coverage and some exploits
were discovered on Chrome (see associated bug, and fix patch:
https://chromium-review.googlesource.com/c/chromium/src/+/3532010)

This patch adds minimal coverage.

Bug: 1305394
Change-Id: I0d1158acf8ba4521eba272c2a9d6170f60b8bd94
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3578744
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Commit-Queue: Arthur Hemery <ahemery@chromium.org>
Cr-Commit-Position: refs/heads/main@{#991150}

[add] https://crrev.com/b465304f25945922b9cf68b7e8bf74c056871ecf/third_party/blink/web_tests/external/wpt/html/cross-origin-opener-policy/coop-popup-opener-navigates.https.html.headers
[add] https://crrev.com/b465304f25945922b9cf68b7e8bf74c056871ecf/third_party/blink/web_tests/external/wpt/html/cross-origin-opener-policy/coop-popup-opener-navigates.https.html


### ah...@chromium.org (2022-04-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-12)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### nd...@protonmail.com (2022-04-22)

Thanks :)

### am...@chromium.org (2022-04-22)

You're welcome! Thanks for your efforts and reporting this issue to us. :) 

### am...@google.com (2022-04-25)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2022-07-29)

This issue was migrated from crbug.com/chromium/1305394?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>SecurityFeature>COOP, Internals>Sandbox>SiteIsolation, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059056)*
