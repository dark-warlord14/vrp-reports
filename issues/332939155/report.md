# SEGV_ACCERR / seccomp-bpf gpu::gles2::cmds::FramebufferPixelLocalClearValuefvANGLEImmediate::Init

| Field | Value |
|-------|-------|
| **Issue ID** | [332939155](https://issues.chromium.org/issues/332939155) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebGL |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 123.0.0.0 |
| **Reporter** | wx...@gmail.com |
| **Assignee** | kb...@chromium.org |
| **Created** | 2024-04-05 |
| **Bounty** | $8,000.00 |

## Description

# Steps to reproduce the problem

1. chrome://flags to enable the #enable-webgl-draft-extensions flags
2. cd chromium\src\third\_party\webgl\src\sdk\tests\ and python -m SimpleHTTPServer
3. change the third\_party\webgl\src\sdk\tests\conformance2\extensions\webgl-shader-pixel-local-storage.html to my upload webgl-shader-pixel-local-storage.html.
4. visit <http://127.0.0.1:8000/conformance2/extensions/webgl-shader-pixel-local-storage.html>
5. you will see the asan log

# Problem Description

above all

# Summary

access-violation on unknown address 0x12700000fffc in chromium

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [webgl-shader-pixel-local-storage.html](attachments/webgl-shader-pixel-local-storage.html) (text/html, 19.5 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 16.4 KB)
- [0001-fix-the-integer-overflow-to-prevent-oob-read.patch](attachments/0001-fix-the-integer-overflow-to-prevent-oob-read.patch) (text/x-diff, 1.2 KB)

## Timeline

### wx...@gmail.com (2024-04-05)

bitset commit:
https://chromium-review.googlesource.com/c/chromium/src/+/4307215

```
bool WebGLShaderPixelLocalStorage::ValidatePLSClearCommand(
    WebGLRenderingContextBase* context,
    const char* function_name,
    GLint plane,
    size_t src_length,
    GLuint src_offset) {
  if (!ValidatePLSFramebuffer(context, function_name) ||
      !ValidatePLSPlaneIndex(context, function_name, plane)) {
    return false;
  }
  if (src_length < src_offset + 4u) {         --------->>here src_offset + 4u  will  integer overflow.
    context->SynthesizeGLError(GL_INVALID_VALUE, function_name,
                               "clear value must contain at least 4 elements");
    return false;
  }
  return true;
}

```

### cl...@appspot.gserviceaccount.com (2024-04-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5186428460793856.

### ar...@chromium.org (2024-04-05)

**security shepherd**

Thanks!

I can reproduce with and without ASAN.

```
arthursonzogni@arthursonzogni:~/chromium/src$ ./out/ASAN/chrome --enable-webgl-draft-extensions  http://127.0.0.1:8000/conformance2/extensions/webgl-shader-pixel-local-storage.html 2>&1 | ./tools/valgrind/asan/asan_symbolize.py
[3538803:3538803:0405/094719.313208:ERROR:viz_main_impl.cc(167)] Exiting GPU process due to errors during initialization
127.0.0.1 - - [05/Apr/2024 09:47:21] "GET /conformance2/extensions/webgl-shader-pixel-local-storage.html HTTP/1.1" 304 -
[3538767:3538767:0405/094721.541642:ERROR:object_proxy.cc(576)] Failed to call method: org.freedesktop.ScreenSaver.GetActive: object_path= /org/freedesktop/ScreenSaver: org.freedesktop.DBus.Error.NotSupported: This method is not implemented
[3538767:3538767:0405/094721.630054:ERROR:object_proxy.cc(576)] Failed to call method: org.gnome.ScreenSaver.GetActive: object_path= /org/gnome/ScreenSaver: org.freedesktop.DBus.Error.ServiceUnknown: GDBus.Error:org.freedesktop.DBus.Error.ServiceUnknown: The name org.gnome.Shell.ScreenShield was not provided by any .service files
[3538929:3538929:0405/094721.674356:ERROR:viz_main_impl.cc(167)] Exiting GPU process due to errors during initialization
[3539009:3539009:0405/094721.986424:ERROR:viz_main_impl.cc(167)] Exiting GPU process due to errors during initialization
[3538901:7:0405/094722.267254:ERROR:command_buffer_proxy_impl.cc(131)] ContextResult::kTransientFailure: Failed to send GpuControl.CreateCommandBuffer.
[3538901:7:0405/094722.267551:ERROR:context_provider_command_buffer.cc(157)] GpuChannelHost failed to create command buffer.
[0405/094723.411000:WARNING:exception_snapshot_linux.cc(391)] thread ID 1 not found in process
[0405/094723.411379:ERROR:process_snapshot_linux.cc(129)] thread not found 1
Received signal 11 SEGV_ACCERR 7dac0000fffc
    #0 0x5652a3dcf506 in ___interceptor_backtrace /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4358:13
    #1 0x5652ba5fbbf8 in base::debug::CollectStackTrace(void const**, unsigned long) ./../../base/debug/stack_trace_posix.cc:1039:7
    #2 0x5652ba5b9d36 in StackTrace ./../../base/debug/stack_trace.cc:229:20
    #3 0x5652ba5b9d36 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:224:28
    #4 0x5652ba5faee6 in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) ./../../base/debug/stack_trace_posix.cc:457:3
    #5 0x7f7b2e65a510 in __GI___sigaction :?
    #6 0x7f7b2e770662 in __memcpy_avx_unaligned_erms ./string/../sysdeps/x86_64/multiarch/memmove-vec-unaligned-erms.S:335:0
    #7 0x5652a3e217e3 in __asan_memcpy _asan_rtl_:3
    #8 0x5652bf6a6e50 in Init ./../../gpu/command_buffer/common/gles2_cmd_format_autogen.h:16783:5
    #9 0x5652bf6a6e50 in FramebufferPixelLocalClearValuefvANGLEImmediate ./../../gpu/command_buffer/client/gles2_cmd_helper_autogen.h:3408:8
    #10 0x5652bf6a6e50 in gpu::gles2::GLES2Implementation::FramebufferPixelLocalClearValuefvANGLE(int, float const*) ./../../gpu/command_buffer/client/gles2_implementation_impl_autogen.h:3780:12
    #11 0x5652d0d30513 in blink::WebGLShaderPixelLocalStorage::framebufferPixelLocalClearValuefvWEBGL(int, blink::NADCTypedArrayView<float>, unsigned int) ./../../third_party/blink/renderer/modules/webgl/webgl_shader_pixel_local_storage.cc:138:25
    #12 0x5652d0d376d2 in blink::(anonymous namespace)::v8_webgl_shader_pixel_local_storage::FramebufferPixelLocalClearValuefvWEBGLOperationOverload1(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/modules/v8/v8_webgl_shader_pixel_local_storage.cc:185:17
    #13 0x5652d0d33dc1 in blink::(anonymous namespace)::v8_webgl_shader_pixel_local_storage::FramebufferPixelLocalClearValuefvWEBGLOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/modules/v8/v8_webgl_shader_pixel_local_storage.cc:0:10
    #14 0x5652af70280f in Builtins_CallApiCallbackGeneric setup-isolate-deserialize.cc:0:0
  r8: 00000fef4a10dbc4  r9: 00007f7a5086de33 r10: 00000fef4a10dbc6 r11: 00000fefca105bc0
 r12: 00000fefca105bc0 r13: ffffffffffffffcf r14: 00007f7b2bcab800 r15: 00007f7b2bcab990
  di: 00007f7a5086de24  si: 00007dac0000fffc  bp: 00007ffe0b969170  bx: 0000000000000000
  dx: 0000000000000010  ax: 00007f7a5086de24  cx: 00000fefca105bc6  sp: 00007ffe0b968928
  ip: 00007f7b2e770662 efl: 0000000000010246 cgf: 002b000000000033 erf: 0000000000000004
 trp: 000000000000000e msk: 0000000000000000 cr2: 00007dac0000fffc
[end of stack trace]
../../sandbox/linux/seccomp-bpf-helpers/sigsys_handlers.cc:**CRASHING**:seccomp-bpf failure in syscall nr=0x25 arg1=0x5 arg2=0x7ffe0b967ff0 arg3=0x0 arg4=0x8


```

- **Clusterfuzz**: I can't upload it to clusterfuzz for now, because it is not self contained. It requires dependencies from chromium tests files. At some point, it would be interesting uploading a self contained reproduce.
- **Severity**: High severity: Memory corruption in GPU process. I guess this is due to the [memcpy](https://source.chromium.org/chromium/chromium/src/+/main:gpu/command_buffer/common/gles2_cmd_format_autogen.h;l=16780?q=FramebufferPixelLocalClearValuefvANGLEImmediate::Init&ss=chromium) in

```
  void Init(GLint _plane, const GLfloat* _value) {
    SetHeader();
    plane = _plane;
    memcpy(ImmediateDataAddress(this), _value, ComputeDataSize());
  }

```

- **Security\_Impact-None**: It requires a specific flag: `--enable-webgl-draft-extensions`. I checked normal users are not affected.
  b
- **Assignee**: [kbr@chromium.org](mailto:kbr@chromium.org), as reviewer of the [patch](https://chromium-review.googlesource.com/c/chromium/src/+/4307215) the @reporter bisected.
- **Found-In**: [Stable 117](https://chromiumdash.appspot.com/commit/78118e8ad88140218c88962f2ff05e32364a2517)

### ar...@chromium.org (2024-04-05)

@bajones, as OWNER, could you please help triage this security bug to the right developer.

### wx...@gmail.com (2024-04-18)

suggtest patch

### kb...@chromium.org (2024-04-18)

Thank you for the report and suggested patch. This is not yet a code path shipping by default in Chrome, so this isn't a security vulnerability, nor is it P1. At the same time, we'll gladly review your fix, and fix this one way or another.

### wx...@gmail.com (2024-04-19)

Hi, you can see this about the definition of vulnerability..
https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md#How-can-I-know-which-fixes-to-include-in-my-downstream-project

### wx...@gmail.com (2024-04-19)

This bug should be set as Security_Impact-None.

### ap...@google.com (2024-04-23)

Project: chromium/src
Branch: main

commit a5cd35835e676d9543384f55965314c86d53cd73
Author: Kenneth Russell <kbr@chromium.org>
Date:   Tue Apr 23 19:32:23 2024

    Check for overflow in PLS clear validation.
    
    Fixed: 332939155
    Change-Id: I4172ede36295b9e1c07a2560dcf3e613a0ba92b2
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5473876
    Reviewed-by: Shrek Shao <shrekshao@google.com>
    Commit-Queue: Kenneth Russell <kbr@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1291476}

M       third_party/blink/renderer/modules/webgl/webgl_shader_pixel_local_storage.cc

https://chromium-review.googlesource.com/5473876


### kb...@chromium.org (2024-04-23)

Submitter, thanks for clarifying the definition of vulnerability.

Security folks, I don't see where to set the security impact field - maybe I can't, from my chromium.org account? I switched the "In Prod" flag to false because this requires a command line flag to enable the code path.

### ap...@google.com (2024-04-30)

Project: chromium/src
Branch: main

commit 08488fd325dfdbce7b6f14975b54ffd644f9a79d
Author: Kenneth Russell <kbr@chromium.org>
Date:   Tue Apr 30 02:40:45 2024

    Roll WebGL bc3c8ba..992583d
    
    https://chromium.googlesource.com/external/khronosgroup/webgl.git/+log/bc3c8ba..992583d
    
    Bug: 40279138
    Bug: 328284177
    Bug: 332939155
    Cq-Include-Trybots: luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-android-arm64
    Change-Id: I9773fdf980a87eb3e2bb19c853b5dcc29b625ed5
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5499102
    Reviewed-by: Kai Ninomiya <kainino@chromium.org>
    Commit-Queue: Kenneth Russell <kbr@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1294130}

M       DEPS
M       content/test/gpu/gpu_tests/test_expectations/webgl2_conformance_expectations.txt
M       content/test/gpu/gpu_tests/webgl_conformance_revision.txt
M       third_party/webgl/src

https://chromium-review.googlesource.com/5499102


### am...@chromium.org (2024-04-30)

Hi kbr@, security\_impact-none was already set as part of the initial security triage in c#4. Thus a merge has not/will not be triggered.
For future reference, Security Impact is now a hotlist (hotlistid:5433277), you should be able to set that for any future issues you need to.

### sp...@google.com (2024-05-09)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
memory corruption in a sandboxed process + $1,000 bisect bonus

Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. Two other things we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.
* If you are already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have already registered, there is no need to repeat the process and you’ll automatically be paid soon. If you have any payment related questions or issues, please reach out to p2p-vrp@google.com.

### pe...@google.com (2024-07-31)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/332939155)*
