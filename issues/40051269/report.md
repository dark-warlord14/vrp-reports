# pdfium (XFA): UAF in CXFA_Node::HasFlag

| Field | Value |
|-------|-------|
| **Issue ID** | [40051269](https://issues.chromium.org/issues/40051269) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | pd...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2020-01-17 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.130 Safari/537.36

Steps to reproduce the problem:
AddressSanitizer: heap-use-after-free on address 0x61100000701a at pc 0x55a82be2fd51 bp 0x7ffd304db380 sp 0x7ffd304db378
READ of size 2 at 0x61100000701a thread T0
SCARINESS: 42 (2-byte-read-heap-use-after-free)

    #0 0x55a82be2fd50 in CXFA_Node::HasFlag(XFA_NodeFlag) const xfa/fxfa/parser/cxfa_node.cpp:1745:7
    #1 0x55a82986c8bd in CXFA_Node::HasRemovedChildren() const xfa/fxfa/parser/cxfa_node.h:141:12
    #2 0x55a82bc4871e in CXFA_FFDocView::RunBindItems() xfa/fxfa/cxfa_ffdocview.cpp:632:15
    #3 0x55a82bc48401 in CXFA_FFDocView::InitLayout(CXFA_Node*) xfa/fxfa/cxfa_ffdocview.cpp:67:3
    #4 0x55a82bc49178 in CXFA_FFDocView::StartLayout() xfa/fxfa/cxfa_ffdocview.cpp:87:3
    #5 0x55a82befdd70 in CPDFXFA_Context::LoadXFADoc() fpdfsdk/fpdfxfa/cpdfxfa_context.cpp:163:22
    #6 0x55a82912dd56 in FPDF_LoadXFA fpdfsdk/fpdf_view.cpp:265:22
    #7 0x55a8290806f4 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:925:12
    #8 0x55a82907cfaa in main samples/pdfium_test.cc:1179:5

0x61100000701a is located 154 bytes inside of 224-byte region [0x611000006f80,0x611000007060)
freed by thread T0 here:
    #0 0x55a82907a89d in operator delete(void*) /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:160:3
    #1 0x55a82bdcba25 in CXFA_BindItems::~CXFA_BindItems() xfa/fxfa/parser/cxfa_binditems.cpp:33:33
    #2 0x55a82bdf9734 in std::__1::default_delete<CXFA_Node>::operator()(CXFA_Node*) const buildtools/third_party/libc++/trunk/include/memory:2378:5
    #3 0x55a82bdf96ba in std::__1::unique_ptr<CXFA_Node, std::__1::default_delete<CXFA_Node> >::reset(CXFA_Node*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #4 0x55a82bde681a in std::__1::unique_ptr<CXFA_Node, std::__1::default_delete<CXFA_Node> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2587:19
    #5 0x55a82bec038b in void std::__1::allocator_traits<std::__1::allocator<std::__1::__tree_node<std::__1::unique_ptr<CXFA_Node, std::__1::default_delete<CXFA_Node> >, void*> > >::__destroy<std::__1::unique_ptr<CXFA_Node, std::__1::default_delete<CXFA_Node> > >(std::__1::integral_constant<bool, false>, std::__1::allocator<std::__1::__tree_node<std::__1::unique_ptr<CXFA_Node, std::__1::default_delete<CXFA_Node> >, void*> >&, std::__1::unique_ptr<CXFA_Node, std::__1::default_delete<CXFA_Node> >*) buildtools/third_party/libc++/trunk/include/memory:1787:23
    #6 0x55a82bec0338 in void std::__1::allocator_traits<std::__1::allocator<std::__1::__tree_node<std::__1::unique_ptr<CXFA_Node, std::__1::default_delete<CXFA_Node> >, void*> > >::destroy<std::__1::unique_ptr<CXFA_Node, std::__1::default_delete<CXFA_Node> > >(std::__1::allocator<std::__1::__tree_node<std::__1::unique_ptr<CXFA_Node, std::__1::default_delete<CXFA_Node> >, void*> >&, std::__1::unique_ptr<CXFA_Node, std::__1::default_delete<CXFA_Node> >*) buildtools/third_party/libc++/trunk/include/memory:1619:14
    #7 0x55a82bec1c77 in std::__1::__tree<std::__1::unique_ptr<CXFA_Node, std::__1::default_delete<CXFA_Node> >, std::__1::less<std::__1::unique_ptr<CXFA_Node, std::__1::default_delete<CXFA_Node> > >, std::__1::allocator<std::__1::unique_ptr<CXFA_Node, std::__1::default_delete<CXFA_Node> > > >::erase(std::__1::__tree_const_iterator<std::__1::unique_ptr<CXFA_Node, std::__1::default_delete<CXFA_Node> >, std::__1::__tree_node<std::__1::unique_ptr<CXFA_Node, std::__1::default_delete<CXFA_Node> >, void*>*, long>) buildtools/third_party/libc++/trunk/include/__tree:2519:5
    #8 0x55a82bebfd87 in std::__1::set<std::__1::unique_ptr<CXFA_Node, std::__1::default_delete<CXFA_Node> >, std::__1::less<std::__1::unique_ptr<CXFA_Node, std::__1::default_delete<CXFA_Node> > >, std::__1::allocator<std::__1::unique_ptr<CXFA_Node, std::__1::default_delete<CXFA_Node> > > >::erase(std::__1::__tree_const_iterator<std::__1::unique_ptr<CXFA_Node, std::__1::default_delete<CXFA_Node> >, std::__1::__tree_node<std::__1::unique_ptr<CXFA_Node, std::__1::default_delete<CXFA_Node> >, void*>*, long>) buildtools/third_party/libc++/trunk/include/set:685:57
    #9 0x55a82bebfb2d in CXFA_NodeOwner::FreeOwnedNode(CXFA_Node*) xfa/fxfa/parser/cxfa_nodeowner.cpp:36:10
    #10 0x55a82986a2c4 in CJX_Object::ScriptAttributeString(CFXJSE_Value*, bool, XFA_Attribute) fxjs/xfa/cjx_object.cpp:1141:18
    #11 0x55a82bef561e in CJX_Object::ScriptAttributeString_static(CJX_Object*, CFXJSE_Value*, bool, XFA_Attribute) fxjs/xfa/cjx_object.h:157:3
    #12 0x55a8297f61c3 in CFXJSE_Engine::NormalPropertySetter(CFXJSE_Value*, fxcrt::StringViewTemplate<char>, CFXJSE_Value*) fxjs/xfa/cfxjse_engine.cpp:410:5
    #13 0x55a8297f0372 in (anonymous namespace)::DynPropSetterAdapter(FXJSE_CLASS_DESCRIPTOR const*, CFXJSE_Value*, fxcrt::StringViewTemplate<char>, CFXJSE_Value*) fxjs/xfa/cfxjse_class.cpp:178:7
    #14 0x55a8297eef73 in (anonymous namespace)::NamedPropertySetterCallback(v8::Local<v8::Name>, v8::Local<v8::Value>, v8::PropertyCallbackInfo<v8::Value> const&) fxjs/xfa/cfxjse_class.cpp:250:3
    #15 0x55a82a101033 in v8::internal::PropertyCallbackArguments::CallNamedSetter(v8::internal::Handle<v8::internal::InterceptorInfo>, v8::internal::Handle<v8::internal::Name>, v8::internal::Handle<v8::internal::Object>) v8/src/api/api-arguments-inl.h:231:3
    #16 0x55a82a61218d in v8::internal::(anonymous namespace)::SetPropertyWithInterceptorInternal(v8::internal::LookupIterator*, v8::internal::Handle<v8::internal::InterceptorInfo>, v8::Maybe<v8::internal::ShouldThrow>, v8::internal::Handle<v8::internal::Object>) v8/src/objects/js-objects.cc:1101:20
    #17 0x55a82a6261c8 in v8::internal::JSObject::SetPropertyWithInterceptor(v8::internal::LookupIterator*, v8::Maybe<v8::internal::ShouldThrow>, v8::internal::Handle<v8::internal::Object>) v8/src/objects/js-objects.cc:3031:10
    #18 0x55a82a77eb20 in v8::internal::Object::SetPropertyInternal(v8::internal::LookupIterator*, v8::internal::Handle<v8::internal::Object>, v8::Maybe<v8::internal::ShouldThrow>, v8::internal::StoreOrigin, bool*) v8/src/objects/objects.cc:2447:15
    #19 0x55a82a77e361 in v8::internal::Object::SetProperty(v8::internal::LookupIterator*, v8::internal::Handle<v8::internal::Object>, v8::internal::StoreOrigin, v8::Maybe<v8::internal::ShouldThrow>) v8/src/objects/objects.cc:2529:9
    #20 0x55a82ab7cdc1 in v8::internal::Runtime::SetObjectProperty(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, v8::internal::StoreOrigin, v8::Maybe<v8::internal::ShouldThrow>) v8/src/runtime/runtime-object.cc:430:3
    #21 0x55a8298d87a1 in v8::Object::Set(v8::Local<v8::Context>, v8::Local<v8::Value>, v8::Local<v8::Value>) v8/src/api/api.cc:4028:7
    #22 0x55a829843e40 in CFXJSE_Value::SetObjectProperty(fxcrt::StringViewTemplate<char>, CFXJSE_Value*) fxjs/xfa/cfxjse_value.cpp:149:54
    #23 0x55a829828061 in CFXJSE_FormCalcContext::assign_value_operator(CFXJSE_Value*, fxcrt::StringViewTemplate<char>, CFXJSE_Arguments&) fxjs/xfa/cfxjse_formcalc_context.cpp:4565:24
    #24 0x55a8297ededf in (anonymous namespace)::V8FunctionCallback_Wrapper(v8::FunctionCallbackInfo<v8::Value> const&) fxjs/xfa/cfxjse_class.cpp:47:3
    #25 0x55a829a18a1d in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api/api-arguments-inl.h:158:3
    #26 0x55a829a163f7 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:111:36
    #27 0x55a829a127a3 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:141:5
    #28 0x55a829a11cbe in v8::internal::Builtin_HandleApiCall(int, unsigned long*, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:129:1
    #29 0x55a82ba611f7 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit

previously allocated by thread T0 here:
    #0 0x55a82907a03d in operator new(unsigned long) /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:99:3
    #1 0x55a82be6f450 in pdfium::internal::MakeUniqueResult<CXFA_BindItems>::Scalar pdfium::MakeUnique<CXFA_BindItems, CXFA_Document*&, XFA_PacketType&>(CXFA_Document*&, XFA_PacketType&) third_party/base/ptr_util.h:56:29
    #2 0x55a82be4ce37 in CXFA_Node::Create(CXFA_Document*, XFA_Element, XFA_PacketType) xfa/fxfa/parser/cxfa_node.cpp:5876:14
    #3 0x55a82bde678e in CXFA_Document::CreateNode(XFA_PacketType, XFA_Element) xfa/fxfa/parser/cxfa_document.cpp:1376:23
    #4 0x55a82be2b392 in CXFA_Node::CloneTemplateToForm(bool) xfa/fxfa/parser/cxfa_node.cpp:1224:20
    #5 0x55a82986a250 in CJX_Object::ScriptAttributeString(CFXJSE_Value*, bool, XFA_Attribute) fxjs/xfa/cjx_object.cpp:1133:39
    #6 0x55a82bef561e in CJX_Object::ScriptAttributeString_static(CJX_Object*, CFXJSE_Value*, bool, XFA_Attribute) fxjs/xfa/cjx_object.h:157:3
    #7 0x55a8297f61c3 in CFXJSE_Engine::NormalPropertySetter(CFXJSE_Value*, fxcrt::StringViewTemplate<char>, CFXJSE_Value*) fxjs/xfa/cfxjse_engine.cpp:410:5
    #8 0x55a8297f0372 in (anonymous namespace)::DynPropSetterAdapter(FXJSE_CLASS_DESCRIPTOR const*, CFXJSE_Value*, fxcrt::StringViewTemplate<char>, CFXJSE_Value*) fxjs/xfa/cfxjse_class.cpp:178:7
    #9 0x55a8297eef73 in (anonymous namespace)::NamedPropertySetterCallback(v8::Local<v8::Name>, v8::Local<v8::Value>, v8::PropertyCallbackInfo<v8::Value> const&) fxjs/xfa/cfxjse_class.cpp:250:3
    #10 0x55a82a101033 in v8::internal::PropertyCallbackArguments::CallNamedSetter(v8::internal::Handle<v8::internal::InterceptorInfo>, v8::internal::Handle<v8::internal::Name>, v8::internal::Handle<v8::internal::Object>) v8/src/api/api-arguments-inl.h:231:3
    #11 0x55a82a61218d in v8::internal::(anonymous namespace)::SetPropertyWithInterceptorInternal(v8::internal::LookupIterator*, v8::internal::Handle<v8::internal::InterceptorInfo>, v8::Maybe<v8::internal::ShouldThrow>, v8::internal::Handle<v8::internal::Object>) v8/src/objects/js-objects.cc:1101:20
    #12 0x55a82a6261c8 in v8::internal::JSObject::SetPropertyWithInterceptor(v8::internal::LookupIterator*, v8::Maybe<v8::internal::ShouldThrow>, v8::internal::Handle<v8::internal::Object>) v8/src/objects/js-objects.cc:3031:10
    #13 0x55a82a77eb20 in v8::internal::Object::SetPropertyInternal(v8::internal::LookupIterator*, v8::internal::Handle<v8::internal::Object>, v8::Maybe<v8::internal::ShouldThrow>, v8::internal::StoreOrigin, bool*) v8/src/objects/objects.cc:2447:15
    #14 0x55a82a77e361 in v8::internal::Object::SetProperty(v8::internal::LookupIterator*, v8::internal::Handle<v8::internal::Object>, v8::internal::StoreOrigin, v8::Maybe<v8::internal::ShouldThrow>) v8/src/objects/objects.cc:2529:9
    #15 0x55a82ab7cdc1 in v8::internal::Runtime::SetObjectProperty(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, v8::internal::StoreOrigin, v8::Maybe<v8::internal::ShouldThrow>) v8/src/runtime/runtime-object.cc:430:3
    #16 0x55a8298d87a1 in v8::Object::Set(v8::Local<v8::Context>, v8::Local<v8::Value>, v8::Local<v8::Value>) v8/src/api/api.cc:4028:7
    #17 0x55a829843e40 in CFXJSE_Value::SetObjectProperty(fxcrt::StringViewTemplate<char>, CFXJSE_Value*) fxjs/xfa/cfxjse_value.cpp:149:54
    #18 0x55a829828061 in CFXJSE_FormCalcContext::assign_value_operator(CFXJSE_Value*, fxcrt::StringViewTemplate<char>, CFXJSE_Arguments&) fxjs/xfa/cfxjse_formcalc_context.cpp:4565:24
    #19 0x55a8297ededf in (anonymous namespace)::V8FunctionCallback_Wrapper(v8::FunctionCallbackInfo<v8::Value> const&) fxjs/xfa/cfxjse_class.cpp:47:3
    #20 0x55a829a18a1d in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api/api-arguments-inl.h:158:3
    #21 0x55a829a163f7 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:111:36
    #22 0x55a829a127a3 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:141:5
    #23 0x55a829a11cbe in v8::internal::Builtin_HandleApiCall(int, unsigned long*, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:129:1
    #24 0x55a82ba611f7 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit
    #25 0x55a82b9ec4aa in Builtins_InterpreterEntryTrampoline
    #26 0x55a82b9ec4aa in Builtins_InterpreterEntryTrampoline
    #27 0x55a82b9e5dbe in Builtins_ArgumentsAdaptorTrampoline
    #28 0x55a82b9ec4aa in Builtins_InterpreterEntryTrampoline
    #29 0x55a82b9e5dbe in Builtins_ArgumentsAdaptorTrampoline

Shadow bytes around the buggy address:
  0x0c227fff8db0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c227fff8dc0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c227fff8dd0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c227fff8de0: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
  0x0c227fff8df0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x0c227fff8e00: fd fd fd[fd]fd fd fd fd fd fd fd fd fa fa fa fa
  0x0c227fff8e10: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c227fff8e20: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c227fff8e30: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
  0x0c227fff8e40: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c227fff8e50: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

Chrome version: 78.0.3904.130  Channel: n/a
OS Version: 
Flash Version:

## Attachments

- [chromium-1042956.pdf](attachments/chromium-1042956.pdf) (application/pdf, 596 B)

## Timeline

### pd...@gmail.com (2020-01-17)

[Empty comment from Monorail migration]

### pd...@gmail.com (2020-01-17)

Note: Chrome doesn't use XFA.

### ct...@chromium.org (2020-01-17)

tsepez@ passing another pfdium XFA memory corruption your way.

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2020-01-17)

