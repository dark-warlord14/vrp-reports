# Security: heap-use-after-free in ~PermissionRequestChip

| Field | Value |
|-------|-------|
| **Issue ID** | [40056766](https://issues.chromium.org/issues/40056766) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Permissions>Prompts |
| **Platforms** | Linux |
| **Reporter** | me...@gmail.com |
| **Assignee** | el...@chromium.org |
| **Created** | 2021-08-03 |
| **Bounty** | $10,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36

Steps to reproduce the problem:
1. download asan-linux-release-907432.zip, unzip chrome
2. copy the mojom: `python copy_mojo_js_bindings.py /path/to/asan-linux-release-907432/gen/` AND start a server at floder of poc.html : `python -m SimpleHTTPServer 8605`
3. ./asan-linux-release-907432/chrome http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html
4. Once you see the microphone request, close the browser immediately.

What is the expected behavior?

What went wrong?
If you cannot repro it, try more times. See the video for more info.
ASAN log:

=================================================================
==2724933==ERROR: AddressSanitizer: heap-use-after-free on address 0x61b00010fb80 at pc 0x562065ede6b3 bp 0x7ffe7a4913c0 sp 0x7ffe7a4913b8
READ of size 8 at 0x61b00010fb80 thread T0 (chrome)
    #0 0x562065ede6b2 in ~PermissionRequestChip chrome/browser/ui/views/location_bar/permission_request_chip.cc:130:45
    #1 0x562065ede6b2 in PermissionRequestChip::~PermissionRequestChip() chrome/browser/ui/views/location_bar/permission_request_chip.cc:128:49
    #2 0x562064a11a2d in views::View::~View() ui/views/view.cc:240:9
    #3 0x562065e32ae4 in ~LocationBarView chrome/browser/ui/views/location_bar/location_bar_view.cc:189:35
    #4 0x562065e32ae4 in non-virtual thunk to LocationBarView::~LocationBarView() chrome/browser/ui/views/location_bar/location_bar_view.cc
    #5 0x562064a11a2d in views::View::~View() ui/views/view.cc:240:9
    #6 0x5620664194dd in ToolbarView::~ToolbarView() chrome/browser/ui/views/toolbar/toolbar_view.cc:185:29
    #7 0x562064a11a2d in views::View::~View() ui/views/view.cc:240:9
    #8 0x562065df401d in ~TopContainerView chrome/browser/ui/views/frame/top_container_view.cc:19:1
    #9 0x562065df401d in TopContainerView::~TopContainerView() chrome/browser/ui/views/frame/top_container_view.cc:18:39
    #10 0x562064a154e8 in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #11 0x562064a154e8 in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #12 0x562064a154e8 in ~unique_ptr buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:269:19
    #13 0x562064a154e8 in views::View::DoRemoveChildView(views::View*, bool, bool, views::View*) ui/views/view.cc:2613:1
    #14 0x562064a158a8 in views::View::RemoveAllChildViews(bool) ui/views/view.cc:315:5
    #15 0x562065c2edd0 in BrowserView::~BrowserView() chrome/browser/ui/views/frame/browser_view.cc:745:3
    #16 0x562065c2fce7 in ~BrowserView chrome/browser/ui/views/frame/browser_view.cc:711:29
    #17 0x562065c2fce7 in non-virtual thunk to BrowserView::~BrowserView() chrome/browser/ui/views/frame/browser_view.cc
    #18 0x562064a11a2d in views::View::~View() ui/views/view.cc:240:9
    #19 0x562066606e92 in ~BrowserFrameViewLinuxNative chrome/browser/ui/views/frame/browser_frame_view_linux_native.cc:25:59
    #20 0x562066606e92 in BrowserFrameViewLinuxNative::~BrowserFrameViewLinuxNative() chrome/browser/ui/views/frame/browser_frame_view_linux_native.cc:25:59
    #21 0x562064b15ba3 in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #22 0x562064b15ba3 in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #23 0x562064b15ba3 in ~unique_ptr buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:269:19
    #24 0x562064b15ba3 in ~NonClientView ui/views/window/non_client_view.cc:150:1
    #25 0x562064b15ba3 in views::NonClientView::~NonClientView() ui/views/window/non_client_view.cc:146:33
    #26 0x562064a154e8 in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #27 0x562064a154e8 in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #28 0x562064a154e8 in ~unique_ptr buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:269:19
    #29 0x562064a154e8 in views::View::DoRemoveChildView(views::View*, bool, bool, views::View*) ui/views/view.cc:2613:1
    #30 0x562064a158a8 in views::View::RemoveAllChildViews(bool) ui/views/view.cc:315:5
    #31 0x562064a90f67 in views::Widget::DestroyRootView() ui/views/widget/widget.cc:1763:15
    #32 0x562064a90777 in views::Widget::~Widget() ui/views/widget/widget.cc:208:3
    #33 0x562065c54ffd in BrowserFrame::~BrowserFrame() chrome/browser/ui/views/frame/browser_frame.cc:83:31
    #34 0x562064b7b87c in views::DesktopNativeWidgetAura::~DesktopNativeWidgetAura() ui/views/widget/desktop_aura/desktop_native_widget_aura.cc
    #35 0x562065dc7596 in ~DesktopBrowserFrameAuraLinux chrome/browser/ui/views/frame/desktop_browser_frame_aura_linux.cc:35:61
    #36 0x562065dc7596 in DesktopBrowserFrameAuraLinux::~DesktopBrowserFrameAuraLinux() chrome/browser/ui/views/frame/desktop_browser_frame_aura_linux.cc:35:61
    #37 0x562064b6a92b in views::DesktopWindowTreeHostLinux::OnClosed() ui/views/widget/desktop_aura/desktop_window_tree_host_linux.cc:274:34
    #38 0x562064bb60a3 in views::DesktopWindowTreeHostPlatform::CloseNow() ui/views/widget/desktop_aura/desktop_window_tree_host_platform.cc:328:22
    #39 0x562064bc0314 in Invoke<void (views::DesktopWindowTreeHostPlatform::*)(), base::WeakPtr<views::DesktopWindowTreeHostPlatform>> base/bind_internal.h:509:12
    #40 0x562064bc0314 in MakeItSo<void (views::DesktopWindowTreeHostPlatform::*)(), base::WeakPtr<views::DesktopWindowTreeHostPlatform>> base/bind_internal.h:668:5
    #41 0x562064bc0314 in RunImpl<void (views::DesktopWindowTreeHostPlatform::*)(), std::tuple<base::WeakPtr<views::DesktopWindowTreeHostPlatform> >, 0UL> base/bind_internal.h:721:12
    #42 0x562064bc0314 in base::internal::Invoker<base::internal::BindState<void (views::DesktopWindowTreeHostPlatform::*)(), base::WeakPtr<views::DesktopWindowTreeHostPlatform> >, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:690:12
    #43 0x56205b34c170 in Run base/callback.h:98:12
    #44 0x56205b34c170 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:178:33
    #45 0x56205b3853e9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:360:23
    #46 0x56205b384b5a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:260:36
    #47 0x56205b385d91 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #48 0x56205b24622a in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:405:48
    #49 0x56205b386454 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:467:12
    #50 0x56205b2c7b51 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14
    #51 0x562052431ee5 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:987:18
    #52 0x562052436a25 in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:152:15
    #53 0x56205242bddf in content::BrowserMain(content::MainFunctionParams const&) content/browser/browser_main.cc:49:28
    #54 0x56205a139eed in RunBrowserProcessMain content/app/content_main_runner_impl.cc:608:10
    #55 0x56205a139eed in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content/app/content_main_runner_impl.cc:1104:10
    #56 0x56205a138ff5 in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:971:12
    #57 0x56205a1325a7 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) content/app/content_main.cc:390:36
    #58 0x56205a1341c2 in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:418:10
    #59 0x56204d1a88e6 in ChromeMain chrome/app/chrome_main.cc:168:12
    #60 0x7f61fa0a70b2 in __libc_start_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16

0x61b00010fb80 is located 0 bytes inside of 1440-byte region [0x61b00010fb80,0x61b000110120)
freed by thread T0 (chrome) here:
    #0 0x56204d1a65fd in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:152:3
    #1 0x562064ab7a0e in views::WidgetDelegate::DeleteDelegate() ui/views/widget/widget_delegate.cc:238:5
    #2 0x562064a9ff2a in views::Widget::OnNativeWidgetDestroyed() ui/views/widget/widget.cc:1412:21
    #3 0x562064b44cde in OnWindowDestroyed ui/views/widget/native_widget_aura.cc:965:14
    #4 0x562064b44cde in non-virtual thunk to views::NativeWidgetAura::OnWindowDestroyed(aura::Window*) ui/views/widget/native_widget_aura.cc
    #5 0x5620606131bf in aura::Window::~Window() ui/aura/window.cc:226:16
    #6 0x562060614b0d in aura::Window::~Window() ui/aura/window.cc:181:19
    #7 0x562063486ba3 in wm::TransientWindowManager::OnWindowDestroying(aura::Window*) ui/wm/core/transient_window_manager.cc:255:5
    #8 0x562060612d21 in aura::Window::~Window() ui/aura/window.cc:192:14
    #9 0x562060614b0d in aura::Window::~Window() ui/aura/window.cc:181:19
    #10 0x5620606130fd in RemoveOrDestroyChildren ui/aura/window.cc:936:7
    #11 0x5620606130fd in aura::Window::~Window() ui/aura/window.cc:218:3
    #12 0x562060614b0d in aura::Window::~Window() ui/aura/window.cc:181:19
    #13 0x562060666bbe in aura::WindowTreeHost::DestroyDispatcher() ui/aura/window_tree_host.cc:411:3
    #14 0x562064bb3421 in views::DesktopWindowTreeHostPlatform::~DesktopWindowTreeHostPlatform() ui/views/widget/desktop_aura/desktop_window_tree_host_platform.cc:173:3
    #15 0x562065dcaa32 in ~BrowserDesktopWindowTreeHostLinux chrome/browser/ui/views/frame/browser_desktop_window_tree_host_linux.cc:74:71
    #16 0x562065dcaa32 in ~BrowserDesktopWindowTreeHostLinux chrome/browser/ui/views/frame/browser_desktop_window_tree_host_linux.cc:74:71
    #17 0x562065dcaa32 in non-virtual thunk to BrowserDesktopWindowTreeHostLinux::~BrowserDesktopWindowTreeHostLinux() chrome/browser/ui/views/frame/browser_desktop_window_tree_host_linux.cc
    #18 0x562064b7c7a4 in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #19 0x562064b7c7a4 in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #20 0x562064b7c7a4 in views::DesktopNativeWidgetAura::OnHostClosed() ui/views/widget/desktop_aura/desktop_native_widget_aura.cc:343:9
    #21 0x562064b6a92b in views::DesktopWindowTreeHostLinux::OnClosed() ui/views/widget/desktop_aura/desktop_window_tree_host_linux.cc:274:34
    #22 0x562064bb60a3 in views::DesktopWindowTreeHostPlatform::CloseNow() ui/views/widget/desktop_aura/desktop_window_tree_host_platform.cc:328:22
    #23 0x562064bc0314 in Invoke<void (views::DesktopWindowTreeHostPlatform::*)(), base::WeakPtr<views::DesktopWindowTreeHostPlatform>> base/bind_internal.h:509:12
    #24 0x562064bc0314 in MakeItSo<void (views::DesktopWindowTreeHostPlatform::*)(), base::WeakPtr<views::DesktopWindowTreeHostPlatform>> base/bind_internal.h:668:5
    #25 0x562064bc0314 in RunImpl<void (views::DesktopWindowTreeHostPlatform::*)(), std::tuple<base::WeakPtr<views::DesktopWindowTreeHostPlatform> >, 0UL> base/bind_internal.h:721:12
    #26 0x562064bc0314 in base::internal::Invoker<base::internal::BindState<void (views::DesktopWindowTreeHostPlatform::*)(), base::WeakPtr<views::DesktopWindowTreeHostPlatform> >, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:690:12
    #27 0x56205b34c170 in Run base/callback.h:98:12
    #28 0x56205b34c170 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:178:33
    #29 0x56205b3853e9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:360:23
    #30 0x56205b384b5a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:260:36
    #31 0x56205b385d91 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #32 0x56205b24622a in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:405:48
    #33 0x56205b386454 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:467:12
    #34 0x56205b2c7b51 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14
    #35 0x562052431ee5 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:987:18
    #36 0x562052436a25 in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:152:15
    #37 0x56205242bddf in content::BrowserMain(content::MainFunctionParams const&) content/browser/browser_main.cc:49:28
    #38 0x56205a139eed in RunBrowserProcessMain content/app/content_main_runner_impl.cc:608:10
    #39 0x56205a139eed in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content/app/content_main_runner_impl.cc:1104:10
    #40 0x56205a138ff5 in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:971:12

previously allocated by thread T0 (chrome) here:
    #0 0x56204d1a5d9d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95:3
    #1 0x562065ee0217 in PermissionRequestChip::OpenBubble() chrome/browser/ui/views/location_bar/permission_request_chip.cc:141:47
    #2 0x562065ecea9a in PermissionChip::ExpandAnimationEnded() chrome/browser/ui/views/location_bar/permission_chip.cc:150:5
    #3 0x56205d50ce06 in gfx::LinearAnimation::Step(base::TimeTicks) ui/gfx/animation/linear_animation.cc:88:5
    #4 0x56205d509ca6 in gfx::AnimationContainer::Run(base::TimeTicks) ui/gfx/animation/animation_container.cc:100:13
    #5 0x56205d50bab0 in Run base/callback.h:166:12
    #6 0x56205d50bab0 in gfx::AnimationRunner::Step(base::TimeTicks) ui/gfx/animation/animation_runner.cc:78:9
    #7 0x56206069af78 in ui::Compositor::BeginMainFrame(viz::BeginFrameArgs const&) ui/compositor/compositor.cc:645:14
    #8 0x56205fc7e1c7 in cc::SingleThreadProxy::DoBeginMainFrame(viz::BeginFrameArgs const&) cc/trees/single_thread_proxy.cc:905:21
    #9 0x56205fc7f7ff in cc::SingleThreadProxy::BeginMainFrame(viz::BeginFrameArgs const&) cc/trees/single_thread_proxy.cc:871:3
    #10 0x56205fc814c6 in Invoke<void (cc::SingleThreadProxy::*)(const viz::BeginFrameArgs &), base::WeakPtr<cc::SingleThreadProxy>, viz::BeginFrameArgs> base/bind_internal.h:509:12
    #11 0x56205fc814c6 in MakeItSo<void (cc::SingleThreadProxy::*)(const viz::BeginFrameArgs &), base::WeakPtr<cc::SingleThreadProxy>, viz::BeginFrameArgs> base/bind_internal.h:668:5
    #12 0x56205fc814c6 in RunImpl<void (cc::SingleThreadProxy::*)(const viz::BeginFrameArgs &), std::tuple<base::WeakPtr<cc::SingleThreadProxy>, viz::BeginFrameArgs>, 0UL, 1UL> base/bind_internal.h:721:12
    #13 0x56205fc814c6 in base::internal::Invoker<base::internal::BindState<void (cc::SingleThreadProxy::*)(viz::BeginFrameArgs const&), base::WeakPtr<cc::SingleThreadProxy>, viz::BeginFrameArgs>, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:690:12
    #14 0x56205b34c170 in Run base/callback.h:98:12
    #15 0x56205b34c170 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:178:33
    #16 0x56205b3853e9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:360:23
    #17 0x56205b384b5a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:260:36
    #18 0x56205b385d91 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #19 0x56205b24622a in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:405:48
    #20 0x56205b386454 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:467:12
    #21 0x56205b2c7b51 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14
    #22 0x562052431ee5 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:987:18
    #23 0x562052436a25 in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:152:15
    #24 0x56205242bddf in content::BrowserMain(content::MainFunctionParams const&) content/browser/browser_main.cc:49:28
    #25 0x56205a139eed in RunBrowserProcessMain content/app/content_main_runner_impl.cc:608:10
    #26 0x56205a139eed in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content/app/content_main_runner_impl.cc:1104:10
    #27 0x56205a138ff5 in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:971:12
    #28 0x56205a1325a7 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) content/app/content_main.cc:390:36
    #29 0x56205a1341c2 in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:418:10
    #30 0x56204d1a88e6 in ChromeMain chrome/app/chrome_main.cc:168:12
    #31 0x7f61fa0a70b2 in __libc_start_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-use-after-free chrome/browser/ui/views/location_bar/permission_request_chip.cc:130:45 in ~PermissionRequestChip
Shadow bytes around the buggy address:
  0x0c3680019f20: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c3680019f30: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c3680019f40: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c3680019f50: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c3680019f60: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x0c3680019f70:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3680019f80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3680019f90: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3680019fa0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3680019fb0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3680019fc0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==2724933==ABORTING

Did this work before? N/A 

Chrome version: 92.0.4515.107  Channel: n/a
OS Version:

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 2.0 KB)
- [copy_mojo_js_bindings.py](attachments/copy_mojo_js_bindings.py) (text/plain, 514 B)
- [video.webm](attachments/video.webm) (video/webm, 4.9 MB)

