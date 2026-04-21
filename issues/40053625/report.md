# Security: heap-buffer-overflow in window.find

| Field | Value |
|-------|-------|
| **Issue ID** | [40053625](https://issues.chromium.org/issues/40053625) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>Editing |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | li...@gmail.com |
| **Assignee** | yo...@chromium.org |
| **Created** | 2020-10-15 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**

**VERSION**  

Chrome Version: 83.0.4103.97 stable  

Operating System: Linux

**REPRODUCTION CASE**  

browse the attached file

**CREDIT INFORMATION**  

Reporter credit: Liang Dong

==1==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60200008d016 at pc 0x5598111fad5e bp 0x7ffe7d21b0f0 sp 0x7ffe7d21b0e8  

READ of size 2 at 0x60200008d016 thread T0 (chrome)  

==1==WARNING: invalid path to external symbolizer!  

==1==WARNING: Failed to use and restart external symbolizer!  

#0 0x5598111fad5d in blink::IsWholeWordMatch(unsigned short const\*, int, blink::MatchResultICU&) ./../../third\_party/blink/renderer/core/editing/iterators/text\_searcher\_icu.cc:109:3  

#1 0x5598111fad5d in blink::TextSearcherICU::ShouldSkipCurrentMatch(blink::MatchResultICU&) const ./../../third\_party/blink/renderer/core/editing/iterators/text\_searcher\_icu.cc:211:35  

#2 0x5598111fa778 in blink::TextSearcherICU::NextMatchResult(blink::MatchResultICU&) ./../../third\_party/blink/renderer/core/editing/iterators/text\_searcher\_icu.cc:170:10  

#3 0x5598111b74fd in blink::FindBuffer::Results::Iterator::operator++() ./../../third\_party/blink/renderer/core/editing/finder/find\_buffer.cc:500:32  

#4 0x5598111b74fd in blink::FindBuffer::Results::Iterator::Iterator(blink::FindBuffer const&, blink::TextSearcherICU\*, WTF::String const&) ./../../third\_party/blink/renderer/core/editing/finder/find\_buffer.cc:489:3  

#5 0x5598111b74fd in blink::FindBuffer::Results::begin() const ./../../third\_party/blink/renderer/core/editing/finder/find\_buffer.cc:451:10  

#6 0x5598111b74fd in blink::FindBuffer::Results::IsEmpty() const ./../../third\_party/blink/renderer/core/editing/finder/find\_buffer.cc:459:10  

#7 0x5598111b74fd in blink::FindBuffer::FindMatchInRange(blink::EphemeralRangeTemplate<blink::EditingAlgorithm[blink::FlatTreeTraversal](javascript:void(0);) > const&, WTF::String, unsigned int) ./../../third\_party/blink/renderer/core/editing/finder/find\_buffer.cc:171:24  

#8 0x5598110d8c04 in blink::FindStringBetweenPositions(WTF::String const&, blink::EphemeralRangeTemplate<blink::EditingAlgorithm[blink::FlatTreeTraversal](javascript:void(0);) > const&, unsigned int) ./../../third\_party/blink/renderer/core/editing/editor.cc:780:9  

#9 0x5598110d7fba in blink::Editor::FindRangeOfString(blink::Document&, WTF::String const&, blink::EphemeralRangeTemplate<blink::EditingAlgorithm[blink::FlatTreeTraversal](javascript:void(0);) > const&, unsigned int, bool\*) ./../../third\_party/blink/renderer/core/editing/editor.cc:848:7  

#10 0x5598110d792b in blink::Editor::FindString(blink::LocalFrame&, WTF::String const&, unsigned int) ./../../third\_party/blink/renderer/core/editing/editor.cc:751:31  

#11 0x559816b00588 in blink::(anonymous namespace)::FindOperationCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) ./gen/third\_party/blink/renderer/bindings/modules/v8/v8\_window.cc:17966:41  

#12 0x5598014f9f6d in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:158:3  

#13 0x5598014f7a35 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:111:36  

#14 0x5598014f559e in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) ./../../v8/src/builtins/builtins-api.cc:141:5  

#15 0x55980360c237 in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_BuiltinExit ??:0:0  

#16 0x55980359e837 in Builtins\_InterpreterEntryTrampoline ??:0:0  

#17 0x55980359e837 in Builtins\_InterpreterEntryTrampoline ??:0:0  

#18 0x55980359e837 in Builtins\_InterpreterEntryTrampoline ??:0:0  

#19 0x55980359e837 in Builtins\_InterpreterEntryTrampoline ??:0:0  

#20 0x55980359e837 in Builtins\_InterpreterEntryTrampoline ??:0:0  

#21 0x55980359e837 in Builtins\_InterpreterEntryTrampoline ??:0:0  

#22 0x55980359e837 in Builtins\_InterpreterEntryTrampoline ??:0:0  

#23 0x55980359e837 in Builtins\_InterpreterEntryTrampoline ??:0:0  

#24 0x55980359e837 in Builtins\_InterpreterEntryTrampoline ??:0:0  

#25 0x55980359c35a in Builtins\_JSEntryTrampoline ??:0:0  

#26 0x55980359c137 in Builtins\_JSEntry ??:0:0  

#27 0x55980178ce60 in v8::internal::GeneratedCode<unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long\*\*>::Call(unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long\*\*) ./../../v8/src/execution/simulator.h:142:12  

#28 0x55980178ce60 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:368:33  

#29 0x55980178bde0 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) ./../../v8/src/execution/execution.cc:462:10  

#30 0x5598013d1b52 in v8::Function::Call(v8::Local[v8::Context](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*) ./../../v8/src/api/api.cc:5007:7  

#31 0x55980fe92424 in blink::V8ScriptRunner::CallFunction(v8::Local[v8::Function](javascript:void(0);), blink::ExecutionContext\*, v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*, v8::Isolate\*) ./../../third\_party/blink/renderer/bindings/core/v8/v8\_script\_runner.cc:629:17  

#32 0x5598115b0ef7 in blink::V8Function::Invoke(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::HeapVector<blink::ScriptValue, 0u> const&) ./gen/third\_party/blink/renderer/bindings/core/v8/v8\_function.cc:107:8  

#33 0x5598115b194c in blink::V8Function::InvokeAndReportException(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::HeapVector<blink::ScriptValue, 0u> const&) ./gen/third\_party/blink/renderer/bindings/core/v8/v8\_function.cc:251:7  

#34 0x5598115af5ae in blink::ScheduledAction::Execute(blink::ExecutionContext\*) ./../../third\_party/blink/renderer/bindings/core/v8/scheduled\_action.cc:130:16  

#35 0x5598115ad783 in blink::DOMTimer::Fired() ./../../third\_party/blink/renderer/core/frame/dom\_timer.cc:209:11  

#36 0x55980fda330a in blink::TimerBase::RunInternal() ./../../third\_party/blink/renderer/platform/timer.cc:152:3  

#37 0x559804993cc5 in base::OnceCallback<void ()>::Run() && ./../../base/callback.h:100:12  

#38 0x559804993cc5 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) ./../../base/task/common/task\_annotator.cc:163:33  

#39 0x5598049cbb9f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:332:23  

#40 0x5598049cb41f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:252:36  

#41 0x5598048c2f6d in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_default.cc:39:55  

#42 0x5598049ccf00 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:446:12  

#43 0x559804940c9a in base::RunLoop::Run() ./../../base/run\_loop.cc:124:14  

#44 0x5598175c551c in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer\_main.cc:256:16  

#45 0x5598046ca22e in content::RunZygote(content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:485:14  

#46 0x5598046cd6d8 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content\_main\_runner\_impl.cc:860:10  

#47 0x5598046c70a1 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:373:36  

#48 0x5598046c76cc in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content\_main.cc:399:10  

#49 0x5597fa42d165 in ChromeMain ./../../chrome/app/chrome\_main.cc:130:12  

#50 0x7f3a858af0b2 in \_\_libc\_start\_main /build/glibc-ZN95T4/glibc-2.31/csu/../csu/libc-start.c:308:16

0x60200008d016 is located 0 bytes to the right of 6-byte region [0x60200008d010,0x60200008d016)  

allocated by thread T0 (chrome) here:  

#0 0x5597fa40101d in malloc /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_malloc\_linux.cpp:145:3  

#1 0x559809c89bd8 in base::PartitionRoot<true>::AllocFlags(int, unsigned long, char const\*) ./../../base/allocator/partition\_allocator/partition\_alloc.h:941:48  

#2 0x559809c89bd8 in base::PartitionRoot<true>::Alloc(unsigned long, char const\*) ./../../base/allocator/partition\_allocator/partition\_alloc.h:1162:10  

#3 0x559809c89bd8 in WTF::Partitions::BufferMalloc(unsigned long, char const\*) ./../../third\_party/blink/renderer/platform/wtf/allocator/partitions.cc:226:29  

#4 0x559800dc3631 in unsigned short\* WTF::PartitionAllocator::AllocateVectorBacking<unsigned short>(unsigned long) ./../../third\_party/blink/renderer/platform/wtf/allocator/partition\_allocator.h:38:9  

#5 0x559800dc3631 in WTF::VectorBufferBase<unsigned short, WTF::PartitionAllocator>::AllocateBufferNoBarrier(unsigned int) ./../../third\_party/blink/renderer/platform/wtf/vector.h:490:9  

#6 0x559800dc3631 in WTF::VectorBufferBase<unsigned short, WTF::PartitionAllocator>::AllocateTemporaryBuffer(unsigned int) ./../../third\_party/blink/renderer/platform/wtf/vector.h:550:12  

#7 0x559800dc3631 in WTF::Vector<unsigned short, 0u, WTF::PartitionAllocator>::ReallocateBuffer(unsigned int) ./../../third\_party/blink/renderer/platform/wtf/vector.h:2207:7  

#8 0x559803948376 in WTF::Vector<unsigned short, 0u, WTF::PartitionAllocator>::ReserveCapacity(unsigned int) ./../../third\_party/blink/renderer/platform/wtf/vector.h:1808:3  

#9 0x559803948376 in WTF::Vector<unsigned short, 0u, WTF::PartitionAllocator>::ExpandCapacity(unsigned int) ./../../third\_party/blink/renderer/platform/wtf/vector.h:1721:3  

#10 0x559803948376 in WTF::Vector<unsigned short, 0u, WTF::PartitionAllocator>::ExpandCapacity(unsigned int, unsigned short\*) ./../../third\_party/blink/renderer/platform/wtf/vector.h:1730:5  

#11 0x559803948376 in WTF::Vector<unsigned short, 0u, WTF::PartitionAllocator>::ExpandCapacity(unsigned int, unsigned short const\*) ./../../third\_party/blink/renderer/platform/wtf/vector.h:1441:12  

#12 0x559803948376 in void WTF::Vector<unsigned short, 0u, WTF::PartitionAllocator>::Append<unsigned short>(unsigned short const\*, unsigned int) ./../../third\_party/blink/renderer/platform/wtf/vector.h:1900:12  

#13 0x5598111bb86d in blink::FindBuffer::AddTextToBuffer(blink::Text const&, blink::LayoutBlockFlow&, blink::EphemeralRangeTemplate<blink::EditingAlgorithm[blink::FlatTreeTraversal](javascript:void(0);) > const&) ./../../third\_party/blink/renderer/core/editing/finder/find\_buffer.cc:422:13  

#14 0x5598111b631f in blink::FindBuffer::CollectTextUntilBlockBoundary(blink::EphemeralRangeTemplate<blink::EditingAlgorithm[blink::FlatTreeTraversal](javascript:void(0);) > const&) ./../../third\_party/blink/renderer/core/editing/finder/find\_buffer.cc:321:7  

#15 0x5598111b72c1 in blink::FindBuffer::FindBuffer(blink::EphemeralRangeTemplate<blink::EditingAlgorithm[blink::FlatTreeTraversal](javascript:void(0);) > const&) ./../../third\_party/blink/renderer/core/editing/finder/find\_buffer.cc:117:3  

#16 0x5598111b72c1 in blink::FindBuffer::FindMatchInRange(blink::EphemeralRangeTemplate<blink::EditingAlgorithm[blink::FlatTreeTraversal](javascript:void(0);) > const&, WTF::String, unsigned int) ./../../third\_party/blink/renderer/core/editing/finder/find\_buffer.cc:168:16  

#17 0x5598110d8c04 in blink::FindStringBetweenPositions(WTF::String const&, blink::EphemeralRangeTemplate<blink::EditingAlgorithm[blink::FlatTreeTraversal](javascript:void(0);) > const&, unsigned int) ./../../third\_party/blink/renderer/core/editing/editor.cc:780:9  

#18 0x5598110d7fba in blink::Editor::FindRangeOfString(blink::Document&, WTF::String const&, blink::EphemeralRangeTemplate<blink::EditingAlgorithm[blink::FlatTreeTraversal](javascript:void(0);) > const&, unsigned int, bool\*) ./../../third\_party/blink/renderer/core/editing/editor.cc:848:7  

#19 0x5598110d792b in blink::Editor::FindString(blink::LocalFrame&, WTF::String const&, unsigned int) ./../../third\_party/blink/renderer/core/editing/editor.cc:751:31  

#20 0x559816b00588 in blink::(anonymous namespace)::FindOperationCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) ./gen/third\_party/blink/renderer/bindings/modules/v8/v8\_window.cc:17966:41  

#21 0x5598014f9f6d in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:158:3  

#22 0x5598014f7a35 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:111:36  

#23 0x5598014f559e in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) ./../../v8/src/builtins/builtins-api.cc:141:5  

#24 0x55980360c237 in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_BuiltinExit ??:0:0  

#25 0x55980359e837 in Builtins\_InterpreterEntryTrampoline ??:0:0  

#26 0x55980359e837 in Builtins\_InterpreterEntryTrampoline ??:0:0  

#27 0x55980359e837 in Builtins\_InterpreterEntryTrampoline ??:0:0  

#28 0x55980359e837 in Builtins\_InterpreterEntryTrampoline ??:0:0  

#29 0x55980359e837 in Builtins\_InterpreterEntryTrampoline ??:0:0  

#30 0x55980359e837 in Builtins\_InterpreterEntryTrampoline ??:0:0  

#31 0x55980359e837 in Builtins\_InterpreterEntryTrampoline ??:0:0  

#32 0x55980359e837 in Builtins\_InterpreterEntryTrampoline ??:0:0  

#33 0x55980359e837 in Builtins\_InterpreterEntryTrampoline ??:0:0  

#34 0x55980359c35a in Builtins\_JSEntryTrampoline ??:0:0  

#35 0x55980359c137 in Builtins\_JSEntry ??:0:0  

#36 0x55980178ce60 in v8::internal::GeneratedCode<unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long\*\*>::Call(unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long\*\*) ./../../v8/src/execution/simulator.h:142:12  

#37 0x55980178ce60 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:368:33  

#38 0x55980178bde0 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) ./../../v8/src/execution/execution.cc:462:10  

#39 0x5598013d1b52 in v8::Function::Call(v8::Local[v8::Context](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*) ./../../v8/src/api/api.cc:5007:7  

#40 0x55980fe92424 in blink::V8ScriptRunner::CallFunction(v8::Local[v8::Function](javascript:void(0);), blink::ExecutionContext\*, v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*, v8::Isolate\*) ./../../third\_party/blink/renderer/bindings/core/v8/v8\_script\_runner.cc:629:17

SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/dev/Downloads/chromium\_src/src/out/asan/chrome+0x20917d5d)  

