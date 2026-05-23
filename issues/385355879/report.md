# Use after free in AddressSignInPromoView.

| Field | Value |
|-------|-------|
| **Issue ID** | [385355879](https://issues.chromium.org/issues/385355879) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Autofill>AddressesAndMore |
| **Platforms** | Linux, Mac, Windows |
| **Chrome Version** | 133.0.6907.0 |
| **Reporter** | ch...@gmail.com |
| **Assignee** | am...@google.com |
| **Created** | 2025-01-01 |
| **Bounty** | $2,000.00 |

## Description

# Steps to reproduce the problem

1. apply attached patch browser.diff [\*]
2. ./path/to/chrome --user-data-dir="/tmp/aaa" --enable-features=ImprovedSigninUIOnDesktop "<http://localhost:8000/poc.html>"
3. Click `Trigger the bug`, input and submit.
4. Click save and waiting for the UAF.
   [\*] This is just for quick reproduction and has nothing to do with the vulnerability itself. This can also be achieved by constructing appropriate form data.
   Since autofill data transmission is done via IPC, if it is a compromised renderer, the vulnerability can be triggered with just two clicks.

# Problem Description

AddressSignInPromoView will keep a pointer `web_contents_`, and the WebContents could be destroyed before AddressSignInPromoView[1].

Therefore, when the window is closed and WindowClosing is called, the released dangling pointer will be used in `static_cast<T*>(contents->GetUserData)`[2]

[1]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/autofill/address_sign_in_promo_view.cc;l=23;drc=5bda4ddf185dbc5591e994acecdf7d8d2c03ff49>
[2]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/autofill/address_sign_in_promo_view.cc;l=74;drc=5bda4ddf185dbc5591e994acecdf7d8d2c03ff49>

# Summary

Use after free in AddressSignInPromoView.

# Custom Questions

#### Type of crash:

browser

#### Crash state:

see attached asan file

#### Reporter credit:

anonymous

# Additional Data

Category: Security   

Chrome Channel: Dev   

Regression: N/A

## Attachments

- [asan](attachments/asan) (application/octet-stream, 18.0 KB)
- [browser.diff](attachments/browser.diff) (text/x-diff, 805 B)
- [demo.mp4](attachments/demo.mp4) (video/mp4, 551.5 KB)
- [poc.html](attachments/poc.html) (text/html, 353 B)
- [popup.html](attachments/popup.html) (text/html, 306 B)

## Timeline

### ch...@gmail.com (2025-01-01)

I also uploaded a demo video, you can refer to the video to reproduce.

### ch...@gmail.com (2025-01-01)

Bisect : https://chromium-review.googlesource.com/c/chromium/src/+/5776109

### pa...@chromium.org (2025-01-02)

[security shepherd] Thanks for your report. Unfortunately, I wasn't able to reproduce locally because I couldn't get `AddressSignInPromoView` to appear. However, manually looking at the code makes me believe this is totally triggereable. Since the feature is disabled by default, impact would be none. Setting sev to P1. Assigning to amelies@ based on reporter bisection. amelies@, can you help me triage further? Feel free to re-assess severity if you feel this isn't appropriate.

### ba...@google.com (2025-01-02)

CCing the reviewers...

### dr...@chromium.org (2025-01-02)

Here's the top of the stack trace from the "asan" file:

```
=================================================================
==384960==ERROR: AddressSanitizer: heap-use-after-free on address 0x74176c44e910 at pc 0x575bf75b9d63 bp 0x7ffe4e041720 sp 0x7ffe4e041718
READ of size 8 at 0x74176c44e910 thread T0 (chrome)
    #0 0x575bf75b9d62 in operator-> third_party/libc++/src/include/__memory/unique_ptr.h:280:101
    #1 0x575bf75b9d62 in base::SupportsUserData::GetUserData(void const*) const base/supports_user_data.cc:46:16
    #2 0x575c049fa9f1 in FromWebContents content/public/browser/web_contents_user_data.h:70:38
    #3 0x575c049fa9f1 in autofill::AddressSignInPromoView::WindowClosing() chrome/browser/ui/views/autofill/address_sign_in_promo_view.cc:78:3
    #4 0x575bff4e414a in views::Widget::HandleWidgetDestroying() ui/views/widget/widget.cc:2420:23

```

### dr...@chromium.org (2025-01-02)

The address signin promo is not launched to users, so I believe there is no way to trigger it.
The linked CL in #3 has been reverted, so the problem may be solved already. However I suspect another similar CL was relanded so we should check if the issue persists in the reland.

Amelie: can you see if this bug is still valid? If it has been fixed, then I think there is nothing to do and we can close this as obsolete.

### am...@google.com (2025-01-02)

Hello, thanks for reporting this!

Looking into it now.

### ch...@gmail.com (2025-01-02)

RE #7:
The problem still exists. After several reverts and relands, this feature was finally relanded in this commit:
https://chromium-review.googlesource.com/c/chromium/src/+/6063804

### am...@google.com (2025-01-02)

I was able to reproduce the bug on trunk, working on a fix now.

### ap...@google.com (2025-01-02)

Project: chromium/src  

Branch: main  

Author: Amelie Schneider <[amelies@google.com](mailto:amelies@google.com)>  

Link:      <https://chromium-review.googlesource.com/6113608>

[UNO] Fix UAF of web contents when address sign in promo is closed

---


Expand for full commit details
```
[UNO] Fix UAF of web contents when address sign in promo is closed 
 
When the window was closed with the address sign in promo open, an 
address bubble controller was created from web contents in an invalid 
sequence, causing a UAF. This fixes the UAF by checking the web 
contents before use. 
 
Bug: 385355879 
Change-Id: I8eee4bdda05b600674567e31113cbe7e47381133 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6113608 
Commit-Queue: Amelie Schneider <amelies@google.com> 
Reviewed-by: David Roger <droger@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1401440}

```

---

Files:

- M `chrome/browser/ui/views/autofill/address_sign_in_promo_view.cc`
- M `chrome/browser/ui/views/autofill/address_sign_in_promo_view.h`

---

Hash: a041f4edb0d1dd90c26f31accdd039f6efdee6ed  

Date:  Thu Jan 02 08:19:37 2025


---

### dr...@chromium.org (2025-01-02)

Note: there are a couple tests that are actually catching the issue:

- MigrateToProfileAddressProfileTest.SaveWithEdit
- SaveAddressProfileTest.SaveAccept
- UpdateAccountAddressProfileTest.UpdateThroughEdit

When enabling the feature and running the CQ, they fail with the same UaF.
I could verify that Amelie's fix makes them pass.

### sp...@google.com (2025-01-09)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
$1,000 for this report of a highly mitigated (mitigated by user gesture and that this would resulted in test failures upon enabling this feature and running CQ) memory corruption bug in a non-sandboxed process + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-01-09)

Congratulations! We did want to reward this report as it did save us future effort and catching this issue now rather than more closely to feature launch due to test failures and ensuring this issue was handled as a security issue. Thank you for your efforts and reporting this issue to us!

### dr...@chromium.org (2025-01-09)

Thank you, this report was indeed helpful. It helped us pinpoint the problem and made it easier to fix.

### ch...@google.com (2025-04-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> $1,000 for this report of a highly mitigated (mitigated by user gesture and that this would resulted in test failures upon enabling this feature and running CQ) memory corruption bug in a non-sandboxed process + $1,000 bisect bonus

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/385355879)*
