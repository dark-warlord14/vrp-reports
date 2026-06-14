# Security: [FG-VD-16-076] Adobe Flash Player Handling ATF Heap Overflow Vulnerability

| Field | Value |
|-------|-------|
| **Issue ID** | [40085906](https://issues.chromium.org/issues/40085906) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **CVE IDs** | CVE-2017-2927 |
| **Reporter** | ke...@gmail.com |
| **Assignee** | na...@google.com |
| **Created** | 2016-11-08 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

It is a heap overflow vulnerability in ATF processing.

**VERSION**  

Adobe Flash Player 23.0.0.207  

Other versions may be affected too

**REPRODUCTION CASE**  

To reproduce the issue, put LoadImage.swf and FG-VD-16-076\_PoC.atf on a server and load <http://127.0.0.1:8080/LoadImage.swf?img=FG-VD-16-076_PoC.atf>.  

run the following command line in cmd.  

flashplayer\_23\_sa\_207.exe <http://127.0.0.1:8080/LoadImage.swf?img=FG-VD-16-076_PoC.atf>

Credits:  

This vulnerability was discovered by Kai Lu of Fortinet's FortiGuard Labs.

## Attachments

- [LoadImage.swf](attachments/LoadImage.swf) (application/octet-stream, 1.2 KB)
- [FG-VD-16-076_PoC.atf](attachments/FG-VD-16-076_PoC.atf) (application/octet-stream, 21.4 KB)
- [crashlog.txt](attachments/crashlog.txt) (text/plain, 1.6 KB)
- [IECrashlog1.txt](attachments/IECrashlog1.txt) (text/plain, 8.7 KB)

## Timeline

### ri...@chromium.org (2016-11-09)

Assigning flash bugs to natashenka@. Mind updating these with whether they affect Chrome stable? Thanks.

[Monorail components: Internals>Plugins>Flash]

### sh...@chromium.org (2016-11-09)

[Empty comment from Monorail migration]

### na...@google.com (2016-11-09)

Sorry, I'm having trouble getting this to crash. What browser and OS do these work on?

### ke...@gmail.com (2016-11-10)

I tested it with flash player standalone in windows 7,10.(enable page heap)
and also tested it in IE11 in Windows 7(enable page heap). They works.


### ke...@gmail.com (2016-11-10)

still not test it in Chrome yet, I will test it right now.

### ke...@gmail.com (2016-11-10)

Attached is the crash log in IE 11.

### na...@google.com (2016-11-12)

I'm still having trouble reproducing these, but I'm going to pass them to Adobe so they can investigate further. In the meantime, can you submit a sample that crashes in Chrome, as this is a Chrome rewards program?

### ke...@gmail.com (2016-11-15)

Ok,thanks. There are many crash samples for this case. I will try to find a sample that crashes in Chrome.

### ke...@chromium.org (2016-11-18)

Any update on triaging this? Thanks.

### na...@google.com (2016-11-18)

Sorry, there isn't. I've reported it to Adobe, I'll let you know when I hear back.

### me...@chromium.org (2016-11-21)

[Comment Deleted]

### na...@google.com (2016-11-30)

Adobe assigned this PSIRT-6013.

### na...@google.com (2017-01-10)

This was fixed this update as CVE-2017-2927. It is ready for the Rewards Panel.

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

This issue was migrated from crbug.com/chromium/663551?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085906)*
