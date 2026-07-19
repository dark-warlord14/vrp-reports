# Use-After-Free in DCOMPSurfaceRegistry due to data race on unsynchronized flat_map access in GPU Process

| Field | Value |
|-------|-------|
| **Issue ID** | [490251701](https://issues.chromium.org/issues/490251701) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>Video |
| **Platforms** | Windows |
| **Reporter** | se...@gmail.com |
| **Assignee** | xh...@chromium.org |
| **Created** | 2026-03-06 |
| **Bounty** | $11,000.00 |

## Description

# Data race in DCOMPSurfaceRegistry leads to GPU process memory corruption via concurrent flat\_map access

## Summary

The `gl::DCOMPSurfaceRegistry` singleton in the GPU process stores Windows Direct Composition surface handles in a `base::flat_map` that is accessed concurrently from two different threads without any synchronization. The GPU IO thread executes `RegisterDCOMPSurfaceHandle` and `UnregisterDCOMPSurfaceHandle` through `GpuServiceImpl` Mojo handlers, while the GPU main thread executes `TakeDCOMPSurfaceHandle` through `DCOMPTexture` Mojo handlers. Since `base::flat_map` is backed by a sorted `std::vector` that is not thread-safe, concurrent insertion on the IO thread can trigger vector reallocation that frees the underlying buffer while the main thread still holds an iterator into it, resulting in a heap-use-after-free in the GPU process. A compromised renderer can trigger this race by initiating multiple MediaFoundation video playback sessions, causing interleaved Register and Take operations on the shared map.

Affected System: Windows. DCOMP (DirectComposition) is a Windows-only API.
GPU requirement: Any GPU with Direct3D 11 and DirectComposition support. Tested with Intel Arc A750. Most modern discrete and integrated GPUs on Windows 10+ satisfy this requirement.

## Bisect

Introducing Commit: `7d5c2028a61829c457e4a0e5eeab2655e2336dca`

- Date: `Fri Jul 02 09:33:32 2021`
- Author: `frankli@microsoft.com`
- Review: `https://chromium-review.googlesource.com/c/chromium/src/+/2993378`

## Root Cause

The `gl::DCOMPSurfaceRegistry` class is a GPU process singleton designed to map `base::UnguessableToken` values to Windows Direct Composition surface handles. Its internal storage is a `base::flat_map<base::UnguessableToken, base::win::ScopedHandle>`, and none of its three public methods carry any form of locking, sequence checking, or thread-safety annotation.

```
// ui/gl/dcomp_surface_registry.h
class GL_EXPORT DCOMPSurfaceRegistry {
 public:
  static DCOMPSurfaceRegistry* GetInstance();

  base::UnguessableToken RegisterDCOMPSurfaceHandle(
      base::win::ScopedHandle surface);

  void UnregisterDCOMPSurfaceHandle(const base::UnguessableToken& token);

  base::win::ScopedHandle TakeDCOMPSurfaceHandle(
      const base::UnguessableToken& token);

 private:
  friend base::NoDestructor<DCOMPSurfaceRegistry>;

  DCOMPSurfaceRegistry();
  ~DCOMPSurfaceRegistry();

  base::flat_map<base::UnguessableToken, base::win::ScopedHandle>
      surface_handle_map_;
};

```

The class header contains no `SEQUENCE_CHECKER`, no `base::Lock`, and no `GUARDED_BY` annotation on `surface_handle_map_`. This is the complete implementation of the three methods that operate on the map:

```
// ui/gl/dcomp_surface_registry.cc
base::UnguessableToken DCOMPSurfaceRegistry::RegisterDCOMPSurfaceHandle(
    base::win::ScopedHandle surface) {
  base::UnguessableToken token = base::UnguessableToken::Create();
  surface_handle_map_[token] = std::move(surface);  // unprotected write
  return token;
}

void DCOMPSurfaceRegistry::UnregisterDCOMPSurfaceHandle(
    const base::UnguessableToken& token) {
  surface_handle_map_.erase(token);  // unprotected write
}

base::win::ScopedHandle DCOMPSurfaceRegistry::TakeDCOMPSurfaceHandle(
    const base::UnguessableToken& token) {
  auto surface_iter = surface_handle_map_.find(token);  // unprotected read
  if (surface_iter != surface_handle_map_.end()) {
    auto surface_handle = std::move(surface_iter->second);  // use iterator
    surface_handle_map_.erase(surface_iter);
    return surface_handle;
  }
  return base::win::ScopedHandle();
}

```

The threading conflict arises because the callers of these methods run on two different threads within the GPU process.

`GpuServiceImpl` binds its Mojo receiver to the IO thread. When the browser process forwards a `RegisterDCOMPSurfaceHandle` or `UnregisterDCOMPSurfaceHandle` call from the MediaFoundation utility process, the handler executes on the GPU IO thread:

```
// components/viz/service/gl/gpu_service_impl.cc
void GpuServiceImpl::Bind(
    mojo::PendingReceiver<mojom::GpuService> pending_receiver) {
  if (main_runner_->BelongsToCurrentThread()) {
    bind_task_tracker_.PostTask(
        io_runner_.get(), FROM_HERE,
        base::BindOnce(&GpuServiceImpl::Bind, base::Unretained(this),
                       std::move(pending_receiver)));
    return;
  }
  receiver_.Bind(std::move(pending_receiver));  // bound to io_runner_
}

void GpuServiceImpl::RegisterDCOMPSurfaceHandle(
    mojo::PlatformHandle surface_handle,
    RegisterDCOMPSurfaceHandleCallback callback) {
  // Runs on IO thread
  base::UnguessableToken token =
      gl::DCOMPSurfaceRegistry::GetInstance()->RegisterDCOMPSurfaceHandle(
          surface_handle.TakeHandle());
  std::move(callback).Run(token);
}

```

Meanwhile, `DCOMPTexture` binds its Mojo receiver to a `SchedulerTaskRunner`, which dispatches tasks on the GPU main thread. When the renderer process sends a `SetDCOMPSurfaceHandle` message, the handler calls `TakeDCOMPSurfaceHandle` on the GPU main thread:

```
// gpu/ipc/service/dcomp_texture_win.cc
DCOMPTexture::DCOMPTexture(GpuChannel* channel, int32_t route_id, ...) {
  auto runner = base::MakeRefCounted<SchedulerTaskRunner>(
      *channel_->scheduler(), sequence_);
  receiver_.Bind(std::move(receiver), runner);  // bound to SchedulerTaskRunner
}

void DCOMPTexture::SetDCOMPSurfaceHandle(
    const base::UnguessableToken& token,
    SetDCOMPSurfaceHandleCallback callback) {
  // Runs on GPU main thread (SchedulerTaskRunner)
  base::win::ScopedHandle surface_handle =
      gl::DCOMPSurfaceRegistry::GetInstance()->TakeDCOMPSurfaceHandle(token);
  ...
}

```

The race proceeds as follows. The GPU main thread calls `TakeDCOMPSurfaceHandle`, which performs `surface_handle_map_.find(token)` and obtains a valid iterator pointing into the underlying vector buffer. Before the method can dereference the iterator with `std::move(surface_iter->second)`, the GPU IO thread calls `RegisterDCOMPSurfaceHandle`, which inserts a new entry into the flat\_map via `surface_handle_map_[token] = std::move(surface)`. If the insertion exceeds the vector capacity, `std::vector::emplace` allocates a new buffer and frees the old one. When the main thread resumes and accesses the iterator, it dereferences a pointer into the freed buffer, producing a use-after-free or container-overflow.

The normal trigger path for this race is MediaFoundation video playback on Windows. When a renderer initiates playback, the MediaFoundation renderer running in a utility process creates a DCOMP surface and sends the handle to the browser, which forwards it to the GPU process via `GpuServiceImpl::RegisterDCOMPSurfaceHandle` on the IO thread. Simultaneously, the renderer creates a `DCOMPTexture` and calls `SetDCOMPSurfaceHandle` on the GPU main thread to retrieve the registered handle. Multiple concurrent video sessions create overlapping Register and Take operations that collide on the shared map.

## Reproduce

The PoC uses an HTML page that creates and destroys multiple video elements to produce interleaved Register and Take calls to `DCOMPSurfaceRegistry`. Two source modifications are required: a one-line renderer patch that forces the MediaFoundation renderer path for clear content (modeling a compromised renderer), and `Sleep(2000ms)` instrumentation in the GPU process to widen the race window for deterministic demonstration. No command-line feature flags are needed.

Tested on Chromium commit `f2502f2d5c51fc78ed59f48827d69426d7193eed`.

Prerequisites: a Windows system with a GPU that supports Direct3D 11 and Direct Composition (the PoC was tested with an Intel Arc A750).

Build:

```
git apply patch.diff
autoninja -C out/asan chrome

```

The ASAN build configuration should include:

```
is_asan = true
is_debug = false
dcheck_always_on = false

```

Place `poc.html` and `bear-vp9.webm` in the same directory, then serve it via HTTP and launch the ASAN build.

```
$ ls
bear-vp9.webm
poc.html
$ python3 -m http.server

```

Run chromium:

```
out/asan/chrome.exe --user-data-dir=/tmp/poc --enable-logging=stderr http://127.0.0.1:8000/poc.html > /tmp/poc-output.txt 2>&1

cat /tmp/poc-output.txt

```
### ASAN output

The GPU process crashes with a heap-use-after-free on the `surface_handle_map_` flat\_map's underlying vector buffer. Thread T0 (GPU main thread) reads through a stale iterator into freed memory, while thread T14 (GPU IO thread) has freed and reallocated the vector buffer via `RegisterDCOMPSurfaceHandle`. The shadow byte `[fd]` (Freed heap region) confirms the access is to genuinely freed memory.

```
=================================================================
==68036==ERROR: AddressSanitizer: heap-use-after-free on address 0x11c2c6937a00 at pc 0x7ffeb8215486 bp 0x00b2a69fe140
 sp 0x00b2a69fe188
READ of size 8 at 0x11c2c6937a00 thread T0
==68036==*** WARNING: Failed to initialize DbgHelp!              ***
==68036==*** Most likely this means that the app is already      ***
==68036==*** using DbgHelp, possibly with incompatible flags.    ***
==68036==*** Due to technical reasons, symbolization might crash ***
==68036==*** or produce wrong results.                           ***
    #0 0x7ffeb8215485 in base::win::GenericScopedHandle<base::win::HandleTraits,base::win::DummyVerifierTraits>::Gener
icScopedHandle C:\Users\test\Desktop\src\chromium\src\base\win\scoped_handle.h:65
    #1 0x7ffed27d0ca0 in gl::DCOMPSurfaceRegistry::TakeDCOMPSurfaceHandle C:\Users\test\Desktop\src\chromium\src\ui\g
l\dcomp_surface_registry.cc:45
    #2 0x7ffed63a3db4 in gpu::DCOMPTexture::SetDCOMPSurfaceHandle C:\Users\test\Desktop\src\chromium\src\gpu\ipc\serv
ice\dcomp_texture_win.cc:228
    #3 0x7ffeb86fbd2b in gpu::mojom::DCOMPTextureStubDispatch::AcceptWithResponder C:\Users\test\Desktop\src\chromium
\src\out\asan\gen\gpu\ipc\common\gpu_channel.mojom.cc:8256
    #4 0x7ffed63a5d6c in gpu::mojom::DCOMPTextureStub<mojo::RawPtrImplRefTraits<gpu::mojom::DCOMPTexture> >::AcceptWit
hResponder C:\Users\test\Desktop\src\chromium\src\out\asan\gen\gpu\ipc\common\gpu_channel.mojom.h:824
    #5 0x7ffeca70bbad in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\Users\test\Desktop\src\chromium\src
\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:1036
    #6 0x7ffecffa482d in mojo::MessageDispatcher::Accept C:\Users\test\Desktop\src\chromium\src\mojo\public\cpp\bindi
ngs\lib\message_dispatcher.cc:44
    #7 0x7ffeca7122ee in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\Users\test\Desktop\src\chromium\src\
mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:747
    #8 0x7ffed110b256 in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread C:\Users\test\Desktop\src\chro
mium\src\ipc\ipc_mojo_bootstrap.cc:1199
    #9 0x7ffed110d791 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupContro
ller::*&&)(mojo::Message, IPC::`anonymous namespace'::ScopedUrgentMessageNotification),IPC::ChannelAssociatedGroupCont
roller *&&,mojo::Message &&,IPC::`anonymous namespace'::ScopedUrgentMessageNotification &&>,base::internal::BindState<
1,1,0,void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::`anonymous namespace'::ScopedUrgentMessageNo
tification),scoped_refptr<IPC::ChannelAssociatedGroupController>,mojo::Message,IPC::`anonymous namespace'::ScopedUrgen
tMessageNotification>,void ()>::RunOnce C:\Users\test\Desktop\src\chromium\src\base\functional\bind_internal.h:982
    #10 0x7ffeb9c9e222 in gpu::SchedulerTaskRunner::RunTask C:\Users\test\Desktop\src\chromium\src\gpu\command_buffer
\service\scheduler_task_runner.cc:76
    #11 0x7ffeb9c9e5f3 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerTaskRunner::*&&)(b
ase::OnceCallback<void ()>),gpu::SchedulerTaskRunner *&&,base::OnceCallback<void ()> &&>,base::internal::BindState<1,1
,0,void (gpu::SchedulerTaskRunner::*)(base::OnceCallback<void ()>),scoped_refptr<gpu::SchedulerTaskRunner>,base::OnceC
allback<void ()> >,void ()>::RunOnce C:\Users\test\Desktop\src\chromium\src\base\functional\bind_internal.h:982
    #12 0x7ffeb9c93b32 in gpu::Scheduler::ExecuteSequence C:\Users\test\Desktop\src\chromium\src\gpu\command_buffer\s
ervice\scheduler.cc:707
    #13 0x7ffeb9c91c60 in gpu::Scheduler::RunNextTask C:\Users\test\Desktop\src\chromium\src\gpu\command_buffer\servi
ce\scheduler.cc:625
    #14 0x7ffeb9c967e4 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(),gpu::Sche
duler *>,base::internal::BindState<1,1,0,void (gpu::Scheduler::*)(),base::internal::UnretainedWrapper<gpu::Scheduler,b
ase::unretained_traits::MayNotDangle,0> >,void ()>::RunOnce C:\Users\test\Desktop\src\chromium\src\base\functional\bi
nd_internal.h:982
    #15 0x7ffeca8f0b98 in base::TaskAnnotator::RunTaskImpl C:\Users\test\Desktop\src\chromium\src\base\task\common\ta
sk_annotator.cc:229
    #16 0x7ffed004c6d1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\Users\1
2828\Desktop\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:475
    #17 0x7ffed004b533 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\Users\test
\Desktop\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:346
    #18 0x7ffed0093dd7 in base::MessagePumpDefault::Run C:\Users\test\Desktop\src\chromium\src\base\message_loop\mess
age_pump_default.cc:42
    #19 0x7ffed004e41f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\Users\test\De
sktop\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:650
    #20 0x7ffeca963c0c in base::RunLoop::Run C:\Users\test\Desktop\src\chromium\src\base\run_loop.cc:135
    #21 0x7ffecde943b3 in content::GpuMain C:\Users\test\Desktop\src\chromium\src\content\gpu\gpu_main.cc:479
    #22 0x7ffec726deff in content::RunOtherNamedProcessTypeMain C:\Users\test\Desktop\src\chromium\src\content\app\co
ntent_main_runner_impl.cc:762
    #23 0x7ffec727066b in content::ContentMainRunnerImpl::Run C:\Users\test\Desktop\src\chromium\src\content\app\cont
ent_main_runner_impl.cc:1152
    #24 0x7ffec726445f in content::RunContentProcess C:\Users\test\Desktop\src\chromium\src\content\app\content_main.
cc:358
    #25 0x7ffec7264c02 in content::ContentMain C:\Users\test\Desktop\src\chromium\src\content\app\content_main.cc:371
    #26 0x7ffeb7092b06 in ChromeMain C:\Users\test\Desktop\src\chromium\src\chrome\app\chrome_main.cc:191
    #27 0x7ff649534807 in MainDllLoader::Launch C:\Users\test\Desktop\src\chromium\src\chrome\app\main_dll_loader_win
.cc:204
    #28 0x7ff649532074 in main C:\Users\test\Desktop\src\chromium\src\chrome\app\chrome_exe_main_win.cc:351
    #29 0x7ff649a2dcdf in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:2
88
    #30 0x7fff80dc7613 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017613)
    #31 0x7fff825e26a0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526a0)

0x11c2c6937a00 is located 16 bytes inside of 24-byte region [0x11c2c69379f0,0x11c2c6937a08)
freed by thread T14 here:
    #0 0x7fff1e3cf036 in operator delete+0x96 (C:\Users\test\Desktop\src\chromium\src\out\asan\clang_rt.asan_dynamic-
x86_64.dll+0x5f036)
    #1 0x7ffed27d1212 in std::__Cr::vector<std::__Cr::pair<base::UnguessableToken,base::win::GenericScopedHandle<base:
:win::HandleTraits,base::win::DummyVerifierTraits> >,std::__Cr::allocator<std::__Cr::pair<base::UnguessableToken,base:
:win::GenericScopedHandle<base::win::HandleTraits,base::win::DummyVerifierTraits> > > >::emplace<const base::Unguessab
leToken &,base::win::GenericScopedHandle<base::win::HandleTraits,base::win::DummyVerifierTraits> > C:\Users\test\Desk
top\src\chromium\src\third_party\libc++\src\include\__vector\vector.h:1251
    #2 0x7ffed27d071e in base::flat_map<base::UnguessableToken,base::win::GenericScopedHandle<base::win::HandleTraits,
base::win::DummyVerifierTraits>,std::__Cr::less<void>,std::__Cr::vector<std::__Cr::pair<base::UnguessableToken,base::w
in::GenericScopedHandle<base::win::HandleTraits,base::win::DummyVerifierTraits> >,std::__Cr::allocator<std::__Cr::pair
<base::UnguessableToken,base::win::GenericScopedHandle<base::win::HandleTraits,base::win::DummyVerifierTraits> > > > >
::operator[]<base::UnguessableToken> C:\Users\test\Desktop\src\chromium\src\base\containers\flat_map.h:315
    #3 0x7ffed27d052b in gl::DCOMPSurfaceRegistry::RegisterDCOMPSurfaceHandle C:\Users\test\Desktop\src\chromium\src\
ui\gl\dcomp_surface_registry.cc:26
    #4 0x7ffecde9f5b5 in viz::GpuServiceImpl::RegisterDCOMPSurfaceHandle C:\Users\test\Desktop\src\chromium\src\compo
nents\viz\service\gl\gpu_service_impl.cc:582
    #5 0x7ffebbe1497e in viz::mojom::GpuServiceStubDispatch::AcceptWithResponder C:\Users\test\Desktop\src\chromium\s
rc\out\asan\gen\services\viz\privileged\mojom\gl\gpu_service.mojom.cc:3792
    #6 0x7ffecdeb2020 in viz::mojom::GpuServiceStub<mojo::RawPtrImplRefTraits<viz::mojom::GpuService> >::AcceptWithRes
ponder C:\Users\test\Desktop\src\chromium\src\out\asan\gen\services\viz\privileged\mojom\gl\gpu_service.mojom.h:396
    #7 0x7ffeca70bbad in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\Users\test\Desktop\src\chromium\src
\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:1036
    #8 0x7ffecffa482d in mojo::MessageDispatcher::Accept C:\Users\test\Desktop\src\chromium\src\mojo\public\cpp\bindi
ngs\lib\message_dispatcher.cc:44
    #9 0x7ffeca7122ee in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\Users\test\Desktop\src\chromium\src\
mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:747
    #10 0x7ffeca6f44a0 in mojo::internal::MultiplexRouter::ProcessIncomingMessage C:\Users\test\Desktop\src\chromium\
src\mojo\public\cpp\bindings\lib\multiplex_router.cc:1204
    #11 0x7ffeca6f2a0f in mojo::internal::MultiplexRouter::Accept C:\Users\test\Desktop\src\chromium\src\mojo\public\
cpp\bindings\lib\multiplex_router.cc:790
    #12 0x7ffecffa482d in mojo::MessageDispatcher::Accept C:\Users\test\Desktop\src\chromium\src\mojo\public\cpp\bind
ings\lib\message_dispatcher.cc:44
    #13 0x7ffeca726ff9 in mojo::Connector::DispatchMessageW C:\Users\test\Desktop\src\chromium\src\mojo\public\cpp\bi
ndings\lib\connector.cc:568
    #14 0x7ffeca728858 in mojo::Connector::ReadAllAvailableMessages C:\Users\test\Desktop\src\chromium\src\mojo\publi
c\cpp\bindings\lib\connector.cc:629
    #15 0x7ffeca7282c7 in mojo::Connector::OnWatcherHandleReady C:\Users\test\Desktop\src\chromium\src\mojo\public\cp
p\bindings\lib\connector.cc:420
    #16 0x7ffeca72a1af in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::*const &)(const
 char *, unsigned int),mojo::Connector *,const char *const &>,base::internal::BindState<1,1,0,void (mojo::Connector::*
)(const char *, unsigned int),base::internal::UnretainedWrapper<mojo::Connector,base::unretained_traits::MayNotDangle,
0>,base::internal::UnretainedWrapper<const char,base::unretained_traits::MayNotDangle,0> >,void (unsigned int)>::Run C
:\Users\test\Desktop\src\chromium\src\base\functional\bind_internal.h:989
    #17 0x7ffebb57810c in base::RepeatingCallback<void (unsigned int)>::Run C:\Users\test\Desktop\src\chromium\src\ba
se\functional\callback.h:346
    #18 0x7ffebb577efc in base::internal::Invoker<base::internal::FunctorTraits<void (*const &)(const base::RepeatingC
allback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),const base::RepeatingCallback<void (un
signed int)> &>,base::internal::BindState<0,1,0,void (*)(const base::RepeatingCallback<void (unsigned int)> &, unsigne
d int, const mojo::HandleSignalsState &),base::RepeatingCallback<void (unsigned int)> >,void (unsigned int, const mojo
::HandleSignalsState &)>::Run C:\Users\test\Desktop\src\chromium\src\base\functional\bind_internal.h:989
    #19 0x7ffecace161b in base::RepeatingCallback<void (unsigned int, const mojo::HandleSignalsState &)>::Run C:\Users
\test\Desktop\src\chromium\src\base\functional\callback.h:346
    #20 0x7ffecace0f24 in mojo::SimpleWatcher::OnHandleReady C:\Users\test\Desktop\src\chromium\src\mojo\public\cpp\s
ystem\simple_watcher.cc:286
    #21 0x7ffecace19da in mojo::SimpleWatcher::Context::Notify C:\Users\test\Desktop\src\chromium\src\mojo\public\cpp
\system\simple_watcher.cc:97
    #22 0x7ffecacde53a in mojo::SimpleWatcher::Context::CallNotify C:\Users\test\Desktop\src\chromium\src\mojo\public
\cpp\system\simple_watcher.cc:61
    #23 0x7ffeb773661f in mojo::core::ipcz_driver::MojoTrap::DispatchOrQueueEvent C:\Users\test\Desktop\src\chromium\
src\mojo\core\ipcz_driver\mojo_trap.cc:577
    #24 0x7ffeb7738d03 in mojo::core::ipcz_driver::MojoTrap::HandleEvent C:\Users\test\Desktop\src\chromium\src\mojo\
core\ipcz_driver\mojo_trap.cc:459
    #25 0x7ffeb77ec34a in ipcz::TrapEventDispatcher::~TrapEventDispatcher C:\Users\test\Desktop\src\chromium\src\thir
d_party\ipcz\src\ipcz\trap_event_dispatcher.cc:12
    #26 0x7ffeb77d1fdb in ipcz::Router::AcceptInboundParcel C:\Users\test\Desktop\src\chromium\src\third_party\ipcz\s
rc\ipcz\router.cc:272
    #27 0x7ffeb779d377 in ipcz::NodeLink::AcceptCompleteParcel C:\Users\test\Desktop\src\chromium\src\third_party\ipc
z\src\ipcz\node_link.cc:1082

previously allocated by thread T14 here:
    #0 0x7fff1e3ce46f in operator new+0x8f (C:\Users\test\Desktop\src\chromium\src\out\asan\clang_rt.asan_dynamic-x86
_64.dll+0x5e46f)
    #1 0x7ffed27d10b6 in std::__Cr::vector<std::__Cr::pair<base::UnguessableToken,base::win::GenericScopedHandle<base:
:win::HandleTraits,base::win::DummyVerifierTraits> >,std::__Cr::allocator<std::__Cr::pair<base::UnguessableToken,base:
:win::GenericScopedHandle<base::win::HandleTraits,base::win::DummyVerifierTraits> > > >::emplace<const base::Unguessab
leToken &,base::win::GenericScopedHandle<base::win::HandleTraits,base::win::DummyVerifierTraits> > C:\Users\test\Desk
top\src\chromium\src\third_party\libc++\src\include\__vector\vector.h:1248
    #2 0x7ffed27d071e in base::flat_map<base::UnguessableToken,base::win::GenericScopedHandle<base::win::HandleTraits,
base::win::DummyVerifierTraits>,std::__Cr::less<void>,std::__Cr::vector<std::__Cr::pair<base::UnguessableToken,base::w
in::GenericScopedHandle<base::win::HandleTraits,base::win::DummyVerifierTraits> >,std::__Cr::allocator<std::__Cr::pair
<base::UnguessableToken,base::win::GenericScopedHandle<base::win::HandleTraits,base::win::DummyVerifierTraits> > > > >
::operator[]<base::UnguessableToken> C:\Users\test\Desktop\src\chromium\src\base\containers\flat_map.h:315
    #3 0x7ffed27d052b in gl::DCOMPSurfaceRegistry::RegisterDCOMPSurfaceHandle C:\Users\test\Desktop\src\chromium\src\
ui\gl\dcomp_surface_registry.cc:26
    #4 0x7ffecde9f5b5 in viz::GpuServiceImpl::RegisterDCOMPSurfaceHandle C:\Users\test\Desktop\src\chromium\src\compo
nents\viz\service\gl\gpu_service_impl.cc:582
    #5 0x7ffebbe1497e in viz::mojom::GpuServiceStubDispatch::AcceptWithResponder C:\Users\test\Desktop\src\chromium\s
rc\out\asan\gen\services\viz\privileged\mojom\gl\gpu_service.mojom.cc:3792
    #6 0x7ffecdeb2020 in viz::mojom::GpuServiceStub<mojo::RawPtrImplRefTraits<viz::mojom::GpuService> >::AcceptWithRes
ponder C:\Users\test\Desktop\src\chromium\src\out\asan\gen\services\viz\privileged\mojom\gl\gpu_service.mojom.h:396
    #7 0x7ffeca70bbad in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\Users\test\Desktop\src\chromium\src
\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:1036
    #8 0x7ffecffa482d in mojo::MessageDispatcher::Accept C:\Users\test\Desktop\src\chromium\src\mojo\public\cpp\bindi
ngs\lib\message_dispatcher.cc:44
    #9 0x7ffeca7122ee in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\Users\test\Desktop\src\chromium\src\
mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:747
    #10 0x7ffeca6f44a0 in mojo::internal::MultiplexRouter::ProcessIncomingMessage C:\Users\test\Desktop\src\chromium\
src\mojo\public\cpp\bindings\lib\multiplex_router.cc:1204
    #11 0x7ffeca6f2a0f in mojo::internal::MultiplexRouter::Accept C:\Users\test\Desktop\src\chromium\src\mojo\public\
cpp\bindings\lib\multiplex_router.cc:790
    #12 0x7ffecffa482d in mojo::MessageDispatcher::Accept C:\Users\test\Desktop\src\chromium\src\mojo\public\cpp\bind
ings\lib\message_dispatcher.cc:44
    #13 0x7ffeca726ff9 in mojo::Connector::DispatchMessageW C:\Users\test\Desktop\src\chromium\src\mojo\public\cpp\bi
ndings\lib\connector.cc:568
    #14 0x7ffeca728858 in mojo::Connector::ReadAllAvailableMessages C:\Users\test\Desktop\src\chromium\src\mojo\publi
c\cpp\bindings\lib\connector.cc:629
    #15 0x7ffeca7282c7 in mojo::Connector::OnWatcherHandleReady C:\Users\test\Desktop\src\chromium\src\mojo\public\cp
p\bindings\lib\connector.cc:420
    #16 0x7ffeca72a1af in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::*const &)(const
 char *, unsigned int),mojo::Connector *,const char *const &>,base::internal::BindState<1,1,0,void (mojo::Connector::*
)(const char *, unsigned int),base::internal::UnretainedWrapper<mojo::Connector,base::unretained_traits::MayNotDangle,
0>,base::internal::UnretainedWrapper<const char,base::unretained_traits::MayNotDangle,0> >,void (unsigned int)>::Run C
:\Users\test\Desktop\src\chromium\src\base\functional\bind_internal.h:989
    #17 0x7ffebb57810c in base::RepeatingCallback<void (unsigned int)>::Run C:\Users\test\Desktop\src\chromium\src\ba
se\functional\callback.h:346
    #18 0x7ffebb577efc in base::internal::Invoker<base::internal::FunctorTraits<void (*const &)(const base::RepeatingC
allback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),const base::RepeatingCallback<void (un
signed int)> &>,base::internal::BindState<0,1,0,void (*)(const base::RepeatingCallback<void (unsigned int)> &, unsigne
d int, const mojo::HandleSignalsState &),base::RepeatingCallback<void (unsigned int)> >,void (unsigned int, const mojo
::HandleSignalsState &)>::Run C:\Users\test\Desktop\src\chromium\src\base\functional\bind_internal.h:989
    #19 0x7ffecace161b in base::RepeatingCallback<void (unsigned int, const mojo::HandleSignalsState &)>::Run C:\Users
\test\Desktop\src\chromium\src\base\functional\callback.h:346
    #20 0x7ffecace0f24 in mojo::SimpleWatcher::OnHandleReady C:\Users\test\Desktop\src\chromium\src\mojo\public\cpp\s
ystem\simple_watcher.cc:286
    #21 0x7ffecace19da in mojo::SimpleWatcher::Context::Notify C:\Users\test\Desktop\src\chromium\src\mojo\public\cpp
\system\simple_watcher.cc:97
    #22 0x7ffecacde53a in mojo::SimpleWatcher::Context::CallNotify C:\Users\test\Desktop\src\chromium\src\mojo\public
\cpp\system\simple_watcher.cc:61
    #23 0x7ffeb773661f in mojo::core::ipcz_driver::MojoTrap::DispatchOrQueueEvent C:\Users\test\Desktop\src\chromium\
src\mojo\core\ipcz_driver\mojo_trap.cc:577
    #24 0x7ffeb7738d03 in mojo::core::ipcz_driver::MojoTrap::HandleEvent C:\Users\test\Desktop\src\chromium\src\mojo\
core\ipcz_driver\mojo_trap.cc:459
    #25 0x7ffeb77ec34a in ipcz::TrapEventDispatcher::~TrapEventDispatcher C:\Users\test\Desktop\src\chromium\src\thir
d_party\ipcz\src\ipcz\trap_event_dispatcher.cc:12
    #26 0x7ffeb77d1fdb in ipcz::Router::AcceptInboundParcel C:\Users\test\Desktop\src\chromium\src\third_party\ipcz\s
rc\ipcz\router.cc:272
    #27 0x7ffeb779d377 in ipcz::NodeLink::AcceptCompleteParcel C:\Users\test\Desktop\src\chromium\src\third_party\ipc
z\src\ipcz\node_link.cc:1082

Thread T14 created by T0 here:
    #0 0x7fff1e3cdb84 in _asan_wrap_CreateThread+0x64 (C:\Users\test\Desktop\src\chromium\src\out\asan\clang_rt.asan_
dynamic-x86_64.dll+0x5db84)
    #1 0x7ffeca7e837b in base::`anonymous namespace'::CreateThreadInternal C:\Users\test\Desktop\src\chromium\src\bas
