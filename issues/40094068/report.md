# pdfium XFA CXFA_FFDocView::RunValidate Use After Free

| Field | Value |
|-------|-------|
| **Issue ID** | [40094068](https://issues.chromium.org/issues/40094068) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ho...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2019-02-18 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15

Steps to reproduce the problem:
1. pdfium with XFA enabled, ASAN enabled
2. ./pdfium_test e8d01dca9386e3b17078653bdd0c952e.pdf
3. 

What is the expected behavior

## Attachments

- [e8d01dca9386e3b17078653bdd0c952e.pdf](attachments/e8d01dca9386e3b17078653bdd0c952e.pdf) (application/pdf, 4.1 KB)
- [asan_e8d01dca9386e3b17078653bdd0c952e](attachments/asan_e8d01dca9386e3b17078653bdd0c952e) (text/plain, 18.3 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094068)*
