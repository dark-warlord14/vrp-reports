# documentPictureInPicture UI spoof via opener

| Field | Value |
|-------|-------|
| **Issue ID** | [40062959](https://issues.chromium.org/issues/40062959) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media>PictureInPicture, UI>Browser>Navigation |
| **Platforms** | Windows |
| **Reporter** | nd...@protonmail.com |
| **Assignee** | st...@chromium.org |
| **Created** | 2023-02-08 |
| **Bounty** | $1,000.00 |

## Description

**Steps to reproduce the problem:**

1. Enable feature chrome://flags/#document-picture-in-picture-api (in Origin Trial)
2. On victim page do documentPictureInPicture.requestWindow();
3. Victim PiP opens popup to attacker page like open('<https://example.org>', '', 'popup=1');
4. On attacker page run opener.location = 'about:blank'; and notice security UI did not update.
5. On attacker page run opener.document.write('foo');

**Problem Description:**  

documentPictureInPicture does not update security UI on about:blank navigations so any window reference allows for a spoof. (maybe apply COOP?)

Could be related to my bug: <https://bugs.chromium.org/p/chromium/issues/detail?id=1413813>

**Additional Comments:**

\*\*Chrome version: \*\* 109.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Windows

## Attachments

- [spoof.mp4](attachments/spoof.mp4) (video/mp4, 488.0 KB)
- [extension.mp4](attachments/extension.mp4) (video/mp4, 3.6 MB)

## Timeline

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### ma...@google.com (2023-02-09)

(Didn't try to repro this one.)

liberato@, could you take a look and decide whether this is a valid security issue?

Speculatively assigning severity and FoundIn for now. (Not setting Impact-None, because an active Origin Trial counts as a default-enabled feature.)

[Monorail components: Blink>Media>PictureInPicture]

### li...@google.com (2023-02-09)

interesting -- yeah i'll take a look.  thanks!

### [Deleted User] (2023-02-09)

[Empty comment from Monorail migration]

### li...@google.com (2023-02-09)

when i do this, the change to `opener.location` causes the pip window to close as part of the navigation.  does your pip window stay open?

### nd...@protonmail.com (2023-02-09)

Doing opener.location = 'about:blank' does not close the PiP window.
Tested with latest chromium build on Linux should I provide a PoC video?

### li...@google.com (2023-02-09)

if you could provide a link that i could try locally, that would help a lot.  whatever i'm doing and whatever you are doing are clearly different in some important way.

### li...@google.com (2023-02-09)

+steimel@ FYI

### nd...@protonmail.com (2023-02-09)

https://ndevtk.github.io/cross-site/pip.html

### nd...@protonmail.com (2023-02-09)

[Empty comment from Monorail migration]

### li...@google.com (2023-02-09)

ah, i see -- i misread the description and had the original page open both the pip and popup, and then update the location of the original page.  thanks!

### [Deleted User] (2023-02-09)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### st...@chromium.org (2023-02-10)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2023-02-11)

Saw the work in progress https://chromium-review.googlesource.com/c/chromium/src/+/4242019 which only applies to subsequent loads.

I know there's code preventing the navigation but should the browser process have a more generic check to close PiP automatically if its not matching top level origin.
Considered about https://bugs.chromium.org/p/chromium/issues/detail?id=1413813 as PiP does open when its not meant to.

### cr...@chromium.org (2023-02-17)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Navigation]

### cr...@chromium.org (2023-02-17)

steimel@ / liberato@: I'm curious why the PIP window's displayed origin itself is stale.  I certainly agree with a policy to close the window if it navigates, but since that appears to be tricky to enforce in practice, I'm wondering why the displayed origin doesn't update when a commit happens (as a second line of defense).  Where is the displayed origin handled in the code?

### st...@chromium.org (2023-02-17)

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/frame/picture_in_picture_browser_frame_view.cc;l=559;drc=4ced8912f6c8b32715984dd81e3f376a260ebab6

### gi...@appspot.gserviceaccount.com (2023-02-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5f49142eb086b425f52bb63592ea0a1540e5b2ac

commit 5f49142eb086b425f52bb63592ea0a1540e5b2ac
Author: Tommy Steimel <steimel@chromium.org>
Date: Tue Feb 21 12:51:37 2023

PiP 2.0: Ensure subsequent about:blank loads close the PiP window

Document PiP windows should always close if navigated from the initial
about:blank document. However, the logic allowed for about:blank
navigations to allow the initial navigation to succeed. This opens up a
couple of issues:

1) Refreshing the PiP document breaks but does not close the document

2) Setting the location of the PiP window to about:blank in JS would
disconnect the PiP document from the original window and render it
unusable.

