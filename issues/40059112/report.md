# Security: Incomplete patch for issue 1246631 (CVE-2021-37981) and inaccurate scaling in EyeDropperView

| Field | Value |
|-------|-------|
| **Issue ID** | [40059112](https://issues.chromium.org/issues/40059112) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Forms>Color |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2021-37981 |
| **Reporter** | l4...@gmail.com |
| **Assignee** | dc...@chromium.org |
| **Created** | 2022-03-16 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**

Description:

There's a heap overflow might occurs in EyeDropperView::OnPaint which is similar to <https://crbug.com/chromium/1246631> (CVE-2021-37981) while Windows scale setting is 125% or 175%

The crash is only reproduced on Microsoft Chromium Edge since there's a scale bug in Chromium which make this bug won't be triggered, however Microsoft fixed it in Edge.

I originally reported it to MSRC, but they insisted it is an upstream Chromium issue.

Analysis:

In Chromium Edge, if the EyeDropperView is moved to the upper left corner of the screen, the `center_position` will be (-1, -1):  

<https://source.chromium.org/chromium/chromium/src/+/refs/tags/101.0.4931.4:chrome/browser/ui/views/eye_dropper/eye_dropper_view.cc;drc=79511d004bff7f4a1c83f8657caff31aa1a19f3b;l=220>

and patch of CVE-2021-37981 in `EyeDropperView::ScreenCapturer::GetColor` didn't check x and y must >= 0:  

<https://source.chromium.org/chromium/chromium/src/+/refs/tags/101.0.4931.4:chrome/browser/ui/views/eye_dropper/eye_dropper_view.cc;drc=79511d004bff7f4a1c83f8657caff31aa1a19f3b;l=130>

Thus the browser process will crash will crash when y is smaller the zero (-1).

--

The implementation of EyeDropperView looks no different on the two browsers, however, this bug can only be reproduced on Microsoft Edge.

By setting some logging breakpoints in both Chrome and Edge, I found that the scale behavior are different on two browsers  

The following log are produced by opening the EyeDropperView when the cursor was at (0, 0) and scale set to 125%:

Chromium:  

// EyeDropperView Widget Created  

GetWindowBoundsInScreen Original Bounds 577 636 125 125  

GetWindowBoundsInScreen ScreenToDIPRect -> 461 508 101 101

// In EyeDropperView::Update  

Before SetBounds DIPToScreenRectInWindow -50 -50 100 100  

DIPToScreenRect Before ScaleToEnclosingRect: -50,-50,100,100  

DIPToScreenRect After ScaleToEnclosingRect: -63,-63,126,126  

After SetBounds DIPToScreenRectInWindow -63 -63 126 126

// In EyeDropperView::OnPaint  

OnPaint GetWindowBoundsInScreen Bounds -51 -51 102 102  

DIPToScreenRect Before ScaleToEnclosingRect: -51,-51,102,102  

DIPToScreenRect After ScaleToEnclosingRect: -64,-64,128,128  

DIPToScreenRectInWindow-> -64, -64, 128, 128  

center\_point = (0, 0)

Edge:  

// EyeDropperView Widget Created  

GetWindowBoundsInScreen Original Bounds 577 636 125 125  

GetWindowBoundsInScreen ScreenToDIPRect -> 461 508 101 101

// In EyeDropperView::Update  

Before SetBounds DIPToScreenRectInWindow -50 -50 100 100  

DIPToScreenRect Before ScaleToEnclosingRect: 0,0,100,100  

DIPToScreenRect After ScaleToEnclosingRect: -63,-63,125,125  

After SetBounds DIPToScreenRectInWindow -63 -63 125 125

// In EyeDropperView::OnPaint  

OnPaint GetWindowBoundsInScreen Bounds -51 -51 101 101  

DIPToScreenRect Before ScaleToEnclosingRect: 0,0,101,101  

DIPToScreenRect After ScaleToEnclosingRect: -64,-64,127,127  

DIPToScreenRectInWindow-> -64, -64, 127, 127  

center\_point = (-1, -1)

After compare the binary of Edge with Chromium, I confirmed the implementation of `display::win::ScreenWin::DIPToScreenRect` in Edge is different from Chromium:  

before calling `ScaleToEnclosingRect`, the origin of rect `dip_bounds` was set to (0, 0):  

(Decompiled Code)  

...  

tmp\_dip\_bounds.origin\_ = 0i64; // <---  

tmp\_dip\_bounds.size\_ = pdip\_bounds->size\_;  

gfx::ScaleToEnclosingRect(result, &tmp\_dip\_bounds, scale\_factor, scale\_factor); <---  

display::win::*anonymous\_namespace*::DIPToScreenPoint(&tmp\_dip\_bounds, &pdip\_bounds->origin\_, screen\_win\_display);  

...

I believe this is done to fix a (EyeDropperView specificed?) scale bug in chromium, since `ScaleToEnclosingRect` use `right()` and `buttom()` with `SetByBounds()` to calculate scaled bounds, the scaled size will be inaccurate with odd number origin:  

<https://source.chromium.org/chromium/chromium/src/+/main:ui/gfx/geometry/rect.h;drc=44004c6ba21e2942e947c22e681b58d19ce9d645;l=325>

e.g. a window with size 100 x 100 and origin at (1, 1) with 125% scale setting will be scaled into a bounds with origin=(1,1) and size=126x126:  

...  

int x = base::ClampFloor(rect.x() \* x\_scale); // 1 \* 1.25  

int y = base::ClampFloor(rect.y() \* y\_scale); // 1 \* 1.25  

int r = rect.width() == 0 ? x : base::ClampCeil(rect.right() \* x\_scale); // (1 + 100) \* 1.25 = 127  

int b = rect.height() == 0 ? y : base::ClampCeil(rect.bottom() \* y\_scale); // (1 + 100) \* 1.25 = 127  

Rect result;  

result.SetByBounds(x, y, r, b);  

-> x = 1, y = 1, width = 127 - 1 = 126, height = 127 - 1 = 126

And if we add a log in `EyeDropperView::OnPaint()` to log the result of `GetWidget()->GetWindowBoundsInScreen()`, we can see that window bounds will keep increaseing:

932,340 102x100  

936,341 102x102  

944,348 104x103  

1012,378 104x104  

1060,396 104x106  

1080,404 104x106  

1076,405 106x107  

1072,406 106x109  

1064,405 108x110  

1060,402 108x110  

1057,401 110x111  

1056,400 111x112  

1054,400 112x112  

1052,397 112x114  

1052,396 112x115  

1050,394 114x116  

...

This is because every time `EyeDropperView::UpdatePosition()` calls `GetWidget()->SetBounds()` will cause the size of window bounds to be increased.

---

`ScreenToDIPRect` and `DIPToScreenRect` both have the same issue and might lead to other security issues.

I've also attach `scale_fix.diff` to reproduce the Edge behavior in Chromium.

**VERSION**  

Chrome Version: 101.0.4931.4 dev + stable  

Operating System: Windows 10 Pro 64-bit 21H2 / 10.0.19044.1586

**REPRODUCTION CASE**

1. Apply scale\_fix.diff
2. Adjust Windows display scaling settings to 125%
3. Open poc.html with Chromium
4. Click button GO, EyeDropper should be opened
5. Move your cursor to the top right corner of the screen
6. Browser process crashed

# Type of crash: browser Crash State:

==5892==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x12a6348b17f8 at pc 0x7ffe02ad3685 bp 0x00bcd81fdef0 sp 0x00bcd81fdf38  

READ of size 4 at 0x12a6348b17f8 thread T0  

#0 0x7ffe02ad3684 in SkPixmap::getColor(int, int) const C:\chromium\src\third\_party\skia\src\core\SkPixmap.cpp:326:30  

#1 0x7ffe1a9a16e9 in SkBitmap::getColor C:\chromium\src\third\_party\skia\include\core\SkBitmap.h:825  

#2 0x7ffe1a9a16e9 in EyeDropperView::ScreenCapturer::GetColor C:\chromium\src\chrome\browser\ui\views\eye\_dropper\eye\_dropper\_view.cc:133  

#3 0x7ffe1a9a16e9 in EyeDropperView::OnPaint(class gfx::Canvas \*) C:\chromium\src\chrome\browser\ui\views\eye\_dropper\eye\_dropper\_view.cc:236:25  

#4 0x7ffe0d096a82 in views::View::Paint(class views::PaintInfo const &) C:\chromium\src\ui\views\view.cc:1194:5  

#5 0x7ffe0d09f8d8 in views::View::RecursivePaintHelper(void (\_\_cdecl views::View::\*)(class views::PaintInfo const &), class views::PaintInfo const &) C:\chromium\src\ui\views\view.cc:2459:7  

#6 0x7ffe0d09f4ce in views::View::PaintChildren(class views::PaintInfo const &) C:\chromium\src\ui\views\view.cc:1958:3  

#7 0x7ffe0d096bbd in views::View::Paint(class views::PaintInfo const &) C:\chromium\src\ui\views\view.cc:1200:3  

#8 0x7ffe0d0a18e3 in views::View::PaintFromPaintRoot(class ui::PaintContext const &) C:\chromium\src\ui\views\view.cc:2466:3  

#9 0x7ffe0d0f0bd2 in ui::Layer::PaintContentsToDisplayList(void) C:\chromium\src\ui\compositor\layer.cc:1332:16  

#10 0x7ffe0fecf66b in cc::PictureLayer::Update(void) C:\chromium\src\cc\layers\picture\_layer.cc:153:41  

#11 0x7ffe0fe69b2e in cc::LayerTreeHost::PaintContent C:\chromium\src\cc\trees\layer\_tree\_host.cc:1569  

#12 0x7ffe0fe69b2e in cc::LayerTreeHost::DoUpdateLayers(void) C:\chromium\src\cc\trees\layer\_tree\_host.cc:924:28  

#13 0x7ffe0fe68f71 in cc::LayerTreeHost::UpdateLayers(void) C:\chromium\src\cc\trees\layer\_tree\_host.cc:787:17  

#14 0x7ffe12f14e55 in cc::SingleThreadProxy::DoPainting(struct viz::BeginFrameArgs const &) C:\chromium\src\cc\trees\single\_thread\_proxy.cc:1068:21  

#15 0x7ffe12f16efc in cc::SingleThreadProxy::BeginMainFrame(struct viz::BeginFrameArgs const &) C:\chromium\src\cc\trees\single\_thread\_proxy.cc:1031:3  

#16 0x7ffe12f181d0 in base::internal::FunctorTraits<void (cc::SingleThreadProxy::\*)(const viz::BeginFrameArgs &),void>::Invoke C:\chromium\src\base\bind\_internal.h:542  

#17 0x7ffe12f181d0 in base::internal::InvokeHelper<1,void>::MakeItSo C:\chromium\src\base\bind\_internal.h:726  

#18 0x7ffe12f181d0 in base::internal::Invoker<base::internal::BindState<void (cc::SingleThreadProxy::\*)(const viz::BeginFrameArgs &),base::WeakPtr[cc::SingleThreadProxy](javascript:void(0);),viz::BeginFrameArgs>,void ()>::RunImpl C:\chromium\src\base\bind\_internal.h:779  

#19 0x7ffe12f181d0 in base::internal::Invoker<struct base::internal::BindState<void (**cdecl cc::SingleThreadProxy::\*)(struct viz::BeginFrameArgs const &), class base::WeakPtr<class cc::SingleThreadProxy>, struct viz::BeginFrameArgs>, (void)>::RunOnce(class base::internal::BindStateBase \*) C:\chromium\src\base\bind\_internal.h:748:12  

#20 0x7ffe0d377924 in base::OnceCallback<void ()>::Run C:\chromium\src\base\callback.h:143  

#21 0x7ffe0d377924 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\chromium\src\base\task\common\task\_annotator.cc:135:32  

#22 0x7ffe101f8675 in base::TaskAnnotator::RunTask C:\chromium\src\base\task\common\task\_annotator.h:75  

#23 0x7ffe101f8675 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence\_manager::LazyNow \*) C:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:385:21  

#24 0x7ffe101f7c69 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:290:41  

#25 0x7ffe0d427866 in base::MessagePumpForUI::DoRunLoop(void) C:\chromium\src\base\message\_loop\message\_pump\_win.cc:220:67  

#26 0x7ffe0d425af8 in base::MessagePumpWin::Run(class base::MessagePump::Delegate \*) C:\chromium\src\base\message\_loop\message\_pump\_win.cc:78:3  

#27 0x7ffe101f9de0 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:497:12  

#28 0x7ffe0d2f5e23 in base::RunLoop::Run(class base::Location const &) C:\chromium\src\base\run\_loop.cc:141:14  

#29 0x7ffe0612c2f5 in content::BrowserMainLoop::RunMainMessageLoop(void) C:\chromium\src\content\browser\browser\_main\_loop.cc:1070:18  

#30 0x7ffe0613193b in content::BrowserMainRunnerImpl::Run(void) C:\chromium\src\content\browser\browser\_main\_runner\_impl.cc:155:15  

#31 0x7ffe06125cd9 in content::BrowserMain(struct content::MainFunctionParams) C:\chromium\src\content\browser\browser\_main.cc:30:28  

#32 0x7ffe0cf29133 in content::RunBrowserProcessMain(struct content::MainFunctionParams, class content::ContentMainDelegate \*) C:\chromium\src\content\app\content\_main\_runner\_impl.cc:642:10  

#33 0x7ffe0cf2c2ac in content::ContentMainRunnerImpl::RunBrowser(struct content::MainFunctionParams, bool) C:\chromium\src\content\app\content\_main\_runner\_impl.cc:1175:10  

#34 0x7ffe0cf2b3de in content::ContentMainRunnerImpl::Run(void) C:\chromium\src\content\app\content\_main\_runner\_impl.cc:1042:12  

#35 0x7ffe0cf27dab in content::RunContentProcess(struct content::ContentMainParams, class content::ContentMainRunner \*) C:\chromium\src\content\app\content\_main.cc:401:36  

#36 0x7ffe0cf28534 in content::ContentMain(struct content::ContentMainParams) C:\chromium\src\content\app\content\_main.cc:429:10  

#37 0x7ffe021314ca in ChromeMain C:\chromium\src\chrome\app\chrome\_main.cc:176:12  

#38 0x7ff761665b16 in MainDllLoader::Launch(struct HINSTANCE**\*, class base::TimeTicks) C:\chromium\src\chrome\app\main\_dll\_loader\_win.cc:167:12  

#39 0x7ff761662b5f in main C:\chromium\src\chrome\app\chrome\_exe\_main\_win.cc:382:20  

#40 0x7ff761a5d68b in invoke\_main d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:78  

#41 0x7ff761a5d68b in \_\_scrt\_common\_main\_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#42 0x7ffeeb247033 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  

#43 0x7ffeeba82650 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

0x12a6348b17f8 is located 8 bytes to the left of 14745600-byte region [0x12a6348b1800,0x12a6356c1800)  

allocated by thread T0 here:  

#0 0x7ff76170dd6b in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ffe0d432066 in base::UncheckedMalloc(unsigned \_\_int64, void \*\*) C:\chromium\src\base\process\memory\_win.cc:67:13  

#2 0x7ffe0d2dca9c in base::UncheckedCalloc(unsigned \_\_int64, unsigned \_\_int64, void \*\*) C:\chromium\src\base\process\memory.cc:86:8  

#3 0x7ffe0db9e336 in calloc\_nothrow C:\chromium\src\skia\ext\SkMemory\_new\_handler.cpp:108  

#4 0x7ffe0db9e336 in sk\_malloc\_flags(unsigned \_\_int64, unsigned int) C:\chromium\src\skia\ext\SkMemory\_new\_handler.cpp:119:14  

#5 0x7ffe029e73d2 in sk\_calloc\_canfail C:\chromium\src\third\_party\skia\include\private\SkMalloc.h:73  

#6 0x7ffe029e73d2 in SkMallocPixelRef::MakeAllocate(struct SkImageInfo const &, unsigned \_\_int64) C:\chromium\src\third\_party\skia\src\core\SkMallocPixelRef.cpp:42:18  

#7 0x7ffe0285766a in SkBitmap::tryAllocPixels(struct SkImageInfo const &, unsigned \_\_int64) C:\chromium\src\third\_party\skia\src\core\SkBitmap.cpp:265:28  

#8 0x7ffe02856826 in SkBitmap::allocPixels C:\chromium\src\third\_party\skia\src\core\SkBitmap.cpp:243  

#9 0x7ffe02856826 in SkBitmap::allocPixels C:\chromium\src\third\_party\skia\src\core\SkBitmap.cpp:247  

#10 0x7ffe02856826 in SkBitmap::allocN32Pixels(int, int, bool) C:\chromium\src\third\_party\skia\src\core\SkBitmap.cpp:222:11  

#11 0x7ffe1a99fba1 in EyeDropperView::ScreenCapturer::OnCaptureResult(enum webrtc::DesktopCapturer::Result, class std::\_\_1::unique\_ptr<class webrtc::DesktopFrame, struct std::\_\_1::default\_delete<class webrtc::DesktopFrame>>) C:\chromium\src\chrome\browser\ui\views\eye\_dropper\eye\_dropper\_view.cc:94:10  

#12 0x7ffe146520b2 in webrtc::FallbackDesktopCapturerWrapper::OnCaptureResult(enum webrtc::DesktopCapturer::Result, class std::\_\_1::unique\_ptr<class webrtc::DesktopFrame, struct std::\_\_1::default\_delete<class webrtc::DesktopFrame>>) C:\chromium\src\third\_party\webrtc\modules\desktop\_capture\fallback\_desktop\_capturer\_wrapper.cc:173:16  

#13 0x7ffe14650367 in std::\_\_1::unique\_ptr<webrtc::DesktopFrame,std::\_\_1::default\_delete[webrtc::DesktopFrame](javascript:void(0);) >::reset C:\chromium\src\buildtools\third\_party\libc++\trunk\include\_\_memory\unique\_ptr.h:313  

#14 0x7ffe14650367 in std::\_\_1::unique\_ptr<webrtc::DesktopFrame,std::\_\_1::default\_delete[webrtc::DesktopFrame](javascript:void(0);) >::~unique\_ptr C:\chromium\src\buildtools\third\_party\libc++\trunk\include\_\_memory\unique\_ptr.h:269  

#15 0x7ffe14650367 in webrtc::BlankDetectorDesktopCapturerWrapper::OnCaptureResult(enum webrtc::DesktopCapturer::Result, class std::\_\_1::unique\_ptr<class webrtc::DesktopFrame, struct std::\_\_1::default\_delete<class webrtc::DesktopFrame>>) C:\chromium\src\third\_party\webrtc\modules\desktop\_capture\blank\_detector\_desktop\_capturer\_wrapper.cc:97:1  

#16 0x7ffe1464f1a6 in webrtc::ScreenCapturerWinDirectx::CaptureFrame(void) C:\chromium\src\third\_party\webrtc\modules\desktop\_capture\win\screen\_capturer\_win\_directx.cc:160:18  

#17 0x7ffe1a99f8dd in EyeDropperView::ScreenCapturer::ScreenCapturer(void) C:\chromium\src\chrome\browser\ui\views\eye\_dropper\eye\_dropper\_view.cc:85:14  

#18 0x7ffe1a9a03eb in std::\_\_1::make\_unique C:\chromium\src\buildtools\third\_party\libc++\trunk\include\_\_memory\unique\_ptr.h:725  

#19 0x7ffe1a9a03eb in EyeDropperView::EyeDropperView(class content::RenderFrameHost \*, class content::EyeDropperListener \*) C:\chromium\src\chrome\browser\ui\views\eye\_dropper\eye\_dropper\_view.cc:150:24  

#20 0x7ffe177fdf39 in std::\_\_1::make\_unique C:\chromium\src\buildtools\third\_party\libc++\trunk\include\_\_memory\unique\_ptr.h:725  

#21 0x7ffe177fdf39 in ShowEyeDropper(class content::RenderFrameHost \*, class content::EyeDropperListener \*) C:\chromium\src\chrome\browser\ui\views\eye\_dropper\eye\_dropper\_view\_aura.cc:115:16  

#22 0x7ffe1344986b in BrowserView::OpenEyeDropper(class content::RenderFrameHost \*, class content::EyeDropperListener \*) C:\chromium\src\chrome\browser\ui\views\frame\browser\_view.cc:4079:10  

#23 0x7ffe0f92d945 in Browser::OpenEyeDropper(class content::RenderFrameHost \*, class content::EyeDropperListener \*) C:\chromium\src\chrome\browser\ui\browser.cc:1874:20  

#24 0x7ffe064b6000 in content::EyeDropperChooserImpl::Choose(class base::OnceCallback<(bool, unsigned int)>) C:\chromium\src\content\browser\eye\_dropper\_chooser\_impl.cc:59:30  

#25 0x7ffe04f1fe3c in blink::mojom::EyeDropperChooserStubDispatch::AcceptWithResponder(class blink::mojom::EyeDropperChooser \*, class mojo::Message \*, class std::\_\_1::unique\_ptr<class mojo::MessageReceiverWithStatus, struct std::\_\_1::default\_delete<class mojo::MessageReceiverWithStatus>>) C:\chromium\src\out\dev\_asan\gen\third\_party\blink\public\mojom\choosers\color\_chooser.mojom.cc:682:13  

#26 0x7ffe064b6b72 in blink::mojom::EyeDropperChooserStub<struct mojo::RawPtrImplRefTraits<class blink::mojom::EyeDropperChooser>>::AcceptWithResponder(class mojo::Message \*, class std::\_\_1::unique\_ptr<class mojo::MessageReceiverWithStatus, struct std::\_\_1::default\_delete<class mojo::MessageReceiverWithStatus>>) C:\chromium\src\out\dev\_asan\gen\third\_party\blink\public\mojom\choosers\color\_chooser.mojom.h:400:12  

#27 0x7ffe0d6ad8f3 in mojo::InterfaceEndpointClient::HandleValidatedMessage(class mojo::Message \*) C:\chromium\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:883:56  

#28 0x7ffe103390fe in mojo::MessageDispatcher::Accept(class mojo::Message \*) C:\chromium\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:43:19  

#29 0x7ffe0d6b1598 in mojo::InterfaceEndpointClient::HandleIncomingMessage(class mojo::Message \*) C:\chromium\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:663:20  

#30 0x7ffe0d6c583a in mojo::internal::MultiplexRouter::ProcessIncomingMessage(class mojo::internal::MultiplexRouter::MessageWrapper \*, enum mojo::internal::MultiplexRouter::ClientCallBehavior, class base::SequencedTaskRunner \*) C:\chromium\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc:1096:42  

#31 0x7ffe0d6c457e in mojo::internal::MultiplexRouter::Accept(class mojo::Message \*) C:\chromium\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc:716:7  

#32 0x7ffe103390fe in mojo::MessageDispatcher::Accept(class mojo::Message \*) C:\chromium\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:43:19  

#33 0x7ffe0d6a86f2 in mojo::Connector::DispatchMessageW(class mojo::ScopedHandleBase<class mojo::MessageHandle>) C:\chromium\src\mojo\public\cpp\bindings\lib\connector.cc:561:49  

#34 0x7ffe0d6a9e81 in mojo::Connector::ReadAllAvailableMessages(void) C:\chromium\src\mojo\public\cpp\bindings\lib\connector.cc:618:14  

#35 0x7ffe0d6fd02a in base::RepeatingCallback<void (unsigned int, const mojo::HandleSignalsState &)>::Run C:\chromium\src\base\callback.h:241  

#36 0x7ffe0d6fd02a in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, struct mojo::HandleSignalsState const &) C:\chromium\src\mojo\public\cpp\system\simple\_watcher.cc:278:14

SUMMARY: AddressSanitizer: heap-buffer-overflow C:\chromium\src\third\_party\skia\src\core\SkPixmap.cpp:326:30 in SkPixmap::getColor(int, int) const  

Shadow bytes around the buggy address:  

0x047ac65162a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x047ac65162b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x047ac65162c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x047ac65162d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x047ac65162e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x047ac65162f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa[fa]  

0x047ac6516300: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x047ac6516310: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x047ac6516320: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x047ac6516330: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x047ac6516340: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

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

==5892==ABORTING

**CREDIT INFORMATION**  

Reporter credit: Shih-Fong Peng (@\_L4ys) of TrapaSecurity

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 224 B)
- [scale_fix.diff](attachments/scale_fix.diff) (text/plain, 700 B)
- [msrc70076_chromium.txt](attachments/msrc70076_chromium.txt) (text/plain, 7.7 KB)
- [asan_eyedropper_100_chromium.txt](attachments/asan_eyedropper_100_chromium.txt) (text/plain, 14.5 KB)

