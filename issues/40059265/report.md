# Security: heap-use-after-free in content::WebContentsViewAura::StartDragging

| Field | Value |
|-------|-------|
| **Issue ID** | [40059265](https://issues.chromium.org/issues/40059265) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Portals |
| **Platforms** | Windows |
| **Reporter** | st...@gmail.com |
| **Assignee** | mc...@chromium.org |
| **Created** | 2022-03-31 |
| **Bounty** | $15,000.00 |

## Description

**VULNERABILITY DETAILS**

1. User drags any draggable content on the page
2. The portal is activated and adopts its predecessor, which destroys the originating |aura::Window|
3. When the user finishes or cancels the drag, |content::WebContentsViewAura::StartDragging| uses the destroyed |aura::Window|, causing a UAF.

**VERSION**  

Chrome Version: 102.0.4977.0  

Operating System: Windows 10

**REPRODUCTION CASE**

1. python3 -m http.server 9000
2. chrome --enable-features=Portals <http://localhost:9000/poc.html>
3. Drag anything on the page

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: browser Crash State:

==18336==ERROR: AddressSanitizer: heap-use-after-free on address 0x12a7638608d0 at pc 0x7ffc56c6d0da bp 0x009cbfdfe360 sp 0x009cbfdfe3a8  

READ of size 1 at 0x12a7638608d0 thread T0  

==18336==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ffc56c6d0d9 in content::WebContentsViewAura::StartDragging C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_view\_aura.cc:1207  

#1 0x7ffc569005b8 in content::RenderWidgetHostImpl::StartDragging C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_widget\_host\_impl.cc:2841  

#2 0x7ffc549ad24c in blink::mojom::FrameWidgetHostStubDispatch::Accept C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\third\_party\blink\public\mojom\page\widget.mojom.cc:3121  

#3 0x7ffc5d3cb8ec in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:922  

#4 0x7ffc60074922 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:43  

#5 0x7ffc5d3cf534 in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:664  

#6 0x7ffc5dd0ba8f in IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnEndpointThread C:\b\s\w\ir\cache\builder\src\ipc\ipc\_mojo\_bootstrap.cc:1010  

#7 0x7ffc5dd056cb in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message),scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:748  

#8 0x7ffc5d09b214 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#9 0x7ffc5ff4f505 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:386  

#10 0x7ffc5ff4eaf9 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:291  

#11 0x7ffc5d14dd16 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:214  

#12 0x7ffc5d14c058 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#13 0x7ffc5ff50c70 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:498  

#14 0x7ffc5d019803 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#15 0x7ffc55ca0e8b in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1067  

#16 0x7ffc55ca6313 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:155  

#17 0x7ffc55c9a2e9 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:30  

#18 0x7ffc5cc47693 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:640  

#19 0x7ffc5cc4a80c in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1147  

#20 0x7ffc5cc4993e in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1019  

#21 0x7ffc5cc4630b in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:407  

#22 0x7ffc5cc46a94 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:435  

#23 0x7ffc51b314ca in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:176  

#24 0x7ff7a17a5b16 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:167  

#25 0x7ff7a17a2b5f in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#26 0x7ff7a1b9db2b in \_\_scrt\_common\_main\_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#27 0x7ffd06b77033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#28 0x7ffd077c2650 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

0x12a7638608d0 is located 208 bytes inside of 240-byte region [0x12a763860800,0x12a7638608f0)  

freed by thread T0 here:  

#0 0x7ff7a184e89b in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ffc56c74759 in content::WebContentsViewAura::~WebContentsViewAura C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_view\_aura.cc:703  

#2 0x7ffc56bf63dc in content::WebContentsImpl::AttachInnerWebContents C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.cc:2461  

#3 0x7ffc564f3e56 in content::Portal::CreateProxyAndAttachPortal C:\b\s\w\ir\cache\builder\src\content\browser\portal\portal.cc:169  

#4 0x7ffc567f34d7 in content::RenderFrameHostImpl::AdoptPortal C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc:7176  

#5 0x7ffc54ea5981 in content::mojom::FrameHostStubDispatch::AcceptWithResponder C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\content\common\frame.mojom.cc:6126  

#6 0x7ffc5683e40e in content::mojom::FrameHostStub<mojo::RawPtrImplRefTraits[content::mojom::FrameHost](javascript:void(0);) >::AcceptWithResponder C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\content\common\frame.mojom.h:702  

#7 0x7ffc5d3cb88b in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:884  

#8 0x7ffc60074835 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:48  

#9 0x7ffc5d3cf534 in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:664  

#10 0x7ffc5dd0b43e in IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptSyncMessage C:\b\s\w\ir\cache\builder\src\ipc\ipc\_mojo\_bootstrap.cc:1050  

#11 0x7ffc5d09b214 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#12 0x7ffc5ff4f505 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:386  

#13 0x7ffc5ff4eaf9 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:291  

#14 0x7ffc5d14c6b3 in base::MessagePumpForUI::MessageCallback C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:172  

#15 0x7ffc5d172638 in base::win::MessageWindow::WindowProc C:\b\s\w\ir\cache\builder\src\base\win\message\_window.cc:162  

#16 0x7ffc5d171c0e in base::win::WrappedWindowProc<&base::win::MessageWindow::WindowProc> C:\b\s\w\ir\cache\builder\src\base\win\wrapped\_window\_proc.h:74  

#17 0x7ffd0759e857 in CallWindowProcW+0x3f7 (C:\WINDOWS\System32\user32.dll+0x18000e857)  

#18 0x7ffd0759e298 in DispatchMessageW+0x258 (C:\WINDOWS\System32\user32.dll+0x18000e298)  

#19 0x7ffd06a5a11f in OleGetPackageClipboardOwner+0xaf2f (C:\WINDOWS\System32\ole32.dll+0x18008a11f)  

#20 0x7ffd06a5c90d in DoDragDrop+0xfd (C:\WINDOWS\System32\ole32.dll+0x18008c90d)  

#21 0x7ffc66c63b21 in views::DesktopDragDropClientWin::StartDragAndDrop C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop\_aura\desktop\_drag\_drop\_client\_win.cc:75  

#22 0x7ffc56c6cb84 in content::WebContentsViewAura::StartDragging C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_view\_aura.cc:1188  

#23 0x7ffc569005b8 in content::RenderWidgetHostImpl::StartDragging C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_widget\_host\_impl.cc:2841  

#24 0x7ffc549ad24c in blink::mojom::FrameWidgetHostStubDispatch::Accept C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\third\_party\blink\public\mojom\page\widget.mojom.cc:3121  

#25 0x7ffc5d3cb8ec in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:922  

#26 0x7ffc60074922 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:43  

#27 0x7ffc5d3cf534 in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:664

previously allocated by thread T0 here:  

#0 0x7ff7a184e99b in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ffc6fac05de in operator new d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ffc56c6645c in content::CreateWebContentsView C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_view\_aura.cc:101  

#3 0x7ffc56bff232 in content::WebContentsImpl::Init C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.cc:3064  

#4 0x7ffc56bdc904 in content::WebContentsImpl::CreateWithOpener C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.cc:1167  

#5 0x7ffc56bdc328 in content::WebContentsImpl::Create C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.cc:593  

#6 0x7ffc56bdc231 in content::WebContents::Create C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.cc:588  

#7 0x7ffc5f68ba2f in Navigate C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser\_navigator.cc:711  

#8 0x7ffc61dc33ec in chrome::OpenCurrentURL C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser\_commands.cc:671  

#9 0x7ffc67760ea9 in ChromeOmniboxEditController::OnAutocompleteAccept C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\omnibox\chrome\_omnibox\_edit\_controller.cc:43  

#10 0x7ffc677a5d97 in OmniboxEditModel::OpenMatch C:\b\s\w\ir\cache\builder\src\components\omnibox\browser\omnibox\_edit\_model.cc:980  

#11 0x7ffc67793848 in OmniboxView::OpenMatch C:\b\s\w\ir\cache\builder\src\components\omnibox\browser\omnibox\_view.cc:175  

#12 0x7ffc677a3119 in OmniboxEditModel::AcceptInput C:\b\s\w\ir\cache\builder\src\components\omnibox\browser\omnibox\_edit\_model.cc:743  

#13 0x7ffc6778138d in OmniboxViewViews::HandleKeyEvent C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\omnibox\omnibox\_view\_views.cc:1590  

#14 0x7ffc5cd8b1a8 in views::Textfield::OnKeyPressed C:\b\s\w\ir\cache\builder\src\ui\views\controls\textfield\textfield.cc:711  

#15 0x7ffc5cdb9e68 in views::View::OnKeyEvent C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:1429  

#16 0x7ffc5ddb1f35 in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:190  

#17 0x7ffc5ddb1455 in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:139  

#18 0x7ffc5ddb0d3f in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:83  

#19 0x7ffc5ddb0980 in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:55  

#20 0x7ffc62c6f532 in ui::EventProcessor::OnEventFromSource C:\b\s\w\ir\cache\builder\src\ui\events\event\_processor.cc:49  

#21 0x7ffc5fb85c7f in ui::EventSource::DeliverEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:118  

#22 0x7ffc5fb858d9 in ui::EventSource::SendEventToSinkFromRewriter C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:143  

#23 0x7ffc5fb853db in ui::EventSource::SendEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:112  

#24 0x7ffc5cde357e in views::Widget::OnKeyEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1510  

#25 0x7ffc5ddb1f35 in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:190  

#26 0x7ffc5ddb1455 in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:139  

#27 0x7ffc5ddb0d3f in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:83

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_view\_aura.cc:1207 in content::WebContentsViewAura::StartDragging  

Shadow bytes around the buggy address:  

0x04da4fa8c0c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 fa  

0x04da4fa8c0d0: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

0x04da4fa8c0e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x04da4fa8c0f0: 00 00 fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x04da4fa8c100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x04da4fa8c110: fd fd fd fd fd fd fd fd fd fd[fd]fd fd fd fa fa  

0x04da4fa8c120: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

0x04da4fa8c130: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x04da4fa8c140: 00 fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x04da4fa8c150: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x04da4fa8c160: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==18336==ABORTING

**CREDIT INFORMATION**  

Reporter credit: Thomas Orlita

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 309 B)
- [portal.html](attachments/portal.html) (text/plain, 140 B)

