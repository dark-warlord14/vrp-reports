# Nasty looking crash on internal pdf-reader

| Field | Value |
|-------|-------|
| **Issue ID** | [40051455](https://issues.chromium.org/issues/40051455) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink, Internals, Internals>Plugins>PDF |
| **Reporter** | at...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-11-21 |
| **Bounty** | $500.00 |

## Description

Nasty looking crash with high crash address with some variation between multiple runs. Crash address seems to change more between program re-runs but there is some variation if the page is refreshed multiple times.

chrome: segfault at 7fff787cbcb3 ip 00007fffe8880b58 sp 00007fffffffc7f0 error 4 in libpdf.so  

chrome: segfault at 7fff787cacb3 ip 00007fffe8880b58 sp 00007fffffffc7f0 error 4 in libpdf.so

**VERSION**  

Chrome Version: 17.0.942.0 (Official Build 110446) dev  

Reproduces on stable, beta and dev-channel versions.

Operating System: Ubuntu x86\_64 11.04

Doesn't reproduce on Windows x64

Reproducing case as attachment. I tried to reduce it as much as possible. Before the reduction there was some odd behavior in stack.

Type of crash: tab-crash  

Crash State: Cannot provide much information.

Program received signal SIGSEGV, Segmentation fault.  

0x00007fffe93e33f8 in ?? () from /opt/google/chrome/libpdf.so  

(gdb) i r  

rax 0x7fff7876b773 140735214434163  

rbx 0x1 1  

rcx 0x0 0  

rdx 0x0 0  

rsi 0x7fff7876b774 140735214434164  

rdi 0x3 3  

rbp 0x7ffff8714280 0x7ffff8714280  

rsp 0x7fffffffc020 0x7fffffffc020  

r8 0x1 1  

r9 0x0 0  

r10 0x1 1  

r11 0x7fffffffbf1c 140737488338716  

r12 0x80000000 2147483648  

r13 0x7fff7876b773 140735214434163  

r14 0x1 1  

r15 0x1 1  

rip 0x7fffe92e6b58 0x7fffe92e6b58  

eflags 0x10246 [ PF ZF IF RF ]  

cs 0x33 51  

ss 0x2b 43  

ds 0x0 0  

es 0x0 0  

fs 0x0 0  

gs 0x0 0

## Attachments

- [segfault-at-7fff787bc153-pdf.pdf](attachments/segfault-at-7fff787bc153-pdf.pdf) (application/pdf; charset=binary, 577 B)

## Timeline

### at...@gmail.com (2011-11-21)

Some additional info.
(gdb) bt 10
#0  0x00007fffe92e6b58 in ?? () from /opt/google/chrome/libpdf.so
#1  0x00007fffe92e7035 in ?? () from /opt/google/chrome/libpdf.so
#2  0x00007fffe92e8d66 in ?? () from /opt/google/chrome/libpdf.so
#3  0x00007fffe9262975 in ?? () from /opt/google/chrome/libpdf.so
#4  0x00007fffe9247d31 in ?? () from /opt/google/chrome/libpdf.so
#5  0x00007fffe92481a5 in ?? () from /opt/google/chrome/libpdf.so
#6  0x00007fffe9229242 in ?? () from /opt/google/chrome/libpdf.so
#7  0x00007fffe922b11d in ?? () from /opt/google/chrome/libpdf.so
#8  0x00007fffe92281a9 in ?? () from /opt/google/chrome/libpdf.so
#9  0x00007ffff65bde47 in ?? ()
(More stack frames follow...)
(gdb) x/i $rip
=> 0x7fffe92e6b58:      movzbl (%rax),%edx
(gdb) 


### [Deleted User] (2011-11-21)

When I run this it looks like a dup of http://crbug.com/104602

I can't tell from your two comments whether the registers listed in https://crbug.com/chromium/104959#c1 are for the instruction listed in https://crbug.com/chromium/104959#c2. This crashes in a null deref for me though.

### [Deleted User] (2011-11-21)

cevans do you see anything other than a null deref for this?

### at...@gmail.com (2011-11-21)

They should be from same but just for sure that I didn't refresh between I'll look for it again.

### at...@gmail.com (2011-11-21)

Program received signal SIGSEGV, Segmentation fault.
0x00007fffe91c3b58 in ?? () from /opt/google/chrome/libpdf.so
(gdb) bt 10
#0  0x00007fffe91c3b58 in ?? () from /opt/google/chrome/libpdf.so
#1  0x00007fffe91c4035 in ?? () from /opt/google/chrome/libpdf.so
#2  0x00007fffe91c5d66 in ?? () from /opt/google/chrome/libpdf.so
#3  0x00007fffe913f975 in ?? () from /opt/google/chrome/libpdf.so
#4  0x00007fffe9124d31 in ?? () from /opt/google/chrome/libpdf.so
#5  0x00007fffe91251a5 in ?? () from /opt/google/chrome/libpdf.so
#6  0x00007fffe9106242 in ?? () from /opt/google/chrome/libpdf.so
#7  0x00007fffe910811d in ?? () from /opt/google/chrome/libpdf.so
#8  0x00007fffe91051a9 in ?? () from /opt/google/chrome/libpdf.so
#9  0x00007ffff65bde47 in ?? ()
(More stack frames follow...)
(gdb) i r
rax            0x7fff787637e3   140735214401507
rbx            0x1      1
rcx            0x0      0
rdx            0x0      0
rsi            0x7fff787637e4   140735214401508
rdi            0x3      3
rbp            0x7ffff86f1500   0x7ffff86f1500
rsp            0x7fffffffbfa0   0x7fffffffbfa0
r8             0x1      1
r9             0x0      0
r10            0x1      1
r11            0x7fffffffbe9c   140737488338588
r12            0x80000000       2147483648
r13            0x7fff787637e3   140735214401507
r14            0x1      1
r15            0x1      1
rip            0x7fffe91c3b58   0x7fffe91c3b58
eflags         0x10246  [ PF ZF IF RF ]
cs             0x33     51
ss             0x2b     43
ds             0x0      0
es             0x0      0
fs             0x0      0
gs             0x0      0
(gdb) x/i $rip
=> 0x7fffe91c3b58:      movzbl (%rax),%edx

### th...@chromium.org (2011-11-21)

I see a different crash with a pending fix for https://crbug.com/chromium/104602 in my tree.

### [Deleted User] (2011-11-21)

Yeah I think this may have just been an issue with my checkout. cevans has verified this bug and will update it shortly.

### sc...@gmail.com (2011-11-21)

Could also be a 64-bit thing. I have easy repro on my M16 PDF checkout, 64-bit Linux.

### th...@chromium.org (2011-11-21)

I can also repro it with 32-bit. I hit the same crash with or without my pending fix for https://crbug.com/chromium/104602.

### sc...@gmail.com (2011-11-21)

Fixed at PDF r1172, rolled DEPS on trunk in r1173.

@attekett: another nice bug, keep 'em coming :)

It's basically a wild read -- I don't see the possibility of memory corruption. We rate these as Medium. I can't rule about the ability to recover the OOB content via an evil PDF, so we'll put this bug to the panel.

### at...@gmail.com (2011-11-21)

Glad you liked it. Lost some hair while minimizing the repro-file, but I think that I will add more effort/computing power on the PDF-testing. ;) Again I appreciate your fast response to the issue. 

### sc...@gmail.com (2011-11-23)

Merged to M16 at PDF r1175

### at...@gmail.com (2011-12-02)

I have now found few more files reproducing this crash and there seems to be some way to control the crash address via pdf-content. Just wanted to add the info.

### sc...@gmail.com (2011-12-10)

@attekett: thanks for your interesting PDF fuzzing. For this particular bug, it is a "medium" severity out-of-bounds read, however it seems likely that the OOB content might be recovered by the attacker. Hence a $500 Chromium Security Reward, good work :)

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

### at...@gmail.com (2011-12-10)

Cool. Thanks. :) 

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

This issue was migrated from crbug.com/chromium/104959?no_tracker_redirect=1

[Multiple monorail components: Blink, Internals, Internals>Plugins>PDF]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051455)*
