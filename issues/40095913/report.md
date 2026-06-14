# Cross-origin-read attack by using an audio tag to download a cross-origin resource

| Field | Value |
|-------|-------|
| **Issue ID** | [40095913](https://issues.chromium.org/issues/40095913) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media>Audio, UI>Browser>Downloads |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | li...@chromium.org |
| **Created** | 2019-08-05 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**   
If a valid resource is used in an audio/video tag, a media player is displayed, which allows one to play/stop the audio/video, change the volume and also download it. A problem exists in that when the user clicks to download the media file, a new request is made, and ins

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095913)*
