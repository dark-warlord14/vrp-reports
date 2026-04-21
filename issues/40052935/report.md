# pdfium(XFA) heap-use-after-free in CXFA_FFWidget::GetWidgetRect()

| Field | Value |
|-------|-------|
| **Issue ID** | [40052935](https://issues.chromium.org/issues/40052935) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux |
| **Reporter** | me...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2020-07-24 |
| **Bounty** | $7,500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36

Steps to reproduce the problem:
1.build pdfium_test with XFA enable
2. put uaf0.pdf and uaf0.evt in same dir
3../pdfium_test --send-events uaf0.pdf

What is the expected behavior?

What went wrong?
Here is the ASAN log
=================================================================
==1621662==ERROR: AddressSanitizer: heap-use-after-free on address 0x60800000f240 at pc 0x5590f3bc60da bp 0x7ffddb5322c0 sp 0x7ffddb5322b8
READ of size 8 at 0x60800000f240 thread T0
    #0 0x5590f3bc60d9 in Get core/fxcrt/unowned_ptr.h:95:36
    #1 0x5590f3bc60d9 in GetLayoutItem xfa/fxfa/cxfa_ffwidget.h:146:72
    #2 0x5590f3bc60d9 in CXFA_FFWidget::GetWidgetRect() const xfa/fxfa/cxfa_ffwidget.cpp:250:8
    #3 0x5590f3bb4267 in operator() xfa/fxfa/cxfa_ffpageview.cpp:423:57
    #4 0x5590f3bb4267 in void std::__1::__sort<CXFA_FFTabOrderPageWidgetIterator::OrderContainer(CXFA_NodeIteratorTemplate<CXFA_LayoutItem, CXFA_TraverseStrategy_LayoutItem, fxcrt::RetainPtr<CXFA_LayoutItem> >*, CXFA_LayoutItem*, CXFA_TabParam*, bool*, bool*, bool)::$_0&, std::__1::unique_ptr<CXFA_TabParam, std::__1::default_delete<CXFA_TabParam> >*>(std::__1::unique_ptr<CXFA_TabParam, std::__1::default_delete<CXFA_TabParam> >*, std::__1::unique_ptr<CXFA_TabParam, std::__1::default_delete<CXFA_TabParam> >*, CXFA_FFTabOrderPageWidgetIterator::OrderContainer(CXFA_NodeIteratorTemplate<CXFA_LayoutItem, CXFA_TraverseStrategy_LayoutItem, fxcrt::RetainPtr<CXFA_LayoutItem> >*, CXFA_LayoutItem*, CXFA_TabParam*, bool*, bool*, bool)::$_0&) buildtools/third_party/libc++/trunk/include/algorithm:3916:17
    #5 0x5590f3baf474 in sort<std::__1::unique_ptr<CXFA_TabParam, std::__1::default_delete<CXFA_TabParam> > *, (lambda at ../../xfa/fxfa/cxfa_ffpageview.cpp:421:13) &> buildtools/third_party/libc++/trunk/include/algorithm:4097:5
    #6 0x5590f3baf474 in sort<std::__1::unique_ptr<CXFA_TabParam, std::__1::default_delete<CXFA_TabParam> >, (lambda at ../../xfa/fxfa/cxfa_ffpageview.cpp:421:13)> buildtools/third_party/libc++/trunk/include/algorithm:4130:5
    #7 0x5590f3baf474 in CXFA_FFTabOrderPageWidgetIterator::OrderContainer(CXFA_NodeIteratorTemplate<CXFA_LayoutItem, CXFA_TraverseStrategy_LayoutItem, fxcrt::RetainPtr<CXFA_LayoutItem> >*, CXFA_LayoutItem*, CXFA_TabParam*, bool*, bool*, bool) xfa/fxfa/cxfa_ffpageview.cpp:420:3
    #8 0x5590f3baf2b5 in CXFA_FFTabOrderPageWidgetIterator::OrderContainer(CXFA_NodeIteratorTemplate<CXFA_LayoutItem, CXFA_TraverseStrategy_LayoutItem, fxcrt::RetainPtr<CXFA_LayoutItem> >*, CXFA_LayoutItem*, CXFA_TabParam*, bool*, bool*, bool) xfa/fxfa/cxfa_ffpageview.cpp:409:9
    #9 0x5590f3baf2b5 in CXFA_FFTabOrderPageWidgetIterator::OrderContainer(CXFA_NodeIteratorTemplate<CXFA_LayoutItem, CXFA_TraverseStrategy_LayoutItem, fxcrt::RetainPtr<CXFA_LayoutItem> >*, CXFA_LayoutItem*, CXFA_TabParam*, bool*, bool*, bool) xfa/fxfa/cxfa_ffpageview.cpp:409:9
    #10 0x5590f3badd51 in CXFA_FFTabOrderPageWidgetIterator::CreateSpaceOrderLayoutItems() xfa/fxfa/cxfa_ffpageview.cpp:440:3
    #11 0x5590f3bab0a2 in CXFA_FFTabOrderPageWidgetIterator::CreateTabOrderWidgetArray() xfa/fxfa/cxfa_ffpageview.cpp:346:7
    #12 0x5590f3ba793d in Reset xfa/fxfa/cxfa_ffpageview.cpp:251:3
    #13 0x5590f3ba793d in CXFA_FFTabOrderPageWidgetIterator xfa/fxfa/cxfa_ffpageview.cpp:244:3
    #14 0x5590f3ba793d in make_unique<CXFA_FFTabOrderPageWidgetIterator, CXFA_FFPageView *, unsigned int &> buildtools/third_party/libc++/trunk/include/memory:3043:32
    #15 0x5590f3ba793d in CXFA_FFPageView::CreateTraverseWidgetIterator(unsigned int) xfa/fxfa/cxfa_ffpageview.cpp:150:10
    #16 0x5590f3e670b4 in CPDFXFA_Page::GetFirstOrLastXFAAnnot(CPDFSDK_PageView*, bool) const fpdfsdk/fpdfxfa/cpdfxfa_page.cpp:222:22
    #17 0x5590f074ef3b in CPDFSDK_AnnotHandlerMgr::GetFirstOrLastFocusableAnnot(CPDFSDK_PageView*, bool) const fpdfsdk/cpdfsdk_annothandlermgr.cpp:363:31
    #18 0x5590f074e880 in CPDFSDK_AnnotHandlerMgr::Annot_OnKeyDown(CPDFSDK_PageView*, CPDFSDK_Annot*, int, int) fpdfsdk/cpdfsdk_annothandlermgr.cpp:250:42
    #19 0x5590f07cd6d6 in FORM_OnKeyDown fpdfsdk/fpdf_formfill.cpp:488:21
    #20 0x5590f073f4e8 in SendKeyCodeEvent samples/pdfium_test_event_helper.cc:52:3
    #21 0x5590f073f4e8 in SendPageEvents(fpdf_form_handle_t__*, fpdf_page_t__*, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test_event_helper.cc:169:7
    #22 0x5590f072ef13 in RenderPage samples/pdfium_test.cc:723:5
    #23 0x5590f072ef13 in RenderPdf samples/pdfium_test.cc:1000:9
    #24 0x5590f072ef13 in main samples/pdfium_test.cc:1223:5
    #25 0x7f6dcf2bb0b2 in __libc_start_main /build/glibc-YYA7BZ/glibc-2.31/csu/../csu/libc-start.c:308:16

0x60800000f240 is located 32 bytes inside of 88-byte region [0x60800000f220,0x60800000f278)
freed by thread T0 here:
    #0 0x5590f072420d in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:160:3
    #1 0x5590f3ce2042 in operator() buildtools/third_party/libc++/trunk/include/memory:2378:5
    #2 0x5590f3ce2042 in reset buildtools/third_party/libc++/trunk/include/memory:2633:7
    #3 0x5590f3ce2042 in ~unique_ptr buildtools/third_party/libc++/trunk/include/memory:2587:19
    #4 0x5590f3ce2042 in CXFA_ContentLayoutItem::~CXFA_ContentLayoutItem() xfa/fxfa/layout/cxfa_contentlayoutitem.cpp:29:1
    #5 0x5590f3ce21fc in CXFA_ContentLayoutItem::~CXFA_ContentLayoutItem() xfa/fxfa/layout/cxfa_contentlayoutitem.cpp:24:51
    #6 0x5590f3d0ebc8 in Release core/fxcrt/retained_tree_node.h:71:7
    #7 0x5590f3d0ebc8 in operator() core/fxcrt/retain_ptr.h:20:47
    #8 0x5590f3d0ebc8 in reset buildtools/third_party/libc++/trunk/include/memory:2633:7
    #9 0x5590f3d0ebc8 in operator= core/fxcrt/retain_ptr.h:73:12
    #10 0x5590f3d0ebc8 in XFA_ReleaseLayoutItem(fxcrt::RetainPtr<CXFA_LayoutItem> const&) xfa/fxfa/layout/cxfa_layoutitem.cpp:25:11
    #11 0x5590f3d0eaf3 in XFA_ReleaseLayoutItem(fxcrt::RetainPtr<CXFA_LayoutItem> const&) xfa/fxfa/layout/cxfa_layoutitem.cpp:24:5
    #12 0x5590f3d0eaf3 in XFA_ReleaseLayoutItem(fxcrt::RetainPtr<CXFA_LayoutItem> const&) xfa/fxfa/layout/cxfa_layoutitem.cpp:24:5
    #13 0x5590f3d0eaf3 in XFA_ReleaseLayoutItem(fxcrt::RetainPtr<CXFA_LayoutItem> const&) xfa/fxfa/layout/cxfa_layoutitem.cpp:24:5
    #14 0x5590f3d0eaf3 in XFA_ReleaseLayoutItem(fxcrt::RetainPtr<CXFA_LayoutItem> const&) xfa/fxfa/layout/cxfa_layoutitem.cpp:24:5
    #15 0x5590f3d13a52 in CXFA_ViewLayoutProcessor::PrepareLayout() xfa/fxfa/layout/cxfa_viewlayoutprocessor.cpp:1908:7
    #16 0x5590f3d1293a in CXFA_ViewLayoutProcessor::InitLayoutPage(CXFA_Node*) xfa/fxfa/layout/cxfa_viewlayoutprocessor.cpp:351:3
    #17 0x5590f3d100e5 in CXFA_LayoutProcessor::StartLayout(bool) xfa/fxfa/layout/cxfa_layoutprocessor.cpp:56:32
    #18 0x5590f3d10937 in CXFA_LayoutProcessor::IncrementLayout() xfa/fxfa/layout/cxfa_layoutprocessor.cpp:108:5
    #19 0x5590f3b7fe5b in CXFA_FFDocView::RunLayout() xfa/fxfa/cxfa_ffdocview.cpp:474:25
    #20 0x5590f3b81512 in CXFA_FFDocView::UpdateDocView() xfa/fxfa/cxfa_ffdocview.cpp:187:7
    #21 0x5590f3ba0d01 in CXFA_FFNotify::OpenDropDownList(CXFA_Node*) xfa/fxfa/cxfa_ffnotify.cpp:270:13
    #22 0x5590f123e58d in CJX_HostPseudoModel::openList(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_hostpseudomodel.cpp:300:14
    #23 0x5590f123b044 in CJX_HostPseudoModel::openList_static(CJX_Object*, CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_hostpseudomodel.h:33:3
    #24 0x5590f1256fe5 in CJX_Object::RunMethod(fxcrt::WideString const&, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_object.cpp:185:10
    #25 0x5590f11a608d in CFXJSE_Engine::NormalMethodCall(v8::FunctionCallbackInfo<v8::Value> const&, fxcrt::WideString const&) fxjs/xfa/cfxjse_engine.cpp:487:31
    #26 0x5590f119f744 in (anonymous namespace)::DynPropGetterAdapter_MethodCallback(v8::FunctionCallbackInfo<v8::Value> const&) fxjs/xfa/cfxjse_class.cpp:102:7
    #27 0x5590f13f9f5f in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api/api-arguments-inl.h:158:3
    #28 0x5590f13f732e in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:111:36
    #29 0x5590f13f4bae in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:141:5
    #30 0x5590f3944a17 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit (/home/krace/fuzz/src/pdfium/out/Debug/pdfium_test+0x442aa17)
    #31 0x5590f38d8754 in Builtins_InterpreterEntryTrampoline (/home/krace/fuzz/src/pdfium/out/Debug/pdfium_test+0x43be754)
    #32 0x5590f38cfa1e in Builtins_ArgumentsAdaptorTrampoline (/home/krace/fuzz/src/pdfium/out/Debug/pdfium_test+0x43b5a1e)
    #33 0x5590f38d8754 in Builtins_InterpreterEntryTrampoline (/home/krace/fuzz/src/pdfium/out/Debug/pdfium_test+0x43be754)
    #34 0x5590f38cfa1e in Builtins_ArgumentsAdaptorTrampoline (/home/krace/fuzz/src/pdfium/out/Debug/pdfium_test+0x43b5a1e)
    #35 0x5590f38d62b9 in Builtins_JSEntryTrampoline (/home/krace/fuzz/src/pdfium/out/Debug/pdfium_test+0x43bc2b9)
    #36 0x5590f38d6097 in Builtins_JSEntry (/home/krace/fuzz/src/pdfium/out/Debug/pdfium_test+0x43bc097)

previously allocated by thread T0 here:
    #0 0x5590f07239ad in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:99:3
    #1 0x5590f3b9ff25 in make_unique<CXFA_FFWidget, CXFA_Node *&> buildtools/third_party/libc++/trunk/include/memory:3043:28
    #2 0x5590f3b9ff25 in CXFA_FFNotify::OnCreateContentLayoutItem(CXFA_Node*) xfa/fxfa/cxfa_ffnotify.cpp:175:17
    #3 0x5590f3ce39d4 in CXFA_ContentLayoutProcessor::CreateContentLayoutItem(CXFA_Node*) xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:644:27
    #4 0x5590f3cece56 in CXFA_ContentLayoutProcessor::DoLayoutPositionedContainer(CXFA_ContentLayoutProcessor::Context*) xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:1032:19
    #5 0x5590f3ceff6b in CXFA_ContentLayoutProcessor::DoLayoutInternal(bool, float, float, CXFA_ContentLayoutProcessor::Context*) xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:2074:11
    #6 0x5590f3ceda64 in CXFA_ContentLayoutProcessor::DoLayoutPositionedContainer(CXFA_ContentLayoutProcessor::Context*) xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:1079:17
    #7 0x5590f3ceff6b in CXFA_ContentLayoutProcessor::DoLayoutInternal(bool, float, float, CXFA_ContentLayoutProcessor::Context*) xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:2074:11
    #8 0x5590f3d03838 in CXFA_ContentLayoutProcessor::InsertFlowedItem(CXFA_ContentLayoutProcessor*, bool, bool, float, XFA_AttributeValue, unsigned char*, std::__1::vector<fxcrt::RetainPtr<CXFA_ContentLayoutItem>, std::__1::allocator<fxcrt::RetainPtr<CXFA_ContentLayoutItem> > > (&) [3], bool, float, float, float, float*, float*, float*, bool*, bool*, CXFA_ContentLayoutProcessor::Context*, bool) xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:2355:29
    #9 0x5590f3cfdcb9 in CXFA_ContentLayoutProcessor::DoLayoutFlowedContainer(bool, XFA_AttributeValue, float, float, CXFA_ContentLayoutProcessor::Context*, bool) xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:1796:23
    #10 0x5590f3d10449 in CXFA_LayoutProcessor::DoLayout() xfa/fxfa/layout/cxfa_layoutprocessor.cpp:81:36
    #11 0x5590f3b7f121 in CXFA_FFDocView::DoLayout() xfa/fxfa/cxfa_ffdocview.cpp:96:38
    #12 0x5590f3e5b844 in CPDFXFA_Context::LoadXFADoc() fpdfsdk/fpdfxfa/cpdfxfa_context.cpp:171:18
    #13 0x5590f07d2953 in FPDF_LoadXFA fpdfsdk/fpdf_view.cpp:216:22
    #14 0x5590f072ea60 in RenderPdf samples/pdfium_test.cc:965:12
    #15 0x5590f072ea60 in main samples/pdfium_test.cc:1223:5
    #16 0x7f6dcf2bb0b2 in __libc_start_main /build/glibc-YYA7BZ/glibc-2.31/csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-use-after-free core/fxcrt/unowned_ptr.h:95:36 in Get
Shadow bytes around the buggy address:
  0x0c107fff9df0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c107fff9e00: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c107fff9e10: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c107fff9e20: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c107fff9e30: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 fa
=>0x0c107fff9e40: fa fa fa fa fd fd fd fd[fd]fd fd fd fd fd fd fa
  0x0c107fff9e50: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x0c107fff9e60: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 fa
  0x0c107fff9e70: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 fa
  0x0c107fff9e80: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c107fff9e90: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 fa
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
==1621662==ABORTING

Did this work before? N/A 

Chrome version: 84.0.4147.89  Channel: n/a
OS Version: 
Flash Version:

## Attachments

- [uaf0.pdf](attachments/uaf0.pdf) (application/pdf, 1.9 KB)
- [uaf0.evt](attachments/uaf0.evt) (application/octet-stream, 10 B)

## Timeline

### me...@gmail.com (2020-07-24)

[Empty comment from Monorail migration]

### me...@gmail.com (2020-07-24)

CREDIT: 
Weipeng Jiang (@Krace) from Codesafe Team of Legendsec at Qi'anxin Group

### me...@gmail.com (2020-07-24)

I provide a easy patch for this one :)

