# Security: [FG-VD-16-075] Adobe Flash Player Handing MP4 Out-of-Bounds Read Vulnerability

| Field | Value |
|-------|-------|
| **Issue ID** | [40085905](https://issues.chromium.org/issues/40085905) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>Flash |
| **CVE IDs** | CVE-2017-2926 |
| **Reporter** | ke...@gmail.com |
| **Assignee** | na...@google.com |
| **Created** | 2016-11-08 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

It is a Out-of-Bounds read vulnerability in MP4 processing.

**VERSION**  

Adobe Flash Player 23.0.0.207  

Other versions may be affected too

**REPRODUCTION CASE**  

put LoadMP42.swf and FG-VD-16-075\_PoC.mp4 on a server and load <http://127.0.0.1:8080/LoadMP42.swf?file=FG-VD-16-075_PoC.mp4>  

run the following command line.  

flashplayer\_23\_sa\_207.exe <http://127.0.0.1:8080/LoadMP42.swf?file=FG-VD-16-075_PoC.mp4>

Credits:  

This vulnerability was discovered by Kai Lu of Fortinet's FortiGuard Labs.

## Attachments

- [LoadMP42.swf](attachments/LoadMP42.swf) (application/octet-stream, 1.0 KB)
- [FG-VD-16-075_PoC.mp4](attachments/FG-VD-16-075_PoC.mp4) (video/mp4, 153.1 KB)
- [crashlog.txt](attachments/crashlog.txt) (text/plain, 2.2 KB)
- [IECrashlog.txt](attachments/IECrashlog.txt) (text/plain, 1.9 KB)

## Timeline

### ri...@chromium.org (2016-11-09)

Assigning flash bugs to natashenka@. Mind updating these with whether they affect Chrome stable? Thanks.

[Monorail components: Internals>Plugins>Flash]

### sh...@chromium.org (2016-11-09)

[Empty comment from Monorail migration]

### na...@google.com (2016-11-09)

Sorry, I'm having trouble getting this to crash. What browser and OS do these work on?

### ke...@gmail.com (2016-11-09)

I tested it with flash player standalone in windows 7,10.(enable page heap)
and also tested it in IE11 in Windows 7(enable page heap).


### ke...@gmail.com (2016-11-10)

still not test it in Chrome yet, I will test it right now.

### ke...@gmail.com (2016-11-10)

attached is the crash log in IE 11.

### na...@google.com (2016-11-12)

I'm still having trouble reproducing these, but I'm going to pass them to Adobe so they can investigate further. In the meantime, can you submit a sample that crashes in Chrome, as this is a Chrome rewards program?

### ke...@gmail.com (2016-11-15)

Ok,thanks. There are some crash samples for this case. I will try to find a sample that crashes in Chrome.

### ke...@chromium.org (2016-11-18)

Any update on triaging this? Thanks.

### na...@google.com (2016-11-18)

Sorry, there isn't. I've reported it to Adobe, I'll let you know when I hear back.

### me...@chromium.org (2016-11-21)

[Empty comment from Monorail migration]

### na...@google.com (2016-11-30)

Adobe has assigned this PSIRT-6012

### na...@google.com (2017-01-10)

This was fixed as CVE-2017-2926 this month, it is ready for Rewards Panel.

### wf...@chromium.org (2017-01-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-18)

The panel decided to award $500 for this report.

### aw...@chromium.org (2017-02-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-20)

[Empty comment from Monorail migration]

### aw...@google.com (2017-03-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-04-19)

This issue was migrated from crbug.com/chromium/663549?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085905)*
