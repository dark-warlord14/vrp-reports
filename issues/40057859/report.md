# Security: UaF in AccessibilityUIMessageHandler::Callback

| Field | Value |
|-------|-------|
| **Issue ID** | [40057859](https://issues.chromium.org/issues/40057859) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Accessibility |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | as...@igalia.com |
| **Created** | 2021-11-09 |
| **Bounty** | $1,000.00 |

## Description

I feel that these two different crashes should be caused by the same reason, and I am not sure(<https://crbug.com/chromium/1267179>). I reproduced this crash under windows, but I couldn’t reproduce it successfully later, I don’t know why. The following is my analysis, which represents my point of view.

AccessibilityUIMessageHandler object was destroyed but is still used in AccessibilityUIMessageHandler::Callback function.Because here use unretained function.

void AccessibilityUIMessageHandler::RequestAccessibilityEvents(  

const base::ListValue\* args) {  

const base::Value& data = args->GetList()[0];  

CHECK(data.is\_dict());

int process\_id = \*data.FindIntPath(kProcessIdField);  

int routing\_id = \*data.FindIntPath(kRoutingIdField);  

bool start\_recording = \*data.FindBoolPath(kStartField);

AllowJavascript();

content::RenderViewHost\* rvh =  

content::RenderViewHost::FromID(process\_id, routing\_id);  

if (!rvh) {  

return;  

}

std::unique\_ptr[base::DictionaryValue](javascript:void(0);) result(BuildTargetDescriptor(rvh));  

content::WebContents\* web\_contents =  

content::WebContents::FromRenderViewHost(rvh);  

if (start\_recording) {  

if (observer\_) {  

return;  

}  

web\_contents->RecordAccessibilityEvents(  

true, base::BindRepeating(&AccessibilityUIMessageHandler::Callback, //UAF here  

base::Unretained(this)));  

**VERSION**  

Chrome Version: chromeos 97.0.4682.0  

Operating System: windows10 21h1

# asan log

==11760==ERROR: AddressSanitizer: heap-use-after-free on address 0x12e0c6957c40 at pc 0x7ffe279c1c38 bp 0x00dfec9fe820 sp 0x00dfec9fe868  

READ of size 8 at 0x12e0c6957c40 thread T0  

==11760==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ffe279c1c37 in AccessibilityUIMessageHandler::Callback C:\b\s\w\ir\cache\builder\src\chrome\browser\accessibility\accessibility\_ui.cc:721  

#1 0x7ffe1a630886 in ui::AXEventRecorder::OnEvent C:\b\s\w\ir\cache\builder\src\ui\accessibility\platform\inspect\ax\_event\_recorder.cc:23  

#2 0x7ffe1c2cc081 in content::AccessibilityEventRecorderWin::OnWinEventHook C:\b\s\w\ir\cache\builder\src\content\browser\accessibility\accessibility\_event\_recorder\_win.cc:337  

#3 0x7ffe1c2c78ac in content::AccessibilityEventRecorderWin::WinEventHookThunk C:\b\s\w\ir\cache\builder\src\content\browser\accessibility\accessibility\_event\_recorder\_win.cc:98  

#4 0x7ffea706671b in GetMenuItemCount+0xeb (C:\WINDOWS\System32\USER32.dll+0x18002671b)  

#5 0x7ffea7bf0ba3 in KiUserCallbackDispatcher+0x23 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800a0ba3)  

#6 0x7ffea53015e3 in NtUserNotifyWinEvent+0x13 (C:\WINDOWS\System32\win32u.dll+0x1800015e3)  

#7 0x7ffe1a697a44 in ui::AXPlatformNodeWin::NotifyAccessibilityEvent C:\b\s\w\ir\cache\builder\src\ui\accessibility\platform\ax\_platform\_node\_win.cc:665  

#8 0x7ffe27602f53 in views::`anonymous namespace'::FlushQueue C:\b\s\w\ir\cache\builder\src\ui\views\accessibility\view\_ax\_platform\_node\_delegate.cc:101  

#9 0x7ffe21fefffa in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:178  

#10 0x7ffe24acaf4f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:358  

#11 0x7ffe24aca668 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:261  

#12 0x7ffe22098c36 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:220  

#13 0x7ffe22096ec8 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#14 0x7ffe24acc365 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:463  

#15 0x7ffe21f6fcf3 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#16 0x7ffe1b27ac81 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1005  

#17 0x7ffe1b27ff8d in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:152  

#18 0x7ffe1b27471a in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:49  

#19 0x7ffe1dc4b4e0 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:641  

#20 0x7ffe1dc4dde9 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1137  

#21 0x7ffe1dc4cfd3 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1004  

#22 0x7ffe1dc499e2 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:390  

#23 0x7ffe1dc4aa24 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:418  

#24 0x7ffe1766147f in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:172  

#25 0x7ff7938b5b45 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:170  

#26 0x7ff7938b2c31 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#27 0x7ff793cad17f in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#28 0x7ffea6c17033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#29 0x7ffea7ba2650 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

0x12e0c6957c40 is located 32 bytes inside of 56-byte region [0x12e0c6957c20,0x12e0c6957c58)  

freed by thread T0 here:  

#0 0x7ff79396227b in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ffe279c1e55 in AccessibilityUIMessageHandler::~~AccessibilityUIMessageHandler C:\b\s\w\ir\cache\builder\src\chrome\browser\accessibility\accessibility\_ui.cc:400  

#2 0x7ffe17712128 in std::\_\_1::\_\_vector\_base<std::\_\_1::unique\_ptr<perfetto::internal::TracingMuxerImpl::ConsumerImpl,std::\_\_1::default\_delete[perfetto::internal::TracingMuxerImpl::ConsumerImpl](javascript:void(0);) >,std::\_\_1::allocator<std::\_\_1::unique\_ptr<perfetto::internal::TracingMuxerImpl::ConsumerImpl,std::\_\_1::default\_delete[perfetto::internal::TracingMuxerImpl::ConsumerImpl](javascript:void(0);) > > >::~~\_\_vector\_base C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\vector:466  

#3 0x7ffe1c27e339 in content::WebUIImpl::~WebUIImpl C:\b\s\w\ir\cache\builder\src\content\browser\webui\web\_ui\_impl.cc:86  

#4 0x7ffe1c282c05 in content::WebUIImpl::~WebUIImpl C:\b\s\w\ir\cache\builder\src\content\browser\webui\web\_ui\_impl.cc:80  

#5 0x7ffe1bdb59f7 in content::RenderFrameHostManager::ClearWebUIInstances C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_manager.cc:840  

#6 0x7ffe1bb1c2af in content::FrameTree::Shutdown C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\frame\_tree.cc:854  

#7 0x7ffe1c11ff75 in content::WebContentsImpl::~WebContentsImpl C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.cc:1022  

#8 0x7ffe1c194171 in content::WebContentsImpl::~WebContentsImpl C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.cc:968  

#9 0x7ffe2428bc47 in TabStripModel::SendDetachWebContentsNotifications C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab\_strip\_model.cc:555  

#10 0x7ffe242920d0 in TabStripModel::CloseTabs C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab\_strip\_model.cc:1797  

#11 0x7ffe24292f8f in TabStripModel::CloseWebContentsAt C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab\_strip\_model.cc:766  

#12 0x7ffe2be902d2 in BrowserTabStripController::CloseTab C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\browser\_tab\_strip\_controller.cc:371  

#13 0x7ffe2bea4a7e in TabStrip::CloseTabInternal C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_strip.cc:3069  

#14 0x7ffe2bea45a9 in TabStrip::CloseTab C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_strip.cc:1983  

#15 0x7ffe2f01475f in Tab::CloseButtonPressed C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab.cc:1073  

#16 0x7ffe21d0887b in views::Button::NotifyClick C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\button.cc:632  

#17 0x7ffe21d04c1d in views::Button::DefaultButtonControllerDelegate::NotifyClick C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\button.cc:66  

#18 0x7ffe2466d68a in views::ButtonController::OnMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\button\_controller.cc:59  

#19 0x7ffe21d43270 in views::View::ProcessMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3077  

#20 0x7ffe2b57f356 in ui::ScopedTargetHandler::OnEvent C:\b\s\w\ir\cache\builder\src\ui\events\scoped\_target\_handler.cc:28  

#21 0x7ffe22c4dc7d in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:191  

#22 0x7ffe22c4d19d in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:140  

#23 0x7ffe22c4ca87 in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:84  

#24 0x7ffe22c4c6c8 in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:56  

#25 0x7ffe246e692b in views::internal::RootView::OnMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\widget\root\_view.cc:485  

#26 0x7ffe21d6aed2 in views::Widget::OnMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1541  

#27 0x7ffe22c4dc7d in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:191

previously allocated by thread T0 here:  

#0 0x7ff79396237b in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ffe347d3c6a in operator new d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ffe279b6090 in AccessibilityUI::AccessibilityUI C:\b\s\w\ir\cache\builder\src\chrome\browser\accessibility\accessibility\_ui.cc:379  

#3 0x7ffe2481229b in ChromeWebUIControllerFactory::CreateWebUIControllerForURL C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\webui\chrome\_web\_ui\_controller\_factory.cc:1184  

#4 0x7ffe1c2738b2 in content::WebUIControllerFactoryRegistry::CreateWebUIControllerForURL C:\b\s\w\ir\cache\builder\src\content\browser\webui\web\_ui\_controller\_factory\_registry.cc:44  

#5 0x7ffe1c18887f in content::WebContentsImpl::CreateWebUI C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.cc:8194  

#6 0x7ffe1c1886c0 in content::WebContentsImpl::CreateWebUIForRenderFrameHost C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.cc:7864  

#7 0x7ffe1bd5c620 in content::RenderFrameHostImpl::CreateWebUI C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc:8442  

#8 0x7ffe1bdb6c43 in content::RenderFrameHostManager::GetFrameHostForNavigation C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_manager.cc:1038  

#9 0x7ffe1bdb5c9a in content::RenderFrameHostManager::DidCreateNavigationRequest C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_manager.cc:895  

#10 0x7ffe1bb2271a in content::FrameTreeNode::CreatedNavigationRequest C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\frame\_tree\_node.cc:528  

#11 0x7ffe1bce4685 in content::Navigator::Navigate C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\navigator.cc:620  

#12 0x7ffe1bc53a4d in content::NavigationControllerImpl::NavigateWithoutEntry C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\navigation\_controller\_impl.cc:3298  

#13 0x7ffe1bc52b84 in content::NavigationControllerImpl::LoadURLWithParams C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\navigation\_controller\_impl.cc:1121  

#14 0x7ffe2427f42c in `anonymous namespace'::LoadURLInContents C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser\_navigator.cc:379  

#15 0x7ffe2427c6f5 in Navigate C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser\_navigator.cc:656  

#16 0x7ffe2426bf8a in Browser::OpenURLFromTab C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser.cc:1589  

#17 0x7ffe1c151241 in content::WebContentsImpl::OpenURL C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.cc:4505  

#18 0x7ffe278eba49 in RenderViewContextMenuBase::OpenURLWithExtraHeaders C:\b\s\w\ir\cache\builder\src\components\renderer\_context\_menu\render\_view\_context\_menu\_base.cc:490  

#19 0x7ffe2bb327d3 in RenderViewContextMenu::ExecuteCommand C:\b\s\w\ir\cache\builder\src\chrome\browser\renderer\_context\_menu\render\_view\_context\_menu.cc:2507  

#20 0x7ffe2e99a79d in views::MenuModelAdapter::ExecuteCommand C:\b\s\w\ir\cache\builder\src\ui\views\controls\menu\menu\_model\_adapter.cc:170  

#21 0x7ffe275f5337 in views::internal::MenuRunnerImpl::OnMenuClosed C:\b\s\w\ir\cache\builder\src\ui\views\controls\menu\menu\_runner\_impl.cc:233  

#22 0x7ffe2b58f082 in views::MenuController::ExitMenu C:\b\s\w\ir\cache\builder\src\ui\views\controls\menu\menu\_controller.cc:3176  

#23 0x7ffe2b5944cd in views::MenuController::Accept C:\b\s\w\ir\cache\builder\src\ui\views\controls\menu\menu\_controller.cc:1779  

#24 0x7ffe2b593a61 in views::MenuController::OnMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\controls\menu\menu\_controller.cc:826  

#25 0x7ffe21d6aed2 in views::Widget::OnMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1541  

#26 0x7ffe22c4dc7d in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:191  

#27 0x7ffe22c4d19d in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:140

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\chrome\browser\accessibility\accessibility\_ui.cc:721 in AccessibilityUIMessageHandler::Callback  

Shadow bytes around the buggy address:  

0x0530df12af30: fd fd fd fd fd fd fd fa fa fa fa fa fd fd fd fd  

0x0530df12af40: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fd  

0x0530df12af50: fa fa fa fa fd fd fd fd fd fd fd fa fa fa fa fa  

0x0530df12af60: 00 00 00 00 00 00 00 00 fa fa fa fa 00 00 00 00  

0x0530df12af70: 00 00 00 00 fa fa fa fa 00 00 00 00 00 00 00 00  

=>0x0530df12af80: fa fa fa fa fd fd fd fd[fd]fd fd fa fa fa fa fa  

0x0530df12af90: fd fd fd fd fd fd fd fd fa fa fa fa fd fd fd fd  

0x0530df12afa0: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fd  

0x0530df12afb0: fa fa fa fa fd fd fd fd fd fd fd fd fa fa fa fa  

0x0530df12afc0: fd fd fd fd fd fd fd fd fa fa fa fa fd fd fd fd  

0x0530df12afd0: fd fd fd fd fa fa fa fa 00 00 00 00 00 00 00 00  

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

==11760==ABORTING

## Attachments

- [crash.mkv](attachments/crash.mkv) (application/octet-stream, 4.9 MB)

## Timeline

### [Deleted User] (2021-11-09)

[Empty comment from Monorail migration]

### ts...@chromium.org (2021-11-09)

Reporter, can you attach the test case which triggered this crash? Thanks.

[Monorail components: UI>Accessibility]

### [Deleted User] (2021-11-09)

[Empty comment from Monorail migration]

### ha...@gmail.com (2021-11-10)

[Comment Deleted]

### ha...@gmail.com (2021-11-10)

tsepez,sorry, I don't know how this change provides recurring steps. This UAF needs to be interacted with. I also triggered this UAF by accident.But I can tell you the steps I used to crash in chrome os, you can refer to this video.Maybe the report I submitted before is the same reason as this vulnerability https://crbug.com/chromium/1267179

### ha...@gmail.com (2021-11-12)

[Comment Deleted]

### ha...@gmail.com (2021-11-12)

hello,I don’t know what operation caused UAF ,but I think I understand the cause of this vulnerability.


void AccessibilityUIMessageHandler::RequestAccessibilityEvents(
    const base::ListValue* args) {
  const base::Value& data = args->GetList()[0];
  CHECK(data.is_dict());

  int process_id = *data.FindIntPath(kProcessIdField);
  int routing_id = *data.FindIntPath(kRoutingIdField);
  bool start_recording = *data.FindBoolPath(kStartField);

  AllowJavascript();

  content::RenderViewHost* rvh =
      content::RenderViewHost::FromID(process_id, routing_id);
  if (!rvh) {
    return;
  }

  std::unique_ptr<base::DictionaryValue> result(BuildTargetDescriptor(rvh));
  content::WebContents* web_contents =
      content::WebContents::FromRenderViewHost(rvh);
  if (start_recording) {
    if (observer_) {
      return;
    }
    web_contents->RecordAccessibilityEvents(
        true, base::BindRepeating(&AccessibilityUIMessageHandler::Callback,  // AccessibilityUIMessageHandler::Callback use  base::Unretained
                                  base::Unretained(this)));


class AccessibilityUIMessageHandler : public content::WebUIMessageHandler {   //These objects are owned by WebUI and destroyed when the host is destroyed.
-------------------------------

void AXEventRecorder::OnEvent(const std::string& event) {
  base::AutoLock lock{on_event_lock_};
  event_logs_.push_back(event);
  if (callback_){ 
    callback_.Run(event);   // The callback function   AccessibilityUIMessageHandler::Callback still will be called,although AccessibilityUIMessageHandler object already destroyed 
  }
}

void AccessibilityUIMessageHandler::Callback(const std::string& str) {
  event_logs_.push_back(str);  //UAF here
}

### ha...@gmail.com (2021-11-17)

Any update?

### rs...@chromium.org (2021-11-23)

As the reporter notes, this is likely an unsafe use of Unretained. Labeling as Sev-Low because this is an internal debug page.

### rs...@chromium.org (2021-11-23)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-23)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-23)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@gmail.com (2021-11-23)

Hello dtseng,this coudle be high because UAF oaccur in browser process. and https://bugs.chromium.org/p/chromium/issues/detail?id=1232628&q=Type%3DBug-Security%20status%3DFixed&can=1  this vuln also happen in an internal debug page.

### gi...@appspot.gserviceaccount.com (2021-11-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0846e75996f4702afb6f6c64e9bb394cf9abe515

commit 0846e75996f4702afb6f6c64e9bb394cf9abe515
Author: David Tseng <dtseng@google.com>
Date: Wed Nov 24 18:02:48 2021

Speculative fix for shutdown crash in chrome://accessibility

R=josiahk@google.com

Bug: 1268240
Test: none
Change-Id: I37d0a77ef24fe9b1fe5ac49cfb3ed73e9551222b
AX-Relnotes: n/a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3299349
Reviewed-by: Josiah Krutz <josiahk@google.com>
Commit-Queue: David Tseng <dtseng@chromium.org>
Cr-Commit-Position: refs/heads/main@{#945034}

[modify] https://crrev.com/0846e75996f4702afb6f6c64e9bb394cf9abe515/chrome/browser/accessibility/accessibility_ui.h
[modify] https://crrev.com/0846e75996f4702afb6f6c64e9bb394cf9abe515/chrome/browser/accessibility/accessibility_ui.cc


### ha...@gmail.com (2021-12-10)

Hello,If this vulnerability is fixed, please change to the fix state 

### me...@chromium.org (2021-12-20)

Bumping this to severity-medium. This is a UAF in the browser process which is normally criticial. There are enough mitigating factors reduce severity down two levels to medium. Webui pages have been used in exploit chains, so severity-low feels too low.

### [Deleted User] (2021-12-21)

abigailbklein: Uh oh! This issue still open and hasn't been updated in the last 42 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@chromium.org (2021-12-21)

[Empty comment from Monorail migration]

### as...@igalia.com (2021-12-22)

I wonder if David's fix from bug https://crbug.com/chromium/1268240#c14 fixed the issue. Is there a way to reproduce the bug or perhaps could somebody check available stack traces (I think I don't have access)?

### ha...@gmail.com (2021-12-22)

Yep,fixed.But didn't change the status to fixed(closed)

### as...@igalia.com (2021-12-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-23)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ha...@gmail.com (2022-01-13)

And a friend of mine just described, there are 5000 without actual repro, which is a bit unfair, https://bugs.chromium.org/p/chromium/issues/detail?id=1243117 This has 15,000 without actual  repro, I don't know what you think

### am...@chromium.org (2022-01-14)

Hello, this reward amount was not determine solely because there was no POC or reproduction, but also because 
1) this bug does not appear to be reachable from the web and triggering it would require considerable amount of UI gesture
2) there would be very limited attacker control to exploit this issue, so with the very low exploitability potential, the reward extended is much lower  

### am...@chromium.org (2022-01-14)

I forgot to add to the above, if you can provide a POC or other demonstration that displays a way to trigger and exploit this issue without exceptional and direct UI gesture and demonstrate greater control of this vulnerability, we would be happy to revisit this issue and reassess the reward amount. Thank you. 

### am...@google.com (2022-01-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-02-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-04-05)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/1268240?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057859)*
