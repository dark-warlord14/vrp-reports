# Change on the credentials mode on redirect specified by the CORS algorithm should be propagated to net/

| Field | Value |
|-------|-------|
| **Issue ID** | [40085972](https://issues.chromium.org/issues/40085972) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>HTML>Modules, Blink>Loader, Blink>SecurityFeature>CORS |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | dh...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2016-11-16 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**   
Due to specification [1] import must fetch document in the anonymous mode to CORS and the credentials mode to same-origin.  
This works only if initial request referer to cross-origin, if we make request to same-origin and then make redirect to cross-origin - Chromium wi

## Attachments

- [2016-11-16-112918.png](attachments/2016-11-16-112918.png) (image/png, 153.5 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085972)*
