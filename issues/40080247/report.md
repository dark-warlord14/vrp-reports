# Security: v8: WebKitPoint() memory corruption

| Field | Value |
|-------|-------|
| **Issue ID** | [40080247](https://issues.chromium.org/issues/40080247) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>JavaScript |
| **Reporter** | sk...@chromium.org |
| **Assignee** | mo...@google.com |
| **Created** | 2010-04-07 |
| **Bounty** | $500.00 |

## Description

By calling window.WebKitPoint(), we are causing some kind of memory 
corruption in v8. The following two html files will trigger the issue by 
calling the method in an IFRAME, while the main page refreshes the IFRAME 
from time to time to cause GarbageCollection, which exposes the memory 
corrup

## Attachments

- [repro5.2.html](attachments/repro5.2.html) (text/plain; charset=us-ascii, 95 B)
- [repro5.1.html](attachments/repro5.1.html) (text/plain; charset=us-ascii, 184 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080247)*
