# Security: mesa stack scribbling thingamadoo

| Field | Value |
|-------|-------|
| **Issue ID** | [40063240](https://issues.chromium.org/issues/40063240) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P0 |
| **Component** | Blink>WebGL, Internals, Internals>GPU |
| **Platforms** | ChromeOS |
| **Reporter** | mi...@gmail.com |
| **Assignee** | jo...@chromium.org |
| **Created** | 2012-08-10 |
| **Bounty** | $3,133.00 |

## Description

**VULNERABILITY DETAILS**   
https://bugzilla.mozilla.org/show_bug.cgi?id=777028  
  
  
**VERSION**   
Chrome Version: dev  
Operating System: linux64bit  
  
**REPRODUCTION CASE**   
<html>  
  <head>  
    <script id="vshader" type="x-shader/x-vertex">  
      void main()  
      {

## Attachments

- [chromium1.html](attachments/chromium1.html) (text/html; charset=us-ascii, 1.1 KB)
- [chromium1.txt](attachments/chromium1.txt) (text/plain; charset=us-ascii, 1.1 KB)
- [ff1.html](attachments/ff1.html) (text/html; charset=us-ascii, 1.1 KB)
- [fix-security](attachments/fix-security) (text/x-c++; charset=us-ascii, 4.8 KB)
- [8.1-array-overflow.patch](attachments/8.1-array-overflow.patch) (text/x-diff; charset=us-ascii, 486 B)
- [wtfgl.html](attachments/wtfgl.html) (text/html; charset=us-ascii, 1.2 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063240)*