## Timeline

### [Deleted User] (2022-03-16)

[Empty comment from Monorail migration]

### ad...@google.com (2022-03-17)

Hi iopopesc@microsoft.com, could you let us know the situation here? Our understanding is that MSRC say this is a Chromium bug, yet it's not reproducible in Chrome, only Edge. Is that right?

I'm labelling it as Security_Impact-None on the basis that it doesn't affect Chrome production versions. Rating as Security_Severity-High to match https://crbug.com/chromium/1246631 (though depending on whether it's readily exploitable, both issues could be Critical as they're browser crashes). Assuming this affects all the desktop platforms.

[Monorail components: Blink>Forms>Color]

### l4...@gmail.com (2022-03-17)

In case you need case number, it's MSRC-70566

### ad...@google.com (2022-03-24)

jonorman@, can you shed any light on this? Thanks!

### jo...@microsoft.com (2022-03-24)

when we got the report, it was tested against Chromium and found it was reproducible. Our normal workflow in those situations is to instruct the finder to report upstream. I do not have the original Chromium version we tested against, but we did keep the asan log which is attached. 

We reproduced using the following steps on Windows 
1. Run the EyeDropper
2. logout windows account with Win+L
3. Login again with password/PIN (not windows hello)

@Choongwoo did the original assessment and might have some perspective. 


