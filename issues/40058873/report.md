# Security: Extension popup can render over permission prompts and screen share dialog

| Field | Value |
|-------|-------|
| **Issue ID** | [40058873](https://issues.chromium.org/issues/40058873) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2022-02-23 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

An extension can show the extension's popup over a permission prompt or screen share dialog, which allows the extension to spoof parts of the prompt's UI that show origin and requested permissions. An extension can perform this attack using either a specially-crafted page without any sensitive permissions, or a content script injected into any page if they have appropriate permissions.

User interaction details:  

Permission prompts require user activation, therefore a single user interaction is required.  

Screen share dialogs don't require user activation, therefore no user interaction is required. The PoC still requests user activation to avoid showing the user an unexpected dialog, but I have verified the screen share dialog spoofs are possible without user interaction.

In Chromium versions without chrome.action.openPopup() available (v98 Stable; also works in newer versions), the user must open the extension popup using a keyboard shortcut (pre-defined in the extension manifest). For permission prompt PoCs, this keyboard input also provides the page with user activation to show the permission prompt. This single keyboard interaction shows both the permission prompt and the extension popup.

In Chromium versions with chrome.action.openPopup() available (v101 Canary, v100 Dev), the extension can arbitrarily open the extension popup. For permission prompts, the page must still obtain user activation to show the permission prompt, but this is easier to obtain since it can be a mouse click or almost any keyboard input. For the screen share dialog, no user interaction is required to perform the attack; both the screen share dialog and the extension popup can be opened arbitrarily.

Potential existing protections:  

There seems to be existing protections which attempt to prevent the extension popup and the permission prompt/screen share dialog from appearing simultaneously if one is already open. The PoCs bypass this by opening them simultaneously, bypassing these potential protections. You can verify this by adjusting the timings in the PoCs.  

For permission prompts, if we call getUserMedia() after extension popup is opened, the permission prompt is not shown until extension prompt is closed by user.  

For screen share dialogs, if we call getDisplayMedia() after extension popup is opened, the extension popup is closed by the browser.

Other dialogs may be similarly affected. Based on quick tests the USB, HID, and similar-style dialogs appear to behave safely.

**VERSION**  

Chrome Version: 98.0.4758.102 (Official Build) (64-bit) (cohort: Stable), 101.0.4902.0 Canary  

Operating System: Windows 10 Version 20H2 (Build 19042.1526)

**REPRODUCTION CASE**  

Initial setup for keyboard PoCs (v98 Stable; also works in newer versions):

1. Install attached extension: manifest-keyboard.json + bg-keyboard.js + popup.html + popup-screenshare.html. Rename the manifest file to manifest.json

Initial setup for chrome.action.openPopup() PoCs (v101 Canary, v100 Dev):

1. Install attached extension: manifest-openPopup.json + bg-openPopup.js + popup.html + popup-screenshare.html. Rename the manifest file to manifest.json

PoC for permission prompt + keyboard PoC:

1. Reload manifest-keyboard.json extension using chrome://extensions
2. Press Ctrl+A when requested by the attacker page.

PoC for permission prompt + openPopup() PoC:

1. Reload manifest-openPopup.json extension using chrome://extensions
2. Click on the gray box in the attacker page.

PoC for screen share dialog + keyboard PoC:

1. Reload manifest-keyboard.json extension using chrome://extensions
2. Press Ctrl+A when requested by the attacker page.

PoC for screen share dialog + openPopup() PoC:

1. Reload manifest-openPopup.json extension using chrome://extensions  
   
   No user interaction required: Wait for attack to run.
2. Optional: Click on the gray box in the attacker page to run same attack with user interaction.

Observed: Extension popup renders simultaneously over permission prompt, screen share dialog, or other sensitive browser UI.  

Expected: Extension popup renders under permission prompt, screen share dialog, or other sensitive browser UI. Or one of the conflicting UI elements is closed automatically before showing the other UI elements. Or any other safer behavior.

**CREDIT INFORMATION**  

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [popup.html](attachments/popup.html) (text/plain, 890 B)
- [popup-screenshare.html](attachments/popup-screenshare.html) (text/plain, 430 B)
- [bg-openPopup.js](attachments/bg-openPopup.js) (text/plain, 2.3 KB)
- [extension-over-prompt.html](attachments/extension-over-prompt.html) (text/plain, 1.9 KB)
- [extension-over-prompt-openPopup.html](attachments/extension-over-prompt-openPopup.html) (text/plain, 2.1 KB)
- [manifest-keyboard.json](attachments/manifest-keyboard.json) (text/plain, 494 B)
- [bg-keyboard.js](attachments/bg-keyboard.js) (text/plain, 1.5 KB)
- [manifest-openPopup.json](attachments/manifest-openPopup.json) (text/plain, 957 B)
- [PoC-keyboard-v98-Stable.mp4](attachments/PoC-keyboard-v98-Stable.mp4) (video/mp4, 4.4 MB)
- [PoC-openPopup-v101-Canary.mp4](attachments/PoC-openPopup-v101-Canary.mp4) (video/mp4, 4.1 MB)
- [Screenshot from 2022-02-23 13-16-02.png](attachments/Screenshot from 2022-02-23 13-16-02.png) (image/png, 69.8 KB)
- [popup.html](attachments/popup.html) (text/plain, 890 B)
- [popup-screenshare.html](attachments/popup-screenshare.html) (text/plain, 430 B)
- [manifest-openPopup.json](attachments/manifest-openPopup.json) (text/plain, 974 B)
- [bg-openPopup.js](attachments/bg-openPopup.js) (text/plain, 2.2 KB)
- [extension-over-prompt-openPopup-june2022.html](attachments/extension-over-prompt-openPopup-june2022.html) (text/plain, 2.3 KB)
- [PoC-openPopup-v104-Canary-June2022.mp4](attachments/PoC-openPopup-v104-Canary-June2022.mp4) (video/mp4, 4.0 MB)
- [popup.html](attachments/popup.html) (text/plain, 890 B)
- [popup-screenshare.html](attachments/popup-screenshare.html) (text/plain, 430 B)
- [manifest.json](attachments/manifest.json) (text/plain, 926 B)
- [bg-keyboard.js](attachments/bg-keyboard.js) (text/plain, 1.8 KB)
- [extension-over-prompt-september2022.html](attachments/extension-over-prompt-september2022.html) (text/plain, 2.2 KB)
- [PoC-keyboard-v108-Canary.mp4](attachments/PoC-keyboard-v108-Canary.mp4) (video/mp4, 3.9 MB)
- [bg-keyboard.js](attachments/bg-keyboard.js) (text/plain, 1.8 KB)
- [extension-icon-bug.png](attachments/extension-icon-bug.png) (image/png, 4.1 KB)
- [Screen Recording 2024-08-14 155735.mp4](attachments/Screen Recording 2024-08-14 155735.mp4) (video/mp4, 28.2 MB)

## Timeline

### al...@alesandroortiz.com (2022-02-23)

Attachments in comment since Monorail kept returning "500 Server Error" responses when submitting with any attachment (just like when I tried submitting https://crbug.com/chromium/1287364).

### al...@alesandroortiz.com (2022-02-23)

Video recordings of PoCs attached.

### [Deleted User] (2022-02-23)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2022-02-23)

The implementation of chrome.action.openPopup() is being tracked in https://crbug.com/chromium/1245093. Based on public docs linked there, it doesn't seem like the relevant behavior of the new API would change by the time the implementation was finalized. Even if the relevant behavior of openPopup() changed, the keyboard PoCs would still work.

The public docs indicate the lack of user interaction requirement is intentional, and does not mention anything about multiple potentially-conflicting UI elements. It does discuss standalone spoofing of browser UI and the various technical and CWS review mitigations. I'm not fully convinced these mitigations are sufficient, especially given the provided PoCs which only contain partial spoofed content which might not be identified as malicious by a CWS review. The content could be more easily disguised as legitimate extension functionality if the same extension popup content is used in other contexts.

### da...@chromium.org (2022-02-23)

In general it seems that extension popups should not show over-top of Chrome's permissions popups. Currently they are simply sorted in order of when they were shown.

I can repro on M96 for the first example.

reillyg could you triage?

High sev for site spoofing? But I'd drop to Medium since it's messing with permissions where the user often knows what they are trying to do/where they are doing it, and since it requires installing an extension. Dropping further to low as it requires a keyboard interaction too, and it seems to require the window to be just the right size.

Presumably the dialogs could be made to look like native linux ones if wanted?
On linux the popups don't look like native, nor appear over top of them.

[Monorail components: Platform>Extensions]

### [Deleted User] (2022-02-23)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2022-02-23)

Thanks for initial triage. For further triage, feel free to use some of my prior issues with similar impacts as a starting point:
https://crbug.com/1290098
https://crbug.com/1239760#c5
https://crbug.com/1237310
https://crbug.com/1235222

Those typically were medium severity, even when extension installation was required.

> "Dropping further to low as it requires a keyboard interaction too, and it seems to require the window to be just the right size."

With openPopup(), either mouse or keyboard interaction can be used for permission prompt PoC. So it's easier to perform the attack.
With openPopup(), no user interaction is required for the screen share PoC.

Window size helps with attack, but depending on the area that needs to be covered, the window can be fairly wide. Extension popups can be up to 800px wide, so if the target dialog's left border is within 800px of the extension popup, a spoof is possible. In wide and center-aligned dialogs like screen share dialog, this is quite easy to achieve. Extensions can also arbitrarily create or resize windows without special permissions (as demonstrated in the PoCs) so a suboptimal window size is not a big mitigation for attackers.

### re...@chromium.org (2022-02-23)

Assigning this to Devlin and marking it as a blocker for https://crbug.com/chromium/1245093. It seems like the issue would be resolved by either forcing the extensions popup to appear under any native browser UI or be delayed until the existing UI has been dismissed by the user.

Replacing Security_Impact-Extended with Security_Impact-Dev because this feature is currently only enabled on dev-channel.

### al...@alesandroortiz.com (2022-02-23)

This also impacts Stable, so label should be Security_Impact-Extended. Keyboard shortcut can be used to open the extension popup on Stable through Canary. The openPopup() scenarios only work on Canary/Dev right now.

If requested, I can split this off into two separate issues to track the keyboard shortcut scenarios separately from the openPopup() scenarios, but I imagine the fix would be the same anyway.

### [Deleted User] (2022-02-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-24)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rd...@chromium.org (2022-02-24)

Thanks for the report!  This is a fun one.  I agree that, while openPopup() is the easiest way to replicate this, it's entirely doable without it (keyboard shortcuts), and that adding a user gesture to openPopup() really wouldn't make much difference.

We could prevent extension dialogs from being opened if there's permissions windows, but that seems like a game of whack-a-mole - we'd have to ensure we check *all* the associated anchored permissions, and I suspect we'd miss some (especially if / when new UI is introduced).  It's also complicated by the fact that the showing / rendering of the widgets can be asynchronous.

I think the real fix here is to ensure native permissions UI always renders on top of extension content (when anchored to the same browser window).  There's still phishing attacks that can happen in that case (popping up extension UI under the permissions prompt with big green arrows pointing to "Allow"), but those aren't really any different than can be accomplished today with tab content.

Elly, is there an any good way to give an "always on top of anchored widgets" property for different views?  (We wouldn't want it to be _truly_ always on top - other browser windows should be able to cover it.)  Is there any prior art for the ordering of anchored widgets, besides "most recently opened on top"?

### [Deleted User] (2022-02-27)

[Empty comment from Monorail migration]

### rd...@chromium.org (2022-03-03)

Ugh, crbug dropped the cc from c#12.  Adding Elly for real.

### el...@chromium.org (2022-03-07)

#12: Short answer, no there is no such thing as "always on top of anchored widgets". We can order widgets relative to each other via z-order or similar though.

I would ask avi@ how to handle this since he is more or less the domain expert on Sketchy Stuff People Do With Window Ordering.

### rd...@chromium.org (2022-03-10)

Tentatively passing to avi@ per c#15; Avi, feel free to pass back to me if there's a preferred extension-y solution here : )

### rd...@chromium.org (2022-04-13)

Passing to robliao@ for input following email discussion.

### rd...@chromium.org (2022-04-14)

I'll take this back for now to fix for the ExtensionPopup case, but it'd be good to have something built more into the views system (as we discussed offline).  I'll file a separate bug for that tomorrow (unless there already is one, Rob?)

### gi...@appspot.gserviceaccount.com (2022-04-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/79dfed91dc6624763788ae7ecb029082bb23d66a

commit 79dfed91dc6624763788ae7ecb029082bb23d66a
Author: Devlin Cronin <rdevlin.cronin@chromium.org>
Date: Wed Apr 20 02:06:51 2022

[Extensions UI] Place popup directly above the browser window

The extension popup should not render over other anchored widgets when
it's displayed. When it shows, stack it directly over the anchor widget
so that other anchored widgets render on top of it.

Add a regression test for the same.

Note: This currently doesn't work on Mac.

Bug: 1300006
Change-Id: Iddb1ba6305e5d2bdee6770e3741c8f0e6627dedb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3584899
Reviewed-by: Emilia Paz <emiliapaz@chromium.org>
Reviewed-by: Elly Fong-Jones <ellyjones@chromium.org>
Commit-Queue: Devlin Cronin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/heads/main@{#994004}

[modify] https://crrev.com/79dfed91dc6624763788ae7ecb029082bb23d66a/chrome/browser/ui/views/extensions/extension_popup_interactive_uitest.cc
[modify] https://crrev.com/79dfed91dc6624763788ae7ecb029082bb23d66a/chrome/browser/ui/views/extensions/extension_popup.cc
[modify] https://crrev.com/79dfed91dc6624763788ae7ecb029082bb23d66a/chrome/browser/ui/views/extensions/extension_popup.h


### rd...@chromium.org (2022-04-20)

This should be fixed for non-mac platforms with c#19.  kerenzhu@ offered to investigate for mac; passing to them.

### ke...@chromium.org (2022-05-10)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-05-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/effdec652111bff9950e5b6d6a276fd53c46fe89

commit effdec652111bff9950e5b6d6a276fd53c46fe89
Author: Keren Zhu <kerenzhu@chromium.org>
Date: Thu May 12 15:13:51 2022

[mac] Fix Widget::{StackAbove(), StackAtTop()} for children windows

These widget methods are no-op because of AppKit quirks:
-[NSWindow orderWindow] and -[NSWindow setOrderedIndex] won't work for
children windows. Their order is fixed to the attachment order (the last
attached window is on the top).

This CL fix them by re-parenting children in our desired order.

Bug: 1324216, 1300006
Change-Id: I6422308458431fdfaa87bb477afa061e58da02e6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3642639
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: Keren Zhu <kerenzhu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1002639}

[modify] https://crrev.com/effdec652111bff9950e5b6d6a276fd53c46fe89/chrome/browser/ui/views/extensions/extension_popup_interactive_uitest.cc
[modify] https://crrev.com/effdec652111bff9950e5b6d6a276fd53c46fe89/ui/views/widget/widget_interactive_uitest.cc
[modify] https://crrev.com/effdec652111bff9950e5b6d6a276fd53c46fe89/components/remote_cocoa/app_shim/native_widget_ns_window_bridge.mm
[modify] https://crrev.com/effdec652111bff9950e5b6d6a276fd53c46fe89/components/remote_cocoa/app_shim/native_widget_mac_nswindow.mm


### gi...@appspot.gserviceaccount.com (2022-05-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/aee1dc89a7c34f5a6b98df7ea3c6dcea51946f73

commit aee1dc89a7c34f5a6b98df7ea3c6dcea51946f73
Author: Og Astorga <ogastorga@chromium.org>
Date: Thu May 12 17:32:21 2022

[Sheriff] Revert "[mac] Fix Widget::{StackAbove(), StackAtTop()} for children windows"

This reverts commit effdec652111bff9950e5b6d6a276fd53c46fe89.

Reason for revert: Suspect culprit of "interactive_ui_tests on Mac-10.11" failing on builder "Mac10.11 Tests"

Bug: 1325021

Original change's description:
> [mac] Fix Widget::{StackAbove(), StackAtTop()} for children windows
>
> These widget methods are no-op because of AppKit quirks:
> -[NSWindow orderWindow] and -[NSWindow setOrderedIndex] won't work for
> children windows. Their order is fixed to the attachment order (the last
> attached window is on the top).
>
> This CL fix them by re-parenting children in our desired order.
>
> Bug: 1324216, 1300006
> Change-Id: I6422308458431fdfaa87bb477afa061e58da02e6
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3642639
> Reviewed-by: Avi Drissman <avi@chromium.org>
> Commit-Queue: Keren Zhu <kerenzhu@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1002639}

Bug: 1324216, 1300006
Change-Id: I4686287db225bc3a9e615361b22ba16e2d26a305
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3644970
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Keren Zhu <kerenzhu@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Og Astorga <ogastorga@chromium.org>
Owners-Override: Og Astorga <ogastorga@chromium.org>
Reviewed-by: Keren Zhu <kerenzhu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1002709}

[modify] https://crrev.com/aee1dc89a7c34f5a6b98df7ea3c6dcea51946f73/chrome/browser/ui/views/extensions/extension_popup_interactive_uitest.cc
[modify] https://crrev.com/aee1dc89a7c34f5a6b98df7ea3c6dcea51946f73/ui/views/widget/widget_interactive_uitest.cc
[modify] https://crrev.com/aee1dc89a7c34f5a6b98df7ea3c6dcea51946f73/components/remote_cocoa/app_shim/native_widget_ns_window_bridge.mm
[modify] https://crrev.com/aee1dc89a7c34f5a6b98df7ea3c6dcea51946f73/components/remote_cocoa/app_shim/native_widget_mac_nswindow.mm


### al...@alesandroortiz.com (2022-06-03)

On 104.0.5100.0 Canary on Windows I'm still able to repro this with 100% reliability with an updated PoC (attached). The updated PoC adds a slight delay before the remote page calls the permission prompt to improve reliability, and adjusts the window width to improve alignment, otherwise it's identical to original PoC. The original PoC without changes still works but with varying reliability for the permission prompt scenario, and with 100% reliability with the screen share dialog scenario.

For some reason, browser action keyboard shortcuts are not working *at all* for me on 102 Stable or 104 Canary, so I don't know if an updated keyboard PoC would work there, but I assume it would work.

REPRODUCTION CASE
Initial setup for chrome.action.openPopup() PoCs (v101-104 Canary):
1. Install attached extension: manifest-openPopup.json + bg-openPopup.js + popup.html + popup-screenshare.html. Rename the manifest file to manifest.json


PoC for permission prompt + openPopup() PoC:
1. Reload manifest-openPopup.json extension using chrome://extensions
2. Click on the gray box in the attacker page.

PoC for screen share dialog + openPopup() PoC:
1. Reload manifest-openPopup.json extension using chrome://extensions
No user interaction required: Wait for attack to run.
2. Optional: Click on the gray box in the attacker page to run same attack with user interaction.

Observed: Extension popup renders simultaneously over permission prompt, screen share dialog, or other sensitive browser UI.
Expected: Extension popup renders under permission prompt, screen share dialog, or other sensitive browser UI. Or one of the conflicting UI elements is closed automatically before showing the other UI elements. Or any other safer behavior.

### al...@alesandroortiz.com (2022-06-03)

Not sure what happened with the attachments. Trying again.

### ke...@chromium.org (2022-06-03)

Thank you for providing an updated PoC. It seems that StackAbove() is not reliable on Windows when it concurs with the open of another window. 
A bandit will be to make the security window StackAtTop(). I will try and see if that works.

In the long run, we need a semantic z-ordering system. I will work on that after we resolve crbug.com/1324216.

### gi...@appspot.gserviceaccount.com (2022-06-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/41f0a903b50b2c168bb6c6df96b71440de95b05a

commit 41f0a903b50b2c168bb6c6df96b71440de95b05a
Author: Keren Zhu <kerenzhu@chromium.org>
Date: Mon Jun 06 22:27:42 2022

Reland "[mac] Fix Widget::{StackAbove(), StackAtTop()} for children windows"

This is a reland of commit effdec652111bff9950e5b6d6a276fd53c46fe89

Disable tests for mac <= 10.13 due to -[NSWindow orderedWindows] not
being reliable after window hierarchy update. I couldn't find a
workaround to that.

Fix failed tests on mac 11 builder. It turned out that
-[NSWindow orderWindow] can be called from -[NSWindow addChildWindow]
from AppKit internally. We don't want to intercept orderWindow in this
case.

Original change's description:
> [mac] Fix Widget::{StackAbove(), StackAtTop()} for children windows
>
> These widget methods are no-op because of AppKit quirks:
> -[NSWindow orderWindow] and -[NSWindow setOrderedIndex] won't work for
> children windows. Their order is fixed to the attachment order (the last
> attached window is on the top).
>
> This CL fix them by re-parenting children in our desired order.
>
> Bug: 1324216, 1300006
> Change-Id: I6422308458431fdfaa87bb477afa061e58da02e6
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3642639
> Reviewed-by: Avi Drissman <avi@chromium.org>
> Commit-Queue: Keren Zhu <kerenzhu@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1002639}

