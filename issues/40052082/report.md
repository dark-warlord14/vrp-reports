# use-after-free in BlobRegistryImpl(browser process)

| Field | Value |
|-------|-------|
| **Issue ID** | [40052082](https://issues.chromium.org/issues/40052082) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Storage |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cd...@gmail.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2020-04-21 |
| **Bounty** | $20,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36

Steps to reproduce the problem:
Steps to reproduce the problem:
Chromium 84.0.4110.0
1 python ./copy_mojo_js_bindings.py /path/to/chrome/.../out/asan/gen
2 python3.6m -m http.server 8605
3 ./chrome --enable-blink-features=MojoJS --user-data-dir=/tmp/nonexist  http://127.0.0.1:8605/poc.html

What is the expected behavior?

What went wrong?
This uaf affects from the latest official version to the latest master brach.
If necessary, I will add a detailed analysis later.
==14941==ERROR: AddressSanitizer: heap-use-after-free on address 0x60e0002cdcf0 at pc 0x55b20a589a3e bp 0x7fdf6903f5d0 sp 0x7fdf6903f5c8
READ of size 8 at 0x60e0002cdcf0 thread T4 (Chrome_IOThread)
    #0 0x55b20a589a3d in scoped_refptr base/memory/scoped_refptr.h:207:54
    #1 0x55b20a589a3d in CallbackBase base/callback_internal.h:172:15
    #2 0x55b20a589a3d in OnceCallback base/callback.h:72:3
    #3 0x55b20a589a3d in Run base/callback.h:95:23
    #4 0x55b20a589a3d in storage::BlobRegistryImpl::BlobUnderConstruction::TransportComplete(storage::BlobStatus) storage/browser/blob/blob_registry_impl.cc:460:10
    #5 0x55b20a5b54a5 in Run base/callback.h:98:12
    #6 0x55b20a5b54a5 in storage::(anonymous namespace)::ReplyTransportStrategy::OnReply(storage::BlobDataBuilder::FutureData, unsigned long, std::__1::vector<unsigned char, std::__1::allocator<unsigned char> > const&) storage/browser/blob/blob_transport_strategy.cc:83:12
    #7 0x55b20a5b598c in Invoke<void (storage::(anonymous namespace)::ReplyTransportStrategy::*)(storage::BlobDataBuilder::FutureData, unsigned long, const std::__1::vector<unsigned char, std::__1::allocator<unsigned char>> &), storage::(anonymous namespace)::ReplyTransportStrategy *, storage::BlobDataBuilder::FutureData, unsigned long, const std::__1::vector<unsigned char, std::__1::allocator<unsigned char>> &> base/bind_internal.h:489:12
    #8 0x55b20a5b598c in MakeItSo<void (storage::(anonymous namespace)::ReplyTransportStrategy::*)(storage::BlobDataBuilder::FutureData, unsigned long, const std::__1::vector<unsigned char, std::__1::allocator<unsigned char>> &), storage::(anonymous namespace)::ReplyTransportStrategy *, storage::BlobDataBuilder::FutureData, unsigned long, const std::__1::vector<unsigned char, std::__1::allocator<unsigned char>> &> base/bind_internal.h:623:12
    #9 0x55b20a5b598c in RunImpl<void (storage::(anonymous namespace)::ReplyTransportStrategy::*)(storage::BlobDataBuilder::FutureData, unsigned long, const std::__1::vector<unsigned char, std::__1::allocator<unsigned char>> &), std::__1::tuple<base::internal::UnretainedWrapper<storage::(anonymous namespace)::ReplyTransportStrategy>, storage::BlobDataBuilder::FutureData, unsigned long>, 0, 1, 2> base/bind_internal.h:696:12
    #10 0x55b20a5b598c in base::internal::Invoker<base::internal::BindState<void (storage::(anonymous namespace)::ReplyTransportStrategy::*)(storage::BlobDataBuilder::FutureData, unsigned long, std::__1::vector<unsigned char, std::__1::allocator<unsigned char> > const&), base::internal::UnretainedWrapper<storage::(anonymous namespace)::ReplyTransportStrategy>, storage::BlobDataBuilder::FutureData, unsigned long>, void (std::__1::vector<unsigned char, std::__1::allocator<unsigned char> > const&)>::RunOnce(base::internal::BindStateBase*, std::__1::vector<unsigned char, std::__1::allocator<unsigned char> > const&) base/bind_internal.h:665:12
    #11 0x55b1fb1b885d in Run base/callback.h:98:12
    #12 0x55b1fb1b885d in blink::mojom::BytesProvider_RequestAsReply_ForwardToCallback::Accept(mojo::Message*) gen/third_party/blink/public/mojom/blob/data_element.mojom.cc:443:26
    #13 0x55b204007135 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:549:23
    #14 0x55b204013952 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:41:19
    #15 0x55b20401f50e in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:953:42
    #16 0x55b20401dc57 in mojo::internal::MultiplexRouter::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/multiplex_router.cc:620:38
    #17 0x55b204013952 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:41:19
    #18 0x55b203ffc8d0 in mojo::Connector::DispatchMessage(mojo::Message) mojo/public/cpp/bindings/lib/connector.cc:539:49
    #19 0x55b203ffea92 in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:627:12
    #20 0x55b20406a03d in Run base/callback.h:132:12
    #21 0x55b20406a03d in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple_watcher.cc:292:14
    #22 0x55b20406aad7 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) mojo/public/cpp/system/simple_watcher.cc:118:22
    #23 0x55b20406835c in mojo::SimpleWatcher::Context::CallNotify(MojoTrapEvent const*) mojo/public/cpp/system/simple_watcher.cc:57:14
    #24 0x55b1fbd2295f in mojo::core::WatcherDispatcher::InvokeWatchCallback(unsigned long, unsigned int, mojo::core::HandleSignalsState const&, unsigned int) mojo/core/watcher_dispatcher.cc:94:3
    #25 0x55b1fbd2193e in mojo::core::Watch::InvokeCallback(unsigned int, mojo::core::HandleSignalsState const&, unsigned int) mojo/core/watch.cc:78:13
    #26 0x55b1fbd15b94 in mojo::core::RequestContext::~RequestContext() mojo/core/request_context.cc:72:20
    #27 0x55b1fbcf2459 in mojo::core::NodeChannel::OnChannelMessage(void const*, unsigned long, std::__1::vector<mojo::PlatformHandle, std::__1::allocator<mojo::PlatformHandle> >) mojo/core/node_channel.cc:739:1
    #28 0x55b1fbcbf803 in mojo::core::Channel::TryDispatchMessage(base::span<char const, 18446744073709551615ul>, unsigned long*) mojo/core/channel.cc:713:16
    #29 0x55b1fbcbeed2 in mojo::core::Channel::OnReadComplete(unsigned long, unsigned long*) mojo/core/channel.cc:611:9
    #30 0x55b1fbd3311f in mojo::core::(anonymous namespace)::ChannelPosix::OnFileCanReadWithoutBlocking(int) mojo/core/channel_posix.cc:294:14
    #31 0x55b203ce930e in base::MessagePumpLibevent::OnLibeventNotification(int, short, void*) base/message_loop/message_pump_libevent.cc
    #32 0x55b203f43e19 in event_process_active base/third_party/libevent/event.c:381:4
    #33 0x55b203f43e19 in event_base_loop base/third_party/libevent/event.c:521:4
    #34 0x55b203ce9e69 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_libevent.cc:257:5
    #35 0x55b203b8d799 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:429:12
    #36 0x55b203b01936 in base::RunLoop::Run() base/run_loop.cc:124:14
    #37 0x55b1fc8d0285 in content::BrowserProcessSubThread::IOThreadRun(base::RunLoop*) content/browser/browser_process_sub_thread.cc:144:11
    #38 0x55b203be1db7 in base::Thread::ThreadMain() base/threading/thread.cc:380:3
    #39 0x55b203cc3cbd in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:81:13
    #40 0x7fdf826e86da in start_thread (/lib/x86_64-linux-gnu/libpthread.so.0+0x76da)

0x60e0002cdcf0 is located 80 bytes inside of 152-byte region [0x60e0002cdca0,0x60e0002cdd38)
freed by thread T4 (Chrome_IOThread) here:
    #0 0x55b1f91a564d in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:160:3
    #1 0x55b20a5917be in operator() buildtools/third_party/libc++/trunk/include/memory:2378:5
    #2 0x55b20a5917be in reset buildtools/third_party/libc++/trunk/include/memory:2633:7
    #3 0x55b20a5917be in ~unique_ptr buildtools/third_party/libc++/trunk/include/memory:2587:19
    #4 0x55b20a5917be in ~pair buildtools/third_party/libc++/trunk/include/utility:297:29
    #5 0x55b20a5917be in __destroy<std::__1::pair<const std::__1::basic_string<char>, std::__1::unique_ptr<storage::BlobRegistryImpl::BlobUnderConstruction, std::__1::default_delete<storage::BlobRegistryImpl::BlobUnderConstruction>>>> buildtools/third_party/libc++/trunk/include/memory:1787:23
    #6 0x55b20a5917be in destroy<std::__1::pair<const std::__1::basic_string<char>, std::__1::unique_ptr<storage::BlobRegistryImpl::BlobUnderConstruction, std::__1::default_delete<storage::BlobRegistryImpl::BlobUnderConstruction>>>> buildtools/third_party/libc++/trunk/include/memory:1619:14
    #7 0x55b20a5917be in std::__1::__tree<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::unique_ptr<storage::BlobRegistryImpl::BlobUnderConstruction, std::__1::default_delete<storage::BlobRegistryImpl::BlobUnderConstruction> > >, std::__1::__map_value_compare<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::unique_ptr<storage::BlobRegistryImpl::BlobUnderConstruction, std::__1::default_delete<storage::BlobRegistryImpl::BlobUnderConstruction> > >, std::__1::less<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > >, true>, std::__1::allocator<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::unique_ptr<storage::BlobRegistryImpl::BlobUnderConstruction, std::__1::default_delete<storage::BlobRegistryImpl::BlobUnderConstruction> > > > >::erase(std::__1::__tree_const_iterator<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::unique_ptr<storage::BlobRegistryImpl::BlobUnderConstruction, std::__1::default_delete<storage::BlobRegistryImpl::BlobUnderConstruction> > >, std::__1::__tree_node<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::unique_ptr<storage::BlobRegistryImpl::BlobUnderConstruction, std::__1::default_delete<storage::BlobRegistryImpl::BlobUnderConstruction> > >, void*>*, long>) buildtools/third_party/libc++/trunk/include/__tree:2519:5
    #8 0x55b20a55a6e6 in Run base/callback.h:98:12
    #9 0x55b20a55a6e6 in storage::BlobEntry::BuildingState::CancelRequestsAndAbort() storage/browser/blob/blob_entry.cc:48:39
    #10 0x55b20a5a34ea in ClearAndFreeMemory storage/browser/blob/blob_storage_context.cc:679:29
    #11 0x55b20a5a34ea in storage::BlobStorageContext::CancelBuildingBlobInternal(storage::BlobEntry*, storage::BlobStatus) storage/browser/blob/blob_storage_context.cc:523:3
    #12 0x55b20a589781 in storage::BlobRegistryImpl::BlobUnderConstruction::TransportComplete(storage::BlobStatus) storage/browser/blob/blob_registry_impl.cc:453:18
    #13 0x55b20a5b54a5 in Run base/callback.h:98:12
    #14 0x55b20a5b54a5 in storage::(anonymous namespace)::ReplyTransportStrategy::OnReply(storage::BlobDataBuilder::FutureData, unsigned long, std::__1::vector<unsigned char, std::__1::allocator<unsigned char> > const&) storage/browser/blob/blob_transport_strategy.cc:83:12
    #15 0x55b20a5b598c in Invoke<void (storage::(anonymous namespace)::ReplyTransportStrategy::*)(storage::BlobDataBuilder::FutureData, unsigned long, const std::__1::vector<unsigned char, std::__1::allocator<unsigned char>> &), storage::(anonymous namespace)::ReplyTransportStrategy *, storage::BlobDataBuilder::FutureData, unsigned long, const std::__1::vector<unsigned char, std::__1::allocator<unsigned char>> &> base/bind_internal.h:489:12
    #16 0x55b20a5b598c in MakeItSo<void (storage::(anonymous namespace)::ReplyTransportStrategy::*)(storage::BlobDataBuilder::FutureData, unsigned long, const std::__1::vector<unsigned char, std::__1::allocator<unsigned char>> &), storage::(anonymous namespace)::ReplyTransportStrategy *, storage::BlobDataBuilder::FutureData, unsigned long, const std::__1::vector<unsigned char, std::__1::allocator<unsigned char>> &> base/bind_internal.h:623:12
    #17 0x55b20a5b598c in RunImpl<void (storage::(anonymous namespace)::ReplyTransportStrategy::*)(storage::BlobDataBuilder::FutureData, unsigned long, const std::__1::vector<unsigned char, std::__1::allocator<unsigned char>> &), std::__1::tuple<base::internal::UnretainedWrapper<storage::(anonymous namespace)::ReplyTransportStrategy>, storage::BlobDataBuilder::FutureData, unsigned long>, 0, 1, 2> base/bind_internal.h:696:12
    #18 0x55b20a5b598c in base::internal::Invoker<base::internal::BindState<void (storage::(anonymous namespace)::ReplyTransportStrategy::*)(storage::BlobDataBuilder::FutureData, unsigned long, std::__1::vector<unsigned char, std::__1::allocator<unsigned char> > const&), base::internal::UnretainedWrapper<storage::(anonymous namespace)::ReplyTransportStrategy>, storage::BlobDataBuilder::FutureData, unsigned long>, void (std::__1::vector<unsigned char, std::__1::allocator<unsigned char> > const&)>::RunOnce(base::internal::BindStateBase*, std::__1::vector<unsigned char, std::__1::allocator<unsigned char> > const&) base/bind_internal.h:665:12
    #19 0x55b1fb1b885d in Run base/callback.h:98:12
    #20 0x55b1fb1b885d in blink::mojom::BytesProvider_RequestAsReply_ForwardToCallback::Accept(mojo::Message*) gen/third_party/blink/public/mojom/blob/data_element.mojom.cc:443:26
    #21 0x55b204007135 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:549:23
    #22 0x55b204013952 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:41:19
    #23 0x55b20401f50e in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:953:42
    #24 0x55b20401dc57 in mojo::internal::MultiplexRouter::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/multiplex_router.cc:620:38
    #25 0x55b204013952 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:41:19
    #26 0x55b203ffc8d0 in mojo::Connector::DispatchMessage(mojo::Message) mojo/public/cpp/bindings/lib/connector.cc:539:49
    #27 0x55b203ffea92 in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:627:12
    #28 0x55b20406a03d in Run base/callback.h:132:12
    #29 0x55b20406a03d in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple_watcher.cc:292:14
    #30 0x55b20406aad7 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) mojo/public/cpp/system/simple_watcher.cc:118:22
    #31 0x55b20406835c in mojo::SimpleWatcher::Context::CallNotify(MojoTrapEvent const*) mojo/public/cpp/system/simple_watcher.cc:57:14
    #32 0x55b1fbd2295f in mojo::core::WatcherDispatcher::InvokeWatchCallback(unsigned long, unsigned int, mojo::core::HandleSignalsState const&, unsigned int) mojo/core/watcher_dispatcher.cc:94:3
    #33 0x55b1fbd2193e in mojo::core::Watch::InvokeCallback(unsigned int, mojo::core::HandleSignalsState const&, unsigned int) mojo/core/watch.cc:78:13
    #34 0x55b1fbd15b94 in mojo::core::RequestContext::~RequestContext() mojo/core/request_context.cc:72:20
    #35 0x55b1fbcf2459 in mojo::core::NodeChannel::OnChannelMessage(void const*, unsigned long, std::__1::vector<mojo::PlatformHandle, std::__1::allocator<mojo::PlatformHandle> >) mojo/core/node_channel.cc:739:1
    #36 0x55b1fbcbf803 in mojo::core::Channel::TryDispatchMessage(base::span<char const, 18446744073709551615ul>, unsigned long*) mojo/core/channel.cc:713:16
    #37 0x55b1fbcbeed2 in mojo::core::Channel::OnReadComplete(unsigned long, unsigned long*) mojo/core/channel.cc:611:9
    #38 0x55b1fbd3311f in mojo::core::(anonymous namespace)::ChannelPosix::OnFileCanReadWithoutBlocking(int) mojo/core/channel_posix.cc:294:14
    #39 0x55b203ce930e in base::MessagePumpLibevent::OnLibeventNotification(int, short, void*) base/message_loop/message_pump_libevent.cc
    #40 0x55b203f43e19 in event_process_active base/third_party/libevent/event.c:381:4
    #41 0x55b203f43e19 in event_base_loop base/third_party/libevent/event.c:521:4
    #42 0x55b203ce9e69 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_libevent.cc:257:5
    #43 0x55b203b8d799 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:429:12
    #44 0x55b203b01936 in base::RunLoop::Run() base/run_loop.cc:124:14

previously allocated by thread T4 (Chrome_IOThread) here:
    #0 0x55b1f91a4ded in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:99:3
    #1 0x55b20a58e039 in std::__1::__unique_if<storage::BlobRegistryImpl::BlobUnderConstruction>::__unique_single std::__1::make_unique<storage::BlobRegistryImpl::BlobUnderConstruction, storage::BlobRegistryImpl*, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, std::__1::vector<mojo::StructPtr<blink::mojom::DataElement>, std::__1::allocator<mojo::StructPtr<blink::mojom::DataElement> > >, base::OnceCallback<void (std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&)> >(storage::BlobRegistryImpl*&&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, std::__1::vector<mojo::StructPtr<blink::mojom::DataElement>, std::__1::allocator<mojo::StructPtr<blink::mojom::DataElement> > >&&, base::OnceCallback<void (std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&)>&&) buildtools/third_party/libc++/trunk/include/memory:3043:28
    #2 0x55b20a58d2f5 in storage::BlobRegistryImpl::Register(mojo::PendingReceiver<blink::mojom::Blob>, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, std::__1::vector<mojo::StructPtr<blink::mojom::DataElement>, std::__1::allocator<mojo::StructPtr<blink::mojom::DataElement> > >, base::OnceCallback<void ()>) storage/browser/blob/blob_registry_impl.cc:574:37
    #3 0x55b1fb1a7958 in blink::mojom::BlobRegistryStubDispatch::AcceptWithResponder(blink::mojom::BlobRegistry*, mojo::Message*, std::__1::unique_ptr<mojo::MessageReceiverWithStatus, std::__1::default_delete<mojo::MessageReceiverWithStatus> >) gen/third_party/blink/public/mojom/blob/blob_registry.mojom.cc:1154:13
    #4 0x55b20a5940e8 in blink::mojom::BlobRegistryStub<mojo::RawPtrImplRefTraits<blink::mojom::BlobRegistry> >::AcceptWithResponder(mojo::Message*, std::__1::unique_ptr<mojo::MessageReceiverWithStatus, std::__1::default_delete<mojo::MessageReceiverWithStatus> >) gen/third_party/blink/public/mojom/blob/blob_registry.mojom.h:265:12
    #5 0x55b204006d30 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:528:56
    #6 0x55b204013868 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:46:24
    #7 0x55b20401f50e in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:953:42
    #8 0x55b20401dc57 in mojo::internal::MultiplexRouter::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/multiplex_router.cc:620:38
    #9 0x55b204013952 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:41:19
    #10 0x55b203ffc8d0 in mojo::Connector::DispatchMessage(mojo::Message) mojo/public/cpp/bindings/lib/connector.cc:539:49
    #11 0x55b203ffea92 in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:627:12
    #12 0x55b20406a03d in Run base/callback.h:132:12
    #13 0x55b20406a03d in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple_watcher.cc:292:14
    #14 0x55b20406aad7 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) mojo/public/cpp/system/simple_watcher.cc:118:22
    #15 0x55b20406835c in mojo::SimpleWatcher::Context::CallNotify(MojoTrapEvent const*) mojo/public/cpp/system/simple_watcher.cc:57:14
    #16 0x55b1fbd2295f in mojo::core::WatcherDispatcher::InvokeWatchCallback(unsigned long, unsigned int, mojo::core::HandleSignalsState const&, unsigned int) mojo/core/watcher_dispatcher.cc:94:3
    #17 0x55b1fbd2193e in mojo::core::Watch::InvokeCallback(unsigned int, mojo::core::HandleSignalsState const&, unsigned int) mojo/core/watch.cc:78:13
    #18 0x55b1fbd15b94 in mojo::core::RequestContext::~RequestContext() mojo/core/request_context.cc:72:20
    #19 0x55b1fbcf2459 in mojo::core::NodeChannel::OnChannelMessage(void const*, unsigned long, std::__1::vector<mojo::PlatformHandle, std::__1::allocator<mojo::PlatformHandle> >) mojo/core/node_channel.cc:739:1
    #20 0x55b1fbcbf803 in mojo::core::Channel::TryDispatchMessage(base::span<char const, 18446744073709551615ul>, unsigned long*) mojo/core/channel.cc:713:16
    #21 0x55b1fbcbeed2 in mojo::core::Channel::OnReadComplete(unsigned long, unsigned long*) mojo/core/channel.cc:611:9
    #22 0x55b1fbd3311f in mojo::core::(anonymous namespace)::ChannelPosix::OnFileCanReadWithoutBlocking(int) mojo/core/channel_posix.cc:294:14
    #23 0x55b203ce930e in base::MessagePumpLibevent::OnLibeventNotification(int, short, void*) base/message_loop/message_pump_libevent.cc
    #24 0x55b203f43e19 in event_process_active base/third_party/libevent/event.c:381:4
    #25 0x55b203f43e19 in event_base_loop base/third_party/libevent/event.c:521:4
    #26 0x55b203ce9e69 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_libevent.cc:257:5
    #27 0x55b203b8d799 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:429:12
    #28 0x55b203b01936 in base::RunLoop::Run() base/run_loop.cc:124:14
    #29 0x55b1fc8d0285 in content::BrowserProcessSubThread::IOThreadRun(base::RunLoop*) content/browser/browser_process_sub_thread.cc:144:11
    #30 0x55b203be1db7 in base::Thread::ThreadMain() base/threading/thread.cc:380:3
    #31 0x55b203cc3cbd in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:81:13

Thread T4 (Chrome_IOThread) created by T0 (chrome) here:
    #0 0x55b1f9166b5a in __interceptor_pthread_create /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:214:3
    #1 0x55b203cc2e0a in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, base::PlatformThreadHandle*, base::ThreadPriority) base/threading/platform_thread_posix.cc:120:13
    #2 0x55b203be0e56 in base::Thread::StartWithOptions(base::Thread::Options const&) base/threading/thread.cc:186:15
    #3 0x55b1fd5ef615 in content::BrowserTaskExecutor::CreateIOThread() content/browser/scheduler/browser_task_executor.cc:338:19
    #4 0x55b202a50eac in content::ContentMainRunnerImpl::RunServiceManager(content::MainFunctionParams&, bool) content/app/content_main_runner_impl.cc:957:9
    #5 0x55b202a50761 in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:879:12
    #6 0x55b202be5ae9 in service_manager::Main(service_manager::MainParams const&) services/service_manager/embedder/main.cc:454:29
    #7 0x55b202a4b646 in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:19:10
    #8 0x55b1f91a7fc4 in ChromeMain chrome/app/chrome_main.cc:110:12
    #9 0x7fdf7adfab96 in __libc_start_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310

SUMMARY: AddressSanitizer: heap-use-after-free base/memory/scoped_refptr.h:207:54 in scoped_refptr
Shadow bytes around the buggy address:
  0x0c1c80051b40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c1c80051b50: 00 00 00 fa fa fa fa fa fa fa fa fa 00 00 00 00
  0x0c1c80051b60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c1c80051b70: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c1c80051b80: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa
=>0x0c1c80051b90: fa fa fa fa fd fd fd fd fd fd fd fd fd fd[fd]fd
  0x0c1c80051ba0: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x0c1c80051bb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c1c80051bc0: 00 00 00 fa fa fa fa fa fa fa fa fa 00 00 00 00
  0x0c1c80051bd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 fa
  0x0c1c80051be0: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
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
==14941==ABORTING
[14993:14993:0421/072105.375257:ERROR:broker_posix.cc(110)] Error sending sync broker message: Broken pipe (32)

Did this work before? N/A 

Chrome version: Chromium 84.0.4110.0   Channel: n/a
OS Version: 6.1 (Windows 7, Windows Server 2008 R2)
Flash Version:

## Attachments

- [poc.zip](attachments/poc.zip) (application/octet-stream, 28.0 KB)

## Timeline

### ad...@google.com (2020-04-21)

pwnall@ - we haven't formally Sheriffed or confirmed this yet, but as a potential Critical please could you take a look.

[Monorail components: Blink>Storage]

### ad...@google.com (2020-04-21)

[Empty comment from Monorail migration]

### ad...@google.com (2020-04-21)

cc'ing release TPMs for M81 on the assumption this will require a respin at some point, assuming it's confirmed.

### cl...@chromium.org (2020-04-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5672689788846080.

### [Deleted User] (2020-04-21)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pw...@chromium.org (2020-04-21)

enne@, dmurph@, mek@: I assigned this based on the knowledge that enne@ worked on moving Blobs to Storage Service, so they should have the freshest mental snapshot of the system.

Please coordinate to ensure that someone investigates this today. Thank you!

### me...@chromium.org (2020-04-21)

I think what's going on is that first BlobRegistryImpl::BlobUnderConstruction::TransportComplete notices that there are no references to the blob being build anymore, so it calls CancelBuildingBlob, which has the side effect of deleting |this| (this being the BlobUnderConstruction). But then the BytesProvider also replied with invalid data (not matching the expected size), so the next branch for if (BlobStatusIsBadIPC) is also reached. However since |this| is deleted, |bad_message_callback_| is also freed, and thus the UAF.

Probably we should just add a if (weak_this) check to the if (BlobStatusIsBadIPC) one as well...

### [Deleted User] (2020-04-21)

This is a critical security issue. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2020-04-21)

