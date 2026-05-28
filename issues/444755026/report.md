# Buffer Overflow in Y16 Video Capture

| Field | Value |
|-------|-------|
| **Issue ID** | [444755026](https://issues.chromium.org/issues/444755026) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media>CameraCapture |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | el...@cryptosearch.tools |
| **Assignee** | il...@chromium.org |
| **Created** | 2025-09-12 |
| **Bounty** | $4,000.00 |

## Description

---

### Report description

Buffer Overflow in Y16 Video Capture

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

---

### The problem

#### Please describe the technical details of the vulnerability

There is a buffer overflow in the Y16 video capture implementation. The problem is that the buffer is allocated based on the width of the images, but copied size includes padding. If padding is present, this will result in a buffer overflow in the destination shared memory region. Interestingly, there is a comment in the code that acknowledges the fact that padding may be present.
Vulnerable code:
<https://source.chromium.org/chromium/chromium/src/+/refs/tags/140.0.7339.128:media/capture/video/video_capture_device_client.cc;drc=fe5d35fd601e4b1461bd447f334b7e0494e64c61;l=1084>

```
void VideoCaptureDeviceClient::OnIncomingCapturedY16Data(
    const uint8_t* data,
    int length,
    const VideoCaptureFormat& format,
    base::TimeTicks reference_time,
    base::TimeDelta timestamp,
    std::optional<base::TimeTicks> capture_begin_timestamp,
    const std::optional<VideoFrameMetadata>& metadata,
    int frame_feedback_id) {
  Buffer buffer;
  const auto reservation_result_code = ReserveOutputBuffer(
      format.frame_size, PIXEL_FORMAT_Y16, frame_feedback_id, &buffer,
      /*require_new_buffer_id=*/nullptr, /*retire_old_buffer_id=*/nullptr);
  // The input |length| can be greater than the required buffer size because of
  // paddings and/or alignments, but it cannot be smaller.
  CHECK_GE(static_cast<size_t>(length),
           media::VideoFrame::AllocationSize(format.pixel_format,
                                             format.frame_size));
  // Failed to reserve output buffer, so drop the frame.
  if (reservation_result_code != ReserveResult::kSucceeded) {
    receiver_->OnFrameDropped(
        ConvertReservationFailureToFrameDropReason(reservation_result_code));
    return;
  }
  auto buffer_access = buffer.handle_provider->GetHandleForInProcessAccess();
  memcpy(buffer_access->data(), data, length);
  const VideoCaptureFormat output_format = VideoCaptureFormat(
      format.frame_size, format.frame_rate, PIXEL_FORMAT_Y16);
  OnIncomingCapturedBuffer(std::move(buffer), output_format, reference_time,
                           timestamp, capture_begin_timestamp, metadata);
}

```
### Proof of Concept

I do not have a Y16 camera, so I implemented virtual cameras for Windows and Linux as a proof of concept.

#### Windows

Chrome version used: 140.0.7339.128 (Official Build) (64-bit) (cohort: Stable)

Install `VCamSample.zip` according to the README (I modified the code to make it use the Y16 pixel format, but the installation still works the same way). Launch Chrome with the command line

```
"C:\Program Files\Google\Chrome\Application\chrome.exe" --enable-logging=stderr --v=1 --utility-startup-dialog=video_capture.mojom.VideoCaptureService --no-sandbox

```

Attach the Visual Studio Debugger to the `VideoCaptureService` process. Then, open `y16_auto_final.html` in Chrome and observe the crash with the error "access violation" (like in the png files appended to this report). Call stack:

```
chrome.dll!memcpy_repmovs() Line 50

chrome.dll!media::VideoCaptureDeviceClient::OnIncomingCapturedY16Data(const unsigned char * data, int length, const media::VideoCaptureFormat & format, base::TimeTicks reference_time, base::TimeDelta timestamp, std::__Cr::optional<base::TimeTicks> capture_begin_timestamp, const std::__Cr::optional<media::VideoFrameMetadata> & metadata, int frame_feedback_id) Line 1110

chrome.dll!media::VideoCaptureDeviceClient::OnIncomingCapturedData(const unsigned char * data, int length, const media::VideoCaptureFormat & format, const gfx::ColorSpace & data_color_space, int rotation, bool flip_y, base::TimeTicks reference_time, base::TimeDelta timestamp, std::__Cr::optional<base::TimeTicks> capture_begin_timestamp, const std::__Cr::optional<media::VideoFrameMetadata> & metadata, int frame_feedback_id) Line 533

chrome.dll!media::VideoCaptureDevice::Client::OnIncomingCapturedData(const unsigned char * data, int length, const media::VideoCaptureFormat & frame_format, const gfx::ColorSpace & color_space, int clockwise_rotation, bool flip_y, base::TimeTicks reference_time, base::TimeDelta timestamp, std::__Cr::optional<base::TimeTicks> capture_begin_timestamp, const std::__Cr::optional<media::VideoFrameMetadata> & metadata) Line 96

chrome.dll!media::VideoCaptureDeviceMFWin::OnIncomingCapturedDataInternal() Line 2507

[Inline Frame] chrome.dll!base::OnceCallback<void ()>::Run() Line 156

[Inline Frame] chrome.dll!base::TaskAnnotator::RunTaskImpl(base::PendingTask & pending_task) Line 207

[Inline Frame] chrome.dll!base::TaskAnnotator::RunTask(perfetto::StaticString event_name, base::PendingTask & pending_task, base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl::<lambda_4> && args) Line 104

[Inline Frame] chrome.dll!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow * continuation_lazy_now) Line 456

chrome.dll!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() Line 330

chrome.dll!base::MessagePumpDefault::Run(base::MessagePump::Delegate * delegate) Line 43

chrome.dll!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool application_tasks_allowed, base::TimeDelta timeout) Line 632

chrome.dll!base::RunLoop::Run(const base::Location & location) Line 136

chrome.dll!content::UtilityMain(content::MainFunctionParams parameters) Line 506

chrome.dll!content::RunOtherNamedProcessTypeMain(const std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char>> & process_type, content::MainFunctionParams main_function_params, content::ContentMainDelegate * delegate) Line 763

chrome.dll!content::ContentMainRunnerImpl::Run() Line 1131

[Inline Frame] chrome.dll!content::RunContentProcess(content::ContentMainParams params, content::ContentMainRunner * content_main_runner) Line 361

chrome.dll!content::ContentMain(content::ContentMainParams params) Line 374

chrome.dll!ChromeMain(HINSTANCE__ * instance, sandbox::SandboxInterfaceInfo * sandbox_info, __int64 exe_entry_point_ticks, __int64 preread_begin_ticks, __int64 preread_end_ticks) Line 224

[External Code]	

```
#### Linux

Chrome version used: 140.0.7339.127 official ASAN build for linux (stable channel)

Note: Linux does not allocate shared memory using 64KiB VirtualAlloc blocks with unmapped pages if the end of the last 4KiB page does not coincide with the 64KiB block boundary, like Windows does, which increases the probability that an adjacent shared memory block will swallow the overflow without a crash. ASAN also does not add redzones next to the shared memory regions.

Note: I tested this on Debian 11 5.10.0-35-amd64

First, get the kernel sources:

```
sudo apt-get install build-essential linux-headers-$(uname -r)
apt-get source linux   # get the exact matching source for your kernel build
cd linux-*/drivers/media/test-drivers/vivid

```

Replace the `vivid` folder with the content from the file `vivid.zip` appended to this report. Compile the `vivid` driver and load it (we first load the original version using modprobe to load dependencies, then remove it and load our own build which was modified to use Y16):

```
make -C /lib/modules/$(uname -r)/build M=$PWD modules
sudo modprobe vivid n_devs=1 vid_cap_nr=42
sudo rmmod vivid
sudo insmod ./vivid.ko n_devs=1 vid_cap_nr=42

```

Open ASAN Chrome with the following command line:

```
./chrome --disable-gpu-sandbox --no-sandbox

```

Open `y16_auto_final.html` and you will get the following ASAN stack trace:

```
=================================================================
==586193==ERROR: AddressSanitizer: memcpy-param-overlap: memory ranges [0x7b385d3dc000,0x7b385d4a6800) and [0x7b385d4a3000, 0x7b385d56d800) overlap
    #0 0x563d91527219 in __asan_memcpy (/home/elias/chromium-exploits/asanchrome-new/chrome+0xff44219) (BuildId: 751dffbb7e8a9303)
    #1 0x563dacc244fc in media::VideoCaptureDeviceClient::OnIncomingCapturedY16Data(unsigned char const*, int, media::VideoCaptureFormat const&, base::TimeTicks, base::TimeDelta, std::__Cr::optional<base::TimeTicks>, std::__Cr::optional<media::VideoFrameMetadata> const&, int) media/capture/video/video_capture_device_client.cc:1109:3
    #2 0x563dacc2342e in media::VideoCaptureDeviceClient::OnIncomingCapturedData(unsigned char const*, int, media::VideoCaptureFormat const&, gfx::ColorSpace const&, int, bool, base::TimeTicks, base::TimeDelta, std::__Cr::optional<base::TimeTicks>, std::__Cr::optional<media::VideoFrameMetadata> const&, int) media/capture/video/video_capture_device_client.cc:533:12
    #3 0x563d9510b093 in media::VideoCaptureDevice::Client::OnIncomingCapturedData(unsigned char const*, int, media::VideoCaptureFormat const&, gfx::ColorSpace const&, int, bool, base::TimeTicks, base::TimeDelta, std::__Cr::optional<base::TimeTicks>, std::__Cr::optional<media::VideoFrameMetadata> const&) media/capture/video/video_capture_device.cc:96:3
    #4 0x563dacc497f3 in media::V4L2CaptureDelegate::DoCapture() media/capture/video/linux/v4l2_capture_delegate.cc:1164:18
    #5 0x563dacc52144 in Invoke<void (V4L2CaptureDelegate::*)(), const base::WeakPtr<media::V4L2CaptureDelegate> &> base/functional/bind_internal.h:731:12
    #6 0x563dacc52144 in MakeItSo<void (V4L2CaptureDelegate::*)(), std::__Cr::tuple<base::WeakPtr<media::V4L2CaptureDelegate> > > base/functional/bind_internal.h:947:5
    #7 0x563dacc52144 in RunImpl<void (V4L2CaptureDelegate::*)(), std::__Cr::tuple<base::WeakPtr<media::V4L2CaptureDelegate> >, 0UL> base/functional/bind_internal.h:1060:14
    #8 0x563dacc52144 in base::internal::Invoker<base::internal::FunctorTraits<void (media::V4L2CaptureDelegate::*&&)(), base::WeakPtr<media::V4L2CaptureDelegate>&&>, base::internal::BindState<true, true, false, void (media::V4L2CaptureDelegate::*)(), base::WeakPtr<media::V4L2CaptureDelegate> >, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:973:12
    #9 0x563da71eee06 in Run base/functional/callback.h:156:12
    #10 0x563da71eee06 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:207:34
    #11 0x563da72863ba in RunTask<(lambda at ../../base/task/thread_pool/task_tracker.cc:687:35)> base/task/common/task_annotator.h:104:5
    #12 0x563da72863ba in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) base/task/thread_pool/task_tracker.cc:686:19
    #13 0x563da728660c in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) base/task/thread_pool/task_tracker.cc:671:3
    #14 0x563da7284c14 in RunTaskWithShutdownBehavior base/task/thread_pool/task_tracker.cc:701:7
    #15 0x563da7284c14 in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&) base/task/thread_pool/task_tracker.cc:501:5
    #16 0x563da7283c74 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource) base/task/thread_pool/task_tracker.cc:391:5
    #17 0x563da72c4dd3 in base::internal::WorkerThread::RunWorker() base/task/thread_pool/worker_thread.cc:473:36
    #18 0x563da72c4167 in base::internal::WorkerThread::RunDedicatedWorker() base/task/thread_pool/worker_thread.cc:379:3
    #19 0x563da72c38e9 in base::internal::WorkerThread::ThreadMain() base/task/thread_pool/worker_thread.cc:345:7
    #20 0x563da734062e in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:101:13
    #21 0x563d91526fd6 in asan_thread_start(void*) (/home/elias/chromium-exploits/asanchrome-new/chrome+0xff43fd6) (BuildId: 751dffbb7e8a9303)

Address 0x7b385d3dc000 is a wild pointer inside of access range of size 0x0000000ca800.
Address 0x7b385d4a3000 is a wild pointer inside of access range of size 0x0000000ca800.
SUMMARY: AddressSanitizer: memcpy-param-overlap (/home/elias/chromium-exploits/asanchrome-new/chrome+0xff44219) (BuildId: 751dffbb7e8a9303) in __asan_memcpy
Thread T7 (ThreadPoolSingl) created by T0 (chrome) here:
    #0 0x563d9150d8c1 in pthread_create (/home/elias/chromium-exploits/asanchrome-new/chrome+0xff2a8c1) (BuildId: 751dffbb7e8a9303)
    #1 0x563da733fc18 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) base/threading/platform_thread_posix.cc:149:13
    #2 0x563da72c26b8 in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*) base/task/thread_pool/worker_thread.cc:185:3
    #3 0x563da72a52ee in CreateTaskRunnerImpl<base::internal::(anonymous namespace)::WorkerThreadDelegate> base/task/thread_pool/pooled_single_thread_task_runner_manager.cc:749:13
    #4 0x563da72a52ee in base::internal::PooledSingleThreadTaskRunnerManager::CreateSingleThreadTaskRunner(base::TaskTraits const&, base::SingleThreadTaskRunnerThreadMode) base/task/thread_pool/pooled_single_thread_task_runner_manager.cc:685:10
    #5 0x563dacc3fcfb in media::VideoCaptureDeviceLinux::VideoCaptureDeviceLinux(scoped_refptr<media::V4L2CaptureDevice>, media::VideoCaptureDeviceDescriptor const&) media/capture/video/linux/video_capture_device_linux.cc:61:20
    #6 0x563dacc39180 in make_unique<media::VideoCaptureDeviceLinux, media::V4L2CaptureDevice *, const media::VideoCaptureDeviceDescriptor &, 0> third_party/libc++/src/include/__memory/unique_ptr.h:759:30
    #7 0x563dacc39180 in media::VideoCaptureDeviceFactoryV4L2::CreateDevice(media::VideoCaptureDeviceDescriptor const&) media/capture/video/linux/video_capture_device_factory_v4l2.cc:148:7
    #8 0x563dacc372b6 in media::VideoCaptureDeviceFactoryLinux::CreateDevice(media::VideoCaptureDeviceDescriptor const&) media/capture/video/linux/video_capture_device_factory_linux.cc
    #9 0x563dacc2d54c in media::VideoCaptureSystemImpl::CreateDevice(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&) media/capture/video/video_capture_system_impl.cc:112:20
    #10 0x563d9eece088 in video_capture::DeviceFactoryImpl::CreateAndAddNewDevice(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, base::OnceCallback<void (video_capture::DeviceFactory::DeviceInfo)>) services/video_capture/device_factory_impl.cc:181:24
    #11 0x563d9eecf1e5 in Invoke<void (DeviceFactoryImpl::*)(const std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > &, base::OnceCallback<void (video_capture::DeviceFactory::DeviceInfo)>), const base::WeakPtr<video_capture::DeviceFactoryImpl> &, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >, base::OnceCallback<void (video_capture::DeviceFactory::DeviceInfo)> > base/functional/bind_internal.h:731:12
    #12 0x563d9eecf1e5 in MakeItSo<void (DeviceFactoryImpl::*)(const std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > &, base::OnceCallback<void (video_capture::DeviceFactory::DeviceInfo)>), std::__Cr::tuple<base::WeakPtr<video_capture::DeviceFactoryImpl>, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >, base::OnceCallback<void (video_capture::DeviceFactory::DeviceInfo)> > > base/functional/bind_internal.h:947:5
    #13 0x563d9eecf1e5 in RunImpl<void (DeviceFactoryImpl::*)(const std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > &, base::OnceCallback<void (video_capture::DeviceFactory::DeviceInfo)>), std::__Cr::tuple<base::WeakPtr<video_capture::DeviceFactoryImpl>, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >, base::OnceCallback<void (video_capture::DeviceFactory::DeviceInfo)> >, 0UL, 1UL, 2UL> base/functional/bind_internal.h:1060:14
    #14 0x563d9eecf1e5 in base::internal::Invoker<base::internal::FunctorTraits<void (video_capture::DeviceFactoryImpl::*&&)(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, base::OnceCallback<void (video_capture::DeviceFactory::DeviceInfo)>), base::WeakPtr<video_capture::DeviceFactoryImpl>&&, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >&&, base::OnceCallback<void (video_capture::DeviceFactory::DeviceInfo)>&&>, base::internal::BindState<true, true, false, void (video_capture::DeviceFactoryImpl::*)(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, base::OnceCallback<void (video_capture::DeviceFactory::DeviceInfo)>), base::WeakPtr<video_capture::DeviceFactoryImpl>, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >, base::OnceCallback<void (video_capture::DeviceFactory::DeviceInfo)> >, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:973:12
    #15 0x563d9eecdc5c in Run base/functional/callback.h:156:12
    #16 0x563d9eecdc5c in video_capture::DeviceFactoryImpl::CreateDevice(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, base::OnceCallback<void (video_capture::DeviceFactory::DeviceInfo)>) services/video_capture/device_factory_impl.cc:135:45
    #17 0x563d9eefc28d in video_capture::VirtualDeviceEnabledDeviceFactory::CreateDevice(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, base::OnceCallback<void (video_capture::DeviceFactory::DeviceInfo)>) services/video_capture/virtual_device_enabled_device_factory.cc:153:27
    #18 0x563d9eef25dc in video_capture::VideoSourceImpl::StartDeviceWithSettings(media::VideoCaptureParams const&) services/video_capture/video_source_impl.cc:134:20
    #19 0x563d9eef189e in video_capture::VideoSourceImpl::CreatePushSubscription(mojo::PendingRemote<video_capture::mojom::VideoFrameHandler>, media::VideoCaptureParams const&, bool, mojo::PendingReceiver<video_capture::mojom::PushVideoStreamSubscription>, base::OnceCallback<void (mojo::InlinedStructPtr<video_capture::mojom::CreatePushSubscriptionResultCode>, media::VideoCaptureParams const&)>) services/video_capture/video_source_impl.cc:63:7
    #20 0x563d95159074 in video_capture::mojom::VideoSourceStubDispatch::AcceptWithResponder(video_capture::mojom::VideoSource*, mojo::Message*, std::__Cr::unique_ptr<mojo::MessageReceiverWithStatus, std::__Cr::default_delete<mojo::MessageReceiverWithStatus> >) gen/services/video_capture/public/mojom/video_source.mojom.cc:2020:13
    #21 0x563da6fc4330 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1013:56
    #22 0x563da6fe1c1d in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:48:24
    #23 0x563da6fc9f74 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:731:20
    #24 0x563da6ff1b3a in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:1120:42
    #25 0x563da6ff0046 in mojo::internal::MultiplexRouter::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/multiplex_router.cc:733:7
    #26 0x563da6fe1d1a in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #27 0x563da6fbae22 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) mojo/public/cpp/bindings/lib/connector.cc:561:49
    #28 0x563da6fbc5c0 in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:619:14
    #29 0x563da6fbbfe9 in OnHandleReadyInternal mojo/public/cpp/bindings/lib/connector.cc:450:3
    #30 0x563da6fbbfe9 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int) mojo/public/cpp/bindings/lib/connector.cc:416:3
    #31 0x563da6fbde6a in Invoke<void (Connector::*)(const char *, unsigned int), mojo::Connector *, const char *, unsigned int> base/functional/bind_internal.h:731:12
    #32 0x563da6fbde6a in MakeItSo<void (Connector::*const &)(const char *, unsigned int), const std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<const char, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, unsigned int> base/functional/bind_internal.h:923:12
    #33 0x563da6fbde6a in RunImpl<void (Connector::*const &)(const char *, unsigned int), const std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<const char, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, 0UL, 1UL> base/functional/bind_internal.h:1060:14
    #34 0x563da6fbde6a in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int) base/functional/bind_internal.h:980:12
    #35 0x563d95efbace in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const & base/functional/callback.h:344:12
    #36 0x563d95efb85f in Invoke<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &> base/functional/bind_internal.h:664:12
    #37 0x563d95efb85f in MakeItSo<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, unsigned int, const mojo::HandleSignalsState &> base/functional/bind_internal.h:923:12
    #38 0x563d95efb85f in RunImpl<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, 0UL> base/functional/bind_internal.h:1060:14
    #39 0x563d95efb85f in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> >, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&) base/functional/bind_internal.h:980:12
    #40 0x563da7d41b40 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const & base/functional/callback.h:344:12
    #41 0x563da7d41478 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple_watcher.cc:278:14
    #42 0x563da7d426ad in Invoke<void (SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), const base::WeakPtr<mojo::SimpleWatcher> &, int, unsigned int, mojo::HandleSignalsState> base/functional/bind_internal.h:731:12
    #43 0x563da7d426ad in MakeItSo<void (SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> > base/functional/bind_internal.h:947:5
    #44 0x563da7d426ad in RunImpl<void (SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0UL, 1UL, 2UL, 3UL> base/functional/bind_internal.h:1060:14
    #45 0x563da7d426ad in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:973:12
    #46 0x563da71eee06 in Run base/functional/callback.h:156:12
    #47 0x563da71eee06 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:207:34
    #48 0x563da7261537 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:458:11)> base/task/common/task_annotator.h:104:5
    #49 0x563da7261537 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:456:23
    #50 0x563da726041c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:330:40
    #51 0x563da726202a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #52 0x563da73efde8 in base::MessagePumpGlib::HandleDispatch() base/message_loop/message_pump_glib.cc:656:46
    #53 0x563da73f31c8 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:275:43
    #54 0x7f386e81ae0a in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x51e0a) (BuildId: 51af3166f1370652c1f9302d6cb2509fd974c335)


==586193==ADDITIONAL INFO

==586193==Note: Please include this section with the ASan report.
Task trace:
    #0 0x563dacc48b69 in media::V4L2CaptureDelegate::DoCapture() media/capture/video/linux/v4l2_capture_delegate.cc:1191:7
    #1 0x563dacc48b69 in media::V4L2CaptureDelegate::DoCapture() media/capture/video/linux/v4l2_capture_delegate.cc:1191:7
    #2 0x563dacc48b69 in media::V4L2CaptureDelegate::DoCapture() media/capture/video/linux/v4l2_capture_delegate.cc:1191:7
    #3 0x563dacc455e0 in media::V4L2CaptureDelegate::AllocateAndStart(int, int, float, std::__Cr::unique_ptr<media::VideoCaptureDevice::Client, std::__Cr::default_delete<media::VideoCaptureDevice::Client> >) media/capture/video/linux/v4l2_capture_delegate.cc:468:7


Command line: `/proc/self/exe --type=utility --utility-sub-type=video_capture.mojom.VideoCaptureService --lang=de --service-sandbox-type=none --no-sandbox --message-loop-type-ui --crashpad-handler-pid=585873 --enable-crash-reporter=, --subproc-heap-profiling --change-stack-guard-on-fork=enable --shared-files=v8_context_snapshot_data:100 --metrics-shmem-handle=4,i,6229673590439775338,1326251627037240520,524288 --field-trial-handle=3,i,2008510889948857896,2382443360607485135,262144 --enable-features=Vulkan --variations-seed-version`


==586193==END OF ADDITIONAL INFO
==586193==ABORTING

```

The memcpy-param-overlap error probably occurs because the smaller destination buffer was allocated directly next to the larger source buffer, which would also explain why the error is silent without ASAN Chrome.

### Bisect

Apparently, this vulnerability has been present since the feature was introduced in 2016 (I did not test it with the 2016 version though).
<https://source.chromium.org/chromium/chromium/src/+/198b050b9fe647bf3799ab75df07b888c7adcf50:media/capture/video/video_capture_device_client.cc;dlc=a6257d62eb21b0e308dbccc8ac45c4f15160f5d8>

### Suggested Patch

Copy row-by-row using the width excluding padding as copy size, or resize the destination buffer to include padding (that might require changes in the logic that later processes this destination buffer though), or reject padding altogether (which would break the feature for all devices / drivers / configurations that use padding though).

#### Impact analysis – Please briefly explain who can exploit the vulnerability, and what they gain when doing so

This vulnerability can be triggered from the web by an attacker against victims that have a Y16 camera (which Chrome must have permission to access) available on their computer, if that camera and its driver have at least one configuration that uses padding. No further user interaction is required (it is not necessary that the user allows camera access for the attacker website, because the vulnerability gets already triggered in the preview when Chrome asks the user to allow access to the camera). The possible impact is a buffer overflow in the shared memory region in the video capture process, which is unsandboxed on Linux and Windows. A memory corruption in this process could theoretically result in a full sandbox escape RCE, if an attacker somehow manages to control the data returned by the camera, and other mitigations and problems typical for memory corruption exploitation can be bypassed / solved (ASLR, memory layout, heap metadata corruption protection).

---

### The cause

#### What version of Chrome have you found the security issue in?

Windows: 140.0.7339.128 (Official Build) (64-bit) (cohort: Stable), Linux: 140.0.7339.127 (stable official ASAN build)

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a non-sandboxed process)