e\threading\platform_thread_win.cc:178
    #2 0x7ffeca8a68c8 in base::Thread::StartWithOptions C:\Users\test\Desktop\src\chromium\src\base\threading\thread.
cc:228
    #3 0x7ffecdf1f2d2 in content::ChildProcess::ChildProcess C:\Users\test\Desktop\src\chromium\src\content\child\chi
ld_process.cc:152
    #4 0x7ffecde94109 in content::GpuMain C:\Users\test\Desktop\src\chromium\src\content\gpu\gpu_main.cc:421
    #5 0x7ffec726deff in content::RunOtherNamedProcessTypeMain C:\Users\test\Desktop\src\chromium\src\content\app\con
tent_main_runner_impl.cc:762
    #6 0x7ffec727066b in content::ContentMainRunnerImpl::Run C:\Users\test\Desktop\src\chromium\src\content\app\conte
nt_main_runner_impl.cc:1152
    #7 0x7ffec726445f in content::RunContentProcess C:\Users\test\Desktop\src\chromium\src\content\app\content_main.c
c:358
    #8 0x7ffec7264c02 in content::ContentMain C:\Users\test\Desktop\src\chromium\src\content\app\content_main.cc:371
    #9 0x7ffeb7092b06 in ChromeMain C:\Users\test\Desktop\src\chromium\src\chrome\app\chrome_main.cc:191
    #10 0x7ff649534807 in MainDllLoader::Launch C:\Users\test\Desktop\src\chromium\src\chrome\app\main_dll_loader_win
