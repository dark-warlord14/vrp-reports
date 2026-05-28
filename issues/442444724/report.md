# Heap-buffer-overflow/wild-read in dawn::native::`anonymous namespace'::ReflectEntryPointUsingTint 

| Field | Value |
|-------|-------|
| **Issue ID** | [442444724](https://issues.chromium.org/issues/442444724) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Dawn |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | at...@gmail.com |
| **Assignee** | gm...@chromium.org |
| **Created** | 2025-09-02 |
| **Bounty** | $25,000.00 |

## Description



Tested on:
 Chromium:  141.0.7379.0 (Developer Build) (64-bit) 
 OS:	Windows 11 Version 24H2 (Build 26100.4946)

GPU-info: Integrated AMD Radeon Graphics of AMD Ryzen 5 5625U

To reproduce run attached .html with '--enable-experimental-web-platform-features' flag.

chromium-141.0.7379.0-win64-asan\chrome.exe --enable-experimental-web-platform-features heap-buffer-overflow-dawnnativeReflectEntryPointUsingTint.html

Reproduces also on Ubuntu 22.04 with '--enable-unsafe-webgpu', but doesn't require '--enable-experimental-web-platform-features'.

ASAN-trace:

==18232==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x1207e5f47bc0 at pc 0x7ffd880d6c79 bp
0x000893ffd030 sp 0x000893ffd078
READ of size 8 at 0x1207e5f47bc0 thread T0
SCARINESS: 33 (8-byte-read-heap-buffer-overflow-far-from-bounds)
    #0 0x7ffd880d6c78 in absl::container_internal::raw_hash_set<absl::container_internal::FlatHashMapPolicy<unsigned int,dawn::native::ShaderBindingInfo>,absl::hash_internal::Hash<unsigned int>,std::__Cr::equal_to<unsigned int>,std::__Cr::allocator<std::__Cr::pair<const unsigned int,dawn::native::ShaderBindingInfo> > >::find<unsigned int> C:\b\s\w\ir\cache\builder\src\third_
party\abseil-cpp\absl\container\internal\raw_hash_set.h:2815
    #1 0x7ffd880ce340 in dawn::native::`anonymous namespace'::ReflectEntryPointUsingTint C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\ShaderModule.cpp:1316
    #2 0x7ffd880bbe2c in dawn::native::ParseShaderModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\ShaderModule.cpp:1571
    #3 0x7ffd87f69109 in dawn::native::LoadOrRun<dawn::Result<dawn::native::ShaderModuleParseResult,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::ShaderModuleParseResult,dawn::native::ErrorData> (*)(dawn::native::ShaderModuleParseRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:165
    #4 0x7ffd87f33d7b in dawn::native::DeviceBase::CreateShaderModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:2231
    #5 0x7ffd87f49789 in dawn::native::DeviceBase::APICreateShaderModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1448
    #6 0x7ffd9dc610bd in dawn::wire::server::Server::DoDeviceCreateShaderModule C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:328
    #7 0x7ffd9dc73e24 in dawn::wire::server::Server::HandleDeviceCreateShaderModule C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:643
    #8 0x7ffd9dc78acb in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1706
    #9 0x7ffd9dc97412 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:156
    #10 0x7ffd9dc97865 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1963
    #11 0x7ffd9dc8d201 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1908
    #12 0x7ffd88c18213 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:266
    #13 0x7ffd9dd269de in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:495
    #14 0x7ffd9dd258e5 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:162
    #15 0x7ffd9dcf0beb in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:848
    #16 0x7ffd9dd00b83 in base::internal::Invoker<base::internal::FunctorTraits<void (GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *),base::WeakPtr<gpu::GpuChannel> &&,mojo::StructPtr<gpu::mojom::DeferredRequestParams> &&>,base::internal::BindState<1,1,0,void (GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestPara
ms>, gpu::FenceSyncReleaseDelegate *),base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams> >,void (gpu::FenceSyncReleaseDelegate *)>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:973
    #17 0x7ffd88c5839d in base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)> &&,gpu::FenceSyncReleaseDelegate *>,base::internal::BindState<0,1,1,base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>,base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate,base::unretained_traits::MayNotDangle,0> >,void
 ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>,std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate,base::unretained_traits::MayNotDangle,0> >,0> C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1060
    #18 0x7ffd88c2bfd0 in gpu::Scheduler::ExecuteSequence C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc:672
    #19 0x7ffd88c29c6d in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc:594
    #20 0x7ffd88c2f468 in base::internal::Invoker<base::internal::FunctorTraits<void (Scheduler::*&&)(),gpu::Scheduler *>,base::internal::BindState<1,1,0,void (Scheduler::*)(),base::internal::UnretainedWrapper<gpu::Scheduler,base::unretained_traits::MayNotDangle,0> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:973
    #21 0x7ffd98e138c3 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:207
    #22 0x7ffd98de6a19 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:472
    #23 0x7ffd98de58bf in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:346
    #24 0x7ffd98f48b32 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:42
    #25 0x7ffd98de8761 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:647
    #26 0x7ffd98e8638e in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #27 0x7ffda2326ab5 in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu_main.cc:474
    #28 0x7ffd94f18a40 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:763
    #29 0x7ffd94f1ae73 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1129
    #30 0x7ffd94f0f3cf in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:346
    #31 0x7ffd94f0f95d in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:359
    #32 0x7ffd85cd301f in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:228
    #33 0x7ff76a84479b in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:201
    #34 0x7ff76a84200c in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:352
    #35 0x7ff76acffa2f in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #36 0x7ffeb034e8d6 in BaseThreadInitThunk+0x16 (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #37 0x7ffeb1d5c34b in RtlUserThreadStart+0x2b (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18003c34b)
