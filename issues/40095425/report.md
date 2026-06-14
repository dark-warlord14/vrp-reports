# heap-use-after-free in ContextProvider

| Field | Value |
|-------|-------|
| **Issue ID** | [40095425](https://issues.chromium.org/issues/40095425) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Canvas, Blink>Paint, Blink>WebGL, Internals>GPU |
| **Platforms** | Linux |
| **Reporter** | cd...@gmail.com |
| **Assignee** | kh...@chromium.org |
| **Created** | 2019-06-18 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36

Steps to reproduce the problem:
1.Build asan 77.0.3828.0 version of chrome
2.Run ./chrome poc.html

What is the expected behavior?

What went wrong?
3.Reproduce ua

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095425)*