## Timeline

### [Deleted User] (2021-08-03)

[Empty comment from Monorail migration]

### me...@gmail.com (2021-08-03)

Update the setp3:
3. ./asan-linux-release-907432/chrome --enable-blink-features=MojoJS --incognito http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html

video is uploaded.

### me...@chromium.org (2021-08-03)

This looks similar to https://crbug.com/chromium/1235068. mabian, could you please take a look? Thanks.

[Monorail components: UI>Browser>Permissions>Prompts]

### ma...@microsoft.com (2021-08-03)

I agree it looks similar, but it appears that this bug repros in stable, correct? The CL that was blamed in #1235068 [1] is not in stable yet.

[1]: https://chromium.googlesource.com/chromium/src/+/2658aff74fd8aaa883f61883a90797d51099f1e4

### [Deleted User] (2021-08-03)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-03)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@microsoft.com (2021-08-06)

crbug.com/1235068 has been fixed, and I was never able to repro and did not land a fix for this. I'm going to remove myself from this.

### ad...@google.com (2021-08-07)

Sorry mabian@microsoft.com, security bugs can't be unowned. Can you suggest the best way forward to investigate what's happening here?

### ma...@microsoft.com (2021-08-07)

Not really, I wasn't able to see any connection between this and my CL. The similar ClusterFuzz bug pointed to the fix being here: https://clusterfuzz.com/revisions?job=linux_ubsan_vptr_chrome&range=909128:909133

