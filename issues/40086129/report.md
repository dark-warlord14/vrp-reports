# Security: [FG-VD-16-088] Adobe Flash Player Handing MP4 Out-of-Bounds Read Vulnerability

| Field | Value |
|-------|-------|
| **Issue ID** | [40086129](https://issues.chromium.org/issues/40086129) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **CVE IDs** | CVE-2017-2991 |
| **Reporter** | ke...@gmail.com |
| **Assignee** | na...@google.com |
| **Created** | 2016-12-01 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

It is a out-of-bounds read vulnerability in MP4 processing.

**VERSION**  

Adobe Flash Player 23.0.0.207  

Other versions may be affected too

**REPRODUCTION CASE**  

put LoadMP42.swf and FG-VD-16-088\_PoC.mp4 on a server and load <http://127.0.0.1:8080/LoadMP42.swf?file=FG-VD-16-088_PoC.mp4>  

run the following command line.  

flashplayer\_23\_sa\_207.exe <http://127.0.0.1:8080/LoadMP42.swf?file=FG-VD-16-088_PoC.mp4>

Credits:  

This vulnerability was discovered by Kai Lu of Fortinet's FortiGuard Labs.

Note: I tested this case and it can be reproduced stably in standalone player(pageheap enabled)and other browsers, such as Firefox , IE on Windows 10 Pro x64 and Windows 7 x64. Repros inconsistently on Chrome ,I need more time to investigate the reason.

## Attachments

- [FG-VD-16-088_PoC.mp4](attachments/FG-VD-16-088_PoC.mp4) (video/mp4, 1.4 MB)
- [LoadMP42.swf](attachments/LoadMP42.swf) (application/octet-stream, 1.0 KB)
- [crashlog.txt](attachments/crashlog.txt) (text/plain, 4.9 KB)

## Timeline

### oc...@chromium.org (2016-12-01)

Natalie, mind taking a look at this one?

### na...@google.com (2016-12-01)

Reproduced the crash on Windows 7. Will report to Adobe.

### na...@google.com (2017-02-13)

This was fixed as CVE-2017-2991

### ke...@gmail.com (2017-02-16)

This is PSIRT-6100.

### ke...@gmail.com (2017-02-18)

[Comment Deleted]

### aw...@chromium.org (2017-02-20)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-21)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-28)

Congratulations! The panel decided to award $1,000 for this bug!

### aw...@chromium.org (2017-02-28)

[Empty comment from Monorail migration]

### ke...@gmail.com (2017-03-01)

thanks!

### aw...@google.com (2017-03-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/670457?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086129)*
