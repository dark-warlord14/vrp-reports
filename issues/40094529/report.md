# v8 crash on map-check

| Field | Value |
|-------|-------|
| **Issue ID** | [40094529](https://issues.chromium.org/issues/40094529) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Compiler |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | yn...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2019-04-07 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36

Steps to reproduce the problem:
1. 
2. 
3. 

What is the expected behavior?

What went wrong?
poc:

function v0(v2, v3){
    Object.defineProperty(v2, 'length',

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094529)*
