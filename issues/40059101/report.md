# getThumbnail() CHECK leaks number of available PDF pages

| Field | Value |
|-------|-------|
| **Issue ID** | [40059101](https://issues.chromium.org/issues/40059101) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | nd...@protonmail.com |
| **Assignee** | dh...@chromium.org |
| **Created** | 2022-03-15 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36

Steps to reproduce the problem:
let w = open('https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf');
setTimeout(_ => w[0].postMessage({type: 'getThum

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059101)*
