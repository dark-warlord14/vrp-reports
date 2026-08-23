# Security: Heap-use-after-free regression in ServiceWorkerContextCore::OnRunningStateChanged


| Field | Value |
|-------|-------|
| **Issue ID** | [505068950](https://issues.chromium.org/issues/505068950) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>ServiceWorker |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 147.0.0.0 |
| **Reporter** | me...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2026-04-22 |
| **Bounty** | $2,000.00 |

## Description

# Steps to reproduce the problem

1. Apply `trigger.patch` to Chromium and compile with ASAN enabled
2. Put `background.js` and `manifest.json` at ext\_poc folder. Run Chrome:
   ```
   ./out/asan/chrome --no-sandbox --no-first-run --load-extension=/path/to/ext_poc
   
   ```
3. ASAN heap-use-after-free fires automatically after 2 seconds.

The `trigger.patch` adds a single line (`wrapper_->Shutdown()`) to simulate the destruction of `ServiceWorkerContextCore` during `OnRunningStateChanged`. This is the exact destruction path that occurs in production (confirmed by production crash reports and LLDB analysis in the original bug) when `ServiceWorkerContextWrapper::Shutdown()` is called while a synchronous observer loop is iterating over `sync_observer_list_->observers`.

# Problem Description

## Introduction

This is a **regression** of [Bug 496389117](https://issues.chromium.org/issues/496389117). The original UAF was fixed twice:

1. **Fix #1** (d819b4683ad8d, 2026-03-30): Held `scoped_refptr<ServiceWorkerContextWrapper>` to keep the wrapper alive. This was a **red herring** — holding the wrapper does not prevent `Shutdown()` from calling `context_core_.reset()`, which destroys the core and its members.
2. **Fix #2** (7e3665aeacc7c, 2026-04-09): Correctly fixed the issue by copying `sync_observer_list_` into a local `safe_sync_observer_list` and iterating over the local copy. This ensures the observer list survives even if `this` is destroyed during iteration.
3. **Regression** (d28abec927384, 2026-04-13): A follow-up commit to fix a CHECK failure changed the sync observer loops back from `safe_sync_observer_list->observers` to `sync_observer_list_->observers`, silently reverting Fix #2. The local variable `safe_sync_observer_list` is now **dead code** — it is assigned at line 1257 but never used.

## Analysis

**Vulnerability Summary**

The vulnerability is a **Use-After-Free (UAF)** in `ServiceWorkerContextCore::OnRunningStateChanged`. When a service worker stops, the method iterates over `sync_observer_list_->observers` — a member of `this`. If an asynchronous observer callback (dispatched via `observer_list_->Notify`) triggers `ServiceWorkerContextWrapper::Shutdown()`, the core is destroyed (`context_core_.reset()`), and the subsequent access to `this->sync_observer_list_` reads freed memory.

**Current code (after regression d28abec927384):**

```
void ServiceWorkerContextCore::OnRunningStateChanged(
    ServiceWorkerVersion* version) {
  // ...
  scoped_refptr<ServiceWorkerContextSynchronousObserverList>
      safe_sync_observer_list = sync_observer_list_;  // [1] DEAD CODE — never used below
  // ...
  switch (version->running_status()) {
    case blink::EmbeddedWorkerStatus::kStopped:
      observer_list_->Notify(FROM_HERE,
                             &ServiceWorkerContextCoreObserver::OnStopped,
                             version->version_id());
      // Shutdown() may be called during async notification above,
      // destroying `this` (context_core_.reset())
      if (start_worker_token.has_value()) {
        for (auto& observer : sync_observer_list_->observers) {  // [2] UAF — reads freed this->sync_observer_list_
          observer.OnStoppedSync(...);
        }
      }
      break;
    case blink::EmbeddedWorkerStatus::kStopping:
      // ...
      if (start_worker_token.has_value()) {
        for (auto& observer : sync_observer_list_->observers) {  // [3] Same UAF
          observer.OnStoppingSync(...);
        }
      }
      break;
  }
}

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/service_worker/service_worker_context_core.cc;l=1257;bpv=1>
[1] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/service_worker/service_worker_context_core.cc;l=1274;bpv=1>
[1] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/service_worker/service_worker_context_core.cc;l=1297;bpv=1>

## Bisect

- **Original bug:** [Bug 496389117](https://issues.chromium.org/issues/496389117) (production crashes)
- **Fix #1:** d819b4683ad8d (2026-03-30) — incomplete fix (wrapper refcount is a red herring)
- **Fix #2:** 7e3665aeacc7c (2026-04-09) — correct fix (local `scoped_refptr` copy of observer list)
- **Regression introduced by:** d28abec927384 (2026-04-13) — reverted Fix #2 by changing loop variables back to member access
- Affects Chrome DEV 149.0.7795.2

# Summary

Security: Heap-use-after-free regression in ServiceWorkerContextCore::OnRunningStateChanged

# Custom Questions

#### Type of crash:

browser

#### Crash state:

```
=================================================================
==384536==ERROR: AddressSanitizer: heap-use-after-free on address 0x7cecb04346f8 at pc 0x7f6d17c1fe4b bp 0x7ffc73d3d010 sp 0x7ffc73d3d008
READ of size 8 at 0x7cecb04346f8 thread T0 (chrome)
    #0 0x7f6d17c1fe4a in content::ServiceWorkerContextCore::OnRunningStateChanged(content::ServiceWorkerVersion*) base/memory/scoped_refptr.h:293:12
    #1 0x7f6d17e359c5 in content::ServiceWorkerVersion::OnStoppedInternal(blink::EmbeddedWorkerStatus) content/browser/service_worker/service_worker_version.cc:3134:14
    #2 0x7f6d17b80122 in content::EmbeddedWorkerInstance::Detach() content/browser/service_worker/embedded_worker_instance.cc:751:14
    #3 0x7f6d17b904d2 in base::internal::Invoker<base::internal::FunctorTraits<void (content::EmbeddedWorkerInstance::*&&)(), content::EmbeddedWorkerInstance*>, base::internal::BindState<true, true, false, void (content::EmbeddedWorkerInstance::*)(), base::internal::UnretainedWrapper<content::EmbeddedWorkerInstance, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #4 0x7f6d33665136 in mojo::InterfaceEndpointClient::NotifyError(std::__Cr::optional<mojo::DisconnectReason> const&) base/functional/callback.h:155:12
    #5 0x7f6d33687e4a in mojo::internal::MultiplexRouter::ProcessNotifyErrorTask(mojo::internal::MultiplexRouter::Task*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:1116:13
    #6 0x7f6d3367e5d5 in mojo::internal::MultiplexRouter::ProcessTasks(mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:1024:15
    #7 0x7f6d33678d32 in mojo::internal::MultiplexRouter::OnPipeConnectionError(bool) mojo/public/cpp/bindings/lib/multiplex_router.cc:930:3
    #8 0x7f6d3368b3eb in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::internal::MultiplexRouter::*&&)(bool), mojo::internal::MultiplexRouter*, bool&&>, base::internal::BindState<true, true, false, void (mojo::internal::MultiplexRouter::*)(bool), base::internal::UnretainedWrapper<mojo::internal::MultiplexRouter, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, bool>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #9 0x7f6d33649f55 in mojo::Connector::HandleError(bool, bool) base/functional/callback.h:155:12
    #10 0x7f6d3364bf89 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int) mojo/public/cpp/bindings/lib/connector.cc
    #11 0x7f6d3364eb51 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int) base/functional/bind_internal.h:740:12
    #12 0x7f6d3364e1fe in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const & base/functional/callback.h:346:12
    #13 0x7f6d3364dfb4 in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&) base/functional/bind_internal.h:673:12
    #14 0x7f6d33571770 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const & base/functional/callback.h:346:12
    #15 0x7f6d3357114b in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple_watcher.cc:286:14
    #16 0x7f6d335721b4 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #17 0x7f6d350f4679 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #18 0x7f6d3516e900 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #19 0x7f6d3516d8d6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:336:40
    #20 0x7f6d35346f59 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:782:48
    #21 0x7f6d3516ff53 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:640:12
    #22 0x7f6d3505f792 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #23 0x7f6d163184b3 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:1103:18
    #24 0x7f6d16320726 in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:151:15
    #25 0x7f6d1630f965 in content::BrowserMain(content::MainFunctionParams) content/browser/browser_main.cc:32:28
    #26 0x7f6d197cec35 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:697:10
    #27 0x7f6d197d256d in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content_main_runner_impl.cc:1332:10
    #28 0x7f6d197d1ac6 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1162:12
    #29 0x7f6d197cbfd3 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:356:36
    #30 0x7f6d197cc35a in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:369:10
    #31 0x557c8a226855 in ChromeMain chrome/app/chrome_main.cc:194:12
    #32 0x7f6cbfed1082 in __libc_start_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16

0x7cecb04346f8 is located 632 bytes inside of 816-byte region [0x7cecb0434480,0x7cecb04347b0)
freed by thread T0 (chrome) here:
    #0 0x557c8a225502 in operator delete(void*, unsigned long) (/home/krace/fuzz/chromium/src/out/ui/chrome+0x67ff502) (BuildId: c0321228bd1952d6)
    #1 0x7f6d17c437fe in content::ServiceWorkerContextWrapper::Shutdown() gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
    #2 0x7f6d17c1ec8f in content::ServiceWorkerContextCore::OnRunningStateChanged(content::ServiceWorkerVersion*) content/browser/service_worker/service_worker_context_core.cc:1268:17
    #3 0x7f6d17e359c5 in content::ServiceWorkerVersion::OnStoppedInternal(blink::EmbeddedWorkerStatus) content/browser/service_worker/service_worker_version.cc:3134:14
    #4 0x7f6d17b80122 in content::EmbeddedWorkerInstance::Detach() content/browser/service_worker/embedded_worker_instance.cc:751:14
    #5 0x7f6d17b904d2 in base::internal::Invoker<base::internal::FunctorTraits<void (content::EmbeddedWorkerInstance::*&&)(), content::EmbeddedWorkerInstance*>, base::internal::BindState<true, true, false, void (content::EmbeddedWorkerInstance::*)(), base::internal::UnretainedWrapper<content::EmbeddedWorkerInstance, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #6 0x7f6d33665136 in mojo::InterfaceEndpointClient::NotifyError(std::__Cr::optional<mojo::DisconnectReason> const&) base/functional/callback.h:155:12
    #7 0x7f6d33687e4a in mojo::internal::MultiplexRouter::ProcessNotifyErrorTask(mojo::internal::MultiplexRouter::Task*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:1116:13
    #8 0x7f6d3367e5d5 in mojo::internal::MultiplexRouter::ProcessTasks(mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:1024:15
    #9 0x7f6d33678d32 in mojo::internal::MultiplexRouter::OnPipeConnectionError(bool) mojo/public/cpp/bindings/lib/multiplex_router.cc:930:3
    #10 0x7f6d3368b3eb in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::internal::MultiplexRouter::*&&)(bool), mojo::internal::MultiplexRouter*, bool&&>, base::internal::BindState<true, true, false, void (mojo::internal::MultiplexRouter::*)(bool), base::internal::UnretainedWrapper<mojo::internal::MultiplexRouter, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, bool>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #11 0x7f6d33649f55 in mojo::Connector::HandleError(bool, bool) base/functional/callback.h:155:12
    #12 0x7f6d3364bf89 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int) mojo/public/cpp/bindings/lib/connector.cc
    #13 0x7f6d3364eb51 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int) base/functional/bind_internal.h:740:12
    #14 0x7f6d3364e1fe in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const & base/functional/callback.h:346:12
    #15 0x7f6d3364dfb4 in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&) base/functional/bind_internal.h:673:12
    #16 0x7f6d33571770 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const & base/functional/callback.h:346:12
    #17 0x7f6d3357114b in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple_watcher.cc:286:14
    #18 0x7f6d335721b4 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #19 0x7f6d350f4679 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #20 0x7f6d3516e900 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #21 0x7f6d3516d8d6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:336:40
    #22 0x7f6d35346f59 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:782:48
    #23 0x7f6d3516ff53 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:640:12
    #24 0x7f6d3505f792 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #25 0x7f6d163184b3 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:1103:18
    #26 0x7f6d16320726 in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:151:15
    #27 0x7f6d1630f965 in content::BrowserMain(content::MainFunctionParams) content/browser/browser_main.cc:32:28
    #28 0x7f6d197cec35 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:697:10
    #29 0x7f6d197d256d in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content_main_runner_impl.cc:1332:10

previously allocated by thread T0 (chrome) here:
    #0 0x557c8a2248fd in operator new(unsigned long) (/home/krace/fuzz/chromium/src/out/ui/chrome+0x67fe8fd) (BuildId: c0321228bd1952d6)
    #1 0x7f6d17c432b0 in content::ServiceWorkerContextWrapper::InitInternal(storage::QuotaManagerProxy*, storage::SpecialStoragePolicy*, content::ChromeBlobStorageContext*, content::BrowserContext*) gen/third_party/libc++/src/include/__memory/unique_ptr.h:756:26
    #2 0x7f6d17f6e7d7 in content::StoragePartitionImpl::Initialize(content::StoragePartitionImpl*) content/browser/storage_partition_impl.cc:1439:28
    #3 0x7f6d17fd35a4 in content::StoragePartitionImplMap::Get(content::StoragePartitionConfig const&, bool) content/browser/storage_partition_impl_map.cc:355:14
    #4 0x7f6d1625d4ea in content::BrowserContext::GetDefaultStoragePartition() content/browser/browser_context.cc:151:52
    #5 0x557c8ac86986 in extensions::CWSInfoService::CWSInfoService(content::BrowserContext*) extensions/browser/cws_info_service.cc:243:44
    #6 0x557c8df7df89 in extensions::CWSInfoServiceFactory::BuildServiceInstanceForBrowserContext(content::BrowserContext*) const gen/third_party/libc++/src/include/__memory/unique_ptr.h:756:30
    #7 0x7f6d2a480d4c in KeyedServiceTemplatedFactory<KeyedService>::GetServiceForContext(void*, bool) components/keyed_service/core/keyed_service_templated_factory.cc:149:22
    #8 0x7f6d2a478ddb in DependencyManager::CreateContextServices(void*, bool) components/keyed_service/core/dependency_manager.cc:125:16
    #9 0x7f6d1ccda855 in BrowserContextDependencyManager::DoCreateBrowserContextServices(content::BrowserContext*, bool) components/keyed_service/content/browser_context_dependency_manager.cc:36:22
    #10 0x557c925180bd in ProfileImpl::OnLocaleReady(Profile::CreateMode) chrome/browser/profiles/profile_impl.cc:1139:51
    #11 0x557c92513191 in ProfileImpl::OnPrefsLoaded(Profile::CreateMode, bool) chrome/browser/profiles/profile_impl.cc:1179:3
    #12 0x557c925115ca in ProfileImpl::ProfileImpl(base::FilePath const&, Profile::Delegate*, Profile::CreateMode, base::Time, scoped_refptr<base::SequencedTaskRunner>) chrome/browser/profiles/profile_impl.cc:545:5
    #13 0x557c92510194 in Profile::CreateProfile(base::FilePath const&, Profile::Delegate*, Profile::CreateMode) chrome/browser/profiles/profile_impl.cc:378:59
    #14 0x557c91183afe in ProfileManager::CreateProfileHelper(base::FilePath const&) chrome/browser/profiles/profile_manager.cc:1327:10
    #15 0x557c91193e87 in base::internal::Invoker<base::internal::FunctorTraits<std::__Cr::unique_ptr<Profile, std::__Cr::default_delete<Profile>> (ProfileManager::*&&)(base::FilePath const&), ProfileManager*>, base::internal::BindState<true, true, false, std::__Cr::unique_ptr<Profile, std::__Cr::default_delete<Profile>> (ProfileManager::*)(base::FilePath const&), base::internal::UnretainedWrapper<ProfileManager, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, std::__Cr::unique_ptr<Profile, std::__Cr::default_delete<Profile>> (base::FilePath const&)>::RunOnce(base::internal::BindStateBase*, base::FilePath const&) base/functional/bind_internal.h:740:12
    #16 0x557c9117bbfb in ProfileManager::CreateAndInitializeProfile(base::FilePath const&, base::OnceCallback<std::__Cr::unique_ptr<Profile, std::__Cr::default_delete<Profile>> (base::FilePath const&)>) base/functional/callback.h:155:12
    #17 0x557c911790f3 in ProfileManager::GetProfile(base::FilePath const&) chrome/browser/profiles/profile_manager.cc:807:10
    #18 0x557c8f626ca4 in GetStartupProfile(base::FilePath const&, base::CommandLine const&) chrome/browser/ui/startup/startup_browser_creator.cc:1705:39
    #19 0x557c923e2eb3 in ChromeBrowserMainParts::PreMainMessageLoopRunImpl() chrome/browser/chrome_browser_main.cc:459:7
    #20 0x557c923e22f4 in ChromeBrowserMainParts::PreMainMessageLoopRun() chrome/browser/chrome_browser_main.cc:1463:18
    #21 0x7f6d16315c7a in content::BrowserMainLoop::PreMainMessageLoopRun() content/browser/browser_main_loop.cc:1003:28
    #22 0x7f6d1631cfb2 in base::internal::Invoker<base::internal::FunctorTraits<int (content::BrowserMainLoop::*&&)(), content::BrowserMainLoop*>, base::internal::BindState<true, true, false, int (content::BrowserMainLoop::*)(), base::internal::UnretainedWrapper<content::BrowserMainLoop, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, int ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #23 0x7f6d17f5e36d in content::StartupTaskRunner::RunAllTasksNow(bool) base/functional/callback.h:155:12
    #24 0x7f6d16314b6b in content::BrowserMainLoop::CreateStartupTasks() content/browser/browser_main_loop.cc:909:25
    #25 0x7f6d1631fe97 in content::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams) content/browser/browser_main_runner_impl.cc:138:15
    #26 0x7f6d1630f90c in content::BrowserMain(content::MainFunctionParams) content/browser/browser_main.cc:28:32
    #27 0x7f6d197cec35 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:697:10
    #28 0x7f6d197d256d in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content_main_runner_impl.cc:1332:10
    #29 0x7f6d197d1ac6 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1162:12

SUMMARY: AddressSanitizer: heap-use-after-free base/memory/scoped_refptr.h:293:12 in content::ServiceWorkerContextCore::OnRunningStateChanged(content::ServiceWorkerVersion*)
Shadow bytes around the buggy address:
  0x7cecb0434400: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x7cecb0434480: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7cecb0434500: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7cecb0434580: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7cecb0434600: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x7cecb0434680: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd[fd]
  0x7cecb0434700: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7cecb0434780: fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa fa
  0x7cecb0434800: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x7cecb0434880: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7cecb0434900: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
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

==384536==ADDITIONAL INFO

==384536==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7f6d33570100 in mojo::SimpleWatcher::ArmOrNotify() mojo/public/cpp/system/simple_watcher.cc:245:28
    #1 0x7f6d3364cf96 in mojo::Connector::ScheduleDispatchOfPendingMessagesOrWaitForMore(unsigned long) mojo/public/cpp/bindings/lib/connector.cc:588:7
    #2 0x7f6d33571b6a in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) mojo/public/cpp/system/simple_watcher.cc:103:13

Command line: `./out/ui/chrome --user-data-dir=/tmp/noexist2 --trigger-sw-context-uaf --load-extension=webnn_tmp/service_worker/ext_poc --ozone-platform=x11 --flag-switches-begin --flag-switches-end`

MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==384536==END OF ADDITIONAL INFO

==384536==ABORTING


```
# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [trigger.patch](attachments/trigger.patch) (text/x-diff, 830 B)
- [background.js](attachments/background.js) (text/javascript, 254 B)
- [manifest.json](attachments/manifest.json) (application/json, 197 B)

## Timeline

### me...@gmail.com (2026-04-24)

Hello any update?

### ca...@chromium.org (2026-04-24)

I was able to reproduce this in dev, but it looks like the CL that introduced the bug was merged to 147, so setting FoundIn as 147. This would be an S0 since it's in the browser process, but since it requires an extension I'm triaging it as S1.

### ca...@chromium.org (2026-04-24)

andreaorru: Assigning to you since you're the CL author, please take a look and further triage. Thanks

### an...@chromium.org (2026-04-24)

I'm dropping this to S2.

The reason why there was a subsequent fix after #2 is because the crash wasn't fixed and `sync_observer_list_` did not actually become null. It turned out to be a red herring. Rather, the `start_worker_token` was null.

I'm skeptical the sequence you describe (and patch into the code) actually happens in practice. However, I suppose it can happen in theory, and there's no harm in being defensive and use `safe_sync_observer_list` just in case.

### ch...@google.com (2026-04-25)

Setting milestone because of s2 severity.

### dx...@google.com (2026-04-27)

Project: chromium/src  

Branch:  main  

Author:  Andrea Orru [andreaorru@chromium.org](mailto:andreaorru@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7793527>

Prevent potential UAF if Shutdown happens in OnRunningStateChanged

---


Expand for full commit details
```
     
    We had already introduced `safe_sync_observer_list` in a previous CL 
    (https://crrev.com/c/7740779) but its use was silently removed as part 
    of another fix (https://crrev.com/c/7749842). 
     
    This CL defensively restores it. 
     
    Fixed: 505068950 
    Change-Id: I85b9a762021a3e9e6e20689755385cedcc1668b0 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7793527 
    Commit-Queue: Andrea Orru <andreaorru@chromium.org> 
    Reviewed-by: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1621288}

```

---

Files:

- M `content/browser/service_worker/service_worker_context_core.cc`

---

Hash: [5dbc814bf3657d2dd0d8ac766756639d6f7f7571](https://chromiumdash.appspot.com/commit/5dbc814bf3657d2dd0d8ac766756639d6f7f7571)  

Date: Mon Apr 27 20:37:26 2026


---

### aj...@google.com (2026-06-16)

-> S3 as this is a theoretical race

### sp...@google.com (2026-06-29)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Highly mitigated. Rce browser shutdown with bisect


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-08-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/505068950)*