This CL changes that logic to only allow the initial synchronous about:blank navigation to succeed. However, this is insufficient for the
second issue, since there was a race where if the navigation succeeded
before the page closed, then the RenderFrameHostImpl would cancel the
closing action. In order to fix this (and other issues with navigations
canceling the close action), this CL also makes close requests from the
browser side always close the page regardless of navigations.

Bug: 1413919, 1406023, 1414124, 1414975
Change-Id: Ib52875be2ad107ce3f33e2682b0b87f2c7bc6cbf
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4242019
Reviewed-by: Charlie Reis <creis@chromium.org>
Commit-Queue: Tommy Steimel <steimel@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1107695}

[modify] https://crrev.com/5f49142eb086b425f52bb63592ea0a1540e5b2ac/content/browser/renderer_host/render_frame_host_impl.h
[modify] https://crrev.com/5f49142eb086b425f52bb63592ea0a1540e5b2ac/chrome/browser/picture_in_picture/document_picture_in_picture_window_controller_browsertest.cc
[modify] https://crrev.com/5f49142eb086b425f52bb63592ea0a1540e5b2ac/chrome/test/data/media/picture-in-picture/document-pip.html
[modify] https://crrev.com/5f49142eb086b425f52bb63592ea0a1540e5b2ac/content/browser/renderer_host/render_frame_proxy_host.cc
[modify] https://crrev.com/5f49142eb086b425f52bb63592ea0a1540e5b2ac/content/browser/renderer_host/render_frame_host_manager.cc
[modify] https://crrev.com/5f49142eb086b425f52bb63592ea0a1540e5b2ac/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/5f49142eb086b425f52bb63592ea0a1540e5b2ac/content/browser/renderer_host/render_frame_host_impl_unittest.cc
[modify] https://crrev.com/5f49142eb086b425f52bb63592ea0a1540e5b2ac/content/browser/picture_in_picture/document_picture_in_picture_window_controller_impl.cc
[modify] https://crrev.com/5f49142eb086b425f52bb63592ea0a1540e5b2ac/content/browser/site_per_process_browsertest.cc
[modify] https://crrev.com/5f49142eb086b425f52bb63592ea0a1540e5b2ac/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/5f49142eb086b425f52bb63592ea0a1540e5b2ac/content/browser/renderer_host/render_frame_host_manager_unittest.cc


### nd...@protonmail.com (2023-02-21)

Patch seems to not be working for the Tabs API:
chrome.tabs.duplicate, chrome.tabs.update results in navigations being allowed and the URL bar displaying victim.
chrome.tabs.discard() results in all navigations being allowed and the URL bar displaying about:blank

From what I can tell this requires no permissions for the browser extension.

### nd...@protonmail.com (2023-02-21)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-02-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c3a3e0ff3d045805d4a3e15c6877b189a767e05c

commit c3a3e0ff3d045805d4a3e15c6877b189a767e05c
Author: Tommy Steimel <steimel@chromium.org>
Date: Mon Feb 27 19:13:20 2023

[M111] PiP 2.0: Ensure subsequent about:blank loads close the PiP window

This is a cherry-pick onto M111 of https://crrev.com/c/4242019.

Original CL description:

> Document PiP windows should always close if navigated from the initial
> about:blank document. However, the logic allowed for about:blank
> navigations to allow the initial navigation to succeed. This opens up a
> couple of issues:
>
> 1) Refreshing the PiP document breaks but does not close the document
>
> 2) Setting the location of the PiP window to about:blank in JS would
> disconnect the PiP document from the original window and render it
> unusable.
>
> This CL changes that logic to only allow the initial synchronous about:blank navigation to succeed. However, this is insufficient for the
> second issue, since there was a race where if the navigation succeeded
> before the page closed, then the RenderFrameHostImpl would cancel the
> closing action. In order to fix this (and other issues with navigations
> canceling the close action), this CL also makes close requests from the
> browser side always close the page regardless of navigations.
>
> Bug: 1413919, 1406023, 1414124, 1414975
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4242019
> Reviewed-by: Charlie Reis <creis@chromium.org>
> Commit-Queue: Tommy Steimel <steimel@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1107695}
(cherry picked from commit 5f49142eb086b425f52bb63592ea0a1540e5b2ac)

