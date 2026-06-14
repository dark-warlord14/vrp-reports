# UAF in indexeddb  IndexedDBDatabase::RequestComplete

| Field | Value |
|-------|-------|
| **Issue ID** | [40094312](https://issues.chromium.org/issues/40094312) |
| **Status** | New |
| **Severity** | S4-Minimal |
| **Priority** | P0 |
| **Component** | Blink>Storage>IndexedDB |
| **Platforms** | Android, Linux, Mac, ChromeOS |
| **Reporter** | cd...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2019-03-17 |
| **Bounty** | $10,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36

Steps to reproduce the problem:
1. download and unzip the release asan chromium :asan-linux-release-639779 
2. Set up a webserver and put poc.html 
3. Run ./chrome  crash.html

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094312)*
