# Security: Chrome OS: OOB read and write in venus_read_queue and venus_write_queue of venus driver

| Field | Value |
|-------|-------|
| **Issue ID** | [40065774](https://issues.chromium.org/issues/40065774) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | pi...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-06-13 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**   
  
Background:  
  
venus is responsible for video hardware codec, it supports some complicated codecs.  
When chrome browses a video web page, if codec matches, chrome browser will send the video buffer to venus driver, venus driver will send to venus firmware to

## Attachments

- [1454624.diff](attachments/1454624.diff) (text/plain, 1.1 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065774)*