#### How would you like to be publicly acknowledged for your report?

Elias Hohl

## Attachments

- [y16_auto_final.html](attachments/y16_auto_final.html) (text/html, 1.4 KB)
- [vivid.zip](attachments/vivid.zip) (application/zip, 109.4 KB)
- [processname_chrome_y16.png](attachments/processname_chrome_y16.png) (image/png, 172.5 KB)
- [chrome_y16_camera_access_violation.png](attachments/chrome_y16_camera_access_violation.png) (image/png, 397.5 KB)
- [chrome_y16_access_violation_2.png](attachments/chrome_y16_access_violation_2.png) (image/png, 364.6 KB)
- [VCamSample.zip](attachments/VCamSample.zip) (application/zip, 91.5 KB)
- [y16_auto_final.html](attachments/y16_auto_final.html) (text/html, 1.4 KB)
- [vivid.zip](attachments/vivid.zip) (application/zip, 109.4 KB)
- [VCamSample.zip](attachments/VCamSample.zip) (application/zip, 91.5 KB)
- [vivid_y16_padding_after_each_row.patch](attachments/vivid_y16_padding_after_each_row.patch) (text/x-diff, 4.7 KB)

## Timeline

### el...@cryptosearch.tools (2025-09-13)

I realized I did not use the correct version of the symbols for the Linux ASAN trace, so I am sending you an updated Linux ASAN trace below (it is almost identical to the original Linux ASAN trace).

