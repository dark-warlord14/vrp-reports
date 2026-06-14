# Heap-use-after-free in FT_New_Size

| Field | Value |
|-------|-------|
| **Issue ID** | [40083759](https://issues.chromium.org/issues/40083759) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Canvas, Internals>Skia |
| **CVE IDs** | CVE-2016-1680 |
| **Reporter** | at...@gmail.com |
| **Assignee** | bu...@chromium.org |
| **Created** | 2016-02-25 |
| **Bounty** | $3,000.00 |

## Description



Tested on: 


Chromium: linux-release-asan-symbolized-linux-release-377548
OS: Ubuntu 14.04

Repro-file as an attachment.

ASAN-trace:

==16790==ERROR: AddressSanitizer: heap-use-after-free on address 0x61a000015130 at pc 0x7f22018a3ab2 bp 0x7ffdeb2c3310 sp 0x7ffdeb2c3308
READ of size 8 at 0x61a000015130 thread T0 (chrome)
    #0 0x7f22018a3ab1 in FT_New_Size /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/freetype2/src/src/base/ftobjs.c:2434
    #1 0x560510dbf4fa in SkScalerContext_FreeType::SkScalerContext_FreeType(SkTypeface*, SkDescriptor const*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/ports/SkFontHost_FreeType.cpp:886 (discriminator 1)
    #2 0x560510dbdd18 in SkTypeface_FreeType::onCreateScalerContext(SkDescriptor const*) const /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/ports/SkFontHost_FreeType.cpp:666 (discriminator 1)
    #3 0x560510746318 in SkTypeface::createScalerContext(SkDescriptor const*, bool) const /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/core/SkScalerContext.cpp:871 (discriminator 1)
    #4 0x560510635768 in SkGlyphCache::VisitCache(SkTypeface*, SkDescriptor const*, bool (*)(SkGlyphCache const*, void*), void*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/core/SkGlyphCache.cpp:548
    #5 0x5605106aa5f7 in DetachDescProc(SkTypeface*, SkDescriptor const*, void*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/core/SkPaint.cpp:457
    #6 0x5605106a5739 in SkPaint::descriptorProc(SkSurfaceProps const*, SkPaint::FakeGamma, SkMatrix const*, void (*)(SkTypeface*, SkDescriptor const*, void*), void*) const /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/core/SkPaint.cpp:1742
    #7 0x5605106aa54a in SkPaint::detachCache(SkSurfaceProps const*, SkPaint::FakeGamma, SkMatrix const*) const /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/core/SkPaint.cpp:1749
    #8 0x56051061b757 in SkAutoGlyphCache::SkAutoGlyphCache(SkPaint const&, SkSurfaceProps const*, SkPaint::FakeGamma, SkMatrix const*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/core/SkGlyphCache.h:294
.
.
.
0x61a000015130 is located 176 bytes inside of 1384-byte region [0x61a000015080,0x61a0000155e8)
freed by thread T0 (chrome) here:
    #0 0x56050d9bb8fb in __interceptor_free ??:?
    #1 0x560510f34259 in sk_free(void*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../skia/ext/SkMemory_new_handler.cpp:42
    #2 0x7f2201898ed2 in ft_mem_free /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/freetype2/src/src/base/ftutil.c:171
    #3 0x7f22018a3dae in FT_Done_Face /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/freetype2/src/src/base/ftobjs.c:2403
    #4 0x7f22018b2939 in FT_Done_Library /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/freetype2/src/src/base/ftobjs.c:4612
    #5 0x560510dca66c in FreeTypeLibrary::~FreeTypeLibrary() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/ports/SkFontHost_FreeType.cpp:122
    #6 0x560510dbe4c7 in unref_ft_library() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/ports/SkFontHost_FreeType.cpp:175 (discriminator 1)
    #7 0x560510dc0bca in SkScalerContext_FreeType::~SkScalerContext_FreeType() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/ports/SkFontHost_FreeType.cpp:945
    #8 0x560510dc0f6a in SkScalerContext_FreeType::~SkScalerContext_FreeType() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/ports/SkFontHost_FreeType.cpp:934
    #9 0x560510632079 in SkGlyphCache::~SkGlyphCache() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/core/SkGlyphCache.cpp:61 (discriminator 1)
    #10 0x560510635021 in SkGlyphCache_Globals::internalPurge(unsigned long) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/core/SkGlyphCache.cpp:706 (discriminator 1)
.
.
.
previously allocated by thread T0 (chrome) here:
    #0 0x56050d9bbc1b in __interceptor_malloc ??:?
    #1 0x560510f342ca in sk_malloc_throw(unsigned long) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../skia/ext/SkMemory_new_handler.cpp:58
    #2 0x7f22018beac5 in ft_mem_qalloc /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/freetype2/src/src/base/ftutil.c:76
    #3 0x7f2201898998 in ft_mem_alloc /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/freetype2/src/src/base/ftutil.c:55 (discriminator 1)
    #4 0x7f22018a1ccb in open_face /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/freetype2/src/src/base/ftobjs.c:1122
    #5 0x7f22018a011c in FT_Open_Face /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/freetype2/src/src/base/ftobjs.c:2126
    #6 0x560510dc00da in ref_ft_face(SkTypeface const*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/ports/SkFontHost_FreeType.cpp:336 (discriminator 4)
    #7 0x560510dbefc0 in SkScalerContext_FreeType::SkScalerContext_FreeType(SkTypeface*, SkDescriptor const*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/ports/SkFontHost_FreeType.cpp:799
.
.
.


## Attachments

- [chrome-heap-use-after-free-FTNewSize10-min.html](attachments/chrome-heap-use-after-free-FTNewSize10-min.html) (text/plain, 591 B)

## Timeline

### cl...@chromium.org (2016-02-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5643000593514496

### oc...@chromium.org (2016-02-25)

(Looks like this was first found by an internal fuzzer 3 days ago: https://cluster-fuzz.appspot.com/testcase?key=5703584043237376)

### cl...@chromium.org (2016-02-25)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5703584043237376

Fuzzer: inferno_canvas_wrecker
Job Type: linux_asan_chrome_gpu
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61a000018130
Crash State:
  FT_New_Size
  SkScalerContext_FreeType::SkScalerContext_FreeType
  SkTypeface_FreeType::onCreateScalerContext
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_gpu&range=376399:376730

Minimized Testcase (0.66 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96ZGzLe_35Wk_9Fm-sYD769RRcvlbTTEHtEIp7zPKX2tw36ur8eLOcipj3JztCmynFZX8RpdK7nfv4xSXSlLtBX6amqrvQrmydHBD6n-2DkbGDbTpd4c6SWGEhFMD-bWtbWwnTbBJKvkqqadLAKTcJxjLgKaQ

Filer: ochang

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### oc...@chromium.org (2016-02-25)

herb, mind taking a look at this one, or with finding a suitable owner? 

The UaF appears to happening in this sequence in SkGlyphCache* SkGlyphCache::VisitCache:

    // Check if we can create a scaler-context before creating the glyphcache.
    // If not, we may have exhausted OS/font resources, so try purging the
    // cache once and try again.
    {
        // pass true the first time, to notice if the scalercontext failed,
        // so we can try the purge.
        SkScalerContext* ctx = typeface->createScalerContext(desc, true);
        if (!ctx) {
            get_globals().purgeAll();                                  *--> leads to unref_ft_library() -> FT_Done_Face
            ctx = typeface->createScalerContext(desc, false);          *--> leads to freed face being passed to FT_New_Size
            SkASSERT(ctx);
        }
        cache = new SkGlyphCache(typeface, desc, ctx);
    }





[Monorail components: Blink>Canvas Internals>Skia]

### cl...@chromium.org (2016-02-25)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5643000593514496

Uploader: ochang@google.com
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61a000017b30
Crash State:
  FT_New_Size
  SkScalerContext_FreeType::SkScalerContext_FreeType
  SkTypeface_FreeType::onCreateScalerContext
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=376399:376730

Minimized Testcase (0.47 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94jetq1n8TCLG-IPrbOR6FfqUsLHx3jUAmNAHhmjWF2Ghk0iDlEQQ73OigRcf8j5Fo4Qebh58ygFvSabprVipY0-IgBAtBm3BYmTVcjj-Y1tmwQQJQR_IxjADBakr_kVk6CyHqBxX5SQx5dF6TQ2pMyPUokKg

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### cl...@chromium.org (2016-02-29)

ClusterFuzz has detected this testcase as flaky and is unable to reproduce it in the original crash revision. Skipping fixed testing check and marking it as potentially fixed.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5703584043237376

Fuzzer: inferno_canvas_wrecker
Job Type: linux_asan_chrome_gpu
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61a000018130
Crash State:
  FT_New_Size
  SkScalerContext_FreeType::SkScalerContext_FreeType
  SkTypeface_FreeType::onCreateScalerContext
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_gpu&range=376399:376730

Minimized Testcase (0.66 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96ZGzLe_35Wk_9Fm-sYD769RRcvlbTTEHtEIp7zPKX2tw36ur8eLOcipj3JztCmynFZX8RpdK7nfv4xSXSlLtBX6amqrvQrmydHBD6n-2DkbGDbTpd4c6SWGEhFMD-bWtbWwnTbBJKvkqqadLAKTcJxjLgKaQ

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2016-02-29)

[Empty comment from Monorail migration]

### oc...@chromium.org (2016-02-29)

[Empty comment from Monorail migration]

### be...@google.com (2016-02-29)

[Empty comment from Monorail migration]

### bu...@google.com (2016-02-29)

ochang: I have a question about https://crbug.com/chromium/589848#c4, did you isolate this code by reproducing locally and noting what was happening? I'm most interested in if you got this to reproduce. The reason I ask is that I'm having a difficult time reproducing locally; if this is actually failing at the code noted in https://crbug.com/chromium/589848#c4 then something is probably already quite wrong, as there are few reasons for the scaler context creation to fail at this point (especially on Linux).

### oc...@chromium.org (2016-02-29)

bungeman, yes I can reproduce this on a local build with the testcase in #1, and in #3. Are you trying this on an ASan build of Chrome? 

I actually based on the #4 on the use/free stacks in the ASan report, not from running it though.

### oc...@chromium.org (2016-02-29)

s/testcase in #1/testcase provided by the reporter/

### bu...@google.com (2016-03-01)

I can reproduce, and can reproduce in a local build. I should have more details soon. 

Let me take this opportunity to curse -gline-tables-only and that it overrides just about everything else. It took me quite some time to figure out why my debug asan build had no locals.

### cl...@chromium.org (2016-03-01)

ClusterFuzz has detected this issue as fixed in range 378207:378422.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5643000593514496

Uploader: ochang@google.com
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61a000017b30
Crash State:
  FT_New_Size
  SkScalerContext_FreeType::SkScalerContext_FreeType
  SkTypeface_FreeType::onCreateScalerContext
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=376399:376730
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=378207:378422

Minimized Testcase (0.47 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94jetq1n8TCLG-IPrbOR6FfqUsLHx3jUAmNAHhmjWF2Ghk0iDlEQQ73OigRcf8j5Fo4Qebh58ygFvSabprVipY0-IgBAtBm3BYmTVcjj-Y1tmwQQJQR_IxjADBakr_kVk6CyHqBxX5SQx5dF6TQ2pMyPUokKg

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### bu...@chromium.org (2016-03-01)

The following revision refers to this bug:
  https://skia.googlesource.com/skia.git/+/aabd71cc2c3313c51e618224426045f8573e69e6

commit aabd71cc2c3313c51e618224426045f8573e69e6
Author: bungeman <bungeman@google.com>
Date: Tue Mar 01 23:15:09 2016

SkFontHost_FreeType constructor to correctly release resources.

BUG=chromium:589848

Review URL: https://codereview.chromium.org/1751883004

[modify] https://crrev.com/aabd71cc2c3313c51e618224426045f8573e69e6/src/ports/SkFontHost_FreeType.cpp


### oc...@chromium.org (2016-03-01)

Thanks for fixing this, bungeman!

### cl...@chromium.org (2016-03-10)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2016-05-24)

Regressed then fixed over M50 branch point - this regression may have shipped with M50 stable. Updating impact.

### ti...@google.com (2016-05-25)

Hey Atte - $3,000 for this report - congrats!

I'll add this in the next payment run.

CVE-ID is CVE-2016-1680

### sh...@chromium.org (2016-06-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2016-07-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/589848?no_tracker_redirect=1

[Multiple monorail components: Blink>Canvas, Internals>Skia]
[Monorail mergedwith: crbug.com/chromium/590622]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083759)*
