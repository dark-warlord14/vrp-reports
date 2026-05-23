# AddressSanitizer: heap-use-after-free fft_frame_pffft.cc:81 in blink::FFTFrame::FFTSetupForSize

| Field | Value |
|-------|-------|
| **Issue ID** | [40055980](https://issues.chromium.org/issues/40055980) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebAudio |
| **Platforms** | Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | rt...@chromium.org |
| **Created** | 2021-05-24 |
| **Bounty** | $7,500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0

Steps to reproduce the problem:
#TestOn
Windows NT 10.0; Win64; x64
gs://chromium-browser-asan/win32-release_x64/asan-win32-release_x64-880310.zip

#Reproduce
python3.6m -m http.server 8000
chrome.exe --no-sandbox --js-flags='--expose_gc' --enable-blink-test-features --single-process --autoplay-policy=no-user-gesture-required --use-fake-device-for-media-stream --no-default-browser-check --disable-extensions --user-data-dir=chrome_test
open http://localhost:8000/fuzz-00001.html

#Debuger
```
The reason for the vulnerability is that multi-threaded race conditions cause the iterator to fail, so it is difficult to reproduce.
Here, you can use WINDBG to add the following breakpoints for observation.
It can be observed that the functions InitializeFFTSetupForSize and FFTSetupForSize are called in different threads, which is the root cause of the vulnerability.

bp blink_platform!blink::FFTFrame::FFTSetupForSize ".echo 'FFTSetupForSize';~#;gc"
bp blink_platform!blink::FFTFrame::InitializeFFTSetupForSize ".echo 'InitializeFFTSetupForSize';~#;gc"
bp blink_platform!blink::HRTFDatabaseLoader::LoadAsynchronously ".echo 'LoadAsynchronously';~#;gc"

...CUT...

'FFTSetupForSize'
. 42  Id: 38f8.3af4 Suspend: 1 Teb: 00000092`64614000 Unfrozen "Chrome_InProcRendererThread"
      Start: base!base::`anonymous namespace'::ThreadFunc (00007ff8`0c620a10)
      Priority: 0  Priority class: 32  Affinity: ffff
'LoadAsynchronously' <<<
. 42  Id: 38f8.3af4 Suspend: 1 Teb: 00000092`64614000 Unfrozen "Chrome_InProcRendererThread"
      Start: base!base::`anonymous namespace'::ThreadFunc (00007ff8`0c620a10)
      Priority: 0  Priority class: 32  Affinity: ffff
'InitializeFFTSetupForSize'
. 42  Id: 38f8.3af4 Suspend: 1 Teb: 00000092`64614000 Unfrozen "Chrome_InProcRendererThread"
      Start: base!base::`anonymous namespace'::ThreadFunc (00007ff8`0c620a10)
      Priority: 0  Priority class: 32  Affinity: ffff
'InitializeFFTSetupForSize'
. 42  Id: 38f8.3af4 Suspend: 1 Teb: 00000092`64614000 Unfrozen "Chrome_InProcRendererThread"
      Start: base!base::`anonymous namespace'::ThreadFunc (00007ff8`0c620a10)
      Priority: 0  Priority class: 32  Affinity: ffff
'InitializeFFTSetupForSize'
. 42  Id: 38f8.3af4 Suspend: 1 Teb: 00000092`64614000 Unfrozen "Chrome_InProcRendererThread"
      Start: base!base::`anonymous namespace'::ThreadFunc (00007ff8`0c620a10)
      Priority: 0  Priority class: 32  Affinity: ffff
'InitializeFFTSetupForSize'
. 42  Id: 38f8.3af4 Suspend: 1 Teb: 00000092`64614000 Unfrozen "Chrome_InProcRendererThread"
      Start: base!base::`anonymous namespace'::ThreadFunc (00007ff8`0c620a10)
      Priority: 0  Priority class: 32  Affinity: ffff
'InitializeFFTSetupForSize'
. 86  Id: 38f8.130 Suspend: 1 Teb: 00000092`64678000 Unfrozen "HRTF database loader thread"
      Start: base!base::`anonymous namespace'::ThreadFunc (00007ff8`0c620a10)
      Priority: 0  Priority class: 32  Affinity: ffff
'FFTSetupForSize'  <<<
. 86  Id: 38f8.130 Suspend: 1 Teb: 00000092`64678000 Unfrozen "HRTF database loader thread"
      Start: base!base::`anonymous namespace'::ThreadFunc (00007ff8`0c620a10)
      Priority: 0  Priority class: 32  Affinity: ffff
'FFTSetupForSize'
. 86  Id: 38f8.130 Suspend: 1 Teb: 00000092`64678000 Unfrozen "HRTF database loader thread"
      Start: base!base::`anonymous namespace'::ThreadFunc (00007ff8`0c620a10)
      Priority: 0  Priority class: 32  Affinity: ffff
```

What is the expected behavior?

What went wrong?

#Analysis
```
By analyzing the ASAN log, it is easy to analyze that the functions InitializeFFTSetupForSize and FFTSetupForSize are called in different threads, and they will all access and modify the same variable named setup, which leads to a race condition, which leads to the failure of the iterator at [2], which leads to vulnerabilities.
void FFTFrame::InitializeFFTSetupForSize(wtf_size_t fft_size) {
  auto& setup = FFTSetups();

  if (!setup.Contains(fft_size)) {
    // Make sure allocation of a new setup only occurs on the main thread so we
    // don't have a race condition with multiple threads trying to write to the
    // same element of the vector.
    DCHECK(IsMainThread());

    setup.insert(fft_size, std::make_unique<FFTSetup>(fft_size));		<<[1]
  }
}

