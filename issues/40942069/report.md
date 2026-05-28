# Security: Content-Type x-mixed-replace can be abused to bypass CSP on iOS

| Field | Value |
|-------|-------|
| **Issue ID** | [40942069](https://issues.chromium.org/issues/40942069) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature |
| **Platforms** | iOS |
| **CVE IDs** | CVE-2024-23263 |
| **Reporter** | jo...@gmail.com |
| **Assignee** | ah...@chromium.org |
| **Created** | 2023-11-13 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

A page that responds with the Content-Type multipart/x-mixed-replace can bypass the same requests CSP header by overwriting the CSP in one of the response parts

Given a server response like this

```
:status: 200  
Content-Type: multipart/x-mixed-replace; boundary=TEST  
Content-Security-Policy: sandbox  
/.. rest of headers ../  
  
--TEST  
Content-Type: text/html  
Content-Security-Policy:  
  
<script>alert(document.domain)</script>  
--TEST--  

```

will trigger the alert (on the real domain) even if the initial response has a CSP header with the value `sandbox`.

This behaviour looks to be a webkit bug. In Chrome on desktop the `multipart/x-mixed-replace` content-type is only allowed for images.

In Firefox the additional CSP headers in the response body will "merge" with the initial CSP and thus not execute in this case. For Chrome on iOS the CSP is instead overwritten by the new value and thus bypassed.

Even if you bypass the CSP in Firefox the sandbox value will force the document to act from a null origin. In Chrome on iOS the JS will run in the context of the domain.

**VERSION**  

Chrome Version: 119.0.6045.109  

Operating System: iOS 16.6.1

**REPRODUCTION CASE**  

Visit <https://joaxcar.com/ios/csp.php> in Chrome on iOS. The CSP in the response is `sandbox` but the JS script will trigger.

The PHP file used here looks like this

```
<?php  
header("Content-Type: multipart/x-mixed-replace; boundary=TEST");  
header("Content-Security-Policy: sandbox");  
?>  
--TEST  
Content-Type: text/html  
Content-Security-Policy:  
  
<script>alert(document.domain)</script>  
--TEST--  

```

The empty CSP in the --TEST block will remove any CSP from the page.

### Impact Note

I have been able to use this to bypass CSP in Grafana (the monitoring platform) where they have an endpoint where they render proxied content. To protect the server domain from XSS they add CSP sandbox to all proxied responses. Using this bug here I was able to bypass CSP and gain full XSS due to them allowing me to set Content-Type and control the response body.

**CREDIT INFORMATION**  

Johan Carlsson (joaxcar)

## Timeline

### [Deleted User] (2023-11-13)

[Empty comment from Monorail migration]

### dr...@chromium.org (2023-11-13)

Thanks for the report! I'm not entirely clear if this is a security bug in Chrome. Some kinds of CSP bug that allow for XSS in otherwise well-configured servers are in scope as Chrome security bugs, but I would imagine exploitation here requires a server that relies on the CSP for protecting users from XSS, but also allows user-generated content to set headers in the responses. I'm not really convinced that's a well-configured server.

I'm not an expert on CSP though, so adding others for thoughts. arthursonzogni@ - I see you own third_party/blink/renderer/core/frame/csp/. What do you think? Is this a security bug, functional bug, or neither?

[Monorail components: Blink>SecurityFeature]

### ad...@google.com (2023-11-13)

(I am a bot: this is an auto-cc on a security bug)

### ar...@google.com (2023-11-14)

(current security shepherd here)

Thanks for reporting this!

I opened a webkit bug: https://bugs.webkit.org/show_bug.cgi?id=264811
Security_Impact-Stable: @ahijazi was able to reproduce on iOS. Thanks!
Security_Severity-Low: (tentatively) This could be considered as a CSP bypass with the extreme mitigating factors that the server uses `Content-Type: multipart/x-mixed-replace` with two different set of CSPs.

This is now in the hands of webkit developers.

### [Deleted User] (2023-11-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-14)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-05)

[Empty comment from Monorail migration]

### is...@google.com (2023-12-05)

This issue was migrated from crbug.com/chromium/1501759?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### mk...@chromium.org (2024-02-05)

Assigning to Arthur to see if the underlying webkit issue is resolved; I don't have access to the bug.

### dd...@apple.com (2024-02-05)

The WebKit issue is not resolved yet.

### jo...@gmail.com (2024-04-11)

Hi again! I do think that this is fixed now with CVE-2024-23263. Release notes <https://support.apple.com/en-gb/HT214082> mention WebKit Bugzilla: 264811

I don't have access to the webkit bug so I can not confirm with the discussion there

/johan

### ar...@chromium.org (2024-04-11)

I CCed mkwst, and asked Ryan (Apple developer) to update the bug status.

---

> I don't have access to the webkit bug so I can not confirm with the discussion there

In the bug, you email address is listed as CC.

---

> do think that this is fixed now with CVE-2024-23263.

Great! Could you or @ah...@chromium.org check if the bug stopped reproducing on this new version?
If yes, then we can close this bug as "verified".

### jo...@gmail.com (2024-07-09)

hi again, yes to me this looks fixed. Since 17.4, the POC is not working on my iPhone anymore at least

### ar...@chromium.org (2024-07-09)

Thanks!
Apple developer also closed the bug, and confirmed it was fixed.

### ar...@chromium.org (2024-07-09)

- Fixed in: [iOS:16.7.6](https://support.apple.com/en-gb/HT214082)
- WebKit Bugzilla: [264811](https://bugs.webkit.org/show_bug.cgi?id=264811)
- **CVE-2024-23263**: Johan Carlsson (joaxcar)

### sp...@google.com (2024-08-01)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
$2,000 for report of low-to-moderate impact exploit mitigation bypass


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-08-02)

Since this is mitigated to being constrained to being exploitable on specific sites, we consider this a bit below moderate impact. We do, however, appreciate the nice quality reporting. Thanks for your efforts and reporting this issue to us, Johan!

### pe...@google.com (2024-10-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40942069)*
