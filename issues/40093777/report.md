# pdfium (XFA): wrong object type in CFXJSE_FormCalcContext::ParseResolveResult

| Field | Value |
|-------|-------|
| **Issue ID** | [40093777](https://issues.chromium.org/issues/40093777) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | pd...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-01-17 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.71 Safari/537.36

Steps to reproduce the problem:
You can reproduce with pdfium_test by setting is_ubsan_security or is_ubsan_vptr.

fxjs/xfa/cjx_node.cpp:460:7: runtime error: member call on addr

## Attachments

- [chromium-922864.pdf](attachments/chromium-922864.pdf) (application/pdf, 418 B)
- [chromium-922864-2.pdf](attachments/chromium-922864-2.pdf) (application/pdf, 421 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093777)*
