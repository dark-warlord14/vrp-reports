# Security: Use after Free in content::AccessibilityEventRecorderWin::AccessibleObjectFromWindowWrapper 

| Field | Value |
|-------|-------|
| **Issue ID** | [40057908](https://issues.chromium.org/issues/40057908) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Accessibility |
| **Platforms** | Windows |
| **Reporter** | ha...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2021-11-14 |
| **Bounty** | $1,000.00 |

## Description

This vulnerability is a new point, and I accidentally triggered this crash, but after I analyzed it, it is indeed a real UAF vulnerability.The asan log of this UAF is not complete, but I still analyzed the specific reasons.  
  
  
[0]https://source.chromium.org/chromium/chromium/src/+/main:content/

## Attachments

- [repro.mp4](attachments/repro.mp4) (video/mp4, 6.2 MB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057908)*
