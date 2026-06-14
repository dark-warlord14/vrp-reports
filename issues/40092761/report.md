# Security: use-after-poison in blink::AsyncMethodRunner<class blink::MediaRecorder>::RunAsync

| Field | Value |
|-------|-------|
| **Issue ID** | [40092761](https://issues.chromium.org/issues/40092761) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>MediaRecording |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | em...@chromium.org |
| **Created** | 2018-10-18 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**   
A MediaRecorder object contains a unique_ptr to a MediaRecorderHandler instance. Therefore, MediaRecorder's destruction might trigger the deletion of the related MediaRecorderHandler object.  
MediaRecorderHandler's destructor would then call back into MediaRecorder::Wri

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 8.3 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092761)*
