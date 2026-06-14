# Security: PDFium heap-use-after-free in CPDFSDK_PageView::ExitWidget (XFA)

| Field | Value |
|-------|-------|
| **Issue ID** | [40050509](https://issues.chromium.org/issues/40050509) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cn...@chromium.org |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-10-23 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**

fpdfsdk/cpdfsdk\_pageview.cpp

bool CPDFSDK\_PageView::OnMouseMove(const CFX\_PointF& point, int nFlag) {  

CPDFSDK\_AnnotHandlerMgr\* pAnnotHandlerMgr =  

m\_pFormFillEnv->GetAnnotHandlerMgr();  

ObservedPtr<CPDFSDK\_Annot> pFXAnnot(GetFXAnnotAtPoint(point));

if (m\_bOnWidget && m\_pCaptureWidget != pFXAnnot)  

ExitWidget(pAnnotHandlerMgr, true, nFlag);

if (pFXAnnot) {  

if (!m\_bOnWidget) {  

EnterWidget(pAnnotHandlerMgr, &pFXAnnot, nFlag); // In EnterWidget, the PageView is destroyed by calling CPDFSDK\_FormFillEnvironment::RemovePageView

```
  // Annot_OnMouseEnter may have invalidated pFXAnnot.  
  if (!pFXAnnot) {  
    ExitWidget(pAnnotHandlerMgr, false, nFlag); // However, ExitWidget then tries to write to an instance variable, causing the heap-use-after-free.  
    return true;  
  }  
}  

pAnnotHandlerMgr->Annot_OnMouseMove(this, &pFXAnnot, nFlag, point);  
return true;  

```

}

return false;  

}

**VERSION**  

Built from 39adbb0284ef3c943db99559bdf419e9d20b9bf5

**REPRODUCTION CASE**  

Run pdfium\_test with --send-events and XFA enabled with poc.pdf and poc.evt.

ASAN output:

=================================================================  

==28106==ERROR: AddressSanitizer: heap-use-after-free on address 0x60b000006c90 at pc 0x5637d1b80963 bp 0x7ffc7cad7ae0 sp 0x7ffc7cad7ad8  

WRITE of size 1 at 0x60b000006c90 thread T0  

SCARINESS: 41 (1-byte-write-heap-use-after-free)  

#0 0x5637d1b80962 in CPDFSDK\_PageView::ExitWidget(CPDFSDK\_AnnotHandlerMgr\*, bool, unsigned int) third\_party/pdfium/fpdfsdk/cpdfsdk\_pageview.cpp:405:15  

#1 0x5637d1b8070e in CPDFSDK\_PageView::OnMouseMove(CFX\_PTemplate<float> const&, int) third\_party/pdfium/fpdfsdk/cpdfsdk\_pageview.cpp:382:9  

#2 0x5637d1bc3b12 in FORM\_OnMouseMove third\_party/pdfium/fpdfsdk/fpdf\_formfill.cpp:360:21  

#3 0x5637d1ac2c5e in SendPageEvents(fpdf\_form\_handle\_t\_\_\*, fpdf\_page\_t\_\_\*, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) third\_party/pdfium/samples/pdfium\_test\_event\_helper.cc:142:7  

#4 0x5637d1ab7394 in (anonymous namespace)::RenderPage(std::\_\_1::basic\_string<char, std::**1::char\_traits<char>, std::1::allocator<char> > const&, fpdf\_document\_t\*, fpdf\_form\_handle\_t**\*, (anonymous namespace)::FPDF\_FORMFILLINFO\_PDFiumTest\*, int, (anonymous namespace)::Options const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) third\_party/pdfium/samples/pdfium\_test.cc:619:5  

#5 0x5637d1aa9da6 in (anonymous namespace)::RenderPdf(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, char const\*, unsigned long, (anonymous namespace)::Options const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) third\_party/pdfium/samples/pdfium\_test.cc:880:9  

#6 0x5637d1aa624e in main third\_party/pdfium/samples/pdfium\_test.cc:1080:5  

#7 0x7f6b42f55504 in \_\_libc\_start\_main (/lib64/libc.so.6+0x22504)

0x60b000006c90 is located 96 bytes inside of 104-byte region [0x60b000006c30,0x60b000006c98)  

freed by thread T0 here:  

#0 0x5637d1aa2930 in operator delete(void\*) /data/chromium/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:160  

#1 0x5637d1b5e4ff in std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<IPDF\_Page\*, std::\_\_1::unique\_ptr<CPDFSDK\_PageView, std::\_\_1::default\_delete<CPDFSDK\_PageView> > >, std::\_\_1::\_\_map\_value\_compare<IPDF\_Page\*, std::\_\_1::\_\_value\_type<IPDF\_Page\*, std::\_\_1::unique\_ptr<CPDFSDK\_PageView, std::\_\_1::default\_delete<CPDFSDK\_PageView> > >, std::\_\_1::less<IPDF\_Page\*>, true>, std::\_\_1::allocator<std::\_\_1::\_\_value\_type<IPDF\_Page\*, std::\_\_1::unique\_ptr<CPDFSDK\_PageView, std::\_\_1::default\_delete<CPDFSDK\_PageView> > > > >::erase(std::\_\_1::\_\_tree\_const\_iterator<std::\_\_1::\_\_value\_type<IPDF\_Page\*, std::\_\_1::unique\_ptr<CPDFSDK\_PageView, std::\_\_1::default\_delete<CPDFSDK\_PageView> > >, std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<IPDF\_Page\*, std::\_\_1::unique\_ptr<CPDFSDK\_PageView, std::\_\_1::default\_delete<CPDFSDK\_PageView> > >, void\*>\*, long>) buildtools/third\_party/libc++/trunk/include/\_\_tree:2561:5  

#2 0x5637d1b55776 in std::\_\_1::map<IPDF\_Page\*, std::\_\_1::unique\_ptr<CPDFSDK\_PageView, std::\_\_1::default\_delete<CPDFSDK\_PageView> >, std::\_\_1::less<IPDF\_Page\*>, std::\_\_1::allocator<std::\_\_1::pair<IPDF\_Page\* const, std::\_\_1::unique\_ptr<CPDFSDK\_PageView, std::\_\_1::default\_delete<CPDFSDK\_PageView> > > > >::erase(std::\_\_1::\_\_map\_iterator<std::\_\_1::\_\_tree\_iterator<std::\_\_1::\_\_value\_type<IPDF\_Page\*, std::\_\_1::unique\_ptr<CPDFSDK\_PageView, std::\_\_1::default\_delete<CPDFSDK\_PageView> > >, std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<IPDF\_Page\*, std::**1::unique\_ptr<CPDFSDK\_PageView, std::1::default\_delete<CPDFSDK\_PageView> > >, void\*>\*, long> >) buildtools/third\_party/libc++/trunk/include/map:1301:56  

#3 0x5637d1b55440 in CPDFSDK\_FormFillEnvironment::RemovePageView(IPDF\_Page\*) third\_party/pdfium/fpdfsdk/cpdfsdk\_formfillenvironment.cpp:646:13  

#4 0x5637d4ad32d6 in CPDFXFA\_DocEnvironment::PageViewEvent(CXFA\_FFPageView\*, unsigned int) third\_party/pdfium/fpdfsdk/fpdfxfa/cpdfxfa\_docenvironment.cpp:297:35  

#5 0x5637d45b52e8 in CXFA\_FFDocView::RunLayout() third\_party/pdfium/xfa/fxfa/cxfa\_ffdocview.cpp:462:34  

#6 0x5637d45b5e6b in CXFA\_FFDocView::UpdateDocView() third\_party/pdfium/xfa/fxfa/cxfa\_ffdocview.cpp:189:7  

#7 0x5637d463e7d3 in CXFA\_FFWidgetHandler::OnMouseEnter(CXFA\_FFWidget\*) third\_party/pdfium/xfa/fxfa/cxfa\_ffwidgethandler.cpp:34:15  

#8 0x5637d1b805e5 in CPDFSDK\_PageView::OnMouseMove(CFX\_PTemplate<float> const&, int) third\_party/pdfium/fpdfsdk/cpdfsdk\_pageview.cpp:378:7  

#9 0x5637d1bc3b12 in FORM\_OnMouseMove third\_party/pdfium/fpdfsdk/fpdf\_formfill.cpp:360:21  

#10 0x5637d1ac2c5e in SendPageEvents(fpdf\_form\_handle\_t\*, fpdf\_page\_t**\*, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) third\_party/pdfium/samples/pdfium\_test\_event\_helper.cc:142:7  

#11 0x5637d1ab7394 in (anonymous namespace)::RenderPage(std::\_\_1::basic\_string<char, std::**1::char\_traits<char>, std::1::allocator<char> > const&, fpdf\_document\_t\*, fpdf\_form\_handle\_t**\*, (anonymous namespace)::FPDF\_FORMFILLINFO\_PDFiumTest\*, int, (anonymous namespace)::Options const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) third\_party/pdfium/samples/pdfium\_test.cc:619:5  

#12 0x5637d1aa9da6 in (anonymous namespace)::RenderPdf(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, char const\*, unsigned long, (anonymous namespace)::Options const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) third\_party/pdfium/samples/pdfium\_test.cc:880:9  

#13 0x5637d1aa624e in main third\_party/pdfium/samples/pdfium\_test.cc:1080:5  

#14 0x7f6b42f55504 in \_\_libc\_start\_main (/lib64/libc.so.6+0x22504)

previously allocated by thread T0 here:  

#0 0x5637d1aa1f38 in operator new(unsigned long) /data/chromium/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:99  

#1 0x5637d1b53880 in pdfium::internal::MakeUniqueResult<CPDFSDK\_PageView>::Scalar pdfium::MakeUnique<CPDFSDK\_PageView, CPDFSDK\_FormFillEnvironment\*, IPDF\_Page\*&>(CPDFSDK\_FormFillEnvironment\*&&, IPDF\_Page\*&) third\_party/pdfium/third\_party/base/ptr\_util.h:56:29  

#2 0x5637d1b46c88 in CPDFSDK\_FormFillEnvironment::GetPageView(IPDF\_Page\*, bool) third\_party/pdfium/fpdfsdk/cpdfsdk\_formfillenvironment.cpp:572:15  

#3 0x5637d1bc53f1 in FORM\_OnAfterLoadPage third\_party/pdfium/fpdfsdk/fpdf\_formfill.cpp:619:37  

#4 0x5637d1ab6f2a in (anonymous namespace)::GetPageForIndex(*FPDF\_FORMFILLINFO\*, fpdf\_document\_t*\_\*, int) third\_party/pdfium/samples/pdfium\_test.cc:596:3  

#5 0x5637d1ab7343 in (anonymous namespace)::RenderPage(std::\_\_1::basic\_string<char, std::**1::char\_traits<char>, std::1::allocator<char> > const&, fpdf\_document\_t\*, fpdf\_form\_handle\_t**\*, (anonymous namespace)::FPDF\_FORMFILLINFO\_PDFiumTest\*, int, (anonymous namespace)::Options const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) third\_party/pdfium/samples/pdfium\_test.cc:615:20  

#6 0x5637d1aa9da6 in (anonymous namespace)::RenderPdf(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, char const\*, unsigned long, (anonymous namespace)::Options const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) third\_party/pdfium/samples/pdfium\_test.cc:880:9  

#7 0x5637d1aa624e in main third\_party/pdfium/samples/pdfium\_test.cc:1080:5  

#8 0x7f6b42f55504 in \_\_libc\_start\_main (/lib64/libc.so.6+0x22504)

SUMMARY: AddressSanitizer: heap-use-after-free third\_party/pdfium/fpdfsdk/cpdfsdk\_pageview.cpp:405:15 in CPDFSDK\_PageView::ExitWidget(CPDFSDK\_AnnotHandlerMgr\*, bool, unsigned int)  

Shadow bytes around the buggy address:  

0x0c167fff8d40: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c167fff8d50: 00 fa fa fa fa fa fa fa fa fa fc fc fc fc fc fc  

0x0c167fff8d60: fc fc fc fc fc fc fc fc fa fa fa fa fa fa fa fa  

0x0c167fff8d70: fc fc fc fc fc fc fc fc fc fc fc fc fc fc fa fa  

0x0c167fff8d80: fa fa fa fa fa fa fd fd fd fd fd fd fd fd fd fd  

=>0x0c167fff8d90: fd fd[fd]fa fa fa fa fa fa fa fa fa fd fd fd fd  

0x0c167fff8da0: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa  

0x0c167fff8db0: fa fa fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

0x0c167fff8dc0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c167fff8dd0: fd fd fd fd fd fa fa fa fa fa fa fa fa fa fc fc  

0x0c167fff8de0: fc fc fc fc fc fc fc fc fc fc fc fc fa fa fa fa  

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

==28106==ABORTING

## Attachments

- [poc.evt](attachments/poc.evt) (application/octet-stream, 36 B)
- [poc.pdf](attachments/poc.pdf) (application/pdf, 1.4 KB)

## Timeline

### cn...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-10-24)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6476182134325248.

### cl...@chromium.org (2019-10-24)

Testcase 6476182134325248 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6476182134325248.

### jd...@chromium.org (2019-10-24)

tsepez: can you PTAL? Adding thestig@ for more visibility (and because tsepez@ is listed as away from crbug for >30 days).

The CF attempt was wishful thinking on my part (XFA+ASAN+pdfium interactions isn't something CF can do right now), but I can reproduce this at ToT myself.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-11-01)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/c3a91730e33ec37e08413edbb6628d789799ba56

commit c3a91730e33ec37e08413edbb6628d789799ba56
Author: Tom Sepez <tsepez@chromium.org>
Date: Fri Nov 01 21:53:00 2019

Make CPDFSDK_Pageview observable across mouse move callbacks

Bug: chromium:1017494
Change-Id: I8a7590be50d11f22e854531903565b2528539005
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/61871
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>

[add] https://pdfium.googlesource.com/pdfium/+/c3a91730e33ec37e08413edbb6628d789799ba56/testing/resources/javascript/xfa_specific/bug_1017494.in
[add] https://pdfium.googlesource.com/pdfium/+/c3a91730e33ec37e08413edbb6628d789799ba56/testing/resources/javascript/xfa_specific/bug_1017494.evt
[modify] https://pdfium.googlesource.com/pdfium/+/c3a91730e33ec37e08413edbb6628d789799ba56/fpdfsdk/cpdfsdk_pageview.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/c3a91730e33ec37e08413edbb6628d789799ba56/core/fpdfapi/page/cpdf_page.h


### ts...@chromium.org (2019-11-01)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-11-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/93d33968d031388f0c9cf2c1c7bec8f8445bb935

commit 93d33968d031388f0c9cf2c1c7bec8f8445bb935
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Nov 01 23:39:33 2019

Roll src/third_party/pdfium dd9ef1c0d58f..c3a91730e33e (3 commits)

https://pdfium.googlesource.com/pdfium.git/+log/dd9ef1c0d58f..c3a91730e33e

git log dd9ef1c0d58f..c3a91730e33e --date=short --no-merges --format='%ad %ae %s'
2019-11-01 tsepez@chromium.org Make CPDFSDK_Pageview observable across mouse move callbacks
2019-11-01 dhoss@chromium.org Remove jumbo usage in GN files throughout PDFium
2019-11-01 tsepez@chromium.org Run another embedder test with javascript disabled.

Created with:
  gclient setdep -r src/third_party/pdfium@c3a91730e33e

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

TBR=pdfium-deps-rolls@chromium.org

Bug: chromium:1017494
Change-Id: Ib0f25d57b2868bbec3fc46b5825d6085611dc284
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1896139
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#711932}

[modify] https://crrev.com/93d33968d031388f0c9cf2c1c7bec8f8445bb935/DEPS


### sh...@chromium.org (2019-11-02)

[Empty comment from Monorail migration]

### cn...@chromium.org (2019-11-07)

Is this bug eligible for the VRP? (I ask since even though I have an @chromium.org email, I'm not a Googler.)

### cn...@chromium.org (2019-11-18)

cc-ing natashapabrai@ re: my previous comment

### ts...@chromium.org (2019-11-18)

+awhalley for vrp

### aw...@google.com (2019-11-18)

Yep, it is eligible for VRP consideration. And thanks for flagging, we don't automatically consider bugs submitted by @chromium.org accounts! I've labelled it for consideration and it will be reviewed the the panel in coming weeks.

### na...@google.com (2019-12-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-12-05)

Congrats! The Panel decided to reward $7,500 for this high quality report!

### na...@google.com (2019-12-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-02-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2020-02-24)

FWIW, this may have been reported earlier as https://crbug.com/chromium/976767, but we lost track.

### is...@google.com (2020-02-24)

This issue was migrated from crbug.com/chromium/1017494?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050509)*
