# SEGV in vk::Image::clear()

| Field | Value |
|-------|-------|
| **Issue ID** | [40057228](https://issues.chromium.org/issues/40057228) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>GPU>SwiftShader |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | at...@gmail.com |
| **Assignee** | ni...@google.com |
| **Created** | 2021-09-10 |
| **Bounty** | $5,000.00 |

## Description


Tested on:
  OS: Ubuntu 20.04
  Chromium: asan-linux-debug-920244 from ttps://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-debug%2Fasan-linux-debug-920244.zip?generation=1631293316584801&alt=media

To reproduce:

export ASAN_OPTIONS="external_symbolizer_path=/chromium/llvm-symbolizer:symbolize=1:alloc_dealloc_mismatch=0:allocator_may_return_null=0:allow_user_segv_handler=0:check_malloc_usable_size=0:detect_leaks=0:detect_odr_violation=0:detect_stack_use_after_return=1:fast_unwind_on_fatal=1:handle_abort=1:handle_segv=1:handle_sigbus=1:handle_sigfpe=1:handle_sigill=1:malloc_context_size=128:max_uar_stack_size_log=16:print_scariness=1:print_summary=1:print_suppressions=0:redzone=128:strict_memcmp=0:use_sigaltstack=1"

CHROMIUM_ARGS='--disable-test-root-certs --disable-in-process-stack-traces --no-user-gesture-required --no-sandbox --window-size=480,242 --window-position=304,118 --js-flags="--expose-gc --verify-heap" --no-first-run --enable-features=PreloadMediaEngagementData,AutoplayIgnoreWebAudio,MediaEngagementBypassAutoplayPolicies --use-gl=angle --use-angle=swiftshader'
		
:$ /chromium/chrome $CHROMIUM_ARGS ./SEGV--Imageclear-CommandBuffersubmit-QueuesubmitQueue1-min.html

Note that you need to use commandline flag "--use-angle=swiftshader" to reproduce.

ASAN-output:

[317898:317898:0911/000101.002458:ERROR:power_monitor_device_source_stub.cc(11)] Not implemented reached in virtual bool base::PowerMonitorDeviceSource::IsOnBatteryPower()
[317898:317898:0911/000101.006865:INFO:content_main_runner_impl.cc(1100)] Chrome is running in full browser mode.
[317898:317898:0911/000101.902521:WARNING:account_consistency_mode_manager.cc(68)] Desktop Identity Consistency cannot be enabled as no OAuth client ID and client secret have been configured.
[317898:317916:0911/000103.483988:WARNING:bus.cc(637)] Bus::SendWithReplyAndBlock took 1363ms to process message: type=method_call, path=/org/freedesktop/Notifications, interface=org.freedesktop.Notifications, member=GetServerInformation
[317924:317924:0911/000104.007142:ERROR:sandbox_linux.cc(374)] InitializeSandbox() called with multiple threads in process gpu-process.
INFO: GL performance: HIGH: GPU stall due to ReadPixels
INFO: GL performance: HIGH: GPU stall due to ReadPixels
INFO: GL performance: LOW: Repeated Clear on framebuffer attachment dropped
AddressSanitizer:DEADLYSIGNAL
=================================================================
==317924==ERROR: AddressSanitizer: SEGV on unknown address 0x629000180000 (pc 0x7f5acd0e114f bp 0x7f5ad8bf2e80 sp 0x7f5ad8bf2c20 T7)
==317924==The signal is caused by a WRITE memory access.
INFO: GL performance: HIGH: GPU stall due to ReadPixels
SCARINESS: 30 (wild-addr-write)
LLVMSymbolizer: error reading file: No such file or directory
    #0 0x7f5acd0e114f  (/memfd:swiftshader_jit (deleted)+0x14f)
    #1 0x7f5adcf53638 in vk::Image::clear(VkClearColorValue const&, VkImageSubresourceRange const&) third_party/swiftshader/src/Vulkan/VkImage.cpp:1039:24
    #2 0x7f5adcefb869 in vk::CommandBuffer::submit(vk::CommandBuffer::ExecutionState&) third_party/swiftshader/src/Vulkan/VkCommandBuffer.cpp:1742:12
    #3 0x7f5adcf6f566 in vk::Queue::submitQueue(vk::Queue::Task const&) third_party/swiftshader/src/Vulkan/VkQueue.cpp:221:42
    #4 0x7f5adcf6d23c in vk::Queue::taskLoop(marl::Scheduler*) third_party/swiftshader/src/Vulkan/VkQueue.cpp:274:4
.
.
.
    #8 0x7f5b0037e608 in start_thread /build/glibc-eX1tMB/glibc-2.31/nptl/pthread_create.c:477:8

AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV (/memfd:swiftshader_jit (deleted)+0x14f) 
Thread T7 created by T0 (chrome) here:
[317898:317935:0911/000111.375621:ERROR:chrome_browser_main_extra_parts_metrics.cc(230)] crbug.com/1216328: Checking Bluetooth availability started. Please report if there is no report that this ends.
[317898:317935:0911/000111.377285:ERROR:chrome_browser_main_extra_parts_metrics.cc(233)] crbug.com/1216328: Checking Bluetooth availability ended.
[317898:317935:0911/000111.377550:ERROR:chrome_browser_main_extra_parts_metrics.cc(236)] crbug.com/1216328: Checking default browser status started. Please report if there is no report that this ends.
[317898:317935:0911/000111.483190:ERROR:chrome_browser_main_extra_parts_metrics.cc(240)] crbug.com/1216328: Checking default browser status ended.
    #0 0x55b0832701ec in pthread_create /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:207:3
    #1 0x7f5adcf6cf7c in __libcpp_thread_create buildtools/third_party/libc++/trunk/include/__threading_support:513:10
    #2 0x7f5adcf6cf7c in thread<void (vk::Queue::*)(marl::Scheduler *), vk::Queue *, marl::Scheduler *&, void> buildtools/third_party/libc++/trunk/include/thread:307:16
    #3 0x7f5adcf6cf7c in vk::Queue::Queue(vk::Device*, marl::Scheduler*) third_party/swiftshader/src/Vulkan/VkQueue.cpp:139:16
    #4 0x7f5adcf14a58 in vk::Device::Device(VkDeviceCreateInfo const*, void*, vk::PhysicalDevice*, VkPhysicalDeviceFeatures const*, std::__Cr::shared_ptr<marl::Scheduler> const&) third_party/swiftshader/src/Vulkan/VkDevice.cpp:139:26

.
.
.
    #37 0x55b0832bf491 in main chrome/app/chrome_exe_main_aura.cc:17:10
    #38 0x7f5aff92b0b2 in __libc_start_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16

==317924==ABORTING
[317898:317898:0911/000112.114641:ERROR:gpu_process_host.cc(958)] GPU process exited unexpectedly: exit_code=256
[317898:317898:0911/000112.114940:WARNING:gpu_process_host.cc(1271)] The GPU process has crashed 1 time(s)
[318054:318054:0911/000114.741227:ERROR:sandbox_linux.cc(374)] InitializeSandbox() called with multiple threads in process gpu-process.
[317898:317898:0911/000114.785163:WARNING:gpu_process_host.cc(986)] Reinitialized the GPU process after a crash. The reported initialization time was 2572 ms
[317898:317898:0911/000114.963113:INFO:CONSOLE(0)] "WebGL: CONTEXT_LOST_WEBGL: loseContext: context lost", source: file:///home/attekett/results/SEGV--Imageclear-CommandBuffersubmit-QueuesubmitQueue/SEGV--Imageclear-CommandBuffersubmit-QueuesubmitQueue1-min.html (0)
INFO: GL performance: HIGH: GPU stall due to ReadPixels
INFO: GL performance: HIGH: GPU stall due to ReadPixels



## Attachments

- [SEGV--Imageclear-CommandBuffersubmit-QueuesubmitQueue1-min.html](attachments/SEGV--Imageclear-CommandBuffersubmit-QueuesubmitQueue1-min.html) (text/plain, 594 B)
- [SEGV--Imageclear-CommandBuffersubmit-QueuesubmitQueue.log](attachments/SEGV--Imageclear-CommandBuffersubmit-QueuesubmitQueue.log) (text/plain, 10.0 KB)

## Timeline

### [Deleted User] (2021-09-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-09-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4976615573225472.

### ad...@google.com (2021-09-11)

Reproduced with asan-linux-debug-920244.

[Monorail components: Internals>GPU>SwiftShader]

### ad...@google.com (2021-09-11)

Severity => GPU process OOB write. GPU process is somewhat sandboxed so we rate this as High.

Also reproduced with ASAN 902204 => FoundIn-93, i.e. stable.

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-09-11)

