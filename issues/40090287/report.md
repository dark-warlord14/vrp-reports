# Security: Self-update service worker to stay alive

| Field | Value |
|-------|-------|
| **Issue ID** | [40090287](https://issues.chromium.org/issues/40090287) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>ServiceWorker |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ya...@gmail.com |
| **Assignee** | ya...@gmail.com |
| **Created** | 2018-01-24 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**   
Service workers can self update to keep at least one version running.  
This is reproducible at least in Chrome and Firefox (Spec bug?).  
  
**REPRODUCTION CASE**   
1. Create index.html to load SW  
     <!DOCTYPE html>  
     <script>  
       navigator.serviceWorker.

## Attachments

- [sw.go](attachments/sw.go) (text/plain, 1.0 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090287)*