Alternatively, I tried chatting with the PermissionChip owner and they pointed me to elklm@, who potentially hit a similar bug when working in the area before. Maybe they can offer some guidance?

### [Deleted User] (2021-08-08)

[Empty comment from Monorail migration]

### el...@google.com (2021-08-09)

@bsep, please check the video at https://crbug.com/chromium/1235949#c2. It seems like due to async permission request flow, the prompt is destroyed during chip destructor is executed. From the crash log it seems like the problem is in `GetWidget()` https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/location_bar/permission_request_chip.cc;l=130

In the past we had 2 step destruction in `LocationBarView::FinalizeChip()`:
1. Unsubscribe a chip from `prompt_bubble_->GetWidget();`
2. Remove it from the view tree.


### bs...@chromium.org (2021-08-10)

#11: I don't think I understand. What is async here? Is ~PermissionRequestChip() racing with OnWidgetClosing()?

If you have a fix in mind already, go ahead and try it. I think you understand this better than I do at this point :)

### el...@google.com (2021-08-12)

[Empty comment from Monorail migration]

### el...@google.com (2021-08-12)

I was able to reproduce the crash. Had to add --use-fake-device-for-media-stream flag to test it without a real mic. 

### el...@chromium.org (2021-08-12)

Chip experiment is disabled by default on stable. After enabling it for testing, was not able to reproduce the crash on 92.0.4515.131

