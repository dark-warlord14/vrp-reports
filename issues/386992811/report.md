# Security: heap-use-after-free in cc::TileManager::MarkTilesOutOfMemory

| Field | Value |
|-------|-------|
| **Issue ID** | [386992811](https://issues.chromium.org/issues/386992811) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Compositing |
| **Platforms** | Mac |
| **Chrome Version** | 131.0.0.0 |
| **Reporter** | zh...@gmail.com |
| **Assignee** | zm...@chromium.org |
| **Created** | 2025-01-01 |
| **Bounty** | $11,000.00 |

## Description

# Steps to reproduce the problem

1. Compile asan chromium on arm mac，The commit I used is `git checkout edaf05b8d1867a0e26a566d19bfcbebc6c117168`
2. To better reproduce the vulnerability, apply some debugging diff `git apply poc.diff`
3. Triggering the vulnerability consumes a lot of memory. To make it easier to do this, you can do this to facilitate reproduction.`./out/asan-1230/Chromium.app/Contents/MacOS/Chromium --no-sandbox --enable-experimental-web-platform-features --user-data-dir=/tmp/userdata/t12 https://registry.khronos.org/webgl/conformance-suites/2.0.0/webgl-conformance-tests.html`

# Problem Description

RCA and Bisect coming soon!

# Summary

Security: heap-use-after-free in cc::TileManager::MarkTilesOutOfMemory

# Custom Questions

#### Crash state:

```
=================================================================
==37873==ERROR: AddressSanitizer: heap-use-after-free on address 0x6110004fbbc0 at pc 0x0001161c21f4 bp 0x000388082530 sp 0x000388082528
READ of size 4 at 0x6110004fbbc0 thread T11
==37873==WARNING: invalid path to external symbolizer!
==37873==WARNING: Failed to use and restart external symbolizer!
    #0 0x0001161c21f0 in cc::TileManager::MarkTilesOutOfMemory(std::__Cr::unique_ptr<cc::RasterTilePriorityQueue, std::__Cr::default_delete<cc::RasterTilePriorityQueue>>) const+0x56c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcc.dylib:arm64+0x30a1f0)
    #1 0x0001161aef74 in cc::TileManager::CheckIfMoreTilesNeedToBePrepared()+0x6b4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcc.dylib:arm64+0x2f6f74)
    #2 0x0001161c4b08 in base::internal::Invoker<base::internal::FunctorTraits<void (cc::TileManager::* const&)(), cc::TileManager*>, base::internal::BindState<true, true, false, void (cc::TileManager::*)(), base::internal::UnretainedWrapper<cc::TileManager, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::Run(base::internal::BindStateBase*)+0x184 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcc.dylib:arm64+0x30cb08)
    #3 0x00010635e2e0 in base::RepeatingCallback<void ()>::Run() const &+0x14c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcc_base.dylib:arm64+0x22e0)
    #4 0x000106388d98 in void base::internal::Invoker<base::internal::FunctorTraits<void (cc::UniqueNotifier::*&&)(), base::WeakPtr<cc::UniqueNotifier>&&>, base::internal::BindState<true, true, false, void (cc::UniqueNotifier::*)(), base::WeakPtr<cc::UniqueNotifier>>, void ()>::RunImpl<void (cc::UniqueNotifier::*)(), std::__Cr::tuple<base::WeakPtr<cc::UniqueNotifier>>, 0ul>(void (cc::UniqueNotifier::*&&)(), std::__Cr::tuple<base::WeakPtr<cc::UniqueNotifier>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>)+0x168 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcc_base.dylib:arm64+0x2cd98)
    #5 0x00010305ed40 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libbase.dylib:arm64+0x1c2d40)
    #6 0x0001030ccc1c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x864 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libbase.dylib:arm64+0x230c1c)
    #7 0x0001030cbf00 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libbase.dylib:arm64+0x22ff00)
    #8 0x00010325b67c in base::MessagePumpKqueue::RunBatched(base::MessagePump::Delegate*)+0x13c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libbase.dylib:arm64+0x3bf67c)
    #9 0x00010325b24c in base::MessagePumpKqueue::Run(base::MessagePump::Delegate*)+0x134 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libbase.dylib:arm64+0x3bf24c)
    #10 0x0001030ce168 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x35c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libbase.dylib:arm64+0x232168)
    #11 0x000102fe0b84 in base::RunLoop::Run(base::Location const&)+0x434 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libbase.dylib:arm64+0x144b84)
    #12 0x000157682934 in blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run()+0x2f8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libblink_platform.dylib:arm64+0xc46934)
    #13 0x0001031ac4a0 in base::(anonymous namespace)::ThreadFunc(void*)+0x154 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libbase.dylib:arm64+0x3104a0)
    #14 0x0001017c2f24 in __sanitizer_weak_hook_memcmp+0x34fdc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libclang_rt.asan_osx_dynamic.dylib:arm64+0x4ef24)
    #15 0x0001009ca9a8 in _pthread_start+0x84 (/usr/lib/system/introspection/libsystem_pthread.dylib:arm64+0x29a8)
    #16 0x0001009d4cf8 in thread_start+0x4 (/usr/lib/system/introspection/libsystem_pthread.dylib:arm64+0xccf8)

0x6110004fbbc0 is located 64 bytes inside of 216-byte region [0x6110004fbb80,0x6110004fbc58)
freed by thread T11 here:
    #0 0x0001017d5f8c in __sanitizer_finish_switch_fiber+0xa2c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libclang_rt.asan_osx_dynamic.dylib:arm64+0x61f8c)
    #1 0x0001161781e0 in cc::PictureLayerTiling::SetRasterSourceAndResize(scoped_refptr<cc::RasterSource>)+0x794 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcc.dylib:arm64+0x2c01e0)
    #2 0x000116177620 in cc::PictureLayerTiling::TakeTilesAndPropertiesFrom(cc::PictureLayerTiling*, cc::Region const&)+0x110 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcc.dylib:arm64+0x2bf620)
    #3 0x000116184e8c in cc::PictureLayerTilingSet::CopyTilingsAndPropertiesFromPendingTwin(cc::PictureLayerTilingSet const*, scoped_refptr<cc::RasterSource>, cc::Region const&)+0x584 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcc.dylib:arm64+0x2cce8c)
    #4 0x000116185790 in cc::PictureLayerTilingSet::UpdateTilingsToCurrentRasterSourceForActivation(scoped_refptr<cc::RasterSource>, cc::PictureLayerTilingSet const*, cc::Region const&, float, float)+0x270 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcc.dylib:arm64+0x2cd790)
    #5 0x000115f8dd50 in cc::PictureLayerImpl::UpdateRasterSourceInternal(scoped_refptr<cc::RasterSource>, cc::Region*, cc::PictureLayerTilingSet const*, base::flat_map<scoped_refptr<cc::PaintWorkletInput const>, std::__Cr::pair<int, std::__Cr::optional<cc::PaintRecord>>, std::__Cr::less<void>, std::__Cr::vector<std::__Cr::pair<scoped_refptr<cc::PaintWorkletInput const>, std::__Cr::pair<int, std::__Cr::optional<cc::PaintRecord>>>, std::__Cr::allocator<std::__Cr::pair<scoped_refptr<cc::PaintWorkletInput const>, std::__Cr::pair<int, std::__Cr::optional<cc::PaintRecord>>>>>> const*, cc::DiscardableImageMap const*)+0xd5c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcc.dylib:arm64+0xd5d50)
    #6 0x000115f8ca78 in cc::PictureLayerImpl::PushPropertiesTo(cc::LayerImpl*)+0x248 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcc.dylib:arm64+0xd4a78)
    #7 0x00011638f9e4 in cc::TreeSynchronizer::PushLayerProperties(cc::LayerTreeImpl*, cc::LayerTreeImpl*)+0x298 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcc.dylib:arm64+0x4d79e4)
    #8 0x000116281b94 in cc::LayerTreeHostImpl::ActivateSyncTree()+0x30c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcc.dylib:arm64+0x3c9b94)
    #9 0x0001160f1794 in cc::Scheduler::ProcessScheduledActions()+0x740 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcc.dylib:arm64+0x239794)
    #10 0x000116348c44 in cc::ProxyImpl::SetNeedsUpdateDisplayTreeOnImplThread()+0x130 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcc.dylib:arm64+0x490c44)
    #11 0x000116272138 in cc::LayerTreeHostImpl::NotifyTileStateChanged(cc::Tile const*)+0x32c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcc.dylib:arm64+0x3ba138)
    #12 0x0001161c216c in cc::TileManager::MarkTilesOutOfMemory(std::__Cr::unique_ptr<cc::RasterTilePriorityQueue, std::__Cr::default_delete<cc::RasterTilePriorityQueue>>) const+0x4e8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcc.dylib:arm64+0x30a16c)
    #13 0x0001161aef74 in cc::TileManager::CheckIfMoreTilesNeedToBePrepared()+0x6b4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcc.dylib:arm64+0x2f6f74)
    #14 0x0001161c4b08 in base::internal::Invoker<base::internal::FunctorTraits<void (cc::TileManager::* const&)(), cc::TileManager*>, base::internal::BindState<true, true, false, void (cc::TileManager::*)(), base::internal::UnretainedWrapper<cc::TileManager, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::Run(base::internal::BindStateBase*)+0x184 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcc.dylib:arm64+0x30cb08)
    #15 0x00010635e2e0 in base::RepeatingCallback<void ()>::Run() const &+0x14c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcc_base.dylib:arm64+0x22e0)
    #16 0x000106388d98 in void base::internal::Invoker<base::internal::FunctorTraits<void (cc::UniqueNotifier::*&&)(), base::WeakPtr<cc::UniqueNotifier>&&>, base::internal::BindState<true, true, false, void (cc::UniqueNotifier::*)(), base::WeakPtr<cc::UniqueNotifier>>, void ()>::RunImpl<void (cc::UniqueNotifier::*)(), std::__Cr::tuple<base::WeakPtr<cc::UniqueNotifier>>, 0ul>(void (cc::UniqueNotifier::*&&)(), std::__Cr::tuple<base::WeakPtr<cc::UniqueNotifier>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>)+0x168 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcc_base.dylib:arm64+0x2cd98)
    #17 0x00010305ed40 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libbase.dylib:arm64+0x1c2d40)
    #18 0x0001030ccc1c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x864 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libbase.dylib:arm64+0x230c1c)
    #19 0x0001030cbf00 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libbase.dylib:arm64+0x22ff00)
    #20 0x00010325b67c in base::MessagePumpKqueue::RunBatched(base::MessagePump::Delegate*)+0x13c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libbase.dylib:arm64+0x3bf67c)
    #21 0x00010325b24c in base::MessagePumpKqueue::Run(base::MessagePump::Delegate*)+0x134 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libbase.dylib:arm64+0x3bf24c)
    #22 0x0001030ce168 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x35c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libbase.dylib:arm64+0x232168)
    #23 0x000102fe0b84 in base::RunLoop::Run(base::Location const&)+0x434 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libbase.dylib:arm64+0x144b84)
    #24 0x000157682934 in blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run()+0x2f8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libblink_platform.dylib:arm64+0xc46934)
    #25 0x0001031ac4a0 in base::(anonymous namespace)::ThreadFunc(void*)+0x154 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libbase.dylib:arm64+0x3104a0)
    #26 0x0001017c2f24 in __sanitizer_weak_hook_memcmp+0x34fdc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libclang_rt.asan_osx_dynamic.dylib:arm64+0x4ef24)
    #27 0x0001009ca9a8 in _pthread_start+0x84 (/usr/lib/system/introspection/libsystem_pthread.dylib:arm64+0x29a8)
    #28 0x0001009d4cf8 in thread_start+0x4 (/usr/lib/system/introspection/libsystem_pthread.dylib:arm64+0xccf8)

previously allocated by thread T11 here:
    #0 0x0001017d5b84 in __sanitizer_finish_switch_fiber+0x624 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libclang_rt.asan_osx_dynamic.dylib:arm64+0x61b84)
    #1 0x0001161c0138 in cc::TileManager::CreateTile(cc::Tile::CreateInfo const&, int, int, int)+0xc4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcc.dylib:arm64+0x308138)
    #2 0x0001161757b0 in cc::PictureLayerTiling::CreateTile(cc::Tile::CreateInfo const&)+0x178 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcc.dylib:arm64+0x2bd7b0)
    #3 0x00011617c63c in cc::PictureLayerTiling::SetLiveTilesRect(gfx::Rect const&)+0x2e4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcc.dylib:arm64+0x2c463c)
    #4 0x000116179af4 in cc::PictureLayerTiling::ComputeTilePriorityRects(gfx::Rect const&, gfx::Rect const&, gfx::Rect const&, gfx::Rect const&, float, cc::Occlusion const&)+0x464 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcc.dylib:arm64+0x2c1af4)
    #5 0x00011618a194 in cc::PictureLayerTilingSet::UpdateTilePriorities(gfx::Rect const&, float, double, cc::Occlusion const&, bool)+0x378 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcc.dylib:arm64+0x2d2194)
    #6 0x0001162c8a94 in cc::LayerTreeImpl::UpdateTiles()+0x244 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcc.dylib:arm64+0x410a94)
    #7 0x0001162c7c78 in cc::LayerTreeImpl::UpdateDrawProperties(bool, bool, std::__Cr::vector<cc::LayerImpl*, std::__Cr::allocator<cc::LayerImpl*>>*)+0x850 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcc.dylib:arm64+0x40fc78)
    #8 0x000116263d18 in cc::LayerTreeHostImpl::UpdateSyncTreeAfterCommitOrImplSideInvalidation()+0x1a8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcc.dylib:arm64+0x3abd18)
    #9 0x0001162630d4 in cc::LayerTreeHostImpl::CommitComplete()+0x274 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcc.dylib:arm64+0x3ab0d4)
    #10 0x0001160f16a4 in cc::Scheduler::ProcessScheduledActions()+0x650 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcc.dylib:arm64+0x2396a4)
    #11 0x0001160f352c in cc::Scheduler::NotifyReadyToCommit(std::__Cr::unique_ptr<cc::BeginMainFrameMetrics, std::__Cr::default_delete<cc::BeginMainFrameMetrics>>)+0x1d4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcc.dylib:arm64+0x23b52c)
    #12 0x0001163474c4 in cc::ProxyImpl::NotifyReadyToCommitOnImpl(cc::CompletionEvent*, std::__Cr::unique_ptr<cc::CommitState, std::__Cr::default_delete<cc::CommitState>>, cc::ThreadUnsafeCommitState const*, base::TimeTicks, viz::BeginFrameArgs const&, bool, cc::CommitTimestamps*, bool)+0x530 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcc.dylib:arm64+0x48f4c4)
    #13 0x00011636cd8c in void base::internal::Invoker<base::internal::FunctorTraits<void (cc::ProxyImpl::*&&)(cc::CompletionEvent*, std::__Cr::unique_ptr<cc::CommitState, std::__Cr::default_delete<cc::CommitState>>, cc::ThreadUnsafeCommitState const*, base::TimeTicks, viz::BeginFrameArgs const&, bool, cc::CommitTimestamps*, bool), cc::ProxyImpl*, cc::CompletionEvent*&&, std::__Cr::unique_ptr<cc::CommitState, std::__Cr::default_delete<cc::CommitState>>&&, cc::ThreadUnsafeCommitState*&&, base::TimeTicks&&, viz::BeginFrameArgs&&, bool&&, cc::CommitTimestamps*&&, bool&&>, base::internal::BindState<true, true, false, void (cc::ProxyImpl::*)(cc::CompletionEvent*, std::__Cr::unique_ptr<cc::CommitState, std::__Cr::default_delete<cc::CommitState>>, cc::ThreadUnsafeCommitState const*, base::TimeTicks, viz::BeginFrameArgs const&, bool, cc::CommitTimestamps*, bool), base::internal::UnretainedWrapper<cc::ProxyImpl, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<cc::CompletionEvent, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, std::__Cr::unique_ptr<cc::CommitState, std::__Cr::default_delete<cc::CommitState>>, base::internal::UnretainedWrapper<cc::ThreadUnsafeCommitState, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::TimeTicks, viz::BeginFrameArgs, bool, base::internal::UnretainedWrapper<cc::CommitTimestamps, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, bool>, void ()>::RunImpl<void (cc::ProxyImpl::*)(cc::CompletionEvent*, std::__Cr::unique_ptr<cc::CommitState, std::__Cr::default_delete<cc::CommitState>>, cc::ThreadUnsafeCommitState const*, base::TimeTicks, viz::BeginFrameArgs const&, bool, cc::CommitTimestamps*, bool), std::__Cr::tuple<base::internal::UnretainedWrapper<cc::ProxyImpl, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<cc::CompletionEvent, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, std::__Cr::unique_ptr<cc::CommitState, std::__Cr::default_delete<cc::CommitState>>, base::internal::UnretainedWrapper<cc::ThreadUnsafeCommitState, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::TimeTicks, viz::BeginFrameArgs, bool, base::internal::UnretainedWrapper<cc::CommitTimestamps, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, bool>, 0ul, 1ul, 2ul, 3ul, 4ul, 5ul, 6ul, 7ul, 8ul>(void (cc::ProxyImpl::*&&)(cc::CompletionEvent*, std::__Cr::unique_ptr<cc::CommitState, std::__Cr::default_delete<cc::CommitState>>, cc::ThreadUnsafeCommitState const*, base::TimeTicks, viz::BeginFrameArgs const&, bool, cc::CommitTimestamps*, bool), std::__Cr::tuple<base::internal::UnretainedWrapper<cc::ProxyImpl, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<cc::CompletionEvent, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, std::__Cr::unique_ptr<cc::CommitState, std::__Cr::default_delete<cc::CommitState>>, base::internal::UnretainedWrapper<cc::ThreadUnsafeCommitState, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::TimeTicks, viz::BeginFrameArgs, bool, base::internal::UnretainedWrapper<cc::CommitTimestamps, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, bool>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul, 4ul, 5ul, 6ul, 7ul, 8ul>)+0x294 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcc.dylib:arm64+0x4b4d8c)
    #14 0x00010305ed40 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libbase.dylib:arm64+0x1c2d40)
    #15 0x0001030ccc1c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x864 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libbase.dylib:arm64+0x230c1c)
    #16 0x0001030cbf00 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libbase.dylib:arm64+0x22ff00)
    #17 0x00010325b67c in base::MessagePumpKqueue::RunBatched(base::MessagePump::Delegate*)+0x13c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libbase.dylib:arm64+0x3bf67c)
    #18 0x00010325b24c in base::MessagePumpKqueue::Run(base::MessagePump::Delegate*)+0x134 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libbase.dylib:arm64+0x3bf24c)
    #19 0x0001030ce168 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x35c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libbase.dylib:arm64+0x232168)
    #20 0x000102fe0b84 in base::RunLoop::Run(base::Location const&)+0x434 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libbase.dylib:arm64+0x144b84)
    #21 0x000157682934 in blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run()+0x2f8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libblink_platform.dylib:arm64+0xc46934)
    #22 0x0001031ac4a0 in base::(anonymous namespace)::ThreadFunc(void*)+0x154 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libbase.dylib:arm64+0x3104a0)
    #23 0x0001017c2f24 in __sanitizer_weak_hook_memcmp+0x34fdc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libclang_rt.asan_osx_dynamic.dylib:arm64+0x4ef24)
    #24 0x0001009ca9a8 in _pthread_start+0x84 (/usr/lib/system/introspection/libsystem_pthread.dylib:arm64+0x29a8)
    #25 0x0001009d4cf8 in thread_start+0x4 (/usr/lib/system/introspection/libsystem_pthread.dylib:arm64+0xccf8)

Thread T11 created by T0 here:
    #0 0x0001017bdc94 in __sanitizer_weak_hook_memcmp+0x2fd4c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libclang_rt.asan_osx_dynamic.dylib:arm64+0x49c94)
    #1 0x0001031abb6c in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType)+0x270 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libbase.dylib:arm64+0x30fb6c)
    #2 0x00010314a354 in base::SimpleThread::StartAsync()+0x15c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libbase.dylib:arm64+0x2ae354)
    #3 0x0001575dfabc in blink::Thread::CreateAndSetCompositorThread()+0x144 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libblink_platform.dylib:arm64+0xba3abc)
    #4 0x00013bcae2d4 in content::RenderThreadImpl::InitializeCompositorThread()+0xd4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcontent.dylib:arm64+0x33422d4)
    #5 0x00013bcaa2cc in content::RenderThreadImpl::InitializeWebKit(mojo::BinderMap*)+0x148 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcontent.dylib:arm64+0x333e2cc)
    #6 0x00013bca65d4 in content::RenderThreadImpl::Init()+0x800 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcontent.dylib:arm64+0x333a5d4)
    #7 0x00013bca9a08 in content::RenderThreadImpl::RenderThreadImpl(base::RepeatingCallback<void ()>, std::__Cr::unique_ptr<blink::scheduler::WebThreadScheduler, std::__Cr::default_delete<blink::scheduler::WebThreadScheduler>>)+0x780 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcontent.dylib:arm64+0x333da08)
    #8 0x00013bccecbc in content::RendererMain(content::MainFunctionParams)+0x484 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcontent.dylib:arm64+0x3362cbc)
    #9 0x00013bee6d48 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x3ec (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcontent.dylib:arm64+0x357ad48)
    #10 0x00013bee8a5c in content::ContentMainRunnerImpl::Run()+0x448 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcontent.dylib:arm64+0x357ca5c)
    #11 0x00013bee49ec in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x5c8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcontent.dylib:arm64+0x35789ec)
    #12 0x00013bee52b8 in content::ContentMain(content::ContentMainParams)+0x190 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcontent.dylib:arm64+0x35792b8)
    #13 0x000118aafef0 in ChromeMain+0x360 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libchrome_dll.dylib:arm64+0xbef0)
    #14 0x0001009a8ce4 in main+0x254 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6928.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer):arm64+0x100000ce4)
    #15 0x00018dfb0270  (<unknown module>)

SUMMARY: AddressSanitizer: heap-use-after-free (/Users/zh1x1an1221/xcode-chromium/src/out/asan-1230/libcc.dylib:arm64+0x30a1f0) in cc::TileManager::MarkTilesOutOfMemory(std::__Cr::unique_ptr<cc::RasterTilePriorityQueue, std::__Cr::default_delete<cc::RasterTilePriorityQueue>>) const+0x56c
Shadow bytes around the buggy address:
  0x6110004fb900: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x6110004fb980: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa
  0x6110004fba00: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x6110004fba80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x6110004fbb00: fd fd fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
=>0x6110004fbb80: fd fd fd fd fd fd fd fd[fd]fd fd fd fd fd fd fd
  0x6110004fbc00: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa
  0x6110004fbc80: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x6110004fbd00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x6110004fbd80: fd fd fd fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x6110004fbe00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
Message from debugger: killed
Program ended with exit code: 9

```
# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [asan-PictureLayerTilingSet.txt](attachments/asan-PictureLayerTilingSet.txt) (text/plain, 28.0 KB)
- [asan-RemoveTilesInRegion.txt](attachments/asan-RemoveTilesInRegion.txt) (text/plain, 33.7 KB)
- [asan-SetRasterSourceAndResize.txt](attachments/asan-SetRasterSourceAndResize.txt) (text/plain, 31.6 KB)
- [poc.diff](attachments/poc.diff) (text/x-diff, 420.8 KB)
- [poc.mov](attachments/poc.mov) (video/quicktime, 135.2 MB)
- [PoC-final.mov](attachments/PoC-final.mov) (video/quicktime, 239.7 MB)

## Timeline

### zh...@gmail.com (2025-01-01)

# RCA HERE

## Objects we need to know before RCA

In [PictureLayerTiling::CreateTile](https://source.chromium.org/chromium/chromium/src/+/main:cc/tiles/picture_layer_tiling.cc;l=80-96?q=PictureLayerTiling::CreateTile) function, we can create a `Tile` object and store it in `tiles_`:

```
Tile* PictureLayerTiling::CreateTile(const Tile::CreateInfo& info) {
  const int i = info.tiling_i_index;
  const int j = info.tiling_j_index;
  TileIndex index(i, j);
  DCHECK(!base::Contains(tiles_, index));

  if (!raster_source_->IntersectsRect(info.enclosing_layer_rect)) {
    return nullptr;
  }

  all_tiles_done_ = false;

  std::unique_ptr<Tile> tile = client_->CreateTile(info); // @audit: create Tile object
  Tile* tile_ptr = tile.get();
  tiles_[index] = std::move(tile); // @audit: add tile object to unordered_map
  return tile_ptr;
}

```

[tiles\_](https://source.chromium.org/chromium/chromium/src/+/main:cc/tiles/picture_layer_tiling.h;drc=cd312f7406c08b31c70ce126b7ab4e9afd49657c;l=231) is an `unordered_map` stored in the `PictureLayerTiling` object:

```
using TileMap = std::unordered_map<TileIndex, std::unique_ptr<Tile>>;

```

And in the `Tile` object there is a [TileDrawInfo](https://source.chromium.org/chromium/chromium/src/+/main:cc/tiles/tile.h;l=172;drc=296a0fe8d8bfa678632bf9b6b4a8af38c998a5e6)

```
TileDrawInfo draw_info_;

```

So once the `Tile` object is released, the `TileDrawInfo` object will also be released.

In [cc/tiles/tile\_manager.h](https://source.chromium.org/chromium/chromium/src/+/main:cc/tiles/tile_manager.h;l=131-134;drc=296a0fe8d8bfa678632bf9b6b4a8af38c998a5e6) there is a comment in the file that describes the life cycle of the `Tile` object and the `TileManager` object:

```
// This class manages tiles, deciding which should get rasterized and which
// should no longer have any memory assigned to them. Tile objects are "owned"
// by layers; they automatically register with the manager when they are
// created, and unregister from the manager when they are deleted.

```

So `TileManager` can create `Tile` objects, such as here: [TileManager::CreateTile](https://source.chromium.org/chromium/chromium/src/+/main:cc/tiles/tile_manager.h;l=203-206;drc=296a0fe8d8bfa678632bf9b6b4a8af38c998a5e6)

The created `Tile` object is actually stored in the `TileMap` of the `PictureLayerTiling` object, which I mentioned at the beginning.

So I am very concerned about what functions the `PictureLayerTiling` object has to release the `tile` object. It is easy to find:[PictureLayerTiling::TakeTilesAndPropertiesFrom](https://source.chromium.org/chromium/chromium/src/+/main:cc/tiles/picture_layer_tiling.cc;l=139-144;drc=cd312f7406c08b31c70ce126b7ab4e9afd49657c;bpv=0;bpt=1) function.

## UAF use path

In [TileManager::CheckIfMoreTilesNeedToBePrepared](https://source.chromium.org/chromium/chromium/src/+/main:cc/tiles/tile_manager.cc;l=1873-1875) function, there is such a code:

```
  // Mark any required tiles that have not been been assigned memory after
  // reaching a steady memory state as OOM. This ensures that we activate/draw
  // even when OOM. Note that we can't reuse the queue we used for
  // AssignGpuMemoryToTiles, since the AssignGpuMemoryToTiles call could have
  // evicted some tiles that would not be picked up by the old raster queue.
  MarkTilesOutOfMemory(client_->BuildRasterQueue(
      global_state_.tree_priority,
      RasterTilePriorityQueue::Type::REQUIRED_FOR_ACTIVATION));
  MarkTilesOutOfMemory(client_->BuildRasterQueue(
      global_state_.tree_priority,
      RasterTilePriorityQueue::Type::REQUIRED_FOR_DRAW));

```

Here it will call [TileManager::MarkTilesOutOfMemory](https://source.chromium.org/chromium/chromium/src/+/main:cc/tiles/tile_manager.cc;l=1884-1894;drc=cd312f7406c08b31c70ce126b7ab4e9afd49657c) function:

```
void TileManager::MarkTilesOutOfMemory(
    std::unique_ptr<RasterTilePriorityQueue> queue) const {
  // Mark required tiles as OOM so that we can activate/draw without them.
  for (; !queue->IsEmpty(); queue->Pop()) {
    Tile* tile = queue->Top().tile();
    if (tile->draw_info().IsReadyToDraw()) // @audit: get TileDrawInfo from tile,can call IsReadyToDraw function
      continue;
    tile->draw_info().set_oom();
    client_->NotifyTileStateChanged(tile);
  }
}

```

The main purpose of `TileManager::MarkTilesOutOfMemory` here is to `Mark required tiles as OOM so that we can activate/draw without them.`

Here, the `Tile` object is taken out from the `RasterTilePriorityQueue`, and then the `IsReadyToDraw` function of the `TileDrawInfo` of this object is called.

**So there is a question, how to ensure that the `Tile` object is not released at this time?**

If the `Tile` object has been released, such as [PictureLayerTiling::TakeTilesAndPropertiesFrom](https://source.chromium.org/chromium/chromium/src/+/main:cc/tiles/picture_layer_tiling.cc;l=139-144;drc=cd312f7406c08b31c70ce126b7ab4e9afd49657c;bpv=0;bpt=1) The function is executed, releasing the `Tile` object and the `TileDrawInfo` object, then UAF will occur: [TileDrawInfo::IsReadyToDraw](https://source.chromium.org/chromium/chromium/src/+/main:cc/tiles/tile_draw_info.h;l=27;drc=cd312f7406c08b31c70ce126b7ab4e9afd49657c) when trying to read `enum Mode`

After multiple tests, I was able to successfully trigger multiple UAFs, but each release path was slightly different. I submitted each different asan.

**To prove my point above, you can search the address `0x6110002e9300` in the `asan-SetRasterSourceAndResize.txt` file I submitted, and you can prove that the object of the UAF is `TileDrawInfo`**

### zh...@gmail.com (2025-01-01)

## Bisect commit：

<https://chromium-review.googlesource.com/c/chromium/src/+/5783760>

### zh...@gmail.com (2025-01-01)

In addition, if you understand my analysis, you should be able to understand that **the HTML used to reproduce the vulnerability only needs to trigger OOM**.

You can flexibly choose any web page that you think can consume a lot of memory. My choice is for reference only.

### zh...@gmail.com (2025-01-01)

After some simple searching, I found that directly accessing large shopping websites, such as `taobao.com`, can make the reproduction very stable. I uploaded the `poc.mov` video.

### pa...@chromium.org (2025-01-01)

[security shepherd] I can't reproduce this issue. Setting labels provisionally (Found-In to extended stable and Sev 1).
vmpstr@chromium, could you PTAL and decide if the analysis in the report is sufficiently actionable?

### zh...@gmail.com (2025-01-01)

It's okay, don't worry about not being able to reproduce. I can now reproduce it stably and 100% successfully. And I am trying to streamline the features required for the POC. I have obtained a very streamlined version, which I will upload soon.

### zh...@gmail.com (2025-01-01)

I can confirm that the only feature you need to reproduce 100% is --enable-features=TreesInViz

### zh...@gmail.com (2025-01-01)

I uploaded a video `PoC-final.mov` showing how to reproduce this vulnerability with only `--enable-features=TreesInViz` feature. Since only 2-3 pages were opened, it took a little longer to trigger OOM. But I can assure you that the way to reproduce and trigger the vulnerability is correct, **because I have tried this reproduction step countless times and it worked every time**, and finally confirmed that only `--enable-features=TreesInViz` feature is needed.

### zh...@gmail.com (2025-01-01)

Therefore, in order to reduce your workload, you can consider downloading `mac-release_asan-mac-release-1401254` directly, and run it directly to reproduce the vulnerability stably:

```
rm -rf /tmp/userdata/ ; ./Chromium.app/Contents/MacOS/Chromium --no-sandbox --enable-experimental-web-platform-features --user-data-dir=/tmp/userdata/t12 https://registry.khronos.org/webgl/conformance-suites/2.0.0/webgl-conformance-tests.html https://www.taobao.com https://www.taobao.com --enable-features=TreesInViz

```

I have verified that this is definitely possible, the asan log is the same as before:

```
=================================================================
==92859==ERROR: AddressSanitizer: heap-use-after-free on address 0x6110004cc140 at pc 0x000171db1412 bp 0x00030eb164d0 sp 0x00030eb164c8
READ of size 4 at 0x6110004cc140 thread T11
==92859==WARNING: invalid path to external symbolizer!
==92859==WARNING: Failed to use and restart external symbolizer!
    #0 0x000171db1411 in cc::TileManager::MarkTilesOutOfMemory(std::__Cr::unique_ptr<cc::RasterTilePriorityQueue, std::__Cr::default_delete<cc::RasterTilePriorityQueue>>) const+0x471 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x1779a411)
    #1 0x000171d9c8d5 in cc::TileManager::CheckIfMoreTilesNeedToBePrepared()+0x875 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x177858d5)
    #2 0x000171db29c0 in base::internal::Invoker<base::internal::FunctorTraits<void (cc::TileManager::* const&)(), cc::TileManager*>, base::internal::BindState<true, true, false, void (cc::TileManager::*)(), base::internal::UnretainedWrapper<cc::TileManager, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::Run(base::internal::BindStateBase*)+0x1d0 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x1779b9c0)
    #3 0x00015bb2f7ed in base::RepeatingCallback<void ()>::Run() const &+0x17d (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x15187ed)
    #4 0x000171d75bb9 in base::internal::Invoker<base::internal::FunctorTraits<void (cc::UniqueNotifier::*&&)(), base::WeakPtr<cc::UniqueNotifier>&&>, base::internal::BindState<true, true, false, void (cc::UniqueNotifier::*)(), base::WeakPtr<cc::UniqueNotifier>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x1d9 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x1775ebb9)
    #5 0x00016cd1a8a8 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x398 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x127038a8)
    #6 0x00016cd7f9a5 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0xbd5 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x127689a5)
    #7 0x00016cd7e862 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x172 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x12767862)
    #8 0x00016cd80714 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x14 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x12769714)
    #9 0x00016cc0b447 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x1f7 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x125f4447)
    #10 0x00016cd8129b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x40b (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x1276a29b)
    #11 0x00016ccadb0e in base::RunLoop::Run(base::Location const&)+0x53e (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x12696b0e)
    #12 0x00016925db6f in blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run()+0x3ef (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0xec46b6f)
    #13 0x00016ce3616e in base::(anonymous namespace)::ThreadFunc(void*)+0x15e (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x1281f16e)
    #14 0x00010b3ed336 in __sanitizer_weak_hook_memcmp+0x34206 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:x86_64+0x51336)
    #15 0x7ff812cf8252 in _pthread_start+0x62 (/usr/lib/system/libsystem_pthread.dylib:x86_64+0x6252)
    #16 0x7ff812cf3bee in thread_start+0xe (/usr/lib/system/libsystem_pthread.dylib:x86_64+0x1bee)

0x6110004cc140 is located 64 bytes inside of 216-byte region [0x6110004cc100,0x6110004cc1d8)
freed by thread T11 here:
    #0 0x00010b3f06bb in __asan_memmove+0x2d1b (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:x86_64+0x546bb)
    #1 0x000171d460f7 in cc::PictureLayerTiling::RemoveTilesInRegion(cc::Region const&, bool)+0x2d7 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x1772f0f7)
    #2 0x000171d442cb in cc::PictureLayerTiling::TakeTilesAndPropertiesFrom(cc::PictureLayerTiling*, cc::Region const&)+0x12b (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x1772d2cb)
    #3 0x000171d53f64 in cc::PictureLayerTilingSet::CopyTilingsAndPropertiesFromPendingTwin(cc::PictureLayerTilingSet const*, scoped_refptr<cc::RasterSource>, cc::Region const&)+0x6d4 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x1773cf64)
    #4 0x000171d548bc in cc::PictureLayerTilingSet::UpdateTilingsToCurrentRasterSourceForActivation(scoped_refptr<cc::RasterSource>, cc::PictureLayerTilingSet const*, cc::Region const&, float, float)+0x29c (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x1773d8bc)
    #5 0x000171d0b4bc in cc::PictureLayerImpl::UpdateRasterSourceInternal(scoped_refptr<cc::RasterSource>, cc::Region*, cc::PictureLayerTilingSet const*, base::flat_map<scoped_refptr<cc::PaintWorkletInput const>, std::__Cr::pair<int, std::__Cr::optional<cc::PaintRecord>>, std::__Cr::less<void>, std::__Cr::vector<std::__Cr::pair<scoped_refptr<cc::PaintWorkletInput const>, std::__Cr::pair<int, std::__Cr::optional<cc::PaintRecord>>>, std::__Cr::allocator<std::__Cr::pair<scoped_refptr<cc::PaintWorkletInput const>, std::__Cr::pair<int, std::__Cr::optional<cc::PaintRecord>>>>>> const*, cc::DiscardableImageMap const*)+0x118c (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x176f44bc)
    #6 0x000171d09cc1 in cc::PictureLayerImpl::PushPropertiesTo(cc::LayerImpl*)+0x2f1 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x176f2cc1)
    #7 0x00017215c953 in cc::TreeSynchronizer::PushLayerProperties(cc::LayerTreeImpl*, cc::LayerTreeImpl*)+0x303 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x17b45953)
    #8 0x000172014f06 in cc::LayerTreeHostImpl::ActivateSyncTree()+0x3d6 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x179fdf06)
    #9 0x0001720f754f in cc::Scheduler::ProcessScheduledActions()+0x9bf (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x17ae054f)
    #10 0x00017210fe3c in cc::ProxyImpl::SetNeedsUpdateDisplayTreeOnImplThread()+0x13c (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x17af8e3c)
    #11 0x0001720032a1 in cc::LayerTreeHostImpl::NotifyTileStateChanged(cc::Tile const*)+0x3e1 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x179ec2a1)
    #12 0x000171db12cf in cc::TileManager::MarkTilesOutOfMemory(std::__Cr::unique_ptr<cc::RasterTilePriorityQueue, std::__Cr::default_delete<cc::RasterTilePriorityQueue>>) const+0x32f (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x1779a2cf)
    #13 0x000171d9c8d5 in cc::TileManager::CheckIfMoreTilesNeedToBePrepared()+0x875 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x177858d5)
    #14 0x000171db29c0 in base::internal::Invoker<base::internal::FunctorTraits<void (cc::TileManager::* const&)(), cc::TileManager*>, base::internal::BindState<true, true, false, void (cc::TileManager::*)(), base::internal::UnretainedWrapper<cc::TileManager, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::Run(base::internal::BindStateBase*)+0x1d0 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x1779b9c0)
    #15 0x00015bb2f7ed in base::RepeatingCallback<void ()>::Run() const &+0x17d (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x15187ed)
    #16 0x000171d75bb9 in base::internal::Invoker<base::internal::FunctorTraits<void (cc::UniqueNotifier::*&&)(), base::WeakPtr<cc::UniqueNotifier>&&>, base::internal::BindState<true, true, false, void (cc::UniqueNotifier::*)(), base::WeakPtr<cc::UniqueNotifier>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x1d9 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x1775ebb9)
    #17 0x00016cd1a8a8 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x398 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x127038a8)
    #18 0x00016cd7f9a5 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0xbd5 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x127689a5)
    #19 0x00016cd7e862 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x172 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x12767862)
    #20 0x00016cd80714 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x14 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x12769714)
    #21 0x00016cc0b447 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x1f7 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x125f4447)
    #22 0x00016cd8129b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x40b (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x1276a29b)
    #23 0x00016ccadb0e in base::RunLoop::Run(base::Location const&)+0x53e (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x12696b0e)
    #24 0x00016925db6f in blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run()+0x3ef (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0xec46b6f)
    #25 0x00016ce3616e in base::(anonymous namespace)::ThreadFunc(void*)+0x15e (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x1281f16e)
    #26 0x00010b3ed336 in __sanitizer_weak_hook_memcmp+0x34206 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:x86_64+0x51336)
    #27 0x7ff812cf8252 in _pthread_start+0x62 (/usr/lib/system/libsystem_pthread.dylib:x86_64+0x6252)
    #28 0x7ff812cf3bee in thread_start+0xe (/usr/lib/system/libsystem_pthread.dylib:x86_64+0x1bee)

previously allocated by thread T11 here:
    #0 0x00010b3f05b2 in __asan_memmove+0x2c12 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:x86_64+0x545b2)
    #1 0x00018347b5d7 in operator new(unsigned long)+0x27 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x28e645d7)
    #2 0x000171daf1c6 in cc::TileManager::CreateTile(cc::Tile::CreateInfo const&, int, int, int)+0xb6 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x177981c6)
    #3 0x000171d4264d in cc::PictureLayerTiling::CreateTile(cc::Tile::CreateInfo const&)+0x1ad (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x1772b64d)
    #4 0x000171d43012 in cc::PictureLayerTiling::CreateMissingTilesInLiveTilesRect()+0x882 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x1772c012)
    #5 0x000171d55c46 in cc::PictureLayerTilingSet::Invalidate(cc::Region const&)+0xc6 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x1773ec46)
    #6 0x000171d1de19 in cc::PictureLayerImpl::InvalidateRegionForImages(base::internal::flat_tree<int, std::__Cr::identity, std::__Cr::less<void>, std::__Cr::vector<int, std::__Cr::allocator<int>>> const&)+0x3e9 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x17706e19)
    #7 0x00017204c6c0 in cc::LayerTreeImpl::InvalidateRegionForImages(base::internal::flat_tree<int, std::__Cr::identity, std::__Cr::less<void>, std::__Cr::vector<int, std::__Cr::allocator<int>>> const&)+0x2d0 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x17a356c0)
    #8 0x000171ff457e in cc::LayerTreeHostImpl::UpdateSyncTreeAfterCommitOrImplSideInvalidation()+0x3fe (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x179dd57e)
    #9 0x000172117a40 in non-virtual thunk to cc::ProxyImpl::ScheduledActionPerformImplSideInvalidation()+0x160 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x17b00a40)
    #10 0x0001720f7278 in cc::Scheduler::ProcessScheduledActions()+0x6e8 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x17ae0278)
    #11 0x0001720ff270 in cc::Scheduler::BeginImplFrame(viz::BeginFrameArgs const&, base::TimeTicks)+0x2b0 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x17ae8270)
    #12 0x0001720fe4f8 in cc::Scheduler::BeginImplFrameWithDeadline(viz::BeginFrameArgs const&)+0x8e8 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x17ae74f8)
    #13 0x0001720fc674 in cc::Scheduler::HandlePendingBeginFrame()+0x1a4 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x17ae5674)
    #14 0x000172104027 in base::internal::Invoker<base::internal::FunctorTraits<void (cc::Scheduler::*&&)(), cc::Scheduler*>, base::internal::BindState<true, true, false, void (cc::Scheduler::*)(), base::internal::UnretainedWrapper<cc::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x147 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x17aed027)
    #15 0x00015bb30176 in void base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>::ForwardOnce<>()+0x166 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x1519176)
    #16 0x00015bb30459 in base::internal::Invoker<base::internal::FunctorTraits<void (base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>::*&&)(), base::WeakPtr<base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>>&&>, base::internal::BindState<true, true, false, void (base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>::*)(), base::WeakPtr<base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x1d9 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x1519459)
    #17 0x00016cd1a8a8 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x398 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x127038a8)
    #18 0x00016cd7f9a5 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0xbd5 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x127689a5)
    #19 0x00016cd7e862 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x172 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x12767862)
    #20 0x00016cd80714 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x14 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x12769714)
    #21 0x00016cc0b447 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x1f7 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x125f4447)
    #22 0x00016cd8129b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x40b (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x1276a29b)
    #23 0x00016ccadb0e in base::RunLoop::Run(base::Location const&)+0x53e (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x12696b0e)
    #24 0x00016925db6f in blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run()+0x3ef (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0xec46b6f)
    #25 0x00016ce3616e in base::(anonymous namespace)::ThreadFunc(void*)+0x15e (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x1281f16e)
    #26 0x00010b3ed336 in __sanitizer_weak_hook_memcmp+0x34206 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:x86_64+0x51336)
    #27 0x7ff812cf8252 in _pthread_start+0x62 (/usr/lib/system/libsystem_pthread.dylib:x86_64+0x6252)
    #28 0x7ff812cf3bee in thread_start+0xe (/usr/lib/system/libsystem_pthread.dylib:x86_64+0x1bee)

Thread T11 created by T0 here:
    #0 0x00010b3e80cd in __sanitizer_weak_hook_memcmp+0x2ef9d (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:x86_64+0x4c0cd)
    #1 0x00016ce3579e in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType)+0x2ee (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x1281e79e)
    #2 0x00016cdebb79 in base::SimpleThread::StartAsync()+0x169 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x127d4b79)
    #3 0x0001691b1fe0 in blink::Thread::CreateAndSetCompositorThread()+0x170 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0xeb9afe0)
    #4 0x00018265c7a1 in content::RenderThreadImpl::InitializeCompositorThread()+0xe1 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x280457a1)
    #5 0x000182658154 in content::RenderThreadImpl::InitializeWebKit(mojo::BinderMap*)+0x184 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x28041154)
    #6 0x000182654364 in content::RenderThreadImpl::Init()+0x9c4 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x2803d364)
    #7 0x0001826577e0 in content::RenderThreadImpl::RenderThreadImpl(base::RepeatingCallback<void ()>, std::__Cr::unique_ptr<blink::scheduler::WebThreadScheduler, std::__Cr::default_delete<blink::scheduler::WebThreadScheduler>>)+0xad0 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x280407e0)
    #8 0x0001826c2cb8 in content::RendererMain(content::MainFunctionParams)+0x538 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x280abcb8)
    #9 0x000169ee0979 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x4a9 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0xf8c9979)
    #10 0x000169ee29e6 in content::ContentMainRunnerImpl::Run()+0x536 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0xf8cb9e6)
    #11 0x000169ede634 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x654 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0xf8c7634)
    #12 0x000169edf06c in content::ContentMain(content::ContentMainParams)+0x1cc (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0xf8c806c)
    #13 0x00015a61d218 in ChromeMain+0x428 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x6218)
    #14 0x0001029adda0 in main+0x260 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer):x86_64+0x100000da0)
    #15 0x000202ec02cc  (<unknown module>)

SUMMARY: AddressSanitizer: heap-use-after-free (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x1779a411) in cc::TileManager::MarkTilesOutOfMemory(std::__Cr::unique_ptr<cc::RasterTilePriorityQueue, std::__Cr::default_delete<cc::RasterTilePriorityQueue>>) const+0x471
Shadow bytes around the buggy address:
  0x6110004cbe80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x6110004cbf00: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa
  0x6110004cbf80: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x6110004cc000: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x6110004cc080: fd fd fd fd fd fa fa fa fa fa fa fa fa fa f7 fa
=>0x6110004cc100: fd fd fd fd fd fd fd fd[fd]fd fd fd fd fd fd fd
  0x6110004cc180: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa
  0x6110004cc200: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x6110004cc280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x6110004cc300: fd fd fd fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x6110004cc380: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

==92859==ADDITIONAL INFO

==92859==Note: Please include this section with the ASan report.
Task trace:
    #0 0x000171d75661 in cc::UniqueNotifier::Schedule()+0x1a1 (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x1775e661)
    #1 0x000171dbf7ac in cc::(anonymous namespace)::DidFinishRunningAllTilesTask::RunOnWorkerThread()+0x22c (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x177a87ac)
    #2 0x00017d77568a in cc::CategorizedWorkerPoolJob::Start(int)+0x3ba (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x2315e68a)
    #3 0x00017210049d in cc::Scheduler::ScheduleBeginImplFrameDeadline()+0x6fd (/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Chromium Framework:x86_64+0x17ae949d)


Command line: `/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/133.0.6933.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer) --type=renderer --string-annotations --user-data-dir=/tmp/userdata/t12 --start-stack-profiler --no-sandbox --enable-experimental-web-platform-features --file-url-path-alias=/gen=/Users/zh1x1an1221/collections-asan-mac-chromium/mac-release_asan-mac-release-1401254/gen --lang=zh-CN --num-raster-threads=4 --enable-zero-copy --enable-gpu-memory-buffer-compositor-resources --enable-main-frame-before-activation --renderer-client-id=8 --time-ticks-at-unix-epoch=-1735672550523221 --launch-time-ticks=84814797916 --shared-files --metrics-shmem-handle=1752395122,r,10362159665685375482,12404225367890463366,2097152 --field-trial-handle=1718379636,r,1151122100166692988,13316068020523541329,262144 --enable-features=BlockInsecurePrivateNetworkRequests,BlockInsecurePrivateNetworkRequestsFromPrivate,BlockInsecurePrivateNetworkRequestsFromUnknown,CookieSameSiteConsidersRedirectChain,CreateImageBitmapOrientationNone,CriticalClientHint,DocumentPictureInPictureAPI,DocumentPolicyIncludeJSCallStacksInCrashReports,DocumentPolicyNegotiation,EnableCanvas2DLayers,ExperimentalContentSecurityPolicyFeatures,OriginIsolationHeader,PartitionedPopins,PrivateNetworkAccessRespectPreflightResults,SchemefulSameSite,StorageAccessHeaders,ThirdPartyStoragePartitioning,TreesInViz --variations-seed-version`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==92859==END OF ADDITIONAL INFO
==92859==ABORTING
Received signal 6
 [0x00016ce66352]
 [0x00016ce3a153]
 [0x00016ce661a8]
 [0x7ff812d2ee1d]
 [0x0000f743125d]
 [0x7ff812c18b19]
 [0x00010b419d38]
 [0x00010b419221]
 [0x00010b3fa883]
 [0x00010b3f99a7]
 [0x00010b3faf66]
 [0x000171db1412]
 [0x000171d9c8d6]
 [0x000171db29c1]
 [0x00015bb2f7ee]
 [0x000171d75bba]
 [0x00016cd1a8a9]
 [0x00016cd7f9a6]
 [0x00016cd7e863]
 [0x00016cd80715]
 [0x00016cc0b448]
 [0x00016cd8129c]
 [0x00016ccadb0f]
 [0x00016925db70]
 [0x00016ce3616f]
 [0x00010b3ed337]
 [0x7ff812cf8253]
 [0x7ff812cf3bef]
[end of stack trace]

```

### zh...@gmail.com (2025-01-01)

And I tested the latest version of `Linux`（I think Windows can also trigger it,because I have analyzed the entire path to trigger the vulnerability and did not see any code related to the operating system, but I don't have a Windows device yet）, and it can also be reproduced. If you think it is more convenient to use Linux, you can download `asan linux 1401257` and repeat the steps I mentioned before.

### pe...@google.com (2025-01-02)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2025-01-02)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### zh...@gmail.com (2025-01-07)

Friendly ping,any update?

### zh...@gmail.com (2025-01-14)

Friendly ping,any update?

### pe...@google.com (2025-01-16)

vmpstr: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### zh...@gmail.com (2025-01-20)

Friengly ping,hmmmmmm, it's been 3 weeks since I submitted the bug report, is there any progress?

### pe...@google.com (2025-01-31)

vmpstr: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### xi...@chromium.org (2025-02-03)

[secondary security shepherd] Unfortunately the original author of the culprit CL (<https://crrev.com/c/5783760>) is no longer available. Adding the new owner of the issue (<https://crbug.com/40902503>) to take a look.

### zh...@gmail.com (2025-02-20)

Friendly ping?

### vm...@chromium.org (2025-02-26)

Thank you for the information, this is a good find.

--enable-features=TreesInViz is under development and isn't shipped in any product currently. Does this vulnerability only occur with this flag, or is that just an easy way to provoke an error because TreesInViz can easily run out of tile memory? The original report doesn't seem to use this flag.

### zh...@gmail.com (2025-02-27)

This UAF bug requires TreesInViz to be enabled to trigger.

### bl...@chromium.org (2025-02-28)

Thanks! This is then not a P1 as we're not shipping TreesInViz in production.

zmo@, assigning to you to ensure that we track this bug as a blocker for Finching TreesInViz on canary (note: not assigning to you to actually do the work as such :).

### ch...@google.com (2025-03-03)

We commit ourselves to a 60 day deadline for fixing for s1 severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

### bl...@chromium.org (2025-03-03)

Moved down to S2 per [comment#23](https://issues.chromium.org/issues/386992811#comment23).

### pg...@google.com (2025-03-12)

Keeping severity as S1 as a UaF in the renderer process

Updating impact to None as TreesInViz is not shipped in production and off by default

### zm...@chromium.org (2025-03-27)

blocking TreesInViz meta bug

### zh...@gmail.com (2025-04-21)

Do we have any new progress on this bug?

### th...@chromium.org (2025-04-25)

[secondary shepherd] I don't see any usages of TreesInViz in a field trial config or in ongoing experiments, and it is still marked as disabled by default. So the Security_Impact-None hotlist still seems valid, and there is no immediate action needed.

### zh...@gmail.com (2025-05-30)

Sorry, what I want to say is that the UAF in this report needs to be followed up and fixed. When it has been fixed, you can close this report and send reward-topanel. This is what I think is the common process for reporting security vulnerabilities. However, this time there was no reply after a long delay. Maybe the frequent changes in the code have caused the vulnerability to be fixed?

Anyway, I would like to ask, can you confirm that the UAF has been fixed? If not, then it should be fixed like other security reports, and then closed for reward.

### el...@chromium.org (2025-07-03)

Secondary shepherd: zmo@, where are we on this?

### bl...@chromium.org (2025-07-10)

Mo and I discussed. We're ready to take TreesInViz to canary now, so he's going to make sure that this is fixed before we flip the switch on that.

### dx...@google.com (2025-07-11)

Project: chromium/src  

Branch:  main  

Author:  Zhenyao Mo [zmo@chromium.org](mailto:zmo@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6724999>

Avoid calling SetNeedsRedraw for each queue inside MarkTilesOOM.

---


Expand for full commit details
```
     
    If we trigger SetNeedsRedraw() inside the loop above, we may end up 
    triggering Scheduler::ProcessScheduledActions(), which is inefficient. 
    Worse, it may in turn trigger ActivateSyncTree() and other actions that 
    remove tiles in the queue, leading to UAF. 
     
    TEST=bots 
     
    Bug: 386992811 
    Change-Id: I02ffd705ff6a04a680a8e093c227aa645240354c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6724999 
    Commit-Queue: Zhenyao Mo <zmo@chromium.org> 
    Reviewed-by: Vasiliy Telezhnikov <vasilyt@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1485589}

```

---

Files:

- M `cc/input/scroll_elasticity_helper.cc`
- M `cc/test/fake_layer_tree_host_impl.cc`
- M `cc/test/fake_layer_tree_host_impl.h`
- M `cc/test/fake_tile_manager_client.h`
- M `cc/test/layer_tree_test.cc`
- M `cc/tiles/tile_manager.cc`
- M `cc/tiles/tile_manager_client.h`
- M `cc/trees/layer_tree_host_impl.cc`
- M `cc/trees/layer_tree_host_impl.h`
- M `cc/trees/layer_tree_host_impl_unittest.cc`
- M `cc/trees/layer_tree_host_perftest.cc`
- M `cc/trees/layer_tree_host_unittest.cc`
- M `cc/trees/layer_tree_host_unittest_copyrequest.cc`
- M `cc/trees/layer_tree_host_unittest_damage.cc`
- M `cc/trees/layer_tree_host_unittest_picture.cc`
- M `cc/trees/layer_tree_host_unittest_scroll.cc`
- M `cc/trees/layer_tree_impl.cc`

---

Hash: 94b949573d9e12e2c6fd97cf9986b7cbbc32dddf  

Date: Fri Jul 11 15:40:27 2025


---

### zm...@chromium.org (2025-07-11)

reporter: can you verify if the original UAF is gone after the above fix?

### zh...@gmail.com (2025-07-11)

No problem, give me some time. I need to compile a new Chromium to test.

### zh...@gmail.com (2025-07-12)

I tested it on `791eddc5a6efdc1b0702c697cc95f9aa5f0001ba`, which contains the patch: <https://chromium-review.googlesource.com/c/chromium/src/+/6724999>

UAF does not trigger, thanks for the fix.

### zm...@chromium.org (2025-07-15)

Thank you for reporting the bug. It's a pretty deeply hidden UAF case. It won't be easy to identify without the detailed report.

### zh...@gmail.com (2025-07-15)

You're welcome, providing detailed analysis in the report also makes me understand the lifecycle management of C++ code better, which is very helpful for both of us

### sp...@google.com (2025-07-24)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
$10,000 for a high-quality report of memory corruption in a sandboxed process + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### zh...@gmail.com (2025-07-25)

deleted

### ch...@google.com (2025-10-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> $10,000 for a high-quality report of memory corruption in a sandboxed process + $1,000 bisect bonus

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/386992811)*
