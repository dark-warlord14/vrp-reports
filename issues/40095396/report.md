# Security: PDFium Font Parsing Heap Use After Free Vulnerability

| Field | Value |
|-------|-------|
| **Issue ID** | [40095396](https://issues.chromium.org/issues/40095396) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-06-14 |
| **Bounty** | $3,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/master/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

This issue affects the lastest version of PDFium ( <https://pdfium.googlesource.com/pdfium/+/refs/heads/master> ). When enabling ASAN, pdfium\_test.exe shows the following log.

# Rendering PDF file C:\poc.pdf.

==11764==ERROR: AddressSanitizer: heap-use-after-free on address 0x06bee95c at pc 0x00d62259 bp 0x0015de28 sp 0x0015de1c  

READ of size 1 at 0x06bee95c thread T0  

#0 0xd62258 in tt\_cmap4\_char\_map\_binary C:\pdfium\third\_party\freetype\src\src\sfnt\ttcmap.c:1238  

#1 0xd4be6a in tt\_cmap4\_char\_index C:\pdfium\third\_party\freetype\src\src\sfnt\ttcmap.c:1492  

#2 0xcca275 in FT\_Get\_Char\_Index C:\pdfium\third\_party\freetype\src\src\base\ftobjs.c:3728  

#3 0xff9aad in CPDF\_CIDFont::GetGlyphIndex C:\pdfium\core\fpdfapi\font\cpdf\_cidfont.cpp:558  

#4 0xff8bc5 in CPDF\_CIDFont::GlyphFromCharCode C:\pdfium\core\fpdfapi\font\cpdf\_cidfont.cpp:696  

#5 0xff7535 in CPDF\_CIDFont::GetCharBBox C:\pdfium\core\fpdfapi\font\cpdf\_cidfont.cpp:428  

#6 0x1120756 in CPDF\_TextObject::CalcPositionData C:\pdfium\core\fpdfapi\page\cpdf\_textobject.cpp:226  

#7 0x110eae0 in CPDF\_StreamContentParser::AddTextObject C:\pdfium\core\fpdfapi\page\cpdf\_streamcontentparser.cpp:1255  

#8 0x1105ae0 in CPDF\_StreamContentParser::Handle\_ShowText C:\pdfium\core\fpdfapi\page\cpdf\_streamcontentparser.cpp:1288  

#9 0x1109293 in CPDF\_StreamContentParser::OnOperator C:\pdfium\core\fpdfapi\page\cpdf\_streamcontentparser.cpp:568  

#10 0x110fa78 in CPDF\_StreamContentParser::Parse C:\pdfium\core\fpdfapi\page\cpdf\_streamcontentparser.cpp:1537  

#11 0x10b9513 in CPDF\_ContentParser::Parse C:\pdfium\core\fpdfapi\page\cpdf\_contentparser.cpp:201  

#12 0x10b84fc in CPDF\_ContentParser::Continue C:\pdfium\core\fpdfapi\page\cpdf\_contentparser.cpp:122  

#13 0x10ee89b in CPDF\_PageObjectHolder::ContinueParse C:\pdfium\core\fpdfapi\page\cpdf\_pageobjectholder.cpp:65  

#14 0x10ec086 in CPDF\_Page::ParseContent C:\pdfium\core\fpdfapi\page\cpdf\_page.cpp:79  

#15 0xc7b59a in FPDF\_LoadPage C:\pdfium\fpdfsdk\fpdf\_view.cpp:359  

#16 0xc207d7 in `anonymous namespace'::GetPageForIndex C:\pdfium\samples\pdfium_test.cc:571 #17 0xc05a3e in` anonymous namespace'::RenderPdf C:\pdfium\samples\pdfium\_test.cc:854  

#18 0xc03a7d in main C:\pdfium\samples\pdfium\_test.cc:1039  

#19 0x139303a in \_\_scrt\_common\_main\_seh d:\agent\_work\2\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#20 0x763b343c in BaseThreadInitThunk+0x11 (C:\Windows\syswow64\kernel32.dll+0x7dd7343c)  

#21 0x776c9801 in RtlInitializeExceptionChain+0x62 (C:\Windows\SysWOW64\ntdll.dll+0x7dea9801)  

#22 0x776c97d4 in RtlInitializeExceptionChain+0x35 (C:\Windows\SysWOW64\ntdll.dll+0x7dea97d4)

0x06bee95c is located 6213980 bytes inside of 15323200-byte region [0x06601800,0x0749e840)  

freed by thread T0 here:  

#0 0x137cf49 in free c:\b\s\w\ir\k\src\third\_party\llvm\projects\compiler-rt\lib\asan\asan\_malloc\_win.cc:52  

#1 0xf505ab in CTTFontDesc::~CTTFontDesc C:\pdfium\core\fxge\cttfontdesc.cpp:15  

#2 0xf2be08 in std::unique\_ptr<CTTFontDesc,std::default\_delete<CTTFontDesc> >::reset C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Tools\MSVC\14.16.27023\include\memory:2333  

#3 0xf29235 in CFX\_FontMgr::AddCachedTTCFace C:\pdfium\core\fxge\cfx\_fontmgr.cpp:180  

#4 0xf24aba in CFX\_FontMapper::GetCachedTTCFace C:\pdfium\core\fxge\cfx\_fontmapper.cpp:693  

#5 0xf225ca in CFX\_FontMapper::FindSubstFont C:\pdfium\core\fxge\cfx\_fontmapper.cpp:629  

#6 0xf275b7 in CFX\_FontMgr::FindSubstFont C:\pdfium\core\fxge\cfx\_fontmgr.cpp:108  

#7 0xf150c5 in CFX\_Font::LoadSubst C:\pdfium\core\fxge\cfx\_font.cpp:352  

#8 0x10110e4 in CPDF\_SimpleFont::LoadSubstFont C:\pdfium\core\fpdfapi\font\cpdf\_simplefont.cpp:270  

#9 0x10107b3 in CPDF\_SimpleFont::LoadCommon C:\pdfium\core\fpdfapi\font\cpdf\_simplefont.cpp:218  

#10 0x1008727 in CPDF\_Font::Create C:\pdfium\core\fpdfapi\font\cpdf\_font.cpp:332  

#11 0x10bfbe3 in CPDF\_DocPageData::GetFont C:\pdfium\core\fpdfapi\page\cpdf\_docpagedata.cpp:257  

#12 0x110e121 in CPDF\_StreamContentParser::FindFont C:\pdfium\core\fpdfapi\page\cpdf\_streamcontentparser.cpp:1166  

#13 0x11058cc in CPDF\_StreamContentParser::Handle\_SetFont C:\pdfium\core\fpdfapi\page\cpdf\_streamcontentparser.cpp:1131  

#14 0x1109293 in CPDF\_StreamContentParser::OnOperator C:\pdfium\core\fpdfapi\page\cpdf\_streamcontentparser.cpp:568  

#15 0x110fa78 in CPDF\_StreamContentParser::Parse C:\pdfium\core\fpdfapi\page\cpdf\_streamcontentparser.cpp:1537  

#16 0x10b9513 in CPDF\_ContentParser::Parse C:\pdfium\core\fpdfapi\page\cpdf\_contentparser.cpp:201  

#17 0x10b84fc in CPDF\_ContentParser::Continue C:\pdfium\core\fpdfapi\page\cpdf\_contentparser.cpp:122  

#18 0x10ee89b in CPDF\_PageObjectHolder::ContinueParse C:\pdfium\core\fpdfapi\page\cpdf\_pageobjectholder.cpp:65  

#19 0x10ec086 in CPDF\_Page::ParseContent C:\pdfium\core\fpdfapi\page\cpdf\_page.cpp:79  

#20 0xc7b59a in FPDF\_LoadPage C:\pdfium\fpdfsdk\fpdf\_view.cpp:359  

#21 0xc207d7 in `anonymous namespace'::GetPageForIndex C:\pdfium\samples\pdfium_test.cc:571 #22 0xc05a3e in` anonymous namespace'::RenderPdf C:\pdfium\samples\pdfium\_test.cc:854  

#23 0xc03a7d in main C:\pdfium\samples\pdfium\_test.cc:1039  

#24 0x139303a in \_\_scrt\_common\_main\_seh d:\agent\_work\2\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#25 0x763b343c in BaseThreadInitThunk+0x11 (C:\Windows\syswow64\kernel32.dll+0x7dd7343c)  

#26 0x776c9801 in RtlInitializeExceptionChain+0x62 (C:\Windows\SysWOW64\ntdll.dll+0x7dea9801)  

#27 0x776c97d4 in RtlInitializeExceptionChain+0x35 (C:\Windows\SysWOW64\ntdll.dll+0x7dea97d4)

previously allocated by thread T0 here:  

#0 0x137d169 in calloc c:\b\s\w\ir\k\src\third\_party\llvm\projects\compiler-rt\lib\asan\asan\_malloc\_win.cc:84  

#1 0xf24992 in CFX\_FontMapper::GetCachedTTCFace C:\pdfium\core\fxge\cfx\_fontmapper.cpp:691  

#2 0xf225ca in CFX\_FontMapper::FindSubstFont C:\pdfium\core\fxge\cfx\_fontmapper.cpp:629  

#3 0xf275b7 in CFX\_FontMgr::FindSubstFont C:\pdfium\core\fxge\cfx\_fontmgr.cpp:108  

#4 0xf150c5 in CFX\_Font::LoadSubst C:\pdfium\core\fxge\cfx\_font.cpp:352  

#5 0xff7312 in CPDF\_CIDFont::LoadSubstFont C:\pdfium\core\fpdfapi\font\cpdf\_cidfont.cpp:759  

#6 0xff55f9 in CPDF\_CIDFont::Load C:\pdfium\core\fpdfapi\font\cpdf\_cidfont.cpp:396  

#7 0x1008727 in CPDF\_Font::Create C:\pdfium\core\fpdfapi\font\cpdf\_font.cpp:332  

#8 0x10bfbe3 in CPDF\_DocPageData::GetFont C:\pdfium\core\fpdfapi\page\cpdf\_docpagedata.cpp:257  

#9 0x110e121 in CPDF\_StreamContentParser::FindFont C:\pdfium\core\fpdfapi\page\cpdf\_streamcontentparser.cpp:1166  

#10 0x11058cc in CPDF\_StreamContentParser::Handle\_SetFont C:\pdfium\core\fpdfapi\page\cpdf\_streamcontentparser.cpp:1131  

#11 0x1109293 in CPDF\_StreamContentParser::OnOperator C:\pdfium\core\fpdfapi\page\cpdf\_streamcontentparser.cpp:568  

#12 0x110fa78 in CPDF\_StreamContentParser::Parse C:\pdfium\core\fpdfapi\page\cpdf\_streamcontentparser.cpp:1537  

#13 0x10b9513 in CPDF\_ContentParser::Parse C:\pdfium\core\fpdfapi\page\cpdf\_contentparser.cpp:201  

#14 0x10b84fc in CPDF\_ContentParser::Continue C:\pdfium\core\fpdfapi\page\cpdf\_contentparser.cpp:122  

#15 0x10ee89b in CPDF\_PageObjectHolder::ContinueParse C:\pdfium\core\fpdfapi\page\cpdf\_pageobjectholder.cpp:65  

#16 0x10ec086 in CPDF\_Page::ParseContent C:\pdfium\core\fpdfapi\page\cpdf\_page.cpp:79  

#17 0xc7b59a in FPDF\_LoadPage C:\pdfium\fpdfsdk\fpdf\_view.cpp:359  

#18 0xc207d7 in `anonymous namespace'::GetPageForIndex C:\pdfium\samples\pdfium_test.cc:571 #19 0xc05a3e in` anonymous namespace'::RenderPdf C:\pdfium\samples\pdfium\_test.cc:854  

#20 0xc03a7d in main C:\pdfium\samples\pdfium\_test.cc:1039  

#21 0x139303a in \_\_scrt\_common\_main\_seh d:\agent\_work\2\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#22 0x763b343c in BaseThreadInitThunk+0x11 (C:\Windows\syswow64\kernel32.dll+0x7dd7343c)  

#23 0x776c9801 in RtlInitializeExceptionChain+0x62 (C:\Windows\SysWOW64\ntdll.dll+0x7dea9801)  

#24 0x776c97d4 in RtlInitializeExceptionChain+0x35 (C:\Windows\SysWOW64\ntdll.dll+0x7dea97d4)

SUMMARY: AddressSanitizer: heap-use-after-free C:\pdfium\third\_party\freetype\src\src\sfnt\ttcmap.c:1238 in tt\_cmap4\_char\_map\_binary  

Shadow bytes around the buggy address:  

0x30d7dcd0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x30d7dce0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x30d7dcf0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x30d7dd00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x30d7dd10: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x30d7dd20: fd fd fd fd fd fd fd fd fd fd fd[fd]fd fd fd fd  

0x30d7dd30: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x30d7dd40: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x30d7dd50: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x30d7dd60: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x30d7dd70: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

Shadow gap: cc  

==11764==ABORTING

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

- [poc.pdf](attachments/poc.pdf) (application/pdf, 45.3 KB)

## Timeline

### cl...@chromium.org (2019-06-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6431982745157632.

### cl...@chromium.org (2019-06-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-06-14)

Testcase 6431982745157632 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6431982745157632.

### me...@chromium.org (2019-06-14)

Tom, can you PTAL?

[Monorail components: Internals>Plugins>PDF]

### me...@chromium.org (2019-06-14)

[Empty comment from Monorail migration]

### me...@chromium.org (2019-06-14)

[Empty comment from Monorail migration]

### ts...@chromium.org (2019-06-14)

Did not reproduce in either pdfium_test or Asanified chrome built with xfa at PDFium revision c7a9124ee6bd6a. 
Can you give us a specific revision (as from git log) for the pdfium you used (rather than just HEAD)? Thanks.

### ts...@chromium.org (2019-06-14)

Lei, want to give this a quick attempt on windows?  Maybe windows specific font code?


### th...@chromium.org (2019-06-15)

https://pdfium-review.googlesource.com/c/pdfium/+/56351

### th...@chromium.org (2019-06-15)

Well, that and potentially the next CL in the chain. I will check on Windows shortly.

### th...@chromium.org (2019-06-15)

- Can repro on ToT on Windows.
- Regressed in https://pdfium-review.googlesource.com/c/pdfium/+/56351
- https://pdfium-review.googlesource.com/c/pdfium/+/56351 makes the issue go away.

### th...@chromium.org (2019-06-15)

Erm, bad copy and paste in https://crbug.com/chromium/974091#c11. Regressed in https://pdfium-review.googlesource.com/c/pdfium/+/54790, which rolled into Chromium in r668527. Thus only some 77.x builds are affected.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-06-15)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/7e5908802f90d171145b4531d11814332dd3ce75

commit 7e5908802f90d171145b4531d11814332dd3ce75
Author: Tom Sepez <tsepez@chromium.org>
Date: Sat Jun 15 00:34:30 2019

Temporary not living long enough in cfx_fontmgr.cpp.

Since CTTFontDesc::SetFace() isn't going to prolong the life of
its CFX_Face argument, it shouldn't take a RetainPtr reference.
Making that change shows that the result of GetFixedFace() needs
to be assigned to and returned from a local.

Broken in https://pdfium-review.googlesource.com/c/pdfium/+/54790
Noticed while investigating linked bug, but probably a different problem.

Bug: chromium:974091
Change-Id: Ife76e82f5176f20586282da14ddb6ca1d66676e8
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/56351
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>

[modify] https://crrev.com/7e5908802f90d171145b4531d11814332dd3ce75/core/fxge/cfx_fontmgr.cpp
[modify] https://crrev.com/7e5908802f90d171145b4531d11814332dd3ce75/core/fxge/cttfontdesc.h
[modify] https://crrev.com/7e5908802f90d171145b4531d11814332dd3ce75/core/fxge/cttfontdesc.cpp


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-06-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d6de67e84d755f2d2d4e74896c706309c0431e91

commit d6de67e84d755f2d2d4e74896c706309c0431e91
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Sat Jun 15 02:07:42 2019

Roll src/third_party/pdfium e7731b3fb4bc..7e5908802f90 (1 commits)

https://pdfium.googlesource.com/pdfium.git/+log/e7731b3fb4bc..7e5908802f90


git log e7731b3fb4bc..7e5908802f90 --date=short --no-merges --format='%ad %ae %s'
2019-06-15 tsepez@chromium.org Temporary not living long enough in cfx_fontmgr.cpp.


Created with:
  gclient setdep -r src/third_party/pdfium@7e5908802f90

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:974091
TBR=pdfium-deps-rolls@chromium.org

Change-Id: Id0114a3d191d449c5925f10617616bb3d66b97d7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1661350
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#669469}

[modify] https://crrev.com/d6de67e84d755f2d2d4e74896c706309c0431e91/DEPS


### sh...@chromium.org (2019-06-15)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-06-17)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/63687a4e83865f415c71800152abc9932d2878f2

commit 63687a4e83865f415c71800152abc9932d2878f2
Author: Tom Sepez <tsepez@chromium.org>
Date: Mon Jun 17 21:13:30 2019

Speculative follow-up for bug_974091.

A failed return from GetFixedFace() might result in the eventual
freeing of a pre-existing CTTFontDesc, so check before adding a new one.
Additionally, split the Get/Add calls so that Get isn't duplicating
work performed by Add.

Bug: chromium:974091
Change-Id: I874f7a85f5c162cd6c4832141a7dac4f6cc8d2b8
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/56331
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>

[modify] https://crrev.com/63687a4e83865f415c71800152abc9932d2878f2/core/fxge/cfx_fontmgr.cpp


### ts...@chromium.org (2019-06-17)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-06-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8062b17f7150966906a8af7701ebfe62717318d5

commit 8062b17f7150966906a8af7701ebfe62717318d5
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Jun 18 03:27:51 2019

Roll src/third_party/pdfium 79b2847f611f..f0f9a8f1fd94 (7 commits)

https://pdfium.googlesource.com/pdfium.git/+log/79b2847f611f..f0f9a8f1fd94


git log 79b2847f611f..f0f9a8f1fd94 --date=short --no-merges --format='%ad %ae %s'
2019-06-18 chinsenj@google.com Split PDF_DataDecode() in two
2019-06-17 tsepez@chromium.org Remove CFX_FontMgr::InitFTLibrary.
2019-06-17 thestig@chromium.org Roll third_party/libjpeg_turbo/ 2a34770be..e1669e370 (3 commits)
2019-06-17 thestig@chromium.org Simplify font code.
2019-06-17 tsepez@chromium.org Introduce enum CFX_FontMapper::StandardFont.
2019-06-17 tsepez@chromium.org Speculative follow-up for bug_974091.
2019-06-17 tsepez@chromium.org Remove unimplemented CFX_FontMgr::ReleaseFace().


Created with:
  gclient setdep -r src/third_party/pdfium@f0f9a8f1fd94

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:922430,chromium:974091
TBR=pdfium-deps-rolls@chromium.org

Change-Id: I0d2299f2f36d81551ed3a2e81689923b6fe2bc66
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1663583
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#669958}

[modify] https://crrev.com/8062b17f7150966906a8af7701ebfe62717318d5/DEPS


### sh...@chromium.org (2019-06-18)

[Empty comment from Monorail migration]

### ts...@chromium.org (2019-06-18)

[Empty comment from Monorail migration]

### ts...@chromium.org (2019-06-18)

Also hit by CF at 976231

### ts...@chromium.org (2019-06-18)

And the CF one is slightly different.  Unmerging.

### cl...@chromium.org (2019-06-20)

ClusterFuzz testcase 5149845412773888 is verified as fixed in https://clusterfuzz.com/revisions?job=windows_libfuzzer_chrome_asan&range=670613:670644

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### na...@google.com (2019-06-24)

[Empty comment from Monorail migration]

### na...@google.com (2019-07-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-07-17)

Congrats! The Panel decided to reward $3,000 for this report!

### na...@google.com (2019-07-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-09-24)

This issue was migrated from crbug.com/chromium/974091?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/976231]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095396)*
