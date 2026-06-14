# Security: Calling console utility functions causes data to be shared between contexts

| Field | Value |
|-------|-------|
| **Issue ID** | [40095777](https://issues.chromium.org/issues/40095777) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | sz...@chromium.org |
| **Created** | 2019-07-20 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**   
Using the debug/monitor console utility functions, a user can break into the debugger when a particular function is called, or monitor when a function is called.  
  
When either of these utility functions is invoked, the process of setting up the debug breakpoint causes

## Attachments

- [content_script.js](attachments/content_script.js) (text/plain, 0 B)
- [index.html](attachments/index.html) (text/plain, 265 B)
- [manifest.json](attachments/manifest.json) (text/plain, 275 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095777)*
