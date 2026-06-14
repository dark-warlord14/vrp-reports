# Site Isolation: Attacker-controlled data URLs end up in wrong process after tab restore

| Field | Value |
|-------|-------|
| **Issue ID** | [40091919](https://issues.chromium.org/issues/40091919) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Sandbox>SiteIsolation |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | s....@gmail.com |
| **Assignee** | cr...@chromium.org |
| **Created** | 2018-07-12 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**   
When cross-site document redirects to Data URL inside iframe, it's still being isolated by Site Isolation. But when same page is loaded from local cache (I will investigate if there is more easy way to exploit this), Data URL iframe is now committed to same process inste

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091919)*
