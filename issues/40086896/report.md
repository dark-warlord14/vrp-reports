# Security: Chrome extension is disabled by crafted chrome-extension:// URL

| Field | Value |
|-------|-------|
| **Issue ID** | [40086896](https://issues.chromium.org/issues/40086896) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions |
| **Platforms** | Windows |
| **Reporter** | ma...@gmail.com |
| **Assignee** | la...@chromium.org |
| **Created** | 2017-02-25 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**   
If you put a `.` to the end of `chrome-extension://` resource's pathname, the extension is disabled.  
For example: `chrome-extension://[extensions]/background.html.`  
  
Navigting from the web origin to chrome-extension:// URL is restricted but if the target extension'

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086896)*
