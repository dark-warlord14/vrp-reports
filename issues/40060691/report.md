# Security: PDFium OOB Write in OpenJPEG due to a missed patch

| Field | Value |
|-------|-------|
| **Issue ID** | [40060691](https://issues.chromium.org/issues/40060691) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2022-08-27 |
| **Bounty** | $7,000.00 |

## Description

# **VULNERABILITY DETAILS**

1. Components: Internals>Plugins>PDF
2. Description: The OpenJPEG code in PDFium missed a patch which addressed a heap buffer overflow vulnerability. The attached proof-of-concept file poc.pdf could trigger OOB write in pdfium\_test.exe.
3. PDFium version: <https://pdfium.googlesource.com/pdfium/+/ef51a2d87a6ac68c74dbbbece1e968edb1a4c20f>
4. ASAN output:

==11644==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x1286146a16e7 at pc 0x7ff68f775c13 bp 0x0074aa0fd7e0 sp 0x0074aa0fd820  

WRITE of size 4752 at 0x1286146a16e7 thread T0  

#0 0x7ff68f775c12 in \_\_asan\_memset C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_interceptors\_memintrinsics.cpp:26  

#1 0x7ff68cd50954 in opj\_t1\_allocate\_buffers C:\pdfium\third\_party\libopenjpeg\t1.c:1504:9  

#2 0x7ff68cd477fa in opj\_t1\_decode\_cblk C:\pdfium\third\_party\libopenjpeg\t1.c:1983  

#3 0x7ff68cd477fa in opj\_t1\_clbl\_decode\_processor C:\pdfium\third\_party\libopenjpeg\t1.c:1704:26  

#4 0x7ff68cd8d25d in opj\_thread\_pool\_submit\_job C:\pdfium\third\_party\libopenjpeg\thread.c:835:9  

#5 0x7ff68cd46b75 in opj\_t1\_decode\_cblks C:\pdfium\third\_party\libopenjpeg\t1.c:1943:21  

#6 0x7ff68cd87b50 in opj\_tcd\_t1\_decode C:\pdfium\third\_party\libopenjpeg\tcd.c:2008  

#7 0x7ff68cd87b50 in opj\_tcd\_decode\_tile C:\pdfium\third\_party\libopenjpeg\tcd.c:1662:11  

#8 0x7ff68cd1d118 in opj\_j2k\_decode\_tile C:\pdfium\third\_party\libopenjpeg\j2k.c:9862:11  

#9 0x7ff68cd32c6b in opj\_j2k\_decode\_tiles C:\pdfium\third\_party\libopenjpeg\j2k.c:11717:15  

#10 0x7ff68cd18b49 in opj\_j2k\_exec C:\pdfium\third\_party\libopenjpeg\j2k.c:9006:33  

#11 0x7ff68cd22a05 in opj\_j2k\_decode C:\pdfium\third\_party\libopenjpeg\j2k.c:12020:11  

#12 0x7ff68cc5f102 in fxcodec::CJPX\_Decoder::StartDecode(void) C:\pdfium\core\fxcodec\jpx\cjpx\_decoder.cpp:468:11  

#13 0x7ff68ce97cde in CPDF\_DIB::LoadJpxBitmap(void) C:\pdfium\core\fpdfapi\page\cpdf\_dib.cpp:574:17  

#14 0x7ff68ce90b44 in CPDF\_DIB::CreateDecoder(void) C:\pdfium\core\fpdfapi\page\cpdf\_dib.cpp:447:23  

#15 0x7ff68ce93bea in CPDF\_DIB::StartLoadDIBBase(bool, class CPDF\_Dictionary const \*, class CPDF\_Dictionary const \*, bool, enum CPDF\_ColorSpace::Family, bool) C:\pdfium\core\fpdfapi\page\cpdf\_dib.cpp:229:31  

#16 0x7ff68cf099b8 in CPDF\_PageRenderCache::ImageCacheEntry::StartGetCachedBitmap(class CPDF\_Dictionary const \*, class CPDF\_RenderStatus const \*, bool) C:\pdfium\core\fpdfapi\render\cpdf\_pagerendercache.cpp:182:58  

#17 0x7ff68cf091a0 in CPDF\_PageRenderCache::StartGetCachedBitmap(class fxcrt::RetainPtr<class CPDF\_Image>, class CPDF\_RenderStatus const \*, bool) C:\pdfium\core\fpdfapi\render\cpdf\_pagerendercache.cpp:93:52  

#18 0x7ff68cefd136 in CPDF\_ImageLoader::Start(class CPDF\_ImageObject const \*, class CPDF\_RenderStatus const \*, bool) C:\pdfium\core\fpdfapi\render\cpdf\_imageloader.cpp:32:21  

#19 0x7ff68cefec1e in CPDF\_ImageRenderer::StartLoadDIBBase(void) C:\pdfium\core\fpdfapi\render\cpdf\_imagerenderer.cpp:70:17  

#20 0x7ff68cf05bee in CPDF\_ImageRenderer::Start(class CPDF\_ImageObject \*, class CFX\_Matrix const &, bool, enum BlendMode) C:\pdfium\core\fpdfapi\render\cpdf\_imagerenderer.cpp:181:7  

#21 0x7ff68cf21e28 in CPDF\_RenderStatus::ContinueSingleObject(class CPDF\_PageObject \*, class CFX\_Matrix const &, class PauseIndicatorIface \*) C:\pdfium\core\fpdfapi\render\cpdf\_renderstatus.cpp:285:26  

#22 0x7ff68cf0ee59 in CPDF\_ProgressiveRenderer::Continue(class PauseIndicatorIface \*) C:\pdfium\core\fpdfapi\render\cpdf\_progressiverenderer.cpp:88:30  

#23 0x7ff68c95cacf in `anonymous namespace'::RenderPageImpl C:\pdfium\fpdfsdk\cpdfsdk_renderpage.cpp:84:26 #24 0x7ff68c95cf58 in CPDFSDK_RenderPageWithContext(class CPDF_PageRenderContext \*, class CPDF_Page \*, int, int, int, int, int, int, struct FPDF_COLORSCHEME_ const \*, bool, class CPDFSDK_PauseAdapter \*) C:\pdfium\fpdfsdk\cpdfsdk_renderpage.cpp:113:3 #25 0x7ff68c97246b in FPDF_RenderPageBitmapWithColorScheme_Start C:\pdfium\fpdfsdk\fpdf_progressive.cpp:73:3 #26 0x7ff68c8f851d in` anonymous namespace'::ProcessPage C:\pdfium\samples\pdfium\_test.cc:811  

#27 0x7ff68c8f851d in `anonymous namespace'::ProcessPdf C:\pdfium\samples\pdfium\_test.cc:1048  

#28 0x7ff68c8f851d in main C:\pdfium\samples\pdfium\_test.cc:1303:5  

#29 0x7ff68fdd680b in invoke\_main D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:78  

#30 0x7ff68fdd680b in \_\_scrt\_common\_main\_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#31 0x7ffcbbed7033 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#32 0x7ffcbc702650 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

0x1286146a16e7 is located 0 bytes to the right of 2663-byte region [0x1286146a0c80,0x1286146a16e7)  

allocated by thread T0 here:  

#0 0x7ff68f77602b in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ff68fde73fc in \_aligned\_malloc\_base C:\pdfium\out\Asan\minkernel\crts\ucrt\src\appcrt\heap\align.cpp:122  

#2 0x7ff68fde73fc in \_aligned\_malloc C:\pdfium\out\Asan\minkernel\crts\ucrt\src\appcrt\heap\align.cpp:555  

#3 0x7ff68c983450 in pdfium::base::AlignedAlloc(unsigned \_\_int64, unsigned \_\_int64) C:\pdfium\third\_party\base\memory\aligned\_memory.cc:23:9  

#4 0x7ff68cd0b5e9 in opj\_t1\_allocate\_buffers C:\pdfium\third\_party\libopenjpeg\ht\_dec.c:1069  

#5 0x7ff68cd0b5e9 in opj\_t1\_ht\_decode\_cblk C:\pdfium\third\_party\libopenjpeg\ht\_dec.c:1154:10  

#6 0x7ff68cd478a7 in opj\_t1\_clbl\_decode\_processor C:\pdfium\third\_party\libopenjpeg\t1.c:1690:26  

#7 0x7ff68cd8d25d in opj\_thread\_pool\_submit\_job C:\pdfium\third\_party\libopenjpeg\thread.c:835:9  

#8 0x7ff68cd46b75 in opj\_t1\_decode\_cblks C:\pdfium\third\_party\libopenjpeg\t1.c:1943:21  

#9 0x7ff68cd87b50 in opj\_tcd\_t1\_decode C:\pdfium\third\_party\libopenjpeg\tcd.c:2008  

#10 0x7ff68cd87b50 in opj\_tcd\_decode\_tile C:\pdfium\third\_party\libopenjpeg\tcd.c:1662:11  

#11 0x7ff68cd1d118 in opj\_j2k\_decode\_tile C:\pdfium\third\_party\libopenjpeg\j2k.c:9862:11  

#12 0x7ff68cd32c6b in opj\_j2k\_decode\_tiles C:\pdfium\third\_party\libopenjpeg\j2k.c:11717:15  

#13 0x7ff68cd18b49 in opj\_j2k\_exec C:\pdfium\third\_party\libopenjpeg\j2k.c:9006:33  

#14 0x7ff68cd22a05 in opj\_j2k\_decode C:\pdfium\third\_party\libopenjpeg\j2k.c:12020:11  

#15 0x7ff68cc5f102 in fxcodec::CJPX\_Decoder::StartDecode(void) C:\pdfium\core\fxcodec\jpx\cjpx\_decoder.cpp:468:11  

#16 0x7ff68ce97cde in CPDF\_DIB::LoadJpxBitmap(void) C:\pdfium\core\fpdfapi\page\cpdf\_dib.cpp:574:17  

#17 0x7ff68ce90b44 in CPDF\_DIB::CreateDecoder(void) C:\pdfium\core\fpdfapi\page\cpdf\_dib.cpp:447:23  

#18 0x7ff68ce93bea in CPDF\_DIB::StartLoadDIBBase(bool, class CPDF\_Dictionary const \*, class CPDF\_Dictionary const \*, bool, enum CPDF\_ColorSpace::Family, bool) C:\pdfium\core\fpdfapi\page\cpdf\_dib.cpp:229:31  

#19 0x7ff68cf099b8 in CPDF\_PageRenderCache::ImageCacheEntry::StartGetCachedBitmap(class CPDF\_Dictionary const \*, class CPDF\_RenderStatus const \*, bool) C:\pdfium\core\fpdfapi\render\cpdf\_pagerendercache.cpp:182:58  

#20 0x7ff68cf091a0 in CPDF\_PageRenderCache::StartGetCachedBitmap(class fxcrt::RetainPtr<class CPDF\_Image>, class CPDF\_RenderStatus const \*, bool) C:\pdfium\core\fpdfapi\render\cpdf\_pagerendercache.cpp:93:52  

#21 0x7ff68cefd136 in CPDF\_ImageLoader::Start(class CPDF\_ImageObject const \*, class CPDF\_RenderStatus const \*, bool) C:\pdfium\core\fpdfapi\render\cpdf\_imageloader.cpp:32:21  

#22 0x7ff68cefec1e in CPDF\_ImageRenderer::StartLoadDIBBase(void) C:\pdfium\core\fpdfapi\render\cpdf\_imagerenderer.cpp:70:17  

#23 0x7ff68cf05bee in CPDF\_ImageRenderer::Start(class CPDF\_ImageObject \*, class CFX\_Matrix const &, bool, enum BlendMode) C:\pdfium\core\fpdfapi\render\cpdf\_imagerenderer.cpp:181:7  

#24 0x7ff68cf21e28 in CPDF\_RenderStatus::ContinueSingleObject(class CPDF\_PageObject \*, class CFX\_Matrix const &, class PauseIndicatorIface \*) C:\pdfium\core\fpdfapi\render\cpdf\_renderstatus.cpp:285:26  

#25 0x7ff68cf0ee59 in CPDF\_ProgressiveRenderer::Continue(class PauseIndicatorIface \*) C:\pdfium\core\fpdfapi\render\cpdf\_progressiverenderer.cpp:88:30  

#26 0x7ff68c95cacf in `anonymous namespace'::RenderPageImpl C:\pdfium\fpdfsdk\cpdfsdk_renderpage.cpp:84:26 #27 0x7ff68c95cf58 in CPDFSDK_RenderPageWithContext(class CPDF_PageRenderContext \*, class CPDF_Page \*, int, int, int, int, int, int, struct FPDF_COLORSCHEME_ const \*, bool, class CPDFSDK_PauseAdapter \*) C:\pdfium\fpdfsdk\cpdfsdk_renderpage.cpp:113:3 #28 0x7ff68c97246b in FPDF_RenderPageBitmapWithColorScheme_Start C:\pdfium\fpdfsdk\fpdf_progressive.cpp:73:3 #29 0x7ff68c8f851d in` anonymous namespace'::ProcessPage C:\pdfium\samples\pdfium\_test.cc:811  

#30 0x7ff68c8f851d in `anonymous namespace'::ProcessPdf C:\pdfium\samples\pdfium\_test.cc:1048  

#31 0x7ff68c8f851d in main C:\pdfium\samples\pdfium\_test.cc:1303:5  

#32 0x7ff68fdd680b in invoke\_main D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:78  

#33 0x7ff68fdd680b in \_\_scrt\_common\_main\_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288

SUMMARY: AddressSanitizer: heap-buffer-overflow C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_interceptors\_memintrinsics.cpp:26 in \_\_asan\_memset  

Shadow bytes around the buggy address:  

0x049ad6f54280: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x049ad6f54290: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x049ad6f542a0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x049ad6f542b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x049ad6f542c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x049ad6f542d0: 00 00 00 00 00 00 00 00 00 00 00 00[07]fa fa fa  

0x049ad6f542e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x049ad6f542f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x049ad6f54300: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x049ad6f54310: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x049ad6f54320: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

==11644==ABORTING

**VERSION**  

**Chrome Version: [x.x.x.x] + [stable, beta, or dev]**  

**Operating System: [Please indicate OS, version, and service pack level]**

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug, or any personal or confidential information.**

**Please attach files directly, not in zip or other archive formats, and if**  

**you've created a demonstration site please also attach the files needed to**  

**reproduce the demonstration locally.**

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

**Reporter credit: [goes here]**

## Attachments

- poc.pdf (application/pdf, 3.0 KB)
- 0044-opj_t1_allocate_buffers.patch (text/plain, 869 B)

## Timeline

### 0x...@gmail.com (2022-08-27)

https://pdfium.googlesource.com/pdfium/+log/ef51a2d87a6ac68c74dbbbece1e968edb1a4c20f/third_party/libopenjpeg/ht_dec.c
missed
https://github.com/uclouvain/openjpeg/commit/0535bfc3b7d5cd6fc73a7d4a6749a338fc5d7703

### [Deleted User] (2022-08-27)

[Empty comment from Monorail migration]

### 0x...@gmail.com (2022-08-27)

This is the patch grabbed from upstream that could fix this issue.

### 0x...@gmail.com (2022-08-27)

[Comment Deleted]

### 0x...@gmail.com (2022-08-27)

PDFium upgraded OpenJPEG to 2.5.0 on Jun 10th [1].
OpenJPEG 2.5.0 was released on May 14th [2].
And the upstream patch was committed on May 31st [3].
PDFium did picked some patches [4] from upstream, but missed the patch for this issue.

Current stable version number for Chrome is 104.0.5112.102 which was NOT affected by this issue [5, 6].
Current beta version number for Chrome is 105.0.5195.52 and it's affected by this issue [7, 8].

[1] https://pdfium.googlesource.com/pdfium/+/c06d7e7486aa5e04d95786b95f5fd6a30c07c982
[2] https://github.com/uclouvain/openjpeg/releases/tag/v2.5.0
[3] https://github.com/uclouvain/openjpeg/commit/0535bfc3b7d5cd6fc73a7d4a6749a338fc5d7703
[4] https://pdfium.googlesource.com/pdfium/+log/ef51a2d87a6ac68c74dbbbece1e968edb1a4c20f/third_party/libopenjpeg
[5] https://chromium.googlesource.com/chromium/src.git/+/refs/tags/104.0.5112.102%5E%21/#F0
[6] https://pdfium.googlesource.com/pdfium/+log/c7c276ce1192f043affb2098ac7ce44f7fd7f084/third_party/libopenjpeg20
[7] https://chromium.googlesource.com/chromium/src.git/+/refs/tags/105.0.5195.52%5E%21/#F0
[8] https://pdfium.googlesource.com/pdfium/+log/d14da8e682e244127db32490365d1c094243e5f3/third_party/libopenjpeg20

### cl...@chromium.org (2022-08-29)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6330409401122816.

### es...@chromium.org (2022-08-29)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### th...@chromium.org (2022-08-29)

tsepez@: Are there any automated tools that we should be using to find out about these issues in OpenJPEG sooner?

### cl...@chromium.org (2022-08-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-08-29)

[Empty comment from Monorail migration]

### th...@chromium.org (2022-08-29)

re: https://crbug.com/chromium/1357303#c4 - Chromium and related projects like PDFium do not take .patch files attached to bugs. Please see https://pdfium.googlesource.com/pdfium/+/e0ea309bac/CONTRIBUTING.md for the process of submitting patches.

### cl...@chromium.org (2022-08-29)

Detailed Report: https://clusterfuzz.com/testcase?key=6330409401122816

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow WRITE {*}
Crash Address: 0x61e0000202d0
Crash State:
  opj_t1_allocate_buffers
  opj_t1_clbl_decode_processor
  opj_thread_pool_submit_job
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=1040481

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6330409401122816

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### th...@chromium.org (2022-08-29)

Setting targets per https://crbug.com/chromium/1357303#c5.

### gi...@appspot.gserviceaccount.com (2022-08-29)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/340bbcf10b50734dee585b0dae5cf295b835c5c9

commit 340bbcf10b50734dee585b0dae5cf295b835c5c9
Author: Lei Zhang <thestig@chromium.org>
Date: Mon Aug 29 23:17:14 2022

Fix a malloc size error in OpenJPEG.

Cherrypick the fix [1] from upstream OpenJPEG.

[1] https://github.com/uclouvain/openjpeg/pull/1426

Bug: chromium:1357303
Change-Id: I0b18a896c061485e41eb2890d21d0f6d842bab18
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/97012
Commit-Queue: Lei Zhang <thestig@chromium.org>
Reviewed-by: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/340bbcf10b50734dee585b0dae5cf295b835c5c9/third_party/libopenjpeg/ht_dec.c
[add] https://pdfium.googlesource.com/pdfium/+/340bbcf10b50734dee585b0dae5cf295b835c5c9/third_party/libopenjpeg/0044-opj_t1_allocate_buffers.patch
[modify] https://pdfium.googlesource.com/pdfium/+/340bbcf10b50734dee585b0dae5cf295b835c5c9/third_party/libopenjpeg/README.pdfium


### gi...@appspot.gserviceaccount.com (2022-08-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0b28a071db9e7c5b18b6eaae8a61d40640960081

commit 0b28a071db9e7c5b18b6eaae8a61d40640960081
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Aug 30 08:41:48 2022

Roll PDFium from 8479a083aa9f to 5e49f9cccf75 (3 revisions)

https://pdfium.googlesource.com/pdfium.git/+log/8479a083aa9f..5e49f9cccf75

2022-08-30 awscreen@chromium.org Add runtime renderer checks
2022-08-30 awscreen@chromium.org Refactor embeddertest constants for runtime renderer selection
2022-08-29 thestig@chromium.org Fix a malloc size error in OpenJPEG.

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To file a bug in PDFium: https://bugs.chromium.org/p/pdfium/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1357303
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I5efe10b55a955c48081eebbe9db165e26ad48a3b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3864806
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1040845}

