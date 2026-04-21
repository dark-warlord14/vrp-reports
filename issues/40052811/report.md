# UAF in sctp_transport

| Field | Value |
|-------|-------|
| **Issue ID** | [40052811](https://issues.chromium.org/issues/40052811) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cd...@gmail.com |
| **Assignee** | de...@chromium.org |
| **Created** | 2020-07-10 |
| **Bounty** | $7,500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36

Steps to reproduce the problem:
./chrome http://localhost/poc.html

What is the expected behavior?

What went wrong?
**This template is ONLY for reporting security bugs. If you are reporting a**
**Download Protection Bypass bug, please use the "Security - Download**
**Protection" template. For all other reports, please use a different**
**template.**

**Please READ THIS FAQ before filing a bug: https://chromium.googlesource.com**
**/chromium/src/+/master/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**
**https://www.chromium.org/Home/chromium-security/reporting-security-bugs**

**Reports may be eligible for reward payments under the Chrome VRP:**
**http://g.co/ChromeBugRewards**

**NOTE: Security bugs are normally made public once a fix has been widely**
**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**

When create `RTCPeerConnection`, the `SctpTransport::UsrSctpWrapper::InitializeUsrSctp` will be called

```c++
// src/third_party/webrtc/media/sctp/sctp_transport.cc
static void InitializeUsrSctp() {
    RTC_LOG(LS_INFO) << __FUNCTION__;

    // register the SCTP Timer
    usrsctp_init(0, &UsrSctpWrapper::OnSctpOutboundPacket, &DebugSctpPrintf); 

    // ...

    // create SctpTransportMap object
    g_transport_map_ = new SctpTransportMap();
}
```

When `RTCPeerConnection` closed, the `SctpTransport::UsrSctpWrapper::DecrementUsrSctpUsageCount` is called

```c++
static void DecrementUsrSctpUsageCount() {
    rtc::GlobalLockScope lock(&g_usrsctp_lock_);
    --g_usrsctp_usage_count;
    if (!g_usrsctp_usage_count) {
        UninitializeUsrSctp();
    }
}
```

If `g_usrsctp_usage_count == 0`，the `UninitializeUsrSctp` called and the SctpTransportMap object will be released

```c++
// src/third_party/webrtc/media/sctp/sctp_transport.cc
static void UninitializeUsrSctp() {

    // relese the SctpTransportMap object
    // but the pointer is not set to NULL.
    delete g_transport_map_;
    RTC_LOG(LS_INFO) << __FUNCTION__;

    for (size_t i = 0; i < 300; ++i) {
        if (usrsctp_finish() == 0) {
            return;
        }

        rtc::Thread::SleepMs(10);
    }
    RTC_LOG(LS_ERROR) << "Failed to shutdown usrsctp.";
}
```

The function release the SctpTransportMap object, but the pointer `g_transport_map_` is not set to NULL.

In `InitializeUsrSctp()`, `UsrSctpWrapper::OnSctpOutboundPacket` is registered as a Timer Handler, it will be called in **another therad**.

```c++
static int OnSctpOutboundPacket(void* addr,
                                  void* data,
                                  size_t length,
                                  uint8_t tos,
                                  uint8_t set_df) {
    SctpTransport* transport =
        g_transport_map_->Retrieve(reinterpret_cast<uintptr_t>(addr));
    // ...
    return 0;
  }
```

It calls `g_transport_map_->Retrieve()` but not check the `g_transport_map_` pointer.

```c++
void *
user_sctp_timer_iterate(void *arg)
{
	sctp_userspace_set_threadname("SCTP timer");
	for (;;) {
#if defined (__Userspace_os_Windows)
		Sleep(TIMEOUT_INTERVAL);
#else
		struct timespec amount, remaining;

		remaining.tv_sec = 0;
		remaining.tv_nsec = TIMEOUT_INTERVAL * 1000 * 1000;
		do {
			amount = remaining;
		} while (nanosleep(&amount, &remaining) == -1);
#endif
		if (atomic_cmpset_int(&SCTP_BASE_VAR(timer_thread_should_exit), 1, 1)) {
			break;
		}
        // sctp_handle_tick will invoke OnSctpOutboundPacket
		sctp_handle_tick(MSEC_TO_TICKS(TIMEOUT_INTERVAL));
	}
	return (NULL);
}
```

A UAF occurs when `sctp_handle_tick`  is invoked and `UninitializeUsrSctp`  is invoked at the same time.

The triggering of this vulnerability is very unstable, perhaps due to limitations and machine performance, but the exact cause is not clear.

**VERSION**
Chrome Version: 86.0.4196.0 (Developer Build) (64-bit)
Operating System: Ubuntu 16.04

**REPRODUCTION CASE**
./chrome http://localhost/poc.html
Crash State: 
==43979==ERROR: AddressSanitizer: heap-use-after-free on address 0x60b00028fe88 at pc 0x5573502708d4 bp 0x7feb9b7da5f0 sp 0x7feb9b7da5e8
READ of size 8 at 0x60b00028fe88 thread T51 (SCTP timer)
    #0 0x5573502708d3 in size ./../../buildtools/third_party/libc++/trunk/include/__hash_table:799:55
    #1 0x5573502708d3 in bucket_count ./../../buildtools/third_party/libc++/trunk/include/__hash_table:1204:45
    #2 0x5573502708d3 in find<unsigned long> ./../../buildtools/third_party/libc++/trunk/include/__hash_table:2488:22
    #3 0x5573502708d3 in find ./../../buildtools/third_party/libc++/trunk/include/unordered_map:1280:69
    #4 0x5573502708d3 in Retrieve ./../../third_party/webrtc/media/sctp/sctp_transport.cc:112:20
    #5 0x5573502708d3 in cricket::SctpTransport::UsrSctpWrapper::OnSctpOutboundPacket(void*, void*, unsigned long, unsigned char, unsigned char) ./../../third_party/webrtc/media/sctp/sctp_transport.cc:344:27
    #6 0x5573502bce9e in sctp_lowlevel_chunk_output ./../../third_party/usrsctp/usrsctplib/usrsctplib/netinet/sctp_output.c:5043:10
    #7 0x5573502e2028 in sctp_send_abort_tcb ./../../third_party/usrsctp/usrsctplib/usrsctplib/netinet/sctp_output.c:11570:15
    #8 0x557350289017 in sctp_inpcb_free ./../../third_party/usrsctp/usrsctplib/usrsctplib/netinet/sctp_pcb.c:4120:4
    #9 0x557350369b44 in sctp_close ./../../third_party/usrsctp/usrsctplib/usrsctplib/netinet/sctp_usrreq.c:0:0
    #10 0x5573502730a9 in sofree ./../../third_party/usrsctp/usrsctplib/usrsctplib/user_socket.c:298:2
    #11 0x55735029ddf9 in sctp_timeout_handler ./../../third_party/usrsctp/usrsctplib/usrsctplib/netinet/sctputil.c:2086:3
    #12 0x55735035a36b in sctp_handle_tick ./../../third_party/usrsctp/usrsctplib/usrsctplib/netinet/sctp_callout.c:167:4
    #13 0x55735035a574 in user_sctp_timer_iterate ./../../third_party/usrsctp/usrsctplib/usrsctplib/netinet/sctp_callout.c:209:3
    #14 0x7febd5e646da in start_thread /build/glibc-OTsEL5/glibc-2.27/nptl/pthread_create.c:463:0

0x60b00028fe88 is located 72 bytes inside of 104-byte region [0x60b00028fe40,0x60b00028fea8)
freed by thread T20 (WebRTC_Network) here:
    #0 0x5573427ab7cd in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:160:3
    #1 0x557350270ef3 in cricket::SctpTransport::UsrSctpWrapper::UninitializeUsrSctp() ./../../third_party/webrtc/media/sctp/sctp_transport.cc:305:5
    #2 0x5573502630b7 in DecrementUsrSctpUsageCount ./../../third_party/webrtc/media/sctp/sctp_transport.cc:332:7
    #3 0x5573502630b7 in cricket::SctpTransport::CloseSctpSocket() ./../../third_party/webrtc/media/sctp/sctp_transport.cc:943:5
    #4 0x557350262d1d in cricket::SctpTransport::~SctpTransport() ./../../third_party/webrtc/media/sctp/sctp_transport.cc:501:3
    #5 0x5573502631fc in cricket::SctpTransport::~SctpTransport() ./../../third_party/webrtc/media/sctp/sctp_transport.cc:499:33
    #6 0x5573505c03ee in operator() ./../../buildtools/third_party/libc++/trunk/include/memory:2378:5
    #7 0x5573505c03ee in reset ./../../buildtools/third_party/libc++/trunk/include/memory:2633:7
    #8 0x5573505c03ee in operator= ./../../buildtools/third_party/libc++/trunk/include/memory:2591:5
    #9 0x5573505c03ee in webrtc::SctpTransport::Clear() ./../../third_party/webrtc/pc/sctp_transport.cc:73:30
    #10 0x557350563bec in cricket::JsepTransport::~JsepTransport() ./../../third_party/webrtc/pc/jsep_transport.cc:161:22
    #11 0x557350564a9c in cricket::JsepTransport::~JsepTransport() ./../../third_party/webrtc/pc/jsep_transport.cc:159:33
    #12 0x557350532de8 in operator() ./../../buildtools/third_party/libc++/trunk/include/memory:2378:5
    #13 0x557350532de8 in reset ./../../buildtools/third_party/libc++/trunk/include/memory:2633:7
    #14 0x557350532de8 in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/memory:2587:19
    #15 0x557350532de8 in ~pair ./../../buildtools/third_party/libc++/trunk/include/utility:297:29
    #16 0x557350532de8 in __destroy<std::__1::pair<const std::__1::basic_string<char>, std::__1::unique_ptr<cricket::JsepTransport, std::__1::default_delete<cricket::JsepTransport> > > > ./../../buildtools/third_party/libc++/trunk/include/memory:1787:23
    #17 0x557350532de8 in destroy<std::__1::pair<const std::__1::basic_string<char>, std::__1::unique_ptr<cricket::JsepTransport, std::__1::default_delete<cricket::JsepTransport> > > > ./../../buildtools/third_party/libc++/trunk/include/memory:1619:14
    #18 0x557350532de8 in std::__1::__tree<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::unique_ptr<cricket::JsepTransport, std::__1::default_delete<cricket::JsepTransport> > >, std::__1::__map_value_compare<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::unique_ptr<cricket::JsepTransport, std::__1::default_delete<cricket::JsepTransport> > >, std::__1::less<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > >, true>, std::__1::allocator<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::unique_ptr<cricket::JsepTransport, std::__1::default_delete<cricket::JsepTransport> > > > >::destroy(std::__1::__tree_node<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::unique_ptr<cricket::JsepTransport, std::__1::default_delete<cricket::JsepTransport> > >, void*>*) ./../../buildtools/third_party/libc++/trunk/include/__tree:1833:9
    #19 0x557350510b1b in clear ./../../buildtools/third_party/libc++/trunk/include/__tree:1870:5
    #20 0x557350510b1b in clear ./../../buildtools/third_party/libc++/trunk/include/map:1309:37
    #21 0x557350510b1b in webrtc::JsepTransportController::DestroyAllJsepTransports_n() ./../../third_party/webrtc/pc/jsep_transport_controller.cc:1287:28
    #22 0x55734b589956 in jingle_glue::JingleThreadWrapper::Dispatch(rtc::Message*) ./../../jingle/glue/thread_wrapper.cc:159:22
    #23 0x55734b58a6b8 in jingle_glue::JingleThreadWrapper::ProcessPendingSends() ./../../jingle/glue/thread_wrapper.cc:227:7
    #24 0x55734d392363 in Run ./../../base/callback.h:99:12
    #25 0x55734d392363 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:142:33
    #26 0x55734d3ccf69 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:332:23
    #27 0x55734d3cc878 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:252:36
    #28 0x55734d2c6c00 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39:55
    #29 0x55734d3ce1e9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:451:12
    #30 0x55734d340de6 in base::RunLoop::Run() ./../../base/run_loop.cc:124:14
    #31 0x55734d425437 in base::Thread::ThreadMain() ./../../base/threading/thread.cc:380:3
    #32 0x55734d4a595d in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:81:13
    #33 0x7febd5e646da in start_thread /build/glibc-OTsEL5/glibc-2.27/nptl/pthread_create.c:463:0

previously allocated by thread T20 (WebRTC_Network) here:
    #0 0x5573427aaf6d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:99:3
    #1 0x55735026fd12 in cricket::SctpTransport::UsrSctpWrapper::InitializeUsrSctp() ./../../third_party/webrtc/media/sctp/sctp_transport.cc:301:24
    #2 0x557350268253 in IncrementUsrSctpUsageCount ./../../third_party/webrtc/media/sctp/sctp_transport.cc:323:7
    #3 0x557350268253 in cricket::SctpTransport::OpenSctpSocket() ./../../third_party/webrtc/media/sctp/sctp_transport.cc:823:3
    #4 0x557350263dfe in cricket::SctpTransport::Connect() ./../../third_party/webrtc/media/sctp/sctp_transport.cc:768:8
    #5 0x5573505549b9 in emit<rtc::PacketTransportInternal *> ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:327:5
    #6 0x5573505549b9 in emit ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:560:12
    #7 0x5573505549b9 in operator() ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:564:35
    #8 0x5573505549b9 in cricket::DtlsTransport::set_writable(bool) ./../../third_party/webrtc/p2p/base/dtls_transport.cc:799:3
    #9 0x557350556780 in cricket::DtlsTransport::OnDtlsEvent(rtc::StreamInterface*, int, int) ./../../third_party/webrtc/p2p/base/dtls_transport.cc:666:7
    #10 0x5573503be1f2 in emit<rtc::StreamInterface *, int, int> ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:327:5
    #11 0x5573503be1f2 in emit ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:560:12
    #12 0x5573503be1f2 in operator() ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:564:35
    #13 0x5573503be1f2 in rtc::StreamAdapterInterface::OnEvent(rtc::StreamInterface*, int, int) ./../../third_party/webrtc/rtc_base/stream.cc:131:3
    #14 0x5573503c3603 in rtc::OpenSSLStreamAdapter::ContinueSSL() ./../../third_party/webrtc/rtc_base/openssl_stream_adapter.cc:862:33
    #15 0x5573503c2dd7 in rtc::OpenSSLStreamAdapter::OnEvent(rtc::StreamInterface*, int, int) ./../../third_party/webrtc/rtc_base/openssl_stream_adapter.cc:757:21
    #16 0x557350550893 in emit<rtc::StreamInterface *, int, int> ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:327:5
    #17 0x557350550893 in emit ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:560:12
    #18 0x557350550893 in operator() ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:564:35
    #19 0x557350550893 in cricket::StreamInterfaceChannel::OnPacketReceived(char const*, unsigned long) ./../../third_party/webrtc/p2p/base/dtls_transport.cc:116:3
    #20 0x55735055a418 in HandleDtlsPacket ./../../third_party/webrtc/p2p/base/dtls_transport.cc:775:21
    #21 0x55735055a418 in cricket::DtlsTransport::OnReadPacket(rtc::PacketTransportInternal*, char const*, unsigned long, long const&, int) ./../../third_party/webrtc/p2p/base/dtls_transport.cc:609:14
    #22 0x55735021c1c9 in emit<rtc::PacketTransportInternal *, const char *, unsigned long, const long &, int> ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:327:5
    #23 0x55735021c1c9 in emit ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:560:12
    #24 0x55735021c1c9 in operator() ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:564:35
    #25 0x55735021c1c9 in cricket::P2PTransportChannel::OnReadPacket(cricket::Connection*, char const*, unsigned long, long) ./../../third_party/webrtc/p2p/base/p2p_transport_channel.cc:2113:5
    #26 0x55734fa955ba in emit<cricket::Connection *, const char *, unsigned long, long> ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:327:5
    #27 0x55734fa955ba in emit ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:560:12
    #28 0x55734fa955ba in operator() ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:564:35
    #29 0x55734fa955ba in cricket::Connection::OnReadPacket(char const*, unsigned long, long) ./../../third_party/webrtc/p2p/base/connection.cc:464:5
    #30 0x55734fb0b8d5 in cricket::UDPPort::HandleIncomingPacket(rtc::AsyncPacketSocket*, char const*, unsigned long, rtc::SocketAddress const&, long) ./../../third_party/webrtc/p2p/base/stun_port.cc:348:3
    #31 0x55735bfe9bea in emit<rtc::AsyncPacketSocket *, const char *, unsigned long, const rtc::SocketAddress &, const long &> ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:327:5
    #32 0x55735bfe9bea in emit ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:560:12
    #33 0x55735bfe9bea in operator() ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:564:35
    #34 0x55735bfe9bea in blink::(anonymous namespace)::IpcPacketSocket::OnDataReceived(net::IPEndPoint const&, WTF::Vector<signed char, 0u, WTF::PartitionAllocator> const&, base::TimeTicks const&) ./../../third_party/blink/renderer/platform/p2p/ipc_socket_factory.cc:644:3
    #35 0x55735bfee148 in DataReceived ./../../third_party/blink/renderer/platform/p2p/socket_client_impl.cc:164:16
    #36 0x55735bfee148 in non-virtual thunk to blink::P2PSocketClientImpl::DataReceived(net::IPEndPoint const&, WTF::Vector<signed char, 0u, WTF::PartitionAllocator> const&, base::TimeTicks) ./../../third_party/blink/renderer/platform/p2p/socket_client_impl.cc:0:0
    #37 0x557348ba41d2 in network::mojom::blink::P2PSocketClientStubDispatch::Accept(network::mojom::blink::P2PSocketClient*, mojo::Message*) ./gen/services/network/public/mojom/p2p.mojom-blink.cc:1330:13
    #38 0x55734d856811 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:554:54
    #39 0x55734d8633b2 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:41:19
    #40 0x55734d86ee3e in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:953:42
    #41 0x55734d86d6a3 in mojo::internal::MultiplexRouter::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:620:38
    #42 0x55734d8633b2 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:41:19
    #43 0x55734d84fc08 in mojo::Connector::DispatchMessage(mojo::Message) ./../../mojo/public/cpp/bindings/lib/connector.cc:509:49
    #44 0x55734d851577 in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:567:14
    #45 0x55734d392363 in Run ./../../base/callback.h:99:12
    #46 0x55734d392363 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:142:33
    #47 0x55734d3ccf69 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:332:23
    #48 0x55734d3cc878 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:252:36
    #49 0x55734d2c6c00 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39:55
    #50 0x55734d3ce1e9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:451:12
    #51 0x55734d340de6 in base::RunLoop::Run() ./../../base/run_loop.cc:124:14

Thread T51 (SCTP timer) created by T20 (WebRTC_Network) here:
    #0 0x55734276cb6a in pthread_create /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:214:3
    #1 0x55735035a737 in sctp_start_timer ./../../third_party/usrsctp/usrsctplib/usrsctplib/netinet/sctp_callout.c:223:7
    #2 0x557350272ab3 in usrsctp_init ./../../third_party/usrsctp/usrsctplib/usrsctplib/user_socket.c:112:2
    #3 0x55735026fc57 in cricket::SctpTransport::UsrSctpWrapper::InitializeUsrSctp() ./../../third_party/webrtc/media/sctp/sctp_transport.cc:263:5
    #4 0x557350268253 in IncrementUsrSctpUsageCount ./../../third_party/webrtc/media/sctp/sctp_transport.cc:323:7
    #5 0x557350268253 in cricket::SctpTransport::OpenSctpSocket() ./../../third_party/webrtc/media/sctp/sctp_transport.cc:823:3
    #6 0x557350263dfe in cricket::SctpTransport::Connect() ./../../third_party/webrtc/media/sctp/sctp_transport.cc:768:8
    #7 0x5573505549b9 in emit<rtc::PacketTransportInternal *> ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:327:5
    #8 0x5573505549b9 in emit ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:560:12
    #9 0x5573505549b9 in operator() ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:564:35
    #10 0x5573505549b9 in cricket::DtlsTransport::set_writable(bool) ./../../third_party/webrtc/p2p/base/dtls_transport.cc:799:3
    #11 0x557350556780 in cricket::DtlsTransport::OnDtlsEvent(rtc::StreamInterface*, int, int) ./../../third_party/webrtc/p2p/base/dtls_transport.cc:666:7
    #12 0x5573503be1f2 in emit<rtc::StreamInterface *, int, int> ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:327:5
    #13 0x5573503be1f2 in emit ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:560:12
    #14 0x5573503be1f2 in operator() ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:564:35
    #15 0x5573503be1f2 in rtc::StreamAdapterInterface::OnEvent(rtc::StreamInterface*, int, int) ./../../third_party/webrtc/rtc_base/stream.cc:131:3
    #16 0x5573503c3603 in rtc::OpenSSLStreamAdapter::ContinueSSL() ./../../third_party/webrtc/rtc_base/openssl_stream_adapter.cc:862:33
    #17 0x5573503c2dd7 in rtc::OpenSSLStreamAdapter::OnEvent(rtc::StreamInterface*, int, int) ./../../third_party/webrtc/rtc_base/openssl_stream_adapter.cc:757:21
    #18 0x557350550893 in emit<rtc::StreamInterface *, int, int> ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:327:5
    #19 0x557350550893 in emit ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:560:12
    #20 0x557350550893 in operator() ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:564:35
    #21 0x557350550893 in cricket::StreamInterfaceChannel::OnPacketReceived(char const*, unsigned long) ./../../third_party/webrtc/p2p/base/dtls_transport.cc:116:3
    #22 0x55735055a418 in HandleDtlsPacket ./../../third_party/webrtc/p2p/base/dtls_transport.cc:775:21
    #23 0x55735055a418 in cricket::DtlsTransport::OnReadPacket(rtc::PacketTransportInternal*, char const*, unsigned long, long const&, int) ./../../third_party/webrtc/p2p/base/dtls_transport.cc:609:14
    #24 0x55735021c1c9 in emit<rtc::PacketTransportInternal *, const char *, unsigned long, const long &, int> ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:327:5
    #25 0x55735021c1c9 in emit ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:560:12
    #26 0x55735021c1c9 in operator() ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:564:35
    #27 0x55735021c1c9 in cricket::P2PTransportChannel::OnReadPacket(cricket::Connection*, char const*, unsigned long, long) ./../../third_party/webrtc/p2p/base/p2p_transport_channel.cc:2113:5
    #28 0x55734fa955ba in emit<cricket::Connection *, const char *, unsigned long, long> ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:327:5
    #29 0x55734fa955ba in emit ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:560:12
    #30 0x55734fa955ba in operator() ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:564:35
    #31 0x55734fa955ba in cricket::Connection::OnReadPacket(char const*, unsigned long, long) ./../../third_party/webrtc/p2p/base/connection.cc:464:5
    #32 0x55734fb0b8d5 in cricket::UDPPort::HandleIncomingPacket(rtc::AsyncPacketSocket*, char const*, unsigned long, rtc::SocketAddress const&, long) ./../../third_party/webrtc/p2p/base/stun_port.cc:348:3
    #33 0x55735bfe9bea in emit<rtc::AsyncPacketSocket *, const char *, unsigned long, const rtc::SocketAddress &, const long &> ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:327:5
    #34 0x55735bfe9bea in emit ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:560:12
    #35 0x55735bfe9bea in operator() ./../../third_party/webrtc/rtc_base/third_party/sigslot/sigslot.h:564:35
    #36 0x55735bfe9bea in blink::(anonymous namespace)::IpcPacketSocket::OnDataReceived(net::IPEndPoint const&, WTF::Vector<signed char, 0u, WTF::PartitionAllocator> const&, base::TimeTicks const&) ./../../third_party/blink/renderer/platform/p2p/ipc_socket_factory.cc:644:3
    #37 0x55735bfee148 in DataReceived ./../../third_party/blink/renderer/platform/p2p/socket_client_impl.cc:164:16
    #38 0x55735bfee148 in non-virtual thunk to blink::P2PSocketClientImpl::DataReceived(net::IPEndPoint const&, WTF::Vector<signed char, 0u, WTF::PartitionAllocator> const&, base::TimeTicks) ./../../third_party/blink/renderer/platform/p2p/socket_client_impl.cc:0:0
    #39 0x557348ba41d2 in network::mojom::blink::P2PSocketClientStubDispatch::Accept(network::mojom::blink::P2PSocketClient*, mojo::Message*) ./gen/services/network/public/mojom/p2p.mojom-blink.cc:1330:13
    #40 0x55734d856811 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:554:54
    #41 0x55734d8633b2 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:41:19
    #42 0x55734d86ee3e in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:953:42
    #43 0x55734d86d6a3 in mojo::internal::MultiplexRouter::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:620:38
    #44 0x55734d8633b2 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:41:19
    #45 0x55734d84fc08 in mojo::Connector::DispatchMessage(mojo::Message) ./../../mojo/public/cpp/bindings/lib/connector.cc:509:49
    #46 0x55734d851577 in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:567:14
    #47 0x55734d392363 in Run ./../../base/callback.h:99:12
    #48 0x55734d392363 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:142:33
    #49 0x55734d3ccf69 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:332:23
    #50 0x55734d3cc878 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:252:36
    #51 0x55734d2c6c00 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39:55
    #52 0x55734d3ce1e9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:451:12
    #53 0x55734d340de6 in base::RunLoop::Run() ./../../base/run_loop.cc:124:14
    #54 0x55734d425437 in base::Thread::ThreadMain() ./../../base/threading/thread.cc:380:3
    #55 0x55734d4a595d in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:81:13
    #56 0x7febd5e646da in start_thread /build/glibc-OTsEL5/glibc-2.27/nptl/pthread_create.c:463:0

Thread T20 (WebRTC_Network) created by T0 (chrome) here:
    #0 0x55734276cb6a in pthread_create /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:214:3
    #1 0x55734d4a4b7a in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, base::PlatformThreadHandle*, base::ThreadPriority) ./../../base/threading/platform_thread_posix.cc:120:13
    #2 0x55734d424316 in base::Thread::StartWithOptions(base::Thread::Options const&) ./../../base/threading/thread.cc:186:15
    #3 0x55734d423cb7 in base::Thread::Start() ./../../base/threading/thread.cc:139:10
    #4 0x55735bfbad21 in blink::PeerConnectionDependencyFactory::CreatePeerConnectionFactory() ./../../third_party/blink/renderer/modules/peerconnection/peer_connection_dependency_factory.cc:201:3
    #5 0x55735bfba8b9 in blink::PeerConnectionDependencyFactory::GetPcFactory() ./../../third_party/blink/renderer/modules/peerconnection/peer_connection_dependency_factory.cc:155:5
    #6 0x55735bfbe422 in blink::PeerConnectionDependencyFactory::CreatePeerConnection(webrtc::PeerConnectionInterface::RTCConfiguration const&, blink::WebLocalFrame*, webrtc::PeerConnectionObserver*) ./../../third_party/blink/renderer/modules/peerconnection/peer_connection_dependency_factory.cc:352:8
    #7 0x55735bff5c62 in blink::RTCPeerConnectionHandler::Initialize(webrtc::PeerConnectionInterface::RTCConfiguration const&, blink::MediaConstraints const&, blink::WebLocalFrame*) ./../../third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc:1148:50
    #8 0x55735e355f35 in blink::RTCPeerConnection::RTCPeerConnection(blink::ExecutionContext*, webrtc::PeerConnectionInterface::RTCConfiguration, bool, bool, bool, blink::MediaConstraints, blink::ExceptionState&) ./../../third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc:800:23
    #9 0x55735e34f1b4 in Call<blink::ExecutionContext *&, webrtc::PeerConnectionInterface::RTCConfiguration, bool, bool, bool, blink::MediaConstraints &, blink::ExceptionState &> ./../../third_party/blink/renderer/platform/heap/heap.h:532:32
    #10 0x55735e34f1b4 in MakeGarbageCollected<blink::RTCPeerConnection, blink::ExecutionContext *&, webrtc::PeerConnectionInterface::RTCConfiguration, bool, bool, bool, blink::MediaConstraints &, blink::ExceptionState &> ./../../third_party/blink/renderer/platform/heap/heap.h:572:15
    #11 0x55735e34f1b4 in blink::RTCPeerConnection::Create(blink::ExecutionContext*, blink::RTCConfiguration const*, blink::Dictionary const&, blink::ExceptionState&) ./../../third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc:695:40
    #12 0x55735e35530d in blink::RTCPeerConnection::Create(blink::ExecutionContext*, blink::RTCConfiguration const*, blink::ExceptionState&) ./../../third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc:733:10
    #13 0x55735e49dba2 in Constructor ./gen/third_party/blink/renderer/bindings/modules/v8/v8_rtc_peer_connection.cc:1547:31
    #14 0x55735e49dba2 in blink::rtc_peer_connection_v8_internal::ConstructorCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/modules/v8/v8_rtc_peer_connection.cc:1584:3
    #15 0x55734920113f in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:158:3
    #16 0x5573491fdda5 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<true>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:111:36
    #17 0x5573491fc6b8 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:137:5
    #18 0x55734b227717 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit ??:0:0
    #19 0x55734b1b8bc4 in Builtins_JSBuiltinsConstructStub ??:0:0
    #20 0x55734b2b02e8 in Builtins_ConstructHandler ??:0:0
    #21 0x55734b1bccb4 in Builtins_InterpreterEntryTrampoline ??:0:0
    #22 0x55734b1bccb4 in Builtins_InterpreterEntryTrampoline ??:0:0
    #23 0x55734b1b417e in Builtins_ArgumentsAdaptorTrampoline ??:0:0
    #24 0x55734b1bccb4 in Builtins_InterpreterEntryTrampoline ??:0:0
    #25 0x55734b1b417e in Builtins_ArgumentsAdaptorTrampoline ??:0:0
    #26 0x55734b26f26a in Builtins_PromiseConstructor ??:0:0
    #27 0x55734b1b8bef in Builtins_JSBuiltinsConstructStub ??:0:0
    #28 0x55734b2b02e8 in Builtins_ConstructHandler ??:0:0
    #29 0x55734b1bccb4 in Builtins_InterpreterEntryTrampoline ??:0:0
    #30 0x55734b1b417e in Builtins_ArgumentsAdaptorTrampoline ??:0:0
    #31 0x55734b270d57 in Builtins_PromiseFulfillReactionJob ??:0:0
    #32 0x55734b1dcd83 in Builtins_RunMicrotasks ??:0:0
    #33 0x55734b1ba757 in Builtins_JSRunMicrotasksEntry ??:0:0
    #34 0x557349497536 in Call ./../../v8/src/execution/simulator.h:142:12
    #35 0x557349497536 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:382:33
    #36 0x55734949aede in v8::internal::(anonymous namespace)::InvokeWithTryCatch(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:427:20
    #37 0x55734949b379 in v8::internal::Execution::TryRunMicrotasks(v8::internal::Isolate*, v8::internal::MicrotaskQueue*, v8::internal::MaybeHandle<v8::internal::Object>*) ./../../v8/src/execution/execution.cc:504:10
    #38 0x557349515a35 in v8::internal::MicrotaskQueue::RunMicrotasks(v8::internal::Isolate*) ./../../v8/src/execution/microtask-queue.cc:165:22
    #39 0x5573495153d6 in v8::internal::MicrotaskQueue::PerformCheckpoint(v8::Isolate*) ./../../v8/src/execution/microtask-queue.cc:117:5
    #40 0x557357a94091 in blink::V8ScriptRunner::RunCompiledScript(v8::Isolate*, v8::Local<v8::Script>, blink::ExecutionContext*) ./../../third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:359:3
    #41 0x5573590f67a1 in blink::ScriptController::ExecuteScriptAndReturnValue(v8::Local<v8::Context>, blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&) ./../../third_party/blink/renderer/bindings/core/v8/script_controller.cc:134:20
    #42 0x5573590f95e7 in blink::ScriptController::EvaluateScriptInMainWorld(blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&, blink::ScriptController::ExecuteScriptPolicy) ./../../third_party/blink/renderer/bindings/core/v8/script_controller.cc:363:33
    #43 0x5573590fa02e in blink::ScriptController::ExecuteScriptInMainWorld(blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&) ./../../third_party/blink/renderer/bindings/core/v8/script_controller.cc:328:3
    #44 0x55735b3c1a24 in blink::PendingScript::ExecuteScriptBlockInternal(blink::Script*, blink::ScriptElementBase*, bool, bool, bool, base::TimeTicks, bool) ./../../third_party/blink/renderer/core/script/pending_script.cc:264:13
    #45 0x55735b3c1314 in blink::PendingScript::ExecuteScriptBlock(blink::KURL const&) ./../../third_party/blink/renderer/core/script/pending_script.cc:170:3
    #46 0x55735b3c75ad in blink::ScriptLoader::PrepareScript(WTF::TextPosition const&, blink::ScriptLoader::LegacyTypeSupport) ./../../third_party/blink/renderer/core/script/script_loader.cc:919:9
    #47 0x55735b373575 in blink::HTMLParserScriptRunner::ProcessScriptElementInternal(blink::Element*, WTF::TextPosition const&) ./../../third_party/blink/renderer/core/script/html_parser_script_runner.cc:610:20
    #48 0x55735b373118 in blink::HTMLParserScriptRunner::ProcessScriptElement(blink::Element*, WTF::TextPosition const&) ./../../third_party/blink/renderer/core/script/html_parser_script_runner.cc:333:3
    #49 0x55735a06a230 in blink::HTMLDocumentParser::RunScriptsForPausedTreeBuilder() ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:491:21
    #50 0x55735a06de3a in blink::HTMLDocumentParser::ProcessTokenizedChunkFromBackgroundParser(std::__1::unique_ptr<blink::HTMLDocumentParser::TokenizedChunk, std::__1::default_delete<blink::HTMLDocumentParser::TokenizedChunk> >, bool*) ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:732:9
    #51 0x55735a069acd in blink::HTMLDocumentParser::PumpPendingSpeculations() ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:792:34
    #52 0x55735a078fa4 in blink::HTMLDocumentParser::ResumeParsingAfterPause() ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:1318:7
    #53 0x55735a079db9 in blink::HTMLDocumentParser::NotifyScriptLoaded(blink::PendingScript*) ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:1375:5
    #54 0x55734d392363 in Run ./../../base/callback.h:99:12
    #55 0x55734d392363 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:142:33
    #56 0x55734d3ccf69 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:332:23
    #57 0x55734d3cc878 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:252:36
    #58 0x55734d2c6c00 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39:55
    #59 0x55734d3ce1e9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:451:12
    #60 0x55734d340de6 in base::RunLoop::Run() ./../../base/run_loop.cc:124:14
    #61 0x55735e82ffce in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer_main.cc:230:16
    #62 0x55734c286f21 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:863:10
    #63 0x55734c41e8f7 in service_manager::Main(service_manager::MainParams const&) ./../../services/service_manager/embedder/main.cc:454:29
    #64 0x55734c281ff6 in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:19:10
    #65 0x5573427ae144 in ChromeMain ./../../chrome/app/chrome_main.cc:118:12
    #66 0x7febce577b96 in __libc_start_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310:0

SUMMARY: AddressSanitizer: heap-use-after-free (/home/cowboy/chromium/src/out/chrome_asan_shared/chrome+0x16d9d8d3)
Shadow bytes around the buggy address:
  0x0c1680049f80: fa fa fa fa fa fa fd fd fd fd fd fd fd fd fd fd
  0x0c1680049f90: fd fd fd fa fa fa fa fa fa fa fa fa fd fd fd fd
  0x0c1680049fa0: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa
  0x0c1680049fb0: fa fa fd fd fd fd fd fd fd fd fd fd fd fd fd fa
  0x0c1680049fc0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
=>0x0c1680049fd0: fd[fd]fd fd fd fa fa fa fa fa fa fa fa fa fd fd
  0x0c1680049fe0: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa
  0x0c1680049ff0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c168004a000: fd fa fa fa fa fa fa fa fa fa fd fd fd fd fd fd
  0x0c168004a010: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x0c168004a020: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa
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
==43979==ABORTING
Received signal 6
    #0 0x5573427405fb in backtrace /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4103:13
    #1 0x55734d46f984 in base::debug::CollectStackTrace(void**, unsigned long) ./../../base/debug/stack_trace_posix.cc:840:39
    #2 0x55734d278622 in StackTrace ./../../base/debug/stack_trace.cc:206:12
    #3 0x55734d278622 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:203:28
    #4 0x55734d46e54e in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) ./../../base/debug/stack_trace_posix.cc:345:3
    #5 0x7febd5e6f890 in __funlockfile ??:?
    #6 0x7febd5e6f890 in ?? ??:0
    #7 0x7febce594e97 in __libc_signal_restore_set /build/glibc-OTsEL5/glibc-2.27/signal/../sysdeps/unix/sysv/linux/nptl-signals.h:80:0
    #8 0x7febce594e97 in raise /build/glibc-OTsEL5/glibc-2.27/signal/../sysdeps/unix/sysv/linux/raise.c:48:0
    #9 0x7febce596801 in abort /build/glibc-OTsEL5/glibc-2.27/stdlib/abort.c:79:0
    #10 0x55734279aa27 in __sanitizer::Abort() /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/sanitizer_common/sanitizer_posix_libcdep.cpp:155:3
    #11 0x5573427997a1 in __sanitizer::Die() /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/sanitizer_common/sanitizer_termination.cpp:58:5
    #12 0x557342785ac4 in __asan::ScopedInErrorReport::~ScopedInErrorReport() /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_report.cpp:189:7
    #13 0x5573427874ae in __asan::ReportGenericError(unsigned long, unsigned long, unsigned long, unsigned long, bool, unsigned long, unsigned int, bool) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_report.cpp:477:1
    #14 0x557342787d68 in __asan_report_load8 /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_rtl.cpp:120:1
    #15 0x5573502708d4 in size ./../../buildtools/third_party/libc++/trunk/include/__hash_table:799:55
    #16 0x5573502708d4 in bucket_count ./../../buildtools/third_party/libc++/trunk/include/__hash_table:1204:45
    #17 0x5573502708d4 in find<unsigned long> ./../../buildtools/third_party/libc++/trunk/include/__hash_table:2488:22
    #18 0x5573502708d4 in find ./../../buildtools/third_party/libc++/trunk/include/unordered_map:1280:69
    #19 0x5573502708d4 in Retrieve ./../../third_party/webrtc/media/sctp/sctp_transport.cc:112:20
    #20 0x5573502708d4 in cricket::SctpTransport::UsrSctpWrapper::OnSctpOutboundPacket(void*, void*, unsigned long, unsigned char, unsigned char) ./../../third_party/webrtc/media/sctp/sctp_transport.cc:344:27
    #21 0x5573502bce9f in sctp_lowlevel_chunk_output ./../../third_party/usrsctp/usrsctplib/usrsctplib/netinet/sctp_output.c:5043:10
    #22 0x5573502e2029 in sctp_send_abort_tcb ./../../third_party/usrsctp/usrsctplib/usrsctplib/netinet/sctp_output.c:11570:15
    #23 0x557350289018 in sctp_inpcb_free ./../../third_party/usrsctp/usrsctplib/usrsctplib/netinet/sctp_pcb.c:4120:4
    #24 0x557350369b45 in sctp_close ./../../third_party/usrsctp/usrsctplib/usrsctplib/netinet/sctp_usrreq.c:0:0
    #25 0x5573502730aa in sofree ./../../third_party/usrsctp/usrsctplib/usrsctplib/user_socket.c:298:2
    #26 0x55735029ddfa in sctp_timeout_handler ./../../third_party/usrsctp/usrsctplib/usrsctplib/netinet/sctputil.c:2086:3
    #27 0x55735035a36c in sctp_handle_tick ./../../third_party/usrsctp/usrsctplib/usrsctplib/netinet/sctp_callout.c:167:4
    #28 0x55735035a575 in user_sctp_timer_iterate ./../../third_party/usrsctp/usrsctplib/usrsctplib/netinet/sctp_callout.c:209:3
    #29 0x7febd5e646db in start_thread /build/glibc-OTsEL5/glibc-2.27/nptl/pthread_create.c:463:0
    #30 0x7febce67788f in clone /build/glibc-OTsEL5/glibc-2.27/misc/../sysdeps/unix/sysv/linux/x86_64/clone.S:95:0
  r8: 0000000000000000  r9: 00007feb9b7d9630 r10: 0000000000000008 r11: 0000000000000246
 r12: 00007feb9b7da5e8 r13: 00007feb9b7da5f0 r14: 00007feb9b7da590 r15: 0000557361929148
  di: 0000000000000002  si: 00007feb9b7d9630  bp: 00007feb9b7da5c0  bx: 0000557361896cd8
  dx: 0000000000000000  ax: 0000000000000000  cx: 00007febce594e97  sp: 00007feb9b7d9630
  ip: 00007febce594e97 efl: 0000000000000246 cgf: 002b000000000033 erf: 0000000000000000
 trp: 0000000000000000 msk: 0000000000000000 cr2: 0000000000000000
[end of stack trace]
Calling _exit(1). Core file will not be generated.

Did this work before? N/A 

Chrome version: Chromium 86.0.4196.0   Channel: n/a
OS Version: 18.04
Flash Version:

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 1.7 KB)

