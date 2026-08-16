# RenderFrameHostImpl::RunJavaScriptDialog() missing browser-side allow-modals sandbox flag check

| Field | Value |
|-------|-------|
| **Issue ID** | [510968707](https://issues.chromium.org/issues/510968707) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>HTML>Dialog, Blink>SecurityFeature>IFrameSandbox, Internals>Sandbox>SiteIsolation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | os...@gmail.com |
| **Assignee** | av...@chromium.org |
| **Created** | 2026-05-08 |
| **Bounty** | $2,000.00 |

## Description

---

### Report description

ScreenOrientationProvider::LockOrientation() missing browser-side sandbox flag check — compromised renderer bypasses kOrientationLock via Mojo IPC

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://source.chromium.org/chromium/chromium/src/+/main:content/browser/screen_orientation/screen_orientation_provider.cc>

---

### The problem

#### Please describe the technical details of the vulnerability

## Summary

`ScreenOrientationProvider::LockOrientation()` (screen\_orientation\_provider.cc:43) does  

not check `IsSandboxed(kOrientationLock)` on the requesting frame. A compromised renderer
inside a sandboxed iframe (without allow-orientation-lock) can call  

`device::mojom::ScreenOrientation::LockOrientation()` via Mojo IPC directly, bypassing the
renderer-side check in `ScreenOrientation::lock()` (screen\_orientation.cc:117-118).

This is the same class of bug as [crbug.com/492211919](https://crbug.com/492211919) (kPointerLock, commit 80ddc28c7cb40)
and [Bug 491676472](https://issues.chromium.org/issues/491676472) (kModals). Both were fixed by adding browser-side `IsSandboxed()` checks
and terminating the renderer on violation. The kOrientationLock flag was missed.

## Root Cause

`LockOrientation()` checks `IsOrientationLockSupported()`, DevTools emulation, and  

`FullScreenRequired()` but never checks the sandbox flags of the requesting frame.

The requesting frame is available via `receivers_.GetCurrentTargetFrame()`  

(RenderFrameHostReceiverSet tracks which frame bound the receiver), but this is never
consulted.

The renderer-side check exists at screen\_orientation.cc:117-118 —  

`GetExecutionContext()->IsSandboxed(kOrientationLock)`. A compromised renderer skips this
check and calls LockOrientation() on the Mojo pipe directly.

## Platform Scope

The ScreenOrientationDelegate is registered in production on **Android**  

(ScreenOrientationDelegateAndroid, browser\_main\_loop.cc:738) and **ChromeOS**
(ScreenOrientationDelegateChromeos). On desktop, no delegate is set, so  

`IsOrientationLockSupported()` returns false and LockOrientation() returns
ERROR\_NOT\_AVAILABLE before any sandbox check would apply. The PoC uses a
TestScreenOrientationDelegate to exercise the code path on desktop — this is noted for
transparency.

## Comparison with Prior Fixes

- **kPopups** — RFH::CreateNewWindow — FIXED
- **kModals** — RFH::RunJavaScriptDialog — FIXED
- **kPointerLock** — RWH::RequestMouseLock (commit 80ddc28c7cb40) — FIXED
- **kOrientationLock** — SOP::LockOrientation — **MISSING**

## Reproducing

The PoC is a Chromium browser test (attached). It requires direct Mojo IPC calls to  

simulate a compromised renderer — the renderer-side check correctly blocks the JavaScript
API, so a standalone HTML file cannot demonstrate the bypass.

1. Place screen\_orientation\_sandbox\_bypass\_browsertest.cc at  
   
   content/browser/screen\_orientation/
2. Add to content/test/BUILD.gn under content\_browsertests sources:
   "../browser/screen\_orientation/screen\_orientation\_sandbox\_bypass\_browsertest.cc"
3. Build: ninja -C out/asan content\_browsertests
4. Run: out/asan/content\_browsertests --gtest\_filter='ScreenOrientationSandboxBypassTest.O
   rientationLockBypassFromSandboxedFrame' --single-process-tests

Expected output:

- Lock result: 0 (SCREEN\_ORIENTATION\_LOCK\_RESULT\_SUCCESS)
- Delegate locked: 1 (orientation was locked)
- Subframe still alive: 1 (renderer NOT terminated)
- CONFIRMED: Orientation lock succeeded from sandboxed frame without  
  
  allow-orientation-lock

Three tests included:

- **OrientationLockBypassFromSandboxedFrame** — lock succeeds from sandboxed frame (the  
  
  bug)
- **OrientationLockAllowedFromUnsandboxedFrame** — positive control
- **RendererSideCheckBlocksOrientationLock** — renderer-side JS check blocks it (negative
  control)

#### Impact analysis

A compromised renderer process within a sandboxed iframe can lock the screen orientation  

on **Android** and **ChromeOS** devices despite the embedding page explicitly restricting
this via the `sandbox` attribute (omitting `allow-orientation-lock`). This violates the  

sandbox security contract.

The attacker gains the ability to force orientation changes from a context that should not
have this capability, which could be combined with fullscreen to create UI spoofing
scenarios on mobile.

Attack requires a compromised renderer, consistent with the threat model for prior sandbox
enforcement fixes (`kPointerLock` [crbug.com/492211919](https://crbug.com/492211919), `kModals` [Bug 491676472](https://issues.chromium.org/issues/491676472),
`kPopups`).

---

### The cause

#### What version of Chrome have you found the security issue in?

150.0.7831.0 (trunk/dev) — also affects current stable as no fix has been applied to screen\_orientation\_provider.cc

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Sandbox Escape

#### How would you like to be publicly acknowledged for your report?

Arni Hardarson (Neonix Security)

## Attachments

- [bug-report.md](attachments/bug-report.md) (text/markdown, 6.8 KB)
- [suggested-fix.diff](attachments/suggested-fix.diff) (application/octet-stream, 2.2 KB)
- [screen_orientation_sandbox_bypass_browsertest.cc](attachments/screen_orientation_sandbox_bypass_browsertest.cc) (application/octet-stream, 8.8 KB)

## Timeline

### sk...@google.com (2026-05-08)

This report does not present evidence of a security issue
reachable in Chrome. Please refer to the Chrome Security FAQ and VRP FAQ for
more information on the types of issues we accept, and how they should be
presented to us for consideration.

[1] <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md#i-can-demonstrate-memory-corruption-in-a-test-binary>

### ch...@google.com (2026-08-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/510968707)*