[modify] https://crrev.com/0b28a071db9e7c5b18b6eaae8a61d40640960081/DEPS


### th...@chromium.org (2022-08-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-30)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-30)

Requesting merge to dev M106 because latest trunk commit (1040845) appears to be after dev branch point (1036826).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-30)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2022-08-30)

ClusterFuzz testcase 6330409401122816 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1040844:1040845

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### sr...@google.com (2022-09-08)

Merge approved for M106 branch: pls refer to go/chrome-branches for more info

### gi...@appspot.gserviceaccount.com (2022-09-09)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/c5f61025a75118b24885f97db4ecfe7f81db462d

commit c5f61025a75118b24885f97db4ecfe7f81db462d
Author: Lei Zhang <thestig@chromium.org>
Date: Fri Sep 09 01:27:54 2022

M106: Fix a malloc size error in OpenJPEG.

Cherrypick the fix [1] from upstream OpenJPEG.

[1] https://github.com/uclouvain/openjpeg/pull/1426

Bug: chromium:1357303
Change-Id: I0b18a896c061485e41eb2890d21d0f6d842bab18
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/97012
Commit-Queue: Lei Zhang <thestig@chromium.org>
Reviewed-by: Tom Sepez <tsepez@chromium.org>
(cherry picked from commit 340bbcf10b50734dee585b0dae5cf295b835c5c9)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/97790

