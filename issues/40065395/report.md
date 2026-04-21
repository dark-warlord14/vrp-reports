# Security: OOB in vb2ops_venc_queue_setup

| Field | Value |
|-------|-------|
| **Issue ID** | [40065395](https://issues.chromium.org/issues/40065395) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | yq...@gmail.com |
| **Assignee** | st...@google.com |
| **Created** | 2023-06-06 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

This vulnerability has been fixed in the vb2ops\_vdec\_queue\_setup function, but not in vb2ops\_venc\_queue\_setup.

variable \*nplanes is provided by user via system call argument. The  

possible value of q\_data->fmt->num\_planes is 1-3, while the value  

of \*nplanes can be 1-8. The array access by index i can cause array  

out-of-bounds.

static int vb2ops\_venc\_queue\_setup(struct vb2\_queue \*vq,  

unsigned int \*nbuffers,  

unsigned int \*nplanes,  

unsigned int sizes[],  

struct device \*alloc\_devs[])  

{  

struct mtk\_vcodec\_ctx \*ctx = vb2\_get\_drv\_priv(vq);  

struct mtk\_q\_data \*q\_data;  

unsigned int i;

```
q_data = mtk_venc_get_q_data(ctx, vq->type);  

if (q_data == NULL)  
	return -EINVAL;  

if (\*nplanes) {  
	for (i = 0; i < \*nplanes; i++)  
		if (sizes[i] < q_data->sizeimage[i])  
			return -EINVAL;  
} else {  
	\*nplanes = q_data->fmt->num_planes;  
	for (i = 0; i < \*nplanes; i++)  
		sizes[i] = q_data->sizeimage[i];  
}  

return 0;  

```

}

**REPRODUCTION CASE**  

(Since I don't have a mediatek chromebook for testing, I can only blindly guess the following poc construction.I will continue the in-depth investigation of poc)  

1.copy this code  

2. change req.type = V4L2\_BUF\_TYPE\_VIDEO\_CAPTURE to req.type =V4L2\_BUF\_TYPE\_VIDEO\_CAPTURE\_MPLANE  

3../capture\_raw\_frames -d /dev/video6 -m -c 1 -o

Patch

see <https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=8fbcf730cb89c3647f3365226fe7014118fa93c7>

## Timeline

### [Deleted User] (2023-06-06)

[Empty comment from Monorail migration]

### aj...@google.com (2023-06-06)

-> ChromeOS for triage

### st...@google.com (2023-06-07)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/286212985). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

### st...@google.com (2023-06-07)

[Empty comment from Monorail migration]

### ch...@google.com (2023-06-12)

[Empty comment from Monorail migration]

[Monorail blocked-on: b/286212985]

### ch...@google.com (2023-08-10)

Project: chromiumos/third_party/kernel
Branch: chromeos-5.10

commit ca6f918123bf4295fbce4f83594395ffa94da8f7
Author: Wei Chen <harperchen1110@gmail.com>
Date:   Tue Mar 28 09:26:08 2023

    FROMLIST: media: vcodec: Fix potential array out-of-bounds in vb2ops_venc_queue_setup
   
    variable *nplanes is provided by user via system call argument. The
    possible value of q_data->fmt->num_planes is 1-3, while the value
    of *nplanes can be 1-8. The array access by index i can cause array
    out-of-bounds.
   
    Fix this bug by checking *nplanes against the array size.
   
    Signed-off-by: Wei Chen <harperchen1110@gmail.com>
    Reviewed-by: Tomasz Figa <tfiga@chromium.org>
    (am from https://patchwork.kernel.org/patch/13190708/)
    (also found at https://lore.kernel.org/r/20230328092608.523933-1-harperchen1110@gmail.com)
   
    BUG=b:286212985
    UPSTREAM-TASK=b:295066113
    TEST=Compiles. Will watch Kukui Tast test results
   
    Change-Id: I839c665737011dded551137cbb256e15fd1e3c44
    Signed-off-by: Nathan Hebert <nhebert@chromium.org>
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4763407
    Reviewed-by: Chen-Yu Tsai <wenst@chromium.org>
    Reviewed-by: Sean Paul <sean@poorly.run>

M       drivers/media/platform/mediatek/vcodec/mtk_vcodec_enc.c

https://chromium-review.googlesource.com/4763407
15:53
15:53
CLs: Merged:​crrev/c/4720055, crrev/c/4720056, crrev/c/4720057, crrev/c/4723203, crrev/c/4763409, crrev/c/4763604, crrev/c/4763605, crrev/c/4763606      crrev/c/4720055, crrev/c/4720056, crrev/c/4720057, crrev/c/4723203, crrev/c/4763407, crrev/c/4763409, crrev/c/4763604, crrev/c/4763605, crrev/c/4763606
CLs: Pending:​crrev/c/4763407      <none>

### [Deleted User] (2023-08-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-10)

[Empty comment from Monorail migration]

### st...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### ch...@google.com (2023-09-19)

Exploitability: Not exploitable by itself. Requires control of the chromeos video stack to inject arbitrary pixel formats.

Privileges and Capabilities: Kernel heap read with limited control over address

Origin of fix: Not known upstream until reported by the reporter

Mitigations: See exploitability

Severity Assessment: Medium severity since this is an OOB read in the kernel, although one could argue that it should be low given the lack of range (no arbitrary reads).

### am...@chromium.org (2023-09-26)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-26)

Congratulations! 
The VRP Panel has decided to award you $500 for this report. 
A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in discovering and reporting this issue to us -- great work! 
Please be mindful that previous reward decisions made by the Chrome VRP should not be considered precedent for potential future ChromeOS VRP reward amounts or decisions.

Can you please send us your desired credit name? --> e.g. yqsun1997

### yq...@gmail.com (2023-10-27)

credit name

Sunyuqin

### am...@google.com (2023-10-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-11-16)

This issue was migrated from crbug.com/chromium/1451680?no_tracker_redirect=1

[Monorail blocked-on: b/286212985]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065395)*
