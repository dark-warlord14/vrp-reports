# Heap-use-after-free in SelectFileDialogExtension::ExtensionDialogClosing

| Field | Value |
|-------|-------|
| **Issue ID** | [40093674](https://issues.chromium.org/issues/40093674) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Views, UI>Browser |
| **Platforms** | ChromeOS |
| **Reporter** | cl...@chromium.org |
| **Assignee** | xi...@chromium.org |
| **Created** | 2019-01-08 |
| **Bounty** | $2,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=6332039456096256

Fuzzer: attekett_webaudio_fuzzer
Job Type: linux_asan_chrome_chromeos
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60c000186110
Crash State:
  SelectFileDialogExtension::ExtensionDialogClosing
  views::Widget::OnNativeWidgetDestroying
  views::NativeWidgetAura::OnWindowDestroying
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_chromeos&range=614363:614364

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6332039456096256

Additional requirements: Requires Gestures

Issue filed automatically.

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

## Timeline

### cl...@chromium.org (2019-01-08)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Views UI>Browser]

### cl...@chromium.org (2019-01-08)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/2a66b11ee57844b24718b518f170706bc9242eab (cros: Fix startup page focus).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### sh...@chromium.org (2019-01-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-08)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-01-08)

[Empty comment from Monorail migration]

### xi...@chromium.org (2019-01-08)

Not sure how it is related to my CL but I could see how it happens. It happens when shutting down with a browser window that has a select file dialog open. During shutdown, we explicitly release Brower object [1], which releases its ref to the SelectFileDialog. And when it comes time to close the select file dialog widget, SelectFileDialogExtension::ExtensionDialogClosing releases last ref to itself [2]. Hence the UAF.


[1] https://cs.chromium.org/chromium/src/chrome/browser/lifetime/browser_close_manager.cc?rcl=f18b096e2de34e724331bfa7b8d3b25eb2e1fc8e&l=181

[2] https://cs.chromium.org/chromium/src/chrome/browser/ui/views/select_file_dialog_extension.cc?rcl=544bafe450869800b25f6a0f9e8a14d201c3ed29&l=218

### xi...@chromium.org (2019-01-08)

Interesting part of the log in the report:

==1493249==ERROR: AddressSanitizer: heap-use-after-free on address 0x6100002adb90 at pc 0x55a6978d28be bp 0x7ffe3ae18a50 sp 0x7ffe3ae18a48
READ of size 8 at 0x6100002adb90 thread T0 (chrome)
SCARINESS: 51 (8-byte-read-heap-use-after-free)
    #0 0x55a6978d28bd in NotifyListener chrome/browser/ui/views/select_file_dialog_extension.cc:301:8
    #1 0x55a6978d28bd in SelectFileDialogExtension::ExtensionDialogClosing(ExtensionDialog*) chrome/browser/ui/views/select_file_dialog_extension.cc:220
    #2 0x55a693e0c1b0 in views::Widget::OnNativeWidgetDestroying() ui/views/widget/widget.cc:1116:21
    #3 0x55a693e3f673 in OnWindowDestroying ui/views/widget/native_widget_aura.cc:889:14
    #4 0x55a693e3f673 in non-virtual thunk to views::NativeWidgetAura::OnWindowDestroying(aura::Window*) ui/views/widget/native_widget_aura.cc:0
    #5 0x55a692cdfc38 in aura::Window::~Window() ui/aura/window.cc:103:16
    #6 0x55a692ce203c in aura::Window::~Window() ui/aura/window.cc:94:19
    #7 0x55a693f33af8 in wm::TransientWindowManager::OnWindowDestroying(aura::Window*) ui/wm/core/transient_window_manager.cc:231:5
    #8 0x55a692ce01a5 in aura::Window::~Window() ui/aura/window.cc:105:14
    #9 0x55a692ce203c in aura::Window::~Window() ui/aura/window.cc:94:19
    #10 0x55a693e054d9 in views::Widget::CloseNow() ui/views/widget/widget.cc:613:19
    #11 0x55a68ce1f3f0 in BrowserCloseManager::CloseBrowsers() chrome/browser/lifetime/browser_close_manager.cc:181:26
    #12 0x55a68ca7af12 in chrome::CloseAllBrowsers() chrome/browser/lifetime/application_lifetime.cc:195:26
    #13 0x55a68ca7d4d7 in AttemptExitInternal chrome/browser/lifetime/application_lifetime.cc:151:39
    #14 0x55a68ca7d4d7 in chrome::ExitIgnoreUnloadHandlers() chrome/browser/lifetime/application_lifetime.cc:317
    #15 0x55a68cf81a70 in Exit chrome/browser/chrome_browser_main_posix.cc:102:3
    #16 0x55a68cf81a70 in (anonymous namespace)::ExitHandler::ExitWhenPossibleOnUIThread() chrome/browser/chrome_browser_main_posix.cc:73
...
	freed by thread T0 (chrome) here:
    #0 0x55a681339852 in operator delete(void*) _asan_rtl_:3
    #1 0x55a6978d65cc in DeleteInternal<ui::SelectFileDialog> base/memory/ref_counted.h:414:5
    #2 0x55a6978d65cc in Destruct base/memory/ref_counted.h:369
    #3 0x55a6978d65cc in Release base/memory/ref_counted.h:403
    #4 0x55a6978d65cc in Release base/memory/scoped_refptr.h:297
    #5 0x55a6978d65cc in ~scoped_refptr base/memory/scoped_refptr.h:209
    #6 0x55a6978d65cc in ~pair buildtools/third_party/libc++/trunk/include/utility:315
    #7 0x55a6978d65cc in __destroy<std::__1::pair<const void *const, scoped_refptr<SelectFileDialogExtension> > > buildtools/third_party/libc++/trunk/include/memory:1734
    #8 0x55a6978d65cc in destroy<std::__1::pair<const void *const, scoped_refptr<SelectFileDialogExtension> > > buildtools/third_party/libc++/trunk/include/memory:1597
    #9 0x55a6978d65cc in erase buildtools/third_party/libc++/trunk/include/__tree:2519
    #10 0x55a6978d65cc in unsigned long std::__1::__tree<std::__1::__value_type<void const*, scoped_refptr<SelectFileDialogExtension> >, std::__1::__map_value_compare<void const*, std::__1::__value_type<void const*, scoped_refptr<SelectFileDialogExtension> >, std::__1::less<void const*>, true>, std::__1::allocator<std::__1::__value_type<void const*, scoped_refptr<SelectFileDialogExtension> > > >::__erase_unique<void const*>(void const* const&) buildtools/third_party/libc++/trunk/include/__tree:2542
    #11 0x55a6978d2625 in erase buildtools/third_party/libc++/trunk/include/map:1269:25
    #12 0x55a6978d2625 in Remove chrome/browser/ui/views/select_file_dialog_extension.cc:92
    #13 0x55a6978d2625 in SelectFileDialogExtension::ExtensionDialogClosing(ExtensionDialog*) chrome/browser/ui/views/select_file_dialog_extension.cc:218
    #14 0x55a693e0c1b0 in views::Widget::OnNativeWidgetDestroying() ui/views/widget/widget.cc:1116:21
    #15 0x55a693e3f673 in OnWindowDestroying ui/views/widget/native_widget_aura.cc:889:14
    #16 0x55a693e3f673 in non-virtual thunk to views::NativeWidgetAura::OnWindowDestroying(aura::Window*) ui/views/widget/native_widget_aura.cc:0
    #17 0x55a692cdfc38 in aura::Window::~Window() ui/aura/window.cc:103:16
    #18 0x55a692ce203c in aura::Window::~Window() ui/aura/window.cc:94:19
    #19 0x55a693f33af8 in wm::TransientWindowManager::OnWindowDestroying(aura::Window*) ui/wm/core/transient_window_manager.cc:231:5
    #20 0x55a692ce01a5 in aura::Window::~Window() ui/aura/window.cc:105:14
    #21 0x55a692ce203c in aura::Window::~Window() ui/aura/window.cc:94:19
    #22 0x55a693e054d9 in views::Widget::CloseNow() ui/views/widget/widget.cc:613:19
    #23 0x55a68ce1f3f0 in BrowserCloseManager::CloseBrowsers() chrome/browser/lifetime/browser_close_manager.cc:181:26
    #24 0x55a68ca7af12 in chrome::CloseAllBrowsers() chrome/browser/lifetime/application_lifetime.cc:195:26
    #25 0x55a68ca7d4d7 in AttemptExitInternal chrome/browser/lifetime/application_lifetime.cc:151:39
    #26 0x55a68ca7d4d7 in chrome::ExitIgnoreUnloadHandlers() chrome/browser/lifetime/application_lifetime.cc:317
    #27 0x55a68cf81a70 in Exit chrome/browser/chrome_browser_main_posix.cc:102:3
    #28 0x55a68cf81a70 in (anonymous namespace)::ExitHandler::ExitWhenPossibleOnUIThread() chrome/browser/chrome_browser_main_posix.cc:73
...
	previously allocated by thread T0 (chrome) here:
    #0 0x55a681338c12 in operator new(unsigned long) _asan_rtl_:3
    #1 0x55a6978d1b45 in SelectFileDialogExtension::Create(ui::SelectFileDialog::Listener*, std::__1::unique_ptr<ui::SelectFilePolicy, std::__1::default_delete<ui::SelectFilePolicy> >) chrome/browser/ui/views/select_file_dialog_extension.cc:181:10
    #2 0x55a6978d76dc in SelectFileDialogExtensionFactory::Create(ui::SelectFileDialog::Listener*, std::__1::unique_ptr<ui::SelectFilePolicy, std::__1::default_delete<ui::SelectFilePolicy> >) chrome/browser/ui/views/select_file_dialog_extension_factory.cc:19:10
    #3 0x55a6935fd472 in ui::SelectFileDialog::Create(ui::SelectFileDialog::Listener*, std::__1::unique_ptr<ui::SelectFilePolicy, std::__1::default_delete<ui::SelectFilePolicy> >) ui/shell_dialogs/select_file_dialog.cc:70:29
    #4 0x55a69758fb7f in Browser::OpenFile() chrome/browser/ui/browser.cc:933:25
    #5 0x55a6975a87ab in chrome::BrowserCommandController::ExecuteCommandWithDisposition(int, WindowOpenDisposition) chrome/browser/ui/browser_command_controller.cc:572:17
    #6 0x55a69c7380b6 in ui::AcceleratorManager::Process(ui::Accelerator const&) ui/base/accelerators/accelerator_manager.cc:89:18
    #7 0x55a693d99684 in views::FocusManager::ProcessAccelerator(ui::Accelerator const&) ui/views/focus/focus_manager.cc:515:28
    #8 0x55a69844a8da in views::UnhandledKeyboardEventHandler::HandleKeyboardEvent(content::NativeWebKeyboardEvent const&, views::FocusManager*) ui/views/controls/webview/unhandled_keyboard_event_handler.cc:48:24

### xi...@chromium.org (2019-01-08)

The key to repro is to call Browser::OpenFile twice. The clusterfuzz gestures has two Ctrl+O that end up with that.

  ...,"key,control+o","keydown,7","key,ctrl+o",...

For a real user, this probably never going to happen tho.

### bu...@chromium.org (2019-01-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4e75b7938e4738e14949d86cdbeb5cd43bef9b4a

commit 4e75b7938e4738e14949d86cdbeb5cd43bef9b4a
Author: Xiyuan Xia <xiyuan@chromium.org>
Date: Wed Jan 09 03:08:46 2019

Fix Browser::OpenFile use-after-free

Happened when clusterfuzz managed to invoke IDC_OPEN_FILE twice.

Bug: 919800
Change-Id: I498c4792696ff508d853a78b63459d0237d39a5e
Reviewed-on: https://chromium-review.googlesource.com/c/1401430
Commit-Queue: Xiyuan Xia <xiyuan@chromium.org>
Reviewed-by: Michael Wasserman <msw@chromium.org>
Cr-Commit-Position: refs/heads/master@{#621023}
[modify] https://crrev.com/4e75b7938e4738e14949d86cdbeb5cd43bef9b4a/chrome/browser/ui/browser.cc
[modify] https://crrev.com/4e75b7938e4738e14949d86cdbeb5cd43bef9b4a/chrome/browser/ui/browser.h
[modify] https://crrev.com/4e75b7938e4738e14949d86cdbeb5cd43bef9b4a/chrome/browser/ui/views/select_file_dialog_extension_browsertest.cc


### xi...@chromium.org (2019-01-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-01-09)

ClusterFuzz has detected this issue as fixed in range 621020:621024.

Detailed report: https://clusterfuzz.com/testcase?key=6332039456096256

Fuzzer: attekett_webaudio_fuzzer
Job Type: linux_asan_chrome_chromeos
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60c000186110
Crash State:
  SelectFileDialogExtension::ExtensionDialogClosing
  views::Widget::OnNativeWidgetDestroying
  views::NativeWidgetAura::OnWindowDestroying
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_chromeos&range=614363:614364
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_chromeos&range=621020:621024

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6332039456096256

Additional requirements: Requires Gestures

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2019-01-09)

ClusterFuzz testcase 6332039456096256 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2019-01-10)

[Empty comment from Monorail migration]

### na...@google.com (2019-01-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### pa...@chromium.org (2019-01-17)

Congrats! The Panel decided to reward $2,500 for this report :) 

### aw...@google.com (2019-01-21)

[Empty comment from Monorail migration]

### aw...@google.com (2019-02-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/919800?no_tracker_redirect=1

[Multiple monorail components: Internals>Views, UI>Browser]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093674)*
