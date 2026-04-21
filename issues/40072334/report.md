# Security: SOP bypass: Portal activation bypasses same-page drag and drop source check

| Field | Value |
|-------|-------|
| **Issue ID** | [40072334](https://issues.chromium.org/issues/40072334) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>DataTransfer, Blink>Portals |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | ad...@chromium.org |
| **Created** | 2023-09-14 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

A <portal> being activated while cross-origin content is being dragged allows the page to capture the drop and read the cross-origin data.

Expected behavior:

> "drag and drop will not expose data across cross-site frames on the same page" [0](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/drag_and_drop_interactive_uitest.cc;l=1366;drc=4eda6e27090c76658af35789c0311118b1cc9b36)

This allows to:

- Read contents from cross-origin iframes via drag and drop (same as in <https://crbug.com/chromium/59081>)
- Drop contents into cross-origin iframes via drag and drop
- Read contents of cross-origin images via drag and drop (same as in <https://crbug.com/chromium/1264873>)

**VERSION**  

Chrome Version: 119.0.6009.0  

Operating System: Windows 11

**REPRODUCTION CASE**  

[poc-iframe.html]:

1. Select text in the iframe
2. Drag it into the textbox

[poc-image.html]:

1. Drag and drop the image

**CREDIT INFORMATION**  

Reporter credit: Thomas Orlita

## Attachments

- [poc.webm](attachments/poc.webm) (video/webm, 1.5 MB)
- [poc-iframe.html](attachments/poc-iframe.html) (text/plain, 588 B)
- [poc-image.html](attachments/poc-image.html) (text/plain, 1.2 KB)
- [portal.html](attachments/portal.html) (text/plain, 243 B)

## Timeline

### [Deleted User] (2023-09-14)

[Empty comment from Monorail migration]

### st...@gmail.com (2023-09-14)

Requires Portals to be enabled:

chrome --enable-features=Portals 

### ja...@chromium.org (2023-09-15)

I was able to reproduce this on 119.0.6008.0 (Official Build) canary (64-bit) (cohort: Clang-64).

Without Portals enabled, I'm unable to drag and drop from the other domain.

### ja...@chromium.org (2023-09-15)

I'm going to attach Medium severity to this bug because it requires enabling Portals, which isn't enabled by default. 

### ja...@chromium.org (2023-09-15)

[Empty comment from Monorail migration]

[Monorail components: Blink>DataTransfer]

### ja...@chromium.org (2023-09-15)

[Empty comment from Monorail migration]

[Monorail components: Blink>Portals]

### ja...@chromium.org (2023-09-15)

It seems like portals should behave similar to iframes, but I could be wrong because maybe this is part of the portals spec.

Adding adithyas as owner for now to take a look.

### ad...@chromium.org (2023-09-15)

Portals are disabled by default (and can only be enabled through the command line), so setting "Security_Impact-None" here.

### ad...@chromium.org (2023-09-15)

Verified that this is reproducible on Linux as well (this this is an Aura issue), looks like a real issue and is definitely unintentional behaviour.

### mc...@chromium.org (2023-09-15)

Portal activation currently causes a change in the WebContentsViewAura, which is where drag start information is stored. Without it, the drop is allowed [1]. We should presumably preserve this information across activation.

[1] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/web_contents/web_contents_view_aura.cc;drc=c2cca37e05cb5b20019a27406714d1954194c2d4;l=855

### ad...@chromium.org (2023-09-15)

[Empty comment from Monorail migration]

### ad...@chromium.org (2023-09-15)

#10: There's also this check [1], which is also bypassed. But looking at [1], there seems to be another issue as well, even if drag_start_ were set. Looks like we just let you drag and drop across WebContents' unrestricted .. so you could just drag and drop across a portal activation to the activated page (as long as you keep the predecessor alive). And I think you could theoretically make the portalled page look the same as the initial page, and it will effectively have the same characteristics of the security risk reported in crbug.com/1264873?

[1] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/web_contents/web_contents_view_aura.cc;l=731;drc=31fb07c05718d671d96c227855bfe97af9e3fb20

### st...@gmail.com (2023-09-16)

> so you could just drag and drop across a portal activation to the activated page

Yes, drag and dropping a cross-origin image as described would reset the drag start information, allowing the leak. In the PoC (#c0), once the drag starts, the portal is activated and then the original page gets immediately activated back. Either way works, and in both cases, the site can keep the URL and content of the page the same, so the user wouldn't notice a difference.

This does enable the same impact as https://crbug.com/chromium/1264873 (read cross-origin image data), and apart from that, it also breaks the security boundaries when dragging from/to a cross-origin iframe.

If attacker.example can frame victim.example, there are many realistic and common attack scenarios how this iframe drag leak can be abused:

1. attacker.example loads victim.example/secret-key in an iframe
2. The attacker makes the iframed page invisible and positions/scales it via CSS
3. The attacker shows a decoy game/captcha, which will make the user drag the secret key out of the iframe into the attacker's page

1. attacker.example loads victim.example/private-project/invite-by-email
2. The attacker makes the iframed page invisible and positions/scales it via CSS
3. The attacker shows a decoy game/captcha, which will make the user drag the attacker's email address into the iframe and click an Invite button

In regular Chrome without Portals, these scenarios wouldn't have worked (https://crbug.com/chromium/59081) as the attacker's page won't be able to access drag and drop data across security origins (OOPIFs, I think, to be precise).


### ad...@chromium.org (2023-09-18)

Reproed on Mac as well.

### gi...@appspot.gserviceaccount.com (2023-09-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b521dfd717611f3615c0bf8bbe31b52326983689

commit b521dfd717611f3615c0bf8bbe31b52326983689
Author: Adithya Srinivasan <adithyas@chromium.org>
Date: Wed Sep 20 14:00:20 2023

Portals: Cancel drag-drop in predecessor before activation

We have existing drag-drop checks that prevent data from a
cross-site subframe from being transferred to the main frame, but
these break with portal activation. With portal activation we have two
problems:

1) Portal activation causes a switch in WebContents, and we currently
   don't restrict drag and drops across WebContents (as dragging
   across tabs is considered to be sufficient user-intent). However,
   in this case, portals are within the same tab, and allowing a
   cross-origin drag-and-drop across portal activation has the
   same security risks outlined in https://crbug.com/59081 and
   https://crbug.com/1264873.

2) Portal activation, adoption and reactivation can result in the
   WebContentsViewAura being reset and recreated, so the |drag_start_|
   field will be reset. We can have a portal being activated, the
   predecessor being adopted, and then reactivated, all while a
   drag-drop is active, and the resulting drop's checks will be
   bypassed (within the same page) as |drag_start_| is reset and is
   now absl::nullopt [1].

[1] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/web_contents/web_contents_view_aura.cc;l=855;drc=c2cca37e05cb5b20019a27406714d1954194c2d4

To fix this, we explicitly cancel a drag-drop before activating a
portal. This disallows a drag-drop for persisting across portal
activation. The predecessor page becomes a portal and doesn't allow
input events at that point, and drag and drop failing shouldn't be unexpected behaviour.

Note: This only fixes the issue on Aura; but this likely needs a fix
for Mac as well, which will be in a follow up.

Bug: 1482848
Change-Id: I0c83b1f869ae10586c8dd649dd9c9fb6c56f72e6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4874216
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Commit-Queue: Adithya Srinivasan <adithyas@chromium.org>
Reviewed-by: Kevin McNee <mcnee@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1198962}

