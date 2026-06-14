# PDF viewer crash

| Field | Value |
|-------|-------|
| **Issue ID** | [40092593](https://issues.chromium.org/issues/40092593) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Internals>Plugins>PDF |
| **Reporter** | ao...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-07-13 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

\*NOTE\* The repro below seems to be a part of a malware sample. Have a look before trying to reproduce.

Opening the attached PDF document causes invalid reads to high usually page-aligned addresses in current Chrome beta on 64-bit Linux. Similar files crash at various addresses, and some are just null derefs or read 0x63. After some minimization the repro has a section of packed JS and a few objects. The crash didn't occur when I tried with unpacked JS (using jsbeautifier.org), so I left that as such to the repro.

**VERSION**  

Chrome Version: 13.0.782.56 (Official Build 92025) beta  

Operating System: Linux, Debian 6.0.2 x64\_64

**REPRODUCTION CASE**  

$ google-chrome malwarep.pdf  

seems to crash every time

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:  

Program received signal SIGSEGV, Segmentation fault.  

0x00007fffece7be9c in ?? () from /opt/google/chrome/libpdf.so  

(gdb) bt 10  

#0 0x00007fffece7be9c in ?? () from /opt/google/chrome/libpdf.so  

#1 0x00007fffecea1cb7 in ?? () from /opt/google/chrome/libpdf.so  

#2 0x00007fffece9cb94 in ?? () from /opt/google/chrome/libpdf.so  

#3 0x00007fffecea236f in ?? () from /opt/google/chrome/libpdf.so  

#4 0x00007fffece86b16 in ?? () from /opt/google/chrome/libpdf.so  

#5 0x00007fffece6b2d1 in ?? () from /opt/google/chrome/libpdf.so  

#6 0x00007fffecd16986 in ?? () from /opt/google/chrome/libpdf.so  

#7 0x00007fffecb7d04f in ?? () from /opt/google/chrome/libpdf.so  

#8 0x00007fffecb7d74c in ?? () from /opt/google/chrome/libpdf.so  

#9 0x00007fffecb7aff3 in ?? () from /opt/google/chrome/libpdf.so  

(More stack frames follow...)  

(gdb) x/5i $rip  

0x7fffece7be9c: mov (%rax,%rdx,8),%rax  

0x7fffece7bea0: mov %rax,0x10(%rsp)  

0x7fffece7bea5: mov 0x78(%r15),%rax  

0x7fffece7bea9: callq \*0x50(%rax)  

0x7fffece7beac: mov 0x8(%rsp),%rdi  

(gdb) i r  

rax 0x7fffc6e78b00 140736530451200  

rbx 0x7fffc6e0a300 140736529998592  

rcx 0xbc89f 772255  

rdx 0xbc8a0 772256  

rsi 0x0 0  

rdi 0x7fffc6e78b78 140736530451320  

rbp 0x7fffc6e60e14 0x7fffc6e60e14  

rsp 0x7fffffffb2f0 0x7fffffffb2f0  

r8 0x0 0  

r9 0x101010101010101 72340172838076673  

r10 0xf 15  

r11 0x7ffff21c938c 140737255347084  

r12 0x7fffc6e69e80 140736530390656  

r13 0x7fffffffb8c0 140737488337088  

r14 0xbc8a0 772256  

r15 0x7fffc6e78b00 140736530451200  

rip 0x7fffece7be9c 0x7fffece7be9c  

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

fiseg 0x7fff 32767  

fioff 0xecea0739 -320207047  

foseg 0x0 0  

fooff 0x0 0  

fop 0x5d8 1496  

mxcsr 0x1fa5 [ IE ZE PE IM DM ZM OM UM PM ]

## Attachments

- [malwarep.pdf](attachments/malwarep.pdf) (application/pdf; charset=us-ascii, 5.8 KB)

## Timeline

### th...@chromium.org (2011-07-13)

I can repro this on ToT.

### sc...@gmail.com (2011-07-13)

Repros for me in the debugger (miracle!!)
I'll fix it today.

### sc...@gmail.com (2011-07-13)

It's to do with nested function contexts.
Committed PDF r1044.
I'm sufficiently confident in the triviality of the fix that I merged it to M13 right away: r1045


### sc...@gmail.com (2011-07-20)

@aohelin: well, well! A PDF bug. Actually been a while since we had one externally, I thought I had fixed them all... hahaha!
Definitely worth a $500 Chromium Security Reward. Might have been $1000 if the actual PDF JS construct causing the issue had been extracted out of the crazy obfuscated JS in the PDF.

### sc...@gmail.com (2011-07-20)

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

### ao...@gmail.com (2011-07-20)

@scarybeasts Thanks :) 

Did you use automatic deobfuscation, tracing or something else on the JS? I tried the first and wasn't sure how to do the second with PDF.

### sc...@gmail.com (2011-07-20)

@aohelin: actually, there was a clearly wrong line of code in the vicinity of the crash, so that saved my sanity. I think a simple repro would be to call an inline-defined function, and have that function call another different inline-defined function. The parameters get messed up.

### sc...@gmail.com (2011-07-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-04)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed.. 

### sc...@gmail.com (2012-07-09)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

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

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/89142?no_tracker_redirect=1

[Multiple monorail components: Blink, Internals>Plugins>PDF]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092593)*
