# Security: heap-use-after-free in views::DesktopWindowTreeHostWin::~DesktopWindowTreeHostWin

| Field | Value |
|-------|-------|
| **Issue ID** | [408132930](https://issues.chromium.org/issues/408132930) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Aura |
| **Platforms** | Windows |
| **Chrome Version** | 135.0.0.0 |
| **Reporter** | zh...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2025-04-03 |
| **Bounty** | $3,000.00 |

## Description

# Steps to reproduce the problem

1. Compile asan chromium using Windows11, the steps are as follows:

```
git checkout 028edb4fcf20b78e5f573d4575f6b1da914ee358
git apply poc.diff
gn gen out/asan-0403 --args="is_component_build=true is_debug=false is_asan=true symbol_level=2 dcheck_always_on=false treat_warnings_as_errors=false"

```

2. Run the following command:

```
./out/asan-0403/chrome.exe --enable-features=WebMachineLearningNeuralNetwork --no-sandbox --enable-experimental-web-platform-features --user-data-dir=./tmp/userdata/t13 http://127.0.0.1/1.html

```

3. Following the steps in poc.mov, the UAF can be reproduced stably.

# Problem Description

RCA and bisect coming soon!

# Summary

Security: heap-use-after-free in views::DesktopWindowTreeHostWin::~DesktopWindowTreeHostWin

# Custom Questions

#### Type of crash:

browser

#### Crash state:

```
./out/asan-0403/chrome.exe --enable-features=WebMachineLearningNeuralNetwork --no-sandbox --enable-experimental-web-platform-features --user-data-dir=./tmp/userdata/t13 http://127.0.0.1/1.html
[4476:9068:0403/193157.671:ERROR:chrome\browser\policy\cloud\fm_registration_token_uploader.cc:179] Client is missing for kUser scope
[4476:9068:0403/193157.671:ERROR:chrome\browser\policy\cloud\fm_registration_token_uploader.cc:179] Client is missing for kUser scope
[4476:26396:0403/193157.885:ERROR:google_apis\gcm\engine\registration_request.cc:291] Registration response error message: DEPRECATED_ENDPOINT
=================================================================
==4476==ERROR: AddressSanitizer: heap-use-after-free on address 0x11708fce7270 at pc 0x014281a86025 bp 0x002ad21fae20 sp 0x002ad21fae68
READ of size 8 at 0x11708fce7270 thread T0
    #0 0x014281a86024 in base::ObserverList<views::WidgetObserver,0,1,base::internal::CheckedObserverAdapter>::RemoveObserver C:\Users\test\src-chromium\src\base\observer_list.h:327
    #1 0x01428165345f in base::ScopedObservation<views::Widget,views::WidgetObserver>::~ScopedObservation C:\Users\test\src-chromium\src\base\scoped_observation.h:101
    #2 0x014281bcb5c3 in views::DesktopWindowTreeHostWin::~DesktopWindowTreeHostWin C:\Users\test\src-chromium\src\ui\views\widget\desktop_aura\desktop_window_tree_host_win.cc:145
    #3 0x014281bdcba6 in views::DesktopWindowTreeHostWin::`vector deleting destructor'+0x16 (C:\Users\test\src-chromium\src\out\asan-0403\ui_views.dll+0x1805acba6)
    #4 0x014281bb27da in views::DesktopNativeWidgetAura::OnHostClosed C:\Users\test\src-chromium\src\ui\views\widget\desktop_aura\desktop_native_widget_aura.cc:381
    #5 0x014281affe14 in views::HWNDMessageHandler::OnWndProc C:\Users\test\src-chromium\src\ui\views\win\hwnd_message_handler.cc:1166
    #6 0x7ff8ab5ed76c in gfx::WindowImpl::WndProc C:\Users\test\src-chromium\src\ui\gfx\win\window_impl.cc:313
    #7 0x7ff8ab5ebc3e in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc> C:\Users\test\src-chromium\src\base\win\wrapped_window_proc.h:74
    #8 0x7ff93332b642 in CallWindowProcW+0x852 (C:\WINDOWS\System32\USER32.dll+0x18000b642)
    #9 0x7ff93332ad1b in SendMessageW+0xacb (C:\WINDOWS\System32\USER32.dll+0x18000ad1b)
    #10 0x7ff9333726ca in SetWindowsHookExAW+0x17a (C:\WINDOWS\System32\USER32.dll+0x1800526ca)
    #11 0x7ff93531ffe3 in KiUserCallbackDispatcher+0x23 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18015ffe3)
    #12 0x7ff932c22533 in NtUserDestroyWindow+0x13 (C:\WINDOWS\System32\win32u.dll+0x180002533)
    #13 0x014281b1c6f2 in base::internal::Invoker<base::internal::FunctorTraits<void (views::HWNDMessageHandler::*&&)(),base::WeakPtr<views::HWNDMessageHandler> &&>,base::internal::BindState<1,1,0,void (views::HWNDMessageHandler::*)(),base::WeakPtr<views::HWNDMessageHandler> >,void ()>::RunOnce C:\Users\test\src-chromium\src\base\functional\bind_internal.h:973
    #14 0x7ff89dc0b893 in base::TaskAnnotator::RunTaskImpl C:\Users\test\src-chromium\src\base\task\common\task_annotator.cc:209
    #15 0x7ff89dc976b4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\Users\test\src-chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:456
    #16 0x7ff89dc9652f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\Users\test\src-chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:330
    #17 0x7ff89de232f0 in base::MessagePumpForUI::DoRunLoop C:\Users\test\src-chromium\src\base\message_loop\message_pump_win.cc:262
    #18 0x7ff89de20a68 in base::MessagePumpWin::Run C:\Users\test\src-chromium\src\base\message_loop\message_pump_win.cc:89
    #19 0x7ff89dc993f1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\Users\test\src-chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:629
    #20 0x7ff89db69f1e in base::RunLoop::Run C:\Users\test\src-chromium\src\base\run_loop.cc:134
    #21 0x7ff85af5e081 in content::BrowserMainLoop::RunMainMessageLoop C:\Users\test\src-chromium\src\content\browser\browser_main_loop.cc:1094
    #22 0x7ff85af66a19 in content::BrowserMainRunnerImpl::Run C:\Users\test\src-chromium\src\content\browser\browser_main_runner_impl.cc:156
    #23 0x7ff85af54963 in content::BrowserMain C:\Users\test\src-chromium\src\content\browser\browser_main.cc:32
    #24 0x7ff85e48b572 in content::RunBrowserProcessMain C:\Users\test\src-chromium\src\content\app\content_main_runner_impl.cc:718
    #25 0x7ff85e48ebd6 in content::ContentMainRunnerImpl::RunBrowser C:\Users\test\src-chromium\src\content\app\content_main_runner_impl.cc:1298
    #26 0x7ff85e48e451 in content::ContentMainRunnerImpl::Run C:\Users\test\src-chromium\src\content\app\content_main_runner_impl.cc:1153
    #27 0x7ff85e48199b in content::RunContentProcess C:\Users\test\src-chromium\src\content\app\content_main.cc:359
    #28 0x7ff85e482520 in content::ContentMain C:\Users\test\src-chromium\src\content\app\content_main.cc:372
    #29 0x7ff8667d16cf in ChromeMain C:\Users\test\src-chromium\src\chrome\app\chrome_main.cc:222
    #30 0x7ff659283e6a in MainDllLoader::Launch C:\Users\test\src-chromium\src\chrome\app\main_dll_loader_win.cc:201
    #31 0x7ff659281c27 in main C:\Users\test\src-chromium\src\chrome\app\chrome_exe_main_win.cc:352
    #32 0x7ff65942fc43 in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #33 0x7ff93311e8d6 in BaseThreadInitThunk+0x16 (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #34 0x7ff9352714fb in RtlUserThreadStart+0x2b (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800b14fb)

0x11708fce7270 is located 240 bytes inside of 712-byte region [0x11708fce7180,0x11708fce7448)
freed by thread T0 here:
    #0 0x7ff89c79ae5d in operator delete+0x8d (C:\Users\test\src-chromium\src\out\asan-0403\clang_rt.asan_dynamic-x86_64.dll+0x18005ae5d)
    #1 0x014281b6dc06 in views::corewm::TooltipAura::TooltipWidget::~TooltipWidget C:\Users\test\src-chromium\src\ui\views\corewm\tooltip_aura.cc:108
    #2 0x014281b6cd54 in views::corewm::TooltipAura::Hide C:\Users\test\src-chromium\src\ui\views\corewm\tooltip_aura.cc:309
    #3 0x014281b74d34 in views::corewm::TooltipStateManager::HideAndReset C:\Users\test\src-chromium\src\ui\views\corewm\tooltip_state_manager.cc:54
    #4 0x014281b71ca7 in views::corewm::TooltipController::OnMouseEvent C:\Users\test\src-chromium\src\ui\views\corewm\tooltip_controller.cc:313
    #5 0x7ff8ef57908a in ui::EventDispatcher::DispatchEvent C:\Users\test\src-chromium\src\ui\events\event_dispatcher.cc:189
    #6 0x7ff8ef578a6c in ui::EventDispatcher::DispatchEventToEventHandlers C:\Users\test\src-chromium\src\ui\events\event_dispatcher.cc:176
    #7 0x7ff8ef577747 in ui::EventDispatcher::ProcessEvent C:\Users\test\src-chromium\src\ui\events\event_dispatcher.cc:124
    #8 0x7ff8ef576d70 in ui::EventDispatcherDelegate::DispatchEventToTarget C:\Users\test\src-chromium\src\ui\events\event_dispatcher.cc:84
    #9 0x7ff8ef5766fd in ui::EventDispatcherDelegate::DispatchEvent C:\Users\test\src-chromium\src\ui\events\event_dispatcher.cc:56
    #10 0x7ff8ef57ffb8 in ui::EventProcessor::OnEventFromSource C:\Users\test\src-chromium\src\ui\events\event_processor.cc:72
    #11 0x7ff8ef584050 in ui::EventSource::DeliverEventToSink C:\Users\test\src-chromium\src\ui\events\event_source.cc:119
    #12 0x7ff8ef583925 in ui::EventSource::SendEventToSinkFromRewriter C:\Users\test\src-chromium\src\ui\events\event_source.cc:134
    #13 0x7ff8ef5834ef in ui::EventSource::SendEventToSink C:\Users\test\src-chromium\src\ui\events\event_source.cc:113
    #14 0x014281bda036 in views::DesktopWindowTreeHostWin::HandleMouseEvent C:\Users\test\src-chromium\src\ui\views\widget\desktop_aura\desktop_window_tree_host_win.cc:1215
    #15 0x014281b06edb in views::HWNDMessageHandler::HandleMouseEventInternal C:\Users\test\src-chromium\src\ui\views\win\hwnd_message_handler.cc:3342
    #16 0x014281b00419 in views::HWNDMessageHandler::_ProcessWindowMessage C:\Users\test\src-chromium\src\ui\views\win\hwnd_message_handler.h:395
    #17 0x014281affb53 in views::HWNDMessageHandler::OnWndProc C:\Users\test\src-chromium\src\ui\views\win\hwnd_message_handler.cc:1147
    #18 0x7ff8ab5ed76c in gfx::WindowImpl::WndProc C:\Users\test\src-chromium\src\ui\gfx\win\window_impl.cc:313
    #19 0x7ff8ab5ebc3e in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc> C:\Users\test\src-chromium\src\base\win\wrapped_window_proc.h:74
    #20 0x7ff93332b642 in CallWindowProcW+0x852 (C:\WINDOWS\System32\USER32.dll+0x18000b642)
    #21 0x7ff9333291cc in IsWindowUnicode+0x20c (C:\WINDOWS\System32\USER32.dll+0x1800091cc)
    #22 0x7ff89de25eb7 in base::MessagePumpForUI::ProcessMessageHelper C:\Users\test\src-chromium\src\base\message_loop\message_pump_win.cc:630
    #23 0x7ff89de23ca2 in base::MessagePumpForUI::ProcessNextWindowsMessage C:\Users\test\src-chromium\src\base\message_loop\message_pump_win.cc:592
    #24 0x7ff89de23196 in base::MessagePumpForUI::DoRunLoop C:\Users\test\src-chromium\src\base\message_loop\message_pump_win.cc:252
    #25 0x7ff89de20a68 in base::MessagePumpWin::Run C:\Users\test\src-chromium\src\base\message_loop\message_pump_win.cc:89
    #26 0x7ff89dc993f1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\Users\test\src-chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:629
    #27 0x7ff89db69f1e in base::RunLoop::Run C:\Users\test\src-chromium\src\base\run_loop.cc:134

previously allocated by thread T0 here:
    #0 0x7ff89c79a63d in operator new+0x8d (C:\Users\test\src-chromium\src\out\asan-0403\clang_rt.asan_dynamic-x86_64.dll+0x18005a63d)
    #1 0x014281b6a9a0 in views::corewm::TooltipAura::CreateTooltipWidget C:\Users\test\src-chromium\src\ui\views\corewm\tooltip_aura.cc:198
    #2 0x014281b6b60f in views::corewm::TooltipAura::Update C:\Users\test\src-chromium\src\ui\views\corewm\tooltip_aura.cc:261
    #3 0x014281b75c86 in views::corewm::TooltipStateManager::ShowNow C:\Users\test\src-chromium\src\ui\views\corewm\tooltip_state_manager.cc:121
    #4 0x014281b7612b in base::internal::Invoker<base::internal::FunctorTraits<void (views::corewm::TooltipStateManager::*&&)(const std::__Cr::basic_string<char16_t,std::__Cr::char_traits<char16_t>,std::__Cr::allocator<char16_t> > &, base::TimeDelta),base::WeakPtr<views::corewm::TooltipStateManager> &&,std::__Cr::basic_string<char16_t,std::__Cr::char_traits<char16_t>,std::__Cr::allocator<char16_t> > &&,base::TimeDelta &&>,base::internal::BindState<1,1,0,void (views::corewm::TooltipStateManager::*)(const std::__Cr::basic_string<char16_t,std::__Cr::char_traits<char16_t>,std::__Cr::allocator<char16_t> > &, base::TimeDelta),base::WeakPtr<views::corewm::TooltipStateManager>,std::__Cr::basic_string<char16_t,std::__Cr::char_traits<char16_t>,std::__Cr::allocator<char16_t> >,base::TimeDelta>,void ()>::RunOnce C:\Users\test\src-chromium\src\base\functional\bind_internal.h:973
    #5 0x7ff89dd5b952 in base::OneShotTimer::RunUserTask C:\Users\test\src-chromium\src\base\timer\timer.cc:176
    #6 0x7ff89dd605e5 in base::internal::Invoker<base::internal::FunctorTraits<void (base::internal::DelayTimerBase::*const &)(),base::internal::DelayTimerBase *>,base::internal::BindState<1,1,0,void (base::internal::DelayTimerBase::*)(),base::internal::UnretainedWrapper<base::internal::DelayTimerBase,base::unretained_traits::MayNotDangle,0> >,void ()>::Run C:\Users\test\src-chromium\src\base\functional\bind_internal.h:980
    #7 0x7ff89dc0b893 in base::TaskAnnotator::RunTaskImpl C:\Users\test\src-chromium\src\base\task\common\task_annotator.cc:209
    #8 0x7ff89dc976b4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\Users\test\src-chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:456
    #9 0x7ff89dc9652f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\Users\test\src-chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:330
    #10 0x7ff89de232f0 in base::MessagePumpForUI::DoRunLoop C:\Users\test\src-chromium\src\base\message_loop\message_pump_win.cc:262
    #11 0x7ff89de20a68 in base::MessagePumpWin::Run C:\Users\test\src-chromium\src\base\message_loop\message_pump_win.cc:89
    #12 0x7ff89dc993f1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\Users\test\src-chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:629
    #13 0x7ff89db69f1e in base::RunLoop::Run C:\Users\test\src-chromium\src\base\run_loop.cc:134
    #14 0x7ff85af5e081 in content::BrowserMainLoop::RunMainMessageLoop C:\Users\test\src-chromium\src\content\browser\browser_main_loop.cc:1094
    #15 0x7ff85af66a19 in content::BrowserMainRunnerImpl::Run C:\Users\test\src-chromium\src\content\browser\browser_main_runner_impl.cc:156
    #16 0x7ff85af54963 in content::BrowserMain C:\Users\test\src-chromium\src\content\browser\browser_main.cc:32
    #17 0x7ff85e48b572 in content::RunBrowserProcessMain C:\Users\test\src-chromium\src\content\app\content_main_runner_impl.cc:718
    #18 0x7ff85e48ebd6 in content::ContentMainRunnerImpl::RunBrowser C:\Users\test\src-chromium\src\content\app\content_main_runner_impl.cc:1298
    #19 0x7ff85e48e451 in content::ContentMainRunnerImpl::Run C:\Users\test\src-chromium\src\content\app\content_main_runner_impl.cc:1153
    #20 0x7ff85e48199b in content::RunContentProcess C:\Users\test\src-chromium\src\content\app\content_main.cc:359
    #21 0x7ff85e482520 in content::ContentMain C:\Users\test\src-chromium\src\content\app\content_main.cc:372
    #22 0x7ff8667d16cf in ChromeMain C:\Users\test\src-chromium\src\chrome\app\chrome_main.cc:222
    #23 0x7ff659283e6a in MainDllLoader::Launch C:\Users\test\src-chromium\src\chrome\app\main_dll_loader_win.cc:201
    #24 0x7ff659281c27 in main C:\Users\test\src-chromium\src\chrome\app\chrome_exe_main_win.cc:352
    #25 0x7ff65942fc43 in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #26 0x7ff93311e8d6 in BaseThreadInitThunk+0x16 (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #27 0x7ff9352714fb in RtlUserThreadStart+0x2b (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800b14fb)

SUMMARY: AddressSanitizer: heap-use-after-free C:\Users\test\src-chromium\src\base\observer_list.h:327 in base::ObserverList<views::WidgetObserver,0,1,base::internal::CheckedObserverAdapter>::RemoveObserver
Shadow bytes around the buggy address:
  0x11708fce6f80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x11708fce7000: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x11708fce7080: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x11708fce7100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x11708fce7180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x11708fce7200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd[fd]fd
  0x11708fce7280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x11708fce7300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x11708fce7380: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x11708fce7400: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa
  0x11708fce7480: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
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

==4476==ADDITIONAL INFO

==4476==Note: Please include this section with the ASan report.
Task trace:
    #0 0x014281af8238 in views::HWNDMessageHandler::Close C:\Users\test\src-chromium\src\ui\views\win\hwnd_message_handler.cc:516

Command line: `"C:\Users\test\src-chromium\src\out\asan-0403\chrome.exe" --enable-features=WebMachineLearningNeuralNetwork --no-sandbox --enable-experimental-web-platform-features --user-data-dir=./tmp/userdata/t13 --flag-switches-begin --flag-switches-end --use-fake-device-for-media-stream http://127.0.0.1/1.html`

MiraclePtr Status: MANUAL ANALYSIS REQUIRED
A pointer to the same region was extracted from a raw_ptr<T> object prior to this crash.
To determine the protection status, enable extraction warnings and check whether the raw_ptr<T> object can be destroyed or overwritten between the extraction and use.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==4476==END OF ADDITIONAL INFO
==4476==ABORTING
[28608:2472:0403/193201.608:ERROR:gpu\ipc\client\command_buffer_proxy_impl.cc:127] ContextResult::kTransientFailure: Failed to send GpuControl.CreateCommandBuffer.

```
# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [asas.txt](attachments/asas.txt) (text/plain, 16.9 KB)
- [1.html](attachments/1.html) (text/html, 210.5 KB)
- [poc.diff](attachments/poc.diff) (text/x-diff, 452.7 KB)
- [poc.mp4](attachments/poc.mp4) (video/mp4, 25.7 MB)
- [poc_streamlined.mp4](attachments/poc_streamlined.mp4) (video/mp4, 75.2 MB)

## Timeline

### nh...@chromium.org (2025-04-04)

The provided POC is too large for me to attempt to reproduce. Can you provide a minimized POC? It looks like the majority of the 1.html POC provided consists of code from the WPT harness (<http://web-platform-tests.org/writing-tests/testharness-api.html>) - what portions of the POC are original/written by you instead of being copied from web-platform-tests?

Your report has the `--enable-experimental-web-platform-features` flag set and has a very large number of feature flags enabled by patching the code to change `FEATURE_DISABLED_BY_DEFAULT` to `FEATURE_ENABLED_BY_DEFAULT`. Can you bisect which feature flags are needed to reproduce this?

### zh...@gmail.com (2025-04-04)

Thanks for the quick reply, no problem, I'm working on those now and will get it done asap.

### pe...@google.com (2025-04-04)

Thank you for providing more feedback. Adding the requester to the CC list.

### ro...@chromium.org (2025-04-04)

Routing to kerenzhu for ScopedObservation.

### zh...@gmail.com (2025-04-04)

## Streamlined POC

1. Download asan windows 1442510
2. Run the following command:

```
rm -rf ./tmp; ./chrome.exe --no-sandbox --user-data-dir="./tmp/userdata/tt13" https://wpt.live/webrtc/RollbackEvents.https.html --enable-features=RemoveRedirectionBitmap

```

The only feature required to trigger this vulnerability is `--enable-features=RemoveRedirectionBitmap`

### pe...@google.com (2025-04-04)

Thank you for providing more feedback. Adding the requester to the CC list.

### zh...@gmail.com (2025-04-04)

```
win32-release_x64_asan-win32-release_x64-1442510 rm -rf ./tmp; ./chrome.exe --no-sandbox --user-data-dir="./tmp/userdata/tt13" https://wpt.live/webrtc/RollbackEvents.https.html --enable-features=RemoveRedirectionBitmap
[28068:10152:0405/020631.433:ERROR:google_apis\gcm\engine\registration_request.cc:291] Registration response error message: DEPRECATED_ENDPOINT
[28068:31868:0405/020634.198:ERROR:chrome\browser\policy\cloud\fm_registration_token_uploader.cc:179] Client is missing for kUser scope
[28068:31868:0405/020634.362:ERROR:chrome\browser\policy\cloud\fm_registration_token_uploader.cc:179] Client is missing for kUser scope
=================================================================
==28068==ERROR: AddressSanitizer: heap-use-after-free on address 0x12099d34b2f0 at pc 0x7ff837c1e6e5 bp 0x001ca33fb120 sp 0x001ca33fb168
READ of size 8 at 0x12099d34b2f0 thread T0
    #0 0x7ff837c1e6e4 in std::__Cr::vector<base::internal::CheckedObserverAdapter,std::__Cr::allocator<base::internal::CheckedObserverAdapter> >::end C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__vector\vector.h:353
    #1 0x7ff837c1e6e4 in std::__Cr::ranges::__end::__fn::operator() C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__ranges\access.h:132
    #2 0x7ff837c1e6e4 in std::__Cr::ranges::__find_if::operator() C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__algorithm\ranges_find_if.h:58
    #3 0x7ff837c1e6e4 in base::ObserverList<class views::WidgetObserver, 0, 1, class base::internal::CheckedObserverAdapter>::RemoveObserver(class views::WidgetObserver const *) C:\b\s\w\ir\cache\builder\src\base\observer_list.h:327:21
    #4 0x7ff83494380c in base::ScopedObservationTraits<views::Widget,views::WidgetObserver>::RemoveObserver C:\b\s\w\ir\cache\builder\src\base\scoped_observation_traits.h:74
    #5 0x7ff83494380c in base::ScopedObservation<views::Widget,views::WidgetObserver>::Reset C:\b\s\w\ir\cache\builder\src\base\scoped_observation.h:115
    #6 0x7ff83494380c in base::ScopedObservation<class views::Widget, class views::WidgetObserver>::~ScopedObservation<class views::Widget, class views::WidgetObserver>(void) C:\b\s\w\ir\cache\builder\src\base\scoped_observation.h:101:26
    #7 0x7ff837b3cf30 in views::DesktopWindowTreeHostWin::~DesktopWindowTreeHostWin(void) C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop_aura\desktop_window_tree_host_win.cc:145:1
    #8 0x7ff837b4d5d6 in [thunk]: views::DesktopWindowTreeHostWin::`vector deleting dtor'`adjustor{16}'(unsigned int) (D:\collection-chromium\win32-release_x64_asan-win32-release_x64-1442510\chrome.dll+0x1910ad5d6)
    #9 0x7ff837b51319 in std::__Cr::default_delete<aura::WindowTreeHost>::operator() C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:76
    #10 0x7ff837b51319 in std::__Cr::unique_ptr<aura::WindowTreeHost,std::__Cr::default_delete<aura::WindowTreeHost> >::reset C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:287
    #11 0x7ff837b51319 in views::DesktopNativeWidgetAura::OnHostClosed(void) C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop_aura\desktop_native_widget_aura.cc:381:9
    #12 0x7ff837bc63b2 in views::HWNDMessageHandler::OnWndProc(unsigned int, unsigned __int64, __int64) C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:1166:18
    #13 0x7ff83bb1006c in gfx::WindowImpl::WndProc(struct HWND__*, unsigned int, unsigned __int64, __int64) C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window_impl.cc:313:18
    #14 0x7ff83bb0eb8e in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc(struct HWND__*, unsigned int, unsigned __int64, __int64)>(struct HWND__*, unsigned int, unsigned __int64, __int64) C:\b\s\w\ir\cache\builder\src\base\win\wrapped_window_proc.h:74:10
    #15 0x7ff93332b642  (C:\WINDOWS\System32\USER32.dll+0x18000b642)
    #16 0x7ff93332ad1b  (C:\WINDOWS\System32\USER32.dll+0x18000ad1b)
    #17 0x7ff9333726ca  (C:\WINDOWS\System32\USER32.dll+0x1800526ca)
    #18 0x7ff93531ffe3  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18015ffe3)
    #19 0x7ff932c22533  (C:\WINDOWS\System32\win32u.dll+0x180002533)
    #20 0x7ff837be04df in base::internal::DecayedFunctorTraits<void (HWNDMessageHandler::*)(),base::WeakPtr<views::HWNDMessageHandler> &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:731
    #21 0x7ff837be04df in base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (HWNDMessageHandler::*&&)(),base::WeakPtr<views::HWNDMessageHandler> &&>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:947
    #22 0x7ff837be04df in base::internal::Invoker<base::internal::FunctorTraits<void (HWNDMessageHandler::*&&)(),base::WeakPtr<views::HWNDMessageHandler> &&>,base::internal::BindState<1,1,0,void (HWNDMessageHandler::*)(),base::WeakPtr<views::HWNDMessageHandler> >,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1060
    #23 0x7ff837be04df in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl views::HWNDMessageHandler::*&&)(void), class base::WeakPtr<class views::HWNDMessageHandler> &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl views::HWNDMessageHandler::*)(void), class base::WeakPtr<class views::HWNDMessageHandler>>, (void)>::RunOnce(class base::internal::BindStateBase *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:973:12
    #24 0x7ff839530d83 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
    #25 0x7ff839530d83 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:209:34
    #26 0x7ff839503db4 in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h:106
    #27 0x7ff839503db4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::LazyNow *) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:456:23
    #28 0x7ff839502c2f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:330:40
    #29 0x7ff8393a0b30 in base::MessagePumpForUI::DoRunLoop(void) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:262:67
    #30 0x7ff83939e2e8 in base::MessagePumpWin::Run(class base::MessagePump::Delegate *) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:89:3
    #31 0x7ff839505aa1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:629:12
    #32 0x7ff8395a057e in base::RunLoop::Run(class base::Location const &) C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134:14
    #33 0x7ff82ffe98dd in content::BrowserMainLoop::RunMainMessageLoop(void) C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1097:18
    #34 0x7ff82fff1449 in content::BrowserMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:156:15
    #35 0x7ff82ffe022c in content::BrowserMain(struct content::MainFunctionParams) C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:32:28
    #36 0x7ff8360977e4 in content::RunBrowserProcessMain(struct content::MainFunctionParams, class content::ContentMainDelegate *) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:718:10
    #37 0x7ff83609a790 in content::ContentMainRunnerImpl::RunBrowser(struct content::MainFunctionParams, bool) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1298:10
    #38 0x7ff836099fca in content::ContentMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1153:12
    #39 0x7ff83608e0c5 in content::RunContentProcess(struct content::ContentMainParams, class content::ContentMainRunner *) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:359:36
    #40 0x7ff83608ec6d in content::ContentMain(struct content::ContentMainParams) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:372:10
    #41 0x7ff826aa16b4 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:222:12
    #42 0x7ff67216472d in MainDllLoader::Launch(struct HINSTANCE__*, class base::TimeTicks) C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:201:12
    #43 0x7ff672161fda in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:352:20
    #44 0x7ff6727f51db in invoke_main D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:78
    #45 0x7ff6727f51db in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #46 0x7ff93311e8d6  (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #47 0x7ff9352714fb  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800b14fb)

0x12099d34b2f0 is located 240 bytes inside of 712-byte region [0x12099d34b200,0x12099d34b4c8)
freed by thread T0 here:
    #0 0x7ff8dcb2ae7d  (D:\collection-chromium\win32-release_x64_asan-win32-release_x64-1442510\clang_rt.asan_dynamic-x86_64.dll+0x18005ae7d)
    #1 0x7ff837b8c3f5 in views::Widget::operator delete C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.h:156
    #2 0x7ff837b8c3f5 in views::corewm::TooltipAura::TooltipWidget::`scalar deleting dtor'(unsigned int) C:\b\s\w\ir\cache\builder\src\ui\views\corewm\tooltip_aura.cc:108:37
    #3 0x7ff837b8b5c1 in std::__Cr::default_delete<views::corewm::TooltipAura::TooltipWidget>::operator() C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:76
    #4 0x7ff837b8b5c1 in std::__Cr::unique_ptr<views::corewm::TooltipAura::TooltipWidget,std::__Cr::default_delete<views::corewm::TooltipAura::TooltipWidget> >::reset C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:287
    #5 0x7ff837b8b5c1 in views::corewm::TooltipAura::DestroyWidget C:\b\s\w\ir\cache\builder\src\ui\views\corewm\tooltip_aura.cc:227
    #6 0x7ff837b8b5c1 in views::corewm::TooltipAura::Hide(void) C:\b\s\w\ir\cache\builder\src\ui\views\corewm\tooltip_aura.cc:309:5
    #7 0x7ff837b7e7b3 in views::corewm::TooltipStateManager::HideAndReset(void) C:\b\s\w\ir\cache\builder\src\ui\views\corewm\tooltip_state_manager.cc:54:13
    #8 0x7ff837b82821 in std::__Cr::unique_ptr<views::corewm::TooltipStateManager,std::__Cr::default_delete<views::corewm::TooltipStateManager> >::operator-> C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:267
    #9 0x7ff837b82821 in views::corewm::TooltipController::OnMouseEvent(class ui::MouseEvent *) C:\b\s\w\ir\cache\builder\src\ui\views\corewm\tooltip_controller.cc:313:7
    #10 0x7ff83bfb91c6 in ui::EventDispatcher::DispatchEvent(class ui::EventHandler *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:189:12
    #11 0x7ff83bfb8ba9 in ui::EventDispatcher::DispatchEventToEventHandlers(class std::__Cr::vector<class base::raw_ptr<class ui::EventHandler, 1>, class std::__Cr::allocator<class base::raw_ptr<class ui::EventHandler, 1>>> *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:176:7
    #12 0x7ff83bfb7bc2 in ui::EventDispatcher::ProcessEvent(class ui::EventTarget *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:124:3
    #13 0x7ff83bfb72cc in ui::EventDispatcherDelegate::DispatchEventToTarget(class ui::EventTarget *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:84:14
    #14 0x7ff83bfb6c5a in ui::EventDispatcherDelegate::DispatchEvent(class ui::EventTarget *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:56:15
    #15 0x7ff83bfb1ca4 in ui::EventProcessor::OnEventFromSource(class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_processor.cc:72:19
    #16 0x7ff83bfb0f10 in ui::EventSource::DeliverEventToSink(class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_source.cc:119:16
    #17 0x7ff83bfb07df in ui::EventSource::SendEventToSinkFromRewriter(class ui::Event const *, class ui::EventRewriter const *) C:\b\s\w\ir\cache\builder\src\ui\events\event_source.cc:134:12
    #18 0x7ff83bfb03cf in ui::EventSource::SendEventToSink(class ui::Event const *) C:\b\s\w\ir\cache\builder\src\ui\events\event_source.cc:113:10
    #19 0x7ff837b4aec4 in views::DesktopWindowTreeHostWin::HandleMouseEvent(class ui::MouseEvent *) C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop_aura\desktop_window_tree_host_win.cc:1215:3
    #20 0x7ff837bcd2e0 in views::HWNDMessageHandler::HandleMouseEventInternal(unsigned int, unsigned __int64, __int64, bool) C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:3342:26
    #21 0x7ff837bc69a6 in views::HWNDMessageHandler::OnMouseRange C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:2192
    #22 0x7ff837bc69a6 in views::HWNDMessageHandler::_ProcessWindowMessage(struct HWND__*, unsigned int, unsigned __int64, __int64, __int64 &, unsigned long) C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.h:395:5
    #23 0x7ff837bc60fd in views::HWNDMessageHandler::OnWndProc(unsigned int, unsigned __int64, __int64) C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:1147:7
    #24 0x7ff83bb1006c in gfx::WindowImpl::WndProc(struct HWND__*, unsigned int, unsigned __int64, __int64) C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window_impl.cc:313:18
    #25 0x7ff83bb0eb8e in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc(struct HWND__*, unsigned int, unsigned __int64, __int64)>(struct HWND__*, unsigned int, unsigned __int64, __int64) C:\b\s\w\ir\cache\builder\src\base\win\wrapped_window_proc.h:74:10
    #26 0x7ff93332b642  (C:\WINDOWS\System32\USER32.dll+0x18000b642)
    #27 0x7ff9333291cc  (C:\WINDOWS\System32\USER32.dll+0x1800091cc)
    #28 0x7ff8393a3677 in base::MessagePumpForUI::ProcessMessageHelper(struct tagMSG const &) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:630:3
    #29 0x7ff8393a14e2 in base::MessagePumpForUI::ProcessNextWindowsMessage(void) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:592:31
    #30 0x7ff8393a09d6 in base::MessagePumpForUI::DoRunLoop(void) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:252:33
    #31 0x7ff83939e2e8 in base::MessagePumpWin::Run(class base::MessagePump::Delegate *) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:89:3
    #32 0x7ff839505aa1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:629:12
    #33 0x7ff8395a057e in base::RunLoop::Run(class base::Location const &) C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134:14

previously allocated by thread T0 here:
    #0 0x7ff8dcb2a65d  (D:\collection-chromium\win32-release_x64_asan-win32-release_x64-1442510\clang_rt.asan_dynamic-x86_64.dll+0x18005a65d)
    #1 0x7ff837b8926f in views::Widget::operator new C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.h:156
    #2 0x7ff837b8926f in std::__Cr::make_unique C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:754
    #3 0x7ff837b8926f in views::corewm::TooltipAura::CreateTooltipWidget(class gfx::Rect const &, struct ui::OwnedWindowAnchor const &) C:\b\s\w\ir\cache\builder\src\ui\views\corewm\tooltip_aura.cc:198:13
    #4 0x7ff837b89eda in views::corewm::TooltipAura::Update(class aura::Window *, class std::__Cr::basic_string<char16_t, struct std::__Cr::char_traits<char16_t>, class std::__Cr::allocator<char16_t>> const &, class gfx::Point const &, enum views::corewm::TooltipTrigger) C:\b\s\w\ir\cache\builder\src\ui\views\corewm\tooltip_aura.cc:261:3
    #5 0x7ff837b7f6e3 in views::corewm::TooltipStateManager::ShowNow(class std::__Cr::basic_string<char16_t, struct std::__Cr::char_traits<char16_t>, class std::__Cr::allocator<char16_t>> const &, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\ui\views\corewm\tooltip_state_manager.cc:121:13
    #6 0x7ff837b7fb88 in base::internal::DecayedFunctorTraits<void (TooltipStateManager::*)(const std::__Cr::basic_string<char16_t,std::__Cr::char_traits<char16_t>,std::__Cr::allocator<char16_t> > &, base::TimeDelta),base::WeakPtr<views::corewm::TooltipStateManager> &&,std::__Cr::basic_string<char16_t,std::__Cr::char_traits<char16_t>,std::__Cr::allocator<char16_t> > &&,base::TimeDelta &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:731
    #7 0x7ff837b7fb88 in base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (TooltipStateManager::*&&)(const std::__Cr::basic_string<char16_t,std::__Cr::char_traits<char16_t>,std::__Cr::allocator<char16_t> > &, base::TimeDelta),base::WeakPtr<views::corewm::TooltipStateManager> &&,std::__Cr::basic_string<char16_t,std::__Cr::char_traits<char16_t>,std::__Cr::allocator<char16_t> > &&,base::TimeDelta &&>,void,0,1,2>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:947
    #8 0x7ff837b7fb88 in base::internal::Invoker<base::internal::FunctorTraits<void (TooltipStateManager::*&&)(const std::__Cr::basic_string<char16_t,std::__Cr::char_traits<char16_t>,std::__Cr::allocator<char16_t> > &, base::TimeDelta),base::WeakPtr<views::corewm::TooltipStateManager> &&,std::__Cr::basic_string<char16_t,std::__Cr::char_traits<char16_t>,std::__Cr::allocator<char16_t> > &&,base::TimeDelta &&>,base::internal::BindState<1,1,0,void (TooltipStateManager::*)(const std::__Cr::basic_string<char16_t,std::__Cr::char_traits<char16_t>,std::__Cr::allocator<char16_t> > &, base::TimeDelta),base::WeakPtr<views::corewm::TooltipStateManager>,std::__Cr::basic_string<char16_t,std::__Cr::char_traits<char16_t>,std::__Cr::allocator<char16_t> >,base::TimeDelta>,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1060
    #9 0x7ff837b7fb88 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl views::corewm::TooltipStateManager::*&&)(class std::__Cr::basic_string<char16_t, struct std::__Cr::char_traits<char16_t>, class std::__Cr::allocator<char16_t>> const &, class base::TimeDelta), class base::WeakPtr<class views::corewm::TooltipStateManager> &&, class std::__Cr::basic_string<char16_t, struct std::__Cr::char_traits<char16_t>, class std::__Cr::allocator<char16_t>> &&, class base::TimeDelta &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl views::corewm::TooltipStateManager::*)(class std::__Cr::basic_string<char16_t, struct std::__Cr::char_traits<char16_t>, class std::__Cr::allocator<char16_t>> const &, class base::TimeDelta), class base::WeakPtr<class views::corewm::TooltipStateManager>, class std::__Cr::basic_string<char16_t, struct std::__Cr::char_traits<char16_t>, class std::__Cr::allocator<char16_t>>, class base::TimeDelta>, (void)>::RunOnce(class base::internal::BindStateBase *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:973:12
    #10 0x7ff83942d4e2 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
    #11 0x7ff83942d4e2 in base::OneShotTimer::RunUserTask(void) C:\b\s\w\ir\cache\builder\src\base\timer\timer.cc:176:19
    #12 0x7ff8394306f5 in base::internal::DecayedFunctorTraits<void (DelayTimerBase::*)(),base::internal::DelayTimerBase *>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:731
    #13 0x7ff8394306f5 in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (DelayTimerBase::*const &)(),base::internal::DelayTimerBase *>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:923
    #14 0x7ff8394306f5 in base::internal::Invoker<base::internal::FunctorTraits<void (DelayTimerBase::*const &)(),base::internal::DelayTimerBase *>,base::internal::BindState<1,1,0,void (DelayTimerBase::*)(),base::internal::UnretainedWrapper<base::internal::DelayTimerBase,base::unretained_traits::MayNotDangle,0> >,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1060
    #15 0x7ff8394306f5 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl base::internal::DelayTimerBase::*const &)(void), class base::internal::DelayTimerBase *>, struct base::internal::BindState<1, 1, 0, void (__cdecl base::internal::DelayTimerBase::*)(void), class base::internal::UnretainedWrapper<class base::internal::DelayTimerBase, struct base::unretained_traits::MayNotDangle, 0>>, (void)>::Run(class base::internal::BindStateBase *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980:12
    #16 0x7ff839530d83 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
    #17 0x7ff839530d83 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:209:34
    #18 0x7ff839503db4 in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h:106
    #19 0x7ff839503db4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::LazyNow *) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:456:23
    #20 0x7ff839502c2f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:330:40
    #21 0x7ff8393a0b30 in base::MessagePumpForUI::DoRunLoop(void) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:262:67
    #22 0x7ff83939e2e8 in base::MessagePumpWin::Run(class base::MessagePump::Delegate *) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:89:3
    #23 0x7ff839505aa1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:629:12
    #24 0x7ff8395a057e in base::RunLoop::Run(class base::Location const &) C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134:14
    #25 0x7ff82ffe98dd in content::BrowserMainLoop::RunMainMessageLoop(void) C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1097:18
    #26 0x7ff82fff1449 in content::BrowserMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:156:15
    #27 0x7ff82ffe022c in content::BrowserMain(struct content::MainFunctionParams) C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:32:28
    #28 0x7ff8360977e4 in content::RunBrowserProcessMain(struct content::MainFunctionParams, class content::ContentMainDelegate *) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:718:10
    #29 0x7ff83609a790 in content::ContentMainRunnerImpl::RunBrowser(struct content::MainFunctionParams, bool) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1298:10
    #30 0x7ff836099fca in content::ContentMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1153:12
    #31 0x7ff83608e0c5 in content::RunContentProcess(struct content::ContentMainParams, class content::ContentMainRunner *) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:359:36
    #32 0x7ff83608ec6d in content::ContentMain(struct content::ContentMainParams) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:372:10
    #33 0x7ff826aa16b4 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:222:12
    #34 0x7ff67216472d in MainDllLoader::Launch(struct HINSTANCE__*, class base::TimeTicks) C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:201:12
    #35 0x7ff672161fda in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:352:20
    #36 0x7ff6727f51db in invoke_main D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:78
    #37 0x7ff6727f51db in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #38 0x7ff93311e8d6  (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #39 0x7ff9352714fb  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800b14fb)

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__vector\vector.h:353 in std::__Cr::vector<base::internal::CheckedObserverAdapter,std::__Cr::allocator<base::internal::CheckedObserverAdapter> >::end
Shadow bytes around the buggy address:
  0x12099d34b000: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x12099d34b080: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x12099d34b100: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x12099d34b180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x12099d34b200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x12099d34b280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd[fd]fd
  0x12099d34b300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x12099d34b380: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x12099d34b400: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x12099d34b480: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa
  0x12099d34b500: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
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

==28068==ADDITIONAL INFO

==28068==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ff837bbee60 in views::HWNDMessageHandler::Close(void) C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:516:9


Command line: `"D:\collection-chromium\win32-release_x64_asan-win32-release_x64-1442510\chrome.exe" --no-sandbox --user-data-dir=./tmp/userdata/tt13 --enable-features=RemoveRedirectionBitmap --flag-switches-begin --flag-switches-end --file-url-path-alias="/gen=D:\collection-chromium\win32-release_x64_asan-win32-release_x64-1442510\gen" https://wpt.live/webrtc/RollbackEvents.https.html`


MiraclePtr Status: MANUAL ANALYSIS REQUIRED
A pointer to the same region was extracted from a raw_ptr<T> object prior to this crash.
To determine the protection status, enable extraction warnings and check whether the raw_ptr<T> object can be destroyed or overwritten between the extraction and use.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==28068==END OF ADDITIONAL INFO
==28068==ABORTING


```

### pe...@google.com (2025-04-05)

The NextAction date has arrived: 2025-04-05
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### dr...@chromium.org (2025-04-07)

[security triage] I was not able to reproduce this in 135.0.7049.42 or 137.0.7114.0, which is beyond your suggested commit. But it looks like kerenzhu@ already has a fix ready. kerenzhu@ - were you able to reproduce this? Do you have a sense of when it was introduced?

### ke...@chromium.org (2025-04-07)

No, I couldn't reproduce. However, I do think that the current code has a UaF risk. The pending CL will eliminate the risk.

### dx...@google.com (2025-04-07)

Project: chromium/src  

Branch: main  

Author: Keren Zhu [kerenzhu@chromium.org](mailto:kerenzhu@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6433952>

Don't observe Widget in DesktopWindowTreeHostWin

---


Expand for full commit details
```
     
    DesktopWindowTreeHostWin uses a ScopedObservation to observe Widget, but 
    the Widget can be destroyed before DWTH. Later when ScopedObservation is 
    destroyed, ~ScopedObservation calls Widget::RemoveObserver and UaF 
    happens. 
     
    This CL fixes the issue by not observing Widget in DWTHW. The plumbing 
    is move into the Widget => NativeWidgetPrivate => DesktopWindowTreeHost 
    layers. 
     
    Fix: 408132930 
    Change-Id: Ifdc94785e170cc38dbed5c7b9ca106bf226e6f26 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6433952 
    Reviewed-by: Dana Fried <dfried@chromium.org> 
    Commit-Queue: Keren Zhu <kerenzhu@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1443804}

