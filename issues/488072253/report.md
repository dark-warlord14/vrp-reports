# V8 Sandbox escape via String::Value::Value unsigned overflow

| Field | Value |
|-------|-------|
| **Issue ID** | [488072253](https://issues.chromium.org/issues/488072253) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | h2...@gmail.com |
| **Assignee** | is...@chromium.org |
| **Created** | 2026-02-27 |
| **Bounty** | $5,000.00 |

## Description

VULNERABILITY DETAILS

The `String::Value` constructor stores the length of the incoming String object into its `length_` member, an `uint32_t`. Then it makes an allocation from PartitionAlloc for `length_ + 1`, which can overflow to zero if the length of the incoming String is UINT32\_MAX.

```
String::Value::Value(v8::Isolate* v8_isolate, v8::Local<v8::Value> obj)
    : str_(nullptr), length_(0) {
  if (obj.IsEmpty()) return;
  i::Isolate* i_isolate = reinterpret_cast<i::Isolate*>(v8_isolate);
  i::HandleScope scope(i_isolate);
  Local<Context> context = v8_isolate->GetCurrentContext();
  EnterV8BasicScope api_scope(i_isolate);
  TryCatch try_catch(v8_isolate);
  Local<String> str;
  if (!obj->ToString(context).ToLocal(&str)) return;
  length_ = str->Length();
  str_ = i::NewArray<uint16_t>(length_ + 1);
  str->WriteV2(v8_isolate, 0, length_, str_,
               String::WriteFlags::kNullTerminate);
}

```

This results in a zero-sized allocation, which PA turns into the smallest bucket size. Then `WriteV2` -> `WriteHelperV2` -> `String::WriteToFlat` proceeds to write into this undersized buffer. In the simplest case the copy will be for 4GB, see `(A)` below, which is what the PoC triggers. This should be exploitable by racing the copy from another thread.

The `ConsString` case (`(B)` below) is pretty complicated and might give more control over the write locations/lengths but I didn't explore this further.

```
// static
template <typename SinkCharT>
void String::WriteToFlat(Tagged<String> source, SinkCharT* sink, uint32_t start,
                         uint32_t length,
                         const SharedStringAccessGuardIfNeeded& access_guard) {
  DisallowGarbageCollection no_gc;
  if (length == 0) return;
  while (true) {
    DCHECK_GT(length, 0);
    DCHECK_LE(length, source->length());
    DCHECK_LT(start, source->length());
    DCHECK_LE(start + length, source->length());

    if (source->DispatchToSpecificType(absl::Overload{
            [&](Tagged<SeqOneByteString> str) {     // <----- (A)
              CopyChars(sink, str->GetChars(no_gc, access_guard) + start,
                        length);
              return true;
            },
            [&](Tagged<SeqTwoByteString> str) {
              CopyChars(sink, str->GetChars(no_gc, access_guard) + start,
                        length);
              return true;
            },
            [&](Tagged<ExternalOneByteString> str) {
              CopyChars(sink, str->GetChars() + start, length);
              return true;
            },
            [&](Tagged<ExternalTwoByteString> str) {
              CopyChars(sink, str->GetChars() + start, length);
              return true;
            },
            [&](Tagged<ConsString> cons_string) {   // <----- (B)
              Tagged<String> first = cons_string->first();
              uint32_t boundary = first->length();
              // Here we explicitly use signed ints as the values can become
              // negative. The sum of {first_length} and {second_length} is
              // always {length}, but the values can become negative, in which
              // case no characters of the respective string are needed.
              int32_t first_length = boundary - start;
              int32_t second_length = length - first_length;
              DCHECK_EQ(static_cast<uint32_t>(first_length + second_length),
                        length);
              if (second_length >= first_length) {
                DCHECK_GT(second_length, 0);
                // Right hand side is longer.  Recurse over left.
                if (first_length > 0) {
                  DCHECK_LT(first_length, length);
                  DCHECK_LT(second_length, length);

                  WriteToFlat(first, sink, start, first_length, access_guard);
                  if (start == 0 && cons_string->second() == first) {
                    DCHECK_LE(boundary * 2, length);
                    CopyChars(sink + boundary, sink, boundary);
                    return true;
                  }
                  sink += first_length;
                  start = 0;
                  length -= first_length;
                } else {
                  start -= boundary;
                }
                source = cons_string->second();
              } else {
                DCHECK_GT(first_length, 0);
                // Left hand side is longer.  Recurse over right.
                if (second_length > 0) {
                  DCHECK_LT(first_length, length);
                  DCHECK_LT(second_length, length);

                  uint32_t second_start = first_length;
                  DCHECK_EQ(second_start + second_length, length);
                  Tagged<String> second = cons_string->second();
                  // When repeatedly appending to a string, we get a cons string
                  // that is unbalanced to the left, a list, essentially.  We
                  // inline the common case of sequential one-byte right child.
                  if (second_length == 1) {
                    sink[second_start] =
                        static_cast<SinkCharT>(second->Get(0, access_guard));
                  } else if (IsSeqOneByteString(second)) {
                    CopyChars(sink + second_start,
                              Cast<SeqOneByteString>(second)->GetChars(
                                  no_gc, access_guard),
                              second_length);
                  } else {
                    WriteToFlat(second, sink + second_start, 0, second_length,
                                access_guard);
                  }
                  length -= second_length;
                }
                source = first;
              }
              return length == 0;
            },
            [&](Tagged<SlicedString> slice) {
              uint32_t offset = slice->offset();
              source = slice->parent();
              start += offset;
              return false;
            },
            [&](Tagged<ThinString> thin_string) {
              source = thin_string->actual();
              return false;
            }})) {
      return;
    }
  }
  UNREACHABLE();
}

```

Currently there's no way to reach this through d8 as far as I can tell, a full chromium build is needed. The only call path that is viable is through `V8Initializer::CodeGenerationCheckCallbackInMainThread`, called for `eval` expressions. In `CodeGenerationCheckCallbackInMainThread`, `source` is the script to eval. We cannot pre-corrupt the string length because that causes `TrustedTypesCodeGenerationCheck` to fail. So we need to race the window between `TrustedTypesCodeGenerationCheck` and the vulnerable call (`ContentSecurityPolicyCodeGenerationCheck` -> `ToBlinkString` -> `String::Value::Value`). To make reproduction easier, I've attached `sleep.patch`, which inserts a sleep of three seconds at the right place, during which the PoC changes the String length to UINT32\_MAX.

Since the vulnerability is in a directly exposed external V8 API, other embedders may contain easier to exploit calls to it.

```
// static
v8::ModifyCodeGenerationFromStringsResult
V8Initializer::CodeGenerationCheckCallbackInMainThread(
    v8::Local<v8::Context> context,
    v8::Local<v8::Value> source,
    bool is_code_like) {
  // The code generation callback should only be installed on "normal" JS
  // contexts, which in turn should always have an associated ExecutionContext.
  // If this invariant holds, we can simplify this code a little bit.
  // We're probing this invariant to ensure it won't cause issues in practice.
  // See also: Discussion on crrev.com/c/7207201.
  CHECK(ToExecutionContext(context), base::NotFatalUntil::M150);

  // The TC39 "Dynamic Code Brand Check" feature is currently behind a flag.
  if (!RuntimeEnabledFeatures::TrustedTypesUseCodeLikeEnabled())
    is_code_like = false;

  // With Trusted Types, we always run the TT check first because of reporting,
  // and because a default policy might want to stringify or modify the original
  // source. When TT enforcement is disabled, codegen is always allowed, and we
  // just use the check to stringify any trusted type source.
  bool codegen_allowed_by_tt = false;
  v8::MaybeLocal<v8::String> stringified_source;
  std::tie(codegen_allowed_by_tt, stringified_source) =
      TrustedTypesCodeGenerationCheck(context, source, is_code_like);

  if (!codegen_allowed_by_tt) {
    return {false, v8::MaybeLocal<v8::String>()};
  }

  if (stringified_source.IsEmpty()) {
    return {true, v8::MaybeLocal<v8::String>()};
  }

  if (!ContentSecurityPolicyCodeGenerationCheck(
          context, stringified_source.ToLocalChecked())) {
    return {false, v8::MaybeLocal<v8::String>()};
  }

  return {true, std::move(stringified_source)};
}

```

Bisecting this traces back to before 2011 but of course this only became a potential issue with the threat model of the sandbox.

A possible fix is attached as fix.patch:

```
diff --git a/src/api/api.cc b/src/api/api.cc
index d2e1e292be0..0248142e162 100644
--- a/src/api/api.cc
+++ b/src/api/api.cc
@@ -11135,6 +11135,7 @@ String::Value::Value(v8::Isolate* v8_isolate, v8::Local<v8::Value> obj)
   Local<String> str;
   if (!obj->ToString(context).ToLocal(&str)) return;
   length_ = str->Length();
+  SBXCHECK_LT(length_, i::String::kMaxLength);
   str_ = i::NewArray<uint16_t>(length_ + 1);
   str->WriteV2(v8_isolate, 0, length_, str_,
                String::WriteFlags::kNullTerminate);

```

VERSION
Chrome Version: 147.0.7698.0 + dev (commit e2c8bc584d4b48c026ea27f8dac55b6b787b4ca8)
Operating System: Linux

REPRODUCTION CASE

To reproduce:

- apply `sleep.patch` and build with the GN args below
- have `server.py` and `poc_chrome_eval.html` in the same directory
- start server.py (needed for CSP headers) and run chrome as follows

```
# Start HTTP server
python3 server.py &

# Run Chrome with sandbox testing API
# cd $CHROME_OUT_DIR
./chrome --no-sandbox --js-flags="--sandbox-testing" \
  --headless --disable-gpu --enable-logging=stderr \
  http://127.0.0.1:8080/poc_chrome_eval.html

```

GN args used for testing:

```
is_debug = false
treat_warnings_as_errors = false
symbol_level = 2
dcheck_always_on = false
is_asan = true
is_component_build = false
v8_enable_memory_corruption_api = true
v8_enable_sandbox = true
v8_enable_disassembler = true
v8_enable_object_print = true

```

It should result in the following crash:

```
==9698==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x776f3ca43c50 at pc 0x5b9f98b49faf bp 0x7ffde36cfa50 sp 0x7ffde36cfa48
WRITE of size 16 at 0x776f3ca43c50 thread T0 (chrome)
    #0 0x5b9f98b49fae in void v8::internal::CopyChars<unsigned char, unsigned short>(unsigned short*, unsigned char const*, unsigned long) gen/third_party/libc++/src/include/__algorithm/copy.h:51:17
    #1 0x5b9f99e02ec7 in void v8::internal::String::WriteToFlat<unsigned short>(v8::internal::Tagged<v8::internal::String>, unsigned short*, unsigned int, unsigned int) v8/src/objects/string.cc:776:10
    #2 0x5b9f98b056c3 in v8::String::Value::Value(v8::Isolate*, v8::Local<v8::Value>) v8/src/api/api.cc:5871:3
    #3 0x5b9fb6ad956f in blink::V8Initializer::CodeGenerationCheckCallbackInMainThread(v8::Local<v8::Context>, v8::Local<v8::Value>, bool) third_party/blink/renderer/bindings/core/v8/v8_initializer.cc:159:21
    #4 0x5b9f98d2f71e in v8::internal::Compiler::ValidateDynamicCompilationSource(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::NativeContext>, v8::internal::Handle<v8::internal::Object>, bool) v8/src/codegen/compiler.cc:3460:7
    #5 0x5b9f9a1ff69a in v8::internal::CompileGlobalEval(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::SharedFunctionInfo>, v8::internal::LanguageMode, int, int) v8/src/runtime/runtime-compiler.cc:747:38
    #6 0x5b9f9a1fa52f in v8::internal::Runtime_ResolvePossiblyDirectEval(int, unsigned long*, v8::internal::Isolate*) v8/src/runtime/runtime-compiler.cc:800:10
    #7 0x5b9f9db6ce70 in Builtins_CEntry_Return1_ArgvInRegister_NoBuiltinExit setup-isolate-deserialize.cc
    #8 0x5b9f9dc75b07 in Builtins_CallRuntimeHandler setup-isolate-deserialize.cc
    #9 0x5b9f9dabb83b in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #10 0x5b9f9dab85db in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #11 0x5b9f9dab832a in Builtins_JSEntry setup-isolate-deserialize.cc
    #12 0x5b9f98f8bb5a in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/simulator.h:216:12
    #13 0x5b9f98f8a412 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>, v8::base::Vector<v8::internal::DirectHandle<v8::internal::Object> const>) v8/src/execution/execution.cc:532:10
    #14 0x5b9f98acaf99 in v8::Function::Call(v8::Isolate*, v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) v8/src/api/api.cc:5582:27
    #15 0x5b9fb6b21c58 in blink::V8ScriptRunner::CallFunction(v8::Local<v8::Function>, blink::ExecutionContext*, v8::Local<v8::Value>, int, v8::Local<v8::Value>*, v8::Isolate*) third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:855:48
    #16 0x5b9fbc127df6 in blink::bindings::CallbackInvokeHelper<blink::CallbackFunctionBase, (blink::bindings::CallbackInvokeHelperMode)0, (blink::bindings::CallbackReturnTypeIsPromise)0>::Call(int, v8::Local<v8::Value>*) third_party/blink/renderer/bindings/core/v8/callback_invoke_helper.cc:126:12
    #17 0x5b9fbc13dfc5 in blink::V8Function::Invoke(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::BasicHeapVector<(blink::internal::HeapCollectionType)1, blink::ScriptValue, 0u> const&) gen/third_party/blink/renderer/bindings/core/v8/v8_function.cc:73:13
    #18 0x5b9fbc13e729 in blink::V8Function::InvokeAndReportException(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::BasicHeapVector<(blink::internal::HeapCollectionType)1, blink::ScriptValue, 0u> const&) gen/third_party/blink/renderer/bindings/core/v8/v8_function.cc:133:15
    #19 0x5b9fbced92c0 in blink::ScheduledAction::Execute(blink::ExecutionContext*) third_party/blink/renderer/core/scheduler/scheduled_action.cc:145:18
    #20 0x5b9fbced1274 in blink::DOMTimer::Fired() third_party/blink/renderer/core/scheduler/dom_timer.cc:446:11
    #21 0x5b9fbb0c666d in blink::TimerBase::RunInternal() third_party/blink/renderer/platform/timer.cc:166:3
    #22 0x5b9fb6a88f00 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::TimerBase::*&&)(), blink::TimerBase*>, base::internal::BindState<true, true, false, void (blink::TimerBase::*)(), blink::UnretainedWrapper<blink::TimerBase>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #23 0x5b9faa697276 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #24 0x5b9faa70e829 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #25 0x5b9faa70d69a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #26 0x5b9faa557d39 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #27 0x5b9faa70ff37 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #28 0x5b9faa612550 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #29 0x5b9fb69b36ce in content::RendererMain(content::MainFunctionParams) content/renderer/renderer_main.cc:364:16
    #30 0x5b9fa633d4ef in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:664:14
    #31 0x5b9fa633e830 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:771:12
    #32 0x5b9fa6341548 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1152:10
    #33 0x5b9fa633af01 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:358:36
    #34 0x5b9fa633b4fc in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:371:10
    #35 0x5b9f930ee269 in ChromeMain chrome/app/chrome_main.cc:191:12
    #36 0x7b4f3e5fc1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #37 0x7b4f3e5fc28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #38 0x5b9f93011029 in _start (/mnt/nvme2t/build/chromium/src/out/asan-rel-x64/chrome+0x10ceb029) (BuildId: c6f02595c62be34e)

0x776f3ca43c51 is located 0 bytes after 1-byte region [0x776f3ca43c50,0x776f3ca43c51)
allocated by thread T0 (chrome) here:
    #0 0x5b9f930ece3d in operator new[](unsigned long, std::nothrow_t const&) (/mnt/nvme2t/build/chromium/src/out/asan-rel-x64/chrome+0x10dc6e3d) (BuildId: c6f02595c62be34e)
    #1 0x5b9f98b055d0 in v8::String::Value::Value(v8::Isolate*, v8::Local<v8::Value>) v8/src/utils/allocation.h:44:15
    #2 0x5b9fb6ad956f in blink::V8Initializer::CodeGenerationCheckCallbackInMainThread(v8::Local<v8::Context>, v8::Local<v8::Value>, bool) third_party/blink/renderer/bindings/core/v8/v8_initializer.cc:159:21
    #3 0x5b9f98d2f71e in v8::internal::Compiler::ValidateDynamicCompilationSource(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::NativeContext>, v8::internal::Handle<v8::internal::Object>, bool) v8/src/codegen/compiler.cc:3460:7
    #4 0x5b9f9a1ff69a in v8::internal::CompileGlobalEval(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::SharedFunctionInfo>, v8::internal::LanguageMode, int, int) v8/src/runtime/runtime-compiler.cc:747:38
    #5 0x5b9f9a1fa52f in v8::internal::Runtime_ResolvePossiblyDirectEval(int, unsigned long*, v8::internal::Isolate*) v8/src/runtime/runtime-compiler.cc:800:10
    #6 0x5b9f9db6ce70 in Builtins_CEntry_Return1_ArgvInRegister_NoBuiltinExit setup-isolate-deserialize.cc
    #7 0x5b9f9dc75b07 in Builtins_CallRuntimeHandler setup-isolate-deserialize.cc
    #8 0x5b9f9dabb83b in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #9 0x5b9f9dab85db in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #10 0x5b9f9dab832a in Builtins_JSEntry setup-isolate-deserialize.cc
    #11 0x5b9f98f8bb5a in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/simulator.h:216:12
    #12 0x5b9f98f8a412 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>, v8::base::Vector<v8::internal::DirectHandle<v8::internal::Object> const>) v8/src/execution/execution.cc:532:10
    #13 0x5b9f98acaf99 in v8::Function::Call(v8::Isolate*, v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) v8/src/api/api.cc:5582:27
    #14 0x5b9fb6b21c58 in blink::V8ScriptRunner::CallFunction(v8::Local<v8::Function>, blink::ExecutionContext*, v8::Local<v8::Value>, int, v8::Local<v8::Value>*, v8::Isolate*) third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:855:48
    #15 0x5b9fbc127df6 in blink::bindings::CallbackInvokeHelper<blink::CallbackFunctionBase, (blink::bindings::CallbackInvokeHelperMode)0, (blink::bindings::CallbackReturnTypeIsPromise)0>::Call(int, v8::Local<v8::Value>*) third_party/blink/renderer/bindings/core/v8/callback_invoke_helper.cc:126:12
    #16 0x5b9fbc13dfc5 in blink::V8Function::Invoke(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::BasicHeapVector<(blink::internal::HeapCollectionType)1, blink::ScriptValue, 0u> const&) gen/third_party/blink/renderer/bindings/core/v8/v8_function.cc:73:13
    #17 0x5b9fbc13e729 in blink::V8Function::InvokeAndReportException(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::BasicHeapVector<(blink::internal::HeapCollectionType)1, blink::ScriptValue, 0u> const&) gen/third_party/blink/renderer/bindings/core/v8/v8_function.cc:133:15
    #18 0x5b9fbced92c0 in blink::ScheduledAction::Execute(blink::ExecutionContext*) third_party/blink/renderer/core/scheduler/scheduled_action.cc:145:18
    #19 0x5b9fbced1274 in blink::DOMTimer::Fired() third_party/blink/renderer/core/scheduler/dom_timer.cc:446:11
    #20 0x5b9fbb0c666d in blink::TimerBase::RunInternal() third_party/blink/renderer/platform/timer.cc:166:3
    #21 0x5b9fb6a88f00 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::TimerBase::*&&)(), blink::TimerBase*>, base::internal::BindState<true, true, false, void (blink::TimerBase::*)(), blink::UnretainedWrapper<blink::TimerBase>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #22 0x5b9faa697276 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #23 0x5b9faa70e829 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #24 0x5b9faa70d69a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #25 0x5b9faa557d39 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #26 0x5b9faa70ff37 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #27 0x5b9faa612550 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #28 0x5b9fb69b36ce in content::RendererMain(content::MainFunctionParams) content/renderer/renderer_main.cc:364:16
    #29 0x5b9fa633d4ef in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:664:14

SUMMARY: AddressSanitizer: heap-buffer-overflow gen/third_party/libc++/src/include/__algorithm/copy.h:51:17 in void v8::internal::CopyChars<unsigned char, unsigned short>(unsigned short*, unsigned char const*, unsigned long)
Shadow bytes around the buggy address:
  0x776f3ca43980: f7 fa fd fd f7 fa fd fa f7 fa fd fa f7 fa fd fa
  0x776f3ca43a00: f7 fa fd fa f7 fa fd fd f7 fa fd fa f7 fa 00 fa
  0x776f3ca43a80: f7 fa fd fa f7 fa 00 fa f7 fa fd fd f7 fa fd fa
  0x776f3ca43b00: f7 fa fd fa f7 fa fd fa f7 fa fd fd f7 fa 00 fa
  0x776f3ca43b80: f7 fa fd fa f7 fa 00 00 f7 fa fd fa f7 fa 00 fa
=>0x776f3ca43c00: f7 fa 00 fa f7 fa 00 00 f7 fa[fa]fa fa fa fa fa
  0x776f3ca43c80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x776f3ca43d00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x776f3ca43d80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x776f3ca43e00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x776f3ca43e80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

==9698==ADDITIONAL INFO

==9698==Note: Please include this section with the ASan report.
Task trace:
    #0 0x5b9fbced0351 in blink::DOMTimer::DOMTimer(blink::ExecutionContext&, blink::ScheduledAction*, base::TimeDelta, bool) third_party/blink/renderer/core/scheduler/dom_timer.cc:343:27
    #1 0x5b9fae363567 in IPC::ChannelAssociatedGroupController::Accept(mojo::Message*) ipc/ipc_mojo_bootstrap.cc:1138:13


Command line: `/proc/self/exe --type=renderer --crashpad-handler-pid=9637 --enable-crash-reporter=, --noerrdialogs --user-data-dir=/tmp/org.chromium.Chromium.scoped_dir.hcFh4O --change-stack-guard-on-fork=enable --no-sandbox --js-flags=--sandbox-testing --ozone-platform=headless --disable-gpu-compositing --lang=en-US --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=5 --time-ticks-at-unix-epoch=-1771874696213936 --launch-time-ticks=312902948923 --shared-files=v8_context_snapshot_data:100 --field-trial-handle=3,i,9094350496089913423,14442727610721306758,262144 --disable-features=PaintHolding --variations-seed-version --pseudonymization-salt-handle=7,i,4360479699736406988,12489524335107657548,4 --trace-process-track-uuid=3190708990997080739 --enable-logging=stderr`


==9698==END OF ADDITIONAL INFO

==9698==ABORTING

```

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: Sandbox violation

CREDIT INFORMATION
Reporter credit: TFGC

## Attachments

- [fix.patch](attachments/fix.patch) (text/x-diff, 518 B)
- [poc_chrome_eval.html](attachments/poc_chrome_eval.html) (text/html, 4.7 KB)
- [server.py](attachments/server.py) (text/x-python, 1.5 KB)
- [sleep.patch](attachments/sleep.patch) (text/x-diff, 1.0 KB)

## Timeline

### aj...@google.com (2026-02-28)

This indeed crashes in an asan build of chrome - I'm not sure if this counts as a v8 sandbox escape at this time so I'll let the v8 folks have a look.

### md...@google.com (2026-03-02)

Assigning to Igor as this is about sandbox and traces back long ago.

### is...@chromium.org (2026-03-05)

Thank you for the report.

This is a legitimate issue with a low exploitability. In practice, we'll hit a segfault while copying 4GB of data either in source V8 heap memory when we'll reach unmapped guard page after the main cage or when writing out of bounds to the C++ heap.

I think we should take an opportunity and also move forward with [deprecation](https://source.chromium.org/chromium/chromium/src/+/main:v8/include/v8-primitive.h?q=%22Prefer%20using%20String::ValueView%20if%20you%20can,%20or%20string-%3EWrite%20to%20a%20%22&ss=chromium) of `String::Value` (there's only one usage left in Blink).

### dx...@google.com (2026-03-06)

Project: chromium/src  

Branch:  main  

Author:  Igor Sheludko [ishell@chromium.org](mailto:ishell@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7642663>

[v8] Fix blink::ToBlinkString(..) to avoid double copying

---


Expand for full commit details
```
     
    ... and using soon to be deprecated v8::String::Value. 
     
    Bug: 488072253 
    Change-Id: I1e146f7c1d583fdfee50f52bd9ac444f2fe90c7d 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7642663 
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    Commit-Queue: Igor Sheludko <ishell@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1595501}

```

---

Files:

- M `third_party/blink/renderer/bindings/core/v8/v8_initializer.cc`

---

Hash: [22eda405aefa1537ec402d1682865ecc563ed4af](https://chromiumdash.appspot.com/commit/22eda405aefa1537ec402d1682865ecc563ed4af)  

Date: Fri Mar 6 18:28:24 2026


---

### dx...@google.com (2026-03-08)

Project: v8/v8  

Branch:  main  

Author:  Igor Sheludko [ishell@chromium.org](mailto:ishell@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7642803>

[api] Advance deprecation of v8::String::Value::Value(..)

---


Expand for full commit details
```
     
    ... and start deprecation of v8::String::Value class. 
     
    Fixed: 488072253 
    Change-Id: I19c281a08b7ab43e513a60ec60d2a270ae0163e2 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7642803 
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    Commit-Queue: Igor Sheludko <ishell@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105658}

```

---

Files:

- M `include/v8-primitive.h`
- M `src/api/api.cc`

---

Hash: [052267577cfd242e77a35b03f320dc1b6374c60d](https://chromiumdash.appspot.com/commit/052267577cfd242e77a35b03f320dc1b6374c60d)  

Date: Fri Mar 6 11:57:45 2026


---

### ch...@google.com (2026-06-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
V8 sandbox bypass.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/488072253)*
