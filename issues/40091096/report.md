# Security: PDFium UAF in CFGAS_FontMgr::FindFont

| Field | Value |
|-------|-------|
| **Issue ID** | [40091096](https://issues.chromium.org/issues/40091096) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2018-04-13 |
| **Bounty** | $5,500.00 |

## Description

**VULNERABILITY DETAILS**

An UAF issue was found in CFGAS\_FontMgr::FindFont in xfa/fgas/font/cfgas\_fontmgr.cpp.

This issue was introduced by <https://pdfium.googlesource.com/pdfium/+/53279b1dcabae4913f7f0a58e741942e82ab7d59%5E%21/>

The root cause is that in function EnumGdiFonts, a temporary variable was returned.

```
std::deque<FX_FONTDESCRIPTOR> EnumGdiFonts(const wchar_t\* pwsFaceName,  
                                           wchar_t wUnicode) {  
  std::deque<FX_FONTDESCRIPTOR> fonts;      // ----> temporary variable  
  LOGFONTW lfFind;  
  memset(&lfFind, 0, sizeof(lfFind));  
  lfFind.lfCharSet = DEFAULT_CHARSET;  
  if (pwsFaceName) {  
    FXSYS_wcsncpy(lfFind.lfFaceName, pwsFaceName, 31);  
    lfFind.lfFaceName[31] = 0;  
  }  
  HDC hDC = ::GetDC(nullptr);  
  EnumFontFamiliesExW(hDC, (LPLOGFONTW)&lfFind, (FONTENUMPROCW)GdiFontEnumProc,  
                      (LPARAM)&fonts, 0);  
  ::ReleaseDC(nullptr, hDC);  
  return fonts;                             // ----> returned  
}  

```

The return value was referenced as a parameter in function MatchDefaultFont.

```
const FX_FONTDESCRIPTOR\* MatchDefaultFont(  
    FX_FONTMATCHPARAMS\* pParams,  
    const std::deque<FX_FONTDESCRIPTOR>& fonts) {   // ----> const reference  
    // ......  
}  

```

However, the temporary variable was freed once we reached the next line since it's an anonymous object.

```
const FX_FONTDESCRIPTOR\* CFGAS_FontMgr::FindFont(const wchar_t\* pszFontFamily,  
                                                 uint32_t dwFontStyles,  
                                                 bool matchParagraphStyle,  
                                                 uint16_t wCodePage,  
                                                 uint32_t dwUSB,  
                                                 wchar_t wUnicode) {  
  FX_FONTMATCHPARAMS params;  
  memset(&params, 0, sizeof(params));  
  params.dwUSB = dwUSB;  
  params.wUnicode = wUnicode;  
  params.wCodePage = wCodePage;  
  params.pwsFamily = pszFontFamily;  
  params.dwFontStyles = dwFontStyles;  
  params.matchParagraphStyle = matchParagraphStyle;  
  
  const FX_FONTDESCRIPTOR\* pDesc = MatchDefaultFont(&params, m_FontFaces);  
  if (pDesc)  
    return pDesc;  
  
  if (!pszFontFamily)  
    return nullptr;  
  
  params.pwsFamily = nullptr;  
  pDesc = MatchDefaultFont(&params, EnumGdiFonts(pszFontFamily, wUnicode)); // ----> Freed after this line  
  if (!pDesc)  
    return nullptr;  
  
  auto it = std::find(m_FontFaces.rbegin(), m_FontFaces.rend(), \*pDesc);    // ----> UAF  
  if (it != m_FontFaces.rend())  
    return &\*it;  
  
  m_FontFaces.push_back(\*pDesc);  
  return &m_FontFaces.back();  
}  

```

Patch suggestion:  

(1) In function MatchDefaultFont, create a temporary variable to store the returned value of EnumGdiFonts.  

(2) Alternatively, add a reference parameter for function EnumGdiFonts to retrieve the 'returned' value. Just as the original code did.

# ASAN log:

==13128==ERROR: AddressSanitizer: heap-use-after-free on address 0x070258e4 at pc 0x033e541b bp 0x0017cb5c sp 0x0017cb50  

READ of size 1 at 0x070258e4 thread T0  

==13128==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==13128==\*\*\* Most likely this means that the app is already \*\*\*  

==13128==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==13128==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==13128==\*\*\* or produce wrong results. \*\*\*  

#0 0x33e541a in std::\_Find\_unchecked<std::reverse\_iterator<std::\_Deque\_iterator<std::\_Deque\_val<std::\_Deque\_simple\_types<FX\_FONTDESCRIPTOR> > > >,FX\_FONTDESCRIPTOR> C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Tools\MSVC\14.13.26128\include\xutility:3499  

#1 0x33dd88d in std::find<std::reverse\_iterator<std::\_Deque\_iterator<std::\_Deque\_val<std::\_Deque\_simple\_types<FX\_FONTDESCRIPTOR> > > >,FX\_FONTDESCRIPTOR> C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Tools\MSVC\14.13.26128\include\xutility:3507  

#2 0x33dc9ee in CFGAS\_FontMgr::FindFont C:\pdfium\xfa\fgas\font\cfgas\_fontmgr.cpp:237  

#3 0x33dff29 in CFGAS\_FontMgr::LoadFont C:\pdfium\xfa\fgas\font\cfgas\_fontmgr.cpp:1099  

#4 0x33ee775 in CFGAS\_DefaultFontManager::GetFont C:\pdfium\xfa\fgas\font\cfgas\_defaultfontmanager.cpp:21  

#5 0x2f42a97 in CXFA\_FontMgr::GetFont C:\pdfium\xfa\fxfa\cxfa\_fontmgr.cpp:48  

#6 0x2f855eb in CXFA\_TextParser::GetFont C:\pdfium\xfa\fxfa\cxfa\_textparser.cpp:354  

#7 0x2f695aa in CXFA\_TextLayout::CreateBreak C:\pdfium\xfa\fxfa\cxfa\_textlayout.cpp:102  

#8 0x2f6b0dd in CXFA\_TextLayout::CalcSize C:\pdfium\xfa\fxfa\cxfa\_textlayout.cpp:387  

#9 0x2f6b860 in CXFA\_TextLayout::StartLayout C:\pdfium\xfa\fxfa\cxfa\_textlayout.cpp:293  

#10 0x2fb2414 in CXFA\_Node::StartTextLayout C:\pdfium\xfa\fxfa\parser\cxfa\_node.cpp:3424  

#11 0x2fb1bed in CXFA\_Node::StartWidgetLayout C:\pdfium\xfa\fxfa\parser\cxfa\_node.cpp:3055  

#12 0x2f4eced in CXFA\_FFNotify::StartFieldDrawLayout C:\pdfium\xfa\fxfa\cxfa\_ffnotify.cpp:199  

#13 0x3048bd6 in CXFA\_ItemLayoutProcessor::DoLayoutField C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2197  

#14 0x30362bb in CXFA\_ItemLayoutProcessor::DoLayout C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2242  

#15 0x30370af in CXFA\_ItemLayoutProcessor::DoLayoutPositionedContainer C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:1163  

#16 0x3036317 in CXFA\_ItemLayoutProcessor::DoLayout C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2231  

#17 0x3039a38 in CXFA\_ItemLayoutProcessor::DoLayoutTableContainer C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:1283  

#18 0x30363b9 in CXFA\_ItemLayoutProcessor::DoLayout C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2235  

#19 0x30370af in CXFA\_ItemLayoutProcessor::DoLayoutPositionedContainer C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:1163  

#20 0x3036317 in CXFA\_ItemLayoutProcessor::DoLayout C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2231  

#21 0x3043d38 in CXFA\_ItemLayoutProcessor::InsertFlowedItem C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2524  

#22 0x304059d in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:1958  

#23 0x30363aa in CXFA\_ItemLayoutProcessor::DoLayout C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2224  

#24 0x2fe9015 in CXFA\_LayoutProcessor::DoLayout C:\pdfium\xfa\fxfa\parser\cxfa\_layoutprocessor.cpp:74  

#25 0x2f2c52a in CXFA\_FFDocView::DoLayout C:\pdfium\xfa\fxfa\cxfa\_ffdocview.cpp:94  

#26 0x2f02e98 in CPDFXFA\_Context::LoadXFADoc C:\pdfium\fpdfsdk\fpdfxfa\cpdfxfa\_context.cpp:113  

#27 0x24e4e05 in FPDF\_LoadXFA C:\pdfium\fpdfsdk\fpdf\_view.cpp:251  

#28 0x924138 in main C:\pdfium\samples\pdfium\_test.cc:902  

#29 0x354877a in \_\_scrt\_common\_main\_seh f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl:283  

#30 0x7627343c in BaseThreadInitThunk+0x11 (C:\Windows\syswow64\kernel32.dll+0x7dd7343c)  

#31 0x77e99831 in RtlInitializeExceptionChain+0x62 (C:\Windows\SysWOW64\ntdll.dll+0x7dea9831)  

#32 0x77e99804 in RtlInitializeExceptionChain+0x35 (C:\Windows\SysWOW64\ntdll.dll+0x7dea9804)

0x070258e4 is located 68 bytes inside of 96-byte region [0x070258a0,0x07025900)  

freed by thread T0 here:  

#0 0x3535388 in free c:\b\rr\tmpkmvu8v\w\src\third\_party\llvm\projects\compiler-rt\lib\asan\asan\_malloc\_win.cc:44  

#1 0x3547c48 in operator delete f:\dd\vctools\crt\vcstartup\src\heap\delete\_scalar\_size.cpp:30  

#2 0x33e28fd in std::deque<FX\_FONTDESCRIPTOR,std::allocator<FX\_FONTDESCRIPTOR> >::\_Tidy C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Tools\MSVC\14.13.26128\include\deque:1935  

#3 0x33dc7c1 in CFGAS\_FontMgr::FindFont C:\pdfium\xfa\fgas\font\cfgas\_fontmgr.cpp:233  

#4 0x33dff29 in CFGAS\_FontMgr::LoadFont C:\pdfium\xfa\fgas\font\cfgas\_fontmgr.cpp:1099  

#5 0x33ee775 in CFGAS\_DefaultFontManager::GetFont C:\pdfium\xfa\fgas\font\cfgas\_defaultfontmanager.cpp:21  

#6 0x2f42a97 in CXFA\_FontMgr::GetFont C:\pdfium\xfa\fxfa\cxfa\_fontmgr.cpp:48  

#7 0x2f855eb in CXFA\_TextParser::GetFont C:\pdfium\xfa\fxfa\cxfa\_textparser.cpp:354  

#8 0x2f695aa in CXFA\_TextLayout::CreateBreak C:\pdfium\xfa\fxfa\cxfa\_textlayout.cpp:102  

#9 0x2f6b0dd in CXFA\_TextLayout::CalcSize C:\pdfium\xfa\fxfa\cxfa\_textlayout.cpp:387  

#10 0x2f6b860 in CXFA\_TextLayout::StartLayout C:\pdfium\xfa\fxfa\cxfa\_textlayout.cpp:293  

#11 0x2fb2414 in CXFA\_Node::StartTextLayout C:\pdfium\xfa\fxfa\parser\cxfa\_node.cpp:3424  

#12 0x2fb1bed in CXFA\_Node::StartWidgetLayout C:\pdfium\xfa\fxfa\parser\cxfa\_node.cpp:3055  

#13 0x2f4eced in CXFA\_FFNotify::StartFieldDrawLayout C:\pdfium\xfa\fxfa\cxfa\_ffnotify.cpp:199  

#14 0x3048bd6 in CXFA\_ItemLayoutProcessor::DoLayoutField C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2197  

#15 0x30362bb in CXFA\_ItemLayoutProcessor::DoLayout C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2242  

#16 0x30370af in CXFA\_ItemLayoutProcessor::DoLayoutPositionedContainer C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:1163  

#17 0x3036317 in CXFA\_ItemLayoutProcessor::DoLayout C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2231  

#18 0x3039a38 in CXFA\_ItemLayoutProcessor::DoLayoutTableContainer C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:1283  

#19 0x30363b9 in CXFA\_ItemLayoutProcessor::DoLayout C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2235  

#20 0x30370af in CXFA\_ItemLayoutProcessor::DoLayoutPositionedContainer C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:1163  

#21 0x3036317 in CXFA\_ItemLayoutProcessor::DoLayout C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2231  

#22 0x3043d38 in CXFA\_ItemLayoutProcessor::InsertFlowedItem C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2524  

#23 0x304059d in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:1958  

#24 0x30363aa in CXFA\_ItemLayoutProcessor::DoLayout C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2224  

#25 0x2fe9015 in CXFA\_LayoutProcessor::DoLayout C:\pdfium\xfa\fxfa\parser\cxfa\_layoutprocessor.cpp:74  

#26 0x2f2c52a in CXFA\_FFDocView::DoLayout C:\pdfium\xfa\fxfa\cxfa\_ffdocview.cpp:94  

#27 0x2f02e98 in CPDFXFA\_Context::LoadXFADoc C:\pdfium\fpdfsdk\fpdfxfa\cpdfxfa\_context.cpp:113  

#28 0x24e4e05 in FPDF\_LoadXFA C:\pdfium\fpdfsdk\fpdf\_view.cpp:251

previously allocated by thread T0 here:  

#0 0x353546c in malloc c:\b\rr\tmpkmvu8v\w\src\third\_party\llvm\projects\compiler-rt\lib\asan\asan\_malloc\_win.cc:60  

#1 0x3547c16 in operator new f:\dd\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:34  

#2 0x33de031 in std::deque<FX\_FONTDESCRIPTOR,std::allocator<FX\_FONTDESCRIPTOR> >::push\_back C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Tools\MSVC\14.13.26128\include\deque:1536  

#3 0x33e056e in `anonymous namespace'::GdiFontEnumProc C:\pdfium\xfa\fgas\font\cfgas_fontmgr.cpp:179 #4 0x75e4c630 in CreateICW+0xf8 (C:\Windows\syswow64\GDI32.dll+0x7dacc630) #5 0x75e4c708 in EnumFontFamiliesExW+0x2f (C:\Windows\syswow64\GDI32.dll+0x7dacc708) #6 0x33dc2be in` anonymous namespace'::EnumGdiFonts C:\pdfium\xfa\fgas\font\cfgas\_fontmgr.cpp:194  

#7 0x33dc7af in CFGAS\_FontMgr::FindFont C:\pdfium\xfa\fgas\font\cfgas\_fontmgr.cpp:233  

#8 0x33dff29 in CFGAS\_FontMgr::LoadFont C:\pdfium\xfa\fgas\font\cfgas\_fontmgr.cpp:1099  

#9 0x33ee775 in CFGAS\_DefaultFontManager::GetFont C:\pdfium\xfa\fgas\font\cfgas\_defaultfontmanager.cpp:21  

#10 0x2f42a97 in CXFA\_FontMgr::GetFont C:\pdfium\xfa\fxfa\cxfa\_fontmgr.cpp:48  

#11 0x2f855eb in CXFA\_TextParser::GetFont C:\pdfium\xfa\fxfa\cxfa\_textparser.cpp:354  

#12 0x2f695aa in CXFA\_TextLayout::CreateBreak C:\pdfium\xfa\fxfa\cxfa\_textlayout.cpp:102  

#13 0x2f6b0dd in CXFA\_TextLayout::CalcSize C:\pdfium\xfa\fxfa\cxfa\_textlayout.cpp:387  

#14 0x2f6b860 in CXFA\_TextLayout::StartLayout C:\pdfium\xfa\fxfa\cxfa\_textlayout.cpp:293  

#15 0x2fb2414 in CXFA\_Node::StartTextLayout C:\pdfium\xfa\fxfa\parser\cxfa\_node.cpp:3424  

#16 0x2fb1bed in CXFA\_Node::StartWidgetLayout C:\pdfium\xfa\fxfa\parser\cxfa\_node.cpp:3055  

#17 0x2f4eced in CXFA\_FFNotify::StartFieldDrawLayout C:\pdfium\xfa\fxfa\cxfa\_ffnotify.cpp:199  

#18 0x3048bd6 in CXFA\_ItemLayoutProcessor::DoLayoutField C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2197  

#19 0x30362bb in CXFA\_ItemLayoutProcessor::DoLayout C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2242  

#20 0x30370af in CXFA\_ItemLayoutProcessor::DoLayoutPositionedContainer C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:1163  

#21 0x3036317 in CXFA\_ItemLayoutProcessor::DoLayout C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2231  

#22 0x3039a38 in CXFA\_ItemLayoutProcessor::DoLayoutTableContainer C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:1283  

#23 0x30363b9 in CXFA\_ItemLayoutProcessor::DoLayout C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2235  

#24 0x30370af in CXFA\_ItemLayoutProcessor::DoLayoutPositionedContainer C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:1163  

#25 0x3036317 in CXFA\_ItemLayoutProcessor::DoLayout C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2231  

#26 0x3043d38 in CXFA\_ItemLayoutProcessor::InsertFlowedItem C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2524  

#27 0x304059d in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:1958  

#28 0x30363aa in CXFA\_ItemLayoutProcessor::DoLayout C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2224

SUMMARY: AddressSanitizer: heap-use-after-free C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Tools\MSVC\14.13.26128\include\xutility:3499 in std::\_Find\_unchecked<std::reverse\_iterator<std::\_Deque\_iterator<std::\_Deque\_val<std::\_Deque\_simple\_types<FX\_FONTDESCRIPTOR> > > >,FX\_FONTDESCRIPTOR>  

Shadow bytes around the buggy address:  

0x30e04ac0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x30e04ad0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x30e04ae0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x30e04af0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x30e04b00: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x30e04b10: fa fa fa fa fd fd fd fd fd fd fd fd[fd]fd fd fd  

0x30e04b20: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 fa  

0x30e04b30: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 fa  

0x30e04b40: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 fa  

0x30e04b50: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 fa  

0x30e04b60: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 fa  

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

==13128==ABORTING

**VERSION**  

Chrome Version: pdfium with XFA enabled  

Operating System: All

**REPRODUCTION CASE**  

A proof-of-concept file which can trigger the crash was attached.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### st...@gmail.com (2018-04-13)

Some of the build arguments:

```
pdf_enable_xfa = true
pdf_enable_v8 = true
is_asan=true
```

### st...@gmail.com (2018-04-13)

I submitted a CL at https://pdfium-review.googlesource.com/c/pdfium/+/30570

### th...@chromium.org (2018-04-13)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### ca...@chromium.org (2018-04-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-04-16)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/d5624a47bcaad45f6fcb30ad03b6e474f5cee17e

commit d5624a47bcaad45f6fcb30ad03b6e474f5cee17e
Author: Ke Liu <stackexploit@gmail.com>
Date: Mon Apr 16 05:19:07 2018

Fix UAF in CFGAS_FontMgr::FindFont

Fix an use-after-free issue which was introduced by
commit 53279b1dcabae4913f7f0a58e741942e82ab7d59.

Bug: chromium:832589
Change-Id: Id7da791c3aa2d71d0a9e56d062069f41b7eb48d1
Reviewed-on: https://pdfium-review.googlesource.com/30570
Commit-Queue: Lei Zhang <thestig@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>

[modify] https://crrev.com/d5624a47bcaad45f6fcb30ad03b6e474f5cee17e/xfa/fgas/font/cfgas_fontmgr.cpp


### bu...@chromium.org (2018-04-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d0e2e34043503af030286ed6eef255c864d2dd69

commit d0e2e34043503af030286ed6eef255c864d2dd69
Author: pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Date: Mon Apr 16 06:31:16 2018

Roll src/third_party/pdfium/ b71d24c1a..d5624a47b (1 commit)

https://pdfium.googlesource.com/pdfium.git/+log/b71d24c1affe..d5624a47bcaa

$ git log b71d24c1a..d5624a47b --date=short --no-merges --format='%ad %ae %s'
2018-04-16 stackexploit Fix UAF in CFGAS_FontMgr::FindFont

Created with:
  roll-dep src/third_party/pdfium
BUG=chromium:832589


The AutoRoll server is located here: https://pdfium-roll.skia.org

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.


TBR=dsinclair@chromium.org

Change-Id: Ia438998e67a9a01581120da381761354ad454962
Reviewed-on: https://chromium-review.googlesource.com/1012725
Commit-Queue: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Reviewed-by: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#550942}
[modify] https://crrev.com/d0e2e34043503af030286ed6eef255c864d2dd69/DEPS


### bu...@chromium.org (2018-04-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d0e2e34043503af030286ed6eef255c864d2dd69

commit d0e2e34043503af030286ed6eef255c864d2dd69
Author: pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Date: Mon Apr 16 06:31:16 2018

Roll src/third_party/pdfium/ b71d24c1a..d5624a47b (1 commit)

https://pdfium.googlesource.com/pdfium.git/+log/b71d24c1affe..d5624a47bcaa

$ git log b71d24c1a..d5624a47b --date=short --no-merges --format='%ad %ae %s'
2018-04-16 stackexploit Fix UAF in CFGAS_FontMgr::FindFont

Created with:
  roll-dep src/third_party/pdfium
BUG=chromium:832589


The AutoRoll server is located here: https://pdfium-roll.skia.org

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.


TBR=dsinclair@chromium.org

Change-Id: Ia438998e67a9a01581120da381761354ad454962
Reviewed-on: https://chromium-review.googlesource.com/1012725
Commit-Queue: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Reviewed-by: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#550942}
[modify] https://crrev.com/d0e2e34043503af030286ed6eef255c864d2dd69/DEPS


### ds...@chromium.org (2018-04-18)

Passing to thestig@ as I believe they reviewed the relevant CLs.

### sh...@chromium.org (2018-04-18)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2018-04-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-19)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-04-27)

Nice one! The VRP panel decided to award $5,500 for this report - thanks as ever!

### aw...@chromium.org (2018-04-27)

[Empty comment from Monorail migration]

### ts...@chromium.org (2018-05-02)

XFA not shipped.

### ts...@chromium.org (2018-05-02)

[Empty comment from Monorail migration]

### ds...@chromium.org (2018-05-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-07-26)

This issue was migrated from crbug.com/chromium/832589?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/62400]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091096)*