.cc:204
    #11 0x7ff649532074 in main C:\Users\test\Desktop\src\chromium\src\chrome\app\chrome_exe_main_win.cc:351
    #12 0x7ff649a2dcdf in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:2
88
    #13 0x7fff80dc7613 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017613)
    #14 0x7fff825e26a0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526a0)

SUMMARY: AddressSanitizer: heap-use-after-free C:\Users\test\Desktop\src\chromium\src\base\win\scoped_handle.h:65 in
base::win::GenericScopedHandle<base::win::HandleTraits,base::win::DummyVerifierTraits>::GenericScopedHandle
Shadow bytes around the buggy address:
  0x11c2c6937780: fd fd fd fd f7 fa fd fd fd fa f7 fa fd fd fd fa
  0x11c2c6937800: f7 fa fd fd fd fd f7 fa fd fd fd fa f7 fa fd fd
  0x11c2c6937880: fd fd f7 fa fd fd fd fd f7 fa fd fd fd fa f7 fa
  0x11c2c6937900: fd fd fd fd f7 fa fd fd fd fd f7 fa fd fd fd fd
  0x11c2c6937980: f7 fa fd fd fd fd f7 fa fd fd fd fa f7 fa fd fd
=>0x11c2c6937a00:[fd]fa f7 fa fd fd fd fd f7 fa fd fd fd fd f7 fa
  0x11c2c6937a80: fd fd fd fd f7 fa fd fd fd fa f7 fa fd fd fd fa
  0x11c2c6937b00: f7 fa fd fd fd fd f7 fa fd fd fd fa f7 fa fd fd
  0x11c2c6937b80: fd fd f7 fa 00 00 00 00 f7 fa fd fd fd fd f7 fa
  0x11c2c6937c00: fd fd fd fd f7 fa fd fd fd fa f7 fa fd fd fd fd
  0x11c2c6937c80: f7 fa 00 00 00 fa f7 fa fd fd fd fd f7 fa fd fd
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

