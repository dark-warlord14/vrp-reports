# Security: Google V8 Array.prototype Memory Corruption Vulnerability (TALOS-2019-0791)

| Field | Value |
|-------|-------|
| **Issue ID** | [40094304](https://issues.chromium.org/issues/40094304) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>GarbageCollection |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | [Deleted User] |
| **Assignee** | ml...@chromium.org |
| **Created** | 2019-03-15 |
| **Bounty** | $2,000.00 |

## Description

### Summary

A specific JavaScript code can trigger a memory corruption in V8 7.3.492.17 which could potentially be abused for remote code execution. In order to trigger this vulnerability in the context of a browser, such as Google Chrome, the victim would need to visit a malicious web page.

## Attachments

- [Google vulnerability Report_TALOS-2019-0791.zip.gpg](attachments/Google vulnerability Report_TALOS-2019-0791.zip.gpg) (application/octet-stream, 8.4 KB)
- [Google vulnerability Report_TALOS-2019-0791.zip](attachments/Google vulnerability Report_TALOS-2019-0791.zip) (application/octet-stream, 8.8 KB)
- [google_v8_array_prototype_memory_corruption_poc.js](attachments/google_v8_array_prototype_memory_corruption_poc.js) (text/plain, 1.7 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094304)*
