# Missing lifetime check in SpdyStream::IncreaseRecvWindowSize leads to use-after-free in Network Service

| Field | Value |
|-------|-------|
| **Issue ID** | [503420443](https://issues.chromium.org/issues/503420443) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals>Network>HTTP2 |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2019-9512, CVE-2019-9514, CVE-2019-9515 |
| **Reporter** | je...@gmail.com |
| **Assignee** | ba...@chromium.org |
| **Created** | 2026-04-17 |
| **Bounty** | $43,000.00 |

## Description

# Missing lifetime check in SpdyStream::IncreaseRecvWindowSize leads to use-after-free in Network Service

## Summary

A use-after-free write exists in the HTTP/2 stack of Chromium's Network Service. When a malicious HTTP/2 server sends a burst of control frames followed by a padded DATA frame, the resulting WINDOW\_UPDATE enqueue can synchronously trigger session draining, which destroys the SpdyStream object while SpdyStream::IncreaseRecvWindowSize is still on the call stack. The function then writes to a member of the freed object. This affects all desktop and mobile platforms. No special GPU or hardware requirements apply.

## Bisect

Introducing Commit: `410676ab9660a0271949e043ddb8678a6d18b097`

- Date: 2019-08-13
- Author: David Schinazi
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/1752387>

This commit added the capped-frame overflow check in EnqueueSessionWrite as a mitigation for CVE-2019-9512, CVE-2019-9514, and CVE-2019-9515. Before this commit, EnqueueSessionWrite never synchronously destroyed streams, so the missing lifetime check in IncreaseRecvWindowSize was not reachable. The mitigation introduced a new code path where DoDrainSession fires synchronously from within EnqueueSessionWrite, creating the UAF.

## Root Cause

SpdyStream::IncreaseRecvWindowSize calls session\_->SendStreamWindowUpdate and then immediately writes to a member field without verifying that the stream is still alive:

```
// net/spdy/spdy_stream.cc
void SpdyStream::IncreaseRecvWindowSize(int32_t delta_window_size) {
  // ...
  if (unacked_recv_window_bytes_ > max_recv_window_size_ / 2 ||
      elapsed >= session_->TimeToBufferSmallWindowUpdates()) {
    last_recv_window_update_ = base::TimeTicks::Now();
    session_->SendStreamWindowUpdate(
        stream_id_, static_cast<uint32_t>(unacked_recv_window_bytes_));
    unacked_recv_window_bytes_ = 0;   // UAF write: stream may have been freed
  }
}

```

The call to SendStreamWindowUpdate chains through SendWindowUpdateFrame into EnqueueSessionWrite. EnqueueSessionWrite contains a guard that synchronously drains the session when the capped-frame queue exceeds a configurable limit:

```
// net/spdy/spdy_session.cc
void SpdySession::EnqueueSessionWrite(...) {
  // ...
  if (write_queue_.num_queued_capped_frames() >
      session_max_queued_capped_frames_) {
    DoDrainSession(ERR_CONNECTION_CLOSED, "Exceeded max queued capped frames");
    return;
  }
  // ...
}

```

DoDrainSession calls StartGoingAway, which iterates over all active streams and destroys them via CloseActiveStreamIterator and DeleteStream. The SpdyStream whose IncreaseRecvWindowSize is on the call stack is among those destroyed. When control returns to IncreaseRecvWindowSize, the assignment `unacked_recv_window_bytes_ = 0` writes to freed heap memory.

The inconsistency is visible within the same file. SpdyStream::OnPaddingConsumed does capture a WeakPtr before calling DecreaseRecvWindowSize and checks it before proceeding, but this guard does not cover the IncreaseRecvWindowSize call that follows:

```
// net/spdy/spdy_stream.cc
void SpdyStream::OnPaddingConsumed(size_t len) {
  base::WeakPtr<SpdyStream> weak_this = GetWeakPtr();
  DecreaseRecvWindowSize(static_cast<int32_t>(len));
  if (!weak_this)
    return;
  IncreaseRecvWindowSize(static_cast<int32_t>(len));
  // No check after IncreaseRecvWindowSize; if it triggers DoDrainSession,
  // `this` is already freed before we return.
}

```

Similarly, SpdyStream::OnDataReceived protects itself with a WeakPtr around DecreaseRecvWindowSize but the consume-callback path through OnReadBufferConsumed into IncreaseRecvWindowSize lacks the same protection.

The triggering sequence works as follows. SpdySession::OnStreamPadding, called during frame decoding inside DoReadComplete, first invokes the session-level IncreaseRecvWindowSize and then calls OnPaddingConsumed on the stream:

```
// net/spdy/spdy_session.cc
void SpdySession::OnStreamPadding(spdy::SpdyStreamId stream_id, size_t len) {
  DecreaseRecvWindowSize(static_cast<int32_t>(len));
  IncreaseRecvWindowSize(static_cast<int32_t>(len));   // session-level
  auto it = active_streams_.find(stream_id);
  if (it == active_streams_.end())
    return;
  it->second->OnPaddingConsumed(len);                   // stream-level
}

```

An attacker controlling an HTTP/2 server can exploit the differential thresholds between session-level and stream-level WINDOW\_UPDATE to ensure the session-level call does not trigger draining while the stream-level call does. The session-level WINDOW\_UPDATE threshold is half of 15 MB (7.5 MB), while the stream-level threshold is half of 6 MB (3 MB). Alternatively, both levels have a time-based fallback that fires after kDefaultTimeToBufferSmallWindowUpdates (5 seconds) of inactivity. By sending exactly N SETTINGS frames (where N equals the configured session\_max\_queued\_capped\_frames limit) followed by a single padded DATA frame after the 5-second window has elapsed, the attacker arranges for the session WINDOW\_UPDATE to pass the overflow check (N > N is false), bringing the queue to N+1, and then the stream WINDOW\_UPDATE to fail the check (N+1 > N is true), triggering DoDrainSession.

Because all frames arrive within a single DoReadComplete call (the entire burst is under kReadBufferSize of 8192 bytes), the write loop never has an opportunity to drain any of the queued SETTINGS ACK frames. The capped-frame count is guaranteed to be at N when the critical WINDOW\_UPDATE is enqueued.

The session\_max\_queued\_capped\_frames parameter defaults to 10000 and is configurable through the HTTP2 field trial ("spdy\_session\_max\_queued\_capped\_frames"). The vulnerability exists regardless of the configured value; only the number of SETTINGS frames the attacker must send changes. With the default value of 10000, the attacker sends 10001 SETTINGS frames (approximately 90 KB), which may span multiple DoReadComplete iterations due to the 8 KB read buffer, but the write loop is unable to keep pace with the read loop's frame processing, allowing the queue to grow past the limit. At default settings the attacker can also apply TCP-level backpressure by not reading from its end of the connection, stalling the client's outbound socket and preventing any queued ACKs from being flushed. For stable reproduction in the attached PoC, the limit is set to 100 via the field trial so that the entire attack burst (100 SETTINGS plus one padded DATA frame, 1166 bytes total) fits within a single 8 KB read and triggers deterministically in one DoReadComplete call.

## Reproduce

Tested on commit `effccce563102fd8315819caf7677f68394be7af` (Linux x86\_64). No source modifications required.

Start the malicious HTTP/2 server from the issue directory:

```
python3 server.py

```

Launch Chrome in a separate terminal. The field trial parameter lowers the capped-frame limit from the default 10000 to 100 for stable, deterministic reproduction; the underlying bug is identical at any limit value.

```
ASAN_OPTIONS=detect_odr_violation=0 ~/chromium/src/out/asan-release/chrome \
  --no-sandbox --disable-gpu --ignore-certificate-errors \
  --user-data-dir=/tmp/poc-$(date +%s) \
  --headless=new \
  --force-fieldtrials=HTTP2/Experiment/ \
  --force-fieldtrial-params="HTTP2.Experiment:spdy_session_max_queued_capped_frames/100" \
  https://localhost:8443/

```

The Network Service IO thread crashes with a heap-use-after-free within approximately 8 seconds.

```
==1795377==ERROR: AddressSanitizer: heap-use-after-free on address 0x7c827e119d14 at pc 0x7f12fcc0c1e9 bp 0x7b1271590750 sp 0x7b1271590748
WRITE of size 4 at 0x7c827e119d14 thread T7 (Chrome_ChildIOT)
    #0 0x7f12fcc0c1e8 in net::SpdyStream::IncreaseRecvWindowSize(int) net/spdy/spdy_stream.cc:289:32
    #1 0x7f12fcc10913 in net::SpdyStream::OnPaddingConsumed(unsigned long) net/spdy/spdy_stream.cc:497:3
    #2 0x7f12fcbd6cd4 in net::SpdySession::OnStreamPadding(unsigned int, unsigned long) net/spdy/spdy_session.cc:3032:15
    #3 0x7f12fb3c9537 in http2::FrameDecoderState::ReadPadLength(http2::DecodeBuffer*, bool) net/third_party/quiche/src/quiche/http2/decoder/frame_decoder_state.cc:29:21
    #4 0x7f12fb3ce259 in http2::DataPayloadDecoder::ResumeDecodingPayload(http2::FrameDecoderState*, http2::DecodeBuffer*) net/third_party/quiche/src/quiche/http2/decoder/payload_decoders/data_payload_decoder.cc:98:23
    #5 0x7f12fb3ca47f in http2::Http2FrameDecoder::StartDecodingPayload(http2::DecodeBuffer*) net/third_party/quiche/src/quiche/http2/decoder/http2_frame_decoder.cc:293:32
    #6 0x7f12fb3c9e29 in http2::Http2FrameDecoder::DecodeFrame(http2::DecodeBuffer*) net/third_party/quiche/src/quiche/http2/decoder/http2_frame_decoder.cc:57:16
    #7 0x7f12fb3993d5 in http2::Http2DecoderAdapter::ProcessInputFrame(char const*, unsigned long) net/third_party/quiche/src/quiche/http2/core/http2_frame_decoder_adapter.cc:800:40
    #8 0x7f12fb399206 in http2::Http2DecoderAdapter::ProcessInput(char const*, unsigned long) net/third_party/quiche/src/quiche/http2/core/http2_frame_decoder_adapter.cc:272:30
    #9 0x7f12fcbcd528 in net::SpdySession::DoReadComplete(int) net/spdy/spdy_session.cc:2063:53
    #10 0x7f12fcbcbed6 in net::SpdySession::DoReadLoop(net::SpdySession::ReadState, int) net/spdy/spdy_session.cc:1981:18
    #11 0x7f12fcbc87b0 in net::SpdySession::PumpReadLoop(net::SpdySession::ReadState, int) net/spdy/spdy_session.cc:1957:17

0x7c827e119d14 is located 148 bytes inside of 648-byte region [0x7c827e119c80,0x7c827e119f08)
freed by thread T7 (Chrome_ChildIOT) here:
    #0 0x560911f23ec2 in operator delete(void*, unsigned long)
    #1 0x7f12fcbc19a5 in net::SpdySession::CloseActiveStreamIterator(...) net/spdy/spdy_session.cc:1855:3
    #2 0x7f12fcbc3e7b in net::SpdySession::StartGoingAway(unsigned int, net::Error) net/spdy/spdy_session.cc:1396:5
    #3 0x7f12fcbbd03f in net::SpdySession::DoDrainSession(...) net/spdy/spdy_session.cc:2744:5
    #4 0x7f12fcbcafa6 in net::SpdySession::EnqueueSessionWrite(...) net/spdy/spdy_session.cc:2562:5
    #5 0x7f12fcbc354a in net::SpdySession::SendWindowUpdateFrame(...) net/spdy/spdy_session.cc:2473:3
    #6 0x7f12fcbc2f8c in net::SpdySession::SendStreamWindowUpdate(...) net/spdy/spdy_session.cc:1349:3
    #7 0x7f12fcc0bf49 in net::SpdyStream::IncreaseRecvWindowSize(int) net/spdy/spdy_stream.cc:284:15
    #8 0x7f12fcc10913 in net::SpdyStream::OnPaddingConsumed(unsigned long) net/spdy/spdy_stream.cc:497:3
    #9 0x7f12fcbd6cd4 in net::SpdySession::OnStreamPadding(unsigned int, unsigned long) net/spdy/spdy_session.cc:3032:15

previously allocated by thread T7 (Chrome_ChildIOT) here:
    #0 0x560911f232bd in operator new(unsigned long)
    #1 0x7f12fcbc8c3e in net::SpdySession::CreateStream(...) gen/third_party/libc++/src/include/__memory/unique_ptr.h:756:26

```
## References

- [net/spdy/spdy\_stream.cc: IncreaseRecvWindowSize](https://source.chromium.org/chromium/chromium/src/+/main:net/spdy/spdy_stream.cc;l=250)
- [net/spdy/spdy\_stream.cc: OnPaddingConsumed](https://source.chromium.org/chromium/chromium/src/+/main:net/spdy/spdy_stream.cc;l=487)
- [net/spdy/spdy\_session.cc: EnqueueSessionWrite](https://source.chromium.org/chromium/chromium/src/+/main:net/spdy/spdy_session.cc;l=2544)
- [net/spdy/spdy\_session.cc: OnStreamPadding](https://source.chromium.org/chromium/chromium/src/+/main:net/spdy/spdy_session.cc;l=3013)
- [net/spdy/spdy\_session.cc: DoDrainSession](https://source.chromium.org/chromium/chromium/src/+/main:net/spdy/spdy_session.cc;l=2686)
- [Introducing commit (HTTP2 DoS Mitigations)](https://chromium-review.googlesource.com/c/chromium/src/+/1752387)

## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [poc.html](attachments/poc.html) (text/html, 243 B)
- [server.py](attachments/server.py) (text/x-python, 5.6 KB)
- [spdy_poc_key.pem](attachments/spdy_poc_key.pem) (application/octet-stream, 1.7 KB)
- [asan.log](attachments/asan.log) (text/plain, 20.3 KB)
- [readme.md](attachments/readme.md) (text/markdown, 1.1 KB)
- [spdy_poc_cert.pem](attachments/spdy_poc_cert.pem) (application/octet-stream, 1.1 KB)
- [server.py](attachments/server_75647074.py) (text/x-python, 8.9 KB)
- [poc.html](attachments/poc_75647075.html) (text/html, 2.4 KB)
- [readme.md](attachments/readme_75644783.md) (text/markdown, 922 B)
- [asan.log](attachments/asan_75632852.log) (text/plain, 18.1 KB)
- [report.md](attachments/report.md) (text/markdown, 13.4 KB)
- [asan.log](attachments/asan_75656900.log) (text/plain, 21.9 KB)

## Timeline

### je...@gmail.com (2026-04-17)

**Update a default configuration trigger version that does not require a flag**

# Use-after-free in SpdyStream::IncreaseRecvWindowSize via HTTP/2 capped frame queue overflow

## Summary

A use-after-free in the HTTP/2 stack allows a malicious server to crash the network service process by exploiting the interaction between flow control window updates and the capped frame queue drain mechanism. When the queue of write-capped frames (SETTINGS ACK, WINDOW\_UPDATE, etc.) exceeds 10000 entries, `EnqueueSessionWrite` synchronously calls `DoDrainSession`, which deletes all active streams. If the triggering `EnqueueSessionWrite` call originated from within `SpdyStream::IncreaseRecvWindowSize`, control returns to the now-freed `SpdyStream` object and writes to deallocated memory. This is remotely triggerable from any web page that connects to an attacker-controlled HTTP/2 origin, requires no user interaction, and affects all platforms.

## Bisect

Introducing Commit: `410676ab9660a0271949e043ddb8678a6d18b097`

- Date: 2019-08-13
- Author: David Schinazi
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/1752387>

This commit introduced the capped frame queue limit and the synchronous `DoDrainSession` call inside `EnqueueSessionWrite`. Prior to this change, `EnqueueSessionWrite` could not synchronously destroy streams, so callers like `IncreaseRecvWindowSize` had no reason to guard against `this` being deleted mid-call.

## Root Cause

When an HTTP/2 DATA frame is received, `SpdySession::OnStreamFrameData` wraps it in a `SpdyBuffer` and registers two consume callbacks on it before passing it to the stream:

```
// net/spdy/spdy_session.cc:2976-2981
buffer = std::make_unique<SpdyBuffer>(...);
DecreaseRecvWindowSize(static_cast<int32_t>(len));
buffer->AddConsumeCallback(base::BindRepeating(
    &SpdySession::OnReadBufferConsumed, weak_factory_.GetWeakPtr()));

```

The stream then registers its own callback:

```
// net/spdy/spdy_stream.cc:472-473
buffer->AddConsumeCallback(
    base::BindRepeating(&SpdyStream::OnReadBufferConsumed, GetWeakPtr()));

```

The session-level callback is registered first. When the buffer is eventually consumed in `SpdyHttpStream::DoBufferedReadCallback`, `SpdyBuffer::ConsumeHelper` iterates through the callbacks in registration order:

```
// net/spdy/spdy_buffer.cc:102-111
void SpdyBuffer::ConsumeHelper(size_t consume_size,
                               ConsumeSource consume_source) {
  offset_ += consume_size;
  for (auto it = consume_callbacks_.begin();
       it != consume_callbacks_.end(); ++it) {
    it->Run(consume_size, consume_source);
  }
}

```

Each callback reaches its respective `IncreaseRecvWindowSize`, which may send a WINDOW\_UPDATE frame. The session-level `SpdySession::IncreaseRecvWindowSize` sends a session-level WINDOW\_UPDATE (stream ID 0). The stream-level `SpdyStream::IncreaseRecvWindowSize` sends a stream-level WINDOW\_UPDATE via `SendStreamWindowUpdate`. Both WINDOW\_UPDATEs go through `EnqueueSessionWrite`, which checks the capped frame queue:

```
// net/spdy/spdy_session.cc:2554-2561
if (write_queue_.num_queued_capped_frames() >
    session_max_queued_capped_frames_) {
  DoDrainSession(ERR_CONNECTION_CLOSED,
                 "Exceeded max queued capped frames");
  return;
}

```

`DoDrainSession` synchronously calls `StartGoingAway`, which iterates over all active streams and calls `CloseActiveStreamIterator` for each, which takes ownership of the `SpdyStream` via `unique_ptr` and calls `DeleteStream`. When `DeleteStream` returns, the `SpdyStream` is freed.

The vulnerability is in `SpdyStream::IncreaseRecvWindowSize`. After calling `SendStreamWindowUpdate`, which may trigger the drain and free `this`, the function unconditionally writes to the now-freed member:

```
// net/spdy/spdy_stream.cc:250-282
void SpdyStream::IncreaseRecvWindowSize(int32_t delta_window_size) {
  if (!session_->IsStreamActive(stream_id_))
    return;
  // ...
  unacked_recv_window_bytes_ += delta_window_size;
  if (unacked_recv_window_bytes_ > max_recv_window_size_ / 2 ||
      elapsed >= session_->TimeToBufferSmallWindowUpdates()) {
    session_->SendStreamWindowUpdate(
        stream_id_,
        static_cast<uint32_t>(unacked_recv_window_bytes_));
    // DoDrainSession may have freed |this| here.
    unacked_recv_window_bytes_ = 0;  // UAF write
  }
}

```

Note the `IsStreamActive` check at the top of the function. This guards against calling the function on an already-closed stream, but it runs before `SendStreamWindowUpdate` and cannot protect against the stream being deleted during the call.

To trigger this, an attacker needs the capped frame queue to contain exactly 10000 entries when the stream-level WINDOW\_UPDATE is enqueued. The session-level callback fires first (because it was registered first) and enqueues a session-level WINDOW\_UPDATE, bringing the count to 10000 without exceeding the limit. The stream-level callback fires second and enqueues a stream-level WINDOW\_UPDATE, bringing the count to 10001, which exceeds `kSpdySessionMaxQueuedCappedFrames` (10000) and triggers the drain. This precision is achieved by flooding 10000 empty SETTINGS frames while the client write loop is blocked, causing 10000 SETTINGS ACK frames to accumulate in the write queue without being flushed.

The write loop remains blocked because a concurrent POST request on the same connection fills the TCP send buffer. When the server stops reading, client-side TCP backpressure sets `in_flight_write_`, which prevents `MaybePostWriteLoop` from scheduling a write pump. The SETTINGS ACKs therefore remain queued until the consume callbacks fire and push the count over the limit.

The entire sequence occurs on a single IO thread with no cross-thread races. It is a purely synchronous reentrant self-deletion: `IncreaseRecvWindowSize` calls `SendStreamWindowUpdate`, which calls `EnqueueSessionWrite`, which calls `DoDrainSession`, which deletes the stream, and control returns to `IncreaseRecvWindowSize` operating on freed memory.

## Reproduce

Tested on commit `effccce563102fd8315819caf7677f68394be7af`, Linux x86\_64, ASAN release build (`autoninja -C out/asan-release chrome`).

The PoC consists of two files: `poc.html` (loaded in Chrome) and `server.py` (a raw HTTP/2 server that sends the exploit payload). Generate a TLS certificate, start both servers, and launch Chrome:

```
cd issue_spdy_stream_uaf
openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:prime256v1 \
  -keyout key.pem -out cert.pem -days 1 -nodes -subj '/CN=localhost'
python3 -m http.server 8888 &
python3 server.py &
ASAN_OPTIONS=detect_odr_violation=0 xvfb-run -a out/asan-release/chrome \
  --no-sandbox --disable-gpu --ignore-certificate-errors --disable-web-security \
  --no-proxy-server --user-data-dir=/tmp/poc-$(date +%s) \
  http://localhost:8888/poc.html

```

The network service process crashes with a heap-use-after-free within approximately 15 seconds.

```
=================================================================
==2432110==ERROR: AddressSanitizer: heap-use-after-free on address 0x7d68951d2684 at pc 0x7ff912e0c4ec bp 0x7bf888590cd0 sp 0x7bf888590cc8
READ of size 4 at 0x7d68951d2684 thread T7 (Chrome_ChildIOT)
    #0 0x7ff912e0c4eb in net::SpdyStream::IncreaseRecvWindowSize(int) net/spdy/spdy_stream.cc:286:36
    #1 0x7ff912e15ed5 in base::internal::Invoker<...>::Run(...) base/functional/bind_internal.h:740:12
    #2 0x7ff912d92dc1 in base::RepeatingCallback<...>::Run(...) base/functional/callback.h:346:12
    #3 0x7ff912d9211f in net::SpdyBuffer::~SpdyBuffer() net/spdy/spdy_buffer.cc:109:9
    #4 0x7ff912db011b in base::internal::VectorBuffer<...>::DestructRange(...) gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
    #5 0x7ff912dafa35 in base::circular_deque<...>::DestructRange(...) base/containers/circular_deque.h
    #6 0x7ff912daf358 in net::SpdyReadQueue::Dequeue(...) base/containers/circular_deque.h:1002:5
    #7 0x7ff912d9cb12 in net::SpdyHttpStream::DoBufferedReadCallback() net/spdy/spdy_http_stream.cc:546:30
    #8 0x7ff912da0bc2 in base::internal::Invoker<...>::RunOnce(...) base/functional/bind_internal.h:740:12
    #9 0x7ff91909299f in base::OneShotTimer::RunUserTask() base/functional/callback.h:155:12
    #10 0x7ff91909663c in base::internal::Invoker<...>::Run(...) base/functional/bind_internal.h:740:12
    #11 0x7ff918f61b59 in base::TaskAnnotator::RunTaskImpl(...) base/functional/callback.h:155:12
    #12 0x7ff918fdc1d0 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(...) base/task/common/task_annotator.h:112:5
    #13 0x7ff918fdb1a6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:336:40
    #14 0x7ff91918c2a9 in base::MessagePumpEpoll::Run(...) base/message_loop/message_pump_epoll.cc:224:55
    #15 0x7ff918fdd823 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(...) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:640:12
    #16 0x7ff918eccc72 in base::RunLoop::Run(...) base/run_loop.cc:135:14
    #17 0x7ff919075892 in base::Thread::Run(...) base/threading/thread.cc:356:13
    #18 0x7ff8f8efefa1 in content::(anonymous namespace)::ChildIOThread::Run(...) content/child/child_process.cc:69:19
    #19 0x7ff919075df5 in base::Thread::ThreadMain() base/threading/thread.cc:426:3
    #20 0x7ff9190daa4c in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:102:13
    #21 0x56340da52b36 in asan_thread_start(void*) asan_interceptors.cpp

0x7d68951d2684 is located 4 bytes inside of 648-byte region [0x7d68951d2680,0x7d68951d2908)
freed by thread T7 (Chrome_ChildIOT) here:
    #0 0x56340da8edc2 in operator delete(void*, unsigned long) (chrome+0x681cdc2)
    #1 0x7ff912dc1b65 in net::SpdySession::CloseActiveStreamIterator(...) net/spdy/spdy_session.cc:1855:3
    #2 0x7ff912dc415b in net::SpdySession::StartGoingAway(...) net/spdy/spdy_session.cc:1396:5
    #3 0x7ff912dbd1ff in net::SpdySession::DoDrainSession(...) net/spdy/spdy_session.cc:2744:5
    #4 0x7ff912dcb31a in net::SpdySession::EnqueueSessionWrite(...) net/spdy/spdy_session.cc:2566:5
    #5 0x7ff912dc3849 in net::SpdySession::SendWindowUpdateFrame(...) net/spdy/spdy_session.cc:2476:3
    #6 0x7ff912dc314c in net::SpdySession::SendStreamWindowUpdate(...) net/spdy/spdy_session.cc:1349:3
    #7 0x7ff912e0c14f in net::SpdyStream::IncreaseRecvWindowSize(int) net/spdy/spdy_stream.cc:283:15
    #8 0x7ff912e15ed5 in base::internal::Invoker<...>::Run(...) base/functional/bind_internal.h:740:12
    #9 0x7ff912d92dc1 in base::RepeatingCallback<...>::Run(...) base/functional/callback.h:346:12
    #10 0x7ff912d9211f in net::SpdyBuffer::~SpdyBuffer() net/spdy/spdy_buffer.cc:109:9
    #11 0x7ff912db011b in base::internal::VectorBuffer<...>::DestructRange(...) gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
    #12 0x7ff912dafa35 in base::circular_deque<...>::DestructRange(...) base/containers/circular_deque.h
    #13 0x7ff912daf358 in net::SpdyReadQueue::Dequeue(...) base/containers/circular_deque.h:1002:5
    #14 0x7ff912d9cb12 in net::SpdyHttpStream::DoBufferedReadCallback() net/spdy/spdy_http_stream.cc:546:30
    #15 0x7ff912da0bc2 in base::internal::Invoker<...>::RunOnce(...) base/functional/bind_internal.h:740:12
    #16 0x7ff91909299f in base::OneShotTimer::RunUserTask() base/functional/callback.h:155:12
    #17 0x7ff91909663c in base::internal::Invoker<...>::Run(...) base/functional/bind_internal.h:740:12
    #18 0x7ff918f61b59 in base::TaskAnnotator::RunTaskImpl(...) base/functional/callback.h:155:12
    #19 0x7ff918fdc1d0 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(...) base/task/common/task_annotator.h:112:5
    #20 0x7ff918fdb1a6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:336:40
    #21 0x7ff91918c2a9 in base::MessagePumpEpoll::Run(...) base/message_loop/message_pump_epoll.cc:224:55
    #22 0x7ff918fdd823 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(...) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:640:12
    #23 0x7ff918eccc72 in base::RunLoop::Run(...) base/run_loop.cc:135:14
    #24 0x7ff919075892 in base::Thread::Run(...) base/threading/thread.cc:356:13
    #25 0x7ff8f8efefa1 in content::(anonymous namespace)::ChildIOThread::Run(...) content/child/child_process.cc:69:19
    #26 0x7ff919075df5 in base::Thread::ThreadMain() base/threading/thread.cc:426:3
    #27 0x7ff9190daa4c in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:102:13
    #28 0x56340da52b36 in asan_thread_start(void*) asan_interceptors.cpp

previously allocated by thread T7 (Chrome_ChildIOT) here:
    #0 0x56340da8e1bd in operator new(unsigned long) (chrome+0x681c1bd)
    #1 0x7ff912dc8f1e in net::SpdySession::CreateStream(...) gen/third_party/libc++/src/include/__memory/unique_ptr.h:756:26
    #2 0x7ff912db64d0 in net::SpdySession::TryCreateStream(...) net/spdy/spdy_session.cc:1697:12
    #3 0x7ff912db564c in net::SpdyStreamRequest::StartRequest(...) net/spdy/spdy_session.cc:617:17
    #4 0x7ff912d9579b in net::SpdyHttpStream::InitializeStream(...) net/spdy/spdy_http_stream.cc:74:28
    #5 0x7ff91292d429 in net::HttpNetworkTransaction::DoInitStream() net/http/http_network_transaction.cc:1262:21

SUMMARY: AddressSanitizer: heap-use-after-free net/spdy/spdy_stream.cc:286:36 in net::SpdyStream::IncreaseRecvWindowSize(int)

```
## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

### ti...@google.com (2026-04-17)

[Security shepherd] This looks plausible, and if true would be a UaF in an unsandboxed process (network process is not sandboxed on android, windows, linux [1](https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/process-sandboxes-by-platform.md)). Setting severity to S0

### ti...@google.com (2026-04-17)

[Security shepherd] I've reproduced this locally against stable (147) using `content_shell` - `chrome` must have been hanging on some first-run UI I couldn't see with XVFB. ASAN log is attached.

I've minimized the command-line arguments to `--no-sandbox`, `--ignore-certificate-errors`.

- `--no-sandbox` allows ASan to symbolize the stack trace and output a good report
- `--ignore-certificate-errors` let's us use a self-signed cert

### ti...@google.com (2026-04-17)

[Security shepherd] Tried to repro reporter's bisection. Commit 410676ab9660a0271949e043ddb8678a6d18b097 [1](https://chromiumdash.appspot.com/commit/410676ab9660a0271949e043ddb8678a6d18b097) landed as r686599. The closest ASan build for Linux is two revisions later at r686601. No ASan crash there.

### ti...@google.com (2026-04-17)

CCing OWNERs of `net/spdy/`. Assigning to visiedo@ to find an owner within the networking team.

### ti...@google.com (2026-04-17)

I don't have any reason to believe that this is limited to Linux only. All of this code seems cross-platform enough, assuming that TCP backpressure works the same everywhere.

### mm...@chromium.org (2026-04-17)

I recently fixed a similar issue in SpdySession, also where it was draining itself synchronously, with a random consumer on the stack - draining notifies consumers synchronously of the effort, and consumers will likely delete their SpdyHttpStreams then. I think we may want to revisit how draining is handled (always do it async, or at least always send notifications asynchronously), but I'm not a SPDY expert.

### ch...@google.com (2026-04-18)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-18)

Setting Priority to P0 to match Severity s0. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### ba...@chromium.org (2026-04-20)

> I think we may want to revisit how draining is handled (always do it async, or at least always send notifications asynchronously),

Yeah, I guess we may want to figure out a safe way to drain the session. Always doing it async seems a good approach, but it may break some assumptions the current logic implicitly has.

Since this is a real UAF, I'm going to add a check in SpdyStream::IncreaseRecvWindowSize() whether the session is still alive, as a bandaid fix.

### dx...@google.com (2026-04-20)

Project: chromium/src  

Branch:  main  

Author:  Kenichi Ishibashi [bashi@chromium.org](mailto:bashi@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7775828>

Fix potential crash in SpdyStream::IncreaseRecvWindowSize

---


Expand for full commit details
```
     
    This CL fixes a potential crash in SpdyStream::IncreaseRecvWindowSize 
    caused by accessing a destroyed object. 
     
    SpdyStream::IncreaseRecvWindowSize calls 
    session_->SendStreamWindowUpdate, which can trigger session draining and 
    stream destruction if the number of queued capped frames exceeds the 
    limit. If the stream is destroyed during this call, accessing member 
    variables like unacked_recv_window_bytes_ after the call results in 
    accessing a invalid memory. 
     
    This CL adds a base::WeakPtr check after SendStreamWindowUpdate to 
    ensure the stream is still alive before proceeding. 
     
    Bug: 503420443 
    Test: SpdySessionTest.WindowUpdateExceedsCappedFramesLimit 
    Change-Id: Idb1f5252c9e05ef24701647ad2e70fd386547640 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7775828 
    Reviewed-by: Adam Rice <ricea@chromium.org> 
    Commit-Queue: Kenichi Ishibashi <bashi@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1617854}

```

---

Files:

- M `net/spdy/spdy_session_unittest.cc`
- M `net/spdy/spdy_stream.cc`

---

Hash: [6810eeb018a99d750b574fe44d44573133d677e3](https://chromiumdash.appspot.com/commit/6810eeb018a99d750b574fe44d44573133d677e3)  

Date: Mon Apr 20 23:30:29 2026


---

### sp...@google.com (2026-05-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $43000.00 for this report.

Rationale for this decision:
High quality with bisect. Memory corruption in a highly privileged process (e.g. GPU, network processes) 


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

**M148** merge request created. **Please update [crbug/514924021](https://crbug.com/514924021) to have this merge reviewed.**

### ch...@google.com (2026-08-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/503420443)*