Bug: 1324216, 1300006
Change-Id: Id046bcdaad4928f5c0a8aeb35e9f1f61fc751b18
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3661767
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: Keren Zhu <kerenzhu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1011169}

[modify] https://crrev.com/41f0a903b50b2c168bb6c6df96b71440de95b05a/chrome/browser/ui/views/extensions/extension_popup_interactive_uitest.cc
[modify] https://crrev.com/41f0a903b50b2c168bb6c6df96b71440de95b05a/ui/views/widget/widget_interactive_uitest.cc
[modify] https://crrev.com/41f0a903b50b2c168bb6c6df96b71440de95b05a/components/remote_cocoa/app_shim/native_widget_ns_window_bridge.mm
[modify] https://crrev.com/41f0a903b50b2c168bb6c6df96b71440de95b05a/components/remote_cocoa/app_shim/native_widget_mac_nswindow.mm


### ke...@chromium.org (2022-06-15)

Discussed offline with with robliao@. Mitigations using StackAtTop() and StackAbove() are inherently susceptible to time delay attack, because of the async natural of window creation. Given that semantic z-ordering is not coming any soon and this bug is blocking https://crbug.com/chromium/1245093, we need an alternative shorter-term solution. 

I propose this protocol (also suggested by robliao@):
1. When there's no extension popup open, prevent new extension popup from opening when a security bubble opens.
2. When there's an extension popup open, close it when a security bubble opens. 

