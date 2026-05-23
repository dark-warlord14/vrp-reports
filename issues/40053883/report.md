# Security: heap-buffer-overflow in blink::WebGLRenderingContextBase::MakeXrCompatibleSync

| Field | Value |
|-------|-------|
| **Issue ID** | [40053883](https://issues.chromium.org/issues/40053883) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGL, Blink>WebXR |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ho...@gmail.com |
| **Assignee** | pa...@microsoft.com |
| **Created** | 2020-11-15 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

**VERSION**  

Chrome Version: 89.0.4327.0 (64-bit) + dev (it also fails on the official dev release channel with version 88.0.4315.5 (64bit) + dev)  

Operating System: Linux-4.15.0-112-generic-x86\_64-with-Ubuntu-18.04-bionic

**REPRODUCTION CASE**

<script>
window.addEventListener("load", () => {
(new OffscreenCanvas(2, 2)).getContext("webgl", {"xrCompatible": true})
})
</script>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

=================================================================  

==45837==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x603000014908 at pc 0x56487356278e bp 0x7ffe3e7dd690 sp 0x7ffe3e7dd688  

READ of size 8 at 0x603000014908 thread T0  

#0 0x56487356278d in GetRaw third\_party/blink/renderer/platform/heap/impl/member.h:253  

#1 0x56487356278d in operator bool third\_party/blink/renderer/platform/heap/impl/member.h:183  

#2 0x56487356278d in GetDocument third\_party/blink/renderer/core/dom/tree\_scope.h:84  

#3 0x56487356278d in GetDocument third\_party/blink/renderer/core/dom/node.h:629  

#4 0x56488341dc24 in blink::WebGLRenderingContextBase::MakeXrCompatibleSync(blink::CanvasRenderingContextHost\*) third\_party/blink/renderer/modules/webgl/webgl\_rendering\_context\_base.cc:818  

#5 0x564883287b1e in blink::WebGL2RenderingContext::Factory::Create(blink::CanvasRenderingContextHost\*, blink::CanvasContextCreationAttributesCore const&) third\_party/blink/renderer/modules/webgl/webgl2\_rendering\_context.cc:85  

#6 0x56487d7c5c13 in blink::OffscreenCanvas::GetCanvasRenderingContext(blink::ExecutionContext\*, WTF::String const&, blink::CanvasContextCreationAttributesCore const&) third\_party/blink/renderer/core/offscreencanvas/offscreen\_canvas.cc:327  

#7 0x564880e7d7b8 in blink::OffscreenCanvasModule::getContext(blink::ExecutionContext\*, blink::OffscreenCanvas&, WTF::String const&, blink::CanvasContextCreationAttributesModule const\*, blink::OffscreenCanvasRenderingContext2DOrWebGLRenderingContextOrWebGL2RenderingContextOrImageBitmapRenderingContext&, blink::ExceptionState&) third\_party/blink/renderer/modules/canvas/offscreencanvas/offscreen\_canvas\_module.cc:30  

#8 0x56488076d131 in blink::(anonymous namespace)::GetContextOperationCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) gen/third\_party/blink/renderer/bindings/modules/v8/v8\_offscreen\_canvas.cc:289  

#9 0x56486cbd552f in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api/api-arguments-inl.h:158  

#10 0x56486cbd1758 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:111  

#11 0x56486cbcde68 in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) v8/src/builtins/builtins-api.cc:141  

#12 0x56486cbccf0c in v8::internal::Builtin\_HandleApiCall(int, unsigned long\*, v8::internal::Isolate\*) v8/src/builtins/builtins-api.cc:129  

#13 0x56486f9e3fbe in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_BuiltinExit setup-isolate-deserialize.cc:?  

#14 0x56486f766c2e in Builtins\_InterpreterEntryTrampoline setup-isolate-deserialize.cc:?  

#15 0x56486f75d91a in Builtins\_JSEntryTrampoline setup-isolate-deserialize.cc:?  

#16 0x56486f75d6f7 in Builtins\_JSEntry setup-isolate-deserialize.cc:?  

#17 0x56486cf4efc6 in Call v8/src/execution/simulator.h:142  

#18 0x56486cf4efc6 in Invoke v8/src/execution/execution.cc:368  

#19 0x56486cf4de15 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution/execution.cc:462  

#20 0x56486c9d6031 in v8::Function::Call(v8::Local[v8::Context](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*) v8/src/api/api.cc:4991  

#21 0x56487e60cc84 in blink::V8ScriptRunner::CallFunction(v8::Local[v8::Function](javascript:void(0);), blink::ExecutionContext\*, v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*, v8::Isolate\*) third\_party/blink/renderer/bindings/core/v8/v8\_script\_runner.cc:632  

#22 0x56487e4d5da7 in blink::bindings::CallbackInvokeHelper<blink::CallbackInterfaceBase, (blink::bindings::CallbackInvokeHelperMode)0>::Call(int, v8::Local[v8::Value](javascript:void(0);)\*) third\_party/blink/renderer/bindings/core/v8/callback\_invoke\_helper.cc:129  

#23 0x56487f6a434a in blink::V8EventListener::InvokeWithoutRunnabilityCheck(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::Event\*) gen/third\_party/blink/renderer/bindings/core/v8/v8\_event\_listener.cc:126  

#24 0x56487e4e034d in blink::JSBasedEventListener::Invoke(blink::ExecutionContext\*, blink::Event\*) third\_party/blink/renderer/bindings/core/v8/js\_based\_event\_listener.cc:150  

#25 0x56487b7a89f5 in blink::EventTarget::FireEventListeners(blink::Event&, blink::EventTargetData\*, blink::HeapVector<blink::RegisteredEventListener, 1u>&) third\_party/blink/renderer/core/dom/events/event\_target.cc:937  

#26 0x56487b7a6cee in blink::EventTarget::FireEventListeners(blink::Event&) third\_party/blink/renderer/core/dom/events/event\_target.cc:851  

#27 0x56487befbc73 in blink::LocalDOMWindow::DispatchEvent(blink::Event&, blink::EventTarget\*) third\_party/blink/renderer/core/frame/local\_dom\_window.cc:1853  

#28 0x56487befaf36 in blink::LocalDOMWindow::DispatchLoadEvent() third\_party/blink/renderer/core/frame/local\_dom\_window.cc:1815  

#29 0x56487befa71d in blink::LocalDOMWindow::DispatchWindowLoadEvent() third\_party/blink/renderer/core/frame/local\_dom\_window.cc:659  

#30 0x56487befb3be in blink::LocalDOMWindow::DocumentWasClosed() third\_party/blink/renderer/core/frame/local\_dom\_window.cc:663  

#31 0x56487b58d5ed in blink::Document::ImplicitClose() third\_party/blink/renderer/core/dom/document.cc:3834  

#32 0x56487b58e756 in blink::Document::CheckCompletedInternal() third\_party/blink/renderer/core/dom/document.cc:3947  

#33 0x56487b55f93d in CheckCompleted third\_party/blink/renderer/core/dom/document.cc:3921  

#34 0x56487b55f93d in LoadEventDelayTimerFired third\_party/blink/renderer/core/dom/document.cc:7503  

#35 0x56487efa20da in blink::TimerBase::RunInternal() third\_party/blink/renderer/platform/timer.cc:152  

#36 0x56487efa28a4 in Invoke<void (blink::TimerBase::\*)(), base::WeakPtr[blink::TimerBase](javascript:void(0);)> base/bind\_internal.h:498  

#37 0x56487efa28a4 in MakeItSo<void (blink::TimerBase::\*)(), base::WeakPtr[blink::TimerBase](javascript:void(0);)> base/bind\_internal.h:657  

#38 0x56487efa28a4 in RunImpl<void (blink::TimerBase::\*)(), std::\_\_1::tuple<base::WeakPtr[blink::TimerBase](javascript:void(0);) >, 0> base/bind\_internal.h:710  

#39 0x56487efa28a4 in RunOnce base/bind\_internal.h:679  

#40 0x56486ff2faed in Run base/callback.h:101  

#41 0x56486ff2faed in RunInternal third\_party/blink/renderer/platform/wtf/functional.h:256  

#42 0x56486ff2faed in Run third\_party/blink/renderer/platform/wtf/functional.h:241  

#43 0x564873befb93 in Run base/callback.h:101  

#44 0x564873befb93 in RunTask base/task/common/task\_annotator.cc:163  

#45 0x564873c43be8 in base::sequence\_manager::internal::ThreadControllerImpl::DoWork(base::sequence\_manager::internal::ThreadControllerImpl::WorkType) base/task/sequence\_manager/thread\_controller\_impl.cc:197  

#46 0x564873c48187 in Invoke<void (base::sequence\_manager::internal::ThreadControllerImpl::\*)(base::sequence\_manager::internal::ThreadControllerImpl::WorkType), const base::WeakPtr[base::sequence\_manager::internal::ThreadControllerImpl](javascript:void(0);) &, const base::sequence\_manager::internal::ThreadControllerImpl::WorkType &> base/bind\_internal.h:498  

#47 0x564873c48187 in MakeItSo<void (base::sequence\_manager::internal::ThreadControllerImpl::\*const &)(base::sequence\_manager::internal::ThreadControllerImpl::WorkType), const base::WeakPtr[base::sequence\_manager::internal::ThreadControllerImpl](javascript:void(0);) &, const base::sequence\_manager::internal::ThreadControllerImpl::WorkType &> base/bind\_internal.h:657  

#48 0x564873c48187 in RunImpl<void (base::sequence\_manager::internal::ThreadControllerImpl::\*const &)(base::sequence\_manager::internal::ThreadControllerImpl::WorkType), const std::\_\_1::tuple<base::WeakPtr[base::sequence\_manager::internal::ThreadControllerImpl](javascript:void(0);), base::sequence\_manager::internal::ThreadControllerImpl::WorkType> &, 0, 1> base/bind\_internal.h:710  

#49 0x564873c48187 in Run base/bind\_internal.h:692  

#50 0x564873befb93 in Run base/callback.h:101  

#51 0x564873befb93 in RunTask base/task/common/task\_annotator.cc:163  

#52 0x564873c502e4 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:352  

#53 0x564873c4f96f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:268  

#54 0x564873af31e3 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:39  

#55 0x564873c52129 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:471  

#56 0x564873b8c59a in base::RunLoop::Run() base/run\_loop.cc:124  

#57 0x56488460176e in content::RenderViewTest::LoadHTMLWithUrlOverride(char const\*, char const\*) content/public/test/render\_view\_test.cc:379  

#58 0x564867417b29 in LoadHTML content/test/fuzzer/fuzzer\_support.h:27  

#59 0x564867417b29 in LLVMFuzzerTestOneInput content/test/fuzzer/renderer\_fuzzer.cc:22  

#60 0x5648674190d8 in main testing/libfuzzer/unittest\_main.cc:57  

#61 0x7f789d4f6bf6 in \_\_libc\_start\_main /build/glibc-S7xCS9/glibc-2.27/csu/../csu/libc-start.c:310

0x603000014908 is located 0 bytes to the right of 24-byte region [0x6030000148f0,0x603000014908)  

allocated by thread T0 here:  

#0 0x5648673eb0fd in \_\_interceptor\_malloc /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_malloc\_linux.cpp:145  

#1 0x564878f74933 in AllocFlags base/allocator/partition\_allocator/partition\_root.h:781  

#2 0x564878f74933 in Alloc base/allocator/partition\_allocator/partition\_root.h:1029  

#3 0x564878f74933 in BufferMalloc third\_party/blink/renderer/platform/wtf/allocator/partitions.cc:245  

#4 0x564878fa24ea in WTF::StringImpl::CreateStatic(char const\*, unsigned int, unsigned int) third\_party/blink/renderer/platform/wtf/text/string\_impl.cc:213  

#5 0x56487e8139b7 in blink::event\_type\_names::Init() gen/third\_party/blink/renderer/core/event\_type\_names.cc:723  

#6 0x56487ade78a9 in blink::CoreInitializer::Initialize() third\_party/blink/renderer/core/core\_initializer.cc:128  

#7 0x56488003c3a1 in blink::ModulesInitializer::Initialize() third\_party/blink/renderer/modules/modules\_initializer.cc:127  

#8 0x56487ad94fe1 in blink::(anonymous namespace)::InitializeCommon(blink::Platform\*, mojo::BinderMap\*) third\_party/blink/renderer/controller/blink\_initializer.cc:131  

#9 0x56487ad94e9f in blink::Initialize(blink::Platform\*, mojo::BinderMap\*, blink::scheduler::WebThreadScheduler\*) third\_party/blink/renderer/controller/blink\_initializer.cc:181  

#10 0x56488460244f in content::RenderViewTest::SetUp() content/public/test/render\_view\_test.cc:430  

#11 0x56486741eabd in content::RenderViewTestAdapter::SetUp() content/test/fuzzer/fuzzer\_support.cc:36  

#12 0x56486741eda2 in content::Env::Env() content/test/fuzzer/fuzzer\_support.cc:56  

#13 0x564867417682 in LLVMFuzzerTestOneInput content/test/fuzzer/renderer\_fuzzer.cc:20  

#14 0x5648674190d8 in main testing/libfuzzer/unittest\_main.cc:57  

#15 0x7f789d4f6bf6 in \_\_libc\_start\_main /build/glibc-S7xCS9/glibc-2.27/csu/../csu/libc-start.c:310

SUMMARY: AddressSanitizer: heap-buffer-overflow third\_party/blink/renderer/platform/heap/impl/member.h:253 in GetRaw  

Shadow bytes around the buggy address:  

0x0c067fffa8d0: 00 00 00 04 fa fa 00 00 00 02 fa fa 00 00 00 06  

0x0c067fffa8e0: fa fa 00 00 00 06 fa fa 00 00 00 00 fa fa 00 00  

0x0c067fffa8f0: 00 04 fa fa 00 00 00 07 fa fa 00 00 00 03 fa fa  

0x0c067fffa900: 00 00 00 03 fa fa 00 00 00 03 fa fa 00 00 00 04  

0x0c067fffa910: fa fa 00 00 00 01 fa fa 00 00 00 07 fa fa 00 00  

=>0x0c067fffa920: 00[fa]fa fa 00 00 00 06 fa fa 00 00 00 03 fa fa  

0x0c067fffa930: 00 00 00 07 fa fa 00 00 00 00 fa fa 00 00 00 05  

0x0c067fffa940: fa fa 00 00 00 03 fa fa 00 00 00 00 fa fa 00 00  

0x0c067fffa950: 00 07 fa fa 00 00 00 05 fa fa 00 00 00 06 fa fa  

0x0c067fffa960: 00 00 00 06 fa fa 00 00 00 05 fa fa 00 00 00 04  

0x0c067fffa970: fa fa 00 00 00 05 fa fa 00 00 00 03 fa fa 00 00  

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

==45837==ABORTING

Client ID (if relevant): crash/181d952e45f85c12

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Renata Hodovan  

This issue was found by the Grammarinator fuzzer.

## Attachments

- [hbo.html](attachments/hbo.html) (text/plain, 142 B)

## Timeline

### [Deleted User] (2020-11-16)

[Empty comment from Monorail migration]

### dr...@chromium.org (2020-11-16)

I can only reproduce this at head, not in the official Dev release, but otherwise it reproduces as described. Triaging to kainino@, as an owner of Blink>WebGL

[Monorail components: Blink>WebGL]

### ka...@chromium.org (2020-11-17)

This seems most likely due to japhet@'s recent change.

[Monorail components: Blink>WebXR]

### ba...@chromium.org (2020-11-17)

[Empty comment from Monorail migration]

### ho...@gmail.com (2020-11-17)

@drubery As per the release channel reproducibility, I forgot to mention that the release channel crashed for me on Mac OS 10.15.5. Now I tried to validate it on Linux but it only reproduced on head, indeed.

### ja...@chromium.org (2020-11-17)

I don't think this is due to my change. The problem is with this line: https://chromium.googlesource.com/chromium/src/+/9e0d0984b9dc88de6fcf2c88b9bd6ec535a5e7c5/third_party/blink/renderer/modules/webgl/webgl_rendering_context_base.cc#831

|host| is being cast to an HTMLCanvasElement, but it's not guaranteed to be a HTMLCanvasElement (in the repro it's an OffscreenCanvas).

