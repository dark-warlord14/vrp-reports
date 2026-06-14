# Security: heap-use-after-free in vrend_destroy_so_target

| Field | Value |
|-------|-------|
| **Issue ID** | [40071201](https://issues.chromium.org/issues/40071201) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | fi...@gmail.com |
| **Assignee** | st...@google.com |
| **Created** | 2023-09-02 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**   
```  
int vrend_create_so_target(struct vrend_context \*ctx,  
                           uint32_t handle,  
                           uint32_t res_handle,  
                           uint32_t buffer_offset,  
                           uint32_t buffer_size)  
{  
   s

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 6.7 KB)
- [virgl_fuzzer.c](attachments/virgl_fuzzer.c) (text/plain, 7.5 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40071201)*
