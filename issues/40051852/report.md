# use after free in mojom::ClipboardHost

| Field | Value |
|-------|-------|
| **Issue ID** | [40051852](https://issues.chromium.org/issues/40051852) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>DataTransfer, Internals>Core, Internals>TaskScheduling |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cd...@gmail.com |
| **Assignee** | dc...@chromium.org |
| **Created** | 2020-03-26 |
| **Bounty** | $10,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36

Steps to reproduce the problem:
Chromium 83.0.4095.0
1 python ./copy_mojo_js_bindings.py /path/to/chrome/.../out/asan/gen
2 python3.6m -m http.server 8605
3 ./chrome --enable-blink-features=MojoJS --user-data-dir=/tmp/nonexist  http://127.0.0.1:8605/poc.html

What is the expected behavior?

What went wrong?
get UAF soon.

Did this work before? N/A 

Chrome version: Chromium 83.0.4095.0  Channel: stable
OS Version: 18.04
Flash Version:

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 62.4 KB)
- [poc.zip](attachments/poc.zip) (application/octet-stream, 27.7 KB)

## Timeline

### jd...@chromium.org (2020-03-26)

dcheng@: you looked at crbug.com/839250 and I know MojoJS security issues are near/dear to your heart. Would you mind either fixing this or finding a better owner? Thanks!

[Monorail components: Blink>DataTransfer]

### jd...@chromium.org (2020-03-26)

Adding huangdarwin@, who is probably who I'd assign it to if I hadn't already sent it to dcheng@.

### dc...@chromium.org (2020-03-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-27)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-10)

dcheng: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2020-04-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5639522935701504.

### cl...@chromium.org (2020-04-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6303981169606656.

### cl...@chromium.org (2020-04-11)

Testcase 5639522935701504 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5639522935701504.

### [Deleted User] (2020-04-11)

dcheng: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dc...@chromium.org (2020-04-11)

Btw I can definitely repro this. It's related to the IPC task annotation.

Posting the ASAN output inline for the sake of completeness.