PFFFT_Setup* FFTFrame::FFTSetupForSize(wtf_size_t fft_size) {
  auto& setup = FFTSetups();

  DCHECK(setup.Contains(fft_size));

  return setup.find(fft_size)->value->GetSetup();	<<[2]
}

=================================================================
==6148==ERROR: AddressSanitizer: heap-use-after-free on address 0x1018802b5e80 at pc 0x7ffc631a1614 bp 0x000077baf120 sp 0x000077baf168
READ of size 4 at 0x1018802b5e80 thread T70
==6148==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ffc631a1613 in blink::FFTFrame::FFTSetupForSize C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\pffft\fft_frame_pffft.cc:81
    #1 0x7ffc631a259e in blink::FFTFrame::DoInverseFFT C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\pffft\fft_frame_pffft.cc:196
    #2 0x7ffc64d1c6ba in blink::FFTFrame::CreateInterpolatedFrame C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\fft_frame.cc:65
    #3 0x7ffc64d21130 in blink::HRTFKernel::CreateInterpolatedKernel C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\hrtf_kernel.cc:119
    #4 0x7ffc647fb4e8 in blink::HRTFElevation::CreateForSubject C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\hrtf_elevation.cc:263
    #5 0x7ffc647f6e8e in blink::HRTFDatabase::HRTFDatabase C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\hrtf_database.cc:55
    #6 0x7ffc63d4175e in blink::HRTFDatabaseLoader::LoadTask C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\hrtf_database_loader.cc:83
    #7 0x7ffc5307101a in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:178
    #8 0x7ffc557d1a5f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:357
    #9 0x7ffc557d10d9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:270
    #10 0x7ffc557a5080 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:39
    #11 0x7ffc557d3104 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:466
    #12 0x7ffc52ff6ba3 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #13 0x7ffc51a7a454 in blink::scheduler::WorkerThread::SimpleThreadImpl::Run C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\scheduler\worker\worker_thread.cc:154
    #14 0x7ffc53142a1f in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:121
    #15 0x7ff60db5dac7 in __asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_thread.cpp:279
    #16 0x7ffca9084d2d in BaseThreadInitThunk+0x1d (C:\WINDOWS\System32\KERNEL32.DLL+0x180014d2d)
    #17 0x7ffcaa9d5a7a in RtlUserThreadStart+0x2a (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180065a7a)

0x1018802b5e80 is located 64 bytes inside of 128-byte region [0x1018802b5e40,0x1018802b5ec0)
freed by thread T33 here:
    #0 0x7ff60db53bcb in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ffc631a3af4 in WTF::HashTable<unsigned int,WTF::KeyValuePair<unsigned int,std::__1::unique_ptr<blink::FFTFrame::FFTSetup,std::__1::default_delete<blink::FFTFrame::FFTSetup> > >,WTF::KeyValuePairKeyExtractor,WTF::IntHash<unsigned int>,WTF::HashMapValueTraits<WTF::HashTraits<unsigned int>,WTF::HashTraits<std::__1::unique_ptr<blink::FFTFrame::FFTSetup,std::__1::default_delete<blink::FFTFrame::FFTSetup> > > >,WTF::HashTraits<unsigned int>,WTF::PartitionAllocator>::RehashTo C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\wtf\hash_table.h:1898
    #2 0x7ffc631a366a in WTF::HashTable<unsigned int,WTF::KeyValuePair<unsigned int,std::__1::unique_ptr<blink::FFTFrame::FFTSetup,std::__1::default_delete<blink::FFTFrame::FFTSetup> > >,WTF::KeyValuePairKeyExtractor,WTF::IntHash<unsigned int>,WTF::HashMapValueTraits<WTF::HashTraits<unsigned int>,WTF::HashTraits<std::__1::unique_ptr<blink::FFTFrame::FFTSetup,std::__1::default_delete<blink::FFTFrame::FFTSetup> > > >,WTF::HashTraits<unsigned int>,WTF::PartitionAllocator>::Expand C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\wtf\hash_table.h:1786
    #3 0x7ffc631a32b3 in WTF::HashTable<unsigned int,WTF::KeyValuePair<unsigned int,std::__1::unique_ptr<blink::FFTFrame::FFTSetup,std::__1::default_delete<blink::FFTFrame::FFTSetup> > >,WTF::KeyValuePairKeyExtractor,WTF::IntHash<unsigned int>,WTF::HashMapValueTraits<WTF::HashTraits<unsigned int>,WTF::HashTraits<std::__1::unique_ptr<blink::FFTFrame::FFTSetup,std::__1::default_delete<blink::FFTFrame::FFTSetup> > > >,WTF::HashTraits<unsigned int>,WTF::PartitionAllocator>::insert<WTF::HashMapTranslator<WTF::HashMapValueTraits<WTF::HashTraits<unsigned int>,WTF::HashTraits<std::unique_ptr<blink::FFTFrame::FFTSetup> > >,WTF::IntHash<unsigned int>,WTF::PartitionAllocator>,unsigned int &,std::unique_ptr<blink::FFTFrame::FFTSetup> > C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\wtf\hash_table.h:1435
    #4 0x7ffc631a109a in blink::FFTFrame::InitializeFFTSetupForSize C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\pffft\fft_frame_pffft.cc:72
    #5 0x7ffc631a173b in blink::FFTFrame::FFTFrame C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\pffft\fft_frame_pffft.cc:94
    #6 0x7ffc63d6254c in blink::RealtimeAnalyser::RealtimeAnalyser C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\realtime_analyser.cc:58
    #7 0x7ffc631d4483 in blink::AnalyserHandler::AnalyserHandler C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\analyser_node.cc:38
    #8 0x7ffc631d718f in blink::AnalyserNode::AnalyserNode C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\analyser_node.cc:196
    #9 0x7ffc631d77b7 in blink::MakeGarbageCollectedTrait<blink::AnalyserNode>::Call<blink::BaseAudioContext &> C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\heap\impl\heap.h:529
    #10 0x7ffc631d71f9 in blink::AnalyserNode::Create C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\analyser_node.cc:211
    #11 0x7ffc6392df20 in blink::`anonymous namespace'::v8_analyser_node::ConstructorCallback C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\bindings\modules\v8\v8_analyser_node.cc:301
    #12 0x7ffc4f15485d in v8::internal::FunctionCallbackArguments::Call C:\b\s\w\ir\cache\builder\src\v8\src\api\api-arguments-inl.h:156
    #13 0x7ffc4f1509e6 in v8::internal::`anonymous namespace'::HandleApiCallHelper<1> C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:112
    #14 0x7ffc4f14efed in v8::internal::Builtin_Impl_HandleApiCall C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:138
    #15 0x7ffc4f14e38e in v8::internal::Builtin_HandleApiCall C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:130
    #16 0x7e8c000f679b  (<unknown module>)