--- xfa/fxfa/cxfa_ffwidget.h	2020-07-24 02:30:39.909122763 -0700
+++ xfa/fxfa/cxfa_ffwidget.h.bak	2020-07-24 02:30:50.689243784 -0700
@@ -192,7 +192,7 @@
   bool IsButtonDown();
   void SetButtonDown(bool bSet);
 
-  RetainPtr<CXFA_ContentLayoutItem> m_pLayoutItem;
+  UnownedPtr<CXFA_ContentLayoutItem> m_pLayoutItem;
   UnownedPtr<CXFA_FFDocView> m_pDocView;
   ObservedPtr<CXFA_FFPageView> m_pPageView;
   UnownedPtr<CXFA_Node> const m_pNode;


### me...@gmail.com (2020-07-24)

Here is the analysis

It was actually in function CXFA_FFTabOrderPageWidgetIterator::OrderContainer of xfa/fxfa/cxfa_ffpageview.cpp:
function OrderContainer is called 4 times  recursively, and the UAF was trigered like this:
OrderContainer(1)=>OrderContainer(2)=>OrderContainer(3)=>OrderContainer(4)=>OrderContainer(3) at line 398=>openlist(free ptr)=> USE again.

397     if (bMasterPage || *bContentArea) {
398       CXFA_FFWidget* hWidget = GetWidget(pSearchItem); // it will call LoadWidget in xfa/fxfa/cxfa_ffcombobox.cpp and then execute JS code to 
                                                                                                         free the `m_pLayoutItem`
399       if (!hWidget) {
400         pSearchItem = sIterator->MoveToNext();
401         continue;
402       }
403       if (pViewItem && (pSearchItem->GetParent() != pViewItem)) {
404         *bCurrentItem = true;
405         break;
406       }
407       tabParams.push_back(std::make_unique<CXFA_TabParam>(hWidget));
408       if (IsLayoutElement(pSearchItem->GetFormNode()->GetElementType(), true)) {
409         OrderContainer(sIterator, pSearchItem, tabParams.back().get(),
410                        bCurrentItem, bContentArea, bMasterPage);
411       }
412     }
413     if (*bCurrentItem) {
414       pSearchItem = sIterator->GetCurrent();
415       *bCurrentItem = false;
416     } else {
417       pSearchItem = sIterator->MoveToNext();
418     }
419   }
420   std::sort(tabParams.begin(), tabParams.end(),
421             [](const std::unique_ptr<CXFA_TabParam>& arg1,
422                const std::unique_ptr<CXFA_TabParam>& arg2) {
423               const CFX_RectF& rt1 = arg1->GetWidget()->GetWidgetRect();
// UAF triger
424               const CFX_RectF& rt2 = arg2->GetWidget()->GetWidgetRect();
425               if (rt1.top - rt2.top >= kXFAWidgetPrecision)
426                 return rt1.top < rt2.top;
427               return rt1.left < rt2.left;
428             });
429   for (const auto& pParam : tabParams)
430     pContainer->AppendTabParam(pParam.get());