=================================================================
==143906==ERROR: AddressSanitizer: heap-use-after-free on address 0x62000009ef1c at pc 0x56338d5875b2 bp 0x7ffe32ea1a50 sp 0x7ffe32ea1a48
READ of size 4 at 0x62000009ef1c thread T0 (chrome)
    #0 0x56338d5875b1 in IsDummyPendingTask ./../../base/task/common/task_annotator.cc:37:13
    #1 0x56338d5875b1 in CurrentTaskForThread ./../../base/task/common/task_annotator.cc:52:23
    #2 0x56338d5875b1 in base::TaskAnnotator::WillQueueTask(char const*, base::PendingTask*, char const*) ./../../base/task/common/task_annotator.cc:77:29
    #3 0x56338d5cd136 in base::sequence_manager::internal::TaskQueueImpl::PostImmediateTaskImpl(base::sequence_manager::internal::PostedTask, base::sequence_manager::internal::TaskQueueImpl::CurrentThread) ./../../base/task/sequence_manager/task_queue_impl.cc:308:24
    #4 0x56338d5c978b in base::sequence_manager::internal::TaskQueueImpl::PostTask(base::sequence_manager::internal::PostedTask) ./../../base/task/sequence_manager/task_queue_impl.cc:236:5
    #5 0x56338d5c9409 in base::sequence_manager::internal::TaskQueueImpl::GuardedTaskPoster::PostTask(base::sequence_manager::internal::PostedTask) ./../../base/task/sequence_manager/task_queue_impl.cc:76:11
    #6 0x56338d5c9c02 in base::sequence_manager::internal::TaskQueueImpl::TaskRunner::PostDelayedTask(base::Location const&, base::OnceCallback<void ()>, base::TimeDelta) ./../../base/task/sequence_manager/task_queue_impl.cc:93:24
    #7 0x56338d677c3d in base::TaskRunner::PostTask(base::Location const&, base::OnceCallback<void ()>) ./../../base/task_runner.cc:45:10
    #8 0x56338dc027f4 in mojo::SimpleWatcher::ArmOrNotify() ./../../mojo/public/cpp/system/simple_watcher.cc:258:17
    #9 0x56338db4964e in mojo::Connector::ActiveDispatchTracker::NotifyBeginNesting() ./../../mojo/public/cpp/bindings/lib/connector.cc:140:34
    #10 0x56338d5173d6 in base::RunLoop::BeforeRun() ./../../base/run_loop.cc:312:16
    #11 0x56338d5161b3 in base::RunLoop::Run() ./../../base/run_loop.cc:105:8
    #12 0x5633934607bc in ui::SelectionRequestor::BlockTillSelectionNotifyForRequest(ui::SelectionRequestor::Request*) ./../../ui/base/x/selection_requestor.cc:260:14
    #13 0x56339345f3c4 in ui::SelectionRequestor::PerformBlockingConvertSelection(unsigned long, unsigned long, scoped_refptr<base::RefCountedMemory>*, unsigned long*, unsigned long*) ./../../ui/base/x/selection_requestor.cc:82:3
    #14 0x56339344ce13 in ui::ClipboardX11::X11Details::WaitAndGetTargetsList(ui::ClipboardBuffer) ./../../ui/base/clipboard/clipboard_x11.cc:396:34
    #15 0x56339344c1cc in ui::ClipboardX11::X11Details::RequestAndWaitForTypes(ui::ClipboardBuffer, std::__1::vector<unsigned long, std::__1::allocator<unsigned long> > const&) ./../../ui/base/clipboard/clipboard_x11.cc:349:26
    #16 0x56339345368c in ui::ClipboardX11::ReadRTF(ui::ClipboardBuffer, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >*) const ./../../ui/base/clipboard/clipboard_x11.cc:660:36
    #17 0x563383a15c24 in content::ClipboardHostImpl::ReadRtf(ui::ClipboardBuffer, base::OnceCallback<void (std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&)>) ./../../content/browser/frame_host/clipboard_host_impl.cc:222:15
    #18 0x56338155d585 in blink::mojom::ClipboardHostStubDispatch::AcceptWithResponder(blink::mojom::ClipboardHost*, mojo::Message*, std::__1::unique_ptr<mojo::MessageReceiverWithStatus, std::__1::default_delete<mojo::MessageReceiverWithStatus> >) ./gen/third_party/blink/public/mojom/clipboard/clipboard.mojom.cc:3037:13
    #19 0x563383a18a5c in blink::mojom::ClipboardHostStub<mojo::RawPtrImplRefTraits<blink::mojom::ClipboardHost> >::AcceptWithResponder(mojo::Message*, std::__1::unique_ptr<mojo::MessageReceiverWithStatus, std::__1::default_delete<mojo::MessageReceiverWithStatus> >) ./gen/third_party/blink/public/mojom/clipboard/clipboard.mojom.h:288:12
    #20 0x56338db60e87 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:528:56
    #21 0x56338db7b719 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:41:19
    #22 0x56338db65bf0 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:356:22
    #23 0x56338db8d1c7 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:953:42
    #24 0x56338db8af6b in mojo::internal::MultiplexRouter::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:620:38
    #25 0x56338db7b719 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:41:19
    #26 0x56338db4f1c3 in mojo::Connector::DispatchMessage(mojo::Message) ./../../mojo/public/cpp/bindings/lib/connector.cc:539:49
    #27 0x56338db524e3 in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:627:12
    #28 0x56338db5198d in mojo::Connector::OnHandleReadyInternal(unsigned int) ./../../mojo/public/cpp/bindings/lib/connector.cc:446:3
    #29 0x563381cc45b3 in Run ./../../base/callback.h:132:12
    #30 0x563381cc45b3 in mojo::SimpleWatcher::DiscardReadyState(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple_watcher.h:194:14
    #31 0x56338dc0381c in Run ./../../base/callback.h:132:12
    #32 0x56338dc0381c in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple_watcher.cc:292:14
    #33 0x56338dc04c7d in Invoke<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> ./../../base/bind_internal.h:489:12
    #34 0x56338dc04c7d in MakeItSo<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> ./../../base/bind_internal.h:643:5
    #35 0x56338dc04c7d in void base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), std::__1::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0ul, 1ul, 2ul, 3ul>(void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), std::__1::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>&&, std::__1::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>) ./../../base/bind_internal.h:696:12
    #36 0x56338d587ce3 in Run ./../../base/callback.h:98:12
    #37 0x56338d587ce3 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:142:33
    #38 0x56338d5f505f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:321:23
    #39 0x56338d5f478f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:246:36
    #40 0x56338d462e39 in HandleDispatch ./../../base/message_loop/message_pump_glib.cc:409:46
    #41 0x56338d462e39 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) ./../../base/message_loop/message_pump_glib.cc:122:43
    #42 0x7f8971fbaf1c in g_main_context_dispatch ??:0:0

