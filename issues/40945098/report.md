# memory corruption in sw::SpirvEmitter::getImageSampler

| Field | Value |
|-------|-------|
| **Issue ID** | [40945098](https://issues.chromium.org/issues/40945098) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>SwiftShader |
| **Platforms** | Linux |
| **Reporter** | em...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2023-11-22 |
| **Bounty** | $10,000.00 |

## Description

**Steps to reproduce the problem:**  

tested os:  

Ubuntu 22.04

tested chromium version:  

Chromium 121.0.6142.0  

Chromium 113.0.5624.0(I believe it should be possible to reproduce earlier than this version.)  

Stable & Beta & Dev & Canary

reproduce steps:  

1 ./chrome --user-data-dir=/tmp/xx22 --incognito <http://localhost:8000/crash.html> --no-sandbox --disable-gpu

The console will immediately output information related to GPU process crashes.  

Received signal 11 SEGV\_ACCERR 52e00050cdd0  

[1122/223124.339346:ERROR:gpu\_process\_host.cc(992)] GPU process exited unexpectedly: exit\_code=139  

[1122/223124.339401:WARNING:gpu\_process\_host.cc(1362)] The GPU process has crashed 1 time(s)  

[1122/223127.773434:WARNING:sandbox\_linux.cc(400)] InitializeSandbox() called with multiple threads in process gpu-process.

**Problem Description:**  

2.For more detailed information, it is necessary to use GDB to attach the GPU process. The following is the information I get from GDB.  

Thread 3 "Thread<01>" received signal SIGSEGV, Segmentation fault.  

[Switching to Thread 0x7f28dc7ff640 (LWP 2763744)]  

0x00007f28edc3f37a in ?? ()  

(gdb) bt  

#0 0x00007f28edc3f37a in ()  

#1 0x00007fff00007fff in ()  

#2 0x00007fff00007fff in ()  

#3 0x00003a3407c45380 in ()  

#4 0x00003a3400039c30 in ()  

#5 0x00007f28dc7fb190 in ()  

#6 0x00007f28e9cd0cc6 in sw::SpirvEmitter::getImageSampler(vk::Device const\*, unsigned int, unsigned int, unsigned int) (device=<optimized out>, signature=<optimized out>, samplerId=<optimized out>, imageViewId=<optimized out>) at ../../third\_party/swiftshader/src/Pipeline/SpirvShaderSampling.cpp:125  

#7 0x00007f28e9b9a8c6 in std::\_\_Cr::\_\_function::\_\_policy\_func<void ()>::operator()() const (this=0x7f28dc7fb730) at ../../third\_party/libc++/src/include/\_\_functional/function.h:856  

#8 std::\_\_Cr::function<void ()>::operator()() const (this=0x7f28dc7fb730) at ../../third\_party/libc++/src/include/\_\_functional/function.h:1170  

#9 marl::Task::operator()() const (this=0x7f28dc7fb730) at ../../third\_party/swiftshader/third\_party/marl/include/marl/task.h:97  

#10 marl::Scheduler::Worker::runUntilIdle()  

(this=0x7f28e9bd971c <std::\_\_Cr::\_\_function::\_\_policy\_invoker<void ()>::\_\_call\_impl<std::\_\_Cr::\_\_function::\_\_default\_alloc\_func<sw::DrawCall::processPixels(vk::Device\*, marl::Pool[sw::DrawCall](javascript:void(0);)::Loan const&, marl::Pool[sw::DrawCall::BatchData](javascript:void(0);)::Loan const&, std::\_\_Cr::shared\_ptr[marl::Finally](javascript:void(0);) const&)::$\_0, void ()> >(std::\_\_Cr::\_\_function::\_\_policy\_storage const\*)+60>, this@entry=0x3a3400123800) at ../../third\_party/swiftshader/third\_party/marl/src/scheduler.cpp:703  

#11 0x00007f28e9b9a2c0 in marl::Scheduler::Worker::runUntilShutdown() (this=<optimized out>) at ../../third\_party/swiftshader/third\_party/marl/src/scheduler.cpp:588  

#12 marl::Scheduler::Worker::run() (this=this@entry=0x3a3400123800) at ../../third\_party/swiftshader/third\_party/marl/src/scheduler.cpp:581  

#13 0x00007f28e9b9d0e7 in marl::Scheduler::Worker::start()::$\_0::operator()() const (this=<optimized out>) at ../../third\_party/swiftshader/third\_party/marl/src/scheduler.cpp:385  

#14 std::\_\_Cr::\_\_invoke[marl::Scheduler::Worker::start()::$\_0&](javascript:void(0);)(marl::Scheduler::Worker::start()::$\_0&) (\_\_f=<optimized out>) at ../../third\_party/libc++/src/include/\_\_type\_traits/invoke.h:344  

#15 std::\_\_Cr::\_\_invoke\_void\_return\_wrapper<void, true>::\_\_call[marl::Scheduler::Worker::start()::$\_0&](javascript:void(0);)(marl::Scheduler::Worker::start()::$\_0&) (\_\_args=<optimized out>) at ../../third\_party/libc++/src/include/\_\_type\_traits/invoke.h:419  

#16 std::\_\_Cr::\_\_function::\_\_default\_alloc\_func<marl::Scheduler::Worker::start()::$\_0, void ()>::operator()() (this=<optimized out>) at ../../third\_party/libc++/src/include/\_\_functional/function.h:242  

#17 std::\_\_Cr::\_\_function::\_\_policy\_invoker<void ()>::\_\_call\_impl<std::\_\_Cr::\_\_function::\_\_default\_alloc\_func<marl::Scheduler::Worker::start()::$\_0, void ()> >(std::\_\_Cr::\_\_function::\_\_policy\_storage const\*) (\_\_buf=<optimized out>) at ../../third\_party/libc++/src/include/\_\_functional/function.h:725  

#18 0x00007f28e9ba02d0 in std::\_\_Cr::\_\_function::\_\_policy\_func<void ()>::operator()() const (this=0x3a3400aeca70) at ../../third\_party/libc++/src/include/\_\_functional/function.h:856  

#19 std::\_\_Cr::function<void ()>::operator()() const (this=0x3a3400aeca70) at ../../third\_party/libc++/src/include/\_\_functional/function.h:1170  

#20 marl::Thread::Impl::Impl(marl::Thread::Affinity&&, std::\_\_Cr::function<void ()>&&)::{lambda()#1}::operator()() const (this=0x3a3400127f38) at ../../third\_party/swiftshader/third\_party/marl/src/thread.cpp:387  

#21 std::\_\_Cr::\_\_invoke<marl::Thread::Impl::Impl(marl::Thread::Affinity&&, std::\_\_Cr::function<void ()>&&)::{lambda()#1}>(marl::Thread::Impl::Impl(marl::Thread::Affinity&&, std::\_\_Cr::function<void ()>&&)::{lambda()#1}&&) (\_\_f=...) at ../../third\_party/libc++/src/include/\_\_type\_traits/invoke.h:344  

#22 \_ZNSt4\_\_Cr16\_\_thread\_executeINS\_10unique\_ptrINS\_15\_\_thread\_structENS\_14default\_deleteIS2\_EEEEZN4marl6Thread4ImplC1EONS7\_8AffinityEONS\_8functionIFvvEEEEUlvE\_JETpTnmJEEEvRNS\_5tupleIJT\_T0\_DpT1\_EEENS\_15\_\_tuple\_indicesIJXspT2\_EEEE (\_\_t=...) at ../../third\_party/libc++/src/include/\_\_thread/thread.h:220  

#23 std::\_\_Cr::\_\_thread\_proxy<std::\_\_Cr::tuple<std::\_\_Cr::unique\_ptr<std::\_\_Cr::\_\_thread\_struct, std::\_\_Cr::default\_delete[std::\_\_Cr::\_\_thread\_struct](javascript:void(0);) >, marl::Thread::Impl::Impl(marl::Thread::Affinity&&, std::\_\_Cr::function<void ()>&&)::{lambda()#1}> >(void\*) (\_\_vp=0x3a3400127f30)  

at ../../third\_party/libc++/src/include/\_\_thread/thread.h:231  

#24 0x00007f28f0494ac3 in start\_thread (arg=<optimized out>) at ./nptl/pthread\_create.c:442  

#25 0x00007f28f0526a40 in clone3 () at ../sysdeps/unix/sysv/linux/x86\_64/clone3.S:81  

(gdb)

**Additional Comments:**

\*\*Chrome version: \*\* 119.0.0.0 \*\*Channel: \*\* Stable

**OS:** Linux

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 4.0 KB)

