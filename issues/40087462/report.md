# Security: Out of bound read in FindSharedFunctionInfo (V8)

| Field | Value |
|-------|-------|
| **Issue ID** | [40087462](https://issues.chromium.org/issues/40087462) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cw...@gmail.com |
| **Assignee** | jo...@chromium.org |
| **Created** | 2017-04-26 |
| **Bounty** | $3,000.00 |

## Description

**VERSION**   
Chrome Version: stable (v8 5.8.283.32)  
  
**REPRODUCTION CASE**   
  
```test.js  
this.__defineGetter__("x", (a = (function f() { return; (function() {}); })()) => { });  
x;  
```  
  
```Backtrace of debug build  
$ ../../..//v8/out/ia32.debug/d8 --allow-natives-syntax --expose-g

## Attachments

- [poc715582.html](attachments/poc715582.html) (text/plain, 1.6 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087462)*
