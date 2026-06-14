# uaf in content::DesktopCaptureDevice::Core::AllocateAndStart

| Field | Value |
|-------|-------|
| **Issue ID** | [40057057](https://issues.chromium.org/issues/40057057) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media>ScreenCapture |
| **Platforms** | Windows |
| **Reporter** | wx...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2021-08-27 |
| **Bounty** | $10,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36

Steps to reproduce the problem:
1.the first step is similar as  https://crbug.com/chromium/1244188
2.1. Apply the attached token.patch (*)
2. $ python ./copy_mojo_js_b

## Attachments

- [access_violation.txt](attachments/access_violation.txt) (text/plain, 15.8 KB)
- deleted (application/octet-stream, 0 B)
- [mojo_test1.html](attachments/mojo_test1.html) (text/plain, 3.8 KB)
- [patch.PNG](attachments/patch.PNG) (image/png, 55.3 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057057)*