Change-Id: I56332ac46ed37227be8da03118c1fe49b2e5294e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4292137
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: Fr <beaufort.francois@gmail.com>
Commit-Queue: Tommy Steimel <steimel@chromium.org>
Cr-Commit-Position: refs/branch-heads/5563@{#866}
Cr-Branched-From: 3ac59a6729cdb287a7ee629a0004c907ec1b06dc-refs/heads/main@{#1097615}

[modify] https://crrev.com/c3a3e0ff3d045805d4a3e15c6877b189a767e05c/chrome/test/data/media/picture-in-picture/document-pip.html
[modify] https://crrev.com/c3a3e0ff3d045805d4a3e15c6877b189a767e05c/content/browser/renderer_host/render_frame_proxy_host.cc
[modify] https://crrev.com/c3a3e0ff3d045805d4a3e15c6877b189a767e05c/content/browser/renderer_host/render_frame_host_impl.h
[modify] https://crrev.com/c3a3e0ff3d045805d4a3e15c6877b189a767e05c/chrome/browser/picture_in_picture/document_picture_in_picture_window_controller_browsertest.cc
[modify] https://crrev.com/c3a3e0ff3d045805d4a3e15c6877b189a767e05c/content/browser/renderer_host/render_frame_host_manager.cc
[modify] https://crrev.com/c3a3e0ff3d045805d4a3e15c6877b189a767e05c/content/browser/renderer_host/render_frame_host_impl_unittest.cc
[modify] https://crrev.com/c3a3e0ff3d045805d4a3e15c6877b189a767e05c/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/c3a3e0ff3d045805d4a3e15c6877b189a767e05c/content/browser/picture_in_picture/document_picture_in_picture_window_controller_impl.cc
[modify] https://crrev.com/c3a3e0ff3d045805d4a3e15c6877b189a767e05c/content/browser/site_per_process_browsertest.cc
[modify] https://crrev.com/c3a3e0ff3d045805d4a3e15c6877b189a767e05c/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/c3a3e0ff3d045805d4a3e15c6877b189a767e05c/content/browser/renderer_host/render_frame_host_manager_unittest.cc


### gi...@appspot.gserviceaccount.com (2023-03-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bbfe16e556cff090a7d1913214bba463eca7b5d2

commit bbfe16e556cff090a7d1913214bba463eca7b5d2
Author: Tommy Steimel <steimel@chromium.org>
Date: Tue Mar 07 17:19:00 2023

Extensions/PiP2: Respect `CanDuplicateTabAt` when duplicating a tab

The `duplicate` method of the Tabs API for extensions does not check
that the tab can be duplicated as determined in `CanDuplicateTabAt`.
This causes an issue where picture-in-picture tabs can be duplicated by
an extension. This CL fixes the `CanDuplicateTabAt` check (which wasn't
taking is_picture_in_picture into account like other `CanDuplicate`
checks) and also makes the Tabs API respect that check.

Bug: 1413919
Change-Id: Ie46517947d774ce0f8f07950db0dba50f8d57fb5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4312190
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Reviewed-by: Peter Boström <pbos@chromium.org>
Commit-Queue: Tommy Steimel <steimel@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1114002}

[modify] https://crrev.com/bbfe16e556cff090a7d1913214bba463eca7b5d2/chrome/browser/extensions/api/tabs/tabs_constants.cc
[modify] https://crrev.com/bbfe16e556cff090a7d1913214bba463eca7b5d2/chrome/browser/ui/browser_commands.cc
[modify] https://crrev.com/bbfe16e556cff090a7d1913214bba463eca7b5d2/chrome/browser/extensions/api/tabs/tabs_api_unittest.cc
[modify] https://crrev.com/bbfe16e556cff090a7d1913214bba463eca7b5d2/chrome/browser/extensions/api/tabs/tabs_constants.h
[modify] https://crrev.com/bbfe16e556cff090a7d1913214bba463eca7b5d2/chrome/browser/extensions/api/tabs/tabs_api.cc


### st...@chromium.org (2023-03-07)

Duplicating the tab generally shouldn't have been possible for pip tabs but was due to an oversight in extensions code. This causes problems since the duplicated tab avoids being controlled by the DocumentPictureInPictureControllerImpl (which enforces the checks to prevent spoofing). I just landed a change in https://crbug.com/chromium/1413919#c22 which should prevent extensions from being able to duplicate the pip tab. I will also separately add a check to more properly ensure that nothing else has a workaround to duplicate a pip tab, but I believe the change in https://crbug.com/chromium/1413919#c22 should fix this issue

### gi...@appspot.gserviceaccount.com (2023-03-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0195cc9b83ebca340aee0a8404ab356cdc5b1d5b

commit 0195cc9b83ebca340aee0a8404ab356cdc5b1d5b
Author: Tommy Steimel <steimel@chromium.org>
Date: Wed Mar 08 17:30:42 2023

PiP2: NOTREACHED when a Document PiP window is duplicated

There was a bug where Document Picture-in-Picture windows could be
duplicated, leading to spoofing issues since the duplicated window
would bypass some pip-specific logic. This CL makes it so that if that
issue regresses, a NOTREACHED will fire when a Document PiP window is
duplicated.

Bug: 1413919
Change-Id: I44db29eb59a09d368366f23e9178acb7d2a19499
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4317563
Commit-Queue: Tommy Steimel <steimel@chromium.org>
Reviewed-by: Fr <beaufort.francois@gmail.com>
Cr-Commit-Position: refs/heads/main@{#1114605}

[modify] https://crrev.com/0195cc9b83ebca340aee0a8404ab356cdc5b1d5b/content/browser/picture_in_picture/document_picture_in_picture_window_controller_impl.h
[modify] https://crrev.com/0195cc9b83ebca340aee0a8404ab356cdc5b1d5b/content/browser/picture_in_picture/document_picture_in_picture_window_controller_impl.cc


### st...@chromium.org (2023-03-08)

Looks like the CL in https://crbug.com/chromium/1413919#c22 is in version 113.0.5638.0

### nd...@protonmail.com (2023-03-08)

discard() then update() allows displaying any site and showing about:blank but that does not seem as bad.

### [Deleted User] (2023-03-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-09)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-17)

Congratulations NDevTK! The VRP Panel has decided to award you $1,000 for this report. Thank you for your efforts and reporting this issue to us! 

### nd...@protonmail.com (2023-03-17)

Thanks :)

### am...@google.com (2023-03-17)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-03-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9f3c30fce2008686da2e15e1afaaf1db30181922

commit 9f3c30fce2008686da2e15e1afaaf1db30181922
Author: Tommy Steimel <steimel@chromium.org>
Date: Wed Mar 29 19:13:18 2023

pip2: Don't allow picture-in-picture windows to be discarded

This CL prevents tabs in a picture-in-picture (PiP) window from being
discarded. Although `CanDiscard` would already return false for PiP
tabs (since they are always the active tab of the window), they can
still end up being discarded when an extension requests it, as that
does not check `CanDiscard`. So this CL add logic directly into
`Discard` to prevent PiP windows from being discarded.

The reason PiP windows should not be discarded is that discarding them
leaves the PiP window in a state where it's no longer connected to the
DocumentPictureInPictureWindowControllerImpl and therefore just
displays "about:blank" and the toolbar controls no longer function.

Bug: 1413919
Change-Id: I6d3207503cf1ed5644fdbaa821a80e17ac519c7b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4347922
Reviewed-by: Patrick Monette <pmonette@chromium.org>
Commit-Queue: Tommy Steimel <steimel@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1123745}

[modify] https://crrev.com/9f3c30fce2008686da2e15e1afaaf1db30181922/chrome/browser/resource_coordinator/tab_lifecycle_unit_unittest.cc
[modify] https://crrev.com/9f3c30fce2008686da2e15e1afaaf1db30181922/chrome/browser/resource_coordinator/tab_lifecycle_unit.cc


### am...@chromium.org (2023-03-31)

[Empty comment from Monorail migration]

### pg...@google.com (2023-04-04)

[Empty comment from Monorail migration]

### pg...@google.com (2023-04-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1413919?no_tracker_redirect=1

[Multiple monorail components: Blink>Media>PictureInPicture, UI>Browser>Navigation]
[Monorail blocking: crbug.com/chromium/1382964]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062959)*
