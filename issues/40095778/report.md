# Security: pdfium XFA CJX_Object::SetContent Use After Free

| Field | Value |
|-------|-------|
| **Issue ID** | [40095778](https://issues.chromium.org/issues/40095778) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-07-20 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

Bug Use After Free in CJX\_Object::SetContent function  

Root cause:  

We could trigger callback to reallocate binding\_nodes\_ which contain binding items

xfa/fxfa/parser/cxfa\_node.h

```
std::vector<CXFA_Node\*> binding_nodes_;  // Raw, node tree cleanup order.  

```

fxjs/xfa/cjx\_object.cpp

```
          for (auto\* pArrayNode : \*(pBind->GetBindItems())) {  
            if (pArrayNode != ToNode(GetXFAObject())) {  
              pArrayNode->JSObject()->SetContent(wsContent, wsContent, bNotify,  
                                                 bScriptModify, false);  
            }  
          }  

```

**VERSION**  

Operating System: Ubuntu 16.04

**REPRODUCTION CASE**

Build pdfium with XFA enabled, ASAN enabled  

Run ./pdfium\_test bug\_38.pdf

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

=================================================================  

==527==ERROR: AddressSanitizer: heap-use-after-free on address 0x6060000ceba8 at pc 0x555b98588cb0 bp 0x7ffcaf61b990 sp 0x7ffcaf61b988  

READ of size 8 at 0x6060000ceba8 thread T0  

#0 0x555b98588caf in CJX\_Object::SetContent(fxcrt::WideString const&, fxcrt::WideString const&, bool, bool, bool) fxjs/xfa/cjx\_object.cpp:621:31  

#1 0x555b9b695430 in CXFA\_Node::SyncValue(fxcrt::WideString const&, bool) xfa/fxfa/parser/cxfa\_node.cpp:2151:15  

#2 0x555b9b697de7 in CXFA\_Node::SetValue(XFA\_VALUEPICTURE, fxcrt::WideString const&) xfa/fxfa/parser/cxfa\_node.cpp:4658:5  

#3 0x555b9b697810 in CXFA\_Node::ProcessCalculate(CXFA\_FFDocView\*) xfa/fxfa/parser/cxfa\_node.cpp:2400:5  

#4 0x555b9b800aa8 in CXFA\_FFDocView::RunCalculateRecursive(unsigned long) xfa/fxfa/cxfa\_ffdocview.cpp:537:15  

#5 0x555b9b800aee in CXFA\_FFDocView::RunCalculateRecursive(unsigned long) xfa/fxfa/cxfa\_ffdocview.cpp:542:13  

#6 0x555b9b800aee in CXFA\_FFDocView::RunCalculateRecursive(unsigned long) xfa/fxfa/cxfa\_ffdocview.cpp:542:13  

#7 0x555b9b800aee in CXFA\_FFDocView::RunCalculateRecursive(unsigned long) xfa/fxfa/cxfa\_ffdocview.cpp:542:13  

#8 0x555b9b800aee in CXFA\_FFDocView::RunCalculateRecursive(unsigned long) xfa/fxfa/cxfa\_ffdocview.cpp:542:13  

#9 0x555b9b800aee in CXFA\_FFDocView::RunCalculateRecursive(unsigned long) xfa/fxfa/cxfa\_ffdocview.cpp:542:13  

#10 0x555b9b800aee in CXFA\_FFDocView::RunCalculateRecursive(unsigned long) xfa/fxfa/cxfa\_ffdocview.cpp:542:13  

#11 0x555b9b800aee in CXFA\_FFDocView::RunCalculateRecursive(unsigned long) xfa/fxfa/cxfa\_ffdocview.cpp:542:13  

#12 0x555b9b800aee in CXFA\_FFDocView::RunCalculateRecursive(unsigned long) xfa/fxfa/cxfa\_ffdocview.cpp:542:13  

#13 0x555b9b800aee in CXFA\_FFDocView::RunCalculateRecursive(unsigned long) xfa/fxfa/cxfa\_ffdocview.cpp:542:13  

#14 0x555b9b800aee in CXFA\_FFDocView::RunCalculateRecursive(unsigned long) xfa/fxfa/cxfa\_ffdocview.cpp:542:13  

#15 0x555b9b7fceec in CXFA\_FFDocView::RunCalculateWidgets() xfa/fxfa/cxfa\_ffdocview.cpp:552:5  

#16 0x555b9b7fcbe7 in CXFA\_FFDocView::StopLayout() xfa/fxfa/cxfa\_ffdocview.cpp:133:3  

#17 0x555b9b8fcbe9 in CPDFXFA\_Context::LoadXFADoc() fpdfsdk/fpdfxfa/cpdfxfa\_context.cpp:132:18  

#18 0x555b9729c30e in FPDF\_LoadXFA fpdfsdk/fpdf\_view.cpp:270:32  

#19 0x555b97127842 in (anonymous namespace)::RenderPdf(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, char const\*, unsigned long, (anonymous namespace)::Options const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) samples/pdfium\_test.cc:841:12  

#20 0x555b97122f01 in main samples/pdfium\_test.cc:1068:5  

#21 0x7f53775bf82f in \_\_libc\_start\_main (/lib/x86\_64-linux-gnu/libc.so.6+0x2082f)

0x6060000ceba8 is located 8 bytes inside of 64-byte region [0x6060000ceba0,0x6060000cebe0)  

freed by thread T0 here:  

#0 0x555b9712014d in operator delete(void\*) /b/swarming/w/ir/k/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cc:166:3  

#1 0x555b97132d14 in std::\_\_1::\_DeallocateCaller::\_\_do\_call(void\*) buildtools/third\_party/libc++/trunk/include/new:319:12  

#2 0x555b97132cf8 in std::\_\_1::\_DeallocateCaller::\_\_do\_deallocate\_handle\_size(void\*, unsigned long) buildtools/third\_party/libc++/trunk/include/new:277:12  

#3 0x555b97132cd0 in std::\_\_1::\_DeallocateCaller::\_\_do\_deallocate\_handle\_size\_align(void\*, unsigned long, unsigned long) buildtools/third\_party/libc++/trunk/include/new:247:12  

#4 0x555b97132ca4 in std::\_\_1::\_\_libcpp\_deallocate(void\*, unsigned long, unsigned long) buildtools/third\_party/libc++/trunk/include/new:325:3  

#5 0x555b984c377f in std::\_\_1::allocator<CXFA\_Node\*>::deallocate(CXFA\_Node\*\*, unsigned long) buildtools/third\_party/libc++/trunk/include/memory:1816:10  

#6 0x555b984c3494 in std::\_\_1::allocator\_traits<std::\_\_1::allocator<CXFA\_Node\*> >::deallocate(std::\_\_1::allocator<CXFA\_Node\*>&, CXFA\_Node\*\*, unsigned long) buildtools/third\_party/libc++/trunk/include/memory:1554:14  

#7 0x555b984c9855 in std::\_\_1::\_\_split\_buffer<CXFA\_Node\*, std::\_\_1::allocator<CXFA\_Node\*>&>::~\_\_split\_buffer() buildtools/third\_party/libc++/trunk/include/\_\_split\_buffer:343:9  

#8 0x555b9b70b52b in void std::\_\_1::vector<CXFA\_Node\*, std::\_\_1::allocator<CXFA\_Node\*> >::\_\_emplace\_back\_slow\_path<CXFA\_Node\*&>(CXFA\_Node\*&) buildtools/third\_party/libc++/trunk/include/vector:1672:1  

#9 0x555b9b6c3782 in void std::\_\_1::vector<CXFA\_Node\*, std::\_\_1::allocator<CXFA\_Node\*> >::emplace\_back<CXFA\_Node\*&>(CXFA\_Node\*&) buildtools/third\_party/libc++/trunk/include/vector:1694:9  

#10 0x555b9b689d44 in CXFA\_Node::AddBindItem(CXFA\_Node\*) xfa/fxfa/parser/cxfa\_node.cpp:1218:22  

#11 0x555b9b623c24 in (anonymous namespace)::CreateDataBinding(CXFA\_Node\*, CXFA\_Node\*, bool) xfa/fxfa/parser/cxfa\_document.cpp:491:14  

#12 0x555b9b62128a in (anonymous namespace)::CopyContainer\_Field(CXFA\_Document\*, CXFA\_Node\*, CXFA\_Node\*, CXFA\_Node\*, bool, bool) xfa/fxfa/parser/cxfa\_document.cpp:816:7  

#13 0x555b9b61e0c9 in CXFA\_Document::DataMerge\_CopyContainer(CXFA\_Node\*, CXFA\_Node\*, CXFA\_Node\*, bool, bool, bool) xfa/fxfa/parser/cxfa\_document.cpp:1590:14  

#14 0x555b9b623310 in CXFA\_Document::DoDataMerge() xfa/fxfa/parser/cxfa\_document.cpp:1750:7  

#15 0x555b9b625b16 in CXFA\_Document::DoDataRemerge(bool) xfa/fxfa/parser/cxfa\_document.cpp:1805:5  

#16 0x555b985afb36 in CJX\_Template::remerge(CFX\_V8\*, std::\_\_1::vector<v8::Local[v8::Value](javascript:void(0);), std::\_\_1::allocator<v8::Local[v8::Value](javascript:void(0);) > > const&) fxjs/xfa/cjx\_template.cpp:50:18  

#17 0x555b985b0e0b in CJX\_Template::remerge\_static(CJX\_Object\*, CFX\_V8\*, std::\_\_1::vector<v8::Local[v8::Value](javascript:void(0);), std::\_\_1::allocator<v8::Local[v8::Value](javascript:void(0);) > > const&) fxjs/xfa/cjx\_template.h:31:3  

#18 0x555b9857f1e5 in CJX\_Object::RunMethod(fxcrt::WideString const&, std::\_\_1::vector<v8::Local[v8::Value](javascript:void(0);), std::\_\_1::allocator<v8::Local[v8::Value](javascript:void(0);) > > const&) fxjs/xfa/cjx\_object.cpp:177:10  

#19 0x555b984b1441 in CFXJSE\_Engine::NormalMethodCall(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&, fxcrt::WideString const&) fxjs/xfa/cfxjse\_engine.cpp:459:31  

#20 0x555b9849c1a6 in (anonymous namespace)::DynPropGetterAdapter\_MethodCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) fxjs/xfa/cfxjse\_class.cpp:112:7  

#21 0x555b9887d515 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api-arguments-inl.h:157:3  

#22 0x555b98879c56 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:109:36  

#23 0x555b9887628a in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) v8/src/builtins/builtins-api.cc:139:5  

#24 0x555b9887555e in v8::internal::Builtin\_HandleApiCall(int, unsigned long\*, v8::internal::Isolate\*) v8/src/builtins/builtins-api.cc:127:1  

#25 0x555b9afac33f in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_NoBuiltinExit (/media/monkie/storage/pdfium/out/asan-2019-07-17/pdfium\_test+0x59bd33f)  

#26 0x555b9ad33f34 in Builtins\_InterpreterEntryTrampoline (/media/monkie/storage/pdfium/out/asan-2019-07-17/pdfium\_test+0x5744f34)  

#27 0x555b9ad1d81b in Builtins\_ArgumentsAdaptorTrampoline (/media/monkie/storage/pdfium/out/asan-2019-07-17/pdfium\_test+0x572e81b)  

#28 0x555b9ad33f34 in Builtins\_InterpreterEntryTrampoline (/media/monkie/storage/pdfium/out/asan-2019-07-17/pdfium\_test+0x5744f34)  

#29 0x555b9ad1d81b in Builtins\_ArgumentsAdaptorTrampoline (/media/monkie/storage/pdfium/out/asan-2019-07-17/pdfium\_test+0x572e81b)

previously allocated by thread T0 here:  

#0 0x555b9711f8ed in operator new(unsigned long) /b/swarming/w/ir/k/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cc:105:3  

#1 0x555b97132058 in std::\_\_1::\_\_libcpp\_allocate(unsigned long, unsigned long) buildtools/third\_party/libc++/trunk/include/new:238:10  

#2 0x555b984c9e67 in std::\_\_1::allocator<CXFA\_Node\*>::allocate(unsigned long, void const\*) buildtools/third\_party/libc++/trunk/include/memory:1813:37  

#3 0x555b984c9d30 in std::\_\_1::allocator\_traits<std::\_\_1::allocator<CXFA\_Node\*> >::allocate(std::\_\_1::allocator<CXFA\_Node\*>&, unsigned long) buildtools/third\_party/libc++/trunk/include/memory:1546:21  

#4 0x555b984c945e in std::\_\_1::\_\_split\_buffer<CXFA\_Node\*, std::\_\_1::allocator<CXFA\_Node\*>&>::\_\_split\_buffer(unsigned long, unsigned long, std::\_\_1::allocator<CXFA\_Node\*>&) buildtools/third\_party/libc++/trunk/include/\_\_split\_buffer:311:29  

#5 0x555b9b70b477 in void std::\_\_1::vector<CXFA\_Node\*, std::\_\_1::allocator<CXFA\_Node\*> >::\_\_emplace\_back\_slow\_path<CXFA\_Node\*&>(CXFA\_Node\*&) buildtools/third\_party/libc++/trunk/include/vector:1667:49  

#6 0x555b9b6c3782 in void std::\_\_1::vector<CXFA\_Node\*, std::\_\_1::allocator<CXFA\_Node\*> >::emplace\_back<CXFA\_Node\*&>(CXFA\_Node\*&) buildtools/third\_party/libc++/trunk/include/vector:1694:9  

#7 0x555b9b689d44 in CXFA\_Node::AddBindItem(CXFA\_Node\*) xfa/fxfa/parser/cxfa\_node.cpp:1218:22  

#8 0x555b9b623c24 in (anonymous namespace)::CreateDataBinding(CXFA\_Node\*, CXFA\_Node\*, bool) xfa/fxfa/parser/cxfa\_document.cpp:491:14  

#9 0x555b9b62128a in (anonymous namespace)::CopyContainer\_Field(CXFA\_Document\*, CXFA\_Node\*, CXFA\_Node\*, CXFA\_Node\*, bool, bool) xfa/fxfa/parser/cxfa\_document.cpp:816:7  

#10 0x555b9b61e0c9 in CXFA\_Document::DataMerge\_CopyContainer(CXFA\_Node\*, CXFA\_Node\*, CXFA\_Node\*, bool, bool, bool) xfa/fxfa/parser/cxfa\_document.cpp:1590:14  

#11 0x555b9b623310 in CXFA\_Document::DoDataMerge() xfa/fxfa/parser/cxfa\_document.cpp:1750:7  

#12 0x555b9b625b16 in CXFA\_Document::DoDataRemerge(bool) xfa/fxfa/parser/cxfa\_document.cpp:1805:5  

#13 0x555b985afb36 in CJX\_Template::remerge(CFX\_V8\*, std::\_\_1::vector<v8::Local[v8::Value](javascript:void(0);), std::\_\_1::allocator<v8::Local[v8::Value](javascript:void(0);) > > const&) fxjs/xfa/cjx\_template.cpp:50:18  

#14 0x555b985b0e0b in CJX\_Template::remerge\_static(CJX\_Object\*, CFX\_V8\*, std::\_\_1::vector<v8::Local[v8::Value](javascript:void(0);), std::\_\_1::allocator<v8::Local[v8::Value](javascript:void(0);) > > const&) fxjs/xfa/cjx\_template.h:31:3  

#15 0x555b9857f1e5 in CJX\_Object::RunMethod(fxcrt::WideString const&, std::\_\_1::vector<v8::Local[v8::Value](javascript:void(0);), std::\_\_1::allocator<v8::Local[v8::Value](javascript:void(0);) > > const&) fxjs/xfa/cjx\_object.cpp:177:10  

#16 0x555b984b1441 in CFXJSE\_Engine::NormalMethodCall(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&, fxcrt::WideString const&) fxjs/xfa/cfxjse\_engine.cpp:459:31  

#17 0x555b9849c1a6 in (anonymous namespace)::DynPropGetterAdapter\_MethodCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) fxjs/xfa/cfxjse\_class.cpp:112:7  

#18 0x555b9887d515 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api-arguments-inl.h:157:3  

#19 0x555b98879c56 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:109:36  

#20 0x555b9887628a in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) v8/src/builtins/builtins-api.cc:139:5  

#21 0x555b9887555e in v8::internal::Builtin\_HandleApiCall(int, unsigned long\*, v8::internal::Isolate\*) v8/src/builtins/builtins-api.cc:127:1  

#22 0x555b9afac33f in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_NoBuiltinExit (/media/monkie/storage/pdfium/out/asan-2019-07-17/pdfium\_test+0x59bd33f)  

#23 0x555b9ad33f34 in Builtins\_InterpreterEntryTrampoline (/media/monkie/storage/pdfium/out/asan-2019-07-17/pdfium\_test+0x5744f34)  

#24 0x555b9ad1d81b in Builtins\_ArgumentsAdaptorTrampoline (/media/monkie/storage/pdfium/out/asan-2019-07-17/pdfium\_test+0x572e81b)  

#25 0x555b9ad33f34 in Builtins\_InterpreterEntryTrampoline (/media/monkie/storage/pdfium/out/asan-2019-07-17/pdfium\_test+0x5744f34)  

#26 0x555b9ad1d81b in Builtins\_ArgumentsAdaptorTrampoline (/media/monkie/storage/pdfium/out/asan-2019-07-17/pdfium\_test+0x572e81b)  

#27 0x555b9ad29d7c in Builtins\_JSEntryTrampoline (/media/monkie/storage/pdfium/out/asan-2019-07-17/pdfium\_test+0x573ad7c)  

#28 0x555b9ad29b57 in Builtins\_JSEntry (/media/monkie/storage/pdfium/out/asan-2019-07-17/pdfium\_test+0x573ab57)  

#29 0x555b98c9d8ae in Call v8/src/simulator.h:138:12  

#30 0x555b98c9d8ae in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution.cc:266

SUMMARY: AddressSanitizer: heap-use-after-free fxjs/xfa/cjx\_object.cpp:621:31 in CJX\_Object::SetContent(fxcrt::WideString const&, fxcrt::WideString const&, bool, bool, bool)  

Shadow bytes around the buggy address:  

0x0c0c80011d20: fd fd fd fd fd fd fd fa fa fa fa fa fd fd fd fd  

0x0c0c80011d30: fd fd fd fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c0c80011d40: fa fa fa fa fd fd fd fd fd fd fd fa fa fa fa fa  

0x0c0c80011d50: fd fd fd fd fd fd fd fd fa fa fa fa fd fd fd fd  

0x0c0c80011d60: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fa  

=>0x0c0c80011d70: fa fa fa fa fd[fd]fd fd fd fd fd fd fa fa fa fa  

0x0c0c80011d80: 00 00 00 00 00 00 00 fa fa fa fa fa fd fd fd fd  

0x0c0c80011d90: fd fd fd fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c0c80011da0: fa fa fa fa fd fd fd fd fd fd fd fa fa fa fa fa  

0x0c0c80011db0: fd fd fd fd fd fd fd fd fa fa fa fa fd fd fd fd  

0x0c0c80011dc0: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fd  

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

==527==ABORTING

## Attachments

- [bug_38.pdf](attachments/bug_38.pdf) (application/pdf, 2.1 KB)

## Timeline

### ts...@chromium.org (2019-07-22)

[Empty comment from Monorail migration]

### ts...@chromium.org (2019-07-22)

[Empty comment from Monorail migration]

### th...@chromium.org (2019-07-22)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-22)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/0a30c29ba84639c7cc631656121a78264ae78bb0

commit 0a30c29ba84639c7cc631656121a78264ae78bb0
Author: Tom Sepez <tsepez@chromium.org>
Date: Mon Jul 22 18:16:09 2019

Return copy of bind nodes vector from CJX_Object::GetBindNodes().

Otherwise, range-based for loops aren't safe in face of additional
manipulations of the set of nodes. Rename to GetBindNodesCopy() to
indicate the copy is intentional. Add HasBindNodes() for the one case
where we don't actually want a copy.

Bug: chromium:986064
Change-Id: I149946e622188bb51bc08d2cd2fbcd7cac7b5c05
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/57990
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/0a30c29ba84639c7cc631656121a78264ae78bb0/fxjs/xfa/cjx_object.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/0a30c29ba84639c7cc631656121a78264ae78bb0/xfa/fxfa/parser/cxfa_node.h
[modify] https://pdfium.googlesource.com/pdfium/+/0a30c29ba84639c7cc631656121a78264ae78bb0/xfa/fxfa/parser/cxfa_node.cpp


### ts...@chromium.org (2019-07-22)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d79e2e510179f5b4a4aaa2de1e7e760774f4ef49

commit d79e2e510179f5b4a4aaa2de1e7e760774f4ef49
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Mon Jul 22 22:01:34 2019

Roll src/third_party/pdfium ca354a4d814d..0a30c29ba846 (3 commits)

https://pdfium.googlesource.com/pdfium.git/+log/ca354a4d814d..0a30c29ba846


git log ca354a4d814d..0a30c29ba846 --date=short --no-merges --format='%ad %ae %s'
2019-07-22 tsepez@chromium.org Return copy of bind nodes vector from CJX_Object::GetBindNodes().
2019-07-22 tsepez@chromium.org Fix worst-case O(n^2) copy in pdfium::Split<>()
2019-07-22 tsepez@chromium.org Rename CPDF_{Byte,Wide}String::AsSpan() to span()


Created with:
  gclient setdep -r src/third_party/pdfium@0a30c29ba846

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:986064
TBR=pdfium-deps-rolls@chromium.org

Change-Id: Iaa56ff1ad059dde063f290ca893d6b3995ba3b66
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1712456
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#679722}

[modify] https://crrev.com/d79e2e510179f5b4a4aaa2de1e7e760774f4ef49/DEPS


### sh...@chromium.org (2019-07-23)

[Empty comment from Monorail migration]

### na...@google.com (2019-07-24)

[Empty comment from Monorail migration]

### na...@google.com (2019-07-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-07-30)

Congrats the Panel decided to reward $5,000 for this report!

### na...@google.com (2019-07-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-10-29)

This issue was migrated from crbug.com/chromium/986064?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095778)*
