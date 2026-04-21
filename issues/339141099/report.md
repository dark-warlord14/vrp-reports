# v8::Value string with unmatched UTF8 surrogate pair causes crash when converted to base::Value

| Field | Value |
|-------|-------|
| **Issue ID** | [339141099](https://issues.chromium.org/issues/339141099) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | go...@gmail.com |
| **Assignee** | le...@chromium.org |
| **Created** | 2024-05-07 |
| **Bounty** | $3,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md

Please see the following link for instructions on filing security bugs: https://www.chromium.org/Home/chromium-security/reporting-security-bugs

Reports may be eligible for reward payments under the Chrome VRP: https://g.co/chrome/vrp

NOTE: Security bugs are normally made public once a fix has been widely deployed.

-------------------------

VULNERABILITY DETAILS
Please provide a brief explanation of the security issue.

VERSION
Chrome Version: [Chromium 126.0.6464.0 ] + [dev]
Operating System:ubuntu

REPRODUCTION CASE
chrome  --load-extension="/home/ubuntu/dev/report" --no-sandbox

Please attach files directly, not in zip or other archive formats, and if you've created a demonstration site please also attach the files needed to reproduce the demonstration locally.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: [extension]
Crash State: 
[1749384:1749384:0507/205933.187938:FATAL:values.cc(195)] Check failed: IsStringUTF8AllowingNoncharacters(GetString()). 
#0 0x7e2907d661bc base::debug::CollectStackTrace() [../../base/debug/stack_trace_posix.cc:1043:7]
#1 0x7e2907d17355 base::debug::StackTrace::StackTrace() [../../base/debug/stack_trace.cc:241:20]
#2 0x7e2907d172e5 base::debug::StackTrace::StackTrace() [../../base/debug/stack_trace.cc:236:28]
#3 0x7e2907a3563f logging::LogMessage::Flush() [../../base/logging.cc:715:29]
#4 0x7e2907a35567 logging::LogMessage::~LogMessage() [../../base/logging.cc:703:3]
#5 0x7e29079dcdd5 logging::(anonymous namespace)::DCheckLogMessage::~DCheckLogMessage() [../../base/check.cc:166:3]
#6 0x7e29079dcdf9 logging::(anonymous namespace)::DCheckLogMessage::~DCheckLogMessage() [../../base/check.cc:161:32]
#7 0x7e29079ddbdc std::__Cr::default_delete<>::operator()() [../../third_party/libc++/src/include/__memory/unique_ptr.h:67:5]
#8 0x7e29079dd13a std::__Cr::unique_ptr<>::reset() [../../third_party/libc++/src/include/__memory/unique_ptr.h:278:7]
#9 0x7e29079dc71d logging::CheckError::~CheckError() [../../base/check.cc:349:16]
#10 0x7e2907cc7222 base::Value::Value() [../../base/values.cc:195:3]
#11 0x7e2905397476 std::__Cr::make_unique<>() [../../third_party/libc++/src/include/__memory/unique_ptr.h:620:30]
#12 0x7e2905391da2 content::V8ValueConverterImpl::FromV8ValueImpl() [../../content/renderer/v8_value_converter_impl.cc:393:12]
#13 0x7e2905391238 content::V8ValueConverterImpl::FromV8Value() [../../content/renderer/v8_value_converter_impl.cc:237:10]
#14 0x5e062052a6fe extensions::ArgumentSpec::ParseArgumentToAny() [../../extensions/renderer/bindings/argument_spec.cc:731:20]
#15 0x5e0620526e07 extensions::ArgumentSpec::ParseArgument() [../../extensions/renderer/bindings/argument_spec.cc:323:14]
#16 0x5e0620528fe5 extensions::ArgumentSpec::ParseArgumentToObject() [../../extensions/renderer/bindings/argument_spec.cc:576:25]
#17 0x5e0620526895 extensions::ArgumentSpec::ParseArgument() [../../extensions/renderer/bindings/argument_spec.cc:295:14]
#18 0x5e062051c456 extensions::(anonymous namespace)::ArgumentParser::ParseArgument() [../../extensions/renderer/bindings/api_signature.cc:374:13]
#19 0x5e062051bb90 extensions::(anonymous namespace)::ArgumentParser::ParseArgumentsImpl() [../../extensions/renderer/bindings/api_signature.cc:269:10]
#20 0x5e062051a0f7 extensions::(anonymous namespace)::BaseValueArgumentParser::ParseArguments() [../../extensions/renderer/bindings/api_signature.cc:433:8]
#21 0x5e0620519fdc extensions::APISignature::ParseArgumentsToJSON() [../../extensions/renderer/bindings/api_signature.cc:585:8]
#22 0x5e06204c1b01 extensions::APIBinding::HandleCall() [../../extensions/renderer/bindings/api_binding.cc:685:22]
#23 0x5e06204c8aad base::internal::DecayedFunctorTraits<>::Invoke<>() [../../base/functional/bind_internal.h:738:12]
#24 0x5e06204c8997 base::internal::InvokeHelper<>::MakeItSo<>() [../../base/functional/bind_internal.h:954:5]
#25 0x5e06204c88c5 base::internal::Invoker<>::RunImpl<>() [../../base/functional/bind_internal.h:1067:14]
#26 0x5e06204c87ef base::internal::Invoker<>::Run() [../../base/functional/bind_internal.h:987:12]
#27 0x5e06204c97b8 base::RepeatingCallback<>::Run() [../../base/functional/callback.h:344:12]
#28 0x5e06204c1f84 extensions::(anonymous namespace)::RunAPIBindingHandlerCallback() [../../extensions/renderer/bindings/api_binding.cc:92:13]
#29 0x7e28d104d38f Builtins_CallApiCallbackGeneric
Task trace:
#0 0x7e28c0fad032 blink::DOMTimer::DOMTimer() [../../third_party/blink/renderer/modules/scheduler/dom_timer.cc:311:29]
#1 0x7e28fafc5895 IPC::ChannelAssociatedGroupController::Accept() [../../ipc/ipc_mojo_bootstrap.cc:1137:13]
Crash keys:
  "view-count" = "1"
  "loaded-origin-0" = "chrome-extension://melpoimnfajnldalfphacjkpnikmdmfo"
  "web-frame-count" = "1"
  "extension-1" = "melpoimnfajnldalfphacjkpnikmdmfo"
  "num-extensions" = "1"
  "renderer_foreground" = "true"
  "v8_ro_space_firstpage_address" = "0x339500000000"
  "v8_isolate_address" = "0x3da0001b4000"
  "reentry_guard_tls_slot" = "unused"
  "switch-16" = "--variations-seed-version"
  "switch-15" = "--field-trial-handle=3,i,2416572154099510137,3024019929584948269"
  "switch-14" = "--metrics-shmem-handle=4,i,9932640714038900285,15894981856334668"
  "switch-13" = "--shared-files=v8_context_snapshot_data:100"
  "switch-12" = "--launch-time-ticks=36526195309"
  "switch-11" = "--time-ticks-at-unix-epoch=-1715050238171397"
  "switch-10" = "--renderer-client-id=7"
  "switch-9" = "--enable-main-frame-before-activation"
  "switch-8" = "--num-raster-threads=4"
  "switch-7" = "--lang=en-US"
  "switch-6" = "--disable-gpu-compositing"
  "switch-5" = "--no-sandbox"
  "osarch" = "x86_64"
  "pid" = "1749384"
  "ptype" = "renderer"
  "switch-4" = "--change-stack-guard-on-fork=enable"
  "switch-3" = "--extension-process"
  "switch-2" = "--enable-crash-reporter=,"
  "switch-1" = "--crashpad-handler-pid=1749024"
  "num-switches" = "17"
Client ID (if relevant): [see link above]

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: [goes here]

## Attachments

- [background.js](attachments/background.js) (text/javascript, 1.1 KB)
- [manifest.json](attachments/manifest.json) (application/json, 225 B)
- [out.txt](attachments/out.txt) (text/plain, 6.8 KB)

## Timeline

### ca...@chromium.org (2024-05-07)

Thanks for the report. Can you provide more details on why this has security implications? It looks like this is the invalid character being caught by the DCHECK.

### ad...@google.com (2024-05-10)

Reproduced this locally in an ASAN, non-DCHECK build.

```
Received signal 11 SEGV_MAPERR 00000000010c
    #0 0x55f054219506 in ___interceptor_backtrace /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4358:13
    #1 0x55f066070dd8 in base::debug::CollectStackTrace(void const**, unsigned long) ./../../base/debug/stack_trace_posix.cc:1039:7
    #2 0x55f066039849 in StackTrace ./../../base/debug/stack_trace.cc:234:12
    #3 0x55f066039849 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:231:28
    #4 0x55f0660700c6 in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) ./../../base/debug/stack_trace_posix.cc:457:3
    #5 0x7f2927042520 in __sigaction ??:?
    #6 0x55f0754d01aa in Get ./../../v8/include/cppgc/internal/member-storage.h:42:20
    #7 0x55f0754d01aa in Decompress ./../../v8/include/cppgc/internal/member-storage.h:160:28
    #8 0x55f0754d01aa in Load ./../../v8/include/cppgc/internal/member-storage.h:85:47
    #9 0x55f0754d01aa in GetRaw ./../../v8/include/cppgc/member.h:52:54
    #10 0x55f0754d01aa in Get ./../../v8/include/cppgc/member.h:270:52
    #11 0x55f0754d01aa in blink::Document::GetExecutionContext() const ./../../third_party/blink/renderer/core/dom/document.cc:7593:29
    #12 0x55f073171956 in blink::DOMPatchSupport::PatchDocument(WTF::String const&) ./../../third_party/blink/renderer/core/inspector/dom_patch_support.cc:66:47
    #13 0x55f07312a63f in blink::InspectorDOMAgent::setOuterHTML(int, WTF::String const&) ./../../third_party/blink/renderer/core/inspector/inspector_dom_agent.cc:1065:23
    #14 0x55f07312ab98 in non-virtual thunk to blink::InspectorDOMAgent::setOuterHTML(int, WTF::String const&) ./../../third_party/blink/renderer/core/inspector/inspector_dom_agent.cc:0:0
    #15 0x55f0629ecc72 in blink::protocol::DOM::DomainDispatcherImpl::setOuterHTML(crdtp::Dispatchable const&) ./gen/third_party/blink/renderer/core/inspector/protocol/dom.cc:2427:44
    #16 0x55f06d845e3b in operator() ./../../third_party/libc++/src/include/__functional/function.h:714:12
    #17 0x55f06d845e3b in operator() ./../../third_party/libc++/src/include/__functional/function.h:981:10
    #18 0x55f06d845e3b in crdtp::UberDispatcher::DispatchResult::Run() ./../../third_party/inspector_protocol/crdtp/dispatch.cc:509:3
    #19 0x55f0732d607d in blink::DevToolsSession::DispatchProtocolCommandImpl(int, WTF::String const&, base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>) ./../../third_party/blink/renderer/core/inspector/devtools_session.cc:268:59
    #20 0x55f0732d59b1 in blink::DevToolsSession::DispatchProtocolCommand(int, WTF::String const&, base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>) ./../../third_party/blink/renderer/core/inspector/devtools_session.cc:232:10
    #21 0x55f0620f22bc in blink::mojom::blink::DevToolsSessionStubDispatch::Accept(blink::mojom::blink::DevToolsSession*, mojo::Message*) ./gen/third_party/blink/public/mojom/devtools/devtools_agent.mojom-blink.cc:1394:13
    #22 0x55f0675a5e5a in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1021:54
    #23 0x55f0675c2048 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #24 0x55f0675aaf46 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:706:20
    #25 0x55f068368350 in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) ./../../ipc/ipc_mojo_bootstrap.cc:1181:24
    #26 0x55f068369a34 in Invoke<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification> ./../../base/functional/bind_internal.h:738:12
    #27 0x55f068369a34 in MakeItSo<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification> > ./../../base/functional/bind_internal.h:930:12
    #28 0x55f068369a34 in RunImpl<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, 0UL, 1UL, 2UL> ./../../base/functional/bind_internal.h:1067:14
    #29 0x55f068369a34 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:980:12
    #30 0x55f065eec175 in Run ./../../base/functional/callback.h:156:12
    #31 0x55f065eec175 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:203:34
    #32 0x55f065f4dbb0 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:11)> ./../../base/task/common/task_annotator.h:90:5
    #33 0x55f065f4dbb0 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:473:23
    #34 0x55f065f4cb9a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:338:40
    #35 0x55f065f4e96b in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #36 0x55f065de6e0d in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:40:55
    #37 0x55f065f4f6b0 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:641:12
    #38 0x55f065e7f5d0 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #39 0x55f07d0f3c1b in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:367:16
    #40 0x55f06366e079 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:676:14
    #41 0x55f06366f5a2 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:780:12
    #42 0x55f063671fe0 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1146:10
    #43 0x55f06366c3d1 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:333:36
    #44 0x55f06366ca4c in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:346:10
    #45 0x55f0542a3de9 in ChromeMain ./../../chrome/app/chrome_main.cc:192:12
    #46 0x7f2927029d90 in __libc_init_first ??:?
    #47 0x7f2927029e40 in __libc_start_main ??:0:0
    #48 0x55f0541d702a in _start ??:0:0
  r8: 00000fe52493355b  r9: 00007f292499aae8 r10: 00000fe52493355d r11: 00000fe5a492b558
 r12: 00007f2924764228 r13: 00007f292499a800 r14: 00000fe5248ec845 r15: 00000fe524933500
  di: 000000000000010c  si: 0000000000000000  bp: 00007ffe9451e7b0  bx: 00007ffe9451e7c0
  dx: 0000000000000011  ax: 00000abe0ff3c658  cx: 000055f07f9e32c0  sp: 00007ffe9451e7b0
  ip: 000055f0754d01aa efl: 0000000000010246 cgf: 002b000000000033 erf: 0000000000000004
 trp: 000000000000000e msk: 0000000000000000 cr2: 000000000000010c


```

(specifically [this build](https://chromium-browser-asan.storage.googleapis.com/linux-release%2Fasan-linux-release-1274542.zip)).

The stack trace appears to be quite different but from the POC's `background.js` it is the `OuterHTML` which contains the invalid character(s) so I do believe this is likely to be the same root cause.

On the face of it, this error is a null-ish pointer dereference which [is not considered a security bug](https://chromium.googlesource.com/chromium/src/+/main/docs/security/faq.md#Why-aren_t-null-pointer-dereferences-considered-security-bugs).... but, that stack trace isn't directly about the HTML characters, so it suggests that the invalid UTF8 is causing some stack trampling to occur. I'm not sure about that, but it's sufficiently worrying for me to pass it through to some of the relevant engineering folks to take a look. I'm going to assume this can be used for renderer RCE with the precondition of an extension being installed, hence S2.

### ad...@google.com (2024-05-10)

I'm not sure where exactly this potential bug should be fixed, but it seems most likely that [this code should validate the information from extensions better](https://source.chromium.org/chromium/chromium/src/+/main:extensions/renderer/bindings/argument_spec.cc?q=extensions%2Frenderer%2Fbindings%2Fargument_spec.cc) so passing it over to extensions folks.

### pe...@google.com (2024-05-10)

Setting milestone because of s2 severity.

### pe...@google.com (2024-05-10)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### rd...@chromium.org (2024-05-16)

I'm not going to have a chance to look into this in the next week or so; Tim, do you have the bandwidth to check this out, since it's related to the bindings?

If not, feel free to pass back to me and I'll take a look when I can.

### go...@gmail.com (2024-05-29)

Hello, please take a look at this issue, thanks.

### pe...@google.com (2024-05-29)

Thank you for providing more feedback. Adding the requester to the CC list.

### tj...@chromium.org (2024-05-29)

I found time to dig into this, but it would have been a lot easier to diagnose if the report had provided any details beyond extension code, or even if the string used to trip this had been reduced down to the minimum reproduction case.

The heart of what's going on here seems to stem from having Unicode high surrogate or low surrogate characters that are not paired with one of the others. Reducing the long string used in the extension code down to `unescape('%uD8AC')` makes this much easier to see and triggers the same crash.

I think this should probably be caught in `V8ValueConverterImpl::FromV8ValueImpl` after we try to create a `v8::String::Utf8Value` here: <https://source.chromium.org/chromium/chromium/src/+/main:content/renderer/v8_value_converter_impl.cc;l=392;drc=c0265133106c7647e90f9aaa4377d28190b1a6a9>

Copying on a v8ValueConverter owner to see if that sounds right to them.

### tj...@chromium.org (2024-05-29)

danakj@ per [comment #10](https://issues.chromium.org/issues/339141099#comment10), does catching this in the V8ValueConverter sound reasonable to you?

### ad...@google.com (2024-05-30)

If possible, let's add a fuzzer when fixing this.

### da...@chromium.org (2024-05-30)

I think it's a bit weird to construct a `v8::String::Utf8Value` and it has invalid Utf8 in it. The type already [handles failures internally](https://source.chromium.org/chromium/chromium/src/+/main:v8/include/v8-primitive.h;l=506-509;drc=8b6aaad8027390ce6b32d82d57328e93f34bb8e5) by making its length 0, but not in this case apparently.

And then quite unfortunate to require every user of `Utf8Value` to know to check if it actually is Utf8 through some other independent thing (`base::IsStringUTF8AllowingNoncharacters()`).

Let's see where `Utf8Value` is constructed... there are **124** callers outside of tests. That's a lot.

Could we make `Utf8Value` not hold invalid Utf8 strings?

### tj...@chromium.org (2024-05-30)

Yeah, I would say that the right approach here would either be to not let the Utf8Value hold the invalid string, or to have the base::Value constructed with the invalid string handle it gracefully.

Also adjusting the title of this bug to better reflect what is going on, as the original title doesn't actually even describe what the replication case is doing (it's using the `DOM.setOuterHTML` protocol with the `chrome.debugger.sendCommand` API).

### da...@chromium.org (2024-05-31)

Yes making a `base::Value::TryFromUtf8String(std::string) -> std::optional<base::Value>` could be alright too, and change that DCHECK in the ctor into a CHECK.

### le...@chromium.org (2024-06-03)

Is the bug here that the String -> Utf8Value conversion in V8 is [calling `WriteUtf8`](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/api/api.cc;l=10755;drc=ac83a5a2d3c04763d86ce16d92f3904cc9566d3a) without passing in [`REPLACE_INVALID_UTF8`](https://source.chromium.org/chromium/chromium/src/+/main:v8/include/v8-primitive.h;l=193;drc=ac83a5a2d3c04763d86ce16d92f3904cc9566d3a)?

### da...@chromium.org (2024-06-03)

Yes that does look like the bug, thank you. Could you please pass to an appropriate owner?

### le...@chromium.org (2024-06-03)

Do you know who an appropriate owner would be for the uses of this conversion? I would help fix this by adding an option to `Utf8Value` to specify the behaviour for invalid utf8, but it's still up to the caller what should happen on invalid utf8 -- as far as V8 is concerned, it's ok to have unmatched surrogates (afaiu, this is called ["wtf8"](https://simonsapin.github.io/wtf-8/)). +jbroman

### da...@chromium.org (2024-06-03)

IIUC you're saying that Utf8Value would be constructible in two ways, either with valid utf8 only or with whatever-was-there "wtf8".

Any string that goes over IPC (as a string) is supposed to be valid utf: https://crbug.com/40509710
Any string that goes into base::Value is supposed to be valid utf: https://source.chromium.org/chromium/chromium/src/+/main:base/values.cc;l=196;drc=42abceb7b1a3ae703fff8ea1a30cde5cdc258195

Maybe there are cases where the UtfValue is not used for those cases, or is kept as an array-of-bytes for IPC rather than a string, in which case we'd want the "wtf8" (latin1?) encoding.

Could we make the default be to produce a Utf8String with valid utf8, and make the explicit choice be to allow other characters in the places that intend for that @jbroman?

### le...@chromium.org (2024-06-03)

Pretty much, I'm saying that Utf8Value would really be Wtf8Value by default (as it is now), with an option to replace unpaired surrogates with bad characters that coerce it to also be valid utf8 (at the cost of losing data in the encoding). For reference, "wtf8" is "utf8 + unpaired surrogates", i.e. a utf8 extension that supports all strings that are valid in JS.

Making Utf8Value do the replacement by default is a bit more tricky because this would technically be an API-breaking change. Probably no-one depends on it the current behaviour, so it might be ok, but it's non-zero risk of breaking somewhere else.

### da...@chromium.org (2024-06-03)

Yeah, for the same kind of reason, why I like changing the default is that there's a non-zero chance that there are other security bugs around caused by assumptions that the string is valid utf8 when it's not.

### le...@chromium.org (2024-06-11)

You know what, I'll try it and see if anything breaks (I don't expect anything to).

### ap...@google.com (2024-06-11)

Project: v8/v8
Branch: main

commit e1a61acd40f102934058d3a92c59aea49d2e9ab4
Author: Leszek Swirski <leszeks@chromium.org>
Date:   Tue Jun 11 16:53:40 2024

    [api] Pass WriteOptions to Utf8Value cstr
    
    ... and make it replace REPLACE_INVALID_UTF8 by default, so that
    Utf8Value holds, by default, a valid utf8 value.
    
    Bug: 339141099
    Change-Id: Icae9f33d389ee64abed4ac8536620e3b4f8ddfd1
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5621893
    Auto-Submit: Leszek Swirski <leszeks@chromium.org>
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
    Commit-Queue: Leszek Swirski <leszeks@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#94379}

M       include/v8-primitive.h
M       src/api/api.cc

https://chromium-review.googlesource.com/5621893


### go...@gmail.com (2024-06-17)

hi, can I get a CVE number and rewards?

### le...@chromium.org (2024-06-18)

This should be fixed as far as V8 is concerned, assigning back(?) to Dana for any next steps like fuzzing (re #12)

### da...@chromium.org (2024-06-18)

Thanks Leszek, I'll give to ade to comment on fuzzing.

### ad...@chromium.org (2024-06-18)

I'm going to mark this as Fixed so that suitable merges can happen (plus CVE/release notes/rewards processes in due course). I'll file another bug for fuzzer stuff.

### ad...@chromium.org (2024-06-18)

Fuzzer improvements raised as [issue 347863960](https://issues.chromium.org/issues/347863960).

### go...@gmail.com (2024-06-24)

Hello, please take a look at this issue, thanks.

### am...@chromium.org (2024-06-24)

Hello, this issue has already been resolved.
In terms of potential VRP rewards, this issue will be assessed at a future VRP Panel session. As always, the bug will be updated with a reward decision after it is assessed.

### sp...@google.com (2024-06-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
$3,000 for report of mildly mitigated memory corruption in a sandboxed process 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-27)

Congratulations! Please let us know what name/handle you would like us to use in acknowledging you for this issue in release notes when the fix is shipped in a Stable channel update. Thank you for your efforts and reporting this issue to us.

### go...@gmail.com (2024-06-29)

Thanks, please use this name:
bowu(@gocrashed)

### pe...@google.com (2024-09-25)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2024-09-25)

1. https://chromium-review.googlesource.com/c/v8/v8/+/5882720
2. Low, no conflicts
3. No.
4. Yes

### pe...@google.com (2024-09-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### gm...@google.com (2024-09-26)

Merged to M128. Approving for LTS-126

### ap...@google.com (2024-10-01)

Project: v8/v8  

Branch: refs/branch-heads/12.6  

Author: Leszek Swirski <[leszeks@chromium.org](mailto:leszeks@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5882720>

[M126-LTS][api] Pass WriteOptions to Utf8Value cstr

---


Expand for full commit details
```
[M126-LTS][api] Pass WriteOptions to Utf8Value cstr

... and make it replace REPLACE_INVALID_UTF8 by default, so that
Utf8Value holds, by default, a valid utf8 value.

(cherry picked from commit e1a61acd40f102934058d3a92c59aea49d2e9ab4)

Bug: 339141099
Change-Id: Icae9f33d389ee64abed4ac8536620e3b4f8ddfd1
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5621893
Auto-Submit: Leszek Swirski <leszeks@chromium.org>
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Commit-Queue: Leszek Swirski <leszeks@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#94379}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5882720
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com>
Cr-Commit-Position: refs/branch-heads/12.6@{#66}
Cr-Branched-From: 3c9fa12db3183a6f4ea53d2675adb66ea1194529-refs/heads/12.6.228@{#2}
Cr-Branched-From: 981bb15ba4dbf9e2381dfc94ec2c4af0b9c6a0b6-refs/heads/main@{#93835}

```

---

Files:

- M `include/v8-primitive.h`
- M `src/api/api.cc`

---

Hash: 4b308315e7ef1eb1b8329beb432ddc8ddf0cd294  

Date:  Tue Jun 11 16:53:40 2024


---

### am...@chromium.org (2025-08-15)

The reward for this issue has been abandoned for over one year. As is our policy for abandoned rewards, it has been processed for donation. The reward for this issue has been donated to the Spyware Accountability Initiative (<https://stopspyware.fund/>)

## Bounty Award

> $3,000 for report of mildly mitigated memory corruption in a sandboxed process

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/339141099)*
