# pdfium_xfa_fuzzer: Heap-buffer-overflow in fxcrt::RetainPtr<fxcrt::StringDataTemplate<wchar_t> >::RetainPtr

| Field | Value |
|-------|-------|
| **Issue ID** | [40095757](https://issues.chromium.org/issues/40095757) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-07-19 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

Out of bound in CJX\_Object::SetContent  

snippet of code

```
            int32_t i = 0;  
            for (CXFA_Node\* pValueNode = pBind->GetFirstChild(); pValueNode;  
                 pValueNode = pValueNode->GetNextSibling()) {  
              pValueNode->JSObject()->SetAttributeValue(  
                  wsSaveTextArray[i], wsSaveTextArray[i], false, false);	// <<== OOB  
              i++;  
            }  

```

**VERSION**  

Operating System: Ubuntu 16.04

**REPRODUCTION CASE**

Build pdfium with XFA enabled, ASAN enabled  

Run ./pdfium\_test bug\_37.pdf

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

=================================================================  

==26675==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60200009a538 at pc 0x556df439f196 bp 0x7ffff46f80d0 sp 0x7ffff46f80c8  

READ of size 8 at 0x60200009a538 thread T0  

#0 0x556df439f195 in std::\_\_1::unique\_ptr<fxcrt::StringDataTemplate<wchar\_t>, fxcrt::ReleaseDeleter<fxcrt::StringDataTemplate<wchar\_t> > >::get() const buildtools/third\_party/libc++/trunk/include/memory:2624:19  

#1 0x556df45b0444 in fxcrt::RetainPtr<fxcrt::StringDataTemplate<wchar\_t> >::Get() const core/fxcrt/retain\_ptr.h:54:34  

#2 0x556df45ab223 in fxcrt::RetainPtr<fxcrt::StringDataTemplate<wchar\_t> >::RetainPtr(fxcrt::RetainPtr<fxcrt::StringDataTemplate<wchar\_t> > const&) core/fxcrt/retain\_ptr.h:33:53  

#3 0x556df459ef4c in fxcrt::WideString::WideString(fxcrt::WideString const&) core/fxcrt/widestring.cpp:327:51  

#4 0x556df57c7d03 in CJX\_Object::SetAttributeValue(fxcrt::WideString const&, fxcrt::WideString const&, bool, bool) fxjs/xfa/cjx\_object.cpp:490:28  

#5 0x556df57c8c93 in CJX\_Object::SetContent(fxcrt::WideString const&, fxcrt::WideString const&, bool, bool, bool) fxjs/xfa/cjx\_object.cpp:611:39  

#6 0x556df88d51c0 in CXFA\_Node::SyncValue(fxcrt::WideString const&, bool) xfa/fxfa/parser/cxfa\_node.cpp:2151:15  

#7 0x556df88d7b77 in CXFA\_Node::SetValue(XFA\_VALUEPICTURE, fxcrt::WideString const&) xfa/fxfa/parser/cxfa\_node.cpp:4673:5  

#8 0x556df88d75a0 in CXFA\_Node::ProcessCalculate(CXFA\_FFDocView\*) xfa/fxfa/parser/cxfa\_node.cpp:2400:5  

#9 0x556df8a4010e in XFA\_ProcessEvent(CXFA\_FFDocView\*, CXFA\_Node\*, CXFA\_EventParam\*) xfa/fxfa/cxfa\_ffdocview.cpp:345:21  

#10 0x556df8a3cbbd in CXFA\_FFDocView::ExecEventActivityByDeepFirst(CXFA\_Node\*, XFA\_EVENTTYPE, bool, bool) xfa/fxfa/cxfa\_ffdocview.cpp:389:12  

#11 0x556df8a64bfc in CXFA\_FFNotify::ExecEventByDeepFirst(CXFA\_Node\*, XFA\_EVENTTYPE, bool, bool) xfa/fxfa/cxfa\_ffnotify.cpp:231:20  

#12 0x556df57963ae in CJX\_Field::execCalculate(CFX\_V8\*, std::\_\_1::vector<v8::Local[v8::Value](javascript:void(0);), std::\_\_1::allocator<v8::Local[v8::Value](javascript:void(0);) > > const&) fxjs/xfa/cjx\_field.cpp:159:14  

#13 0x556df579910b in CJX\_Field::execCalculate\_static(CJX\_Object\*, CFX\_V8\*, std::\_\_1::vector<v8::Local[v8::Value](javascript:void(0);), std::\_\_1::allocator<v8::Local[v8::Value](javascript:void(0);) > > const&) fxjs/xfa/cjx\_field.h:27:3  

#14 0x556df57bf495 in CJX\_Object::RunMethod(fxcrt::WideString const&, std::\_\_1::vector<v8::Local[v8::Value](javascript:void(0);), std::\_\_1::allocator<v8::Local[v8::Value](javascript:void(0);) > > const&) fxjs/xfa/cjx\_object.cpp:177:10  

#15 0x556df56f1711 in CFXJSE\_Engine::NormalMethodCall(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&, fxcrt::WideString const&) fxjs/xfa/cfxjse\_engine.cpp:459:31  

#16 0x556df56dc476 in (anonymous namespace)::DynPropGetterAdapter\_MethodCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) fxjs/xfa/cfxjse\_class.cpp:112:7  

#17 0x556df5abd5e5 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api-arguments-inl.h:157:3  

#18 0x556df5ab9d26 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:109:36  

#19 0x556df5ab635a in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) v8/src/builtins/builtins-api.cc:139:5  

#20 0x556df5ab562e in v8::internal::Builtin\_HandleApiCall(int, unsigned long\*, v8::internal::Isolate\*) v8/src/builtins/builtins-api.cc:127:1  

#21 0x556df81ec3ff in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_NoBuiltinExit (/media/monkie/storage/pdfium/out/asan-2019-07-17/pdfium\_test+0x59bd3ff)  

#22 0x556df7f73ff4 in Builtins\_InterpreterEntryTrampoline (/media/monkie/storage/pdfium/out/asan-2019-07-17/pdfium\_test+0x5744ff4)  

#23 0x556df7f5d8db in Builtins\_ArgumentsAdaptorTrampoline (/media/monkie/storage/pdfium/out/asan-2019-07-17/pdfium\_test+0x572e8db)  

#24 0x556df7f73ff4 in Builtins\_InterpreterEntryTrampoline (/media/monkie/storage/pdfium/out/asan-2019-07-17/pdfium\_test+0x5744ff4)  

#25 0x556df7f5d8db in Builtins\_ArgumentsAdaptorTrampoline (/media/monkie/storage/pdfium/out/asan-2019-07-17/pdfium\_test+0x572e8db)  

#26 0x556df7f69e3c in Builtins\_JSEntryTrampoline (/media/monkie/storage/pdfium/out/asan-2019-07-17/pdfium\_test+0x573ae3c)  

#27 0x556df7f69c17 in Builtins\_JSEntry (/media/monkie/storage/pdfium/out/asan-2019-07-17/pdfium\_test+0x573ac17)  

#28 0x556df5edd97e in Call v8/src/simulator.h:138:12  

#29 0x556df5edd97e in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution.cc:266  

#30 0x556df5edcd61 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution.cc:358:10  

#31 0x556df58999f9 in v8::Function::Call(v8::Local[v8::Context](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*) v8/src/api.cc:4954:7  

#32 0x556df56e56ee in CFXJSE\_Context::ExecuteScript(char const\*, CFXJSE\_Value\*, CFXJSE\_Value\*) fxjs/xfa/cfxjse\_context.cpp:300:21  

#33 0x556df56f4de3 in CFXJSE\_Engine::RunScript(CXFA\_Script::Type, fxcrt::StringViewTemplate<wchar\_t>, CFXJSE\_Value\*, CXFA\_Object\*) fxjs/xfa/cfxjse\_engine.cpp:153:23  

#34 0x556df88dbed3 in CXFA\_Node::ExecuteBoolScript(CXFA\_FFDocView\*, CXFA\_Script\*, CXFA\_EventParam\*) xfa/fxfa/parser/cxfa\_node.cpp:2700:22  

#35 0x556df88dad2f in CXFA\_Node::ProcessValidate(CXFA\_FFDocView\*, int) xfa/fxfa/parser/cxfa\_node.cpp:2598:28  

#36 0x556df8a401b9 in XFA\_ProcessEvent(CXFA\_FFDocView\*, CXFA\_Node\*, CXFA\_EventParam\*) xfa/fxfa/cxfa\_ffdocview.cpp:349:23  

#37 0x556df8a3ce84 in CXFA\_FFDocView::ExecEventActivityByDeepFirst(CXFA\_Node\*, XFA\_EVENTTYPE, bool, bool) xfa/fxfa/cxfa\_ffdocview.cpp:413:35  

#38 0x556df8a3ccf3 in CXFA\_FFDocView::ExecEventActivityByDeepFirst(CXFA\_Node\*, XFA\_EVENTTYPE, bool, bool) xfa/fxfa/cxfa\_ffdocview.cpp:400:20  

#39 0x556df8a3ccf3 in CXFA\_FFDocView::ExecEventActivityByDeepFirst(CXFA\_Node\*, XFA\_EVENTTYPE, bool, bool) xfa/fxfa/cxfa\_ffdocview.cpp:400:20  

#40 0x556df8a3d339 in CXFA\_FFDocView::InitValidate(CXFA\_Node\*) xfa/fxfa/cxfa\_ffdocview.cpp:581:3  

#41 0x556df8a3d540 in CXFA\_FFDocView::StopLayout() xfa/fxfa/cxfa\_ffdocview.cpp:127:3  

#42 0x556df8b3d4d9 in CPDFXFA\_Context::LoadXFADoc() fpdfsdk/fpdfxfa/cpdfxfa\_context.cpp:132:18  

#43 0x556df44dd19e in FPDF\_LoadXFA fpdfsdk/fpdf\_view.cpp:270:32  

#44 0x556df4368842 in (anonymous namespace)::RenderPdf(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, char const\*, unsigned long, (anonymous namespace)::Options const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) samples/pdfium\_test.cc:841:12  

#45 0x556df4363f01 in main samples/pdfium\_test.cc:1068:5  

#46 0x7f946df7a82f in \_\_libc\_start\_main (/lib/x86\_64-linux-gnu/libc.so.6+0x2082f)

0x60200009a538 is located 0 bytes to the right of 8-byte region [0x60200009a530,0x60200009a538)  

allocated by thread T0 here:  

#0 0x556df43608ed in operator new(unsigned long) /b/swarming/w/ir/k/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cc:105:3  

#1 0x556df4373058 in std::\_\_1::\_\_libcpp\_allocate(unsigned long, unsigned long) buildtools/third\_party/libc++/trunk/include/new:238:10  

#2 0x556df45ca8a7 in std::\_\_1::allocator[fxcrt::WideString](javascript:void(0);)::allocate(unsigned long, void const\*) buildtools/third\_party/libc++/trunk/include/memory:1813:37  

#3 0x556df45ca5a0 in std::\_\_1::allocator\_traits<std::\_\_1::allocator[fxcrt::WideString](javascript:void(0);) >::allocate(std::\_\_1::allocator[fxcrt::WideString](javascript:void(0);)&, unsigned long) buildtools/third\_party/libc++/trunk/include/memory:1546:21  

#4 0x556df45caf4e in std::\_\_1::\_\_split\_buffer<fxcrt::WideString, std::\_\_1::allocator[fxcrt::WideString](javascript:void(0);)&>::\_\_split\_buffer(unsigned long, unsigned long, std::\_\_1::allocator[fxcrt::WideString](javascript:void(0);)&) buildtools/third\_party/libc++/trunk/include/\_\_split\_buffer:311:29  

#5 0x556df545b3d7 in void std::\_\_1::vector<fxcrt::WideString, std::\_\_1::allocator[fxcrt::WideString](javascript:void(0);) >::\_\_push\_back\_slow\_path[fxcrt::WideString](javascript:void(0);)(fxcrt::WideString&&) buildtools/third\_party/libc++/trunk/include/vector:1617:49  

#6 0x556df545b1a2 in std::\_\_1::vector<fxcrt::WideString, std::\_\_1::allocator[fxcrt::WideString](javascript:void(0);) >::push\_back(fxcrt::WideString&&) buildtools/third\_party/libc++/trunk/include/vector:1658:9  

#7 0x556df57c8783 in CJX\_Object::SetContent(fxcrt::WideString const&, fxcrt::WideString const&, bool, bool, bool) fxjs/xfa/cjx\_object.cpp:568:31  

#8 0x556df88d51c0 in CXFA\_Node::SyncValue(fxcrt::WideString const&, bool) xfa/fxfa/parser/cxfa\_node.cpp:2151:15  

#9 0x556df88d7b77 in CXFA\_Node::SetValue(XFA\_VALUEPICTURE, fxcrt::WideString const&) xfa/fxfa/parser/cxfa\_node.cpp:4673:5  

#10 0x556df88d75a0 in CXFA\_Node::ProcessCalculate(CXFA\_FFDocView\*) xfa/fxfa/parser/cxfa\_node.cpp:2400:5  

#11 0x556df8a4010e in XFA\_ProcessEvent(CXFA\_FFDocView\*, CXFA\_Node\*, CXFA\_EventParam\*) xfa/fxfa/cxfa\_ffdocview.cpp:345:21  

#12 0x556df8a3cbbd in CXFA\_FFDocView::ExecEventActivityByDeepFirst(CXFA\_Node\*, XFA\_EVENTTYPE, bool, bool) xfa/fxfa/cxfa\_ffdocview.cpp:389:12  

#13 0x556df8a64bfc in CXFA\_FFNotify::ExecEventByDeepFirst(CXFA\_Node\*, XFA\_EVENTTYPE, bool, bool) xfa/fxfa/cxfa\_ffnotify.cpp:231:20  

#14 0x556df57963ae in CJX\_Field::execCalculate(CFX\_V8\*, std::\_\_1::vector<v8::Local[v8::Value](javascript:void(0);), std::\_\_1::allocator<v8::Local[v8::Value](javascript:void(0);) > > const&) fxjs/xfa/cjx\_field.cpp:159:14  

#15 0x556df579910b in CJX\_Field::execCalculate\_static(CJX\_Object\*, CFX\_V8\*, std::\_\_1::vector<v8::Local[v8::Value](javascript:void(0);), std::\_\_1::allocator<v8::Local[v8::Value](javascript:void(0);) > > const&) fxjs/xfa/cjx\_field.h:27:3  

#16 0x556df57bf495 in CJX\_Object::RunMethod(fxcrt::WideString const&, std::\_\_1::vector<v8::Local[v8::Value](javascript:void(0);), std::\_\_1::allocator<v8::Local[v8::Value](javascript:void(0);) > > const&) fxjs/xfa/cjx\_object.cpp:177:10  

#17 0x556df56f1711 in CFXJSE\_Engine::NormalMethodCall(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&, fxcrt::WideString const&) fxjs/xfa/cfxjse\_engine.cpp:459:31  

#18 0x556df56dc476 in (anonymous namespace)::DynPropGetterAdapter\_MethodCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) fxjs/xfa/cfxjse\_class.cpp:112:7  

#19 0x556df5abd5e5 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api-arguments-inl.h:157:3  

#20 0x556df5ab9d26 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:109:36  

#21 0x556df5ab635a in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) v8/src/builtins/builtins-api.cc:139:5  

#22 0x556df5ab562e in v8::internal::Builtin\_HandleApiCall(int, unsigned long\*, v8::internal::Isolate\*) v8/src/builtins/builtins-api.cc:127:1  

#23 0x556df81ec3ff in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_NoBuiltinExit (/media/monkie/storage/pdfium/out/asan-2019-07-17/pdfium\_test+0x59bd3ff)  

#24 0x556df7f73ff4 in Builtins\_InterpreterEntryTrampoline (/media/monkie/storage/pdfium/out/asan-2019-07-17/pdfium\_test+0x5744ff4)  

#25 0x556df7f5d8db in Builtins\_ArgumentsAdaptorTrampoline (/media/monkie/storage/pdfium/out/asan-2019-07-17/pdfium\_test+0x572e8db)  

#26 0x556df7f73ff4 in Builtins\_InterpreterEntryTrampoline (/media/monkie/storage/pdfium/out/asan-2019-07-17/pdfium\_test+0x5744ff4)  

#27 0x556df7f5d8db in Builtins\_ArgumentsAdaptorTrampoline (/media/monkie/storage/pdfium/out/asan-2019-07-17/pdfium\_test+0x572e8db)  

#28 0x556df7f69e3c in Builtins\_JSEntryTrampoline (/media/monkie/storage/pdfium/out/asan-2019-07-17/pdfium\_test+0x573ae3c)  

#29 0x556df7f69c17 in Builtins\_JSEntry (/media/monkie/storage/pdfium/out/asan-2019-07-17/pdfium\_test+0x573ac17)

SUMMARY: AddressSanitizer: heap-buffer-overflow buildtools/third\_party/libc++/trunk/include/memory:2624:19 in std::\_\_1::unique\_ptr<fxcrt::StringDataTemplate<wchar\_t>, fxcrt::ReleaseDeleter<fxcrt::StringDataTemplate<wchar\_t> > >::get() const  

Shadow bytes around the buggy address:  

0x0c048000b450: fa fa fd fa fa fa fd fa fa fa fd fd fa fa fd fa  

0x0c048000b460: fa fa fd fa fa fa fd fd fa fa fd fd fa fa fd fd  

0x0c048000b470: fa fa fd fa fa fa fd fd fa fa fd fd fa fa fd fd  

0x0c048000b480: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa  

0x0c048000b490: fa fa fd fd fa fa fd fd fa fa fd fd fa fa 00 fa  

=>0x0c048000b4a0: fa fa 00 fa fa fa 00[fa]fa fa 00 fa fa fa 00 fa  

0x0c048000b4b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c048000b4c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c048000b4d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c048000b4e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c048000b4f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

==26675==ABORTING

## Attachments

- [bug_37.pdf](attachments/bug_37.pdf) (application/pdf, 2.1 KB)

## Timeline

### cl...@chromium.org (2019-07-19)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4731246788083712.

### ts...@chromium.org (2019-07-19)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### cl...@chromium.org (2019-07-19)

Detailed report: https://clusterfuzz.com/testcase?key=4731246788083712

Fuzzer: libFuzzer_pdfium_xfa_fuzzer
Fuzz target binary: pdfium_xfa_fuzzer
Job Type: libfuzzer_chrome_asan
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 8
Crash Address: 0x6090000ae9e8
Crash State:
  fxcrt::RetainPtr<fxcrt::StringDataTemplate<wchar_t> >::RetainPtr
  CJX_Object::SetAttributeValue
  CJX_Object::SetContent
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=616464:616465

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4731246788083712

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

The recommended severity (Security_Severity-Medium) is different from what was assigned to the bug. Please double check the accuracy of the assigned severity.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-19)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/22d27c1c734a372bf72dea9531ded2889e932d0b

