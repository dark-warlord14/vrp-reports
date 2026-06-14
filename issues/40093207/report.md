# Security: WebGL heap-buffer-overflow in clearBufferuiv()

| Field | Value |
|-------|-------|
| **Issue ID** | [40093207](https://issues.chromium.org/issues/40093207) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>WebGL, Internals>GPU |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | zm...@chromium.org |
| **Created** | 2018-11-27 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

This bug tested in stable chrome asan linux build (asan-linux-release-611016) Chromium 72.0.3623.0

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

=================================================================  

==9880==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602000235994 at pc 0x556b1b9d5789 bp 0x7f8ed7ffffe0 sp 0x7f8ed7fff790  

READ of size 16 at 0x602000235994 thread T20 (Chrome\_InProcRe)  

#0 0x556b1b9d5788 in \_\_asan\_memcpy /b/swarming/w/ir/kitchen-workdir/src/third\_party/llvm/compiler-rt/lib/asan/asan\_interceptors\_memintrinsics.cc:23:3  

#1 0x556b2738eff8 in Init gpu/command\_buffer/common/gles2\_cmd\_format\_autogen.h:1036:5  

#2 0x556b2738eff8 in ClearBufferuivImmediate gpu/command\_buffer/client/gles2\_cmd\_helper\_autogen.h:218  

#3 0x556b2738eff8 in gpu::gles2::GLES2Implementation::ClearBufferuiv(unsigned int, int, unsigned int const\*) gpu/command\_buffer/client/gles2\_implementation\_impl\_autogen.h:279  

#4 0x556b2e91bf60 in blink::WebGL2RenderingContextBase::clearBufferuiv(unsigned int, int, blink::MaybeShared<blink::DOMTypedArray<WTF::Uint32Array, v8::Uint32Array> >, unsigned int) third\_party/blink/renderer/modules/webgl/webgl2\_rendering\_context\_base.cc:3629:16  

#5 0x556b2dd31155 in blink::webgl2\_rendering\_context\_v8\_internal::ClearBufferuiv1Method(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) gen/third\_party/blink/renderer/bindings/modules/v8/v8\_webgl2\_rendering\_context.cc:6665:9  

#6 0x556b2dc54fc1 in ClearBufferuivMethod gen/third\_party/blink/renderer/bindings/modules/v8/v8\_webgl2\_rendering\_context.cc  

#7 0x556b2dc54fc1 in blink::V8WebGL2RenderingContext::ClearBufferuivMethodCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) gen/third\_party/blink/renderer/bindings/modules/v8/v8\_webgl2\_rendering\_context.cc:13989  

#8 0x556b1ecc9ca2 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo\*) v8/src/api-arguments-inl.h:146:3  

#9 0x556b1ecc711e in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:109:36  

#10 0x556b1ecc4c60 in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) v8/src/builtins/builtins-api.cc:139:5  

#11 0x556b20a4db4a in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_NoBuiltinExit (../asan-linux-release-611016/content\_shell+0xaed8b4a)  

#12 0x556b209a1704 in Builtins\_InterpreterEntryTrampoline (../asan-linux-release-611016/content\_shell+0xae2c704)  

#13 0x556b2099eb22 in Builtins\_JSEntryTrampoline (../asan-linux-release-611016/content\_shell+0xae29b22)  

#14 0x7ee42d302136 (<unknown module>)  

#15 0x556b1f7378b6 in Call v8/src/simulator.h:113:12  

#16 0x556b1f7378b6 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, bool, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Execution::MessageHandling, v8::internal::Execution::Target) v8/src/execution.cc:156  

#17 0x556b1f736dc2 in CallInternal v8/src/execution.cc:192:10  

#18 0x556b1f736dc2 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution.cc:203  

#19 0x556b1eb18895 in v8::Script::Run(v8::Local[v8::Context](javascript:void(0);)) v8/src/api.cc:2117:7  

#20 0x556b29109c56 in blink::V8ScriptRunner::RunCompiledScript(v8::Isolate\*, v8::Local[v8::Script](javascript:void(0);), blink::ExecutionContext\*) third\_party/blink/renderer/bindings/core/v8/v8\_script\_runner.cc:293:22  

#21 0x556b2ad2b50d in blink::ScriptController::ExecuteScriptAndReturnValue(v8::Local[v8::Context](javascript:void(0);), blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&) third\_party/blink/renderer/bindings/core/v8/script\_controller.cc:131:20  

#22 0x556b2ad2de2a in blink::ScriptController::EvaluateScriptInMainWorld(blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&, blink::ScriptController::ExecuteScriptPolicy) third\_party/blink/renderer/bindings/core/v8/script\_controller.cc:349:33  

#23 0x556b2ad2e851 in blink::ScriptController::ExecuteScriptInMainWorld(blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&) third\_party/blink/renderer/bindings/core/v8/script\_controller.cc:313:3  

#24 0x556b2d31cdb6 in blink::PendingScript::ExecuteScriptBlockInternal(blink::Script\*, blink::ScriptElementBase\*, bool, bool, bool, base::TimeTicks, bool) third\_party/blink/renderer/core/script/pending\_script.cc:274:13  

#25 0x556b2d31c7ca in blink::PendingScript::ExecuteScriptBlock(blink::KURL const&) third\_party/blink/renderer/core/script/pending\_script.cc:185:3  

#26 0x556b2d321fc3 in blink::ScriptLoader::PrepareScript(WTF::TextPosition const&, blink::ScriptLoader::LegacyTypeSupport) third\_party/blink/renderer/core/script/script\_loader.cc:734:9  

#27 0x556b2d2da5ab in blink::HTMLParserScriptRunner::ProcessScriptElementInternal(blink::Element\*, WTF::TextPosition const&) third\_party/blink/renderer/core/script/html\_parser\_script\_runner.cc:541:20  

#28 0x556b2d2d9ee8 in blink::HTMLParserScriptRunner::ProcessScriptElement(blink::Element\*, WTF::TextPosition const&) third\_party/blink/renderer/core/script/html\_parser\_script\_runner.cc:320:3  

#29 0x556b2be776bc in RunScriptsForPausedTreeBuilder third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:278:21  

#30 0x556b2be776bc in blink::HTMLDocumentParser::ProcessTokenizedChunkFromBackgroundParser(std::\_\_1::unique\_ptr<blink::HTMLDocumentParser::TokenizedChunk, std::\_\_1::default\_delete[blink::HTMLDocumentParser::TokenizedChunk](javascript:void(0);) >) third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:535  

#31 0x556b2be72771 in blink::HTMLDocumentParser::PumpPendingSpeculations() third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:593:9  

#32 0x556b20caf873 in Run base/callback.h:99:12  

#33 0x556b20caf873 in blink::TaskHandle::Runner::Run(blink::TaskHandle const&) third\_party/blink/renderer/platform/scheduler/common/post\_cancellable\_task.cc:48  

#34 0x556b23949d3e in Run base/callback.h:99:12  

#35 0x556b23949d3e in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/debug/task\_annotator.cc:99  

#36 0x556b23a48a48 in base::sequence\_manager::internal::ThreadControllerImpl::DoWork(base::sequence\_manager::internal::ThreadControllerImpl::WorkType) base/task/sequence\_manager/thread\_controller\_impl.cc:209:23  

#37 0x556b23949d3e in Run base/callback.h:99:12  

#38 0x556b23949d3e in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/debug/task\_annotator.cc:99  

#39 0x556b23946f77 in base::MessageLoopImpl::RunTask(base::PendingTask\*) base/message\_loop/message\_loop\_impl.cc:350:46  

#40 0x556b23948457 in DeferOrRunPendingTask base/message\_loop/message\_loop\_impl.cc:361:5  

#41 0x556b23948457 in base::MessageLoopImpl::DoWork() base/message\_loop/message\_loop\_impl.cc:449  

#42 0x556b2394f6ff in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:39:31  

#43 0x556b239c21db in base::RunLoop::Run() base/run\_loop.cc:102:14  

#44 0x556b23ab8d18 in base::Thread::ThreadMain() base/threading/thread.cc:332:3  

#45 0x556b23b9cdbd in base::(anonymous namespace)::ThreadFunc(void\*) base/threading/platform\_thread\_posix.cc:81:13  

#46 0x7f8f1ef3a6b9 in start\_thread (/lib/x86\_64-linux-gnu/libpthread.so.0+0x76b9)

## Attachments

- [bug_01.html](attachments/bug_01.html) (text/plain, 378 B)
- [bug_01-asan.txt](attachments/bug_01-asan.txt) (text/plain, 20.4 KB)

## Timeline

### cl...@chromium.org (2018-11-27)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6307805860200448.

### cl...@chromium.org (2018-11-28)

Detailed report: https://clusterfuzz.com/testcase?key=6307805860200448

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 16
Crash Address: 0x6090001b8c94
Crash State:
  gpu::gles2::GLES2Implementation::ClearBufferuiv
  blink::WebGL2RenderingContextBase::clearBufferuiv
  blink::webgl2_rendering_context_v8_internal::ClearBufferuiv1Method
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=495501:495712

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6307805860200448

See https://github.com/google/clusterfuzz-tools for more information.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### ct...@chromium.org (2018-11-28)

The regression range from clusterfuzz is rather large, but looking through a couple possible CLs stand out:

1) Roll SwiftShader e8d42ae..0def102 https://chromium.googlesource.com/chromium/src/+/ed09b0b2296674b3aadeac11ca33475a809d2d8c
2) Lower GPU SharedMemoryLimits on Low-End and Consolidate Logic https://chromium.googlesource.com/chromium/src/+/2fc4409b9b179323f14888b74968b88a7432ee07

