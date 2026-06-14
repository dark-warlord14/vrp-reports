# Security: Race Condition UAF in radeon_gem_set_domain_ioctl

| Field | Value |
|-------|-------|
| **Issue ID** | [40063579](https://issues.chromium.org/issues/40063579) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>GPU>VendorSpecific |
| **Platforms** | ChromeOS |
| **Reporter** | lm...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2023-03-14 |
| **Bounty** | $250.00 |

## Description

**VULNERABILITY DETAILS**   
  
The root cause of this issue is similar to https://crbug.com/chromium/1400113, race condition UAF.  
  
ioctl$RADEON_GEM_SET_DOMAIN will call \*radeon_gem_set_domain_ioctl\* function[1] to set domain. \*gobj\* is obtained via \*drm_gem_object_lookup\*[1], which refere

## Attachments

- [poc.c](attachments/poc.c) (text/plain, 1.5 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063579)*
