# UAF in gsm_cleanup_mux

| Field | Value |
|-------|-------|
| **Issue ID** | [40067327](https://issues.chromium.org/issues/40067327) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-07-13 |
| **Bounty** | $1,500.00 |

## Description

**Steps to reproduce the problem:**  

will attach details soon.

**Problem Description:**  

UAF in kernel

**Additional Comments:**

\*\*Chrome version: \*\* Kernel 5.10 \*\*Channel: \*\* Stable

**OS:** Chrome OS

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2023-07-13)

[Empty comment from Monorail migration]

### he...@gmail.com (2023-07-13)

Use after free in gsm_cleanup_mux

# detail 

vfs_ioctl/gsmld_ioctl will call *gsm_config* to config the gsm using `gsm_config`. If `need_restart` or `need_close` is set according to the new config, it will call `gsm_cleanup_mux` [1] with `disc` parameter set as `true`.

```
static int gsm_config(struct gsm_mux *gsm, struct gsm_config *c)
{
	int ret = 0;
	int need_close = 0;
	int need_restart = 0;
...
	if (c->t1 != 0 && c->t1 != gsm->t1)
		need_restart = 1;
	if (c->t2 != 0 && c->t2 != gsm->t2)
		need_restart = 1;
	if (c->encapsulation != gsm->encoding)
		need_restart = 1;
	if (c->adaption != gsm->adaption)
		need_restart = 1;
	/* Requires care */
	if (c->initiator != gsm->initiator)
		need_close = 1;
	if (c->mru != gsm->mru)
		need_restart = 1;
	if (c->mtu != gsm->mtu)
		need_restart = 1;

...
	if (need_close || need_restart)
		gsm_cleanup_mux(gsm, true); // [1]
```

In `gsm_cleanup_mux`, it will try to release all `gsm->dlci[i]` using `gsm_dlci_release` [2]. (The `gsm_dlci_release` may free the actual `dlci` later, please see kasan.txt for detail). However, `gsm_cleanup_mux` doesn't set the element pointer of `gsm->dlci` to NULL after calling the `gsm_dlci_release`. This is problematic if we trigger the `gsm_cleanup_mux` function again after the `gsm->dlci[0]` freed, this would cause UAF while accessing the `gsm->dlci[0]` (i.e., dlci) in [4], since the freed pointer doesn't be NULL-ed properly.


```
static void gsm_cleanup_mux(struct gsm_mux *gsm, bool disc)
{
	int i;
	struct gsm_dlci *dlci = gsm->dlci[0];
	struct gsm_msg *txq, *ntxq;

	gsm->dead = true;
	mutex_lock(&gsm->mutex);

	if (dlci) {
		if (disc && dlci->state != DLCI_CLOSED) { // ---------- [4] UAF here
			gsm_dlci_begin_close(dlci);
			wait_event(gsm->event, dlci->state == DLCI_CLOSED);
		}
		dlci->dead = true;
	}

	/* Finish outstanding timers, making sure they are done */
	del_timer_sync(&gsm->t2_timer);

	/* Free up any link layer users and finally the control channel */
	for (i = NUM_DLCI - 1; i >= 0; i--)
		if (gsm->dlci[i])
			gsm_dlci_release(gsm->dlci[i]); // ---------- [2]
	mutex_unlock(&gsm->mutex);
	/* Now wipe the queues */
	tty_ldisc_flush(gsm->tty);
	list_for_each_entry_safe(txq, ntxq, &gsm->tx_list, list)
		kfree(txq);
	INIT_LIST_HEAD(&gsm->tx_list);
}
```

```
/**
 *	gsm_dlci_release		-	release DLCI
 *	@dlci: DLCI to destroy
 *
 *	Release a DLCI. Actual free is deferred until either
 *	mux is closed or tty is closed - whichever is last.
 *
 *	Can sleep.
 */
static void gsm_dlci_release(struct gsm_dlci *dlci)
{
	struct tty_struct *tty = tty_port_tty_get(&dlci->port);
	if (tty) {
		mutex_lock(&dlci->mutex);
		gsm_destroy_network(dlci);
		mutex_unlock(&dlci->mutex);

		/* We cannot use tty_hangup() because in tty_kref_put() the tty
		 * driver assumes that the hangup queue is free and reuses it to
		 * queue release_one_tty() -> NULL pointer panic in
		 * process_one_work().
		 */
		tty_vhangup(tty);

		tty_port_tty_set(&dlci->port, NULL);
		tty_kref_put(tty);
	}
	dlci->state = DLCI_CLOSED;
	dlci_put(dlci); // -------- [3] free pointer though dlci_put -> tty_port_put -> kref_put -> tty_port_destructor -> gsm_dlci_free 
}
```