This protocol is partially implemented on some security bubbles. Some work items:
A. make a consistent API for it. The API should at least support i. mark a widget as security related. ii. check if any security widget is open or being open. 
B. make sure this API is robust against simulations showing of widget (exploited by this bug)

The idea was disputed in https://crbug.com/chromium/1300006#c12, but I think an easy to use API should resolve most concerns there. rdevlin.cronin@ let me know if this sounds good to you, because it will go against the original direction we were heading (i.e. use StackAbove()).

IIUC, we don't have a central place to track widgets. This API will likely involve such a thing, similar to a Widget-level window manager, although it will manage only child widgets (we won't want independent browser windows to interfere each others). 

### rd...@chromium.org (2022-07-21)

Thanks for the comments here, and sorry for the delay.  A couple considerations here:

- If we have an easy-to-use, central API for displaying these types of widgets, that definitely alleviates my concerns from c#12.  I was worried that would be much more work than we'd want to do for this bug : )  That said, it's definitely a good solution, and I think would allow us to have more holistic fixes in the future for issues like this.  Do you have an idea of what the timeline for that might be like, and who the proper owners would be?  (I'd assume that's something the views team would want to have direction over?)

- I also slightly worry that this could become an issue in the _other_ direction, depending on our classification of security UI.  If, say, requesting location or permission access is considered security UI (which I think it should be), then a website could potentially DOS an extension trying to open a popup by opening their own prompt.  If we have an extension that relies on displaying the popup for timely (perhaps even security-or-privacy-related) information, this could be a problem.  Do we think we'd want to have this restriction in place from the other end, as well, and not allow a website-triggered request to appear if an extension popup is active?  (Obviously, and browser-initiated UI takes precedence over both.)  That is _less_ of a concern, given much of that UI is gated in some way, shape, or form (behind a user gesture, having dismiss count as denial and not showing again, etc) to prevent existing website abuse, but it seems like a potential rough-edge.