Address 0x1207e5f47bc0 is a wild pointer inside of access range of size 0x000000000008.
SUMMARY: AddressSanitizer: heap-buffer-overflow C:\b\s\w\ir\cache\builder\src\third_party\abseil-cpp\absl\container\internal\raw_hash_set.h:2815 in absl::container_internal::raw_hash_set<absl::container_internal::FlatHashMapPolicy<unsigned int,dawn::native::ShaderBindingInfo>,absl::hash_internal::Hash<unsigned int>,std::__Cr::equal_to<unsigned int>,std::__Cr::allocator<std::
__Cr::pair<const unsigned int,dawn::native::ShaderBindingInfo> > >::find<unsigned int>
Shadow bytes around the buggy address:
  0x1207e5f47900: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1207e5f47980: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1207e5f47a00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1207e5f47a80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1207e5f47b00: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa
=>0x1207e5f47b80: fa fa fa fa fa fa fa fa[fa]fa fa fa fa fa fa fa
  0x1207e5f47c00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x1207e5f47c80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1207e5f47d00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1207e5f47d80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1207e5f47e00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==18232==ADDITIONAL INFO
==18232==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffd88c2a1fc in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc:610
    #1 0x7ffd88c2a1fc in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc:610
    #2 0x7ffd88c2a1fc in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc:610
    #3 0x7ffd88c2a1fc in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc:610
Command line: `"chromium-141.0.7379.0-win64-asan\chrome.exe" --type=gpu-process --no-pre-read-main-dll --start-stack-profiler --gpu-preferences=SAAAAAAAAADgAQAEAAAAAAAAAAAAAMAAAwAAAAAAAAAAAAAAAAAAABIAAAAAAAAAAAAAAAAAAAAQAAAAAAAAABAAAAAAAAAACAAAAAAAAAAIAAAAAAAAAA== --metrics-shmem-handle=1856,i,16049326817075466414,7205898037398527891,262144 -
-field-trial-handle=1960,i,2671077517126853030,12550265571060057205,262144 --enable-features=BlockInsecurePrivateNetworkRequests,BlockInsecurePrivateNetworkRequestsFromPrivate,BlockInsecurePrivateNetworkRequestsFromUnknown,CookieIndicesHeader,CookieSameSiteConsidersRedirectChain,CreateImageBitmapOrientationNone,CriticalClientHint,DocumentPolicyNegotiation,EnableCanvas2DLayer
s,ExperimentalContentSecurityPolicyFeatures,OriginIsolationHeader,PartitionedPopins,PrefetchCookieIndices,PrivateNetworkAccessRespectPreflightResults,ThirdPartyStoragePartitioning --variations-seed-version --mojo-platform-channel-handle=1952 /prefetch:2`
==18232==END OF ADDITIONAL INFO
==18232==ABORTING

