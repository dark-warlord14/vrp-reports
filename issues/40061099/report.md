# uaf in v8_inspector::InjectedScript::addPromiseCallback

| Field | Value |
|-------|-------|
| **Issue ID** | [40061099](https://issues.chromium.org/issues/40061099) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Unknown |
| **Platforms** | Linux |
| **Reporter** | em...@gmail.com |
| **Assignee** | sz...@chromium.org |
| **Created** | 2022-09-22 |
| **Bounty** | $1,000.00 |

## Description

\*\*Steps to reproduce the problem:\*\*
tested os:ubuntu 22.04
tested chrome:
Version 106.0.5249.12 (Official Build) dev (64-bit)
Chromium 108.0.5312.0
This issue can be reproduced in scenarios where automation tools are used, such as puppeteer.
1. install puppeteer.
2. node ./test.js
3. immediately crash.
\*\*Problem Description:\*\*
==311686==ERROR: AddressSanitizer: heap-use-after-free on address 0x6110000d6be8 at pc 0x7f89998a37e1 bp 0x7ffcbe9ea300 sp 0x7ffcbe9ea2f8
READ of size 8 at 0x6110000d6be8 thread T0 (chrome)
#0 0x7f89998a37e0 in size ./../../buildtools/third\_party/libc++/trunk/include/\_\_hash\_table:777:55
#1 0x7f89998a37e0 in bucket\_count ./../../buildtools/third\_party/libc++/trunk/include/\_\_hash\_table:1173:45
#2 0x7f89998a37e0 in std::Cr::pair<std::Cr::\_\_hash\_iterator<std::Cr::\_\_hash\_node<v8\_inspector::EvaluateCallback\\*, void\\*>\\*>, bool> std::Cr::\_\_hash\_table<v8\_inspector::EvaluateCallback\\*, std::Cr::hash<v8\_inspector::EvaluateCallback\\*>, std::Cr::equal\_to<v8\_inspector::EvaluateCallback\\*>, std::Cr::allocator<v8\_inspector::EvaluateCallback\\*>>::\_\_emplace\_unique\_key\_args<v8\_inspector::EvaluateCallback\\*, v8\_inspector::EvaluateCallback\\*>(v8\_inspector::EvaluateCallback\\* const&, v8\_inspector::EvaluateCallback\\*&&) ./../../buildtools/third\_party/libc++/trunk/include/\_\_hash\_table:2002:22
#3 0x7f89998858e3 in \_\_insert\_unique ./../../buildtools/third\_party/libc++/trunk/include/\_\_hash\_table:1102:14
#4 0x7f89998858e3 in insert ./../../buildtools/third\_party/libc++/trunk/include/unordered\_set:669:26
#5 0x7f89998858e3 in v8\_inspector::InjectedScript::addPromiseCallback(v8\_inspector::V8InspectorSessionImpl\\*, v8::MaybeLocal<v8::Value>, v8\_inspector::String16 const&, v8\_inspector::WrapMode, bool, bool, std::Cr::unique\_ptr<v8\_inspector::EvaluateCallback, std::Cr::default\_delete<v8\_inspector::EvaluateCallback>>) ./../../v8/src/inspector/injected-script.cc:669:25
#6 0x7f89999d4dc8 in v8\_inspector::(anonymous namespace)::innerCallFunctionOn(v8\_inspector::V8InspectorSessionImpl\\*, v8\_inspector::InjectedScript::Scope&, v8::Local<v8::Value>, v8\_inspector::String16 const&, v8\_crdtp::detail::PtrMaybe<std::Cr::vector<std::Cr::unique\_ptr<v8\_inspector::protocol::Runtime::CallArgument, std::Cr::default\_delete<v8\_inspector::protocol::Runtime::CallArgument>>, std::Cr::allocator<std::Cr::unique\_ptr<v8\_inspector::protocol::Runtime::CallArgument, std::Cr::default\_delete<v8\_inspector::protocol::Runtime::CallArgument>>>>>, bool, v8\_inspector::WrapMode, bool, bool, v8\_inspector::String16 const&, bool, std::Cr::unique\_ptr<v8\_inspector::protocol::Runtime::Backend::CallFunctionOnCallback, std::Cr::default\_delete<v8\_inspector::protocol::Runtime::Backend::CallFunctionOnCallback>>) ./../../v8/src/inspector/v8-runtime-agent-impl.cc:205:27
#7 0x7f89999d320b in v8\_inspector::V8RuntimeAgentImpl::callFunctionOn(v8\_inspector::String16 const&, v8\_crdtp::detail::ValueMaybe<v8\_inspector::String16>, v8\_crdtp::detail::PtrMaybe<std::Cr::vector<std::Cr::unique\_ptr<v8\_inspector::protocol::Runtime::CallArgument, std::Cr::default\_delete<v8\_inspector::protocol::Runtime::CallArgument>>, std::Cr::allocator<std::Cr::unique\_ptr<v8\_inspector::protocol::Runtime::CallArgument, std::Cr::default\_delete<v8\_inspector::protocol::Runtime::CallArgument>>>>>, v8\_crdtp::detail::ValueMaybe<bool>, v8\_crdtp::detail::ValueMaybe<bool>, v8\_crdtp::detail::ValueMaybe<bool>, v8\_crdtp::detail::ValueMaybe<bool>, v8\_crdtp::detail::ValueMaybe<bool>, v8\_crdtp::detail::ValueMaybe<int>, v8\_crdtp::detail::ValueMaybe<v8\_inspector::String16>, v8\_crdtp::detail::ValueMaybe<bool>, v8\_crdtp::detail::ValueMaybe<bool>, std::Cr::unique\_ptr<v8\_inspector::protocol::Runtime::Backend::CallFunctionOnCallback, std::Cr::default\_delete<v8\_inspector::protocol::Runtime::Backend::CallFunctionOnCallback>>) ./../../v8/src/inspector/v8-runtime-agent-impl.cc:422:5
#8 0x7f89998561b4 in v8\_inspector::protocol::Runtime::DomainDispatcherImpl::callFunctionOn(v8\_crdtp::Dispatchable const&) ./gen/v8/src/inspector/protocol/Runtime.cpp:811:16
#9 0x7f8999a57505 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_functional/function.h:854:16
#10 0x7f8999a57505 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_functional/function.h:1193:12
#11 0x7f8999a57505 in v8\_crdtp::UberDispatcher::DispatchResult::Run() ./../../v8/third\_party/inspector\_protocol/crdtp/dispatch.cc:509:3
#12 0x7f89999b0490 in v8\_inspector::V8InspectorSessionImpl::dispatchProtocolMessage(v8\_inspector::StringView) ./../../v8/src/inspector/v8-inspector-session-impl.cc:401:39
#13 0x7f89a3c08add in blink::DevToolsSession::DispatchProtocolCommandImpl(int, WTF::String const&, base::span<unsigned char const, 18446744073709551615ul>) ./../../third\_party/blink/renderer/core/inspector/devtools\_session.cc:232:18
#14 0x7f89a3c07fa8 in blink::DevToolsSession::DispatchProtocolCommand(int, WTF::String const&, base::span<unsigned char const, 18446744073709551615ul>) ./../../third\_party/blink/renderer/core/inspector/devtools\_session.cc:203:10
#15 0x7f899dc28fcf in blink::mojom::blink::DevToolsSessionStubDispatch::Accept(blink::mojom::blink::DevToolsSession\\*, mojo::Message\\*) ./gen/third\_party/blink/public/mojom/devtools/devtools\_agent.mojom-blink.cc:1085:13
#16 0x7f89d2934605 in mojo::InterfaceEndpointClie
\*\*Additional Comments:\*\*
\*\*Chrome version: \*\* 106.0.5249.12 \*\*Channel: \*\* Not sure
\*\*OS:\*\* Linux

## Attachments

- [test.js](attachments/test.js) (text/plain, 732 B)
- [crash.html](attachments/crash.html) (text/plain, 102 B)
- [asan.log](attachments/asan.log) (text/plain, 53.4 KB)

## Timeline

### [Deleted User] (2022-09-22)

[Empty comment from Monorail migration]

### hc...@google.com (2022-09-22)

UAF in log so redirecting to verwaest@ as per go/v8-issue-triage-how-to. Unsure of exact component.

Unconfirmed yet as I don't have a puppeteer instance handy, figured i'd send it through while trying to get that working.

[Monorail components: Blink>JavaScript]

### em...@gmail.com (2022-09-22)


Alternative way,patch the code to  insert  awaitPromise can also quickly confirm this issue.
v8/src/inspector/v8-runtime-agent-impl.cc
if (!response.IsSuccess()) {
    callback->sendFailure(response);
    return;
  }
  + awaitPromise=true; //force trigger awaitPromise
  if (!awaitPromise || scope.tryCatch().HasCaught()) {
    wrapEvaluateResultAsync(scope.injectedScript(), maybeResultValue,
                            scope.tryCatch(), objectGroup, wrapMode,
                            throwOnSideEffect, callback.get());
    return;
  }

  repro step:
  1 ./chrome http://localhost:8000/crash.html
  2 open DevTools,
  3. type "location.reload(" // do not need to enter a closing bracket,
  4. ater print dialog shows,click refres page.

### [Deleted User] (2022-09-22)

[Empty comment from Monorail migration]

### hc...@google.com (2022-09-27)

Confirmed repro in 108

verwaest@ reports that this is probably in an API used only by devtools, so assigning medium severity and reassigning to bmeurer@

bmeurer@, once you investigate could you help identify how long this bug has been around for?

### [Deleted User] (2022-09-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-27)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-27)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-27)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bm...@chromium.org (2022-09-28)

Simon, please take a look.

I'd rate severity as low, since it requires a puppeteer script to trigger the UAF. But might also happen with regular Chrome DevTools.

[Monorail components: -Blink>JavaScript Platform>DevTools>JavaScript]

### sz...@chromium.org (2022-09-28)

I tried to repro this in an inspector-protocol test, but unfortunately `print` is not supported in `content_shell`. Also I didn't get the puppeteer repro to work, only the repro from https://crbug.com/chromium/1366843#c3.

### sz...@chromium.org (2022-09-29)

I also noticed that in a build with DCHECKs enabled, we'll run into this DCHECK in DocumentLoader: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/loader/document_loader.cc;l=972;drc=5eb97d970978084c1724f736cf1d44a82e7e7760

### gi...@appspot.gserviceaccount.com (2022-10-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/699147d17f6fa33a6463313a259b6b40499b9273

commit 699147d17f6fa33a6463313a259b6b40499b9273
Author: Simon Zünd <szuend@chromium.org>
Date: Fri Sep 30 11:47:11 2022

[inspector] Fix user-after-free bug around async evaluations

This CL fixes a use-after-free bug where we try to access an
`InjectedScript` object after it died. This can happen when we
transition into JS and back and the context group dies in the mean
time (e.g. because of a navigation). Normally we check for this but
we missed a call to `Promise#then`.

The access that triggers the UaF is when we try to stash away the
protocol callback function after returning from `Promise#then`.
The callback function is responsible for sending the protocol
response back to DevTools containing the result of the evaluation.

There are two objects with different lifetimes involved:

  - InjectedScript: Owns the `EvaluationCallback`. We keep a
    a reference in case the context group dies. This allows us to
    cancel any pending evaluate requests.

  - ProtocolPromiseHandler: Has a reference to `EvaluationCallback`.
    The handler itself is managed by the V8 GC via `v8::External`
    and a weak `v8::Global`.

When the `ProtocolPromiseHandler` wants use the callback to send
a response, it needs to take ownership first.

We could invert the ownership but it's preferable for evaluation
callbacks to die together with execution contexts and not when the
GC feels like it.

We fix the UaF by using an `InjectedSript::ContextScope` and reloading
the `InjectedScript` after we return from `Promise#then`. Then
we can take proper ownership of the callback and use it in case the
call failed.

R=jarin@chormium.org

Fixed: chromium:1366843
Change-Id: I3a68e8609a9681d7343c71f43cc6e67064f41530
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3925937
Reviewed-by: Jaroslav Sevcik <jarin@chromium.org>
Commit-Queue: Simon Zünd <szuend@chromium.org>
Cr-Commit-Position: refs/heads/main@{#83506}

[add] https://crrev.com/699147d17f6fa33a6463313a259b6b40499b9273/test/inspector/regress/regress-crbug-1366843-expected.txt
[add] https://crrev.com/699147d17f6fa33a6463313a259b6b40499b9273/test/inspector/regress/regress-crbug-1366843.js
[modify] https://crrev.com/699147d17f6fa33a6463313a259b6b40499b9273/src/inspector/injected-script.cc
[modify] https://crrev.com/699147d17f6fa33a6463313a259b6b40499b9273/test/inspector/inspector-test.cc


### gi...@appspot.gserviceaccount.com (2022-10-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/ed5db2eaec82dc28134eb9a0607ca2b5b872e9c0

commit ed5db2eaec82dc28134eb9a0607ca2b5b872e9c0
Author: Simon Zünd <szuend@chromium.org>
Date: Tue Oct 04 06:04:56 2022

[cleanup] Replace raw pointer with std::weak_ptr for EvaluateCallback

This CL replaces the raw pointer in the `ProtocolPromiseHandler` to the
`EvaluateCallback` with a std::weak_ptr. This better matches the
semantics. If the `ProtocolPromiseHandler` is able to lock the
shared_ptr, we still have to remove it from the `InjectedScript`
since the `ProtocolPromiseHandler` sends the response.

R=jarin@chormium.org

Bug: chromium:1366843
Change-Id: I7f371dbd5423f88105981996584ccba5f814dcdb
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3933352
Reviewed-by: Jaroslav Sevcik <jarin@chromium.org>
Commit-Queue: Simon Zünd <szuend@chromium.org>
Cr-Commit-Position: refs/heads/main@{#83508}

[modify] https://crrev.com/ed5db2eaec82dc28134eb9a0607ca2b5b872e9c0/src/inspector/v8-runtime-agent-impl.cc
[modify] https://crrev.com/ed5db2eaec82dc28134eb9a0607ca2b5b872e9c0/src/inspector/injected-script.cc
[modify] https://crrev.com/ed5db2eaec82dc28134eb9a0607ca2b5b872e9c0/src/inspector/injected-script.h


### gi...@appspot.gserviceaccount.com (2022-10-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/bec2a3b3716252fdc98aa3e41a3996711a52d4bf

commit bec2a3b3716252fdc98aa3e41a3996711a52d4bf
Author: Simon Zünd <szuend@chromium.org>
Date: Tue Oct 04 09:21:18 2022

[cleanup] Make it harder to hold EvaluateCallback wrong

This CL shuffles around some code so it becomes impossible to send the
response of an `EvaluateCallback` witout removing it from the owning
`InjectedScript` first.

R=jarin@chromium.org

Bug: chromium:1366843
Change-Id: I6ed8aa767f15802265995ab308cfdfa3fbe5ac0d
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3933353
Commit-Queue: Simon Zünd <szuend@chromium.org>
Reviewed-by: Jaroslav Sevcik <jarin@chromium.org>
Cr-Commit-Position: refs/heads/main@{#83513}

[modify] https://crrev.com/bec2a3b3716252fdc98aa3e41a3996711a52d4bf/src/inspector/injected-script.cc
[modify] https://crrev.com/bec2a3b3716252fdc98aa3e41a3996711a52d4bf/src/inspector/injected-script.h


### [Deleted User] (2022-10-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-04)

[Empty comment from Monorail migration]

### am...@google.com (2022-10-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-10-14)

Congratulations, Cassidy Kim! The VRP Panel has decided to award you $1,000 for this report of a heavily mitigated security bug. Thank you for your efforts in discovering this issue and reporting it to us! 

### am...@google.com (2022-10-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-06-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/7144fdef2edeae2ff39175f4092e2b4900123522

commit 7144fdef2edeae2ff39175f4092e2b4900123522
Author: Igor Sheludko <ishell@chromium.org>
Date: Wed Jun 07 09:56:11 2023

[inspector] Remove outdated test

The test was carefully crafted to setup the UaF conditions but it's
also very sensitive to the timing and the upcoming CL that's going to
change the timing (crrev.com/c/4582948) now make this test report
a memory leak ASan mode because the test completes before the
InjectedScript::ProtocolPromiseHandler's promise callbacks are called
by the microtask queue to free up resources.

Since the conditions the test was intended to trigger are no longer
triggering any issues anyway it's less confusing to just remove
the test instead of trying to keep it "working".

Bug: chromium:1366843, v8:13825
Change-Id: I02b10f09de10ecb5ab5167f3d11cb4ca4b3674ac
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4596058
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Reviewed-by: Simon Zünd <szuend@chromium.org>
Cr-Commit-Position: refs/heads/main@{#88110}

[delete] https://crrev.com/70ce7590c7036f049018bbb5cf3bcf26439df538/test/inspector/regress/regress-crbug-1366843-expected.txt
[delete] https://crrev.com/70ce7590c7036f049018bbb5cf3bcf26439df538/test/inspector/regress/regress-crbug-1366843.js


### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1366843?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061099)*
