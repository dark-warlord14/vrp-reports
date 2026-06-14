# CVE-2017-5123: Chrome Sandbox escape through linux kernel vulnerability introduced in 4.13 in waitid

| Field | Value |
|-------|-------|
| **Issue ID** | [40089264](https://issues.chromium.org/issues/40089264) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Linux |
| **CVE IDs** | CVE-2017-5123 |
| **Reporter** | ch...@gmail.com |
| **Assignee** | gr...@chromium.org |
| **Created** | 2017-10-09 |
| **Bounty** | $15,000.00 |

## Description

A linux kernel vulnerability introduced in 4.13 can be used to escape the chrome sandbox. 4.13 is a stable release and is included in Ubuntu 17.10 which is set to be released on October 19th. 

Vulnerability Details:
In the linux kernel, inside the waitid syscall, unsafe_put_user is used to copy

## Attachments

- [exploit_no_smap.c](attachments/exploit_no_smap.c) (text/plain, 10.3 KB)
- [exploit_smap_bypass.c](attachments/exploit_smap_bypass.c) (text/plain, 25.4 KB)
- [standalone_poc_no_smap.c](attachments/standalone_poc_no_smap.c) (text/plain, 12.8 KB)
- [standalone_poc_smap_bypass.c](attachments/standalone_poc_smap_bypass.c) (text/plain, 28.3 KB)
- [chrome_seccomp_filter](attachments/chrome_seccomp_filter) (text/plain, 3.6 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089264)*
