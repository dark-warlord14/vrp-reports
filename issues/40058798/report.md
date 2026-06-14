# Security: TrustedTypes does not block assignment when modifying existing attribute value via nodeValue/textContent

| Field | Value |
|-------|-------|
| **Issue ID** | [40058798](https://issues.chromium.org/issues/40058798) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>TrustedTypes |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | vo...@chromium.org |
| **Created** | 2022-02-16 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**   
TrustedTypes blocks the following cases:  
```  
iframe.setAttribute('srcdoc','XSS');//blocked  
iframe.srcdoc='XSS';//blocked  
```  
But if the existing attribute value is modified via the nodeValue or textContent property, it does not block the assignment. e.g.:  
```

## Attachments

- [ttbypass_attr_nodeValue_textContent.html](attachments/ttbypass_attr_nodeValue_textContent.html) (text/plain, 492 B)
- [ttbypass_attr_nodeValue_textContent2.html](attachments/ttbypass_attr_nodeValue_textContent2.html) (text/plain, 517 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058798)*
