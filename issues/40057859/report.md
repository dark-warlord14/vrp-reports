# Security: UaF in AccessibilityUIMessageHandler::Callback

| Field | Value |
|-------|-------|
| **Issue ID** | [40057859](https://issues.chromium.org/issues/40057859) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Accessibility |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | as...@igalia.com |
| **Created** | 2021-11-09 |
| **Bounty** | $1,000.00 |

## Description

I feel that these two different crashes should be caused by the same reason, and I am not sure(https://crbug.com/chromium/1267179). I reproduced this crash under windows, but I couldn’t reproduce it successfully later, I don’t know why. The following is my analysis, which represents my point of view

## Attachments

- [crash.mkv](attachments/crash.mkv) (application/octet-stream, 4.9 MB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057859)*
