# security: libmbim | out-of-bounds access on mbim-message.c

| Field | Value |
|-------|-------|
| **Issue ID** | [40070139](https://issues.chromium.org/issues/40070139) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | rh...@gmail.com |
| **Assignee** | st...@google.com |
| **Created** | 2023-08-21 |
| **Bounty** | $250.00 |

## Description

**Steps to reproduce the problem:**   
1. Tested on zork board Chromebook.  
  
**Problem Description:**   
Found the OOB access by libfuzzer. Tested on zork board Chromebook.  
  
Tested on main libmbim  
```  
commit 623d6bf0df63b57b2c466677140aadb705c67cc5 (HEAD, m/release-R117-15572.B, m/main, c

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40070139)*
