# Security: Extensions can silently debug (run code) in ANY tab and escape the sandbox

| Field | Value |
|-------|-------|
| **Issue ID** | [40081378](https://issues.chromium.org/issues/40081378) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions, Platform>Extensions>API |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | ro...@robwu.nl |
| **Created** | 2015-02-09 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**   
**Please provide a brief explanation of the security issue.**   
  
The chrome.debugger extension API can attach to targets at any origin, including URLs such as file://, chrome://, chrome-extension:// and the Chrome Web store. Attaching to privileged targets is usually

## Attachments

- [manifest.json](attachments/manifest.json) (application/json, 220 B)
- [background.js](attachments/background.js) (text/javascript, 4.1 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081378)*