Detailed Report: https://clusterfuzz.com/testcase?key=4976615573225472

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN WRITE
Crash Address: 0x6290000b0000
Crash State:
  memfd:swiftshader_jit
  vk::Image::clear
  vk::CommandBuffer::submit
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=896834:896839

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4976615573225472

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/4976615573225472 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### [Deleted User] (2021-09-11)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### su...@chromium.org (2021-09-13)

This piece of code:

    const width = 0xc2;
    const height = 0x541;
    const depth = 0x404;
    gl.texStorage3D(gl.TEXTURE_3D, 1, gl.RGBA32F, width, height, depth);

would allocate 194 * 1346 (1345 rounded up no next even number) * 1028 pixels or 268,435,472 pixels.
This, with the extra 16 bytes at the end, would require 4,294,967,568 bytes, which is just over 4 GB of memory.

The regression CL is identified as:
https://swiftshader-review.googlesource.com/c/SwiftShader/+/55248
but all this did was increase the maximum depth from 1024 to 2048, allowing the 1028 depth in this example, but this bug is probably also reproducible if you halve the depth and double the width, in order to allocate the exact same amount of memory.

capn@, can you check why allocating just over 4 GB of memory would cause an issue?

### at...@gmail.com (2021-09-21)

I have been seeing this crash on my fuzzing cluster. Interesting thing is that with the values from the original repro the SEGV address is pretty stable:

