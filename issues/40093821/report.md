# Security: heap-use-after-free in blink::CSSToLengthConversionData::FontSizes::FontSizes

| Field | Value |
|-------|-------|
| **Issue ID** | [40093821](https://issues.chromium.org/issues/40093821) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>CSS |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cl...@gmail.com |
| **Assignee** | fs...@opera.com |
| **Created** | 2019-01-23 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**   
The following testcase crashes the latest ASAN build of content_shell when loaded from an HTTP server. It requires the attached img.svg in the same directory. The testcase might require a few attempts to trigger the issue.  
  
**VERSION**   
Chrome Version: asan-linux-r

## Attachments

- [img.svg](attachments/img.svg) (image/svg+xml, 2.8 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093821)*
