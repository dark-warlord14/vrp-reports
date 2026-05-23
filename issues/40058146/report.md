# Security: heap-use-after-free ui::AXEventRecorder::OnEvent

| Field | Value |
|-------|-------|
| **Issue ID** | [40058146](https://issues.chromium.org/issues/40058146) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Accessibility |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2021-12-07 |
| **Bounty** | $7,000.00 |

## Description

It looks different from the cause of <https://crbug.com/chromium/1277324>, trigger this vulnerability needs to be enabled Touch UI Layout.If you need to reproduce the video, I will send it to you.

=================================================================  

==11216==ERROR: AddressSanitizer: heap-use-after-free on address 0x1200fef329d0 at pc 0x7ffcb0c08d54 bp 0x00de365f94e0 sp 0x00de365f9528  

READ of size 8 at 0x1200fef329d0 thread T0  

#0 0x7ffcb0c08d53 in ui::AXEventRecorder::OnEvent E:\src\chromium\src\ui\accessibility\platform\inspect\ax\_event\_recorder.cc:24  

#1 0x7ffcbb5b0d09 in content::AccessibilityEventRecorderWin::OnWinEventHook E:\src\chromium\src\content\browser\accessibility\accessibility\_event\_recorder\_win.cc:337  

#2 0x7ffcbb5acd08 in content::AccessibilityEventRecorderWin::WinEventHookThunk E:\src\chromium\src\content\browser\accessibility\accessibility\_event\_recorder\_win.cc:98  

#3 0x7ffd3056671b in GetMenuItemCount+0xeb (C:\Windows\System32\USER32.dll+0x18002671b)  

#4 0x7ffd32450ba3 in KiUserCallbackDispatcher+0x23 (C:\Windows\SYSTEM32\ntdll.dll+0x1800a0ba3)  

#5 0x7ffd2fdf15e3 in NtUserNotifyWinEvent+0x13 (C:\Windows\System32\win32u.dll+0x1800015e3)  

#6 0x7ffcbb5ea904 in content::BrowserAccessibilityManagerWin::FireGeneratedEvent E:\src\chromium\src\content\browser\accessibility\browser\_accessibility\_manager\_win.cc:213  

#7 0x7ffcba00b94a in content::BrowserAccessibilityManager::OnAccessibilityEvents E:\src\chromium\src\content\browser\accessibility\browser\_accessibility\_manager.cc:554  

#8 0x7ffcbaf1f5f8 in content::RenderFrameHostImpl::HandleAXEvents E:\src\chromium\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc:7180  

#9 0x7ffcba030e11 in base::internal::Invoker<base::internal::BindState<void (content::RenderFrameHostImpl::\*)(const ui::AXTreeID &, mojo::StructPtr[content::mojom::AXUpdatesAndEvents](javascript:void(0);), int),base::WeakPtr[content::RenderFrameHostImpl](javascript:void(0);),ui::AXTreeID,mojo::StructPtr[content::mojom::AXUpdatesAndEvents](javascript:void(0);),int>,void ()>::RunOnce E:\src\chromium\src\base\bind\_internal.h:741  

#10 0x7ffcd2cdb3df in base::`anonymous namespace'::PostTaskAndReplyRelay::RunTaskAndPostReply E:\src\chromium\src\base\threading\post\_task\_and\_reply\_impl.cc:100  

#11 0x7ffcd2cdbc23 in base::internal::Invoker<base::internal::BindState<void (\*)(base::(anonymous namespace)::PostTaskAndReplyRelay),base::(anonymous namespace)::PostTaskAndReplyRelay>,void ()>::RunOnce E:\src\chromium\src\base\bind\_internal.h:741  

#12 0x7ffcd2c27474 in base::TaskAnnotator::RunTaskImpl E:\src\chromium\src\base\task\common\task\_annotator.cc:135  

#13 0x7ffcd2c74789 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl E:\src\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:356  

#14 0x7ffcd2c73e58 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork E:\src\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:261  

#15 0x7ffcd2d70216 in base::MessagePumpForUI::DoRunLoop E:\src\chromium\src\base\message\_loop\message\_pump\_win.cc:220  

#16 0x7ffcd2d6dccf in base::MessagePumpWin::Run E:\src\chromium\src\base\message\_loop\message\_pump\_win.cc:78  

#17 0x7ffcd2c75f03 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run E:\src\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:468  

#18 0x7ffcd2b71e03 in base::RunLoop::Run E:\src\chromium\src\base\run\_loop.cc:140  

#19 0x7ffcba2a72a1 in content::BrowserMainLoop::RunMainMessageLoop E:\src\chromium\src\content\browser\browser\_main\_loop.cc:1038  

#20 0x7ffcba2ad0a3 in content::BrowserMainRunnerImpl::Run E:\src\chromium\src\content\browser\browser\_main\_runner\_impl.cc:153  

#21 0x7ffcba2a072f in content::BrowserMain E:\src\chromium\src\content\browser\browser\_main.cc:30  

#22 0x7ffcbc3eb22e in content::RunBrowserProcessMain E:\src\chromium\src\content\app\content\_main\_runner\_impl.cc:646  

#23 0x7ffcbc3ee3e3 in content::ContentMainRunnerImpl::RunBrowser E:\src\chromium\src\content\app\content\_main\_runner\_impl.cc:1160  

#24 0x7ffcbc3ed511 in content::ContentMainRunnerImpl::Run E:\src\chromium\src\content\app\content\_main\_runner\_impl.cc:1026  

#25 0x7ffcbc3e92bf in content::RunContentProcess E:\src\chromium\src\content\app\content\_main.cc:398  

#26 0x7ffcbc3ea327 in content::ContentMain E:\src\chromium\src\content\app\content\_main.cc:426  

#27 0x7ffcbf9314a5 in ChromeMain E:\src\chromium\src\chrome\app\chrome\_main.cc:172  

#28 0x7ff7903d5554 in MainDllLoader::Launch E:\src\chromium\src\chrome\app\main\_dll\_loader\_win.cc:169  

#29 0x7ff7903d2a02 in main E:\src\chromium\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#30 0x7ff7905aee4b in \_\_scrt\_common\_main\_seh D:\agent\_work\13\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#31 0x7ffd30497033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  

#32 0x7ffd32402650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

0x1200fef329d0 is located 32 bytes inside of 72-byte region [0x1200fef329b0,0x1200fef329f8)  

freed by thread T0 here:  

#0 0x7ffcd1af070b in operator delete+0x8b (E:\src\chromium\src\out\Default\clang\_rt.asan\_dynamic-x86\_64.dll+0x18004070b)  

#1 0x7ffcbb5b3960 in content::AccessibilityEventRecorderWin::~AccessibilityEventRecorderWin E:\src\chromium\src\content\browser\accessibility\accessibility\_event\_recorder\_win.cc:136  

#2 0x7ffcbb3b30a4 in content::WebContentsImpl::~WebContentsImpl E:\src\chromium\src\content\browser\web\_contents\web\_contents\_impl.cc:1070  

#3 0x7ffcbb43e49b in content::WebContentsImpl::~WebContentsImpl E:\src\chromium\src\content\browser\web\_contents\web\_contents\_impl.cc:972  

#4 0x7ffc8e8988c9 in views::WebView::SetWebContents E:\src\chromium\src\ui\views\controls\webview\webview.cc:106  

#5 0x7ffc8e898699 in views::WebView::~WebView E:\src\chromium\src\ui\views\controls\webview\webview.cc:74  

#6 0x7ffc8e89c849 in views::WebView::~WebView E:\src\chromium\src\ui\views\controls\webview\webview.cc:72  

#7 0x7ffcbf55cffd in views::View::~View E:\src\chromium\src\ui\views\view.cc:253  

#8 0x7ffcc732149f in WebUITabStripContainerView::~WebUITabStripContainerView E:\src\chromium\src\chrome\browser\ui\views\frame\webui\_tab\_strip\_container\_view.cc:494  

#9 0x7ffcc57f0188 in BrowserView::MaybeInitializeWebUITabStrip E:\src\chromium\src\chrome\browser\ui\views\frame\browser\_view.cc:3441  

#10 0x7ffcb0bdf1ed in ui::AXPlatformNode::NotifyAddAXModeFlags E:\src\chromium\src\ui\accessibility\platform\ax\_platform\_node.cc:105  

#11 0x7ffcb0c823a4 in ui::AXPlatformNodeWin::get\_states E:\src\chromium\src\ui\accessibility\platform\ax\_platform\_node\_win.cc:1270  

#12 0x7ffcbb5ae4be in content::AccessibilityEventRecorderWin::OnWinEventHook E:\src\chromium\src\content\browser\accessibility\accessibility\_event\_recorder\_win.cc:248  

#13 0x7ffcbb5acd08 in content::AccessibilityEventRecorderWin::WinEventHookThunk E:\src\chromium\src\content\browser\accessibility\accessibility\_event\_recorder\_win.cc:98  

#14 0x7ffd3056671b in GetMenuItemCount+0xeb (C:\Windows\System32\USER32.dll+0x18002671b)  

#15 0x7ffd32450ba3 in KiUserCallbackDispatcher+0x23 (C:\Windows\SYSTEM32\ntdll.dll+0x1800a0ba3)  

#16 0x7ffd2fdf15e3 in NtUserNotifyWinEvent+0x13 (C:\Windows\System32\win32u.dll+0x1800015e3)  

#17 0x7ffcbb5ea904 in content::BrowserAccessibilityManagerWin::FireGeneratedEvent E:\src\chromium\src\content\browser\accessibility\browser\_accessibility\_manager\_win.cc:213  

#18 0x7ffcba00b94a in content::BrowserAccessibilityManager::OnAccessibilityEvents E:\src\chromium\src\content\browser\accessibility\browser\_accessibility\_manager.cc:554  

#19 0x7ffcbaf1f5f8 in content::RenderFrameHostImpl::HandleAXEvents E:\src\chromium\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc:7180  

#20 0x7ffcba030e11 in base::internal::Invoker<base::internal::BindState<void (content::RenderFrameHostImpl::\*)(const ui::AXTreeID &, mojo::StructPtr[content::mojom::AXUpdatesAndEvents](javascript:void(0);), int),base::WeakPtr[content::RenderFrameHostImpl](javascript:void(0);),ui::AXTreeID,mojo::StructPtr[content::mojom::AXUpdatesAndEvents](javascript:void(0);),int>,void ()>::RunOnce E:\src\chromium\src\base\bind\_internal.h:741  

#21 0x7ffcd2cdb3df in base::`anonymous namespace'::PostTaskAndReplyRelay::RunTaskAndPostReply E:\src\chromium\src\base\threading\post\_task\_and\_reply\_impl.cc:100  

#22 0x7ffcd2cdbc23 in base::internal::Invoker<base::internal::BindState<void (\*)(base::(anonymous namespace)::PostTaskAndReplyRelay),base::(anonymous namespace)::PostTaskAndReplyRelay>,void ()>::RunOnce E:\src\chromium\src\base\bind\_internal.h:741  

#23 0x7ffcd2c27474 in base::TaskAnnotator::RunTaskImpl E:\src\chromium\src\base\task\common\task\_annotator.cc:135  

#24 0x7ffcd2c74789 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl E:\src\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:356  

#25 0x7ffcd2c73e58 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork E:\src\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:261  

#26 0x7ffcd2d70216 in base::MessagePumpForUI::DoRunLoop E:\src\chromium\src\base\message\_loop\message\_pump\_win.cc:220  

#27 0x7ffcd2d6dccf in base::MessagePumpWin::Run E:\src\chromium\src\base\message\_loop\message\_pump\_win.cc:78

previously allocated by thread T0 here:  

#0 0x7ffcd1af041b in operator new+0x8b (E:\src\chromium\src\out\Default\clang\_rt.asan\_dynamic-x86\_64.dll+0x18004041b)  

#1 0x7ffcb904ec4c in content::AXInspectFactory::CreateRecorder E:\src\chromium\src\content\public\browser\ax\_inspect\_factory\_win.cc:75  

#2 0x7ffcb904ea05 in content::AXInspectFactory::CreatePlatformRecorder E:\src\chromium\src\content\public\browser\ax\_inspect\_factory\_win.cc:30  

#3 0x7ffcbb3e90df in content::WebContentsImpl::RecordAccessibilityEvents E:\src\chromium\src\content\browser\web\_contents\web\_contents\_impl.cc:4348  

#4 0x7ffcc5603008 in AccessibilityUIMessageHandler::RequestAccessibilityEvents E:\src\chromium\src\chrome\browser\accessibility\accessibility\_ui.cc:737  

#5 0x7ffcbb554b94 in content::WebUIImpl::ProcessWebUIMessage E:\src\chromium\src\content\browser\webui\web\_ui\_impl.cc:288  

#6 0x7ffcbb550f87 in content::WebUIImpl::Send E:\src\chromium\src\content\browser\webui\web\_ui\_impl.cc:112  

#7 0x7ffcb98324e8 in content::mojom::WebUIHostStubDispatch::Accept E:\src\chromium\src\out\Default\gen\content\common\web\_ui.mojom.cc:159  

#8 0x7ffcfa049a14 in mojo::InterfaceEndpointClient::HandleValidatedMessage E:\src\chromium\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:900  

#9 0x7ffcfa059a88 in mojo::MessageDispatcher::Accept E:\src\chromium\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:43  

#10 0x7ffcfa04d3c4 in mojo::InterfaceEndpointClient::HandleIncomingMessage E:\src\chromium\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:657  

#11 0x7ffcf1f0e5d4 in IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnEndpointThread E:\src\chromium\src\ipc\ipc\_mojo\_bootstrap.cc:1005  

#12 0x7ffcf1f07dd4 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message),scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce E:\src\chromium\src\base\bind\_internal.h:741  

#13 0x7ffcd2c27474 in base::TaskAnnotator::RunTaskImpl E:\src\chromium\src\base\task\common\task\_annotator.cc:135  

#14 0x7ffcd2c74789 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl E:\src\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:356  

#15 0x7ffcd2c73e58 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork E:\src\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:261  

#16 0x7ffcd2d70216 in base::MessagePumpForUI::DoRunLoop E:\src\chromium\src\base\message\_loop\message\_pump\_win.cc:220  

#17 0x7ffcd2d6dccf in base::MessagePumpWin::Run E:\src\chromium\src\base\message\_loop\message\_pump\_win.cc:78  

#18 0x7ffcd2c75f03 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run E:\src\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:468  

#19 0x7ffcd2b71e03 in base::RunLoop::Run E:\src\chromium\src\base\run\_loop.cc:140  

#20 0x7ffcba2a72a1 in content::BrowserMainLoop::RunMainMessageLoop E:\src\chromium\src\content\browser\browser\_main\_loop.cc:1038  

#21 0x7ffcba2ad0a3 in content::BrowserMainRunnerImpl::Run E:\src\chromium\src\content\browser\browser\_main\_runner\_impl.cc:153  

#22 0x7ffcba2a072f in content::BrowserMain E:\src\chromium\src\content\browser\browser\_main.cc:30  

#23 0x7ffcbc3eb22e in content::RunBrowserProcessMain E:\src\chromium\src\content\app\content\_main\_runner\_impl.cc:646  

#24 0x7ffcbc3ee3e3 in content::ContentMainRunnerImpl::RunBrowser E:\src\chromium\src\content\app\content\_main\_runner\_impl.cc:1160  

#25 0x7ffcbc3ed511 in content::ContentMainRunnerImpl::Run E:\src\chromium\src\content\app\content\_main\_runner\_impl.cc:1026  

#26 0x7ffcbc3e92bf in content::RunContentProcess E:\src\chromium\src\content\app\content\_main.cc:398  

#27 0x7ffcbc3ea327 in content::ContentMain E:\src\chromium\src\content\app\content\_main.cc:426

SUMMARY: AddressSanitizer: heap-use-after-free E:\src\chromium\src\ui\accessibility\platform\inspect\ax\_event\_recorder.cc:24 in ui::AXEventRecorder::OnEvent  

Shadow bytes around the buggy address:  

0x04331df664e0: fa fa fd fd fd fd fd fd fd fd fd fd fa fa fa fa  

0x04331df664f0: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fd fd  

0x04331df66500: fd fd fd fd fd fd fd fd fa fa fa fa fd fd fd fd  

0x04331df66510: fd fd fd fd fd fa fa fa fa fa fd fd fd fd fd fd  

0x04331df66520: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fd  

=>0x04331df66530: fd fa fa fa fa fa fd fd fd fd[fd]fd fd fd fd fa  

0x04331df66540: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fa fa  

0x04331df66550: fa fa fd fd fd fd fd fd fd fd fd fd fa fa fa fa  

0x04331df66560: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fd fd  

0x04331df66570: fd fd fd fd fd fd fd fa fa fa fa fa fd fd fd fd  

0x04331df66580: fd fd fd fd fd fa fa fa fa fa fd fd fd fd fd fd  

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

==11216==ABORTING

**VERSION**  

Chrome Version: 98.0.4750.0 x64  

Operating System: windows 10 21h1  

credit information:

Zhihua Yao of KunLun Lab

## Attachments

- [demo.mp4](attachments/demo.mp4) (video/mp4, 5.1 MB)

## Timeline

### [Deleted User] (2021-12-07)

[Empty comment from Monorail migration]

### ha...@gmail.com (2021-12-07)

[0] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/web_contents/web_contents_impl.h;l=2105

WebContentsImpl own the  unique ptr ui::AXEventRecorder, and class AccessibilityEventRecorderWin  inheritance AccessibilityEventRecorder, AccessibilityEventRecorder inheritance ui::AXEventRecorder,while  WebContentsImpl destruction,ui::AXEventRecorder will be destroyed,so AccessibilityEventRecorderWin also will be destroyed.

[1] https://source.chromium.org/chromium/chromium/src/+/main:ui/accessibility/platform/inspect/ax_event_recorder.cc;l=24
void AXEventRecorder::OnEvent(const std::string& event) {
  base::AutoLock lock{on_event_lock_};
  event_logs_.push_back(event);
  if (callback_)
    callback_.Run(event);
} //UAF here

### do...@chromium.org (2021-12-07)

Can you please provide a repro POC or the video to help triage this properly?

[Monorail components: Internals>Accessibility]

### ha...@gmail.com (2021-12-07)

1.open the chrome://accessibility with Touch UI Layout
2.click "chrome://tab-strip.top-chrome/"  "star recording" button
3.choose Native accessibility API support options
4.UAF occurs

### do...@chromium.org (2021-12-08)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-12-14)

Sheriff ping: can owners please take a look at this issue and help triage, thanks

### me...@chromium.org (2021-12-16)

Adding labels. If Touch UI Layout is a requirement for this bug, it should be Impact=None.

hackyzh002: Does this trigger on Android without the "Touch UI Layout" flag?

### [Deleted User] (2021-12-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-17)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-17)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@google.com (2021-12-20)

@dlibby, you've been working on memory safety issues like this in the browser a11y code lately?

Are you interested in taking a look at this one?

### al...@chromium.org (2021-12-20)

[Empty comment from Monorail migration]

### me...@chromium.org (2021-12-20)

hackyzh002: Are you able to repro this in 96, with something other than chrome://tab-strip.top-chrome?

I'd like to make sure that this is indeed a release blocking regression. If we can get a repro in M96, that would be great.

### ha...@gmail.com (2021-12-20)

Sorry, because I only found this direction, if I find other ways to trigger this vulnerability, I think I will update it in time 

### as...@igalia.com (2021-12-21)

I attempted to remove the old hack which requires dependency on BrowserAccessibilityManager in win event recorder https://chromium-review.googlesource.com/c/chromium/src/+/3351225. Let's see if tests flakiness is not issue anymore and if so, the patch will be a fix for the bug.

### gi...@appspot.gserviceaccount.com (2021-12-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5884c1fd0971e0a446d03de1f112d6cd44258ce6

commit 5884c1fd0971e0a446d03de1f112d6cd44258ce6
Author: Alexander Surkov <asurkov@igalia.com>
Date: Tue Dec 21 18:41:38 2021

ax_inspect: let loose browser ax manager dependency in win event recorder

The hack was introduced in https://codereview.chromium.org/901183003
(crbug.com/440579) to mitigate dump accessibility event tests flakiness
caused by inconsistent AccessibleObjectFromWindow results. It is
a 6 years old hack and perhaps the issue self healed. At least it's
worth to give it a try.

Bug: 1277327
Change-Id: If2bd33b232da18093266b42fcd45aea0d0d41dd1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3351225
Reviewed-by: Aaron Leventhal <aleventhal@chromium.org>
Reviewed-by: Daniel Libby <dlibby@microsoft.com>
Commit-Queue: Alexander Surkkov <asurkov@igalia.com>
Cr-Commit-Position: refs/heads/main@{#953271}

[modify] https://crrev.com/5884c1fd0971e0a446d03de1f112d6cd44258ce6/content/browser/accessibility/accessibility_event_recorder_win.h
[modify] https://crrev.com/5884c1fd0971e0a446d03de1f112d6cd44258ce6/content/browser/accessibility/accessibility_event_recorder_win.cc


### as...@igalia.com (2021-12-23)

The patch https://chromium-review.googlesource.com/c/chromium/src/+/3351225 sticks, so the bug should be fixed by now.

### [Deleted User] (2021-12-23)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-23)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-23)

Requesting merge to dev M98 because latest trunk commit (953271) appears to be after dev branch point (950365).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-23)

Merge approved: your change passed merge requirements and is auto-approved for M98. Please go ahead and merge the CL to branch 4758 (refs/branch-heads/4758) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@gmail.com (2021-12-24)

This vulnerability can still be triggered 

### as...@igalia.com (2021-12-24)

Could you please file an updated stack trace? I wonder if this is the same issue or something similar to https://crbug.com/chromium/1277324.

### ha...@gmail.com (2021-12-24)

=================================================================
==11892==ERROR: AddressSanitizer: heap-use-after-free on address 0x11cb6ba1abd8 at pc 0x7fffb169c7fa bp 0x000d3c7fe060 sp 0x000d3c7fe0a8
READ of size 8 at 0x11cb6ba1abd8 thread T0
==11892==WARNING: Failed to use and restart external symbolizer!
    #0 0x7fffb169c7f9 in std::__1::vector<std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> >,std::__1::allocator<std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> > > >::push_back C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\vector:1637
    #1 0x7fffb46217fc in ui::AXEventRecorder::OnEvent C:\b\s\w\ir\cache\builder\src\ui\accessibility\platform\inspect\ax_event_recorder.cc:21
    #2 0x7fffb62d72c3 in content::AccessibilityEventRecorderWin::OnWinEventHook C:\b\s\w\ir\cache\builder\src\content\browser\accessibility\accessibility_event_recorder_win.cc:337
    #3 0x7fffb62d2b1c in content::AccessibilityEventRecorderWin::WinEventHookThunk C:\b\s\w\ir\cache\builder\src\content\browser\accessibility\accessibility_event_recorder_win.cc:98
    #4 0x7ff852d1c7f5 in RemovePropW+0x135 (C:\WINDOWS\System32\user32.dll+0x18002c7f5)
    #5 0x7ff854a86c13 in KiUserCallbackDispatcher+0x23 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800a6c13)
    #6 0x7ff8521219b3 in NtUserNotifyWinEvent+0x13 (C:\WINDOWS\System32\win32u.dll+0x1800019b3)
    #7 0x7ff852d1b3cb in NotifyWinEvent+0xfb (C:\WINDOWS\System32\user32.dll+0x18002b3cb)
    #8 0x7fffb631322c in content::BrowserAccessibilityManagerWin::OnSubtreeWillBeDeleted C:\b\s\w\ir\cache\builder\src\content\browser\accessibility\browser_accessibility_manager_win.cc:717
    #9 0x7fffbd5c4221 in ui::AXTree::NotifySubtreeWillBeReparentedOrDeleted C:\b\s\w\ir\cache\builder\src\ui\accessibility\ax_tree.cc:1713
    #10 0x7fffbd5bf5c5 in ui::AXTree::Unserialize C:\b\s\w\ir\cache\builder\src\ui\accessibility\ax_tree.cc:1050
    #11 0x7fffb5049146 in content::BrowserAccessibilityManager::Unserialize C:\b\s\w\ir\cache\builder\src\content\browser\accessibility\browser_accessibility_manager.cc:225
    #12 0x7fffb504a8a4 in content::BrowserAccessibilityManager::OnAccessibilityEvents C:\b\s\w\ir\cache\builder\src\content\browser\accessibility\browser_accessibility_manager.cc:460
    #13 0x7fffb5d3a13f in content::RenderFrameHostImpl::HandleAXEvents C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_impl.cc:7250
    #14 0x7fffb506330c in base::internal::Invoker<base::internal::BindState<void (content::RenderFrameHostImpl::*)(const ui::AXTreeID &, mojo::StructPtr<content::mojom::AXUpdatesAndEvents>, int),base::WeakPtr<content::RenderFrameHostImpl>,ui::AXTreeID,mojo::StructPtr<content::mojom::AXUpdatesAndEvents>,int>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:741
    #15 0x7fffbebd514f in base::`anonymous namespace'::PostTaskAndReplyRelay::RunTaskAndPostReply C:\b\s\w\ir\cache\builder\src\base\threading\post_task_and_reply_impl.cc:100
    #16 0x7fffbebd5993 in base::internal::Invoker<base::internal::BindState<void (*)(base::(anonymous namespace)::PostTaskAndReplyRelay),base::(anonymous namespace)::PostTaskAndReplyRelay>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:741
    #17 0x7fffbc0a0df4 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:135
    #18 0x7fffbebdaff5 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:356
    #19 0x7fffbebda6c8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:261
    #20 0x7fffbc148c46 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:220
    #21 0x7fffbc146ed8 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78
    #22 0x7fffbebdc6c1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:468
    #23 0x7fffbc01f963 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:140
    #24 0x7fffb523fe41 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1048
    #25 0x7fffb5245261 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:153
    #26 0x7fffb52394c9 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:30
    #27 0x7fffb7cc9313 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:646
    #28 0x7fffb7ccc353 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1160
    #29 0x7fffb7ccb486 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1026
    #30 0x7fffb7cc775d in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:398
    #31 0x7fffb7cc87e8 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:426
    #32 0x7fffb158148e in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:177
    #33 0x7ff663905b85 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:169
    #34 0x7ff663902b5f in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:382
    #35 0x7ff663d0753f in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #36 0x7ff85382134f in BaseThreadInitThunk+0xf (C:\WINDOWS\System32\KERNEL32.DLL+0x18001134f)
    #37 0x7ff854a31e77 in RtlUserThreadStart+0x27 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180051e77)

0x11cb6ba1abd8 is located 56 bytes inside of 96-byte region [0x11cb6ba1aba0,0x11cb6ba1ac00)
freed by thread T0 here:
    #0 0x7ff6639b23fb in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7fffb62da993 in content::AccessibilityEventRecorderWin::~AccessibilityEventRecorderWin C:\b\s\w\ir\cache\builder\src\content\browser\accessibility\accessibility_event_recorder_win.cc:136
    #2 0x7fffb6118176 in content::WebContentsImpl::~WebContentsImpl C:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.cc:1087
    #3 0x7fffb618c7b7 in content::WebContentsImpl::~WebContentsImpl C:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.cc:989
    #4 0x7fffc5ebb904 in views::WebView::SetWebContents C:\b\s\w\ir\cache\builder\src\ui\views\controls\webview\webview.cc:106
    #5 0x7fffc5ebb6ee in views::WebView::~WebView C:\b\s\w\ir\cache\builder\src\ui\views\controls\webview\webview.cc:74
    #6 0x7fffc5ebf593 in views::WebView::~WebView C:\b\s\w\ir\cache\builder\src\ui\views\controls\webview\webview.cc:72
    #7 0x7fffbbdd49cd in views::View::~View C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:253
    #8 0x7fffc5f3a495 in WebUITabStripContainerView::~WebUITabStripContainerView C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\webui_tab_strip_container_view.cc:494
    #9 0x7fffc1c5d65d in BrowserView::MaybeInitializeWebUITabStrip C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_view.cc:3461
    #10 0x7fffb45d8a56 in ui::AXPlatformNode::NotifyAddAXModeFlags C:\b\s\w\ir\cache\builder\src\ui\accessibility\platform\ax_platform_node.cc:105
    #11 0x7fffb4672273 in ui::AXPlatformNodeWin::get_states C:\b\s\w\ir\cache\builder\src\ui\accessibility\platform\ax_platform_node_win.cc:1270
    #12 0x7fffb62d4536 in content::AccessibilityEventRecorderWin::OnWinEventHook C:\b\s\w\ir\cache\builder\src\content\browser\accessibility\accessibility_event_recorder_win.cc:248
    #13 0x7fffb62d2b1c in content::AccessibilityEventRecorderWin::WinEventHookThunk C:\b\s\w\ir\cache\builder\src\content\browser\accessibility\accessibility_event_recorder_win.cc:98
    #14 0x7ff852d1c7f5 in RemovePropW+0x135 (C:\WINDOWS\System32\user32.dll+0x18002c7f5)
    #15 0x7ff854a86c13 in KiUserCallbackDispatcher+0x23 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800a6c13)
    #16 0x7ff8521219b3 in NtUserNotifyWinEvent+0x13 (C:\WINDOWS\System32\win32u.dll+0x1800019b3)
    #17 0x7ff852d1b3cb in NotifyWinEvent+0xfb (C:\WINDOWS\System32\user32.dll+0x18002b3cb)
    #18 0x7fffb631322c in content::BrowserAccessibilityManagerWin::OnSubtreeWillBeDeleted C:\b\s\w\ir\cache\builder\src\content\browser\accessibility\browser_accessibility_manager_win.cc:717
    #19 0x7fffbd5c4221 in ui::AXTree::NotifySubtreeWillBeReparentedOrDeleted C:\b\s\w\ir\cache\builder\src\ui\accessibility\ax_tree.cc:1713
    #20 0x7fffbd5bf5c5 in ui::AXTree::Unserialize C:\b\s\w\ir\cache\builder\src\ui\accessibility\ax_tree.cc:1050
    #21 0x7fffb5049146 in content::BrowserAccessibilityManager::Unserialize C:\b\s\w\ir\cache\builder\src\content\browser\accessibility\browser_accessibility_manager.cc:225
    #22 0x7fffb504a8a4 in content::BrowserAccessibilityManager::OnAccessibilityEvents C:\b\s\w\ir\cache\builder\src\content\browser\accessibility\browser_accessibility_manager.cc:460
    #23 0x7fffb5d3a13f in content::RenderFrameHostImpl::HandleAXEvents C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_impl.cc:7250
    #24 0x7fffb506330c in base::internal::Invoker<base::internal::BindState<void (content::RenderFrameHostImpl::*)(const ui::AXTreeID &, mojo::StructPtr<content::mojom::AXUpdatesAndEvents>, int),base::WeakPtr<content::RenderFrameHostImpl>,ui::AXTreeID,mojo::StructPtr<content::mojom::AXUpdatesAndEvents>,int>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:741
    #25 0x7fffbebd514f in base::`anonymous namespace'::PostTaskAndReplyRelay::RunTaskAndPostReply C:\b\s\w\ir\cache\builder\src\base\threading\post_task_and_reply_impl.cc:100
    #26 0x7fffbebd5993 in base::internal::Invoker<base::internal::BindState<void (*)(base::(anonymous namespace)::PostTaskAndReplyRelay),base::(anonymous namespace)::PostTaskAndReplyRelay>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:741
    #27 0x7fffbc0a0df4 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:135

previously allocated by thread T0 here:
    #0 0x7ff6639b24fb in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7fffce861c7e in operator new d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:35
    #2 0x7fffb4dd10b1 in content::AXInspectFactory::CreateRecorder C:\b\s\w\ir\cache\builder\src\content\public\browser\ax_inspect_factory_win.cc:75
    #3 0x7fffb4dd0e6d in content::AXInspectFactory::CreatePlatformRecorder C:\b\s\w\ir\cache\builder\src\content\public\browser\ax_inspect_factory_win.cc:30
    #4 0x7fffb6146f71 in content::WebContentsImpl::RecordAccessibilityEvents C:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.cc:4365
    #5 0x7fffc1aab2fa in AccessibilityUIMessageHandler::RequestAccessibilityEvents C:\b\s\w\ir\cache\builder\src\chrome\browser\accessibility\accessibility_ui.cc:737
    #6 0x7fffb628971d in content::WebUIImpl::ProcessWebUIMessage C:\b\s\w\ir\cache\builder\src\content\browser\webui\web_ui_impl.cc:296
    #7 0x7fffb6285aee in content::WebUIImpl::Send C:\b\s\w\ir\cache\builder\src\content\browser\webui\web_ui_impl.cc:113
    #8 0x7fffb454bf1c in content::mojom::WebUIHostStubDispatch::Accept C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\content\common\web_ui.mojom.cc:159
    #9 0x7fffbc3ed789 in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:900
    #10 0x7fffbed21af2 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43
    #11 0x7fffbc3f0f94 in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:657
    #12 0x7fffbcc7f8bb in IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnEndpointThread C:\b\s\w\ir\cache\builder\src\ipc\ipc_mojo_bootstrap.cc:1008
    #13 0x7fffbcc794d7 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message),scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:741
    #14 0x7fffbc0a0df4 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:135
    #15 0x7fffbebdaff5 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:356
    #16 0x7fffbebda6c8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:261
    #17 0x7fffbc148c46 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:220
    #18 0x7fffbc146ed8 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78
    #19 0x7fffbebdc6c1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:468
    #20 0x7fffbc01f963 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:140
    #21 0x7fffb523fe41 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1048
    #22 0x7fffb5245261 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:153
    #23 0x7fffb52394c9 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:30
    #24 0x7fffb7cc9313 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:646
    #25 0x7fffb7ccc353 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1160
    #26 0x7fffb7ccb486 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1026
    #27 0x7fffb7cc775d in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:398

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\vector:1637 in std::__1::vector<std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> >,std::__1::allocator<std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> > > >::push_back
Shadow bytes around the buggy address:
  0x03f4d8dc3520: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x03f4d8dc3530: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x03f4d8dc3540: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x03f4d8dc3550: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x03f4d8dc3560: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fa
=>0x03f4d8dc3570: fa fa fa fa fd fd fd fd fd fd fd[fd]fd fd fd fd
  0x03f4d8dc3580: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x03f4d8dc3590: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x03f4d8dc35a0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x03f4d8dc35b0: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 00
  0x03f4d8dc35c0: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 00
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
==11892==ABORTING

### ha...@gmail.com (2021-12-24)

The stack is a bit different 

### as...@igalia.com (2021-12-27)

This one is interesting. It turns out that AccessibilityEventRecorderWin kills itself during AccessibilityEventRecorderWin::OnWinEventHook handling. In particular AccessibilityEventRecorderWin instance is destroyed while calling into iaccessible2->get_states(&ia2_state); It is the very same issue I commented in 1277324#c13. I suppose we can have a host fix which will check if AccessibilityEventRecorderWin got destroyed after iaccessible2->get_states call but the real issue is iaccessible2->get_states shouldn't destroy anything.

### as...@igalia.com (2021-12-27)

here's a hot fix 3358735: ax_inspect: safety check for the windows event recorder event processing | https://chromium-review.googlesource.com/c/chromium/src/+/3358735

### [Deleted User] (2021-12-27)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-12-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1887890ad91c39748535fa073648a281370205f3

commit 1887890ad91c39748535fa073648a281370205f3
Author: Alexander Surkov <asurkov@igalia.com>
Date: Tue Dec 28 19:51:27 2021

ax_inspect: safety check for the windows event recorder event processing

The windows event recorder can be killed on the run during
IA2::get_states call. Add a null check.

Bug: 1277327
Change-Id: I2df080a60f4cf6ca2c6e9afda29374eeff128b5b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3358735
Reviewed-by: Nektarios Paisios <nektar@chromium.org>
Commit-Queue: Alexander Surkkov <asurkov@igalia.com>
Cr-Commit-Position: refs/heads/main@{#954337}

[modify] https://crrev.com/1887890ad91c39748535fa073648a281370205f3/content/browser/accessibility/accessibility_event_recorder_win.cc


### as...@igalia.com (2021-12-28)

should be fixed now, please feel free to reopen it if you can reproduce (please provide a stack trace if so).

### ha...@gmail.com (2021-12-29)

Thanks,I have no way to reproduce it at the moment 

### [Deleted User] (2021-12-31)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2022-01-07)

This issue has been approved for merge to M98, we are cutting beta RC build today end of the day for a release on Monday . Please help complete your merges asap so this change can bake in beta at the earliest. 

### sr...@google.com (2022-01-07)

asurkov@ can you pls help merge to M98 asap  , looks like there are 2 CL's needed to merge

### al...@chromium.org (2022-01-07)

Alex is back on Monday.

### as...@igalia.com (2022-01-10)

These two CL's are independent on each other and can be backported independently.
https://chromium-review.googlesource.com/c/chromium/src/+/3358735 (let loose browser ax manager dependency in win event recorder)
https://chromium-review.googlesource.com/c/chromium/src/+/3351225 (safety check for the windows event recorder event processing)

I never did merging myself before. Any guidance please?

### al...@chromium.org (2022-01-10)

See https://chromium.googlesource.com/chromium/src/+/HEAD/docs/process/merge_request.md

### as...@igalia.com (2022-01-10)

[Comment Deleted]

### as...@igalia.com (2022-01-10)

1) Why does your merge fit within the merge criteria for these milestones (Chrome Browser, Chrome OS)?
the sec issue
2) What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/chromium/src/+/3358735 (let loose browser ax manager dependency in win event recorder)
https://chromium-review.googlesource.com/c/chromium/src/+/3351225 (safety check for the windows event recorder event processing)
3) Have the changes been released and tested on canary?
yes
4) Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
no

