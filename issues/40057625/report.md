# Security: PDFium Use-After-Free in v8::internal::ArrayBufferExtension::Mark

| Field | Value |
|-------|-------|
| **Issue ID** | [40057625](https://issues.chromium.org/issues/40057625) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler, Blink>JavaScript>GarbageCollection, Internals>Plugins>PDF |
| **Platforms** | Windows |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | ml...@chromium.org |
| **Created** | 2021-10-16 |
| **Bounty** | $1,000.00 |

## Description

## **VULNERABILITY DETAILS**

Reproduce steps:

1. Checkout <https://pdfium.googlesource.com/pdfium/+/877b5b9170f101e4aec980e3807dbb787a3f6fa4>
2. Compile a 32-bit version of pdfium\_test with xfa and v8 enabled
3. Enable page heap for pdfium\_test.exe
4. Open poc.pdf
5. Please note that currently I can only reproduce the crash with 32-bit version of pdfium\_test.exe. And Asan only supports x64. Thus the following debug log was copied from WinDbg.

(39c8.43d0): Access violation - code c0000005 (!!! second chance !!!)  

eax=15b8afe8 ebx=0f3c5ec7 ecx=058fea38 edx=00000006 esi=166f6fd8 edi=28504869  

eip=00a1b6cc esp=058fe9f4 ebp=058fe9f4 iopl=0 nv up ei pl nz na pe nc  

cs=0023 ss=002b ds=002b es=002b fs=0053 gs=002b efl=00010206  

pdfium\_test!std::\_\_1::\_\_cxx\_atomic\_store [inlined in pdfium\_test!v8::internal::JSArrayBuffer::MarkExtension+0xc]:  

00a1b6cc c60001 mov byte ptr [eax],1 ds:002b:15b8afe8=??

0:000> ub eip  

pdfium\_test!v8::internal::JSArrayBuffer::GetBackingStore+0x3e:  

00a1b6be cc int 3  

00a1b6bf cc int 3  

pdfium\_test!v8::internal::JSArrayBuffer::MarkExtension [pdfium\v8\src\objects\js-array-buffer.cc @ 154]:  

00a1b6c0 55 push ebp  

00a1b6c1 89e5 mov ebp,esp  

00a1b6c3 8b01 mov eax,dword ptr [ecx]  

00a1b6c5 8b4017 mov eax,dword ptr [eax+17h]  

00a1b6c8 85c0 test eax,eax  

00a1b6ca 7403 je pdfium\_test!v8::internal::JSArrayBuffer::MarkExtension+0xf (00a1b6cf)

0:000> dd poi(ecx)  

28504869 a50f3c5e a52aa021 002aa021 00000100  

28504879 00000100 e8125940 0215b8af 00000000  

28504889 00000000 90000000 a51b6020 a52aa021  

28504899 002aa021 00000000 00000000 00000000  

285048a9 02000000 00000000 00000000 15000000  

285048b9 902aa022 c000076e 9c0073ff c0327848  

285048c9 a40073ff e0327848 ac0073ff e0327848  

285048d9 b40073ff 00327848 bc007400 00327848

0:000> !heap -p -a eax  

address 15b8afe8 found in  

\_DPH\_HEAP\_ROOT @ a2b1000  

in free-ed allocation ( DPH\_HEAP\_BLOCK: VirtAddr VirtSize)  

155036b4: 15b8a000 2000  

6c0aab02 verifier!AVrfDebugPageHeapFree+0x000000c2  

76fff966 ntdll!RtlDebugFreeHeap+0x0000003e  

76f63d46 ntdll!RtlpFreeHeap+0x000000d6  

76fa791d ntdll!RtlpFreeHeapInternal+0x00000783  

76f63c16 ntdll!RtlFreeHeap+0x00000046  

0114c35a pdfium\_test!\_free\_base+0x0000001c [pdfium\out\Fuzzing\minkernel\crts\ucrt\src\appcrt\heap\free\_base.cpp @ 105]  

01141198 pdfium\_test!free+0x00000018 [pdfium\out\Fuzzing\minkernel\crts\ucrt\src\appcrt\heap\free.cpp @ 30]  

00897af5 pdfium\_test!v8::internal::ArrayBufferSweeper::SweepingJob::SweepYoung+0x000000e5 [pdfium\v8\src\heap\array-buffer-sweeper.cc @ 330]  

00897441 pdfium\_test!v8::internal::ArrayBufferSweeper::SweepingJob::Sweep+0x00000031 [pdfium\v8\src\heap\array-buffer-sweeper.cc @ 276]  

00897695 pdfium\_test!v8::internal::ArrayBufferSweeper::RequestSweep+0x00000045 [pdfium\v8\src\heap\array-buffer-sweeper.cc @ 171]  

00933153 pdfium\_test!v8::internal::ScavengerCollector::CollectGarbage+0x00001633 [pdfium\v8\src\heap\scavenger.cc @ 452]  

008c9658 pdfium\_test!v8::internal::Heap::Scavenge+0x00000208 [pdfium\v8\src\heap\heap.cc @ 2646]  

008c73aa pdfium\_test!v8::internal::Heap::PerformGarbageCollection+0x0000034a [pdfium\v8\src\heap\heap.cc @ 2209]  

008c4dec pdfium\_test!v8::internal::Heap::CollectGarbage+0x000007ec [pdfium\v8\src\heap\heap.cc @ 1788]  

008cb6f3 pdfium\_test!v8::internal::Heap::AllocateExternalBackingStore+0x00000063 [pdfium\v8\src\heap\heap.cc @ 3095]  

009c0a61 pdfium\_test!v8::internal::BackingStore::Allocate+0x00000091 [pdfium\v8\src\objects\backing-store.cc @ 301]  

007d6e53 pdfium\_test!v8::internal::`anonymous namespace'::ConstructBuffer+0x00000113 [pdfium\v8\src\builtins\builtins-arraybuffer.cc @ 79] 007d5c61 pdfium_test!v8::internal::Builtin_Impl_ArrayBufferConstructor+0x000001e1 [pdfium\v8\src\builtins\builtins-arraybuffer.cc @ 164] 007d585f pdfium_test!v8::internal::Builtin_ArrayBufferConstructor+0x0000002f [pdfium\v8\src\builtins\builtins-arraybuffer.cc @ 128] 01084b37 pdfium_test!Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit+0x00000037 01026973 pdfium_test!Builtins_JSBuiltinsConstructStub+0x00000113 0102723c pdfium_test!Builtins_JSConstructEntryTrampoline+0x0000005c 01027085 pdfium_test!Builtins_JSConstructEntry+0x00000065 0086e799 pdfium_test!v8::internal::`anonymous namespace'::Invoke+0x00000949 [pdfium\v8\src\execution\execution.cc @ 375]  

0086eba5 pdfium\_test!v8::internal::Execution::New+0x00000065 [pdfium\v8\src\execution\execution.cc @ 487]  

007d74f2 pdfium\_test!v8::internal::SliceHelper+0x00000512 [pdfium\v8\src\builtins\builtins-arraybuffer.cc @ 261]  

007d62c6 pdfium\_test!v8::internal::Builtin\_ArrayBufferPrototypeSlice+0x00000036 [pdfium\v8\src\builtins\builtins-arraybuffer.cc @ 352]  

01084b37 pdfium\_test!Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_BuiltinExit+0x00000037  

01028b55 pdfium\_test!Builtins\_InterpreterEntryTrampoline+0x000000d5  

01028b55 pdfium\_test!Builtins\_InterpreterEntryTrampoline+0x000000d5  

01028b55 pdfium\_test!Builtins\_InterpreterEntryTrampoline+0x000000d5  

010271bc pdfium\_test!Builtins\_JSEntryTrampoline+0x0000005c

0:000> k

# ChildEBP RetAddr

00 (Inline) -------- pdfium\_test!std::\_\_1::\_\_cxx\_atomic\_store [pdfium\buildtools\third\_party\libc++\trunk\include\atomic @ 993]  

01 (Inline) -------- pdfium\_test!std::\_\_1::\_\_atomic\_base<bool,0>::store [pdfium\buildtools\third\_party\libc++\trunk\include\atomic @ 1607]  

02 (Inline) -------- pdfium\_test!v8::internal::ArrayBufferExtension::Mark [pdfium\v8\src\objects\js-array-buffer.h @ 169]  

03 058fe9f4 008dca49 pdfium\_test!v8::internal::JSArrayBuffer::MarkExtension+0xc [pdfium\v8\src\objects\js-array-buffer.cc @ 157]  

04 (Inline) -------- pdfium\_test!v8::internal::MarkingVisitorBase<v8::internal::MainMarkingVisitor[v8::internal::MajorMarkingState](javascript:void(0);),v8::internal::MajorMarkingState>::VisitJSArrayBuffer+0xb [pdfium\v8\src\heap\marking-visitor-inl.h @ 284]  

05 (Inline) -------- pdfium\_test!v8::internal::HeapVisitor<int,v8::internal::MainMarkingVisitor[v8::internal::MajorMarkingState](javascript:void(0);) >::Visit+0xab9 [pdfium\v8\src\heap\objects-visiting-inl.h @ 50]  

06 058fea78 008e85ac pdfium\_test!v8::internal::MarkCompactCollector::ProcessMarkingWorklist[v8::internal::MarkCompactCollector::MarkingWorklistProcessingMode::kDefault](javascript:void(0);)+0xbb9 [pdfium\v8\src\heap\mark-compact.cc @ 1939]  

07 (Inline) -------- pdfium\_test!v8::internal::MarkCompactCollector::DrainMarkingWorklist+0xe [pdfium\v8\src\heap\mark-compact.cc @ 1900]  

08 058fec0c 008e7e69 pdfium\_test!v8::internal::MarkCompactCollector::MarkLiveObjects+0x6dc [pdfium\v8\src\heap\mark-compact.cc @ 2066]  

09 058fec28 008c8ff9 pdfium\_test!v8::internal::MarkCompactCollector::CollectGarbage+0x79 [pdfium\v8\src\heap\mark-compact.cc @ 587]  

0a 058fec70 008c73a1 pdfium\_test!v8::internal::Heap::MarkCompact+0x169 [pdfium\v8\src\heap\heap.cc @ 2475]  

0b 058feda0 008c4dec pdfium\_test!v8::internal::Heap::PerformGarbageCollection+0x341 [pdfium\v8\src\heap\heap.cc @ 2203]  

0c 058feecc 008ce813 pdfium\_test!v8::internal::Heap::CollectGarbage+0x7ec [pdfium\v8\src\heap\heap.cc @ 1788]  

0d 058fef00 008ce8dc pdfium\_test!v8::internal::Heap::AllocateRawWithLightRetrySlowPath+0x73 [pdfium\v8\src\heap\heap.cc @ 5471]  

0e 058fef30 008aa1f8 pdfium\_test!v8::internal::Heap::AllocateRawWithRetryOrFailSlowPath+0x2c [pdfium\v8\src\heap\heap.cc @ 5486]  

0f (Inline) -------- pdfium\_test!v8::internal::Heap::AllocateRawWith+0x43 [pdfium\v8\src\heap\heap-inl.h @ 346]  

10 058fef64 008a4e76 pdfium\_test!v8::internal::Factory::AllocateRaw+0x68 [pdfium\v8\src\heap\factory.cc @ 370]  

11 (Inline) -------- pdfium\_test!v8::internal::FactoryBase[v8::internal::Factory](javascript:void(0);)::AllocateRaw+0x13 [pdfium\v8\src\heap\factory-base.cc @ 861]  

12 (Inline) -------- pdfium\_test!v8::internal::FactoryBase[v8::internal::Factory](javascript:void(0);)::AllocateRawWithImmortalMap+0x13 [pdfium\v8\src\heap\factory-base.cc @ 852]  

13 058fef94 00a9ea88 pdfium\_test!v8::internal::FactoryBase[v8::internal::Factory](javascript:void(0);)::NewRawTwoByteString+0x66 [pdfium\v8\src\heap\factory-base.cc @ 572]  

14 058fefdc 00799384 pdfium\_test!v8::internal::String::SlowFlatten+0xf8 [pdfium\v8\src\objects\string.cc @ 64]  

15 058ff000 008ac660 pdfium\_test!v8::internal::String::Flatten+0x54 [pdfium\v8\src\objects\string-inl.h @ 612]  

16 058ff05c 00b8f2ca pdfium\_test!v8::internal::Factory::NewProperSubString+0x30 [pdfium\v8\src\heap\factory.cc @ 1002]  

17 (Inline) -------- pdfium\_test!v8::internal::Factory::NewSubString+0x19 [pdfium\v8\src\heap\factory-inl.h @ 46]  

18 (Inline) -------- pdfium\_test!v8::internal::\_\_RT\_impl\_Runtime\_StringSubstring+0xe4 [pdfium\v8\src\runtime\runtime-strings.cc @ 158]  

19 058ff098 01084a57 pdfium\_test!v8::internal::Runtime\_StringSubstring+0x10a [pdfium\v8\src\runtime\runtime-strings.cc @ 148]  

1a 058ff0b4 010da734 pdfium\_test!Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_NoBuiltinExit+0x37  

1b 058ff0f4 01028b55 pdfium\_test!Builtins\_StringPrototypeSubstring+0x774  

1c 058ff140 01028b55 pdfium\_test!Builtins\_InterpreterEntryTrampoline+0xd5  

1d 058ff194 01028b55 pdfium\_test!Builtins\_InterpreterEntryTrampoline+0xd5  

1e 058ff1c0 010271bc pdfium\_test!Builtins\_InterpreterEntryTrampoline+0xd5  

1f 058ff1d4 01026fe5 pdfium\_test!Builtins\_JSEntryTrampoline+0x5c  

20 058ff200 0086e799 pdfium\_test!Builtins\_JSEntry+0x65  

21 (Inline) -------- pdfium\_test!v8::internal::GeneratedCode<unsigned int,unsigned int,unsigned int,unsigned int,unsigned int,int,unsigned int \*\*>::Call+0xf [pdfium\v8\src\execution\simulator.h @ 152]  

22 058ff304 0086de2c pdfium\_test!v8::internal::`anonymous namespace'::Invoke+0x949 [pdfium\v8\src\execution\execution.cc @ 375] 23 058ff350 00797811 pdfium_test!v8::internal::Execution::Call+0xdc [pdfium\v8\src\execution\execution.cc @ 470] 24 058ff470 007373f2 pdfium_test!v8::Script::Run+0x441 [pdfium\v8\src\api\api.cc @ 2084] 25 058ff4ec 00760fc3 pdfium_test!CFXJS_Engine::Execute+0xb6 [pdfium\fxjs\cfxjs_engine.cpp @ 582] 26 058ff500 0074aac9 pdfium_test!CJS_Runtime::ExecuteScript+0x13 [pdfium\fxjs\cjs_runtime.cpp @ 171] 27 058ff57c 005884ce pdfium_test!CJS_EventContext::RunScript+0x139 [pdfium\fxjs\cjs_event_context.cpp @ 49] 28 058ff5b8 00587bd2 pdfium_test!CPDFSDK_ActionHandler::RunScript+0x4e [pdfium\fpdfsdk\cpdfsdk_actionhandler.cpp @ 456] 29 058ff5f4 00587a29 pdfium_test!CPDFSDK_ActionHandler::RunDocumentOpenJavaScript+0x62 [pdfium\fpdfsdk\cpdfsdk_actionhandler.cpp @ 381] 2a 058ff634 0058794e pdfium_test!CPDFSDK_ActionHandler::ExecuteDocumentOpenAction+0xb9 [pdfium\fpdfsdk\cpdfsdk_actionhandler.cpp @ 149] 2b 058ff664 005993fc pdfium_test!CPDFSDK_ActionHandler::DoAction_DocOpen+0x32 [pdfium\fpdfsdk\cpdfsdk_actionhandler.cpp @ 27] 2c 058ff68c 005830f7 pdfium_test!CPDFSDK_FormFillEnvironment::ProcOpenAction+0xb4 [pdfium\fpdfsdk\cpdfsdk_formfillenvironment.cpp @ 692] 2d 058ff8a8 00582a4f pdfium_test!`anonymous namespace'::ProcessPdf+0x2de [pdfium\samples\pdfium\_test.cc @ 1006]  

2e 058ffa94 0112a81a pdfium\_test!main+0x1a4f [pdfium\samples\pdfium\_test.cc @ 1289]  

2f (Inline) -------- pdfium\_test!invoke\_main+0x1a [d:\agent\_work\57\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 102]  

30 058ffae0 7640fa29 pdfium\_test!\_\_scrt\_common\_main\_seh+0xf8 [d:\agent\_work\57\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 288]  

31 058ffaf0 76f87a9e KERNEL32!BaseThreadInitThunk+0x19  

32 058ffb4c 76f87a6e ntdll!\_\_RtlUserThreadStart+0x2f  

33 058ffb5c 00000000 ntdll!\_RtlUserThreadStart+0x1b

**VERSION**  

**Chrome Version: [x.x.x.x] + [stable, beta, or dev]**  

**Operating System: [Please indicate OS, version, and service pack level]**

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug, or any personal or confidential information.**

**Please attach files directly, not in zip or other archive formats, and if**  

**you've created a demonstration site please also attach the files needed to**  

**reproduce the demonstration locally.**

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

**Reporter credit: [goes here]**

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 2.7 KB)