0x62000009ef1c is located 3740 bytes inside of 3840-byte region [0x62000009e080,0x62000009ef80)
freed by thread T0 (chrome) here:
    #0 0x56337e7b465d in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:160:3
    #1 0x56338d5b60d0 in __do_call ./../../buildtools/third_party/libc++/trunk/include/new:334:12
    #2 0x56338d5b60d0 in __do_deallocate_handle_size ./../../buildtools/third_party/libc++/trunk/include/new:292:12
    #3 0x56338d5b60d0 in __do_deallocate_handle_size_align ./../../buildtools/third_party/libc++/trunk/include/new:262:12
    #4 0x56338d5b60d0 in __libcpp_deallocate ./../../buildtools/third_party/libc++/trunk/include/new:340:3
    #5 0x56338d5b60d0 in deallocate ./../../buildtools/third_party/libc++/trunk/include/memory:1856:10
    #6 0x56338d5b60d0 in deallocate ./../../buildtools/third_party/libc++/trunk/include/memory:1578:14
    #7 0x56338d5b60d0 in ~__split_buffer ./../../buildtools/third_party/libc++/trunk/include/__split_buffer:350:9
    #8 0x56338d5b60d0 in void std::__1::vector<base::sequence_manager::internal::SequenceManagerImpl::ExecutingTask, std::__1::allocator<base::sequence_manager::internal::SequenceManagerImpl::ExecutingTask> >::__emplace_back_slow_path<base::sequence_manager::Task, base::sequence_manager::internal::TaskQueueImpl*, base::sequence_manager::TaskQueue::TaskTiming>(base::sequence_manager::Task&&, base::sequence_manager::internal::TaskQueueImpl*&&, base::sequence_manager::TaskQueue::TaskTiming&&) ./../../buildtools/third_party/libc++/trunk/include/vector:1669:1
    #9 0x56338d59fa60 in emplace_back<base::sequence_manager::Task, base::sequence_manager::internal::TaskQueueImpl *, base::sequence_manager::TaskQueue::TaskTiming> ./../../buildtools/third_party/libc++/trunk/include/vector:1686:9
    #10 0x56338d59fa60 in base::sequence_manager::internal::SequenceManagerImpl::SelectNextTaskImpl() ./../../base/task/sequence_manager/sequence_manager_impl.cc:626:45
    #11 0x56338d59e6e0 in base::sequence_manager::internal::SequenceManagerImpl::SelectNextTask() ./../../base/task/sequence_manager/sequence_manager_impl.cc:496:16
    #12 0x56338d5f4eef in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:301:50
    #13 0x56338d5f478f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:246:36
    #14 0x56338d461770 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_glib.cc:443:48
    #15 0x56338d5f6b5f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:422:12
    #16 0x56338d516949 in base::RunLoop::Run() ./../../base/run_loop.cc:124:14
    #17 0x5633934607bc in ui::SelectionRequestor::BlockTillSelectionNotifyForRequest(ui::SelectionRequestor::Request*) ./../../ui/base/x/selection_requestor.cc:260:14
    #18 0x56339345f3c4 in ui::SelectionRequestor::PerformBlockingConvertSelection(unsigned long, unsigned long, scoped_refptr<base::RefCountedMemory>*, unsigned long*, unsigned long*) ./../../ui/base/x/selection_requestor.cc:82:3
    #19 0x56339344c9dc in ui::ClipboardX11::X11Details::WaitAndGetTargetsList(ui::ClipboardBuffer) ./../../ui/base/clipboard/clipboard_x11.cc:376:30
    #20 0x56339344c1cc in ui::ClipboardX11::X11Details::RequestAndWaitForTypes(ui::ClipboardBuffer, std::__1::vector<unsigned long, std::__1::allocator<unsigned long> > const&) ./../../ui/base/clipboard/clipboard_x11.cc:349:26
    #21 0x56339345368c in ui::ClipboardX11::ReadRTF(ui::ClipboardBuffer, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >*) const ./../../ui/base/clipboard/clipboard_x11.cc:660:36
    #22 0x563383a15c24 in content::ClipboardHostImpl::ReadRtf(ui::ClipboardBuffer, base::OnceCallback<void (std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&)>) ./../../content/browser/frame_host/clipboard_host_impl.cc:222:15
    #23 0x56338155d585 in blink::mojom::ClipboardHostStubDispatch::AcceptWithResponder(blink::mojom::ClipboardHost*, mojo::Message*, std::__1::unique_ptr<mojo::MessageReceiverWithStatus, std::__1::default_delete<mojo::MessageReceiverWithStatus> >) ./gen/third_party/blink/public/mojom/clipboard/clipboard.mojom.cc:3037:13
    #24 0x563383a18a5c in blink::mojom::ClipboardHostStub<mojo::RawPtrImplRefTraits<blink::mojom::ClipboardHost> >::AcceptWithResponder(mojo::Message*, std::__1::unique_ptr<mojo::MessageReceiverWithStatus, std::__1::default_delete<mojo::MessageReceiverWithStatus> >) ./gen/third_party/blink/public/mojom/clipboard/clipboard.mojom.h:288:12
    #25 0x56338db60e87 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:528:56
    #26 0x56338db7b719 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:41:19
    #27 0x56338db65bf0 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:356:22
    #28 0x56338db8d1c7 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:953:42
    #29 0x56338db8af6b in mojo::internal::MultiplexRouter::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:620:38
    #30 0x56338db7b719 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:41:19
    #31 0x56338db4f1c3 in mojo::Connector::DispatchMessage(mojo::Message) ./../../mojo/public/cpp/bindings/lib/connector.cc:539:49
    #32 0x56338db524e3 in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:627:12
    #33 0x56338db5198d in mojo::Connector::OnHandleReadyInternal(unsigned int) ./../../mojo/public/cpp/bindings/lib/connector.cc:446:3
    #34 0x563381cc45b3 in Run ./../../base/callback.h:132:12
    #35 0x563381cc45b3 in mojo::SimpleWatcher::DiscardReadyState(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple_watcher.h:194:14
    #36 0x56338dc0381c in Run ./../../base/callback.h:132:12
    #37 0x56338dc0381c in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple_watcher.cc:292:14
    #38 0x56338dc04c7d in Invoke<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> ./../../base/bind_internal.h:489:12
    #39 0x56338dc04c7d in MakeItSo<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> ./../../base/bind_internal.h:643:5
    #40 0x56338dc04c7d in void base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), std::__1::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0ul, 1ul, 2ul, 3ul>(void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), std::__1::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>&&, std::__1::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>) ./../../base/bind_internal.h:696:12
    #41 0x56338d587ce3 in Run ./../../base/callback.h:98:12
    #42 0x56338d587ce3 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:142:33

