# WebInstallService InstallFromElement() bypasses WEB_APP_INSTALLATION permission prompt via renderer-callable Mojo method

| Field | Value |
|-------|-------|
| **Issue ID** | [487568011](https://issues.chromium.org/issues/487568011) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>WebAppInstalls |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | os...@gmail.com |
| **Assignee** | mk...@chromium.org |
| **Created** | 2026-02-25 |
| **Bounty** | $4,000.00 |

## Description

---

### Report description

WebInstallService InstallFromElement() bypasses WEB\_APP\_INSTALLATION permission prompt via renderer-callable Mojo method

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/web_applications/web_install_service_impl.cc>

---

### The problem

#### Please describe the technical details of the vulnerability

`WebInstallServiceImpl::InstallFromElement()` sets `triggered_from_element_ = true` then calls `Install()`. In `RequestWebInstallPermission()`, this flag causes the `WEB_APP_INSTALLATION` permission to be auto-granted without showing a permission prompt. A compromised renderer can call `InstallFromElement()` directly via Mojo to install cross-origin PWAs without user consent to the permission.

The permission bypass was designed intentionally for the `<install>` HTML element — the rationale being that a user clicking an `<install>` element already implies consent, so no separate permission prompt is needed. However, this design violates the Chromium security model: Mojo does not enforce which renderer code path invoked a method. The browser cannot distinguish between a call from a legitimate `<install>` element click handler and a call from compromised renderer code. Both arrive as the same `InstallFromElement()` IPC. The `triggered_from_element_` flag is therefore a renderer-trusted boolean that the browser uses to make a security decision — a classic Mojo trust boundary violation. The existing test `InstallWithUrl_IgnoresDeniedPermission` explicitly asserts this bypass works, confirming the design intent, but the threat model was not considered.

**Vulnerable files:**

- Mojo definition: [web\_install.mojom](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/public/mojom/web_install/web_install.mojom)
- Browser: [web\_install\_service\_impl.cc](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/web_applications/web_install_service_impl.cc)
- Registration: [chrome\_browser\_interface\_binders.cc](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/chrome_browser_interface_binders.cc)

**Transmission chain:**

1. The renderer calls `WebInstallService::InstallFromElement(options, callback)` via Mojo. This method is intended only for the `<install>` HTML element, but any renderer code can call it.
2. In `WebInstallServiceImpl::InstallFromElement()`, the browser unconditionally sets `triggered_from_element_ = true`, then delegates to `Install()`.
3. `Install()` eventually calls `RequestWebInstallPermission()`. When the permission status is `ASK`, the method checks `triggered_from_element_`:

```
if (triggered_from_element_) {
  // Do not show permission prompt for installs from an element entry point.
  // Grant permission by default if not already granted or denied.
  std::move(callback).Run(
      std::vector<content::PermissionResult>({content::PermissionResult(
          PermissionStatus::GRANTED,
          content::PermissionStatusSource::UNSPECIFIED)}));
  return;
}

```

4. The permission is auto-granted and the install proceeds without a permission prompt.
5. Additionally, `triggered_from_element_` is never reset, so all subsequent `Install()` calls on the same `WebInstallServiceImpl` instance also bypass the permission prompt (sticky state).

**Steps to reproduce:**

1. Check out stable tag: `git checkout -b poc 145.0.7632.117`
2. `git apply poc_patch.diff`
3. `autoninja -C out/Default chrome -j8`
4. Place PoC files (`index.html`, `serve.py`) in a directory and start the server:
   - `python3 serve.py`
5. Launch patched Chrome:
   - `out/Default/Chromium.app/Contents/MacOS/Chromium --user-data-dir=/tmp/chrome-poc-test --enable-blink-features=WebAppInstallation http://localhost:8080/index.html`
6. Click "Install cross-origin PWA". The install dialog appears directly without a permission prompt.

The renderer patch replaces `Install()` with `InstallFromElement()` in the renderer's `navigator.install()` implementation, simulating a compromised renderer. `--enable-blink-features=WebAppInstallation` is needed to expose the JS API, but the underlying Mojo interface is already bound by default (the `kWebAppInstallation` base feature is enabled by default).

**Bisect:**
Introducing commit: `1fd86f307a82e5a58bb86dafcb0e19cb7c29016e`

- Author: Kristin Lee ([kristinlee@microsoft.com](mailto:kristinlee@microsoft.com)), Dec 19 2025
- Message: "[<install> Element] Do not show the permission prompt"
- CL: <https://chromium-review.googlesource.com/c/chromium/src/+/7266918>
- Evidence: parent `f8e2c3ebdf4e904db590874c40168861ccf4f606` has no `InstallFromElement` or `triggered_from_element_`; this commit adds both.
- Cr-Commit-Position: refs/heads/main@{#1560950} — after M144 branch (1552494), before M145 branch (1568190).
- Earliest affected: M145. Latest confirmed: M145 (145.0.7632.117).

Note: a follow-up commit `8d4441fe2c2a7f58a3db483da333f9ed0b933822` (Jan 20 2026, CL <https://chromium-review.googlesource.com/c/chromium/src/+/7278710>) changed the bypass from "allow unless previously denied" to "always GRANTED unconditionally," worsening the bug in M146+.

**Suggested fix (attached as `fix.diff`):**

Remove `triggered_from_element_` from the permission bypass condition in `Install()`:

```
-  if (triggered_from_element_ || install_target == last_committed_url_) {
+  if (install_target == last_committed_url_) {

```

The browser cannot verify that `InstallFromElement()` was called from a genuine `<install>` element versus a compromised renderer. The fix removes the renderer-trusted flag from the permission decision, so `InstallFromElement()` goes through the normal `RequestWebInstallPermission()` flow. The `triggered_from_element_` field is retained for UMA/UKM metrics routing only. The existing `InstallWithUrl_IgnoresDeniedPermission` test is updated to expect permission denial instead of bypass.

#### Impact analysis

A compromised renderer can install arbitrary cross-origin PWAs without the `WEB_APP_INSTALLATION` permission prompt. This bypasses the permission model that gates the Web Install API.

**User harm:**

- **Phishing:** Install a malicious PWA mimicking a banking/email app — PWAs appear as native apps with no browser chrome, making phishing more convincing.
- **Persistence:** PWAs persist beyond browser sessions and appear in the OS app list/dock, giving the attacker a persistent foothold.
- **No user awareness:** The permission prompt is the user's only signal that a cross-origin install is happening. Bypassing it means the user sees only the install dialog (which may look legitimate) without the preceding "allow this site to install apps?" consent.

**Reachability:** A compromised renderer in any top-level frame on desktop Chrome. Reachable via renderer exploits (e.g., V8 bugs) or compromised ad network code.

**Compounding factors:**

1. The `triggered_from_element_` flag is sticky — once set, it persists for the lifetime of the `WebInstallServiceImpl` instance, so all subsequent `Install()` calls on the same document also bypass the permission prompt.
2. On M145 (stable), the bypass is in `RequestWebInstallPermission()` after the `GRANTED`/`DENIED` switch — so the bypass fires when permission status is `ASK` (the default). A user who previously clicked "Block" is protected. However, on `main` (shipping in M146), the bypass was moved **before** `RequestWebInstallPermission()` entirely (line 320: `if (triggered_from_element_ || ...)` → `OnPermissionDecided(GRANTED)`), meaning the permission is auto-granted even if the user previously denied it. This makes the M146 variant strictly worse.

---

### The cause

#### What version of Chrome have you found the security issue in?

145.0.7632.117 (Stable)

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Permissions Bypass

#### How would you like to be publicly acknowledged for your report?

Tianyi Hu

## Attachments

- [fix.diff](attachments/fix.diff) (application/octet-stream, 5.8 KB)
- [poc_patch.diff](attachments/poc_patch.diff) (application/octet-stream, 1.0 KB)
- [serve.py](attachments/serve.py) (text/x-python-script, 2.4 KB)
- [index.html](attachments/index.html) (text/html, 737 B)

## Timeline

### os...@gmail.com (2026-02-25)

The fix CL: <https://chromium-review.googlesource.com/c/chromium/src/+/7607759>

### aj...@google.com (2026-02-26)

Reading the report and code I believe this seems like a possible bypass of the web-app install permission prompt from a compromised renderer.



### aj...@google.com (2026-02-26)

I'm not sure what the security model for these browser-hosted permission chips is, so this might not in fact be a security issue - mkwst hopefully can answer this.

### ch...@google.com (2026-02-26)

Setting milestone because of s2 severity.

### ch...@google.com (2026-02-26)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### li...@microsoft.com (2026-02-26)

Thanks for the report! I've opened the following bug to track the issue with `triggered_from_element_`.

<https://issues.chromium.org/487938764> [<install> Element] triggered\_from\_element\_ should not be sticky

Re. the rest of the issues described in this bug, will defer to @mk...@google.com to explain the security model here.

### mk...@chromium.org (2026-03-02)

We've intentionally chosen to rely only upon the app installation dialog when installation is explicitly triggered through an `<install>` element.

The permission prompt is helpful (necessary?) for an imperative API, insofar as it confirms a user's intent to allow a given origin to trigger an installation flow at an arbitrary point. It seems superfluous in a situation where we have a firm understanding of what the user clicked upon, and can derive a strong signal of intent from that understanding.

I agree with you that the boolean is not verifiable by the browser in our current implementation, and that corrupted renderers will indeed be able to cause an installation prompt to appear. That prompt, however, does attempt to make it clear that an installation is happening cross-origin: it contains both the origin of the page causing the prompt and the origin of the PWA being installed. If you're concerned that the dialog isn't clear enough, it's worth discussing improvements.

We should likewise probably ensure that a gesture could have been available to the renderer (and consume it) so that a renderer can't spam the app installation dialog, but allowing a renderer to pop up a single dialog per click doesn't seem out of line to me, as it maintains the constraint that PWAs are installed only with user opt-in, just like every other powerful feature.

Tagging cthomp@ for more informed opinions from a UX perspective, but this setup seems quite reasonable to me.

### os...@gmail.com (2026-03-02)

Thanks for the detailed explanation and I do agree the dialog already provides sufficient user consent. Glad the sticky flag is being tracked separately.

### dx...@google.com (2026-03-03)

Project: chromium/src  

Branch:  main  

Author:  Lia Hiscock [liahiscock@microsoft.com](mailto:liahiscock@microsoft.com)  

Link:    <https://chromium-review.googlesource.com/7615447>

[WebInstall] Fix triggered\_from\_element\_ sticky state

---


Expand for full commit details
```
     
    WebInstallServiceImpl::InstallFromElement() set the member 
    triggered_from_element_ to true but never reset it. Because the service 
    instance is per-document, a subsequent navigator.install() call on the 
    same page reused the stale flag, skipping the permissions-policy gate 
    and the WEB_APP_INSTALLATION permission prompt. 
     
    Replace the mutable member with a local parameter by introducing a 
    private InstallInternal(options, callback, triggered_from_element) 
    helper. Install() forwards with false; InstallFromElement() forwards 
    with true. This ensures the flag is scoped to a single call and cannot 
    leak across Mojo method invocations. 
     
    Add a regression test that performs an <install>-element install 
    followed by a navigator.install() call on the same document with the 
    WEB_APP_INSTALLATION permission blocked, and verifies that the JS API 
    call is correctly denied. 
     
    Bug: 487938764, 487568011, 333795265 
    Change-Id: Ibe56b00bcb1018a25bfadce92dcdc98e4f9c4360 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7615447 
    Reviewed-by: Lu Huang <luhua@microsoft.com> 
    Reviewed-by: Marijn Kruisselbrink <mek@chromium.org> 
    Commit-Queue: Lia Hiscock <liahiscock@microsoft.com> 
    Cr-Commit-Position: refs/heads/main@{#1593535}

```

---

Files:

- M `chrome/browser/web_applications/install_element_browsertest.cc`
- M `chrome/browser/web_applications/web_install_service_impl.cc`
- M `chrome/browser/web_applications/web_install_service_impl.h`

---

Hash: [35d688b7c5984f28b1cfe4816a93b586fabf6cd6](https://chromiumdash.appspot.com/commit/35d688b7c5984f28b1cfe4816a93b586fabf6cd6)  

Date: Tue Mar 3 22:39:46 2026


---

### ch...@google.com (2026-03-17)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $4000.00 for this report.

Rationale for this decision:
Moderate Impact. Web platform privilege escalation.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/487568011)*