Shadow bytes around the buggy address:  

0x0c04800099b0: fa fa 05 fa fa fa 00 06 fa fa fd fa fa fa fd fa  

0x0c04800099c0: fa fa fd fa fa fa fd fa fa fa fd fa fa fa 01 fa  

0x0c04800099d0: fa fa 01 fa fa fa 06 fa fa fa 06 fa fa fa fd fa  

0x0c04800099e0: fa fa fd fa fa fa fd fd fa fa fd fd fa fa fd fa  

0x0c04800099f0: fa fa fd fd fa fa fd fa fa fa 00 00 fa fa fd fd  

=>0x0c0480009a00: fa fa[06]fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0480009a10: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0480009a20: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0480009a30: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0480009a40: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0480009a50: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

## Attachments

- [heap-buffer-overflow.html](attachments/heap-buffer-overflow.html) (text/plain, 279 B)

## Timeline

### cl...@chromium.org (2020-10-15)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5767959052353536.

### pa...@chromium.org (2020-10-15)

rakina, it looks like you last worked on the code at the top of the stack. Could you please take a look? Thank you!

[Monorail components: Blink>Editing]

### cl...@chromium.org (2020-10-16)

Detailed Report: https://clusterfuzz.com/testcase?key=5767959052353536

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 2
Crash Address: 0x60900023fff4
Crash State:
  blink::TextSearcherICU::ShouldSkipCurrentMatch
  blink::TextSearcherICU::NextMatchResult
  blink::FindBuffer::FindMatchInRange
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=628682:628683

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5767959052353536

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5767959052353536 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### ra...@chromium.org (2020-10-16)