previously allocated by thread T0 (chrome) here:
    #0 0x56337e7b3dfd in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:99:3
    #1 0x56338d5b5e4a in __libcpp_allocate ./../../buildtools/third_party/libc++/trunk/include/new:253:10
    #2 0x56338d5b5e4a in allocate ./../../buildtools/third_party/libc++/trunk/include/memory:1853:37
    #3 0x56338d5b5e4a in allocate ./../../buildtools/third_party/libc++/trunk/include/memory:1570:21
    #4 0x56338d5b5e4a in __split_buffer ./../../buildtools/third_party/libc++/trunk/include/__split_buffer:318:29
    #5 0x56338d5b5e4a in void std::__1::vector<base::sequence_manager::internal::SequenceManagerImpl::ExecutingTask, std::__1::allocator<base::sequence_manager::internal::SequenceManagerImpl::ExecutingTask> >::__emplace_back_slow_path<base::sequence_manager::Task, base::sequence_manager::internal::TaskQueueImpl*, base::sequence_manager::TaskQueue::TaskTiming>(base::sequence_manager::Task&&, base::sequence_manager::internal::TaskQueueImpl*&&, base::sequence_manager::TaskQueue::TaskTiming&&) ./../../buildtools/third_party/libc++/trunk/include/vector:1664:49
    #6 0x56338d59fa60 in emplace_back<base::sequence_manager::Task, base::sequence_manager::internal::TaskQueueImpl *, base::sequence_manager::TaskQueue::TaskTiming> ./../../buildtools/third_party/libc++/trunk/include/vector:1686:9
    #7 0x56338d59fa60 in base::sequence_manager::internal::SequenceManagerImpl::SelectNextTaskImpl() ./../../base/task/sequence_manager/sequence_manager_impl.cc:626:45
    #8 0x56338d59e6e0 in base::sequence_manager::internal::SequenceManagerImpl::SelectNextTask() ./../../base/task/sequence_manager/sequence_manager_impl.cc:496:16
    #9 0x56338d5f4eef in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:301:50
    #10 0x56338d5f478f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:246:36
    #11 0x56338d461770 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_glib.cc:443:48
    #12 0x56338d5f6b5f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:422:12
    #13 0x56338d516949 in base::RunLoop::Run() ./../../base/run_loop.cc:124:14
    #14 0x5633934607bc in ui::SelectionRequestor::BlockTillSelectionNotifyForRequest(ui::SelectionRequestor::Request*) ./../../ui/base/x/selection_requestor.cc:260:14
    #15 0x56339345f3c4 in ui::SelectionRequestor::PerformBlockingConvertSelection(unsigned long, unsigned long, scoped_refptr<base::RefCountedMemory>*, unsigned long*, unsigned long*) ./../../ui/base/x/selection_requestor.cc:82:3
    #16 0x56339344c9dc in ui::ClipboardX11::X11Details::WaitAndGetTargetsList(ui::ClipboardBuffer) ./../../ui/base/clipboard/clipboard_x11.cc:376:30
    #17 0x56339344c1cc in ui::ClipboardX11::X11Details::RequestAndWaitForTypes(ui::ClipboardBuffer, std::__1::vector<unsigned long, std::__1::allocator<unsigned long> > const&) ./../../ui/base/clipboard/clipboard_x11.cc:349:26
    #18 0x56339345368c in ui::ClipboardX11::ReadRTF(ui::ClipboardBuffer, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >*) const ./../../ui/base/clipboard/clipboard_x11.cc:660:36
    #19 0x563383a15c24 in content::ClipboardHostImpl::ReadRtf(ui::ClipboardBuffer, base::OnceCallback<void (std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&)>) ./../../content/browser/frame_host/clipboard_host_impl.cc:222:15
    #20 0x56338155d585 in blink::mojom::ClipboardHostStubDispatch::AcceptWithResponder(blink::mojom::ClipboardHost*, mojo::Message*, std::__1::unique_ptr<mojo::MessageReceiverWithStatus, std::__1::default_delete<mojo::MessageReceiverWithStatus> >) ./gen/third_party/blink/public/mojom/clipboard/clipboard.mojom.cc:3037:13
    #21 0x563383a18a5c in blink::mojom::ClipboardHostStub<mojo::RawPtrImplRefTraits<blink::mojom::ClipboardHost> >::AcceptWithResponder(mojo::Message*, std::__1::unique_ptr<mojo::MessageReceiverWithStatus, std::__1::default_delete<mojo::MessageReceiverWithStatus> >) ./gen/third_party/blink/public/mojom/clipboard/clipboard.mojom.h:288:12
    #22 0x56338db60e87 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:528:56
    #23 0x56338db7b719 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:41:19
    #24 0x56338db65bf0 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:356:22
    #25 0x56338db8d1c7 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:953:42
    #26 0x56338db8af6b in mojo::internal::MultiplexRouter::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:620:38
    #27 0x56338db7b719 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:41:19
    #28 0x56338db4f1c3 in mojo::Connector::DispatchMessage(mojo::Message) ./../../mojo/public/cpp/bindings/lib/connector.cc:539:49
    #29 0x56338db524e3 in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:627:12
    #30 0x56338db5198d in mojo::Connector::OnHandleReadyInternal(unsigned int) ./../../mojo/public/cpp/bindings/lib/connector.cc:446:3
    #31 0x563381cc45b3 in Run ./../../base/callback.h:132:12
    #32 0x563381cc45b3 in mojo::SimpleWatcher::DiscardReadyState(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple_watcher.h:194:14
    #33 0x56338dc0381c in Run ./../../base/callback.h:132:12
    #34 0x56338dc0381c in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple_watcher.cc:292:14
    #35 0x56338dc04c7d in Invoke<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> ./../../base/bind_internal.h:489:12
    #36 0x56338dc04c7d in MakeItSo<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> ./../../base/bind_internal.h:643:5
    #37 0x56338dc04c7d in void base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), std::__1::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0ul, 1ul, 2ul, 3ul>(void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), std::__1::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>&&, std::__1::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>) ./../../base/bind_internal.h:696:12
    #38 0x56338d587ce3 in Run ./../../base/callback.h:98:12
    #39 0x56338d587ce3 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:142:33

