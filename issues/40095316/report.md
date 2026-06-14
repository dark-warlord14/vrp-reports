# UAF in chrome!content::Portal::Activate

| Field | Value |
|-------|-------|
| **Issue ID** | [40095316](https://issues.chromium.org/issues/40095316) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>Portals |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | pa...@blackowlsec.com |
| **Assignee** | lf...@chromium.org |
| **Created** | 2019-06-06 |
| **Bounty** | $8,000.00 |

## Description

**VULNERABILITY DETAILS**   
Use-After-Free in chrome!content::Portal::Activate+0xc1 [C:\b\c\b\win64_clang\src\content\browser\portal\portal.cc @ 195  
  
==58576==ERROR: AddressSanitizer: heap-use-after-free on address 0x119bdfe95280 at pc 0x7ffd21aea585 bp 0x00593c9fe4a0 sp 0x00593c9fe4e8  
READ o

## Attachments

- [cm_portal3_asan.txt](attachments/cm_portal3_asan.txt) (text/plain, 18.0 KB)
- [cm_portal3_windbg.txt](attachments/cm_portal3_windbg.txt) (text/plain, 6.6 KB)
- [cm_portal3.html](attachments/cm_portal3.html) (text/plain, 63.9 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095316)*
