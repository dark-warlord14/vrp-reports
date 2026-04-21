# Security: Draw Mouse Cursor to hide omni box

| Field | Value |
|-------|-------|
| **Issue ID** | [40060702](https://issues.chromium.org/issues/40060702) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Input, UI>HighDPI |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | sa...@gmail.com |
| **Assignee** | ms...@chromium.org |
| **Created** | 2022-08-29 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**

**VERSION**  

Chrome Version: Version 103.0.5046.0 (Developer Build) (64-bit)]  

Operating System: Windows 10

**REPRODUCTION CASE**

1. Open pocursors.html
2. move the cursor at the top until the black rectacle is appears, its over into omni box and the omni box is covered by a box

I attached POC video

**CREDIT INFORMATION**

Reporter credit: Hafiizh (<https://www.linkedin.com/in/hafiizh-7aa6bb31/>)

## Attachments

- [poccursors.html](attachments/poccursors.html) (text/plain, 3.1 KB)
- [bandicam 2022-08-29 09-27-18-095.mp4](attachments/bandicam 2022-08-29 09-27-18-095.mp4) (video/mp4, 1.7 MB)

## Timeline

### [Deleted User] (2022-08-29)

[Empty comment from Monorail migration]

### es...@chromium.org (2022-08-29)

Thanks for the report. This doesn't seem likely to be exploitable because of the specific user interaction involved, however I'll conservatively label it as Low severity -- perhaps it could be more useful to an attacker if the cursor image was a spoofed URL. This seems like a bug for CSS folks since custom cursors presumably shouldn't be able to bust out of the web content area.

CSS owners, do you know who works on custom cursors?

[Monorail components: Blink>CSS]

### [Deleted User] (2022-08-29)

[Empty comment from Monorail migration]

### an...@chromium.org (2022-08-30)

I don't know.

[Monorail components: -Blink>CSS]

### fu...@chromium.org (2022-08-30)

There are means of trying to limit the cursor size in event_handler.cc:

https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/input/event_handler.cc;l=607-650

If we need to reduce that further in size, that would be the place, I assume.

[Monorail components: Blink>Input]

### [Deleted User] (2022-08-30)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@chromium.org (2022-09-08)

Assigning to csharrison based on blame for the code linked in #5 (and https://crbug.com/chromium/880863)

### cs...@chromium.org (2022-09-08)

I bisected this on macos to   https://chromium.googlesource.com/chromium/src/+log/dd8e0cd89d5988504b5ca95ad671105f11edd31b..8452a88148e5fca992e8ec02ec7b5c2e8386d1b3 using the following command:
python3 tools/bisect-builds.py -a mac-arm -b 1036826 -g 912729 --verify-range -- https://cr.kungfoo.net/style/cursor/abusive-cursor.html

My guess is that this regressed with https://chromium.googlesource.com/chromium/src/+/5867d6d62373c99f5b69fe93c1ac7a87d4fd7de2. I also have a repro hosted at https://cr.kungfoo.net/style/cursor/abusive-cursor.html.

cc cbiesinger, can you explain that change? My guess is that since this also repros on windows there is some shared logic that also changed in Windows, but I don't have a machine to do a bisect at the moment.

### cb...@chromium.org (2022-09-08)

vmpstr has taken over zoom-for-dsf bugs

### cb...@chromium.org (2022-09-08)

btw does this also reproduce on windows with a high-dpi display?

### vm...@chromium.org (2022-09-27)

This doesn't look to be zoom-for-dsf since https://cr.kungfoo.net/style/cursor/abusive-cursor.html reproduces on low-dpi linux as well

### dr...@chromium.org (2022-11-17)

[Empty comment from Monorail migration]

### es...@chromium.org (2023-01-20)

[Empty comment from Monorail migration]

### sa...@gmail.com (2023-03-24)

hello any updates?

### se...@chromium.org (2023-03-24)

[Empty comment from Monorail migration]

### fu...@chromium.org (2023-03-24)

[Empty comment from Monorail migration]

### sa...@gmail.com (2023-05-17)

hello any updates?

### cs...@chromium.org (2023-06-13)

+hferreiro: would you be able to own this bug? msw mentioned you were working on some cursor related things. I don't have the cycles to debug further right now.

### sa...@gmail.com (2023-07-07)

hello any updates?

### sa...@gmail.com (2023-07-21)

hello any updates?

### ms...@chromium.org (2023-08-09)

I have a local fix for some custom cursor image High-DPI >100% display scaling viewport escape issues. http://crrev.com/c/4730733

[Monorail components: UI>HighDPI]

### ms...@chromium.org (2023-08-11)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-08-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3b3c412dc32f81872e86337c998574e88036fd1b

commit 3b3c412dc32f81872e86337c998574e88036fd1b
Author: Mike Wasserman <msw@chromium.org>
Date: Fri Aug 11 16:54:59 2023

Fix custom cursor scaling logic for viewport checks

Fix some cases where custom cursor images escape the viewport.
- Apply display scale factor to fix High-DPI on all desktop OSes
- Use the ui::Cursor hotspot clamped to custom image dimensions
- Apply macOS's accessibility cursor scale factor, plus plumbing
  (other OS cursor scaling doesn't affect custom images for now)
  (note: we can skip plumbing if stale startup values suffice)

Update and expand the relevant Blink unit test.

Fixed: 1357442, 1455005
Change-Id: Id4f0d617210cdabdd616627217e661cc462f2291
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4730733
Commit-Queue: Mike Wasserman <msw@chromium.org>
Reviewed-by: Robert Sesek <rsesek@chromium.org>
Reviewed-by: Jeremy Roman <jbroman@chromium.org>
Reviewed-by: Henrique Ferreiro <hferreiro@igalia.com>
Reviewed-by: Ken Buchanan <kenrb@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1182635}

[modify] https://crrev.com/3b3c412dc32f81872e86337c998574e88036fd1b/content/browser/renderer_host/render_widget_host_view_mac.h
[modify] https://crrev.com/3b3c412dc32f81872e86337c998574e88036fd1b/third_party/blink/public/common/frame/frame_visual_properties.h
[modify] https://crrev.com/3b3c412dc32f81872e86337c998574e88036fd1b/third_party/blink/common/widget/visual_properties_mojom_traits.cc
[modify] https://crrev.com/3b3c412dc32f81872e86337c998574e88036fd1b/third_party/blink/renderer/core/frame/web_frame_widget_impl.cc
[modify] https://crrev.com/3b3c412dc32f81872e86337c998574e88036fd1b/third_party/blink/renderer/core/frame/remote_frame.h
[modify] https://crrev.com/3b3c412dc32f81872e86337c998574e88036fd1b/content/browser/renderer_host/render_widget_host_view_mac.mm
[modify] https://crrev.com/3b3c412dc32f81872e86337c998574e88036fd1b/third_party/blink/public/common/frame/frame_visual_properties_mojom_traits.h
[modify] https://crrev.com/3b3c412dc32f81872e86337c998574e88036fd1b/ui/base/cocoa/cursor_utils.mm
[modify] https://crrev.com/3b3c412dc32f81872e86337c998574e88036fd1b/third_party/blink/renderer/core/frame/remote_frame.cc
[add] https://crrev.com/3b3c412dc32f81872e86337c998574e88036fd1b/ui/base/cocoa/cursor_accessibility_scale_factor_observer.h
[modify] https://crrev.com/3b3c412dc32f81872e86337c998574e88036fd1b/third_party/blink/renderer/core/input/event_handler.cc
[modify] https://crrev.com/3b3c412dc32f81872e86337c998574e88036fd1b/third_party/blink/common/frame/frame_visual_properties_mojom_traits.cc
[modify] https://crrev.com/3b3c412dc32f81872e86337c998574e88036fd1b/third_party/blink/public/common/widget/visual_properties.h
[modify] https://crrev.com/3b3c412dc32f81872e86337c998574e88036fd1b/third_party/blink/public/mojom/frame/frame_visual_properties.mojom
[modify] https://crrev.com/3b3c412dc32f81872e86337c998574e88036fd1b/third_party/blink/common/widget/visual_properties.cc
[modify] https://crrev.com/3b3c412dc32f81872e86337c998574e88036fd1b/third_party/blink/renderer/core/input/event_handler_test.cc
[modify] https://crrev.com/3b3c412dc32f81872e86337c998574e88036fd1b/ui/base/BUILD.gn
[modify] https://crrev.com/3b3c412dc32f81872e86337c998574e88036fd1b/ui/base/cocoa/cursor_utils.h
[modify] https://crrev.com/3b3c412dc32f81872e86337c998574e88036fd1b/third_party/blink/public/mojom/widget/visual_properties.mojom
[modify] https://crrev.com/3b3c412dc32f81872e86337c998574e88036fd1b/third_party/blink/renderer/core/input/event_handler.h
[add] https://crrev.com/3b3c412dc32f81872e86337c998574e88036fd1b/ui/base/cocoa/cursor_accessibility_scale_factor_observer.mm
[modify] https://crrev.com/3b3c412dc32f81872e86337c998574e88036fd1b/content/browser/renderer_host/render_widget_host_impl.cc
[modify] https://crrev.com/3b3c412dc32f81872e86337c998574e88036fd1b/third_party/blink/public/common/widget/visual_properties_mojom_traits.h


### [Deleted User] (2023-08-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-12)

[Empty comment from Monorail migration]

### sa...@gmail.com (2023-09-09)

Hello any updates?

### am...@chromium.org (2023-09-11)

Thanks for the ping. The VRP Panel was recently on hiatus for two-weeks. Reward decisions are made in the order of critical and high -> low severity. This issue will be evaluated at a future VRP Panel session. Thank you for your patience in the meantime. 

### sa...@gmail.com (2023-09-12)

thank you amy for the information...

### am...@google.com (2023-09-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-21)

Congratulations Hafiizh! The Chrome VRP Panel has decided to award you $1,000 for this report based on the minimal impact and opportunity to exploit this issue in a real world scenario. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-09-22)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-09)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-11)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-12-04)

Hi Hafiizh, we consider attachments/POCs and all analysis included with reports to be an integral part of the report (https://g.co/chrome/vrp/#investigating-and-reporting-bugs), so I've undeleted them. Thanks! 

### sa...@gmail.com (2023-12-04)

Hi amy im sorry for deletion because my vps hit by several DDoS attacks because I put POC on my VPS 
server (on other my report but not this report). 

Im sorry for deletion this is my fault. No problem if it all to be  undeleted.


### is...@google.com (2023-12-04)

This issue was migrated from crbug.com/chromium/1357442?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Input, UI>HighDPI]
[Monorail mergedwith: crbug.com/chromium/1385726]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060702)*
