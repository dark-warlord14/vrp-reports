# ipcz bug can allow renderer duplicate browser process handle to escape sandbox

| Field | Value |
|-------|-------|
| **Issue ID** | [503197487](https://issues.chromium.org/issues/503197487) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Mojo>Core |
| **Platforms** | Windows |
| **Chrome Version** | 135.0.0.0 |
| **Reporter** | ha...@gmail.com |
| **Assignee** | aj...@chromium.org |
| **Created** | 2026-04-16 |
| **Bounty** | $250,000.00 |

## Description

# Steps to reproduce the problem

### Reproduce Crash

1. Download brokerhost\_lifecycle.patch (attached)
2. Apply patch using `git apply brokerhost_lifecycle.patch`
3. Here's out/asan/args.gn

```
# Set build arguments here. See `gn help buildargs`.
is_asan = true
is_clang = true
is_debug = false

symbol_level = 2
is_component_build = true
enable_nacl = false

```

4. Compile chromium
5. Run chromium with tracking flag `ASAN_OPTIONS="detect_odr_violation=0" ./out/asan/chrome --track-brokerhost`
6. Use normally for a while, and it will crash

### Reproduce Code Execution

1. Download exploit.patch (attached)
2. Apply using `git apply exploit.patch` and compile the chromium binary
3. Open terminal1 and run nc -nvlp 1234
4. Open terminal2 and run `ASAN_OPTIONS="detect_odr_violation=0" ./out/asan/chrome --rce-shell`

# Problem Description

A use-after-free vulnerability exists in `mojo::core::BrokerHost` where a deferred task can access a BrokerHost object after it has been deleted via `OnChannelError()`. This vulnerability is triggerable from a compromised renderer process and allows memory corruption leading to potential sandbox escape and arbitrary code execution in the browser process.

# Summary

`mojo::core::BrokerHost::OnChannelError()` can be exploited to achieve Remote Code Execution

# Custom Questions

#### Type of crash:

browser

#### Crash state:

==1218107==ERROR: AddressSanitizer: heap-use-after-free on address 0x720fa24e3948 at pc 0x75e048f3df4d bp 0x71df84b03030 sp 0x71df84b03028
READ of size 8 at 0x720fa24e3948 thread T22 (Chrome\_IOThread)
#0 0x75e048f3df4c in mojo::core::BrokerHost::OnBufferRequest(unsigned int) base/memory/scoped\_refptr.h:292:12
#1 0x75e048f3f0f0 in base::internal::Invoker<base::internal::FunctorTraits<mojo::core::BrokerHost::OnChannelError(mojo::core::Channel::Error)::$\_0&&, mojo::core::BrokerHost\*&&>, base::internal::BindState<false, false, false, mojo::core::BrokerHost::OnChannelError(mojo::core::Channel::Error)::$\_0, base::internal::UnretainedWrapper<mojo::core::BrokerHost, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase\*) mojo/core/broker\_host.cc:209:22
#2 0x75e04a88291d in base::OnceCallback<void ()>::Run() && base/functional/callback.h:155:12
#3 0x75e04aadcef0 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task\_annotator.cc:229:34
#4 0x75e04ab84cbe in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) base/task/common/task\_annotator.h:112:5
#5 0x75e04ab83027 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:336:40
#6 0x75e04ada7ad8 in base::MessagePumpEpoll::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_epoll.cc:224:55
#7 0x75e04ab86c9f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:640:12
#8 0x75e04aa2de59 in base::RunLoop::Run(base::Location const&) base/run\_loop.cc:135:14
#9 0x75e04ac57c42 in base::Thread::Run(base::RunLoop\*) base/threading/thread.cc:356:13
#10 0x75e0265e52ef in content::BrowserProcessIOThread::IOThreadRun(base::RunLoop\*) content/browser/browser\_process\_io\_thread.cc:104:11
#11 0x75e0265e516d in content::BrowserProcessIOThread::Run(base::RunLoop\*) content/browser/browser\_process\_io\_thread.cc:84:3
#12 0x75e04ac5847e in base::Thread::ThreadMain() base/threading/thread.cc:426:3
#13 0x75e04acd183c in base::(anonymous namespace)::ThreadFunc(void\*) base/threading/platform\_thread\_posix.cc:102:13
#14 0x62d2ead25cd6 in asan\_thread\_start(void\*) asan\_interceptors.cpp

0x720fa24e3948 is located 24 bytes inside of 32-byte region [0x720fa24e3930,0x720fa24e3950)
freed by thread T22 (Chrome\_IOThread) here:
#0 0x62d2ead61f62 in operator delete(void\*, unsigned long) (/home/lukee/Documents/Research/chromium/src/out/asan/chrome+0x7dd8f62) (BuildId: 428b50c9020d33cc)
#1 0x75e048f3e81d in mojo::core::BrokerHost::OnChannelError(mojo::core::Channel::Error) mojo/core/broker\_host.cc:220:3
#2 0x75e048f2461d in mojo::core::ChannelPosix::OnFdReadable(int) mojo/core/channel\_posix.cc
#3 0x75e04adad723 in base::MessagePumpEpoll::HandleEvent(int, bool, bool, base::MessagePumpEpoll::FdWatchController\*) base/message\_loop/message\_pump\_epoll.cc:760:13
#4 0x75e04adac3d6 in base::MessagePumpEpoll::OnEpollEvent(base::MessagePumpEpoll::EpollEventEntry&, unsigned int) base/message\_loop/message\_pump\_epoll.cc:614:7
#5 0x75e04ada9092 in base::MessagePumpEpoll::WaitForEpollEvents(base::TimeDelta) base/message\_loop/message\_pump\_epoll.cc:506:7
#6 0x75e04ada7a6a in base::MessagePumpEpoll::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_epoll.cc:285:5
#7 0x75e04ab86c9f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:640:12
#8 0x75e04aa2de59 in base::RunLoop::Run(base::Location const&) base/run\_loop.cc:135:14
#9 0x75e04ac57c42 in base::Thread::Run(base::RunLoop\*) base/threading/thread.cc:356:13
#10 0x75e0265e52ef in content::BrowserProcessIOThread::IOThreadRun(base::RunLoop\*) content/browser/browser\_process\_io\_thread.cc:104:11
#11 0x75e0265e516d in content::BrowserProcessIOThread::Run(base::RunLoop\*) content/browser/browser\_process\_io\_thread.cc:84:3
#12 0x75e04ac5847e in base::Thread::ThreadMain() base/threading/thread.cc:426:3
#13 0x75e04acd183c in base::(anonymous namespace)::ThreadFunc(void\*) base/threading/platform\_thread\_posix.cc:102:13
#14 0x62d2ead25cd6 in asan\_thread\_start(void\*) asan\_interceptors.cpp

previously allocated by thread T22 (Chrome\_IOThread) here:
#0 0x62d2ead6135d in operator new(unsigned long) (/home/lukee/Documents/Research/chromium/src/out/asan/chrome+0x7dd835d) (BuildId: 428b50c9020d33cc)
#1 0x75e048ee5fb9 in mojo::core::ipcz\_driver::(anonymous namespace)::CreateBrokerHostOnIOThread(mojo::PlatformChannelEndpoint) mojo/core/ipcz\_driver/base\_shared\_memory\_service.cc:44:3
#2 0x75e048ee620f in base::internal::Invoker<base::internal::FunctorTraits<void (*&&)(mojo::PlatformChannelEndpoint), mojo::PlatformChannelEndpoint&&>, base::internal::BindState<false, true, false, void (*)(mojo::PlatformChannelEndpoint), mojo::PlatformChannelEndpoint>, void ()>::RunOnce(base::internal::BindStateBase\*) base/functional/bind\_internal.h:673:12
#3 0x75e04a88291d in base::OnceCallback<void ()>::Run() && base/functional/callback.h:155:12
#4 0x75e04aadcef0 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task\_annotator.cc:229:34
#5 0x75e04ab84cbe in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) base/task/common/task\_annotator.h:112:5
#6 0x75e04ab83027 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:336:40
#7 0x75e04ada7ad8 in base::MessagePumpEpoll::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_epoll.cc:224:55
#8 0x75e04ab86c9f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:640:12
#9 0x75e04aa2de59 in base::RunLoop::Run(base::Location const&) base/run\_loop.cc:135:14
#10 0x75e04ac57c42 in base::Thread::Run(base::RunLoop\*) base/threading/thread.cc:356:13
#11 0x75e0265e52ef in content::BrowserProcessIOThread::IOThreadRun(base::RunLoop\*) content/browser/browser\_process\_io\_thread.cc:104:11
#12 0x75e0265e516d in content::BrowserProcessIOThread::Run(base::RunLoop\*) content/browser/browser\_process\_io\_thread.cc:84:3
#13 0x75e04ac5847e in base::Thread::ThreadMain() base/threading/thread.cc:426:3
#14 0x75e04acd183c in base::(anonymous namespace)::ThreadFunc(void\*) base/threading/platform\_thread\_posix.cc:102:13
#15 0x62d2ead25cd6 in asan\_thread\_start(void\*) asan\_interceptors.cpp

Thread T22 (Chrome\_IOThread) created by T0 (chrome) here:
#0 0x62d2ead0bb51 in pthread\_create (/home/lukee/Documents/Research/chromium/src/out/asan/chrome+0x7d82b51) (BuildId: 428b50c9020d33cc)
#1 0x75e04acd0ee9 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate\*, base::PlatformThreadHandle\*, base::ThreadType, base::MessagePumpType) base/threading/platform\_thread\_posix.cc:153:13
#2 0x75e04ac56364 in base::Thread::StartWithOptions(base::Thread::Options) base/threading/thread.cc:232:26
#3 0x75e0281181f6 in content::BrowserTaskExecutor::CreateIOThread() content/browser/scheduler/browser\_task\_executor.cc:304:19
#4 0x75e02a1ea5a1 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content\_main\_runner\_impl.cc:1282:42
#5 0x75e02a1e9631 in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner\_impl.cc:1150:12
#6 0x75e02a1e3243 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) content/app/content\_main.cc:356:36
#7 0x75e02a1e35ca in content::ContentMain(content::ContentMainParams) content/app/content\_main.cc:369:10
#8 0x62d2ead632b4 in ChromeMain chrome/app/chrome\_main.cc:194:12
#9 0x75dfb3629d8f in \_\_libc\_start\_call\_main csu/../sysdeps/nptl/libc\_start\_call\_main.h:58:16

SUMMARY: AddressSanitizer: heap-use-after-free base/memory/scoped\_refptr.h:292:12 in mojo::core::BrokerHost::OnBufferRequest(unsigned int)
Shadow bytes around the buggy address:
0x720fa24e3680: f7 fa fd fd fd fd f7 fa fd fd fd fa f7 fa fd fd
0x720fa24e3700: fd fd f7 fa fd fd fd fd f7 fa fd fd fd fd f7 fa
0x720fa24e3780: fd fd fd fa f7 fa fd fd fd fd f7 fa fd fd fd fd
0x720fa24e3800: f7 fa fd fd fd fd f7 fa fd fd fd fd f7 fa fd fd
0x720fa24e3880: fd fa f7 fa fd fd fd fa f7 fa fd fd fd fd f7 fa
=>0x720fa24e3900: fd fd fd fa f7 fa fd fd fd[fd]f7 fa fd fd fd fd
0x720fa24e3980: f7 fa fd fd fd fd f7 fa fd fd fd fd f7 fa fd fd
0x720fa24e3a00: fd fd f7 fa fd fd fd fd f7 fa fd fd fd fd f7 fa
0x720fa24e3a80: fd fd fd fd f7 fa fd fd fd fd f7 fa fd fd fd fd
0x720fa24e3b00: f7 fa fd fd fd fd f7 fa fd fd fd fd f7 fa fd fd
0x720fa24e3b80: fd fd f7 fa fd fd fd fd f7 fa fd fd fd fa f7 fa
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

==1218107==ADDITIONAL INFO

==1218107==Note: Please include this section with the ASan report.
Task trace:
#0 0x75e048f3e665 in mojo::core::BrokerHost::OnChannelError(mojo::core::Channel::Error) mojo/core/broker\_host.cc:204:9

Command line: `./out/asan/chrome --track-brokerhost --enable-logging --log-file=/tmp/chrome.log --v=1 --flag-switches-begin --flag-switches-end --ozone-platform=wayland --render-node-override=/dev/dri/renderD128`

#### Reporter credit:

Shulkhan Efendi

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [exploit.patch](attachments/exploit.patch) (text/x-diff, 2.7 KB)
- [asan.log](attachments/asan.log) (text/plain, 13.9 KB)
- [brokerhost_lifecycle.patch](attachments/brokerhost_lifecycle.patch) (text/x-diff, 2.1 KB)
- [exploit.mp4](attachments/exploit.mp4) (video/mp4, 4.0 MB)

## Timeline

### ts...@google.com (2026-04-16)

You'll need to demonstrate the UaF without the patch.

### ch...@google.com (2026-04-16)

This issue has been closed as an incomplete or invalid report and we will not respond to further comments. If you can improve your report please open a fresh issue that addresses any feedback provided.

For more information on our vulnerability policies, please refer to <https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md>

### mu...@gmail.com (2026-04-16)

Based on the rules under “Reports of memory safety issues must:”, am I correct that I can attach a minimized PoC or a patch?

As stated in the Chrome VRP rules (<https://bughunters.google.com/about/rules/chrome-friends/chrome-vulnerability-reward-program-rules>), the section explicitly mentions that submissions can include a “minimized PoC or patch.”

Additionally, there are existing reports that include a patch as part of the submission, for example: <https://issues.chromium.org/issues/412578726>

So I would like to confirm that providing a patch alone is acceptable.

### ch...@google.com (2026-07-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/503197487)*
