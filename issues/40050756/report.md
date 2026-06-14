# pdfium (XFA): invalid-vptr / uaf in CPDFSDK_PageView::ExitWidget

| Field | Value |
|-------|-------|
| **Issue ID** | [40050756](https://issues.chromium.org/issues/40050756) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | pd...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2019-11-21 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.101 Safari/537.36

Steps to reproduce the problem:
(UBSAN)

fpdfsdk/cpdfsdk_pageview.cpp:416:22: runtime error: member call on address 0x564f1e52e440 which does not point to an object of type 'fxcrt::ObservedPtr<CPDFSDK_Annot>'
0x564f1e52e440: note: object has invalid vptr
 00 00 00 00  78 3b 87 3d ec 7f 00 00  78 3b 87 3d ec 7f 00 00  00 00 00 00 00 00 00 00  00 01 00 01
              ^~~~~~~~~~~~~~~~~~~~~~~
              invalid vptr

    #0 0x564f1aa49279 in CPDFSDK_PageView::ExitWidget(CPDFSDK_AnnotHandlerMgr*, bool, unsigned int) fpdfsdk/cpdfsdk_pageview.cpp:416:22
    #1 0x564f1aa48d2a in CPDFSDK_PageView::OnMouseMove(CFX_PTemplate<float> const&, int) fpdfsdk/cpdfsdk_pageview.cpp:378:5
    #2 0x564f1aa773ba in FORM_OnMouseMove fpdfsdk/fpdf_formfill.cpp:360:21
    #3 0x564f1a9d214a in (anonymous namespace)::SendMouseMoveEvent(fpdf_form_handle_t__*, fpdf_page_t__*, std::__1::vector<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::allocator<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > > > const&) samples/pdfium_test_event_helper.cc:107:3
    #4 0x564f1a9d1b85 in SendPageEvents(fpdf_form_handle_t__*, fpdf_page_t__*, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test_event_helper.cc:142:7
    #5 0x564f1a9c94be in (anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__*, fpdf_form_handle_t__*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:669:5
    #6 0x564f1a9c10c6 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:929:9
    #7 0x564f1a9be9b9 in main samples/pdfium_test.cc:1138:5

(ASAN)

AddressSanitizer: heap-use-after-free on address 0x60c0000116e8 at pc 0x55f4b6a9c16a bp 0x7ffe3425b6c0 sp 0x7ffe3425b6b8
READ of size 8 at 0x60c0000116e8 thread T0
SCARINESS: 51 (8-byte-read-heap-use-after-free)

    #0 0x55f4b6a9c169 in fxcrt::ObservedPtr<CPDFSDK_Annot>::Reset(CPDFSDK_Annot*) core/fxcrt/observed_ptr.h:64:9
    #1 0x55f4b6ab2762 in CPDFSDK_PageView::ExitWidget(CPDFSDK_AnnotHandlerMgr*, bool, unsigned int) fpdfsdk/cpdfsdk_pageview.cpp:416:22
    #2 0x55f4b6ab2516 in CPDFSDK_PageView::OnMouseMove(CFX_PTemplate<float> const&, int) fpdfsdk/cpdfsdk_pageview.cpp:378:5
    #3 0x55f4b6ad54db in FORM_OnMouseMove fpdfsdk/fpdf_formfill.cpp:360:21
    #4 0x55f4b6a46924 in (anonymous namespace)::SendMouseMoveEvent(fpdf_form_handle_t__*, fpdf_page_t__*, std::__1::vector<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::allocator<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > > > const&) samples/pdfium_test_event_helper.cc:107:3
    #5 0x55f4b6a46062 in SendPageEvents(fpdf_form_handle_t__*, fpdf_page_t__*, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test_event_helper.cc:142:7
    #6 0x55f4b6a3da2f in (anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__*, fpdf_form_handle_t__*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:669:5
    #7 0x55f4b6a37649 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:929:9
    #8 0x55f4b6a342fd in main samples/pdfium_test.cc:1138:5

0x60c0000116e8 is located 104 bytes inside of 128-byte region [0x60c000011680,0x60c000011700)
freed by thread T0 here:
    #0 0x55f4b6a3190d in operator delete(void*) /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:160:3
    #1 0x55f4b6a9f74d in std::__1::default_delete<CPDFSDK_PageView>::operator()(CPDFSDK_PageView*) const buildtools/third_party/libc++/trunk/include/memory:2338:5
    #2 0x55f4b6a9f6ea in std::__1::unique_ptr<CPDFSDK_PageView, std::__1::default_delete<CPDFSDK_PageView> >::reset(CPDFSDK_PageView*) buildtools/third_party/libc++/trunk/include/memory:2651:7
    #3 0x55f4b6a9ad1a in std::__1::unique_ptr<CPDFSDK_PageView, std::__1::default_delete<CPDFSDK_PageView> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2605:19
    #4 0x55f4b6a9ce7c in std::__1::pair<IPDF_Page* const, std::__1::unique_ptr<CPDFSDK_PageView, std::__1::default_delete<CPDFSDK_PageView> > >::~pair() buildtools/third_party/libc++/trunk/include/utility:315:29
    #5 0x55f4b6a9ce6b in void std::__1::allocator_traits<std::__1::allocator<std::__1::__tree_node<std::__1::__value_type<IPDF_Page*, std::__1::unique_ptr<CPDFSDK_PageView, std::__1::default_delete<CPDFSDK_PageView> > >, void*> > >::__destroy<std::__1::pair<IPDF_Page* const, std::__1::unique_ptr<CPDFSDK_PageView, std::__1::default_delete<CPDFSDK_PageView> > > >(std::__1::integral_constant<bool, false>, std::__1::allocator<std::__1::__tree_node<std::__1::__value_type<IPDF_Page*, std::__1::unique_ptr<CPDFSDK_PageView, std::__1::default_delete<CPDFSDK_PageView> > >, void*> >&, std::__1::pair<IPDF_Page* const, std::__1::unique_ptr<CPDFSDK_PageView, std::__1::default_delete<CPDFSDK_PageView> > >*) buildtools/third_party/libc++/trunk/include/memory:1747:23
    #6 0x55f4b6a9ce08 in void std::__1::allocator_traits<std::__1::allocator<std::__1::__tree_node<std::__1::__value_type<IPDF_Page*, std::__1::unique_ptr<CPDFSDK_PageView, std::__1::default_delete<CPDFSDK_PageView> > >, void*> > >::destroy<std::__1::pair<IPDF_Page* const, std::__1::unique_ptr<CPDFSDK_PageView, std::__1::default_delete<CPDFSDK_PageView> > > >(std::__1::allocator<std::__1::__tree_node<std::__1::__value_type<IPDF_Page*, std::__1::unique_ptr<CPDFSDK_PageView, std::__1::default_delete<CPDFSDK_PageView> > >, void*> >&, std::__1::pair<IPDF_Page* const, std::__1::unique_ptr<CPDFSDK_PageView, std::__1::default_delete<CPDFSDK_PageView> > >*) buildtools/third_party/libc++/trunk/include/memory:1595:14
    #7 0x55f4b6aa0e17 in std::__1::__tree<std::__1::__value_type<IPDF_Page*, std::__1::unique_ptr<CPDFSDK_PageView, std::__1::default_delete<CPDFSDK_PageView> > >, std::__1::__map_value_compare<IPDF_Page*, std::__1::__value_type<IPDF_Page*, std::__1::unique_ptr<CPDFSDK_PageView, std::__1::default_delete<CPDFSDK_PageView> > >, std::__1::less<IPDF_Page*>, true>, std::__1::allocator<std::__1::__value_type<IPDF_Page*, std::__1::unique_ptr<CPDFSDK_PageView, std::__1::default_delete<CPDFSDK_PageView> > > > >::erase(std::__1::__tree_const_iterator<std::__1::__value_type<IPDF_Page*, std::__1::unique_ptr<CPDFSDK_PageView, std::__1::default_delete<CPDFSDK_PageView> > >, std::__1::__tree_node<std::__1::__value_type<IPDF_Page*, std::__1::unique_ptr<CPDFSDK_PageView, std::__1::default_delete<CPDFSDK_PageView> > >, void*>*, long>) buildtools/third_party/libc++/trunk/include/__tree:2561:5
    #8 0x55f4b6a9b8de in std::__1::map<IPDF_Page*, std::__1::unique_ptr<CPDFSDK_PageView, std::__1::default_delete<CPDFSDK_PageView> >, std::__1::less<IPDF_Page*>, std::__1::allocator<std::__1::pair<IPDF_Page* const, std::__1::unique_ptr<CPDFSDK_PageView, std::__1::default_delete<CPDFSDK_PageView> > > > >::erase(std::__1::__map_iterator<std::__1::__tree_iterator<std::__1::__value_type<IPDF_Page*, std::__1::unique_ptr<CPDFSDK_PageView, std::__1::default_delete<CPDFSDK_PageView> > >, std::__1::__tree_node<std::__1::__value_type<IPDF_Page*, std::__1::unique_ptr<CPDFSDK_PageView, std::__1::default_delete<CPDFSDK_PageView> > >, void*>*, long> >) buildtools/third_party/libc++/trunk/include/map:1301:56
    #9 0x55f4b6a9b6da in CPDFSDK_FormFillEnvironment::RemovePageView(IPDF_Page*) fpdfsdk/cpdfsdk_formfillenvironment.cpp:646:13
    #10 0x55f4b96d146e in CPDFXFA_DocEnvironment::PageViewEvent(CXFA_FFPageView*, unsigned int) fpdfsdk/fpdfxfa/cpdfxfa_docenvironment.cpp:297:35
    #11 0x55f4b941d5b5 in CXFA_FFDocView::RunLayout() xfa/fxfa/cxfa_ffdocview.cpp:462:34
    #12 0x55f4b941db8d in CXFA_FFDocView::UpdateDocView() xfa/fxfa/cxfa_ffdocview.cpp:189:7
    #13 0x55f4b945cf47 in CXFA_FFWidgetHandler::OnMouseExit(CXFA_FFWidget*) xfa/fxfa/cxfa_ffwidgethandler.cpp:42:15
    #14 0x55f4b96d5751 in CPDFXFA_WidgetHandler::OnMouseExit(CPDFSDK_PageView*, fxcrt::ObservedPtr<CPDFSDK_Annot>*, unsigned int) fpdfsdk/fpdfxfa/cpdfxfa_widgethandler.cpp:392:19
    #15 0x55f4b6a5864f in CPDFSDK_AnnotHandlerMgr::Annot_OnMouseExit(CPDFSDK_PageView*, fxcrt::ObservedPtr<CPDFSDK_Annot>*, unsigned int) fpdfsdk/cpdfsdk_annothandlermgr.cpp:224:35
    #16 0x55f4b6ab2758 in CPDFSDK_PageView::ExitWidget(CPDFSDK_AnnotHandlerMgr*, bool, unsigned int) fpdfsdk/cpdfsdk_pageview.cpp:414:25
    #17 0x55f4b6ab2516 in CPDFSDK_PageView::OnMouseMove(CFX_PTemplate<float> const&, int) fpdfsdk/cpdfsdk_pageview.cpp:378:5
    #18 0x55f4b6ad54db in FORM_OnMouseMove fpdfsdk/fpdf_formfill.cpp:360:21
    #19 0x55f4b6a46924 in (anonymous namespace)::SendMouseMoveEvent(fpdf_form_handle_t__*, fpdf_page_t__*, std::__1::vector<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::allocator<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > > > const&) samples/pdfium_test_event_helper.cc:107:3
    #20 0x55f4b6a46062 in SendPageEvents(fpdf_form_handle_t__*, fpdf_page_t__*, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test_event_helper.cc:142:7
    #21 0x55f4b6a3da2f in (anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__*, fpdf_form_handle_t__*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:669:5
    #22 0x55f4b6a37649 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:929:9
    #23 0x55f4b6a342fd in main samples/pdfium_test.cc:1138:5

previously allocated by thread T0 here:
    #0 0x55f4b6a310ad in operator new(unsigned long) /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:99:3
    #1 0x55f4b6a9aa50 in pdfium::internal::MakeUniqueResult<CPDFSDK_PageView>::Scalar pdfium::MakeUnique<CPDFSDK_PageView, CPDFSDK_FormFillEnvironment*, IPDF_Page*&>(CPDFSDK_FormFillEnvironment*&&, IPDF_Page*&) third_party/base/ptr_util.h:56:29
    #2 0x55f4b6a96ef4 in CPDFSDK_FormFillEnvironment::GetPageView(IPDF_Page*, bool) fpdfsdk/cpdfsdk_formfillenvironment.cpp:572:15
    #3 0x55f4b6ad5586 in (anonymous namespace)::FormHandleToPageView(fpdf_form_handle_t__*, fpdf_page_t__*) fpdfsdk/fpdf_formfill.cpp:171:39
    #4 0x55f4b6ad6491 in FORM_OnAfterLoadPage fpdfsdk/fpdf_formfill.cpp:619:37
    #5 0x55f4b6a3d62c in (anonymous namespace)::GetPageForIndex(_FPDF_FORMFILLINFO*, fpdf_document_t__*, int) samples/pdfium_test.cc:646:3
    #6 0x55f4b6a3d9e9 in (anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__*, fpdf_form_handle_t__*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:665:20
    #7 0x55f4b6a37649 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:929:9
    #8 0x55f4b6a342fd in main samples/pdfium_test.cc:1138:5

Shadow bytes around the buggy address:
  0x0c187fffa280: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
  0x0c187fffa290: 00 00 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x0c187fffa2a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa
  0x0c187fffa2b0: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
  0x0c187fffa2c0: 00 00 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
=>0x0c187fffa2d0: fd fd fd fd fd fd fd fd fd fd fd fd fd[fd]fd fd
  0x0c187fffa2e0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c187fffa2f0: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
  0x0c187fffa300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c187fffa310: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c187fffa320: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa
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
  Shadow gap:              cc

What is the expected behavior?

What went wrong?
^

Did this work before? N/A 

Chrome version: 78.0.3904.101  Channel: n/a
OS Version: 
Flash Version:

## Attachments

- [chromium-1026991.pdf](attachments/chromium-1026991.pdf) (application/pdf, 729 B)
- [chromium-1026991.evt](attachments/chromium-1026991.evt) (application/octet-stream, 87 B)
- [chromium-1026991-1.pdf](attachments/chromium-1026991-1.pdf) (application/pdf, 812 B)
- [chromium-1026991-1.evt](attachments/chromium-1026991-1.evt) (application/octet-stream, 77 B)

## Timeline

### pd...@gmail.com (2019-11-21)

Triggering this requires minor user interaction.

1. Enter character into field.
2. Remove focus for that field (by tabbing to a different field or otherwise).
3. Move mouse away from field.

It's likely possible to automate the second step in FormCalc by calling setFocus() when the field changes.

I've attached the event file to use with pdfium_test.

### pd...@gmail.com (2019-11-21)

Note: Chrome doesn't use XFA.

### me...@chromium.org (2019-11-21)

Lei, PTAL?

[Monorail components: Internals>Plugins>PDF]

### pd...@gmail.com (2020-01-08)

I produced a non-XFA PDF with the same conditions and interaction, which also calls CPDFSDK_PageView::ExitWidget, but it doesn't show the bug. The different is that XFA goes through CPDFXFA_WidgetHandler::OnMouseExit rather than CPDFSDK_WidgetHandler::OnMouseExit.

### pd...@gmail.com (2020-02-08)

As mentioned, I'm attaching a PDF with the second step automated.



### th...@chromium.org (2020-02-20)

Thanks for the easy repro.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-21)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/689a47976f8cf260df674e7579d0d53d2e43e4b3

