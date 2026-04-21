# heap-buffer-overflow in StringForwardingTable::UpdateAfterFullEvacuation

| Field | Value |
|-------|-------|
| **Issue ID** | [40069416](https://issues.chromium.org/issues/40069416) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>GarbageCollection |
| **Platforms** | Android, Linux, Mac, Windows |
| **Reporter** | em...@gmail.com |
| **Assignee** | pt...@chromium.org |
| **Created** | 2023-08-11 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**  

Tested Environment:  

Operating System: Ubuntu 22.04

Tested Chrome Versions:  

Chromium 118.0.5940.0 (gs://chromium-browser-asan/linux-release/asan-linux-release-1182064.zip)  

Chromium 113.0.5624.0 (Possibly earlier versions may also repro the same issue)  

Issue Background:  

I identified this issue while working on another bug submission approximately two months ago, as indicated in my previous report [https://bugs.chromium.org/p/chromium/issues/detail?id=1450809#c15]. However, I was unable to reproduce it at the time, which led to my delay in submission. Recently, I have managed to identify a more stable method for reproducing the issue, prompting me to submit this issue.

Reproduction Steps:  

To reproduce the issue, please follow these steps:

Utilize Puppeteer to execute the attached 'test.js' script. The issue should repro within approximately 1-2 minutes.  

Within the 'test.js' script, it is necessary to modify the paths for both the Chrome executable path and the 'poc.html' path.

- sudo apt-get install nodejs npm
- sudo npm install -g puppeteer
- node ./test.js 2>&1|grep -E 'AddressSanitizer'

**Problem Description:**  

==3813310==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x51d00026aa88 at pc 0x5583a5423548 bp 0x7fd5e59fbee0 sp 0x7fd5e59fbed8  

READ of size 4 at 0x51d00026aa88 thread T16 (DedicatedWorker)  

#0 0x5583a5423547 in \_\_cxx\_atomic\_load<int> ./../../buildtools/third\_party/libc++/trunk/include/\_\_atomic/cxx\_atomic\_impl.h:356:12  

#1 0x5583a5423547 in load ./../../buildtools/third\_party/libc++/trunk/include/\_\_atomic/atomic\_base.h:56:14  

#2 0x5583a5423547 in atomic\_load\_explicit<int> ./../../buildtools/third\_party/libc++/trunk/include/\_\_atomic/atomic.h:239:17  

#3 0x5583a5423547 in Acquire\_Load ./../../v8/src/base/atomicops.h:247:10  

#4 0x5583a5423547 in Acquire\_Load<unsigned int> ./../../v8/src/base/atomic-utils.h:80:9  

#5 0x5583a5423547 in Acquire\_Load ./../../v8/src/objects/compressed-slots-inl.h:198:26  

#6 0x5583a5423547 in UpdateAfterFullEvacuation ./../../v8/src/objects/string-forwarding-table.cc:122:37  

#7 0x5583a5423547 in v8::internal::StringForwardingTable::UpdateAfterFullEvacuation() ./../../v8/src/objects/string-forwarding-table.cc:385:9  

#8 0x5583a4abc76c in v8::internal::MarkCompactCollector::UpdatePointersAfterEvacuation() ./../../v8/src/heap/mark-compact.cc:4828:50  

#9 0x5583a4a826c6 in v8::internal::MarkCompactCollector::Evacuate() ./../../v8/src/heap/mark-compact.cc:4335:3  

#10 0x5583a4a69a4c in v8::internal::MarkCompactCollector::CollectGarbage() ./../../v8/src/heap/mark-compact.cc:396:3  

#11 0x5583a49f601d in v8::internal::Heap::MarkCompact() ./../../v8/src/heap/heap.cc:2665:29  

#12 0x5583a49ec1c6 in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GarbageCollectionReason, char const\*) ./../../v8/src/heap/heap.cc:2392:5  

#13 0x5583a49e42df in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:1863:9  

#14 0x5583a4a082a8 in CollectAllGarbage ./../../v8/src/heap/heap.cc:1522:3  

#15 0x5583a4a082a8 in v8::internal::Heap::CollectGarbageOnMemoryPressure() ./../../v8/src/heap/heap.cc:4165:3  

#16 0x5583a49e569d in v8::internal::Heap::CheckMemoryPressure() ./../../v8/src/heap/heap.cc:4148:5  

#17 0x5583a4a08901 in v8::internal::Heap::MemoryPressureNotification(v8::MemoryPressureLevel, bool) ./../../v8/src/heap/heap.cc:4205:7  

#18 0x5583a4e6d5e6 in operator() ./../../v8/src/objects/backing-store.cc:355:26  

#19 0x5583a4e6d5e6 in v8::internal::BackingStore::TryAllocateAndPartiallyCommitMemory(v8::internal::Isolate\*, unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, v8::internal::WasmMemoryFlag, v8::internal::SharedFlag) ./../../v8/src/objects/backing-store.cc:375:8  

#20 0x5583a4e6e031 in operator() ./../../v8/src/objects/backing-store.cc:458:19  

#21 0x5583a4e6e031 in v8::internal::BackingStore::AllocateWasmMemory(v8::internal::Isolate\*, unsigned long, unsigned long, v8::internal::WasmMemoryFlag, v8::internal::SharedFlag) ./../../v8/src/objects/backing-store.cc:468:24  

#22 0x5583a62a3e54 in v8::internal::WasmMemoryObject::New(v8::internal::Isolate\*, int, int, v8::internal::SharedFlag, v8::internal::WasmMemoryFlag) ./../../v8/src/wasm/wasm-objects.cc:824:7  

#23 0x5583a625bf33 in v8::(anonymous namespace)::WebAssemblyMemory(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) ./../../v8/src/wasm/wasm-js.cc:1355:8  

#24 0x5583a4476e18 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:99:3  

#25 0x5583a447533e in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<true>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), unsigned long\*, int) ./../../v8/src/builtins/builtins-api.cc:113:36  

#26 0x5583a447347d in v8::internal::Builtin\_Impl\_HandleApiConstruct(v8::internal::BuiltinArguments, v8::internal::Isolate\*) ./../../v8/src/builtins/builtins-api.cc:144:3  

#27 0x5583a760d1f5 in Builtins\_CEntry\_Return1\_ArgvOnStack\_BuiltinExit setup-isolate-deserialize.cc:0:0  

#28 0x5583a7574121 in Builtins\_JSBuiltinsConstructStub setup-isolate-deserialize.cc:0:0  

#19 0x5583e00441a9 ([anon:v8]+0x1a9)  

#30 0x5583a7574d5b in Builtins\_JSEntryTrampoline setup-isolate-deserialize.cc:0:0  

#31 0x5583a7574a86 in Builtins\_JSEntry setup-isolate-deserialize.cc:0:0  

#32 0x5583a47e36eb in Call ./../../v8/src/execution/simulator.h:178:12  

#33 0x5583a47e36eb in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:427:33  

#34 0x5583a47e2357 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) .

**Additional Comments:**

\*\*Chrome version: \*\* 115.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.5 KB)
- [test.js](attachments/test.js) (text/plain, 1.1 KB)
- [asan.log](attachments/asan.log) (text/plain, 37.3 KB)
- [poc2.html](attachments/poc2.html) (text/plain, 1.5 KB)
- [test2.js](attachments/test2.js) (text/plain, 1.3 KB)

## Timeline

### [Deleted User] (2023-08-11)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-11)

Setting OSes liberally and tentatively
FoundIn to 113 as mentioned by the reporter
FoundIn, Severity, OS, and Impact are set provisionally

Over to v8 for full triage! 




[Monorail components: Blink>JavaScript]

### [Deleted User] (2023-08-11)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-12)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-12)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2023-08-14)

Reassigning to this week's v8 security sheriff since cffsmith@ is OOO

### cl...@chromium.org (2023-08-14)

This seems to require --shared-string-table, hence no impact on production. I'll try reproducing to bisect.

### cl...@chromium.org (2023-08-14)

I was not able to reproduce yet. Is there a stand-alone reproducer in chrome or V8 that we can use?

CCing Shu as the author of --shared-string-table. Also adding GC component.

[Monorail components: -Blink>JavaScript Blink>JavaScript>GarbageCollection]

### cl...@chromium.org (2023-08-18)

Over to next week's sheriff. If we can't reproduce, this might be a WontFix for now.

### em...@gmail.com (2023-08-18)

Sorry, I don't have a stable way to reproduce it in a single browser. Using puppeteer in my local machine can reproduce it stably.
I uploaded new poc2.html and test2.js.Can you modify browser number and running time in test2.js, and try again?

I just tested it in the new version, and it can still be reproduced stably with puppeteer.

Thanks~

test version:

(Chromium 118.0.5955.0) gs://chromium-browser-asan/linux-release/asan-linux-release-1185022.zip
repro step:
node ./test2.js  2>&1 |grep -E 'AddressSanitizer'

### sa...@google.com (2023-08-21)

I've managed to reproduce this on a local Chromium build from current HEAD. The gn args I used:

use_goma = true
is_debug = false
is_official_build = false
is_asan = true
symbol_level = 2

and then I just started Chrome with '--js-flags=--shared-string-table,--expose-gc --no-sandbox', served the original poc.html via `python3 -m http.server 8000 --bind 127.0.0.1` and navigated to the site + waited a couple of minutes (so I didn't use the Puppeteer script at all).

Then eventually I saw the following crash:

#
# Fatal error in ../../v8/src/objects/string-forwarding-table-inl.h, line 241
# Debug check failed: index < capacity() (16 vs. 16).
#

So I guess that would match the ASan out-of-bounds access crash (but I guess since non-debug builds still have DCHECKs enabled, it failed the DCHECK before ASan had a chance to notice the OOB access).

Patrick, could you take a look?

I've also seen other DCHECK failures with the same testcase:

#
# Fatal error in ../../v8/src/handles/handles-inl.h, line 224
# Debug check failed: isolate->main_thread_local_heap()->IsRunning().
#

But I'm not sure if these are related.

I'll also give Clusterfuzz a chance to repro this bug, but I doubt it'll be successful (and I'm not sure if it would be particularly helpful anyway).


### cl...@chromium.org (2023-08-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5753556155695104.

### cl...@chromium.org (2023-08-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6267084037881856.

### sa...@google.com (2023-08-21)

I've now also seen this crash on a regular debug build of Chromium (i.e. non-ASan), although so far only with the 2nd DCHECK failure ("Debug check failed: isolate->main_thread_local_heap()->IsRunning().")

### pt...@chromium.org (2023-08-22)

So far I was only able to reproduce the DCHECK for handle creation. That's probably harmless as GCTracer should only be accessed with --trace-gc.
Nevertheless something we should look into. @dinfuehr: Could you take a look at this?
Stack trace:

#0  0x0000555cf57a2738 in v8::base::OS::Abort()::$_0::operator()() const (this=<optimized out>) at ../../v8/src/base/platform/platform-posix.cc:698
#1  v8::base::OS::Abort() () at ../../v8/src/base/platform/platform-posix.cc:698
#2  0x0000555cf576f3bc in V8_Fatal(char const*, int, char const*, ...) (file=<optimized out>, line=<optimized out>, format=<optimized out>)
    at ../../v8/src/base/logging.cc:167
#3  0x0000555cf576e43f in v8::base::(anonymous namespace)::DefaultDcheckHandler(char const*, int, char const*)
    (file=0x555cce3fdfe0 <str> "../../v8/src/handles/handles-inl.h", line=224, message=0x555cce3fe0a0 <str> "isolate->main_thread_local_heap()->IsRunning()")
    at ../../v8/src/base/logging.cc:57
#4  0x0000555cde4d3919 in v8::internal::HandleScope::CreateHandle(v8::internal::Isolate*, unsigned long) (isolate=0x531000168800, value=137967262514817)
    at ../../v8/src/handles/handles-inl.h:224
#5  0x0000555cdf0e22e3 in v8::internal::HandleBase::HandleBase(unsigned long, v8::internal::Isolate*) (object=139997179654144, isolate=0x531000168800, this=<optimized out>)
    at ../../v8/src/handles/handles-inl.h:29
#6  v8::internal::Handle<v8::internal::NativeContext>::Handle(v8::internal::Tagged<v8::internal::NativeContext>, v8::internal::Isolate*)
    (object=..., isolate=0x531000168800, this=<optimized out>) at ../../v8/src/handles/handles-inl.h:60
#7  v8::internal::handle<v8::internal::NativeContext>(v8::internal::Tagged<v8::internal::NativeContext>, v8::internal::Isolate*) (object=..., isolate=0x531000168800)
    at ../../v8/src/handles/handles-inl.h:72
#8  v8::internal::handle<v8::internal::NativeContext>(v8::internal::NativeContext, v8::internal::Isolate*) (object=..., isolate=0x531000168800)
    at ../../v8/src/handles/handles-inl.h:88
#9  v8::internal::Isolate::native_context() (this=0x531000168800) at ../../v8/src/execution/isolate-inl.h:51
#10 v8::internal::(anonymous namespace)::GetContextId(v8::internal::Isolate*) (isolate=0x531000168800) at ../../v8/src/heap/gc-tracer.cc:1504
#11 0x0000555cdf0d930b in v8::internal::GCTracer::ReportFullCycleToRecorder() (this=0x523000181100) at ../../v8/src/heap/gc-tracer.cc:1660
#12 0x0000555cdf0d68f3 in v8::internal::GCTracer::StopCycle(v8::internal::GarbageCollector) (this=0x523000181100, collector=<optimized out>)
    at ../../v8/src/heap/gc-tracer.cc:443
#13 0x0000555cdf0dab8a in v8::internal::GCTracer::StopFullCycleIfNeeded() (this=0x523000181100) at ../../v8/src/heap/gc-tracer.cc:460
#14 v8::internal::GCTracer::NotifyFullSweepingCompleted() (this=0x523000181100) at ../../v8/src/heap/gc-tracer.cc:524
#15 0x0000555cdf10f935 in v8::internal::Heap::EnsureSweepingCompleted(v8::internal::Heap::SweepingForcedFinalizationMode) (this=0x5310001760e8, mode=<optimized out>)
    at ../../v8/src/heap/heap.cc:7238
#16 0x0000555cdf1253d2 in v8::internal::Heap::MakeHeapIterable() (this=0x5310001760e8) at ../../v8/src/heap/heap.cc:3615
#17 0x0000555cdf1b4bba in v8::internal::MarkCompactCollector::MarkObjectsFromClientHeap(v8::internal::Isolate*) (this=0x51b000005480, client=<optimized out>)
    at ../../v8/src/heap/mark-compact.cc:1844
#18 0x0000555cdf1a183b in v8::internal::MarkCompactCollector::MarkObjectsFromClientHeaps()::$_0::operator()(v8::internal::Isolate*) const
    (client=0x531000168800, this=<optimized out>) at ../../v8/src/heap/mark-compact.cc:1828
#19 v8::internal::GlobalSafepoint::IterateClientIsolates<v8::internal::MarkCompactCollector::MarkObjectsFromClientHeaps()::$_0>(v8::internal::MarkCompactCollector::MarkObjectsFromClientHeaps()::$_0) (this=<optimized out>, callback=...) at ../../v8/src/heap/safepoint.h:178


saelo@ and/or reporter: How many cores is your system running when you are able to repro the OOB access?

### em...@gmail.com (2023-08-22)

The system I tested on, which is running Ubuntu, has 32 CPU cores and 128GB of RAM.

### pt...@chromium.org (2023-08-24)

So far still not able to repro, but thanks to dinfuehr@ we have a pretty good idea what the issue should be.


### gi...@appspot.gserviceaccount.com (2023-08-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/56a9f7b86f9f3f398cfae2f91a953ed0941ec49e

commit 56a9f7b86f9f3f398cfae2f91a953ed0941ec49e
Author: pthier <pthier@chromium.org>
Date: Fri Aug 25 07:54:58 2023

Update string forwarding table pointers only after shared GC

All entries are objects in shared space (unless
--always-use-forwarding-table), so we only need to update pointers
during a shared GC.

Bug: chromium:1472372
Change-Id: I91d23ea254c671e184d4c28a1783e5cdf55b3535
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4810357
Commit-Queue: Patrick Thier <pthier@chromium.org>
Reviewed-by: Dominik Inführ <dinfuehr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#89624}

[modify] https://crrev.com/56a9f7b86f9f3f398cfae2f91a953ed0941ec49e/src/heap/mark-compact.cc


### gi...@appspot.gserviceaccount.com (2023-08-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/bde589f3a6fd7bba05cd2bd1381e7c8f262239a5

commit bde589f3a6fd7bba05cd2bd1381e7c8f262239a5
Author: Dominik Inführ <dinfuehr@chromium.org>
Date: Fri Aug 25 07:19:36 2023

[heap] Introduce Heap::MakeNewSpaceIterable method

Add method to make the new space iterable. This is useful for a
shared GC which needs the new space to be iterable.

So far we simply used Heap::MakeHeapIterable for convenience for this purpose. However, this method makes the whole heap iterable which is
not really necessary. But more importantly, Heap::MakeHeapIterable performs a lot of actions and e.g. creates handles in
GCTracer::StopCycle. Client isolates are parked during a shared GC and therefore shouldn't create handles.

Bug: chromium:1472372
Change-Id: Ia15ad5153e60e90c4732338a834a099e271caeec
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4813236
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Commit-Queue: Dominik Inführ <dinfuehr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#89632}

[modify] https://crrev.com/bde589f3a6fd7bba05cd2bd1381e7c8f262239a5/src/heap/heap.h
[modify] https://crrev.com/bde589f3a6fd7bba05cd2bd1381e7c8f262239a5/src/heap/heap.cc
[modify] https://crrev.com/bde589f3a6fd7bba05cd2bd1381e7c8f262239a5/src/heap/mark-compact.cc


### gi...@appspot.gserviceaccount.com (2023-08-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/b9caf556b535a1d3ebf1ec8b4c29c0519fc5db8b

commit b9caf556b535a1d3ebf1ec8b4c29c0519fc5db8b
Author: Dominik Inführ <dinfuehr@chromium.org>
Date: Sun Aug 27 05:56:25 2023

Revert "[heap] Introduce Heap::MakeNewSpaceIterable method"

This reverts commit bde589f3a6fd7bba05cd2bd1381e7c8f262239a5.

Reason for revert: Seems to cause crashes.

Original change's description:
> [heap] Introduce Heap::MakeNewSpaceIterable method
>
> Add method to make the new space iterable. This is useful for a
> shared GC which needs the new space to be iterable.
>
> So far we simply used Heap::MakeHeapIterable for convenience for this purpose. However, this method makes the whole heap iterable which is
> not really necessary. But more importantly, Heap::MakeHeapIterable performs a lot of actions and e.g. creates handles in
> GCTracer::StopCycle. Client isolates are parked during a shared GC and therefore shouldn't create handles.
>
> Bug: chromium:1472372
> Change-Id: Ia15ad5153e60e90c4732338a834a099e271caeec
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4813236
> Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
> Commit-Queue: Dominik Inführ <dinfuehr@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#89632}

Bug: chromium:1472372
Change-Id: I117875f1ae6fd350ed9d2ea97f798b307392ccd7
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4813325
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Dominik Inführ <dinfuehr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#89635}

[modify] https://crrev.com/b9caf556b535a1d3ebf1ec8b4c29c0519fc5db8b/src/heap/heap.h
[modify] https://crrev.com/b9caf556b535a1d3ebf1ec8b4c29c0519fc5db8b/src/heap/heap.cc
[modify] https://crrev.com/b9caf556b535a1d3ebf1ec8b4c29c0519fc5db8b/src/heap/mark-compact.cc


### gi...@appspot.gserviceaccount.com (2023-08-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/d81b82c1259ee39f12e1e2ee1b781d97afa74fff

commit d81b82c1259ee39f12e1e2ee1b781d97afa74fff
Author: Dominik Inführ <dinfuehr@chromium.org>
Date: Mon Aug 28 13:34:51 2023

[heap] Introduce HeapObjectRange for iterating objects on pages

This CL introduces the HeapObjectRange iterator to iterate objects
on a page and uses that iterator in PagedSpaceObjectIterator.

In addition this CL changes the following things:
* Removes unused PagedSpaceObjectIterator ctor.
* Moves the PagedSpaceObjectIterator class definition into the
  .h file.
* Replaced uses of PagedSpaceObjectIterator which only iterated over
  a single page with this newly introduced iterator.

Bug: chromium:1472372
Change-Id: Ic0d1cc9ec77f3c38fe1b43caed87a0c033359339
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4813856
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Commit-Queue: Dominik Inführ <dinfuehr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#89659}

[modify] https://crrev.com/d81b82c1259ee39f12e1e2ee1b781d97afa74fff/src/heap/paged-spaces.cc
[modify] https://crrev.com/d81b82c1259ee39f12e1e2ee1b781d97afa74fff/src/heap/paged-spaces.h
[modify] https://crrev.com/d81b82c1259ee39f12e1e2ee1b781d97afa74fff/src/heap/paged-spaces-inl.h
[modify] https://crrev.com/d81b82c1259ee39f12e1e2ee1b781d97afa74fff/src/heap/spaces.h
[modify] https://crrev.com/d81b82c1259ee39f12e1e2ee1b781d97afa74fff/src/heap/mark-compact.cc


### gi...@appspot.gserviceaccount.com (2023-08-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/2a76240fed2f6b0fb7e5d9bffc33da429333ef6f

commit 2a76240fed2f6b0fb7e5d9bffc33da429333ef6f
Author: Dominik Inführ <dinfuehr@chromium.org>
Date: Mon Aug 28 14:33:14 2023

Reland "[heap] Introduce Heap::MakeNewSpaceIterable method"

This is a reland of commit bde589f3a6fd7bba05cd2bd1381e7c8f262239a5

This CL contains the following changes compared to the first version
of this CL:
* Use EnsureYoungSweepingCompleted() to finish minor sweeping.
* Avoids the PagedSpaceObjectIterator with minor ms since this
  class was using Heap::MakeHeapIterable() internally as well.

Original change's description:
> [heap] Introduce Heap::MakeNewSpaceIterable method
>
> Add method to make the new space iterable. This is useful for a
> shared GC which needs the new space to be iterable.
>
> So far we simply used Heap::MakeHeapIterable for convenience for this purpose. However, this method makes the whole heap iterable which is
> not really necessary. But more importantly, Heap::MakeHeapIterable performs a lot of actions and e.g. creates handles in
> GCTracer::StopCycle. Client isolates are parked during a shared GC and therefore shouldn't create handles.
>
> Bug: chromium:1472372
> Change-Id: Ia15ad5153e60e90c4732338a834a099e271caeec
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4813236
> Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
> Commit-Queue: Dominik Inführ <dinfuehr@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#89632}

Bug: chromium:1472372
Change-Id: I084bf282236c28063c5ff1796ff3525854897f2c
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4816530
Commit-Queue: Dominik Inführ <dinfuehr@chromium.org>
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Cr-Commit-Position: refs/heads/main@{#89663}

[modify] https://crrev.com/2a76240fed2f6b0fb7e5d9bffc33da429333ef6f/src/heap/heap.h
[modify] https://crrev.com/2a76240fed2f6b0fb7e5d9bffc33da429333ef6f/src/heap/heap.cc
[modify] https://crrev.com/2a76240fed2f6b0fb7e5d9bffc33da429333ef6f/src/heap/mark-compact.cc


### gi...@appspot.gserviceaccount.com (2023-08-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/4564a561cb2df158b3e237f965205164a8e3ffd3

commit 4564a561cb2df158b3e237f965205164a8e3ffd3
Author: Dominik Inführ <dinfuehr@chromium.org>
Date: Tue Aug 29 08:46:01 2023

Revert "Reland "[heap] Introduce Heap::MakeNewSpaceIterable method""

This reverts commit 2a76240fed2f6b0fb7e5d9bffc33da429333ef6f.

Reason for revert: Causes data races

Original change's description:
> Reland "[heap] Introduce Heap::MakeNewSpaceIterable method"
>
> This is a reland of commit bde589f3a6fd7bba05cd2bd1381e7c8f262239a5
>
> This CL contains the following changes compared to the first version
> of this CL:
> * Use EnsureYoungSweepingCompleted() to finish minor sweeping.
> * Avoids the PagedSpaceObjectIterator with minor ms since this
>   class was using Heap::MakeHeapIterable() internally as well.
>
> Original change's description:
> > [heap] Introduce Heap::MakeNewSpaceIterable method
> >
> > Add method to make the new space iterable. This is useful for a
> > shared GC which needs the new space to be iterable.
> >
> > So far we simply used Heap::MakeHeapIterable for convenience for this purpose. However, this method makes the whole heap iterable which is
> > not really necessary. But more importantly, Heap::MakeHeapIterable performs a lot of actions and e.g. creates handles in
> > GCTracer::StopCycle. Client isolates are parked during a shared GC and therefore shouldn't create handles.
> >
> > Bug: chromium:1472372
> > Change-Id: Ia15ad5153e60e90c4732338a834a099e271caeec
> > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4813236
> > Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
> > Commit-Queue: Dominik Inführ <dinfuehr@chromium.org>
> > Cr-Commit-Position: refs/heads/main@{#89632}
>
> Bug: chromium:1472372
> Change-Id: I084bf282236c28063c5ff1796ff3525854897f2c
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4816530
> Commit-Queue: Dominik Inführ <dinfuehr@chromium.org>
> Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#89663}

Bug: chromium:1472372
Change-Id: I34427f9353b50bb483f731ebafb2e68b4cb67c63
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4821532
Auto-Submit: Dominik Inführ <dinfuehr@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#89670}

[modify] https://crrev.com/4564a561cb2df158b3e237f965205164a8e3ffd3/src/heap/heap.h
[modify] https://crrev.com/4564a561cb2df158b3e237f965205164a8e3ffd3/src/heap/heap.cc
[modify] https://crrev.com/4564a561cb2df158b3e237f965205164a8e3ffd3/src/heap/mark-compact.cc


### gi...@appspot.gserviceaccount.com (2023-08-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/6133f171f2d93f38185153cced462228da54930f

commit 6133f171f2d93f38185153cced462228da54930f
Author: Dominik Inführ <dinfuehr@chromium.org>
Date: Wed Aug 30 08:10:30 2023

[heap] Add Sweeper::FinishMinor/MajorJobs methods

These new methods finish sweeper work/tasks without resetting the
sweeper state to done.

We can then use these methods to finish sweeping jobs in
MarkCompactCollector::MarkObjectsFromClientHeap to replace
Heap::MakeHeapIterable. This method is problematic in a shared GC
because it may create handles while the client isolates is
parked which violates DCHECKs.

Bug: chromium:1472372
Change-Id: I6183ca3031ef34fea522d2309ec90b218449b383
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4822567
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Commit-Queue: Dominik Inführ <dinfuehr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#89703}

[modify] https://crrev.com/6133f171f2d93f38185153cced462228da54930f/src/heap/mark-compact.cc
[modify] https://crrev.com/6133f171f2d93f38185153cced462228da54930f/src/heap/sweeper.h
[modify] https://crrev.com/6133f171f2d93f38185153cced462228da54930f/src/heap/sweeper.cc


### di...@chromium.org (2023-08-31)

@emilykim8708@gmail.com: Could you please check whether you can still reproduce the asan crasher after applying the fix in [0]? We were never able to reproduce this crash so can't verify that we fixed this for good.

0: https://chromium-review.googlesource.com/c/v8/v8/+/4810357

### em...@gmail.com (2023-08-31)

#26
On my local PC, the asan error did not repro after applying the patch.
Tested version:118.0.5966.0(with patch 4810357)
test steps:
1.node test2.js 2>&1 | grep -E 'AddressSanitizer'
2.Run for more than an hour to see the output.

### di...@chromium.org (2023-08-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-31)

[Empty comment from Monorail migration]

### am...@google.com (2023-09-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-07)

Congratulations Cassidy Kim! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-09-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1472372?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40069416)*
