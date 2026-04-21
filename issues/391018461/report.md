# use-after-poison in AtomicWriteMemcpyImpl<unsigned long>

| Field | Value |
|-------|-------|
| **Issue ID** | [391018461](https://issues.chromium.org/issues/391018461) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>GarbageCollection |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | ml...@chromium.org |
| **Created** | 2025-01-20 |
| **Bounty** | $7,000.00 |

## Description

VULNERABILITY DETAILS
use-after-poison in AtomicWriteMemcpyImpl<unsigned long>

VERSION
Chromium	134.0.6965.0 (Developer Build) (64-bit) 
OS	Linux

REPRODUCTION CASE
1. Download the latest asan build 
2. put the attchments into the dir and run python -m http.server 8000
3. Run the command: ./chrome --user-data-dir=/tmp/any --no-sandbox http://localhost:8000/poc.html

I can reproduce this issue on both Windows and Linux systems

PS:The issue is easier to reproduce when the system has higher memory capacity.


FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: [tab, browser, etc.]
2285:2301:0119/185153.013555:ERROR:registration_request.cc(291)] Registration response error message: DEPRECATED_ENDPOINT
=================================================================
==2393==ERROR: AddressSanitizer: use-after-poison on address 0x7ba601c80050 at pc 0x562a914d8a48 bp 0x7ffee1a685c0 sp 0x7ffee1a685b8
READ of size 8 at 0x7ba601c80050 thread T0 (chrome)
==2393==WARNING: invalid path to external symbolizer!
==2393==WARNING: Failed to use and restart external symbolizer!
    #0 0x562a914d8a47 in AtomicWriteMemcpyImpl<unsigned long> ./../../third_party/blink/renderer/platform/wtf/atomic_operations.cc:58:34
    #1 0x562a914d8a47 in WTF::AtomicWriteMemcpy(void*, void const*, unsigned long) ./../../third_party/blink/renderer/platform/wtf/atomic_operations.cc:126:3
    #2 0x562a98bbd4b7 in Move ./../../third_party/blink/renderer/platform/wtf/vector.h:223:7
    #3 0x562a98bbd4b7 in WTF::Vector<cppgc::internal::BasicMember<blink::Element, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 0u, blink::HeapAllocator>::ReallocateBuffer(unsigned int) ./../../third_party/blink/renderer/platform/wtf/vector.h:2480:3
    #4 0x562a98bbcfac in WTF::Vector<cppgc::internal::BasicMember<blink::Element, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 0u, blink::HeapAllocator>::reserve(unsigned int) ./../../third_party/blink/renderer/platform/wtf/vector.h:2051:3
    #5 0x562a99898b30 in ExpandCapacity ./../../third_party/blink/renderer/platform/wtf/vector.h:1947:3
    #6 0x562a99898b30 in ExpandCapacity<blink::Element *> ./../../third_party/blink/renderer/platform/wtf/vector.h:1969:3
    #7 0x562a99898b30 in void WTF::Vector<cppgc::internal::BasicMember<blink::Element, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 0u, blink::HeapAllocator>::AppendSlowCase<blink::Element*>(blink::Element*&&) ./../../third_party/blink/renderer/platform/wtf/vector.h:2169:9
    #8 0x562a9cd77c14 in push_back<blink::Element *> ./../../third_party/blink/renderer/platform/wtf/vector.h:2119:3
    #9 0x562a9cd77c14 in AppendElement ./../../third_party/blink/renderer/core/css/selector_query.cc:97:12
    #10 0x562a9cd77c14 in void blink::CollectElementsByTagName<blink::AllElementsSelectorQueryTrait>(blink::ContainerNode&, blink::QualifiedName const&, blink::AllElementsSelectorQueryTrait::OutputType&) ./../../third_party/blink/renderer/core/css/selector_query.cc:205:7
    #11 0x562a9cd70fb1 in void blink::SelectorQuery::Execute<blink::AllElementsSelectorQueryTrait>(blink::ContainerNode&, blink::AllElementsSelectorQueryTrait::OutputType&) const ./../../third_party/blink/renderer/core/css/selector_query.cc:529:11
    #12 0x562a9cd70905 in blink::SelectorQuery::QueryAll(blink::ContainerNode&) const ./../../third_party/blink/renderer/core/css/selector_query.cc:142:3
    #13 0x562a9daf1dd7 in blink::(anonymous namespace)::v8_document::QuerySelectorAllOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/modules/v8/v8_document.cc:7852:39
    #14 0x562a7fe7ca3f in Builtins_CallApiCallbackGeneric setup-isolate-deserialize.cc:0:0
    #9 0x562adfec097d  (<unknown module>)
    #15 0x562a7fe7875b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc:0:0
    #16 0x562a7fe784aa in Builtins_JSEntry setup-isolate-deserialize.cc:0:0
    #17 0x562a7bc4a1bb in Call ./../../v8/src/execution/simulator.h:191:12
    #18 0x562a7bc4a1bb in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:437:22
    #19 0x562a7bc48ba9 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>, v8::base::Vector<v8::internal::DirectHandle<v8::internal::Object> const>) ./../../v8/src/execution/execution.cc:527:10
    #20 0x562a7b772ba3 in v8::Function::Call(v8::Isolate*, v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) ./../../v8/src/api/api.cc:5605:7
    #21 0x562a984f5fc8 in blink::V8ScriptRunner::CallFunction(v8::Local<v8::Function>, blink::ExecutionContext*, v8::Local<v8::Value>, int, v8::Local<v8::Value>*, v8::Isolate*) ./../../third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:886:48
    #22 0x562a9d1e4e4e in CallInternal ./../../third_party/blink/renderer/bindings/core/v8/callback_invoke_helper.cc:142:12
    #23 0x562a9d1e4e4e in blink::bindings::CallbackInvokeHelper<blink::CallbackFunctionBase, (blink::bindings::CallbackInvokeHelperMode)2, (blink::bindings::CallbackReturnTypeIsPromise)0>::Call(int, v8::Local<v8::Value>*) ./../../third_party/blink/renderer/bindings/core/v8/callback_invoke_helper.cc:166:10
    #24 0x562a9d1f3fa2 in blink::V8EventHandlerNonNull::InvokeWithoutRunnabilityCheck(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::HeapVector<blink::ScriptValue, 0u> const&) ./gen/third_party/blink/renderer/bindings/core/v8/v8_event_handler_non_null.cc:183:13
    #25 0x562a990d4749 in blink::JSEventHandler::InvokeInternal(blink::EventTarget&, blink::Event&, v8::Local<v8::Value>) ./../../third_party/blink/renderer/bindings/core/v8/js_event_handler.cc:134:14
    #26 0x562a98fb630a in blink::JSBasedEventListener::Invoke(blink::ExecutionContext*, blink::Event*) ./../../third_party/blink/renderer/bindings/core/v8/js_based_event_listener.cc:158:5
    #27 0x562a98fa5906 in blink::EventTarget::FireEventListeners(blink::Event&, blink::EventTargetData*, blink::HeapVector<cppgc::internal::BasicMember<blink::RegisteredEventListener, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 1u>) ./../../third_party/blink/renderer/core/dom/events/event_target.cc:1094:15
    #28 0x562a98fa39b4 in blink::EventTarget::FireEventListeners(blink::Event&) ./../../third_party/blink/renderer/core/dom/events/event_target.cc:1016:29
    #29 0x562a996d86fe in blink::LocalDOMWindow::DispatchEvent(blink::Event&, blink::EventTarget*) ./../../third_party/blink/renderer/core/frame/local_dom_window.cc:2156:10
    #30 0x562a996d7eb6 in blink::LocalDOMWindow::DispatchLoadEvent() ./../../third_party/blink/renderer/core/frame/local_dom_window.cc:2116:5
    #31 0x562a996d7695 in blink::LocalDOMWindow::DispatchWindowLoadEvent() ./../../third_party/blink/renderer/core/frame/local_dom_window.cc:907:3
    #32 0x562a996d8123 in blink::LocalDOMWindow::DocumentWasClosed() ./../../third_party/blink/renderer/core/frame/local_dom_window.cc:911:3
    #33 0x562a9c7b9b91 in blink::Document::ImplicitClose() ./../../third_party/blink/renderer/core/dom/document.cc:3940:18
    #34 0x562a9c7bac8b in blink::Document::CheckCompletedInternal() ./../../third_party/blink/renderer/core/dom/document.cc:4056:5
    #35 0x562a9c7b97e2 in blink::Document::CheckCompleted() ./../../third_party/blink/renderer/core/dom/document.cc:4018:7
    #36 0x562a9ad9f0b9 in blink::FrameLoader::FinishedParsing() ./../../third_party/blink/renderer/core/loader/frame_loader.cc:460:26
    #37 0x562a9c7f29ba in blink::Document::FinishedParsing() ./../../third_party/blink/renderer/core/dom/document.cc:7440:21
    #38 0x562a9cae5c52 in end ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:1084:18
    #39 0x562a9cae5c52 in AttemptToRunDeferredScriptsAndEnd ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:1097:3
    #40 0x562a9cae5c52 in blink::HTMLDocumentParser::PrepareToStopParsing() ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:563:3
    #41 0x562a9caeb6f9 in blink::HTMLDocumentParser::AttemptToEnd() ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:1121:3
    #42 0x562a9cae661e in blink::HTMLDocumentParser::PumpTokenizerIfPossible() ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:651:5
    #43 0x562a9cae6e3c in blink::HTMLDocumentParser::DeferredPumpTokenizerIfPossible(bool, base::TimeTicks) ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:623:7
    #44 0x562a9cb0491c in Invoke<void (blink::HTMLDocumentParser::*)(bool, base::TimeTicks), cppgc::internal::BasicPersistent<blink::HTMLDocumentParser, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, bool, base::TimeTicks> ./../../base/functional/bind_internal.h:729:12
    #45 0x562a9cb0491c in MakeItSo<void (blink::HTMLDocumentParser::*)(bool, base::TimeTicks), std::__Cr::tuple<cppgc::internal::BasicPersistent<blink::HTMLDocumentParser, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, bool, base::TimeTicks> > ./../../base/functional/bind_internal.h:921:12
    #46 0x562a9cb0491c in RunImpl<void (blink::HTMLDocumentParser::*)(bool, base::TimeTicks), std::__Cr::tuple<cppgc::internal::BasicPersistent<blink::HTMLDocumentParser, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, bool, base::TimeTicks>, 0UL, 1UL, 2UL> ./../../base/functional/bind_internal.h:1058:14
    #47 0x562a9cb0491c in base::internal::Invoker<base::internal::FunctorTraits<void (blink::HTMLDocumentParser::*&&)(bool, base::TimeTicks), cppgc::internal::BasicPersistent<blink::HTMLDocumentParser, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>&&, bool&&, base::TimeTicks&&>, base::internal::BindState<true, true, false, void (blink::HTMLDocumentParser::*)(bool, base::TimeTicks), cppgc::internal::BasicPersistent<blink::HTMLDocumentParser, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, bool, base::TimeTicks>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:971:12
    #48 0x562a8a589862 in Run ./../../base/functional/callback.h:156:12
    #49 0x562a8a589862 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:210:34
    #50 0x562a8a5f3a38 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:472:11)> ./../../base/task/common/task_annotator.h:106:5
    #51 0x562a8a5f3a38 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:470:23
    #52 0x562a8a5f27da in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:330:40
    #53 0x562a8a5f476a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #54 0x562a8a470f41 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:42:55
    #55 0x562a8a5f532c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:643:12
    #56 0x562a8a51856f in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #57 0x562aa1bd7331 in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:351:16
    #58 0x562a8766d134 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:678:14
    #59 0x562a8766dffd in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:782:12
    #60 0x562a87670895 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1142:10
    #61 0x562a8766b4cd in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:348:36
    #62 0x562a8766babb in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:361:10
    #63 0x562a75b5cb1a in ChromeMain ./../../chrome/app/chrome_main.cc:222:12
    #64 0x7fb251c25082 in __libc_start_main /build/glibc-LcI20x/glibc-2.31/csu/../csu/libc-start.c:308:16

