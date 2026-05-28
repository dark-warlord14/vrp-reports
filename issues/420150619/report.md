# Security: Race condition in AudioRendererImpl

| Field | Value |
|-------|-------|
| **Issue ID** | [420150619](https://issues.chromium.org/issues/420150619) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media>Video |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | asan-linux-release-1460407 |
| **Reporter** | su...@gmail.com |
| **Assignee** | mj...@chromium.org |
| **Created** | 2025-05-25 |
| **Bounty** | $8,000.00 |

## Description

# Steps to reproduce the problem

1. fetch asan-linux-release-1460407
2. serve poc.html and big-buck-bunny\_trailer.webm on port 8080
3. ./chrome --autoplay-policy=no-user-gesture-required <http://127.0.0.1:8080/poc.html>

Since this is a race condition issue, the POC cannot guarantee stable triggering. You can try a few more times.

# Problem Description

When the `HTMLMediaElement` loads a resource file, it creates a `WebMediaPlayerImpl` object in `HTMLMediaElement::StartPlayerLoad`, and subsequently calls `WebMediaPlayerImpl::Load`.

```
void HTMLMediaElement::StartPlayerLoad() {
  ...

  web_media_player_ =
      frame->Client()->CreateWebMediaPlayer(*this, source, this);

  ...

  auto load_timing = web_media_player_->Load(GetLoadType(), source, CorsMode(),
                                             is_cache_disabled);
  ...
}

```

In `WebMediaPlayerImpl::Load`, `WebMediaPlayerImpl::StartPipeline` is invoked to start the rendering pipeline. Then, `RendererImplFactory::CreateRenderer` is called to create an `AudioRendererImpl` object. The pointer to the `AudioRendererImpl` object is passed to `RendererImpl`.

```
std::unique_ptr<Renderer> RendererImplFactory::CreateRenderer(
    const scoped_refptr<base::SequencedTaskRunner>& media_task_runner,
    const scoped_refptr<base::TaskRunner>& worker_task_runner,
    AudioRendererSink* audio_renderer_sink,
    VideoRendererSink* video_renderer_sink,
    RequestOverlayInfoCB request_overlay_info_cb,
    const gfx::ColorSpace& target_color_space) {
  DCHECK(audio_renderer_sink);

  std::unique_ptr<AudioRenderer> audio_renderer(new AudioRendererImpl(
      media_task_runner, audio_renderer_sink,
      // Unretained is safe here, because the RendererFactory is guaranteed to
      // outlive the RendererImpl. The RendererImpl is destroyed when WMPI
      // destructor calls pipeline_controller_.Stop() -> PipelineImpl::Stop() ->
      // RendererWrapper::Stop -> RendererWrapper::DestroyRenderer(). And the
      // RendererFactory is owned by WMPI and gets called after WMPI destructor
      // finishes.
      base::BindRepeating(&RendererImplFactory::CreateAudioDecoders,
                          base::Unretained(this), media_task_runner),
      media_log_, media_player_id_
#if BUILDFLAG(IS_ANDROID)
      ));
#else
      ,
      speech_recognition_client_.get()));
#endif
  
  ...
  
  return std::make_unique<RendererImpl>(
      media_task_runner, std::move(audio_renderer), std::move(video_renderer));
}

```

When the Iframe is destroyed, that is, after `LocalDOMWindow::FrameDestroyed` is called, it triggers the callback `media::PipelineImpl::RendererWrapper::CompleteSuspend`. In this callback, `PipelineImpl::RendererWrapper::DestroyRenderer` is called to release the previously allocated `RendererImpl` object, and the corresponding `AudioRendererImpl` is also released. `PipelineImpl::RendererWrapper::DestroyRenderer` is executed in the Media thread.

```
void PipelineImpl::RendererWrapper::DestroyRenderer() {
  DCHECK(media_task_runner_->RunsTasksInCurrentSequence());

  // Destroy the renderer outside the lock scope to avoid holding the lock
  // while renderer is being destroyed (in case Renderer destructor is costly).
  std::unique_ptr<Renderer> renderer;
  {
    base::AutoLock auto_lock(shared_state_lock_);
    renderer.swap(shared_state_.renderer);
  }
}

```

At this time, the pointer to the `AudioRendererImpl` object is still being used in the AudioOutputDevice thread, causing a UAF issue.

```
int Render(base::TimeDelta delay,
            base::TimeTicks delay_timestamp,
            const media::AudioGlitchInfo& glitch_info,
            media::AudioBus* audio_bus) override {
  ...

  const int num_rendered_frames =
      renderer_->Render(delay, delay_timestamp, glitch_info, audio_bus);

  ...
}

```
# Summary

Security: Race condition in AudioRendererImpl

# Custom Questions

#### Type of crash:

tab

#### Crash state:

```
=================================================================
==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x756ff4952e98 at pc 0x572c7929ef02 bp 0x72c4e73fced0 sp 0x72c4e73fcec8
READ of size 1 at 0x756ff4952e98 thread T3144 (AudioOutputDevi)
==1==WARNING: invalid path to external symbolizer!
==1==WARNING: Failed to use and restart external symbolizer!
    #0 0x572c7929ef01 in base::internal::(anonymous namespace)::CrashImmediatelyOnUseAfterFree(unsigned long) _asan_rtl_:17
    #1 0x572c7929ea85 in base::internal::(anonymous namespace)::SafelyUnwrapForDereference(unsigned long) _asan_rtl_:5
    #2 0x572c88865663 in SafelyUnwrapPtrForDereference<media::AudioRendererSink::RenderCallback> ./../../base/allocator/partition_allocator/src/partition_alloc/pointers/raw_ptr_hookable_impl.h:84:9
    #3 0x572c88865663 in GetForDereference ./../../base/allocator/partition_allocator/src/partition_alloc/pointers/raw_ptr.h:996:12
    #4 0x572c88865663 in operator-> ./../../base/allocator/partition_allocator/src/partition_alloc/pointers/raw_ptr.h:665:12
    #5 0x572c88865663 in blink::WebAudioSourceProviderImpl::TeeFilter::Render(base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, media::AudioBus*) ./../../third_party/blink/renderer/platform/media/web_audio_source_provider_impl.cc:62:9
    #6 0x572c8d80d4af in blink::AudioRendererMixerInput::ProvideInput(media::AudioBus*, unsigned int, media::AudioGlitchInfo const&) ./../../third_party/blink/renderer/modules/media/audio/audio_renderer_mixer_input.cc:241:18
    #7 0x572c66603e51 in media::AudioConverter::SourceCallback(int, media::AudioBus*) ./../../media/base/audio_converter.cc:224:33
    #8 0x572c66603537 in media::AudioConverter::ProvideInput(int, media::AudioBus*) ./../../media/base/audio_converter.cc:266:5
    #9 0x572c66606046 in Invoke<void (AudioConverter::*)(int, media::AudioBus *), media::AudioConverter *, int, media::AudioBus *> ./../../base/functional/bind_internal.h:731:12
    #10 0x572c66606046 in MakeItSo<void (AudioConverter::*const &)(int, media::AudioBus *), const std::__Cr::tuple<base::internal::UnretainedWrapper<media::AudioConverter, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, int, media::AudioBus *> ./../../base/functional/bind_internal.h:923:12
    #11 0x572c66606046 in RunImpl<void (AudioConverter::*const &)(int, media::AudioBus *), const std::__Cr::tuple<base::internal::UnretainedWrapper<media::AudioConverter, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, 0UL> ./../../base/functional/bind_internal.h:1060:14
    #12 0x572c66606046 in base::internal::Invoker<base::internal::FunctorTraits<void (media::AudioConverter::* const&)(int, media::AudioBus*), media::AudioConverter*>, base::internal::BindState<true, true, false, void (media::AudioConverter::*)(int, media::AudioBus*), base::internal::UnretainedWrapper<media::AudioConverter, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (int, media::AudioBus*)>::Run(base::internal::BindStateBase*, int, media::AudioBus*) ./../../base/functional/bind_internal.h:980:12
    #13 0x572c66619950 in base::RepeatingCallback<void (int, media::AudioBus*)>::Run(int, media::AudioBus*) const & ./../../base/functional/callback.h:344:12
    #14 0x572c6669cf0c in media::MultiChannelResampler::ProvideInput(int, int, float*) ./../../media/base/multi_channel_resampler.cc:105:14
    #15 0x572c6669e3cd in Invoke<void (MultiChannelResampler::*)(int, int, float *), media::MultiChannelResampler *, const int &, int, float *> ./../../base/functional/bind_internal.h:731:12
    #16 0x572c6669e3cd in MakeItSo<void (MultiChannelResampler::*const &)(int, int, float *), const std::__Cr::tuple<base::internal::UnretainedWrapper<media::MultiChannelResampler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, int> &, int, float *> ./../../base/functional/bind_internal.h:923:12
    #17 0x572c6669e3cd in RunImpl<void (MultiChannelResampler::*const &)(int, int, float *), const std::__Cr::tuple<base::internal::UnretainedWrapper<media::MultiChannelResampler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, int> &, 0UL, 1UL> ./../../base/functional/bind_internal.h:1060:14
    #18 0x572c6669e3cd in base::internal::Invoker<base::internal::FunctorTraits<void (media::MultiChannelResampler::* const&)(int, int, float*), media::MultiChannelResampler*, int const&>, base::internal::BindState<true, true, false, void (media::MultiChannelResampler::*)(int, int, float*), base::internal::UnretainedWrapper<media::MultiChannelResampler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, int>, void (int, float*)>::Run(base::internal::BindStateBase*, int, float*) ./../../base/functional/bind_internal.h:980:12
    #19 0x572c666e73c0 in base::RepeatingCallback<void (int, float*)>::Run(int, float*) const & ./../../base/functional/callback.h:344:12
    #20 0x572c666e6ea2 in media::SincResampler::Resample(int, float*) ./../../media/base/sinc_resampler.cc:348:14
    #21 0x572c6669d4ba in media::MultiChannelResampler::Resample(int, media::AudioBus*) ./../../media/base/multi_channel_resampler.cc:59:21
    #22 0x572c66605b7a in media::AudioConverter::ConvertWithInfo(unsigned int, media::AudioGlitchInfo const&, media::AudioBus*) ./../../media/base/audio_converter.cc:160:19
    #23 0x572c6668269d in media::LoopbackAudioConverter::ProvideInput(media::AudioBus*, unsigned int, media::AudioGlitchInfo const&) ./../../media/base/loopback_audio_converter.cc:21:20
    #24 0x572c66603e51 in media::AudioConverter::SourceCallback(int, media::AudioBus*) ./../../media/base/audio_converter.cc:224:33
    #25 0x572c66605bf9 in media::AudioConverter::ConvertWithInfo(unsigned int, media::AudioGlitchInfo const&, media::AudioBus*) ./../../media/base/audio_converter.cc:157:5
    #26 0x572c8d8108fc in blink::AudioRendererMixer::Render(base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, media::AudioBus*) ./../../third_party/blink/renderer/modules/media/audio/audio_renderer_mixer.cc:155:24
    #27 0x572c66583d5b in media::AudioOutputDeviceThreadCallback::Process(unsigned int) ./../../media/audio/audio_output_device_thread_callback.cc:96:21
    #28 0x572c66554072 in media::AudioDeviceThread::ThreadMain() ./../../media/audio/audio_device_thread.cc:114:18
    #29 0x572c79531ede in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:103:13
    #30 0x572c6389b186 in asan_thread_start(void*) _asan_rtl_:28

0x756ff4952e98 is located 24 bytes inside of 552-byte region [0x756ff4952e80,0x756ff49530a8)
freed by thread T10 (Media) here:
    #0 0x572c638d7492 in operator delete(void*, unsigned long) _asan_rtl_:3
    #1 0x572c67c13a71 in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:76:5
    #2 0x572c67c13a71 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:287:7
    #3 0x572c67c13a71 in media::RendererImpl::~RendererImpl() ./../../media/renderers/renderer_impl.cc:128:19
    #4 0x572c67c14ab3 in media::RendererImpl::~RendererImpl() ./../../media/renderers/renderer_impl.cc:116:31
    #5 0x572c666ab313 in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:76:5
    #6 0x572c666ab313 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:287:7
    #7 0x572c666ab313 in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:256:71
    #8 0x572c666ab313 in DestroyRenderer ./../../media/base/pipeline_impl.cc:1191:1
    #9 0x572c666ab313 in media::PipelineImpl::RendererWrapper::CompleteSuspend(media::TypedStatus<media::PipelineStatusTraits>) ./../../media/base/pipeline_impl.cc:1083:3
    #10 0x572c666bd754 in void base::internal::DecayedFunctorTraits<void (media::PipelineImpl::RendererWrapper::*)(media::TypedStatus<media::PipelineStatusTraits>), base::WeakPtr<media::PipelineImpl::RendererWrapper>&&>::Invoke<void (media::PipelineImpl::RendererWrapper::*)(media::TypedStatus<media::PipelineStatusTraits>), base::WeakPtr<media::PipelineImpl::RendererWrapper> const&, media::TypedStatus<media::PipelineStatusTraits>>(void (media::PipelineImpl::RendererWrapper::*)(media::TypedStatus<media::PipelineStatusTraits>), base::WeakPtr<media::PipelineImpl::RendererWrapper> const&, media::TypedStatus<media::PipelineStatusTraits>&&) ./../../base/functional/bind_internal.h:731:12
    #11 0x572c666bd4f4 in MakeItSo<void (RendererWrapper::*)(media::TypedStatus<media::PipelineStatusTraits>), std::__Cr::tuple<base::WeakPtr<media::PipelineImpl::RendererWrapper> >, media::TypedStatus<media::PipelineStatusTraits> > ./../../base/functional/bind_internal.h:947:5
    #12 0x572c666bd4f4 in RunImpl<void (RendererWrapper::*)(media::TypedStatus<media::PipelineStatusTraits>), std::__Cr::tuple<base::WeakPtr<media::PipelineImpl::RendererWrapper> >, 0UL> ./../../base/functional/bind_internal.h:1060:14
    #13 0x572c666bd4f4 in base::internal::Invoker<base::internal::FunctorTraits<void (media::PipelineImpl::RendererWrapper::*&&)(media::TypedStatus<media::PipelineStatusTraits>), base::WeakPtr<media::PipelineImpl::RendererWrapper>&&>, base::internal::BindState<true, true, false, void (media::PipelineImpl::RendererWrapper::*)(media::TypedStatus<media::PipelineStatusTraits>), base::WeakPtr<media::PipelineImpl::RendererWrapper>>, void (media::TypedStatus<media::PipelineStatusTraits>)>::RunOnce(base::internal::BindStateBase*, media::TypedStatus<media::PipelineStatusTraits>&&) ./../../base/functional/bind_internal.h:973:12
    #14 0x572c666d6403 in Run ./../../base/functional/callback.h:156:12
    #15 0x572c666d6403 in media::SerialRunner::RunNextInSeries(media::TypedStatus<media::PipelineStatusTraits>) ./../../media/base/serial_runner.cc:100:25
    #16 0x572c666d7fb2 in void base::internal::DecayedFunctorTraits<void (media::SerialRunner::*)(media::TypedStatus<media::PipelineStatusTraits>), base::WeakPtr<media::SerialRunner>&&, media::PipelineStatusCodes&&>::Invoke<void (media::SerialRunner::*)(media::TypedStatus<media::PipelineStatusTraits>), base::WeakPtr<media::SerialRunner> const&, media::PipelineStatusCodes>(void (media::SerialRunner::*)(media::TypedStatus<media::PipelineStatusTraits>), base::WeakPtr<media::SerialRunner> const&, media::PipelineStatusCodes&&) ./../../base/functional/bind_internal.h:731:12
    #17 0x572c666d7d4c in MakeItSo<void (SerialRunner::*)(media::TypedStatus<media::PipelineStatusTraits>), std::__Cr::tuple<base::WeakPtr<media::SerialRunner>, media::PipelineStatusCodes> > ./../../base/functional/bind_internal.h:947:5
    #18 0x572c666d7d4c in RunImpl<void (SerialRunner::*)(media::TypedStatus<media::PipelineStatusTraits>), std::__Cr::tuple<base::WeakPtr<media::SerialRunner>, media::PipelineStatusCodes>, 0UL, 1UL> ./../../base/functional/bind_internal.h:1060:14
    #19 0x572c666d7d4c in base::internal::Invoker<base::internal::FunctorTraits<void (media::SerialRunner::*&&)(media::TypedStatus<media::PipelineStatusTraits>), base::WeakPtr<media::SerialRunner>&&, media::PipelineStatusCodes&&>, base::internal::BindState<true, true, false, void (media::SerialRunner::*)(media::TypedStatus<media::PipelineStatusTraits>), base::WeakPtr<media::SerialRunner>, media::PipelineStatusCodes>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:973:12
    #20 0x572c793e2086 in Run ./../../base/functional/callback.h:156:12
    #21 0x572c793e2086 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:209:34
    #22 0x572c79454b77 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:458:11)> ./../../base/task/common/task_annotator.h:106:5
    #23 0x572c79454b77 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:456:23
    #24 0x572c79453a5c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:330:40
    #25 0x572c7945566a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #26 0x572c792aae63 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:42:55
    #27 0x572c79456224 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:629:12
    #28 0x572c79364e0f in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #29 0x572c794d9ffc in base::Thread::Run(base::RunLoop*) ./../../base/threading/thread.cc:344:13
    #30 0x572c794da591 in base::Thread::ThreadMain() ./../../base/threading/thread.cc:419:3
    #31 0x572c79531ede in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:103:13
    #32 0x572c6389b186 in asan_thread_start(void*) _asan_rtl_:28

previously allocated by thread T0 (chrome) here:
    #0 0x572c638d682d in operator new(unsigned long) _asan_rtl_:3
    #1 0x572c67c28763 in media::RendererImplFactory::CreateRenderer(scoped_refptr<base::SequencedTaskRunner> const&, scoped_refptr<base::TaskRunner> const&, media::AudioRendererSink*, media::VideoRendererSink*, base::RepeatingCallback<void (bool, base::RepeatingCallback<void (media::OverlayInfo const&)>)>, gfx::ColorSpace const&) ./../../media/renderers/renderer_impl_factory.cc:89:49
    #2 0x572c8e32e7d9 in blink::WebMediaPlayerImpl::CreateRenderer(std::__Cr::optional<media::RendererType>) ./../../third_party/blink/renderer/platform/media/web_media_player_impl.cc:2999:59
    #3 0x572c8e35e110 in Invoke<std::__Cr::unique_ptr<media::Renderer, std::__Cr::default_delete<media::Renderer> > (WebMediaPlayerImpl::*)(std::__Cr::optional<media::RendererType>), blink::WebMediaPlayerImpl *, std::__Cr::optional<media::RendererType> > ./../../base/functional/bind_internal.h:731:12
    #4 0x572c8e35e110 in MakeItSo<std::__Cr::unique_ptr<media::Renderer, std::__Cr::default_delete<media::Renderer> > (WebMediaPlayerImpl::*const &)(std::__Cr::optional<media::RendererType>), const std::__Cr::tuple<WTF::UnretainedWrapper<blink::WebMediaPlayerImpl> > &, std::__Cr::optional<media::RendererType> > ./../../base/functional/bind_internal.h:923:12
    #5 0x572c8e35e110 in RunImpl<std::__Cr::unique_ptr<media::Renderer, std::__Cr::default_delete<media::Renderer> > (WebMediaPlayerImpl::*const &)(std::__Cr::optional<media::RendererType>), const std::__Cr::tuple<WTF::UnretainedWrapper<blink::WebMediaPlayerImpl> > &, 0UL> ./../../base/functional/bind_internal.h:1060:14
    #6 0x572c8e35e110 in base::internal::Invoker<base::internal::FunctorTraits<std::__Cr::unique_ptr<media::Renderer, std::__Cr::default_delete<media::Renderer>> (blink::WebMediaPlayerImpl::* const&)(std::__Cr::optional<media::RendererType>), blink::WebMediaPlayerImpl*>, base::internal::BindState<true, true, false, std::__Cr::unique_ptr<media::Renderer, std::__Cr::default_delete<media::Renderer>> (blink::WebMediaPlayerImpl::*)(std::__Cr::optional<media::RendererType>), WTF::UnretainedWrapper<blink::WebMediaPlayerImpl>>, std::__Cr::unique_ptr<media::Renderer, std::__Cr::default_delete<media::Renderer>> (std::__Cr::optional<media::RendererType>)>::Run(base::internal::BindStateBase*, std::__Cr::optional<media::RendererType>&&) ./../../base/functional/bind_internal.h:980:12
    #7 0x572c666b870d in base::RepeatingCallback<std::__Cr::unique_ptr<media::Renderer, std::__Cr::default_delete<media::Renderer>> (std::__Cr::optional<media::RendererType>)>::Run(std::__Cr::optional<media::RendererType>) const & ./../../base/functional/callback.h:344:12
    #8 0x572c666b810e in media::PipelineImpl::Start(media::Pipeline::StartType, media::Demuxer*, media::Pipeline::Client*, base::OnceCallback<void (media::TypedStatus<media::PipelineStatusTraits>)>) ./../../media/base/pipeline_impl.cc:1310:44
    #9 0x572c67a7dce1 in media::PipelineController::Start(media::Pipeline::StartType, media::Demuxer*, media::Pipeline::Client*, bool, bool) ./../../media/filters/pipeline_controller.cc:56:14
    #10 0x572c8e354c30 in blink::WebMediaPlayerImpl::OnDemuxerCreated(media::Demuxer*, media::Pipeline::StartType, bool, bool) ./../../third_party/blink/renderer/platform/media/web_media_player_impl.cc:3027:25
    #11 0x572c8e365a65 in Invoke<media::TypedStatus<media::PipelineStatusTraits> (WebMediaPlayerImpl::*)(media::Demuxer *, media::Pipeline::StartType, bool, bool), blink::WebMediaPlayerImpl *, media::Demuxer *, media::Pipeline::StartType, bool, bool> ./../../base/functional/bind_internal.h:731:12
    #12 0x572c8e365a65 in MakeItSo<media::TypedStatus<media::PipelineStatusTraits> (WebMediaPlayerImpl::*)(media::Demuxer *, media::Pipeline::StartType, bool, bool), std::__Cr::tuple<WTF::UnretainedWrapper<blink::WebMediaPlayerImpl> >, media::Demuxer *, media::Pipeline::StartType, bool, bool> ./../../base/functional/bind_internal.h:923:12
    #13 0x572c8e365a65 in RunImpl<media::TypedStatus<media::PipelineStatusTraits> (WebMediaPlayerImpl::*)(media::Demuxer *, media::Pipeline::StartType, bool, bool), std::__Cr::tuple<WTF::UnretainedWrapper<blink::WebMediaPlayerImpl> >, 0UL> ./../../base/functional/bind_internal.h:1060:14
    #14 0x572c8e365a65 in base::internal::Invoker<base::internal::FunctorTraits<media::TypedStatus<media::PipelineStatusTraits> (blink::WebMediaPlayerImpl::*&&)(media::Demuxer*, media::Pipeline::StartType, bool, bool), blink::WebMediaPlayerImpl*>, base::internal::BindState<true, true, false, media::TypedStatus<media::PipelineStatusTraits> (blink::WebMediaPlayerImpl::*)(media::Demuxer*, media::Pipeline::StartType, bool, bool), WTF::UnretainedWrapper<blink::WebMediaPlayerImpl>>, media::TypedStatus<media::PipelineStatusTraits> (media::Demuxer*, media::Pipeline::StartType, bool, bool)>::RunOnce(base::internal::BindStateBase*, media::Demuxer*, media::Pipeline::StartType, bool, bool) ./../../base/functional/bind_internal.h:973:12
    #15 0x572c67a5f442 in Run ./../../base/functional/callback.h:156:12
    #16 0x572c67a5f442 in media::DemuxerManager::CreateDemuxer(bool, media::DataSource::Preload, bool, base::OnceCallback<media::TypedStatus<media::PipelineStatusTraits> (media::Demuxer*, media::Pipeline::StartType, bool, bool)>, base::flat_map<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::less<void>, std::__Cr::vector<std::__Cr::pair<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>, std::__Cr::allocator<std::__Cr::pair<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>>>>) ./../../media/filters/demuxer_manager.cc:368:10
    #17 0x572c8e33b96e in blink::WebMediaPlayerImpl::StartPipeline() ./../../third_party/blink/renderer/platform/media/web_media_player_impl.cc:3054:49
    #18 0x572c8e354851 in blink::WebMediaPlayerImpl::DataSourceInitialized(bool) ./../../third_party/blink/renderer/platform/media/web_media_player_impl.cc:2846:3
    #19 0x572c8e33c400 in blink::WebMediaPlayerImpl::MultiBufferDataSourceInitialized(bool) ./../../third_party/blink/renderer/platform/media/web_media_player_impl.cc:2860:3
    #20 0x572c8e361cb9 in Invoke<void (WebMediaPlayerImpl::*)(bool), const base::WeakPtr<blink::WebMediaPlayerImpl> &, bool> ./../../base/functional/bind_internal.h:731:12
    #21 0x572c8e361cb9 in MakeItSo<void (WebMediaPlayerImpl::*)(bool), std::__Cr::tuple<base::WeakPtr<blink::WebMediaPlayerImpl> >, bool> ./../../base/functional/bind_internal.h:947:5
    #22 0x572c8e361cb9 in RunImpl<void (WebMediaPlayerImpl::*)(bool), std::__Cr::tuple<base::WeakPtr<blink::WebMediaPlayerImpl> >, 0UL> ./../../base/functional/bind_internal.h:1060:14
    #23 0x572c8e361cb9 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::WebMediaPlayerImpl::*&&)(bool), base::WeakPtr<blink::WebMediaPlayerImpl>&&>, base::internal::BindState<true, true, false, void (blink::WebMediaPlayerImpl::*)(bool), base::WeakPtr<blink::WebMediaPlayerImpl>>, void (bool)>::RunOnce(base::internal::BindStateBase*, bool) ./../../base/functional/bind_internal.h:973:12
    #24 0x572c640290cb in Run ./../../base/functional/callback.h:156:12
    #25 0x572c640290cb in Invoke<base::OnceCallback<void (bool)>, bool> ./../../base/functional/bind_internal.h:806:49
    #26 0x572c640290cb in MakeItSo<base::OnceCallback<void (bool)>, std::__Cr::tuple<bool> > ./../../base/functional/bind_internal.h:923:12
    #27 0x572c640290cb in RunImpl<base::OnceCallback<void (bool)>, std::__Cr::tuple<bool>, 0UL> ./../../base/functional/bind_internal.h:1060:14
    #28 0x572c640290cb in base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (bool)>&&, bool&&>, base::internal::BindState<false, true, true, base::OnceCallback<void (bool)>, bool>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:973:12
    #29 0x572c793e2086 in Run ./../../base/functional/callback.h:156:12
    #30 0x572c793e2086 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:209:34
    #31 0x572c79454b77 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:458:11)> ./../../base/task/common/task_annotator.h:106:5
    #32 0x572c79454b77 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:456:23
    #33 0x572c79453a5c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:330:40
    #34 0x572c7945566a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #35 0x572c792aae63 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:42:55
    #36 0x572c79456224 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:629:12
    #37 0x572c79364e0f in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #38 0x572c844d2d05 in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:356:16
    #39 0x572c760a7adc in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:699:14
    #40 0x572c760a8aac in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:803:12
    #41 0x572c760ab461 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1183:10
    #42 0x572c760a5819 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:374:36
    #43 0x572c760a5d3b in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:387:10
    #44 0x572c638d8157 in ChromeMain ./../../chrome/app/chrome_main.cc:222:12
    #45 0x780ff5a29d8f in errx ??:?

Thread T3144 (AudioOutputDevi) created by T4 (Chrome_ChildIOT) here:
    #0 0x572c63881891 in ___interceptor_pthread_create _asan_rtl_:3
    #1 0x572c795314c8 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) ./../../base/threading/platform_thread_posix.cc:151:13
    #2 0x572c665538b7 in media::AudioDeviceThread::AudioDeviceThread(media::AudioDeviceThread::Callback*, base::ScopedGeneric<int, base::internal::ScopedFDCloseTraits>, char const*, base::ThreadType) ./../../media/audio/audio_device_thread.cc:66:3
    #3 0x572c6657d368 in std::__Cr::unique_ptr<media::AudioDeviceThread, std::__Cr::default_delete<media::AudioDeviceThread>> std::__Cr::make_unique<media::AudioDeviceThread, media::AudioOutputDeviceThreadCallback*, base::ScopedGeneric<int, base::internal::ScopedFDCloseTraits>, char const (&) [18], base::ThreadType, 0>(media::AudioOutputDeviceThreadCallback*&&, base::ScopedGeneric<int, base::internal::ScopedFDCloseTraits>&&, char const (&) [18], base::ThreadType&&) ./../../third_party/libc++/src/include/__memory/unique_ptr.h:754:30
    #4 0x572c6657cf61 in media::AudioOutputDevice::OnStreamCreated(base::UnsafeSharedMemoryRegion, base::ScopedGeneric<int, base::internal::ScopedFDCloseTraits>, bool) ./../../media/audio/audio_output_device.cc:430:21
    #5 0x572c8d82569d in blink::MojoAudioOutputIPC::Created(mojo::PendingRemote<media::mojom::blink::AudioOutputStream>, mojo::StructPtr<media::mojom::blink::ReadWriteAudioDataPipe>) ./../../third_party/blink/renderer/modules/media/audio/mojo_audio_output_ipc.cc:243:14
    #6 0x572c72f96264 in media::mojom::blink::AudioOutputStreamProviderClientStubDispatch::Accept(media::mojom::blink::AudioOutputStreamProviderClient*, mojo::Message*) ./gen/media/mojo/mojom/audio_output_stream.mojom-blink.cc:1156:13
    #7 0x572c791bd6ef in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1059:54
    #8 0x572c791db13a in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #9 0x572c791c3434 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:731:20
    #10 0x572c791eaf5a in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:1120:42
    #11 0x572c791e9466 in mojo::internal::MultiplexRouter::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:733:7
    #12 0x572c791db13a in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #13 0x572c791b4858 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) ./../../mojo/public/cpp/bindings/lib/connector.cc:561:49
    #14 0x572c791b5fd0 in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:619:14
    #15 0x572c791b59f9 in OnHandleReadyInternal ./../../mojo/public/cpp/bindings/lib/connector.cc:450:3
    #16 0x572c791b59f9 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int) ./../../mojo/public/cpp/bindings/lib/connector.cc:416:3
    #17 0x572c791b787a in Invoke<void (Connector::*)(const char *, unsigned int), mojo::Connector *, const char *, unsigned int> ./../../base/functional/bind_internal.h:731:12
    #18 0x572c791b787a in MakeItSo<void (Connector::*const &)(const char *, unsigned int), const std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<const char, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, unsigned int> ./../../base/functional/bind_internal.h:923:12
    #19 0x572c791b787a in RunImpl<void (Connector::*const &)(const char *, unsigned int), const std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<const char, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, 0UL, 1UL> ./../../base/functional/bind_internal.h:1060:14
    #20 0x572c791b787a in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int) ./../../base/functional/bind_internal.h:980:12
    #21 0x572c68b1648e in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const & ./../../base/functional/callback.h:344:12
    #22 0x572c68b1621f in Invoke<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind_internal.h:664:12
    #23 0x572c68b1621f in MakeItSo<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind_internal.h:923:12
    #24 0x572c68b1621f in RunImpl<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, 0UL> ./../../base/functional/bind_internal.h:1060:14
    #25 0x572c68b1621f in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&) ./../../base/functional/bind_internal.h:980:12
    #26 0x572c79f2c560 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const & ./../../base/functional/callback.h:344:12
    #27 0x572c79f2be98 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple_watcher.cc:278:14
    #28 0x572c79f2c946 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) ./../../mojo/public/cpp/system/simple_watcher.cc:96:22
    #29 0x572c79f291e5 in mojo::SimpleWatcher::Context::CallNotify(MojoTrapEvent const*) ./../../mojo/public/cpp/system/simple_watcher.cc:61:14
    #30 0x572c63ec781d in DispatchEvent ./../../mojo/core/ipcz_driver/mojo_trap.cc:612:3
    #31 0x572c63ec781d in mojo::core::ipcz_driver::MojoTrap::DispatchOrQueueEvent(mojo::core::ipcz_driver::MojoTrap::Trigger&, MojoTrapEvent const&) ./../../mojo/core/ipcz_driver/mojo_trap.cc:584:5
    #32 0x572c63eca17a in mojo::core::ipcz_driver::MojoTrap::HandleEvent(IpczTrapEvent const&) ./../../mojo/core/ipcz_driver/mojo_trap.cc:466:3
    #33 0x572c64434e81 in DispatchAll ./../../third_party/ipcz/src/ipcz/trap_event_dispatcher.cc:30:5
    #34 0x572c64434e81 in ipcz::TrapEventDispatcher::~TrapEventDispatcher() ./../../third_party/ipcz/src/ipcz/trap_event_dispatcher.cc:12:3
    #35 0x572c64417621 in ipcz::Router::AcceptInboundParcel(std::__Cr::unique_ptr<ipcz::Parcel, std::__Cr::default_delete<ipcz::Parcel>>) ./../../third_party/ipcz/src/ipcz/router.cc:274:1
    #36 0x572c643e5c45 in ipcz::NodeLink::AcceptCompleteParcel(ipcz::StrongAlias<ipcz::SublinkIdTag, unsigned long>, std::__Cr::unique_ptr<ipcz::Parcel, std::__Cr::default_delete<ipcz::Parcel>>) ./../../third_party/ipcz/src/ipcz/node_link.cc:1051:31
    #37 0x572c643e47bb in ipcz::NodeLink::OnAcceptParcel(ipcz::msg::AcceptParcel&) ./../../third_party/ipcz/src/ipcz/node_link.cc:642:10
    #38 0x572c64404939 in ipcz::msg::NodeMessageListener::OnTransportMessage(ipcz::DriverTransport::RawMessage const&, ipcz::DriverTransport const&, unsigned long) ./../../third_party/ipcz/src/ipcz/node_messages_generator.h:357:1
    #39 0x572c643a80cc in Notify ./../../third_party/ipcz/src/ipcz/driver_transport.cc:129:20
    #40 0x572c643a80cc in ipcz::(anonymous namespace)::NotifyTransport(unsigned long, void const*, unsigned long, unsigned long const*, unsigned long, unsigned int, IpczTransportActivityOptions const*) ./../../third_party/ipcz/src/ipcz/driver_transport.cc:47:11
    #41 0x572c63ede75e in mojo::core::ipcz_driver::Transport::OnChannelMessage(void const*, unsigned long, std::__Cr::vector<mojo::PlatformHandle, std::__Cr::allocator<mojo::PlatformHandle>>, scoped_refptr<mojo::core::ipcz_driver::Envelope>) ./../../mojo/core/ipcz_driver/transport.cc:738:29
    #42 0x572c63e9cf3e in mojo::core::Channel::TryDispatchMessage(base::span<char const, 18446744073709551615ul, char const*>, std::__Cr::optional<std::__Cr::vector<mojo::PlatformHandle, std::__Cr::allocator<mojo::PlatformHandle>>>, scoped_refptr<mojo::core::ipcz_driver::Envelope>, unsigned long*) ./../../mojo/core/channel.cc:1056:16
    #43 0x572c63e9b4b7 in TryDispatchMessage ./../../mojo/core/channel.cc:1000:10
    #44 0x572c63e9b4b7 in mojo::core::Channel::OnReadComplete(unsigned long, unsigned long*) ./../../mojo/core/channel.cc:977:9
    #45 0x572c63eea2df in mojo::core::ChannelPosix::OnFdReadable(int) ./../../mojo/core/channel_posix.cc:307:12
    #46 0x572c795c0fb5 in OnFdReadable ./../../base/message_loop/message_pump_epoll.cc:764:13
    #47 0x572c795c0fb5 in base::MessagePumpEpoll::HandleEvent(int, bool, bool, base::MessagePumpEpoll::FdWatchController*) ./../../base/message_loop/message_pump_epoll.cc:672:17
    #48 0x572c795bff5a in base::MessagePumpEpoll::OnEpollEvent(base::MessagePumpEpoll::EpollEventEntry&, unsigned int) ./../../base/message_loop/message_pump_epoll.cc:618:7
    #49 0x572c795be276 in base::MessagePumpEpoll::WaitForEpollEvents(base::TimeDelta) ./../../base/message_loop/message_pump_epoll.cc:509:7
    #50 0x572c795bcdd9 in base::MessagePumpEpoll::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_epoll.cc:288:5
    #51 0x572c79456224 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:629:12
    #52 0x572c79364e0f in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #53 0x572c794d9ffc in base::Thread::Run(base::RunLoop*) ./../../base/threading/thread.cc:344:13
    #54 0x572c842d4637 in content::(anonymous namespace)::ChildIOThread::Run(base::RunLoop*) ./../../content/child/child_process.cc:60:19
    #55 0x572c794da591 in base::Thread::ThreadMain() ./../../base/threading/thread.cc:419:3
    #56 0x572c79531ede in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:103:13
    #57 0x572c6389b186 in asan_thread_start(void*) _asan_rtl_:28

Thread T4 (Chrome_ChildIOT) created by T0 (chrome) here:
    #0 0x572c63881891 in ___interceptor_pthread_create _asan_rtl_:3
    #1 0x572c795314c8 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) ./../../base/threading/platform_thread_posix.cc:151:13
    #2 0x572c794d9303 in base::Thread::StartWithOptions(base::Thread::Options) ./../../base/threading/thread.cc:211:26
    #3 0x572c842d34a9 in content::ChildProcess::ChildProcess(base::ThreadType, std::__Cr::unique_ptr<base::ThreadPoolInstance::InitParams, std::__Cr::default_delete<base::ThreadPoolInstance::InitParams>>) ./../../content/child/child_process.cc:125:3
    #4 0x572c8444a7cb in content::RenderProcess::RenderProcess(std::__Cr::unique_ptr<base::ThreadPoolInstance::InitParams, std::__Cr::default_delete<base::ThreadPoolInstance::InitParams>>) ./../../content/renderer/render_process.cc:18:7
    #5 0x572c8444a055 in content::RenderProcessImpl::RenderProcessImpl() ./../../content/renderer/render_process_impl.cc:112:7
    #6 0x572c8444a5b0 in content::RenderProcessImpl::Create() ./../../content/renderer/render_process_impl.cc:231:31
    #7 0x572c844d27e9 in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:274:53
    #8 0x572c760a7adc in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:699:14
    #9 0x572c760a8aac in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:803:12
    #10 0x572c760ab461 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1183:10
    #11 0x572c760a5819 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:374:36
    #12 0x572c760a5d3b in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:387:10
    #13 0x572c638d8157 in ChromeMain ./../../chrome/app/chrome_main.cc:222:12
    #14 0x780ff5a29d8f in errx ??:?

Thread T10 (Media) created by T0 (chrome) here:
    #0 0x572c63881891 in ___interceptor_pthread_create _asan_rtl_:3
    #1 0x572c795314c8 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) ./../../base/threading/platform_thread_posix.cc:151:13
    #2 0x572c794d9303 in base::Thread::StartWithOptions(base::Thread::Options) ./../../base/threading/thread.cc:211:26
    #3 0x572c8445835a in content::RenderThreadImpl::GetMediaSequencedTaskRunner() ./../../content/renderer/render_thread_impl.cc:1698:20
    #4 0x572c843c8361 in content::MediaFactory::CreateMediaPlayer(blink::WebMediaPlayerSource const&, blink::WebMediaPlayerClient*, blink::MediaInspectorContext*, blink::WebMediaPlayerEncryptedMediaClient*, blink::WebContentDecryptionModule*, blink::WebString const&, viz::FrameSinkId, cc::LayerTreeSettings const&, scoped_refptr<base::SingleThreadTaskRunner>, scoped_refptr<base::TaskRunner>) ./../../content/renderer/media/media_factory.cc:465:22
    #5 0x572c843353e8 in content::RenderFrameImpl::CreateMediaPlayer(blink::WebMediaPlayerSource const&, blink::WebMediaPlayerClient*, blink::MediaInspectorContext*, blink::WebMediaPlayerEncryptedMediaClient*, blink::WebContentDecryptionModule*, blink::WebString const&, cc::LayerTreeSettings const*, scoped_refptr<base::TaskRunner>) ./../../content/renderer/render_frame_impl.cc:3546:25
    #6 0x572c8a0e412a in blink::ModulesInitializer::CreateWebMediaPlayer(blink::WebLocalFrameClient*, blink::HTMLMediaElement&, blink::WebMediaPlayerSource const&, blink::WebMediaPlayerClient*) const ./../../third_party/blink/renderer/modules/modules_initializer.cc:357:28
    #7 0x572c861a0196 in blink::HTMLMediaElement::StartPlayerLoad() ./../../third_party/blink/renderer/core/html/media/html_media_element.cc:1625:24
    #8 0x572c8619c4a3 in blink::HTMLMediaElement::LoadResource(blink::WebMediaPlayerSource const&, WTF::String const&) ./../../third_party/blink/renderer/core/html/media/html_media_element.cc:1480:7
    #9 0x572c8619833f in blink::HTMLMediaElement::LoadSourceFromAttribute() ./../../third_party/blink/renderer/core/html/media/html_media_element.cc:1342:3
    #10 0x572c86196a6b in blink::HTMLMediaElement::SelectMediaResource() ./../../third_party/blink/renderer/core/html/media/html_media_element.cc:1269:7
    #11 0x572c86192262 in blink::HTMLMediaElement::LoadInternal() ./../../third_party/blink/renderer/core/html/media/html_media_element.cc:1204:3
    #12 0x572c86187ec8 in blink::HTMLMediaElement::LoadTimerFired(blink::TimerBase*) ./../../third_party/blink/renderer/core/html/media/html_media_element.cc:930:7
    #13 0x572c888f96ad in blink::TimerBase::RunInternal() ./../../third_party/blink/renderer/platform/timer.cc:166:3
    #14 0x572c861d26c1 in Invoke<void (*)(blink::HeapTaskRunnerTimer<blink::HTMLMediaElement> *, blink::HTMLMediaElement *), blink::HeapTaskRunnerTimer<blink::HTMLMediaElement> *, cppgc::internal::BasicPersistent<blink::HTMLMediaElement, cppgc::internal::WeakPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy> > ./../../base/functional/bind_internal.h:664:12
    #15 0x572c861d26c1 in MakeItSo<void (*)(blink::HeapTaskRunnerTimer<blink::HTMLMediaElement> *, blink::HTMLMediaElement *), std::__Cr::tuple<WTF::UnretainedWrapper<blink::HeapTaskRunnerTimer<blink::HTMLMediaElement> >, cppgc::internal::BasicPersistent<blink::HTMLMediaElement, cppgc::internal::WeakPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy> > > ./../../base/functional/bind_internal.h:923:12
    #16 0x572c861d26c1 in RunImpl<void (*)(blink::HeapTaskRunnerTimer<blink::HTMLMediaElement> *, blink::HTMLMediaElement *), std::__Cr::tuple<WTF::UnretainedWrapper<blink::HeapTaskRunnerTimer<blink::HTMLMediaElement> >, cppgc::internal::BasicPersistent<blink::HTMLMediaElement, cppgc::internal::WeakPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy> >, 0UL, 1UL> ./../../base/functional/bind_internal.h:1060:14
    #17 0x572c861d26c1 in base::internal::Invoker<base::internal::FunctorTraits<void (*&&)(blink::HeapTaskRunnerTimer<blink::HTMLMediaElement>*, blink::HTMLMediaElement*), blink::HeapTaskRunnerTimer<blink::HTMLMediaElement>*, cppgc::internal::BasicPersistent<blink::HTMLMediaElement, cppgc::internal::WeakPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>&&>, base::internal::BindState<false, true, false, void (*)(blink::HeapTaskRunnerTimer<blink::HTMLMediaElement>*, blink::HTMLMediaElement*), WTF::UnretainedWrapper<blink::HeapTaskRunnerTimer<blink::HTMLMediaElement>>, cppgc::internal::BasicPersistent<blink::HTMLMediaElement, cppgc::internal::WeakPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:973:12
    #18 0x572c793e2086 in Run ./../../base/functional/callback.h:156:12
    #19 0x572c793e2086 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:209:34
    #20 0x572c79454b77 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:458:11)> ./../../base/task/common/task_annotator.h:106:5
    #21 0x572c79454b77 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:456:23
    #22 0x572c79453a5c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:330:40
    #23 0x572c7945566a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #24 0x572c792aae63 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:42:55
    #25 0x572c79456224 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:629:12
    #26 0x572c79364e0f in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #27 0x572c844d2d05 in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:356:16
    #28 0x572c760a7adc in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:699:14
    #29 0x572c760a8aac in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:803:12
    #30 0x572c760ab461 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1183:10
    #31 0x572c760a5819 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:374:36
    #32 0x572c760a5d3b in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:387:10
    #33 0x572c638d8157 in ChromeMain ./../../chrome/app/chrome_main.cc:222:12
    #34 0x780ff5a29d8f in errx ??:?

SUMMARY: AddressSanitizer: heap-use-after-free (asan-linux-release-1460407/chrome+0x2550cf01) (BuildId: 07ee9f0d0206f4b6)
Shadow bytes around the buggy address:
  0x756ff4952c00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x756ff4952c80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x756ff4952d00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x756ff4952d80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x756ff4952e00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
=>0x756ff4952e80: fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd
  0x756ff4952f00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x756ff4952f80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x756ff4953000: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x756ff4953080: fd fd fd fd fd fa fa fa fa fa fa fa fa fa fa fa
  0x756ff4953100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
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

==1==ADDITIONAL INFO

==1==Note: Please include this section with the ASan report.
Task trace:

Command line: `/proc/self/exe --type=renderer --crashpad-handler-pid=123756 --enable-crash-reporter=, --change-stack-guard-on-fork=enable --autoplay-policy=no-user-gesture-required --file-url-path-alias=/gen=asan-linux-release-1460407/gen --ozone-platform=wayland --disable-gpu-compositing --lang=en-US --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=5 --time-ticks-at-unix-epoch=-1747394574300974 --launch-time-ticks=251374854937 --shared-files=v8_context_snapshot_data:100 --metrics-shmem-handle=4,i,14665207153857744594,12260671244325860807,2097152 --field-trial-handle=3,i,12642760950729403537,12599755197160342593,262144 --disable-features=EyeDropper --variations-seed-version`

MiraclePtr Status: MANUAL ANALYSIS REQUIRED
This crash occurred while a raw_ptr<T> object containing a dangling pointer was being dereferenced.
The "use" and "free" threads don't match. This crash is likely to have been caused by a race condition that is mislabeled as a use-after-free. Make sure that the "free" is sequenced after the "use" (e.g. both are on the same sequence, or the "free" is in a task posted after the "use"). Otherwise, the crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==1==END OF ADDITIONAL INFO
==1==ABORTING

```
#### Reporter credit:

Huang Xilin of Ant Group Light-Year Security Lab

# Additional Data

Category: Security   

Chrome Channel: Dev   

Regression: N/A

## Attachments

- [poc.html](attachments/poc.html) (text/html, 3.1 KB)
- [big-buck-bunny_trailer.webm](attachments/big-buck-bunny_trailer.webm) (video/webm, 2.1 MB)
- [poc.html](attachments/poc.html) (text/html, 3.1 KB)

## Timeline

### su...@gmail.com (2025-05-25)

Bisect: <https://source.chromium.org/chromium/chromium/src/+/610196b281d2ea861996de949f80e47cb2c28cea>

### cl...@appspot.gserviceaccount.com (2025-05-26)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6223372610371584.

### pa...@chromium.org (2025-05-26)

[security shepherd] Could not reproduce as is, but a slightly modified version of the testcase did the trick. I could at least reproduce on dev. Setting Sev-High for now.

### pa...@chromium.org (2025-05-26)

Launched CF with the new testcase to get OS and FoundIn.

### 24...@project.gserviceaccount.com (2025-05-26)

Testcase 6223372610371584 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6223372610371584.

### 24...@project.gserviceaccount.com (2025-05-26)

Testcase 6223372610371584 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6223372610371584.

### 24...@project.gserviceaccount.com (2025-05-26)

ClusterFuzz testcase 6223372610371584 appears to be flaky, updating reproducibility hotlist.

### da...@chromium.org (2025-05-27)

Hmm, `~AudioRendererImpl` stops the sink before destructing:

- <https://source.chromium.org/chromium/chromium/src/+/main:media/renderers/audio_renderer_impl.cc;l=110;drc=1aa30237013ab1efb8ce9f0e5dfd55b67dc55071>

Which is supposed to disconnect it and prevent this from happening. It's not immediately clear to me why that's not working here.

### da...@chromium.org (2025-05-27)

Oh I missed the bisect above, it's due to <https://chromium-review.googlesource.com/c/chromium/src/+/6444424> which delays the `Stop()` call incorrectly in this case. I'll disable the feature for now.

### ch...@google.com (2025-05-28)

Setting milestone because of s0/s1 severity.

### dx...@google.com (2025-05-28)

Project: chromium/src  

Branch: main  

Author: Dale Curtis [dalecurtis@chromium.org](mailto:dalecurtis@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6594254>

Disable DelayStopForMediaElementSourceNode feature.

---


Expand for full commit details
```
     
    It's leading to some crashes that need to be fixed first. 
     
    R=mjwilson 
     
    Bug: 420150619 
    Change-Id: Ia0cee190bd08dda26f27d2e36fa42ff0b1da5438 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6594254 
    Commit-Queue: Michael Wilson <mjwilson@chromium.org> 
    Auto-Submit: Dale Curtis <dalecurtis@chromium.org> 
    Reviewed-by: Michael Wilson <mjwilson@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1466488}

```

---

Files:

- M `third_party/blink/renderer/platform/media/web_audio_source_provider_impl.cc`
- M `third_party/blink/renderer/platform/media/web_audio_source_provider_impl_test.cc`

---

Hash: 5d1549a771f8a35b9c1e02df27013dc4e1d4ec30  

Date:  Wed May 28 15:20:20 2025


---

### mj...@chromium.org (2025-05-28)

Using the poc in [#comment4](https://issues.chromium.org/issues/420150619#comment4), I verified that <https://crrev.com/c/6594254> fixes the issue. I will set this issue to fixed and start the merge request process.

### ch...@google.com (2025-05-28)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2025-05-28)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), pbommana (Desktop US), danielyip (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2025-05-28)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: andywu (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### mj...@chromium.org (2025-05-28)

1. Important security issues (medium severity or higher)
2. <https://crrev.com/c/6594254>
3. No. The change is merged on main, and should be released in the next canary. I tested and verified locally.
4. No. The original feature was behind a flag guard, and the change turns off the original feature via the flag.
5. N/A
6. No, we shouldn't need the test team to verify.

Also, I realized the original change that introduced the bug landed in M137 so there is nothing to do in M136. I will adjust the Milestone and Merge fields appropriately.

### pg...@google.com (2025-05-29)

updating foundIn as well (thanks for updating the other labels!!)

(Since the fix just landed just a day ago, we will give this bug some more time in Canary before back merging to older branches. but this is on our radar (: )

### am...@chromium.org (2025-06-03)

while I was reviewing Canary data related to this change disabling this feature, I ran into four crashes related to blink::WebAudioMediaStreamSource::SetFormat that should probably be looked at, just to ensure there are no issues with that

As long as there are no issues related to backmerging this change, approving merges to M137 and M138.
Please merge <https://crrev.com/c/6594254> to M138 / branch 7204 and M137 / branch 7151 at your earliest convenience, NLT EOD Thursday, 5 June.

### mj...@chromium.org (2025-06-04)

The crashes I see in blink::WebAudioMediaStreamSource::SetFormat seem to be DCHECK failures for the thread checker (<https://crsrc.org/c/third_party/blink/renderer/platform/mediastream/webaudio_media_stream_source.cc;l=33>) which is a concerning, but should be unrelated to this issue. I will start the backmerges.

### dx...@google.com (2025-06-04)

Project: chromium/src  

Branch: refs/branch-heads/7151  

Author: Dale Curtis [dalecurtis@chromium.org](mailto:dalecurtis@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6619533>

[M137] Disable DelayStopForMediaElementSourceNode feature.

---


Expand for full commit details
```
     
    It's leading to some crashes that need to be fixed first. 
     
    R=mjwilson 
     
    (cherry picked from commit 5d1549a771f8a35b9c1e02df27013dc4e1d4ec30) 
     
    Bug: 420150619 
    Change-Id: Ia0cee190bd08dda26f27d2e36fa42ff0b1da5438 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6594254 
    Commit-Queue: Michael Wilson <mjwilson@chromium.org> 
    Auto-Submit: Dale Curtis <dalecurtis@chromium.org> 
    Reviewed-by: Michael Wilson <mjwilson@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1466488} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6619533 
    Auto-Submit: Michael Wilson <mjwilson@chromium.org> 
    Reviewed-by: Dale Curtis <dalecurtis@chromium.org> 
    Commit-Queue: Dale Curtis <dalecurtis@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7151@{#1915} 
    Cr-Branched-From: 8e0d32ed6e49a2415b16e5ed402957cac2349ce2-refs/heads/main@{#1453031}

```

---

Files:

- M `third_party/blink/renderer/platform/media/web_audio_source_provider_impl.cc`
- M `third_party/blink/renderer/platform/media/web_audio_source_provider_impl_test.cc`

---

Hash: d36d9a59adbd318d170cccb717dd3357178ab62d  

Date:  Wed Jun 4 18:41:14 2025


---

### pe...@google.com (2025-06-04)

LTS Milestone M132

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### mj...@chromium.org (2025-06-04)

#comment22

1. No, it is a new bug.
2. No, I think the latest LTS milestone is 138 and this issue is related to a change which was merged before this in M137.

### dx...@google.com (2025-06-04)

Project: chromium/src  

Branch: refs/branch-heads/7204  

Author: Dale Curtis [dalecurtis@chromium.org](mailto:dalecurtis@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6617517>

[M138] Disable DelayStopForMediaElementSourceNode feature.

---


Expand for full commit details
```
     
    It's leading to some crashes that need to be fixed first. 
     
    R=mjwilson 
     
    (cherry picked from commit 5d1549a771f8a35b9c1e02df27013dc4e1d4ec30) 
     
    Bug: 420150619 
    Change-Id: Ia0cee190bd08dda26f27d2e36fa42ff0b1da5438 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6594254 
    Commit-Queue: Michael Wilson <mjwilson@chromium.org> 
    Auto-Submit: Dale Curtis <dalecurtis@chromium.org> 
    Reviewed-by: Michael Wilson <mjwilson@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1466488} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6617517 
    Reviewed-by: Dale Curtis <dalecurtis@chromium.org> 
    Auto-Submit: Michael Wilson <mjwilson@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7204@{#554} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `third_party/blink/renderer/platform/media/web_audio_source_provider_impl.cc`
- M `third_party/blink/renderer/platform/media/web_audio_source_provider_impl_test.cc`

---

Hash: 2b3f39392152a07129c5600420ea570325e0eeb5  

Date:  Wed Jun 4 19:35:52 2025


---

### sp...@google.com (2025-06-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
$7,000 for report of memory corruption in a sandboxed process / renderer + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-06-04)

Thank you for your efforts and reporting this issue to us.

### qk...@google.com (2025-06-06)

Labelling as not applicable for LTS 132 because the suspected CL[1] was landed in M137 according to comment #17 and #23.


### ch...@google.com (2025-09-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/420150619)*
