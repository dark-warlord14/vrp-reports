# Security: heap-buffer-overflow in SelectFileDialogImpl::OnSelectFileExecuted

| Field | Value |
|-------|-------|
| **Issue ID** | [40056997](https://issues.chromium.org/issues/40056997) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Cast>UI |
| **Platforms** | Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ta...@chromium.org |
| **Created** | 2021-08-24 |
| **Bounty** | $7,000.00 |

## Description

Chrome Version: 95.0.4620.0 (Official Build) canary (64-bit) (cohort: Clang-64)  

Operating System: Windows 10

**REPRODUCTION CASE**

1. Open the test case or cast any tab by right-click
2. Click on Sources button >> select Cast file
3. Repeat step-2
4. Close the Cast dialog
5. Close the file dialogs

==8972==ERROR: AddressSanitizer: heap-use-after-free on address 0x124e93a41840 at pc 0x7ffe65c55fbf bp 0x00ada41fe600 sp 0x00ada41fe648  

READ of size 8 at 0x124e93a41840 thread T0  

==8972==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ffe65c55fbe in ui::`anonymous namespace'::SelectFileDialogImpl::OnSelectFileExecuted C:\b\s\w\ir\cache\builder\src\ui\shell\_dialogs\select\_file\_dialog\_win.cc:292  

#1 0x7ffe65c56d1b in base::internal::Invoker<base::internal::BindState<void (ui::(anonymous namespace)::SelectFileDialogImpl::\*)(ui::SelectFileDialog::Type, std::\_\_1::unique\_ptr<ui::BaseShellDialogImpl::RunState,std::\_\_1::default\_delete[ui::BaseShellDialogImpl::RunState](javascript:void(0);) >, void \*, const std::\_\_1::vector<base::FilePath,std::\_\_1::allocator[base::FilePath](javascript:void(0);) > &, int),scoped\_refptr<ui::(anonymous namespace)::SelectFileDialogImpl>,ui::SelectFileDialog::Type,std::\_\_1::unique\_ptr<ui::BaseShellDialogImpl::RunState,std::\_\_1::default\_delete[ui::BaseShellDialogImpl::RunState](javascript:void(0);) >,void \*>,void (const std::\_\_1::vector<base::FilePath,std::\_\_1::allocator[base::FilePath](javascript:void(0);) > &, int)>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:690  

#2 0x7ffe65c573fc in base::internal::Invoker<base::internal::BindState<base::OnceCallback<void (const std::\_\_1::vector<base::FilePath,std::\_\_1::allocator[base::FilePath](javascript:void(0);) > &, int)>,std::\_\_1::vector<base::FilePath,std::\_\_1::allocator[base::FilePath](javascript:void(0);) >,int>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:690  

#3 0x7ffe61db685a in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:178  

#4 0x7ffe6474ed32 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:360  

#5 0x7ffe6474e392 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:260  

#6 0x7ffe61e5d136 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:220  

#7 0x7ffe61e5b378 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#8 0x7ffe6475022e in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:467  

#9 0x7ffe61d39153 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:134  

#10 0x7ffe5b270589 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:988  

#11 0x7ffe5b275905 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:152  

#12 0x7ffe5b269bee in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:49  

#13 0x7ffe5db9fab4 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:608  

#14 0x7ffe5dba2350 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1104  

#15 0x7ffe5dba1537 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:971  

#16 0x7ffe5db9dfba in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:390  

#17 0x7ffe5db9effc in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:418  

#18 0x7ffe5775148c in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:172  

#19 0x7ff61ec75b74 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:169  

#20 0x7ff61ec72be8 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#21 0x7ff61f066e8f in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#22 0x7ffee5df7033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  

#23 0x7ffee73e2650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

0x124e93a41840 is located 0 bytes inside of 432-byte region [0x124e93a41840,0x124e93a419f0)  

freed by thread T0 here:  

#0 0x7ff61ed16ddb in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ffe6e75eadb in media\_router::MediaRouterFileDialog::~MediaRouterFileDialog C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\media\_router\media\_router\_file\_dialog.cc:143  

#2 0x7ffe6b3d2339 in media\_router::MediaRouterUI::~MediaRouterUI C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\media\_router\media\_router\_ui.cc:304  

#3 0x7ffe6b3e2747 in media\_router::MediaRouterUI::~MediaRouterUI C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\media\_router\media\_router\_ui.cc:276  

#4 0x7ffe673098aa in media\_router::MediaRouterDialogControllerViews::Reset C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\media\_router\media\_router\_dialog\_controller\_views.cc:139  

#5 0x7ffe67309990 in media\_router::MediaRouterDialogControllerViews::OnWidgetClosing C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\media\_router\media\_router\_dialog\_controller\_views.cc:148  

#6 0x7ffe61b231ca in views::Widget::CloseWithReason C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:696  

#7 0x7ffe61acadb7 in views::Button::NotifyClick C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\button.cc:632  

#8 0x7ffe61ac714d in views::Button::DefaultButtonControllerDelegate::NotifyClick C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\button.cc:66  

#9 0x7ffe642faf66 in views::ButtonController::OnMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\button\_controller.cc:59  

#10 0x7ffe61b04760 in views::View::ProcessMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3050  

#11 0x7ffe6afc427a in ui::ScopedTargetHandler::OnEvent C:\b\s\w\ir\cache\builder\src\ui\events\scoped\_target\_handler.cc:28  

#12 0x7ffe629fd3ef in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:191  

#13 0x7ffe629fc90f in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:140  

#14 0x7ffe629fc2f8 in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:84  

#15 0x7ffe629fbf3c in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:56  

#16 0x7ffe6437260b in views::internal::RootView::OnMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\widget\root\_view.cc:480  

#17 0x7ffe61b2c8b1 in views::Widget::OnMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1548  

#18 0x7ffe629fd3ef in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:191  

#19 0x7ffe629fc90f in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:140  

#20 0x7ffe629fc2f8 in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:84  

#21 0x7ffe629fbf3c in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:56  

#22 0x7ffe67164d4c in ui::EventProcessor::OnEventFromSource C:\b\s\w\ir\cache\builder\src\ui\events\event\_processor.cc:49  

#23 0x7ffe64364b6f in ui::EventSource::DeliverEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:113  

#24 0x7ffe643647c9 in ui::EventSource::SendEventToSinkFromRewriter C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:138  

#25 0x7ffe643642cb in ui::EventSource::SendEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:107  

#26 0x7ffe67162729 in views::DesktopWindowTreeHostWin::HandleMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop\_aura\desktop\_window\_tree\_host\_win.cc:1006  

#27 0x7ffe6b034021 in views::HWNDMessageHandler::HandleMouseEventInternal C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:3143

previously allocated by thread T0 here:  

#0 0x7ff61ed16edb in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ffe742e1a2a in operator new d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ffe6b3d49e0 in media\_router::MediaRouterUI::OpenFileDialog C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\media\_router\media\_router\_ui.cc:519  

#3 0x7ffe6b3d48b1 in media\_router::MediaRouterUI::ChooseLocalFile C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\media\_router\media\_router\_ui.cc:332  

#4 0x7ffe6b3ccec1 in media\_router::CastDialogView::ExecuteCommand C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\media\_router\cast\_dialog\_view.cc:177  

#5 0x7ffe6e3d1e59 in views::MenuModelAdapter::ExecuteCommand C:\b\s\w\ir\cache\builder\src\ui\views\controls\menu\menu\_model\_adapter.cc:170  

#6 0x7ffe67128f4f in views::internal::MenuRunnerImpl::OnMenuClosed C:\b\s\w\ir\cache\builder\src\ui\views\controls\menu\menu\_runner\_impl.cc:245  

#7 0x7ffe6afcdd32 in views::MenuController::ExitMenu C:\b\s\w\ir\cache\builder\src\ui\views\controls\menu\menu\_controller.cc:3154  

#8 0x7ffe6afd3153 in views::MenuController::Accept C:\b\s\w\ir\cache\builder\src\ui\views\controls\menu\menu\_controller.cc:1780  

#9 0x7ffe6afd26e7 in views::MenuController::OnMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\controls\menu\menu\_controller.cc:827  

#10 0x7ffe61b2c8b1 in views::Widget::OnMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1548  

#11 0x7ffe629fd3ef in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:191  

#12 0x7ffe629fc90f in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:140  

#13 0x7ffe629fc2f8 in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:84  

#14 0x7ffe629fbf3c in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:56  

#15 0x7ffe67164d4c in ui::EventProcessor::OnEventFromSource C:\b\s\w\ir\cache\builder\src\ui\events\event\_processor.cc:49  

#16 0x7ffe64364b6f in ui::EventSource::DeliverEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:113  

#17 0x7ffe643647c9 in ui::EventSource::SendEventToSinkFromRewriter C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:138  

#18 0x7ffe643642cb in ui::EventSource::SendEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:107  

#19 0x7ffe67162729 in views::DesktopWindowTreeHostWin::HandleMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop\_aura\desktop\_window\_tree\_host\_win.cc:1006  

#20 0x7ffe6b034021 in views::HWNDMessageHandler::HandleMouseEventInternal C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:3143  

#21 0x7ffe6b02d473 in views::HWNDMessageHandler::\_ProcessWindowMessage C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.h:356  

#22 0x7ffe6b02cb12 in views::HWNDMessageHandler::OnWndProc C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:1017  

#23 0x7ffe64a8b34a in gfx::WindowImpl::WndProc C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window\_impl.cc:306  

#24 0x7ffe64a89c65 in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc> C:\b\s\w\ir\cache\builder\src\base\win\wrapped\_window\_proc.h:74  

#25 0x7ffee70de857 in CallWindowProcW+0x3f7 (C:\Windows\System32\user32.dll+0x18000e857)  

#26 0x7ffee70de298 in DispatchMessageW+0x258 (C:\Windows\System32\user32.dll+0x18000e298)  

#27 0x7ffe61e5f76a in base::MessagePumpForUI::ProcessMessageHelper C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:542

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\ui\shell\_dialogs\select\_file\_dialog\_win.cc:292 in ui::`anonymous namespace'::SelectFileDialogImpl::OnSelectFileExecuted  

Shadow bytes around the buggy address:  

0x047065dc82b0: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa  

0x047065dc82c0: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

0x047065dc82d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x047065dc82e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x047065dc82f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x047065dc8300: fa fa fa fa fa fa fa fa[fd]fd fd fd fd fd fd fd  

0x047065dc8310: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x047065dc8320: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x047065dc8330: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa  

0x047065dc8340: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x047065dc8350: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==8972==ABORTING

## Attachments

- [cast.html](attachments/cast.html) (text/plain, 963 B)
- [screen.mp4](attachments/screen.mp4) (video/mp4, 2.0 MB)
- [screen.mp4](attachments/screen.mp4) (video/mp4, 964.4 KB)

## Timeline

### [Deleted User] (2021-08-24)

[Empty comment from Monorail migration]

### dr...@chromium.org (2021-08-24)

I'm unable to reproduce the automatic crash with the PoC. Can you share a screencast of that as well, in case I misunderstood some steps?

The crash with user gestures reproduced as claimed on Windows in M92. On Linux, the file chooser maintained the focus at all times, so I wasn't able to open a second file picker. Assigning Medium severity, as this requires a very detailed set of user gestures, and requires the user be on the same network as a Chromecast device.

mfolts@, btolsh@ - can you take a look?

[Monorail components: Internals>Cast>UI]

### [Deleted User] (2021-08-24)

[Empty comment from Monorail migration]

### ch...@gmail.com (2021-08-24)

If you want to repro this with the PoC, you will need to disable chrome://flags/#global-media-controls-cast-start-stop flag.

### ch...@gmail.com (2021-08-24)

[Empty comment from Monorail migration]

### mf...@chromium.org (2021-08-24)

[Empty comment from Monorail migration]

### dr...@chromium.org (2021-08-24)

Thank you for sharing. Since the PoC still requires all the same user gestures, I'll leave the severity determination where it is.

### [Deleted User] (2021-08-25)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dr...@chromium.org (2021-08-27)

[Empty comment from Monorail migration]

### ta...@chromium.org (2021-08-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-14)

takumif: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### ch...@gmail.com (2021-09-29)

[Comment Deleted]

### ch...@gmail.com (2021-09-29)

Friendly ping. Any update? - Thanks :)