@meacer: I set Security_Impact-Beta because we do not have chip on stable.

### [Deleted User] (2021-08-12)

[Empty comment from Monorail migration]

### el...@chromium.org (2021-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### el...@chromium.org (2021-08-16)

[Empty comment from Monorail migration]

### pb...@chromium.org (2021-08-16)

My read is that prompt_bubble_ is UAF here, prompt_bubble_ is set to nullptr in OnWidgetClosing but that doesn't happen if the OS destroys the widget I believe. Presumably OnWidgetDestroying or OnWidgetDestroyed would be a good place to catch this. (This API makes for some good foot shooting. Maybe we need to make sure that OnWidgetClosing is called even during OS Widget destruction.)

### pb...@chromium.org (2021-08-16)

Per offline chats it may also be easier to just use a ViewTracker for prompt_bubble_ as you wouldn't need to know how the View got destroyed just whether ~View got called or not.

### me...@chromium.org (2021-08-16)

Just to clarify the Security_Impact* label: My initial assessment was incorrect (thanks elklm@ for catching that!). Sheriffbot also incorrectly added Security_Stable but then corrected itself. The current impact label is correct but it's also not critical since FoundIn-MM is the source of truth nowadays.

### gi...@appspot.gserviceaccount.com (2021-08-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c490819db1ce602f12bda83f55e12ba332fb57ff