## Timeline

### cl...@chromium.org (2020-07-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5688819204030464.

### mm...@chromium.org (2020-07-10)

I've reproduced it locally on Linux after a few attempts using a Stable build: https://storage.googleapis.com/chromium-browser-asan/linux-release/asan-linux-release-756066.zip


mmoroz@mmoroz3:~/Downloads/asan-linux-release-756066$ ./chrome --user-data-dir=profile http://127.0.0.1:8000/crash.html
[323479:323479:0710/134128.321750:ERROR:edid_parser.cc(102)] Too short EDID data: manufacturer id
[323511:323511:0710/134128.601507:ERROR:sandbox_linux.cc(374)] InitializeSandbox() called with multiple threads in process gpu-process.
=================================================================
==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x6160001e9b64 at pc 0x555bf2ec904c bp 0x7fe482b17e40 sp 0x7fe482b17e38
WRITE of size 4 at 0x6160001e9b64 thread T16 (WebRTC_Worker)
==1==WARNING: invalid path to external symbolizer!
==1==WARNING: Failed to use and restart external symbolizer!
    #0 0x555bf2ec904b  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x169ef04b)
    #1 0x555bf2dd3e0d  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x168f9e0d)
    #2 0x555bf2dc5ed6  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x168ebed6)
    #3 0x555bf2dc61bd  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x168ec1bd)
    #4 0x555bf3119f6f  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x16c3ff6f)
    #5 0x555bf30be680  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x16be4680)
    #6 0x555bf30bf51d  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x16be551d)
    #7 0x555bf308ed39  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x16bb4d39)
    #8 0x555bf306d1ab  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x16b931ab)
    #9 0x555bee1f5fbb  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x11d1bfbb)
    #10 0x555bee1f6cd8  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x11d1ccd8)
    #11 0x555beff916c2  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13ab76c2)
    #12 0x555beffc9a28  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13aefa28)
    #13 0x555beffc9347  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13aef347)
    #14 0x555befeca8f0  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x139f08f0)
    #15 0x555beffcac78  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13af0c78)
    #16 0x555beff429ba  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13a689ba)
    #17 0x555bf001cf8b  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13b42f8b)
    #18 0x555bf00fa041  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13c20041)
    #19 0x7fe49e3aef26  (/lib/x86_64-linux-gnu/libpthread.so.0+0x8f26)

