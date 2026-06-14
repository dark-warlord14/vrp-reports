# ignored TLS errors propagate from webview to main browser

| Field | Value |
|-------|-------|
| **Issue ID** | [40085151](https://issues.chromium.org/issues/40085151) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Network>SSL, UI>Browser>Interstitials |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ja...@googlemail.com |
| **Assignee** | es...@chromium.org |
| **Created** | 2016-08-19 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36

Steps to reproduce the problem:
1. Add the attached app to Chrome. Note that it does not request any user-visible permissions.
2. Go to https://37.221.195.125/. You'll see the TL

## Attachments

- [webview-tls-test.crx](attachments/webview-tls-test.crx) (application/octet-stream, 1.5 KB)
- [webview-tls-test.zip](attachments/webview-tls-test.zip) (application/octet-stream, 1.4 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085151)*
