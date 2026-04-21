# Security: Heap-use-after-free in ui::MenuModel::GetModelAndIndexForCommandId

| Field | Value |
|-------|-------|
| **Issue ID** | [40058166](https://issues.chromium.org/issues/40058166) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | me...@gmail.com |
| **Assignee** | el...@chromium.org |
| **Created** | 2021-12-09 |
| **Bounty** | $10,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36

Steps to reproduce the problem:
1. download asan-linux-release-949870.zip and unzip
2. start a server at poc.html : `python -m SimpleHTTPServer 8605`
3. ./chrome http://127.0.0.1:8605/poc.html about:blank
4. right click the address bar to show the menu, after the tab is closed, move your cursor to the menu

What is the expected behavior?

What went wrong?
UAF occurs:

=================================================================
==1844193==ERROR: AddressSanitizer: heap-use-after-free on address 0x611000483f40 at pc 0x559e217eb0d6 bp 0x7ffe9085be50 sp 0x7ffe9085be48
READ of size 8 at 0x611000483f40 thread T0 (chrome)
    #0 0x559e217eb0d5 in ui::MenuModel::GetModelAndIndexForCommandId(int, ui::MenuModel**, int*) ui/base/models/menu_model.cc:38:36
    #1 0x559e217eaec4 in ui::MenuModel::GetModelAndIndexForCommandId(int, ui::MenuModel**, int*) ui/base/models/menu_model.cc:50:11
    #2 0x559e2a24f652 in views::MenuModelAdapter::GetLabelFontList(int) const ui/views/controls/menu/menu_model_adapter.cc:208:7
    #3 0x559e2a2317f9 in views::MenuItemView::GetFontList() const ui/views/controls/menu/menu_item_view.cc:939:23
    #4 0x559e2a22b00a in views::MenuItemView::OnPaintImpl(gfx::Canvas*, views::MenuItemView::PaintMode) ui/views/controls/menu/menu_item_view.cc:1010:36
    #5 0x559e2a36f968 in views::View::Paint(views::PaintInfo const&) ui/views/view.cc:1194:5
    #6 0x559e2a379136 in RecursivePaintHelper ui/views/view.cc:2459:7
    #7 0x559e2a379136 in views::View::PaintChildren(views::PaintInfo const&) ui/views/view.cc:1958:3
    #8 0x559e2a2561bc in views::SubmenuView::PaintChildren(views::PaintInfo const&) ui/views/controls/menu/submenu_view.cc:218:9
    #9 0x559e2a36facf in views::View::Paint(views::PaintInfo const&) ui/views/view.cc:1200:3
    #10 0x559e2a379136 in RecursivePaintHelper ui/views/view.cc:2459:7
    #11 0x559e2a379136 in views::View::PaintChildren(views::PaintInfo const&) ui/views/view.cc:1958:3
    #12 0x559e2a36facf in views::View::Paint(views::PaintInfo const&) ui/views/view.cc:1200:3
    #13 0x559e2a379136 in RecursivePaintHelper ui/views/view.cc:2459:7
    #14 0x559e2a379136 in views::View::PaintChildren(views::PaintInfo const&) ui/views/view.cc:1958:3
    #15 0x559e2a36facf in views::View::Paint(views::PaintInfo const&) ui/views/view.cc:1200:3
    #16 0x559e2a379136 in RecursivePaintHelper ui/views/view.cc:2459:7
    #17 0x559e2a379136 in views::View::PaintChildren(views::PaintInfo const&) ui/views/view.cc:1958:3
    #18 0x559e2a36facf in views::View::Paint(views::PaintInfo const&) ui/views/view.cc:1200:3
    #19 0x559e2a37c62c in views::View::PaintFromPaintRoot(ui::PaintContext const&) ui/views/view.cc:2466:3
    #20 0x559e25bc898d in ui::Layer::PaintContentsToDisplayList() ui/compositor/layer.cc:1329:16
    #21 0x559e24e29f7a in cc::PictureLayer::Update() cc/layers/picture_layer.cc:150:41
    #22 0x559e24f14fcf in PaintContent cc/trees/layer_tree_host.cc:1464:33
    #23 0x559e24f14fcf in cc::LayerTreeHost::DoUpdateLayers() cc/trees/layer_tree_host.cc:832:28
    #24 0x559e24f1474e in cc::LayerTreeHost::UpdateLayers() cc/trees/layer_tree_host.cc:701:17
    #25 0x559e2516c8b1 in cc::SingleThreadProxy::DoPainting(viz::BeginFrameArgs const&) cc/trees/single_thread_proxy.cc:941:21
    #26 0x559e2516e235 in cc::SingleThreadProxy::BeginMainFrame(viz::BeginFrameArgs const&) cc/trees/single_thread_proxy.cc:907:3
    #27 0x559e2516fdec in Invoke<void (cc::SingleThreadProxy::*)(const viz::BeginFrameArgs &), base::WeakPtr<cc::SingleThreadProxy>, viz::BeginFrameArgs> base/bind_internal.h:535:12
    #28 0x559e2516fdec in MakeItSo<void (cc::SingleThreadProxy::*)(const viz::BeginFrameArgs &), base::WeakPtr<cc::SingleThreadProxy>, viz::BeginFrameArgs> base/bind_internal.h:719:5
    #29 0x559e2516fdec in RunImpl<void (cc::SingleThreadProxy::*)(const viz::BeginFrameArgs &), std::__1::tuple<base::WeakPtr<cc::SingleThreadProxy>, viz::BeginFrameArgs>, 0UL, 1UL> base/bind_internal.h:772:12
    #30 0x559e2516fdec in base::internal::Invoker<base::internal::BindState<void (cc::SingleThreadProxy::*)(viz::BeginFrameArgs const&), base::WeakPtr<cc::SingleThreadProxy>, viz::BeginFrameArgs>, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:741:12
    #31 0x559e20ad85d3 in Run base/callback.h:142:12
    #32 0x559e20ad85d3 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:135:32
    #33 0x559e20b176a3 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:358:29)> base/task/common/task_annotator.h:74:5
    #34 0x559e20b176a3 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:356:21
    #35 0x559e20b16eb7 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:261:30
    #36 0x559e20b18271 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #37 0x559e209cf6b9 in HandleDispatch base/message_loop/message_pump_glib.cc:375:46
    #38 0x559e209cf6b9 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:125:43
    #39 0x7f7d1296317c in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x5217c)

0x611000483f40 is located 0 bytes inside of 256-byte region [0x611000483f40,0x611000484040)
freed by thread T0 (chrome) here:
    #0 0x559e1278748d in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:152:3
    #1 0x559e2ba93361 in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #2 0x559e2ba93361 in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #3 0x559e2ba93361 in OmniboxViewViews::OnTabChanged(content::WebContents*) chrome/browser/ui/views/omnibox/omnibox_view_views.cc:261:24
    #4 0x559e2b93367b in LocationBarView::Update(content::WebContents*) chrome/browser/ui/views/location_bar/location_bar_view.cc:803:20
    #5 0x559e2bf18d71 in ToolbarView::Update(content::WebContents*) chrome/browser/ui/views/toolbar/toolbar_view.cc:422:20
    #6 0x559e2aede8f6 in UpdateToolbar chrome/browser/ui/browser.cc:2469:12
    #7 0x559e2aede8f6 in Browser::OnActiveTabChanged(content::WebContents*, content::WebContents*, int, int) chrome/browser/ui/browser.cc:2381:3
    #8 0x559e2aedd8ee in Browser::OnTabStripModelChanged(TabStripModel*, TabStripModelChange const&, TabStripSelectionChange const&) chrome/browser/ui/browser.cc:1186:3
    #9 0x559e2b0a62d8 in TabStripModel::SendDetachWebContentsNotifications(TabStripModel::DetachNotifications*) chrome/browser/ui/tabs/tab_strip_model.cc:534:16
    #10 0x559e2b0af266 in TabStripModel::CloseTabs(base::span<content::WebContents* const, 18446744073709551615ul>, unsigned int) chrome/browser/ui/tabs/tab_strip_model.cc:1782:5
    #11 0x559e2b0b0721 in TabStripModel::CloseWebContentsAt(int, unsigned int) chrome/browser/ui/tabs/tab_strip_model.cc:752:10
    #12 0x559e188f9617 in Close content/browser/web_contents/web_contents_impl.cc:7164:16
    #13 0x559e188f9617 in non-virtual thunk to content::WebContentsImpl::Close(content::RenderViewHost*) content/browser/web_contents/web_contents_impl.cc
    #14 0x559e15dcaa8b in blink::mojom::LocalMainFrameHostStubDispatch::Accept(blink::mojom::LocalMainFrameHost*, mojo::Message*) gen/third_party/blink/public/mojom/frame/frame.mojom.cc:18887:13
    #15 0x559e21615c74 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:900:54
    #16 0x559e216281a2 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:48:24
    #17 0x559e21619f37 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:657:20
    #18 0x559e22f0b441 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ipc/ipc_mojo_bootstrap.cc:1008:24
    #19 0x559e22f03a84 in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind_internal.h:535:12
    #20 0x559e22f03a84 in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind_internal.h:699:12
    #21 0x559e22f03a84 in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), std::__1::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> base/bind_internal.h:772:12
    #22 0x559e22f03a84 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:741:12
    #23 0x559e20ad85d3 in Run base/callback.h:142:12
    #24 0x559e20ad85d3 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:135:32
    #25 0x559e20b176a3 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:358:29)> base/task/common/task_annotator.h:74:5
    #26 0x559e20b176a3 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:356:21
    #27 0x559e20b16eb7 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:261:30
    #28 0x559e20b18271 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #29 0x559e209cf6b9 in HandleDispatch base/message_loop/message_pump_glib.cc:375:46
    #30 0x559e209cf6b9 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:125:43
    #31 0x7f7d1296317c in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x5217c)

previously allocated by thread T0 (chrome) here:
    #0 0x559e12786c2d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95:3
    #1 0x559e2baa8991 in std::__1::__unique_if<share::ShareSubmenuModel>::__unique_single std::__1::make_unique<share::ShareSubmenuModel, content::WebContents*&, std::__1::unique_ptr<ui::DataTransferEndpoint, std::__1::default_delete<ui::DataTransferEndpoint> >, share::ShareSubmenuModel::Context, GURL const&, std::__1::basic_string<char16_t, std::__1::char_traits<char16_t>, std::__1::allocator<char16_t> > const&>(content::WebContents*&, std::__1::unique_ptr<ui::DataTransferEndpoint, std::__1::default_delete<ui::DataTransferEndpoint> >&&, share::ShareSubmenuModel::Context&&, GURL const&, std::__1::basic_string<char16_t, std::__1::char_traits<char16_t>, std::__1::allocator<char16_t> > const&) buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:725:28
    #2 0x559e2baa762a in OmniboxViewViews::MaybeAddShareSubmenu(ui::SimpleMenuModel*) chrome/browser/ui/views/omnibox/omnibox_view_views.cc:1928:26
    #3 0x559e2baa704a in OmniboxViewViews::UpdateContextMenu(ui::SimpleMenuModel*) chrome/browser/ui/views/omnibox/omnibox_view_views.cc:1806:5
    #4 0x559e2a277573 in views::Textfield::UpdateContextMenu() ui/views/controls/textfield/textfield.cc:2533:18
    #5 0x559e2a27787b in ShowContextMenuForViewImpl ui/views/controls/textfield/textfield.cc:1114:3
    #6 0x559e2a27787b in non-virtual thunk to views::Textfield::ShowContextMenuForViewImpl(views::View*, gfx::Point const&, ui::MenuSourceType) ui/views/controls/textfield/textfield.cc
    #7 0x559e2a1eb23f in views::ContextMenuController::ShowContextMenuForView(views::View*, gfx::Point const&, ui::MenuSourceType) ui/views/context_menu_controller.cc:29:3
    #8 0x559e2a373bec in views::View::ProcessMousePressed(ui::MouseEvent const&) ui/views/view.cc:3022:7
    #9 0x559e2a3735ee in views::View::OnMouseEvent(ui::MouseEvent*) ui/views/view.cc:1436:11
    #10 0x559e22ff9095 in DispatchEvent ui/events/event_dispatcher.cc:190:12
    #11 0x559e22ff9095 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:139:5
    #12 0x559e22ff894c in DispatchEventToTarget ui/events/event_dispatcher.cc:83:14
    #13 0x559e22ff894c in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:55:15
    #14 0x559e2a3b365f in views::internal::RootView::OnMousePressed(ui::MouseEvent const&) ui/views/widget/root_view.cc:418:9
    #15 0x559e2a3d4795 in views::Widget::OnMouseEvent(ui::MouseEvent*) ui/views/widget/widget.cc:1522:35
    #16 0x559e22ff9095 in DispatchEvent ui/events/event_dispatcher.cc:190:12
    #17 0x559e22ff9095 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:139:5
    #18 0x559e22ff894c in DispatchEventToTarget ui/events/event_dispatcher.cc:83:14
    #19 0x559e22ff894c in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:55:15
    #20 0x559e25b5ea8d in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:49:17
    #21 0x559e25b7e59f in ui::EventSource::DeliverEventToSink(ui::Event*) ui/events/event_source.cc:118:16
    #22 0x559e25b7e199 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const*, ui::EventRewriter const*) ui/events/event_source.cc:143:12
    #23 0x559e2a4abed7 in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event*) ui/aura/window_tree_host_platform.cc:230:38
    #24 0x559e2a4a6250 in views::DesktopWindowTreeHostLinux::DispatchEvent(ui::Event*) ui/views/widget/desktop_aura/desktop_window_tree_host_linux.cc:284:29
    #25 0x559e23005cad in Run base/callback.h:142:12
    #26 0x559e23005cad in ui::DispatchEventFromNativeUiEvent(ui::Event* const&, base::OnceCallback<void (ui::Event*)>) ui/events/ozone/events_ozone.cc:36:25
    #27 0x559e245244b2 in ui::X11Window::DispatchUiEvent(ui::Event*, x11::Event const&) ui/platform_window/x11/x11_window.cc:1304:3
    #28 0x559e2452385f in ui::X11Window::DispatchEvent(ui::Event* const&) ui/platform_window/x11/x11_window.cc:1257:3
    #29 0x559e2452469c in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event* const&) ui/platform_window/x11/x11_window.cc
    #30 0x559e22fd6954 in ui::PlatformEventSource::DispatchEvent(ui::Event*) ui/events/platform/platform_event_source.cc:98:29
    #31 0x559e24386fa4 in ui::X11EventSource::OnEvent(x11::Event const&) ui/events/platform/x11/x11_event_source.cc:287:5
    #32 0x559e13d8229a in x11::Connection::DispatchEvent(x11::Event const&) ui/gfx/x/connection.cc:469:14
    #33 0x559e13d81301 in ProcessNextEvent ui/gfx/x/connection.cc:520:3
    #34 0x559e13d81301 in x11::Connection::Dispatch() ui/gfx/x/connection.cc:446:5
    #35 0x559e24395064 in ui::(anonymous namespace)::XSourceDispatch(_GSource*, int (*)(void*), void*) ui/events/platform/x11/x11_event_watcher_glib.cc:55:15
    #36 0x7f7d1296304d in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x5204d)

SUMMARY: AddressSanitizer: heap-use-after-free ui/base/models/menu_model.cc:38:36 in ui::MenuModel::GetModelAndIndexForCommandId(int, ui::MenuModel**, int*)
Shadow bytes around the buggy address:
  0x0c2280088790: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c22800887a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c22800887b0: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x0c22800887c0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c22800887d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa
=>0x0c22800887e0: fa fa fa fa fa fa fa fa[fd]fd fd fd fd fd fd fd
  0x0c22800887f0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2280088800: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
  0x0c2280088810: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2280088820: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa
  0x0c2280088830: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
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
==1844193==ABORTING

Did this work before? N/A 

Chrome version: 94.0.4606.81  Channel: n/a
OS Version:

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 61 B)
- [video.webm](attachments/video.webm) (video/webm, 4.0 MB)