### ke...@chromium.org (2022-07-21)

We (the views team) want to explore the feasibility of widget ordering starting next week for two weeks. We will have a better estimate on the timeline as we unearth the unknown unknowns. If we decide to go for it, the current plan is to work on the implementation throughout August. I will probably be the main owner. 

I just closed https://crbug.com/chromium/1324216. That's the main known blocker at the system API level. It should give us a bit more confidence.

Regarding the web page might DDOS an extension by requesting security prompts, I am not too concerned about that. As you've pointed out, such prompts should be gated to prevent website abuse, regardless of the presence of extensions. 

> Do we think we'd want to have this restriction in place from the other end, as well, and not allow a website-triggered request to appear if an extension popup is active?
If extensions are allowed to suppress website from requesting permission, I feel that it might open up an attack vector for malicious extension to DDOS website. I think this is a chicken or the egg problem that we can only choose one and sacrifice the other. 

### ke...@chromium.org (2022-08-18)

[Empty comment from Monorail migration]

### ke...@chromium.org (2022-08-22)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-09-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f1af757861b73712d0347cd88d21aa7a92484966

commit f1af757861b73712d0347cd88d21aa7a92484966
Author: Keren Zhu <kerenzhu@chromium.org>
Date: Wed Sep 14 23:51:57 2022

