# Security: Heap-use-after-free in payments::PaymentRequestSheetController::UpdateHeaderView

| Field | Value |
|-------|-------|
| **Issue ID** | [40095970](https://issues.chromium.org/issues/40095970) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Unknown |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2019-08-13 |
| **Bounty** | $5,000.00 |

## Description

Chrome version : 78.0.3880.4 (Official Build) canary (64-bit)
OS : Windows 

This is same bug as https://crbug.com/chromium/992285, but the stack trace is different. 

1. Load repro.html
2. Click somewhere
2. Click on "pay" and wait


000007fe`e1b032c2 ff5050          call    qword ptr [rax+50h] ds:00000000`18060970=feeefeeefeeefeee
0:000> k
Child-SP          RetAddr           Call Site
00000000`008acaa0 000007fe`e427aee2 chrome_7fee1930000!views::View::UpdateTooltip+0x8 [c:\b\s\w\ir\cache\builder\src\ui\views\view.cc @ 2850]
00000000`008acad0 000007fe`e427c7be chrome_7fee1930000!payments::PaymentRequestSheetController::UpdateHeaderView+0x26 [c:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\payments\payment_request_sheet_controller.cc @ 298]
00000000`008acb40 000007fe`e1d27685 chrome_7fee1930000!payments::PaymentHandlerWebFlowViewController::DidFinishNavigation+0xf8 [c:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\payments\payment_handler_web_flow_view_controller.cc @ 343]
00000000`008acbb0 000007fe`e1d27443 chrome_7fee1930000!content::WebContentsImpl::DidFinishNavigation+0xdf [c:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.cc @ 4373]
00000000`008accc0 000007fe`e1d273e2 chrome_7fee1930000!content::NavigationHandleImpl::~NavigationHandleImpl+0x4b [c:\b\s\w\ir\cache\builder\src\content\browser\frame_host\navigation_handle_impl.cc @ 62]
00000000`008acd80 000007fe`e1d26f5f chrome_7fee1930000!content::NavigationHandleImpl::~NavigationHandleImpl+0x10 [c:\b\s\w\ir\cache\builder\src\content\browser\frame_host\navigation_handle_impl.cc @ 58]
00000000`008acdc0 000007fe`e1d26ea6 chrome_7fee1930000!content::NavigationRequest::~NavigationRequest+0xa3 [c:\b\s\w\ir\cache\builder\src\content\browser\frame_host\navigation_request.cc @ 931]
00000000`008acf70 000007fe`e247ea74 chrome_7fee1930000!content::NavigationRequest::~NavigationRequest+0x10 [c:\b\s\w\ir\cache\builder\src\content\browser\frame_host\navigation_request.cc @ 913]
00000000`008acfb0 000007fe`e24a3176 chrome_7fee1930000!content::FrameTreeNode::~FrameTreeNode+0x208 [c:\b\s\w\ir\cache\builder\src\content\browser\frame_host\frame_tree_node.cc @ 172]
00000000`008ad080 000007fe`e24af88d chrome_7fee1930000!std::__1::unique_ptr<content::FrameTreeNode,std::__1::default_delete<content::FrameTreeNode> >::reset+0x18 [c:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\memory @ 2651]
00000000`008ad0b0 000007fe`e1bba60b chrome_7fee1930000!std::__1::__vector_base<std::__1::unique_ptr<content::FrameTreeNode,std::__1::default_delete<content::FrameTreeNode> >,std::__1::allocator<std::__1::unique_ptr<content::FrameTreeNode,std::__1::default_delete<content::FrameTreeNode> > > >::~__vector_base+0x29 [c:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\vector @ 463]
00000000`008ad0f0 000007fe`e26aba04 chrome_7fee1930000!content::RenderFrameHostImpl::ResetChildren+0x6d [c:\b\s\w\ir\cache\builder\src\content\browser\frame_host\render_frame_host_impl.cc @ 2211]
00000000`008ad150 000007fe`e26bdc78 chrome_7fee1930000!content::WebContentsImpl::~WebContentsImpl+0x368 [c:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.cc @ 675]
00000000`008ad250 000007fe`e1bd77e3 chrome_7fee1930000!content::WebContentsImpl::~WebContentsImpl+0x10 [c:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.cc @ 619]
00000000`008ad290 000007fe`e3de4b3a chrome_7fee1930000!views::WebView::SetWebContents+0x91 [c:\b\s\w\ir\cache\builder\src\ui\views\controls\webview\webview.cc @ 78]
00000000`008ad320 000007fe`e3de55ce chrome_7fee1930000!views::WebView::~WebView+0xb6 [c:\b\s\w\ir\cache\builder\src\ui\views\controls\webview\webview.cc @ 56]
00000000`008ad370 000007fe`e1b11779 chrome_7fee1930000!views::WebView::~WebView+0x10 [c:\b\s\w\ir\cache\builder\src\ui\views\controls\webview\webview.cc @ 54]
00000000`008ad3b0 000007fe`e2a7320a chrome_7fee1930000!views::View::~View+0xff [c:\b\s\w\ir\cache\builder\src\ui\views\view.cc @ 134]
00000000`008ad480 000007fe`e1b11779 chrome_7fee1930000!views::View::~View+0x10 [c:\b\s\w\ir\cache\builder\src\ui\views\view.cc @ 128]
00000000`008ad4c0 000007fe`e2a7320a chrome_7fee1930000!views::View::~View+0xff [c:\b\s\w\ir\cache\builder\src\ui\views\view.cc @ 134]



## Attachments

- [screen.mp4](attachments/screen.mp4) (video/mp4, 301.1 KB)
- [repro.html](attachments/repro.html) (text/plain, 295 B)
- [poc.html](attachments/poc.html) (text/plain, 1.1 KB)
- [Untitled.mov](attachments/Untitled.mov) (video/quicktime, 1.6 MB)
- [poc.html](attachments/poc_53395092.html) (text/plain, 1.2 KB)
- [M77.mov](attachments/M77.mov) (video/quicktime, 7.6 MB)

## Timeline

### mm...@chromium.org (2019-08-13)

Reproduced locally with https://storage.googleapis.com/chromium-browser-asan/linux-release/asan-linux-release-686546.zip

mmoroz@mmoroz3:~/Downloads/asan-linux-release-686546$ ./chrome --user-data-dir=./profile ../993223/repro.html 

(chrome:208173): dbind-WARNING **: 14:20:36.382: Couldn't register with accessibility bus: Did not receive a reply. Possible causes include: the remote application did not send a reply, the message bus security policy blocked the reply, the reply timeout expired, or the network connection was broken.
=================================================================
==208173==ERROR: AddressSanitizer: heap-use-after-free on address 0x6160005401a0 at pc 0x55e6d84e9deb bp 0x7ffdc6d33fb0 sp 0x7ffdc6d33fa8
READ of size 8 at 0x6160005401a0 thread T0 (chrome)
    #0 0x55e6d84e9dea in empty buildtools/third_party/libc++/trunk/include/vector:662:23
    #1 0x55e6d84e9dea in views::View::RemoveAllChildViews(bool) ui/views/view.cc:202
    #2 0x55e6db417916 in payments::PaymentRequestSheetController::UpdateHeaderView() chrome/browser/ui/views/payments/payment_request_sheet_controller.cc:297:17
    #3 0x55e6db40b352 in payments::PaymentHandlerWebFlowViewController::DidFinishNavigation(content::NavigationHandle*) chrome/browser/ui/views/payments/payment_handler_web_flow_view_controller.cc:342:3
    #4 0x55e6ccba33aa in content::WebContentsImpl::DidFinishNavigation(content::NavigationHandle*) content/browser/web_contents/web_contents_impl.cc:4374:14
    #5 0x55e6cc04f955 in content::NavigationHandleImpl::~NavigationHandleImpl() content/browser/frame_host/navigation_handle_impl.cc:60:18
    #6 0x55e6cc04ffed in content::NavigationHandleImpl::~NavigationHandleImpl() content/browser/frame_host/navigation_handle_impl.cc:58:47
    #7 0x55e6cc05c03f in operator() buildtools/third_party/libc++/trunk/include/memory:2338:5
    #8 0x55e6cc05c03f in reset buildtools/third_party/libc++/trunk/include/memory:2651
    #9 0x55e6cc05c03f in content::NavigationRequest::~NavigationRequest() content/browser/frame_host/navigation_request.cc:924
    #10 0x55e6cc05d22d in content::NavigationRequest::~NavigationRequest() content/browser/frame_host/navigation_request.cc:907:41
    #11 0x55e6cbfefa66 in operator() buildtools/third_party/libc++/trunk/include/memory:2338:5
    #12 0x55e6cbfefa66 in reset buildtools/third_party/libc++/trunk/include/memory:2651
    #13 0x55e6cbfefa66 in content::FrameTreeNode::~FrameTreeNode() content/browser/frame_host/frame_tree_node.cc:172
    #14 0x55e6cc09bd91 in operator() buildtools/third_party/libc++/trunk/include/memory:2338:5
    #15 0x55e6cc09bd91 in reset buildtools/third_party/libc++/trunk/include/memory:2651
    #16 0x55e6cc09bd91 in ~unique_ptr buildtools/third_party/libc++/trunk/include/memory:2605
    #17 0x55e6cc09bd91 in destroy buildtools/third_party/libc++/trunk/include/memory:1880
    #18 0x55e6cc09bd91 in __destroy<std::__1::unique_ptr<content::FrameTreeNode, std::__1::default_delete<content::FrameTreeNode> > > buildtools/third_party/libc++/trunk/include/memory:1742
    #19 0x55e6cc09bd91 in destroy<std::__1::unique_ptr<content::FrameTreeNode, std::__1::default_delete<content::FrameTreeNode> > > buildtools/third_party/libc++/trunk/include/memory:1595
    #20 0x55e6cc09bd91 in __destruct_at_end buildtools/third_party/libc++/trunk/include/vector:426
    #21 0x55e6cc09bd91 in clear buildtools/third_party/libc++/trunk/include/vector:369
    #22 0x55e6cc09bd91 in ~__vector_base buildtools/third_party/libc++/trunk/include/vector:463
    #23 0x55e6cc09bd91 in ~vector buildtools/third_party/libc++/trunk/include/vector:555
    #24 0x55e6cc09bd91 in content::RenderFrameHostImpl::ResetChildren() content/browser/frame_host/render_frame_host_impl.cc:2214
    #25 0x55e6ccb564e9 in content::WebContentsImpl::~WebContentsImpl() content/browser/web_contents/web_contents_impl.cc:675:19
    #26 0x55e6ccb5ab8d in content::WebContentsImpl::~WebContentsImpl() content/browser/web_contents/web_contents_impl.cc:619:37
    #27 0x55e6db806cdd in operator() buildtools/third_party/libc++/trunk/include/memory:2338:5
    #28 0x55e6db806cdd in reset buildtools/third_party/libc++/trunk/include/memory:2651
    #29 0x55e6db806cdd in views::WebView::SetWebContents(content::WebContents*) ui/views/controls/webview/webview.cc:77
    #30 0x55e6db8084a5 in ~WebView ui/views/controls/webview/webview.cc:55:3
    #31 0x55e6db8084a5 in views::WebView::~WebView() ui/views/controls/webview/webview.cc:54
    #32 0x55e6d84e6391 in views::View::~View() ui/views/view.cc:137:9
    #33 0x55e6d84e7b0d in views::View::~View() ui/views/view.cc:128:15
    #34 0x55e6d84e6391 in views::View::~View() ui/views/view.cc:137:9
    #35 0x55e6d84e7b0d in views::View::~View() ui/views/view.cc:128:15
    #36 0x55e6d84e6391 in views::View::~View() ui/views/view.cc:137:9
    #37 0x55e6dac7b03d in views::ScrollView::Viewport::~Viewport() ui/views/controls/scroll_view.cc:113:32
    #38 0x55e6d84e6391 in views::View::~View() ui/views/view.cc:137:9
    #39 0x55e6dac728fd in views::ScrollView::~ScrollView() ui/views/controls/scroll_view.cc:214:27
    #40 0x55e6d84e6391 in views::View::~View() ui/views/view.cc:137:9
    #41 0x55e6db418c9d in ~SheetView chrome/browser/ui/views/payments/payment_request_sheet_controller.cc:46:7
    #42 0x55e6db418c9d in payments::(anonymous namespace)::SheetView::~SheetView() chrome/browser/ui/views/payments/payment_request_sheet_controller.cc:46
    #43 0x55e6db45828c in operator() buildtools/third_party/libc++/trunk/include/memory:2338:5
    #44 0x55e6db45828c in reset buildtools/third_party/libc++/trunk/include/memory:2651
    #45 0x55e6db45828c in ~unique_ptr buildtools/third_party/libc++/trunk/include/memory:2605
    #46 0x55e6db45828c in destroy buildtools/third_party/libc++/trunk/include/memory:1880
    #47 0x55e6db45828c in __destroy<std::__1::unique_ptr<views::View, std::__1::default_delete<views::View> > > buildtools/third_party/libc++/trunk/include/memory:1742
    #48 0x55e6db45828c in destroy<std::__1::unique_ptr<views::View, std::__1::default_delete<views::View> > > buildtools/third_party/libc++/trunk/include/memory:1595
    #49 0x55e6db45828c in __destruct_at_end buildtools/third_party/libc++/trunk/include/vector:426
    #50 0x55e6db45828c in clear buildtools/third_party/libc++/trunk/include/vector:369
    #51 0x55e6db45828c in ~__vector_base buildtools/third_party/libc++/trunk/include/vector:463
    #52 0x55e6db45828c in ~vector buildtools/third_party/libc++/trunk/include/vector:555
    #53 0x55e6db45828c in ViewStack::~ViewStack() chrome/browser/ui/views/payments/view_stack.cc:30
    #54 0x55e6db45849d in ViewStack::~ViewStack() chrome/browser/ui/views/payments/view_stack.cc:30:25
    #55 0x55e6db3d70db in operator() buildtools/third_party/libc++/trunk/include/memory:2338:5
    #56 0x55e6db3d70db in reset buildtools/third_party/libc++/trunk/include/memory:2651
    #57 0x55e6db3d70db in payments::PaymentRequestDialogView::Cancel() chrome/browser/ui/views/payments/payment_request_dialog_view.cc:121
    #58 0x55e6d8551c00 in views::DialogClientView::CanClose() ui/views/window/dialog_client_view.cc:120:52
    #59 0x55e6d853419c in views::Widget::CloseWithReason(views::Widget::ClosedReason) ui/views/widget/widget.cc:587:46
    #60 0x55e6d94a5569 in web_modal::WebContentsModalDialogManager::CloseAllDialogs() components/web_modal/web_contents_modal_dialog_manager.cc:124:37
    #61 0x55e6dabeda9d in Browser::OnTabClosing(content::WebContents*) chrome/browser/ui/browser.cc:2100:61
    #62 0x55e6dabecd14 in Browser::OnTabStripModelChanged(TabStripModel*, TabStripModelChange const&, TabStripSelectionChange const&) chrome/browser/ui/browser.cc:1042:11
    #63 0x55e6dad09c73 in TabStripModel::SendDetachWebContentsNotifications(TabStripModel::DetachNotifications*) chrome/browser/ui/tabs/tab_strip_model.cc:528:16
    #64 0x55e6dad23444 in TabStripModel::CloseWebContentses(base::span<content::WebContents* const, 18446744073709551615ul>, unsigned int) chrome/browser/ui/tabs/tab_strip_model.cc:1670:5
    #65 0x55e6dad11948 in TabStripModel::InternalCloseTabs(base::span<content::WebContents* const, 18446744073709551615ul>, unsigned int) chrome/browser/ui/tabs/tab_strip_model.cc:1584:27
    #66 0x55e6dad123d5 in TabStripModel::CloseWebContentsAt(int, unsigned int) chrome/browser/ui/tabs/tab_strip_model.cc:714:10
    #67 0x55e6cc7aa3ff in OnClose content/browser/renderer_host/render_widget_host_impl.cc:2183:22
    #68 0x55e6cc7aa3ff in DispatchToMethodImpl<content::RenderWidgetHostImpl *, void (content::RenderWidgetHostImpl::*)(), std::__1::tuple<>> base/tuple.h:52
    #69 0x55e6cc7aa3ff in DispatchToMethod<content::RenderWidgetHostImpl *, void (content::RenderWidgetHostImpl::*)(), std::__1::tuple<> > base/tuple.h:60
    #70 0x55e6cc7aa3ff in DispatchToMethod<content::RenderWidgetHostImpl, void (content::RenderWidgetHostImpl::*)(), void, std::__1::tuple<> > ipc/ipc_message_templates.h:51
    #71 0x55e6cc7aa3ff in Dispatch<content::RenderWidgetHostImpl, content::RenderWidgetHostImpl, void, void (content::RenderWidgetHostImpl::*)()> ipc/ipc_message_templates.h:146
    #72 0x55e6cc7aa3ff in content::RenderWidgetHostImpl::OnMessageReceived(IPC::Message const&) content/browser/renderer_host/render_widget_host_impl.cc:624
    #73 0x55e6cc74e9d0 in content::RenderProcessHostImpl::OnMessageReceived(IPC::Message const&) content/browser/renderer_host/render_process_host_impl.cc:3266:20
    #74 0x55e6d4b05b1d in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ipc/ipc_channel_proxy.cc:323:14
    #75 0x55e6d2764d52 in Run base/callback.h:98:12
    #76 0x55e6d2764d52 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:142
    #77 0x55e6d27a0146 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*, bool*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:365:23
    #78 0x55e6d279f6d7 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:219:7
    #79 0x55e6d26ab0e9 in HandleDispatch base/message_loop/message_pump_glib.cc:392:46
    #80 0x55e6d26ab0e9 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:108
    #81 0x7fcd98607d86 in g_main_context_dispatch (/usr/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x4dd86)

0x6160005401a0 is located 288 bytes inside of 632-byte region [0x616000540080,0x6160005402f8)
freed by thread T0 (chrome) here:
    #0 0x55e6c8bbabbd in operator delete(void*) /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cc:160:3
    #1 0x55e6d84e6391 in views::View::~View() ui/views/view.cc:137:9
    #2 0x55e6db418c9d in ~SheetView chrome/browser/ui/views/payments/payment_request_sheet_controller.cc:46:7
    #3 0x55e6db418c9d in payments::(anonymous namespace)::SheetView::~SheetView() chrome/browser/ui/views/payments/payment_request_sheet_controller.cc:46
    #4 0x55e6db45828c in operator() buildtools/third_party/libc++/trunk/include/memory:2338:5
    #5 0x55e6db45828c in reset buildtools/third_party/libc++/trunk/include/memory:2651
    #6 0x55e6db45828c in ~unique_ptr buildtools/third_party/libc++/trunk/include/memory:2605
    #7 0x55e6db45828c in destroy buildtools/third_party/libc++/trunk/include/memory:1880
    #8 0x55e6db45828c in __destroy<std::__1::unique_ptr<views::View, std::__1::default_delete<views::View> > > buildtools/third_party/libc++/trunk/include/memory:1742
    #9 0x55e6db45828c in destroy<std::__1::unique_ptr<views::View, std::__1::default_delete<views::View> > > buildtools/third_party/libc++/trunk/include/memory:1595
    #10 0x55e6db45828c in __destruct_at_end buildtools/third_party/libc++/trunk/include/vector:426
    #11 0x55e6db45828c in clear buildtools/third_party/libc++/trunk/include/vector:369
    #12 0x55e6db45828c in ~__vector_base buildtools/third_party/libc++/trunk/include/vector:463
    #13 0x55e6db45828c in ~vector buildtools/third_party/libc++/trunk/include/vector:555
    #14 0x55e6db45828c in ViewStack::~ViewStack() chrome/browser/ui/views/payments/view_stack.cc:30
    #15 0x55e6db45849d in ViewStack::~ViewStack() chrome/browser/ui/views/payments/view_stack.cc:30:25
    #16 0x55e6db3d70db in operator() buildtools/third_party/libc++/trunk/include/memory:2338:5
    #17 0x55e6db3d70db in reset buildtools/third_party/libc++/trunk/include/memory:2651
    #18 0x55e6db3d70db in payments::PaymentRequestDialogView::Cancel() chrome/browser/ui/views/payments/payment_request_dialog_view.cc:121
    #19 0x55e6d8551c00 in views::DialogClientView::CanClose() ui/views/window/dialog_client_view.cc:120:52
    #20 0x55e6d853419c in views::Widget::CloseWithReason(views::Widget::ClosedReason) ui/views/widget/widget.cc:587:46
    #21 0x55e6d94a5569 in web_modal::WebContentsModalDialogManager::CloseAllDialogs() components/web_modal/web_contents_modal_dialog_manager.cc:124:37
    #22 0x55e6dabeda9d in Browser::OnTabClosing(content::WebContents*) chrome/browser/ui/browser.cc:2100:61
    #23 0x55e6dabecd14 in Browser::OnTabStripModelChanged(TabStripModel*, TabStripModelChange const&, TabStripSelectionChange const&) chrome/browser/ui/browser.cc:1042:11
    #24 0x55e6dad09c73 in TabStripModel::SendDetachWebContentsNotifications(TabStripModel::DetachNotifications*) chrome/browser/ui/tabs/tab_strip_model.cc:528:16
    #25 0x55e6dad23444 in TabStripModel::CloseWebContentses(base::span<content::WebContents* const, 18446744073709551615ul>, unsigned int) chrome/browser/ui/tabs/tab_strip_model.cc:1670:5
    #26 0x55e6dad11948 in TabStripModel::InternalCloseTabs(base::span<content::WebContents* const, 18446744073709551615ul>, unsigned int) chrome/browser/ui/tabs/tab_strip_model.cc:1584:27
    #27 0x55e6dad123d5 in TabStripModel::CloseWebContentsAt(int, unsigned int) chrome/browser/ui/tabs/tab_strip_model.cc:714:10
    #28 0x55e6cc7aa3ff in OnClose content/browser/renderer_host/render_widget_host_impl.cc:2183:22
    #29 0x55e6cc7aa3ff in DispatchToMethodImpl<content::RenderWidgetHostImpl *, void (content::RenderWidgetHostImpl::*)(), std::__1::tuple<>> base/tuple.h:52
    #30 0x55e6cc7aa3ff in DispatchToMethod<content::RenderWidgetHostImpl *, void (content::RenderWidgetHostImpl::*)(), std::__1::tuple<> > base/tuple.h:60
    #31 0x55e6cc7aa3ff in DispatchToMethod<content::RenderWidgetHostImpl, void (content::RenderWidgetHostImpl::*)(), void, std::__1::tuple<> > ipc/ipc_message_templates.h:51
    #32 0x55e6cc7aa3ff in Dispatch<content::RenderWidgetHostImpl, content::RenderWidgetHostImpl, void, void (content::RenderWidgetHostImpl::*)()> ipc/ipc_message_templates.h:146
    #33 0x55e6cc7aa3ff in content::RenderWidgetHostImpl::OnMessageReceived(IPC::Message const&) content/browser/renderer_host/render_widget_host_impl.cc:624
    #34 0x55e6cc74e9d0 in content::RenderProcessHostImpl::OnMessageReceived(IPC::Message const&) content/browser/renderer_host/render_process_host_impl.cc:3266:20
    #35 0x55e6d4b05b1d in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ipc/ipc_channel_proxy.cc:323:14
    #36 0x55e6d2764d52 in Run base/callback.h:98:12
    #37 0x55e6d2764d52 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:142
    #38 0x55e6d27a0146 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*, bool*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:365:23
    #39 0x55e6d279f6d7 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:219:7
    #40 0x55e6d26ab0e9 in HandleDispatch base/message_loop/message_pump_glib.cc:392:46
    #41 0x55e6d26ab0e9 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:108
    #42 0x7fcd98607d86 in g_main_context_dispatch (/usr/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x4dd86)

previously allocated by thread T0 (chrome) here:
    #0 0x55e6c8bba35d in operator new(unsigned long) /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cc:99:3
    #1 0x55e6db415143 in make_unique<views::View> buildtools/third_party/libc++/trunk/include/memory:3131:28
    #2 0x55e6db415143 in payments::PaymentRequestSheetController::CreateView() chrome/browser/ui/views/payments/payment_request_sheet_controller.cc:236
    #3 0x55e6db3d819d in CreateViewAndInstallController chrome/browser/ui/views/payments/payment_request_dialog_view.cc:51:51
    #4 0x55e6db3d819d in payments::PaymentRequestDialogView::ShowPaymentHandlerScreen(GURL const&, base::OnceCallback<void (bool, int, int)>) chrome/browser/ui/views/payments/payment_request_dialog_view.cc:181
    #5 0x55e6d234a2e3 in payments::ChromePaymentRequestDelegate::EmbedPaymentHandlerWindow(GURL const&, base::OnceCallback<void (bool, int, int)>) chrome/browser/payments/chrome_payment_request_delegate.cc:182:20
    #6 0x55e6dbcbb9a9 in DisplayPaymentHandlerWindow components/payments/content/payment_request_display_manager.cc:41:14
    #7 0x55e6dbcbb9a9 in payments::PaymentRequestDisplayManager::ShowPaymentHandlerWindow(GURL const&, base::OnceCallback<void (bool, int, int)>) components/payments/content/payment_request_display_manager.cc:64
    #8 0x55e6d197aa6f in ChromeContentBrowserClient::ShowPaymentHandlerWindow(content::BrowserContext*, GURL const&, base::OnceCallback<void (bool, int, int)>) chrome/browser/chrome_content_browser_client.cc:5116:9
    #9 0x55e6cc8b4c20 in content::(anonymous namespace)::ShowPaymentHandlerWindowOnUI(scoped_refptr<content::ServiceWorkerContextWrapper>, GURL const&, base::OnceCallback<void (base::OnceCallback<void (bool, mojo::StructPtr<blink::mojom::ServiceWorkerClientInfo>, base::Optional<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > > const&)>, bool, int, int)>, base::OnceCallback<void (base::OnceCallback<void (bool, mojo::StructPtr<blink::mojom::ServiceWorkerClientInfo>, base::Optional<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > > const&)>)>, base::OnceCallback<void (bool, mojo::StructPtr<blink::mojom::ServiceWorkerClientInfo>, base::Optional<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > > const&)>) content/browser/service_worker/payment_handler_support.cc:83:34
    #10 0x55e6cc8b5c11 in Invoke<void (*)(scoped_refptr<content::ServiceWorkerContextWrapper>, const GURL &, base::OnceCallback<void (base::OnceCallback<void (bool, mojo::StructPtr<blink::mojom::ServiceWorkerClientInfo>, const base::Optional<std::__1::basic_string<char> > &)>, bool, int, int)>, base::OnceCallback<void (base::OnceCallback<void (bool, mojo::StructPtr<blink::mojom::ServiceWorkerClientInfo>, const base::Optional<std::__1::basic_string<char> > &)>)>, base::OnceCallback<void (bool, mojo::StructPtr<blink::mojom::ServiceWorkerClientInfo>, const base::Optional<std::__1::basic_string<char> > &)>), scoped_refptr<content::ServiceWorkerContextWrapper>, GURL, base::OnceCallback<void (base::OnceCallback<void (bool, mojo::StructPtr<blink::mojom::ServiceWorkerClientInfo>, const base::Optional<std::__1::basic_string<char> > &)>, bool, int, int)>, base::OnceCallback<void (base::OnceCallback<void (bool, mojo::StructPtr<blink::mojom::ServiceWorkerClientInfo>, const base::Optional<std::__1::basic_string<char> > &)>)>, base::OnceCallback<void (bool, mojo::StructPtr<blink::mojom::ServiceWorkerClientInfo>, const base::Optional<std::__1::basic_string<char> > &)> > base/bind_internal.h:399:12
    #11 0x55e6cc8b5c11 in MakeItSo<void (*)(scoped_refptr<content::ServiceWorkerContextWrapper>, const GURL &, base::OnceCallback<void (base::OnceCallback<void (bool, mojo::StructPtr<blink::mojom::ServiceWorkerClientInfo>, const base::Optional<std::__1::basic_string<char> > &)>, bool, int, int)>, base::OnceCallback<void (base::OnceCallback<void (bool, mojo::StructPtr<blink::mojom::ServiceWorkerClientInfo>, const base::Optional<std::__1::basic_string<char> > &)>)>, base::OnceCallback<void (bool, mojo::StructPtr<blink::mojom::ServiceWorkerClientInfo>, const base::Optional<std::__1::basic_string<char> > &)>), scoped_refptr<content::ServiceWorkerContextWrapper>, GURL, base::OnceCallback<void (base::OnceCallback<void (bool, mojo::StructPtr<blink::mojom::ServiceWorkerClientInfo>, const base::Optional<std::__1::basic_string<char> > &)>, bool, int, int)>, base::OnceCallback<void (base::OnceCallback<void (bool, mojo::StructPtr<blink::mojom::ServiceWorkerClientInfo>, const base::Optional<std::__1::basic_string<char> > &)>)>, base::OnceCallback<void (bool, mojo::StructPtr<blink::mojom::ServiceWorkerClientInfo>, const base::Optional<std::__1::basic_string<char> > &)> > base/bind_internal.h:599
    #12 0x55e6cc8b5c11 in RunImpl<void (*)(scoped_refptr<content::ServiceWorkerContextWrapper>, const GURL &, base::OnceCallback<void (base::OnceCallback<void (bool, mojo::StructPtr<blink::mojom::ServiceWorkerClientInfo>, const base::Optional<std::__1::basic_string<char> > &)>, bool, int, int)>, base::OnceCallback<void (base::OnceCallback<void (bool, mojo::StructPtr<blink::mojom::ServiceWorkerClientInfo>, const base::Optional<std::__1::basic_string<char> > &)>)>, base::OnceCallback<void (bool, mojo::StructPtr<blink::mojom::ServiceWorkerClientInfo>, const base::Optional<std::__1::basic_string<char> > &)>), std::__1::tuple<scoped_refptr<content::ServiceWorkerContextWrapper>, GURL, base::OnceCallback<void (base::OnceCallback<void (bool, mojo::StructPtr<blink::mojom::ServiceWorkerClientInfo>, const base::Optional<std::__1::basic_string<char> > &)>, bool, int, int)>, base::OnceCallback<void (base::OnceCallback<void (bool, mojo::StructPtr<blink::mojom::ServiceWorkerClientInfo>, const base::Optional<std::__1::basic_string<char> > &)>)>, base::OnceCallback<void (bool, mojo::StructPtr<blink::mojom::ServiceWorkerClientInfo>, const base::Optional<std::__1::basic_string<char> > &)> >, 0, 1, 2, 3, 4> base/bind_internal.h:672
    #13 0x55e6cc8b5c11 in base::internal::Invoker<base::internal::BindState<void (*)(scoped_refptr<content::ServiceWorkerContextWrapper>, GURL const&, base::OnceCallback<void (base::OnceCallback<void (bool, mojo::StructPtr<blink::mojom::ServiceWorkerClientInfo>, base::Optional<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > > const&)>, bool, int, int)>, base::OnceCallback<void (base::OnceCallback<void (bool, mojo::StructPtr<blink::mojom::ServiceWorkerClientInfo>, base::Optional<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > > const&)>)>, base::OnceCallback<void (bool, mojo::StructPtr<blink::mojom::ServiceWorkerClientInfo>, base::Optional<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > > const&)>), scoped_refptr<content::ServiceWorkerContextWrapper>, GURL, base::OnceCallback<void (base::OnceCallback<void (bool, mojo::StructPtr<blink::mojom::ServiceWorkerClientInfo>, base::Optional<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > > const&)>, bool, int, int)>, base::OnceCallback<void (base::OnceCallback<void (bool, mojo::StructPtr<blink::mojom::ServiceWorkerClientInfo>, base::Optional<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > > const&)>)>, base::OnceCallback<void (bool, mojo::StructPtr<blink::mojom::ServiceWorkerClientInfo>, base::Optional<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > > const&)> >, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:641
    #14 0x55e6d2764d52 in Run base/callback.h:98:12
    #15 0x55e6d2764d52 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:142
    #16 0x55e6d27a0146 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*, bool*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:365:23
    #17 0x55e6d279f6d7 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:219:7
    #18 0x55e6d26ab0e9 in HandleDispatch base/message_loop/message_pump_glib.cc:392:46
    #19 0x55e6d26ab0e9 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:108
    #20 0x7fcd98607d86 in g_main_context_dispatch (/usr/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x4dd86)

SUMMARY: AddressSanitizer: heap-use-after-free buildtools/third_party/libc++/trunk/include/vector:662:23 in empty
Shadow bytes around the buggy address:
  0x0c2c8009ffe0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2c8009fff0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2c800a0000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2c800a0010: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2c800a0020: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x0c2c800a0030: fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd
  0x0c2c800a0040: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2c800a0050: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa
  0x0c2c800a0060: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2c800a0070: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2c800a0080: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
  Shadow gap:              cc
==208173==ABORTING




[Monorail components: UI>Browser>Payments]

### mm...@chromium.org (2019-08-13)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-08-13)

Actually, copying M related labels from https://crbug.com/chromium/992285.

### mm...@chromium.org (2019-08-13)

Also, I'm leaning towards High severity (not Critical), as this requires a user interaction which is not a very obvious one as an attacker would need to convince the victim to click Pay. However, given the simplicity of the interaction on the other hand, I'm leaving Critical severity here just to be extra cautious.

### ro...@chromium.org (2019-08-13)

Does not repro on M-76 stable, so it's a regression and release-block-stable, right?

### ro...@chromium.org (2019-08-13)

Ah yes, it says 'the same bug' in the description.

### ro...@chromium.org (2019-08-13)

Confirmed fixed in ToT with https://crrev.com/1f3d381e1f42a45e48aa649ee942741828a40a0d

Still waiting for the merge approval into M-77 on  https://crbug.com/chromium/992285.

### ro...@chromium.org (2019-08-13)

Going to mark this fixed, but not a duplicate of https://crbug.com/chromium/992285.

### bu...@chromium.org (2019-08-13)

[Auto-generated comment by a script] We noticed that this issue is targeted for M-77; it appears the fix may have landed after branch point, meaning a merge might be required. The owner of this bug should confirm if a merge is required here. If so, add Merge-Request-77 label and indicate which commits/CLs are to be merged. Otherwise, remove Merge-TBD label. Thanks.

### ro...@chromium.org (2019-08-13)

Merge will be performed in https://crbug.com/chromium/992285.

### ro...@chromium.org (2019-08-13)

The fix (https://crrev.com/1f3d381e1f42a45e48aa649ee942741828a40a0d) is now merged into M-77 branch as well (https://crrev.com/ce0f4a101d78085707e8c9561ee793c912b1f20e).

### ch...@gmail.com (2019-08-13)

@rouslan, Thanks for the update! - Should this be fixed on the latest version of Chromium 78.0.3882.0 refs/heads/master@{#686535}? 

### ch...@gmail.com (2019-08-14)

I'm still able to repro this easily without "click Pay" on the latest version of Chromium (78.0.3882.0 refs/heads/master@{#686609}) even the fix in https://crbug.com/chromium/992285 https://crrev.com/1f3d381e1f42a45e48aa649ee942741828a40a0d has landed on refs/heads/master@{#685758} 

### ch...@gmail.com (2019-08-14)

Reproduced on M77 branch 3865 as well.

### ro...@google.com (2019-08-14)

Thank you for the follow up. I'm also able to reproduce on Canary 78.0.3882.0. Could it be due to the following patch?

https://chromium.googlesource.com/chromium/src.git/+/6f23eb2615bb59b3cfcfc2437c5803a4e07e4cfd

Investigating now.


### ro...@google.com (2019-08-14)

Hm, I'm no longer able to reproduce on Canary:

Google Chrome: 78.0.3882.0 (Official Build) canary (64-bit)
Revision: 5ff46e6737b9c1c08fcf035108b349b5b7c6de43-refs/branch-heads/3882@{#1}
OS: macOS Version 10.14.6 (Build 18G87)

The merge into M-77 has not been released in an official build yet, so let's give it some time.

Do you have access to the website that lists out where the patches have been released?

Fix on trunk: https://chromiumdash.appspot.com/commit/1f3d381e1f42a45e48aa649ee942741828a40a0d
Fix in M-77: https://chromiumdash.appspot.com/commit/ce0f4a101d78085707e8c9561ee793c912b1f20e

Related follow up work on trunk: https://chromiumdash.appspot.com/commit/6f23eb2615bb59b3cfcfc2437c5803a4e07e4cfd

### ro...@chromium.org (2019-08-14)

The poc.html reproduces for me on ToT when the service worker is not installed. Looking into this.

### ro...@chromium.org (2019-08-14)

Stack trace:

Received signal 11 SEGV_MAPERR ffffca99ff11058c
#0 0x5618725dafc9 base::debug::CollectStackTrace()
#1 0x5618724f01c3 base::debug::StackTrace::StackTrace()
#2 0x5618725daab1 base::debug::(anonymous namespace)::StackDumpSignalHandler()
#3 0x7fe3e706a3a0 <unknown>
#4 0x56187451f49b views::View::RemoveAllChildViews()
#5 0x56187536c132 payments::PaymentRequestSheetController::UpdateHeaderView()
#6 0x56187536310f payments::PaymentHandlerWebFlowViewController::DidFinishNavigation()
#7 0x561870170e0c content::WebContentsImpl::DidFinishNavigation()
#8 0x56186fd61719 content::NavigationHandleImpl::~NavigationHandleImpl()
#9 0x56186fd6196e content::NavigationHandleImpl::~NavigationHandleImpl()
#10 0x56186fd66953 content::NavigationRequest::~NavigationRequest()
#11 0x56186fd66f6e content::NavigationRequest::~NavigationRequest()
#12 0x56186fd447bd content::FrameTreeNode::~FrameTreeNode()
#13 0x56186fd822b2 content::RenderFrameHostImpl::ResetChildren()
#14 0x56187015ad20 content::WebContentsImpl::~WebContentsImpl()
#15 0x56187015be4e content::WebContentsImpl::~WebContentsImpl()
#16 0x5618754557ca views::WebView::SetWebContents()
#17 0x561875456227 views::WebView::~WebView()
#18 0x56187451e47b views::View::~View()
#19 0x5618744929ae views::InkDropContainerView::~InkDropContainerView()
#20 0x56187451e47b views::View::~View()
#21 0x5618744929ae views::InkDropContainerView::~InkDropContainerView()
#22 0x56187451e47b views::View::~View()
#23 0x5618744929ae views::InkDropContainerView::~InkDropContainerView()
#24 0x56187451e47b views::View::~View()
#25 0x5618744dd68e views::ScrollView::~ScrollView()
#26 0x56187451e47b views::View::~View()
#27 0x56187537a60d payments::(anonymous namespace)::SheetView::~SheetView()
#28 0x56187537c720 ViewStack::~ViewStack()
#29 0x56187537c80e ViewStack::~ViewStack()
#30 0x561875366041 payments::PaymentRequestDialogView::Cancel()
#31 0x56187453bc43 views::DialogClientView::CanClose()
#32 0x561874532b94 views::Widget::CloseWithReason()
#33 0x5618755a08e9 constrained_window::NativeWebContentsModalDialogManagerViews::Close()
#34 0x561874a41932 web_modal::WebContentsModalDialogManager::DidFinishNavigation()
#35 0x561870170e0c content::WebContentsImpl::DidFinishNavigation()
#36 0x56186fd61719 content::NavigationHandleImpl::~NavigationHandleImpl()
#37 0x56186fd6196e content::NavigationHandleImpl::~NavigationHandleImpl()
#38 0x56186fd66953 content::NavigationRequest::~NavigationRequest()
#39 0x56186fd66f6e content::NavigationRequest::~NavigationRequest()
#40 0x56186fd7bdb5 content::NavigatorImpl::DidNavigate()
#41 0x56186fd9177a content::RenderFrameHostImpl::DidCommitNavigationInternal()
#42 0x56186fd90c85 content::RenderFrameHostImpl::DidCommitNavigation()
#43 0x56186fd919f5 content::RenderFrameHostImpl::DidCommitPerNavigationMojoInterfaceNavigation()
#44 0x56186fdb14b2 base::internal::Invoker<>::RunOnce()
#45 0x56186f21b10b content::mojom::NavigationClient_CommitNavigation_ForwardToCallback::Accept()
#46 0x56187270b944 mojo::InterfaceEndpointClient::HandleValidatedMessage()
#47 0x56187270e616 mojo::FilterChain::Accept()
#48 0x56187270cf05 mojo::InterfaceEndpointClient::HandleIncomingMessage()
#49 0x5618730f780f IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnProxyThread()
#50 0x5618730f791c base::internal::Invoker<>::RunOnce()
#51 0x561872560118 base::TaskAnnotator::RunTask()
#52 0x56187257b871 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl()
#53 0x56187257b28b base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork()
#54 0x5618725170aa base::MessagePumpGlib::Run()
#55 0x56187257c6f7 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run()
#56 0x561872541536 base::RunLoop::RunWithTimeout()
#57 0x561872008cf8 ChromeBrowserMainParts::MainMessageLoopRun()
#58 0x56186fbb205b content::BrowserMainLoop::RunMainMessageLoopParts()
#59 0x56186fbb3c83 content::BrowserMainRunnerImpl::Run()
#60 0x56186fba53fc content::BrowserMain()
#61 0x561871f6d416 content::ContentMainRunnerImpl::RunServiceManager()
#62 0x561871f6cfe3 content::ContentMainRunnerImpl::Run()
#63 0x561871fc38a4 service_manager::Main()
#64 0x561871f6b1f1 content::ContentMain()
#65 0x56186eb831bf ChromeMain
#66 0x7fe3e256952b __libc_start_main
#67 0x56186eb8302a _start
  r8: 0000000000000004  r9: 0000000000000001 r10: 8080808080808080 r11: 00003564b0374005
 r12: 00007ffc7fc45838 r13: 00003564b0393480 r14: 00007ffc7fc45800 r15: 00007ffc7fc457d0
  di: 00003564b02d9500  si: 0000000000000001  bp: 00007ffc7fc45600  bx: 00003564b02d9500
  dx: 00003564b0373800  ax: ffffca99ff110524  cx: fffffffd4f3c8a24  sp: 00007ffc7fc455f0
  ip: 000056187451f49b efl: 0000000000010246 cgf: 002b000000000033 erf: 0000000000000005
 trp: 000000000000000e msk: 0000000000000000 cr2: ffffca99ff11058c
[end of stack trace]


### ch...@gmail.com (2019-08-14)

- Still able to repro this on Chromium 78.0.3883.0 (Developer Build) (64-bit) 0c5cc2a81628cb80949b330232d8ba10013c45ba-refs/heads/master@{#686772} and Canary (78.0.3882.0 heads/3882@{#1}) as well.

Sometimes looks like it can take several tries to repro the crash.

### ro...@chromium.org (2019-08-14)

chromium.khalil@ - is your stack trace the same as in https://crbug.com/chromium/993223#c18?

### ro...@chromium.org (2019-08-14)

> Sometimes looks like it can take several tries to repro the crash.

Yes, it appears intermittent. Could be timing-dependent. Debug build in particular has a harder time reproducing the crash.

### ro...@chromium.org (2019-08-14)

chromium.khalil@ - what are the GN args you're using for your developer build?

### ch...@gmail.com (2019-08-14)

>  is your stack trace the same as in https://crbug.com/chromium/993223#c18?

Yes.

> what are the GN args you're using for your developer build?

I'm using a raw build for Mac from https://download-chromium.appspot.com

Command Line	/private/var/folders/c_/ljsgs5gn0h1fkj0bw1jq6jjh0000gn/T/AppTranslocation/F44B151E-B426-4166-BA71-9D0EABE2099F/d/Chromium.app/Contents/MacOS/Chromium --flag-switches-begin --enable-experimental-web-platform-features --flag-switches-end --file-url-path-alias=/gen=/private/var/folders/c_/ljsgs5gn0h1fkj0bw1jq6jjh0000gn/T/AppTranslocation/F44B151E-B426-4166-BA71-9D0EABE2099F/d/gen

### ro...@chromium.org (2019-08-14)

These steps appear to be more reliable. Do they work for you, chromium.khalil@?

1. Open poc.html from https://crbug.com/chromium/993223#c13.
2. Click on the page and wait for it to navigate to google.com.
3. Click on the back button (<--) to navigate back to poc.html.
4. Open a new tab with chrome://serviceworker-internals.
5. Stop and unregregister the pay.google.com service worker.
6. Open the poc.html tab.
7. Click anywhere on the page.

Observed: Crash.

### ch...@gmail.com (2019-08-14)

> These steps appear to be more reliable. Do they work for you, chromium.khalil@?

Yes.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/eb2394265927839ccd3fa40d098c62ac3f3a8948

commit eb2394265927839ccd3fa40d098c62ac3f3a8948
Author: Rouslan Solomakhin <rouslan@chromium.org>
Date: Wed Aug 14 21:48:19 2019

[Web Payment] Prevent use-after-free in payment handler UI.

Bug: 993223
Change-Id: If5ae0321142cdb3d2b54957bf3d09d67e8611010
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1754523
Reviewed-by: Danyao Wang <danyao@chromium.org>
Commit-Queue: Rouslan Solomakhin <rouslan@chromium.org>
Auto-Submit: Rouslan Solomakhin <rouslan@chromium.org>
Cr-Commit-Position: refs/heads/master@{#687023}

[modify] https://crrev.com/eb2394265927839ccd3fa40d098c62ac3f3a8948/chrome/browser/ui/views/payments/payment_handler_web_flow_view_controller.cc
[modify] https://crrev.com/eb2394265927839ccd3fa40d098c62ac3f3a8948/chrome/browser/ui/views/payments/payment_request_dialog_view.cc
[modify] https://crrev.com/eb2394265927839ccd3fa40d098c62ac3f3a8948/chrome/browser/ui/views/payments/payment_request_sheet_controller.h


### ro...@chromium.org (2019-08-14)

I'd like to merge https://crrev.com/eb2394265927839ccd3fa40d098c62ac3f3a8948 into M-77 to fix the crash. I've verified the fix on ToT so far and will also verify it in the next release of the Canary channel.

### ro...@chromium.org (2019-08-14)

[Empty comment from Monorail migration]

### ch...@gmail.com (2019-08-14)

Verified on Chromium 78.0.3883.0 (Developer Build) (64-bit) heads/master@{#687023} this seems like fixed. Thanks for the fixed!

### ro...@chromium.org (2019-08-15)

Thank you for the bug report!

+CC for the merge review.

### sh...@chromium.org (2019-08-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-15)

This bug requires manual review: M77 has already been promoted to the beta branch, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), dgagnon@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ro...@chromium.org (2019-08-15)

1. Yes, it's a crash fix.
2. https://crrev.com/eb2394265927839ccd3fa40d098c62ac3f3a8948
3. Landed and verified on ToT.
4. To fix a crash.
5. No.
6. N/A.

### la...@chromium.org (2019-08-15)

merge approved for M77 branch 3865

### ro...@chromium.org (2019-08-16)

Merged into M77 in https://chromium.googlesource.com/chromium/src/+/307da68c7c1ae6a8c02c6c9b18c99fb6397cd7c8.

### na...@google.com (2019-08-19)

[Empty comment from Monorail migration]

### [Deleted User] (2019-08-20)

[Empty comment from Monorail migration]

### [Deleted User] (2019-08-20)

cc pmukherj@microsoft.com for validating it on edge (chromium)

### da...@chromium.org (2019-08-20)

[Empty comment from Monorail migration]

### na...@google.com (2019-08-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-08-21)

Congrats! The Panel decided to reward $5,000 for this report!

### na...@google.com (2019-08-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@chromium.org (2020-01-07)

rouslan@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### is...@google.com (2020-01-07)

This issue was migrated from crbug.com/chromium/993223?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095970)*
