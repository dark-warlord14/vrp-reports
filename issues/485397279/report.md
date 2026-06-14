# Security: Heap-use-after-free in SecureChannelImpl::OnDecryptedResponse

| Field | Value |
|-------|-------|
| **Issue ID** | [485397279](https://issues.chromium.org/issues/485397279) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Privacy |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 144.0.0.0 |
| **Reporter** | me...@gmail.com |
| **Assignee** | du...@chromium.org |
| **Created** | 2026-02-18 |
| **Bounty** | $11,000.00 |

## Description

# Steps to reproduce the problem

1. apply the change.txt to the newest Chromium and compile chrome with ASAN
2. Run chrome with : `./chrome --user-data-dir=/tmp/noexist --enable-features=ZeroStateSuggestionsUseLegion,Legion`
3. Move mouse to the "Ask Gemini" button. (Don't need to click)

**Note that this UAF can be exploited to escape the sandbox without requiring a compromised renderer. The patch I provided only simulates a successful decryption operation to trigger the callback, and does not affect Chromium’s original logic**

**Bisect**
This UAF is introduced in this commit: <https://chromium-review.googlesource.com/c/chromium/src/+/7139550>
According to the commit, this UAF affects Chrome Stable 144.0.7559.59.

# Problem Description

**Vulnerability Analysis**

In the `SecureChannleImpl` class, `response_callback_` deletes the `SecureChannleImpl` instance itself [1]. Therefore, any reference to `|this|` after invoking the callback will result in a use-after-free vulnerability.

[1]

```
void SecureChannelImpl::OnDecryptedResponse(
    const std::optional<Request>& decrypted_response) {
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);

  if (!decrypted_response.has_value()) {
    DLOG(ERROR) << "Failed to decrypt response.";
    FailAllRequestsAndClose(ErrorCode::kDecryptionFailed);
    return;
  }
  DVLOG(1) << "Response decrypted successfully.";

  CHECK(response_callback_);
   response_callback_.Run(base::ok(*decrypted_response)); //@audit: the response_callback_ will delete |this|

  ProcessPendingEncryptionRequests(); 
}

void SecureChannelImpl::ProcessPendingEncryptionRequests() {
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);

  DCHECK_EQ(state_, State::kEstablished);
  if (state_ != State::kEstablished) { //@audit: use after |this| hase been deleted
    return;
  }

```

`SecureChannelImpl` is owned by a `std::unique_ptr` created by `ConnectionBasic` [2], which itself is owned by a `std::unique_ptr` in `ClientImpl` [3][4]. This establishes an ownership chain: `ClientImpl` → `ConnectionBasic` → `SecureChannelImpl`.

`ConnectionBasic` is reset in `ClientImpl::OnConnectionDisconnected()` [5]. This function is registered as a callback in `ConnectionBasic`, which in turn passes `ConnectionBasic::OnResponseReceived` to `SecureChannelImpl` as a callback. When triggered, this callback ultimately deletes `ClientImpl`, thereby destroying `ConnectionBasic` and, consequently, `SecureChannelImpl`.

[2]

```
ConnectionBasic::ConnectionBasic(
    std::unique_ptr<SecureChannel::Factory> secure_channel_factory,
    base::OnceClosure on_disconnect)
    : on_disconnect_(std::move(on_disconnect)) {
  CHECK(secure_channel_factory);
  CHECK(on_disconnect_);

  secure_channel_ = secure_channel_factory->Create(base::BindRepeating(
      &ConnectionBasic::OnResponseReceived, weak_factory_.GetWeakPtr()));
  CHECK(secure_channel_);
}

```

[3]

```
std::unique_ptr<Connection> CreateBasicMetricsTimeoutConnection(
    const GURL& url,
    network::mojom::NetworkContext* network_context,
    LegionLogger* logger,
    base::OnceClosure on_disconnect) {
  auto connection_basic = std::make_unique<ConnectionBasic>(
      std::make_unique<SecureChannelImpl::FactoryImpl>(url, network_context,
                                                       logger),
      std::move(on_disconnect));

  auto connection_metrics =
      std::make_unique<ConnectionMetrics>(std::move(connection_basic));

  auto connection_timeout =
      std::make_unique<ConnectionTimeout>(std::move(connection_metrics));

  return connection_timeout;
}

```

[4]

```
Connection* ClientImpl::GetOrCreateConnection() {
  if (!connection_) {
    connection_ = connection_factory_->Create(base::BindRepeating(
        &ClientImpl::OnConnectionDisconnected, base::Unretained(this)));
  }
  return connection_.get();
}

```

[5]

```
void ClientImpl::OnConnectionDisconnected() {
  logger_->LogInfo(FROM_HERE,
                   "Connection disconnected. Destroying connection.");
  connection_.reset();
}

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:components/legion/secure_channel_impl.cc;l=357>
[2] <https://source.chromium.org/chromium/chromium/src/+/main:components/legion/connection_basic.cc;l=26>
[3] <https://source.chromium.org/chromium/chromium/src/+/main:components/legion/connection_factory_impl.cc;l=33>
[4] <https://source.chromium.org/chromium/chromium/src/+/main:components/legion/client_impl.cc;l=95>
[5] <https://source.chromium.org/chromium/chromium/src/+/main:components/legion/client_impl.cc;l=183>

# Summary

Security: Heap-use-after-free in SecureChannelImpl::OnDecryptedResponse

# Custom Questions

#### Type of crash:

browser

#### Crash state:

=================================================================
==608920==ERROR: AddressSanitizer: heap-use-after-free on address 0x7c1f73a6fca0 at pc 0x5653945f5dc2 bp 0x7ffc213669d0 sp 0x7ffc213669c8
READ of size 4 at 0x7c1f73a6fca0 thread T0 (chrome)
#0 0x5653945f5dc1 in legion::SecureChannelImpl::ProcessPendingEncryptionRequests() components/legion/secure\_channel\_impl.cc:421:7
#1 0x5653945f6ce2 in legion::SecureChannelImpl::OnDecryptedResponse(std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&) components/legion/secure\_channel\_impl.cc:367:3
#2 0x5653945f8980 in base::internal::Invoker<base::internal::FunctorTraits<void (legion::SecureChannelImpl::*&&)(std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&), base::WeakPtr[legion::SecureChannelImpl](javascript:void(0);)&&>, base::internal::BindState<true, true, false, void (legion::SecureChannelImpl::*)(std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&), base::WeakPtr[legion::SecureChannelImpl](javascript:void(0);)>, void (std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&)>::RunOnce(base::internal::BindStateBase\*, std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&) base/functional/bind\_internal.h:740:12
#3 0x565394607987 in base::internal::OnceCallbackHolder<std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&>::Run(std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&) base/functional/callback.h:155:12
#4 0x565394607bc5 in base::internal::Invoker<base::internal::FunctorTraits<void (base::internal::OnceCallbackHolder<std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&>::\* const&)(std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&), std::\_\_Cr::unique\_ptr<base::internal::OnceCallbackHolder<std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&>, std::\_\_Cr::default\_delete<base::internal::OnceCallbackHolder<std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&>>> const&>, base::internal::BindState<true, true, false, void (base::internal::OnceCallbackHolder<std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&>::*)(std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&), std::\_\_Cr::unique\_ptr<base::internal::OnceCallbackHolder<std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&>, std::\_\_Cr::default\_delete<base::internal::OnceCallbackHolder<std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&>>>>, void (std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&)>::Run(base::internal::BindStateBase*, std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&) base/functional/bind\_internal.h:740:12
#5 0x565394603ecb in base::internal::Invoker<base::internal::FunctorTraits<legion::SecureSessionAsyncImpl::Decrypt(oak::session::v1::EncryptedMessage const&, base::OnceCallback<void (std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&)>)::$\_0&&, base::OnceCallback<void (std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&)>&&>, base::internal::BindState<false, false, false, legion::SecureSessionAsyncImpl::Decrypt(oak::session::v1::EncryptedMessage const&, base::OnceCallback<void (std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&)>)::$\_0, base::OnceCallback<void (std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&)>>, void (std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&)>::RunOnce(base::internal::BindStateBase\*, std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&) base/functional/callback.h:155:12
#6 0x565394607212 in mojo::internal::CallbackWithDeleteHelper<void (std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&)>::Run(std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&) base/functional/callback.h:155:12
#7 0x565394607435 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::internal::CallbackWithDeleteHelper<void (std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&)>::*&&)(std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&), std::\_\_Cr::unique\_ptr<mojo::internal::CallbackWithDeleteHelper<void (std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&)>, std::\_\_Cr::default\_delete<mojo::internal::CallbackWithDeleteHelper<void (std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&)>>>&&>, base::internal::BindState<true, true, false, void (mojo::internal::CallbackWithDeleteHelper<void (std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&)>::*)(std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&), std::\_\_Cr::unique\_ptr<mojo::internal::CallbackWithDeleteHelper<void (std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&)>, std::\_\_Cr::default\_delete<mojo::internal::CallbackWithDeleteHelper<void (std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&)>>>>, void (std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&)>::RunOnce(base::internal::BindStateBase\*, std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&) base/functional/bind\_internal.h:740:12
#8 0x56539461ff5d in legion::mojom::OakSession\_Decrypt\_ForwardToCallback::Accept(mojo::Message\*) base/functional/callback.h:155:12
#9 0x7f4ff243391f in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:1079:41
#10 0x7f4ff244a65b in mojo::MessageDispatcher::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/message\_dispatcher.cc:44:19
#11 0x7f4ff2438b64 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:747:20
#12 0x7f4ff2459c1e in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) mojo/public/cpp/bindings/lib/multiplex\_router.cc:1204:42
#13 0x7f4ff245844d in mojo::internal::MultiplexRouter::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/multiplex\_router.cc:790:7
#14 0x7f4ff244a65b in mojo::MessageDispatcher::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/message\_dispatcher.cc:44:19
#15 0x7f4ff241eeff in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase[mojo::MessageHandle](javascript:void(0);)) mojo/public/cpp/bindings/lib/connector.cc:568:49
#16 0x7f4ff242074e in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:629:14
#17 0x7f4ff24201e7 in mojo::Connector::OnWatcherHandleReady(char const\*, unsigned int) mojo/public/cpp/bindings/lib/connector.cc:454:3
#18 0x7f4ff2422dd1 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::\* const&)(char const\*, unsigned int), mojo::Connector\*, char const\* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase\*, unsigned int) base/functional/bind\_internal.h:740:12
#19 0x7f4ff242247e in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const & base/functional/callback.h:343:12
#20 0x7f4ff2422234 in base::internal::Invoker<base::internal::FunctorTraits<void (\* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&) base/functional/bind\_internal.h:673:12
#21 0x7f4ff0767430 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const & base/functional/callback.h:343:12
#22 0x7f4ff0766e0b in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple\_watcher.cc:286:14
#23 0x7f4ff0767e74 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);)&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase\*) base/functional/bind\_internal.h:740:12
#24 0x7f4ff1c8d8b2 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
#25 0x7f4ff1d0ee2e in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) base/task/common/task\_annotator.h:112:5
#26 0x7f4ff1d0de06 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:346:40
#27 0x7f4ff1ee2737 in base::MessagePumpGlib::HandleDispatch() base/message\_loop/message\_pump\_glib.cc:736:46
#28 0x7f4ff1ee5ee2 in base::(anonymous namespace)::WorkSourceDispatch(\_GSource\*, int (*)(void*), void\*) base/message\_loop/message\_pump\_glib.cc:355:43
#29 0x7f4f82e7617c in g\_main\_context\_dispatch (/lib/x86\_64-linux-gnu/libglib-2.0.so.0+0x5217c) (BuildId: 2c1d2f9d4a08c71a36797aeb246ab7ae377934ea)

0x7c1f73a6fca0 is located 32 bytes inside of 144-byte region [0x7c1f73a6fc80,0x7c1f73a6fd10)
freed by thread T0 (chrome) here:
#0 0x56539178f4d2 in operator delete(void\*, unsigned long) (/home/krace/fuzz/chromium/src/out/ui/chrome+0x67e64d2) (BuildId: 3cd4a8fa4a7bd132)
#1 0x5653945e1635 in legion::ConnectionBasic::~ConnectionBasic() gen/third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:74:5
#2 0x5653945e7d07 in legion::ConnectionMetrics::~ConnectionMetrics() gen/third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:74:5
#3 0x5653945edc8c in legion::ConnectionTimeout::~ConnectionTimeout() gen/third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:74:5
#4 0x5653945f0334 in legion::ConnectionTokenAttestation::~ConnectionTokenAttestation() gen/third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:74:5
#5 0x5653945d9f0c in legion::ClientImpl::OnConnectionDisconnected() gen/third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:74:5
#6 0x5653945dd862 in base::internal::Invoker<base::internal::FunctorTraits<void (legion::ClientImpl::\* const&)(), legion::ClientImpl\*>, base::internal::BindState<true, true, false, void (legion::ClientImpl::*)(), base::internal::UnretainedWrapper<legion::ClientImpl, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>>, void ()>::Run(base::internal::BindStateBase*) base/functional/bind\_internal.h:740:12
#7 0x5653945e20de in legion::ConnectionBasic::HandleDisconnect(legion::ErrorCode) base/functional/callback.h:155:12
#8 0x5653945e0f2d in legion::ConnectionBasic::OnResponseReceived(base::expected<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>, legion::ErrorCode>) components/legion/connection\_basic.cc:71:5
#9 0x5653945e297b in void base::internal::DecayedFunctorTraits<void (legion::ConnectionBasic::*)(base::expected<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>, legion::ErrorCode>), base::WeakPtr[legion::ConnectionBasic](javascript:void(0);) const&>::Invoke<void (legion::ConnectionBasic::*)(base::expected<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>, legion::ErrorCode>), base::WeakPtr[legion::ConnectionBasic](javascript:void(0);) const&, base::expected<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>, legion::ErrorCode>>(void (legion::ConnectionBasic::*)(base::expected<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>, legion::ErrorCode>), base::WeakPtr[legion::ConnectionBasic](javascript:void(0);) const&, base::expected<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>, legion::ErrorCode>&&) base/functional/bind\_internal.h:740:12
#10 0x5653945e26b2 in base::internal::Invoker<base::internal::FunctorTraits<void (legion::ConnectionBasic::* const&)(base::expected<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>, legion::ErrorCode>), base::WeakPtr[legion::ConnectionBasic](javascript:void(0);) const&>, base::internal::BindState<true, true, false, void (legion::ConnectionBasic::*)(base::expected<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>, legion::ErrorCode>), base::WeakPtr[legion::ConnectionBasic](javascript:void(0);)>, void (base::expected<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>, legion::ErrorCode>)>::Run(base::internal::BindStateBase*, base::expected<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>, legion::ErrorCode>&&) base/functional/bind\_internal.h:956:5
#11 0x5653945f712f in base::RepeatingCallback<void (base::expected<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>, legion::ErrorCode>)>::Run(base::expected<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>, legion::ErrorCode>) const & base/functional/callback.h:343:12
#12 0x5653945f6ca5 in legion::SecureChannelImpl::OnDecryptedResponse(std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&) components/legion/secure\_channel\_impl.cc:365:22
#13 0x5653945f8980 in base::internal::Invoker<base::internal::FunctorTraits<void (legion::SecureChannelImpl::*&&)(std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&), base::WeakPtr[legion::SecureChannelImpl](javascript:void(0);)&&>, base::internal::BindState<true, true, false, void (legion::SecureChannelImpl::*)(std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&), base::WeakPtr[legion::SecureChannelImpl](javascript:void(0);)>, void (std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&)>::RunOnce(base::internal::BindStateBase\*, std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&) base/functional/bind\_internal.h:740:12
#14 0x565394607987 in base::internal::OnceCallbackHolder<std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&>::Run(std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&) base/functional/callback.h:155:12
#15 0x565394607bc5 in base::internal::Invoker<base::internal::FunctorTraits<void (base::internal::OnceCallbackHolder<std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&>::\* const&)(std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&), std::\_\_Cr::unique\_ptr<base::internal::OnceCallbackHolder<std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&>, std::\_\_Cr::default\_delete<base::internal::OnceCallbackHolder<std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&>>> const&>, base::internal::BindState<true, true, false, void (base::internal::OnceCallbackHolder<std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&>::*)(std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&), std::\_\_Cr::unique\_ptr<base::internal::OnceCallbackHolder<std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&>, std::\_\_Cr::default\_delete<base::internal::OnceCallbackHolder<std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&>>>>, void (std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&)>::Run(base::internal::BindStateBase*, std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&) base/functional/bind\_internal.h:740:12
#16 0x565394603ecb in base::internal::Invoker<base::internal::FunctorTraits<legion::SecureSessionAsyncImpl::Decrypt(oak::session::v1::EncryptedMessage const&, base::OnceCallback<void (std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&)>)::$\_0&&, base::OnceCallback<void (std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&)>&&>, base::internal::BindState<false, false, false, legion::SecureSessionAsyncImpl::Decrypt(oak::session::v1::EncryptedMessage const&, base::OnceCallback<void (std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&)>)::$\_0, base::OnceCallback<void (std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&)>>, void (std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&)>::RunOnce(base::internal::BindStateBase\*, std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&) base/functional/callback.h:155:12
#17 0x565394607212 in mojo::internal::CallbackWithDeleteHelper<void (std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&)>::Run(std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&) base/functional/callback.h:155:12
#18 0x565394607435 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::internal::CallbackWithDeleteHelper<void (std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&)>::*&&)(std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&), std::\_\_Cr::unique\_ptr<mojo::internal::CallbackWithDeleteHelper<void (std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&)>, std::\_\_Cr::default\_delete<mojo::internal::CallbackWithDeleteHelper<void (std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&)>>>&&>, base::internal::BindState<true, true, false, void (mojo::internal::CallbackWithDeleteHelper<void (std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&)>::*)(std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&), std::\_\_Cr::unique\_ptr<mojo::internal::CallbackWithDeleteHelper<void (std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&)>, std::\_\_Cr::default\_delete<mojo::internal::CallbackWithDeleteHelper<void (std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&)>>>>, void (std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&)>::RunOnce(base::internal::BindStateBase\*, std::\_\_Cr::optional<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>> const&) base/functional/bind\_internal.h:740:12
#19 0x56539461ff5d in legion::mojom::OakSession\_Decrypt\_ForwardToCallback::Accept(mojo::Message\*) base/functional/callback.h:155:12
#20 0x7f4ff243391f in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:1079:41
#21 0x7f4ff244a65b in mojo::MessageDispatcher::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/message\_dispatcher.cc:44:19
#22 0x7f4ff2438b64 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:747:20
#23 0x7f4ff2459c1e in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) mojo/public/cpp/bindings/lib/multiplex\_router.cc:1204:42
#24 0x7f4ff245844d in mojo::internal::MultiplexRouter::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/multiplex\_router.cc:790:7
#25 0x7f4ff244a65b in mojo::MessageDispatcher::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/message\_dispatcher.cc:44:19
#26 0x7f4ff241eeff in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase[mojo::MessageHandle](javascript:void(0);)) mojo/public/cpp/bindings/lib/connector.cc:568:49
#27 0x7f4ff242074e in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:629:14
#28 0x7f4ff24201e7 in mojo::Connector::OnWatcherHandleReady(char const\*, unsigned int) mojo/public/cpp/bindings/lib/connector.cc:454:3
#29 0x7f4ff2422dd1 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::\* const&)(char const\*, unsigned int), mojo::Connector\*, char const\* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase\*, unsigned int) base/functional/bind\_internal.h:740:12

previously allocated by thread T0 (chrome) here:
#0 0x56539178e8cd in operator new(unsigned long) (/home/krace/fuzz/chromium/src/out/ui/chrome+0x67e58cd) (BuildId: 3cd4a8fa4a7bd132)
#1 0x5653945f3b60 in legion::SecureChannelImpl::FactoryImpl::Create(base::RepeatingCallback<void (base::expected<std::\_\_Cr::vector<unsigned char, std::\_\_Cr::allocator<unsigned char>>, legion::ErrorCode>)>) gen/third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:756:26
#2 0x5653945e0692 in legion::ConnectionBasic::ConnectionBasic(std::\_\_Cr::unique\_ptr<legion::SecureChannel::Factory, std::\_\_Cr::default\_delete[legion::SecureChannel::Factory](javascript:void(0);)>, base::OnceCallback<void ()>) components/legion/connection\_basic.cc:26:45
#3 0x5653945e61f3 in legion::(anonymous namespace)::CreateTokenAttestationConnection(GURL const&, legion::phosphor::TokenManager\*, base::RepeatingCallback<void ()>, network::mojom::NetworkContext\*) gen/third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:756:30
#4 0x5653945e5f14 in legion::TokenConnectionFactoryImpl::Create(base::RepeatingCallback<void ()>) components/legion/connection\_factory\_impl.cc:101:10
#5 0x5653945d9c96 in legion::ClientImpl::GetOrCreateConnection() components/legion/client\_impl.cc:90:40
#6 0x5653945d98dd in legion::ClientImpl::EstablishSession(base::OnceCallback<void (base::expected<void, legion::ErrorCode>)>) components/legion/client\_impl.cc:84:3
#7 0x56539ec13bc6 in TabStripActionContainer::OnGlicButtonHovered() chrome/browser/ui/views/tabs/tab\_strip\_action\_container.cc:99:17
#8 0x56539ec1b8c2 in base::internal::Invoker<base::internal::FunctorTraits<void (TabStripActionContainer::\* const&)(), TabStripActionContainer\*>, base::internal::BindState<true, true, false, void (TabStripActionContainer::*)(), base::internal::UnretainedWrapper<TabStripActionContainer, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>>, void ()>::Run(base::internal::BindStateBase*) base/functional/bind\_internal.h:740:12
#9 0x565391f2accf in base::RepeatingCallback<void ()>::Run() const & base/functional/callback.h:343:12
#10 0x565397089f4e in glic::TabStripGlicButton::StateChanged(views::Button::ButtonState) chrome/browser/ui/views/tabs/glic/tab\_strip\_glic\_button.cc:475:25
#11 0x7f4fc1dfc1d9 in views::Button::SetState(views::Button::ButtonState) ui/views/controls/button/button.cc:263:3
#12 0x7f4feca86fd4 in ui::ScopedTargetHandler::OnEvent(ui::Event\*) ui/events/scoped\_target\_handler.cc:30:24
#13 0x7f4feca6e308 in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ui/events/event\_dispatcher.cc:189:12
#14 0x7f4feca6ce6b in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:138:5
#15 0x7f4feca6c5c4 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:84:14
#16 0x7f4feca6c0fa in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:56:15
#17 0x7f4fc2100a96 in views::internal::RootView::HandleMouseEnteredOrMoved(ui::MouseEvent const&) ui/views/widget/root\_view.cc:912:13
#18 0x7f4fc21320e0 in views::Widget::OnMouseEvent(ui::MouseEvent\*) ui/views/widget/widget.cc
#19 0x7f4fc2200b95 in views::DesktopNativeWidgetAura::OnMouseEvent(ui::MouseEvent\*) ui/views/widget/desktop\_aura/desktop\_native\_widget\_aura.cc:1445:30
#20 0x7f4feca6e308 in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ui/events/event\_dispatcher.cc:189:12
#21 0x7f4feca6ce6b in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:138:5
#22 0x7f4feca6c5c4 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:84:14
#23 0x7f4feca6c0fa in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:56:15
#24 0x7f4feca74aaf in ui::EventProcessor::OnEventFromSource(ui::Event\*) ui/events/event\_processor.cc:72:19
#25 0x7f4feca78051 in ui::EventSource::DeliverEventToSink(ui::Event\*) ui/events/event\_source.cc:119:16
#26 0x7f4feca779f4 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const\*, ui::EventRewriter const\*) ui/events/event\_source.cc:134:12
#27 0x7f4fd1706fbd in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event\*) ui/aura/window\_tree\_host\_platform.cc:300:38
#28 0x7f4fc2208d38 in views::DesktopWindowTreeHostLinux::DispatchEvent(ui::Event\*) ui/views/widget/desktop\_aura/desktop\_window\_tree\_host\_linux.cc:250:29
#29 0x7f4ff2c31487 in base::internal::Invoker<base::internal::FunctorTraits<void (ui::PlatformWindowDelegate::*&&)(ui::Event*), ui::PlatformWindowDelegate\*>, base::internal::BindState<true, true, false, void (ui::PlatformWindowDelegate::*)(ui::Event*), base::internal::UnretainedWrapper<ui::PlatformWindowDelegate, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>>, void (ui::Event\*)>::RunOnce(base::internal::BindStateBase\*, ui::Event\*) base/functional/bind\_internal.h:740:12

SUMMARY: AddressSanitizer: heap-use-after-free components/legion/secure\_channel\_impl.cc:421:7 in legion::SecureChannelImpl::ProcessPendingEncryptionRequests()
Shadow bytes around the buggy address:
0x7c1f73a6fa00: f7 fa fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x7c1f73a6fa80: fd fd fd fa fa fa fa fa fa fa f7 fa fd fd fd fd
0x7c1f73a6fb00: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa
0x7c1f73a6fb80: fa fa fa fa f7 fa fd fd fd fd fd fd fd fd fd fd
0x7c1f73a6fc00: fd fd fd fd fd fd fd fa fa fa fa fa fa fa f7 fa
=>0x7c1f73a6fc80: fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd
0x7c1f73a6fd00: fd fd fa fa fa fa fa fa f7 fa fd fd fd fd fd fd
0x7c1f73a6fd80: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa
0x7c1f73a6fe00: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
0x7c1f73a6fe80: fd fd fd fd fd fd fa fa fa fa fa fa f7 fa fd fd
0x7c1f73a6ff00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
Shadow byte legend (one shadow byte represents 8 application bytes):
Addressable: 00
Partially addressable: 01 02 03 04 05 06 07
Heap left redzone: fa
Freed heap region: fd
Stack left redzone: f1
Stack mid redzone: f2
Stack right redzone: f3
Stack after return: f5
Stack use after scope: f8
Global redzone: f9
Global init order: f6
Poisoned by user: f7
Container overflow: fc
Array cookie: ac
Intra object redzone: bb
ASan internal: fe
Left alloca redzone: ca
Right alloca redzone: cb

==608920==ADDITIONAL INFO

==608920==Note: Please include this section with the ASan report.
Task trace:
#0 0x7f4ff076782a in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) mojo/public/cpp/system/simple\_watcher.cc:103:13

Command line: `/home/krace/fuzz/chromium/src/out/ui/chrome --user-data-dir=/tmp/noexist --enable-features=ZeroStateSuggestionsUseLegion,Legion --flag-switches-begin --flag-switches-end --ozone-platform=x11`

MiraclePtr Status: NOT PROTECTED
No raw\_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to <https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md> for details.

==608920==END OF ADDITIONAL INFO

==608920==ABORTING

#### Reporter credit:

Please only credit: Krace

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A \

## Attachments

- [change.txt](attachments/change.txt) (text/plain, 3.5 KB)
- change.txt (text/plain, 4.0 KB)

## Timeline

### me...@gmail.com (2026-02-18)

Sorry, please use this change.txt

### an...@chromium.org (2026-02-18)

[security shepherd]: Thanks for the report! Assigning this to owner of the directory. @du...@chromium.org , would you be able to confirm this UAF? Also, I'm not entirely sure which Chromium component the directory falls under, so if you are able to assign that as well, that'd be great. Thanks!

### du...@chromium.org (2026-02-19)

Thanks for the report. OnDecryptedResponse is bound to a weak_ptr, so I'm not quite sure how it would get invoked after SecureChannelImpl is destroyed?
https://source.chromium.org/chromium/chromium/src/+/main:components/private_ai/secure_channel_impl.cc;l=354;drc=dbefe14f890716a7ca5a58a709cd774118b2660f

### me...@gmail.com (2026-02-19)

The SecureChannelImpl is destroyed at the line 371. <https://source.chromium.org/chromium/chromium/src/+/main:components/private_ai/secure_channel_impl.cc;l=371;drc=dbefe14f890716a7ca5a58a709cd774118b2660f>
After `OnDecryptedResponse` is invoked, `response_callback_` destroys the `SecureChannelImpl` instance. In other words, `SecureChannelImpl` is destroyed *as a result of* running `OnDecryptedResponse`, not before the function is called.

```
void SecureChannelImpl::OnDecryptedResponse(
    const std::optional<Request>& decrypted_response) {
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);

  if (!decrypted_response.has_value()) {
    logger_->LogError(FROM_HERE, "Failed to decrypt response.");
    FailAllRequestsAndClose(ErrorCode::kDecryptionFailed);
    return;
  }
  DVLOG(1) << "Response decrypted successfully.";

  CHECK(response_callback_);
  response_callback_.Run(base::ok(*decrypted_response));  // destroyed here

  ProcessPendingEncryptionRequests();  // used here
}

```

### ch...@google.com (2026-02-19)

Setting milestone because of s2 severity.

### ch...@google.com (2026-02-19)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### du...@chromium.org (2026-02-19)

Thanks, that makes sense. I created a CL to destroy the connection object asynchronously. That should avoid any use-after-free in logic that happens after a disconnect is triggered: https://crrev.com/c/7594013
I updated the milestone to 147 since the feature is still under development and not rolled out to anyone yet.

### dx...@google.com (2026-02-19)

Project: chromium/src  

Branch:  main  

Author:  Christian Dullweber [dullweber@chromium.org](mailto:dullweber@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7594013>

Legion: prevent use-after-free on disconnect

---


Expand for full commit details
```
     
    Destroy Connection asynchronously to prevent use-after-free in logic 
    that runs after the disconnect callback is called. 
     
    Bug: 485397279 
    Change-Id: Id6e98ccdf3c811c7c81d870f02e2cebc5000c6a6 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7594013 
    Commit-Queue: Oleh Lamzin <lamzin@google.com> 
    Reviewed-by: Oleh Lamzin <lamzin@google.com> 
    Auto-Submit: Christian Dullweber <dullweber@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1587237}

