# Heap buffer overflow in Blink animation timing

| Field | Value |
|-------|-------|
| **Issue ID** | [493534964](https://issues.chromium.org/issues/493534964) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Animation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sh...@gmail.com |
| **Assignee** | fl...@google.com |
| **Created** | 2026-03-17 |
| **Bounty** | $2,000.00 |

## Description

# Security Bug

## VULNERABILITY DETAILS

This issue is a heap-buffer-overflow in Blink’s animation timing code, with the crashing callsite at blink::LinearTimingFunction::Range. A crafted page can feed malformed timing-function data into the animation / paint pipeline, causing Blink to compute or read past the valid bounds of the underlying linear easing point array during range evaluation. The most likely root cause is insufficient bounds validation when a linear() timing function is parsed and later consumed by animation or paint code, leaving an internal point list in a shape that Range() does not safely handle.

```
=================================================================
==102068==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7b932a480e08 at pc 0x7f134e33a239 bp 0x7ffc94b1e640 sp 0x7ffc94b1e638
READ of size 8 at 0x7b932a480e08 thread T0 (chrome)
    #0 0x7f134e33a238 in blink::LinearTimingFunction::Range(double*, double*) const third_party/blink/renderer/platform/animation/timing_function.cc:72:51
    #1 0x7f134085ef1f in blink::ClipPathPaintDefinition::GetAnimationBoundingRect(blink::LayoutObject const&) third_party/blink/renderer/modules/csspaint/nativepaint/clip_path_paint_definition.cc:705:12
    #2 0x7f13590ae707 in blink::PaintPropertyTreeBuilder::UpdateForSelf() third_party/blink/renderer/core/paint/paint_property_tree_builder.cc:2468:39
    #3 0x7f13590e2411 in blink::PrePaintTreeWalk::WalkInternal(blink::LayoutObject const&, blink::PrePaintTreeWalk::PrePaintTreeWalkContext&, blink::PrePaintInfo*) third_party/blink/renderer/core/paint/pre_paint_tree_walk.cc:632:28
    #4 0x7f13590debd9 in blink::PrePaintTreeWalk::Walk(blink::LayoutObject const&, blink::PrePaintTreeWalk::PrePaintTreeWalkContext const&, blink::PrePaintInfo*) third_party/blink/renderer/core/paint/pre_paint_tree_walk.cc:1406:3
    #5 0x7f13590e9ce4 in blink::PrePaintTreeWalk::WalkLayoutObjectChildren(blink::LayoutObject const&, blink::PhysicalBoxFragment const*, blink::PrePaintTreeWalk::PrePaintTreeWalkContext const&) third_party/blink/renderer/core/paint/pre_paint_tree_walk.cc:1068:7
    #6 0x7f13590e9461 in blink::PrePaintTreeWalk::WalkChildren(blink::LayoutObject const&, blink::PhysicalBoxFragment const*, blink::PrePaintTreeWalk::PrePaintTreeWalkContext&, bool) third_party/blink/renderer/core/paint/pre_paint_tree_walk.cc:1356:5
    #7 0x7f13590decd2 in blink::PrePaintTreeWalk::Walk(blink::LayoutObject const&, blink::PrePaintTreeWalk::PrePaintTreeWalkContext const&, blink::PrePaintInfo*) third_party/blink/renderer/core/paint/pre_paint_tree_walk.cc:1429:5
    #8 0x7f13590e9ce4 in blink::PrePaintTreeWalk::WalkLayoutObjectChildren(blink::LayoutObject const&, blink::PhysicalBoxFragment const*, blink::PrePaintTreeWalk::PrePaintTreeWalkContext const&) third_party/blink/renderer/core/paint/pre_paint_tree_walk.cc:1068:7
    #9 0x7f13590decd2 in blink::PrePaintTreeWalk::Walk(blink::LayoutObject const&, blink::PrePaintTreeWalk::PrePaintTreeWalkContext const&, blink::PrePaintInfo*) third_party/blink/renderer/core/paint/pre_paint_tree_walk.cc:1429:5
    #10 0x7f13590e9ce4 in blink::PrePaintTreeWalk::WalkLayoutObjectChildren(blink::LayoutObject const&, blink::PhysicalBoxFragment const*, blink::PrePaintTreeWalk::PrePaintTreeWalkContext const&) third_party/blink/renderer/core/paint/pre_paint_tree_walk.cc:1068:7
    #11 0x7f13590decd2 in blink::PrePaintTreeWalk::Walk(blink::LayoutObject const&, blink::PrePaintTreeWalk::PrePaintTreeWalkContext const&, blink::PrePaintInfo*) third_party/blink/renderer/core/paint/pre_paint_tree_walk.cc:1429:5
    #12 0x7f13590e9ce4 in blink::PrePaintTreeWalk::WalkLayoutObjectChildren(blink::LayoutObject const&, blink::PhysicalBoxFragment const*, blink::PrePaintTreeWalk::PrePaintTreeWalkContext const&) third_party/blink/renderer/core/paint/pre_paint_tree_walk.cc:1068:7
    #13 0x7f13590e9461 in blink::PrePaintTreeWalk::WalkChildren(blink::LayoutObject const&, blink::PhysicalBoxFragment const*, blink::PrePaintTreeWalk::PrePaintTreeWalkContext&, bool) third_party/blink/renderer/core/paint/pre_paint_tree_walk.cc:1356:5
    #14 0x7f13590decd2 in blink::PrePaintTreeWalk::Walk(blink::LayoutObject const&, blink::PrePaintTreeWalk::PrePaintTreeWalkContext const&, blink::PrePaintInfo*) third_party/blink/renderer/core/paint/pre_paint_tree_walk.cc:1429:5
    #15 0x7f13590de1b0 in blink::PrePaintTreeWalk::Walk(blink::LocalFrameView&, blink::PrePaintTreeWalk::PrePaintTreeWalkContext const&) third_party/blink/renderer/core/paint/pre_paint_tree_walk.cc:169:5
    #16 0x7f13590ddbce in blink::PrePaintTreeWalk::WalkTree(blink::LocalFrameView&) third_party/blink/renderer/core/paint/pre_paint_tree_walk.cc:90:3
    #17 0x7f13573ad59f in blink::LocalFrameView::RunPrePaintLifecyclePhase(blink::DocumentLifecycle::LifecycleState) third_party/blink/renderer/core/frame/local_frame_view.cc:2824:24
    #18 0x7f13573ab79c in blink::LocalFrameView::UpdateLifecyclePhasesInternal(blink::DocumentLifecycle::LifecycleState) third_party/blink/renderer/core/frame/local_frame_view.cc:2453:35
    #19 0x7f13573a797f in blink::LocalFrameView::UpdateLifecyclePhases(blink::DocumentLifecycle::LifecycleState, blink::DocumentUpdateReason) third_party/blink/renderer/core/frame/local_frame_view.cc:2315:3
    #20 0x7f13573a71da in blink::LocalFrameView::UpdateAllLifecyclePhases(blink::DocumentUpdateReason) third_party/blink/renderer/core/frame/local_frame_view.cc:2030:54
    #21 0x7f1358e591d7 in blink::PageAnimator::UpdateAllLifecyclePhases(blink::LocalFrame&, blink::DocumentUpdateReason) third_party/blink/renderer/core/page/page_animator.cc:394:9
    #22 0x7f13575188d3 in blink::WebFrameWidgetImpl::UpdateLifecycle(blink::WebLifecycleUpdate, blink::DocumentUpdateReason) third_party/blink/renderer/core/frame/web_frame_widget_impl.cc:1697:14
    #23 0x7f134edb5d25 in non-virtual thunk to blink::WidgetBase::UpdateVisualState() third_party/blink/renderer/platform/widget/widget_base.cc:1055:12
    #24 0x7f139693cec6 in cc::LayerTreeHost::RequestMainFrameUpdate(bool) cc/trees/layer_tree_host.cc:411:12
    #25 0x7f1396a9688a in cc::ProxyMain::BeginMainFrame(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState>>) cc/trees/proxy_main.cc:337:21
    #26 0x7f1396a8d992 in base::internal::Invoker<base::internal::FunctorTraits<void (cc::ProxyMain::*&&)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState>>), base::WeakPtr<cc::ProxyMain>&&, std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState>>&&>, base::internal::BindState<true, true, false, void (cc::ProxyMain::*)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState>>), base::WeakPtr<cc::ProxyMain>, std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState>>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #27 0x7f13a8c86ed2 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #28 0x7f13a8d083ce in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #29 0x7f13a8d073a6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #30 0x7f13a8b28ea1 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #31 0x7f13a8d09a48 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #32 0x7f13a8bf1512 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #33 0x7f139e8d0bfe in content::RendererMain(content::MainFunctionParams) content/renderer/renderer_main.cc:364:16
    #34 0x7f139ed030b7 in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:664:14
    #35 0x7f139ed0421f in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:771:12
    #36 0x7f139ed0680a in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1152:10
    #37 0x7f139ed00f53 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:358:36
    #38 0x7f139ed012ea in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:371:10
    #39 0x55d9e4b27345 in ChromeMain chrome/app/chrome_main.cc:191:12
    #40 0x7f1338fa2d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

0x7b932a480e08 is located 8 bytes after 96-byte region [0x7b932a480da0,0x7b932a480e00)
allocated by thread T0 (chrome) here:
    #0 0x55d9e4b258fd in operator new(unsigned long) (/mnt/lvm_data/chromium/src/out/asan_nodcheck/chrome+0x686e8fd) (BuildId: f667536c8ff65a4b)
    #1 0x7f13566121de in void std::__Cr::vector<gfx::LinearEasingPoint, std::__Cr::allocator<gfx::LinearEasingPoint>>::__init_with_size<blink::UncheckedIterator<gfx::LinearEasingPoint>, blink::UncheckedIterator<gfx::LinearEasingPoint>>(blink::UncheckedIterator<gfx::LinearEasingPoint>, blink::UncheckedIterator<gfx::LinearEasingPoint>, unsigned long) gen/third_party/libc++/src/include/__new/allocate.h:43:28
    #2 0x7f135660a9b3 in blink::CSSToStyleMap::MapAnimationTimingFunction(blink::CSSLengthResolver const&, blink::CSSValue const&) gen/third_party/libc++/src/include/__vector/vector.h:211:5
    #3 0x7f135ab3304c in blink::AnimationInputHelpers::ParseTimingFunction(blink::String const&, blink::Document*, blink::ExceptionState&) third_party/blink/renderer/core/animation/animation_input_helpers.cc:97:10
    #4 0x7f135ad4d453 in blink::EffectInput::ParseKeyframesArgument(blink::Element*, blink::ScriptValue const&, blink::ScriptState*, blink::ExceptionState&) third_party/blink/renderer/core/animation/effect_input.cc:510:9
    #5 0x7f135ad4a848 in blink::EffectInput::Convert(blink::Element*, blink::ScriptValue const&, blink::EffectModel::CompositeOperation, blink::ScriptState*, blink::ExceptionState&) third_party/blink/renderer/core/animation/effect_input.cc:787:7
    #6 0x7f135ade2efb in blink::KeyframeEffect::Create(blink::ScriptState*, blink::Element*, blink::ScriptValue const&, blink::V8UnionKeyframeEffectOptionsOrUnrestrictedDouble const*, blink::ExceptionState&) third_party/blink/renderer/core/animation/keyframe_effect.cc:208:36
    #7 0x7f1359ccadd8 in blink::Element::animate(blink::ScriptState*, blink::ScriptValue const&, blink::V8UnionKeyframeAnimationOptionsOrUnrestrictedDouble const*, blink::ExceptionState&) third_party/blink/renderer/core/dom/element.cc:680:7
    #8 0x7f135a6ace90 in blink::(anonymous namespace)::v8_element::AnimateOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&) gen/third_party/blink/renderer/bindings/core/v8/v8_element.cc:3235:32
    #9 0x7b12fc6506a3  (<unknown module>)
    #10 0x7b12fc64e83b  (<unknown module>)
    #11 0x7b12fc64e83b  (<unknown module>)
    #12 0x7b12fc64e83b  (<unknown module>)
    #13 0x7b12fc64e83b  (<unknown module>)
    #14 0x7b12fc64b5db  (<unknown module>)
    #15 0x7b12fc64b32a  (<unknown module>)
    #16 0x7f13475e2711 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/simulator.h:216:12
    #17 0x7f13475e005e in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>, v8::base::Vector<v8::internal::DirectHandle<v8::internal::Object> const>) v8/src/execution/execution.cc:564:10
    #18 0x7f13474eec2a in v8::debug::CallFunctionOn(v8::Local<v8::Context>, v8::Local<v8::Function>, v8::Local<v8::Value>, v8::base::Vector<v8::Local<v8::Value>>, bool) v8/src/debug/debug-interface.cc:1251:7
    #19 0x7f1349c9a4ca in v8_inspector::(anonymous namespace)::innerCallFunctionOn(v8_inspector::V8InspectorSessionImpl*, v8_inspector::InjectedScript::Scope&, v8::Local<v8::Value>, v8_inspector::String16 const&, std::__Cr::unique_ptr<std::__Cr::vector<std::__Cr::unique_ptr<v8_inspector::protocol::Runtime::CallArgument, std::__Cr::default_delete<v8_inspector::protocol::Runtime::CallArgument>>, std::__Cr::allocator<std::__Cr::unique_ptr<v8_inspector::protocol::Runtime::CallArgument, std::__Cr::default_delete<v8_inspector::protocol::Runtime::CallArgument>>>>, std::__Cr::default_delete<std::__Cr::vector<std::__Cr::unique_ptr<v8_inspector::protocol::Runtime::CallArgument, std::__Cr::default_delete<v8_inspector::protocol::Runtime::CallArgument>>, std::__Cr::allocator<std::__Cr::unique_ptr<v8_inspector::protocol::Runtime::CallArgument, std::__Cr::default_delete<v8_inspector::protocol::Runtime::CallArgument>>>>>>, bool, std::__Cr::unique_ptr<v8_inspector::WrapOptions, std::__Cr::default_delete<v8_inspector::WrapOptions>>, bool, bool, v8_inspector::String16 const&, bool, std::__Cr::unique_ptr<v8_inspector::protocol::Runtime::Backend::CallFunctionOnCallback, std::__Cr::default_delete<v8_inspector::protocol::Runtime::Backend::CallFunctionOnCallback>>) v8/src/inspector/v8-runtime-agent-impl.cc:190:24
    #20 0x7f1349c991cf in v8_inspector::V8RuntimeAgentImpl::callFunctionOn(v8_inspector::String16 const&, std::__Cr::optional<v8_inspector::String16>, std::__Cr::unique_ptr<std::__Cr::vector<std::__Cr::unique_ptr<v8_inspector::protocol::Runtime::CallArgument, std::__Cr::default_delete<v8_inspector::protocol::Runtime::CallArgument>>, std::__Cr::allocator<std::__Cr::unique_ptr<v8_inspector::protocol::Runtime::CallArgument, std::__Cr::default_delete<v8_inspector::protocol::Runtime::CallArgument>>>>, std::__Cr::default_delete<std::__Cr::vector<std::__Cr::unique_ptr<v8_inspector::protocol::Runtime::CallArgument, std::__Cr::default_delete<v8_inspector::protocol::Runtime::CallArgument>>, std::__Cr::allocator<std::__Cr::unique_ptr<v8_inspector::protocol::Runtime::CallArgument, std::__Cr::default_delete<v8_inspector::protocol::Runtime::CallArgument>>>>>>, std::__Cr::optional<bool>, std::__Cr::optional<bool>, std::__Cr::optional<bool>, std::__Cr::optional<bool>, std::__Cr::optional<bool>, std::__Cr::optional<int>, std::__Cr::optional<v8_inspector::String16>, std::__Cr::optional<bool>, std::__Cr::optional<v8_inspector::String16>, std::__Cr::unique_ptr<v8_inspector::protocol::Runtime::SerializationOptions, std::__Cr::default_delete<v8_inspector::protocol::Runtime::SerializationOptions>>, std::__Cr::unique_ptr<v8_inspector::protocol::Runtime::Backend::CallFunctionOnCallback, std::__Cr::default_delete<v8_inspector::protocol::Runtime::Backend::CallFunctionOnCallback>>) v8/src/inspector/v8-runtime-agent-impl.cc:530:5
    #21 0x7f1349b93789 in v8_inspector::protocol::Runtime::DomainDispatcherImpl::callFunctionOn(v8_crdtp::Dispatchable const&) gen/v8/src/inspector/protocol/Runtime.cpp:837:16
    #22 0x7f1349ce68b3 in v8_crdtp::UberDispatcher::DispatchResult::Run() gen/third_party/libc++/src/include/__functional/function.h:502:12
    #23 0x7f1349c84ac2 in v8_inspector::V8InspectorSessionImpl::dispatchProtocolMessage(v8_inspector::StringView) v8/src/inspector/v8-inspector-session-impl.cc:388:39
    #24 0x7f1357cdcfe2 in blink::DevToolsSession::DispatchProtocolCommandImpl(int, blink::String const&, base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>) third_party/blink/renderer/core/inspector/devtools_session.cc:272:18
    #25 0x7f1357cdd65f in non-virtual thunk to blink::DevToolsSession::DispatchProtocolCommand(int, blink::String const&, base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>) third_party/blink/renderer/core/inspector/devtools_session.cc:243:10
    #26 0x7f13501c9b61 in blink::mojom::blink::DevToolsSessionStubDispatch::Accept(blink::mojom::blink::DevToolsSession*, mojo::Message*) gen/third_party/blink/public/mojom/devtools/devtools_agent.mojom-blink.cc:1542:13
    #27 0x7f13a942f3e2 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1085:54
    #28 0x7f13a944678b in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:44:19
    #29 0x7f13a9434c94 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:747:20

SUMMARY: AddressSanitizer: heap-buffer-overflow third_party/blink/renderer/platform/animation/timing_function.cc:72:51 in blink::LinearTimingFunction::Range(double*, double*) const
Shadow bytes around the buggy address:
  0x7b932a480b80: fa fa f7 fa 00 00 00 00 00 00 00 00 00 00 00 fa
  0x7b932a480c00: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x7b932a480c80: fa fa f7 fa 00 00 00 00 00 00 00 00 00 00 00 00
  0x7b932a480d00: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x7b932a480d80: fa fa f7 fa 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7b932a480e00: fa[fa]f7 fa 00 00 00 00 00 00 00 00 00 00 fc fc
  0x7b932a480e80: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x7b932a480f00: fa fa f7 fa 00 00 00 00 00 00 00 00 00 00 00 fa
  0x7b932a480f80: fa fa f7 fa 00 00 00 00 00 00 00 00 00 00 00 03
  0x7b932a481000: fa fa f7 fa 00 00 00 00 00 00 00 00 00 00 fc fc
  0x7b932a481080: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
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

==102068==ADDITIONAL INFO

==102068==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7f1396a83193 in cc::ProxyImpl::ScheduledActionSendBeginMainFrame(viz::BeginFrameArgs const&) cc/trees/proxy_impl.cc:780:7


Command line: `/proc/self/exe --type=renderer --crashpad-handler-pid=102010 --enable-crash-reporter=, --noerrdialogs --user-data-dir=/mnt/lvm_data/chromium/a98/profiles/chrome_profile_7qyc2eee --change-stack-guard-on-fork=enable --no-sandbox --remote-debugging-port=37679 --ozone-platform=headless --disable-gpu-compositing --lang=en-US --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=5 --time-ticks-at-unix-epoch=-1772947841576980 --launch-time-ticks=603989475063 --shared-files=v8_context_snapshot_data:100 --field-trial-handle=3,i,7138623061569844128,7663592372563810646,262144 --enable-features=PaintHolding --variations-seed-version --pseudonymization-salt-handle=7,i,10853764944089851745,11327994552876179331,4 --trace-process-track-uuid=3190708990997080739`


==102068==END OF ADDITIONAL INFO

==102068==ABORTING
[101991:101991:0315/051905.626181:ERROR:content/common/zygote/zygote_communication_linux.cc:291] Failed to send GetTerminationStatus message to zygote


```
## VERSION

Chrome Version: Chromium 147.0.7703.0 and Chromium 148.0.7729.0 dev ASAN builds  

Operating System: Linux x86\_64 on the two provided repro hosts (Ubuntu 22.04.3 LTS class and Ubuntu 25.04 class)

## REPRODUCTION CASE

HTML artifact: `poc_min.html` (single-file PoC)

Open `poc_min.html` directly in Chrome.

## FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: Renderer process crash
Crash State: `blink::LinearTimingFunction::Range`
ASAN type: heap-buffer-overflow

## CREDIT INFORMATION

Reporter credit: heapracer

## Attachments

- [poc_min.html](attachments/poc_min.html) (text/html, 6.3 KB)
- [Screenshot 2026-03-18 at 3.44.51 PM.png](attachments/Screenshot 2026-03-18 at 3.44.51 PM.png) (image/png, 1.7 MB)

## Timeline

### ts...@google.com (2026-03-17)

I didn't actually see the PoC, please attach presently or we can not accept the report.

### sh...@gmail.com (2026-03-17)

sorry here is the poc

### cl...@appspot.gserviceaccount.com (2026-03-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4659794770165760.

### sh...@gmail.com (2026-03-18)

not sure why clusterfuzz fails to reproduce - i can reproduce this on multiple builds from M145 to M146.

### 24...@project.gserviceaccount.com (2026-03-19)

Testcase 4659794770165760 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=4659794770165760.

### es...@chromium.org (2026-03-20)

I was able to reproduce locally at an asan build of r1597448, checking earlier milestones now.

### ch...@google.com (2026-03-20)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-20)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### fl...@google.com (2026-04-09)

deleted

### dx...@google.com (2026-04-27)

Project: chromium/src  

Branch:  main  

Author:  Robert Flack [flackr@chromium.org](mailto:flackr@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7792295>

Fix division by zero in clip path paint definition

---


Expand for full commit details
```
     
    Two keyframes can have the same offset. When that happens, there's 
    no need to interpolate between them. 
     
    Bug: 493534964 
    Change-Id: I6f57a4049c4651c8a2c44cf88509d59569e666d6 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7792295 
    Reviewed-by: Kevin Ellis <kevers@chromium.org> 
    Commit-Queue: Robert Flack <flackr@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1621327}

```

---

Files:

- M `third_party/blink/renderer/modules/csspaint/nativepaint/clip_path_paint_definition.cc`
- A `third_party/blink/web_tests/external/wpt/css/css-easing/linear-timing-functions-duplicate-points-crash.html`

---

Hash: [bcd65a3e56f37cfddd5718aba5fabb96c5e5fbb5](https://chromiumdash.appspot.com/commit/bcd65a3e56f37cfddd5718aba5fabb96c5e5fbb5)  

Date: Mon Apr 27 21:36:10 2026


---

### aj...@google.com (2026-05-13)

-> Medium as this looks like a renderer READ only.

### sp...@google.com (2026-05-14)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline - User information disclosure


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-08-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2026-08-05)

This Blink bug has been marked as either a release blocker or a vulnerability bug. Blink bugs affect all OSs supported by Chrome (except iOS), so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/493534964)*