My guess is that this was introduced in https://chromium.googlesource.com/chromium/src/+/30f128d41eab22c218d42378a5e732bf532252b6, so reassigning to patrto@. If my analysis seems wrong, feel free to reassign back to me.

### [Deleted User] (2020-11-17)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-11-17)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ka...@chromium.org (2020-11-17)

Oops, I missed that line, and for some reason though the error was in XRSystem::From. I agree with your analysis.
(Nit: the commit where it was introduced was actually e13b32c143ede19ff2790664447a561f768522d0 .)

### pa...@microsoft.com (2020-11-17)

Taking a look, will have a fix shortly

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### ho...@gmail.com (2020-11-19)

Additional information: I've installed Chrome Dev on my Android device and loaded the test case above. The result was a crash there, too (although I don't have any further information about the circumstances or backtrace on the device, yet).

Chrome version on Android: 88.0.4319.2 + dev + 32bit
OS: Android 10, SM-G973F


### pa...@microsoft.com (2020-11-19)

CL for the fix: https://chromium-review.googlesource.com/c/chromium/src/+/2545580

### ho...@gmail.com (2020-11-29)

For the record, with slightly modified test cases - that still contained an OffscreenCanvas and an xrCompatible context - I could trigger a global-buffer-overflow, a use-after-poison, a heap-use-after-free, an unknown-crash, and a null-dereference issue beside the heap-buffer-overflow reported in this ticket. I don't report them separately, since most probably they will be fixed by the CL above, once it will be landed.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/36c015641d140993d468c564474602415e353ab4

