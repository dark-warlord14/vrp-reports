# Security:  Chrome OS: Buffer overflow in function parse_raw_formats of venus driver

| Field | Value |
|-------|-------|
| **Issue ID** | [40065630](https://issues.chromium.org/issues/40065630) |
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

venus dsp is responsible for video hardware codec, it support some complicated codecs.  

When chrome browsing a video web page, if codec matches, chrome browser will send the video buffer to venus driver, venus driver will send to venus firmware to decode.

So venus firmware itself is a remote attack surface from chrome browser, and usually DSP firmware has little mitigations than application processor, like this venus firmware exploit:  

<https://i.blackhat.com/USA-19/Wednesday/us-19-Gong-Bypassing-The-Maginot-Line-Remotely-Exploit-The-Hardware-Decoder-On-Smartphone.pdf>

After venus firmware been compromised remotely, it can't do many things, like in a sandbox.  

But venus firmware can do Inter-Processor Communication with Application Processor, venus linux kernel driver will handle the Inter-Processor Communications from venus firmware.

On strongbad or trogdor chromebooks, they are using venus to do hardware accelerate:  

<https://bugs.chromium.org/p/chromium/issues/detail?id=1198714>

The Bug:

When venus dsp do IPC to AP, below venus driver function will read and process the packet:  

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.15/drivers/media/platform/qcom/venus/hfi_venus.c;l=1081>

static irqreturn\_t venus\_isr\_thread(struct venus\_core \*core)  

{  

struct venus\_hfi\_device \*hdev = to\_hfi\_priv(core);  

const struct venus\_resources \*res;  

void \*pkt;  

u32 msg\_ret;

```
if (!hdev)  
	return IRQ_NONE;  

res = hdev->core->res;  
pkt = hdev->pkt_buf;  


while (!venus_iface_msgq_read(hdev, pkt)) {  <-------- read packet from share memory  
	msg_ret = hfi_process_msg_packet(core, pkt);  <----------- process packet  
	switch (msg_ret) {  
	case HFI_MSG_EVENT_NOTIFY:  
		venus_process_msg_sys_error(hdev, pkt);  
		break;  
	case HFI_MSG_SYS_INIT:  
		venus_hfi_core_set_resource(core, res->vmem_id,  
					    res->vmem_size,  
					    res->vmem_addr,  
					    hdev);  
		break;  
	case HFI_MSG_SYS_RELEASE_RESOURCE:  
		complete(&hdev->release_resource);  
		break;  
	case HFI_MSG_SYS_PC_PREP:  
		complete(&hdev->pwr_collapse_prep);  
		break;  
	default:  
		break;  
	}  
}  

venus_flush_debug_queue(hdev);  

return IRQ_HANDLED;  

```

}

In hfi\_process\_msg\_packet, it will find correponding handler from the handlers table.  

This bug is in call path:  

hfi\_process\_msg\_packet -> ... -> hfi\_parser -> parse\_raw\_formats

In function parse\_raw\_formats:  

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.15/drivers/media/platform/qcom/venus/hfi_parser.c;drc=eb09ee77f7f8fb33ea76385333b7abcb5fc79bd9;l=145>

static void  

parse\_raw\_formats(struct venus\_core \*core, u32 codecs, u32 domain, void \*data)  

{  

struct hfi\_uncompressed\_format\_supported \*fmt = data; <----------- data is the ipc packet  

struct hfi\_uncompressed\_plane\_info \*pinfo = fmt->plane\_info;  

struct hfi\_uncompressed\_plane\_constraints \*constr;  

struct raw\_formats rawfmts[MAX\_FMT\_ENTRIES] = {};  

u32 entries = fmt->format\_entries; <-------- entries is from ipc  

unsigned int i = 0;  

u32 num\_planes;

```
while (entries) {      <--------- doesn't check the entries  
	num_planes = pinfo->num_planes;  

	rawfmts[i].fmt = pinfo->format;        <--------- stack buffer overflow  
	rawfmts[i].buftype = fmt->buffer_type; <--------- stack buffer overflow  
	i++;  

	if (pinfo->num_planes > MAX_PLANES)  
		break;  

	pinfo = (void \*)pinfo + sizeof(\*constr) \* num_planes +  
		2 \* sizeof(u32);  
	entries--;  
}  

for_each_codec(core->caps, ARRAY_SIZE(core->caps), codecs, domain,  
	       fill_raw_fmts, rawfmts, i); <--------- here i is a big value, heap buffer overflow!!  

```

}

Patch:

diff --git a/drivers/media/platform/qcom/venus/hfi\_parser.c b/drivers/media/platform/qcom/venus/hfi\_parser.c  

index 6cf74b2bc5ae..1ece52ae0c46 100644  

--- a/drivers/media/platform/qcom/venus/hfi\_parser.c  

+++ b/drivers/media/platform/qcom/venus/hfi\_parser.c  

@@ -152,6 +152,9 @@ parse\_raw\_formats(struct venus\_core \*core, u32 codecs, u32 domain, void \*data)  

unsigned int i = 0;  

u32 num\_planes;

- ```
    if (entries > MAX_FMT_ENTRIES)  
  
  ```
- ```
            return;  
  
  ```
- ```
    while (entries) {  
            num_planes = pinfo->num_planes;  
  
  ```

**VERSION**  

strongbad or trogdor, latest v5.15 kernel code

**CREDIT INFORMATION**

Reporter credit: [lovepink]

## Attachments

- [venus_1_fix.patch](attachments/venus_1_fix.patch) (text/plain, 557 B)
- [1453927.diff](attachments/1453927.diff) (text/plain, 1.3 KB)

## Timeline

### [Deleted User] (2023-06-11)

[Empty comment from Monorail migration]

### pi...@gmail.com (2023-06-11)

Sorry, the "venus dsp" description may not correct, the venus firmware is arm 32bit elf, so maybe it's arm processor not a dsp

### ar...@google.com (2023-06-12)

[Empty comment from Monorail migration]

### ch...@google.com (2023-06-13)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/286980477). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.”



[Monorail blocking: b/286980477]

### [Deleted User] (2023-06-13)

[Empty comment from Monorail migration]

### ch...@google.com (2023-08-14)

I created a FROMLIST CL: https://crrev.com/c/4766224. The commit that resolves this issue was already reviewed upstream, so there should hopefully be no changes when it lands. We are still engaged with Qualcomm to get a V2 patch series up, reviewed and eventually into the kernel. Landing this CL should let us resolve this ticket in the meantime.

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

### ch...@google.com (2023-09-19)

Exploitability: Not exploitable by itself. Requires arbitrary code execution on the Venus hardware decoder (which has had atleast one AV:N as noted).

Privileges and Capabilities: Kernel stack and heap write.

Origin of fix: Not known upstream until reported by the reporter

Mitigations: See exploitability

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

This issue was migrated from crbug.com/chromium/1453927?no_tracker_redirect=1

[Monorail blocking: b/286980477]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065630)*
