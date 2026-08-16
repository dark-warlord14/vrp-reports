# V8 race UAF/SEGV in `TracedHandles` with ProgrammaticScrollPromise

| Field | Value |
|-------|-------|
| **Issue ID** | [504073879](https://issues.chromium.org/issues/504073879) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Scroll |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | at...@gmail.com |
| **Assignee** | mu...@chromium.org |
| **Created** | 2026-04-19 |
| **Bounty** | $10,000.00 |

## Description


Description:
There is a race condition involving ProgrammaticScrollPromise in TracedHandles GC, resulting to renderer crash, SEGV wild address read or use-after-free. Same test case can trigger both crashes, SEGV being more common.

VERSION
Chrome Version: 149.0.7795.0 ASAN build 250795ae951b3a3b
Operating System: Ubuntu 24.04 LTS

REPRODUCTION CASE

Reproducing requires a state build up, and doesn't trigger with single file. I have attached three files:
poc.html - the actual test case
serve.py - A small python server mimicking Mozilla Grizzly fuzzer server
harness.html - initial browser entrypoint that builds the state by opening poc.html in tabs.

Place all three files to same directory and launch python serve.py, then connect chrome: 
/path/to/asan/chrome --no-sandbox --disable-in-process-stack-traces --disable-popup-blocking --enable-experimental-web-platform-features --js-flags="--verify-heap" --user-data-dir=/tmp/test-prof "http://127.0.0.1:8080/?close_after=50&time_limit=2000"


serve.py behavior: 

| URL | Response |
|-----|----------|
| `/` | 307 → `/harness?<query>` |
| `/harness` | serves `harness.html` |
| `/test` | 307 → `/poc.html` |
| `/poc.html` | serves the test case |

The harness page runs as chrome's top-level document. It reads
`close_after` and `time_limit` from the query string, then repeatedly:

1. `sub = window.open()` — blank popup
2. `sub.opener = null`
3. `sub.location = "/test"` — navigate popup to poc
4. popup runs, calls `window.close()` (built into `poc.html`)
5. harness polls `sub.closed` every 50 ms
6. once closed, opens next iteration
7. after `close_after` iterations, harness closes itself

Running the test in the same renderer across many iterations is what
accumulates enough cppgc-managed promise/animator state for the race
to fire. `poc.html` directly does **not** reproduce the issue.

Default serve.py iterations is 30 before closing. It can be adjusted with --close-after. The poc.html has setTimeout window.close(), that controls the popup closing and adjusting that could help if defaults fail.

I have tested the poc on two similar machines and the default settings reproduce the issue on both machines. 

--enable-experimental-web-platform-features is currently needed, as the feature is to be landed in Chrome 149 - https://chromestatus.com/feature/5082138340491264

ASAN-trace snippets:

SEGV:
==2332528==ERROR: AddressSanitizer: SEGV on unknown address (pc 0x58b62c68028e bp 0x7ffe27c5b0f0 sp 0x7ffe27c5b0d0 T0)
==2332528==The signal is caused by a READ memory access.
==2332528==Hint: this fault was caused by a dereference of a high value address (see register values below).  Disassemble the provided pc to learn which register was used.
    #0 0x58b62c68028e in v8::internal::TracedHandles::UpdateListOfYoungNodes() v8/src/heap/memory-chunk.h:344:12
    #1 0x58b62cb26431 in v8::internal::ScavengerCollector::CollectGarbage() v8/src/heap/scavenger.cc:1883:30
    #2 0x58b62c8c753f in v8::internal::Heap::Scavenge() v8/src/heap/heap.cc:2685:25
    #3 0x58b62c8c4a0d in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GarbageCollectionReason, char const*) v8/src/heap/heap.cc:2368:5
    #4 0x58b62c919e1e in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags, v8::internal::PerformHeapLimitCheck, v8::internal::PerformIneffectiveMarkCompactCheck)::$_0::operator()() const v8/src/heap/heap.cc:1631:7
    #5 0x58b62c8b9366 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags, v8::internal::PerformHeapLimitCheck, v8::internal::PerformIneffectiveMarkCompactCheck) v8/src/heap/base/stack.h:82:7
    #6 0x58b62c8437bc in v8::internal::HeapAllocator::CollectGarbageAndRetryAllocation(v8::base::FunctionRef<bool ()>, v8::internal::AllocationType, v8::internal::GarbageCollectionReason) v8/src/heap/heap-allocator.cc:550:5
...

UAF:
==2355635==ERROR: AddressSanitizer: heap-use-after-free on address 0x728a9f9f4772 at pc 0x64f9dd7cf693 bp 0x7ffcc007d8b0 sp 0x7ffcc007d8a8
READ of size 2 at 0x728a9f9f4772 thread T0 (chrome)
    #0 0x64f9dd7cf692 in v8::internal::TracedHandles::Destroy(unsigned long*) v8/src/handles/traced-handles.h:42:36
    #1 0x64f9fcbdbeaa in cppgc::internal::FinalizerTrait<blink::ScriptPromiseProperty<blink::IDLUndefined, blink::IDLAny>>::Finalize(void*) v8/include/v8-traced-handle.h:313:3
    #2 0x64f9dfcd8d69 in cppgc::internal::(anonymous namespace)::SweepFinalizer::FinalizePage(cppgc::internal::(anonymous namespace)::SweepingState::SweptPageState*) v8/src/heap/cppgc/sweeper.cc:512:15
    #3 0x64f9dfcd7957 in cppgc::internal::Sweeper::SweeperImpl::Finish() v8/src/heap/cppgc/sweeper.cc:457:7
    #4 0x64f9dfcca6b1 in cppgc::internal::Sweeper::SweeperImpl::FinishIfRunning() v8/src/heap/cppgc/sweeper.cc:1236:7
    #5 0x64f9dd8a5c2a in v8::internal::CppHeap::FinishSweepingIfRunning() v8/src/heap/cppgc-js/cpp-heap.cc:1264:12
...

Full traces as an attachment.


## Attachments

- [harness.html](attachments/harness.html) (text/html, 1.4 KB)
- [serve.py](attachments/serve.py) (text/x-python, 4.7 KB)
- [asan-segv-updatelistofyoungnodes.txt](attachments/asan-segv-updatelistofyoungnodes.txt) (text/plain, 15.1 KB)
- [asan-uaf-destroy.txt](attachments/asan-uaf-destroy.txt) (text/plain, 25.2 KB)
- [poc.html](attachments/poc.html) (text/html, 9.4 KB)
- [Screencast from 2026-04-21 12-15-23.webm](attachments/Screencast from 2026-04-21 12-15-23.webm) (video/webm, 5.7 MB)
- [poc.html](attachments/poc_75782618.html) (text/html, 9.4 KB)
- [poc-minimized.html](attachments/poc-minimized.html) (text/html, 2.0 KB)

## Timeline

### ch...@google.com (2026-04-21)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-21)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### em...@google.com (2026-04-21)

Didn't manage to reproduce this so far. Reporter: can you share any additional details of the setup or improve the POC?

### at...@gmail.com (2026-04-21)

Timing may be tricky. I had hard time trying to minimize the repro, as small changes in the timing resulted in not reproducing.

That PoC had 100% reproduction rate on my two systems, with serve.py defaults. I tested it with Ubuntu 24.04 and 25.10 desktops, running AMD Strix Halo 395+ and AMD Ryzen 5 9600X, but those do have similar single core performance. My fuzzer also detected the issue on AMD EPYC 7502P CPU machine, which has a lot slower cores, so the race is triggable there, but the PoC was not tested there.

The ASAN build was downloaded with get_asan_chrome.py from https://source.chromium.org/chromium/chromium/src/+/main:tools/get_asan_chrome/get_asan_chrome.py

I think I have a laptop with less beefy CPU and Ubuntu installed. I'll check if that requires a different timing and also test on the EPYC server. I'll report with the results.


### at...@gmail.com (2026-04-21)

The poc.html reproduced also on a laptop with AMD Ryzen 5 5625U and Ubuntu 24.04.

Downloaded both .html files and serve.py to a same directory and run python3 serve.py.

Downloaded newest ASAN chromium with get_asan_chrome.py and launched chrome: ./chrome --no-sandbox --disable-in-process-stack-traces --disable-popup-blocking --enable-experimental-web-platform-features --js-flags="--verify-heap" --user-data-dir=/tmp/test-prof "http://127.0.0.1:8080/?close_after=50&time_limit=2000"

 It reproduced on each execution. Attached a video, but there is not much to see.

### at...@gmail.com (2026-04-21)

On EPYC the original poc.html didn't reproduce. Changed the poc.html window.close() timeout to use Math.random()*50 instead of 50 and now it reproduces on each system. Not ideal, but try if you can get it to reproduce with that.

### at...@gmail.com (2026-04-21)

With that Math.random() I got the test case minimized further. Usage is same as with the original poc.html.

Couple of things to notice:
- as the test case reduced, instead of ASAN catching a memory issue, the race started to hit: bad_optional_access was thrown in -fno-exceptions mode
- minimized poc very rarely crashes on UAF.

Let me know, if this and the previous Math.random()*50 versions do not reproduce. Next option is to write a larger python server and harness that would dynamically change the timeout.

### em...@google.com (2026-04-21)

Thanks, I managed to repro using the version from [comment #7](https://issues.chromium.org/issues/504073879#comment7) and `get_asan_chrome.py`; somehow it didn't repro using a locally built Chrome. Let's see if it repros on Clusterfuzz.

### cl...@appspot.gserviceaccount.com (2026-04-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6202814955028480.

### em...@google.com (2026-04-21)

Reproduced using a locally built Chrome as well, using the following GN flags (the last one was the one I was missing initially):

```
dcheck_always_on = false
is_asan = true
is_component_build = false
is_debug = false
target_cpu = "x64"
target_os = "linux"
v8_enable_verify_heap = true

```

### 24...@project.gserviceaccount.com (2026-04-22)

Testcase 6202814955028480 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6202814955028480.

### ml...@google.com (2026-04-22)

Since this is related to ProgrammaticScrollPromise, which is on track for M149 this should be release blocking for that.

### ml...@google.com (2026-04-22)

Reprodces for me, with `dcheck_always_on=true`, I see

```
$ out/Release/chrome --headless  --no-sandbox --disable-in-process-stack-traces --disable-popup-blocking --enable-experimental-web-platform-features --js-flags=--verify-heap "http://127.0.0.1:8080/?close_after=30&time_limit=2000"                                                                                                    
[1001617:1001617:0422/081304.218763:ERROR:ui/base/cursor/cursor_factory.cc:97] Not implemented reached in virtual void ui::CursorFactory::ObserveThemeChanges().
WARN: SystemInfo_vulkan.cpp:197 (HasKhronosValidationLayer): Vulkan validation layers are missing
[1001734:1001753:0422/081304.672786:ERROR:gpu/ipc/client/command_buffer_proxy_impl.cc:285] ContextResult::kTransientFailure: Failed to send GpuControl.CreateCommandBuffer.
[1001734:1001753:0422/081304.672970:ERROR:services/viz/public/cpp/gpu/context_provider_command_buffer.cc:264] GpuChannelHost failed to create command buffer.


#
# Fatal error in ../../v8/src/heap/heap-allocator-inl.h, line 79
# Debug check failed: AllowHeapAllocation::IsAllowed().
#
#
#
#FailureMessage Object: 0x7ffc848c4470#0 0x55e31ea12892 base::debug::CollectStackTrace()
#1 0x55e31e9f9bc1 base::debug::StackTrace::StackTrace()
#2 0x55e32130c4fd gin::(anonymous namespace)::PrintStackTrace()
#3 0x55e320c1d9b3 V8_Fatal()
#4 0x55e320c1d3c5 v8::base::(anonymous namespace)::DefaultDcheckHandler()
#5 0x55e3180818dd v8::internal::HeapAllocator::AllocateRaw<>()
#6 0x55e318054c58 v8::internal::Factory::AllocateRawWithAllocationSite()
#7 0x55e31805d65e v8::internal::Factory::NewJSObjectFromMap()
#8 0x55e31865f2e5 v8::internal::DictionaryTemplateInfo::NewInstance()
#9 0x55e317c1d3a1 v8::DictionaryTemplate::NewInstance()
#10 0x55e324a0871c blink::bindings::DictionaryBase::ToV8()
#11 0x55e3235ab3e5 blink::ScriptPromiseResolverBase::ResolveOrReject<>()
#12 0x55e3236bf88c blink::ScrollPromiseResolver::ActiveScrollTrackerRemoved()
#13 0x55e32447af27 base::internal::Invoker<>::RunOnce()
#14 0x55e3161d8ef7 base::OnceCallback<>::Run()
#15 0x55e323626b40 blink::ThreadCheckingCallbackWrapper<>::Run()
#16 0x55e3161d8ef7 base::OnceCallback<>::Run()
#17 0x55e32447d0e4 blink::ProgrammaticScrollAnimator::~ProgrammaticScrollAnimator()
#18 0x55e3190d9206 cppgc::internal::(anonymous namespace)::SweepFinalizer::FinalizePage()
#19 0x55e3190d8de1 cppgc::internal::(anonymous namespace)::SweepFinalizer::Finalize()
#20 0x55e3190d8892 cppgc::internal::Sweeper::SweeperImpl::Finish()
#21 0x55e3190d4af1 cppgc::internal::Sweeper::SweeperImpl::FinishIfRunning()
#22 0x55e31802a2f5 v8::internal::CppHeap::FinishSweepingIfRunning()
#23 0x55e3180f65ab v8::internal::Heap::EnsureSweepingCompleted()
#24 0x55e3180f5d52 v8::internal::Heap::CompleteSweepingFull()
#25 0x55e3180f6eda v8::internal::Heap::PerformGarbageCollection()
#26 0x55e31811fc6f v8::internal::Heap::CollectGarbage()::$_0::operator()()
#27 0x55e31811f84f heap::base::Stack::SetMarkerAndCallbackImpl<>()
#28 0x55e3190df78b PushAllRegistersAndIterateStack
#29 0x55e3180f3050 v8::internal::Heap::CollectGarbage()
#30 0x55e3180a10a4 v8::internal::HeapAllocator::CollectGarbageAndRetryAllocation()
#31 0x55e3180a0642 v8::internal::HeapAllocator::RetryCustomAllocateOrFail()
#32 0x55e3180a0452 v8::internal::HeapAllocator::AllocateRawSlowPath()
#33 0x55e318054f94 v8::internal::Factory::NewFillerObject()
#34 0x55e3187f48bd v8::internal::__RT_impl_Runtime_AllocateInYoungGeneration()
#35 0x55e3187f4540 v8::internal::Runtime_AllocateInYoungGeneration()
#36 0x55e31a4533fd Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit

```

### ml...@google.com (2026-04-22)

Oilpan destructors must not run JavaScript. Resolving a promise executes JavaScript.

On the Oilpan side we can make sanitization scopes more agressive to avoid relying on garbage collection stress modes.

Trying to triage this properly now.

### ml...@google.com (2026-04-22)

mustaq: As feature owner, can you take a look. This is a memory corruption that should be launch blocking.

We cannot execute JavaScript from `~ProgrammaticScrollAnimator()`.

### mu...@chromium.org (2026-04-22)

[mlippautz@google.com](mailto:mlippautz@google.com): I need some details about this:

> Oilpan destructors must not run JavaScript. Resolving a promise executes JavaScript.

When JS is waiting for a promise to resolve but then destroys some part of the DOM which is in charge of resolving the promise (a `ScrollableArea` in case of the stack trace in [Comment #14](https://issues.chromium.org/issues/504073879#comment14)), the promise still needs to be handled somehow, right? I don't see why this is a problem unique to scroll-promises, wondering what I missed here! Maybe there is a "standard" way to take care of such promises?

### fl...@google.com (2026-04-22)

I think we need to do something similar to Animation::ResolvePromiseMaybeAsync, where if we're in a state where script is not currently allowed we schedule a task to resolve the promise at the next opportunity.

### mu...@chromium.org (2026-04-22)

deleted

### ml...@google.com (2026-04-23)

Thanks for jumping in here! +caseq who also has experience with Promises and V8.

### ca...@google.com (2026-04-23)

I think the problem starts here: <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/scroll/programmatic_scroll_animator.cc;l=23;drc=c0f23dc884b194c040601b8e4248919106bcbf20;bpv=1;bpt=1>

Invoking callbacks from the destructor of a GC'ed class doesn't look safe.

### mu...@chromium.org (2026-04-24)

It seems moving the promise-resolver call from the destructor to a pre-finalizer didn't help, at least for the single successful repro I had since my change. Right now I am unable to repro with or without my change, so trying to guess my next steps :|

### mu...@chromium.org (2026-04-24)

[caseq@google.com](mailto:caseq@google.com): Any chance we don't have a `ScriptForbiddenScope` created during oilpan destruction? When the bug reproduces, it didn't hit [this CHECK](https://chromium-review.git.corp.google.com/c/chromium/src/+/7794088/comment/74b5bc7f_b5e499b4/) but failed elsewhere.

### ml...@google.com (2026-04-27)

1. Pre-finalizers are not allowed to allocate. They may reach through the object graph to otherwise dead objects though.
2. Finalizers are allowed to allocate on Oilpan. They must not reach through the object graph.

This should allow for modeling something that reaches through the graph and allocates if absolutely necessary. Both concepts have performance implications.

1. - 2. are never allowed to execute JavaScript and thus are also never allowed to allocate on the JavaScript heap.

We have scopes in place to catch these but have some gaps in terms where these checks are. We will improve these as part of this bug.

### mu...@chromium.org (2026-04-29)

This [change (PS4)](https://chromium-review.git.corp.google.com/c/chromium/src/+/7794088/4) has no calls left to resolve the promise, and still gives me the exact same error with v8 allocation:

```
#
# Fatal error in ../../v8/src/heap/heap-allocator-inl.h, line 79
# Debug check failed: AllowHeapAllocation::IsAllowed().
#

```

### mu...@chromium.org (2026-04-29)

Finally, a one line change with an empty dtor body as follows produces the same v8 allocation problem, and this confirms that the problem lies elsewhere.

```
ProgrammaticScrollAnimator::~ProgrammaticScrollAnimator() = default;

```

Assigning the bug to [mlippautz@google.com](mailto:mlippautz@google.com): I don't get a symbolized stack trace like your [Comment #14](https://issues.chromium.org/issues/504073879#comment14), so can't investigate further.

Here is my repro details: I ran the original repro steps but with the minimized html in [Comment #8](https://issues.chromium.org/issues/504073879#comment8). My asan build doesn't give me a symbolized stack trace, and a build with `is_debug = true` fails. Here is my gn args:

```
dcheck_always_on = true
is_asan = true
is_component_build = false
is_debug = false
target_cpu = "x64"
target_os = "linux"
v8_enable_verify_heap = true

```

### ml...@google.com (2026-04-29)

> My asan build doesn't give me a symbolized stack trace, and a build with is\_debug = true fails.

What does this mean? A build fails? This is a regular debug config that should work and give you a stack trace.

We can certainly help with GC problems but at this point it's unclear what you are running and what you expect.

E.g., [comment #25](https://issues.chromium.org/issues/504073879#comment25) still shows a destructor that executes callbacks that can certainly fail.

### mu...@chromium.org (2026-04-29)

> What does this mean? A build fails? This is a regular debug config that should work and give you a stack trace.

Yes, unfortunately...a linker failure with my ASAN build that I didn't dig into.

[mlippautz@google.com](mailto:mlippautz@google.com): By "regular", did you mean the bug reproduced for you w/o ASAN?

> E.g., [comment #25](https://issues.chromium.org/issues/504073879#comment25) still shows a destructor that executes callbacks that can certainly fail.

We (vmpstr@ and I) concluded the same right after my comment above and found a way forward.

### ml...@google.com (2026-04-30)

These DCHECK failures have nothing to do with ASAN. So all of this should reproduce also on a regular debug build as well.

### mu...@chromium.org (2026-04-30)

Thanks mlippautz@ for confirming that this reproduces w/o ASAN. Having the symbolized stack trace helps a lot:

The root cause of the problem is that the Document associated with the ProgrammaticScrollAnimator is gone when ~ProgrammaticScrollAnimator() is called, or even when it is getting pre-finalized in [this patch](https://chromium-review.git.corp.google.com/c/chromium/src/+/7794088/6/third_party/blink/renderer/core/scroll/programmatic_scroll_animator.cc#39). So our attempt to postTask has been failing trivially all along.

### mu...@chromium.org (2026-05-01)

We found a solution, yayy. We confirmed (through [this CL](https://chromium-review.git.corp.google.com/c/chromium/src/+/7808036)) that the `ScrollCallback` run at `~ProgrammaticScrollAnimator()` is not used in practice, which makes perfect sense for this garbage-collected class. So it is okay to skip Promise resolution there if we can handle the multi-scroller case (with `elem.scrollIntoView`) carefully.

### dx...@google.com (2026-05-06)

Project: chromium/src  

Branch:  main  

Author:  Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:    <https://chromium-review.googlesource.com/7823183>

Avoid Promise handling at GC by deferring the handling to a post-task.

---


Expand for full commit details
```
     
    This CL fixes the UAF bug by deferring promise resolution to a 
    post-task. This correctly handles pending promises even when 
    ProgrammaticScrollAnimator is getting garbage-collected. In 
    particular, if the execution context is removed, we are skipping the 
    resolution because JS can't be waiting on the promise. 
     
    This also adds an internal GC test that reproduces the bug (to be 
    precise, crashes) without the fix here. 
     
    Fixed: 504073879 
    Bug: 41406914 
    Change-Id: I1f6a4d3d83eb3945f8b1f1803949e76b4e8d037f 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7823183 
    Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1626423}

```

---

Files:

- M `third_party/blink/renderer/core/scroll/programmatic_scroll_animator.cc`
- M `third_party/blink/renderer/core/scroll/programmatic_scroll_animator.h`
- M `third_party/blink/renderer/core/scroll/scroll_promise_resolver.h`
- M `third_party/blink/web_tests/cssom/scroll-promise-after-gc.html`

---

Hash: [962d47a2214fd831399abf703ca73e3f7a23808f](https://chromiumdash.appspot.com/commit/962d47a2214fd831399abf703ca73e3f7a23808f)  

Date: Wed May 6 20:34:05 2026


---

### ch...@google.com (2026-05-06)

**M149** merge request created. **Please update [crbug/510437254](https://crbug.com/510437254) to have this merge reviewed.**

### dx...@google.com (2026-05-07)

Project: chromium/src  

Branch:  refs/branch-heads/7827  

Author:  Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:    <https://chromium-review.googlesource.com/7828804>

[M149] Avoid Promise handling at GC by deferring the handling to a post-task.

---


Expand for full commit details
```
     
    Original change's description: 
    > Avoid Promise handling at GC by deferring the handling to a post-task. 
    > 
    > This CL fixes the UAF bug by deferring promise resolution to a 
    > post-task. This correctly handles pending promises even when 
    > ProgrammaticScrollAnimator is getting garbage-collected. In 
    > particular, if the execution context is removed, we are skipping the 
    > resolution because JS can't be waiting on the promise. 
    > 
    > This also adds an internal GC test that reproduces the bug (to be 
    > precise, crashes) without the fix here. 
    > 
    > Fixed: 504073879 
    > Bug: 41406914 
    > Change-Id: I1f6a4d3d83eb3945f8b1f1803949e76b4e8d037f 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7823183 
    > Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
    > Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1626423} 
     
    (cherry picked from commit 962d47a2214fd831399abf703ca73e3f7a23808f) 
     
    Bug: 510437254,504073879,41406914 
    Change-Id: I1f6a4d3d83eb3945f8b1f1803949e76b4e8d037f 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7828804 
    Commit-Queue: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7827@{#146} 
    Cr-Branched-From: 9f3e9aaccba63bd2ec30334e45e0bfd07ebcc8f1-refs/heads/main@{#1625079}

```

---

Files:

- M `third_party/blink/renderer/core/scroll/programmatic_scroll_animator.cc`
- M `third_party/blink/renderer/core/scroll/programmatic_scroll_animator.h`
- M `third_party/blink/renderer/core/scroll/scroll_promise_resolver.h`
- M `third_party/blink/web_tests/cssom/scroll-promise-after-gc.html`

---

Hash: [4b53542fc783152f88cb8fcf7e2d111ae8077ca6](https://chromiumdash.appspot.com/commit/4b53542fc783152f88cb8fcf7e2d111ae8077ca6)  

Date: Thu May 7 20:17:12 2026


---

### pe...@google.com (2026-05-07)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### sp...@google.com (2026-05-13)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
High quality. Renderer RCE / memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### qk...@google.com (2026-06-08)

Add the `LTS-NotApplicable-144` label because M144 does not contain the target file that the fix should modify.

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/504073879)*
