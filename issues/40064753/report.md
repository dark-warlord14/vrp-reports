# Security: UXSS via com.android.browser.application_id Intent extra

| Field | Value |
|-------|-------|
| **Issue ID** | [40064753](https://issues.chromium.org/issues/40064753) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals |
| **Platforms** | Android |
| **Reporter** | we...@gmail.com |
| **Assignee** | ni...@chromium.org |
| **Created** | 2012-08-25 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**   
By sending a crafted intent to Chrome for Android, malicious Android  
apps can inject javascript: URIs into arbitrary Web pages loaded  
in Chrome. Injected javascript works in the context of the target  
Web page's domain, not a blank domain. So it can be used for Cook

## Attachments

- [poc1.txt](attachments/poc1.txt) (text/x-java; charset=us-ascii, 1.4 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064753)*
