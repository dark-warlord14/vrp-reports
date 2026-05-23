# SUMMARY: AddressSanitizer: heap-use-after-free web_view_impl.cc:1020 in blink::WebViewImpl::ClosePagePopup

| Field | Value |
|-------|-------|
| **Issue ID** | [40057288](https://issues.chromium.org/issues/40057288) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WindowDialog |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | dt...@chromium.org |
| **Created** | 2021-09-16 |
| **Bounty** | $7,500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4628.3 Safari/537.36

Steps to reproduce the problem:

#TestOn
Windows NT 10.0; Win64; x64
gs://chromium-browser-asan/win32-release_x64/asan-win32-release_x64-920053.zip

#Reproduce
This issue is not stable to reproduce, but it is easy to find through a code audit, so I did not provide a POC but provided an analysis

What is the expected behavior?

What went wrong?
Type of crash
render tab

Did this work before? N/A 

Chrome version: 95.0.4628.3  Channel: n/a
OS Version: 10.0

#Analysis
1. web_view is created as a self-reference obj released by calling Close()[2].
2. ChromeClientImpl has a raw pointer to WebViewImpl, the comment says this is a weakpointer, but obviously not[1].
3. when WebViewImpl::WebViewImpl called it will pass this to ChromeClientImpl[3] with out addref.
4. So when WebViewImpl::Close is called, the WebViewImpl object will be released, and ChromeClientImpl has a raw pointer to execute it, causing UAF.

```
third_party/blink/renderer/core/page/chrome_client_impl.h:314
// Handles window-level notifications from core on behalf of a WebView.
class CORE_EXPORT ChromeClientImpl final : public ChromeClient {
 public:
  explicit ChromeClientImpl(WebViewImpl*);

<<<-CUT->>>
  WebViewImpl* web_view_;  // Weak pointer.		<<[1]

third_party/blink/renderer/core/exported/web_view_impl.cc:483      
WebViewImpl* WebViewImpl::Create(
    WebViewClient* client,
    mojom::blink::PageVisibilityState visibility,
    bool is_prerendering,
    bool is_inside_portal,
    bool compositing_enabled,
    bool widgets_never_composited,
    WebViewImpl* opener,
    mojo::PendingAssociatedReceiver<mojom::blink::PageBroadcast> page_handle,
    blink::scheduler::WebAgentGroupScheduler& agent_group_scheduler,
    const SessionStorageNamespaceId& session_storage_namespace_id,
    absl::optional<SkColor> page_base_background_color) {

  // Take a self-reference for WebViewImpl that is released by calling Close(),
  // then return a raw pointer to the caller.
  auto web_view = base::AdoptRef(new WebViewImpl(			<<[2]
      client, visibility, is_prerendering, is_inside_portal,
      compositing_enabled, widgets_never_composited, opener,
      std::move(page_handle), agent_group_scheduler,
      session_storage_namespace_id, std::move(page_base_background_color)));
  web_view->AddRef();
  return web_view.get();
}

third_party/blink/renderer/core/exported/web_view_impl.cc:556
WebViewImpl::WebViewImpl(
    WebViewClient* client,
    mojom::blink::PageVisibilityState visibility,
    bool is_prerendering,
    bool is_inside_portal,
    bool does_composite,
    bool widgets_never_composited,
    WebViewImpl* opener,
    mojo::PendingAssociatedReceiver<mojom::blink::PageBroadcast> page_handle,
    blink::scheduler::WebAgentGroupScheduler& agent_group_scheduler,
    const SessionStorageNamespaceId& session_storage_namespace_id,
    absl::optional<SkColor> page_base_background_color)
    : widgets_never_composited_(widgets_never_composited),
      web_view_client_(client),
      chrome_client_(MakeGarbageCollected<ChromeClientImpl>(this)),			<<[3]
```

#Patch
My fix is very simple, addref to web_view_ when ChromeClientImpl create and release when it destruct.

```
diff --git a/third_party/blink/renderer/core/page/chrome_client_impl.cc b/third_party/blink/renderer/core/page/chrome_client_impl.cc
index 724a67a4011..1ec74ab756b 100644
--- a/third_party/blink/renderer/core/page/chrome_client_impl.cc
+++ b/third_party/blink/renderer/core/page/chrome_client_impl.cc
@@ -168,10 +168,14 @@ class CompositorAnimationTimeline;
 ChromeClientImpl::ChromeClientImpl(WebViewImpl* web_view)
     : web_view_(web_view),
       cursor_overridden_(false),
-      did_request_non_empty_tool_tip_(false) {}
+      did_request_non_empty_tool_tip_(false) {
+
+  web_view_->AddRef();
+}

 ChromeClientImpl::~ChromeClientImpl() {
   DCHECK(file_chooser_queue_.IsEmpty());
+  web_view_->Release();
 }

 void ChromeClientImpl::Trace(Visitor* visitor) const {

```

#asan
=================================================================
==7316==ERROR: AddressSanitizer: heap-use-after-free on address 0x103c80023388 at pc 0x7ff90e6b17a3 bp 0x000000bff050 sp 0x000000bff098
READ of size 8 at 0x103c80023388 thread T0
==7316==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ff90e6b17a2 in blink::WebViewImpl::ClosePagePopup C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\exported\web_view_impl.cc:1020
    #1 0x7ff91119d934 in blink::WebPagePopupImpl::Close C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\exported\web_page_popup_impl.cc:948
    #2 0x7ff909d3a665 in mojo::InterfaceEndpointClient::NotifyError C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:685
    #3 0x7ff90a5a4927 in IPC::`anonymous namespace'::ChannelAssociatedGroupController::NotifyEndpointOfError C:\b\s\w\ir\cache\builder\src\ipc\ipc_mojo_bootstrap.cc:803
    #4 0x7ff90a5a4de9 in IPC::`anonymous namespace'::ChannelAssociatedGroupController::NotifyEndpointOfErrorOnEndpointThread C:\b\s\w\ir\cache\builder\src\ipc\ipc_mojo_bootstrap.cc:823
    #5 0x7ff9099ec41a in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:178
    #6 0x7ff90c393de2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:360
    #7 0x7ff90c393442 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:260
    #8 0x7ff90c36d347 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:39
    #9 0x7ff90c3952e5 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:467
    #10 0x7ff90996ea43 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #11 0x7ff90bea76b6 in content::RendererMain C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:265
    #12 0x7ff9057f38cd in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:973
    #13 0x7ff9057f0326 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:390
    #14 0x7ff9057f1368 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:418
    #15 0x7ff8ff36148c in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:172
    #16 0x7ff656b85b74 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:169
    #17 0x7ff656b82be8 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:382
    #18 0x7ff656f751af in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #19 0x7ff9696b4d2d in BaseThreadInitThunk+0x1d (C:\WINDOWS\System32\KERNEL32.DLL+0x180014d2d)
    #20 0x7ff96ac35a7a in RtlUserThreadStart+0x2a (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180065a7a)

0x103c80023388 is located 776 bytes inside of 2728-byte region [0x103c80023080,0x103c80023b28)
freed by thread T0 here:
    #0 0x7ff656c26edb in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ff90e6b2721 in blink::WebViewImpl::Close C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\exported\web_view_impl.cc:1096
    #2 0x7ff90bea4d9d in content::RenderViewImpl::Destroy C:\b\s\w\ir\cache\builder\src\content\renderer\render_view_impl.cc:232
    #3 0x7ff9099ec41a in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:178
    #4 0x7ff90c393de2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:360
    #5 0x7ff90c393442 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:260
    #6 0x7ff90c36d347 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:39
    #7 0x7ff90c3952e5 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:467
    #8 0x7ff90996ea43 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #9 0x7ff90bea76b6 in content::RendererMain C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:265
    #10 0x7ff9057f38cd in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:973
    #11 0x7ff9057f0326 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:390
    #12 0x7ff9057f1368 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:418
    #13 0x7ff8ff36148c in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:172
    #14 0x7ff656b85b74 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:169
    #15 0x7ff656b82be8 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:382
    #16 0x7ff656f751af in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #17 0x7ff9696b4d2d in BaseThreadInitThunk+0x1d (C:\WINDOWS\System32\KERNEL32.DLL+0x180014d2d)
    #18 0x7ff96ac35a7a in RtlUserThreadStart+0x2a (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180065a7a)

previously allocated by thread T0 here:
    #0 0x7ff656c26fdb in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ff90adf0a23 in WTF::Partitions::FastMalloc C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\wtf\allocator\partitions.cc:291
    #2 0x7ff90e6a7e4e in blink::WebViewImpl::Create C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\exported\web_view_impl.cc:483
    #3 0x7ff90e6a7cd9 in blink::WebView::Create C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\exported\web_view_impl.cc:459
    #4 0x7ff90bea3c3f in content::RenderViewImpl::Initialize C:\b\s\w\ir\cache\builder\src\content\renderer\render_view_impl.cc:121
    #5 0x7ff90bea4c0b in content::RenderViewImpl::Create C:\b\s\w\ir\cache\builder\src\content\renderer\render_view_impl.cc:224
    #6 0x7ff90eb4c6a0 in content::AgentSchedulingGroup::CreateView C:\b\s\w\ir\cache\builder\src\content\renderer\agent_scheduling_group.cc:209
    #7 0x7ff9020eac6e in content::mojom::AgentSchedulingGroupStubDispatch::Accept C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\content\common\agent_scheduling_group.mojom.cc:573
    #8 0x7ff909d368b1 in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:898
    #9 0x7ff90c4d8286 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43
    #10 0x7ff909d3a13c in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:655
    #11 0x7ff90a5a5a40 in IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnEndpointThread C:\b\s\w\ir\cache\builder\src\ipc\ipc_mojo_bootstrap.cc:981
    #12 0x7ff90a59f935 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message),scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:690
    #13 0x7ff9099ec41a in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:178
    #14 0x7ff90c393de2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:360
    #15 0x7ff90c393442 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:260
    #16 0x7ff90c36d347 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:39
    #17 0x7ff90c3952e5 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:467
    #18 0x7ff90996ea43 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #19 0x7ff90bea76b6 in content::RendererMain C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:265
    #20 0x7ff9057f38cd in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:973
    #21 0x7ff9057f0326 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:390
    #22 0x7ff9057f1368 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:418
    #23 0x7ff8ff36148c in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:172
    #24 0x7ff656b85b74 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:169
    #25 0x7ff656b82be8 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:382
    #26 0x7ff656f751af in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #27 0x7ff9696b4d2d in BaseThreadInitThunk+0x1d (C:\WINDOWS\System32\KERNEL32.DLL+0x180014d2d)

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\exported\web_view_impl.cc:1020 in blink::WebViewImpl::ClosePagePopup
Shadow bytes around the buggy address:
  0x020810004620: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x020810004630: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x020810004640: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x020810004650: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x020810004660: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x020810004670: fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x020810004680: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x020810004690: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0208100046a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0208100046b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0208100046c0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==7316==ABORTING

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 11.4 KB)
- [patch.diff](attachments/patch.diff) (text/plain, 776 B)