### io...@microsoft.com (2022-03-24)

After https://crrev.com/a9082474c0f3633ef07438db9b5b10ad44bdb551 that landed in 101.0.4939.0, the EyeDropperView won't be impacted anymore by having negative coordinates due to scaling issues. 

### io...@microsoft.com (2022-03-24)

In terms of reproducing the crash, I wasn't able to reproduce it in neither Edge nor Chrome, so adetaylor@ I am going to let you decide if the fix from https://crbug.com/chromium/1306861#c6 should be cherry picked to other release branches.

### ad...@google.com (2022-03-25)

Thanks for the updates!

OK, so if this is reproducible in Chromium, I'm going to remove Security_Impact-None and replace it with a proper FoundIn label. It looks like this eyedropper code hasn't changed since September, so assuming this impacts all versions from Extended Stable onwards.

The fix in https://crbug.com/chromium/1306861#c6 (thanks pkasting@!) should be in M101+. So, ideally we will indeed backport this to M100. M98 is currently Extended Stable and M99 is stable, but only for a few more days, so let's not think about them.

iopopesc/pkasting - do you think it's riskier to backport the whole CL, or to just make a smaller change with the co-ordinate-related parts?

My instinct is to take the whole CL back to M100. It doesn't seem risky and it's had a few weeks to bake, so it's probably safer than creating a more specific patch.

