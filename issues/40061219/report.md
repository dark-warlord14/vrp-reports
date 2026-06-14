# Security: Files saved through showSaveFilePicker have unexpected read access

| Field | Value |
|-------|-------|
| **Issue ID** | [40061219](https://issues.chromium.org/issues/40061219) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Blink>Storage>FileSystem |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | re...@gmail.com |
| **Assignee** | ay...@chromium.org |
| **Created** | 2022-10-03 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**   
The showSaveFilePicker() method from the File System Access API can be used to open a read/write handle to a file chosen by the user. The save dialog displayed looks identical to a file download or the "save as" functionality, which implies that a file is being saved, bu

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.2 KB)
- [demo.mp4](attachments/demo.mp4) (video/mp4, 1.2 MB)
- [Screenshot 2023-09-28 at 10.52.36 AM.png](attachments/Screenshot 2023-09-28 at 10.52.36 AM.png) (image/png, 182.7 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061219)*