## Timeline

### [Deleted User] (2021-09-16)

[Empty comment from Monorail migration]

### ca...@chromium.org (2021-09-16)

dtapuska: Can you help find an appropriate owner for this (or further triage). I was not able to reproduce this since there is no proof of concept, but the explanation seems plausible and the suggested fix is simple. Thanks

[Monorail components: Blink Platform>Apps>BrowserTag]

### [Deleted User] (2021-09-16)

[Empty comment from Monorail migration]

### dt...@chromium.org (2021-09-16)

dcheng@ thoughts on this one.

This seems like a GC timing issue to me. It looks ChromeClient is held on as a Member in some situations here: https://source.chromium.org/search?q=Member%3CChromeClient%3E&sq=&ss=chromium%2Fchromium%2Fsrc so while we reference ChromeClientImpl's lifecycle is tied to the Page's lifecycle it seems it can outlive the WebView and get called back on it for a popup.

A few things come to mind should WebViewImpl Closing the popup when it is destroyed. Seems it is self referenced until the mojo disconnect call. Should ChromeClientImpl not listen to ChromeDestroyed callback (which could invalidate web_view ptr... but we'd probably need to check for null in various spots). But being that this is GC'd object it is possible to call into references from it by the Members...

### mc...@chromium.org (2021-09-16)

Removing Platform>Apps>BrowserTag since it does not appear relevant (this component is for a particular extensions API).

[Monorail components: -Platform>Apps>BrowserTag]

### ch...@chromium.org (2021-09-16)

[Empty comment from Monorail migration]

[Monorail components: -Blink Blink>WindowDialog]

### [Deleted User] (2021-09-17)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-17)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dc...@chromium.org (2021-09-24)

I think there are several aspects to this bug.

1. It is 100% unsafe to have a 'weak pointer' but not clear it by setting it to null. The other alternative is to AddRef()/Release() WebViewImpl, but I'm not sure if this will have any other undesirable side effects. Nulling out web_view_ and maybe *not* adding checks is what I would propose (since we shouldn't be calling any of these methods after the WebView is closed really...)