0x6160001e9b64 is located 484 bytes inside of 584-byte region [0x6160001e9980,0x6160001e9bc8)
freed by thread T2516 (SCTP timer) here:
    #0 0x555be583aead  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x9360ead)
    #1 0x555bf2dfe57a  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x1692457a)
    #2 0x555bf2eb9e1b  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x169dfe1b)
    #3 0x555bf2eba014  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x169e0014)
    #4 0x7fe49e3aef26  (/lib/x86_64-linux-gnu/libpthread.so.0+0x8f26)

previously allocated by thread T16 (WebRTC_Worker) here:
    #0 0x555be583b12d  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x936112d)
    #1 0x555bf2dd5403  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x168fb403)
    #2 0x555bf2dd6a8e  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x168fca8e)
    #3 0x555bf2dd6e0c  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x168fce0c)
    #4 0x555bf2dcb399  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x168f1399)
    #5 0x555bf2dc6daf  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x168ecdaf)
    #6 0x555bf30afb49  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x16bd5b49)
    #7 0x555bf30b1824  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x16bd7824)
    #8 0x555bf2f1cb52  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x16a42b52)
    #9 0x555bf2f21d77  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x16a47d77)
    #10 0x555bf2f21635  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x16a47635)
    #11 0x555bf30abbd7  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x16bd1bd7)
    #12 0x555bf30b53aa  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x16bdb3aa)
    #13 0x555bf2d80f0d  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x168a6f0d)
    #14 0x555bf261f68a  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x1614568a)
    #15 0x555bf2691ad4  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x161b7ad4)
    #16 0x555bfe85a148  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x22380148)
    #17 0x555bfe85e5f3  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x223845f3)
    #18 0x555beb852348  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0xf378348)
    #19 0x555bf0434160  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13f5a160)
    #20 0x555bf04407e6  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13f667e6)
    #21 0x555bf044c02c  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13f7202c)
    #22 0x555bf044a79a  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13f7079a)
    #23 0x555bf04407e6  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13f667e6)
    #24 0x555bf0429e96  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13f4fe96)
    #25 0x555bf042c05d  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13f5205d)
    #26 0x555bf04958cf  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13fbb8cf)
    #27 0x555beff916c2  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13ab76c2)
    #28 0x555beffc9a28  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13aefa28)
    #29 0x555beffc9347  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13aef347)