commit 689a47976f8cf260df674e7579d0d53d2e43e4b3
Author: Lei Zhang <thestig@chromium.org>
Date: Fri Feb 21 00:45:39 2020

Observe CPDFSDK_PageView inside ExitWidget().

ExitWidget() can trigger the deletion of caller. Use an ObserverPtr to
check for this and bail out safely.

Bug: chromium:1026991
Change-Id: If27c1b02a0d6f3bb39c999a85366e393fa150687
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/66815
Commit-Queue: Lei Zhang <thestig@chromium.org>
Reviewed-by: Tom Sepez <tsepez@chromium.org>

[add] https://pdfium.googlesource.com/pdfium/+/689a47976f8cf260df674e7579d0d53d2e43e4b3/testing/resources/javascript/xfa_specific/bug_1026991.in
[modify] https://pdfium.googlesource.com/pdfium/+/689a47976f8cf260df674e7579d0d53d2e43e4b3/fpdfsdk/cpdfsdk_pageview.cpp
[add] https://pdfium.googlesource.com/pdfium/+/689a47976f8cf260df674e7579d0d53d2e43e4b3/testing/resources/javascript/xfa_specific/bug_1026991.evt


### th...@chromium.org (2020-02-21)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0f3e96396fce24132b47a1edcc007642848cc82b