```
=================================================================
==707455==ERROR: AddressSanitizer: memcpy-param-overlap: memory ranges [0x7b738bf6a000,0x7b738c034800) and [0x7b738c031000, 0x7b738c0fb800) overlap
    #0 0x560531b3d219 in __asan_memcpy (/home/elias/chromium-exploits/asanchrome-new/chrome+0xff44219) (BuildId: 751dffbb7e8a9303)
    #1 0x56054d23a4fc in media::VideoCaptureDeviceClient::OnIncomingCapturedY16Data(unsigned char const*, int, media::VideoCaptureFormat const&, base::TimeTicks, base::TimeDelta, std::__Cr::optional<base::TimeTicks>, std::__Cr::optional<media::VideoFrameMetadata> const&, int) media/capture/video/video_capture_device_client.cc:1109:3
    #2 0x56054d23942e in media::VideoCaptureDeviceClient::OnIncomingCapturedData(unsigned char const*, int, media::VideoCaptureFormat const&, gfx::ColorSpace const&, int, bool, base::TimeTicks, base::TimeDelta, std::__Cr::optional<base::TimeTicks>, std::__Cr::optional<media::VideoFrameMetadata> const&, int) media/capture/video/video_capture_device_client.cc:533:12
    #3 0x560535721093 in media::VideoCaptureDevice::Client::OnIncomingCapturedData(unsigned char const*, int, media::VideoCaptureFormat const&, gfx::ColorSpace const&, int, bool, base::TimeTicks, base::TimeDelta, std::__Cr::optional<base::TimeTicks>, std::__Cr::optional<media::VideoFrameMetadata> const&) media/capture/video/video_capture_device.cc:96:3
    #4 0x56054d25f7f3 in media::V4L2CaptureDelegate::DoCapture() media/capture/video/linux/v4l2_capture_delegate.cc:1164:18
    #5 0x56054d268144 in Invoke<void (V4L2CaptureDelegate::*)(), const base::WeakPtr<media::V4L2CaptureDelegate> &> base/functional/bind_internal.h:731:12
    #6 0x56054d268144 in MakeItSo<void (V4L2CaptureDelegate::*)(), std::__Cr::tuple<base::WeakPtr<media::V4L2CaptureDelegate> > > base/functional/bind_internal.h:947:5
    #7 0x56054d268144 in RunImpl<void (V4L2CaptureDelegate::*)(), std::__Cr::tuple<base::WeakPtr<media::V4L2CaptureDelegate> >, 0UL> base/functional/bind_internal.h:1060:14
    #8 0x56054d268144 in base::internal::Invoker<base::internal::FunctorTraits<void (media::V4L2CaptureDelegate::*&&)(), base::WeakPtr<media::V4L2CaptureDelegate>&&>, base::internal::BindState<true, true, false, void (media::V4L2CaptureDelegate::*)(), base::WeakPtr<media::V4L2CaptureDelegate> >, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:973:12
    #9 0x560547804e06 in Run base/functional/callback.h:156:12
    #10 0x560547804e06 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:207:34
    #11 0x56054789c3ba in RunTask<(lambda at ../../base/task/thread_pool/task_tracker.cc:687:35)> base/task/common/task_annotator.h:104:5
    #12 0x56054789c3ba in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) base/task/thread_pool/task_tracker.cc:686:19
    #13 0x56054789c60c in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) base/task/thread_pool/task_tracker.cc:671:3
    #14 0x56054789ac14 in RunTaskWithShutdownBehavior base/task/thread_pool/task_tracker.cc:701:7
    #15 0x56054789ac14 in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&) base/task/thread_pool/task_tracker.cc:501:5
    #16 0x560547899c74 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource) base/task/thread_pool/task_tracker.cc:391:5
    #17 0x5605478dadd3 in base::internal::WorkerThread::RunWorker() base/task/thread_pool/worker_thread.cc:473:36
    #18 0x5605478da167 in base::internal::WorkerThread::RunDedicatedWorker() base/task/thread_pool/worker_thread.cc:379:3
    #19 0x5605478d98e9 in base::internal::WorkerThread::ThreadMain() base/task/thread_pool/worker_thread.cc:345:7
    #20 0x56054795662e in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:101:13
    #21 0x560531b3cfd6 in asan_thread_start(void*) (/home/elias/chromium-exploits/asanchrome-new/chrome+0xff43fd6) (BuildId: 751dffbb7e8a9303)

Address 0x7b738bf6a000 is a wild pointer inside of access range of size 0x0000000ca800.
Address 0x7b738c031000 is a wild pointer inside of access range of size 0x0000000ca800.
SUMMARY: AddressSanitizer: memcpy-param-overlap (/home/elias/chromium-exploits/asanchrome-new/chrome+0xff44219) (BuildId: 751dffbb7e8a9303) in __asan_memcpy
Thread T7 (ThreadPoolSingl) created by T0 (chrome) here:
    #0 0x560531b238c1 in pthread_create (/home/elias/chromium-exploits/asanchrome-new/chrome+0xff2a8c1) (BuildId: 751dffbb7e8a9303)
    #1 0x560547955c18 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) base/threading/platform_thread_posix.cc:149:13
    #2 0x5605478d86b8 in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*) base/task/thread_pool/worker_thread.cc:185:3
    #3 0x5605478bb2ee in CreateTaskRunnerImpl<base::internal::(anonymous namespace)::WorkerThreadDelegate> base/task/thread_pool/pooled_single_thread_task_runner_manager.cc:749:13
    #4 0x5605478bb2ee in base::internal::PooledSingleThreadTaskRunnerManager::CreateSingleThreadTaskRunner(base::TaskTraits const&, base::SingleThreadTaskRunnerThreadMode) base/task/thread_pool/pooled_single_thread_task_runner_manager.cc:685:10
    #5 0x56054d255cfb in media::VideoCaptureDeviceLinux::VideoCaptureDeviceLinux(scoped_refptr<media::V4L2CaptureDevice>, media::VideoCaptureDeviceDescriptor const&) media/capture/video/linux/video_capture_device_linux.cc:61:20
    #6 0x56054d24f180 in make_unique<media::VideoCaptureDeviceLinux, media::V4L2CaptureDevice *, const media::VideoCaptureDeviceDescriptor &, 0> third_party/libc++/src/include/__memory/unique_ptr.h:759:30
    #7 0x56054d24f180 in media::VideoCaptureDeviceFactoryV4L2::CreateDevice(media::VideoCaptureDeviceDescriptor const&) media/capture/video/linux/video_capture_device_factory_v4l2.cc:148:7
    #8 0x56054d24d2b6 in media::VideoCaptureDeviceFactoryLinux::CreateDevice(media::VideoCaptureDeviceDescriptor const&) media/capture/video/linux/video_capture_device_factory_linux.cc
    #9 0x56054d24354c in media::VideoCaptureSystemImpl::CreateDevice(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&) media/capture/video/video_capture_system_impl.cc:112:20
    #10 0x56053f4e4088 in video_capture::DeviceFactoryImpl::CreateAndAddNewDevice(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, base::OnceCallback<void (video_capture::DeviceFactory::DeviceInfo)>) services/video_capture/device_factory_impl.cc:181:24
    #11 0x56053f4e51e5 in Invoke<void (DeviceFactoryImpl::*)(const std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > &, base::OnceCallback<void (video_capture::DeviceFactory::DeviceInfo)>), const base::WeakPtr<video_capture::DeviceFactoryImpl> &, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >, base::OnceCallback<void (video_capture::DeviceFactory::DeviceInfo)> > base/functional/bind_internal.h:731:12
    #12 0x56053f4e51e5 in MakeItSo<void (DeviceFactoryImpl::*)(const std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > &, base::OnceCallback<void (video_capture::DeviceFactory::DeviceInfo)>), std::__Cr::tuple<base::WeakPtr<video_capture::DeviceFactoryImpl>, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >, base::OnceCallback<void (video_capture::DeviceFactory::DeviceInfo)> > > base/functional/bind_internal.h:947:5
    #13 0x56053f4e51e5 in RunImpl<void (DeviceFactoryImpl::*)(const std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > &, base::OnceCallback<void (video_capture::DeviceFactory::DeviceInfo)>), std::__Cr::tuple<base::WeakPtr<video_capture::DeviceFactoryImpl>, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >, base::OnceCallback<void (video_capture::DeviceFactory::DeviceInfo)> >, 0UL, 1UL, 2UL> base/functional/bind_internal.h:1060:14
    #14 0x56053f4e51e5 in base::internal::Invoker<base::internal::FunctorTraits<void (video_capture::DeviceFactoryImpl::*&&)(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, base::OnceCallback<void (video_capture::DeviceFactory::DeviceInfo)>), base::WeakPtr<video_capture::DeviceFactoryImpl>&&, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >&&, base::OnceCallback<void (video_capture::DeviceFactory::DeviceInfo)>&&>, base::internal::BindState<true, true, false, void (video_capture::DeviceFactoryImpl::*)(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, base::OnceCallback<void (video_capture::DeviceFactory::DeviceInfo)>), base::WeakPtr<video_capture::DeviceFactoryImpl>, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >, base::OnceCallback<void (video_capture::DeviceFactory::DeviceInfo)> >, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:973:12
    #15 0x56053f4e3c5c in Run base/functional/callback.h:156:12
    #16 0x56053f4e3c5c in video_capture::DeviceFactoryImpl::CreateDevice(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, base::OnceCallback<void (video_capture::DeviceFactory::DeviceInfo)>) services/video_capture/device_factory_impl.cc:135:45
    #17 0x56053f51228d in video_capture::VirtualDeviceEnabledDeviceFactory::CreateDevice(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, base::OnceCallback<void (video_capture::DeviceFactory::DeviceInfo)>) services/video_capture/virtual_device_enabled_device_factory.cc:153:27
    #18 0x56053f5085dc in video_capture::VideoSourceImpl::StartDeviceWithSettings(media::VideoCaptureParams const&) services/video_capture/video_source_impl.cc:134:20
    #19 0x56053f50789e in video_capture::VideoSourceImpl::CreatePushSubscription(mojo::PendingRemote<video_capture::mojom::VideoFrameHandler>, media::VideoCaptureParams const&, bool, mojo::PendingReceiver<video_capture::mojom::PushVideoStreamSubscription>, base::OnceCallback<void (mojo::InlinedStructPtr<video_capture::mojom::CreatePushSubscriptionResultCode>, media::VideoCaptureParams const&)>) services/video_capture/video_source_impl.cc:63:7
    #20 0x56053576f074 in video_capture::mojom::VideoSourceStubDispatch::AcceptWithResponder(video_capture::mojom::VideoSource*, mojo::Message*, std::__Cr::unique_ptr<mojo::MessageReceiverWithStatus, std::__Cr::default_delete<mojo::MessageReceiverWithStatus> >) gen/services/video_capture/public/mojom/video_source.mojom.cc:2020:13
    #21 0x5605475da330 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1013:56
    #22 0x5605475f7c1d in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:48:24
    #23 0x5605475dff74 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:731:20
    #24 0x560547607b3a in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:1120:42
    #25 0x560547606046 in mojo::internal::MultiplexRouter::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/multiplex_router.cc:733:7
    #26 0x5605475f7d1a in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #27 0x5605475d0e22 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) mojo/public/cpp/bindings/lib/connector.cc:561:49
    #28 0x5605475d25c0 in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:619:14
    #29 0x5605475d1fe9 in OnHandleReadyInternal mojo/public/cpp/bindings/lib/connector.cc:450:3
    #30 0x5605475d1fe9 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int) mojo/public/cpp/bindings/lib/connector.cc:416:3
    #31 0x5605475d3e6a in Invoke<void (Connector::*)(const char *, unsigned int), mojo::Connector *, const char *, unsigned int> base/functional/bind_internal.h:731:12
    #32 0x5605475d3e6a in MakeItSo<void (Connector::*const &)(const char *, unsigned int), const std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<const char, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, unsigned int> base/functional/bind_internal.h:923:12
    #33 0x5605475d3e6a in RunImpl<void (Connector::*const &)(const char *, unsigned int), const std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<const char, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, 0UL, 1UL> base/functional/bind_internal.h:1060:14
    #34 0x5605475d3e6a in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int) base/functional/bind_internal.h:980:12
    #35 0x560536511ace in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const & base/functional/callback.h:344:12
    #36 0x56053651185f in Invoke<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &> base/functional/bind_internal.h:664:12
    #37 0x56053651185f in MakeItSo<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, unsigned int, const mojo::HandleSignalsState &> base/functional/bind_internal.h:923:12
    #38 0x56053651185f in RunImpl<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, 0UL> base/functional/bind_internal.h:1060:14
    #39 0x56053651185f in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> >, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&) base/functional/bind_internal.h:980:12
    #40 0x560548357b40 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const & base/functional/callback.h:344:12
    #41 0x560548357478 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple_watcher.cc:278:14
    #42 0x5605483586ad in Invoke<void (SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), const base::WeakPtr<mojo::SimpleWatcher> &, int, unsigned int, mojo::HandleSignalsState> base/functional/bind_internal.h:731:12
    #43 0x5605483586ad in MakeItSo<void (SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> > base/functional/bind_internal.h:947:5
    #44 0x5605483586ad in RunImpl<void (SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0UL, 1UL, 2UL, 3UL> base/functional/bind_internal.h:1060:14
    #45 0x5605483586ad in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:973:12
    #46 0x560547804e06 in Run base/functional/callback.h:156:12
    #47 0x560547804e06 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:207:34
    #48 0x560547877537 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:458:11)> base/task/common/task_annotator.h:104:5
    #49 0x560547877537 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:456:23
    #50 0x56054787641c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:330:40
    #51 0x56054787802a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #52 0x560547a06744 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:702:48
    #53 0x560547878be4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:629:12
    #54 0x560547783bff in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14
    #55 0x560541826056 in content::UtilityMain(content::MainFunctionParams) content/utility/utility_main.cc:506:12
    #56 0x560543e52aa9 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:763:14
    #57 0x560543e555b3 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1129:10
    #58 0x560543e4f8de in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:361:36
    #59 0x560543e4fe0b in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:374:10
    #60 0x560531b7a277 in ChromeMain chrome/app/chrome_main.cc:222:12
    #61 0x7f739ba59d79 in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x23d79) (BuildId: a727537547829074887adbdd56624e44bb0011bb)


==707455==ADDITIONAL INFO

==707455==Note: Please include this section with the ASan report.
Task trace:
    #0 0x56054d25eb69 in media::V4L2CaptureDelegate::DoCapture() media/capture/video/linux/v4l2_capture_delegate.cc:1191:7
    #1 0x56054d25eb69 in media::V4L2CaptureDelegate::DoCapture() media/capture/video/linux/v4l2_capture_delegate.cc:1191:7
    #2 0x56054d25eb69 in media::V4L2CaptureDelegate::DoCapture() media/capture/video/linux/v4l2_capture_delegate.cc:1191:7
    #3 0x56054d25b5e0 in media::V4L2CaptureDelegate::AllocateAndStart(int, int, float, std::__Cr::unique_ptr<media::VideoCaptureDevice::Client, std::__Cr::default_delete<media::VideoCaptureDevice::Client> >) media/capture/video/linux/v4l2_capture_delegate.cc:468:7


Command line: `/proc/self/exe --type=utility --utility-sub-type=video_capture.mojom.VideoCaptureService --lang=de --service-sandbox-type=none --no-sandbox --message-loop-type-ui --crashpad-handler-pid=707232 --enable-crash-reporter=, --subproc-heap-profiling --change-stack-guard-on-fork=enable --shared-files=v8_context_snapshot_data:100 --metrics-shmem-handle=4,i,16962954098460712124,6132244070057152194,524288 --field-trial-handle=3,i,4666661224000360426,16348132831561574091,262144 --enable-features=Vulkan --variations-seed-version`


==707455==END OF ADDITIONAL INFO
==707455==ABORTING

```