Thread T16 (WebRTC_Worker) created by T0 (chrome) here:
    #0 0x555be5825fda  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x934bfda)
    #1 0x555bf00f920e  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13c1f20e)
    #2 0x555bf001c0a4  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13b420a4)
    #3 0x555bf001ba4b  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13b41a4b)
    #4 0x555bfe82b5a1  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x223515a1)
    #5 0x555bfe82afd0  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x22350fd0)
    #6 0x555bfe82f269  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x22355269)
    #7 0x555bfe8660ff  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x2238c0ff)
    #8 0x555c00b836bf  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x246a96bf)
    #9 0x555c00b7cb71  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x246a2b71)
    #10 0x555c00b82b38  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x246a8b38)
    #11 0x555c00c3e07b  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x2476407b)
    #12 0x555bebe99af0  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0xf9bfaf0)
    #13 0x555bebe96a16  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0xf9bca16)
    #14 0x555bebe9549d  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0xf9bb49d)
    #15 0x555bede9ee77  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x119c4e77)
    #16 0x555bede2eae4  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x11954ae4)
    #17 0x555bedf2113e  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x11a4713e)
    #18 0x555bede32bb4  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x11958bb4)
    #19 0x555bede306f9  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x119566f9)
    #20 0x555bede304d7  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x119564d7)
    #21 0x555bec12fa67  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0xfc55a67)
    #22 0x555bec12e990  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0xfc54990)
    #23 0x555bebd3e12d  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0xf86412d)
    #24 0x555bfa505559  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x1e02b559)
    #25 0x555bfbb05622  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x1f62b622)
    #26 0x555bfbb0812b  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x1f62e12b)
    #27 0x555bfbb08b42  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x1f62eb42)
    #28 0x555bfddfbfed  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x21921fed)
    #29 0x555bfddfba99  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x21921a99)
    #30 0x555bfde00acf  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x21926acf)
    #31 0x555bfddaf3ab  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x218d53ab)
    #32 0x555bfddaef2b  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x218d4f2b)
    #33 0x555bfca6ca6a  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x20592a6a)
    #34 0x555bfca6898d  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x2058e98d)
    #35 0x555bee157511  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x11c7d511)
    #36 0x555beff916c2  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13ab76c2)
    #37 0x555beffc9a28  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13aefa28)
    #38 0x555beffc9347  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13aef347)
    #39 0x555befeca8f0  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x139f08f0)
    #40 0x555beffcac78  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13af0c78)
    #41 0x555beff429ba  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13a689ba)
    #42 0x555c00fc63e6  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x24aec3e6)
    #43 0x555beeeb208f  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x129d808f)
    #44 0x555beeeb557c  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x129db57c)
    #45 0x555bef046179  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x12b6c179)
    #46 0x555beeeb04df  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x129d64df)
    #47 0x555be5867123  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x938d123)
    #48 0x7fe49cc7ee0a  (/lib/x86_64-linux-gnu/libc.so.6+0x26e0a)

