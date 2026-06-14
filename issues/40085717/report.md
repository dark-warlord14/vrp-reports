# Security: Buffer Overflow in glBindBuffer

| Field | Value |
|-------|-------|
| **Issue ID** | [40085717](https://issues.chromium.org/issues/40085717) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Reporter** | ne...@gmail.com |
| **Assignee** | cw...@chromium.org |
| **Created** | 2016-10-17 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**   
in src/libANGLE/HandleAllocator.cpp see HandleAllocator::reserve. This function is called by glBindBuffer using the user provided handle:  
  
void HandleAllocator::reserve(GLuint handle)  
{  
    // ...  
  
    // Not in released list, reserve in the unallocated list.

## Attachments

- [poc.cc](attachments/poc.cc) (text/plain, 753 B)
- [asan](attachments/asan) (text/plain, 23.2 KB)
- [additional_logs](attachments/additional_logs) (text/plain, 1.2 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085717)*