## Timeline

### [Deleted User] (2021-12-09)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-12-09)

+views folks. This is a browser process UaF, can you please urgently investigate.

Normally these are Critical severity; this needs a somewhat unusual interaction (closing a tab via JavaScript while the location bar context menu is open), so I'm downgrading to High, but I could be convinced to keep it at Critical.

[Monorail components: Internals>Views]

### do...@chromium.org (2021-12-09)

Also, it's unclear to me when this vulnerability was first introduced. Going to set to stable; if you narrow the source down, please indicate which commit introduced the issue. Thanks!

### [Deleted User] (2021-12-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-09)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-09)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@gmail.com (2021-12-10)

When the current tab is closed, `OmniboxViewViews::OnTabChanged`[1] will be called, which will reset and delete `share_submenu_model_`. However the right click menu UI is still shown. If we choose one of the submenu, `MenuModel::GetModelAndIndexForCommandId`[2] will be called, and submenu_model is used after free.

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/omnibox/omnibox_view_views.cc;l=261;drc=3f96b0a4cf8cc23144504482446a088f0dcc023e;bpv=0;bpt=0 
[2] https://source.chromium.org/chromium/chromium/src/+/main:ui/base/models/menu_model.cc;l=38;drc=272ac63fa83bec4585544eee14596c90ca3cfcb5;bpv=0;bpt=0

