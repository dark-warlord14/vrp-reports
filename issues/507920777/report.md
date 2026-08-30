# SpdyStream Use-After-Free in QueueNextDataFrame via PrefacePing drain

| Field | Value |
|-------|-------|
| **Issue ID** | [507920777](https://issues.chromium.org/issues/507920777) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals>Network>HTTP2 |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ci...@gmail.com |
| **Assignee** | ba...@chromium.org |
| **Created** | 2026-04-29 |
| **Bounty** | $43,000.00 |

## Description

---

### Report description

WebSocket-over-H2 Adapter Use-After-Free in SpdyReadQueue::Dequeue

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://source.chromium.org/chromium/chromium/src/+/main:net/websockets/websocket_basic_stream_adapters.cc>

---

### The problem

#### Please describe the technical details of the vulnerability

WebSocketSpdyStreamAdapter::OnDataReceived() queues an incoming WebSocket-over-HTTP/2 DATA buffer, then calls CopySavedReadDataIntoBuffer(). That function calls read\_data\_.Dequeue().

SpdyReadQueue::Dequeue() destroys SpdyBuffer objects while it is still iterating the queue. Destroying a SpdyBuffer runs its consume callbacks.

If the session's capped write queue is already over session\_max\_queued\_capped\_frames (default 10000), EnqueueSessionWrite() synchronously calls DoDrainSession(). The drain closes active streams. Closing the target WebSocket-over-H2 stream calls WebSocketSpdyStreamAdapter::OnClose(), which runs the pending write callback. That callback reaches network::WebSocket::Reset(), destroys WebSocketChannel/WebSocketBasicStream, and deletes the WebSocketSpdyStreamAdapter while read\_data\_.Dequeue() is still executing on its embedded SpdyReadQueue.

Control then returns to SpdyReadQueue::Dequeue(), which continues reading from the freed WebSocketSpdyStreamAdapter object. ASan reports a heap-use-after-free READ of size 8 in SpdyReadQueue::Dequeue().

### Steps to Reproduce

1. Save poc.html and server.py in the same folder
2. `pip3 install h2`
3. `python3 server.py --port 9945`
4. Launch Chromium directly to the server URL (<https://localhost:9945/poc.html>). Do not open poc.html as a file:// URL. Accept the self-signed HTTPS certificate.

```
~/chromium/src/out/ASan/Chromium.app/Contents/MacOS/Chromium https://localhost:9945/poc.html

```

5. Wait approximately. 10 seconds, then ASan reports:

```
==61419==ERROR: AddressSanitizer: heap-use-after-free on address 0x6100000ac188 at pc 0x000379373c78 bp 0x0001712f1750 sp 0x0001712f1748
READ of size 8 at 0x6100000ac188 thread T9
    #0 net::SpdyReadQueue::Dequeue(...) net/spdy/spdy_read_queue.cc:46
    #1 net::WebSocketSpdyStreamAdapter::CopySavedReadDataIntoBuffer() net/websockets/websocket_basic_stream_adapters.cc:230
    #2 net::WebSocketSpdyStreamAdapter::OnDataReceived(...) net/websockets/websocket_basic_stream_adapters.cc:171
    #3 net::SpdyStream::OnDataReceived(...) net/spdy/spdy_stream.cc:485
[...]
MiraclePtr Status: NOT PROTECTED

```
#### Crash Evidence

**149.0.7813.0 (Developer Build) (arm64) - macOS 15 (Apple M5)**

- Attached `asan_symbolized.txt`

**149.0.7806.0 (Official Build) dev (64-bit) - Android 16 (Pixel 10, arm64)**

- chrome://crashes ID `ab76d78e338ac345`

### Proposed Fix

Do not let SpdyReadQueue::Dequeue() destroy SpdyBuffer objects and run consume callbacks while it will continue touching the queue afterward. A safe pattern would move consumed buffers out of the queue and defer destruction/consume callbacks until after Dequeue() no longer needs the SpdyReadQueue object, or make the capped-frame drain asynchronous for this reentrant path.

### Bisect

Source history indicates the complete bug shape became possible no later than commit 410676ab9660a0271949e043ddb8678a6d18b097 (HTTP2 DoS Mitigations, 2019-08-13), which added session\_max\_queued\_capped\_frames\_ and the synchronous EnqueueSessionWrite() -> DoDrainSession(ERR\_CONNECTION\_CLOSED) path used by this PoC.

#### Impact analysis

- Web-reachable, no compromised renderer required.
- Heap use-after-free in the network service process.
- Default configuration; no special feature flags required.
- Cross-platform (tested on macOS Apple Silicon and Android)

---

### The cause

#### What version of Chrome have you found the security issue in?

149.0.7813.0 (Developer Build) (arm64)

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed process)

#### How would you like to be publicly acknowledged for your report?

cinzinga

## Attachments

- [server.py](attachments/server.py) (text/x-python-script, 11.9 KB)
- [poc.html](attachments/poc.html) (text/html, 3.4 KB)
- [asan_symbolized.txt](attachments/asan_symbolized.txt) (text/plain, 50.4 KB)

## Timeline

### ye...@google.com (2026-04-30)

Setting this to s2 since it looks like a self-signed cert is required to exploit this, and having to convince a user to accept a self signed cert is enough of an unusual step for them to take that it is a mitigation that lowers the severity imo.

If it's possible to hit the crash without having to accept a self-signed cert then this may qualify as high severity.

### ci...@gmail.com (2026-04-30)

Thanks for the triage, security shepherd!

The requirement is HTTPS with HTTP/2, not a self-signed certificate. The original submission uses a self-signed localhost cert only for convenience.

On macOS this can be verified locally with a trusted certificate:

1. `brew install mkcert nss`
2. `mkcert -install`
3. `cd` into the directory containing server.py and poc.html
4. `mkdir -p .cert`
5. `mkcert -cert-file .cert/cert.pem -key-file .cert/key.pem localhost 127.0.0.1 ::1`
6. `python3 server.py --port 9945`
7. `~/chromium/src/out/ASan/Chromium.app/Contents/MacOS/Chromium https://localhost:9945/poc.html`

This reproduces the same ASan crash with a certificate trusted by Chrome.

### ch...@google.com (2026-05-01)

Setting milestone because of s2 severity.

### ch...@google.com (2026-05-01)

Setting Priority to P2 to match Severity s2. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### rc...@chromium.org (2026-05-06)

Assigning to bashi to evaluate who should work on this

### ba...@chromium.org (2026-05-07)

I agree that this doesn't seem to require a self-signed certificate. This issue is similar to [issue 507365348](https://issues.chromium.org/issues/507365348), which is S0/P0. Should we set this to S0/P0 too?

### ba...@chromium.org (2026-05-07)

I confirmed that the fix for [issue 507365348](https://issues.chromium.org/issues/507365348) also fixes this report.

### ch...@google.com (2026-08-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/507920777)*