## Timeline

### [Deleted User] (2021-10-16)

[Empty comment from Monorail migration]

### bd...@chromium.org (2021-10-18)

Assigning to @verwaest to triage

### is...@chromium.org (2021-10-19)

CCing GC folks for triaging.

[Monorail components: Blink>JavaScript>GarbageCollection]

### ml...@chromium.org (2021-10-19)

I don't recall us changing anything in the area of ABs for some time now. Anything changed in PDFium recently which could make this issue visible?

[Monorail components: Internals>Plugins>PDF]

### is...@chromium.org (2021-10-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-19)

[Empty comment from Monorail migration]

### ml...@chromium.org (2021-10-20)

[Empty comment from Monorail migration]

### ml...@chromium.org (2021-10-20)

Also reproduces slightly differently on a x86 debug build on Linux. Looks like a heap corruption.

gn args:
  is_component_build=false
  is_debug=true
  use_goma=true
  pdf_enable_v8 = true
  pdf_enable_xfa = true
  pdf_is_standalone=true
  v8_optimized_debug = false
  v8_enable_v8_checks = true
  v8_enable_fast_mksnapshot = true
  target_cpu = "x86"

Repro:
$ out/Debug/pdfium_test ~/Downloads/poc.pdf

Stack:
#
# Fatal error in ../../v8/src/heap/marking-visitor-inl.h, line 26
# Debug check failed: ReadOnlyHeap::Contains(object) || heap_->Contains(object).
#
#
#
#FailureMessage Object: 0xff86c048
==== C stack trace ===============================

    out/Debug/pdfium_test(v8::base::debug::StackTrace::StackTrace()+0x2c) [0x5bf57b8c]
    out/Debug/pdfium_test(+0x57ec24e) [0x5bd7024e]
    out/Debug/pdfium_test(V8_Fatal(char const*, int, char const*, ...)+0x134) [0x5bf2e054]
    out/Debug/pdfium_test(std::__1::enable_if<((!(std::is_function<std::__1::remove_pointer<char>::type>::value)) && (!(std::is_enum<char>::value))) && (has_output_operator<char, v8::base::CheckMessageStream>::value), std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > >::type v8::base::PrintCheckOperand<char>(char)+0) [0x5bf2d9d0]
    out/Debug/pdfium_test(V8_Dcheck(char const*, int, char const*)+0x39) [0x5bf2e139]
    out/Debug/pdfium_test(v8::internal::MarkingVisitorBase<v8::internal::MainMarkingVisitor<v8::internal::MajorMarkingState>, v8::internal::MajorMarkingState>::MarkObject(v8::internal::HeapObject, v8::internal::HeapObject)+0xb1) [0x59afe701]
    out/Debug/pdfium_test(void v8::internal::MarkingVisitorBase<v8::internal::MainMarkingVisitor<v8::internal::MajorMarkingState>, v8::internal::MajorMarkingState>::ProcessStrongHeapObject<v8::internal::FullHeapObjectSlot>(v8::internal::HeapObject, v8::internal::FullHeapObjectSlot, v8::internal::HeapObject)+0xda) [0x59afe5da]
    out/Debug/pdfium_test(void v8::internal::MarkingVisitorBase<v8::internal::MainMarkingVisitor<v8::internal::MajorMarkingState>, v8::internal::MajorMarkingState>::VisitPointersImpl<v8::internal::FullObjectSlot>(v8::internal::HeapObject, v8::internal::FullObjectSlot, v8::internal::FullObjectSlot)+0x125) [0x59afe4d5]
    out/Debug/pdfium_test(v8::internal::MarkingVisitorBase<v8::internal::MainMarkingVisitor<v8::internal::MajorMarkingState>, v8::internal::MajorMarkingState>::VisitPointers(v8::internal::HeapObject, v8::internal::FullObjectSlot, v8::internal::FullObjectSlot)+0x55) [0x59afdc35]
    out/Debug/pdfium_test(void v8::internal::BodyDescriptorBase::IteratePointers<v8::internal::MainMarkingVisitor<v8::internal::MajorMarkingState> >(v8::internal::HeapObject, int, int, v8::internal::MainMarkingVisitor<v8::internal::MajorMarkingState>*)+0xc4) [0x59b09234]
    out/Debug/pdfium_test(void v8::internal::SuffixRangeBodyDescriptor<4>::IterateBody<v8::internal::MainMarkingVisitor<v8::internal::MajorMarkingState> >(v8::internal::Map, v8::internal::HeapObject, int, v8::internal::MainMarkingVisitor<v8::internal::MajorMarkingState>*)+0x44) [0x59b0be04]
    out/Debug/pdfium_test(int v8::internal::MainMarkingVisitor<v8::internal::MajorMarkingState>::VisitLeftTrimmableArray<v8::internal::FixedArray>(v8::internal::Map, v8::internal::FixedArray)+0xd1) [0x59b0c1f1]
    out/Debug/pdfium_test(v8::internal::MarkingVisitorBase<v8::internal::MainMarkingVisitor<v8::internal::MajorMarkingState>, v8::internal::MajorMarkingState>::VisitFixedArray(v8::internal::Map, v8::internal::FixedArray)+0xeb) [0x59b056fb]
    out/Debug/pdfium_test(v8::internal::HeapVisitor<int, v8::internal::MainMarkingVisitor<v8::internal::MajorMarkingState> >::Visit(v8::internal::Map, v8::internal::HeapObject)+0x12f1) [0x59ad83e1]
    out/Debug/pdfium_test(std::__1::pair<unsigned int, unsigned int> v8::internal::MarkCompactCollector::ProcessMarkingWorklist<(v8::internal::MarkCompactCollector::MarkingWorklistProcessingMode)0>(unsigned int)+0x649) [0x59ad6f79]
    out/Debug/pdfium_test(v8::internal::MarkCompactCollector::DrainMarkingWorklist()+0x32) [0x59abd562]
    out/Debug/pdfium_test(v8::internal::MarkCompactCollector::MarkLiveObjects()+0xba5) [0x59ab4515]
    out/Debug/pdfium_test(v8::internal::MarkCompactCollector::CollectGarbage()+0x96) [0x59ab3796]
    out/Debug/pdfium_test(v8::internal::Heap::MarkCompact()+0x1c1) [0x59a1f8a1]
    out/Debug/pdfium_test(v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::GCCallbackFlags)+0x5f9) [0x59a1c869]
    out/Debug/pdfium_test(v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags)+0xd7b) [0x59a195db]
    out/Debug/pdfium_test(v8::internal::Heap::CollectAllGarbage(int, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags)+0x5b) [0x59a1794b]
    out/Debug/pdfium_test(v8::internal::Heap::HandleGCRequest()+0x16a) [0x59a1782a]
    out/Debug/pdfium_test(v8::internal::StackGuard::HandleInterrupts()+0x550) [0x598f2d50]
    out/Debug/pdfium_test(+0x3f71024) [0x5a4f5024]
    out/Debug/pdfium_test(v8::internal::Runtime_StackGuard(int, unsigned int*, v8::internal::Isolate*)+0x19f) [0x5a4f4aff]
    out/Debug/pdfium_test(+0x4efb3e3) [0x5b47f3e3]
    out/Debug/pdfium_test(+0x51c02d1) [0x5b7442d1]
    out/Debug/pdfium_test(+0x4bda705) [0x5b15e705]
    out/Debug/pdfium_test(+0x4bda705) [0x5b15e705]
    out/Debug/pdfium_test(+0x4bda705) [0x5b15e705]
    out/Debug/pdfium_test(+0x4bd243c) [0x5b15643c]
    out/Debug/pdfium_test(+0x4bd2265) [0x5b156265]
    out/Debug/pdfium_test(v8::internal::GeneratedCode<unsigned int, unsigned int, unsigned int, unsigned int, unsigned int, int, unsigned int**>::Call(unsigned int, unsigned int, unsigned int, unsigned int, int, unsigned int**)+0x67) [0x59864c17]
    out/Debug/pdfium_test(+0x32de1b6) [0x598621b6]
    out/Debug/pdfium_test(v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*)+0x94) [0x59861014]
    out/Debug/pdfium_test(v8::Script::Run(v8::Local<v8::Context>)+0xa7f) [0x59338e0f]
    out/Debug/pdfium_test(+0x2c1a879) [0x5919e879]
    out/Debug/pdfium_test(+0x2cd2c0a) [0x59256c0a]
    out/Debug/pdfium_test(+0x2c7ddbf) [0x59201dbf]
    out/Debug/pdfium_test(+0x24e4651) [0x58a68651]
    out/Debug/pdfium_test(+0x24e3054) [0x58a67054]
    out/Debug/pdfium_test(+0x24e2db5) [0x58a66db5]
    out/Debug/pdfium_test(+0x24e2c29) [0x58a66c29]
    out/Debug/pdfium_test(+0x2522a7d) [0x58aa6a7d]
    out/Debug/pdfium_test(+0x257ece2) [0x58b02ce2]
    out/Debug/pdfium_test(+0x24c82a8) [0x58a4c2a8]
    out/Debug/pdfium_test(+0x24c592d) [0x58a4992d]
    /lib/i386-linux-gnu/libc.so.6(__libc_start_main+0x106) [0xf7bf1fd6]
