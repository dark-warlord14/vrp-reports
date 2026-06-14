# Security: use-after-poison in blink::InspectorAccessibilityAgent::RefreshFrontendNodes 

| Field | Value |
|-------|-------|
| **Issue ID** | [40058326](https://issues.chromium.org/issues/40058326) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Platform>DevTools>Accessibility |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | jo...@chromium.org |
| **Created** | 2021-12-23 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**   
  
I think this vulnerability can be triggered in a simpler way, but I haven't found it yet.   
  
  
=================================================================  
==12428==ERROR: AddressSanitizer: use-after-poison on address 0x7e9700534380 at pc 0x7fffc5246bad

## Attachments

- [repro.mp4](attachments/repro.mp4) (video/mp4, 25.8 MB)
- [ddemo.mp4](attachments/ddemo.mp4) (video/mp4, 12.6 MB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058326)*
