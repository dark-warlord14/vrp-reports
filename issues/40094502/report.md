# pdfium (XFA): wrong object type / uaf in SyncContainer

| Field | Value |
|-------|-------|
| **Issue ID** | [40094502](https://issues.chromium.org/issues/40094502) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | pd...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-04-04 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.124 Safari/537.36

Steps to reproduce the problem:
This is related to https://crbug.com/chromium/943522.

The following (simplified) snippet is invalid because overflow sets the trailer attribute

## Attachments

- [chromium-949413.pdf](attachments/chromium-949413.pdf) (application/pdf, 603 B)
- [patch-949413](attachments/patch-949413) (text/plain, 2.0 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094502)*
