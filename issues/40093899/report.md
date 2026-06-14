# pdfium: use-after-dtor in CPDF_GeneralState::StateData::~StateData()

| Field | Value |
|-------|-------|
| **Issue ID** | [40093899](https://issues.chromium.org/issues/40093899) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | pd...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2019-01-30 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.124 Safari/537.36

Steps to reproduce the problem:
To reproduce set is_msan, and run as follows.

$ MSAN_OPTIONS=poison_in_dtor=1 pdfium_test path/to/pdf

==32141==WARNING: MemorySanitizer: use-of-uninitialized-value
    #0 0x55a743213953 in CPDF_GeneralState::StateData::~StateData() core/fpdfapi/page/cpdf_generalstate.cpp:298:9
    #1 0x55a743213a6c in CPDF_GeneralState::StateData::~StateData() core/fpdfapi/page/cpdf_generalstate.cpp:294:44
    #2 0x55a7432c7e0f in std::__1::unique_ptr<CPDF_GeneralState::StateData, fxcrt::ReleaseDeleter<CPDF_GeneralState::StateData> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2592:19
    #3 0x55a7432c7de8 in fxcrt::RetainPtr<CPDF_GeneralState::StateData>::~RetainPtr() core/fxcrt/retain_ptr.h:101:16
    #4 0x55a7432119f8 in fxcrt::SharedCopyOnWrite<CPDF_GeneralState::StateData>::~SharedCopyOnWrite() core/fxcrt/shared_copy_on_write.h:23:25
    #5 0x55a7432119e8 in CPDF_GeneralState::~CPDF_GeneralState() core/fpdfapi/page/cpdf_generalstate.cpp:76:42
    #6 0x55a7431de76f in CPDF_GraphicStates::~CPDF_GraphicStates() core/fpdfapi/page/cpdf_graphicstates.cpp:11:44
    #7 0x55a74320da3e in CPDF_PageObject::~CPDF_PageObject() core/fpdfapi/page/cpdf_pageobject.cpp:16:35
    #8 0x55a7432223dc in CPDF_PathObject::~CPDF_PathObject() core/fpdfapi/page/cpdf_pathobject.cpp:14:35
    #9 0x55a74322243c in CPDF_PathObject::~CPDF_PathObject() core/fpdfapi/page/cpdf_pathobject.cpp:14:35
    #10 0x55a743102e9f in std::__1::unique_ptr<CPDF_PageObject, std::__1::default_delete<CPDF_PageObject> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2592:19
    #11 0x55a74327aada in std::__1::__deque_base<std::__1::unique_ptr<CPDF_PageObject, std::__1::default_delete<CPDF_PageObject> >, std::__1::allocator<std::__1::unique_ptr<CPDF_PageObject, std::__1::default_delete<CPDF_PageObject> > > >::clear() buildtools/third_party/libc++/trunk/include/deque:1175:9
    #12 0x55a7432209d3 in std::__1::__deque_base<std::__1::unique_ptr<CPDF_PageObject, std::__1::default_delete<CPDF_PageObject> >, std::__1::allocator<std::__1::unique_ptr<CPDF_PageObject, std::__1::default_delete<CPDF_PageObject> > > >::~__deque_base() buildtools/third_party/libc++/trunk/include/deque:1112:5
    #13 0x55a74320c71b in CPDF_PageObjectHolder::~CPDF_PageObjectHolder() core/fpdfapi/page/cpdf_pageobjectholder.cpp:47:47
    #14 0x55a74320c66c in CPDF_Form::~CPDF_Form() core/fpdfapi/page/cpdf_form.cpp:46:23
    #15 0x55a74320c84c in CPDF_Form::~CPDF_Form() core/fpdfapi/page/cpdf_form.cpp:46:23
    #16 0x55a74319c0af in std::__1::unique_ptr<CPDF_Form, std::__1::default_delete<CPDF_Form> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2592:19
    #17 0x55a74326137b in CPDF_TilingPattern::~CPDF_TilingPattern() core/fpdfapi/page/cpdf_tilingpattern.cpp:24:44
    #18 0x55a7432613fc in CPDF_TilingPattern::~CPDF_TilingPattern() core/fpdfapi/page/cpdf_tilingpattern.cpp:24:43
    #19 0x55a7431fd7cb in CPDF_DocPageData::Clear(bool) core/fpdfapi/page/cpdf_docpagedata.cpp:69:15
    #20 0x55a7431fc9b3 in CPDF_DocPageData::~CPDF_DocPageData() core/fpdfapi/page/cpdf_docpagedata.cpp:38:3
    #21 0x55a7433e786e in std::__1::default_delete<CPDF_DocPageData>::operator()(CPDF_DocPageData*) const buildtools/third_party/libc++/trunk/include/memory:2325:5
    #22 0x55a743345ddf in std::__1::unique_ptr<CPDF_DocPageData, std::__1::default_delete<CPDF_DocPageData> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2592:19
    #23 0x55a743345c38 in CPDF_Document::~CPDF_Document() core/fpdfapi/parser/cpdf_document.cpp:190:31
    #24 0x55a743345f0c in CPDF_Document::~CPDF_Document() core/fpdfapi/parser/cpdf_document.cpp:190:31
    #25 0x55a74310893f in std::__1::unique_ptr<CPDF_Document, std::__1::default_delete<CPDF_Document> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2592:19
    #26 0x55a743118582 in FPDF_CloseDocument fpdfsdk/fpdf_view.cpp:732:3
    #27 0x55a742da14ff in std::__1::unique_ptr<fpdf_document_t__, FPDFDocumentDeleter>::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2592:19
    #28 0x55a742d94e2a in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:841:1
    #29 0x55a742d901e6 in main samples/pdfium_test.cc:1006:5

  Memory was marked as uninitialized
    #1 0x55a743345dac in std::__1::unique_ptr<CPDF_DocRenderData, std::__1::default_delete<CPDF_DocRenderData> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2592:28
    #2 0x55a743345c1f in CPDF_Document::~CPDF_Document() core/fpdfapi/parser/cpdf_document.cpp:190:31
    #3 0x55a743345f0c in CPDF_Document::~CPDF_Document() core/fpdfapi/parser/cpdf_document.cpp:190:31
    #4 0x55a74310893f in std::__1::unique_ptr<CPDF_Document, std::__1::default_delete<CPDF_Document> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2592:19
    #5 0x55a743118582 in FPDF_CloseDocument fpdfsdk/fpdf_view.cpp:732:3
    #6 0x55a742da14ff in std::__1::unique_ptr<fpdf_document_t__, FPDFDocumentDeleter>::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2592:19
    #7 0x55a742d94e2a in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:841:1
    #8 0x55a742d901e6 in main samples/pdfium_test.cc:1006:5

What is the expected behavior?

What went wrong?
^

Did this work before? N/A 

Chrome version: 70.0.3538.124  Channel: stable
OS Version: 
Flash Version:

## Attachments

- [chromium-926640.pdf](attachments/chromium-926640.pdf) (application/pdf, 764 B)

## Timeline

### pd...@gmail.com (2019-01-30)

[Comment Deleted]

### pd...@gmail.com (2019-01-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-01-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5093009121214464.

### cl...@chromium.org (2019-01-30)

Testcase 5093009121214464 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5093009121214464.

### me...@chromium.org (2019-01-30)

Was able to repro locally. 
Using MSAN_OPTIONS=poison_in_dtor=1 is necessary for reproing.
Because CF doesn't use this, CF wasn't able to repro. Will look into enabling it on CF.
The feature is marked experimental so it is possible this is a false positive, but I haven't looked into it.

dsinclair@ Could you please take a look?

[Monorail components: Internals>Plugins>PDF]

### ds...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### th...@chromium.org (2019-01-31)

https://pdfium-review.googlesource.com/c/pdfium/+/49570

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-01-31)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/228fec164f16009ae630f687d065a54ae4413265