2. Normally, WebView is not synchronously closed, right? But it's close by a posted task? Is it possible to have JS on the stack when we call WebView::Close()?

3. The particular free stack seems to be triggered by Mojo. So maybe there's another additional bug here that we should have closed all existing page popups when the webview itself was closed?

### dt...@chromium.org (2021-09-27)

reporter@ do you have more details of the reproduction steps. I agree that you can get a UAF from the code point of view but from my testing it seems contrived because you need to adjust browser side behavior. ie. The popup should always be destroyed on unfocus and that happens before the view is destroyed so writing a test that reproduces this seems not possible without complex hooking changing the normal flow.

### dt...@chromium.org (2021-09-27)

This is the callstack that cleans up a PagePopup when it is detached. 

#2 0x7fa884ed0346 blink::WebViewImpl::CleanupPagePopup()
#3 0x7fa884ebdbab blink::WebPagePopupImpl::ClosePopup()
#4 0x7fa884ed02a9 blink::WebViewImpl::ClosePagePopup()
#5 0x7fa8840908ec blink::PickerIndicatorElement::DetachLayoutTree()
#6 0x7fa883c518df blink::ContainerNode::DetachLayoutTree()
#7 0x7fa883d2e63c blink::ShadowRoot::DetachLayoutTree()
#8 0x7fa883caa343 blink::Element::DetachLayoutTree()
#9 0x7fa884064e7e blink::HTMLInputElement::DetachLayoutTree()
#10 0x7fa883c518df blink::ContainerNode::DetachLayoutTree()
#11 0x7fa883caa364 blink::Element::DetachLayoutTree()
#12 0x7fa883c518df blink::ContainerNode::DetachLayoutTree()
#13 0x7fa883caa364 blink::Element::DetachLayoutTree()
#14 0x7fa883c518df blink::ContainerNode::DetachLayoutTree()
#15 0x7fa883c6a2a6 blink::Document::Shutdown()
#16 0x7fa883f17236 blink::LocalDOMWindow::FrameDestroyed()
#17 0x7fa883f2914e blink::LocalFrame::DetachImpl()
#18 0x7fa883efb461 blink::Frame::Detach()
#19 0x7fa884743c0f blink::Page::WillBeDestroyed()
#20 0x7fa884ed0812 blink::WebViewImpl::Close()

