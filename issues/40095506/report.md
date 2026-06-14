# Security: PDFium (XFA) Use-after-free in CXFA_FFWidget::OnSetFocus

| Field | Value |
|-------|-------|
| **Issue ID** | [40095506](https://issues.chromium.org/issues/40095506) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Linux, ChromeOS |
| **Reporter** | my...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-06-25 |
| **Bounty** | $3,000.00 |

## Description

Steps to reproduce the problem:
1. Compile the latest chromium with enabled XFA PDFium
2. Open file test.pdf with chrome
3. 

What is the expected behavior?

What went wrong?
xfa.host.setFocus() triggers use-after-free CXFA_FFExclGroup object in CXFA_FFWidget::OnSetFocus

Did this work b

## Attachments

- [test.pdf](attachments/test.pdf) (application/pdf, 226.2 KB)
- [crash_log.txt](attachments/crash_log.txt) (text/plain, 28.2 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095506)*
