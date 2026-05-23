# V8 Sandbox Bypass: AAW due to JSArrayBuffer extension handle double fetch

| Field | Value |
|-------|-------|
| **Issue ID** | [464296297](https://issues.chromium.org/issues/464296297) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Sandbox |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | h3...@gmail.com |
| **Assignee** | ml...@chromium.org |
| **Created** | 2025-11-28 |
| **Bounty** | $20,000.00 |

## Description

### VULNERABILITY DETAILS

#### Summary

V8 sandbox bypass, arbitrary write by exploiting double fetch race condition of `JSArrayBuffer` extension handle multiple times.

#### Background

To obtain an `ArrayBufferExtension` from a `JSArrayBuffer` object, V8 first loads the object’s `ExternalPointerHandle` from the heap sandbox, then use the handle as a index to retrieve the pointer store on External Pointer Table (EPT). Thus, if the heap sandbox has been compromised, every call to `JSArrayBuffer::GetBackingStore` or `JSArrayBuffer::extension` on same `JSArrayBuffer` object could potentially fetch a different entry from EPT due to the fact that attacker can now alter the handle at anytime. This creates inconsistencies between calls.

```
std::shared_ptr<BackingStore> JSArrayBuffer::GetBackingStore() const {
  if (!extension()) return nullptr;
  return extension()->backing_store();
}

ArrayBufferExtension* JSArrayBuffer::extension() const {
#if V8_COMPRESS_POINTERS
  // We need Acquire semantics here when loading the entry, see below.
  // Consider adding respective external pointer accessors if non-relaxed
  // ordering semantics are ever needed in other places as well.
  Isolate* isolate = Isolate::Current();
  ExternalPointerHandle handle =
      base::AsAtomic32::Acquire_Load(extension_handle_location());
  return reinterpret_cast<ArrayBufferExtension*>(
      isolate->external_pointer_table().Get(handle, kArrayBufferExtensionTag));
#else
  return base::AsAtomicPointer::Acquire_Load(extension_location());
#endif  // V8_COMPRESS_POINTERS
}

```

`JSArrayBuffer::set_extension` binds an extension pointer to a `JSArrayBuffer` object.  

The current implementation supports both "new" and "update" semantics:

- **New** – If the current handle is `kNullExternalPointerHandle`, a new entry is allocated in the External Pointer Table (EPT) to reference the extension, and the `JSArrayBuffer`’s external handle is updated to bind it to this new backing extension.
- **Update** – If the current handle already holds a valid pointer, the old extension is detached first, and then the same steps as in the “new” case are performed to bind the new extension.

```
void JSArrayBuffer::set_extension(ArrayBufferExtension* extension) {
  ...

  ExternalPointerHandle current_handle =
      base::AsAtomic32::Relaxed_Load(extension_handle_location());
  if (current_handle == kNullExternalPointerHandle) { // new
    // We need Release semantics here, see above.
    ExternalPointerHandle handle = table.AllocateAndInitializeEntry(
        isolate.GetExternalPointerTableSpaceFor(tag, address()), value, tag);
    base::AsAtomic32::Release_Store(extension_handle_location(), handle);
    EXTERNAL_POINTER_WRITE_BARRIER(*this, kExtensionOffset, tag);
  } else {
    table.Set(current_handle, value, tag); // update
  }
  ...
}

```

Below we will exploit the inconsistency caused by the double fetch to confuse `JSArrayBuffer::set_extension` into performing different actions based on incorrect semantics.

#### The vulnerability

With above background in mind, we can start to analysis the vulnerable `Serializer::ObjectSerializer::SerializeJSArrayBuffer`. As its name imply, the function serializes an `ArrayBuffer` object. During the serialization, the function first retrieves the extension[1], update the backing extension to nullptr[2], and set the extension back[3].

The "save‑reset‑recover" pattern becomes problematic if an attacker can alter the handle at any time. By concurrently modifying the `JSArrayBuffer`'s handle value between each step, we can create two identical entries in the EPT that reference to the same extension.

```
void Serializer::ObjectSerializer::SerializeJSArrayBuffer() {
  ArrayBufferExtension* extension;
  void* backing_store;
  {
    ...
    extension = buffer->extension(); // [1] fetch handle

    // Only serialize non-empty backing stores.
    if (buffer->IsEmpty()) {
      buffer->SetBackingStoreRefForSerialization(kEmptyBackingStoreRefSentinel);
    } else {
      uint32_t ref =
          SerializeBackingStore(backing_store, byte_length, max_byte_length);
      buffer->SetBackingStoreRefForSerialization(ref);
    }

    // Ensure deterministic output by setting extension to null during
    // serialization.
    buffer->set_extension(nullptr); // [2] re-fetch handle
  }
  SerializeObject();
  {
    Tagged<JSArrayBuffer> buffer = Cast<JSArrayBuffer>(*object_);
    buffer->set_backing_store(isolate(), backing_store);
    buffer->set_extension(extension); // [3] re-fetch handle
  }
}

```

The race attack plan is listed below:

1. An `ArrayBuffer` object with an `extension` indexed at entry `A` on EPT is being serialized by `SerializeJSArrayBuffer()`
2. During backing store serialization: racing thread sets the handle to `null` to make `set_extension` work under "new" semantics
3. When `set_extension(nullptr)`[2] is executed, it **re‑fetches the null handle** , allocates a new EPT entry `B` with value `null`, and updates the object’s handle to `B`
4. During object serialization: racing thread again sets the handle to `null`
5. When `set_extension(extension)`[3] is executed, it **re‑fetches the null handle** , allocates a new EPT entry `C` with value `extension`, and again update the object’s handle to `C`

After the race, both EPT index `A` and `C` reference to the same `ArrayBufferExtension` object.

To trigger this vulnerability, `SerializeJSArrayBuffer` has to be invoked. We couldn’t find any direct code path that calls it, but after some trial‑and‑error we discovered that injecting a `JSArrayBuffer` into `SharedFunctionInfo.untrusted_function_data` causes the function to be called during the creation of a service‑worker code cache (`v8::ScriptCompiler::CreateCodeCache`). Thus, we are able to race a worker thread created by `navigator.serviceWorker.register` in the main thread.

#### Dealing with GC

Even though we managed to create two identical entries on EPT, we still cannot simply delete one of the entry from the EPT to force the backing extension to be freed, since `ExternalPointerTable` entry and `ArrayBufferExtension` are **both \*separately\* managed by GC**.

During the GC marking phase, the extension is marked in `JSArrayBuffer::YoungMarkExtension`[4], and immediately afterward the array buffer itself is marked in `JSArrayBuffer::BodyDescriptor::IterateBody`[5] via a call to `VisitExternalPointer`[6]. Both marking procedures start by retrieving the same external handle from the `JSArrayBuffer` object, so they are either both marked or neither is.

Therefore, it seems impossible to keep only one of the entries alive while freeing the backing extension, since if the entry is marked, the backing extension will be marked as well. This should stop our exploit, right?

```
  V8_INLINE size_t VisitJSArrayBuffer(Tagged<Map> map,
                                      Tagged<JSArrayBuffer> object,
                                      MaybeObjectSize) {
    if constexpr (kExpectedObjectAge == ObjectAge::kYoung) {
      object->YoungMarkExtension();                                      // [4]
    } else {
      object->YoungMarkExtensionPromoted();
    }
    ...
    JSArrayBuffer::BodyDescriptor::IterateBody(map, object, size, this); // [5]
    return size;
  }

void JSArrayBuffer::YoungMarkExtension() {
  ArrayBufferExtension* extension = this->extension();                   // fetch #1
  if (extension) {
    DCHECK_EQ(ArrayBufferExtension::Age::kYoung, extension->age());
    extension->YoungMark();
  }
}

  template <typename ObjectVisitor>
  static inline void IterateBody(Tagged<Map> map, Tagged<HeapObject> obj,
                                 int object_size, ObjectVisitor* v) {
    // Iterate other pointers
    ...

    v->VisitExternalPointer(                                              // [6]
        obj, obj->RawExternalPointerField(JSArrayBuffer::kExtensionOffset,
                                          kArrayBufferExtensionTag));
    // JSObject tail: possible embedder fields + in-object properties.
    ...
  }

template <typename ConcreteVisitor>
void MarkingVisitorBase<ConcreteVisitor>::VisitExternalPointer(
    Tagged<HeapObject> host, ExternalPointerSlot slot) {
  ...
  if (slot.HasExternalPointerHandle()) {
    ExternalPointerHandle handle = slot.Relaxed_LoadHandle();             // fetch #2
    ...
    table->Mark(space, handle, slot.address());
  }
}

```

It turns out the same handle double fetch pattern also occurred here:

- Mark `ArrayBufferExtension` [4]: `this->extension()`
- Mark `ExternalPointerTable` entry [6]: `slot.Relaxed_LoadHandle()`

Therefore, by racing against asynchronous GC, we can trick collector into treating the EPT entry as live while leaving its backing`ArrayBufferExtension` unmarked. In the following sweeping phase, the backing extension will be freed by `ArrayBufferSweeper` in `FinalizeAndDelete`[7], leaving a dangling entry in the EPT.

It is worth mentioning that before deletion, `ZapExternalPointerTableEntry` will be called to "zap" (delete) the entry[8] on EPT to avoid accidentally leaving dangling entries. In our case, however, two EPT entries reference to the same extension, thus `ext->ept_entry_` can be zapped while another entry that still refers to the same extension remains alive.

```
bool ArrayBufferSweeper::SweepingState::SweepingJob::SweepListFull(
    JobDelegate* delegate, ArrayBufferList& list,
    ArrayBufferExtension::Age age) {
  ...

  while (current) {
    ...
    ArrayBufferExtension* next = current->next();

    if (!current->IsMarked()) {
      freed_bytes += current->accounting_length();
      FinalizeAndDelete(current);                   // [7]
    } else {
      current->Unmark();
      accounted_bytes += new_old.Append(current);
    }

    current = next;
  }
  ...
}

void ArrayBufferSweeper::FinalizeAndDelete(ArrayBufferExtension* extension) {
#ifdef V8_COMPRESS_POINTERS
  extension->ZapExternalPointerTableEntry();
#endif  // V8_COMPRESS_POINTERS
  delete extension;
}

void ExternalPointerTable::ManagedResource::ZapExternalPointerTableEntry() {
  if (owning_table_) {
    owning_table_->Zap(ept_entry_);                 // [8]
  }
  ept_entry_ = kNullExternalPointerHandle;
}

```
#### From UAF to arbitrary write

With two race in `SerializeJSArrayBuffer` and one race in `JSArrayBuffer::BodyDescriptor` we now create a freed 64‑byte chunk managed by native heap which still referenced by an entry on EPT.

To exploit this UAF, we first spray a number of text buffers with `console.log` to reclaim the freed chunk. Next, we instantiate a `DataView` object with the vulnerable `ArrayBuffer` that holds the dandling handle. The `DataView` constructor internally calls `JSArrayBuffer::GetBackingStore` to reads the `backing_store_` field from the extension.

Because `backing_store_` is a `std::shared_ptr`, it contains another internal pointer that points to an object holding a reference count. Assigning this `std::shared_ptr` to a new variable will increment the counter, so by manipulating the internal pointer we can perform an arbitrary write (arbitrarily incrementing the reference count by one) during the construction of `DataView`.

### VERSION

The exploit is tested on Chromium commit `bc0e4f7e37c39876da88bad1af597c69032b61ad` (the vuln still exist in latest version, however, I'm not yet port the exploit), running on macOS 15.6.1 on an Apple M3 Max chip with the following configuration.

```
is_debug = true
symbol_level = 2
target_cpu = "arm64"
v8_target_cpu = "arm64"
v8_enable_sandbox = true
v8_enable_backtrace = true
v8_enable_fast_mksnapshot = true
v8_enable_memory_corruption_api = true
v8_enable_verify_heap = false
v8_enable_verify_csa = false
v8_dcheck_always_on = false
v8_optimized_debug = false

```

The race timing depends on the underlying hardware and may need to be adjusted when testing on a different platform/hardware; we deliberately use the debug build to enlarge the race window.

We applied some patches to v8 source code to make the race exploit stable, but it is unrelated to the bug itself.

- Disable all debug checks
- Disable `verify_snapshot_checksum` since it only affect debug build
- Expose `memory_corruption_api` by default since the sandbox crash filter only available on Linux
- Add a `sleep` in `JSArrayBuffer::BodyDescriptor` to ease the race exploit development
- Add a builtin function `Sandbox.getExternalPointerTable` just for debug purpose

```
diff --git a/src/base/logging.cc b/src/base/logging.cc
index 54aa99f02d7..525defc7b93 100644
--- a/src/base/logging.cc
+++ b/src/base/logging.cc
@@ -226,3 +226,5 @@ void V8_Dcheck(const char* file, int line, const char* message) {
 
   v8::base::g_dcheck_function(file, line, message);
 }
+
+void V8_Dnocheck(const char* file __attribute__((unused)), int line __attribute__((unused)), const char* message __attribute__((unused))) {}
diff --git a/src/base/logging.h b/src/base/logging.h
index 722c6cdabda..a3d0c530847 100644
--- a/src/base/logging.h
+++ b/src/base/logging.h
@@ -23,6 +23,9 @@
 V8_BASE_EXPORT V8_NOINLINE void V8_Dcheck(const char* file, int line,
                                           const char* message);
 
+V8_BASE_EXPORT V8_NOINLINE void V8_Dnocheck(const char* file __attribute__((unused)), int line __attribute__((unused)),
+                                          const char* message __attribute__((unused)));
+
 #ifdef DEBUG
 // In debug, include file, line, and full error message for all
 // FATAL() calls.
@@ -132,13 +135,13 @@ enum class OOMType {
 #define DCHECK_WITH_MSG_AND_LOC(condition, message, loc)                    \
   do {                                                                      \
     if (V8_UNLIKELY(!(condition))) {                                        \
-      V8_Dcheck((loc).FileName(), static_cast<int>((loc).Line()), message); \
+      V8_Dnocheck((loc).FileName(), static_cast<int>((loc).Line()), message); \
     }                                                                       \
   } while (false)
 #define DCHECK_WITH_MSG(condition, message)   \
   do {                                        \
     if (V8_UNLIKELY(!(condition))) {          \
-      V8_Dcheck(__FILE__, __LINE__, message); \
+      V8_Dnocheck(__FILE__, __LINE__, message); \
     }                                         \
   } while (false)
 #define DCHECK_WITH_LOC(condition, loc) \
@@ -164,7 +167,7 @@ enum class OOMType {
             typename ::v8::base::pass_value_or_ref<decltype(lhs)>::type,  \
             typename ::v8::base::pass_value_or_ref<decltype(rhs)>::type>( \
             (lhs), (rhs), #lhs " " #op " " #rhs)) {                       \
-      V8_Dcheck(__FILE__, __LINE__, _msg->c_str());                       \
+      V8_Dnocheck(__FILE__, __LINE__, _msg->c_str());                       \
       delete _msg;                                                        \
     }                                                                     \
   } while (false)
diff --git a/src/flags/flag-definitions.h b/src/flags/flag-definitions.h
index dfa1cabafa3..2b20f35e6d1 100644
--- a/src/flags/flag-definitions.h
+++ b/src/flags/flag-definitions.h
@@ -3015,7 +3015,7 @@ DEFINE_BOOL(rcs_cpu_time, false,
 DEFINE_IMPLICATION(rcs_cpu_time, rcs)
 
 // snapshot-common.cc
-DEFINE_BOOL(verify_snapshot_checksum, DEBUG_BOOL,
+DEFINE_BOOL(verify_snapshot_checksum, false,
             "Verify snapshot checksums when deserializing snapshots. Enable "
             "checksum creation and verification for code caches. Enabled by "
             "default in debug builds and once per process for Android.")
@@ -3187,7 +3187,7 @@ DEFINE_NEG_IMPLICATION(sandbox_fuzzing, sandbox_testing)
 DEFINE_NEG_IMPLICATION(sandbox_testing, sandbox_fuzzing)
 
 #ifdef V8_ENABLE_MEMORY_CORRUPTION_API
-DEFINE_BOOL(expose_memory_corruption_api, false,
+DEFINE_BOOL(expose_memory_corruption_api, true,
             "Exposes the memory corruption API. Set automatically by "
             "--sandbox-testing and --sandbox-fuzzing.")
 DEFINE_IMPLICATION(sandbox_fuzzing, expose_memory_corruption_api)
diff --git a/src/objects/objects-body-descriptors-inl.h b/src/objects/objects-body-descriptors-inl.h
index ef7b05780c1..b349d2ec536 100644
--- a/src/objects/objects-body-descriptors-inl.h
+++ b/src/objects/objects-body-descriptors-inl.h
@@ -614,6 +614,14 @@ class JSArrayBuffer::BodyDescriptor final
     // JSObject with wrapper field.
     IterateJSAPIObjectWithEmbedderSlotsHeader(map, obj, object_size, v);
     // JSArrayBuffer.
+    auto slot = obj->RawField(JSArrayBuffer::kStartOfStrongFieldsOffset);
+    unsigned flag = static_cast<unsigned>(slot.load(v->cage_base()).ptr());
+    if (flag == 0x41414141) {
+      puts("going to sleep...");
+      slot.store(v8::internal::GetReadOnlyRoots().undefined_value()); // delete custom flag
+      sleep(10);
+      puts("wake up");
+    }
     IteratePointers(obj, JSArrayBuffer::kStartOfStrongFieldsOffset,
                     JSArrayBuffer::kEndOfStrongFieldsOffset, v);
     v->VisitExternalPointer(
diff --git a/src/sandbox/testing.cc b/src/sandbox/testing.cc
index f263687ef69..ed13068c6ff 100644
--- a/src/sandbox/testing.cc
+++ b/src/sandbox/testing.cc
@@ -485,6 +485,14 @@ void SandboxSetFunctionCodeToBuiltin(
   info.GetReturnValue().Set(true);
 }
 
+void SandboxGetExternalPointerTable(const v8::FunctionCallbackInfo<v8::Value>& info) {
+  v8::Isolate* isolate = info.GetIsolate();
+  i::Isolate* i_isolate = v8::internal::g_current_isolate_;
+  auto pept = (char *)&i_isolate->external_pointer_table();
+  double base = *(size_t *)pept; // base_ is at offset 0
+  info.GetReturnValue().Set(v8::Number::New(isolate, base));
+}
+
 Handle<FunctionTemplateInfo> NewFunctionTemplate(
     Isolate* isolate, FunctionCallback func,
     ConstructorBehavior constructor_behavior) {
@@ -583,6 +591,8 @@ void SandboxTesting::InstallMemoryCorruptionApi(Isolate* isolate) {
                   0);
   InstallFunction(isolate, sandbox, SandboxSetFunctionCodeToBuiltin,
                   "setFunctionCodeToBuiltin", 2);
+  InstallFunction(isolate, sandbox, SandboxGetExternalPointerTable,
+                  "getExternalPointerTable", 0);
 
   // Install the Sandbox object as property on the global object.
   Handle<JSGlobalObject> global = isolate->global_object();


```
### REPRODUCTION CASE

The exploit requires registering a service worker to race, thus, a full Chromium environment is required.

Use `python3 -m http.server <PORT>` to host `exp.html` and `sw_longlonglonglonglonglonglongname.js` (deliberate long name to avoid unintended allocation), navigate to the page and click to visit `exp.html`, the exploit attempts a controlled write by increment one on `0x4141414141414149`.

If the exploit failed, before re-run, the previously registered service worker should be unregistered in `chrome://serviceworker-internals/?devtools`.

### FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: Sandbox violation

Crash state:

```
* thread #18, name = 'ServiceWorker thread', stop reason = EXC_BAD_ACCESS (code=257, address=0x4141414141414149)
    frame #0: 0x000000037bc1ff34 libv8.dylib`long std::__Cr::__libcpp_atomic_refcount_increment<long>(__t=0x4141414141414149) at shared_count.h:56:10
   53   template <class _Tp>
   54   inline _LIBCPP_HIDE_FROM_ABI _Tp __libcpp_atomic_refcount_increment(_Tp& __t) _NOEXCEPT {
   55   #if _LIBCPP_HAS_BUILTIN_ATOMIC_SUPPORT && _LIBCPP_HAS_THREADS
-> 56     return __atomic_add_fetch(std::addressof(__t), 1, __ATOMIC_RELAXED);
   57   #else
   58     return __t += 1;
   59   #endif
Target 0: (Chromium Helper (Renderer)) stopped.
(lldb) bt
* thread #18, name = 'ServiceWorker thread', stop reason = EXC_BAD_ACCESS (code=257, address=0x4141414141414149)
  * frame #0: 0x000000037bc1ff34 libv8.dylib`long std::__Cr::__libcpp_atomic_refcount_increment<long>(__t=0x4141414141414149) at shared_count.h:56:10
    frame #1: 0x000000037bc1ff10 libv8.dylib`std::__Cr::__shared_count::__add_shared(this=0x4141414141414141) at shared_count.h:89:57
    frame #2: 0x000000037bc1fee8 libv8.dylib`std::__Cr::__shared_weak_count::__add_shared(this=0x4141414141414141) at shared_count.h:118:73
    frame #3: 0x000000037bc1febc libv8.dylib`std::__Cr::shared_ptr<v8::internal::BackingStore>::shared_ptr(this=0x00000005007ff0c8, __r=std::__Cr::shared_ptr<v8::internal::BackingStore>::element_type @ 0x4141414141414141) at shared_ptr.h:478:17
    frame #4: 0x000000037bc1fe58 libv8.dylib`std::__Cr::shared_ptr<v8::internal::BackingStore>::shared_ptr(this=0x00000005007ff0c8, __r=std::__Cr::shared_ptr<v8::internal::BackingStore>::element_type @ 0x4141414141414141) at shared_ptr.h:476:114
    frame #5: 0x000000037bc1fda0 libv8.dylib`v8::internal::ArrayBufferExtension::backing_store(this=0x0000600002fa5c80) at js-array-buffer.h:230:58
    frame #6: 0x000000037bb956f8 libv8.dylib`v8::internal::JSArrayBuffer::GetBackingStore(this=0x00000005007ff748) const at js-array-buffer-inl.h:68:23
    frame #7: 0x000000037bbc4b3c libv8.dylib`v8::internal::JSArrayBuffer::GetByteLength(this=0x00000005007ff748) const at js-array-buffer-inl.h:82:26
    frame #8: 0x000000037bdc6cb8 libv8.dylib`v8::internal::Builtin_Impl_DataViewConstructor(args=BuiltinArguments @ 0x00000005007ff858, isolate=0x00000004d8028000) at builtins-dataview.cc:60:45
    frame #9: 0x000000037bdc65c8 libv8.dylib`v8::internal::Builtin_DataViewConstructor(args_length=6, args_object=0x00000005007ff9c8, isolate=0x00000004d8028000) at builtins-dataview.cc:21:1
    frame #10: 0x00000004229efff0
    frame #11: 0x00000004227374e4
    frame #12: 0x0000000422e9cbbc
    frame #13: 0x0000000422736734
    frame #14: 0x000000042272e6e0
    frame #15: 0x000000042272e314
    frame #16: 0x000000037c2c5b64 libv8.dylib`v8::internal::GeneratedCode<unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**>::Call(this=0x00000005007fffa0, args=20803911936, args=54919746813969, args=<unavailable>, args=<unavailable>, args=<unavailable>, args=<unavailable>) at simulator.h:212:12
    frame #17: 0x000000037c2c2c10 libv8.dylib`v8::internal::(anonymous namespace)::Invoke(isolate=0x00000004d8028000, params=0x0000000500800338) at execution.cc:442:22
    frame #18: 0x000000037c2c1c24 libv8.dylib`v8::internal::Execution::Call(isolate=0x00000004d8028000, callable=DirectHandle<v8::internal::Object> @ 0x00000005008003c0, receiver=DirectHandle<v8::internal::Object> @ 0x00000005008003b8, args=Vector<const v8::internal::DirectHandle<v8::internal::Object> > @ 0x00000005008003a8) at execution.cc:532:10
    frame #19: 0x000000037bba44c8 libv8.dylib`v8::Function::Call(this=0x00000003a984c820, isolate=0x00000004d8028000, context=Local<v8::Context> @ 0x00000005008004f8, recv=Local<v8::Value> @ 0x00000005008004f0, argc=0, argv=0x0000000500800da8) at api.cc:5380:27
    frame #20: 0x0000000347c2d3d8 libblink_core.dylib`blink::V8ScriptRunner::CallFunction(function=Local<v8::Function> @ 0x0000000500800778, context=0x0000013400660868, receiver=Local<v8::Value> @ 0x0000000500800770, argc=0, argv=0x0000000500800da8, isolate=0x00000004d8028000) at v8_script_runner.cc:855:48
    frame #21: 0x00000003479cd5ec libblink_core.dylib`blink::bindings::CallbackInvokeHelper<blink::CallbackFunctionBase, (blink::bindings::CallbackInvokeHelperMode)0, (blink::bindings::CallbackReturnTypeIsPromise)0>::CallInternal(this=0x0000000500800cf0, argc=0, argv=0x0000000500800da8) at callback_invoke_helper.cc:126:12
    frame #22: 0x00000003479cd41c libblink_core.dylib`blink::bindings::CallbackInvokeHelper<blink::CallbackFunctionBase, (blink::bindings::CallbackInvokeHelperMode)0, (blink::bindings::CallbackReturnTypeIsPromise)0>::Call(this=0x0000000500800cf0, argc=0, argv=0x0000000500800da8) at callback_invoke_helper.cc:150:10
    frame #23: 0x000000034d0f95d8 libblink_core.dylib`blink::V8Function::Invoke(this=0x0000013400640d18, arg0_receiver=V8ValueOrScriptWrappableAdapter @ 0x0000000500800cd8, arg1_arguments=0x0000013400640d48) at v8_function.cc:73:13
    frame #24: 0x000000034d0f9dcc libblink_core.dylib`blink::V8Function::InvokeAndReportException(this=0x0000013400640d18, arg0_receiver=V8ValueOrScriptWrappableAdapter @ 0x0000000500800e60, arg1_arguments=0x0000013400640d48) at v8_function.cc:133:15
    frame #25: 0x000000034bbfa110 libblink_core.dylib`blink::ScheduledAction::Execute(this=0x0000013400640d38, context=0x0000013400660868) at scheduled_action.cc:145:18
    frame #26: 0x000000034bbe9e78 libblink_core.dylib`blink::DOMTimer::Fired(this=0x0000013400663f08) at dom_timer.cc:444:11
    frame #27: 0x000000035b4c1fe8 libblink_platform.dylib`blink::TimerBase::RunInternal(this=0x0000013400663f08) at timer.cc:166:3
    frame #28: 0x000000034967d7f4 libblink_core.dylib`void base::internal::DecayedFunctorTraits<void (blink::TimerBase::*)(), blink::TimerBase*>::Invoke<void (blink::TimerBase::*)(), blink::TimerBase*>(method=(libblink_platform.dylib`blink::TimerBase::RunInternal() at timer.cc:140), receiver_ptr=0x0000000500802150) at bind_internal.h:730:12
    frame #29: 0x000000034967d73c libblink_core.dylib`void base::internal::InvokeHelper<false, base::internal::FunctorTraits<void (blink::TimerBase::*&&)(), blink::TimerBase*>, void, 0ul>::MakeItSo<void (blink::TimerBase::*)(), std::__Cr::tuple<blink::UnretainedWrapper<blink::TimerBase>>>(functor=0x0000600002ff4fa0, bound=size=1) at bind_internal.h:922:12
    frame #30: 0x000000034967d6c4 libblink_core.dylib`void base::internal::Invoker<base::internal::FunctorTraits<void (blink::TimerBase::*&&)(), blink::TimerBase*>, base::internal::BindState<true, true, false, void (blink::TimerBase::*)(), blink::UnretainedWrapper<blink::TimerBase>>, void ()>::RunImpl<void (blink::TimerBase::*)(), std::__Cr::tuple<blink::UnretainedWrapper<blink::TimerBase>>, 0ul>(functor=0x0000600002ff4fa0, bound=size=1, (null)=std::__Cr::index_sequence<0UL> @ 0x000000050080218f) at bind_internal.h:1059:14
    frame #31: 0x000000034967d64c libblink_core.dylib`base::internal::Invoker<base::internal::FunctorTraits<void (blink::TimerBase::*&&)(), blink::TimerBase*>, base::internal::BindState<true, true, false, void (blink::TimerBase::*)(), blink::UnretainedWrapper<blink::TimerBase>>, void ()>::RunOnce(base=0x0000600002ff4f80) at bind_internal.h:972:12
    frame #32: 0x0000000347a917a0 libblink_core.dylib`base::OnceCallback<void ()>::Run(this=0x000060000083d678) && at callback.h:155:12
    frame #33: 0x0000000347a916e4 libblink_core.dylib`blink::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>::RunInternal(callback=0x000060000083d678) at functional.h:243:33
    frame #34: 0x0000000347a8ff10 libblink_core.dylib`blink::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>::Run(this=0x000060000083d5f0) at functional.h:228:12
    frame #35: 0x0000000347a90eb0 libblink_core.dylib`void base::internal::DecayedFunctorTraits<void (blink::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>::*)(), std::__Cr::unique_ptr<blink::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>, std::__Cr::default_delete<blink::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>>>&&>::Invoke<void (blink::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>::*)(), std::__Cr::unique_ptr<blink::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>, std::__Cr::default_delete<blink::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>>>>(method=(libblink_core.dylib`blink::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>::Run() at functional.h:226), receiver_ptr=0x0000600002ff4eb0) at bind_internal.h:730:12
    frame #36: 0x0000000347a90e18 libblink_core.dylib`void base::internal::InvokeHelper<false, base::internal::FunctorTraits<void (blink::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>::*&&)(), std::__Cr::unique_ptr<blink::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>, std::__Cr::default_delete<blink::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>>>&&>, void, 0ul>::MakeItSo<void (blink::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>::*)(), std::__Cr::tuple<std::__Cr::unique_ptr<blink::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>, std::__Cr::default_delete<blink::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>>>>>(functor=0x0000600002ff4ea0, bound=size=1) at bind_internal.h:922:12
    frame #37: 0x0000000347a90db4 libblink_core.dylib`void base::internal::Invoker<base::internal::FunctorTraits<void (blink::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>::*&&)(), std::__Cr::unique_ptr<blink::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>, std::__Cr::default_delete<blink::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>>>&&>, base::internal::BindState<true, true, false, void (blink::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>::*)(), std::__Cr::unique_ptr<blink::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>, std::__Cr::default_delete<blink::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>>>>, void ()>::RunImpl<void (blink::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>::*)(), std::__Cr::tuple<std::__Cr::unique_ptr<blink::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>, std::__Cr::default_delete<blink::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>>>>, 0ul>(functor=0x0000600002ff4ea0, bound=size=1, (null)=std::__Cr::index_sequence<0UL> @ 0x000000050080234f) at bind_internal.h:1059:14
    frame #38: 0x0000000347a90d3c libblink_core.dylib`base::internal::Invoker<base::internal::FunctorTraits<void (blink::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>::*&&)(), std::__Cr::unique_ptr<blink::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>, std::__Cr::default_delete<blink::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>>>&&>, base::internal::BindState<true, true, false, void (blink::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>::*)(), std::__Cr::unique_ptr<blink::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>, std::__Cr::default_delete<blink::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>>>>, void ()>::RunOnce(base=0x0000600002ff4e80) at bind_internal.h:972:12
    frame #39: 0x0000000104d9051c libbase.dylib`base::OnceCallback<void ()>::Run(this=0x00000003b303b478) && at callback.h:155:12
    frame #40: 0x0000000105007e90 libbase.dylib`base::TaskAnnotator::RunTaskImpl(this=0x00000003aa0a4f58, pending_task=0x00000003b303b400) at task_annotator.cc:207:34
    frame #41: 0x0000000105093a38 libbase.dylib`void base::TaskAnnotator::RunTask<base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_4>(this=0x00000003aa0a4f58, event_name=(value = "ThreadControllerImpl::RunTask"), pending_task=0x00000003b303b400, args=0x00000005008026b8) at task_annotator.h:104:5
    frame #42: 0x00000001050933a0 libbase.dylib`base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(this=0x00000003aa0a4c00, continuation_lazy_now=0x0000000500802990) at thread_controller_with_message_pump_impl.cc:472:23
    frame #43: 0x0000000105092b54 libbase.dylib`base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(this=0x00000003aa0a4c00) at thread_controller_with_message_pump_impl.cc:346:40
    frame #44: 0x0000000104e371ac libbase.dylib`base::MessagePumpDefault::Run(this=0x0000600001e383c0, delegate=0x00000003aa0a4d20) at message_pump_default.cc:42:55
    frame #45: 0x00000001050941dc libbase.dylib`base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(this=0x00000003aa0a4c00, application_tasks_allowed=true, timeout=TimeDelta @ 0x0000000500802c08) at thread_controller_with_message_pump_impl.cc:647:12
    frame #46: 0x0000000104f54e94 libbase.dylib`base::RunLoop::Run(this=0x0000000500802e30, location=0x0000000500802dd8) at run_loop.cc:134:14
    frame #47: 0x000000035bad10ec libblink_platform.dylib`blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run(this=0x0000600000339f80) at non_main_thread_impl.cc:187:14
    frame #48: 0x00000001051382d0 libbase.dylib`base::SimpleThread::ThreadMain(this=0x0000600000339f80) at simple_thread.cc:79:3
    frame #49: 0x00000001051b2270 libbase.dylib`base::(anonymous namespace)::ThreadFunc(params=0x0000600003a0ed00) at platform_thread_posix.cc:102:13
    frame #50: 0x000000019f5e7c0c libsystem_pthread.dylib`_pthread_start + 136

```
### CREDIT INFORMATION

Reporter credit: HexRabbit (@h3xr4bb1t) of DEVCORE Research Team

## Attachments

- [exp.html](attachments/exp.html) (text/html, 3.6 KB)
- [sw_longlonglonglonglonglonglongname.js](attachments/sw_longlonglonglonglonglonglongname.js) (text/javascript, 3.7 KB)
- [v8-sandbox-exploit.mp4](attachments/v8-sandbox-exploit.mp4) (video/mp4, 6.2 MB)

## Timeline

### ar...@chromium.org (2025-11-28)

Thanks for the detailed report and the exploit.

I am triaging this as a V8 Sandbox bypass. Per our [security shepherding guidelines for sandbox bypasses](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/shepherd.md#:~:text=normally%20be%20necessary.-,V8%20Sandbox%20bypasses,-.%20The%20V8%20Sandbox), I am setting the following properties:

- **Severity:** S2
- **Priority:** P1
- **Hotlists:** `Security_Impact-None` and `V8 Sandbox`

I am assigning this to the current V8 Shepherd for further review and remediation.

### pa...@google.com (2025-11-28)

Thank you for the detailed report @h3...@gmail.com.

I didn't try to reproduce. From a quick look @sa...@google.com confirms that it looks good.

@ml...@google.com CYPTAL?

### ml...@chromium.org (2025-12-02)

Nice bug!

So, here's my thinking:

1. GC must keep liveness of JSArrayBuffer EPT handle + extension in sync. This is the bug that should be immediately fixed.
2. Multiple references of the same EPT entry to the AB::Extension. This seems fine if 1. is fixed.
3. Multiple different EPT entries to the same AB::Extension. Seems like a bug that can happen with corrupted handles (like in the exploit). As long as live EPT entries keep the AB::Extension alive this should be fine and likely crash on dead EPT entries that are either zapped in the GC due to not being alive or compaction.

### dx...@google.com (2025-12-18)

Project: v8/v8  

Branch:  main  

Author:  Michael Lippautz [mlippautz@chromium.org](mailto:mlippautz@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7268786>

[heap] Avoid double-read of handles in garbage collector

---


Expand for full commit details
```
     
    Some objects are marked behind their EPT entries: 
    - ArrayBufferExtension 
    - All CppHeap objects 
     
    Ensure that marking the table entry and the object happens from the 
    same handle. Otherwise, an attacker could swap handles and create a 
    state where handles are marked but their corresponding objects are 
    unmarked, leading to UAFs. 
     
    Bug: 464296297 
    Change-Id: I9612ea7b3b32e9f2e6d81f0540a271533ef945d3 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7268786 
    Reviewed-by: Omer Katz <omerkatz@chromium.org> 
    Reviewed-by: Samuel Groß <saelo@chromium.org> 
    Commit-Queue: Michael Lippautz <mlippautz@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#104398}

```

---

Files:

- M `src/heap/heap-write-barrier.cc`
- M `src/heap/marking-visitor-inl.h`
- M `src/heap/marking-visitor.h`
- M `src/heap/scavenger.cc`
- M `src/heap/sweeper.cc`
- M `src/heap/young-generation-marking-visitor-inl.h`
- M `src/heap/young-generation-marking-visitor.h`
- M `src/objects/js-array-buffer.cc`
- M `src/objects/js-array-buffer.h`
- M `src/objects/slots-inl.h`
- M `src/objects/slots.h`
- M `src/sandbox/cppheap-pointer-inl.h`

---

Hash: [a49bee15a2278070f339529a011e75f3a463bcd5](https://chromiumdash.appspot.com/commit/a49bee15a2278070f339529a011e75f3a463bcd5)  

Date: Wed Dec 17 17:28:30 2025


---

### dx...@google.com (2025-12-18)

Project: v8/v8  

Branch:  main  

Author:  Michael Lippautz [mlippautz@chromium.org](mailto:mlippautz@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7274342>

Revert "[heap] Avoid double-read of handles in garbage collector"

---


Expand for full commit details
```
     
    This reverts commit a49bee15a2278070f339529a011e75f3a463bcd5. 
     
    Reason for revert: Bunch of breakage. 
     
    Original change's description: 
    > [heap] Avoid double-read of handles in garbage collector 
    > 
    > Some objects are marked behind their EPT entries: 
    > - ArrayBufferExtension 
    > - All CppHeap objects 
    > 
    > Ensure that marking the table entry and the object happens from the 
    > same handle. Otherwise, an attacker could swap handles and create a 
    > state where handles are marked but their corresponding objects are 
    > unmarked, leading to UAFs. 
    > 
    > Bug: 464296297 
    > Change-Id: I9612ea7b3b32e9f2e6d81f0540a271533ef945d3 
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7268786 
    > Reviewed-by: Omer Katz <omerkatz@chromium.org> 
    > Reviewed-by: Samuel Groß <saelo@chromium.org> 
    > Commit-Queue: Michael Lippautz <mlippautz@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#104398} 
     
    Bug: 464296297 
    Fixed: 469997565,470009008,469985338,469996512,470038411,470034094,469996513,470039797,470027493,470027494,470040637,470039922 
    No-Presubmit: true 
    No-Tree-Checks: true 
    No-Try: true 
    Change-Id: Ie1f86f95a2a5900ecea31f9454efdec666c254c4 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7274342 
    Reviewed-by: Samuel Groß <saelo@chromium.org> 
    Commit-Queue: Samuel Groß <saelo@chromium.org> 
    Reviewed-by: Omer Katz <omerkatz@chromium.org> 
    Auto-Submit: Michael Lippautz <mlippautz@chromium.org> 
    Commit-Queue: Michael Lippautz <mlippautz@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#104419}

```

---

Files:

- M `src/heap/heap-write-barrier.cc`
- M `src/heap/marking-visitor-inl.h`
- M `src/heap/marking-visitor.h`
- M `src/heap/scavenger.cc`
- M `src/heap/sweeper.cc`
- M `src/heap/young-generation-marking-visitor-inl.h`
- M `src/heap/young-generation-marking-visitor.h`
- M `src/objects/js-array-buffer.cc`
- M `src/objects/js-array-buffer.h`
- M `src/objects/slots-inl.h`
- M `src/objects/slots.h`
- M `src/sandbox/cppheap-pointer-inl.h`

---

Hash: [ed2467e38b94f7d24a8817a3e3f16b269cbd8540](https://chromiumdash.appspot.com/commit/ed2467e38b94f7d24a8817a3e3f16b269cbd8540)  

Date: Thu Dec 18 17:21:22 2025


---

### dx...@google.com (2026-01-07)

Project: v8/v8  

Branch:  main  

Author:  Michael Lippautz [mlippautz@chromium.org](mailto:mlippautz@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7368074>

[heap] Avoid double-read of CppHeapPointerTable handles

---


Expand for full commit details
```
     
    Splits off the trivial CppHeap parts of http://crrev.com/c/7268786. 
     
    Ensure that marking the table entry and the object happens from the 
    same handle. Otherwise, an attacker could swap handles and create a 
    state where handles are marked but their corresponding objects are 
    unmarked, leading to UAFs. 
     
    Bug: 464296297 
    Change-Id: Id1ab0e92d31f5ca1337b63ab41acb86c8dd4900b 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7368074 
    Reviewed-by: Omer Katz <omerkatz@chromium.org> 
    Commit-Queue: Michael Lippautz <mlippautz@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#104526}

```

---

Files:

- M `src/heap/heap-write-barrier.cc`
- M `src/heap/marking-visitor-inl.h`
- M `src/heap/young-generation-marking-visitor-inl.h`
- M `src/objects/slots-inl.h`
- M `src/objects/slots.h`
- M `src/sandbox/cppheap-pointer-inl.h`

---

Hash: [b85c5419d1e291e216fb816d5f94c7cdff8928f9](https://chromiumdash.appspot.com/commit/b85c5419d1e291e216fb816d5f94c7cdff8928f9)  

Date: Wed Jan 7 15:48:36 2026


---

### dx...@google.com (2026-01-09)

Project: v8/v8  

Branch:  main  

Author:  Michael Lippautz [mlippautz@chromium.org](mailto:mlippautz@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7364011>

[heap] Avoid double-read of handles in garbage collector

---


Expand for full commit details
```
     
    Ensure that marking the table entry and the object happens from the 
    same handle. Otherwise, an attacker could swap handles and create a 
    state where handles are marked but their corresponding objects are 
    unmarked, leading to UAFs. 
     
    Since ArrayBufferExtension objects are themselves marked behind their 
    EPT entries we also need to properly publish the extension object. 
    This previously happened via acq/rel get/set pairs on the handle 
    stored in the AB itself. The CL unifies this approach with how CppHeap 
    objects are handled by introducing an initialization fence that is 
    only ever used for concurrent uses in the GC. The end result is fully 
    relaxed handling of handles and entries for both: ExternalPointerTable 
    and CppHeapPointerTable. 
     
    Bug: 464296297 
    Change-Id: I0c398a3d6dfdf230c19be2de39a8a309fd88b5c2 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7364011 
    Reviewed-by: Omer Katz <omerkatz@chromium.org> 
    Commit-Queue: Michael Lippautz <mlippautz@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#104606}

```

---

Files:

- M `src/heap/array-buffer-sweeper.cc`
- M `src/heap/marking-visitor-inl.h`
- M `src/heap/marking-visitor.h`
- M `src/heap/scavenger.cc`
- M `src/heap/sweeper.cc`
- M `src/heap/young-generation-marking-visitor-inl.h`
- M `src/heap/young-generation-marking-visitor.h`
- M `src/objects/js-array-buffer-inl.h`
- M `src/objects/js-array-buffer.cc`
- M `src/objects/js-array-buffer.h`
- M `src/objects/slots.h`

---

Hash: [f3bc9b98b34f481039a14fd8acc0a075bad8de9a](https://chromiumdash.appspot.com/commit/f3bc9b98b34f481039a14fd8acc0a075bad8de9a)  

Date: Thu Jan 8 13:37:26 2026


---

### dx...@google.com (2026-01-12)

Project: v8/v8  

Branch:  main  

Author:  Michael Achenbach [machenbach@chromium.org](mailto:machenbach@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7450458>

Revert "[heap] Avoid double-read of handles in garbage collector"

---


Expand for full commit details
```
     
    This reverts commit f3bc9b98b34f481039a14fd8acc0a075bad8de9a. 
     
    Reason for revert: Causes various issues, e.g.: 
    https://crbug.com/474809546 
    https://crbug.com/474424159 
     
    Original change's description: 
    > [heap] Avoid double-read of handles in garbage collector 
    > 
    > Ensure that marking the table entry and the object happens from the 
    > same handle. Otherwise, an attacker could swap handles and create a 
    > state where handles are marked but their corresponding objects are 
    > unmarked, leading to UAFs. 
    > 
    > Since ArrayBufferExtension objects are themselves marked behind their 
    > EPT entries we also need to properly publish the extension object. 
    > This previously happened via acq/rel get/set pairs on the handle 
    > stored in the AB itself. The CL unifies this approach with how CppHeap 
    > objects are handled by introducing an initialization fence that is 
    > only ever used for concurrent uses in the GC. The end result is fully 
    > relaxed handling of handles and entries for both: ExternalPointerTable 
    > and CppHeapPointerTable. 
    > 
    > Bug: 464296297 
    > Change-Id: I0c398a3d6dfdf230c19be2de39a8a309fd88b5c2 
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7364011 
    > Reviewed-by: Omer Katz <omerkatz@chromium.org> 
    > Commit-Queue: Michael Lippautz <mlippautz@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#104606} 
     
    Bug: 464296297 
    Change-Id: I3a4ff65554b669261ff3b51d39d218ee25a73edc 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7450458 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Reviewed-by: Omer Katz <omerkatz@chromium.org> 
    Commit-Queue: Michael Achenbach <machenbach@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#104629}

```

---

Files:

- M `src/heap/array-buffer-sweeper.cc`
- M `src/heap/marking-visitor-inl.h`
- M `src/heap/marking-visitor.h`
- M `src/heap/scavenger.cc`
- M `src/heap/sweeper.cc`
- M `src/heap/young-generation-marking-visitor-inl.h`
- M `src/heap/young-generation-marking-visitor.h`
- M `src/objects/js-array-buffer-inl.h`
- M `src/objects/js-array-buffer.cc`
- M `src/objects/js-array-buffer.h`
- M `src/objects/slots.h`

---

Hash: [4b61a58c7904a8c4891f044ca05270e79685b6cd](https://chromiumdash.appspot.com/commit/4b61a58c7904a8c4891f044ca05270e79685b6cd)  

Date: Mon Jan 12 09:38:32 2026


---

### dx...@google.com (2026-01-13)

Project: v8/v8  

Branch:  main  

Author:  Michael Lippautz [mlippautz@chromium.org](mailto:mlippautz@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7451938>

Reland "[heap] Avoid double-read of handles in garbage collector"

---


Expand for full commit details
```
     
    This is a reland of commit f3bc9b98b34f481039a14fd8acc0a075bad8de9a 
     
    The relanded fixes `--minor-ms` 32-bit builds which lacked visitor 
    support as it was #ifdef'ed away. 
     
    Original change's description: 
    > [heap] Avoid double-read of handles in garbage collector 
    > 
    > Ensure that marking the table entry and the object happens from the 
    > same handle. Otherwise, an attacker could swap handles and create a 
    > state where handles are marked but their corresponding objects are 
    > unmarked, leading to UAFs. 
    > 
    > Since ArrayBufferExtension objects are themselves marked behind their 
    > EPT entries we also need to properly publish the extension object. 
    > This previously happened via acq/rel get/set pairs on the handle 
    > stored in the AB itself. The CL unifies this approach with how CppHeap 
    > objects are handled by introducing an initialization fence that is 
    > only ever used for concurrent uses in the GC. The end result is fully 
    > relaxed handling of handles and entries for both: ExternalPointerTable 
    > and CppHeapPointerTable. 
    > 
    > Bug: 464296297 
    > Change-Id: I0c398a3d6dfdf230c19be2de39a8a309fd88b5c2 
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7364011 
    > Reviewed-by: Omer Katz <omerkatz@chromium.org> 
    > Commit-Queue: Michael Lippautz <mlippautz@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#104606} 
     
    Bug: 464296297 
    Change-Id: I480f963d248c6f88203b87347928cd672186d8c9 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7451938 
    Commit-Queue: Michael Lippautz <mlippautz@chromium.org> 
    Reviewed-by: Omer Katz <omerkatz@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#104669}

```

---

Files:

- M `src/heap/array-buffer-sweeper.cc`
- M `src/heap/marking-visitor-inl.h`
- M `src/heap/marking-visitor.h`
- M `src/heap/scavenger.cc`
- M `src/heap/sweeper.cc`
- M `src/heap/young-generation-marking-visitor-inl.h`
- M `src/heap/young-generation-marking-visitor.h`
- M `src/objects/js-array-buffer-inl.h`
- M `src/objects/js-array-buffer.cc`
- M `src/objects/js-array-buffer.h`
- M `src/objects/slots.h`

---

Hash: [83ac15dc368ce0d4d45cbcf7a0e3a358869dc0ec](https://chromiumdash.appspot.com/commit/83ac15dc368ce0d4d45cbcf7a0e3a358869dc0ec)  

Date: Mon Jan 12 11:32:25 2026


---

### sp...@google.com (2026-01-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $20000.00 for this report.

Rationale for this decision:
v8 sandbox bypass demonstrating controlled write


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### h3...@gmail.com (2026-01-29)

Thanks for the bounty :)

### ch...@google.com (2026-04-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> v8 sandbox bypass demonstrating controlled write

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/464296297)*
