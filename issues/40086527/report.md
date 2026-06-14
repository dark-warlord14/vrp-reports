# invalid free() in bundled pdf viewer

| Field | Value |
|-------|-------|
| **Issue ID** | [40086527](https://issues.chromium.org/issues/40086527) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Internals, Internals>Plugins>PDF |
| **Reporter** | ao...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2010-12-28 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Opening the attached PDF document causes tcmalloc to abort when trying to free an invalid pointer. Changing the content of the PDF document can be used to change the freed address. Sounds like the data in the document can be used to corrupt objects in memory, so reporting this as a potential security issue.

**VERSION**  

Chrome Version: 8.0.552.224 (Official Build 68599), 10.0.612.1 (Official Build 69289) dev  

Operating System: Linux (64-bit Ubuntu 10.10)

**REPRODUCTION CASE**  

Attached

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab (abort, not crash)  

Crash State:  

stderr shows "third\_party/tcmalloc/chromium/src/tcmalloc.cc:406] Attempt to free invalid pointer: 0x3f7e8000".

Backtrace is rather useless without debugging symbols:  

Program received signal SIGABRT, Aborted.  

0x00007ffff1cc5ba5 in raise (sig=<value optimized out>)  

at ../nptl/sysdeps/unix/sysv/linux/raise.c:64  

64 ../nptl/sysdeps/unix/sysv/linux/raise.c: No such file or directory.  

in ../nptl/sysdeps/unix/sysv/linux/raise.c  

(gdb) bt 10  

#0 0x00007ffff1cc5ba5 in raise (sig=<value optimized out>)  

at ../nptl/sysdeps/unix/sysv/linux/raise.c:64  

#1 0x00007ffff1cc96b0 in abort () at abort.c:92  

#2 0x0000000000b41f60 in ?? ()  

#3 0x0000000000b42098 in ?? ()  

#4 0x0000000000b3b0b3 in ?? ()  

#5 0x00007fffec1e4d13 in ?? () from /opt/google/chrome/libpdf.so  

#6 0x00007fffec1e5866 in ?? () from /opt/google/chrome/libpdf.so  

#7 0x00007fffec1e59f1 in ?? () from /opt/google/chrome/libpdf.so  

#8 0x00007fffec1d5ec8 in ?? () from /opt/google/chrome/libpdf.so  

#9 0x00007fffec1d74f9 in ?? () from /opt/google/chrome/libpdf.so  

(More stack frames follow...)

## Attachments

- [pointer.pdf](attachments/pointer.pdf) (application/pdf; charset=binary, 1.4 KB)
- [stutr.pdf](attachments/stutr.pdf) (application/pdf; charset=binary, 107.8 KB)

## Timeline

### sc...@gmail.com (2010-12-28)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-12-28)

Interesting bug. How did you generate this bad file?

### ao...@gmail.com (2010-12-28)

This one was from plain sample-based fuzzing. I left a test running over Christmas using some new samples from http://acroeng.adobe.com/ (would recommend having a look). This one was the only result that did not look harmless. The original repro was pretty large and had content from several sample files, so I just did a quick manual minimization on it.

### sc...@gmail.com (2010-12-28)

What do you mean by "sample-based fuzzing"? Fuzzing a large sample set? Or just running a large number of unmodified inputs?

In the case of active fuzzing, what mutation algorithm is in use?

### ao...@gmail.com (2010-12-28)

Active fuzzing using several black-box fuzzers. Each fuzzer does some possibly global preprocessing using the given sample files, and then uses the result (or just the raw sample data) to make something like the given samples. In practice this was from $ radamsa -o /tmp samples/*.pdf :)

The original repro was from the surfy fuzzer module, which computes suffix arrays and uses them to jump at random positions to other places with a shared suffix, allowing content to be mixed within and between files, often without breaking the structure too much.

I just noticed stutr also found this bug, so it can be triggered with just material from one file. Have to go now, but adding it anyway in case it is useful. It is based on just one of some of the acroeng.adobe.com files.

### sc...@gmail.com (2010-12-28)

Easy enough to fix -- fix is in review.

### sc...@gmail.com (2010-12-28)

Fixed on PDF branch r789 (trunk), r790 (m8) and r791 (m9)

Hopefully the speed of this fix meets with your expectations of the Chrome team :)

### sc...@gmail.com (2010-12-29)

@aohelin -- congratulations! This bug provisionally qualifies for a $1000 Chromium Security Reward!
It's a great find.
We're rewarding above the base $500 level due to various things:
- Thanks for taking effort to minimize the input file!
- Inclusion of stack details and error message.
- Providing repro information about multiple versions.

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### ao...@gmail.com (2010-12-29)

Woah! 4 hours between report being issued and fix landing to major branches. Nice :)

### js...@chromium.org (2011-01-14)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-01-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-01-18)

Invoice finalized; payment is in e-payment system.

Was fixed in 8.0.552.237

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### sc...@gmail.com (2012-07-09)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/68170?no_tracker_redirect=1

[Multiple monorail components: Blink, Internals, Internals>Plugins>PDF]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086527)*
