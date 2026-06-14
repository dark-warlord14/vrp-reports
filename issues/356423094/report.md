# Security: heap-use-after-free in webrtc::VSyncEncodeAdapterMode::EncodeAllEnqueuedFrames

| Field | Value |
|-------|-------|
| **Issue ID** | [356423094](https://issues.chromium.org/issues/356423094) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>WebRTC |
| **Platforms** | Mac |
| **Chrome Version** | 129.0.6627.0 |
| **Reporter** | zh...@gmail.com |
| **Assignee** | ha...@google.com |
| **Created** | 2024-07-31 |
| **Bounty** | $8,000.00 |

## Description

# Steps to reproduce the problem

## Asan chromium environment required to trigger the vulnerability (only tested on macos)

```
git checkout 29c6b26f72febe6ee85bcc285b8ef77390d132ec
git apply trigger.diff

```

- gn args

```
is_component_build = true
is_debug = false
is_asan = true
symbol_level = 2
dcheck_always_on = false
treat_warnings_as_errors = false

```
## So far I can trigger the vulnerability on both devices:

```
npm install puppeteer-core
node trigger.js 2>&1 | grep -E "AddressSanitizer" -A 100

```

Then just wait for the UAF to be triggered

# Problem Description

Security: heap-use-after-free in webrtc::VSyncEncodeAdapterMode::EncodeAllEnqueuedFrames

# Additional Comments

## Bisect commit

<https://source.chromium.org/chromium/_/webrtc/src/+/f089d7ea541106c8632db0aecee02d8c97e59ba7>

# Summary

Security: heap-use-after-free in webrtc::VSyncEncodeAdapterMode::EncodeAllEnqueuedFrames

# Custom Questions

#### Type of crash:

tab

#### Crash state:

```
=================================================================
[1m[31m==97826==ERROR: AddressSanitizer: heap-use-after-free on address 0x611000713300 at pc 0x000117ecdf6c bp 0x00037fec6510 sp 0x00037fec6508
[1m[0m[1m[34mREAD of size 8 at 0x611000713300 thread T15[1m[0m
==97826==WARNING: invalid path to external symbolizer!
==97826==WARNING: Failed to use and restart external symbolizer!
    #0 0x117ecdf68 in webrtc::(anonymous namespace)::VSyncEncodeAdapterMode::EncodeAllEnqueuedFrames()+0x8ec (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x7d1f68)
    #1 0x117ecd0f4 in webrtc::(anonymous namespace)::VSyncEncodeAdapterMode::OnFrame(webrtc::Timestamp, bool, webrtc::VideoFrame const&)+0x7a8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x7d10f4)
    #2 0x175afffec in webrtc::ThreadWrapper::RunTaskQueueTask(absl::AnyInvocable<void () &&>)+0x54 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0x2d8bfec)
    #3 0x175b02bc4 in void base::internal::DecayedFunctorTraits<void (webrtc::ThreadWrapper::*)(absl::AnyInvocable<void () &&>), base::WeakPtr<webrtc::ThreadWrapper>&&, absl::AnyInvocable<void () &&>&&>::Invoke<void (webrtc::ThreadWrapper::*)(absl::AnyInvocable<void () &&>), base::WeakPtr<webrtc::ThreadWrapper> const&, absl::AnyInvocable<void () &&>>(void (webrtc::ThreadWrapper::*)(absl::AnyInvocable<void () &&>), base::WeakPtr<webrtc::ThreadWrapper> const&, absl::AnyInvocable<void () &&>&&)+0x174 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0x2d8ebc4)
    #4 0x175b029ac in base::internal::Invoker<base::internal::FunctorTraits<void (webrtc::ThreadWrapper::*&&)(absl::AnyInvocable<void () &&>), base::WeakPtr<webrtc::ThreadWrapper>&&, absl::AnyInvocable<void () &&>&&>, base::internal::BindState<true, true, false, void (webrtc::ThreadWrapper::*)(absl::AnyInvocable<void () &&>), base::WeakPtr<webrtc::ThreadWrapper>, absl::AnyInvocable<void () &&>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x110 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0x2d8e9ac)
    #5 0x106fce708 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x34c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x1ae708)
    #6 0x10703ac64 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x7f0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x21ac64)
    #7 0x10703a0d8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x21a0d8)
    #8 0x106ea99f4 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x1b0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x899f4)
    #9 0x10703c210 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x3cc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x21c210)
    #10 0x106f56f4c in base::RunLoop::Run(base::Location const&)+0x434 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x136f4c)
    #11 0x1070ccaa4 in base::Thread::Run(base::RunLoop*)+0xd8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x2acaa4)
    #12 0x1070ccf0c in base::Thread::ThreadMain()+0x3e0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x2acf0c)
    #13 0x10712134c in base::(anonymous namespace)::ThreadFunc(void*)+0x12c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x30134c)
    #14 0x1053d9d18 in __sanitizer_weak_hook_memcmp+0x35118 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libclang_rt.asan_osx_dynamic.dylib:arm64+0x4dd18)
    #15 0x1049855bc in _pthread_start+0x84 (/usr/lib/system/introspection/libsystem_pthread.dylib:arm64+0x15bc)
    #16 0x711480010498fa9c  (<unknown module>)

[1m[32m0x611000713300 is located 0 bytes inside of 216-byte region [0x611000713300,0x6110007133d8)
[1m[0m[1m[35mfreed by thread T15 here:[1m[0m
    #0 0x1053ec500 in __sanitizer_finish_switch_fiber+0xa24 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libclang_rt.asan_osx_dynamic.dylib:arm64+0x60500)
    #1 0x117719dec in blink::WebRtcTaskQueue::Delete()+0x168 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x1ddec)
    #2 0x117eeeb14 in webrtc::VideoStreamEncoder::~VideoStreamEncoder()+0xb8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x7f2b14)
    #3 0x117eef39c in webrtc::VideoStreamEncoder::~VideoStreamEncoder()+0x8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x7f339c)
    #4 0x117eb93c8 in webrtc::internal::VideoSendStreamImpl::~VideoSendStreamImpl()+0x340 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x7bd3c8)
    #5 0x117eb95c4 in webrtc::internal::VideoSendStreamImpl::~VideoSendStreamImpl()+0x8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x7bd5c4)
    #6 0x117c7ccac in webrtc::internal::Call::DestroyVideoSendStream(webrtc::VideoSendStream*)+0x610 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x580cac)
    #7 0x1177d6edc in cricket::WebRtcVideoSendChannel::WebRtcVideoSendStream::~WebRtcVideoSendStream()+0x7c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xdaedc)
    #8 0x1177c1d58 in cricket::WebRtcVideoSendChannel::~WebRtcVideoSendChannel()+0x4ac (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xc5d58)
    #9 0x1177c2018 in non-virtual thunk to cricket::WebRtcVideoSendChannel::~WebRtcVideoSendChannel()+0xc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xc6018)
    #10 0x118664684 in cricket::BaseChannel::~BaseChannel()+0x614 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xf68684)
    #11 0x11867085c in cricket::VideoChannel::~VideoChannel()+0x1b4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xf7485c)
    #12 0x118670994 in cricket::VideoChannel::~VideoChannel()+0x8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xf74994)
    #13 0x175affb98 in webrtc::ThreadWrapper::ProcessPendingSends()+0x1ac (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0x2d8bb98)
    #14 0x175b026c8 in void base::internal::Invoker<base::internal::FunctorTraits<void (webrtc::ThreadWrapper::*&&)(), base::WeakPtr<webrtc::ThreadWrapper>&&>, base::internal::BindState<true, true, false, void (webrtc::ThreadWrapper::*)(), base::WeakPtr<webrtc::ThreadWrapper>>, void ()>::RunImpl<void (webrtc::ThreadWrapper::*)(), std::__Cr::tuple<base::WeakPtr<webrtc::ThreadWrapper>>, 0ul>(void (webrtc::ThreadWrapper::*&&)(), std::__Cr::tuple<base::WeakPtr<webrtc::ThreadWrapper>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>)+0x16c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0x2d8e6c8)
    #15 0x106fce708 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x34c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x1ae708)
    #16 0x10703ac64 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x7f0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x21ac64)
    #17 0x10703a0d8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x21a0d8)
    #18 0x106ea99f4 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x1b0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x899f4)
    #19 0x10703c210 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x3cc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x21c210)
    #20 0x106f56f4c in base::RunLoop::Run(base::Location const&)+0x434 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x136f4c)
    #21 0x1070ccaa4 in base::Thread::Run(base::RunLoop*)+0xd8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x2acaa4)
    #22 0x1070ccf0c in base::Thread::ThreadMain()+0x3e0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x2acf0c)
    #23 0x10712134c in base::(anonymous namespace)::ThreadFunc(void*)+0x12c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x30134c)
    #24 0x1053d9d18 in __sanitizer_weak_hook_memcmp+0x35118 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libclang_rt.asan_osx_dynamic.dylib:arm64+0x4dd18)
    #25 0x1049855bc in _pthread_start+0x84 (/usr/lib/system/introspection/libsystem_pthread.dylib:arm64+0x15bc)
    #26 0x711480010498fa9c  (<unknown module>)

[1m[35mpreviously allocated by thread T15 here:[1m[0m
    #0 0x1053ec0f8 in __sanitizer_finish_switch_fiber+0x61c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libclang_rt.asan_osx_dynamic.dylib:arm64+0x600f8)
    #1 0x11771bc38 in blink::(anonymous namespace)::WebrtcTaskQueueFactory::CreateTaskQueue(std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>, webrtc::TaskQueueFactory::Priority) const+0xb4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x1fc38)
    #2 0x117eb79bc in webrtc::internal::VideoSendStreamImpl::VideoSendStreamImpl(webrtc::Environment const&, int, webrtc::RtcpRttStats*, webrtc::RtpTransportControllerSendInterface*, webrtc::Metronome*, webrtc::BitrateAllocatorInterface*, webrtc::SendDelayStats*, webrtc::VideoSendStream::Config, webrtc::VideoEncoderConfig, std::__Cr::map<unsigned int, webrtc::RtpState, std::__Cr::less<unsigned int>, std::__Cr::allocator<std::__Cr::pair<unsigned int const, webrtc::RtpState>>> const&, std::__Cr::map<unsigned int, webrtc::RtpPayloadState, std::__Cr::less<unsigned int>, std::__Cr::allocator<std::__Cr::pair<unsigned int const, webrtc::RtpPayloadState>>> const&, std::__Cr::unique_ptr<webrtc::FecController, std::__Cr::default_delete<webrtc::FecController>>, std::__Cr::unique_ptr<webrtc::VideoStreamEncoderInterface, std::__Cr::default_delete<webrtc::VideoStreamEncoderInterface>>)+0x460 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x7bb9bc)
    #3 0x117c7bbec in webrtc::internal::Call::CreateVideoSendStream(webrtc::VideoSendStream::Config, webrtc::VideoEncoderConfig, std::__Cr::unique_ptr<webrtc::FecController, std::__Cr::default_delete<webrtc::FecController>>)+0x65c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x57fbec)
    #4 0x117c7c5cc in webrtc::internal::Call::CreateVideoSendStream(webrtc::VideoSendStream::Config, webrtc::VideoEncoderConfig)+0x214 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x5805cc)
    #5 0x1177d9f08 in cricket::WebRtcVideoSendChannel::WebRtcVideoSendStream::RecreateWebRtcStream()+0x3e0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xddf08)
    #6 0x1177d6bd8 in cricket::WebRtcVideoSendChannel::WebRtcVideoSendStream::SetCodec(cricket::VideoCodecSettings const&)+0x5ec (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xdabd8)
    #7 0x1177ca4c8 in cricket::WebRtcVideoSendChannel::WebRtcVideoSendStream::SetSenderParameters(cricket::WebRtcVideoSendChannel::ChangedSenderParameters const&)+0x438 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xce4c8)
    #8 0x1177c8998 in cricket::WebRtcVideoSendChannel::ApplyChangedParams(cricket::WebRtcVideoSendChannel::ChangedSenderParameters const&)+0x484 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xcc998)
    #9 0x1177c7d48 in cricket::WebRtcVideoSendChannel::SetSenderParameters(cricket::VideoSenderParameters const&)+0x5e4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xcbd48)
    #10 0x1186731bc in cricket::VideoChannel::SetRemoteContent_w(cricket::MediaContentDescription const*, webrtc::SdpType, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>&)+0xc18 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xf771bc)
    #11 0x118666494 in cricket::BaseChannel::SetRemoteContent(cricket::MediaContentDescription const*, webrtc::SdpType, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>&)+0x158 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xf6a494)
    #12 0x118867c90 in void rtc::FunctionView<void ()>::CallVoidPtr<bool rtc::Thread::BlockingCall<webrtc::SdpOfferAnswerHandler::PushdownMediaDescription(webrtc::SdpType, cricket::ContentSource, std::__Cr::map<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, cricket::ContentGroup const*, std::__Cr::less<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>, std::__Cr::allocator<std::__Cr::pair<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const, cricket::ContentGroup const*>>> const&)::$_2, bool, void>(webrtc::SdpOfferAnswerHandler::PushdownMediaDescription(webrtc::SdpType, cricket::ContentSource, std::__Cr::map<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, cricket::ContentGroup const*, std::__Cr::less<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>, std::__Cr::allocator<std::__Cr::pair<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const, cricket::ContentGroup const*>>> const&)::$_2&&, base::Location const&)::'lambda'()>(rtc::FunctionView<void ()>::VoidUnion)+0x114 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x116bc90)
    #13 0x175affb98 in webrtc::ThreadWrapper::ProcessPendingSends()+0x1ac (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0x2d8bb98)
    #14 0x175b026c8 in void base::internal::Invoker<base::internal::FunctorTraits<void (webrtc::ThreadWrapper::*&&)(), base::WeakPtr<webrtc::ThreadWrapper>&&>, base::internal::BindState<true, true, false, void (webrtc::ThreadWrapper::*)(), base::WeakPtr<webrtc::ThreadWrapper>>, void ()>::RunImpl<void (webrtc::ThreadWrapper::*)(), std::__Cr::tuple<base::WeakPtr<webrtc::ThreadWrapper>>, 0ul>(void (webrtc::ThreadWrapper::*&&)(), std::__Cr::tuple<base::WeakPtr<webrtc::ThreadWrapper>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>)+0x16c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0x2d8e6c8)
    #15 0x106fce708 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x34c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x1ae708)
    #16 0x10703ac64 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x7f0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x21ac64)
    #17 0x10703a0d8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x21a0d8)
    #18 0x106ea99f4 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x1b0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x899f4)
    #19 0x10703c210 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x3cc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x21c210)
    #20 0x106f56f4c in base::RunLoop::Run(base::Location const&)+0x434 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x136f4c)
    #21 0x1070ccaa4 in base::Thread::Run(base::RunLoop*)+0xd8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x2acaa4)
    #22 0x1070ccf0c in base::Thread::ThreadMain()+0x3e0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x2acf0c)
    #23 0x10712134c in base::(anonymous namespace)::ThreadFunc(void*)+0x12c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x30134c)
    #24 0x1053d9d18 in __sanitizer_weak_hook_memcmp+0x35118 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libclang_rt.asan_osx_dynamic.dylib:arm64+0x4dd18)
    #25 0x1049855bc in _pthread_start+0x84 (/usr/lib/system/introspection/libsystem_pthread.dylib:arm64+0x15bc)
    #26 0x711480010498fa9c  (<unknown module>)

Thread T15 created by T0 here:
Chromium Helper(98096,0x1fc964c00) malloc: nano zone abandoned due to inability to reserve vm space.
objc[98096]: Class DownloadDelegate is implemented in both /Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbrowser_ui_views.dylib (0x13b2cc4b8) and /Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libchrome_dll.dylib (0x12502c6f8). One of the two will be used. Which one is undefined.
    #0 0x1053d4a98 in __sanitizer_weak_hook_memcmp+0x2fe98 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libclang_rt.asan_osx_dynamic.dylib:arm64+0x48a98)
    #1 0x107120a14 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType)+0x270 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x300a14)
    #2 0x1070cb8d8 in base::Thread::StartWithOptions(base::Thread::Options)+0x3f4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x2ab8d8)
    #3 0x174f5e26c in blink::PeerConnectionDependencyFactory::CreatePeerConnectionFactory()+0x450 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0x21ea26c)
    #4 0x174f5dd2c in blink::PeerConnectionDependencyFactory::GetPcFactory()+0xd4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0x21e9d2c)
    #5 0x174f658f8 in blink::PeerConnectionDependencyFactory::CreatePeerConnection(webrtc::PeerConnectionInterface::RTCConfiguration const&, blink::WebLocalFrame*, webrtc::PeerConnectionObserver*, blink::ExceptionState&)+0x138 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0x21f18f8)
    #6 0x175026788 in blink::RTCPeerConnectionHandler::Initialize(blink::ExecutionContext*, webrtc::PeerConnectionInterface::RTCConfiguration const&, blink::WebLocalFrame*, blink::ExceptionState&)+0x51c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0x22b2788)
    #7 0x174fea114 in blink::RTCPeerConnection::RTCPeerConnection(blink::ExecutionContext*, webrtc::PeerConnectionInterface::RTCConfiguration, bool, blink::ExceptionState&)+0x8f4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0x2276114)
    #8 0x174fe96bc in blink::RTCPeerConnection* blink::MakeGarbageCollected<blink::RTCPeerConnection, blink::ExecutionContext*&, webrtc::PeerConnectionInterface::RTCConfiguration, bool, blink::ExceptionState&>(blink::ExecutionContext*&, webrtc::PeerConnectionInterface::RTCConfiguration&&, bool&&, blink::ExceptionState&)+0x160 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0x22756bc)
    #9 0x174fe639c in blink::RTCPeerConnection::Create(blink::ExecutionContext*, blink::RTCConfiguration const*, blink::ExceptionState&)+0x580 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0x227239c)
    #10 0x173b26aa0 in blink::(anonymous namespace)::v8_rtc_peer_connection::ConstructorCallback(v8::FunctionCallbackInfo<v8::Value> const&)+0x6bc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0xdb2aa0)
    #11 0x14bd2b488 in v8::internal::FunctionCallbackArguments::CallOrConstruct(v8::internal::Tagged<v8::internal::FunctionTemplateInfo>, bool)+0x4e4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libv8.dylib:arm64+0x32b488)
    #12 0x14bd299e4 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<true>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, unsigned long*, int)+0x408 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libv8.dylib:arm64+0x3299e4)
    #13 0x14bd28248 in v8::internal::Builtin_Impl_HandleApiConstruct(v8::internal::BuiltinArguments, v8::internal::Isolate*)+0x184 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libv8.dylib:arm64+0x328248)
    #14 0x7ff847ea8190  (<unknown module>)
    #15 0x7ff847e0e268  (<unknown module>)
    #16 0x7ff847f90494  (<unknown module>)
    #17 0x7ff847e0d3fc  (<unknown module>)
    #18 0x7ff847e0d3fc  (<unknown module>)
    #19 0x7ff847e0d3fc  (<unknown module>)
    #20 0x7ff847f1b678  (<unknown module>)
    #21 0x7ff847e0e268  (<unknown module>)
    #22 0x7ff847f90494  (<unknown module>)
    #23 0x7ff847e0d3fc  (<unknown module>)
    #24 0x7ff847f1db94  (<unknown module>)
    #25 0x7ff847e3b5dc  (<unknown module>)
    #26 0x7ff847e0aef0  (<unknown module>)
    #27 0x14c02b6d0 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&)+0x1744 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libv8.dylib:arm64+0x62b6d0)
    #28 0x14c02d8dc in v8::internal::(anonymous namespace)::InvokeWithTryCatch(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&)+0x118 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libv8.dylib:arm64+0x62d8dc)
    #29 0x14c02dc68 in v8::internal::Execution::TryRunMicrotasks(v8::internal::Isolate*, v8::internal::MicrotaskQueue*)+0x38 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libv8.dylib:arm64+0x62dc68)
    #30 0x14c0bb17c in v8::internal::MicrotaskQueue::RunMicrotasks(v8::internal::Isolate*)+0x3b4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libv8.dylib:arm64+0x6bb17c)
    #31 0x14c0bad20 in v8::internal::MicrotaskQueue::PerformCheckpointInternal(v8::Isolate*)+0x118 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libv8.dylib:arm64+0x6bad20)
    #32 0x14bc89ea0 in v8::MicrotasksScope::~MicrotasksScope()+0x13c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libv8.dylib:arm64+0x289ea0)
    #33 0x15c2d4f8c in blink::V8ScriptRunner::RunCompiledScript(v8::Isolate*, v8::Local<v8::Script>, v8::Local<v8::Data>, blink::ExecutionContext*)+0x600 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_core.dylib:arm64+0x174f8c)
    #34 0x15c2d6178 in blink::V8ScriptRunner::CompileAndRunScript(blink::ScriptState*, blink::ClassicScript*, blink::ExecuteScriptPolicy, blink::V8ScriptRunner::RethrowErrorsOption)+0x8b0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_core.dylib:arm64+0x176178)
    #35 0x15ed0cd08 in blink::ClassicScript::RunScriptOnScriptStateAndReturnValue(blink::ScriptState*, blink::ExecuteScriptPolicy, blink::V8ScriptRunner::RethrowErrorsOption)+0x19c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_core.dylib:arm64+0x2bacd08)
    #36 0x15ed5b7b0 in blink::Script::RunScriptOnScriptState(blink::ScriptState*, blink::ExecuteScriptPolicy, blink::V8ScriptRunner::RethrowErrorsOption)+0x1b4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_core.dylib:arm64+0x2bfb7b0)
    #37 0x15ed5bac0 in blink::Script::RunScript(blink::LocalDOMWindow*, blink::ExecuteScriptPolicy, blink::V8ScriptRunner::RethrowErrorsOption)+0x140 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_core.dylib:arm64+0x2bfbac0)
    #38 0x15ed5ad10 in blink::PendingScript::ExecuteScriptBlockInternal(blink::Script*, blink::ScriptElementBase*, bool, bool, bool, base::TimeTicks, bool)+0x3ec (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_core.dylib:arm64+0x2bfad10)
    #39 0x15ed59c6c in blink::PendingScript::ExecuteScriptBlock()+0x560 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_core.dylib:arm64+0x2bf9c6c)
    #40 0x15ed1c2a0 in blink::HTMLParserScriptRunner::ExecutePendingParserBlockingScriptAndDispatchEvent()+0x310 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_core.dylib:arm64+0x2bbc2a0)
    #41 0x15ed1e8b8 in blink::HTMLParserScriptRunner::ExecuteParsingBlockingScripts()+0x39c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_core.dylib:arm64+0x2bbe8b8)
    #42 0x15ed1ee60 in blink::HTMLParserScriptRunner::ExecuteScriptsWaitingForResources()+0x120 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_core.dylib:arm64+0x2bbee60)
    #43 0x15f65e3ac in blink::HTMLDocumentParser::ExecuteScriptsWaitingForResources()+0x254 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_core.dylib:arm64+0x34fe3ac)
    #44 0x15ed6e664 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::ScriptRunner::*&&)(), cppgc::internal::BasicPersistent<blink::ScriptRunner, cppgc::internal::WeakPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>&&>, base::internal::BindState<true, true, false, void (blink::ScriptRunner::*)(), cppgc::internal::BasicPersistent<blink::ScriptRunner, cppgc::internal::WeakPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x120 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_core.dylib:arm64+0x2c0e664)
    #45 0x106fce708 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x34c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x1ae708)
    #46 0x10703ac64 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x7f0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x21ac64)
    #47 0x10703a0d8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x21a0d8)
    #48 0x106ea99f4 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x1b0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x899f4)
    #49 0x10703c210 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x3cc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x21c210)
    #50 0x106f56f4c in base::RunLoop::Run(base::Location const&)+0x434 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x136f4c)
    #51 0x135530ae0 in content::RendererMain(content::MainFunctionParams)+0x6e8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libcontent.dylib:arm64+0x30c4ae0)
    #52 0x13570ae20 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x3f8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libcontent.dylib:arm64+0x329ee20)
    #53 0x13570cb74 in content::ContentMainRunnerImpl::Run()+0x434 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libcontent.dylib:arm64+0x32a0b74)
    #54 0x135708c38 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x5b4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libcontent.dylib:arm64+0x329cc38)
    #55 0x1357094f8 in content::ContentMain(content::ContentMainParams)+0x190 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libcontent.dylib:arm64+0x329d4f8)
    #56 0x11b846e58 in ChromeMain+0x370 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libchrome_dll.dylib:arm64+0xae58)
    #57 0x10431cce4 in main+0x254 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/129.0.6627.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer):arm64+0x100000ce4)
    #58 0x1947a20dc  (<unknown module>)
    #59 0x9377fffffffffffc  (<unknown module>)

SUMMARY: AddressSanitizer: heap-use-after-free (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x7d1f68) in webrtc::(anonymous namespace)::VSyncEncodeAdapterMode::EncodeAllEnqueuedFrames()+0x8ec
Shadow bytes around the buggy address:
  0x611000713080: [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m
  0x611000713100: [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m
  0x611000713180: [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[34mf7[1m[0m [1m[31mfa[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m
  0x611000713200: [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m
  0x611000713280: [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[34mf7[1m[0m [1m[31mfa[1m[0m
=>0x611000713300:[[1m[35mfd[1m[0m][1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m
  0x611000713380: [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m
  0x611000713400: [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[34mf7[1m[0m [1m[31mfa[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m
  0x611000713480: [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m
  0x611000713500: [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[34mf7[1m[0m [1m[31mfa[1m[0m
  0x611000713580: [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           [1m[0m00[1m[0m
  Partially addressable: [1m[0m01[1m[0m [1m[0m02[1m[0m [1m[0m03[1m[0m [1m[0m04[1m[0m [1m[0m05[1m[0m [1m[0m06[1m[0m [1m[0m07[1m[0m 
  Heap left redzone:       [1m[31mfa[1m[0m
  Freed heap region:       [1m[35mfd[1m[0m
  Stack left redzone:      [1m[31mf1[1m[0m
  Stack mid redzone:       [1m[31mf2[1m[0m
  Stack right redzone:     [1m[31mf3[1m[0m
  Stack after return:      [1m[35mf5[1m[0m
  Stack use after scope:   [1m[35mf8[1m[0m
  Global redzone:          [1m[31mf9[1m[0m
  Global init order:       [1m[36mf6[1m[0m
  Poisoned by user:        [1m[34mf7[1m[0m
  Container overflow:      [1m[34mfc[1m[0m
  Array cookie:            [1m[31mac[1m[0m
  Intra object redzone:    [1m[33mbb[1m[0m
  ASan internal:           [1m[33mfe[1m[0m
  Left alloca redzone:     [1m[34mca[1m[0m
  Right alloca redzone:    [1m[34mcb[1m[0m

==97826==ADDITIONAL INFO

==97826==Note: Please include this section with the ASan report.
Task trace:
    #0 0x117eccba4 in webrtc::(anonymous namespace)::VSyncEncodeAdapterMode::OnFrame(webrtc::Timestamp, bool, webrtc::VideoFrame const&)+0x258 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x7d0ba4)
    #1 0x117ec0d18 in webrtc::(anonymous namespace)::FrameCadenceAdapterImpl::OnFrame(webrtc::VideoFrame const&)+0x2c4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x7c4d18)
    #2 0x174f54284 in blink::MediaStreamVideoWebRtcSink::WebRtcVideoSourceAdapter::OnVideoFrameOnIO(scoped_refptr<media::VideoFrame>, base::TimeTicks)+0x130 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0x21e0284)
    #3 0x174c9942c in blink::MediaStreamVideoSource::AddTrack(blink::MediaStreamVideoTrack*, blink::VideoTrackAdapterSettings const&, base::RepeatingCallback<void (scoped_refptr<media::VideoFrame>, base::TimeTicks)> const&, base::RepeatingCallback<void (media::VideoCaptureFrameDropReason)> const&, base::RepeatingCallback<void (scoped_refptr<blink::EncodedVideoFrame>, base::TimeTicks)> const&, base::RepeatingCallback<void (unsigned int)> const&, base::RepeatingCallback<void (gfx::Size, double)> const&, base::RepeatingCallback<void (media::VideoCaptureFormat const&)> const&, base::OnceCallback<void (blink::WebPlatformMediaStreamSource*, blink::mojom::MediaStreamRequestResult, blink::WebString const&)>)+0xb30 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0x1f2542c)

Command line: `/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/129.0.6627.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer) --type=renderer --user-data-dir=/tmp/userdata/t1 --enable-isolated-web-apps-in-renderer --no-subproc-heap-profiling --no-sandbox --enable-experimental-web-platform-features --enable-blink-test-features --use-fake-ui-for-media-stream --js-flags=--expose-gc --enable-blink-features=CSSTextAutoSpace --lang=zh-CN --touch-selection-strategy=direction --num-raster-threads=4 --enable-zero-copy --enable-gpu-memory-buffer-compositor-resources --enable-main-frame-before-activation --renderer-client-id=34 --time-ticks-at-unix-epoch=-1722243859565583 --launch-time-ticks=94788496559 --shared-files --metrics-shmem-handle=1752395122,r,18374326972935874337,5759133869106502841,2097152 --field-trial-handle=1718379636,r,1530538758962008953,13102353070936157238,262144 --enable-features=BlockInsecurePrivateNetworkRequests,BlockInsecurePrivateNetworkRequestsFromPrivate,BlockInsecurePrivateNetworkRequestsFromUnknown,CSSDisplayModePictureInPicture,ClientHintsFormFactors,CookieSameSiteConsidersRedirectChain,CreateImageBitmapOrientationNone,CriticalClientHint,DocumentPictureInPictureAPI,DocumentPolicyIncludeJSCallStacksInCrashReports,DocumentPolicyNegotiation,DocumentReporting,EnableCanvas2DLayers,ExperimentalContentSecurityPolicyFeatures,OriginIsolationHeader,PrivateNetworkAccessRespectPreflightResults,SchemefulSameSite,ThirdPartyStoragePartitioning,WebMachineLearningNeuralNetwork --disable-features=PrivateNetworkAccessPreflightShortTimeout --variations-seed-version`

MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==97826==END OF ADDITIONAL INFO
==97826==ABORTING
Received signal 6
 [0x000107166840]
 [0x00010712319c]
 [0x000107166348]
 [0x000194b5b584]
 [0x000104986be8]
 [0x000194a37a30]
 [0x000105402a0c]
 [0x00010540204c]
 [0x0001053e5388]
 [0x0001053e4648]
 [0x0001053e5b5c]
 [0x000117ecdf6c]
 [0x000117ecd0f8]
 [0x000175affff0]
 [0x000175b02bc8]
 [0x000175b029b0]
 [0x000106fce70c]
 [0x00010703ac68]
 [0x00010703a0dc]
 [0x000106ea99f8]
 [0x00010703c214]
 [0x000106f56f50]
 [0x0001070ccaa8]
 [0x0001070ccf10]
 [0x000107121350]
 [0x0001053d9d1c]
 [0x0001049855c0]
 [0x00010498faa0]
[end of stack trace]
[0730/192432.228823:WARNING:process_memory_mac.cc(94)] mach_vm_read(0x10476c000, 0x8000): (os/kern) invalid address (1)
[0730/192432.230418:WARNING:process_memory_mac.cc(94)] mach_vm_read(0x10476c000, 0x8000): (os/kern) invalid address (1)
[0730/192432.230732:WARNING:process_memory_mac.cc(94)] mach_vm_read(0x10476c000, 0x8000): (os/kern) invalid address (1)
[0730/192432.343772:WARNING:process_memory_mac.cc(94)] mach_vm_read(0x10476c000, 0x8000): (os/kern) invalid address (1)
[0730/192432.369146:WARNING:process_memory_mac.cc(94)] mach_vm_read(0x114d88000, 0x8000): (os/kern) invalid address (1)
[0730/192432.369585:WARNING:process_memory_mac.cc(94)] mach_vm_read(0x114d88000, 0x8000): (os/kern) invalid address (1)
[0730/192432.369857:WARNING:process_memory_mac.cc(94)] mach_vm_read(0x114d88000, 0x8000): (os/kern) invalid address (1)
[0730/192432.370182:WARNING:process_memory_mac.cc(94)] mach_vm_read(0x114d88000, 0x8000): (os/kern) invalid address (1)
[0730/192432.370446:WARNING:process_memory_mac.cc(94)] mach_vm_read(0x114d88000, 0x8000): (os/kern) invalid address (1)
[0730/192432.370694:WARNING:process_memory_mac.cc(94)] mach_vm_read(0x114d88000, 0x8000): (os/kern) invalid address (1)
[0730/192432.370980:WARNING:process_memory_mac.cc(94)] mach_vm_read(0x114d88000, 0x8000): (os/kern) invalid address (1)
[0730/192432.500241:WARNING:process_memory_mac.cc(94)] mach_vm_read(0x1417c0000, 0x8000): (os/kern) invalid address (1)
[0730/192432.500963:WARNING:process_memory_mac.cc(94)] mach_vm_read(0x1417c0000, 0x8000): (os/kern) invalid address (1)
[0730/192432.501542:WARNING:process_memory_mac.cc(94)] mach_vm_read(0x1417c0000, 0x8000): (os/kern) invalid address (1)
[0730/192432.502373:WARNING:process_memory_mac.cc(94)] mach_vm_read(0x1417c0000, 0x8000): (os/kern) invalid address (1)
[0730/192432.502893:WARNING:process_memory_mac.cc(94)] mach_vm_read(0x1417c0000, 0x8000): (os/kern) invalid address (1)
Chromium Helper(98180,0x1fc964c00) malloc: nano zone abandoned due to inability to reserve vm space.
objc[98180]: Class DownloadDelegate is implemented in both /Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbrowser_ui_views.dylib (0x13bab44b8) and /Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libchrome_dll.dylib (0x1258146f8). One of the two will be used. Which one is undefined.
Chromium Helper(98264,0x1fc964c00) malloc: nano zone abandoned due to inability to reserve vm space.
objc[98264]: Class DownloadDelegate is implemented in both /Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbrowser_ui_views.dylib (0x13bc104b8) and /Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libchrome_dll.dylib (0x1259706f8). One of the two will be used. Which one is undefined.
cannot add handler to 4 from 4 - dropping
Chromium Helper(98287,0x1fc964c00) malloc: nano zone abandoned due to inability to reserve vm space.
objc[98287]: Class DownloadDelegate is implemented in both /Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbrowser_ui_views.dylib (0x13b3f44b8) and /Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libchrome_dll.dylib (0x1251546f8). One of the two will be used. Which one is undefined.
Chromium Helper(98371,0x1fc964c00) malloc: nano zone abandoned due to inability to reserve vm space.
objc[98371]: Class DownloadDelegate is implemented in both /Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbrowser_ui_views.dylib (0x13d4a84b8) and /Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libchrome_dll.dylib (0x1272086f8). One of the two will be used. Which one is undefined.
Chromium Helper(98466,0x1fc964c00) malloc: nano zone abandoned due to inability to reserve vm space.
objc[98466]: Class DownloadDelegate is implemented in both /Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbrowser_ui_views.dylib (0x13da444b8) and /Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libchrome_dll.dylib (0x1277a46f8). One of the two will be used. Which one is undefined.
Invalid image size X: 128 Y: 128
Invalid image size X: 128 Y: 128
Chromium Helper(98553,0x1fc964c00) malloc: nano zone abandoned due to inability to reserve vm space.
objc[98553]: Class DownloadDelegate is implemented in both /Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbrowser_ui_views.dylib (0x13b48c4b8) and /Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libchrome_dll.dylib (0x1251ec6f8). One of the two will be used. Which one is undefined.
Chromium Helper(98643,0x1fc964c00) malloc: nano zone abandoned due to inability to reserve vm space.
objc[98643]: Class DownloadDelegate is implemented in both /Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbrowser_ui_views.dylib (0x13c1884b8) and /Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libchrome_dll.dylib (0x125ee86f8). One of the two will be used. Which one is undefined.
Chromium Helper(98782,0x1fc964c00) malloc: nano zone abandoned due to inability to reserve vm space.
objc[98782]: Class DownloadDelegate is implemented in both /Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbrowser_ui_views.dylib (0x13b3104b8) and /Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libchrome_dll.dylib (0x1250706f8). One of the two will be used. Which one is undefined.
Chromium Helper(99023,0x1fc964c00) malloc: nano zone abandoned due to inability to reserve vm space.
objc[99023]: Class DownloadDelegate is implemented in both /Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbrowser_ui_views.dylib (0x13ba184b8) and /Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libchrome_dll.dylib (0x1257786f8). One of the two will be used. Which one is undefined.
Chromium Helper(99272,0x1fc964c00) malloc: nano zone abandoned due to inability to reserve vm space.
objc[99272]: Class DownloadDelegate is implemented in both /Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbrowser_ui_views.dylib (0x13ff244b8) and /Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libchrome_dll.dylib (0x129c846f8). One of the two will be used. Which one is undefined.
Chromium Helper(99567,0x1fc964c00) malloc: nano zone abandoned due to inability to reserve vm space.
objc[99567]: Class DownloadDelegate is implemented in both /Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbrowser_ui_views.dylib (0x13d1f04b8) and /Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libchrome_dll.dylib (0x126f506f8). One of the two will be used. Which one is undefined.

```
# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 43.8 KB)
- [trigger.diff](attachments/trigger.diff) (text/x-diff, 333.0 KB)
- [trigger.js](attachments/trigger.js) (text/javascript, 2.6 KB)
- [asan.png](attachments/asan.png) (image/png, 1.7 MB)
- [wrapper.html](attachments/wrapper.html) (text/html, 561 B)
- [poc.mov](attachments/poc.mov) (video/quicktime, 480.5 MB)
- [webrtc_poc.zip](attachments/webrtc_poc.zip) (application/zip, 62.8 KB)
- [asan_results.txt](attachments/asan_results.txt) (text/plain, 586.5 KB)
- [poc_final.mov](attachments/poc_final.mov) (video/quicktime, 358.1 MB)
- [command_line_result.txt](attachments/command_line_result.txt) (text/plain, 740.1 KB)
- [debug_fix_result.txt](attachments/debug_fix_result.txt) (text/plain, 944.7 KB)
- [debug_fix.diff](attachments/debug_fix.diff) (text/x-diff, 3.8 KB)
- debug_fix_result.txt (text/plain, 937.6 KB)
- debug_fix.diff (text/x-diff, 4.1 KB)

