# Cookies with SameSite=Strict; are sent for link rel="prerender" when requested from 3rd party site

| Field | Value |
|-------|-------|
| **Issue ID** | [40090228](https://issues.chromium.org/issues/40090228) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Network>Cookies |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | is...@gmail.com |
| **Assignee** | ry...@chromium.org |
| **Created** | 2018-01-18 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36

Steps to reproduce the problem:
1. Start a webserver (say localhost:8080) issuing a SameSite=Strict; cookie for a domain. (See server code, in which case you brows

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090228)*
