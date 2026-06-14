# heap-use-after-free in ProfileCompare::operator()

| Field | Value |
|-------|-------|
| **Issue ID** | [40091762](https://issues.chromium.org/issues/40091762) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Incognito, UI>Browser>Profiles |
| **Platforms** | Linux |
| **Reporter** | cd...@gmail.com |
| **Assignee** | rh...@chromium.org |
| **Created** | 2018-06-25 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36

Steps to reproduce the problem:
1. Build source code 
    config args.gn file as below:
		use_sanitizer_coverage = true
		is_asan = true
		is_debug = false
		enable_nacl = fal

## Attachments

- deleted (application/octet-stream, 0 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091762)*