## Timeline

### [Deleted User] (2023-11-22)

[Empty comment from Monorail migration]

### pm...@chromium.org (2023-11-22)

I was able  to reproduce locally (Linux M121 and M119)

[Monorail components: Internals>GPU>SwiftShader]

### [Deleted User] (2023-11-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-22)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-11-22)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

syoussefi: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ja...@chromium.org (2023-12-14)

[security shepherd] I've schedule sent a bump to syoussefi@ asking them to take a look.

### [Deleted User] (2023-12-21)

syoussefi: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### sy...@chromium.org (2024-01-15)

@reporter, are there any more logs to look at? Like what are the other threads doing? 

Also, what happens if the test actually deletes the buffers and textures it creates? I'm asking to make sure this is not a run-of-the-mill out-of-memory situation.

### sy...@chromium.org (2024-01-15)

I can try on an ASAN build of Chrome in a few days, but FWIW trying this code in an end2end test, I don't see any ASAN errors. If I stay faithful to the code and leak the buffers and textures I do see memory rise up but my computer is too beefy to hit OOM, lol

### em...@gmail.com (2024-01-15)

When chrome starts, add an additional launch flag '--disable-in-process-stack-traces', and you will see an asan output.
./chrome  --user-data-dir=/tmp/xx22 --incognito  http://localhost:8000/crash.html --disable-gpu --disable-in-process-stack-traces

