# Security:  type confusion  in chrome

| Field | Value |
|-------|-------|
| **Issue ID** | [40060314](https://issues.chromium.org/issues/40060314) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | UI>Accessibility |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | wx...@gmail.com |
| **Assignee** | ab...@google.com |
| **Created** | 2022-07-17 |
| **Bounty** | $1,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**

**VERSION**  

**Chrome Version: [x.x.x.x] + [stable, beta, or dev]**  

**Operating System: [Please indicate OS, version, and service pack level]**

linux

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug, or any personal or confidential information.**

**Please attach files directly, not in zip or other archive formats, and if**  

**you've created a demonstration site please also attach the files needed to**  

**reproduce the demonstration locally.**

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

**Reporter credit: [goes here]**

## Attachments

- [0001-fix-type-confusion.patch](attachments/0001-fix-type-confusion.patch) (text/plain, 1.5 KB)

## Timeline

### wx...@gmail.com (2022-07-17)

1.download asan-linux-debug-1019996 chromium
2../chrome --no-sandbox --enable-features=ReadAnything,UnifiedSidePanel
3.open chrome, visit "chrome://version", open devtools, enter 
```
chrome.readAnything.setContentForTesting(123, [])
```
4.crash at dcheck 

```
[130551:130551:0717/180718.774217:FATAL:v8_initializer.cc(700)] V8 error: Value is not an Object (v8::Object::Cast).
#0 0x5565e0e0a57b (/home/raven/asan-linux-debug-1019996/chrome+0x9da557a)
#1 0x7f943d4d164f (/home/raven/asan-linux-debug-1019996/libbase.so+0xdf964e)
#2 0x7f943cd1ac34 (/home/raven/asan-linux-debug-1019996/libbase.so+0x642c33)
#3 0x7f943cd1aaa5 (/home/raven/asan-linux-debug-1019996/libbase.so+0x642aa4)
#4 0x7f943cdfc21e (/home/raven/asan-linux-debug-1019996/libbase.so+0x72421d)
#5 0x7f93a59b736a (/home/raven/asan-linux-debug-1019996/libblink_core.so+0x5042369)
#6 0x7f938ace9fa0 (/home/raven/asan-linux-debug-1019996/libv8.so+0x20a4f9f)
#7 0x7f938ad5b101 (/home/raven/asan-linux-debug-1019996/libv8.so+0x2116100)
#8 0x5565fa389509 (/home/raven/asan-linux-debug-1019996/chrome+0x23324508)
#9 0x5565fa388d73 (/home/raven/asan-linux-debug-1019996/chrome+0x23323d72)
#10 0x5565fa3a638d (/home/raven/asan-linux-debug-1019996/chrome+0x2334138c)
#11 0x5565fa3a6041 (/home/raven/asan-linux-debug-1019996/chrome+0x23341040)
#12 0x5565fa3a5e61 (/home/raven/asan-linux-debug-1019996/chrome+0x23340e60)
#13 0x5565fa3a5d50 (/home/raven/asan-linux-debug-1019996/chrome+0x23340d4f)
#14 0x5565fa3a5b40 (/home/raven/asan-linux-debug-1019996/chrome+0x23340b3f)
#15 0x5565fa3a42db (/home/raven/asan-linux-debug-1019996/chrome+0x2333f2da)
#16 0x5565fa3a3f0e (/home/raven/asan-linux-debug-1019996/chrome+0x2333ef0d)
#17 0x5565fa3a3af7 (/home/raven/asan-linux-debug-1019996/chrome+0x2333eaf6)
#18 0x7f938afc1146 (/home/raven/asan-linux-debug-1019996/libv8.so+0x237c145)
#19 0x7f938afbd545 (/home/raven/asan-linux-debug-1019996/libv8.so+0x2378544)
#20 0x7f938afb7946 (/home/raven/asan-linux-debug-1019996/libv8.so+0x2372945)
#21 0x7f938afb62ee (/home/raven/asan-linux-debug-1019996/libv8.so+0x23712ed)
#22 0x7f931f9fc93f <unknown>
Task trace:
#0 0x7f9432409b29 (/home/raven/asan-linux-debug-1019996/libipc.so+0x10ab28)
Crash keys:
  "blink_scheduler_async_stack" = "0x7F9432409B29 0x0"
  "v8_code_space_firstpage_address" = "0x7f9300000000"
  "v8_ro_space_firstpage_address" = "0x7d7b00000000"
  "v8_isolate_address" = "0x630000000400"
```

### [Deleted User] (2022-07-17)

[Empty comment from Monorail migration]

### wx...@gmail.com (2022-07-17)

though ```setContentForTesting``` is a test api, but it still can be accessed when we enable the ReadAnything features.

### wx...@gmail.com (2022-07-17)

the bug reason is that https://source.chromium.org/chromium/chromium/src/+/main:chrome/renderer/accessibility/read_anything_app_controller.cc;l=114
```
ui::AXTreeUpdate GetSnapshotFromV8SnapshotLite(
    v8::Isolate* isolate,
    v8::Local<v8::Value> v8_snapshot_lite) {
  ui::AXTreeUpdate snapshot;
  gin::Dictionary v8_snapshot_dict(
      isolate, v8::Local<v8::Object>::Cast(v8_snapshot_lite));  // just cast it to object without check its type.
  SetAXTreeUpdateRootId(isolate, &v8_snapshot_dict, &snapshot);

  v8::Local<v8::Value> v8_nodes;
  v8_snapshot_dict.Get("nodes", &v8_nodes);
  std::vector<v8::Local<v8::Value>> v8_nodes_vector;
  gin::Converter<std::vector<v8::Local<v8::Value>>>::FromV8(isolate, v8_nodes,
                                                            &v8_nodes_vector);
```

### wx...@gmail.com (2022-07-18)

[Comment Deleted]

### dc...@chromium.org (2022-07-18)

This is interesting.

I'm only able to repro with asan-linux-debug and not asan-linux-release. In asan-linux-release, I see:

VM81:1 Uncaught TypeError: chrome.readAnything.updateContent is not a function
    at <anonymous>:1:21
    at <anonymous>:1:21

There are two points of concern here:
- why is chrome.readAnything injected into chrome://version?
- what controls whether updateContent() is defined?

Assigning to an accessibility ONWER to help understand the answers to those two questions.

[Monorail components: UI>Accessibility]

### dc...@chromium.org (2022-07-18)

Also, a symbolized stack:

[45417:1:0718/221814.051950:FATAL:v8_initializer.cc(700)] V8 error: Value is not an Object (v8::Object::Cast).
    #0 0x5614c430657b in backtrace /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4404:13
    #1 0x7f12d1afc64f in base::debug::CollectStackTrace(void**, unsigned long) ./../../base/debug/stack_trace_posix.cc:875:39
    #2 0x7f12d1345c34 in base::debug::StackTrace::StackTrace(unsigned long) ./../../base/debug/stack_trace.cc:221:12
    #3 0x7f12d1345aa5 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:218:28
    #4 0x7f12d142721e in logging::LogMessage::~LogMessage() ./../../base/logging.cc:669:29
    #5 0x7f1239fd036a in blink::ReportV8FatalError(char const*, char const*) ./../../third_party/blink/renderer/bindings/core/v8/v8_initializer.cc:700:3
    #6 0x7f121f302fa0 in v8::Utils::ReportApiFailure(char const*, char const*) ./../../v8/src/api/api.cc:337:5
    #7 0x7f121f374101 in ApiCheck ./../../v8/src/api/api.h:153:21
    #8 0x7f121f374101 in v8::Object::CheckCast(v8::Value*) ./../../v8/src/api/api.cc:3912:3
    #9 0x5614dd885509 in Cast ./../../v8/include/v8-object.h:763:3
    #10 0x5614dd885509 in Cast<v8::Value> ./../../v8/include/v8-local-handle.h:242:21
    #11 0x5614dd885509 in (anonymous namespace)::GetSnapshotFromV8SnapshotLite(v8::Isolate*, v8::Local<v8::Value>) ./../../chrome/renderer/accessibility/read_anything_app_controller.cc:119:16
    #12 0x5614dd884d73 in ReadAnythingAppController::SetContentForTesting(v8::Local<v8::Value>, std::Cr::vector<int, std::Cr::allocator<int>>) ./../../chrome/renderer/accessibility/read_anything_app_controller.cc:321:7
    #13 0x5614dd8a238d in void base::internal::FunctorTraits<void (ReadAnythingAppController::*)(v8::Local<v8::Value>, std::Cr::vector<int, std::Cr::allocator<int>>), void>::Invoke<void (ReadAnythingAppController::*)(v8::Local<v8::Value>, std::Cr::vector<int, std::Cr::allocator<int>>), ReadAnythingAppController*, v8::Local<v8::Value>, std::Cr::vector<int, std::Cr::allocator<int>>>(void (ReadAnythingAppController::*)(v8::Local<v8::Value>, std::Cr::vector<int, std::Cr::allocator<int>>), ReadAnythingAppController*&&, v8::Local<v8::Value>&&, std::Cr::vector<int, std::Cr::allocator<int>>&&) ./../../base/bind_internal.h:562:12
    #14 0x5614dd8a2041 in void base::internal::InvokeHelper<false, void>::MakeItSo<void (ReadAnythingAppController::* const&)(v8::Local<v8::Value>, std::Cr::vector<int, std::Cr::allocator<int>>), ReadAnythingAppController*, v8::Local<v8::Value>, std::Cr::vector<int, std::Cr::allocator<int>>>(void (ReadAnythingAppController::* const&)(v8::Local<v8::Value>, std::Cr::vector<int, std::Cr::allocator<int>>), ReadAnythingAppController*&&, v8::Local<v8::Value>&&, std::Cr::vector<int, std::Cr::allocator<int>>&&) ./../../base/bind_internal.h:726:12
    #15 0x5614dd8a1e61 in void base::internal::Invoker<base::internal::BindState<void (ReadAnythingAppController::*)(v8::Local<v8::Value>, std::Cr::vector<int, std::Cr::allocator<int>>)>, void (ReadAnythingAppController*, v8::Local<v8::Value>, std::Cr::vector<int, std::Cr::allocator<int>>)>::RunImpl<void (ReadAnythingAppController::* const&)(v8::Local<v8::Value>, std::Cr::vector<int, std::Cr::allocator<int>>), std::Cr::tuple<> const&>(void (ReadAnythingAppController::* const&)(v8::Local<v8::Value>, std::Cr::vector<int, std::Cr::allocator<int>>), std::Cr::tuple<> const&, std::Cr::integer_sequence<unsigned long>, ReadAnythingAppController*&&, v8::Local<v8::Value>&&, std::Cr::vector<int, std::Cr::allocator<int>>&&) ./../../base/bind_internal.h:799:12
    #16 0x5614dd8a1d50 in base::internal::Invoker<base::internal::BindState<void (ReadAnythingAppController::*)(v8::Local<v8::Value>, std::Cr::vector<int, std::Cr::allocator<int>>)>, void (ReadAnythingAppController*, v8::Local<v8::Value>, std::Cr::vector<int, std::Cr::allocator<int>>)>::Run(base::internal::BindStateBase*, ReadAnythingAppController*, v8::Local<v8::Value>&&, std::Cr::vector<int, std::Cr::allocator<int>>&&) ./../../base/bind_internal.h:781:12
    #17 0x5614dd8a1b40 in base::RepeatingCallback<void (ReadAnythingAppController*, v8::Local<v8::Value>, std::Cr::vector<int, std::Cr::allocator<int>>)>::Run(ReadAnythingAppController*, v8::Local<v8::Value>, std::Cr::vector<int, std::Cr::allocator<int>>) const & ./../../base/callback.h:242:12
    #18 0x5614dd8a02db in gin::internal::Invoker<std::Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul>, ReadAnythingAppController*, v8::Local<v8::Value>, std::Cr::vector<int, std::Cr::allocator<int>>>::DispatchToCallback(base::RepeatingCallback<void (ReadAnythingAppController*, v8::Local<v8::Value>, std::Cr::vector<int, std::Cr::allocator<int>>)>) ./../../gin/function_template.h:181:14
    #19 0x5614dd89ff0e in gin::internal::Dispatcher<void (ReadAnythingAppController*, v8::Local<v8::Value>, std::Cr::vector<int, std::Cr::allocator<int>>)>::DispatchToCallbackImpl(gin::Arguments*) ./../../gin/function_template.h:213:15
    #20 0x5614dd89faf7 in gin::internal::Dispatcher<void (ReadAnythingAppController*, v8::Local<v8::Value>, std::Cr::vector<int, std::Cr::allocator<int>>)>::DispatchToCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./../../gin/function_template.h:219:5
    #21 0x7f121f5da146 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:147:3
    #22 0x7f121f5d6545 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:114:36
    #23 0x7f121f5d0946 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:144:5
    #24 0x7f121f5cf2ee in v8::internal::Builtin_HandleApiCall(int, unsigned long*, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:132:1
#22 0x7f119f9fc93f <unknown>


### ab...@google.com (2022-07-19)

chrome.readAnything is injected by the ReadAnythingAppController [1], which is instantiated by the ChromeRenderFrameObserver whenever the ReadAnything experiment is enabled and when the render frame is a WebUI [2]. chrome.readAnything.updateContent is defined in read_anything.d.ts [3] and implemented in read_anything/app.ts [4]. read_anything.app.ts is only added whenever the Read Anything WebUI appears. It seems like there are 2 options here:
(a) Only create ReadAnythingAppController when the render_frame happens to be a ReadAnything WebUI. Right now we are instantiating on any WebUI which we neither want nor need.
(b) Perhaps read_anything.d.ts should implement updateContent and the other functions as no-op to avoid this crash.

I'd like to do (a) if it's possible to identify the type of WebUI from ChromeRenderFrameObserver. Otherwise, I think (b) will suffice.

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/renderer/accessibility/read_anything_app_controller.cc;l=171?q=read_anything_app_controller&ss=chromium
[2] https://source.chromium.org/chromium/chromium/src/+/main:chrome/renderer/chrome_render_frame_observer.cc;l=326?q=read_anything_app_controller&ss=chromium
[3] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/resources/side_panel/read_anything/read_anything.d.ts;l=81?q=readanything%20updatecontent%20-f:debug&ss=chromium
[4] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/resources/side_panel/read_anything/app.ts;l=30?q=readanything%20updatecontent%20-f:debug&ss=chromium

### dc...@chromium.org (2022-07-19)

To be clear, I think the bug is present even if we inject only on the ReadAnything WebUI. We need to typecheck the arguments before casting them. The safest way to do this is probably by using v8::Value::ToObject<> and then using either:
1. v8::MaybeLocal::IsEmpty() to check before using v8::MaybeLocal::ToLocalChecked()
2. v8::MaybeLocal::ToLocal() and checking the return value.

Medium because type confusion could reasonably lead to memory corruption, but it is in a sandboxed process. I think this could potentially be low given that it also requires devtools currently (though it's certainly a bug that could weaken the effectiveness of the sandbox if chained with something else).

Is ReadAnything enabled anywhere by default? It's off by default here (https://source.chromium.org/chromium/chromium/src/+/main:ui/accessibility/accessibility_features.cc;l=190;drc=b6ac8170f0a9b83bf0ce57b1a4f882199180604c) but I'm not sure if it's enabled via finch anywhere by default.

Re: FoundIn, I believe this was introduced by https://source.chromium.org/chromium/chromium/src/+/8bb1c56b6bb22cb2f8e52ca038ac2c6b02d6ead7.

### [Deleted User] (2022-07-19)

[Empty comment from Monorail migration]

### wx...@gmail.com (2022-07-19)

sugguest patch.

### dc...@chromium.org (2022-07-19)

As mentioned in the previous comment, it's probably better to use the ToObject helpers that return a MaybeLocal.

### wx...@gmail.com (2022-07-19)

yes, you are right.

### ab...@google.com (2022-07-19)

Read Anything is off by default everywhere, including via finch. And setContentForTesting is also just used for tests (as per the name). I thought our compiler was somewhat smart and only exposed ForTesting functions in our testing builds...maybe not in this case.

### dc...@chromium.org (2022-07-19)

ForTesting() is built everywhere; we rely on dead code elimination for it to be removed where it's not needed (e.g. in official Chrome binaries that ship to users).

However, if something is exposed through gin, the compiler/linker doesn't have a way to prove that the code isn't used, so it can't be eliminated.

### [Deleted User] (2022-07-20)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-20)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wx...@gmail.com (2022-07-21)

I think this bug should set impact-None as this bug should enable the ReadAnything features.

### dc...@chromium.org (2022-07-21)

Setting to none per https://crbug.com/chromium/1345088#c14:

> Read Anything is off by default everywhere, including via finch. 

### [Deleted User] (2022-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-23)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dc...@chromium.org (2022-07-23)

[Empty comment from Monorail migration]

### dc...@chromium.org (2022-07-23)

[Empty comment from Monorail migration]

### dc...@chromium.org (2022-07-23)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-07-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c14dc950b3c731e5daf58bdba4b4a7ee9b64e337

commit c14dc950b3c731e5daf58bdba4b4a7ee9b64e337
Author: Abigail Klein <abigailbklein@google.com>
Date: Mon Jul 25 01:26:39 2022

[Read Anything] Typecheck v8 arguments before casting them.

Fixed: 1345088
Bug: 1266555
Change-Id: Icd1690b961af585d33d3afa5ac909939629b48f4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3776954
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Abigail Klein <abigailbklein@google.com>
Cr-Commit-Position: refs/heads/main@{#1027608}

[modify] https://crrev.com/c14dc950b3c731e5daf58bdba4b4a7ee9b64e337/chrome/renderer/accessibility/read_anything_app_controller.cc


### [Deleted User] (2022-07-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-25)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-11)

Congratulations! The VRP Panel has decided to award you $1,000 for this report. The reward amount was based on this issue potentially resulting in type confusion in a sandboxed process and substantially mitigated by not being remote exploitable, and the user interaction required. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ni...@google.com (2022-10-31)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1345088?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060314)*