Address 0x7ba601c80050 is a wild pointer inside of access range of size 0x000000000008.
SUMMARY: AddressSanitizer: use-after-poison (/home/test/chromium/chrome+0x2a901a47) (BuildId: 32b11e2b295747ed)
Shadow bytes around the buggy address:
  0x7ba601c7fd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba601c7fe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba601c7fe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba601c7ff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ba601c7ff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7ba601c80000: 00 00 00 00 00 00 00 00 00 00[f7]f7 f7 f7 f7 f7
  0x7ba601c80080: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7ba601c80100: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7ba601c80180: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7ba601c80200: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7ba601c80280: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
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

==2393==ADDITIONAL INFO

==2393==Note: Please include this section with the ASan report.
Task trace:
    #0 0x562a9caeacef in blink::HTMLDocumentParser::SchedulePumpTokenizer(bool) ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:892:7
    #1 0x562a8cc80b32 in IPC::ChannelAssociatedGroupController::Accept(mojo::Message*) ./../../ipc/ipc_mojo_bootstrap.cc:1141:13


Command line: `/proc/self/exe --type=renderer --crashpad-handler-pid=2287 --enable-crash-reporter=, --user-data-dir=/tmp/test --change-stack-guard-on-fork=enable --no-sandbox --file-url-path-alias=/gen=/home/test/chromium/gen --ozone-platform=x11 --lang=en-US --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=6 --time-ticks-at-unix-epoch=-1737340891078071 --launch-time-ticks=210467608 --shared-files=v8_context_snapshot_data:100 --metrics-shmem-handle=4,i,17239521505382249196,13372886934701411403,2097152 --field-trial-handle=3,i,9977679730515195972,12697029115113428102,262144 --variations-seed-version`