If you agree then please just mark this as Fixed, and sheriffbot should add appropriate merge requests.

### [Deleted User] (2022-03-25)

[Empty comment from Monorail migration]

### pk...@chromium.org (2022-03-25)

I don't think we should take the whole patch, because the color pipeline bits are in active development and I don't know what state M100 was in.

I would just take the change to EyeDropperView::ScreenCapturer::GetColor(); that can stand alone.

If there's a way to reproduce in Chrome (#c5?) then it would be nice to handle better on trunk and/or update the comment in code describing how control can reach here.

### [Deleted User] (2022-03-27)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@microsoft.com (2022-03-29)

I tried the reproduction step in https://crbug.com/chromium/1306861#c5 again since it seems like I'm the only one who can reproduce. I could reproduce the same crash in M98, 99, 100, but it was very unreliable at this time. I could reproduce only once out of 30 trials for M100, so I couldn't debug how this happens. it may be some kind of race condition. It also sometimes makes the browser unresponsive.

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-09)

iopopesc: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### io...@microsoft.com (2022-04-12)

[Empty comment from Monorail migration]

### dc...@chromium.org (2022-04-14)

Since https://chromium-review.googlesource.com/c/chromium/src/+/3518451 fixed this, I'm going to mark this as fixed.

pkasting@ is out; it's not hard to cherry-pick just the coordinate fixes so I'll just assign to myself to get this off the security bug tracking sheet.