## Attachments

- [heap-buffer-overflow-dawnnativeReflectEntryPointUsingTint.html](attachments/heap-buffer-overflow-dawnnativeReflectEntryPointUsingTint.html) (text/html, 6.3 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2025-09-02)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5958912058523648.

### el...@chromium.org (2025-09-02)

Thanks for the report! I can reproduce this crash with a linux asan build at r1509576 using these args:

```
blink_enable_generated_code_formatting = false
dcheck_always_on = true
enable_mojom_fuzzer = true
ffmpeg_branding = "Chrome"
# high_end_fuzzer_targets = true
is_asan = true
is_component_build = true
is_debug = false
proprietary_codecs = true
symbol_level = 1
use_libfuzzer = true
use_remoteexec = true
use_siso = true
```

Given that it requires --enable-experimental-web-platform-features to reach on Windows and --enable-unsafe-gpu to reach on Linux I'm calling this SecurityImpact-None, but Pri-1 / Sev-1 given the possibility of memory corruption in the GPU process.

### ka...@chromium.org (2025-09-02)

Heap overflow is in compatibility mode code here:
<https://source.chromium.org/chromium/chromium/src/+/refs/tags/141.0.7379.0:third_party/dawn/src/dawn/native/ShaderModule.cpp;l=1316;drc=9276b62e3e1fb174e212e9d87a09797b5801d1c3>

### ka...@chromium.org (2025-09-02)

I started linking up the blocking issues so that this could block shipment of WebGPU Compatibility Mode. But then I remembered that we already have an origin trial for it, which means this should be accessible in the wild already.

### ka...@chromium.org (2025-09-02)

For some reason I cannot set the impact hotlist. @el...@chromium.org can you help update the metadata on this bug?

### ka...@chromium.org (2025-09-02)

EDIT: reposted with correction below

### ka...@chromium.org (2025-09-02)

This should be accessible in the wild on Mac, Android, and ChromeOS too. Not on Linux because WebGPU is not shipped there.

On Mac Canary this results in `[65019:19777579:0902/153958.785015:FATAL:raw_hash_set.h:1251] NOTREACHED hit. operator-> called on end() iterator.` which means I'm not sure if it actually hit the heap overflow or not.

### gm...@chromium.org (2025-09-02)

I think this might fix it. Testing locally

<https://dawn-review.googlesource.com/c/dawn/+/260455>

### ka...@chromium.org (2025-09-02)

Definitely looks like it should fix the NOTREACHED, so if the heap overflow is the same thing, I think so.

### el...@chromium.org (2025-09-02)

kainino: you don't set the hotlists directly - you set FoundIn and the hotlists are computed from that.

### ka...@chromium.org (2025-09-02)

Setting 139 since that's when we shipped the origin trial.

### ka...@chromium.org (2025-09-02)

Reproduced a crash in 139 Stable on Mac using just an origin trial token. However ~~presumably~~ this is just the NOTREACHED ~~but the crash hasn't processed yet~~ <http://crash/cadabf6682452ecc>

### ka...@chromium.org (2025-09-02)

I believe we have a kill switch for Compat. We probably need to invoke it for this?

### gm...@chromium.org (2025-09-03)

sadly that's not it. I think the issue maybe related to it's declaring `@group(1240)` and **maybe** the code doesn't handle past `4`? I'm not sure. I could really use some tips navigating dawn code. For example I must have spent 2 hours trying to track down where `EntryPointMetadata` is defined. Because apparently it's defined in a macro the normal searches didn't get me there. I think I finally got here

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/native/ShaderModule.h;l=277;drc=391e98eeaee80326c3a9d9e9dd731570dba0981a>

Which got me here

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/native/ShaderModule.h;l=203?q=BindingInfoArray&ss=chromium%2Fchromium%2Fsrc>