==2393==END OF ADDITIONAL INFO
==2393==ABORTING
[2285:2301:0119/185833.040177:ERROR:registration_request.cc(291)] Registration response error message: DEPRECATED_ENDPOINT

## Attachments

- poc.html (text/html, 379 B)
- frame1.html (text/html, 640 B)
- frame2.html (text/html, 17.7 KB)
- stackscan1.log (text/plain, 587.4 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2025-01-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4770103786668032.

### ad...@google.com (2025-01-20)

I can't reproduce this manually, and ClusterFuzz failed too.

I assume this is happening in times of resource stress, but still, we shouldn't be seeing a use-after-poison even if RAM is exhausted.

I'm going to assume this is a real issue and pass it on to the Blink team, but Blink folks please note we haven't been able to reproduce this within the security team. We also therefore don't have any ideas when it was introduced so I'm labeling as if this only affects 134+ which may be wrong. If that's wrong please adjust the FoundIn field.

### ad...@google.com (2025-01-20)

Rating as S1 assuming renderer RCE can be achieved.

### ad...@google.com (2025-01-20)

Morten, please could you suggest a good owner here?

### pe...@google.com (2025-01-20)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2025-01-20)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### pe...@google.com (2025-01-20)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### 0x...@gmail.com (2025-01-20)

In a Linux system with 32GB of memory, the issue can be reproduced but it's relatively difficult to trigger. The webpage refreshes periodically, so you may need to wait longer to reproduce the issue.In systems with 64GB of memory or more, it can be triggered more easily.

You can set smaller numbers to trigger it in systems with less memory.

```
for (var index = 0; index < 5555; ++index)
    target.appendChild(template.cloneNode(true));

for (var index = 0; index < 5555; ++index)
    document.querySelectorAll("div");

```

You can can also run this comand to increase the success rate:

`./chrome --user-data-dir=/tmp/any --no-sandbox http://localhost:8000/poc.html http://localhost:8000/poc.html http://localhost:8000/poc.html`

### ms...@chromium.org (2025-01-22)

No need for web server or frames. Also reproducible in content\_shell. Just load this:

```
<!DOCTYPE html>
<div id="target" style="display:none;"><div><div><div><div><div></div></div></div></div></div></div>
<p id="message">Please wait...</p>
<script>
  var template = target.firstChild;

  // Build a large:ish tree.
  for (var index = 0; index < 10000; ++index) {
    target.appendChild(template.cloneNode(true));
  }

  // Create many large StaticNodeList objects.
  for (var index = 0; index < 10000; ++index) {
    document.querySelectorAll("div");
  }

  message.innerHTML = "PASS - retrying in 5 seconds.";

  setTimeout(() => {
    location.reload()
  }, 5000);
</script>

```

### an...@chromium.org (2025-01-22)

I can reproduce this after a while, both with the original case and mstensho's case.

Provided I understand how ASAN works, it appears that in `Vector::reserve` -> `ReallocateBuffer` -> `AtomicWriteMemcpyImpl`, the `to` buffer is somehow poisoned (see patch below used to determine this). Possibly, the alignment check reading a `size_t` from `to` is the 8-byte read ASAN originally complained about here.

I don't think the destination buffer during a Vector realloc is something an outside user of Vector can control at all, and I assume that if something "higher up" was poisoned (e.g. the Vector itself), ASAN would have complained higher up in the call stack.

I can't immediately tell if this is a "real" bug, or just an ASAN false positive; I notice that in Vector::reserve, there are some "ASAN acrobatics", with a mention of lingering shadow bytes. This may or may not be related, but either way this needs to be looked at by a memory / ASAN expert. Probably @mlippautz, or someone nearby.

```
--- a/third_party/blink/renderer/platform/wtf/atomic_operations.cc
+++ b/third_party/blink/renderer/platform/wtf/atomic_operations.cc
@@ -8,6 +8,7 @@
 #endif
 
 #include "third_party/blink/renderer/platform/wtf/atomic_operations.h"
+#include <sanitizer/asan_interface.h>
 
 namespace WTF {
 
@@ -46,6 +47,8 @@ void AtomicReadMemcpyImpl(void* to, const void* from, size_t bytes) {
 
 template <typename AlignmentType>
 void AtomicWriteMemcpyImpl(void* to, const void* from, size_t bytes) {
+  CHECK(!__asan_address_is_poisoned(to)) << "to is poisoned"; // <========= This check triggers.
+  CHECK(!__asan_address_is_poisoned(from)) << "from is poisoned";
   // Check alignment of |to| and |from|.
   DCHECK_EQ(0u, static_cast<AlignmentType>(reinterpret_cast<size_t>(to)) &
                     (sizeof(AlignmentType) - 1));
diff --git a/third_party/blink/renderer/platform/wtf/vector.h b/third_party/blink/renderer/platform/wtf/vector.h
index 9caeb874445a7..1a431472b4220 100644
--- a/third_party/blink/renderer/platform/wtf/vector.h
+++ b/third_party/blink/renderer/platform/wtf/vector.h

```

### pe...@google.com (2025-01-22)

The issue's primary component must be in the Component Tags, so re-adding it. To change the primary component, use the edit button at the top of the issue, just above the title.

### 0x...@gmail.com (2025-01-22)

There is another asan crash related to this issue:
=================================================================
==19804==ERROR: AddressSanitizer: use-after-poison on address 0x7eed210331a0 at pc 0x7ffb06cc41bb bp 0x00988d1f89c0 sp 0x00988d1f8a08
READ of size 8 at 0x7eed210331a0 thread T0
    #0 0x7ffb06cc41ba in scoped_refptr<blink::ParkableStringImpl>::operator bool C:\b\s\w\ir\cache\builder\src\base\memory\scoped_refptr.h:319
    #1 0x7ffb06cc41ba in blink::ParkableString::length C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\bindings\parkable_string.h:381
    #2 0x7ffb06cc41ba in blink::V8ScriptRunner::CompileAndRunScript(class blink::ScriptState *, class blink::ClassicScript *, enum blink::ExecuteScriptPolicy, class blink::V8ScriptRunner::RethrowErrorsOption) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\bindings\core\v8\v8_script_runner.cc:696:65
    #3 0x7ffb06c68725 in blink::ClassicScript::RunScriptOnScriptStateAndReturnValue(class blink::ScriptState *, enum blink::ExecuteScriptPolicy, class blink::V8ScriptRunner::RethrowErrorsOption) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\script\classic_script.cc:225:10
    #4 0x7ffb06c698a2 in blink::Script::RunScriptOnScriptState(class blink::ScriptState *, enum blink::ExecuteScriptPolicy, class blink::V8ScriptRunner::RethrowErrorsOption) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\script\script.cc:35:17
    #5 0x7ffb06c69c63 in blink::Script::RunScript(class blink::LocalDOMWindow *, enum blink::ExecuteScriptPolicy, class blink::V8ScriptRunner::RethrowErrorsOption) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\script\script.cc:42:3
    #6 0x7ffb0ee30f7a in blink::PendingScript::ExecuteScriptBlockInternal(class blink::Script *, class blink::ScriptElementBase *, bool, bool, bool, class base::TimeTicks, bool) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\script\pending_script.cc:293:13
    #7 0x7ffb0ee2fa87 in blink::PendingScript::ExecuteScriptBlock(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\script\pending_script.cc:190:3
    #8 0x7ffb0ac23724 in blink::ScriptLoader::PrepareScript(enum blink::ScriptLoader::ParserBlockingInlineOption, class WTF::TextPosition const &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\script\script_loader.cc:1246:60
    #9 0x7ffb0f1f7285 in blink::HTMLParserScriptRunner::ProcessScriptElementInternal(class blink::Element *, class WTF::TextPosition const &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\script\html_parser_script_runner.cc:494:52
    #10 0x7ffb0f1f6aaa in blink::HTMLParserScriptRunner::ProcessScriptElement(class blink::Element *, class WTF::TextPosition const &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\script\html_parser_script_runner.cc:288:3
    #11 0x7ffb0af1b7fb in blink::HTMLDocumentParser::RunScriptsForPausedTreeBuilder(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc:678:21
    #12 0x7ffb0af172c1 in blink::HTMLDocumentParser::CanTakeNextToken C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.h:193
    #13 0x7ffb0af172c1 in blink::HTMLDocumentParser::PumpTokenizer(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc:748:36
    #14 0x7ffb0af1569e in blink::HTMLDocumentParser::PumpTokenizerIfPossible(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc:640:15
    #15 0x7ffb0af16002 in blink::HTMLDocumentParser::DeferredPumpTokenizerIfPossible(bool, class base::TimeTicks) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc:623:7
    #16 0x7ffb0af353c5 in base::internal::DecayedFunctorTraits<void (blink::HTMLDocumentParser::*)(bool, base::TimeTicks),cppgc::internal::BasicPersistent<blink::HTMLDocumentParser,cppgc::internal::StrongPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy> &&,bool &&,base::TimeTicks &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:729
    #17 0x7ffb0af353c5 in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (blink::HTMLDocumentParser::*&&)(bool, base::TimeTicks),cppgc::internal::BasicPersistent<blink::HTMLDocumentParser,cppgc::internal::StrongPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy> &&,bool &&,base::TimeTicks &&>,void,0,1,2>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:921
    #18 0x7ffb0af353c5 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::HTMLDocumentParser::*&&)(bool, base::TimeTicks),cppgc::internal::BasicPersistent<blink::HTMLDocumentParser,cppgc::internal::StrongPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy> &&,bool &&,base::TimeTicks &&>,base::internal::BindState<1,1,0,void (blink::HTMLDocumentParser::*)(bool, base::TimeTicks),cppgc::internal::BasicPersistent<blink::HTMLDocumentParser,cppgc::internal::StrongPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy>,bool,base::TimeTicks>,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1058
    #19 0x7ffb0af353c5 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl blink::HTMLDocumentParser::*&&)(bool, class base::TimeTicks), class cppgc::internal::BasicPersistent<class blink::HTMLDocumentParser, struct cppgc::internal::StrongPersistentPolicy, class cppgc::internal::IgnoreLocationPolicy, class cppgc::internal::DisabledCheckingPolicy> &&, bool &&, class base::TimeTicks &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl blink::HTMLDocumentParser::*)(bool, class base::TimeTicks), class cppgc::internal::BasicPersistent<class blink::HTMLDocumentParser, struct cppgc::internal::StrongPersistentPolicy, class cppgc::internal::IgnoreLocationPolicy, class cppgc::internal::DisabledCheckingPolicy>, bool, class base::TimeTicks>, (void)>::RunOnce(class base::internal::BindStateBase *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:971:12
    #20 0x7ffafe62eb6c in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
    #21 0x7ffafe62eb6c in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:210:34
    #22 0x7ffb036ab5a4 in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h:106
    #23 0x7ffb036ab5a4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::LazyNow *) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:470:23
    #24 0x7ffb036aa2f9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:330:40
    #25 0x7ffb036edd82 in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:42:55
    #26 0x7ffb036ad292 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:643:12
    #27 0x7ffafe68eb1e in base::RunLoop::Run(class base::Location const &) C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134:14
    #28 0x7ffb026e0302 in content::RendererMain(struct content::MainFunctionParams) C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:351:16
    #29 0x7ffafc4287b1 in content::RunOtherNamedProcessTypeMain(class std::__Cr::basic_string<char, struct std::__Cr::char_traits<char>, class std::__Cr::allocator<char>> const &, struct content::MainFunctionParams, class content::ContentMainDelegate *) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:773:14
    #30 0x7ffafc42a9f0 in content::ContentMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1142:10
    #31 0x7ffafc41ecd5 in content::RunContentProcess(struct content::ContentMainParams, class content::ContentMainRunner *) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:348:36
    #32 0x7ffafc41f87d in content::ContentMain(struct content::ContentMainParams) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:361:10
    #33 0x7ffaed531681 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:222:12
    #34 0x7ff70dd545ed in MainDllLoader::Launch(struct HINSTANCE__*, class base::TimeTicks) C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:201:12
    #35 0x7ff70dd51fe4 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:352:20
    #36 0x7ff70e34607b in invoke_main D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:78
    #37 0x7ff70e34607b in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #38 0x7ffbcf53e8d6  (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #39 0x7ffbd049fbcb  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800dfbcb)

Address 0x7eed210331a0 is a wild pointer inside of access range of size 0x000000000008.
SUMMARY: AddressSanitizer: use-after-poison C:\b\s\w\ir\cache\builder\src\base\memory\scoped_refptr.h:319 in scoped_refptr<blink::ParkableStringImpl>::operator bool
Shadow bytes around the buggy address:
  0x7eed21032f00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7eed21032f80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7eed21033000: 00 00 00 00 00 00 00 00 00 00 00 f7 f7 f7 f7 f7
  0x7eed21033080: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7eed21033100: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
=>0x7eed21033180: f7 f7 f7 f7[f7]f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7eed21033200: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7eed21033280: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7eed21033300: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7eed21033380: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7eed21033400: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
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

==19804==ADDITIONAL INFO

==19804==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffb0af1a25e in blink::HTMLDocumentParser::SchedulePumpTokenizer(bool) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc:892:7
    #1 0x7ffafed8f25b in IPC::ChannelAssociatedGroupController::Accept(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\ipc\ipc_mojo_bootstrap.cc:1141:13


==19804==END OF ADDITIONAL INFO
==19804==ABORTING




### ml...@chromium.org (2025-01-24)

I looked at this closer today. I can somewhat reproduce it within a minute and catch in in rr. However, so far only in release builds which is harder to analyze.

So far, I think this may actually a legit GC issue in that the conservative stack scan doesn't find a `HeapVector` backing. Basically in `SelectorQuery` we keep the result vector [1] alive from stack while going very deep on the stack. The last GC before the crash seems to reclaim the backing.

I see both `to` and `from` being poisoned but focusing on `from` right now as that seems what's going wrong in the stack scan. The `from` part matches also ASAN which reports a poisoned READ. I also manually computed the shadow area of the poisoned address and see that the last GC did indeed poison it because it could not find any references to the backing. (This requires some manual hackery as ASAN doesn't expose helpers to get to the shadow mapping.)

