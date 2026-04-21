# Security:UAF in content::SyntheticPointerAction::ForwardTouchOrMouseInputEvents(browser process)

| Field | Value |
|-------|-------|
| **Issue ID** | [40062021](https://issues.chromium.org/issues/40062021) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Input |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | bo...@chromium.org |
| **Created** | 2022-12-02 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**  

UAF in content::SyntheticPointerAction::ForwardTouchOrMouseInputEvents in the browser process.

**VERSION**  

Chromium 110.0.5454.0 (Developer Build) (64-bit)  

Revision cc61387c480b9e654aa416d63e422ee20fd0b903-refs/heads/main@{#1078520}  

OS Windows 10 Version 22H2 (Build 19045.2251)

**REPRODUCTION CASE**  

This issue can reproduce in Windows/Linxu/ChromiumOS-Linux stably.

1. run `python -m http.server 8000` in any directory.
2. unzip the file to extension\_path and run:  
   
   chrome.exe --user-data-dir=C:/any --remote-debugging-port=9222 --enable-features=SyntheticPointerActions --load-extension="extension\_path"

The UAF will be triggered stably.

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: [browser]

==22888==ERROR: AddressSanitizer: heap-use-after-free on address 0x12ad89308a80 at pc 0x7ff8bfb32a49 bp 0x0088107fe660 sp 0x0088107fe6a8  

READ of size 1 at 0x12ad89308a80 thread T0  

==22888==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ff8bfb32a48 in base::internal::`anonymous namespace'::CrashImmediatelyOnUseAfterFree C:\b\s\w\ir\cache\builder\src\base\memory\raw_ptr.cc:162 #1 0x7ff8bfb326ab in base::internal::AsanBackupRefPtrImpl::AsanCheckIfValidDereference C:\b\s\w\ir\cache\builder\src\base\memory\raw_ptr.cc:174 #2 0x7ff8baf68a1e in content::SyntheticPointerAction::ForwardTouchOrMouseInputEvents C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\input\synthetic_pointer_action.cc:76 #3 0x7ff8baf68611 in content::SyntheticPointerAction::ForwardInputEvents C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\input\synthetic_pointer_action.cc:44 #4 0x7ff8baf5e783 in content::SyntheticGestureController::DispatchNextEvent C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\input\synthetic_gesture_controller.cc:113 #5 0x7ff8baf61f24 in base::internal::Invoker<base::internal::BindState<`lambda at ../../content/browser/renderer\_host/input/synthetic\_gesture\_controller.cc:98:11',base::WeakPtr[content::SyntheticGestureController](javascript:void(0);) >,void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:908  

#6 0x7ff8bfc8a337 in base::MetronomeTimer::OnScheduledTaskInvoked C:\b\s\w\ir\cache\builder\src\base\timer\timer.cc:477  

#7 0x7ff8bfc8ac5e in base::internal::Invoker<base::internal::BindState<void (base::MetronomeTimer::\*)(),base::internal::UnretainedWrapper[base::MetronomeTimer,base::RawPtrBanDanglingIfSupported](javascript:void(0);) >,void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:908  

#8 0x7ff8bfc298d9 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:156  

#9 0x7ff8c2d6e4f1 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:450  

#10 0x7ff8c2d6cfe2 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:301  

#11 0x7ff8bfcdb772 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:214  

#12 0x7ff8bfcd98f0 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#13 0x7ff8c2d70923 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:610  

#14 0x7ff8bfbb8f8e in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#15 0x7ff8ba42e445 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1050  

#16 0x7ff8ba434cdf in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:162  

#17 0x7ff8ba427179 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:32  

#18 0x7ff8bf775145 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:693  

#19 0x7ff8bf77893d in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1231  

#20 0x7ff8bf7780ae in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1087  

#21 0x7ff8bf7731ce in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:344  

#22 0x7ff8bf774029 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:372  

#23 0x7ff8b31014a5 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:174  

#24 0x7ff7cfd96288 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:166  

#25 0x7ff7cfd92c0a in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:391  

#26 0x7ff7d01c2c6b in \_\_scrt\_common\_main\_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#27 0x7ff9928a74b3 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x1800174b3)  

#28 0x7ff9941026a0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526a0)

0x12ad89308a80 is located 0 bytes inside of 1320-byte region [0x12ad89308a80,0x12ad89308fa8)  

freed by thread T0 here:  

#0 0x7ff7cfe4407d in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ff8baf7130c in content::SyntheticTouchDriver::~SyntheticTouchDriver C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\input\synthetic\_touch\_driver.cc:17  

#2 0x7ff8ba677f2b in content::protocol::InputHandler::~InputHandler C:\b\s\w\ir\cache\builder\src\content\browser\devtools\protocol\input\_handler.cc:539  

#3 0x7ff8ba6969cb in content::protocol::InputHandler::~InputHandler C:\b\s\w\ir\cache\builder\src\content\browser\devtools\protocol\input\_handler.cc:539  

#4 0x7ff8b3ebbc70 in std::Cr::\_\_destroy\_at<std::Cr::pair<const std::Cr::basic\_string<char,std::Cr::char\_traits<char>,std::Cr::allocator<char> >,std::Cr::unique\_ptr<const webrtc::RTCStats,std::Cr::default\_delete<const webrtc::RTCStats> > >,0> C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_memory\construct\_at.h:64  

#5 0x7ff8ba6012e1 in std::Cr::vector<std::Cr::pair<std::Cr::basic\_string<char,std::Cr::char\_traits<char>,std::Cr::allocator<char> >,std::Cr::unique\_ptr<content::protocol::DevToolsDomainHandler,std::Cr::default\_delete[content::protocol::DevToolsDomainHandler](javascript:void(0);) > >,std::Cr::allocator<std::Cr::pair<std::Cr::basic\_string<char,std::Cr::char\_traits<char>,std::Cr::allocator<char> >,std::Cr::unique\_ptr<content::protocol::DevToolsDomainHandler,std::Cr::default\_delete[content::protocol::DevToolsDomainHandler](javascript:void(0);) > > > >::clear C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\vector:624  

#6 0x7ff8ba5f6c31 in content::DevToolsSession::Dispose C:\b\s\w\ir\cache\builder\src\content\browser\devtools\devtools\_session.cc:151  

#7 0x7ff8ba5ace62 in content::DevToolsAgentHostImpl::DetachInternal C:\b\s\w\ir\cache\builder\src\content\browser\devtools\devtools\_agent\_host\_impl.cc:259  

#8 0x7ff8ba5acbfe in content::DevToolsAgentHostImpl::DetachClient C:\b\s\w\ir\cache\builder\src\content\browser\devtools\devtools\_agent\_host\_impl.cc:242  

#9 0x7ff8ba5d1079 in content::DevToolsAgentHostClientImpl::~DevToolsAgentHostClientImpl C:\b\s\w\ir\cache\builder\src\content\browser\devtools\devtools\_http\_handler.cc:343  

#10 0x7ff8ba5d06c5 in content::DevToolsAgentHostClientImpl::~DevToolsAgentHostClientImpl C:\b\s\w\ir\cache\builder\src\content\browser\devtools\devtools\_http\_handler.cc:340  

#11 0x7ff8ba5d1d47 in std::Cr::\_\_tree<std::Cr::\_\_value\_type<int,std::Cr::unique\_ptr<content::DevToolsAgentHostClientImpl,std::Cr::default\_delete[content::DevToolsAgentHostClientImpl](javascript:void(0);) > >,std::Cr::\_\_map\_value\_compare<int,std::Cr::\_\_value\_type<int,std::Cr::unique\_ptr<content::DevToolsAgentHostClientImpl,std::Cr::default\_delete[content::DevToolsAgentHostClientImpl](javascript:void(0);) > >,std::Cr::less<int>,1>,std::Cr::allocator<std::Cr::\_\_value\_type<int,std::Cr::unique\_ptr<content::DevToolsAgentHostClientImpl,std::Cr::default\_delete[content::DevToolsAgentHostClientImpl](javascript:void(0);) > > > >::\_\_erase\_unique<int> C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_tree:2445  

#12 0x7ff8ba5c62b4 in content::DevToolsHttpHandler::OnClose C:\b\s\w\ir\cache\builder\src\content\browser\devtools\devtools\_http\_handler.cc:809  

#13 0x7ff8ba5cf47b in base::internal::Invoker<base::internal::BindState<void (content::DevToolsHttpHandler::\*)(int),base::WeakPtr[content::DevToolsHttpHandler](javascript:void(0);),int>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:895  

#14 0x7ff8bfc298d9 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:156  

#15 0x7ff8c2d6e4f1 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:450  

#16 0x7ff8c2d6cfe2 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:301  

#17 0x7ff8bfcdb772 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:214  

#18 0x7ff8bfcd98f0 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#19 0x7ff8c2d70923 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:610  

#20 0x7ff8bfbb8f8e in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#21 0x7ff8ba42e445 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1050  

#22 0x7ff8ba434cdf in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:162  

#23 0x7ff8ba427179 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:32  

#24 0x7ff8bf775145 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:693  

#25 0x7ff8bf77893d in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1231  

#26 0x7ff8bf7780ae in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1087  

#27 0x7ff8bf7731ce in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:344

previously allocated by thread T0 here:  

#0 0x7ff7cfe4417d in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ff8d43384de in operator new d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ff8baf69abd in content::SyntheticPointerDriver::Create C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\input\synthetic\_pointer\_driver.cc:21  

#3 0x7ff8baf69b38 in content::SyntheticPointerDriver::Create C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\input\synthetic\_pointer\_driver.cc:37  

#4 0x7ff8ba688731 in content::protocol::InputHandler::DispatchSyntheticPointerActionTouch C:\b\s\w\ir\cache\builder\src\content\browser\devtools\protocol\input\_handler.cc:1382  

#5 0x7ff8ba686832 in content::protocol::InputHandler::DispatchTouchEvent C:\b\s\w\ir\cache\builder\src\content\browser\devtools\protocol\input\_handler.cc:1061  

#6 0x7ff8ba0e1b87 in content::protocol::Input::DomainDispatcherImpl::dispatchTouchEvent C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\content\browser\devtools\protocol\input.cc:658  

#7 0x7ff8b94775e9 in v8\_crdtp::UberDispatcher::DispatchResult::Run C:\b\s\w\ir\cache\builder\src\v8\third\_party\inspector\_protocol\crdtp\dispatch.cc:511  

#8 0x7ff8ba5fb720 in content::DevToolsSession::HandleCommandInternal C:\b\s\w\ir\cache\builder\src\content\browser\devtools\devtools\_session.cc:369  

#9 0x7ff8ba5fb4f5 in content::DevToolsSession::HandleCommand C:\b\s\w\ir\cache\builder\src\content\browser\devtools\devtools\_session.cc:355  

#10 0x7ff8ba604d48 in base::internal::Invoker<base::internal::BindState<void (content::DevToolsSession::\*)(base::span<const unsigned char,18446744073709551615>),base::WeakPtr[content::DevToolsSession](javascript:void(0);) >,void (base::span<const unsigned char,18446744073709551615>)>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:895  

#11 0x7ff8c63650bc in ChromeDevToolsSession::HandleCommand C:\b\s\w\ir\cache\builder\src\chrome\browser\devtools\chrome\_devtools\_session.cc:109  

#12 0x7ff8c2b1a1f6 in ChromeDevToolsManagerDelegate::HandleCommand C:\b\s\w\ir\cache\builder\src\chrome\browser\devtools\chrome\_devtools\_manager\_delegate.cc:141  

#13 0x7ff8ba5faeb0 in content::DevToolsSession::DispatchProtocolMessageInternal C:\b\s\w\ir\cache\builder\src\content\browser\devtools\devtools\_session.cc:346  

#14 0x7ff8ba5fa317 in content::DevToolsSession::DispatchProtocolMessage C:\b\s\w\ir\cache\builder\src\content\browser\devtools\devtools\_session.cc:314  

#15 0x7ff8ba5ad30f in content::DevToolsAgentHostImpl::DispatchProtocolMessage C:\b\s\w\ir\cache\builder\src\content\browser\devtools\devtools\_agent\_host\_impl.cc:251  

#16 0x7ff8ba5c5d6e in content::DevToolsHttpHandler::OnWebSocketMessage C:\b\s\w\ir\cache\builder\src\content\browser\devtools\devtools\_http\_handler.cc:804  

#17 0x7ff8ba5cf915 in base::internal::Invoker<base::internal::BindState<void (content::DevToolsHttpHandler::\*)(int, std::Cr::basic\_string<char,std::Cr::char\_traits<char>,std::Cr::allocator<char> >),base::WeakPtr[content::DevToolsHttpHandler](javascript:void(0);),int,std::Cr::basic\_string<char,std::Cr::char\_traits<char>,std::Cr::allocator<char> > >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:895  

#18 0x7ff8bfc298d9 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:156  

#19 0x7ff8c2d6e4f1 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:450  

#20 0x7ff8c2d6cfe2 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:301  

#21 0x7ff8bfcdb772 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:214  

#22 0x7ff8bfcd98f0 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#23 0x7ff8c2d70923 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:610  

#24 0x7ff8bfbb8f8e in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#25 0x7ff8ba42e445 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1050  

#26 0x7ff8ba434cdf in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:162  

#27 0x7ff8ba427179 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:32

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\base\memory\raw\_ptr.cc:162 in base::internal::`anonymous namespace'::CrashImmediatelyOnUseAfterFree  

Shadow bytes around the buggy address:  

0x12ad89308800: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x12ad89308880: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x12ad89308900: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa  

0x12ad89308980: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x12ad89308a00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa  

=>0x12ad89308a80:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x12ad89308b00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x12ad89308b80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x12ad89308c00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x12ad89308c80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x12ad89308d00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

MiraclePtr Status: PROTECTED  

This crash occurred while a raw\_ptr<T> object containing a dangling pointer was being dereferenced.  

MiraclePtr is expected to make this crash non-exploitable once fully enabled.  

Refer to <https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md> for details.  

==22888==ABORTING

## Attachments

- [extension.zip](attachments/extension.zip) (application/octet-stream, 1.9 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 306 B)
- [background.js](attachments/background.js) (text/plain, 68 B)
- [script.js](attachments/script.js) (text/plain, 653 B)
- [injection.js](attachments/injection.js) (text/plain, 1.4 KB)
- [index.html](attachments/index.html) (text/plain, 74 B)

## Timeline

### 0x...@gmail.com (2022-12-02)

unzip 

### [Deleted User] (2022-12-02)

[Empty comment from Monorail migration]

### ca...@chromium.org (2022-12-02)

Thanks for the report. I can repro in M109 and M110, but not M108. I'm triageing this as high since it's in the browser process, but mitigated by requiring an extension to be installed. This is also SecurityImpact_None since it requires the SyntheticPointerActions flag to be enabled, and it's currently off by default.

bokan: Can you help further triage this and reassign as appropriate? Thanks

[Monorail components: Blink>Input]

### bo...@chromium.org (2022-12-07)

Hmm, I can see the issue - InputHandler sets a raw pointer on the SyntheticGesture back to synthetic_pointer_driver_. The gesture is held on the RWH's SyntheticGestureController which isn't deleted if the InputHandler is disconnected and disposed so this pointer is used when the gesture dispatches. However, I don't see any of this having changed recently. 

I'm having a hard time reproducing this from a build. I'm using Linux and sync'd at r1078520.

My gn args:
dcheck_always_on = true
is_asan = true
is_component_build = false
is_debug = false
symbol_level = 1
use_goma = true

I downloaded the files in #1 to ~/temp.

I start `python -m http.server 8000` in ~/temp (though, does this do anything?)

Then I run: ./out/ChromeAsan/chrome --user-data-dir=/tmp/alsiefjsleiva --remote-debugging-port=9222 --enable-features=SyntheticPointerActions --load-extension=~/temp

I see the UAF POC window and I hit unrelated DCHECKs in LocalWindowProxy::DisposeContext: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/bindings/core/v8/local_window_proxy.cc;l=94;drc=04c75e2eb647dea7b4ab707a32c9fef3828bcc17

If I disable DCHECKs I don't see any crashes.

Did I miss anything?


### an...@chromium.org (2022-12-15)

[security marshal] I tried reproducing the issue with the latest canary build (110.0.5479.0) on Windows 10 but did not get Chrome to crash. I did not launch the local http server in the same directory as the extension and just served a dummy file from another folder instead. 

carlosil@, 0xasnine@gmail.com: Same question as that from bokan@ in https://crbug.com/chromium/1395354#c4. Did we miss anything?

### 0x...@gmail.com (2022-12-21)


Sorry for the wrong poc.
Just change the content
url_list = ['about:blank']  >>  
url_list = ['http://localhost:8000']
in the script.js file
It can be triggered in the latest asan build 1085772.




### bo...@chromium.org (2023-01-03)

Thanks, reproduced!

### bo...@chromium.org (2023-01-03)

Fix is up for review: https://chromium-review.googlesource.com/c/chromium/src/+/4134565

### bo...@chromium.org (2023-01-03)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-01-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c965ac9f24e3a589fe4007bd441d493a8e4bf9b4

commit c965ac9f24e3a589fe4007bd441d493a8e4bf9b4
Author: David Bokan <bokan@chromium.org>
Date: Wed Jan 04 19:59:29 2023

Fix UAF in SyntheticPointerAction

SyntheticPointerAction supports providing an external pointer driver for
use with DevTools' InputHandler so that state can be kept across
gestures.

This code currently assumes InputHandler will outlive the
SyntheticPointerAction so the driver is kept as a raw pointer. However,
InputHandler can go away without the action being cleared. In this case,
we'll use a WeakPtr to clear the driver from the action and end the
gesture.

Bug: 1395354
Change-Id: I93337ea04df1d426ce4942f11cb23bdf6aad3e24
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4134565
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Commit-Queue: David Bokan <bokan@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1088894}

[modify] https://crrev.com/c965ac9f24e3a589fe4007bd441d493a8e4bf9b4/content/browser/renderer_host/input/synthetic_pointer_action_unittest.cc
[modify] https://crrev.com/c965ac9f24e3a589fe4007bd441d493a8e4bf9b4/content/browser/renderer_host/input/synthetic_pointer_action.h
[modify] https://crrev.com/c965ac9f24e3a589fe4007bd441d493a8e4bf9b4/content/browser/devtools/protocol/input_handler.cc
[modify] https://crrev.com/c965ac9f24e3a589fe4007bd441d493a8e4bf9b4/content/browser/renderer_host/input/synthetic_pointer_action.cc
[modify] https://crrev.com/c965ac9f24e3a589fe4007bd441d493a8e4bf9b4/content/browser/renderer_host/input/synthetic_pointer_driver.h


### bo...@chromium.org (2023-01-04)

This should be fixed, PLMK if you still see it or something related. And thanks for the report!

### [Deleted User] (2023-01-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-05)

[Empty comment from Monorail migration]

### ts...@chromium.org (2023-01-12)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-18)

Congratulations, asnine! The VRP Panel has decided to award you $7,000 for this report of a mildly mitigated security bug. Thank you for your efforts in discovering and reporting this issue to us -- nice work! 

### am...@google.com (2023-01-23)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-04-13)

This issue was migrated from crbug.com/chromium/1395354?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062021)*