This is a bug in the node tree, which is strange because nodes nowdays come from an arena and are expected to live for the duration of the document (since they tend to be mostly static).  And you've found a way to hit the one place where we call FreeOwnedNode(), which seems like it is an anachronism.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-18)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/120629a8c3f9ff01ebcbbb6be4fee08e22d6121f

commit 120629a8c3f9ff01ebcbbb6be4fee08e22d6121f
Author: Tom Sepez <tsepez@chromium.org>
Date: Sat Jan 18 00:42:52 2020

Remove CXFA_NodeOwner::FreeOwnedNode().

Nodes live essentially in an "arena" and live for the duration of
the document. This appears to be an anachronism from earlier node
ownership models.

- use vector since lookup for removal not required.
- remove a no-op assignment near the call as well.

Bug: chromium:1042956
Change-Id: Ic1b4789766a6dc4b6e7a14ff289cc53090c93539
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/65330
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/120629a8c3f9ff01ebcbbb6be4fee08e22d6121f/xfa/fxfa/parser/cxfa_nodeowner.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/120629a8c3f9ff01ebcbbb6be4fee08e22d6121f/xfa/fxfa/parser/cxfa_nodeowner.h
[modify] https://pdfium.googlesource.com/pdfium/+/120629a8c3f9ff01ebcbbb6be4fee08e22d6121f/fxjs/xfa/cjx_object.cpp
[add] https://pdfium.googlesource.com/pdfium/+/120629a8c3f9ff01ebcbbb6be4fee08e22d6121f/testing/resources/javascript/xfa_specific/bug_1042956.pdf


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/63c8b9188e9fc9969e507324ca0b8f7f40d31d5e