commit 36c015641d140993d468c564474602415e353ab4
Author: Patrick To <patrto@microsoft.com>
Date: Mon Nov 30 23:49:15 2020

Prevent cast of HTMLCanvasElement to OffscreenCanvas in MakeXrCompatible

For offscreen canvases without a placeholder canvas, the
CanvasRenderingContextHost is of type OffscreenCanvas, not
HTMLCanvasElement. This change sets the xr compatible flag to false for
these canvases to avoid the security issue of casting incompatible types

A follow up change will add support and tests for OffscreenCanvas.

Bug: 1149204
Change-Id: Id8d31126b4ba2af50d02390141afdd4e4046394f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2545580
Reviewed-by: Brandon Jones <bajones@chromium.org>
Commit-Queue: Patrick To <patrto@microsoft.com>
Cr-Commit-Position: refs/heads/master@{#832078}

[modify] https://crrev.com/36c015641d140993d468c564474602415e353ab4/third_party/blink/renderer/modules/webgl/webgl_rendering_context_base.cc


### pa...@microsoft.com (2020-12-01)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-01)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-01)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-01)

This release blocking issue appears to be targeted for M88, which has already branched. Because this issue was marked as fixed after branch point, a merge of any CLs which landed on or after November 12 may be required. Please review whether or not any CLs should be merged ASAP, and if a merge is necessary apply the label Merge-Request-88 to begin the merge review process. If no merge is required, please simply remove the Merge-TBD label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pa...@microsoft.com (2020-12-02)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-03)

