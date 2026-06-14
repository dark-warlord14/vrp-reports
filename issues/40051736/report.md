# Security: PDFium heap-use-after-free in CPDFXFA_Page::GetNextXFAAnnot (XFA)

| Field | Value |
|-------|-------|
| **Issue ID** | [40051736](https://issues.chromium.org/issues/40051736) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | my...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2020-03-11 |
| **Bounty** | $7,500.00 |

## Description

PDFium heap-use-after-free in CPDFXFA\_Page::GetNextXFAAnnot (XFA)

**VULNERABILITY DETAILS**

CPDFSDK\_Annot\* CPDFXFA\_Page::GetNextXFAAnnot(CPDFSDK\_Annot\* pSDKAnnot,  

bool bNext) {  

...  

std::unique\_ptr<IXFA\_WidgetIterator> pWidgetIterator =  

GetXFAPageView()->CreateTraverseWidgetIterator(XFA\_WidgetStatus\_Visible | // ==> trigger JS callback  

XFA\_WidgetStatus\_Viewable |  

XFA\_WidgetStatus\_Focused);

// Check |pSDKAnnot| again because JS may have destroyed it  

if (!pObservedAnnot)  

return nullptr;

if (pWidgetIterator->GetCurrentWidget() != pXFAWidget->GetXFAFFWidget())  

pWidgetIterator->SetCurrentWidget(pXFAWidget->GetXFAFFWidget());

CXFA\_FFWidget\* hNextFocus =  

bNext ? pWidgetIterator->MoveToNext() : pWidgetIterator->MoveToPrevious(); // ==> use object that is freed!!!  

if (!hNextFocus && pSDKAnnot)  

hNextFocus = pWidgetIterator->MoveToFirst();  

...  

}

Function CreateTraverseWidgetIterator() can trigger JS callback => we can free CXFA\_FFWidget object. After that, the  

freed object is used in function pWidgetIterator->MoveToNext().

**VERSION**  

Built from dbb6fcdf4353e6f186ee60b377d594c813f8fa63  

With pdf\_enable\_xfa = true

**REPRODUCTION CASE**  

Run pdfium\_test.exe with input file test.pdf

pdfium\_test.exe --send-events C:\Users\minhtt\OneDrive\pdfium\_issues\pdfium\_38\pdfium\_16\poc\test.pdf

ASAN OUTPUT  

==16148==ERROR: AddressSanitizer: heap-use-after-free on address 0x11a309c00a60 at pc 0x7ff788273ab0 bp 0x0061df6fee10 sp 0x0061df6fee58  

READ of size 8 at 0x11a309c00a60 thread T0  

#0 0x7ff788273aaf in `anonymous namespace'::PageWidgetFilter C:\Users\minhtt\Desktop\pdfium\xfa\fxfa\cxfa\_ffpageview.cpp:88  

#1 0x7ff7882758dc in CXFA\_FFTabOrderPageWidgetIterator::MoveToNext C:\Users\minhtt\Desktop\pdfium\xfa\fxfa\cxfa\_ffpageview.cpp:279  

#2 0x7ff7884589b8 in CPDFXFA\_Page::GetNextXFAAnnot C:\Users\minhtt\Desktop\pdfium\fpdfsdk\fpdfxfa\cpdfxfa\_page.cpp:199  

#3 0x7ff7857412e0 in CPDFSDK\_AnnotHandlerMgr::GetNextAnnot C:\Users\minhtt\Desktop\pdfium\fpdfsdk\cpdfsdk\_annothandlermgr.cpp:325  

#4 0x7ff785740a6a in CPDFSDK\_AnnotHandlerMgr::Annot\_OnKeyDown C:\Users\minhtt\Desktop\pdfium\fpdfsdk\cpdfsdk\_annothandlermgr.cpp:245  

#5 0x7ff7857a49d0 in FORM\_OnKeyDown C:\Users\minhtt\Desktop\pdfium\fpdfsdk\fpdf\_formfill.cpp:474  

#6 0x7ff785732be1 in SendPageEvents C:\Users\minhtt\Desktop\pdfium\samples\pdfium\_test\_event\_helper.cc:150  

#7 0x7ff785727ded in main C:\Users\minhtt\Desktop\pdfium\samples\pdfium\_test.cc:1172  

#8 0x7ff7889514d7 in \_\_scrt\_common\_main\_seh f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl:283  

#9 0x7ffe1f1d7bd3 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017bd3)  

#10 0x7ffe202eced0 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18006ced0)

0x11a309c00a60 is located 64 bytes inside of 88-byte region [0x11a309c00a20,0x11a309c00a78)  

freed by thread T0 here:  

#0 0x7ff7884ebf44 in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ff788245f0f in CXFA\_FFArc::~CXFA\_FFArc C:\Users\minhtt\Desktop\pdfium\xfa\fxfa\cxfa\_ffarc.cpp:14  

#2 0x7ff788356664 in CXFA\_ContentLayoutItem::~CXFA\_ContentLayoutItem C:\Users\minhtt\Desktop\pdfium\xfa\fxfa\layout\cxfa\_contentlayoutitem.cpp:29  

#3 0x7ff788356f63 in CXFA\_ContentLayoutItem::~CXFA\_ContentLayoutItem C:\Users\minhtt\Desktop\pdfium\xfa\fxfa\layout\cxfa\_contentlayoutitem.cpp:24  

#4 0x7ff788386f8a in CXFA\_ViewLayoutProcessor::SaveLayoutItemChildren C:\Users\minhtt\Desktop\pdfium\xfa\fxfa\layout\cxfa\_viewlayoutprocessor.cpp:1614  

#5 0x7ff788386f2a in CXFA\_ViewLayoutProcessor::SaveLayoutItemChildren C:\Users\minhtt\Desktop\pdfium\xfa\fxfa\layout\cxfa\_viewlayoutprocessor.cpp:1613  

#6 0x7ff788386f2a in CXFA\_ViewLayoutProcessor::SaveLayoutItemChildren C:\Users\minhtt\Desktop\pdfium\xfa\fxfa\layout\cxfa\_viewlayoutprocessor.cpp:1613  

#7 0x7ff788386f2a in CXFA\_ViewLayoutProcessor::SaveLayoutItemChildren C:\Users\minhtt\Desktop\pdfium\xfa\fxfa\layout\cxfa\_viewlayoutprocessor.cpp:1613  

#8 0x7ff788386f2a in CXFA\_ViewLayoutProcessor::SaveLayoutItemChildren C:\Users\minhtt\Desktop\pdfium\xfa\fxfa\layout\cxfa\_viewlayoutprocessor.cpp:1613  

#9 0x7ff78837bc56 in CXFA\_ViewLayoutProcessor::PrepareLayout C:\Users\minhtt\Desktop\pdfium\xfa\fxfa\layout\cxfa\_viewlayoutprocessor.cpp:1931  

#10 0x7ff78837a58c in CXFA\_ViewLayoutProcessor::InitLayoutPage C:\Users\minhtt\Desktop\pdfium\xfa\fxfa\layout\cxfa\_viewlayoutprocessor.cpp:352  

#11 0x7ff788378bf9 in CXFA\_LayoutProcessor::StartLayout C:\Users\minhtt\Desktop\pdfium\xfa\fxfa\layout\cxfa\_layoutprocessor.cpp:55  

#12 0x7ff788256a8d in CXFA\_FFDocView::RunLayout C:\Users\minhtt\Desktop\pdfium\xfa\fxfa\cxfa\_ffdocview.cpp:476  

#13 0x7ff788257713 in CXFA\_FFDocView::UpdateDocView C:\Users\minhtt\Desktop\pdfium\xfa\fxfa\cxfa\_ffdocview.cpp:188  

#14 0x7ff78826e5ef in CXFA\_FFNotify::OpenDropDownList C:\Users\minhtt\Desktop\pdfium\xfa\fxfa\cxfa\_ffnotify.cpp:272  

#15 0x7ff785f62b7a in CJX\_HostPseudoModel::openList C:\Users\minhtt\Desktop\pdfium\fxjs\xfa\cjx\_hostpseudomodel.cpp:300  

#16 0x7ff785f60601 in CJX\_HostPseudoModel::openList\_static C:\Users\minhtt\Desktop\pdfium\fxjs\xfa\cjx\_hostpseudomodel.h:33  

#17 0x7ff785f7610a in CJX\_Object::RunMethod C:\Users\minhtt\Desktop\pdfium\fxjs\xfa\cjx\_object.cpp:177  

#18 0x7ff785ef3b5a in CFXJSE\_Engine::NormalMethodCall C:\Users\minhtt\Desktop\pdfium\fxjs\xfa\cfxjse\_engine.cpp:483  

#19 0x7ff785eede67 in `anonymous namespace'::DynPropGetterAdapter_MethodCallback C:\Users\minhtt\Desktop\pdfium\fxjs\xfa\cfxjse_class.cpp:112 #20 0x7ff7860b7bff in v8::internal::FunctionCallbackArguments::Call C:\Users\minhtt\Desktop\pdfium\v8\src\api\api-arguments-inl.h:158 #21 0x7ff7860b4c1e in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> C:\Users\minhtt\Desktop\pdfium\v8\src\builtins\builtins-api.cc:111  

#22 0x7ff7860b22c0 in v8::internal::Builtin\_Impl\_HandleApiCall C:\Users\minhtt\Desktop\pdfium\v8\src\builtins\builtins-api.cc:141  

#23 0x7ff7860b155e in v8::internal::Builtin\_HandleApiCall C:\Users\minhtt\Desktop\pdfium\v8\src\builtins\builtins-api.cc:129  

#24 0x7ff78809dfbb in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_BuiltinExit+0x3b (C:\Users\minhtt\Desktop\pdfium\out\Debug\pdfium\_test.exe+0x14297dfbb)  

#25 0x7ff78802c8ca in Builtins\_InterpreterEntryTrampoline+0xca (C:\Users\minhtt\Desktop\pdfium\out\Debug\pdfium\_test.exe+0x14290c8ca)  

#26 0x7ff788025f1e in Builtins\_ArgumentsAdaptorTrampoline+0xbe (C:\Users\minhtt\Desktop\pdfium\out\Debug\pdfium\_test.exe+0x142905f1e)  

#27 0x7ff78802c8ca in Builtins\_InterpreterEntryTrampoline+0xca (C:\Users\minhtt\Desktop\pdfium\out\Debug\pdfium\_test.exe+0x14290c8ca)  

#28 0x7ff788025f1e in Builtins\_ArgumentsAdaptorTrampoline+0xbe (C:\Users\minhtt\Desktop\pdfium\out\Debug\pdfium\_test.exe+0x142905f1e)

previously allocated by thread T0 here:  

#0 0x7ff7884ec034 in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ff78894fdf6 in operator new f:\dd\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ff78826d9c0 in CXFA\_FFNotify::OnCreateContentLayoutItem C:\Users\minhtt\Desktop\pdfium\xfa\fxfa\cxfa\_ffnotify.cpp:177  

#3 0x7ff788357528 in CXFA\_ContentLayoutProcessor::CreateContentLayoutItem C:\Users\minhtt\Desktop\pdfium\xfa\fxfa\layout\cxfa\_contentlayoutprocessor.cpp:644  

#4 0x7ff78835ed0c in CXFA\_ContentLayoutProcessor::DoLayoutPositionedContainer C:\Users\minhtt\Desktop\pdfium\xfa\fxfa\layout\cxfa\_contentlayoutprocessor.cpp:1032  

#5 0x7ff78836158f in CXFA\_ContentLayoutProcessor::DoLayoutInternal C:\Users\minhtt\Desktop\pdfium\xfa\fxfa\layout\cxfa\_contentlayoutprocessor.cpp:2075  

#6 0x7ff78835f4b5 in CXFA\_ContentLayoutProcessor::DoLayoutPositionedContainer C:\Users\minhtt\Desktop\pdfium\xfa\fxfa\layout\cxfa\_contentlayoutprocessor.cpp:1079  

#7 0x7ff78836158f in CXFA\_ContentLayoutProcessor::DoLayoutInternal C:\Users\minhtt\Desktop\pdfium\xfa\fxfa\layout\cxfa\_contentlayoutprocessor.cpp:2075  

#8 0x7ff78836faed in CXFA\_ContentLayoutProcessor::InsertFlowedItem C:\Users\minhtt\Desktop\pdfium\xfa\fxfa\layout\cxfa\_contentlayoutprocessor.cpp:2356  

#9 0x7ff78836ac69 in CXFA\_ContentLayoutProcessor::DoLayoutFlowedContainer C:\Users\minhtt\Desktop\pdfium\xfa\fxfa\layout\cxfa\_contentlayoutprocessor.cpp:1797  

#10 0x7ff7883615f9 in CXFA\_ContentLayoutProcessor::DoLayoutInternal C:\Users\minhtt\Desktop\pdfium\xfa\fxfa\layout\cxfa\_contentlayoutprocessor.cpp:2068  

#11 0x7ff78835e7ef in CXFA\_ContentLayoutProcessor::DoLayout C:\Users\minhtt\Desktop\pdfium\xfa\fxfa\layout\cxfa\_contentlayoutprocessor.cpp:2047  

#12 0x7ff788378ed0 in CXFA\_LayoutProcessor::DoLayout C:\Users\minhtt\Desktop\pdfium\xfa\fxfa\layout\cxfa\_layoutprocessor.cpp:80  

#13 0x7ff7882563ce in CXFA\_FFDocView::DoLayout C:\Users\minhtt\Desktop\pdfium\xfa\fxfa\cxfa\_ffdocview.cpp:97  

#14 0x7ff78844f0f8 in CPDFXFA\_Context::LoadXFADoc C:\Users\minhtt\Desktop\pdfium\fpdfsdk\fpdfxfa\cpdfxfa\_context.cpp:169  

#15 0x7ff7857a8a51 in FPDF\_LoadXFA C:\Users\minhtt\Desktop\pdfium\fpdfsdk\fpdf\_view.cpp:205  

#16 0x7ff785727b45 in main C:\Users\minhtt\Desktop\pdfium\samples\pdfium\_test.cc:1172  

#17 0x7ff7889514d7 in \_\_scrt\_common\_main\_seh f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl:283  

#18 0x7ffe1f1d7bd3 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017bd3)  

#19 0x7ffe202eced0 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18006ced0)

SUMMARY: AddressSanitizer: heap-use-after-free C:\Users\minhtt\Desktop\pdfium\xfa\fxfa\cxfa\_ffpageview.cpp:88 in `anonymous namespace'::PageWidgetFilter  

Shadow bytes around the buggy address:  

0x03c76af800f0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fa  

0x03c76af80100: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 fa  

0x03c76af80110: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 fa  

0x03c76af80120: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 fa  

0x03c76af80130: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 fa  

=>0x03c76af80140: fa fa fa fa fd fd fd fd fd fd fd fd[fd]fd fd fa  

0x03c76af80150: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 fa  

0x03c76af80160: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 fa  

0x03c76af80170: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 fa  

0x03c76af80180: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 fa  

0x03c76af80190: fa fa fa fa 00 00 00 00 00 00 00 00 00 fc fc fc  

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

==16148==ABORTING

## Attachments

- [test.evt](attachments/test.evt) (application/octet-stream, 56 B)
- [test.pdf](attachments/test.pdf) (application/pdf, 6.3 KB)

## Timeline

### my...@gmail.com (2020-03-11)

I can not attach my poc when creating this issue so I upload it in here

### ts...@chromium.org (2020-03-11)

[Empty comment from Monorail migration]

### ts...@chromium.org (2020-03-11)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### th...@chromium.org (2020-03-11)

Thanks for the report. I own a couple other issues involving CXFA_FFTabOrderPageWidgetIterator, so I can take this. May take a bit of time to resolve since XFA is not shipped to users.

### ts...@chromium.org (2020-03-16)

[Empty comment from Monorail migration]

### th...@chromium.org (2020-03-16)

Or tsepez@ can take this and probably fix it sooner.

### ts...@chromium.org (2020-03-19)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-03-20)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/cdcf21fd6ad96c9cb8c589d91ff09a1b6c856629

commit cdcf21fd6ad96c9cb8c589d91ff09a1b6c856629
Author: Tom Sepez <tsepez@chromium.org>
Date: Fri Mar 20 17:24:24 2020

CXFA_FFTabOrderPageWidgetIterator must retain layout items for widgets.

This will keep the layout item owning the widget (and hence the
widget itself) alive for the lifetime of the iterator.

Bug: chromium:1060549
Change-Id: Ib5751ef9d302e9adc633ca1001b8a670732dd28e
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/67590
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[add] https://pdfium.googlesource.com/pdfium/+/cdcf21fd6ad96c9cb8c589d91ff09a1b6c856629/testing/resources/javascript/xfa_specific/bug_1060549.evt
[modify] https://pdfium.googlesource.com/pdfium/+/cdcf21fd6ad96c9cb8c589d91ff09a1b6c856629/xfa/fxfa/cxfa_ffpageview.h
[add] https://pdfium.googlesource.com/pdfium/+/cdcf21fd6ad96c9cb8c589d91ff09a1b6c856629/testing/resources/javascript/xfa_specific/bug_1060549.in
[modify] https://pdfium.googlesource.com/pdfium/+/cdcf21fd6ad96c9cb8c589d91ff09a1b6c856629/xfa/fxfa/cxfa_ffpageview.cpp


### ts...@chromium.org (2020-03-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-20)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-03-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2293f8995ffda44fd411c7679d2863442dbd558c

commit 2293f8995ffda44fd411c7679d2863442dbd558c
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Mar 20 20:32:09 2020

Roll src/third_party/pdfium 8867d042d59a..fc407350ad45 (6 commits)

https://pdfium.googlesource.com/pdfium.git/+log/8867d042d59a..fc407350ad45

git log 8867d042d59a..fc407350ad45 --date=short --first-parent --format='%ad %ae %s'
2020-03-20 thestig@chromium.org Remove parameter from CFFL_FormFiller::GetCurPageView().
2020-03-20 thestig@chromium.org Disambiguate CPDFSDK_FormFillEnvironment::GetPageView().
2020-03-20 thestig@chromium.org Fix nits in CPDF_Document.
2020-03-20 thestig@chromium.org Make CPDF_Document::FindPageIndex() standalone.
2020-03-20 thestig@chromium.org Simplify CXFA_FFTabOrderPageWidgetIterator.
2020-03-20 tsepez@chromium.org CXFA_FFTabOrderPageWidgetIterator must retain layout items for widgets.

Created with:
  gclient setdep -r src/third_party/pdfium@fc407350ad45

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:1060549
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I4d5dbfaad193fcdd94a073beed307ad9430d2f8e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2112782
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#752158}

[modify] https://crrev.com/2293f8995ffda44fd411c7679d2863442dbd558c/DEPS


### na...@google.com (2020-03-23)

[Empty comment from Monorail migration]

### na...@google.com (2020-03-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-03-26)

Congrats! The Panel decided to award $7,500 for this report! 

### na...@google.com (2020-03-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-06-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-06-26)

This issue was migrated from crbug.com/chromium/1060549?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051736)*
