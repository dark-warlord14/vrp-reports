# Compromised renderer can inject invalid Sec-WebSocket-Protocol header values.

| Field | Value |
|-------|-------|
| **Issue ID** | [404573970](https://issues.chromium.org/issues/404573970) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Network>WebSockets |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | origin/main (59cdc128f) |
| **Reporter** | i....@gmail.com |
| **Assignee** | ri...@chromium.org |
| **Created** | 2025-03-19 |
| **Bounty** | Confirmed (amount unknown) |

## Description

# Steps to reproduce the problem

1. apply the below patch (attached as `diff.patch`)

```
diff --git a/third_party/blink/renderer/modules/websockets/websocket_channel_impl.cc b/third_party/blink/renderer/modules/websockets/websocket_channel_impl.cc
index d7f5c10b6f82..734fd042c852 100644
--- a/third_party/blink/renderer/modules/websockets/websocket_channel_impl.cc
+++ b/third_party/blink/renderer/modules/websockets/websocket_channel_impl.cc
@@ -310,14 +310,8 @@ bool WebSocketChannelImpl::Connect(const KURL& url, const String& protocol) {
   }

   url_ = url;
-  Vector<String> protocols;
-  // Avoid placing an empty token in the Vector when the protocol string is
-  // empty.
-  if (!protocol.empty()) {
-    // Since protocol is already verified and escaped, we can simply split
-    // it.
-    protocol.Split(", ", true, protocols);
-  }
+  // Simulate a compromised renderer sending crafted protocols.
+  Vector<String> protocols = { "()<>@,;:\\\"/[]?={}漢字", "()<>@,;:\\\"/[]?={}漢字" };

   // If the connection needs to be filtered, asynchronously fail. Synchronous
   // failure blocks the worker thread which should be avoided. Note that

```

2. run the server by running the below code with node. (attached as `server.js`)

```
const http = require('http');
http.createServer((req, res) => {
    console.log(req.headers)
}).listen(8888)

```

3. Open the below page (attached as `page.html`) by the patched chromium.

```
<body>
<script>
const socket = new WebSocket("ws://localhost:8888");
</script>
</body>

```

4. Check the server log, and you should see a log like below. Here, the values of `Sec-Websocket-Protocols` violates the two restrictions in RFC6455: they consists of disallowed chars (separators and chars outside the allowed range) and are not unique.

```
{
  host: 'localhost:8888',
  connection: 'Upgrade',
  pragma: 'no-cache',
  'cache-control': 'no-cache',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
  upgrade: 'websocket',
  origin: 'null',
  'sec-websocket-version': '13',
  'accept-encoding': 'gzip, deflate, br, zstd',
  'accept-language': 'en-US,en;q=0.9',
  'sec-websocket-key': 'FUv3W21YMU1XntNG/tLOAg==',
  'sec-websocket-extensions': 'permessage-deflate; client_max_window_bits',
  'sec-websocket-protocol': '()<>@,;:\\"/[]?={}Ã¦Â¼Â¢Ã¥ÂÂ\x97, ()<>@,;:\\"/[]?={}Ã¦Â¼Â¢Ã¥ÂÂ\x97'  // using disallowed chars and not unique
}

```
# Problem Description

# Vulnerability Details

- According to RFC6455, a websocket request may have `Sec-Websocket-Protocols` header. If this header is present, it has one or more values and they have two restrictions. [1](https://datatracker.ietf.org/doc/html/rfc6455#section-4.1:~:text=10.%20%20The%20request,in%20%5BRFC2616%5D.)
  
  1. "MUST be non-empty strings with characters in the range U+0021 to U+007E not including separator characters as defined in [RFC2616]"
  2. "MUST all be unique".
- For this header, validation for these restrictions is done in the renderer. [2](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/websockets/websocket_common.cc;l=100;bpv=1;bpt=1?q=websocket_common.&ss=chromium%2Fchromium%2Fsrc) But not in the browser process. So, if compromised renderer sends non-compliant values to the browser process, these values are used in a request.
- This means a compromised renderer can bypass these crucial security checks, potentially leading to unexpected behavior on the server.
- I'd like to add a point: I believe header injection cannot be achieved by this bug. This is because the browser process does the minimum validation for "Sec-Websocket-Protocols" values. Specifically, the value is checked by `HttpUtil::IsValidHeaderValue`. Actually, when `\n` is included in values in the patch file, PoC does not succeed. [3]
  
  - ref: `WebSocketBasicHandshakeStream::SendRequest` -> `WebSocketHandshakeStreamBase::AddVectorHeaders` -> `HttpRequestHeaders::SetHeader` -> `HttpUtil::IsValidHeaderValue`

# Impact

- Non-compliant header values can be a problem for a websocket server. It can lead to DoS and/or other exploits.
- "Sec-\*" value is generally thought as strictly controlled by the browser (client). So it should not be affected by the compromised renderer.

# Mitigation Idea

As mentioned above, the validation is already implemented in `WebSocketCommon::Connect` (third\_party/blink/renderer/modules/websockets/websocket\_common.cc) in the renderer process. So it can be moved or duplicated in the browser process.

# References

```
  // Fail if not all elements in |protocols| are valid.
  for (const String& protocol : protocols) {
    if (!IsValidSubprotocolString(protocol)) {
      state_ = kClosed;
      exception_state.ThrowDOMException(DOMExceptionCode::kSyntaxError,
                                        "The subprotocol '" +
                                            EncodeSubprotocolString(protocol) +
                                            "' is invalid.");
      return ConnectResult::kException;
    }
  }

  // Fail if there're duplicated elements in |protocols|.
  HashSet<String> visited;
  for (const String& protocol : protocols) {
    if (!visited.insert(protocol).is_new_entry) {
      state_ = kClosed;
      exception_state.ThrowDOMException(DOMExceptionCode::kSyntaxError,
                                        "The subprotocol '" +
                                            EncodeSubprotocolString(protocol) +
                                            "' is duplicated.");
      return ConnectResult::kException;
    }
  }

```

[3] the error exceeds the character limit, so I'll attach it in the following reply.

# Summary

Compromised renderer can inject invalid Sec-WebSocket-Protocol header values.

# Custom Questions

#### Reporter credit:

canalun

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [diff.patch](attachments/diff.patch) (text/x-diff, 1.0 KB)
- [page.html](attachments/page.html) (text/html, 87 B)
- [server.js](attachments/server.js) (text/javascript, 111 B)

## Timeline

### i....@gmail.com (2025-03-19)

[3] Here is the error message when you includes `\n` in values in the patch file.

And the version I used to reproduce the problem is `origin/main`(`59cdc128`).

```
[87115:14704740:0319/104519.425172:FATAL:net/http/http_request_headers.cc:136] Check failed: HttpUtil::IsValidHeaderValue(value). Sec-WebSocket-Protocol has invalid value.
0   libbase.dylib                       0x000000010571dad4 base::debug::CollectStackTrace(base::span<void const*, 18446744073709551615ul, void const**>) + 84
1   libbase.dylib                       0x00000001056bd8a4 base::debug::StackTrace::StackTrace(unsigned long) + 156
2   libbase.dylib                       0x00000001056bd94c base::debug::StackTrace::StackTrace(unsigned long) + 36
3   libbase.dylib                       0x00000001056bd918 base::debug::StackTrace::StackTrace() + 40
4   libbase.dylib                       0x0000000105325844 logging::LogMessage::Flush() + 196
5   libbase.dylib                       0x0000000105325764 logging::LogMessage::~LogMessage() + 44
6   libbase.dylib                       0x00000001052b844c logging::(anonymous namespace)::CheckLogMessage::~CheckLogMessage() + 72
7   libbase.dylib                       0x00000001052b83c4 logging::(anonymous namespace)::CheckLogMessage::~CheckLogMessage() + 28
8   libbase.dylib                       0x00000001052b83f0 logging::(anonymous namespace)::CheckLogMessage::~CheckLogMessage() + 28
9   libbase.dylib                       0x00000001052b95a4 std::__Cr::default_delete<logging::LogMessage>::operator()(logging::LogMessage*) const + 52
10  libbase.dylib                       0x00000001052b7d0c std::__Cr::unique_ptr<logging::LogMessage, std::__Cr::default_delete<logging::LogMessage>>::reset(logging::LogMessage*) + 68
11  libbase.dylib                       0x00000001052b7d94 logging::CheckNoreturnError::~CheckNoreturnError() + 32
12  libbase.dylib                       0x00000001052b7db4 logging::CheckNoreturnError::Check(char const*, base::Location const&) + 0
13  libnet.dylib                        0x000000011257d108 net::HttpRequestHeaders::SetHeader(std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>&&) + 256
14  libnet.dylib                        0x0000000112c1b628 net::(anonymous namespace)::AddVectorHeaderIfNonEmpty(char const*, std::__Cr::vector<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::allocator<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>> const&, net::HttpRequestHeaders*) + 200
15  libnet.dylib                        0x0000000112c1b53c net::WebSocketHandshakeStreamBase::AddVectorHeaders(std::__Cr::vector<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::allocator<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>> const&, std::__Cr::vector<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::allocator<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>> const&, net::HttpRequestHeaders*) + 64
16  libnet.dylib                        0x0000000112bd53cc net::WebSocketBasicHandshakeStream::SendRequest(net::HttpRequestHeaders const&, net::HttpResponseInfo*, base::OnceCallback<void (int)>) + 1140
17  libnet.dylib                        0x00000001125462c8 net::HttpNetworkTransaction::DoSendRequest() + 248
18  libnet.dylib                        0x000000011253e75c net::HttpNetworkTransaction::DoLoop(int) + 1168
19  libnet.dylib                        0x000000011253d32c net::HttpNetworkTransaction::OnIOComplete(int) + 36
20  libnet.dylib                        0x0000000112541d74 net::HttpNetworkTransaction::OnStreamReady(net::ProxyInfo const&, std::__Cr::unique_ptr<net::HttpStream, std::__Cr::default_delete<net::HttpStream>>) + 644
21  libnet.dylib                        0x00000001125421a8 net::HttpNetworkTransaction::OnWebSocketHandshakeStreamReady(net::ProxyInfo const&, std::__Cr::unique_ptr<net::WebSocketHandshakeStreamBase, std::__Cr::default_delete<net::WebSocketHandshakeStreamBase>>) + 100
22  libnet.dylib                        0x00000001125e853c net::HttpStreamFactory::JobController::OnWebSocketHandshakeStreamReady(net::HttpStreamFactory::Job*, net::ProxyInfo const&, std::__Cr::unique_ptr<net::WebSocketHandshakeStreamBase, std::__Cr::default_delete<net::WebSocketHandshakeStreamBase>>) + 564
23  libnet.dylib                        0x00000001125d5034 net::HttpStreamFactory::Job::OnWebSocketHandshakeStreamReadyCallback() + 404
24  libnet.dylib                        0x00000001125e0c38 void base::internal::DecayedFunctorTraits<void (net::HttpStreamFactory::Job::*)(), base::WeakPtr<net::HttpStreamFactory::Job>&&>::Invoke<void (net::HttpStreamFactory::Job::*)(), base::WeakPtr<net::HttpStreamFactory::Job> const&>(void (net::HttpStreamFactory::Job::*)(), base::WeakPtr<net::HttpStreamFactory::Job> const&) + 140
25  libnet.dylib                        0x00000001125e0b78 void base::internal::InvokeHelper<true, base::internal::FunctorTraits<void (net::HttpStreamFactory::Job::*&&)(), base::WeakPtr<net::HttpStreamFactory::Job>&&>, void, 0ul>::MakeItSo<void (net::HttpStreamFactory::Job::*)(), std::__Cr::tuple<base::WeakPtr<net::HttpStreamFactory::Job>>>(void (net::HttpStreamFactory::Job::*&&)(), std::__Cr::tuple<base::WeakPtr<net::HttpStreamFactory::Job>>&&) + 104
26  libnet.dylib                        0x00000001125e0b04 void base::internal::Invoker<base::internal::FunctorTraits<void (net::HttpStreamFactory::Job::*&&)(), base::WeakPtr<net::HttpStreamFactory::Job>&&>, base::internal::BindState<true, true, false, void (net::HttpStreamFactory::Job::*)(), base::WeakPtr<net::HttpStreamFactory::Job>>, void ()>::RunImpl<void (net::HttpStreamFactory::Job::*)(), std::__Cr::tuple<base::WeakPtr<net::HttpStreamFactory::Job>>, 0ul>(void (net::HttpStreamFactory::Job::*&&)(), std::__Cr::tuple<base::WeakPtr<net::HttpStreamFactory::Job>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) + 32
27  libnet.dylib                        0x00000001125e0a8c base::internal::Invoker<base::internal::FunctorTraits<void (net::HttpStreamFactory::Job::*&&)(), base::WeakPtr<net::HttpStreamFactory::Job>&&>, base::internal::BindState<true, true, false, void (net::HttpStreamFactory::Job::*)(), base::WeakPtr<net::HttpStreamFactory::Job>>, void ()>::RunOnce(base::internal::BindStateBase*) + 44
28  libbase.dylib                       0x00000001052a8634 base::OnceCallback<void ()>::Run() && + 176
29  libbase.dylib                       0x000000010551eb2c base::TaskAnnotator::RunTaskImpl(base::PendingTask&) + 480
30  libbase.dylib                       0x00000001055a8ac4 _ZN4base13TaskAnnotator7RunTaskIJZNS_16sequence_manager8internal35ThreadControllerWithMessagePumpImpl10DoWorkImplEPNS_7LazyNowEE3$_4EEEvN8perfetto12StaticStringERNS_11PendingTaskEDpOT_ + 144
31  libbase.dylib                       0x00000001055a8428 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) + 1540
32  libbase.dylib                       0x00000001055a7bb8 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() + 240
33  libbase.dylib                       0x00000001057a1010 base::MessagePumpKqueue::RunBatched(base::MessagePump::Delegate*) + 148
34  libbase.dylib                       0x00000001057a0de4 base::MessagePumpKqueue::Run(base::MessagePump::Delegate*) + 124
35  libbase.dylib                       0x00000001055a9260 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) + 592
36  libbase.dylib                       0x0000000105474310 base::RunLoop::Run(base::Location const&) + 628
37  libbase.dylib                       0x000000010564d1f0 base::Thread::Run(base::RunLoop*) + 252
38  libcontent.dylib                    0x00000003000f61e0 content::(anonymous namespace)::ChildIOThread::Run(base::RunLoop*) + 164
39  libbase.dylib                       0x000000010564d6c4 base::Thread::ThreadMain() + 860
40  libbase.dylib                       0x00000001056ba468 base::(anonymous namespace)::ThreadFunc(void*) + 244
41  libsystem_pthread.dylib             0x0000000199b642e4 _pthread_start + 136
42  libsystem_pthread.dylib             0x0000000199b5f0fc thread_start + 8
Task trace:
0   libnet.dylib                        0x00000001125d6850 net::HttpStreamFactory::Job::RunLoop(int) + 976
1   libnet.dylib                        0x0000000112907c60 net::WebSocketTransportClientSocketPool::InvokeUserCallbackLater(net::ClientSocketHandle*, base::OnceCallback<void (int)>, int) + 220
Crash keys:
  "chrome-trace-id" = "12309077458098954327"
  "service-name" = "network.mojom.NetworkService"
  "reentry_guard_tls_slot" = "395"
  "switch-9" = "--seatbelt-client=109"
  "switch-8" = "--variations-seed-version"
  "switch-7" = "--field-trial-handle=1718379636,r,10560309286850901982,124118133"
  "switch-6" = "--metrics-shmem-handle=1752395122,r,2834735197396655481,20354222"
  "switch-5" = "--shared-files"
  "switch-4" = "--start-stack-profiler"
  "switch-3" = "--service-sandbox-type=network"
  "switch-2" = "--lang=en-US"
  "switch-1" = "--utility-sub-type=network.mojom.NetworkService"
  "num-switches" = "10"
  "osarch" = "arm64"
  "pid" = "87115"
  "ptype" = "utility"

Received signal 6
0   libbase.dylib                       0x000000010571dad4 base::debug::CollectStackTrace(base::span<void const*, 18446744073709551615ul, void const**>) + 84
1   libbase.dylib                       0x00000001056bd8a4 base::debug::StackTrace::StackTrace(unsigned long) + 156
2   libbase.dylib                       0x00000001056bd94c base::debug::StackTrace::StackTrace(unsigned long) + 36
3   libbase.dylib                       0x00000001056bd918 base::debug::StackTrace::StackTrace() + 40
4   libbase.dylib                       0x000000010571d8d0 base::debug::(anonymous namespace)::StackDumpSignalHandler(int, __siginfo*, void*) + 1352
5   libsystem_platform.dylib            0x0000000199b9ade4 _sigtramp + 56
6   libsystem_pthread.dylib             0x0000000199b63f70 pthread_kill + 288
7   libsystem_c.dylib                   0x0000000199a70908 abort + 128
8   libbase.dylib                       0x0000000105326a84 logging::LogMessage::HandleFatal(unsigned long, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&) const + 424
9   libbase.dylib                       0x0000000105334d18 _ZZN7logging10LogMessage5FlushEvENK3$_0clEv + 72
10  libbase.dylib                       0x0000000105334c78 _ZN4absl16cleanup_internal7StorageIZN7logging10LogMessage5FlushEvE3$_0E14InvokeCallbackEv + 28
11  libbase.dylib                       0x0000000105334c24 _ZN4absl7CleanupINS_16cleanup_internal3TagEZN7logging10LogMessage5FlushEvE3$_0ED2Ev + 48
12  libbase.dylib                       0x0000000105326468 _ZN4absl7CleanupINS_16cleanup_internal3TagEZN7logging10LogMessage5FlushEvE3$_0ED1Ev + 28
13  libbase.dylib                       0x0000000105325d0c logging::LogMessage::Flush() + 1420
14  libbase.dylib                       0x0000000105325764 logging::LogMessage::~LogMessage() + 44
15  libbase.dylib                       0x00000001052b844c logging::(anonymous namespace)::CheckLogMessage::~CheckLogMessage() + 72
16  libbase.dylib                       0x00000001052b83c4 logging::(anonymous namespace)::CheckLogMessage::~CheckLogMessage() + 28
17  libbase.dylib                       0x00000001052b83f0 logging::(anonymous namespace)::CheckLogMessage::~CheckLogMessage() + 28
18  libbase.dylib                       0x00000001052b95a4 std::__Cr::default_delete<logging::LogMessage>::operator()(logging::LogMessage*) const + 52
19  libbase.dylib                       0x00000001052b7d0c std::__Cr::unique_ptr<logging::LogMessage, std::__Cr::default_delete<logging::LogMessage>>::reset(logging::LogMessage*) + 68
20  libbase.dylib                       0x00000001052b7d94 logging::CheckNoreturnError::~CheckNoreturnError() + 32
21  libbase.dylib                       0x00000001052b7db4 logging::CheckNoreturnError::Check(char const*, base::Location const&) + 0
22  libnet.dylib                        0x000000011257d108 net::HttpRequestHeaders::SetHeader(std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>&&) + 256
23  libnet.dylib                        0x0000000112c1b628 net::(anonymous namespace)::AddVectorHeaderIfNonEmpty(char const*, std::__Cr::vector<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::allocator<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>> const&, net::HttpRequestHeaders*) + 200
24  libnet.dylib                        0x0000000112c1b53c net::WebSocketHandshakeStreamBase::AddVectorHeaders(std::__Cr::vector<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::allocator<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>> const&, std::__Cr::vector<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::allocator<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>> const&, net::HttpRequestHeaders*) + 64
25  libnet.dylib                        0x0000000112bd53cc net::WebSocketBasicHandshakeStream::SendRequest(net::HttpRequestHeaders const&, net::HttpResponseInfo*, base::OnceCallback<void (int)>) + 1140
26  libnet.dylib                        0x00000001125462c8 net::HttpNetworkTransaction::DoSendRequest() + 248
27  libnet.dylib                        0x000000011253e75c net::HttpNetworkTransaction::DoLoop(int) + 1168
28  libnet.dylib                        0x000000011253d32c net::HttpNetworkTransaction::OnIOComplete(int) + 36
29  libnet.dylib                        0x0000000112541d74 net::HttpNetworkTransaction::OnStreamReady(net::ProxyInfo const&, std::__Cr::unique_ptr<net::HttpStream, std::__Cr::default_delete<net::HttpStream>>) + 644
30  libnet.dylib                        0x00000001125421a8 net::HttpNetworkTransaction::OnWebSocketHandshakeStreamReady(net::ProxyInfo const&, std::__Cr::unique_ptr<net::WebSocketHandshakeStreamBase, std::__Cr::default_delete<net::WebSocketHandshakeStreamBase>>) + 100
31  libnet.dylib                        0x00000001125e853c net::HttpStreamFactory::JobController::OnWebSocketHandshakeStreamReady(net::HttpStreamFactory::Job*, net::ProxyInfo const&, std::__Cr::unique_ptr<net::WebSocketHandshakeStreamBase, std::__Cr::default_delete<net::WebSocketHandshakeStreamBase>>) + 564
32  libnet.dylib                        0x00000001125d5034 net::HttpStreamFactory::Job::OnWebSocketHandshakeStreamReadyCallback() + 404
33  libnet.dylib                        0x00000001125e0c38 void base::internal::DecayedFunctorTraits<void (net::HttpStreamFactory::Job::*)(), base::WeakPtr<net::HttpStreamFactory::Job>&&>::Invoke<void (net::HttpStreamFactory::Job::*)(), base::WeakPtr<net::HttpStreamFactory::Job> const&>(void (net::HttpStreamFactory::Job::*)(), base::WeakPtr<net::HttpStreamFactory::Job> const&) + 140
34  libnet.dylib                        0x00000001125e0b78 void base::internal::InvokeHelper<true, base::internal::FunctorTraits<void (net::HttpStreamFactory::Job::*&&)(), base::WeakPtr<net::HttpStreamFactory::Job>&&>, void, 0ul>::MakeItSo<void (net::HttpStreamFactory::Job::*)(), std::__Cr::tuple<base::WeakPtr<net::HttpStreamFactory::Job>>>(void (net::HttpStreamFactory::Job::*&&)(), std::__Cr::tuple<base::WeakPtr<net::HttpStreamFactory::Job>>&&) + 104
35  libnet.dylib                        0x00000001125e0b04 void base::internal::Invoker<base::internal::FunctorTraits<void (net::HttpStreamFactory::Job::*&&)(), base::WeakPtr<net::HttpStreamFactory::Job>&&>, base::internal::BindState<true, true, false, void (net::HttpStreamFactory::Job::*)(), base::WeakPtr<net::HttpStreamFactory::Job>>, void ()>::RunImpl<void (net::HttpStreamFactory::Job::*)(), std::__Cr::tuple<base::WeakPtr<net::HttpStreamFactory::Job>>, 0ul>(void (net::HttpStreamFactory::Job::*&&)(), std::__Cr::tuple<base::WeakPtr<net::HttpStreamFactory::Job>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) + 32
36  libnet.dylib                        0x00000001125e0a8c base::internal::Invoker<base::internal::FunctorTraits<void (net::HttpStreamFactory::Job::*&&)(), base::WeakPtr<net::HttpStreamFactory::Job>&&>, base::internal::BindState<true, true, false, void (net::HttpStreamFactory::Job::*)(), base::WeakPtr<net::HttpStreamFactory::Job>>, void ()>::RunOnce(base::internal::BindStateBase*) + 44
37  libbase.dylib                       0x00000001052a8634 base::OnceCallback<void ()>::Run() && + 176
38  libbase.dylib                       0x000000010551eb2c base::TaskAnnotator::RunTaskImpl(base::PendingTask&) + 480
39  libbase.dylib                       0x00000001055a8ac4 _ZN4base13TaskAnnotator7RunTaskIJZNS_16sequence_manager8internal35ThreadControllerWithMessagePumpImpl10DoWorkImplEPNS_7LazyNowEE3$_4EEEvN8perfetto12StaticStringERNS_11PendingTaskEDpOT_ + 144
40  libbase.dylib                       0x00000001055a8428 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) + 1540
41  libbase.dylib                       0x00000001055a7bb8 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() + 240
42  libbase.dylib                       0x00000001057a1010 base::MessagePumpKqueue::RunBatched(base::MessagePump::Delegate*) + 148
43  libbase.dylib                       0x00000001057a0de4 base::MessagePumpKqueue::Run(base::MessagePump::Delegate*) + 124
44  libbase.dylib                       0x00000001055a9260 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) + 592
45  libbase.dylib                       0x0000000105474310 base::RunLoop::Run(base::Location const&) + 628
46  libbase.dylib                       0x000000010564d1f0 base::Thread::Run(base::RunLoop*) + 252
47  libcontent.dylib                    0x00000003000f61e0 content::(anonymous namespace)::ChildIOThread::Run(base::RunLoop*) + 164
48  libbase.dylib                       0x000000010564d6c4 base::Thread::ThreadMain() + 860
49  libbase.dylib                       0x00000001056ba468 base::(anonymous namespace)::ThreadFunc(void*) + 244
50  libsystem_pthread.dylib             0x0000000199b642e4 _pthread_start + 136
51  libsystem_pthread.dylib             0x0000000199b5f0fc thread_start + 8
[end of stack trace]
[87057:14703701:0319/104519.916244:ERROR:google_apis/gcm/engine/connection_factory_impl.cc:483] ConnectionHandler failed with net error: -2
[87057:14703574:0319/104519.925272:ERROR:content/browser/network_service_instance_impl.cc:586] Network service crashed, restarting service.

```

### wf...@chromium.org (2025-03-19)

Thank you for your report. I agree with your conclusions, these checks should probably be in the browser, but I think the impact of this is low as it requires a) a bug to get code exec in the renderer then b) a second bug in the server that could be exploited with this capability - this is therefore highly mitigated to the point of being severity Low.

