# Security: Access-Control-Expose-Headers is not honored for redirects

| Field | Value |
|-------|-------|
| **Issue ID** | [40094855](https://issues.chromium.org/issues/40094855) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Network>XHR, Blink>SecurityFeature>CORS |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sh...@gmail.com |
| **Assignee** | yh...@chromium.org |
| **Created** | 2019-05-03 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**   
CORS defines a mechanism to hide custom response headers, unless explicitly allowed by listing in Access-Control-Expose-Headers. Chrome exposes all headers regardless, if response is a result of a redirect from first party to third-party.   
  
I expect Chrome to follow

## Attachments

- deleted (application/octet-stream, 0 B)
- [cors_redirect_testcase.go](attachments/cors_redirect_testcase.go) (text/plain, 1.4 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094855)*
