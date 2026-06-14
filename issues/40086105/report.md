# Security:  [FG-VD-16-086] Adobe Flash Player Handing MP4 Memory Corruption Vulnerability

| Field | Value |
|-------|-------|
| **Issue ID** | [40086105](https://issues.chromium.org/issues/40086105) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **Platforms** | Windows |
| **CVE IDs** | CVE-2017-2990 |
| **Reporter** | ke...@gmail.com |
| **Assignee** | na...@google.com |
| **Created** | 2016-11-28 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

It is a memory corruption vulnerability in MP4 processing.

**VERSION**  

Adobe Flash Player 23.0.0.207  

Other versions may be affected too

**REPRODUCTION CASE**  

put LoadMP42.swf and FG-VD-16-086\_PoC.mp4 on a server and load <http://127.0.0.1:8080/LoadMP42.swf?file=FG-VD-16-086_PoC.mp4>  

run the following command line.  

flashplayer\_23\_sa\_207.exe <http://127.0.0.1:8080/LoadMP42.swf?file=FG-VD-16-086_PoC.mp4>

Credits:  

This vulnerability was discovered by Kai Lu of Fortinet's FortiGuard Labs.

## Attachments

- [FG-VD-16-086_PoC.mp4](attachments/FG-VD-16-086_PoC.mp4) (video/mp4, 1.1 MB)
- [LoadMP42.swf](attachments/LoadMP42.swf) (application/octet-stream, 1.0 KB)
- [crashlog1.txt](attachments/crashlog1.txt) (text/plain, 3.6 KB)

## Timeline

### do...@chromium.org (2016-11-28)

+natashenka

Can you please confirm this affects the Flash player shipped with Chrome?

[Monorail components: Internals>Plugins>Flash]

### do...@chromium.org (2016-11-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-29)

[Empty comment from Monorail migration]

### na...@google.com (2016-11-30)

Repros for me consistently on Firefox, and inconsistently on Chrome and content projector only on Windows 7. I'll report this to Adobe.

### na...@google.com (2016-11-30)

This is PSIRT-6066.

### sh...@chromium.org (2016-12-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-26)

[Empty comment from Monorail migration]

### na...@google.com (2017-02-13)

This was fixed as CVE-2017-2990

### aw...@chromium.org (2017-02-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-18)

The panel decided to award $500 for this report - thanks!

### aw...@chromium.org (2017-02-18)

[Empty comment from Monorail migration]

### ke...@gmail.com (2017-02-18)

[Comment Deleted]

### ke...@gmail.com (2017-02-18)

[Comment Deleted]

### sh...@chromium.org (2017-02-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-19)

Your change meets the bar and is auto-approved for M57. Please go ahead and merge the CL to branch 2987 manually. Please contact milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), ketakid@(cros), govind@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2017-02-20)

No merge needed.

### aw...@google.com (2017-03-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-05-25)

This issue was migrated from crbug.com/chromium/669136?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086105)*
