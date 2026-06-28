# Security: heap-use-after-free in blink::WebAudioSourceProviderImpl::TeeFilter::Render

| Field | Value |
|-------|-------|
| **Issue ID** | [488188176](https://issues.chromium.org/issues/488188176) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebAudio |
| **Platforms** | Mac |
| **Chrome Version** | 145.0.0.0 |
| **Reporter** | zh...@gmail.com |
| **Assignee** | km...@google.com |
| **Created** | 2026-02-27 |
| **Bounty** | $8,000.00 |

## Description

# Steps to reproduce the problem

1. compile asan chromium on MacOS:

```
git checkout da4487887d1ce22cb50ce4e407320dc5f2573b27
gn gen out/asan-0227 --args="is_component_build=true is_debug=false is_asan=true symbol_level=2 dcheck_always_on=false treat_warnings_as_errors=false"

```

2. run asan chromium on MacOS:

```
./out/asan-0227/Chromium.app/Contents/MacOS/Chromium --no-sandbox --user-data-dir=/tmp/userdata/t1  --enable-features=WebMachineLearningNeuralNetwork,DelayStopForMediaElementSourceNode --enable-unsafe-webgpu --js-flags=--expose-gc --enable-logging --v=1 http://127.0.0.1/index.html --autoplay-policy=no-user-gesture-required

```
# Problem Description

RCA and Bisect coming soon!

# Summary

Security: heap-use-after-free in blink::WebAudioSourceProviderImpl::TeeFilter::Render

# Custom Questions

#### Type of crash:

--type=renderer

#### Crash state:

```
=================================================================
==76292==ERROR: AddressSanitizer: heap-use-after-free on address 0x616000579698 at pc 0x0001035c7d14 bp 0x0003aa5be130 sp 0x0003aa5be128
READ of size 1 at 0x616000579698 thread T1082
==76292==WARNING: invalid path to external symbolizer!
==76292==WARNING: Failed to use and restart external symbolizer!
    #0 0x0001035c7d10 in base::(anonymous namespace)::CrashImmediatelyOnUseAfterFree(unsigned long)+0xf0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x387d10)
    #1 0x0001035c78f0 in base::(anonymous namespace)::SafelyUnwrapForDereference(unsigned long)+0x70 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x3878f0)
    #2 0x00014a757350 in blink::WebAudioSourceProviderImpl::TeeFilter::Render(base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, media::AudioBus*)+0x6c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libblink_platform.dylib:arm64+0x693350)
    #3 0x00017118a3d0 in blink::AudioRendererMixerInput::ProvideInput(media::AudioBus*, unsigned int, media::AudioGlitchInfo const&)+0x234 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libblink_modules.dylib:arm64+0x22563d0)
    #4 0x00010ff10158 in media::AudioConverter::SourceCallback(int, media::AudioBus*)+0x534 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmedia.dylib:arm64+0x138158)
    #5 0x00010ff0fad4 in media::AudioConverter::ProvideInput(int, media::AudioBus*)+0x1e0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmedia.dylib:arm64+0x137ad4)
    #6 0x00010ff11ea8 in base::internal::Invoker<base::internal::FunctorTraits<void (media::AudioConverter::* const&)(int, media::AudioBus*), media::AudioConverter*>, base::internal::BindState<true, true, false, void (media::AudioConverter::*)(int, media::AudioBus*), base::internal::UnretainedWrapper<media::AudioConverter, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (int, media::AudioBus*)>::Run(base::internal::BindStateBase*, int, media::AudioBus*)+0x194 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmedia.dylib:arm64+0x139ea8)
    #7 0x00010ff3acd8 in base::RepeatingCallback<void (int, media::AudioBus*)>::Run(int, media::AudioBus*) const &+0x154 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmedia.dylib:arm64+0x162cd8)
    #8 0x00010ffcf9b0 in media::MultiChannelResampler::ProvideInput(int, int, float*)+0x1d8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmedia.dylib:arm64+0x1f79b0)
    #9 0x00010ffd0c10 in base::internal::Invoker<base::internal::FunctorTraits<void (media::MultiChannelResampler::* const&)(int, int, float*), media::MultiChannelResampler*, int const&>, base::internal::BindState<true, true, false, void (media::MultiChannelResampler::*)(int, int, float*), base::internal::UnretainedWrapper<media::MultiChannelResampler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, int>, void (int, float*)>::Run(base::internal::BindStateBase*, int, float*)+0x1b8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmedia.dylib:arm64+0x1f8c10)
    #10 0x00011001abe0 in base::RepeatingCallback<void (int, float*)>::Run(int, float*) const &+0x154 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmedia.dylib:arm64+0x242be0)
    #11 0x00011001a64c in media::SincResampler::Resample(base::span<float, 18446744073709551615ul, float*>)+0x8e0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmedia.dylib:arm64+0x24264c)
    #12 0x00010ffcfeb8 in media::MultiChannelResampler::Resample(int, media::AudioBus*)+0x1d8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmedia.dylib:arm64+0x1f7eb8)
    #13 0x00010ff11998 in media::AudioConverter::ConvertWithInfo(unsigned int, media::AudioGlitchInfo const&, media::AudioBus*)+0x30c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmedia.dylib:arm64+0x139998)
    #14 0x00010ffad9c0 in media::LoopbackAudioConverter::ProvideInput(media::AudioBus*, unsigned int, media::AudioGlitchInfo const&)+0x1c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmedia.dylib:arm64+0x1d59c0)
    #15 0x00010ff10158 in media::AudioConverter::SourceCallback(int, media::AudioBus*)+0x534 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmedia.dylib:arm64+0x138158)
    #16 0x00010ff119e0 in media::AudioConverter::ConvertWithInfo(unsigned int, media::AudioGlitchInfo const&, media::AudioBus*)+0x354 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmedia.dylib:arm64+0x1399e0)
    #17 0x000171182c38 in blink::AudioRendererMixer::Render(base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, media::AudioBus*)+0x278 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libblink_modules.dylib:arm64+0x224ec38)
    #18 0x00010fe328e4 in media::AudioOutputDeviceThreadCallback::Process(unsigned int)+0x390 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmedia.dylib:arm64+0x5a8e4)
    #19 0x00010fdf59f0 in media::AudioDeviceThread::ThreadMain()+0x234 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmedia.dylib:arm64+0x1d9f0)
    #20 0x0001035c613c in base::(anonymous namespace)::ThreadFunc(void*)+0x154 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x38613c)
    #21 0x000101755878 in __sanitizer_weak_hook_memcmp+0x3674c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libclang_rt.asan_osx_dynamic.dylib:arm64+0x51878)
    #22 0x000199e57c04 in _pthread_start+0x84 (/usr/lib/system/libsystem_pthread.dylib:arm64e+0x6c04)
    #23 0x000199e52ba4 in thread_start+0x4 (/usr/lib/system/libsystem_pthread.dylib:arm64e+0x1ba4)

0x616000579698 is located 24 bytes inside of 584-byte region [0x616000579680,0x6160005798c8)
freed by thread T16 here:
    #0 0x0001017697a8 in __sanitizer_finish_switch_fiber+0xa04 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libclang_rt.asan_osx_dynamic.dylib:arm64+0x657a8)
    #1 0x000110443ac4 in media::RendererImpl::~RendererImpl()+0x15c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmedia.dylib:arm64+0x66bac4)
    #2 0x000110444888 in media::RendererImpl::~RendererImpl()+0x8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmedia.dylib:arm64+0x66c888)
    #3 0x00010ffddbe8 in media::PipelineImpl::RendererWrapper::CompleteSuspend(media::TypedStatus<media::PipelineStatusTraits>)+0x224 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmedia.dylib:arm64+0x205be8)
    #4 0x00010ffee61c in void base::internal::DecayedFunctorTraits<void (media::PipelineImpl::RendererWrapper::*)(media::TypedStatus<media::PipelineStatusTraits>), base::WeakPtr<media::PipelineImpl::RendererWrapper>&&>::Invoke<void (media::PipelineImpl::RendererWrapper::*)(media::TypedStatus<media::PipelineStatusTraits>), base::WeakPtr<media::PipelineImpl::RendererWrapper> const&, media::TypedStatus<media::PipelineStatusTraits>>(void (media::PipelineImpl::RendererWrapper::*)(media::TypedStatus<media::PipelineStatusTraits>), base::WeakPtr<media::PipelineImpl::RendererWrapper> const&, media::TypedStatus<media::PipelineStatusTraits>&&)+0x154 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmedia.dylib:arm64+0x21661c)
    #5 0x00010ffee420 in base::internal::Invoker<base::internal::FunctorTraits<void (media::PipelineImpl::RendererWrapper::*&&)(media::TypedStatus<media::PipelineStatusTraits>), base::WeakPtr<media::PipelineImpl::RendererWrapper>&&>, base::internal::BindState<true, true, false, void (media::PipelineImpl::RendererWrapper::*)(media::TypedStatus<media::PipelineStatusTraits>), base::WeakPtr<media::PipelineImpl::RendererWrapper>>, void (media::TypedStatus<media::PipelineStatusTraits>)>::RunOnce(base::internal::BindStateBase*, media::TypedStatus<media::PipelineStatusTraits>&&)+0x120 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmedia.dylib:arm64+0x216420)
    #6 0x00011000a0a0 in media::SerialRunner::RunNextInSeries(media::TypedStatus<media::PipelineStatusTraits>)+0x204 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmedia.dylib:arm64+0x2320a0)
    #7 0x00011000bb6c in void base::internal::DecayedFunctorTraits<void (media::SerialRunner::*)(media::TypedStatus<media::PipelineStatusTraits>), base::WeakPtr<media::SerialRunner>&&, media::PipelineStatusCodes&&>::Invoke<void (media::SerialRunner::*)(media::TypedStatus<media::PipelineStatusTraits>), base::WeakPtr<media::SerialRunner> const&, media::PipelineStatusCodes>(void (media::SerialRunner::*)(media::TypedStatus<media::PipelineStatusTraits>), base::WeakPtr<media::SerialRunner> const&, media::PipelineStatusCodes&&)+0x1e4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmedia.dylib:arm64+0x233b6c)
    #8 0x00011000b8e4 in base::internal::Invoker<base::internal::FunctorTraits<void (media::SerialRunner::*&&)(media::TypedStatus<media::PipelineStatusTraits>), base::WeakPtr<media::SerialRunner>&&, media::PipelineStatusCodes&&>, base::internal::BindState<true, true, false, void (media::SerialRunner::*)(media::TypedStatus<media::PipelineStatusTraits>), base::WeakPtr<media::SerialRunner>, media::PipelineStatusCodes>, void ()>::RunOnce(base::internal::BindStateBase*)+0x110 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmedia.dylib:arm64+0x2338e4)
    #9 0x00010343da34 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x1fda34)
    #10 0x0001034bb170 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x88c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x27b170)
    #11 0x0001034ba528 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x27a528)
    #12 0x0001032df7e4 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x244 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x9f7e4)
    #13 0x0001034bc52c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x32c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x27c52c)
    #14 0x0001033a8d40 in base::RunLoop::Run(base::Location const&)+0x430 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x168d40)
    #15 0x000103554328 in base::Thread::Run(base::RunLoop*)+0xd8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x314328)
    #16 0x000103554788 in base::Thread::ThreadMain()+0x3d8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x314788)
    #17 0x0001035c613c in base::(anonymous namespace)::ThreadFunc(void*)+0x154 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x38613c)
    #18 0x000101755878 in __sanitizer_weak_hook_memcmp+0x3674c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libclang_rt.asan_osx_dynamic.dylib:arm64+0x51878)
    #19 0x000199e57c04 in _pthread_start+0x84 (/usr/lib/system/libsystem_pthread.dylib:arm64e+0x6c04)
    #20 0x000199e52ba4 in thread_start+0x4 (/usr/lib/system/libsystem_pthread.dylib:arm64e+0x1ba4)

previously allocated by thread T0 here:
    #0 0x0001017693c0 in __sanitizer_finish_switch_fiber+0x61c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libclang_rt.asan_osx_dynamic.dylib:arm64+0x653c0)
    #1 0x000110456060 in media::RendererImplFactory::CreateRenderer(scoped_refptr<base::SequencedTaskRunner> const&, scoped_refptr<base::TaskRunner> const&, media::AudioRendererSink*, media::VideoRendererSink*, base::RepeatingCallback<void (base::RepeatingCallback<void (media::OverlayInfo const&)>)>, gfx::ColorSpace const&)+0x110 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmedia.dylib:arm64+0x67e060)
    #2 0x00015b76e724 in blink::WebMediaPlayerImpl::CreateRenderer(std::__Cr::optional<media::RendererType>)+0x464 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libblink_platform_media.dylib:arm64+0x96724)
    #3 0x00015b7974f4 in base::internal::Invoker<base::internal::FunctorTraits<std::__Cr::unique_ptr<media::Renderer, std::__Cr::default_delete<media::Renderer>> (blink::WebMediaPlayerImpl::* const&)(std::__Cr::optional<media::RendererType>), blink::WebMediaPlayerImpl*>, base::internal::BindState<true, true, false, std::__Cr::unique_ptr<media::Renderer, std::__Cr::default_delete<media::Renderer>> (blink::WebMediaPlayerImpl::*)(std::__Cr::optional<media::RendererType>), blink::UnretainedWrapper<blink::WebMediaPlayerImpl>>, std::__Cr::unique_ptr<media::Renderer, std::__Cr::default_delete<media::Renderer>> (std::__Cr::optional<media::RendererType>)>::Run(base::internal::BindStateBase*, std::__Cr::optional<media::RendererType>&&)+0x158 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libblink_platform_media.dylib:arm64+0xbf4f4)
    #4 0x00010ffe9d60 in base::RepeatingCallback<std::__Cr::unique_ptr<media::Renderer, std::__Cr::default_delete<media::Renderer>> (std::__Cr::optional<media::RendererType>)>::Run(std::__Cr::optional<media::RendererType>) const &+0x160 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmedia.dylib:arm64+0x211d60)
    #5 0x00010ffe9860 in media::PipelineImpl::Start(media::Pipeline::StartType, media::Demuxer*, media::Pipeline::Client*, base::OnceCallback<void (media::TypedStatus<media::PipelineStatusTraits>)>)+0x1c8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmedia.dylib:arm64+0x211860)
    #6 0x0001101d1ebc in media::PipelineController::Start(media::Pipeline::StartType, media::Demuxer*, media::Pipeline::Client*, bool, bool)+0x370 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmedia.dylib:arm64+0x3f9ebc)
    #7 0x00015b78f380 in blink::WebMediaPlayerImpl::OnDemuxerCreated(media::Demuxer*, media::Pipeline::StartType, bool, bool)+0x188 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libblink_platform_media.dylib:arm64+0xb7380)
    #8 0x00015b79f800 in base::internal::Invoker<base::internal::FunctorTraits<media::TypedStatus<media::PipelineStatusTraits> (blink::WebMediaPlayerImpl::*&&)(media::Demuxer*, media::Pipeline::StartType, bool, bool), blink::WebMediaPlayerImpl*>, base::internal::BindState<true, true, false, media::TypedStatus<media::PipelineStatusTraits> (blink::WebMediaPlayerImpl::*)(media::Demuxer*, media::Pipeline::StartType, bool, bool), blink::UnretainedWrapper<blink::WebMediaPlayerImpl>>, media::TypedStatus<media::PipelineStatusTraits> (media::Demuxer*, media::Pipeline::StartType, bool, bool)>::RunOnce(base::internal::BindStateBase*, media::Demuxer*, media::Pipeline::StartType, bool, bool)+0x140 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libblink_platform_media.dylib:arm64+0xc7800)
    #9 0x0001101b7cac in media::DemuxerManager::CreateDemuxer(bool, media::DataSource::Preload, bool, base::OnceCallback<media::TypedStatus<media::PipelineStatusTraits> (media::Demuxer*, media::Pipeline::StartType, bool, bool)>, base::flat_map<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::less<void>, std::__Cr::vector<std::__Cr::pair<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>, std::__Cr::allocator<std::__Cr::pair<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>>>>)+0x818 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmedia.dylib:arm64+0x3dfcac)
    #10 0x00015b778ed8 in blink::WebMediaPlayerImpl::StartPipeline()+0xa4c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libblink_platform_media.dylib:arm64+0xa0ed8)
    #11 0x00015b78ea64 in blink::WebMediaPlayerImpl::DataSourceInitialized(bool)+0xd8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libblink_platform_media.dylib:arm64+0xb6a64)
    #12 0x00015b779bb8 in blink::WebMediaPlayerImpl::MultiBufferDataSourceInitialized(bool)+0x1e8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libblink_platform_media.dylib:arm64+0xa1bb8)
    #13 0x00015b79bed4 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::WebMediaPlayerImpl::*&&)(bool), base::WeakPtr<blink::WebMediaPlayerImpl>&&>, base::internal::BindState<true, true, false, void (blink::WebMediaPlayerImpl::*)(bool), base::WeakPtr<blink::WebMediaPlayerImpl>>, void (bool)>::RunOnce(base::internal::BindStateBase*, bool)+0x168 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libblink_platform_media.dylib:arm64+0xc3ed4)
    #14 0x00015b722020 in base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (bool)>&&, bool&&>, base::internal::BindState<false, true, true, base::OnceCallback<void (bool)>, bool>, void ()>::RunOnce(base::internal::BindStateBase*)+0x16c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libblink_platform_media.dylib:arm64+0x4a020)
    #15 0x00010343da34 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x1fda34)
    #16 0x0001034bb170 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x88c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x27b170)
    #17 0x0001034ba528 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x27a528)
    #18 0x0001032df7e4 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x244 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x9f7e4)
    #19 0x0001034bc52c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x32c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x27c52c)
    #20 0x0001033a8d40 in base::RunLoop::Run(base::Location const&)+0x430 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x168d40)
    #21 0x00013564d7f8 in content::RendererMain(content::MainFunctionParams)+0x884 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libcontent.dylib:arm64+0x3b497f8)
    #22 0x00013588e92c in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x420 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libcontent.dylib:arm64+0x3d8a92c)
    #23 0x000135890aac in content::ContentMainRunnerImpl::Run()+0x53c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libcontent.dylib:arm64+0x3d8caac)
    #24 0x00013588c3bc in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x858 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libcontent.dylib:arm64+0x3d883bc)
    #25 0x00013588c8ac in content::ContentMain(content::ContentMainParams)+0x190 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libcontent.dylib:arm64+0x3d888ac)
    #26 0x00011957f724 in ChromeMain+0x490 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libchrome_dll.dylib:arm64+0xb724)
    #27 0x000100eccb94 in main+0x254 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7706.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer):arm64+0x100000b94)
    #28 0x000199a8dd50 in start+0x1c0c (/usr/lib/dyld:arm64e+0x8d50)

Thread T1082 created by T8 here:
    #0 0x00010174f968 in __sanitizer_weak_hook_memcmp+0x3083c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libclang_rt.asan_osx_dynamic.dylib:arm64+0x4b968)
    #1 0x0001035c5700 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType)+0x270 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x385700)
    #2 0x00010fdf4f64 in media::AudioDeviceThread::AudioDeviceThread(media::AudioDeviceThread::Callback*, base::ScopedGeneric<int, base::internal::ScopedFDCloseTraits>, char const*, base::ThreadType)+0x25c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmedia.dylib:arm64+0x1cf64)
    #3 0x00010fe2c9ac in media::AudioOutputDevice::OnStreamCreated(base::UnsafeSharedMemoryRegion, base::ScopedGeneric<int, base::internal::ScopedFDCloseTraits>, bool)+0x2e4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmedia.dylib:arm64+0x549ac)
    #4 0x0001711a2778 in blink::MojoAudioOutputIPC::Created(mojo::PendingRemote<media::mojom::blink::AudioOutputStream>, mojo::StructPtr<media::mojom::blink::ReadWriteAudioDataPipe>)+0x2dc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libblink_modules.dylib:arm64+0x226e778)
    #5 0x00014c4694a0 in media::mojom::blink::AudioOutputStreamProviderClientStubDispatch::Accept(media::mojom::blink::AudioOutputStreamProviderClient*, mojo::Message*)+0x258 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libblink_platform.dylib:arm64+0x23a54a0)
    #6 0x0001011b9cac in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*)+0x8fc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmojo_public_cpp_bindings.dylib:arm64+0x25cac)
    #7 0x0001011cff18 in mojo::MessageDispatcher::Accept(mojo::Message*)+0x2f0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmojo_public_cpp_bindings.dylib:arm64+0x3bf18)
    #8 0x0001011beea0 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*)+0x148 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmojo_public_cpp_bindings.dylib:arm64+0x2aea0)
    #9 0x0001011dd5c4 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*)+0x650 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmojo_public_cpp_bindings.dylib:arm64+0x495c4)
    #10 0x0001011dc058 in mojo::internal::MultiplexRouter::Accept(mojo::Message*)+0x558 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmojo_public_cpp_bindings.dylib:arm64+0x48058)
    #11 0x0001011cff18 in mojo::MessageDispatcher::Accept(mojo::Message*)+0x2f0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmojo_public_cpp_bindings.dylib:arm64+0x3bf18)
    #12 0x0001011a6ad0 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>)+0x394 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmojo_public_cpp_bindings.dylib:arm64+0x12ad0)
    #13 0x0001011a8208 in mojo::Connector::ReadAllAvailableMessages()+0x23c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmojo_public_cpp_bindings.dylib:arm64+0x14208)
    #14 0x0001011a7ce0 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int)+0xe8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmojo_public_cpp_bindings.dylib:arm64+0x13ce0)
    #15 0x0001011aa6a0 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int)+0x1b8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmojo_public_cpp_bindings.dylib:arm64+0x166a0)
    #16 0x0001011a9d54 in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const &+0x148 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmojo_public_cpp_bindings.dylib:arm64+0x15d54)
    #17 0x0001011a9b30 in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&)+0xf0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmojo_public_cpp_bindings.dylib:arm64+0x15b30)
    #18 0x00010111ae64 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const &+0x154 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmojo_public_system_cpp.dylib:arm64+0x1ae64)
    #19 0x00010111a880 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&)+0x398 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmojo_public_system_cpp.dylib:arm64+0x1a880)
    #20 0x00010111b1a4 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int)+0x1d8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmojo_public_system_cpp.dylib:arm64+0x1b1a4)
    #21 0x000101118380 in mojo::SimpleWatcher::Context::CallNotify(MojoTrapEvent const*)+0xb8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmojo_public_system_cpp.dylib:arm64+0x18380)
    #22 0x00010282f29c in mojo::core::ipcz_driver::MojoTrap::DispatchOrQueueEvent(mojo::core::ipcz_driver::MojoTrap::Trigger&, MojoTrapEvent const&)+0x334 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmojo_core_embedder_internal.dylib:arm64+0x3729c)
    #23 0x000102831338 in mojo::core::ipcz_driver::MojoTrap::HandleEvent(IpczTrapEvent const&)+0x680 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmojo_core_embedder_internal.dylib:arm64+0x39338)
    #24 0x0001028e2164 in ipcz::TrapEventDispatcher::~TrapEventDispatcher()+0x16c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmojo_core_embedder_internal.dylib:arm64+0xea164)
    #25 0x0001028caa68 in ipcz::Router::AcceptInboundParcel(std::__Cr::unique_ptr<ipcz::Parcel, std::__Cr::default_delete<ipcz::Parcel>>)+0x248 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmojo_core_embedder_internal.dylib:arm64+0xd2a68)
    #26 0x000102898848 in ipcz::NodeLink::AcceptCompleteParcel(ipcz::StrongAlias<ipcz::SublinkIdTag, unsigned long long>, std::__Cr::unique_ptr<ipcz::Parcel, std::__Cr::default_delete<ipcz::Parcel>>)+0x9a8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmojo_core_embedder_internal.dylib:arm64+0xa0848)
    #27 0x00010289cb54 in ipcz::NodeLink::OnAcceptParcel(ipcz::msg::AcceptParcel&)+0xc54 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmojo_core_embedder_internal.dylib:arm64+0xa4b54)
    #28 0x0001028bb304 in ipcz::msg::NodeMessageListener::OnTransportMessage(ipcz::DriverTransport::RawMessage const&, ipcz::DriverTransport const&, unsigned long)+0x1c80 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmojo_core_embedder_internal.dylib:arm64+0xc3304)
    #29 0x000102868684 in ipcz::(anonymous namespace)::NotifyTransport(unsigned long, void const*, unsigned long, unsigned long const*, unsigned long, unsigned int, IpczTransportActivityOptions const*)+0x340 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmojo_core_embedder_internal.dylib:arm64+0x70684)
    #30 0x00010284176c in mojo::core::ipcz_driver::Transport::OnChannelMessage(void const*, unsigned long, std::__Cr::vector<mojo::PlatformHandle, std::__Cr::allocator<mojo::PlatformHandle>>, scoped_refptr<mojo::core::ipcz_driver::Envelope>)+0x5b8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmojo_core_embedder_internal.dylib:arm64+0x4976c)
    #31 0x0001027ff518 in mojo::core::Channel::TryDispatchMessage(base::span<char const, 18446744073709551615ul, char const*>, std::__Cr::optional<std::__Cr::vector<mojo::PlatformHandle, std::__Cr::allocator<mojo::PlatformHandle>>>, scoped_refptr<mojo::core::ipcz_driver::Envelope>, unsigned long*)+0x9a4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmojo_core_embedder_internal.dylib:arm64+0x7518)
    #32 0x00010284ae8c in mojo::core::(anonymous namespace)::ChannelMac::OnMachMessageReceived(unsigned int)+0x16c0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libmojo_core_embedder_internal.dylib:arm64+0x52e8c)
    #33 0x000103691034 in base::MessagePumpKqueue::ProcessEvents(base::MessagePump::Delegate*, unsigned long)+0x630 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x451034)
    #34 0x00010368e5c4 in base::MessagePumpKqueue::DoInternalWork(base::MessagePump::Delegate*, base::MessagePump::Delegate::NextWorkInfo*)+0x258 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x44e5c4)
    #35 0x00010368e178 in base::MessagePumpKqueue::Run(base::MessagePump::Delegate*)+0x230 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x44e178)
    #36 0x0001034bc52c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x32c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x27c52c)
    #37 0x0001033a8d40 in base::RunLoop::Run(base::Location const&)+0x430 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x168d40)
    #38 0x000103554328 in base::Thread::Run(base::RunLoop*)+0xd8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x314328)
    #39 0x000131bbdb5c in content::(anonymous namespace)::ChildIOThread::Run(base::RunLoop*)+0x168 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libcontent.dylib:arm64+0xb9b5c)
    #40 0x000103554788 in base::Thread::ThreadMain()+0x3d8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x314788)
    #41 0x0001035c613c in base::(anonymous namespace)::ThreadFunc(void*)+0x154 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x38613c)
    #42 0x000101755878 in __sanitizer_weak_hook_memcmp+0x3674c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libclang_rt.asan_osx_dynamic.dylib:arm64+0x51878)
    #43 0x000199e57c04 in _pthread_start+0x84 (/usr/lib/system/libsystem_pthread.dylib:arm64e+0x6c04)
    #44 0x000199e52ba4 in thread_start+0x4 (/usr/lib/system/libsystem_pthread.dylib:arm64e+0x1ba4)

Thread T8 created by T0 here:
    #0 0x00010174f968 in __sanitizer_weak_hook_memcmp+0x3083c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libclang_rt.asan_osx_dynamic.dylib:arm64+0x4b968)
    #1 0x0001035c5700 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType)+0x270 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x385700)
    #2 0x000103553008 in base::Thread::StartWithOptions(base::Thread::Options)+0x498 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x313008)
    #3 0x000131bbc800 in content::ChildProcess::ChildProcess(base::ThreadType, std::__Cr::unique_ptr<base::ThreadPoolInstance::InitParams, std::__Cr::default_delete<base::ThreadPoolInstance::InitParams>>, bool)+0x404 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libcontent.dylib:arm64+0xb8800)
    #4 0x000135622094 in content::RenderProcess::RenderProcess(std::__Cr::unique_ptr<base::ThreadPoolInstance::InitParams, std::__Cr::default_delete<base::ThreadPoolInstance::InitParams>>)+0x24 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libcontent.dylib:arm64+0x3b1e094)
    #5 0x000135622144 in content::RenderProcessImpl::RenderProcessImpl()+0x4c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libcontent.dylib:arm64+0x3b1e144)
    #6 0x00013564d514 in content::RendererMain(content::MainFunctionParams)+0x5a0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libcontent.dylib:arm64+0x3b49514)
    #7 0x00013588e92c in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x420 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libcontent.dylib:arm64+0x3d8a92c)
    #8 0x000135890aac in content::ContentMainRunnerImpl::Run()+0x53c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libcontent.dylib:arm64+0x3d8caac)
    #9 0x00013588c3bc in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x858 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libcontent.dylib:arm64+0x3d883bc)
    #10 0x00013588c8ac in content::ContentMain(content::ContentMainParams)+0x190 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libcontent.dylib:arm64+0x3d888ac)
    #11 0x00011957f724 in ChromeMain+0x490 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libchrome_dll.dylib:arm64+0xb724)
    #12 0x000100eccb94 in main+0x254 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7706.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer):arm64+0x100000b94)
    #13 0x000199a8dd50 in start+0x1c0c (/usr/lib/dyld:arm64e+0x8d50)

Thread T16 created by T0 here:
    #0 0x00010174f968 in __sanitizer_weak_hook_memcmp+0x3083c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libclang_rt.asan_osx_dynamic.dylib:arm64+0x4b968)
    #1 0x0001035c5700 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType)+0x270 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x385700)
    #2 0x000103553008 in base::Thread::StartWithOptions(base::Thread::Options)+0x498 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x313008)
    #3 0x00013562f378 in content::RenderThreadImpl::GetMediaSequencedTaskRunner()+0x364 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libcontent.dylib:arm64+0x3b2b378)
    #4 0x000135563268 in content::MediaFactory::CreateMediaPlayer(blink::WebMediaPlayerSource const&, blink::WebMediaPlayerClient*, blink::MediaInspectorContext*, blink::WebMediaPlayerEncryptedMediaClient*, blink::WebContentDecryptionModule*, blink::WebString const&, viz::FrameSinkId, cc::LayerTreeSettings const&, scoped_refptr<base::SingleThreadTaskRunner>, scoped_refptr<base::TaskRunner>)+0xf6c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libcontent.dylib:arm64+0x3a5f268)
    #5 0x0001355c1360 in content::RenderFrameImpl::CreateMediaPlayer(blink::WebMediaPlayerSource const&, blink::WebMediaPlayerClient*, blink::MediaInspectorContext*, blink::WebMediaPlayerEncryptedMediaClient*, blink::WebContentDecryptionModule*, blink::WebString const&, cc::LayerTreeSettings const*, scoped_refptr<base::TaskRunner>)+0x2fc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libcontent.dylib:arm64+0x3abd360)
    #6 0x00016ef3e440 in blink::ModulesInitializer::CreateWebMediaPlayer(blink::WebLocalFrameClient*, blink::HTMLMediaElement&, blink::WebMediaPlayerSource const&, blink::WebMediaPlayerClient*) const+0x33c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libblink_modules.dylib:arm64+0xa440)
    #7 0x000150bd325c in blink::HTMLMediaElement::StartPlayerLoad()+0xaf0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libblink_core.dylib:arm64+0x1e5725c)
    #8 0x000150bd0098 in blink::HTMLMediaElement::LoadResource(blink::WebMediaPlayerSource const&, blink::String const&)+0x1550 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libblink_core.dylib:arm64+0x1e54098)
    #9 0x000150bccf60 in blink::HTMLMediaElement::LoadSourceFromAttribute()+0x470 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libblink_core.dylib:arm64+0x1e50f60)
    #10 0x000150bc78e8 in blink::HTMLMediaElement::LoadInternal()+0x4d4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libblink_core.dylib:arm64+0x1e4b8e8)
    #11 0x000150bbef88 in blink::HTMLMediaElement::LoadTimerFired(blink::TimerBase*)+0xa8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libblink_core.dylib:arm64+0x1e42f88)
    #12 0x00014a8e5668 in blink::TimerBase::RunInternal()+0xb0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libblink_platform.dylib:arm64+0x821668)
    #13 0x000150c027c4 in base::internal::Invoker<base::internal::FunctorTraits<void (*&&)(blink::HeapTaskRunnerTimer<blink::HTMLMediaElement>*, blink::HTMLMediaElement*), blink::HeapTaskRunnerTimer<blink::HTMLMediaElement>*, cppgc::internal::BasicPersistent<blink::HTMLMediaElement, cppgc::internal::WeakPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>&&>, base::internal::BindState<false, true, false, void (*)(blink::HeapTaskRunnerTimer<blink::HTMLMediaElement>*, blink::HTMLMediaElement*), blink::UnretainedWrapper<blink::HeapTaskRunnerTimer<blink::HTMLMediaElement>>, cppgc::internal::BasicPersistent<blink::HTMLMediaElement, cppgc::internal::WeakPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x104 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libblink_core.dylib:arm64+0x1e867c4)
    #14 0x00010343da34 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x1fda34)
    #15 0x0001034bb170 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x88c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x27b170)
    #16 0x0001034ba528 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x27a528)
    #17 0x0001032df7e4 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x244 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x9f7e4)
    #18 0x0001034bc52c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x32c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x27c52c)
    #19 0x0001033a8d40 in base::RunLoop::Run(base::Location const&)+0x430 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x168d40)
    #20 0x00013564d7f8 in content::RendererMain(content::MainFunctionParams)+0x884 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libcontent.dylib:arm64+0x3b497f8)
    #21 0x00013588e92c in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x420 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libcontent.dylib:arm64+0x3d8a92c)
    #22 0x000135890aac in content::ContentMainRunnerImpl::Run()+0x53c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libcontent.dylib:arm64+0x3d8caac)
    #23 0x00013588c3bc in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x858 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libcontent.dylib:arm64+0x3d883bc)
    #24 0x00013588c8ac in content::ContentMain(content::ContentMainParams)+0x190 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libcontent.dylib:arm64+0x3d888ac)
    #25 0x00011957f724 in ChromeMain+0x490 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libchrome_dll.dylib:arm64+0xb724)
    #26 0x000100eccb94 in main+0x254 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7706.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer):arm64+0x100000b94)
    #27 0x000199a8dd50 in start+0x1c0c (/usr/lib/dyld:arm64e+0x8d50)

SUMMARY: AddressSanitizer: heap-use-after-free (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/libbase.dylib:arm64+0x387d10) in base::(anonymous namespace)::CrashImmediatelyOnUseAfterFree(unsigned long)+0xf0
Shadow bytes around the buggy address:
  0x616000579400: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x616000579480: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x616000579500: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x616000579580: 00 00 00 00 00 fa fa fa fa fa fa fa fa fa fa fa
  0x616000579600: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
=>0x616000579680: fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd
  0x616000579700: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x616000579780: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x616000579800: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x616000579880: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa
  0x616000579900: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
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

==76292==ADDITIONAL INFO

==76292==Note: Please include this section with the ASan report.
Task trace:

Command line: `/Users/zh1x1an1221/xcode-chromium/src/out/asan-0226/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7706.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer) --type=renderer --user-data-dir=/tmp/userdata/t1 --no-sandbox --autoplay-policy=no-user-gesture-required --enable-unsafe-webgpu --js-flags=--expose-gc --lang=zh-CN --num-raster-threads=4 --enable-zero-copy --enable-gpu-memory-buffer-compositor-resources --enable-main-frame-before-activation --renderer-client-id=8 --time-ticks-at-unix-epoch=-1771763490829566 --launch-time-ticks=425807712059 --shared-files --metrics-shmem-handle=1752395122,r,18311278004034314543,10969004337976533599,2097152 --field-trial-handle=1718379636,r,7025290019596801173,14402638972469218545,262144 --enable-features=DelayStopForMediaElementSourceNode,WebMachineLearningNeuralNetwork --variations-seed-version --pseudonymization-salt-handle=1935764596,r,15831238535175078915,4820942144019577492,4 --trace-process-track-uuid=3190708993808206286 --enable-logging --v=1`

MiraclePtr Status: MANUAL ANALYSIS REQUIRED
This crash occurred while a raw_ptr<T> object containing a dangling pointer was being dereferenced.
The "use" and "free" threads don't match. This crash is likely to have been caused by a race condition that is mislabeled as a use-after-free. Make sure that the "free" is sequenced after the "use" (e.g. both are on the same sequence, or the "free" is in a task posted after the "use"). Otherwise, the crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==76292==END OF ADDITIONAL INFO

==76292==ABORTING

```
# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [420150619big-buck-bunny_trailer.webm](attachments/420150619big-buck-bunny_trailer.webm) (video/webm, 2.1 MB)
- [index.html](attachments/index.html) (text/html, 3.2 KB)
- [poc.mov](attachments/poc.mov) (video/quicktime, 55.6 MB)

