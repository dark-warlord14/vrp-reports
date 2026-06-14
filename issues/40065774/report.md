# Security: Chrome OS: OOB read and write in venus_read_queue and venus_write_queue of venus driver

| Field | Value |
|-------|-------|
| **Issue ID** | [40065774](https://issues.chromium.org/issues/40065774) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | pi...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-06-13 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

Background:

venus is responsible for video hardware codec, it supports some complicated codecs.  

When chrome browses a video web page, if codec matches, chrome browser will send the video buffer to venus driver, venus driver will send to venus firmware to decode.

So venus firmware itself is a remote attack surface from chrome browser, and usually firmware has little mitigations than application processor, like this venus firmware exploit:  

<https://i.blackhat.com/USA-19/Wednesday/us-19-Gong-Bypassing-The-Maginot-Line-Remotely-Exploit-The-Hardware-Decoder-On-Smartphone.pdf>

After venus firmware has been compromised remotely, it can't do many things, like in a sandbox.  

But venus firmware can do Inter-Processor Communication with Application Processor, venus linux kernel driver will handle the Inter-Processor Communications from venus firmware.

On strongbad or trogdor chromebooks, they are using venus to do hardware accelerate:  

<https://bugs.chromium.org/p/chromium/issues/detail?id=1198714>

The Bug:

Venus firmware do IPC with venus driver via share memory message queues.

In function venus\_interface\_queues\_init, it will initialize the queue address and size:  

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.15/drivers/media/platform/qcom/venus/hfi_venus.c;drc=6886317d165b75dd4f170edff054c951243e12cd;l=766>

In function venus\_run, it will write the queue information to venus register, then venus know how to use the queue:  

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.15/drivers/media/platform/qcom/venus/hfi_venus.c;drc=6886317d165b75dd4f170edff054c951243e12cd;l=510>

After share memory queue setup, venus driver will use infra functions to read/write from/to queue when do ipc.

venus\_write\_queue:  

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.15/drivers/media/platform/qcom/venus/hfi_venus.c;drc=6886317d165b75dd4f170edff054c951243e12cd;l=185>

static int venus\_write\_queue(struct venus\_hfi\_device \*hdev,  

struct iface\_queue \*queue,  

void \*packet, u32 \*rx\_req)  

{  

struct hfi\_queue\_header \*qhdr;  

u32 dwords, new\_wr\_idx;  

u32 empty\_space, rd\_idx, wr\_idx, qsize;  

u32 \*wr\_ptr;

```
if (!queue->qmem.kva)  
	return -EINVAL;  

qhdr = queue->qhdr;  
if (!qhdr)  
	return -EINVAL;  

venus_dump_packet(hdev, packet);  

dwords = (\*(u32 \*)packet) >> 2;      
if (!dwords)  
	return -EINVAL;  

rd_idx = qhdr->read_idx;  <------ get read_idx from share memory, doesn't check, venus firmware can set it  
wr_idx = qhdr->write_idx; <------ get write_idx from share memory, doesn't check, venus firmware can set it  
qsize = qhdr->q_size;     <------ get qsize from share memory, doesn't check, venus firmware can set it  
/\* ensure rd/wr indices's are read from memory \*/  
rmb();  

if (wr_idx >= rd_idx)  
	empty_space = qsize - (wr_idx - rd_idx);  
else  
	empty_space = rd_idx - wr_idx;  

if (empty_space <= dwords) {  
	qhdr->tx_req = 1;  
	/\* ensure tx_req is updated in memory \*/  
	wmb();  
	return -ENOSPC;  
}  

qhdr->tx_req = 0;  
/\* ensure tx_req is updated in memory \*/  
wmb();  

new_wr_idx = wr_idx + dwords;  
wr_ptr = (u32 \*)(queue->qmem.kva + (wr_idx << 2));   <---------- wr_ptr can out of queue memory range  
if (new_wr_idx < qsize) {  
	memcpy(wr_ptr, packet, dwords << 2);  <---------  oob write  
} else {  
	size_t len;  

	new_wr_idx -= qsize;  
	len = (dwords - new_wr_idx) << 2;  
	memcpy(wr_ptr, packet, len);            <------------- oob write  
	memcpy(queue->qmem.kva, packet + len, new_wr_idx << 2); <---------  
}  

```

//skip..  

}

venus\_read\_queue:  

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.15/drivers/media/platform/qcom/venus/hfi_venus.c;drc=6886317d165b75dd4f170edff054c951243e12cd;l=250>

static int venus\_read\_queue(struct venus\_hfi\_device \*hdev,  

struct iface\_queue \*queue, void \*pkt, u32 \*tx\_req)  

{  

struct hfi\_queue\_header \*qhdr;  

u32 dwords, new\_rd\_idx;  

u32 rd\_idx, wr\_idx, type, qsize;  

u32 \*rd\_ptr;  

u32 recv\_request = 0;  

int ret = 0;

```
if (!queue->qmem.kva)  
	return -EINVAL;  

qhdr = queue->qhdr;  
if (!qhdr)  
	return -EINVAL;  

type = qhdr->type;  
rd_idx = qhdr->read_idx; <------ get it from share memory, doesn't check, venus firmware can set it  
wr_idx = qhdr->write_idx; <------ get it from share memory, doesn't check, venus firmware can set it  
qsize = qhdr->q_size; <------ get it from share memory, doesn't check, venus firmware can set it  

/\* make sure data is valid before using it \*/  
rmb();  

//skip...  

rd_ptr = (u32 \*)(queue->qmem.kva + (rd_idx << 2)); <------- rd_ptr can out of queue memory range  
dwords = \*rd_ptr >> 2;  
if (!dwords)  
	return -EINVAL;  

new_rd_idx = rd_idx + dwords;  
if (((dwords << 2) <= IFACEQ_VAR_HUGE_PKT_SIZE) && rd_idx <= qsize) {  
	if (new_rd_idx < qsize) {  
		memcpy(pkt, rd_ptr, dwords << 2);    <----------- oob read from the share memory queue  
	} else {  
		size_t len;  

		new_rd_idx -= qsize;  
		len = (dwords - new_rd_idx) << 2;  
		memcpy(pkt, rd_ptr, len);          <----------- oob read from the share memory queue  
		memcpy(pkt + len, queue->qmem.kva, new_rd_idx << 2); <----------  
	}  
}   

```

//skip...

}

**VERSION**  

strongbad or trogdor chromebooks

**CREDIT INFORMATION**  

Reporter credit: [lovepink]

## Attachments

- [1454624.diff](attachments/1454624.diff) (text/plain, 1.1 KB)

## Timeline

### pi...@gmail.com (2023-06-13)

Like previous qcom tickets, I will also report it to qcom and update the status.

### [Deleted User] (2023-06-13)

[Empty comment from Monorail migration]

### dc...@chromium.org (2023-06-14)

[Empty comment from Monorail migration]

### ch...@google.com (2023-06-14)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/287208685). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.



[Monorail blocking: b/287208685]

### [Deleted User] (2023-06-14)

[Empty comment from Monorail migration]

### ch...@google.com (2023-08-14)

Project: chromiumos/third_party/kernel
Branch: chromeos-5.15

commit f079843ec3d749e30452911bfb77d779bf0ca807
Author: Vikash Garodia <quic_vgarodia@quicinc.com>
Date:   Thu Jul 27 10:04:26 2023

    FROMLIST: venus: hfi: add checks to perform sanity on queue pointers
   
    Read and write pointers are used to track the packet index in the memory
    shared between video driver and firmware. There is a possibility of OOB
    access if the read or write pointer goes beyond the queue memory size.
    Add checks for the read and write pointer to avoid OOB access.
   
    Cc: stable@vger.kernel.org
    Fixes: d96d3f30c0f2 ("[media] media: venus: hfi: add Venus HFI files")
    Signed-off-by: Vikash Garodia <quic_vgarodia@quicinc.com>
    (am from https://patchwork.kernel.org/patch/13328721/)
    (also found at https://lore.kernel.org/r/1690432469-14803-2-git-send-email-quic_vgarodia@quicinc.com)
   
    UPSTREAM-TASK=b:295178594
    BUG=b:287208685
    TEST=Compiles. Will watch Trogdor test results
   
    Change-Id: Icaf0c1ce1480cc13d5cf27e1a6f9729f8a660293
    Signed-off-by: Nathan Hebert <nhebert@chromium.org>
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4766222
    Reviewed-by: Stephen Boyd <swboyd@chromium.org>
    Reviewed-by: Sean Paul <sean@poorly.run>

M       drivers/media/platform/qcom/venus/hfi_venus.c

https://chromium-review.googlesource.com/4766222
04:13
04:13
CLs: Merged:​<none>      crrev/c/4766222
CLs: Pending:​crrev/c/4766222      <none>

### [Deleted User] (2023-08-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-14)

[Empty comment from Monorail migration]

### pi...@gmail.com (2023-08-20)

PoC method.

These venus driver issues are straightforward and have been confirmed by Qcom Security Team and Dev Team, but for PoC it is hard to modify venus binary firmware to set the queue fields in share memory. 

Because this bug is straightforward, so we can modify linux kernel to simulate firmware to set the queue fields.

A PoC idea is patch linux kernel to set the queue fields to malicious in function venus_write_queue, and open chrome browser to visit hardware decoding video to trigger IPC from firmware, when hit venus_write_queue it can use the malicious queue fields (and above fix patch should also defend this poc method)

I try to give a PoC patch of Linux kernel, but strongbad test image seems can't boot correctly on my strongbad chromebook while kukui and hana all are OK, I don't know why:
1, build test kernel image with attached diff, deploy to device
2, may crash on boot, because when booting the venus firmware may contact with linux kernel with IPC messages
3, if boot not crash, use chrome browser to visit the official video test url and play the video: http://crosvideo.appspot.com/?codec=vp8




### am...@chromium.org (2023-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-12-12)

[Empty comment from Monorail migration]

### ch...@google.com (2023-12-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-12)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2023-12-15)

[Empty comment from Monorail migration]

### is...@google.com (2023-12-15)

This issue was migrated from crbug.com/chromium/1454624?no_tracker_redirect=1

[Monorail blocking: b/287208685]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065774)*