SUMMARY: AddressSanitizer: heap-use-after-free (/usr/local/google/home/dcheng/src/chrome/src/out/asan/chrome+0x206145b1)
Shadow bytes around the buggy address:
  0x0c408000bd90: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c408000bda0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c408000bdb0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c408000bdc0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c408000bdd0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x0c408000bde0: fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c408000bdf0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c408000be00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c408000be10: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c408000be20: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c408000be30: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
  Shadow gap:              cc
Cannot upload crash dump: failed to open
==143906==ABORTING

[Monorail components: Internals>TaskScheduling]

### dc...@chromium.org (2020-04-11)

A lot of the task annotation code has changed, but the fundamental reason is that vector does not guarantee pointer / iterator stability.

https://source.chromium.org/chromium/chromium/src/+/master:base/task/sequence_manager/sequence_manager_impl.h;l=305;drc=8acb3248d5f60094a2007a6360250a4013f64bfe?originalUrl=https:%2F%2Fcs.chromium.org%2F stores the stack of currently executing tasks as a std::vector:

  std::vector<ExecutingTask> task_execution_stack;

Later on, when we check IsDummyPendingTask(), we have a pointer to a PendingTask stored in TLS:

https://source.chromium.org/chromium/chromium/src/+/master:base/task/common/task_annotator.cc;l=29;drc=8acb3248d5f60094a2007a6360250a4013f64bfe?originalUrl=https:%2F%2Fcs.chromium.org%2F

  ThreadLocalPointer<PendingTask>* GetTLSForCurrentPendingTask() {
    static NoDestructor<ThreadLocalPointer<PendingTask>> instance;
    return instance.get();
  }

