# pdfium (XFA): wrong object type / uaf in SyncContainer

| Field | Value |
|-------|-------|
| **Issue ID** | [40094502](https://issues.chromium.org/issues/40094502) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | pd...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-04-04 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.124 Safari/537.36

Steps to reproduce the problem:
This is related to https://crbug.com/chromium/943522.

The following (simplified) snippet is invalid because overflow sets the trailer attribute to its containing subform. (An overflow trailer is inserted at the end of a subform if it overflows a page.) This causes SyncContainer to call itself recursively as it ping-pongs between both elements until the eventual stack overflow. And somewhere on the way it confuses objects.

<subform id="a"><exclGroup><overflow trailer="#a"/>

https://cs.chromium.org/chromium/src/third_party/pdfium/xfa/fxfa/layout/cxfa_layoutpagemgr.cpp?l=102&rcl=d5bcd378e5892bf6b0bac1e3b3a0982156e179a3

What is the expected behavior?

What went wrong?
^

Did this work before? N/A 

Chrome version: 70.0.3538.124  Channel: n/a
OS Version: 
Flash Version:

## Attachments

- [chromium-949413.pdf](attachments/chromium-949413.pdf) (application/pdf, 603 B)
- [patch-949413](attachments/patch-949413) (text/plain, 2.0 KB)

## Timeline

### pd...@gmail.com (2019-04-04)

(UBSAN)

xfa/fxfa/layout/cxfa_layoutpagemgr.cpp:128:17: runtime error: member call on address 0x5566fd289360 which does not point to an object of type 'CXFA_LayoutItem'
0x5566fd289360: note: object is of type 'CXFA_Subform'
 00 00 00 00  98 aa 84 fb 66 55 00 00  60 c2 1c fd 66 55 00 00  08 00 00 00 7c 00 00 00  ef 2f 01 f8
              ^~~~~~~~~~~~~~~~~~~~~~~
              vptr for 'CXFA_Subform'
    #0 0x5566fb756cdd in (anonymous namespace)::SyncContainer(CXFA_FFNotify*, CXFA_LayoutProcessor*, CXFA_LayoutItem*, unsigned int, bool, int) xfa/fxfa/layout/cxfa_layoutpagemgr.cpp:128:17
    #1 0x5566fb756d5d in (anonymous namespace)::SyncContainer(CXFA_FFNotify*, CXFA_LayoutProcessor*, CXFA_LayoutItem*, unsigned int, bool, int) xfa/fxfa/layout/cxfa_layoutpagemgr.cpp:129:7
    #2 0x5566fb7564e4 in CXFA_LayoutPageMgr::SyncLayoutData() xfa/fxfa/layout/cxfa_layoutpagemgr.cpp:1936:9
    #3 0x5566fb7583f1 in CXFA_LayoutProcessor::DoLayout() xfa/fxfa/layout/cxfa_layoutprocessor.cpp:89:23
    #4 0x5566fad4a457 in CXFA_FFDocView::DoLayout() xfa/fxfa/cxfa_ffdocview.cpp:96:30
    #5 0x5566facc5b8e in CPDFXFA_Context::LoadXFADoc() fpdfsdk/fpdfxfa/cpdfxfa_context.cpp:131:18
    #6 0x5566fa6b9a4a in FPDF_LoadXFA fpdfsdk/fpdf_view.cpp:255:32
    #7 0x5566f95a93d1 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:800:12
    #8 0x5566f95a74c8 in main samples/pdfium_test.cc:1015:5


### pd...@gmail.com (2019-04-04)

(ASAN)

AddressSanitizer: heap-use-after-free on address 0x60c00000b828 at pc 0x55e1be27c5ae bp 0x7fff5483c110 sp 0x7fff5483c108
READ of size 8 at 0x60c00000b828 thread T0
SCARINESS: 51 (8-byte-read-heap-use-after-free)
    #0 0x55e1be27c5ad in fxcrt::UnownedPtr<CXFA_Node>::Get() const core/fxcrt/unowned_ptr.h:91:36
    #1 0x55e1be3fc66c in CXFA_LayoutItem::GetFormNode() const xfa/fxfa/layout/cxfa_layoutitem.h:33:55
    #2 0x55e1bec395ac in (anonymous namespace)::SyncContainer(CXFA_FFNotify*, CXFA_LayoutProcessor*, CXFA_LayoutItem*, unsigned int, bool, int) xfa/fxfa/layout/cxfa_layoutpagemgr.cpp:113:25
    #3 0x55e1bec39694 in (anonymous namespace)::SyncContainer(CXFA_FFNotify*, CXFA_LayoutProcessor*, CXFA_LayoutItem*, unsigned int, bool, int) xfa/fxfa/layout/cxfa_layoutpagemgr.cpp:129:7
    #4 0x55e1bec39694 in (anonymous namespace)::SyncContainer(CXFA_FFNotify*, CXFA_LayoutProcessor*, CXFA_LayoutItem*, unsigned int, bool, int) xfa/fxfa/layout/cxfa_layoutpagemgr.cpp:129:7
    #5 0x55e1bec38e80 in CXFA_LayoutPageMgr::SyncLayoutData() xfa/fxfa/layout/cxfa_layoutpagemgr.cpp:1936:9
    #6 0x55e1bec3abf5 in CXFA_LayoutProcessor::DoLayout() xfa/fxfa/layout/cxfa_layoutprocessor.cpp:89:23
    #7 0x55e1be479d49 in CXFA_FFDocView::DoLayout() xfa/fxfa/cxfa_ffdocview.cpp:96:30
    #8 0x55e1be420269 in CPDFXFA_Context::LoadXFADoc() fpdfsdk/fpdfxfa/cpdfxfa_context.cpp:131:18
    #9 0x55e1bdeb4196 in FPDF_LoadXFA fpdfsdk/fpdf_view.cpp:255:32
    #10 0x55e1bbeb8d92 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:800:12
    #11 0x55e1bbeb62b0 in main samples/pdfium_test.cc:1015:5

0x60c00000b828 is located 40 bytes inside of 128-byte region [0x60c00000b800,0x60c00000b880)
freed by thread T0 here:
    #0 0x55e1bbeb3d1d in operator delete(void*) /b/swarming/w/ir/k/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cc:166:3
    #1 0x55e1be49a895 in CXFA_FFWidget::~CXFA_FFWidget() xfa/fxfa/cxfa_ffwidget.cpp:239:31
    #2 0x55e1bec26223 in XFA_ReleaseLayoutItem(CXFA_LayoutItem*) xfa/fxfa/layout/cxfa_layoutitem.cpp:34:3
    #3 0x55e1bec26124 in CXFA_ItemLayoutProcessor::ProcessUnUseOverFlow(CXFA_Node*, CXFA_Node*, CXFA_ContentLayoutItem*, CXFA_Node*) xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:1491:5
    #4 0x55e1bec2b56b in CXFA_ItemLayoutProcessor::InsertFlowedItem(CXFA_ItemLayoutProcessor*, bool, bool, float, XFA_AttributeValue, unsigned char*, std::__1::vector<CXFA_ContentLayoutItem*, std::__1::allocator<CXFA_ContentLayoutItem*> > (&) [3], bool, float, float, float, float*, float*, float*, bool*, bool*, CXFA_LayoutContext*, bool) xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:2527:21
    #5 0x55e1bec2799d in CXFA_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA_AttributeValue, float, float, CXFA_LayoutContext*, bool) xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:1800:23
    #6 0x55e1bec1ee34 in CXFA_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA_LayoutContext*) xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:2064:18
    #7 0x55e1bec3ab03 in CXFA_LayoutProcessor::DoLayout() xfa/fxfa/layout/cxfa_layoutprocessor.cpp:74:43
    #8 0x55e1be479d49 in CXFA_FFDocView::DoLayout() xfa/fxfa/cxfa_ffdocview.cpp:96:30
    #9 0x55e1be420269 in CPDFXFA_Context::LoadXFADoc() fpdfsdk/fpdfxfa/cpdfxfa_context.cpp:131:18
    #10 0x55e1bdeb4196 in FPDF_LoadXFA fpdfsdk/fpdf_view.cpp:255:32
    #11 0x55e1bbeb8d92 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:800:12
    #12 0x55e1bbeb62b0 in main samples/pdfium_test.cc:1015:5

previously allocated by thread T0 here:
    #0 0x55e1bbeb34bd in operator new(unsigned long) /b/swarming/w/ir/k/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cc:105:3
    #1 0x55e1be48b0b9 in pdfium::internal::MakeUniqueResult<CXFA_FFWidget>::Scalar pdfium::MakeUnique<CXFA_FFWidget, CXFA_Node*&>(CXFA_Node*&) third_party/base/ptr_util.h:56:29
    #2 0x55e1be4888f4 in CXFA_FFNotify::OnCreateContentLayoutItem(CXFA_Node*) xfa/fxfa/cxfa_ffnotify.cpp:195:17
    #3 0x55e1bec1a20e in CXFA_ItemLayoutProcessor::CreateContentLayoutItem(CXFA_Node*) xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:643:23
    #4 0x55e1bec1f735 in CXFA_ItemLayoutProcessor::DoLayoutPositionedContainer(CXFA_LayoutContext*) xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:1026:19
    #5 0x55e1bec1edc5 in CXFA_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA_LayoutContext*) xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:2071:11
    #6 0x55e1bec2a914 in CXFA_ItemLayoutProcessor::InsertFlowedItem(CXFA_ItemLayoutProcessor*, bool, bool, float, XFA_AttributeValue, unsigned char*, std::__1::vector<CXFA_ContentLayoutItem*, std::__1::allocator<CXFA_ContentLayoutItem*> > (&) [3], bool, float, float, float, float*, float*, float*, bool*, bool*, CXFA_LayoutContext*, bool) xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:2394:37
    #7 0x55e1bec2799d in CXFA_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA_AttributeValue, float, float, CXFA_LayoutContext*, bool) xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:1800:23
    #8 0x55e1bec1ee34 in CXFA_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA_LayoutContext*) xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:2064:18
    #9 0x55e1bec3ab03 in CXFA_LayoutProcessor::DoLayout() xfa/fxfa/layout/cxfa_layoutprocessor.cpp:74:43
    #10 0x55e1be479d49 in CXFA_FFDocView::DoLayout() xfa/fxfa/cxfa_ffdocview.cpp:96:30
    #11 0x55e1be420269 in CPDFXFA_Context::LoadXFADoc() fpdfsdk/fpdfxfa/cpdfxfa_context.cpp:131:18
    #12 0x55e1bdeb4196 in FPDF_LoadXFA fpdfsdk/fpdf_view.cpp:255:32
    #13 0x55e1bbeb8d92 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:800:12
    #14 0x55e1bbeb62b0 in main samples/pdfium_test.cc:1015:5

SUMMARY: AddressSanitizer: heap-use-after-free core/fxcrt/unowned_ptr.h:91:36 in fxcrt::UnownedPtr<CXFA_Node>::Get() const
Shadow bytes around the buggy address:
  0x0c187fff96b0: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
  0x0c187fff96c0: 00 00 00 00 00 00 00 00 fa fa fa fa fa fa fa fa
  0x0c187fff96d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c187fff96e0: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
  0x0c187fff96f0: 00 00 00 00 00 00 00 00 fa fa fa fa fa fa fa fa
=>0x0c187fff9700: fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd
  0x0c187fff9710: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c187fff9720: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
  0x0c187fff9730: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c187fff9740: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c187fff9750: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
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


### pd...@gmail.com (2019-04-04)

[Empty comment from Monorail migration]

### pd...@gmail.com (2019-04-04)

The possible patch expand on the patch of https://crbug.com/chromium/943522, but that's not required for this issue.

### cl...@chromium.org (2019-04-04)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5658659601383424.

### cl...@chromium.org (2019-04-04)

Detailed report: https://clusterfuzz.com/testcase?key=5658659601383424

Fuzzer: libFuzzer_pdfium_xfa_fuzzer
Fuzz target binary: pdfium_xfa_fuzzer
Job Type: libfuzzer_chrome_asan
Platform Id: linux

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x610000016888
Crash State:
  CXFA_LayoutItem::IsContentLayoutItem
  SyncContainer
  SyncContainer
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=556697:556708

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5658659601383424

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### cl...@chromium.org (2019-04-04)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Plugins>PDF]

### cl...@chromium.org (2019-04-04)

Automatically adding ccs based on suspected regression changelists:

Restore logic of CreateChildUIAndValueNodesIfNeeded(). by hnakashima@chromium.org - https://pdfium.googlesource.com/pdfium/+/c732e9aa64a82c06c0ad369088d0481dd2636b86

Ensure that XFA Pages always have a corresponding PDF page by tsepez@chromium.org - https://pdfium.googlesource.com/pdfium/+/e7207f33f8024b59fc85abb1b4594b0fbab5361b

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label.

### sh...@chromium.org (2019-04-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-05)

[Empty comment from Monorail migration]

### mb...@chromium.org (2019-04-08)

[Empty comment from Monorail migration]

### ts...@chromium.org (2019-04-16)

I'm going to bounce this to thestig who was looking at the related issue and patch/

### cl...@chromium.org (2019-05-09)

ClusterFuzz has detected this issue as fixed in range 657870:657884.

Detailed report: https://clusterfuzz.com/testcase?key=5658659601383424

Fuzzer: libFuzzer_pdfium_xfa_fuzzer
Fuzz target binary: pdfium_xfa_fuzzer
Job Type: libfuzzer_chrome_asan
Platform Id: linux

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x610000016888
Crash State:
  CXFA_LayoutItem::IsContentLayoutItem
  SyncContainer
  SyncContainer
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=556697:556708
Fixed: https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=657870:657884

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5658659601383424

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2019-05-09)

ClusterFuzz testcase 5658659601383424 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2019-05-10)

[Empty comment from Monorail migration]

### na...@google.com (2019-05-13)

[Empty comment from Monorail migration]

### na...@google.com (2019-05-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### th...@chromium.org (2019-05-15)

CF says https://pdfium.googlesource.com/pdfium/+/17dedfae fixed this.

### na...@google.com (2019-05-15)

Congrats the Panel decided to reward $3,000 for this report

### na...@google.com (2019-05-15)

[Empty comment from Monorail migration]

### th...@chromium.org (2019-07-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/949413?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/943522]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094502)*
