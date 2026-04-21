# Security: Out-Of-Bound read in Flash PCRE (regex engine)

| Field | Value |
|-------|-------|
| **Issue ID** | [40086850](https://issues.chromium.org/issues/40086850) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>Flash |
| **Platforms** | Windows |
| **Reporter** | sw...@gmail.com |
| **Assignee** | ih...@chromium.org |
| **Created** | 2017-02-19 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

There is a OOB read bug in the PCRE engine used in Flash player. This bug exists in match function while parsing the data that contains unicode.

src/pcre2\_intmodedep.h  

#define BACKCHAR(eptr) if ((\*eptr & 0xfc00u) == 0xdc00u) eptr--

src/pcre2\_match.c:3311  

for(;;)  

{  

RMATCH(eptr, ecode, offset\_top, mb, eptrb, RM21);  

if (rrc != MATCH\_NOMATCH) RRETURN(rrc);  

if (eptr-- == pp) break; /\* Stop if tried at original pos \*/  

#ifdef SUPPORT\_UNICODE  

if (utf) BACKCHAR(eptr);  

#endif  

}

The bugs occurs BACKCHAR macro when 'eptr' points specific letter(e.g. 'Ώ' or 'ŀ' and so on).  

In this case, 'eptr--' code will execute 'twice'. (First code : if (eptr-- == pp), Second code : BACKCHAR(eptr);).  

And eptr's value will be lower than pp. So, It will loop until found the match data(potential info leak) or crash.

To fix this problem, we need to modify break condition.

src/pcre2\_match.c:3158  

if (eptr-- == pp) break; to if (eptr-- <= pp) break;

src/pcre2\_match.c:3315  

if (eptr-- == pp) break; to if (eptr-- <= pp) break;

**VERSION**  

Chrome Version: 56.0.2924.87 stable  

Operating System: Windows 10  

Flash Version : 24.0.0.221  

PCRE2 Version : 10.23

**REPRODUCTION CASE**  

To reproduce crash in chrome  

1. I attached the testcase to reproduce bug. Please download the Main.swf (or compile Main.as using mxmlc) and index.html.  

2. Execute index.html

To download pcre2 engine

- You can download the source code at <ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/>

## Attachments

- [Main.as](attachments/Main.as) (text/plain, 253 B)
- [Main.swf](attachments/Main.swf) (application/octet-stream, 589 B)
- [repro.PNG](attachments/repro.PNG) (image/png, 4.5 KB)
- [test.html](attachments/test.html) (text/plain, 26 B)
- [callstack.txt](attachments/callstack.txt) (text/plain, 848 B)
- [pcre2grep_asan_log.txt](attachments/pcre2grep_asan_log.txt) (text/plain, 2.7 KB)

## Timeline

### ra...@chromium.org (2017-02-20)

Thanks for the report! I can verify that the crash happens on Windows. Could you please provide a stack trace?

ihf: are you able to forward this to the flash folks? Thanks!

[Monorail components: Internals>Plugins>Flash]

### ih...@chromium.org (2017-02-21)

[Empty comment from Monorail migration]

### sw...@gmail.com (2017-02-21)

Hello! I attached two logs.

- callstack.txt : crash log (Include call stack).

- pcre2grep_asan_log.txt : ASAN output of pcre2grep. (This log will help you. pcre2grep is one of the tools of pcre2 project)

Thank you.

### sh...@chromium.org (2017-02-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-07)

ihf: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2017-03-07)

This is fixed in 25.0.0.127.

### sh...@chromium.org (2017-03-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-15)

[Empty comment from Monorail migration]

### aw...@google.com (2017-03-15)

Congratulations! The panel decided to award $2,000 for this bug. Cheers!

### aw...@chromium.org (2017-03-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-18)

Your change meets the bar and is auto-approved for M58. Please go ahead and merge the CL to branch 3029 manually. Please contact milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), bhthompson@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@chromium.org (2017-03-18)

No merge's necessary.

### aw...@google.com (2017-04-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@chromium.org (2021-02-25)

[Empty comment from Monorail migration]

### is...@google.com (2021-02-25)

This issue was migrated from crbug.com/chromium/694067?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086850)*