Each ExecutionTask holds a PendingTask internally, and a pointer to the PendingTask is set in TLS when we call TaskAnnotator::RunTask() (I think).

When we push enough tasks onto the stack, we resize the buffer and invalidate the PendingTask pointer held in |instance|, but |instance| isn't updated and it's now a dangling pointer.

### dc...@chromium.org (2020-04-11)

There are several possibilities here:

1. Clipboard code could try harder not to execute any application tasks. I'm not sure how feasible this is though: fundamentally, we need to wait for messages from X to service the selection request, and it's conceivable that some of the other X events could call back into Chrome application code.

2. We could implement some variant of the previous suggestions to selectively disable Mojo's sync IPC deadlock prevention, which is what I believe causes additional sync IPCs to be handled while we're in the nested run loop while waiting for the selection request.

3. Fundamentally, task annotator cannot assume pointer stability of std::vector. I've put up a simple patch to fix this, but I'm not 100% sure of the performance implications.

### dc...@chromium.org (2020-04-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-04-13)

ClusterFuzz testcase 6303981169606656 appears to be flaky, updating reproducibility label.

### cl...@chromium.org (2020-04-13)

Detailed Report: https://clusterfuzz.com/testcase?key=6303981169606656

Fuzzer: 
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: CHECK failure
Crash Address: 
Crash State:
  r. Sending zygote magic failed in zygote_linux.cc
  service_manager::Zygote::ProcessRequests
  service_manager::ZygoteMain
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=758353

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6303981169606656

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/6303981169606656 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

