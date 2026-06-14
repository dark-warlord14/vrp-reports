# Security: Browser_crash - heap-use-after-free in extensions::ChromeExtensionsBrowserClient::GetOriginalContext(content::BrowserContext*) 

| Field | Value |
|-------|-------|
| **Issue ID** | [40052285](https://issues.chromium.org/issues/40052285) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Speech, Platform>Extensions>API |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2020-05-11 |
| **Bounty** | $15,000.00 |

## Description

**VERSION**  

Chrome Version: 84.0.4143.0 Canary and 81.0.4044.138 stable  

Operating System: all

**REPRODUCTION CASE**  

This is similar to <https://crbug.com/chromium/402957> which is fixed M40.

1. Open the testcase and click on the button
2. Open again the testcase on an incognito tab and click on the button then close
3. Wait => Crash!

==2176==ERROR: AddressSanitizer: heap-use-after-free on address 0x61100094ab00 at pc 0x55557046c2e7 bp 0x7fffffffcc40 sp 0x7fffffffcc38  

READ of size 8 at 0x61100094ab00 thread T0 (chrome)  

[Detaching after fork from child process 2494]  

#0 0x55557046c2e6 in extensions::ChromeExtensionsBrowserClient::GetOriginalContext(content::BrowserContext\*) chrome/browser/extensions/chrome\_extensions\_browser\_client.cc:149:42  

#1 0x55556c818a74 in KeyedServiceFactory::GetServiceForContext(void\*, bool) components/keyed\_service/core/keyed\_service\_factory.cc:56:13  

#2 0x555568ca20bb in TtsExtensionEngine::GetVoices(content::BrowserContext\*, std::\_\_1::vector<content::VoiceData, std::\_\_1::allocator[content::VoiceData](javascript:void(0);) >\*) chrome/browser/speech/extension\_api/tts\_engine\_extension\_api.cc:171:31  

#3 0x555562ec9b78 in content::TtsControllerImpl::SpeakNow(std::\_\_1::unique\_ptr<content::TtsUtterance, std::\_\_1::default\_delete[content::TtsUtterance](javascript:void(0);) >) content/browser/speech/tts\_controller\_impl.cc:342:3  

#4 0x555562ecd0a5 in content::TtsControllerImpl::SpeakNextUtterance() content/browser/speech/tts\_controller\_impl.cc:462:5  

#5 0x555562ecd5df in content::TtsControllerImpl::OnTtsEvent(int, content::TtsEventType, int, int, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) content/browser/speech/tts\_controller\_impl.cc:229:5  

#6 0x55556311dcac in content::TtsPlatformImplLinux::OnSpeechEvent(SPDNotificationType) content/browser/speech/tts\_linux.cc:321:19  

#7 0x555569016e2d in Run base/callback.h:99:12  

#8 0x555569016e2d in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/task/common/task\_annotator.cc:142:33  

#9 0x55556904f03f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:329:23  

#10 0x55556904e9ac in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:254:36  

#11 0x555568f55649 in HandleDispatch base/message\_loop/message\_pump\_glib.cc:409:46  

#12 0x555568f55649 in base::(anonymous namespace)::WorkSourceDispatch(\_GSource\*, int (\*)(void\*), void\*) base/message\_loop/message\_pump\_glib.cc:122:43  

#13 0x7ffff7e42fbc in g\_main\_context\_dispatch (/lib/x86\_64-linux-gnu/libglib-2.0.so.0+0x51fbc)

0x61100094ab00 is located 0 bytes inside of 256-byte region [0x61100094ab00,0x61100094ac00)  

freed by thread T0 (chrome) here:  

#0 0x55555e91745d in operator delete(void\*) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:160:3  

#1 0x55556869480b in operator() buildtools/third\_party/libc++/trunk/include/memory:2378:5  

#2 0x55556869480b in reset buildtools/third\_party/libc++/trunk/include/memory:2633:7  

#3 0x55556869480b in ~unique\_ptr buildtools/third\_party/libc++/trunk/include/memory:2587:19  

#4 0x55556869480b in ~pair buildtools/third\_party/libc++/trunk/include/utility:297:29  

#5 0x55556869480b in \_\_destroy<std::\_\_1::pair<const Profile::OTRProfileID, std::\_\_1::unique\_ptr<Profile, std::\_\_1::default\_delete<Profile>>>> buildtools/third\_party/libc++/trunk/include/memory:1787:23  

#6 0x55556869480b in destroy<std::\_\_1::pair<const Profile::OTRProfileID, std::\_\_1::unique\_ptr<Profile, std::\_\_1::default\_delete<Profile>>>> buildtools/third\_party/libc++/trunk/include/memory:1619:14  

#7 0x55556869480b in std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<Profile::OTRProfileID, std::\_\_1::unique\_ptr<Profile, std::\_\_1::default\_delete<Profile> > >, std::\_\_1::\_\_map\_value\_compare<Profile::OTRProfileID, std::\_\_1::\_\_value\_type<Profile::OTRProfileID, std::\_\_1::unique\_ptr<Profile, std::\_\_1::default\_delete<Profile> > >, std::\_\_1::less[Profile::OTRProfileID](javascript:void(0);), true>, std::\_\_1::allocator<std::\_\_1::\_\_value\_type<Profile::OTRProfileID, std::\_\_1::unique\_ptr<Profile, std::\_\_1::default\_delete<Profile> > > > >::erase(std::\_\_1::\_\_tree\_const\_iterator<std::\_\_1::\_\_value\_type<Profile::OTRProfileID, std::\_\_1::unique\_ptr<Profile, std::\_\_1::default\_delete<Profile> > >, std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<Profile::OTRProfileID, std::\_\_1::unique\_ptr<Profile, std::\_\_1::default\_delete<Profile> > >, void\*>\*, long>) buildtools/third\_party/libc++/trunk/include/\_\_tree:2519:5  

#8 0x55556868c906 in \_\_erase\_unique[Profile::OTRProfileID](javascript:void(0);) buildtools/third\_party/libc++/trunk/include/\_\_tree:2542:5  

#9 0x55556868c906 in erase buildtools/third\_party/libc++/trunk/include/map:1304:25  

#10 0x55556868c906 in ProfileImpl::DestroyOffTheRecordProfile(Profile\*) chrome/browser/profiles/profile\_impl.cc:911:17  

#11 0x555568697c7d in ProfileDestroyer::DestroyProfileWhenAppropriate(Profile\*) chrome/browser/profiles/profile\_destroyer.cc:73:38  

#12 0x555571ad5bea in Browser::~Browser() chrome/browser/ui/browser.cc:651:7  

#13 0x555571ad6ecd in Browser::~Browser() chrome/browser/ui/browser.cc:565:21  

#14 0x5555720b955c in operator() buildtools/third\_party/libc++/trunk/include/memory:2378:5  

#15 0x5555720b955c in reset buildtools/third\_party/libc++/trunk/include/memory:2633:7  

#16 0x5555720b955c in ~unique\_ptr buildtools/third\_party/libc++/trunk/include/memory:2587:19  

#17 0x5555720b955c in BrowserView::~BrowserView() chrome/browser/ui/views/frame/browser\_view.cc:616:1  

#18 0x5555720b9de7 in ~BrowserView chrome/browser/ui/views/frame/browser\_view.cc:567:29  

#19 0x5555720b9de7 in non-virtual thunk to BrowserView::~BrowserView() chrome/browser/ui/views/frame/browser\_view.cc  

#20 0x55556fbd1ea1 in views::View::~View() ui/views/view.cc:200:9  

#21 0x55556fc7d79b in ~NonClientView ui/views/window/non\_client\_view.cc:151:1  

#22 0x55556fc7d79b in views::NonClientView::~NonClientView() ui/views/window/non\_client\_view.cc:147:33  

#23 0x55556fbd534f in operator() buildtools/third\_party/libc++/trunk/include/memory:2378:5  

#24 0x55556fbd534f in reset buildtools/third\_party/libc++/trunk/include/memory:2633:7  

#25 0x55556fbd534f in ~unique\_ptr buildtools/third\_party/libc++/trunk/include/memory:2587:19  

#26 0x55556fbd534f in views::View::DoRemoveChildView(views::View\*, bool, bool, bool, views::View\*) ui/views/view.cc:2362:1  

#27 0x55556fbd56e8 in views::View::RemoveAllChildViews(bool) ui/views/view.cc:272:5  

#28 0x55556fc28a8a in DestroyRootView ui/views/widget/widget.cc:1508:15  

#29 0x55556fc28a8a in views::Widget::~Widget() ui/views/widget/widget.cc:182:3  

#30 0x5555720e5457 in BrowserFrame::~BrowserFrame() chrome/browser/ui/views/frame/browser\_frame.cc:71:32  

#31 0x5555720e555d in BrowserFrame::~BrowserFrame() chrome/browser/ui/views/frame/browser\_frame.cc:71:31  

#32 0x55556fcde1ef in views::DesktopNativeWidgetAura::~DesktopNativeWidgetAura() ui/views/widget/desktop\_aura/desktop\_native\_widget\_aura.cc  

#33 0x5555721c09f6 in ~DesktopBrowserFrameAuraLinux chrome/browser/ui/views/frame/desktop\_browser\_frame\_aura\_linux.cc:28:64  

#34 0x5555721c09f6 in DesktopBrowserFrameAuraLinux::~DesktopBrowserFrameAuraLinux() chrome/browser/ui/views/frame/desktop\_browser\_frame\_aura\_linux.cc:28:63  

#35 0x55556fd0cf17 in views::DesktopWindowTreeHostPlatform::OnClosed() ui/views/widget/desktop\_aura/desktop\_window\_tree\_host\_platform.cc:683:32  

#36 0x55556fcb574a in views::DesktopWindowTreeHostLinux::OnClosed() ui/views/widget/desktop\_aura/desktop\_window\_tree\_host\_linux.cc:262:34  

#37 0x55556fd05aae in views::DesktopWindowTreeHostPlatform::CloseNow() ui/views/widget/desktop\_aura/desktop\_window\_tree\_host\_platform.cc:283:22  

#38 0x555569016e2d in Run base/callback.h:99:12  

#39 0x555569016e2d in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/task/common/task\_annotator.cc:142:33  

#40 0x55556904f03f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:329:23  

#41 0x55556904e9ac in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:254:36  

#42 0x555568f55649 in HandleDispatch base/message\_loop/message\_pump\_glib.cc:409:46  

#43 0x555568f55649 in base::(anonymous namespace)::WorkSourceDispatch(\_GSource\*, int (\*)(void\*), void\*) base/message\_loop/message\_pump\_glib.cc:122:43  

#44 0x7ffff7e42fbc in g\_main\_context\_dispatch (/lib/x86\_64-linux-gnu/libglib-2.0.so.0+0x51fbc)

previously allocated by thread T0 (chrome) here:  

#0 0x55555e916bfd in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:99:3  

#1 0x5555686ccddd in Profile::CreateOffTheRecordProfile(Profile\*, Profile::OTRProfileID const&) chrome/browser/profiles/off\_the\_record\_profile\_impl.cc:635:19  

#2 0x55556868bd71 in ProfileImpl::GetOffTheRecordProfile(Profile::OTRProfileID const&) chrome/browser/profiles/profile\_impl.cc:885:7  

#3 0x55556866223a in Profile::GetPrimaryOTRProfile() chrome/browser/profiles/profile.cc:480:10  

#4 0x555571b04c48 in chrome::NewIncognitoWindow(Profile\*) chrome/browser/ui/browser\_commands.cc:647:27  

#5 0x555571afb259 in chrome::BrowserCommandController::ExecuteCommandWithDisposition(int, WindowOpenDisposition, base::TimeTicks) chrome/browser/ui/browser\_command\_controller.cc:395:7  

#6 0x5555725e28dd in AppMenu::ExecuteCommand(int, int) chrome/browser/ui/views/toolbar/app\_menu.cc:924:23  

#7 0x55556fae4878 in views::internal::MenuRunnerImpl::OnMenuClosed(views::internal::MenuControllerDelegate::NotifyType, views::MenuItemView\*, int) ui/views/controls/menu/menu\_runner\_impl.cc:218:29  

#8 0x55556fafaf64 in views::MenuController::ExitMenu() ui/views/controls/menu/menu\_controller.cc:2937:13  

#9 0x55556faffb64 in ReallyAccept ui/views/controls/menu/menu\_controller.cc:1700:3  

#10 0x55556faffb64 in Accept ui/views/controls/menu/menu\_controller.cc:1681:3  

#11 0x55556faffb64 in views::MenuController::OnMouseReleased(views::SubmenuView\*, ui::MouseEvent const&) ui/views/controls/menu/menu\_controller.cc:787:7  

#12 0x55556fc38c28 in views::Widget::OnMouseEvent(ui::MouseEvent\*) ui/views/widget/widget.cc:1275:20  

#13 0x55556b3c5239 in DispatchEvent ui/events/event\_dispatcher.cc:193:12  

#14 0x55556b3c5239 in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:142:5  

#15 0x55556b3c4b01 in DispatchEventToTarget ui/events/event\_dispatcher.cc:86:14  

#16 0x55556b3c4b01 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:58:15  

#17 0x55556d8adb0d in ui::EventProcessor::OnEventFromSource(ui::Event\*) ui/events/event\_processor.cc:49:17  

#18 0x55556d8ca61f in ui::EventSource::DeliverEventToSink(ui::Event\*) ui/events/event\_source.cc:113:16  

#19 0x55556d8ca23a in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const\*, ui::EventRewriter const\*) ui/events/event\_source.cc:138:12  

#20 0x55556fcba5b0 in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event\*) ui/aura/window\_tree\_host\_platform.cc:229:38  

#21 0x55556fcb53a7 in views::DesktopWindowTreeHostLinux::DispatchEvent(ui::Event\*) ui/views/widget/desktop\_aura/desktop\_window\_tree\_host\_linux.cc:256:29  

#22 0x55556fcc105c in ui::X11Window::DispatchUiEvent(ui::Event\*, \_XEvent\*) ui/platform\_window/x11/x11\_window.cc:619:32  

#23 0x55556fcc073d in ui::X11Window::DispatchEvent(ui::Event\* const&) ui/platform\_window/x11/x11\_window.cc:566:3  

#24 0x55556fcc124f in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event\* const&) ui/platform\_window/x11/x11\_window.cc  

#25 0x55556b4eb802 in ui::PlatformEventSource::DispatchEvent(ui::Event\*) ui/events/platform/platform\_event\_source.cc:101:29  

#26 0x55556b4e307b in ui::X11EventSource::DispatchPlatformEvent(ui::Event\* const&, \_XEvent\*) ui/events/platform/x11/x11\_event\_source.cc:386:3  

#27 0x55556b4e0ee1 in ProcessXEvent ui/events/platform/x11/x11\_event\_source.cc:441:5  

#28 0x55556b4e0ee1 in ui::X11EventSource::ExtractCookieDataDispatchEvent(\_XEvent\*) ui/events/platform/x11/x11\_event\_source.cc:461:3  

#29 0x55556b4e0488 in operator() ui/events/platform/x11/x11\_event\_source.cc:209:5  

#30 0x55556b4e0488 in ui::X11EventSource::DispatchXEvents() ui/events/platform/x11/x11\_event\_source.cc:238:7  

#31 0x55556b4fd70b in ui::(anonymous namespace)::XSourceDispatch(\_GSource\*, int (\*)(void\*), void\*) ui/events/platform/x11/x11\_event\_watcher\_glib.cc:40:15  

#32 0x7ffff7e42e8d in g\_main\_context\_dispatch (/lib/x86\_64-linux-gnu/libglib-2.0.so.0+0x51e8d)

SUMMARY: AddressSanitizer: heap-use-after-free chrome/browser/extensions/chrome\_extensions\_browser\_client.cc:149:42 in extensions::ChromeExtensionsBrowserClient::GetOriginalContext(content::BrowserContext\*)  

Shadow bytes around the buggy address:  

0x0c2280121510: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2280121520: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa  

0x0c2280121530: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c2280121540: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2280121550: fd fd fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x0c2280121560:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2280121570: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2280121580: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c2280121590: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c22801215a0: fd fd fd fd fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c22801215b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

Shadow gap: cc

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [crash-test.html](attachments/crash-test.html) (text/plain, 281 B)
- [main.html](attachments/main.html) (text/plain, 388 B)
- [screen.mov](attachments/screen.mov) (video/quicktime, 7.0 MB)
- screen.mov (video/quicktime, 8.0 MB)

## Timeline

### oc...@google.com (2020-05-12)

dmazzoni, could you please take a look at this one? 

[Monorail components: Blink>Speech Platform>Extensions>API]

### ct...@chromium.org (2020-05-12)

[Empty comment from Monorail migration]

### ch...@gmail.com (2020-05-16)

I have a new testcase that doesn't require a lot of user interaction.

1. Lunch chrome 
2. Open https://lbstyle.github.io/main.html on an incognito tab.
3. Click on the button and close the tab.

Note: This is very similar to https://crbug.com/chromium/1043603.

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### dm...@chromium.org (2020-05-20)

I successfully wrote a failing test:
https://chromium-review.googlesource.com/c/chromium/src/+/2211123

Trying to figure out the right fix.


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9cca480661c60c22ec08320fd945923251be948a

commit 9cca480661c60c22ec08320fd945923251be948a
Author: Dominic Mazzoni <dmazzoni@chromium.org>
Date: Thu May 21 22:28:34 2020

Fix UAF in TtsPlatformImpl if a BrowserContext is deleted.

Bug: 1081350
Change-Id: I2b1824abefbd7fc3e8ce1c0cb433896161bab4e5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2211123
Reviewed-by: David Tseng <dtseng@chromium.org>
Reviewed-by: John Abd-El-Malek <jam@chromium.org>
Commit-Queue: Dominic Mazzoni <dmazzoni@chromium.org>
Cr-Commit-Position: refs/heads/master@{#771222}

[modify] https://crrev.com/9cca480661c60c22ec08320fd945923251be948a/chrome/browser/speech/extension_api/tts_extension_apitest.cc
[modify] https://crrev.com/9cca480661c60c22ec08320fd945923251be948a/content/browser/browser_context.cc
[modify] https://crrev.com/9cca480661c60c22ec08320fd945923251be948a/content/browser/speech/tts_controller_impl.cc
[modify] https://crrev.com/9cca480661c60c22ec08320fd945923251be948a/content/browser/speech/tts_controller_impl.h
[modify] https://crrev.com/9cca480661c60c22ec08320fd945923251be948a/content/browser/speech/tts_controller_unittest.cc
[modify] https://crrev.com/9cca480661c60c22ec08320fd945923251be948a/content/browser/speech/tts_utterance_impl.cc
[modify] https://crrev.com/9cca480661c60c22ec08320fd945923251be948a/content/browser/speech/tts_utterance_impl.h
[modify] https://crrev.com/9cca480661c60c22ec08320fd945923251be948a/content/public/browser/tts_utterance.h


### ch...@gmail.com (2020-05-22)

Verified on Chromium 85.0.4152.0 refs/heads/master@{#771235}. Fixed.

### ch...@gmail.com (2020-05-22)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/01fdc7ccfc6191c20330c4838d40b8d2c144df04

commit 01fdc7ccfc6191c20330c4838d40b8d2c144df04
Author: David Tseng <dtseng@chromium.org>
Date: Sat May 23 05:47:30 2020

Revert "Fix UAF in TtsPlatformImpl if a BrowserContext is deleted."

This reverts commit 9cca480661c60c22ec08320fd945923251be948a.

Reason for revert: <INSERT REASONING HERE>
See flakey failures
https://analysis.chromium.org/p/chromium/flake-portal/flakes/occurrences?key=ag9zfmZpbmRpdC1mb3ItbWVyTwsSBUZsYWtlIkRjaHJvbWl1bUBicm93c2VyX3Rlc3RzQENocm9tZVZveEJyYWlsbGVUYWJsZVRlc3QudGVzdEdldFVuY29udHJhY3RlZAw

[7369:7369:0522/203957.919406:FATAL:chrome_extensions_browser_client.cc(148)] Check failed: context.
#0 0x55cfe9dfc549 base::debug::CollectStackTrace()
#1 0x55cfe9d09be3 base::debug::StackTrace::StackTrace()
#2 0x55cfe9d20d7f logging::LogMessage::~LogMessage()
#3 0x55cfe9d2156e logging::LogMessage::~LogMessage()
#4 0x55cfed7b0e42 extensions::ChromeExtensionsBrowserClient::GetOriginalContext()
#5 0x55cfed58f4c3 BrowserContextKeyedServiceFactory::GetContextToUse()
#6 0x55cfebd733c3 KeyedServiceFactory::GetServiceForContext()
#7 0x55cfea38f279 extensions::TtsExtensionEventHandler::OnTtsEvent()
#8 0x55cfe73698c8 content::TtsUtteranceImpl::OnTtsEvent()
#9 0x55cfe7365120 content::TtsControllerImpl::ClearUtteranceQueue()
#10 0x55cfe7365f03 content::TtsControllerImpl::StopInternal()
#11 0x55cfe7367071 content::TtsControllerImpl::OnBrowserContextDestroyed()
#12 0x55cfe6d1d18c content::BrowserContext::~BrowserContext()
#13 0x55cfea0f813f ProfileImpl::~ProfileImpl()
#14 0x55cfea0f816e ProfileImpl::~ProfileImpl()
#15 0x55cfea0f1f72 ProfileDestroyer::DestroyRegularProfileNow()
#16 0x55cfea0f1d00 ProfileDestroyer::DestroyProfileWhenAppropriate()
#17 0x55cfea1137e8 std::__1::unique_ptr<>::~unique_ptr()
#18 0x55cfea114ee3 std::__1::__tree<>::destroy()
#19 0x55cfea11473b ProfileManager::~ProfileManager()
#20 0x55cfea10bfae ProfileManager::~ProfileManager()
#21 0x55cfe9eac15a BrowserProcessImpl::StartTearDown()
#22 0x55cfe9eaab2a ChromeBrowserMainParts::PostMainMessageLoopRun()
#23 0x55cfe51c9e74 chromeos::ChromeBrowserMainPartsChromeos::PostMainMessageLoopRun()
#24 0x55cfe6d41ccf content::BrowserMainLoop::ShutdownThreadsAndCleanUp()
#25 0x55cfe6d43b6d content::BrowserMainRunnerImpl::Shutdown()
#26 0x55cfe6d3eb02 content::BrowserMain()
#27 0x55cfe97ac717 content::ContentMainRunnerImpl::RunServiceManager()
#28 0x55cfe97ac2cf content::ContentMainRunnerImpl::Run()
#29 0x55cfec99806a service_manager::Main()
#30 0x55cfe7f60444 content::ContentMain()
#31 0x55cfea5622a4 content::BrowserTestBase::SetUp()
#32 0x55cfe9cf633b InProcessBrowserTest::SetUp()
#33 0x55cfe579858e testing::Test::Run()
#34 0x55cfe5799948 testing::TestInfo::Run()
#35 0x55cfe579a5e7 testing::TestSuite::Run()
#36 0x55cfe57aa747 testing::internal::UnitTestImpl::RunAllTests()
#37 0x55cfe57aa179 testing::UnitTest::Run()
#38 0x55cfe9e477e2 base::TestSuite::Run()
#39 0x55cfe9cdf0e7 BrowserTestSuiteRunnerChromeOS::RunTestSuite()
#40 0x55cfea5a72f4 content::LaunchTests()
#41 0x55cfe9cdf494 LaunchChromeTests()
#42 0x55cfe9cdf032 main
#43 0x7f421a16f830 __libc_start_main
#44 0x55cfe29b442a _start

Fixed: Fixed: 1085878, 1085877
Fixed: 1085878, 1085877

Original change's description:
> Fix UAF in TtsPlatformImpl if a BrowserContext is deleted.
>
> Bug: 1081350
> Change-Id: I2b1824abefbd7fc3e8ce1c0cb433896161bab4e5
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2211123
> Reviewed-by: David Tseng <dtseng@chromium.org>
> Reviewed-by: John Abd-El-Malek <jam@chromium.org>
> Commit-Queue: Dominic Mazzoni <dmazzoni@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#771222}

TBR=dmazzoni@chromium.org,dtseng@chromium.org,jam@chromium.org

# Not skipping CQ checks because original CL landed > 1 day ago.

Bug: 1081350
Change-Id: I88ec7e523fbe56845b8480b112535b2f8e18a520
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2213553
Reviewed-by: David Tseng <dtseng@chromium.org>
Commit-Queue: David Tseng <dtseng@chromium.org>
Cr-Commit-Position: refs/heads/master@{#771379}

[modify] https://crrev.com/01fdc7ccfc6191c20330c4838d40b8d2c144df04/chrome/browser/speech/extension_api/tts_extension_apitest.cc
[modify] https://crrev.com/01fdc7ccfc6191c20330c4838d40b8d2c144df04/content/browser/browser_context.cc
[modify] https://crrev.com/01fdc7ccfc6191c20330c4838d40b8d2c144df04/content/browser/speech/tts_controller_impl.cc
[modify] https://crrev.com/01fdc7ccfc6191c20330c4838d40b8d2c144df04/content/browser/speech/tts_controller_impl.h
[modify] https://crrev.com/01fdc7ccfc6191c20330c4838d40b8d2c144df04/content/browser/speech/tts_controller_unittest.cc
[modify] https://crrev.com/01fdc7ccfc6191c20330c4838d40b8d2c144df04/content/browser/speech/tts_utterance_impl.cc
[modify] https://crrev.com/01fdc7ccfc6191c20330c4838d40b8d2c144df04/content/browser/speech/tts_utterance_impl.h
[modify] https://crrev.com/01fdc7ccfc6191c20330c4838d40b8d2c144df04/content/public/browser/tts_utterance.h


### ch...@gmail.com (2020-05-26)

Friendly ping. Is there more work here? Thanks!

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/622d2e3ee522557da4bceef4e3f2fc06cbdcfdff

commit 622d2e3ee522557da4bceef4e3f2fc06cbdcfdff
Author: Dominic Mazzoni <dmazzoni@chromium.org>
Date: Fri May 29 23:30:00 2020

Re-land: Fix UAF in TtsPlatformImpl if a BrowserContext is deleted.

Original: http://crrev.com/c/2211123
Reverted: http://crrev.com/c/2213553

The underlying issue that caused the crash was that we
were trying to send a TTS event while a Profile was being
deleted. In the first patch I tried to work around that
and it added complexity.

In this new patch, there's a simpler solution: just use
PostTask to call Stop() - that way the Stop doesn't happen
until the Profile/BrowserContext is fully deleted.

Bug: 1081350
Tbr: jam@chromium.org
Change-Id: I4ce09a2cde3ef5fec93f73d723d9ec585e4c5815
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2218725
Commit-Queue: Dominic Mazzoni <dmazzoni@chromium.org>
Reviewed-by: David Tseng <dtseng@chromium.org>
Cr-Commit-Position: refs/heads/master@{#773411}

[modify] https://crrev.com/622d2e3ee522557da4bceef4e3f2fc06cbdcfdff/content/browser/browser_context.cc
[modify] https://crrev.com/622d2e3ee522557da4bceef4e3f2fc06cbdcfdff/content/browser/speech/tts_controller_impl.cc
[modify] https://crrev.com/622d2e3ee522557da4bceef4e3f2fc06cbdcfdff/content/browser/speech/tts_controller_impl.h
[modify] https://crrev.com/622d2e3ee522557da4bceef4e3f2fc06cbdcfdff/content/browser/speech/tts_controller_unittest.cc
[modify] https://crrev.com/622d2e3ee522557da4bceef4e3f2fc06cbdcfdff/content/browser/speech/tts_utterance_impl.cc
[modify] https://crrev.com/622d2e3ee522557da4bceef4e3f2fc06cbdcfdff/content/browser/speech/tts_utterance_impl.h
[modify] https://crrev.com/622d2e3ee522557da4bceef4e3f2fc06cbdcfdff/content/public/browser/tts_utterance.h


### dm...@chromium.org (2020-05-29)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-30)

[Empty comment from Monorail migration]

### na...@google.com (2020-06-01)

[Empty comment from Monorail migration]

### [Deleted User] (2020-06-01)

Requesting merge to beta M84 because latest trunk commit (773411) appears to be after beta branch point (768962).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-01)

This bug requires manual review: Reverts referenced in bugdroid comments after merge request.
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
Owners: govind@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2020-06-03)

+Adetaylor@(Security TPM) for Merge decision.

### ad...@chromium.org (2020-06-03)

As a browser process UaF, I think we should regard this as High - it would be Critical but it's mitigated down to High by the need for user interaction.

The change isn't trivial so let's not rush to merge this into M83, but approving merge to M84 (branch 4147). Applying a label for future M83 merge consideration.

### dm...@chromium.org (2020-06-03)

Merging to M84: https://chromium-review.googlesource.com/c/chromium/src/+/2228982


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-06-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/73f97c558c7cb3f38250e1274da4bdcc5f85dc9f

commit 73f97c558c7cb3f38250e1274da4bdcc5f85dc9f
Author: Dominic Mazzoni <dmazzoni@chromium.org>
Date: Wed Jun 03 19:00:39 2020

Merge to M84: Re-land: Fix UAF in TtsPlatformImpl if a BrowserContext is deleted.

Original: http://crrev.com/c/2211123
Reverted: http://crrev.com/c/2213553

The underlying issue that caused the crash was that we
were trying to send a TTS event while a Profile was being
deleted. In the first patch I tried to work around that
and it added complexity.

In this new patch, there's a simpler solution: just use
PostTask to call Stop() - that way the Stop doesn't happen
until the Profile/BrowserContext is fully deleted.

(cherry picked from commit 622d2e3ee522557da4bceef4e3f2fc06cbdcfdff)

Bug: 1081350
Tbr: jam@chromium.org
Change-Id: I4ce09a2cde3ef5fec93f73d723d9ec585e4c5815
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2218725
Commit-Queue: Dominic Mazzoni <dmazzoni@chromium.org>
Reviewed-by: David Tseng <dtseng@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#773411}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2228982
Reviewed-by: Dominic Mazzoni <dmazzoni@chromium.org>
Cr-Commit-Position: refs/branch-heads/4147@{#458}
Cr-Branched-From: 16307825352720ae04d898f37efa5449ad68b606-refs/heads/master@{#768962}

[modify] https://crrev.com/73f97c558c7cb3f38250e1274da4bdcc5f85dc9f/content/browser/browser_context.cc
[modify] https://crrev.com/73f97c558c7cb3f38250e1274da4bdcc5f85dc9f/content/browser/speech/tts_controller_impl.cc
[modify] https://crrev.com/73f97c558c7cb3f38250e1274da4bdcc5f85dc9f/content/browser/speech/tts_controller_impl.h
[modify] https://crrev.com/73f97c558c7cb3f38250e1274da4bdcc5f85dc9f/content/browser/speech/tts_controller_unittest.cc
[modify] https://crrev.com/73f97c558c7cb3f38250e1274da4bdcc5f85dc9f/content/browser/speech/tts_utterance_impl.cc
[modify] https://crrev.com/73f97c558c7cb3f38250e1274da4bdcc5f85dc9f/content/browser/speech/tts_utterance_impl.h
[modify] https://crrev.com/73f97c558c7cb3f38250e1274da4bdcc5f85dc9f/content/public/browser/tts_utterance.h


### na...@google.com (2020-06-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-06-04)

Congrats! The Panel decided to award $15,000 for this report. 

### na...@google.com (2020-06-04)

[Empty comment from Monorail migration]

### ad...@google.com (2020-06-04)

Approving merge to M83, branch 4103, assuming things look good in Canary. There may be an Android refresh early next week, so (again, assuming things are looking good) please merge fairly urgently.

### [Deleted User] (2020-06-08)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-09)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-10)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-06-10)

[Empty comment from Monorail migration]

### sr...@google.com (2020-06-10)

Please complete your merges to M83 branch asap, 

### sr...@google.com (2020-06-11)

Please complete merge to m83 by end of today Thursday June 11 , I am cutting stable RC for respin tomorrow PST time 

### [Deleted User] (2020-06-11)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-11)

The older reward-topanel https://crbug.com/chromium/1078642 has been merged into this one. Please manually review this issue to see if the duplicate is potentially eligible for a reward.



### ch...@gmail.com (2020-06-11)

[Comment Deleted]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-06-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/de8823fbc3fa3e985502eb05aaf2e044af361e63

commit de8823fbc3fa3e985502eb05aaf2e044af361e63
Author: Dominic Mazzoni <dmazzoni@chromium.org>
Date: Thu Jun 11 21:11:53 2020

Merge to M83: Re-land: Fix UAF in TtsPlatformImpl if a BrowserContext is deleted.

Original: http://crrev.com/c/2211123
Reverted: http://crrev.com/c/2213553

The underlying issue that caused the crash was that we
were trying to send a TTS event while a Profile was being
deleted. In the first patch I tried to work around that
and it added complexity.

In this new patch, there's a simpler solution: just use
PostTask to call Stop() - that way the Stop doesn't happen
until the Profile/BrowserContext is fully deleted.

(cherry picked from commit 622d2e3ee522557da4bceef4e3f2fc06cbdcfdff)

Bug: 1081350
Change-Id: Ia10fde26f526873d37855b03f66c5efb71a33225
Tbr: jam@chromium.org
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2242111
Reviewed-by: Dominic Mazzoni <dmazzoni@chromium.org>
Commit-Queue: Dominic Mazzoni <dmazzoni@chromium.org>
Cr-Commit-Position: refs/branch-heads/4103@{#688}
Cr-Branched-From: 8ad47e8d21f6866e4a37f47d83a860d41debf514-refs/heads/master@{#756066}

[modify] https://crrev.com/de8823fbc3fa3e985502eb05aaf2e044af361e63/content/browser/browser_context.cc
[modify] https://crrev.com/de8823fbc3fa3e985502eb05aaf2e044af361e63/content/browser/speech/tts_controller_impl.cc
[modify] https://crrev.com/de8823fbc3fa3e985502eb05aaf2e044af361e63/content/browser/speech/tts_controller_impl.h
[modify] https://crrev.com/de8823fbc3fa3e985502eb05aaf2e044af361e63/content/browser/speech/tts_controller_unittest.cc
[modify] https://crrev.com/de8823fbc3fa3e985502eb05aaf2e044af361e63/content/browser/speech/tts_utterance_impl.cc
[modify] https://crrev.com/de8823fbc3fa3e985502eb05aaf2e044af361e63/content/browser/speech/tts_utterance_impl.h
[modify] https://crrev.com/de8823fbc3fa3e985502eb05aaf2e044af361e63/content/public/browser/tts_utterance.h


### ad...@google.com (2020-06-12)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-06-12)

[Empty comment from Monorail migration]

### na...@google.com (2020-06-24)

[Empty comment from Monorail migration]

### ad...@google.com (2020-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2020-09-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1081350?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Speech, Platform>Extensions>API]
[Monorail mergedwith: crbug.com/chromium/1078642]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052285)*