In the original repro, the value were, in decimal:

      const width = 194;
      const height = 1345;
      const depth = 1028;

When repeating the crash, the address stays some what same:

==765480==ERROR: AddressSanitizer: SEGV on unknown address 0x629000160000 (pc 0x7f0b76dc914f bp 0x7f0b7d24d460 sp 0x7f0b7d24d200 T10)
==765648==ERROR: AddressSanitizer: SEGV on unknown address 0x6290001c0000 (pc 0x7f2f7732b14f bp 0x7f2f7d4cf460 sp 0x7f2f7d4cf200 T10)
==766281==ERROR: AddressSanitizer: SEGV on unknown address 0x629000180000 (pc 0x7f10f329314f bp 0x7f10ed182460 sp 0x7f10ed182200 T10)
==765925==ERROR: AddressSanitizer: SEGV on unknown address 0x629000120000 (pc 0x7fd80ada914f bp 0x7fd804b25460 sp 0x7fd804b25200 T10)

If the values of width, height, or depth are changed, the behavior changes, if for example you change the value of height in repro to:

	const height = 1340;

(Which is decimal value -5 from the original hex.)

You get internal Vulkan error and a null-pointer crash.

764448:764448:0921/153438.666252:ERROR:gl_utils.cc(314)] [.WebGL-0x61b000043d80] GL_OUT_OF_MEMORY: Internal Vulkan error (-2): A device memory allocation has failed.
==764448==ERROR: AddressSanitizer: SEGV on unknown address 0x000000000008 (pc 0x7fa0c18f52e9 bp 0x7fa0bc55e250 sp 0x7fa0bc55e250 T10)
==764448==The signal is caused by a READ memory access.
==764448==Hint: address points to the zero page.
SCARINESS: 10 (null-deref)
    #0 0x7fa0c18f52e9 in vk::DeviceMemory::getOffsetPointer(unsigned long) const third_party/swiftshader/src/Vulkan/VkDeviceMemory.cpp:348:42
    #1 0x7fa0c1964fbf in sw::Blitter::clear(void*, vk::Format, vk::Image*, vk::Format const&, VkImageSubresourceRange const&, VkRect2D const*) third_party/swiftshader/src/Device/Blitter.cpp:155:24
    #2 0x7fa0c1906eee in vk::Image::clear(VkClearColorValue const&, VkImageSubresourceRange const&) third_party/swiftshader/src/Vulkan/VkImage.cpp:1043:24
    #3 0x7fa0c18db10e in vk::CommandBuffer::submit(vk::CommandBuffer::ExecutionState&) third_party/swiftshader/src/Vulkan/VkCommandBuffer.cpp:1742:12