### do...@chromium.org (2021-12-10)

Shifting to the omnibox team

[Monorail components: -Internals>Views UI>Browser>Omnibox]

### el...@chromium.org (2021-12-10)

This and https://crbug.com/chromium/1278613 are basically the same problem, just with different submenus, and these are likely to need the same fix. I'll take this one as well.

### gi...@appspot.gserviceaccount.com (2021-12-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a3393ce39586558f74b4fd57495bfdd66a6b564b

commit a3393ce39586558f74b4fd57495bfdd66a6b564b
Author: Elly Fong-Jones <ellyjones@chromium.org>
Date: Wed Dec 15 20:20:30 2021

omnibox: close menu when invalidating parts of its model

The omnibox context menu's root menu is owned by Textfield,
but some submenus are owned by OmniboxViewViews, and only
OmniboxViewViews knows when they're destroyed. If that happens,
ask Textfield to close any running context menu and also
reset the root menu model, since it holds references to the now-
destroyed submenu models.

Fixed: 1278613,1278180
Bug: 1278942
Change-Id: If3df10d56501f975ce408e60538cc4652f5472e6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3330922
Reviewed-by: Justin Donnelly <jdonnelly@chromium.org>
Commit-Queue: Elly Fong-Jones <ellyjones@chromium.org>
Auto-Submit: Elly Fong-Jones <ellyjones@chromium.org>
Cr-Commit-Position: refs/heads/main@{#952052}

[modify] https://crrev.com/a3393ce39586558f74b4fd57495bfdd66a6b564b/ui/views/controls/textfield/textfield.cc
[modify] https://crrev.com/a3393ce39586558f74b4fd57495bfdd66a6b564b/ui/views/controls/textfield/textfield.h
[modify] https://crrev.com/a3393ce39586558f74b4fd57495bfdd66a6b564b/chrome/browser/ui/views/omnibox/omnibox_view_views.cc


### [Deleted User] (2021-12-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-16)

Requesting merge to stable M96 because latest trunk commit (952052) appears to be after stable branch point (929512).

Requesting merge to beta M97 because latest trunk commit (952052) appears to be after beta branch point (938553).

Requesting merge to dev M98 because latest trunk commit (952052) appears to be after dev branch point (950365).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-16)

