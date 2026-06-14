# Security: heap-use-after-free in blink::AudioNodeOutput::Pull

| Field | Value |
|-------|-------|
| **Issue ID** | [40092590](https://issues.chromium.org/issues/40092590) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebAudio |
| **Platforms** | Linux |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ho...@chromium.org |
| **Created** | 2018-10-02 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**   
The following testcase crashes the latest ASAN build of Chrome. It might take a few minutes to reproduce. Run with --js-flags=--expose-gc  
  
**VERSION**   
Chrome Version: asan-linux-release-595737  
Operating System: Linux 64bit  
  
**REPRODUCTION CASE**   
<script>

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092590)*