In my repro the last GC finds ~13k valid references on stack which makes it really hard to see where we go wrong.

Using rr on the run without symbols, I could also time travel back and see that we try to expand a ~50k backing.

```
(rr) info registers
rax            0x0                 0
rbx            0xf6abe2cb415       16951131550741
rcx            0x0                 0
rdx            0xcef0              52976           <<<<<<< length
rsi            0x7b4516dcade0      135536666521056 <<<<<<< from
rdi            0x7b4516de0050      135536666607696 <<<<<<< to
rbp            0x7b55f35fad90      0x7b55f35fad90
rsp            0x7b55f35fad90      0x7b55f35fad90
r8             0x0                 0
r9             0x7fffffffff01      140737488355073
r10            0x7fffffffff01      140737488355073
r11            0x1                 1
r12            0x40ac              16556
r13            0x7b55f165a0a0      135609052405920
r14            0x7b55f165a0ac      135609052405932
r15            0x7b4516de0050      135536666607696
rip            0x559c64f53504      0x559c64f53504 <WTF::AtomicWriteMemcpy(void*, void const*, unsigned long)+4>
eflags         0x216               [ PF AF IF ]
cs             0x33                51
ss             0x2b                43
ds             0x0                 0
es             0x0                 0
fs             0x0                 0
gs             0x0                 0

```