[modify] https://crrev.com/b521dfd717611f3615c0bf8bbe31b52326983689/content/browser/web_contents/web_contents_view.h
[modify] https://crrev.com/b521dfd717611f3615c0bf8bbe31b52326983689/content/browser/web_contents/web_contents_view_mac.mm
[modify] https://crrev.com/b521dfd717611f3615c0bf8bbe31b52326983689/content/browser/web_contents/web_contents_view_child_frame.h
[modify] https://crrev.com/b521dfd717611f3615c0bf8bbe31b52326983689/content/browser/portal/portal.cc
[modify] https://crrev.com/b521dfd717611f3615c0bf8bbe31b52326983689/content/browser/web_contents/web_contents_view_mac.h
[modify] https://crrev.com/b521dfd717611f3615c0bf8bbe31b52326983689/content/browser/web_contents/web_contents_view_aura.h
[modify] https://crrev.com/b521dfd717611f3615c0bf8bbe31b52326983689/content/browser/web_contents/web_contents_view_child_frame.cc
[modify] https://crrev.com/b521dfd717611f3615c0bf8bbe31b52326983689/content/browser/web_contents/web_contents_view_aura.cc
[modify] https://crrev.com/b521dfd717611f3615c0bf8bbe31b52326983689/content/browser/web_contents/web_contents_view_android.h
[modify] https://crrev.com/b521dfd717611f3615c0bf8bbe31b52326983689/content/browser/web_contents/web_contents_view_android.cc


