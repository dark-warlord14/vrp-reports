# Security: PEPC prompt can be obscured by Video/Document PiP window

| Field | Value |
|-------|-------|
| **Issue ID** | [342194497](https://issues.chromium.org/issues/342194497) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Permissions>Prompts |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | st...@chromium.org |
| **Created** | 2024-05-23 |
| **Bounty** | $4,000.00 |

## Description

#### SUMMARY

The Page Embedded Permission Control (PEPC) prompt can be obscured by a Video or Document PiP window, allowing a page to obtain permissions without user awareness.

The current address bar permission prompts do check for PiP window occlusion.

Interestingly, it seems that PEPC also has PiP occlusion checks, but they aren't working as expected for some reason.

To reduce user interaction, a compromised renderer can open the PiP window ([issue 338398040](https://issues.chromium.org/issues/338398040)) and PEPC prompt without user interaction.

Based on this commit [1], PEPC will be in origin trial soon (although I haven't seen a milestone yet).

PEPC is behind a flag since M121 [2].

[1] <https://chromium.googlesource.com/chromium/src/+/7fb7ce92aac3851d7e7245b19b9526730a23a923>

[2] <https://chromestatus.com/feature/5125006551416832>

#### VULNERABILITY DETAILS

A page can show a Video or Document PiP window over a normal window with a PEPC prompt to obscure the prompt.

An attacker can instruct the user to press keys while the PEPC prompt is obscured, resulting in the user granting permissions without awareness.

Opening the PEPC prompt does not consume user activation, so an attacker can open both a PEPC prompt and a PiP window with a single user interaction.

To move focus from the PiP window to the PEPC prompt, the attacker doesn't need to do anything since opening a PEPC prompt will steal focus from other windows.

After commit `6acd413854481030263494f1ee8e5da778812475` (May 9, 2024), the PEPC element can no longer be focused with JavaScript. Prior to this commit, the first `Tab` keypress to focus the PEPC element wasn't necessary.

This requires the `PermissionElement` flag. While not required for most attacks, with `PermissionElementDialogPositioning` enabled, the attacker has more flexibility to position the PEPC prompt behind the PiP window.

This does not seem to repro with existing address bar permission prompts, only with PEPC prompts. I still have to test another prompt that may also be affected (will update in comments).

#### ROOT CAUSE

I initially thought the PEPC prompt was missing PiP window occlusion checks, but turns out it does have occlusion checks. This looks more like a regression, since occlusion checks worked up to commit `77cfa22d7ff196ba21ca866982c7715c27321c2e` [3].

The only code changes that alter production behavior are in `permission_prompt_base_view.cc`.

Notably, this block is removed:

```
-  std::optional<gfx::Rect> pip_window_bounds =
-      PictureInPictureWindowManager::GetInstance()
-          ->GetPictureInPictureWindowBounds();
-
-  return pip_window_bounds &&
-         pip_window_bounds->Intersects(button->GetBoundsInScreen());

```

And the return value of `ShouldIgnoreButtonPressedEventHandling()` now fully depends on `OnOcclusionStateChanged()`:

```
 bool PermissionPromptBaseView::ShouldIgnoreButtonPressedEventHandling(
     View* button,
     const ui::Event& event) const {
-  // Ignore the key pressed event if the button row bounds intersect with PiP
-  // windows bounds.
-  if (!event.IsKeyEvent()) {
-    return false;
-  }
+  // Ignore button pressed events whenever we're occluded by a
+  // picture-in-picture window.
+  return occluded_by_picture_in_picture_;
+}
// ...
+void PermissionPromptBaseView::OnOcclusionStateChanged(bool occluded) {
+  occluded_by_picture_in_picture_ = occluded;
}

```

My best guess is that `OnOcclusionStateChanged()` isn't being called as expected for this scenario, and `occluded_by_picture_in_picture_` is `false` despite occlusion, although I cannot quite tell why yet.

Using `PictureInPictureOcclusionTracker` is a newer way to track PiP window occlusion, and the intent [4] is to roll it out to all places that need to check for PiP window occlusion.

Other UIs that have PiP occlusion checks use an older method, which is essentially this pattern (same pattern that was removed above):

```
  std::optional<gfx::Rect> pip_window_bounds =
      PictureInPictureWindowManager::GetInstance()
          ->GetPictureInPictureWindowBounds();

  return pip_window_bounds &&
         pip_window_bounds->Intersects(button->GetBoundsInScreen());

```

I'm guessing this type of check still works, because other prompts I've tested so far such as autofill aren't affected by the same regression.

Also worth noting that both `PermissionPromptBubbleBaseView` (normal address bar permission prompts) and `EmbeddedPermissionPromptBaseView` (PEPC prompts) inherit from the same `PermissionPromptBaseView` class, but only PEPC seems affected. This suggests that `OnOcclusionStateChanged()` is being called as expected in some cases, but isn't in other cases.

I'll defer to folks more familiar with this code to finish analyzing why `OnOcclusionStateChanged()` probably isn't being called as expected (or if something else is going wrong).

[3] `[picture-in-picture] Disable permission prompt buttons when occluded` (February 2024) <https://chromium.googlesource.com/chromium/src/+/77cfa22d7ff196ba21ca866982c7715c27321c2e>

[4] From this comment: <https://issues.chromium.org/issues/338634231#comment9>

> The autofill pip detection stuff was written before the PictureInPictureOcclusionTracker existed, [...] so it'll be good to change it to use the tracker. And yeah, there are other UIs we want to use the tracker for but haven't gotten around to yet

#### VERSION

Chrome Version: 127.0.6495.0 Canary, 125.0.6422.76 Stable

Operating System: Windows 10 Version 22H2 (Build 19045.4170)

#### BISECT

Starts reproducing on commit <https://chromium.googlesource.com/chromium/src/+/77cfa22d7ff196ba21ca866982c7715c27321c2e>

Landed in 124.0.6319.0 in February 2024: <https://chromiumdash.appspot.com/commit/77cfa22d7ff196ba21ca866982c7715c27321c2e>

Verified repro down to 124.0.6319.0.

Some older versions require a slightly modified PoC, but the impact is the same.

#### REPRODUCTION CASE

Note: The PoC uses Document PiP, but this also works with Video PiP.

Prerequisites: Run Chrome with `--enable-features=PermissionElement` flag. Optionally, also enable the `PermissionElementDialogPositioning` flag.

1. Navigate to <https://alesandroortiz.com/security/chromium/pepc-pip.html>
2. Press tab, then enter
3. Press tab twice, then press enter

Observed: PEPC prompt remains open under PiP window. User is able to interact with prompt. Attacker is able to obtain permissions without user awareness.

Expected: PEPC prompt closes or is not interactive when under a PiP window. Attacker cannot obtain permissions without user awareness.

#### CREDIT INFORMATION

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [pepc-pip.html](attachments/pepc-pip.html) (text/html, 1.8 KB)
- [pepc-pip.mp4](attachments/pepc-pip.mp4) (video/mp4, 1.0 MB)
- [kplock-pip.html](attachments/kplock-pip.html) (text/html, 1.2 KB)
- [kplock-pip.mp4](attachments/kplock-pip.mp4) (video/mp4, 1.1 MB)

## Timeline

### ps...@google.com (2024-05-23)

Thank you OP. 

Verified that this works. Assigning based on reproducing CL.

@steimel could you please take a look or assign if you are not the right person for this task?

### al...@alesandroortiz.com (2024-05-23)

This also repros with the Keyboard/Pointer Lock permission prompt `ExclusiveAccessPermissionPromptView`, which also inherits from `PermissionPromptBaseView`.

The Keyboard Lock and Pointer Lock permission prompts are both implemented via `ExclusiveAccessPermissionPromptView`, so the behaviors (and fixes) are identical for both Keyboard Lock and Pointer Lock. PoCs use Pointer Lock to demonstrate issue.

#### REPRODUCTION CASE

Note: The PoC uses Document PiP, but this also works with Video PiP.

After testing, to reset the Keyboard/Pointer Lock permission to "Ask", go to the site's settings and look for the Pointer Lock. This does not yet appear in the content settings in the omnibar.

Prerequisites:

1. Run Chrome with `--enable-features=PermissionElement` flag. Optionally, also enable the `PermissionElementDialogPositioning` flag.
2. Also enable `chrome://flags/#keyboard-and-pointer-lock-prompt` flag.

##### Scenario: Pointer Lock

1. Navigate to <https://alesandroortiz.com/security/chromium/kplock-pip.html>
2. Press tab, then enter
3. Press tab twice, then press enter

Observed: Pointer Lock permission prompt remains open under PiP window. User is able to interact with prompt. Attacker is able to obtain permissions without prior user awareness (overlay is shown after obtaining lock).

Expected: Pointer Lock permission prompt closes or is not interactive when under a PiP window. Attacker cannot obtain permissions without prior user awareness.

### st...@chromium.org (2024-05-23)

Thanks for the detailed report! Seems like the issue is that we start tracking occlusion in `PermissionPromptBaseView::AddedToWidget()`, but some of its subclasses (including `ExclusiveAccessPermissionPromptView`) override `AddedToWidget()` without calling the superclass implementation. We don't actually want to call the superclass implementation here, so instead I'm splitting that logic into another method that the subclasses can call to start the tracking.

Fix is at crrev.com/c/5564973

### al...@alesandroortiz.com (2024-05-24)

Ah, thanks for finishing the analysis! I should have noticed the occlusion tracking was started in `AddedToWidget()`, given I was looking at that and its overrides this week for another issue.

The CL LGTM.

I see you also updated `PermissionPromptBubbleTwoOriginsView` which means the Storage Access API (SAA) prompt presumably was also affected.

### ap...@google.com (2024-05-24)

Project: chromium/src
Branch: main

commit 663358207f305a0a18dd7b62b9c3d8a5b128b319
Author: Tommy Steimel <steimel@chromium.org>
Date:   Fri May 24 14:35:28 2024

    Track picture-in-picture occlusion for more permission prompts
    
    Currently, we prevent input on permission prompts that are occluded by
    a picture-in-picture window. We start tracking the occlusion in
    `PermissionPromptBaseView::AddedToWidget()`. However, some subclasses
    of PermissionPromptBaseView override `AddedToWidget()` and purposefully
    don't call `PermissionPromptBaseView::AddedToWidget()`, which results
    in those prompts not properly tracking picture-in-picture occlusion.
    
    This CL moves the tracking initialization logic into a separate method,
    so that subclasses can call it inside their `AddedToWidget()`
    implementations to properly track occlusion.
    
    Bug: 342194497
    Change-Id: I3f8e2121c4641e66ebe49ae3e88f5b6c76d228b2
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5564973
    Reviewed-by: Elias Klim <elklm@chromium.org>
    Commit-Queue: Tommy Steimel <steimel@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1305696}

M       chrome/browser/ui/views/permissions/embedded_permission_prompt_base_view.cc
M       chrome/browser/ui/views/permissions/exclusive_access_permission_prompt_view.cc
M       chrome/browser/ui/views/permissions/permission_prompt_base_view.cc
M       chrome/browser/ui/views/permissions/permission_prompt_base_view.h
M       chrome/browser/ui/views/permissions/permission_prompt_bubble_two_origins_view.cc

https://chromium-review.googlesource.com/5564973


### al...@alesandroortiz.com (2024-05-28)

Verified as fixed in 127.0.6507.0 Canary on Windows 10 Version 22H2 (Build 19045.4412), using these PoCs:

- <https://alesandroortiz.com/security/chromium/pepc-pip.html>
- <https://alesandroortiz.com/security/chromium/kplock-pip.html>

Also verified Storage Access API (SAA) prompt as fixed by manually testing.

Thanks for quick fix!

### sp...@google.com (2024-06-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $4000.00 for this report.

Rationale for this decision:
$3,000 for high quality report of security UI spoofing, but mitigated by many user gestures + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-05)

Congratulations, Alesandro! Thank you for your efforts and reporting this issue to us!

### al...@alesandroortiz.com (2024-06-05)

Thanks for the reward!

### pe...@google.com (2024-09-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/342194497)*
