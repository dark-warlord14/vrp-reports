# use-after-poison in mojo::InterfaceEndpointClient::HandleValidatedMessage)

| Field | Value |
|-------|-------|
| **Issue ID** | [40092022](https://issues.chromium.org/issues/40092022) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Loader, Blink>Storage |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2018-07-25 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**   
The following testcase crashes the latest Chromium ASAN build when loaded from a HTTP server.  
  
**VERSION**   
Chrome Version: asan-linux-release-577824  
Operating System: Linux 64-bit  
  
**REPRODUCTION CASE**   
  
<script>  
function start() {  
        o178=wind

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092022)*
