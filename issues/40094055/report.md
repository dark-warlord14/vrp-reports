# pdfium XFA CXFA_FFDocView::RunSubformIndexChange Use After Free

| Field | Value |
|-------|-------|
| **Issue ID** | [40094055](https://issues.chromium.org/issues/40094055) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ho...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2019-02-16 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15

Steps to reproduce the problem:
1. pdfium with XFA build , ASAN enable
2. ./pdfium_test 5db68c09ecaba144679862bb220ba4ae.pdf
3. 

What is the expected behavior?

## Attachments

- [5db68c09ecaba144679862bb220ba4ae.pdf](attachments/5db68c09ecaba144679862bb220ba4ae.pdf) (application/pdf, 3.1 KB)
- [asan_5db68c09ecaba144679862bb220ba4ae](attachments/asan_5db68c09ecaba144679862bb220ba4ae) (text/plain, 18.8 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094055)*