Trace/breakpoint trap

### ml...@chromium.org (2021-10-20)

Looked into this with cbruni@ a bit now and it looks like a missed generational barrier from IC code.

What we know:
- JSArray with holey elements where elements are backed by a FixedArray in OLD_SPACE
- JSArrayBuffer in new space
- Previously slot pointed into RO SPACE (odd ball)
- We write FixedArray[x] = JSArrayBuffer
- On this interesting write we seem to fail in the OutOfLineRecordWrite [1] page check where we should see the new space page having the kPointersToHereAreInteresting bit set. However, we see that it has kPointersFromHereAreInteresting are set.
- This results in us bailing out on the write barrier.

The only related change I remember now was [2]. Locally reverting didn't help though, so it's not that.

Looking into why we set up wrong page flags now. 

[1] https://source.chromium.org/chromium/chromium/src/+/main:v8/src/compiler/backend/ia32/code-generator-ia32.cc;l=326?q=OutOfLineRecordWrite&ss=chromium
[2] https://chromium-review.googlesource.com/c/v8/v8/+/3123412

Better repro:
$ ./out/Debug/pdfium_test --js-flags="--verify-heap --code-comments --debug-code" ~/Downloads/poc.pdf

Stack:
#
# Fatal error in ../../v8/src/heap/heap.cc, line 4453
# Check failed: untyped_->count(slot.address()) > 0 (0 vs. 0).
#
#
#
#FailureMessage Object: 0xffc2cce8
==== C stack trace ===============================

    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x2c) [0xf18e09dc]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8_libplatform.so(+0x5335e) [0xf7ecc35e]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x134) [0xf18aefd4]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(v8::internal::SlotVerifyingVisitor::VisitPointers(v8::internal::HeapObject, v8::internal::FullMaybeObjectSlot, v8::internal::FullMaybeObjectSlot)+0x162) [0xf6160e72]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(v8::internal::SlotVerifyingVisitor::VisitPointers(v8::internal::HeapObject, v8::internal::FullObjectSlot, v8::internal::FullObjectSlot)+0x1b3) [0xf6160d03]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(void v8::internal::BodyDescriptorBase::IteratePointers<v8::internal::ObjectVisitor>(v8::internal::HeapObject, int, int, v8::internal::ObjectVisitor*)+0xc5) [0xf621ed85]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(void v8::internal::SuffixRangeBodyDescriptor<4>::IterateBody<v8::internal::ObjectVisitor>(v8::internal::Map, v8::internal::HeapObject, int, v8::internal::ObjectVisitor*)+0x44) [0xf68e2cd4]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(void v8::internal::CallIterateBody::apply<v8::internal::FixedArray::BodyDescriptor, v8::internal::ObjectVisitor>(v8::internal::Map, v8::internal::HeapObject, int, v8::internal::ObjectVisitor*)+0x4e) [0xf68e15ae]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(void v8::internal::BodyDescriptorApply<v8::internal::CallIterateBody, void, v8::internal::Map, v8::internal::HeapObject, int, v8::internal::ObjectVisitor*>(v8::internal::InstanceType, v8::internal::Map, v8::internal::HeapObject, int, v8::internal::ObjectVisitor*)+0x15d6) [0xf68e0b26]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(void v8::internal::HeapObject::IterateBodyFast<v8::internal::ObjectVisitor>(v8::internal::Map, int, v8::internal::ObjectVisitor*)+0x76) [0xf68d5166]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(v8::internal::HeapObject::IterateBody(v8::internal::ObjectVisitor*)+0x7c) [0xf6884cbc]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(v8::internal::Heap::VerifyRememberedSetFor(v8::internal::HeapObject)+0x232) [0xf61384b2]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(v8::internal::PagedSpace::Verify(v8::internal::Isolate*, v8::internal::ObjectVisitor*)+0x629) [0xf62a4cf9]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(v8::internal::Heap::Verify()+0x462) [0xf612be22]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::GCCallbackFlags)+0x4ca) [0xf61290da]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags)+0xd7b) [0xf6125f7b]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(v8::internal::Heap::AllocateExternalBackingStore(std::__Cr::function<void* (unsigned int)> const&, unsigned int)+0xb0) [0xf6131e70]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(v8::internal::BackingStore::Allocate(v8::internal::Isolate*, unsigned int, v8::internal::SharedFlag, v8::internal::InitializedFlag)+0x1aa) [0xf64d532a]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(+0x3e318e2) [0xf5bec8e2]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(+0x3e2eeb1) [0xf5be9eb1]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(v8::internal::Builtin_ArrayBufferConstructor(int, unsigned int*, v8::internal::Isolate*)+0x158) [0xf5be9028]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(+0x3703823) [0xf54be823]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(+0x33d616a) [0xf519116a]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(+0x33d8e5c) [0xf5193e5c]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(+0x33d8ca5) [0xf5193ca5]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(v8::internal::GeneratedCode<unsigned int, unsigned int, unsigned int, unsigned int, unsigned int, int, unsigned int**>::Call(unsigned int, unsigned int, unsigned int, unsigned int, int, unsigned int**)+0x67) [0xf5f6bc77]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(+0x41ae216) [0xf5f69216]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(v8::internal::Execution::New(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*)+0x94) [0xf5f69a84]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(v8::internal::Execution::New(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*)+0x68) [0xf5f699d8]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(+0x3e333b2) [0xf5bee3b2]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(+0x3e2fcd2) [0xf5beacd2]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(v8::internal::Builtin_ArrayBufferPrototypeSlice(int, unsigned int*, v8::internal::Isolate*)+0x158) [0xf5bea9f8]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(+0x3703823) [0xf54be823]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(+0x33e10a5) [0xf519c0a5]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(+0x33e10a5) [0xf519c0a5]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(+0x33e10a5) [0xf519c0a5]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(+0x33d8ddc) [0xf5193ddc]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(+0x33d8c05) [0xf5193c05]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(v8::internal::GeneratedCode<unsigned int, unsigned int, unsigned int, unsigned int, unsigned int, int, unsigned int**>::Call(unsigned int, unsigned int, unsigned int, unsigned int, int, unsigned int**)+0x67) [0xf5f6bc77]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(+0x41ae216) [0xf5f69216]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*)+0x94) [0xf5f68074]
    /usr/local/google/home/mlippautz/workspace/pdfium/pdfium/out/Debug/libv8.so(v8::Script::Run(v8::Local<v8::Context>)+0xa7f) [0xf5a2c21f]
    ./out/Debug/pdfium_test(+0xb855d9) [0x5718d5d9]
    ./out/Debug/pdfium_test(+0xc3db5a) [0x57245b5a]
    ./out/Debug/pdfium_test(+0xbe8b1f) [0x571f0b1f]
    ./out/Debug/pdfium_test(+0x546d31) [0x56b4ed31]
    ./out/Debug/pdfium_test(+0x545734) [0x56b4d734]
    ./out/Debug/pdfium_test(+0x545495) [0x56b4d495]
    ./out/Debug/pdfium_test(+0x545309) [0x56b4d309]
    ./out/Debug/pdfium_test(+0x58515d) [0x56b8d15d]
    ./out/Debug/pdfium_test(FORM_DoDocumentOpenAction+0x62) [0x56be93c2]
    ./out/Debug/pdfium_test(+0x52a988) [0x56b32988]
    ./out/Debug/pdfium_test(+0x52800d) [0x56b3000d]
    /lib/i386-linux-gnu/libc.so.6(__libc_start_main+0x106) [0xf190bfd6]
