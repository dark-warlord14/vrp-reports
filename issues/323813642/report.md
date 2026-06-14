# UAF in v8_inspector

| Field | Value |
|-------|-------|
| **Issue ID** | [323813642](https://issues.chromium.org/issues/323813642) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools>Sources |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | sz...@google.com |
| **Created** | 2024-02-05 |
| **Bounty** | $3,000.00 |

## Description

tested os:
ubuntu 22.04
tested chrome version:
stable & beta & dev

component:Platform>DevTools>JavaScript

repro steps:
1. ~./chrome  --user-data-dir=/tmp/xx1 
2. open the devtools.
2. open page http://localhost:8880/crash.html

You should see the UAF crash in a few seconds.

==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x50d0003a2078 at pc 0x560782104db6 bp 0x7f461763d470 sp 0x7f461763d468
READ of size 8 at 0x50d0003a2078 thread T35 (DedicatedWorker)
    #0 0x560782104db5 in v8_inspector::protocol::Runtime::Frontend::exceptionThrown(double, std::__Cr::unique_ptr<v8_inspector::protocol::Runtime::ExceptionDetails, std::__Cr::default_delete<v8_inspector::protocol::Runtime::ExceptionDetails>>) ./gen/v8/src/inspector/protocol/Runtime.cpp:498:10
    #1 0x560782153749 in v8_inspector::V8ConsoleMessage::reportToFrontend(v8_inspector::protocol::Runtime::Frontend*, v8_inspector::V8InspectorSessionImpl*, bool) const ./../../v8/src/inspector/v8-console-message.cc:340:15
    #2 0x56078221864e in reportMessage ./../../v8/src/inspector/v8-runtime-agent-impl.cc:1155:12
    #3 0x56078221864e in v8_inspector::V8RuntimeAgentImpl::messageAdded(v8_inspector::V8ConsoleMessage*) ./../../v8/src/inspector/v8-runtime-agent-impl.cc:1150:18
    #4 0x5607821e1607 in operator() ./../../third_party/libc++/src/include/__functional/function.h:711:12
    #5 0x5607821e1607 in operator() ./../../third_party/libc++/src/include/__functional/function.h:978:10
    #6 0x5607821e1607 in v8_inspector::V8InspectorImpl::forEachSession(int, std::__Cr::function<void (v8_inspector::V8InspectorSessionImpl*)> const&) ./../../v8/src/inspector/v8-inspector-impl.cc:430:40
    #7 0x56078215736e in v8_inspector::V8ConsoleMessageStorage::addMessage(std::__Cr::unique_ptr<v8_inspector::V8ConsoleMessage, std::__Cr::default_delete<v8_inspector::V8ConsoleMessage>>) ./../../v8/src/inspector/v8-console-message.cc:567:14
    #8 0x5607821e3366 in v8_inspector::V8InspectorImpl::exceptionThrown(v8::Local<v8::Context>, v8_inspector::StringView, v8::Local<v8::Value>, v8_inspector::StringView, v8_inspector::StringView, unsigned int, unsigned int, std::__Cr::unique_ptr<v8_inspector::V8StackTrace, std::__Cr::default_delete<v8_inspector::V8StackTrace>>, int) ./../../v8/src/inspector/v8-inspector-impl.cc:296:41
    #9 0x56079948116b in blink::ThreadDebuggerCommonImpl::PromiseRejected(v8::Local<v8::Context>, WTF::String const&, v8::Local<v8::Value>, std::__Cr::unique_ptr<blink::SourceLocation, std::__Cr::default_delete<blink::SourceLocation>>) ./../../third_party/blink/renderer/core/inspector/thread_debugger_common_impl.cc:146:28
    #10 0x560797acb343 in blink::RejectedPromises::Message::Report() ./../../third_party/blink/renderer/bindings/core/v8/rejected_promises.cc:90:43
    #11 0x560797ac919f in blink::RejectedPromises::ProcessQueueNow(WTF::Vector<std::__Cr::unique_ptr<blink::RejectedPromises::Message, std::__Cr::default_delete<blink::RejectedPromises::Message>>, 0u, WTF::PartitionAllocator>) ./../../third_party/blink/renderer/bindings/core/v8/rejected_promises.cc:268:16
    #12 0x560797acce79 in void base::internal::FunctorTraits<void (blink::RejectedPromises::*)(WTF::Vector<std::__Cr::unique_ptr<blink::RejectedPromises::Message, std::__Cr::default_delete<blink::RejectedPromises::Message>>, 0u, WTF::PartitionAllocator>)>::Invoke<void (blink::RejectedPromises::*)(WTF::Vector<std::__Cr::unique_ptr<blink::RejectedPromises::Message, std::__Cr::default_delete<blink::RejectedPromises::Message>>, 0u, WTF::PartitionAllocator>), scoped_refptr<blink::RejectedPromises>, WTF::Vector<std::__Cr::unique_ptr<blink::RejectedPromises::Message, std::__Cr::default_delete<blink::RejectedPromises::Message>>, 0u, WTF::PartitionAllocator>>(void (blink::RejectedPromises::*)(WTF::Vector<std::__Cr::unique_ptr<blink::RejectedPromises::Message, std::__Cr::default_delete<blink::RejectedPromises::Message>>, 0u, WTF::PartitionAllocator>), scoped_refptr<blink::RejectedPromises>&&, WTF::Vector<std::__Cr::unique_ptr<blink::RejectedPromises::Message, std::__Cr::default_delete<blink::RejectedPromises::Message>>, 0u, WTF::PartitionAllocator>&&) ./../../base/functional/bind_internal.h:710:12
    #13 0x560797accc79 in MakeItSo<void (blink::RejectedPromises::*)(WTF::Vector<std::__Cr::unique_ptr<blink::RejectedPromises::Message, std::__Cr::default_delete<blink::RejectedPromises::Message> >, 0U, WTF::PartitionAllocator>), std::__Cr::tuple<scoped_refptr<blink::RejectedPromises>, WTF::Vector<std::__Cr::unique_ptr<blink::RejectedPromises::Message, std::__Cr::default_delete<blink::RejectedPromises::Message> >, 0U, WTF::PartitionAllocator> > > ./../../base/functional/bind_internal.h:860:12
    #14 0x560797accc79 in RunImpl<void (blink::RejectedPromises::*)(WTF::Vector<std::__Cr::unique_ptr<blink::RejectedPromises::Message, std::__Cr::default_delete<blink::RejectedPromises::Message> >, 0U, WTF::PartitionAllocator>), std::__Cr::tuple<scoped_refptr<blink::RejectedPromises>, WTF::Vector<std::__Cr::unique_ptr<blink::RejectedPromises::Message, std::__Cr::default_delete<blink::RejectedPromises::Message> >, 0U, WTF::PartitionAllocator> >, 0UL, 1UL> ./../../base/functional/bind_internal.h:991:14
    #15 0x560797accc79 in base::internal::Invoker<base::internal::BindState<void (blink::RejectedPromises::*)(WTF::Vector<std::__Cr::unique_ptr<blink::RejectedPromises::Message, std::__Cr::default_delete<blink::RejectedPromises::Message>>, 0u, WTF::PartitionAllocator>), scoped_refptr<blink::RejectedPromises>, WTF::Vector<std::__Cr::unique_ptr<blink::RejectedPromises::Message, std::__Cr::default_delete<blink::RejectedPromises::Message>>, 0u, WTF::PartitionAllocator>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:904:12
    #16 0x56078c2e5a84 in Run ./../../base/functional/callback.h:156:12
    #17 0x56078c2e5a84 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:201:34
    #18 0x56078c344a8f in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:480:11)> ./../../base/task/common/task_annotator.h:89:5
    #19 0x56078c344a8f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:478:23
    #20 0x56078c343a89 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:343:41
    #21 0x56078c34584a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #22 0x56078c1ded8c in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:40:55
    #23 0x56078c34657f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:646:12
    #24 0x56078c27a10f in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #25 0x560788b5d8bc in blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run() ./../../third_party/blink/renderer/platform/scheduler/worker/non_main_thread_impl.cc:182:14
    #26 0x56078c40add7 in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:103:13
    #27 0x56077a897918 in asan_thread_start(void*) _asan_rtl_:28

0x50d0003a2078 is located 24 bytes inside of 144-byte region [0x50d0003a2060,0x50d0003a20f0)
freed by thread T35 (DedicatedWorker) here:
    #0 0x56077a8ce0bd in operator delete(void*) _asan_rtl_:3
    #1 0x5607821f26f8 in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:66:5
    #2 0x5607821f26f8 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:266:7
    #3 0x5607821f26f8 in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:236:71
    #4 0x5607821f26f8 in v8_inspector::V8InspectorSessionImpl::~V8InspectorSessionImpl() ./../../v8/src/inspector/v8-inspector-session-impl.cc:169:1
    #5 0x5607821f2d93 in v8_inspector::V8InspectorSessionImpl::~V8InspectorSessionImpl() ./../../v8/src/inspector/v8-inspector-session-impl.cc:160:51
    #6 0x5607995a0eac in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:66:5
    #7 0x5607995a0eac in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:266:7
    #8 0x5607995a0eac in blink::DevToolsSession::Detach() ./../../third_party/blink/renderer/core/inspector/devtools_session.cc:215:15
    #9 0x5607995ad042 in Invoke<void (blink::DevToolsSession::*)(), const cppgc::internal::BasicPersistent<blink::DevToolsSession, cppgc::internal::WeakPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy> &> ./../../base/functional/bind_internal.h:710:12
    #10 0x5607995ad042 in MakeItSo<void (blink::DevToolsSession::*)(), std::__Cr::tuple<cppgc::internal::BasicPersistent<blink::DevToolsSession, cppgc::internal::WeakPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy> > > ./../../base/functional/bind_internal.h:881:5
    #11 0x5607995ad042 in RunImpl<void (blink::DevToolsSession::*)(), std::__Cr::tuple<cppgc::internal::BasicPersistent<blink::DevToolsSession, cppgc::internal::WeakPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy> >, 0UL> ./../../base/functional/bind_internal.h:991:14
    #12 0x5607995ad042 in base::internal::Invoker<base::internal::BindState<void (blink::DevToolsSession::*)(), cppgc::internal::BasicPersistent<blink::DevToolsSession, cppgc::internal::WeakPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:904:12
    #13 0x56078d976002 in Run ./../../base/functional/callback.h:156:12
    #14 0x56078d976002 in mojo::InterfaceEndpointClient::NotifyError(std::__Cr::optional<mojo::DisconnectReason> const&) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:744:31
    #15 0x56078d99c676 in mojo::internal::MultiplexRouter::ProcessNotifyErrorTask(mojo::internal::MultiplexRouter::Task*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:1010:13
    #16 0x56078d993b24 in mojo::internal::MultiplexRouter::ProcessTasks(mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:923:15
    #17 0x56078d99da78 in mojo::internal::MultiplexRouter::LockAndCallProcessTasks() ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:1124:3
    #18 0x56078d99f0e4 in Invoke<void (mojo::internal::MultiplexRouter::*)(), scoped_refptr<mojo::internal::MultiplexRouter> > ./../../base/functional/bind_internal.h:710:12
    #19 0x56078d99f0e4 in MakeItSo<void (mojo::internal::MultiplexRouter::*)(), std::__Cr::tuple<scoped_refptr<mojo::internal::MultiplexRouter> > > ./../../base/functional/bind_internal.h:860:12
    #20 0x56078d99f0e4 in RunImpl<void (mojo::internal::MultiplexRouter::*)(), std::__Cr::tuple<scoped_refptr<mojo::internal::MultiplexRouter> >, 0UL> ./../../base/functional/bind_internal.h:991:14
    #21 0x56078d99f0e4 in base::internal::Invoker<base::internal::BindState<void (mojo::internal::MultiplexRouter::*)(), scoped_refptr<mojo::internal::MultiplexRouter>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:904:12
    #22 0x56078c2e5a84 in Run ./../../base/functional/callback.h:156:12
    #23 0x56078c2e5a84 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:201:34
    #24 0x56078c344a8f in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:480:11)> ./../../base/task/common/task_annotator.h:89:5
    #25 0x56078c344a8f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:478:23
    #26 0x56078c343a89 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:343:41
    #27 0x56078c34584a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #28 0x56078c1ded8c in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:40:55
    #29 0x56078c34668e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:643:12
    #30 0x56078c27a10f in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #31 0x5607a31a7bf3 in content::(anonymous namespace)::NestedMessageLoopRunnerImpl::Run() ./../../content/child/blink_platform_impl.cc:88:14
    #32 0x56079ad736e5 in blink::WorkerThread::PauseOrFreezeOnWorkerThread(blink::mojom::FrameLifecycleState, bool) ./../../third_party/blink/renderer/core/workers/worker_thread.cc:916:20
    #33 0x5607802ff331 in v8::internal::Isolate::InvokeApiInterruptCallbacks() ./../../v8/src/execution/isolate.cc:1739:5
    #34 0x56078036027c in v8::internal::StackGuard::HandleInterrupts(v8::internal::StackGuard::InterruptLevel) ./../../v8/src/execution/stack-guard.cc:371:15
    #35 0x5607812d683f in __RT_impl_Runtime_StackGuard ./../../v8/src/runtime/runtime-internal.cc:354:34
    #36 0x5607812d683f in v8::internal::Runtime_StackGuard(int, unsigned long*, v8::internal::Isolate*) ./../../v8/src/runtime/runtime-internal.cc:343:1
    #37 0x56078369ee75 in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit setup-isolate-deserialize.cc:0:0
    #38 0x560783682026 in Builtins_SetPrototypeAdd setup-isolate-deserialize.cc:0:0
    #39 0x5607836037db in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc:0:0
    #40 0x560783603506 in Builtins_JSEntry setup-isolate-deserialize.cc:0:0
    #41 0x5607802bd85d in Call ./../../v8/src/execution/simulator.h:178:12
    #42 0x5607802bd85d in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:418:22
    #43 0x5607802c074a in v8::internal::Execution::CallBuiltin(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) ./../../v8/src/execution/execution.cc:526:10
    #44 0x56077fe752f8 in v8::Set::Add(v8::Local<v8::Context>, v8::Local<v8::Value>) ./../../v8/src/api/api.cc:8502:20
    #45 0x56078222d634 in v8_inspector::ValueMirror::getProperties(v8::Local<v8::Context>, v8::Local<v8::Object>, bool, bool, bool, v8_inspector::ValueMirror::PropertyAccumulator*) ./../../v8/src/inspector/value-mirror.cc:1520:15

## Attachments

- [crash.html](attachments/crash.html) (text/html, 1.2 KB)
- [asan.log](attachments/asan.log) (text/plain, 42.3 KB)
- asan.log (text/plain, 44.7 KB)

## Timeline

### aj...@google.com (2024-02-05)

Thanks this indeed repros after a few refreshes.

### aj...@google.com (2024-02-05)

Severity S2/Medium as this UAF requires devtools to be open. Please investigate or assign to someone who can make progress on this issue.

### sz...@chromium.org (2024-02-06)

I'll take a look later.

### pe...@google.com (2024-02-06)

Setting milestone because of s2 severity.

### pe...@google.com (2024-02-06)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ap...@google.com (2024-02-07)

Project: v8/v8
Branch: main

commit 41dd803aaaba04c36403c28225a36bd61ee26572
Author: Simon Zünd <szuend@chromium.org>
Date:   Tue Feb 06 13:02:17 2024

    [inspector] Don't interrupt while building console messages
    
    This CL fixes a use-after-free of the InspectorSession. This can
    happen for workers since they are killed (and the DevToolsSession
    detached) during an interrupt.
    
    The problem is that we might have already entered the inspector and
    the inspector entered JavaScript land. This could mean that we detach
    a session on which we are currently operating on (e.g. building a
    console message to send it to the frontend).
    
    The fix is to postpone interrupts until after we are done building
    console messages so we don't lose the DevTools session half-way
    through it.
    
    R=dsv@chromium.org
    
    Fixed: b:323813642
    Change-Id: I495d926830bc0ed129b0632d454b2d94f3123180
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5272444
    Commit-Queue: Simon Zünd <szuend@chromium.org>
    Reviewed-by: Eric Leese <leese@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#92226}

M       src/inspector/v8-console-message.cc
M       test/unittests/inspector/inspector-unittest.cc

https://chromium-review.googlesource.com/5272444


### pe...@google.com (2024-02-07)

This is sufficiently serious that it should be merged to beta. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M122. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### sz...@chromium.org (2024-02-08)

1. https://crrev.com/c/5272444
2. No
3. No
4. No
5. No

### pe...@google.com (2024-02-08)

Merge review required: M122 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), ceb (ChromeOS), pbommana (Desktop)

