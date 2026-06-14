# uaf in TabSharingInfoBarDelegate

| Field | Value |
|-------|-------|
| **Issue ID** | [40052122](https://issues.chromium.org/issues/40052122) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cd...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2020-04-26 |
| **Bounty** | $15,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36

Steps to reproduce the problem:
version:Chromium 84.0.4127.0 
1 python ./copy_mojo_js_bindings.py /path/to/chrome/.../out/asan/gen
2 python3.6m -m http.server 8605
3 ./chrome --enable-blink-features=MojoJS --user-data-dir=/tmp/nonexist  http://127.0.0.1:8605/poc.html
This crash requires user interaction. Select "Chrome tab" in the pop-up dialog box, and then click "share". Two "stop" buttons will appear on the left side. Click "stop" button twice again browser process  will crash.
Because this repro needs user interaction, I also uploaded the repro video file.

What is the expected behavior?

What went wrong?
==18964==ERROR: AddressSanitizer: heap-use-after-free on address 0x611000423000 at pc 0x55e5b8517edb bp 0x7ffe1a617680 sp 0x7ffe1a617678
READ of size 8 at 0x611000423000 thread T0 (chrome)
    #0 0x55e5b8517eda in TabSharingInfoBarDelegate::Accept() chrome/browser/ui/tab_sharing/tab_sharing_infobar_delegate.cc:84:8
    #1 0x55e5b823519f in ButtonPressed chrome/browser/ui/views/infobars/confirm_infobar.cc
    #2 0x55e5b823519f in non-virtual thunk to ConfirmInfoBar::ButtonPressed(views::Button*, ui::Event const&) chrome/browser/ui/views/infobars/confirm_infobar.cc
    #3 0x55e5b5a0f066 in views::ButtonController::OnMouseReleased(ui::MouseEvent const&) ui/views/controls/button/button_controller.cc
    #4 0x55e5b59c458b in ui::ScopedTargetHandler::OnEvent(ui::Event*) ui/events/scoped_target_handler.cc:32:24
    #5 0x55e5b0b9e4f9 in DispatchEvent ui/events/event_dispatcher.cc:193:12
    #6 0x55e5b0b9e4f9 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:142:5
    #7 0x55e5b0b9dd8d in DispatchEventToTarget ui/events/event_dispatcher.cc:86:14
    #8 0x55e5b0b9dd8d in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:58:15
    #9 0x55e5b5b6a6ba in views::internal::RootView::OnMouseReleased(ui::MouseEvent const&) ui/views/widget/root_view.cc:467:9
    #10 0x55e5b5b8a612 in views::Widget::OnMouseEvent(ui::MouseEvent*) ui/views/widget/widget.cc:1275:20
    #11 0x55e5b0b9e4f9 in DispatchEvent ui/events/event_dispatcher.cc:193:12
    #12 0x55e5b0b9e4f9 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:142:5
    #13 0x55e5b0b9dd8d in DispatchEventToTarget ui/events/event_dispatcher.cc:86:14
    #14 0x55e5b0b9dd8d in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:58:15
    #15 0x55e5b37186cd in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:49:17
    #16 0x55e5b3735eab in ui::EventSource::DeliverEventToSink(ui::Event*) ui/events/event_source.cc:113:16
    #17 0x55e5b3735ab6 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const*, ui::EventRewriter const*) ui/events/event_source.cc:138:12
    #18 0x55e5b5c11a90 in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event*) ui/aura/window_tree_host_platform.cc:229:38
    #19 0x55e5b5c0c34c in views::DesktopWindowTreeHostLinux::DispatchEvent(ui::Event*) ui/views/widget/desktop_aura/desktop_window_tree_host_linux.cc:281:29
    #20 0x55e5b5c18ed8 in ui::X11Window::DispatchUiEvent(ui::Event*, _XEvent*) ui/platform_window/x11/x11_window.cc:616:32
    #21 0x55e5b5c185e9 in ui::X11Window::DispatchEvent(ui::Event* const&) ui/platform_window/x11/x11_window.cc:566:3
    #22 0x55e5b5c190da in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event* const&) ui/platform_window/x11/x11_window.cc
    #23 0x55e5b10c6762 in ui::PlatformEventSource::DispatchEvent(ui::Event*) ui/events/platform/platform_event_source.cc:101:29
    #24 0x55e5b10c102b in ui::X11EventSource::DispatchPlatformEvent(ui::Event* const&, _XEvent*) ui/events/platform/x11/x11_event_source.cc:303:3
    #25 0x55e5b10bee01 in ProcessXEvent ui/events/platform/x11/x11_event_source.cc:358:5
    #26 0x55e5b10bee01 in ui::X11EventSource::ExtractCookieDataDispatchEvent(_XEvent*) ui/events/platform/x11/x11_event_source.cc:378:3
    #27 0x55e5b10beb39 in ui::X11EventSource::DispatchXEvents() ui/events/platform/x11/x11_event_source.cc:158:5
    #28 0x55e5b10d886c in ui::(anonymous namespace)::XSourceDispatch(_GSource*, int (*)(void*), void*) ui/events/platform/x11/x11_event_watcher_glib.cc:40:15
    #29 0x7f0f0ee08284 in g_main_context_dispatch (/usr/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x4c284)

0x611000423000 is located 0 bytes inside of 224-byte region [0x611000423000,0x6110004230e0)
freed by thread T0 (chrome) here:
    #0 0x55e5a432515d in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:160:3
    #1 0x55e5adeb1b30 in operator() buildtools/third_party/libc++/trunk/include/memory:2378:5
    #2 0x55e5adeb1b30 in reset buildtools/third_party/libc++/trunk/include/memory:2633:7
    #3 0x55e5adeb1b30 in ~unique_ptr buildtools/third_party/libc++/trunk/include/memory:2587:19
    #4 0x55e5adeb1b30 in MediaStreamCaptureIndicator::UIDelegate::~UIDelegate() chrome/browser/media/webrtc/media_stream_capture_indicator.cc:182:3
    #5 0x55e5adeb1ccc in MediaStreamCaptureIndicator::UIDelegate::~UIDelegate() chrome/browser/media/webrtc/media_stream_capture_indicator.cc:179:26
    #6 0x55e5a862b83e in operator() buildtools/third_party/libc++/trunk/include/memory:2378:5
    #7 0x55e5a862b83e in reset buildtools/third_party/libc++/trunk/include/memory:2633:7
    #8 0x55e5a862b83e in ~unique_ptr buildtools/third_party/libc++/trunk/include/memory:2587:19
    #9 0x55e5a862b83e in ~Core content/browser/renderer_host/media/media_stream_ui_proxy.cc:107:1
    #10 0x55e5a862b83e in base::DeleteHelper<content::MediaStreamUIProxy::Core>::DoDelete(void const*) base/sequenced_task_runner_helpers.h:24:5
    #11 0x55e5aec29b79 in Run base/callback.h:99:12
    #12 0x55e5aec29b79 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:142:33
    #13 0x55e5aec638e1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:321:23
    #14 0x55e5aec63248 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:246:36
    #15 0x55e5aeb63c5c in HandleDispatch base/message_loop/message_pump_glib.cc:409:46
    #16 0x55e5aeb63c5c in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:122:43
    #17 0x7f0f0ee08416 in g_main_context_dispatch (/usr/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x4c416)

previously allocated by thread T0 (chrome) here:
    #0 0x55e5a43248fd in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:99:3
    #1 0x55e5b8512cd2 in TabSharingUI::Create(content::DesktopMediaID const&, std::__1::basic_string<unsigned short, base::string16_internals::string16_char_traits, std::__1::allocator<unsigned short> >) chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views.cc:117:27
    #2 0x55e5ae4e9015 in GetDevicesForDesktopCapture(content::WebContents*, std::__1::vector<blink::MediaStreamDevice, std::__1::allocator<blink::MediaStreamDevice> >*, content::DesktopMediaID const&, blink::mojom::MediaStreamType, blink::mojom::MediaStreamType, bool, bool, bool, std::__1::basic_string<unsigned short, base::string16_internals::string16_char_traits, std::__1::allocator<unsigned short> > const&, std::__1::basic_string<unsigned short, base::string16_internals::string16_char_traits, std::__1::allocator<unsigned short> > const&) chrome/browser/media/webrtc/desktop_capture_devices_util.cc:187:25
    #3 0x55e5ae4e39d0 in DisplayMediaAccessHandler::OnPickerDialogResults(content::WebContents*, content::DesktopMediaID) chrome/browser/media/webrtc/display_media_access_handler.cc:232:12
    #4 0x55e5ae4e766e in Invoke<void (DisplayMediaAccessHandler::*)(content::WebContents *, content::DesktopMediaID), DisplayMediaAccessHandler *, content::WebContents *, content::DesktopMediaID> base/bind_internal.h:490:12
    #5 0x55e5ae4e766e in MakeItSo<void (DisplayMediaAccessHandler::*)(content::WebContents *, content::DesktopMediaID), DisplayMediaAccessHandler *, content::WebContents *, content::DesktopMediaID> base/bind_internal.h:624:12
    #6 0x55e5ae4e766e in RunImpl<void (DisplayMediaAccessHandler::*)(content::WebContents *, content::DesktopMediaID), std::__1::tuple<base::internal::UnretainedWrapper<DisplayMediaAccessHandler>, content::WebContents *>, 0, 1> base/bind_internal.h:697:12
    #7 0x55e5ae4e766e in base::internal::Invoker<base::internal::BindState<void (DisplayMediaAccessHandler::*)(content::WebContents*, content::DesktopMediaID), base::internal::UnretainedWrapper<DisplayMediaAccessHandler>, content::WebContents*>, void (content::DesktopMediaID)>::RunOnce(base::internal::BindStateBase*, content::DesktopMediaID&&) base/bind_internal.h:666:12
    #8 0x55e5b80029b6 in Run base/callback.h:99:12
    #9 0x55e5b80029b6 in Invoke<base::OnceCallback<void (content::DesktopMediaID)>, content::DesktopMediaID> base/bind_internal.h:585:49
    #10 0x55e5b80029b6 in MakeItSo<base::OnceCallback<void (content::DesktopMediaID)>, content::DesktopMediaID> base/bind_internal.h:624:12
    #11 0x55e5b80029b6 in RunImpl<base::OnceCallback<void (content::DesktopMediaID)>, std::__1::tuple<content::DesktopMediaID>, 0> base/bind_internal.h:697:12
    #12 0x55e5b80029b6 in base::internal::Invoker<base::internal::BindState<base::OnceCallback<void (content::DesktopMediaID)>, content::DesktopMediaID>, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:666:12
    #13 0x55e5aec29b79 in Run base/callback.h:99:12
    #14 0x55e5aec29b79 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:142:33
    #15 0x55e5aec638e1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:321:23
    #16 0x55e5aec63248 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:246:36
    #17 0x55e5aeb62e70 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:443:48
    #18 0x55e5aec64b39 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:425:12
    #19 0x55e5aebdacc6 in base::RunLoop::Run() base/run_loop.cc:124:14
    #20 0x55e5add818fc in ChromeBrowserMainParts::MainMessageLoopRun(int*) chrome/browser/chrome_browser_main.cc:1683:15
    #21 0x55e5a7af2242 in content::BrowserMainLoop::RunMainMessageLoopParts() content/browser/browser_main_loop.cc:1054:29
    #22 0x55e5a7af86f1 in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:150:15
    #23 0x55e5a7aea35c in content::BrowserMain(content::MainFunctionParams const&) content/browser/browser_main.cc:47:28
    #24 0x55e5adb8ab6e in RunBrowserProcessMain content/app/content_main_runner_impl.cc:502:10
    #25 0x55e5adb8ab6e in content::ContentMainRunnerImpl::RunServiceManager(content::MainFunctionParams&, bool) content/app/content_main_runner_impl.cc:944:10
    #26 0x55e5adb89ea1 in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:845:12
    #27 0x55e5add1d305 in service_manager::Main(service_manager::MainParams const&) services/service_manager/embedder/main.cc:454:29
    #28 0x55e5adb84f96 in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:19:10
    #29 0x55e5a4327424 in ChromeMain chrome/app/chrome_main.cc:110:12
    #30 0x7f0f099fcb96 in __libc_start_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310

SUMMARY: AddressSanitizer: heap-use-after-free chrome/browser/ui/tab_sharing/tab_sharing_infobar_delegate.cc:84:8 in TabSharingInfoBarDelegate::Accept()
Shadow bytes around the buggy address:
  0x0c228007c5b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c228007c5c0: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa
  0x0c228007c5d0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c228007c5e0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c228007c5f0: fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa fa
=>0x0c228007c600:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c228007c610: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa
  0x0c228007c620: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
  0x0c228007c630: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c228007c640: 00 00 00 fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c228007c650: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==18964==ABORTING

Did this work before? N/A 

Chrome version: Chromium 84.0.4127.0  Channel: n/a
OS Version: Ubuntu8.04
Flash Version:

## Attachments

- [poc.zip](attachments/poc.zip) (application/octet-stream, 5.4 MB)

## Timeline

### me...@chromium.org (2020-04-27)

marinaciocea: Can you please take a look as an owner of chrome/browser/ui/tab_sharing? Thanks.

(The code has been around for about a year, so I'm assuming this impacts stable channel as well.)

[Monorail components: Blink>GetUserMedia>Desktop]

### ma...@chromium.org (2020-04-27)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-27)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2020-04-27)

This issue is marked as RBS for M-83, please help review the issue and remove the RBS label if this is not deemed critical for M-83, If it is critical please help get the fix landed to canary asap and get the merge ready for M-83 so we can include in beta release. With COVID-19 we want to get all stable blockers fixed asap and get more beta coverage so your help is greatly appreciated.

### ma...@chromium.org (2020-04-29)

Fixed in https://crrev.com/c/2171857.

### ma...@chromium.org (2020-04-29)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-29)

This bug requires manual review: To minimize risk and increase branch stability, all merge requests are being reviewed manually by the release team.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@chromium.org (2020-04-29)

1. Does your merge fit within the Merge Decision Guidelines?
Yes, the CL fixes a security bug.

2. Links to the CLs you are requesting to merge.
https://crrev.com/c/2171857

3. Has the change landed and been verified on master/ToT?
Yes, verified on ToT.

4. Why are these changes required in this milestone after branch?
Fixes a security bug impacting stable.

5. Is this a new feature?
No

6. If it is a new feature, is it behind a flag using finch?
N/A

### sr...@google.com (2020-04-30)

Merge approved for M83 branch:4103 please merge your changes asap

### [Deleted User] (2020-04-30)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4cdaab95fff3abc46d4400eed20d72cf229f796d

commit 4cdaab95fff3abc46d4400eed20d72cf229f796d
Author: Marina Ciocea <marinaciocea@chromium.org>
Date: Thu Apr 30 20:10:10 2020

[M83][TabSharingUI] Replace infobar if it already exists.

There should be only one infobar per tab within a TabSharingUIViews.
When creating a new infobar for a tab, replace the old infobar if there
already exists one for that tab.

(cherry picked from commit 67b81f0558bb733d09a04c173527c842b31a25e7)

Bug: 1074706
Change-Id: I95fab09a5b2c6f3393ec2e8779161ea6a9b349f9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2171857
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Marina Ciocea <marinaciocea@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#763800}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2173189
Reviewed-by: Marina Ciocea <marinaciocea@chromium.org>
Cr-Commit-Position: refs/branch-heads/4103@{#395}
Cr-Branched-From: 8ad47e8d21f6866e4a37f47d83a860d41debf514-refs/heads/master@{#756066}

[modify] https://crrev.com/4cdaab95fff3abc46d4400eed20d72cf229f796d/chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views.cc


### na...@google.com (2020-05-04)

[Empty comment from Monorail migration]

### na...@google.com (2020-05-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-05-07)

Congrats! The Panel decided to award $15,000 for this report. 

### na...@google.com (2020-05-07)

[Empty comment from Monorail migration]

### ad...@google.com (2020-05-15)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-05-18)

[Empty comment from Monorail migration]

### ke...@google.com (2020-05-18)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e88e24ab48a60a3a95f001eba7c6b809aca1aea5

commit e88e24ab48a60a3a95f001eba7c6b809aca1aea5
Author: Marina Ciocea <marinaciocea@chromium.org>
Date: Tue May 19 17:40:34 2020

[M81][TabSharingUI] Replace infobar if it already exists.

There should be only one infobar per tab within a TabSharingUIViews.
When creating a new infobar for a tab, replace the old infobar if there
already exists one for that tab.

(cherry picked from commit 67b81f0558bb733d09a04c173527c842b31a25e7)

(cherry picked from commit 4cdaab95fff3abc46d4400eed20d72cf229f796d)

Bug: 1074706
Change-Id: I95fab09a5b2c6f3393ec2e8779161ea6a9b349f9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2171857
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Marina Ciocea <marinaciocea@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#763800}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2173189
Reviewed-by: Marina Ciocea <marinaciocea@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4103@{#395}
Cr-Original-Branched-From: 8ad47e8d21f6866e4a37f47d83a860d41debf514-refs/heads/master@{#756066}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2208257
Commit-Queue: Jorge Lucangeli Obes <jorgelo@chromium.org>
Cr-Commit-Position: refs/branch-heads/4044@{#1015}
Cr-Branched-From: a6d9daf149a473ceea37f629c41d4527bf2055bd-refs/heads/master@{#737173}

[modify] https://crrev.com/e88e24ab48a60a3a95f001eba7c6b809aca1aea5/chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views.cc


### ad...@chromium.org (2020-05-21)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-06-30)

marinaciocea@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### [Deleted User] (2020-08-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1074706?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052122)*
