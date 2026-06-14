# Security: Heap-use-after-free in TypedArray.join

| Field | Value |
|-------|-------|
| **Issue ID** | [40093588](https://issues.chromium.org/issues/40093588) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | jg...@chromium.org |
| **Created** | 2018-12-27 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**   
While verifying the fix for https://crbug.com/chromium/915783, I noticed another issue in |TypedArray.join|. Converting the |separator| argument to a string has side effects, and then the method doesn't ensure that the array buffer hasn't been detached. That might lead t

## Attachments

- [join_image.html](attachments/join_image.html) (text/plain, 1.4 KB)
- [join.log](attachments/join.log) (text/plain, 1.0 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093588)*
