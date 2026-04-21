# Security: Chrome OS: Heap Buffer OOB write in function init_codecs of venus driver

| Field | Value |
|-------|-------|
| **Issue ID** | [40065632](https://issues.chromium.org/issues/40065632) |
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

hfi\_process\_msg\_packet -> ... -> hfi\_parser -> parse\_codecs & init\_codecs

hfi\_parser will parse venus attributes from firmware:  

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.15/drivers/media/platform/qcom/venus/hfi_parser.c;drc=eb09ee77f7f8fb33ea76385333b7abcb5fc79bd9;l=266>

```
while (words_count) {  
	data = word + 1;  

	switch (\*word) {  
	case HFI_PROPERTY_PARAM_CODEC_SUPPORTED:  
		parse_codecs(core, data);  <---------- get codecs  
		init_codecs(core);         <---------- init structure according above codes  
		break;  
	case HFI_PROPERTY_PARAM_MAX_SESSIONS_SUPPORTED:  
		parse_max_sessions(core, data);  
		break;  

	//skip...  

	default:  
		break;  
	}  

	word++;  
	words_count--;  
}  

```

In parse\_codecs, it will get codes from venus ipc data:  

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.15/drivers/media/platform/qcom/venus/hfi_parser.c;drc=eb09ee77f7f8fb33ea76385333b7abcb5fc79bd9;l=174>  

static void parse\_codecs(struct venus\_core \*core, void \*data)  

{  

struct hfi\_codec\_supported \*codecs = data;

```
core->dec_codecs = codecs->dec_codecs; <--------- get dec_codes, uint32, can have 32 bits set  
core->enc_codecs = codecs->enc_codecs; <---------- get enc_codes, uint32, can have 32 bits set  

if (IS_V1(core)) {                    <---------- venus version is 5.4, not V1  
	core->dec_codecs &= ~HFI_VIDEO_CODEC_HEVC;  
	core->dec_codecs &= ~HFI_VIDEO_CODEC_SPARK;  
	core->enc_codecs &= ~HFI_VIDEO_CODEC_HEVC;  
}  

```

}

In init\_codecs, it will init structure according to core->dec\_codecs and core->enc\_codecs:  

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.15/drivers/media/platform/qcom/venus/hfi_parser.c;drc=eb09ee77f7f8fb33ea76385333b7abcb5fc79bd9;l=17>  

static void init\_codecs(struct venus\_core \*core)  

{  

struct hfi\_plat\_caps \*caps = core->caps, \*cap; <-------- core->caps array size is 32  

unsigned long bit;

```
for_each_set_bit(bit, &core->dec_codecs, MAX_CODEC_NUM) {  
	cap = &caps[core->codecs_count++];  <------------ core->dec_codecs can have 32 bits set  
	cap->codec = BIT(bit);  
	cap->domain = VIDC_SESSION_TYPE_DEC;  
	cap->valid = false;  
}  

for_each_set_bit(bit, &core->enc_codecs, MAX_CODEC_NUM) {  
	cap = &caps[core->codecs_count++]; <------------ core->enc_codecs can have 32 bits set, OOB write  
	cap->codec = BIT(bit);     <-------------- OOB write  
	cap->domain = VIDC_SESSION_TYPE_ENC; <-------------- OOB write  
	cap->valid = false; <-------------- OOB write  
}  

```

}

You can see above, core->caps array size is MAX\_CODEC\_NUM(32), so the second for loop can cause heap buffer OOB write.

Patch:

Below patch calculate the bits in codecs, so bits + core->codecs\_count should not bigger than 32.

diff --git a/drivers/media/platform/qcom/venus/hfi\_parser.c b/drivers/media/platform/qcom/venus/hfi\_parser.c  

index 6cf74b2bc5ae..0d686828d86c 100644  

--- a/drivers/media/platform/qcom/venus/hfi\_parser.c  

+++ b/drivers/media/platform/qcom/venus/hfi\_parser.c  

@@ -19,6 +19,9 @@ static void init\_codecs(struct venus\_core \*core)  

struct hfi\_plat\_caps \*caps = core->caps, \*cap;  

unsigned long bit;

- ```
    if (hweight_long(core->dec_codecs) + hweight_long(core->enc_codecs) + core->codecs_count > MAX_CODEC_NUM)  
  
  ```
- ```
            return;  
  
  ```
- ```
    for_each_set_bit(bit, &core->dec_codecs, MAX_CODEC_NUM) {  
            cap = &caps[core->codecs_count++];  
            cap->codec = BIT(bit);  
  
  ```

**VERSION**  

strongbad or trogdor, latest v5.15 kernel code

**CREDIT INFORMATION**  

Reporter credit: [lovepink]

## Attachments

- [venus_2_fix.patch](attachments/venus_2_fix.patch) (text/plain, 715 B)
- [1453934.diff](attachments/1453934.diff) (text/plain, 934 B)

## Timeline

### [Deleted User] (2023-06-11)

[Empty comment from Monorail migration]

### ar...@google.com (2023-06-12)

[Empty comment from Monorail migration]

### ch...@google.com (2023-06-13)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/286979641). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.”

[Monorail blocking: b/286979641]

### [Deleted User] (2023-06-13)

[Empty comment from Monorail migration]

### ch...@google.com (2023-08-14)

Project: chromiumos/third_party/kernel
Branch: chromeos-5.15

commit dfec4e9726df8b087e4b81173ef12b1beb79eed7
Author: Vikash Garodia <quic_vgarodia@quicinc.com>
Date:   Thu Jul 27 10:04:29 2023

    FROMLIST: venus: hfi_parser: Add check to keep the number of codecs within range
   
    Supported codec bitmask is populated from the payload from venus firmware.
    There is a possible case when all the bits in the codec bitmask is set. In
    such case, core cap for decoder is filled  and MAX_CODEC_NUM is utilized.
    Now while filling the caps for encoder, it can lead to access the caps
    array beyong 32 index. Hence leading to OOB write.
    The fix counts the supported encoder and decoder. If the count is more than
    max, then it skips accessing the caps.
   
    Cc: stable@vger.kernel.org
    Fixes: 1a73374a04e5 ("media: venus: hfi_parser: add common capability parser")
    Signed-off-by: Vikash Garodia <quic_vgarodia@quicinc.com>
    (am from https://patchwork.kernel.org/patch/13328724/)
    (also found at https://lore.kernel.org/r/1690432469-14803-5-git-send-email-quic_vgarodia@quicinc.com)
   
    UPSTREAM-TASK=b:295182374
    BUG=b:286979641
    TEST=Compiles. Will watch Trogdor test results
   
    Change-Id: If1123ca65b1db9a8c06a2b863bb73cd6ac2ec3a0
    Signed-off-by: Nathan Hebert <nhebert@chromium.org>
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4766226
    Reviewed-by: Sean Paul <sean@poorly.run>
    Reviewed-by: Stephen Boyd <swboyd@chromium.org>

M       drivers/media/platform/qcom/venus/hfi_parser.c

https://chromium-review.googlesource.com/4766226
04:13
04:13
CLs: Merged:​<none>      crrev/c/4766226, crrev/c/4766227
CLs: Pending:​crrev/c/4766226, crrev/c/4766227      <none>

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

This issue was migrated from crbug.com/chromium/1453934?no_tracker_redirect=1

[Monorail blocking: b/286979641]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065632)*
