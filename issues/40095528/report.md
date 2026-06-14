# Bad-cast to net::URLRequestFtpJob from invalid vptr in net::URLRequestFtpJob::OnStartCompleted

| Field | Value |
|-------|-------|
| **Issue ID** | [40095528](https://issues.chromium.org/issues/40095528) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Network |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | te...@google.com |
| **Created** | 2019-06-28 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=5155387255160832

Fuzzer: domino
Job Type: linux_ubsan_vptr_chrome
Platform Id: linux

Crash Type: Bad-cast
Crash Address: 0x2c4782449c00
Crash State:
  Bad-cast to net::URLRequestFtpJob from invalid vptr
  net::URLRequestFtpJob::OnStartCompleted

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095528)*