previously allocated by thread T33 here:
    #0 0x7ff60db53ccb in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ffc5454b667 in WTF::Partitions::FastMalloc C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\wtf\allocator\partitions.cc:271
    #2 0x7ffc631a3640 in WTF::HashTable<unsigned int,WTF::KeyValuePair<unsigned int,std::__1::unique_ptr<blink::FFTFrame::FFTSetup,std::__1::default_delete<blink::FFTFrame::FFTSetup> > >,WTF::KeyValuePairKeyExtractor,WTF::IntHash<unsigned int>,WTF::HashMapValueTraits<WTF::HashTraits<unsigned int>,WTF::HashTraits<std::__1::unique_ptr<blink::FFTFrame::FFTSetup,std::__1::default_delete<blink::FFTFrame::FFTSetup> > > >,WTF::HashTraits<unsigned int>,WTF::PartitionAllocator>::Expand C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\wtf\hash_table.h:1786
    #3 0x7ffc631a32b3 in WTF::HashTable<unsigned int,WTF::KeyValuePair<unsigned int,std::__1::unique_ptr<blink::FFTFrame::FFTSetup,std::__1::default_delete<blink::FFTFrame::FFTSetup> > >,WTF::KeyValuePairKeyExtractor,WTF::IntHash<unsigned int>,WTF::HashMapValueTraits<WTF::HashTraits<unsigned int>,WTF::HashTraits<std::__1::unique_ptr<blink::FFTFrame::FFTSetup,std::__1::default_delete<blink::FFTFrame::FFTSetup> > > >,WTF::HashTraits<unsigned int>,WTF::PartitionAllocator>::insert<WTF::HashMapTranslator<WTF::HashMapValueTraits<WTF::HashTraits<unsigned int>,WTF::HashTraits<std::unique_ptr<blink::FFTFrame::FFTSetup> > >,WTF::IntHash<unsigned int>,WTF::PartitionAllocator>,unsigned int &,std::unique_ptr<blink::FFTFrame::FFTSetup> > C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\wtf\hash_table.h:1435
    #4 0x7ffc631a109a in blink::FFTFrame::InitializeFFTSetupForSize C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\pffft\fft_frame_pffft.cc:72
    #5 0x7ffc631a173b in blink::FFTFrame::FFTFrame C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\pffft\fft_frame_pffft.cc:94
    #6 0x7ffc631e2af2 in blink::PeriodicWave::CreateBandLimitedTables C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\periodic_wave.cc:407
    #7 0x7ffc631e45e8 in blink::PeriodicWave::GenerateBasicWaveform C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\periodic_wave.cc:548
    #8 0x7ffc631e423f in blink::PeriodicWave::CreateSine C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\periodic_wave.cc:130
    #9 0x7ffc6245cd86 in blink::BaseAudioContext::GetPeriodicWave C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\base_audio_context.cc:583
    #10 0x7ffc631dc54d in blink::OscillatorHandler::SetType C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\oscillator_node.cc:138
    #11 0x7ffc631dbf5e in blink::OscillatorHandler::OscillatorHandler C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\oscillator_node.cc:71
    #12 0x7ffc631e1045 in blink::OscillatorNode::OscillatorNode C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\oscillator_node.cc:834
    #13 0x7ffc631e201e in blink::MakeGarbageCollectedTrait<blink::OscillatorNode>::Call<blink::BaseAudioContext &,const WTF::String &,blink::PeriodicWave *&> C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\heap\impl\heap.h:529
    #14 0x7ffc631e11c2 in blink::OscillatorNode::Create C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\oscillator_node.cc:845
    #15 0x7ffc6245ca94 in blink::BaseAudioContext::createOscillator C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\base_audio_context.cc:544
    #16 0x7ffc631fe4f0 in blink::`anonymous namespace'::v8_base_audio_context::CreateOscillatorOperationCallback C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\bindings\modules\v8\v8_base_audio_context.cc:708
    #17 0x7ffc4f15485d in v8::internal::FunctionCallbackArguments::Call C:\b\s\w\ir\cache\builder\src\v8\src\api\api-arguments-inl.h:156
    #18 0x7ffc4f151ad7 in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:112
    #19 0x7ffc4f14f091 in v8::internal::Builtin_Impl_HandleApiCall C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:142
    #20 0x7ffc4f14e38e in v8::internal::Builtin_HandleApiCall C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:130
    #21 0x7e8c000f679b  (<unknown module>)

