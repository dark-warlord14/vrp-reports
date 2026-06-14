# Arbitrary Read in swiftshader

| Field | Value |
|-------|-------|
| **Issue ID** | [40094236](https://issues.chromium.org/issues/40094236) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>SwiftShader |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2019-03-07 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36

Steps to reproduce the problem:
Simplest PoC:

#version 300 es
layout(location=0x86868686u

* the value in "location" must be greater than 0x7fffffff and should be

## Attachments

- [0xc0000005.jpg](attachments/0xc0000005.jpg) (image/jpeg, 296.8 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094236)*