This bug requires manual review: M88's targeted beta branch promotion date has already passed, so this requires manual review
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
Owners: govind@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2020-12-04)

Pls answer questions in https://crbug.com/chromium/1149204#c21 for merge review 

### ba...@chromium.org (2020-12-04)

1. Yes, this is a "critical, release blocking issues where the fix is low complexity."
2.  https://chromium.googlesource.com/chromium/src.git/+/36c015641d140993d468c564474602415e353ab4
3. Yes.
4. The issue does not affect < M88, and has already landed in M89 prior to branch.
5. A related change (https://chromium.googlesource.com/chromium/src/+/30f128d41eab22c218d42378a5e732bf532252b6) which landed in M88 prior to branch caused the heap-buffer-overflow due to an invalid cast.
6. No.
7. N/A

### ba...@chromium.org (2020-12-05)

[Empty comment from Monorail migration]

### ad...@google.com (2020-12-07)

Approving merge to M88, branch 4324.

### pa...@microsoft.com (2020-12-07)

Thank you everyone!

Merge CL: https://chromium-review.googlesource.com/c/chromium/src/+/2577503

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e3cb21077df6b9aaa98d51ab01b768fc1a19fe45

commit e3cb21077df6b9aaa98d51ab01b768fc1a19fe45
Author: Patrick To <patrto@microsoft.com>
Date: Mon Dec 07 22:05:22 2020

Prevent cast of HTMLCanvasElement to OffscreenCanvas in MakeXrCompatible

For offscreen canvases without a placeholder canvas, the
CanvasRenderingContextHost is of type OffscreenCanvas, not
HTMLCanvasElement. This change sets the xr compatible flag to false for
these canvases to avoid the security issue of casting incompatible types

A follow up change will add support and tests for OffscreenCanvas.

(cherry picked from commit 36c015641d140993d468c564474602415e353ab4)

Bug: 1149204
Change-Id: Id8d31126b4ba2af50d02390141afdd4e4046394f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2545580
Reviewed-by: Brandon Jones <bajones@chromium.org>
Commit-Queue: Patrick To <patrto@microsoft.com>
Cr-Original-Commit-Position: refs/heads/master@{#832078}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2577503
Reviewed-by: Patrick To <patrto@microsoft.com>
Cr-Commit-Position: refs/branch-heads/4324@{#648}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/e3cb21077df6b9aaa98d51ab01b768fc1a19fe45/third_party/blink/renderer/modules/webgl/webgl_rendering_context_base.cc


### ad...@google.com (2020-12-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-12-10)

Congratulations! The VRP panel has decided to award $5000 for this bug.

### ad...@google.com (2020-12-10)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1149204?no_tracker_redirect=1

[Multiple monorail components: Blink>WebGL, Blink>WebXR]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053883)*
