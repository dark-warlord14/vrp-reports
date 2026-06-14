# Security: Race Condition Double Free in adreno_set_param

| Field | Value |
|-------|-------|
| **Issue ID** | [40062541](https://issues.chromium.org/issues/40062541) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P4 |
| **Component** | Internals>GPU>VendorSpecific |
| **Platforms** | ChromeOS |
| **Reporter** | lm...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2023-01-07 |
| **Bounty** | $21,000.00 |

## Description

**VULNERABILITY DETAILS**   
  
ioctl$MSM_SET_PARAM will call \*msm_ioctl_set_param\* to set param. The real code logic is implemented in the \*adreno_set_param\* function. If the \*param\* is \*MSM_PARAM_COMM\*, \*ctx->comm\* will be freed[1]. There is no lock. So if \*adreno_set_param\* is called

## Attachments

- [poc.c](attachments/poc.c) (text/plain, 1.7 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062541)*
