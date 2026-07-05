# RequestService::RequestToken() missing browser-side identity-credentials-get Permissions Policy enforcement

| Field | Value |
|-------|-------|
| **Issue ID** | [494449806](https://issues.chromium.org/issues/494449806) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Identity>FedCM, Blink>PermissionsPolicy |
| **Reporter** | os...@gmail.com |
| **Assignee** | os...@gmail.com |
| **Created** | 2026-03-20 |
| **Bounty** | $500.00 |

## Description

---

### Report description

RequestService::RequestToken() missing browser-side identity-credentials-get Permissions Policy enforcement

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://source.chromium.org/chromium/chromium/src/+/main:content/browser/webid/request_service.cc>

---

### The problem

#### Please describe the technical details of the vulnerability

`RequestService::RequestToken()` has no browser-side check for the `identity-credentials-get` Permissions Policy. The check exists only renderer-side (`authentication_credentials_container.cc:308`). A compromised renderer bypasses it and calls the `FederatedAuthRequest` Mojo interface directly.

**Vulnerable file:** [request\_service.cc](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/webid/request_service.cc) — `RequestToken()`, `RequestUserInfo()`, `Disconnect()`

Zero instances of `IsFeatureEnabled(kIdentityCredentialsGet)` in `content/browser/webid/`. The Mojo interface is unconditionally bound at `browser_interface_binders.cc:1171`. `Disconnect()` is also missing the check.

**Steps to reproduce:**

1. Check out stable tag: `git checkout 146.0.7680.76`
2. `git apply poc_patch.diff`
3. `autoninja -C out/Default chrome`
4. Start PoC server: `python3 serve.py`
5. Launch patched Chrome: `out/Default/Chromium.app/Contents/MacOS/Chromium`
6. Open `http://localhost:8080/`
7. The parent page sets `Permissions-Policy: identity-credentials-get=()`. The cross-origin iframe at `localhost:8081` calls `navigator.credentials.get()` with FedCM.
8. Click "Continue as Test" in the FedCM dialog.
9. Observe: the iframe receives a federated identity token despite the PP denial. The iframe shows "BUG CONFIRMED: FedCM succeeded despite PP denial!"

The renderer patch comments out the two renderer-side PP checks (the early rejection and the `SECURITY_CHECK`) to simulate a compromised renderer calling Mojo directly. No flags needed.

**Bisect:**

- Introducing commit: `bffd518194f7c` — Peter Kotwicz, June 14, 2022, M105. Added `federated-credentials` (now `identity-credentials-get`) Permissions Policy with renderer-side enforcement only. Browser-side check was never added.
- Affected: M105 through M146 (current stable).

**Fix:** Add `render_frame_host().IsFeatureEnabled(kIdentityCredentialsGet)` with `mojo::ReportBadMessage()` at the top of `RequestToken()`, `RequestUserInfo()`, and `Disconnect()`. Attached as `fix.diff`. Will upload Gerrit CL.

#### Impact analysis

The PoC demonstrates that a compromised renderer in a cross-origin iframe receives a federated identity token despite the parent setting `Permissions-Policy: identity-credentials-get=()`. This violates the `identity-credentials-get` Permissions Policy contract, which should be browser-enforced per Chrome's compromised renderer threat model.

---

### The cause

#### What version of Chrome have you found the security issue in?

146.0.7680.76 (Stable)

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Permissions Bypass

#### How would you like to be publicly acknowledged for your report?

Tianyi Hu

## Attachments

- [fix.diff](attachments/fix.diff) (application/octet-stream, 5.3 KB)
- [serve.py](attachments/serve.py) (text/x-python-script, 7.1 KB)
- [poc_patch.diff](attachments/poc_patch.diff) (application/octet-stream, 1.6 KB)

## Timeline

### os...@gmail.com (2026-03-20)

CL with fix to all 3 methods, plus unit tests:

<https://chromium-review.googlesource.com/c/chromium/src/+/7685939>

### pe...@google.com (2026-03-21)

The issue's primary component must be in the Component Tags, so re-adding it. To change the primary component, use the edit button at the top of the issue, just above the title.

### ch...@google.com (2026-03-21)

Setting Priority to P3 to match Severity s3. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-03-24)

Project: chromium/src  

Branch:  main  

Author:  Tianyi Hu [oscarhuthu@gmail.com](mailto:oscarhuthu@gmail.com)  

Link:    <https://chromium-review.googlesource.com/7685939>

Enforce identity-credentials-get Permissions Policy browser-side

---


Expand for full commit details
```
     
    RequestService::RequestToken(), RequestUserInfo(), and Disconnect() 
    do not check the identity-credentials-get Permissions Policy 
    browser-side. The check exists only in the renderer. Add 
    IsFeatureEnabled(kIdentityCredentialsGet) with ReportBadMessage() 
    to each method. 
     
    For RequestToken(), the check is in ShouldTerminateRequest(), 
    guarded by !navigation_handle, since navigation interception calls 
    are browser-initiated and do not need the check. 
     
    Bug: 494449806 
    Change-Id: I42cce0352ce1344a2e355b648bd3ddec2afc50e6 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7685939 
    Reviewed-by: Christian Biesinger <cbiesinger@chromium.org> 
    Reviewed-by: Nicolás Peña <npm@chromium.org> 
    Commit-Queue: Nicolás Peña <npm@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1604169}

```

---

Files:

- M `content/browser/webid/request_service.cc`
- M `content/browser/webid/request_service.h`
- M `content/browser/webid/request_service_multiple_frames_unittest.cc`
- M `content/browser/webid/request_service_unittest.cc`

---

Hash: [920737e00f4fcae7b718f43c8c0a7ddd7942dc5d](https://chromiumdash.appspot.com/commit/920737e00f4fcae7b718f43c8c0a7ddd7942dc5d)  

Date: Tue Mar 24 16:07:29 2026


---

### cb...@chromium.org (2026-03-24)

Unsure if this is important enough to merge to branches

### sp...@google.com (2026-05-16)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
web platform bypass via compromised renderer


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### os...@gmail.com (2026-05-18)

Hi team,

Just want to check there is no bisect and patch reward anymore? As the bisect is attached and my CL is merged as the fix.

### np...@google.com (2026-06-01)

Not sure anyone will monitor this bug from VRP but per the message you can email [security-vrp@chromium.org](mailto:security-vrp@chromium.org) asking your question

### ch...@google.com (2026-07-01)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/494449806)*
