# Security: heap-use-after-free on vrend_renderer_get_meminfo

| Field | Value |
|-------|-------|
| **Issue ID** | [40072461](https://issues.chromium.org/issues/40072461) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | ph...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-09-15 |
| **Bounty** | $2,000.00 |

## Description

**-------------------------**   
  
**VULNERABILITY DETAILS**   
virgl_resource_create can destroy prev allocated resource lead to UAF  
```  
  
static struct virgl_resource \*  
virgl_resource_create(uint32_t res_id)  
{  
   struct virgl_resource \*res;  
   enum pipe_error err;  
  
   res =

## Attachments

- deleted (application/octet-stream, 0 B)
- [virgl_fuzzer.c](attachments/virgl_fuzzer.c) (text/plain, 6.0 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40072461)*
