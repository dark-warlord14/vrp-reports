# Security: chrome.devtools.inspectedWindow.eval executes within privileged pages

| Field | Value |
|-------|-------|
| **Issue ID** | [40089937](https://issues.chromium.org/issues/40089937) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools>Extensions, Platform>Extensions>API |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | gr...@hotmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2017-12-17 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**   
Extensions are normally not allowed to execute javascript within privileged pages for many reasons. Though it seems like we can use "chrome.devtools.inspectedWindow.eval" to execute JS in any page we want.   
  
Given that the manifest contains permission for only "<all_

## Attachments

- [devtools-panels.zip](attachments/devtools-panels.zip) (application/octet-stream, 5.2 KB)
- [PoC.zip](attachments/PoC.zip) (application/octet-stream, 1.7 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089937)*
