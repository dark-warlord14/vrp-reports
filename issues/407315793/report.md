# Security: heap-use-after-free in gpu::CommandBufferProxyImpl::OnDisconnect

| Field | Value |
|-------|-------|
| **Issue ID** | [407315793](https://issues.chromium.org/issues/407315793) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Services>GPU |
| **Platforms** | Mac |
| **Chrome Version** | 134.0.0.0 |
| **Reporter** | zh...@gmail.com |
| **Assignee** | mf...@chromium.org |
| **Created** | 2025-03-30 |
| **Bounty** | $3,000.00 |

## Description

# Steps to reproduce the problem

1. Compile asan chromium using mac, the steps are as follows:

```
git checkout 924d038bf0e3f482162c5f5658ef15658f33f222
git apply poc.diff

```

2. `args.gn` content is as follows:

```
# Build arguments go here.
# See "gn args <out_dir> --list" for available build arguments.
is_component_build = true
is_debug = false
is_asan = true
symbol_level = 2
dcheck_always_on = false
treat_warnings_as_errors = false

```

3. Run the following command:

```
./Chromium.app/Contents/MacOS/Chromium http://127.0.0.1/index.html --no-sandbox --enable-experimental-web-platform-features --user-data-dir=/tmp/userdata/t11`

```

Following the steps in poc.mov, the UAF can be reproduced stably.

# Problem Description

RCA and bisect coming soon!

# Summary

Security: heap-use-after-free in gpu::CommandBufferProxyImpl::OnDisconnect

# Custom Questions

#### Type of crash:

Chromium Helper --type=utility

#### Crash state:

```
[20596:24442322:0330/222242.493539:ERROR:gpu/ipc/client/command_buffer_proxy_impl.cc:801] in CommandBufferProxyImpl::DisconnectChannel !!! !!! zh1x1an: 0x619000bac780
[20596:24442322:0330/222242.493587:ERROR:gpu/ipc/client/command_buffer_proxy_impl.cc:813] in CommandBufferProxyImpl::DisconnectChannel !!! !!! gpu_control_client_: 0x0 zh1x1an: 0x619000bac780
[20596:24442322:0330/222242.493695:ERROR:gpu/ipc/client/command_buffer_proxy_impl.cc:801] in CommandBufferProxyImpl::DisconnectChannel !!! !!! zh1x1an: 0x619000bac280
[20596:24442322:0330/222242.493723:ERROR:gpu/ipc/client/command_buffer_proxy_impl.cc:813] in CommandBufferProxyImpl::DisconnectChannel !!! !!! gpu_control_client_: 0x0 zh1x1an: 0x619000bac280
[20622:24442719:0330/222242.493630:ERROR:gpu/ipc/client/command_buffer_proxy_impl.cc:146] in CommandBufferProxyImpl::OnDisconnect !!! !!! zh1x1an :0x6190005c3080
[20622:24442719:0330/222242.497507:ERROR:gpu/ipc/client/command_buffer_proxy_impl.cc:801] in CommandBufferProxyImpl::DisconnectChannel !!! !!! zh1x1an: 0x6190005c3080
[20622:24442719:0330/222242.497571:ERROR:gpu/ipc/client/command_buffer_proxy_impl.cc:813] in CommandBufferProxyImpl::DisconnectChannel !!! !!! gpu_control_client_: 0x611000019058 zh1x1an: 0x6190005c3080
[20622:24442719:0330/222242.497586:ERROR:gpu/ipc/client/command_buffer_proxy_impl.cc:815] in CommandBufferProxyImpl::DisconnectChannel ,,, before OnGpuControlLostContext ,,, ,,, zh1x1an: 0x6190005c3080
[20622:24442719:0330/222242.497710:ERROR:gpu/ipc/client/command_buffer_proxy_impl.cc:328] GPU state invalid after WaitForGetOffsetInRange.
[20622:24442719:0330/222242.497768:ERROR:gpu/ipc/client/command_buffer_proxy_impl.cc:801] in CommandBufferProxyImpl::DisconnectChannel !!! !!! zh1x1an: 0x6190005c4480
[20622:24442719:0330/222242.497803:ERROR:gpu/ipc/client/command_buffer_proxy_impl.cc:813] in CommandBufferProxyImpl::DisconnectChannel !!! !!! gpu_control_client_: 0x0 zh1x1an: 0x6190005c4480
=================================================================
==20622==ERROR: AddressSanitizer: heap-use-after-free on address 0x606000052ac0 at pc 0x000102c57f2c bp 0x00016da15dd0 sp 0x00016da15580
READ of size 53 at 0x606000052ac0 thread T0
==20622==WARNING: invalid path to external symbolizer!
==20622==WARNING: Failed to use and restart external symbolizer!
    #0 0x000102c57f28 in __asan_memmove+0x2d4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libclang_rt.asan_osx_dynamic.dylib:arm64+0x4ff28)
    #1 0x000102938cc4 in std::__Cr::basic_streambuf<char, std::__Cr::char_traits<char>>::xsputn(char const*, long)+0xcc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libc++_chrome.dylib:arm64+0x6ccc4)
    #2 0x00012cb186b8 in std::__Cr::ostreambuf_iterator<char, std::__Cr::char_traits<char>> std::__Cr::__pad_and_output<char, std::__Cr::char_traits<char>>(std::__Cr::ostreambuf_iterator<char, std::__Cr::char_traits<char>>, char const*, char const*, char const*, std::__Cr::ios_base&, char)+0x2b4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libcontent.dylib:arm64+0xc6b8)
    #3 0x00012cb18230 in std::__Cr::basic_ostream<char, std::__Cr::char_traits<char>>& std::__Cr::__put_character_sequence<char, std::__Cr::char_traits<char>>(std::__Cr::basic_ostream<char, std::__Cr::char_traits<char>>&, char const*, unsigned long)+0x250 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libcontent.dylib:arm64+0xc230)
    #4 0x0001303f374c in video_effects::VideoEffectsServiceImpl::OnDeviceLost(wgpu::DeviceLostReason, std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>)+0x148 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libcontent.dylib:arm64+0x38e774c)
    #5 0x0001303f5268 in base::internal::Invoker<base::internal::FunctorTraits<void (video_effects::VideoEffectsServiceImpl::*&&)(wgpu::DeviceLostReason, std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>), base::WeakPtr<video_effects::VideoEffectsServiceImpl>&&>, base::internal::BindState<true, true, false, void (video_effects::VideoEffectsServiceImpl::*)(wgpu::DeviceLostReason, std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>), base::WeakPtr<video_effects::VideoEffectsServiceImpl>>, void (wgpu::DeviceLostReason, std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>)>::RunOnce(base::internal::BindStateBase*, wgpu::DeviceLostReason, std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>&&)+0x1b0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libcontent.dylib:arm64+0x38e9268)
    #6 0x0001303f859c in base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (wgpu::DeviceLostReason, std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>)>&&, wgpu::DeviceLostReason&&, std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>&&>, base::internal::BindState<false, true, true, base::OnceCallback<void (wgpu::DeviceLostReason, std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>)>, wgpu::DeviceLostReason, std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x198 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libcontent.dylib:arm64+0x38ec59c)
    #7 0x000104923810 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x344 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libbase.dylib:arm64+0x1eb810)
    #8 0x000104999f7c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x864 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libbase.dylib:arm64+0x261f7c)
    #9 0x000104999358 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libbase.dylib:arm64+0x261358)
    #10 0x0001047d1da4 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x208 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libbase.dylib:arm64+0x99da4)
    #11 0x00010499b498 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x32c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libbase.dylib:arm64+0x263498)
    #12 0x00010489a454 in base::RunLoop::Run(base::Location const&)+0x434 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libbase.dylib:arm64+0x162454)
    #13 0x0001303d02dc in content::UtilityMain(content::MainFunctionParams)+0x7d4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libcontent.dylib:arm64+0x38c42dc)
    #14 0x00013040b8f8 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x3d8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libcontent.dylib:arm64+0x38ff8f8)
    #15 0x00013040d860 in content::ContentMainRunnerImpl::Run()+0x448 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libcontent.dylib:arm64+0x3901860)
    #16 0x000130409124 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x5b4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libcontent.dylib:arm64+0x38fd124)
    #17 0x000130409980 in content::ContentMain(content::ContentMainParams)+0x190 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libcontent.dylib:arm64+0x38fd980)
    #18 0x0001179c028c in ChromeMain+0x360 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libchrome_dll.dylib:arm64+0xc28c)
    #19 0x0001023e8c94 in main+0x254 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/136.0.7096.0/Helpers/Chromium Helper.app/Contents/MacOS/Chromium Helper:arm64+0x100000c94)
    #20 0x00019a198270  (<unknown module>)

0x606000052ac0 is located 0 bytes inside of 56-byte region [0x606000052ac0,0x606000052af8)
freed by thread T0 here:
    #0 0x000102c6a6d4 in __sanitizer_finish_switch_fiber+0xa24 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libclang_rt.asan_osx_dynamic.dylib:arm64+0x626d4)
    #1 0x00013fd43b7c in dawn::wire::client::Device::DeviceLostEvent::~DeviceLostEvent()+0x90 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libdawn_wire.dylib:arm64+0xe3b7c)
    #2 0x00013fd4a4f4 in std::__Cr::__tree<std::__Cr::__value_type<unsigned long long, std::__Cr::unique_ptr<dawn::wire::client::TrackedEvent, std::__Cr::default_delete<dawn::wire::client::TrackedEvent>>>, std::__Cr::__map_value_compare<unsigned long long, std::__Cr::__value_type<unsigned long long, std::__Cr::unique_ptr<dawn::wire::client::TrackedEvent, std::__Cr::default_delete<dawn::wire::client::TrackedEvent>>>, std::__Cr::less<unsigned long long>, true>, std::__Cr::allocator<std::__Cr::__value_type<unsigned long long, std::__Cr::unique_ptr<dawn::wire::client::TrackedEvent, std::__Cr::default_delete<dawn::wire::client::TrackedEvent>>>>>::destroy(std::__Cr::__tree_node<std::__Cr::__value_type<unsigned long long, std::__Cr::unique_ptr<dawn::wire::client::TrackedEvent, std::__Cr::default_delete<dawn::wire::client::TrackedEvent>>>, void*>*)+0x98 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libdawn_wire.dylib:arm64+0xea4f4)
    #3 0x00013fd47a20 in dawn::wire::client::EventManager::TransitionTo(dawn::wire::client::EventManager::State)+0x178 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libdawn_wire.dylib:arm64+0xe7a20)
    #4 0x00013fd39ce8 in dawn::wire::client::Client::Disconnect()+0x228 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libdawn_wire.dylib:arm64+0xd9ce8)
    #5 0x00013b5fa014 in gpu::webgpu::DawnWireServices::Disconnect()+0x44 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libgpu_webgpu.dylib:arm64+0x2014)
    #6 0x00013b5fcca0 in non-virtual thunk to gpu::webgpu::WebGPUImplementation::OnGpuControlLostContext()+0x120 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libgpu_webgpu.dylib:arm64+0x4ca0)
    #7 0x00010883eb2c in gpu::CommandBufferProxyImpl::DisconnectChannel()+0x488 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libgpu.dylib:arm64+0x12ab2c)
    #8 0x000108840d64 in gpu::CommandBufferProxyImpl::OnDisconnect()+0x390 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libgpu.dylib:arm64+0x12cd64)
    #9 0x0001088498ac in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::CommandBufferProxyImpl::*&&)(), gpu::CommandBufferProxyImpl*>, base::internal::BindState<true, true, false, void (gpu::CommandBufferProxyImpl::*)(), base::internal::UnretainedWrapper<gpu::CommandBufferProxyImpl, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x184 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libgpu.dylib:arm64+0x1358ac)
    #10 0x0001027b3098 in mojo::InterfaceEndpointClient::NotifyError(std::__Cr::optional<mojo::DisconnectReason> const&)+0x3c0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libmojo_public_cpp_bindings.dylib:arm64+0x2b098)
    #11 0x00010774b434 in IPC::ChannelAssociatedGroupController::NotifyEndpointOfError(IPC::ChannelAssociatedGroupController::Endpoint*, bool)+0x3e0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libipc.dylib:arm64+0x47434)
    #12 0x00010774b830 in IPC::ChannelAssociatedGroupController::NotifyEndpointOfErrorOnEndpointThread(unsigned int, base::raw_ptr<IPC::ChannelAssociatedGroupController::Endpoint, (partition_alloc::internal::RawPtrTraits)1>)+0x1cc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libipc.dylib:arm64+0x47830)
    #13 0x00010774bad0 in void base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(unsigned int, base::raw_ptr<IPC::ChannelAssociatedGroupController::Endpoint, (partition_alloc::internal::RawPtrTraits)1>), IPC::ChannelAssociatedGroupController*&&, unsigned int&&, base::raw_ptr<IPC::ChannelAssociatedGroupController::Endpoint, (partition_alloc::internal::RawPtrTraits)1>>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(unsigned int, base::raw_ptr<IPC::ChannelAssociatedGroupController::Endpoint, (partition_alloc::internal::RawPtrTraits)1>), scoped_refptr<IPC::ChannelAssociatedGroupController>, unsigned int, base::internal::UnretainedWrapper<IPC::ChannelAssociatedGroupController::Endpoint, base::unretained_traits::MayDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<void (IPC::ChannelAssociatedGroupController::*)(unsigned int, base::raw_ptr<IPC::ChannelAssociatedGroupController::Endpoint, (partition_alloc::internal::RawPtrTraits)1>), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, unsigned int, base::internal::UnretainedWrapper<IPC::ChannelAssociatedGroupController::Endpoint, base::unretained_traits::MayDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul, 1ul, 2ul>(void (IPC::ChannelAssociatedGroupController::*&&)(unsigned int, base::raw_ptr<IPC::ChannelAssociatedGroupController::Endpoint, (partition_alloc::internal::RawPtrTraits)1>), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, unsigned int, base::internal::UnretainedWrapper<IPC::ChannelAssociatedGroupController::Endpoint, base::unretained_traits::MayDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul>)+0x1e8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libipc.dylib:arm64+0x47ad0)
    #14 0x000104923810 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x344 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libbase.dylib:arm64+0x1eb810)
    #15 0x000104999f7c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x864 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libbase.dylib:arm64+0x261f7c)
    #16 0x000104999358 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libbase.dylib:arm64+0x261358)
    #17 0x0001047d1da4 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x208 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libbase.dylib:arm64+0x99da4)
    #18 0x00010499b498 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x32c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libbase.dylib:arm64+0x263498)
    #19 0x00010489a454 in base::RunLoop::Run(base::Location const&)+0x434 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libbase.dylib:arm64+0x162454)
    #20 0x0001303d02dc in content::UtilityMain(content::MainFunctionParams)+0x7d4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libcontent.dylib:arm64+0x38c42dc)
    #21 0x00013040b8f8 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x3d8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libcontent.dylib:arm64+0x38ff8f8)
    #22 0x00013040d860 in content::ContentMainRunnerImpl::Run()+0x448 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libcontent.dylib:arm64+0x3901860)
    #23 0x000130409124 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x5b4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libcontent.dylib:arm64+0x38fd124)
    #24 0x000130409980 in content::ContentMain(content::ContentMainParams)+0x190 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libcontent.dylib:arm64+0x38fd980)
    #25 0x0001179c028c in ChromeMain+0x360 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libchrome_dll.dylib:arm64+0xc28c)
    #26 0x0001023e8c94 in main+0x254 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/136.0.7096.0/Helpers/Chromium Helper.app/Contents/MacOS/Chromium Helper:arm64+0x100000c94)
    #27 0x00019a198270  (<unknown module>)

previously allocated by thread T0 here:
    #0 0x000102c6a2cc in __sanitizer_finish_switch_fiber+0x61c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libclang_rt.asan_osx_dynamic.dylib:arm64+0x622cc)
    #1 0x0001029faf50 in std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>::__grow_by_and_replace(unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, char const*)+0xd4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libc++_chrome.dylib:arm64+0x12ef50)
    #2 0x0001029fc610 in std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>::__assign_external(char const*, unsigned long)+0xb0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libc++_chrome.dylib:arm64+0x130610)
    #3 0x00013fd43d7c in dawn::wire::client::Device::DeviceLostEvent::CompleteImpl(unsigned long long, dawn::EventCompletionType)+0xf4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libdawn_wire.dylib:arm64+0xe3d7c)
    #4 0x00013fd47fec in dawn::wire::client::EventManager::TransitionTo(dawn::wire::client::EventManager::State)+0x744 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libdawn_wire.dylib:arm64+0xe7fec)
    #5 0x00013fd39ce8 in dawn::wire::client::Client::Disconnect()+0x228 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libdawn_wire.dylib:arm64+0xd9ce8)
    #6 0x00013b5fa014 in gpu::webgpu::DawnWireServices::Disconnect()+0x44 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libgpu_webgpu.dylib:arm64+0x2014)
    #7 0x00013b5fcca0 in non-virtual thunk to gpu::webgpu::WebGPUImplementation::OnGpuControlLostContext()+0x120 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libgpu_webgpu.dylib:arm64+0x4ca0)
    #8 0x00010883eb2c in gpu::CommandBufferProxyImpl::DisconnectChannel()+0x488 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libgpu.dylib:arm64+0x12ab2c)
    #9 0x000108840d64 in gpu::CommandBufferProxyImpl::OnDisconnect()+0x390 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libgpu.dylib:arm64+0x12cd64)
    #10 0x0001088498ac in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::CommandBufferProxyImpl::*&&)(), gpu::CommandBufferProxyImpl*>, base::internal::BindState<true, true, false, void (gpu::CommandBufferProxyImpl::*)(), base::internal::UnretainedWrapper<gpu::CommandBufferProxyImpl, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x184 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libgpu.dylib:arm64+0x1358ac)
    #11 0x0001027b3098 in mojo::InterfaceEndpointClient::NotifyError(std::__Cr::optional<mojo::DisconnectReason> const&)+0x3c0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libmojo_public_cpp_bindings.dylib:arm64+0x2b098)
    #12 0x00010774b434 in IPC::ChannelAssociatedGroupController::NotifyEndpointOfError(IPC::ChannelAssociatedGroupController::Endpoint*, bool)+0x3e0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libipc.dylib:arm64+0x47434)
    #13 0x00010774b830 in IPC::ChannelAssociatedGroupController::NotifyEndpointOfErrorOnEndpointThread(unsigned int, base::raw_ptr<IPC::ChannelAssociatedGroupController::Endpoint, (partition_alloc::internal::RawPtrTraits)1>)+0x1cc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libipc.dylib:arm64+0x47830)
    #14 0x00010774bad0 in void base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(unsigned int, base::raw_ptr<IPC::ChannelAssociatedGroupController::Endpoint, (partition_alloc::internal::RawPtrTraits)1>), IPC::ChannelAssociatedGroupController*&&, unsigned int&&, base::raw_ptr<IPC::ChannelAssociatedGroupController::Endpoint, (partition_alloc::internal::RawPtrTraits)1>>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(unsigned int, base::raw_ptr<IPC::ChannelAssociatedGroupController::Endpoint, (partition_alloc::internal::RawPtrTraits)1>), scoped_refptr<IPC::ChannelAssociatedGroupController>, unsigned int, base::internal::UnretainedWrapper<IPC::ChannelAssociatedGroupController::Endpoint, base::unretained_traits::MayDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<void (IPC::ChannelAssociatedGroupController::*)(unsigned int, base::raw_ptr<IPC::ChannelAssociatedGroupController::Endpoint, (partition_alloc::internal::RawPtrTraits)1>), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, unsigned int, base::internal::UnretainedWrapper<IPC::ChannelAssociatedGroupController::Endpoint, base::unretained_traits::MayDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul, 1ul, 2ul>(void (IPC::ChannelAssociatedGroupController::*&&)(unsigned int, base::raw_ptr<IPC::ChannelAssociatedGroupController::Endpoint, (partition_alloc::internal::RawPtrTraits)1>), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, unsigned int, base::internal::UnretainedWrapper<IPC::ChannelAssociatedGroupController::Endpoint, base::unretained_traits::MayDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul>)+0x1e8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libipc.dylib:arm64+0x47ad0)
    #15 0x000104923810 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x344 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libbase.dylib:arm64+0x1eb810)
    #16 0x000104999f7c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x864 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libbase.dylib:arm64+0x261f7c)
    #17 0x000104999358 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libbase.dylib:arm64+0x261358)
    #18 0x0001047d1da4 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x208 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libbase.dylib:arm64+0x99da4)
    #19 0x00010499b498 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x32c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libbase.dylib:arm64+0x263498)
    #20 0x00010489a454 in base::RunLoop::Run(base::Location const&)+0x434 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libbase.dylib:arm64+0x162454)
    #21 0x0001303d02dc in content::UtilityMain(content::MainFunctionParams)+0x7d4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libcontent.dylib:arm64+0x38c42dc)
    #22 0x00013040b8f8 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x3d8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libcontent.dylib:arm64+0x38ff8f8)
    #23 0x00013040d860 in content::ContentMainRunnerImpl::Run()+0x448 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libcontent.dylib:arm64+0x3901860)
    #24 0x000130409124 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x5b4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libcontent.dylib:arm64+0x38fd124)
    #25 0x000130409980 in content::ContentMain(content::ContentMainParams)+0x190 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libcontent.dylib:arm64+0x38fd980)
    #26 0x0001179c028c in ChromeMain+0x360 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libchrome_dll.dylib:arm64+0xc28c)
    #27 0x0001023e8c94 in main+0x254 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/136.0.7096.0/Helpers/Chromium Helper.app/Contents/MacOS/Chromium Helper:arm64+0x100000c94)
    #28 0x00019a198270  (<unknown module>)

SUMMARY: AddressSanitizer: heap-use-after-free (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libc++_chrome.dylib:arm64+0x6ccc4) in std::__Cr::basic_streambuf<char, std::__Cr::char_traits<char>>::xsputn(char const*, long)+0xcc
Shadow bytes around the buggy address:
  0x606000052800: fa fa f7 fa fd fd fd fd fd fd fd fa fa fa f7 fa
  0x606000052880: fd fd fd fd fd fd fd fd fa fa f7 fa fd fd fd fd
  0x606000052900: fd fd fd fd fa fa f7 fa 00 00 00 00 00 00 00 fa
  0x606000052980: fa fa f7 fa 00 00 00 00 00 00 00 fa fa fa f7 fa
  0x606000052a00: 00 00 00 00 00 00 00 fa fa fa f7 fa fd fd fd fd
=>0x606000052a80: fd fd fd fa fa fa f7 fa[fd]fd fd fd fd fd fd fa
  0x606000052b00: fa fa f7 fa 00 00 00 00 00 00 00 00 fa fa f7 fa
  0x606000052b80: fd fd fd fd fd fd fd fa fa fa f7 fa fd fd fd fd
  0x606000052c00: fd fd fd fa fa fa f7 fa fd fd fd fd fd fd fd fa
  0x606000052c80: fa fa f7 fa 00 00 00 00 00 00 00 00 fa fa f7 fa
  0x606000052d00: fd fd fd fd fd fd fd fa fa fa f7 fa fd fd fd fd
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

==20622==ADDITIONAL INFO

==20622==Note: Please include this section with the ASan report.
Task trace:
    #0 0x0001303f2208 in video_effects::VideoEffectsServiceImpl::CreateWebGpuDeviceAndEffectsProcessors()+0x360 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libcontent.dylib:arm64+0x38e6208)
    #1 0x00010774b27c in IPC::ChannelAssociatedGroupController::NotifyEndpointOfError(IPC::ChannelAssociatedGroupController::Endpoint*, bool)+0x228 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libipc.dylib:arm64+0x4727c)
    #2 0x00010374afcc in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int)+0x238 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libmojo_public_system_cpp.dylib:arm64+0x1afcc)

Command line: `/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/136.0.7096.0/Helpers/Chromium Helper.app/Contents/MacOS/Chromium Helper --type=utility --utility-sub-type=video_effects.mojom.VideoEffectsService --lang=zh-CN --service-sandbox-type=service --no-sandbox --use-fake-device-for-media-stream --enable-experimental-web-platform-features --user-data-dir=/tmp/userdata/t11 --shared-files --metrics-shmem-handle=1752395122,r,1391373736273614438,16120701820397089619,524288 --field-trial-handle=1718379636,r,220246078397822839,8460141702355793248,262144 --enable-features=BlockInsecurePrivateNetworkRequests,BlockInsecurePrivateNetworkRequestsFromPrivate,BlockInsecurePrivateNetworkRequestsFromUnknown,CookieSameSiteConsidersRedirectChain,CreateImageBitmapOrientationNone,CriticalClientHint,DocumentPictureInPictureAPI,DocumentPolicyNegotiation,EnableCanvas2DLayers,ExperimentalContentSecurityPolicyFeatures,OriginIsolationHeader,PartitionedPopins,PrivateNetworkAccessRespectPreflightResults,SchemefulSameSite,StorageAccessHeaders,ThirdPartyStoragePartitioning --variations-seed-version`

MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==20622==END OF ADDITIONAL INFO
==20622==ABORTING
Received signal 6
 [0x000104ade3f4]
 [0x000104a933bc]
 [0x000104addfa8]
 [0x00019a54ede4]
 [0x00019a517f70]
 [0x00019a424908]
 [0x000102c8093c]
 [0x000102c7fe5c]
 [0x000102c6332c]
 [0x000102c625a0]
 [0x000102c57f54]
 [0x000102938cc8]
 [0x00012cb186bc]
 [0x00012cb18234]
 [0x0001303f3750]
 [0x0001303f526c]
 [0x0001303f85a0]
 [0x000104923814]
 [0x000104999f80]
 [0x00010499935c]
 [0x0001047d1da8]
 [0x00010499b49c]
 [0x00010489a458]
 [0x0001303d02e0]
 [0x00013040b8fc]
 [0x00013040d864]
 [0x000130409128]
 [0x000130409984]
 [0x0001179c0290]
 [0x0001023e8c98]
 [0x00019a198274]
[end of stack trace]

```
# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 27.5 KB)
- [index.html](attachments/index.html) (text/html, 191.0 KB)
- [poc.diff](attachments/poc.diff) (text/x-diff, 457.1 KB)
- [poc.mov](attachments/poc.mov) (video/quicktime, 104.1 MB)

## Timeline

### zh...@gmail.com (2025-03-30)

## Bisect commit

<https://chromium-review.googlesource.com/c/chromium/src/+/6112258>

### zh...@gmail.com (2025-03-30)

## RCA

This is a 53-byte UAF read, so the object being UAFed can be easily identified as the fields of [class Device::DeviceLostEvent](https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/wire/client/Device.cpp;l=165;drc=7ca86321d94b2fcc130ac751da8d35a02ddc43b9;bpv=0;bpt=0),that is: [std::string mMessage](https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/wire/client/Device.cpp;l=216;drc=7ca86321d94b2fcc130ac751da8d35a02ddc43b9;bpv=0;bpt=0)

In its private function [CompleteImpl](https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/wire/client/Device.cpp;l=189-192;drc=7ca86321d94b2fcc130ac751da8d35a02ddc43b9;bpv=0;bpt=0), `mMessage` is assigned a value of 53 bytes of "A valid external Instance reference no longer exists.":

```
void CompleteImpl(FutureID futureID, EventCompletionType completionType) override {
        if (completionType == EventCompletionType::Shutdown) {
            mReason = WGPUDeviceLostReason_CallbackCancelled;
            mMessage = "A valid external Instance reference no longer exists."; // 53 bytes here
        }
//...
}

```

The life cycle of `mMessage` is consistent with the class `Device::DeviceLostEvent` in which it is located. Therefore, when class `Device::DeviceLostEvent` is released, `mMessage` is also released. This can be seen in the asan log:

```
    #1 0x00013fd43b7c in dawn::wire::client::Device::DeviceLostEvent::~DeviceLostEvent()+0x90 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0328/libdawn_wire.dylib:arm64+0xe3b7c)

```

However, after that, [VideoEffectsServiceImpl::OnDeviceLost](https://source.chromium.org/chromium/chromium/src/+/main:services/video_effects/video_effects_service_impl.cc;l=144-148;drc=7ca86321d94b2fcc130ac751da8d35a02ddc43b9;bpv=0;bpt=0?q=VideoEffectsServiceImpl::OnDeviceLost&ss=chromium%2Fchromium%2Fsrc) is executed and reads the released `mMessage` (`std::string_view msg`):

```
  LOG(ERROR) << "wgpu::Device was lost; reason = "
             << base::to_underlying(reason) << ": " << msg; // UAF here !!!

```

Based on my analysis, [lokokung@google.com](mailto:lokokung@google.com) seems to be the better owner of this problem, because most of the code in `third_party/dawn/src/dawn/wire/client/Device.cpp` is written by him.

### zh...@gmail.com (2025-03-31)

Use a short C++ code to simulate the cause of this vulnerability:

```
#include <iostream>
#include <vector>
#include <string>
#include <string_view>

class Device{
public:
    explicit Device(std::string mMessage):mMessage_(std::move(mMessage)){}
    ~Device(){
        std::cout << "in Device ~~~ ~~~ " << std::endl;
    }
    std::string getMessage() const{
        return mMessage_;
    }
private:
    std::string mMessage_;
};

void test(){
    auto d1 = new Device("A valid external Instance reference no longer exists.");
    std::string_view v1(d1->getMessage());

    delete d1;
    std::cout << v1 << std::endl;
}


int main() {
    test();
    return 0;
}

```

Execute the following command:

```
g++ 1.cpp -std=c++17 -fsanitize=address; ./a.out

```

- result:

```
1.cpp:21:25: warning: object backing the pointer will be destroyed at the end of the full-expression [-Wdangling-gsl]
   21 |     std::string_view v1(d1->getMessage());
      |                         ^~~~~~~~~~~~~~~~
1 warning generated.
a.out(42059,0x1fbc74840) malloc: nano zone abandoned due to inability to reserve vm space.
in Device ~~~ ~~~ 
=================================================================
==42059==ERROR: AddressSanitizer: heap-use-after-free on address 0x606000000320 at pc 0x000104c6025c bp 0x00016b95df20 sp 0x00016b95d6e0
READ of size 53 at 0x606000000320 thread T0
    #0 0x104c60258 in memchr+0x27c (libclang_rt.asan_osx_dynamic.dylib:arm64e+0x1c258)
    #1 0x19219caf0 in __sfvwrite+0x270 (libsystem_c.dylib:arm64e+0x5af0)
    #2 0x1921b868c in fwrite+0x138 (libsystem_c.dylib:arm64e+0x2168c)
    #3 0x104c617cc in fwrite+0x78 (libclang_rt.asan_osx_dynamic.dylib:arm64e+0x1d7cc)
    #4 0x1044a596c in std::__1::basic_streambuf<char, std::__1::char_traits<char>>::sputn[abi:ne180100](char const*, long)+0xb8 (a.out:arm64+0x10000596c)
    #5 0x1044a5304 in std::__1::ostreambuf_iterator<char, std::__1::char_traits<char>> std::__1::__pad_and_output[abi:ne180100]<char, std::__1::char_traits<char>>(std::__1::ostreambuf_iterator<char, std::__1::char_traits<char>>, char const*, char const*, char const*, std::__1::ios_base&, char)+0x570 (a.out:arm64+0x100005304)
    #6 0x1044a48a4 in std::__1::basic_ostream<char, std::__1::char_traits<char>>& std::__1::__put_character_sequence[abi:ne180100]<char, std::__1::char_traits<char>>(std::__1::basic_ostream<char, std::__1::char_traits<char>>&, char const*, unsigned long)+0x410 (a.out:arm64+0x1000048a4)
    #7 0x1044a3bbc in std::__1::basic_ostream<char, std::__1::char_traits<char>>& std::__1::operator<<[abi:ne180100]<char, std::__1::char_traits<char>>(std::__1::basic_ostream<char, std::__1::char_traits<char>>&, std::__1::basic_string_view<char, std::__1::char_traits<char>>)+0x18c (a.out:arm64+0x100003bbc)
    #8 0x1044a3564 in test()+0x318 (a.out:arm64+0x100003564)
    #9 0x1044a3d70 in main+0x18 (a.out:arm64+0x100003d70)
    #10 0x191f84270  (<unknown module>)

0x606000000320 is located 0 bytes inside of 56-byte region [0x606000000320,0x606000000358)
freed by thread T0 here:
    #0 0x104ca82d4 in _ZdlPv+0x74 (libclang_rt.asan_osx_dynamic.dylib:arm64e+0x642d4)
    #1 0x1922321a8 in std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::~basic_string()+0x20 (libc++.1.dylib:arm64e+0x191a8)
    #2 0x1044a34bc in test()+0x270 (a.out:arm64+0x1000034bc)
    #3 0x1044a3d70 in main+0x18 (a.out:arm64+0x100003d70)
    #4 0x191f84270  (<unknown module>)

previously allocated by thread T0 here:
    #0 0x104ca7e94 in _Znwm+0x74 (libclang_rt.asan_osx_dynamic.dylib:arm64e+0x63e94)
    #1 0x19222be80 in std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::__init_copy_ctor_external(char const*, unsigned long)+0x58 (libc++.1.dylib:arm64e+0x12e80)
    #2 0x192231fc4 in std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>::basic_string(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&)+0x3c (libc++.1.dylib:arm64e+0x18fc4)
    #3 0x1044a37d4 in Device::getMessage() const+0x28 (a.out:arm64+0x1000037d4)
    #4 0x1044a3458 in test()+0x20c (a.out:arm64+0x100003458)
    #5 0x1044a3d70 in main+0x18 (a.out:arm64+0x100003d70)
    #6 0x191f84270  (<unknown module>)

SUMMARY: AddressSanitizer: heap-use-after-free (libclang_rt.asan_osx_dynamic.dylib:arm64e+0x1c258) in memchr+0x27c
Shadow bytes around the buggy address:
  0x606000000080: 00 00 00 00 00 00 00 00 fa fa fa fa 00 00 00 00
  0x606000000100: 00 00 00 00 fa fa fa fa 00 00 00 00 00 00 02 fa
  0x606000000180: fa fa fa fa 00 00 00 00 00 00 00 00 fa fa fa fa
  0x606000000200: 00 00 00 00 00 00 04 fa fa fa fa fa 00 00 00 00
  0x606000000280: 00 00 06 fa fa fa fa fa fd fd fd fd fd fd fd fa
=>0x606000000300: fa fa fa fa[fd]fd fd fd fd fd fd fa fa fa fa fa
  0x606000000380: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x606000000400: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x606000000480: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x606000000500: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x606000000580: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==42059==ABORTING
[1]    42059 abort      ./a.out

```

### za...@google.com (2025-03-31)

Hi mfoltz@ can you please take a look at this bug? I am setting the severity as S1 since it's a UaF bug. Note that I am not able to reproduce this as I can't build on MacOS devices. But the bisect from the reporter suggests this CL(<https://chromium-review.googlesource.com/c/chromium/src/+/6112258>) is where the potential culprit is. Can you please take a look? Thank you!

### ch...@google.com (2025-04-01)

Setting milestone because of s0/s1 severity.

### mf...@chromium.org (2025-04-01)

This shouldn't happen unless the browser is run with flags that are default-off, and it's a utility process crash in a sandboxed process, so the risk here is low. Still worth fixing of course.

I only work on media in my ~10% time so it may be a week or two until I get to this.

### zh...@gmail.com (2025-04-06)

## Streamlined POC

To reproduce the vulnerability more easily, you can download asan mac 1443156 and run the following command to reproduce the vulnerability stably. The only feature required to trigger the vulnerability is `CameraMicEffects`

```
rm -rf /tmp/userdata/; ./Chromium.app/Contents/MacOS/Chromium https://wpt.live/webrtc/RollbackEvents.https.html --no-sandbox --user-data-dir=/tmp/userdata/t11 --enable-features=CameraMicEffects

```

- asan log:

```
~/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156
rm -rf /tmp/userdata/; ./Chromium.app/Contents/MacOS/Chromium https://wpt.live/webrtc/RollbackEvents.https.html --no-sandbox --user-data-dir=/tmp/userdata/t11 --enable-features=CameraMicEffects
Chromium(19339,0x2007e9200) malloc: nano zone abandoned due to inability to reserve vm space.


chrome_crashpad_handler(19342,0x204f7d200) malloc: nano zone abandoned due to inability to reserve vm space.
chrome_crashpad_handler(19344,0x2032e0200) malloc: nano zone abandoned due to inability to reserve vm space.
[19339:6075469:0406/154144.297566:ERROR:chrome/browser/chrome_browser_main.cc:1036] The use of Rosetta to run the x64 version of Chromium on Arm is neither tested nor maintained, and unexpected behavior will likely result. Please check that all tools that spawn Chromium are Arm-native.
Chromium Helper(19351,0x2008ca200) malloc: nano zone abandoned due to inability to reserve vm space.
Chromium Helper(19352,0x204857200) malloc: nano zone abandoned due to inability to reserve vm space.
Chromium Helper(19353,0x204291200) malloc: nano zone abandoned due to inability to reserve vm space.
Chromium Helper (Alerts)(19354,0x200905200) malloc: nano zone abandoned due to inability to reserve vm space.
Chromium Helper (Renderer)(19355,0x204fa7200) malloc: nano zone abandoned due to inability to reserve vm space.
Chromium Helper (Renderer)(19356,0x201178200) malloc: nano zone abandoned due to inability to reserve vm space.
Chromium Helper(19363,0x2023b8200) malloc: nano zone abandoned due to inability to reserve vm space.
Chromium Helper (Renderer)(19366,0x2029fa200) malloc: nano zone abandoned due to inability to reserve vm space.
[19363:6075885:0406/154159.760216:ERROR:sandbox/mac/system_services.cc:31] SetApplicationIsDaemon: Error Domain=NSOSStatusErrorDomain Code=-50 "paramErr: error in user parameter list" (-50)
Chromium Helper (Plugin)(19367,0x204781200) malloc: nano zone abandoned due to inability to reserve vm space.
[19339:6075653:0406/154200.209311:ERROR:google_apis/gcm/engine/registration_request.cc:291] Registration response error message: DEPRECATED_ENDPOINT
[19339:6075469:0406/154203.018763:ERROR:chrome/browser/policy/cloud/fm_registration_token_uploader.cc:179] Client is missing for kUser scope
[19339:6075469:0406/154203.034695:ERROR:chrome/browser/policy/cloud/fm_registration_token_uploader.cc:179] Client is missing for kUser scope
Chromium Helper(19371,0x204835200) malloc: nano zone abandoned due to inability to reserve vm space.
Chromium Helper (Renderer)(19375,0x204851200) malloc: nano zone abandoned due to inability to reserve vm space.
=================================================================
==19371==ERROR: AddressSanitizer: heap-use-after-free on address 0x60600004d780 at pc 0x00010ce4c15d bp 0x00030cd739c0 sp 0x00030cd73178
READ of size 53 at 0x60600004d780 thread T0
==19371==WARNING: invalid path to external symbolizer!
==19371==WARNING: Failed to use and restart external symbolizer!
    #0 0x00010ce4c15c in __asan_memmove+0x25c (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Helpers/Chromium Helper.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:x86_64+0x5215c)
    #1 0x00016516b796 in std::__Cr::basic_streambuf<char, std::__Cr::char_traits<char>>::xsputn(char const*, long)+0xe6 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x11cca796)
    #2 0x0001534a8bbc in std::__Cr::ostreambuf_iterator<char, std::__Cr::char_traits<char>> std::__Cr::__pad_and_output<char, std::__Cr::char_traits<char>>(std::__Cr::ostreambuf_iterator<char, std::__Cr::char_traits<char>>, char const*, char const*, char const*, std::__Cr::ios_base&, char)+0x2ec (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x7bbc)
    #3 0x0001534a86cf in std::__Cr::basic_ostream<char, std::__Cr::char_traits<char>>& std::__Cr::__put_character_sequence<char, std::__Cr::char_traits<char>>(std::__Cr::basic_ostream<char, std::__Cr::char_traits<char>>&, char const*, unsigned long)+0x2df (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x76cf)
    #4 0x000162a30220 in video_effects::VideoEffectsServiceImpl::OnDeviceLost(wgpu::DeviceLostReason, std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>)+0x180 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0xf58f220)
    #5 0x000162a31f3b in base::internal::Invoker<base::internal::FunctorTraits<void (video_effects::VideoEffectsServiceImpl::*&&)(wgpu::DeviceLostReason, std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>), base::WeakPtr<video_effects::VideoEffectsServiceImpl>&&>, base::internal::BindState<true, true, false, void (video_effects::VideoEffectsServiceImpl::*)(wgpu::DeviceLostReason, std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>), base::WeakPtr<video_effects::VideoEffectsServiceImpl>>, void (wgpu::DeviceLostReason, std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>)>::RunOnce(base::internal::BindStateBase*, wgpu::DeviceLostReason, std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>&&)+0x20b (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0xf590f3b)
    #6 0x000162a356fe in base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (wgpu::DeviceLostReason, std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>)>&&, wgpu::DeviceLostReason&&, std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>&&>, base::internal::BindState<false, true, true, base::OnceCallback<void (wgpu::DeviceLostReason, std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>)>, wgpu::DeviceLostReason, std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x1ee (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0xf5946fe)
    #7 0x0001667b0158 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x388 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x1330f158)
    #8 0x00016681c595 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0xbd5 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x1337b595)
    #9 0x00016681b53f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x17f (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x1337a53f)
    #10 0x00016681d304 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x14 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x1337c304)
    #11 0x0001666841cc in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x29c (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x131e31cc)
    #12 0x00016681de61 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x3e1 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x1337ce61)
    #13 0x00016673762e in base::RunLoop::Run(base::Location const&)+0x53e (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x1329662e)
    #14 0x000161c94955 in content::UtilityMain(content::MainFunctionParams)+0x925 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0xe7f3955)
    #15 0x00016364ffdf in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x49f (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x101aefdf)
    #16 0x000163652276 in content::ContentMainRunnerImpl::Run()+0x536 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x101b1276)
    #17 0x00016364d809 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x649 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x101ac809)
    #18 0x00016364e1bc in content::ContentMain(content::ContentMainParams)+0x1cc (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x101ad1bc)
    #19 0x0001534a70d8 in ChromeMain+0x428 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x60d8)
    #20 0x0001044ead40 in main+0x260 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Helpers/Chromium Helper.app/Contents/MacOS/Chromium Helper:x86_64+0x100000d40)
    #21 0x00020477652f  (<unknown module>)

0x60600004d780 is located 0 bytes inside of 56-byte region [0x60600004d780,0x60600004d7b8)
freed by thread T0 here:
    #0 0x00010ce4ec2b in __asan_memmove+0x2d2b (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Helpers/Chromium Helper.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:x86_64+0x54c2b)
    #1 0x00016d5c74f8 in dawn::wire::client::Device::DeviceLostEvent::~DeviceLostEvent()+0x98 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x1a1264f8)
    #2 0x00016d5ce315 in std::__Cr::__tree<std::__Cr::__value_type<unsigned long long, std::__Cr::unique_ptr<dawn::wire::client::TrackedEvent, std::__Cr::default_delete<dawn::wire::client::TrackedEvent>>>, std::__Cr::__map_value_compare<unsigned long long, std::__Cr::__value_type<unsigned long long, std::__Cr::unique_ptr<dawn::wire::client::TrackedEvent, std::__Cr::default_delete<dawn::wire::client::TrackedEvent>>>, std::__Cr::less<unsigned long long>, true>, std::__Cr::allocator<std::__Cr::__value_type<unsigned long long, std::__Cr::unique_ptr<dawn::wire::client::TrackedEvent, std::__Cr::default_delete<dawn::wire::client::TrackedEvent>>>>>::destroy(std::__Cr::__tree_node<std::__Cr::__value_type<unsigned long long, std::__Cr::unique_ptr<dawn::wire::client::TrackedEvent, std::__Cr::default_delete<dawn::wire::client::TrackedEvent>>>, void*>*)+0xa5 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x1a12d315)
    #3 0x00016d5ce2cc in std::__Cr::__tree<std::__Cr::__value_type<unsigned long long, std::__Cr::unique_ptr<dawn::wire::client::TrackedEvent, std::__Cr::default_delete<dawn::wire::client::TrackedEvent>>>, std::__Cr::__map_value_compare<unsigned long long, std::__Cr::__value_type<unsigned long long, std::__Cr::unique_ptr<dawn::wire::client::TrackedEvent, std::__Cr::default_delete<dawn::wire::client::TrackedEvent>>>, std::__Cr::less<unsigned long long>, true>, std::__Cr::allocator<std::__Cr::__value_type<unsigned long long, std::__Cr::unique_ptr<dawn::wire::client::TrackedEvent, std::__Cr::default_delete<dawn::wire::client::TrackedEvent>>>>>::destroy(std::__Cr::__tree_node<std::__Cr::__value_type<unsigned long long, std::__Cr::unique_ptr<dawn::wire::client::TrackedEvent, std::__Cr::default_delete<dawn::wire::client::TrackedEvent>>>, void*>*)+0x5c (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x1a12d2cc)
    #4 0x00016d5cbbff in dawn::wire::client::EventManager::TransitionTo(dawn::wire::client::EventManager::State)+0x17f (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x1a12abff)
    #5 0x00016d5bcee5 in dawn::wire::client::Client::Disconnect()+0x2b5 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x1a11bee5)
    #6 0x00015f4184d7 in gpu::webgpu::DawnWireServices::Disconnect()+0x37 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0xbf774d7)
    #7 0x00015f41b279 in non-virtual thunk to gpu::webgpu::WebGPUImplementation::OnGpuControlLostContext()+0x129 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0xbf7a279)
    #8 0x000156fdd12f in gpu::CommandBufferProxyImpl::DisconnectChannel()+0x2ef (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x3b3c12f)
    #9 0x000156fdfb63 in gpu::CommandBufferProxyImpl::OnDisconnect()+0x323 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x3b3eb63)
    #10 0x000156fe8680 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::CommandBufferProxyImpl::*&&)(), gpu::CommandBufferProxyImpl*>, base::internal::BindState<true, true, false, void (gpu::CommandBufferProxyImpl::*)(), base::internal::UnretainedWrapper<gpu::CommandBufferProxyImpl, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x1d0 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x3b47680)
    #11 0x00016659c519 in mojo::InterfaceEndpointClient::NotifyError(std::__Cr::optional<mojo::DisconnectReason> const&)+0x509 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x130fb519)
    #12 0x00016961be22 in IPC::ChannelAssociatedGroupController::NotifyEndpointOfError(IPC::ChannelAssociatedGroupController::Endpoint*, bool)+0x4d2 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x1617ae22)
    #13 0x00016961c256 in IPC::ChannelAssociatedGroupController::NotifyEndpointOfErrorOnEndpointThread(unsigned int, base::raw_ptr<IPC::ChannelAssociatedGroupController::Endpoint, (partition_alloc::internal::RawPtrTraits)1>)+0x206 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x1617b256)
    #14 0x00016961c587 in void base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(unsigned int, base::raw_ptr<IPC::ChannelAssociatedGroupController::Endpoint, (partition_alloc::internal::RawPtrTraits)1>), IPC::ChannelAssociatedGroupController*&&, unsigned int&&, base::raw_ptr<IPC::ChannelAssociatedGroupController::Endpoint, (partition_alloc::internal::RawPtrTraits)1>>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(unsigned int, base::raw_ptr<IPC::ChannelAssociatedGroupController::Endpoint, (partition_alloc::internal::RawPtrTraits)1>), scoped_refptr<IPC::ChannelAssociatedGroupController>, unsigned int, base::internal::UnretainedWrapper<IPC::ChannelAssociatedGroupController::Endpoint, base::unretained_traits::MayDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<void (IPC::ChannelAssociatedGroupController::*)(unsigned int, base::raw_ptr<IPC::ChannelAssociatedGroupController::Endpoint, (partition_alloc::internal::RawPtrTraits)1>), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, unsigned int, base::internal::UnretainedWrapper<IPC::ChannelAssociatedGroupController::Endpoint, base::unretained_traits::MayDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul, 1ul, 2ul>(void (IPC::ChannelAssociatedGroupController::*&&)(unsigned int, base::raw_ptr<IPC::ChannelAssociatedGroupController::Endpoint, (partition_alloc::internal::RawPtrTraits)1>), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, unsigned int, base::internal::UnretainedWrapper<IPC::ChannelAssociatedGroupController::Endpoint, base::unretained_traits::MayDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul>)+0x257 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x1617b587)
    #15 0x0001667b0158 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x388 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x1330f158)
    #16 0x00016681c595 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0xbd5 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x1337b595)
    #17 0x00016681b53f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x17f (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x1337a53f)
    #18 0x00016681d304 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x14 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x1337c304)
    #19 0x0001666841cc in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x29c (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x131e31cc)
    #20 0x00016681de61 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x3e1 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x1337ce61)
    #21 0x00016673762e in base::RunLoop::Run(base::Location const&)+0x53e (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x1329662e)
    #22 0x000161c94955 in content::UtilityMain(content::MainFunctionParams)+0x925 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0xe7f3955)
    #23 0x00016364ffdf in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x49f (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x101aefdf)
    #24 0x000163652276 in content::ContentMainRunnerImpl::Run()+0x536 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x101b1276)
    #25 0x00016364d809 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x649 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x101ac809)
    #26 0x00016364e1bc in content::ContentMain(content::ContentMainParams)+0x1cc (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x101ad1bc)
    #27 0x0001534a70d8 in ChromeMain+0x428 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x60d8)
    #28 0x0001044ead40 in main+0x260 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Helpers/Chromium Helper.app/Contents/MacOS/Chromium Helper:x86_64+0x100000d40)
    #29 0x00020477652f  (<unknown module>)

previously allocated by thread T0 here:
    #0 0x00010ce4eb22 in __asan_memmove+0x2c22 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Helpers/Chromium Helper.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:x86_64+0x54b22)
    #1 0x00017d8585b7 in operator new(unsigned long)+0x27 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x2a3b75b7)
    #2 0x0001651deb11 in std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>::__grow_by_and_replace(unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, char const*)+0xd1 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x11d3db11)
    #3 0x0001651df7eb in std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>::__assign_external(char const*, unsigned long)+0xfb (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x11d3e7eb)
    #4 0x00016d5c770f in dawn::wire::client::Device::DeviceLostEvent::CompleteImpl(unsigned long long, dawn::EventCompletionType)+0xdf (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x1a12670f)
    #5 0x00016d5cc33e in dawn::wire::client::EventManager::TransitionTo(dawn::wire::client::EventManager::State)+0x8be (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x1a12b33e)
    #6 0x00016d5bcee5 in dawn::wire::client::Client::Disconnect()+0x2b5 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x1a11bee5)
    #7 0x00015f4184d7 in gpu::webgpu::DawnWireServices::Disconnect()+0x37 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0xbf774d7)
    #8 0x00015f41b279 in non-virtual thunk to gpu::webgpu::WebGPUImplementation::OnGpuControlLostContext()+0x129 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0xbf7a279)
    #9 0x000156fdd12f in gpu::CommandBufferProxyImpl::DisconnectChannel()+0x2ef (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x3b3c12f)
    #10 0x000156fdfb63 in gpu::CommandBufferProxyImpl::OnDisconnect()+0x323 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x3b3eb63)
    #11 0x000156fe8680 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::CommandBufferProxyImpl::*&&)(), gpu::CommandBufferProxyImpl*>, base::internal::BindState<true, true, false, void (gpu::CommandBufferProxyImpl::*)(), base::internal::UnretainedWrapper<gpu::CommandBufferProxyImpl, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x1d0 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x3b47680)
    #12 0x00016659c519 in mojo::InterfaceEndpointClient::NotifyError(std::__Cr::optional<mojo::DisconnectReason> const&)+0x509 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x130fb519)
    #13 0x00016961be22 in IPC::ChannelAssociatedGroupController::NotifyEndpointOfError(IPC::ChannelAssociatedGroupController::Endpoint*, bool)+0x4d2 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x1617ae22)
    #14 0x00016961c256 in IPC::ChannelAssociatedGroupController::NotifyEndpointOfErrorOnEndpointThread(unsigned int, base::raw_ptr<IPC::ChannelAssociatedGroupController::Endpoint, (partition_alloc::internal::RawPtrTraits)1>)+0x206 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x1617b256)
    #15 0x00016961c587 in void base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(unsigned int, base::raw_ptr<IPC::ChannelAssociatedGroupController::Endpoint, (partition_alloc::internal::RawPtrTraits)1>), IPC::ChannelAssociatedGroupController*&&, unsigned int&&, base::raw_ptr<IPC::ChannelAssociatedGroupController::Endpoint, (partition_alloc::internal::RawPtrTraits)1>>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(unsigned int, base::raw_ptr<IPC::ChannelAssociatedGroupController::Endpoint, (partition_alloc::internal::RawPtrTraits)1>), scoped_refptr<IPC::ChannelAssociatedGroupController>, unsigned int, base::internal::UnretainedWrapper<IPC::ChannelAssociatedGroupController::Endpoint, base::unretained_traits::MayDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<void (IPC::ChannelAssociatedGroupController::*)(unsigned int, base::raw_ptr<IPC::ChannelAssociatedGroupController::Endpoint, (partition_alloc::internal::RawPtrTraits)1>), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, unsigned int, base::internal::UnretainedWrapper<IPC::ChannelAssociatedGroupController::Endpoint, base::unretained_traits::MayDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul, 1ul, 2ul>(void (IPC::ChannelAssociatedGroupController::*&&)(unsigned int, base::raw_ptr<IPC::ChannelAssociatedGroupController::Endpoint, (partition_alloc::internal::RawPtrTraits)1>), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, unsigned int, base::internal::UnretainedWrapper<IPC::ChannelAssociatedGroupController::Endpoint, base::unretained_traits::MayDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul>)+0x257 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x1617b587)
    #16 0x0001667b0158 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x388 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x1330f158)
    #17 0x00016681c595 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0xbd5 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x1337b595)
    #18 0x00016681b53f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x17f (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x1337a53f)
    #19 0x00016681d304 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x14 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x1337c304)
    #20 0x0001666841cc in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x29c (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x131e31cc)
    #21 0x00016681de61 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x3e1 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x1337ce61)
    #22 0x00016673762e in base::RunLoop::Run(base::Location const&)+0x53e (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x1329662e)
    #23 0x000161c94955 in content::UtilityMain(content::MainFunctionParams)+0x925 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0xe7f3955)
    #24 0x00016364ffdf in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x49f (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x101aefdf)
    #25 0x000163652276 in content::ContentMainRunnerImpl::Run()+0x536 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x101b1276)
    #26 0x00016364d809 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x649 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x101ac809)
    #27 0x00016364e1bc in content::ContentMain(content::ContentMainParams)+0x1cc (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x101ad1bc)
    #28 0x0001534a70d8 in ChromeMain+0x428 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x60d8)
    #29 0x0001044ead40 in main+0x260 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Helpers/Chromium Helper.app/Contents/MacOS/Chromium Helper:x86_64+0x100000d40)

SUMMARY: AddressSanitizer: heap-use-after-free (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x11cca796) in std::__Cr::basic_streambuf<char, std::__Cr::char_traits<char>>::xsputn(char const*, long)+0xe6
Shadow bytes around the buggy address:
  0x60600004d500: fd fd fd fd fa fa f7 fa fd fd fd fd fd fd fd fa
  0x60600004d580: fa fa f7 fa 00 00 00 00 00 00 00 fa fa fa f7 fa
  0x60600004d600: fd fd fd fd fd fd fd fa fa fa f7 fa fd fd fd fd
  0x60600004d680: fd fd fd fa fa fa f7 fa fd fd fd fd fd fd fd fa
  0x60600004d700: fa fa f7 fa fd fd fd fd fd fd fd fd fa fa f7 fa
=>0x60600004d780:[fd]fd fd fd fd fd fd fa fa fa f7 fa 00 00 00 00
  0x60600004d800: 00 00 00 00 fa fa f7 fa 00 00 00 00 00 00 00 00
  0x60600004d880: fa fa f7 fa fd fd fd fd fd fd fd fa fa fa f7 fa
  0x60600004d900: fd fd fd fd fd fd fd fa fa fa f7 fa 00 00 00 00
  0x60600004d980: 00 00 00 fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x60600004da00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==19371==ADDITIONAL INFO

==19371==Note: Please include this section with the ASan report.
Task trace:
    #0 0x000162a2ead2 in video_effects::VideoEffectsServiceImpl::CreateWebGpuDeviceAndEffectsProcessors()+0x422 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0xf58dad2)
    #1 0x00016961bbf7 in IPC::ChannelAssociatedGroupController::NotifyEndpointOfError(IPC::ChannelAssociatedGroupController::Endpoint*, bool)+0x2a7 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Chromium Framework:x86_64+0x1617abf7)


Command line: `/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1443156/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/137.0.7111.0/Helpers/Chromium Helper.app/Contents/MacOS/Chromium Helper --type=utility --utility-sub-type=video_effects.mojom.VideoEffectsService --lang=zh-CN --service-sandbox-type=service --no-sandbox --user-data-dir=/tmp/userdata/t11 --shared-files --metrics-shmem-handle=1752395122,r,13864777176726645377,3540275483318182800,524288 --field-trial-handle=1718379636,r,16609507799193086395,14846044316104397296,262144 --enable-features=CameraMicEffects --variations-seed-version`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==19371==END OF ADDITIONAL INFO
==19371==ABORTING
Received signal 6
 [0x00016691a392]
 [0x0001668ebda3]
 [0x00016691a1e8]
 [0x7ff80ae3d25d]
 [0x00017e7dcd3c]
 [0x7ff80ad2373e]
 [0x00010ce782c8]
 [0x00010ce777b1]
 [0x00010ce58df3]
 [0x00010ce57f17]
 [0x00010ce4c18d]
 [0x00016516b797]
 [0x0001534a8bbd]
 [0x0001534a86d0]
 [0x000162a30221]
 [0x000162a31f3c]
 [0x000162a356ff]
 [0x0001667b0159]
 [0x00016681c596]
 [0x00016681b540]
 [0x00016681d305]
 [0x0001666841cd]
 [0x00016681de62]
 [0x00016673762f]
 [0x000161c94956]
 [0x00016364ffe0]
 [0x000163652277]
 [0x00016364d80a]
 [0x00016364e1bd]
 [0x0001534a70d9]
 [0x0001044ead41]
 [0x000204776530]
[end of stack trace]

```

### ch...@google.com (2025-04-16)

mfoltz: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-17)

mfoltz: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-18)

mfoltz: Uh oh! This issue still open and hasn't been updated in the last 16 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### bi...@chromium.org (2025-04-18)

I am reducing the severity and priority given that the runtime feature that gates this code was (and still is) disabled by default. In addition, the video\_effects\_service\_impl.cc belongs to a [target](https://source.chromium.org/chromium/chromium/src/+/main:services/video_effects/BUILD.gn;l=18;drc=87a0737293e42d60a8e08028fafa577973bddf52) that is only [compiled](https://source.chromium.org/chromium/chromium/src/+/main:content/utility/BUILD.gn;l=88;drc=f3f56feaa064616c819218cfd3a96c9cc0a57c3b) when `enable_video_effects` build flag is set to true - this is not the case as of CL <https://crrev.com/c/6460788> (which landed yesterday).

As for the proper fix, I don't have an easy way of reproing the issue myself right now, but I'm guessing that all that is needed here is switching the type of the `msg` parameter from `std::string_view` to `std::string` in `VideoEffectsServiceImpl::OnDeviceError()` and `VideoEffectsServiceImpl::OnDeviceLost()`.

### zh...@gmail.com (2025-04-19)

Hi, don't worry, after my test, this fix can indeed fix this vulnerability. I verified it as follows

```
git checkout c096101161292a37f8a0865c7266c90e0c8bb5d1
git apply fix.diff

```
```
diff --git a/services/video_effects/video_effects_service_impl.cc b/services/video_effects/video_effects_service_impl.cc
index eef4bfdf0185d..4f560e78aeceb 100644
--- a/services/video_effects/video_effects_service_impl.cc
+++ b/services/video_effects/video_effects_service_impl.cc
@@ -5,7 +5,7 @@
 #include "services/video_effects/video_effects_service_impl.h"
 
 #include <memory>
-#include <string_view>
+#include <string>
 #include <utility>
 
 #include "base/check.h"
@@ -133,7 +133,7 @@ void VideoEffectsServiceImpl::OnDeviceCreated(wgpu::Device device) {
 }
 
 void VideoEffectsServiceImpl::OnDeviceError(WebGpuDevice::Error error,
-                                            std::string_view msg) {
+                                            std::string msg) {
   DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
   CHECK(!device_);
   LOG(WARNING) << "Unable to create wgpu::Device; error = "
@@ -142,7 +142,7 @@ void VideoEffectsServiceImpl::OnDeviceError(WebGpuDevice::Error error,
 }
 
 void VideoEffectsServiceImpl::OnDeviceLost(wgpu::DeviceLostReason reason,
-                                           std::string_view msg) {
+                                           std::string msg) {
   DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
   LOG(ERROR) << "wgpu::Device was lost; reason = "
              << base::to_underlying(reason) << ": " << msg;
diff --git a/services/video_effects/video_effects_service_impl.h b/services/video_effects/video_effects_service_impl.h
index c941b381686e7..412efff2cea33 100644
--- a/services/video_effects/video_effects_service_impl.h
+++ b/services/video_effects/video_effects_service_impl.h
@@ -59,8 +59,8 @@ class VideoEffectsServiceImpl : public mojom::VideoEffectsService,
 
   // Callback functions for WebGpuDevice.
   void OnDeviceCreated(wgpu::Device device);
-  void OnDeviceError(WebGpuDevice::Error error, std::string_view msg);
-  void OnDeviceLost(wgpu::DeviceLostReason reason, std::string_view msg);
+  void OnDeviceError(WebGpuDevice::Error error, std::string msg);
+  void OnDeviceLost(wgpu::DeviceLostReason reason, std::string msg);
 
   // Finishes creation of pending effects processors in `pending_processors_`.
   void FinishCreatingEffectsProcessors();
diff --git a/services/video_effects/webgpu_device.cc b/services/video_effects/webgpu_device.cc
index 4a2b331aead9b..b913be9d933ed 100644
--- a/services/video_effects/webgpu_device.cc
+++ b/services/video_effects/webgpu_device.cc
@@ -4,6 +4,7 @@
 
 #include "services/video_effects/webgpu_device.h"
 
+#include <string>
 #include <string_view>
 #include <type_traits>
 #include <utility>
@@ -25,6 +26,14 @@
 #include "third_party/mediapipe/src/mediapipe/gpu/webgpu/webgpu_device_registration.h"
 #endif
 
+namespace {
+
+std::string ToString(wgpu::StringView string_view) {
+  return std::string(std::string_view(string_view));
+}
+
+}  // namespace
+
 namespace video_effects {
 
 WebGpuDevice::WebGpuDevice(
@@ -68,7 +77,7 @@ void WebGpuDevice::Initialize(DeviceCallback device_cb,
          ErrorCallback error_cb, wgpu::RequestAdapterStatus status,
          wgpu::Adapter adapter, wgpu::StringView message) {
         if (self) {
-          self->OnRequestAdapter(status, std::move(adapter), message,
+          self->OnRequestAdapter(status, std::move(adapter), ToString(message),
                                  std::move(device_cb), std::move(error_cb));
         }
       },
@@ -83,13 +92,13 @@ void WebGpuDevice::Initialize(DeviceCallback device_cb,
 
 void WebGpuDevice::OnRequestAdapter(wgpu::RequestAdapterStatus status,
                                     wgpu::Adapter adapter,
-                                    std::string_view message,
+                                    std::string message,
                                     DeviceCallback device_cb,
                                     ErrorCallback error_cb) {
   DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
 
   if (status != wgpu::RequestAdapterStatus::Success || !adapter) {
-    std::move(error_cb).Run(Error::kFailedToObtainAdapter, message);
+    std::move(error_cb).Run(Error::kFailedToObtainAdapter, std::move(message));
     return;
   }
 
@@ -101,7 +110,7 @@ void WebGpuDevice::OnRequestAdapter(wgpu::RequestAdapterStatus status,
       [](base::WeakPtr<WebGpuDevice> self, const wgpu::Device& device,
          wgpu::DeviceLostReason reason, wgpu::StringView message) {
         if (self) {
-          self->OnDeviceLost(device, reason, message);
+          self->OnDeviceLost(device, reason, ToString(message));
         }
       },
       weak_ptr_factory_.GetWeakPtr());
@@ -123,7 +132,8 @@ void WebGpuDevice::OnRequestAdapter(wgpu::RequestAdapterStatus status,
         // We're treating uncaptured WebGPU error like a device loss. It likely
         // signifies programmer error, meaning that we can't really trust the
         // contents of the textures that we're producing.
-        self->OnDeviceLost(device, wgpu::DeviceLostReason::Unknown, message);
+        self->OnDeviceLost(device, wgpu::DeviceLostReason::Unknown,
+                                        ToString(message));
       },
       weak_ptr_factory_.GetWeakPtr());
 
@@ -136,7 +146,7 @@ void WebGpuDevice::OnRequestAdapter(wgpu::RequestAdapterStatus status,
          ErrorCallback error_cb, wgpu::RequestDeviceStatus status,
          wgpu::Device device, wgpu::StringView message) {
         if (self) {
-          self->OnRequestDevice(status, std::move(device), message,
+          self->OnRequestDevice(status, std::move(device), ToString(message),
                                 std::move(device_cb), std::move(error_cb));
         }
       },
@@ -150,12 +160,12 @@ void WebGpuDevice::OnRequestAdapter(wgpu::RequestAdapterStatus status,
 
 void WebGpuDevice::OnRequestDevice(wgpu::RequestDeviceStatus status,
                                    wgpu::Device device,
-                                   std::string_view message,
+                                   std::string message,
                                    DeviceCallback device_cb,
                                    ErrorCallback error_cb) {
   DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
   if (status != wgpu::RequestDeviceStatus::Success || !device) {
-    std::move(error_cb).Run(Error::kFailedToObtainDevice, message);
+    std::move(error_cb).Run(Error::kFailedToObtainDevice, std::move(message));
     return;
   }
 
@@ -171,14 +181,14 @@ void WebGpuDevice::OnRequestDevice(wgpu::RequestDeviceStatus status,
 
 void WebGpuDevice::OnDeviceLost(const wgpu::Device& device,
                                 wgpu::DeviceLostReason reason,
-                                std::string_view message) {
+                                std::string message) {
   DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
 
 #if MEDIAPIPE_USE_WEBGPU
   mediapipe::WebGpuDeviceRegistration::GetInstance().UnRegisterWebGpuDevice();
 #endif
   if (device_lost_cb_) {
-    std::move(device_lost_cb_).Run(reason, message);
+    std::move(device_lost_cb_).Run(reason, std::move(message));
   }
 }
 
diff --git a/services/video_effects/webgpu_device.h b/services/video_effects/webgpu_device.h
index af1d824d7bb1c..f9f838755483a 100644
--- a/services/video_effects/webgpu_device.h
+++ b/services/video_effects/webgpu_device.h
@@ -30,10 +30,10 @@ class WebGpuDevice final {
     kUncapturedError,
   };
 
-  using DeviceCallback = base::OnceCallback<void(wgpu::Device)>;
-  using ErrorCallback = base::OnceCallback<void(Error, std::string_view)>;
-  using DeviceLostCallback =
-      base::OnceCallback<void(wgpu::DeviceLostReason, std::string_view)>;
+    using DeviceCallback = base::OnceCallback<void(wgpu::Device)>;
+    using ErrorCallback = base::OnceCallback<void(Error, std::string)>;
+    using DeviceLostCallback =
+        base::OnceCallback<void(wgpu::DeviceLostReason, std::string)>;
 
   // `context_provider` provides access to the GPU context (command buffer).
   // `device_lost_cb` is invoked if the GPU context was lost with the reason and
@@ -60,19 +60,19 @@ class WebGpuDevice final {
  private:
   void OnRequestAdapter(wgpu::RequestAdapterStatus status,
                         wgpu::Adapter adapter,
-                        std::string_view message,
+                        std::string message,
                         DeviceCallback device_cb,
                         ErrorCallback error_cb);
 
   void OnRequestDevice(wgpu::RequestDeviceStatus status,
                        wgpu::Device device,
-                       std::string_view message,
+                       std::string message,
                        DeviceCallback device_cb,
                        ErrorCallback error_cb);
 
   void OnDeviceLost(const wgpu::Device& device,
                     wgpu::DeviceLostReason reason,
-                    std::string_view message);
+                    std::string message);
 
   static void LoggingCallback(wgpu::LoggingType type, wgpu::StringView message);
 


```

Repeated the method of triggering the vulnerability in the vulnerability report, and I can no longer trigger this vulnerability

### pg...@google.com (2025-04-21)

(Updating labels per comment #12 - updating impact to None! thank you for the info! )

### dx...@google.com (2025-04-22)

Project: chromium/src  

Branch: main  

Author: mark a. foltz [mfoltz@chromium.org](mailto:mfoltz@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6473272>

[Video Effects] Convert wgpu::StringView to std::string.

---


Expand for full commit details
```
     
    This prevents passing unowned strings into clients of WebGpuDevice via 
    callbacks. 
     
    Fixed: 407315793 
    Change-Id: Ib03912c875124a0497f2800bf3c77012f588d133 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6473272 
    Reviewed-by: Piotr Bialecki <bialpio@chromium.org> 
    Commit-Queue: Mark Foltz <mfoltz@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1449890}

```

---

Files:

- M `services/video_effects/video_effects_service_impl.cc`
- M `services/video_effects/video_effects_service_impl.h`
- M `services/video_effects/webgpu_device.cc`
- M `services/video_effects/webgpu_device.h`

---

Hash: 17c050eef5e206a3d45054030b6941a8bf048490  

Date:  Tue Apr 22 13:57:59 2025


---

### sp...@google.com (2025-04-25)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
$2,000 for report of significantly mitigated memory corruption in a non-sandboxed project, mitigated by precondition for shutdown and UI gestures / user granting permissions + $1,000 patch bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### zh...@gmail.com (2025-04-26)

Thank you very much Amy, Cheers🍻

### zh...@gmail.com (2025-05-20)

Hi, I would like to ask if there is any progress on this bug reward? The later bug bounty I submitted has been received, but the earlier one has not been received

### am...@chromium.org (2025-05-20)

Hello, I reached out to the finance team. According to their records, this reward payment was indeed processed. If it has not already, it should be paid to your account soon.

### zh...@gmail.com (2025-05-21)

Thank you very much. I have seen the payment invoice.

### ch...@google.com (2025-07-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/407315793)*