### sz...@chromium.org (2024-02-08)

1. P1/S2 use-after-free security bug
2. https://crrev.com/c/5272444
3. Yes (123.0.6288.0)
4. No


### am...@chromium.org (2024-02-10)

<https://crrev.com/c/5272444> approved for merge to M122
please merge this fix to M122, branch 6261, by EOD Monday, 12 February so this fix can be included in the M122 Stable cut

### pe...@google.com (2024-02-12)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ap...@google.com (2024-02-12)

Project: v8/v8
Branch: refs/branch-heads/12.2

commit 72c073ca0d0508b840b4d2bbcca812c276484905
Author: Simon Zünd <szuend@chromium.org>
Date:   Tue Feb 06 13:02:17 2024

    Merged: [inspector] Don't interrupt while building console messages
    
    This CL fixes a use-after-free of the InspectorSession. This can
    happen for workers since they are killed (and the DevToolsSession
    detached) during an interrupt.
    
    The problem is that we might have already entered the inspector and
    the inspector entered JavaScript land. This could mean that we detach
    a session on which we are currently operating on (e.g. building a
    console message to send it to the frontend).
    
    The fix is to postpone interrupts until after we are done building
    console messages so we don't lose the DevTools session half-way
    through it.
    
    R=dsv@chromium.org
    
    (cherry picked from commit 41dd803aaaba04c36403c28225a36bd61ee26572)
    
    Fixed: b:323813642
    Change-Id: I495d926830bc0ed129b0632d454b2d94f3123180
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5280692
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Auto-Submit: Simon Zünd <szuend@chromium.org>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Commit-Queue: Simon Zünd <szuend@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.2@{#26}
    Cr-Branched-From: 6eb5a9616aa6f8c705217aeb7c7ab8c037a2f676-refs/heads/12.2.281@{#1}
    Cr-Branched-From: 44cf56d850167c6988522f8981730462abc04bcc-refs/heads/main@{#91934}

M       src/inspector/v8-console-message.cc
M       test/unittests/inspector/inspector-unittest.cc

https://chromium-review.googlesource.com/5280692


### pe...@google.com (2024-02-12)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### sz...@chromium.org (2024-02-12)

1. No
2. No

### na...@google.com (2024-02-18)

Hi szuend@chromium.org,
Could you help confirm if this fix is needed for LTS-114? If Yes, then pls add the hotlist "LTS-Merge-request-114" to the bug and respond to the questionnaire that gets populated with it. thanks

### sz...@chromium.org (2024-02-19)

No need to merge this to 114.

### na...@google.com (2024-02-21)

LTS-NotApplicable-114 based on comment#18

### am...@google.com (2024-02-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-22)

Congratulations, Cassidy Kim! The Chrome VRP Panel has decided to award you $3,000 for this report of a mildly mitigated memory corruption bug in the renderer process. Thank you for your efforts and reporting this issue to us!

### pe...@google.com (2024-03-12)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



### vo...@google.com (2024-03-12)

1. <https://crrev.com/c/5362664>
2. Low - simple conflicts
3. M122
4. Yes

### ap...@google.com (2024-03-14)

Project: v8/v8
Branch: refs/branch-heads/12.0

commit 6feeaeaefa4a0b543cc7d6bc94d69a815a955542
Author: Zakhar Voit <voit@google.com>
Date:   Tue Mar 12 08:10:08 2024

    [M120-LTS][inspector] Don't interrupt while building console messages
    
    This CL fixes a use-after-free of the InspectorSession. This can
    happen for workers since they are killed (and the DevToolsSession
    detached) during an interrupt.
    
    The problem is that we might have already entered the inspector and
    the inspector entered JavaScript land. This could mean that we detach
    a session on which we are currently operating on (e.g. building a
    console message to send it to the frontend).
    
    The fix is to postpone interrupts until after we are done building
    console messages so we don't lose the DevTools session half-way
    through it.
    
    R=dsv@chromium.org
    
    (cherry picked from commit 41dd803aaaba04c36403c28225a36bd61ee26572)
    
    (cherry picked from commit 72c073ca0d0508b840b4d2bbcca812c276484905)
    
    Fixed: b:323813642
    Change-Id: I495d926830bc0ed129b0632d454b2d94f3123180
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5280692
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Auto-Submit: Simon Zünd <szuend@chromium.org>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Commit-Queue: Simon Zünd <szuend@chromium.org>
    Cr-Original-Commit-Position: refs/branch-heads/12.2@{#26}
    Cr-Original-Branched-From: 6eb5a9616aa6f8c705217aeb7c7ab8c037a2f676-refs/heads/12.2.281@{#1}
    Cr-Original-Branched-From: 44cf56d850167c6988522f8981730462abc04bcc-refs/heads/main@{#91934}
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5362664
    Commit-Queue: Zakhar Voit <voit@google.com>
    Reviewed-by: Simon Zünd <szuend@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.0@{#40}
    Cr-Branched-From: ed7b4caf1fb8184ad9e24346c84424055d4d430a-refs/heads/12.0.267@{#1}
    Cr-Branched-From: 210e75b19db4352c9b78dce0bae11c2dc3077df4-refs/heads/main@{#90651}

M       src/inspector/v8-console-message.cc
M       test/unittests/inspector/inspector-unittest.cc

https://chromium-review.googlesource.com/5362664


### pe...@google.com (2024-05-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/323813642)*