Thread T2516 (SCTP timer) created by T16 (WebRTC_Worker) here:
    #0 0x555be5825fda  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x934bfda)
    #1 0x555bf2eba1cb  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x169e01cb)
    #2 0x555bf2dd3867  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x168f9867)
    #3 0x555bf2dd261e  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x168f861e)
    #4 0x555bf2dcb348  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x168f1348)
    #5 0x555bf2dc6daf  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x168ecdaf)
    #6 0x555bf30afb49  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x16bd5b49)
    #7 0x555bf30b1824  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x16bd7824)
    #8 0x555bf2f1cb52  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x16a42b52)
    #9 0x555bf2f21d77  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x16a47d77)
    #10 0x555bf2f21635  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x16a47635)
    #11 0x555bf30abbd7  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x16bd1bd7)
    #12 0x555bf30b53aa  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x16bdb3aa)
    #13 0x555bf2d80f0d  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x168a6f0d)
    #14 0x555bf261f68a  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x1614568a)
    #15 0x555bf2691ad4  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x161b7ad4)
    #16 0x555bfe85a148  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x22380148)
    #17 0x555bfe85e5f3  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x223845f3)
    #18 0x555beb852348  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0xf378348)
    #19 0x555bf0434160  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13f5a160)
    #20 0x555bf04407e6  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13f667e6)
    #21 0x555bf044c02c  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13f7202c)
    #22 0x555bf044a79a  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13f7079a)
    #23 0x555bf04407e6  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13f667e6)
    #24 0x555bf0429e96  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13f4fe96)
    #25 0x555bf042c05d  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13f5205d)
    #26 0x555bf04958cf  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13fbb8cf)
    #27 0x555beff916c2  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13ab76c2)
    #28 0x555beffc9a28  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13aefa28)
    #29 0x555beffc9347  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13aef347)
    #30 0x555befeca8f0  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x139f08f0)
    #31 0x555beffcac78  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13af0c78)
    #32 0x555beff429ba  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13a689ba)
    #33 0x555bf001cf8b  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13b42f8b)
    #34 0x555bf00fa041  (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x13c20041)
    #35 0x7fe49e3aef26  (/lib/x86_64-linux-gnu/libpthread.so.0+0x8f26)