### mp...@google.com (2025-09-15)

We can't really unzip drivers and install them due to security concerns; even on VMs that is discouraged. Do you think you could provide a diff of the vivid driver?

Why would Y16 contain padding bytes? Are there any configurations on Windows or linux where this would be the case?

It does seem like it'd be safest to do a CHECK\_EQ that we are memcpying with the correct length, the CHECK\_GE definitely seems strange to me. I will CC some OWNERS.

### pe...@google.com (2025-09-16)

The NextAction date has arrived: 2025-09-16
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### el...@cryptosearch.tools (2025-09-16)

Here is the vivid patch

### pe...@google.com (2025-09-16)

Thank you for providing more feedback. Adding the requester to the CC list.

### el...@cryptosearch.tools (2025-09-16)

Regarding your other questions - to be honest, I am not an expert on camera drivers and I don't want to give you any wrong information. It seems that padding to multiples of a power of 2 is sometimes done due to hardware requirements or for efficieny reasons. However, it was not so easy for me to find public information regarding the padding behavior Y16 cameras and drivers. However, the NVIDIA Jetson V4L2 camera driver uses 64 byte alignment, according to the information I found:

<https://forums.developer.nvidia.com/t/how-to-safely-change-stride-alignment/202677>

<https://forums.developer.nvidia.com/t/stride-alignment-problem-when-capture-720x288-50-video-with-csi/66577>

