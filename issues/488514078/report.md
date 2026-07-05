# EnterFullscreen() bypasses fullscreen Permissions Policy via missing browser-side check

| Field | Value |
|-------|-------|
| **Issue ID** | [488514078](https://issues.chromium.org/issues/488514078) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Sandbox>SiteIsolation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | os...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2026-02-28 |
| **Bounty** | $2,000.00 |

## Description

---

### Report description

EnterFullscreen() bypasses fullscreen Permissions Policy via missing browser-side check

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_impl.cc>

---

### The problem

#### Please describe the technical details of the vulnerability

`RenderFrameHostImpl::EnterFullscreen()` does not check the `fullscreen` Permissions Policy browser-side. A compromised renderer in a cross-site OOPIF can bypass the renderer-side check in `AllowedToUseFullscreen()` and send `EnterFullscreen()` via Mojo — the browser grants it even when the iframe has no `allowfullscreen` attribute.

**Vulnerable file:** [render\_frame\_host\_impl.cc](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_impl.cc) — `EnterFullscreen()`

The code has a TODO acknowledging this: `TODO(alexmos): When the allowFullscreen flag is known in the browser process, use it to double-check that fullscreen can be entered here.` Other Permissions-Policy-gated features (`CreatePaymentManager`, `GetUsbDeviceService`, `GetSerialService`) already check `IsFeatureEnabled()` + `ReportBadMessage` in the same file.

**Steps to reproduce:**

1. Check out stable tag: `git checkout 146.0.7680.32`
2. `git apply poc_patch.diff` (bypasses renderer-side `AllowedToUseFullscreen()` with `return true`)
3. Build with: `is_debug=false is_component_build=true symbol_level=1 blink_symbol_level=0 dcheck_always_on=true`
4. `autoninja -C out/Default chrome`
5. Start the PoC server (no root required):
   - `python3 serve.py`
   - Parent: `http://localhost:8080` — embeds `<iframe src="http://127.0.0.1:8081/attacker.html">` without `allowfullscreen`
   - `localhost` vs `127.0.0.1` = different eTLD+1 = cross-site OOPIF
6. Launch patched Chromium:
   - `out/Default/Chromium.app/Contents/MacOS/Chromium --user-data-dir=/tmp/chrome-poc-test http://localhost:8080/`
7. Click "Go Fullscreen" in the iframe. The iframe enters fullscreen and renders a fake browser chrome with spoofed URL bar (`https://secure.mybank.example.com/login`) and login form.

No special flags required. The Mojo interface `blink.mojom.LocalFrameHost::EnterFullscreen` is always bound.

**Bisect:**
Introducing commit: `1f7eac4a2affa` — [alexmos@chromium.org](mailto:alexmos@chromium.org), 2016-05-25, "Reland: Add support for entering/exiting HTML fullscreen from OOPIFs."
CL: <https://codereview.chromium.org/2008873004>
Cr-Commit-Position: refs/heads/master@{#396027}
Evidence: M52 (branch-heads/2743) absent, M53 (branch-heads/2785) present.
Affected: M53 (~September 2016) through M146 (current stable).

**Fix:** Add `IsFeatureEnabled(kFullscreen)` check + `ReceivedBadMessage` to `EnterFullscreen()`, matching the pattern used by `CreatePaymentManager()`. Attached as `fix.diff` (includes unit test).

#### Impact analysis

A compromised renderer in a cross-site OOPIF (separate process) can enter fullscreen without the `allowfullscreen` attribute. This enables fullscreen UI spoofing — the PoC demonstrates a fake browser chrome with spoofed URL bar and phishing login form. Chromium shows a transient "Press Esc to exit full screen" notification, partially mitigating the attack but not eliminating it (the notification disappears after a few seconds). This is a Permissions Policy enforcement gap, comparable to other `IsFeatureEnabled` checks already present in the same file.

---

### The cause

#### What version of Chrome have you found the security issue in?

146.0.7680.32 (Stable)

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Permissions Bypass

#### How would you like to be publicly acknowledged for your report?

Tianyi Hu

## Attachments

- [fix.diff](attachments/fix.diff) (application/octet-stream, 7.2 KB)
- [attacker.html](attachments/attacker.html) (text/html, 4.3 KB)
- [serve.py](attachments/serve.py) (text/x-python-script, 2.6 KB)
- [poc_patch.diff](attachments/poc_patch.diff) (application/octet-stream, 1.1 KB)
- [index.html](attachments/index.html) (text/html, 3.2 KB)

## Timeline

### os...@gmail.com (2026-02-28)

CL with test:

<https://chromium-review.googlesource.com/c/chromium/src/+/7616589>

### mp...@google.com (2026-03-04)

This is quite low severity since it requires a compromised renderer, but also may be something easy to fix. We also are not accepting new fullscreen bugs at the moment (<https://chromium.googlesource.com/chromium/src/+/main/docs/security/fullscreen.md>) but I'm choosing to triage this because it's outside of the normal UI bug/logic bug obscures Fullscreen toast notification and circumvents a web platform permission, and again can possibly be fixed easily.

### ch...@google.com (2026-03-04)

Setting Priority to P3 to match Severity s3. To ensure SLOs are tracked correctly, priority must exceed severity.

### os...@gmail.com (2026-03-12)

Updated the CL, the new patchset fixed conflict with main and also added a browser test. Can you please help assign a reviewer for this CL?

<https://chromium-review.googlesource.com/c/chromium/src/+/7616589>

### al...@chromium.org (2026-03-20)

[Site isolation triage] I've reviewed the fix in <https://crrev.com/c/7616589>, and it looks good. This is all similar to the missing enforcements in a few other recent bugs ([issue 487471101](https://issues.chromium.org/issues/487471101), [issue 486761170](https://issues.chromium.org/issues/486761170)). I think we can just go ahead and land the proposed fix; I'm happy to take ownership of this bug to make sure the fix lands.

### dx...@google.com (2026-03-24)

Project: chromium/src  

Branch:  main  

Author:  Tianyi Hu [oscarhuthu@gmail.com](mailto:oscarhuthu@gmail.com)  

Link:    <https://chromium-review.googlesource.com/7616589>

Enforce fullscreen Permissions Policy in EnterFullscreen

---


Expand for full commit details
```
     
    RenderFrameHostImpl::EnterFullscreen() does not validate the 
    fullscreen Permissions Policy browser-side. Add an 
    IsFeatureEnabled(kFullscreen) check before proceeding, and 
    report a bad message if the policy is not granted. This 
    matches the pattern used by CreatePaymentManager(), 
    GetUsbDeviceService(), and GetSerialService(). 
     
    Also remove the two TODO(alexmos) comments that noted this 
    missing check on EnterFullscreen and ExitFullscreen. 
     
    Bug: 488514078 
    Change-Id: I8ae0cfc07a104c9f555f7590db1e788d3e4067cd 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7616589 
    Reviewed-by: Mark Pearson <mpearson@chromium.org> 
    Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
    Commit-Queue: Alex Moshchuk <alexmos@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1604447}

```

---

Files:

- M `content/browser/bad_message.h`
- M `content/browser/renderer_host/render_frame_host_impl.cc`
- M `content/browser/security_exploit_browsertest.cc`
- M `content/browser/web_contents/web_contents_impl_unittest.cc`
- M `tools/metrics/histograms/metadata/stability/enums.xml`

---

Hash: [23da98ae6f278771869a49c7350b867dd10d24e5](https://chromiumdash.appspot.com/commit/23da98ae6f278771869a49c7350b867dd10d24e5)  

Date: Tue Mar 24 23:12:32 2026


---

### sp...@google.com (2026-05-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline with bisect. Security UI Spoofing


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/488514078)*
