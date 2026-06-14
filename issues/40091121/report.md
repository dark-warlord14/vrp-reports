# Security: PDFium heap-buffer-overflow WRITE  in CPDF_ExpIntFunc::v_Call

| Field | Value |
|-------|-------|
| **Issue ID** | [40091121](https://issues.chromium.org/issues/40091121) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | zh...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2018-04-17 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

heap-buffer-overflow WRITE of size 4 in CPDF\_ExpIntFunc::v\_Call(float\*, float\*) const core/fpdfapi/page/cpdf\_expintfunc.cpp:55:39

=================================================================  

==24517==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60700000d884 at pc 0x000000e81b65 bp 0x7ffeee6c0380 sp 0x7ffeee6c0378  

WRITE of size 4 at 0x60700000d884 thread T0  

#0 0xe81b64 in CPDF\_ExpIntFunc::v\_Call(float\*, float\*) const core/fpdfapi/page/cpdf\_expintfunc.cpp:55:39  

#1 0xe7fa1e in CPDF\_Function::Call(float\*, unsigned int, float\*, int\*) const core/fpdfapi/page/cpdf\_function.cpp:116:3  

#2 0x1195056 in (anonymous namespace)::DrawRadialShading(fxcrt::RetainPtr<CFX\_DIBitmap> const&, CFX\_Matrix\*, CPDF\_Dictionary\*, std::\_\_1::vector<std::\_\_1::unique\_ptr<CPDF\_Function, std::\_\_1::default\_delete<CPDF\_Function> >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<CPDF\_Function, std::\_\_1::default\_delete<CPDF\_Function> > > > const&, CPDF\_ColorSpace\*, int) core/fpdfapi/render/cpdf\_renderstatus.cpp:233:19  

#3 0x1190807 in CPDF\_RenderStatus::DrawShading(CPDF\_ShadingPattern const\*, CFX\_Matrix\*, FX\_RECT&, int, bool) core/fpdfapi/render/cpdf\_renderstatus.cpp:2133:7  

#4 0x119aaa8 in CPDF\_RenderStatus::DrawShadingPattern(CPDF\_ShadingPattern\*, CPDF\_PageObject const\*, CFX\_Matrix const\*, bool) core/fpdfapi/render/cpdf\_renderstatus.cpp:2197:3  

#5 0x119fc46 in CPDF\_RenderStatus::DrawPathWithPattern(CPDF\_PathObject\*, CFX\_Matrix const\*, CPDF\_Color const\*, bool) core/fpdfapi/render/cpdf\_renderstatus.cpp:2421:5  

#6 0x117f910 in CPDF\_RenderStatus::ProcessPathPattern(CPDF\_PathObject\*, CFX\_Matrix const\*, int\*, bool\*) core/fpdfapi/render/cpdf\_renderstatus.cpp:2434:7  

#7 0x117d806 in CPDF\_RenderStatus::ProcessPath(CPDF\_PathObject\*, CFX\_Matrix const\*) core/fpdfapi/render/cpdf\_renderstatus.cpp:1311:3  

#8 0x117a4c0 in CPDF\_RenderStatus::ProcessObjectNoClip(CPDF\_PageObject\*, CFX\_Matrix const\*) core/fpdfapi/render/cpdf\_renderstatus.cpp:1198:14  

#9 0x117acc9 in CPDF\_RenderStatus::ContinueSingleObject(CPDF\_PageObject\*, CFX\_Matrix const\*, PauseIndicatorIface\*) core/fpdfapi/render/cpdf\_renderstatus.cpp:1151:5  

#10 0x116bced in CPDF\_ProgressiveRenderer::Continue(PauseIndicatorIface\*) core/fpdfapi/render/cpdf\_progressiverenderer.cpp:93:30  

#11 0x1169d43 in CPDF\_ProgressiveRenderer::Start(PauseIndicatorIface\*) core/fpdfapi/render/cpdf\_progressiverenderer.cpp:44:3  

#12 0xbe8fbd in (anonymous namespace)::RenderPageImpl(CPDF\_PageRenderContext\*, CPDF\_Page\*, CFX\_Matrix const&, FX\_RECT const&, int, bool, IPDFSDK\_PauseAdapter\*) fpdfsdk/fpdf\_view.cpp:124:26  

#13 0xbe5f61 in FPDF\_RenderPage\_Retail(CPDF\_PageRenderContext\*, void\*, int, int, int, int, int, int, bool, IPDFSDK\_PauseAdapter\*) fpdfsdk/fpdf\_view.cpp:902:3  

#14 0xbdbdf4 in FPDF\_RenderPageBitmap\_Start fpdfsdk/fpdf\_progressive.cpp:60:3  

#15 0x8f8b43 in (anonymous namespace)::RenderPage(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, void\*, void\*, (anonymous namespace)::FPDF\_FORMFILLINFO\_PDFiumTest\*, int, (anonymous namespace)::Options const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) samples/pdfium\_test.cc:543:16  

#16 0x8f301f in (anonymous namespace)::RenderPdf(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, char const\*, unsigned long, (anonymous namespace)::Options const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) samples/pdfium\_test.cc:741:9  

#17 0x8e6508 in main samples/pdfium\_test.cc:902:5  

#18 0x7f8ebe35682f in \_\_libc\_start\_main /build/glibc-Cl5G7W/glibc-2.23/csu/../csu/libc-start.c:291

0x60700000d884 is located 0 bytes to the right of 68-byte region [0x60700000d840,0x60700000d884)  

allocated by thread T0 here:  

#0 0x8b3373 in \_\_interceptor\_malloc /b/build/slave/linux\_upload\_clang/build/src/third\_party/llvm/compiler-rt/lib/asan/asan\_malloc\_linux.cc:88:3  

#1 0xaf200f in pdfium::base::PartitionAllocGenericFlags(pdfium::base::PartitionRootGeneric\*, int, unsigned long, char const\*) third\_party/base/allocator/partition\_allocator/partition\_alloc.h:790:18  

#2 0xaf1e14 in FX\_SafeAlloc(unsigned long, unsigned long) core/fxcrt/fx\_memory.h:46:18  

#3 0xaf121c in FX\_AllocOrDie(unsigned long, unsigned long) core/fxcrt/fx\_memory.h:67:18  

#4 0xdd4ab5 in CFX\_FixedBufGrow<float, 16>::CFX\_FixedBufGrow(int) core/fxcrt/cfx\_fixedbufgrow.h:19:25  

#5 0x119496a in (anonymous namespace)::DrawRadialShading(fxcrt::RetainPtr<CFX\_DIBitmap> const&, CFX\_Matrix\*, CPDF\_Dictionary\*, std::\_\_1::vector<std::\_\_1::unique\_ptr<CPDF\_Function, std::\_\_1::default\_delete<CPDF\_Function> >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<CPDF\_Function, std::\_\_1::default\_delete<CPDF\_Function> > > > const&, CPDF\_ColorSpace\*, int) core/fpdfapi/render/cpdf\_renderstatus.cpp:223:31  

#6 0x1190807 in CPDF\_RenderStatus::DrawShading(CPDF\_ShadingPattern const\*, CFX\_Matrix\*, FX\_RECT&, int, bool) core/fpdfapi/render/cpdf\_renderstatus.cpp:2133:7  

#7 0x119aaa8 in CPDF\_RenderStatus::DrawShadingPattern(CPDF\_ShadingPattern\*, CPDF\_PageObject const\*, CFX\_Matrix const\*, bool) core/fpdfapi/render/cpdf\_renderstatus.cpp:2197:3  

#8 0x119fc46 in CPDF\_RenderStatus::DrawPathWithPattern(CPDF\_PathObject\*, CFX\_Matrix const\*, CPDF\_Color const\*, bool) core/fpdfapi/render/cpdf\_renderstatus.cpp:2421:5  

#9 0x117f910 in CPDF\_RenderStatus::ProcessPathPattern(CPDF\_PathObject\*, CFX\_Matrix const\*, int\*, bool\*) core/fpdfapi/render/cpdf\_renderstatus.cpp:2434:7  

#10 0x117d806 in CPDF\_RenderStatus::ProcessPath(CPDF\_PathObject\*, CFX\_Matrix const\*) core/fpdfapi/render/cpdf\_renderstatus.cpp:1311:3  

#11 0x117a4c0 in CPDF\_RenderStatus::ProcessObjectNoClip(CPDF\_PageObject\*, CFX\_Matrix const\*) core/fpdfapi/render/cpdf\_renderstatus.cpp:1198:14  

#12 0x117acc9 in CPDF\_RenderStatus::ContinueSingleObject(CPDF\_PageObject\*, CFX\_Matrix const\*, PauseIndicatorIface\*) core/fpdfapi/render/cpdf\_renderstatus.cpp:1151:5  

#13 0x116bced in CPDF\_ProgressiveRenderer::Continue(PauseIndicatorIface\*) core/fpdfapi/render/cpdf\_progressiverenderer.cpp:93:30  

#14 0x1169d43 in CPDF\_ProgressiveRenderer::Start(PauseIndicatorIface\*) core/fpdfapi/render/cpdf\_progressiverenderer.cpp:44:3  

#15 0xbe8fbd in (anonymous namespace)::RenderPageImpl(CPDF\_PageRenderContext\*, CPDF\_Page\*, CFX\_Matrix const&, FX\_RECT const&, int, bool, IPDFSDK\_PauseAdapter\*) fpdfsdk/fpdf\_view.cpp:124:26  

#16 0xbe5f61 in FPDF\_RenderPage\_Retail(CPDF\_PageRenderContext\*, void\*, int, int, int, int, int, int, bool, IPDFSDK\_PauseAdapter\*) fpdfsdk/fpdf\_view.cpp:902:3  

#17 0xbdbdf4 in FPDF\_RenderPageBitmap\_Start fpdfsdk/fpdf\_progressive.cpp:60:3  

#18 0x8f8b43 in (anonymous namespace)::RenderPage(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, void\*, void\*, (anonymous namespace)::FPDF\_FORMFILLINFO\_PDFiumTest\*, int, (anonymous namespace)::Options const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) samples/pdfium\_test.cc:543:16  

#19 0x8f301f in (anonymous namespace)::RenderPdf(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, char const\*, unsigned long, (anonymous namespace)::Options const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) samples/pdfium\_test.cc:741:9  

#20 0x8e6508 in main samples/pdfium\_test.cc:902:5  

#21 0x7f8ebe35682f in \_\_libc\_start\_main /build/glibc-Cl5G7W/glibc-2.23/csu/../csu/libc-start.c:291

SUMMARY: AddressSanitizer: heap-buffer-overflow core/fpdfapi/page/cpdf\_expintfunc.cpp:55:39 in CPDF\_ExpIntFunc::v\_Call(float\*, float\*) const  

Shadow bytes around the buggy address:  

0x0c0e7fff9ac0: fa fa fd fd fd fd fd fd fd fd fd fd fa fa fa fa  

0x0c0e7fff9ad0: 00 00 00 00 00 00 00 00 00 fa fa fa fa fa fd fd  

0x0c0e7fff9ae0: fd fd fd fd fd fd fd fa fa fa fa fa 00 00 00 00  

0x0c0e7fff9af0: 00 00 00 00 00 fa fa fa fa fa 00 00 00 00 00 00  

0x0c0e7fff9b00: 00 00 00 fa fa fa fa fa 00 00 00 00 00 00 00 00  

=>0x0c0e7fff9b10:[04]fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0e7fff9b20: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0e7fff9b30: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0e7fff9b40: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0e7fff9b50: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0e7fff9b60: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

==24517==ABORTING

**VERSION** ：  

asan-linux-beta-66.0.3359.106

**REPRODUCTION CASE** ：  

testcase-002921\_OOB\_write

## Attachments

- [poc_oobwrite.mov](attachments/poc_oobwrite.mov) (video/quicktime, 9.0 MB)
- [testcase-002921_OOB_write](attachments/testcase-002921_OOB_write) (text/plain, 906.1 KB)

## Timeline

### ts...@chromium.org (2018-04-17)

[Empty comment from Monorail migration]

### ts...@chromium.org (2018-04-17)

Lei, could you take a look?  You were just poking around in here the other day ...

### sh...@chromium.org (2018-04-18)

[Empty comment from Monorail migration]

### th...@chromium.org (2018-04-18)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### cl...@chromium.org (2018-04-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6451397336498176.

### th...@chromium.org (2018-04-18)

https://pdfium-review.googlesource.com/c/pdfium/+/30992

### bu...@chromium.org (2018-04-18)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/e06880f8eb984a48921f0560bd7ab4e055da432d

commit e06880f8eb984a48921f0560bd7ab4e055da432d
Author: Lei Zhang <thestig@chromium.org>
Date: Wed Apr 18 22:59:32 2018

Fix integer overflow in shading drawing code.

BUG=chromium:833721

Change-Id: I3ca878760c12144ef27a71dcbbfd7c18d12a5f3b
Reviewed-on: https://pdfium-review.googlesource.com/30992
Commit-Queue: Lei Zhang <thestig@chromium.org>
Reviewed-by: Tom Sepez <tsepez@chromium.org>

[modify] https://crrev.com/e06880f8eb984a48921f0560bd7ab4e055da432d/core/fpdfapi/render/cpdf_renderstatus.cpp


### bu...@chromium.org (2018-04-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1b7273d7a120c7e558287ce6878e8d96d40e3de7

commit 1b7273d7a120c7e558287ce6878e8d96d40e3de7
Author: pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Date: Thu Apr 19 01:25:21 2018

Roll src/third_party/pdfium/ fbecb9a51..e06880f8e (2 commits)

https://pdfium.googlesource.com/pdfium.git/+log/fbecb9a5150d..e06880f8eb98

$ git log fbecb9a51..e06880f8e --date=short --no-merges --format='%ad %ae %s'
2018-04-18 thestig Fix integer overflow in shading drawing code.
2018-04-18 tsepez Always build JS Runtime stubs even if V8 present.

Created with:
  roll-dep src/third_party/pdfium
BUG=chromium:833721


The AutoRoll server is located here: https://pdfium-roll.skia.org

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.


TBR=dsinclair@chromium.org

Change-Id: I5f24866aeca19c08d4e8f0459180c5b617263dc6
Reviewed-on: https://chromium-review.googlesource.com/1018119
Reviewed-by: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Commit-Queue: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#551912}
[modify] https://crrev.com/1b7273d7a120c7e558287ce6878e8d96d40e3de7/DEPS


### th...@chromium.org (2018-04-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-19)

[Empty comment from Monorail migration]

### th...@chromium.org (2018-04-20)

awhalley: The fix landed in 68.0.3401.0. Should we consider M66 and M67 merges?

### aw...@google.com (2018-04-20)

Thanks thesig@ - let's get this in M67 for now and look at 66 once it's been out in dev/beta for a bit

### sh...@chromium.org (2018-04-20)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-04-20)

Approving merge to M67 branch 3396 based on https://crbug.com/chromium/833721#c12. Please merge ASAP. Thank you.

### bu...@chromium.org (2018-04-20)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/a1666b8e536e90a4cc21787fe12c95e052454b6d

commit a1666b8e536e90a4cc21787fe12c95e052454b6d
Author: Lei Zhang <thestig@chromium.org>
Date: Fri Apr 20 22:42:54 2018

M67: Fix integer overflow in shading drawing code.

BUG=chromium:833721
TBR=tsepez@chromium.org

Change-Id: I3ca878760c12144ef27a71dcbbfd7c18d12a5f3b
Reviewed-on: https://pdfium-review.googlesource.com/30992
Commit-Queue: Lei Zhang <thestig@chromium.org>
Reviewed-by: Tom Sepez <tsepez@chromium.org>
(cherry picked from commit e06880f8eb984a48921f0560bd7ab4e055da432d)
Reviewed-on: https://pdfium-review.googlesource.com/31131
Reviewed-by: Lei Zhang <thestig@chromium.org>

[modify] https://crrev.com/a1666b8e536e90a4cc21787fe12c95e052454b6d/core/fpdfapi/render/cpdf_renderstatus.cpp


### aw...@google.com (2018-04-23)

[Empty comment from Monorail migration]

### zh...@gmail.com (2018-04-25)

[Comment Deleted]

### zh...@gmail.com (2018-04-25)

[Comment Deleted]

### zh...@gmail.com (2018-04-25)

[Comment Deleted]

### aw...@chromium.org (2018-04-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-04-27)

Very nicely done! The Chrome VRP panel decided to award $5,000 for this report.  Cheers!

### aw...@google.com (2018-04-27)

A member of our finance team will be in touch to arrange payment.  Also, how would you like to be credited in Chrome Release notes?

### zh...@gmail.com (2018-04-27)

[Comment Deleted]

### aw...@chromium.org (2018-04-27)

[Empty comment from Monorail migration]

### aw...@google.com (2018-05-08)

abdulsyed@ - good for 66

### ab...@chromium.org (2018-05-08)

How safe is this merge overall?

### th...@chromium.org (2018-05-08)

Should be fine. It mostly sanity checks a series of additions to make sure they don't overflow.

### ab...@chromium.org (2018-05-08)

Ok great, and should be a clean merge to M66 as well, correct? Approving merge to M66 branch:3359.  

### th...@chromium.org (2018-05-08)

Clean merge to M66.

### bu...@chromium.org (2018-05-08)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/1e37088495505a646d7725a0991252ca45e90322

commit 1e37088495505a646d7725a0991252ca45e90322
Author: Lei Zhang <thestig@chromium.org>
Date: Tue May 08 22:27:21 2018

M66: Fix integer overflow in shading drawing code.

BUG=chromium:833721
TBR=tsepez@chromium.org

Change-Id: I3ca878760c12144ef27a71dcbbfd7c18d12a5f3b
Reviewed-on: https://pdfium-review.googlesource.com/30992
Commit-Queue: Lei Zhang <thestig@chromium.org>
Reviewed-by: Tom Sepez <tsepez@chromium.org>
(cherry picked from commit e06880f8eb984a48921f0560bd7ab4e055da432d)
Reviewed-on: https://pdfium-review.googlesource.com/32195
Reviewed-by: Lei Zhang <thestig@chromium.org>

[modify] https://crrev.com/1e37088495505a646d7725a0991252ca45e90322/core/fpdfapi/render/cpdf_renderstatus.cpp


### aw...@google.com (2018-05-09)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-09)

[Empty comment from Monorail migration]

### zh...@gmail.com (2018-05-18)

[Comment Deleted]

### aw...@google.com (2018-05-18)

Hi zhouat2017@ - will follow up over email.

### sh...@chromium.org (2018-07-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### ad...@chromium.org (2021-10-19)

Original attachments undeleted because they're considered to be a key part of the bug report.

### is...@google.com (2021-10-19)

This issue was migrated from crbug.com/chromium/833721?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091121)*