commit 22d27c1c734a372bf72dea9531ded2889e932d0b
Author: Tom Sepez <tsepez@chromium.org>
Date: Fri Jul 19 22:06:19 2019

CJX_Object::SetContent() should only update value nodes.

This method operates in two passes. In the first part, a set
of value nodes children is collected, but in the second pass,
all children are traversed regardless of whether they are
value nodes. There's no reason to believe these are the same
when the node has non-value node children.

- Fix possibly overly-strong assert in CXFA_Node. In turn, this
  causes one test to leave a node unmodified rather than CHECK().

Bug: chromium:985781
Change-Id: Idd8ae5d8fb5f07ae01487db589036bdab3a99ada
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/57932
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>

[add] https://pdfium.googlesource.com/pdfium/+/22d27c1c734a372bf72dea9531ded2889e932d0b/testing/resources/javascript/xfa_specific/bug_985781_expected.txt
[modify] https://pdfium.googlesource.com/pdfium/+/22d27c1c734a372bf72dea9531ded2889e932d0b/xfa/fxfa/parser/cxfa_node_unittest.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/22d27c1c734a372bf72dea9531ded2889e932d0b/fxjs/xfa/cjx_object.cpp
[add] https://pdfium.googlesource.com/pdfium/+/22d27c1c734a372bf72dea9531ded2889e932d0b/testing/resources/javascript/xfa_specific/bug_985781.in
[modify] https://pdfium.googlesource.com/pdfium/+/22d27c1c734a372bf72dea9531ded2889e932d0b/xfa/fxfa/parser/cxfa_node.cpp


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f0d04b72438ec06f09a6723bea7cc35e6f146a95