commit c490819db1ce602f12bda83f55e12ba332fb57ff
Author: Illia Klimov <elklm@google.com>
Date: Thu Aug 19 11:10:45 2021

Migrate PermissionChip to OnWidgetDestroying.

OnWidgetClosing is notified only after widget->Close()/CloseNow() is
called. In case of ~Window() is triggered, there is a chance that
PermissionPromptBubble will be deleted before chip cleanup logic is
executed, which may lead to  UAF.

To prevent UAF:
* PermissionChip implements OnWidgetDestroying to unsubscribe from
widget observer.
* ViewTracker is used to track a permission prompt bubble state.

Bug: 1235949
Change-Id: Ibeeb63e37ef2be088f80b760e0c2de286b45563b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3097833
Commit-Queue: Illia Klimov <elklm@chromium.org>
Reviewed-by: Bret Sepulveda <bsep@chromium.org>
Reviewed-by: Andy Paicu <andypaicu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#913353}

[modify] https://crrev.com/c490819db1ce602f12bda83f55e12ba332fb57ff/chrome/browser/ui/views/location_bar/permission_chip.cc
[modify] https://crrev.com/c490819db1ce602f12bda83f55e12ba332fb57ff/chrome/browser/ui/views/location_bar/permission_chip.h
[modify] https://crrev.com/c490819db1ce602f12bda83f55e12ba332fb57ff/chrome/browser/ui/views/location_bar/permission_quiet_chip.cc
[modify] https://crrev.com/c490819db1ce602f12bda83f55e12ba332fb57ff/chrome/browser/ui/views/location_bar/permission_quiet_chip.h
[modify] https://crrev.com/c490819db1ce602f12bda83f55e12ba332fb57ff/chrome/browser/ui/views/location_bar/permission_request_chip.cc
[modify] https://crrev.com/c490819db1ce602f12bda83f55e12ba332fb57ff/chrome/browser/ui/views/location_bar/permission_request_chip.h
[modify] https://crrev.com/c490819db1ce602f12bda83f55e12ba332fb57ff/chrome/browser/ui/views/permission_bubble/permission_prompt_impl.cc
[modify] https://crrev.com/c490819db1ce602f12bda83f55e12ba332fb57ff/chrome/browser/ui/views/permission_bubble/permission_prompt_impl.h
[modify] https://crrev.com/c490819db1ce602f12bda83f55e12ba332fb57ff/chrome/test/permissions/permission_request_manager_test_api.cc


