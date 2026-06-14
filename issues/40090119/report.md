# Stack-buffer-overflow in SkPackBits::Unpack8

| Field | Value |
|-------|-------|
| **Issue ID** | [40090119](https://issues.chromium.org/issues/40090119) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Skia |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | jo...@gmail.com |
| **Assignee** | re...@google.com |
| **Created** | 2018-01-08 |
| **Bounty** | $1,500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36

Steps to reproduce the problem:
1. build https://chromium.googlesource.com/chromium/src/+/65.0.3311.3
2. run ./filter_fuzz_stub path/to/poc

What is the expected behavior?
crashed by asan and report stack-buffer-overflow

What went wrong?
Summarize
======================================
Lack of the checking of src buffer remain in SkPackBits::Unpack8

Debug information
======================================
Breakpoint 2, SkPackBits::Unpack8 (
    src=0x7fffffffb680 "\377\036<\242\025B\023U&\212\363+\252\212\305\302N_l\310~\251jpϧ\324\345\351\347:\020r.;@\311\361\222\244\326z*\200\004\357CRN\257\032\314X\204<(,\020\r\025\370G%jua\252?R<\343)\266\r\251\272\374\354\fK\234&", srcSize=1273, dst=0x7fffffffb280 "0\263\377\377\377\177", dstSize=1024) at ../../src/third_party/skia/src/effects/SkPackBits.cpp:83
warning: Source file is more recent than executable.
83      uint8_t* const origDst = dst;
(gdb) p/x src
$22 = 0x7fffffffb680
(gdb) p/x srcSize
$23 = 0x4f9
(gdb) p/x dst
$24 = 0x7fffffffb280
(gdb) p/x dstSize
$25 = 0x400
(gdb) info b 3
Num     Type           Disp Enb Address            What
3       breakpoint     keep y   0x00007ffff718fdc9 in SkPackBits::Unpack8(uint8_t const* restrict, size_t, uint8_t* restrict, size_t) at ../../src/third_party/skia/src/effects/SkPackBits.cpp:100
    breakpoint already hit 2 times
        p/x dst
        p/x dstSize
        p/x src
        p/x srcSize
        p/x n
        c
Breakpoint 3, SkPackBits::Unpack8 (
    src=0x7fffffffb681 "\036<\242\025B\023U&\212\363+\252\212\305\302N_l\310~\251jpϧ\324\345\351\347:\020r.;@\311\361\222\244\326z*\200\004\357CRN\257\032\314X\204<(,\020\r\025\370G%jua\252?R<\343)\266\r\251\272\374\354\fK\234&", srcSize=1273, dst=0x7fffffffb280 "0\263\377\377\377\177", dstSize=1024) at ../../src/third_party/skia/src/effects/SkPackBits.cpp:100
100             memcpy(dst, src, n);
$26 = 0x7fffffffb280
$27 = 0x400
$28 = 0x7fffffffb681
$29 = 0x4f9
$30 = 0x80

Breakpoint 3, SkPackBits::Unpack8 (src=0x7fffffffbb2c "\377\377\377", srcSize=1273, dst=0x7fffffffb515 "\020", dstSize=1024) at ../../src/third_party/skia/src/effects/SkPackBits.cpp:100
100             memcpy(dst, src, n);
$31 = 0x7fffffffb515
$32 = 0x400
$33 = 0x7fffffffbb2c
$34 = 0x4f9
$35 = 0x68

Breakpoint 4, SkPackBits::Unpack8 (src=0x7fffffffbb94 "\377\177", srcSize=1273, dst=0x7fffffffb57d "\020", dstSize=1024) at ../../src/third_party/skia/src/effects/SkPackBits.cpp:105
105     SkASSERT(src <= stop);
(gdb) p src
$36 = (const uint8_t * restrict) 0x7fffffffbb94 "\377\177"
(gdb) p stop
$37 = (const uint8_t *) 0x7fffffffbb79 "n\365\366\377\177"

Source code analysis
=======================================
SkPackBits.cpp:[SkPackBits::Unpack8]
......
    while (src < stop) {
        unsigned n = *src++;
        if (n <= 127) {   // repeat count (n + 1)
            n += 1;
            if (dst >(endDst - n)) {         <= Lack of the checking of src buffer remain
                return 0;
            }
            memset(dst, *src++, n);          <= Stack-buffer-overflow may also happen here
        } else {    // same count (n - 127)
            n -= 127;
            if (dst > (endDst - n)) {        <= Lack of the checking of src buffer remain
                return 0;
            }
            memcpy(dst, src, n);             <= Stack-buffer-overflow occured here with the my poc
            src += n;
        }
        dst += n;
    }

You can fix the issue like this
=======================================
--- a/src/effects/SkPackBits.cpp
+++ b/src/effects/SkPackBits.cpp
@@ -88,13 +88,13 @@ int SkPackBits::Unpack8(const uint8_t* SK_RESTRICT src, size_t srcSize,
         unsigned n = *src++;
         if (n <= 127) {   // repeat count (n + 1)
             n += 1;
-            if (dst >(endDst - n)) {
+            if ((dst >(endDst - n)) || (src >(stop - n))) {
                 return 0;
             }
             memset(dst, *src++, n);
         } else {    // same count (n - 127)
             n -= 127;
-            if (dst > (endDst - n)) {
+            if ((dst >(endDst - n)) || (src >(stop - n))) {
                 return 0;
             }
             memcpy(dst, src, n);

Did this work before? N/A 

Chrome version: 65.0.3311.3  Channel: dev
OS Version: Ubuntu 16.04.3 LTS X64
Flash Version: 

[0108/213023.617127:INFO:filter_fuzz_stub.cc(61)] Test case: path/to/poc
=================================================================
==24057==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7fef05f02520 at pc 0x0000005f0399 bp 0x7ffd164d5f20 sp 0x7ffd164d56d0
READ of size 104 at 0x7fef05f02520 thread T0
    #0 0x5f0398 in __asan_memcpy /b/build/slave/linux_upload_clang/build/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors_memintrinsics.cc:23:3
    #1 0xd1a94d in SkPackBits::Unpack8(unsigned char const*, unsigned long, unsigned char*, unsigned long) src/third_party/skia/src/effects/SkPackBits.cpp:100:13
    #2 0xd158ee in SkTable_ColorFilter::CreateProc(SkReadBuffer&) src/third_party/skia/src/effects/SkTableColorFilter.cpp:208:27
    #3 0xaa3b79 in SkReadBuffer::readFlattenable(SkFlattenable::Type) src/third_party/skia/src/core/SkReadBuffer.cpp:407:15
    #4 0xd7ec01 in readFlattenable<SkColorFilter> src/third_party/skia/src/core/SkReadBuffer.h:141:35
    #5 0xd7ec01 in readColorFilter src/third_party/skia/src/core/SkReadBuffer.h:143
    #6 0xd7ec01 in SkColorFilterImageFilter::CreateProc(SkReadBuffer&) src/third_party/skia/src/effects/SkColorFilterImageFilter.cpp:53
    #7 0xaa3b79 in SkReadBuffer::readFlattenable(SkFlattenable::Type) src/third_party/skia/src/core/SkReadBuffer.cpp:407:15
    #8 0x9bf75e in readFlattenable<SkImageFilter> src/third_party/skia/src/core/SkReadBuffer.h:141:35
    #9 0x9bf75e in readImageFilter src/third_party/skia/src/core/SkReadBuffer.h:145
    #10 0x9bf75e in SkImageFilter::Common::unflatten(SkReadBuffer&, int) src/third_party/skia/src/core/SkImageFilter.cpp:130
    #11 0xcfadfa in SkTileImageFilter::CreateProc(SkReadBuffer&) src/third_party/skia/src/effects/SkTileImageFilter.cpp:147:5
    #12 0xaa3b79 in SkReadBuffer::readFlattenable(SkFlattenable::Type) src/third_party/skia/src/core/SkReadBuffer.cpp:407:15
    #13 0x9bacd3 in SkFlattenable::Deserialize(SkFlattenable::Type, void const*, unsigned long, SkDeserialProcs const*) src/third_party/skia/src/core/SkFlattenable.cpp:145:40
    #14 0x9baf53 in Deserialize src/third_party/skia/include/core/SkImageFilter.h:241:5
    #15 0x9baf53 in SkValidatingDeserializeImageFilter(void const*, unsigned long) src/third_party/skia/src/core/SkFlattenableSerialization.cpp:22
    #16 0x61efc0 in RunTestCase src/skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:33:38
    #17 0x61efc0 in ReadAndRunTestCase src/skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:67
    #18 0x61efc0 in main src/skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:87
    #19 0x7fef091dd82f in __libc_start_main /build/glibc-bfm8X4/glibc-2.23/csu/../csu/libc-start.c:291
Address 0x7fef05f02520 is located in stack of thread T0 at offset 1312 in frame
    #0 0xd156ef in SkTable_ColorFilter::CreateProc(SkReadBuffer&) src/third_party/skia/src/effects/SkTableColorFilter.cpp:193
  This frame has 2 object(s):
    [32, 1312) 'packedStorage' (line 198) <== Memory access at offset 1312 overflows this variable
    [1440, 2464) 'unpackedStorage' (line 207)
HINT: this may be a false positive if your program uses some custom stack unwind mechanism or swapcontext
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-buffer-overflow /b/build/slave/linux_upload_clang/build/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors_memintrinsics.cc:23:3 in __asan_memcpy
Shadow bytes around the buggy address:
  0x0ffe60bd8450: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ffe60bd8460: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ffe60bd8470: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ffe60bd8480: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ffe60bd8490: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0ffe60bd84a0: 00 00 00 00[f2]f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2
  0x0ffe60bd84b0: f2 f2 f2 f2 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ffe60bd84c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ffe60bd84d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ffe60bd84e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ffe60bd84f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==24057==ABORTING

## Attachments

- [skia_sbof.poc](attachments/skia_sbof.poc) (application/octet-stream, 3.4 KB)
- [skia_sbof.diff](attachments/skia_sbof.diff) (application/octet-stream, 781 B)

## Timeline

### jo...@gmail.com (2018-01-08)

It can also be reproduced in other Channel，like the latest stable 63.0.3239.84(test on asan-linux-stable-63.0.3239.84)

### el...@chromium.org (2018-01-08)

[Empty comment from Monorail migration]

[Monorail components: Internals>Skia]

### cl...@chromium.org (2018-01-08)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6263432109359104.

### me...@chromium.org (2018-01-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-01-09)

Detailed report: https://clusterfuzz.com/testcase?key=6263432109359104

Job Type: linux_asan_filter_fuzz_stub
Crash Type: Stack-buffer-overflow READ {*}
Crash Address: 0x7f3b615bcd20
Crash State:
  SkPackBits::Unpack8
  SkTable_ColorFilter::CreateProc
  SkReadBuffer::readFlattenable
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_filter_fuzz_stub&range=480432:480486

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6263432109359104

See https://github.com/google/clusterfuzz-tools for more information.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.


### cl...@chromium.org (2018-01-09)

Automatically assigning owner based on suspected regression changelist https://skia.googlesource.com/skia/+/0bdaf05fc17ebe5d4ad01d70c80df2425e83c737 (remove unused mode parameter from SkMergeImageFilter).

If this is incorrect, please remove the owner and apply the Test-Predator-Wrong-CLs label.

### sh...@chromium.org (2018-01-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-09)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-01-09)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/fca3d0aba5a7d17dbf97082b6837e31ff2808b4f

commit fca3d0aba5a7d17dbf97082b6837e31ff2808b4f
Author: Mike Reed <reed@google.com>
Date: Tue Jan 09 20:41:17 2018

check for bad buffers in Unpack8

Bug:799918
Change-Id: I0502a487d67ce757bf818823cf0ad46b7703294c
Reviewed-on: https://skia-review.googlesource.com/92841
Commit-Queue: Mike Reed <reed@google.com>
Reviewed-by: Florin Malita <fmalita@chromium.org>

[modify] https://crrev.com/fca3d0aba5a7d17dbf97082b6837e31ff2808b4f/src/effects/SkPackBits.cpp
[modify] https://crrev.com/fca3d0aba5a7d17dbf97082b6837e31ff2808b4f/src/effects/SkPackBits.h


### cl...@chromium.org (2018-01-12)

ClusterFuzz has detected this issue as fixed in range 528693:528695.

Detailed report: https://clusterfuzz.com/testcase?key=6263432109359104

Job Type: linux_asan_filter_fuzz_stub
Crash Type: Stack-buffer-overflow READ {*}
Crash Address: 0x7f3b615bcd20
Crash State:
  SkPackBits::Unpack8
  SkTable_ColorFilter::CreateProc
  SkReadBuffer::readFlattenable
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_filter_fuzz_stub&range=480432:480486
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_filter_fuzz_stub&range=528693:528695

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6263432109359104

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2018-01-12)

ClusterFuzz testcase 6263432109359104 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2018-01-12)

[Empty comment from Monorail migration]

### aw...@google.com (2018-01-16)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### aw...@google.com (2018-01-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-01-29)

Congrats! The VRP panel looked at this and decided to award $1,000, with an additional $500 for supplying the patch we used.

Also, how would you like to be credited in the Chrome release notes?

### aw...@chromium.org (2018-01-29)

[Empty comment from Monorail migration]

### jo...@gmail.com (2018-02-03)

Thanks for your information.
Please credit this to Wanglu & Yangkang(@dnpushme) of Qihoo360 Qex Team.

### sh...@chromium.org (2018-02-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-09)

This bug requires manual review: M65 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), bhthompson@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-02-09)

[Bulk Edit]

+awhalley@ (Security TPM) for M65 merge review

### aw...@google.com (2018-02-09)

govind@ - Good for 65.

### go...@chromium.org (2018-02-09)

Approving merge to M65 branch 3325 based on https://crbug.com/chromium/799918#c23. Please merge ASAP so we can pick it up for next week Beta release. Thank you.

### sh...@chromium.org (2018-02-12)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### re...@google.com (2018-02-12)

fix already in chrome/m65

### go...@chromium.org (2018-02-12)

Removing "Merge-Approved-65" label per https://crbug.com/chromium/799918#c26. Thank you.

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-11-14)

[Empty comment from Monorail migration]

### is...@google.com (2018-11-14)

This issue was migrated from crbug.com/chromium/799918?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090119)*
