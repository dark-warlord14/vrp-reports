# Security: Heap-use-after-free in content::EyeDropperChooserImpl::ColorSelected() 

| Field | Value |
|-------|-------|
| **Issue ID** | [40056268](https://issues.chromium.org/issues/40056268) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P1 |
| **Component** | Blink>Forms>Color |
| **Reporter** | ch...@gmail.com |
| **Assignee** | io...@microsoft.com |
| **Created** | 2021-06-19 |
| **Bounty** | $10,000.00 |

## Description

Chrome Version: 93.0.4546.0 (Official Build) canary (x86\_64)

Operating System: All

**REPRODUCTION CASE**

1. Open the testcase
2. Click on the color icon
3. Click on the custom color then click anywhere in the page

==7470==ERROR: AddressSanitizer: heap-use-after-free on address 0x619000f0e070 at pc 0x5631a090d0c5 bp 0x7ffe8563e3c0 sp 0x7ffe8563e3b8  

READ of size 8 at 0x619000f0e070 thread T0 (chrome)  

==7470==WARNING: invalid path to external symbolizer!  

==7470==WARNING: Failed to use and restart external symbolizer!  

#0 0x5631a090d0c4 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x23a9b0c4)  

#1 0x5631a090d22d (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x23a9b22d)  

#2 0x56318cce9620 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0xfe77620)  

#3 0x5631a090b6d5 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x23a996d5)  

#4 0x563197cbfab7 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x1ae4dab7)  

#5 0x563197cbe2aa (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x1ae4c2aa)  

#6 0x563197cbd395 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x1ae4b395)  

#7 0x563197cbcef3 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x1ae4aef3)  

#8 0x56319a9cdc4d (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x1db5bc4d)  

#9 0x56319a9ec4ff (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x1db7a4ff)  

#10 0x56319a9ec1a3 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x1db7a1a3)  

#11 0x56319eecd387 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x2205b387)  

#12 0x56319eec7d16 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x22055d16)  

#13 0x563198e5da83 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x1bfeba83)  

#14 0x563198e5cd8f (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x1bfead8f)  

#15 0x563198e5dc9c (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x1bfebc9c)  

#16 0x56319790f2d4 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x1aa9d2d4)  

#17 0x563197e1caf4 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x1afaaaf4)  

#18 0x563188c5465a (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0xbde265a)  

#19 0x563188c536c1 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0xbde16c1)  

#20 0x563197e2b6d4 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x1afb96d4)  

#21 0x7f127e7ce04d (/lib/x86\_64-linux-gnu/libglib-2.0.so.0+0x5204d)

0x619000f0e070 is located 1008 bytes inside of 1032-byte region [0x619000f0dc80,0x619000f0e088)  

freed by thread T0 (chrome) here:  

#0 0x56318777327d (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0xa90127d)  

#1 0x56319ed71d08 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x21effd08)  

#2 0x56319ed720c8 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x21f000c8)  

#3 0x56319edee217 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x21f7c217)  

#4 0x56319ededa97 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x21f7ba97)  

#5 0x56319edee39d (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x21f7c39d)  

#6 0x56319eed902c (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x2206702c)  

#7 0x56319eed984d (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x2206784d)  

#8 0x56319eec810b (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x2205610b)  

#9 0x56319ef13b13 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x220a1b13)  

#10 0x56319edf3ea2 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x21f81ea2)  

#11 0x5631a090cf46 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x23a9af46)  

#12 0x5631a090d22d (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x23a9b22d)  

#13 0x56318cce9620 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0xfe77620)  

#14 0x5631a090b6d5 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x23a996d5)  

#15 0x563197cbfab7 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x1ae4dab7)  

#16 0x563197cbe2aa (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x1ae4c2aa)  

#17 0x563197cbd395 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x1ae4b395)  

#18 0x563197cbcef3 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x1ae4aef3)  

#19 0x56319a9cdc4d (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x1db5bc4d)  

#20 0x56319a9ec4ff (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x1db7a4ff)  

#21 0x56319a9ec1a3 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x1db7a1a3)  

#22 0x56319eecd387 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x2205b387)  

#23 0x56319eec7d16 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x22055d16)  

#24 0x563198e5da83 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x1bfeba83)  

#25 0x563198e5cd8f (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x1bfead8f)  

#26 0x563198e5dc9c (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x1bfebc9c)  

#27 0x56319790f2d4 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x1aa9d2d4)  

#28 0x563197e1caf4 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x1afaaaf4)  

#29 0x563188c5465a (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0xbde265a)

previously allocated by thread T0 (chrome) here:  

#0 0x563187772a1d (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0xa900a1d)  

#1 0x5631a090b949 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x23a99949)  

#2 0x56318cce8f38 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0xfe76f38)  

#3 0x56318b225ab3 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0xe3b3ab3)  

#4 0x56319625902f (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x193e702f)  

#5 0x56319626a5d1 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x193f85d1)  

#6 0x56319625ce85 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x193eae85)  

#7 0x563196276263 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x19404263)  

#8 0x5631962747b9 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x194027b9)  

#9 0x56319626a5d1 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x193f85d1)  

#10 0x5631962521e7 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x193e01e7)  

#11 0x563196253f30 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x193e1f30)  

#12 0x5631962bbbed (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x19449bed)  

#13 0x5631962bcbd4 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x1944abd4)  

#14 0x5631948b3340 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x17a41340)  

#15 0x5631948edb09 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x17a7bb09)  

#16 0x5631948ed27a (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x17a7b27a)  

#17 0x5631948ee4c1 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x17a7c4c1)  

#18 0x5631947a9819 (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x17937819)  

#19 0x7f127e7ce17c (/lib/x86\_64-linux-gnu/libglib-2.0.so.0+0x5217c)

SUMMARY: AddressSanitizer: heap-use-after-free (/home/lbstyle/Desktop/asan-linux-release-894027/chrome+0x23a9b0c4)  

Shadow bytes around the buggy address:  

0x0c32801d9bb0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c32801d9bc0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c32801d9bd0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c32801d9be0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c32801d9bf0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x0c32801d9c00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd[fd]fd  

0x0c32801d9c10: fd fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c32801d9c20: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c32801d9c30: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c32801d9c40: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c32801d9c50: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==7470==ABORTING

## Attachments

- [poc (4).html](attachments/poc (4).html) (text/plain, 20 B)
- [screen.mov](attachments/screen.mov) (video/quicktime, 5.0 MB)

## Timeline

### [Deleted User] (2021-06-19)

[Empty comment from Monorail migration]

### ch...@gmail.com (2021-06-19)

[Empty comment from Monorail migration]

### ts...@chromium.org (2021-06-19)

Symbolized trace looks like:
==3056162==ERROR: AddressSanitizer: heap-use-after-free on address 0x6190007a5770 at pc 0x55c23540a93e bp 0x7ffc21caff40 sp 0x7ffc21caff38
READ of size 8 at 0x6190007a5770 thread T0 (chrome)
    #0 0x55c23540a93d in reset buildtools/third_party/libc++/trunk/include/memory:1593:28
    #1 0x55c23540a93d in ~unique_ptr buildtools/third_party/libc++/trunk/include/memory:1550:19
    #2 0x55c23540a93d in EyeDropperView::~EyeDropperView() chrome/browser/ui/views/eye_dropper/eye_dropper_view.cc:142:1
    #3 0x55c23540ab58 in EyeDropperView::~EyeDropperView() chrome/browser/ui/views/eye_dropper/eye_dropper_view.cc:139:35
    #4 0x55c21e440c53 in operator() buildtools/third_party/libc++/trunk/include/memory:1335:5
    #5 0x55c21e440c53 in reset buildtools/third_party/libc++/trunk/include/memory:1596:7
    #6 0x55c21e440c53 in ColorSelected content/browser/eye_dropper_chooser_impl.cc:68:16
    #7 0x55c21e440c53 in non-virtual thunk to content::EyeDropperChooserImpl::ColorSelected(unsigned int) content/browser/eye_dropper_chooser_impl.cc
    #8 0x55c235408ad9 in EyeDropperView::PreEventDispatchHandler::OnMouseEvent(ui::MouseEvent*) chrome/browser/ui/views/eye_dropper/eye_dropper_view_aura.cc:31:12
    #9 0x55c22b5829f7 in ui::EventHandler::OnEvent(ui::Event*) ui/events/event_handler.cc
    #10 0x55c22b58098c in DispatchEvent ui/events/event_dispatcher.cc:191:12
    #11 0x55c22b58098c in ui::EventDispatcher::DispatchEventToEventHandlers(std::__1::vector<ui::EventHandler*, std::__1::allocator<ui::EventHandler*> >*, ui::Event*) ui/events/event_dispatcher.cc:178:7
    #12 0x55c22b57f752 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:126:3
    #13 0x55c22b57f1a0 in DispatchEventToTarget ui/events/event_dispatcher.cc:84:14
    #14 0x55c22b57f1a0 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:56:15
    #15 0x55c22ebf17ce in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:49:17
    #16 0x55c22ec16fcc in ui::EventSource::DeliverEventToSink(ui::Event*) ui/events/event_source.cc:113:16
    #17 0x55c22ec16c27 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const*, ui::EventRewriter const*) ui/events/event_source.cc:138:12
    #18 0x55c2335ec804 in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event*) ui/aura/window_tree_host_platform.cc:247:38
    #19 0x55c2335e618b in views::DesktopWindowTreeHostLinux::DispatchEvent(ui::Event*) ui/views/widget/desktop_aura/desktop_window_tree_host_linux.cc:273:29
    #20 0x55c22cb11b09 in ui::X11Window::DispatchUiEvent(ui::Event*, x11::Event const&) ui/platform_window/x11/x11_window.cc:1229:34
    #21 0x55c22cb10b9c in ui::X11Window::DispatchEvent(ui::Event* const&) ui/platform_window/x11/x11_window.cc:1175:3
    #22 0x55c22cb11f64 in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event* const&) ui/platform_window/x11/x11_window.cc
    #23 0x55c22b110798 in ui::PlatformEventSource::DispatchEvent(ui::Event*) ui/events/platform/platform_event_source.cc:97:29
    #24 0x55c22b66a3e2 in ui::X11EventSource::OnEvent(x11::Event const&) ui/events/platform/x11/x11_event_source.cc:291:5
    #25 0x55c21988c8ad in x11::Connection::DispatchEvent(x11::Event const&) ui/gfx/x/connection.cc:469:14
    #26 0x55c21988c01d in x11::Connection::ProcessNextEvent() ui/gfx/x/connection.cc:520:3
    #27 0x55c21988b3b0 in x11::Connection::Dispatch() ui/gfx/x/connection.cc
    #28 0x55c22b67c01c in ui::(anonymous namespace)::XSourceDispatch(_GSource*, int (*)(void*), void*) ui/events/platform/x11/x11_event_watcher_glib.cc:55:15
    #29 0x7f4c626c0d6e in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x51d6e)

0x6190007a5770 is located 1008 bytes inside of 1032-byte region [0x6190007a5380,0x6190007a5788)
freed by thread T0 (chrome) here:
    #0 0x55c217f58d5d in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:152:3
    #1 0x55c23344a117 in operator() buildtools/third_party/libc++/trunk/include/memory:1335:5
    #2 0x55c23344a117 in reset buildtools/third_party/libc++/trunk/include/memory:1596:7
    #3 0x55c23344a117 in ~unique_ptr buildtools/third_party/libc++/trunk/include/memory:1550:19
    #4 0x55c23344a117 in views::View::DoRemoveChildView(views::View*, bool, bool, views::View*) ui/views/view.cc:2601:1
    #5 0x55c23344a498 in views::View::RemoveAllChildViews(bool) ui/views/view.cc:315:5
    #6 0x55c2334de0f9 in views::Widget::DestroyRootView() ui/views/widget/widget.cc:1681:15
    #7 0x55c2334dd778 in views::Widget::~Widget() ui/views/widget/widget.cc:207:3
    #8 0x55c2334de2d8 in views::Widget::~Widget() ui/views/widget/widget.cc:188:19
    #9 0x55c2335fa5fd in views::DesktopNativeWidgetAura::~DesktopNativeWidgetAura() ui/views/widget/desktop_aura/desktop_native_widget_aura.cc:279:5
    #10 0x55c2335fb0d8 in views::DesktopNativeWidgetAura::~DesktopNativeWidgetAura() ui/views/widget/desktop_aura/desktop_native_widget_aura.cc:277:53
    #11 0x55c2335e65c7 in views::DesktopWindowTreeHostLinux::OnClosed() ui/views/widget/desktop_aura/desktop_window_tree_host_linux.cc:279:34
    #12 0x55c233641428 in views::DesktopWindowTreeHostPlatform::CloseNow() ui/views/widget/desktop_aura/desktop_window_tree_host_platform.cc:329:22
    #13 0x55c2334e5892 in views::Widget::CloseNow() ui/views/widget/widget.cc:687:19
    #14 0x55c23540a762 in EyeDropperView::~EyeDropperView() chrome/browser/ui/views/eye_dropper/eye_dropper_view.cc:141:18
    #15 0x55c23540ab58 in EyeDropperView::~EyeDropperView() chrome/browser/ui/views/eye_dropper/eye_dropper_view.cc:139:35
    #16 0x55c21e440c53 in operator() buildtools/third_party/libc++/trunk/include/memory:1335:5
    #17 0x55c21e440c53 in reset buildtools/third_party/libc++/trunk/include/memory:1596:7
    #18 0x55c21e440c53 in ColorSelected content/browser/eye_dropper_chooser_impl.cc:68:16
    #19 0x55c21e440c53 in non-virtual thunk to content::EyeDropperChooserImpl::ColorSelected(unsigned int) content/browser/eye_dropper_chooser_impl.cc
    #20 0x55c235408ad9 in EyeDropperView::PreEventDispatchHandler::OnMouseEvent(ui::MouseEvent*) chrome/browser/ui/views/eye_dropper/eye_dropper_view_aura.cc:31:12
    #21 0x55c22b5829f7 in ui::EventHandler::OnEvent(ui::Event*) ui/events/event_handler.cc
    #22 0x55c22b58098c in DispatchEvent ui/events/event_dispatcher.cc:191:12
    #23 0x55c22b58098c in ui::EventDispatcher::DispatchEventToEventHandlers(std::__1::vector<ui::EventHandler*, std::__1::allocator<ui::EventHandler*> >*, ui::Event*) ui/events/event_dispatcher.cc:178:7
    #24 0x55c22b57f752 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:126:3
    #25 0x55c22b57f1a0 in DispatchEventToTarget ui/events/event_dispatcher.cc:84:14
    #26 0x55c22b57f1a0 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:56:15
    #27 0x55c22ebf17ce in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:49:17
    #28 0x55c22ec16fcc in ui::EventSource::DeliverEventToSink(ui::Event*) ui/events/event_source.cc:113:16
    #29 0x55c22ec16c27 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const*, ui::EventRewriter const*) ui/events/event_source.cc:138:12
    #30 0x55c2335ec804 in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event*) ui/aura/window_tree_host_platform.cc:247:38
    #31 0x55c2335e618b in views::DesktopWindowTreeHostLinux::DispatchEvent(ui::Event*) ui/views/widget/desktop_aura/desktop_window_tree_host_linux.cc:273:29
    #32 0x55c22cb11b09 in ui::X11Window::DispatchUiEvent(ui::Event*, x11::Event const&) ui/platform_window/x11/x11_window.cc:1229:34
    #33 0x55c22cb10b9c in ui::X11Window::DispatchEvent(ui::Event* const&) ui/platform_window/x11/x11_window.cc:1175:3
    #34 0x55c22cb11f64 in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event* const&) ui/platform_window/x11/x11_window.cc
    #35 0x55c22b110798 in ui::PlatformEventSource::DispatchEvent(ui::Event*) ui/events/platform/platform_event_source.cc:97:29
    #36 0x55c22b66a3e2 in ui::X11EventSource::OnEvent(x11::Event const&) ui/events/platform/x11/x11_event_source.cc:291:5
    #37 0x55c21988c8ad in x11::Connection::DispatchEvent(x11::Event const&) ui/gfx/x/connection.cc:469:14

previously allocated by thread T0 (chrome) here:
    #0 0x55c217f584fd in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95:3
    #1 0x55c235408e41 in make_unique<EyeDropperView, content::RenderFrameHost *&, content::EyeDropperListener *&> buildtools/third_party/libc++/trunk/include/memory:2006:28
    #2 0x55c235408e41 in ShowEyeDropper(content::RenderFrameHost*, content::EyeDropperListener*) chrome/browser/ui/views/eye_dropper/eye_dropper_view_aura.cc:71:10
    #3 0x55c21e440449 in content::EyeDropperChooserImpl::Choose(base::OnceCallback<void (bool, unsigned int)>) content/browser/eye_dropper_chooser_impl.cc:59:30
    #4 0x55c21c499144 in blink::mojom::EyeDropperChooserStubDispatch::AcceptWithResponder(blink::mojom::EyeDropperChooser*, mojo::Message*, std::__1::unique_ptr<mojo::MessageReceiverWithStatus, std::__1::default_delete<mojo::MessageReceiverWithStatus> >) gen/third_party/blink/public/mojom/choosers/color_chooser.mojom.cc:729:13
    #5 0x55c229598e26 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:835:56
    #6 0x55c2295ad839 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #7 0x55c22959d6e3 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:648:21
    #8 0x55c2295bd169 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:1083:42
    #9 0x55c2295baf13 in mojo::internal::MultiplexRouter::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/multiplex_router.cc:712:7
    #10 0x55c2295ad839 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #11 0x55c229590d92 in mojo::Connector::DispatchMessage(mojo::Message) mojo/public/cpp/bindings/lib/connector.cc:548:49
    #12 0x55c229592ec4 in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:606:14
    #13 0x55c22960f7e3 in Run base/callback.h:166:12
    #14 0x55c22960f7e3 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple_watcher.cc:278:14
    #15 0x55c229610798 in Invoke<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> base/bind_internal.h:509:12
    #16 0x55c229610798 in MakeItSo<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> base/bind_internal.h:668:5
    #17 0x55c229610798 in RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), std::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0UL, 1UL, 2UL, 3UL> base/bind_internal.h:721:12
    #18 0x55c229610798 in base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:690:12
    #19 0x55c227706ce6 in Run base/callback.h:98:12
    #20 0x55c227706ce6 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:178:33
    #21 0x55c22774d751 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:360:23
    #22 0x55c22774ccc7 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:260:36
    #23 0x55c22774e2dc in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #24 0x55c2275bf628 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:405:48
    #25 0x55c22774eb59 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:467:12
    #26 0x55c2276687c4 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14
    #27 0x55c21df16fac in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:999:18
    #28 0x55c21df1cb9d in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:152:15
    #29 0x55c21df0fbda in content::BrowserMain(content::MainFunctionParams const&) content/browser/browser_main.cc:47:28
    #30 0x55c2272ff8b9 in RunBrowserProcessMain content/app/content_main_runner_impl.cc:598:10
    #31 0x55c2272ff8b9 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content/app/content_main_runner_impl.cc:1087:10
    #32 0x55c2272fe84e in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:956:12
    #33 0x55c2272f7cbd in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) content/app/content_main.cc:386:36
    #34 0x55c2272f8277 in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:412:10
    #35 0x55c217f5b081 in ChromeMain chrome/app/chrome_main.cc:151:12
    #36 0x7f4c60d0cd09 in __libc_start_main csu/../csu/libc-start.c:308:16



### ts...@chromium.org (2021-06-19)

May be tough to get a CF repro due to needing to know location for the gestures, trying anyway.


### cl...@chromium.org (2021-06-19)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4784865160265728.

### ts...@chromium.org (2021-06-19)

Assigning per eye dropper OWNERS.

### ts...@chromium.org (2021-06-19)

Might be sev-high for UaF in browser, but mitigated by gestures.

[Monorail components: Blink>Forms>Color]

### [Deleted User] (2021-06-20)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### io...@microsoft.com (2021-06-22)

[Empty comment from Monorail migration]

### ch...@gmail.com (2021-07-01)

Any update on this bug? Thanks.

### ch...@gmail.com (2021-07-05)

This seems like fixed in https://crbug.com/chromium/1224350. 

### ch...@gmail.com (2021-07-05)

To whoever sees this, note that this bug is older than https://crbug.com/chromium/1224350.

### [Deleted User] (2021-07-06)

iopopesc: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### io...@microsoft.com (2021-07-07)

This is indeed a duplicate of http://crbug.com/1224350. Note that the CL that introduced the regression (https://chromium-review.googlesource.com/c/chromium/src/+/2966804) landed on Jun 17, before this issue was opened.

### ch...@gmail.com (2021-07-07)

Thanks for the update!

>> Note that the CL that introduced the regression (https://chromium-review.googlesource.com/c/chromium/src/+/2966804) landed on Jun 17, before this issue was opened. 

Because this is a regression crash from https://chromium-review.googlesource.com/c/chromium/src/+/2966804 (there was no crash before revision #893451). 

### aw...@google.com (2021-07-07)

Adding reward-topanel to take a look since this was a forward dupe

### [Deleted User] (2021-07-07)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-08-25)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-08-25)

Congratulations, Khalil on another one! The VRP Panel has decided to award you $10,000 for this report. Nice find! 

### am...@google.com (2021-08-27)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-10-13)

This issue was migrated from crbug.com/chromium/1221746?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1222112]
[Monorail mergedinto: crbug.com/chromium/1224350]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056268)*