### wf...@chromium.org (2025-03-19)

ricea, can you take a look at this or find someone who might? This is a LOW severity bug in websocket.

### ch...@google.com (2025-03-20)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ri...@chromium.org (2025-03-21)

I agree with your assessment. Low severity but real issue.

### i....@gmail.com (2025-03-21)

Thank you for triaging it!

### i....@gmail.com (2025-04-11)

Hi, is there any update here?

If it's alright, could I work on a fix? It seems a good opportunity for me as a contributor to learn the browser process code :)

(Since I’ve already landed some patches before, I’m familiar with the contribution and review process.)

### ri...@chromium.org (2025-04-14)

If you could contribute a fix, that would be great! Either network::WebSocket::AddChannel() or net::WebSocketChannel::SendAddChannelRequestWithSuppliedCallback() would be good places to add a check. The former would let you easily call mojo::ReportBadMessage() to terminate the render process that sent the bad message, while the latter is a closer match to how the existing code validates parameters.

### i....@gmail.com (2025-04-20)

thanks!! I will try it and update here soon!

### i....@gmail.com (2025-04-27)

FYI: I submitted the draft and assigned you as the reviewer now :)

### dx...@google.com (2025-07-04)

Project: chromium/src  

Branch: main  

Author: canalun [i.am.kanaru.sato@gmail.com](mailto:i.am.kanaru.sato@gmail.com)  

