# Leaking size of cross-origin resource by using Range Requests and Service Workers

| Field | Value |
|-------|-------|
| **Issue ID** | [40095912](https://issues.chromium.org/issues/40095912) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>PerformanceAPIs>ResourceTiming, Blink>ServiceWorker, Internals>Media>Network |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | yo...@chromium.org |
| **Created** | 2019-08-05 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**   
When a cross-origin resource is used in an audio/video tag, a request containing the Range header asking for bytes=0- is issued.  
If the request is intercepted using a Service Worker and we respond with an arbitrary body, e.g:  
e.respondWith(new Response("aaa", {status

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095912)*
