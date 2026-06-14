# Heap-buffer-overflow in SkAlphaRuns::add

| Field | Value |
|-------|-------|
| **Issue ID** | [40063405](https://issues.chromium.org/issues/40063405) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals, Internals>Skia |
| **Reporter** | at...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2012-08-11 |
| **Bounty** | $500.00 |

## Description

All files needed for reproducing are as attachments.

This issue can be hard to reproduce, I created the runner.html to help in reproducing. Place all the attached files in a same folder and open the runner.html with Chrome. I had a success rate of about one of ten tries to reproduce the issue. (I

## Attachments

- [runner.html](attachments/runner.html) (text/html; charset=us-ascii, 547 B)
- [chrome-heap-buffer-overflow-SkAlphaRunsadd-c5610.html](attachments/chrome-heap-buffer-overflow-SkAlphaRunsadd-c5610.html) (text/html; charset=utf-8, 22.4 KB)
- [chrome-heap-buffer-overflow-SkAlphaRunsadd-c569.html](attachments/chrome-heap-buffer-overflow-SkAlphaRunsadd-c569.html) (text/html; charset=utf-8, 25.0 KB)
- [chrome-heap-buffer-overflow-SkAlphaRunsadd-c569.html](attachments/chrome-heap-buffer-overflow-SkAlphaRunsadd-c569_53180796.html) (text/html; charset=utf-8, 13.1 KB)
- [chrome-heap-buffer-overflow-SkAlphaRunsadd-c5610.html](attachments/chrome-heap-buffer-overflow-SkAlphaRunsadd-c5610_53180797.html) (text/html; charset=us-ascii, 1.5 KB)
- [chrome-heap-buffer-overflow-SkAlphaRunsadd-c5610.html](attachments/chrome-heap-buffer-overflow-SkAlphaRunsadd-c5610_53180804.html) (text/html; charset=us-ascii, 1.5 KB)
- [repro.zip](attachments/repro.zip) (application/zip; charset=binary, 6.7 KB)
- [Repro-8-from-10.zip](attachments/Repro-8-from-10.zip) (application/zip; charset=binary, 6.5 KB)
- [Repro-10-from-10.zip](attachments/Repro-10-from-10.zip) (application/zip; charset=binary, 1.6 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063405)*