Trace/breakpoint trap

### ml...@chromium.org (2021-10-21)

The issue here is very subtle: PDFium builds without wasm [1] and unfortunately this configuration has a bug in the compiler when emitting the trampolines for write barriers on x86. So the bug is limited to a configuration of x86 without wasm at build time.

Afaik, there is no Chrome build shipping in this config, so I guess this is a PDFium-only issue. I don't think the configuration is tested well as our regular V8-based CF should immediately find an issue when running without write barriers from generated code.

Fix is in flight here: https://chromium-review.googlesource.com/c/v8/v8/+/3236990

The larger question is whether this actually needs a backmerge.

tsepez: Is x86+JS a valid PDFium config? I guess on Windows 32bit?

[1] https://pdfium-review.googlesource.com/c/pdfium/+/84850


[Monorail components: Blink>JavaScript>Compiler]

### ml...@chromium.org (2021-10-21)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-10-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/2b14bd03dcf05f2b91daf51108d014041e510668

commit 2b14bd03dcf05f2b91daf51108d014041e510668
Author: Michael Lippautz <mlippautz@chromium.org>
Date: Thu Oct 21 14:59:00 2021

compiler: Fix x86 OOL write barrier stub when building without wasm

Bug: chromium:1260621
Change-Id: Iddfd5ee70ce9479209ff81f41197805e738298e0
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3236990
Reviewed-by: Michael Stanton <mvstanton@chromium.org>
Commit-Queue: Michael Lippautz <mlippautz@chromium.org>
Cr-Commit-Position: refs/heads/main@{#77501}

[modify] https://crrev.com/2b14bd03dcf05f2b91daf51108d014041e510668/src/compiler/backend/ia32/code-generator-ia32.cc


### th...@chromium.org (2021-10-21)

Well, now that there is a V8 build config without WASM, you have one more user. In Chrome, the process running PDFium passes --jitless, which I've been told implies --no-expose-wasm. That's not quite the same, right?

If it only affects standalone PDFium, then no merge is necessary.

x86 + JS is a valid PDFium config. On any given platform, the general PDFium configs are: [No JS, JS but not XFA, XFA (implies JS)]

### cb...@chromium.org (2021-10-21)

Correct, this is only cause by the compile-time flag (v8_enable_webassembly = false), not the runtime-flag ("--jitless" or "--no-expose-wasm")

### ml...@chromium.org (2021-10-21)

>Well, now that there is a V8 build config without WASM, you have one more user.

I am not sure all buildflags in V8 are officially supported. At least this one probably lacks fuzzer coverage then. I guess that should be a follow up then.

> In Chrome, the process running PDFium passes --jitless, which I've been told implies --no-expose-wasm. That's not quite the same, right?

These are different in that they switch things at runtime. E.g., even with --no-expose-wasm the engine would still support generating wasm code.

> x86 + JS is a valid PDFium config. On any given platform, the general PDFium configs are: [No JS, JS but not XFA, XFA (implies JS)]

That's what I thought :/

I think for x86, Windows is the only platform left.

V8 bug was introduced in M91 [1], PDFium switched in M92 [2]. So I think this just hit stable.

[1] https://chromiumdash.appspot.com/commit/75d7d12720594d19140aeb86a9183ed342615547
[2] https://chromiumdash.appspot.com/commit/96c19b36e4b7fc65f7973ae373edf24889798584

### [Deleted User] (2021-10-21)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2021-10-21)

We don't build and ship 32-bit x86 Chrome Linux, but standalone PDFium, like Chromium, can be built with x86 as the target platform on Linux.

### ec...@chromium.org (2021-10-21)

> I am not sure all buildflags in V8 are officially supported. At least this one probably lacks fuzzer coverage then. I guess that should be a follow up then.

v8_enable_webassembly was introduced for the Cobalt team to reduce binary size and lower the maintenance effort for them. It has not been intended to be supported beyond that until now. If there is more use of that flag, we should take the necessary steps to feel comfortable supporting it.

### ml...@chromium.org (2021-10-21)

> We don't build and ship 32-bit x86 Chrome Linux, but standalone PDFium, like Chromium, can be built with x86 as the target platform on Linux.

Not requiring a merge though, right?

This can result in UAF, can you help with severity? medium/high?

### ml...@chromium.org (2021-10-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-22)

Merge review required: M96 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-22)

