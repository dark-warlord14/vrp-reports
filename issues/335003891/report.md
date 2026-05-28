# Use-after-poison in blink::LocalDOMWindow::Trace

| Field | Value |
|-------|-------|
| **Issue ID** | [335003891](https://issues.chromium.org/issues/335003891) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Media>PictureInPicture |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 123.0.0.0 |
| **Reporter** | ki...@gmail.com |
| **Assignee** | st...@chromium.org |
| **Created** | 2024-04-16 |
| **Bounty** | $3,000.00 |

## Description

# Steps to reproduce the problem

FUZZBUILD COMMIT (NOT BISECTION)

```
commit 0024113cb6aac52353cff60e017cc4d2b0394b3c (HEAD -> main, origin/main, origin/HEAD)
Author: Marc Treib <treib@chromium.org>
Date:   Fri Apr 12 13:19:51 2024 +0000

    Sync: Fix CHECK crash in DataTypeManagerImpl

    DataTypeManagerImpl::OnAllDataTypesReadyForConfigure() contains a CHECK
    that ensure the `configurer_` is set, which is more or less equivalent
    to not being in the STOPPED state.
    It turns out there was a situation where such a call could happen while
    stopped: If a configuration attempt is abandoned before finishing, a
    timeout timer in ModelLoadManager would still trigger, leading to the
    unexpected call.

    This CL contains two fixes, each of which independently prevent the
    crash:
    1) Stop the timeout timer in ModelLoadManager::Stop().
    2) Also in ModelLoadManager::Stop(), reset
       notified_about_ready_for_configure_.

    Bug: 333865298, 40901755
    Change-Id: I2c2a3c2e44532d41068cd68ccbda0d2268352f58
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5444756
    Commit-Queue: Marc Treib <treib@chromium.org>
    Reviewed-by: Mikel Astiz <mastiz@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1286436}


```

1. git checkout 0024113cb6aac52353cff60e017cc4d2b0394b3c
2. git apply patch.diff
3. gclient sync && gn gen .\out\asan-release && ninja -C .\out\asan-release chrome
4. extract resources.zip, cd into it and run `python3 -m http.server 8888`
5. create another powershell and run following command:
   
   ```
   \path\to\chromium\src\out\asan-release\chrome.exe --user-data-dir=.\uap-userdata --no-sandbox --no-user-gesture-required  --use-fake-ui-for-media-stream --enable-logging=stderr --deny-permission-prompts http://127.0.0.1:8888/fuzz-4-15_21-56-45-697521-testcase.html
   
   ```
   
   The log of execution is also attached below.

# Problem Description

This vulnerability can trigger different types of asan logs, all of which I've posted on the attachment.

# Summary

Use-after-poison in blink::LocalDOMWindow::Trace

# Custom Questions

#### Type of crash:

tab

#### Crash state:

=================================================================
==71920==ERROR: AddressSanitizer: use-after-poison on address 0x7ec70027d2b4 at pc 0x7ffb64e8b16a bp 0x003180ff9b00 sp 0x003180ff9b48
READ of size 4 at 0x7ec70027d2b4 thread T0
#0 0x7ffb64e8b169 in blink::LocalDOMWindow::Trace D:\project\chromium\src\third\_party\blink\renderer\core\frame\local\_dom\_window.cc:2386
#1 0x7ffb53087339 in cppgc::internal::MarkerBase::ProcessWorklistsWithDeadline D:\project\chromium\src\v8\src\heap\cppgc\marker.cc:654
#2 0x7ffb5308455c in cppgc::internal::MarkerBase::AdvanceMarkingWithLimits D:\project\chromium\src\v8\src\heap\cppgc\marker.cc:580
#3 0x7ffb5110b903 in v8::internal::CppHeap::AdvanceTracing D:\project\chromium\src\v8\src\heap\cppgc-js\cpp-heap.cc:812
#4 0x7ffb51291741 in v8::internal::IncrementalMarking::EmbedderStep D:\project\chromium\src\v8\src\heap\incremental-marking.cc:560
#5 0x7ffb51294084 in v8::internal::IncrementalMarking::Step D:\project\chromium\src\v8\src\heap\incremental-marking.cc:893
#6 0x7ffb512937fe in v8::internal::IncrementalMarking::AdvanceAndFinalizeIfComplete D:\project\chromium\src\v8\src\heap\incremental-marking.cc:744
#7 0x7ffb51288e39 in v8::internal::IncrementalMarkingJob::Task::RunInternal D:\project\chromium\src\v8\src\heap\incremental-marking-job.cc:137
#8 0x7ffb6e003067 in base::internal::Invoker<base::internal::FunctorTraits<void (v8::Task::*&&)(),std::\_\_Cr::unique\_ptr<v8::Task,std::\_\_Cr::default\_delete[v8::Task](javascript:void(0);) > &&>,base::internal::BindState<1,1,0,void (v8::Task::*)(),std::\_\_Cr::unique\_ptr<v8::Task,std::\_\_Cr::default\_delete[v8::Task](javascript:void(0);) > >,void ()>::RunOnce D:\project\chromium\src\base\functional\bind\_internal.h:980
#9 0x7ffbaa92a7a0 in base::TaskAnnotator::RunTaskImpl D:\project\chromium\src\base\task\common\task\_annotator.cc:203
#10 0x7ffbaa9a1a46 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl D:\project\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:473
#11 0x7ffbaa9a0969 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork D:\project\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:338
#12 0x7ffbaa7f329e in base::MessagePumpDefault::Run D:\project\chromium\src\base\message\_loop\message\_pump\_default.cc:40
#13 0x7ffbaa9a364c in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run D:\project\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:644
#14 0x7ffbaa8a9130 in base::RunLoop::Run D:\project\chromium\src\base\run\_loop.cc:134
#15 0x7ffb895c91c4 in content::RendererMain D:\project\chromium\src\content\renderer\renderer\_main.cc:368
#16 0x7ffb899939ba in content::RunOtherNamedProcessTypeMain D:\project\chromium\src\content\app\content\_main\_runner\_impl.cc:770
#17 0x7ffb89996190 in content::ContentMainRunnerImpl::Run D:\project\chromium\src\content\app\content\_main\_runner\_impl.cc:1145
#18 0x7ffb8999175f in content::RunContentProcess D:\project\chromium\src\content\app\content\_main.cc:329
#19 0x7ffb89992130 in content::ContentMain D:\project\chromium\src\content\app\content\_main.cc:342
#20 0x7ffb95711767 in ChromeMain D:\project\chromium\src\chrome\app\chrome\_main.cc:192
#21 0x7ff7bb3a3be3 in MainDllLoader::Launch D:\project\chromium\src\chrome\app\main\_dll\_loader\_win.cc:180
#22 0x7ff7bb3a1d93 in main D:\project\chromium\src\chrome\app\chrome\_exe\_main\_win.cc:350
#23 0x7ff7bb53d9f3 in \_\_scrt\_common\_main\_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288
#24 0x7ffbfac67033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)
#25 0x7ffbfcbe2650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

Address 0x7ec70027d2b4 is a wild pointer inside of access range of size 0x000000000004.
SUMMARY: AddressSanitizer: use-after-poison D:\project\chromium\src\third\_party\blink\renderer\core\frame\local\_dom\_window.cc:2386 in blink::LocalDOMWindow::Trace
Shadow bytes around the buggy address:
0x7ec70027d000: f7 f7 00 00 00 00 00 00 00 00 00 00 00 00 00 00
0x7ec70027d080: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 f7
0x7ec70027d100: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
0x7ec70027d180: f7 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
0x7ec70027d200: 00 00 00 00 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
=>0x7ec70027d280: f7 f7 f7 f7 f7 f7[f7]f7 f7 f7 f7 f7 f7 f7 f7 f7
0x7ec70027d300: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
0x7ec70027d380: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
0x7ec70027d400: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
0x7ec70027d480: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
0x7ec70027d500: f7 f7 f7 f7 f7 f7 f7 00 00 00 00 00 00 00 00 00
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

==71920==ADDITIONAL INFO

==71920==Note: Please include this section with the ASan report.
Task trace:
#0 0x7ffb6dfeaf23 in gin::V8ToBaseLocation D:\project\chromium\src\gin\converter.cc:291
#1 0x7ffb6dfeaf23 in gin::V8ToBaseLocation D:\project\chromium\src\gin\converter.cc:291
#2 0x7ffb6dfeaf23 in gin::V8ToBaseLocation D:\project\chromium\src\gin\converter.cc:291
#3 0x7ffb6dfeaf23 in gin::V8ToBaseLocation D:\project\chromium\src\gin\converter.cc:291

==71920==END OF ADDITIONAL INFO
==71920==ABORTING

#### Reporter credit:

Zhenghang Xiao (@Kipreyyy)

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [asan_of_accessviolate1.txt](attachments/asan_of_accessviolate1.txt) (text/plain, 4.8 KB)
- [asan_of_accessviolate2.txt](attachments/asan_of_accessviolate2.txt) (text/plain, 12.2 KB)
- [asan_of_uap.txt](attachments/asan_of_uap.txt) (text/plain, 6.0 KB)
- [execution_log.txt](attachments/execution_log.txt) (text/plain, 17.9 KB)
- [fuzz-4-15_21-56-45-697521-testcase.html](attachments/fuzz-4-15_21-56-45-697521-testcase.html) (text/html, 1019.8 KB)
- [patch.diff](attachments/patch.diff) (text/x-diff, 1.6 KB)
- [resources.zip](attachments/resources.zip) (application/zip, 2.0 MB)
- [repro.mp4](attachments/repro.mp4) (video/mp4, 11.3 MB)

## Timeline

### ki...@gmail.com (2024-04-17)

Repro video is attached below.

### ma...@google.com (2024-04-17)

Thanks for the report.

From looking at the stack traces, this looks V8 GC related. Over to V8 sheriff for triage. (Severity and FoundIn set provisionally.)

### pe...@google.com (2024-04-18)

Setting milestone because of s0/s1 severity.

### ki...@gmail.com (2024-04-19)

hello，any update？

### ml...@chromium.org (2024-04-19)

This is very likely *not* an actual garbage collection bug but somewhere an issue in Blink.

From the `asan_*.txt` files it looks like the GC is crashing on different fields. This suggests that this is a uaf of `LocalDOMWindow` which would mean that a previous GC already reclaimed that object.

The commit looks innocent, so we probably need to investigate this properly and see where the actual issue is.

Will try to reproduce locally which is necessary in this case.

### ml...@chromium.org (2024-04-19)

Managed to reproduce on Linux.

Stack:

```
    #0 0x55a5f25c3866 in ___interceptor_backtrace /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4364:13
    #1 0x55a60481eb98 in base::debug::CollectStackTrace(void const**, unsigned long) ./../../base/debug/stack_trace_posix.cc:1039:7
    #2 0x55a6047e6a07 in StackTrace ./../../base/debug/stack_trace.cc:236:20
    #3 0x55a6047e6a07 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:231:28
    #4 0x55a60481de86 in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) ./../../base/debug/stack_trace_posix.cc:457:3
    #5 0x7fabc4c5a510 in __GI___sigaction :?
    #6 0x55a5f8094c2f in __cxx_atomic_load<unsigned short> ./../../third_party/libc++/src/include/__atomic/cxx_atomic_impl.h:342:10
    #7 0x55a5f8094c2f in load ./../../third_party/libc++/src/include/__atomic/atomic_base.h:60:12
    #8 0x55a5f8094c2f in LoadEncoded<(cppgc::internal::AccessMode)1, (cppgc::internal::HeapObjectHeader::EncodedHalf)1, (std::__Cr::memory_order)2> ./../../v8/src/heap/cppgc/heap-object-header.h:355:40
    #9 0x55a5f8094c2f in IsInConstruction<(cppgc::internal::AccessMode)1> ./../../v8/src/heap/cppgc/heap-object-header.h:260:7
    #10 0x55a5f8094c2f in MarkAndPush ./../../v8/src/heap/cppgc/marking-state.h:77:14
    #11 0x55a5f8094c2f in MarkAndPush ./../../v8/src/heap/cppgc/marking-state.h:68:3
    #12 0x55a5f8094c2f in v8::internal::UnifiedHeapMarkingVisitorBase::Visit(void const*, cppgc::TraceDescriptor) ./../../v8/src/heap/cppgc-js/unified-heap-marking-visitor.cc:41:18
    #13 0x55a610fcdd55 in TraceImpl<blink::ScriptController> ./../../v8/include/cppgc/visitor.h:422:5
    #14 0x55a610fcdd55 in Trace<blink::ScriptController> ./../../v8/include/cppgc/visitor.h:77:5
    #15 0x55a610fcdd55 in blink::LocalDOMWindow::Trace(cppgc::Visitor*) const ./../../third_party/blink/renderer/core/frame/local_dom_window.cc:2386:12
    #16 0x55a5f9ea5986 in operator() ./../../v8/src/heap/cppgc/marker.cc:663:17
    #17 0x55a5f9ea5986 in DrainWorklistWithPredicate<150UL, heap::base::Worklist<cppgc::TraceDescriptor, (unsigned short)512>::Local, (lambda at ../../v8/src/heap/cppgc/marker.cc:657:15), (lambda at ../../v8/src/heap/cppgc/marker.cc:69:7)> ./../../v8/src/heap/cppgc/marking-state.h:487:5
    #18 0x55a5f9ea5986 in DrainWorklistWithBytesAndTimeDeadline<150UL, heap::base::Worklist<cppgc::TraceDescriptor, (unsigned short)512>::Local, (lambda at ../../v8/src/heap/cppgc/marker.cc:657:15)> ./../../v8/src/heap/cppgc/marker.cc:68:10
    #19 0x55a5f9ea5986 in cppgc::internal::MarkerBase::ProcessWorklistsWithDeadline(unsigned long, v8::base::TimeTicks) ./../../v8/src/heap/cppgc/marker.cc:654:12
    #20 0x55a5f9ea2980 in cppgc::internal::MarkerBase::AdvanceMarkingWithLimits(v8::base::TimeDelta, unsigned long) ./../../v8/src/heap/cppgc/marker.cc:580:15
    #21 0x55a5f807eed8 in v8::internal::CppHeap::AdvanceTracing(v8::base::TimeDelta) ./../../v8/src/heap/cppgc-js/cpp-heap.cc:812:16
    #22 0x55a5f81be07b in v8::internal::IncrementalMarking::EmbedderStep(v8::base::TimeDelta) ./../../v8/src/heap/incremental-marking.cc:560:13
    #23 0x55a5f81c0983 in v8::internal::IncrementalMarking::Step(v8::base::TimeDelta, unsigned long, v8::internal::StepOrigin) ./../../v8/src/heap/incremental-marking.cc:893:25
    #24 0x55a5f81c00fd in v8::internal::IncrementalMarking::AdvanceAndFinalizeIfComplete() ./../../v8/src/heap/incremental-marking.cc:744:3
    #25 0x55a5f81b603e in v8::internal::IncrementalMarkingJob::Task::RunInternal() ./../../v8/src/heap/incremental-marking-job.cc:137:34
    #26 0x55a60b8ea5b5 in Invoke<void (v8::Task::*)(), std::__Cr::unique_ptr<v8::Task, std::__Cr::default_delete<v8::Task> > > ./../../base/functional/bind_internal.h:738:12
    #27 0x55a60b8ea5b5 in MakeItSo<void (v8::Task::*)(), std::__Cr::tuple<std::__Cr::unique_ptr<v8::Task, std::__Cr::default_delete<v8::Task> > > > ./../../base/functional/bind_internal.h:930:12
    #28 0x55a60b8ea5b5 in RunImpl<void (v8::Task::*)(), std::__Cr::tuple<std::__Cr::unique_ptr<v8::Task, std::__Cr::default_delete<v8::Task> > >, 0UL> ./../../base/functional/bind_internal.h:1067:14
    #29 0x55a60b8ea5b5 in base::internal::Invoker<base::internal::FunctorTraits<void (v8::Task::*&&)(), std::__Cr::unique_ptr<v8::Task, std::__Cr::default_delete<v8::Task>>&&>, base::internal::BindState<true, true, false, void (v8::Task::*)(), std::__Cr::unique_ptr<v8::Task, std::__Cr::default_delete<v8::Task>>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:980:12
    #30 0x55a60469b125 in Run ./../../base/functional/callback.h:156:12
    #31 0x55a60469b125 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:203:34
    #32 0x55a6046fcda5 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:11)> ./../../base/task/common/task_annotator.h:90:5
    #33 0x55a6046fcda5 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:473:23
    #34 0x55a6046fbcbe in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:338:40
    #35 0x55a6046fdadb in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #36 0x55a6045916fe in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:40:55
    #37 0x55a6046fe6f7 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:644:12
    #38 0x55a60462b250 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #39 0x55a61bb88af4 in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:368:16
    #40 0x55a601db519a in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:675:14
    #41 0x55a601db66ef in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:779:12
    #42 0x55a601db9242 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1145:10
    #43 0x55a601db34c1 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:329:36
    #44 0x55a601db3b3c in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:342:10
    #45 0x55a5f26530f9 in ChromeMain ./../../chrome/app/chrome_main.cc:192:12
    #46 0x7fabc4c456ca in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #47 0x7fabc4c45785 in __libc_start_main ./csu/../csu/libc-start.c:360:3
    #48 0x55a5f257f02a in _start ??:0:0

```

### ml...@chromium.org (2024-04-19)

I see that the GC processes a `LocalDOMWindow` that was never created. Using `rr` on content\_shell I found that we `DOMWindow` in question is actually a `RemoteDOMWindow`.

So somewhere along the way, currently it looks like in PiP code, we confuse a `RemoteDOMWindow` as `LocalDOMWindow` and store that in a `Member`. The GC then trips over the type confusion.

The GC finds the broken `LocalDOMWindow` in `DocumentPictureInPictureEvent::document_picture_in_picture_window_` [1](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/document_picture_in_picture/document_picture_in_picture_event.h;l=36;drc=42debe0b0e6bf90175dd0d121eb0e7dc11a6d29c;bpv=1;bpt=1):

### ml...@chromium.org (2024-04-19)

Alright, the issue is indeed DocumentPictureInPictureEvent::document\_picture\_in\_picture\_window\_ [2](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/document_picture_in_picture/document_picture_in_picture_event.h;l=36;drc=42debe0b0e6bf90175dd0d121eb0e7dc11a6d29c;bpv=1;bpt=1). There's a static cast to `LocalDOMWindow` on construction [3](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/document_picture_in_picture/document_picture_in_picture_event.cc;l=37;drc=42debe0b0e6bf90175dd0d121eb0e7dc11a6d29c;bpv=1;bpt=1). In the repro case this is a `RemoteDOMWindow`. The GC just trips over this during marking because the types and payloads don't match up.

This would have been easily caught with `To<LocalDOMWindow>()` which emits a `CHECK` before the call. Even years ago this would have been a DCHECK already and helped diagnosing this much more quickly.

```
diff --git a/third_party/blink/renderer/modules/document_picture_in_picture/document_picture_in_picture_event.cc b/third_party/blink/renderer/modules/document_picture_in_picture/document_picture_in_picture_event.cc
index 037813c62c2f0..79d4c24fcbf04 100644
--- a/third_party/blink/renderer/modules/document_picture_in_picture/document_picture_in_picture_event.cc
+++ b/third_party/blink/renderer/modules/document_picture_in_picture/document_picture_in_picture_event.cc
@@ -34,7 +34,7 @@ DocumentPictureInPictureEvent::DocumentPictureInPictureEvent(
     const DocumentPictureInPictureEventInit* initializer)
     : Event(type, initializer),
       document_picture_in_picture_window_(
-          static_cast<LocalDOMWindow*>(initializer->window())) {}
+          To<LocalDOMWindow>(initializer->window())) {}
 
 void DocumentPictureInPictureEvent::Trace(Visitor* visitor) const {
   visitor->Trace(document_picture_in_picture_window_);

```

### ml...@chromium.org (2024-04-19)

fwiw, the code for the wrongly typed pointer was added in Nov 2021 here [4](https://chromium-review.googlesource.com/c/chromium/src/+/4036968). I am not sure if there's other guarantees that are violated and we should never arrive with a remote window at event construction.

### ml...@chromium.org (2024-04-19)

Likely related crashes: <https://crash.corp.google.com/browse?q=product_name%3D%27Chrome%27+AND+EXISTS+%28SELECT+1+FROM+UNNEST%28CrashedStackTrace.StackFrame%29+WHERE+FunctionName+LIKE+%27blink%3A%3ALocalDOMWindow%3A%3ATrace%28%25%27%29#samplereports>

### ma...@google.com (2024-04-19)

Thanks a lot for that thorough analysis, mlippautz!

PiP folks, could you PTAL and work on the fix?

(Taking a guess here at the affected OSes. Please adjust if any of these are not actually affected.)

### st...@chromium.org (2024-04-19)

I'm not sure how it ever would be a RemoteDOMWindow, but maybe the fuzzer is breaking assumptions with its `--no-sandbox` flag. Either way I don't think it matters since we don't depend on the fact that it's a LocalDOMWindow, so I'll update this to just store a DOMWindow and I think that should fix the issue. Thanks for the detailed analysis!

### ma...@google.com (2024-04-19)

> maybe the fuzzer is breaking assumptions with its `--no-sandbox` flag

Does this mean you believe the issue to be non-reachable for users running production/release builds without the flag enabled? (If so, we should mark this [Security\_Impact-None](https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/security-labels.md#TOC-Security-Impact-None).)

### ap...@google.com (2024-04-19)

Project: chromium/src
Branch: main

commit 2314741cdf2c4a6e11234dda7006ec0dd9005bbb
Author: Tommy Steimel <steimel@chromium.org>
Date:   Fri Apr 19 19:43:57 2024

    [document pip] Don't assume the enter event window is a LocalDOMWindow
    
    This CL changes DocumentPictureInPictureEvent to store a DOMWindow
    instead of a LocalDOMWindow to prevent crashes when the window it gets
    is actually a RemoteDOMWindow.
    
    Bug: 335003891
    Change-Id: I86a0ec5a89b51a26d5dd89559f86e6e4d6c3e8fe
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5467978
    Commit-Queue: Tommy Steimel <steimel@chromium.org>
    Reviewed-by: Frank Liberato <liberato@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1290122}

M       third_party/blink/renderer/modules/document_picture_in_picture/document_picture_in_picture_event.cc
M       third_party/blink/renderer/modules/document_picture_in_picture/document_picture_in_picture_event.h

https://chromium-review.googlesource.com/5467978


### st...@chromium.org (2024-04-19)

I was thinking that they were somehow managing to get us to create a pip window and fire an enter event to a frame in a different process than the pip window, which I don't think is possible. HOWEVER, I looked at the fuzz testcase and realized that they're actually just creating their own DocumentPictureInPictureEvent and passing in a RemoteDOMWindow, which I had not considered :). So actually you can trivially make this happen via `new DocumentPictureInPictureEvent('enter', {window: my_remote_dom_window});`

### st...@chromium.org (2024-04-19)

but the CL in comment 15 should have fixed this

### pe...@google.com (2024-04-20)

Requesting merge to stable (M124) because latest trunk commit (1290122) appears to be after stable branch point (1274542).
Requesting merge to beta (M125) because latest trunk commit (1290122) appears to be after beta branch point (1287751).
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### pe...@google.com (2024-04-20)

Merge review required: M125 is already shipping to beta.

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
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

### pe...@google.com (2024-04-20)

Merge review required: M124 is already shipping to stable.

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
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

### am...@chromium.org (2024-04-23)

M125 and M124 merge approved for <https://crrev.com/c/5467978>, please merge this fix to M125 Beta / branch 6422 at soonest so this fix can be included in the next Beta update;
please merge this fix to M124 Stable / branch 6367 by EOD Thursday, 25 April so this fix can be included in the next week's M124 Stable update -- thank you!

### ap...@google.com (2024-04-23)

Project: chromium/src
Branch: refs/branch-heads/6422

commit b4d752aad73f482cdea1b44a7a42ad7d8ade2e83
Author: Tommy Steimel <steimel@chromium.org>
Date:   Tue Apr 23 18:59:03 2024

    [M125][document pip] Don't assume the enter event window is a LocalDOMWindow
    
    This CL changes DocumentPictureInPictureEvent to store a DOMWindow
    instead of a LocalDOMWindow to prevent crashes when the window it gets
    is actually a RemoteDOMWindow.
    
    (cherry picked from commit 2314741cdf2c4a6e11234dda7006ec0dd9005bbb)
    
    Bug: 335003891
    Change-Id: I86a0ec5a89b51a26d5dd89559f86e6e4d6c3e8fe
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5467978
    Commit-Queue: Tommy Steimel <steimel@chromium.org>
    Reviewed-by: Frank Liberato <liberato@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1290122}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5478729
    Commit-Queue: Frank Liberato <liberato@chromium.org>
    Auto-Submit: Tommy Steimel <steimel@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6422@{#278}
    Cr-Branched-From: 9012208d0ce02e0cf0adb9b62558627c356f3278-refs/heads/main@{#1287751}

M       third_party/blink/renderer/modules/document_picture_in_picture/document_picture_in_picture_event.cc
M       third_party/blink/renderer/modules/document_picture_in_picture/document_picture_in_picture_event.h

https://chromium-review.googlesource.com/5478729


### pe...@google.com (2024-04-23)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### st...@chromium.org (2024-04-23)

1. Not a regression. This has been in Chrome since M110
2. No

### ap...@google.com (2024-04-23)

Project: chromium/src
Branch: refs/branch-heads/6367

commit 98bcf9ef5cdd3a19f8b739f2cc6b2afdb01b7694
Author: Tommy Steimel <steimel@chromium.org>
Date:   Tue Apr 23 19:29:23 2024

    [M124][document pip] Don't assume the enter event window is a LocalDOMWindow
    
    This CL changes DocumentPictureInPictureEvent to store a DOMWindow
    instead of a LocalDOMWindow to prevent crashes when the window it gets
    is actually a RemoteDOMWindow.
    
    (cherry picked from commit 2314741cdf2c4a6e11234dda7006ec0dd9005bbb)
    
    Bug: 335003891
    Change-Id: I86a0ec5a89b51a26d5dd89559f86e6e4d6c3e8fe
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5467978
    Commit-Queue: Tommy Steimel <steimel@chromium.org>
    Reviewed-by: Frank Liberato <liberato@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1290122}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5477908
    Auto-Submit: Tommy Steimel <steimel@chromium.org>
    Commit-Queue: Frank Liberato <liberato@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6367@{#974}
    Cr-Branched-From: d158c6dc6e3604e6f899041972edf26087a49740-refs/heads/main@{#1274542}

M       third_party/blink/renderer/modules/document_picture_in_picture/document_picture_in_picture_event.cc
M       third_party/blink/renderer/modules/document_picture_in_picture/document_picture_in_picture_event.h

https://chromium-review.googlesource.com/5477908


### pe...@google.com (2024-04-24)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



### vo...@google.com (2024-04-24)

1. <https://crrev.com/c/5481473>
2. Low - small change, no conflicts
3. M124, M125
4. Yes

### am...@google.com (2024-04-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-04-25)

Congratulations kipreyyy! The Chrome VRP Panel has decided to award you $3,000 for this report of a moderately mitigated memory corruption bug in a sandboxed process. Thank you for your efforts and reporting this issue to us!

### ki...@gmail.com (2024-04-26)

Hi, amy, I don't think it's a mitigated problem, because it's not a competition. You only need a simple single sentence call in comment16 to trigger it stably. This is a type confusion problem, and it is not affected by maricle ptr.

### ki...@gmail.com (2024-04-26)

Please watch the reproduce video I provided, which fully proves this. I don't think this security vulnerability has been mitigated in any way. It can be triggered 100% stably.

### ki...@gmail.com (2024-04-26)

In addition, please refer to the multiple asan logs I provided. This problem can even cause segment fault directly on the release, which is obviously not mitigated ：）

### ki...@gmail.com (2024-04-26)

As far as I know, this should be a stable trigger and not mitigated uaf that does not require ui interaction. Please refer to #comment16

### am...@chromium.org (2024-04-26)

Hello Zhenghang Xiao, how this issue manifested in PIP as well as the preconditions of the flags in your original description (--no-user-gesture-required --use-fake-ui-for-media-stream --deny-permission-prompts) suggests this is mitigated. We realize that we can be incorrect here, so we'll consult with steimel@ and the folks that worked on this issue to verify.

More importantly, I should have been more clear in my feedback related to the reward decision in that not only does this issue present as mitigated in a potential real world exploitation scenario (again if we got this incorrect, we are happy to take another look); however, the reward decision was also related this report being presented with an unminimized test case and the amount of effort required on the engineering side to root out the actual issue being presented.

### ki...@gmail.com (2024-04-26)

deleted

### am...@chromium.org (2024-05-01)

Hello Zhenghang Xiao, upon reassessment we have decided that the current reward amount is sufficient for this report. While remote exploitation of this issue could potentially be possible without user interaction, that has not been determined to be the case and is not able to be ascertained based on the information in this report as presented.

Raw testcases over 1 MB in size that are presently directly in the a report and outside of the context of being a part of a fuzzing corpus are not considered to meet the minimized testcase conditions of a baseline VRP report. Also, this does not provide conciseness of data that allows up to reproduce and investigate this issue as present. There was much effort within the engineering teams to sort through and determine the core bug here, and that it was related to PIP.

Report quality and baseline characteristics (<https://g.co/chrome/vrp#report-quality>) have always been a part of VRP reward decisions along with security impact of the bug itself. Simply providing an ASAN stack trace without further information or a test case has considered the minimum for a baseline reward aside from rare exceptions. Based on this, it has been determined that the reward amount -- for a report of below baseline characteristics and mitigated -- is sufficient for this report. Thank you for understanding.

### ki...@gmail.com (2024-05-02)

This sounds a little bad to me. If I can provide a poc less than 1m next time, can it be regarded as a baseline report? I will continue to improve the quality of the report.


### ap...@google.com (2024-05-07)

Project: chromium/src
Branch: refs/branch-heads/6099

commit d0c69e72e0a22bf3b78ea09de6af17120f2b496e
Author: Tommy Steimel <steimel@chromium.org>
Date:   Tue May 07 18:56:27 2024

    [M120-LTS][document pip] Don't assume the enter event window is a LocalDOMWindow
    
    This CL changes DocumentPictureInPictureEvent to store a DOMWindow
    instead of a LocalDOMWindow to prevent crashes when the window it gets
    is actually a RemoteDOMWindow.
    
    (cherry picked from commit 2314741cdf2c4a6e11234dda7006ec0dd9005bbb)
    
    (cherry picked from commit 98bcf9ef5cdd3a19f8b739f2cc6b2afdb01b7694)
    
    Bug: 335003891
    Change-Id: I86a0ec5a89b51a26d5dd89559f86e6e4d6c3e8fe
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5467978
    Commit-Queue: Tommy Steimel <steimel@chromium.org>
    Cr-Original-Original-Commit-Position: refs/heads/main@{#1290122}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5477908
    Auto-Submit: Tommy Steimel <steimel@chromium.org>
    Commit-Queue: Frank Liberato <liberato@chromium.org>
    Cr-Original-Commit-Position: refs/branch-heads/6367@{#974}
    Cr-Original-Branched-From: d158c6dc6e3604e6f899041972edf26087a49740-refs/heads/main@{#1274542}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5481473
    Reviewed-by: Tommy Steimel <steimel@chromium.org>
    Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
    Commit-Queue: Achuith Bhandarkar <achuith@chromium.org>
    Owners-Override: Achuith Bhandarkar <achuith@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6099@{#2012}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

M       third_party/blink/renderer/modules/document_picture_in_picture/document_picture_in_picture_event.cc
M       third_party/blink/renderer/modules/document_picture_in_picture/document_picture_in_picture_event.h

https://chromium-review.googlesource.com/5481473


### pe...@google.com (2024-07-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/335003891)*