Merge approved: your change passed merge requirements and is auto-approved for M98. Please go ahead and merge the CL to branch 4758 (refs/branch-heads/4758) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-16)

Merge review required: M97 has already been cut for stable release.

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

### [Deleted User] (2021-12-16)

Merge review required: M96 is already shipping to stable.

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

### me...@gmail.com (2021-12-20)

Hi, I want to change my Credit info to:

Weipeng Jiang (@Krace) and Guang Gong of 360 Vulnerability Research Institute

Thank you.

### [Deleted User] (2021-12-20)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-12-21)

merge approved to M98 prior, please merge to branch 4758 
merge approved to M97, please merge to branch 4692 at your earliest convenience 
merge also approved to M96, please merge to branch 4664 as well; while there are no further planned releases of M96 it will go into Extended Stable 4 January, so this should be merged accordingly

Thanks! :) 

### [Deleted User] (2021-12-27)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2021-12-29)

I tried to CP to M97/M96 branches but they had merge conflicts so this change will not be part of first M97 stable promotion or extended stable release next week.

### el...@chromium.org (2022-01-04)

I'll do these merges today.

### el...@chromium.org (2022-01-04)

[Empty comment from Monorail migration]

### el...@chromium.org (2022-01-04)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-01-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ecf38d17dba552c9802d4580e49e635340d20b72

