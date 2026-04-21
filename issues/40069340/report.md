# Security: UAF in SimpleHostResolverImpl::ResolveHost with chrome

| Field | Value |
|-------|-------|
| **Issue ID** | [40069340](https://issues.chromium.org/issues/40069340) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Network, Internals>Services>Network |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | gr...@google.com |
| **Created** | 2023-08-11 |
| **Bounty** | $7,000.00 |

## Description

VULNERABILITY DETAILS

VERSION
Chrome Version:
Fuzz Test chrome commit
```
commit d9311ec1371882264b48d70ca71d22706801ba76 (HEAD -> main, origin/main, origin/HEAD)
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date:   Tue Aug 8 06:12:42 2023 +0000

    Roll Skia from f7162d33afb2 to 1efbe756a7e0 (1 revision)

    https://skia.googlesource.com/skia.git/+log/f7162d33afb2..1efbe756a7e0

    2023-08-08 skia-autoroll@skia-public.iam.gserviceaccount.com Roll Skia Infra from 0e52994bf1b6 to 333a87d1ef8a (6 revisions)

    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/skia-autoroll
    Please CC kjlubick@google.com,skiabot@google.com on the revert to ensure that a human
    is aware of the problem.

    To file a bug in Skia: https://bugs.chromium.org/p/skia/issues/entry
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

    To report a problem with the AutoRoller itself, please file a bug:
    https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux-blink-rel;luci.chromium.try:linux-chromeos-compile-dbg;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel
    Cq-Do-Not-Cancel-Tryjobs: true
    Bug: chromium:1470711
    Tbr: kjlubick@google.com
    Change-Id: Ia582d9925f0005c16beb16186557767ed940cef1
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4758009
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#1180708}
```
Operating System: Windows


REPRODUCTION CASE
The vulnerability was triggered by my fuzzer, it does not require any interaction. 
I am unable to provide a minimized poc at this time. However, I have provided the ASAN log to assist with the vulnerability fix.


FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: browser
Crash State: see asan log

## Root Cause Analyze

### Create

[0] `StoragePartitionImpl::InitNetworkContext` initializes `network_context_` and creates a `NetworkContextProxy` object, which is saved within `network_context_`.

```cpp
class CONTENT_EXPORT StoragePartitionImpl
 public:
	mojo::Remote<network::mojom::NetworkContext> network_context_; // [0]

...
void StoragePartitionImpl::InitNetworkContext() {
  network::mojom::NetworkContextParamsPtr context_params =
	network_context_.reset();
  CreateNetworkContextInNetworkService(
      network_context_.BindNewPipeAndPassReceiver(), std::move(context_params)); // [0]
  DCHECK(network_context_);
}
```

### Free

[1] `StoragePartitionImpl::InitNetworkContext` registers a disconnect handler.

[2] When this handler is triggered, it will call `StoragePartitionImpl::InitNetworkContext` again, reset `network_context_`, leading to the release of the `NetworkContextProxy` object saved in the previous network_context_.

```cpp
void StoragePartitionImpl::InitNetworkContext() {
	...
	network_context_.reset(); // [2]
	...
	network_context_.set_disconnect_handler(base::BindOnce(
      &StoragePartitionImpl::InitNetworkContext, weak_factory_.GetWeakPtr()));// [1]
}
```

### Use

[3] The constructor of `DirectSocketsServiceImpl` creates a `SimpleHostResolver` and stores it in `resolver_`.

[4] The initialization of `SimpleHostResolver` calls `GetNetworkContext()` to obtain the raw pointer to the `NetworkContext` object saved in `StoragePartitionImpl`, and eventually stores it in its own `network_context_` field.

[5] When a call is made from the rendering process to `GetServiceRemote()->OpenTCPSocket`, such as in the `TCPSocket::Open` function, it will invoke the implementation of `DirectSocketsServiceImpl::OpenTCPSocket` in the browser process.

[6] Due to the possibility that the `network_context_` field in `StoragePartitionImpl` may have been reset earlier, a new `NetworkContext` object is initialized. **This situation causes the `NetworkContext` pointer saved in the `network_context_` field of `SimpleHostResolver` to become invalid, essentially a dangling pointer.** When `DirectSocketsServiceImpl::OpenTCPSocket` calls `resolver_->ResolveHost` and accesses the `network_context_` pointer saved in `SimpleHostResolverImpl`, this ultimately triggers a Use-After-Free (UAF) issue.

```cpp
DirectSocketsServiceImpl::DirectSocketsServiceImpl(
    RenderFrameHost* render_frame_host,
    mojo::PendingReceiver<blink::mojom::DirectSocketsService> receiver)
    : DocumentService(*render_frame_host, std::move(receiver)),
      resolver_(network::SimpleHostResolver::Create(GetNetworkContext())) { // [3]
	...
}

network::mojom::NetworkContext* StoragePartitionImpl::GetNetworkContext() {
  DCHECK(initialized_);
  if (!network_context_.is_bound()) {
    InitNetworkContext();
  }
  return network_context_.get(); // [4]
}

std::unique_ptr<SimpleHostResolver> SimpleHostResolver::Create(
    network::mojom::NetworkContext* network_context) {
  return std::make_unique<SimpleHostResolverImpl>(network_context); // [4]
}

explicit SimpleHostResolverImpl(mojom::NetworkContext* network_context)
      : network_context_(network_context) { // [4]
	...
}

class SimpleHostResolverImpl : public SimpleHostResolver,
                               public ResolveHostClientBase {
	...
  const raw_ptr<mojom::NetworkContext> network_context_; // [4]
};

bool TCPSocket::Open(const String& remote_address,
                     const uint16_t remote_port,
                     const TCPSocketOptions* options,
                     ExceptionState& exception_state) {
	...
  GetServiceRemote()->OpenTCPSocket( // [5]
      std::move(open_tcp_socket_options), std::move(socket_receiver),
      std::move(observer_remote), std::move(callback));
  return true;
}

void DirectSocketsServiceImpl::OpenTCPSocket(
    blink::mojom::DirectTCPSocketOptionsPtr options,
    mojo::PendingReceiver<network::mojom::TCPConnectedSocket> receiver,
    mojo::PendingRemote<network::mojom::SocketObserver> observer,
    OpenTCPSocketCallback callback) {
	...
  resolver_->ResolveHost( // [6]
      network::mojom::HostResolverHost::NewHostPortPair(std::move(remote_addr)),
      net::NetworkAnonymizationKey::CreateTransient(), std::move(parameters),
      base::BindOnce(&DirectSocketsServiceImpl::OnResolveCompleteForTCPSocket,
                     base::Unretained(this), std::move(options),
                     std::move(receiver), std::move(observer),
                     std::move(callback)));
}

void ResolveHost(
    mojom::HostResolverHostPtr host,
    const net::NetworkAnonymizationKey& network_anonymization_key,
    mojom::ResolveHostParametersPtr optional_parameters,
    ResolveHostCallback callback) override {
  ...
  network_context_->ResolveHost(std::move(host), network_anonymization_key, // [6] use here!!!
                                std::move(optional_parameters),
                                receiver.InitWithNewPipeAndPassRemote());
}

```

[0] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:content/browser/storage_partition_impl.cc;l=3302;drc=b86abfa407f3f35d3e5904e76b9a8d3a741bdc8b;

[1] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:content/browser/storage_partition_impl.cc;l=3308;drc=b86abfa407f3f35d3e5904e76b9a8d3a741bdc8b;

[2] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:content/browser/storage_partition_impl.cc;l=3300;drc=b86abfa407f3f35d3e5904e76b9a8d3a741bdc8b;

[3] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:content/browser/direct_sockets/direct_sockets_service_impl.cc;l=213;drc=b86abfa407f3f35d3e5904e76b9a8d3a741bdc8b;

[4] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/storage_partition_impl.cc;l=1605;drc=b86abfa407f3f35d3e5904e76b9a8d3a741bdc8b;

https://source.chromium.org/chromium/chromium/src/+/main:services/network/public/cpp/simple_host_resolver.cc;l=70;drc=b86abfa407f3f35d3e5904e76b9a8d3a741bdc8b;

https://source.chromium.org/chromium/chromium/src/+/main:services/network/public/cpp/simple_host_resolver.cc;l=21;drc=b86abfa407f3f35d3e5904e76b9a8d3a741bdc8b;

https://source.chromium.org/chromium/chromium/src/+/main:services/network/public/cpp/simple_host_resolver.cc;l=63;drc=b86abfa407f3f35d3e5904e76b9a8d3a741bdc8b;

[5] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/direct_sockets/tcp_socket.cc;l=197;drc=b86abfa407f3f35d3e5904e76b9a8d3a741bdc8b;

[6] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/direct_sockets/direct_sockets_service_impl.cc;l=262;drc=b86abfa407f3f35d3e5904e76b9a8d3a741bdc8b;

https://source.chromium.org/chromium/chromium/src/+/main:services/network/public/cpp/simple_host_resolver.cc;l=33;drc=b86abfa407f3f35d3e5904e76b9a8d3a741bdc8b;


## Other

### Network Service Restart

From my Fuzz logs, it is evident that the restart of the Network Service could be related to triggering this vulnerability, as indicated by the following comment:

`[79800:58400:0810/115605.039:ERROR:network_service_instance_impl.cc(657)] Network service crashed, restarting service.`

```
// Returns a raw mojom::NetworkContext pointer. When the network service crashes
// or restarts, the raw pointer will not be valid or safe to use. Therefore,
// the caller should not retain this pointer beyond the same message loop task.
virtual network::mojom::NetworkContext* GetNetworkContext() = 0;
```

https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:content/public/browser/storage_partition.h;l=105;drc=b86abfa407f3f35d3e5904e76b9a8d3a741bdc8b;

### Trigger by MojoJS

Moreover, it's apparent that `DirectSocketsService::OpenTCPSocket` can be triggered from `mojojs`, suggesting that this vulnerability could potentially represent a real-world exploitable sandbox escape vulnerability.

```cpp
map->Add<blink::mojom::DirectSocketsService>(
      base::BindRepeating(&DirectSocketsServiceImpl::CreateForFrame));
```

https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:content/browser/browser_interface_binders.cc;l=1153;drc=b86abfa407f3f35d3e5904e76b9a8d3a741bdc8b;

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 18.1 KB)
- [fuzzlog.txt](attachments/fuzzlog.txt) (text/plain, 65.4 KB)
- [asan.log](attachments/asan.log) (text/plain, 18.1 KB)
- [fuzzlog.txt](attachments/fuzzlog.txt) (text/plain, 65.4 KB)

