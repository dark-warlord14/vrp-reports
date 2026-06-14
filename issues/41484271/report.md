# Security: Use After Free in sqlite

| Field | Value |
|-------|-------|
| **Issue ID** | [41484271](https://issues.chromium.org/issues/41484271) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage>WebSQL, Internals>Storage>SQLite |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | gc...@gmail.com |
| **Assignee** | es...@chromium.org |
| **Created** | 2023-12-14 |
| **Bounty** | $1,000.00 |

## Description

VULNERABILITY DETAILS

## Introduction

Note: This vulnerability exists in the latest version of Chrome Stable and in the mainline Chrome.

- Versions affected in Chrome: Chrome-Stable-116 to the latest
- Time introduced in Chromium: https://chromium-review.googlesource.com/c/chromium/src/+/4545677

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 47.8 KB)
- [poc.sql](attachments/poc.sql) (text/plain, 207 B)
- [poc.html](attachments/poc.html) (text/plain, 1.3 KB)
- [poc.html](attachments/poc_53182198.html) (text/plain, 1.4 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41484271)*
