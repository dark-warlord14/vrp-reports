# AddressSanitizer: use-after-poison connector.cc:546 in mojo::Connector::DispatchMessageW

| Field | Value |
|-------|-------|
| **Issue ID** | [40056521](https://issues.chromium.org/issues/40056521) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Messaging, Internals>Mojo>Bindings |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2021-07-13 |
| **Bounty** | $7,500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4494.0 Safari/537.36

Steps to reproduce the problem:
#TestOn
Windows NT 10.0; Win64; x64
gs://chromium-browser-asan/win32-release_x64/asan-win32-release_x64-898565.zip

#Reproduce
1.python -m http.server 8000
2.chrome.exe --enable-blink-test-features --single-process --user-data-dir=0707 http://localhost:8000/fuzz-00006.html http://localhost:8000/fuzz-00006.html http://localhost:8000/fuzz-00006.html http://localhost:8000/fuzz-00006.html http://localhost:8000/fuzz-00006.html
3.wait 60 second,if not succeed,try again.

There is minicase in the min directory, but my test reproduction is not very stable, org is the original sample

The attached video has a reproduction process

What is the expected behavior?

What went wrong?

Type of crash
browser

#asan
=================================================================
==14416==ERROR: AddressSanitizer: use-after-poison on address 0x7ea69bc23c88 at pc 0x7ff916d4b188 bp 0x0056b69fee00 sp 0x0056b69fee48
READ of size 8 at 0x7ea69bc23c88 thread T38
==14416==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ff916d4b187 in mojo::Connector::DispatchMessageW C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:546
    #1 0x7ff916d4c35d in mojo::Connector::ReadAllAvailableMessages C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:604
    #2 0x7ff916d9c2c6 in mojo::SimpleWatcher::OnHandleReady C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple_watcher.cc:278
    #3 0x7ff91692184a in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:178
    #4 0x7ff9190b5d83 in base::sequence_manager::internal::ThreadControllerImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_impl.cc:199
    #5 0x7ff9190b8903 in base::internal::Invoker<base::internal::BindState<void (base::sequence_manager::internal::ThreadControllerImpl::*)(base::sequence_manager::internal::ThreadControllerImpl::WorkType),base::WeakPtr<base::sequence_manager::internal::ThreadControllerImpl>,base::sequence_manager::internal::ThreadControllerImpl::WorkType>,void ()>::Run C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:703
    #6 0x7ff91692184a in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:178
    #7 0x7ff9190baa63 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:360
    #8 0x7ff9190ba0d2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:260
    #9 0x7ff9169cd336 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:220
    #10 0x7ff9169cb4b8 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78
    #11 0x7ff9190bbf2e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:467
    #12 0x7ff9168a57a3 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #13 0x7ff916969ee9 in base::Thread::Run C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:341
    #14 0x7ff91696a400 in base::Thread::ThreadMain C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:412
    #15 0x7ff9169eebff in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:121
    #16 0x7ff70a561037 in __asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_thread.cpp:278
    #17 0x7ff9b5147033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)
    #18 0x7ff9b6362650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

Address 0x7ea69bc23c88 is a wild pointer inside of access range of size 0x000000000008.
SUMMARY: AddressSanitizer: use-after-poison C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:546 in mojo::Connector::DispatchMessageW
Shadow bytes around the buggy address:
  0x1199f3084740: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x1199f3084750: 00 00 00 f7 00 00 00 00 00 00 00 00 00 00 00 00
  0x1199f3084760: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x1199f3084770: 00 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x1199f3084780: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
=>0x1199f3084790: f7[f7]f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 00 00
  0x1199f30847a0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x1199f30847b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 f7 00 00
  0x1199f30847c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x1199f30847d0: 00 00 00 00 00 00 00 00 00 00 00 00 f7 f7 f7 f7
  0x1199f30847e0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
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
Thread T38 created by T0 here:
    #0 0x7ff70a561aa2 in __asan_wrap_CreateThread C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_win.cpp:146
    #1 0x7ff9169edfde in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:185
    #2 0x7ff91696910d in base::Thread::StartWithOptions C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:216
    #3 0x7ff910b29211 in content::RenderProcessHostImpl::Init C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_process_host_impl.cc:1992
    #4 0x7ff910b0bfa6 in content::RenderFrameHostManager::InitRenderView C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:2870
    #5 0x7ff910b02eb5 in content::RenderFrameHostManager::ReinitializeMainRenderFrame C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:3106
    #6 0x7ff910b00714 in content::RenderFrameHostManager::GetFrameHostForNavigation C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:1071
    #7 0x7ff910aff29a in content::RenderFrameHostManager::DidCreateNavigationRequest C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:826
    #8 0x7ff91087c1d9 in content::FrameTreeNode::CreatedNavigationRequest C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\frame_tree_node.cc:536
    #9 0x7ff910a35187 in content::Navigator::Navigate C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\navigator.cc:585
    #10 0x7ff9109a9edf in content::NavigationControllerImpl::NavigateWithoutEntry C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\navigation_controller_impl.cc:3231
    #11 0x7ff9109a901a in content::NavigationControllerImpl::LoadURLWithParams C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\navigation_controller_impl.cc:1093
    #12 0x7ff918b64092 in `anonymous namespace'::LoadURLInContents C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser_navigator.cc:387
    #13 0x7ff918b61444 in Navigate C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser_navigator.cc:659
    #14 0x7ff9200b584b in StartupBrowserCreatorImpl::OpenTabsInBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:320
    #15 0x7ff9200b7654 in StartupBrowserCreatorImpl::RestoreOrCreateBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:591
    #16 0x7ff9200b49e2 in StartupBrowserCreatorImpl::DetermineURLsAndLaunch C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:435
    #17 0x7ff9200b4084 in StartupBrowserCreatorImpl::Launch C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:224
    #18 0x7ff91c0648bc in StartupBrowserCreator::LaunchBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:590
    #19 0x7ff91c0677ce in StartupBrowserCreator::ProcessLastOpenedProfiles C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1194
    #20 0x7ff91c066921 in StartupBrowserCreator::LaunchBrowserForLastProfiles C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:681
    #21 0x7ff91c06a64e in StartupBrowserCreator::StartupLaunchAfterProtocolHandler C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1147
    #22 0x7ff91c063d73 in StartupBrowserCreator::ProcessCmdLineImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1107
    #23 0x7ff91c06231d in StartupBrowserCreator::Start C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:526
    #24 0x7ff9192110ac in ChromeBrowserMainParts::PreMainMessageLoopRunImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc:1684
    #25 0x7ff91920eb76 in ChromeBrowserMainParts::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc:1054
    #26 0x7ff91000340c in content::BrowserMainLoop::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:946
    #27 0x7ff910ddb0cf in content::StartupTaskRunner::RunAllTasksNow C:\b\s\w\ir\cache\builder\src\content\browser\startup_task_runner.cc:41
    #28 0x7ff910002912 in content::BrowserMainLoop::CreateStartupTasks C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:854
    #29 0x7ff91000a335 in content::BrowserMainRunnerImpl::Initialize C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:131
    #30 0x7ff90fffeed8 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:43
    #31 0x7ff91662e16c in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:595
    #32 0x7ff916630ac8 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1084
    #33 0x7ff91662fc7e in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:953
    #34 0x7ff91662d01a in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:386
    #35 0x7ff91662d633 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:412
    #36 0x7ff90c2f145a in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:151
    #37 0x7ff70a4b5bb4 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:169
    #38 0x7ff70a4b2be8 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:382
    #39 0x7ff70a89eadf in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #40 0x7ff9b5147033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)
    #41 0x7ff9b6362650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

==14416==ABORTING

Did this work before? N/A 

Chrome version: 92.0.4494.0  Channel: n/a
OS Version: 10.0

There are a lot of related files needed to reproduce, so I made a zip package

## Attachments

- [poc.zip](attachments/poc.zip) (application/octet-stream, 267.7 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 10.7 KB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [patch.diff](attachments/patch.diff) (text/plain, 701 B)

## Timeline

### [Deleted User] (2021-07-13)

[Empty comment from Monorail migration]

### jd...@chromium.org (2021-07-14)

Thanks for the report. I've been unable to reproduce, and there aren't any clear leads in the stack trace.

Are you able to reproduce this without the --single-process flag? Have you been able to do any root cause analysis?

I'm tentatively assigning this impact-none, since --single-process isn't a supported configuration, but I'd be happy to be shown to be wrong.

### aj...@chromium.org (2021-07-14)

I also cannot repro on Windows with build 898565.

It would be great to see a reliable, minimized testcase that works without the --single-process flag (you may need to run asan with --no-sandbox to view a stacktrace).

### m....@gmail.com (2021-07-17)

https://crbug.com/chromium/1228661#c2 
Thank you for your suggestion, it can be reproduced without using --single-process flags.

I haven't analyzed it in depth yet. The current guess is that incoming_receiver_[1] was released early, and I am still analyzing it when I have time.

I have provided a new replay video here，You can open a few more pages manually to increase the chance of reproducing the problem.

``` 
 mojo/public/cpp/bindings/lib/connector.cc:546
 if (connection_group_)
    message.set_receiver_connection_group(&connection_group_);
  bool receiver_result =
      incoming_receiver_ && incoming_receiver_->Accept(&message); [1]
  if (!weak_self)
    return receiver_result;
``` 


### [Deleted User] (2021-07-17)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### m....@gmail.com (2021-07-20)

I compiled a debug version test, this poc may crash in multiple places in the debug version, but I think the following crash location is the key point.
By the way, this is a Renderer crash, the initial statement was wrong.

```
9:038> r
rax=2a2a2a2a2a2a2a2a rbx=0000000000000000 rcx=2a2a2a2a2a2a2a2a
rdx=2a2a2a2a2a2a2a2a rsi=0000000000000000 rdi=0000000000000000
rip=00007ffc69d13839 rsp=0000002e1f7fd7b0 rbp=0000000000000000
 r8=000000002a2a2a2a  r9=00007ffc6d5fb4ac r10=000000000000024d
r11=0000002e1f7fda40 r12=0000000000000000 r13=0000000000000000
r14=0000000000000000 r15=0000000000000000
iopl=0         nv up ei pl nz na po nc
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010206
blink_core!blink::MemberBase<blink::EventListener,blink::TracenessMemberConfiguration::kTraced>::GetRaw+0x9:
00007ffc`69d13839 488b00          mov     rax,qword ptr [rax] ds:2a2a2a2a`2a2a2a2a=????????????????

9:038> k
 # Child-SP          RetAddr               Call Site
00 0000002e`1f7fd7b0 00007ffc`69d13823     blink_core!blink::MemberBase<blink::EventListener,blink::TracenessMemberConfiguration::kTraced>::GetRaw+0x9 [E:\v8\chromium\src\third_party\blink\renderer\platform\heap\impl\member.h @ 257] 
01 0000002e`1f7fd7c0 00007ffc`69d481c2     blink_core!blink::MemberBase<blink::EventListener,blink::TracenessMemberConfiguration::kTraced>::operator blink::EventListener *+0x13 [E:\v8\chromium\src\third_party\blink\renderer\platform\heap\impl\member.h @ 187] 
02 0000002e`1f7fd7f0 00007ffc`69d47332     blink_core!blink::MemberBase<blink::EventListener,blink::TracenessMemberConfiguration::kTraced>::MemberBase+0x22 [E:\v8\chromium\src\third_party\blink\renderer\platform\heap\impl\member.h @ 116] 
03 0000002e`1f7fd830 00007ffc`69d472f2     blink_core!blink::Member<blink::EventListener>::Member+0x22 [E:\v8\chromium\src\third_party\blink\renderer\platform\heap\impl\member.h @ 294] 
04 0000002e`1f7fd870 00007ffc`69d3e24b     blink_core!blink::RegisteredEventListener::RegisteredEventListener+0x22 [E:\v8\chromium\src\third_party\blink\renderer\core\dom\events\registered_event_listener.cc @ 54] 
05 0000002e`1f7fd8b0 00007ffc`69d3da47     blink_core!blink::EventTarget::FireEventListeners+0x2fb [E:\v8\chromium\src\third_party\blink\renderer\core\dom\events\event_target.cc @ 883] 
06 0000002e`1f7fda80 00007ffc`69d3d7f7     blink_core!blink::EventTarget::FireEventListeners+0x237 [E:\v8\chromium\src\third_party\blink\renderer\core\dom\events\event_target.cc @ 818] 
07 0000002e`1f7fdb40 00007ffc`69d3d787     blink_core!blink::EventTarget::DispatchEventInternal+0x57 [E:\v8\chromium\src\third_party\blink\renderer\core\dom\events\event_target.cc @ 725] 
08 0000002e`1f7fdb90 00007ffc`6b41cc79     blink_core!blink::EventTarget::DispatchEvent+0x57 [E:\v8\chromium\src\third_party\blink\renderer\core\dom\events\event_target.cc @ 718] 
09 0000002e`1f7fdbe0 00007ffc`cc14cb29     blink_core!blink::MessagePort::Accept+0x309 [E:\v8\chromium\src\third_party\blink\renderer\core\messaging\message_port.cc @ 293] 
0a 0000002e`1f7fdda0 00007ffc`cc14dc96     bindings!mojo::Connector::DispatchMessageW+0x469 [E:\v8\chromium\src\mojo\public\cpp\bindings\lib\connector.cc @ 548] 
0b 0000002e`1f7fdf00 00007ffc`cc14d8b2     bindings!mojo::Connector::ReadAllAvailableMessages+0x1f6 [E:\v8\chromium\src\mojo\public\cpp\bindings\lib\connector.cc @ 608] 
0c 0000002e`1f7fe090 00007ffc`cc14d7fb     bindings!mojo::Connector::OnHandleReadyInternal+0xa2 [E:\v8\chromium\src\mojo\public\cpp\bindings\lib\connector.cc @ 441] 
0d 0000002e`1f7fe0f0 00007ffc`cc154fa5     bindings!mojo::Connector::OnWatcherHandleReady+0x1b [E:\v8\chromium\src\mojo\public\cpp\bindings\lib\connector.cc @ 411] 
0e 0000002e`1f7fe130 00007ffc`cc154edd     bindings!base::internal::FunctorTraits<void (mojo::Connector::*)(unsigned int),void>::Invoke<void (mojo::Connector::*)(unsigned int),mojo::Connector *,unsigned int>+0x45 [E:\v8\chromium\src\base\bind_internal.h @ 509] 
0f 0000002e`1f7fe180 00007ffc`cc154e71     bindings!base::internal::InvokeHelper<0,void>::MakeItSo<void (mojo::Connector::*const &)(unsigned int),mojo::Connector *,unsigned int>+0x4d [E:\v8\chromium\src\base\bind_internal.h @ 648] 
10 0000002e`1f7fe1d0 00007ffc`cc154dde     bindings!base::internal::Invoker<base::internal::BindState<void (mojo::Connector::*)(unsigned int),base::internal::UnretainedWrapper<mojo::Connector> >,void (unsigned int)>::RunImpl<void (mojo::Connector::*const &)(unsigned int),const std::tuple<base::internal::UnretainedWrapper<mojo::Connector> > &,0>+0x71 [E:\v8\chromium\src\base\bind_internal.h @ 721] 
11 0000002e`1f7fe230 00007ffc`cc150d51     bindings!base::internal::Invoker<base::internal::BindState<void (mojo::Connector::*)(unsigned int),base::internal::UnretainedWrapper<mojo::Connector> >,void (unsigned int)>::Run+0x5e [E:\v8\chromium\src\base\bind_internal.h @ 703] 
12 0000002e`1f7fe280 00007ffc`cc150500     bindings!base::RepeatingCallback<void (unsigned int)>::Run+0x71 [E:\v8\chromium\src\base\callback.h @ 166] 
13 0000002e`1f7fe2e0 00007ffc`cc1508d6     bindings!mojo::SimpleWatcher::DiscardReadyState+0x20 [E:\v8\chromium\src\mojo\public\cpp\system\simple_watcher.h @ 190] 
14 0000002e`1f7fe320 00007ffc`cc1507f6     bindings!base::internal::FunctorTraits<void (*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),void>::Invoke<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),const base::RepeatingCallback<void (unsigned int)> &,unsigned int,const mojo::HandleSignalsState &>+0x66 [E:\v8\chromium\src\base\bind_internal.h @ 404] 
15 0000002e`1f7fe380 00007ffc`cc150771     bindings!base::internal::InvokeHelper<0,void>::MakeItSo<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),const base::RepeatingCallback<void (unsigned int)> &,unsigned int,const mojo::HandleSignalsState &>+0x66 [E:\v8\chromium\src\base\bind_internal.h @ 648] 
16 0000002e`1f7fe3e0 00007ffc`cc1506dc     bindings!base::internal::Invoker<base::internal::BindState<void (*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),base::RepeatingCallback<void (unsigned int)> >,void (unsigned int, const mojo::HandleSignalsState &)>::RunImpl<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),const std::tuple<base::RepeatingCallback<void (unsigned int)> > &,0>+0x81 [E:\v8\chromium\src\base\bind_internal.h @ 721] 
17 0000002e`1f7fe440 00007ffc`db4aa65a     bindings!base::internal::Invoker<base::internal::BindState<void (*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),base::RepeatingCallback<void (unsigned int)> >,void (unsigned int, const mojo::HandleSignalsState &)>::Run+0x7c [E:\v8\chromium\src\base\bind_internal.h @ 703] 
18 0000002e`1f7fe4b0 00007ffc`db4aa2d9     mojo_public_system_cpp!base::RepeatingCallback<void (unsigned int, const mojo::HandleSignalsState &)>::Run+0x8a [E:\v8\chromium\src\base\callback.h @ 166] 
19 0000002e`1f7fe520 00007ffc`db4ab100     mojo_public_system_cpp!mojo::SimpleWatcher::OnHandleReady+0x179 [E:\v8\chromium\src\mojo\public\cpp\system\simple_watcher.cc @ 279] 
1a 0000002e`1f7fe5c0 00007ffc`db4aaf54     mojo_public_system_cpp!base::internal::FunctorTraits<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &),void>::Invoke<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr<mojo::SimpleWatcher>,int,unsigned int,mojo::HandleSignalsState>+0x80 [E:\v8\chromium\src\base\bind_internal.h @ 509] 
1b 0000002e`1f7fe630 00007ffc`db4aae8a     mojo_public_system_cpp!base::internal::InvokeHelper<1,void>::MakeItSo<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr<mojo::SimpleWatcher>,int,unsigned int,mojo::HandleSignalsState>+0xa4 [E:\v8\chromium\src\base\bind_internal.h @ 671] 
1c 0000002e`1f7fe6a0 00007ffc`db4aadc5     mojo_public_system_cpp!base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr<mojo::SimpleWatcher>,int,unsigned int,mojo::HandleSignalsState>,void ()>::RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &),std::tuple<base::WeakPtr<mojo::SimpleWatcher>,int,unsigned int,mojo::HandleSignalsState>,0,1,2,3>+0xba [E:\v8\chromium\src\base\bind_internal.h @ 721] 
1d 0000002e`1f7fe710 00007ffc`ceaa1a97     mojo_public_system_cpp!base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr<mojo::SimpleWatcher>,int,unsigned int,mojo::HandleSignalsState>,void ()>::RunOnce+0x55 [E:\v8\chromium\src\base\bind_internal.h @ 690] 
1e 0000002e`1f7fe760 00007ffc`cecb7502     base!base::OnceCallback<void ()>::Run+0x77 [E:\v8\chromium\src\base\callback.h @ 99] 
1f 0000002e`1f7fe7b0 00007ffc`ced0a7ab     base!base::TaskAnnotator::RunTask+0x4f2 [E:\v8\chromium\src\base\task\common\task_annotator.cc @ 180] 
20 0000002e`1f7fe930 00007ffc`ced09d26     base!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl+0x77b [E:\v8\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 361] 
21 0000002e`1f7feb10 00007ffc`ceb6d1e1     base!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork+0x126 [E:\v8\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 260] 
22 0000002e`1f7fec40 00007ffc`ced0b31f     base!base::MessagePumpDefault::Run+0x91 [E:\v8\chromium\src\base\message_loop\message_pump_default.cc @ 40] 
23 0000002e`1f7fecd0 00007ffc`cec3ba2d     base!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run+0x29f [E:\v8\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 470] 
24 0000002e`1f7fed90 00007ffc`7a9f4e3d     base!base::RunLoop::Run+0x2ed [E:\v8\chromium\src\base\run_loop.cc @ 134] 
25 0000002e`1f7feeb0 00007ffc`7ae912e5     content!content::RendererMain+0x6fd [E:\v8\chromium\src\content\renderer\renderer_main.cc @ 262] 
26 0000002e`1f7ff260 00007ffc`7ae92450     content!content::RunOtherNamedProcessTypeMain+0xf5 [E:\v8\chromium\src\content\app\content_main_runner_impl.cc @ 621] 
27 0000002e`1f7ff2c0 00007ffc`7ae8fb9a     content!content::ContentMainRunnerImpl::Run+0x300 [E:\v8\chromium\src\content\app\content_main_runner_impl.cc @ 955] 
28 0000002e`1f7ff3a0 00007ffc`7ae901b5     content!content::RunContentProcess+0x3ea [E:\v8\chromium\src\content\app\content_main.cc @ 386] 
29 0000002e`1f7ff600 00007ffc`7caf1351     content!content::ContentMain+0x45 [E:\v8\chromium\src\content\app\content_main.cc @ 412] 
2a 0000002e`1f7ff650 00007ff7`2fe66584     chrome_7ffc7caf0000!ChromeMain+0x211 [E:\v8\chromium\src\chrome\app\chrome_main.cc @ 151] 
2b 0000002e`1f7ff780 00007ff7`2fe61814     chrome!MainDllLoader::Launch+0x284 [E:\v8\chromium\src\chrome\app\main_dll_loader_win.cc @ 169] 
2c 0000002e`1f7ff870 00007ff7`3005a472     chrome!wWinMain+0x7a4 [E:\v8\chromium\src\chrome\app\chrome_exe_main_win.cc @ 382] 
```

### m....@gmail.com (2021-07-20)

[Comment Deleted]

### me...@chromium.org (2021-07-30)

rockot, could you PTAL and see if you can repro this issue?

[Monorail components: Internals>Mojo>Bindings]

### me...@chromium.org (2021-07-30)

Seems like this is hard to repro, so assigning medium severity.

### m....@gmail.com (2021-07-30)

https://crbug.com/chromium/1228661#c9
This issue reproduced very stably in the debug version.

### ro...@google.com (2021-07-30)

This looks like a typical Blink + Mojo bug where some Receiver or Remote is owned by a GCed object that does not finalize or dispose of itself properly. Like many async operations these objects internally rely on WeakPtrFactory properly finalizing to avoid tasks UAFing.

The blink::HeapMojoRemote/Receiver types were introduced to avoid this problem, but they still aren't used everywhere in Blink. It's not clear from the stacks where the offending binding lives but if we're lucky and it's not stomped yet the Connector's interface_name() could give a clue in a repro.

### m....@gmail.com (2021-08-04)

I think I found the root cause of the vulnerability
#RCA
1. The MessagePort::Entangle calls[1] connector_->set_incoming_receiver and pass this as a parameter
2. set_incoming_receiver save this as a raw pointer[3]
3. set_connection_error_handler use WrapWeakPersistent(this)[2] as parameter
4. So when MessagePort is GCed, connector_[3] will retain the dangling pointer of MessagePort cause UAF!

```
third_party/blink/renderer/core/messaging/message_port.cc:166
void MessagePort::Entangle(MessagePortDescriptor port) {
  DCHECK(port.IsValid());
  DCHECK(!connector_);

  port_ = std::move(port);
  connector_ = std::make_unique<mojo::Connector>(
      port_.TakeHandleToEntangle(GetExecutionContext()),
      mojo::Connector::SINGLE_THREADED_SEND);
  connector_->set_incoming_receiver(this);		<<[1]
  connector_->set_connection_error_handler(
      WTF::Bind(&MessagePort::close, WrapWeakPersistent(this)));  <<[2]
}

mojo/public/cpp/bindings/connector.h:294
class COMPONENT_EXPORT(MOJO_CPP_BINDINGS) Connector : public MessageReceiver {

...CUT...

  base::OnceClosure connection_error_handler_;

  ScopedMessagePipeHandle message_pipe_;
  MessageReceiver* incoming_receiver_ = nullptr;	<<[3]
```

### m....@gmail.com (2021-08-04)

And this is my patch, the vulnerability will no longer be reproduced in the local test

#Patch
```
diff --git a/third_party/blink/renderer/core/messaging/message_port.cc b/third_party/blink/renderer/core/messaging/message_port.cc
index cc07bc2680c..e67bd810f12 100644
--- a/third_party/blink/renderer/core/messaging/message_port.cc
+++ b/third_party/blink/renderer/core/messaging/message_port.cc
@@ -171,7 +171,7 @@ void MessagePort::Entangle(MessagePortDescriptor port) {
       mojo::Connector::SINGLE_THREADED_SEND);
   connector_->set_incoming_receiver(this);
   connector_->set_connection_error_handler(
-      WTF::Bind(&MessagePort::close, WrapWeakPersistent(this)));
+      WTF::Bind(&MessagePort::close, WrapPersistent(this)));
 }

 void MessagePort::Entangle(MessagePortChannel channel) {
```

### m....@gmail.com (2021-09-14)

I think the security level of this issue is raised to high and priority 1,because it can be reproduced stably。

### m....@gmail.com (2021-10-25)

https://crbug.com/chromium/1228661#c11 @rockot This issue has been open for more than 3 months,can you find someone to look at this issue.

### ro...@google.com (2021-10-26)

Sorry, lost track of this. Looks like an issue specific to MessagePort based on the latest comments? Over to Blink messaging owners

### m....@gmail.com (2021-12-01)

mek@ Can you take a look at this issue.

### m....@gmail.com (2022-01-20)

ping @mek~

### am...@chromium.org (2022-03-14)

setting RV-SE at reporting researcher's request 

### hc...@google.com (2022-03-30)

[Empty comment from Monorail migration]

### me...@chromium.org (2022-03-30)

Unfortunately the proposed fix would result in a memory leak (as there would be no way for MessagePort instances to be garbage collected if an instance owns a Persistent to itself).

I think adding a pre-finalizer is probably the (unfortunate) correct fix in this case.

### ye...@google.com (2022-03-30)

Modifying severity to high and priority to pri_1 since there is a stable PoC and this is a UAF in a renderer.

### me...@chromium.org (2022-03-30)

https://chromium-review.googlesource.com/c/chromium/src/+/3561845 should fix this.

### me...@chromium.org (2022-03-30)

[Empty comment from Monorail migration]

[Monorail components: Blink>Messaging]

### me...@chromium.org (2022-04-01)

jbroman raised a good point that it's not clear at all how MessagePort could get garbage collected while connector_ is still dispatching messages. For MessagePort to get garbage collected, HasPendingActivity() has to return false (the only other case it can get GC'ed is after the ExecutionContext goes away, but in that case the pipe will be closed already).

For HasPendingActivity() to return false, either started_ has to be false, or IsEntangled() has to be false.

If started_ is false, connector_->StartReceiving was never called, and thus the connector should not be dispatching any messages.

For IsEntangled() to return false, either closed_ has to be true, or IsNeutered() has to return true.

If closed_ is true, either the port was already neutered, or connector_ was (re)created with a dangling message pipe. Other than a connection error (resulting in a no-op close()), the connector shouldn't dispatch anything, as nothing is ever send over that pipe.

So that leaves IsNeutered() returning true. For that to be the case, either connector_ has to be null (in which case there are no messages to dispatch), or connector_->is_valid() has to return false (in which case connector_ wouldn't have a message pipe, so shouldn't be dispatching any messages either).

So with all that, I'm not sure how Connector::DispatchMessage could possibly be getting called after MessagePort is garbage collected.



However it does repro for me on Windows (not on linux for some reason), and one time I did get the DCHECK in ~MessagePort() DCHECK(!started_ || !IsEntangled()); to trigger instead as well, so clearly something is going wrong somewhere in that logic...

### me...@chromium.org (2022-04-01)

the DCHECK being the inverse of the HasPendingActivity logic. So somehow the MessagePort is getting garbage collected while HasPendingActivity is still returning true, and the ExecutionContext hasn't been destroyed yet (because if the ExecutionContext was destroyed, close() would have been called, closed_ would be set to true, and IsEntangled() would be returning false).

### me...@chromium.org (2022-04-01)

Not sure why I thought I couldn't repro on linux. After rebuilding with DCHECKs enabled, I'm also hitting the UAP on linux.

### me...@chromium.org (2022-04-01)

One theory I have is that maybe this is because (until recently) main-thread worklets would not call ContextDestroyed. I'm not sure if the repro here actually uses message ports in paint or layout worklets, but if that is the case that would explain the behavior. That was however fixed in M101/backported to M100 which doesn't match with it still reproing in newer versions in https://crbug.com/chromium/1311545.

### me...@chromium.org (2022-04-01)

Ah, I think I figured out what is going on. After adding a bunch of debug logging, I think what's happening is that the MessagePorts here are created in an already destroyed/detached ExecutionContext. As such ContextDestroyed is never called, and HasPendingActivity is ignored because the context was already destroyed...

As such, while my fix works, it is probably still not the correct fix.

### gi...@appspot.gserviceaccount.com (2022-04-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/068f13cc5aa5f7a6e9faf28d8731275e64cb657b

commit 068f13cc5aa5f7a6e9faf28d8731275e64cb657b
Author: Marijn Kruisselbrink <mek@chromium.org>
Date: Tue Apr 05 07:00:37 2022

Close a MessagePort if it is created in a destroyed context.

MessagePort assumes it is only destroyed either after ContextDestroyed,
or after the port has been closed explicitly. As it turns out ports that
were created in an already detached iframe would violate this invariant,
causing issues.

Bug: 1228661
Change-Id: Ib1abce15f1d1d15f044de19fe0534767db488af0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3561845
Reviewed-by: Jeremy Roman <jbroman@chromium.org>
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Cr-Commit-Position: refs/heads/main@{#988859}

[modify] https://crrev.com/068f13cc5aa5f7a6e9faf28d8731275e64cb657b/third_party/blink/renderer/core/messaging/message_port.h
[add] https://crrev.com/068f13cc5aa5f7a6e9faf28d8731275e64cb657b/third_party/blink/web_tests/external/wpt/webmessaging/message-channels/detached-iframe.window.js
[modify] https://crrev.com/068f13cc5aa5f7a6e9faf28d8731275e64cb657b/third_party/blink/renderer/core/messaging/message_port.cc


### gi...@appspot.gserviceaccount.com (2022-04-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f9bba74f9a4c8e50af2f6ba4e447fd6bb43edc7d

commit f9bba74f9a4c8e50af2f6ba4e447fd6bb43edc7d
Author: Hiroki Nakagawa <nhiroki@chromium.org>
Date: Tue Apr 05 08:39:15 2022

Revert "Close a MessagePort if it is created in a destroyed context."

This reverts commit 068f13cc5aa5f7a6e9faf28d8731275e64cb657b.

Reason for revert:
external/wpt/webmessaging/message-channels/detached-iframe.window.html
is constantly timing out on the linux-bfcache-rel bot:
https://ci.chromium.org/ui/p/chromium/builders/ci/linux-bfcache-rel/30737/overview

Original change's description:
> Close a MessagePort if it is created in a destroyed context.
>
> MessagePort assumes it is only destroyed either after ContextDestroyed,
> or after the port has been closed explicitly. As it turns out ports that
> were created in an already detached iframe would violate this invariant,
> causing issues.
>
> Bug: 1228661
> Change-Id: Ib1abce15f1d1d15f044de19fe0534767db488af0
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3561845
> Reviewed-by: Jeremy Roman <jbroman@chromium.org>
> Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#988859}

Bug: 1228661
Change-Id: I520cd4288c1cfac865866d1018d55a68266ef08e
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3571105
Auto-Submit: Hiroki Nakagawa <nhiroki@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#988879}

[modify] https://crrev.com/f9bba74f9a4c8e50af2f6ba4e447fd6bb43edc7d/third_party/blink/renderer/core/messaging/message_port.h
[delete] https://crrev.com/7872197d682374ac82490c57700f9a25596c8d65/third_party/blink/web_tests/external/wpt/webmessaging/message-channels/detached-iframe.window.js
[modify] https://crrev.com/f9bba74f9a4c8e50af2f6ba4e447fd6bb43edc7d/third_party/blink/renderer/core/messaging/message_port.cc


### me...@chromium.org (2022-04-06)

Unfortunately I'll be OOO for the next two weeks so I won't have time to figure out what's going on with the test and/or reland without the test.

jbroman: Do you think you could try to figure this out?

### bo...@google.com (2022-04-20)

This is your friendly Security Marshall checking in since it's been a couple weeks without activity. 

@jbroman and/or @mek, could you please allocate some time to look into what caused the revert? It looks like this bug has been unresolved for ~9 months so it would be really great to get this finally resolved. 

Adding Linux as an affected platform per https://crbug.com/chromium/1228661#c27, which makes me suspect Android is also plausibly affected. Removing SecurityImpact-None since it is reproducible without --single-process per https://crbug.com/chromium/1228661#c4.

### [Deleted User] (2022-04-20)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-20)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2022-04-26)

Sorry for the delay. Back from vacation, it seems the revert was just because the 2*3 second timeout in the test is too much for the default 6 second timeout our release bots use, but otherwise the fix and test should be correct. Relanding with reduced timeouts in https://chromium-review.googlesource.com/c/chromium/src/+/3609249.

And yes, this would effect all operation systems where blink runs, so including android.

### gi...@appspot.gserviceaccount.com (2022-04-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2782c7bc5bbe0829ad39907866f59bad65777df5

commit 2782c7bc5bbe0829ad39907866f59bad65777df5
Author: Marijn Kruisselbrink <mek@chromium.org>
Date: Wed Apr 27 20:51:50 2022

Reland "Close a MessagePort if it is created in a destroyed context."

This is a reland of commit 068f13cc5aa5f7a6e9faf28d8731275e64cb657b

This reland changes the timeout in the test from 3 to 2 seconds, because
two 3 second timeouts is too long for chrome's default overall test
timeout of 6 seconds on non-dcheck release builds.

Original change's description:
> Close a MessagePort if it is created in a destroyed context.
>
> MessagePort assumes it is only destroyed either after ContextDestroyed,
> or after the port has been closed explicitly. As it turns out ports that
> were created in an already detached iframe would violate this invariant,
> causing issues.
>
> Bug: 1228661
> Change-Id: Ib1abce15f1d1d15f044de19fe0534767db488af0
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3561845
> Reviewed-by: Jeremy Roman <jbroman@chromium.org>
> Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#988859}

Bug: 1228661
Change-Id: Ifc5ec866678667b0d81438e2a2c8e5ada6e19d8c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3609249
Commit-Queue: Jeremy Roman <jbroman@chromium.org>
Reviewed-by: Jeremy Roman <jbroman@chromium.org>
Auto-Submit: Marijn Kruisselbrink <mek@chromium.org>
Cr-Commit-Position: refs/heads/main@{#996880}

[modify] https://crrev.com/2782c7bc5bbe0829ad39907866f59bad65777df5/third_party/blink/renderer/core/messaging/message_port.h
[add] https://crrev.com/2782c7bc5bbe0829ad39907866f59bad65777df5/third_party/blink/web_tests/external/wpt/webmessaging/message-channels/detached-iframe.window.js
[modify] https://crrev.com/2782c7bc5bbe0829ad39907866f59bad65777df5/third_party/blink/renderer/core/messaging/message_port.cc


### me...@chromium.org (2022-04-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-29)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-05-06)

Congratulations! The VRP Panel has decided to award you $7,500 for this report. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2022-05-07)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-05-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-05-24)

removing RV-SE label based on off-bug conversation 

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### gm...@google.com (2022-05-25)

[Empty comment from Monorail migration]

### hu...@navercorp.com (2022-05-26)

Hi, is this patch merged into 102.0.5005.61 as announced at http://chromereleases.googleblog.com/search/label/Desktop%20Update ?
According to the commit logs, the last re-land CL seems not included.
https://chromium.googlesource.com/chromium/src/+log/101.0.4951.67..102.0.5005.63?pretty=fuller&n=10000

### rz...@google.com (2022-05-27)

[Empty comment from Monorail migration]

### rz...@google.com (2022-05-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-27)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-05-30)

1. Just https://crrev.com/c/3670161
2. Low, no conflicts
3. Merged to main in Apr. 05
4. Yes

### gm...@google.com (2022-05-31)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-06-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/303ddbf651751350972426689f95c76752f2e0e2

commit 303ddbf651751350972426689f95c76752f2e0e2
Author: Marijn Kruisselbrink <mek@chromium.org>
Date: Wed Jun 01 11:28:48 2022

[M96-LTS] Close a MessagePort if it is created in a destroyed context.

MessagePort assumes it is only destroyed either after ContextDestroyed,
or after the port has been closed explicitly. As it turns out ports that
were created in an already detached iframe would violate this invariant,
causing issues.

(cherry picked from commit 068f13cc5aa5f7a6e9faf28d8731275e64cb657b)

Bug: 1228661
Change-Id: Ib1abce15f1d1d15f044de19fe0534767db488af0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3561845
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#988859}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3670161
Owners-Override: Simon Hangl <simonha@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Simon Hangl <simonha@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1642}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/303ddbf651751350972426689f95c76752f2e0e2/third_party/blink/renderer/core/messaging/message_port.h
[add] https://crrev.com/303ddbf651751350972426689f95c76752f2e0e2/third_party/blink/web_tests/external/wpt/webmessaging/message-channels/detached-iframe.window.js
[modify] https://crrev.com/303ddbf651751350972426689f95c76752f2e0e2/third_party/blink/renderer/core/messaging/message_port.cc


### rz...@google.com (2022-06-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-08-05)

This issue was migrated from crbug.com/chromium/1228661?no_tracker_redirect=1

[Multiple monorail components: Blink>Messaging, Internals>Mojo>Bindings]
[Monorail mergedwith: crbug.com/chromium/1311545]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056521)*
