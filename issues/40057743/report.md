# Security: UAF in SharingHub

| Field | Value |
|-------|-------|
| **Issue ID** | [40057743](https://issues.chromium.org/issues/40057743) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | UI>Browser>Sharing |
| **Platforms** | ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | kr...@chromium.org |
| **Created** | 2021-10-28 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**   
  
I think this bug was caused by this submission: https://source.chromium.org/chromium/chromium/src/+/f50ae42daa8b4d22db68202a38afa9dc17680b06  
  
|OnSharesheetClosed| is bound[1] as a callback function |close_callback_|.   
  
When class |SharingHubBubbleController| i

## Attachments

- [asan](attachments/asan) (text/plain, 24.5 KB)
- [poc.html](attachments/poc.html) (text/plain, 123 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057743)*
