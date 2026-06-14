# Security: Select Options Can Escape Across Tabs

| Field | Value |
|-------|-------|
| **Issue ID** | [41494315](https://issues.chromium.org/issues/41494315) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Forms>Select, Blink>HTML, Internals>Sandbox>SiteIsolation |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | fa...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2024-01-24 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**   
Using the select option and showPicker(), an attacker could overlay content on other tabs from a malicious site.  
  
Below is a proof-of-concept page; when a victim clicks on a malicious site, the select options are displayed over other tabs opened by the victim.  
  
*

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 904 B)
- [demo.mp4](attachments/demo.mp4) (video/mp4, 1.2 MB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41494315)*