So would like more information on how your ASAN code reproduced an example.

### m....@gmail.com (2021-09-28)

[Comment Deleted]

### [Deleted User] (2021-10-12)

dtapuska: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-25)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-05)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### m....@gmail.com (2021-11-09)

re https://crbug.com/chromium/1250227#c11 Do you have time to look at this issue, or assign it to others, thanks.

### dt...@chromium.org (2021-11-09)

I've had a fix posted for review for a while now... https://chromium-review.googlesource.com/c/chromium/src/+/3247534

I wasn't able to reproduce your issue it would be good to know if you can reproduce it with that patch.

dcheng@ ping on the review.

### m....@gmail.com (2021-11-09)

re https://crbug.com/chromium/1250227#c17 Thanks for your patch, I will download the pre-compiled ASAN version for testing tomorrow.

In local test https://crbug.com/chromium/1250227#c12 poc sample can reproduce stably.

### dt...@chromium.org (2021-11-09)

Ya it hasn't landed yet so a precompiled version won't work yet. I tried for a long time trying to reproduce https://crbug.com/chromium/1250227#c12 on a local build and didn't have success.

### m....@gmail.com (2021-11-09)

No problem,I will test when the pre-compiled version is landed.

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### m....@gmail.com (2021-11-17)

re https://crbug.com/chromium/1250227#c17 I compiled the ASAN version and tested locally.

Before patch-> reproduce stable
After patch-> not reproduce

conclusion-> The patch is working~

### [Deleted User] (2021-12-20)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-30)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dt...@chromium.org (2022-01-04)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-01-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/48ece4df40019535a3c21308941428ec82837c52

commit 48ece4df40019535a3c21308941428ec82837c52
Author: Dave Tapuska <dtapuska@chromium.org>
Date: Tue Jan 04 22:52:37 2022

Cancel WebPagePopup immediately on WebViewImpl::Close.

If we have a WebPagePopup cancel it immediately. Detaching it from
the layout was the handled via Detaching the layout nodes but that
is slightly complex. Call cancel before we destroy the layout tree.

BUG=1250227

