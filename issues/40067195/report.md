# Security: ChromeOS: Information leak due to type confusion in u32 classifier

| Field | Value |
|-------|-------|
| **Issue ID** | [40067195](https://issues.chromium.org/issues/40067195) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | mg...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-07-11 |
| **Bounty** | $750.00 |

## Description

**VULNERABILITY DETAILS**

In the u32 classifier, when the lower 12 bits of the key node's handle are set to 0, type confusion occurs when reading it. As a result, the attacker can read the upper 4 bytes of the kernel heap address, which is the physmap\_base, and this can be used for kernel exploitation, such as unlinking attack.

```
static int u32_change(struct net \*net, struct sk_buff \*in_skb,  
		      struct tcf_proto \*tp, unsigned long base, u32 handle,  
		      struct nlattr \*\*tca, void \*\*arg, u32 flags,  
		      struct netlink_ext_ack \*extack)  
{  
	...  
	if (tb[TCA_U32_HASH]) {  
		htid = nla_get_u32(tb[TCA_U32_HASH]);  
		if (TC_U32_HTID(htid) == TC_U32_ROOT) {  
			ht = rtnl_dereference(tp->root);  
			htid = ht->handle;  
		} else {  
			ht = u32_lookup_ht(tp->data, TC_U32_HTID(htid));  
			if (!ht) {  
				NL_SET_ERR_MSG_MOD(extack, "Specified hash table not found");  
				return -EINVAL;  
			}  
		}  
	} else {  
		ht = rtnl_dereference(tp->root);  
		htid = ht->handle;  
	}  
  
	if (ht->divisor < TC_U32_HASH(htid)) {  
		NL_SET_ERR_MSG_MOD(extack, "Specified hash table buckets exceed configured value");  
		return -EINVAL;  
	}  
  
	if (handle) {  
		if (TC_U32_HTID(handle) && TC_U32_HTID(handle ^ htid)) {  
			NL_SET_ERR_MSG_MOD(extack, "Handle specified hash table address mismatch");  
			return -EINVAL;  
		}  
		handle = htid | TC_U32_NODE(handle);  
		err = idr_alloc_u32(&ht->handle_idr, NULL, &handle, handle,  
				    GFP_KERNEL);  
		if (err)  
			return err;  
	} else  
		handle = gen_new_kid(ht, htid);  
	...  

```

When creating a filter in the u32\_change(), since the handle value of tp->root is 0x80000000, if the handle value is input within the range of 0x01000 to 0xff000, the lower 12 bits of the handle value is set to 0.

```
static int u32_dump(struct net \*net, struct tcf_proto \*tp, void \*fh,  
		    struct sk_buff \*skb, struct tcmsg \*t, bool rtnl_held)  
{  
	struct tc_u_knode \*n = fh;  
	struct tc_u_hnode \*ht_up, \*ht_down;  
	struct nlattr \*nest;  
  
	if (n == NULL)  
		return skb->len;  
  
	t->tcm_handle = n->handle;  
  
	nest = nla_nest_start_noflag(skb, TCA_OPTIONS);  
	if (nest == NULL)  
		goto nla_put_failure;  
  
	if (TC_U32_KEY(n->handle) == 0) {  
		struct tc_u_hnode \*ht = fh;  
		u32 divisor = ht->divisor + 1;  
  
		if (nla_put_u32(skb, TCA_U32_DIVISOR, divisor))  
			goto nla_put_failure;  

```

Afterwards, when reading a knode in the u32\_dump(), "TC\_U32\_KEY(n->handle) == 0" is satisfied, the knode is treated as an hnode, and the ht->divisor of the hnode structure is read.

```
struct tc_u_knode {  
	struct tc_u_knode __rcu	\*next;  
	u32			handle;  
	struct tc_u_hnode __rcu	\*ht_up;  
	struct tcf_exts		exts;  
	int			ifindex;  
	u8			fshift;  
	struct tcf_result	res;  
	struct tc_u_hnode __rcu	\*ht_down;  
#ifdef CONFIG_CLS_U32_PERF  
	struct tc_u32_pcnt __percpu \*pf;  
#endif  
	u32			flags;  
	unsigned int		in_hw_count;  
#ifdef CONFIG_CLS_U32_MARK  
	u32			val;  
	u32			mask;  
	u32 __percpu		\*pcpu_success;  
#endif  
	struct rcu_work		rwork;  
	/\* The 'sel' field MUST be the last field in structure to allow for  
	 \* tc_u32_keys allocated at end of structure.  
	 \*/  
	struct tc_u32_sel	sel;  
};  
  
struct tc_u_hnode {  
	struct tc_u_hnode __rcu	\*next;  
	u32			handle;  
	u32			prio;  
	int			refcnt;  
	unsigned int		divisor;  
	struct idr		handle_idr;  
	bool			is_root;  
	struct rcu_head		rcu;  
	u32			flags;  
	/\* The 'ht' field MUST be the last field in structure to allow for  
	 \* more entries allocated at end of structure.  
	 \*/  
	struct tc_u_knode __rcu	\*ht[];  
};  

```

Since the offset of the divisor of the tc\_u\_hnode structure is the upper 4 bytes of the ht\_up pointer of tc\_u\_knode, the upper 4 bytes of the kernel heap address are leaked.

To prevent this, do not allow "TC\_U32\_KEY(n->handle) == 0" when creating a node, or check the type by using a flag instead of the handle value.

**VERSION**  

Operating System: chromeos-5.15

**REPRODUCTION CASE**

- The POC code creates the u32 filter with handle 0x1000, and reads it to trigger information leak.

Compile & Execute:

$ gcc -o poc poc.c  

$ ./poc

Results:

filter parent 8008: protocol [256] pref 1 u32 chain 0  

filter parent 8008: protocol [256] pref 1 u32 chain 0 fh 800: ht divisor 1  

filter parent 8008: protocol [256] pref 1 u32 chain 0 fh 800: ht divisor -30591

We can obtain upper four bytes of the kernel heap address through ht divisor field. For example, as shown above, we can know that physmap\_base is 0xffff8880 (-30591 - 1) through divisor field.

**CREDIT INFORMATION**

Reporter credit: Mingi Cho of Theori

## Attachments

- [poc.c](attachments/poc.c) (text/plain, 4.3 KB)

## Timeline

### [Deleted User] (2023-07-11)

[Empty comment from Monorail migration]

### da...@chromium.org (2023-07-11)

[Empty comment from Monorail migration]

### ch...@google.com (2023-07-12)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/290877450). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

[Monorail blocking: b/290877450]

### [Deleted User] (2023-07-16)

[Empty comment from Monorail migration]

### ch...@google.com (2023-08-17)

Marked as fixed.
Upstream commit e68409db995 ("net: sched: cls_u32: Fix match key mis-addressing")
  Integrated in v6.5-rc5
  Fixed in chromeos-6.1 with merge of v6.1.45 (sha d652c080b67c)
    Not in R108, R114, R115, R116
  Fixed in chromeos-5.15 with merge of v5.15.126 (sha 8dedcc6af341)
    Not in R108, R114, R115, R116
  Fixed in chromeos-5.10 with merge of v5.10.190 (sha d163337bef20)
    Not in R108, R114, R115, R116
  Fixed in chromeos-5.4 with merge of v5.4.253 (sha 42b28808070e)
    Not in R108, R114, R115, R116
  Fixed in chromeos-4.19 with merge of v4.19.291 (sha 866e43b0d684)
    Not in R108, R114, R115, R116
  Not in chromeos-4.14

### [Deleted User] (2023-08-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-17)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-09-26)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-26)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-26)

Congratulations! 
The VRP Panel has decided to award you $750 for this report. 
A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in discovering and reporting this issue to us -- great work! 
Please be mindful that previous reward decisions made by the Chrome VRP should not be considered precedent for potential future ChromeOS VRP reward amounts or decisions.

### am...@google.com (2023-10-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-11-23)

This issue was migrated from crbug.com/chromium/1463903?no_tracker_redirect=1

[Monorail blocking: b/290877450]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40067195)*
