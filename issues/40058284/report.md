# Security: heap-use-after-free in TabStripLayoutHelper::SlotIsCollapsedTab

| Field | Value |
|-------|-------|
| **Issue ID** | [40058284](https://issues.chromium.org/issues/40058284) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P1 |
| **Component** | UI>Browser>TopChrome>TabStrip>TabGroups |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | dp...@chromium.org |
| **Created** | 2021-12-18 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**   
Dragging a tab group while a new tab in the tab group is opened results in the group being opened across multiple windows, which causes unexpected behaviour.  
  
**VERSION**   
Chrome Version: 99.0.4774.0  
Operating System: Windows 10  
  
**REPRODUCTION CASE**   
1. L

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 91 B)
- [uaf.mp4](attachments/uaf.mp4) (video/mp4, 764.1 KB)
- [drag-detach.mp4](attachments/drag-detach.mp4) (video/mp4, 1.7 MB)
- [detach-drag.mp4](attachments/detach-drag.mp4) (video/mp4, 1.2 MB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058284)*