```

---

Files:

- M `ui/views/test/mock_native_widget.h`
- M `ui/views/widget/desktop_aura/desktop_native_widget_aura.cc`
- M `ui/views/widget/desktop_aura/desktop_native_widget_aura.h`
- M `ui/views/widget/desktop_aura/desktop_window_tree_host.h`
- M `ui/views/widget/desktop_aura/desktop_window_tree_host_platform.cc`
- M `ui/views/widget/desktop_aura/desktop_window_tree_host_platform.h`
- M `ui/views/widget/desktop_aura/desktop_window_tree_host_win.cc`
- M `ui/views/widget/desktop_aura/desktop_window_tree_host_win.h`
- M `ui/views/widget/native_widget_aura.cc`
- M `ui/views/widget/native_widget_aura.h`
- M `ui/views/widget/native_widget_mac.h`
- M `ui/views/widget/native_widget_mac.mm`
- M `ui/views/widget/native_widget_private.h`
- M `ui/views/widget/widget.cc`

---

Hash: 2eab5089118e2fd88ed880ff6ea60912711eaa25  

Date:  Mon Apr 7 22:21:49 2025


---

### ch...@google.com (2025-04-07)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches (as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact ([security@chromium.org](mailto:security@chromium.org)) to arrange to set these labels. Severity guidelines: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues> FoundIn guidelines: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security>
  After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2025-04-08)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### am...@chromium.org (2025-04-10)

marking as SI-None based on requirement for --enable-features=RemoveRedirectionBitmap

### sp...@google.com (2025-04-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
moderately mitigated memory corruption in a non-sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-04-18)

Congratulations! We consider this issue to be moderately mitigated based on the non-standard user gesture required to trigger this issue. Thank you for your efforts and reporting this issue to us!

### zh...@gmail.com (2025-04-19)

Thank you very much Amy, Cheers🍻

### ch...@google.com (2025-07-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> moderately mitigated memory corruption in a non-sandboxed process

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/408132930)*
