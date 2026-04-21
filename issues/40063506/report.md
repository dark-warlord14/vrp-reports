# Security: ChromeOS: Local privilege escalation due to use-after-free in u32 classifier

| Field | Value |
|-------|-------|
| **Issue ID** | [40063506](https://issues.chromium.org/issues/40063506) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | mg...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2023-03-10 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

A reference counter leak occurs due to incorrect error handling when creating a `tc_u_knode` object in the `u32_change()`. By exploiting the vulnerability, an attacker could gain root privilege.

```
static int u32_change(struct net \*net, struct sk_buff \*in_skb,  
		      struct tcf_proto \*tp, unsigned long base, u32 handle,  
		      struct nlattr \*\*tca, void \*\*arg, u32 flags,  
		      struct netlink_ext_ack \*extack)  
{  
	...  
	n = kzalloc(struct_size(n, sel.keys, s->nkeys), GFP_KERNEL);  
	if (n == NULL) {  
		err = -ENOBUFS;  
		goto erridr;  
	}  
	...  
	err = u32_set_parms(net, tp, base, n, tb, tca[TCA_RATE],		// [1]  
			    flags, n->flags, extack);  
	if (err == 0) {  
		...  
	}  
  
errhw:  
#ifdef CONFIG_CLS_U32_MARK  
	free_percpu(n->pcpu_success);  
#endif  
  
errout:  
	tcf_exts_destroy(&n->exts);  
#ifdef CONFIG_CLS_U32_PERF  
errfree:  
	free_percpu(n->pf);  
#endif  
	kfree(n);							// [2]  
erridr:  
	idr_remove(&ht->handle_idr, handle);  
	return err;  
}  

```

When creating a new knode in the `u32_change()`, `u32_set_parms()` is called to set parameters.

```
static int u32_set_parms(struct net \*net, struct tcf_proto \*tp,  
			 unsigned long base,  
			 struct tc_u_knode \*n, struct nlattr \*\*tb,  
			 struct nlattr \*est, u32 flags, u32 fl_flags,  
			 struct netlink_ext_ack \*extack)  
{  
	int err;  
  
	err = tcf_exts_validate_ex(net, tp, tb, est, &n->exts, flags,  
				   fl_flags, extack);  
	if (err < 0)  
		return err;  
  
	if (tb[TCA_U32_LINK]) {  
		u32 handle = nla_get_u32(tb[TCA_U32_LINK]);  
		struct tc_u_hnode \*ht_down = NULL, \*ht_old;  
  
		if (TC_U32_KEY(handle)) {  
			NL_SET_ERR_MSG_MOD(extack, "u32 Link handle must be a hash table");  
			return -EINVAL;  
		}  
  
		if (handle) {  
			ht_down = u32_lookup_ht(tp->data, handle);  
  
			if (!ht_down) {  
				NL_SET_ERR_MSG_MOD(extack, "Link hash table not found");  
				return -EINVAL;  
			}  
			if (ht_down->is_root) {  
				NL_SET_ERR_MSG_MOD(extack, "Not linking to root node");  
				return -EINVAL;  
			}  
			ht_down->refcnt++;			// [3]  
		}  
  
		ht_old = rtnl_dereference(n->ht_down);  
		rcu_assign_pointer(n->ht_down, ht_down);  
  
		if (ht_old)  
			ht_old->refcnt--;  
	}  
	if (tb[TCA_U32_CLASSID]) {  
		n->res.classid = nla_get_u32(tb[TCA_U32_CLASSID]);  
		tcf_bind_filter(tp, &n->res, base);  
	}  
  
	if (tb[TCA_U32_INDEV]) {  
		int ret;  
		ret = tcf_change_indev(net, tb[TCA_U32_INDEV], extack);  
		if (ret < 0)  
			return -EINVAL;				// [4]  
		n->ifindex = ret;  
	}  
	return 0;  
}  

```

If `TCA_U32_LINK` is set in the `u32_set_parms()`, the hnode with the given id is fetched, linked with the created knode, and the reference counter of the hnode is increased [3]. Then in the last `if` statement, if the `tcf_change_indev()` returns an error, the `u32_set_parms()` returns an error [4]. If `u32_set_parms()` returns an error, the error handling routine is executed in the `u32_change()` [2]. At this time, a reference counter leak occurs because the increased reference counter is not decremented in the error handling routine.

```
struct tc_u_hnode {  
	struct tc_u_hnode __rcu	\*next;  
	u32			handle;  
	u32			prio;  
	int			refcnt;  
	...  
};  

```

Since the `refcnt` member of the `tc_u_hnode` structure is int type (size of 32 bits), reference counter overflow can occur if knode allocations fail 2^32 times resulting in use-after-free.

```
static int u32_delete(struct tcf_proto \*tp, void \*arg, bool \*last,  
		      bool rtnl_held, struct netlink_ext_ack \*extack)  
{  
	struct tc_u_hnode \*ht = arg;  
	struct tc_u_common \*tp_c = tp->data;  
	int ret = 0;  
  
	if (TC_U32_KEY(ht->handle)) {  
		u32_remove_hw_knode(tp, (struct tc_u_knode \*)ht, extack);  
		ret = u32_delete_key(tp, (struct tc_u_knode \*)ht);				// [5]  
		goto out;  
	}  
  
	if (ht->is_root) {  
		NL_SET_ERR_MSG_MOD(extack, "Not allowed to delete root node");  
		return -EINVAL;  
	}  
  
	if (ht->refcnt == 1) {  
		u32_destroy_hnode(tp, ht, extack);								// [6]  
	} else {  
		NL_SET_ERR_MSG_MOD(extack, "Can not delete in-use filter");  
		return -EBUSY;  
	}  
  
out:  
	\*last = tp_c->refcnt == 1 && tp_c->knodes == 0;  
	return ret;  
}  

```

When a reference counter overflow occurs in the hnode object, it can be deleted by `u32_delete()` even if the linked knode exists [6].

```
static void __u32_destroy_key(struct tc_u_knode \*n)  
{  
	struct tc_u_hnode \*ht = rtnl_dereference(n->ht_down);  
  
	tcf_exts_destroy(&n->exts);  
	if (ht && --ht->refcnt == 0)  
		kfree(ht);	// [7]  
	kfree(n);  
}  

```

Finally, when the knode linking the freed hnode is deleted, the `u32_delete()` calls `__u32_destroy_key()` [5], and use-after-free occurs since `ht` is already freed. To free an arbitrary object in [7], we should spray slab objects to set `ht->refcnt` to 1.

**VERSION**  

Operating System: chromeos 5.10.168-21783-g5a3143bcd0de

**REPRODUCTION CASE**

To reproduce the vulnerability, download the attached `poc.c` file, compile and run it. Before compiling it, modify the offsets variable of poc.c to the `user_free_payload_rcu()` offset loaded in the target kernel. I disabled `CONFIG_RCU_LAZY` when building the kernel to increase the success rate of the exploit.

The vulnerability is triggered about 1-2 hours after the poc is executed (<1 hour with i7-12700). To make the test faster, modify the size of `refcnt` of `struct tc_u_hnode` to 20 bits (i.e., int refcnt:20), and set `REFCNT_SIZE` in `poc.c` to 20. If the POC is executed successfully, the following dmesg log is printed.

```
[   62.426858] BUG: unable to handle page fault for address: 0000616161616161  
[   62.428642] #PF: supervisor instruction fetch in kernel mode  
[   62.430070] #PF: error_code(0x0010) - not-present page  
[   62.431371] PGD 0 P4D 0   
[   62.432114] Oops: 0010 [#1] PREEMPT SMP NOPTI  
[   62.433412] CPU: 1 PID: 278 Comm: poc Not tainted 5.10.168-21783-g5a3143bcd0de-dirty #42 b488ae1acf08a3d6b927f61cd3677c369649aa18  
[   62.436743] Hardware name: QEMU Standard PC (i440FX + PIIX, 1996), BIOS 1.13.0-1ubuntu1.1 04/01/2014  
[   62.438880] RIP: 0010:0x616161616161  
[   62.439589] Code: Unable to access opcode bytes at RIP 0x616161616137.  
[   62.440764] RSP: 0018:ffffc9000051f7e8 EFLAGS: 00010246  
[   62.441563] RAX: ffff8881060fef80 RBX: ffff8881087d4200 RCX: ffff888102809000  
[   62.442549] RDX: 0000000000000000 RSI: 0000000000000001 RDI: ffff8881060fe880  
[   62.443414] RBP: ffffc9000051f930 R08: 0000000000000000 R09: ffffc9000051fb90  
[   62.444181] R10: ffffffff8219c940 R11: 0000616161616161 R12: ffffc9000051fb90  
[   62.444868] R13: ffff88810609a380 R14: ffff8881087b2b00 R15: ffff8881060fe880  
[   62.445497] FS:  00007d0b5b8e0480(0000) GS:ffff888237d00000(0000) knlGS:0000000000000000  
[   62.446140] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033  
[   62.446543] CR2: 0000616161616161 CR3: 00000001055cc001 CR4: 0000000000770ee0  
[   62.447017] PKRU: 55555554  
[   62.447197] Call Trace:  
[   62.447354]  ? tc_del_tfilter+0x408/0x6af  
[   62.447596]  ? tc_new_tfilter+0x9d8/0x9d8  
[   62.447832]  rtnetlink_rcv_msg+0x337/0x3fa  
[   62.448076]  ? sysvec_apic_timer_interrupt+0x6c/0x7a  
[   62.448367]  ? get_page_from_freelist+0x15ea/0x16e4  
[   62.448651]  ? get_page_from_freelist+0x15ea/0x16e4  
[   62.448936]  ? avc_has_perm+0xa0/0x182  
[   62.449156]  ? rtnetlink_bind+0x2c/0x2c  
[   62.449382]  netlink_rcv_skb+0x88/0xfc  
[   62.449602]  netlink_unicast+0x162/0x237  
[   62.449832]  netlink_sendmsg+0x3b8/0x44b  
[   62.450063]  sock_sendmsg+0x6b/0x71  
[   62.450269]  ____sys_sendmsg+0x152/0x20e  
[   62.450499]  ? copy_msghdr_from_user+0x5e/0x86  
[   62.450759]  ? _raw_spin_unlock_irqrestore+0x17/0x2d  
[   62.451049]  ___sys_sendmsg+0x7c/0xb5  
[   62.451265]  ? __wake_up_common_lock+0x7a/0xa4  
[   62.451528]  ? file_tty_write+0x2b4/0x2c6  
[   62.451763]  ? vfs_write+0x195/0x3c6  
[   62.451976]  __sys_sendmsg+0x5d/0x97  
[   62.452187]  ? ksys_write+0x6d/0xce  
[   62.452393]  do_syscall_64+0x3d/0x50  
[   62.452603]  entry_SYSCALL_64_after_hwframe+0x61/0xc6  
[   62.452898] RIP: 0033:0x7d0b5b40cdc7  
[   62.453108] Code: d8 64 89 02 48 c7 c0 ff ff ff ff eb cd 66 0f 1f 44 00 00 8b 05 4a 49 2b 00 85 c0 75 2e 48 63 ff 48 63 d2 b8 2e 00 00  
[   62.454184] RSP: 002b:00007ffc345bd858 EFLAGS: 00000246 ORIG_RAX: 000000000000002e  
[   62.454622] RAX: ffffffffffffffda RBX: 00000000000003e8 RCX: 00007d0b5b40cdc7  
[   62.455035] RDX: 0000000000000000 RSI: 00007ffc345bd8c0 RDI: 0000000000000003  
[   62.455450] RBP: 00007ffc345bd900 R08: 0000000000000000 R09: 0000000000002010  
[   62.455861] R10: 0000000000000000 R11: 0000000000000246 R12: 00005b006769d4e0  
[   62.456303] R13: 00007ffc345bda50 R14: 0000000000000000 R15: 0000000000000000  
[   62.456715] Modules linked in:  
[   62.456896] CR2: 0000616161616161  
[   62.457092] ---[ end trace 3662603ec87bcb02 ]---  
[   62.457361] RIP: 0010:0x616161616161  
[   62.457586] Code: Unable to access opcode bytes at RIP 0x616161616137.  
[   62.457965] RSP: 0018:ffffc9000051f7e8 EFLAGS: 00010246  
[   62.458269] RAX: ffff8881060fef80 RBX: ffff8881087d4200 RCX: ffff888102809000  
[   62.458680] RDX: 0000000000000000 RSI: 0000000000000001 RDI: ffff8881060fe880  
[   62.459092] RBP: ffffc9000051f930 R08: 0000000000000000 R09: ffffc9000051fb90  
[   62.459504] R10: ffffffff8219c940 R11: 0000616161616161 R12: ffffc9000051fb90  
[   62.459919] R13: ffff88810609a380 R14: ffff8881087b2b00 R15: ffff8881060fe880  
[   62.460357] FS:  00007d0b5b8e0480(0000) GS:ffff888237d00000(0000) knlGS:0000000000000000  
[   62.460823] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033  
[   62.461158] CR2: 0000616161616161 CR3: 00000001055cc001 CR4: 0000000000770ee0  
[   62.461574] PKRU: 55555554  
[   62.461734] Kernel panic - not syncing: Fatal exception  
[   62.462321] Kernel Offset: disabled  
[   62.462532] ---[ end Kernel panic - not syncing: Fatal exception ]---  

```

We can see that the RIP value is modified to a controlled value of '0x616161616161'. Since the RIP value has been modified, the arbitrary code can be executed in kernel context, thus, we can gain root privilege by performing ROP. I have successfully obtained root privilege on Google's container-optimized OS, but not on CrOS yet.

`poc_min.c` is the minimized code that triggers only UAF. After executing the poc\_min.c, a UAF log is printed as follows.

```
[   62.298959] ==================================================================  
[   62.301117] BUG: KASAN: use-after-free in __u32_destroy_key+0x2f/0x5e  
[   62.303079] Read of size 4 at addr ffff8881157a7b10 by task kworker/u4:2/89  
  
[   62.305539] CPU: 1 PID: 89 Comm: kworker/u4:2 Not tainted 5.10.168-21783-g5a3143bcd0de-dirty #49 c598755f91ac827b2343804529b50104e3602ff3  
[   62.308836] Hardware name: QEMU Standard PC (i440FX + PIIX, 1996), BIOS 1.13.0-1ubuntu1.1 04/01/2014  
[   62.310729] Workqueue: netns cleanup_net  
[   62.311416] Call Trace:  
[   62.311835]  dump_stack+0xe4/0x143  
[   62.312393]  print_address_description+0x25/0x4dd  
[   62.313052]  ? printk+0x59/0x73  
[   62.313467]  kasan_report+0x146/0x18e  
[   62.314011]  ? __u32_destroy_key+0x2f/0x5e  
[   62.314474]  ? __u32_destroy_key+0x2f/0x5e  
[   62.315001]  __u32_destroy_key+0x2f/0x5e  
[   62.315513]  u32_clear_hnode+0x237/0x29f  
[   62.316061]  u32_destroy+0x115/0x1a7  
[   62.316584]  tcf_proto_destroy+0x44/0x134  
[   62.317271]  tcf_chain_flush+0xb1/0xc2  
[   62.317847]  __tcf_block_put+0x136/0x1b1  
[   62.318397]  tcf_block_put+0x47/0x62  

```

The suggested patch is as follows. When handling errors in the `u32_change()`, if `n->ht_down` is set, the reference counter decreases.

```
--- a/net/sched/cls_u32.c  
+++ b/net/sched/cls_u32.c  
@@ -1109,6 +1109,10 @@ static int u32_change(struct net \*net, struct sk_buff \*in_skb,  
 errfree:  
        free_percpu(n->pf);  
 #endif  
+       ht = rtnl_dereference(n->ht_down);  
+  
+       if (ht && --ht->refcnt == 0)  
+               kfree(ht);  
        kfree(n);  
 erridr:  
        idr_remove(&ht->handle_idr, handle);  

```

**CREDIT INFORMATION**

Reporter credit: Mingi Cho of Theori

## Attachments

- [poc_min.c](attachments/poc_min.c) (text/plain, 9.1 KB)
- [poc.c](attachments/poc.c) (text/plain, 20.2 KB)

## Timeline

### [Deleted User] (2023-03-10)

[Empty comment from Monorail migration]

### ma...@chromium.org (2023-03-10)

[Empty comment from Monorail migration]

### en...@google.com (2023-03-14)

Thank you for the report.
Assigning to roxabee@ while we decide on an official course of action for upstream kernel bug reports.

### [Deleted User] (2023-03-19)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ch...@google.com (2023-06-12)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/286856236). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.”

[Monorail blocked-on: b/286856236]

### ch...@google.com (2023-07-24)

Marked as fixed.
Problem has ben fixed in ToT of affected kernel branches. Marking as Fixed. Reopen to cherry-pick to release branches if needed.

### [Deleted User] (2023-07-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-11-06)

Congratulations! 
The VRP Panel has decided to award you $500 for this report. 
A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in discovering and reporting this issue to us -- great work! 
Please be mindful that previous reward decisions made by the Chrome VRP should not be considered precedent for potential future ChromeOS VRP reward amounts or decisions.

### mg...@gmail.com (2023-11-07)

Hello,

Thanks for the reward. I have few questions about it.

Firstly, why the rule is changed after report? The decision to report here was based on the rule at the time of the report. I think it's confusing and unfair.

Second, according to the Buganizer system, the vulnerability is rated as high severity, so why is the reward in the medium severity range?

Third, why was the report rated a baseline reward? I haven't seen any recent report that proved the vulnerability is *really exploitable*, and some of them is even unreachable with user privilege. But my report showed that the vulnerability is exploitable by controlling RIP register to 0x616161616161(i.e., Control-flow hijacking). Also, I attached root cause analysis, the POC code and proposed patch.

### am...@google.com (2023-11-11)

[Empty comment from Monorail migration]

### is...@google.com (2023-11-11)

This issue was migrated from crbug.com/chromium/1423266?no_tracker_redirect=1

[Monorail blocked-on: b/286856236]

### mg...@gmail.com (2024-06-27)

Appeal reward reason: Hello,

The Buganizer system rated the vulnerability as high severity as shown below, but awarded a medium severity reward.

"Severity: High severity. This is an escalation of privilege so it is not lower than high. The vulnerability needs the attacker to be able to run arbitrary code so it is not critical severity."

In the report, I provided a detailed root cause explanation of the vulnerability and demonstrated that control flow hijacking was possible by controlling the RIP register by exploiting it. Therefore, I believe that the report qualifies for "High Quality Reports".

Finally, I would like you to consider that the bounty amount was set at $20,000 based on the rule at the time of reporting the vulnerability.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063506)*
