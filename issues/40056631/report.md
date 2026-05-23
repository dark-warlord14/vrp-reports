# Security: UAF in perfromance_manager's site_data_impl.cc

| Field | Value |
|-------|-------|
| **Issue ID** | [40056631](https://issues.chromium.org/issues/40056631) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>PerformanceManager |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | rz...@gmail.com |
| **Assignee** | si...@chromium.org |
| **Created** | 2021-07-22 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**

SiteDataImpl object is accessing the destroyed OnDestroyDelegate object [1]; triggered soon after the tab is closed while attempting to receive the notification from OnSiteDataImplDestroyed [2], when it is about to get destroyed.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:components/performance_manager/persistence/site_data/site_data_impl.cc;l=202>

[2] <https://source.chromium.org/chromium/chromium/src/+/main:components/performance_manager/persistence/site_data/site_data_impl.h;l=64>

**VERSION**  

Chrome Version: 93.0.4544.0 (Developer Build) (64-Bit)  

Operating System: Ubuntu 20.04

**REPRODUCTION CASE**

1. save the attached files to /path/to/chromium/src/
2. $ cd /path/to/chromium/src/
3. $ python ./copy\_mojo\_js\_bindings.py /path/to/chromium/src/out/asan/gen
4. $ python3 -m http.server
5. out/asan/chrome --user-data-dir=/tmp/x/ --enable-blink-features=MojoJS "<http://localhost:8000/sitedata.html>"
6. open "chrome://discards" in another tab
7. wait for a couple of seconds and navigate to sitedata.html and then close the window.
8. finally close the leftover "chrome://discards" window.
9. observe the crash.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

Type of crash: browser  

Crash State: asan\_log [attachment]

**CREDIT INFORMATION**

Reporter credit: sri

## Attachments

- [sitedata.html](attachments/sitedata.html) (text/plain, 713 B)
- [asan_log](attachments/asan_log) (text/plain, 24.7 KB)
- deleted (application/octet-stream, 0 B)
- [copy_mojo_js_bindings.py](attachments/copy_mojo_js_bindings.py) (text/plain, 514 B)
- [asan_new](attachments/asan_new) (text/plain, 27.0 KB)
- [poc.mp4](attachments/poc.mp4) (video/mp4, 2.4 MB)
- [site.tar.xz](attachments/site.tar.xz) (application/octet-stream, 1008 B)

## Timeline

### [Deleted User] (2021-07-22)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-07-22)

+sebmarchand and other folks in this file: can you take a look?

A UaF in the browser process that's accessible with MojoJS is usually High severity. This also needs chrome://discards to be opened and closed, so I think that possibly takes it down to a Medium severity, but I will keep it at High for now.

[Monorail components: Internals>PerformanceManager]

### [Deleted User] (2021-07-22)

[Empty comment from Monorail migration]

### ch...@chromium.org (2021-07-22)

Aside: how does the MojoJS blink feature work, and how does sitedata.html gain access to the SiteDataProvider interface? That particular interface is only exposed and injected into the "privileged" renderer hosting  chrome://discards, so presumably shouldn't be accessible from just any renderer?

### si...@chromium.org (2021-07-22)

At the start of the attached video, the renderer is already dead on BAD MESSAGE, which is what I'd have expected for an attempted connection to this interface. I think the attached content is likely a red herring, and this is just a shutdown order UAF?

### rz...@gmail.com (2021-07-22)

Attached content is not 'red herring'. Have only started to record once the browser is up and running - since it is taking few seconds to boot up ; thus limiting the attachment size. This is still being reproduced very stable at my end. However, recorded right from the beginning - Please check the attached content now for better clarity. 

### si...@chromium.org (2021-07-22)

Re https://crbug.com/chromium/1231933#c6, I don't doubt that there's a UAF and a crash there. My question is whether it repros without doing anything other than loading the discards page and shutting down the browser. 

### si...@chromium.org (2021-07-22)

Sadly I cannot repro with a locally built ASAN build: Version 93.0.4544.0 (Developer Build) (64-bit).  I can trip ASAN with chrome://crash/heap-overflow, so I wonder if there's something I'm missing in the build configuration.

### [Deleted User] (2021-07-22)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@gmail.com (2021-07-22)

@siggi, Just FYI, this is my args.gn

`
    is_asan = true
    is_debug = false
    enable_nacl = false
    treat_warnings_as_errors = false
    is_component_build=true
`

### si...@chromium.org (2021-07-22)

@rzintct, thanks!

### si...@chromium.org (2021-07-22)

Still cannot repro with above args.gn at Version 93.0.4544.0 (Developer Build) (64-bit), nor at ToT.


### si...@chromium.org (2021-07-22)

With this args.gn:

$ cat out/ASANRelease/args.gn 
is_asan = true
is_debug = false
enable_nacl = false
treat_warnings_as_errors = false
is_component_build=true
use_goma = true

I repro the expected renderer termination, but no UAF.

$ out/ASANRelease/chrome --user-data-dir=/tmp/x --enable-blink-features=MojoJS "http://localhost:8000/sitedata.html"
libva error: vaGetDriverNameByIndex() failed with unknown libva error, driver_name = (null)
[1747302:1747302:0722/182714.827490:ERROR:viz_main_impl.cc(162)] Exiting GPU process due to errors during initialization
libva error: vaGetDriverNameByIndex() failed with unknown libva error, driver_name = (null)
[1747391:1747391:0722/182715.755932:ERROR:viz_main_impl.cc(162)] Exiting GPU process due to errors during initialization
Warning: disabling flag --regexp_tier_up due to conflicting flags
[1747452:1747452:0722/182715.915996:ERROR:gpu_init.cc(441)] Passthrough is not supported, GL is swiftshader
127.0.0.1 - - [22/Jul/2021 18:27:16] "GET /mojo_bindings.js HTTP/1.1" 304 -
127.0.0.1 - - [22/Jul/2021 18:27:16] "GET /chrome/browser/ui/webui/discards/site_data.mojom.js HTTP/1.1" 304 -
[1747271:1747271:0722/182716.255560:ERROR:bad_message.cc(18)] Terminating renderer for bad IPC message, reason 3
[0722/182716.408521:WARNING:exception_snapshot_linux.cc(427)] Unhandled signal -1
[0722/182716.409277:ERROR:file_io_posix.cc(144)] open /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq: No such file or directory (2)
[0722/182716.409425:ERROR:file_io_posix.cc(144)] open /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq: No such file or directory (2)


### si...@chromium.org (2021-07-22)

So here's my current hypothesis as to what's happening. 
SiteDataCacheFactory::SetDataCacheInspectorForBrowserContext is getting invoked for an outgoing profile (browser context) while there's still an outstanding mojo interface to a SiteDataProviderImpl. This is probably through the OriginToReaderMap requested_origins_; map, which holds unique_ptrs to SiteDataReader which in turn have a reference to the SiteDataImpl.
If the inspector goes away before the mojo interface to the SiteDataProviderImpl, we'd see this UAF and crash.

This is a shutdown-like UAF though, and it requires that the chrome://discards WebUI is invoked.
I'm guessing the MojoJS and the tab with "http://localhost:8000/sitedata.html" are necessary only to prime the race to fall out a certain way.



### si...@chromium.org (2021-07-22)

K, got a repro:
==1756937==ERROR: AddressSanitizer: heap-use-after-free on address 0x6070000e41d0 at pc 0x562d758253ed bp 0x7f0319fb7680 sp 0x7f0319fb7678
READ of size 8 at 0x6070000e41d0 thread T29 (ThreadPoolForeg)
    #0 0x562d758253ec in performance_manager::internal::SiteDataImpl::~SiteDataImpl() components/performance_manager/persistence/site_data/site_data_impl.cc:202:14
    #1 0x562d7582582d in performance_manager::internal::SiteDataImpl::~SiteDataImpl() components/performance_manager/persistence/site_data/site_data_impl.cc:192:31
    #2 0x562d778071b2 in operator() buildtools/third_party/libc++/trunk/include/memory:1335:5
    #3 0x562d778071b2 in reset buildtools/third_party/libc++/trunk/include/memory:1596:7
    #4 0x562d778071b2 in ~unique_ptr buildtools/third_party/libc++/trunk/include/memory:1550:19
    #5 0x562d778071b2 in ~pair buildtools/third_party/libc++/trunk/include/utility:297:29
    #6 0x562d778071b2 in destroy buildtools/third_party/libc++/trunk/include/memory:829:15
    #7 0x562d778071b2 in destroy<std::pair<std::string, std::unique_ptr<performance_manager::SiteDataReader> >, void> buildtools/third_party/libc++/trunk/include/__memory/allocator_traits.h:307:13
    #8 0x562d778071b2 in __destruct_at_end buildtools/third_party/libc++/trunk/include/vector:428:9
    #9 0x562d778071b2 in clear buildtools/third_party/libc++/trunk/include/vector:371:29
    #10 0x562d778071b2 in ~__vector_base buildtools/third_party/libc++/trunk/include/vector:465:9
    #11 0x562d778071b2 in std::__Cr::vector<std::__Cr::pair<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >, std::__Cr::unique_ptr<performance_manager::SiteDataReader, std::__Cr::default_delete<performance_manager::SiteDataReader> > >, std::__Cr::allocator<std::__Cr::pair<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >, std::__Cr::unique_ptr<performance_manager::SiteDataReader, std::__Cr::default_delete<performance_manager::SiteDataReader> > > > >::~vector() buildtools/third_party/libc++/trunk/include/vector:557:5
    #12 0x562d77803e84 in ~flat_tree base/containers/flat_tree.h:222:24
    #13 0x562d77803e84 in ~SiteDataProviderImpl chrome/browser/ui/webui/discards/site_data_provider_impl.cc:89:45
    #14 0x562d77803e84 in ~SiteDataProviderImpl chrome/browser/ui/webui/discards/site_data_provider_impl.cc:89:45
    #15 0x562d77803e84 in non-virtual thunk to SiteDataProviderImpl::~SiteDataProviderImpl() chrome/browser/ui/webui/discards/site_data_provider_impl.cc
    #16 0x7f038b7018da in Run base/callback.h:98:12
    #17 0x7f038b7018da in mojo::InterfaceEndpointClient::NotifyError(absl::optional<mojo::DisconnectReason> const&) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:672:31
    #18 0x7f038b71be14 in mojo::internal::MultiplexRouter::ProcessNotifyErrorTask(mojo::internal::MultiplexRouter::Task*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:1003:13
    #19 0x7f038b715421 in mojo::internal::MultiplexRouter::ProcessTasks(mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:916:15
    #20 0x7f038b7116f3 in mojo::internal::MultiplexRouter::OnPipeConnectionError(bool) mojo/public/cpp/bindings/lib/multiplex_router.cc:826:3
    #21 0x7f038b6f0408 in Run base/callback.h:98:12
    #22 0x7f038b6f0408 in mojo::Connector::HandleError(bool, bool) mojo/public/cpp/bindings/lib/connector.cc:676:44
    #23 0x7f038b6777ad in Run base/callback.h:166:12
    #24 0x7f038b6777ad in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple_watcher.cc:278:14
    #25 0x7f038b678794 in Invoke<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> base/bind_internal.h:509:12
    #26 0x7f038b678794 in MakeItSo<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> base/bind_internal.h:668:5
    #27 0x7f038b678794 in RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), std::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0UL, 1UL, 2UL, 3UL> base/bind_internal.h:721:12
    #28 0x7f038b678794 in base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:690:12
    #29 0x7f038c9cecc0 in Run base/callback.h:98:12
    #30 0x7f038c9cecc0 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:178:33
    #31 0x7f038ca3ac36 in base::internal::TaskTracker::RunBlockShutdown(base::internal::Task*) base/task/thread_pool/task_tracker.cc:668:19
    #32 0x7f038ca39981 in RunTaskWithShutdownBehavior base/task/thread_pool/task_tracker.cc:682:7
    #33 0x7f038ca39981 in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&) base/task/thread_pool/task_tracker.cc:525:5
    #34 0x7f038cb1203c in base::internal::TaskTrackerPosix::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&) base/task/thread_pool/task_tracker_posix.cc:22:16
    #35 0x7f038ca38b0a in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource) base/task/thread_pool/task_tracker.cc:432:5
    #36 0x7f038ca55a02 in base::internal::WorkerThread::RunWorker() base/task/thread_pool/worker_thread.cc:367:34
    #37 0x7f038ca54e41 in base::internal::WorkerThread::RunPooledWorker() base/task/thread_pool/worker_thread.cc:262:3
    #38 0x7f038cb137a5 in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:96:13
    #39 0x7f034c82aea6 in start_thread nptl/pthread_create.c:477:8

0x6070000e41d0 is located 16 bytes inside of 80-byte region [0x6070000e41c0,0x6070000e4210)
freed by thread T38 (ThreadPoolForeg) here:
    #0 0x562d702d17fd in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:160:3
    #1 0x562d75813d76 in operator() buildtools/third_party/libc++/trunk/include/memory:1335:5
    #2 0x562d75813d76 in reset buildtools/third_party/libc++/trunk/include/memory:1596:7
    #3 0x562d75813d76 in operator= buildtools/third_party/libc++/trunk/include/memory:1515:5
    #4 0x562d75813d76 in operator= buildtools/third_party/libc++/trunk/include/utility:533:16
    #5 0x562d75813d76 in __move_constexpr<std::pair<std::string, std::unique_ptr<performance_manager::SiteDataCache> > *, std::pair<std::string, std::unique_ptr<performance_manager::SiteDataCache> > *> buildtools/third_party/libc++/trunk/include/algorithm:1876:19
    #6 0x562d75813d76 in __move<std::pair<std::string, std::unique_ptr<performance_manager::SiteDataCache> > *, std::pair<std::string, std::unique_ptr<performance_manager::SiteDataCache> > *> buildtools/third_party/libc++/trunk/include/algorithm:1885:12
    #7 0x562d75813d76 in move<std::pair<std::string, std::unique_ptr<performance_manager::SiteDataCache> > *, std::pair<std::string, std::unique_ptr<performance_manager::SiteDataCache> > *> buildtools/third_party/libc++/trunk/include/algorithm:1913:13
    #8 0x562d75813d76 in std::__Cr::vector<std::__Cr::pair<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >, std::__Cr::unique_ptr<performance_manager::SiteDataCache, std::__Cr::default_delete<performance_manager::SiteDataCache> > >, std::__Cr::allocator<std::__Cr::pair<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >, std::__Cr::unique_ptr<performance_manager::SiteDataCache, std::__Cr::default_delete<performance_manager::SiteDataCache> > > > >::erase(std::__Cr::__wrap_iter<std::__Cr::pair<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >, std::__Cr::unique_ptr<performance_manager::SiteDataCache, std::__Cr::default_delete<performance_manager::SiteDataCache> > > const*>, std::__Cr::__wrap_iter<std::__Cr::pair<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >, std::__Cr::unique_ptr<performance_manager::SiteDataCache, std::__Cr::default_delete<performance_manager::SiteDataCache> > > const*>) buildtools/third_party/libc++/trunk/include/vector:1739:33
    #9 0x7f038c9cecc0 in Run base/callback.h:98:12
    #10 0x7f038c9cecc0 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:178:33
    #11 0x7f038ca3ac36 in base::internal::TaskTracker::RunBlockShutdown(base::internal::Task*) base/task/thread_pool/task_tracker.cc:668:19
    #12 0x7f038ca39981 in RunTaskWithShutdownBehavior base/task/thread_pool/task_tracker.cc:682:7
    #13 0x7f038ca39981 in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&) base/task/thread_pool/task_tracker.cc:525:5
    #14 0x7f038cb1203c in base::internal::TaskTrackerPosix::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&) base/task/thread_pool/task_tracker_posix.cc:22:16
    #15 0x7f038ca38b0a in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource) base/task/thread_pool/task_tracker.cc:432:5
    #16 0x7f038ca55a02 in base::internal::WorkerThread::RunWorker() base/task/thread_pool/worker_thread.cc:367:34
    #17 0x7f038ca54e41 in base::internal::WorkerThread::RunPooledWorker() base/task/thread_pool/worker_thread.cc:262:3
    #18 0x7f038cb137a5 in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:96:13
    #19 0x7f034c82aea6 in start_thread nptl/pthread_create.c:477:8

previously allocated by thread T9 (ThreadPoolForeg) here:
    #0 0x562d702d0f9d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:99:3
    #1 0x562d75810bdb in make_unique<performance_manager::SiteDataCacheImpl, const std::string &, const base::FilePath &> buildtools/third_party/libc++/trunk/include/memory:2006:28
    #2 0x562d75810bdb in performance_manager::SiteDataCacheFactory::OnBrowserContextCreated(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, base::FilePath const&, absl::optional<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > >) components/performance_manager/persistence/site_data/site_data_cache_factory.cc:127:9
    #3 0x562d7373d0e1 in Invoke<void (performance_manager::SiteDataCacheFactory::*)(const std::string &, const base::FilePath &, absl::optional<std::string>), performance_manager::SiteDataCacheFactory *, std::string, base::FilePath, absl::optional<std::string> > base/bind_internal.h:509:12
    #4 0x562d7373d0e1 in MakeItSo<void (performance_manager::SiteDataCacheFactory::*)(const std::string &, const base::FilePath &, absl::optional<std::string>), performance_manager::SiteDataCacheFactory *, std::string, base::FilePath, absl::optional<std::string> > base/bind_internal.h:648:12
    #5 0x562d7373d0e1 in RunImpl<void (performance_manager::SiteDataCacheFactory::*)(const std::string &, const base::FilePath &, absl::optional<std::string>), std::tuple<base::internal::UnretainedWrapper<performance_manager::SiteDataCacheFactory>, std::string, base::FilePath, absl::optional<std::string> >, 0UL, 1UL, 2UL, 3UL> base/bind_internal.h:721:12
    #6 0x562d7373d0e1 in base::internal::Invoker<base::internal::BindState<void (performance_manager::SiteDataCacheFactory::*)(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, base::FilePath const&, absl::optional<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > >), base::internal::UnretainedWrapper<performance_manager::SiteDataCacheFactory>, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >, base::FilePath, absl::optional<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > > >, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:690:12
    #7 0x7f038c9cecc0 in Run base/callback.h:98:12
    #8 0x7f038c9cecc0 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:178:33
    #9 0x7f038ca3ac36 in base::internal::TaskTracker::RunBlockShutdown(base::internal::Task*) base/task/thread_pool/task_tracker.cc:668:19
    #10 0x7f038ca39981 in RunTaskWithShutdownBehavior base/task/thread_pool/task_tracker.cc:682:7
    #11 0x7f038ca39981 in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&) base/task/thread_pool/task_tracker.cc:525:5
    #12 0x7f038cb1203c in base::internal::TaskTrackerPosix::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&) base/task/thread_pool/task_tracker_posix.cc:22:16
    #13 0x7f038ca38b0a in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource) base/task/thread_pool/task_tracker.cc:432:5
    #14 0x7f038ca55a02 in base::internal::WorkerThread::RunWorker() base/task/thread_pool/worker_thread.cc:367:34
    #15 0x7f038ca54e41 in base::internal::WorkerThread::RunPooledWorker() base/task/thread_pool/worker_thread.cc:262:3
    #16 0x7f038cb137a5 in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:96:13
    #17 0x7f034c82aea6 in start_thread nptl/pthread_create.c:477:8

Thread T29 (ThreadPoolForeg) created by T0 (chrome) here:
    #0 0x562d7029134c in pthread_create /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:207:3
    #1 0x7f038cb12a0e in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, base::PlatformThreadHandle*, base::ThreadPriority) base/threading/platform_thread_posix.cc:139:13
    #2 0x7f038ca540af in base::internal::WorkerThread::Start(base::WorkerThreadObserver*) base/task/thread_pool/worker_thread.cc:109:3
    #3 0x7f038ca49bb5 in operator() base/task/thread_pool/thread_group_impl.cc:186:15
    #4 0x7f038ca49bb5 in void base::internal::ThreadGroupImpl::ScopedCommandsExecutor::WorkerContainer::ForEachWorker<base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl()::'lambda0'(base::internal::WorkerThread*)>(base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl()::'lambda0'(base::internal::WorkerThread*)) base/task/thread_pool/thread_group_impl.cc:153:9
    #5 0x7f038ca49711 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl() base/task/thread_pool/thread_group_impl.cc:185:23
    #6 0x7f038ca3f968 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::~ScopedCommandsExecutor() base/task/thread_pool/thread_group_impl.cc:104:31
    #7 0x7f038ca40c54 in base::internal::ThreadGroupImpl::PushTaskSourceAndWakeUpWorkers(base::internal::TransactionWithRegisteredTaskSource) base/task/thread_pool/thread_group_impl.cc:445:1
    #8 0x7f038ca51170 in base::internal::ThreadPoolImpl::PostTaskWithSequenceNow(base::internal::Task, scoped_refptr<base::internal::Sequence>) base/task/thread_pool/thread_pool_impl.cc:427:38
    #9 0x7f038ca5167d in base::internal::ThreadPoolImpl::PostTaskWithSequence(base::internal::Task, scoped_refptr<base::internal::Sequence>) base/task/thread_pool/thread_pool_impl.cc:444:12
    #10 0x7f038ca2964c in base::internal::PooledSequencedTaskRunner::PostDelayedTask(base::Location const&, base::OnceCallback<void ()>, base::TimeDelta) base/task/thread_pool/pooled_sequenced_task_runner.cc:34:40
    #11 0x7f038ca57317 in PostTask base/task_runner.cc:45:10
    #12 0x7f038ca57317 in base::(anonymous namespace)::PostTaskAndReplyTaskRunner::PostTask(base::Location const&, base::OnceCallback<void ()>) base/task_runner.cc:39:24
    #13 0x7f038ca681c7 in base::internal::PostTaskAndReplyImpl::PostTaskAndReply(base::Location const&, base::OnceCallback<void ()>, base::OnceCallback<void ()>) base/threading/post_task_and_reply_impl.cc:139:34
    #14 0x7f038ca56fbe in base::TaskRunner::PostTaskAndReply(base::Location const&, base::OnceCallback<void ()>, base::OnceCallback<void ()>) base/task_runner.cc:51:43
    #15 0x562d74373492 in component_updater::ComponentInstaller::Register(base::OnceCallback<bool (update_client::CrxComponent const&)>, base::OnceCallback<void ()>) components/component_updater/component_installer.cc:94:17
    #16 0x562d74372ee6 in component_updater::ComponentInstaller::Register(component_updater::ComponentUpdateService*, base::OnceCallback<void ()>) components/component_updater/component_installer.cc:73:3
    #17 0x562d72e6c38a in component_updater::RegisterAutofillRegexComponent(component_updater::ComponentUpdateService*) chrome/browser/component_updater/autofill_regex_component_installer.cc:134:14
    #18 0x562d72e604a1 in component_updater::RegisterComponentsForUpdate(bool, PrefService*, base::FilePath const&) chrome/browser/component_updater/registration.cc:193:3
    #19 0x562d72dff7e2 in ChromeBrowserMainParts::PreMainMessageLoopRunImpl() chrome/browser/chrome_browser_main.cc:1641:5
    #20 0x562d72dfdd92 in ChromeBrowserMainParts::PreMainMessageLoopRun() chrome/browser/chrome_browser_main.cc:1055:18
    #21 0x7f038226b03c in content::BrowserMainLoop::PreMainMessageLoopRun() content/browser/browser_main_loop.cc:949:28
    #22 0x7f03833a1268 in Run base/callback.h:98:12
    #23 0x7f03833a1268 in content::StartupTaskRunner::RunAllTasksNow() content/browser/startup_task_runner.cc:41:29
    #24 0x7f038226a67d in content::BrowserMainLoop::CreateStartupTasks() content/browser/browser_main_loop.cc:857:25
    #25 0x7f038227127a in content::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams const&) content/browser/browser_main_runner_impl.cc:131:15
    #26 0x7f0382266c45 in content::BrowserMain(content::MainFunctionParams const&) content/browser/browser_main.cc:43:32
    #27 0x7f03842b7f84 in RunBrowserProcessMain content/app/content_main_runner_impl.cc:598:10
    #28 0x7f03842b7f84 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content/app/content_main_runner_impl.cc:1087:10
    #29 0x7f03842b7239 in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:956:12
    #30 0x7f03842b194d in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) content/app/content_main.cc:386:36
    #31 0x7f03842b1e7c in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:412:10
    #32 0x562d702d3abd in ChromeMain chrome/app/chrome_main.cc:151:12
    #33 0x7f034be04d09 in __libc_start_main csu/../csu/libc-start.c:308:16

Thread T38 (ThreadPoolForeg) created by T37 (ThreadPoolForeg) here:
    #0 0x562d7029134c in pthread_create /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:207:3
    #1 0x7f038cb12a0e in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, base::PlatformThreadHandle*, base::ThreadPriority) base/threading/platform_thread_posix.cc:139:13
    #2 0x7f038ca540af in base::internal::WorkerThread::Start(base::WorkerThreadObserver*) base/task/thread_pool/worker_thread.cc:109:3
    #3 0x7f038ca49bb5 in operator() base/task/thread_pool/thread_group_impl.cc:186:15
    #4 0x7f038ca49bb5 in void base::internal::ThreadGroupImpl::ScopedCommandsExecutor::WorkerContainer::ForEachWorker<base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl()::'lambda0'(base::internal::WorkerThread*)>(base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl()::'lambda0'(base::internal::WorkerThread*)) base/task/thread_pool/thread_group_impl.cc:153:9
    #5 0x7f038ca49711 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl() base/task/thread_pool/thread_group_impl.cc:185:23
    #6 0x7f038ca4246a in FlushWorkerCreation base/task/thread_pool/thread_group_impl.cc:118:5
    #7 0x7f038ca4246a in base::internal::ThreadGroupImpl::WorkerThreadDelegateImpl::GetWork(base::internal::WorkerThread*) base/task/thread_pool/thread_group_impl.cc:596:14
    #8 0x7f038ca5598d in base::internal::WorkerThread::RunWorker() base/task/thread_pool/worker_thread.cc:354:51
    #9 0x7f038ca54e41 in base::internal::WorkerThread::RunPooledWorker() base/task/thread_pool/worker_thread.cc:262:3
    #10 0x7f038cb137a5 in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:96:13
    #11 0x7f034c82aea6 in start_thread nptl/pthread_create.c:477:8

Thread T37 (ThreadPoolForeg) created by T29 (ThreadPoolForeg) here:
    #0 0x562d7029134c in pthread_create /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:207:3
    #1 0x7f038cb12a0e in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, base::PlatformThreadHandle*, base::ThreadPriority) base/threading/platform_thread_posix.cc:139:13
    #2 0x7f038ca540af in base::internal::WorkerThread::Start(base::WorkerThreadObserver*) base/task/thread_pool/worker_thread.cc:109:3
    #3 0x7f038ca49bb5 in operator() base/task/thread_pool/thread_group_impl.cc:186:15
    #4 0x7f038ca49bb5 in void base::internal::ThreadGroupImpl::ScopedCommandsExecutor::WorkerContainer::ForEachWorker<base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl()::'lambda0'(base::internal::WorkerThread*)>(base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl()::'lambda0'(base::internal::WorkerThread*)) base/task/thread_pool/thread_group_impl.cc:153:9
    #5 0x7f038ca49711 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl() base/task/thread_pool/thread_group_impl.cc:185:23
    #6 0x7f038ca3f968 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::~ScopedCommandsExecutor() base/task/thread_pool/thread_group_impl.cc:104:31
    #7 0x7f038ca43b9c in base::internal::ThreadGroupImpl::WorkerThreadDelegateImpl::DidProcessTask(base::internal::RegisteredTaskSource) base/task/thread_pool/thread_group_impl.cc:673:1
    #8 0x7f038ca55a8c in base::internal::WorkerThread::RunWorker() base/task/thread_pool/worker_thread.cc:369:16
    #9 0x7f038ca54e41 in base::internal::WorkerThread::RunPooledWorker() base/task/thread_pool/worker_thread.cc:262:3
    #10 0x7f038cb137a5 in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:96:13
    #11 0x7f034c82aea6 in start_thread nptl/pthread_create.c:477:8

Thread T9 (ThreadPoolForeg) created by T5 (ThreadPoolForeg) here:
    #0 0x562d7029134c in pthread_create /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:207:3
    #1 0x7f038cb12a0e in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, base::PlatformThreadHandle*, base::ThreadPriority) base/threading/platform_thread_posix.cc:139:13
    #2 0x7f038ca540af in base::internal::WorkerThread::Start(base::WorkerThreadObserver*) base/task/thread_pool/worker_thread.cc:109:3
    #3 0x7f038ca49bb5 in operator() base/task/thread_pool/thread_group_impl.cc:186:15
    #4 0x7f038ca49bb5 in void base::internal::ThreadGroupImpl::ScopedCommandsExecutor::WorkerContainer::ForEachWorker<base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl()::'lambda0'(base::internal::WorkerThread*)>(base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl()::'lambda0'(base::internal::WorkerThread*)) base/task/thread_pool/thread_group_impl.cc:153:9
    #5 0x7f038ca49711 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl() base/task/thread_pool/thread_group_impl.cc:185:23
    #6 0x7f038ca4246a in FlushWorkerCreation base/task/thread_pool/thread_group_impl.cc:118:5
    #7 0x7f038ca4246a in base::internal::ThreadGroupImpl::WorkerThreadDelegateImpl::GetWork(base::internal::WorkerThread*) base/task/thread_pool/thread_group_impl.cc:596:14
    #8 0x7f038ca5598d in base::internal::WorkerThread::RunWorker() base/task/thread_pool/worker_thread.cc:354:51
    #9 0x7f038ca54e41 in base::internal::WorkerThread::RunPooledWorker() base/task/thread_pool/worker_thread.cc:262:3
    #10 0x7f038cb137a5 in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:96:13
    #11 0x7f034c82aea6 in start_thread nptl/pthread_create.c:477:8

Thread T5 (ThreadPoolForeg) created by T0 (chrome) here:
    #0 0x562d7029134c in pthread_create /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:207:3
    #1 0x7f038cb12a0e in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, base::PlatformThreadHandle*, base::ThreadPriority) base/threading/platform_thread_posix.cc:139:13
    #2 0x7f038ca540af in base::internal::WorkerThread::Start(base::WorkerThreadObserver*) base/task/thread_pool/worker_thread.cc:109:3
    #3 0x7f038ca49bb5 in operator() base/task/thread_pool/thread_group_impl.cc:186:15
    #4 0x7f038ca49bb5 in void base::internal::ThreadGroupImpl::ScopedCommandsExecutor::WorkerContainer::ForEachWorker<base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl()::'lambda0'(base::internal::WorkerThread*)>(base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl()::'lambda0'(base::internal::WorkerThread*)) base/task/thread_pool/thread_group_impl.cc:153:9
    #5 0x7f038ca49711 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl() base/task/thread_pool/thread_group_impl.cc:185:23
    #6 0x7f038ca3f968 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::~ScopedCommandsExecutor() base/task/thread_pool/thread_group_impl.cc:104:31
    #7 0x7f038ca3eedb in base::internal::ThreadGroupImpl::Start(int, int, base::TimeDelta, scoped_refptr<base::SequencedTaskRunner>, base::WorkerThreadObserver*, base::internal::ThreadGroup::WorkerEnvironment, bool, absl::optional<base::TimeDelta>) base/task/thread_pool/thread_group_impl.cc:425:1
    #8 0x7f038ca4ef0f in base::internal::ThreadPoolImpl::Start(base::ThreadPoolInstance::InitParams const&, base::WorkerThreadObserver*) base/task/thread_pool/thread_pool_impl.cc:230:11
    #9 0x7f03833a0172 in content::StartBrowserThreadPool() content/browser/startup_helper.cc:95:36
    #10 0x7f03842b7840 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content/app/content_main_runner_impl.cc:1020:7
    #11 0x7f03842b7239 in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:956:12
    #12 0x7f03842b194d in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) content/app/content_main.cc:386:36
    #13 0x7f03842b1e7c in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:412:10
    #14 0x562d702d3abd in ChromeMain chrome/app/chrome_main.cc:151:12
    #15 0x7f034be04d09 in __libc_start_main csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-use-after-free components/performance_manager/persistence/site_data/site_data_impl.cc:202:14 in performance_manager::internal::SiteDataImpl::~SiteDataImpl()
Shadow bytes around the buggy address:
  0x0c0e800147e0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fa fa
  0x0c0e800147f0: fa fa fd fd fd fd fd fd fd fd fd fd fa fa fa fa
  0x0c0e80014800: fd fd fd fd fd fd fd fd fd fd fa fa fa fa 00 00
  0x0c0e80014810: 00 00 00 00 00 00 00 00 fa fa fa fa 00 00 00 00
  0x0c0e80014820: 00 00 00 00 00 00 fa fa fa fa fd fd fd fd fd fd
=>0x0c0e80014830: fd fd fd fd fa fa fa fa fd fd[fd]fd fd fd fd fd
  0x0c0e80014840: fd fd fa fa fa fa fd fd fd fd fd fd fd fd fd fa
  0x0c0e80014850: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fa fa
  0x0c0e80014860: fa fa fd fd fd fd fd fd fd fd fd fd fa fa fa fa
  0x0c0e80014870: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fd fd
  0x0c0e80014880: fd fd fd fd fd fd fd fd fa fa fa fa fd fd fd fd
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
==1756937==ABORTING


### si...@chromium.org (2021-07-22)

To improve the odds of the race falling out "right", create multiple tabs to chrome://discards/database. It is necessary for the tab to have requested at least one origin, which is why the "http:localhost:8000" is necessary for the repro. MojoJS is immaterial, as is the content loaded.
I'm leaving now and OOO tomorrow, so reassigning to Chris for further triaging or re-prioritization.

### ch...@chromium.org (2021-07-22)

Since the doesn't actually require MojoJS to trigger (that bit is a red herring), and can't actually be triggered from within a renderer, then this doesn't actually seem to be a security issue. Rather, it appears to be a run-of-the-mill UAF that can only occur during browser shutdown.

At the very least I'd suggest dropping the security labeling on this.

In the meantime, with most folks off tomorrow or on vacation I don't think anybody will be able to address this until next wekk.

### si...@chromium.org (2021-07-22)

I can repro without MojoJS. It's about 1/10 to hit the race with a bunch of chrome://discards/database tabs, all closed at the same time.
Here's my command line.
$ taskset 0x1 out/ASANRelease/chrome --user-data-dir=/tmp/x "http://localhost:8000/"


### do...@chromium.org (2021-07-22)

Thanks for investigating. A browser process UaF is still serious, but it's not web accessible and racy/only at shutdown, that takes the severity down to Medium (possibly Low but normally we just reduce severity by one level through mitigations).

### si...@chromium.org (2021-07-26)

So to be clear on how this occurs:
1. You need a tab open on chrome://discards.
2. You quit the browser.

So this is in practice a browser shutdown UAF. It should be fixed, but I don't understand the severity rating attached.

### do...@chromium.org (2021-07-27)

UaFs in the browser process are serious issues - Critical severity[1] if they are directly web accessible and High severity if they are accessible from a compromised renderer. The mitigating circumstances here bump the severity down to Medium - e.g. this issue could still be used as part of a longer chain of exploits to get control of the browser process.

1. https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md

### si...@chromium.org (2021-07-27)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cbb8d0d0e698ae0397aa8e959fda8ee22de904ba

commit cbb8d0d0e698ae0397aa8e959fda8ee22de904ba
Author: Sigurdur Asgeirsson <siggi@chromium.org>
Date: Wed Jul 28 14:13:17 2021

PM: Remove decoy member variable in discards UI.

Turns out this member variable is never assigned or used by anyone.

Bug: 1231933
Change-Id: I5f946adcf796b342f1793c3684298c16c9622b79
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3057114
Commit-Queue: Sigurður Ásgeirsson <siggi@chromium.org>
Commit-Queue: Joe Mason <joenotcharles@chromium.org>
Auto-Submit: Sigurður Ásgeirsson <siggi@chromium.org>
Reviewed-by: Joe Mason <joenotcharles@chromium.org>
Cr-Commit-Position: refs/heads/master@{#906177}

[modify] https://crrev.com/cbb8d0d0e698ae0397aa8e959fda8ee22de904ba/chrome/browser/ui/webui/discards/discards_ui.h


### gi...@appspot.gserviceaccount.com (2021-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fd490a4d868a1596720185a36f67326b509de4c2

commit fd490a4d868a1596720185a36f67326b509de4c2
Author: Sigurdur Asgeirsson <siggi@chromium.org>
Date: Wed Jul 28 20:14:13 2021

PM: Work around UAF on destruction notification.

Avoid dispatching on a deleted SiteDataCacheImpl by using a WeakPtr
for the delegate.

This CL is a quick workaround for the larger problem, which is that the
WebUI's SiteDataProviderImpl needs a teardown notification when the
SiteDataCacheImpl is unregistered and/or deleted. This would allow the
data provider to clean up before deletion of the data provider, which
could then in turn assert that no site datums are held on its destruction.

Bug: 1231933
Change-Id: Ia50464f0f3dee6ded38f1b1b84f00f0ebd79fc9a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3057116
Commit-Queue: Sigurður Ásgeirsson <siggi@chromium.org>
Reviewed-by: Sébastien Marchand <sebmarchand@chromium.org>
Reviewed-by: Chris Hamilton <chrisha@chromium.org>
Cr-Commit-Position: refs/heads/master@{#906345}

[modify] https://crrev.com/fd490a4d868a1596720185a36f67326b509de4c2/components/performance_manager/decorators/site_data_recorder_unittest.cc
[modify] https://crrev.com/fd490a4d868a1596720185a36f67326b509de4c2/components/performance_manager/persistence/site_data/site_data_cache_impl.cc
[modify] https://crrev.com/fd490a4d868a1596720185a36f67326b509de4c2/components/performance_manager/persistence/site_data/site_data_cache_impl.h
[modify] https://crrev.com/fd490a4d868a1596720185a36f67326b509de4c2/components/performance_manager/persistence/site_data/site_data_cache_impl_unittest.cc
[modify] https://crrev.com/fd490a4d868a1596720185a36f67326b509de4c2/components/performance_manager/persistence/site_data/site_data_impl.cc
[modify] https://crrev.com/fd490a4d868a1596720185a36f67326b509de4c2/components/performance_manager/persistence/site_data/site_data_impl.h
[modify] https://crrev.com/fd490a4d868a1596720185a36f67326b509de4c2/components/performance_manager/persistence/site_data/site_data_impl_unittest.cc
[modify] https://crrev.com/fd490a4d868a1596720185a36f67326b509de4c2/components/performance_manager/persistence/site_data/site_data_reader_unittest.cc
[modify] https://crrev.com/fd490a4d868a1596720185a36f67326b509de4c2/components/performance_manager/persistence/site_data/site_data_writer_unittest.cc
[modify] https://crrev.com/fd490a4d868a1596720185a36f67326b509de4c2/components/performance_manager/persistence/site_data/unittest_utils.h


### si...@chromium.org (2021-07-29)

Will this want merging to earlier milestones?

Note that AFAIK it's not possible to provoke this without explicit user interaction, as there's no way that I know of to navigate to a chrome:// page through any kind of hotlinking or even command line invocation. You'd need the user to explicitly navigate to (e.g. type in the omnibar) chrome://discards, then quit the browser.

### rz...@gmail.com (2021-07-30)

Although it could be possible to access chrome://discards via extensions, Not quite sure how to trigger this. 

### si...@chromium.org (2021-08-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-02)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-08-04)

Congratulations! The VRP Panel has decided to award you $10,000 for this report. A member of our finance team will be in touch soon to arrange payment. In the meantime, please let us know how (name or handle) you'd like to be credited for this issue. Thank you! 

### si...@chromium.org (2021-08-05)

Hey rzintct@gmail.com, congrats and thanks for your help in reproing and fixing my gaffe. Next time it'd be helpful for the hapless developer to know whether the issue (UAF or other) reproduces deterministically or else your proximate hit rate. I was going bonkers trying to repro :). Knowing your build config was sanity preserving also.

### rz...@gmail.com (2021-08-05)

[Comment Deleted]

### rz...@gmail.com (2021-08-05)

@siggi, Haha. Thank you. My inputs here are almost insignificant when compared to you identifying and pointing the exact root cause for this much complex issue. I had reasonable doubts on site data readers / writers and data cache interactions and their life times. But not quite so sure. Hence, just mentioned in the context dispatching notification to the deleted delegate. Nonetheless, huge credits to you for the exemplary analysis and fixing this in such short time. :)

### rz...@gmail.com (2021-08-05)

@amyressler, Thank you for the reward ! Please credit "Sri", for this issue. Thanks once again. 

### am...@google.com (2021-08-13)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-09-20)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-21)

[Empty comment from Monorail migration]

### rz...@google.com (2021-09-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-30)

[Empty comment from Monorail migration]

### gi...@google.com (2021-09-30)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-10-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bbcb0c00f648ddfa2257c90e1ebdffb85af9fa80

commit bbcb0c00f648ddfa2257c90e1ebdffb85af9fa80
Author: Sigurdur Asgeirsson <siggi@chromium.org>
Date: Fri Oct 01 13:12:18 2021

[M90-LTS] PM: Work around UAF on destruction notification.

Avoid dispatching on a deleted SiteDataCacheImpl by using a WeakPtr
for the delegate.

This CL is a quick workaround for the larger problem, which is that the
WebUI's SiteDataProviderImpl needs a teardown notification when the
SiteDataCacheImpl is unregistered and/or deleted. This would allow the
data provider to clean up before deletion of the data provider, which
could then in turn assert that no site datums are held on its destruction.

M90 merge issues:
  site_data_cache_impl_unittest: origin_ doesn't exist, changed to
  TestOrigin1()

(cherry picked from commit fd490a4d868a1596720185a36f67326b509de4c2)

Bug: 1231933
Change-Id: Ia50464f0f3dee6ded38f1b1b84f00f0ebd79fc9a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3057116
Commit-Queue: Sigurður Ásgeirsson <siggi@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#906345}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3181906
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Owners-Override: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1633}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/bbcb0c00f648ddfa2257c90e1ebdffb85af9fa80/components/performance_manager/persistence/site_data/site_data_writer_unittest.cc
[modify] https://crrev.com/bbcb0c00f648ddfa2257c90e1ebdffb85af9fa80/components/performance_manager/persistence/site_data/site_data_reader_unittest.cc
[modify] https://crrev.com/bbcb0c00f648ddfa2257c90e1ebdffb85af9fa80/components/performance_manager/decorators/site_data_recorder_unittest.cc
[modify] https://crrev.com/bbcb0c00f648ddfa2257c90e1ebdffb85af9fa80/components/performance_manager/persistence/site_data/site_data_impl_unittest.cc
[modify] https://crrev.com/bbcb0c00f648ddfa2257c90e1ebdffb85af9fa80/components/performance_manager/persistence/site_data/site_data_cache_impl.h
[modify] https://crrev.com/bbcb0c00f648ddfa2257c90e1ebdffb85af9fa80/components/performance_manager/persistence/site_data/site_data_impl.cc
[modify] https://crrev.com/bbcb0c00f648ddfa2257c90e1ebdffb85af9fa80/components/performance_manager/persistence/site_data/unittest_utils.h
[modify] https://crrev.com/bbcb0c00f648ddfa2257c90e1ebdffb85af9fa80/components/performance_manager/persistence/site_data/site_data_cache_impl_unittest.cc
[modify] https://crrev.com/bbcb0c00f648ddfa2257c90e1ebdffb85af9fa80/components/performance_manager/persistence/site_data/site_data_impl.h
[modify] https://crrev.com/bbcb0c00f648ddfa2257c90e1ebdffb85af9fa80/components/performance_manager/persistence/site_data/site_data_cache_impl.cc


### rz...@google.com (2021-10-01)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1231933?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056631)*