commit 228fec164f16009ae630f687d065a54ae4413265
Author: Lei Zhang <thestig@chromium.org>
Date: Thu Jan 31 18:55:58 2019

Fix CPDF_Document member destruction order.

A class held by |m_pDocPage| accesses |m_pDocRender| during its
destruction. So |m_pDocPage| should be destroyed first.

BUG=chromium:926640

Change-Id: I77daad1e56f72a1af7c41b6467e798cc75acaff0
Reviewed-on: https://pdfium-review.googlesource.com/c/49570
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>

[modify] https://crrev.com/228fec164f16009ae630f687d065a54ae4413265/core/fpdfapi/parser/cpdf_document.cpp
[modify] https://crrev.com/228fec164f16009ae630f687d065a54ae4413265/core/fpdfapi/parser/cpdf_document.h


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-01-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8624e8bc5ef6adaf26c222a5bc03e8a1eec216f8

commit 8624e8bc5ef6adaf26c222a5bc03e8a1eec216f8
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Jan 31 20:01:26 2019

Roll src/third_party/pdfium 96a7c58e4c71..228fec164f16 (1 commits)

https://pdfium.googlesource.com/pdfium.git/+log/96a7c58e4c71..228fec164f16


git log 96a7c58e4c71..228fec164f16 --date=short --no-merges --format='%ad %ae %s'
2019-01-31 thestig@chromium.org Fix CPDF_Document member destruction order.


Created with:
  gclient setdep -r src/third_party/pdfium@228fec164f16

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:926640
TBR=dsinclair@chromium.org

Change-Id: I0d212803d4004106dbb8c7a7dedc7ab1488c9e73
Reviewed-on: https://chromium-review.googlesource.com/c/1448603
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#628052}
[modify] https://crrev.com/8624e8bc5ef6adaf26c222a5bc03e8a1eec216f8/DEPS


### th...@chromium.org (2019-02-01)

Should be fixed.

### sh...@chromium.org (2019-02-01)

[Empty comment from Monorail migration]

### pd...@gmail.com (2019-02-01)

Confirmed.

### na...@google.com (2019-02-04)

[Empty comment from Monorail migration]

### na...@google.com (2019-02-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-02-07)

Congrats! The Panel has decided to reward $1000 for this report :) 

### na...@google.com (2019-02-07)

[Empty comment from Monorail migration]

### pd...@gmail.com (2019-03-02)

It doesn't really matter, but this should be Impact Stable.

### th...@chromium.org (2019-03-04)

Yes, Impact Stable. Do we want to take any more actions here?

### ad...@chromium.org (2019-04-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-05-10)

This issue was migrated from crbug.com/chromium/926640?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093899)*
