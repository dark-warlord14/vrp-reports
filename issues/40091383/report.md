# use-after-poison in  operator-> (from HTMLImportsController::Dispose)

| Field | Value |
|-------|-------|
| **Issue ID** | [40091383](https://issues.chromium.org/issues/40091383) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>GarbageCollection, Blink>HTML>Modules |
| **Platforms** | Linux |
| **Reporter** | cd...@gmail.com |
| **Assignee** | tk...@chromium.org |
| **Created** | 2018-05-15 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36

Steps to reproduce the problem:
1.Get new version chrome:
 a) Build source code 
    config args.gn file as below:
		use_sanitizer_coverage = true
		is_asan = true
		is_d

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [launcher.html](attachments/launcher.html) (text/plain, 223 B)
- [poc1.html](attachments/poc1.html) (text/plain, 816 B)
- [poc2.html](attachments/poc2.html) (text/plain, 3.4 KB)
- [repro.mp4](attachments/repro.mp4) (video/mp4, 6.0 MB)
- [launcher.html](attachments/launcher_53384809.html) (text/plain, 381 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091383)*