Next up:

- Try to disable ASAN fake stack as it's just a mess to debug. Poisoning should not depend on it
- Locate the stack area where we don't seem to find the pointer.
- Check disasm for the surrounding code.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/selector_query.cc;l=141;drc=27d34700b83f381c62e3a348de2e6dfdc08364b8;bpv=1;bpt=1?q=blink::SelectorQuery::Execute&ss=chromium>

### ml...@chromium.org (2025-01-24)

Still triggers with `ASAN_OPTIONS=detect_stack_use_after_return=0` which should disable ASAN fake stacks. So I think this part can be ruled out.

<https://github.com/llvm-mirror/compiler-rt/blob/69445f095c22aac2388f939bedebf224a6efcdaf/lib/asan/asan_thread.cpp#L232C7-L232C50>

### ml...@chromium.org (2025-01-24)

I can confirm that by the time we crash we actually do still see the backing on the stack and I can read back the from pointer from the stack slot.

Unless there's something swapped in/out around the GC in Vector's internals, the pointer is at least there.

### ml...@chromium.org (2025-01-24)

Alright, stack scan seems to be working. Here's a log from the last GC to crashing.

```
Scanning stack: from 0x7b1c80ff21a0 to 0x7b1c81001000 (css slot: 0x7b1c80ff2a00)
+-> found vector slot (0x7b1c80ff2a00), contents: 0x7b0d03a40050
[2139248:0x7e2ca4ec1000]    59508 ms: Mark-Compact 0.8 (2.4) -> 0.8 (2.4) MB, pooled: 1 MB, 94.23 / 0.01 ms  (+ 896.9 ms in 0 steps since start of marking, biggest step 0.0 ms, walltime since start of marking 23110 ms) (average mu = 0.994, current mu = 0.996) external finalize; GC in old space requested
to poisoned: 0x7b0d03a60050
from poisoned: 0x7b0d03a40050
+-> Vector slot on stack: 0x7b1c80ff2a00
+-> contents of first word: 0x7b0d03a40050
<UAP crash>

```

