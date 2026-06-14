# Security: SEE_MASK_FLAG_NO_UI behavior changes in Windows 10, allowing SmartScreen bypass

| Field | Value |
|-------|-------|
| **Issue ID** | [40090721](https://issues.chromium.org/issues/40090721) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Windows |
| **Reporter** | jk...@cornell.edu |
| **Assignee** | as...@chromium.org |
| **Created** | 2018-03-07 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**   
In the next Windows Release (Redstone 4), Windows Defender SmartScreen will honor the SEE_MASK_FLAG_NO_UI flag. This flag is passed through shellexecute when a user runs an executable, or other supported file, through the chrome download manager. Edge/Firefox/Windows Exp

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090721)*
