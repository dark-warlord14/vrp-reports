# Null-dereference READ in blink::AudioNode::Handler

| Field | Value |
|-------|-------|
| **Issue ID** | [40091851](https://issues.chromium.org/issues/40091851) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebAudio |
| **Platforms** | Linux |
| **Reporter** | cd...@gmail.com |
| **Assignee** | rt...@chromium.org |
| **Created** | 2018-07-05 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36

Steps to reproduce the problem:
Version 69.0.3477.0 (Developer Build) (64-bit)
1.Get new version chrome:
    Build source code 
    Config args.gn file as below:
		use_sani

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [crash.html](attachments/crash.html) (text/plain, 479 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091851)*