### ml...@chromium.org (2025-01-24)

We find the slot in the stack scanner but somehow fail to mark it properly.

```
Scanning stack: from 0x7bf5dbff21a0 to 0x7bf5dc001000 (css slot: 0x7bf5dbff2a00)
+-> found vector slot (0x7bf5dbff2a00), contents: 0x7be52d4a0050, poisoned: 0
After PrepareForSweepVisitor:
+-> contents: 0x7be52d4a0050, poisoned: 1
[2158575:0x7f05ffed5000]    65110 ms: Mark-Compact 0.9 (2.4) -> 0.8 (2.4) MB, pooled: 1 MB, 108.89 / 0.01 ms  (+ 1037.1 ms in 0 steps since start of marking, biggest step 0.0 ms, walltime since start of marking 24916 ms) (average mu = 0.989, current mu = 0.996) external finalize; GC in old space requested
to poisoned: 0x7be52d4c0050
from poisoned: 0x7be52d4a0050
+-> Vector slot on stack: 0x7bf5dbff2a00
+-> contents of first word: 0x7be52d4a0050

```

### ml...@chromium.org (2025-01-24)

So, yeah, this is a GC bug that is a result of a feature contributed by externals (Msft) that is not correct in place that's tricky to see and a recent optimization that just assumes that this stuff works.

