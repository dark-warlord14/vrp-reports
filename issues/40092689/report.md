# Security: Markup injection is possible in the Preview feature in the Developer Tools due to mishandling of URI encoded strings

| Field | Value |
|-------|-------|
| **Issue ID** | [40092689](https://issues.chromium.org/issues/40092689) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P3 |
| **Component** | Platform>DevTools |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | sh...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2018-10-13 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**   
Preview feature in the Developer Tools handles URI encoded strings in the response body in an unsafe manner that allows for markup injections. The URI encoded strings are decoded and interpreted as part of the HTML, therefore someone who is able to inject a URI encoded s

## Attachments

- [index.html](attachments/index.html) (text/plain, 301 B)
- [chrome-preview-injection-8ubB4QAUdhB42iE.png](attachments/chrome-preview-injection-8ubB4QAUdhB42iE.png) (image/png, 560.6 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092689)*