Hmm, there might be some unicode-related subtleties here. We overflowed trying to get the text with U16_GET: https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/core/editing/iterators/text_searcher_icu.cc;l=109;drc=fd343439bf9582a4f3c21276893a9c081e29929c. I'm re-assigning to yosin@ who should know more than I do on this.

### yo...@chromium.org (2020-10-16)

In review: http://crrev.com/c/2476878

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/93a75877b2db7f00e94f9c8619a26e6777ce3f11

commit 93a75877b2db7f00e94f9c8619a26e6777ce3f11
Author: Yoshifumi Inoue <yosin@chromium.org>
Date: Fri Oct 16 08:41:24 2020

[FindInPage] Make IsWholeWordMatch() to use U16_GET() with valid parameter

This patch chagnes |IsWholeWordMatch()| to use |U16_GET()| with valid
parameters to avoid reading out of bounds data.

In case of search "\uDB00" (broken surrogate pair) in "\u0022\uDB00", we
call |U16_GET(text, start, index, length, u32)| with start=1, index=1,
length=1, where text = "\u0022\DB800", then |U16_GET()| reads text[2]
for surrogate tail.

After this patch, we call |U16_GET()| with length=2==end of match, to
make |U16_GET()| not to read text[2].

Bug: 1138877
Change-Id: I3407f795ab181edc7d0f1d1f0a0d380974cd34eb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2476878
Auto-Submit: Yoshifumi Inoue <yosin@chromium.org>
Reviewed-by: Rakina Zata Amni <rakina@chromium.org>
Commit-Queue: Rakina Zata Amni <rakina@chromium.org>
Commit-Queue: Yoshifumi Inoue <yosin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#817847}