Link:      <https://chromium-review.googlesource.com/6491749>

Add validation for |Sec-WebSocket-Protocol| request header in browser process.

---


Expand for full commit details
```
     
    The validation logic is the same as the one in renderer. 
     
    Bug: 404573970 
    Change-Id: Ic2152af290f5c18b8d000ba10f856370d175276c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6491749 
    Commit-Queue: Nidhi Jaju <nidhijaju@chromium.org> 
    Reviewed-by: Nidhi Jaju <nidhijaju@chromium.org> 
    Reviewed-by: Adam Rice <ricea@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1482490}

```

---

Files:

- M `net/websockets/websocket_channel.cc`
- M `net/websockets/websocket_channel_test.cc`
- M `services/network/websocket.cc`

---

Hash: b1b9d6e336eb2421e9e520c653453eea896e2a1c  

Date:  Fri Jul 4 08:35:23 2025


---

### i....@gmail.com (2025-08-05)

Hi, if I may, I'd like to ask if this bug is in scope of VRP?

And will it be disclosed after v140 is released?

Thank you :)

### sp...@google.com (2025-10-22)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this
issue does not meet the criteria to qualify for a reward.

Rationale for this decision:

this was determined to be a spec violation and a functional bug

Note that the fact that this issue is not being rewarded does not mean
that the product team won't fix the issue. We have filed a bug with the product
team and they will review your report and decide if a fix is required. We'll
let you know if the issue was fixed.

Regards,   

Google Security Bot

*How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

### ch...@google.com (2026-01-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> this was determined to be a spec violation and a functional bug
> 
> 
> Note that the fact that this issue is not being rewarded does not mean
> that the product team won't fix the issue. We have filed a bug with the product
> team and they will review your report and decide if a fix is required. We'll
> let you know if the issue was fixed.
> 
> Regards, \
> Google Security Bot
> 
> *How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/404573970)*