[Additional note] The actual free stack of the `gsm_dlci_release` from the `kasan2.txt`:
```
 kfree+0xb8/0x19c mm/slab_common.c:1015
 gsm_dlci_free+0x11c/0x168 drivers/tty/n_gsm.c:2671
 tty_port_destructor drivers/tty/tty_port.c:296 [inline]
 kref_put include/linux/kref.h:65 [inline]
 tty_port_put+0xfc/0x190 drivers/tty/tty_port.c:311
 dlci_put drivers/tty/n_gsm.c:2681 [inline]
 gsm_dlci_release drivers/tty/n_gsm.c:2714 [inline]
```


 [1] https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.10/drivers/tty/n_gsm.c;l=2410-2411;drc=a16293af64a1f558dab9a5dd7fb05fdbc2b7c5c0

 [2] https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.10/drivers/tty/n_gsm.c;l=2181-2182;drc=a16293af64a1f558dab9a5dd7fb05fdbc2b7c5c0

 [3] https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.10/drivers/tty/n_gsm.c;l=1804-1812;drc=a16293af64a1f558dab9a5dd7fb05fdbc2b7c5c0

 [4] https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.10/drivers/tty/n_gsm.c;l=2168-2169;drc=a16293af64a1f558dab9a5dd7fb05fdbc2b7c5c0

# bisect

 https://source.chromium.org/chromiumos/_/chromium/chromiumos/third_party/kernel/+/47132f9f7f766718513625982468f7f1339ca666

This affect ChromiumOS Kernel 5.10 & 5.15. Note that kernel 5.4 is not affected.

# reproduction

It is reproduced on the linux-5.15 kernel and the root cause is clear.

You could use the following syzkaller repo or the attached poc.

```
r0 = syz_open_dev$tty20(0xc, 0x4, 0x1)
ioctl$TIOCSETD(r0, 0x5423, &(0x7f0000000080)=0x15)
ioctl$TCSETSF2(r0, 0x404c4701, &(0x7f0000000040)={0x2, 0x0, 0x0, 0x0, 0x0, "ebeed70000000000000000960000000800", 0x0, 0x2})
r1 = syz_open_dev$tty20(0xc, 0x4, 0x1)
ioctl$TCSETSF2(r1, 0x404c4701, &(0x7f0000000040)={0x2, 0x0, 0x0, 0x0, 0x3, "ebeed70000000000000000960000000800", 0x0, 0x2})
ioctl$TCSETSF2(r1, 0x404c4701, &(0x7f0000000040)={0x2, 0x0, 0x0, 0x0, 0x3, "ebeed70000000000000000960000000800", 0x0, 0x2})
```


# patch suggestion

We could NULL-ify the `gsm->dlci[i]` or `gsm->dlci[0]` after calling `gsm_dlci_release`.

### da...@chromium.org (2023-07-13)

[Empty comment from Monorail migration]

### ch...@google.com (2023-07-14)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/291178675). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

[Monorail blocking: b/291178675]

### [Deleted User] (2023-07-16)

[Empty comment from Monorail migration]

### ch...@google.com (2023-07-31)

Update from the reporter:

the upstream kernel has merged the aforementioned patch to fix this UAF. The stable kernel, i.e., 5.10, 5.15, 6.1, 6.4, have applied this patch as well.

The patch could be viewed at
https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/commit/?id=9b9c8195f3f0d74a826077fc1c01b9ee74907239


### [Deleted User] (2023-07-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-31)

[Empty comment from Monorail migration]

### st...@google.com (2023-08-29)

[Empty comment from Monorail migration]

### ch...@google.com (2023-09-18)

Exploitability - Explain why/why not the bug is reachable and/or exploitable
Exploitable, because the bug exists in an active kernel version used by ChromeOS. The original bug doesn't need to trigger any race condition.

Privileges and Capabilities - Identify which process is exploited and where code execution potentially can be achieved if the attacker can break out of that process, and explain why
This can lead to arbitrary code execution in kernel at worse, or cause crashes or memory leaks at best.

Origin of fix - Is the issue already known upstream, fixed by work from a previously known or reported issue, provided by the reporter, or any other information that would be relevant toward reward eligibility
Reporter reported the issue upstream and wrote a patch, however the patch was not sufficient for mitigation, due to race condition. Another patch was written by someone else that addressed the race issue by utilizing a mutex_lock() before assigning values. Patches are present in ChromeOS.

Mitigations - Detail any regarding mitigation considerations (we're run across a few comments, such as "we considered this issue to be highly mitigated" without explanation)
The issue is mitigated as both the UAF and race conditions have been fixed, as described above.

Severity assessment - why not higher, why not lower
Security_Severity-Medium. Not lower because it can potentially grant arbitrary code execution, and not higher because it would be difficult to achieve arbitrary code execution due to the nature of the bug being memory corruption.

### am...@chromium.org (2023-09-26)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-12)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-12)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-12)

Congratulations! 
The VRP Panel has decided to award you $1500 for this report. 
A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in discovering and reporting this issue to us -- great work! 
Please be mindful that previous reward decisions made by the Chrome VRP should not be considered precedent for potential future ChromeOS VRP reward amounts or decisions.

### am...@google.com (2023-10-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-11-06)

This issue was migrated from crbug.com/chromium/1464449?no_tracker_redirect=1

[Monorail blocking: b/291178675]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40067327)*