```

---

Files:

- M `components/private_ai/client_impl.cc`
- M `components/private_ai/client_impl_unittest.cc`
- M `components/private_ai/testing/fake_connection.cc`
- M `components/private_ai/testing/fake_connection.h`

---

Hash: [e9d98e66790f540f797a277de2c8f76e82a36664](https://chromiumdash.appspot.com/commit/e9d98e66790f540f797a277de2c8f76e82a36664)  

Date: Thu Feb 19 17:56:48 2026


---

### du...@chromium.org (2026-02-19)

Fixed, thanks for the report!
I'm curious how this could be exploited since the uaf happens immediately after the object is freed and the disconnect can't be triggered by an attacker?

### me...@gmail.com (2026-02-20)

One possible exploit is to use a Mojo interface to perform heap spraying in another thread. This has the potential to allocate the freed memory immediately after it is released, thus deploying the memory for exploitation before UAF occurs.

### dx...@google.com (2026-02-25)

Project: chromium/src  

Branch:  main  

Author:  Christian Dullweber [dullweber@chromium.org](mailto:dullweber@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7602453>

Legion: Clear disconnect handler on destroy

---


Expand for full commit details
```
     
    Ensure that we only call one disconnect handler per disconnect. 
    Add integration tests for the whole ClientImpl+Connection stack. 
     
    Bug: 485397279 
    Change-Id: I58498cdf00eb68836bf272bf0b2a25f32ef760b7 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7602453 
    Commit-Queue: Christian Dullweber <dullweber@chromium.org> 
    Reviewed-by: Oleh Lamzin <lamzin@google.com> 
    Auto-Submit: Christian Dullweber <dullweber@chromium.org> 
    Commit-Queue: Oleh Lamzin <lamzin@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1590168}

