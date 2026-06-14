# pdfium (XFA): oob read+write in CFDE_TextOut

| Field | Value |
|-------|-------|
| **Issue ID** | [40094660](https://issues.chromium.org/issues/40094660) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | pd...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2019-04-17 |
| **Bounty** | $7,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.124 Safari/537.36  
  
Steps to reproduce the problem:  
There are two separate and independent of each other bugs here, which however seem to only reproduce in tandem. The initial ASAN report seems re

## Attachments

- [chromium-953881.pdf](attachments/chromium-953881.pdf) (application/pdf, 689 B)
- [chromium-953881.ttf](attachments/chromium-953881.ttf) (application/octet-stream, 7.1 KB)
- [chromium-953881-with-font.pdf](attachments/chromium-953881-with-font.pdf) (application/pdf, 10.3 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094660)*
