# Security: heap-buffer-overflow vrend_write_to_iovec

| Field | Value |
|-------|-------|
| **Issue ID** | [40071209](https://issues.chromium.org/issues/40071209) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | ph...@gmail.com |
| **Assignee** | st...@google.com |
| **Created** | 2023-09-02 |
| **Bounty** | $250.00 |

## Description

**VULNERABILITY DETAILS**   
heap-buffer-overflow vrend_write_to_iovec  
  
vrend_write_to_iovec call memcpy without check for buf size lead to heap buffer overlow  
```  
  
size_t vrend_write_to_iovec(const struct iovec \*iov, int iovlen,  
			 size_t offset, const char \*buf, size_t count)  
{

## Attachments

- [virgl_fuzzer.c](attachments/virgl_fuzzer.c) (text/plain, 7.7 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40071209)*