I'm not sure whether this is a swiftshader issue or a general GPU issue, so I'm tentatively assigning this to piman@ -- please take a look and feel free to re-assign if this isn't correct.

Also cc'ing other folks involved on those two CLs for visibility.

(Tentatively assigning OS labels where we should have Blink/V8/WebGL.)

[Monorail components: Blink>WebGL Internals>GPU]

### sh...@chromium.org (2018-11-28)

[Empty comment from Monorail migration]

### pi...@chromium.org (2018-11-28)

It probably bisected to CL #1 because that likely is what enabled webgl2 on the bots, but the problem predates it. The ClearBufferuiv is hard-coded to take 4 uints, but that isn't correct for depth or stencil buffers. Size of the imput array is properly validated in webgl, but the command buffer code will incorrectly read 4 uints.

### zm...@chromium.org (2018-11-28)

Actually ClearBufferuiv can only take GL_COLOR. WebGL side's validation is only to make sure buffer access is valid because WebGL allows an offset.

This is something else. I am looking.

### zm...@chromium.org (2018-11-28)

So the bug is on the client side. Since the GL API signature passes data as a pointer, in theory at command buffer client side, we don't have a mechanism to guard against out-of-bound read.

What we can do is to enhance WebGL2's validation code to be a full validation, so it won't pass an invalid call to GLES2Implementation.