```
using BindingInfoArray = ityp::array<BindGroupIndex, BindingGroupInfoMap, kMaxBindGroups>;

```

where `kMaxBindGroups = 4`

I'm wondering if this is not actually a compat bug. It's just only compat that happens to hit it.

### ka...@chromium.org (2025-09-03)

The cross-references in chromium code search work fine for me, if I click `EntryPointMetadata` it takes me here:
<https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/native/ShaderModule.h;l=337;drc=391e98eeaee80326c3a9d9e9dd731570dba0981a>
Of course it takes some scrutiny to figure out what that actually does but it did take me to the correct place.

### ka...@chromium.org (2025-09-03)

Looking at other usages of `EntryPointMetadata::bindings` [1] it seems like we usually index it using an index from a pipeline layout rather than from the Tint inspector. That's already been validated so it can't be out of bounds.

[1] this took a bit of a trick due to the macro; had to start [here](https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/native/ShaderModule.cpp;l=1338;drc=08b832c14d8a2b56f34297099db3bce96ce07fff) and right click -> "References" on `metadata->`**`bindings`**

### 24...@project.gserviceaccount.com (2025-09-03)

Detailed Report: https://clusterfuzz.com/testcase?key=5958912058523648

Fuzzer: tint_graphicsfuzz_fuzzer
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 8
Crash Address: 0x79510c4d81c0
Crash State:
  absl::container_internal::raw_hash_set<absl::container_internal::FlatHashMapPoli
  dawn::native::ReflectEntryPointUsingTint
  dawn::native::ParseShaderModule
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=1509620

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5958912058523648

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### cw...@chromium.org (2025-09-03)

The DAWN\_SERIALIZABLE structures suck for code search, it would be nice to replace them with something like TINT\_REFLECT in the future, but with some static assert that all the members are listed (we tried coming up with something like that with Ben in the past but it was technically full of C++ UB).