## Timeline

### [Deleted User] (2022-03-31)

[Empty comment from Monorail migration]

### hc...@google.com (2022-04-01)

This at least crashes in 99 Stable, so marking it as such. 

starting triage with domenic@ because he has the last commit visible in https://github.com/WICG/portals

Marking as low severity because its behind a Feature flag and I can't find any evidence of the Feature flag being on by default in any finch trials.

[Monorail components: Blink>Portals]

### hc...@google.com (2022-04-01)

And by Stable i mean 100.0.4896.60, oops. 

### [Deleted User] (2022-04-01)

[Empty comment from Monorail migration]

### do...@chromium.org (2022-04-01)

I am not an appropriate owner for this; the Blink>Portals team should be able to triage if it is a portals bug.

### hc...@google.com (2022-04-01)

jbroman@ can you take a look?

### [Deleted User] (2022-04-01)

[Empty comment from Monorail migration]

### hc...@google.com (2022-04-04)

Switching severity and impact due to misunderstanding of what to do for features behind feature flags.

### hc...@google.com (2022-04-04)

[Empty comment from Monorail migration]

### da...@chromium.org (2022-04-05)

Portals is behind a flag still - and not enabled for any domains yet - so this is lower priority, right jbroman?

Is there a bug that should block on this?

### jb...@chromium.org (2022-04-05)