null-pointer is not that exiting, but if you instead change:

      const width = 196;

You get SEGV to different address range:

AddressSanitizer:DEADLYSIGNAL
=================================================================
==767676==ERROR: AddressSanitizer: SEGV on unknown address 0x7f5ef1eb7000 (pc 0x7f5f1aa0914f bp 0x7f5f144a3460 sp 0x7f5f144a3200 T10)
==767920==ERROR: AddressSanitizer: SEGV on unknown address 0x7f56e710c000 (pc 0x7f56e9ea014f bp 0x7f56f275e460 sp 0x7f56f275e200 T10)
==768156==ERROR: AddressSanitizer: SEGV on unknown address 0x7f88147aa000 (pc 0x7f8817dc514f bp 0x7f881df5e460 sp 0x7f881df5e200 T10)

Stack trace of the crash still stays the same.


### ca...@chromium.org (2021-09-22)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-22)

The following revision refers to this bug:
  https://swiftshader.googlesource.com/SwiftShader/+/4e3812937c5f2835c861a3e578d9f063b88bbfe3

commit 4e3812937c5f2835c861a3e578d9f063b88bbfe3
Author: Nicolas Capens <capn@google.com>
Date: Wed Sep 22 05:11:42 2021

Compute the image size in 64-bit arithmetic

The size of a 2D 'slice' is returned in a 32-bit value, which is
sufficient for the maximum supported dimensions of 8192x8192, but for
3D images we need to multiply by the depth in 64-bit to avoid numerical
overflow.

Note that currently we only allow memory allocations up to 1 GiB, but
this change fixes correctly reporting how much memory would be required,
from a call to vkGetImageMemoryRequirements().

Bug: chromium:1248567
Change-Id: Ic055790b4ae53355a90a173b824e94e3c5933316
Reviewed-on: https://swiftshader-review.googlesource.com/c/SwiftShader/+/57268
Kokoro-Result: kokoro <noreply+kokoro@google.com>
Tested-by: Nicolas Capens <nicolascapens@google.com>
Reviewed-by: Alexis Hétu <sugoi@google.com>

[modify] https://swiftshader.googlesource.com/SwiftShader/+/4e3812937c5f2835c861a3e578d9f063b88bbfe3/src/Vulkan/VkImage.cpp


### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d38c55d07e913fd1d313dc3c3bab16b0ae26a005

commit d38c55d07e913fd1d313dc3c3bab16b0ae26a005
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Sep 22 20:29:21 2021

Roll SwiftShader from 755b78dc66b2 to 4e3812937c5f (1 revision)

https://swiftshader.googlesource.com/SwiftShader.git/+log/755b78dc66b2..4e3812937c5f

2021-09-22 capn@google.com Compute the image size in 64-bit arithmetic

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/swiftshader-chromium-autoroll
Please CC swiftshader-eng+autoroll@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in SwiftShader: https://bugs.chromium.org/p/swiftshader/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_chromium_msan_rel_ng;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1248567
Tbr: swiftshader-eng+autoroll@google.com
Change-Id: I9bd5bfc83552a7e17f29e9dd7a9e2bb5cb2f803c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3175520
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#924017}

[modify] https://crrev.com/d38c55d07e913fd1d313dc3c3bab16b0ae26a005/DEPS


### ni...@google.com (2021-09-22)

This issue has been fixed, but I've filed https://issuetracker.google.com/200806413 as a follow-up to avoid/detect similar bugs.

I've lowered the security severity because fortunately ANGLE will clear every image that has been created, and writing out of bounds by ~4 GB will undoubtedly result in crashing the GPU process, which is acceptable.

### [Deleted User] (2021-09-23)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-09-23)

ClusterFuzz testcase 4976615573225472 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=924011:924017

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### am...@google.com (2021-10-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-10-20)

Congratulations, Atte! The VRP Panel has decided to award you $5000 for this report. Thanks for your efforts and this report!  

### am...@google.com (2021-10-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-11-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-11-11)

(Sheriffbot didn't ask for merges here. That Sheriffbot bug is tracked as https://crbug.com/chromium/1262390).

### ad...@google.com (2021-11-12)

[Empty comment from Monorail migration]

### am...@google.com (2021-12-23)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1248567?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057228)*
