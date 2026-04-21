# Security: Chrome OS: Multiple Heap Buffer OOB write bugs in venus driver because of reenter in hfi_parser function

| Field | Value |
|-------|-------|
| **Issue ID** | [40065633](https://issues.chromium.org/issues/40065633) |
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

hfi\_process\_msg\_packet -> ... -> hfi\_parser

In hfi\_parser, there is a while loop to parse different types data:  

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.15/drivers/media/platform/qcom/venus/hfi_parser.c;drc=eb09ee77f7f8fb33ea76385333b7abcb5fc79bd9;l=287>

```
while (words_count) {                <----------- based on ipc data size  
	data = word + 1;             <----------- data from ipc  

	switch (\*word) {  
	case HFI_PROPERTY_PARAM_CODEC_SUPPORTED:  
		parse_codecs(core, data);  
		init_codecs(core);  
		break;  
	case HFI_PROPERTY_PARAM_MAX_SESSIONS_SUPPORTED:  
		parse_max_sessions(core, data);  
		break;  
	case HFI_PROPERTY_PARAM_CODEC_MASK_SUPPORTED:  
		parse_codecs_mask(&codecs, &domain, data);  
		break;  
	case HFI_PROPERTY_PARAM_UNCOMPRESSED_FORMAT_SUPPORTED:  
		parse_raw_formats(core, codecs, domain, data);  
		break;  
	case HFI_PROPERTY_PARAM_CAPABILITY_SUPPORTED:  
		parse_caps(core, codecs, domain, data);  <----------- use this as example  
		break;  
	case HFI_PROPERTY_PARAM_PROFILE_LEVEL_SUPPORTED:  
		parse_profile_level(core, codecs, domain, data);  
		break;  
	case HFI_PROPERTY_PARAM_BUFFER_ALLOC_MODE_SUPPORTED:  
		parse_alloc_mode(core, codecs, domain, data);  
		break;  
	default:  
		break;  
	}  

	word++;  
	words_count--;  
}  

```

Above while loop's original design is to parse each type in one iterate, but if we let the while loop reenter some type handler functions, it will cause heap buffer OOB write.

Use parse\_caps as example, parse\_caps has correct bounds check:

static void  

parse\_caps(struct venus\_core \*core, u32 codecs, u32 domain, void \*data)  

{  

struct hfi\_capabilities \*caps = data; <------------- ipc data  

struct hfi\_capability \*cap = caps->data;  

u32 num\_caps = caps->num\_capabilities; <--------------- num\_caps from ipc data  

struct hfi\_capability caps\_arr[MAX\_CAP\_ENTRIES] = {};

```
if (num_caps > MAX_CAP_ENTRIES)         <----------------- has bounds check  
	return;  

memcpy(caps_arr, cap, num_caps \* sizeof(\*cap));  

for_each_codec(core->caps, ARRAY_SIZE(core->caps), codecs, domain,  
	       fill_caps, caps_arr, num_caps); <-------------------- here will call fill_caps  

```

}

static void  

fill\_caps(struct hfi\_plat\_caps \*cap, const void \*data, unsigned int num)  

{  

const struct hfi\_capability \*caps = data;

```
memcpy(&cap->caps[cap->num_caps], caps, num \* sizeof(\*caps));  <-------- according to parse_caps, num will not bigger than MAX_CAP_ENTRIES  
cap->num_caps += num;   <------------- cap->num_caps now is MAX_CAP_ENTRIES, if reenter parse_caps again in while loop of hfi_parser, OOB write!  

```

}

For example, the cap->num\_caps above now is MAX\_CAP\_ENTRIES, if we construct the ipc data to reenter parse\_caps in next iterates of the hfi\_parser while loop, will cause OOB write in the memcpy of fill\_caps.

Patch:

diff --git a/drivers/media/platform/qcom/venus/hfi\_parser.c b/drivers/media/platform/qcom/venus/hfi\_parser.c  

index 6cf74b2bc5ae..49548ec8dcc4 100644  

--- a/drivers/media/platform/qcom/venus/hfi\_parser.c  

+++ b/drivers/media/platform/qcom/venus/hfi\_parser.c  

@@ -86,6 +86,9 @@ static void fill\_profile\_level(struct hfi\_plat\_caps \*cap, const void \*data,  

{  

const struct hfi\_profile\_level \*pl = data;

- ```
    if (cap->num_pl >= HFI_MAX_PROFILE_COUNT)  
  
  ```
- ```
            return;  
  
  ```
- ```
    memcpy(&cap->pl[cap->num_pl], pl, num \* sizeof(\*pl));  
    cap->num_pl += num;  
  
  ```

}  

@@ -111,6 +114,9 @@ fill\_caps(struct hfi\_plat\_caps \*cap, const void \*data, unsigned int num)  

{  

const struct hfi\_capability \*caps = data;

- ```
    if (cap->num_caps >= MAX_CAP_ENTRIES)  
  
  ```
- ```
            return;  
  
  ```
- ```
    memcpy(&cap->caps[cap->num_caps], caps, num \* sizeof(\*caps));  
    cap->num_caps += num;  
  
  ```

}  

@@ -137,6 +143,9 @@ static void fill\_raw\_fmts(struct hfi\_plat\_caps \*cap, const void \*fmts,  

{  

const struct raw\_formats \*formats = fmts;

- ```
    if (cap->num_fmts >= MAX_FMT_ENTRIES)  
  
  ```
- ```
            return;  
  
  ```
- ```
    memcpy(&cap->fmts[cap->num_fmts], formats, num_fmts \* sizeof(\*formats));  
    cap->num_fmts += num_fmts;  
  
  ```

}

**VERSION**

strongbad or trogdor, latest v5.15 kernel code

**CREDIT INFORMATION**

Reporter credit: [lovepink]

## Attachments

- deleted (application/octet-stream, 0 B)
- [1453935.diff](attachments/1453935.diff) (text/plain, 2.6 KB)

## Timeline

### pi...@gmail.com (2023-06-11)

According to function venus_interface_queues_init, the max ipc data size in each queue is ~2K, so it's big enough to reenter many times to OOB write

https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.15/drivers/media/platform/qcom/venus/hfi_venus.c;l=787

### [Deleted User] (2023-06-11)

[Empty comment from Monorail migration]

### ar...@google.com (2023-06-12)

[Empty comment from Monorail migration]

### ch...@google.com (2023-06-13)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/286984316). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.”

[Monorail blocking: b/286984316]

### [Deleted User] (2023-06-13)

[Empty comment from Monorail migration]

### pi...@gmail.com (2023-06-14)

My patch above is not correct, please see my update in the issuertracker b/286984316

### ch...@google.com (2023-08-14)

I created a FROMLIST CL: https://crrev.com/c/4766224. There is a second CHROMIUM CL, https://crrev.com/c/4766225, which addresses review feedback from the linux-media mailing list. We are still engaged with Qualcomm to get a V2 patch series up, reviewed and eventually into the kernel. Landing this CL should let us resolve this ticket in the meantime.

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

Privileges and Capabilities: Kernel heap write. Unknown if this can be escalated to arbitrary code execution without e.g help from userspace.

Origin of fix: Not known upstream until reported by the reporter

Mitigations: See exploitability

Severity Assessment: Medium. Memory corruption that's not directly triggerable from an exposed interface.

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

This issue was migrated from crbug.com/chromium/1453935?no_tracker_redirect=1

[Monorail blocking: b/286984316]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065633)*
