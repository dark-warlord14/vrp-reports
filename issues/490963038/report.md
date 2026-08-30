# Missing validation of linear timing function point count in Viz process DeserializeTimingFunction leads to OOB read in GPU process

| Field | Value |
|-------|-------|
| **Issue ID** | [490963038](https://issues.chromium.org/issues/490963038) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Services>Viz |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | zm...@chromium.org |
| **Created** | 2026-03-09 |
| **Bounty** | $3,000.00 |

## Description

## Summary

The GPU process deserializes linear timing functions from renderer-supplied Mojo messages without enforcing a minimum point count. A compromised renderer can send a single-point linear easing array through the LayerContext.UpdateDisplayTree interface, causing LinearTimingFunction::GetValue to perform an iterator underflow via std::prev(cbegin()) and read out of bounds from the heap. The vulnerability affects all platforms when the kTreeAnimationsInViz feature is enabled. No special GPU is required.

## Bisect

The vulnerable DeserializeTimingFunction was introduced in the initial animation synchronization commit for VizLayers. The linear branch accepted any non-empty array of easing points without enforcing a minimum size of two, relying solely on a downstream DCHECK in LinearTimingFunction::Create.

Introducing Commit: `63a3937d6059cfad7f4fa91192d1a9726cc80d1c`

- Date: Thu Sep 26 21:50:54 2024
- Author: Ken Rockot
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/5875659>

## Root Cause

When the GPU process receives animation data from the renderer, it reconstructs timing functions through DeserializeTimingFunction in layer\_context\_impl.cc. The linear branch handles the incoming array of easing points:

```
// components/viz/service/layers/layer_context_impl.cc
case mojom::TimingFunction::Tag::kLinear: {
  const auto& wire_points = wire.get_linear();
  std::vector<gfx::LinearEasingPoint> points;
  points.reserve(wire_points.size());
  for (const auto& wire_point : wire_points) {
    points.emplace_back(wire_point->in, wire_point->out);
  }
  if (points.empty()) {
    return gfx::LinearTimingFunction::Create();
  }
  return gfx::LinearTimingFunction::Create(std::move(points));
}

```

This code correctly handles the empty case by creating a trivial linear function, but it does not reject arrays with fewer than two points. The downstream factory method relies solely on a DCHECK to enforce the minimum:

```
// ui/gfx/animation/keyframe/timing_function.cc
std::unique_ptr<LinearTimingFunction> LinearTimingFunction::Create(
    std::vector<LinearEasingPoint> points) {
  DCHECK(points.size() >= 2);
  return base::WrapUnique(new LinearTimingFunction(std::move(points)));
}

```

Since DCHECK is stripped in Release builds, a single-element vector passes through without any check.

The Mojo definition for the linear variant is `array<LinearEasingPoint>` with no minimum size constraint, so the Mojo deserialization layer does not reject undersized arrays either.

When the animation system later evaluates the timing function, GetValue enters its non-trivial path because IsTrivial() returns false for a non-empty points vector. The algorithm locates the insertion point via std::upper\_bound, then attempts to find a pair of adjacent points. With only one point in the vector, the logic reaches a state where `point_a` equals `cbegin()` and `std::next(point_a)` equals `cend()`:

```
// ui/gfx/animation/keyframe/timing_function.cc
point_a = std::next(point_a) == points_.cend() ? std::prev(point_a) : point_a;

```

This conditional evaluates to true, executing std::prev(point\_a) where point\_a is already cbegin(). The result is an iterator pointing 16 bytes before the start of the vector's heap buffer (one LinearEasingPoint of two doubles). The subsequent code dereferences this underflowed iterator:

```
const auto& point_b = std::next(point_a);
if (point_a->input == point_b->input) {
    return point_b->output;
}
const double progress_from_point_a = input_progress - point_a->input / 100;

```

Each access to point\_a->input and point\_a->output reads 8 bytes from the heap region preceding the vector buffer, constituting an out-of-bounds read.

Chromium enables \_LIBCPP\_HARDENING\_MODE\_EXTENSIVE for libc++ containers, which provides bounds checking on operator[] and at(). However, vector iterator arithmetic through \_\_wrap\_iter does not carry bounds metadata; the \_LIBCPP\_ABI\_BOUNDED\_ITERATORS\_IN\_VECTOR macro that would enable checked iterators for std::vector is commented out in the libc++ configuration. Consequently, the std::prev(cbegin()) operation and the subsequent dereference proceed without any runtime check.

## Reproduce

This reproducer uses MojoJS to send a crafted single-point linear timing function directly to the GPU process via the LayerContext.UpdateDisplayTree interface, simulating a compromised renderer. No source patches are required.

Tested on Chromium commit `770da727191cd5ba2f552fc88a1e9a7ea4ec1f1a`, macOS. The ASAN build directory should be configured with the following args.gn:

```
is_asan = true
is_debug = false
dcheck_always_on = false

```

Place the `poc.html` and `copy_mojo_js_bindings.py` in the same directory(such as `poc_mojo`) and start a local HTTP server:

```
cd poc_mojo/
python3 copy_mojo_js_bindings.py /path/to/out/asan/gen
python3 -m http.server 8000

```

Launch Chrome:

```
./out/asan/Chromium.app/Contents/MacOS/Chromium --enable-blink-features=MojoJS,MojoJSTest --enable-features=kTreeAnimationsInViz --user-data-dir=./userdata http://127.0.0.1:8000/poc.html

```

ASAN output:

```
=================================================================
==21702==ERROR: AddressSanitizer: use-after-poison on address 0x60200009aaa0 at pc 0x000362e5dce4 bp 0x000173e60320 sp 0x000173e60318
READ of size 8 at 0x60200009aaa0 thread T15
==21702==WARNING: invalid path to external symbolizer!
==21702==WARNING: Failed to use and restart external symbolizer!
    #0 0x000362e5dce0 in gfx::LinearTimingFunction::GetValue(double, gfx::TimingFunction::LimitDirection) const+0x194 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x19391ce0)
    #1 0x000362e4c140 in gfx::KeyframedFloatAnimationCurve::GetTransformedValue(base::TimeDelta, gfx::TimingFunction::LimitDirection) const+0x3d8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x19380140)
    #2 0x000362e46dc8 in gfx::FloatAnimationCurve::Tick(base::TimeDelta, int, gfx::KeyframeModel*, gfx::TimingFunction::LimitDirection) const+0x134 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1937adc8)
    #3 0x000362e6263c in gfx::KeyframeEffect::TickKeyframeModel(base::TimeTicks, gfx::KeyframeModel*)+0x184 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1939663c)
    #4 0x000362e78670 in cc::KeyframeEffect::Tick(base::TimeTicks)+0xe0 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x193ac670)
    #5 0x000362e717d0 in cc::AnimationTimeline::TickTimeLinkedAnimations(std::__Cr::vector<scoped_refptr<cc::Animation>, std::__Cr::allocator<scoped_refptr<cc::Animation>>> const&, base::TimeTicks, bool)+0x1f4 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x193a57d0)
    #6 0x000362e98788 in cc::AnimationHost::TickAnimations(base::TimeTicks, cc::ScrollTree const&, bool, cc::MutatorEvents*)+0x320 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x193cc788)
    #7 0x0003606e4940 in cc::LayerTreeHostImpl::AnimateLayers(base::TimeTicks, bool)+0xa4 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x16c18940)
    #8 0x0003606be438 in cc::LayerTreeHostImpl::AnimateInternal()+0xe8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x16bf2438)
    #9 0x0003606d6db8 in cc::LayerTreeHostImpl::WillBeginImplFrame(viz::BeginFrameArgs const&)+0x56c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x16c0adb8)
    #10 0x000365573f94 in viz::LayerContextImpl::DoDrawInternal(viz::BeginFrameArgs const&, base::TimeTicks, std::__Cr::optional<bool>)+0x274 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1baa7f94)
    #11 0x000365346ff8 in viz::CompositorFrameSinkSupport::OnBeginFrame(viz::BeginFrameArgs const&)+0x860 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1b87aff8)
    #12 0x0003607acd10 in viz::ExternalBeginFrameSource::AddObserver(viz::BeginFrameObserver*)+0x2e0 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x16ce0d10)
    #13 0x0003606bb5e8 in cc::LayerTreeHostImpl::ActivateAnimations()+0x144 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x16bef5e8)
    #14 0x00036557f450 in viz::LayerContextImpl::DoUpdateDisplayTree(mojo::StructPtr<viz::mojom::LayerTreeUpdate>)+0x89a4 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1bab3450)
    #15 0x0003655765a4 in viz::LayerContextImpl::UpdateDisplayTree(mojo::StructPtr<viz::mojom::LayerTreeUpdate>)+0x1ac (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1baaa5a4)
    #16 0x00034d20e438 in viz::mojom::LayerContextStubDispatch::Accept(viz::mojom::LayerContext*, mojo::Message*)+0x1fc (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x3742438)
    #17 0x00035bcf7c6c in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*)+0x8fc (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1222bc6c)
    #18 0x00035bd0ca9c in mojo::MessageDispatcher::Accept(mojo::Message*)+0x2f0 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x12240a9c)
    #19 0x00035bcfce6c in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*)+0x148 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x12230e6c)
    #20 0x00035bd19c20 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*)+0x650 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1224dc20)
    #21 0x00035bd186dc in mojo::internal::MultiplexRouter::Accept(mojo::Message*)+0x558 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1224c6dc)
    #22 0x00035bd0ca9c in mojo::MessageDispatcher::Accept(mojo::Message*)+0x2f0 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x12240a9c)
    #23 0x00035bceae3c in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>)+0x394 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1221ee3c)
    #24 0x00035bcec300 in mojo::Connector::ReadAllAvailableMessages()+0x234 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x12220300)
    #25 0x00035bcebe08 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int)+0xe8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1221fe08)
    #26 0x00035bced8e8 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int)+0x1b8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x122218e8)
    #27 0x00034d44e440 in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const &+0x148 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x3982440)
    #28 0x00034d44e21c in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&)+0xf0 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x398221c)
    #29 0x00035c4d1d04 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const &+0x154 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x12a05d04)
    #30 0x00035c4d1720 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&)+0x398 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x12a05720)
    #31 0x00035c4d2660 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase*)+0x184 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x12a06660)
    #32 0x00035beea8a4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1241e8a4)
    #33 0x00035bf5290c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x88c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1248690c)
    #34 0x00035bf51cc4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x12485cc4)
    #35 0x00035c073330 in base::MessagePumpCFRunLoopBase::RunWork()+0x1c8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x125a7330)
    #36 0x00035c0649e0 in base::apple::CallWithEHFrame(void () block_pointer)+0xc (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x125989e0)
    #37 0x00035c071798 in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0xe4 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x125a5798)
    #38 0x00019b3549f4 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5f9f4)
    #39 0x00019b354988 in __CFRunLoopDoSource0+0xa8 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5f988)
    #40 0x00019b3546f4 in __CFRunLoopDoSources0+0xe4 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5f6f4)
    #41 0x00019b353384 in __CFRunLoopRun+0x330 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5e384)
    #42 0x00019b40de30 in _CFRunLoopRunSpecificWithOptions+0x210 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x118e30)
    #43 0x00019d5a2960 in -[NSRunLoop(NSRunLoop) runMode:beforeDate:]+0xd0 (/System/Library/Frameworks/Foundation.framework/Versions/C/Foundation:arm64e+0xa5b960)
    #44 0x00035c07448c in base::MessagePumpNSRunLoop::DoRun(base::MessagePump::Delegate*)+0xc8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x125a848c)
    #45 0x00035c070500 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x290 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x125a4500)
    #46 0x00035bf53c6c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x32c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x12487c6c)
    #47 0x00035be7885c in base::RunLoop::Run(base::Location const&)+0x430 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x123ac85c)
    #48 0x00035bfc8e78 in base::Thread::Run(base::RunLoop*)+0xd8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x124fce78)
    #49 0x00035bfc92d0 in base::Thread::ThreadMain()+0x3d8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x124fd2d0)
    #50 0x00035c0200ac in base::(anonymous namespace)::ThreadFunc(void*)+0x154 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x125540ac)
    #51 0x0001025c9870 in __sanitizer_weak_hook_memcmp+0x36750 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Helpers/Chromium Helper.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x51870)
    #52 0x00019b2b5c04 in _pthread_start+0x84 (/usr/lib/system/libsystem_pthread.dylib:arm64e+0x6c04)
    #53 0x00019b2b0ba4 in thread_start+0x4 (/usr/lib/system/libsystem_pthread.dylib:arm64e+0x1ba4)

0x60200009aaa0 is located 8 bytes after 8-byte region [0x60200009aa90,0x60200009aa98)
allocated by thread T15 here:
    #0 0x0001025ccf84 in __asan_memmove+0x2f9c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Helpers/Chromium Helper.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x54f84)
    #1 0x0003724bf98c in operator new(unsigned long)+0x18 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x289f398c)
    #2 0x00034a7845b8 in base::internal::UncheckedObserverAdapter<(partition_alloc::internal::RawPtrTraits)0, false>* std::__Cr::vector<base::internal::UncheckedObserverAdapter<(partition_alloc::internal::RawPtrTraits)0, false>, std::__Cr::allocator<base::internal::UncheckedObserverAdapter<(partition_alloc::internal::RawPtrTraits)0, false>>>::__emplace_back_slow_path<base::internal::UncheckedObserverAdapter<(partition_alloc::internal::RawPtrTraits)0, false>>(base::internal::UncheckedObserverAdapter<(partition_alloc::internal::RawPtrTraits)0, false>&&)+0xb8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0xcb85b8)
    #3 0x000362e65128 in base::ObserverList<cc::KeyframeEffect, false, (base::ObserverListReentrancyPolicy)1, base::internal::UncheckedObserverAdapter<(partition_alloc::internal::RawPtrTraits)0, false>>::AddObserver(cc::KeyframeEffect*)+0x320 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x19399128)
    #4 0x000362e64df0 in cc::ElementAnimations::AddKeyframeEffect(cc::KeyframeEffect*)+0x18 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x19398df0)
    #5 0x000362e92920 in cc::AnimationHost::RegisterAnimationForElement(cc::ElementId, cc::Animation*)+0x3c0 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x193c6920)
    #6 0x0003655848f8 in viz::(anonymous namespace)::DeserializeAnimationUpdates(viz::mojom::LayerTreeUpdate const&, cc::AnimationHost&)+0x7c8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1bab88f8)
    #7 0x00036557f414 in viz::LayerContextImpl::DoUpdateDisplayTree(mojo::StructPtr<viz::mojom::LayerTreeUpdate>)+0x8968 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1bab3414)
    #8 0x0003655765a4 in viz::LayerContextImpl::UpdateDisplayTree(mojo::StructPtr<viz::mojom::LayerTreeUpdate>)+0x1ac (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1baaa5a4)
    #9 0x00034d20e438 in viz::mojom::LayerContextStubDispatch::Accept(viz::mojom::LayerContext*, mojo::Message*)+0x1fc (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x3742438)
    #10 0x00035bcf7c6c in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*)+0x8fc (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1222bc6c)
    #11 0x00035bd0ca9c in mojo::MessageDispatcher::Accept(mojo::Message*)+0x2f0 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x12240a9c)
    #12 0x00035bcfce6c in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*)+0x148 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x12230e6c)
    #13 0x00035bd19c20 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*)+0x650 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1224dc20)
    #14 0x00035bd186dc in mojo::internal::MultiplexRouter::Accept(mojo::Message*)+0x558 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1224c6dc)
    #15 0x00035bd0ca9c in mojo::MessageDispatcher::Accept(mojo::Message*)+0x2f0 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x12240a9c)
    #16 0x00035bceae3c in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>)+0x394 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1221ee3c)
    #17 0x00035bcec300 in mojo::Connector::ReadAllAvailableMessages()+0x234 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x12220300)
    #18 0x00035bcebe08 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int)+0xe8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1221fe08)
    #19 0x00035bced8e8 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int)+0x1b8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x122218e8)
    #20 0x00034d44e440 in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const &+0x148 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x3982440)
    #21 0x00034d44e21c in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&)+0xf0 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x398221c)
    #22 0x00035c4d1d04 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const &+0x154 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x12a05d04)
    #23 0x00035c4d1720 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&)+0x398 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x12a05720)
    #24 0x00035c4d2660 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase*)+0x184 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x12a06660)
    #25 0x00035beea8a4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1241e8a4)
    #26 0x00035bf5290c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x88c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1248690c)
    #27 0x00035bf51cc4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x12485cc4)
    #28 0x00035c073330 in base::MessagePumpCFRunLoopBase::RunWork()+0x1c8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x125a7330)
    #29 0x00035c0649e0 in base::apple::CallWithEHFrame(void () block_pointer)+0xc (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x125989e0)

Thread T15 created by T0 here:
    #0 0x0001025c395c in __sanitizer_weak_hook_memcmp+0x3083c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Helpers/Chromium Helper.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x4b95c)
    #1 0x00035c01f670 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType)+0x26c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x12553670)
    #2 0x00035bfc81b0 in base::Thread::StartWithOptions(base::Thread::Options)+0x498 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x124fc1b0)
    #3 0x0003555621d8 in viz::VizCompositorThreadRunnerImpl::VizCompositorThreadRunnerImpl()+0x228 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0xba961d8)
    #4 0x000355567934 in viz::VizMainImpl::VizMainImpl(viz::VizMainImpl::Delegate*, viz::VizMainImpl::ExternalDependencies, std::__Cr::unique_ptr<gpu::GpuInit, std::__Cr::default_delete<gpu::GpuInit>>)+0x7c8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0xba9b934)
    #5 0x00036523941c in content::GpuChildThread::GpuChildThread(base::RepeatingCallback<void ()>, content::ChildThreadImpl::Options, std::__Cr::unique_ptr<gpu::GpuInit, std::__Cr::default_delete<gpu::GpuInit>>)+0x1c0 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1b76d41c)
    #6 0x0003652391a0 in content::GpuChildThread::GpuChildThread(base::RepeatingCallback<void ()>, std::__Cr::unique_ptr<gpu::GpuInit, std::__Cr::default_delete<gpu::GpuInit>>)+0x184 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1b76d1a0)
    #7 0x00036523c3ec in content::GpuMain(content::MainFunctionParams)+0x788 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1b7703ec)
    #8 0x0003585cbdd0 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x420 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0xeaffdd0)
    #9 0x0003585cdf50 in content::ContentMainRunnerImpl::Run()+0x53c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0xeb01f50)
    #10 0x0003585c9ac0 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x858 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0xeafdac0)
    #11 0x0003585c9fb0 in content::ContentMain(content::ContentMainParams)+0x190 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0xeafdfb0)
    #12 0x000349ad1cb4 in ChromeMain+0x490 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x5cb4)
    #13 0x00010219cc94 in main+0x254 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Helpers/Chromium Helper.app/Contents/MacOS/Chromium Helper:arm64+0x100000c94)
    #14 0x00019aeedd50 in start+0x1c0c (/usr/lib/dyld:arm64e+0x8d50)

SUMMARY: AddressSanitizer: use-after-poison (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x19391ce0) in gfx::LinearTimingFunction::GetValue(double, gfx::TimingFunction::LimitDirection) const+0x194
Shadow bytes around the buggy address:
  0x60200009a800: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa fd fa
  0x60200009a880: f7 fa 00 fa f7 fa 00 fa f7 fa fd fa f7 fa 00 fa
  0x60200009a900: f7 fa 00 00 f7 fa 00 00 f7 fa 00 00 f7 fa 00 00
  0x60200009a980: f7 fa 00 fa f7 fa 00 fa f7 fa 00 fa f7 fa 00 00
  0x60200009aa00: f7 fa 00 fa f7 fa fd fd f7 fa 00 00 f7 fa 00 00
=>0x60200009aa80: f7 fa 00 fa[f7]fa 00 00 f7 fa fd fa f7 fa 00 00
  0x60200009ab00: f7 fa 00 fa f7 fa 00 fa f7 fa fd fd f7 fa fd fd
  0x60200009ab80: f7 fa fd fa f7 fa fd fa fa fa fa fa fa fa fa fa
  0x60200009ac00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x60200009ac80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x60200009ad00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

NOTE: the stack trace above identifies the code that *accessed* the poisoned memory.
To identify the code that *poisoned* the memory, try the experimental setting ASAN_OPTIONS=poison_history_size=<size>.

==21702==ADDITIONAL INFO

==21702==Note: Please include this section with the ASan report.
Task trace:
    #0 0x00035c4d209c in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int)+0x230 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x12a0609c)

==21702==END OF ADDITIONAL INFO

==21702==ABORTING
[21684:69061786:0309/181449.460350:ERROR:content/browser/gpu/gpu_process_host.cc:999] GPU process exited unexpectedly: exit_code=256

```
## References

- DeserializeTimingFunction (linear branch with missing size >= 2 check): <https://source.chromium.org/chromium/chromium/src/+/main:components/viz/service/layers/layer_context_impl.cc;l=1187-1201>
- LinearTimingFunction::Create (DCHECK-only guard): <https://source.chromium.org/chromium/chromium/src/+/main:ui/gfx/animation/keyframe/timing_function.cc;l=169-173>
- LinearTimingFunction::GetValue (OOB access site): <https://source.chromium.org/chromium/chromium/src/+/main:ui/gfx/animation/keyframe/timing_function.cc;l=187-228>
- IsTrivial definition: <https://source.chromium.org/chromium/chromium/src/+/main:ui/gfx/animation/keyframe/timing_function.h;l=164>
- Mojo TimingFunction union (no array size constraint): <https://source.chromium.org/chromium/chromium/src/+/main:services/viz/public/mojom/compositing/animation.mojom;l=53-55>
- \_LIBCPP\_ABI\_BOUNDED\_ITERATORS\_IN\_VECTOR (commented out): <https://source.chromium.org/chromium/chromium/src/+/main:third_party/libc++/src/include/__cxx03/__configuration/abi.h;l=155>

## Credit

Please use 86ac1f1587b71893ed2ad792cd7dde32 as the credit for this vulnerability. Thank you.

## Attachments

- [poc.html](attachments/poc.html) (text/html, 24.9 KB)
- [copy_mojo_js_bindings.py](attachments/copy_mojo_js_bindings.py) (text/x-python, 468 B)

## Timeline

### jd...@chromium.org (2026-03-09)

Adding TENTATIVE severity to aid in triage.

### ns...@chromium.org (2026-03-09)

Thank you for your bug report. Marking security-impact-none as this requires `kTreeAnimationsInViz` which hasn't been enabled by default.

S1/P1 as the OOB read requires a compromised renderer.

### bl...@chromium.org (2026-03-09)

Mo, can you triage as this is TiV-specific? Thanks!

### zm...@chromium.org (2026-04-30)

The analysis is correct. We should add validation of the size of the points. It's not a security concern as pointed out in Comment #3 since TreeAnimationsInViz is still under development.

### dx...@google.com (2026-04-30)

Project: chromium/src  

Branch:  main  

Author:  Zhenyao Mo [zmo@chromium.org](mailto:zmo@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7807569>

[TreesInViz] Validate LinearTimingFunction's input point count.

---


Expand for full commit details
```
     
    If they are none-zero, they have to be at least two. 
     
    TEST=viz_unittests 
     
    Bug: 490963038 
    Change-Id: Iade42c29b81fd2c5613b6ed395c5b3189d5b7778 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7807569 
    Commit-Queue: Zhenyao Mo <zmo@chromium.org> 
    Commit-Queue: Robert Flack <flackr@chromium.org> 
    Auto-Submit: Zhenyao Mo <zmo@chromium.org> 
    Reviewed-by: Robert Flack <flackr@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1623399}

```

---

Files:

- M `components/viz/service/layers/layer_context_impl.cc`
- M `components/viz/service/layers/layer_context_impl_animation_unittest.cc`
- M `ui/gfx/animation/keyframe/timing_function.cc`

---

Hash: [006569f40dacbc962a9610f426fd31bf6efec3bc](https://chromiumdash.appspot.com/commit/006569f40dacbc962a9610f426fd31bf6efec3bc)  

Date: Thu Apr 30 20:23:28 2026


---

### sp...@google.com (2026-05-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Baseline with bisect. User information disclosure


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### kb...@google.com (2026-05-22)

This was actually reported earlier by another security researcher in [Bug 488089244](https://issues.chromium.org/issues/488089244).

### ch...@google.com (2026-08-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/490963038)*
