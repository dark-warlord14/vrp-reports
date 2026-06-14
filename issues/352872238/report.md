# Webtransport session close crashes browser tab

| Field | Value |
|-------|-------|
| **Issue ID** | [352872238](https://issues.chromium.org/issues/352872238) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Network>WebTransport |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@googlemail.com |
| **Assignee** | ri...@chromium.org |
| **Created** | 2024-07-13 |
| **Bounty** | $7,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

VULNERABILITY DETAILS
Please provide a brief explanation of the security issue.

VERSION
Chrome Version: 126, 127, and Canary tested, but 119 does not show the issue.
Operating System: Linux and Windows 11, I do not think it is OS-dependent
The server side uses the current quiche git.

REPRODUCTION CASE
I may add a simpler reproduction later.
But for now, I am developing/maintaining a node.js package for webtransport support.
Today, I updated the unit tests to newer browser versions (on my machine, not committed).

You find the code for the server side here:
<https://github.com/fails-components/webtransport/blob/a58e330ce680018aecb79477d2cdb3e3830134e9/main/test/fixtures/server.js#L107>

The client side is represented by this test:
<https://github.com/fails-components/webtransport/blob/a58e330ce680018aecb79477d2cdb3e3830134e9/main/test/bidirectional-streams.spec.js#L109>
It runs until:
<https://github.com/fails-components/webtransport/blob/a58e330ce680018aecb79477d2cdb3e3830134e9/main/test/bidirectional-streams.spec.js#L125>
where the user agent crashes. With crashes, I mean, it says:
Fehlercode: STATUS\_ACCESS\_VIOLATION

I do not know if it is a severe crash (security vulnerability) or just a crash, so I filed it using the security template as a precaution.

I have also seen a problem with my unit test for unidirectional streams at the session's close; for now, I assume it has the same cause.

Debugging canary outside the unit tests using windows (also tested on edge) with Visual Studio shows the following stack trace:

```
 	chrome.dll!blink::bindings::DictionaryBase::ToV8(blink::ScriptState * script_state) Zeile 16	C++
 	[Inlineframe] chrome.dll!blink::ToV8Traits<blink::AppBannerPromptResult,void>::ToV8(blink::ScriptState * script_state, const blink::AppBannerPromptResult * dictionary) Zeile 275	C++	chrome.dll!blink::ScriptPromiseResolverBase::ResolveOrReject<blink::AppBannerPromptResult,cppgc::internal::BasicMember<blink::AppBannerPromptResult,cppgc::internal::StrongMemberTag,cppgc::internal::DijkstraWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy,cppgc::internal::CompressedPointer>>(cppgc::internal::BasicMember<blink::AppBannerPromptResult,cppgc::internal::StrongMemberTag,cppgc::internal::DijkstraWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy,cppgc::internal::CompressedPointer> value) Zeile 196	C++
 	[Inlineframe] chrome.dll!blink::ScriptPromiseResolver<blink::WebSocketCloseInfo>::Resolve(cppgc::internal::BasicMember<blink::WebSocketCloseInfo,cppgc::internal::StrongMemberTag,cppgc::internal::DijkstraWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy,cppgc::internal::CompressedPointer> value) Zeile 260	C++
 	chrome.dll!blink::ScriptPromiseProperty<blink::WebSocketCloseInfo,blink::IDLAny>::Promise(blink::DOMWrapperWorld & world) Zeile 75	C++
 	chrome.dll!blink::WebTransport::closed(blink::ScriptState * script_state) Zeile 942	C++
 	chrome.dll!blink::`anonymous namespace'::v8_web_transport::ClosedAttributeGetCallback(const v8::FunctionCallbackInfo<v8::Value> & info) Zeile 181	C++
 	[Externer Code]	
 	chrome.dll!v8::internal::`anonymous namespace'::Invoke(v8::internal::Isolate * isolate, const v8::internal::`anonymous namespace'::InvokeParams & params) Zeile 435	C++
 	chrome.dll!v8::internal::`anonymous namespace'::InvokeWithTryCatch(v8::internal::Isolate * isolate, const v8::internal::`anonymous namespace'::InvokeParams & params) Zeile 477	C++
 	[Inlineframe] chrome.dll!v8::internal::Execution::TryRunMicrotasks(v8::internal::Isolate * isolate, v8::internal::MicrotaskQueue * microtask_queue) Zeile 578	C++
 	[Inlineframe] chrome.dll!v8::internal::MicrotaskQueue::RunMicrotasks(v8::internal::Isolate * isolate) Zeile 185	C++
 	[Inlineframe] chrome.dll!v8::internal::MicrotaskQueue::PerformCheckpointInternal(v8::Isolate * v8_isolate) Zeile 129	C++
 	chrome.dll!v8::internal::MicrotaskQueue::PerformCheckpoint(v8::Isolate * isolate) Zeile 48	C++
 	[Inlineframe] chrome.dll!blink::scheduler::EventLoop::PerformMicrotaskCheckpoint() Zeile 79	C++
 	[Inlineframe] chrome.dll!blink::Agent::PerformMicrotaskCheckpoint() Zeile 135	C++
 	[Inlineframe] chrome.dll!blink::WindowAgent::PerformMicrotaskCheckpoint() Zeile 50	C++
 	[Inlineframe] chrome.dll!() Zeile 0	C++
 	[Inlineframe] chrome.dll!blink::scheduler::AgentGroupSchedulerImpl::PerformMicrotaskCheckpoint() Zeile 117	C++
 	[Inlineframe] chrome.dll!blink::scheduler::MainThreadSchedulerImpl::PerformMicrotaskCheckpoint() Zeile 1137	C++
 	chrome.dll!blink::scheduler::MainThreadSchedulerImpl::OnTaskCompleted(base::WeakPtr<blink::scheduler::MainThreadTaskQueue> queue, const base::sequence_manager::Task & task, base::sequence_manager::TaskQueue::TaskTiming * task_timing, base::LazyNow * lazy_now) Zeile 2284	C++
 	[Inlineframe] chrome.dll!blink::scheduler::MainThreadTaskQueue::OnTaskCompleted(const base::sequence_manager::Task & task, base::sequence_manager::TaskQueue::TaskTiming * task_timing, base::LazyNow * lazy_now) Zeile 174	C++
 	[Inlineframe] chrome.dll!base::internal::DecayedFunctorTraits<void (blink::scheduler::MainThreadTaskQueue::*)(const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *),blink::scheduler::MainThreadTaskQueue *>::Invoke(void(blink::scheduler::MainThreadTaskQueue::*)(const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *) method, blink::scheduler::MainThreadTaskQueue * && receiver_ptr, const base::sequence_manager::Task & args, base::sequence_manager::TaskQueue::TaskTiming * && args, base::LazyNow * && args) Zeile 738	C++
 	[Inlineframe] chrome.dll!base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (blink::scheduler::MainThreadTaskQueue::*const &)(const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *),blink::scheduler::MainThreadTaskQueue *>,void,0>::MakeItSo(void(blink::scheduler::MainThreadTaskQueue::*)(const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *) & functor, const std::__Cr::tuple<base::internal::UnretainedWrapper<blink::scheduler::MainThreadTaskQueue,base::unretained_traits::MayNotDangle,0>> & bound, const base::sequence_manager::Task & args, base::sequence_manager::TaskQueue::TaskTiming * && args, base::LazyNow * && args) Zeile 930	C++
 	[Inlineframe] chrome.dll!base::internal::Invoker<base::internal::FunctorTraits<void (blink::scheduler::MainThreadTaskQueue::*const &)(const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *),blink::scheduler::MainThreadTaskQueue *>,base::internal::BindState<1,1,0,void (blink::scheduler::MainThreadTaskQueue::*)(const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *),base::internal::UnretainedWrapper<blink::scheduler::MainThreadTaskQueue,base::unretained_traits::MayNotDangle,0>>,void (const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *)>::RunImpl(void(blink::scheduler::MainThreadTaskQueue::*)(const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *) & functor, const std::__Cr::tuple<base::internal::UnretainedWrapper<blink::scheduler::MainThreadTaskQueue,base::unretained_traits::MayNotDangle,0>> & bound, std::__Cr::integer_sequence<unsigned long long,0>, const base::sequence_manager::Task & unbound_args, base::sequence_manager::TaskQueue::TaskTiming * && unbound_args, base::LazyNow * && unbound_args) Zeile 1067	C++
 	[Inlineframe] chrome.dll!base::internal::Invoker<base::internal::FunctorTraits<void (blink::scheduler::MainThreadTaskQueue::*const &)(const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *),blink::scheduler::MainThreadTaskQueue *>,base::internal::BindState<1,1,0,void (blink::scheduler::MainThreadTaskQueue::*)(const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *),base::internal::UnretainedWrapper<blink::scheduler::MainThreadTaskQueue,base::unretained_traits::MayNotDangle,0>>,void (const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *)>::Run(base::internal::BindStateBase * base, const base::sequence_manager::Task & unbound_args, base::sequence_manager::TaskQueue::TaskTiming * unbound_args, base::LazyNow * unbound_args) Zeile 987	C++
 	[Inlineframe] chrome.dll!base::RepeatingCallback<void (const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *)>::Run(const base::sequence_manager::Task & args, base::sequence_manager::TaskQueue::TaskTiming * args, base::LazyNow * args) Zeile 344	C++
 	[Inlineframe] chrome.dll!base::sequence_manager::internal::TaskQueueImpl::OnTaskCompleted(const base::sequence_manager::Task & task, base::sequence_manager::TaskQueue::TaskTiming * task_timing, base::LazyNow * lazy_now) Zeile 1376	C++
 	[Inlineframe] chrome.dll!base::sequence_manager::internal::SequenceManagerImpl::NotifyDidProcessTask(base::sequence_manager::internal::SequenceManagerImpl::ExecutingTask * executing_task, base::LazyNow * time_after_task) Zeile 910	C++
 	chrome.dll!base::sequence_manager::internal::SequenceManagerImpl::DidRunTask(base::LazyNow & lazy_now) Zeile 679	C++
 	[Inlineframe] chrome.dll!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow * continuation_lazy_now) Zeile 500	C++
 	chrome.dll!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() Zeile 346	C++
 	chrome.dll!base::MessagePumpDefault::Run(base::MessagePump::Delegate * delegate) Zeile 41	C++
 	chrome.dll!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool application_tasks_allowed, base::TimeDelta timeout) Zeile 657	C++
 	chrome.dll!base::RunLoop::Run(const base::Location & location) Zeile 136	C++
 	chrome.dll!content::RendererMain(content::MainFunctionParams parameters) Zeile 367	C++
 	chrome.dll!content::RunOtherNamedProcessTypeMain(const std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char>> & process_type, content::MainFunctionParams main_function_params, content::ContentMainDelegate * delegate) Zeile 798	C++
 	chrome.dll!content::ContentMainRunnerImpl::Run() Zeile 1177	C++
 	[Inlineframe] chrome.dll!content::RunContentProcess(content::ContentMainParams params, content::ContentMainRunner * content_main_runner) Zeile 333	C++
 	chrome.dll!content::ContentMain(content::ContentMainParams params) Zeile 346	C++
 	chrome.dll!ChromeMain(HINSTANCE__ * instance, sandbox::SandboxInterfaceInfo * sandbox_info, __int64 exe_entry_point_ticks) Zeile 230	C++
 	chrome.exe!MainDllLoader::Launch(HINSTANCE__ * instance, base::TimeTicks exe_entry_point_ticks) Zeile 181	C++
 	chrome.exe!wWinMain(HINSTANCE__ * instance, HINSTANCE__ * prev, wchar_t *, int) Zeile 351	C++
 	[Externer Code]	