SUMMARY: AddressSanitizer: heap-use-after-free (/usr/local/google/home/mmoroz/Downloads/asan-linux-release-756066/chrome+0x169ef04b) 
Shadow bytes around the buggy address:
  0x0c2c80035310: fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa fa
  0x0c2c80035320: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2c80035330: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2c80035340: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2c80035350: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x0c2c80035360: fd fd fd fd fd fd fd fd fd fd fd fd[fd]fd fd fd
  0x0c2c80035370: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa
  0x0c2c80035380: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2c80035390: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2c800353a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2c800353b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==1==ABORTING


### mm...@chromium.org (2020-07-10)

[Empty comment from Monorail migration]

[Monorail components: Blink>WebRTC]

### de...@chromium.org (2020-07-10)

Fix here: https://webrtc-review.googlesource.com/c/src/+/179161

Note that this is an existing issue: https://github.com/sctplab/usrsctp/issues/405

Except the previous issue would require two SctpTransports, and this only requires one which is far more common...

### de...@chromium.org (2020-07-11)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-07-11)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-11)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2020-07-13)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-13)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src.git/+/c7c412a36cbea0812122985872d1fcb34f688f80

commit c7c412a36cbea0812122985872d1fcb34f688f80
Author: Taylor Brandstetter <deadbeef@webrtc.org>
Date: Mon Jul 13 19:46:30 2020