commit f0d04b72438ec06f09a6723bea7cc35e6f146a95
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Sat Jul 20 05:12:17 2019

Roll src/third_party/pdfium 23fdf8916502..ca354a4d814d (4 commits)

https://pdfium.googlesource.com/pdfium.git/+log/23fdf8916502..ca354a4d814d


git log 23fdf8916502..ca354a4d814d --date=short --no-merges --format='%ad %ae %s'
2019-07-20 tsepez@chromium.org Add fxcrt::Split() templated function.
2019-07-19 tsepez@chromium.org CJX_Object::SetContent() should only update value nodes.
2019-07-19 thestig@chromium.org Split CXFA_Node::GetNodeList().
2019-07-19 thestig@chromium.org Validate JPEG data size in libtiff.


Created with:
  gclient setdep -r src/third_party/pdfium@ca354a4d814d

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:985781,chromium:925269
TBR=pdfium-deps-rolls@chromium.org

Change-Id: Idd1ed74a0f42ea8f17a12c95c467aa495a8f1ac9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1711015
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#679370}

[modify] https://crrev.com/f0d04b72438ec06f09a6723bea7cc35e6f146a95/DEPS


### sh...@chromium.org (2019-07-20)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2019-07-22)

ClusterFuzz testcase 4731246788083712 is verified as fixed in https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=679240:679438

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### na...@google.com (2019-07-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-23)

[Empty comment from Monorail migration]

### ad...@google.com (2019-07-24)

Resetting to Security_Impact-None as it's XFA. Hopefully Clusterfuzz will get the hint :)

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

### th...@chromium.org (2020-02-20)

[Empty comment from Monorail migration]

### is...@google.com (2020-02-20)

This issue was migrated from crbug.com/chromium/985781?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095757)*