[modify] https://pdfium.googlesource.com/pdfium/+/c5f61025a75118b24885f97db4ecfe7f81db462d/third_party/libopenjpeg/ht_dec.c
[modify] https://pdfium.googlesource.com/pdfium/+/c5f61025a75118b24885f97db4ecfe7f81db462d/third_party/libopenjpeg/README.pdfium
[add] https://pdfium.googlesource.com/pdfium/+/c5f61025a75118b24885f97db4ecfe7f81db462d/third_party/libopenjpeg/0044-opj_t1_allocate_buffers.patch


### th...@chromium.org (2022-09-09)

amyressler@: Clusterfuzz somehow incorrectly determined this does not affect M105, but I agree with https://crbug.com/chromium/1357303#c5 that it does. Can you set the labels so we get the fix merged to M105?

### am...@chromium.org (2022-09-09)

Thanks for that insight thesitig@ - updating FoundIn based on https://crbug.com/chromium/1357303#c5 and https://crbug.com/chromium/1357303#c25. 

The next/ last planned security respin for M105 is being cut tomorrow, so bypassing merge review/request labeling and adding merge approval label based on the autoroll CL with this fix being landed over one week ago and not seeing any apparent issues. 
As long as there are no issues or concerns with merging this fix now, please merge to branch 5195 by 9am PDT tomorrow/Friday, 9 September, so this fix can be included in the security refresh of M105. Thanks! 

