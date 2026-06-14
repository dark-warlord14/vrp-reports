# Site Isolation breaking bug in filesystem

| Field | Value |
|-------|-------|
| **Issue ID** | [40095069](https://issues.chromium.org/issues/40095069) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Storage>FileSystem, Internals>Sandbox>SiteIsolation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | wy...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2019-05-17 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36

Steps to reproduce the problem:
I find that the javascript code under domain A can access the filesystem data under domain B, and the only one check exists in the render

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095069)*