### dc...@chromium.org (2022-04-14)

I've filed a separate bug for the scaling issue as https://crbug.com/chromium/1316494.

### [Deleted User] (2022-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-15)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M100. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M101. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-15)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

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
Owners: benmason (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-15)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dc...@chromium.org (2022-04-15)

This does not need to be merged to M101. Proposed cherry-pick for M100 is https://chromium-review.googlesource.com/c/chromium/src/+/3588856.



### am...@chromium.org (2022-04-16)

since the original CL landed 11 March and the CP just landed today, approving merge of the CP to M100, please merge to branch 4896 at your earliest convenience so this can be included in Extended Stable cut on Tuesday -- thank you! 

### [Deleted User] (2022-04-19)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dc...@chromium.org (2022-04-19)

Ah I landed the merge yesterday but did not tag it with the right bug, sorry: https://chromium-review.googlesource.com/c/chromium/src/+/3588856

### am...@google.com (2022-04-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-04-22)

Congratulations, L4ys! The VRP Panel has decided to award you $7,000 for this report. While this issue does result in a memory corruption in the browser process, it is also mitigated by sufficient and specific user interaction. If you can demonstrate exploitation that does not require user interaction, we would be happy to reassess for a potentially higher reward amount. 
A member of our finance team will be in touch soon to arrange payment. Thank you for your efforts and reporting this issue to us!  

### am...@google.com (2022-04-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2022-12-13)

https://crbug.com/chromium/1306861#c26 says this was fixed in M100, but chromiumdash suggests it didn't quite make it into any of the M100 refreshes, so labelling this as fixed in M101.
l4ys.tw@ - very sorry that we didn't properly credit this in the release notes nor assign a CVE - we'll do so.

### l4...@gmail.com (2023-01-10)

 Hi, will I still get credit for this issue?

### pg...@google.com (2023-02-12)

[Empty comment from Monorail migration]

### pg...@google.com (2023-04-24)

Hi reporter@ sorry for the late reply - yes a CVE id has been reserved and this bug is queued up to be updated in the release notes! apologies for the delay!!

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1306861?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059112)*