That's correct. Kevin looked at a similar issue recently related to the eye dropper also assuming an aura::Window was valid, so he might be able to quickly assess this -- but action isn't urgent here.

### mc...@chromium.org (2022-04-29)

It looks like this is due to the nested run loop in WebContentsViewAura::StartDragging. Portal activation and adoption occurs here and destroys `this`.

### mc...@chromium.org (2022-04-29)

CL: https://chromium-review.googlesource.com/c/chromium/src/+/3614254

### gi...@appspot.gserviceaccount.com (2022-05-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/81f80d1929966f4817db9fe76356c225aaa7ad55

commit 81f80d1929966f4817db9fe76356c225aaa7ad55
Author: Kevin McNee <mcnee@chromium.org>
Date: Thu May 05 22:58:22 2022

Check WebContentsViewAura validity after the drag and drop nested run loop

Portal activation and adoption destroys the previous
WebContentsViewAura. If this happens during a drag and drop nested run
loop, then WebContentsViewAura::StartDragging can continue running with
`this` being destroyed. We now handle the case of it being destroyed.

Bug: 1312144
Change-Id: Ibcfe1c4026dcf283717521927dc180150af144f7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3614254
Commit-Queue: Kevin McNee <mcnee@chromium.org>
Reviewed-by: Sadrul Chowdhury <sadrul@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1000142}

[modify] https://crrev.com/81f80d1929966f4817db9fe76356c225aaa7ad55/content/browser/web_contents/web_contents_view_aura.cc


### mc...@chromium.org (2022-05-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-06)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-05-24)

Congratulations, Thomas! The VRP Panel has decided to award you $10,000 for this report + $5,000 renderer bonus as this appears to be web accessible memory corruption of the browser process. Thank you for your efforts and nice work! 

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-06-21)

[Comment Deleted]

### am...@google.com (2022-06-21)

[Comment Deleted]

### am...@chromium.org (2022-06-21)

[Comment Deleted]

### am...@google.com (2022-07-14)

[Comment Deleted]

### am...@google.com (2022-07-28)

[Comment Deleted]

### [Deleted User] (2022-08-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-08-12)

This issue was migrated from crbug.com/chromium/1312144?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059265)*