```

---

Files:

- M `components/private_ai/BUILD.gn`
- A `components/private_ai/client_impl_integration_test.cc`
- M `components/private_ai/connection.h`
- M `components/private_ai/connection_basic.cc`
- M `components/private_ai/connection_basic.h`
- M `components/private_ai/connection_basic_unittest.cc`
- M `components/private_ai/connection_metrics.cc`
- M `components/private_ai/connection_proxy.cc`
- M `components/private_ai/connection_proxy.h`
- M `components/private_ai/connection_timeout.cc`
- M `components/private_ai/connection_token_attestation.cc`
- M `components/private_ai/connection_token_attestation.h`
- M `components/private_ai/testing/fake_connection.cc`
- A `components/private_ai/testing/fake_secure_channel.cc`
- A `components/private_ai/testing/fake_secure_channel.h`

---

Hash: [a05183da7089f1b2cedf6eab0ac1e92499309761](https://chromiumdash.appspot.com/commit/a05183da7089f1b2cedf6eab0ac1e92499309761)  

Date: Wed Feb 25 15:37:17 2026


---

### dx...@google.com (2026-02-25)

Project: chromium/src  

Branch:  main  

Author:  Joshua Pawlicki [waffles@chromium.org](mailto:waffles@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7608109>

Revert "Legion: Clear disconnect handler on destroy"

---


Expand for full commit details
```
     
    This reverts commit a05183da7089f1b2cedf6eab0ac1e92499309761. 
     
    Reason for revert: msan failures due to use of uninitialized value 
     
    Uninitialized value was stored to memory at 
        #0 0x5555791db917 in private_ai::ClientImplIntegrationTest::on_secure_channel_destroyed(private_ai::FakeSecureChannel*) 
     
    https://luci-milo.appspot.com/ui/inv/build-8688879230713537553/test-results?q=ClientImplIntegrationTest.AttestationFailure 
     
    Specifically it looks like the system might need to be attentive to 
    the order in which members of the text fixture are destroyed. 
     
    Original change's description: 
    > Legion: Clear disconnect handler on destroy 
    > 
    > Ensure that we only call one disconnect handler per disconnect. 
    > Add integration tests for the whole ClientImpl+Connection stack. 
    > 
    > Bug: 485397279 
    > Change-Id: I58498cdf00eb68836bf272bf0b2a25f32ef760b7 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7602453 
    > Commit-Queue: Christian Dullweber <dullweber@chromium.org> 
    > Reviewed-by: Oleh Lamzin <lamzin@google.com> 
    > Auto-Submit: Christian Dullweber <dullweber@chromium.org> 
    > Commit-Queue: Oleh Lamzin <lamzin@google.com> 
    > Cr-Commit-Position: refs/heads/main@{#1590168} 
     
    Bug: 485397279 
    Change-Id: If930f3c4551e4d6b08d5df8df7ceabe6d72eeacc 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7608109 
    Auto-Submit: Joshua Pawlicki <waffles@chromium.org> 
    Owners-Override: Joshua Pawlicki <waffles@chromium.org> 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1590451}