### [Deleted User] (2021-09-29)

takumif: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@gmail.com (2021-11-01)

takumif@ Friendly ping :).

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-01-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/823301b29d38ed1d393c1488c0f7069d229a2d74

commit 823301b29d38ed1d393c1488c0f7069d229a2d74
Author: Takumi Fujimoto <takumif@chromium.org>
Date: Sat Jan 08 05:28:27 2022

Cast UI: Remove the "cast file" option from the sources dropdown

The underlying MediaRouterUI/MediaRouterFileDialog code is deleted in a
subsequent CL.

Bug: 1284717, 1242962, 1274077
Change-Id: I04c7414795b28bf1e2658ec51e4198efa9c0f016
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3355496
Reviewed-by: Muyao Xu <muyaoxu@google.com>
Commit-Queue: Takumi Fujimoto <takumif@chromium.org>
Cr-Commit-Position: refs/heads/main@{#956805}

[modify] https://crrev.com/823301b29d38ed1d393c1488c0f7069d229a2d74/chrome/browser/ui/views/media_router/cast_dialog_view.cc
[modify] https://crrev.com/823301b29d38ed1d393c1488c0f7069d229a2d74/chrome/browser/ui/views/media_router/cast_dialog_view_unittest.cc
[modify] https://crrev.com/823301b29d38ed1d393c1488c0f7069d229a2d74/chrome/test/media_router/media_router_cast_ui_for_test.cc
[modify] https://crrev.com/823301b29d38ed1d393c1488c0f7069d229a2d74/chrome/browser/ui/views/media_router/cast_dialog_view.h


### ch...@gmail.com (2022-01-08)

Thanks for the fix! 

### ch...@gmail.com (2022-01-21)

I think this bug should be marked as Fixed. 

### ta...@google.com (2022-01-22)

Yup, thanks for pinging.

### [Deleted User] (2022-01-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-22)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-17)

Congratulations, Khalil on another one! The VRP Panel has decided to award you $7000 for this report. Thank your efforts and reporting this issue to us. 

### am...@google.com (2022-02-18)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-02-28)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1242962?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1244042]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056997)*
