# UAF in media::VideoCaptureDeviceFactoryLinux::OnGetDevicesInfo

| Field | Value |
|-------|-------|
| **Issue ID** | [346044228](https://issues.chromium.org/issues/346044228) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Core, Internals>Media>CameraCapture |
| **Platforms** | Linux |
| **Reporter** | m....@gmail.com |
| **Assignee** | il...@chromium.org |
| **Created** | 2024-06-09 |
| **Bounty** | $3,000.00 |

## Description

## reproduce

Found by myfuzzer run on CF(<https://clusterfuzz.com/testcase-detail/5965107015122944>)

## type

Utility process(maybe sandbox escape)

## bisect

<https://chromium-review.googlesource.com/c/chromium/src/+/3308882>

## RCA

1. webrtc\_factory\_->GetDevicesInfo constructs an OnceCallback using the this in the base::Unretained way, which will be posted back to the current task queue and called later [1]
2. VideoCaptureDeviceFactoryLinux will destoryed when mojo::ServiceFactory::OnInstanceDisconnected get call
3. The OnceCallback in the first step is executed, but the this pointer has already been released, causing UAF [2]

```
https://source.chromium.org/chromium/chromium/src/+/main:media/capture/video/linux/video_capture_device_factory_linux.cc;drc=edcd0133f90605ed29cba55b60d4c0d236a3adfb;l=48

void VideoCaptureDeviceFactoryLinux::GetDevicesInfo(
    GetDevicesInfoCallback callback) {
#if defined(WEBRTC_USE_PIPEWIRE)
  if (webrtc_factory_->IsAvailable()) {
    webrtc_factory_->GetDevicesInfo(
        base::BindOnce(&VideoCaptureDeviceFactoryLinux::OnGetDevicesInfo,               <<<1>>>
                       base::Unretained(this), std::move(callback)));
    return;
  }
#endif  // defined(WEBRTC_USE_PIPEWIRE)
  factory_->GetDevicesInfo(std::move(callback));
}

#if defined(WEBRTC_USE_PIPEWIRE)
void VideoCaptureDeviceFactoryLinux::OnGetDevicesInfo(
    GetDevicesInfoCallback callback,
    std::vector<VideoCaptureDeviceInfo> devices_info) {
  // IsAvailable() can change from true to false during device enumeration.
  // Check again to see if we need to fall back to the V4L2 factory.
  if (webrtc_factory_->IsAvailable()) {                                                    <<<2>>>
    std::move(callback).Run(devices_info);
  } else {
    factory_->GetDevicesInfo(std::move(callback));
  }
}

```
## ASAN

```
=================================================================
==2947584==ERROR: AddressSanitizer: heap-use-after-free on address 0x50a00005c1b8 at pc 0x59ce45ecd69c bp 0x7ffe19282450 sp 0x7ffe19282448
READ of size 8 at 0x50a00005c1b8 thread T0 (chrome)
SCARINESS: 51 (8-byte-read-heap-use-after-free)
    #0 0x59ce45ecd69b in operator-> third_party/libc++/src/include/__memory/unique_ptr.h:258:108
    #1 0x59ce45ecd69b in media::VideoCaptureDeviceFactoryLinux::OnGetDevicesInfo(base::OnceCallback<void (std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo>>)>, std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo>>) media/capture/video/linux/video_capture_device_factory_linux.cc:67:7
    #2 0x59ce45ecdb49 in void base::internal::DecayedFunctorTraits<void (media::VideoCaptureDeviceFactoryLinux::*)(base::OnceCallback<void (std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo>>)>, std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo>>), media::VideoCaptureDeviceFactoryLinux*, base::OnceCallback<void (std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo>>)>&&>::Invoke<void (media::VideoCaptureDeviceFactoryLinux::*)(base::OnceCallback<void (std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo>>)>, std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo>>), media::VideoCaptureDeviceFactoryLinux*, base::OnceCallback<void (std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo>>)>, std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo>>>(void (media::VideoCaptureDeviceFactoryLinux::*)(base::OnceCallback<void (std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo>>)>, std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo>>), media::VideoCaptureDeviceFactoryLinux*&&, base::OnceCallback<void (std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo>>)>&&, std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo>>&&) base/functional/bind_internal.h:738:12
    #3 0x59ce45ecd8e4 in MakeItSo<void (media::VideoCaptureDeviceFactoryLinux::*)(base::OnceCallback<void (std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo> >)>, std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo> >), std::__Cr::tuple<base::internal::UnretainedWrapper<media::VideoCaptureDeviceFactoryLinux, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::OnceCallback<void (std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo> >)> >, std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo> > > base/functional/bind_internal.h:930:12
    #4 0x59ce45ecd8e4 in RunImpl<void (media::VideoCaptureDeviceFactoryLinux::*)(base::OnceCallback<void (std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo> >)>, std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo> >), std::__Cr::tuple<base::internal::UnretainedWrapper<media::VideoCaptureDeviceFactoryLinux, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::OnceCallback<void (std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo> >)> >, 0UL, 1UL> base/functional/bind_internal.h:1067:14
    #5 0x59ce45ecd8e4 in base::internal::Invoker<base::internal::FunctorTraits<void (media::VideoCaptureDeviceFactoryLinux::*&&)(base::OnceCallback<void (std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo>>)>, std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo>>), media::VideoCaptureDeviceFactoryLinux*, base::OnceCallback<void (std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo>>)>&&>, base::internal::BindState<true, true, false, void (media::VideoCaptureDeviceFactoryLinux::*)(base::OnceCallback<void (std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo>>)>, std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo>>), base::internal::UnretainedWrapper<media::VideoCaptureDeviceFactoryLinux, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::OnceCallback<void (std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo>>)>>, void (std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo>>)>::RunOnce(base::internal::BindStateBase*, std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo>>&&) base/functional/bind_internal.h:980:12
    #6 0x59ce45eea699 in Run base/functional/callback.h:156:12
    #7 0x59ce45eea699 in void base::internal::DecayedFunctorTraits<base::OnceCallback<void (std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo>>)>, std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo>>&&>::Invoke<base::OnceCallback<void (std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo>>)>, std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo>>>(base::OnceCallback<void (std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo>>)>&&, std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo>>&&) base/functional/bind_internal.h:813:49
    #8 0x59ce45eea428 in MakeItSo<base::OnceCallback<void (std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo> >)>, std::__Cr::tuple<std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo> > > > base/functional/bind_internal.h:930:12
    #9 0x59ce45eea428 in RunImpl<base::OnceCallback<void (std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo> >)>, std::__Cr::tuple<std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo> > >, 0UL> base/functional/bind_internal.h:1067:14
    #10 0x59ce45eea428 in base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo>>)>&&, std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo>>&&>, base::internal::BindState<false, true, true, base::OnceCallback<void (std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo>>)>, std::__Cr::vector<media::VideoCaptureDeviceInfo, std::__Cr::allocator<media::VideoCaptureDeviceInfo>>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:980:12
    #11 0x59ce4092a0e4 in Run base/functional/callback.h:156:12
    #12 0x59ce4092a0e4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:203:34
    #13 0x59ce4098c5c6 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:486:11)> base/task/common/task_annotator.h:90:5
    #14 0x59ce4098c5c6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:484:23
    #15 0x59ce4098b4e0 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #16 0x59ce4098d30a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0
    #17 0x59ce40aefaf2 in base::MessagePumpGlib::HandleDispatch() base/message_loop/message_pump_glib.cc:649:46
    #18 0x59ce40af29b8 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:274:43
    #19 0x7e181b7fe17c in g_main_context_dispatch
    #20 0x7e181b7fe3ff in libglib-2.0.so.0
    #21 0x7e181b7fe4a2 in g_main_context_iteration
    #22 0x59ce40af011f in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:683:30
    #23 0x59ce4098df76 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:654:12
    #24 0x59ce408bd6ef in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14
    #25 0x59ce3c1b0f35 in content::UtilityMain(content::MainFunctionParams) content/utility/utility_main.cc:429:12
    #26 0x59ce3e001bc2 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:779:14
    #27 0x59ce3e004b98 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1151:10
    #28 0x59ce3dffec10 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:332:36
    #29 0x59ce3dfff29b in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:345:10
    #30 0x59ce2dbf93c8 in ChromeMain chrome/app/chrome_main.cc:192:12
    #31 0x7e181a0e3082 in __libc_start_main /build/glibc-BHL3KM/glibc-2.31/csu/libc-start.c:308:16
    #32 0x59ce2db25029 in _start
0x50a00005c1b8 is located 24 bytes inside of 32-byte region [0x50a00005c1a0,0x50a00005c1c0)
freed by thread T0 (chrome) here:
    #0 0x59ce2dbf744d in operator delete(void*) third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:143:3
    #1 0x59ce45eb9b53 in media::VideoCaptureSystemImpl::~VideoCaptureSystemImpl() media/capture/video/video_capture_system_impl.cc:86:49
    #2 0x59ce39ef71f8 in operator() third_party/libc++/src/include/__memory/unique_ptr.h:67:5
    #3 0x59ce39ef71f8 in reset third_party/libc++/src/include/__memory/unique_ptr.h:278:7
    #4 0x59ce39ef71f8 in ~unique_ptr third_party/libc++/src/include/__memory/unique_ptr.h:248:71
    #5 0x59ce39ef71f8 in ~DeviceFactoryImpl services/video_capture/device_factory_impl.cc:97:39
    #6 0x59ce39ef71f8 in video_capture::DeviceFactoryImpl::~DeviceFactoryImpl() services/video_capture/device_factory_impl.cc:97:39
    #7 0x59ce39f23a68 in operator() third_party/libc++/src/include/__memory/unique_ptr.h:67:5
    #8 0x59ce39f23a68 in reset third_party/libc++/src/include/__memory/unique_ptr.h:278:7
    #9 0x59ce39f23a68 in ~unique_ptr third_party/libc++/src/include/__memory/unique_ptr.h:248:71
    #10 0x59ce39f23a68 in ~VirtualDeviceEnabledDeviceFactory services/video_capture/virtual_device_enabled_device_factory.cc:130:71
    #11 0x59ce39f23a68 in video_capture::VirtualDeviceEnabledDeviceFactory::~VirtualDeviceEnabledDeviceFactory() services/video_capture/virtual_device_enabled_device_factory.cc:130:71
    #12 0x59ce39f13639 in operator() third_party/libc++/src/include/__memory/unique_ptr.h:67:5
    #13 0x59ce39f13639 in reset third_party/libc++/src/include/__memory/unique_ptr.h:278:7
    #14 0x59ce39f13639 in video_capture::VideoCaptureServiceImpl::~VideoCaptureServiceImpl() services/video_capture/video_capture_service_impl.cc:262:19
    #15 0x59ce3c1abf5a in operator() third_party/libc++/src/include/__memory/unique_ptr.h:67:5
    #16 0x59ce3c1abf5a in reset third_party/libc++/src/include/__memory/unique_ptr.h:278:7
    #17 0x59ce3c1abf5a in ~unique_ptr third_party/libc++/src/include/__memory/unique_ptr.h:248:71
    #18 0x59ce3c1abf5a in ~InstanceHolder mojo/public/cpp/bindings/service_factory.h:140:40
    #19 0x59ce3c1abf5a in mojo::ServiceFactory::InstanceHolder<content::(anonymous namespace)::UtilityThreadVideoCaptureServiceImpl>::~InstanceHolder() mojo/public/cpp/bindings/service_factory.h:140:40
    #20 0x59ce4207cf09 in operator() third_party/libc++/src/include/__memory/unique_ptr.h:67:5
    #21 0x59ce4207cf09 in reset third_party/libc++/src/include/__memory/unique_ptr.h:278:7
    #22 0x59ce4207cf09 in ~unique_ptr third_party/libc++/src/include/__memory/unique_ptr.h:248:71
    #23 0x59ce4207cf09 in __destroy_at<std::__Cr::unique_ptr<mojo::ServiceFactory::InstanceHolderBase, std::__Cr::default_delete<mojo::ServiceFactory::InstanceHolderBase> >, 0> third_party/libc++/src/include/__memory/construct_at.h:67:11
    #24 0x59ce4207cf09 in destroy<std::__Cr::unique_ptr<mojo::ServiceFactory::InstanceHolderBase, std::__Cr::default_delete<mojo::ServiceFactory::InstanceHolderBase> >, void, 0> third_party/libc++/src/include/__memory/allocator_traits.h:339:5
    #25 0x59ce4207cf09 in __base_destruct_at_end third_party/libc++/src/include/vector:927:7
    #26 0x59ce4207cf09 in __destruct_at_end third_party/libc++/src/include/vector:817:5
    #27 0x59ce4207cf09 in std::__Cr::vector<std::__Cr::unique_ptr<mojo::ServiceFactory::InstanceHolderBase, std::__Cr::default_delete<mojo::ServiceFactory::InstanceHolderBase>>, std::__Cr::allocator<std::__Cr::unique_ptr<mojo::ServiceFactory::InstanceHolderBase, std::__Cr::default_delete<mojo::ServiceFactory::InstanceHolderBase>>>>::erase(std::__Cr::__wrap_iter<std::__Cr::unique_ptr<mojo::ServiceFactory::InstanceHolderBase, std::__Cr::default_delete<mojo::ServiceFactory::InstanceHolderBase>> const*>, std::__Cr::__wrap_iter<std::__Cr::unique_ptr<mojo::ServiceFactory::InstanceHolderBase, std::__Cr::default_delete<mojo::ServiceFactory::InstanceHolderBase>> const*>) third_party/libc++/src/include/vector:1560:11
    #28 0x59ce4207ab72 in erase base/containers/flat_tree.h:865:16
    #29 0x59ce4207ab72 in erase<mojo::ServiceFactory::InstanceHolderBase *> base/containers/flat_tree.h:857:3
    #30 0x59ce4207ab72 in mojo::ServiceFactory::OnInstanceDisconnected(mojo::ServiceFactory::InstanceHolderBase*) mojo/public/cpp/bindings/service_factory.cc:52:14
    #31 0x59ce4207b747 in Invoke<void (mojo::ServiceFactory::*)(mojo::ServiceFactory::InstanceHolderBase *), const base::WeakPtr<mojo::ServiceFactory> &, mojo::ServiceFactory::InstanceHolderBase *> base/functional/bind_internal.h:738:12
    #32 0x59ce4207b747 in MakeItSo<void (mojo::ServiceFactory::*)(mojo::ServiceFactory::InstanceHolderBase *), std::__Cr::tuple<base::WeakPtr<mojo::ServiceFactory>, base::internal::UnretainedWrapper<mojo::ServiceFactory::InstanceHolderBase, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > base/functional/bind_internal.h:954:5
    #33 0x59ce4207b747 in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::ServiceFactory::*&&)(mojo::ServiceFactory::InstanceHolderBase*), base::WeakPtr<mojo::ServiceFactory>&&, mojo::ServiceFactory::InstanceHolderBase*&&>, base::internal::BindState<true, true, false, void (mojo::ServiceFactory::*)(mojo::ServiceFactory::InstanceHolderBase*), base::WeakPtr<mojo::ServiceFactory>, base::internal::UnretainedWrapper<mojo::ServiceFactory::InstanceHolderBase, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<void (mojo::ServiceFactory::*)(mojo::ServiceFactory::InstanceHolderBase*), std::__Cr::tuple<base::WeakPtr<mojo::ServiceFactory>, base::internal::UnretainedWrapper<mojo::ServiceFactory::InstanceHolderBase, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul, 1ul>(void (mojo::ServiceFactory::*&&)(mojo::ServiceFactory::InstanceHolderBase*), std::__Cr::tuple<base::WeakPtr<mojo::ServiceFactory>, base::internal::UnretainedWrapper<mojo::ServiceFactory::InstanceHolderBase, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>) base/functional/bind_internal.h:1067:14
    #34 0x59ce3744a7c7 in Run base/functional/callback.h:156:12
    #35 0x59ce3744a7c7 in base::internal::ThenHelper<base::OnceCallback<void ()>, base::OnceCallback<void ()>>::CreateTrampoline()::'lambda'(base::OnceCallback<void ()>, base::OnceCallback<void ()>)::operator()(base::OnceCallback<void ()>, base::OnceCallback<void ()>) const base/functional/callback_internal.h:206:23
    #36 0x59ce3744a523 in Invoke<(lambda at ../../base/functional/callback_internal.h:202:12), base::OnceCallback<void ()>, base::OnceCallback<void ()> > base/functional/bind_internal.h:656:12
    #37 0x59ce3744a523 in MakeItSo<(lambda at ../../base/functional/callback_internal.h:202:12), std::__Cr::tuple<base::OnceCallback<void ()>, base::OnceCallback<void ()> > > base/functional/bind_internal.h:930:12
    #38 0x59ce3744a523 in RunImpl<(lambda at ../../base/functional/callback_internal.h:202:12), std::__Cr::tuple<base::OnceCallback<void ()>, base::OnceCallback<void ()> >, 0UL, 1UL> base/functional/bind_internal.h:1067:14
    #39 0x59ce3744a523 in base::internal::Invoker<base::internal::FunctorTraits<base::internal::ThenHelper<base::OnceCallback<void ()>, base::OnceCallback<void ()>>::CreateTrampoline()::'lambda'(base::OnceCallback<void ()>, base::OnceCallback<void ()>)&&, base::OnceCallback<void ()>&&, base::OnceCallback<void ()>&&>, base::internal::BindState<false, false, false, base::internal::ThenHelper<base::OnceCallback<void ()>, base::OnceCallback<void ()>>::CreateTrampoline()::'lambda'(base::OnceCallback<void ()>, base::OnceCallback<void ()>), base::OnceCallback<void ()>, base::OnceCallback<void ()>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:980:12
    #40 0x59ce4207b093 in Run base/functional/callback.h:156:12
    #41 0x59ce4207b093 in mojo::ServiceFactory::InstanceHolderBase::OnPipeSignaled(unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/bindings/service_factory.cc:83:37
    #42 0x59ce4207bbb6 in Invoke<void (mojo::ServiceFactory::InstanceHolderBase::*)(unsigned int, const mojo::HandleSignalsState &), mojo::ServiceFactory::InstanceHolderBase *, unsigned int, const mojo::HandleSignalsState &> base/functional/bind_internal.h:738:12
    #43 0x59ce4207bbb6 in MakeItSo<void (mojo::ServiceFactory::InstanceHolderBase::*const &)(unsigned int, const mojo::HandleSignalsState &), const std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::ServiceFactory::InstanceHolderBase, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, unsigned int, const mojo::HandleSignalsState &> base/functional/bind_internal.h:930:12
    #44 0x59ce4207bbb6 in RunImpl<void (mojo::ServiceFactory::InstanceHolderBase::*const &)(unsigned int, const mojo::HandleSignalsState &), const std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::ServiceFactory::InstanceHolderBase, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, 0UL> base/functional/bind_internal.h:1067:14
    #45 0x59ce4207bbb6 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::ServiceFactory::InstanceHolderBase::* const&)(unsigned int, mojo::HandleSignalsState const&), mojo::ServiceFactory::InstanceHolderBase*>, base::internal::BindState<true, true, false, void (mojo::ServiceFactory::InstanceHolderBase::*)(unsigned int, mojo::HandleSignalsState const&), base::internal::UnretainedWrapper<mojo::ServiceFactory::InstanceHolderBase, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&) base/functional/bind_internal.h:987:12
    #46 0x59ce420b2b8b in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const & base/functional/callback.h:344:12
    #47 0x59ce420b24b3 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple_watcher.cc:278:14
    #48 0x59ce420b36f4 in Invoke<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), const base::WeakPtr<mojo::SimpleWatcher> &, int, unsigned int, mojo::HandleSignalsState> base/functional/bind_internal.h:738:12
    #49 0x59ce420b36f4 in MakeItSo<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> > base/functional/bind_internal.h:954:5
    #50 0x59ce420b36f4 in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0ul, 1ul, 2ul, 3ul>(void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>) base/functional/bind_internal.h:1067:14
    #51 0x59ce4092a0e4 in Run base/functional/callback.h:156:12
    #52 0x59ce4092a0e4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:203:34
    #53 0x59ce4098c5c6 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:486:11)> base/task/common/task_annotator.h:90:5
    #54 0x59ce4098c5c6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:484:23
    #55 0x59ce4098b4e0 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #56 0x59ce4098d30a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0
    #57 0x59ce40af0429 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:694:48
    #58 0x59ce4098df76 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:654:12
    #59 0x59ce408bd6ef in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14
    #60 0x59ce3c1b0f35 in content::UtilityMain(content::MainFunctionParams) content/utility/utility_main.cc:429:12
    #61 0x59ce3e001bc2 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:779:14
    #62 0x59ce3e004b98 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1151:10
    #63 0x59ce3dffec10 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:332:36
    #64 0x59ce3dfff29b in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:345:10
    #65 0x59ce2dbf93c8 in ChromeMain chrome/app/chrome_main.cc:192:12
    #66 0x7e181a0e3082 in __libc_start_main /build/glibc-BHL3KM/glibc-2.31/csu/libc-start.c:308:16
previously allocated by thread T0 (chrome) here:
    #0 0x59ce2dbf6bed in operator new(unsigned long) third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:86:3
    #1 0x59ce45eaae6c in make_unique<media::VideoCaptureDeviceFactoryLinux, scoped_refptr<base::SingleThreadTaskRunner> &> third_party/libc++/src/include/__memory/unique_ptr.h:620:26
    #2 0x59ce45eaae6c in CreatePlatformSpecificVideoCaptureDeviceFactory media/capture/video/create_video_capture_device_factory.cc:60:10
    #3 0x59ce45eaae6c in media::CreateVideoCaptureDeviceFactory(scoped_refptr<base::SingleThreadTaskRunner>) media/capture/video/create_video_capture_device_factory.cc:96:12
    #4 0x59ce39f14b52 in video_capture::VideoCaptureServiceImpl::LazyInitializeDeviceFactory() services/video_capture/video_capture_service_impl.cc:341:7
    #5 0x59ce39f13f8b in video_capture::VideoCaptureServiceImpl::LazyInitializeVideoSourceProvider() services/video_capture/video_capture_service_impl.cc:404:3
    #6 0x59ce39f13de1 in video_capture::VideoCaptureServiceImpl::ConnectToVideoSourceProvider(mojo::PendingReceiver<video_capture::mojom::VideoSourceProvider>) services/video_capture/video_capture_service_impl.cc:297:3
    #7 0x59ce31f165e2 in video_capture::mojom::VideoCaptureServiceStubDispatch::Accept(video_capture::mojom::VideoCaptureService*, mojo::Message*) gen/services/video_capture/public/mojom/video_capture_service.mojom.cc:253:13
    #8 0x59ce420313b7 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1036:54
    #9 0x59ce4204d37a in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #10 0x59ce42036575 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:721:20
    #11 0x59ce4205af7f in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:1120:42
    #12 0x59ce42058cb0 in mojo::internal::MultiplexRouter::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/multiplex_router.cc:733:7
    #13 0x59ce4204d37a in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #14 0x59ce42028adb in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) mojo/public/cpp/bindings/lib/connector.cc:562:49
    #15 0x59ce4202a450 in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:620:14
    #16 0x59ce4202ae6d in Invoke<void (mojo::Connector::*)(), const base::WeakPtr<mojo::Connector> &> base/functional/bind_internal.h:738:12
    #17 0x59ce4202ae6d in MakeItSo<void (mojo::Connector::*)(), std::__Cr::tuple<base::WeakPtr<mojo::Connector> > > base/functional/bind_internal.h:954:5
    #18 0x59ce4202ae6d in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::*&&)(), base::WeakPtr<mojo::Connector>&&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(), base::WeakPtr<mojo::Connector>>, void ()>::RunImpl<void (mojo::Connector::*)(), std::__Cr::tuple<base::WeakPtr<mojo::Connector>>, 0ul>(void (mojo::Connector::*&&)(), std::__Cr::tuple<base::WeakPtr<mojo::Connector>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/bind_internal.h:1067:14
    #19 0x59ce4092a0e4 in Run base/functional/callback.h:156:12
    #20 0x59ce4092a0e4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:203:34
    #21 0x59ce4098c5c6 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:486:11)> base/task/common/task_annotator.h:90:5
    #22 0x59ce4098c5c6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:484:23
    #23 0x59ce4098b4e0 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #24 0x59ce4098d30a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0
    #25 0x59ce40aefaf2 in base::MessagePumpGlib::HandleDispatch() base/message_loop/message_pump_glib.cc:649:46
    #26 0x59ce40af29b8 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:274:43
    #27 0x7e181b7fe17c in g_main_context_dispatch
SUMMARY: AddressSanitizer: heap-use-after-free (/mnt/scratch0/clusterfuzz/bot/builds/chromium-browser-asan_linux-release-media_eb660d5ee526c9c1c1608a71fcbe7a713c490533/revisions/chrome+0x26f6669b) (BuildId: 1486a0b2c1e93e30)
Shadow bytes around the buggy address:
  0x50a00005bf00: fa fa f7 fa fd fd fd fd fa fa fa fa fa fa fa fa
  0x50a00005bf80: fa fa fa fa fa fa f7 fa fd fd fd fd fa fa fa fa
  0x50a00005c000: fa fa fa fa fa fa fa fa fa fa f7 fa fd fd fd fa
  0x50a00005c080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x50a00005c100: fd fd fd fd fa fa fa fa fa fa fa fa fa fa fa fa
=>0x50a00005c180: fa fa f7 fa fd fd fd[fd]fa fa fa fa fa fa fa fa
  0x50a00005c200: fa fa fa fa fa fa f7 fa fd fd fd fa fa fa fa fa
  0x50a00005c280: fa fa fa fa fa fa fa fa fa fa f7 fa fd fd fd fa
  0x50a00005c300: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x50a00005c380: fd fd fd fd fa fa fa fa fa fa fa fa fa fa fa fa
  0x50a00005c400: fa fa f7 fa fd fd fd fd fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:00
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
==2947584==ADDITIONAL INFO
==2947584==Note: Please include this section with the ASan report.
Task trace:
    #0 0x59ce45ee99cd in media::VideoCaptureDeviceFactoryWebRtc::FinishGetDevicesInfo() media/capture/video/linux/video_capture_device_factory_webrtc.cc:98:7
    #1 0x59ce420b130f in mojo::SimpleWatcher::ArmOrNotify() mojo/public/cpp/system/simple_watcher.cc:238:28
    #2 0x59ce4202aa37 in PostDispatchNextMessageFromPipe mojo/public/cpp/bindings/lib/connector.cc:582:7
    #3 0x59ce4202aa37 in mojo::Connector::ScheduleDispatchOfPendingMessagesOrWaitForMore(unsigned long) mojo/public/cpp/bindings/lib/connector.cc:604:5
    #4 0x59ce420b130f in mojo::SimpleWatcher::ArmOrNotify() mojo/public/cpp/system/simple_watcher.cc:238:28
MiraclePtr Status: PROTECTED
This crash occurred inside a callback where a raw_ptr<T> pointing to the same region was bound to one of the arguments.
MiraclePtr is expected to make this crash non-exploitable once fully enabled.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.
==2947584==END OF ADDITIONAL INFO
==2947584==ABORTING

```

## Timeline

### cl...@appspot.gserviceaccount.com (2024-06-10)

Detailed Report: https://clusterfuzz.com/testcase?key=5965107015122944

Fuzzer: b0ring_webidl_fuzzer
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x50a00005c1b8
Crash State:
  void base::internal::DecayedFunctorTraits<void
  base::internal::Invoker<base::internal::FunctorTraits<void
  void base::internal::DecayedFunctorTraits<base::OnceCallback<void
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_media&revision=1306983

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5965107015122944

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### 24...@project.gserviceaccount.com (2024-06-10)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2024-06-10)

ClusterFuzz testcase 5965107015122944 appears to be flaky, updating reproducibility hotlist.

### li...@chromium.org (2024-06-10)

tommi@ could you PTAL as one of the reviewrs on the bisected CL? This looks pretty flaky as an FYI

### il...@chromium.org (2024-06-11)

One way to fix this is to change webrtc\_factory\_ to not trigger any callbacks after it's been destructed. But it's not quite clean to have the fix in webrtc repository.

Second option is to slap a `WeakPtrFactory` onto `VideoCaptureDeviceFactoryLinux` and pass a `WeakPtr` into callback instead of the `Unretained(this)`.

If no one objects, I'll go with the second option.

### ap...@google.com (2024-06-11)

Project: chromium/src
Branch: main

commit d76c14af8c1a1ecf07b4f3c618683bde52b811eb
Author: Ilya Nikolaevskiy <ilnik@chromium.org>
Date:   Tue Jun 11 13:58:52 2024

    Use WeakPtr in VideoCaptureDeviceFactoryLinux instead of Unretained(this)
    
    Fixed: 346044228
    Change-Id: Ia0e5ceb9115c8f23770dd3a2ffa5bef1d9a1c46f
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5621333
    Commit-Queue: Ilya Nikolaevskiy <ilnik@chromium.org>
    Reviewed-by: Guido Urdaneta <guidou@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1313383}

M       media/capture/video/linux/video_capture_device_factory_linux.cc
M       media/capture/video/linux/video_capture_device_factory_linux.h

https://chromium-review.googlesource.com/5621333


### pe...@google.com (2024-06-11)

Dear owner, thanks for fixing this bug. We've reopened it because security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact ([security@chromium.org](mailto:security@chromium.org)) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues> FoundIn guidelines: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security> Thanks for your time!

### pe...@google.com (2024-06-11)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-06-12)

Requesting merge to dev (M127) because latest trunk commit (1313383) appears to be after dev branch point (1313161).
Merge approved: your change passed merge requirements and is auto-approved for M127. Please go ahead and merge the CL to branch 6533 (refs/branch-heads/6533) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: eakpobaro (Android), eakpobaro (iOS), alonbajayo (ChromeOS), danielyip (Desktop)
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [127].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### pe...@google.com (2024-06-17)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### il...@google.com (2024-06-17)

Sorry, I've missed the ping.

1. <https://chromium-review.googlesource.com/c/chromium/src/+/5621333>
2. Tested on canary
3. no
4. no
5. no

Cherry-pick to M127 is in CQ.

### ap...@google.com (2024-06-17)

Project: chromium/src
Branch: refs/branch-heads/6533

commit 5ed200daa4cb14c2f460c06c5964d60d6d0afd42
Author: Ilya Nikolaevskiy <ilnik@chromium.org>
Date:   Mon Jun 17 17:59:19 2024

    [M127] Use WeakPtr in VideoCaptureDeviceFactoryLinux instead of Unretained(this)
    
    (cherry picked from commit d76c14af8c1a1ecf07b4f3c618683bde52b811eb)
    
    Fixed: 346044228
    Change-Id: Ia0e5ceb9115c8f23770dd3a2ffa5bef1d9a1c46f
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5621333
    Commit-Queue: Ilya Nikolaevskiy <ilnik@chromium.org>
    Reviewed-by: Guido Urdaneta <guidou@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1313383}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5630748
    Reviewed-by: Mark Foltz <mfoltz@chromium.org>
    Commit-Queue: Mark Foltz <mfoltz@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6533@{#281}
    Cr-Branched-From: 7e0b87ec6b8cb5cb2969e1479fc25776e582721d-refs/heads/main@{#1313161}

M       media/capture/video/linux/video_capture_device_factory_linux.cc
M       media/capture/video/linux/video_capture_device_factory_linux.h

https://chromium-review.googlesource.com/5630748


### sp...@google.com (2024-06-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
$2,000 for report of highly mitigated (by BRP protection) memory corruption in a non-sandboxed process + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-21)

Congratulations! Thank you for your efforts and reporting this issue to us!

### pe...@google.com (2024-09-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/346044228)*