[modify] https://crrev.com/93a75877b2db7f00e94f9c8619a26e6777ce3f11/third_party/blink/renderer/core/editing/iterators/text_searcher_icu.cc
[modify] https://crrev.com/93a75877b2db7f00e94f9c8619a26e6777ce3f11/third_party/blink/renderer/core/editing/iterators/text_searcher_icu_test.cc


### [Deleted User] (2020-10-16)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2020-10-19)

Detailed Report: https://clusterfuzz.com/testcase?key=5767959052353536

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 2
Crash Address: 0x60900023fff4
Crash State:
  blink::TextSearcherICU::ShouldSkipCurrentMatch
  blink::TextSearcherICU::NextMatchResult
  blink::FindBuffer::FindMatchInRange
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=628682:628683

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5767959052353536

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5767959052353536 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2020-10-19)

Detailed Report: https://clusterfuzz.com/testcase?key=5767959052353536

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 2
Crash Address: 0x60900023fff4
Crash State:
  blink::TextSearcherICU::ShouldSkipCurrentMatch
  blink::TextSearcherICU::NextMatchResult
  blink::FindBuffer::FindMatchInRange
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=628682:628683

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5767959052353536

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5767959052353536 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2020-10-19)

Detailed Report: https://clusterfuzz.com/testcase?key=5767959052353536

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 2
Crash Address: 0x60900023fff4
Crash State:
  blink::TextSearcherICU::ShouldSkipCurrentMatch
  blink::TextSearcherICU::NextMatchResult
  blink::FindBuffer::FindMatchInRange
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=628682:628683

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5767959052353536

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5767959052353536 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2020-10-20)