commit 0f3e96396fce24132b47a1edcc007642848cc82b
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Feb 21 05:55:46 2020

Roll src/third_party/pdfium adfb1574077d..d41bcabd124f (4 commits)

https://pdfium.googlesource.com/pdfium.git/+log/adfb1574077d..d41bcabd124f

git log adfb1574077d..d41bcabd124f --date=short --first-parent --format='%ad %ae %s'
2020-02-21 nigi@chromium.org Roll buildtools/ 1f38b432e..713b351a1 (7 commits)
2020-02-21 nigi@chromium.org Roll tools/code_coverage/ c7a868bac..a8f20a1da (1 commit)
2020-02-21 thestig@chromium.org Observe CPDFSDK_PageView inside ExitWidget().
2020-02-20 tsepez@chromium.org Add test cases for several recently fixed XFA bugs.

Created with:
  gclient setdep -r src/third_party/pdfium@d41bcabd124f

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:1026991
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I6a4ccbe1b938d8d640da1491b64a79cbde588e7f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2068016
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#743444}

[modify] https://crrev.com/0f3e96396fce24132b47a1edcc007642848cc82b/DEPS


### [Deleted User] (2020-02-21)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-24)

[Empty comment from Monorail migration]

### th...@chromium.org (2020-02-24)

This is similar to https://crbug.com/chromium/1017494. In that bug, the fix missed the code path that this bug triggers.

### na...@google.com (2020-02-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-02-27)

Congrats the Panel decided to award $5,000 for this report!

### na...@google.com (2020-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-05-29)

This issue was migrated from crbug.com/chromium/1026991?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050756)*
