# Security: use-after-poison in mojo::SimpleWatcher::OnHandleReady

| Field | Value |
|-------|-------|
| **Issue ID** | [40093088](https://issues.chromium.org/issues/40093088) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Core, Internals>Mojo |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cl...@gmail.com |
| **Assignee** | wa...@chromium.org |
| **Created** | 2018-11-16 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**   
The following testcase crashes the latest ASAN build of content_shell. It might require a few reloads.  
  
**VERSION**   
Chrome Version: asan-linux-release-608443  
Operating System: Linux 64bit  
  
**REPRODUCTION CASE**   
<script>  
function start() {  
        o14=

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093088)*