### pb...@google.com (2022-09-09)

This merge has been approved for M105, please help complete your merges asap (before Noon PST) today, so the change can be included in next weeks RC build for Stable releases.

### gi...@appspot.gserviceaccount.com (2022-09-09)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/4da7fd57f192eedf8c89f7e1dd2c8fbed71358c8

commit 4da7fd57f192eedf8c89f7e1dd2c8fbed71358c8
Author: Lei Zhang <thestig@chromium.org>
Date: Fri Sep 09 19:23:15 2022

M105: Fix a malloc size error in OpenJPEG.

Cherrypick the fix [1] from upstream OpenJPEG.

[1] https://github.com/uclouvain/openjpeg/pull/1426

Bug: chromium:1357303
Change-Id: I0b18a896c061485e41eb2890d21d0f6d842bab18
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/97012
Commit-Queue: Lei Zhang <thestig@chromium.org>
Reviewed-by: Tom Sepez <tsepez@chromium.org>
(cherry picked from commit 340bbcf10b50734dee585b0dae5cf295b835c5c9)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/97810
Reviewed-by: Nigi <nigi@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/4da7fd57f192eedf8c89f7e1dd2c8fbed71358c8/third_party/libopenjpeg/ht_dec.c
[add] https://pdfium.googlesource.com/pdfium/+/4da7fd57f192eedf8c89f7e1dd2c8fbed71358c8/third_party/libopenjpeg/0044-opj_t1_allocate_buffers.patch
[modify] https://pdfium.googlesource.com/pdfium/+/4da7fd57f192eedf8c89f7e1dd2c8fbed71358c8/third_party/libopenjpeg/README.pdfium


### am...@google.com (2022-09-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-09-09)

Congratulations on another one! The VRP Panel has decided to award you $7,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. Please let us know the name/handle/tag or other identifier you would like us to use in acknowledging you for reporting this issue. Thank you for your efforts and reporting this issue to us -- nice work! 

### 0x...@gmail.com (2022-09-10)

Please credit to MerdroidSG. Thanks.

### am...@google.com (2022-09-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-12-06)

This issue was migrated from crbug.com/chromium/1357303?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060691)*