commit ecf38d17dba552c9802d4580e49e635340d20b72
Author: Elly Fong-Jones <ellyjones@chromium.org>
Date: Tue Jan 04 21:14:42 2022

[M98] omnibox: close menu when invalidating parts of its model

The omnibox context menu's root menu is owned by Textfield,
but some submenus are owned by OmniboxViewViews, and only
OmniboxViewViews knows when they're destroyed. If that happens,
ask Textfield to close any running context menu and also
reset the root menu model, since it holds references to the now-
destroyed submenu models.

(cherry picked from commit a3393ce39586558f74b4fd57495bfdd66a6b564b)

Fixed: 1278613,1278180
Bug: 1278942
Change-Id: If3df10d56501f975ce408e60538cc4652f5472e6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3330922
Reviewed-by: Justin Donnelly <jdonnelly@chromium.org>
Commit-Queue: Elly Fong-Jones <ellyjones@chromium.org>
Auto-Submit: Elly Fong-Jones <ellyjones@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#952052}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3365380
Reviewed-by: Jeffrey Cohen <jeffreycohen@chromium.org>
Commit-Queue: Jeffrey Cohen <jeffreycohen@chromium.org>
Cr-Commit-Position: refs/branch-heads/4758@{#318}
Cr-Branched-From: 4a2cf4baf90326df19c3ee70ff987960d59a386e-refs/heads/main@{#950365}

[modify] https://crrev.com/ecf38d17dba552c9802d4580e49e635340d20b72/ui/views/controls/textfield/textfield.cc
[modify] https://crrev.com/ecf38d17dba552c9802d4580e49e635340d20b72/ui/views/controls/textfield/textfield.h
[modify] https://crrev.com/ecf38d17dba552c9802d4580e49e635340d20b72/chrome/browser/ui/views/omnibox/omnibox_view_views.cc


### gi...@appspot.gserviceaccount.com (2022-01-04)

https://crbug.com/chromium/1278613 has been un-merged from this issue.


### gi...@appspot.gserviceaccount.com (2022-01-04)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-01-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bd367fdccc0f9d19989f0c02312c27c60511acd7

commit bd367fdccc0f9d19989f0c02312c27c60511acd7
Author: Elly Fong-Jones <ellyjones@chromium.org>
Date: Tue Jan 04 22:52:35 2022

[M96] omnibox: close menu when invalidating parts of its model

The omnibox context menu's root menu is owned by Textfield,
but some submenus are owned by OmniboxViewViews, and only
OmniboxViewViews knows when they're destroyed. If that happens,
ask Textfield to close any running context menu and also
reset the root menu model, since it holds references to the now-
destroyed submenu models.

(cherry picked from commit a3393ce39586558f74b4fd57495bfdd66a6b564b)

Fixed: 1278613,1278180
Bug: 1278942
Change-Id: If3df10d56501f975ce408e60538cc4652f5472e6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3330922
Reviewed-by: Justin Donnelly <jdonnelly@chromium.org>
Commit-Queue: Elly Fong-Jones <ellyjones@chromium.org>
Auto-Submit: Elly Fong-Jones <ellyjones@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#952052}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3366837
Reviewed-by: Jeffrey Cohen <jeffreycohen@chromium.org>
Cr-Commit-Position: refs/branch-heads/4664@{#1366}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/bd367fdccc0f9d19989f0c02312c27c60511acd7/ui/views/controls/textfield/textfield.cc
[modify] https://crrev.com/bd367fdccc0f9d19989f0c02312c27c60511acd7/ui/views/controls/textfield/textfield.h
[modify] https://crrev.com/bd367fdccc0f9d19989f0c02312c27c60511acd7/chrome/browser/ui/views/omnibox/omnibox_view_views.cc


### gi...@appspot.gserviceaccount.com (2022-01-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a6e660f31604746d334f0b3312da1557a27554c3

commit a6e660f31604746d334f0b3312da1557a27554c3
Author: Elly Fong-Jones <ellyjones@chromium.org>
Date: Tue Jan 04 23:38:07 2022

[M97] omnibox: close menu when invalidating parts of its model

The omnibox context menu's root menu is owned by Textfield,
but some submenus are owned by OmniboxViewViews, and only
OmniboxViewViews knows when they're destroyed. If that happens,
ask Textfield to close any running context menu and also
reset the root menu model, since it holds references to the now-
destroyed submenu models.

(cherry picked from commit a3393ce39586558f74b4fd57495bfdd66a6b564b)

Fixed: 1278613,1278180
Bug: 1278942
Change-Id: If3df10d56501f975ce408e60538cc4652f5472e6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3330922
Reviewed-by: Justin Donnelly <jdonnelly@chromium.org>
Commit-Queue: Elly Fong-Jones <ellyjones@chromium.org>
Auto-Submit: Elly Fong-Jones <ellyjones@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#952052}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3366835
Reviewed-by: Jeffrey Cohen <jeffreycohen@chromium.org>
Commit-Queue: Jeffrey Cohen <jeffreycohen@chromium.org>
Cr-Commit-Position: refs/branch-heads/4692@{#1357}
Cr-Branched-From: 038cd96142d384c0d2238973f1cb277725a62eba-refs/heads/main@{#938553}

[modify] https://crrev.com/a6e660f31604746d334f0b3312da1557a27554c3/ui/views/controls/textfield/textfield.cc
[modify] https://crrev.com/a6e660f31604746d334f0b3312da1557a27554c3/chrome/browser/ui/views/omnibox/omnibox_view_views.cc
[modify] https://crrev.com/a6e660f31604746d334f0b3312da1557a27554c3/ui/views/controls/textfield/textfield.h


### am...@chromium.org (2022-01-12)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-13)

Congratulations! The VRP Panel has decided to award you $10,000 for this report. Thank you for your report and nice work! 

### am...@google.com (2022-01-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-19)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1278180?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1278613, crbug.com/chromium/1281836]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058166)*