Check for null before accessing SctpTransport map.

Bug: chromium:1104061
Change-Id: I52d44ff1603341777a873e747c625665bc11bfa5
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/179161
Commit-Queue: Taylor <deadbeef@webrtc.org>
Reviewed-by: Harald Alvestrand <hta@webrtc.org>
Cr-Commit-Position: refs/heads/master@{#31720}

[modify] https://crrev.com/c7c412a36cbea0812122985872d1fcb34f688f80/media/sctp/sctp_transport.cc


### de...@chromium.org (2020-07-15)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-07-15)

deadbeef@ do you consider this fixed? If so, please mark it as Fixed and then Sheriffbot will initiate the merge processes.

### [Deleted User] (2020-07-15)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5e9d7418af40e0f7f482166fa7d85ac56b0b252e

commit 5e9d7418af40e0f7f482166fa7d85ac56b0b252e
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Jul 16 15:26:31 2020

Roll WebRTC from 8df59bc74ebb to 359283989608 (39 revisions)

https://webrtc.googlesource.com/src.git/+log/8df59bc74ebb..359283989608

2020-07-16 nisse@webrtc.org Add default values for VideoEncoderFactory::CodecInfo
2020-07-16 nisse@webrtc.org Delete obsolete TODO item
2020-07-16 mirtad@webrtc.org Do not use internal source in video send stream tests.
2020-07-16 nisse@webrtc.org Fix override declarations and delete related TODOs
2020-07-16 landrey@webrtc.org Add constrained high profile level for h264 codec to media_constants
2020-07-16 chromium-webrtc-autoroll@webrtc-ci.iam.gserviceaccount.com Roll chromium_revision 4b7890cdbe..f831fc29d7 (788759:788907)
2020-07-15 handellm@webrtc.org Remove rtc::GlobalLock.
2020-07-15 chromium-webrtc-autoroll@webrtc-ci.iam.gserviceaccount.com Roll chromium_revision bc87af3aed..4b7890cdbe (788656:788759)
2020-07-15 mbonadei@webrtc.org Trigger CI bots.
2020-07-15 chromium-webrtc-autoroll@webrtc-ci.iam.gserviceaccount.com Roll chromium_revision a29ceb7864..bc87af3aed (788510:788656)
2020-07-15 handellm@webrtc.org Migrate to webrtc::GlobalMutex.
2020-07-15 danilchap@webrtc.org Add factory to create scalability structures by name
2020-07-15 mirtad@webrtc.org Do not use internal source in H.264 bitstream rewriting tests.
2020-07-15 philipp.hancke@googlemail.com sdp: parse and serialize b=TIAS
2020-07-15 nisse@webrtc.org Reland "Delete PeerConnectionInterface::BitrateParameters"
2020-07-15 nisse@webrtc.org Delete CompositeDataChannelTransport
2020-07-15 chromium-webrtc-autoroll@webrtc-ci.iam.gserviceaccount.com Roll chromium_revision 812a4946f7..a29ceb7864 (788405:788510)
2020-07-15 chromium-webrtc-autoroll@webrtc-ci.iam.gserviceaccount.com Roll chromium_revision 20d0aa1d03..812a4946f7 (788294:788405)
2020-07-14 chromium-webrtc-autoroll@webrtc-ci.iam.gserviceaccount.com Roll chromium_revision 3e578a0ddf..20d0aa1d03 (787863:788294)
2020-07-14 daniel.l@hpcnt.com Use Android Q API to test if MediaCodecInfo is HW Accelerated
2020-07-14 danilchap@webrtc.org Delete legacy cricket::RtpHeaderExtension struct as unused
2020-07-14 chromium-webrtc-autoroll@webrtc-ci.iam.gserviceaccount.com Roll chromium_revision 432e660d6d..3e578a0ddf (787714:787863)
2020-07-13 deadbeef@webrtc.org Check for null before accessing SctpTransport map.
2020-07-13 titovartem@webrtc.org Revert "Delete PeerConnectionInterface::BitrateParameters"
2020-07-13 chromium-webrtc-autoroll@webrtc-ci.iam.gserviceaccount.com Roll chromium_revision f629a87d19..432e660d6d (787611:787714)
2020-07-13 handellm@webrtc.org Migrate stray leftovers from rtc_base/ and test/ to webrtc::Mutex.
2020-07-13 handellm@webrtc.org Reland "Migrate modules/desktop_capture and modules/video_capture to webrtc::Mutex."
2020-07-13 adetaylor@chromium.org Add CPEPrefix.
2020-07-13 nisse@webrtc.org Delete PeerConnectionInterface::BitrateParameters
2020-07-13 jleconte@webrtc.org Auto roller: send trooper notifications only when Commit-Queue+2.
2020-07-13 nisse@webrtc.org Delete obsolete method JsepTransport::NegotiateDatagramTransport
2020-07-13 chromium-webrtc-autoroll@webrtc-ci.iam.gserviceaccount.com Roll chromium_revision 598b095453..f629a87d19 (787511:787611)
2020-07-11 mbonadei@webrtc.org Inclusive language in DEPS.
2020-07-11 mbonadei@webrtc.org Revert "Test luci.notifier."
2020-07-11 chromium-webrtc-autoroll@webrtc-ci.iam.gserviceaccount.com Roll chromium_revision f0f2118569..598b095453 (787142:787511)
2020-07-11 mbonadei@webrtc.org Reland "Test luci.notifier."
2020-07-11 mbonadei@webrtc.org Revert "Test luci.notifier."
2020-07-11 mbonadei@webrtc.org Add target_sdk_version to rtc_test.
2020-07-10 dminor@webrtc.org Check old_vector_size prior to copying in RTPFragmentationHeader::Resize

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/webrtc-chromium-autoroll
Please CC webrtc-chromium-sheriffs-robots@google.com on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/master/autoroll/README.md

Bug: chromium:1104061,chromium:428099,chromium:895969
Tbr: webrtc-chromium-sheriffs-robots@google.com
Change-Id: I2d17e3645667acd0f886ee85f9f4a2194529e042
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2302218
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#789054}

[modify] https://crrev.com/5e9d7418af40e0f7f482166fa7d85ac56b0b252e/DEPS


### de...@chromium.org (2020-07-20)

Was waiting for the fix to be included in a Canary build, which it now has.

Requesting merge to M85.

### [Deleted User] (2020-07-20)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
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
Owners: benmason@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2020-07-20)

