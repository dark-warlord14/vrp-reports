# Oilpan reintroduced inline meta-data

| Field | Value |
|-------|-------|
| **Issue ID** | [40084983](https://issues.chromium.org/issues/40084983) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>GarbageCollection |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | pa...@chromium.org |
| **Created** | 2016-08-01 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2813.0 Safari/537.36

Steps to reproduce the problem:
The Oilpan GC heap has replaced PartitionAlloc as the backing store for Blink objects that inherit from Node. While this design maint

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084983)*
