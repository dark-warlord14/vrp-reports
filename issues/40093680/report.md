# Security: http authentication spoof on chrome iOS (repro issue 884179)

| Field | Value |
|-------|-------|
| **Issue ID** | [40093680](https://issues.chromium.org/issues/40093680) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Mobile>iOSWeb>Security |
| **Platforms** | iOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | eu...@chromium.org |
| **Created** | 2019-01-09 |
| **Bounty** | $500.00 |

## Description

**VERSION**   
Chrome Version: 72.0.3626.28 beta   
Operating System: iOS 12.1.2   
  
**REPRODUCTION CASE**   
  
1. Lunch the PoC.html   
2. Click on the red button, then click on the green button quickly.  
  
The authentication dialog should be gone after navigation (see https://crbug.com/chromi

## Attachments

- [screenshot.jpeg](attachments/screenshot.jpeg) (image/jpeg, 78.4 KB)
- [poc.html](attachments/poc.html) (text/plain, 1.2 KB)
- [AA29DEDB-D2E2-47E9-8335-2C78DAC5AB65.MOV](attachments/AA29DEDB-D2E2-47E9-8335-2C78DAC5AB65.MOV) (video/quicktime, 1.4 MB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093680)*
