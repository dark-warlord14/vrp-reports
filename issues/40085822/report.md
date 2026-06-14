# expose() leaks privateClass via Object[@@hasInstance]

| Field | Value |
|-------|-------|
| **Issue ID** | [40085822](https://issues.chromium.org/issues/40085822) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ja...@googlemail.com |
| **Assignee** | ro...@robwu.nl |
| **Created** | 2016-10-29 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36

Steps to reproduce the problem:
Steps:
1. ensure that there are no extensions installed that inject content scripts into google.com
2. unpack and install test-victim-extension.zi

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085822)*
