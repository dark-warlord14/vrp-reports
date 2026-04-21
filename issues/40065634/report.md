# Security: Chrome OS: OOB write in function session_get_prop_buf_req of venus driver

| Field | Value |
|-------|-------|
| **Issue ID** | [40065634](https://issues.chromium.org/issues/40065634) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | pi...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-06-11 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

Background:

venus on qcom chromebook is responsible for video hardware codec, it support some complicated codecs.  

When chrome browsing a video web page, if codec matches, chrome browser will send the video buffer to venus driver, venus driver will send to venus firmware to decode.

So venus firmware itself is a remote attack surface from chrome browser, and usually firmware has little mitigations than application processor, like this venus firmware exploit:  

<https://i.blackhat.com/USA-19/Wednesday/us-19-Gong-Bypassing-The-Maginot-Line-Remotely-Exploit-The-Hardware-Decoder-On-Smartphone.pdf>

After venus firmware been compromised remotely, it can't do many things, like in a sandbox.  

But venus firmware can do Inter-Processor Communication with Application Processor, venus linux kernel driver will handle the Inter-Processor Communications from venus firmware.

On strongbad or trogdor chromebooks, they are using venus to do hardware accelerate:  

<https://bugs.chromium.org/p/chromium/issues/detail?id=1198714>

venus firmware can set ipc data in share memory and trigger AP interrupt to let AP to process the ipc data.

The Bug:

When venus do IPC to AP, below venus driver function venus\_isr\_thread will read and process the packet:  

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.15/drivers/media/platform/qcom/venus/hfi_venus.c;l=1081>

static irqreturn\_t venus\_isr\_thread(struct venus\_core \*core) <------- interrupt handler  

{  

//skip...

```
while (!venus_iface_msgq_read(hdev, pkt)) {  <-------- read packet from share memory  
	msg_ret = hfi_process_msg_packet(core, pkt);  <----------- process packet  
	switch (msg_ret) {  
	case HFI_MSG_EVENT_NOTIFY:  
		venus_process_msg_sys_error(hdev, pkt);  
		break;  
	//skip...  
	default:  
		break;  
	}  
}  

```

}

In hfi\_process\_msg\_packet, it will find correponding handler from the handlers table.  

This bug is in call path:  

hfi\_process\_msg\_packet -> hfi\_session\_prop\_info -> session\_get\_prop\_buf\_req

In function session\_get\_prop\_buf\_req:  

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.15/drivers/media/platform/qcom/venus/hfi_msgs.c;drc=59cc491a68bd9dc348e98695ed10a9b560086caa;l=377>

static unsigned int  

session\_get\_prop\_buf\_req(struct hfi\_msg\_session\_property\_info\_pkt \*pkt,  

struct hfi\_buffer\_requirements \*bufreq)  

{  

struct hfi\_buffer\_requirements \*buf\_req;  

u32 req\_bytes;  

unsigned int idx = 0;

```
req_bytes = pkt->shdr.hdr.size - sizeof(\*pkt);  

if (!req_bytes || req_bytes % sizeof(\*buf_req) || !pkt->data[0])  
	/\* bad packet \*/  
	return HFI_ERR_SESSION_INVALID_PARAMETER;  

buf_req = (struct hfi_buffer_requirements \*)&pkt->data[0];  <------------- ipc data  
if (!buf_req)  
	return HFI_ERR_SESSION_INVALID_PARAMETER;  

while (req_bytes) {  
	memcpy(&bufreq[idx], buf_req, sizeof(\*bufreq));  <--------- copy ipc data to bufreq[idx]  
	idx++;  

	if (idx > HFI_BUFFER_TYPE_MAX)  <------------- wrong bounds check, should be >=  
		return HFI_ERR_SESSION_INVALID_PARAMETER;  

	req_bytes -= sizeof(struct hfi_buffer_requirements);  
	buf_req++;  
}  

return HFI_ERR_NONE;  

```

}

Above bounds check is not correct, will cause oob write sizeof(struct hfi\_buffer\_requirements),  

from the struct venus\_init, it can oob write the struct ida which has a object pointer:  

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.15/drivers/media/platform/qcom/venus/core.h;drc=402fc24bd722630e2ea3afc14ea503bb16124e8d;l=479>

```
union hfi_get_property hprop;   <----------  
unsigned int core_acquired: 1;  
unsigned int bit_depth;  
unsigned int pic_struct;  
bool next_buf_last;  
bool drain_active;  
enum venus_inst_modes flags;  
struct ida dpb_ids;    <------------- can overwrite this object  

```

Patch:

diff --git a/drivers/media/platform/qcom/venus/hfi\_msgs.c b/drivers/media/platform/qcom/venus/hfi\_msgs.c  

index df96db3761a7..1c5cc5a5f89a 100644  

--- a/drivers/media/platform/qcom/venus/hfi\_msgs.c  

+++ b/drivers/media/platform/qcom/venus/hfi\_msgs.c  

@@ -374,7 +374,7 @@ session\_get\_prop\_buf\_req(struct hfi\_msg\_session\_property\_info\_pkt \*pkt,  

memcpy(&bufreq[idx], buf\_req, sizeof(\*bufreq));  

idx++;

- ```
            if (idx > HFI_BUFFER_TYPE_MAX)  
  
  ```

- ```
            if (idx >= HFI_BUFFER_TYPE_MAX)  
                    return HFI_ERR_SESSION_INVALID_PARAMETER;  
  
            req_bytes -= sizeof(struct hfi_buffer_requirements);  
  
  ```

**VERSION**  

strongbad or trogdor, latest v5.15 kernel code

**CREDIT INFORMATION**  

Reporter credit: [lovepink]

## Attachments

- [venus_4_fix.patch](attachments/venus_4_fix.patch) (text/plain, 669 B)
- [1453937.diff](attachments/1453937.diff) (text/plain, 2.4 KB)

## Timeline

### [Deleted User] (2023-06-11)

[Empty comment from Monorail migration]

### ar...@google.com (2023-06-12)

[Empty comment from Monorail migration]

### ch...@google.com (2023-06-13)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/286974958). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.”

[Monorail blocking: b/286974958]

### [Deleted User] (2023-06-13)

[Empty comment from Monorail migration]

### ch...@google.com (2023-08-14)

Project: chromiumos/third_party/kernel
Branch: chromeos-5.15

commit bc8df7481fa11f36f21cba9d0ff55c38cd1ae6b8
Author: Vikash Garodia <quic_vgarodia@quicinc.com>
Date:   Thu Jul 27 10:04:27 2023

    FROMLIST: venus: hfi: fix the check to handle session buffer requirement
   
    Buffer requirement, for different buffer type, comes from video firmware.
    While copying these requirements, there is an OOB possibility when the
    payload from firmware is more than expected size. Fix the check to avoid
    the OOB possibility.
   
    Cc: stable@vger.kernel.org
    Fixes: 09c2845e8fe4 ("[media] media: venus: hfi: add Host Firmware Interface (HFI)")
    Signed-off-by: Vikash Garodia <quic_vgarodia@quicinc.com>
    Reviewed-by: Nathan Hebert <nhebert@chromium.org>
    (am from https://patchwork.kernel.org/patch/13328722/)
    (also found at https://lore.kernel.org/r/1690432469-14803-3-git-send-email-quic_vgarodia@quicinc.com)
   
    UPSTREAM-TASK=b:295178805
    BUG=b:286974958
    TEST=Compiles. Will watch Trogdor test results
   
    Change-Id: Ie4993855dfabcd7bf415c3a98308409c93c08908
    Signed-off-by: Nathan Hebert <nhebert@chromium.org>
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4766223
    Reviewed-by: Stephen Boyd <swboyd@chromium.org>
    Reviewed-by: Sean Paul <sean@poorly.run>

M       drivers/media/platform/qcom/venus/hfi_msgs.c

https://chromium-review.googlesource.com/4766223
04:13
04:13
CLs: Merged:​<none>      crrev/c/4766223, crrev/c/4766224, crrev/c/4766225
CLs: Pending:​crrev/c/4766223, crrev/c/4766224, crrev/c/4766225      <none>

### [Deleted User] (2023-08-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-14)

[Empty comment from Monorail migration]

### pi...@gmail.com (2023-08-20)

PoC method.

These venus driver issues are straightforward and have been confirmed by Qcom Security Team and Dev Team, but for PoC it is hard to modify venus binary firmware to send a malicious IPC message to Linux kernel. You can try below PoC idea.

A PoC idea is patch linux kernel to modify normal IPC message to malicious one, just simulate the firmware behaviour. And open chrome browser to visit hardware decoding video to trigger IPC from firmware.
I try to give a PoC patch of Linux kernel, but strongbad test image seems can't boot correctly on my strongbad chromebook while kukui and hana all are OK, I don't know why:
1, build test kernel image with attached diff, deploy to device
2, may crash on boot, because when booting the venus firmware may contact with linux kernel with IPC messages
3, if boot not crash, use chrome browser to visit the official video test url and play the video: http://crosvideo.appspot.com/?codec=vp8
4, if not crash, then should print the added log in patch:  printk("[poc] idx oob write!\n");

### ch...@google.com (2023-09-19)

Exploitability: Not exploitable by itself. Requires arbitrary code execution on the Venus hardware decoder (which has had atleast one AV:N as noted). The victim struct ida, as noted, has data pointers which could be plausibly used to influence writes or frees of arbitrary addresses.

Privileges and Capabilities: Kernel heap write. Unknown if this can be escalated to arbitrary code execution without e.g help from userspace.

Origin of fix: Not known upstream until reported by the reporter

Mitigations: Requires arbitrary code execution on the Venus hardware decoder.

Severity Assessment: Medium since this is a Memory corruption that's not directly triggerable from an exposed interface

### pi...@gmail.com (2023-09-19)

I think above severity assessment is not right, qcom security and me both think this is a High Severity.

Chromebooks have same attack scenario as other devices, so the severity will not changed because of there is any special security design on chromebooks.

Use CVSS Score 3.1, the severity is High :

CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H  8.1 High

### pi...@gmail.com (2023-09-20)

In https://chromium.googlesource.com/chromiumos/docs/+/HEAD/security_severity_guidelines.md#High-Severity
```
In general, these are the bypasses we consider High-severity bugs:
...
Code execution in the kernel that requires local privileges to exploit (i.e. local kernel privilege escalation)
...
```

### am...@chromium.org (2023-09-26)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-26)

Congratulations! 
The VRP Panel has decided to award you $500 for this report. 
A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in discovering and reporting this issue to us -- great work! 
Please be mindful that previous reward decisions made by the Chrome VRP should not be considered precedent for potential future ChromeOS VRP reward amounts or decisions.

### am...@google.com (2023-10-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-11-20)

This issue was migrated from crbug.com/chromium/1453937?no_tracker_redirect=1

[Monorail blocking: b/286974958]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065634)*