Detailed Report: https://clusterfuzz.com/testcase?key=5767959052353536

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 2
Crash Address: 0x60900023fff4
Crash State:
  blink::TextSearcherICU::ShouldSkipCurrentMatch
  blink::TextSearcherICU::NextMatchResult
  blink::FindBuffer::FindMatchInRange
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=628682:628683

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5767959052353536

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5767959052353536 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### yo...@chromium.org (2020-10-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-10-20)

Detailed Report: https://clusterfuzz.com/testcase?key=5767959052353536

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 2
Crash Address: 0x60900023fff4
Crash State:
  blink::TextSearcherICU::ShouldSkipCurrentMatch
  blink::TextSearcherICU::NextMatchResult
  blink::FindBuffer::FindMatchInRange
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=628682:628683

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5767959052353536

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5767959052353536 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### [Deleted User] (2020-10-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-10-21)

Detailed Report: https://clusterfuzz.com/testcase?key=5767959052353536

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 2
Crash Address: 0x60900023fff4
Crash State:
  blink::TextSearcherICU::ShouldSkipCurrentMatch
  blink::TextSearcherICU::NextMatchResult
  blink::FindBuffer::FindMatchInRange
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=628682:628683

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5767959052353536

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5767959052353536 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2020-10-21)

ClusterFuzz testcase 5767959052353536 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=817421:819253

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### cl...@chromium.org (2020-10-22)

