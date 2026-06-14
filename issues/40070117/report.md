# Security: Out-of-Bound Write due to bound check missing

| Field | Value |
|-------|-------|
| **Issue ID** | [40070117](https://issues.chromium.org/issues/40070117) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | bu...@gmail.com |
| **Assignee** | st...@google.com |
| **Created** | 2023-08-21 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**   
  
When converting the IR of TGSI, `vrend_convert_shader` function will be invoked(https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/virglrenderer/src/vrend_shader.c;l=8048). The `iterate_declaration` function is set at the point[1]. Sub

## Attachments

- [evil_frag.txt](attachments/evil_frag.txt) (text/plain, 3.0 KB)
- [log_helper.diff](attachments/log_helper.diff) (text/plain, 543 B)
- deleted (application/octet-stream, 0 B)
- [patch.diff](attachments/patch.diff) (text/plain, 553 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40070117)*
