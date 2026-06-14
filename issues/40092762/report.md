# Security: Skia: Out-of-bounds Read in src/codec/SkSwizzler

| Field | Value |
|-------|-------|
| **Issue ID** | [40092762](https://issues.chromium.org/issues/40092762) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Skia |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | qu...@gmail.com |
| **Assignee** | sc...@google.com |
| **Created** | 2018-10-18 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

<https://cs.chromium.org/chromium/src/third_party/skia/src/codec/SkSwizzler.cpp?l=54>

```
static void sample6(void\* dst, const uint8_t\* src, int width, int bpp, int deltaSrc, int offset,  
        const SkPMColor ctable[]) {  
    src += offset;  
    uint8_t\* dst8 = (uint8_t\*) dst;  
    for (int x = 0; x < width; x++) {  
        memcpy(dst8, src, 6);  
        dst8 += 6;  
        src += deltaSrc;  
    }  
}  

```

This function doesn't verify `src` memory address before using it.

**VERSION**  

Operating System: Linux  

Skia version: I use latest version in github(<https://github.com/google/skia>), commit <https://github.com/google/skia/commit/d18e14c69e56d400eac1005c49b393152e136b96>

**REPRODUCTION CASE**

Build Skia with asserts disabled

```
bin/gn gen out/Release --args='is_debug=false'  
ninja -C out/Release  

```

Run testcase:

```
./out/Release/fuzz  -t android_codec -b Sk_android_codec_crash  

```

Crash state:

```
=================================================================  
==23559==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7f932775c852 at pc 0x00000066a772 bp 0x7fffe00d5300 sp 0x7fffe00d4ab0  
READ of size 6 at 0x7f932775c852 thread T0  
    #0 0x66a771 in __asan_memcpy /home/brian/final/llvm.src/projects/compiler-rt/lib/asan/asan_interceptors.cc:466:3  
    #1 0xc26687 in sample6(void\*, unsigned char const\*, int, int, int, int, unsigned int const\*) /mnt/data/skia/out/Release-asan/../../src/codec/SkSwizzler.cpp:59:9  
    #2 0xc2ccf0 in SkSwizzler::swizzle(void\*, unsigned char const\*) /mnt/data/skia/out/Release-asan/../../src/codec/SkSwizzler.cpp:1233:5  
    #3 0x12f379f in SkJpegCodec::readRows(SkImageInfo const&, void\*, unsigned long, int, SkCodec::Options const&) /mnt/data/skia/out/Release-asan/../../src/codec/SkJpegCodec.cpp:540:24  
    #4 0x12f5d0d in SkJpegCodec::onGetScanlines(void\*, int, unsigned long) /mnt/data/skia/out/Release-asan/../../src/codec/SkJpegCodec.cpp:753:22  
    #5 0xc18670 in SkCodec::getScanlines(void\*, int, unsigned long) /mnt/data/skia/out/Release-asan/../../src/codec/SkCodec.cpp:517:36  
    #6 0xc21c61 in SkSampledCodec::sampledDecode(SkImageInfo const&, void\*, unsigned long, SkAndroidCodec::AndroidOptions const&) /mnt/data/skia/out/Release-asan/../../src/codec/SkSampledCodec.cpp:290:41  
    #7 0xc20812 in SkSampledCodec::onGetAndroidPixels(SkImageInfo const&, void\*, unsigned long, SkAndroidCodec::AndroidOptions const&) /mnt/data/skia/out/Release-asan/../../src/codec/SkSampledCodec.cpp:87:22  
    #8 0xc123b8 in SkAndroidCodec::getAndroidPixels(SkImageInfo const&, void\*, unsigned long, SkAndroidCodec::AndroidOptions const\*) /mnt/data/skia/out/Release-asan/../../src/codec/SkAndroidCodec.cpp:393:22  
    #9 0x76cadb in FuzzAndroidCodec(sk_sp<SkData>, unsigned char) /mnt/data/skia/out/Release-asan/../../fuzz/oss_fuzz/FuzzAndroidCodec.cpp:33:26  
    #10 0x7092e3 in fuzz_android_codec(sk_sp<SkData>) /mnt/data/skia/out/Release-asan/../../fuzz/FuzzMain.cpp:385:9  
    #11 0x7092e3 in fuzz_file(SkString, SkString) /mnt/data/skia/out/Release-asan/../../fuzz/FuzzMain.cpp:143  
    #12 0x707343 in main /mnt/data/skia/out/Release-asan/../../fuzz/FuzzMain.cpp:110:16  
    #13 0x7f932c3cb82f in __libc_start_main /build/glibc-Cl5G7W/glibc-2.23/csu/../csu/libc-start.c:291  
    #14 0x5e0148 in _start (/mnt/data/skia/out/Release-asan/fuzz+0x5e0148)  
  
0x7f932775c852 is located 82 bytes to the right of 131072-byte region [0x7f932773c800,0x7f932775c800)  
allocated by thread T0 here:  
    #0 0x680be3 in __interceptor_malloc /home/brian/final/llvm.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cc:67:3  
    #1 0xc2f795 in sk_malloc_flags(unsigned long, unsigned int) /mnt/data/skia/out/Release-asan/../../src/ports/SkMemory_malloc.cpp:71:13  
  
SUMMARY: AddressSanitizer: heap-buffer-overflow /home/brian/final/llvm.src/projects/compiler-rt/lib/asan/asan_interceptors.cc:466:3 in __asan_memcpy  
Shadow bytes around the buggy address:  
  0x0ff2e4ee38b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  
  0x0ff2e4ee38c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  
  0x0ff2e4ee38d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  
  0x0ff2e4ee38e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  
  0x0ff2e4ee38f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  
=>0x0ff2e4ee3900: fa fa fa fa fa fa fa fa fa fa[fa]fa fa fa fa fa  
  0x0ff2e4ee3910: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  
  0x0ff2e4ee3920: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  
  0x0ff2e4ee3930: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  
  0x0ff2e4ee3940: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  
  0x0ff2e4ee3950: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  
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
==23559==ABORTING  

```

## Attachments

- [Sk_android_codec_crash](attachments/Sk_android_codec_crash) (text/plain, 2.0 KB)

## Timeline

### me...@chromium.org (2018-10-18)

[Empty comment from Monorail migration]

[Monorail components: Internals>Skia]

### me...@chromium.org (2018-10-18)

The crash doesn't repo on most recent OSS-Fuzz build (ie: not ToT). 
I suspect that means it is just very new.

### in...@chromium.org (2018-10-18)

[Empty comment from Monorail migration]

### kj...@chromium.org (2018-10-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-19)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-10-19)

[Empty comment from Monorail migration]

### sc...@google.com (2018-10-22)

If I run fuzz in Debug mode, I hit an assert in SkSwizzler [1]:

            case SkEncodedInfo::kRGB_Color:
                // We have a png that remains in its original format.
                SkASSERT(16 == encodedInfo.bitsPerComponent());

We get here because SkJpegCodec called CreateSwizzler with skipFormatConversion = true [2]. But we shouldn't want to skip format conversion, because the jpeg only has three components (RGB), and the output wants 4 (including Alpha). I don't know why we ever thought we wanted to skip here.

[1] https://skia.googlesource.com/skia.git/+/07afa23/src/codec/SkSwizzler.cpp#834
[2] https://skia.googlesource.com/skia.git/+/07afa23/src/codec/SkJpegCodec.cpp#669

### sc...@google.com (2018-10-24)

Fix is in https://skia-review.googlesource.com/c/skia/+/164619

### bu...@chromium.org (2018-10-26)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/65f4aeae923d82c39d83e05e0a6c6bc5c25291ab

commit 65f4aeae923d82c39d83e05e0a6c6bc5c25291ab
Author: Leon Scroggins III <scroggo@google.com>
Date: Fri Oct 26 16:40:16 2018

Fix bug decoding JCS_RGB jpeg files

Bug: chromium:897031
Bug: chromium:896776

Prior to this fix, we would treat the output from such a JPEG
as if it were a 16 bit per component RGB PNG. We hit an assert
in debug, but in release mode we do the wrong thing.

Split up SkSwizzler::CreateSwizzler into two public factories
(and a private one) based on whether format conversion is desired.
Without format conversion, we may have already converted (as is
the case with this JPEG), so the SkEncodedInfo::Color is not relevant.
That flavor of the factory just needs to know the bytes per pixel,
so provide that info instead.

Add a test file to Google Storage: apron.jpg, from Chromium's
benchmark files.

Change-Id: If1337d58a508466299f9e4666778727c6cdc879a
Reviewed-on: https://skia-review.googlesource.com/c/164619
Auto-Submit: Leon Scroggins <scroggo@google.com>
Commit-Queue: Mike Klein <mtklein@google.com>
Reviewed-by: Mike Klein <mtklein@google.com>

[modify] https://crrev.com/65f4aeae923d82c39d83e05e0a6c6bc5c25291ab/infra/bots/assets/skimage/VERSION
[modify] https://crrev.com/65f4aeae923d82c39d83e05e0a6c6bc5c25291ab/src/codec/SkRawCodec.cpp
[modify] https://crrev.com/65f4aeae923d82c39d83e05e0a6c6bc5c25291ab/src/codec/SkWbmpCodec.cpp
[modify] https://crrev.com/65f4aeae923d82c39d83e05e0a6c6bc5c25291ab/src/codec/SkHeifCodec.cpp
[modify] https://crrev.com/65f4aeae923d82c39d83e05e0a6c6bc5c25291ab/infra/bots/tasks.json
[modify] https://crrev.com/65f4aeae923d82c39d83e05e0a6c6bc5c25291ab/src/codec/SkBmpStandardCodec.cpp
[modify] https://crrev.com/65f4aeae923d82c39d83e05e0a6c6bc5c25291ab/src/codec/SkWbmpCodec.h
[modify] https://crrev.com/65f4aeae923d82c39d83e05e0a6c6bc5c25291ab/src/codec/SkSwizzler.h
[modify] https://crrev.com/65f4aeae923d82c39d83e05e0a6c6bc5c25291ab/src/codec/SkPngCodec.cpp
[modify] https://crrev.com/65f4aeae923d82c39d83e05e0a6c6bc5c25291ab/src/codec/SkGifCodec.cpp
[modify] https://crrev.com/65f4aeae923d82c39d83e05e0a6c6bc5c25291ab/src/codec/SkJpegCodec.cpp
[modify] https://crrev.com/65f4aeae923d82c39d83e05e0a6c6bc5c25291ab/src/codec/SkSwizzler.cpp


### bu...@chromium.org (2018-10-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5e5ea4b8bc7cfc1ebf9fb536680d895ed2e5efe8

commit 5e5ea4b8bc7cfc1ebf9fb536680d895ed2e5efe8
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Oct 26 22:11:52 2018

Roll src/third_party/skia 7d20bc42f453..63fdd972c866 (20 commits)

https://skia.googlesource.com/skia.git/+log/7d20bc42f453..63fdd972c866


git log 7d20bc42f453..63fdd972c866 --date=short --no-merges --format='%ad %ae %s'
2018-10-26 herb@google.com Combine mask loops in bitmap device
2018-10-26 brianosman@google.com On second thought, remove GrColor4s
2018-10-26 herb@google.com Remove functional part of unique glyphs from the builder
2018-10-26 brianosman@google.com Use SkColor4f functionality, rather than SkPM4f.h inline functions
2018-10-26 halcanary@google.com SkQP/Java: remove unneeded stack trace, count tests correcctly
2018-10-26 halcanary@google.com skqp/.../assets/.gitignore: remove important things
2018-10-26 brianosman@google.com Revert "Remove memory used by unique glyphs"
2018-10-26 brianosman@google.com Remove SkPM4fPriv.h, inline the two functions at call-sites
2018-10-26 skia-autoroll@skia-public.iam.gserviceaccount.com Roll third_party/externals/angle2 e9503ae90a9d..3ce69ba3eb60 (1 commits)
2018-10-26 mtklein@google.com remove RP bench
2018-10-26 mtklein@google.com use Steps in SkSRGBGammaColorFilter
2018-10-26 skia-autoroll@skia-public.iam.gserviceaccount.com Roll third_party/externals/swiftshader 38ff83043a35..50b105973431 (1 commits)
2018-10-26 scroggo@google.com Fix bug decoding JCS_RGB jpeg files
2018-10-26 benjaminwagner@google.com Fix Bazel formatting.
2018-10-26 michaelludwig@google.com Extract per-edge quad vertex tesselation code into reusable interface
2018-10-26 mtklein@google.com add a test for extend range sRGB roundtripping
2018-10-26 csmartdalton@google.com ccpr: Unregister path listeners when their cache entries are evicted
2018-10-26 mtklein@google.com move unspecialized routines out of SkOpts
2018-10-26 scroggo@google.com Reformat public.bzl
2018-10-26 skia-autoroll@skia-public.iam.gserviceaccount.com Roll third_party/externals/swiftshader fde88d96a58b..38ff83043a35 (1 commits)


Created with:
  gclient setdep -r src/third_party/skia@63fdd972c866

The AutoRoll server is located here: https://autoroll.skia.org/r/skia-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.

CQ_INCLUDE_TRYBOTS=luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux-chromeos-compile-dbg;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;master.tryserver.blink:linux_trusty_blink_rel

BUG=chromium:897031,chromium:896776
TBR=brianosman@chromium.org

Change-Id: Ie2a6213901c7888513732bbe5b6ab8c59b9af155
Reviewed-on: https://chromium-review.googlesource.com/c/1302703
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#603213}
[modify] https://crrev.com/5e5ea4b8bc7cfc1ebf9fb536680d895ed2e5efe8/DEPS


### sc...@google.com (2018-10-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-31)

[Empty comment from Monorail migration]

### sc...@google.com (2018-11-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-11-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-11-12)

hi quangnh89@, the VRP panel awarded $1,000 for this bug, cheers!

### qu...@gmail.com (2018-11-12)

Thank you very much! I do appreciate it. :)

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/896776?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/897031]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092762)*
