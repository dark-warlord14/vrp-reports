# Security: ui::AXPlatformNodeWin Use-After-Free issue

| Field | Value |
|-------|-------|
| **Issue ID** | [41491428](https://issues.chromium.org/issues/41491428) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | UI>Accessibility, UI>Browser>Panels |
| **Platforms** | Windows |
| **Reporter** | sw...@gmail.com |
| **Assignee** | ks...@microsoft.com |
| **Created** | 2024-01-15 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**   
  
## Root Case  
  
### Alloc   
  
When using customize chrome feature, the 'side panel' will be opened. The `SetCustomizeChromeSidePanelVisible` function will be called here:  
```  
void CustomizeChromeSidePanelController::SetCustomizeChromeSidePanelVisible(  
    bo

## Attachments

- [repro-1-15.mp4](attachments/repro-1-15.mp4) (video/mp4, 4.1 MB)
- [UAF-2.asan](attachments/UAF-2.asan) (text/plain, 15.5 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41491428)*
