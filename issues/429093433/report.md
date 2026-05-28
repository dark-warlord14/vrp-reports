# Security: WebAuthn dialog URL is not elided correctly on macOS


| Field | Value |
|-------|-------|
| **Issue ID** | [429093433](https://issues.chromium.org/issues/429093433) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Blink>WebAuthentication |
| **Platforms** | Mac |
| **Chrome Version** | 138.0.7204.93 |
| **Reporter** | sy...@gmail.com |
| **Assignee** | ns...@chromium.org |
| **Created** | 2025-07-02 |
| **Bounty** | Confirmed (amount unknown) |

## Description

# Steps to reproduce the problem

1. Visit: <https://longextendedsubdomainnamewithoutdashesinordertotestwordwrapping.badssl.com/>
2. Copy paste this script to console tab

```
setTimeout(async () => {
  if (!window.PublicKeyCredential) {
    console.error("WebAuthn tidak didukung di browser ini.");
    return;
  }

  console.log("⏳ Memulai proses WebAuthn setelah 2 detik...");

  const challenge = new Uint8Array(32);
  window.crypto.getRandomValues(challenge);

  try {
    const result = await navigator.credentials.get({
      publicKey: {
        challenge: challenge.buffer,
        timeout: 60000,
        userVerification: "preferred",
        allowCredentials: []
      }
    });

    console.log("✅ WebAuthn sukses!");
    console.log("📌 Credential ID:", result.id);
    console.log("📄 Type:", result.type);
    console.log("📦 Authenticator response:", result.response);
  } catch (err) {
    console.error("❌ WebAuthn gagal atau dibatalkan:", err);
  }
}, 2000); // Ganti ke 3000 jika butuh waktu lebih

```

3. See that only the left-most portion of the subdomain is visible in the WebAuthN dialog (see attached screenshot).

# Problem Description

As you can see on <https://issues.chromium.org/issues/40092650> , I noticed that the URL is not elided in the WebAuthn dialog on macOS as well.

# Summary

Security: WebAuthn dialog URL is not elided correctly on macOS

# Custom Questions

#### Reporter credit:

Syarif Muhammad Sajjad

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [Screenshot 2025-07-02 at 20.03.52.png](attachments/Screenshot 2025-07-02 at 20.03.52.png) (image/png, 1.0 MB)
- [Screen Recording 2025-07-02 at 20.02.18.mov](attachments/Screen Recording 2025-07-02 at 20.02.18.mov) (video/quicktime, 24.9 MB)

## Timeline

### ke...@chromium.org (2025-07-02)

Thanks for the report.

I agree we should be following the usual domain elision conventions on this dialog.

Since this is a sign-in dialog for the current origin this is low severity.

### sy...@gmail.com (2025-07-22)

Hi team any update?

### dx...@google.com (2025-07-30)

Project: chromium/src  

Branch:  main  

Author:  Nina Satragno [nsatragno@chromium.org](mailto:nsatragno@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6798506>

[webauthn] Fix missing RP ID eliding

---


Expand for full commit details
```
     
    Fix missing RP ID eliding for the following cases: 
    * Ambient bubble. 
    * Immediate mediation dialog. 
    * QR code / USB sheet. 
     
    This also stops hardcoding the elision width. 
     
    Fixed: 429093433 
    Change-Id: Ifae9100bfc773b908a7b41e4999100c2eb53295d 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6798506 
    Commit-Queue: Nina Satragno <nsatragno@chromium.org> 
    Reviewed-by: Ken Buchanan <kenrb@chromium.org> 
    Auto-Submit: Nina Satragno <nsatragno@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1494197}

```

---

Files:

- M `chrome/browser/ui/views/webauthn/ambient/ambient_signin_bubble_view.cc`
- M `chrome/browser/ui/views/webauthn/authenticator_hybrid_and_security_key_sheet_view.cc`
- M `chrome/browser/ui/webauthn/ambient/ambient_signin_controller.cc`
- M `chrome/browser/ui/webauthn/ambient/ambient_signin_controller.h`
- M `chrome/browser/ui/webauthn/sheet_models.cc`
- M `chrome/browser/ui/webauthn/sheet_models.h`
- M `chrome/browser/ui/webauthn/webauthn_ui_helpers.cc`
- M `chrome/browser/ui/webauthn/webauthn_ui_helpers.h`

---

Hash: [d162321296bb1d4a2711cb0fd1fb29da4e1662bb](http://crrev.com/d162321296bb1d4a2711cb0fd1fb29da4e1662bb)  

Date: Wed Jul 30 14:53:59 2025


---

### sy...@gmail.com (2025-08-02)

Hi team thanks for update. How about bounty?

### sy...@gmail.com (2025-08-09)

Hi team any update?

### am...@chromium.org (2025-08-11)

Hello, VRP reports are assessed at Chrome VRP panel, which is generally held weekly. Bugs are assessed in order of severity (critical to low) and by age. This report will be reviewed at a future VRP panel session in the coming weeks. Reward decision will be communicated directly on the bug following it's assessment. Please refrain from pinging on the bug for updates in the meantime and thank you for your patience.

### sy...@gmail.com (2025-08-26)

Any update about the VRP reward? it's morethan 2 weeks.

### sp...@google.com (2025-09-04)

** NOTE: This is an automatically generated email **

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this issue does not meet the criteria to qualify for a reward.

Rationale for this decision:
Thank you for the report. This appears to be a functional issue rather than an issue that would result in security implications to a user, as the full and correct origin information is clearly presented to the user in the omnibox. Since there are not security consequences here, we are unfortunately unable to extend a Chrome VRP reward for this report. 

Please note that the fact that this issue is not being rewarded does not mean that the product team won't fix the issue. We have filed a bug with the product team and they will review your report and decide if a fix is required. We'll let you know if the issue was fixed.

Regards,
Google Security Bot


--
How did we do? Please fill out a short anonymous survey (https://goo.gl/IR3KRH).

### sy...@gmail.com (2025-09-06)

I am very disappointed with the Chrome VRP Panel's decision to deny a bounty for the report “Security: WebAuthn dialog URL is not elided correctly on macOS.” This decision feels unfair and inconsistent, considering that a similar report, “Security: Web Share dialog URL is not elided correctly on Android” (<https://issues.chromium.org/issues/40059765>
), received a $500 bounty. Both cases are identical in nature, both involve system dialogs displaying URLs incorrectly, both impact the security UI aspect that could mislead users, and both are categorized as external security reports. Why is the Android case considered important enough to receive a bounty, while the macOS case, which clearly has a similar impact, is considered only a functional issue? This inconsistency makes the reporter feel undervalued, even though my report has resulted in real improvements in Chromium. I demand an objective explanation of the basis for this difference in decision-making, because if Android can receive $500, then this macOS case should be treated with the same standard.

### ke...@chromium.org (2025-09-08)

You're right that incorrect URL elision can often be a security bug, but it depends on the context. Users often have to rely on displayed URLs to understand what site they are interacting with, and if being misled about the site can create a risk to the user, then we do treat that as a Chrome vulnerability. However, the Relying Party Identifier (RPID) of a WebAuthn credential is guaranteed to be matched to the site that is invoking the request, and so the only consequence of a misleading RPID is that the user might not be clear about what site to which they are currently signing in. We want our UI to be as clear as possible to users, but signing in to a website using a credential that belongs to that website does not put users at risk in the same way that misleading URLs on other surfaces can.

### ch...@google.com (2025-11-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Thank you for the report. This appears to be a functional issue rather than an issue that would result in security implications to a user, as the full and correct origin information is clearly presented to the user in the omnibox. Since there are not security consequences here, we are unfortunately unable to extend a Chrome VRP reward for this report. 
> 
> Please note that the fact that this issue is not being rewarded does not mean that the product team won't fix the issue. We have filed a bug wit

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/429093433)*