asan log:
ddressSanitizerAddressSanitizer:DEADLYSIGNAL
:DEADLYSIGNAL
=================================================================
AddressSanitizerAddressSanitizerAddressSanitizerAddressSanitizer:DEADLYSIGNAL
AddressSanitizerAddressSanitizerAddressSanitizerAddressSanitizerAddressSanitizerAddressSanitizerAddressSanitizer:DEADLYSIGNAL
:DEADLYSIGNAL
AddressSanitizer:DEADLYSIGNAL
:DEADLYSIGNAL
:DEADLYSIGNAL
:DEADLYSIGNAL
:DEADLYSIGNAL
:DEADLYSIGNAL
:DEADLYSIGNAL
:DEADLYSIGNAL
AddressSanitizer:DEADLYSIGNAL
:DEADLYSIGNAL
AddressSanitizer:DEADLYSIGNAL
==3996529==ERROR: AddressSanitizer: SEGV on unknown address 0x52e00053cdd0 (pc 0x7f3cdabc11e0 bp 0x7f3cad157010 sp 0x7f3cad156990 T14)
==3996529==The signal is caused by a READ memory access.
/home/pwn11/chromium/src/third_party/llvm-build/Release+Asserts/bin/llvm-symbolizer: error: '/memfd:swiftshader_jit (deleted)': No such file or directory
addr2line: '/memfd:swiftshader_jit (deleted)': No such file
    #0 0x7f3cdabc11e0 in ?? ??:0
    #1 0x7f3cd536149b in operator() ./../../third_party/libc++/src/include/__functional/function.h:711:12
    #2 0x7f3cd536149b in operator() ./../../third_party/libc++/src/include/__functional/function.h:978:10
    #3 0x7f3cd536149b in operator() ./../../third_party/swiftshader/third_party/marl/include/marl/task.h:97:3
    #4 0x7f3cd536149b in marl::Scheduler::Worker::runUntilIdle() ./../../third_party/swiftshader/third_party/marl/src/scheduler.cpp:703:7
    #5 0x7f3cd535eca9 in marl::Scheduler::Worker::runUntilShutdown() ./../../third_party/swiftshader/third_party/marl/src/scheduler.cpp:588:5
    #6 0x7f3cd5360cd9 in marl::Scheduler::Worker::run() ./../../third_party/swiftshader/third_party/marl/src/scheduler.cpp:581:3
    #7 0x7f3cd536bb81 in operator() ./../../third_party/swiftshader/third_party/marl/src/scheduler.cpp:385:11
    #8 0x7f3cd536bb81 in __invoke<(lambda at ../../third_party/swiftshader/third_party/marl/src/scheduler.cpp:372:44) &> ./../../third_party/libc++/src/include/__type_traits/invoke.h:344:25
    #9 0x7f3cd536bb81 in __call<(lambda at ../../third_party/swiftshader/third_party/marl/src/scheduler.cpp:372:44) &> ./../../third_party/libc++/src/include/__type_traits/invoke.h:419:5
    #10 0x7f3cd536bb81 in operator() ./../../third_party/libc++/src/include/__functional/function.h:205:12
    #11 0x7f3cd536bb81 in void std::__Cr::__function::__policy_invoker<void ()>::__call_impl<std::__Cr::__function::__default_alloc_func<marl::Scheduler::Worker::start()::$_0, void ()>>(std::__Cr::__function::__policy_storage const*) ./../../third_party/libc++/src/include/__functional/function.h:605:12
    #12 0x7f3cd53782dc in operator() ./../../third_party/libc++/src/include/__functional/function.h:711:12
    #13 0x7f3cd53782dc in operator() ./../../third_party/libc++/src/include/__functional/function.h:978:10
    #14 0x7f3cd53782dc in operator() ./../../third_party/swiftshader/third_party/marl/src/thread.cpp:387:11
    #15 0x7f3cd53782dc in __invoke<(lambda at ../../third_party/swiftshader/third_party/marl/src/thread.cpp:385:67)> ./../../third_party/libc++/src/include/__type_traits/invoke.h:344:25
    #16 0x7f3cd53782dc in __thread_execute<std::__Cr::unique_ptr<std::__Cr::__thread_struct, std::__Cr::default_delete<std::__Cr::__thread_struct> >, (lambda at ../../third_party/swiftshader/third_party/marl/src/thread.cpp:385:67)> ./../../third_party/libc++/src/include/__thread/thread.h:190:3
    #17 0x7f3cd53782dc in void* std::__Cr::__thread_proxy<std::__Cr::tuple<std::__Cr::unique_ptr<std::__Cr::__thread_struct, std::__Cr::default_delete<std::__Cr::__thread_struct>>, marl::Thread::Impl::Impl(marl::Thread::Affinity&&, std::__Cr::function<void ()>&&)::'lambda'()>>(void*) ./../../third_party/libc++/src/include/__thread/thread.h:199:3

    #18 0x561b443f5918 in asan_thread_start(void*) _asan_rtl_:28

AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV (/memfd:swiftshader_jit (deleted)+0x1e0)
Thread T14 created by T0 (chrome) here:
    #0 0x561b443dd9f1 in ___interceptor_pthread_create _asan_rtl_:3
    #1 0x7f3cd537820a in __libcpp_thread_create ./../../third_party/libc++/src/include/__threading_support:317:10
    #2 0x7f3cd537820a in std::__Cr::thread::thread<marl::Thread::Impl::Impl(marl::Thread::Affinity&&, std::__Cr::function<void ()>&&)::'lambda'(), void>(marl::Thread::Impl::Impl(marl::Thread::Affinity&&, std::__Cr::function<void ()>&&)::'lambda'()&&) ./../../third_party/libc++/src/include/__thread/thread.h:209:14
    #3 0x7f3cd5377b43 in marl::Thread::Impl::Impl(marl::Thread::Affinity&&, std::__Cr::function<void ()>&&) ./../../third_party/swiftshader/third_party/marl/src/thread.cpp:385:60
    #4 0x7f3cd5377958 in marl::Thread::Thread(marl::Thread::Affinity&&, std::__Cr::function<void ()>&&) ./../../third_party/swiftshader/third_party/marl/src/thread.cpp:424:16
    #5 0x7f3cd535ae12 in marl::Scheduler::Worker::start() ./../../third_party/swiftshader/third_party/marl/src/scheduler.cpp:372:16
    #6 0x7f3cd535bf62 in marl::Scheduler::Scheduler(marl::Scheduler::Config const&) ./../../third_party/swiftshader/third_party/marl/src/scheduler.cpp:141:23
    #7 0x7f3cd534ee40 in marl::Scheduler* std::__Cr::construct_at<marl::Scheduler, marl::Scheduler::Config&, marl::Scheduler*>(marl::Scheduler*, marl::Scheduler::Config&) ./../../third_party/libc++/src/include/__memory/construct_at.h:41:46
    #8 0x7f3cd5334c77 in __construct_at<marl::Scheduler, marl::Scheduler::Config &, marl::Scheduler *> ./../../third_party/libc++/src/include/__memory/construct_at.h:49:10
    #9 0x7f3cd5334c77 in construct<marl::Scheduler, marl::Scheduler::Config &, void, void> ./../../third_party/libc++/src/include/__memory/allocator_traits.h:305:5
    #10 0x7f3cd5334c77 in __shared_ptr_emplace<marl::Scheduler::Config &, std::__Cr::allocator<marl::Scheduler>, 0> ./../../third_party/libc++/src/include/__memory/shared_ptr.h:262:5
    #11 0x7f3cd5334c77 in allocate_shared<marl::Scheduler, std::__Cr::allocator<marl::Scheduler>, marl::Scheduler::Config &, void> ./../../third_party/libc++/src/include/__memory/shared_ptr.h:820:51
    #12 0x7f3cd5334c77 in make_shared<marl::Scheduler, marl::Scheduler::Config &, void> ./../../third_party/libc++/src/include/__memory/shared_ptr.h:828:10
    #13 0x7f3cd5334c77 in getOrCreateScheduler ./../../third_party/swiftshader/src/Vulkan/libVulkan.cpp:132:10
    #14 0x7f3cd5334c77 in vkCreateDevice ./../../third_party/swiftshader/src/Vulkan/libVulkan.cpp:1252:19
    #15 0x7f3cd6b31a02 in terminator_CreateDevice ./../../third_party/vulkan-deps/vulkan-loader/src/loader/loader.c:5833:11
    #16 0x7f3cd6b35699 in loader_create_device_chain ./../../third_party/vulkan-deps/vulkan-loader/src/loader/loader.c:4937:15
    #17 0x7f3cd6b33ab5 in loader_layer_create_device ./../../third_party/vulkan-deps/vulkan-loader/src/loader/loader.c:4317:11
    #18 0x7f3cd6b4aa38 in vkCreateDevice ./../../third_party/vulkan-deps/vulkan-loader/src/loader/trampoline.c:1004:20
    #19 0x7f3cd7b5b225 in rx::RendererVk::createDeviceAndQueue(rx::DisplayVk*, unsigned int) ./../../third_party/angle/src/libANGLE/renderer/vulkan/RendererVk.cpp:3452:5
    #20 0x7f3cd7b55a2a in rx::RendererVk::initialize(rx::DisplayVk*, egl::Display*, char const*, char const*) ./../../third_party/angle/src/libANGLE/renderer/vulkan/RendererVk.cpp:1965:9
    #21 0x7f3cd7ac9022 in rx::DisplayVk::initialize(egl::Display*) ./../../third_party/angle/src/libANGLE/renderer/vulkan/DisplayVk.cpp:110:39
    #22 0x7f3cd7dbe170 in rx::DisplayVkXcb::initialize(egl::Display*) ./../../third_party/angle/src/libANGLE/renderer/vulkan/linux/xcb/DisplayVkXcb.cpp:65:23
    #23 0x7f3cd7f9a22d in egl::Display::initialize() ./../../third_party/angle/src/libANGLE/Display.cpp:1048:36
    #24 0x7f3cd79d635f in egl::Initialize(egl::Thread*, egl::Display*, int*, int*) ./../../third_party/angle/src/libGLESv2/egl_stubs.cpp:514:5
    #25 0x7f3cd79de65f in EGL_Initialize ./../../third_party/angle/src/libGLESv2/entry_points_egl_autogen.cpp:478:27
    #26 0x7f3cd6f07a9e in eglInitialize ./../../third_party/angle/src/libEGL/libEGL_autogen.cpp:177:12
    #27 0x561b5d3feb92 in gl::GLDisplayEGL::InitializeDisplay(bool, std::__Cr::vector<gl::DisplayType, std::__Cr::allocator<gl::DisplayType>>, gl::EGLDisplayPlatform, gl::GLDisplayEGL*) ./../../ui/gl/gl_display.cc:783:10
    #28 0x561b5d3fbffc in gl::GLDisplayEGL::Initialize(bool, std::__Cr::vector<gl::DisplayType, std::__Cr::allocator<gl::DisplayType>>, gl::EGLDisplayPlatform) ./../../ui/gl/gl_display.cc:673:8
    #29 0x561b46f36d78 in ui::GLOzoneEGL::InitializeGLOneOffPlatform(bool, std::__Cr::vector<gl::DisplayType, std::__Cr::allocator<gl::DisplayType>>, gl::GpuPreference) ./../../ui/ozone/common/gl_ozone_egl.cc:25:17
    #30 0x561b61dd6ab2 in gl::init::InitializeGLOneOffPlatform(gl::GpuPreference) ./../../ui/gl/init/gl_initializer_ozone.cc:27:26
    #31 0x561b61dd41cb in gl::init::InitializeGLOneOffPlatformImplementation(bool, bool, bool, gl::GpuPreference) ./../../ui/gl/init/gl_factory.cc:211:24
    #32 0x561b61dd39cd in gl::init::(anonymous namespace)::InitializeGLOneOffPlatformHelper(bool, gl::GpuPreference) ./../../ui/gl/init/gl_factory.cc:135:10
    #33 0x561b61dd3e72 in gl::init::InitializeGLNoExtensionsOneOff(bool, gl::GpuPreference) ./../../ui/gl/init/gl_factory.cc:166:10
    #34 0x561b61e3b211 in gpu::GpuInit::InitializeAndStartSandbox(base::CommandLine*, gpu::GpuPreferences const&) ./../../gpu/ipc/service/gpu_init.cc:446:18
    #35 0x561b72292f23 in content::GpuMain(content::MainFunctionParams) ./../../content/gpu/gpu_main.cc:359:39
    #36 0x561b558683c9 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:676:14
    #37 0x561b55869dc3 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:780:12
    #38 0x561b5586cddb in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1142:10
    #39 0x561b55865f55 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:335:36
    #40 0x561b55866682 in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:348:10
    #41 0x561b4442de8d in ChromeMain ./../../chrome/app/chrome_main.cc:194:12
    #42 0x7f3ce0429d8f in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16


