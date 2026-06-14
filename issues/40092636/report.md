# Security: crosvm: integer overflow in PluginVcpu::handle_request

| Field | Value |
|-------|-------|
| **Issue ID** | [40092636](https://issues.chromium.org/issues/40092636) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P4 |
| **Component** | OS>Systems |
| **Platforms** | ChromeOS |
| **Reporter** | al...@gmail.com |
| **Assignee** | za...@chromium.org |
| **Created** | 2018-10-06 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**   
  
https://chromium.googlesource.com/chromiumos/platform/crosvm/+/master/src/plugin/vcpu.rs#468  
  
the addition and multiplication here can overflow. when they do, |vec| will be smaller than was expected.  
  
However, this memory will then, unsafely be treated as if t

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092636)*
