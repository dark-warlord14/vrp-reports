# Security: Hostname not elided securely (URL spoofing on iOS)

| Field | Value |
|-------|-------|
| **Issue ID** | [40093740](https://issues.chromium.org/issues/40093740) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Omnibox, UI>Browser>Omnibox>SecurityIndicators |
| **Platforms** | iOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | rk...@google.com |
| **Created** | 2019-01-13 |
| **Bounty** | $500.00 |

## Description

**VERSION**   
Chrome Version: 72.0.3626.51  
Operating System: iOS 12.1.2  
  
**REPRODUCTION CASE**   
1. Load the testcase   
2. Click on "Click here to go to Google.com"  
3. Click on the omnibox quickly, then you will see an alert  
4. Click on 'OK' or 'Cancel'  
5. Wait >> You will see :

## Attachments

- [9D3458ED-D984-4B21-A837-C451E24DF476.MOV](attachments/9D3458ED-D984-4B21-A837-C451E24DF476.MOV) (video/quicktime, 836.8 KB)
- [testcase.html](attachments/testcase.html) (text/plain, 676 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093740)*