commit 63c8b9188e9fc9969e507324ca0b8f7f40d31d5e
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Jan 22 00:08:27 2020

Roll src/third_party/pdfium fcb6cd6d22a2..c3e55aa23f88 (6 commits)

https://pdfium.googlesource.com/pdfium.git/+log/fcb6cd6d22a2..c3e55aa23f88

git log fcb6cd6d22a2..c3e55aa23f88 --date=short --first-parent --format='%ad %ae %s'
2020-01-21 thestig@chromium.org Rearrange CPDF_LinkExtract::ExtractLinks().
2020-01-21 thestig@chromium.org Remove |CPDF_LinkExtract::m_strPageText|.
2020-01-21 thestig@chromium.org Do some clean up in CXFA_FFDocView.
2020-01-21 thestig@chromium.org Make FSMatrixFromCFXMatrix() consistent with FSRectFFromCFXFloatRect().
2020-01-21 nigi@chromium.org [SkiaPaths] Make MatrixChanged() indicate changes of all its elements.
2020-01-18 tsepez@chromium.org Remove CXFA_NodeOwner::FreeOwnedNode().

Created with:
  gclient setdep -r src/third_party/pdfium@c3e55aa23f88

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:1042956
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I02ddf3838e21d9c838dfb1adeec7484c890abf21
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2013509
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#733812}

[modify] https://crrev.com/63c8b9188e9fc9969e507324ca0b8f7f40d31d5e/DEPS


### ts...@chromium.org (2020-01-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-23)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-27)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-01-30)

Congrats! The Panel decided to award $5,000 for this report!

### na...@google.com (2020-01-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-04-30)

This issue was migrated from crbug.com/chromium/1042956?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051269)*
