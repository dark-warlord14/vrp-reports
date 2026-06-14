# It's possible to load chrome-extension:// URLs

| Field | Value |
|-------|-------|
| **Issue ID** | [40081020](https://issues.chromium.org/issues/40081020) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Sandbox>SiteIsolation, Platform>Extensions, UI>Browser>Navigation |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | co...@gmail.com |
| **Assignee** | lu...@chromium.org |
| **Created** | 2014-12-16 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.65 Safari/537.36

Steps to reproduce the problem:
1.Add a form element to a page with a named frame as a target.  Set the method as 'post' and the action attribute as any chrome-extension:// URL.
2

## Attachments

- [extensionLoad-testcase-new.html](attachments/extensionLoad-testcase-new.html) (text/html, 237 B)
- [extensionLoad-testcase-mod01.html](attachments/extensionLoad-testcase-mod01.html) (text/html, 249 B)
- [extensionLoad-testcase-alt.html](attachments/extensionLoad-testcase-alt.html) (text/html, 593 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081020)*