```

What I found interesting is that the `blink::WebTransportCloseInfo` object is converted to a `blink::WebSocketCloseInfo`. This may be a side effect of the change of the close code type in web transport, which now matches the WebSocketCloseInfo???

The code owner of the affected code is [ricea@chromium.org](mailto:ricea@chromium.org) .

Besides, I am sitting at the debugger and do not have a clue what caused it, as I am not that familiar with the code. If this changes, I may report more information later.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: Tab crash
Crash State: See stack trace above
crash id: 718f5204b07e6a81
Client ID (if relevant): [see link above]

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: Marten Richter [marten.richter@tu-berlin.de](mailto:marten.richter@tu-berlin.de)

## Timeline

### ma...@googlemail.com (2024-07-13)

Interesting, if I change the last part of the code to:

```
const closed = client.closed

  // redirect input to output
  try {
    await bidiStream.readable.pipeTo(bidiStream.writable)
  } catch (error) {
    console.log('Pipe to error (ignore)', error) // Actually all you can get is, that the fin is catched
  }

  // the remote will close the session
  //  const result = await client.closed
  await closed

```

So moving the getter of the closed promise up, everything runs through.
It seems that the client object so the Webtransport object becomes invalid after the pipeTo.
It also works in this way:

```
  const closed = client.closed

  // redirect input to output
  try {
    await bidiStream.readable.pipeTo(bidiStream.writable)
  } catch (error) {
    console.log('Pipe to error (ignore)', error) // Actually, all you can get is, that the fin is catched
  }

  // the remote will close the session
  //  const result = await client.closed
  const result = await client.closed

