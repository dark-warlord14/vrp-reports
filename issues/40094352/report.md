# Security: CORB not enforced for WebSocket requests 

| Field | Value |
|-------|-------|
| **Issue ID** | [40094352](https://issues.chromium.org/issues/40094352) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Network>WebSockets, Internals>Sandbox>SiteIsolation, Platform>DevTools>Network, Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@piosek.pl |
| **Assignee** | yo...@chromium.org |
| **Created** | 2019-03-21 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**   
CORB policy is not enforced for WebSocket requests. It is possible to create new WebSocket object with connection URL which refers to resource for which Content-Type header is set e.g. to text/html. In such situation CORB policy violation doesn't occurs.   
  
**VERSION*

## Attachments

- [CORB_WebSocket.mp4](attachments/CORB_WebSocket.mp4) (video/mp4, 861.9 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094352)*