Apparently, this driver needs to be patched to support Y16: <https://forums.developer.nvidia.com/t/support-for-y16-format/112135>

The fact that there is a comment in the code acknowledging that there might be the padding also supports the idea that this can actually be the case for Y16 cameras. In the case of alignment padding, multiple conditions need to be met for the vulnerable code path to be used though:

1. Chrome must decide to use the Y16 pixel format. If the camera also advertises other formats, it might prefer another one (this cannot be controlled from JS, there is a preference logic implemented).
2. The driver must return padding to Chrome that is aligned to some number of bytes per row, most likely a power of 2
3. The camera must support a width that is not already a multiple of the power of two to which the driver aligns

It might be possible that padding is added for another reason than alignment, for example, extra rows for telemetry data, but according to what I found, these extra rows usually need to be specifically requested by increasing the requested height by the number of telemetry rows.

Maybe someone in the Chromium team knows more. I will also try to find additional information within the next days, maybe I will find information that confirms a specific camera model / driver / resolution combination triggers the vulnerability.

### es...@chromium.org (2025-09-17)

Tentatively triaging as High severity and assigning to a media/capture/video OWNER, but it seems unclear whether this is actually realistically exploitable or not.

### ch...@google.com (2025-09-17)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-09-17)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### hb...@chromium.org (2025-09-18)