[Empty comment from Monorail migration]

### me...@chromium.org (2020-04-21)

actually, I don't think "no reference to the blob" was related. Just simply having a BytesProvider reply with invalid data was enough to trigger the UAF. Should be fixed by https://chromium-review.googlesource.com/c/chromium/src/+/2159583

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/38990b7d56e6dde6bfdc2d81950db8ddef4e4116

commit 38990b7d56e6dde6bfdc2d81950db8ddef4e4116
Author: Marijn Kruisselbrink <mek@chromium.org>
Date: Tue Apr 21 23:51:25 2020

[Blobs] Fix bug when BytesProvider replies with invalid data.

Bug: 1072983
Change-Id: Ideaa0a67680375e770995880a4b8d2014b51d642
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2159583
Reviewed-by: enne <enne@chromium.org>
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Cr-Commit-Position: refs/heads/master@{#761203}

[modify] https://crrev.com/38990b7d56e6dde6bfdc2d81950db8ddef4e4116/storage/browser/blob/blob_registry_impl.cc
[modify] https://crrev.com/38990b7d56e6dde6bfdc2d81950db8ddef4e4116/storage/browser/blob/blob_registry_impl_unittest.cc


### cl...@chromium.org (2020-04-22)

ClusterFuzz testcase 5672689788846080 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=761195:761230

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### ad...@google.com (2020-04-22)

Assuming this applies to all the Blink platforms. Sheriffbot will shortly add merge requests for 81 and 83, so I'll short-cut the process and do so.

### [Deleted User] (2020-04-22)

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

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/40bebdcff14bb2a3157d1f2b49e9417ed108b02d

commit 40bebdcff14bb2a3157d1f2b49e9417ed108b02d
Author: Marijn Kruisselbrink <mek@chromium.org>
Date: Wed Apr 22 16:29:58 2020

[Blobs] Fix bug when BytesProvider replies with invalid data.

(cherry picked from commit 38990b7d56e6dde6bfdc2d81950db8ddef4e4116)

Bug: 1072983
Change-Id: Ideaa0a67680375e770995880a4b8d2014b51d642
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2159583
Reviewed-by: enne <enne@chromium.org>
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#761203}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2161428
Reviewed-by: Krishna Govind <govind@chromium.org>
Cr-Commit-Position: refs/branch-heads/4122@{#7}
Cr-Branched-From: f909a6a231ec78eb10f433f0599d4053ab02b73e-refs/heads/master@{#761185}

[modify] https://crrev.com/40bebdcff14bb2a3157d1f2b49e9417ed108b02d/storage/browser/blob/blob_registry_impl.cc
[modify] https://crrev.com/40bebdcff14bb2a3157d1f2b49e9417ed108b02d/storage/browser/blob/blob_registry_impl_unittest.cc


### sr...@google.com (2020-04-22)

mek@ pls help answer questions in https://crbug.com/chromium/1072983#c14 for merge-review. 

+adetaylor@ to review/approve.


### me...@chromium.org (2020-04-22)

1) Fixes a critical security vulnerability. Fix is simple and includes a unit test.
2) https://crrev.com/38990b7d56e6dde6bfdc2d81950db8ddef4e4116
3) Change has landed and has been verified on master
4) Fixes a critical security vulnerability
5) Not a new feature, fixes a long-standing bug
6) N/A