Remove StackAbove() for extension popup when widget layering is enabled

The security bubble will have a higher widget sublevel when the widget
layering feature is enabled. Therefore, we don't need an explicit
StackAbove() for the extension popup.

Bug: 1355904, 1300006
Change-Id: Ib8c5e7882052b363f0cd2796c1f44e4aa255a158
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3895938
Commit-Queue: Keren Zhu <kerenzhu@chromium.org>
Reviewed-by: Emilia Paz <emiliapaz@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1047209}

[modify] https://crrev.com/f1af757861b73712d0347cd88d21aa7a92484966/chrome/browser/ui/views/extensions/extension_popup.cc


### al...@alesandroortiz.com (2022-09-15)

Hi folks, thanks for working on this. Is there a way for me to enable Widget Layering to verify presumed fix from https://crbug.com/chromium/1300006#c33?

I see the feature flag was added in https://bugs.chromium.org/p/chromium/issues/detail?id=1355904#c3 but I'm unclear on how to enable it manually in my Canary instance, if that's even possible. The PoC from https://crbug.com/chromium/1300006#c24 still repros on my Canary instance so I imagine it doesn't have Widget Layering enabled.

### ke...@chromium.org (2022-09-15)

Hi alesandro@, you could enable it using command line "--enable-features=WidgetLayering". Thank you for volunteer to verify the fix.