### el...@google.com (2021-08-19)

I mark the bug as Fixed because it is not reproducible anymore.

### [Deleted User] (2021-08-19)

This bug requires manual review: We are only 11 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), govind@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-08-19)

Since this fix just landed a few hours ago, and it is not trivial, I'd prefer it to get a bit more bake time on Canary, so I'm going to suggest that we not yet merge. Especially since 93 is slated to be cut for Monday for a release next week. If this gets pushed back, then we can revisit on Monday to be included. Otherwise, this can be included in the first refresh of M93. Please let me know if there's any issues or concerns. Thanks!

### [Deleted User] (2021-08-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-20)

Your change meets the bar and is auto-approved for M94. Please go ahead and merge the CL to branch 4606 (refs/branch-heads/4606) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: govind@(Android), harrysouders@(iOS), matthewjoseph@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-08-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b0700526df65969f911e9cb8a8d3be70cb4badc4

commit b0700526df65969f911e9cb8a8d3be70cb4badc4
Author: Illia Klimov <elklm@google.com>
Date: Mon Aug 23 12:58:27 2021

Migrate PermissionChip to OnWidgetDestroying.

OnWidgetClosing is notified only after widget->Close()/CloseNow() is
called. In case of ~Window() is triggered, there is a chance that
PermissionPromptBubble will be deleted before chip cleanup logic is
executed, which may lead to  UAF.

To prevent UAF:
* PermissionChip implements OnWidgetDestroying to unsubscribe from
widget observer.
* ViewTracker is used to track a permission prompt bubble state.

(cherry picked from commit c490819db1ce602f12bda83f55e12ba332fb57ff)

Bug: 1235949
Change-Id: Ibeeb63e37ef2be088f80b760e0c2de286b45563b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3097833
Commit-Queue: Illia Klimov <elklm@chromium.org>
Reviewed-by: Bret Sepulveda <bsep@chromium.org>
Reviewed-by: Andy Paicu <andypaicu@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#913353}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3110444
Reviewed-by: Ravjit Singh Uppal <ravjit@chromium.org>
Reviewed-by: Balazs Engedy <engedy@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4606@{#214}
Cr-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}