## Timeline

### [Deleted User] (2023-08-11)

[Empty comment from Monorail migration]

### ki...@gmail.com (2023-08-11)

VULNERABILITY DETAILS

VERSION
Chrome Version:
Fuzz Test chrome commit
```
commit d9311ec1371882264b48d70ca71d22706801ba76 (HEAD -> main, origin/main, origin/HEAD)
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date:   Tue Aug 8 06:12:42 2023 +0000

    Roll Skia from f7162d33afb2 to 1efbe756a7e0 (1 revision)

    https://skia.googlesource.com/skia.git/+log/f7162d33afb2..1efbe756a7e0

    2023-08-08 skia-autoroll@skia-public.iam.gserviceaccount.com Roll Skia Infra from 0e52994bf1b6 to 333a87d1ef8a (6 revisions)

    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/skia-autoroll
    Please CC kjlubick@google.com,skiabot@google.com on the revert to ensure that a human
    is aware of the problem.

    To file a bug in Skia: https://bugs.chromium.org/p/skia/issues/entry
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

    To report a problem with the AutoRoller itself, please file a bug:
    https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux-blink-rel;luci.chromium.try:linux-chromeos-compile-dbg;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel
    Cq-Do-Not-Cancel-Tryjobs: true
    Bug: chromium:1470711
    Tbr: kjlubick@google.com
    Change-Id: Ia582d9925f0005c16beb16186557767ed940cef1
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4758009
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#1180708}
```
Operating System: Windows