### al...@alesandroortiz.com (2022-09-15)

I might actually have Widget Layering enabled. I was on yesterday's Canary which is why I was able to repro both scenarios.

Today's Canary fixes the permission prompt scenario (presumably thanks to https://crbug.com/chromium/1300006#c33 + Widget Layering enabled), but I'm still able to repro the screenshare dialog scenario.

### ke...@chromium.org (2022-09-15)

Thank you. I have not applied the fix to the screen sharing dialog yet, stay tuned.

### al...@alesandroortiz.com (2022-09-15)

kerenzhu@, thanks, also verified that this is partially fixed with --enable-features=WidgetLayering on 107.0.5303.0 Canary:
permission prompt scenario is fixed, but the screenshare dialog scenario still repros (same as https://crbug.com/chromium/1300006#c36).

### ke...@chromium.org (2022-09-16)

cc'd reviewers of a pending CL. 

### ke...@chromium.org (2022-09-22)

The screenshare dialog can't be forced on top of the extension popup by manipulating z-orders. Therefore, I am blocking API-initiated extension popups when there's a screensharing dialog in https://crrev.com/c/3902206. This idea was previously discussed in https://crbug.com/1300006#c28. We call this strategy the "Mutual Exclusion" between widgets in https://crbug.com/chromium/1355904.

To facilitate CL review (eladalon@ is interested) and for posterity, I'll explain why the z-order trick won't work for the screensharing dialog.

Simply put, this is because the screensharing dialog is a non-desktop widget and the extension popup is a desktop widget (at least on Windows). A non-desktop widget can't be rendered on top of another desktop widget. The distinction between desktop and non-desktop widget ought to be an Aura internal detail but is unfortunately not transparent to the client code. 

A non-desktop widget is always a secondary UI on desktop*. It paints its content to the top-level desktop widget's AccelerateWidget (e.g. HWND on Windows), so it can't go beyond the bound of the root window. Web dialogs like the screensharing dialog are always non-desktop dialog because AFAIK we want to constrain them in the browser window bound. 

As for why non-desktop widget can't be on top of another desktop widget, it is because from the perspective of the OS the non-destop widget is painted together with its desktop root in a single round, therefore it is impossible to paint another desktop widget in-between. A visual explainer (google internal): http://slides/1fleqHZvZtxLdPLWlR3bbgfQvMpG_wksBelxmADGoZi8

Now, this obstacle will be eliminated if we make EVERYTHING a desktop widget. This is what mac is doing. However, we don't know its implication on performance and animation. See also discussion about this option in https://crbug.com/chromium/1280332.

* ChromeOS adds more complexity to the situation. On ash, everything is a non-desktop widget. However with lacros, the browser frame is a desktop widget. Explaining their technical reasons is beyond the scope of this bug.



### al...@alesandroortiz.com (2022-09-22)

Left two comments in https://crrev.com/c/3902206 to provide context around a couple of important assumptions.

### gi...@appspot.gserviceaccount.com (2022-09-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e60e29b323e7462c5732beca39fdb69865a5330b

commit e60e29b323e7462c5732beca39fdb69865a5330b
Author: Keren Zhu <kerenzhu@chromium.org>
Date: Tue Sep 27 17:18:55 2022

Block API-initiated extension popups when there's visible media picker dialog

This will prevent malicious extension from spoofing media picker modal.

Bug: 1300006, 1355904
Change-Id: I27d7c822dcc882e4c8d956b2a54a400dd3540e03
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3902206
Reviewed-by: Emilia Paz <emiliapaz@chromium.org>
Commit-Queue: Keren Zhu <kerenzhu@chromium.org>
Reviewed-by: Elad Alon <eladalon@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1051898}

[modify] https://crrev.com/e60e29b323e7462c5732beca39fdb69865a5330b/chrome/browser/ui/views/desktop_capture/desktop_media_picker_views.cc
[modify] https://crrev.com/e60e29b323e7462c5732beca39fdb69865a5330b/chrome/browser/ui/views/extensions/extensions_toolbar_container.cc
[modify] https://crrev.com/e60e29b323e7462c5732beca39fdb69865a5330b/chrome/browser/ui/views/desktop_capture/desktop_media_picker_views.h


### al...@alesandroortiz.com (2022-09-27)

Patch in https://crbug.com/chromium/1300006#c42 fixed the share dialog scenario using openPopup(), as noted in commit message. Thanks kerenzhu@!

I need to nail down the timing once Canary with the patch comes out tomorrow, but I'm still able to repro the share dialog scenario with keyboard PoC in ASan build 1052020 with the patch. This PoC is a bit more difficult to perform due to keyboard interaction and less precise (potentially allowing user to briefly notice non-spoofed content), but still should be fixed.

Will provide PoC + screen recording tomorrow once Canary is out.

### al...@alesandroortiz.com (2022-09-27)

For future reference, triggering the extension manually by clicking extension icon in toolbar was discussed in https://chromium-review.googlesource.com/c/chromium/src/+/3902206/comment/c7c18e57_39135a22/ but that doesn't cover the keyboard trigger. User is likely not aware that a particular keyboard shortcut is also a trigger for the extension popup since the keyboard shortcut is defined in extension manifest and not communicated to user outside of chrome://extensions/shortcuts which is fairly hidden.