==68036==ADDITIONAL INFO

==68036==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffeb9c8ce18 in gpu::Scheduler::TryScheduleSequence C:\Users\test\Desktop\src\chromium\src\gpu\command_buffe
r\service\scheduler.cc:432

MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==68036==END OF ADDITIONAL INFO

==68036==ABORTING

```
## References

- <https://source.chromium.org/chromium/chromium/src/+/main:ui/gl/dcomp_surface_registry.cc>
- <https://source.chromium.org/chromium/chromium/src/+/main:ui/gl/dcomp_surface_registry.h>
- <https://source.chromium.org/chromium/chromium/src/+/main:components/viz/service/gl/gpu_service_impl.cc>
- <https://source.chromium.org/chromium/chromium/src/+/main:gpu/ipc/service/dcomp_texture_win.cc>

## Credit

86ac1f1587b71893ed2ad792cd7dde32

## Attachments

- [patch.diff](attachments/patch.diff) (text/x-diff, 1.9 KB)
- [poc.html](attachments/poc.html) (text/html, 1.6 KB)
- [bear-vp9.webm](attachments/bear-vp9.webm) (video/webm, 65.9 KB)
- [sleep.diff](attachments/sleep.diff) (text/x-diff, 814 B)
- [poc.html](attachments/poc_74174646.html) (text/html, 1.6 KB)
- [bear-vp9.webm](attachments/bear-vp9_74167887.webm) (video/webm, 65.9 KB)
- [asan-uaf.txt](attachments/asan-uaf.txt) (text/plain, 20.8 KB)
- [asan-oob.txt](attachments/asan-oob.txt) (text/plain, 15.4 KB)

## Timeline

### jd...@chromium.org (2026-03-09)

Thanks for the report. Are you able to provide a PoC that reproduces without a custom patch using MojoJS?

### jd...@chromium.org (2026-03-09)

Due to an influx in security vulnerability reports, I am not able to fully investigate this report. I'm setting labels conservatively assuming the report is valid, and forwarding it on in hopes of getting it in front of the right people quickly.

xhwang@: would you mind taking a look? If this report is invalid, feel free to close with my apologies.

### ch...@google.com (2026-03-10)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-10)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### se...@gmail.com (2026-03-10)

Hi! The PoC patch has two parts: a renderer-side change that forces MediaFoundation renderer selection for clear video, and a GPU-side Sleep that widens the race window between flat\_map iterator acquisition and dereference. Neither sends additional or malformed IPC — the renderer change is a local code path selection and the GPU change only adjusts timing. Since the vulnerability triggers through the normal video playback pipeline rather than direct Mojo IPC, converting to MojoJS provides no advantage.

I've simplified the PoC to retain only the GPU-side Sleep and replace the renderer patch with `--enable-features=MediaFoundationClearPlayback`. This flag isn't a precondition for the bug — it just substitutes for the renderer code change. A compromised renderer could achieve the same by modifying its own factory selection logic directly.

The reproduction method and environment (Windows) remain unchanged.

```
$ git apply sleep.diff
$ ninja -C out/asan/ chrome

