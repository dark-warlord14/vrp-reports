# Fatal error in V8 API due to microtask queue depth inconsistency during IndexedDB operation.

| Field | Value |
|-------|-------|
| **Issue ID** | [434115938](https://issues.chromium.org/issues/434115938) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Blink>Bindings, Blink>JavaScript, Blink>Storage>IndexedDB |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 138.0.7186.0 |
| **Reporter** | cj...@gmail.com |
| **Assignee** | ca...@google.com |
| **Created** | 2025-07-25 |
| **Bounty** | Confirmed (amount unknown) |

## Description

# Steps to reproduce the problem

1. gn gen out/IndexedDBDebug
2. rm -rf /tmp/chrome-tmp && /chromium/src/out/IndexedDBDebug/chrome --no-sandbox --disable-gpu --enable-logging=stderr --user-data-dir=/tmp/chrome-tmp /test.html
   test.html:

<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>IndexedDB</title></head>
<body>
<script>
console.log(123123123123)
const openRequest\_108 = window.indexedDB.open('str\_7519', 1)
openRequest\_108.onupgradeneeded = (event) => {
const db\_108 = event.target.result;
const objectStore\_1 = db\_108.createObjectStore('objectStore\_581', {keyPath: 'a.b', autoIncrement: true});
objectStore\_1.put({});
objectStore\_1.createIndex('i', 't');
};
</script>
</body></html>
# Problem Description

The issue is that a nested keyPath is created with autoIncrement: true, but during put, the key is not correctly auto-incremented, causing the subsequent createIndex check to fail. This failure occurs only in the debug build due to strict consistency checks, while the release build executes without error.

# Additional Comments

cat /chromium/src/chrome/VERSION
MAJOR=138
MINOR=0
BUILD=7186
PATCH=0

# Summary

Fatal error in V8 API due to microtask queue depth inconsistency during IndexedDB operation.

# Custom Questions

#### Type of crash:

browser, indexedDB API

#### Crash state:

```
/index# rm -rf /tmp/chrome-tmp && /timer/chromium/src/out/IndexedDBDebug/chrome   --no-sandbox   --disable-gpu   --enable-logging=stderr     --user-data-dir=/tmp/chrome-tmp   file:///timer/index/test/test.html
[557751:557751:0725/203931.449904:WARNING:ui/linux/display_server_utils.cc:92] This is not a Wayland session. Falling back to X11. If you need to run Chrome on Wayland using some embedded compositor, e.g. Weston, please specify Wayland as your preferred Ozone platform, or use --ozone-platform=wayland.
[557788:557788:0725/203931.647945:WARNING:ui/gfx/linux/gpu_memory_buffer_support_x11.cc:49] dri3 extension not supported.
[557751:557751:0725/203931.674890:WARNING:chrome/browser/signin/account_consistency_mode_manager.cc:73] Desktop Identity Consistency cannot be enabled as no OAuth client ID and client secret have been configured.
[557751:557751:0725/203931.998315:ERROR:chrome/browser/ui/views/frame/browser_view.cc:6177] Attempting to show IPH IPH_TabSearchToolbarButton before browser initialization; IPH will not be shown.
[557789:557832:0725/203932.243371:WARNING:net/disk_cache/simple/simple_synchronous_entry.cc:1444] Could not open platform files for entry.
[557751:557751:0725/203932.348047:WARNING:ui/base/idle/idle_linux.cc:110] None of the known D-Bus ScreenSaver services could be used.
[557751:557751:0725/203932.444360:INFO:CONSOLE:5] "123123123123", source: file:///timer/index/test/test.html (5)
[557751:557773:0725/203932.479630:WARNING:content/browser/indexed_db/file_path_util.cc:97] GetMaximumPathComponentLength returned -1

#
# Fatal error in ../../v8/src/api/api-inl.h, line 189
# Debug check failed: microtask_queue->GetMicrotasksScopeDepth() || !microtask_queue->DebugMicrotasksScopeDepthIsZero().
#
#
#
#FailureMessage Object: 0x7ffd22f28f70#0 0x70200f44b1c9 base::debug::CollectStackTrace() [../../base/debug/stack_trace_posix.cc:1058:7]
#1 0x70200f3fa5ea base::debug::StackTrace::StackTrace() [../../base/debug/stack_trace.cc:255:20]
#2 0x70200f3fa555 base::debug::StackTrace::StackTrace() [../../base/debug/stack_trace.cc:250:28]
#3 0x701fe071497d gin::(anonymous namespace)::PrintStackTrace() [../../gin/v8_platform.cc:41:27]
#4 0x701f941d86e4 V8_Fatal() [../../v8/src/base/logging.cc:212:38]
#5 0x701f941d80a5 v8::base::(anonymous namespace)::DefaultDcheckHandler()
#6 0x701fb5e934aa v8::CallDepthScope<>::~CallDepthScope() [../../v8/src/api/api-inl.h:188:9]
#7 0x701fb5e4e4fe v8::Object::HasOwnProperty() [../../v8/src/api/api-inl.h:259:20]
#8 0x701faeaed044 blink::InjectV8KeyIntoV8Value() [../../third_party/blink/renderer/bindings/modules/v8/v8_binding_for_modules.cc:599:18]
#9 0x701faeaeeb80 blink::AssertPrimaryKeyValidOrInjectable() [../../third_party/blink/renderer/bindings/modules/v8/v8_binding_for_modules.cc:709:19]
#10 0x701fb0b4d517 blink::IDBCursor::value() [../../third_party/blink/renderer/modules/indexeddb/idb_cursor.cc:362:7]
#11 0x701fb0bcb024 blink::(anonymous namespace)::IndexPopulator::Invoke() [../../third_party/blink/renderer/modules/indexeddb/idb_object_store.cc:736:35]
#12 0x701fc3344118 blink::EventTarget::FireEventListeners() [../../third_party/blink/renderer/core/dom/events/event_target.cc:1089:15]
#13 0x701fc3342692 blink::EventTarget::FireEventListeners() [../../third_party/blink/renderer/core/dom/events/event_target.cc:1010:29]
#14 0x701fb0b81c87 blink::IDBEventDispatcher::Dispatch() [../../third_party/blink/renderer/modules/indexeddb/idb_event_dispatcher.cc:53:21]
#15 0x701fb0bef16b blink::IDBRequest::DispatchEventInternal() [../../third_party/blink/renderer/modules/indexeddb/idb_request.cc:933:7]
#16 0x701fc33424bc blink::EventTarget::DispatchEvent() [../../third_party/blink/renderer/core/dom/events/event_target.cc:898:10]
#17 0x701fb0be5d69 blink::IDBRequest::SendResult() [../../third_party/blink/renderer/modules/indexeddb/idb_request.cc:758:3]
#18 0x701fb0be5bfc blink::IDBRequest::SendResultCursorInternal() [../../third_party/blink/renderer/modules/indexeddb/idb_request.cc:439:3]
#19 0x701fb0beb988 blink::IDBRequest::SendResultCursor() [../../third_party/blink/renderer/modules/indexeddb/idb_request.cc:728:3]
#20 0x701fb0c001a4 blink::IDBRequestQueueItem::SendResult() [../../third_party/blink/renderer/modules/indexeddb/idb_request_queue_item.cc:366:17]
#21 0x701fb0c0b3d1 blink::IDBTransaction::OnResultReady() [../../third_party/blink/renderer/modules/indexeddb/idb_transaction.cc:415:32]
#22 0x701fb0bf5118 base::internal::DecayedFunctorTraits<>::Invoke<>() [../../base/functional/bind_internal.h:731:12]
#23 0x701fb0bf5099 base::internal::InvokeHelper<>::MakeItSo<>() [../../base/functional/bind_internal.h:923:12]
#24 0x701fb0bf502d base::internal::Invoker<>::RunImpl<>() [../../base/functional/bind_internal.h:1060:14]
#25 0x701fb0bf4fb9 base::internal::Invoker<>::RunOnce() [../../base/functional/bind_internal.h:973:12]
#26 0x701faf84af9c base::OnceCallback<>::Run() [../../base/functional/callback.h:156:12]
#27 0x701faf84af05 WTF::ThreadCheckingCallbackWrapper<>::RunInternal() [../../third_party/blink/renderer/platform/wtf/functional.h:242:33]
#28 0x701faf849da3 WTF::ThreadCheckingCallbackWrapper<>::Run() [../../third_party/blink/renderer/platform/wtf/functional.h:227:12]
#29 0x701faf84a928 base::internal::DecayedFunctorTraits<>::Invoke<>() [../../base/functional/bind_internal.h:731:12]
#30 0x701faf84a8a9 base::internal::InvokeHelper<>::MakeItSo<>() [../../base/functional/bind_internal.h:923:12]
#31 0x701faf84a83d base::internal::Invoker<>::RunImpl<>() [../../base/functional/bind_internal.h:1060:14]
#32 0x701faf84a7c9 base::internal::Invoker<>::RunOnce() [../../base/functional/bind_internal.h:973:12]
#33 0x701faf84af9c base::OnceCallback<>::Run() [../../base/functional/callback.h:156:12]
#34 0x701fb0bffaea blink::IDBRequestQueueItem::OnResultReady() [../../third_party/blink/renderer/modules/indexeddb/idb_request_queue_item.cc:260:31]
#35 0x701fb0bffde9 blink::IDBRequestQueueItem::StartLoading() [../../third_party/blink/renderer/modules/indexeddb/idb_request_queue_item.cc:320:5]
#36 0x701fb0c0b2f8 blink::IDBTransaction::EnqueueResult() [../../third_party/blink/renderer/modules/indexeddb/idb_transaction.cc:403:25]
#37 0x701fb0bea16f blink::IDBRequest::OnOpenCursor() [../../third_party/blink/renderer/modules/indexeddb/idb_request.cc:589:17]
#38 0x701fb0b71af5 base::internal::DecayedFunctorTraits<>::Invoke<>() [../../base/functional/bind_internal.h:731:12]
#39 0x701fb0b71a36 base::internal::InvokeHelper<>::MakeItSo<>() [../../base/functional/bind_internal.h:947:5]
#40 0x701fb0b719b5 base::internal::Invoker<>::RunImpl<>() [../../base/functional/bind_internal.h:1060:14]
#41 0x701fb0b71901 base::internal::Invoker<>::RunOnce() [../../base/functional/bind_internal.h:973:12]
#42 0x701fb0b72a28 base::OnceCallback<>::Run() [../../base/functional/callback.h:156:12]
#43 0x701fb0b72972 WTF::ThreadCheckingCallbackWrapper<>::RunInternal() [../../third_party/blink/renderer/platform/wtf/functional.h:242:33]
#44 0x701fb0b7174f WTF::ThreadCheckingCallbackWrapper<>::Run() [../../third_party/blink/renderer/platform/wtf/functional.h:227:12]
#45 0x701fb0b72365 base::internal::DecayedFunctorTraits<>::Invoke<>() [../../base/functional/bind_internal.h:731:12]
#46 0x701fb0b722c1 base::internal::InvokeHelper<>::MakeItSo<>() [../../base/functional/bind_internal.h:923:12]
#47 0x701fb0b72255 base::internal::Invoker<>::RunImpl<>() [../../base/functional/bind_internal.h:1060:14]
#48 0x701fb0b721d1 base::internal::Invoker<>::RunOnce() [../../base/functional/bind_internal.h:973:12]
#49 0x701fb0b72a28 base::OnceCallback<>::Run() [../../base/functional/callback.h:156:12]
#50 0x701fb266f9a0 blink::mojom::blink::IDBDatabase_OpenCursor_ForwardToCallback::Accept() [gen/third_party/blink/public/mojom/indexeddb/indexeddb.mojom-blink.cc:6553:26]
#51 0x7020106def60 mojo::InterfaceEndpointClient::HandleValidatedMessage() [../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1054:41]
#52 0x7020106de704 mojo::InterfaceEndpointClient::HandleIncomingMessageThunk::Accept() [../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:377:18]
#53 0x7020106f72fa mojo::MessageDispatcher::Accept() [../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19]
#54 0x7020106e0e31 mojo::InterfaceEndpointClient::HandleIncomingMessage() [../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:731:20]
#55 0x7020106fad3f mojo::internal::MultiplexRouter::ProcessIncomingMessage() [../../mojo/public/cpp/bindings/lib/multiplex_router.cc:1120:42]
#56 0x7020106fa4bb mojo::internal::MultiplexRouter::Accept() [../../mojo/public/cpp/bindings/lib/multiplex_router.cc:733:7]
#57 0x7020106f72fa mojo::MessageDispatcher::Accept() [../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19]
#58 0x7020106c42ad mojo::Connector::DispatchMessage() [../../mojo/public/cpp/bindings/lib/connector.cc:561:49]
#59 0x7020106c4c7e mojo::Connector::ReadAllAvailableMessages() [../../mojo/public/cpp/bindings/lib/connector.cc:619:14]
#60 0x7020106c4a56 mojo::Connector::OnHandleReadyInternal() [../../mojo/public/cpp/bindings/lib/connector.cc:450:3]
#61 0x7020106c49d0 mojo::Connector::OnWatcherHandleReady() [../../mojo/public/cpp/bindings/lib/connector.cc:416:3]
#62 0x7020106ca128 base::internal::DecayedFunctorTraits<>::Invoke<>() [../../base/functional/bind_internal.h:731:12]
#63 0x7020106ca092 base::internal::InvokeHelper<>::MakeItSo<>() [../../base/functional/bind_internal.h:923:12]
#64 0x7020106ca005 base::internal::Invoker<>::RunImpl<>() [../../base/functional/bind_internal.h:1060:14]
#65 0x7020106c9f40 base::internal::Invoker<>::Run() [../../base/functional/bind_internal.h:980:12]
#66 0x7020106c9912 base::RepeatingCallback<>::Run() [../../base/functional/callback.h:344:12]
#67 0x7020106c934f mojo::SimpleWatcher::DiscardReadyState() [../../mojo/public/cpp/system/simple_watcher.h:192:14]
#68 0x7020106c954f base::internal::DecayedFunctorTraits<>::Invoke<>() [../../base/functional/bind_internal.h:664:12]
#69 0x7020106c951a base::internal::InvokeHelper<>::MakeItSo<>() [../../base/functional/bind_internal.h:923:12]
#70 0x7020106c94bd base::internal::Invoker<>::RunImpl<>() [../../base/functional/bind_internal.h:1060:14]
#71 0x7020106c9418 base::internal::Invoker<>::Run() [../../base/functional/bind_internal.h:980:12]
#72 0x70200fdc366a base::RepeatingCallback<>::Run() [../../base/functional/callback.h:344:12]
#73 0x70200fdc241d mojo::SimpleWatcher::OnHandleReady() [../../mojo/public/cpp/system/simple_watcher.cc:278:14]
#74 0x70200fdc3ce4 base::internal::DecayedFunctorTraits<>::Invoke<>() [../../base/functional/bind_internal.h:731:12]
#75 0x70200fdc3bfc base::internal::InvokeHelper<>::MakeItSo<>() [../../base/functional/bind_internal.h:947:5]
#76 0x70200fdc3b1d base::internal::Invoker<>::RunImpl<>() [../../base/functional/bind_internal.h:1060:14]
#77 0x70200fdc3a79 base::internal::Invoker<>::RunOnce() [../../base/functional/bind_internal.h:973:12]
#78 0x70200f0aa35c base::OnceCallback<>::Run() [../../base/functional/callback.h:156:12]
#79 0x70200f28ff84 base::TaskAnnotator::RunTaskImpl() [../../base/task/common/task_annotator.cc:209:34]
#80 0x70200f2fe818 base::TaskAnnotator::RunTask<>() [../../base/task/common/task_annotator.h:106:5]
#81 0x70200f2fe2ae base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl() [../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:456:23]
#82 0x70200f2fd91a base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() [../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:330:40]
#83 0x70200f2fe4e3 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
#84 0x70200f131568 base::MessagePumpDefault::Run() [../../base/message_loop/message_pump_default.cc:42:55]
#85 0x70200f2feea7 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run() [../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:629:12]
#86 0x70200f20cf6b base::RunLoop::Run() [../../base/run_loop.cc:134:14]
#87 0x7020064c5f95 content::RendererMain() [../../content/renderer/renderer_main.cc:356:16]
#88 0x7020068e03b0 content::RunZygote() [../../content/app/content_main_runner_impl.cc:699:14]
#89 0x7020068e0b3b content::RunOtherNamedProcessTypeMain() [../../content/app/content_main_runner_impl.cc:803:12]
#90 0x7020068e1ed1 content::ContentMainRunnerImpl::Run() [../../content/app/content_main_runner_impl.cc:1183:10]
#91 0x7020068ddf86 content::RunContentProcess() [../../content/app/content_main.cc:374:36]
#92 0x7020068de586 content::ContentMain() [../../content/app/content_main.cc:387:10]
#93 0x5c798eb77980 ChromeMain [../../chrome/app/chrome_main.cc:222:12]
#94 0x5c798eb77712 main
#95 0x701fab42a1ca (/usr/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9)
#96 0x701fab42a28b __libc_start_main
#97 0x5c798eb7762a _start
[0725/203933.029361:ERROR:third_party/crashpad/crashpad/util/file/file_io_posix.cc:145] open /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq: No such file or directory (2)
[0725/203933.029477:ERROR:third_party/crashpad/crashpad/util/file/file_io_posix.cc:145] open /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq: No such file or directory (2)

```
#### Reporter credit:

Please credit as Jingyi Chen

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A \

## Attachments

- [test.html](attachments/test.html) (text/html, 478 B)
- [args.txt](attachments/args.txt) (text/plain, 255.2 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2025-07-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5887101702701056.

### pg...@google.com (2025-07-25)

is the tmp directory important? unsure - trying to repro on clusterfuzz before sending over to the (secondary) v8 sheriff

setting **provisional** severity=s1 and foundin 138 (extended stable)

### cj...@gmail.com (2025-07-26)

Yes, the /tmp/chrome-tmp directory is important when testing or debugging because it serves as Chrome’s user data directory, storing runtime states such as IndexedDB databases, cache, and cookies. Using a clean /tmp/chrome-tmp for each run ensures a fresh environment, avoids interference from previous data, and improves the reproducibility of test results.  

Besides, the crash is non-reproducible in ClusterFuzz because our build configuration differs significantly from theirs. We use a debug build with dcheck_always_on=true and is_debug=true, which enables additional DCHECK assertions and debug-only code paths, while ClusterFuzz uses a release ASan/LSan build (dcheck_always_on=false, is_debug=false, is_asan=true, is_lsan=true). Such crashes often only occur in debug builds with DCHECK enabled and are optimized away or suppressed in release configurations. The full build arguments we used to reproduce the crash are attached for your reference.

### ch...@google.com (2025-07-26)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-07-26)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### bi...@google.com (2025-07-29)

This looks like V8 API misuse. Andrey, could you please take a look or help finding the right owner?

### pe...@google.com (2025-08-07)

The issue's primary component must be in the Component Tags, so re-adding it. To change the primary component, use the edit button at the top of the issue, just above the title.

### ca...@google.com (2025-08-08)

This is because we're missing MicrotasksScope, which is required by all v8 API calls since we [initialize isolate with `v8::MicrotasksPolicy::kScoped`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/bindings/core/v8/v8_initializer.cc;l=795). The fix is in progress: <https://chromium-review.googlesource.com/c/chromium/src/+/6829385>

### dx...@google.com (2025-08-13)

Project: chromium/src  

Branch:  main  

Author:  Andrey Kosyakov [caseq@chromium.org](mailto:caseq@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6829385>

Create v8::MicrotasksScope in IndexPopulator native event listener

---


Expand for full commit details
```
     
    ... otherwise nested calls to v8 API are going to trigger a DCHECK(). 
     
    Bug: 434115938 
    Change-Id: I855212793fccbc7c3e521eb8a13183523021a5a4 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6829385 
    Commit-Queue: Andrey Kosyakov <caseq@chromium.org> 
    Reviewed-by: Fergal Daly <fergal@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1500514}

```

---

Files:

- M `third_party/blink/renderer/modules/indexeddb/idb_object_store.cc`
- A `third_party/blink/web_tests/external/wpt/IndexedDB/crashtests/create-index.any.js`

---

Hash: [cd5adf6e5bddc1e0dc6d3c4c24e9c7778e4c23a7](https://chromiumdash.appspot.com/commit/cd5adf6e5bddc1e0dc6d3c4c24e9c7778e4c23a7)  

Date: Wed Aug 13 00:13:40 2025


---

### sp...@google.com (2025-08-21)

** NOTE: This is an automatically generated email **

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this issue does not meet the criteria to qualify for a reward.

Rationale for this decision:
Hello, thank you for the report. Based on our assessment, this does not appear to be any evidence of an exploitable security issue here and this appears to be a functional issue. Therefore, this report is unfortunately not eligible for a Chrome VRP reward.

Please note that the fact that this issue is not being rewarded does not mean that the product team won't fix the issue. We have filed a bug with the product team and they will review your report and decide if a fix is required. We'll let you know if the issue was fixed.

Regards,
Google Security Bot


--
How did we do? Please fill out a short anonymous survey (https://goo.gl/IR3KRH).

### dx...@google.com (2025-08-28)

Project: chromium/src  

Branch:  main  

Author:  Fergal Daly [fergal@chromium.org](mailto:fergal@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6883410>

Tweak create-index.any.js to use IndexedDB test infrastructure.

---


Expand for full commit details
```
     
    https://crrev.com/c/6894032 shows that this still triggers the same DCHECK. 
     
    Bug: 434115938 
    Change-Id: Iadb57ed2f9af571e8e482b40fb627341c73923b5 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6883410 
    Reviewed-by: Andrey Kosyakov <caseq@chromium.org> 
    Commit-Queue: Fergal Daly <fergal@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1508091}

```

---

Files:

- M `third_party/blink/web_tests/external/wpt/IndexedDB/crashtests/create-index.any.js`

---

Hash: [917edcc70e785a1937f34a1a45ca7bac1f5cd574](https://chromiumdash.appspot.com/commit/917edcc70e785a1937f34a1a45ca7bac1f5cd574)  

Date: Thu Aug 28 23:29:49 2025


---

### ch...@google.com (2025-11-20)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Hello, thank you for the report. Based on our assessment, this does not appear to be any evidence of an exploitable security issue here and this appears to be a functional issue. Therefore, this report is unfortunately not eligible for a Chrome VRP reward.
> 
> Please note that the fact that this issue is not being rewarded does not mean that the product team won't fix the issue. We have filed a bug with the product team and they will review your report and decide if a fix is required. We'll let you

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/434115938)*
