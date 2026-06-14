# Security: Malicious Extension can ignore SOP, with only `downloads` permission.

| Field | Value |
|-------|-------|
| **Issue ID** | [40095773](https://issues.chromium.org/issues/40095773) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions, UI>Browser>Downloads |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | co...@kjsman.me |
| **Assignee** | rd...@chromium.org |
| **Created** | 2019-07-20 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**   
Same-Origin Policy wasn't applied at `chrome.downloads.download` API. So, malicious extension can ignore SOP, with only `downloads` permission.  
If victim clicks somewhere on the extension's malicious page, it triggered.  
  
**VERSION**   
Chrome Version: 75.0.3770.90

## Attachments

- [PoC.crx](attachments/PoC.crx) (application/octet-stream, 4.4 KB)
- [poc.js](attachments/poc.js) (text/plain, 1.5 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095773)*
