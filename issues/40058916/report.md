# Security: Extension can move window off screen, user can interact with sensitive UI using keyboard without being aware

| Field | Value |
|-------|-------|
| **Issue ID** | [40058916](https://issues.chromium.org/issues/40058916) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions>API |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | em...@chromium.org |
| **Created** | 2022-02-27 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

An extension can create or move any window outside of the screen, and the window can still receive keyboard input. This can hide user interactions using keyboard input with sensitive browser UI and web pages. I've identified a myriad of affected areas, and there are potentially other areas which may have similar or greater severity impacts. I've verified on Windows + Chrome OS. The extension does not require any permissions.

On Windows, for most scenarios, the window position must be just off screen which is sufficient to completely hide the window from the user. For the screen share dialog, external protocol dialog, and possibly other dialogs, the window position does not matter (we can set coordinates thousands of pixels off screen).

On Chrome OS, the window position does not matter (we can set coordinates thousands of pixels off screen).

Verified impacts ("without user awareness" implied unless otherwise specified):

\* Screen share dialog: Share screen with 3 keypresses. Only mitigation is the small widget/notification after sharing that says "example.com is sharing your screen".

\* Permssion prompts: Allow permission for origin with 3 keypresses (4 on ChromeOS). e.g. camera, microphone, location, etc.

\* Autofill: Open autofill prompt, select item, and fill autofill entry into page with 2 keypresses. The browser fills in multiple fields at once with this interaction. Can obtain name, address, and credit card info.

\* Payment request: Complete payment request with a few keypresses (as few as 2 keypresses; depends on payment flow).

\* Web pages: Interact with any page. Can perform sensitive actions on logged-in or intranet pages.

\* chrome:// pages: Interact with any chrome:// page.  

\* chrome://settings/security contains settings related to Safe Browsing, and other chrome://settings page may have sensitive settings.  

\* chrome://flags/ can toggle features which may affect security with 3 keypresses.

\* External protocols: Allow website to open app with 2 keypresses. Also can enable "always allow {origin} to open links of this type..." to allow multi-step or future drive-by external protocol launches.

\* Downloads: Open downloads in download bar with 2 keypresses, or in chrome://downloads with a few keypresses (does not bypass any OS-level protection)

\* Pointer lock: Obtain pointer lock without notification. Might be useful when combined with other bugs.

\* Copy/paste: Can obtain page content with Ctrl+A, Ctrl+C, Ctrl+V from most web pages or chrome:// pages. This is an issue if the page has sensitive content.  

\* chrome://predictors/  

\* chrome://local-state/ (os\_crypt.encrypted\_key?)  

\* chrome://prefs-internals/ (gaia, sync entries?)  

\* And others which provide potentially sensitive info such as frequent sites, recent sites/URLs, installed extensions, etc.

Mitigated impact:

\* Installing extension from Chrome Web Store requires a lot of keypresses (at least 7), and the confirmation dialog always appears on screen even if window is off screen.

**VERSION**  

Chrome Version: 98.0.4758.102 (Official Build) (64-bit) (cohort: Stable), 101.0.4912.0 Canary  

Operating System: Windows 10 Version 20H2 (Build 19042.1526)

Chrome Version: 98.0.4758.107 Stable, 93.0.4577.85 Stable  

Operating System: Chrome OS 14388.61.0, 14092.57.0

**REPRODUCTION CASE**  

Initial setup:

1. Install attached extension: manifest.json + bg.js

All PoC scenarios:

1. Set the scenario variable in bg.js.  
   
   Available scenarios: permission, screenshare, download, payment, autofill, autofill-creditcard, externalprotocol, flags, extension
2. Reload the extension.
3. Follow instructions shown in the extension-created tab.
4. Once the extension reveals the off-screen window, observe the interaction results.

Observed: Window is off screen and not visible to user. Off-screen window accepts keyboard input in sensitive browser UI and web pages.  

Expected: Sensitive browser UI is always visible to user, or window does not accept keyboard input when not properly visible to user.

Optional:  

You can try different window positions to see that on Windows most scenarios don't work with larger off-screen positions.  

To observe real-time keyboard input interaction results, you can keep the window on screen by commenting-out the windows.update() call. This is also useful for debugging or developing new scenarios.  

I've verified the other scenarios in internal PoCs. You can update the attached PoC to test the other scenarios if you'd like.

**CREDIT INFORMATION**  

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [manifest.json](attachments/manifest.json) (text/plain, 265 B)
- [bg.js](attachments/bg.js) (text/plain, 3.0 KB)
- [extension-interaction-offscreen.mp4](attachments/extension-interaction-offscreen.mp4) (video/mp4, 2.7 MB)
- [offscreen.html](attachments/offscreen.html) (text/plain, 3.7 KB)
- [offscreen-instructions.html](attachments/offscreen-instructions.html) (text/plain, 1.7 KB)
- [manifest-offscreen-bookmark-xss.json](attachments/manifest-offscreen-bookmark-xss.json) (text/plain, 346 B)
- [bg-offscreen-bookmark-xss.js](attachments/bg-offscreen-bookmark-xss.js) (text/plain, 1.7 KB)
- [offscreen.html](attachments/offscreen.html) (text/plain, 4.5 KB)
- [offscreen-instructions.html](attachments/offscreen-instructions.html) (text/plain, 1.9 KB)
- [offscreen-bookmark-xss.mp4](attachments/offscreen-bookmark-xss.mp4) (video/mp4, 1.2 MB)

## Timeline

### [Deleted User] (2022-02-27)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2022-02-27)

Attached remote files.

### al...@alesandroortiz.com (2022-03-01)

Additional verified impact:
* XSS via bookmark + address bar: Run attacker-provided JavaScript on any web page with 4 or 6 keypresses.

As described in https://crbug.com/chromium/1301874, an extension with only bookmarks permission can create or update a bookmark with a javascript: URL (this is supported behavior). A user can also run a javascript: bookmark from the address bar (probably unsafe). That issue uses several techniques to convince the user to select the malicious bookmark in a fully-visible window with minimal suspicion (unsafe).

However, we can get rid of all the stealth techniques from https://crbug.com/chromium/1301874 and replace them with an off-screen window to achieve the same result. This is easier to perform since the user has no awareness whatsoever, while in https://crbug.com/chromium/1301874 there's some user awareness.

I've attached a separate PoC extension which uses the bookmarks permission, but otherwise is roughly the same as the PoC from https://crbug.com/chromium/1301203#c0. I've also attached the updated offscreen.html and offscreen-instructions.html to include additional logic for this PoC. (I've also updated the hosted versions.)

REPRODUCTION CASE
Initial setup:
1. Install attached extension: manifest-offscreen-bookmark-xss.json + bg-offscreen-bookmark-xss.js. Rename the manifest file to manifest.json.

Off-screen window bookmark XSS scenario:
1. Reload the extension to start the PoC. The next steps are also shown as instructions in the extension-created tab.
2. Press Tab, Tab, Tab to focus on the address bar.
3. Press Ctrl+V to paste the bookmark name (written into clipboard by attacker page).
4. Press Tab to select the bookmark item in the address bar dropdown.
5. Press Enter to navigate the bookmark item.
6. Once the extension reveals the off-screen window, observe the interaction results.

Observed: Same as https://crbug.com/chromium/1301203#c0. In this specific scenario, bookmark runs JavaScript payload on target origin.
Expected: Same as https://crbug.com/chromium/1301203#c0. In this specific scenario, bookmark does not run JavaScript payload.

(Note to self: Avoid disclosing this crbug before https://crbug.com/chromium/1301874 since this comment includes details of the other crbug.)

### dc...@chromium.org (2022-03-02)

[Empty comment from Monorail migration]

### dc...@chromium.org (2022-03-02)

It probably makes sense for any restrictions on window.open() to also apply here.

msw@, IIRC, there are some restrictions for window.open() right? e.g. there are minimum sizes, and (i assume) it's not possible to position windows wholly offscreen?

[Monorail components: Platform>Extensions>API]

### [Deleted User] (2022-03-02)

[Empty comment from Monorail migration]

### ms...@google.com (2022-03-02)

Our window.open()|moveTo()|moveBy()|resizeTo()|resizeBy() should never permit a placement to be offscreen or partly offscreen.
window.open() by default clamps placements to be entirely within the current screen's available space.
With the new window-placement permission, we permit placement on another screen's available space.
There are indeed also minimum size requirements.

### dc...@chromium.org (2022-03-03)

msw@/avi@: do you know if these requirements are documented anywhere?

### [Deleted User] (2022-03-03)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rd...@chromium.org (2022-03-03)

As dcheng@ mentioned, I'd suggest we apply similar (or identical) restrictions to extension windows being created.  I could see us being slightly more flexible (say, maybe >50% of the window needs to be visible?), but extensions should not be able to create entirely offscreen windows.

avi@, msw@, if you can include any links to specs and/or code enforcement, it'd be helpful.

### ms...@chromium.org (2022-03-04)

Here's the best info I found with a quick search, which describe clamping in a user-agent defined manner:
https://developer.mozilla.org/en-US/docs/Web/API/Window/open#note_on_position_and_dimension_error_correction
https://drafts.csswg.org/cssom-view/#the-features-argument-to-the-open()-method
https://drafts.csswg.org/cssom-view/#dom-window-moveto

Here's the code in Blink (ChromeClientImpl::CalculateWindowRectWithAdjustment) and Chrome (AdjustRequestedWindowBounds):
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/page/chrome_client_impl.cc;drc=d66537237772201bb97d69d94c0d82acabe7fee0;l=1300
https://source.chromium.org/chromium/chromium/src/+/main:content/browser/web_contents/web_contents_impl.cc;drc=4289e8d842107e2f99d6d2213ffe52dfa4677646;l=484

### rd...@chromium.org (2022-03-10)

Thanks for the pointers, msw@!  I think we'll want to do something conceptually similar, but slightly different than those.  In particular, the WebContents method says:

// The bounds may not extend
// outside a single screen's work area, and the |host| requires permission to
// specify bounds on a screen other than its current screen.

But I think both of these would be fine for extensions (and may well be relied upon for things like session managers).  But we should be able to use somewhat similar logic to tell if a window's requested bounds are beyond the full "screen" (which may be multiple displays).  One solution that comes to mind would be requiring >=50% of the window to be in a single display; however, I wonder if this would break valid use cases with multi-display setup (like three monitors side by side where an extension wants the window to be full-screen across all three).  msw@, do you know if Screen / Display have any handy methods that would help us determine whether enough of the window is on valid displays, or is the best way to just iterate over all displays in the screen to determine?

emiliapaz@, do you think you have the bandwidth to work with msw@ to take this one on?

### [Deleted User] (2022-03-16)

emiliapaz: Uh oh! This issue still open and hasn't been updated in the last 16 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ms...@chromium.org (2022-03-16)

RE #12: Those use cases seem reasonable for a powerful extension (and maybe eventually for a powerful web platform API). You'll likely need to iterate over display::Screen::GetAllDisplays() to determine the overall on-screen portion of the requested window bounds. You might want to ensure that some portion of the window's titlebar is on screen too (if the window has a titlebar for identity, user controls and dragging, etc.). I'm happy to help with code review or other questions here.

### em...@chromium.org (2022-03-18)

Showing the popup only when it appears at least 50% on the current displays seems reasonable to me. The question then is, what happens if bounds do not intersect 50% with the displays? Do we a) leave the popup at its current position or b) get the closest display matching and adjust to fit (similar to [1])?

[1] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/web_contents/web_contents_impl.cc;l=484-492;drc=28f8c4edef0c91c02a15ec3bd26f6f38a2d256ca;bpv=1;bpt=1

### gi...@appspot.gserviceaccount.com (2022-03-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d51682b36adc22496f45a8111358a8bb30914534

commit d51682b36adc22496f45a8111358a8bb30914534
Author: Emilia Paz <emiliapaz@chromium.org>
Date: Tue Mar 29 15:40:06 2022

[Extensions] Display window only when its bounds intersect the displays

Windows should only be displayed when they intersect the displays in a
meaningful manner (in this case, window should be visible at least 50%).
Otherwise, the window will be displayed in the current default.

This prevents for windows to be created or moved outside the displays,
and potentially been exploited.

Screencast: https://drive.google.com/file/d/1dTJdC1OtQek4n6ok0sOfccbEr8H0Ah3U/view?usp=sharing

Bug: 1301203
Change-Id: I306d837d12a79a99039e5336792a72cbe20ea57d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3536833
Reviewed-by: Mike Wasserman <msw@chromium.org>
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
Commit-Queue: Emilia Paz <emiliapaz@chromium.org>
Cr-Commit-Position: refs/heads/main@{#986515}

[modify] https://crrev.com/d51682b36adc22496f45a8111358a8bb30914534/chrome/browser/extensions/api/tabs/tabs_test.cc
[modify] https://crrev.com/d51682b36adc22496f45a8111358a8bb30914534/chrome/browser/extensions/api/tabs/tabs_constants.cc
[modify] https://crrev.com/d51682b36adc22496f45a8111358a8bb30914534/chrome/browser/extensions/api/tabs/tabs_constants.h
[modify] https://crrev.com/d51682b36adc22496f45a8111358a8bb30914534/chrome/browser/extensions/api/tabs/tabs_api.cc


### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### em...@chromium.org (2022-05-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-19)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### gm...@google.com (2022-05-25)

[Empty comment from Monorail migration]

### rz...@google.com (2022-05-26)

[Empty comment from Monorail migration]

### rz...@google.com (2022-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-26)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rd...@chromium.org (2022-05-26)

This CL has the possibility of breaking extension functionality.  Due to this, we decided not to merge to previous branches.  I think we should avoid merging to M96 as well for the same reason.

### rz...@google.com (2022-05-27)

Thanks rdevlin, recommending not to merge:

1. Just https://crrev.com/c/3668845
2. Low, just a few functions/tests conflicts around the added code
3. https://crbug.com/1301203#c27
4. No, as per https://crbug.com/1301203#c27

### gm...@google.com (2022-05-31)

[Empty comment from Monorail migration]

### am...@google.com (2022-06-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-06-01)

Congratulations, Alesandro! The VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts and nice work! 

### al...@alesandroortiz.com (2022-06-01)

Thanks for the reward!

The 50% check in https://crbug.com/chromium/1301203#c27 doesn't fully resolve the issue on Windows and potentially other platforms (based on the video in https://crbug.com/chromium/1301203#c27, it seems resolved on MacOS, but I can't verify myself).

I'll file a new report later today with updated PoCs that still repro and add a comment with the link to the new crbug.

### al...@alesandroortiz.com (2022-06-01)

Meant commit in https://crbug.com/chromium/1301203#c16, not https://crbug.com/chromium/1301203#c27.

### al...@alesandroortiz.com (2022-06-02)

Filed https://crbug.com/chromium/1331162 for bypass mentioned in https://crbug.com/chromium/1301203#c32. Some scenarios likely work on all desktop platforms (including MacOS), other scenarios likely work on many desktop platforms (Windows, Chrome OS, maybe others).

### am...@google.com (2022-06-05)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1301203?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058916)*