[modify] https://crrev.com/b0700526df65969f911e9cb8a8d3be70cb4badc4/chrome/browser/ui/views/location_bar/permission_chip.cc
[modify] https://crrev.com/b0700526df65969f911e9cb8a8d3be70cb4badc4/chrome/browser/ui/views/location_bar/permission_chip.h
[modify] https://crrev.com/b0700526df65969f911e9cb8a8d3be70cb4badc4/chrome/browser/ui/views/location_bar/permission_quiet_chip.cc
[modify] https://crrev.com/b0700526df65969f911e9cb8a8d3be70cb4badc4/chrome/browser/ui/views/location_bar/permission_quiet_chip.h
[modify] https://crrev.com/b0700526df65969f911e9cb8a8d3be70cb4badc4/chrome/browser/ui/views/location_bar/permission_request_chip.cc
[modify] https://crrev.com/b0700526df65969f911e9cb8a8d3be70cb4badc4/chrome/browser/ui/views/location_bar/permission_request_chip.h
[modify] https://crrev.com/b0700526df65969f911e9cb8a8d3be70cb4badc4/chrome/browser/ui/views/permission_bubble/permission_prompt_impl.cc
[modify] https://crrev.com/b0700526df65969f911e9cb8a8d3be70cb4badc4/chrome/browser/ui/views/permission_bubble/permission_prompt_impl.h
[modify] https://crrev.com/b0700526df65969f911e9cb8a8d3be70cb4badc4/chrome/test/permissions/permission_request_manager_test_api.cc


### el...@chromium.org (2021-08-24)

1. Does your merge fit within the Merge Decision Guidelines?
Yes.
2. Links to the CLs you are requesting to merge.
https://chromium-review.googlesource.com/c/chromium/src/+/3097833
3. Has the change landed and been verified on ToT?
Yes.
4. Does this change need to be merged into other active release branches (M-1, M+1)?
Yes, Merged into M94.
5. Why are these changes required in this milestone after branch?
Security bug.
6. Is this a new feature?
No.
7. If it is a new feature, is it behind a flag using finch?
It is not a new feature, but the code is behind a flag and it is enabled to Beta only.

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents
No.

### am...@chromium.org (2021-08-25)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-08-25)

merge approved to M93, please merge to branch 4577 at your convenience; also please merge to M92, branch 4515, as M92 will become the Extended Stable channel release version as M93 gets promoted to Stable and we transition to the 4W stable channel release cycle 

### am...@google.com (2021-08-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-08-25)

Congratulations, the VRP Panel has decided to award you $10,000 for this report. Thank you for reporting this issue and nice work! 

### me...@gmail.com (2021-08-26)

Thank you!

### am...@google.com (2021-08-27)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-08-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/455b63779c76f8f171bf0d9b2909f7f962292a4e

commit 455b63779c76f8f171bf0d9b2909f7f962292a4e
Author: Illia Klimov <elklm@google.com>
Date: Fri Aug 27 15:55:17 2021

Migrate PermissionChip to OnWidgetDestroying.

OnWidgetClosing is notified only after widget->Close()/CloseNow() is
called. In case of ~Window() is triggered, there is a chance that
PermissionPromptBubble will be deleted before chip cleanup logic is
executed, which may lead to  UAF.

To prevent UAF:
* PermissionChip implements OnWidgetDestroying to unsubscribe from
widget observer.
* ViewTracker is used to track a permission prompt bubble state.

(cherry picked from commit c490819db1ce602f12bda83f55e12ba332fb57ff)

