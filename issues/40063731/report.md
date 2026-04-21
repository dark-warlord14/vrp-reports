# Security: Race Condition UAF in l2cap_disconnect_req and l2cap_disconnect_rsp

| Field | Value |
|-------|-------|
| **Issue ID** | [40063731](https://issues.chromium.org/issues/40063731) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | lm...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-03-23 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

The root cause of this issue is similar to this one[1][2]. According to the discussion here[3], we should use l2cap\_chan\_hold\_unless\_zero instead of l2cap\_chan\_lock to avoid adding a refcount when it is already 0.

We should replace the l2cap\_chan\_lock[4][5] to l2cap\_chan\_hold\_unless\_zero in l2cap\_disconnect\_req and l2cap\_disconnect\_rsp.

```
static inline int l2cap_disconnect_req(struct l2cap_conn \*conn,  
				       struct l2cap_cmd_hdr \*cmd, u16 cmd_len,  
				       u8 \*data)  
{  
	struct l2cap_disconn_req \*req = (struct l2cap_disconn_req \*) data;  
	struct l2cap_disconn_rsp rsp;  
	u16 dcid, scid;  
	struct l2cap_chan \*chan;  
  
	if (cmd_len != sizeof(\*req))  
		return -EPROTO;  
  
	scid = __le16_to_cpu(req->scid);  
	dcid = __le16_to_cpu(req->dcid);  
  
	BT_DBG("scid 0x%4.4x dcid 0x%4.4x", scid, dcid);  
  
	mutex_lock(&conn->chan_lock);  
  
	chan = __l2cap_get_chan_by_scid(conn, dcid);  
	if (!chan) {  
		mutex_unlock(&conn->chan_lock);  
		cmd_reject_invalid_cid(conn, cmd->ident, dcid, scid);  
		return 0;  
	}  
  
	l2cap_chan_hold(chan);			// [4]  
	l2cap_chan_lock(chan);  
  
	rsp.dcid = cpu_to_le16(chan->scid);  
	rsp.scid = cpu_to_le16(chan->dcid);  
	l2cap_send_cmd(conn, cmd->ident, L2CAP_DISCONN_RSP, sizeof(rsp), &rsp);  
  
	chan->ops->set_shutdown(chan);  
  
	l2cap_chan_del(chan, ECONNRESET);  
  
	chan->ops->close(chan);  
  
	l2cap_chan_unlock(chan);  
	l2cap_chan_put(chan);  
  
	mutex_unlock(&conn->chan_lock);  
  
	return 0;  
}  
  
static inline int l2cap_disconnect_rsp(struct l2cap_conn \*conn,  
				       struct l2cap_cmd_hdr \*cmd, u16 cmd_len,  
				       u8 \*data)  
{  
	struct l2cap_disconn_rsp \*rsp = (struct l2cap_disconn_rsp \*) data;  
	u16 dcid, scid;  
	struct l2cap_chan \*chan;  
  
	if (cmd_len != sizeof(\*rsp))  
		return -EPROTO;  
  
	scid = __le16_to_cpu(rsp->scid);  
	dcid = __le16_to_cpu(rsp->dcid);  
  
	BT_DBG("dcid 0x%4.4x scid 0x%4.4x", dcid, scid);  
  
	mutex_lock(&conn->chan_lock);  
  
	chan = __l2cap_get_chan_by_scid(conn, scid);  
	if (!chan) {  
		mutex_unlock(&conn->chan_lock);  
		return 0;  
	}  
  
	l2cap_chan_hold(chan);			// [5]  
	l2cap_chan_lock(chan);  
  
	if (chan->state != BT_DISCONN) {  
		l2cap_chan_unlock(chan);  
		l2cap_chan_put(chan);  
		mutex_unlock(&conn->chan_lock);  
		return 0;  
	}  
  
	l2cap_chan_del(chan, 0);  
  
	chan->ops->close(chan);  
  
	l2cap_chan_unlock(chan);  
	l2cap_chan_put(chan);  
  
	mutex_unlock(&conn->chan_lock);  
  
	return 0;  
}  

```

[1] <https://lore.kernel.org/netdev/CABBYNZLyCzQ_RUJKUi8dpZorPjUsyCxXcZ-ScmMHWx0a86Ra5w@mail.gmail.com/T/>  

[2] <https://lore.kernel.org/lkml/20220622082716.478486-1-lee.jones@linaro.org/>  

[3] <https://lore.kernel.org/netdev/CABBYNZKvVKRRdWnX3uFWdTXJ_S+oAj6z72zgyV148VmFtUnPpA@mail.gmail.com/>  

[4] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.15/net/bluetooth/l2cap_core.c;drc=e2353808c6e8d1f36fb7568b4e6497e3cecf6778;l=4624>  

[5] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.15/net/bluetooth/l2cap_core.c;drc=e2353808c6e8d1f36fb7568b4e6497e3cecf6778;l=4669>

**VERSION**  

Operating System: ChromiumOS Kernel 5.15 stable + dev

**REPRODUCTION CASE**

This issue is discovered by manual code review, I will try to construct a poc to reproduce it.

FIX PATCH SUGGESTION  

I think the follwing patch should fix the problem.

```
diff --git a/net/bluetooth/l2cap_core.c b/net/bluetooth/l2cap_core.c  
index 357c3070cd37..4186a005e906 100644  
--- a/net/bluetooth/l2cap_core.c  
+++ b/net/bluetooth/l2cap_core.c  
@@ -4645,7 +4645,10 @@ static inline int l2cap_disconnect_req(struct l2cap_conn \*conn,  
                return 0;  
        }  
   
-       l2cap_chan_hold(chan);  
+       chan = l2cap_chan_hold_unless_zero(chan);  
+       if (!chan) {  
+               goto unlock;  
+       }  
        l2cap_chan_lock(chan);  
   
        rsp.dcid = cpu_to_le16(chan->scid);  
@@ -4661,6 +4664,7 @@ static inline int l2cap_disconnect_req(struct l2cap_conn \*conn,  
        l2cap_chan_unlock(chan);  
        l2cap_chan_put(chan);  
   
+unlock:  
        mutex_unlock(&conn->chan_lock);  
   
        return 0;  
@@ -4690,7 +4694,10 @@ static inline int l2cap_disconnect_rsp(struct l2cap_conn \*conn,  
                return 0;  
        }  
   
-       l2cap_chan_hold(chan);  
+       chan = l2cap_chan_hold_unless_zero(chan);  
+       if (!chan) {  
+               goto unlock;  
+       }  
        l2cap_chan_lock(chan);  
   
        if (chan->state != BT_DISCONN) {  
@@ -4706,7 +4713,7 @@ static inline int l2cap_disconnect_rsp(struct l2cap_conn \*conn,  
   
        l2cap_chan_unlock(chan);  
        l2cap_chan_put(chan);  
-  
+unlock:  
        mutex_unlock(&conn->chan_lock);  
   
        return 0;  

```

## Timeline

### [Deleted User] (2023-03-23)

[Empty comment from Monorail migration]

### hc...@google.com (2023-03-23)

[Empty comment from Monorail migration]

### ch...@google.com (2023-03-24)

[Empty comment from Monorail migration]

[Monorail blocking: b/275017040]

### ch...@google.com (2023-03-24)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/275017040). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on.

### [Deleted User] (2023-03-24)

[Empty comment from Monorail migration]

### ch...@google.com (2023-03-30)

[Comment Deleted]

### ch...@google.com (2023-03-30)

[Comment Deleted]

### ch...@google.com (2023-04-14)

marked as fixed in order to reflect the linked buganizer ticket

### ch...@google.com (2023-04-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-14)

[Empty comment from Monorail migration]

### pa...@chromium.org (2023-04-24)

Is there a path to exploitation for this bug on a ChromeOS system? Would the attacker need local root, or perhaps local lower-priv service UID/GID? I suggest Low severity unless there is a plausible path to exploitation (in which case maybe Medium or maybe keep it at High, if the preconditions are easy enough).

### ch...@google.com (2023-04-25)

[Empty comment from Monorail migration]

### am...@google.com (2023-04-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-04-27)

Congratulations! The VRP Panel has decided to award you $5,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-04-29)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-02)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-02)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-05-02)

issue is in upstream kernel, we would not be the appropriate issuer of a CVE for this issue 

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-07-21)

This issue was migrated from crbug.com/chromium/1427012?no_tracker_redirect=1

[Monorail blocking: b/275017040]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063731)*