Ilya is OOO for two weeks so I can take a stab at it. It's also not clear to me how exploitable this is, but we should never memcpy with wrong lengths like that.

This should fix the issue, right? The only data not copied in cases where the lengths differ would be the "unnecessary" padding, if I understand correctly.

```
- memcpy(buffer_access->data(), data, length);
+ memcpy(buffer_access->data(), data,
+        std::min(static_cast<size_t>(length), buffer_access->mapped_size()));

```

CL here: <https://chromium-review.googlesource.com/c/chromium/src/+/6965575>

### el...@cryptosearch.tools (2025-09-18)

This should fix the vulnerability, but according to my understanding, the padding can be in between rows if row alignment is creating the padding, and this code is copying everything at once, meaning the fix might cut of actual data and include padding in the copied data. I believe the correct fix would be to loop over the image height and copy width \* bytes\_per\_pixel every time into the destination buffer, while considering the bytes per line reported by the driver to understand how many bytes of padding need to be skipped after each iteration

### hb...@chromium.org (2025-09-18)

Makes sense, so improvements are possible in this area. In the meantime since I don't have a Y16 video camera to test with and it's not clear how common this would be in the wild, I say we merge the immediate bug fix and then revisit this.

### dx...@google.com (2025-09-19)

Project: chromium/src  

Branch:  main  

