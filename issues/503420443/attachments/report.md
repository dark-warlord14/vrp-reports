# Use-after-free in SpdyStream::IncreaseRecvWindowSize via HTTP/2 capped frame queue overflow

## Summary

A use-after-free in the HTTP/2 stack allows a malicious server to crash the network service process by exploiting the interaction between flow control window updates and the capped frame queue drain mechanism. When the queue of write-capped frames (SETTINGS ACK, WINDOW_UPDATE, etc.) exceeds 10000 entries, `EnqueueSessionWrite` synchronously calls `DoDrainSession`, which deletes all active streams. If the triggering `EnqueueSessionWrite` call originated from within `SpdyStream::IncreaseRecvWindowSize`, control returns to the now-freed `SpdyStream` object and writes to deallocated memory. This is remotely triggerable from any web page that connects to an attacker-controlled HTTP/2 origin, requires no user interaction, and affects all platforms.

## Bisect

Introducing Commit: `410676ab9660a0271949e043ddb8678a6d18b097`
- Date: 2019-08-13
- Author: David Schinazi
- Review: https://chromium-review.googlesource.com/c/chromium/src/+/1752387

This commit introduced the capped frame queue limit and the synchronous `DoDrainSession` call inside `EnqueueSessionWrite`. Prior to this change, `EnqueueSessionWrite` could not synchronously destroy streams, so callers like `IncreaseRecvWindowSize` had no reason to guard against `this` being deleted mid-call.

## Root Cause

When an HTTP/2 DATA frame is received, `SpdySession::OnStreamFrameData` wraps it in a `SpdyBuffer` and registers two consume callbacks on it before passing it to the stream:

```cpp
// net/spdy/spdy_session.cc:2976-2981
buffer = std::make_unique<SpdyBuffer>(...);
DecreaseRecvWindowSize(static_cast<int32_t>(len));
buffer->AddConsumeCallback(base::BindRepeating(
    &SpdySession::OnReadBufferConsumed, weak_factory_.GetWeakPtr()));
```

The stream then registers its own callback:

```cpp
// net/spdy/spdy_stream.cc:472-473
buffer->AddConsumeCallback(
    base::BindRepeating(&SpdyStream::OnReadBufferConsumed, GetWeakPtr()));
```

The session-level callback is registered first. When the buffer is eventually consumed in `SpdyHttpStream::DoBufferedReadCallback`, `SpdyBuffer::ConsumeHelper` iterates through the callbacks in registration order:

```cpp
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

Each callback reaches its respective `IncreaseRecvWindowSize`, which may send a WINDOW_UPDATE frame. The session-level `SpdySession::IncreaseRecvWindowSize` sends a session-level WINDOW_UPDATE (stream ID 0). The stream-level `SpdyStream::IncreaseRecvWindowSize` sends a stream-level WINDOW_UPDATE via `SendStreamWindowUpdate`. Both WINDOW_UPDATEs go through `EnqueueSessionWrite`, which checks the capped frame queue:

```cpp
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

```cpp
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

To trigger this, an attacker needs the capped frame queue to contain exactly 10000 entries when the stream-level WINDOW_UPDATE is enqueued. The session-level callback fires first (because it was registered first) and enqueues a session-level WINDOW_UPDATE, bringing the count to 10000 without exceeding the limit. The stream-level callback fires second and enqueues a stream-level WINDOW_UPDATE, bringing the count to 10001, which exceeds `kSpdySessionMaxQueuedCappedFrames` (10000) and triggers the drain. This precision is achieved by flooding 10000 empty SETTINGS frames while the client write loop is blocked, causing 10000 SETTINGS ACK frames to accumulate in the write queue without being flushed.

The write loop remains blocked because a concurrent POST request on the same connection fills the TCP send buffer. When the server stops reading, client-side TCP backpressure sets `in_flight_write_`, which prevents `MaybePostWriteLoop` from scheduling a write pump. The SETTINGS ACKs therefore remain queued until the consume callbacks fire and push the count over the limit.

The entire sequence occurs on a single IO thread with no cross-thread races. It is a purely synchronous reentrant self-deletion: `IncreaseRecvWindowSize` calls `SendStreamWindowUpdate`, which calls `EnqueueSessionWrite`, which calls `DoDrainSession`, which deletes the stream, and control returns to `IncreaseRecvWindowSize` operating on freed memory.

## Reproduce

Tested on commit `effccce563102fd8315819caf7677f68394be7af`, Linux x86_64, ASAN release build (`autoninja -C out/asan-release chrome`).

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
