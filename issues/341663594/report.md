# Security: PEPC prompt renders outside initiator window in small windows

| Field | Value |
|-------|-------|
| **Issue ID** | [341663594](https://issues.chromium.org/issues/341663594) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Permissions>Prompts |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2024-05-21 |
| **Bounty** | $2,000.00 |

## Description

#### SUMMARY

The Page Embedded Permission Control (PEPC) prompt will render outside the initiator window if the window is smaller than the prompt. This causes the window UI, including address bar and other browser UI, to be obscured.

When chained with [issue 341436934](https://issues.chromium.org/issues/341436934) (origin spoofing in PEPC prompt), this can result in more effective origin spoofs. (See chained PoC.)

Based on this commit [1], PEPC will be in origin trial soon (although I haven't seen a milestone yet).

PEPC is behind a flag since M121 [2].

[1] <https://chromium.googlesource.com/chromium/src/+/7fb7ce92aac3851d7e7245b19b9526730a23a923>

[2] <https://chromestatus.com/feature/5125006551416832>

#### VULNERABILITY DETAILS

The PEPC prompt doesn't seem to be clipped within the browser window, nor does the prompt hide when the window is too small for full display. The prompt is large enough to obscure window/browser UI.

When all window/browser UI is obscured, the PEPC prompt can appear as actual browser UI from the page, despite it coming from the small window. If the small window is shown over another origin, this can lead to origin confusion by user since the prompt will appear to be from the page (other than the origin display within the prompt itself).

An attacker can position the PEPC prompt either over the current permission prompt location near the address bar, or within the page to simulate a normal PEPC prompt.

An attacker can show a PEPC in an `about:blank` popup window or a narrow popup window (known [issue 40082790](https://issues.chromium.org/issues/40082790)) over the target origin for a convincing attack, especially when chained with [issue 341436934](https://issues.chromium.org/issues/341436934) to show a spoofed origin in the PEPC prompt.

POTENTIAL SOLUTION

Hide the PEPC prompt if the window is too large to display, or somehow ensure the prompt never obscures the address bar even in a small window. Given the PEPC element itself is required to be fully visible in the window, it's probably reasonable to hide the PEPC prompt if it isn't fully visible within the window.

#### VERSION

Chrome Version: 127.0.6491.0 Canary, 125.0.6422.60 Stable.

Requires `--enable-features=PermissionElement` flag on all channels.

Operating System: Windows 10 Version 22H2 (Build 19045.4170)

#### BISECT

Starts reproducing on commit <https://chromium.googlesource.com/chromium/src/+/2790300f72201c55a60ff9c7f83e03dcc85432d1>

Landed in 120.0.6048.0 in October 2023: <https://chromiumdash.appspot.com/commit/2790300f72201c55a60ff9c7f83e03dcc85432d1>

Verified repro down to 120.0.6048.0.

Prior to commit <https://chromium.googlesource.com/chromium/src/+/b5bed932501052e09f05fb975bd302f06a3107c7>, requires `--enable-features=PermissionElement --enable-blink-features=PermissionElement` flags. After that commit, only requires `--enable-features=PermissionElement` flag.

#### REPRODUCTION CASE

Prerequisites: Run Chrome with `--enable-features=PermissionElement` flag.

Note: Instead of copy/pasting the links below, you can also navigate to <https://aogarantiza.com/chromium/pepc-bounds.html> and click the link for the corresponding scenario.

##### Scenario 1: Chained with [issue 341436934](https://issues.chromium.org/issues/341436934), using about:blank popup

Note: My server doesn't have a valid SSL cert for this hostname, so you must manually proceed when the security interstitial is shown. This does not affect repro.

1. Navigate to <https://example.com____________________________________________________________.aogarantiza.com/chromium/pepc-bounds.html>
2. Click anywhere once
3. Click permission element
4. Click "Allow"

##### Scenario 2: Chained with [issue 341436934](https://issues.chromium.org/issues/341436934), using narrow popup spoof

Note: My server doesn't have a valid SSL cert for this hostname, so you must manually proceed when the security interstitial is shown. This does not affect repro.

1. Navigate to <https://example.com____________________________________________________________.aogarantiza.com/chromium/pepc-bounds.html?mode=popup-spoof>
2. Click anywhere once
3. Click permission element
4. Click "Allow"

##### Scenario 3: Standalone, using about:blank popup

1. Navigate to <https://aogarantiza.com/chromium/pepc-bounds.html?mode=standalone>
2. Click anywhere once
3. Click permission element
4. Click "Allow"

For all scenarios:

Observed: PEPC prompt renders outside the initiator window. Attacker is able to obtain permission while PEPC prompt renders outside of initiator window and over another origin.

Expected: PEPC prompt is hidden if initiator window is too small. Attacker is unable to obtain permission while PEPC prompt renders outside of initiator window.

#### CREDIT INFORMATION

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [pepc-bounds.html](attachments/pepc-bounds.html) (text/html, 4.2 KB)
- [pepc-bounds.mp4](attachments/pepc-bounds.mp4) (video/mp4, 11.6 MB)
- [prompt-pepc.png](attachments/prompt-pepc.png) (image/png, 35.2 KB)
- [prompt-addressbar.png](attachments/prompt-addressbar.png) (image/png, 37.7 KB)
- [pepc-offscreen.html](attachments/pepc-offscreen.html) (text/html, 2.1 KB)
- [pepc-offscreen-after-fix.mp4](attachments/pepc-offscreen-after-fix.mp4) (video/mp4, 2.5 MB)
- [pepc-offscreen-before-fix.mp4](attachments/pepc-offscreen-before-fix.mp4) (video/mp4, 1.9 MB)

## Timeline

### ps...@google.com (2024-05-21)

Security Shepard: Reproduced report in redshell

engedy@ this is a related bug with https://g-issues.chromium.org/issues/341436934, set severity to s3

### al...@alesandroortiz.com (2024-05-21)

Filed similar [issue 342003160](https://issues.chromium.org/issues/342003160) for another prompt. These two issues may or may not have the same fix, depending on how the fix is implemented.

### en...@chromium.org (2024-05-22)

alesandro@, which of the three attacks flavors can be reproduces with the traditional permission prompt?

### al...@alesandroortiz.com (2024-05-22)

If you're referring to this:

> An attacker can position the PEPC prompt either over the current permission prompt location near the address bar, or within the page to simulate a normal PEPC prompt.

I didn't mean that the issue also occurs with traditional permission prompts; only that a PEPC prompt can look like a traditional permission prompt if placed in the same position.

Scenarios 1 and 2 move the PEPC prompt to appear below the address bar, in the same position as a traditional permission prompt. See attached screenshots showing both types of prompts in the same position.

Most users probably wouldn't be able to tell the difference between a PEPC prompt and traditional permission prompt shown in this position (other than the slightly unusual origin display, but this might not be noticed at a glance, or an attacker can use a longer origin in the spoof, such as `secure.call.meet.google.com` (really `secure.call.meet.google.com.attacker.com`), that would remove the need for underscores).

### ap...@google.com (2024-06-11)

Project: chromium/src
Branch: main

commit 3fa6bf8f9d3b51268f16fb7cac0ad1fcf611222f
Author: Andy Paicu <andypaicu@chromium.org>
Date:   Tue Jun 11 14:13:08 2024

    [PEPC] Ensure PEPC prompt can not overlap browser UI
    
    Ensure the PEPC prompt can not be placed above the top bound of the
    container, in order to prevent it obfuscating potentially critical
    browser UI. The kLegacyPrompt positioning option will still use the
    legacy bevahior of anchoring to the page info view.
    
    Fixed: 342318870
    Fixed: 341663594
    Change-Id: I1a1e49a13afb724e2864f92a14d6a91e4b9eab2f
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5612401
    Reviewed-by: Kamila Hasanbega <hkamila@chromium.org>
    Commit-Queue: Andy Paicu <andypaicu@chromium.org>
    Reviewed-by: Kamila Hasanbega <hkamila@google.com>
    Cr-Commit-Position: refs/heads/main@{#1313391}

M       chrome/browser/ui/views/permissions/embedded_permission_prompt_base_view.cc

https://chromium-review.googlesource.com/5612401


### al...@alesandroortiz.com (2024-06-11)

Verified the address bar is no longer obscured in snapshot build 1313413 [1] on Windows 10, using the three available positioning options [2].

However, the duplicate [issue 342003160](https://issues.chromium.org/issues/342003160) still repros. That may indeed require a separate patch. I'll make a comment over there too.

Would a more robust fix be to hide the prompt completely if the window cannot contain the PEPC prompt? It is meant to be *embedded* after all, but the fix still allows the prompt to render outside the window. This is done for some sensitive UI such as FedCM ([issue 338233148](https://issues.chromium.org/issues/338233148)).

For example, if an attacker were to use a current or future PEPC prompt origin spoof vulnerability such as [issue 341436934](https://issues.chromium.org/issues/341436934), the current fix wouldn't help since the address bar in popups can be easily manipulated to spoof the origin there too, as shown in Scenarios 1 and 2, so there wouldn't be a correct origin display anywhere.

I'm aware current permission prompts also render outside the window, but PEPC doesn't feel like it should render outside the window given the goals of PEPC. Hiding if window is too small would reduce future risk specifically with PEPC if there were a future origin spoof only affecting PEPC prompts.

[1] <https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Win_x64/1313413/>

[2] <https://source.chromium.org/chromium/chromium/src/+/main:components/permissions/features.h;l=106;drc=20135c10f0869fdefb75d990ec84143a649d84c3>

### al...@alesandroortiz.com (2024-06-11)

Actually, will follow up soon with an additional impact + PoC. That will show the need to hide the prompt in small windows.

### al...@alesandroortiz.com (2024-06-12)

The PoC below shows the PEPC prompt is now mostly off screen after the fix in [#comment6](https://issues.chromium.org/issues/341663594#comment6) (commit 3fa6bf8f9d3b51268f16fb7cac0ad1fcf611222f).

Before the fix, the prompt was more visible so an attack wasn't really feasible. Also attached are videos of the PoC running before and after the fix.

This is similar to [issue 338233148](https://issues.chromium.org/issues/338233148) affecting another UI (specifically see <https://issues.chromium.org/issues/338233148#comment31> )

Also want to note that steps 2 and 3 can be performed by a compromised renderer.

#### REPRODUCTION CASE

Prerequisites:

- Run Chrome with `--enable-features=PermissionElement` flag.
- Use Chrome version after commit 3fa6bf8f9d3b51268f16fb7cac0ad1fcf611222f (position 1313391)

1. Navigate to <https://alesandroortiz.com/security/chromium/pepc-offscreen.html>
2. Press any key once
3. Press tab once, then press enter
4. Press tab twice, then press enter

Observed: PEPC prompt is shown mostly off screen. User is able to interact with prompt. Attacker is able to obtain permission with minimal or no user awareness.

Expected: PEPC prompt is shown on screen at all times, similar to current permission prompts. If offscreen or in a small window, prompt is hidden or made non-interactive.

### en...@chromium.org (2024-06-12)

Procedural question: should [issue 342003160](https://issues.chromium.org/issues/342003160) actually marked as a duplicate of this? AFAIU, it is a separate implementation and is launched separately (not sure about the current implementation readiness).

### al...@alesandroortiz.com (2024-06-12)

I also have the same question: <https://issues.chromium.org/issues/342003160#comment4>

That issue still repros even after this issue's fix, so it requires its own patch, even if similar.

### ap...@google.com (2024-06-24)

Project: chromium/src
Branch: refs/branch-heads/6533

commit 7c5226639ef328894bf0ab984c427804c3baa55a
Author: Andy Paicu <andypaicu@chromium.org>
Date:   Mon Jun 24 07:52:47 2024

    [PEPC] Ensure PEPC prompt can not overlap browser UI
    
    Ensure the PEPC prompt can not be placed above the top bound of the
    container, in order to prevent it obfuscating potentially critical
    browser UI. The kLegacyPrompt positioning option will still use the
    legacy bevahior of anchoring to the page info view.
    
    (cherry picked from commit 3fa6bf8f9d3b51268f16fb7cac0ad1fcf611222f)
    
    Fixed: 342318870
    Fixed: 341663594
    Change-Id: I1a1e49a13afb724e2864f92a14d6a91e4b9eab2f
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5612401
    Reviewed-by: Kamila Hasanbega <hkamila@chromium.org>
    Commit-Queue: Andy Paicu <andypaicu@chromium.org>
    Reviewed-by: Kamila Hasanbega <hkamila@google.com>
    Cr-Original-Commit-Position: refs/heads/main@{#1313391}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5645671
    Auto-Submit: Andy Paicu <andypaicu@chromium.org>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6533@{#593}
    Cr-Branched-From: 7e0b87ec6b8cb5cb2969e1479fc25776e582721d-refs/heads/main@{#1313161}

M       chrome/browser/ui/views/permissions/embedded_permission_prompt_base_view.cc

https://chromium-review.googlesource.com/5645671


### sp...@google.com (2024-08-01)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
$1,000 for report of lower impact security UI issue + $1,000 bisect bonus


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-08-02)

Congratulations, Alesandro! Thanks for your efforts and reporting this issue to us!

### al...@alesandroortiz.com (2024-08-22)

Thanks for the reward!

### pe...@google.com (2024-09-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/341663594)*