$ ls
bear-vp9.webm
poc.html
$ python3 -m http.server

$ out/asan/chrome.exe --user-data-dir=/tmp/poc --enable-features=MediaFoundationClearPlayback --enable-logging=stderr http://127.0.0.1:8000/poc.html > /tmp/poc-output.txt 2>&1

$ cat /tmp/poc-output.txt

```

The `bear-vp9.webm` is a test file from the official Chromium source code: <https://source.chromium.org/chromium/chromium/src/+/main:media/test/data/bear-vp9.webm>.

And the ASan crashes triggered generally fall into two types: one is `heap-use-after-free`, and the other is `container-overflow`.

### pe...@google.com (2026-03-10)

Thank you for providing more feedback. Adding the requester to the CC list.

### xh...@chromium.org (2026-04-09)

This was fixed in <https://chromium-review.git.corp.google.com/c/chromium/src/+/7737061>

### ch...@google.com (2026-04-09)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-04-10)

This is sufficiently serious that it should be merged to M146. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M146. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

This is sufficiently serious that it should be merged to M147. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M147. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to M148. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M148. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

### ch...@google.com (2026-04-10)

**M146** merge request created. **Please update [crbug/501314752](https://crbug.com/501314752) to have this merge reviewed.**

### ch...@google.com (2026-04-10)

**M147** merge request created. **Please update [crbug/501315131](https://crbug.com/501315131) to have this merge reviewed.**

### ch...@google.com (2026-04-10)

**M148** merge request created. **Please update [crbug/501313704](https://crbug.com/501313704) to have this merge reviewed.**

### dx...@google.com (2026-04-10)

Project: chromium/src  

Branch:  refs/branch-heads/7778  

Author:  Jonathan Ross [jonross@chromium.org](mailto:jonross@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7747633>

[M148] gl: Make DCOMPSurfaceRegistry thread-safe

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
     
    Bug: 490251701 
    Fixed: 501313704 
    Change-Id: Ibb7ef5e602f222410fde06a61fb3f5e571e7a70f 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7747633 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: Xiaohan Wang <xhwang@chromium.org> 
    Commit-Queue: Sunny Sachanandani <sunnyps@chromium.org> 
    Reviewed-by: Sunny Sachanandani <sunnyps@chromium.org> 
    Reviewed-by: Jonathan Ross <jonross@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7778@{#259} 
    Cr-Branched-From: 77f495ee216d4c3cc784d33658bad4778c0680ee-refs/heads/main@{#1610480}

```