REPRODUCTION CASE
The vulnerability was triggered by my fuzzer, it does not require any interaction. 
I am unable to provide a minimized poc at this time. However, I have provided the ASAN log to assist with the vulnerability fix.


FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: browser
Crash State: see asan log

### ki...@gmail.com (2023-08-11)

## Root Cause Analyze

### Create

[0] `StoragePartitionImpl::InitNetworkContext` initializes `network_context_` and creates a `NetworkContextProxy` object, which is saved within `network_context_`.

```cpp
class CONTENT_EXPORT StoragePartitionImpl
 public:
	mojo::Remote<network::mojom::NetworkContext> network_context_; // [0]

...
void StoragePartitionImpl::InitNetworkContext() {
  network::mojom::NetworkContextParamsPtr context_params =
	network_context_.reset();
  CreateNetworkContextInNetworkService(
      network_context_.BindNewPipeAndPassReceiver(), std::move(context_params)); // [0]
  DCHECK(network_context_);
}
```

### Free

[1] `StoragePartitionImpl::InitNetworkContext` registers a disconnect handler.

[2] When this handler is triggered, it will call `StoragePartitionImpl::InitNetworkContext` again, reset `network_context_`, leading to the release of the `NetworkContextProxy` object saved in the previous network_context_.

```cpp
void StoragePartitionImpl::InitNetworkContext() {
	...
	network_context_.reset(); // [2]
	...
	network_context_.set_disconnect_handler(base::BindOnce(
      &StoragePartitionImpl::InitNetworkContext, weak_factory_.GetWeakPtr()));// [1]
}
```

