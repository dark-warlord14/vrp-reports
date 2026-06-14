# Security: UAF IN BaseRenderingContext2D::ResetInternal

| Field | Value |
|-------|-------|
| **Issue ID** | [41493290](https://issues.chromium.org/issues/41493290) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Canvas |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2024-01-21 |
| **Bounty** | $4,000.00 |

## Description

##Reproduce
The issue was found by code review, and I will provide a POC later.

##RCA
Similar to the issue(1511567) I previously reported.

1. ResetInternal calls GetPaintCanvas to get the PaintCanvas object pointer c[1], which is valid at this time. 
2. Then WillDraw[2] is called, and Wil

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 7.4 KB)
- [poc.html](attachments/poc.html) (text/plain, 380 B)
- [rep.patch.diff](attachments/rep.patch.diff) (text/plain, 6.9 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41493290)*
