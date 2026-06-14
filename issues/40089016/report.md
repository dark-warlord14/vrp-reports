# Security: METHOD_LOCALTIME browser->renderer infoleak

| Field | Value |
|-------|-------|
| **Issue ID** | [40089016](https://issues.chromium.org/issues/40089016) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Sandbox |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | vi...@microsoft.com |
| **Assignee** | pa...@chromium.org |
| **Created** | 2017-09-15 |
| **Bounty** | $3,337.00 |

## Description

VULNERABILITY DETAILS

In the IPC method METHOD_LOCALTIME there is a full pointer infoleak when Chromium is built against glibc on Linux.

The bug is in the function HandleLocaltime(...).
It sends an entire “struct tm” from the browser process to renderer:

  const struct tm* expanded_time =

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089016)*