### al...@alesandroortiz.com (2022-09-28)

For keyboard + screen share dialog PoC that still repros:

REPRODUCTION CASE
Initial setup for keyboard PoC:
1. Install attached extension: manifest.json + bg-keyboard.js + popup.html + popup-screenshare.html.

PoC for screen share dialog + keyboard PoC:
1. Reload manifest.json extension using chrome://extensions
2. Press Ctrl+A when requested by the attacker page. (Optional: Try different speeds between the 'Ctrl' keypress and 'A' keypress along with different &dialogDelay param values.)

Observed: Extension popup renders simultaneously over screen share dialog (and potentially other sensitive browser UI).
Expected: Extension popup is not allowed to open over screen share dialog (and potentially other sensitive browser UI).

---

For quick typers like myself, a dialog delay of 50ms is optimal. For most users, optimal value is probably 80-100ms or higher. Delays of 150ms or higher will likely cause failure due to dialog closing extension popup. You can play around with this delay using the &dialogDelay param. Regardless of delay, if user isn't paying attention or is looking at another area of screen, it's likely they will miss the original text and only see the spoofed text. Or potentially think the browser itself updated the text in the dialog.

Updated remote PoC URL is https://alesandroortiz.com/security/chromium/extension-over-prompt-september2022.html?screenshare&dialogDelay=50

Permission prompt PoC doesn't repro since layering works as intended, but left it there for verification purposes.

### al...@alesandroortiz.com (2022-09-28)

https://crbug.com/chromium/1300006#c45 repro is on 108.0.5327.1 Canary with all fixes in this crbug.

### al...@alesandroortiz.com (2022-09-28)

Attached fixed bg-keyboard.js

### ke...@chromium.org (2022-09-29)

Thank you alesandro@ for your latest PoC. 

Previous fixes should have resolved zero-user-interaction attacks. https://crbug.com/chromium/1300006#c45 is a PoC that needs keyboard input. 
We can patch this easily by extending the fix in https://crbug.com/chromium/1300006#c42 to non-API-triggered extension, but I would like to learn opinions from extension owners & security folks. 

Devlin, Emilia, do you think that the PoC still something worrisome and need to be fixed? I feel that since this involves user interaction, the risk becomes much lower. 

### al...@alesandroortiz.com (2022-11-29)

Friendly ping: Any updates on this issue, particularly the question in https://crbug.com/chromium/1300006#c48?

### ad...@chromium.org (2022-12-01)

[Empty comment from Monorail migration]

### em...@chromium.org (2022-12-01)

I was not able to reproduce on MacOs with 107.0.5304.110. Steps followed:
1. Install https://crbug.com/chromium/1300006#c45 extension with fixed bg-keyboard.js from https://crbug.com/chromium/1300006#c47
2. In chrome://extensions, update extension
3. Window opens
4. Click crl or crl+A:
  - screen share dialog opens
  - extension popup does NOT automatically open
  - extension popup does NOT open when icon is clicked

Seems this security bug is fixed, or I didn't reproduce it correctely. alessandro@ are my steps correct?

### al...@alesandroortiz.com (2022-12-01)

Hm, seems like the keyboard shortcut isn't immediately registered when loading an unpacked extension. You'll need to go to chrome://extensions/shortcuts and set the shortcut again (even though it appears as already having the shortcut). Then you can re-try the repro. I verified this still works in 107.0.5304.107 Stable and 110.0.5451.0 Canary on 	Windows 10 Version 21H2 (Build 19044.2251).

For CWS extensions I already have installed, the predefined keyboard shortcuts seem to work without any additional poking, so might be a bug affecting unpacked extensions or with my PoC extension for some reason.

### rd...@chromium.org (2023-03-02)

[Empty comment from Monorail migration]

### el...@google.com (2023-07-07)

[Empty comment from Monorail migration]

### el...@google.com (2023-07-07)

[Empty comment from Monorail migration]

### ke...@chromium.org (2023-08-03)

[Empty comment from Monorail migration]

### rd...@chromium.org (2023-08-11)

Revisiting this.

Re https://crbug.com/chromium/1300006#c48: Yes, I think we should still consider that a bug.  While it's reduced severity (because it requires certain timing and user interaction), I think it's still worth fixing.  As a general rule, I'd say we should ensure extension popups never cover security UI dialogs.

### ke...@chromium.org (2023-08-15)

Sounds good, I'll work on fixing the remaining case (the case that involves user actions).  

### is...@google.com (2023-08-23)

This issue was migrated from crbug.com/chromium/1300006?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/1324216]
[Monorail blocking: crbug.com/chromium/1245093]
[Monorail components added to Component Tags custom field.]

### ap...@google.com (2024-02-27)

Project: chromium/src
Branch: main

commit 2ae924296dd882acde3e277355b3bfce20b93851
Author: Keren Zhu <kerenzhu@chromium.org>
Date:   Tue Feb 27 21:09:47 2024

    Block user-triggered extension popups on possibly overlapping security UIs
    
    The extension team considers the user-triggered overlapping case is
    critical enough to be addressed, therefore this patches blocks the popup
    when there is possibly overlapping security UI.
    
    Test: manually verify that this fixes crbug.com/40058873#comment46
    Bug: 40058873, 326681253
    Change-Id: Ie29870f2011cee9e4d521efe76e11cb63d6fc1c2
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5321044
    Reviewed-by: Emilia Paz <emiliapaz@chromium.org>
    Commit-Queue: Keren Zhu <kerenzhu@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1266060}

