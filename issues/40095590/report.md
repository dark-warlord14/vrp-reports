# OOB in SwiftShader textureSize

| Field | Value |
|-------|-------|
| **Issue ID** | [40095590](https://issues.chromium.org/issues/40095590) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>SwiftShader |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cd...@gmail.com |
| **Assignee** | ni...@google.com |
| **Created** | 2019-07-03 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36

Steps to reproduce the problem:
1. Put the js file and poc.html,crash.html into same dir and setup a webserver. 
2. Run ./chrome --disable-gpu crash.html

What is the expected

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 2.1 KB)
- [utility.js](attachments/utility.js) (text/plain, 2.0 KB)
- [webgl-utils.js](attachments/webgl-utils.js) (text/plain, 10.0 KB)
- [crash.html](attachments/crash.html) (text/plain, 1.1 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095590)*
