# Update Poc: Container-Overflow in `SurfaceAllocationGroup::OnFirstSurfaceActivation` due to reentrant mutation of `active_embedders_` in GPU process

| Field | Value |
|-------|-------|
| **Issue ID** | [491685406](https://issues.chromium.org/issues/491685406) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Compositing |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | su...@google.com |
| **Created** | 2026-03-11 |
| **Bounty** | $3,000.00 |

## Description

## Note

**I reported this issue in the previous issue: <https://issues.chromium.org/issues/489358139>.
Due to differences in my local environment, I made a small mistake that caused the PoC to fail to reproduce on ClusterFuzz, and the issue was closed. This issue will supplement the correct PoC.**

**Now I integrated the dependent MojoJS code into the HTML file to maintain its independence, and have successfully tested it on the official ASan-enabled Chromium builds for both Linux and macOS: <https://commondatastorage.googleapis.com/chromium-browser-asan/index.html>.**

## Summary

The `SurfaceAllocationGroup::OnFirstSurfaceActivation` function in the viz compositor service iterates over `active_embedders_` using a C++ range-for loop while synchronously invoking callbacks on each embedder. These callbacks can trigger a reentrant call chain that ultimately calls `UnregisterActiveEmbedder`, which erases an element from the same `base::flat_set` being iterated. Because `base::flat_set` is backed by a sorted `std::vector`, the erase invalidates the captured iterators, causing the loop to read past the vector's logical size boundary. A compromised renderer can exploit this via `SubmitCompositorFrame` to attack the GPU process.

The vulnerable code resides in `components/viz/service/surfaces/surface_allocation_group.cc`, which is platform-independent and compiled on all Chromium desktop and mobile targets. This vulnerability affects all platforms where Chromium runs with the viz compositor service enabled, including Windows, Linux, macOS, ChromeOS, and Android. No specific GPU hardware is required to trigger the bug; the crash occurs on the VizCompositorThread in the GPU process during surface management logic that is independent of the graphics backend.

## Bisect

Introducing Commit: [`a661cdf7498e`](https://chromium.googlesource.com/chromium/src/+/a661cdf7498ea72e18b3b81a1fa0aeed19680416) "Add RegisterActiveEmbedder to SurfaceAllocationGroup"

- Date: 2019-03-11
- Author: Saman Sami [samans@chromium.org](mailto:samans@chromium.org)
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/1506593>

## Root Cause

The vulnerability lies in `SurfaceAllocationGroup::OnFirstSurfaceActivation`, which uses a C++ range-for loop to iterate `active_embedders_` and synchronously invoke `OnChildActivatedForActiveFrame` on each embedder surface. The `active_embedders_` member is declared as a `base::flat_set<raw_ptr<Surface, CtnExperimental>>`, which is internally backed by a sorted `std::vector`.

```
// components/viz/service/surfaces/surface_allocation_group.h
base::flat_set<raw_ptr<Surface, CtnExperimental>> active_embedders_;

```
```
// components/viz/service/surfaces/surface_allocation_group.cc
void SurfaceAllocationGroup::OnFirstSurfaceActivation(Surface* surface) {
  for (Surface* embedder : active_embedders_)
    embedder->OnChildActivatedForActiveFrame(surface->surface_id());
  // ...
}

```

The C++ range-for loop captures `begin()` and `end()` iterators at the start of iteration. Because `base::flat_set` is backed by a `std::vector`, any insertion or erasure invalidates these iterators.

The callback `OnChildActivatedForActiveFrame` can trigger a reentrant modification of `active_embedders_` through the following call chain. When a surface activates for the first time, it calls `OnFirstSurfaceActivation` on its allocation group (GroupA). This function iterates GroupA's `active_embedders_` and calls `OnChildActivatedForActiveFrame` on each embedder. The embedder then calls `RecomputeActiveReferencedSurfaces`, which evaluates all `SurfaceRange` entries in the embedder's active frame metadata.

```
// components/viz/service/surfaces/surface.cc
void Surface::OnChildActivatedForActiveFrame(const SurfaceId& activated_id) {
  DCHECK(HasActiveFrame());
  for (auto& surface_range : GetActiveFrame().metadata.referenced_surfaces) {
    if (surface_range.IsInRangeInclusive(activated_id)) {
      RecomputeActiveReferencedSurfaces();
      return;
    }
  }
}

```

For a `SurfaceRange` with different embed tokens (a cross-group reference), `RecomputeActiveReferencedSurfaces` calls `UpdateLastActiveReferenceAndMaybeActivate` on the end allocation group (GroupB). This function can force-activate a pending surface via deadline inheritance.

```
// components/viz/service/surfaces/surface_allocation_group.cc
void SurfaceAllocationGroup::UpdateLastActiveReferenceAndMaybeActivate(
    const SurfaceId& surface_id) {
  // ...
  auto it = FindLatestSurfaceUpTo(surface_id);
  if (it != surfaces_.end() && !(*it)->HasActiveFrame())
    (*it)->ActivatePendingFrameForInheritedDeadline();
  // ...
}

```

When this pending surface in GroupB activates, it triggers GroupB's own `OnFirstSurfaceActivation`, which again calls `OnChildActivatedForActiveFrame` on the same embedder surface (E1). This recursive call to `RecomputeActiveReferencedSurfaces` re-evaluates E1's `SurfaceRange`. Now that GroupB has an active surface, `GetLatestInFlightSurface` resolves the range to GroupB's surface. Because the resolved surface's embed token no longer matches the start of the range, the start allocation group (GroupA) is dropped from the new referenced set.

```
// components/viz/service/surfaces/surface.cc
void Surface::RecomputeActiveReferencedSurfaces() {
  // ...
  for (const SurfaceRange& surface_range :
       active_frame_data_->frame.metadata.referenced_surfaces) {
    Surface* surface =
        surface_manager_->GetLatestInFlightSurface(surface_range);
    // ...
    if (surface_range.HasDifferentEmbedTokens() &&
        (!surface ||
         surface->surface_id().HasSameEmbedTokenAs(*surface_range.start()))) {
      // start allocation group is only referenced when resolved surface
      // matches start's embed token
    }
  }
  UpdateReferencedAllocationGroups(std::move(new_referenced_allocation_groups));
}

```

When `UpdateReferencedAllocationGroups` detects that GroupA is no longer in the new set, it calls `GroupA->UnregisterActiveEmbedder(E1)`, which erases E1 from GroupA's `active_embedders_`.

```
// components/viz/service/surfaces/surface.cc
void Surface::UpdateReferencedAllocationGroups(
    std::vector<SurfaceAllocationGroup*> new_referenced_allocation_groups) {
  // ...
  for (SurfaceAllocationGroup* group : referenced_allocation_groups_) {
    if (!new_set.count(group))
      group->UnregisterActiveEmbedder(this);
  }
  // ...
}

```
```
// components/viz/service/surfaces/surface_allocation_group.cc
void SurfaceAllocationGroup::UnregisterActiveEmbedder(Surface* surface) {
  DCHECK(active_embedders_.count(surface));
  active_embedders_.erase(surface);
  MaybeMarkForDestruction();
}

```

This erase occurs while the outer `OnFirstSurfaceActivation` is still iterating over the same `active_embedders_` container. The erase shifts all subsequent elements left in the underlying vector, invalidating the captured `__end` iterator and corrupting the iteration state. The loop skips the element that shifted into the erased position and eventually reads past the vector's logical end, producing a container-overflow.

With five active embedders (the root compositor plus four attacker-controlled surfaces E1 through E4), erasing E1 reduces the size from five to four. The stale `__end` iterator still points to index five, so after processing E3 and E4 (E2 is skipped due to the left-shift), the loop attempts to read index four of a size-four vector, triggering an out-of-bounds read.

A compromised renderer can construct this scenario because `CompositorFrameMetadata::referenced_surfaces` accepts arbitrary `SurfaceRange` values without any permission or ownership validation. The renderer controls multiple FrameSinks (obtained through OffscreenCanvas), can submit frames with cross-group SurfaceRange references, and can create pending surfaces with unresolvable activation dependencies to set up the precise timing required.

## Reproduce

Run with the asan chromium using MojoJS:

```
# test on macOS
out/asan/Chromium.app/Contents/MacOS/Chromium --user-data-dir=./user --enable-blink-features=MojoJS,MojoJSTest --enable-logging=stderr poc_mojo_standalone.html

# test on Linux
out/asan/chrome --user-data-dir=./user --enable-blink-features=MojoJS,MojoJSTest --enable-logging=stderr poc_mojo_standalone.html

```
### ASAN output

```
=================================================================
==35918==ERROR: AddressSanitizer: container-overflow on address 0x60600035cb60 at pc 0x00031b9e3ee8 bp 0x0001741d8850 sp 0x0001741d8848
READ of size 8 at 0x60600035cb60 thread T13
==35918==WARNING: invalid path to external symbolizer!
==35918==WARNING: Failed to use and restart external symbolizer!
    #0 0x00031b9e3ee4 in viz::SurfaceAllocationGroup::OnFirstSurfaceActivation(viz::Surface*)+0x468 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x1b9e3ee4)
    #1 0x00031b9cbe98 in viz::Surface::ActivateFrame(viz::Surface::FrameData)+0x840 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x1b9cbe98)
    #2 0x00031b9ca254 in viz::Surface::CommitFrame(viz::Surface::FrameData)+0xd94 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x1b9ca254)
    #3 0x00031b9c9140 in viz::Surface::QueueFrame(viz::CompositorFrame, unsigned int, base::ScopedClosureRunner)+0x714 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x1b9c9140)
    #4 0x00031b771924 in viz::CompositorFrameSinkSupport::MaybeSubmitCompositorFrame(viz::LocalSurfaceId const&, viz::CompositorFrame, std::__Cr::optional<viz::HitTestRegionList>, unsigned long long)+0x1e44 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x1b771924)
    #5 0x00031b788958 in viz::CompositorFrameSinkImpl::SubmitCompositorFrame(viz::LocalSurfaceId const&, viz::CompositorFrame, std::__Cr::optional<viz::HitTestRegionList>, unsigned long long)+0x19c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x1b788958)
    #6 0x00030371e328 in viz::mojom::CompositorFrameSinkStubDispatch::Accept(viz::mojom::CompositorFrameSink*, mojo::Message*)+0x3cc (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x371e328)
    #7 0x000312130064 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*)+0x8fc (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x12130064)
    #8 0x000312144edc in mojo::MessageDispatcher::Accept(mojo::Message*)+0x2f0 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x12144edc)
    #9 0x000312135264 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*)+0x148 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x12135264)
    #10 0x000312151cb8 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*)+0x650 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x12151cb8)
    #11 0x000312150768 in mojo::internal::MultiplexRouter::Accept(mojo::Message*)+0x558 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x12150768)
    #12 0x000312144edc in mojo::MessageDispatcher::Accept(mojo::Message*)+0x2f0 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x12144edc)
    #13 0x000312123228 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>)+0x394 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x12123228)
    #14 0x0003121246f8 in mojo::Connector::ReadAllAvailableMessages()+0x23c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x121246f8)
    #15 0x0003121241f8 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int)+0xe8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x121241f8)
    #16 0x000312125ce0 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int)+0x1b8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x12125ce0)
    #17 0x0003039b4b50 in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const &+0x148 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x39b4b50)
    #18 0x0003039b492c in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&)+0xf0 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x39b492c)
    #19 0x000312903370 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const &+0x154 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x12903370)
    #20 0x000312902d8c in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&)+0x398 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x12902d8c)
    #21 0x000312903ccc in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase*)+0x184 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x12903ccc)
    #22 0x000312322bb0 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x12322bb0)
    #23 0x00031238b0e4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x88c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x1238b0e4)
    #24 0x00031238a430 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x1238a430)
    #25 0x0003124abb74 in base::MessagePumpCFRunLoopBase::RunWork()+0x1c8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x124abb74)
    #26 0x00031249d2a8 in base::apple::CallWithEHFrame(void () block_pointer)+0xc (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x1249d2a8)
    #27 0x0003124a9fac in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0xec (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x124a9fac)
    #28 0x00019b3549f4 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5f9f4)
    #29 0x00019b354988 in __CFRunLoopDoSource0+0xa8 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5f988)
    #30 0x00019b3546f4 in __CFRunLoopDoSources0+0xe4 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5f6f4)
    #31 0x00019b353384 in __CFRunLoopRun+0x330 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5e384)
    #32 0x00019b40de30 in _CFRunLoopRunSpecificWithOptions+0x210 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x118e30)
    #33 0x00019d5a2960 in -[NSRunLoop(NSRunLoop) runMode:beforeDate:]+0xd0 (/System/Library/Frameworks/Foundation.framework/Versions/C/Foundation:arm64e+0xa5b960)
    #34 0x0003124accc4 in base::MessagePumpNSRunLoop::DoRun(base::MessagePump::Delegate*)+0xc8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x124accc4)
    #35 0x0003124a8d04 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x290 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x124a8d04)
    #36 0x00031238c444 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x32c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x1238c444)
    #37 0x0003122b1290 in base::RunLoop::Run(base::Location const&)+0x430 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x122b1290)
    #38 0x000312401a24 in base::Thread::Run(base::RunLoop*)+0xd8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x12401a24)
    #39 0x000312401eac in base::Thread::ThreadMain()+0x3d8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x12401eac)
    #40 0x000312458b18 in base::(anonymous namespace)::ThreadFunc(void*)+0x154 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x12458b18)
    #41 0x000101221878 in __sanitizer_weak_hook_memcmp+0x3674c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Helpers/Chromium Helper.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x51878)
    #42 0x00019b2b5c04 in _pthread_start+0x84 (/usr/lib/system/libsystem_pthread.dylib:arm64e+0x6c04)
    #43 0x00019b2b0ba4 in thread_start+0x4 (/usr/lib/system/libsystem_pthread.dylib:arm64e+0x1ba4)

0x60600035cb60 is located 32 bytes inside of 64-byte region [0x60600035cb40,0x60600035cb80)
allocated by thread T13 here:
    #0 0x000101224fc0 in __asan_memmove+0x2fd0 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Helpers/Chromium Helper.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x54fc0)
    #1 0x0003288abff0 in operator new(unsigned long)+0x18 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x288abff0)
    #2 0x00031b784488 in std::__Cr::__wrap_iter<base::raw_ptr<viz::Surface, (partition_alloc::internal::RawPtrTraits)1>*> std::__Cr::vector<base::raw_ptr<viz::Surface, (partition_alloc::internal::RawPtrTraits)1>, std::__Cr::allocator<base::raw_ptr<viz::Surface, (partition_alloc::internal::RawPtrTraits)1>>>::emplace<base::raw_ptr<viz::Surface, (partition_alloc::internal::RawPtrTraits)1>>(std::__Cr::__wrap_iter<base::raw_ptr<viz::Surface, (partition_alloc::internal::RawPtrTraits)1> const*>, base::raw_ptr<viz::Surface, (partition_alloc::internal::RawPtrTraits)1>&&)+0x160 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x1b784488)
    #3 0x00031b78427c in std::__Cr::pair<std::__Cr::__wrap_iter<base::raw_ptr<viz::Surface, (partition_alloc::internal::RawPtrTraits)1>*>, bool> base::internal::flat_tree<base::raw_ptr<viz::Surface, (partition_alloc::internal::RawPtrTraits)1>, std::__Cr::identity, std::__Cr::less<void>, std::__Cr::vector<base::raw_ptr<viz::Surface, (partition_alloc::internal::RawPtrTraits)1>, std::__Cr::allocator<base::raw_ptr<viz::Surface, (partition_alloc::internal::RawPtrTraits)1>>>>::emplace_key_args<base::raw_ptr<viz::Surface, (partition_alloc::internal::RawPtrTraits)1>, base::raw_ptr<viz::Surface, (partition_alloc::internal::RawPtrTraits)1>>(base::raw_ptr<viz::Surface, (partition_alloc::internal::RawPtrTraits)1> const&, base::raw_ptr<viz::Surface, (partition_alloc::internal::RawPtrTraits)1>&&)+0x184 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x1b78427c)
    #4 0x00031b9e29dc in viz::SurfaceAllocationGroup::RegisterActiveEmbedder(viz::Surface*)+0x54 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x1b9e29dc)
    #5 0x00031b9ce734 in viz::Surface::UpdateReferencedAllocationGroups(std::__Cr::vector<viz::SurfaceAllocationGroup*, std::__Cr::allocator<viz::SurfaceAllocationGroup*>>)+0x26c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x1b9ce734)
    #6 0x00031b9c8060 in viz::Surface::RecomputeActiveReferencedSurfaces()+0x58c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x1b9c8060)
    #7 0x00031b9cbc98 in viz::Surface::ActivateFrame(viz::Surface::FrameData)+0x640 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x1b9cbc98)
    #8 0x00031b9ca254 in viz::Surface::CommitFrame(viz::Surface::FrameData)+0xd94 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x1b9ca254)
    #9 0x00031b9c9140 in viz::Surface::QueueFrame(viz::CompositorFrame, unsigned int, base::ScopedClosureRunner)+0x714 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x1b9c9140)
    #10 0x00031b771924 in viz::CompositorFrameSinkSupport::MaybeSubmitCompositorFrame(viz::LocalSurfaceId const&, viz::CompositorFrame, std::__Cr::optional<viz::HitTestRegionList>, unsigned long long)+0x1e44 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x1b771924)
    #11 0x00031b788958 in viz::CompositorFrameSinkImpl::SubmitCompositorFrame(viz::LocalSurfaceId const&, viz::CompositorFrame, std::__Cr::optional<viz::HitTestRegionList>, unsigned long long)+0x19c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x1b788958)
    #12 0x00030371e328 in viz::mojom::CompositorFrameSinkStubDispatch::Accept(viz::mojom::CompositorFrameSink*, mojo::Message*)+0x3cc (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x371e328)
    #13 0x000312130064 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*)+0x8fc (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x12130064)
    #14 0x000312144edc in mojo::MessageDispatcher::Accept(mojo::Message*)+0x2f0 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x12144edc)
    #15 0x000312135264 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*)+0x148 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x12135264)
    #16 0x000312151cb8 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*)+0x650 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x12151cb8)
    #17 0x000312150768 in mojo::internal::MultiplexRouter::Accept(mojo::Message*)+0x558 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x12150768)
    #18 0x000312144edc in mojo::MessageDispatcher::Accept(mojo::Message*)+0x2f0 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x12144edc)
    #19 0x000312123228 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>)+0x394 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x12123228)
    #20 0x0003121246f8 in mojo::Connector::ReadAllAvailableMessages()+0x23c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x121246f8)
    #21 0x0003121241f8 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int)+0xe8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x121241f8)
    #22 0x000312125ce0 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int)+0x1b8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x12125ce0)
    #23 0x0003039b4b50 in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const &+0x148 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x39b4b50)
    #24 0x0003039b492c in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&)+0xf0 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x39b492c)
    #25 0x000312903370 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const &+0x154 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x12903370)
    #26 0x000312902d8c in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&)+0x398 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x12902d8c)
    #27 0x000312903ccc in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase*)+0x184 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x12903ccc)
    #28 0x000312322bb0 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x12322bb0)
    #29 0x00031238b0e4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x88c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x1238b0e4)

Thread T13 created by T0 here:
    #0 0x00010121b968 in __sanitizer_weak_hook_memcmp+0x3083c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Helpers/Chromium Helper.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x4b968)
    #1 0x0003124580dc in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType)+0x270 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x124580dc)
    #2 0x000312400d5c in base::Thread::StartWithOptions(base::Thread::Options)+0x498 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x12400d5c)
    #3 0x00030ba32390 in viz::VizCompositorThreadRunnerImpl::VizCompositorThreadRunnerImpl()+0x228 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0xba32390)
    #4 0x00030ba37abc in viz::VizMainImpl::VizMainImpl(viz::VizMainImpl::Delegate*, viz::VizMainImpl::ExternalDependencies, std::__Cr::unique_ptr<gpu::GpuInit, std::__Cr::default_delete<gpu::GpuInit>>)+0x7c8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0xba37abc)
    #5 0x00031b666c1c in content::GpuChildThread::GpuChildThread(base::RepeatingCallback<void ()>, content::ChildThreadImpl::Options, std::__Cr::unique_ptr<gpu::GpuInit, std::__Cr::default_delete<gpu::GpuInit>>)+0x1c0 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x1b666c1c)
    #6 0x00031b6669a0 in content::GpuChildThread::GpuChildThread(base::RepeatingCallback<void ()>, std::__Cr::unique_ptr<gpu::GpuInit, std::__Cr::default_delete<gpu::GpuInit>>)+0x184 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x1b6669a0)
    #7 0x00031b669bec in content::GpuMain(content::MainFunctionParams)+0x788 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x1b669bec)
    #8 0x00030ea3a5f0 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x420 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0xea3a5f0)
    #9 0x00030ea3c770 in content::ContentMainRunnerImpl::Run()+0x53c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0xea3c770)
    #10 0x00030ea382e0 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x858 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0xea382e0)
    #11 0x00030ea387d0 in content::ContentMain(content::ContentMainParams)+0x190 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0xea387d0)
    #12 0x000300005cb4 in ChromeMain+0x490 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x5cb4)
    #13 0x000100d88ce4 in main+0x254 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Helpers/Chromium Helper.app/Contents/MacOS/Chromium Helper:arm64+0x100000ce4)
    #14 0x00019aeedd50 in start+0x1c0c (/usr/lib/dyld:arm64e+0x8d50)

HINT: if you don't care about these errors you may set ASAN_OPTIONS=detect_container_overflow=0.
Or if supported by the container library, pass -D__SANITIZER_DISABLE_CONTAINER_OVERFLOW__ to the compiler to disable  instrumentation.
If you suspect a false positive see also: https://github.com/google/sanitizers/wiki/AddressSanitizerContainerOverflow.
SUMMARY: AddressSanitizer: container-overflow (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x1b9e3ee4) in viz::SurfaceAllocationGroup::OnFirstSurfaceActivation(viz::Surface*)+0x468
Shadow bytes around the buggy address:
  0x60600035c880: fa fa f7 fa fd fd fd fd fd fd fd fa fa fa f7 fa
  0x60600035c900: fd fd fd fd fd fd fd fa fa fa f7 fa fd fd fd fd
  0x60600035c980: fd fd fd fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x60600035ca00: fa fa f7 fa 00 00 00 00 00 00 00 00 fa fa f7 fa
  0x60600035ca80: 00 00 00 00 00 00 00 00 fa fa f7 fa 00 00 00 00
=>0x60600035cb00: 00 00 00 00 fa fa f7 fa 00 00 00 00[fc]fc fc fc
  0x60600035cb80: fa fa f7 fa fd fd fd fd fd fd fd fd fa fa f7 fa
  0x60600035cc00: 00 00 00 00 00 00 00 00 fa fa f7 fa 00 00 00 00
  0x60600035cc80: 00 00 00 00 fa fa f7 fa 00 00 00 00 00 00 00 00
  0x60600035cd00: fa fa f7 fa 00 00 00 00 00 00 00 00 fa fa f7 fa
  0x60600035cd80: fd fd fd fd fd fd fd fd fa fa f7 fa fd fd fd fd
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

==35918==ADDITIONAL INFO

==35918==Note: Please include this section with the ASan report.
Task trace:
    #0 0x000312903708 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int)+0x230 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7714.0/Chromium Framework:arm64+0x12903708)

==35918==END OF ADDITIONAL INFO

==35918==ABORTING
[35850:53415468:0304/015935.928417:ERROR:content/browser/gpu/gpu_process_host.cc:999] GPU process exited unexpectedly: exit_code=256

```
## References

- `components/viz/service/surfaces/surface_allocation_group.cc` (OnFirstSurfaceActivation, UnregisterActiveEmbedder, UpdateLastActiveReferenceAndMaybeActivate)
- `components/viz/service/surfaces/surface_allocation_group.h` (active\_embedders\_ declaration)
- `components/viz/service/surfaces/surface.cc` (OnChildActivatedForActiveFrame, RecomputeActiveReferencedSurfaces, UpdateReferencedAllocationGroups, ActivateFrame)
- `components/viz/service/frame_sinks/compositor_frame_sink_support.cc` (MaybeSubmitCompositorFrame, no validation of referenced\_surfaces)

## Credit

86ac1f1587b71893ed2ad792cd7dde32

## Attachments

- [poc_mojo_standalone.html](attachments/poc_mojo_standalone.html) (text/html, 1.0 MB)

## Timeline

### dc...@chromium.org (2026-03-11)

I /think/ this can only be reached by a compromised renderer, hence high severity. If you can demonstrate that a regular page without MojoJS can trigger this, that would affect the severity evaluation.

### ch...@google.com (2026-03-12)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-12)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### jo...@chromium.org (2026-03-17)

So far demonstrated with testing api, not a regular page. Decreasing priority

### ky...@chromium.org (2026-05-08)

I think this should be S1 since it's a UAF that impacts the unsandboxed Android GPU process from a compromised renderer.

### ch...@google.com (2026-05-11)

We commit ourselves to a 60 day deadline for fixing for s1 severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

### su...@google.com (2026-05-11)

Fix is in flight: [crrev.com/c/7833806](https://crrev.com/c/7833806)

### dx...@google.com (2026-05-12)

Project: chromium/src  

Branch:  main  

Author:  Sunny Sachanandani [sunnyps@chromium.org](mailto:sunnyps@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7833806>

[viz] Fix iterator invalidation in SurfaceAllocationGroup

---


Expand for full commit details
```
     
    Copy `active_embedders_` before iterating to avoid invalidation due to 
    re-entrant container modification when calling 
    `OnChildActivatedForActiveFrame`. 
     
    Also add a regression test in `surface_unittest.cc`. 
     
    Bug: 491685406, 510107264 
    Test: SurfaceTest.ActiveEmbeddersIteratorInvalidation 
    Link: https://chromium-review.googlesource.com/id/I6f3a281267b1159afaacbe9d90c67bee6a6a6964 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7833806 
    Reviewed-by: Kyle Charbonneau <kylechar@chromium.org> 
    Auto-Submit: Sunny Sachanandani <sunnyps@chromium.org> 
    Commit-Queue: Sunny Sachanandani <sunnyps@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1628995}

```

---

Files:

- M `components/viz/service/surfaces/surface_allocation_group.cc`
- M `components/viz/service/surfaces/surface_unittest.cc`

---

Hash: [dc693a9dbcc71f46e9f1f51a355df8a8a5f2bf85](https://chromiumdash.appspot.com/commit/dc693a9dbcc71f46e9f1f51a355df8a8a5f2bf85)  

Date: Tue May 12 02:37:02 2026


---

### ch...@google.com (2026-05-20)

Requesting merge to M148 because latest trunk commit is in 150.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to M149 because latest trunk commit is in 150.

### ch...@google.com (2026-05-20)

**M148** merge request created. **Please update [crbug/514925662](https://crbug.com/514925662) to have this merge reviewed.**

### ch...@google.com (2026-05-20)

**M149** merge request created. **Please update [crbug/514928461](https://crbug.com/514928461) to have this merge reviewed.**

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

### dx...@google.com (2026-05-22)

Project: chromium/src  

Branch:  refs/branch-heads/7778  

Author:  Sunny Sachanandani [sunnyps@chromium.org](mailto:sunnyps@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7869012>

[M148] [viz] Fix iterator invalidation in SurfaceAllocationGroup

---


Expand for full commit details
```
     
    Original change's description: 
    > [viz] Fix iterator invalidation in SurfaceAllocationGroup 
    > 
    > Copy `active_embedders_` before iterating to avoid invalidation due to 
    > re-entrant container modification when calling 
    > `OnChildActivatedForActiveFrame`. 
    > 
    > Also add a regression test in `surface_unittest.cc`. 
    > 
    > Bug: 491685406, 510107264 
    > Test: SurfaceTest.ActiveEmbeddersIteratorInvalidation 
    > Link: https://chromium-review.googlesource.com/id/I6f3a281267b1159afaacbe9d90c67bee6a6a6964 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7833806 
    > Reviewed-by: Kyle Charbonneau <kylechar@chromium.org> 
    > Auto-Submit: Sunny Sachanandani <sunnyps@chromium.org> 
    > Commit-Queue: Sunny Sachanandani <sunnyps@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1628995} 
     
    (cherry picked from commit dc693a9dbcc71f46e9f1f51a355df8a8a5f2bf85) 
     
    Bug: 514925662,491685406,510107264 
    Change-Id: Ib3efcd6b671327b952b9d142d50c09187614a92f 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7869012 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Commit-Queue: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7778@{#3453} 
    Cr-Branched-From: 77f495ee216d4c3cc784d33658bad4778c0680ee-refs/heads/main@{#1610480}

```

---

Files:

- M `components/viz/service/surfaces/surface_allocation_group.cc`
- M `components/viz/service/surfaces/surface_unittest.cc`

---

Hash: [2f9d75781848df77a6d25116c72b011deb93e022](https://chromiumdash.appspot.com/commit/2f9d75781848df77a6d25116c72b011deb93e022)  

Date: Fri May 22 02:22:48 2026


---

### pe...@google.com (2026-05-22)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pe...@google.com (2026-05-28)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-05-28)

1. <https://chromium-review.git.corp.google.com/c/chromium/src/+/7866659>
2. Low - There was a small conflict.
3. 148
4. Yes, the bug was introduced in 2019.

### dx...@google.com (2026-05-30)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Sunny Sachanandani [sunnyps@chromium.org](mailto:sunnyps@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7866659>

[M144-LTS][viz] Fix iterator invalidation in SurfaceAllocationGroup

---


Expand for full commit details
```
     
    Copy `active_embedders_` before iterating to avoid invalidation due to 
    re-entrant container modification when calling 
    `OnChildActivatedForActiveFrame`. 
     
    Also add a regression test in `surface_unittest.cc`. 
     
    Bug: 491685406, 510107264 
    Test: SurfaceTest.ActiveEmbeddersIteratorInvalidation 
    Link: https://chromium-review.googlesource.com/id/I6f3a281267b1159afaacbe9d90c67bee6a6a6964 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7833806 
    Reviewed-by: Kyle Charbonneau <kylechar@chromium.org> 
    Auto-Submit: Sunny Sachanandani <sunnyps@chromium.org> 
    Commit-Queue: Sunny Sachanandani <sunnyps@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1628995} 
    (cherry picked from commit dc693a9dbcc71f46e9f1f51a355df8a8a5f2bf85) 
     
    Change-Id: Ib90a35b06a618a7cc1bafd807d1b418fa06d08e9 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7866659 
    Reviewed-by: Kyle Charbonneau <kylechar@chromium.org> 
    Reviewed-by: Fahad Mansoor <fahadmansoor@google.com> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Sunny Sachanandani <sunnyps@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4919} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `components/viz/service/surfaces/surface_allocation_group.cc`
- M `components/viz/service/surfaces/surface_unittest.cc`

---

Hash: [9604fce3faee18fa4ef3999c5aacc69ec011da63](https://chromiumdash.appspot.com/commit/9604fce3faee18fa4ef3999c5aacc69ec011da63)  

Date: Sat May 30 08:28:40 2026


---

### dx...@google.com (2026-06-18)

Project: chromium/src  

Branch:  refs/branch-heads/7827  

Author:  Sunny Sachanandani [sunnyps@chromium.org](mailto:sunnyps@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7868994>

[M149] [viz] Fix iterator invalidation in SurfaceAllocationGroup

---


Expand for full commit details
```
[M149] [viz] Fix iterator invalidation in SurfaceAllocationGroup

Original change's description:
> [viz] Fix iterator invalidation in SurfaceAllocationGroup
>
> Copy `active_embedders_` before iterating to avoid invalidation due to
> re-entrant container modification when calling
> `OnChildActivatedForActiveFrame`.
>
> Also add a regression test in `surface_unittest.cc`.
>
> Bug: 491685406, 510107264
> Test: SurfaceTest.ActiveEmbeddersIteratorInvalidation
> Link: https://chromium-review.googlesource.com/id/I6f3a281267b1159afaacbe9d90c67bee6a6a6964
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7833806
> Reviewed-by: Kyle Charbonneau <kylechar@chromium.org>
> Auto-Submit: Sunny Sachanandani <sunnyps@chromium.org>
> Commit-Queue: Sunny Sachanandani <sunnyps@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1628995}

(cherry picked from commit dc693a9dbcc71f46e9f1f51a355df8a8a5f2bf85)

Bug: 514928461,491685406,510107264
Change-Id: Ib057de44d0eef67d0161f012c74fd34c4a5882e4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7868994
Reviewed-by: Maggie Chen <magchen@chromium.org>
Commit-Queue: Sunny Sachanandani <sunnyps@chromium.org>
Cr-Commit-Position: refs/branch-heads/7827@{#3421}
Cr-Branched-From: 9f3e9aaccba63bd2ec30334e45e0bfd07ebcc8f1-refs/heads/main@{#1625079}

```

---

Files:

- M `components/viz/service/surfaces/surface_allocation_group.cc`
- M `components/viz/service/surfaces/surface_unittest.cc`

---

Hash: [3c6a5a6cd43605bf90a61cf45f2d5ed2280a3e5e](https://chromiumdash.appspot.com/commit/3c6a5a6cd43605bf90a61cf45f2d5ed2280a3e5e)  

Date: Thu Jun 18 22:32:51 2026


---

### ch...@google.com (2026-08-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/491685406)*