==3996529==ADDITIONAL INFO

==3996529==Note: Please include this section with the ASan report.
Task trace:


==3996529==END OF ADDITIONAL INFO
==3996529==ABORTING
[3996470:3996470:0116/053601.602196:ERROR:gpu_process_host.cc(991)] GPU process exited unexpectedly: exit_code=134


### sy...@chromium.org (2024-01-18)

Thank you, I can reproduce the issue.

### sy...@chromium.org (2024-01-18)

Tweaking crash.html, it seems that the issue really is in the call to `texelFetch`, which is given an LOD of 0x7fff. Looks like SwiftShader doesn't clamp that value. Setting it to 0 fixes the crash, setting it to 50 reproduces the crash. A small value like 1 or 10 doesn't repro, presumably due to ANGLE's memory suballocation.

### gi...@appspot.gserviceaccount.com (2024-01-22)

The following revision refers to this bug:
  https://swiftshader.googlesource.com/SwiftShader/+/5ab5177fc72dbb67f7353f1cfeb5ef64d67cfc67

commit 5ab5177fc72dbb67f7353f1cfeb5ef64d67cfc67
Author: Shahbaz Youssefi <syoussefi@google.com>
Date: Fri Jan 19 20:36:25 2024

Clamp LOD during image Fetch for robustness

