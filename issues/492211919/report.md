# Missing Browser-Side Sandbox Enforcement for kPointerLock

| Field | Value |
|-------|-------|
| **Issue ID** | [492211919](https://issues.chromium.org/issues/492211919) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Input>PointerLock, Blink>SecurityFeature>IFrameSandbox, Internals>Sandbox>SiteIsolation |
| **Platforms** | Mac |
| **Reporter** | mi...@bountyy.fi |
| **Assignee** | mi...@bountyy.fi |
| **Created** | 2026-03-12 |
| **Bounty** | $1,500.00 |

## Description

# Steps to reproduce the problem

1. `RenderWidgetHostImpl::RequestMouseLock()` does not check the
   `WebSandboxFlags::kPointerLock` sandbox flag. A compromised renderer
   inside a sandboxed frame (without `allow-pointer-lock`) can call
   `FrameWidgetInputHandler::RequestMouseLock` over Mojo IPC directly,
   bypassing the renderer-side check and obtaining pointer lock from the
   browser process.

## Severity

**High** - Sandbox policy bypass from compromised renderer process.

Comparable to [Bug 491676472](https://issues.chromium.org/issues/491676472) (allow-modals missing browser-side check,
fixed 2025-03-12). That bug was assigned Security\_Severity-High and
fixed with `bad_message::ReceivedBadMessage()`.

## Component

- Primary: `content/browser/renderer_host/render_widget_host_impl.cc`
- Secondary: `content/browser/web_contents/web_contents_impl.cc`
- Mojo interface: `blink.mojom.FrameWidgetInputHandler::RequestMouseLock`

## Affected Versions

All current Chrome stable/beta versions (unfixed as of 2026-03-12):

- Chrome 145.0.7632.160 (Stable, arm64, macOS) - verified
- Chrome 146.0.7680.72 (next Stable, branch pos 1582197) - unfixed
- Chromium main - unfixed

Note: The comparable kModals fix ([Bug 491676472](https://issues.chromium.org/issues/491676472)) landed at Cr-Commit-Position
1598123, which is newer than both 145 stable (pos ~1568190) and 146
stable (pos ~1582197). kPointerLock fix has not landed anywhere.

2.
3.

# Problem Description

## Root Cause

Renderer-side (`PointerLockController::RequestPointerLock`) correctly
checks the sandbox flag and blocks the request:

```
// third_party/blink/renderer/core/page/pointer_lock_controller.cc:94
if (window->IsSandboxed(WebSandboxFlags::kPointerLock)) {
    resolver->RejectWithSecurityError(...);
    return;
}
// calls: GetWidgetForLocalRoot()->RequestMouseLock(...)

```

But the browser-side handler does NOT re-validate:

```
// content/browser/renderer_host/render_widget_host_impl.cc:3281
void RenderWidgetHostImpl::RequestMouseLock(
    bool from_user_gesture,
    bool unadjusted_movement,
    RequestMouseLockCallback response) {
  // ❌ MISSING: IsSandboxed(WebSandboxFlags::kPointerLock) check
  if (IsPointerLocked()) { ... }
  if (!view_ || !view_->CanBePointerLocked()) { ... }
  delegate_->RequestToLockPointer(this, from_user_gesture, ...);
}

```

`WebContentsImpl::RequestToLockPointer` (called next) checks for
fenced frames but NOT for sandboxed frames:

```
// content/browser/web_contents/web_contents_impl.cc:5091
void WebContentsImpl::RequestToLockPointer(...) {
  if (render_widget_host->frame_tree()->is_fenced_frame()) {
    ReceivedBadMessage(...);  // ✅ fenced frame check
    return;
  }
  // ❌ NO: GetSandboxFlags() & WebSandboxFlags::kPointerLock
  delegate_->RequestPointerLock(this, user_gesture, ...);
}

```
## Attack Scenario

As an attacker with code execution in a renderer process
(e.g. via a V8 or Blink memory corruption bug):

1. The renderer is hosting a sandboxed iframe (sandbox="allow-scripts",
   no allow-pointer-lock).
2. Normal pointer lock is blocked by renderer check.
3. Attacker patches renderer or calls Mojo IPC directly:
   `FrameWidgetInputHandler::RequestMouseLock(true, false, callback)`
4. Browser grants pointer lock - cursor disappears, all mouse movement
   events captured by the sandboxed frame.

**As an attacker I could:**

- Capture the mouse cursor from a privileged parent frame context
- Perform UI redress attacks against the user (cursor hidden, fake UI shown)
- Bypass the `allow-pointer-lock` sandboxing contract that sites rely on
  to safely embed third-party content

## PoC

See attached `index.html`. It demonstrates:

1. The renderer-side check correctly blocks pointer lock via normal JS.
2. The missing browser-side check (shown via code reference).
3. A compromised renderer can call the Mojo IPC directly to bypass.

To reproduce the FULL bypass (requires patched renderer or Mojo fuzzer):

```
# Call FrameWidgetInputHandler::RequestMouseLock(true, false)
# from a renderer hosting a sandbox="allow-scripts" iframe
# without allow-pointer-lock. Browser grants the lock.

```
## Comparison: [Bug 491676472](https://issues.chromium.org/issues/491676472) (Fixed)

The just-fixed `allow-modals` bug had the identical pattern:

```
// BEFORE fix: RunJavaScriptDialog() had no IsSandboxed(kModals) check
// AFTER fix (render_frame_host_impl.cc:7251):
if (IsSandboxed(WebSandboxFlags::kModals)) {
    bad_message::ReceivedBadMessage(GetProcess(),
        bad_message::RFH_JS_DIALOG_FROM_SANDBOXED_FRAME);
    return;
}

```
## Proposed Fix

In `RenderWidgetHostImpl::RequestMouseLock()`:

```
// Get the focused frame and check its sandbox flags
if (RenderFrameHostImpl* rfh = GetFocusedFrame()) {
  if (rfh->IsSandboxed(WebSandboxFlags::kPointerLock)) {
    bad_message::ReceivedBadMessage(
        GetProcess(),
        bad_message::RWHI_POINTER_LOCK_FROM_SANDBOXED_FRAME);
    std::move(response).Run(
        blink::mojom::PointerLockResult::kPermissionDenied,
        mojo::NullRemote());
    return;
  }
}

```

Also add corresponding test to
`content/browser/security_exploit_browsertest.cc` (same file as the
kModals fix test).

## Additional Notes

- Other sandbox flags may have similar missing browser-side checks.
  Recommend auditing: `kDownloads`, `kOrientationLock`,
  `kPresentationController`, `kDocumentDomain`.
- `kPopups` already has browser-side check (CreateNewWindow, line 10092).
- `kTopNavigationByUserActivation` has browser-side check (line 983).
- `kModals` just got its check ([Bug 491676472](https://issues.chromium.org/issues/491676472)).

# Summary

Missing Browser-Side Sandbox Enforcement for kPointerLock

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A \

## Attachments

- [poc_chrome.html](attachments/poc_chrome.html) (text/html, 6.2 KB)

## Timeline

### ch...@google.com (2026-03-13)

Setting Priority to P3 to match Severity s3. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### mi...@bountyy.fi (2026-03-19)

Flagging that this report appears unassigned. The companion bugs 492209810 (kPresentationController) and 492198556 (kOrientationLock) were both assigned within hours of filing. Happy to provide any additional information needed for triage.

Mihalis Haatainen
Bountyy Oy

### mi...@bountyy.fi (2026-03-23)

Following up - this remains unassigned while companion issues 492209810 and 492198556 are actively assigned. The root cause and fix location are identical to those bugs. Happy to assist triage.

### mi...@bountyy.fi (2026-04-02)

This remains unassigned while 492209810 and 492198556 are actively assigned. Root cause and fix are identical to the kModals fix (491676472). Happy to assist triage.

### mi...@bountyy.fi (2026-04-12)

Flagging again for triage. Companion bugs 492209810 (kPresentationController), 492198556 (kOrientationLock), and 491676472 (kModals) are all assigned and actively worked. This bug covers the identical missing sandbox enforcement gap for kPointerLock - same root cause, same fix location, same impact class.
If the three companion bugs are being fixed as a batch, kPointerLock should be included in that fix. Leaving it unpatched while the others are fixed would create an incomplete remediation - an attacker could simply use kPointerLock instead of the patched capabilities.
Requesting assignment to the engineer handling the companion bugs.
Mihalis Haatainen, Bountyy Oy

### mi...@bountyy.fi (2026-04-15)

Submitted a patch implementing the proposed fix:
https://chromium-review.googlesource.com/c/chromium/src/+/7761269
The CL adds browser-side IsSandboxed(kPointerLock) enforcement in RenderWidgetHostImpl::RequestMouseLock(), matching the pattern of the kModals fix (Bug 491676472).

### cr...@chromium.org (2026-04-15)

Note for context: alexmos@ posted many of these sandbox flags to audit in <https://issues.chromium.org/issues/40607568#comment12>.

### dx...@google.com (2026-04-17)

Project: chromium/src  

Branch:  main  

Author:  Mihalis Haatainen [mihalis.haatainen@bountyy.fi](mailto:mihalis.haatainen@bountyy.fi)  

Link:    <https://chromium-review.googlesource.com/7761269>

Fix missing browser-side sandbox enforcement for kPointerLock

---


Expand for full commit details
```
     
    RenderWidgetHostImpl::RequestMouseLock() does not check the 
    WebSandboxFlags::kPointerLock sandbox flag. A compromised renderer 
    inside a sandboxed frame (without allow-pointer-lock) can call 
    RequestMouseLock() via Mojo IPC directly, bypassing the renderer-side 
    check in PointerLockController::RequestPointerLock(). 
     
    Add browser-side IsSandboxed(kPointerLock) check matching the pattern 
    of the kModals fix (Bug 491676472, fixed 2025-03-12). 
     
    Bug: 492211919 
    Change-Id: I504cbfc17b6e7e8484a9622939dc98fef2beb755 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7761269 
    Reviewed-by: Dave Tapuska <dtapuska@chromium.org> 
    Commit-Queue: Charlie Reis <creis@chromium.org> 
    Reviewed-by: Charlie Reis <creis@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1616880}

```

---

Files:

- M `AUTHORS`
- M `content/browser/bad_message.h`
- M `content/browser/renderer_host/render_widget_host_delegate.cc`
- M `content/browser/renderer_host/render_widget_host_delegate.h`
- M `content/browser/renderer_host/render_widget_host_impl.cc`
- M `content/browser/security_exploit_browsertest.cc`
- M `content/browser/web_contents/web_contents_impl.cc`
- M `content/browser/web_contents/web_contents_impl.h`
- M `tools/metrics/histograms/metadata/stability/enums.xml`

---

Hash: [80ddc28c7cb4038a6a73b15f452c1239222fd036](https://chromiumdash.appspot.com/commit/80ddc28c7cb4038a6a73b15f452c1239222fd036)  

Date: Fri Apr 17 22:00:53 2026


---

### mi...@bountyy.fi (2026-04-20)

The fix landed per [comment #9](https://issues.chromium.org/issues/492211919#comment9) (CL 7761269). Could this be moved to Assigned/Fixed status and assigned to the appropriate owner? The companion bugs (492209810 kPresentationController, 492198556 kOrientationLock) are in Assigned status with owners tracking their fixes.

### sp...@google.com (2026-05-16)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1500.00 for this report.

Rationale for this decision:
Known issue (web platform bypass via compromised render), + patch


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### mi...@bountyy.fi (2026-05-16)

Amazing , thanks alot for the bounty!

### ch...@google.com (2026-06-04)

WARNING: Removing security\_release value because the issue is not on security\_impact-stable or security\_impact-extended hotlists. Please add to the correct hotlist if the issue is on a release branch.

### ch...@google.com (2026-08-01)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/492211919)*