Hope this is useful for you guys :)


### aj...@google.com (2020-07-24)

Thanks for the report. CC'ing some interested people.

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2020-07-24)

[Empty comment from Monorail migration]

### ts...@chromium.org (2020-07-24)

Unfortunately, the fix isn't going to be quite as simple as what is suggested in C3, since this would create a cycle of of reference pointers, and lead to a leak.

### ts...@chromium.org (2020-07-24)

CL at https://pdfium-review.googlesource.com/c/pdfium/+/71890

### [Deleted User] (2020-07-24)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-24)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/1c21d8655cb77b7629247e2744ea61e6be4f203a

commit 1c21d8655cb77b7629247e2744ea61e6be4f203a
Author: Tom Sepez <tsepez@chromium.org>
Date: Fri Jul 24 22:14:41 2020

Retain layout items rather than raw widgets in CFXA_TabParam.

Prevent them from popping out of existence while we might be iterating
over them.

-- forward-declare CXFA_TabParam in header file.

Bug: chromium:1109108
Change-Id: I0e97cf3a98861e004808c124f5cfdffb3abf27fd
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/71890
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>

[add] https://pdfium.googlesource.com/pdfium/+/1c21d8655cb77b7629247e2744ea61e6be4f203a/testing/resources/javascript/xfa_specific/bug_1109108_expected.txt
[modify] https://pdfium.googlesource.com/pdfium/+/1c21d8655cb77b7629247e2744ea61e6be4f203a/xfa/fxfa/cxfa_ffpageview.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/1c21d8655cb77b7629247e2744ea61e6be4f203a/xfa/fxfa/cxfa_ffpageview.h
[add] https://pdfium.googlesource.com/pdfium/+/1c21d8655cb77b7629247e2744ea61e6be4f203a/testing/resources/javascript/xfa_specific/bug_1109108.evt
[add] https://pdfium.googlesource.com/pdfium/+/1c21d8655cb77b7629247e2744ea61e6be4f203a/testing/resources/javascript/xfa_specific/bug_1109108.in
[modify] https://pdfium.googlesource.com/pdfium/+/1c21d8655cb77b7629247e2744ea61e6be4f203a/fpdfsdk/cpdfsdk_formfillenvironment.cpp