### Use

[3] The constructor of `DirectSocketsServiceImpl` creates a `SimpleHostResolver` and stores it in `resolver_`.

[4] The initialization of `SimpleHostResolver` calls `GetNetworkContext()` to obtain the raw pointer to the `NetworkContext` object saved in `StoragePartitionImpl`, and eventually stores it in its own `network_context_` field.

[5] When a call is made from the rendering process to `GetServiceRemote()->OpenTCPSocket`, such as in the `TCPSocket::Open` function, it will invoke the implementation of `DirectSocketsServiceImpl::OpenTCPSocket` in the browser process.

[6] Due to the possibility that the `network_context_` field in `StoragePartitionImpl` may have been reset earlier, a new `NetworkContext` object is initialized. **This situation causes the `NetworkContext` pointer saved in the `network_context_` field of `SimpleHostResolver` to become invalid, essentially a dangling pointer.** When `DirectSocketsServiceImpl::OpenTCPSocket` calls `resolver_->ResolveHost` and accesses the `network_context_` pointer saved in `SimpleHostResolverImpl`, this ultimately triggers a Use-After-Free (UAF) issue.

```cpp
DirectSocketsServiceImpl::DirectSocketsServiceImpl(
    RenderFrameHost* render_frame_host,
    mojo::PendingReceiver<blink::mojom::DirectSocketsService> receiver)
    : DocumentService(*render_frame_host, std::move(receiver)),
      resolver_(network::SimpleHostResolver::Create(GetNetworkContext())) { // [3]
	...
}

network::mojom::NetworkContext* StoragePartitionImpl::GetNetworkContext() {
  DCHECK(initialized_);
  if (!network_context_.is_bound()) {
    InitNetworkContext();
  }
  return network_context_.get(); // [4]
}

std::unique_ptr<SimpleHostResolver> SimpleHostResolver::Create(
    network::mojom::NetworkContext* network_context) {
  return std::make_unique<SimpleHostResolverImpl>(network_context); // [4]
}

explicit SimpleHostResolverImpl(mojom::NetworkContext* network_context)
      : network_context_(network_context) { // [4]
	...
}

class SimpleHostResolverImpl : public SimpleHostResolver,
                               public ResolveHostClientBase {
	...
  const raw_ptr<mojom::NetworkContext> network_context_; // [4]
};

bool TCPSocket::Open(const String& remote_address,
                     const uint16_t remote_port,
                     const TCPSocketOptions* options,
                     ExceptionState& exception_state) {
	...
  GetServiceRemote()->OpenTCPSocket( // [5]
      std::move(open_tcp_socket_options), std::move(socket_receiver),
      std::move(observer_remote), std::move(callback));
  return true;
}

void DirectSocketsServiceImpl::OpenTCPSocket(
    blink::mojom::DirectTCPSocketOptionsPtr options,
    mojo::PendingReceiver<network::mojom::TCPConnectedSocket> receiver,
    mojo::PendingRemote<network::mojom::SocketObserver> observer,
    OpenTCPSocketCallback callback) {
	...
  resolver_->ResolveHost( // [6]
      network::mojom::HostResolverHost::NewHostPortPair(std::move(remote_addr)),
      net::NetworkAnonymizationKey::CreateTransient(), std::move(parameters),
      base::BindOnce(&DirectSocketsServiceImpl::OnResolveCompleteForTCPSocket,
                     base::Unretained(this), std::move(options),
                     std::move(receiver), std::move(observer),
                     std::move(callback)));
}

void ResolveHost(
    mojom::HostResolverHostPtr host,
    const net::NetworkAnonymizationKey& network_anonymization_key,
    mojom::ResolveHostParametersPtr optional_parameters,
    ResolveHostCallback callback) override {
  ...
  network_context_->ResolveHost(std::move(host), network_anonymization_key, // [6] use here!!!
                                std::move(optional_parameters),
                                receiver.InitWithNewPipeAndPassRemote());
}

```