Bug: chromium:1504556
Change-Id: Ie110fe4e1b065a815c09986ab91b1336ef4761ad
Reviewed-on: https://swiftshader-review.googlesource.com/c/SwiftShader/+/72948
Presubmit-Ready: Shahbaz Youssefi <syoussefi@google.com>
Kokoro-Result: kokoro <noreply+kokoro@google.com>
Reviewed-by: Ben Clayton <bclayton@google.com>
Commit-Queue: Ben Clayton <bclayton@google.com>
Tested-by: Ben Clayton <bclayton@google.com>

[modify] https://swiftshader.googlesource.com/SwiftShader/+/5ab5177fc72dbb67f7353f1cfeb5ef64d67cfc67/src/Pipeline/SamplerCore.cpp
[modify] https://swiftshader.googlesource.com/SwiftShader/+/5ab5177fc72dbb67f7353f1cfeb5ef64d67cfc67/src/Vulkan/VkImageView.cpp
[modify] https://swiftshader.googlesource.com/SwiftShader/+/5ab5177fc72dbb67f7353f1cfeb5ef64d67cfc67/src/Pipeline/SpirvShaderSampling.cpp
[modify] https://swiftshader.googlesource.com/SwiftShader/+/5ab5177fc72dbb67f7353f1cfeb5ef64d67cfc67/src/Vulkan/VkImageView.hpp


