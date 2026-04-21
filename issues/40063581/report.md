# Security: out of bound read in vfd_out_locked

| Field | Value |
|-------|-------|
| **Issue ID** | [40063581](https://issues.chromium.org/issues/40063581) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | sy...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-03-14 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

There is an out of bound read in vfd\_out\_locked(drivers/virtio/virtio\_wl.c):

```
static ssize_t vfd_out_locked(struct virtwl_vfd \*vfd, char __user \*buffer,  
			      size_t len)  
{  
		[...]  
		size_t recv_offset = sizeof(\*recv) + recv->vfd_count \*  
				     sizeof(__le32) + qentry->data_offset;     [1] recv->vfd_count contorlled by attacker, so recv_offset can be contorlled  
		u8 \*buf = (u8 \*)recv + recv_offset;					   [2] buf ptr controlled by attacker  
		ssize_t to_read = (ssize_t)qentry->len - (ssize_t)recv_offset;  
  
		if (qentry->hdr->type != VIRTIO_WL_CMD_VFD_RECV)  
			continue;  
  
		if ((to_read + read_count) > len)  
			to_read = len - read_count;  
  
		if (copy_to_user(buffer + read_count, buf, to_read)) { [3] tigger out of bound read  
			read_count = -EFAULT;  
			break;  
		}  
		[...]  

```

If attacker control recv buffer, attacker can controll buf ptr[1][2], then tigger out of bound read at copy\_to\_user[3]

**VERSION**  

Chrome Version: 110.0.5481.181  

Operating System: chromeos 5.10.159-20950-g3963226d9eb4

**REPRODUCTION CASE**

I audit this vulnerability and still working for a poc.

## Timeline

### [Deleted User] (2023-03-14)

[Empty comment from Monorail migration]

### ts...@chromium.org (2023-03-14)

Over to ChromeOS rotation.

### th...@google.com (2023-03-20)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-24)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-22)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/283747290. You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting  Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.



### [Deleted User] (2023-05-22)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-23)

[Empty comment from Monorail migration]

[Monorail blocking: b/283747290]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ch...@google.com (2023-06-12)

Project: chromiumos/third_party/kernel
Branch: chromeos-5.15

commit 1238c4742f0edd19723ae9950a12fbcf7157fe59
Author: David Stevens <stevensd@chromium.org>
Date:   Tue Jun 06 11:18:40 2023

    CHROMIUM: virtwl: fixes for vfd_out_locked
   
    Add a missing bounds check and fix a potential integer overflow in
    vfd_out_lock.
   
    BUG=b:283747290
    TEST=tast run DUT arc.Boot.vm
   
    Change-Id: I7ac37921f8e89904d28b32ee183667502e32eb51
    Signed-off-by: David Stevens <stevensd@chromium.org>
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4592734
    Reviewed-by: Suleiman Souhlal <suleiman@chromium.org>
    (cherry picked from commit 5deb2eda861b2af69834632efffc40f848871bfd)
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4600221

M       drivers/virtio/virtio_wl.c

https://chromium-review.googlesource.com/4600221

The fix is in both our VM kernels, as well as 6.1

### [Deleted User] (2023-06-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-12)

[Empty comment from Monorail migration]

### ch...@google.com (2023-06-20)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-18)

[Comment Deleted]

### am...@chromium.org (2023-08-18)

Congratulations! The VRP Panel has decided to award you $1,000 for this report of an OOB read in the ChromeOS guest kernel. This report may have been eligible for a higher reward had it been of at least baseline quality [1], such as consisting of a stack trace, a POC, and/or steps to reproduce, and information as to how this could be exploited. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us! 

[1] https://g.co/chrome/vrp/#report-quality

### am...@google.com (2023-08-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-09-18)

This issue was migrated from crbug.com/chromium/1424270?no_tracker_redirect=1

[Monorail blocking: b/283747290]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063581)*
