# Security: Keyboard/Pointer Lock permission prompt does not elide origins correctly, allows origin spoof

| Field | Value |
|-------|-------|
| **Issue ID** | [341432425](https://issues.chromium.org/issues/341432425) |
| **Status** | Verified |
| **Severity** | Unknown |
| **Priority** | P3 |
| **Component** | UI>Browser>Permissions>Prompts |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | ta...@chromium.org |
| **Created** | 2024-05-18 |
| **Bounty** | $500.00 |

## Description

#### SUMMARY

Similar to [issue 341436934](https://issues.chromium.org/issues/341436934), the Keyboard/Pointer Lock [1] permission prompt does not elide origins correctly, which allows the origin shown in the prompt to be spoofed.

The root cause appears to be a pattern that affects other sensitive dialogs. These other instances will be reported separately.

[1] <https://chromestatus.com/feature/5142031990259712>

#### VULNERABILITY DETAILS

Current permission prompts elide origins safely, but the new Keyboard/Pointer Lock permission prompts do not elide origins correctly. The hostname is shown from the first character instead of from the last character, and is not intentionally elided in any way. The last part of the hostname (the eTLD+1) is not shown if the hostname is long enough.

The origin also wraps into multiple lines if it's long and contains characters that indicate a word break, such as dashes.

An attacker can use either an origin of underscores or dashes (for an effectively blank origin), or an origin starting with arbitrary text followed by underscores/dashes (e.g. `example.com____`, `chrome___`).

There is no ellipsis shown in the dialog when the origin is too long and cut off, so the usual indication of elision is not present.

An attacker can show the prompt in an `about:blank` or narrow popup window (known [issue 40082790](https://issues.chromium.org/issues/40082790)) with the spoofed origin over the target origin for a fairly convincing attack.

The Keyboard Lock and Pointer Lock permission prompts are both implemented via `ExclusiveAccessPermissionPromptView`, so the behaviors (and fixes) are identical for both. PoCs use Pointer Lock to demonstrate issue.

#### ROOT CAUSE

The root cause is the same pattern seen in [issue 341436934](https://issues.chromium.org/issues/341436934). See that issue's `Root Cause` section for details (to prevent repetition).

For the Keyboard/Pointer Lock permission prompt, `ExclusiveAccessPermissionPromptView::AddedToWidget()` [2] overrides  `PermissionPromptBaseView::AddedToWidget()` [3]. This override does not elide origins safely, following the same pattern as the other issue.

```
void ExclusiveAccessPermissionPromptView::AddedToWidget() {
  auto title_container = std::make_unique<views::FlexLayoutView>();
  title_container->SetOrientation(views::LayoutOrientation::kHorizontal);

  auto label = std::make_unique<views::Label>(
      GetWindowTitle(), views::style::CONTEXT_DIALOG_BODY_TEXT);
  label->SetHorizontalAlignment(gfx::ALIGN_LEFT);
  label->SetCollapseWhenHidden(true);
  label->SetMultiLine(true);
  label->SetProperty(
      views::kFlexBehaviorKey,
      views::FlexSpecification(views::MinimumFlexSizeRule::kScaleToZero,
                               views::MaximumFlexSizeRule::kScaleToMaximum,
                               /*adjust_height_for_width=*/true));
  AddElementIdentifierToLabel(*label, /*index*/ 0);

  title_container->AddChildView(std::move(label));

  GetBubbleFrameView()->SetTitleView(std::move(title_container));
}

```

[2] `ExclusiveAccessPermissionPromptView::AddedToWidget()` <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/permissions/permission_prompt_base_view.cc;l=51;drc=d12bb664d7632a41b96af48e736f7407aa5df291>

[3] `PermissionPromptBaseView::AddedToWidget()` <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/permissions/permission_prompt_base_view.cc;l=51;drc=d12bb664d7632a41b96af48e736f7407aa5df291>

POTENTIAL SOLUTION

Similar to [issue 341436934](https://issues.chromium.org/issues/341436934), use `CreateTitleOriginLabel()` or equivalent in Keyboard/Pointer Lock permission prompts and ensure other properties are safe.

The fix is in a different location, so it requires a separate patch.

#### VERSION

Chrome Version: 127.0.6487.0 Canary, 126.0.6478.8 Beta

On 125.0.6422.60 Stable, whole browser crashes, presumably because bisected commit below hasn't landed on Stable yet.

Requires `chrome://flags/#keyboard-and-pointer-lock-prompt` flag on all channels.

Operating System: Windows 10 Version 22H2 (Build 19045.4170)

#### BISECT

Starts reproducing on commit <https://chromium.googlesource.com/chromium/src/+/0f0b7f0ffad6c04b135823e776aed9a1fc3b4f16>

Landed in 126.0.6424.0 in April 17, 2024: <https://chromiumdash.appspot.com/commit/0f0b7f0ffad6c04b135823e776aed9a1fc3b4f16>

Verified repro down to 126.0.6424.0.

#### REPRODUCTION CASE

Prerequisites: Enable `chrome://flags/#keyboard-and-pointer-lock-prompt` flag

After testing, to reset the Keyboard/Pointer Lock permission to "Ask", go to the site's settings and look for the Pointer Lock. This does not yet appear in the content settings in the omnibar.

Note: Instead of copy/pasting the links below, you can also navigate to <https://aogarantiza.com/chromium/kplock-elision.html> and click the link for the corresponding scenario.

##### Scenario 1: Shown over another origin (via popup)

Note: My server doesn't have a valid SSL cert for this hostname, so you must manually proceed when the security interstitial is shown. This does not affect repro.

1. Navigate to <https://example.com____________________________________________________________.aogarantiza.com/chromium/kplock-elision.html?mode=popup>
2. Click anywhere on page
3. Click anywhere on popup
4. Click "Allow"

Observed: Origin in Pointer Lock permission prompt is shown as `example.com_____________`. Attacker is able to obtain permission while spoofing origin.

Expected: Origin in Pointer Lock permission prompt is shown as `..._____.aogarantiza.com`.

##### Scenario 2: Underscores (effectively blank origin)

1. Navigate to https://\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_.aogarantiza.com/chromium/kplock-elision.html
2. Click anywhere

Observed: Origin in Pointer Lock permission prompt is shown as `___________________`.

Expected: Origin in Pointer Lock permission prompt is shown as `..._____.aogarantiza.com`.

##### Scenario 3: Chrome spoof (arbitrary text)

1. Navigate to <https://chrome_________________________________________________________.aogarantiza.com/chromium/kplock-elision.html>
2. Click anywhere

Observed: Origin in Pointer Lock permission prompt is shown as `chrome_______________`.

Expected: Origin in Pointer Lock permission prompt is shown as `..._____.aogarantiza.com`.

##### Scenario 4: Origin spoof (basic example of Scenario 1)

Note: My server doesn't have a valid SSL cert for this hostname, so you must manually proceed when the security interstitial is shown. This does not affect repro.

1. Navigate to <https://example.com____________________________________________________________.aogarantiza.com/chromium/kplock-elision.html>
2. Click anywhere

Observed: Origin in Pointer Lock permission prompt is shown as `example.com_____________`.

Expected: Origin in Pointer Lock permission prompt is shown as `..._____.aogarantiza.com`.

#### CREDIT INFORMATION

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- kplock-elision.html (text/html, 2.6 KB)
- kplock-elision.mp4 (video/mp4, 2.6 MB)

## Timeline

### ph...@chromium.org (2024-05-20)

Security shepherds: I can reproduce.
engedy@: Could you help triage this permission prompt related bug?

### al...@alesandroortiz.com (2024-05-22)

~~FYI, I'm planning to work on a patch for this issue, after implementing a patch for [issue 341436934](https://issues.chromium.org/issues/341436934).~~ See [#comment4](https://issues.chromium.org/issues/341432425#comment4).

### al...@alesandroortiz.com (2024-05-24)

The same change made in this CL is probably the best fix for this:
<https://chromium-review.googlesource.com/c/chromium/src/+/5497035>

Making the same change in `ExclusiveAccessPermissionPromptView` should resolve the issue, but I'll need to verify.

I'll let someone else submit the patch since it's a trivial patch (and I don't have trybot access).

### en...@chromium.org (2024-07-08)

Routing to Takumi who is working on this specific prompt. Can you please take a look?

Once fixed, note to @amyressler & VRP panel -- I was not sure if we need to de-dupe this against [Issue 40095827](https://issues.chromium.org/issues/40095827), which covers the broader problem of origins being incorrectly truncated over various UI surfaces; while on the flipside, a different CL will be required to fix this variant. I have provided some more context for you per email, search for "[crbug.com/40095827](https://crbug.com/40095827)" in the subject.

### ap...@google.com (2024-07-24)

Project: chromium/src
Branch: main

commit 066cccca5ba84c465fc4f73091b82da6efd17c77
Author: Takumi Fujimoto <takumif@chromium.org>
Date:   Wed Jul 24 12:23:52 2024

    Allow line breaks in ExclusiveAccessPermissionPromptView
    
    This allows long origins to be shown without being elided.
    
    Bug: 341432425
    Change-Id: I454b6009d02795568ce5b9ea3d9e0fe8de6af1d7
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5736928
    Commit-Queue: Ravjit Uppal <ravjit@chromium.org>
    Reviewed-by: Ravjit Uppal <ravjit@chromium.org>
    Auto-Submit: Takumi Fujimoto <takumif@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1332263}

M       chrome/browser/ui/views/permissions/exclusive_access_permission_prompt_view.cc

https://chromium-review.googlesource.com/5736928


### al...@alesandroortiz.com (2024-07-24)

~~Hm, I tested on snapshot build 1332276 [1] which should have the commit above, but it doesn't seem to be fixed using the PoCs from report. Behavior is the same as before.~~

~~Perhaps there's additional label properties that need to be set for multiline logic to work properly in the scenarios above.~~

~~Takumi, can you please take another look? Thanks.~~

Nevermind, I accidentally tested wrong build.

[1] <https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Win_x64/1332276/>

### al...@alesandroortiz.com (2024-07-24)

Disregard my prior comment. I accidentally tested wrong build.

### al...@alesandroortiz.com (2024-07-24)

Verified as fixed on snapshot build 1332276 [1].

Thanks for fix! Feel free to mark this crbug as fixed.

[1] <https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Win_x64/1332276/>

### ta...@chromium.org (2024-07-24)

Thanks for verifying!

### sp...@google.com (2024-08-01)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
Thank you reward for the nudge related to these permissions prompt origin elision issues and reports that provided us with good testcases; however, as c#5 conveys, these issues were already known and well-documented with other reports merged into the canonical issue as duplicates. 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-08-02)

Thank you for the report and effort, Alesandro!
As explained in the reward notification, we consider this a duplicate of previous documented defect, but appreciate the nudge to land these specific changes here.

### al...@alesandroortiz.com (2024-08-17)

Thanks for the reward. :) I understand, since it was already a priority for the year per other bug (I hadn't seen it prior to fixes) and work was already planned.

### pe...@google.com (2024-10-31)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/341432425)*