M       chrome/browser/ui/extensions/extension_action_view_controller.cc
M       chrome/browser/ui/extensions/extensions_container.h
M       chrome/browser/ui/views/extensions/extensions_toolbar_container.cc
M       chrome/browser/ui/views/extensions/extensions_toolbar_container.h

https://chromium-review.googlesource.com/5321044


### ke...@chromium.org (2024-02-27)

Case [comment #46](https://issues.chromium.org/issues/40058873#comment46) should have been fixed. Closing. Sorry for the long delay.

alesandro@ could you verify this when you have time. Thanks.

### al...@alesandroortiz.com (2024-02-29)

kerenzhu@, thanks for fix! There is a non-security UI bug, but otherwise verified all scenarios as fixed in 124.0.6328.0 Canary on Windows 10 Version 22H2 (Build 19045.4046).

Verified by testing all the PoCs in this report: [#comment2](https://issues.chromium.org/issues/40058873#comment2), [#comment6](https://issues.chromium.org/issues/40058873#comment6), [#comment46](https://issues.chromium.org/issues/40058873#comment46) for both the screenshare and permission (camera) scenarios.

The minor UI bug is that if the timing is right, the extension toolbar animation will be stopped but not fully reset when the popup open is cancelled (see attached screenshot). The icon for the invoked extension (square gray "P" in this case) is shown over the extension puzzle icon. Despite the invoked extension icon being shown over the extension puzzle icon, it functions normally when clicked (opens the extension list, not the extension's popup), so it's only a visual quirk due to the cancelled animation.

I can repro this on my device when using [#comment46](https://issues.chromium.org/issues/40058873#comment46) PoC with &dialogDelay param set to 80-100ms.

### am...@google.com (2024-03-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-03-07)

Congratulations Alesandro! The Chrome VRP has decided to award you $5,000 for this report of security UI spoofing. The reward amount represents the high-quality reporting of an entire class of permission prompt issues, which is why it was above the standard of the reward amount generally standard for this type of security UI bug in terms of class and impact. Thank you for your efforts and thorough reporting, reporting this issue to us, and your patience while we worked to resolve this issue!

### al...@alesandroortiz.com (2024-03-07)

Thanks for the reward!

I had forgotten Widget Layering ([issue 40236074](https://issues.chromium.org/issues/40236074)) also helped fix the reported issues, in addition to the commits in this issue. Thanks for considering that as part of the reward!

### pe...@google.com (2024-06-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ke...@chromium.org (2024-07-02)

Unblocking [Issue 350256140](https://issues.chromium.org/issues/350256140) since the two issues have different causes.

### sr...@microsoft.com (2024-08-14)

kerenzhu@ & emiliapaz@ I am able repro the case where extension popup renders over the screenshare dialog prompt on chrome canary - the extension is from #comment46. The screen recording is attached. Is this because of the changes made by https://chromium-review.googlesource.com/c/chromium/src/+/5525866?

### ke...@chromium.org (2024-08-14)

Good catch. This is indeed regressed by <https://chromium-review.googlesource.com/c/chromium/src/+/5525866>

In the POC from [#comment46](https://issues.chromium.org/issues/40058873#comment46), the extension is configured in manifest.json to be triggered by Ctrl+A. This is considered a user-triggered action, and was blocked by my [previous CL](https://chromium-review.googlesource.com/c/chromium/src/+/3902206). However in the [culprit CL](https://chromium-review.googlesource.com/c/chromium/src/+/3902206) this behavior is reverted and only API-triggered extensions are blocked.

### ap...@google.com (2024-08-15)

Project: chromium/src
Branch: main

commit 61d739870c7ccba8d7d1b55e04c9bcba9540c096
Author: Keren Zhu <kerenzhu@chromium.org>
Date:   Wed Aug 14 23:57:29 2024

    Don't show user-triggered extensions that may block security dialogs
    
    User-triggered extensions, including those triggered by shortcuts, were
    blocked by security dialogs since https://crrev.com/c/3902206 but this
    behavior was mistakenly reverted by https://crrev.com/c/5525866.
    
    Bug: 40058873
    Change-Id: Ib0277808b9805b4b624b93d4ca6d1b704213bfcc
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5783625
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Commit-Queue: Keren Zhu <kerenzhu@chromium.org>
    Reviewed-by: Emilia Paz <emiliapaz@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1342033}

M       chrome/browser/ui/extensions/extension_action_platform_delegate.h
M       chrome/browser/ui/extensions/extension_action_view_controller.cc
M       chrome/browser/ui/views/extensions/extension_action_platform_delegate_views.cc
M       chrome/browser/ui/views/extensions/extension_action_platform_delegate_views.h
M       chrome/browser/ui/views/extensions/extension_popup.cc
M       chrome/browser/ui/views/extensions/extension_popup.h
M       chrome/browser/ui/views/extensions/extension_popup_interactive_uitest.cc

https://chromium-review.googlesource.com/5783625


### al...@alesandroortiz.com (2024-08-16)

Given the regressing commit is present in 127.0.6533.57 Stable [1] released on Jul 17, 2024, should someone file a new security issue so it's properly tracked, and make sure it's merged if appropriate?

I'll let Microsoft or Chromium folks file the new issue since I didn't find the regression. (Thanks commenter from [#comment70](https://issues.chromium.org/issues/40058873#comment70) for identifying the regression!)

[1] <https://chromiumdash.appspot.com/commit/321371e933dbd68b63d4dfaae5963fed4b7dc19>

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058873)*
