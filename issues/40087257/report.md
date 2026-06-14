# Security: Print Preview allows spoofing on other tab

| Field | Value |
|-------|-------|
| **Issue ID** | [40087257](https://issues.chromium.org/issues/40087257) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>PrintPreview |
| **Platforms** | Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2017-04-05 |
| **Bounty** | $500.00 |

## Description

Chrome Version: 57.0.2987.133 stable   
Operating System: Windows 7  
  
**REPRODUCTION CASE**   
Print preview can appears over the different origin and that's produces "spoofing", the address bar shows google.com but the print preview shows the content that used by document.write() in the PoC.

## Attachments

- [screenshot.png](attachments/screenshot.png) (image/png, 98.9 KB)
- [PoC.html](attachments/PoC.html) (text/plain, 282 B)
- [print_preview_with_source.png](attachments/print_preview_with_source.png) (image/png, 20.4 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087257)*