### em...@gmail.com (2024-01-22)

Thank you for the quick fix. After testing, the original PoC no longer reproduces the issue. However, modifying it to negative numbers still reproduces the issue, for example:
-1 or 0xffffffff.

### sy...@chromium.org (2024-01-22)

Oops, looks like a clamp to min lod is also needed. Thanks for checking that.

### gi...@appspot.gserviceaccount.com (2024-01-22)

The following revision refers to this bug:
  https://swiftshader.googlesource.com/SwiftShader/+/3bc9ccd923dafcaf43c63da60dd56e4d3050db39

commit 3bc9ccd923dafcaf43c63da60dd56e4d3050db39
Author: Shahbaz Youssefi <syoussefi@google.com>
Date: Mon Jan 22 14:49:16 2024

Clamp min LOD during image Fetch for robustness

The previous change clamped max LOD only, but min LOD also needs
clamping because texelFetch takes an `int` as LOD instead of `uint`.

Bug: chromium:1504556
Change-Id: Ibae8250a877b3e04b71fac45a40b77c78756d6c8
Reviewed-on: https://swiftshader-review.googlesource.com/c/SwiftShader/+/72968
Kokoro-Result: kokoro <noreply+kokoro@google.com>
Reviewed-by: Ben Clayton <bclayton@google.com>
Tested-by: Shahbaz Youssefi <syoussefi@google.com>
Commit-Queue: Shahbaz Youssefi <syoussefi@google.com>
Presubmit-Ready: Shahbaz Youssefi <syoussefi@google.com>

[modify] https://swiftshader.googlesource.com/SwiftShader/+/3bc9ccd923dafcaf43c63da60dd56e4d3050db39/src/Pipeline/SamplerCore.cpp
[modify] https://swiftshader.googlesource.com/SwiftShader/+/3bc9ccd923dafcaf43c63da60dd56e4d3050db39/src/Vulkan/VkImageView.cpp
[modify] https://swiftshader.googlesource.com/SwiftShader/+/3bc9ccd923dafcaf43c63da60dd56e4d3050db39/src/Pipeline/SpirvShaderSampling.cpp
[modify] https://swiftshader.googlesource.com/SwiftShader/+/3bc9ccd923dafcaf43c63da60dd56e4d3050db39/src/Vulkan/VkImageView.hpp


### gi...@appspot.gserviceaccount.com (2024-01-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/f794c9c2bbf25c1502e1702b6365952c329f86f9

commit f794c9c2bbf25c1502e1702b6365952c329f86f9
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Mon Jan 22 14:56:08 2024

Tests for out-of-bounds LOD in texelFetch

Bug: chromium:1504556
Change-Id: I3a92da00d9a8781122c7218f22a681839783dc7e
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5225080
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-by: Yuxin Hu <yuxinhu@google.com>

[modify] https://crrev.com/f794c9c2bbf25c1502e1702b6365952c329f86f9/src/tests/gl_tests/GLSLTest.cpp


### gi...@appspot.gserviceaccount.com (2024-01-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5f944e997f5a9c00a2f83e54d9c2ad59370d9ccc

commit 5f944e997f5a9c00a2f83e54d9c2ad59370d9ccc
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Jan 24 01:14:34 2024

