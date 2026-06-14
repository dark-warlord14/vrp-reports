# segfault in bundled PDF viewer (invalid read in strlen)

| Field | Value |
|-------|-------|
| **Issue ID** | [40084957](https://issues.chromium.org/issues/40084957) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | ao...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2010-11-15 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Opening the attached PDF document causes a controllable arbitrary read to happen in strlen(). The error is triggered from JS with a call to util.printf() with a somewhat funny format. I did not have time to look at this further today, but decided to submit as such as the viewer is already enabled in beta. The read obviously gives some control over the assumed size of some string, which might allow exploitation via a stack- of buffer overflow, but this bug might also have more direct use cases.

**VERSION**  

Chrome Version: 8.0.552.200 (Official Build 65749) beta  

Operating System: Linux, Debian 5.0.6, 32-bit

**REPRODUCTION CASE**  

Attached.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:  

Program received signal SIGSEGV, Segmentation fault.  

0xb72594cb in strlen () from /lib/i686/cmov/libc.so.6  

(gdb) bt  

#0 0xb72594cb in strlen () from /lib/i686/cmov/libc.so.6  

#1 0xb5b87b50 in ?? () from /opt/google/chrome/libpdf.so  

#2 0xb5b87cf2 in ?? () from /opt/google/chrome/libpdf.so  

#3 0xb5c0c32a in ?? () from /opt/google/chrome/libpdf.so  

#4 0xb5c0cd3b in ?? () from /opt/google/chrome/libpdf.so  

#5 0xb5c7a905 in ?? () from /opt/google/chrome/libpdf.so  

#6 0xb5c9dcd7 in ?? () from /opt/google/chrome/libpdf.so  

#7 0xb5cb1787 in ?? () from /opt/google/chrome/libpdf.so  

#8 0xb5cacd7a in ?? () from /opt/google/chrome/libpdf.so  

#9 0xb5c9dcd7 in ?? () from /opt/google/chrome/libpdf.so  

#10 0xb5cb186d in ?? () from /opt/google/chrome/libpdf.so  

#11 0xb5c90580 in ?? () from /opt/google/chrome/libpdf.so  

#12 0xb5c79273 in ?? () from /opt/google/chrome/libpdf.so  

[...]  

(gdb) disas $eip-13, $eip+8  

Dump of assembler code from 0xb72594be to 0xb72594d3:  

0xb72594be <strerror\_r+302>: jmp 0xb725947c <strerror\_r+236>  

0xb72594c0 <strlen+0>: mov 0x4(%esp),%ecx  

0xb72594c4 <strlen+4>: mov %ecx,%eax  

0xb72594c6 <strlen+6>: and $0x3,%ecx  

0xb72594c9 <strlen+9>: je 0xb72594f3 <strlen+51>  

=> 0xb72594cb <strlen+11>: cmp %ch,(%eax)  

0xb72594cd <strlen+13>: je 0xb725956a <strlen+170>  

End of assembler dump.  

(gdb) p $ch  

$1 = 0  

(gdb) info registers  

eax 0xbadf00d 195948557  

ecx 0x1 1  

edx 0x73 115  

ebx 0xb6a5c208 -1230650872  

esp 0xbfffc9bc 0xbfffc9bc  

ebp 0xbfffcb18 0xbfffcb18  

esi 0xbfffcb5c -1073755300  

edi 0xbfffcb58 -1073755304  

eip 0xb72594cb 0xb72594cb <strlen+11>  

eflags 0x10202 [ IF RF ]  

cs 0x73 115  

ss 0x7b 123  

ds 0x7b 123  

es 0x7b 123  

fs 0x0 0  

gs 0x33 51

## Attachments

- [printf.pdf](attachments/printf.pdf) (application/pdf; charset=us-ascii, 697 B)

## Timeline

### sc...@gmail.com (2010-11-15)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-11-16)

Ugh, I can use this to sneak in a bad memory write.
Nice find, Aki.

### sc...@gmail.com (2010-11-17)

Fixed in r709 plus compile fix (r710), merged to M8. Should hit the next Beta going out this week.

### sc...@gmail.com (2010-11-18)

Woohoo! This qualifies for a $1000 Chromium Security Reward.

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

### ao...@gmail.com (2010-11-18)

Excellent :)

Thanks for finding the write case.

### sc...@gmail.com (2010-11-21)

Payment is in the electronic system.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update: More fuzzy classification of security bugs not affecting stable.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/63248?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084957)*