Merge review required: M95 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: benmason (Android), harrysouders (iOS), None (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ml...@chromium.org (2021-10-25)

1. Why does your merge fit within the merge criteria for these milestones?

Security fix.

2. What changes specifically would you like to merge? Please link to Gerrit.

https://chromium-review.googlesource.com/c/v8/v8/+/3236990

3. Have the changes been released and tested on canary?

It's on 97.0.4678.0 and doesn't seem to cause breakage.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

n/a

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

No manual testing required.

### ml...@chromium.org (2021-10-25)

I think this is severity 'high'. Please correct me otherwise.

### va...@google.com (2021-10-25)

Thanks for dogfooding the new V8 security issue post mortem process. Please answer the Qs raised in this form:
https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.975983575=mlippautz@chromium.org&entry.307501673=1260621&entry.958145677=Windows&entry.364066060=External&entry.763880440=Head&entry.1678852700=High&entry.763402679=Internals%3EPlugins%3EPDF,+Blink%3EJavaScript%3EGarbageCollection,+Blink%3EJavaScript%3ECompiler

Thanks!

### va...@google.com (2021-10-25)

[Empty comment from Monorail migration]

### 0x...@gmail.com (2021-10-25)

> I think this is severity 'high'. Please correct me otherwise.

Hi mlippautz, I agree with you. BTW, I also found some other crashes like OOB write and OOB read, and I can confirm that your patch fixed them all, thanks.

### ml...@chromium.org (2021-10-25)

FWIW, while filling out the post mortem docs I realized that this can only be an issue if we use a different V8 than the one shipped in Chrome.

thestig: Sorry to bother again: Would this really need a backmerge as I think the PDFium shipped with Chrome on Windows32 also runs with WebAssembly.

### am...@chromium.org (2021-10-25)

merge approved for M95 and M96, please merge to the appropriate V8 branches for M95 and M96 at your earliest convenience - thanks! 

### th...@chromium.org (2021-10-25)

re: https://crbug.com/chromium/1260621#c28 - 32-bit Windows Chrome ships with WASM-enabled V8, and the code in //pdf passes --jitless, just like on any other platform. If this issue only happens when one builds V8 with v8_enable_webassembly=false, then I don't think a Chromium merge is needed.

### gi...@appspot.gserviceaccount.com (2021-10-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/194969ec77d8d100e4593a99eaa57a944b6fe302

commit 194969ec77d8d100e4593a99eaa57a944b6fe302
Author: Michael Lippautz <mlippautz@chromium.org>
Date: Thu Oct 21 14:59:00 2021

Merged: compiler: Fix x86 OOL write barrier stub when building without wasm

(cherry picked from commit 2b14bd03dcf05f2b91daf51108d014041e510668)

Bug: chromium:1260621
No-Try: true
No-Presubmit: true
No-Tree-Checks: true
Change-Id: I23dc6b2a20fce2f9c625b190eef91fc27dbd3644
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3242003
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Reviewed-by: Hannes Payer <hpayer@chromium.org>
Commit-Queue: Michael Lippautz <mlippautz@chromium.org>
Cr-Commit-Position: refs/branch-heads/9.6@{#14}
Cr-Branched-From: 0b7bda016178bf438f09b3c93da572ae3663a1f7-refs/heads/9.6.180@{#1}
Cr-Branched-From: 41a5a247d9430b953e38631e88d17790306f7a4c-refs/heads/main@{#77244}

[modify] https://crrev.com/194969ec77d8d100e4593a99eaa57a944b6fe302/src/compiler/backend/ia32/code-generator-ia32.cc


### [Deleted User] (2021-10-25)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-25)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-10-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/5cb5bb98d79c63766b85f976306ba016104b87ed

commit 5cb5bb98d79c63766b85f976306ba016104b87ed
Author: Michael Lippautz <mlippautz@chromium.org>
Date: Thu Oct 21 14:59:00 2021

Merged: compiler: Fix x86 OOL write barrier stub when building without wasm

(cherry picked from commit 2b14bd03dcf05f2b91daf51108d014041e510668)

Bug: chromium:1260621
Change-Id: I09c268bf54b3960e7cbaca45cf4384ade6acd576
No-Try: true
No-Presubmit: true
No-Tree-Checks: true
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3242004
Reviewed-by: Hannes Payer <hpayer@chromium.org>
Commit-Queue: Michael Lippautz <mlippautz@chromium.org>
Cr-Commit-Position: refs/branch-heads/9.5@{#46}
Cr-Branched-From: 4a03d61accede9dd0e3e6dc0456ff5a0e3f792b4-refs/heads/9.5.172@{#1}
Cr-Branched-From: 9a607043cb3161f8ceae1583807bece595388108-refs/heads/main@{#76741}

[modify] https://crrev.com/5cb5bb98d79c63766b85f976306ba016104b87ed/src/compiler/backend/ia32/code-generator-ia32.cc


### ml...@chromium.org (2021-10-25)

https://crbug.com/chromium/1260621#c30: Thanks, so I guess the merges were not needed then. Since they were trivial and I had them already queued, they went in nonethless.

Security folks: Unless you find a platform that ships with x86 and `v8_enable_webassembly = false` this should not be a security issue that affects users in the wild.

### am...@google.com (2021-10-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-10-28)

Since this issue only affects configuration that does not ship in a production chromium build, the VRP Panel declines to reward the usual bug amount based on class and impact; however, we did want to thank you for your efforts in reporting this to us which allowed us to identify and fix this issue regardless. We would like to award you $1000 for this report and your efforts. A member of our finance team will be in touch soon to arrange payment. Thank you! 

### am...@chromium.org (2021-10-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-10-28)

Based on https://crbug.com/chromium/1260621#c36 as well as evaluation, adjusting to security_impact-none

### am...@google.com (2021-10-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1260621?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript>Compiler, Blink>JavaScript>GarbageCollection, Internals>Plugins>PDF]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057625)*
