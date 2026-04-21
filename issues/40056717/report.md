# Security: a READ memory access in jsimd_huff_encode_one_block_sse2

| Field | Value |
|-------|-------|
| **Issue ID** | [40056717](https://issues.chromium.org/issues/40056717) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P3 |
| **Component** | Internals>Images>Codecs |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | mu...@gmail.com |
| **Assignee** | jo...@arm.com |
| **Created** | 2021-07-29 |
| **Bounty** | $5,000.00 |

## Description

# VULNERABILITY DETAILS

a READ memory access in jsimd\_huff\_encode\_one\_block\_sse2

# VERSION

commit: 84d6306f64afd189de148ff13895537a24a55dd3  

git repo:<https://github.com/libjpeg-turbo/libjpeg-turbo>

# REPRODUCTION CASE

./jpegtran(-static) -outfile x @@

There are four different situations at runtime:

## jpegtran with ASAN

./jpegtran -outfile x ./testcase

```
Corrupt JPEG data: 1 extraneous bytes before marker 0xda  
AddressSanitizer:DEADLYSIGNAL  
=================================================================  
==96684==ERROR: AddressSanitizer: SEGV on unknown address 0x7fb6e2dc70a0 (pc 0x7fb6e2d6fdf4 bp 0x00000000fe80 sp 0x7ffef62ea720 T0)                                                                                                         
==96684==The signal is caused by a READ memory access.                                                                 
    #0 0x7fb6e2d6fdf4 in jsimd_huff_encode_one_block_sse2 (/home/kali/libjpeg-turbo/memtest/libjpeg.so.62+0x142df4)  
  
AddressSanitizer can not provide additional info.  
SUMMARY: AddressSanitizer: SEGV (/home/kali/libjpeg-turbo/memtest/libjpeg.so.62+0x142df4) in jsimd_huff_encode_one_block_sse2  
==96684==ABORTING  

```
## jpegtran without compiler and linker flags

./jpegtran -outfile x ./testcase

normal operation

## jpegtran-static with ASAN

./jpegtran-static -outfile x ./testcase

normal operation

## jpegtran-static without compiler and linker flags

./jpegtran-static -outfile x ./testcase

```
Corrupt JPEG data: 1 extraneous bytes before marker 0xda  
zsh: segmentation fault  ../debug/jpegtran-static -outfile mmm ../memtest/plot/crash/0005  

```

segmentation fault at jsimd\_huff\_encode\_one\_block\_sse2()

**CREDIT INFORMATION**

Xu Hanyu and Lu Yutao from Panguite-Forensics-Lab of Qianxin

## Attachments

- [0005](attachments/0005) (text/plain, 324 B)

## Timeline

### [Deleted User] (2021-07-29)

[Empty comment from Monorail migration]

### me...@chromium.org (2021-07-29)

 jonathan.wright, could you please take a look at this one as well? Is this also in unreachable code as in https://crbug.com/chromium/1231868?

### me...@chromium.org (2021-07-29)

(Actually assigning the bug)

### me...@chromium.org (2021-07-30)

Tentatively adding labels. Low severity as this is a single byte read.

[Monorail components: Internals>Images>Codecs]

### [Deleted User] (2021-07-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-30)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jo...@arm.com (2021-08-03)

This bug seems a bit more worrying as there's a crash inside the libjpeg.so - which shouldn't happen, regardless of the data fed into it.

On further investigation, the bug causing the crash is only present on x86_64 platforms - I could not reproduce the crash on AArch64 Linux or Apple Silicon MacOS when building libjpeg-turbo in either Debug or Release modes.

Digging further into the x86_64 Linux builds, things get interesting:

For Release builds, "./jpegtran -outfile x ./testcase" and "./jpegtran-static -outfile x ./testcase" both result in a segfault.

For Debug builds, however, "./jpegtran -outfile x ./testcase" does not result in a crash, while "./jpegtran-static -outfile x ./testcase" does.

Running under GDB to figure out what's happening:

For Release builds, "./jpegtran -outfile x ./testcase" results in a segfault but "./jpegtran-static -outfile x ./testcase" does *not*.

For Debug builds, *neither* "./jpegtran -outfile x ./testcase" nor "./jpegtran-static -outfile x ./testcase" result in a crash.

The most information I can get out of GDB for a Release build is:

Program received signal SIGSEGV, Segmentation fault.
0x00007ffff7f7b694 in jsimd_huff_encode_one_block_sse2 ()
   from /chromium/x86-build-libjpeg-turbo/x86-build/libjpeg.so.62
(gdb) bt
#0  0x00007ffff7f7b694 in jsimd_huff_encode_one_block_sse2 ()
   from /chromium/x86-build-libjpeg-turbo/x86-build/libjpeg.so.62
#1  0x000055555557ba00 in ?? ()
#2  0x0000000000000000 in ?? ()

---

It seems we have a classic Heisenbug on our hands... I'll report it to the upstream project maintainer to see if he can offer any assistance.

### jo...@arm.com (2021-08-03)

Reported to the upstream project.[1] 

[1] https://github.com/libjpeg-turbo/libjpeg-turbo/issues/543

### [Deleted User] (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-08-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/deps/libjpeg_turbo/+/ff19e5b2e176c61d552f68768e0e051867745321

commit ff19e5b2e176c61d552f68768e0e051867745321
Author: Jonathan Wright <jonathan.wright@arm.com>
Date: Mon Aug 09 09:09:36 2021

Update libjpeg-turbo to 2.1.1 stable release

Notable changes include a fix for a crash in the 64-bit SSE2 Huffman
encoder.

Bug: 1234259
Change-Id: Id764c5d8485f095a693504580d9ad81ba860d3ae

[modify] https://crrev.com/ff19e5b2e176c61d552f68768e0e051867745321/ChangeLog.md
[modify] https://crrev.com/ff19e5b2e176c61d552f68768e0e051867745321/README.chromium
[modify] https://crrev.com/ff19e5b2e176c61d552f68768e0e051867745321/jconfig.h
[modify] https://crrev.com/ff19e5b2e176c61d552f68768e0e051867745321/jconfigint.h
[modify] https://crrev.com/ff19e5b2e176c61d552f68768e0e051867745321/jcphuff.c
[modify] https://crrev.com/ff19e5b2e176c61d552f68768e0e051867745321/jdhuff.c
[modify] https://crrev.com/ff19e5b2e176c61d552f68768e0e051867745321/jmemmgr.c
[modify] https://crrev.com/ff19e5b2e176c61d552f68768e0e051867745321/jpegint.h
[modify] https://crrev.com/ff19e5b2e176c61d552f68768e0e051867745321/jpegtran.1
[modify] https://crrev.com/ff19e5b2e176c61d552f68768e0e051867745321/jpegtran.c
[modify] https://crrev.com/ff19e5b2e176c61d552f68768e0e051867745321/simd/x86_64/jchuff-sse2.asm
[modify] https://crrev.com/ff19e5b2e176c61d552f68768e0e051867745321/transupp.c
[modify] https://crrev.com/ff19e5b2e176c61d552f68768e0e051867745321/transupp.h
[modify] https://crrev.com/ff19e5b2e176c61d552f68768e0e051867745321/turbojpeg.c
[modify] https://crrev.com/ff19e5b2e176c61d552f68768e0e051867745321/usage.txt


### gi...@appspot.gserviceaccount.com (2021-08-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/98907227c199b72fcfa1e179f0c1d528fa17e093

commit 98907227c199b72fcfa1e179f0c1d528fa17e093
Author: Jonathan Wright <jonathan.wright@arm.com>
Date: Tue Aug 10 17:25:06 2021

Roll src/third_party/libjpeg_turbo/ ad8b3b0f8..ff19e5b2e (1 commit)

https://chromium.googlesource.com/chromium/deps/libjpeg_turbo.git/+log/ad8b3b0f84ba..ff19e5b2e176

$ git log ad8b3b0f8..ff19e5b2e --date=short --no-merges --format='%ad %ae %s'
2021-08-09 jonathan.wright Update libjpeg-turbo to 2.1.1 stable release

Created with:
  roll-dep src/third_party/libjpeg_turbo

Bug: 1234259
Change-Id: I352f4b4fec2433e958c4ff076ee9441f2bcc0105
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3085668
Commit-Queue: Leon Scroggins <scroggo@google.com>
Auto-Submit: Jonathan Wright <jonathan.wright@arm.com>
Reviewed-by: Leon Scroggins <scroggo@google.com>
Cr-Commit-Position: refs/heads/master@{#910376}

[modify] https://crrev.com/98907227c199b72fcfa1e179f0c1d528fa17e093/DEPS


### jo...@arm.com (2021-08-10)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-09-20)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-21)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-09-28)

Congratulations, Xu Hanyu and Lu Yutao! The VRP Panel has decided to award you $5,000 for this report. A member of our finance team will be in touch in the coming days to arrange payment. Thank you for this report and nice work! 

### am...@google.com (2021-10-01)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-11-16)

This issue was migrated from crbug.com/chromium/1234259?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056717)*