Thread T70 created by T33 here:
    #0 0x7ff60db5e5b2 in __asan_wrap_CreateThread C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_win.cpp:146
    #1 0x7ffc53141dfe in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:185
    #2 0x7ffc530b5460 in base::SimpleThread::StartAsync C:\b\s\w\ir\cache\builder\src\base\threading\simple_thread.cc:51
    #3 0x7ffc519fbcb6 in blink::Thread::CreateThread C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\scheduler\common\thread.cc:86
    #4 0x7ffc5548e592 in blink::Platform::CreateThread C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\exported\platform.cc:297
    #5 0x7ffc63d40a8e in blink::HRTFDatabaseLoader::LoadAsynchronously C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\hrtf_database_loader.cc:97
    #6 0x7ffc63d40615 in blink::HRTFDatabaseLoader::CreateAndLoadAsynchronouslyIfNecessary C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\hrtf_database_loader.cc:60
    #7 0x7ffc6319b7ea in blink::AudioListener::CreateAndLoadHRTFDatabaseLoader C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\audio_listener.cc:297
    #8 0x7ffc631c9fb2 in blink::PannerHandler::SetPanningModel C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\panner_node.cc:395
    #9 0x7ffc631c47fd in blink::PannerHandler::SetPanningModel C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\panner_node.cc:380
    #10 0x7ffc6397bb59 in blink::`anonymous namespace'::v8_panner_node::PanningModelAttributeSetCallback C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\bindings\modules\v8\v8_panner_node.cc:124
    #11 0x7ffc4f15485d in v8::internal::FunctionCallbackArguments::Call C:\b\s\w\ir\cache\builder\src\v8\src\api\api-arguments-inl.h:156
    #12 0x7ffc4f151ad7 in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:112
    #13 0x7ffc4f14fd49 in v8::internal::Builtins::InvokeApiFunction C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:226
    #14 0x7ffc4fd92a74 in v8::internal::Object::SetPropertyWithAccessor C:\b\s\w\ir\cache\builder\src\v8\src\objects\objects.cc:1636
    #15 0x7ffc4fda2c63 in v8::internal::Object::SetPropertyInternal C:\b\s\w\ir\cache\builder\src\v8\src\objects\objects.cc:2588
    #16 0x7ffc4fda1cf3 in v8::internal::Object::SetProperty C:\b\s\w\ir\cache\builder\src\v8\src\objects\objects.cc:2643
    #17 0x7ffc4f840f0e in v8::internal::StoreIC::Store C:\b\s\w\ir\cache\builder\src\v8\src\ic\ic.cc:1661
    #18 0x7ffc4f85923b in v8::internal::Runtime_StoreIC_Miss C:\b\s\w\ir\cache\builder\src\v8\src\ic\ic.cc:2540
    #19 0x7e8c000f669b  (<unknown module>)

