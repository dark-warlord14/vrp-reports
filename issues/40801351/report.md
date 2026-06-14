# Security: Heap-use-after-free in lens::LensRegionSearchController::OnCaptureCompleted

| Field | Value |
|-------|-------|
| **Issue ID** | [40801351](https://issues.chromium.org/issues/40801351) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Internals>Plugins>PDF, UI>Browser>Mobile |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | dh...@chromium.org |
| **Created** | 2021-11-01 |
| **Bounty** | $3,000.00 |

## Description

Chrome Version: 97.0.4687.2 (Official Build) canary (x86\_64)  

Operating System: MacOS and Windows 10

**REPRODUCTION CASE**

Enable #enable-lens-region-search flag.

On MacOS:

1. Open tabs A and B
2. On tab B, Go to <https://www.orimi.com/pdf-test.pdf> -> Right click -> Search Image with Google Lens
3. Detach tab B from tab A
4. On tab A, close "Drag over any image to search" notification

On Windows:

1. Open tabs A and B
2. On tab B, Go to <https://www.orimi.com/pdf-test.pdf> -> Right click -> Search Image with Google Lens
3. Detach tab B from tab A
4. Close tab A
5. Reload tab B

chrome!views::Widget::CloseWithReason+0x2be:  

00007ff9`d95c70fe 488b8048010000 mov rax,qword ptr [rax+148h] ds:4045ec00`0a0a0148=????????????????  

0:000> k

# Child-SP RetAddr Call Site

00 000000ea`2e7fd6f0 00007ff9`e034f312 chrome!views::Widget::CloseWithReason+0x2be [C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc @ 704]  

01 000000ea`2e7fd7a0 00007ff9`e034f607 chrome!lens::LensRegionSearchController::CloseWithReason+0x22 [C:\b\s\w\ir\cache\builder\src\chrome\browser\lens\region\_search\lens\_region\_search\_controller.cc @ 238]  

02 000000ea`2e7fd7d0 00007ff9`dff0b80e chrome!lens::LensRegionSearchController::OnCaptureCompleted+0x27 [C:\b\s\w\ir\cache\builder\src\chrome\browser\lens\region\_search\lens\_region\_search\_controller.cc @ 159]  

03 (Inline Function) --------`-------- chrome!base::OnceCallback<void (const image_editor::ScreenshotCaptureResult &)>::Run+0x22 [C:\b\s\w\ir\cache\builder\src\base\callback.h @ 142] 04 000000ea`2e7fd860 00007ff9`dff0b780 chrome!image_editor::ScreenshotFlow::RunScreenshotCompleteCallback+0x7e [C:\b\s\w\ir\cache\builder\src\chrome\browser\image_editor\screenshot_flow.cc @ 263] 05 000000ea`2e7fd8e0 00007ff9`dff0b8b7 chrome!image_editor::ScreenshotFlow::CaptureAndRunScreenshotCompleteCallback+0x180 [C:\b\s\w\ir\cache\builder\src\chrome\browser\image_editor\screenshot_flow.cc @ 145] 06 (Inline Function) --------`-------- chrome!image\_editor::ScreenshotFlow::CompleteCapture+0x21 [C:\b\s\w\ir\cache\builder\src\chrome\browser\image\_editor\screenshot\_flow.cc @ 251]  

07 000000ea`2e7fd980 00007ff9`dc0be9ae chrome!image\_editor::ScreenshotFlow::OnKeyEvent+0x67 [C:\b\s\w\ir\cache\builder\src\chrome\browser\image\_editor\screenshot\_flow.cc @ 175]  

08 (Inline Function) --------`-------- chrome!ui::EventDispatcher::DispatchEvent+0x4a [C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc @ 191] 09 000000ea`2e7fd9d0 00007ff9`d8ac3060 chrome!ui::EventDispatcher::DispatchEventToEventHandlers+0x1fe [C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc @ 178] 0a (Inline Function) --------`-------- chrome!ui::EventDispatcher::ProcessEvent+0x61 [C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc @ 126]  

0b (Inline Function) --------`-------- chrome!ui::EventDispatcherDelegate::DispatchEventToTarget+0x87 [C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc @ 84] 0c 000000ea`2e7fda90 00007ff9`d8ac2e2c chrome!ui::EventDispatcherDelegate::DispatchEvent+0x100 [C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc @ 56] 0d 000000ea`2e7fdb30 00007ff9`de5fea02 chrome!ui::EventProcessor::OnEventFromSource+0x12c [C:\b\s\w\ir\cache\builder\src\ui\events\event_processor.cc @ 49] 0e 000000ea`2e7fdbd0 00007ff9`dfe825e0 chrome!aura::WindowTreeHost::DispatchKeyEventPostIME+0x52 [C:\b\s\w\ir\cache\builder\src\ui\aura\window_tree_host.cc @ 320] 0f (Inline Function) --------`-------- chrome!ui::InputMethodBase::DispatchKeyEventPostIME+0x31 [C:\b\s\w\ir\cache\builder\src\ui\base\ime\input\_method\_base.cc @ 142]  

10 000000ea`2e7fdc10 00007ff9`dfe8232f chrome!ui::InputMethodWinBase::ProcessUnhandledKeyEvent+0x70 [C:\b\s\w\ir\cache\builder\src\ui\base\ime\win\input\_method\_win\_base.cc @ 495]  

11 000000ea`2e7fdce0 00007ff9`dec4aff8 chrome!ui::InputMethodWinBase::DispatchKeyEvent+0x2ef [C:\b\s\w\ir\cache\builder\src\ui\base\ime\win\input\_method\_win\_base.cc @ 234]  

12 000000ea`2e7fdde0 00007ff9`d8934d3f chrome!aura::WindowEventDispatcher::PreDispatchKeyEvent+0xc8 [C:\b\s\w\ir\cache\builder\src\ui\aura\window\_event\_dispatcher.cc @ 1064]  

13 000000ea`2e7fde40 00007ff9`d8ac2fb5 chrome!aura::WindowEventDispatcher::PreDispatchEvent+0x67f [C:\b\s\w\ir\cache\builder\src\ui\aura\window\_event\_dispatcher.cc @ 551]  

14 000000ea`2e7fdf50 00007ff9`d8ac2e2c chrome!ui::EventDispatcherDelegate::DispatchEvent+0x55 [C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc @ 53]  

15 000000ea`2e7fdff0 00007ff9`d92fc6eb chrome!ui::EventProcessor::OnEventFromSource+0x12c [C:\b\s\w\ir\cache\builder\src\ui\events\event\_processor.cc @ 49]  

16 (Inline Function) --------`-------- chrome!ui::EventSource::DeliverEventToSink+0x27 [C:\b\s\w\ir\cache\builder\src\ui\events\event_source.cc @ 117] 17 000000ea`2e7fe090 00007ff9`defd99fd chrome!ui::EventSource::SendEventToSinkFromRewriter+0x7b [C:\b\s\w\ir\cache\builder\src\ui\events\event_source.cc @ 145] 18 (Inline Function) --------`-------- chrome!ui::EventSource::SendEventToSink+0xe [C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc @ 111]  

19 000000ea`2e7fe120 00007ff9`df9c3f21 chrome!views::DesktopWindowTreeHostWin::HandleKeyEvent+0x6d [C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop\_aura\desktop\_window\_tree\_host\_win.cc @ 1027]  

1a 000000ea`2e7fe170 00007ff9`d92752d1 chrome!views::HWNDMessageHandler::OnKeyEvent+0xe1 [C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc @ 1926]  

1b 000000ea`2e7fe300 00007ff9`d9272d43 chrome!views::HWNDMessageHandler::\_ProcessWindowMessage+0x1e81 [C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.h @ 398]  

1c 000000ea`2e7fe4b0 00007ff9`d896b524 chrome!views::HWNDMessageHandler::OnWndProc+0x103 [C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc @ 1018]  

1d 000000ea`2e7fe5b0 00007ff9`d896b48f chrome!gfx::WindowImpl::WndProc+0x84 [C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window\_impl.cc @ 307]  

1e 000000ea`2e7fe620 00007ffa`2c50e858 chrome!base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc>+0xf [C:\b\s\w\ir\cache\builder\src\base\win\wrapped\_window\_proc.h @ 77]  

1f 000000ea`2e7fe650 00007ffa`2c50e299 user32!CallWindowProcW+0x3f8  

20 000000ea`2e7fe7e0 00007ff9`dbfc5acf user32!DispatchMessageW+0x259  

21 000000ea`2e7fe860 00007ff9`dbfc48cb chrome!base::MessagePumpForUI::ProcessMessageHelper+0x86f [C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc @ 543]  

22 (Inline Function) --------`-------- chrome!base::MessagePumpForUI::ProcessNextWindowsMessage+0x27e [C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc @ 504] 23 000000ea`2e7fe980 00007ff9`d88d4fdb chrome!base::MessagePumpForUI::DoRunLoop+0x2db [C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc @ 215] 24 000000ea`2e7feae0 00007ff9`d8df8eaa chrome!base::MessagePumpWin::Run+0x4b [C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc @ 79] 25 000000ea`2e7feb30 00007ff9`d8ff74cd chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run+0x8a [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 461] 26 000000ea`2e7feba0 00007ff9`d9545ac9 chrome!base::RunLoop::Run+0x1cd [C:\b\s\w\ir\cache\builder\src\base\run_loop.cc @ 142] 27 000000ea`2e7fecd0 00007ff9`d9041851 chrome!content::BrowserMainLoop::RunMainMessageLoop+0xd9 [C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc @ 1007] 28 (Inline Function) --------`-------- chrome!content::BrowserMainRunnerImpl::Run+0x9 [C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc @ 152]  

29 000000ea`2e7fed40 00007ff9`d903f8df chrome!content::BrowserMain+0xb1 [C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc @ 49]  

2a (Inline Function) --------`-------- chrome!content::RunBrowserProcessMain+0x6b [C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc @ 641] 2b 000000ea`2e7fede0 00007ff9`d9032f9d chrome!content::ContentMainRunnerImpl::RunBrowser+0x43f [C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc @ 1137] 2c 000000ea`2e7feed0 00007ff9`d8d39ce2 chrome!content::ContentMainRunnerImpl::Run+0x20d [C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc @ 1004] 2d (Inline Function) --------`-------- chrome!content::RunContentProcess+0x11d [C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc @ 390]  

2e 000000ea`2e7fefa0 00007ff9`d8d38f3a chrome!content::ContentMain+0x152 [C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc @ 418]  

2f 000000ea`2e7ff190 00007ff6`46a32c5c chrome!ChromeMain+0x18a [C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc @ 175]  

30 000000ea`2e7ff2a0 00007ff6`46a327ea chrome\_exe!GetPakFileHashes+0x115c  

31 000000ea`2e7ff520 00007ff6`46ab0592 chrome\_exe!GetPakFileHashes+0xcea  

32 000000ea`2e7ff950 00007ffa`2c327034 chrome\_exe!GetHandleVerifier+0x77512  

33 000000ea`2e7ff990 00007ffa`2cea2651 KERNEL32!BaseThreadInitThunk+0x14  

34 000000ea`2e7ff9c0 00000000`00000000 ntdll!RtlUserThreadStart+0x21

## Attachments

- [MacOS.mov](attachments/MacOS.mov) (video/quicktime, 11.1 MB)
- [Windows.mov](attachments/Windows.mov) (video/quicktime, 5.5 MB)
- [mac.mov](attachments/mac.mov) (video/quicktime, 4.1 MB)
- [screen.mov](attachments/screen.mov) (video/quicktime, 7.1 MB)

## Timeline

### [Deleted User] (2021-11-01)

[Empty comment from Monorail migration]

### da...@chromium.org (2021-11-02)

This is behind a command line flag, so no security implications (yet).

There should be a Lens component probably, but going by https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/lens/DIR_METADATA

This would be a P0 if it was enabled for users, so needs to be fixed before we enable the enable-lens-region-search flag

[Monorail components: UI>Browser>Mobile]

### ch...@gmail.com (2021-11-02)

I think this should be a security bug as in the previous https://crbug.com/chromium/1244348.

### si...@google.com (2021-11-02)

Assigning to Juan based on https://crbug.com/chromium/1244348.

### ju...@google.com (2021-11-02)

I was not able to reproduce this on Chrome Canary 97.0.4688.0 (Official Build) canary (x86_64) on Mac using the steps provided in this bug. The region search menu item does not appear on the page in question. See attached recording. 

Also, as far as I know, it is expected that this context menu item does not appear on PDF links. See pointer at https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/renderer_context_menu/render_view_context_menu.cc;l=3121;drc=49e30ea02860a4b573e2c7309429c0a5b3a740e2

Is it possible you are using an older version? 

### ch...@gmail.com (2021-11-02)

I tried with a fresh profile on the latest version of canary 97.0.4689.0 on Windows 10 and MacOS, the region search menu item still appears on the PDF link.

### ju...@google.com (2021-11-02)

[Empty comment from Monorail migration]

### ju...@google.com (2021-11-03)

[Empty comment from Monorail migration]

### dh...@chromium.org (2021-11-03)

I think this may be caused by an experiment the PDF team is running on Canary. I'm able to repro this issue only when I enable chrome://flags/#pdf-unseasoned. I can look into it further.

### dh...@chromium.org (2021-11-03)

I just confirmed this can only be repro'ed when chrome://flags/#pdf-unseasoned is enabled. We're running an experiment for the feature on Canary and Beta.

Our feature messed with assumptions of the frame-tree model of the PDF viewer, so we're not checking the correct origin when selecting context menu options. 

[Monorail components: -UI>Browser>Mobile Internals>Plugins>PDF]

### dh...@chromium.org (2021-11-05)

WIP is crrev.com/c/3259600

Also, I'm going to add UI>Browser>Mobile back as a component. Is there no better component for Lens? If not, I'd suggest the team to create one.

[Monorail components: UI>Browser>Mobile]

### gi...@appspot.gserviceaccount.com (2021-11-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/aa10b7bd9d1a681d34a5d285ed5cc15e90c6cea7

commit aa10b7bd9d1a681d34a5d285ed5cc15e90c6cea7
Author: Daniel Hosseinian <dhoss@chromium.org>
Date: Fri Nov 05 22:13:10 2021

[unseasoned-pdf] Update context menu checks of the PDF viewer

Context menus need to check if they are invoked in the PDF viewer to
provide appropriate options.

Before, it did this by checking the URL of the invoking frame. This was
fine when the PDF viewer had one frame, the extension's. However, the
Unseasoned PDF viewer has two frames, the extension's and the plugin's.
The plugin's frame has an unpredictable origin, so we need to check if
its parent is the extension frame.

Fixed: 1265345
Change-Id: I08d2d9b4fc3e96047ebca8b9eb04b270b8c56ccc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3259600
Commit-Queue: Daniel Hosseinian <dhoss@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>
Cr-Commit-Position: refs/heads/main@{#938976}

[modify] https://crrev.com/aa10b7bd9d1a681d34a5d285ed5cc15e90c6cea7/chrome/browser/pdf/pdf_extension_test.cc
[modify] https://crrev.com/aa10b7bd9d1a681d34a5d285ed5cc15e90c6cea7/chrome/test/BUILD.gn
[modify] https://crrev.com/aa10b7bd9d1a681d34a5d285ed5cc15e90c6cea7/chrome/browser/renderer_context_menu/render_view_context_menu.cc


### dh...@chromium.org (2021-11-05)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-11-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4087acaf9a4bbc4808f5a663070ac700b2c6c789

commit 4087acaf9a4bbc4808f5a663070ac700b2c6c789
Author: Austin Sullivan <asully@chromium.org>
Date: Fri Nov 05 22:46:29 2021

Revert "[unseasoned-pdf] Update context menu checks of the PDF viewer"

This reverts commit aa10b7bd9d1a681d34a5d285ed5cc15e90c6cea7.

Reason for revert: <INSERT REASONING HERE>

Original change's description:
> [unseasoned-pdf] Update context menu checks of the PDF viewer
>
> Context menus need to check if they are invoked in the PDF viewer to
> provide appropriate options.
>
> Before, it did this by checking the URL of the invoking frame. This was
> fine when the PDF viewer had one frame, the extension's. However, the
> Unseasoned PDF viewer has two frames, the extension's and the plugin's.
> The plugin's frame has an unpredictable origin, so we need to check if
> its parent is the extension frame.
>
> Fixed: 1265345
> Change-Id: I08d2d9b4fc3e96047ebca8b9eb04b270b8c56ccc
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3259600
> Commit-Queue: Daniel Hosseinian <dhoss@chromium.org>
> Reviewed-by: Lei Zhang <thestig@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#938976}

Change-Id: I52d90c3bda285d1a544261906fb6bfaf810f7c87
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: 1267445
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3265891
Auto-Submit: Austin Sullivan <asully@chromium.org>
Owners-Override: Austin Sullivan <asully@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Austin Sullivan <asully@chromium.org>
Cr-Commit-Position: refs/heads/main@{#938995}

[modify] https://crrev.com/4087acaf9a4bbc4808f5a663070ac700b2c6c789/chrome/browser/pdf/pdf_extension_test.cc
[modify] https://crrev.com/4087acaf9a4bbc4808f5a663070ac700b2c6c789/chrome/test/BUILD.gn
[modify] https://crrev.com/4087acaf9a4bbc4808f5a663070ac700b2c6c789/chrome/browser/renderer_context_menu/render_view_context_menu.cc


### [Deleted User] (2021-11-05)

Merge review required: a reverted commit was detected after the merge request.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dh...@chromium.org (2021-11-05)

Recanting my merge request until I reland with the fix: crrev.com/c/3266104

### gi...@appspot.gserviceaccount.com (2021-11-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bb2753263b750141f4ed53265a5fd9943ea1b832

commit bb2753263b750141f4ed53265a5fd9943ea1b832
Author: Daniel Hosseinian <dhoss@chromium.org>
Date: Sat Nov 06 01:55:52 2021

Reland "[unseasoned-pdf] Update context menu checks of the PDF viewer"

This is a reland of aa10b7bd9d1a681d34a5d285ed5cc15e90c6cea7. The
original change was reverted because it made a dependency on
//components/lens/ conditional on `enable_pdf`. However,
pdf_extension_test.cc is not build conditioned on `enable_pdf`.

Original change's description:
> [unseasoned-pdf] Update context menu checks of the PDF viewer
>
> Context menus need to check if they are invoked in the PDF viewer to
> provide appropriate options.
>
> Before, it did this by checking the URL of the invoking frame. This was
> fine when the PDF viewer had one frame, the extension's. However, the
> Unseasoned PDF viewer has two frames, the extension's and the plugin's.
> The plugin's frame has an unpredictable origin, so we need to check if
> its parent is the extension frame.
>
> Fixed: 1265345
> Change-Id: I08d2d9b4fc3e96047ebca8b9eb04b270b8c56ccc
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3259600
> Commit-Queue: Daniel Hosseinian <dhoss@chromium.org>
> Reviewed-by: Lei Zhang <thestig@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#938976}

Change-Id: Ib36a2bd0c4134b8bbfe866028c0fc43947e52e24
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3266104
Auto-Submit: Daniel Hosseinian <dhoss@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>
Commit-Queue: Daniel Hosseinian <dhoss@chromium.org>
Cr-Commit-Position: refs/heads/main@{#939048}

[modify] https://crrev.com/bb2753263b750141f4ed53265a5fd9943ea1b832/chrome/browser/pdf/pdf_extension_test.cc
[modify] https://crrev.com/bb2753263b750141f4ed53265a5fd9943ea1b832/chrome/browser/renderer_context_menu/render_view_context_menu.cc


### dh...@chromium.org (2021-11-06)

Re-submitting my merge request!

### [Deleted User] (2021-11-07)

Merge approved: your change passed merge requirements and is auto-approved for M97. Please go ahead and merge the CL to branch 4692 (refs/branch-heads/4692) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-07)

[Empty comment from Monorail migration]

### sk...@chromium.org (2021-11-08)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-11-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f97a833f880f945236df7352af4be82177a25939

commit f97a833f880f945236df7352af4be82177a25939
Author: Daniel Hosseinian <dhoss@chromium.org>
Date: Mon Nov 08 21:47:58 2021

[M97][unseasoned-pdf] Update context menu checks of the PDF viewer

This is a merge of a reland of
aa10b7bd9d1a681d34a5d285ed5cc15e90c6cea7. The original change was
reverted because it made a dependency on //components/lens/ conditional
on `enable_pdf`. However, pdf_extension_test.cc is not build
conditioned on `enable_pdf`.

Original change's description:
> [unseasoned-pdf] Update context menu checks of the PDF viewer
>
> Context menus need to check if they are invoked in the PDF viewer to
> provide appropriate options.
>
> Before, it did this by checking the URL of the invoking frame. This was
> fine when the PDF viewer had one frame, the extension's. However, the
> Unseasoned PDF viewer has two frames, the extension's and the plugin's.
> The plugin's frame has an unpredictable origin, so we need to check if
> its parent is the extension frame.
>
> Fixed: 1265345
> Change-Id: I08d2d9b4fc3e96047ebca8b9eb04b270b8c56ccc
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3259600
> Commit-Queue: Daniel Hosseinian <dhoss@chromium.org>
> Reviewed-by: Lei Zhang <thestig@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#938976}

(cherry picked from commit bb2753263b750141f4ed53265a5fd9943ea1b832)

Change-Id: Ib36a2bd0c4134b8bbfe866028c0fc43947e52e24
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3266104
Auto-Submit: Daniel Hosseinian <dhoss@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>
Commit-Queue: Daniel Hosseinian <dhoss@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#939048}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3267037
Cr-Commit-Position: refs/branch-heads/4692@{#22}
Cr-Branched-From: 038cd96142d384c0d2238973f1cb277725a62eba-refs/heads/main@{#938553}

[modify] https://crrev.com/f97a833f880f945236df7352af4be82177a25939/chrome/browser/pdf/pdf_extension_test.cc
[modify] https://crrev.com/f97a833f880f945236df7352af4be82177a25939/chrome/test/BUILD.gn
[modify] https://crrev.com/f97a833f880f945236df7352af4be82177a25939/chrome/browser/renderer_context_menu/render_view_context_menu.cc


### ch...@gmail.com (2021-12-27)

This bug needs Security_Severity and Type-Bug-Security labels set.

### ch...@gmail.com (2022-01-27)

Any update on reward-topanel? Thanks.

### [Deleted User] (2022-02-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-03-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-23)

Congratulations, Khalil on another one! The VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2022-03-25)

[Empty comment from Monorail migration]

### is...@google.com (2022-03-25)

This issue was migrated from crbug.com/chromium/1265345?no_tracker_redirect=1

[Multiple monorail components: Internals>Plugins>PDF, UI>Browser>Mobile]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40801351)*
