# Security: Talos Security Advisory for Google PDFium (TALOS-2018-0639)

| Field | Value |
|-------|-------|
| **Issue ID** | [40092024](https://issues.chromium.org/issues/40092024) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | [Deleted User] |
| **Assignee** | ts...@chromium.org |
| **Created** | 2018-07-25 |
| **Bounty** | $2,000.00 |

## Description

### Summary

An exploitable out-of-bounds read on the heap vulnerability exists in the JBIG2 parsing code of Google Chrome version 67.0.3396.99. A specially crafted PDF document can trigger an out-of-bounds read, which can possibly lead to an information leak that could be used as part of an explo

## Attachments

- [Google Vulnerability Report.TALOS 2018 0639.zip](attachments/Google Vulnerability Report.TALOS 2018 0639.zip) (application/octet-stream, 8.4 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092024)*