## Timeline

### dc...@chromium.org (2024-08-01)

In the future, if you can try to provide a reproduction without requiring a custom patch, that would greatly simplify things. It looks like the patch just enables a bunch of features that are otherwise disabled by default; that can be done from the command line (see <https://source.chromium.org/chromium/chromium/src/+/main:base/feature_list.h;l=193;drc=291e9041b6d5e23015c55a32fe8d179f496a5f73>)

### zh...@gmail.com (2024-08-01)

I'm sorry for the inconvenience caused to you in reproducing the vulnerability. In order to accurately and stably reproduce this vulnerability, the custom patch I provided is the exact environment where the fuzz vulnerability was successfully triggered. I will provide a more streamlined reproduction step as soon as possible.

### zh...@gmail.com (2024-08-02)

In order to improve the quality of this vulnerability report, I have partially optimized the POC for reproducing the vulnerability on macos (arm). This is just a phased progress before this weekend, not the final version, because I am still trying to optimize the feature that triggers the vulnerability. You can refer to this step to reproduce it more easily and stably instead of using puppeteer.

This part remains the same:

```
git checkout 29c6b26f72febe6ee85bcc285b8ef77390d132ec
git apply trigger.diff

```

This means that we still need to use some features enabled in trigger.diff. I will confirm which features to enable later.

- gn args

```
is_component_build = true
is_debug = false
is_asan = true
symbol_level = 2
dcheck_always_on = false
treat_warnings_as_errors = false

```

To trigger the vulnerability, please use the newly uploaded webrtc\_poc.zip:

```
unzip webrtc_poc.zip
cd webrtc_poc
http-server -c-1 -p 80

```

In the `webrtc_poc` directory, I provided the command line parameter file that triggers the vulnerability, which is `command_line.txt`.
You can run it directly with macos to stably trigger the vulnerability.

Currently, it can trigger the vulnerability **100%** stably on my two Mac devices.

For detailed steps, please refer to `poc.mov`.In order to trigger renderer UAF multiple times more intuitively, I opened multiple <http://127.0.0.1/webrtc-extensions/RTCRtpParameters-codec.html> You can reduce the number of tabs according to your actual situation.

My command line results are also displayed in text format in the `asan_results.txt` file.

### zh...@gmail.com (2024-08-03)

### Here is an update on the progress of further optimization of vulnerability reproduction:

1. Please use macos to trigger the vulnerability, do not use linux and windows
2. Regarding the features required to trigger the vulnerability: You can reproduce the vulnerability by adding the following command line parameters in the startup parameters instead of applying my trigger.diff. The most concise command line feature parameter required to trigger the vulnerability is: `--enable-features=PMLoadingPageVoter,VSyncEncoding,WebRtcUseMinMaxVEADimensions`
3. It is recommended to trigger it by compiling asan chromium on mac. It is also possible to use the downloaded asan mac chromium. However, since most macs are arm, the downloaded asan mac runs very slowly after being translated by rosetta, which is a very bad experience. I don’t know whether it will be possible to download online arm mac asan chromium in the future (nevertheless, I can still reproduce the vulnerability in mac-release\_asan-mac-release-1336986)

### Summarize the updated and more concise reproduction steps, as well as some precautions:

Most of the steps are the same as in [#comment4](https://issues.chromium.org/issues/356423094#comment4). The features required to trigger the vulnerability are simplified to `--enable-features=PMLoadingPageVoter,VSyncEncoding,WebRtcUseMinMaxVEADimensions`

**However, actual tests have found that there are differences in stability on different computers. If you want to trigger the vulnerability 100% stably, you will need slightly more features:**

`--enable-features=PMLoadingPageVoter,VSyncDecoding,VSyncEncoding,WebRtcUseCaptureBeginTimestamp,WebRtcThreadsUseResourceEfficientType,WebRtcUseMinMaxVEADimensions`

For details, please refer to `poc_final.mov`

### zh...@gmail.com (2024-08-05)

## RCA

In the `VSyncEncodeAdapterMode` class, a pure raw pointer to the `TaskQueueBase` class is stored <https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/video/frame_cadence_adapter.cc;l=312;bpv=0;bpt=1>

```
class VSyncEncodeAdapterMode : public AdapterMode {

private:
    TaskQueueBase* queue_; // @here
}

```

When the `VSyncEncodeAdapterMode::EncodeAllEnqueuedFrames` function is executed, `queue_->PostTask` is called <https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/video/frame_cadence_adapter.cc;l=829;drc=c55c4a4997144a5ff358f3271f5a304dd1eff57d;bpv=1;bpt=1>

However, before this, the `queue_` object may have been released.

The call stack for releasing the object can refer to the path in asan:

```
    #1 0x117719dec in blink::WebRtcTaskQueue::Delete()+0x168 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x1ddec)
    #2 0x117eeeb14 in webrtc::VideoStreamEncoder::~VideoStreamEncoder()+0xb8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x7f2b14)
    #3 0x117eef39c in webrtc::VideoStreamEncoder::~VideoStreamEncoder()+0x8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x7f339c)
    #4 0x117eb93c8 in webrtc::internal::VideoSendStreamImpl::~VideoSendStreamImpl()+0x340 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x7bd3c8)
    #5 0x117eb95c4 in webrtc::internal::VideoSendStreamImpl::~VideoSendStreamImpl()+0x8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x7bd5c4)
    #6 0x117c7ccac in webrtc::internal::Call::DestroyVideoSendStream(webrtc::VideoSendStream*)+0x610 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x580cac)
    #7 0x1177d6edc in cricket::WebRtcVideoSendChannel::WebRtcVideoSendStream::~WebRtcVideoSendStream()+0x7c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xdaedc)
    #8 0x1177c1d58 in cricket::WebRtcVideoSendChannel::~WebRtcVideoSendChannel()+0x4ac (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xc5d58)
    #9 0x1177c2018 in non-virtual thunk to cricket::WebRtcVideoSendChannel::~WebRtcVideoSendChannel()+0xc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xc6018)
    #10 0x118664684 in cricket::BaseChannel::~BaseChannel()+0x614 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xf68684)
    #11 0x11867085c in cricket::VideoChannel::~VideoChannel()+0x1b4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xf7485c)
    #12 0x118670994 in cricket::VideoChannel::~VideoChannel()+0x8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xf74994)
    #13 0x175affb98 in webrtc::ThreadWrapper::ProcessPendingSends()+0x1ac (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0x2d8bb98)

```

### zh...@gmail.com (2024-08-05)

## To prove the above point:

- debug.diff

```
diff --git a/video/frame_cadence_adapter.cc b/video/frame_cadence_adapter.cc
index b11c7ba913..e85ac7784f 100644
--- a/video/frame_cadence_adapter.cc
+++ b/video/frame_cadence_adapter.cc
@@ -7,7 +7,7 @@
*  in the file PATENTS.  All contributing project authors may
*  be found in the AUTHORS file in the root of the source tree.
*/
-
+#include "base/logging.h"
#include "video/frame_cadence_adapter.h"

#include <algorithm>
@@ -826,6 +826,7 @@ void VSyncEncodeAdapterMode::EncodeAllEnqueuedFrames() {
(post_time - input.time_when_posted_us).ms());

const VideoFrame frame = std::move(input.video_frame);
+      LOG(ERROR) << "in EncodeAllEnqueuedFrames ,,, queue_ is: " <<queue_ << " !!! !!! zh1x1an";
queue_->PostTask(SafeTask(queue_safety_flag_, [this, post_time, frame] {
RTC_DCHECK_RUN_ON(queue_);

diff --git a/video/video_stream_encoder.cc b/video/video_stream_encoder.cc
index af26db8719..ba01f54bd6 100644
--- a/video/video_stream_encoder.cc
+++ b/video/video_stream_encoder.cc
@@ -7,7 +7,7 @@
*  in the file PATENTS.  All contributing project authors may
*  be found in the AUTHORS file in the root of the source tree.
*/
-
+#include "base/logging.h"
#include "video/video_stream_encoder.h"

#include <algorithm>
@@ -721,6 +721,7 @@ VideoStreamEncoder::~VideoStreamEncoder() {
// encoder_queue_.
// std::unique_ptr destructor does the same two operations in reverse order as
// it doesn't expect member would be used after its destruction has started.
+    LOG(ERROR) << "in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: " << encoder_queue_;
encoder_queue_.get_deleter()(encoder_queue_.get());
encoder_queue_.release();
}


```
```
cd third_party/webrtc
git apply debug.diff

```
## asan log result:

```
[62554:61955:0805/211624.637090:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611000e16a80
[62556:49923:0805/211624.637124:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62556:49923:0805/211624.637147:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62593:53763:0805/211624.638949:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001755240
[62608:52483:0805/211624.641430:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62608:52483:0805/211624.641487:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62608:52483:0805/211624.645756:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62608:52483:0805/211624.652947:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62608:52483:0805/211624.652990:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62562:48899:0805/211624.660197:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62556:49923:0805/211624.666523:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62556:49923:0805/211624.666577:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62608:52483:0805/211624.667165:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62608:52483:0805/211624.667189:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62608:52483:0805/211624.673997:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62608:52483:0805/211624.674038:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62593:53763:0805/211624.674119:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001757180
[62608:52483:0805/211624.677256:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62608:52483:0805/211624.677283:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62608:52483:0805/211624.683327:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62608:52483:0805/211624.688614:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62608:52483:0805/211624.688662:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62608:52483:0805/211624.692755:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62608:52483:0805/211624.692799:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62593:53763:0805/211624.699022:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001758f80
[62608:52483:0805/211624.699296:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62608:52483:0805/211624.699320:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62556:49923:0805/211624.699700:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62556:49923:0805/211624.699736:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62608:52483:0805/211624.702836:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62608:52483:0805/211624.702890:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62608:52483:0805/211624.708293:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62556:49923:0805/211624.712169:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62556:49923:0805/211624.712316:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62583:85763:0805/211624.727310:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211624.727339:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62583:85763:0805/211624.731966:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211624.731994:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62618:51971:0805/211624.733782:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001737240
[62583:85763:0805/211624.735476:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211624.735502:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62556:49923:0805/211624.739799:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62608:52483:0805/211624.740046:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211624.748735:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211624.748765:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62608:52483:0805/211624.769918:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62562:48899:0805/211624.773686:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211624.785775:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62546:48131:0805/211624.787113:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110010bb740 !!! !!! zh1x1an
[62585:62467:0805/211624.806532:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x61100103b540 !!! !!! zh1x1an
[62585:62467:0805/211624.806819:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110010ac100 !!! !!! zh1x1an
[62613:47875:0805/211624.809228:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x61100155c4c0 !!! !!! zh1x1an
[62613:47875:0805/211624.811356:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110015f9f40 !!! !!! zh1x1an
[62613:47875:0805/211624.812526:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001600fc0 !!! !!! zh1x1an
[62546:48131:0805/211624.813190:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110010cc7c0 !!! !!! zh1x1an
[62546:48131:0805/211624.813333:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110010cf880 !!! !!! zh1x1an
[62541:59139:0805/211624.821652:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110014dca40 !!! !!! zh1x1an
[62585:62467:0805/211624.822012:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110010af440 !!! !!! zh1x1an
[62527:52483:0805/211624.822541:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x61100156b380 !!! !!! zh1x1an
[62540:47107:0805/211624.849190:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110010cc040 !!! !!! zh1x1an
[62613:47875:0805/211624.852053:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001604080 !!! !!! zh1x1an
[62547:61699:0805/211624.853397:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110010d3840 !!! !!! zh1x1an
[62547:61699:0805/211624.853432:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110010e0900 !!! !!! zh1x1an
[62590:61187:0805/211624.858759:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110010cb500 !!! !!! zh1x1an
[62614:62467:0805/211624.866866:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x61100109f400 !!! !!! zh1x1an
[62540:47107:0805/211624.867072:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110010cf100 !!! !!! zh1x1an
[62540:47107:0805/211624.867196:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x61100105bd40 !!! !!! zh1x1an
[62614:62467:0805/211624.867394:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110010a24c0 !!! !!! zh1x1an
[62614:62467:0805/211624.868100:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110010a5580 !!! !!! zh1x1an
[62565:35587:0805/211624.873169:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x61100054ab40 !!! !!! zh1x1an
[62558:45059:0805/211624.878532:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611000568140
[62554:61955:0805/211624.881460:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611000e59c40 !!! !!! zh1x1an
[62590:61187:0805/211624.882946:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x61100105b5c0 !!! !!! zh1x1an
[62590:61187:0805/211624.882995:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110010ce700 !!! !!! zh1x1an
[62568:59395:0805/211624.890742:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x61100158f780 !!! !!! zh1x1an
[62568:59395:0805/211624.890876:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x61100162d0c0 !!! !!! zh1x1an
[62541:59139:0805/211624.891566:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110015f2c40 !!! !!! zh1x1an
[62561:48643:0805/211624.892163:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110010fd3c0 !!! !!! zh1x1an
[62541:59139:0805/211624.892476:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110015f5d00 !!! !!! zh1x1an
[62561:48643:0805/211624.892564:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001075c40 !!! !!! zh1x1an
[62541:59139:0805/211624.892575:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001620640 !!! !!! zh1x1an
[62574:47619:0805/211624.880662:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611000e57a80 !!! !!! zh1x1an
[62574:47619:0805/211624.893642:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611000e59880 !!! !!! zh1x1an
[62561:48643:0805/211624.904035:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110010f0300 !!! !!! zh1x1an
[62554:61955:0805/211624.906381:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611000e5ba40 !!! !!! zh1x1an
[62603:46083:0805/211624.914699:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x6110009e7cc0
[62547:61699:0805/211624.915018:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110010e39c0 !!! !!! zh1x1an
[62568:59395:0805/211624.916370:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001630180 !!! !!! zh1x1an
[62568:59395:0805/211624.916517:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001641200 !!! !!! zh1x1an
[62554:61955:0805/211624.921026:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611000e5d840 !!! !!! zh1x1an
[62574:47619:0805/211624.927540:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611000e5b7c0 !!! !!! zh1x1an
[62565:35587:0805/211624.933540:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x61100054ab40
[62573:60675:0805/211624.941485:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110015600c0 !!! !!! zh1x1an
[62589:47619:0805/211624.946857:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x6110009dc640
[62573:60675:0805/211624.954884:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001601880 !!! !!! zh1x1an
[62573:60675:0805/211624.969571:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001604a80 !!! !!! zh1x1an
[62573:60675:0805/211624.969677:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001607b40 !!! !!! zh1x1an
[62583:85763:0805/211624.990239:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211624.990328:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62608:52483:0805/211624.997167:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62562:48899:0805/211624.999172:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62608:52483:0805/211625.009922:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62556:49923:0805/211625.001062:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211625.015969:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211625.016011:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62556:49923:0805/211625.027194:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211625.063424:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211625.063454:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62617:67587:0805/211625.068387:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62617:67587:0805/211625.068464:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62556:49923:0805/211625.069078:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.070388:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.070429:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62562:48899:0805/211625.070738:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62589:47619:0805/211625.072546:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110009de440 !!! !!! zh1x1an
[62589:47619:0805/211625.094870:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x6110009de440
[62569:66819:0805/211625.095029:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.095062:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62551:59907:0805/211625.096099:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001578800 !!! !!! zh1x1an
[62551:59907:0805/211625.096365:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x61100161a4c0 !!! !!! zh1x1an
[62551:59907:0805/211625.096465:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x61100161d580 !!! !!! zh1x1an
[62551:59907:0805/211625.096658:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001620640 !!! !!! zh1x1an
[62603:46083:0805/211625.112506:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110009e9c00 !!! !!! zh1x1an
[62583:85763:0805/211625.133549:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211625.133604:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62617:67587:0805/211625.137348:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62617:67587:0805/211625.137378:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62569:66819:0805/211625.141011:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.141042:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62603:46083:0805/211625.156957:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x6110009e9c00
[62617:67587:0805/211625.168188:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62617:67587:0805/211625.168224:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62583:85763:0805/211625.182083:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.182281:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.182322:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62598:67843:0805/211625.203972:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001f0dc80 !!! !!! zh1x1an
[62617:67587:0805/211625.215145:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62617:67587:0805/211625.215175:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62555:47895:0805/211625.220862:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x61100156aac0 !!! !!! zh1x1an
[62555:47895:0805/211625.220901:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x61100160cc80 !!! !!! zh1x1an
[62555:47895:0805/211625.220921:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x61100160fd40 !!! !!! zh1x1an
[62569:66819:0805/211625.232333:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62545:53507:0805/211625.234574:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001ab5c00
[62545:53507:0805/211625.239674:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001aba340
[62545:53507:0805/211625.242759:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001bdfa40 !!! !!! zh1x1an
[62545:53507:0805/211625.242829:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001be1840 !!! !!! zh1x1an
[62545:53507:0805/211625.242859:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001b4c9c0 !!! !!! zh1x1an
[62545:53507:0805/211625.242889:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001b51100 !!! !!! zh1x1an
[62545:53507:0805/211625.242913:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001b55840 !!! !!! zh1x1an
[62534:53507:0805/211625.245793:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001aae400
[62583:85763:0805/211625.252937:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62617:67587:0805/211625.255967:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62545:53507:0805/211625.283661:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001b4c9c0
[62534:53507:0805/211625.300035:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001b28ac0
[62534:53507:0805/211625.301498:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001bce880 !!! !!! zh1x1an
[62534:53507:0805/211625.301629:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001b28ac0 !!! !!! zh1x1an
=================================================================
==62534==ERROR: AddressSanitizer: heap-use-after-free on address 0x611001b28ac0 at pc 0x000114745ff0 bp 0x000381582530 sp 0x000381582528
READ of size 8 at 0x611001b28ac0 thread T18
[62545:53507:0805/211625.307289:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001b51100
[62555:47895:0805/211625.307718:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001613a80 !!! !!! zh1x1an
[62545:53507:0805/211625.309146:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001b59f80 !!! !!! zh1x1an
[62569:66819:0805/211625.322816:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.322853:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62583:85763:0805/211625.332298:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62545:53507:0805/211625.332871:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001b55840
[62552:86275:0805/211625.349914:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001ec4580
[62545:53507:0805/211625.355497:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001b59f80
==62534==WARNING: invalid path to external symbolizer!
==62534==WARNING: Failed to use and restart external symbolizer!
[62569:66819:0805/211625.359857:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.359933:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62583:85763:0805/211625.365409:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211625.365448:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62617:67587:0805/211625.377019:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.381919:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.381961:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62583:85763:0805/211625.384441:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211625.384478:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62598:67843:0805/211625.385324:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001fab700 !!! !!! zh1x1an
[62598:67843:0805/211625.385410:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001fb0200 !!! !!! zh1x1an
[62598:67843:0805/211625.385462:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001fb4bc0 !!! !!! zh1x1an
[62598:67843:0805/211625.385532:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001fb96c0 !!! !!! zh1x1an
[62617:67587:0805/211625.398343:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62617:67587:0805/211625.398511:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62569:66819:0805/211625.404697:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.404774:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62583:85763:0805/211625.408294:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211625.408328:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62552:86275:0805/211625.408412:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001f6c000 !!! !!! zh1x1an
[62552:86275:0805/211625.408470:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001f70740 !!! !!! zh1x1an
[62552:86275:0805/211625.408649:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001f74fc0 !!! !!! zh1x1an
[62545:53507:0805/211625.412158:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001bdfa40
[62552:86275:0805/211625.423397:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001f79840 !!! !!! zh1x1an
[62617:67587:0805/211625.424073:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62617:67587:0805/211625.424111:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62552:86275:0805/211625.427161:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001f7e340 !!! !!! zh1x1an
[62552:86275:0805/211625.427288:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001fbee40 !!! !!! zh1x1an
[62552:86275:0805/211625.427431:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001f67780 !!! !!! zh1x1an
[62569:66819:0805/211625.431632:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211625.442060:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211625.442200:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62617:67587:0805/211625.447669:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62617:67587:0805/211625.447699:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62552:86275:0805/211625.453583:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001f67780
[62583:85763:0805/211625.454354:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62601:61187:0805/211625.456405:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x61100057bc40
[62569:66819:0805/211625.457209:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211625.461504:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211625.461565:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62617:67587:0805/211625.466861:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62617:67587:0805/211625.466902:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62552:86275:0805/211625.468156:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001f6c000
[62538:63747:0805/211625.468164:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611000567600
[62569:66819:0805/211625.470231:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62593:53763:0805/211625.472511:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001a3d700 !!! !!! zh1x1an
[62583:85763:0805/211625.473819:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211625.473856:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62569:66819:0805/211625.478133:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.478209:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62617:67587:0805/211625.478896:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211625.480308:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211625.480352:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62552:86275:0805/211625.480340:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001f70740
[62569:66819:0805/211625.486230:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.486514:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62617:67587:0805/211625.491305:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62617:67587:0805/211625.491342:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62583:85763:0805/211625.492981:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211625.493012:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62552:86275:0805/211625.493259:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001f74fc0
[62569:66819:0805/211625.495431:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.495726:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62617:67587:0805/211625.497623:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62617:67587:0805/211625.497654:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62601:61187:0805/211625.501508:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x6110005b5940
[62617:67587:0805/211625.502731:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62617:67587:0805/211625.502752:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62583:85763:0805/211625.504679:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.505317:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.505347:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62552:86275:0805/211625.506452:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001f79840
[62617:67587:0805/211625.508958:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62617:67587:0805/211625.508995:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62583:85763:0805/211625.510113:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211625.510133:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62569:66819:0805/211625.516165:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62552:86275:0805/211625.520276:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001f7e340
[62583:85763:0805/211625.520377:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211625.520429:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62617:67587:0805/211625.522253:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.522926:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.522962:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62538:63747:0805/211625.523815:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x61100059de80
[62552:86275:0805/211625.523876:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001fbee40
[62545:53507:0805/211625.524068:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001be1840
[62601:61187:0805/211625.524375:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x6110005b97c0
[62583:85763:0805/211625.525723:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211625.525765:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62617:67587:0805/211625.525968:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62617:67587:0805/211625.525990:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62569:66819:0805/211625.526490:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.526509:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62617:67587:0805/211625.539513:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62617:67587:0805/211625.539557:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62583:85763:0805/211625.539625:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211625.539648:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62569:66819:0805/211625.541275:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.541311:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62617:67587:0805/211625.542975:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62617:67587:0805/211625.543002:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62545:53507:0805/211625.543455:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001be4a40
[62583:85763:0805/211625.543931:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.544336:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.544360:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62617:67587:0805/211625.546108:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62617:67587:0805/211625.546792:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62583:85763:0805/211625.548772:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211625.548827:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62569:66819:0805/211625.550410:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62617:67587:0805/211625.551082:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211625.553367:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211625.553420:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62569:66819:0805/211625.554056:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.554149:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62617:67587:0805/211625.555056:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62617:67587:0805/211625.555086:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62583:85763:0805/211625.557257:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211625.557300:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62569:66819:0805/211625.557357:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.557373:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62569:66819:0805/211625.564611:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.564639:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
    #0 0x114745fec in webrtc::(anonymous namespace)::VSyncEncodeAdapterMode::EncodeAllEnqueuedFrames()+0x970 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x7d1fec)
    #1 0x1147450f4 in webrtc::(anonymous namespace)::VSyncEncodeAdapterMode::OnFrame(webrtc::Timestamp, bool, webrtc::VideoFrame const&)+0x7a8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x7d10f4)
    #2 0x171e67fec in webrtc::ThreadWrapper::RunTaskQueueTask(absl::AnyInvocable<void () &&>)+0x54 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0x2d8bfec)
    #3 0x171e6abc4 in void base::internal::DecayedFunctorTraits<void (webrtc::ThreadWrapper::*)(absl::AnyInvocable<void () &&>), base::WeakPtr<webrtc::ThreadWrapper>&&, absl::AnyInvocable<void () &&>&&>::Invoke<void (webrtc::ThreadWrapper::*)(absl::AnyInvocable<void () &&>), base::WeakPtr<webrtc::ThreadWrapper> const&, absl::AnyInvocable<void () &&>>(void (webrtc::ThreadWrapper::*)(absl::AnyInvocable<void () &&>), base::WeakPtr<webrtc::ThreadWrapper> const&, absl::AnyInvocable<void () &&>&&)+0x174 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0x2d8ebc4)
    #4 0x171e6a9ac in base::internal::Invoker<base::internal::FunctorTraits<void (webrtc::ThreadWrapper::*&&)(absl::AnyInvocable<void () &&>), base::WeakPtr<webrtc::ThreadWrapper>&&, absl::AnyInvocable<void () &&>&&>, base::internal::BindState<true, true, false, void (webrtc::ThreadWrapper::*)(absl::AnyInvocable<void () &&>), base::WeakPtr<webrtc::ThreadWrapper>, absl::AnyInvocable<void () &&>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x110 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0x2d8e9ac)
    #5 0x103846708 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x34c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x1ae708)
    #6 0x1038b2c64 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x7f0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x21ac64)
    #7 0x1038b20d8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x21a0d8)
    #8 0x1037219f4 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x1b0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x899f4)
    #9 0x1038b4210 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x3cc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x21c210)
    #10 0x1037cef4c in base::RunLoop::Run(base::Location const&)+0x434 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x136f4c)
    #11 0x103944aa4 in base::Thread::Run(base::RunLoop*)+0xd8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib[62545:53507:0805/211625.565633:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001be6c00
:arm64+0x2acaa4)
    #12 0x103944f0c in base::Thread::ThreadMain()+0x3e0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x2acf0c)
    #13 0x10399934c in base::(anonymous namespace)::ThreadFunc(void*)+0x12c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x30134c)
    #14 0x101c51d18 in __sanitizer_weak_hook_memcmp+0x35118 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libclang_rt.asan_osx_dynamic.dylib:arm64+0x4dd18)
    #15 0x19c0e5f90 in _pthread_start+0x84 (/usr/lib/system/libsystem_pthread.dylib:arm64+0x6f90)
    #16 0x702c00019c0e0d30  (<unknown module>)

0x611001b28ac0 is located 0 bytes inside of 216-byte region [0x611001b28ac0,0x611001b28b98)
freed by thread T18 here:
[62569:66819:0805/211625.567754:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.567810:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62617:67587:0805/211625.569511:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62617:67587:0805/211625.569594:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62569:66819:0805/211625.572917:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211625.572919:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211625.572953:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62617:67587:0805/211625.573525:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62617:67587:0805/211625.573548:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62552:86275:0805/211625.575546:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x61100200c000
[62617:67587:0805/211625.576736:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62617:67587:0805/211625.576757:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62583:85763:0805/211625.577306:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.577472:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.577494:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62569:66819:0805/211625.581130:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.581171:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62583:85763:0805/211625.581271:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211625.581291:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62617:67587:0805/211625.581678:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.589068:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.589099:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62545:53507:0805/211625.589654:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x61100017e340
[62583:85763:0805/211625.590065:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211625.590084:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62617:67587:0805/211625.590152:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62617:67587:0805/211625.590169:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62569:66819:0805/211625.592098:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.592119:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62617:67587:0805/211625.593375:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62617:67587:0805/211625.593420:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62552:86275:0805/211625.594036:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x61100200df40
[62583:85763:0805/211625.594510:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211625.594560:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62569:66819:0805/211625.596786:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62617:67587:0805/211625.596932:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62617:67587:0805/211625.596965:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62583:85763:0805/211625.598368:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211625.598402:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62617:67587:0805/211625.599800:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62617:67587:0805/211625.599841:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62598:67843:0805/211625.601004:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001f0dc80
[62569:66819:0805/211625.601099:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.601124:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62583:85763:0805/211625.602580:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62598:67843:0805/211625.604102:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001f12c80
[62617:67587:0805/211625.604747:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.605979:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.606080:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62617:67587:0805/211625.611799:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62617:67587:0805/211625.611837:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62545:53507:0805/211625.612156:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611000149f00
[62569:66819:0805/211625.612559:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.612589:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62598:67843:0805/211625.616163:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001fab700
[62552:86275:0805/211625.616249:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x61100200fe80
[62617:67587:0805/211625.616397:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62617:67587:0805/211625.616443:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62617:67587:0805/211625.619973:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62617:67587:0805/211625.620012:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62617:67587:0805/211625.623417:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62617:67587:0805/211625.623440:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62598:67843:0805/211625.626317:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001fb0200
[62618:51971:0805/211625.626880:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001a59f40 !!! !!! zh1x1an
[62569:66819:0805/211625.628298:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.628359:ERROR:peer_connection.cc(1159)] Attempted to use an unsupported codec for layer 0 (UNSUPPORTED_OPERATION)
[62583:85763:0805/211625.635479:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.635550:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62598:67843:0805/211625.637495:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001fb4bc0
    #0 0x101c64500 in __sanitizer_finish_switch_fiber+0xa24 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libclang_rt.asan_osx_dynamic.dylib:arm64+0x60500)
    #1 0x113f91dec in blink::WebRtcTaskQueue::Delete()+0x168 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x1ddec)
    #2 0x114766cdc in webrtc::VideoStreamEncoder::~VideoStreamEncoder()+0x1f4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x7f2cdc)
    #3 0x1147675e0 in webrtc::VideoStreamEncoder::~VideoStreamEncoder()+0x8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x7f35e0)
    #4 0x1147313c8 in webrtc::internal::VideoSendStreamImpl::~VideoSendStreamImpl()+0x340 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x7bd3c8)
    #5 0x1147315c4 in webrtc::internal::VideoSendStreamImpl::~VideoSendStreamImpl()+0x8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x7bd5c4)
    #6 0x1144f4cac in webrtc::internal::Call::DestroyVideoSendStream(webrtc::VideoSendStream*)+0x610 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x580cac)
    #7 0x114051c70 in cricket::WebRtcVideoSendChannel::WebRtcVideoSendStream::RecreateWebRtcStream()+0x148 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xddc70)
    #8 0x11404ebd8 in cricket::WebRtcVideoSendChannel::WebRtcVideoSendStream::SetCodec(cricket::VideoCodecSettings const&)+0x5ec (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xdabd8)
    #9 0x1140424c8 in cricket::WebRtcVideoSendChannel::WebRtcVideoSendStream::SetSenderParameters(cricket::WebRtcVideoSendChannel::ChangedSenderParameters const&)+0x438 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xce4c8)
    #10 0x114040998 in cricket::WebRtcVideoSendChannel::ApplyChangedParams(cricket::WebRtcVideoSendChannel::ChangedSenderParameters const&)+0x484 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xcc998)
    #11 0x1140439cc in cricket::WebRtcVideoSendChannel::SetRtpSendParameters(unsigned int, webrtc::RtpParameters const&, absl::AnyInvocable<void (webrtc::RTCError) &&>)+0x704 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xcf9cc)
    #12 0x114fe5f2c in webrtc::RtpSenderBase::SetParametersInternal(webrtc::RtpParameters const&, absl::AnyInvocable<void (webrtc::RTCError) &&>, bool)::$_1::operator()()+0x864 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x1071f2c)
    #13 0x171e67fec in webrtc::ThreadWrapper::RunTaskQueueTask(absl::AnyInvocable<void () &&>)+0x54 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0x2d8bfec)
    #14 0x171e6abc4 in void base::internal::DecayedFunctorTraits<void (webrtc::ThreadWrapper::*)(absl::AnyInvocable<void () &&>), base::WeakPtr<webrtc::ThreadWrapper>&&, absl::AnyInvocable<void () &&>&&>::Invoke<void (webrtc::ThreadWrapper::*)(absl::AnyInvocable<void () &&>), base::WeakPtr<webrtc::ThreadWrapper> const&, absl::AnyInvocable<void () &&>>(void (webrtc::ThreadWrapper::*)(absl::AnyInvocable<void () &&>), base::WeakPtr<webrtc::ThreadWrapper> const&, absl::AnyInvocable<void () &&>&&)+0x174 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0x2d8ebc4)
    #15 0x171e6a9ac in base::internal::Invoker<base::internal::FunctorTraits<void (webrtc::ThreadWrapper::*&&)(absl::AnyInvocable<void () &&>), base::WeakPtr<webrtc::ThreadWrapper>&&, absl::AnyInvocable<void () &&>&&>, base::internal::BindState<true, true, false, void (webrtc::ThreadWrapper::*)(absl::AnyInvocable<void () &&>), base::WeakPtr<webrtc::ThreadWrapper>, absl::AnyInvocable<void () &&>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x110 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0x2d8e9ac)
    #16 0x103846708 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x34c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x1ae708)
    #17 0x1038b2c64 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x7f0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x21ac64)
    #18 0x1038b20d8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x21a0d8)
    #19 0x1037219f4 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x1b0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x899f4)
    #20 0x1038b4210 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x3cc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x21c210)
    #21 0x1037cef4c in base::RunLoop::Run(base::Location const&)+0x434 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x136f4c)
    #22 0x103944aa4 in base::Thread::Run(base::RunLoop*)+0xd8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x2acaa4)
    #23 0x103944f0c in base::Thread::ThreadMain()+0x3e0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x2acf0c)
    #24 0x10399934c in base::(anonymous namespace)::ThreadFunc(void*)+0x12c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x30134c)
    #25 0x101c51d18 in __sanitizer_weak_hook_memcmp+0x35118 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libclang_rt.asan_osx_dynamic.dylib:arm64+0x4dd18)
    #26 0x19c0e5f90 in _pthread_start+0x84 (/usr/lib/system/libsystem_pthread.dylib:arm64+0x6f90)
    #27 0x702c00019c0e0d30  (<unknown module>)

previously allocated by thread T18 here:
[62617:67587:0805/211625.639951:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62583:85763:0805/211625.643482:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62598:67843:0805/211625.647547:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001fb96c0
[62552:86275:0805/211625.647852:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611002011f00
[62583:85763:0805/211625.648852:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62598:67843:0805/211625.651084:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001fe1080
[62583:85763:0805/211625.659720:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62566:66563:0805/211625.660040:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001f43100
[62566:66563:0805/211625.665469:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001f47980
[62617:67587:0805/211625.665663:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62598:67843:0805/211625.665813:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611000038440
[62566:66563:0805/211625.667181:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001f821c0
[62566:66563:0805/211625.669111:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001f86900
[62583:85763:0805/211625.669224:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62566:66563:0805/211625.670845:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001f8b040
[62617:67587:0805/211625.672511:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62566:66563:0805/211625.673208:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001f8f8c0
    #0 0x101c640f8 in __sanitizer_finish_switch_fiber+0x61c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libclang_rt.asan_osx_dynamic.dylib:arm64+0x600f8)
    #1 0x113f93c38 in blink::(anonymous namespace)::WebrtcTaskQueueFactory::CreateTaskQueue(std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>, webrtc::TaskQueueFactory::Priority) const+0xb4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x1fc38)
    #2 0x11472f9bc in webrtc::internal::VideoSendStreamImpl::VideoSendStreamImpl(webrtc::Environment const&, int, webrtc::RtcpRttStats*, webrtc::RtpTransportControllerSendInterface*, webrtc::Metronome*, webrtc::BitrateAllocatorInterface*, webrtc::SendDelayStats*, webrtc::VideoSendStream::Config, webrtc::VideoEncoderConfig, std::__Cr::map<unsigned int, webrtc::RtpState, std::__Cr::less<unsigned int>, std::__Cr::allocator<std::__Cr::pair<unsigned int const, webrtc::RtpState>>> const&, std::__Cr::map<unsigned int, webrtc::RtpPayloadState, std::__Cr::less<unsigned int>, std::__Cr::allocator<std::__Cr::pair<unsigned int const, webrtc::RtpPayloadState>>> const&, std::__Cr::unique_ptr<webrtc::FecController, std::__Cr::default_delete<webrtc::FecController>>, std::__Cr::unique_ptr<webrtc::VideoStreamEncoderInterface, std::__Cr::default_delete<webrtc::VideoStreamEncoderInterface>>)+0x460 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x7bb9bc)
    #3 0x1144f3bec in webrtc::internal::Call::CreateVideoSendStream(webrtc::VideoSendStream::Config, webrtc::VideoEncoderConfig, std::__Cr::unique_ptr<webrtc::FecController, std::__Cr::default_delete<webrtc::FecController>>)+0x65c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x57fbec)
    #4 0x1144f45cc in webrtc::internal::Call::CreateVideoSendStream(webrtc::VideoSendStream::Config, webrtc::VideoEncoderConfig)+0x214 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x5805cc)
    #5 0x114051f08 in cricket::WebRtcVideoSendChannel::WebRtcVideoSendStream::RecreateWebRtcStream()+0x3e0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xddf08)
    #6 0x11404ebd8 in cricket::WebRtcVideoSendChannel::WebRtcVideoSendStream::SetCodec(cricket::VideoCodecSettings const&)+0x5ec (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xdabd8)
    #7 0x1140424c8 in cricket::WebRtcVideoSendChannel::WebRtcVideoSendStream::SetSenderParameters(cricket::WebRtcVideoSendChannel::ChangedSenderParameters const&)+0x438 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xce4c8)
    #8 0x114040998 in cricket::WebRtcVideoSendChannel::ApplyChangedParams(cricket::WebRtcVideoSendChannel::ChangedSenderParameters const&)+0x484 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xcc998)
    #9 0x11403fd48 in cricket::WebRtcVideoSendChannel::SetSenderParameters(cricket::VideoSenderParameters const&)+0x5e4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xcbd48)
    #10 0x114eeb400 in cricket::VideoChannel::SetRemoteContent_w(cricket::MediaContentDescription const*, webrtc::SdpType, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>&)+0xc18 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xf77400)
    #11 0x114ede6d8 in cricket::BaseChannel::SetRemoteContent(cricket::MediaContentDescription const*, webrtc::SdpType, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>&)+0x158 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xf6a6d8)
    #12 0x1150dfed4 in void rtc::FunctionView<void ()>::CallVoidPtr<bool rtc::Thread::BlockingCall<webrtc::SdpOfferAnswerHandler::PushdownMediaDescription(webrtc::SdpType, cricket::ContentSource, std::__Cr::map<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, cricket::ContentGroup const*, std::__Cr::less<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>, std::__Cr::allocator<std::__Cr::pair<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const, cricket::ContentGroup const*>>> const&)::$_2, bool, void>(webrtc::SdpOfferAnswerHandler::PushdownMediaDescription(webrtc::SdpType, cricket::ContentSource, std::__Cr::map<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, cricket::ContentGroup const*, std::__Cr::less<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>, std::__Cr::allocator<std::__Cr::pair<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const, cricket::ContentGroup const*>>> const&)::$_2&&, base::Location const&)::'lambda'()>(rtc::FunctionView<void ()>::VoidUnion)+0x114 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x116bed4)
    #13 0x171e67b98 in webrtc::ThreadWrapper::ProcessPendingSends()+0x1ac (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0x2d8bb98)
    #14 0x171e6a6c8 in void base::internal::Invoker<base::internal::FunctorTraits<void (webrtc::ThreadWrapper::*&&)(), base::WeakPtr<webrtc::ThreadWrapper>&&>, base::internal::BindState<true, true, false, void (webrtc::ThreadWrapper::*)(), base::WeakPtr<webrtc::ThreadWrapper>>, void ()>::RunImpl<void (webrtc::ThreadWrapper::*)(), std::__Cr::tuple<base::WeakPtr<webrtc::ThreadWrapper>>, 0ul>(void (webrtc::ThreadWrapper::*&&)(), std::__Cr::tuple<base::WeakPtr<webrtc::ThreadWrapper>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>)+0x16c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0x2d8e6c8)
    #15 0x103846708 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x34c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x1ae708)
    #16 0x1038b2c64 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x7f0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x21ac64)
    #17 0x1038b20d8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x21a0d8)
    #18 0x1037219f4 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x1b0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x899f4)
    #19 0x1038b4210 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x3cc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x21c210)
    #20 0x1037cef4c in base::RunLoop::Run(base::Location const&)+0x434 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x136f4c)
    #21 0x103944aa4 in base::Thread::Run(base::RunLoop*)+0xd8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x2acaa4)
    #22 0x103944f0c in base::Thread::ThreadMain()+0x3e0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x2acf0c)
    #23 0x10399934c in base::(anonymous namespace)::ThreadFunc(void*)+0x12c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x30134c)
    #24 0x101c51d18 in __sanitizer_weak_hook_memcmp+0x35118 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libclang_rt.asan_osx_dynamic.dylib:arm64+0x4dd18)
    #25 0x19c0e5f90 in _pthread_start+0x84 (/usr/lib/system/libsystem_pthread.dylib:arm64+0x6f90)
    #26 0x702c00019c0e0d30  (<unknown module>)

Thread T18 created by T0 here:
[62569:66819:0805/211625.675082:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62552:86275:0805/211625.676734:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611002013e40
[62566:66563:0805/211625.676866:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001fb23c0
[62617:67587:0805/211625.682020:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.684317:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.690533:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.694669:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62617:67587:0805/211625.698723:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62569:66819:0805/211625.702343:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62598:67843:0805/211625.706354:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611000231940
[62617:67587:0805/211625.706717:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62617:67587:0805/211625.711306:ERROR:media_engine.cc(94)] Attempted to use an unsupported codec for layer 0 (INVALID_MODIFICATION)
[62552:86275:0805/211625.711684:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x6110010eeb40
[62598:67843:0805/211625.722583:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611000254080
[62556:57603:0805/211625.727244:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611000722440
[62601:61187:0805/211625.731827:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x6110007d1580
[62598:67843:0805/211625.744704:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x61100022eec0
[62556:57603:0805/211625.755593:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611000779c40
[62601:61187:0805/211625.767375:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611000814c40
[62561:48643:0805/211625.790638:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001075c40 !!! !!! zh1x1an
[62618:51971:0805/211625.794801:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001b398c0 !!! !!! zh1x1an
[62540:47107:0805/211625.795288:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110010cf100 !!! !!! zh1x1an
[62585:62467:0805/211625.795580:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110010ac100 !!! !!! zh1x1an
[62585:62467:0805/211625.795618:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110010af440 !!! !!! zh1x1an
[62585:62467:0805/211625.795638:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x61100103b540 !!! !!! zh1x1an
[62590:61187:0805/211625.795910:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110010ce700 !!! !!! zh1x1an
[62603:46083:0805/211625.795931:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611000b8cbc0 !!! !!! zh1x1an
[62555:47895:0805/211625.805362:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x61100160cc80 !!! !!! zh1x1an
[62618:51971:0805/211625.806816:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001b4aa80 !!! !!! zh1x1an
[62568:59395:0805/211625.812230:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x61100158f780 !!! !!! zh1x1an
[62589:47619:0805/211625.813166:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611000b81680 !!! !!! zh1x1an
[62561:48643:0805/211625.814138:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110010fd3c0 !!! !!! zh1x1an
[62566:66563:0805/211625.814267:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x61100203aa40 !!! !!! zh1x1an
[62613:47875:0805/211625.818533:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001600fc0 !!! !!! zh1x1an
[62590:61187:0805/211625.818650:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x61100105b5c0 !!! !!! zh1x1an
[62551:59907:0805/211625.819573:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x61100161a4c0 !!! !!! zh1x1an
[62565:35587:0805/211625.827363:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110006254c0 !!! !!! zh1x1an
[62603:46083:0805/211625.828174:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611000b8fc80 !!! !!! zh1x1an
[62554:61955:0805/211625.828232:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611000e59c40 !!! !!! zh1x1an
[62558:45059:0805/211625.828263:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110006506c0 !!! !!! zh1x1an
[62547:61699:0805/211625.830612:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110010d3840 !!! !!! zh1x1an
[62593:53763:0805/211625.831766:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001b64e80 !!! !!! zh1x1an
[62555:47895:0805/211625.831889:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x61100156aac0 !!! !!! zh1x1an
[62527:52483:0805/211625.834165:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x61100156b380
[62561:48643:0805/211625.835898:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110010f0300 !!! !!! zh1x1an
[62589:47619:0805/211625.836192:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611000b84740 !!! !!! zh1x1an
[62618:51971:0805/211625.836821:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001a59f40 !!! !!! zh1x1an
[62598:67843:0805/211625.837342:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x61100022d0c0
[62614:62467:0805/211625.838597:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x61100109f400 !!! !!! zh1x1an
[62574:47619:0805/211625.839239:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611000e57a80
[62541:59139:0805/211625.839406:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110014dca40 !!! !!! zh1x1an
[62566:66563:0805/211625.840376:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611002044400 !!! !!! zh1x1an
[62547:61699:0805/211625.844076:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110010e0900 !!! !!! zh1x1an
[62551:59907:0805/211625.844887:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001578800
[62546:48131:0805/211625.845616:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x6110010bb740
[62573:60675:0805/211625.850997:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110015600c0 !!! !!! zh1x1an
[62590:61187:0805/211625.851420:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x61100105b5c0
[62618:51971:0805/211625.851528:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001b33600 !!! !!! zh1x1an
[62568:59395:0805/211625.852048:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001641200 !!! !!! zh1x1an
[62593:53763:0805/211625.852438:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001b71f40 !!! !!! zh1x1an
[62601:61187:0805/211625.852897:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611000818ac0
[62547:61699:0805/211625.853470:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110010e39c0 !!! !!! zh1x1an
[62554:61955:0805/211625.857204:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611000e59c40
[62613:47875:0805/211625.858138:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x61100155c4c0 !!! !!! zh1x1an
[62566:66563:0805/211625.858580:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611002036a80 !!! !!! zh1x1an
[62540:47107:0805/211625.861571:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110010cc040 !!! !!! zh1x1an
[62540:47107:0805/211625.861631:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x61100105bd40 !!! !!! zh1x1an
[62556:57603:0805/211625.862061:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611000781bc0
[62618:51971:0805/211625.862608:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001b36800 !!! !!! zh1x1an
[62561:48643:0805/211625.863027:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001075c40
[62541:59139:0805/211625.864157:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110015f2c40 !!! !!! zh1x1an
[62555:47895:0805/211625.864597:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x61100156aac0
[62593:53763:0805/211625.867954:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001b5ebc0 !!! !!! zh1x1an
[62614:62467:0805/211625.869212:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x61100109f400
[62573:60675:0805/211625.869374:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x6110015600c0
[62566:66563:0805/211625.874885:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611002040800 !!! !!! zh1x1an
[62566:66563:0805/211625.874929:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611002038c40 !!! !!! zh1x1an
[62593:53763:0805/211625.875275:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001b61c80 !!! !!! zh1x1an
[62613:47875:0805/211625.877234:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x61100155c4c0
[62566:66563:0805/211625.877623:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110020465c0 !!! !!! zh1x1an
[62593:53763:0805/211625.878026:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001a3d700 !!! !!! zh1x1an
[62566:66563:0805/211625.880434:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611002042600 !!! !!! zh1x1an
[62568:59395:0805/211625.883027:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x61100158f780
[62585:62467:0805/211625.885107:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x61100103b540
[62540:47107:0805/211625.890912:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x61100105bd40
[62541:59139:0805/211625.893274:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x6110015f2c40
[62547:61699:0805/211625.904062:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x6110010d3840
[62551:59907:0805/211625.916885:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001620640 !!! !!! zh1x1an
[62556:57603:0805/211625.916977:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611000785a40
[62551:59907:0805/211625.917294:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x61100161d580 !!! !!! zh1x1an
[62554:61955:0805/211625.929615:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611000e5ba40
[62598:67843:0805/211625.929645:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x61100022a000
[62546:48131:0805/211625.934598:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x6110010cc7c0
[62568:59395:0805/211625.936152:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001630180 !!! !!! zh1x1an
[62561:48643:0805/211625.948604:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x6110010f0300
[62555:47895:0805/211625.949702:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001613a80 !!! !!! zh1x1an
[62555:47895:0805/211625.949739:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x61100160fd40 !!! !!! zh1x1an
[62574:47619:0805/211625.957465:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611000e59880
[62541:59139:0805/211625.963219:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001620640 !!! !!! zh1x1an
[62614:62467:0805/211625.964418:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x6110010a24c0
[62585:62467:0805/211625.975890:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x6110010ac100
[62608:58371:0805/211625.977832:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x61100087aa40
[62590:61187:0805/211625.979806:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x6110010cb500
[62573:60675:0805/211625.982052:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001601880
[62540:47107:0805/211625.982547:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x6110010cc040
[62541:59139:0805/211625.983787:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x6110015f5d00
[62562:49155:0805/211625.984876:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x6110006bc3c0
[62568:59395:0805/211625.996965:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x61100162d0c0
[62538:63747:0805/211626.008122:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x61100070ad40
[62613:47875:0805/211626.008727:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x6110015f9f40
[62547:61699:0805/211626.010623:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x6110010e0900
[62554:61955:0805/211626.026881:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611000e5d840
[62546:48131:0805/211626.074317:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x6110010cf880 !!! !!! zh1x1an
[62614:62467:0805/211626.074940:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x6110010a5580
[62561:48643:0805/211626.076943:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x6110010fd3c0
[62585:62467:0805/211626.081052:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x6110010af440
[62538:63747:0805/211626.081149:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x6110007e0440
[62573:60675:0805/211626.081444:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001607b40 !!! !!! zh1x1an
[62613:47875:0805/211626.089683:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001604080 !!! !!! zh1x1an
[62568:59395:0805/211626.091563:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001630180
[62573:60675:0805/211626.094151:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001604a80
[62590:61187:0805/211626.095170:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x6110010ce700
[62541:59139:0805/211626.098601:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001620640
[62574:47619:0805/211626.099122:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611000e5b7c0
[62540:47107:0805/211626.099831:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x6110010cf100
[62546:48131:0805/211626.105321:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x6110010cf880
[62613:47875:0805/211626.114982:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001600fc0
[62545:53507:0805/211626.123535:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611000d4b4c0 !!! !!! zh1x1an
[62545:53507:0805/211626.123636:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611000d47a00 !!! !!! zh1x1an
[62545:53507:0805/211626.123703:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611000c3fe00 !!! !!! zh1x1an
[62545:53507:0805/211626.129453:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611000cfc500 !!! !!! zh1x1an
[62545:53507:0805/211626.129568:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611000d3e540 !!! !!! zh1x1an
[62545:53507:0805/211626.129599:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611000cc7f80 !!! !!! zh1x1an
[62598:67843:0805/211626.147645:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611000e558c0
[62608:58371:0805/211626.172436:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x6110008ea340
[62547:61699:0805/211626.181815:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x6110010e39c0
[62613:47875:0805/211626.187249:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001604080
[62573:60675:0805/211626.187457:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001607b40
[62562:49155:0805/211626.210900:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x61100075bd80
[62608:58371:0805/211626.235928:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x6110008ee1c0
[62568:59395:0805/211626.242763:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611001641200
[62541:59139:0805/211626.254196:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x6110014dca40
[62562:49155:0805/211626.276593:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x61100075fd40
[62608:58371:0805/211626.310556:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x6110008fc540
[62562:49155:0805/211626.326016:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x611000763bc0
[62552:86275:0805/211626.344404:ERROR:frame_cadence_adapter.cc(829)] in EncodeAllEnqueuedFrames ,,, queue_ is: 0x611001b7f8c0 !!! !!! zh1x1an
[62608:58371:0805/211626.384658:ERROR:video_stream_encoder.cc(724)] in VideoStreamEncoder ~~~ ~~~ zh1x1an ,,, encoder_queue_: 0x6110008bc580
    #0 0x101c4ca98 in __sanitizer_weak_hook_memcmp+0x2fe98 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libclang_rt.asan_osx_dynamic.dylib:arm64+0x48a98)
    #1 0x103998a14 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType)+0x270 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x300a14)
    #2 0x1039438d8 in base::Thread::StartWithOptions(base::Thread::Options)+0x3f4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x2ab8d8)
    #3 0x1712c626c in blink::PeerConnectionDependencyFactory::CreatePeerConnectionFactory()+0x450 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0x21ea26c)
    #4 0x1712c5d2c in blink::PeerConnectionDependencyFactory::GetPcFactory()+0xd4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0x21e9d2c)
    #5 0x1712cd8f8 in blink::PeerConnectionDependencyFactory::CreatePeerConnection(webrtc::PeerConnectionInterface::RTCConfiguration const&, blink::WebLocalFrame*, webrtc::PeerConnectionObserver*, blink::ExceptionState&)+0x138 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0x21f18f8)
    #6 0x17138e788 in blink::RTCPeerConnectionHandler::Initialize(blink::ExecutionContext*, webrtc::PeerConnectionInterface::RTCConfiguration const&, blink::WebLocalFrame*, blink::ExceptionState&)+0x51c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0x22b2788)
    #7 0x171352114 in blink::RTCPeerConnection::RTCPeerConnection(blink::ExecutionContext*, webrtc::PeerConnectionInterface::RTCConfiguration, bool, blink::ExceptionState&)+0x8f4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0x2276114)
    #8 0x1713516bc in blink::RTCPeerConnection* blink::MakeGarbageCollected<blink::RTCPeerConnection, blink::ExecutionContext*&, webrtc::PeerConnectionInterface::RTCConfiguration, bool, blink::ExceptionState&>(blink::ExecutionContext*&, webrtc::PeerConnectionInterface::RTCConfiguration&&, bool&&, blink::ExceptionState&)+0x160 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0x22756bc)
    #9 0x17134e39c in blink::RTCPeerConnection::Create(blink::ExecutionContext*, blink::RTCConfiguration const*, blink::ExceptionState&)+0x580 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0x227239c)
    #10 0x16fe8eaa0 in blink::(anonymous namespace)::v8_rtc_peer_connection::ConstructorCallback(v8::FunctionCallbackInfo<v8::Value> const&)+0x6bc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0xdb2aa0)
    #11 0x14858b488 in v8::internal::FunctionCallbackArguments::CallOrConstruct(v8::internal::Tagged<v8::internal::FunctionTemplateInfo>, bool)+0x4e4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libv8.dylib:arm64+0x32b488)
    #12 0x1485899e4 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<true>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, unsigned long*, int)+0x408 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libv8.dylib:arm64+0x3299e4)
    #13 0x148588248 in v8::internal::Builtin_Impl_HandleApiConstruct(v8::internal::BuiltinArguments, v8::internal::Isolate*)+0x184 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libv8.dylib:arm64+0x328248)
    #14 0x7ede87ea8190  (<unknown module>)
    #15 0x7ede87e0e268  (<unknown module>)
    #16 0x7ede87f90494  (<unknown module>)
    #17 0x7ede87e0d3fc  (<unknown module>)
    #18 0x7ede87e0d3fc  (<unknown module>)
    #19 0x7ede87e0d3fc  (<unknown module>)
    #20 0x7ede87f1b678  (<unknown module>)
    #21 0x7ede87e0e268  (<unknown module>)
    #22 0x7ede87f90494  (<unknown module>)
    #23 0x7ede87e0d3fc  (<unknown module>)
    #24 0x7ede87f1db94  (<unknown module>)
    #25 0x7ede87e3b5dc  (<unknown module>)
    #26 0x7ede87e0aef0  (<unknown module>)
    #27 0x14888b6d0 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&)+0x1744 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libv8.dylib:arm64+0x62b6d0)
    #28 0x14888d8dc in v8::internal::(anonymous namespace)::InvokeWithTryCatch(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&)+0x118 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libv8.dylib:arm64+0x62d8dc)
    #29 0x14888dc68 in v8::internal::Execution::TryRunMicrotasks(v8::internal::Isolate*, v8::internal::MicrotaskQueue*)+0x38 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libv8.dylib:arm64+0x62dc68)
    #30 0x14891b17c in v8::internal::MicrotaskQueue::RunMicrotasks(v8::internal::Isolate*)+0x3b4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libv8.dylib:arm64+0x6bb17c)
    #31 0x14891ad20 in v8::internal::MicrotaskQueue::PerformCheckpointInternal(v8::Isolate*)+0x118 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libv8.dylib:arm64+0x6bad20)
    #32 0x1484e9ea0 in v8::MicrotasksScope::~MicrotasksScope()+0x13c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libv8.dylib:arm64+0x289ea0)
    #33 0x158b34f8c in blink::V8ScriptRunner::RunCompiledScript(v8::Isolate*, v8::Local<v8::Script>, v8::Local<v8::Data>, blink::ExecutionContext*)+0x600 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_core.dylib:arm64+0x174f8c)
    #34 0x158b36178 in blink::V8ScriptRunner::CompileAndRunScript(blink::ScriptState*, blink::ClassicScript*, blink::ExecuteScriptPolicy, blink::V8ScriptRunner::RethrowErrorsOption)+0x8b0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_core.dylib:arm64+0x176178)
    #35 0x15b56cd08 in blink::ClassicScript::RunScriptOnScriptStateAndReturnValue(blink::ScriptState*, blink::ExecuteScriptPolicy, blink::V8ScriptRunner::RethrowErrorsOption)+0x19c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_core.dylib:arm64+0x2bacd08)
    #36 0x15b5bb7b0 in blink::Script::RunScriptOnScriptState(blink::ScriptState*, blink::ExecuteScriptPolicy, blink::V8ScriptRunner::RethrowErrorsOption)+0x1b4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_core.dylib:arm64+0x2bfb7b0)
    #37 0x15b5bbac0 in blink::Script::RunScript(blink::LocalDOMWindow*, blink::ExecuteScriptPolicy, blink::V8ScriptRunner::RethrowErrorsOption)+0x140 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_core.dylib:arm64+0x2bfbac0)
    #38 0x15b5bad10 in blink::PendingScript::ExecuteScriptBlockInternal(blink::Script*, blink::ScriptElementBase*, bool, bool, bool, base::TimeTicks, bool)+0x3ec (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_core.dylib:arm64+0x2bfad10)
    #39 0x15b5b9c6c in blink::PendingScript::ExecuteScriptBlock()+0x560 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_core.dylib:arm64+0x2bf9c6c)
    #40 0x15b5bf324 in blink::ScriptLoader::PrepareScript(blink::ScriptLoader::ParserBlockingInlineOption, WTF::TextPosition const&)+0x2588 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_core.dylib:arm64+0x2bff324)
    #41 0x15b57d724 in blink::HTMLParserScriptRunner::ProcessScriptElementInternal(blink::Element*, WTF::TextPosition const&)+0x410 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_core.dylib:arm64+0x2bbd724)
    #42 0x15b57d058 in blink::HTMLParserScriptRunner::ProcessScriptElement(blink::Element*, WTF::TextPosition const&)+0xac (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_core.dylib:arm64+0x2bbd058)
    #43 0x15beb6cd4 in blink::HTMLDocumentParser::RunScriptsForPausedTreeBuilder()+0x1a4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_core.dylib:arm64+0x34f6cd4)
    #44 0x15beb3700 in blink::HTMLDocumentParser::PumpTokenizer()+0x708 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_core.dylib:arm64+0x34f3700)
    #45 0x15beb1e80 in blink::HTMLDocumentParser::PumpTokenizerIfPossible()+0x34c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_core.dylib:arm64+0x34f1e80)
    #46 0x15beb27c4 in blink::HTMLDocumentParser::DeferredPumpTokenizerIfPossible(bool, base::TimeTicks)+0x2bc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_core.dylib:arm64+0x34f27c4)
    #47 0x15becc95c in base::internal::Invoker<base::internal::FunctorTraits<void (blink::HTMLDocumentParser::*&&)(bool, base::TimeTicks), cppgc::internal::BasicPersistent<blink::HTMLDocumentParser, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>&&, bool&&, base::TimeTicks&&>, base::internal::BindState<true, true, false, void (blink::HTMLDocumentParser::*)(bool, base::TimeTicks), cppgc::internal::BasicPersistent<blink::HTMLDocumentParser, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, bool, base::TimeTicks>, void ()>::RunOnce(base::internal::BindStateBase*)+0x150 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_core.dylib:arm64+0x350c95c)
    #48 0x103846708 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x34c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x1ae708)
    #49 0x1038b2c64 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x7f0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x21ac64)
    #50 0x1038b20d8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x21a0d8)
    #51 0x1037219f4 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x1b0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x899f4)
    #52 0x1038b4210 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x3cc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x21c210)
    #53 0x1037cef4c in base::RunLoop::Run(base::Location const&)+0x434 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libbase.dylib:arm64+0x136f4c)
    #54 0x131da8ae0 in content::RendererMain(content::MainFunctionParams)+0x6e8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libcontent.dylib:arm64+0x30c4ae0)
    #55 0x131f82e20 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x3f8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libcontent.dylib:arm64+0x329ee20)
    #56 0x131f84b74 in content::ContentMainRunnerImpl::Run()+0x434 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libcontent.dylib:arm64+0x32a0b74)
    #57 0x131f80c38 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x5b4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libcontent.dylib:arm64+0x329cc38)
    #58 0x131f814f8 in content::ContentMain(content::ContentMainParams)+0x190 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libcontent.dylib:arm64+0x329d4f8)
    #59 0x1180bee58 in ChromeMain+0x370 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libchrome_dll.dylib:arm64+0xae58)
    #60 0x100d24ce4 in main+0x254 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/129.0.6627.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer):arm64+0x100000ce4)
    #61 0x19bd5b150  (<unknown module>)
    #62 0x5d137ffffffffffc  (<unknown module>)

SUMMARY: AddressSanitizer: heap-use-after-free (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x7d1fec) in webrtc::(anonymous namespace)::VSyncEncodeAdapterMode::EncodeAllEnqueuedFrames()+0x970
Shadow bytes around the buggy address:
  0x611001b28800: fa fa fa fa fa fa f7 fa 00 00 00 00 00 00 00 00
  0x611001b28880: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x611001b28900: 00 00 00 00 00 00 fa fa fa fa fa fa fa fa f7 fa
  0x611001b28980: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x611001b28a00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 fa fa
=>0x611001b28a80: fa fa fa fa fa fa f7 fa[fd]fd fd fd fd fd fd fd
  0x611001b28b00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x611001b28b80: fd fd fd fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x611001b28c00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x611001b28c80: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa
  0x611001b28d00: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
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

==62534==ADDITIONAL INFO

==62534==Note: Please include this section with the ASan report.
Task trace:
    #0 0x114744ba4 in webrtc::(anonymous namespace)::VSyncEncodeAdapterMode::OnFrame(webrtc::Timestamp, bool, webrtc::VideoFrame const&)+0x258 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x7d0ba4)
    #1 0x114738d18 in webrtc::(anonymous namespace)::FrameCadenceAdapterImpl::OnFrame(webrtc::VideoFrame const&)+0x2c4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x7c4d18)
    #2 0x1712bc284 in blink::MediaStreamVideoWebRtcSink::WebRtcVideoSourceAdapter::OnVideoFrameOnIO(scoped_refptr<media::VideoFrame>, base::TimeTicks)+0x130 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0x21e0284)
    #3 0x170e155c8 in blink::CanvasCaptureHandler::SendFrame(base::TimeTicks, gfx::ColorSpace const&, scoped_refptr<media::VideoFrame>)+0x33c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/libblink_modules.dylib:arm64+0x1d395c8)


Command line: `/Users/zh1x1an1221/xcode-chromium/src/out/asan-0730/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/129.0.6627.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer) --type=renderer --user-data-dir=/tmp/userdata/t1 --no-subproc-heap-profiling --no-sandbox --lang=zh-CN --num-raster-threads=4 --enable-zero-copy --enable-gpu-memory-buffer-compositor-resources --enable-main-frame-before-activation --renderer-client-id=19 --time-ticks-at-unix-epoch=-1722416918773237 --launch-time-ticks=446797497971 --shared-files --metrics-shmem-handle=1752395122,r,17474507040910173048,11118684217549666121,2097152 --field-trial-handle=1718379636,r,18119731364420737652,13075120152529407137,262144 --enable-features=PMLoadingPageVoter,VSyncDecoding,VSyncEncoding,WebRtcThreadsUseResourceEfficientType,WebRtcUseCaptureBeginTimestamp,WebRtcUseMinMaxVEADimensions --variations-seed-version`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==62534==END OF ADDITIONAL INFO
==62534==ABORTING
Received signal 6
 [0x0001039de840]
 [0x00010399b19c]
 [0x0001039de348]
 [0x00019c116584]
 [0x00019c0e5c20]
 [0x00019bff2a30]
 [0x000101c7aa0c]
 [0x000101c7a04c]
 [0x000101c5d388]
 [0x000101c5c648]
 [0x000101c5db5c]
 [0x000114745ff0]
 [0x0001147450f8]
 [0x000171e67ff0]
 [0x000171e6abc8]
 [0x000171e6a9b0]
 [0x00010384670c]
 [0x0001038b2c68]
 [0x0001038b20dc]
 [0x0001037219f8]
 [0x0001038b4214]
 [0x0001037cef50]
 [0x000103944aa8]
 [0x000103944f10]
 [0x000103999350]
 [0x000101c51d1c]
 [0x00019c0e5f94]
 [0x00019c0e0d34]
[end of stack trace]

```

**Just search for the address 0x611001b28ac0**

### pe...@google.com (2024-08-05)

The NextAction date has arrived: 2024-08-05
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### kr...@google.com (2024-08-05)

Great work analyzing the bug! Setting to S2 as it requires a non standard flag.

handellm@ can you take a look as you approve the change introducing this?

### pe...@google.com (2024-08-06)

Setting milestone because of s2 severity.

### pe...@google.com (2024-08-06)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ha...@google.com (2024-08-06)

Unfortunately I wasn't able to reproduce 100% reliably using the instructions. It only triggers like 1 in 10 tries, so I'm not sure I can use the repro to verify the problem is gone unless it's refined somehow.

Anyway, a sequence triggering it is per below

1. FrameCadenceAdapter (FCA) is configured with Metronome with >= 34 ms tick delay.
2. A frame is queued for processing on worker queue.
3. The FCA is destroyed. The contained VSyncEncodeAdapterMode instance is scheduled for deletion on worker queue.
4. Encode queue is destroyed.
5. Worker queue is executed, which runs a task that dereferences `queue_`.

I managed to write a unit test for this + a fix: <https://webrtc-review.googlesource.com/c/src/+/358660>, I'm now awaiting reviewer feedback.

### kr...@google.com (2024-08-06)

Thank you, that is really nice work!

### zh...@gmail.com (2024-08-07)

> Unfortunately I wasn't able to reproduce 100% reliably using the instructions. It only triggers like 1 in 10 tries, so I'm not sure I can use the repro to verify the problem is gone unless it's refined somehow.

It doesn't matter. If you don't mind, I can help you test the fix of the vulnerability. As I said, the POC may be related to the configuration of different devices, so my POC can only guarantee 100% triggering under the premise of confirming the device configuration.

### zh...@gmail.com (2024-08-07)

There is no problem with fixing the commit in my test, as shown below:

```
git checkout 1e2a3dd9e56b736fe6808e325d3fcfca1e33b533
cd third_party/webrtc
git apply debug_fix.diff

```

Repeat the previous operation that stably triggered the vulnerability (in my environment)

Detailed execution results are in the `debug_fix_result.txt` file

### ha...@google.com (2024-08-07)

Thanks, @zh1x1an1221 - can you please recheck with the latest patchset uploaded in the CL? The scope of the mutex lock was reduced.

### ha...@google.com (2024-08-08)

Landed the CL in the meantime.

### ap...@google.com (2024-08-08)

Project: src
Branch: main

commit e864dec2e98bb0786c015aabc712cf978b5e3634
Author: Markus Handell <handellm@webrtc.org>
Date:   Wed Aug 07 14:11:18 2024

    VSyncEncodeAdapterMode: avoid UAF.
    
    This CL fixes a problem where VSEAM's `queue_` was dereferenced
    post destruction. A sequence triggering it is:
    
    0. FrameCadenceAdapter (FCA) is configured with Metronome with >= 34 ms tick delay.
    1. A frame is queued for processing on worker queue.
    2. The FCA is destroyed. The contained VSyncEncodeAdapterMode instance is scheduled for deletion on worker queue.
    3. Encode queue is destroyed.
    4. Worker queue is executed, which runs a task that dereferences `queue_`.
    
    Bug: chromium:356423094
    Change-Id: Iae8dc070304ef5ec0cfb0b4f27bbb7fe86e7def7
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/358660
    Commit-Queue: Markus Handell <handellm@webrtc.org>
    Reviewed-by: Danil Chapovalov <danilchap@webrtc.org>
    Reviewed-by: Ilya Nikolaevskiy <ilnik@webrtc.org>
    Cr-Commit-Position: refs/heads/main@{#42745}

M       video/frame_cadence_adapter.cc
M       video/frame_cadence_adapter_unittest.cc

https://webrtc-review.googlesource.com/358660


### ap...@google.com (2024-08-08)

Project: chromium/src
Branch: main

commit 0394cd2ed0a3475bab9a60c6fbc839455bdff476
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date:   Thu Aug 08 13:23:27 2024

    Roll WebRTC from c7e25684573d to e864dec2e98b (4 revisions)
    
    https://webrtc.googlesource.com/src.git/+log/c7e25684573d..e864dec2e98b
    
    2024-08-08 handellm@webrtc.org VSyncEncodeAdapterMode: avoid UAF.
    2024-08-08 mbonadei@webrtc.org Roll chromium_revision ba1ae79f58..6f9b3224db (1319128:1338914)
    2024-08-08 webrtc-version-updater@webrtc-ci.iam.gserviceaccount.com Update WebRTC code version (2024-08-08T04:02:48).
    2024-08-07 dorhen@meta.com Apply include-cleaner to api/transport
    
    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/webrtc-chromium-autoroll
    Please CC webrtc-chromium-sheriffs-robots@google.com,webrtc-infra@google.com on the revert to ensure that a human
    is aware of the problem.
    
    To file a bug in WebRTC: https://bugs.chromium.org/p/webrtc/issues/entry
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry
    
    To report a problem with the AutoRoller itself, please file a bug:
    https://issues.skia.org/issues/new?component=1389291&template=1850622
    
    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md
    
    Bug: chromium:356423094
    Tbr: webrtc-chromium-sheriffs-robots@google.com
    Change-Id: I5e40993d49b5a5b3dd8610a1c7c3003402a04b4f
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5772957
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#1339024}

M       DEPS
M       third_party/webrtc

https://chromium-review.googlesource.com/5772957


### zh...@gmail.com (2024-08-08)

> Thanks, @zh1x1an1221 - can you please recheck with the latest patchset uploaded in the CL? The scope of the mutex lock was reduced.

OK, sorry I was on vacation.

After testing this patch, I don't see any issues for now.

```
git checkout 1e2a3dd9e56b736fe6808e325d3fcfca1e33b533
cd third_party/webrtc
git apply debug_fix.diff

```

### pe...@google.com (2024-08-08)

Requesting merge to beta (M128) because latest trunk commit (1339024) appears to be after beta branch point (1331488).
Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [128].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### ha...@google.com (2024-08-08)

I'm not sure backports are needed - this feature is not experimented with in the field yet, and needs a command-line flag to get enabled.

### sp...@google.com (2024-08-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
$7,000 for report of memory corruption in a sandboxed process + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-08-22)

Congratulations, zh1x1an1221! Thanks for your efforts and reporting this issue to us -- nice work!

### zh...@gmail.com (2024-08-22)

Thanks, Amy, this is a good experience for me, I looked very hard about this module about half a year ago, but found nothing at that time. Cheers 🍻

### pe...@google.com (2024-11-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/356423094)*
