# DCOMPSurfaceRegistry race in Media Foundation DirectComposition

| Field | Value |
|-------|-------|
| **Issue ID** | [493315759](https://issues.chromium.org/issues/493315759) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>Internals |
| **Platforms** | Windows |
| **Reporter** | ke...@gmail.com |
| **Assignee** | jo...@chromium.org |
| **Created** | 2026-03-17 |
| **Bounty** | $4,000.00 |

## Description

## Vulnerability Details

`gl::DCOMPSurfaceRegistry` is a process-wide singleton in the GPU process that maps `UnguessableToken` to DCOMP surface handles via a `base::flat_map`.

`RegisterDCOMPSurfaceHandle` and `UnregisterDCOMPSurfaceHandle` are called on the GPU IO thread via `GpuServiceImpl`.  

While `TakeDCOMPSurfaceHandle` is called on the GPU main scheduler thread via `DCOMPTexture`.

Concurrent access can corrupt the contiguous-storage container, leading to out-of-bounds access, UAF, etc in the GPU process.

The DCOMP surface path is reachable through both clear and encrypted Media Foundation playback on Windows. Both paths converge at the same flow:
`MediaFoundationRendererWrapper::OnReceiveDCOMPSurface → DCOMPSurfaceRegistryBroker → GpuServiceImpl`
and the same take flow:
`DCOMPTexture::SetDCOMPSurfaceHandle`

- Clear playback requires `--enable-features=MediaFoundationClearPlayback` (`FEATURE_DISABLED_BY_DEFAULT`).
- Encrypted/DRM playback is enabled by default on x86\_64 Windows 10 20H1+ via `kHardwareSecureDecryption` (`FEATURE_ENABLED_BY_DEFAULT`).  
  
  Any DRM-protected video (e.g. Widevine content) triggers this path without any flags.

---

## Reproduction Case

The core PoC idea is to rapidly create and tear down Media Foundation DirectComposition video instances so DCOMP surface registration and consumption overlap

Revision: 5990b7366c12ac9102276663d7ae6069faae6b76 but the relevant files haven't been touched since 2022

1. Add some delays, patch `ui\gl\dcomp_surface_registry.cc` with attached diff
2. `python -m http.server 8000` in the directory with the html and webm files
3. Run with in fresh profile  
   
   `.\chrome.exe --no-sandbox --profile-directory=xxx --enable-features=MediaFoundationClearPlayback "http://127.0.0.1:8000/dcomp_race_test_v44.html?video=http://127.0.0.1:8000/red-a500hz.webm"`

Very unreliable, and there are multiple crashes that are not security related that can kill the GPU process, even before reaching DCOMP path. The POC tries to "tune" the timings automatically, but usually it either crashes early, or never. So better to restart if nothing happens after a few minutes.

Most common crash is this, attached Uaf, heapbof:

```

==52704==ERROR: AddressSanitizer: container-overflow on address 0x120e7da66038 at pc 0x7ffb9a0cb4ec bp 0x00f9ec30c960 sp 0x00f9ec30c9a8
[52704:28508:0310/191005.549:ERROR:gpu\ipc\service\dcomp_texture_win.cc:230] SetDCOMPSurfaceHandle: No surface registered for token (C32F19E478142311778D829FF2292F79)
WRITE of size 16 at 0x120e7da66038 thread T47
==52704==*** WARNING: Failed to initialize DbgHelp!              ***
==52704==*** Most likely this means that the app is already      ***
==52704==*** using DbgHelp, possibly with incompatible flags.    ***
==52704==*** Due to technical reasons, symbolization might crash ***
==52704==*** or produce wrong results.                           ***
[51916:57220:0310/191006.217:INFO:CONSOLE:122] "[2026-03-10T18:10:06.216Z] elapsed=51952ms active_videos=19 anchors=1 churn=18/18 add=19 remove=0 reload=330 video_err=32 play_err=197 tick_now=25 batch_max_now=1 reload_gap_now=100 tuning=on", source: http://127.0.0.1:8000/dcomp_mojo_race_test_v42.html?video=http://127.0.0.1:8000/red-a500hz.webm (122)
    #0 0x7ffb9a0cb4eb in _asan_memcpy+0x3db (F:\src\chromium\src\out\march\clang_rt.asan_dynamic-x86_64.dll+0x18004b4eb)
    #1 0x7ffb5424ae2a in std::__Cr::vector<std::__Cr::pair<base::UnguessableToken,base::win::GenericScopedHandle<base::win::HandleTraits,base::win::VerifierTraits> >,std::__Cr::allocator<std::__Cr::pair<base::UnguessableToken,base::win::GenericScopedHandle<base::win::HandleTraits,base::win::VerifierTraits> > > >::__move_range F:\src\chromium\src\third_party\libc++\src\include\__vector\vector.h:1190
    #2 0x7ffb5424a7e0 in std::__Cr::vector<std::__Cr::pair<base::UnguessableToken,base::win::GenericScopedHandle<base::win::HandleTraits,base::win::VerifierTraits> >,std::__Cr::allocator<std::__Cr::pair<base::UnguessableToken,base::win::GenericScopedHandle<base::win::HandleTraits,base::win::VerifierTraits> > > >::emplace<const base::UnguessableToken &,base::win::GenericScopedHandle<base::win::HandleTraits,base::win::VerifierTraits> > F:\src\chromium\src\third_party\libc++\src\include\__vector\vector.h:1244
    #3 0x7ffb54249540 in base::flat_map<base::UnguessableToken,base::win::GenericScopedHandle<base::win::HandleTraits,base::win::VerifierTraits>,std::__Cr::less<void>,std::__Cr::vector<std::__Cr::pair<base::UnguessableToken,base::win::GenericScopedHandle<base::win::HandleTraits,base::win::VerifierTraits> >,std::__Cr::allocator<std::__Cr::pair<base::UnguessableToken,base::win::GenericScopedHandle<base::win::HandleTraits,base::win::VerifierTraits> > > > >::operator[]<base::UnguessableToken> F:\src\chromium\src\base\containers\flat_map.h:315
    #4 0x7ffb54248eec in gl::DCOMPSurfaceRegistry::RegisterDCOMPSurfaceHandle F:\src\chromium\src\ui\gl\dcomp_surface_registry.cc:27
    #5 0x7ffac7e469bf in viz::GpuServiceImpl::RegisterDCOMPSurfaceHandle F:\src\chromium\src\components\viz\service\gl\gpu_service_impl.cc:582
    #6 0x7ffac810fe6e in viz::mojom::GpuServiceStubDispatch::AcceptWithResponder F:\src\chromium\src\out\march\gen\services\viz\privileged\mojom\gl\gpu_service.mojom.cc:3792
    #7 0x7ffac7e64060 in viz::mojom::GpuServiceStub<mojo::RawPtrImplRefTraits<viz::mojom::GpuService> >::AcceptWithResponder F:\src\chromium\src\out\march\gen\services\viz\privileged\mojom\gl\gpu_service.mojom.h:396
    #8 0x7ffbf3c5cae6 in mojo::InterfaceEndpointClient::HandleValidatedMessage F:\src\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:1036
    #9 0x7ffbf3c7cd86 in mojo::MessageDispatcher::Accept F:\src\chromium\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:44
    #10 0x7ffbf3c6428c in mojo::InterfaceEndpointClient::HandleIncomingMessage F:\src\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:747
    #11 0x7ffbf3c90178 in mojo::internal::MultiplexRouter::ProcessIncomingMessage F:\src\chromium\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:1204
    #12 0x7ffbf3c8e303 in mojo::internal::MultiplexRouter::Accept F:\src\chromium\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:790
    #13 0x7ffbf3c7cd86 in mojo::MessageDispatcher::Accept F:\src\chromium\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:44
    #14 0x7ffbf3c3c83d in mojo::Connector::DispatchMessageW F:\src\chromium\src\mojo\public\cpp\bindings\lib\connector.cc:568
    #15 0x7ffbf3c3e8c1 in mojo::Connector::ReadAllAvailableMessages F:\src\chromium\src\mojo\public\cpp\bindings\lib\connector.cc:629
    #16 0x7ffbf3c3e082 in mojo::Connector::OnWatcherHandleReady F:\src\chromium\src\mojo\public\cpp\bindings\lib\connector.cc:420
    #17 0x7ffbf3c41db3 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::*const &)(const char *, unsigned int),mojo::Connector *,const char *const &>,base::internal::BindState<1,1,0,void (mojo::Connector::*)(const char *, unsigned int),base::internal::UnretainedWrapper<mojo::Connector,base::unretained_traits::MayNotDangle,0>,base::internal::UnretainedWrapper<const char,base::unretained_traits::MayNotDangle,0> >,void (unsigned int)>::Run F:\src\chromium\src\base\functional\bind_internal.h:989
    #18 0x7ffbf3c41225 in base::RepeatingCallback<void (unsigned int)>::Run F:\src\chromium\src\base\functional\callback.h:346
    #19 0x7ffbf3c40f3d in base::internal::Invoker<base::internal::FunctorTraits<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),const base::RepeatingCallback<void (unsigned int)> &>,base::internal::BindState<0,1,0,void (*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),base::RepeatingCallback<void (unsigned int)> >,void (unsigned int, const mojo::HandleSignalsState &)>::Run F:\src\chromium\src\base\functional\bind_internal.h:989
    #20 0x7ffbf5b47204 in base::RepeatingCallback<void (unsigned int, const mojo::HandleSignalsState &)>::Run F:\src\chromium\src\base\functional\callback.h:346
    #21 0x7ffbf5b46a6d in mojo::SimpleWatcher::OnHandleReady F:\src\chromium\src\mojo\public\cpp\system\simple_watcher.cc:286
    #22 0x7ffbf5b47694 in mojo::SimpleWatcher::Context::Notify F:\src\chromium\src\mojo\public\cpp\system\simple_watcher.cc:97
    #23 0x7ffbf5b43d8a in mojo::SimpleWatcher::Context::CallNotify F:\src\chromium\src\mojo\public\cpp\system\simple_watcher.cc:61
    #24 0x7ffad0ac3c8f in mojo::core::ipcz_driver::MojoTrap::DispatchEvent F:\src\chromium\src\mojo\core\ipcz_driver\mojo_trap.cc:605
    #25 0x7ffad0abfc67 in mojo::core::ipcz_driver::MojoTrap::DispatchOrQueueEvent F:\src\chromium\src\mojo\core\ipcz_driver\mojo_trap.cc:577
    #26 0x7ffad0ac2e2e in mojo::core::ipcz_driver::MojoTrap::HandleEvent F:\src\chromium\src\mojo\core\ipcz_driver\mojo_trap.cc:459
    #27 0x7ffad0ac2028 in mojo::core::ipcz_driver::MojoTrap::TrapEventHandler F:\src\chromium\src\mojo\core\ipcz_driver\mojo_trap.cc:393
    #28 0x7ffad0baceda in ipcz::TrapEventDispatcher::~TrapEventDispatcher F:\src\chromium\src\third_party\ipcz\src\ipcz\trap_event_dispatcher.cc:12
    #29 0x7ffad0b8dd8b in ipcz::Router::AcceptInboundParcel F:\src\chromium\src\third_party\ipcz\src\ipcz\router.cc:272
    #30 0x7ffad0b47435 in ipcz::NodeLink::AcceptCompleteParcel F:\src\chromium\src\third_party\ipcz\src\ipcz\node_link.cc:1082
    #31 0x7ffad0b4c383 in ipcz::NodeLink::OnAcceptParcel F:\src\chromium\src\third_party\ipcz\src\ipcz\node_link.cc:666
    #32 0x7ffad0b76bb8 in ipcz::msg::NodeMessageListener::OnTransportMessage F:\src\chromium\src\third_party\ipcz\src\ipcz\node_messages.cc:746
    #33 0x7ffad0b0a007 in ipcz::`anonymous namespace'::NotifyTransport F:\src\chromium\src\third_party\ipcz\src\ipcz\driver_transport.cc:47
    #34 0x7ffad0adbb93 in mojo::core::ipcz_driver::Transport::OnChannelMessage F:\src\chromium\src\mojo\core\ipcz_driver\transport.cc:744
    #35 0x7ffad0a7ead9 in mojo::core::Channel::TryDispatchMessage F:\src\chromium\src\mojo\core\channel.cc:1210
    #36 0x7ffad0a7c97d in mojo::core::Channel::OnReadComplete F:\src\chromium\src\mojo\core\channel.cc:1094
    #37 0x7ffad0aec9c6 in mojo::core::`anonymous namespace'::ChannelWin::OnIOCompleted F:\src\chromium\src\mojo\core\channel_win.cc:253
    #38 0x7ffb92a489bc in base::MessagePumpForIO::WaitForIOCompletion F:\src\chromium\src\base\message_loop\message_pump_win.cc:903
    #39 0x7ffb92a47f9a in base::MessagePumpForIO::DoRunLoop F:\src\chromium\src\base\message_loop\message_pump_win.cc:843
    #40 0x7ffb92a3eec3 in base::MessagePumpWin::Run F:\src\chromium\src\base\message_loop\message_pump_win.cc:87
    #41 0x7ffb92829603 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run F:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:650
    #42 0x7ffb92692aea in base::RunLoop::Run F:\src\chromium\src\base\run_loop.cc:135
    #43 0x7ffb9291b408 in base::Thread::Run F:\src\chromium\src\base\threading\thread.cc:361
    #44 0x7ffb371b3275 in content::`anonymous namespace'::ChildIOThread::Run F:\src\chromium\src\content\child\child_process.cc:69
    #45 0x7ffb9291bc4e in base::Thread::ThreadMain F:\src\chromium\src\base\threading\thread.cc:436
    #46 0x7ffb92a9a320 in base::`anonymous namespace'::ThreadFunc F:\src\chromium\src\base\threading\platform_thread_win.cc:112
    #47 0x7ffb9a0ddc6e in _asan_wrap_CreateThread+0x14e (F:\src\chromium\src\out\march\clang_rt.asan_dynamic-x86_64.dll+0x18005dc6e)
    #48 0x7ffc4892e8d6 in BaseThreadInitThunk+0x16 (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #49 0x7ffc49a4c40b in RtlUserThreadStart+0x2b (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18008c40b)

0x120e7da66038 is located 24 bytes inside of 96-byte region [0x120e7da66020,0x120e7da66080)
allocated by thread T47 here:
    #0 0x7ffb9a0de46f in operator new+0x8f (F:\src\chromium\src\out\march\clang_rt.asan_dynamic-x86_64.dll+0x18005e46f)
    #1 0x7ffb5424a905 in std::__Cr::vector<std::__Cr::pair<base::UnguessableToken,base::win::GenericScopedHandle<base::win::HandleTraits,base::win::VerifierTraits> >,std::__Cr::allocator<std::__Cr::pair<base::UnguessableToken,base::win::GenericScopedHandle<base::win::HandleTraits,base::win::VerifierTraits> > > >::emplace<const base::UnguessableToken &,base::win::GenericScopedHandle<base::win::HandleTraits,base::win::VerifierTraits> > F:\src\chromium\src\third_party\libc++\src\include\__vector\vector.h:1248
    #2 0x7ffb54249540 in base::flat_map<base::UnguessableToken,base::win::GenericScopedHandle<base::win::HandleTraits,base::win::VerifierTraits>,std::__Cr::less<void>,std::__Cr::vector<std::__Cr::pair<base::UnguessableToken,base::win::GenericScopedHandle<base::win::HandleTraits,base::win::VerifierTraits> >,std::__Cr::allocator<std::__Cr::pair<base::UnguessableToken,base::win::GenericScopedHandle<base::win::HandleTraits,base::win::VerifierTraits> > > > >::operator[]<base::UnguessableToken> F:\src\chromium\src\base\containers\flat_map.h:315
    #3 0x7ffb54248eec in gl::DCOMPSurfaceRegistry::RegisterDCOMPSurfaceHandle F:\src\chromium\src\ui\gl\dcomp_surface_registry.cc:27
    #4 0x7ffac7e469bf in viz::GpuServiceImpl::RegisterDCOMPSurfaceHandle F:\src\chromium\src\components\viz\service\gl\gpu_service_impl.cc:582
    #5 0x7ffac810fe6e in viz::mojom::GpuServiceStubDispatch::AcceptWithResponder F:\src\chromium\src\out\march\gen\services\viz\privileged\mojom\gl\gpu_service.mojom.cc:3792
    #6 0x7ffac7e64060 in viz::mojom::GpuServiceStub<mojo::RawPtrImplRefTraits<viz::mojom::GpuService> >::AcceptWithResponder F:\src\chromium\src\out\march\gen\services\viz\privileged\mojom\gl\gpu_service.mojom.h:396
    #7 0x7ffbf3c5cae6 in mojo::InterfaceEndpointClient::HandleValidatedMessage F:\src\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:1036
    #8 0x7ffbf3c7cd86 in mojo::MessageDispatcher::Accept F:\src\chromium\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:44
    #9 0x7ffbf3c6428c in mojo::InterfaceEndpointClient::HandleIncomingMessage F:\src\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:747
    #10 0x7ffbf3c90178 in mojo::internal::MultiplexRouter::ProcessIncomingMessage F:\src\chromium\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:1204
    #11 0x7ffbf3c8e303 in mojo::internal::MultiplexRouter::Accept F:\src\chromium\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:790
    #12 0x7ffbf3c7cd86 in mojo::MessageDispatcher::Accept F:\src\chromium\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:44
    #13 0x7ffbf3c3c83d in mojo::Connector::DispatchMessageW F:\src\chromium\src\mojo\public\cpp\bindings\lib\connector.cc:568
    #14 0x7ffbf3c3e8c1 in mojo::Connector::ReadAllAvailableMessages F:\src\chromium\src\mojo\public\cpp\bindings\lib\connector.cc:629
    #15 0x7ffbf3c3e082 in mojo::Connector::OnWatcherHandleReady F:\src\chromium\src\mojo\public\cpp\bindings\lib\connector.cc:420
    #16 0x7ffbf3c41db3 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::*const &)(const char *, unsigned int),mojo::Connector *,const char *const &>,base::internal::BindState<1,1,0,void (mojo::Connector::*)(const char *, unsigned int),base::internal::UnretainedWrapper<mojo::Connector,base::unretained_traits::MayNotDangle,0>,base::internal::UnretainedWrapper<const char,base::unretained_traits::MayNotDangle,0> >,void (unsigned int)>::Run F:\src\chromium\src\base\functional\bind_internal.h:989
    #17 0x7ffbf3c41225 in base::RepeatingCallback<void (unsigned int)>::Run F:\src\chromium\src\base\functional\callback.h:346
    #18 0x7ffbf3c40f3d in base::internal::Invoker<base::internal::FunctorTraits<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),const base::RepeatingCallback<void (unsigned int)> &>,base::internal::BindState<0,1,0,void (*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),base::RepeatingCallback<void (unsigned int)> >,void (unsigned int, const mojo::HandleSignalsState &)>::Run F:\src\chromium\src\base\functional\bind_internal.h:989
    #19 0x7ffbf5b47204 in base::RepeatingCallback<void (unsigned int, const mojo::HandleSignalsState &)>::Run F:\src\chromium\src\base\functional\callback.h:346
    #20 0x7ffbf5b46a6d in mojo::SimpleWatcher::OnHandleReady F:\src\chromium\src\mojo\public\cpp\system\simple_watcher.cc:286
    #21 0x7ffbf5b47694 in mojo::SimpleWatcher::Context::Notify F:\src\chromium\src\mojo\public\cpp\system\simple_watcher.cc:97
    #22 0x7ffbf5b43d8a in mojo::SimpleWatcher::Context::CallNotify F:\src\chromium\src\mojo\public\cpp\system\simple_watcher.cc:61
    #23 0x7ffad0ac3c8f in mojo::core::ipcz_driver::MojoTrap::DispatchEvent F:\src\chromium\src\mojo\core\ipcz_driver\mojo_trap.cc:605
    #24 0x7ffad0abfc67 in mojo::core::ipcz_driver::MojoTrap::DispatchOrQueueEvent F:\src\chromium\src\mojo\core\ipcz_driver\mojo_trap.cc:577
    #25 0x7ffad0ac2e2e in mojo::core::ipcz_driver::MojoTrap::HandleEvent F:\src\chromium\src\mojo\core\ipcz_driver\mojo_trap.cc:459
    #26 0x7ffad0ac2028 in mojo::core::ipcz_driver::MojoTrap::TrapEventHandler F:\src\chromium\src\mojo\core\ipcz_driver\mojo_trap.cc:393
    #27 0x7ffad0baceda in ipcz::TrapEventDispatcher::~TrapEventDispatcher F:\src\chromium\src\third_party\ipcz\src\ipcz\trap_event_dispatcher.cc:12

Thread T47 created by T0 here:
[51916:57220:0310/191007.221:INFO:CONSOLE:122] "[2026-03-10T18:10:07.220Z] elapsed=52956ms active_videos=19 anchors=1 churn=18/18 add=19 remove=0 reload=336 video_err=32 play_err=201 tick_now=25 batch_max_now=1 reload_gap_now=100 tuning=on", source: http://127.0.0.1:8000/dcomp_mojo_race_test_v42.html?video=http://127.0.0.1:8000/red-a500hz.webm (122)
    #0 0x7ffb9a0ddb84 in _asan_wrap_CreateThread+0x64 (F:\src\chromium\src\out\march\clang_rt.asan_dynamic-x86_64.dll+0x18005db84)
    #1 0x7ffb92a98ab6 in base::`anonymous namespace'::CreateThreadInternal F:\src\chromium\src\base\threading\platform_thread_win.cc:178
    #2 0x7ffb92a9884b in base::PlatformThreadBase::CreateWithType F:\src\chromium\src\base\threading\platform_thread_win.cc:301
    #3 0x7ffb929194fd in base::Thread::StartWithOptions F:\src\chromium\src\base\threading\thread.cc:228
    #4 0x7ffb371b10e6 in content::ChildProcess::ChildProcess F:\src\chromium\src\content\child\child_process.cc:152
    #5 0x7ffb370fd5e6 in content::GpuMain F:\src\chromium\src\content\gpu\gpu_main.cc:421
    #6 0x7ffb3ed58f03 in content::RunOtherNamedProcessTypeMain F:\src\chromium\src\content\app\content_main_runner_impl.cc:762
    #7 0x7ffb3ed5c3e0 in content::ContentMainRunnerImpl::Run F:\src\chromium\src\content\app\content_main_runner_impl.cc:1152
    #8 0x7ffb3ed4eba7 in content::RunContentProcess F:\src\chromium\src\content\app\content_main.cc:358
    #9 0x7ffb3ed4f310 in content::ContentMain F:\src\chromium\src\content\app\content_main.cc:371
    #10 0x7ffb5db525ec in ChromeMain F:\src\chromium\src\chrome\app\chrome_main.cc:191
    #11 0x7ff67ab9432e in MainDllLoader::Launch F:\src\chromium\src\chrome\app\main_dll_loader_win.cc:204
    #12 0x7ff67ab92006 in main F:\src\chromium\src\chrome\app\chrome_exe_main_win.cc:351
    #13 0x7ff67add42c3 in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #14 0x7ffc4892e8d6 in BaseThreadInitThunk+0x16 (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #15 0x7ffc49a4c40b in RtlUserThreadStart+0x2b (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18008c40b)

HINT: if you don't care about these errors you may set ASAN_OPTIONS=detect_container_overflow=0.
Or if supported by the container library, pass -D__SANITIZER_DISABLE_CONTAINER_OVERFLOW__ to the compiler to disable  instrumentation.
If you suspect a false positive see also: https://github.com/google/sanitizers/wiki/AddressSanitizerContainerOverflow.
SUMMARY: AddressSanitizer: container-overflow F:\src\chromium\src\third_party\libc++\src\include\__vector\vector.h:1190 in std::__Cr::vector<std::__Cr::pair<base::UnguessableToken,base::win::GenericScopedHandle<base::win::HandleTraits,base::win::VerifierTraits> >,std::__Cr::allocator<std::__Cr::pair<base::UnguessableToken,base::win::GenericScopedHandle<base::win::HandleTraits,base::win::VerifierTraits> > > >::__move_range
Shadow bytes around the buggy address:
  0x120e7da65d80: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x120e7da65e00: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x120e7da65e80: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x120e7da65f00: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x120e7da65f80: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
=>0x120e7da66000: fa fa f7 fa 00 00 00[fc]fc fc 00 00 00 fc fc fc
  0x120e7da66080: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x120e7da66100: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x120e7da66180: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x120e7da66200: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x120e7da66280: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fa
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

==52704==ADDITIONAL INFO

==52704==Note: Please include this section with the ASan report.
Task trace:


Command line: `"F:\src\chromium\src\out\march\chrome.exe" --type=gpu-process --no-sandbox --disable-skia-graphite --use-angle=d3d11 --enable-direct-composition-video-overlays --no-pre-read-main-dll --start-stack-profiler --gpu-preferences=SAAAAAAAAADgAQAEAAAAAAAAAAAAAMAAAQAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAQAAAAAAAAABAAAAAAAAAACAAAAAAAAAAIAAAAAAAAAA== --metrics-shmem-handle=4224,i,16351623397870310290,15405135615145505874,262144 --field-trial-handle=1972,i,77247585974289099,1981378759889770096,262144 --enable-features=MediaFoundationClearPlayback --variations-seed-version --pseudonymization-salt-handle=2120,i,17779908215867826830,2526559194405592156,4 --trace-process-track-uuid=4068719430183723278 --enable-logging=stderr --v=0 --mojo-platform-channel-handle=3956 /prefetch:2`


==52704==END OF ADDITIONAL INFO

==52704==ABORTING

```

Bisects to the implementation of DCOMPSurfaceRegistry:

<https://chromium-review.googlesource.com/c/chromium/src/+/2993378>

Type of crash: GPU, windows only.

Reporter credit: soiax

## Attachments

- [patch.diff](attachments/patch.diff) (text/x-diff, 3.2 KB)
- [red-a500hz.webm](attachments/red-a500hz.webm) (video/webm, 128.3 KB)
- [dcomp_race_test_v44.html](attachments/dcomp_race_test_v44.html) (text/html, 23.9 KB)
- [asanuaf.txt](attachments/asanuaf.txt) (text/plain, 21.6 KB)
- [asanheapbof.txt](attachments/asanheapbof.txt) (text/plain, 22.0 KB)
- [asancont.txt](attachments/asancont.txt) (text/plain, 20.3 KB)

## Timeline

### ke...@gmail.com (2026-03-17)

Forgot to mention: "--no-sandbox" isn’t technically required, but for some reason in my ASAN build it causes the MediaFoundation and DCOMP paths to fail early, before any racing even occurs.

### ts...@google.com (2026-03-18)

Given the patch and the flaky nature of the crash, did not reproduce.  Assigning per attached symbolized ASAN trace.

### ts...@google.com (2026-03-18)

Over to Ken to re-assign as appropriate. 

### ts...@google.com (2026-03-18)

Setting provisional found-in and Severity medium as it is flaky even with a patch.

### ts...@google.com (2026-03-18)

Looks to be win-specific per BUILD.gn file

### ch...@google.com (2026-03-19)

Setting milestone because of s2 severity.

### kb...@chromium.org (2026-03-21)

Jon, since this code path is triggerable under Viz would you be able to find someone on the Viz team to take this? I would ask our colleagues at Microsoft to do so since they originally wrote this code but they may not have the same timelines as the Chrome team. Thanks.

### am...@google.com (2026-03-21)

From the bug description:

> RegisterDCOMPSurfaceHandle and UnregisterDCOMPSurfaceHandle are called on the GPU IO thread via GpuServiceImpl. While TakeDCOMPSurfaceHandle is called on the GPU main scheduler thread via DCOMPTexture.

If this is the case, we would need to mutex protect access to `surface_handle_map_`. Am surprised this wasn't caught by TSAN, though. Maybe we're missing tests that would trigger TSAN failures.

### ke...@gmail.com (2026-03-24)

> Am surprised this wasn't caught by TSAN, though. Maybe we're missing tests that would trigger TSAN failures.

Because this is in a windows only code, TSAN is not working on windows.

### jo...@chromium.org (2026-03-25)

Is there a repro for this without adding sleeps to `ui\gl\dcomp_surface_registry.cc` and without enabling `MediaFoundationClearPlayback`?

### ke...@gmail.com (2026-03-25)

Not really.

Delay is needed because the race is tight, and the whole mediafoundation pipeline crashes all the time before reaching this code.

MediaFoundationClearPlayback is needed, because i don't have a DRM license server.

But both the encrypted and clear codepaths end in the same place.

### ke...@gmail.com (2026-03-31)

> If this is the case, we would need to mutex protect access to surface\_handle\_map\_.

Nearby `ui/gl` code already protects cross-thread/global state with `base::Lock`/`base::AutoLock`
and `GUARDED_BY`, for example in [direct\_composition\_support.cc#L52](https://source.chromium.org/chromium/chromium/src/+/main:ui/gl/direct_composition_support.cc;l=52) and
[gl\_display\_manager.h#L150](https://source.chromium.org/chromium/chromium/src/+/main:ui/gl/gl_display_manager.h;l=150).

### dx...@google.com (2026-04-09)

Project: chromium/src  

Branch:  main  

Author:  Jonathan Ross [jonross@chromium.org](mailto:jonross@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7737061>

gl: Make DCOMPSurfaceRegistry thread-safe

---


Expand for full commit details
```
     
    DCOMPSurfaceRegistry is accessed from both the GPU IO thread (via 
    GpuServiceImpl) and the GPU main scheduler thread (via DCOMPTexture). 
    The underlying base::flat_map is not thread-safe, leading to potential 
    container corruption and crashes (UAF, BOf) during concurrent access. 
     
    This CL adds a base::Lock to protect all accesses to the map and 
    includes a new multi-threaded stress test to verify the fix. 
     
    Bug: 493315759 
    Change-Id: Ibb7ef5e602f222410fde06a61fb3f5e571e7a70f 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7737061 
    Reviewed-by: Sunny Sachanandani <sunnyps@chromium.org> 
    Commit-Queue: Jonathan Ross <jonross@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1611867}