### cl...@chromium.org (2020-04-13)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Core Internals>Sandbox]

### dc...@chromium.org (2020-04-13)

I'm not sure what clusterfuzz is finding, but I don't think it's right with the sandbox attribution here.

(Is there a label for when the Clusterfuzz  repro itself is wrong?)

[Monorail components: -Internals>Sandbox]

### cl...@chromium.org (2020-04-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5631729214226432.

### cl...@chromium.org (2020-04-13)

Testcase 5631729214226432 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5631729214226432.

### cl...@chromium.org (2020-04-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5723860826128384.

### cl...@chromium.org (2020-04-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5655458304557056.

### cl...@chromium.org (2020-04-13)

Testcase 5723860826128384 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5723860826128384.

### cl...@chromium.org (2020-04-14)

Testcase 5655458304557056 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5655458304557056.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c34431a597aba8f4374975217d97a73eaf7d1f18

commit c34431a597aba8f4374975217d97a73eaf7d1f18
Author: Daniel Cheng <dcheng@chromium.org>
Date: Tue Apr 14 21:20:16 2020

Use std::deque to store the stack of currently executing tasks

The stack of currently executing stacks includes a PendingTask field. A
pointer to this field is stored in TLS. However, std::vector does not
guarantee pointer stability on resize.

Bug: 1064891
Change-Id: I04eb06c9521722f08fd72826f552cedaffe61b53
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2146349
Commit-Queue: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Sami Kyöstilä <skyostil@chromium.org>
Reviewed-by: François Doray <fdoray@chromium.org>
Cr-Commit-Position: refs/heads/master@{#759017}

[modify] https://crrev.com/c34431a597aba8f4374975217d97a73eaf7d1f18/base/task/sequence_manager/sequence_manager_impl.cc
[modify] https://crrev.com/c34431a597aba8f4374975217d97a73eaf7d1f18/base/task/sequence_manager/sequence_manager_impl.h


### dc...@chromium.org (2020-04-14)

I don't know how to make the Clusterfuzz repro work unfortunately, but this should be fixed.

### [Deleted User] (2020-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-15)

Requesting merge to stable M81 because latest trunk commit (759017) appears to be after stable branch point (737173).

Requesting merge to beta M81 because latest trunk commit (759017) appears to be after beta branch point (737173).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-04-15)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-04-15)

dcheng@ I'd like to follow Sheriffbot's recommendations and merge this back to M81 and M83. The fix seems extremely low-risk. My only concern would be if we think there are any pathological cases where we could use a lot more memory by using the deque, but that seems very unlikely given the nature of SequenceManager. But please can you comment on that as well as the questions in https://crbug.com/chromium/1064891#c29?

### dc...@chromium.org (2020-04-15)

Yes, I think it should be safe to merge. The memory increase per-process should be a small constant factor, based on how libc++ implements deque.

1. This is a security bug, and security believes it should be merged: it's a use-after-free in the browser, and the fix is simple.
2. https://chromium-review.googlesource.com/c/chromium/src/+/2146349
3. Yes. That being said, I'd like to wait a few more days and see if there are any interesting performance regressions reported.
4. Because the issue wasn't found earlier :)
5. No.
6. n/a

### pb...@google.com (2020-04-16)

+Adetaylor(Security TPM)

### ad...@chromium.org (2020-04-17)

Yep. Setting a next action date for next Wednesday to consider merging.

### [Deleted User] (2020-04-17)

This bug requires manual review: To minimize risk and increase branch stability, all merge requests are being reviewed manually by the release team.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dc...@chromium.org (2020-04-17)

