# Security: potential buffer overflow in zlib - CVE-2022-37434

| Field | Value |
|-------|-------|
| **Issue ID** | [40060641](https://issues.chromium.org/issues/40060641) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **CVE IDs** | CVE-2022-37434 |
| **Reporter** | ri...@sap.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2022-08-21 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**   
In zlib a potential buffer overflow was fixed recently. See: https://github.com/madler/zlib/commit/eff308af425b67093bab25f80f1ae950166bece1  
The fix introduced a null pointer deref, which was fixed as well. See: https://github.com/madler/zlib/commit/1eb7682f845ac9e9bf9a

## Attachments

- [tot_unpatched.png](attachments/tot_unpatched.png) (image/png, 441.1 KB)
- [sync_patched.png](attachments/sync_patched.png) (image/png, 504.8 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060641)*