### ts...@chromium.org (2020-07-24)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d91baed31069213e2c9b24bef3dfc3f93f4afbe4

commit d91baed31069213e2c9b24bef3dfc3f93f4afbe4
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Sat Jul 25 14:18:25 2020

Roll PDFium from 9e1fc05ef7a2 to df34e3c37407 (12 revisions)

https://pdfium.googlesource.com/pdfium.git/+log/9e1fc05ef7a2..df34e3c37407

2020-07-25 tsepez@chromium.org Make ownership of XML document slightly saner.
2020-07-24 tsepez@chromium.org Rename CFXA_DocumentParser to CXFA_DocumentBuilder.
2020-07-24 tsepez@chromium.org Make an XML-tree be the input to CFXA_DocumentParser().
2020-07-24 tsepez@chromium.org Retain layout items rather than raw widgets in CFXA_TabParam.
2020-07-24 tsepez@chromium.org Make CPDFXFA_Context::m_DocEnv into a pointer.
2020-07-24 tsepez@chromium.org Simplify ~CPDFXFA_Context(), part 2
2020-07-24 tsepez@chromium.org Slightly simplify ~CPDFXFA_Context().
2020-07-24 thestig@chromium.org Fix issue with FPDFText_GetLooseCharBox() and the tranformation matrix.
2020-07-24 thestig@chromium.org Add experimental APIs to get XFA data.
2020-07-23 tsepez@chromium.org Move fxv8_unittests.{cpp,h} and fxgc_unittests.{cpp,h} to testing/
2020-07-22 tsepez@chromium.org Make test environment setup consistent with gtest model.
2020-07-22 tsepez@chromium.org Move class EmbedderTestEnvironment to standalone V8TestEnvironment.

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/master/autoroll/README.md

Bug: chromium:1109108
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I58d04da158120610f2cc3dbc3c36eec5a169c806
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2318966
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#791452}

[modify] https://crrev.com/d91baed31069213e2c9b24bef3dfc3f93f4afbe4/DEPS


### [Deleted User] (2020-07-25)

[Empty comment from Monorail migration]

### ad...@google.com (2020-07-27)

[Empty comment from Monorail migration]

### ad...@google.com (2020-07-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-07-30)

Congratulations! The VRP panel has awarded $7,500 for this report.

### me...@gmail.com (2020-07-30)

Thanks :)

### ad...@google.com (2020-07-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@transcend.io (2020-10-31)

Why were the testcase files deleted for this bug?

### th...@chromium.org (2021-03-16)

re: https://crbug.com/chromium/1109108#c20 - not sure about the original test cases, but a minimized test case got added. See https://crbug.com/chromium/1109108#c10.

### am...@chromium.org (2021-03-29)

hi, merc.ouc@ - we consider attachments/pocs included with reports to be an integral part of the report, so I've un-deleted them. Thanks!

### is...@google.com (2021-03-29)

This issue was migrated from crbug.com/chromium/1109108?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052935)*