(copied and pasted from https://crbug.com/chromium/1064891#c31, for the M83 merge questions)

1. This is a security bug, and security believes it should be merged: it's a use-after-free in the browser, and the fix is simple.
2. https://chromium-review.googlesource.com/c/chromium/src/+/2146349
3. Yes. That being said, I'd like to wait a few more days and see if there are any interesting performance regressions reported.
4. Because the issue wasn't found earlier :)
5. No.
6. n/a

### ad...@google.com (2020-04-20)

dcheng@ - I know I said we'd wait until Wednesday, but it turns out that it's not too late to get this into tomorrow's M81 stable refresh. The branch will be cut around 12pm PST today. Do you feel there's enough information from Canary over the weekend to make that judgement?

Obviously we only want to merge to M81 if we're sure this is 100% safe and has no risk whatsoever of performance or stability regressions.

I am approving merge to M83 (branch 4103) and M81 (branch 4044) now, but please only merge if you're totally confident. Otherwise we can discuss again later in the week.

### na...@google.com (2020-04-20)

[Empty comment from Monorail migration]

### sr...@google.com (2020-04-21)

dcheng@ please merge these to M83 before 2pm PST today so that we can include in tomorrow's beta release, if you feel this needs more bake time, then we can wait for merge to M83.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/67864c2147709e07a2a7a1c8be8c2086e014e3f0

commit 67864c2147709e07a2a7a1c8be8c2086e014e3f0
Author: Daniel Cheng <dcheng@chromium.org>
Date: Tue Apr 21 19:35:10 2020

Use std::deque to store the stack of currently executing tasks

The stack of currently executing stacks includes a PendingTask field. A
pointer to this field is stored in TLS. However, std::vector does not
guarantee pointer stability on resize.

(cherry picked from commit c34431a597aba8f4374975217d97a73eaf7d1f18)

Bug: 1064891
Change-Id: I04eb06c9521722f08fd72826f552cedaffe61b53
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2146349
Commit-Queue: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Sami Kyöstilä <skyostil@chromium.org>
Reviewed-by: François Doray <fdoray@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#759017}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2158048
Cr-Commit-Position: refs/branch-heads/4044@{#970}
Cr-Branched-From: a6d9daf149a473ceea37f629c41d4527bf2055bd-refs/heads/master@{#737173}

[modify] https://crrev.com/67864c2147709e07a2a7a1c8be8c2086e014e3f0/base/task/sequence_manager/sequence_manager_impl.cc
[modify] https://crrev.com/67864c2147709e07a2a7a1c8be8c2086e014e3f0/base/task/sequence_manager/sequence_manager_impl.h


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ed014dd6ca85ebf34acfc04844bc12737d194cba

commit ed014dd6ca85ebf34acfc04844bc12737d194cba
Author: Daniel Cheng <dcheng@chromium.org>
Date: Wed Apr 22 09:54:01 2020

Use std::deque to store the stack of currently executing tasks

The stack of currently executing stacks includes a PendingTask field. A
pointer to this field is stored in TLS. However, std::vector does not
guarantee pointer stability on resize.

(cherry picked from commit c34431a597aba8f4374975217d97a73eaf7d1f18)

Bug: 1064891
Change-Id: I04eb06c9521722f08fd72826f552cedaffe61b53
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2146349
Commit-Queue: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Sami Kyöstilä <skyostil@chromium.org>
Reviewed-by: François Doray <fdoray@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#759017}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2158012
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Cr-Commit-Position: refs/branch-heads/4103@{#273}
Cr-Branched-From: 8ad47e8d21f6866e4a37f47d83a860d41debf514-refs/heads/master@{#756066}

[modify] https://crrev.com/ed014dd6ca85ebf34acfc04844bc12737d194cba/base/task/sequence_manager/sequence_manager_impl.cc
[modify] https://crrev.com/ed014dd6ca85ebf34acfc04844bc12737d194cba/base/task/sequence_manager/sequence_manager_impl.h


### na...@google.com (2020-04-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-04-23)

Congrats the Panel decided to award $10,000 for this report!

### na...@google.com (2020-04-23)

[Empty comment from Monorail migration]

### ad...@google.com (2020-04-26)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-04-27)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-05-21)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-06-30)

dcheng@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### [Deleted User] (2020-07-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1064891?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>DataTransfer, Internals>Core, Internals>TaskScheduling]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051852)*
