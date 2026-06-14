# Security: heap-use-after-free in ui::AXTree::NotifyNodeWillBeReparentedOrDeleted 

| Field | Value |
|-------|-------|
| **Issue ID** | [40058147](https://issues.chromium.org/issues/40058147) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P2 |
| **Component** | Internals>Accessibility |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | dl...@gmail.com |
| **Created** | 2021-12-07 |
| **Bounty** | $7,000.00 |

## Description

This vulnerability is similar to the triggering method of https://crbug.com/chromium/1277327, but it has a fundamentally different cause. It seems to be a new UAF, wait for me to have time to analyze it in detail.   
  
=================================================================  
==13220==ERR

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058147)*