Thread T33 created by T0 here:
    #0 0x7ff60db5e5b2 in __asan_wrap_CreateThread C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_win.cpp:146
    #1 0x7ffc53141dfe in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:185
    #2 0x7ffc530b6bca in base::Thread::StartWithOptions C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:187
    #3 0x7ffc4d2f27ba in content::RenderProcessHostImpl::Init C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_process_host_impl.cc:1861
    #4 0x7ffc4d2d55d2 in content::RenderFrameHostManager::InitRenderView C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:2806
    #5 0x7ffc4d2ccdb5 in content::RenderFrameHostManager::ReinitializeMainRenderFrame C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:3032
    #6 0x7ffc4d2cab48 in content::RenderFrameHostManager::GetFrameHostForNavigation C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:1052
    #7 0x7ffc4d2c970c in content::RenderFrameHostManager::DidCreateNavigationRequest C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:807
    #8 0x7ffc4d04f5e5 in content::FrameTreeNode::CreatedNavigationRequest C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\frame_tree_node.cc:532
    #9 0x7ffc4d209c5f in content::Navigator::Navigate C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\navigator.cc:596
    #10 0x7ffc4d17957e in content::NavigationControllerImpl::NavigateWithoutEntry C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\navigation_controller_impl.cc:3302
    #11 0x7ffc4d178734 in content::NavigationControllerImpl::LoadURLWithParams C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\navigation_controller_impl.cc:1136
    #12 0x7ffc552bafb9 in `anonymous namespace'::LoadURLInContents C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser_navigator.cc:386
    #13 0x7ffc552b8316 in Navigate C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser_navigator.cc:658
    #14 0x7ffc5c78c291 in StartupBrowserCreatorImpl::OpenTabsInBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:313
    #15 0x7ffc5c78e06f in StartupBrowserCreatorImpl::RestoreOrCreateBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:582
    #16 0x7ffc5c78b438 in StartupBrowserCreatorImpl::DetermineURLsAndLaunch C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:429
    #17 0x7ffc5c78aaa0 in StartupBrowserCreatorImpl::Launch C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:218
    #18 0x7ffc5877ce4e in StartupBrowserCreator::LaunchBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:689
    #19 0x7ffc587837ff in StartupBrowserCreator::ProcessLastOpenedProfiles C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1259
    #20 0x7ffc58782d43 in StartupBrowserCreator::LaunchBrowserForLastProfiles C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1209
    #21 0x7ffc5877c349 in StartupBrowserCreator::ProcessCmdLineImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1127
    #22 0x7ffc5877a973 in StartupBrowserCreator::Start C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:624
    #23 0x7ffc5590c310 in ChromeBrowserMainParts::PreMainMessageLoopRunImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc:1647
    #24 0x7ffc55909dbe in ChromeBrowserMainParts::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc:1039
    #25 0x7ffc4c8071de in content::BrowserMainLoop::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:960
    #26 0x7ffc4d59f283 in content::StartupTaskRunner::RunAllTasksNow C:\b\s\w\ir\cache\builder\src\content\browser\startup_task_runner.cc:41
    #27 0x7ffc4c8066e8 in content::BrowserMainLoop::CreateStartupTasks C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:868
    #28 0x7ffc4c80e125 in content::BrowserMainRunnerImpl::Initialize C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:131
    #29 0x7ffc4c802cd4 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:43
    #30 0x7ffc52d8cbe8 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:597
    #31 0x7ffc52d8f51f in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1080
    #32 0x7ffc52d8e72f in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:955
    #33 0x7ffc52d8ba97 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:372
    #34 0x7ffc52d8c08b in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:398
    #35 0x7ffc48d3145a in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:151
    #36 0x7ff60dab5bd1 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:169
    #37 0x7ff60dab2c1d in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:369
    #38 0x7ff60de9bb7f in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #39 0x7ffca9084d2d in BaseThreadInitThunk+0x1d (C:\WINDOWS\System32\KERNEL32.DLL+0x180014d2d)
    #40 0x7ffcaa9d5a7a in RtlUserThreadStart+0x2a (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180065a7a)

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\pffft\fft_frame_pffft.cc:81 in blink::FFTFrame::FFTSetupForSize
Shadow bytes around the buggy address:
  0x020390056b80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x020390056b90: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x020390056ba0: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x020390056bb0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa
  0x020390056bc0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
=>0x020390056bd0:[fd]fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
  0x020390056be0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x020390056bf0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x020390056c00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x020390056c10: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x020390056c20: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
  Shadow gap:              cc