## Timeline

### zh...@gmail.com (2026-02-27)

# RCA HERE

The vulnerability is a lifecycle contract violation in the sink adapter layer:

- `AudioRendererImpl::~AudioRendererImpl()` depends on `sink_->Stop()` to quiesce all future callbacks before destruction.
- In the vulnerable logic, `WebAudioSourceProviderImpl::Stop()` skipped forwarding `Stop()` when `client_` was attached.
- This allowed the audio callback path to continue and dereference a stale renderer callback target after teardown.

1. [`PipelineImpl::RendererWrapper::CompleteSuspend`](https://source.chromium.org/chromium/chromium/src/+/main:media/base/pipeline_impl.cc;l=1158-1185?q=PipelineImpl::RendererWrapper::CompleteSuspend) destroys renderer state and must make old renderer objects unreachable from audio callbacks.
2. [`RendererImpl::~RendererImpl`](https://source.chromium.org/chromium/chromium/src/+/main:media/renderers/renderer_impl.cc;l=118-136?q=RendererImpl::~RendererImpl) destroys `AudioRendererImpl` via `audio_renderer_.reset()`.
3. [`AudioRendererImpl::~AudioRendererImpl`](https://source.chromium.org/chromium/chromium/src/+/main:media/renderers/audio_renderer_impl.cc;l=104-118?q=AudioRendererImpl::~AudioRendererImpl) requires that after `sink_->Stop()`, sink must not call `Render()` again.
4. `WebAudioSourceProviderImpl` must preserve stop semantics regardless of WebAudio client attachment state.

- Playback Callback Chain

1. [`AudioRendererMixer::Render`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/media/audio/audio_renderer_mixer.cc;l=126-156?q=AudioRendererMixer::Render)
2. [`AudioConverter::ConvertWithInfo` / `AudioConverter::SourceCallback`](https://source.chromium.org/chromium/chromium/src/+/main:media/base/audio_converter.cc;l=176-267?q=AudioConverter::SourceCallback)
3. [`AudioRendererMixerInput::ProvideInput`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/media/audio/audio_renderer_mixer_input.cc;l=233-244?q=AudioRendererMixerInput::ProvideInput)
4. `callback_->Render(...)` (`callback_` is `TeeFilter`)
5. [`WebAudioSourceProviderImpl::TeeFilter::Render`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/media/web_audio_source_provider_impl.cc;l=56-65?q=TeeFilter::Render)
6. `renderer_->Render(...)` (`renderer_` points to `AudioRendererImpl` callback)
7. [`AudioRendererImpl::Render`](https://source.chromium.org/chromium/chromium/src/+/main:media/renderers/audio_renderer_impl.cc;l=1285-1302?q=AudioRendererImpl::Render)

- Suspend / Teardown Chain

1. [`PipelineImpl::RendererWrapper::CompleteSuspend`](https://source.chromium.org/chromium/chromium/src/+/main:media/base/pipeline_impl.cc;l=1158-1185?q=PipelineImpl::RendererWrapper::CompleteSuspend)
2. [`DestroyRenderer`](https://source.chromium.org/chromium/chromium/src/+/main:media/base/pipeline_impl.cc;l=1271-1281?q=DestroyRenderer)
3. [`RendererImpl::~RendererImpl`](https://source.chromium.org/chromium/chromium/src/+/main:media/renderers/renderer_impl.cc;l=118-136?q=RendererImpl::~RendererImpl)
4. `audio_renderer_.reset()`
5. [`AudioRendererImpl::~AudioRendererImpl`](https://source.chromium.org/chromium/chromium/src/+/main:media/renderers/audio_renderer_impl.cc;l=104-118?q=AudioRendererImpl::~AudioRendererImpl)
6. `sink_->Stop()`

- Contract Violation in Vulnerable Code

Vulnerable `Stop()` logic:

```
void WebAudioSourceProviderImpl::Stop() {
  base::AutoLock auto_lock(sink_lock_);
  state_ = kStopped;
  if (!client_ && sink_)
    sink_->Stop();
}

```

This makes callback quiescing dependent on `client_`, which violates destructor-time lifecycle requirements.

Additionally, in [`WebAudioSourceProviderImpl::SetClient`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/media/web_audio_source_provider_impl.cc;l=138-156?q=WebAudioSourceProviderImpl::SetClient), when `DelayStopForMediaElementSourceNode` is enabled, sink detachment is deferred. Combined with conditional `Stop()`, callback activity can overlap with renderer teardown.

- UAF Access Point

`TeeFilter` stores a non-owning callback pointer:

```
raw_ptr<AudioRendererSink::RenderCallback, DanglingUntriaged> renderer_ = nullptr;

```

If teardown frees `AudioRendererImpl` while callback quiescing is incomplete, the callback path can still execute:

`AudioRendererMixerInput::ProvideInput()` -> `TeeFilter::Render()` -> `renderer_->Render(...)`

At this point, `renderer_` may refer to freed memory.

## Remediation

`WebAudioSourceProviderImpl::Stop()` should always forwards `Stop()` whenever `sink_` exists, independent of `client_`.

```
diff --git a/third_party/blink/renderer/platform/media/web_audio_source_provider_impl.cc b/third_party/blink/renderer/platform/media/web_audio_source_provider_impl.cc
index ad266a2a91fd7..e2f4e9390624f 100644
--- a/third_party/blink/renderer/platform/media/web_audio_source_provider_impl.cc
+++ b/third_party/blink/renderer/platform/media/web_audio_source_provider_impl.cc
@@ -289,7 +289,10 @@ void WebAudioSourceProviderImpl::Start() {
 void WebAudioSourceProviderImpl::Stop() {
   base::AutoLock auto_lock(sink_lock_);
   state_ = kStopped;
-  if (!client_ && sink_)
+  // Stop() must always quiesce the underlying sink so that it cannot issue
+  // further callbacks into a renderer that is in teardown. This is required
+  // even while a WebAudio client is attached.
+  if (sink_)
     sink_->Stop();
 }
 

```

### zh...@gmail.com (2026-02-27)

## Bisect

The bisect of this buf should be: <https://chromium-review.googlesource.com/c/chromium/src/+/6594254>
This patch didn't fix the root cause of the vulnerability at all; it only changed the feature to DISABLED, and for almost a year afterward, the issue remained unresolved and was still a TODO. My fuzz was consistently blocked by this crash locally.

### li...@chromium.org (2026-02-27)

@Reporter - as clarification, this requires the flag disabled in [crbug.com/420150619](https://crbug.com/420150619) to be enabled, right?

@da...@chromium.org - do you mind taking a look or rerouting as necessary?

### zh...@gmail.com (2026-02-27)

Yes. If my analysis is correct, this is an incomplete fix, and the vulnerability's root cause code hasn't been truly addressed for a long time.

### da...@chromium.org (2026-03-02)

I was expecting @mj...@chromium.org to keep working on that feature and fix issues like this one. If it's not going to be fixed, I think it's time to delete this "feature". Can you take care of that @mj...@chromium.org ?

### mj...@chromium.org (2026-03-02)

I haven't had time to work on this, and I agree if nobody has missed it while it's been disabled then we can probably delete it and reopen the bug it was designed to fix (original author is no longer contributing to Chromium as far as I know).

Just to confirm: this isn't actively exploitable right now, correct?

### zh...@gmail.com (2026-03-02)

I don't think so at the moment.

### pe...@google.com (2026-03-02)

Thank you for providing more feedback. Adding the requester to the CC list.

### mj...@chromium.org (2026-03-02)

Thank you, then the plan is:

- Remove the feature, which was landed with <https://crrev.com/c/6444424>
- Reopen <https://crbug.com/41450896> when we do so

### dx...@google.com (2026-03-13)

Project: chromium/src  

Branch:  main  

Author:  Mahesh Bharadwaj Kannan [kmaheshb@google.com](mailto:kmaheshb@google.com)  

Link:    <https://chromium-review.googlesource.com/7659366>

[webaudio] Remove DelayStopForMediaElementSourceNode

---


Expand for full commit details
```
     
    The DelayStopForMediaElementSourceNode feature exposed a latent 
    lifecycle contract violation in WebAudioSourceProviderImpl. A legacy 
    check in Stop() skipped stopping the underlying sink if a WebAudio 
    client was attached, assuming SetClient() had already stopped it. When 
    the feature deferred this stop in SetClient(), the sink was never 
    reliably quiesced during teardown. This allowed audio callbacks to fire 
    after AudioRendererImpl was destroyed, leading to a heap-use-after-free. 
     
    This change completely removes the feature and its associated plumbing 
    (ConnectToDestinationReady) across HTMLMediaElement, AudioNode, and 
    WebAudioSourceProviderImpl. The sink is now unconditionally stopped 
    during teardown and client attachment, restoring the strict lifecycle 
    invariants required by the audio rendering pipeline. 
     
    Bug: 488188176 
    Change-Id: I081c81ba0f2f7723a1752990e9ad230e98199e99 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7659366 
    Reviewed-by: David Baron <dbaron@chromium.org> 
    Reviewed-by: Michael Wilson <mjwilson@chromium.org> 
    Reviewed-by: Eugene Zemtsov <eugene@chromium.org> 
    Commit-Queue: Mahesh Kannan <kmaheshb@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1599151}

```

---

Files:

- M `third_party/blink/public/platform/web_audio_source_provider_impl.h`
- M `third_party/blink/renderer/core/html/media/html_media_element.cc`
- M `third_party/blink/renderer/core/html/media/html_media_element.h`
- M `third_party/blink/renderer/modules/webaudio/audio_node.cc`
- M `third_party/blink/renderer/modules/webaudio/audio_node.h`
- M `third_party/blink/renderer/modules/webaudio/media_element_audio_source_node.cc`
- M `third_party/blink/renderer/modules/webaudio/media_element_audio_source_node.h`
- M `third_party/blink/renderer/platform/audio/audio_source_provider.h`
- M `third_party/blink/renderer/platform/media/web_audio_source_provider_impl.cc`
- M `third_party/blink/renderer/platform/media/web_audio_source_provider_impl_test.cc`

---

Hash: [7020a2cd5b02f820f500b93e6e21a29eb217aa85](https://chromiumdash.appspot.com/commit/7020a2cd5b02f820f500b93e6e21a29eb217aa85)  

Date: Fri Mar 13 17:22:45 2026


---

### km...@google.com (2026-03-13)

Reverted <https://crrev.com/c/6444424> and also addressed the lifecycle contract violation. Re-opening <https://crbug.com/41450896>

### sp...@google.com (2026-04-08)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
Baseline with bisect. Renderer RCE / memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### zh...@gmail.com (2026-04-09)

Hi—thanks for the reward. I was just curious: given that I provided a detailed RCA and bisect, why didn't this qualify as a "High-Quality Report"? Would it be possible to request that you reconsider this? Thank you very much.

### ch...@google.com (2026-06-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/488188176)*
