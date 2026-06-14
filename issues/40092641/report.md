# Security: pageCapture permission allows access to arbitrary local files and chrome:// pages

| Field | Value |
|-------|-------|
| **Issue ID** | [40092641](https://issues.chromium.org/issues/40092641) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions>API |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | bd...@chromium.org |
| **Created** | 2018-10-08 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**   
The pageCapture permission allows an extension to call the chrome.pageCapture.saveAsMHTML method. This method will save the page data for any tab, regardless of whether it's a standard web page, chrome:// page or local file. This is true even if "Allow access to file URL

## Attachments

- [pagecapture_poc.zip](attachments/pagecapture_poc.zip) (application/octet-stream, 1.0 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092641)*