==6148==ABORTING
```

Did this work before? N/A 

Chrome version: <Copy from: 'about:version'>  Channel: dev
OS Version: 10.0
Flash Version:

## Attachments

- [fuzz-00001.html](attachments/fuzz-00001.html) (text/plain, 62.9 KB)
- [demicmAudioShort.mp3](attachments/demicmAudioShort.mp3) (application/octet-stream, 22.4 KB)
- [viper.mp3](attachments/viper.mp3) (application/octet-stream, 3.3 KB)
- [viper.ogg](attachments/viper.ogg) (application/octet-stream, 2.5 KB)
- [patch.diff](attachments/patch.diff) (text/plain, 2.1 KB)
- [tsan.txt](attachments/tsan.txt) (text/plain, 58.0 KB)

## Timeline

### [Deleted User] (2021-05-24)

[Empty comment from Monorail migration]

### m....@gmail.com (2021-05-24)

[Comment Deleted]

### m....@gmail.com (2021-05-24)

[Comment Deleted]

### m....@gmail.com (2021-05-25)

There are two kinds of fixes here, one is to let 2 functions in the same thread or sequence, the other is to use the lock, I am trying to use the second solution here, because it is easier to implement.
```
diff --git a/fft_frame.h b/fft_frame.h
index 5474597..372f4e9 100644
--- a/fft_frame.h
+++ b/fft_frame.h
@@ -209,6 +209,9 @@ class PLATFORM_EXPORT FFTFrame {
   // |InitializeFFTSetupForSize()| must be called for this size before calling
   // |FFTSetupForSize()|.
   static PFFFT_Setup* FFTSetupForSize(wtf_size_t fft_order);
+  
+  //lock for FFTSetups() 
+  static base::Lock& FFTSetupLock();
 
   // Work array for converting PFFFT results to and from the format expected in
   // |real_data_| and |imag_datra_|.
diff --git a/fft_frame_pffft.cc b/fft_frame_pffft.cc
index 410c38a..a2af5ba 100644
--- a/fft_frame_pffft.cc
+++ b/fft_frame_pffft.cc
@@ -47,6 +47,8 @@ HashMap<unsigned, std::unique_ptr<FFTFrame::FFTSetup>>& FFTFrame::FFTSetups() {
     // Make sure we construct the fft_setups vector below on the main thread.
     // Once constructed, we can access it from any thread.
     DCHECK(IsMainThread());
+    
+    FFTSetupLock();
     first_call = false;
   }
 
@@ -60,6 +62,11 @@ HashMap<unsigned, std::unique_ptr<FFTFrame::FFTSetup>>& FFTFrame::FFTSetups() {
   return fft_setups;
 }
 
+Lock& FFTFrame::FFTSetupLock(){
+  DEFINE_STATIC_LOCAL(Lock, fft_setups_lock, ());
+  return fft_setups_lock;
+}
+
 void FFTFrame::InitializeFFTSetupForSize(wtf_size_t fft_size) {
   auto& setup = FFTSetups();
 
@@ -68,7 +75,7 @@ void FFTFrame::InitializeFFTSetupForSize(wtf_size_t fft_size) {
     // don't have a race condition with multiple threads trying to write to the
     // same element of the vector.
     DCHECK(IsMainThread());
-
+    AutoLock locked(FFTSetupLock());
     setup.insert(fft_size, std::make_unique<FFTSetup>(fft_size));
   }
 }
@@ -77,7 +84,8 @@ PFFFT_Setup* FFTFrame::FFTSetupForSize(wtf_size_t fft_size) {
   auto& setup = FFTSetups();
 
   DCHECK(setup.Contains(fft_size));
-
+  
+  AutoLock locked(FFTSetupLock());
   return setup.find(fft_size)->value->GetSetup();
 }
 
@@ -145,6 +153,8 @@ void FFTFrame::Initialize(float sample_rate) {
 }
 
 void FFTFrame::Cleanup() {
+  //not sure here
+  AutoLock locked(FFTSetupLock());
   for (auto& setup : FFTSetups()) {
     setup.value.reset();
   }

```

### va...@chromium.org (2021-05-25)

hongchan@ -- tentatively assigning this to you. I haven't reproduced it yet.

[Monorail components: Blink>WebAudio]

### va...@chromium.org (2021-05-25)

[Empty comment from Monorail migration]

### m....@gmail.com (2021-05-25)

https://crbug.com/chromium/1212599#c5

I found that using TSAN version test is very easy to reproduce
“gs://chromium-browser-tsan/linux-release/tsan-linux-release-886199.zip”

p@ubuntu:~/Desktop/tmp/tsan-linux-release-886199$ ./content_shell  --no-sandbox --js-flags='--expose_gc' --enable-blink-test-features --single-process --autoplay-policy=no-user-gesture-required --use-fake-device-for-media-stream --no-default-browser-check --disable-extensions

==================
WARNING: ThreadSanitizer: data race (pid=5018)
  Write of size 8 at 0x7b2000053048 by thread T20:
    #0 release buildtools/third_party/libc++/trunk/include/memory:1587:20 (content_shell+0xcc9ae9d)
    #1 unique_ptr buildtools/third_party/libc++/trunk/include/memory:1492:20 (content_shell+0xcc9ae9d)
    #2 KeyValuePair third_party/blink/renderer/platform/wtf/hash_traits.h:408:8 (content_shell+0xcc9ae9d)
    #3 Move third_party/blink/renderer/platform/wtf/hash_table.h:572:37 (content_shell+0xcc9ae9d)
    #4 WTF::HashTable<unsigned int, WTF::KeyValuePair<unsigned int, std::__1::unique_ptr<blink::FFTFrame::FFTSetup, 
..
SUMMARY: ThreadSanitizer: data race buildtools/third_party/libc++/trunk/include/memory:1587:20 in release
...

### rt...@chromium.org (2021-05-25)

[Empty comment from Monorail migration]

### rt...@chromium.org (2021-05-25)

Thanks for the test case and analysis.  I haven't tried to reproduce this yet, but will soon.  One thing I wanted to note is that FFTSetupUpSize is called from the convolver threads that are used in the convolver process.  Having the thread be blocked by the lock will introduce delays that might affect the output of the convolver producing glitches.  And convolvers can have pretty large impulse responses so FFTSetupForSize gets called a lot from the threads.

We'll have to look more closely at where all the call sites for FFTSetupForSize to see if this would not impact the convolver.

### [Deleted User] (2021-05-25)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-25)

[Empty comment from Monorail migration]

### rt...@chromium.org (2021-05-26)

My local linux tsan builds won't open a window so I can't do any tests. 

I'll have to figure that out why that's happening....

### rt...@chromium.org (2021-05-26)

Filed https://crbug.com/chromium/1213598 for the TSAN issue.

### m....@gmail.com (2021-05-27)

re #12
You can tested on content_shell or tsan-linux-stable-90.0.4430.93~

### rt...@chromium.org (2021-05-27)

Ah, I rarely ever need to run content_shell explicitly that I forgot about it.  It runs and reproduces the data race immediately.  While I could use the prebuilt tsan build, I want to have a local build for testing fixes to verify that it's actually fixed.

 Thanks for the reminder!  

### rt...@chromium.org (2021-05-27)

Does running the test case with an asan build trigger the UaF?  I don't get any failures locally.

### rt...@chromium.org (2021-05-27)

From the tsan logs, what's happening is that the PannerNode is setting up for the HRTF mode and computes a bunch of FFTs.  This is done in separate thread.  At the same time, the AnalyserNode is setting up the FFT object so that FFTs can be computed later.

In this case, it's ok to have the HRTF computations wait for a lock before computing the FFTs.

### ad...@google.com (2021-05-27)

rtoy@ it sounds like you've identified the root cause - could you confirm whether this affects M91, or if it's a more recent regression? If it affects M91 please could you set the label Security_Impact-Stable, which will enable sheriffbot to make all the right deciisions about merging/priority/release notes/etc. later. Thanks!

### rt...@chromium.org (2021-05-27)

The new part of the code that uses hash map instead of a vector landed in https://crrev.com/c/2785204, that landed in r867445.  Omahaproxy says that was in 91.0.4464.0 so it just made it into M91.

Updating labels.

### rt...@chromium.org (2021-05-27)

Reverting the change mentioned in https://crbug.com/chromium/1212599#c19 fixes the tsan race.  This will allow me some time to figure out how to do what I want with the hash table (which was to support non-power of two FFTs eventually).

### rt...@chromium.org (2021-05-27)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-28)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-06-02)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-06-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e34e28f6afc6844c95df347a19bca40496823979

commit e34e28f6afc6844c95df347a19bca40496823979
Author: Raymond Toy <rtoy@chromium.org>
Date: Wed Jun 02 23:14:16 2021

Initialize FFT HashMap with all possible keys

The HashMap that maps the FFT size to the setup data is initialized
with all of the valid FFT sizes with a nullptr for the setup data.
This means the keys of the HashMap never need to be updated; only the
setup data corresponding to the key needs updating.

Bug: 1212599
Change-Id: I60438e341f3b8f2a4512b3b0709fc99fb4119794
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2930542
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Commit-Queue: Raymond Toy <rtoy@chromium.org>
Cr-Commit-Position: refs/heads/master@{#888656}

[modify] https://crrev.com/e34e28f6afc6844c95df347a19bca40496823979/third_party/blink/renderer/platform/audio/pffft/fft_frame_pffft.cc


### rt...@chromium.org (2021-06-03)

The fix is now in Chrome  93.0.4531.0.  TSAN issue is fixed; I couldn't reproduce the original ASAN issue, but I think fixing TSAN fixes that as well.


### rt...@chromium.org (2021-06-04)

I'll let this bake over the weekend, and then we can consider merging this to M92 and possibly M91.

### [Deleted User] (2021-06-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-05)

Requesting merge to stable M91 because latest trunk commit (888656) appears to be after stable branch point (870763).

Requesting merge to beta M92 because latest trunk commit (888656) appears to be after beta branch point (885287).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-06-05)

This bug requires manual review: M92's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2021-06-07)

pls answer https://crbug.com/chromium/1212599#c30 for merge review. 

### rt...@chromium.org (2021-06-07)

1. Fits with the merge decision guidelines
2. https://chromium-review.googlesource.com/c/chromium/src/+/2930542
3. Yes. I did a TSAN build from ToT and used content_shell to run the test.  No failures
4. Yes, to M92
5. It's a race condition that very likely leads to a UaF.  (Unable to verify the ASAN UaF myself.)
6. No


### sr...@google.com (2021-06-08)

Merge approved for M92 branch:4515 pls merge asap

### gi...@appspot.gserviceaccount.com (2021-06-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d2e1eeb7abe8011d78fc2eed2ca55d8ef54edccc

commit d2e1eeb7abe8011d78fc2eed2ca55d8ef54edccc
Author: Raymond Toy <rtoy@chromium.org>
Date: Tue Jun 08 22:20:15 2021

Initialize FFT HashMap with all possible keys

The HashMap that maps the FFT size to the setup data is initialized
with all of the valid FFT sizes with a nullptr for the setup data.
This means the keys of the HashMap never need to be updated; only the
setup data corresponding to the key needs updating.

(cherry picked from commit e34e28f6afc6844c95df347a19bca40496823979)

Bug: 1212599
Change-Id: I60438e341f3b8f2a4512b3b0709fc99fb4119794
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2930542
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Commit-Queue: Raymond Toy <rtoy@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#888656}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2946280
Auto-Submit: Raymond Toy <rtoy@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4515@{#433}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[modify] https://crrev.com/d2e1eeb7abe8011d78fc2eed2ca55d8ef54edccc/third_party/blink/renderer/platform/audio/pffft/fft_frame_pffft.cc


### rt...@chromium.org (2021-06-08)

Let me know if this still needs to be merged to M91.  The M92 stable cut seems far away enough that we would want an M91 update.

### am...@google.com (2021-06-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-06-10)

Congratulations! The VRP Panel has decided to award you $7,500 for this report. Nice work! 

### m....@gmail.com (2021-06-11)

[Comment Deleted]

### am...@google.com (2021-06-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-06-15)

Merge approved for M91; please merge to branch 4472 as soon as possible/ before EOD tomorrow so this can be included in M91 security respin 

### rt...@chromium.org (2021-06-15)

CL for merge to M91 on its way:  https://chromium-review.googlesource.com/c/chromium/src/+/2965677


### gi...@appspot.gserviceaccount.com (2021-06-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0d0066a85064140025c868cff05a4cf61aebb8c3

commit 0d0066a85064140025c868cff05a4cf61aebb8c3
Author: Raymond Toy <rtoy@chromium.org>
Date: Wed Jun 16 02:27:08 2021

Initialize FFT HashMap with all possible keys

The HashMap that maps the FFT size to the setup data is initialized
with all of the valid FFT sizes with a nullptr for the setup data.
This means the keys of the HashMap never need to be updated; only the
setup data corresponding to the key needs updating.

(cherry picked from commit e34e28f6afc6844c95df347a19bca40496823979)

Bug: 1212599
Change-Id: I60438e341f3b8f2a4512b3b0709fc99fb4119794
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2930542
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Commit-Queue: Raymond Toy <rtoy@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#888656}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2965677
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Raymond Toy <rtoy@chromium.org>
Commit-Queue: Hongchan Choi <hongchan@chromium.org>
Cr-Commit-Position: refs/branch-heads/4472@{#1487}
Cr-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}

[modify] https://crrev.com/0d0066a85064140025c868cff05a4cf61aebb8c3/third_party/blink/renderer/platform/audio/pffft/fft_frame_pffft.cc


### am...@chromium.org (2021-06-17)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-17)

[Empty comment from Monorail migration]

### as...@google.com (2021-06-21)

[Empty comment from Monorail migration]

### gi...@google.com (2021-06-22)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-06-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/87dfa1af321f6ac7b9c6cd61534f82be455be9d9

commit 87dfa1af321f6ac7b9c6cd61534f82be455be9d9
Author: Artem Sumaneev <asumaneev@google.com>
Date: Tue Jun 22 12:46:05 2021

[M90-LTS] Initialize FFT HashMap with all possible keys

The HashMap that maps the FFT size to the setup data is initialized
with all of the valid FFT sizes with a nullptr for the setup data.
This means the keys of the HashMap never need to be updated; only the
setup data corresponding to the key needs updating.

M90 merge conflicts and resolution:
* third_party/blink/renderer/platform/audio/pffft/fft_frame_pffft.cc
  fft_setups are Vector in M90, the fix is picked with
  crrev.com/c/2785204, which updates setups to HashMap.

(cherry picked from commit e34e28f6afc6844c95df347a19bca40496823979)

(cherry picked from commit 0d0066a85064140025c868cff05a4cf61aebb8c3)

Bug: 1212599
Change-Id: I60438e341f3b8f2a4512b3b0709fc99fb4119794
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2930542
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Commit-Queue: Raymond Toy <rtoy@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#888656}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2965677
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Raymond Toy <rtoy@chromium.org>
Commit-Queue: Hongchan Choi <hongchan@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4472@{#1487}
Cr-Original-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2975764
Reviewed-by: Jana Grill <janagrill@google.com>
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Artem Sumaneev <asumaneev@google.com>
Owners-Override: Artem Sumaneev <asumaneev@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1531}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/87dfa1af321f6ac7b9c6cd61534f82be455be9d9/third_party/blink/renderer/platform/audio/fft_frame.h
[modify] https://crrev.com/87dfa1af321f6ac7b9c6cd61534f82be455be9d9/third_party/blink/renderer/platform/audio/pffft/fft_frame_pffft.cc


### as...@google.com (2021-06-22)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-06-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2a4354a12021affe58c951fa6a1d3679677dfa59

commit 2a4354a12021affe58c951fa6a1d3679677dfa59
Author: Artem Sumaneev <asumaneev@google.com>
Date: Tue Jun 22 12:52:03 2021

[M86-LTS] Initialize FFT HashMap with all possible keys

The HashMap that maps the FFT size to the setup data is initialized
with all of the valid FFT sizes with a nullptr for the setup data.
This means the keys of the HashMap never need to be updated; only the
setup data corresponding to the key needs updating.

M86 merge conflicts and resolution:
* third_party/blink/renderer/platform/audio/pffft/fft_frame_pffft.cc
  fft_setups are Vector in M86, the fix is picked with
  crrev.com/c/2785204, which updates setups to HashMap.

(cherry picked from commit e34e28f6afc6844c95df347a19bca40496823979)

(cherry picked from commit 0d0066a85064140025c868cff05a4cf61aebb8c3)

Bug: 1212599
Change-Id: I60438e341f3b8f2a4512b3b0709fc99fb4119794
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2930542
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Commit-Queue: Raymond Toy <rtoy@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#888656}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2965677
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Raymond Toy <rtoy@chromium.org>
Commit-Queue: Hongchan Choi <hongchan@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4472@{#1487}
Cr-Original-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2975761
Reviewed-by: Jana Grill <janagrill@google.com>
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Artem Sumaneev <asumaneev@google.com>
Owners-Override: Artem Sumaneev <asumaneev@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1674}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/2a4354a12021affe58c951fa6a1d3679677dfa59/third_party/blink/renderer/platform/audio/fft_frame.h
[modify] https://crrev.com/2a4354a12021affe58c951fa6a1d3679677dfa59/third_party/blink/renderer/platform/audio/pffft/fft_frame_pffft.cc


### as...@google.com (2021-06-22)

[Empty comment from Monorail migration]

### am...@google.com (2021-07-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1212599?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055980)*
