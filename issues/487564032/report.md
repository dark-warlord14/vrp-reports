# Refactor _unfencedTop MPArch code path

| Field | Value |
|-------|-------|
| **Issue ID** | [487564032](https://issues.chromium.org/issues/487564032) |
| **Status** | Accepted |
| **Severity** | S1-High |
| **Priority** | P4 |
| **Component** | Blink>FencedFrames, UI>Browser>Navigation |
| **Reporter** | gt...@chromium.org |
| **Assignee** | sh...@chromium.org |
| **Created** | 2026-02-25 |
| **Bounty** | $3,000.00 |

## Description

---

### Report description

Fenced frame `_unfencedTop` navigation leaks `initiator_origin` to destination via `Sec-Fetch-Site`

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_impl.cc>

---

### The problem

#### Please describe the technical details of the vulnerability

`RenderFrameHostImpl::OpenURL()` contains a commented-out TODO ([crbug.com/40221940](https://crbug.com/40221940)) that was supposed to replace the renderer-supplied `initiator_origin` with an opaque origin before forwarding a `_unfencedTop` navigation to `NavigateFromFrameProxy()`. The fix was never completed: `// url::Origin initiator_origin;` remains commented out, and `params->initiator_origin` — fully controlled by the renderer — is passed directly to `NavigateFromFrameProxy()`.

A compromised fenced frame renderer can set `initiator_origin` to any origin its process hosts, causing the browser to forward the fenced frame's real identity to the destination server via `Sec-Fetch-Site`, violating the Privacy Sandbox isolation requirement.

**Vulnerable files:**

- Renderer: [content/renderer/render\_frame\_impl.cc](https://source.chromium.org/chromium/chromium/src/+/main:content/renderer/render_frame_impl.cc)
- Mojo definition: [third\_party/blink/public/mojom/frame/remote\_frame.mojom](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/public/mojom/frame/remote_frame.mojom)
- Browser: [content/browser/renderer\_host/render\_frame\_host\_impl.cc](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_impl.cc)

**Vulnerable code:**

```
// In RenderFrameHostImpl::OpenURL(), inside the is_unfenced_top_navigation block:

// TODO(crbug.com/40221940): Null out the initiator origin, frame token, and
// site instance.
// We use an opaque `initiator_origin` in order to avoid leaking
// information from the fenced frame to its embedder. (The navigation will
// be treated as cross-origin unconditionally.) We don't need to provide a
// `source_site_instance`.
// url::Origin initiator_origin;    // <── FIX IS COMMENTED OUT

// ...

target_frame->frame_tree_node()->navigator().NavigateFromFrameProxy(
    ..., params->initiator_origin,  // <── RENDERER VALUE FORWARDED UNCHANGED
    ..., /*is_unfenced_top_navigation=*/true, ...);

```

**Transmission chain:**

1. Fenced frame renderer calls `RenderFrameImpl::OpenURL()` with `is_unfenced_top_navigation=true`.
2. Renderer sets `params->initiator_origin = info->url_request.RequestorOrigin()` — the real fenced frame origin. A compromised renderer can set this to any origin its process hosts.
3. `params` is sent to the browser via the `LocalFrameHost::OpenURL` Mojo IPC (`OpenURLParams` struct in `remote_frame.mojom`).
4. In `RenderFrameHostImpl::OpenURL()`, the browser validates the origin with `VerifyInitiatorOrigin()` (passes, since the process does host the origin), then enters the `_unfencedTop` code path.
5. The TODO fix (`url::Origin initiator_origin;`) is commented out and has no effect.
6. `params->initiator_origin` (the real fenced frame origin) is passed directly to `NavigateFromFrameProxy()`, which stores it in `FrameNavigationEntry` and forwards it in `CommonNavigationParams`.
7. The network service sets `Sec-Fetch-Site` on the outgoing request using the stored initiator origin. If the fenced frame and destination share the same origin, Chrome sets `Sec-Fetch-Site: same-origin` instead of the required `cross-site`.

**Steps to reproduce:**

1. `git apply m2_poc_patch.diff` in the stable checkout
2. `autoninja -C out/Default chrome -j8`
3. Place `index.html`, `fenced.html`, and `serve.py` in the same directory, then start the HTTP server:
   - `python3 serve.py`
4. Launch patched Chrome and observe:
   - `out/Default/Chromium.app/Contents/MacOS/Chromium --enable-blink-features=FencedFramesDefaultMode --user-data-dir=/tmp/chrome-m2-test http://localhost:8080/index.html`
   - After ~2 seconds, server stdout shows: `[*] /destination Sec-Fetch-Site: same-origin`
   - The fenced frame's origin has leaked. Privacy Sandbox isolation is violated.

`m2_poc_patch.diff` simulates a compromised renderer by forging `user_gesture=true` for `_unfencedTop` navigations, bypassing `ValidateUnfencedTopNavigation()` so the navigation proceeds without user interaction. The renderer's real `initiator_origin` (the fenced frame's origin) flows through unchanged — the bug is that the browser forwards it to `NavigateFromFrameProxy()` instead of replacing it with an opaque origin. `FencedFramesDefaultMode` enables the `FencedFrameConfig` URL constructor for testing; in production, fenced frames are created via Protected Audience or Shared Storage APIs.

**Bisect:**

Introducing commit: `a42fdef8ad1898f97e34eaf8b74f0d3a82361d29`

- Author: Garrett Tanzer ([gtanzer@chromium.org](mailto:gtanzer@chromium.org))
- Date: Mon Jun 13, 2022
- Message: "Fenced Frames: \_unfencedTop MPArch partial refactor"
- CL: <https://chromium-review.googlesource.com/c/chromium/src/+/3615129>
- Cr-Commit-Position: refs/heads/main@{#1013498}

Evidence:

- M104 (104.0.5112.0): `"Null out the initiator origin"` pattern is **absent** (grep count = 0)
- M105 (105.0.5195.0): pattern is **present** (grep count = 1)
- Parent commit (`a42fdef^`): pattern absent — the diff shows these lines being added
- Commit `a42fdef`: pattern present — introduces the TODO + commented-out `url::Origin initiator_origin;`

Earliest affected: Chrome M105 (stable August 30, 2022). Latest confirmed: Chrome M145 (145.0.7632.117, current Stable). Vulnerable for ~3.5 years.

**Suggested fix:**

`m2_fix.diff` is attached. Uncomment and activate the opaque origin, then use it instead of `params->initiator_origin` in the `NavigateFromFrameProxy()` call:

```
-    // TODO(crbug.com/40221940): Null out the initiator origin, ...
-    // url::Origin initiator_origin;
+    url::Origin initiator_origin;

-        GetProcess()->GetDeprecatedID(), params->initiator_origin,
+        GetProcess()->GetDeprecatedID(), initiator_origin,

```

A default-constructed `url::Origin` is opaque, so the destination server will see `Sec-Fetch-Site: cross-site` — matching the Privacy Sandbox requirement. Normal (non-fenced-frame) navigations are unaffected because they do not enter the `is_unfenced_top_navigation` code path.

I will upload a Gerrit CL and add the link in a follow-up comment.

#### Impact analysis

A compromised renderer inside a fenced frame (e.g., via renderer RCE in a third-party ad delivered via Protected Audience/FLEDGE) can set `initiator_origin` to its real origin. The browser forwards this to the destination server via `Sec-Fetch-Site`, revealing the fenced frame's content identity.

The Privacy Sandbox guarantee for fenced frames is that the embedding page and the fenced frame cannot identify each other. Leaking the fenced frame's origin to the destination of a `_unfencedTop` navigation breaks this by:

- Allowing the destination server to identify what ad/content was displayed in the fenced frame
- Enabling cross-context correlation that the Privacy Sandbox is specifically designed to prevent
- Leaking via standard HTTP headers (`Sec-Fetch-Site`, `Referer` if applicable) that are routinely logged

The Chromium code itself acknowledges this is a bug (`crbug.com/40221940` appears three times in the same function) and documents the intended fix — it was simply never activated.

Exploitation requires a compromised renderer (renderer RCE), which is a standard assumption in Chrome's security model.

---

### The cause

#### What version of Chrome have you found the security issue in?

145.0.7632.117 (Stable, current as of February 2026)

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Site Isolation Bypass

#### How would you like to be publicly acknowledged for your report?

Tianyi Hu

## Attachments

- [m2_fix.diff](attachments/m2_fix.diff) (application/octet-stream, 4.8 KB)
- [m2_poc_patch.diff](attachments/m2_poc_patch.diff) (application/octet-stream, 1.2 KB)
- [fenced.html](attachments/fenced.html) (text/html, 297 B)
- [serve.py](attachments/serve.py) (text/x-python-script, 1018 B)
- [index.html](attachments/index.html) (text/html, 710 B)

## Timeline

### os...@gmail.com (2026-02-25)

Fix CL with browser test: <https://chromium-review.googlesource.com/c/chromium/src/+/7607320>

### li...@chromium.org (2026-02-25)

Would this not be a duplicate of [crbug.com/40221940](https://crbug.com/40221940)? Marking as such, but correct me if I'm wrong.

### os...@gmail.com (2026-02-25)

Thanks for the reference. I'd note a few differences:

1. [Bug 40221940](https://issues.chromium.org/issues/40221940) is a refactoring task, not a security report. The initiator origin nulling is listed as a TODO in [comment #6](https://issues.chromium.org/issues/487564032#comment6) (June 2022) but remains unimplemented after nearly 4 years.
2. The security impact is concrete: a fenced frame's origin — intended to be opaque — is disclosed to the navigation destination via the `Sec-Fetch-Site` header on `_unfencedTop` navigations. This breaks the fenced frame privacy boundary.
3. [Comment #9](https://issues.chromium.org/issues/487564032#comment9) (Aug 2024) lists the remaining work items for that bug and does not include the initiator origin nulling, suggesting it may have been deprioritized.

I think this should be tracked separately as a security issue.

### li...@chromium.org (2026-02-25)

Sounds good. @gt...@chromium.org do you mind taking a look at this?

### ch...@google.com (2026-02-26)

Setting milestone because of s2 severity.

### os...@gmail.com (2026-03-12)

Hi, any update on this?

I've rebased the fix CL ([crrev.com/c/7607320](https://crrev.com/c/7607320)) onto main — it applies cleanly and the test passes (locally). Happy to address any review feedback.

### ch...@google.com (2026-03-12)

gtanzer: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sh...@chromium.org (2026-04-03)

A few thoughts here:

- The only ways of creating FFs (Protected Audience and Shared Storage) are deprecated.
- This is more of a privacy issue than a security issue, given that the main goal of Fenced Frames is to prevent joining user data across contexts and this is a case of compromised renderer leading to a privacy bypass.

reducing priority and severity based on the above.

### os...@gmail.com (2026-04-03)

Thanks for the context on deprecation. fair point on reduced practical impact.

However I do have two notes on the severity change:

1. S4 seems too low. `compromised-renderers.md` lists cross-site frame identity isolation as a browser enforced security boundary. The browser is supposed to replace `initiator_origin` with an opaque origin before `NavigateFromFrameProxy()` — the code acknowledges this with the commented-out TODO. While deprecation reduces the attack surface, this is still a boundary violation as long as the APIs ship. S3 would be more appropriate.
2. Privacy vs. security framing: The fenced frame's identity leaks via `Sec-Fetch-Site`, a browser enforced security header. A compromised renderer bypasses a browser side control, this is the standard Chrome security threat model, not a privacy only concern.

After all, the fix is a one line uncomment. Happy to address any review feedback:

<https://chromium-review.googlesource.com/c/chromium/src/+/7607320>

### ch...@google.com (2026-04-04)

Setting Priority to P3 to match Severity s3. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-04-09)

Project: chromium/src  

Branch:  main  

Author:  Tianyi Hu [oscarhuthu@gmail.com](mailto:oscarhuthu@gmail.com)  

Link:    <https://chromium-review.googlesource.com/7607320>

Use opaque initiator\_origin for \_unfencedTop navigations

---


Expand for full commit details
```
     
    RenderFrameHostImpl::OpenURL() forwards the renderer-supplied 
    params->initiator_origin to NavigateFromFrameProxy() for 
    _unfencedTop navigations from fenced frames. The code contains 
    a commented-out declaration (url::Origin initiator_origin;) that 
    was intended to replace the renderer value with an opaque origin, 
    but was never activated. 
     
    Uncomment the opaque origin declaration and pass it to 
    NavigateFromFrameProxy() instead of params->initiator_origin. 
    A default-constructed url::Origin is opaque, so the destination 
    will see Sec-Fetch-Site: cross-site — matching the fenced frame 
    privacy model requirement. Non-fenced-frame navigations are 
    unaffected because they do not enter the is_unfenced_top_navigation 
    code path. 
     
    Bug: 487564032, 40221940 
    Change-Id: I7d5767f345e90e6dadf8d9c2f39c71d15cff6103 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7607320 
    Commit-Queue: Xiaochen Zhou <xiaochenzh@chromium.org> 
    Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
    Reviewed-by: Xiaochen Zhou <xiaochenzh@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1612246}

```

---

Files:

- M `content/browser/renderer_host/render_frame_host_impl.cc`
- M `content/browser/security_exploit_browsertest.cc`

---

Hash: [f7d4aed5f74244c2f81129f4b1a1e9d953c8b269](https://chromiumdash.appspot.com/commit/f7d4aed5f74244c2f81129f4b1a1e9d953c8b269)  

Date: Thu Apr 9 15:15:44 2026


---

### os...@gmail.com (2026-04-23)

Hi team, the fix landed in <https://chromium-review.googlesource.com/c/chromium/src/+/7607320>. Added to Security-Fixed-Issue-Request hotlist per the rule update.

### aj...@google.com (2026-04-29)

Note for VRP - patch uploaded by reporter.

### sp...@google.com (2026-05-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Baseline with patch bonus. User information disclosure


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2026-08-14)

This Blink bug has been marked as either a release blocker or a vulnerability bug. Blink bugs affect all OSs supported by Chrome (except iOS), so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

## Bounty Award

> Baseline with patch bonus. User information disclosure

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/487564032)*