Roll ANGLE from 317108d6ac82 to 81a43bd703a7 (12 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/317108d6ac82..81a43bd703a7

2024-01-23 romanl@google.com Tests: skip TexelFetchLodOutOfBounds on SwS
2024-01-23 romanl@google.com Add third_party/dawn to .gitignore
2024-01-23 romanl@google.com Trace tests: extend warmup to at least 1.5s
2024-01-23 romanl@google.com Tests: skip UniformUsageCombinations test on SwS
2024-01-23 syoussefi@chromium.org Tests for out-of-bounds LOD in texelFetch
2024-01-23 angle-autoroll@skia-public.iam.gserviceaccount.com Roll SwiftShader from 5ab5177fc72d to 3bc9ccd923da (1 revision)
2024-01-23 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from 6d5cc7186844 to 2e1050880b38 (298 revisions)
2024-01-23 syoussefi@chromium.org Vulkan: Never delay device and queue selection
2024-01-22 lexa.knyazev@gmail.com Metal: Skip array index clamp for constant values
2024-01-22 angle-autoroll@skia-public.iam.gserviceaccount.com Manual roll Chromium from 32cda1ad29f0 to 6d5cc7186844 (1322 revisions)
2024-01-22 romanl@google.com android_helper: fix corner-case byte/string mismatch
2024-01-22 syoussefi@chromium.org Vulkan: Fix input attachments leaking into uniform list

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC angle-team@google.com,romanl@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://issues.skia.org/issues/new?component=1389291&template=1850622

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1504556
Tbr: romanl@google.com
Change-Id: I1c0357c4acb7596b3e175eb9d0452fcef91464a6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5230567
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1251161}

[modify] https://crrev.com/5f944e997f5a9c00a2f83e54d9c2ad59370d9ccc/DEPS
[modify] https://crrev.com/5f944e997f5a9c00a2f83e54d9c2ad59370d9ccc/third_party/angle


### sy...@chromium.org (2024-02-01)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2024-02-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b503c930adce021f8638a12273230dff2b501fe6

commit b503c930adce021f8638a12273230dff2b501fe6
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Feb 01 23:50:13 2024

Roll SwiftShader from 2fa7e9b99ae4 to eb75201a4e03 (10 revisions)

https://swiftshader.googlesource.com/SwiftShader.git/+log/2fa7e9b99ae4..eb75201a4e03

2024-02-01 syoussefi@google.com Revert "Default to use llvm16"
2024-02-01 yuxinhu@google.com Add llvm-16.0 required files for windows platform
2024-02-01 yuxinhu@google.com Revert^2 "LLVMReactor: Remove CreateFreeze() call"
2024-01-30 rsworktech@outlook.com Default to use llvm16
2024-01-30 syoussefi@google.com Fix MSAN complaint about uninitialized (and unused) value
2024-01-26 thakis@chromium.org Merge two upstream LLVM commits
2024-01-22 syoussefi@google.com Clamp min LOD during image Fetch for robustness
2024-01-22 syoussefi@google.com Clamp LOD during image Fetch for robustness
2024-01-17 syoussefi@google.com Support VK_EXT_vertex_input_dynamic_state
2024-01-10 natsu@google.com Revert "LLVMReactor: Remove CreateFreeze() call"

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/swiftshader-chromium-autoroll
Please CC alanbaker@google.com,capn@chromium.org,swiftshader-eng+autoroll@google.com,yuxinhu@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in SwiftShader: https://bugs.chromium.org/p/swiftshader/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://issues.skia.org/issues/new?component=1389291&template=1850622

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:linux_chromium_msan_rel_ng;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1504556,chromium:1520616
Tbr: alanbaker@google.com,swiftshader-eng+autoroll@google.com,yuxinhu@google.com
Change-Id: Ib67cc847b2de886971322af180c1c664b4275d2d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5259664
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1255354}

[modify] https://crrev.com/b503c930adce021f8638a12273230dff2b501fe6/third_party/swiftshader
[modify] https://crrev.com/b503c930adce021f8638a12273230dff2b501fe6/DEPS


### [Deleted User] (2024-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2024-02-02)

[Empty comment from Monorail migration]

### is...@google.com (2024-02-02)

This issue was migrated from crbug.com/chromium/1504556?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### am...@google.com (2024-02-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-14)

Congratulations on another one this week, Cassidy Kim! The Chrome VRP Panel has decided to award you $10,000 for this report of GPU process memory corruption issues. Thank you for your efforts and reporting this issue to us!

### pe...@google.com (2024-05-10)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40945098)*
