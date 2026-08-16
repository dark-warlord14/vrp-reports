# VerifyInitiatorOrigin() skips HostsOrigin() process lock check for opaque origins in error documents and MHTML subframes

| Field | Value |
|-------|-------|
| **Issue ID** | [487300831](https://issues.chromium.org/issues/487300831) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | os...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2026-02-24 |
| **Bounty** | $2,000.00 |

## Description

---

### Report description

VerifyInitiatorOrigin() skips HostsOrigin() process lock check for opaque origins in error documents and MHTML subframes

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/ipc_utils.cc>

---

### The problem

#### Please describe the technical details of the vulnerability

# The problem

`VerifyInitiatorOrigin()` completely skips the `HostsOrigin()` process lock check when the `initiator_origin` is opaque and the current frame is an error document or MHTML subframe. A compromised renderer in these contexts can forge any opaque initiator origin with an arbitrary precursor, and the browser accepts it without verification — a site isolation boundary violation.

**Vulnerable files:**

- Browser: [content/browser/renderer\_host/ipc\_utils.cc](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/ipc_utils.cc)
- Mojo definition: [third\_party/blink/public/mojom/frame/remote\_frame.mojom](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/public/mojom/frame/remote_frame.mojom) (`OpenURLParams.initiator_origin`)
- Renderer: [content/renderer/render\_frame\_impl.cc](https://source.chromium.org/chromium/chromium/src/+/main:content/renderer/render_frame_impl.cc) (`RenderFrameImpl::OpenURL()`)

**Transmission chain:**

1. In `RenderFrameImpl::OpenURL()`, the renderer sets `params->initiator_origin` from `info->url_request.RequestorOrigin()` — attacker-controlled in a compromised renderer.
2. The field is a `url.mojom.Origin` in the `OpenURLParams` Mojo struct, sent via `mojom::FrameHost::OpenURL()`.
3. In `VerifyOpenURLParams()`, the browser calls `VerifyInitiatorOrigin()` which checks whether the renderer process hosts the claimed origin.
4. However, when the origin is opaque AND the frame is an error document, the function returns `true` immediately without calling `HostsOrigin()`:

```
if (initiator_origin.opaque()) {
    if (current_rfh && current_rfh->IsErrorDocument()) {
        return true;  // SKIP ALL VERIFICATION
    }
    if (current_rfh && current_rfh->IsMhtmlSubframe()) {
        return true;  // SKIP ALL VERIFICATION
    }
}

```

Two TODO comments in the code explicitly acknowledge this gap:

> `TODO(crbug.com/40109437): Ideally, origin verification should be performed even if initiator_origin is opaque, to ensure that the precursor origin matches the process lock.`

**Steps to reproduce:**

1. Check out the current stable tag (145.0.7632.110)
2. `git apply h5_patch_renderer_poc.diff`
3. Build: `autoninja -C out/Default chrome`
4. Place PoC files in the same directory, start HTTP server:
   - `python3 serve.py`
5. Launch patched Chrome and observe:
   - `out/Default/Chromium.app/Contents/MacOS/Chromium --user-data-dir=/tmp/chrome-h5-test --enable-logging=stderr http://localhost:8080/index.html`
   - The page embeds an iframe to a dead port (localhost:9999). After the error page loads, the patched renderer sends `OpenURL` with a forged opaque origin (precursor=`http://cross-site-forged.example`). The iframe navigates to `victim.html` — proving the forged initiator origin was accepted by the browser.

The renderer patch hooks `DidFinishLoad()` to detect error page subframes, then after 3 seconds calls `GetFrameHost()->OpenURL()` with a forged opaque `initiator_origin` whose precursor (`http://cross-site-forged.example`) does not match the error page's process lock (`chrome-error://chromewebdata/`). No special flags are needed.

**Bisect:**
Introducing commit: `4043b7370f9b845cd06f07296e115c7094662c66`

- Author: Alex Moshchuk ([alexmos@chromium.org](mailto:alexmos@chromium.org)), June 14, 2024
- Message: "Remove opaque origin exception from VerifyInitiatorOrigin()"
- CL: <https://chromium-review.googlesource.com/c/chromium/src/+/5590305>
- Cr-Commit-Position: refs/heads/main@{#1315048}
- Bug: [crbug.com/40109437](https://crbug.com/40109437)

Evidence:

- M127 (127.0.6533.72): blanket `return true` for ALL opaque origins (no `IsErrorDocument`/`IsMhtmlSubframe` check)
- M128 (128.0.6613.84): first milestone with the targeted `IsErrorDocument()`/`IsMhtmlSubframe()` bypass pattern
- Parent commit (`5c67fc2a6cca`): blanket bypass, no `current_rfh` parameter
- Commit `4043b737`: introduced `current_rfh` parameter and the error doc/MHTML bypass paths

The commit was a security hardening that narrowed a blanket opaque origin bypass to only error documents and MHTML subframes. However, these two remaining `return true` paths still skip `HostsOrigin()` entirely, and the TODOs acknowledge the gap remains unfixed.

Earliest affected release: Chrome M128 (stable August 2024). Latest confirmed: Chrome M145 (145.0.7632.110, current stable).

**Suggested fix (attached as `h5_fix.diff`):**
Instead of blanket `return true` for opaque origins in error pages and MHTML subframes, validate that the precursor of the provided opaque origin matches the precursor of the frame's committed origin:

```
// Before (vulnerable):
if (current_rfh && current_rfh->IsErrorDocument()) {
    return true;
}

// After (fixed):
if (current_rfh && current_rfh->IsErrorDocument()) {
    const auto& committed = current_rfh->GetLastCommittedOrigin();
    if (committed.opaque() &&
        committed.GetTupleOrPrecursorTupleIfOpaque() ==
            initiator_origin.GetTupleOrPrecursorTupleIfOpaque()) {
        return true;
    }
    bad_message::ReceivedBadMessage(
        process_id, bad_message::INVALID_INITIATOR_ORIGIN);
    return false;
}

```

This allows legitimate error page reloads (where the precursor naturally matches) while blocking forged cross-site precursors. Verified: with the fix applied, the renderer is killed with `bad_message::INVALID_INITIATOR_ORIGIN` (reason 213) instead of the navigation succeeding.

A browser test (`h5_browsertest.diff`) is also attached. It adds `SecurityExploitBrowserTest.InvalidOpaqueInitiatorFromErrorPage` to `content/browser/security_exploit_browsertest.cc`, following the same pattern as existing `INVALID_INITIATOR_ORIGIN` tests. The test creates an error page subframe via `URLLoaderInterceptor`, then directly injects a forged `OpenURL` with a mismatched opaque precursor and verifies the renderer is killed. Plan to upload both fix and test as a Gerrit CL.

#### Impact analysis

A compromised renderer in an error page or MHTML subframe context can forge navigation initiator origins with arbitrary cross-site precursors. This violates site isolation boundaries — the browser accepts navigations attributed to origins that the renderer process does not host.

Error pages are easy to trigger: any iframe pointed at a non-responsive server produces one. A compromised renderer in this context could forge initiator origins to manipulate navigation attribution, potentially affecting security decisions downstream that rely on the initiator origin (e.g., CSP, CORS preflight, permission delegation).

---

### The cause

#### What version of Chrome have you found the security issue in?

145.0.7632.110 (Stable)

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Site Isolation Bypass

#### How would you like to be publicly acknowledged for your report?

Tianyi Hu

## Attachments

- [h5_fix.diff](attachments/h5_fix.diff) (application/octet-stream, 3.3 KB)
- [h5_browsertest.diff](attachments/h5_browsertest.diff) (application/octet-stream, 3.5 KB)
- [serve.py](attachments/serve.py) (text/x-python-script, 269 B)
- [index.html](attachments/index.html) (text/html, 774 B)
- [h5_patch_renderer_poc.diff](attachments/h5_patch_renderer_poc.diff) (application/octet-stream, 4.0 KB)
- [victim.html](attachments/victim.html) (text/html, 126 B)

## Timeline

### os...@gmail.com (2026-02-24)

The CL link for both fix and a corresponding browser test:
<https://chromium-review.googlesource.com/c/chromium/src/+/7603574>

### aj...@google.com (2026-02-24)

-> Some csa folks - I've not reproduced this but the patch is renderer only and there is a CL from the reporter which will need review from you.

### ch...@google.com (2026-02-25)

Setting milestone because of s2 severity.

### ch...@google.com (2026-02-25)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### al...@chromium.org (2026-03-07)

Thanks for the report, but this basically restates an [open TODO](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/ipc_utils.cc;l=56-83;drc=b496550e39c5c1752d504a684ebc4d88b4009ed3) from our code. Originally, all opaque origins were exempted from CPSP security checks, and we've been gradually locking down those cases to go through stricter checks based on precursors of those origins. <https://chromium-review.googlesource.com/c/chromium/src/+/5590305> did that for most cases involving initiator origin verification, except for the error page and MHTML case. This is known and covered by [issue 40109437](https://issues.chromium.org/issues/40109437).

Some analysis:

- MHTML is already pretty locked down (running in locked file: sandboxed processes, unable to run scripts or make requests, etc), so I think a spoofed initiator origin in this case is very low priority.
- Main frame error pages are isolated in their own process (chrome-error://chromewebdata), with no attacker-controlled content, so no need to worry about that case either.
- That leaves subframe error pages, because unfortunately we don't have subframe error page isolation (tracked <https://crbug.com/40134629>).
- The attacker can indeed navigate an existing subframe in its process to an error page at foo.com, which will have an opaque origin with foo.com as its precursor. Then the attacker could navigate that frame to bar.com, while providing an arbitrary initiator origin victim.com, and it won't get verified.
- I struggle to understand if the attacker can actually do something meaningful by spoofing the initiator origin for a navigation out of an opaque-origin, error-page document. Seems like we still wouldn't allow the attacker to commit any third-party origin in its process (other site isolation checks should catch that), and content on opaque origins is already restricted (e.g., can't use cookies or storage). The only thing I can think of is that the spoofed initiator origin might be used to send incorrect Sec-Fetch-Site headers for a victim's site, for a navigation on that error subframe. Maybe this warrants revisiting the priority/severity of this?

I do agree we should try to lock down the error page case a bit more to avoid this. However, I don't think the proposed fix is sufficient: it assumes current\_rfh is the initiator frame, which isn't generally true, and it also doesn't prevent an attacker from first navigating the subframe to victim.com/404 (i.e., the precursor of the error page's origin can be attacker-controlled), and then navigating that frame to victim.com/target, which still results in an initiator origin with victim.com as the precursor, without requiring a spoofed initiator origin in OpenURLParams.

I think the best ways to fix this are subframe error page isolation (<https://crbug.com/40134629>) or revisiting how precursors are set for error pages - which might be both difficult to do. I'll try to think of shorter-term options as well.

Reporter: it might be helpful if you can provide repro steps to prove that there are meaningful security consequences the attacker can achieve with this. I'm not sure I see how it would affect the things mentioned in the report (CSP, CORS preflight, permission delegation).

### al...@chromium.org (2026-03-07)

Perhaps one shorter-term option might be to sanitize the initiator origin in the error page navigation case using the process lock and/or a saved initiator origin that was used when the error document originally loaded. We could store the latter on RFH, or maybe it's already available via last\_committed\_frame\_entry\_->initiator\_origin().

### al...@chromium.org (2026-03-07)

I'm experimenting with #7 in <https://chromium-review.git.corp.google.com/c/chromium/src/+/7644301>. I suppose we could also try to force all subframe error pages to commit in opaque origins without a precursor, though I'm not sure if that's going to break anything.

### os...@gmail.com (2026-03-07)

Thanks for the very thorough analysis! Really appreciate you taking the time to walk through the error page cases and the fix limitations in detail. You're right on all points: my fix is insufficient, and the downstream impact I claimed was overstated. The verification bypass is a real code bug, but I can't demonstrate practical security consequences from it. Apologies for the noise.

Happy to defer to your CL. Let me know if I can help with testing.

### al...@chromium.org (2026-03-12)

I think this should be low severity based on the analysis and comments above.

### dx...@google.com (2026-05-02)

Project: chromium/src  

Branch:  main  

Author:  Alex Moshchuk [alexmos@chromium.org](mailto:alexmos@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7794327>

Don't use precursors for error page origins for kCurrentProcess.

---


Expand for full commit details
```
     
    Currently, when a subframe navigation fails due to deterministic 
    failures (e.g., CSP or BLOCKED_BY_CLIENT), the resulting error page is 
    committed in the current process (`ErrorPageProcess::kCurrentProcess`) 
    to avoid spawning a new process for a potentially privileged 
    destination. 
     
    Previously, this error page was given an opaque origin derived from 
    the destination URL. If a compromised renderer intentionally triggered 
    a CSP failure against a cross-site victim URL, it could force an error 
    page with the victim's precursor to commit within the attacker's 
    process. This is risky, and among other problems, it allowed the 
    compromised renderer to inject a sandboxed srcdoc iframe into the 
    error page, which would inherit the victim precursor and could be 
    incorrectly granted a dedicated SiteInstance/process belonging to the 
    victim. 
     
    This CL fixes this by forcing error pages that stay in the current 
    process to use opaque unique origins with no precursor. Note that 
    this only affects subframe error pages, since main frame error pages 
    have error page isolation which avoids these problems. 
     
    Change-Id: Ib43c88233b36cd0ba84dff993134e2fcaa52ba13 
    Bug: 502348223, 487300831 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7794327 
    Commit-Queue: Alex Moshchuk <alexmos@chromium.org> 
    Reviewed-by: Charlie Reis <creis@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1624238}

```

---

Files:

- M `content/browser/renderer_host/navigation_request.cc`
- M `content/browser/renderer_host/render_frame_host_manager_browsertest.cc`
- M `content/browser/security_exploit_browsertest.cc`

---

Hash: [470a5614ecfbdd85e5b0bb97719ffafa85410872](https://chromiumdash.appspot.com/commit/470a5614ecfbdd85e5b0bb97719ffafa85410872)  

Date: Sat May 2 03:31:33 2026


---

### al...@chromium.org (2026-05-04)

Update: this also came up in [issue 502348223](https://issues.chromium.org/issues/502348223), which also demonstrated a more impactful way for a compromised renderer to take advantage of subframe error page precursors. I landed a fix in <https://crrev.com/c/7794327> which stops using precursors for error pages in these problematic cases, namely error pages that stay in the current process. This still leaves the MHTML part of this, but I think that can be tracked by [issue 40109437](https://issues.chromium.org/issues/40109437), so I'll go ahead and close this.

### sp...@google.com (2026-05-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline with bisect. Exploitation Mitigation Bypass


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

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/487300831)*
