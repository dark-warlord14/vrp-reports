# Security: Cursor hijacking mitigation bypass if iframe's content area is outside the top-layer content area

| Field | Value |
|-------|-------|
| **Issue ID** | [40065759](https://issues.chromium.org/issues/40065759) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>CSS, Blink>HTML>IFrame, Blink>Input |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | ms...@chromium.org |
| **Created** | 2023-06-13 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

If an iframe's content area exists outside the content area of the top layer, it is possible to bypass the 32x32 custom cursor hijacking mitigation and render a 128x128 cursor over browser UI.

**VERSION**  

Chrome Version: 114.0.5735.110 (Official Build) (64-bit) (cohort: Stable)  

Operating System: Windows 10 Version 22H2 (Build 19045.2965)

**REPRODUCTION CASE**

1. Go to <https://small-rocky-tennis.glitch.me/mouse-hack.html> (mouse-hack.html is frame.html in the attached files)
2. Hover over anywhere on the page to gain the fake cursor
3. Using the fake cursor, click on the padlock icon and see fake status

This reproduction uses the page at <https://jameshfisher.github.io/cursory-hack/>.  

If you would like a local server reproduction:

1. Download cursor.png, padlock.png, popout.png, cursor-page.html (credit to jameshfisher.github.io) and serve it on origin A
2. frame.html hosted on origin B and edit the iframe to point to origin A. (Note that must be different origins as I think it has something to do with "OOPIFs")

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Axel Chong

## Attachments

- [cursor.png](attachments/cursor.png) (image/png, 9.8 KB)
- [popout.png](attachments/popout.png) (image/png, 28.2 KB)
- [padlock.png](attachments/padlock.png) (image/png, 3.9 KB)
- [cursor-page.html](attachments/cursor-page.html) (text/plain, 2.9 KB)
- [frame.html](attachments/frame.html) (text/plain, 146 B)
- [Untitled_ Jun 14, 2023 1_23 AM.webm](attachments/Untitled_ Jun 14, 2023 1_23 AM.webm) (video/webm, 663.1 KB)
- [Screenshot 2023-06-14 014432.png](attachments/Screenshot 2023-06-14 014432.png) (image/png, 19.7 KB)
- [Untitled_ Jun 15, 2023 8_32 AM.webm](attachments/Untitled_ Jun 15, 2023 8_32 AM.webm) (video/webm, 725.7 KB)
- [Untitled_ Jul 30, 2023 4_42 PM.webm](attachments/Untitled_ Jul 30, 2023 4_42 PM.webm) (video/webm, 800.0 KB)

## Timeline

### [Deleted User] (2023-06-13)

[Empty comment from Monorail migration]

### ha...@gmail.com (2023-06-13)

I think this image explains the problem

### dc...@chromium.org (2023-06-13)

I'm not 100% sure if OOPIF is required here. There does seem to be some bug here with high DPI displays.

I've reproduced various versions of this not being clipped properly by the viewport on Mac; it looks like the original report was not limited to Mac-only though, so I'm going to tag all non-iOS platforms for now.

From some brief testing, it seems like stable is also prone to this; I haven't tested extended stable yet.

[Monorail components: Blink>CSS]

### dc...@chromium.org (2023-06-13)

Oh extended stable is the same as stable atm.

### [Deleted User] (2023-06-13)

[Empty comment from Monorail migration]

### ms...@chromium.org (2023-06-13)

I can repro on Mac 13.4 + Chrome M114, the effect is more pronounced on the internal retina display.
Some related Issues: https://crbug.com/chromium/1149906, https://crbug.com/chromium/1246188, https://crbug.com/chromium/1357442, https://crbug.com/chromium/1385714
Some relevant code: https://crsrc.org/c/third_party/blink/renderer/core/input/event_handler.cc;drc=1ab551376498819cea8404e0826a063c3b579f04;l=590
Other useful repro links: https://benjaminbenben.com/cursory-hack/ https://cr.kungfoo.net/style/cursor/abusive-cursor.html

### ha...@gmail.com (2023-06-14)

I think this may be the issue:

In https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/input/event_handler.cc;l=599;drc=1ab551376498819cea8404e0826a063c3b579f04

This line suggests that the custom cursor is being checked against the visual viewport of a page. Since the custom cursor exists in the iframe and therefore is checked against the visual viewport of the iframe (instead of the top frame), which according to MDN:
(https://developer.mozilla.org/en-US/docs/Web/CSS/Viewport_concepts > Search for keyword "iframe"), which need not be visible in the parent page (and can exist outside the top frame as it is in this case)

-- my non-expert take.


### ha...@gmail.com (2023-06-14)

There is also similar security bug https://bugs.chromium.org/p/chromium/issues/detail?id=1099276 which involves custom cursor and iframes and is what led me to find this bug

### ha...@gmail.com (2023-06-14)

[Comment Deleted]

### ha...@gmail.com (2023-06-14)

It also seems that the payload in https://bugs.chromium.org/p/chromium/issues/detail?id=1099276
-----
data:text/html,<iframe src="http://cr.kungfoo.net/style/cursor/abusive-cursor.html" style="width:700px;height:1000px;position:absolute;top:-100px;">
-----
Does not work. The difference between that payload is that the old payload uses negative offset (top:-100px) for the iframe to cause its visual viewport to exist outside of the top frame. On the other hand the new payload in this report is that this report involves a window.scrollTo() to change the iframe position. I am not entirely sure how window.scrollTo is different from a negative top offset though.

### ha...@gmail.com (2023-06-14)

It also seems like in https://bugs.chromium.org/p/chromium/issues/detail?id=1099276 they were aware of the issue where if the visual viewport of the iframe exist outside of the page then this particular issue occurs, the fix was line 593-597 which seems to account for this by applying some kind of transform on the cursor position:

https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/input/event_handler.cc;l=593;drc=1ab551376498819cea8404e0826a063c3b579f04
--------
            frame_->ContentLayoutObject()->LocalToAncestorPoint(
                location.Point(),
                nullptr,  // no ancestor maps all the way up the hierarchy
                kTraverseDocumentBoundaries | kApplyRemoteMainFrameTransform) -
            PhysicalOffset(hot_spot);
--------
So perhaps the cursor offset is computed wrongly when the page is scrolled?

I also checked MapCoordinatesFlag for LocalToAncestorPoint and notice the kIgnoreScrollOffset flag --https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:third_party/blink/renderer/core/layout/map_coordinates_flags.h;l=22;drc=7ac4a606711a108763d6dedbc84e6fc32ccf821f;bpv=0;bpt=1

Maybe this flag is missing?

### [Deleted User] (2023-06-14)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@gmail.com (2023-06-15)

I have another video which demonstrates how the scroll + iframe affects the issue.

As can be seen, the effect is more pronounced the further you scroll down. 

Tested on Windows 10.

POC URL: https://small-rocky-tennis.glitch.me/mouse-hack-2.html

### [Deleted User] (2023-06-28)

msw: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ms...@chromium.org (2023-06-30)

Thanks for the updates and keen observations, haxatron1@gmail.com!
The repro in #13 is helpful, and the event_handler.cc code cited in #11 is almost certainly using an incorrect transform.
https://crsrc.org/c/third_party/blink/renderer/core/input/event_handler.cc;l=593;drc=1ab551376498819cea8404e0826a063c3b579f04
I'll look when I return on July 20th. This can probably wait, but others can jump in while I'm out.

[Monorail components: Blink>Input]

### [Deleted User] (2023-07-15)

msw: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@gmail.com (2023-07-30)

I have a working fix for this issue 🎉

The solution was to apply MapToVisualRectInAncestorSpace to the frame rect which accounts for scroll, before checking .contains()

Verified locally (see video)

Patch: https://chromium-review.googlesource.com/c/chromium/src/+/4728774

### ms...@chromium.org (2023-07-31)

Nice, thanks for devising and uploading the fix! Adding reviewer for context

[Monorail components: Blink>HTML>IFrame]

### gi...@appspot.gserviceaccount.com (2023-08-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/19fdec19317884bacf8f48fce2f0c222d0497caa

commit 19fdec19317884bacf8f48fce2f0c222d0497caa
Author: Haxatron Sec <haxatron1@gmail.com>
Date: Thu Aug 03 17:44:55 2023

Account for scroll in cursor checks

Use the correct transform for frame rect to account for scroll.

Video: https://bugs.chromium.org/p/chromium/issues/detail?id=1454515#c18

Fixed: 1454515
Change-Id: I996bfaaaddc22055f7f350c40357625c420141e6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4728774
Reviewed-by: Stefan Zager <szager@chromium.org>
Reviewed-by: Mike Wasserman <msw@chromium.org>
Commit-Queue: Mike Wasserman <msw@chromium.org>
Reviewed-by: Ken Buchanan <kenrb@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1179139}

[modify] https://crrev.com/19fdec19317884bacf8f48fce2f0c222d0497caa/third_party/blink/renderer/core/input/event_handler.cc
[modify] https://crrev.com/19fdec19317884bacf8f48fce2f0c222d0497caa/content/browser/site_per_process_hit_test_browsertest.cc


### [Deleted User] (2023-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-04)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-09)

Congratulations, Axel! The VRP Panel has decided to award you $1,000 for this report. The reward amount was based on the fairly limited feasibility to convincingly exploit this issue. Thank you for your efforts and reporting this issue to us! 

### am...@chromium.org (2023-08-10)

Hi Axel -- please accept our apologies. In the original assessment of this issue, we missed that you submitted and committed the patch and browser test for this issue. Thanks for your efforts on this. I've updated the reward amount to reflect a $1,000 patch bonus for this patch. Nice work! 

### ms...@chromium.org (2023-08-10)

+1, thank you Axel!
And thanks Amy for updating Axel's recognition and award!

### am...@google.com (2023-08-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-09-09)

[Empty comment from Monorail migration]

### pg...@google.com (2023-09-12)

[Empty comment from Monorail migration]

### pg...@google.com (2023-09-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1454515?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>CSS, Blink>HTML>IFrame, Blink>Input]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065759)*
