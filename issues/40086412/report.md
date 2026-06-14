# Security: PDFium OpenJPEG Use-After-Free Vulnerability

| Field | Value |
|-------|-------|
| **Issue ID** | [40086412](https://issues.chromium.org/issues/40086412) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Windows |
| **Reporter** | st...@gmail.com |
| **Assignee** | np...@chromium.org |
| **Created** | 2017-01-05 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

=================================================================  

==15048==ERROR: AddressSanitizer: heap-use-after-free on address 0x0ee03740 at pc 0x025d7625 bp 0x03eac1fc sp 0x03eac1f0  

READ of size 4 at 0x0ee03740 thread T0  

#0 0x25d7624 in opj\_j2k\_read\_mco C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\third\_party\libopenjpeg20\j2k.c:5671:68  

#1 0x25cc88f in opj\_j2k\_read\_header\_procedure C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\third\_party\libopenjpeg20\j2k.c:7217:23  

#2 0x25dcef8 in opj\_jp2\_exec C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\third\_party\libopenjpeg20\jp2.c:2261:26  

#3 0x25c1779 in opj\_j2k\_read\_header C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\third\_party\libopenjpeg20\j2k.c:6768:15  

#4 0x25bf156 in opj\_read\_header C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\third\_party\libopenjpeg20\openjpeg.c:391:10  

#5 0x2529799 in CJPX\_Decoder::Init(unsigned char const \*,unsigned int) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fxcodec\codec\fx\_codec\_jpx\_opj.cpp:761:8  

#6 0x252b624 in CCodec\_JpxModule::CreateDecoder(unsigned char const \*,unsigned int,class CPDF\_ColorSpace \*) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fxcodec\codec\fx\_codec\_jpx\_opj.cpp:900:19  

#7 0x24749d3 in CPDF\_DIBSource::LoadJpxBitmap(void) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fpdfapi\render\fpdf\_render\_loadimage.cpp:638:36  

#8 0x246e1d9 in CPDF\_DIBSource::CreateDecoder(void) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fpdfapi\render\fpdf\_render\_loadimage.cpp:527:5  

#9 0x2471fe0 in CPDF\_DIBSource::StartLoadDIBSource(class CPDF\_Document \*,class CPDF\_Stream const \*,bool,class CPDF\_Dictionary \*,class CPDF\_Dictionary \*,bool,unsigned int,bool) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fpdfapi\render\fpdf\_render\_loadimage.cpp:302:13  

#10 0x243d2f7 in CPDF\_ImageCacheEntry::StartGetCachedBitmap(class CPDF\_Dictionary \*,class CPDF\_Dictionary \*,bool,unsigned int,bool,class CPDF\_RenderStatus \*,int,int) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fpdfapi\render\cpdf\_imagecacheentry.cpp:121:13  

#11 0x23e410e in CPDF\_PageRenderCache::StartGetCachedBitmap(class CPDF\_Stream \*,bool,unsigned int,bool,class CPDF\_RenderStatus \*,int,int) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fpdfapi\render\cpdf\_pagerendercache.cpp:98:36  

#12 0x2495c18 in CPDF\_ImageLoader::Start(class CPDF\_ImageObject const \*,class CPDF\_PageRenderCache \*,bool,unsigned int,bool,class CPDF\_RenderStatus \*,int,int) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fpdfapi\render\cpdf\_imageloader.cpp:48:19  

#13 0x2452e08 in CPDF\_ImageRenderer::StartLoadDIBSource(void) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fpdfapi\render\cpdf\_imagerenderer.cpp:66:16  

#14 0x2458126 in CPDF\_ImageRenderer::Start(class CPDF\_RenderStatus \*,class CPDF\_PageObject \*,class CFX\_Matrix const \*,bool,int) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fpdfapi\render\cpdf\_imagerenderer.cpp:205:7  

#15 0x23eebee in CPDF\_RenderStatus::ContinueSingleObject(class CPDF\_PageObject \*,class CFX\_Matrix const \*,class IFX\_Pause \*) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fpdfapi\render\cpdf\_renderstatus.cpp:1084:28  

#16 0x238498c in CPDF\_ProgressiveRenderer::Continue(class IFX\_Pause \*) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fpdfapi\render\cpdf\_progressiverenderer.cpp:78:30  

#17 0x228b84d in `anonymous namespace'::RenderPageImpl C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\fpdfsdk\fpdfview.cpp:115:26  

#18 0x228b047 in FPDF\_RenderPage\_Retail(class CPDF\_PageRenderContext \*,void \*,int,int,int,int,int,int,bool,class IFSDK\_PAUSE\_Adapter \*) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\fpdfsdk\fpdfview.cpp:982:3  

#19 0x228b273 in FPDF\_RenderPageBitmap C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\fpdfsdk\fpdfview.cpp:716:3  

#20 0x4975d in RenderPage(class std::basic\_string<char,struct std::char\_traits<char>,class std::allocator<char> > const &,void \*,void \* &,struct FPDF\_FORMFILLINFO\_PDFiumTest &,int,struct Options const &,class std::basic\_string<char,struct std::char\_traits<char>,class std::allocator<char> > const &) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\samples\pdfium\_test.cc:657:5  

#21 0x4c615 in RenderPdf(class std::basic\_string<char,struct std::char\_traits<char>,class std::allocator<char> > const &,char const \*,unsigned int,struct Options const &,class std::basic\_string<char,struct std::char\_traits<char>,class std::allocator<char> > const &) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\samples\pdfium\_test.cc:862:9  

#22 0x4d583 in main C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\samples\pdfium\_test.cc:998:5  

#23 0x2c5b9b8 in \_scrt\_common\_main\_seh f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl:253  

#24 0x749e3389 (C:\Windows\syswow64\kernel32.dll+0x7dd73389)  

#25 0x76f99a01 (C:\Windows\SysWOW64\ntdll.dll+0x7dea9a01)  

#26 0x76f999d4 (C:\Windows\SysWOW64\ntdll.dll+0x7dea99d4)

0x0ee03740 is located 0 bytes inside of 200-byte region [0x0ee03740,0x0ee03808)  

freed by thread T0 here:  

#0 0x2c41398 in realloc e:\b\build\slave\win\_upload\_clang\build\src\third\_party\llvm\projects\compiler-rt\lib\asan\asan\_malloc\_win.cc:102  

#1 0x25d500d in opj\_j2k\_read\_mct C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\third\_party\libopenjpeg20\j2k.c:5179:62  

#2 0x25cc88f in opj\_j2k\_read\_header\_procedure C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\third\_party\libopenjpeg20\j2k.c:7217:23  

#3 0x25dcef8 in opj\_jp2\_exec C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\third\_party\libopenjpeg20\jp2.c:2261:26  

#4 0x25c1779 in opj\_j2k\_read\_header C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\third\_party\libopenjpeg20\j2k.c:6768:15  

#5 0x25bf156 in opj\_read\_header C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\third\_party\libopenjpeg20\openjpeg.c:391:10  

#6 0x2529799 in CJPX\_Decoder::Init(unsigned char const \*,unsigned int) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fxcodec\codec\fx\_codec\_jpx\_opj.cpp:761:8  

#7 0x252b624 in CCodec\_JpxModule::CreateDecoder(unsigned char const \*,unsigned int,class CPDF\_ColorSpace \*) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fxcodec\codec\fx\_codec\_jpx\_opj.cpp:900:19  

#8 0x24749d3 in CPDF\_DIBSource::LoadJpxBitmap(void) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fpdfapi\render\fpdf\_render\_loadimage.cpp:638:36  

#9 0x246e1d9 in CPDF\_DIBSource::CreateDecoder(void) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fpdfapi\render\fpdf\_render\_loadimage.cpp:527:5  

#10 0x2471fe0 in CPDF\_DIBSource::StartLoadDIBSource(class CPDF\_Document \*,class CPDF\_Stream const \*,bool,class CPDF\_Dictionary \*,class CPDF\_Dictionary \*,bool,unsigned int,bool) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fpdfapi\render\fpdf\_render\_loadimage.cpp:302:13  

#11 0x243d2f7 in CPDF\_ImageCacheEntry::StartGetCachedBitmap(class CPDF\_Dictionary \*,class CPDF\_Dictionary \*,bool,unsigned int,bool,class CPDF\_RenderStatus \*,int,int) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fpdfapi\render\cpdf\_imagecacheentry.cpp:121:13  

#12 0x23e410e in CPDF\_PageRenderCache::StartGetCachedBitmap(class CPDF\_Stream \*,bool,unsigned int,bool,class CPDF\_RenderStatus \*,int,int) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fpdfapi\render\cpdf\_pagerendercache.cpp:98:36  

#13 0x2495c18 in CPDF\_ImageLoader::Start(class CPDF\_ImageObject const \*,class CPDF\_PageRenderCache \*,bool,unsigned int,bool,class CPDF\_RenderStatus \*,int,int) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fpdfapi\render\cpdf\_imageloader.cpp:48:19  

#14 0x2452e08 in CPDF\_ImageRenderer::StartLoadDIBSource(void) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fpdfapi\render\cpdf\_imagerenderer.cpp:66:16  

#15 0x2458126 in CPDF\_ImageRenderer::Start(class CPDF\_RenderStatus \*,class CPDF\_PageObject \*,class CFX\_Matrix const \*,bool,int) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fpdfapi\render\cpdf\_imagerenderer.cpp:205:7  

#16 0x23eebee in CPDF\_RenderStatus::ContinueSingleObject(class CPDF\_PageObject \*,class CFX\_Matrix const \*,class IFX\_Pause \*) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fpdfapi\render\cpdf\_renderstatus.cpp:1084:28  

#17 0x238498c in CPDF\_ProgressiveRenderer::Continue(class IFX\_Pause \*) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fpdfapi\render\cpdf\_progressiverenderer.cpp:78:30  

#18 0x228b84d in `anonymous namespace'::RenderPageImpl C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\fpdfsdk\fpdfview.cpp:115:26  

#19 0x228b047 in FPDF\_RenderPage\_Retail(class CPDF\_PageRenderContext \*,void \*,int,int,int,int,int,int,bool,class IFSDK\_PAUSE\_Adapter \*) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\fpdfsdk\fpdfview.cpp:982:3  

#20 0x228b273 in FPDF\_RenderPageBitmap C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\fpdfsdk\fpdfview.cpp:716:3  

#21 0x4975d in RenderPage(class std::basic\_string<char,struct std::char\_traits<char>,class std::allocator<char> > const &,void \*,void \* &,struct FPDF\_FORMFILLINFO\_PDFiumTest &,int,struct Options const &,class std::basic\_string<char,struct std::char\_traits<char>,class std::allocator<char> > const &) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\samples\pdfium\_test.cc:657:5  

#22 0x4c615 in RenderPdf(class std::basic\_string<char,struct std::char\_traits<char>,class std::allocator<char> > const &,char const \*,unsigned int,struct Options const &,class std::basic\_string<char,struct std::char\_traits<char>,class std::allocator<char> > const &) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\samples\pdfium\_test.cc:862:9  

#23 0x4d583 in main C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\samples\pdfium\_test.cc:998:5  

#24 0x2c5b9b8 in \_scrt\_common\_main\_seh f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl:253  

#25 0x749e3389 (C:\Windows\syswow64\kernel32.dll+0x7dd73389)  

#26 0x76f99a01 (C:\Windows\SysWOW64\ntdll.dll+0x7dea9a01)  

#27 0x76f999d4 (C:\Windows\SysWOW64\ntdll.dll+0x7dea99d4)

previously allocated by thread T0 here:  

#0 0x2c410f8 in calloc e:\b\build\slave\win\_upload\_clang\build\src\third\_party\llvm\projects\compiler-rt\lib\asan\asan\_malloc\_win.cc:81  

#1 0x25d3262 in opj\_j2k\_read\_siz C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\third\_party\libopenjpeg20\j2k.c:2252:42  

#2 0x25cc88f in opj\_j2k\_read\_header\_procedure C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\third\_party\libopenjpeg20\j2k.c:7217:23  

#3 0x25dcef8 in opj\_jp2\_exec C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\third\_party\libopenjpeg20\jp2.c:2261:26  

#4 0x25c1779 in opj\_j2k\_read\_header C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\third\_party\libopenjpeg20\j2k.c:6768:15  

#5 0x25bf156 in opj\_read\_header C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\third\_party\libopenjpeg20\openjpeg.c:391:10  

#6 0x2529799 in CJPX\_Decoder::Init(unsigned char const \*,unsigned int) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fxcodec\codec\fx\_codec\_jpx\_opj.cpp:761:8  

#7 0x252b624 in CCodec\_JpxModule::CreateDecoder(unsigned char const \*,unsigned int,class CPDF\_ColorSpace \*) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fxcodec\codec\fx\_codec\_jpx\_opj.cpp:900:19  

#8 0x24749d3 in CPDF\_DIBSource::LoadJpxBitmap(void) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fpdfapi\render\fpdf\_render\_loadimage.cpp:638:36  

#9 0x246e1d9 in CPDF\_DIBSource::CreateDecoder(void) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fpdfapi\render\fpdf\_render\_loadimage.cpp:527:5  

#10 0x2471fe0 in CPDF\_DIBSource::StartLoadDIBSource(class CPDF\_Document \*,class CPDF\_Stream const \*,bool,class CPDF\_Dictionary \*,class CPDF\_Dictionary \*,bool,unsigned int,bool) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fpdfapi\render\fpdf\_render\_loadimage.cpp:302:13  

#11 0x243d2f7 in CPDF\_ImageCacheEntry::StartGetCachedBitmap(class CPDF\_Dictionary \*,class CPDF\_Dictionary \*,bool,unsigned int,bool,class CPDF\_RenderStatus \*,int,int) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fpdfapi\render\cpdf\_imagecacheentry.cpp:121:13  

#12 0x23e410e in CPDF\_PageRenderCache::StartGetCachedBitmap(class CPDF\_Stream \*,bool,unsigned int,bool,class CPDF\_RenderStatus \*,int,int) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fpdfapi\render\cpdf\_pagerendercache.cpp:98:36  

#13 0x2495c18 in CPDF\_ImageLoader::Start(class CPDF\_ImageObject const \*,class CPDF\_PageRenderCache \*,bool,unsigned int,bool,class CPDF\_RenderStatus \*,int,int) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fpdfapi\render\cpdf\_imageloader.cpp:48:19  

#14 0x2452e08 in CPDF\_ImageRenderer::StartLoadDIBSource(void) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fpdfapi\render\cpdf\_imagerenderer.cpp:66:16  

#15 0x2458126 in CPDF\_ImageRenderer::Start(class CPDF\_RenderStatus \*,class CPDF\_PageObject \*,class CFX\_Matrix const \*,bool,int) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fpdfapi\render\cpdf\_imagerenderer.cpp:205:7  

#16 0x23eebee in CPDF\_RenderStatus::ContinueSingleObject(class CPDF\_PageObject \*,class CFX\_Matrix const \*,class IFX\_Pause \*) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fpdfapi\render\cpdf\_renderstatus.cpp:1084:28  

#17 0x238498c in CPDF\_ProgressiveRenderer::Continue(class IFX\_Pause \*) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\core\fpdfapi\render\cpdf\_progressiverenderer.cpp:78:30  

#18 0x228b84d in `anonymous namespace'::RenderPageImpl C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\fpdfsdk\fpdfview.cpp:115:26  

#19 0x228b047 in FPDF\_RenderPage\_Retail(class CPDF\_PageRenderContext \*,void \*,int,int,int,int,int,int,bool,class IFSDK\_PAUSE\_Adapter \*) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\fpdfsdk\fpdfview.cpp:982:3  

#20 0x228b273 in FPDF\_RenderPageBitmap C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\fpdfsdk\fpdfview.cpp:716:3  

#21 0x4975d in RenderPage(class std::basic\_string<char,struct std::char\_traits<char>,class std::allocator<char> > const &,void \*,void \* &,struct FPDF\_FORMFILLINFO\_PDFiumTest &,int,struct Options const &,class std::basic\_string<char,struct std::char\_traits<char>,class std::allocator<char> > const &) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\samples\pdfium\_test.cc:657:5  

#22 0x4c615 in RenderPdf(class std::basic\_string<char,struct std::char\_traits<char>,class std::allocator<char> > const &,char const \*,unsigned int,struct Options const &,class std::basic\_string<char,struct std::char\_traits<char>,class std::allocator<char> > const &) C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\samples\pdfium\_test.cc:862:9  

#23 0x4d583 in main C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\samples\pdfium\_test.cc:998:5  

#24 0x2c5b9b8 in \_scrt\_common\_main\_seh f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl:253  

#25 0x749e3389 (C:\Windows\syswow64\kernel32.dll+0x7dd73389)  

#26 0x76f99a01 (C:\Windows\SysWOW64\ntdll.dll+0x7dea9a01)  

#27 0x76f999d4 (C:\Windows\SysWOW64\ntdll.dll+0x7dea99d4)

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\c\b\win\_asan\_release\src\third\_party\pdfium\third\_party\libopenjpeg20\j2k.c:5671:68 in opj\_j2k\_read\_mco  

Shadow bytes around the buggy address:  

0x31dc0690: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x31dc06a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x31dc06b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x31dc06c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x31dc06d0: 00 00 00 00 00 00 00 00 00 fa fa fa fa fa fa fa  

=>0x31dc06e0: fa fa fa fa fa fa fa fa[fd]fd fd fd fd fd fd fd  

0x31dc06f0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x31dc0700: fd fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x31dc0710: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x31dc0720: 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa fa  

0x31dc0730: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

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

==15048==ABORTING

**VERSION**  

Chrome Version: Stable  

Operating System: All

**REPRODUCTION CASE**  

See attachment.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: Tab  

**Crash State: [see link above: stack trace, registers, exception record]**  

**Client ID (if relevant): [see link above]**

## Timeline

### st...@gmail.com (2017-01-05)

[Comment Deleted]

### cl...@chromium.org (2017-01-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6025704501411840

### cl...@chromium.org (2017-01-05)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6025704501411840

Job Type: linux_asan_pdfium
Crash Type: Heap-use-after-free READ 4
Crash Address: 0x613000000b00
Crash State:
  opj_j2k_read_mco
  opj_j2k_read_header_procedure
  opj_j2k_read_header
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=321780:322012

Minimized Testcase (1.56 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97TI-j38amhThvsc3CMKah8kNCCVL_RBQW7QN9ogDYAuYZ26Zl9VP6jpbgL3czp_jHWGjpRVy2Wc-2TkfASjFcZ0_TFiXtJIFJfer2JvffLLqsche897cK7xpUk9JhkLKN1aTtW5amknEFFQ8wG3NqcStHMdm-3lZumvjEqzavs2ZmOi2pPJrgcBVKdyihXqeebFqxVfsq-2NFiKi4LErKZCG-YmgvpnQ8zPd-cmds8Np1bAcKLEixlKy794BVpO_SFzlNW5yU4vunaWu1T4whUIbn39rXDfVyhJuwaZJttMlXv73ACs6sW2SXuZfM-DE8gRjswfTVixvr5VOsT_DncX58bBCB0m4kU8ZPGyLFwkwqi4FM?testcase_id=6025704501411840

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.


### mm...@chromium.org (2017-01-05)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### st...@gmail.com (2017-01-05)

This issue affects all chrome versions, including chrome stable, we should fix it ASAP.

### rs...@chromium.org (2017-01-06)

jun_fang: This looks like it may have been caused by updating openjpeg: https://pdfium.googlesource.com/pdfium/+/ec61a859344dc6d2a60e4cbcd1555e6d317f2add.

### sh...@chromium.org (2017-01-07)

[Empty comment from Monorail migration]

### ds...@chromium.org (2017-01-10)

npm@ can you take a look? This one isn't XFA so needs to get fixed soon.

### bu...@chromium.org (2017-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a427ba0638c4294faf264550d12077b709f5c0de

commit a427ba0638c4294faf264550d12077b709f5c0de
Author: pdfium-deps-roller <pdfium-deps-roller@chromium.org>
Date: Wed Jan 11 06:42:58 2017

Roll src/third_party/pdfium/ 29a9f87a8..44bc1f818 (5 commits).

https://pdfium.googlesource.com/pdfium.git/+log/29a9f87a8bcd..44bc1f818dd7

$ git log 29a9f87a8..44bc1f818 --date=short --no-merges --format='%ad %ae %s'
2017-01-10 npm Fix m_nb_mct_records calculation in opj_j2k_read_mct
2017-01-10 dsinclair Strip out custom allocator code
2017-01-10 dsinclair Split xfa_textlayout apart.
2017-01-10 dsinclair Remove custom allocator from CFDE_TxtEdtBuf.
2017-01-10 tsepez Remove CFX_ArrayTemplate in cfx_psrender.

BUG=678461

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, see:
http://www.chromium.org/developers/tree-sheriffs/sheriff-details-chromium#TOC-Failures-due-to-DEPS-rolls

TBR=dsinclair@chromium.org

Review-Url: https://codereview.chromium.org/2628783002
Cr-Commit-Position: refs/heads/master@{#442827}

[modify] https://crrev.com/a427ba0638c4294faf264550d12077b709f5c0de/DEPS


### cl...@chromium.org (2017-01-11)

ClusterFuzz has detected this issue as fixed in range 441524:442831.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6025704501411840

Job Type: linux_asan_pdfium
Crash Type: Heap-use-after-free READ 4
Crash Address: 0x613000000b00
Crash State:
  opj_j2k_read_mco
  opj_j2k_read_header_procedure
  opj_j2k_read_header
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=321780:322012
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=441524:442831

Minimized Testcase (1.56 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97TI-j38amhThvsc3CMKah8kNCCVL_RBQW7QN9ogDYAuYZ26Zl9VP6jpbgL3czp_jHWGjpRVy2Wc-2TkfASjFcZ0_TFiXtJIFJfer2JvffLLqsche897cK7xpUk9JhkLKN1aTtW5amknEFFQ8wG3NqcStHMdm-3lZumvjEqzavs2ZmOi2pPJrgcBVKdyihXqeebFqxVfsq-2NFiKi4LErKZCG-YmgvpnQ8zPd-cmds8Np1bAcKLEixlKy794BVpO_SFzlNW5yU4vunaWu1T4whUIbn39rXDfVyhJuwaZJttMlXv73ACs6sW2SXuZfM-DE8gRjswfTVixvr5VOsT_DncX58bBCB0m4kU8ZPGyLFwkwqi4FM?testcase_id=6025704501411840

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### np...@chromium.org (2017-01-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2017-01-11)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6025704501411840

Job Type: linux_asan_pdfium
Crash Type: Heap-use-after-free READ 4
Crash Address: 0x613000000b00
Crash State:
  opj_j2k_read_mco
  opj_j2k_read_header_procedure
  opj_j2k_read_header
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=321780:322012
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=441524:442831

Minimized Testcase (1.56 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97TI-j38amhThvsc3CMKah8kNCCVL_RBQW7QN9ogDYAuYZ26Zl9VP6jpbgL3czp_jHWGjpRVy2Wc-2TkfASjFcZ0_TFiXtJIFJfer2JvffLLqsche897cK7xpUk9JhkLKN1aTtW5amknEFFQ8wG3NqcStHMdm-3lZumvjEqzavs2ZmOi2pPJrgcBVKdyihXqeebFqxVfsq-2NFiKi4LErKZCG-YmgvpnQ8zPd-cmds8Np1bAcKLEixlKy794BVpO_SFzlNW5yU4vunaWu1T4whUIbn39rXDfVyhJuwaZJttMlXv73ACs6sW2SXuZfM-DE8gRjswfTVixvr5VOsT_DncX58bBCB0m4kU8ZPGyLFwkwqi4FM?testcase_id=6025704501411840

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### bu...@chromium.org (2017-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/68e998adb1ea9fd998afd4dafd372d3d4729a54b

commit 68e998adb1ea9fd998afd4dafd372d3d4729a54b
Author: pdfium-deps-roller <pdfium-deps-roller@chromium.org>
Date: Wed Jan 11 23:46:19 2017

Roll src/third_party/pdfium/ 8fa82794f..96f482c9c (2 commits).

https://pdfium.googlesource.com/pdfium.git/+log/8fa82794ffc2..96f482c9cd3c

$ git log 8fa82794f..96f482c9c --date=short --no-merges --format='%ad %ae %s'
2017-01-11 dsinclair Convert FDE CSS enums to enum classes.
2017-01-11 npm Really fix m_nb_mct_records calculation in opj_j2k_read_mct

BUG=678461,680102

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, see:
http://www.chromium.org/developers/tree-sheriffs/sheriff-details-chromium#TOC-Failures-due-to-DEPS-rolls

TBR=dsinclair@chromium.org

Review-Url: https://codereview.chromium.org/2623103004
Cr-Commit-Position: refs/heads/master@{#443057}

[modify] https://crrev.com/68e998adb1ea9fd998afd4dafd372d3d4729a54b/DEPS


### sh...@chromium.org (2017-01-12)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-23)

Nice one! The panel awarded $3,000 for this report!

### aw...@chromium.org (2017-01-23)

[Empty comment from Monorail migration]

### st...@gmail.com (2017-01-24)

When you're going to release a new version of Chrome, please use the following text as the credit information. Thanks.

Ke Liu (@klotxl) of Tencent's Xuanwu LAB (http://xlab.tencent.com/)


### aw...@chromium.org (2017-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-17)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), bhthompson@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2017-03-21)

mbarbella@, any idea why sheriffbot@ is requesting 58 merge? Can't see how it's needed.

### mb...@chromium.org (2017-03-21)

I see what's happening, but I'm not totally sure what the best way to fix this is. Will follow up with you off-bug.

### aw...@google.com (2017-03-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### 92...@gmail.com (2017-04-27)

How can I download minimized testcase? Any suggestions? 
Greate thanks~~~~

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/678461?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086412)*