### as...@igalia.com (2022-01-10)

apparently I have merge-approved label, sorry for the spam

### gi...@appspot.gserviceaccount.com (2022-01-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1a3d7fb8a365f10b1f9f6ccc7266bde871ec76ae

commit 1a3d7fb8a365f10b1f9f6ccc7266bde871ec76ae
Author: Alexander Surkov <asurkov@igalia.com>
Date: Mon Jan 10 18:19:31 2022

ax_inspect: safety check for the windows event recorder event processing

The windows event recorder can be killed on the run during
IA2::get_states call. Add a null check.

(cherry picked from commit 1887890ad91c39748535fa073648a281370205f3)

Bug: 1277327
Change-Id: I2df080a60f4cf6ca2c6e9afda29374eeff128b5b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3358735
Reviewed-by: Nektarios Paisios <nektar@chromium.org>
Commit-Queue: Alexander Surkkov <asurkov@igalia.com>
Cr-Original-Commit-Position: refs/heads/main@{#954337}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3377589
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Reviewed-by: Aaron Leventhal <aleventhal@chromium.org>
Commit-Queue: Aaron Leventhal <aleventhal@chromium.org>
Cr-Commit-Position: refs/branch-heads/4758@{#468}
Cr-Branched-From: 4a2cf4baf90326df19c3ee70ff987960d59a386e-refs/heads/main@{#950365}

[modify] https://crrev.com/1a3d7fb8a365f10b1f9f6ccc7266bde871ec76ae/content/browser/accessibility/accessibility_event_recorder_win.cc


### gi...@appspot.gserviceaccount.com (2022-01-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9a34f1f062ddd96889955743d8eaf6f6f05b3305

commit 9a34f1f062ddd96889955743d8eaf6f6f05b3305
Author: Alexander Surkov <asurkov@igalia.com>
Date: Mon Jan 10 18:30:21 2022

ax_inspect: let loose browser ax manager dependency in win event recorder

The hack was introduced in https://codereview.chromium.org/901183003
(crbug.com/440579) to mitigate dump accessibility event tests flakiness
caused by inconsistent AccessibleObjectFromWindow results. It is
a 6 years old hack and perhaps the issue self healed. At least it's
worth to give it a try.

(cherry picked from commit 5884c1fd0971e0a446d03de1f112d6cd44258ce6)

Bug: 1277327
Change-Id: If2bd33b232da18093266b42fcd45aea0d0d41dd1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3351225
Reviewed-by: Aaron Leventhal <aleventhal@chromium.org>
Reviewed-by: Daniel Libby <dlibby@microsoft.com>
Commit-Queue: Alexander Surkkov <asurkov@igalia.com>
Cr-Original-Commit-Position: refs/heads/main@{#953271}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3378025
Commit-Queue: Aaron Leventhal <aleventhal@chromium.org>
Cr-Commit-Position: refs/branch-heads/4758@{#469}
Cr-Branched-From: 4a2cf4baf90326df19c3ee70ff987960d59a386e-refs/heads/main@{#950365}

[modify] https://crrev.com/9a34f1f062ddd96889955743d8eaf6f6f05b3305/content/browser/accessibility/accessibility_event_recorder_win.h
[modify] https://crrev.com/9a34f1f062ddd96889955743d8eaf6f6f05b3305/content/browser/accessibility/accessibility_event_recorder_win.cc


### gi...@appspot.gserviceaccount.com (2022-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d0f4da375838e3b0ba0dc23d5ea917e56194ae23

commit d0f4da375838e3b0ba0dc23d5ea917e56194ae23
Author: Alexander Surkov <asurkov@igalia.com>
Date: Tue Jan 11 17:22:15 2022

ax_inspect: no content dependency for win event recorder

Bug: 1277327
Change-Id: Ideef60b4bcae27286324dc8211fe75e07d146b22
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3354915
Reviewed-by: Nektarios Paisios <nektar@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: Alexander Surkkov <asurkov@igalia.com>
Cr-Commit-Position: refs/heads/main@{#957600}

[modify] https://crrev.com/d0f4da375838e3b0ba0dc23d5ea917e56194ae23/ui/accessibility/platform/ax_platform_node_win.h
[modify] https://crrev.com/d0f4da375838e3b0ba0dc23d5ea917e56194ae23/content/public/browser/ax_inspect_factory_win.cc
[modify] https://crrev.com/d0f4da375838e3b0ba0dc23d5ea917e56194ae23/content/browser/accessibility/accessibility_event_recorder_win.h
[modify] https://crrev.com/d0f4da375838e3b0ba0dc23d5ea917e56194ae23/content/browser/accessibility/accessibility_event_recorder_win.cc
[modify] https://crrev.com/d0f4da375838e3b0ba0dc23d5ea917e56194ae23/content/browser/accessibility/browser_accessibility_com_win.h


### [Deleted User] (2022-01-13)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-02-01)

[Empty comment from Monorail migration]

### rz...@google.com (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-02-02)

1. Number of CLs needed for this fix and links to them.
2 CLs, https://crrev.com/c/3431000 and https://crrev.com/c/3430345/1

2. Level of complexity (High, Medium, Low - Explain)
Low, conflict on differences on removed lines from AccessibleObjectFromWindowWrapper.

3. Has this been merged to a stable release? beta release?
Yes, 98

4. Overall Recommendation (Yes, No)
Yes

### gm...@google.com (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-02-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1db00d254f6a12eb9594b0e043e2f4a790f80381

commit 1db00d254f6a12eb9594b0e043e2f4a790f80381
Author: Alexander Surkov <asurkov@igalia.com>
Date: Thu Feb 03 12:24:02 2022

[M96-LTS] ax_inspect: let loose browser ax manager dependency in win event recorder

M96 merge issues:
  accessibility_event_recorder_win.cc
   Removed method AccessibleObjectFromWindowWrapper has different comments on main
   which caused a conflict.

The hack was introduced in https://codereview.chromium.org/901183003
(crbug.com/440579) to mitigate dump accessibility event tests flakiness
caused by inconsistent AccessibleObjectFromWindow results. It is
a 6 years old hack and perhaps the issue self healed. At least it's
worth to give it a try.

(cherry picked from commit 5884c1fd0971e0a446d03de1f112d6cd44258ce6)

Bug: 1277327
Change-Id: If2bd33b232da18093266b42fcd45aea0d0d41dd1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3351225
Commit-Queue: Alexander Surkkov <asurkov@igalia.com>
Cr-Original-Commit-Position: refs/heads/main@{#953271}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3431000
Reviewed-by: Jana Grill <janagrill@google.com>
Owners-Override: Jana Grill <janagrill@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1438}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/1db00d254f6a12eb9594b0e043e2f4a790f80381/content/browser/accessibility/accessibility_event_recorder_win.h
[modify] https://crrev.com/1db00d254f6a12eb9594b0e043e2f4a790f80381/content/browser/accessibility/accessibility_event_recorder_win.cc


### rz...@google.com (2022-02-03)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-02-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/599e658a9d7768b913e958b894b0c8c8e2bcdd0b

commit 599e658a9d7768b913e958b894b0c8c8e2bcdd0b
Author: Alexander Surkov <asurkov@igalia.com>
Date: Thu Feb 03 14:38:51 2022

[M96-LTS] ax_inspect: safety check for the windows event recorder event processing

The windows event recorder can be killed on the run during
IA2::get_states call. Add a null check.

(cherry picked from commit 1887890ad91c39748535fa073648a281370205f3)

Bug: 1277327
Change-Id: I2df080a60f4cf6ca2c6e9afda29374eeff128b5b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3358735
Commit-Queue: Alexander Surkkov <asurkov@igalia.com>
Cr-Original-Commit-Position: refs/heads/main@{#954337}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3430345
Reviewed-by: Jana Grill <janagrill@google.com>
Owners-Override: Jana Grill <janagrill@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1441}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/599e658a9d7768b913e958b894b0c8c8e2bcdd0b/content/browser/accessibility/accessibility_event_recorder_win.cc


### am...@google.com (2022-02-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-11)

Congratulations on another one! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2022-02-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2022-09-26)

Crash no longer being reported. Issue presumed fixed

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1277327?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058146)*