However, for something other than WebGL2, say, Nacl (which is no longer a concern since we don't expose WebGL2) or internal usage, it is up to the caller's discretion not to pass down invalid data size.

### bu...@chromium.org (2018-11-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5f8761dd073c4ddd3b5aea8d95a2717e7b6e36e5

commit 5f8761dd073c4ddd3b5aea8d95a2717e7b6e36e5
Author: Zhenyao Mo <zmo@chromium.org>
Date: Thu Nov 29 03:48:39 2018

Validate glClearBuffer*v function |buffer| param on the client side

Otherwise we could read out-of-bounds even if an invalid |buffer| is passed
in and in theory we should not read the buffer at all.

BUG=908749
TEST=gl_tests in ASAN build
R=piman@chromium.org

Change-Id: I94b69b56ce3358ff9bfc0e21f0618aec4371d1ec
Reviewed-on: https://chromium-review.googlesource.com/c/1354571
Reviewed-by: Antoine Labour <piman@chromium.org>
Commit-Queue: Zhenyao Mo <zmo@chromium.org>
Cr-Commit-Position: refs/heads/master@{#612023}
[modify] https://crrev.com/5f8761dd073c4ddd3b5aea8d95a2717e7b6e36e5/gpu/command_buffer/build_cmd_buffer_lib.py
[modify] https://crrev.com/5f8761dd073c4ddd3b5aea8d95a2717e7b6e36e5/gpu/command_buffer/build_gles2_cmd_buffer.py
[modify] https://crrev.com/5f8761dd073c4ddd3b5aea8d95a2717e7b6e36e5/gpu/command_buffer/client/gles2_implementation_impl_autogen.h
[modify] https://crrev.com/5f8761dd073c4ddd3b5aea8d95a2717e7b6e36e5/gpu/command_buffer/common/gles2_cmd_format_autogen.h
[modify] https://crrev.com/5f8761dd073c4ddd3b5aea8d95a2717e7b6e36e5/gpu/command_buffer/common/gles2_cmd_utils.cc
[modify] https://crrev.com/5f8761dd073c4ddd3b5aea8d95a2717e7b6e36e5/gpu/command_buffer/common/gles2_cmd_utils.h
[modify] https://crrev.com/5f8761dd073c4ddd3b5aea8d95a2717e7b6e36e5/gpu/command_buffer/tests/gl_clear_framebuffer_unittest.cc


### cl...@chromium.org (2018-11-29)

ClusterFuzz has detected this issue as fixed in range 612022:612027.

Detailed report: https://clusterfuzz.com/testcase?key=6307805860200448

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 16
Crash Address: 0x6090001b8c94
Crash State:
  gpu::gles2::GLES2Implementation::ClearBufferuiv
  blink::WebGL2RenderingContextBase::clearBufferuiv
  blink::webgl2_rendering_context_v8_internal::ClearBufferuiv1Method
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=495501:495712
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=612022:612027

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6307805860200448

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2018-11-29)

ClusterFuzz testcase 6307805860200448 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2018-11-29)

[Empty comment from Monorail migration]

### na...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-12-07)

Hi! The Chrome VRP decided to reward $1,000 for this report :-) A member of our finance team will be in touch to arrange payment.  Also, how would you like to be credited in our release notes?

### aw...@google.com (2018-12-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-14)

This bug requires manual review: M72 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), djmm@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-12-14)

Already in 72

### aw...@google.com (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-02-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/908749?no_tracker_redirect=1

[Multiple monorail components: Blink>WebGL, Internals>GPU]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093207)*
