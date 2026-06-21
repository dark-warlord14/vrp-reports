# Sandboxed iframe bypasses allow-popups restriction via CreateNewWindow Mojo IPC — browser has zero sandbox enforcement

| Field | Value |
|-------|-------|
| **Issue ID** | [487471101](https://issues.chromium.org/issues/487471101) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Sandbox>SiteIsolation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | os...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2026-02-25 |
| **Bounty** | $1,000.00 |

## Description

---

### Report description

Sandboxed iframe bypasses allow-popups restriction via CreateNewWindow Mojo IPC — browser has zero sandbox enforcement

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_impl.cc>

---

### The problem

#### Please describe the technical details of the vulnerability

`RenderFrameHostImpl::CreateNewWindow()` in `content/browser/renderer_host/render_frame_host_impl.cc` does not check the `allow-popups` sandbox flag (`WebSandboxFlags::kPopups`) before opening a new window. The sandbox enforcement for popup creation is only performed on the renderer side in `create_window.cc`. A compromised renderer in a sandboxed iframe can call the `CreateNewWindow` Mojo IPC directly with `allow_popup=true`, bypassing all Blink-side sandbox enforcement and opening arbitrary popups.

**Vulnerable files:**

- Browser: [content/browser/renderer\_host/render\_frame\_host\_impl.cc](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_impl.cc)
- Renderer sandbox check (bypassed): [third\_party/blink/renderer/core/page/create\_window.cc](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/page/create_window.cc)
- Renderer sets allow\_popup: [content/renderer/render\_frame\_impl.cc](https://source.chromium.org/chromium/chromium/src/+/main:content/renderer/render_frame_impl.cc)
- Mojom definition: [third\_party/blink/public/mojom/frame/frame.mojom](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/public/mojom/frame/frame.mojom) (`CreateNewWindowParams.allow_popup`)

**Transmission chain:**

1. A sandboxed `<iframe sandbox="allow-scripts allow-same-origin">` (without `allow-popups`) contains a compromised renderer.
2. The renderer patches out the Blink-side `IsSandboxed(kPopups)` check in `create_window.cc:347-358` — the only enforcement point — and sets `params->allow_popup = true` unconditionally in `render_frame_impl.cc:6779-6781`.
3. `RenderFrameHostImpl::CreateNewWindow()` receives the IPC. It computes `effective_transient_activation_state` by OR-ing `params->allow_popup` directly:

```
// render_frame_host_impl.cc:9994-9997
bool effective_transient_activation_state =
    params->allow_popup || HasTransientUserActivation() ||
    (transient_allow_popup_.IsActive() &&
     params->disposition == WindowOpenDisposition::NEW_POPUP);

```

4. Since `params->allow_popup = true`, `effective_transient_activation_state` is `true` regardless of any sandbox restrictions.
5. `CanCreateWindow()` is called with `effective_transient_activation_state=true` — popup is allowed. **No `IsSandboxed()` check anywhere in the browser handler.**
6. The new window opens in full non-sandboxed browser context.

The renderer-side sandbox check in `create_window.cc`:

```
// create_window.cc:347-358
if (opener_window.IsSandboxed(
        network::mojom::blink::WebSandboxFlags::kPopups)) {
  opener_window.AddConsoleMessage(...
      "Blocked opening '...' in a new window because the request was made "
      "in a sandboxed frame whose 'allow-popups' permission is not set.");
  return nullptr;
}

```

...is Blink renderer code only. The browser-side `CreateNewWindow()` handler has **no equivalent check** — `IsSandboxed()` and `WebSandboxFlags::kPopups` do not appear anywhere in the method.

**Steps to reproduce:**

1. Apply `h6_patch_renderer_poc.diff` to `chromium-stable/src/` (Chrome 145.0.7632.117):
   ```
   cd chromium-stable/src
   git apply h6_patch_renderer_poc.diff
   
   ```
2. Build Chrome:
   ```
   autoninja -C out/Default chrome
   
   ```
3. Start the PoC HTTP server:
   ```
   python3 serve.py
   
   ```
4. Launch the patched Chrome:
   ```
   out/Default/Chromium.app/Contents/MacOS/Chromium \
     --user-data-dir=/tmp/chrome-h6-test \
     http://localhost:8080/index.html
   
   ```
5. After 1 second, `pwned.html` opens in a new popup window — despite the iframe having `sandbox="allow-scripts allow-same-origin"` with **no** `allow-popups`.

`h6_patch_renderer_poc.diff` simulates a compromised renderer by (1) removing the `IsSandboxed(kPopups)` check from `create_window.cc` and (2) forcing `params->allow_popup = true` unconditionally in `render_frame_impl.cc`. In practice, a compromised renderer would call the `CreateNewWindow` Mojo IPC directly with `allow_popup=true`, skipping Blink entirely.

**Bisect:**

Introducing commit: `c4cb716e319efaa1c2582565c5f18965dfa39366`

- Author: Mustaq Ahmed ([mustaq@google.com](mailto:mustaq@google.com))
- Date: Tue Jun 05, 2018
- Message: "Browser-side activation state with sync across OOPIFs"
- CL: <https://chromium-review.googlesource.com/967260>
- Cr-Commit-Position: refs/heads/master@{#564530}
- Bugs: 780556, 775930

Evidence:

- Gitiles blame on `render_frame_host_impl.cc` line 9994 (`params->allow_popup || HasTransientUserActivation()`) traces directly to this commit.
- This CL introduced `effective_transient_activation_state` which OR-s the renderer-supplied `mimic_user_gesture` (later renamed `allow_popup`) into the browser's activation decision, with no `IsSandboxed(kPopups)` check.
- The field was later renamed `mimic_user_gesture` → `allow_popup` in commit `8601a5646d6e` (Mustaq Ahmed, 2020-01-31, CL: <https://chromium-review.googlesource.com/c/chromium/src/+/2031187>, refs/heads/master@{#737378}), but the missing browser-side sandbox check persisted.
- The renderer-side `IsSandboxed(kPopups)` check in `create_window.cc` has existed since the early Blink sandbox implementation and was never mirrored browser-side.

Earliest affected: Chrome M68 (stable July 2018, when `c4cb716e` landed). Latest confirmed: Chrome M145 (145.0.7632.117, current Stable). Vulnerable for ~7.5 years.

**Suggested fix:**

I will upload a Gerrit CL with this fix to chromium-review.googlesource.com and add the link in a follow-up comment. `h6_fix.diff` is attached for reference.

Add a browser-side sandbox check in `RenderFrameHostImpl::CreateNewWindow()`, after the fenced frame check and before `effective_transient_activation_state` is computed:

```
+  // Sandboxed frames without allow-popups cannot open new windows.
+  // This enforces the kPopups sandbox flag browser-side; the renderer-side
+  // check in create_window.cc can be bypassed by a compromised renderer
+  // sending allow_popup=true in the Mojo params.
+  if (IsSandboxed(network::mojom::WebSandboxFlags::kPopups)) {
+    bad_message::ReceivedBadMessage(
+        GetProcess(),
+        bad_message::RFH_CREATE_NEW_WINDOW_FROM_SANDBOXED_FRAME);
+    std::move(callback).Run(mojom::CreateNewWindowStatus::kBlocked, nullptr);
+    return;
+  }

```

And in `bad_message.h`, after `RFH_CREATE_NEW_WINDOW_INVALID_DISPOSITION = 334`:

```
+  RFH_CREATE_NEW_WINDOW_FROM_SANDBOXED_FRAME = 335,

```

This mirrors the renderer-side check but enforces it browser-side with `ReceivedBadMessage` to kill the compromised renderer. `IsSandboxed()` uses the browser's own `active_sandbox_flags()` which cannot be forged by a compromised renderer.

Verified: applying both `h6_patch_renderer_poc.diff` and `h6_fix.diff`, the exploit is blocked and the renderer process is terminated. Normal popups from non-sandboxed frames still work correctly.

#### Impact analysis

A compromised renderer inside a sandboxed iframe (e.g., a sandboxed ad frame with `sandbox="allow-scripts allow-same-origin"`) can open arbitrary popup windows, bypassing the `allow-popups` sandbox restriction.

Exploitation requires a compromised renderer (renderer RCE), which is a standard assumption in Chrome's threat model. The attacker gains the ability to:

- **Open arbitrary popups** from content that is explicitly sandboxed to prevent popup creation
- **Bypass the iframe sandbox contract** that embedders rely on to restrict ad/third-party content
- **UI spoofing and phishing** — a sandboxed ad frame could open convincing browser windows mimicking security dialogs or login pages
- **Popup flood attacks** — repeatedly open windows from a sandboxed context that should not have this capability
- **Bypass permission-policy enforcement** — sites use `allow-popups` restriction to prevent untrusted third-party content from opening new browsing contexts

The `allow-popups` sandbox flag exists specifically to prevent untrusted content from opening new windows. The browser's failure to enforce this flag means the sandbox guarantee is illusory against a compromised renderer.

This is the same vulnerability class as H4 (download sandbox bypass via `DownloadURL`) and H1 (user gesture spoofing), both previously accepted. The pattern: renderer-only enforcement of a `WebSandboxFlags` restriction, with the browser unconditionally trusting a renderer-supplied parameter.

---

### The cause

#### What version of Chrome have you found the security issue in?

145.0.7632.117 (Stable, current as of February 25, 2026)

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Site Isolation Bypass

#### How would you like to be publicly acknowledged for your report?

Tianyi Hu

## Attachments

- [h6_fix.diff](attachments/h6_fix.diff) (application/octet-stream, 4.8 KB)
- [index.html](attachments/index.html) (text/html, 1.9 KB)
- [sandboxed.html](attachments/sandboxed.html) (text/html, 678 B)
- [pwned.html](attachments/pwned.html) (text/html, 997 B)
- [h6_patch_renderer_poc.diff](attachments/h6_patch_renderer_poc.diff) (application/octet-stream, 2.3 KB)
- [serve.py](attachments/serve.py) (text/x-python-script, 814 B)

## Timeline

### os...@gmail.com (2026-02-25)

The fix CL for this issue, plus unittest:

<https://chromium-review.googlesource.com/c/chromium/src/+/7605762>

### aj...@google.com (2026-02-26)

Looking at issue 40607568 this sounds like it should be prevented. The supplied patch seems to only affect the renderer.

Sev=Medium as opening popups from a sandboxed iframe is not super-sensitive.

### ch...@google.com (2026-02-26)

Setting milestone because of s2 severity.

### ch...@google.com (2026-02-26)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### al...@chromium.org (2026-02-26)

Thanks for the report. I don't think we've ever actually gone through the full list of iframe sandbox attributes to see what should be hardened by extra validation in the browser process. It seems that [issue 40607568](https://issues.chromium.org/issues/40607568) tracked some of this, and we might have closed it out too early, because while the work on process-isolated sandboxed frames in [issue 40082497](https://issues.chromium.org/issues/40082497) provides strong enforcement for data access, it didn't specifically address attribute validation. I do agree that we should be validating attributes like allow-popups in the browser process, and that this validation is actually meaningful now that a sandboxed frame would be in a separate process from a non-sandboxed frame served from the same origin. I'll put together a fix for allow-popups here and reopen [issue 40607568](https://issues.chromium.org/issues/40607568) to track any remaining attributes.

Note, however, that the provided repro needs a couple of fixes:

1. "allow-same-origin" should actually *not* be in the list of iframe sandbox attributes. This allows the sandboxed frame to share the same origin as its non-sandboxed parent, so the sandboxed frame could just directly script the parent to open the popup, bypassing the allow-popups even without a compromised renderer. allow-same-origin pretty much makes sandboxed frames not meaningful. (Note that it is also used to gate process isolation for a sandboxed frame.)
2. The provided repro doesn't actually open a popup with the default popup blocker behavior due to lack of a user activation, but that is also bypassable.

### os...@gmail.com (2026-02-27)

Thank you for the feedback — noted on both points. I'll make sure future repros demonstrate the realistic attack scenario more carefully.

### dx...@google.com (2026-02-28)

Project: chromium/src  

Branch:  main  

Author:  Alex Moshchuk [alexmos@chromium.org](mailto:alexmos@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7617636>

Add browser-side validation for allow-popups sandboxed frame attribute

---


Expand for full commit details
```
     
    Sandboxed frames created without an allow-popups attribute should not 
    be allowed to create popups. Previously, this attribute was only 
    checked in the renderer. This CL adds additional validation in 
    RenderFrameHostImpl::CreateNewWindow(), the browser process's 
    entrypoint for creating popups via web APIs like window.open(). 
     
    Bug: 487471101 
    Change-Id: I0776f9d6df4200ecf20b29e8ecd18efa2edcd45a 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7617636 
    Reviewed-by: Mark Pearson <mpearson@chromium.org> 
    Auto-Submit: Alex Moshchuk <alexmos@chromium.org> 
    Commit-Queue: Mark Pearson <mpearson@chromium.org> 
    Reviewed-by: Charlie Reis <creis@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1592057}

```

---

Files:

- M `content/browser/bad_message.h`
- M `content/browser/renderer_host/render_frame_host_impl.cc`
- M `content/browser/renderer_host/render_frame_host_impl.h`
- M `content/browser/security_exploit_browsertest.cc`
- M `tools/metrics/histograms/metadata/stability/enums.xml`

---

Hash: [a12e651f6f62614ab4a0c0eed6d686fec8414682](https://chromiumdash.appspot.com/commit/a12e651f6f62614ab4a0c0eed6d686fec8414682)  

Date: Sat Feb 28 19:18:02 2026


---

### ch...@google.com (2026-03-02)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-06-12)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Baseline. Exploit mitigation bypass.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/487471101)*
