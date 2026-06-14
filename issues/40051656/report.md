# Nasty looking INVALID_POINTER_READ in internal PDF-reader

| Field | Value |
|-------|-------|
| **Issue ID** | [40051656](https://issues.chromium.org/issues/40051656) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals |
| **Reporter** | at...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-11-29 |
| **Bounty** | $500.00 |

## Description

Nasty looking tab-crash with high and slightly changing crash address.

chrome: segfault at 7f0dcb89ac72 ip 00007f0dc710c2a1 sp 00007ffffdba5288 error 4 in libpdf.so[7f0dc6fe2000+5d4000]  

chrome: segfault at 7f0dcb899c72 ip 00007f0dc710c2a1 sp 00007ffffdba5288 error 4 in libpdf.so[7f0dc6fe2000+5d4000]  

chrome: segfault at 7f0dcb927c72 ip 00007f0dc710c2a1 sp 00007ffffdba5288 error 4 in libpdf.so[7f0dc6fe2000+5d4000]  

chrome: segfault at 7f0dcb928c72 ip 00007f0dc710c2a1 sp 00007ffffdba5288 error 4 in libpdf.so[7f0dc6fe2000+5d4000]

Reproduction case as attachment.

**VERSION**  

Ubuntu x64  

Chrome Versions:15.0.874.121-r109964(stable)  

16.0.912.41-r110024(beta)  

17.0.942.0-r110446(dev)  

Windows 7 x64 SP1  

Chrome Version: 17.0.942.0 (Official Build 110446) dev-m

More information:

<</Decode[0.0 255.0]/Intent/RelativeColorimetric/Type/XObject/ColorSpace 15 0 R/Subtype/Image/Name/X/Width 36/BitsPerComponent 242794283153874938024420238

Bringing the value of BitsPerComponent into "BitsPerComponent 59652324" turns the crash on linux into Abort and on windows gives weird error popup with only error icon(Red X) and OK button. Changing the value into anything smaller will prevent the crash. Also changing any character from the first FlateDecoded object will prevent the crash.

Windows WinDBG Analyze:

0:000> !load winext\msec.dll  

0:000> !analyze -v

FAULTING\_IP:  

pdf!PPP\_GetInterface+14e506  

63620344 0fb610 movzx edx,byte ptr [eax]

EXCEPTION\_RECORD: ffffffff -- (.exr 0xffffffffffffffff)  

ExceptionAddress: 63620344 (pdf!PPP\_GetInterface+0x0014e506)  

ExceptionCode: c0000005 (Access violation)  

ExceptionFlags: 00000000  

NumberParameters: 2  

Parameter[0]: 00000000  

Parameter[1]: f684ef16  

Attempt to read from address f684ef16

DEFAULT\_BUCKET\_ID: INVALID\_POINTER\_READ

PROCESS\_NAME: chrome.exe

EXCEPTION\_PARAMETER1: 00000000

EXCEPTION\_PARAMETER2: f684ef16

READ\_ADDRESS: f684ef16

FOLLOWUP\_IP:  

pdf!PPP\_GetInterface+14e506  

63620344 0fb610 movzx edx,byte ptr [eax]

MOD\_LIST: <ANALYSIS/>

FAULTING\_THREAD: 00000974

PRIMARY\_PROBLEM\_CLASS: INVALID\_POINTER\_READ

BUGCHECK\_STR: APPLICATION\_FAULT\_INVALID\_POINTER\_READ

LAST\_CONTROL\_TRANSFER: from 636218ca to 63620344

STACK\_TEXT:  

WARNING: Stack unwind information not available. Following frames may be wrong.  

0015f240 636218ca 046e0020 02c4c178 02c50898 pdf!PPP\_GetInterface+0x14e506  

0015f26c 6351f5c7 046e0020 02cb4a08 02c4b988 pdf!PPP\_GetInterface+0x14fa8c  

0015f2ac 63635d96 00000000 017d8650 02cb4a08 pdf!PPP\_GetInterface+0x4d789  

0015f2c0 63635d0d 02c4b980 02c4b984 017d8470 pdf!PPP\_GetInterface+0x163f58  

0015f2e8 63621f0d 02c4b980 02c4b984 02c4b988 pdf!PPP\_GetInterface+0x163ecf  

0015f350 63625427 02c6f0b0 02c6bad8 02c730ac pdf!PPP\_GetInterface+0x1500cf  

0015f3c0 6362637f 02c6ecf0 0015f450 634c4721 pdf!PPP\_GetInterface+0x1535e9  

0015f410 634c7ebc 02c3ab30 017da848 00000005 pdf!PPP\_GetInterface+0x154541  

0015f470 634b68e8 02c50598 017da848 00000005 pdf!GetPDFDocInfo+0x19bef  

0015f4d4 634b3300 00000000 017d3e18 0015f5e0 pdf!GetPDFDocInfo+0x861b  

0015f574 634a5eec 0015f618 0015f5f8 0015f5e0 pdf!GetPDFDocInfo+0x5033  

0015f664 634ace0c 0015f72c 0015f690 0015f6ac pdf+0x5eec  

0015f790 634ad2eb 0015f808 02c711f0 010e3268 pdf+0xce0c  

0015f7a4 634ad62f 00000000 0015f7d4 5fd9c54c pdf+0xd2eb  

0015f7e8 5fa9d59a 00115d14 0015f808 0015fae0 pdf+0xd62f  

0015f7f8 5fa9d92a 0015fad8 01060140 01117600 chrome\_5f970000!MessageLoop::DeferOrRunPendingTask+0x26 [d:\b\build\slave\chrome-official\build\src\base\message\_loop.cc @ 515]  

0015f840 5fab845e 0106eb04 0015fad8 00000000 chrome\_5f970000!MessageLoop::DoWork+0x87 [d:\b\build\slave\chrome-official\build\src\base\message\_loop.cc @ 702]  

0015f86c 5fa9d40c 0015fad8 60f029b0 5fa9d391 chrome\_5f970000!base::MessagePumpDefault::Run+0xc2 [d:\b\build\slave\chrome-official\build\src\base\message\_pump\_default.cc @ 55]  

0015f878 5fa9d391 00000000 5fa9d314 0015f8a0 chrome\_5f970000!MessageLoop::RunInternal+0x31 [d:\b\build\slave\chrome-official\build\src\base\message\_loop.cc @ 460]  

0015f880 5fa9d314 0015f8a0 00000001 0106eb00 chrome\_5f970000!MessageLoop::RunHandler+0x17 [d:\b\build\slave\chrome-official\build\src\base\message\_loop.cc @ 432]  

0015f8a0 5ff21188 0015fdcc 00000001 00000000 chrome\_5f970000!MessageLoop::Run+0x15 [d:\b\build\slave\chrome-official\build\src\base\message\_loop.cc @ 343]  

0015fc1c 5fac1316 0015fc84 00000001 00000000 chrome\_5f970000!RendererMain+0x329 [d:\b\build\slave\chrome-official\build\src\content\renderer\renderer\_main.cc @ 242]  

0015fc30 5fac16b3 0015fd7c 0015fc84 00c65368 chrome\_5f970000!`anonymous namespace'::RunNamedProcessTypeMain+0x41 [d:\b\build\slave\chrome-official\build\src\content\app\content\_main.cc @ 262]  

0015fdb8 5f974a12 0015fe94 0015fdcc 00c65378 chrome\_5f970000!content::ContentMain+0x394 [d:\b\build\slave\chrome-official\build\src\content\app\content\_main.cc @ 453]  

0015fde8 002b1d9f 002b0000 0015fe94 0015fe9c chrome\_5f970000!ChromeMain+0x32 [d:\b\build\slave\chrome-official\build\src\chrome\app\chrome\_main.cc @ 28]  

0015fe70 002b10ce 002b0000 0015fe94 fffffffe chrome!MainDllLoader::Launch+0xf3 [d:\b\build\slave\chrome-official\build\src\chrome\app\client\_util.cc @ 347]  

0015fed8 0030a438 002b0000 00000000 005a2498 chrome!wWinMain+0xce [d:\b\build\slave\chrome-official\build\src\chrome\app\chrome\_exe\_main\_win.cc @ 37]  

0015ff68 7500339a 7efde000 0015ffb4 76ec9ed2 chrome!\_\_tmainCRTStartup+0x112 [f:\dd\vctools\crt\_bld\self\_x86\crt\src\crt0.c @ 263]  

0015ff74 76ec9ed2 7efde000 76fd836e 00000000 kernel32!BaseThreadInitThunk+0xe  

0015ffb4 76ec9ea5 0030a4a3 7efde000 00000000 ntdll!\_\_RtlUserThreadStart+0x70  

0015ffcc 00000000 0030a4a3 7efde000 00000000 ntdll!\_RtlUserThreadStart+0x1b

STACK\_COMMAND: ~0s; .ecxr ; kb

SYMBOL\_STACK\_INDEX: 0

SYMBOL\_NAME: pdf!PPP\_GetInterface+14e506

MODULE\_NAME: pdf

IMAGE\_NAME: pdf.dll

FAILURE\_BUCKET\_ID: INVALID\_POINTER\_READ\_c0000005\_pdf.dll!PPP\_GetInterface

BUCKET\_ID: APPLICATION\_FAULT\_INVALID\_POINTER\_READ\_pdf!PPP\_GetInterface+14e506

---

0:000> !exploitable  

Exploitability Classification: UNKNOWN  

Recommended Bug Title: Read Access Violation starting at pdf!PPP\_GetInterface+0x000000000014e506 (Hash=0x0064646f.0x001e1c1f)

## Attachments

- [reduced_possible_wild_read_29.11.pdf](attachments/reduced_possible_wild_read_29.11.pdf) (application/pdf; charset=binary, 9.2 KB)
- [reduced_later_29.11.pdf](attachments/reduced_later_29.11.pdf) (application/pdf; charset=binary, 15.5 KB)

## Timeline

### at...@gmail.com (2011-11-29)

Linux side GDB info:

Program received signal SIGSEGV, Segmentation fault.
0x00007fffe91ce2a1 in ?? () from /opt/google/chrome/libpdf.so

(gdb) bt 10
#0  0x00007fffe91ce2a1 in ?? () from /opt/google/chrome/libpdf.so
#1  0x00007fffe91cee8d in ?? () from /opt/google/chrome/libpdf.so
#2  0x00007fffe91cf284 in ?? () from /opt/google/chrome/libpdf.so
#3  0x00007fffe933a22d in ?? () from /opt/google/chrome/libpdf.so
#4  0x00007fffe91cb3fa in ?? () from /opt/google/chrome/libpdf.so
#5  0x00007fffe91cb4e4 in ?? () from /opt/google/chrome/libpdf.so
#6  0x00007fffe91d0f09 in ?? () from /opt/google/chrome/libpdf.so
#7  0x00007fffe91cddc4 in ?? () from /opt/google/chrome/libpdf.so
#8  0x00007fffe91cae1f in ?? () from /opt/google/chrome/libpdf.so
#9  0x00007fffe91cb032 in ?? () from /opt/google/chrome/libpdf.so
(More stack frames follow...)

(gdb) i r
rax            0xf2d27c72       4073880690
rbx            0x7ffff888a320   140737363092256
rcx            0xfffffffff2d27c72       -221086606
rdx            0x9693e38e       2526274446
rsi            0x9693e38e       2526274446
rdi            0x7ffff88b0000   140737363247104
rbp            0x9693e38e       0x9693e38e
rsp            0x7fffffffbf08   0x7fffffffbf08
r8             0x1      1
r9             0xb      11
r10            0x0      0
r11            0x24     36
r12            0x7fffffffbf40   140737488338752
r13            0x7ffff88b0000   140737363247104
r14            0x7ffff88a3773   140737363195763
r15            0x1      1
rip            0x7fffe91ce2a1   0x7fffe91ce2a1
eflags         0x10282  [ SF IF RF ]
cs             0x33     51
ss             0x2b     43
ds             0x0      0
es             0x0      0
fs             0x0      0
gs             0x0      0

(gdb)  x/i $rip
=> 0x7fffe91ce2a1:      movzbl (%rdi,%rcx,1),%eax

### at...@gmail.com (2011-11-29)

I think that this is a problem with BitsPerComponent. Just found another reprofile that causes same looking crash and same type of ip. File has value /BitsPerComponent 928136143161367830519585563 and when the value is reduced into small enough the crashing stops. If you need I can reduce the second reprofile and submit it also. I think I take a look into it later on today anyway.

### pa...@chromium.org (2011-11-29)

Thanks attekett! If you could reduce and send the second repro file, that'd be helpful.

### at...@gmail.com (2011-11-29)

Working on it. 

### at...@gmail.com (2011-11-29)

I have no idea how to reduce the file more. I can't touch the FlateDecoded stuff that makes most of the file. Well it is much better now than with the original 700k size. I hope this helps you.

### sc...@gmail.com (2011-11-29)

Looks easy to fix, I will do so a bit later today. Looks more like a medium than high (OOB reads)

### sc...@gmail.com (2011-11-30)

Fix is very safe to merge.
Fixed on PDF trunk at r1196

### sc...@gmail.com (2011-11-30)

Trunk DEPS rolled at r1197 and merged to M16 at r1198.

### at...@gmail.com (2011-12-07)

I updated into the newest version from dev-channel. The reprofile I uploaded here doesn't reproduce the crash anymore but if you change the "/BitsPerComponent 242794283153874938024420238" into "/BitsPerComponent 59652324" you will still get on linux side sad-face tab-crash with signal 6 abort. Empty error popup and sad-face tab-crash on Windows side.

### sc...@gmail.com (2011-12-08)

@attekett: yeah, with some sets of values, you'll trigger either an OOM or a psuedo-OOM in an internal calloc()-like function. That's intentional and harmless.


### sc...@gmail.com (2011-12-16)

@attekett: oops, sorry, we missed this one for the M16 release notes. I'll make sure the correct credit is added to the Hall of Fame.
Anyway, again, we can't rule out disclosure of the out-of-bounds content, so happy to issue a $500 Chromium Security Reward :D

---
Blurb omitted since the fix is already live
---

### at...@gmail.com (2011-12-17)

heh. I wondered why this was left out from the Release note. :D Didn't notice that it was still in topanel status. 

Thanks for the reward and hopefully I find something new to report soon. :) 

### sc...@gmail.com (2012-01-31)

Payment in system -- sorry for delay / mess up on this one!

### at...@gmail.com (2012-01-31)

@scarybeasts

If possible it would be better that this payment is paid, after you guys get the two other possible security bugs, I have reported, reviewed. My bank hits me with static amount of expenses on each transaction made in foreign currency. 

### sc...@gmail.com (2012-01-31)

May be too late :(
But, noted. I'll look to batch things aggressively.

### at...@gmail.com (2012-01-31)

No problem. Actually, before the notification mail at morning, I didn't even remember this one. :)

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

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

This issue was migrated from crbug.com/chromium/105714?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051656)*
