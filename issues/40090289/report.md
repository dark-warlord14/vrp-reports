# Security: DevTools protocol clients (e.g. extensions) can read arbitrary local files via DOM.setFileInputFiles

| Field | Value |
|-------|-------|
| **Issue ID** | [40090289](https://issues.chromium.org/issues/40090289) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools, Platform>Extensions>API |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | dg...@chromium.org |
| **Created** | 2018-01-24 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**   
DevTools protocol v1.3 offers the DOM.setFileInputFiles method (implemented by content::protocol::DOMHandler::SetFileInputFiles [1]), to allow clients to assign a file to an <input type=file>. The file is given as a string, so DevTools API clients (e.g. extensions and re

## Attachments

- [debugger-setFileInputFiles.zip](attachments/debugger-setFileInputFiles.zip) (application/octet-stream, 1.2 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090289)*