[0] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:content/browser/storage_partition_impl.cc;l=3302;drc=b86abfa407f3f35d3e5904e76b9a8d3a741bdc8b;

[1] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:content/browser/storage_partition_impl.cc;l=3308;drc=b86abfa407f3f35d3e5904e76b9a8d3a741bdc8b;

[2] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:content/browser/storage_partition_impl.cc;l=3300;drc=b86abfa407f3f35d3e5904e76b9a8d3a741bdc8b;

[3] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:content/browser/direct_sockets/direct_sockets_service_impl.cc;l=213;drc=b86abfa407f3f35d3e5904e76b9a8d3a741bdc8b;

[4] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/storage_partition_impl.cc;l=1605;drc=b86abfa407f3f35d3e5904e76b9a8d3a741bdc8b;

https://source.chromium.org/chromium/chromium/src/+/main:services/network/public/cpp/simple_host_resolver.cc;l=70;drc=b86abfa407f3f35d3e5904e76b9a8d3a741bdc8b;

https://source.chromium.org/chromium/chromium/src/+/main:services/network/public/cpp/simple_host_resolver.cc;l=21;drc=b86abfa407f3f35d3e5904e76b9a8d3a741bdc8b;

https://source.chromium.org/chromium/chromium/src/+/main:services/network/public/cpp/simple_host_resolver.cc;l=63;drc=b86abfa407f3f35d3e5904e76b9a8d3a741bdc8b;

[5] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/direct_sockets/tcp_socket.cc;l=197;drc=b86abfa407f3f35d3e5904e76b9a8d3a741bdc8b;

[6] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/direct_sockets/direct_sockets_service_impl.cc;l=262;drc=b86abfa407f3f35d3e5904e76b9a8d3a741bdc8b;

https://source.chromium.org/chromium/chromium/src/+/main:services/network/public/cpp/simple_host_resolver.cc;l=33;drc=b86abfa407f3f35d3e5904e76b9a8d3a741bdc8b;


## Other

### Network Service Restart

From my Fuzz logs, it is evident that the restart of the Network Service could be related to triggering this vulnerability, as indicated by the following comment:

`[79800:58400:0810/115605.039:ERROR:network_service_instance_impl.cc(657)] Network service crashed, restarting service.`

```
// Returns a raw mojom::NetworkContext pointer. When the network service crashes
// or restarts, the raw pointer will not be valid or safe to use. Therefore,
// the caller should not retain this pointer beyond the same message loop task.
virtual network::mojom::NetworkContext* GetNetworkContext() = 0;
```

https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:content/public/browser/storage_partition.h;l=105;drc=b86abfa407f3f35d3e5904e76b9a8d3a741bdc8b;

### Trigger by MojoJS

Moreover, it's apparent that `DirectSocketsService::OpenTCPSocket` can be triggered from `mojojs`, suggesting that this vulnerability could potentially represent a real-world exploitable sandbox escape vulnerability.

```cpp
map->Add<blink::mojom::DirectSocketsService>(
      base::BindRepeating(&DirectSocketsServiceImpl::CreateForFrame));
```

https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:content/browser/browser_interface_binders.cc;l=1153;drc=b86abfa407f3f35d3e5904e76b9a8d3a741bdc8b;


### pg...@google.com (2023-08-11)

Assuming from "Trigger by MojoJS" that this would require a compromised renderer. A crash in the browser process, though, so setting severity to be high

It is unclear how the bisected commit (d9311ec1371882264b48d70ca71d22706801ba76) mentioned in https://crbug.com/chromium/1472173#c2 exposed this problem though - assigning to @horo from the history of this component bugs and cc'ing others

I haven't been able to reproduce this due to the lack of a POC, but the RCA seems plausible.
- @reporter, can you provide the non-minimized POC for now until you can provide a minimized one? 
- horo@, can you take a look and reroute if necessary?

[Monorail components: Internals>Network Internals>Services>Network]

### pg...@google.com (2023-08-11)

adding needs-feedback label for the non minimized POC for now and a minimized poc when ready

### [Deleted User] (2023-08-11)

[Empty comment from Monorail migration]

