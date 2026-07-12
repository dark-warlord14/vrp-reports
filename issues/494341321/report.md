# Extension access to passkeys (webauthn) bypasses runtime_blocked_hosts enterprise policy

| Field | Value |
|-------|-------|
| **Issue ID** | [494341321](https://issues.chromium.org/issues/494341321) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | ns...@chromium.org |
| **Created** | 2026-03-20 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

The `ExtensionCanAssertRpId` function (in [chrome\_web\_authentication\_delegate.cc](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/webauthn/chrome_web_authentication_delegate.cc;l=130-189;drc=5112a539ef7979b1a5cb29b9171b77c40fb20969)) validates whether an extension is allowed to pass a given domain as a [RP ID](https://w3c.github.io/webauthn/#relying-party-identifier) to the `navigatior.credentials` API. Being able to do so allows an extension to impersonate a domain when dealing with passkeys. The vulnerability is that `ExtensionCanAssertRpId` only checks host permissions, not enterprise policies. The relevant enterpise policy is documented at <https://www.chromium.org/administrators/policy-list-3/extension-settings-full/> as:

> "runtime\_blocked\_hosts": Maps to a list of strings representing hosts whose webpages the extension will be blocked from modifying.
> This includes injecting javascript, altering and viewing webRequests / webNavigation, **viewing and altering cookies**, exceptions to the same-origin policy, etc.

Note my emphasis on cookies. Passkeys are the superior form of cookies for authentication, yet extensions are not restricted from accessing passkeys for a domain that they can otherwise not access through scripting.

A Google engineer makes the following assertion on security in an announcement on the [webauthn mailing list](https://lists.w3.org/Archives/Public/public-webauthn/2023Dec/0078.html):

> This should not fundamentally change the security and privacy properties of
> WebAuthn, as extensions with host permissions can already script pages
> running on those hosts and thus claim the same relying party identifiers.

When the `runtime_blocked_hosts` enterprise policy is used to protect domains from extensions, the extension cannot run scripts on the specified domains. But this report demonstrates that an extension can still impersonate such a domain in the WebAuthn API to access passkeys.

**VERSION**  

Chrome Version: 146.0.7680.153  

Operating System: Any desktop OS (tested with Linux)

**REPRODUCTION CASE**

1. Create a policy that prevents extensions from accessing google.com domains.
   E.g. on Linux, create `/etc/chromium/policies/managed/block-google.json` (Chromium) or `/etc/opt/chrome/policies/managed/block-google.json` (Chrome) containing
   ```
   {
     "ExtensionSettings": {
       "*": {
         "runtime_blocked_hosts": ["*://*.google.com"],
         "blocked_permissions": []
       }
     }
   }
   
   ```
2. Download the attached files `manifest.json`, `poc.html` and `poc.js` to a directory.
3. Visit `chrome://extensions/` and load that directory as an unpacked extension.
4. Sanity check: Visit `chrome://policy` to verify that the enterprise policy restricting extension access to `google.com` was applied.
5. Click on the extension button, click on "WebAuthn RP ID test" to open the test page.  
   
   ( optional, if you want to shield your real passkeys: emulate an authenticator with the devtools: <https://developer.chrome.com/docs/devtools/webauthn/> )
6. With `RP ID:` `example.com`, click on `Query credentials for RP ID`.
7. With `RP ID:` `example.net`, click on `Query credentials for RP ID`.
8. With `RP ID:` `google.com`, click on `Query credentials for RP ID`.

Expected:

- Step 6 triggers a request for a passkey ("Use your security key with example.com")
- Step 7 fails immediately with `SecurityError`. This is because `example.net` is not part of the extension's host permissions.
- Step 8 should be like step 7 (despite `google.com` being listed in the extension's host permissions), because access should be blocked by the enterprise policy.

Actual:

- Step 8 behaves like step 6, i.e. despite an enterprise policy protecting `google.com` from extensions, the browser still allows the extension access to passkeys from `google.com`.

**CREDIT INFORMATION**  

Reporter credit: Rob Wu

## Attachments

- [manifest.json](attachments/manifest.json) (application/json, 211 B)
- [poc.html](attachments/poc.html) (text/html, 1.2 KB)
- [poc.js](attachments/poc.js) (text/javascript, 735 B)

## Timeline

### ma...@google.com (2026-03-20)

Thanks for the report!

Limited extension permission bypass should be S3 IMO.

### ch...@google.com (2026-03-21)

Setting Priority to P3 to match Severity s3. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### ns...@chromium.org (2026-03-27)

Thank you so much for your excellent bug report! In a sea of AI slop, a high quality report is refreshing (even if I introduced the bug in the first place :)).

### dx...@google.com (2026-03-30)

Project: chromium/src  

Branch:  main  

Author:  Nina Satragno [nsatragno@chromium.org](mailto:nsatragno@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7707959>

[webauthn] Fix extension RP ID handling

---


Expand for full commit details
```
     
    Checking the list of allowed hosts is not enough to assert that an 
    extension can script a given origin. Align RP ID permissions with 
    scripting permissions by relying on `HasHostPermission` instead of 
    iterating the list of allowed hosts for an extension. 
     
    This solution unfortunately adds additional two additional restrictions 
    to claiming RP IDs that do not apply to normal websites: 
    * Extensions must have permissions over the origin corresponding to the 
      claimed RP ID. It is no longer enough to have permissions over a 
      subdomain. 
    * Extensions must have permissions over the origin corresponding to the 
      default https port for RP IDs other than the extension ID or 
      localhost. 
     
    There is some potential to break extensions that fall into these edge 
    cases. The solution should be straightforward though: simply claim the 
    origin matching the claimed RP ID. 
     
    Fixed: 494341321 
    Change-Id: I3c25e9432d71ab7126bcfe7416a14ddacd3720bb 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7707959 
    Reviewed-by: Oliver Dunk <oliverdunk@chromium.org> 
    Commit-Queue: Nina Satragno <nsatragno@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1607097}

```

---

Files:

- M `chrome/browser/webauthn/chrome_web_authentication_delegate.cc`
- M `chrome/browser/webauthn/chrome_web_authentication_delegate_unittest.cc`

---

Hash: [ecf43dd2aa505fc586380559884f304e1846c32d](https://chromiumdash.appspot.com/commit/ecf43dd2aa505fc586380559884f304e1846c32d)  

Date: Mon Mar 30 14:41:36 2026


---

### sp...@google.com (2026-05-16)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
web platform privilege escalation (extension permissions)


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/494341321)*
