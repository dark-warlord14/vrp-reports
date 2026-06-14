# Security: Skia heap use-after-freed in SkPath::addPath

| Field | Value |
|-------|-------|
| **Issue ID** | [40092420](https://issues.chromium.org/issues/40092420) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2018-09-10 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**   
  
There is a heap use-after-free in Skia at SkPath::addPath()  
https://cs.chromium.org/chromium/src/third_party/skia/src/core/SkPath.cpp?dr&q=addpath&g=0&l=1614  
  
Root cause:  
"RawIter iter(path);" variable at line  
https://cs.chromium.org/chromium/src/third

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092420)*
