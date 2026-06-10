# memory corruption in perfetto

| Field | Value |
|-------|-------|
| **Issue ID** | [343754425](https://issues.chromium.org/issues/343754425) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Speed>Tracing |
| **Platforms** | Linux, Windows |
| **Reporter** | em...@gmail.com |
| **Assignee** | kh...@google.com |
| **Created** | 2024-05-31 |
| **Bounty** | $2,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md

Please see the following link for instructions on filing security bugs: https://www.chromium.org/Home/chromium-security/reporting-security-bugs

Reports may be eligible for reward payments under the Chrome VRP: https://g.co/chrome/vrp

NOTE: Security bugs are normally made public once a fix has been widely deployed.

-------------------------

VULNERABILITY DETAILS

Not sure about the cause of this vulnerability, discovered by accident

VERSION
Chrome Version: 127.0.6501.0
Operating System: macos
REPRODUCTION CASE
see record video


crash
=================================================================
==95161==ERROR: AddressSanitizer: use-after-poison on address 0x7e8501742e18 at pc 0x000107035348 bp 0x00017a885b10 sp 0x00017a885b08
READ of size 8 at 0x7e8501742e18 thread T4
==95161==WARNING: invalid path to external symbolizer!
==95161==WARNING: Failed to use and restart external symbolizer!
    #0 0x107035344 in base::trace_event::TraceLog::OnStop(perfetto::DataSourceBase::StopArgs const&)+0x5e8 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x3e1344)
    #1 0x108e5d160 in perfetto::internal::TrackEventInternal::OnStop(perfetto::internal::TrackEventCategoryRegistry const&, perfetto::DataSourceBase::StopArgs const&)+0x170 (/Users/test/chromium/src/out/Default/libthird_party_perfetto_libperfetto.dylib:arm64+0x239160)
    #2 0x10701ff2c in perfetto::internal::TrackEventDataSource<base::perfetto_track_event::TrackEvent, &base::perfetto_track_event::internal::kCategoryRegistry>::OnStop(perfetto::DataSourceBase::StopArgs const&)+0x2d0 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x3cbf2c)
    #3 0x108e4291c in perfetto::internal::TracingMuxerImpl::StopDataSource_AsyncBeginImpl(perfetto::internal::TracingMuxerImpl::FindDataSourceRes const&)+0x390 (/Users/test/chromium/src/out/Default/libthird_party_perfetto_libperfetto.dylib:arm64+0x21e91c)
    #4 0x108e332fc in perfetto::internal::TracingMuxerImpl::ProducerImpl::StopDataSource(unsigned long long)+0x68 (/Users/test/chromium/src/out/Default/libthird_party_perfetto_libperfetto.dylib:arm64+0x20f2fc)
    #5 0x10871dd6c in tracing::ProducerEndpoint::StopDataSource(unsigned long long, base::OnceCallback<void ()>)+0x26c (/Users/test/chromium/src/out/Default/libtracing_cpp.dylib:arm64+0x35d6c)
    #6 0x1085786b8 in tracing::mojom::ProducerClientStubDispatch::AcceptWithResponder(tracing::mojom::ProducerClient*, mojo::Message*, std::__Cr::unique_ptr<mojo::MessageReceiverWithStatus, std::__Cr::default_delete<mojo::MessageReceiverWithStatus>>)+0x42c (/Users/test/chromium/src/out/Default/libtracing_mojom.dylib:arm64+0x1c6b8)
    #7 0x1062169a0 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*)+0x768 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x229a0)
    #8 0x10622a914 in mojo::MessageDispatcher::Accept(mojo::Message*)+0x2f8 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x36914)
    #9 0x10621ad9c in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*)+0x154 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x26d9c)
    #10 0x106236244 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*)+0x77c (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x42244)
    #11 0x10623489c in mojo::internal::MultiplexRouter::Accept(mojo::Message*)+0x418 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x4089c)
    #12 0x10622a914 in mojo::MessageDispatcher::Accept(mojo::Message*)+0x2f8 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x36914)
    #13 0x106204ff8 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>)+0x378 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x10ff8)
    #14 0x106206930 in mojo::Connector::ReadAllAvailableMessages()+0x23c (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x12930)
    #15 0x106206408 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int)+0xe8 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x12408)
    #16 0x1062085a0 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int)+0x1b8 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x145a0)
    #17 0x106207fbc in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const &+0x154 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x13fbc)
    #18 0x106207d90 in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&)+0xf0 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x13d90)
    #19 0x10511b9e8 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const &+0x164 (/Users/test/chromium/src/out/Default/libmojo_public_system_cpp.dylib:arm64+0x179e8)
    #20 0x10511b3f0 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&)+0x3a4 (/Users/test/chromium/src/out/Default/libmojo_public_system_cpp.dylib:arm64+0x173f0)
    #21 0x10511c310 in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0ul, 1ul, 2ul, 3ul>(void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>)+0x198 (/Users/test/chromium/src/out/Default/libmojo_public_system_cpp.dylib:arm64+0x18310)
    #22 0x106ddffc4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x34c (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x18bfc4)
    #23 0x106e86544 in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)+0x1fc (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x232544)
    #24 0x106e86798 in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)+0xec (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x232798)
    #25 0x106e859b4 in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&)+0x3b8 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x2319b4)
    #26 0x106e84cd8 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource)+0x544 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x230cd8)
    #27 0x106eab704 in base::internal::WorkerThread::RunWorker()+0x900 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x257704)
    #28 0x106eaaaf0 in base::internal::WorkerThread::RunPooledWorker()+0xac (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x256af0)
    #29 0x106eaa4d0 in base::internal::WorkerThread::ThreadMain()+0x1b0 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x2564d0)
    #30 0x106f28100 in base::(anonymous namespace)::ThreadFunc(void*)+0x12c (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x2d4100)
    #31 0x10579dd3c in __sanitizer_weak_hook_memcmp+0x35118 (/Users/test/chromium/src/out/Default/libclang_rt.asan_osx_dynamic.dylib:arm64+0x4dd3c)
    #32 0x18e286f90 in _pthread_start+0x84 (/usr/lib/system/libsystem_pthread.dylib:arm64+0x6f90)
    #33 0xf85000018e281d30  (<unknown module>)

Address 0x7e8501742e18 is a wild pointer inside of access range of size 0x000000000008.
SUMMARY: AddressSanitizer: use-after-poison (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x3e1344) in base::trace_event::TraceLog::OnStop(perfetto::DataSourceBase::StopArgs const&)+0x5e8
Shadow bytes around the buggy address:
  0x7e8501742b80: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7e8501742c00: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7e8501742c80: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7e8501742d00: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7e8501742d80: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 00 00
=>0x7e8501742e00: 00 00 00[00]00 00 00 00 00 00 00 00 00 00 00 00
  0x7e8501742e80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7e8501742f00: 00 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7e8501742f80: f7 f7 f7 f7 f7 00 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7e8501743000: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7e8501743080: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
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
Thread T4 created by T0 here:
    #0 0x105798abc in __sanitizer_weak_hook_memcmp+0x2fe98 (/Users/test/chromium/src/out/Default/libclang_rt.asan_osx_dynamic.dylib:arm64+0x48abc)
    #1 0x106f277e4 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType)+0x274 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x2d37e4)
    #2 0x106ea9898 in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*)+0x3b8 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x255898)
    #3 0x106e88fb4 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush()+0x4b8 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x234fb4)
    #4 0x106e889ac in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor()+0x4c (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x2349ac)
    #5 0x106e97a6c in base::internal::ThreadGroupSemaphore::Start(unsigned long, unsigned long, base::TimeDelta, scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*, base::internal::ThreadGroup::WorkerEnvironment, bool, std::__Cr::optional<base::TimeDelta>)+0x320 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x243a6c)
    #6 0x106ea25f0 in base::internal::ThreadPoolImpl::Start(base::ThreadPoolInstance::InitParams const&, base::WorkerThreadObserver*)+0x12bc (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x24e5f0)
    #7 0x1112d7d58 in content::ChildProcess::ChildProcess(base::ThreadType, std::__Cr::unique_ptr<base::ThreadPoolInstance::InitParams, std::__Cr::default_delete<base::ThreadPoolInstance::InitParams>>)+0x2ec (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x9fd58)
    #8 0x114145084 in content::RenderProcess::RenderProcess(std::__Cr::unique_ptr<base::ThreadPoolInstance::InitParams, std::__Cr::default_delete<base::ThreadPoolInstance::InitParams>>)+0x20 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x2f0d084)
    #9 0x1141451ec in content::RenderProcessImpl::RenderProcessImpl()+0x108 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x2f0d1ec)
    #10 0x11416bc9c in content::RendererMain(content::MainFunctionParams)+0x39c (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x2f33c9c)
    #11 0x11432d39c in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x23c (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x30f539c)
    #12 0x11432f158 in content::ContentMainRunnerImpl::Run()+0x460 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x30f7158)
    #13 0x11432b360 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x670 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x30f3360)
    #14 0x11432bc18 in content::ContentMain(content::ContentMainParams)+0x190 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x30f3c18)
    #15 0x11b11ae6c in ChromeMain+0x338 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0xae6c)
    #16 0x104880ce4 in main+0x254 (/Users/test/chromium/src/out/Default/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/127.0.6501.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer):arm64+0x100000ce4)
    #17 0x18defe0dc  (<unknown module>)
    #18 0xb245fffffffffffc  (<unknown module>)


==95161==ADDITIONAL INFO

==95161==Note: Please include this section with the ASan report.
Task trace:
    #0 0x10511bdd0 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int)+0x248 (/Users/test/chromium/src/out/Default/libmojo_public_system_cpp.dylib:arm64+0x17dd0)



## Attachments

- [reproduce.mov](attachments/reproduce.mov) (video/quicktime, 33.1 MB)

## Timeline

### za...@google.com (2024-06-03)

Hi eseckler@ can you please take a look at this trace_event related issue? I was not able to reproduce it. Can you please help us identify whether this is a security vulnerability? Thank you. 

### es...@google.com (2024-06-04)

Zack, is there a way for us to tell which access within OnStop is the problematic one here?

Would we have to build the binary to identify which access is at `base::trace_event::TraceLog::OnStop(perfetto::DataSourceBase::StopArgs const&)+0x5e8`? I'm assuming this is an official ASAN build at 127.0.6501.0 for arm64 macos?

+khokhlov or +etiennep may be able to look into this further if this is possible somehow.

### es...@google.com (2024-06-04)

If I were to guess, maybe there's a TraceLog observer that doesn't get removed when it is destroyed? TraceLog itself is a singleton no-destructor, so its own property accesses should be pretty safe.

### kh...@google.com (2024-06-04)

I believe it's a duplicate of [issue 40067111](https://issues.chromium.org/issues/40067111)

### ha...@gmail.com (2024-06-18)

Hi,

Has it been fixed? Why can I still reproduce it on 128.0.6541.0?

### es...@google.com (2024-06-18)

Let's discuss in the duplicate issue. Adding you there as cc.

### ha...@gmail.com (2024-07-30)

Any update here?This seems to be a race problem. I seem to be able to reproduce the steps stably, but it seems to take many attempts.

### za...@google.com (2024-07-30)

Thanks for following up, this bug seems to be a duplicate issue. Can you please follow up there? Thanks! 

### pe...@google.com (2025-01-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/343754425)*
