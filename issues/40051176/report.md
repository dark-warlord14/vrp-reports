# heap use-after-free in CFDE_TextEditEngine::Insert

| Field | Value |
|-------|-------|
| **Issue ID** | [40051176](https://issues.chromium.org/issues/40051176) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux |
| **Reporter** | me...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2020-01-09 |
| **Bounty** | $7,500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36

Steps to reproduce the problem:
1. build pdfium_test with XFA enable
2. ./pdfium_test uaf.pdf
3.

What is the expected behavior?

What went wrong?
In function CFDE_TextEditEngine::Insert in xfa/fde/cfde_texteditengine.cpp 

We can call js in line 283 delegate_->OnTextWillChange(&change); and free |this|, then it will be used in line 295 `text_length_` ==> UAF

 265 void CFDE_TextEditEngine::Insert(size_t idx,
 266                                  const WideString& request_text,
 267                                  RecordOperation add_operation) {
 268   WideString text = request_text;
 269   if (text.GetLength() == 0)
 270     return;
 271 
 272   idx = std::min(idx, text_length_);
 273 
 274   TextChange change;
 275   change.selection_start = idx;
 276   change.selection_end = idx;
 277   change.text = text;
 278   change.previous_text = GetText();
 279   change.cancelled = false;
 280 
 281   if (delegate_ && (add_operation != RecordOperation::kSkipRecord &&
 282                     add_operation != RecordOperation::kSkipNotify)) {
 283     delegate_->OnTextWillChange(&change); // call HJS
 284     if (change.cancelled)
 285       return;
 286 
 287     text = change.text;
 288     idx = change.selection_start;
 289 
 290     // Delegate extended the selection, so delete it before we insert.
 291     if (change.selection_end != change.selection_start)
 292       DeleteSelectedText(RecordOperation::kSkipRecord);
 293 
 294     // Delegate may have changed text entirely, recheck.
 295     idx = std::min(idx, text_length_);  // Use here. withtou ASAN ,it will crash in line 355 too.
 296   }
.
.
.
 354   if (add_operation == RecordOperation::kInsertRecord) {
 355     AddOperationRecord(
 356         pdfium::MakeUnique<InsertOperation>(this, gap_position_, text));
 357   }

ASAN log:

=================================================================
==3352==ERROR: AddressSanitizer: heap-use-after-free on address 0x615000013a58 at pc 0x565556886469 bp 0x7ffe61d946f0 sp 0x7ffe61d946e8
READ of size 8 at 0x615000013a58 thread T0
    #0 0x565556886468 in std::__1::__less<unsigned long, unsigned long>::operator()(unsigned long const&, unsigned long const&) const buildtools/third_party/libc++/trunk/include/algorithm:715:67
    #1 0x565556886fa4 in unsigned long const& std::__1::min<unsigned long, std::__1::__less<unsigned long, unsigned long> >(unsigned long const&, unsigned long const&, std::__1::__less<unsigned long, unsigned long>) buildtools/third_party/libc++/trunk/include/algorithm:2525:12
    #2 0x565556886e2c in unsigned long const& std::__1::min<unsigned long>(unsigned long const&, unsigned long const&) buildtools/third_party/libc++/trunk/include/algorithm:2534:12
    #3 0x56555b2df598 in CFDE_TextEditEngine::Insert(unsigned long, fxcrt::WideString const&, CFDE_TextEditEngine::RecordOperation) xfa/fde/cfde_texteditengine.cpp:295:11
    #4 0x56555b397c75 in CFWL_Edit::SetText(fxcrt::WideString const&) xfa/fwl/cfwl_edit.cpp:167:18
    #5 0x56555b37e964 in CFWL_ComboBox::SetEditText(fxcrt::WideString const&) xfa/fwl/cfwl_combobox.cpp:180:12
    #6 0x56555b1b3493 in CXFA_FFComboBox::UpdateFWLData() xfa/fxfa/cxfa_ffcombobox.cpp:203:16
    #7 0x56555b1c76f2 in CXFA_FFDocView::UpdateUIDisplay(CXFA_Node*, CXFA_FFWidget*) xfa/fxfa/cxfa_ffdocview.cpp:209:15
    #8 0x56555b1f78c8 in CXFA_FFNotify::OnValueChanged(CXFA_Node*, XFA_Attribute, CXFA_Node*, CXFA_Node*) xfa/fxfa/cxfa_ffnotify.cpp:407:31
    #9 0x56555b534b6b in CXFA_Node::SendAttributeChangeMessage(XFA_Attribute, bool) xfa/fxfa/parser/cxfa_node.cpp:2165:20
    #10 0x565557d179bc in CJX_Object::OnChanged(XFA_Attribute, bool, bool) fxjs/xfa/cjx_object.cpp:1065:29
    #11 0x565557d1904c in CJX_Object::SetAttributeValue(fxcrt::WideString const&, fxcrt::WideString const&, bool, bool) fxjs/xfa/cjx_object.cpp:493:3
    #12 0x565557d1a873 in CJX_Object::SetContent(fxcrt::WideString const&, fxcrt::WideString const&, bool, bool, bool) fxjs/xfa/cjx_object.cpp:693:3
    #13 0x565557d1a5f4 in CJX_Object::SetContent(fxcrt::WideString const&, fxcrt::WideString const&, bool, bool, bool) fxjs/xfa/cjx_object.cpp:655:40
    #14 0x565557d1a110 in CJX_Object::SetContent(fxcrt::WideString const&, fxcrt::WideString const&, bool, bool, bool) fxjs/xfa/cjx_object.cpp:614:34
    #15 0x565557d1a37b in CJX_Object::SetContent(fxcrt::WideString const&, fxcrt::WideString const&, bool, bool, bool) fxjs/xfa/cjx_object.cpp:623:37
    #16 0x56555b534eed in CXFA_Node::SyncValue(fxcrt::WideString const&, bool) xfa/fxfa/parser/cxfa_node.cpp:2200:15
    #17 0x56555b537893 in CXFA_Node::SetValue(XFA_VALUEPICTURE, fxcrt::WideString const&) xfa/fxfa/parser/cxfa_node.cpp:4682:5
    #18 0x56555b5372be in CXFA_Node::ProcessCalculate(CXFA_FFDocView*) xfa/fxfa/parser/cxfa_node.cpp:2449:5
    #19 0x56555b1ca1d8 in CXFA_FFDocView::RunCalculateRecursive(unsigned long) xfa/fxfa/cxfa_ffdocview.cpp:555:15
    #20 0x56555b1ca21e in CXFA_FFDocView::RunCalculateRecursive(unsigned long) xfa/fxfa/cxfa_ffdocview.cpp:560:13
    #21 0x56555b1c5fbc in CXFA_FFDocView::RunCalculateWidgets() xfa/fxfa/cxfa_ffdocview.cpp:570:5
    #22 0x56555b1c5cb7 in CXFA_FFDocView::StopLayout() xfa/fxfa/cxfa_ffdocview.cpp:133:3
    #23 0x56555b668202 in CPDFXFA_Context::LoadXFADoc() fpdfsdk/fpdfxfa/cpdfxfa_context.cpp:170:18
    #24 0x565556a2d2c7 in FPDF_LoadXFA fpdfsdk/fpdf_view.cpp:262:22
    #25 0x56555687e82b in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:924:12
    #26 0x565556879450 in main samples/pdfium_test.cc:1170:5
    #27 0x7ff638219b96 in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x21b96)

0x615000013a58 is located 344 bytes inside of 480-byte region [0x615000013900,0x615000013ae0)
freed by thread T0 here:
    #0 0x5655568762fd in operator delete(void*) /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:160:3
    #1 0x56555b2dd457 in CFDE_TextEditEngine::~CFDE_TextEditEngine() xfa/fde/cfde_texteditengine.cpp:172:45
    #2 0x56555b3a893f in std::__1::default_delete<CFDE_TextEditEngine>::operator()(CFDE_TextEditEngine*) const buildtools/third_party/libc++/trunk/include/memory:2378:5
    #3 0x56555b3a8878 in std::__1::unique_ptr<CFDE_TextEditEngine, std::__1::default_delete<CFDE_TextEditEngine> >::reset(CFDE_TextEditEngine*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #4 0x56555b3a6418 in std::__1::unique_ptr<CFDE_TextEditEngine, std::__1::default_delete<CFDE_TextEditEngine> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2587:19
    #5 0x56555b390326 in CFWL_Edit::~CFWL_Edit() xfa/fwl/cfwl_edit.cpp:60:1
    #6 0x56555b3837c7 in CFWL_ComboEdit::~CFWL_ComboEdit() xfa/fwl/cfwl_comboedit.cpp:23:33
    #7 0x56555b382d3a in std::__1::default_delete<CFWL_ComboEdit>::operator()(CFWL_ComboEdit*) const buildtools/third_party/libc++/trunk/include/memory:2378:5
    #8 0x56555b382cc8 in std::__1::unique_ptr<CFWL_ComboEdit, std::__1::default_delete<CFWL_ComboEdit> >::reset(CFWL_ComboEdit*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #9 0x56555b382058 in std::__1::unique_ptr<CFWL_ComboEdit, std::__1::default_delete<CFWL_ComboEdit> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2587:19
    #10 0x56555b37b88f in CFWL_ComboBox::~CFWL_ComboBox() xfa/fwl/cfwl_combobox.cpp:38:31
    #11 0x56555b37b8cb in CFWL_ComboBox::~CFWL_ComboBox() xfa/fwl/cfwl_combobox.cpp:38:31
    #12 0x56555b1ab80f in std::__1::default_delete<CFWL_Widget>::operator()(CFWL_Widget*) const buildtools/third_party/libc++/trunk/include/memory:2378:5
    #13 0x56555b1ab748 in std::__1::unique_ptr<CFWL_Widget, std::__1::default_delete<CFWL_Widget> >::reset(CFWL_Widget*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #14 0x56555b1aa2f8 in std::__1::unique_ptr<CFWL_Widget, std::__1::default_delete<CFWL_Widget> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2587:19
    #15 0x56555b1d98ec in CXFA_FFField::~CXFA_FFField() xfa/fxfa/cxfa_fffield.cpp:50:29
    #16 0x56555b1d93c7 in CXFA_FFDropDown::~CXFA_FFDropDown() xfa/fxfa/cxfa_ffdropdown.cpp:11:35
    #17 0x56555b1b1cba in CXFA_FFComboBox::~CXFA_FFComboBox() xfa/fxfa/cxfa_ffcombobox.cpp:34:35
    #18 0x56555b1b1d0b in CXFA_FFComboBox::~CXFA_FFComboBox() xfa/fxfa/cxfa_ffcombobox.cpp:34:35
    #19 0x56555b202e8f in std::__1::default_delete<CXFA_FFWidget>::operator()(CXFA_FFWidget*) const buildtools/third_party/libc++/trunk/include/memory:2378:5
    #20 0x56555b202dc8 in std::__1::unique_ptr<CXFA_FFWidget, std::__1::default_delete<CXFA_FFWidget> >::reset(CXFA_FFWidget*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #21 0x56555b1fb248 in std::__1::unique_ptr<CXFA_FFWidget, std::__1::default_delete<CXFA_FFWidget> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2587:19
    #22 0x56555b4273e6 in CXFA_ContentLayoutItem::~CXFA_ContentLayoutItem() xfa/fxfa/layout/cxfa_contentlayoutitem.cpp:26:1
    #23 0x56555b4274fb in CXFA_ContentLayoutItem::~CXFA_ContentLayoutItem() xfa/fxfa/layout/cxfa_contentlayoutitem.cpp:24:51
    #24 0x565557cfe91d in fxcrt::RetainedTreeNode<CXFA_LayoutItem>::Release() core/fxcrt/retained_tree_node.h:71:7
    #25 0x565557cfe7ab in fxcrt::ReleaseDeleter<CXFA_LayoutItem>::operator()(CXFA_LayoutItem*) const core/fxcrt/retain_ptr.h:20:47
    #26 0x565557cfe748 in std::__1::unique_ptr<CXFA_LayoutItem, fxcrt::ReleaseDeleter<CXFA_LayoutItem> >::reset(CXFA_LayoutItem*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #27 0x565557cffc7c in fxcrt::RetainPtr<CXFA_LayoutItem>::operator=(fxcrt::RetainPtr<CXFA_LayoutItem>&&) core/fxcrt/retain_ptr.h:72:12
    #28 0x56555b45e20a in XFA_ReleaseLayoutItem(fxcrt::RetainPtr<CXFA_LayoutItem> const&) xfa/fxfa/layout/cxfa_layoutitem.cpp:25:11
    #29 0x56555b45e1f5 in XFA_ReleaseLayoutItem(fxcrt::RetainPtr<CXFA_LayoutItem> const&) xfa/fxfa/layout/cxfa_layoutitem.cpp:24:5

previously allocated by thread T0 here:
    #0 0x565556875a9d in operator new(unsigned long) /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:99:3
    #1 0x56555b3a5ff6 in pdfium::internal::MakeUniqueResult<CFDE_TextEditEngine>::Scalar pdfium::MakeUnique<CFDE_TextEditEngine>() third_party/base/ptr_util.h:56:29
    #2 0x56555b390077 in CFWL_Edit::CFWL_Edit(CFWL_App const*, std::__1::unique_ptr<CFWL_WidgetProperties, std::__1::default_delete<CFWL_WidgetProperties> >, CFWL_Widget*) xfa/fwl/cfwl_edit.cpp:52:21
    #3 0x56555b3836c0 in CFWL_ComboEdit::CFWL_ComboEdit(CFWL_App const*, std::__1::unique_ptr<CFWL_WidgetProperties, std::__1::default_delete<CFWL_WidgetProperties> >, CFWL_Widget*) xfa/fwl/cfwl_comboedit.cpp:20:7
    #4 0x56555b382926 in pdfium::internal::MakeUniqueResult<CFWL_ComboEdit>::Scalar pdfium::MakeUnique<CFWL_ComboEdit, CFWL_App const*, std::__1::unique_ptr<CFWL_WidgetProperties, std::__1::default_delete<CFWL_WidgetProperties> >, CFWL_ComboBox*>(CFWL_App const*&&, std::__1::unique_ptr<CFWL_WidgetProperties, std::__1::default_delete<CFWL_WidgetProperties> >&&, CFWL_ComboBox*&&) third_party/base/ptr_util.h:56:33
    #5 0x56555b37b726 in CFWL_ComboBox::InitComboEdit() xfa/fwl/cfwl_combobox.cpp:424:13
    #6 0x56555b37afdf in CFWL_ComboBox::CFWL_ComboBox(CFWL_App const*) xfa/fwl/cfwl_combobox.cpp:35:3
    #7 0x56555b1b5ad8 in pdfium::internal::MakeUniqueResult<CFWL_ComboBox>::Scalar pdfium::MakeUnique<CFWL_ComboBox, CFWL_App const*>(CFWL_App const*&&) third_party/base/ptr_util.h:56:33
    #8 0x56555b1b279f in CXFA_FFComboBox::LoadWidget() xfa/fxfa/cxfa_ffcombobox.cpp:49:15
    #9 0x56555b1c8a92 in CXFA_FFDocView::SetFocus(CXFA_FFWidget*) xfa/fxfa/cxfa_ffdocview.cpp:315:22
    #10 0x56555b1c65fa in CXFA_FFDocView::SetFocusNode(CXFA_Node*) xfa/fxfa/cxfa_ffdocview.cpp:334:8
    #11 0x56555b1f74a8 in CXFA_FFNotify::SetFocusWidgetNode(CXFA_Node*) xfa/fxfa/cxfa_ffnotify.cpp:320:13
    #12 0x565557cf05c1 in CJX_HostPseudoModel::setFocus(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_hostpseudomodel.cpp:447:12
    #13 0x565557cf37b2 in CJX_HostPseudoModel::setFocus_static(CJX_Object*, CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_hostpseudomodel.h:39:3
    #14 0x565557d10800 in CJX_Object::RunMethod(fxcrt::WideString const&, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_object.cpp:177:10
    #15 0x565557c3fbaf in CFXJSE_Engine::NormalMethodCall(v8::FunctionCallbackInfo<v8::Value> const&, fxcrt::WideString const&) fxjs/xfa/cfxjse_engine.cpp:483:31
    #16 0x565557c2a361 in (anonymous namespace)::DynPropGetterAdapter_MethodCallback(v8::FunctionCallbackInfo<v8::Value> const&) fxjs/xfa/cfxjse_class.cpp:112:7
    #17 0x565557fe774d in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api/api-arguments-inl.h:158:3
    #18 0x565557fe3c9e in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:111:36
    #19 0x565557fdff55 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:141:5
    #20 0x565557fdf18f in v8::internal::Builtin_HandleApiCall(int, unsigned long*, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:129:1
    #21 0x56555abe929e in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit (/home/krace/tool/pdfium/out/Debug/pdfium_test+0x608529e)
    #22 0x56555a99ea4a in Builtins_InterpreterEntryTrampoline (/home/krace/tool/pdfium/out/Debug/pdfium_test+0x5e3aa4a)
    #23 0x56555a986a9e in Builtins_ArgumentsAdaptorTrampoline (/home/krace/tool/pdfium/out/Debug/pdfium_test+0x5e22a9e)
    #24 0x56555a99ea4a in Builtins_InterpreterEntryTrampoline (/home/krace/tool/pdfium/out/Debug/pdfium_test+0x5e3aa4a)
    #25 0x56555a986a9e in Builtins_ArgumentsAdaptorTrampoline (/home/krace/tool/pdfium/out/Debug/pdfium_test+0x5e22a9e)
    #26 0x56555a994eb9 in Builtins_JSEntryTrampoline (/home/krace/tool/pdfium/out/Debug/pdfium_test+0x5e30eb9)
    #27 0x56555a994c97 in Builtins_JSEntry (/home/krace/tool/pdfium/out/Debug/pdfium_test+0x5e30c97)
    #28 0x5655583f591e in Call v8/src/execution/simulator.h:142:12
    #29 0x5655583f591e in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:271:33
    #30 0x5655583f4ad5 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution/execution.cc:365:10

SUMMARY: AddressSanitizer: heap-use-after-free buildtools/third_party/libc++/trunk/include/algorithm:715:67 in std::__1::__less<unsigned long, unsigned long>::operator()(unsigned long const&, unsigned long const&) const
Shadow bytes around the buggy address:
  0x0c2a7fffa6f0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a7fffa700: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a7fffa710: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2a7fffa720: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a7fffa730: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x0c2a7fffa740: fd fd fd fd fd fd fd fd fd fd fd[fd]fd fd fd fd
  0x0c2a7fffa750: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa
  0x0c2a7fffa760: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2a7fffa770: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a7fffa780: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a7fffa790: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==3352==ABORTING

Did this work before? N/A 

Chrome version: 78.0.3904.70  Channel: n/a
OS Version: ubuntu
Flash Version:

## Attachments

- [uaf.pdf](attachments/uaf.pdf) (application/pdf, 2.1 KB)

## Timeline

### cl...@chromium.org (2020-01-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5569032319205376.

### cl...@chromium.org (2020-01-09)

Automatically adding ccs based on OWNERS file / target commit history.

If this is incorrect, please add the ClusterFuzz-Wrong label.

### cl...@chromium.org (2020-01-09)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Plugins>PDF]

### cl...@chromium.org (2020-01-09)

Automatically assigning owner based on suspected regression changelist https://pdfium.googlesource.com/pdfium/+/5131f71d63052ca851f6a78830d2da564be50f44 (Observe CXFA_FFWidget across UpdateFWLData() calls.).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### cl...@chromium.org (2020-01-09)

Detailed Report: https://clusterfuzz.com/testcase?key=5569032319205376

Fuzzing Engine: libFuzzer
Fuzz Target: pdfium_xfa_fuzzer
Job Type: libfuzzer_chrome_asan
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x615000012658
Crash State:
  CFDE_TextEditEngine::Insert
  CFWL_Edit::SetText
  CFWL_ComboBox::SetEditText
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=729241:729242

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5569032319205376

See https://chromium.googlesource.com/chromium/src/+/master/testing/libfuzzer/reproducing.md for instructions on reproducing this bug locally.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### sh...@chromium.org (2020-01-10)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2020-01-11)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2020-01-11)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2020-01-13)

[Empty comment from Monorail migration]

### ts...@chromium.org (2020-01-16)

[Empty comment from Monorail migration]

### me...@gmail.com (2020-01-17)

Hello, any patch for this one ?

### me...@gmail.com (2020-01-28)

ping...

### th...@chromium.org (2020-01-29)

With enough checks to make sure every object in the stack trace is dead and bail out, I can get the POC to become UAF-free. It works but it's ugly and fragile.

I suspect the underlying issue is we are not handling re-entrancy correctly. Maybe we should get back to solving https://crbug.com/chromium/877165.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-19)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/d15d718e8d5e8d664454625f2b0c51ed71a2b10e

commit d15d718e8d5e8d664454625f2b0c51ed71a2b10e
Author: Tom Sepez <tsepez@chromium.org>
Date: Wed Feb 19 22:12:51 2020

Protect owning layout item in all UpdateFWLData() overrides.

Also observe |this| in CFWL_DateTimePicker::SetEditText() and
ProcessSelChanged().

Bug: chromium:1053617,chromium:1052786,chromium:1040329
Change-Id: Icb4afcd7e5432787668355102b3b36faf5572894
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/66630
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/d15d718e8d5e8d664454625f2b0c51ed71a2b10e/xfa/fxfa/cxfa_fflistbox.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/d15d718e8d5e8d664454625f2b0c51ed71a2b10e/xfa/fxfa/cxfa_ffcheckbutton.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/d15d718e8d5e8d664454625f2b0c51ed71a2b10e/xfa/fwl/cfwl_datetimepicker.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/d15d718e8d5e8d664454625f2b0c51ed71a2b10e/xfa/fxfa/cxfa_fftextedit.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/d15d718e8d5e8d664454625f2b0c51ed71a2b10e/xfa/fxfa/cxfa_ffdatetimeedit.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/d15d718e8d5e8d664454625f2b0c51ed71a2b10e/xfa/fxfa/cxfa_ffcombobox.cpp


### ts...@chromium.org (2020-02-19)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/eca24f9ecc907c4bfd7a4a2ce36b4ac863155066

commit eca24f9ecc907c4bfd7a4a2ce36b4ac863155066
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Feb 20 00:35:24 2020

Roll src/third_party/pdfium 1217cd17daba..d15d718e8d5e (5 commits)

https://pdfium.googlesource.com/pdfium.git/+log/1217cd17daba..d15d718e8d5e

git log 1217cd17daba..d15d718e8d5e --date=short --first-parent --format='%ad %ae %s'
2020-02-19 tsepez@chromium.org Protect owning layout item in all UpdateFWLData() overrides.
2020-02-19 nigi@chromium.org Roll third_party/binutils/ 01aa7745b..ffd1fdb90 (1 commit)
2020-02-19 nigi@chromium.org Roll tools/memory/ f7b00daf4..89552acb6 (1 commit)
2020-02-19 nigi@chromium.org Roll third_party/instrumented_libraries/ 4dca59c6a..bb3f1802c (1 commit)
2020-02-19 tsepez@chromium.org Pass spans to UTF8Decode() in cfx_seekablestreamproxy.cpp

Created with:
  gclient setdep -r src/third_party/pdfium@d15d718e8d5e

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:1040329,chromium:1052786,chromium:1053617
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I38b0499a67c4f681302621455ddd7dca9011c4ea
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2065391
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#742885}

[modify] https://crrev.com/eca24f9ecc907c4bfd7a4a2ce36b4ac863155066/DEPS


### [Deleted User] (2020-02-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-02-20)

ClusterFuzz testcase 5569032319205376 is verified as fixed in https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=742877:742902

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### na...@google.com (2020-02-24)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-02-27)

Congrats the Panel decided to award $7,500 for this report!

### me...@gmail.com (2020-02-27)

Tanks :)

### na...@google.com (2020-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1040329?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1042176]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051176)*
