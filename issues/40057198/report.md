# Google Chrome WebRTC RTPSenderVideoFrameTransformerDelegate memory corruption vulnerability (TALOS-2021-1372)

| Field | Value |
|-------|-------|
| **Issue ID** | [40057198](https://issues.chromium.org/issues/40057198) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC>Video |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2021-09-07 |
| **Bounty** | $7,500.00 |

## Description

### Summary

A memory corruption vulnerability exists in WebRTC functionality of Google Chrome 92.0.4515.159 (Stable) and 95.0.4623.0 (Canary). A specially-crafted web page can trigger this vulnerability which ccan cause a heap buffer overflow and result in remote code execution. Victim would need to visit a malicious website to trigger this vulnerability.

### Tested Versions

Google Chrome 95.0.4623.0 (Canary)  

Google Chrome 92.0.4515.159 (Stable)

### Details

Google Chrome is a cross-platform web browser, developed by Google.

This vulnerability is in WebRTC, which is a technology that enables websites to capture/stream audio/video and other data between browsers.

While executing the attached PoC on Ubuntu 20.04 x64 / Windows 10 x64 machine with ASAN enabled, Chrome crashes inside SendVideo function from RTPSenderVideoFrameTransformerDelegate. Snippet of this function is as follows:

```
  1:  void RTPSenderVideoFrameTransformerDelegate::SendVideo(  
  2:      std::unique_ptr<TransformableFrameInterface> transformed_frame) const {  
  3:    RTC_CHECK(encoder_queue_->IsCurrent());  
  4:    MutexLock lock(&sender_lock_);  
  5:    if (!sender_)  
  6:      return;  
  7:    auto\* transformed_video_frame =  
  8:        static_cast<TransformableVideoSenderFrame\*>(transformed_frame.get());  
  9:    sender_->SendVideo(  
  10:        transformed_video_frame->GetPayloadType(),  
  11:        transformed_video_frame->GetCodecType(),  
  12:        transformed_video_frame->GetTimestamp(),  
  13:        transformed_video_frame->GetCaptureTimeMs(),  
  14:        transformed_video_frame->GetData(),  
  15:        transformed_video_frame->GetHeader(),  
  16:        transformed_video_frame->GetExpectedRetransmissionTimeMs());  
  17:  }  

```

Based on contents of the ASAN crash log, crash occurs on line 9.  

WebRTC is based on two way communication and during initialization phase of WebRTC we need to have Caller and Callee, and create Reader/Writer relationship for them.

Events required to trigger this vulnerability are convoluted and are best described step by step through javascript code.

1. The PoC creates "ReadableStream.getReader()" which is responsible for reading and locking of the stream.
2. A Promise for reading data is created. The expectation is that code inside the Promise should only be in read state.
3. However, inside this promise the PoC can actually write data using `WritableStream.getWriter()` object. This results in data that should be read being sent back into the stream with write.
4. After finishing reading loop (in which that is actually written), PoC is exchanging candidate in custom function `exchangeIceCandidates` which is a helper function to exchange ICE candidates between  
   
   two local peer connections.
5. Last step is to read messeage from sender and write it, however due to use of function "exchangeIceCandidates" we are back to the same place that is described in point 3.

This results in confusing Callee with Caller which results in a heap overflow due to constant read and writing of the same data.

With more experimentation with a modified PoC , we can show the following crash:

```
    for (let i = 0; i < 5; i++) {  
        const result = await senderReader.read();  
        senderWriter.write(result.value);  
        result.value.toString()   <—  AddressSanitizer: access-violation on unknown address 0x000000000010   
    }  

```

Execution crashes because of a NULL pointer dereference when accessing the object inside loop . This indicates that the object is deleted ahead of time inside the promise.

Next step in analyzing this issue was to try and create an object that will be equal to `result` which is contains object of `ArrayBuffer` type in dictionary `result.value.data`.  

If there are any expression statements that keep a reference to this data, for example `var x = new DataView(result.value.data)` then the crash null pointer dereference doesn't happen because ArrayBuffer object will be still alive and with reference.  

Keeping ArrayBuffer alive like this:

```
   for(let i=0;i < 5; i++) {  
       const result = awaitt senderReader.read();  
        var x = new DataView(result.value.data)  
        senderWriter.write(result.value);  
        result.value.toString()   <— Does not result in null pointer dereference because result.value.data is retained  
    }  

```

This would suggest a use-after-free like component to this issue. Therefore, with proper manipulation of streamed data (ArrayBuffer) inside Promise, this vulnerability could lead to further memory corruption and ultimately arbitrary code execution.

### Crash Information

```
Steps to reproduce:  
a) Without user interaction  
chrome.exe --no-sandbox --use-fake-ui-for-media-stream poc.html  
b) Clicking allow webcam popup  
chrome.exe --no-sandbox poc.html  

=================================================================  
==20772==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x125a0c2c1ad0 at pc 0x7ff6bae168af bp 0x00809abfe550 sp 0x00809abfe598  
READ of size 24 at 0x125a0c2c1ad0 thread T22  
==20772==WARNING: Failed to use and restart external symbolizer!  
==20772==\*\*\* WARNING: Failed to initialize DbgHelp!              \*\*\*  
==20772==\*\*\* Most likely this means that the app is already      \*\*\*  
==20772==\*\*\* using DbgHelp, possibly with incompatible flags.    \*\*\*  
==20772==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  
==20772==\*\*\* or produce wrong results.                           \*\*\*  
    #0 0x7ff6bae168ae in __asan_memcpy C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_interceptors_memintrinsics.cpp:22  
    #1 0x7ffc2f8ce464 in webrtc::RTPSenderVideoFrameTransformerDelegate::SendVideo C:\b\s\w\ir\cache\builder\src\third_party\webrtc\modules\rtp_rtcp\source\rtp_sender_video_frame_transformer_delegate.cc:159  
    #2 0x7ffc2f8cf2bb in webrtc::webrtc_new_closure_impl::ClosureTask<`lambda at ../../third_party/webrtc/modules/rtp_rtcp/source/rtp_sender_video_frame_transformer_delegate.cc:139:7'>::Run C:\b\s\w\ir\cache\builder\src\third_party\webrtc\rtc_base\task_utils\to_queued_task.h:32  
    #3 0x7ffc14d117ec in `anonymous namespace'::WebrtcTaskQueue::RunTask C:\b\s\w\ir\cache\builder\src\third_party\webrtc_overrides\task_queue_factory.cc:80  
    #4 0x7ffc14d11af2 in base::internal::Invoker<base::internal::BindState<void (\*)((anonymous namespace)::WebrtcTaskQueue \*, scoped_refptr<base::RefCountedData<bool> >, std::__1::unique_ptr<webrtc::QueuedTask,std::__1::default_delete<webrtc::QueuedTask> >),base::internal::UnretainedWrapper<(anonymous namespace)::WebrtcTaskQueue>,scoped_refptr<base::RefCountedData<bool> >,std::__1::unique_ptr<webrtc::QueuedTask,std::__1::default_delete<webrtc::QueuedTask> > >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:690  
    #5 0x7ffc1d811bda in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:178  
    #6 0x7ffc23864996 in base::internal::TaskTracker::RunSkipOnShutdown C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:663  
    #7 0x7ffc2386391e in base::internal::TaskTracker::RunTask C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:524  
    #8 0x7ffc23862c6a in base::internal::TaskTracker::RunAndPopNextTask C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:431  
    #9 0x7ffc27cf5d34 in base::internal::WorkerThread::RunWorker C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:371  
    #10 0x7ffc27cf4e3b in base::internal::WorkerThread::RunPooledWorker C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:262  
    #11 0x7ffc1d8d991f in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:121  
    #12 0x7ff6bae22373 in __asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_thread.cpp:278  
    #13 0x7ffd34087033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  
    #14 0x7ffd341c2650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)  

0x125a0c2c1ad0 is located 1968 bytes to the right of 160-byte region [0x125a0c2c1280,0x125a0c2c1320)  
allocated by thread T19 here:  
    #0 0x7ff6bae16edb in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98  
    #1 0x7ffc2fd50a2a in operator new d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:35  
    #2 0x7ffc2f7fe80c in webrtc::RtpVideoStreamReceiverFrameTransformerDelegate::TransformFrame C:\b\s\w\ir\cache\builder\src\third_party\webrtc\video\rtp_video_stream_receiver_frame_transformer_delegate.cc:96  
    #3 0x7ffc2f31ce3c in webrtc::RtpVideoStreamReceiver2::OnAssembledFrame C:\b\s\w\ir\cache\builder\src\third_party\webrtc\video\rtp_video_stream_receiver2.cc:854  
    #4 0x7ffc2f31b0ea in webrtc::RtpVideoStreamReceiver2::OnInsertedPacket C:\b\s\w\ir\cache\builder\src\third_party\webrtc\video\rtp_video_stream_receiver2.cc:763  
    #5 0x7ffc2f318526 in webrtc::RtpVideoStreamReceiver2::OnReceivedPayloadData C:\b\s\w\ir\cache\builder\src\third_party\webrtc\video\rtp_video_stream_receiver2.cc:626  
    #6 0x7ffc2f31c1e4 in webrtc::RtpVideoStreamReceiver2::ReceivePacket C:\b\s\w\ir\cache\builder\src\third_party\webrtc\video\rtp_video_stream_receiver2.cc:966  
    #7 0x7ffc2f31bc3b in webrtc::RtpVideoStreamReceiver2::OnRecoveredPacket C:\b\s\w\ir\cache\builder\src\third_party\webrtc\video\rtp_video_stream_receiver2.cc:649  
    #8 0x7ffc2f7f0789 in webrtc::UlpfecReceiverImpl::ProcessReceivedFec C:\b\s\w\ir\cache\builder\src\third_party\webrtc\modules\rtp_rtcp\source\ulpfec_receiver_impl.cc:175  
    #9 0x7ffc2f31bef1 in webrtc::RtpVideoStreamReceiver2::ReceivePacket C:\b\s\w\ir\cache\builder\src\third_party\webrtc\video\rtp_video_stream_receiver2.cc:951  
    #10 0x7ffc2f31c437 in webrtc::RtpVideoStreamReceiver2::OnRtpPacket C:\b\s\w\ir\cache\builder\src\third_party\webrtc\video\rtp_video_stream_receiver2.cc:660  
    #11 0x7ffc2f2bd188 in webrtc::RtpDemuxer::OnRtpPacket C:\b\s\w\ir\cache\builder\src\third_party\webrtc\call\rtp_demuxer.cc:249  
    #12 0x7ffc2dcf8278 in webrtc::internal::Call::DeliverRtp C:\b\s\w\ir\cache\builder\src\third_party\webrtc\call\call.cc:1593  
    #13 0x7ffc2dcf901c in webrtc::internal::Call::DeliverPacket C:\b\s\w\ir\cache\builder\src\third_party\webrtc\call\call.cc:1615  
    #14 0x7ffc2dd7f691 in webrtc::webrtc_new_closure_impl::SafetyClosureTask<`lambda at ../../third_party/webrtc/media/engine/webrtc_video_engine.cc:1720:34'>::Run C:\b\s\w\ir\cache\builder\src\third_party\webrtc\rtc_base\task_utils\to_queued_task.h:50  
    #15 0x7ffc1c1f338f in jingle_glue::JingleThreadWrapper::RunTaskQueueTask C:\b\s\w\ir\cache\builder\src\jingle\glue\thread_wrapper.cc:364  
    #16 0x7ffc1c1f4ca2 in base::internal::Invoker<base::internal::BindState<void (jingle_glue::JingleThreadWrapper::\*)(std::__1::unique_ptr<webrtc::QueuedTask,std::__1::default_delete<webrtc::QueuedTask> >),base::WeakPtr<jingle_glue::JingleThreadWrapper>,std::__1::unique_ptr<webrtc::QueuedTask,std::__1::default_delete<webrtc::QueuedTask> > >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:690  
    #17 0x7ffc1d811bda in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:178  
    #18 0x7ffc201aa342 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:360  
    #19 0x7ffc201a99a2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:260  
    #20 0x7ffc20183937 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:39  
    #21 0x7ffc201ab83e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:467  
    #22 0x7ffc1d7944d3 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134  
    #23 0x7ffc1d857d29 in base::Thread::Run C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:341  
    #24 0x7ffc1d858240 in base::Thread::ThreadMain C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:412  
    #25 0x7ffc1d8d991f in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:121  
    #26 0x7ff6bae22373 in __asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_thread.cpp:278  
    #27 0x7ffd34087033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  

Thread T22 created by T4 here:  
    #0 0x7ff6bae22dd2 in __asan_wrap_CreateThread C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_win.cpp:146  
    #1 0x7ffc1d8d8cfe in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:185  
    #2 0x7ffc27cf3d5e in base::internal::WorkerThread::Start C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:109  
    #3 0x7ffc2387d0b0 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::WorkerContainer::ForEachWorker<`lambda at ../../base/task/thread_pool/thread_group_impl.cc:185:37'> C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_group_impl.cc:153  
    #4 0x7ffc2387cbdf in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_group_impl.cc:185  
    #5 0x7ffc238763f8 in base::internal::ThreadGroupImpl::WorkerThreadDelegateImpl::GetWork C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_group_impl.cc:600  
    #6 0x7ffc27cf5c9d in base::internal::WorkerThread::RunWorker C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:354  
    #7 0x7ffc27cf4e3b in base::internal::WorkerThread::RunPooledWorker C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:262  
    #8 0x7ffc1d8d991f in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:121  
    #9 0x7ff6bae22373 in __asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_thread.cpp:278  
    #10 0x7ffd34087033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  
    #11 0x7ffd341c2650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)  

Thread T4 created by T0 here:  
    #0 0x7ff6bae22dd2 in __asan_wrap_CreateThread C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_win.cpp:146  
    #1 0x7ffc1d8d8cfe in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:185  
    #2 0x7ffc27cf3d5e in base::internal::WorkerThread::Start C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:109  
    #3 0x7ffc2387d0b0 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::WorkerContainer::ForEachWorker<`lambda at ../../base/task/thread_pool/thread_group_impl.cc:185:37'> C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_group_impl.cc:153  
    #4 0x7ffc2387cbdf in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_group_impl.cc:185  
    #5 0x7ffc2387451e in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::~ScopedCommandsExecutor C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_group_impl.cc:104  
    #6 0x7ffc2387394a in base::internal::ThreadGroupImpl::Start C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_group_impl.cc:429  
    #7 0x7ffc201b6545 in base::internal::ThreadPoolImpl::Start C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_pool_impl.cc:231  
    #8 0x7ffc1faaa7f2 in content::ChildProcess::ChildProcess C:\b\s\w\ir\cache\builder\src\content\child\child_process.cc:80  
    #9 0x7ffc267cdf37 in content::RenderProcess::RenderProcess C:\b\s\w\ir\cache\builder\src\content\renderer\render_process.cc:28  
    #10 0x7ffc2290745a in content::RenderProcessImpl::RenderProcessImpl C:\b\s\w\ir\cache\builder\src\content\renderer\render_process_impl.cc:96  
    #11 0x7ffc22908069 in content::RenderProcessImpl::Create C:\b\s\w\ir\cache\builder\src\content\renderer\render_process_impl.cc:295  
    #12 0x7ffc1fcc39fa in content::RendererMain C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:209  
    #13 0x7ffc195fa869 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:973  
    #14 0x7ffc195f7282 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:390  
    #15 0x7ffc195f8306 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:418  
    #16 0x7ffc131a148c in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:172  
    #17 0x7ff6bad75b74 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:169  
    #18 0x7ff6bad72be8 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:382  
    #19 0x7ff6bb1659af in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288  
    #20 0x7ffd34087033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  
    #21 0x7ffd341c2650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)  

Thread T19 created by T0 here:  
    #0 0x7ff6bae22dd2 in __asan_wrap_CreateThread C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_win.cpp:146  
    #1 0x7ffc1d8d8cfe in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:185  
    #2 0x7ffc1d856f4d in base::Thread::StartWithOptions C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:216  
    #3 0x7ffc1d856708 in base::Thread::Start C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:168  
    #4 0x7ffc2bd2f5dd in blink::PeerConnectionDependencyFactory::CreatePeerConnectionFactory C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\peerconnection\peer_connection_dependency_factory.cc:391  
    #5 0x7ffc2bd2f1ca in blink::PeerConnectionDependencyFactory::GetPcFactory C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\peerconnection\peer_connection_dependency_factory.cc:378  
    #6 0x7ffc2bd3445a in blink::PeerConnectionDependencyFactory::CreatePeerConnection C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\peerconnection\peer_connection_dependency_factory.cc:585  
    #7 0x7ffc2cb1562b in blink::RTCPeerConnectionHandler::Initialize C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\peerconnection\rtc_peer_connection_handler.cc:1185  
    #8 0x7ffc2ef89b32 in blink::RTCPeerConnection::RTCPeerConnection C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\peerconnection\rtc_peer_connection.cc:848  
    #9 0x7ffc2efb63cf in cppgc::MakeGarbageCollectedTrait<blink::RTCPeerConnection>::Call<blink::ExecutionContext \*&,webrtc::PeerConnectionInterface::RTCConfiguration,bool,bool,bool,blink::MediaConstraints &,blink::ExceptionState &> C:\b\s\w\ir\cache\builder\src\v8\include\cppgc\allocation.h:174  
    #10 0x7ffc2ef88c64 in blink::MakeGarbageCollected<blink::RTCPeerConnection,blink::ExecutionContext \*&,webrtc::PeerConnectionInterface::RTCConfiguration,bool,bool,bool,blink::MediaConstraints &,blink::ExceptionState &> C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\heap\v8_wrapper\heap.h:26  
    #11 0x7ffc2ef84ca9 in blink::RTCPeerConnection::Create C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\peerconnection\rtc_peer_connection.cc:737  
    #12 0x7ffc2ef88fd1 in blink::RTCPeerConnection::Create C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\peerconnection\rtc_peer_connection.cc:782  
    #13 0x7ffc2e3deda5 in blink::`anonymous namespace'::v8_rtc_peer_connection::ConstructorCallback C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\bindings\modules\v8\v8_rtc_peer_connection.cc:649  
    #14 0x7ffc1978de03 in v8::internal::FunctionCallbackArguments::Call C:\b\s\w\ir\cache\builder\src\v8\src\api\api-arguments-inl.h:152  
    #15 0x7ffc19789f9d in v8::internal::`anonymous namespace'::HandleApiCallHelper<1> C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:112  
    #16 0x7ffc197884cb in v8::internal::Builtin_Impl_HandleApiCall C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:138  
    #17 0x7ffc1978788e in v8::internal::Builtin_HandleApiCall C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:130  
    #18 0x7eb5000bdffb  (<unknown module>)  

SUMMARY: AddressSanitizer: heap-buffer-overflow C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_interceptors_memintrinsics.cpp:22 in __asan_memcpy  
Shadow bytes around the buggy address:  
  0x04894dad8300: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  
  0x04894dad8310: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  
  0x04894dad8320: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  
  0x04894dad8330: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  
  0x04894dad8340: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  
=>0x04894dad8350: fa fa fa fa fa fa fa fa fa fa[fa]fa fa fa fa fa  
  0x04894dad8360: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  
  0x04894dad8370: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  
  0x04894dad8380: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  
  0x04894dad8390: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  
  0x04894dad83a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  
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
==20772==ABORTING  

```

**For graphics-related bugs, please copy/paste the contents of the about:gpu**  

**page at the end of this report.**

## Attachments

- [poc.zip](attachments/poc.zip) (application/octet-stream, 42.8 KB)
- [TALOS-2021-1372 - Google_Chrome_WebRTC_RTPSenderVideoFrameTransformerDelegate_memory_corruption_vulnerability.txt](attachments/TALOS-2021-1372 - Google_Chrome_WebRTC_RTPSenderVideoFrameTransformerDelegate_memory_corruption_vulnerability.txt) (text/plain, 23.3 KB)
- [poc.html](attachments/poc.html) (text/plain, 1.7 KB)

## Timeline

### dt...@chromium.org (2021-09-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-09-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6064678521077760.

### ad...@google.com (2021-09-08)

I was able to reproduce this on Redshell, ASAN linux release 902206, using ./chrome --no-sandbox --use-fake-ui-for-media-stream --use-fake-device-for-media-stream  http://localhost:8080/poc.html.  ** NOTE THE ADDITIONAL COMMAND LINE ARGUMENT required for a reproduction environment without a real camera.

902206 = ~M93.
Renderer memory corruption => high severity.

I'll have another crack at getting ClusterFuzz to reproduce this (with the additional flag) so that we get the benefits of auto-bisection and so forth.

### [Deleted User] (2021-09-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-09-08)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6087373774192640.

### ad...@google.com (2021-09-08)

[Empty comment from Monorail migration]

[Monorail components: Blink>WebRTC>Video]

### [Deleted User] (2021-09-08)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@chromium.org (2021-09-08)

I have switched teams, I think this area is now owned by Fredrik's team. Fredrik, can you please help find an appropriate owner for this bug? Thank you.

### so...@google.com (2021-09-09)

[Empty comment from Monorail migration]

### to...@chromium.org (2021-09-10)

At least part of this bug is caused by a TransformableFrameInterface* pointing to an TransformableVideoReceiverFrame but being accidentally cast to a TransformableVideoSenderFrame* in RTPSenderVideoFrameTransformerDelegate::SendVideo.

I'm working on exposing the actual Receiver/Sender types in the WebRTC interface and then making an actual check in the Insertable Streams JS interface that an RTCEncodedVideoFrame object written to a writeable references the correct WebRTC type.

### [Deleted User] (2021-09-10)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-27)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/8fb41a39e1a2d151d1c00c409630dcee80adeb76

commit 8fb41a39e1a2d151d1c00c409630dcee80adeb76
Author: Tony Herre <toprice@chromium.org>
Date: Fri Sep 24 12:05:20 2021

Add Direction indicator to TransformableFrames

Currently the implementation of FrameTransformers uses distinct,
incompatible types for recevied vs about-to-be-sent frames. This adds a
flag in the interface so we can at least check that we are being given
the correct type. crbug.com/1250638 tracks removing the need for this.

Chrome will be updated after this to check the direction flag and provide
a javascript error if the wrong type of frame is written into the
encoded insertable streams writable stream, rather than crashing.

Bug: chromium:1247260
Change-Id: I9cbb66962ea0718ed47c5e5dba19a8ff9635b0b1
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/232301
Reviewed-by: Harald Alvestrand <hta@webrtc.org>
Commit-Queue: Tony Herre <toprice@chromium.org>
Cr-Commit-Position: refs/heads/main@{#35100}

[modify] https://crrev.com/8fb41a39e1a2d151d1c00c409630dcee80adeb76/api/frame_transformer_interface.h
[modify] https://crrev.com/8fb41a39e1a2d151d1c00c409630dcee80adeb76/modules/rtp_rtcp/source/rtp_sender_video_frame_transformer_delegate.cc
[modify] https://crrev.com/8fb41a39e1a2d151d1c00c409630dcee80adeb76/audio/channel_receive_frame_transformer_delegate.cc
[modify] https://crrev.com/8fb41a39e1a2d151d1c00c409630dcee80adeb76/video/rtp_video_stream_receiver_frame_transformer_delegate.cc
[modify] https://crrev.com/8fb41a39e1a2d151d1c00c409630dcee80adeb76/audio/channel_send_frame_transformer_delegate.cc


### gi...@appspot.gserviceaccount.com (2021-09-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3ede49de5e3416d33e9c87e0ee08b9c2441b0513

commit 3ede49de5e3416d33e9c87e0ee08b9c2441b0513
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Sep 28 00:02:06 2021

Roll WebRTC from 6ee97348872c to 3efea373092c (2 revisions)

https://webrtc.googlesource.com/src.git/+log/6ee97348872c..3efea373092c

2021-09-27 chromium-webrtc-autoroll@webrtc-ci.iam.gserviceaccount.com Roll chromium_revision 714d043f97..f1f05ac6a6 (925247:925390)
2021-09-27 toprice@chromium.org Add Direction indicator to TransformableFrames

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/webrtc-chromium-autoroll
Please CC webrtc-chromium-sheriffs-robots@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in WebRTC: https://bugs.chromium.org/p/webrtc/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1247260
Tbr: webrtc-chromium-sheriffs-robots@google.com
Change-Id: Ie7574b8d20611d3f7925ececd51b368408815ad8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3188845
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#925514}

[modify] https://crrev.com/3ede49de5e3416d33e9c87e0ee08b9c2441b0513/DEPS


### to...@chromium.org (2021-09-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-30)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: benmason (Android), harrysouders (iOS), None (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-30)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### to...@chromium.org (2021-09-30)

Plan to merge the initial fix back into 94 and 95, so that we fail a CHECK and crash rather than incorrectly casting and exposing corrupt memory. I don't intend to back merge the later change to remove the crash.


1. Why does your merge fit within the merge criteria for these milestones?
Security bug fix.

2. What changes specifically would you like to merge? Please link to Gerrit.
https://webrtc-review.googlesource.com/c/src/+/232301

3. Have the changes been released and tested on canary?
Yes

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
No. 

### gi...@appspot.gserviceaccount.com (2021-10-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/36e370cf4db9aee828ca327245d51ab042e8d3ae

commit 36e370cf4db9aee828ca327245d51ab042e8d3ae
Author: Tony Herre <toprice@chromium.org>
Date: Fri Oct 01 19:18:45 2021

Check direction of RTCEncodedFrames

Add a check to RTCEncodedVideoUnderlyingSink of the direction of the
underlying webrtc frame, to make sure a web app doesn't take a received
encoded frame and pass it into a sender insertable stream, which is as
yet unsupported in WebRTC.

Bug: 1247260
Change-Id: I9ed5bd8b2bd5e5ee461f3b553f8a91f6cc2e9ed7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3190473
Commit-Queue: Tony Herre <toprice@chromium.org>
Reviewed-by: Harald Alvestrand <hta@chromium.org>
Cr-Commit-Position: refs/heads/main@{#927323}

[modify] https://crrev.com/36e370cf4db9aee828ca327245d51ab042e8d3ae/third_party/blink/renderer/modules/peerconnection/rtc_rtp_receiver.cc
[modify] https://crrev.com/36e370cf4db9aee828ca327245d51ab042e8d3ae/third_party/blink/renderer/modules/peerconnection/rtc_encoded_video_underlying_sink.cc
[modify] https://crrev.com/36e370cf4db9aee828ca327245d51ab042e8d3ae/third_party/blink/renderer/modules/peerconnection/testing/mock_transformable_video_frame.h
[modify] https://crrev.com/36e370cf4db9aee828ca327245d51ab042e8d3ae/third_party/blink/renderer/modules/peerconnection/rtc_encoded_video_underlying_sink.h
[modify] https://crrev.com/36e370cf4db9aee828ca327245d51ab042e8d3ae/third_party/blink/renderer/modules/peerconnection/rtc_rtp_sender.cc
[modify] https://crrev.com/36e370cf4db9aee828ca327245d51ab042e8d3ae/third_party/blink/renderer/modules/peerconnection/rtc_encoded_video_underlying_sink_test.cc


### am...@chromium.org (2021-10-01)

toprice@ thank you for the information in https://crbug.com/chromium/1247260#c19; since this initial fix resulting in crash upon CHECK failure (to avoid exposing the memory corruption vector) has been on Canary a few days now, please do first confirm that you're not seeing any unintended consequences in overall stability. Presuming not (I'm not seeing any indicators of such on canary presently), please go ahead and merge https://webrtc-review.googlesource.com/c/src/+/232301 into M94 and M95. 

Please ensure these merges are completed by EOD Tuesday, 5 October so the fix can be included in the M94 refresh next Thursday. Thank you. 

### to...@chromium.org (2021-10-04)

Thanks Amy. Double checked canary crashes and not seeing any increased instability. I'll cherrypick now.

### to...@chromium.org (2021-10-04)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-10-04)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/8d8c0b440022c84386e02cc0c24c053aa7920be1

commit 8d8c0b440022c84386e02cc0c24c053aa7920be1
Author: Tony Herre <toprice@chromium.org>
Date: Fri Sep 24 12:05:20 2021

[Merge to 95] Add Direction indicator to TransformableFrames

Currently the implementation of FrameTransformers uses distinct,
incompatible types for recevied vs about-to-be-sent frames. This adds a
flag in the interface so we can at least check that we are being given
the correct type. crbug.com/1250638 tracks removing the need for this.

Chrome will be updated after this to check the direction flag and provide
a javascript error if the wrong type of frame is written into the
encoded insertable streams writable stream, rather than crashing.

(cherry picked from commit 8fb41a39e1a2d151d1c00c409630dcee80adeb76)

Bug: chromium:1247260
Change-Id: I9cbb66962ea0718ed47c5e5dba19a8ff9635b0b1
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/232301
Reviewed-by: Harald Alvestrand <hta@webrtc.org>
Commit-Queue: Tony Herre <toprice@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#35100}
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/233941
Commit-Queue: Harald Alvestrand <hta@webrtc.org>
Cr-Commit-Position: refs/branch-heads/4638@{#2}
Cr-Branched-From: fb501792ebb6474f9055fce4d8f8581aa47eadc8-refs/heads/main@{#34960}

[modify] https://crrev.com/8d8c0b440022c84386e02cc0c24c053aa7920be1/api/frame_transformer_interface.h
[modify] https://crrev.com/8d8c0b440022c84386e02cc0c24c053aa7920be1/modules/rtp_rtcp/source/rtp_sender_video_frame_transformer_delegate.cc
[modify] https://crrev.com/8d8c0b440022c84386e02cc0c24c053aa7920be1/audio/channel_receive_frame_transformer_delegate.cc
[modify] https://crrev.com/8d8c0b440022c84386e02cc0c24c053aa7920be1/video/rtp_video_stream_receiver_frame_transformer_delegate.cc
[modify] https://crrev.com/8d8c0b440022c84386e02cc0c24c053aa7920be1/audio/channel_send_frame_transformer_delegate.cc


### gi...@appspot.gserviceaccount.com (2021-10-04)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/6584528aeb0f0e2ab4d14114aefeee7e5997ade9

commit 6584528aeb0f0e2ab4d14114aefeee7e5997ade9
Author: Tony Herre <toprice@chromium.org>
Date: Mon Oct 04 10:02:51 2021

[Merge to 94] Add Direction indicator to TransformableFrames

Currently the implementation of FrameTransformers uses distinct,
incompatible types for recevied vs about-to-be-sent frames. This adds a
flag in the interface so we can at least check that we are being given
the correct type. crbug.com/1250638 tracks removing the need for this.

Chrome will be updated after this to check the direction flag and provide
a javascript error if the wrong type of frame is written into the
encoded insertable streams writable stream, rather than crashing.

(cherry picked from commit 8fb41a39e1a2d151d1c00c409630dcee80adeb76)

Bug: chromium:1247260
Change-Id: I9cbb66962ea0718ed47c5e5dba19a8ff9635b0b1
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/232301
Reviewed-by: Harald Alvestrand <hta@webrtc.org>
Commit-Queue: Tony Herre <toprice@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#35100}
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/233943
Commit-Queue: Harald Alvestrand <hta@webrtc.org>
Cr-Commit-Position: refs/branch-heads/4606@{#4}
Cr-Branched-From: 8b18304e66524060eca390f143033ba51322b3a2-refs/heads/master@{#34737}

[modify] https://crrev.com/6584528aeb0f0e2ab4d14114aefeee7e5997ade9/api/frame_transformer_interface.h
[modify] https://crrev.com/6584528aeb0f0e2ab4d14114aefeee7e5997ade9/modules/rtp_rtcp/source/rtp_sender_video_frame_transformer_delegate.cc
[modify] https://crrev.com/6584528aeb0f0e2ab4d14114aefeee7e5997ade9/audio/channel_receive_frame_transformer_delegate.cc
[modify] https://crrev.com/6584528aeb0f0e2ab4d14114aefeee7e5997ade9/video/rtp_video_stream_receiver_frame_transformer_delegate.cc
[modify] https://crrev.com/6584528aeb0f0e2ab4d14114aefeee7e5997ade9/audio/channel_send_frame_transformer_delegate.cc


### [Deleted User] (2021-10-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-04)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-10-06)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-10-06)

Congratulations to Marcin! The VRP Panel has decided to award $7500 for this report. Thank you for this detailed report (as always) and nice finding! 

### am...@chromium.org (2021-10-07)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-07)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### rz...@google.com (2021-10-11)

[Empty comment from Monorail migration]

### gi...@google.com (2021-10-18)

[Empty comment from Monorail migration]

### am...@google.com (2021-11-02)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-11-29)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/a07012e049a56730dfd6c77628e82d1bf5b3d68f

commit a07012e049a56730dfd6c77628e82d1bf5b3d68f
Author: Roger Zanoni <rzanoni@google.com>
Date: Mon Oct 11 12:01:44 2021

[M90-LTS] Add Direction indicator to TransformableFrames

Currently the implementation of FrameTransformers uses distinct,
incompatible types for recevied vs about-to-be-sent frames. This adds a
flag in the interface so we can at least check that we are being given
the correct type. crbug.com/1250638 tracks removing the need for this.

Chrome will be updated after this to check the direction flag and provide
a javascript error if the wrong type of frame is written into the
encoded insertable streams writable stream, rather than crashing.

M90 merge notes:
  - Conflicting lines above Direction enum (main has no GetSsrc())
  - Added the GetDirection mock method from
  https://chromium-review.googlesource.com/c/chromium/src/+/3190473

(cherry picked from commit 8fb41a39e1a2d151d1c00c409630dcee80adeb76)

Bug: chromium:1247260
No-Try: true
No-Presubmit: true
No-Tree-Checks: true
Change-Id: I9cbb66962ea0718ed47c5e5dba19a8ff9635b0b1
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/232301
Commit-Queue: Tony Herre <toprice@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#35100}
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/234751
Commit-Queue: Mirko Bonadei <mbonadei@webrtc.org>
Reviewed-by: Magnus Flodman <mflodman@webrtc.org>
Cr-Commit-Position: refs/branch-heads/4430@{#4}
Cr-Branched-From: bb52bdf09516ca548c4aff50526eda561f239bc0-refs/heads/master@{#33341}

[modify] https://crrev.com/a07012e049a56730dfd6c77628e82d1bf5b3d68f/api/test/mock_transformable_video_frame.h
[modify] https://crrev.com/a07012e049a56730dfd6c77628e82d1bf5b3d68f/api/frame_transformer_interface.h
[modify] https://crrev.com/a07012e049a56730dfd6c77628e82d1bf5b3d68f/modules/rtp_rtcp/source/rtp_sender_video_frame_transformer_delegate.cc
[modify] https://crrev.com/a07012e049a56730dfd6c77628e82d1bf5b3d68f/audio/channel_receive_frame_transformer_delegate.cc
[modify] https://crrev.com/a07012e049a56730dfd6c77628e82d1bf5b3d68f/video/rtp_video_stream_receiver_frame_transformer_delegate.cc
[modify] https://crrev.com/a07012e049a56730dfd6c77628e82d1bf5b3d68f/audio/channel_send_frame_transformer_delegate.cc


### gi...@appspot.gserviceaccount.com (2021-11-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/24c201444aee8a545e8daa9c8fa3a703f1876565

commit 24c201444aee8a545e8daa9c8fa3a703f1876565
Author: Tony Herre <toprice@chromium.org>
Date: Mon Nov 29 14:58:54 2021

[M90-LTS] Check direction of RTCEncodedFrames

Add a check to RTCEncodedVideoUnderlyingSink of the direction of the
underlying webrtc frame, to make sure a web app doesn't take a received
encoded frame and pass it into a sender insertable stream, which is as
yet unsupported in WebRTC.

M90 merge issues:
  - mock_transformable_video_frame.h not present

  - conflicting declarations of mock_frame on
  CreateEncodedVideoFrameChunk()

(cherry picked from commit 36e370cf4db9aee828ca327245d51ab042e8d3ae)

Bug: 1247260
Change-Id: I9ed5bd8b2bd5e5ee461f3b553f8a91f6cc2e9ed7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3190473
Commit-Queue: Tony Herre <toprice@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#927323}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3217734
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1670}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/24c201444aee8a545e8daa9c8fa3a703f1876565/third_party/blink/renderer/modules/peerconnection/rtc_rtp_receiver.cc
[modify] https://crrev.com/24c201444aee8a545e8daa9c8fa3a703f1876565/third_party/blink/renderer/modules/peerconnection/rtc_encoded_video_underlying_sink.cc
[modify] https://crrev.com/24c201444aee8a545e8daa9c8fa3a703f1876565/third_party/blink/renderer/modules/peerconnection/rtc_encoded_video_underlying_sink.h
[modify] https://crrev.com/24c201444aee8a545e8daa9c8fa3a703f1876565/third_party/blink/renderer/modules/peerconnection/rtc_rtp_sender.cc
[modify] https://crrev.com/24c201444aee8a545e8daa9c8fa3a703f1876565/third_party/blink/renderer/modules/peerconnection/rtc_encoded_video_underlying_sink_test.cc


### rz...@google.com (2021-11-29)

[Empty comment from Monorail migration]

### vu...@sourcefire.com (2021-12-01)

Please advise status for disclosure release.


### am...@chromium.org (2021-12-01)

This issue was fixed on 4 October, so it will be opened/labeled as allpublic 14 weeks later, which (by my math) is 10 January 2022. 

### [Deleted User] (2022-01-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-10-11)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/15dfc5a567e64405db573c0b7a959c9d9a786ecc

commit 15dfc5a567e64405db573c0b7a959c9d9a786ecc
Author: Sergio Garcia Murillo <sergio.garcia.murillo@gmail.com>
Date: Tue Oct 11 10:34:44 2022

Add GetContributionSources to TransformableIncomingAudioFrame

RTPHeader is not exported, so the TransformableIncomingAudioFrame can't be mocked in chrome tests, using a getter instead.

Bug: chromium:1247260
Change-Id: I2af4e6a88b3f4772b3bb50ee0ae9d5c80fed3ae4
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/278785
Reviewed-by: Harald Alvestrand <hta@webrtc.org>
Commit-Queue: Tomas Gunnarsson <tommi@webrtc.org>
Reviewed-by: Tomas Gunnarsson <tommi@webrtc.org>
Cr-Commit-Position: refs/heads/main@{#38352}

[modify] https://crrev.com/15dfc5a567e64405db573c0b7a959c9d9a786ecc/api/frame_transformer_interface.h
[modify] https://crrev.com/15dfc5a567e64405db573c0b7a959c9d9a786ecc/audio/channel_receive_frame_transformer_delegate.cc


### gi...@appspot.gserviceaccount.com (2022-10-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5b9820958c81b5e261c64ad091d12fe2ef4f09c7

commit 5b9820958c81b5e261c64ad091d12fe2ef4f09c7
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Oct 11 19:26:27 2022

Roll WebRTC from 6b7505877464 to 78d80f9be7c2 (7 revisions)

https://webrtc.googlesource.com/src.git/+log/6b7505877464..78d80f9be7c2

2022-10-11 perkj@webrtc.org Add SmokeSendAndReceivePacketsOnOneThread
2022-10-11 hta@webrtc.org Reland "Add test for StunMessage::ValidateMessageIntegrity"
2022-10-11 sergio.garcia.murillo@gmail.com Add GetContributionSources to TransformableIncomingAudioFrame
2022-10-11 mbonadei@webrtc.org Include jni.h in jni_int_wrapper.h.
2022-10-11 mbonadei@webrtc.org Add missing dependency and remove nogncheck.
2022-10-11 mbonadei@webrtc.org Revert "Add test for StunMessage::ValidateMessageIntegrity"
2022-10-11 titovartem@webrtc.org [PCLF] Prepare to add extra scaling step before passing frame to analyzer and video sinks

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/webrtc-chromium-autoroll
Please CC webrtc-chromium-sheriffs-robots@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in WebRTC: https://bugs.chromium.org/p/webrtc/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1177125,chromium:1247260
Tbr: webrtc-chromium-sheriffs-robots@google.com
Change-Id: I71b908afa6c133250689e4333e247b30b57981b7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3946322
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1057594}

[modify] https://crrev.com/5b9820958c81b5e261c64ad091d12fe2ef4f09c7/DEPS


### gi...@appspot.gserviceaccount.com (2022-10-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cd868c2d083e6528f018c4b94c0ebcc6239bb9ce

commit cd868c2d083e6528f018c4b94c0ebcc6239bb9ce
Author: Sergio Garcia Murillo <sergio.garcia.murillo@gmail.com>
Date: Fri Oct 14 08:15:24 2022

Check direction of RTCEncodedFrames in audio

This CL mimics what was already done for video here:
https://chromium-review.googlesource.com/c/chromium/src/+/3190473

Add a check to RTCEncodedVideoUnderlyingSink of the direction of the
underlying webrtc frame, to make sure a web app doesn't take a received
encoded frame and pass it into a sender insertable stream, which is as
yet unsupported in WebRTC.

Bug: 1247260
Change-Id: Ibfd4d37f5be161d6080aa16bdbf4e68dfe0ed084
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3938077
Reviewed-by: Mike West <mkwst@chromium.org>
Reviewed-by: Harald Alvestrand <hta@chromium.org>
Reviewed-by: Tomas Gunnarsson <tommi@chromium.org>
Commit-Queue: Harald Alvestrand <hta@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1059144}

[modify] https://crrev.com/cd868c2d083e6528f018c4b94c0ebcc6239bb9ce/third_party/blink/renderer/modules/peerconnection/rtc_encoded_audio_underlying_sink.cc
[modify] https://crrev.com/cd868c2d083e6528f018c4b94c0ebcc6239bb9ce/third_party/blink/renderer/modules/peerconnection/rtc_rtp_receiver.cc
[modify] https://crrev.com/cd868c2d083e6528f018c4b94c0ebcc6239bb9ce/third_party/blink/renderer/modules/peerconnection/rtc_encoded_audio_underlying_sink.h
[modify] https://crrev.com/cd868c2d083e6528f018c4b94c0ebcc6239bb9ce/third_party/blink/renderer/modules/peerconnection/rtc_encoded_audio_frame.cc
[modify] https://crrev.com/cd868c2d083e6528f018c4b94c0ebcc6239bb9ce/third_party/blink/renderer/modules/peerconnection/rtc_encoded_audio_sender_sink_optimizer.cc
[modify] https://crrev.com/cd868c2d083e6528f018c4b94c0ebcc6239bb9ce/third_party/blink/renderer/modules/peerconnection/rtc_encoded_audio_underlying_sink_test.cc
[modify] https://crrev.com/cd868c2d083e6528f018c4b94c0ebcc6239bb9ce/third_party/blink/renderer/modules/peerconnection/rtc_rtp_sender.cc
[add] https://crrev.com/cd868c2d083e6528f018c4b94c0ebcc6239bb9ce/third_party/blink/renderer/modules/peerconnection/testing/mock_transformable_audio_frame.h
[modify] https://crrev.com/cd868c2d083e6528f018c4b94c0ebcc6239bb9ce/third_party/blink/renderer/modules/peerconnection/rtc_encoded_audio_receiver_source_optimizer.cc
[modify] https://crrev.com/cd868c2d083e6528f018c4b94c0ebcc6239bb9ce/third_party/blink/renderer/modules/BUILD.gn
[modify] https://crrev.com/cd868c2d083e6528f018c4b94c0ebcc6239bb9ce/third_party/blink/renderer/modules/peerconnection/rtc_encoded_audio_receiver_sink_optimizer.cc


### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1247260?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057198)*