### ad...@chromium.org (2020-04-22)

Thanks. Approving merge to both M81 (branch 4044) and M83 (branch 4103).

### go...@chromium.org (2020-04-22)

Please verify this bug on canary version #84.0.4122.7 for Android, Desktop and Chrome OS. 

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/85100cf0ce9f3ee7e068fb4a6060f9af8810439b

commit 85100cf0ce9f3ee7e068fb4a6060f9af8810439b
Author: Marijn Kruisselbrink <mek@chromium.org>
Date: Wed Apr 22 20:51:50 2020

[Blobs] Fix bug when BytesProvider replies with invalid data.

(cherry picked from commit 38990b7d56e6dde6bfdc2d81950db8ddef4e4116)

Bug: 1072983
Change-Id: Ideaa0a67680375e770995880a4b8d2014b51d642
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2159583
Reviewed-by: enne <enne@chromium.org>
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#761203}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2161421
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Cr-Commit-Position: refs/branch-heads/4103@{#277}
Cr-Branched-From: 8ad47e8d21f6866e4a37f47d83a860d41debf514-refs/heads/master@{#756066}

[modify] https://crrev.com/85100cf0ce9f3ee7e068fb4a6060f9af8810439b/storage/browser/blob/blob_registry_impl.cc
[modify] https://crrev.com/85100cf0ce9f3ee7e068fb4a6060f9af8810439b/storage/browser/blob/blob_registry_impl_unittest.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/bd0577b00b3b46aea1faf6d07faed1784ddd460f

commit bd0577b00b3b46aea1faf6d07faed1784ddd460f
Author: Marijn Kruisselbrink <mek@chromium.org>
Date: Wed Apr 22 21:10:26 2020

[Blobs] Fix bug when BytesProvider replies with invalid data.

(cherry picked from commit 38990b7d56e6dde6bfdc2d81950db8ddef4e4116)

Bug: 1072983
Change-Id: Ideaa0a67680375e770995880a4b8d2014b51d642
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2159583
Reviewed-by: enne <enne@chromium.org>
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#761203}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2161377
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Cr-Commit-Position: refs/branch-heads/4044@{#972}
Cr-Branched-From: a6d9daf149a473ceea37f629c41d4527bf2055bd-refs/heads/master@{#737173}

[modify] https://crrev.com/bd0577b00b3b46aea1faf6d07faed1784ddd460f/storage/browser/blob/blob_registry_impl.cc
[modify] https://crrev.com/bd0577b00b3b46aea1faf6d07faed1784ddd460f/storage/browser/blob/blob_registry_impl_unittest.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/16a54df2d3b93b0a335050ebfb6be0550c2cacfd

commit 16a54df2d3b93b0a335050ebfb6be0550c2cacfd
Author: Marijn Kruisselbrink <mek@chromium.org>
Date: Wed Apr 22 21:40:02 2020

[Blobs] Fix bug when BytesProvider replies with invalid data.

(cherry picked from commit 38990b7d56e6dde6bfdc2d81950db8ddef4e4116)

Bug: 1072983
Change-Id: Ideaa0a67680375e770995880a4b8d2014b51d642
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2159583
Reviewed-by: enne <enne@chromium.org>
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#761203}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2161620
Reviewed-by: Krishna Govind <govind@chromium.org>
Cr-Commit-Position: refs/branch-heads/4120@{#10}
Cr-Branched-From: 1e7636e63d751cc4c768f85f325e483b50ca66f6-refs/heads/master@{#760368}

[modify] https://crrev.com/16a54df2d3b93b0a335050ebfb6be0550c2cacfd/storage/browser/blob/blob_registry_impl.cc
[modify] https://crrev.com/16a54df2d3b93b0a335050ebfb6be0550c2cacfd/storage/browser/blob/blob_registry_impl_unittest.cc


### go...@chromium.org (2020-04-23)

[Empty comment from Monorail migration]

### go...@chromium.org (2020-04-23)

How is the change looking in canary? 

### [Deleted User] (2020-04-23)

[Empty comment from Monorail migration]

### be...@chromium.org (2020-04-24)

Please can we get confirmation that the fix is correct asap? We want to release this on Monday and need to cut our release candidate.

### me...@chromium.org (2020-04-24)

Afaict things are looking good in canary. I don't see any unexpected crashes, and the repro no longer repros on Canary/Dev.

### ad...@chromium.org (2020-04-24)

Thanks mek@.

### be...@chromium.org (2020-04-24)

Thank you! For Android, I've asked test team to qualify build for release on Monday.

### ad...@google.com (2020-04-26)

[Empty comment from Monorail migration]

### ad...@google.com (2020-04-27)

benmason@ pbommana@ geohsu@ mek@ I realize that I messed up here quite badly.

This is not, in fact, critical.

It's a sandbox escape, so it is the most severe type of "high", but as it requires a pre-existing compromised renderer this is in fact only "high" severity not "critical".

We have two such sandbox escape bugs right now - this and https://crbug.com/chromium/1064891 - so in some ways I'm glad we're making a release, but I asked for that release on the basis that this was Critical, and I'm wrong. SORRY!!! Especially to those (like pbommana@) who have had to do a bit of work over the weekend to get these bugs ready for release :(

I am going to do a mini-post-mortem here to see what lessons I can learn.

### ad...@chromium.org (2020-04-27)

[Empty comment from Monorail migration]

### na...@google.com (2020-04-27)

[Empty comment from Monorail migration]

### na...@google.com (2020-04-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-04-30)

Congrats! The Panel decided to award $20,000 for this report!

### na...@google.com (2020-05-01)

[Empty comment from Monorail migration]

### dg...@google.com (2020-05-13)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-05-21)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-06-30)

mek@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### mm...@chromium.org (2020-07-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1072983?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052082)*