### ad...@google.com (2023-08-11)

(I am a bot: this is an auto-cc on a security bug)

### ki...@gmail.com (2023-08-11)

Re https://crbug.com/chromium/1472173#c4
I apologize for any confusion caused. Since my fuzzer does not include mojojs, this vulnerability can be triggered solely through the web API without requiring a patch render. Mentioning mojojs was just to emphasize its exploitability.

Additionally, as this vulnerability was discovered through our fuzzing process, we currently do not have a minimized proof-of-concept (POC) available, which is quite challenging. However, I believe the root cause of this vulnerability has been sufficiently analyzed. Please refer to the ASAN log to assist in fixing it. Thank you.



### ki...@gmail.com (2023-08-11)

Additionally, the commit hash I provided is only the Chromium commit hash when this vulnerability was fuzzed, not for bisecting. Please do not mistakenly assign it. This vulnerability may affect the stable version, and developers need to evaluate it.

### pg...@google.com (2023-08-11)

ahh gotcha that makes more sense (: thank you for clarifying!
Updating FoundIn to 116 as the relevant files have not been updated recently

Setting OS liberally assuming the hostresolver is used by all - @owner, please update if some are certainly not impacted

### [Deleted User] (2023-08-12)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-12)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ho...@chromium.org (2023-08-15)

greengrape@
Could you please handle this?
There seems to be an UAF issue in network::SimpleHostResolver which was introduced by crrev.com/c/4206827.

### [Deleted User] (2023-08-15)

[Empty comment from Monorail migration]

### ki...@gmail.com (2023-08-16)

Hello, any update? Thanks

### gr...@google.com (2023-08-16)

Taking a look.

### gr...@google.com (2023-08-16)

kipreyxx -- thanks for the detailed explanation :) I've drafted a CL at https://chromium-review.googlesource.com/c/chromium/src/+/4783547 to mitigate this.

I'd suggest lowering the priority -- the API in question is not publicly available unless the user deliberately started chrome with the corresponding flag.

### pg...@google.com (2023-08-16)

ah thank you for the info! updating impact per https://crbug.com/chromium/1472173#c17

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### ki...@gmail.com (2023-08-16)

Thanks for your quick fix!

### gi...@appspot.gserviceaccount.com (2023-08-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9ca444b4c937ce9d90852b1e1e8223795ab00812

commit 9ca444b4c937ce9d90852b1e1e8223795ab00812
Author: Andrew Rayskiy <greengrape@google.com>
Date: Wed Aug 16 14:56:21 2023

[DirectSockets] Fix UAF in the host resolution process

The network context associated with StoragePartition might change over
time -- for instance, when the network service crashes. To prevent UAF
in this case, SimpleHostResolver should be created with a network
context factory instead of a single network context pointer.

Bug: 1472173
Change-Id: Ifa8320828be170acd83d06565e6be20f6d964166
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4783547
Reviewed-by: Adam Rice <ricea@chromium.org>
Commit-Queue: Andrew Rayskiy <greengrape@google.com>
Cr-Commit-Position: refs/heads/main@{#1184160}

[modify] https://crrev.com/9ca444b4c937ce9d90852b1e1e8223795ab00812/services/network/public/cpp/simple_host_resolver.h
[modify] https://crrev.com/9ca444b4c937ce9d90852b1e1e8223795ab00812/content/browser/direct_sockets/direct_sockets_service_impl.cc
[modify] https://crrev.com/9ca444b4c937ce9d90852b1e1e8223795ab00812/services/network/public/cpp/simple_host_resolver.cc


### gr...@google.com (2023-08-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-17)

Requesting merge to stable M116 because latest trunk commit (1184160) appears to be after stable branch point (1160321).

Requesting merge to beta M117 because latest trunk commit (1184160) appears to be after beta branch point (1181205).

Merge review required: M116 is already shipping to stable.

Merge review required: M117 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [116, 117].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ki...@gmail.com (2023-08-18)

per https://crbug.com/chromium/1472173#c17, The issue don't need to merge to stable.

### pg...@google.com (2023-08-18)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-09-05)

[Description Changed]

### am...@google.com (2023-09-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-07)

Congratulations, Kiprey! The VRP Panel has decided to award you $7,000 for this report of a mitigated security bug in the browser process, mitigated by precondition to crash / restart the network service. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-09-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1472173?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Network, Internals>Services>Network]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40069340)*
