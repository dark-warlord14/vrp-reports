# An extension can access and modify all chrome:// pages, options, etc.

| Field | Value |
|-------|-------|
| **Issue ID** | [40091029](https://issues.chromium.org/issues/40091029) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **Reporter** | tw...@googlemail.com |
| **Assignee** | se...@chromium.org |
| **Created** | 2011-05-18 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**   
An packaged app/extension can access and modify all chrome: pages, read/write preferences, run chrome.send function,   
pass arguments directly to c++,   
without required permissions,  
without using NPAPI plugin,   
content script or chrome.tabs.executeScript  
  
**VE

## Attachments

- [Hotcleaner_Alpha_Test.crx](attachments/Hotcleaner_Alpha_Test.crx) (application/octet-stream; charset=binary, 30.0 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091029)*