```

---

Files:

- M `components/private_ai/BUILD.gn`
- D `components/private_ai/client_impl_integration_test.cc`
- M `components/private_ai/connection.h`
- M `components/private_ai/connection_basic.cc`
- M `components/private_ai/connection_basic.h`
- M `components/private_ai/connection_basic_unittest.cc`
- M `components/private_ai/connection_metrics.cc`
- M `components/private_ai/connection_proxy.cc`
- M `components/private_ai/connection_proxy.h`
- M `components/private_ai/connection_timeout.cc`
- M `components/private_ai/connection_token_attestation.cc`
- M `components/private_ai/connection_token_attestation.h`
- M `components/private_ai/testing/fake_connection.cc`
- D `components/private_ai/testing/fake_secure_channel.cc`
- D `components/private_ai/testing/fake_secure_channel.h`

---

Hash: [c63cf223b3be08bbdf48f509588fbee9d08e1ca1](https://chromiumdash.appspot.com/commit/c63cf223b3be08bbdf48f509588fbee9d08e1ca1)  

Date: Wed Feb 25 23:15:20 2026


---

### dx...@google.com (2026-02-26)

Project: chromium/src  

Branch:  main  

Author:  Christian Dullweber [dullweber@chromium.org](mailto:dullweber@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7610708>

Reland "Legion: Clear disconnect handler on destroy"

---


Expand for full commit details
```
     
    This is a reland of commit a05183da7089f1b2cedf6eab0ac1e92499309761 
     
    Original change's description: 
    > Legion: Clear disconnect handler on destroy 
    > 
    > Ensure that we only call one disconnect handler per disconnect. 
    > Add integration tests for the whole ClientImpl+Connection stack. 
    > 
    > Bug: 485397279 
    > Change-Id: I58498cdf00eb68836bf272bf0b2a25f32ef760b7 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7602453 
    > Commit-Queue: Christian Dullweber <dullweber@chromium.org> 
    > Reviewed-by: Oleh Lamzin <lamzin@google.com> 
    > Auto-Submit: Christian Dullweber <dullweber@chromium.org> 
    > Commit-Queue: Oleh Lamzin <lamzin@google.com> 
    > Cr-Commit-Position: refs/heads/main@{#1590168} 
     
    Cq-Include-Trybots: luci.chromium.try:linux_chromium_msan_rel_ng 
    Bug: 485397279 
    Change-Id: Ia3acb8b62a318e62f991bdf15e5d31ee0337bf90 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7610708 
    Auto-Submit: Christian Dullweber <dullweber@chromium.org> 
    Reviewed-by: Oleh Lamzin <lamzin@google.com> 
    Commit-Queue: Christian Dullweber <dullweber@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1590816}

```

---

Files:

- M `components/private_ai/BUILD.gn`
- A `components/private_ai/client_impl_integration_test.cc`
- M `components/private_ai/connection.h`
- M `components/private_ai/connection_basic.cc`
- M `components/private_ai/connection_basic.h`
- M `components/private_ai/connection_basic_unittest.cc`
- M `components/private_ai/connection_metrics.cc`
- M `components/private_ai/connection_proxy.cc`
- M `components/private_ai/connection_proxy.h`
- M `components/private_ai/connection_timeout.cc`
- M `components/private_ai/connection_token_attestation.cc`
- M `components/private_ai/connection_token_attestation.h`
- M `components/private_ai/testing/fake_connection.cc`
- A `components/private_ai/testing/fake_secure_channel.cc`
- A `components/private_ai/testing/fake_secure_channel.h`

---

Hash: [84d05b258ef82a9d3f0a2317167868861f7cea66](https://chromiumdash.appspot.com/commit/84d05b258ef82a9d3f0a2317167868861f7cea66)  

Date: Thu Feb 26 15:48:00 2026


---

### sp...@google.com (2026-03-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
mildly mitigated browser memory corruption with a bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/485397279)*
