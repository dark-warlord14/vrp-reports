# RenderFrameHostImpl::RunJavaScriptDialog() missing browser-side allow-modals sandbox flag check

| Field | Value |
|-------|-------|
| **Issue ID** | [491676472](https://issues.chromium.org/issues/491676472) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>HTML>Dialog, Blink>SecurityFeature>IFrameSandbox, Internals>Sandbox>SiteIsolation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | os...@gmail.com |
| **Assignee** | av...@chromium.org |
| **Created** | 2026-03-11 |
| **Bounty** | $2,000.00 |

## Description

---

### Report description

RenderFrameHostImpl::RunJavaScriptDialog() missing browser-side allow-modals sandbox flag check

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_impl.cc>

---

### The problem

#### Please describe the technical details of the vulnerability

**This is a variant of [issue 487471101](https://issues.chromium.org/issues/487471101) (allow-popups sandbox bypass).** I am filing it separately since it affects a different IPC entrypoint (`RunJavaScriptDialog` vs `CreateNewWindow`) and requires its own fix, but I understand it may be considered part of the same effort tracked in [issue 40607568](https://issues.chromium.org/issues/40607568). I leave it to the security team to decide whether this warrants a separate report or should be folded into the existing tracking bug.

`RunJavaScriptDialog()` does not check `IsSandboxed(kModals)` before showing `alert()`, `confirm()`, or `prompt()` dialogs. A compromised renderer in a sandboxed iframe (without `allow-modals`) can send `RunModalAlertDialog`/`RunModalConfirmDialog`/`RunModalPromptDialog` IPC directly and the browser shows the dialogs.

**Vulnerable file:** [render\_frame\_host\_impl.cc](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_impl.cc) - `RunJavaScriptDialog()`

The renderer-side check in `LocalDOMWindow::alert()/confirm()/prompt()` blocks sandboxed calls, but the browser entrypoint has no corresponding check. Compare with the kPopups fix in `CreateNewWindow()` which checks `IsSandboxed(kPopups)` + `ReceivedBadMessage`.

**Steps to reproduce:**

1. Check out stable tag: `git checkout 146.0.7680.32`
2. `git apply poc_patch.diff` (removes renderer-side kModals checks to simulate compromised renderer)
3. `autoninja -C out/Default chrome`
4. Start HTTP server: `python3 serve.py`
5. Launch patched Chrome:
   - `out/Default/Chromium.app/Contents/MacOS/Chromium --user-data-dir=/tmp/md1 http://127.0.0.1:8080/index.html`
   - Observe: `alert()`, `confirm()`, and `prompt()` dialogs appear from `<iframe sandbox="allow-scripts">` (no `allow-modals`). The iframe has opaque origin (`null`).

**Bisect:**

- Introducing commit: `15bee8d78bc8b` - [mkwst@chromium.org](mailto:mkwst@chromium.org), May 22 2015. Added `allow-modals` sandbox flag with renderer-only enforcement; browser-side `RunJavaScriptDialog()` was never updated.
- Variant gap widened by `a12e651f6f626` (Feb 28, 2026) which added browser-side enforcement for kPopups but not kModals.
- Affected: M44 through M146 (current stable).

**Fix:** Add `IsSandboxed(kModals)` check + `ReceivedBadMessage` in `RunJavaScriptDialog()`, matching the kPopups pattern in `CreateNewWindow()`.

```
if (IsSandboxed(network::mojom::WebSandboxFlags::kModals)) {
  bad_message::ReceivedBadMessage(
      GetProcess(),
      bad_message::RFH_MODAL_DIALOG_FROM_SANDBOXED_FRAME);
  return;
}

```
#### Impact analysis

A compromised renderer in a cross-site sandboxed iframe (separate process via site isolation) can show modal dialogs that block the page, phish via `prompt()`, or manipulate user decisions via `confirm()`. Same class as [bug 487471101](https://issues.chromium.org/issues/487471101) but lower impact since dialogs are less sensitive than popups.

---

### The cause

#### What version of Chrome have you found the security issue in?

146.0.7680.32 (Stable)

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Site Isolation Bypass

#### How would you like to be publicly acknowledged for your report?

Tianyi Hu

## Attachments

- [serve.py](attachments/serve.py) (text/x-python-script, 448 B)
- [poc_patch.diff](attachments/poc_patch.diff) (application/octet-stream, 3.1 KB)
- [index.html](attachments/index.html) (text/html, 3.8 KB)

## Timeline

### os...@gmail.com (2026-03-11)

As mentioned in the report, this is a direct variant of [issue 487471101](https://issues.chromium.org/issues/487471101) with lower security impact. I wasn't sure if I should submit this separately or comment on the existing bug, but I thought it's better to let the security team decide. Perhaps alexmos@ could have a look.

### os...@gmail.com (2026-03-11)

CL: <https://chromium-review.googlesource.com/c/chromium/src/+/7656345>, following the fix for 487471101 pattern.

### dx...@google.com (2026-03-12)

Project: chromium/src  

Branch:  main  

Author:  Tianyi Hu [oscarhuthu@gmail.com](mailto:oscarhuthu@gmail.com)  

Link:    <https://chromium-review.googlesource.com/7656345>

Add browser-side validation for allow-modals sandbox attribute

---


Expand for full commit details
```
     
    RunJavaScriptDialog() does not check IsSandboxed(kModals) before 
    showing alert/confirm/prompt dialogs. Add a browser-side check 
    matching the allow-popups validation in CreateNewWindow(), so that 
    a sandboxed frame without allow-modals cannot show modal dialogs 
    even if the renderer is compromised. 
     
    Bug: 491676472 
    Change-Id: I8c3d3c0d2f167754399a67d6970313c3a6acbe64 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7656345 
    Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
    Reviewed-by: Mark Pearson <mpearson@chromium.org> 
    Reviewed-by: Avi Drissman <avi@chromium.org> 
    Commit-Queue: Alex Moshchuk <alexmos@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1598123}

```

---

Files:

- M `content/browser/bad_message.h`
- M `content/browser/renderer_host/render_frame_host_impl.cc`
- M `content/browser/renderer_host/render_frame_host_impl.h`
- M `content/browser/security_exploit_browsertest.cc`
- M `tools/metrics/histograms/metadata/stability/enums.xml`

---

Hash: [7e257667273927316e93b112d1ec27830fdcdffe](https://chromiumdash.appspot.com/commit/7e257667273927316e93b112d1ec27830fdcdffe)  

Date: Thu Mar 12 01:16:21 2026


---

### ch...@google.com (2026-03-12)

Setting Priority to P3 to match Severity s3. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### cr...@chromium.org (2026-04-15)

avi@: Can this be marked fixed now that <https://chromium-review.googlesource.com/7656345> has landed?

### sp...@google.com (2026-05-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
web platform privilege escalation via compromised renderer, low impact with bisect


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/491676472)*