### gi...@appspot.gserviceaccount.com (2023-10-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/37a1187c60ed169bcd4198847330081b18d91711

commit 37a1187c60ed169bcd4198847330081b18d91711
Author: Adithya Srinivasan <adithyas@chromium.org>
Date: Thu Oct 12 14:54:19 2023

Portals: Transfer DragSecurityInfo across portal activation

https://crrev.com/c/4874216 cancelled the drag on portal activation,
but this approach doesn't really work on Mac. This CL updates the
logic to transfer the drag security info across portal activation
instead (so the drag continues, but the drop fails), and fix the
issue on both Aura and Mac. It also includes a browser test for Aura.

Bug: 1482848
Change-Id: I8aad26c6794a140ba11237e9a7d44c8b11d2cb06
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4928028
Commit-Queue: Adithya Srinivasan <adithyas@chromium.org>
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: Kevin McNee <mcnee@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1208844}

[modify] https://crrev.com/37a1187c60ed169bcd4198847330081b18d91711/content/browser/web_contents/web_contents_view_mac.mm
[modify] https://crrev.com/37a1187c60ed169bcd4198847330081b18d91711/content/browser/web_contents/web_contents_view_child_frame.h
[modify] https://crrev.com/37a1187c60ed169bcd4198847330081b18d91711/content/browser/web_contents/web_contents_view_mac.h
[modify] https://crrev.com/37a1187c60ed169bcd4198847330081b18d91711/content/browser/web_contents/web_contents_view_android.h
[modify] https://crrev.com/37a1187c60ed169bcd4198847330081b18d91711/content/browser/web_contents/web_contents_view.h
[modify] https://crrev.com/37a1187c60ed169bcd4198847330081b18d91711/content/browser/portal/portal.cc
[modify] https://crrev.com/37a1187c60ed169bcd4198847330081b18d91711/content/browser/web_contents/web_contents_view_aura.h
[modify] https://crrev.com/37a1187c60ed169bcd4198847330081b18d91711/content/browser/web_contents/web_drag_dest_mac.mm
[modify] https://crrev.com/37a1187c60ed169bcd4198847330081b18d91711/chrome/browser/ui/views/drag_and_drop_interactive_uitest.cc
[modify] https://crrev.com/37a1187c60ed169bcd4198847330081b18d91711/content/browser/web_contents/web_contents_view_child_frame.cc
[modify] https://crrev.com/37a1187c60ed169bcd4198847330081b18d91711/content/browser/web_contents/web_contents_view_aura.cc
[modify] https://crrev.com/37a1187c60ed169bcd4198847330081b18d91711/content/browser/web_contents/web_contents_view_android.cc
[modify] https://crrev.com/37a1187c60ed169bcd4198847330081b18d91711/content/browser/web_contents/web_drag_dest_mac.h


### ad...@chromium.org (2023-10-12)

Issue has been fixed on Desktop platforms. Android doesn't have any security checks for cross-origin drag-drop currently (crbug.com/1488620).

### [Deleted User] (2023-10-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-12)

[Empty comment from Monorail migration]

### am...@google.com (2023-10-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-10-18)

Congratulations Thomas! The Chrome VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-10-23)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-18)

This issue was migrated from crbug.com/chromium/1482848?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>DataTransfer, Blink>Portals]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40072334)*
