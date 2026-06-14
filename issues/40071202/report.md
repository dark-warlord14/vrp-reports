# Security: heap-use-after-free in vrend_destroy_surface

| Field | Value |
|-------|-------|
| **Issue ID** | [40071202](https://issues.chromium.org/issues/40071202) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | fi...@gmail.com |
| **Assignee** | st...@google.com |
| **Created** | 2023-09-02 |
| **Bounty** | $4,000.00 |

## Description

**VULNERABILITY DETAILS**   
```  
int vrend_create_surface(struct vrend_context \*ctx,  
                         uint32_t handle,  
                         uint32_t res_handle, uint32_t format,  
                         uint32_t val0, uint32_t val1,  
                         uint32_t nr_samples

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 6.4 KB)
- [virgl_fuzzer.c](attachments/virgl_fuzzer.c) (text/plain, 7.5 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40071202)*
