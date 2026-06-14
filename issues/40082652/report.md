# Security: Overflow in VertexBufferInterface::reserveVertexSpace causes memory-safety bug

| Field | Value |
|-------|-------|
| **Issue ID** | [40082652](https://issues.chromium.org/issues/40082652) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Reporter** | [Deleted User] |
| **Assignee** | jm...@chromium.org |
| **Created** | 2015-08-09 |
| **Bounty** | $5,000.00 |

## Description

[I reported the following bug to Mozilla (for its manifestations in Firefox, Thunderbird, etc.) at https://bugzilla.mozilla.org/show_bug.cgi?id=1190526 . Since the bug is in Angle, a Google library, I am also reporting it here. Version and reproduction information pertain to Firefox. I do not know w

## Attachments

- [glMatrix-0.9.5.min.js](attachments/glMatrix-0.9.5.min.js) (text/javascript, 18.3 KB)
- [poc.js](attachments/poc.js) (text/javascript, 8.3 KB)
- [poc.htm](attachments/poc.htm) (text/html, 1.4 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082652)*