```

So, I am not sure if this is really a pure web transport issue.

### ma...@googlemail.com (2024-07-14)

I have browsed a bit through the git. Given that it worked with 119 and did not work with 126, I would guess that the typed promise refactoring work by [japhet@chromium.org](mailto:japhet@chromium.org) may be the cause. (But it is still speculation.) If this is the case, all bindings addressed by this change may be affected. (But as I did not really find the cause other changes, which I did not relate are also possible.)

### ja...@chromium.org (2024-07-16)

Hi, thanks for the bug report. It would be helpful if you can provide a small proof of concept in a file.

If I understand correctly, when you run the test case, it now fails on M126: <https://github.com/fails-components/webtransport/blob/a58e330ce680018aecb79477d2cdb3e3830134e9/main/test/bidirectional-streams.spec.js#L109>

Is this an issue that can be triggered when a user browses to a specially crafted web page?

### ja...@chromium.org (2024-07-16)

I haven't been able to reproduce this issue yet and have asked the bug reporter for more information, including a proof of concept file, but cc'ing japhet@ and ricea@ in case they can spot the issue. Adding blink as the component for now.

### ma...@googlemail.com (2024-07-16)

> Hi, thanks for the bug report. It would be helpful if you can provide a small proof of concept in a file.

I will try. I am working in parallel on a bug report demonstration for Firefox (a different test), which also crashes. At the moment, I am stuck establishing a secure context for WebTransport at the example, so it will take a while.

> If I understand correctly, when you run the test case, it now fails on M126: <https://github.com/fails-components/webtransport/blob/a58e330ce680018aecb79477d2cdb3e3830134e9/main/test/bidirectional-streams.spec.js#L109>

Yes, this is correct (additionally, one of the unidirectional stream tests probably has the same issue).

> Is this an issue that can be triggered when a user browses to a specially crafted web page?

Yes, all you need to set up a web server and a web transport server, and a user tab will crash. At the moment, how harmful the crash is is unclear as the cause is not really understood.

### pe...@google.com (2024-07-16)

Thank you for providing more feedback. Adding the requester to the CC list.

### dr...@chromium.org (2024-07-16)

[security shepherd] I was able to reproduce this by copying your [test code](https://github.com/fails-components/webtransport/blob/a58e330ce680018aecb79477d2cdb3e3830134e9/main/test/bidirectional-streams.spec.js#L108-L125) to third\_party/blink/web\_tests/external/wpt/webtransport/close.https.any.js, and then running the webtransport server following [the docs](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/web_tests/external/wpt/webtransport/README.md).

This seems like memory corruption in the renderer process without any user interaction, which is High severity. ricea@ - can you take a look?

### ma...@googlemail.com (2024-07-17)

Perfect, then I do not have to write demonstration code.
When you check it, please also look at the unidirectional tests. One of them also did not work. I did not run it outside the test harness, so I do not know if it is also a tab crash, but I assume it has the same origin. Comparing the two tests and looking for similarities and differences may help identify the cause.

### pe...@google.com (2024-07-17)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-07-17)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ri...@chromium.org (2024-07-18)

#8 I cannot reproduce. Could you provide me with the files you used?

This could be a toolchain bug. If it's calling WebSocketCloseInfo methods on a WebTransportCloseInfo object, that could lead to a crash, as the two classes are actually different.

### ma...@googlemail.com (2024-07-18)

> This could be a toolchain bug. If it's calling WebSocketCloseInfo methods on a WebTransportCloseInfo object, that could lead to a crash, as the two classes are actually different.

That is also what I thought (some template type confusion as WebSocketCloseInfo and WebTransportCloseInfo have the structure). But do Windows and Linux builds use the same compilers? (I am asking as my unit tests run on Linux container using playwright and also crashed, and the other test were on Windows using Chrome and Edge).
But can also be that MSVC Debugger outputs nonsense.

### ri...@chromium.org (2024-07-18)

#8 Never mind, I have reproduced now. I will upload a repro later.

### ri...@chromium.org (2024-07-18)

Okay, I found the problem. In blink::WebTransport::OnClosed() we create a WebTransportCloseInfo object on the stack, and then pass a pointer to it to Cleanup(). Before the change to use ScriptPromiseProperty in <https://chromium-review.googlesource.com/c/chromium/src/+/5353700> this used to be immediately converted to a v8 object, but now a pointer to the original C++ object is retained inside the ScriptPromiseProperty object. The pointer becomes invalid as soon as OnClosed() returns.

You will only run into the problem if the server performs a clean close of the WebTransport session before JavaScript looks at the "closed" Promise. Once JavaScript has looked at it, the value is cached and the v8 dictionary is created synchronously.

This is potentially exploitable if an attacker finds a way to control the contents of the vtable pointer for WebTransportCloseInfo on the stack.

### ri...@chromium.org (2024-07-19)

Fix in progress at <https://chromium-review.googlesource.com/c/chromium/src/+/5725413>.

### ap...@google.com (2024-07-23)

Project: chromium/src
Branch: main

commit 84c1481d8a8d5e7f51316b648d1bf71f2ae52122
Author: Adam Rice <ricea@chromium.org>
Date:   Tue Jul 23 03:35:53 2024

    Don't allocate WebTransportCloseInfo on stack
    
    blink::WebTransport::OnClosed() was allocating a WebTransportCloseInfo
    object on the stack. Since it is a garbage-collected object, this is
    wrong. Allocate it with MakeGarbageCollected<>() instead.
    
    Fixed: 352872238
    Change-Id: I83484021d5f3f6d49d3c222c8f2dc34219f2d240
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5725413
    Commit-Queue: Nidhi Jaju <nidhijaju@chromium.org>
    Reviewed-by: Nidhi Jaju <nidhijaju@chromium.org>
    Auto-Submit: Adam Rice <ricea@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1331525}

M       third_party/blink/renderer/modules/webtransport/web_transport.cc
M       third_party/blink/renderer/modules/webtransport/web_transport_test.cc
M       third_party/blink/web_tests/external/wpt/webtransport/close.https.any-expected.txt
M       third_party/blink/web_tests/external/wpt/webtransport/close.https.any.js
M       third_party/blink/web_tests/external/wpt/webtransport/close.https.any.serviceworker-expected.txt
M       third_party/blink/web_tests/external/wpt/webtransport/close.https.any.sharedworker-expected.txt
M       third_party/blink/web_tests/external/wpt/webtransport/close.https.any.worker-expected.txt
A       third_party/blink/web_tests/external/wpt/webtransport/handlers/server-read-then-close.py

https://chromium-review.googlesource.com/5725413


### ri...@chromium.org (2024-07-23)

This will need a merge to M127 and M128.

### pe...@google.com (2024-07-23)

Requesting merge to extended stable (M126) because latest trunk commit (1331525) appears to be after extended stable branch point (1300313).
Requesting merge to stable (M127) because latest trunk commit (1331525) appears to be after stable branch point (1313161).
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### pe...@google.com (2024-07-24)

Merge review required: M127 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), alonbajayo (ChromeOS), danielyip (Desktop)

### pe...@google.com (2024-07-24)

Merge review required: M126 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), ceb (ChromeOS), srinivassista (Desktop)

### ri...@chromium.org (2024-07-24)

Re: #19

> 1. Which CLs should be backmerged? (Please include Gerrit links.)

<https://chromium-review.googlesource.com/c/chromium/src/+/5725413>

> Has this fix been verified on Canary to not pose any stability regressions?

Landed in Canary 129.0.6614.0. No relevant crashes so far.

> Does this fix pose any potential non-verifiable stability risks?

No, it is believed safe.

> Does this fix pose any known compatibility risks?

None.

> Does it require manual verification by the test team? If so, please describe required testing.

No.

### ri...@chromium.org (2024-07-24)

Responding for M126 and M127 simultaneously:

> Why does your merge fit within the merge criteria for these milestones?
> Chrome Browser: <https://chromiumdash.appspot.com/branches>

It's a high-severity security bug.

> What changes specifically would you like to merge? Please link to Gerrit.

<https://chromium-review.googlesource.com/c/chromium/src/+/5725413>

> Have the changes been released and tested on canary?

Landed in Canary 129.0.6614.0. Passing automated tests.

> Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No. Security fix to an existing feature.

> If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

No. The fix includes fully automated testing.

### ma...@googlemail.com (2024-07-24)

May be a stupid question, but what is about M128? (It just branched out on Monday?)

### ri...@chromium.org (2024-07-24)

#24 Not a stupid question. I added a merge request for 128. Thanks.

### pe...@google.com (2024-07-24)

**Merge approved:** your change passed merge requirements and is auto-approved for M128. Please go ahead and merge the CL to branch 6613 (refs/branch-heads/6613) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: harrysouders (Android), harrysouders (iOS), obenedict (ChromeOS), pbommana (Desktop)

### am...@chromium.org (2024-07-24)

this is in our security merge review queue -- since this fix was just landed on the 22nd it needed relevant bake time. it will be reviewed later today or tomorrow for merge before the deadlines for next M126 Extended and M127 Stable

### am...@chromium.org (2024-07-25)

merges approved for <https://crrev.com/c/5725413>, please merge this fix to M127 branch 6533 and M126 branch 6478 at soonest / before 10am Pacific Friday, 26 July so this fix can be included in the next updates of Stable and Extended Stable -- thanks!

### ap...@google.com (2024-07-25)

Project: chromium/src
Branch: refs/branch-heads/6478

commit d9f7652c867c474738055eb362cb064f98c9ebc4
Author: Adam Rice <ricea@chromium.org>
Date:   Thu Jul 25 05:28:45 2024

    Don't allocate WebTransportCloseInfo on stack
    
    blink::WebTransport::OnClosed() was allocating a WebTransportCloseInfo
    object on the stack. Since it is a garbage-collected object, this is
    wrong. Allocate it with MakeGarbageCollected<>() instead.
    
    (cherry picked from commit 84c1481d8a8d5e7f51316b648d1bf71f2ae52122)
    
    Fixed: 352872238
    Change-Id: I83484021d5f3f6d49d3c222c8f2dc34219f2d240
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5725413
    Commit-Queue: Nidhi Jaju <nidhijaju@chromium.org>
    Reviewed-by: Nidhi Jaju <nidhijaju@chromium.org>
    Auto-Submit: Adam Rice <ricea@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1331525}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5740536
    Commit-Queue: Adam Rice <ricea@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6478@{#1848}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       third_party/blink/renderer/modules/webtransport/web_transport.cc
M       third_party/blink/renderer/modules/webtransport/web_transport_test.cc
M       third_party/blink/web_tests/external/wpt/webtransport/close.https.any-expected.txt
M       third_party/blink/web_tests/external/wpt/webtransport/close.https.any.js
M       third_party/blink/web_tests/external/wpt/webtransport/close.https.any.serviceworker-expected.txt
M       third_party/blink/web_tests/external/wpt/webtransport/close.https.any.sharedworker-expected.txt
M       third_party/blink/web_tests/external/wpt/webtransport/close.https.any.worker-expected.txt
A       third_party/blink/web_tests/external/wpt/webtransport/handlers/server-read-then-close.py

https://chromium-review.googlesource.com/5740536


### ap...@google.com (2024-07-25)

Project: chromium/src
Branch: refs/branch-heads/6613

commit 3031aee4544d4045ce94dc6cc785817d0497da09
Author: Adam Rice <ricea@chromium.org>
Date:   Thu Jul 25 05:43:30 2024

    Don't allocate WebTransportCloseInfo on stack
    
    blink::WebTransport::OnClosed() was allocating a WebTransportCloseInfo
    object on the stack. Since it is a garbage-collected object, this is
    wrong. Allocate it with MakeGarbageCollected<>() instead.
    
    (cherry picked from commit 84c1481d8a8d5e7f51316b648d1bf71f2ae52122)
    
    Fixed: 352872238
    Change-Id: I83484021d5f3f6d49d3c222c8f2dc34219f2d240
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5725413
    Commit-Queue: Nidhi Jaju <nidhijaju@chromium.org>
    Reviewed-by: Nidhi Jaju <nidhijaju@chromium.org>
    Auto-Submit: Adam Rice <ricea@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1331525}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5740537
    Commit-Queue: Adam Rice <ricea@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6613@{#72}
    Cr-Branched-From: 03c1799e6f9c7239802827eab5e935b9e14fceae-refs/heads/main@{#1331488}

M       third_party/blink/renderer/modules/webtransport/web_transport.cc
M       third_party/blink/renderer/modules/webtransport/web_transport_test.cc
M       third_party/blink/web_tests/external/wpt/webtransport/close.https.any-expected.txt
M       third_party/blink/web_tests/external/wpt/webtransport/close.https.any.js
M       third_party/blink/web_tests/external/wpt/webtransport/close.https.any.serviceworker-expected.txt
M       third_party/blink/web_tests/external/wpt/webtransport/close.https.any.sharedworker-expected.txt
M       third_party/blink/web_tests/external/wpt/webtransport/close.https.any.worker-expected.txt
A       third_party/blink/web_tests/external/wpt/webtransport/handlers/server-read-then-close.py

https://chromium-review.googlesource.com/5740537


### ap...@google.com (2024-07-25)

Project: chromium/src
Branch: refs/branch-heads/6533

commit 459645d5f572be89cee46670c0ba42f719a3f844
Author: Adam Rice <ricea@chromium.org>
Date:   Thu Jul 25 05:50:09 2024

    Don't allocate WebTransportCloseInfo on stack
    
    blink::WebTransport::OnClosed() was allocating a WebTransportCloseInfo
    object on the stack. Since it is a garbage-collected object, this is
    wrong. Allocate it with MakeGarbageCollected<>() instead.
    
    (cherry picked from commit 84c1481d8a8d5e7f51316b648d1bf71f2ae52122)
    
    Fixed: 352872238
    Change-Id: I83484021d5f3f6d49d3c222c8f2dc34219f2d240
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5725413
    Commit-Queue: Nidhi Jaju <nidhijaju@chromium.org>
    Reviewed-by: Nidhi Jaju <nidhijaju@chromium.org>
    Auto-Submit: Adam Rice <ricea@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1331525}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5740933
    Commit-Queue: Adam Rice <ricea@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6533@{#1807}
    Cr-Branched-From: 7e0b87ec6b8cb5cb2969e1479fc25776e582721d-refs/heads/main@{#1313161}

M       third_party/blink/renderer/modules/webtransport/web_transport.cc
M       third_party/blink/renderer/modules/webtransport/web_transport_test.cc
M       third_party/blink/web_tests/external/wpt/webtransport/close.https.any-expected.txt
M       third_party/blink/web_tests/external/wpt/webtransport/close.https.any.js
M       third_party/blink/web_tests/external/wpt/webtransport/close.https.any.serviceworker-expected.txt
M       third_party/blink/web_tests/external/wpt/webtransport/close.https.any.sharedworker-expected.txt
M       third_party/blink/web_tests/external/wpt/webtransport/close.https.any.worker-expected.txt
A       third_party/blink/web_tests/external/wpt/webtransport/handlers/server-read-then-close.py

https://chromium-review.googlesource.com/5740933


### ma...@googlemail.com (2024-07-29)

I have looked at:
<https://chromiumdash.appspot.com/commit/639df13d56714ca8fb42557268499489fc83d664> (the commit, which introduced the problem)
and
<https://chromiumdash.appspot.com/releases?platform=FuchsiaWebEngine>
If I am correct, then Fuchsia WebEngine would use a vulnerable M124. But please double-check, as I am not experienced with your release cycle.

### am...@chromium.org (2024-07-29)

This has been merged to all the active release channels of Chrome. Fuchsia merges and merge decisions are not handled here.

### am...@google.com (2024-07-29)

Also, I've just noted this elsewhere but realize it was noted here. This looks like it resulted in an OOB read. OOB reads are generally triaged as medium severity, so I don't believe this would be a critical backmerge for Fuchsia regardless.

### ri...@chromium.org (2024-07-30)

#34 The read is of an object vtable. If it is exploitable, then it is an arbitrary code execution vulnerability in the render process.

### sp...@google.com (2024-07-31)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
$7,000 for report of memory corruption in a sandboxed process / renderer


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-07-31)

Congratulations -- thank you for your efforts and reporting this issue to us.

### ap...@google.com (2024-08-02)

Project: chromium/src
Branch: refs/branch-heads/6478_182

commit 993c1a03b44000330fcecf5a285f19d11cc60442
Author: Adam Rice <ricea@chromium.org>
Date:   Fri Aug 02 17:03:07 2024

    [CfM-R126] Don't allocate WebTransportCloseInfo on stack
    
    blink::WebTransport::OnClosed() was allocating a WebTransportCloseInfo
    object on the stack. Since it is a garbage-collected object, this is
    wrong. Allocate it with MakeGarbageCollected<>() instead.
    
    (cherry picked from commit 84c1481d8a8d5e7f51316b648d1bf71f2ae52122)
    
    (cherry picked from commit d9f7652c867c474738055eb362cb064f98c9ebc4)
    
    Fixed: 352872238
    Change-Id: I83484021d5f3f6d49d3c222c8f2dc34219f2d240
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5725413
    Commit-Queue: Nidhi Jaju <nidhijaju@chromium.org>
    Reviewed-by: Nidhi Jaju <nidhijaju@chromium.org>
    Auto-Submit: Adam Rice <ricea@chromium.org>
    Cr-Original-Original-Commit-Position: refs/heads/main@{#1331525}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5740536
    Commit-Queue: Adam Rice <ricea@chromium.org>
    Cr-Original-Commit-Position: refs/branch-heads/6478@{#1848}
    Cr-Original-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5758107
    Owners-Override: Kyle Williams <kdgwill@chromium.org>
    Commit-Queue: Kyle Williams <kdgwill@chromium.org>
    Reviewed-by: Niko Tsirakis <ntsirakis@google.com>
    Auto-Submit: Kyle Williams <kdgwill@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6478_182@{#53}
    Cr-Branched-From: 5b5d8292ddf182f8b2096fa665b473b6317906d5-refs/branch-heads/6478@{#1776}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       third_party/blink/renderer/modules/webtransport/web_transport.cc
M       third_party/blink/renderer/modules/webtransport/web_transport_test.cc
M       third_party/blink/web_tests/external/wpt/webtransport/close.https.any-expected.txt
M       third_party/blink/web_tests/external/wpt/webtransport/close.https.any.js
M       third_party/blink/web_tests/external/wpt/webtransport/close.https.any.serviceworker-expected.txt
M       third_party/blink/web_tests/external/wpt/webtransport/close.https.any.sharedworker-expected.txt
M       third_party/blink/web_tests/external/wpt/webtransport/close.https.any.worker-expected.txt
A       third_party/blink/web_tests/external/wpt/webtransport/handlers/server-read-then-close.py

https://chromium-review.googlesource.com/5758107


### pe...@google.com (2024-10-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/352872238)*