Change-Id: I8707e59a3c99a57a16d8b8d8cb35213a33365833
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3247534
Reviewed-by: Stefan Zager <szager@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Dave Tapuska <dtapuska@chromium.org>
Cr-Commit-Position: refs/heads/main@{#955417}

[modify] https://crrev.com/48ece4df40019535a3c21308941428ec82837c52/third_party/blink/renderer/core/page/chrome_client_impl.cc
[modify] https://crrev.com/48ece4df40019535a3c21308941428ec82837c52/third_party/blink/renderer/core/exported/web_view_impl.cc


### dt...@chromium.org (2022-01-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-05)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-12)

one of the known instances in which the bot is ignoring fixes for medium severity bugs, so adding merge labels accordingly 

### [Deleted User] (2022-01-12)

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

### [Deleted User] (2022-01-12)

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

### [Deleted User] (2022-01-12)

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

### am...@chromium.org (2022-01-13)

I got a little too ambitious with the merge review labels on this one, merge-review for M98 should be sufficient for this issue 

### am...@google.com (2022-01-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-14)

Congratulations on yet another one! The VRP Panel has decided to award you $7500 for this report. Thank you for your report and great work! 

### am...@chromium.org (2022-01-14)

based on some initial checks, tentatively approving for merge to M98; please double check to ensure there are no stability issues or other concern and merge to branch 4758 at your earliest convenience -- thank you 

### go...@chromium.org (2022-01-14)

Please merge your change to M98 branch 4758 ASAP, Thank you.

### gi...@appspot.gserviceaccount.com (2022-01-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/008d0651213fdf43407f5fe90c48e5432c0b64c7

commit 008d0651213fdf43407f5fe90c48e5432c0b64c7
Author: Dave Tapuska <dtapuska@chromium.org>
Date: Fri Jan 14 21:11:59 2022

Cancel WebPagePopup immediately on WebViewImpl::Close.

If we have a WebPagePopup cancel it immediately. Detaching it from
the layout was the handled via Detaching the layout nodes but that
is slightly complex. Call cancel before we destroy the layout tree.

BUG=1250227

(cherry picked from commit 48ece4df40019535a3c21308941428ec82837c52)

Change-Id: I8707e59a3c99a57a16d8b8d8cb35213a33365833
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3247534
Reviewed-by: Stefan Zager <szager@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Dave Tapuska <dtapuska@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#955417}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3389469
Cr-Commit-Position: refs/branch-heads/4758@{#637}
Cr-Branched-From: 4a2cf4baf90326df19c3ee70ff987960d59a386e-refs/heads/main@{#950365}

[modify] https://crrev.com/008d0651213fdf43407f5fe90c48e5432c0b64c7/third_party/blink/renderer/core/page/chrome_client_impl.cc
[modify] https://crrev.com/008d0651213fdf43407f5fe90c48e5432c0b64c7/third_party/blink/renderer/core/exported/web_view_impl.cc


### [Deleted User] (2022-01-14)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-01-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-02-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-01)

[Empty comment from Monorail migration]

### vo...@google.com (2022-02-02)

[Empty comment from Monorail migration]

### vo...@google.com (2022-02-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-03)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-03)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vo...@google.com (2022-02-03)

1. Just one https://crrev.com/c/3430821
2. Low - trivial merge conflicts
3. Stable - M98
4. Yes

### gm...@google.com (2022-02-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-03)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gm...@google.com (2022-02-04)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-02-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/220ee40ce9d98c917c979923b1a2fa0d14ea484b

commit 220ee40ce9d98c917c979923b1a2fa0d14ea484b
Author: Zakhar Voit <voit@google.com>
Date: Sat Feb 05 13:41:37 2022

[M96-LTS] Cancel WebPagePopup immediately on WebViewImpl::Close.

If we have a WebPagePopup cancel it immediately. Detaching it from
the layout was the handled via Detaching the layout nodes but that
is slightly complex. Call cancel before we destroy the layout tree.

BUG=1250227

(cherry picked from commit 48ece4df40019535a3c21308941428ec82837c52)

(cherry picked from commit 008d0651213fdf43407f5fe90c48e5432c0b64c7)

Change-Id: I8707e59a3c99a57a16d8b8d8cb35213a33365833
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3247534
Commit-Queue: Dave Tapuska <dtapuska@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/main@{#955417}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3389469
Cr-Original-Commit-Position: refs/branch-heads/4758@{#637}
Cr-Original-Branched-From: 4a2cf4baf90326df19c3ee70ff987960d59a386e-refs/heads/main@{#950365}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3430821
Reviewed-by: Jana Grill <janagrill@google.com>
Owners-Override: Jana Grill <janagrill@google.com>
Commit-Queue: Zakhar Voit <voit@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1454}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/220ee40ce9d98c917c979923b1a2fa0d14ea484b/third_party/blink/renderer/core/page/chrome_client_impl.cc
[modify] https://crrev.com/220ee40ce9d98c917c979923b1a2fa0d14ea484b/third_party/blink/renderer/core/exported/web_view_impl.cc


### vo...@google.com (2022-02-07)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1250227?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057288)*