---

Files:

- M `ui/gl/BUILD.gn`
- M `ui/gl/dcomp_surface_registry.cc`
- M `ui/gl/dcomp_surface_registry.h`
- A `ui/gl/dcomp_surface_registry_unittest.cc`

---

Hash: [5ca5c486b26eda16b32b19da50a4239e1bef1968](https://chromiumdash.appspot.com/commit/5ca5c486b26eda16b32b19da50a4239e1bef1968)  

Date: Fri Apr 10 23:13:20 2026


---

### dx...@google.com (2026-04-13)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Jonathan Ross [jonross@chromium.org](mailto:jonross@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7749840>

[M147] gl: Make DCOMPSurfaceRegistry thread-safe

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
     
    Bug: 490251701 
    Fixed: 501315131 
    Change-Id: I0b7e5f5ce2f699bc6a561dc69ca0db033d1a464d 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7749840 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: Xiaohan Wang <xhwang@chromium.org> 
    Reviewed-by: Sunny Sachanandani <sunnyps@chromium.org> 
    Reviewed-by: Jonathan Ross <jonross@chromium.org> 
    Commit-Queue: Xiaohan Wang <xhwang@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7727@{#2842} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `ui/gl/BUILD.gn`
- M `ui/gl/dcomp_surface_registry.cc`
- M `ui/gl/dcomp_surface_registry.h`
- A `ui/gl/dcomp_surface_registry_unittest.cc`

---

Hash: [94af0d5de45073c5d7ef0538705c90cb36d7705b](https://chromiumdash.appspot.com/commit/94af0d5de45073c5d7ef0538705c90cb36d7705b)  

Date: Mon Apr 13 20:40:24 2026


---

### sp...@google.com (2026-05-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
Baseline with bisect. Memory Corruption / RCE in a highly privileged process (e.g. GPU or network)


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/490251701)*
