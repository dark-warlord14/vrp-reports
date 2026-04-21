# Security: UaF in TabSharingUI

| Field | Value |
|-------|-------|
| **Issue ID** | [40053503](https://issues.chromium.org/issues/40053503) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>MediaCapture |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | gu...@chromium.org |
| **Created** | 2020-10-05 |
| **Bounty** | $15,000.00 |

## Description

Chrome Version: 88.0.4283.0  

Operating System: Ubuntu

**REPRODUCTION CASE**

This is similar to <https://crbug.com/chromium/1074706>.

1. python ./copy\_mojo\_js\_bindings.py /path/to/chrome/.../out/asan/gen
2. python3.6m -m http.server 8605
3. Run chrome with --enable-blink-features=MojoJS
4. Open <http://127.0.0.1:8000/poc.html> and a new tab, on the first tab (poc.html) select "Chrome tab" in the pop-up dialog box, then try to share the new tab
5. Close the shared tab and wait => crash!

================================================================  

==8842==ERROR: AddressSanitizer: heap-use-after-free on address 0x61d000313a98 at pc 0x555563d8f865 bp 0x7fffffffccb0 sp 0x7fffffffcca8  

READ of size 8 at 0x61d000313a98 thread T0 (chrome)  

[Detaching after fork from child process 11310]  

#0 0x555563d8f864 in begin buildtools/third\_party/libc++/trunk/include/vector:1524:30  

#1 0x555563d8f864 in HasObserver base/observer\_list.h:303:36  

#2 0x555563d8f864 in AddObserver base/observer\_list.h:271:9  

#3 0x555563d8f864 in AddObserver content/browser/web\_contents/web\_contents\_impl.cc:784:14  

#4 0x555563d8f864 in content::WebContentsImpl::AddObserver(content::WebContentsObserver\*) content/browser/web\_contents/web\_contents\_impl.cc:2878:14  

#5 0x55556a0f7329 in WebContentsDeviceUsage chrome/browser/media/webrtc/media\_stream\_capture\_indicator.cc:135:9  

#6 0x55556a0f7329 in make\_unique<MediaStreamCaptureIndicator::WebContentsDeviceUsage, MediaStreamCaptureIndicator \*, content::WebContents \*&> buildtools/third\_party/libc++/trunk/include/memory:3043:32  

#7 0x55556a0f7329 in MediaStreamCaptureIndicator::RegisterMediaStream(content::WebContents\*, std::\_\_1::vector<blink::MediaStreamDevice, std::\_\_1::allocator[blink::MediaStreamDevice](javascript:void(0);) > const&, std::\_\_1::unique\_ptr<MediaStreamUI, std::\_\_1::default\_delete<MediaStreamUI> >) chrome/browser/media/webrtc/media\_stream\_capture\_indicator.cc:337:13  

#8 0x555573834da9 in TabSharingUIViews::CreateTabCaptureIndicator() chrome/browser/ui/views/tab\_sharing/tab\_sharing\_ui\_views.cc:306:37  

#9 0x555573834622 in TabSharingUIViews::OnStarted(base::OnceCallback<void ()>, base::RepeatingCallback<void (content::DesktopMediaID const&)>) chrome/browser/ui/views/tab\_sharing/tab\_sharing\_ui\_views.cc:148:3  

#10 0x55556a0fc148 in MediaStreamCaptureIndicator::UIDelegate::OnStarted(base::OnceCallback<void ()>, base::RepeatingCallback<void (content::DesktopMediaID const&)>) chrome/browser/media/webrtc/media\_stream\_capture\_indicator.cc:214:19  

#11 0x5555636ae83d in content::MediaStreamUIProxy::Core::OnStarted(long\*, bool) content/browser/renderer\_host/media/media\_stream\_ui\_proxy.cc:144:23  

#12 0x55556960d563 in Run base/callback.h:100:12  

#13 0x55556960d563 in base::(anonymous namespace)::PostTaskAndReplyRelay::RunTaskAndPostReply(base::(anonymous namespace)::PostTaskAndReplyRelay) base/threading/post\_task\_and\_reply\_impl.cc:97:28  

#14 0x55556960dd54 in Invoke<void (\*)(base::(anonymous namespace)::PostTaskAndReplyRelay), base::(anonymous namespace)::PostTaskAndReplyRelay> base/bind\_internal.h:393:12  

#15 0x55556960dd54 in MakeItSo<void (\*)(base::(anonymous namespace)::PostTaskAndReplyRelay), base::(anonymous namespace)::PostTaskAndReplyRelay> base/bind\_internal.h:637:12  

#16 0x55556960dd54 in RunImpl<void (\*)(base::(anonymous namespace)::PostTaskAndReplyRelay), std::\_\_1::tuple<base::(anonymous namespace)::PostTaskAndReplyRelay>, 0> base/bind\_internal.h:710:12  

#17 0x55556960dd54 in base::internal::Invoker<base::internal::BindState<void (\*)(base::(anonymous namespace)::PostTaskAndReplyRelay), base::(anonymous namespace)::PostTaskAndReplyRelay>, void ()>::RunOnce(base::internal::BindStateBase\*) base/bind\_internal.h:679:12  

#18 0x555569589985 in Run base/callback.h:100:12  

#19 0x555569589985 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/task/common/task\_annotator.cc:163:33  

#20 0x5555695c127f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:332:23  

#21 0x5555695c0aff in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:252:36  

#22 0x5555694bcb09 in HandleDispatch base/message\_loop/message\_pump\_glib.cc:374:46  

#23 0x5555694bcb09 in base::(anonymous namespace)::WorkSourceDispatch(\_GSource\*, int (\*)(void\*), void\*) base/message\_loop/message\_pump\_glib.cc:124:43  

#24 0x7ffff7e42fbc in g\_main\_context\_dispatch (/lib/x86\_64-linux-gnu/libglib-2.0.so.0+0x51fbc)

0x61d000313a98 is located 536 bytes inside of 2416-byte region [0x61d000313880,0x61d0003141f0)  

freed by thread T0 (chrome) here:  

#0 0x55555f1ae4ed in operator delete(void\*) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:160:3  

#1 0x555572eedee1 in operator() buildtools/third\_party/libc++/trunk/include/memory:2378:5  

#2 0x555572eedee1 in reset buildtools/third\_party/libc++/trunk/include/memory:2633:7  

#3 0x555572eedee1 in TabStripModel::SendDetachWebContentsNotifications(TabStripModel::DetachNotifications\*) chrome/browser/ui/tabs/tab\_strip\_model.cc:544:21  

#4 0x555572f08d48 in TabStripModel::CloseWebContentses(base::span<content::WebContents\* const, 18446744073709551615ul>, unsigned int) chrome/browser/ui/tabs/tab\_strip\_model.cc:1799:5  

#5 0x555572ef41d0 in TabStripModel::InternalCloseTabs(base::span<content::WebContents\* const, 18446744073709551615ul>, unsigned int) chrome/browser/ui/tabs/tab\_strip\_model.cc:1713:27  

#6 0x555572ef4951 in TabStripModel::CloseWebContentsAt(int, unsigned int) chrome/browser/ui/tabs/tab\_strip\_model.cc:741:10  

#7 0x55557388e057 in TabStrip::CloseTabInternal(int, CloseTabSource) chrome/browser/ui/views/tabs/tab\_strip.cc:2966:16  

#8 0x55557388d999 in TabStrip::CloseTab(Tab\*, CloseTabSource) chrome/browser/ui/views/tabs/tab\_strip.cc:1817:3  

#9 0x5555738b7bec in Tab::CloseButtonPressed(ui::Event const&) chrome/browser/ui/views/tabs/tab.cc:1040:16  

#10 0x5555710a7fcd in views::ButtonController::OnMouseReleased(ui::MouseEvent const&) ui/views/controls/button/button\_controller.cc  

#11 0x55557106c0a4 in ui::ScopedTargetHandler::OnEvent(ui::Event\*) ui/events/scoped\_target\_handler.cc:32:24  

#12 0x55556c8a61b9 in DispatchEvent ui/events/event\_dispatcher.cc:191:12  

#13 0x55556c8a61b9 in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:140:5  

#14 0x55556c8a5a81 in DispatchEventToTarget ui/events/event\_dispatcher.cc:84:14  

#15 0x55556c8a5a81 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:56:15  

#16 0x5555712331d6 in views::internal::RootView::OnMouseReleased(ui::MouseEvent const&) ui/views/widget/root\_view.cc:467:9  

#17 0x5555712537c5 in views::Widget::OnMouseEvent(ui::MouseEvent\*) ui/views/widget/widget.cc:1292:20  

#18 0x55556c8a61b9 in DispatchEvent ui/events/event\_dispatcher.cc:191:12  

#19 0x55556c8a61b9 in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:140:5  

#20 0x55556c8a5a81 in DispatchEventToTarget ui/events/event\_dispatcher.cc:84:14  

#21 0x55556c8a5a81 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:56:15  

#22 0x55556e887add in ui::EventProcessor::OnEventFromSource(ui::Event\*) ui/events/event\_processor.cc:49:17  

#23 0x55556e8a3a4f in ui::EventSource::DeliverEventToSink(ui::Event\*) ui/events/event\_source.cc:113:16  

#24 0x55556e8a366a in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const\*, ui::EventRewriter const\*) ui/events/event\_source.cc:138:12  

#25 0x5555712d7c07 in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event\*) ui/aura/window\_tree\_host\_platform.cc:238:38  

#26 0x5555712d2af7 in views::DesktopWindowTreeHostLinux::DispatchEvent(ui::Event\*) ui/views/widget/desktop\_aura/desktop\_window\_tree\_host\_linux.cc:242:29  

#27 0x55556d4435d5 in ui::X11Window::DispatchUiEvent(ui::Event\*, x11::Event\*) ui/platform\_window/x11/x11\_window.cc:661:34  

#28 0x55556d442b34 in ui::X11Window::DispatchEvent(ui::Event\* const&) ui/platform\_window/x11/x11\_window.cc:605:3  

#29 0x55556d4437ff in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event\* const&) ui/platform\_window/x11/x11\_window.cc  

#30 0x55556c557d24 in ui::PlatformEventSource::DispatchEvent(ui::Event\*) ui/events/platform/platform\_event\_source.cc:100:29  

#31 0x55556c9ce16d in ui::X11EventSource::DispatchPlatformEvent(ui::Event\* const&, x11::Event\*) ui/events/platform/x11/x11\_event\_source.cc:323:3  

#32 0x55556c9d0400 in ui::X11EventSource::ProcessXEvent(x11::Event\*) ui/events/platform/x11/x11\_event\_source.cc:384:5  

#33 0x55556c9d0ae9 in DispatchXEvent ui/events/platform/x11/x11\_event\_source.cc:453:3  

#34 0x55556c9d0ae9 in non-virtual thunk to ui::X11EventSource::DispatchXEvent(x11::Event\*) ui/events/platform/x11/x11\_event\_source.cc  

#35 0x55556c4e4ce8 in operator() ui/gfx/x/connection.cc:448:15  

#36 0x55556c4e4ce8 in x11::Connection::Dispatch(x11::Connection::Delegate\*) ui/gfx/x/connection.cc:475:7  

#37 0x55556c9dfe8b in ui::(anonymous namespace)::XSourceDispatch(\_GSource\*, int (\*)(void\*), void\*) ui/events/platform/x11/x11\_event\_watcher\_glib.cc:43:15

previously allocated by thread T0 (chrome) here:  

#0 0x55555f1adc8d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:99:3  

#1 0x555563d56359 in content::WebContentsImpl::CreateWithOpener(content::WebContents::CreateParams const&, content::RenderFrameHostImpl\*) content/browser/web\_contents/web\_contents\_impl.cc:1001:7  

#2 0x555563d560d8 in Create content/browser/web\_contents/web\_contents\_impl.cc:515:10  

#3 0x555563d560d8 in content::WebContents::Create(content::WebContents::CreateParams const&) content/browser/web\_contents/web\_contents\_impl.cc:510:10  

#4 0x555572e19bb4 in CreateTargetContents chrome/browser/ui/browser\_navigator.cc:436:7  

#5 0x555572e19bb4 in Navigate(NavigateParams\*) chrome/browser/ui/browser\_navigator.cc:630:28  

#6 0x555573431eb3 in BrowserRootView::OnPerformDrop(ui::DropTargetEvent const&) chrome/browser/ui/views/frame/browser\_root\_view.cc:252:3  

#7 0x5555712cc12e in views::DropHelper::OnDrop(ui::OSExchangeData const&, gfx::Point const&, int) ui/views/widget/drop\_helper.cc:98:21  

#8 0x5555712ec5f1 in OnPerformDrop ui/views/widget/desktop\_aura/desktop\_native\_widget\_aura.cc:1240:24  

#9 0x5555712ec5f1 in non-virtual thunk to views::DesktopNativeWidgetAura::OnPerformDrop(ui::DropTargetEvent const&, std::\_\_1::unique\_ptr<ui::OSExchangeData, std::\_\_1::default\_delete[ui::OSExchangeData](javascript:void(0);) >) ui/views/widget/desktop\_aura/desktop\_native\_widget\_aura.cc  

#10 0x55557130b1e5 in views::DesktopDragDropClientOzone::OnDragDrop(std::\_\_1::unique\_ptr<ui::OSExchangeData, std::\_\_1::default\_delete[ui::OSExchangeData](javascript:void(0);) >, int) ui/views/widget/desktop\_aura/desktop\_drag\_drop\_client\_ozone.cc:272:26  

#11 0x55556d44641f in PerformDrop ui/platform\_window/x11/x11\_window.cc:913:17  

#12 0x55556d44641f in non-virtual thunk to ui::X11Window::PerformDrop() ui/platform\_window/x11/x11\_window.cc  

#13 0x55556d44e449 in OnXdndDrop ui/base/x/x11\_drag\_drop\_client.cc:413:35  

#14 0x55556d44e449 in ui::XDragDropClient::HandleXdndEvent(x11::ClientMessageEvent const&) ui/base/x/x11\_drag\_drop\_client.cc:281:5  

#15 0x55556d4292ae in ui::XWindow::ProcessEvent(x11::Event\*) ui/base/x/x11\_window.cc  

#16 0x55556d44275c in DispatchXEvent ui/platform\_window/x11/x11\_window.cc:580:12  

#17 0x55556d44275c in non-virtual thunk to ui::X11Window::DispatchXEvent(x11::Event\*) ui/platform\_window/x11/x11\_window.cc  

#18 0x55556c9cf4a0 in ui::X11EventSource::DispatchXEventToXEventDispatchers(x11::Event\*) ui/events/platform/x11/x11\_event\_source.cc:342:22  

#19 0x55556c9d0417 in ui::X11EventSource::ProcessXEvent(x11::Event\*) ui/events/platform/x11/x11\_event\_source.cc:388:5  

#20 0x55556c9d0ae9 in DispatchXEvent ui/events/platform/x11/x11\_event\_source.cc:453:3  

#21 0x55556c9d0ae9 in non-virtual thunk to ui::X11EventSource::DispatchXEvent(x11::Event\*) ui/events/platform/x11/x11\_event\_source.cc  

#22 0x55556c4e4ce8 in operator() ui/gfx/x/connection.cc:448:15  

#23 0x55556c4e4ce8 in x11::Connection::Dispatch(x11::Connection::Delegate\*) ui/gfx/x/connection.cc:475:7  

#24 0x55556c9dfe8b in ui::(anonymous namespace)::XSourceDispatch(\_GSource\*, int (\*)(void\*), void\*) ui/events/platform/x11/x11\_event\_watcher\_glib.cc:43:15  

#25 0x7ffff7e42e8d in g\_main\_context\_dispatch (/lib/x86\_64-linux-gnu/libglib-2.0.so.0+0x51e8d)

SUMMARY: AddressSanitizer: heap-use-after-free buildtools/third\_party/libc++/trunk/include/vector:1524:30 in begin  

Shadow bytes around the buggy address:  

0x0c3a8005a700: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c3a8005a710: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3a8005a720: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3a8005a730: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3a8005a740: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x0c3a8005a750: fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3a8005a760: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3a8005a770: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3a8005a780: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3a8005a790: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3a8005a7a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

- [copy_mojo_js_bindings.py](attachments/copy_mojo_js_bindings.py) (text/plain, 514 B)
- [mojo_bindings.js](attachments/mojo_bindings.js) (text/plain, 162.8 KB)
- [poc.html](attachments/poc.html) (text/plain, 845 B)
- [screen.mp4](attachments/screen.mp4) (video/mp4, 5.4 MB)

## Timeline

### ch...@gmail.com (2020-10-05)

[Empty comment from Monorail migration]

### do...@chromium.org (2020-10-05)

+TabSharingUI and GetUserMedia folks, can you please take a look at this? Looks like it's in stable; a compromised renderer that can trigger UaF in the browser process is a High severity security issue.

[Monorail components: Blink>GetUserMedia>Desktop]

### gu...@chromium.org (2020-10-05)

agpalak@ 

[Monorail components: UI>Browser>TabCapture]

### gu...@chromium.org (2020-10-05)

agpalak@: Can you take a look?

### [Deleted User] (2020-10-05)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ag...@chromium.org (2020-10-06)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### ch...@gmail.com (2020-10-12)

Any update on this bug? Thanks!

### ag...@chromium.org (2020-10-13)

[Empty comment from Monorail migration]

### ag...@chromium.org (2020-10-13)

[Empty comment from Monorail migration]

### ch...@gmail.com (2020-10-14)

[Comment Deleted]

### gu...@chromium.org (2020-10-14)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/229fdaf8fc05e0eeadad380d401c191afd822d92

commit 229fdaf8fc05e0eeadad380d401c191afd822d92
Author: Guido Urdaneta <guidou@chromium.org>
Date: Wed Oct 14 19:40:12 2020

Validate input of MediaStreamDispatcherHost::OpenDevice()

This method forwards to MediaStreamManager::OpenDevice(), which
DCHECKs for the stream type to be device video or audio capture
(i.e., webcam or mic). However, MSDH admits other stream types,
which cause MSM::OpenDevice to hit this DCHECK.

This CL ensures that a message containing an incorrect stream type,
which could be sent by a malicious renderer, results in killing the
renderer process.

Bug: 1135018
Change-Id: I3884dde95d92c41f44966a8ab1dd7bdfd4b23b9b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2472397
Auto-Submit: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#817151}

[modify] https://crrev.com/229fdaf8fc05e0eeadad380d401c191afd822d92/content/browser/bad_message.h
[modify] https://crrev.com/229fdaf8fc05e0eeadad380d401c191afd822d92/content/browser/renderer_host/media/media_stream_dispatcher_host.cc
[modify] https://crrev.com/229fdaf8fc05e0eeadad380d401c191afd822d92/tools/metrics/histograms/enums.xml


### gu...@chromium.org (2020-10-14)

[Empty comment from Monorail migration]

### gu...@chromium.org (2020-10-14)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-15)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-15)

This bug requires manual review: M87's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
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
Owners: benmason@(Android), bindusuvarna @(iOS), cindyb@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@google.com (2020-10-16)

guidou@ - can you please address the merge questionnaire to consider this for M87? Thanks!

### ad...@google.com (2020-10-18)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-18)

[Empty comment from Monorail migration]

### gu...@chromium.org (2020-10-19)

[Empty comment from Monorail migration]

### gu...@chromium.org (2020-10-19)

1. Does your merge fit within the Merge Decision Guidelines?
Yes. 

2. Links to the CLs you are requesting to merge.
https://chromium-review.googlesource.com/c/chromium/src/+/2472397

3. Has the change landed and been verified on ToT?
Yes.

4. Does this change need to be merged into other active release branches (M-1, M+1)?
We should consider merging to M86, if a respin is planned.

5. Why are these changes required in this milestone after branch?
To fix a security issue.

6. Is this a new feature?
No.

7. If it is a new feature, is it behind a flag using finch?
N/A

### ad...@chromium.org (2020-10-19)

Approving merge to M87, branch 4280, and M86, branch 4240, assuming no problems have appeared in Canary.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2bf28a4ef7c8cc5d544f23039eb9574ae9aedd6b

commit 2bf28a4ef7c8cc5d544f23039eb9574ae9aedd6b
Author: Guido Urdaneta <guidou@chromium.org>
Date: Mon Oct 19 17:11:22 2020

Validate input of MediaStreamDispatcherHost::OpenDevice()

This method forwards to MediaStreamManager::OpenDevice(), which
DCHECKs for the stream type to be device video or audio capture
(i.e., webcam or mic). However, MSDH admits other stream types,
which cause MSM::OpenDevice to hit this DCHECK.

This CL ensures that a message containing an incorrect stream type,
which could be sent by a malicious renderer, results in killing the
renderer process.

(cherry picked from commit 229fdaf8fc05e0eeadad380d401c191afd822d92)

Bug: 1135018
Change-Id: I3884dde95d92c41f44966a8ab1dd7bdfd4b23b9b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2472397
Auto-Submit: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#817151}
TBR: avi@chromium.org
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2485055
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/branch-heads/4280@{#493}
Cr-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}

[modify] https://crrev.com/2bf28a4ef7c8cc5d544f23039eb9574ae9aedd6b/content/browser/bad_message.h
[modify] https://crrev.com/2bf28a4ef7c8cc5d544f23039eb9574ae9aedd6b/content/browser/renderer_host/media/media_stream_dispatcher_host.cc
[modify] https://crrev.com/2bf28a4ef7c8cc5d544f23039eb9574ae9aedd6b/tools/metrics/histograms/enums.xml


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/740285102aa1c160151e0470a496fdc81a7e1cd4

commit 740285102aa1c160151e0470a496fdc81a7e1cd4
Author: Guido Urdaneta <guidou@chromium.org>
Date: Mon Oct 19 17:15:33 2020

Validate input of MediaStreamDispatcherHost::OpenDevice()

This method forwards to MediaStreamManager::OpenDevice(), which
DCHECKs for the stream type to be device video or audio capture
(i.e., webcam or mic). However, MSDH admits other stream types,
which cause MSM::OpenDevice to hit this DCHECK.

This CL ensures that a message containing an incorrect stream type,
which could be sent by a malicious renderer, results in killing the
renderer process.

(cherry picked from commit 229fdaf8fc05e0eeadad380d401c191afd822d92)

Bug: 1135018
Change-Id: I3884dde95d92c41f44966a8ab1dd7bdfd4b23b9b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2472397
Auto-Submit: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#817151}
TBR: avi@chromium.org
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2485092
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1277}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/740285102aa1c160151e0470a496fdc81a7e1cd4/content/browser/bad_message.h
[modify] https://crrev.com/740285102aa1c160151e0470a496fdc81a7e1cd4/content/browser/renderer_host/media/media_stream_dispatcher_host.cc
[modify] https://crrev.com/740285102aa1c160151e0470a496fdc81a7e1cd4/tools/metrics/histograms/enums.xml


### ad...@google.com (2020-10-20)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-10-21)

Congratulations, the VRP panel has decided to award $15,000 for this bug.

### ad...@google.com (2020-10-22)

[Empty comment from Monorail migration]

### ad...@google.com (2020-12-06)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mf...@chromium.org (2021-03-22)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>MediaCapture]

### mf...@chromium.org (2021-03-22)

[Empty comment from Monorail migration]

[Monorail components: -UI>Browser>TabCapture]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1135018?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053503)*
