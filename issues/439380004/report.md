# V8 Sandbox Bypass: In-sandbox corruption allows execution of arbitrary runtime functions / intrinsics

| Field | Value |
|-------|-------|
| **Issue ID** | [439380004](https://issues.chromium.org/issues/439380004) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Sandbox |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | is...@chromium.org |
| **Created** | 2025-08-17 |
| **Bounty** | $20,000.00 |

## Description

### VULNERABILITY DETAILS

#### README

**This bug report is yet another meta-report on a class of V8 sandbox bypasses**. I will not be filing bugs for every single discovered bypasses of these types (i.e. each and every exploitable runtime functions / intrinsics or ways to execute arbitrary extension code) as it just adds noise, but if you want to see more of these let me know.

#### Summary

An attacker may exploit in-sandbox corruption primitives to unlock arbitrary runtime functions and intrinsics, i.e. everything reachable with `--allow-natives-syntax`. By exploiting these code paths, an attacker may easily discover and exploit V8 sandbox violations in such code.

---

This is yet another issue orthogonal to [b/435630464](https://issues.chromium.org/issues/435630464) - this bug allows execution of arbitrary runtime functions and intrinsics, while the [b/435630464](https://issues.chromium.org/issues/435630464) allows execution of arbitrary JS-compatible builtins. However, it shares the same underlying principle. The repeated issue we were seeing and was mostly concerned about was:

1. The V8 Sandbox mostly focuses on what happens in code executing *within* sandbox context, but all bets are off for codes executing *outside* of it. We have generic sandbox "idioms" like EPT and mitigations with `SBXCHECK`s, but this turned out to be a whac-a-mole situation with spot mitigations.

The last several reports of mine also shows that:

2. The construction of V8 Sandbox only considers satisfying several high-level security properties that do not concern semantic correctness. This "semantic correctness" problem often leaks into the security domain in various ways as the high-level security property is unsound - executing some type-compatible debugging / experimental function not meant to execute in this context, confusing trustedness between the boundaries of V8 and its embedder, and so on. Introducing the embedder reveals even bigger issues that is increasingly difficult to reason about in V8.

---

#### Details

[b/435630464](https://issues.chromium.org/issues/435630464) describes a problem where in-sandbox corruption allows attackers to execute arbitrary JS-compatible builtins. This report fills in another gap where in-sandbox corruption may allow attackers to execute arbitrary runtime functions / intrinsics.

Intrinsics are allowed in context where either 1. `--allow-natives-syntax` v8 flag is on, or 2. the AST parser is currently parsing a V8 extension:

```
// https://source.chromium.org/chromium/chromium/src/+/main:v8/src/parsing/parser-base.h;drc=5d26c73d287ec98a3c1f9474955367317851f8d9;l=2277
ParserBase<Impl>::ParsePrimaryExpression() {
  // ...
  switch (token) {
    // ...
    case Token::kMod:
      if (flags().allow_natives_syntax() || impl()->ParsingExtension()) {
        return ParseV8Intrinsic();
      }
      break;

    default:
      break;
  }
  // ...
}

```

V8 extensions may be supplied and be enabled by the embedder. As an example, `chrome.{loadTimes,csi}` is injected by the embedder to provide [load time related features](https://source.chromium.org/chromium/chromium/src/+/main:chrome/renderer/loadtimes_extension_bindings.cc).

Extensions are loaded for all new window context, which means that a root window will have its own extension instantiated within its scope as well as any other frames later initialized. Since same-origin frames share the same process and the isolate, an attacker may already have acquired control over the sandbox memory before a new frame and its extensions are instantiated. A new context is instantiated with extensions to load in `LocalWindowProxy::CreateContext()`:

```
// https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/bindings/core/v8/local_window_proxy.cc;drc=eeb0929b5898a67e4342b0dd090cf77c836fa93e;l=234
void LocalWindowProxy::CreateContext() {
  // ...
  v8::ExtensionConfiguration extension_configuration =
      ScriptController::ExtensionsFor(GetFrame()->DomWindow());                 // [!] load all Blink-registered extensions

  DCHECK(GetFrame()->DomWindow());
  v8::Local<v8::Context> context;
  {
    v8::Isolate* isolate = GetIsolate();
    V8PerIsolateData::UseCounterDisabledScope use_counter_disabled(
        V8PerIsolateData::From(isolate));
    Document* document = GetFrame()->GetDocument();

    v8::Local<v8::Object> global_proxy = global_proxy_.Get(isolate);
    context = V8ContextSnapshot::CreateContextFromSnapshot(
        isolate, World(), &extension_configuration, global_proxy, document);    // [!] request extension loading to V8
    context_was_created_from_snapshot_ = !context.IsEmpty();

    // Even if we enable V8 context snapshot feature, we may hit this branch
    // in some cases, e.g. loading XML files.
    if (context.IsEmpty()) {
      v8::Local<v8::ObjectTemplate> global_template =
          V8Window::GetWrapperTypeInfo()
              ->GetV8ClassTemplate(isolate, World())
              .As<v8::FunctionTemplate>()
              ->InstanceTemplate();
      CHECK(!global_template.IsEmpty());
      context = v8::Context::New(isolate, &extension_configuration,             // [!] request extension loading to V8
                                 global_template, global_proxy,
                                 v8::DeserializeInternalFieldsCallback(),
                                 GetFrame()->DomWindow()->GetMicrotaskQueue());
      VLOG(1) << "A context is created NOT from snapshot";
    }
  }
  // ...
}

// https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/bindings/core/v8/script_controller.cc;drc=26004e20898f2a99531301ddaa1b54d0a7ce027c;l=221
v8::ExtensionConfiguration ScriptController::ExtensionsFor(
    const ExecutionContext* context) {
  if (context->ShouldInstallV8Extensions()) {                                   // [!] true for non-empty windows
    return v8::ExtensionConfiguration(RegisteredExtensionNames().size(),        // [!] get names of all registered extensions in Blink
                                      RegisteredExtensionNames().data());
  }
  return v8::ExtensionConfiguration();
}

```

The two extensions that are unconditionally loaded in Blink is [`extensions::SafeBuiltins`](https://source.chromium.org/chromium/chromium/src/+/main:extensions/renderer/dispatcher.cc;drc=68858dacd9a2a79c9504d8310e7aa223aff45d40;l=472) and [`v8/LoadTimes`](https://source.chromium.org/chromium/chromium/src/+/main:chrome/renderer/chrome_content_renderer_client.cc;drc=7ce73baa09400dc405a9cf925bbce1908457387e;l=450).

V8 attempts to install and compile the two extensions as requested by the embedder Blink. The compilation is done in `Genesis::CompileExtension()`:

```
// https://source.chromium.org/chromium/chromium/src/+/main:v8/src/init/bootstrapper.cc;drc=75836b4e5f0cacab5cf2024ebbe33234caee56cb;l=5124
bool Genesis::CompileExtension(Isolate* isolate, v8::Extension* extension) {
  Factory* factory = isolate->factory();
  HandleScope scope(isolate);
  DirectHandle<SharedFunctionInfo> function_info;

  Handle<String> source =
      isolate->factory()
          ->NewExternalStringFromOneByte(extension->source())                   // [!] create in-sandbox String object
          .ToHandleChecked();
  DCHECK(source->IsOneByteRepresentation());

  // If we can't find the function in the cache, we compile a new
  // function and insert it into the cache.
  base::Vector<const char> name = base::CStrVector(extension->name());
  SourceCodeCache* cache = isolate->bootstrapper()->extensions_cache();
  DirectHandle<Context> context(isolate->context(), isolate);
  DCHECK(IsNativeContext(*context));

  if (!cache->Lookup(isolate, name, &function_info)) {                          // [!] check in-sandbox cache for extensions already compiled previously
    Handle<String> script_name =
        factory->NewStringFromUtf8(name).ToHandleChecked();
    ScriptCompiler::CompilationDetails compilation_details;
    MaybeDirectHandle<SharedFunctionInfo> maybe_function_info =
        Compiler::GetSharedFunctionInfoForScriptWithExtension(                  // [!] TARGET: compile new extension with in-sandbox String `source`
            isolate, source, ScriptDetails(script_name), extension,
            ScriptCompiler::kNoCompileOptions, EXTENSION_CODE,
            &compilation_details);
    if (!maybe_function_info.ToHandle(&function_info)) return false;
    cache->Add(isolate, name, function_info);
  }
  // [!] ...create function and execute it
}

// https://source.chromium.org/chromium/chromium/src/+/main:v8/src/init/bootstrapper.h;drc=26004e20898f2a99531301ddaa1b54d0a7ce027c;l=41
class SourceCodeCache final {
 public:
  // ...
  bool Lookup(Isolate* isolate, base::Vector<const char> name,
              DirectHandle<SharedFunctionInfo>* handle);

  void Add(Isolate* isolate, base::Vector<const char> name,
           DirectHandle<SharedFunctionInfo> shared);

 private:
  Script::Type type_;
  Tagged<FixedArray> cache_;                                                    // [!] corruptable in-sandbox cache
};

// https://source.chromium.org/chromium/chromium/src/+/main:v8/src/init/bootstrapper.cc;drc=26004e20898f2a99531301ddaa1b54d0a7ce027c;l=107
bool SourceCodeCache::Lookup(Isolate* isolate, base::Vector<const char> name,
                             DirectHandle<SharedFunctionInfo>* handle) {
  for (int i = 0; i < cache_->length(); i += 2) {
    Tagged<SeqOneByteString> str = Cast<SeqOneByteString>(cache_->get(i));      // [!] cache bypassable by corrupting key string in cache_ FixedArray
    if (str->IsOneByteEqualTo(name)) {                                          // [!] DELAY POINT
      *handle =
          direct_handle(Cast<SharedFunctionInfo>(cache_->get(i + 1)), isolate);
      return true;
    }
  }
  return false;
}

```

Note how the function creates an in-sandbox string object `source` representing an external string based on the supplied extension source code, checks the in-sandbox `cache_` for any precompiled matches, and then use the `source` string for compilation. This gives us a race window to corrupt `source` into an attacker-controlled string, which will provide the primitive to compile arbitrary extension code and use intrinsics within it. This can of course also be used to hoist intrinsic-calling functions as "polyfilled intrinsics" into the global state so that the newly created frame can easily access it through its globals.

Again, there is an obvious race window but:

1. Racy exploits are no good
2. Triggering the bug involves creating a new (i)frame, which causes significant heap noise

Thus, we would ideally want a primitive to halt execution of the newly created iframe (running on main thread) after creation of `source` String object within the sandbox but before using it to compile an extension function, while a worker thread does its wonders and resumes the execution with a forged string. This point is marked as `DELAY POINT`.

A forged `SlicedString` or a `ThinString` referencing itself can be set as the key to compare. This will result in an infinite loop as V8 attempts to follow the chain and find the underlying string to compare with the embedder-supplied extension name:

```
// https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/string-inl.h;drc=26004e20898f2a99531301ddaa1b54d0a7ce027c;l=728
template <String::EqualityType kEqType, typename Char>
bool String::IsEqualToImpl(
    base::Vector<const Char> str,
    const SharedStringAccessGuardIfNeeded& access_guard) const {
  size_t len = str.size();
  switch (kEqType) {
    case EqualityType::kWholeString:
      if (static_cast<size_t>(length()) != len) return false;                   // [!] make the length match
      break;
    // ...
  }

  DisallowGarbageCollection no_gc;

  int slice_offset = 0;
  Tagged<String> string = this;
  const Char* data = str.data();
  while (true) {
    auto ret = string->DispatchToSpecificType(absl::Overload{
        // ...
        [&](Tagged<SlicedString> s) {
          slice_offset += s->offset();
          string = s->parent();                                                 // [!] cyclic reference causes infloop
          return std::nullopt;
        },
        [&](Tagged<ConsString> s) {
          // ...
        },
        [&](Tagged<ThinString> s) {
          string = s->actual();                                                 // [!] cyclic reference causes infloop
          return std::nullopt;
        }});
    if (ret) return ret.value();
  }
}

```

Now reaching `TARGET` is just a matter of:

1. Egghunting for values in the main frame
2. Searching & corrupting values as necessary (set cyclic string key, ...)
3. Spawning a concurrent Worker thread that searches newly created `source` and overwrites it, then unlocks the cyclic reference
4. Creating a new iframe to instantiate a new context & Blink extensions
5. Waiting for the worker to do its wonders

Exploiting is just one step ahead:

6. Use any hoisted builtins in the iframe context

A simple `%DebugPrintPtr(0x424242424241)` is sufficient to demonstrate a read violation outside of v8sbx. For a full bypass, [`%DeserializeWasmModule(serialized_bytes, wire_bytes)`](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/runtime/runtime-test-wasm.cc;drc=5619ecfaa0cbe5fd32304cf98c3095e3d3f2aadb;l=536) is one easy path that allows the attacker to deserialize arbitrary native code. The attached exploit uses the latter to execute attacker-controlled shellcode.

### VERSION

V8: Tested on [`asan-v8-sandbox-testing-linux-release-1502435`](https://console.cloud.google.com/storage/browser/_details/chromium-browser-asan/linux-release-v8-sandbox-testing/asan-v8-sandbox-testing-linux-release-1502435.zip)

### REPRODUCTION CASE

Attached as `v8sbx-unlock-intrinsics.html`. The repro hoists out some intrinsics into the iframe's globals as `EXT` and uses this to execute arbitrary shellcode that:

1. Prints out `/etc/passwd` to stdout
2. Executes a controlled write equivalent to pseudo-asm `movq [0x424242424242], 0x4343434343434343` and crashes with a v8sbx violation

Run with `./chrome --js-flags=--sandbox-testing --no-sandbox` to see both 1 & 2. You can omit `--no-sandbox` which will still show v8sbx violation crash from 2. Search and change the shellcode after `let shellcode =`  if you want different behavior.

### FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: Sandbox violation

### CREDIT INFORMATION

Reporter credit: Seunghyun Lee (@0x10n) of CMU CyLab

---

A far variant of [b/435630464](https://issues.chromium.org/issues/435630464) where the underlying security problem is similar.  

Marking any rewards for charity in advance.

## Attachments

- [v8sbx-unlock-intrinsics.html](attachments/v8sbx-unlock-intrinsics.html) (text/html, 87.0 KB)

## Timeline

### th...@chromium.org (2025-08-18)

[security shepherd] Triaging V8 sandbox bypass: 
 - Set a provisional severity of Medium (S2).
 - Set a provisional priority of P1.
 - Assign to the current V8 Sheriff.
 - Apply the Security_Impact-None hotlist (hotlistID:5433277).
 - If possible, please also apply the V8 Sandbox hotlist (hotlistID:4802478).

### ml...@google.com (2025-08-19)

Summary from offline chat:

1. `v8::Extension` allows for using native syntax, which is really unfortunate but seems like an old design decision
2. Chrome ships in production with extensions.
3. The extension source string is untrusted and lives in the sandbox and can thus be corrupted.

Options:

- Add an option that prohibits native syntax in extension and require that all Chrome-shipped extensions follow this policy. The bool needs to be trusted.
- Use a trusted string (e.g. c string) for compiling extensions. This seems doable.

We probably can't forbid extensions in Chrome and also cannot forbid natives in general (?)

### is...@chromium.org (2025-08-20)

Thank you for the report! Nice catch!

It seems that disallowing natives syntax in extensions is the way to go. `v8::Extension` Api provides a way for defining custom functionality [v8::Extension::GetNativeFunctionTemplate()](https://source.chromium.org/chromium/chromium/src/+/main:chrome/renderer/loadtimes_extension_bindings.cc;l=65?q=GetNativeFunctionTemplate&ss=chromium%2Fchromium%2Fsrc&start=11) and all extensions already use it.

So, as long as the custom extensions' functions are robust against random input and thus against potential extension's code modifications we should be fine. Not 100% sure yet how we can enforce this robustness.

### dx...@google.com (2025-08-20)

Project: v8/v8  

Branch:  main  

Author:  Igor Sheludko [ishell@chromium.org](mailto:ishell@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6863072>

[parser] Disallow natives syntax in v8::Extensions

---


Expand for full commit details
```
     
    v8::Extension Api provides a way for defining custom functionality 
    via v8::Extension::GetNativeFunctionTemplate(). So there's no need 
    to allow them to run arbitrary runtime functions. 
     
    This disentangles V8 internals (runtime functions set) from embedders' 
    world and allows V8 to modify the set of runtime functions without 
    a fear of breaking extensions. 
     
    Fixed: 439380004 
    Change-Id: I38a97120ea02e5a3aa60eab316cea7a04742f41a 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6863072 
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    Commit-Queue: Igor Sheludko <ishell@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#101956}

```

---

Files:

- M `src/parsing/parser-base.h`
- M `src/parsing/parser.cc`
- M `test/cctest/test-api.cc`

---

Hash: [4108ddc017df6463a114aa64371d79b6c8b162c5](https://chromiumdash.appspot.com/commit/4108ddc017df6463a114aa64371d79b6c8b162c5)  

Date: Wed Aug 20 13:48:39 2025


---

### sp...@google.com (2025-08-28)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $20000.00 for this report.

Rationale for this decision:
report of V8 sandbox bypass demonstrating a controlled write outside the V8 heap sandbox


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2025-11-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-11-28)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/439380004)*
