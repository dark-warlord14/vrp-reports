# type confusion between ScriptWrappable and EventTarget by StorageManager

| Field | Value |
|-------|-------|
| **Issue ID** | [375317755](https://issues.chromium.org/issues/375317755) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P1 |
| **Component** | Blink>Storage |
| **Platforms** | Linux, Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | es...@chromium.org |
| **Created** | 2024-10-24 |
| **Bounty** | $3,000.00 |

## Description

# Reproduce

asan-win32-release\_x64-1371981

1. chrome --no-sandbox --user-data-dir=test poc.html

# Bisect

<https://chromium-review.googlesource.com/c/chromium/src/+/5930607>

# RCA

StorageManager is defined as a ScriptWrappable[1] object in the code, but as a EventTarget[2] object in the IDL file, leading to type confusion.

```
1. https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/quota/storage_manager.h;drc=9a450718fb4d6d0178d1201d9d7ee2224fb84624;l=22
class StorageManager final : public ScriptWrappable {
  DEFINE_WRAPPERTYPEINFO();

 public:
___CUT___

2. https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/quota/storage_manager.idl;drc=9a450718fb4d6d0178d1201d9d7ee2224fb84624;l=10
[
    SecureContext,
    Exposed=(Window,Worker)
] interface StorageManager : EventTarget {
    [CallWith=ScriptState, MeasureAs=DurableStoragePersisted, RaisesException] Promise<boolean> persisted();
    [Exposed=Window, CallWith=ScriptState, MeasureAs=DurableStoragePersist, RaisesException] Promise<boolean> persist();

    [CallWith=ScriptState, MeasureAs=DurableStorageEstimate, RaisesException] Promise<StorageEstimate> estimate();
};

```
# Asan

```
=================================================================
==9284==ERROR: AddressSanitizer: global-buffer-overflow on address 0x7ffaf68472d0 at pc 0x7ffadfd91bb1 bp 0x00a1531f6ce0 sp 0x00a1531f6d28
READ of size 8 at 0x7ffaf68472d0 thread T0
    #0 0x7ffadfd91bb0 in blink::IsValidSource C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\events\message_event.cc:45
    #1 0x7ffadfd91bb0 in blink::MessageEvent::Create(class WTF::AtomicString const &, class blink::MessageEventInit const *, class blink::ExceptionState &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\events\message_event.cc:206:33
    #2 0x7ffae422d6ba in blink::`anonymous namespace'::v8_message_event::ConstructorCallback C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\bindings\core\v8\v8_message_event.cc:276:23
    #3 0x7ffac81aa678 in v8::internal::FunctionCallbackArguments::CallOrConstruct(class v8::internal::Tagged<class v8::internal::FunctionTemplateInfo>, bool) C:\b\s\w\ir\cache\builder\src\v8\src\api\api-arguments-inl.h:95:3
    #4 0x7ffac81a87d7 in v8::internal::`anonymous namespace'::HandleApiCallHelper<1> C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:108:36
    #5 0x7ffac81a6674 in v8::internal::Builtin_Impl_HandleApiConstruct C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:139:3
    #6 0x7ffac81a6024 in v8::internal::Builtin_HandleApiConstruct(int, unsigned __int64 *, class v8::internal::Isolate *) C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:130:1
    #7 0x7ffaead3e9b9 in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit (E:\chrome_asan\asan-win32-release_x64-1371981\chrome.dll+0x1a773e9b9)
    #8 0x7ffaeac9aa72 in Builtins_InterpreterPushArgsThenFastConstructFunction (E:\chrome_asan\asan-win32-release_x64-1371981\chrome.dll+0x1a769aa72)
    #9 0x7ffaeae31ee6 in Builtins_ConstructHandler (E:\chrome_asan\asan-win32-release_x64-1371981\chrome.dll+0x1a7831ee6)
    #10 0x7ffaeac99f8a in Builtins_InterpreterEntryTrampoline (E:\chrome_asan\asan-win32-release_x64-1371981\chrome.dll+0x1a7699f8a)
    #11 0x7ffaeac97b1b in Builtins_JSEntryTrampoline (E:\chrome_asan\asan-win32-release_x64-1371981\chrome.dll+0x1a7697b1b)
    #12 0x7ffaeac97672 in Builtins_JSEntry (E:\chrome_asan\asan-win32-release_x64-1371981\chrome.dll+0x1a7697672)
    #13 0x7ffac8652a28 in v8::internal::GeneratedCode<unsigned long long,unsigned long long,unsigned long long,unsigned long long,unsigned long long,long long,unsigned long long **>::Call C:\b\s\w\ir\cache\builder\src\v8\src\execution\simulator.h:191
    #14 0x7ffac8652a28 in v8::internal::`anonymous namespace'::Invoke C:\b\s\w\ir\cache\builder\src\v8\src\execution\execution.cc:420:22
    #15 0x7ffac8655564 in v8::internal::Execution::CallScript(class v8::internal::Isolate *, class v8::internal::Handle<class v8::internal::JSFunction>, class v8::internal::Handle<class v8::internal::Object>, class v8::internal::Handle<class v8::internal::Object>) C:\b\s\w\ir\cache\builder\src\v8\src\execution\execution.cc:517:10
    #16 0x7ffac80755ca in v8::Script::Run(class v8::Local<class v8::Context>, class v8::Local<class v8::Data>) C:\b\s\w\ir\cache\builder\src\v8\src\api\api.cc:2140:7
    #17 0x7ffadbe3c079 in blink::V8ScriptRunner::RunCompiledScript(class v8::Isolate *, class v8::Local<class v8::Script>, class v8::Local<class v8::Data>, class blink::ExecutionContext *) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\bindings\core\v8\v8_script_runner.cc:517:22
    #18 0x7ffadbe3d974 in blink::V8ScriptRunner::CompileAndRunScript(class blink::ScriptState *, class blink::ClassicScript *, enum blink::ExecuteScriptPolicy, class blink::V8ScriptRunner::RethrowErrorsOption) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\bindings\core\v8\v8_script_runner.cc:644:22
    #19 0x7ffadbde52d5 in blink::ClassicScript::RunScriptOnScriptStateAndReturnValue(class blink::ScriptState *, enum blink::ExecuteScriptPolicy, class blink::V8ScriptRunner::RethrowErrorsOption) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\script\classic_script.cc:225:10
    #20 0x7ffadbde6452 in blink::Script::RunScriptOnScriptState(class blink::ScriptState *, enum blink::ExecuteScriptPolicy, class blink::V8ScriptRunner::RethrowErrorsOption) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\script\script.cc:35:17
    #21 0x7ffadbde6813 in blink::Script::RunScript(class blink::LocalDOMWindow *, enum blink::ExecuteScriptPolicy, class blink::V8ScriptRunner::RethrowErrorsOption) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\script\script.cc:42:3
    #22 0x7ffae44b1bef in blink::PendingScript::ExecuteScriptBlockInternal(class blink::Script *, class blink::ScriptElementBase *, bool, bool, bool, class base::TimeTicks, bool) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\script\pending_script.cc:293:13
    #23 0x7ffae44b0688 in blink::PendingScript::ExecuteScriptBlock(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\script\pending_script.cc:190:3
    #24 0x7ffadffa63e5 in blink::ScriptLoader::PrepareScript(enum blink::ScriptLoader::ParserBlockingInlineOption, class WTF::TextPosition const &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\script\script_loader.cc:1302:60
    #25 0x7ffae4968af9 in blink::HTMLParserScriptRunner::ProcessScriptElementInternal(class blink::Element *, class WTF::TextPosition const &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\script\html_parser_script_runner.cc:494:52
    #26 0x7ffae496831a in blink::HTMLParserScriptRunner::ProcessScriptElement(class blink::Element *, class WTF::TextPosition const &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\script\html_parser_script_runner.cc:288:3
    #27 0x7ffae029804b in blink::HTMLDocumentParser::RunScriptsForPausedTreeBuilder(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc:680:21
    #28 0x7ffae0293a93 in blink::HTMLDocumentParser::CanTakeNextToken C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.h:192
    #29 0x7ffae0293a93 in blink::HTMLDocumentParser::PumpTokenizer(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc:750:36
    #30 0x7ffae0291e3e in blink::HTMLDocumentParser::PumpTokenizerIfPossible(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc:642:15
    #31 0x7ffae02927a2 in blink::HTMLDocumentParser::DeferredPumpTokenizerIfPossible(bool, class base::TimeTicks) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc:625:7
    #32 0x7ffae02b19d5 in base::internal::DecayedFunctorTraits<void (blink::HTMLDocumentParser::*)(bool, base::TimeTicks),cppgc::internal::BasicPersistent<blink::HTMLDocumentParser,cppgc::internal::StrongPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy> &&,bool &&,base::TimeTicks &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:738
    #33 0x7ffae02b19d5 in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (blink::HTMLDocumentParser::*&&)(bool, base::TimeTicks),cppgc::internal::BasicPersistent<blink::HTMLDocumentParser,cppgc::internal::StrongPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy> &&,bool &&,base::TimeTicks &&>,void,0,1,2>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:930
    #34 0x7ffae02b19d5 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::HTMLDocumentParser::*&&)(bool, base::TimeTicks),cppgc::internal::BasicPersistent<blink::HTMLDocumentParser,cppgc::internal::StrongPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy> &&,bool &&,base::TimeTicks &&>,base::internal::BindState<1,1,0,void (blink::HTMLDocumentParser::*)(bool, base::TimeTicks),cppgc::internal::BasicPersistent<blink::HTMLDocumentParser,cppgc::internal::StrongPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy>,bool,base::TimeTicks>,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1067
    #35 0x7ffae02b19d5 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl blink::HTMLDocumentParser::*&&)(bool, class base::TimeTicks), class cppgc::internal::BasicPersistent<class blink::HTMLDocumentParser, struct cppgc::internal::StrongPersistentPolicy, class cppgc::internal::IgnoreLocationPolicy, class cppgc::internal::DisabledCheckingPolicy> &&, bool &&, class base::TimeTicks &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl blink::HTMLDocumentParser::*)(bool, class base::TimeTicks), class cppgc::internal::BasicPersistent<class blink::HTMLDocumentParser, struct cppgc::internal::StrongPersistentPolicy, class cppgc::internal::IgnoreLocationPolicy, class cppgc::internal::DisabledCheckingPolicy>, bool, class base::TimeTicks>, (void)>::RunOnce(class base::internal::BindStateBase *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980:12
    #36 0x7ffad4186b60 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
    #37 0x7ffad4186b60 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:202:34
    #38 0x7ffad90b1654 in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h:98
    #39 0x7ffad90b1654 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::LazyNow *) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:471:23
    #40 0x7ffad90b03a9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:332:40
    #41 0x7ffad90f53de in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:40:55
    #42 0x7ffad90b334f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:641:12
    #43 0x7ffad41e206e in base::RunLoop::Run(class base::Location const &) C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:133:14
    #44 0x7ffad810ef4a in content::RendererMain(struct content::MainFunctionParams) C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:361:16
    #45 0x7ffad1fed831 in content::RunOtherNamedProcessTypeMain(class std::__Cr::basic_string<char, struct std::__Cr::char_traits<char>, class std::__Cr::allocator<char>> const &, struct content::MainFunctionParams, class content::ContentMainDelegate *) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:795:14
    #46 0x7ffad1fefa8f in content::ContentMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1164:10
    #47 0x7ffad1fe4095 in content::RunContentProcess(struct content::ContentMainParams, class content::ContentMainRunner *) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:356:36
    #48 0x7ffad1fe4c3d in content::ContentMain(struct content::ContentMainParams) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:369:10
    #49 0x7ffac36016b0 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:231:12
    #50 0x7ff6cc1c438d in MainDllLoader::Launch(struct HINSTANCE__*, class base::TimeTicks) C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:201:12
    #51 0x7ff6cc1c200c in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:351:20
    #52 0x7ff6cc5debfb in invoke_main D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:78
    #53 0x7ff6cc5debfb in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #54 0x7ffb534f257c  (C:\WINDOWS\System32\KERNEL32.DLL+0x18001257c)
    #55 0x7ffb5516af07  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18005af07)

0x7ffaf68472d0 is located 16 bytes before global variable 'char const *const blink::`anonymous namespace'::kUniqueOriginErrorMessage' defined in '../../third_party/blink/renderer/modules/quota/storage_manager.cc' (0x7ffaf68472e0) of size 48
  'char const *const blink::`anonymous namespace'::kUniqueOriginErrorMessage' is ascii string 'The operation is not supported in this context.'
0x7ffaf68472d0 is located 24 bytes after global variable 'const blink::StorageManager::`vftable'' defined in '../../third_party/blink/renderer/modules/quota/storage_manager.cc' (0x7ffaf6847280) of size 56
SUMMARY: AddressSanitizer: global-buffer-overflow C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\events\message_event.cc:45 in blink::IsValidSource
Shadow bytes around the buggy address:
  0x7ffaf6847000: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ffaf6847080: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ffaf6847100: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ffaf6847180: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ffaf6847200: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7ffaf6847280: 00 00 00 00 00 00 00 f9 f9 f9[f9]f9 00 00 00 00
  0x7ffaf6847300: 00 00 f9 f9 f9 f9 f9 f9 00 00 00 00 00 00 00 00
  0x7ffaf6847380: 02 f9 f9 f9 f9 f9 f9 f9 00 00 00 00 02 f9 f9 f9
  0x7ffaf6847400: f9 f9 f9 f9 00 00 00 00 00 07 f9 f9 f9 f9 f9 f9
  0x7ffaf6847480: 00 00 00 00 00 03 f9 f9 f9 f9 f9 f9 00 00 00 00
  0x7ffaf6847500: f9 f9 f9 f9 00 00 00 f9 f9 f9 f9 f9 00 00 00 00
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

==9284==ADDITIONAL INFO

==9284==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffae0296aae in blink::HTMLDocumentParser::SchedulePumpTokenizer(bool) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc:886:7
    #1 0x7ffad48d5179 in IPC::ChannelAssociatedGroupController::Accept(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\ipc\ipc_mojo_bootstrap.cc:1154:13

```

## Attachments

- [poc.html](attachments/poc.html) (text/html, 71 B)
- [fix.diff](attachments/fix.diff) (text/x-diff, 689 B)

## Timeline

### m....@gmail.com (2024-10-25)

The fix is simple - just remove the inheritance from EventTarget in the IDL file as well

```
diff --git a/third_party/blink/renderer/modules/quota/storage_manager.idl b/third_party/blink/renderer/modules/quota/storage_manager.idl
index b259ee80b47cc..11ebb9c2fabbc 100644
--- a/third_party/blink/renderer/modules/quota/storage_manager.idl
+++ b/third_party/blink/renderer/modules/quota/storage_manager.idl
@@ -7,7 +7,7 @@
 [
     SecureContext,
     Exposed=(Window,Worker)
-] interface StorageManager : EventTarget {
+] interface StorageManager {
     [CallWith=ScriptState, MeasureAs=DurableStoragePersisted, RaisesException] Promise<boolean> persisted();
     [Exposed=Window, CallWith=ScriptState, MeasureAs=DurableStoragePersist, RaisesException] Promise<boolean> persist();
 


```

### cl...@chromium.org (2024-10-25)

+Evan as author of the CL where this reportedly was introduced (<https://crrev.com/c/5930607>).

### cl...@chromium.org (2024-10-25)

The reproducer looks innocent, uploading to Clusterfuzz:

```
<body><script>
navigator.storage.addEventListener(null,null)
</script>

```

### cl...@appspot.gserviceaccount.com (2024-10-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5560992100450304.

### cl...@appspot.gserviceaccount.com (2024-10-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5355422265311232.

### 24...@project.gserviceaccount.com (2024-10-25)

This crash occurs very frequently on windows platform and is likely preventing the fuzzer None from making much progress. Fixing this will allow more bugs to be found.

Marking this bug as a blocker for next Beta release.

If this is incorrect, please add the hotlistid:5433040 and remove the hotlistid:ReleaseBlock-Beta.

### pe...@google.com (2024-10-25)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-10-25)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### pe...@google.com (2024-10-25)

This issue appears to be blocking an upcoming release and is therefore an **Urgent Release Blocking Issue** as per <http://go/chrome-slo#release-blocking-issues>. Bumping the priority to P0 to better reflect the urgency.

If this is not a release blocking issue, please adjust the release block field. Adjusting the priority will have no affect, P0 will be re-applied whilever this is marked as a release blocking issue.

### cl...@chromium.org (2024-10-25)

Still waiting for regression range on https://clusterfuzz.com/testcase-detail/5355422265311232.
Signing off for the weekend.

### cl...@chromium.org (2024-10-25)

Unassigning myself because this does not seem to be a V8 issue. Maybe a chrome sheriff can take over further triaging.

### ke...@chromium.org (2024-10-28)

estade@: Your change https://crrev.com/1370046 appears to be the most likely cause in the regression range. Can you PTAL or revert?

### ke...@chromium.org (2024-10-28)

I realize that that CL is marked as not having behavioural changes but there don't seem to be any other candidates touching this area in the range CF identified: https://chromium.googlesource.com/chromium/src/+log/eab899ce58267f316c5285f9e69ebb636ce45592..814c3d563cdda7781a69d51bf28827af86609ed9

I'm running regression analysis again to check, but I think it is worth checking to see if there might have been a bug in that flag removal.

### pe...@google.com (2024-10-28)

This issue is marked as a release blocker with no milestone associated. Please add an appropriate milestone.

All release blocking issues should have milestones associated to it, so that the issue can tracked and the fixes can be pushed promptly.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-10-28)

Setting milestone because of s0/s1 severity.

### ke...@chromium.org (2024-10-28)

Closing this as a duplicate because I just noticed that issue 373924126 has the same crash stack and was found by Cluster-fuzz several days earlier (October 19).

### m....@gmail.com (2024-10-29)

re #c17 can you cc me on that issue.

### am...@chromium.org (2024-11-08)

temporarily unmerging as duplicate for VRP automation

### sp...@google.com (2024-11-08)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
$3000 super thank you reward; while this issue was already discovered and reported through fuzzing, this report helped in the investigation and resolution of this issue 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-11-08)

Congratulations -- thank you again for your report that resulted in helping us more efficiently and quickly resolve this issue that was also reported from our fuzzing. Thank you for your efforts and reporting this issue to us!

### ph...@google.com (2025-02-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/375317755)*
