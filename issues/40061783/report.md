# Security: Permissions Prompt UI spoof through a custom CSS cursor

| Field | Value |
|-------|-------|
| **Issue ID** | [40061783](https://issues.chromium.org/issues/40061783) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser, UI>Browser>Permissions>Prompts |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | re...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2022-11-17 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

CSS allows setting custom mouse cursors up to 128x128 in size. There are checks in place to prevent this from covering up the browser UI, but there isn't one for the permission prompt (UI>Browser>Permissions>Prompts). A maliciously crafted website can overlay custom content on top of the permission prompt and trick a user into accepting unwanted prompts.

A prompt popping up hides the custom cursor, but it can be bypassed by refocusing the main window. In my poc I've achieved that by popping up a popup window for 100ms and then closing it, refocusing the main window.

I think that the best approach to fixing this issue would be to disallow all custom cursors while a permissions prompt is open.

**VERSION**  

Chrome Version: 107.0.5304.107 Stable, 109.0.5410.0 Dev  

Operating System: Windows 10/11, macOS (couldn't repro on Linux)

**REPRODUCTION CASE**

1. Download the poc, as well as the png files, and host them in a secure context.
2. Visit the site on a Windows computer.
3. Click the button on the site.
4. You will now see the permissions prompt with the cursor overlay on top of it, switching the "Allow" and "Block" buttons around.

I have also included a demonstration video of the issue.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Jasper Rebane (popstonia)

## Attachments

- [demo.mp4](attachments/demo.mp4) (video/mp4, 999.8 KB)
- [poc.html](attachments/poc.html) (text/plain, 1.9 KB)
- [overlay.png](attachments/overlay.png) (image/png, 1.3 KB)
- [cursor.png](attachments/cursor.png) (image/png, 322 B)
- [1385714.webm](attachments/1385714.webm) (video/webm, 605.1 KB)
- [cursor.png](attachments/cursor.png) (image/png, 131 B)

## Timeline

### [Deleted User] (2022-11-17)

[Empty comment from Monorail migration]

### dr...@chromium.org (2022-11-17)

The offsets, sizing, and color scheme are all wrong for my machine, but I do get some drawing over the permissions prompt in M107. I'm assuming a more complete implementation of the PoC could figure out the needed size/offset, but it would still be pretty finicky. The fake buttons visibly move around with the mouse cursor, and once the mouse is over the permission prompt, we begin using the regular cursor, so the overlays disappear. This is all visible in your PoC video, so I don't think my reproduction is incomplete. Because of these caveats, giving low severity.

Permissions owners - is this something you can take a look at?

[Monorail components: UI>Browser>Permissions>Prompts]

### [Deleted User] (2022-11-17)

[Empty comment from Monorail migration]

### re...@gmail.com (2022-11-17)

The sizing should be correct unless on a HiDPI display (could be worked around with window.devicePixelRatio) or Linux (known to have cursor size issues). From what I understand, there are only two color schemes for the prompt and they are based on the desktop theme (can be detected with window.matchMedia) unless in Incognito (always dark). I don't think the visual matching would be a problem with more work put into the PoC.

The cursor being finnicky and disappearing once on the permissions prompt is the right reproduction and not possible to work around. I intentionally placed the button close to the prompt so that the impact of that would be minimal and it would be easy to click on the wrong button without noticing, but I understand that it's still a bit unconvincing.

### [Deleted User] (2022-11-18)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### an...@chromium.org (2022-11-28)

[Empty comment from Monorail migration]

### tu...@chromium.org (2022-11-29)

So the concern is the time switching between the overlaid cursor and the real button is too short and the user could not recognize that. I also think that is quite low severity because user could easy be aware of the finnicky cursor. I am skeptical what could we do to make it better here, delay after cursor switching? 

### re...@gmail.com (2022-11-29)

I think custom cursors should not be allowed to render at all while a permissions prompt is visible. This is already done in other similar cases where the cursor could affect the browser UI, for example if you get close enough to the URL bar for the custom cursor to overlap it, it's switched to the system cursor.

I recommend looking at https://crbug.com/chromium/1246188, which goes over the topic a bit more in-depth and links additional issues/resources.

### tu...@chromium.org (2022-11-29)

Yeah, maybe we can do the same with other ticket, the cursor's rect will intersect with prompt UI, then switch to the system cursor. It would prevent us from overlaying fake cursor

### [Deleted User] (2022-11-29)

[Empty comment from Monorail migration]

### an...@chromium.org (2023-01-11)

[Empty comment from Monorail migration]

### an...@chromium.org (2023-01-12)

Added more people that might have input


### ms...@chromium.org (2023-01-12)

I tested with the attached solid red 128x128 cursor (and `python3 -m http.server`) with
  document.body.style.cursor = `url('http://localhost:8000/cursor.png') 128 128, auto`;

If Chrome already tries to disallow custom cursor images from overlapping browser UI, then it's not WAI.
Custom cursors covering the URL, page info icon, etc. seems potentially more severe than the initial report. 
Does anyone have a pointer to the code or issues discussing that functionality? (I'm not aware of that offhand)

I agree that implementing or fixing that behavior (for top-chrome, bubbles, dialogs, menus, download bar, etc.) seems appropriate.

[Monorail components: Security UI>Browser]

### re...@gmail.com (2023-01-12)

It seems like you're on a Mac with a HiDPI display. That is a separate bug that only occurs on HiDPI screens. I reported it in https://crbug.com/chromium/1385726 some time ago, but it was closed as a duplicate for an issue I don't have view access on.

### ms...@chromium.org (2023-01-12)

Thanks for pointing that out. If anyone can CC me on https://crbug.com/chromium/1385726, I'd be interested to follow along.
I tested again on a non-Mac-HighDPI display and it seems like the code for https://crbug.com/chromium/880863 does actually prevent such custom cursors from overlapping top-chrome and the bottom download bar:
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/input/event_handler.cc;drc=23cacdc8c92193f2089a4eb10a504d1dda060475;l=627

So, *this* defect mainly applies to secondary Chrome UI surfaces that overlap the content area (at least those that don't take input focus from content).
I've been able to repro with: omnibox dropdown, three-dot menu, find bar, bookmark folders, and even `javascript:prompt('foo')` repros flakily.

It may be reasonable to avoid showing custom cursors when any such transient ui surfaces would be obscured, or perhaps even regardless of overlap.

### an...@chromium.org (2023-01-19)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-03-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5608bda8ba25f912561e81cdc35bc7f3796682fb

commit 5608bda8ba25f912561e81cdc35bc7f3796682fb
Author: Andy Paicu <andypaicu@chromium.org>
Date: Fri Mar 03 15:09:20 2023

Disallow custom cursors when a permission prompt is displayed

Bug: 1385714
Change-Id: I73ee22d0d8ad331efc5cb40ce800a47939c66663
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4154719
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: Andy Paicu <andypaicu@chromium.org>
Reviewed-by: Elias Klim <elklm@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1112775}

[modify] https://crrev.com/5608bda8ba25f912561e81cdc35bc7f3796682fb/chrome/browser/ui/views/permissions/permission_prompt_bubble_view_unittest.cc
[modify] https://crrev.com/5608bda8ba25f912561e81cdc35bc7f3796682fb/chrome/browser/ui/views/permissions/chip_controller.h
[modify] https://crrev.com/5608bda8ba25f912561e81cdc35bc7f3796682fb/components/permissions/permission_prompt.h
[add] https://crrev.com/5608bda8ba25f912561e81cdc35bc7f3796682fb/content/public/test/cursor_utils.cc
[modify] https://crrev.com/5608bda8ba25f912561e81cdc35bc7f3796682fb/content/public/browser/web_contents.h
[modify] https://crrev.com/5608bda8ba25f912561e81cdc35bc7f3796682fb/content/test/test_render_view_host.cc
[modify] https://crrev.com/5608bda8ba25f912561e81cdc35bc7f3796682fb/chrome/browser/ui/views/permissions/permission_prompt_bubble.h
[modify] https://crrev.com/5608bda8ba25f912561e81cdc35bc7f3796682fb/chrome/browser/ui/permission_bubble/permission_bubble_browser_test_util.cc
[modify] https://crrev.com/5608bda8ba25f912561e81cdc35bc7f3796682fb/chrome/browser/ui/permission_bubble/permission_bubble_browser_test_util.h
[modify] https://crrev.com/5608bda8ba25f912561e81cdc35bc7f3796682fb/chrome/browser/ui/views/permissions/permission_prompt_bubble_view_browsertest.cc
[modify] https://crrev.com/5608bda8ba25f912561e81cdc35bc7f3796682fb/chrome/browser/ui/views/permissions/permission_prompt_bubble.cc
[modify] https://crrev.com/5608bda8ba25f912561e81cdc35bc7f3796682fb/content/test/test_render_view_host.h
[modify] https://crrev.com/5608bda8ba25f912561e81cdc35bc7f3796682fb/chrome/browser/ui/views/permissions/permission_prompt_bubble_view.cc
[modify] https://crrev.com/5608bda8ba25f912561e81cdc35bc7f3796682fb/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/5608bda8ba25f912561e81cdc35bc7f3796682fb/content/browser/renderer_host/cursor_manager.cc
[modify] https://crrev.com/5608bda8ba25f912561e81cdc35bc7f3796682fb/components/permissions/permission_request_manager.cc
[modify] https://crrev.com/5608bda8ba25f912561e81cdc35bc7f3796682fb/chrome/browser/ui/views/permissions/permission_chip_unittest.cc
[modify] https://crrev.com/5608bda8ba25f912561e81cdc35bc7f3796682fb/content/browser/renderer_host/cursor_manager_unittest.cc
[modify] https://crrev.com/5608bda8ba25f912561e81cdc35bc7f3796682fb/content/browser/web_contents/web_contents_impl.h
[modify] https://crrev.com/5608bda8ba25f912561e81cdc35bc7f3796682fb/content/test/BUILD.gn
[modify] https://crrev.com/5608bda8ba25f912561e81cdc35bc7f3796682fb/components/permissions/permission_request_manager.h
[modify] https://crrev.com/5608bda8ba25f912561e81cdc35bc7f3796682fb/chrome/browser/ui/views/permissions/chip_controller.cc
[modify] https://crrev.com/5608bda8ba25f912561e81cdc35bc7f3796682fb/content/public/browser/BUILD.gn
[modify] https://crrev.com/5608bda8ba25f912561e81cdc35bc7f3796682fb/content/browser/renderer_host/cursor_manager.h
[add] https://crrev.com/5608bda8ba25f912561e81cdc35bc7f3796682fb/content/public/test/cursor_utils.h


### an...@chromium.org (2023-03-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-08)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-17)

Congratulations, Jasper! The VPR Panel has decided to award you $3,000 for this report. We found this discovery and POC to be quite clever! (Some of us may have watched your demonstration video more than once :)) Thank you so much for your efforts in discovering and reporting this issue to us -- great work! 

### am...@google.com (2023-03-17)

[Empty comment from Monorail migration]

### re...@gmail.com (2023-03-21)

That's awesome news, thank you so much :)

### am...@chromium.org (2023-04-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-05-02)

[Empty comment from Monorail migration]

### pg...@google.com (2023-05-02)

[Empty comment from Monorail migration]

### an...@chromium.org (2023-05-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-06-14)

This issue was migrated from crbug.com/chromium/1385714?no_tracker_redirect=1

[Multiple monorail components: Security, UI>Browser, UI>Browser>Permissions>Prompts]
[Monorail mergedwith: crbug.com/chromium/1445459]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061783)*
