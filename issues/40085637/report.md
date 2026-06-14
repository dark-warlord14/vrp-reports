# Security: PDFium (XFA) Heap Buffer Overflow in CWeightTable::Calc

| Field | Value |
|-------|-------|
| **Issue ID** | [40085637](https://issues.chromium.org/issues/40085637) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | st...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2016-10-08 |
| **Bounty** | $3,500.00 |

## Description

**VULNERABILITY DETAILS**  

<https://crbug.com/chromium/619398> was not fixed properly but labeled as verified and security view restrictions have been removed.  

So I opened this new issue.  

The proof-of-concept files for <https://crbug.com/chromium/619398> have been deleted since it still can be reproducible.

The root cause of this issue is that the bounds check in function CWeightTable::Calc was insufficient. There were two patches related to the bounds check.

1. Lei Zhang (@thestig) submitted a patch for this issue at <https://pdfium.googlesource.com/pdfium/+/766901f5ec79b3c3ccd1e872f699642d771a89c5> on Aug 04.
2. I (Ke Liu, @stackexploit) submitted another patch to strengthen the bounds check at <https://pdfium.googlesource.com/pdfium/+/5aed0216ad6574944e76a95ef0dbbc910bab4a1a> on Sep 26.

Today I found that my patch (submitted on Sep 26) was insufficient too. The beginning address of array |PixelWeight.m\_Weights| can be changed dynamically. So we must calculate the array size dynamically too.

struct PixelWeight {  

int m\_SrcStart;  

int m\_SrcEnd;  

int m\_Weights[1]; // ----> The beginning address of this array can be changed dynamically  

};

44 size\_t CWeightTable::GetPixelWeightSize() const {  

45 return m\_dwWeightTablesSize / sizeof(int); // ----> Must be calculated dynamically  

46 }  

47

The solution is easy. The size of heap block |m\_pWeightTables| is |m\_dwWeightTablesSize| so we can get the end address of the it. Also, we can get the beginning address of array |PixelWeight.m\_Weights| directly. Then we can calculate the maximum array size dynamically.

size\_t CWeightTable::GetMaximumPixelWeightSize(PixelWeight\* pWeight) const {  

uint8\_t\* end\_addr = m\_pWeightTables + m\_dwWeightTablesSize;  

uint8\_t\* begin\_addr = reinterpret\_cast<uint8\_t\*>(&pWeight->m\_Weights);  

return (end\_addr - begin\_addr) / sizeof(pWeight->m\_Weights[0]);  

}

**VERSION**  

Chrome Version: PDFium with XFA enabled  

Operating System: All

**REPRODUCTION CASE**  

See attachments.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:  

==21787==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7fffa0f20704 at pc 0x0000020d090f bp 0x7fffffffd140 sp 0x7fffffffd138  

WRITE of size 4 at 0x7fffa0f20704 thread T0  

#0 0x20d090e in CWeightTable::Calc(int, int, int, int, int, int, int) core/fxge/dib/fx\_dib\_engine.cpp:245:36  

#1 0x20d6773 in CStretchEngine::StartStretchHorz() core/fxge/dib/fx\_dib\_engine.cpp:418:21  

#2 0x20d83d6 in CFX\_ImageStretcher::StartStretch() core/fxge/dib/fx\_dib\_engine.cpp:937:21  

#3 0x20d7932 in CFX\_ImageStretcher::Start() core/fxge/dib/fx\_dib\_engine.cpp:924:10  

#4 0x2080a74 in CFX\_ImageRenderer::Start(CFX\_DIBitmap\*, CFX\_ClipRgn const\*, CFX\_DIBSource const\*, int, unsigned int, CFX\_Matrix const\*, unsigned int, int, int, void\*, int) core/fxge/dib/fx\_dib\_main.cpp:1606:23  

#5 0x20c294b in CFX\_AggDeviceDriver::StartDIBits(CFX\_DIBSource const\*, int, unsigned int, CFX\_Matrix const\*, unsigned int, void\*&, int) core/fxge/agg/fx\_agg\_driver.cpp:1706:14  

#6 0x25f5113 in CXFA\_ImageRenderer::StartDIBSource() xfa/fxfa/app/xfa\_ffwidget.cpp:626:18  

#7 0x25f7986 in Start xfa/fxfa/app/xfa\_ffwidget.cpp:622:10  

#8 0x25f7986 in XFA\_DrawImage(CFX\_Graphics\*, CFX\_RTemplate<float> const&, CFX\_Matrix\*, CFX\_DIBitmap\*, int, int, int, int, int) xfa/fxfa/app/xfa\_ffwidget.cpp:899  

#9 0x27b1301 in CXFA\_FFImage::RenderWidget(CFX\_Graphics\*, CFX\_Matrix\*, unsigned int) xfa/fxfa/app/xfa\_ffimage.cpp:63:5  

#10 0x2614dd2 in CXFA\_RenderContext::DoRender(IFX\_Pause\*) xfa/fxfa/app/xfa\_rendercontext.cpp:60:16  

#11 0x1c4b41d in CPDFSDK\_PageView::PageView\_OnDraw(CFX\_RenderDevice\*, CFX\_Matrix\*, CPDF\_RenderOptions\*, FX\_RECT const&) fpdfsdk/cpdfsdk\_pageview.cpp:112:21  

#12 0x1c343ec in FFLCommon fpdfsdk/fpdfformfill.cpp:132:16  

#13 0x1c343ec in FPDF\_FFLDraw fpdfsdk/fpdfformfill.cpp:407  

#14 0x4f5da5 in RenderPage(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, void\*, void\*&, FPDF\_FORMFILLINFO\_PDFiumTest&, int, Options const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) samples/pdfium\_test.cc:594:5  

#15 0x4f735d in RenderPdf(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, char const\*, unsigned long, Options const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) samples/pdfium\_test.cc:786:9  

#16 0x4f8878 in main samples/pdfium\_test.cc:916:5  

#17 0x7ffff69d382f in \_\_libc\_start\_main /build/glibc-GKVZIf/glibc-2.23/csu/../csu/libc-start.c:291

0x7fffa0f20704 is located 0 bytes to the right of 335552260-byte region [0x7fff8cf1e800,0x7fffa0f20704)  

allocated by thread T0 here:  

#0 0x4c2573 in \_\_interceptor\_calloc (/pdfium/out/Debug/pdfium\_test+0x4c2573)  

#1 0x20cf31d in CWeightTable::Calc(int, int, int, int, int, int, int) core/fxge/dib/fx\_dib\_engine.cpp:70:21  

#2 0x20d6773 in CStretchEngine::StartStretchHorz() core/fxge/dib/fx\_dib\_engine.cpp:418:21  

#3 0x20d83d6 in CFX\_ImageStretcher::StartStretch() core/fxge/dib/fx\_dib\_engine.cpp:937:21  

#4 0x20d7932 in CFX\_ImageStretcher::Start() core/fxge/dib/fx\_dib\_engine.cpp:924:10  

#5 0x2080a74 in CFX\_ImageRenderer::Start(CFX\_DIBitmap\*, CFX\_ClipRgn const\*, CFX\_DIBSource const\*, int, unsigned int, CFX\_Matrix const\*, unsigned int, int, int, void\*, int) core/fxge/dib/fx\_dib\_main.cpp:1606:23  

#6 0x20c294b in CFX\_AggDeviceDriver::StartDIBits(CFX\_DIBSource const\*, int, unsigned int, CFX\_Matrix const\*, unsigned int, void\*&, int) core/fxge/agg/fx\_agg\_driver.cpp:1706:14  

#7 0x25f5113 in CXFA\_ImageRenderer::StartDIBSource() xfa/fxfa/app/xfa\_ffwidget.cpp:626:18  

#8 0x25f7986 in Start xfa/fxfa/app/xfa\_ffwidget.cpp:622:10  

#9 0x25f7986 in XFA\_DrawImage(CFX\_Graphics\*, CFX\_RTemplate<float> const&, CFX\_Matrix\*, CFX\_DIBitmap\*, int, int, int, int, int) xfa/fxfa/app/xfa\_ffwidget.cpp:899  

#10 0x27b1301 in CXFA\_FFImage::RenderWidget(CFX\_Graphics\*, CFX\_Matrix\*, unsigned int) xfa/fxfa/app/xfa\_ffimage.cpp:63:5  

#11 0x2614dd2 in CXFA\_RenderContext::DoRender(IFX\_Pause\*) xfa/fxfa/app/xfa\_rendercontext.cpp:60:16  

#12 0x1c4b41d in CPDFSDK\_PageView::PageView\_OnDraw(CFX\_RenderDevice\*, CFX\_Matrix\*, CPDF\_RenderOptions\*, FX\_RECT const&) fpdfsdk/cpdfsdk\_pageview.cpp:112:21  

#13 0x1c343ec in FFLCommon fpdfsdk/fpdfformfill.cpp:132:16  

#14 0x1c343ec in FPDF\_FFLDraw fpdfsdk/fpdfformfill.cpp:407  

#15 0x4f5da5 in RenderPage(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, void\*, void\*&, FPDF\_FORMFILLINFO\_PDFiumTest&, int, Options const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) samples/pdfium\_test.cc:594:5  

#16 0x4f735d in RenderPdf(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, char const\*, unsigned long, Options const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) samples/pdfium\_test.cc:786:9  

#17 0x4f8878 in main samples/pdfium\_test.cc:916:5  

#18 0x7ffff69d382f in \_\_libc\_start\_main /build/glibc-GKVZIf/glibc-2.23/csu/../csu/libc-start.c:291

SUMMARY: AddressSanitizer: heap-buffer-overflow core/fxge/dib/fx\_dib\_engine.cpp:245:36 in CWeightTable::Calc(int, int, int, int, int, int, int)  

Shadow bytes around the buggy address:  

0x1000741dc090: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x1000741dc0a0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x1000741dc0b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x1000741dc0c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x1000741dc0d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x1000741dc0e0:[04]fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x1000741dc0f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x1000741dc100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x1000741dc110: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x1000741dc120: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x1000741dc130: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Heap right redzone: fb  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack partial redzone: f4  

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

==21787==ABORTING

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### st...@gmail.com (2016-10-08)

I've uploaded a patch for this issue at https://codereview.chromium.org/2404453003

BTW, although the heap buffer overflow issue was triggered under XFA, but the code was shared in non XFA mode too. In other words, pdfium may be vulnerable even if XFA was disabled.

### ts...@chromium.org (2016-10-10)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### ds...@chromium.org (2016-10-11)

Passing off to thestig@ who has been reviewing the CL in https://crbug.com/chromium/654183#c1.

### bu...@chromium.org (2016-10-17)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium.git/+/05923132ae08d45fbe957219775a48c55ee57aef

commit 05923132ae08d45fbe957219775a48c55ee57aef
Author: stackexploit <stackexploit@gmail.com>
Date: Mon Oct 17 07:16:23 2016

Strengthen bounds check in CWeightTable::Calc * part II

This CL implemented a better version of CWeightTable::GetPixelWeightSize(), which will calculate the size of array PixelWeight.m_Weights correctly to prevent potential heap buffer overflow conditions.

BUG=chromium:654183
R=ochang@chromium.org, thestig@chromium.org, dsinclair@chromium.org

Review-Url: https://codereview.chromium.org/2404453003

[modify] https://crrev.com/05923132ae08d45fbe957219775a48c55ee57aef/core/fxge/dib/fx_dib_engine.cpp


### th...@chromium.org (2016-10-17)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-10-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/665001ab4f668881d484579557d5e5f1ec22aa18

commit 665001ab4f668881d484579557d5e5f1ec22aa18
Author: pdfium-deps-roller <pdfium-deps-roller@chromium.org>
Date: Mon Oct 17 08:39:34 2016

Roll src/third_party/pdfium/ 4dc112664..05923132a (1 commit).

https://pdfium.googlesource.com/pdfium.git/+log/4dc112664e9d..05923132ae08

$ git log 4dc112664..05923132a --date=short --no-merges --format='%ad %ae %s'
2016-10-17 stackexploit Strengthen bounds check in CWeightTable::Calc * part II

BUG=654183

TBR=dsinclair@chromium.org

Review-Url: https://codereview.chromium.org/2424743002
Cr-Commit-Position: refs/heads/master@{#425636}

[modify] https://crrev.com/665001ab4f668881d484579557d5e5f1ec22aa18/DEPS


### sh...@chromium.org (2016-10-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-21)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-10-21)

[Automated comment] DEPS changes referenced in bugdroid comments, needs manual review.

### go...@chromium.org (2016-10-23)

+awhalley@ for M55 merge review

### go...@chromium.org (2016-10-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-24)

Nice one, $3,500 for this report!

### aw...@chromium.org (2016-10-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-24)

Looks good for M55.

### go...@chromium.org (2016-10-24)

Approving merge to M55 branch 2883 based on https://crbug.com/chromium/654183#c16. Please merge ASAP. Thank you.

### th...@chromium.org (2016-10-24)

Will merge.

### bu...@chromium.org (2016-10-24)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/chrome/tools/buildspec/+/e84013dc2611fe399d435debdd36c6da9aab3664

commit e84013dc2611fe399d435debdd36c6da9aab3664
Author: Lei Zhang <thestig@google.com>
Date: Mon Oct 24 20:54:36 2016


### go...@chromium.org (2016-10-24)

Seems like M55 merge is done per https://crbug.com/chromium/654183#c19.

Is anything pending for M55? If not, please remove "Merge-Approved-55" label and apply "merge-merged-2883" label. Thank you.

### th...@chromium.org (2016-10-24)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-10-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-29)

[Empty comment from Monorail migration]

### st...@gmail.com (2016-11-29)

Please credit to Ke Liu of Tencent's Xuanwu LAB for this issue, thanks.

### aw...@chromium.org (2017-01-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@gmail.com (2017-12-12)

Sorry,
but why such issue was rewarded ? (it’s just a question)

Since the xfa feature isn’t enabled with google chrome and thus that Google chrome can’t open xfa pdf or PDF1.7?

### st...@gmail.com (2017-12-14)

For https://crbug.com/chromium/654183#c27, please read https://crbug.com/chromium/654183#c1, hope it helps.

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/654183?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085637)*
