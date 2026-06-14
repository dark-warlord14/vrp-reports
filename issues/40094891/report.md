# Security: storage estimate allows obtaining size of cached cross-origin resource

| Field | Value |
|-------|-------|
| **Issue ID** | [40094891](https://issues.chromium.org/issues/40094891) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Storage>Quota, Internals>Network>Cache |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | to...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2019-05-07 |
| **Bounty** | $500.00 |

## Description

The available quota is calculated as min(10% available disk space, 2GB); by opening/prerendering a website, certain resources might be cached. This will affect the available disk space (and the quota). By observing the quota before and after opening the website, it's possible to obtain the (exact) s

## Attachments

- [cache-spy.html](attachments/cache-spy.html) (text/plain, 1.1 KB)
- [cache-spy-url.html](attachments/cache-spy-url.html) (text/plain, 1.6 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094891)*
