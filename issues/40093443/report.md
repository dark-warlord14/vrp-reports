# pdfium: signed-integer-overflow in AdjustGlyphSpace / CFX_DIBBase::GetOverlapRect

| Field | Value |
|-------|-------|
| **Issue ID** | [40093443](https://issues.chromium.org/issues/40093443) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux |
| **Reporter** | pd...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2018-12-13 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.71 Safari/537.36

Steps to reproduce the problem:
I'm tentatively filing this as a security bug, as the code path doesn't seem to be used in Chrome easily.

https://cs.chromium.org/chromium/src/th

## Attachments

- [chromium-914983.pdf](attachments/chromium-914983.pdf) (application/pdf, 417 B)
- [chromium-914983-2.pdf](attachments/chromium-914983-2.pdf) (application/pdf, 412 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093443)*
