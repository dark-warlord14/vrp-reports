# Use-After-Free in AllocateSctpSids via DCEP OPEN Message Failure Leads to Renderer Crash

| Field | Value |
|-------|-------|
| **Issue ID** | [503422316](https://issues.chromium.org/issues/503422316) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | ht...@chromium.org |
| **Created** | 2026-04-17 |
| **Bounty** | $11,000.00 |

## Description

# Use-After-Free in AllocateSctpSids via DCEP OPEN Message Failure Leads to Renderer Crash

## Summary

A use-after-free vulnerability exists in the WebRTC SCTP data channel implementation. When DataChannelController::AllocateSctpSids iterates over newly assigned channels using raw pointers, the act of sending the DCEP OPEN control message can synchronously fail if the message exceeds the negotiated max-message-size. The failure path destroys the SctpDataChannel object while the calling function still holds and uses the now-dangling raw pointer. A web page can trigger this deterministically, without any race condition, by creating data channels with long labels and then munging the remote SDP to set an artificially small max-message-size. The bug affects all platforms. MiraclePtr does not protect this code path.

## Bisect

Introducing Commit: `1fbc1f1be61c6ad0ee5212b5e29ebc4103e8b8eb`

- Date: 2025-12-22
- Author: Harald Alvestrand
- Review: <https://webrtc-review.googlesource.com/c/src/+/435520>

## Root Cause

DataChannelController::AllocateSctpSids assigns stream IDs to pending data channels and then starts them. The function collects channels into a local vector of raw pointers before calling OnTransportReady on each one:

```
// third_party/webrtc/pc/data_channel_controller.cc:455-488
void DataChannelController::AllocateSctpSids(SSLRole role) {
  std::vector<SctpDataChannel*> channels_to_start;
  // ...
  for (auto it = sctp_data_channels_n_.begin();
       it != sctp_data_channels_n_.end();) {
    if (!(*it)->sid_n().has_value()) {
      std::optional<StreamId> sid = sid_allocator_.AllocateSid(role);
      if (sid.has_value()) {
        (*it)->SetSctpSid_n(*sid);
        AddSctpDataStream(*sid, (*it)->priority());
        channels_to_start.push_back((*it).get());  // raw pointer extracted
      }
      // ...
    }
    ++it;
  }
  if (ready_to_send) {
    for (auto* channel : channels_to_start) {
      channel->OnTransportReady();  // uses raw pointer after potential free
    }
  }
}

```

A comment in the code acknowledges that "OnTransportReady can cause sending, and sending may fail and cause channel to close," yet the function stores only raw pointers rather than scoped\_refptr to keep the channels alive.

OnTransportReady delegates to UpdateState, which, for channels in the kConnecting state with handshake\_state\_ equal to kHandshakeShouldSendOpen, serializes a DCEP OPEN message and passes it to SendControlMessage:

```
// third_party/webrtc/pc/sctp_data_channel.cc:791-822
void SctpDataChannel::UpdateState() {
  switch (state_) {
    case kConnecting: {
      if (connected_to_transport() && controller_) {
        if (handshake_state_ == kHandshakeShouldSendOpen) {
          CopyOnWriteBuffer payload;
          WriteDataChannelOpenMessage(label_, protocol_, priority_, ordered_,
                                      max_retransmits_, max_retransmit_time_,
                                      &payload);
          SendControlMessage(payload);
        }
        // ... execution continues here after SendControlMessage returns
        if (handshake_state_ == kHandshakeReady ||
            handshake_state_ == kHandshakeWaitingForAck) {
          SetState(kOpen);
        }
      }
      break;
    }
    case kOpen: {  // line 823: the UAF read occurs here
      break;
    }
    // ...
  }
}

```

SendControlMessage calls controller\_->SendData, which routes through DcSctpTransport::SendData. That function enforces the negotiated max-message-size:

```
// third_party/webrtc/media/sctp/dcsctp_transport.cc:341-348
auto max_message_size = socket_->options().max_message_size;
if (max_message_size > 0 && payload.size() > max_message_size) {
  return RTCError(RTCErrorType::INVALID_RANGE);
}

```

When the DCEP OPEN message (12 bytes of header plus the label and protocol strings) exceeds this limit, SendData returns an INVALID\_RANGE error. SendControlMessage then calls CloseAbruptlyWithError:

```
// third_party/webrtc/pc/sctp_data_channel.cc:970-1003
bool SctpDataChannel::SendControlMessage(const CopyOnWriteBuffer& buffer) {
  RTCError err = controller_->SendData(*id_n_, send_params, buffer);
  if (!err.ok()) {
    CloseAbruptlyWithError(err);
  }
  return err.ok();
}

```

CloseAbruptlyWithError transitions the channel through kClosing to kClosed via SetState. Each SetState call notifies the controller through OnChannelStateChanged:

```
// third_party/webrtc/pc/sctp_data_channel.cc:853-865
void SctpDataChannel::SetState(DataState state) {
  state_ = state;
  if (observer_)
    observer_->OnStateChange();
  if (controller_)
    controller_->OnChannelStateChanged(this, state_);
}

```

When the state reaches kClosed, OnChannelStateChanged calls OnSctpDataChannelClosed, which erases the channel from the controller's sctp\_data\_channels\_n\_ vector:

```
// third_party/webrtc/pc/data_channel_controller.cc:110-119
void DataChannelController::OnChannelStateChanged(
    SctpDataChannel* channel,
    DataChannelInterface::DataState state) {
  if (state == DataChannelInterface::DataState::kClosed)
    OnSctpDataChannelClosed(channel);
  // ...
}

// third_party/webrtc/pc/data_channel_controller.cc:497-508
void DataChannelController::OnSctpDataChannelClosed(SctpDataChannel* channel) {
  auto it = absl::c_find_if(sctp_data_channels_n_,
                            [&](const auto& c) { return c.get() == channel; });
  if (it != sctp_data_channels_n_.end()) {
    sctp_data_channels_n_.erase(it);  // drops the scoped_refptr
  }
}

```

If the JavaScript page does not retain a reference to the RTCDataChannel wrapper, the scoped\_refptr in sctp\_data\_channels\_n\_ is the last reference. Erasing it destroys the SctpDataChannel object. Control then unwinds back through CloseAbruptlyWithError, SendControlMessage, and into UpdateState, which proceeds to evaluate the switch statement against state\_, now reading freed memory at offset 232 within the deallocated 312-byte region.

The attacker controls both the label length (which determines the DCEP OPEN message size) and the remote SDP (which sets max-message-size through the a=max-message-size attribute). By creating data channels with labels of approximately 2000 bytes and munging the answer SDP to set max-message-size to 10, the DCEP OPEN message of roughly 2012 bytes is guaranteed to exceed the limit. The bug is fully deterministic and requires no race condition or timing sensitivity.

## Reproduce

Tested at commit `bb43679d94d13`.

Build with ASAN:

```
autoninja -C ~/chromium/src/out/asan-release chrome

```

Launch:

```
ASAN_OPTIONS=detect_odr_violation=0 ~/chromium/src/out/asan-release/chrome \
  --no-sandbox --disable-gpu \
  --js-flags="--expose-gc" \
  --user-data-dir=/tmp/poc-$(date +%s) \
  ~/chromium/src/issue_webrtc032/poc.html

```

The renderer process crashes with a heap-use-after-free within seconds of the SCTP association establishing. No user interaction is required.

```
==2497007==ERROR: AddressSanitizer: heap-use-after-free on address 0x7c1bb8d10ba8 at pc 0x7efc2bf06be6 bp 0x7afaac6c5370 sp 0x7afaac6c5368
READ of size 4 at 0x7c1bb8d10ba8 thread T12 (WebRTC_W_and_N)
    #0 0x7efc2bf06be5 in webrtc::SctpDataChannel::UpdateState() third_party/webrtc/pc/sctp_data_channel.cc:823:13
    #1 0x7efc2bdbc17f in webrtc::DataChannelController::AllocateSctpSids(webrtc::SSLRole) third_party/webrtc/pc/data_channel_controller.cc:501:16
    #2 0x7efc2bcb241f in non-virtual thunk to webrtc::DcSctpTransport::OnConnected() third_party/webrtc/media/sctp/dcsctp_transport.cc:581:25
    #3 0x7efc2bcb6866 in dcsctp::CallbackDeferrer::TriggerDeferred() third_party/webrtc/net/dcsctp/socket/callback_deferrer.cc:49:5
    #4 0x7efc2bcc5122 in dcsctp::DcSctpSocket::ReceivePacket(std::__Cr::span<unsigned char const, 18446744073709551615ul>) third_party/webrtc/net/dcsctp/socket/callback_deferrer.h:54:44
    #5 0x7efc2bae945a in webrtc::callback_list_impl::CallbackListReceivers::Foreach(webrtc::FunctionView<void (webrtc::UntypedFunction&)>) third_party/webrtc/api/function_view.h:96:12
    #6 0x7efc2b9c2f29 in webrtc::PacketTransportInternal::NotifyPacketReceived(webrtc::ReceivedIpPacket const&) third_party/webrtc/rtc_base/callback_list.h:211:16
    #7 0x7efc2be0ec0c in webrtc::DtlsTransportInternalImpl::OnDtlsEvent(int, int) third_party/webrtc/p2p/dtls/dtls_transport.cc:1019:9
    #8 0x7efc2be03b93 in webrtc::StreamInterfaceChannel::OnPacketReceived(std::__Cr::span<unsigned char const, 18446744073709551615ul>) third_party/abseil-cpp/absl/functional/internal/any_invocable.h:766:1
    #9 0x7efc2be0dad8 in webrtc::DtlsTransportInternalImpl::OnReadPacket(webrtc::PacketTransportInternal*, webrtc::ReceivedIpPacket const&, bool) third_party/webrtc/p2p/dtls/dtls_transport.cc:1114:21
    #10 0x7efc2bae945a in webrtc::callback_list_impl::CallbackListReceivers::Foreach(webrtc::FunctionView<void (webrtc::UntypedFunction&)>) third_party/webrtc/api/function_view.h:96:12
    #11 0x7efc2b9c2f29 in webrtc::PacketTransportInternal::NotifyPacketReceived(webrtc::ReceivedIpPacket const&) third_party/webrtc/rtc_base/callback_list.h:211:16
    #12 0x7efc2b9c0f00 in void absl::internal_any_invocable::LocalInvoker<false, void, webrtc::P2PTransportChannel::AddConnection(webrtc::Connection*)::$_0&, webrtc::Connection*, webrtc::ReceivedIpPacket const&>(absl::internal_any_invocable::TypeErasedState*, absl::internal_any_invocable::ForwardedParameter<webrtc::Connection*>::type, absl::internal_any_invocable::ForwardedParameter<webrtc::ReceivedIpPacket const&>::type) third_party/webrtc/p2p/base/p2p_transport_channel.cc:2270:3
    #13 0x7efc2b98985e in webrtc::Connection::OnReadPacket(webrtc::ReceivedIpPacket const&) third_party/abseil-cpp/absl/functional/internal/any_invocable.h:766:1
    #14 0x7efc2c0124a8 in webrtc::UDPPort::HandleIncomingPacket(webrtc::AsyncPacketSocket*, webrtc::ReceivedIpPacket const&) third_party/webrtc/p2p/base/stun_port.cc:363:3
    #15 0x7efbde87d286 in blink::(anonymous namespace)::IpcPacketSocket::OnDataReceived(net::IPEndPoint const&, base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>, base::TimeTicks const&, webrtc::EcnMarking) third_party/blink/renderer/platform/p2p/ipc_socket_factory.cc:709:3
    #16 0x7efbde88a16a in non-virtual thunk to blink::P2PSocketClientImpl::DataReceived(blink::Vector<mojo::StructPtr<network::mojom::blink::P2PReceivedPacket>, 0u, blink::PartitionAllocator>) third_party/blink/renderer/platform/p2p/socket_client_impl.cc:187:18
    #17 0x7efbdf6d7770 in network::mojom::blink::P2PSocketClientStubDispatch::Accept(network::mojom::blink::P2PSocketClient*, mojo::Message*) gen/services/network/public/mojom/p2p.mojom-blink.cc:2039:13
    #18 0x7efc3e0f2062 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1085:54
    #19 0x7efc3e10942b in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:44:19
    #20 0x7efc3e0f7914 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:747:20
    #21 0x7efc3e118a0e in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:1204:42
    #22 0x7efc3e11723d in mojo::internal::MultiplexRouter::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/multiplex_router.cc:790:7
    #23 0x7efc3e10942b in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:44:19
    #24 0x7efc3e0ddc8f in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) mojo/public/cpp/bindings/lib/connector.cc:567:49
    #25 0x7efc3e0df4de in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:628:14
    #26 0x7efc3e0e0404 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::*&&)(), base::WeakPtr<mojo::Connector>&&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(), base::WeakPtr<mojo::Connector>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #27 0x7efc3cb61b59 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #28 0x7efc3cbdc1d0 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #29 0x7efc3cbdb1a6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:336:40
    #30 0x7efc3ca02e24 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #31 0x7efc3cbdd823 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:640:12
    #32 0x7efc3caccc72 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #33 0x7efc3cc75892 in base::Thread::Run(base::RunLoop*) base/threading/thread.cc:356:13
    #34 0x7efc3cc75df5 in base::Thread::ThreadMain() base/threading/thread.cc:426:3
    #35 0x7efc3ccdaa4c in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:102:13
    #36 0x55a454fd0b36 in asan_thread_start(void*) asan_interceptors.cpp

0x7c1bb8d10ba8 is located 232 bytes inside of 312-byte region [0x7c1bb8d10ac0,0x7c1bb8d10bf8)
freed by thread T12 (WebRTC_W_and_N) here:
    #0 0x55a45500cdc2 in operator delete(void*, unsigned long) (out/asan-release/chrome+0x681cdc2) (BuildId: 436e46875e0ded00)
    #1 0x7efc2bf0e39c in webrtc::RefCountedObject<webrtc::SctpDataChannel>::Release() const third_party/webrtc/rtc_base/ref_counted_object.h:42:7
    #2 0x7efc2bdbb4bb in webrtc::DataChannelController::OnSctpDataChannelClosed(webrtc::SctpDataChannel*) third_party/webrtc/api/scoped_refptr.h:105:13
    #3 0x7efc2bdbaf32 in webrtc::DataChannelController::OnChannelStateChanged(webrtc::SctpDataChannel*, webrtc::DataChannelInterface::DataState) third_party/webrtc/pc/data_channel_controller.cc:119:5
    #4 0x7efc2bf0b244 in webrtc::SctpDataChannel::SendControlMessage(webrtc::CopyOnWriteBuffer const&) third_party/webrtc/pc/sctp_data_channel.cc:1013:5
    #5 0x7efc2bf0655c in webrtc::SctpDataChannel::UpdateState() third_party/webrtc/pc/sctp_data_channel.cc:817:11
    #6 0x7efc2bdbc17f in webrtc::DataChannelController::AllocateSctpSids(webrtc::SSLRole) third_party/webrtc/pc/data_channel_controller.cc:501:16
    #7 0x7efc2bcb241f in non-virtual thunk to webrtc::DcSctpTransport::OnConnected() third_party/webrtc/media/sctp/dcsctp_transport.cc:581:25
    #8 0x7efc2bcb6866 in dcsctp::CallbackDeferrer::TriggerDeferred() third_party/webrtc/net/dcsctp/socket/callback_deferrer.cc:49:5
    #9 0x7efc2bcc5122 in dcsctp::DcSctpSocket::ReceivePacket(std::__Cr::span<unsigned char const, 18446744073709551615ul>) third_party/webrtc/net/dcsctp/socket/callback_deferrer.h:54:44
    #10 0x7efc2bae945a in webrtc::callback_list_impl::CallbackListReceivers::Foreach(webrtc::FunctionView<void (webrtc::UntypedFunction&)>) third_party/webrtc/api/function_view.h:96:12
    #11 0x7efc2b9c2f29 in webrtc::PacketTransportInternal::NotifyPacketReceived(webrtc::ReceivedIpPacket const&) third_party/webrtc/rtc_base/callback_list.h:211:16
    #12 0x7efc2be0ec0c in webrtc::DtlsTransportInternalImpl::OnDtlsEvent(int, int) third_party/webrtc/p2p/dtls/dtls_transport.cc:1019:9
    #13 0x7efc2be03b93 in webrtc::StreamInterfaceChannel::OnPacketReceived(std::__Cr::span<unsigned char const, 18446744073709551615ul>) third_party/abseil-cpp/absl/functional/internal/any_invocable.h:766:1
    #14 0x7efc2be0dad8 in webrtc::DtlsTransportInternalImpl::OnReadPacket(webrtc::PacketTransportInternal*, webrtc::ReceivedIpPacket const&, bool) third_party/webrtc/p2p/dtls/dtls_transport.cc:1114:21
    #15 0x7efc2bae945a in webrtc::callback_list_impl::CallbackListReceivers::Foreach(webrtc::FunctionView<void (webrtc::UntypedFunction&)>) third_party/webrtc/api/function_view.h:96:12
    #16 0x7efc2b9c2f29 in webrtc::PacketTransportInternal::NotifyPacketReceived(webrtc::ReceivedIpPacket const&) third_party/webrtc/rtc_base/callback_list.h:211:16
    #17 0x7efc2b9c0f00 in void absl::internal_any_invocable::LocalInvoker<false, void, webrtc::P2PTransportChannel::AddConnection(webrtc::Connection*)::$_0&, webrtc::Connection*, webrtc::ReceivedIpPacket const&>(absl::internal_any_invocable::TypeErasedState*, absl::internal_any_invocable::ForwardedParameter<webrtc::Connection*>::type, absl::internal_any_invocable::ForwardedParameter<webrtc::ReceivedIpPacket const&>::type) third_party/webrtc/p2p/base/p2p_transport_channel.cc:2270:3
    #18 0x7efc2b98985e in webrtc::Connection::OnReadPacket(webrtc::ReceivedIpPacket const&) third_party/abseil-cpp/absl/functional/internal/any_invocable.h:766:1
    #19 0x7efc2c0124a8 in webrtc::UDPPort::HandleIncomingPacket(webrtc::AsyncPacketSocket*, webrtc::ReceivedIpPacket const&) third_party/webrtc/p2p/base/stun_port.cc:363:3
    #20 0x7efbde87d286 in blink::(anonymous namespace)::IpcPacketSocket::OnDataReceived(net::IPEndPoint const&, base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>, base::TimeTicks const&, webrtc::EcnMarking) third_party/blink/renderer/platform/p2p/ipc_socket_factory.cc:709:3
    #21 0x7efbde88a16a in non-virtual thunk to blink::P2PSocketClientImpl::DataReceived(blink::Vector<mojo::StructPtr<network::mojom::blink::P2PReceivedPacket>, 0u, blink::PartitionAllocator>) third_party/blink/renderer/platform/p2p/socket_client_impl.cc:187:18
    #22 0x7efbdf6d7770 in network::mojom::blink::P2PSocketClientStubDispatch::Accept(network::mojom::blink::P2PSocketClient*, mojo::Message*) gen/services/network/public/mojom/p2p.mojom-blink.cc:2039:13
    #23 0x7efc3e0f2062 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1085:54
    #24 0x7efc3e10942b in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:44:19
    #25 0x7efc3e0f7914 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:747:20
    #26 0x7efc3e118a0e in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:1204:42
    #27 0x7efc3e11723d in mojo::internal::MultiplexRouter::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/multiplex_router.cc:790:7
    #28 0x7efc3e10942b in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:44:19
    #29 0x7efc3e0ddc8f in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) mojo/public/cpp/bindings/lib/connector.cc:567:49

previously allocated by thread T12 (WebRTC_W_and_N) here:
    #0 0x55a45500c1bd in operator new(unsigned long) (out/asan-release/chrome+0x681c1bd) (BuildId: 436e46875e0ded00)
    #1 0x7efc2bf04232 in webrtc::SctpDataChannel::Create(webrtc::WeakPtr<webrtc::SctpDataChannelControllerInterface>, std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>, bool, webrtc::InternalDataChannelInit const&, webrtc::Thread*, webrtc::Thread*) third_party/webrtc/api/make_ref_counted.h:90:27
    #2 0x7efc2bdbf7c9 in webrtc::DataChannelController::CreateDataChannel(std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>, webrtc::InternalDataChannelInit&) third_party/webrtc/pc/data_channel_controller.cc:409:44
    #3 0x7efc2bdc5081 in void webrtc::FunctionView<void ()>::CallVoidPtr<webrtc::RTCErrorOr<webrtc::scoped_refptr<webrtc::SctpDataChannel>> webrtc::Thread::BlockingCall<webrtc::DataChannelController::InternalCreateDataChannelWithProxy(std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>, webrtc::InternalDataChannelInit const&)::$_0, webrtc::RTCErrorOr<webrtc::scoped_refptr<webrtc::SctpDataChannel>>, void>(webrtc::DataChannelController::InternalCreateDataChannelWithProxy(std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>, webrtc::InternalDataChannelInit const&)::$_0&&, base::Location const&)::'lambda'()>(webrtc::FunctionView<void ()>::VoidUnion) third_party/webrtc/pc/data_channel_controller.cc:444:24
    #4 0x7efbd14258e4 in webrtc::ThreadWrapper::ProcessPendingSends() third_party/webrtc/api/function_view.h:96:12
    #5 0x7efbd1428314 in base::internal::Invoker<base::internal::FunctorTraits<void (webrtc::ThreadWrapper::*&&)(), base::WeakPtr<webrtc::ThreadWrapper>&&>, base::internal::BindState<true, true, false, void (webrtc::ThreadWrapper::*)(), base::WeakPtr<webrtc::ThreadWrapper>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #6 0x7efc3cb61b59 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #7 0x7efc3cbdc1d0 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #8 0x7efc3cbdb1a6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:336:40
    #9 0x7efc3ca02e24 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #10 0x7efc3cbdd823 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:640:12
    #11 0x7efc3caccc72 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #12 0x7efc3cc75892 in base::Thread::Run(base::RunLoop*) base/threading/thread.cc:356:13
    #13 0x7efc3cc75df5 in base::Thread::ThreadMain() base/threading/thread.cc:426:3
    #14 0x7efc3ccdaa4c in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:102:13
    #15 0x55a454fd0b36 in asan_thread_start(void*) asan_interceptors.cpp

SUMMARY: AddressSanitizer: heap-use-after-free third_party/webrtc/pc/sctp_data_channel.cc:823:13 in webrtc::SctpDataChannel::UpdateState()
Shadow bytes around the buggy address:
  0x7c1bb8d10900: fa fa fa fa fa fa f7 fa f7 00 00 00 00 00 00 00
  0x7c1bb8d10980: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c1bb8d10a00: 00 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa
  0x7c1bb8d10a80: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x7c1bb8d10b00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x7c1bb8d10b80: fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd fa
  0x7c1bb8d10c00: fa fa fa fa fa fa f7 fa 00 00 00 00 00 00 00 01
  0x7c1bb8d10c80: fc 00 00 00 00 00 00 00 00 00 01 fc 00 00 00 00
  0x7c1bb8d10d00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 fa
  0x7c1bb8d10d80: fa fa fa fa fa fa f7 fa 00 00 00 00 00 00 00 01
  0x7c1bb8d10e00: fc 00 00 00 00 00 00 00 00 00 01 fc 00 00 00 00
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

==2497007==ADDITIONAL INFO

==2497007==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7efc3e0dff96 in mojo::Connector::ScheduleDispatchOfPendingMessagesOrWaitForMore(unsigned long) mojo/public/cpp/bindings/lib/connector.cc:588:7
    #1 0x7efc3e0dff96 in mojo::Connector::ScheduleDispatchOfPendingMessagesOrWaitForMore(unsigned long) mojo/public/cpp/bindings/lib/connector.cc:588:7
    #2 0x7efc3e0dff96 in mojo::Connector::ScheduleDispatchOfPendingMessagesOrWaitForMore(unsigned long) mojo/public/cpp/bindings/lib/connector.cc:588:7
    #3 0x7efc3e0dff96 in mojo::Connector::ScheduleDispatchOfPendingMessagesOrWaitForMore(unsigned long) mojo/public/cpp/bindings/lib/connector.cc:588:7

MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==2497007==END OF ADDITIONAL INFO

==2497007==ABORTING

```
## References

- [data\_channel\_controller.cc:455 (AllocateSctpSids)](https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/pc/data_channel_controller.cc;l=455)
- [data\_channel\_controller.cc:497 (OnSctpDataChannelClosed)](https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/pc/data_channel_controller.cc;l=497)
- [sctp\_data\_channel.cc:791 (UpdateState)](https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/pc/sctp_data_channel.cc;l=791)
- [sctp\_data\_channel.cc:970 (SendControlMessage)](https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/pc/sctp_data_channel.cc;l=970)
- [sctp\_data\_channel.cc:766 (CloseAbruptlyWithError)](https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/pc/sctp_data_channel.cc;l=766)
- [dcsctp\_transport.cc:341 (SendData max\_message\_size check)](https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/media/sctp/dcsctp_transport.cc;l=341)
- [Introducing commit 1fbc1f1be6](https://webrtc-review.googlesource.com/c/src/+/435520)

## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 21.2 KB)
- [readme.md](attachments/readme.md) (text/markdown, 598 B)
- [poc.html](attachments/poc.html) (text/html, 3.3 KB)

## Timeline

### an...@chromium.org (2026-04-17)

Setting severity to S1 (renderer memory corruption) and FoundIn to 147 based on date of bisect commit.

### ch...@google.com (2026-04-18)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-18)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-04-21)

Project: src  

Branch:  main  

Author:  Harald Alvestrand [hta@webrtc.org](mailto:hta@webrtc.org)  

Link:    <https://webrtc-review.googlesource.com/465701>

pc: fix use-after-free in AllocateSctpSids

---


Expand for full commit details
```
     
    AllocateSctpSids iterates over newly assigned channels using raw 
    pointers and calls OnTransportReady on each one. OnTransportReady 
    can synchronously fail (e.g. if sending the DCEP OPEN message 
    fails), which may cause the channel to close and be deleted, 
    leaving the controller with a dangling pointer. 
     
    This change ensures the channels are kept alive during the loop by 
    using scoped_refptr for the temporary collection. This fixes the 
    UAF for any failure mode that prevents synchronous sending of the 
    initialization message. 
     
    Bug: chromium:503422316 
    Change-Id: I1b927386fb4ed4279036835a244320aba6acf875 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/465701 
    Commit-Queue: Harald Alvestrand <hta@webrtc.org> 
    Auto-Submit: Harald Alvestrand <hta@webrtc.org> 
    Reviewed-by: Danil Chapovalov <danilchap@webrtc.org> 
    Cr-Commit-Position: refs/heads/main@{#47503}

```

---

Files:

- M `pc/data_channel_controller.cc`
- M `pc/data_channel_controller_unittest.cc`

---

Hash: 13fdb6e802e5c326533445aa15f9717f2fc26004  

Date: Tue Apr 21 14:59:35 2026


---

### dx...@google.com (2026-04-22)

Project: chromium/src  

Branch:  main  

Author:  [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com) [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7784212>

Roll WebRTC from c420a240e19e to 5ec4c28c1f05 (7 revisions)

---


Expand for full commit details
```
     
    https://webrtc.googlesource.com/src.git/+log/c420a240e19e..5ec4c28c1f05 
     
    2026-04-21 hta@webrtc.org Discard STUN attributes that follow MESSAGE-INTEGRITY 
    2026-04-21 sprang@webrtc.org Remove audio stream from old sync group on update. 
    2026-04-21 hta@webrtc.org pc: fix use-after-free in AllocateSctpSids 
    2026-04-21 mfoltz@chromium.org [Pipewire] Fix mouse cursor data race. 
    2026-04-21 chromium-webrtc-autoroll@webrtc-ci.iam.gserviceaccount.com Roll chromium_revision 6c2e563d17..7ba297c76f (1618153:1618313) 
    2026-04-21 perkj@webrtc.org Send packets as ECT(1) after all route changes 
    2026-04-21 chromium-webrtc-autoroll@webrtc-ci.iam.gserviceaccount.com Roll chromium_revision c2ee2515c0..6c2e563d17 (1618020:1618153) 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/webrtc-chromium-autoroll 
    Please CC webrtc-chromium-sheriffs-robots@google.com,webrtc-infra@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in WebRTC: https://bugs.chromium.org/p/webrtc/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Bug: chromium:503422316,chromium:504551032,chromium:504567957,chromium:504599749 
    Tbr: webrtc-chromium-sheriffs-robots@google.com 
    Change-Id: I682f77f56171d2f1bce52d662c954cff8397d253 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7784212 
    Bot-Commit: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1618588}

```

---

Files:

- M `DEPS`
- M `third_party/webrtc`

---

Hash: [98df43e77043dbf844d95b29512af37ae3fb2776](https://chromiumdash.appspot.com/commit/98df43e77043dbf844d95b29512af37ae3fb2776)  

Date: Wed Apr 22 01:06:25 2026


---

### sp...@google.com (2026-05-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
hq renderer memory corruption with bisect


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-20)

Requesting merge to M148 because latest trunk commit is in 149.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

### ch...@google.com (2026-05-20)

**M148** merge request created. **Please update [crbug/514924244](https://crbug.com/514924244) to have this merge reviewed.**

### dx...@google.com (2026-06-29)

Project: src  

Branch:  refs/branch-heads/7778  

Author:  Harald Alvestrand [hta@webrtc.org](mailto:hta@webrtc.org)  

Link:    <https://webrtc-review.googlesource.com/485860>

[M148] pc: fix use-after-free in AllocateSctpSids

---


Expand for full commit details
```
[M148] pc: fix use-after-free in AllocateSctpSids

AllocateSctpSids iterates over newly assigned channels using raw
pointers and calls OnTransportReady on each one. OnTransportReady
can synchronously fail (e.g. if sending the DCEP OPEN message
fails), which may cause the channel to close and be deleted,
leaving the controller with a dangling pointer.

This change ensures the channels are kept alive during the loop by
using scoped_refptr for the temporary collection. This fixes the
UAF for any failure mode that prevents synchronous sending of the
initialization message.

(cherry picked from commit 13fdb6e802e5c326533445aa15f9717f2fc26004)

No-Try: true
Bug: chromium:503422316
Fixed: chromium:514924244
Change-Id: I1b927386fb4ed4279036835a244320aba6acf875
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/465701
Commit-Queue: Harald Alvestrand <hta@webrtc.org>
Auto-Submit: Harald Alvestrand <hta@webrtc.org>
Reviewed-by: Danil Chapovalov <danilchap@webrtc.org>
Cr-Original-Commit-Position: refs/heads/main@{#47503}
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/485860
Cr-Commit-Position: refs/branch-heads/7778@{#16}
Cr-Branched-From: ca896b7ffef011bbf6957c99d413c5aac602c99f-refs/heads/main@{#47319}

```

---

Files:

- M `pc/data_channel_controller.cc`

---

Hash: bc4f3f308398a9cd542b9f70c31cb231a05a47d7  

Date: Tue Apr 21 14:59:35 2026


---

### pe...@google.com (2026-06-29)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ht...@chromium.org (2026-06-30)

1. The code that was fixed was introduced in commit 1fbc1f1be61c6ad0ee5212b5e29ebc4103e8b8eb on Dec 22, 2025. It's possible that the issue existed before, but the patch won't apply cleanly there. That change made it to 145.0.7603.0, so patching 144 would require a different patch (albeit probably quite similar).

2. No. The introducing change was a refactoring.


### qk...@google.com (2026-07-24)

Add 'LTS-NotApplicable-144` because M144 didn't have the suspected CL[1]. Besides, the fix should be updated to be merged to M144.

[1] https://webrtc-review.git.corp.google.com/c/src/+/435520.

### ch...@google.com (2026-07-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/503422316)*