OK, thank you! Can I ask why you've targeted this only at M85 not M84? Our normal practice here would be to merge it back to M84 for the next stable security refresh as well as merging to M84. Do you consider this fix risky?

### de...@chromium.org (2020-07-21)

I didn't realize that was an option; no, I don't consider it risky at all.

1. Yes, as a high severity security vulnerability. Adding chrome-security@ to confirm.
2. https://webrtc-review.googlesource.com/c/src/+/179161
3. Yes.
4. Just wasn't fixed in time.
5. No.
6. N/A

### [Deleted User] (2020-07-21)

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
Owners: govind@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-07-21)

Great.

Approving merge to M85; please merge to branch 4183 (or whatever the equivalent WebRTC branch is).

Approving merge to M84; please merge to branch 4147 (or equivalent).

Both approvals are conditional on no problems having been spotted in Canary; it looks like you've already done some diligence here per https://crbug.com/chromium/1104061#c14. Thanks!

### go...@chromium.org (2020-07-21)

Please merge your change to M84 branch 4147 ASAP so we can pick it up for next M84 Respin. Thank you.

### [Deleted User] (2020-07-21)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@chromium.org (2020-07-21)

deadbeef@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### [Deleted User] (2020-07-21)

[Empty comment from Monorail migration]

### de...@chromium.org (2020-07-21)

Merges complete.

M84: https://webrtc-review.googlesource.com/c/src/+/179900
M85: https://webrtc-review.googlesource.com/c/src/+/179901

### ad...@google.com (2020-07-27)

[Empty comment from Monorail migration]

### ad...@google.com (2020-07-27)

[Empty comment from Monorail migration]

### ad...@google.com (2020-07-27)

[Empty comment from Monorail migration]

### ad...@google.com (2020-07-27)

Reporter normally requests anonymity so RV-SE.

### ad...@google.com (2020-07-27)

[Empty comment from Monorail migration]

### aw...@google.com (2020-07-28)

Bugs from this reporter will need to be made public, even though they have asked for anonymity, and will be credited as Anonymous on release notes.

### ad...@google.com (2020-07-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-07-30)

Congratulations! The VRP panel decided to award $7,500 for this report.

### va...@chromium.org (2020-07-30)

[Empty comment from Monorail migration]

### ad...@google.com (2020-07-30)

[Empty comment from Monorail migration]

### ad...@google.com (2020-09-21)

[Empty comment from Monorail migration]

### gu...@chromium.org (2020-10-15)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1104061?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052811)*