Details:

Since we added Oilpan pointer compression we didn't want to assume (or rather restrict) C++ compiler optimization. So, when scanning the stack, we assume that we can find full pointers, compressed pointers, intermediate representations of compression that the compiler may generate and keep around. E.g, we assume that there could be half-compressed half-words on the stack, so when we scan the stack we tear apart half-words and try to find objects to retain.

A recent optimization [1](https://chromium-review.googlesource.com/c/v8/v8/+/6164787) assumes this treatment works properly and removing handling full-words as well because they should be recovered from the parts. The logic we have in place works for anything <4G.

In [issue 343959927](https://issues.chromium.org/issues/343959927) Msft contributed code for 16G cages. Unfortunately, this part misses out on the handling of intermediate compressed values, which admitedly is hard to spot and understand.

Now, the problem is combining both: Not checkign for the full words works as long as we have cages <4G. Once the high water mark reaches >4G, the scanner will not find pointers anymore because the intermediate values not recovered properly. This happensi n the repro.

The interesting code is here [2](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/heap/cppgc/visitor.cc;l=91?q=ConservativeTracingVisitor&ss=chromium).

A quick fix for the repro is to revert the optimization.

That said, we still need to think through the impact of 16G cage on intermediate values here. E.g., whether clang would be able to tear apart a 34bit value across the stack. If we think this can happen in practice, then we need to check for 8 additional cases on the fast path (2 bits that we don't know = 4 values x 2 half-words). We can add a high water mark to make the checks fast for smaller heaps.

### ap...@google.com (2025-01-24)

Project: v8/v8  

Branch: main  

Author: Michael Lippautz <[mlippautz@chromium.org](mailto:mlippautz@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6198226>

Revert "[cppgc] Skip checking full addresses in CSS"

---


Expand for full commit details
```
Revert "[cppgc] Skip checking full addresses in CSS" 
 
This reverts commit d8675404884800e4bb3934826dcac5367dc550a8. 
 
Reason for revert: Not always correct, see bug. 
 
Bug: 391018461 
 
Original change's description: 
> [cppgc] Skip checking full addresses in CSS 
> 
> For each 64bit address found on the stack during CSS, we first try to 
> match the full 64bit address to an object, then treat each of the 32bit 
> halves of the address as a compressed pointer, decompress them and try 
> to match them to an object. 
> If the 64bit address points to within a cage, the decompressed lower 
> 32bit half of it would point to the same address, and we will be 
> handling the address twice. 
> 
> Optimize by skipping the full 64bit address in builds with pointer 
> compression enabled. 
> 
> Change-Id: I21f3e28550ed12b59a06c6d9db3024b32f770f9c 
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6164787 
> Commit-Queue: Michael Lippautz <mlippautz@chromium.org> 
> Auto-Submit: Omer Katz <omerkatz@chromium.org> 
> Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
> Commit-Queue: Omer Katz <omerkatz@chromium.org> 
> Cr-Commit-Position: refs/heads/main@{#98060} 
 
Change-Id: I34837b80b16f5d8eaf32ccf97d2b7e552c445ecd 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6198226 
Commit-Queue: Michael Lippautz <mlippautz@chromium.org> 
Reviewed-by: Igor Sheludko <ishell@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#98320}

```

---

Files:

- M `src/heap/cppgc/visitor.cc`

---

Hash: dc2bf8b84f69728863e5e679d4488e3e0fb40b6c  

Date:  Fri Jan 24 10:42:35 2025


---

### ap...@google.com (2025-01-28)

Project: v8/v8  

Branch: main  

Author: Michael Lippautz <[mlippautz@chromium.org](mailto:mlippautz@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6198347>

cppgc: Fix handling of intermediate values on the stack for 16G cages

---


Expand for full commit details
```
cppgc: Fix handling of intermediate values on the stack for 16G cages 
 
This fixes the handling of intermediate values when conservatively 
iterating memory (stack, but also heap). 
 
To this end we will scan through memory word-by-word and consider: 
1. Full pointers; 
2. Compressed pointers in both half words; 
3. A half-decompressed 35-bit value as intermediate state that doesn't 
   assume sign extension happened; 
 
We also bring back the optimization from https://crrev.com/c/6198226 
which relied on the fact that the full pointer will be reached through 
the intermediate state. This is now actually the case and handling 3. 
implicitly also handles 1. 
 
The CL also adds a bunch of tests that would have caught the original 
problem. 
 
Change-Id: Ibde3af33894b1f044cde49e97492b46c3e4b4e24 
Bug: 391018461 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6198347 
Commit-Queue: Michael Lippautz <mlippautz@chromium.org> 
Reviewed-by: Anton Bikineev <bikineev@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#98372}

```

---

Files:

- M `include/cppgc/internal/member-storage.h`
- M `src/base/sanitizer/msan.h`
- M `src/heap/cppgc-js/cpp-snapshot.cc`
- M `src/heap/cppgc/visitor.cc`
- M `src/heap/cppgc/visitor.h`
- M `test/unittests/heap/cppgc/member-unittest.cc`

---

Hash: 43479135b3021527907de520793c2515633abadb  

Date:  Tue Jan 28 16:38:15 2025


---

### sp...@google.com (2025-01-29)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
baseline report of memory corruption in a sandboxed process / the renderer 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-01-29)

Congratulations! Thank you for your efforts and reporting this issue to us.

### pe...@google.com (2025-02-05)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M134. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: a reverted commit was detected after the merge request.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [134].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ml...@chromium.org (2025-02-05)

Broken code landed in M134: <https://chromium-review.googlesource.com/c/v8/v8/+/6164787>
Fix landed in M134: <https://chromium-review.googlesource.com/6198226>

I don't think anything needs. to be backermged here.

### ch...@google.com (2025-05-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> baseline report of memory corruption in a sandboxed process / the renderer

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/391018461)*
