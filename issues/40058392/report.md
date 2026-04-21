# Container-overflow in TableView::UpdateVirtualAccessibilityChildrenBounds

| Field | Value |
|-------|-------|
| **Issue ID** | [40058392](https://issues.chromium.org/issues/40058392) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>TaskManager |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | sa...@gmail.com |
| **Assignee** | af...@chromium.org |
| **Created** | 2022-01-02 |
| **Bounty** | Confirmed (amount unknown) |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36

Steps to reproduce the problem:
1. ./chrome.exe --user-data-dir=D:\log\log500 --disable-popup-blocking  http://localhost:8000/chrome/poc.html
2.  Shift + Esc
3.  Right click anywhere in task manager window. 
4.  Uncheck every column.
5.  Click the button in poc.html.

What is the expected behavior?

What went wrong?
=================================================================
==21580==ERROR: AddressSanitizer: container-overflow on address 0x120f93ac3168 at pc 0x7ff97d258691 bp 0x00d45b1fd800 sp 0x00d45b1fd848
READ of size 8 at 0x120f93ac3168 thread T0
==21580==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ff97d258690 in views::TableView::UpdateVirtualAccessibilityChildrenBounds C:\b\s\w\ir\cache\builder\src\ui\views\controls\table\table_view.cc:1652
    #1 0x7ff97d254064 in views::TableView::SortItemsAndUpdateMapping C:\b\s\w\ir\cache\builder\src\ui\views\controls\table\table_view.cc:1045
    #2 0x7ff97d25c30e in views::TableView::OnItemsAdded C:\b\s\w\ir\cache\builder\src\ui\views\controls\table\table_view.cc:804
    #3 0x7ff97669a75a in task_manager::TaskManagerInterface::NotifyObserversOnTaskAdded C:\b\s\w\ir\cache\builder\src\chrome\browser\task_manager\task_manager_interface.cc:130
    #4 0x7ff979a6a676 in task_manager::TaskManagerImpl::TaskAdded C:\b\s\w\ir\cache\builder\src\chrome\browser\task_manager\sampling\task_manager_impl.cc:512
    #5 0x7ff97dd721bf in task_manager::FallbackTaskProvider::ShowTask C:\b\s\w\ir\cache\builder\src\chrome\browser\task_manager\providers\fallback_task_provider.cc:136
    #6 0x7ff97dd725da in task_manager::FallbackTaskProvider::OnTaskAddedBySource C:\b\s\w\ir\cache\builder\src\chrome\browser\task_manager\providers\fallback_task_provider.cc:172
    #7 0x7ff97dd72dd3 in task_manager::FallbackTaskProvider::SubproviderSource::TaskAdded C:\b\s\w\ir\cache\builder\src\chrome\browser\task_manager\providers\fallback_task_provider.cc:216
    #8 0x7ff97dd6a5b7 in task_manager::WebContentsTaskProvider::WebContentsEntry::CreateTaskForFrame C:\b\s\w\ir\cache\builder\src\chrome\browser\task_manager\providers\web_contents\web_contents_task_provider.cc:357
    #9 0x7ff96dd6d50a in content::WebContentsImpl::WebContentsObserverList::NotifyObservers<void (content::WebContentsObserver::*)(content::NavigationEntry *),content::NavigationEntryImpl *&> C:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.h:1502
    #10 0x7ff96ddac21b in content::WebContentsImpl::RenderFrameCreated C:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.cc:6628
    #11 0x7ff96d94a7a3 in content::RenderFrameHostImpl::RenderFrameCreated C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_impl.cc:3156
    #12 0x7ff96d972eb5 in content::RenderFrameHostImpl::CreateNewWindow C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_impl.cc:6848
    #13 0x7ff96c11cae9 in content::mojom::FrameHostStubDispatch::AcceptWithResponder C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\content\common\frame.mojom.cc:5922
    #14 0x7ff96d9bcc9e in content::mojom::FrameHostStub<mojo::RawPtrImplRefTraits<content::mojom::FrameHost> >::AcceptWithResponder C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\content\common\frame.mojom.h:698
    #15 0x7ff974036065 in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:862
    #16 0x7ff976961e05 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:48
    #17 0x7ff9740398c8 in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:657
    #18 0x7ff9748b935a in IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptSyncMessage C:\b\s\w\ir\cache\builder\src\ipc\ipc_mojo_bootstrap.cc:1048
    #19 0x7ff973ce8624 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:135
    #20 0x7ff97681b415 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:356
    #21 0x7ff97681aae8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:261
    #22 0x7ff973d91176 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:220
    #23 0x7ff973d8f408 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78
    #24 0x7ff97681cae1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:468
    #25 0x7ff973c67193 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:140
    #26 0x7ff96ce7f1b1 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1048
    #27 0x7ff96ce845d1 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:153
    #28 0x7ff96ce78839 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:30
    #29 0x7ff96f90ab43 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:646
    #30 0x7ff96f90db83 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1160
    #31 0x7ff96f90ccb6 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1026
    #32 0x7ff96f908f8d in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:398
    #33 0x7ff96f90a018 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:426
    #34 0x7ff9691c148e in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:177
    #35 0x7ff681945b85 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:169
    #36 0x7ff681942b5f in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:382
    #37 0x7ff681d4753f in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #38 0x7ffa111b54df in BaseThreadInitThunk+0xf (C:\WINDOWS\System32\KERNEL32.DLL+0x1800154df)
    #39 0x7ffa1240485a in RtlUserThreadStart+0x2a (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18000485a)

0x120f93ac3168 is located 8 bytes inside of 64-byte region [0x120f93ac3160,0x120f93ac31a0)
allocated by thread T0 here:
    #0 0x7ff6819f24fb in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ff9864b58be in operator new d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:35
    #2 0x7ff9763eba7d in std::__1::vector<std::__1::unique_ptr<views::AXVirtualView,std::__1::default_delete<views::AXVirtualView> >,std::__1::allocator<std::__1::unique_ptr<views::AXVirtualView,std::__1::default_delete<views::AXVirtualView> > > >::insert C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\vector:1828
    #3 0x7ff9763eb6ed in views::ViewAccessibility::AddVirtualChildViewAt C:\b\s\w\ir\cache\builder\src\ui\views\accessibility\view_accessibility.cc:106
    #4 0x7ff9763eb4d0 in views::ViewAccessibility::AddVirtualChildView C:\b\s\w\ir\cache\builder\src\ui\views\accessibility\view_accessibility.cc:85
    #5 0x7ff97d25341e in views::TableView::RebuildVirtualAccessibilityChildren C:\b\s\w\ir\cache\builder\src\ui\views\controls\table\table_view.cc:1382
    #6 0x7ff979a2df1b in task_manager::TaskManagerView::Init C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\task_manager_view.cc:331
    #7 0x7ff979a2c5cc in task_manager::TaskManagerView::TaskManagerView C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\task_manager_view.cc:306
    #8 0x7ff979a2bc74 in task_manager::TaskManagerView::Show C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\task_manager_view.cc:78
    #9 0x7ff97853239d in chrome::OpenTaskManager C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser_commands.cc:1564
    #10 0x7ff978509379 in chrome::BrowserCommandController::ExecuteCommandWithDisposition C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser_command_controller.cc:706
    #11 0x7ff9798b8c4f in BrowserView::AcceleratorPressed C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_view.cc:3428
    #12 0x7ff97936be2f in ui::AcceleratorManager::Process C:\b\s\w\ir\cache\builder\src\ui\base\accelerators\accelerator_manager.cc:83
    #13 0x7ff976429d88 in views::FocusManager::ProcessAccelerator C:\b\s\w\ir\cache\builder\src\ui\views\focus\focus_manager.cc:536
    #14 0x7ff97db01f54 in views::UnhandledKeyboardEventHandler::HandleKeyboardEvent C:\b\s\w\ir\cache\builder\src\ui\views\controls\webview\unhandled_keyboard_event_handler.cc:45
    #15 0x7ff96dd77953 in content::WebContentsImpl::HandleKeyboardEvent C:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.cc:3260
    #16 0x7ff96da7311c in content::RenderWidgetHostImpl::OnKeyboardEventAck C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_widget_host_impl.cc:2501
    #17 0x7ff96d75acd5 in content::InputRouterImpl::KeyboardEventHandled C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\input\input_router_impl.cc:592
    #18 0x7ff96d762a18 in base::internal::FunctorTraits<void (content::InputRouterImpl::*)(const content::EventWithLatencyInfo<blink::WebMouseEvent> &, base::OnceCallback<void (const content::EventWithLatencyInfo<blink::WebMouseEvent> &, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState)>, blink::mojom::InputEventResultSource, const ui::LatencyInfo &, blink::mojom::InputEventResultState, mojo::StructPtr<blink::mojom::DidOverscrollParams>, mojo::InlinedStructPtr<blink::mojom::TouchActionOptional>),void>::Invoke<void (content::InputRouterImpl::*)(const content::EventWithLatencyInfo<blink::WebMouseEvent> &, base::OnceCallback<void (const content::EventWithLatencyInfo<blink::WebMouseEvent> &, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState)>, blink::mojom::InputEventResultSource, const ui::LatencyInfo &, blink::mojom::InputEventResultState, mojo::StructPtr<blink::mojom::DidOverscrollParams>, mojo::InlinedStructPtr<blink::mojom::TouchActionOptional>),base::WeakPtr<content::InputRouterImpl>,content::EventWithLatencyInfo<blink::WebMouseEvent>,base::OnceCallback<void (const content::EventWithLatencyInfo<blink::WebMouseEvent> &, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState)>,blink::mojom::InputEventResultSource,const ui::LatencyInfo &,blink::mojom::InputEventResultState,mojo::StructPtr<blink::mojom::DidOverscrollParams>,mojo::InlinedStructPtr<blink::mojom::TouchActionOptional> > C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:535
    #19 0x7ff96d76270b in base::internal::Invoker<base::internal::BindState<void (content::InputRouterImpl::*)(const content::EventWithLatencyInfo<content::NativeWebKeyboardEvent> &, base::OnceCallback<void (const content::EventWithLatencyInfo<content::NativeWebKeyboardEvent> &, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState)>, blink::mojom::InputEventResultSource, const ui::LatencyInfo &, blink::mojom::InputEventResultState, mojo::StructPtr<blink::mojom::DidOverscrollParams>, mojo::InlinedStructPtr<blink::mojom::TouchActionOptional>),base::WeakPtr<content::InputRouterImpl>,content::EventWithLatencyInfo<content::NativeWebKeyboardEvent>,base::OnceCallback<void (const content::EventWithLatencyInfo<content::NativeWebKeyboardEvent> &, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState)> >,void (blink::mojom::InputEventResultSource, const ui::LatencyInfo &, blink::mojom::InputEventResultState, mojo::StructPtr<blink::mojom::DidOverscrollParams>, mojo::InlinedStructPtr<blink::mojom::TouchActionOptional>)>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:741
    #20 0x7ff96bd75eea in base::OnceCallback<void (blink::mojom::InputEventResultSource, const ui::LatencyInfo &, blink::mojom::InputEventResultState, mojo::StructPtr<blink::mojom::DidOverscrollParams>, mojo::InlinedStructPtr<blink::mojom::TouchActionOptional>)>::Run C:\b\s\w\ir\cache\builder\src\base\callback.h:142
    #21 0x7ff96d7667c9 in base::internal::Invoker<base::internal::BindState<`lambda at ../../content/browser/renderer_host/input/input_router_impl.cc:544:13',base::OnceCallback<void (blink::mojom::InputEventResultSource, const ui::LatencyInfo &, blink::mojom::InputEventResultState, mojo::StructPtr<blink::mojom::DidOverscrollParams>, mojo::InlinedStructPtr<blink::mojom::TouchActionOptional>)>,base::WeakPtr<content::InputRouterImpl> >,void (blink::mojom::InputEventResultSource, const ui::LatencyInfo &, blink::mojom::InputEventResultState, mojo::StructPtr<blink::mojom::DidOverscrollParams>, mojo::InlinedStructPtr<blink::mojom::TouchActionOptional>)>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:741
    #22 0x7ff96bd75eea in base::OnceCallback<void (blink::mojom::InputEventResultSource, const ui::LatencyInfo &, blink::mojom::InputEventResultState, mojo::StructPtr<blink::mojom::DidOverscrollParams>, mojo::InlinedStructPtr<blink::mojom::TouchActionOptional>)>::Run C:\b\s\w\ir\cache\builder\src\base\callback.h:142
    #23 0x7ff96bd75847 in blink::mojom::WidgetInputHandler_DispatchEvent_ForwardToCallback::Accept C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\public\mojom\input\input_handler.mojom.cc:5428
    #24 0x7ff974035f31 in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:895
    #25 0x7ff976961ef2 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43
    #26 0x7ff9740398c8 in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:657
    #27 0x7ff97404d715 in mojo::internal::MultiplexRouter::ProcessIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:1104

HINT: if you don't care about these errors you may set ASAN_OPTIONS=detect_container_overflow=0.
If you suspect a false positive see also: https://github.com/google/sanitizers/wiki/AddressSanitizerContainerOverflow.
SUMMARY: AddressSanitizer: container-overflow C:\b\s\w\ir\cache\builder\src\ui\views\controls\table\table_view.cc:1652 in views::TableView::UpdateVirtualAccessibilityChildrenBounds
Shadow bytes around the buggy address:
  0x044585fd85d0: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fd
  0x044585fd85e0: fa fa fa fa fd fd fd fd fd fd fd fd fa fa fa fa
  0x044585fd85f0: fd fd fd fd fd fd fd fd fa fa fa fa fd fd fd fd
  0x044585fd8600: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fd
  0x044585fd8610: fa fa fa fa fd fd fd fd fd fd fd fd fa fa fa fa
=>0x044585fd8620: fd fd fd fd fd fd fd fd fa fa fa fa 00[fc]fc fc
  0x044585fd8630: fc fc fc fc fa fa fa fa fd fd fd fd fd fd fd fd
  0x044585fd8640: fa fa fa fa fd fd fd fd fd fd fd fd fa fa fa fa
  0x044585fd8650: fd fd fd fd fd fd fd fd fa fa fa fa fd fd fd fd
  0x044585fd8660: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fd
  0x044585fd8670: fa fa fa fa fd fd fd fd fd fd fd fd fa fa fa fa
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
==21580==ABORTING

Did this work before? N/A 

Chrome version: 96.0.4664.110  Channel: stable
OS Version: 10.0

Thanks,

Samet Bekmezci @sametbekmezci

## Attachments

- [poc.mp4](attachments/poc.mp4) (video/mp4, 2.6 MB)
- [asan.log](attachments/asan.log) (text/plain, 15.7 KB)
- [poc.html](attachments/poc.html) (text/plain, 287 B)

## Timeline

### [Deleted User] (2022-01-02)

[Empty comment from Monorail migration]

### dr...@chromium.org (2022-01-05)

I was able to reproduce this crash. Due to the unusual flag and user gestures, assigning medium severity.

I think the root cause is probably in task manager code, so afakhry@chromium.org - can you take a look?


[Monorail components: UI>TaskManager]

### [Deleted User] (2022-01-05)

[Empty comment from Monorail migration]

### af...@chromium.org (2022-01-05)

What're the contents of that page poc.html? Opening that link takes me no where.

### sa...@gmail.com (2022-01-05)

poc.html

<!DOCTYPE html>
<html lang="en">
<head>
</head>
<body>
	<button onclick="test()">click</button>

	<script>
	function test() {
    setInterval(() => {
		var win = open("blank.html")
		setTimeout(() => {
			win.close()
		}, 1000);
	}, 500);
}

	</script>
</body>
</html>

### sa...@gmail.com (2022-01-05)

[Comment Deleted]

### sa...@gmail.com (2022-01-05)

[Comment Deleted]

### sa...@gmail.com (2022-01-05)

https://crbug.com/chromium/1283807#c2 Actually, there is no need to add a flag. After the user removes the columns in the task manager, he has to "ctrl+t" twice. So I believe this report should be high severity

### [Deleted User] (2022-01-05)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-05)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### af...@chromium.org (2022-01-05)

The actual crash happens due to an out-of-bounds access into a vector in the following line: https://source.chromium.org/chromium/chromium/src/+/main:ui/views/controls/table/table_view.cc;drc=0e45c020c43b1a9f6d2870ff7f92b30a2f03a458;l=1651

    auto& ax_row = virtual_children[header_ ? row_index + 1 : row_index];

`virtual_children` in this case has only one element (the header I suppose), so row_index + 1 is out of bounds already.

../../buildtools/third_party/libc++/trunk/include/vector:1559: _LIBCPP_ASSERT '__n < size()' failed. vector[] index out of bounds
Received signal 6
#0 0x7f639838d219 base::debug::CollectStackTrace()
#1 0x7f639828c843 base::debug::StackTrace::StackTrace()
#2 0x7f639838cd13 base::debug::(anonymous namespace)::StackDumpSignalHandler()
#3 0x7f63860fa8e0 (/usr/lib/x86_64-linux-gnu/libpthread-2.32.so+0x138df)
#4 0x7f6385ba0e71 gsignal
#5 0x7f6385b8a536 abort
#6 0x7f63861a915a std::__Cr::__libcpp_abort_debug_function()
#7 0x7f6392fbfb17 views::TableView::UpdateVirtualAccessibilityChildrenBounds()
#8 0x7f6392fbd6e7 views::TableView::SortItemsAndUpdateMapping()
#9 0x7f6392fc13a9 views::TableView::OnItemsAdded()
#10 0x559a669be274 policy::DeviceLocalAccountPolicyService::NotifyPolicyUpdated()
#11 0x559a673b7242 task_manager::TaskManagerImpl::TaskAdded()
...

The same issue can happen in TableView::OnItemsRemoved(), which was reported in https://crbug.com/chromium/1283805. https://source.chromium.org/chromium/chromium/src/+/main:ui/views/controls/table/table_view.cc;l=855-857;drc=0e45c020c43b1a9f6d2870ff7f92b30a2f03a458. `virtual_children` can be empty, so in this line:

    virtual_children[virtual_children.size() - 1]->RemoveFromParentView();

`virtual_children.size() - 1` is also out of bounds.


### gi...@appspot.gserviceaccount.com (2022-01-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cc6c21a0f3ab8a0d066b85dcfc5638de41a935cd

commit cc6c21a0f3ab8a0d066b85dcfc5638de41a935cd
Author: Ahmed Fakhry <afakhry@chromium.org>
Date: Fri Jan 07 02:27:29 2022

Fix out-of-bounds crashes in TableView

BUG=1283805, 1283807
TEST=Manual, added a unittest.

Change-Id: I127b7d9683c716ebfc2df4eaa47257785c7786f0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3368601
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: Ahmed Fakhry <afakhry@chromium.org>
Cr-Commit-Position: refs/heads/main@{#956343}

[modify] https://crrev.com/cc6c21a0f3ab8a0d066b85dcfc5638de41a935cd/ui/views/controls/table/table_view.cc
[modify] https://crrev.com/cc6c21a0f3ab8a0d066b85dcfc5638de41a935cd/ui/views/controls/table/table_view_unittest.cc


### af...@chromium.org (2022-01-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-07)

[Empty comment from Monorail migration]

### af...@chromium.org (2022-01-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-08)

Merge review required: M98 is already shipping to beta.

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-08)

Merge review required: M97 is already shipping to stable.

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

### sr...@google.com (2022-01-10)

pls answer https://crbug.com/chromium/1283807#c17 for merge review.

### am...@chromium.org (2022-01-11)

merge approved to M98, please merge to branch 4758 asap (before 12pm PST, tomorrow/Tuesday, 11 January) so this fix can be included in this week's beta release -- thank you! 

### sr...@google.com (2022-01-11)

Please complete your merge before 2pm PST today so it can be part of beta release tomorrow. I will cut the RC build after 2pm PST today Jan 11, 2022

### af...@chromium.org (2022-01-11)

[Comment Deleted]

### af...@chromium.org (2022-01-11)

For some reason, I didn't get email notification of all the above messages.

1. Fixes a couple of out-of-bounds array accesses that lead to crashes.
2. https://chromium-review.googlesource.com/c/chromium/src/+/3368601
3. Yes,
4. No,
5. +dhaddock@
6. No need for manual verification

### gi...@appspot.gserviceaccount.com (2022-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d9bd6f7c0f6fad3f4a710cacde3fefa78b1d190b

commit d9bd6f7c0f6fad3f4a710cacde3fefa78b1d190b
Author: Ahmed Fakhry <afakhry@chromium.org>
Date: Tue Jan 11 21:55:01 2022

[Merge to M-98] Fix out-of-bounds crashes in TableView

BUG=1283805, 1283807
TEST=Manual, added a unittest.

(cherry picked from commit cc6c21a0f3ab8a0d066b85dcfc5638de41a935cd)

Change-Id: I127b7d9683c716ebfc2df4eaa47257785c7786f0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3368601
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: Ahmed Fakhry <afakhry@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#956343}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3381395
Auto-Submit: Ahmed Fakhry <afakhry@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Scott Violet <sky@chromium.org>
Cr-Commit-Position: refs/branch-heads/4758@{#520}
Cr-Branched-From: 4a2cf4baf90326df19c3ee70ff987960d59a386e-refs/heads/main@{#950365}

[modify] https://crrev.com/d9bd6f7c0f6fad3f4a710cacde3fefa78b1d190b/ui/views/controls/table/table_view.cc
[modify] https://crrev.com/d9bd6f7c0f6fad3f4a710cacde3fefa78b1d190b/ui/views/controls/table/table_view_unittest.cc


### am...@chromium.org (2022-01-12)

merge approved for M96/M97, unless there are stability or other concerns about merging this to M96/M97, please merge to branches 4664 and 4692 before 11am PST, Friday 14 January so this can be included in the next Extended and Stable security respins -- thank you 

### gi...@appspot.gserviceaccount.com (2022-01-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/78fb8233e30d54aa60da398030bc971b1dc03127

commit 78fb8233e30d54aa60da398030bc971b1dc03127
Author: Ahmed Fakhry <afakhry@chromium.org>
Date: Thu Jan 13 17:37:04 2022

[Merge to M-97] Fix out-of-bounds crashes in TableView

BUG=1283805, 1283807
TEST=Manual, added a unittest.

(cherry picked from commit cc6c21a0f3ab8a0d066b85dcfc5638de41a935cd)

Change-Id: I127b7d9683c716ebfc2df4eaa47257785c7786f0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3368601
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: Ahmed Fakhry <afakhry@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#956343}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3385296
Auto-Submit: Ahmed Fakhry <afakhry@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Scott Violet <sky@chromium.org>
Cr-Commit-Position: refs/branch-heads/4692@{#1429}
Cr-Branched-From: 038cd96142d384c0d2238973f1cb277725a62eba-refs/heads/main@{#938553}

[modify] https://crrev.com/78fb8233e30d54aa60da398030bc971b1dc03127/ui/views/controls/table/table_view.cc
[modify] https://crrev.com/78fb8233e30d54aa60da398030bc971b1dc03127/ui/views/controls/table/table_view_unittest.cc


### gi...@appspot.gserviceaccount.com (2022-01-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/77f141ce750bb9a14e2c394165a15f3a3c6f3d1f

commit 77f141ce750bb9a14e2c394165a15f3a3c6f3d1f
Author: Ahmed Fakhry <afakhry@chromium.org>
Date: Thu Jan 13 19:49:22 2022

[Merge to M-96] Fix out-of-bounds crashes in TableView

BUG=1283805, 1283807
TEST=Manual, added a unittest.

(cherry picked from commit cc6c21a0f3ab8a0d066b85dcfc5638de41a935cd)

Change-Id: I127b7d9683c716ebfc2df4eaa47257785c7786f0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3368601
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: Ahmed Fakhry <afakhry@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#956343}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3385300
Auto-Submit: Ahmed Fakhry <afakhry@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Scott Violet <sky@chromium.org>
Cr-Commit-Position: refs/branch-heads/4664@{#1399}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/77f141ce750bb9a14e2c394165a15f3a3c6f3d1f/ui/views/controls/table/table_view.cc
[modify] https://crrev.com/77f141ce750bb9a14e2c394165a15f3a3c6f3d1f/ui/views/controls/table/table_view_unittest.cc


### am...@chromium.org (2022-01-19)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-19)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-02-11)

Hello, Samet. We appreciate your efforts and reporting this issue; unfortunately the VRP Panel has decided to decline a reward for this report. After careful evaluation, it was decided that the level of user interaction required for this issue falls into an implausible level of user interaction, resulting in this issue being more akin to a functional bug rather than a security bug due to the near zero level of attacker control and exploitability. 
If you can provide a simplified POC that demonstrates triggered of this issue with far fewer user interactions and not having to deleted all the columns Task Manager, we would be happy to revisit and reassess for a potential reward. 

### sa...@gmail.com (2022-02-11)

Hi amyressler@, it requires a lot of user interaction but that doesn't guarantee that you won't be abused. (Eg:1281941) What is the maximum number of user interactions required for a report to receive an award?

### sa...@gmail.com (2022-02-11)

If a victim is listening to the attacker's commands for any attack, it doesn't matter if the attack is at 5 steps or 10 steps.

### sa...@gmail.com (2022-02-11)

Also, the more steps there are, the more effort it takes to find it. In other words, it is just as difficult to detect this problem by only doing code review or using certain fuzzing methods. But I respect VRP's final decision.

Thanks

### am...@chromium.org (2022-02-15)

Hi Samet, there is not a maximum number of interactions that negate a reward, but more so a set or series of interactions that make the issue implausible a user could be reasonably convinced to perform them to perform a task that is consistent usual browsing behavior. 
While we genuinely appreciate your efforts, eligibility and reward decisions are not based on the difficulty to find the bug, but on the impact of the bug itself, exploitability, and the control a bug would provide an attacker to exploit more Chrome users.

### [Deleted User] (2022-04-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1283807?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058392)*
