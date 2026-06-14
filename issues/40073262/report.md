# Security: Race Condition UAF in virtio_transport_space_update

| Field | Value |
|-------|-------|
| **Issue ID** | [40073262](https://issues.chromium.org/issues/40073262) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | da...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-09-24 |
| **Bounty** | $2,000.00 |

## Description

---

### Report description


Security: Race Condition UAF in virtio_transport_space_update


---

### Bug location


#### Which product or website have you found a vulnerability in?

Google Chrome


---

### The problem


#### Please describe the technical details of the vulnerability

Security: Race Condition UAF in virtio_transport_space_update

**VULNERABILITY DETAIL**
The vulnerability is in v5.4 kernel mainline, when calling `sys_connect` with `AF_VSOCK` socket, function `vsock_assign_transport` is called to assign a transport to a socket, it will call `virtio_transport_do_socket_init` to initialize `struct virtio_vsock_sock`[1], and save its pointer in `struct vsock_sock` [2], if `vsk->transport` is already exist, `vsock_assign_transport` will try to release `vsk` and free `vss` [3], so `kmalloc` of `vss` and `kfree(vss)` are both in function `vsock_assign_transport`, and both can be triggered by syscall `connect`. There's a worker thread `vsock_loopback_work`, it will call `virtio_transport_space_update` and get 'vss' from 'vsk' [4]. These two routine is supposed to be protected by `lock_sock(sk);`, but the `kfree(vss)` still can be prior than `virtio_transport_space_update`, making `vss` a dangling pointer and get UAF at [5].

```
int vsock_assign_transport(struct vsock_sock *vsk, struct vsock_sock *psk)
{
	const struct vsock_transport *new_transport;
	struct sock *sk = sk_vsock(vsk);
	unsigned int remote_cid = vsk->remote_addr.svm_cid;
	int ret;

	switch (sk->sk_type) {
	case SOCK_DGRAM:
		new_transport = transport_dgram;
		break;
	case SOCK_STREAM:
		if (vsock_use_local_transport(remote_cid))
			new_transport = transport_local;
		else if (remote_cid <= VMADDR_CID_HOST || !transport_h2g)
			new_transport = transport_g2h;
		else
			new_transport = transport_h2g;
		break;
	default:
		return -ESOCKTNOSUPPORT;
	}

	if (vsk->transport) {
		if (vsk->transport == new_transport)
			return 0;

		/* transport->release() must be called with sock lock acquired.
		 * This path can only be taken during vsock_stream_connect(),
		 * where we have already held the sock lock.
		 * In the other cases, this function is called on a new socket
		 * which is not assigned to any transport.
		 */
		vsk->transport->release(vsk);
		vsock_deassign_transport(vsk);							//<-------------[3]
	}

	/* We increase the module refcnt to prevent the transport unloading
	 * while there are open sockets assigned to it.
	 */
	if (!new_transport || !try_module_get(new_transport->module))
		return -ENODEV;

	ret = new_transport->init(vsk, psk);						//<---------------[1]
	if (ret) {
		module_put(new_transport->module);
		return ret;
	}

	vsk->transport = new_transport;

	return 0;
}
```

```
int virtio_transport_do_socket_init(struct vsock_sock *vsk,
				    struct vsock_sock *psk)
{
	struct virtio_vsock_sock *vvs;

	vvs = kzalloc(sizeof(*vvs), GFP_KERNEL);
	if (!vvs)
		return -ENOMEM;

	vsk->trans = vvs;									//<---------------[2]
	vvs->vsk = vsk;
	if (psk && psk->trans) {
		struct virtio_vsock_sock *ptrans = psk->trans;

		vvs->peer_buf_alloc = ptrans->peer_buf_alloc;
	}

	if (vsk->buffer_size > VIRTIO_VSOCK_MAX_BUF_SIZE)
		vsk->buffer_size = VIRTIO_VSOCK_MAX_BUF_SIZE;

	vvs->buf_alloc = vsk->buffer_size;

	spin_lock_init(&vvs->rx_lock);
	spin_lock_init(&vvs->tx_lock);
	INIT_LIST_HEAD(&vvs->rx_queue);

	return 0;
}
```


```
static bool virtio_transport_space_update(struct sock *sk,
					  struct virtio_vsock_pkt *pkt)
{
	struct vsock_sock *vsk = vsock_sk(sk);
	struct virtio_vsock_sock *vvs = vsk->trans;						// <----------[4]
	bool space_available;

	/* Listener sockets are not associated with any transport, so we are
	 * not able to take the state to see if there is space available in the
	 * remote peer, but since they are only used to receive requests, we
	 * can assume that there is always space available in the other peer.
	 */
	if (!vvs)
		return true;

	/* buf_alloc and fwd_cnt is always included in the hdr */
	spin_lock_bh(&vvs->tx_lock);									//<------------[5]
	vvs->peer_buf_alloc = le32_to_cpu(pkt->hdr.buf_alloc);
	vvs->peer_fwd_cnt = le32_to_cpu(pkt->hdr.fwd_cnt);
	space_available = virtio_transport_has_space(vsk);
	spin_unlock_bh(&vvs->tx_lock);
	return space_available;
}
```

[1] https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.4/net/vmw_vsock/af_vsock.c;l=475

[2] https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.4/net/vmw_vsock/virtio_transport_common.c;l=415

[3] https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.4/net/vmw_vsock/af_vsock.c;l=466

[4] https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.4/net/vmw_vsock/virtio_transport_common.c;l=952

[5] https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.4/net/vmw_vsock/virtio_transport_common.c;l=964



**REPRODUCE**
PoC and Crash log are in the attachment, please compile the poc and run it with a normal user privilege.

In order to make the race condition UAF easily triggered, please add the following patch first:
```
diff --git a/net/vmw_vsock/virtio_transport_common.c b/net/vmw_vsock/virtio_transport_common.c
index b792c0cb783d..e68bf613774d 100644
--- a/net/vmw_vsock/virtio_transport_common.c
+++ b/net/vmw_vsock/virtio_transport_common.c
@@ -1075,6 +1075,7 @@ void virtio_transport_recv_pkt(struct virtio_transport *t,
 
        vsk = vsock_sk(sk);
 
+       mdelay(40);
        lock_sock(sk);
 
        space_available = virtio_transport_space_update(sk, pkt);
```


**PATCH SUGGESTION**
I think make the freed `vss` pointer to NULL can mitigate this issue : 

```
diff --git a/net/vmw_vsock/virtio_transport_common.c b/net/vmw_vsock/virtio_transport_common.c
index b792c0cb783d..b67875a6f628 100644
--- a/net/vmw_vsock/virtio_transport_common.c
+++ b/net/vmw_vsock/virtio_transport_common.c
@@ -627,6 +627,7 @@ void virtio_transport_destruct(struct vsock_sock *vsk)
        struct virtio_vsock_sock *vvs = vsk->trans;
 
        kfree(vvs);
+       vsk->trans = NULL;
 }
 EXPORT_SYMBOL_GPL(virtio_transport_destruct);
```




#### Please briefly explain who can exploit the vulnerability, and what they gain when doing so

Kernel code execution


---

### The cause


#### What version of Chrome have you found the security issue in?

Latest ChromeOS v5.4 kernel


#### Is the security issue related to a crash?

Yes


#### Choose the type of vulnerability

Chrome OS - Firmware Vulnerabilities 




## Attachments

- [vsock.c](attachments/vsock.c) (text/plain, 1.1 KB)
- [crash_log](attachments/crash_log) (text/plain, 3.6 KB)

## Timeline

### da...@gmail.com (2023-09-24)

[Empty comment from Monorail migration]

### ch...@appspot.gserviceaccount.com (2023-09-24)

[Empty comment from Monorail migration]

### do...@chromium.org (2023-09-24)

Routing to ChromeOS triage.

### ch...@google.com (2023-09-25)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/301886931). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed

[Monorail blocking: b/301886931]

### [Deleted User] (2023-09-26)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-26)

Verified by 

jadmanski@google.com.
Exploitability: The current PoC and reproductions depend on injecting some mdelay waits to make it consistent. This doesn't mean it's not exploitable without tweaks, but it is at least somewhat tricky to reproduce on an unmodified build.

Privileges and Capabilities: If you can reproduce this you can get the code to use freed memory as a spinlock; so if you can trigger this you can get writes to the freed memory (although you can't control the values) AND you can get the code to use a spinlock which doesn't work correctly (potentially allowing you to generate more race conditions).

Origin of fix: The bug was fixed incidentally by another patch, however that patch was not picked up for the CrOS kernels, i.e. this is basically a missed patch.

Mitigations: You need to be able to create AF_VSOCK sockets.

Severity assessment: Rating this as high because this race can cause writes to freed memory crossing the userspace -> kernel boundary. And because the freed memory is used as a lock, I think it could reasonably be used to generate additional races. I think there is an argument that this is only medium because a) it's not clear that the timing necessary to exploit this race is really possible to trigger in practice, and b) it probably would have to combined with more race conditions to actually generate some controllable behavior and so may not actually be realistic to exploit it.

### [Deleted User] (2023-10-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-27)

[Empty comment from Monorail migration]

### ch...@google.com (2023-12-12)

[Empty comment from Monorail migration]

### am...@google.com (2023-12-15)

[Empty comment from Monorail migration]

### [Deleted User] (2024-02-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-02-01)

This issue was migrated from crbug.com/chromium/1486350?no_tracker_redirect=1

[Monorail blocking: b/301886931]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40073262)*