Author:  Henrik Boström [hbos@chromium.org](mailto:hbos@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6965575>

Fix copy operation inside OnIncomingCapturedY16Data.

---


Expand for full commit details
```
     
    See issue description for details. 
     
    Bug: chromium:444755026 
    Change-Id: If6388a472e837240f6c3eae5c2b8960af93037bf 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6965575 
    Auto-Submit: Henrik Boström <hbos@chromium.org> 
    Reviewed-by: Guido Urdaneta <guidou@chromium.org> 
    Commit-Queue: Henrik Boström <hbos@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1517794}

```

---

Files:

- M `media/capture/video/video_capture_device_client.cc`

---

Hash: [8f2cf429ca3090d84c767aa3eddb1e9c3aa57671](https://chromiumdash.appspot.com/commit/8f2cf429ca3090d84c767aa3eddb1e9c3aa57671)  

Date: Fri Sep 19 08:34:03 2025


---

### hb...@chromium.org (2025-09-19)

OK so the security issue has been Fixed, but there are some possible follow-ups that I'll track separately to avoid a Security issue being open:

1. Dale suggested VideoCaptureBufferHandle is modernized to use spans: <https://crbug.com/445967240>
2. As per [comment #12](https://issues.chromium.org/issues/444755026#comment12), we should copy by "width \* bytes\_per\_pixel" instead: <https://crbug.com/445967239>

### ch...@google.com (2025-09-19)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M140. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M141. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
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

### hb...@chromium.org (2025-09-22)

The fix CL is linked to in [comment #14](https://issues.chromium.org/issues/444755026#comment14), it's <https://chromium-review.googlesource.com/c/chromium/src/+/6965575>

The fix has reached Canary 142.0.7423.0, see <https://chromiumdash.appspot.com/commit/8f2cf429ca3090d84c767aa3eddb1e9c3aa57671>. In terms of verifying the fix, firstly I don't have a Y16 pixel format camera to test with, but secondly it's unclear if this is an issue with "real" cameras or only happens with virtual cameras, see issue descriptions.

It should be safe though, the fix only prevents a memcpy operation from overflowing, so it seems rather harmless. I don't have a strong opinion about whether or not this needs to be backmerged.

### aw...@google.com (2025-09-22)

Thanks for the fix hbos@. If anybody's around to merge by 11am Pacific today, we can take it in the next M140 stable update, otherwise it will go in next week's M141 release.

### sr...@google.com (2025-09-22)

For this bug to get into m141, we need to get the merges for m141 to be completed by EOD today( Monday sept 22 ) we are cutting 141 stable RC tomorrow, so even if you miss 140, please make sure you land by EOD today

### sr...@google.com (2025-09-22)

M141 RC cut for stalbe is tomorrow , around 11am PST, this bug is approved for merge to m141 and so if you need this to make to stable releease, please help complete the merge before 11am PST tuesday sept 23. 

### mp...@google.com (2025-09-22)

I'll note that `VideoCaptureDeviceClient::OnIncomingCapturedData` has the [same comment](https://source.chromium.org/chromium/chromium/src/+/main:media/capture/video/video_capture_device_client.cc;drc=89f6321d4c72ccc4b16de1d3e700e66b878e624b;l=504) about data being bigger than the required buffer size, but it's difficult to tell if it ever reaches a similar memcpy.

### el...@cryptosearch.tools (2025-09-22)

An example of a camera that might trigger this memory corruption is e-CAM131\_CURB by e-con Systems (<https://www.e-consystems.com/raspberry-pi-4/ar1335-mipi-13mp-monochrome-camera.asp>). It supports Y16 and Y8 according to the website, which should result in Chromium choosing Y16, according to my understanding (<https://chromium.googlesource.com/chromium/src/media/%2B/refs/heads/main/capture/video/linux/v4l2_capture_delegate.cc>). Raspberry Pi 4 seems to align stride to a multiple of 32 bytes for CSI-2 cameras (<https://github.com/torvalds/linux/blob/cec1e6e5d1ab33403b809f79cd20d6aff124ccfe/drivers/media/platform/broadcom/bcm2835-unicam.c#L74-L79>, <https://forums.raspberrypi.com/viewtopic.php?t=321403>, <https://forums.raspberrypi.com/viewtopic.php?t=344556>). In the datasheet, it says that the camera supports the resolution 4200 x 3120. A width of 4200 corresponds to 8400 bytes in Y16. 8400 mod 32 = 16, so we can expect 16 bytes of padding per line.

I did not actually buy this camera and try it though.

### el...@cryptosearch.tools (2025-09-23)

A note regarding exploitability - if the overflow can be triggered with a camera that includes telemetry data into the frame, that could be a much more realistic exploitation scenario, because this metadata is much more predictable than the actual image data. In particular, timestamps and frame counters could be useful, because they are not only predictable, but can also cover a significant range of values (the attacker would just need to wait until the time / frame counter is at the desired value).

### hb...@chromium.org (2025-09-23)

Backmerges:

- <https://chromium-review.googlesource.com/c/chromium/src/+/6973462>
- <https://chromium-review.googlesource.com/c/chromium/src/+/6973568>

### hb...@chromium.org (2025-09-23)

Re [comment #22](https://issues.chromium.org/issues/444755026#comment22): interesting!

### dx...@google.com (2025-09-23)

Project: chromium/src  

Branch:  refs/branch-heads/7390  

Author:  Henrik Boström [hbos@chromium.org](mailto:hbos@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6973462>

[M141] Fix copy operation inside OnIncomingCapturedY16Data.

---


Expand for full commit details
```
     
    See issue description for details. 
     
    (cherry picked from commit 8f2cf429ca3090d84c767aa3eddb1e9c3aa57671) 
     
    Bug: chromium:444755026 
    Change-Id: If6388a472e837240f6c3eae5c2b8960af93037bf 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6965575 
    Auto-Submit: Henrik Boström <hbos@chromium.org> 
    Reviewed-by: Guido Urdaneta <guidou@chromium.org> 
    Commit-Queue: Henrik Boström <hbos@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1517794} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6973462 
    Reviewed-by: Daniel Yip <danielyip@google.com> 
    Commit-Queue: Daniel Yip <danielyip@google.com> 
    Cr-Commit-Position: refs/branch-heads/7390@{#1587} 
    Cr-Branched-From: d481efce5eb300acbb896686676ebd0352a6f1db-refs/heads/main@{#1509326}

```

---

Files:

- M `media/capture/video/video_capture_device_client.cc`

---

Hash: [8b414867504feb365650df47c435139a17cd13fd](https://chromiumdash.appspot.com/commit/8b414867504feb365650df47c435139a17cd13fd)  

Date: Tue Sep 23 12:46:54 2025


---

### pe...@google.com (2025-09-23)

LTS Milestone M138

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### hb...@chromium.org (2025-09-23)

No this appears to be old code

### dx...@google.com (2025-09-23)

Project: chromium/src  

Branch:  refs/branch-heads/7339  

Author:  Henrik Boström [hbos@chromium.org](mailto:hbos@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6973568>

[M140] Fix copy operation inside OnIncomingCapturedY16Data.

---


Expand for full commit details
```
     
    See issue description for details. 
     
    (cherry picked from commit 8f2cf429ca3090d84c767aa3eddb1e9c3aa57671) 
     
    Bug: chromium:444755026 
    Change-Id: If6388a472e837240f6c3eae5c2b8960af93037bf 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6965575 
    Auto-Submit: Henrik Boström <hbos@chromium.org> 
    Reviewed-by: Guido Urdaneta <guidou@chromium.org> 
    Commit-Queue: Henrik Boström <hbos@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1517794} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6973568 
    Reviewed-by: Daniel Yip <danielyip@google.com> 
    Commit-Queue: Daniel Yip <danielyip@google.com> 
    Cr-Commit-Position: refs/branch-heads/7339@{#2433} 
    Cr-Branched-From: 27be8b77710f4405fdfeb4ee946fcabb0f6c92b2-refs/heads/main@{#1496484}

```

---

Files:

- M `media/capture/video/video_capture_device_client.cc`

---

Hash: [6232927979f41672feabaa24dbb22a6f0a845dd6](https://chromiumdash.appspot.com/commit/6232927979f41672feabaa24dbb22a6f0a845dd6)  

Date: Tue Sep 23 17:36:06 2025


---

### el...@cryptosearch.tools (2025-09-26)

Link to Linux kernel documentation that states the driver is allowed to add padding: <https://docs.kernel.org/userspace-api/media/v4l/pixfmt-v4l2.html>

### sp...@google.com (2025-09-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $4000.00 for this report.

Rationale for this decision:
memory corruption in a sandboxed process which is mildly mitigated, with a bisect bonus


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### el...@cryptosearch.tools (2025-09-26)

Dear Chrome VRP team,

I believe the reward amount is incorrect. Please correct me if I am wrong, but according to my understanding, the overflow happens in the video capture process, which is apparently unsandboxed on Linux and Windows. The Linux ASAN stack trace shows `--service-sandbox-type=none`, and the following file also indicates that the process is unsandboxed on all platforms apart from Fuchsia: <https://source.chromium.org/chromium/chromium/src/+/main:services/video_capture/public/mojom/video_capture_service.mojom>

I am also not sure why the bug was classified as mildly mitigated. No user interaction is required, apart from opening the HTML page, as long as Chrome is not blocked on the OS level from accessing the camera (On windows, access for all cameras is apparently on by default, and can only be switched on/off for all non-Microsoft-store apps and all cameras at the same time <https://support.microsoft.com/en-us/windows/manage-app-permissions-for-a-camera-in-windows-87ebc757-1f87-7bbf-84b5-0686afb6ca6b>, <https://www.elevenforum.com/t/enable-or-disable-apps-access-to-camera-in-windows-11.17140/>, and on Linux, if you are not using Flatpak or AppArmor something like that, it cannot even be configured at all on a per-app level, according to my knowledge, because the cameras are simply accessed via `/dev/video*`, and if the user can access them, Chrome can access them too). Let me cite my original report:

*No further user interaction is required (it is not necessary that the user allows camera access for the attacker website, because the vulnerability gets already triggered in the preview when Chrome asks the user to allow access to the camera).*

Was it classified as mitigated because only systems with specific hardware are affected? I thought this does not affect the reward because your rules state:

*Conversely, we do not consider it a mitigating factor if a vulnerability applies only to a particular group of users. For instance, a Critical vulnerability is still considered Critical even if it applies only to Linux or to those users running with accessibility features enabled.*

Thank you in advance for reconsidering.

Best regards,
Elias Hohl

### el...@cryptosearch.tools (2025-09-27)

What might have caused the confusion regarding "mildly mitigated" - if the system has multiple cameras and the wrong one happens to be selected for preview, the bug indeed requires further user action (the Y16 camera must be selected from the drop-down menu). However, if the system has no other cameras apart from the Y16 camera, or if the Y16 camera is the default camera, the preview will directly open the Y16 camera and trigger the memory corruption.

On my Linux laptop, deactivating the normal camera with `sudo rmmod uvcvideo` or setting the default camera to `vivid` in chrome://settings/content/camera resulted in the bug automatically getting triggered when opening `y16_auto_final.html`.

Note that in older Chromium versions - I tested on 120.0.6099.224 (Official Build) built on Debian 11.8, running on Debian 11.11 (64-bit) - it seems like there was no camera preview, so the bug could not have been triggered automatically in these versions (clicking "Allow" on the camera popup would have been necessary).

According to my understanding of the Chrome VRP rules and severity guidelines, the reward for this bug should be up to $35000 (memory corruption in non-sandboxed process) + up to $10000 (note [2], a compromised renderer is not required) + $1000 (bisect bonus) = up to $46000 total.

<https://bughunters.google.com/about/rules/chrome-friends/5745167867576320/chrome-vulnerability-reward-program-rules>
<https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md>

If you think my reward calculation is not correct, please let me know what I misunderstood, and if you cannot reproduce the direct memory corruption trigger (without user interaction apart from opening the `y16_auto_final.html`), please also let me know.

### wf...@chromium.org (2025-09-28)

Thank you for your additional comments. We will look at this again in the next VRP panel.

### pe...@google.com (2025-09-29)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2025-09-29)

1. https://chromium-review.googlesource.com/c/chromium/src/+/6981753
2. Low - there was no conflict.
3. 140 and 141
4. Yes, this issue has existed since 2016 according to the description.

### pe...@google.com (2025-09-29)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2025-09-29)

1. https://chromium-review.googlesource.com/c/chromium/src/+/6981949
2. Low - there was no conflict.
3. 140 and 141
4. Yes, this issue has existed since 2016 according to the description.

### dx...@google.com (2025-10-02)

Project: chromium/src  

Branch:  refs/branch-heads/7204  

Author:  Henrik Boström [hbos@chromium.org](mailto:hbos@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6981753>

[M138-LTS] Fix copy operation inside OnIncomingCapturedY16Data.

---


Expand for full commit details
```
     
    See issue description for details. 
     
    (cherry picked from commit 8f2cf429ca3090d84c767aa3eddb1e9c3aa57671) 
     
    Bug: chromium:444755026 
    Change-Id: If6388a472e837240f6c3eae5c2b8960af93037bf 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6965575 
    Auto-Submit: Henrik Boström <hbos@chromium.org> 
    Reviewed-by: Guido Urdaneta <guidou@chromium.org> 
    Commit-Queue: Henrik Boström <hbos@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1517794} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6981753 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Owners-Override: Mohamed Omar <mohamedaomar@google.com> 
    Reviewed-by: Henrik Boström <hbos@chromium.org> 
    Reviewed-by: Mohamed Omar <mohamedaomar@google.com> 
    Cr-Commit-Position: refs/branch-heads/7204@{#3422} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `media/capture/video/video_capture_device_client.cc`

---

Hash: [afaa8b37eea09c11361618ac07bd0785ad994d9a](https://chromiumdash.appspot.com/commit/afaa8b37eea09c11361618ac07bd0785ad994d9a)  

Date: Thu Oct 2 07:15:24 2025


---

### dx...@google.com (2025-10-02)

Project: chromium/src  

Branch:  refs/branch-heads/6834  

Author:  Henrik Boström [hbos@chromium.org](mailto:hbos@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6981949>

[M132-LTS] Fix copy operation inside OnIncomingCapturedY16Data.

---


Expand for full commit details
```
     
    See issue description for details. 
     
    (cherry picked from commit 8f2cf429ca3090d84c767aa3eddb1e9c3aa57671) 
     
    Bug: chromium:444755026 
    Change-Id: If6388a472e837240f6c3eae5c2b8960af93037bf 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6965575 
    Auto-Submit: Henrik Boström <hbos@chromium.org> 
    Reviewed-by: Guido Urdaneta <guidou@chromium.org> 
    Commit-Queue: Henrik Boström <hbos@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1517794} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6981949 
    Reviewed-by: Mohamed Omar <mohamedaomar@google.com> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Owners-Override: Mohamed Omar <mohamedaomar@google.com> 
    Reviewed-by: Henrik Boström <hbos@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/6834@{#5654} 
    Cr-Branched-From: 47a3549fac11ee8cb7be6606001ede605b302b9f-refs/heads/main@{#1381561}

```

---

Files:

- M `media/capture/video/video_capture_device_client.cc`

---

Hash: [959f41a7f58755d4644f98a14197b5b89c0d7542](https://chromiumdash.appspot.com/commit/959f41a7f58755d4644f98a14197b5b89c0d7542)  

Date: Thu Oct 2 08:34:17 2025


---

### wf...@chromium.org (2025-10-07)

Re: #33 the panel agreed this was in an unsandboxed process and have adjusted the reward to reflect this. Thank you for raising this with us.

### sp...@google.com (2025-10-07)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $39000.00 for this report.

Rationale for this decision:
high quality report sandbox escape, from a renderer, with bisect bonus


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### el...@cryptosearch.tools (2025-10-08)

Thank you very much!!

### ch...@google.com (2025-12-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/444755026)*