Bug: 1235949
Change-Id: Ibeeb63e37ef2be088f80b760e0c2de286b45563b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3097833
Commit-Queue: Illia Klimov <elklm@chromium.org>
Reviewed-by: Bret Sepulveda <bsep@chromium.org>
Reviewed-by: Andy Paicu <andypaicu@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#913353}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3121265
Reviewed-by: Balazs Engedy <engedy@chromium.org>
Reviewed-by: Illia Klimov <elklm@chromium.org>
Auto-Submit: Illia Klimov <elklm@chromium.org>
Owners-Override: Prudhvi Kumar Bommana <pbommana@google.com>
Cr-Commit-Position: refs/branch-heads/4577@{#1132}
Cr-Branched-From: 761ddde228655e313424edec06497d0c56b0f3c4-refs/heads/master@{#902210}

[modify] https://crrev.com/455b63779c76f8f171bf0d9b2909f7f962292a4e/chrome/browser/ui/views/location_bar/permission_chip.cc
[modify] https://crrev.com/455b63779c76f8f171bf0d9b2909f7f962292a4e/chrome/browser/ui/views/location_bar/permission_chip.h
[modify] https://crrev.com/455b63779c76f8f171bf0d9b2909f7f962292a4e/chrome/browser/ui/views/location_bar/permission_quiet_chip.cc
[modify] https://crrev.com/455b63779c76f8f171bf0d9b2909f7f962292a4e/chrome/browser/ui/views/location_bar/permission_quiet_chip.h
[modify] https://crrev.com/455b63779c76f8f171bf0d9b2909f7f962292a4e/chrome/browser/ui/views/location_bar/permission_request_chip.cc
[modify] https://crrev.com/455b63779c76f8f171bf0d9b2909f7f962292a4e/chrome/browser/ui/views/location_bar/permission_request_chip.h
[modify] https://crrev.com/455b63779c76f8f171bf0d9b2909f7f962292a4e/chrome/browser/ui/views/permission_bubble/permission_prompt_impl.cc
[modify] https://crrev.com/455b63779c76f8f171bf0d9b2909f7f962292a4e/chrome/browser/ui/views/permission_bubble/permission_prompt_impl.h
[modify] https://crrev.com/455b63779c76f8f171bf0d9b2909f7f962292a4e/chrome/test/permissions/permission_request_manager_test_api.cc


### gi...@appspot.gserviceaccount.com (2021-08-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0f8fb0ed80ec63dfe5969e0dd45499fba7aa8494

commit 0f8fb0ed80ec63dfe5969e0dd45499fba7aa8494
Author: Illia Klimov <elklm@google.com>
Date: Fri Aug 27 16:02:01 2021

Migrate PermissionChip to OnWidgetDestroying.

OnWidgetClosing is notified only after widget->Close()/CloseNow() is
called. In case of ~Window() is triggered, there is a chance that
PermissionPromptBubble will be deleted before chip cleanup logic is
executed, which may lead to  UAF.

To prevent UAF:
* PermissionChip implements OnWidgetDestroying to unsubscribe from
widget observer.
* ViewTracker is used to track a permission prompt bubble state.

(cherry picked from commit c490819db1ce602f12bda83f55e12ba332fb57ff)

Bug: 1235949
Change-Id: Ibeeb63e37ef2be088f80b760e0c2de286b45563b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3097833
Commit-Queue: Illia Klimov <elklm@chromium.org>
Reviewed-by: Bret Sepulveda <bsep@chromium.org>
Reviewed-by: Andy Paicu <andypaicu@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#913353}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3121448
Reviewed-by: Balazs Engedy <engedy@chromium.org>
Reviewed-by: Illia Klimov <elklm@chromium.org>
Auto-Submit: Illia Klimov <elklm@chromium.org>
Owners-Override: Prudhvi Kumar Bommana <pbommana@google.com>
Cr-Commit-Position: refs/branch-heads/4515@{#2091}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[modify] https://crrev.com/0f8fb0ed80ec63dfe5969e0dd45499fba7aa8494/chrome/browser/ui/views/location_bar/permission_chip.cc
[modify] https://crrev.com/0f8fb0ed80ec63dfe5969e0dd45499fba7aa8494/chrome/browser/ui/views/location_bar/permission_chip.h
[modify] https://crrev.com/0f8fb0ed80ec63dfe5969e0dd45499fba7aa8494/chrome/browser/ui/views/location_bar/permission_request_chip.cc
[modify] https://crrev.com/0f8fb0ed80ec63dfe5969e0dd45499fba7aa8494/chrome/browser/ui/views/location_bar/permission_request_chip.h
[modify] https://crrev.com/0f8fb0ed80ec63dfe5969e0dd45499fba7aa8494/chrome/browser/ui/views/permission_bubble/permission_prompt_impl.cc
[modify] https://crrev.com/0f8fb0ed80ec63dfe5969e0dd45499fba7aa8494/chrome/browser/ui/views/permission_bubble/permission_prompt_impl.h
[modify] https://crrev.com/0f8fb0ed80ec63dfe5969e0dd45499fba7aa8494/chrome/test/permissions/permission_request_manager_test_api.cc


### am...@chromium.org (2021-08-30)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-31)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-03)

[Empty comment from Monorail migration]

### as...@google.com (2021-09-08)

[Empty comment from Monorail migration]

### as...@google.com (2021-09-08)

Marking as NA for M90 LTS as chrome/browser/ui/views/location_bar/permission_request_chip.* with PermissionRequestChip are not in M90 branch.

### [Deleted User] (2021-11-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1235949?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056766)*
