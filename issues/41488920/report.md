# Crash in v8::internal::SemiSpaceNewSpace::VerifyObjects

| Field | Value |
|-------|-------|
| **Issue ID** | [41488920](https://issues.chromium.org/issues/41488920) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | d8...@gmail.com |
| **Assignee** | le...@chromium.org |
| **Created** | 2024-01-05 |
| **Bounty** | $16,000.00 |

## Description

When compiling the :
```
class C3 extends C2 {
    constructor(obj) {
        try { new.target(); } catch (e) {}
        super();
        new Array(32);
            for (let v13 = 0; v13 < 2; v13++) {
                if(!v13) {
                    gc();
                } 
            }

## Attachments

- [poc_crash.js](attachments/poc_crash.js) (text/plain, 1.5 KB)
- [poc_rce.js](attachments/poc_rce.js) (text/plain, 6.5 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41488920)*
