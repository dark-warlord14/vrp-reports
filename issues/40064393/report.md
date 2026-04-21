# Security: Race Condition in amdgpu_ttm_tt_get_user_pages

| Field | Value |
|-------|-------|
| **Issue ID** | [40064393](https://issues.chromium.org/issues/40064393) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | yq...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-05-06 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

I found that this uaf vulnerability does not exist in linux kernel 5.10, but this problem exists in chromeos kernel 5.10.

When you mmap() the gem object, amdgpu\_gem\_object\_mmap() records  

the pointers to the mm\_struct and the VMA. When you unmap the VMA (or any VMA that was forked from this  

VMA), the vm\_operations\_struct::close handler ttm\_bo\_vm\_close() clears out the  

vma pointer.  

When amdgpu\_ttm\_tt\_get\_user\_pages() wants to access the VMA,amdgpu\_ttm\_tt\_get\_user\_pages expose to amdgpu\_gem\_userptr\_ioctl.  

It locks when looking for vma, but the subsequent vma object operation is outside the scope of the lock. So there can be race UAF.

int amdgpu\_ttm\_tt\_get\_user\_pages(struct amdgpu\_bo \*bo, struct page \*\*pages)  

{  

struct ttm\_tt \*ttm = bo->tbo.ttm;  

struct amdgpu\_ttm\_tt \*gtt = (void \*)ttm;  

unsigned long start = gtt->userptr;  

struct vm\_area\_struct \*vma;  

struct mm\_struct \*mm;  

bool readonly;  

int r = 0;

```
mm = bo->notifier.mm;  
if (unlikely(!mm)) {  
	DRM_DEBUG_DRIVER("BO is not registered?\n");  
	return -EFAULT;  
}  

/\* Another get_user_pages is running at the same time?? \*/  
if (WARN_ON(gtt->range))  
	return -EFAULT;  

if (!mmget_not_zero(mm)) /\* Happens during process shutdown \*/  
	return -ESRCH;  

mmap_read_lock(mm);  
vma = find_vma(mm, start);  
mmap_read_unlock(mm);  
if (unlikely(!vma || start < vma->vm_start)) {  
	r = -EFAULT;  
	goto out_putmm;  
}  
if (unlikely((gtt->userflags & AMDGPU_GEM_USERPTR_ANONONLY) &&  
	vma->vm_file)) {  
	r = -EPERM;  
	goto out_putmm;  
}  

readonly = amdgpu_ttm_tt_is_readonly(ttm);  
r = amdgpu_hmm_range_get_pages(&bo->notifier, mm, pages, start,  
			       ttm->num_pages, &gtt->range, readonly,  
			       false, NULL);  

```

out\_putmm:  

mmput(mm);

```
return r;  

```

}

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.10/drivers/gpu/drm/amd/amdgpu/amdgpu_ttm.c;l=658;bpv=0>

**VERSION**  

Operating System: chromeos kernel 5.10

Components: gpu

Patch

--- a/driver/gpu/drm/amd/amdgpu/amdgpu\_ttm.c  

+++ b/driver/gpu/drm/amd/amdgpu/amdgpu\_ttm.c  

@@ -680,7 +680,7 @@ int amdgpu\_ttm\_tt\_get\_user\_pages(struct

```
mmap_read_lock(mm);  
vma = find_vma(mm, start);  

```

- mmap\_read\_unlock(mm);

- if (unlikely(!vma || start < vma->vm\_start)) {  
  
  r = -EFAULT;  
  
  goto out\_putmm;  
  
  @@ -696,6 +696,7 @@ int amdgpu\_ttm\_tt\_get\_user\_pages(struct  
  
  ttm->num\_pages, &gtt->range, readonly,  
  
  false, NULL);  
  
  out\_putmm:
- mmap\_read\_unlock(mm);  
  
  mmput(mm);
  
  return r;

## Timeline

### [Deleted User] (2023-05-06)

[Empty comment from Monorail migration]

### yq...@gmail.com (2023-05-06)

Because there is no AMD device test, there is no Kasan, but POC I am trying to construct.

### nh...@google.com (2023-05-08)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-08)

[Empty comment from Monorail migration]

[Monorail blocking: b/281467238]

### ch...@google.com (2023-05-08)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/281467238). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on.

### ch...@google.com (2023-05-24)

Project: chromiumos/third_party/kernel
Branch: release-R114-15437.B-chromeos-5.10

commit c952fc054dac8eb6f1f11054de5ecd37d56f80c7
Author: Chia-I Wu <olv@google.com>
Date:   Sun May 21 10:55:56 2023

    CHROMIUM: drm/amdgpu: fix a race in amdgpu_ttm_tt_get_user_pages
   
    This is a backport of commit e058a84bfddc ("Merge tag
    'drm-next-2021-07-01' of git://anongit.freedesktop.org/drm/drm").  The
    merge fixed the race when resolving the merge conflict.
   
    BUG=b:281467238
    TEST=CQ
   
    Change-Id: I063f4330f9ab781938e872d7d68f441d36a717c5
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4550869
    Tested-by: Chia-I Wu <olv@google.com>
    Reviewed-by: Rob Clark <robdclark@chromium.org>
    Commit-Queue: Chia-I Wu <olv@google.com>
    (cherry picked from commit 612ec1b0599b6b500d7993d746f9f0424812e5f9)
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4551292
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Auto-Submit: Chia-I Wu <olv@google.com>

M       drivers/gpu/drm/amd/amdgpu/amdgpu_ttm.c

https://chromium-review.googlesource.com/4551292
21:40
21:40
CLs: Merged:​crrev/c/4550869      crrev/c/4550869, crrev/c/4551292
CLs: Pending:​crrev/c/4551292      <none>

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-26)

[Empty comment from Monorail migration]

### st...@google.com (2023-06-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-03)

This bug is a regression and does not impact stable or extended stable.Removing incorrectly added Release- labels.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### st...@google.com (2023-06-05)

[Empty comment from Monorail migration]

### am...@google.com (2023-06-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### yq...@gmail.com (2023-06-16)

Hello Amy,why this pay only for 1000?

### am...@chromium.org (2023-06-16)

Thank you for this report. The VRP Panel has decided to award you $1,000 for this report based on that this issue was known and fixed upstream prior to this report. 

### am...@google.com (2023-06-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-08-30)

This issue was migrated from crbug.com/chromium/1443107?no_tracker_redirect=1

[Monorail blocking: b/281467238]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064393)*