```

---

Files:

- M `ui/gl/BUILD.gn`
- M `ui/gl/dcomp_surface_registry.cc`
- M `ui/gl/dcomp_surface_registry.h`
- A `ui/gl/dcomp_surface_registry_unittest.cc`

---

Hash: [be87466afecb1bbcb29ad8b87bd88a6ba6d0dda0](https://chromiumdash.appspot.com/commit/be87466afecb1bbcb29ad8b87bd88a6ba6d0dda0)  

Date: Thu Apr 9 00:15:45 2026


---

### dx...@google.com (2026-04-10)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Jonathan Ross [jonross@chromium.org](mailto:jonross@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7748991>

[M146] gl: Make DCOMPSurfaceRegistry thread-safe

---


Expand for full commit details
```
     
    Original change's description: 
    > gl: Make DCOMPSurfaceRegistry thread-safe 
    > 
    > DCOMPSurfaceRegistry is accessed from both the GPU IO thread (via 
    > GpuServiceImpl) and the GPU main scheduler thread (via DCOMPTexture). 
    > The underlying base::flat_map is not thread-safe, leading to potential 
    > container corruption and crashes (UAF, BOf) during concurrent access. 
    > 
    > This CL adds a base::Lock to protect all accesses to the map and 
    > includes a new multi-threaded stress test to verify the fix. 
    > 
    > Bug: 493315759 
    > Change-Id: Ibb7ef5e602f222410fde06a61fb3f5e571e7a70f 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7737061 
    > Reviewed-by: Sunny Sachanandani <sunnyps@chromium.org> 
    > Commit-Queue: Jonathan Ross <jonross@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1611867} 
     
    (cherry picked from commit be87466afecb1bbcb29ad8b87bd88a6ba6d0dda0) 
     
    Bug: 501314752,493315759 
    Change-Id: Ibb7ef5e602f222410fde06a61fb3f5e571e7a70f 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7748991 
    Reviewed-by: Jonathan Ross <jonross@chromium.org> 
    Auto-Submit: Chrome Cherry Picker <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7680@{#3916} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `ui/gl/BUILD.gn`
- M `ui/gl/dcomp_surface_registry.cc`
- M `ui/gl/dcomp_surface_registry.h`
- A `ui/gl/dcomp_surface_registry_unittest.cc`

---

Hash: [a88077daa0c4f106f08930d4ac515279ceae4d94](https://chromiumdash.appspot.com/commit/a88077daa0c4f106f08930d4ac515279ceae4d94)  

Date: Fri Apr 10 21:08:59 2026


---

### sp...@google.com (2026-07-10)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided to issue a reward of
**$4000.00** for your report. Congratulations!

Rationale for this decision:

Mildly mitigated sandbox with bisect.

Important payment guidance:

- **Bugcrowd**: This payment will be issued by Bugcrowd. You will receive an
  email from Bugcrowd in the next 24 hours which contains a submission you
  must claim to be rewarded.
  
  If you do not receive an email from Bugcrowd, please check your spam folder
  and then reach out to us via a comment here. For issues related to Bugcrowd
  itself, please contact them via <https://bugcrowd.com/support>.

Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot

P.S. One other thing we'd like to mention:

- Please do NOT publicly disclose details until a fix has been released to all
  our users. Early public disclosure may cancel the provisional reward. Also,
  please be considerate about disclosure when the bug affects a core library
  that may be used by other products. Please do NOT share this information
  with third parties who are not directly involved in fixing the bug. Doing so
  may cancel the provisional reward. Please be honest if you have already
  disclosed anything publicly or to third parties. Lastly, we understand that
  some of you are not interested in money. We offer the option to donate your
  reward to an eligible charity. Any rewards that are unclaimed after 12
  months will be donated to a charity of our choosing.

Please contact [security-vrp@chromium.org](mailto:security-vrp@chromium.org) with any questions.

### ch...@google.com (2026-07-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/493315759)*