Detailed Report: https://clusterfuzz.com/testcase?key=5767959052353536

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 2
Crash Address: 0x60900023fff4
Crash State:
  blink::TextSearcherICU::ShouldSkipCurrentMatch
  blink::TextSearcherICU::NextMatchResult
  blink::FindBuffer::FindMatchInRange
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=628682:628683

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5767959052353536

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5767959052353536 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### ad...@google.com (2020-10-26)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-26)

mbarbella@ is there any way to request a finer grained fix range after the recent ASAN outage (see the huge range in https://crbug.com/chromium/1138877#c16)? There are several bugs which are going to be time-consuming to discuss at the VRP as we don't know which CL fixed them, so I can't check for duplicates.

### [Deleted User] (2020-10-26)

Requesting merge to beta M87 because latest trunk commit (817847) appears to be after beta branch point (812852).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-26)

This bug requires manual review: M87's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna @(iOS), cindyb@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2020-10-26)

Re https://crbug.com/chromium/1138877#c19: I can't think of anything simple that would work well. On the off chance that any of the bugs can be reproduced on jobs that didn't break, re-uploading to those is the only thing I can think of that would help, but I don't expect that to be likely.

### ad...@google.com (2020-10-27)

Thanks mbarbella@. yosin@, can you help identify how this was fixed?

Rejecting merge to M87 because it's not clear what we should merge.

### ad...@google.com (2020-10-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-10-28)

Congratulations! The VRP panel has awarded $2000 for this bug.

### ad...@google.com (2020-10-29)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-13)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-19)

[Empty comment from Monorail migration]

### ja...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### gi...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e75cf1792dba812a4e43a928e275f6d83df8b961

commit e75cf1792dba812a4e43a928e275f6d83df8b961
Author: Yoshifumi Inoue <yosin@chromium.org>
Date: Fri Jan 22 10:09:22 2021

[FindInPage] Make IsWholeWordMatch() to use U16_GET() with valid parameter

This patch chagnes |IsWholeWordMatch()| to use |U16_GET()| with valid
parameters to avoid reading out of bounds data.

In case of search "\uDB00" (broken surrogate pair) in "\u0022\uDB00", we
call |U16_GET(text, start, index, length, u32)| with start=1, index=1,
length=1, where text = "\u0022\DB800", then |U16_GET()| reads text[2]
for surrogate tail.

After this patch, we call |U16_GET()| with length=2==end of match, to
make |U16_GET()| not to read text[2].

(cherry picked from commit 93a75877b2db7f00e94f9c8619a26e6777ce3f11)

Bug: 1138877
Change-Id: I3407f795ab181edc7d0f1d1f0a0d380974cd34eb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2476878
Auto-Submit: Yoshifumi Inoue <yosin@chromium.org>
Reviewed-by: Rakina Zata Amni <rakina@chromium.org>
Commit-Queue: Rakina Zata Amni <rakina@chromium.org>
Commit-Queue: Yoshifumi Inoue <yosin@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#817847}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2640057
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Yoshifumi Inoue <yosin@chromium.org>
Commit-Queue: Jana Grill <janagrill@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1527}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/e75cf1792dba812a4e43a928e275f6d83df8b961/third_party/blink/renderer/core/editing/iterators/text_searcher_icu_test.cc
[modify] https://crrev.com/e75cf1792dba812a4e43a928e275f6d83df8b961/third_party/blink/renderer/core/editing/iterators/text_searcher_icu.cc


### ja...@google.com (2021-01-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-02-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1138877?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053625)*
