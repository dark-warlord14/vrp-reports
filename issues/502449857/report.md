# Security: Heap-use-after-free in CastActivityManager::FindActivityForSessionJoin

| Field | Value |
|-------|-------|
| **Issue ID** | [502449857](https://issues.chromium.org/issues/502449857) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Cast |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 146.0.0.0 |
| **Reporter** | me...@gmail.com |
| **Assignee** | mu...@google.com |
| **Created** | 2026-04-14 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

1. Apply `change.txt` to Chromium and compile with ASAN enabled.
2. Start the mDNS advertisement: python3 fake\_cast.py
3. Start the fake Cast receiver: python3 fake\_castd.py
4. Launch Chrome: ./out/asan/chrome --remote-debugging-port=9222 --user-data-dir=/tmp/noexist poc.html
5. In a separate terminal, run the CDP trigger: python3 cdp\_trigger.py
6. The browser process crashes with UAF.

# Problem Description

## Introduction

The root cause is that `AddMirroringActivity()` calls `activities_.insert_or_assign(route_id, unique_ptr<MirroringActivity>)` which **destroys any existing `AppActivity`** stored under the same route ID via `unique_ptr` reset, but **never erases the stale raw pointer** from `app_activities_`. `FindActivityForSessionJoin()` subsequently iterates `app_activities_` and dereferences `entry.second->session_id()` on every entry — including the now-freed `AppActivity` — producing a heap-use-after-free. By contrast, `AddAppActivity()` (the symmetric operation that goes in the other direction) was separately patched against route-ID collision via a comment referencing [crbug.com/500091052](https://crbug.com/500091052), but `AddMirroringActivity()` was left unprotected against the cross-type collision where a mirroring session overwrites an app session.

Note: `change.txt` for this PoC contains two patches:

- `cast_activity_manager.cc`: artificially forces the cross-type collision in `DoLaunchSession` by calling `AddAppActivity` then `AddMirroringActivity` for the same route when the source is a streaming app, then immediately calls `FindActivityForSessionJoin` to produce the crash. This exposes the latent bug — in production the same race can be reached via `AddNonLocalActivity` or a session type change on a live route.
- `cast_auth_util.cc`: bypasses Cast device certificate verification so that the Python fake receiver (fake\_castd.py) is accepted as a valid Cast sink without requiring real Chromecast hardware.

# Additional Comments

## Analysis

### Vulnerability Summary

`CastActivityManager` maintains two parallel data structures **[1]**:

```
// Owns all activity objects.
base::flat_map<MediaRoute::Id, std::unique_ptr<CastActivity>> activities_;

// Subset of activities_ that are AppActivity instances; raw pointers only.
std::map<MediaRoute::Id, AppActivity*> app_activities_;

```

`AddAppActivity()` **[2]** registers an entry in both maps:

```
AppActivity* CastActivityManager::AddAppActivity(const MediaRoute& route,
                                                 const std::string& app_id) {
  auto activity = std::make_unique<AppActivity>(route, app_id, ...);
  auto* const activity_ptr = activity.get();
  activities_.insert_or_assign(route.media_route_id(), std::move(activity));
  app_activities_[route.media_route_id()] = activity_ptr;  // [A] raw ptr stored
  return activity_ptr;
}

```

`AddMirroringActivity()` **[3]** replaces the entry in `activities_` but **never touches `app_activities_`**:

```
CastActivity* CastActivityManager::AddMirroringActivity(...) {
  auto activity = std::make_unique<MirroringActivity>(route, app_id, ...);
  activities_.insert_or_assign(route.media_route_id(), std::move(activity));
  // [B] insert_or_assign destroys the old unique_ptr<AppActivity> → FREE
  // [C] app_activities_[route_id] is NEVER erased → dangling raw pointer
  return activity_ptr;
}

```

`FindActivityForSessionJoin()` **[4]** iterates `app_activities_` and dereferences every entry:

```
AppActivity* CastActivityManager::FindActivityForSessionJoin(
    const CastMediaSource& cast_source,
    const std::string& presentation_id) {
  ...
  auto it = std::ranges::find(
      app_activities_, session_id,
      [](const auto& entry) { return entry.second->session_id(); }); // [D] UAF: reads freed AppActivity
  ...
}

```

If `AddMirroringActivity` is called for a route that already has an `AppActivity` registered via `AddAppActivity`, the sequence [A] → [B] → [C] → [D] produces a heap-use-after-free at step [D].

### Production Reachability via AddNonLocalActivity

The PoC patch forces the collision synchronously inside `DoLaunchSession`, but the same condition is reachable in unmodified Chrome via `AddNonLocalActivity()` **[5]**, which is invoked from `OnSessionAddedOrUpdated()` whenever the Cast receiver reports a session update over the Cast channel.

The route ID is a deterministic string derived from `presentation_id`, `sink_id`, and `source_id`. Consider the following sequence on an unpatched build:

1. A tab-streaming session is initiated locally. `DoLaunchSession` dispatches `ContainsStreamingApp() == false` for the initial source type and calls `AddAppActivity(route, app_id)`, storing the `AppActivity*` in both `activities_` and `app_activities_`.
2. The receiver transitions the session to a mirroring type (e.g. the app on the receiver side switches its session type), and sends a session-updated message. Chrome's `OnSessionAddedOrUpdated` **[5]** receives this, classifies the updated session as a mirroring session, and calls `AddMirroringActivity` for the same route ID.
3. `AddMirroringActivity` calls `activities_.insert_or_assign(route_id, std::move(mirroring_activity))`, which destroys the old `unique_ptr<AppActivity>` and frees the `AppActivity` object. The entry in `app_activities_` is not erased — it now holds a dangling pointer to freed memory.
4. Any subsequent call to `FindActivityForSessionJoin` — triggered when a second Cast source attempts to join an existing session by presentation ID — iterates `app_activities_` and dereferences `entry.second->session_id()` on the freed object, producing the heap-use-after-free.

The cross-type transition in step 2 is a normal part of the Cast session lifecycle and does not require attacker control beyond the ability to influence the session type reported by the receiver (e.g. via a rogue Cast device on the local network, since Cast sink discovery is unauthenticated at the mDNS level).

## References

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/media/router/providers/cast/cast_activity_manager.h>

[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/media/router/providers/cast/cast_activity_manager.cc;l=534>

[3] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/media/router/providers/cast/cast_activity_manager.cc;l=550>

[4] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/media/router/providers/cast/cast_activity_manager.cc;l=272>

[5] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/media/router/providers/cast/cast_activity_manager.cc;l=789>

# Summary

Security: Heap-use-after-free in CastActivityManager::FindActivityForSessionJoin

# Custom Questions

#### Type of crash:

browser

#### Crash state:

=================================================================
==261776==ERROR: AddressSanitizer: heap-use-after-free on address 0x7c85a4c80ce0 at pc 0x558e10f07224 bp 0x7b25912464f0 sp 0x7b25912464e8
READ of size 1 at 0x7c85a4c80ce0 thread T12 (Chrome\_IOThread)
#0 0x558e10f07223 in media\_router::CastActivityManager::FindActivityForSessionJoin(media\_router::CastMediaSource const&, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&) gen/third\_party/libc++/src/include/optional:447:96
#1 0x558e10f04c0f in media\_router::CastActivityManager::DoLaunchSession(media\_router::CastActivityManager::DoLaunchSessionParams) chrome/browser/media/router/providers/cast/cast\_activity\_manager.cc:240:5
#2 0x558e10f041c4 in media\_router::CastActivityManager::LaunchSessionParsed(media\_router::CastMediaSource const&, media\_router::MediaSinkInternal const&, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&, url::Origin const&, base::IdType<content::FrameTreeNodeIdTag, int, -1, 1, 0>, base::OnceCallback<void (std::\_\_Cr::optional<media\_router::MediaRoute> const&, mojo::StructPtr<media\_router::mojom::RoutePresentationConnection>, std::\_\_Cr::optional<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>> const&, media\_router::mojom::RouteRequestResultCode)>, base::expected<base::Value, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>>) chrome/browser/media/router/providers/cast/cast\_activity\_manager.cc:208:3
#3 0x558e10f0311a in media\_router::CastActivityManager::LaunchSession(media\_router::CastMediaSource const&, media\_router::MediaSinkInternal const&, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&, url::Origin const&, base::IdType<content::FrameTreeNodeIdTag, int, -1, 1, 0>, base::OnceCallback<void (std::\_\_Cr::optional<media\_router::MediaRoute> const&, mojo::StructPtr<media\_router::mojom::RoutePresentationConnection>, std::\_\_Cr::optional<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>> const&, media\_router::mojom::RouteRequestResultCode)>) chrome/browser/media/router/providers/cast/cast\_activity\_manager.cc:138:5
#4 0x558e10efa0df in media\_router::CastMediaRouteProvider::CreateRoute(std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&, url::Origin const&, int, base::TimeDelta, base::OnceCallback<void (std::\_\_Cr::optional<media\_router::MediaRoute> const&, mojo::StructPtr<media\_router::mojom::RoutePresentationConnection>, std::\_\_Cr::optional<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>> const&, media\_router::mojom::RouteRequestResultCode)>) chrome/browser/media/router/providers/cast/cast\_media\_route\_provider.cc:215:22
#5 0x558e08910317 in media\_router::mojom::MediaRouteProviderStubDispatch::AcceptWithResponder(media\_router::mojom::MediaRouteProvider\*, mojo::Message\*, std::\_\_Cr::unique\_ptr<mojo::MessageReceiverWithStatus, std::\_\_Cr::default\_delete[mojo::MessageReceiverWithStatus](javascript:void(0);)>) gen/components/media\_router/common/mojom/media\_router.mojom.cc:3005:13
#6 0x7f2628eb1fee in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:1036:56
#7 0x7f2628ec93eb in mojo::MessageDispatcher::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/message\_dispatcher.cc:44:19
#8 0x7f2628eb78f4 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:747:20
#9 0x7f2628ed89ce in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) mojo/public/cpp/bindings/lib/multiplex\_router.cc:1204:42
#10 0x7f2628ed71fd in mojo::internal::MultiplexRouter::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/multiplex\_router.cc:790:7
#11 0x7f2628ec93eb in mojo::MessageDispatcher::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/message\_dispatcher.cc:44:19
#12 0x7f2628e9dc8f in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase[mojo::MessageHandle](javascript:void(0);)) mojo/public/cpp/bindings/lib/connector.cc:567:49
#13 0x7f2628e9f4de in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:628:14
#14 0x7f2628e9ef77 in mojo::Connector::OnWatcherHandleReady(char const\*, unsigned int) mojo/public/cpp/bindings/lib/connector.cc:453:3
#15 0x7f2628ea1b51 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::\* const&)(char const\*, unsigned int), mojo::Connector\*, char const\* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase\*, unsigned int) base/functional/bind\_internal.h:740:12
#16 0x7f2628ea11fe in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const & base/functional/callback.h:346:12
#17 0x7f2628ea0fb4 in base::internal::Invoker<base::internal::FunctorTraits<void (\* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&) base/functional/bind\_internal.h:673:12
#18 0x7f262710c450 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const & base/functional/callback.h:346:12
#19 0x7f262710be2b in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple\_watcher.cc:286:14
#20 0x7f262710ce94 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);)&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase\*) base/functional/bind\_internal.h:740:12
#21 0x7f2628714209 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
#22 0x7f262878e750 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) base/task/common/task\_annotator.h:112:5
#23 0x7f262878d726 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:336:40
#24 0x7f262893e6c1 in base::MessagePumpEpoll::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_epoll.cc:224:55
#25 0x7f262878fda3 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:640:12
#26 0x7f262867f652 in base::RunLoop::Run(base::Location const&) base/run\_loop.cc:135:14
#27 0x7f2628827ca2 in base::Thread::Run(base::RunLoop\*) base/threading/thread.cc:356:13
#28 0x7f260a29fe3f in content::BrowserProcessIOThread::IOThreadRun(base::RunLoop\*) content/browser/browser\_process\_io\_thread.cc:104:11
#29 0x7f2628828205 in base::Thread::ThreadMain() base/threading/thread.cc:426:3
#30 0x7f262888cfdc in base::(anonymous namespace)::ThreadFunc(void\*) base/threading/platform\_thread\_posix.cc:102:13
#31 0x558e04792486 in asan\_thread\_start(void\*) asan\_interceptors.cpp

0x7c85a4c80ce0 is located 352 bytes inside of 640-byte region [0x7c85a4c80b80,0x7c85a4c80e00)
freed by thread T12 (Chrome\_IOThread) here:
#0 0x558e047ce842 in operator delete(void\*, unsigned long) (/home/krace/fuzz/chromium/src/out/ui/chrome+0x67e9842) (BuildId: 2d2b77c81d15022a)
#1 0x558e10f1070c in std::\_\_Cr::pair<std::\_\_Cr::\_\_wrap\_iter<std::\_\_Cr::pair<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>, std::\_\_Cr::unique\_ptr<media\_router::CastActivity, std::\_\_Cr::default\_delete<media\_router::CastActivity>>>*>, bool> base::flat\_map<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>, std::\_\_Cr::unique\_ptr<media\_router::CastActivity, std::\_\_Cr::default\_delete<media\_router::CastActivity>>, std::\_\_Cr::less<void>, std::\_\_Cr::vector<std::\_\_Cr::pair<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>, std::\_\_Cr::unique\_ptr<media\_router::CastActivity, std::\_\_Cr::default\_delete<media\_router::CastActivity>>>, std::\_\_Cr::allocator<std::\_\_Cr::pair<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>, std::\_\_Cr::unique\_ptr<media\_router::CastActivity, std::\_\_Cr::default\_delete<media\_router::CastActivity>>>>>>::insert\_or\_assign<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>, std::\_\_Cr::unique\_ptr<media\_router::MirroringActivity, std::\_\_Cr::default\_delete<media\_router::MirroringActivity>>>(std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&, std::\_\_Cr::unique\_ptr<media\_router::MirroringActivity, std::\_\_Cr::default\_delete<media\_router::MirroringActivity>>&&) gen/third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:74:5
#2 0x558e10f06d2f in media\_router::CastActivityManager::AddMirroringActivity(media\_router::MediaRoute const&, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&, base::IdType<content::FrameTreeNodeIdTag, int, -1, 1, 0>, media\_router::CastSinkExtraData const&) chrome/browser/media/router/providers/cast/cast\_activity\_manager.cc:576:15
#3 0x558e10f04b61 in media\_router::CastActivityManager::DoLaunchSession(media\_router::CastActivityManager::DoLaunchSessionParams) chrome/browser/media/router/providers/cast/cast\_activity\_manager.cc:232:9
#4 0x558e10f041c4 in media\_router::CastActivityManager::LaunchSessionParsed(media\_router::CastMediaSource const&, media\_router::MediaSinkInternal const&, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&, url::Origin const&, base::IdType<content::FrameTreeNodeIdTag, int, -1, 1, 0>, base::OnceCallback<void (std::\_\_Cr::optional<media\_router::MediaRoute> const&, mojo::StructPtr<media\_router::mojom::RoutePresentationConnection>, std::\_\_Cr::optional<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>> const&, media\_router::mojom::RouteRequestResultCode)>, base::expected<base::Value, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>>) chrome/browser/media/router/providers/cast/cast\_activity\_manager.cc:208:3
#5 0x558e10f0311a in media\_router::CastActivityManager::LaunchSession(media\_router::CastMediaSource const&, media\_router::MediaSinkInternal const&, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&, url::Origin const&, base::IdType<content::FrameTreeNodeIdTag, int, -1, 1, 0>, base::OnceCallback<void (std::\_\_Cr::optional<media\_router::MediaRoute> const&, mojo::StructPtr<media\_router::mojom::RoutePresentationConnection>, std::\_\_Cr::optional<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>> const&, media\_router::mojom::RouteRequestResultCode)>) chrome/browser/media/router/providers/cast/cast\_activity\_manager.cc:138:5
#6 0x558e10efa0df in media\_router::CastMediaRouteProvider::CreateRoute(std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&, url::Origin const&, int, base::TimeDelta, base::OnceCallback<void (std::\_\_Cr::optional<media\_router::MediaRoute> const&, mojo::StructPtr<media\_router::mojom::RoutePresentationConnection>, std::\_\_Cr::optional<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>> const&, media\_router::mojom::RouteRequestResultCode)>) chrome/browser/media/router/providers/cast/cast\_media\_route\_provider.cc:215:22
#7 0x558e08910317 in media\_router::mojom::MediaRouteProviderStubDispatch::AcceptWithResponder(media\_router::mojom::MediaRouteProvider*, mojo::Message\*, std::\_\_Cr::unique\_ptr<mojo::MessageReceiverWithStatus, std::\_\_Cr::default\_delete[mojo::MessageReceiverWithStatus](javascript:void(0);)>) gen/components/media\_router/common/mojom/media\_router.mojom.cc:3005:13
#8 0x7f2628eb1fee in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:1036:56
#9 0x7f2628ec93eb in mojo::MessageDispatcher::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/message\_dispatcher.cc:44:19
#10 0x7f2628eb78f4 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:747:20
#11 0x7f2628ed89ce in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) mojo/public/cpp/bindings/lib/multiplex\_router.cc:1204:42
#12 0x7f2628ed71fd in mojo::internal::MultiplexRouter::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/multiplex\_router.cc:790:7
#13 0x7f2628ec93eb in mojo::MessageDispatcher::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/message\_dispatcher.cc:44:19
#14 0x7f2628e9dc8f in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase[mojo::MessageHandle](javascript:void(0);)) mojo/public/cpp/bindings/lib/connector.cc:567:49
#15 0x7f2628e9f4de in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:628:14
#16 0x7f2628e9ef77 in mojo::Connector::OnWatcherHandleReady(char const\*, unsigned int) mojo/public/cpp/bindings/lib/connector.cc:453:3
#17 0x7f2628ea1b51 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::\* const&)(char const\*, unsigned int), mojo::Connector\*, char const\* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase\*, unsigned int) base/functional/bind\_internal.h:740:12
#18 0x7f2628ea11fe in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const & base/functional/callback.h:346:12
#19 0x7f2628ea0fb4 in base::internal::Invoker<base::internal::FunctorTraits<void (\* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&) base/functional/bind\_internal.h:673:12
#20 0x7f262710c450 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const & base/functional/callback.h:346:12
#21 0x7f262710be2b in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple\_watcher.cc:286:14
#22 0x7f262710ce94 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);)&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase\*) base/functional/bind\_internal.h:740:12
#23 0x7f2628714209 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
#24 0x7f262878e750 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) base/task/common/task\_annotator.h:112:5
#25 0x7f262878d726 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:336:40
#26 0x7f262893e6c1 in base::MessagePumpEpoll::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_epoll.cc:224:55
#27 0x7f262878fda3 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:640:12
#28 0x7f262867f652 in base::RunLoop::Run(base::Location const&) base/run\_loop.cc:135:14
#29 0x7f2628827ca2 in base::Thread::Run(base::RunLoop\*) base/threading/thread.cc:356:13

previously allocated by thread T12 (Chrome\_IOThread) here:
#0 0x558e047cdc3d in operator new(unsigned long) (/home/krace/fuzz/chromium/src/out/ui/chrome+0x67e8c3d) (BuildId: 2d2b77c81d15022a)
#1 0x558e10f060e5 in media\_router::CastActivityManager::AddAppActivity(media\_router::MediaRoute const&, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&) gen/third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:756:26
#2 0x558e10f04b27 in media\_router::CastActivityManager::DoLaunchSession(media\_router::CastActivityManager::DoLaunchSessionParams) chrome/browser/media/router/providers/cast/cast\_activity\_manager.cc:229:5
#3 0x558e10f041c4 in media\_router::CastActivityManager::LaunchSessionParsed(media\_router::CastMediaSource const&, media\_router::MediaSinkInternal const&, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&, url::Origin const&, base::IdType<content::FrameTreeNodeIdTag, int, -1, 1, 0>, base::OnceCallback<void (std::\_\_Cr::optional<media\_router::MediaRoute> const&, mojo::StructPtr<media\_router::mojom::RoutePresentationConnection>, std::\_\_Cr::optional<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>> const&, media\_router::mojom::RouteRequestResultCode)>, base::expected<base::Value, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>>) chrome/browser/media/router/providers/cast/cast\_activity\_manager.cc:208:3
#4 0x558e10f0311a in media\_router::CastActivityManager::LaunchSession(media\_router::CastMediaSource const&, media\_router::MediaSinkInternal const&, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&, url::Origin const&, base::IdType<content::FrameTreeNodeIdTag, int, -1, 1, 0>, base::OnceCallback<void (std::\_\_Cr::optional<media\_router::MediaRoute> const&, mojo::StructPtr<media\_router::mojom::RoutePresentationConnection>, std::\_\_Cr::optional<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>> const&, media\_router::mojom::RouteRequestResultCode)>) chrome/browser/media/router/providers/cast/cast\_activity\_manager.cc:138:5
#5 0x558e10efa0df in media\_router::CastMediaRouteProvider::CreateRoute(std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&, url::Origin const&, int, base::TimeDelta, base::OnceCallback<void (std::\_\_Cr::optional<media\_router::MediaRoute> const&, mojo::StructPtr<media\_router::mojom::RoutePresentationConnection>, std::\_\_Cr::optional<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>> const&, media\_router::mojom::RouteRequestResultCode)>) chrome/browser/media/router/providers/cast/cast\_media\_route\_provider.cc:215:22
#6 0x558e08910317 in media\_router::mojom::MediaRouteProviderStubDispatch::AcceptWithResponder(media\_router::mojom::MediaRouteProvider\*, mojo::Message\*, std::\_\_Cr::unique\_ptr<mojo::MessageReceiverWithStatus, std::\_\_Cr::default\_delete[mojo::MessageReceiverWithStatus](javascript:void(0);)>) gen/components/media\_router/common/mojom/media\_router.mojom.cc:3005:13
#7 0x7f2628eb1fee in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:1036:56
#8 0x7f2628ec93eb in mojo::MessageDispatcher::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/message\_dispatcher.cc:44:19
#9 0x7f2628eb78f4 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:747:20
#10 0x7f2628ed89ce in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) mojo/public/cpp/bindings/lib/multiplex\_router.cc:1204:42
#11 0x7f2628ed71fd in mojo::internal::MultiplexRouter::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/multiplex\_router.cc:790:7
#12 0x7f2628ec93eb in mojo::MessageDispatcher::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/message\_dispatcher.cc:44:19
#13 0x7f2628e9dc8f in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase[mojo::MessageHandle](javascript:void(0);)) mojo/public/cpp/bindings/lib/connector.cc:567:49
#14 0x7f2628e9f4de in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:628:14
#15 0x7f2628e9ef77 in mojo::Connector::OnWatcherHandleReady(char const\*, unsigned int) mojo/public/cpp/bindings/lib/connector.cc:453:3
#16 0x7f2628ea1b51 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::\* const&)(char const\*, unsigned int), mojo::Connector\*, char const\* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase\*, unsigned int) base/functional/bind\_internal.h:740:12
#17 0x7f2628ea11fe in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const & base/functional/callback.h:346:12
#18 0x7f2628ea0fb4 in base::internal::Invoker<base::internal::FunctorTraits<void (\* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&) base/functional/bind\_internal.h:673:12
#19 0x7f262710c450 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const & base/functional/callback.h:346:12
#20 0x7f262710be2b in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple\_watcher.cc:286:14
#21 0x7f262710ce94 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);)&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase\*) base/functional/bind\_internal.h:740:12
#22 0x7f2628714209 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
#23 0x7f262878e750 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) base/task/common/task\_annotator.h:112:5
#24 0x7f262878d726 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:336:40
#25 0x7f262893e6c1 in base::MessagePumpEpoll::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_epoll.cc:224:55
#26 0x7f262878fda3 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:640:12
#27 0x7f262867f652 in base::RunLoop::Run(base::Location const&) base/run\_loop.cc:135:14
#28 0x7f2628827ca2 in base::Thread::Run(base::RunLoop\*) base/threading/thread.cc:356:13
#29 0x7f260a29fe3f in content::BrowserProcessIOThread::IOThreadRun(base::RunLoop\*) content/browser/browser\_process\_io\_thread.cc:104:11

Thread T12 (Chrome\_IOThread) created by T0 (chrome) here:
#0 0x558e047782b1 in pthread\_create (/home/krace/fuzz/chromium/src/out/ui/chrome+0x67932b1) (BuildId: 2d2b77c81d15022a)
#1 0x7f262888c69c in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate\*, base::PlatformThreadHandle\*, base::ThreadType, base::MessagePumpType) base/threading/platform\_thread\_posix.cc:153:13
#2 0x7f262882652b in base::Thread::StartWithOptions(base::Thread::Options) base/threading/thread.cc:232:26
#3 0x7f260baa1340 in content::BrowserTaskExecutor::CreateIOThread() content/browser/scheduler/browser\_task\_executor.cc:304:19
#4 0x7f260d739653 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content\_main\_runner\_impl.cc:1282:42
#5 0x7f260d7383d6 in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner\_impl.cc:1150:12
#6 0x7f260d732af3 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) content/app/content\_main.cc:356:36
#7 0x7f260d732e7a in content::ContentMain(content::ContentMainParams) content/app/content\_main.cc:369:10
#8 0x558e047cfb95 in ChromeMain chrome/app/chrome\_main.cc:194:12
#9 0x7f25b429f082 in \_\_libc\_start\_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-use-after-free gen/third\_party/libc++/src/include/optional:447:96 in media\_router::CastActivityManager::FindActivityForSessionJoin(media\_router::CastMediaSource const&, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&)
Shadow bytes around the buggy address:
0x7c85a4c80a00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
0x7c85a4c80a80: 00 00 00 00 00 00 fa fa fa fa fa fa fa fa fa fa
0x7c85a4c80b00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
0x7c85a4c80b80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x7c85a4c80c00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x7c85a4c80c80: fd fd fd fd fd fd fd fd fd fd fd fd[fd]fd fd fd
0x7c85a4c80d00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x7c85a4c80d80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x7c85a4c80e00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
0x7c85a4c80e80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
0x7c85a4c80f00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
Addressable: 00
Partially addressable: 01 02 03 04 05 06 07
Heap left redzone: fa
Freed heap region: fd
Stack left redzone: f1
Stack mid redzone: f2
Stack right redzone: f3
Stack after return: f5
Stack use after scope: f8
Global redzone: f9
Global init order: f6
Poisoned by user: f7
Container overflow: fc
Array cookie: ac
Intra object redzone: bb
ASan internal: fe
Left alloca redzone: ca
Right alloca redzone: cb

==261776==ADDITIONAL INFO

==261776==Note: Please include this section with the ASan report.
Task trace:
#0 0x7f262710c84a in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) mojo/public/cpp/system/simple\_watcher.cc:103:13
#1 0x7f260a524687 in content::ServerWrapper::OnWebSocketMessage(int, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>) content/browser/devtools/devtools\_http\_handler.cc:531:7

Command line: `./out/ui/chrome --remote-debugging-port=9222 --flag-switches-begin --enable-experimental-web-platform-features --flag-switches-end --ozone-platform=x11 tmp/finding10.html`

MiraclePtr Status: NOT PROTECTED
No raw\_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to <https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md> for details.

==261776==END OF ADDITIONAL INFO

==261776==ABORTING

#### Reporter credit:

Krace

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [fake_cast.py](attachments/fake_cast.py) (text/x-python, 2.7 KB)
- [fake_castd.py](attachments/fake_castd.py) (text/x-python, 10.4 KB)
- [poc.html](attachments/poc.html) (text/html, 791 B)
- [cdp_trigger.py](attachments/cdp_trigger.py) (text/x-python, 5.2 KB)
- [change.txt](attachments/change.txt) (text/plain, 3.9 KB)

## Timeline

### ma...@google.com (2026-04-15)

[security shepherd] Triage following 500091052

apaseltiner, PTAL?

### ch...@google.com (2026-04-16)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-16)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-04-17)

Project: chromium/src  

Branch:  main  

Author:  Muyao Xu [muyaoxu@google.com](mailto:muyaoxu@google.com)  

Link:    <https://chromium-review.googlesource.com/7766193>

[MediaRouter] Fix UAF in CastActivityManager::AddMirroringActivity

---


Expand for full commit details
```
     
    When AddMirroringActivity is called on an existing route ID, it 
    overwrites the entry in activities_ using insert_or_assign(), destroying 
    the old CastActivity (which could be an AppActivity). This left the raw 
    pointer in app_activities_ dangling, causing a Use-After-Free if 
    accessed later. This CL adds app_activities_.erase() to safely clear 
    the raw pointer when the owning unique_ptr is replaced. 
     
    Bug: 502449857 
    Change-Id: Id320a57560898dd340760be9f7821512321ace56 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7766193 
    Reviewed-by: Jordan Bayles <jophba@chromium.org> 
    Commit-Queue: Muyao Xu <muyaoxu@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1616219}

```

---

Files:

- M `chrome/browser/media/router/providers/cast/cast_activity_manager.cc`
- M `chrome/browser/media/router/providers/cast/cast_activity_manager.h`
- M `chrome/browser/media/router/providers/cast/cast_activity_manager_unittest.cc`

---

Hash: [a1d328a102b58e941cab8fdcdc74749358d8084b](https://chromiumdash.appspot.com/commit/a1d328a102b58e941cab8fdcdc74749358d8084b)  

Date: Fri Apr 17 00:27:56 2026


---

### ch...@google.com (2026-04-18)

Requesting merge to M146 because latest trunk commit (1616219) appears to be after M146 branch point (1582197).

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to M147 because latest trunk commit (1616219) appears to be after M147 branch point (1596535).

Requesting merge to M148 because latest trunk commit (1616219) appears to be after M148 branch point (1610480).

### ch...@google.com (2026-04-18)

**M146** merge request created. **Please update [crbug/503979723](https://crbug.com/503979723) to have this merge reviewed.**

### ch...@google.com (2026-04-18)

**M147** merge request created. **Please update [crbug/503979526](https://crbug.com/503979526) to have this merge reviewed.**

### ch...@google.com (2026-04-18)

**M148** merge request created. **Please update [crbug/503979821](https://crbug.com/503979821) to have this merge reviewed.**

### dx...@google.com (2026-04-21)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Muyao Xu [muyaoxu@google.com](mailto:muyaoxu@google.com)  

Link:    <https://chromium-review.googlesource.com/7783789>

[M147] [MediaRouter] Fix UAF in CastActivityManager::AddMirroringActivity

---


Expand for full commit details
```
     
    Original change's description: 
    > [MediaRouter] Fix UAF in CastActivityManager::AddMirroringActivity 
    > 
    > When AddMirroringActivity is called on an existing route ID, it 
    > overwrites the entry in activities_ using insert_or_assign(), destroying 
    > the old CastActivity (which could be an AppActivity). This left the raw 
    > pointer in app_activities_ dangling, causing a Use-After-Free if 
    > accessed later. This CL adds app_activities_.erase() to safely clear 
    > the raw pointer when the owning unique_ptr is replaced. 
    > 
    > Bug: 502449857 
    > Change-Id: Id320a57560898dd340760be9f7821512321ace56 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7766193 
    > Reviewed-by: Jordan Bayles <jophba@chromium.org> 
    > Commit-Queue: Muyao Xu <muyaoxu@google.com> 
    > Cr-Commit-Position: refs/heads/main@{#1616219} 
     
    (cherry picked from commit a1d328a102b58e941cab8fdcdc74749358d8084b) 
     
    Bug: 503979526,502449857 
    Change-Id: Id320a57560898dd340760be9f7821512321ace56 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7783789 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Commit-Queue: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7727@{#3428} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `chrome/browser/media/router/providers/cast/cast_activity_manager.cc`
- M `chrome/browser/media/router/providers/cast/cast_activity_manager.h`
- M `chrome/browser/media/router/providers/cast/cast_activity_manager_unittest.cc`

---

Hash: [b8b1fcd6a440ac5acf386fcd99d264dab8b81d67](https://chromiumdash.appspot.com/commit/b8b1fcd6a440ac5acf386fcd99d264dab8b81d67)  

Date: Tue Apr 21 22:29:50 2026


---

### pe...@google.com (2026-04-21)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dx...@google.com (2026-04-21)

Project: chromium/src  

Branch:  refs/branch-heads/7778  

Author:  Muyao Xu [muyaoxu@google.com](mailto:muyaoxu@google.com)  

Link:    <https://chromium-review.googlesource.com/7783769>

[M148] [MediaRouter] Fix UAF in CastActivityManager::AddMirroringActivity

---


Expand for full commit details
```
     
    Original change's description: 
    > [MediaRouter] Fix UAF in CastActivityManager::AddMirroringActivity 
    > 
    > When AddMirroringActivity is called on an existing route ID, it 
    > overwrites the entry in activities_ using insert_or_assign(), destroying 
    > the old CastActivity (which could be an AppActivity). This left the raw 
    > pointer in app_activities_ dangling, causing a Use-After-Free if 
    > accessed later. This CL adds app_activities_.erase() to safely clear 
    > the raw pointer when the owning unique_ptr is replaced. 
    > 
    > Bug: 502449857 
    > Change-Id: Id320a57560898dd340760be9f7821512321ace56 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7766193 
    > Reviewed-by: Jordan Bayles <jophba@chromium.org> 
    > Commit-Queue: Muyao Xu <muyaoxu@google.com> 
    > Cr-Commit-Position: refs/heads/main@{#1616219} 
     
    (cherry picked from commit a1d328a102b58e941cab8fdcdc74749358d8084b) 
     
    Bug: 503979821,502449857 
    Change-Id: Id320a57560898dd340760be9f7821512321ace56 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7783769 
    Commit-Queue: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7778@{#1318} 
    Cr-Branched-From: 77f495ee216d4c3cc784d33658bad4778c0680ee-refs/heads/main@{#1610480}

```

---

Files:

- M `chrome/browser/media/router/providers/cast/cast_activity_manager.cc`
- M `chrome/browser/media/router/providers/cast/cast_activity_manager.h`
- M `chrome/browser/media/router/providers/cast/cast_activity_manager_unittest.cc`

---

Hash: [3f9df1a456948965a1a1a2ff653d42c4198bafa0](https://chromiumdash.appspot.com/commit/3f9df1a456948965a1a1a2ff653d42c4198bafa0)  

Date: Tue Apr 21 22:54:58 2026


---

### aj...@google.com (2026-04-29)

Low severity as this has several mitigating factors.

### sp...@google.com (2026-05-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
highly mitigated browser memory corruption


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### pe...@google.com (2026-06-02)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-06-02)

1. https://chromium-review.git.corp.google.com/c/chromium/src/+/7885122/1..2
2. Low - There were a couple of conflicts, but they were not difficult to fix.
3. 147 and 148
4. Yes.

### dx...@google.com (2026-06-09)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Muyao Xu [muyaoxu@google.com](mailto:muyaoxu@google.com)  

Link:    <https://chromium-review.googlesource.com/7885122>

[M144-LTS][MediaRouter] Fix UAF in CastActivityManager::AddMirroringActivity

---


Expand for full commit details
```
     
    When AddMirroringActivity is called on an existing route ID, it 
    overwrites the entry in activities_ using insert_or_assign(), destroying 
    the old CastActivity (which could be an AppActivity). This left the raw 
    pointer in app_activities_ dangling, causing a Use-After-Free if 
    accessed later. This CL adds app_activities_.erase() to safely clear 
    the raw pointer when the owning unique_ptr is replaced. 
     
    (cherry picked from commit a1d328a102b58e941cab8fdcdc74749358d8084b) 
     
    Bug: 502449857 
    Change-Id: Id320a57560898dd340760be9f7821512321ace56 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7766193 
    Reviewed-by: Jordan Bayles <jophba@chromium.org> 
    Commit-Queue: Muyao Xu <muyaoxu@google.com> 
    Cr-Original-Commit-Position: refs/heads/main@{#1616219} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7885122 
    Reviewed-by: Mohamed Omar <mohamedaomar@google.com> 
    Reviewed-by: Muyao Xu <muyaoxu@google.com> 
    Owners-Override: Artem Sumaneev <asumaneev@google.com> 
    Commit-Queue: Jordan Bayles <jophba@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4985} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `chrome/browser/media/router/providers/cast/cast_activity_manager.cc`
- M `chrome/browser/media/router/providers/cast/cast_activity_manager.h`
- M `chrome/browser/media/router/providers/cast/cast_activity_manager_unittest.cc`

---

Hash: [47a3ec444fd76833b862d024605a70a3c9bd60d5](https://chromiumdash.appspot.com/commit/47a3ec444fd76833b862d024605a70a3c9bd60d5)  

Date: Tue Jun 9 20:11:29 2026


---

### ch...@google.com (2026-07-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/502449857)*