What looks to be happening in the crash is that we try to access the bindings map with unvalidated indices. The bindings map is already [accessed earlier to store the bindings](https://source.chromium.org/chromium/chromium/src/+/refs/tags/141.0.7379.0:third_party/dawn/src/dawn/native/ShaderModule.cpp;drc=9276b62e3e1fb174e212e9d87a09797b5801d1c3;l=1217) but only after validation that the indices are valid. That validation is a bit special because it is not using `DAWN_TRY` like normal check but `DelayedInvalidIf` because these are checks against limits and supposed to be reported at pipeline compilation time and not shader module compilation time (which `ReflectEntryPointUsingTint` is in). This means that when iterating over pairs of texture/sampler later, we are not guaranteed to have returned early if one of them is invalid.

Possible fixes would be to either 1) (safest short term) don't enter [this condition](https://source.chromium.org/chromium/chromium/src/+/refs/tags/141.0.7379.0:third_party/dawn/src/dawn/native/ShaderModule.cpp;drc=9276b62e3e1fb174e212e9d87a09797b5801d1c3;l=1304) if there is any delayed validation error 2) re-validate the BindGroupIndex in that loop or 3) (likely the best long term) move the computation (that's only for [numTextureSamplerCombinations](https://source.chromium.org/chromium/chromium/src/+/refs/tags/141.0.7379.0:third_party/dawn/src/dawn/native/ShaderModule.h;drc=9276b62e3e1fb174e212e9d87a09797b5801d1c3;l=336)) to happen when it is actually needed [here](https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/native/Pipeline.cpp;drc=c3999d7e32b1accce2ce2f2431db487541a4f15e;l=107). (all the required data should already be reflected in [samplerAndNonSamplerTexturePairs](https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/native/ShaderModule.h;drc=9276b62e3e1fb174e212e9d87a09797b5801d1c3;l=291)).

### ch...@google.com (2025-09-03)

Setting milestone because of s0/s1 severity.

### ka...@chromium.org (2025-09-03)

Ohh I understand what's happening now:

- There's an overrun on `metadata->bindings`
- In stable it goes right past that, and a few lines later it crashes dereferencing `end()->`

That said it seems like an underlying bug that we can have an overrun on `metadata->bindings` at all. It's an `ityp::array` which wraps a `std::array` so it's supposed to hit the libc++ assertions which AFAICT Chromium is [supposed to enable in release](https://source.chromium.org/chromium/chromium/src/+/main:buildtools/third_party/libc++/__assertion_handler;l=32;drc=515e524058a7daaf1a5ee36645a008ddb8ba8367). So we must have a build config issue that prevents us from picking that up, I guess?

### gm...@chromium.org (2025-09-03)

I think it's just that we don't have any tests that tried making an out of range group index in compat. As soon as I added one I got

Error: Assertion failure at ../../src/dawn/common/ityp\_array.h:61 (operator[]): index >= 0 && index < I(Size)

(debug build of dawn\_unittests)

### ka...@chromium.org (2025-09-03)

That's the logic bug, but there's also a build config bug, because going out of bounds is supposed to crash safely. I'm looking into that to figure out what's wrong.

### dx...@google.com (2025-09-04)

Project: dawn  

Branch:  main  

Author:  Gregg Tavares [gman@chromium.org](mailto:gman@chromium.org)  

Link:    <https://dawn-review.googlesource.com/260455>

Fix Heap-overflow in dawn ReflectEntryPointUsingTint

---


Expand for full commit details
```
     
    Note: The operators needed to be added so BindingSlot 
    can be used in std::set. The needed to be constexpr 
    so that the static_assert that converting a tint 
    nonSamplerBindingPoint turns into a dawn nonSamplerBindingPoint. 
    The clang-format off is needed because clang-format fails 
    on the code in BindingPoint.h 
     
    Change-Id: I1bdc075323a14bda264655e475fe6fdc074ced8a 
    Bug: 442444724 
    Fixes: 442444724 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/260455 
    Reviewed-by: Kai Ninomiya <kainino@chromium.org> 
    Commit-Queue: Gregg Tavares <gman@chromium.org> 
    Auto-Submit: Gregg Tavares <gman@chromium.org>

```

---

Files:

- M `src/dawn/native/BindingInfo.h`
- M `src/dawn/native/Pipeline.cpp`
- M `src/dawn/native/ShaderModule.cpp`
- M `src/dawn/native/ShaderModule.h`
- M `src/dawn/tests/unittests/validation/CompatValidationTests.cpp`

---

Hash: 471c3d7e4b83b98ec8c0d8e2d4b566c3b7f5e43c  

Date: Thu Sep 4 01:52:22 2025


---

### ka...@chromium.org (2025-09-04)

Will need security team guidance on:

- Which branches to merge back to
- Whether to invoke the Finch kill switch for WebGPU Compatibility Mode which would prevent this from being reachable

### ch...@google.com (2025-09-04)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2025-09-04)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M140. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M141. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [140, 141].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ka...@chromium.org (2025-09-04)

1. <https://dawn-review.googlesource.com/c/dawn/+/260455> into Dawn's chromium-release branches
2. No, it hasn't rolled yet
3. Change is not trivial so maybe
4. Change is not trivial so maybe
5. No
6. FYI it only affects Linux with command line flags because the feature hasn't shipped there.

### ka...@chromium.org (2025-09-04)

2. ... note it's not easily detectable in release builds except by a different crash several lines later, so being in canary will only tell us that it's stable, not that it fixes the bug (though we know from inspecting the code that it definitely does)

### ka...@chromium.org (2025-09-04)

1. I also have another, simpler CL up <https://dawn-review.googlesource.com/c/dawn/+/260462> that would just introduce a CHECK crash, which would also fix the security bug, while introducing a GPU process crash (EDIT: but only right before I think it was going to crash anyway). It's technically possible to merge that back instead.

### dx...@google.com (2025-09-04)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/6916291>

Roll Dawn from 0567736dfb04 to 95122946d574 (25 revisions)

---


Expand for full commit details
```
     
    https://dawn.googlesource.com/dawn.git/+log/0567736dfb04..95122946d574 
     
    2025-09-04 dsinclair@chromium.org Add missing gn dependency 
    2025-09-04 cwallez@chromium.org [dawn][native] Add a test that WGSL hasBinding is false for OOB 
    2025-09-04 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 8415cc875465 to 0c650120dc77 (10 revisions) 
    2025-09-04 alanbaker@google.com Fix tables in subgroup_matrix.md 
    2025-09-04 dsinclair@chromium.org Auto-convert `ConstOffset` in spirv-reader. 
    2025-09-04 lehoangquyen@chromium.org D3D11: print CreateShaderResourceView1 params upon failure. 
    2025-09-04 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll ANGLE from 8280ca3745ca to 397b39fee2c5 (3 revisions) 
    2025-09-04 cwallez@chromium.org [dawn][native] Cleanup a few "bindless" TODOs. 
    2025-09-04 shanxing.mei@intel.com Add failures to expectations.txt related to tier1 
    2025-09-04 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll DirectX Shader Compiler from 4e0f5364a369 to 4ddee810a588 (2 revisions) 
    2025-09-04 shaoboyan@microsoft.com Dawn/Native: Implement SetImmediateData() in Metal Backend 
    2025-09-04 gman@chromium.org Fix Heap-overflow in dawn ReflectEntryPointUsingTint 
    2025-09-04 lokokung@google.com [dawn][wire] Adds spontaneous wire mode. 
    2025-09-03 cwallez@chromium.org [dawn][native] Add validation DynamicBindingKind::SampledTexture views 
    2025-09-03 bsheedy@google.com Download Node deps on gn_v2 builder 
    2025-09-03 bsheedy@google.com Rename and enable gn_v2 fuzz builder 
    2025-09-03 cwallez@chromium.org [dawn][native] Handle typeId computation for all dynamic binding textures. 
    2025-09-03 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll ANGLE from 875b7400b543 to 8280ca3745ca (4 revisions) 
    2025-09-03 bsheedy@google.com Enable gn_v2 fuzz tests 
    2025-09-03 alanbaker@google.com Add feature documentation for subgroup matrix 
    2025-09-03 cwallez@chromium.org [dawn][native] Update typeId metadata for dynamic binding arrays. 
    2025-09-03 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 724d98c0e40e to 8415cc875465 (9 revisions) 
    2025-09-03 jrprice@google.com [tint] Add DIR_METADATA to src/tint/ 
    2025-09-03 dsinclair@chromium.org Cleanup sem 
    2025-09-03 cwallez@chromium.org Revert "Suppress test to fix vulkan-deps roll" 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/dawn-chromium-autoroll 
    Please CC cwallez@google.com,dsinclair@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in Dawn: https://bugs.chromium.org/p/dawn/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:dawn-android-arm-deps-rel;luci.chromium.try:dawn-android-arm64-deps-rel;luci.chromium.try:dawn-linux-x64-deps-rel;luci.chromium.try:dawn-mac-x64-deps-rel;luci.chromium.try:dawn-mac-arm64-deps-rel;luci.chromium.try:dawn-win10-x64-deps-rel;luci.chromium.try:dawn-win10-x86-deps-rel;luci.chromium.try:dawn-win11-arm64-deps-rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-android-arm64 
    Bug: chromium:366291600,chromium:412761856,chromium:42161933,chromium:421941589,chromium:435317394,chromium:440120139,chromium:441327468,chromium:441328362,chromium:442444724,chromium:442593063,chromium:442613328 
    Tbr: dsinclair@google.com 
    Change-Id: Ic356da7255bba12716c01212408c88297612154c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6916291 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1511150}

```

---

Files:

- M `DEPS`
- M `third_party/dawn`

---

Hash: [3ddf9a18f5ec781b7ad1c71568333ee052a5ec18](https://chromiumdash.appspot.com/commit/3ddf9a18f5ec781b7ad1c71568333ee052a5ec18)  

Date: Thu Sep 4 21:10:15 2025


---

### am...@chromium.org (2025-09-04)

The DAWN -> Chromium roll was just landed earlier today, therefore, we can't yet perform security merge review at this time and will not make merge deadlines for next week's Stable channel update. This issue will need to be revisited on Monday for merge for the next M141 Beta and following M140 Stable.

### 24...@project.gserviceaccount.com (2025-09-05)

ClusterFuzz testcase 5958912058523648 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1511149:1511153

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### dx...@google.com (2025-09-05)

Project: dawn  

Branch:  main  

Author:  Kai Ninomiya [kainino@chromium.org](mailto:kainino@chromium.org)  

Link:    <https://dawn-review.googlesource.com/260462>

[dawn] Ensure release bounds checks in ityp::\*

---


Expand for full commit details
```
     
    Add death tests to ensure out-of-bounds accesses in all the ityp::* 
    containers crashes in release. 
     
    Both libc++ and absl are supposed to be configured to guarantee this, so 
    we don't need our own checks for those. (MSVC is not configured this 
    way, and I don't think we test libstdc++. Both are capable though.) 
     
    Fix ityp::array/vector/stack_vec by just removing the DAWN_ASSERT. That 
    was telling the compiler to assume its condition is true, causing it to 
    elide the bounds checks inside libc++ (that are supposed to always be 
    enabled for safety). 
     
    Fix ityp::span by changing the DAWN_ASSERT to a DAWN_CHECK. This should 
    really be changed to be based on std::span but that should be done 
    separately. 
     
    Bug: 442444724, 442860471 
    Change-Id: I7c37fc9c382b840a09df0b00dd782a5cdb80de6e 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/260462 
    Reviewed-by: Gregg Tavares <gman@chromium.org> 
    Commit-Queue: Kai Ninomiya <kainino@chromium.org> 
    Reviewed-by: Brandon Jones <bajones@chromium.org>

```

---

Files:

- M `src/dawn/common/ityp_array.h`
- M `src/dawn/common/ityp_span.h`
- M `src/dawn/common/ityp_stack_vec.h`
- M `src/dawn/common/ityp_vector.h`
- M `src/dawn/tests/BUILD.gn`
- M `src/dawn/tests/unittests/ITypArrayTests.cpp`
- M `src/dawn/tests/unittests/ITypSpanTests.cpp`
- A `src/dawn/tests/unittests/ITypStackVecTests.cpp`
- M `src/dawn/tests/unittests/ITypVectorTests.cpp`

---

Hash: fb9949186b30ce39ca31524e2c11cee227ce7a81  

Date: Fri Sep 5 20:29:37 2025


---

### dx...@google.com (2025-09-06)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/6920373>

Roll Dawn from 5c08e28a3144 to 859da64f47cb (5 revisions)

---


Expand for full commit details
```
     
    https://dawn.googlesource.com/dawn.git/+log/5c08e28a3144..859da64f47cb 
     
    2025-09-05 kainino@chromium.org [dawn][native] Cap maxImmediateSize at 32 
    2025-09-05 lokokung@google.com [dawn][common] Move Nanoseconds into common. 
    2025-09-05 kainino@chromium.org [dawn][native][d3d12] Remove dynamic allocation of limits in root signature 
    2025-09-05 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 0c650120dc77 to 31fde841db1d (7 revisions) 
    2025-09-05 kainino@chromium.org [dawn] Ensure release bounds checks in ityp::* 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/dawn-chromium-autoroll 
    Please CC cwallez@google.com,dsinclair@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in Dawn: https://bugs.chromium.org/p/dawn/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:dawn-android-arm-deps-rel;luci.chromium.try:dawn-android-arm64-deps-rel;luci.chromium.try:dawn-linux-x64-deps-rel;luci.chromium.try:dawn-mac-x64-deps-rel;luci.chromium.try:dawn-mac-arm64-deps-rel;luci.chromium.try:dawn-win10-x64-deps-rel;luci.chromium.try:dawn-win10-x86-deps-rel;luci.chromium.try:dawn-win11-arm64-deps-rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-android-arm64 
    Bug: chromium:366291600,chromium:440381283,chromium:441981783,chromium:442444724,chromium:442860471 
    Tbr: dsinclair@google.com 
    Change-Id: Idebaa9d948f745bdf412096d4fe64f8359ab8a53 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6920373 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1511988}

```

---

Files:

- M `DEPS`
- M `third_party/dawn`

---

Hash: [c025218d5cc6cbedf7098f659695d172564ad232](https://chromiumdash.appspot.com/commit/c025218d5cc6cbedf7098f659695d172564ad232)  

Date: Sat Sep 6 04:12:16 2025


---

### ch...@google.com (2025-09-11)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ts...@google.com (2025-09-11)

This does seem too complex for a merge to 140.  Thanks. Please merge to M141 (7390) as soon as you are able.

### ka...@chromium.org (2025-09-11)

@ts...@chromium.org would you like to merge <https://dawn-review.googlesource.com/c/dawn/+/260462> (see [#comment30](https://issues.chromium.org/issues/442444724#comment30)) instead? Up to y'all's judgement of what's worth a late merge vs just waiting for 141.

### sp...@google.com (2025-09-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $25000.00 for this report.

Rationale for this decision:
Sandbox escape in GPU on android (non-sandboxed)


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### dx...@google.com (2025-09-11)

Project: dawn  

Branch:  chromium/7390  

Author:  Gregg Tavares [gman@chromium.org](mailto:gman@chromium.org)  

Link:    <https://dawn-review.googlesource.com/261439>

[M141] Fix Heap-overflow in dawn ReflectEntryPointUsingTint

---


Expand for full commit details
```
     
    Note: The operators needed to be added so BindingSlot 
    can be used in std::set. The needed to be constexpr 
    so that the static_assert that converting a tint 
    nonSamplerBindingPoint turns into a dawn nonSamplerBindingPoint. 
    The clang-format off is needed because clang-format fails 
    on the code in BindingPoint.h 
     
    Change-Id: I1bdc075323a14bda264655e475fe6fdc074ced8a 
    Bug: 442444724 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/260455 
    Reviewed-by: Kai Ninomiya <kainino@chromium.org> 
    Commit-Queue: Gregg Tavares <gman@chromium.org> 
    Auto-Submit: Gregg Tavares <gman@chromium.org> 
    (cherry picked from commit 471c3d7e4b83b98ec8c0d8e2d4b566c3b7f5e43c) 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/261439 
    Auto-Submit: Kai Ninomiya <kainino@chromium.org> 
    Commit-Queue: Kai Ninomiya <kainino@chromium.org> 
    Reviewed-by: Gregg Tavares <gman@chromium.org>

```

---

Files:

- M `src/dawn/native/BindingInfo.h`
- M `src/dawn/native/Pipeline.cpp`
- M `src/dawn/native/ShaderModule.cpp`
- M `src/dawn/native/ShaderModule.h`
- M `src/dawn/tests/unittests/validation/CompatValidationTests.cpp`

---

Hash: 9caf49389e5e0564d18e0504c6cfa45c88b4e4fd  

Date: Thu Sep 11 21:20:47 2025


---

### ch...@google.com (2025-09-15)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-09-16)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sr...@google.com (2025-09-16)

Please complete your merges to M141 branch before 2pm PST today so they can be part of the beta release tomorrow ( we are cutting stable RC next week) so it would be good to get beta coverage for these CL's this week

### sr...@google.com (2025-09-16)

adjusted labels as merge to 141 is completed in comment#40 

if there are more merges needed, please reach out to me 

### pe...@google.com (2025-09-16)

LTS Milestone M138

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ka...@chromium.org (2025-09-16)

Let's just make sure that the Compatibility Mode origin trial is not active in M138 and then we don't have to merge anything back.

### ka...@chromium.org (2025-09-16)

Never mind, I already checked that earlier in this thread:

> Setting 139 since that's when we shipped the origin trial.

So no, it doesn't affect M138.

### ka...@chromium.org (2025-09-16)

Bumping the question above for M140:

> Would you like to merge <https://dawn-review.googlesource.com/c/dawn/+/260462> (see [#comment30](https://issues.chromium.org/issues/442444724#comment30)) [to M140] instead? Up to y'all's judgement of what's worth a late merge vs just waiting for 141.

### qk...@google.com (2025-09-17)

Labeled as not applicable for M138 LTS because the issue doesn't happen in M138 according to the comment #47.

### ch...@google.com (2025-12-12)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/442444724)*
