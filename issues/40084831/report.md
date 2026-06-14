# Use-after-poison in content::WebMessagePortChannelImpl::OnMessage

| Field | Value |
|-------|-------|
| **Issue ID** | [40084831](https://issues.chromium.org/issues/40084831) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Core |
| **Platforms** | Mac |
| **Reporter** | at...@gmail.com |
| **Assignee** | tz...@chromium.org |
| **Created** | 2016-07-12 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5079226818756608

Fuzzer: attekett_dom_fuzzer
Job Type: mac_asan_chrome
Platform Id: mac

Crash Type: Use-after-poison READ 8
Crash Address: 0x7ee7424e1d68
Crash State:
  content::WebMessagePortChannelImpl::OnMessage
  bool IPC::MessageT

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084831)*
