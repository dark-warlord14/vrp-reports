# Security: Uninitialized Pointer in `msm_parse_post_deps`

| Field | Value |
|-------|-------|
| **Issue ID** | [40063040](https://issues.chromium.org/issues/40063040) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>VendorSpecific |
| **Platforms** | ChromeOS |
| **Reporter** | lm...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2023-02-12 |
| **Bounty** | $15,000.00 |

## Description

**VULNERABILITY DETAILS**

ioctl$MSM\_GEM\_SUBMIT will call \*msm\_ioctl\_gem\_submit\* to submit gem. If \*MSM\_SUBMIT\_SYNCOBJ\_OUT\* is set in \*args->flags\*, it will call \*msm\_parse\_post\_deps\*. The \*post\_deps\* is allocated by \*kmalloc\_array\*[1] without \*\_\_GFP\_ZERO\* flag which means the memory will not be initialized with zero. So \*post\_deps\* will be filled with the last time used data. If \*copy\_from\_user\*[2] failed, it will break out the for loop, and start the clear work. \*dma\_fence\_chain\_free\*[3] will be call with an uninitialized pointer. The attacker can allocate the same size buffer first, fill it with any data, and then free it. Finally trigger this to call \*dma\_fence\_chain\_free\* with an uninitialized pointer under attacker control.

```
static struct msm_submit_post_dep \*msm_parse_post_deps(struct drm_device \*dev,  
                                                       struct drm_file \*file,  
                                                       uint64_t syncobjs_addr,  
                                                       uint32_t nr_syncobjs,  
                                                       size_t syncobj_stride)  
{  
	struct msm_submit_post_dep \*post_deps;  
	struct drm_msm_gem_submit_syncobj syncobj_desc = {0};  
	int ret = 0;  
	uint32_t i, j;  
  
	post_deps = kmalloc_array(nr_syncobjs, sizeof(\*post_deps),			// [1]  
	                          GFP_KERNEL | __GFP_NOWARN | __GFP_NORETRY);  
	if (!post_deps)  
		return ERR_PTR(-ENOMEM);  
  
	for (i = 0; i < nr_syncobjs; ++i) {  
		uint64_t address = syncobjs_addr + i \* syncobj_stride;  
  
		if (copy_from_user(&syncobj_desc,				// [2]  
			           u64_to_user_ptr(address),  
			           min(syncobj_stride, sizeof(syncobj_desc)))) {  
			ret = -EFAULT;  
			break;  
		}  
  
		post_deps[i].point = syncobj_desc.point;  
		post_deps[i].chain = NULL;  
  
		if (syncobj_desc.flags) {  
			ret = -EINVAL;  
			break;  
		}  
  
		if (syncobj_desc.point) {  
			if (!drm_core_check_feature(dev,  
			                            DRIVER_SYNCOBJ_TIMELINE)) {  
				ret = -EOPNOTSUPP;  
				break;  
			}  
  
			post_deps[i].chain = dma_fence_chain_alloc();  
			if (!post_deps[i].chain) {  
				ret = -ENOMEM;  
				break;  
			}  
		}  
  
		post_deps[i].syncobj =  
			drm_syncobj_find(file, syncobj_desc.handle);  
		if (!post_deps[i].syncobj) {  
			ret = -EINVAL;  
			break;  
		}  
	}  
  
	if (ret) {  
		for (j = 0; j <= i; ++j) {  
			dma_fence_chain_free(post_deps[j].chain);	// [3]  
			if (post_deps[j].syncobj)  
				drm_syncobj_put(post_deps[j].syncobj);  
		}  
  
		kfree(post_deps);  
		return ERR_PTR(ret);  
	}  
  
	return post_deps;  
}  

```

[1] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v6.1/drivers/gpu/drm/msm/msm_gem_submit.c;drc=133a14afb9c2d651523102e1659a851b708b619a;l=626>  

[2] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v6.1/drivers/gpu/drm/msm/msm_gem_submit.c;drc=133a14afb9c2d651523102e1659a851b708b619a;l=634>  

[3] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v6.1/drivers/gpu/drm/msm/msm_gem_submit.c;drc=133a14afb9c2d651523102e1659a851b708b619a;l=673>

**VERSION**  

Operating System: ChromiumOS Kernel 6.1 stable + dev

Bisect:  

<https://source.chromium.org/chromiumos/_/chromium/chromiumos/third_party/kernel/+/ab723b7a992a19b843f798b183f53f7472f598c8>

**REPRODUCTION CASE**  

\*\*It needs to be reproduced in real devices, with specific gpu. Sorry I don't have a chromebook with that gpu. If there is any problem with the poc, please feel free to contact me.\*\*

1. Compile the poc.
2. Run poc in ChromiumOS system. (please make sure current user is in video group. it needs the privilege to access drm to trigger this bug).

FIX PATCH SUGGESTION  

I think the follwing patch should fix the problem. Just like \*msm\_parse\_deps\*, use \*kcalloc\* instead of \*kmalloc\_array\*

```
diff --git a/drivers/gpu/drm/msm/msm_gem_submit.c b/drivers/gpu/drm/msm/msm_gem_submit.c  
index 1af7e7c613a6..93c5e92fe297 100644  
--- a/drivers/gpu/drm/msm/msm_gem_submit.c  
+++ b/drivers/gpu/drm/msm/msm_gem_submit.c  
@@ -633,7 +633,7 @@ static struct msm_submit_post_dep \*msm_parse_post_deps(struct drm_device \*dev,  
        int ret = 0;  
        uint32_t i, j;  
   
-       post_deps = kmalloc_array(nr_syncobjs, sizeof(\*post_deps),  
+       post_deps = kcalloc(nr_syncobjs, sizeof(\*post_deps),  
                                  GFP_KERNEL | __GFP_NOWARN | __GFP_NORETRY);  
        if (!post_deps)  
                return ERR_PTR(-ENOMEM);  

```

## Attachments

- [poc.c](attachments/poc.c) (text/plain, 886 B)

## Timeline

### [Deleted User] (2023-02-12)

[Empty comment from Monorail migration]

### lm...@gmail.com (2023-02-12)

Sorry for the typo in the title, there is nothing to do with the race condition.

### lm...@gmail.com (2023-02-13)

[Comment Deleted]

### lm...@gmail.com (2023-02-13)

Here is the poc

### ma...@google.com (2023-02-13)

Thank you for your report! 

Assigning to ChromeOS security bug triage.

### pa...@chromium.org (2023-02-15)

Thank you for the good report, PoC, and patch!

[Monorail components: Internals>GPU>VendorSpecific OS>Security]

### [Deleted User] (2023-02-15)

[Empty comment from Monorail migration]

### ro...@chromium.org (2023-02-15)

https://patchwork.freedesktop.org/series/114073/

### gi...@appspot.gserviceaccount.com (2023-02-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/895e82fb798ff9e97cf154f3c29aa2328831bb92

commit 895e82fb798ff9e97cf154f3c29aa2328831bb92
Author: Rob Clark <robdclark@chromium.org>
Date: Wed Feb 15 23:50:48 2023

FROMGIT: drm/msm: Fix potential invalid ptr free

The error path cleanup expects that chain and syncobj are either NULL or
valid pointers.  But post_deps was not allocated with __GFP_ZERO.

Fixes: ab723b7a992a ("drm/msm: Add syncobj support.")
Signed-off-by: Rob Clark <robdclark@chromium.org>
Reviewed-by: Dmitry Baryshkov <dmitry.baryshkov@linaro.org>
Reviewed-by: Dmitry Osipenko <dmitry.osipenko@collabora.com>
Patchwork: https://patchwork.freedesktop.org/patch/523051/
Link: https://lore.kernel.org/r/20230215235048.1166484-1-robdclark@gmail.com
(cherry picked from commit 8a86f213f4426f19511a16d886871805b35c3acf
 https://gitlab.freedesktop.org/drm/msm.git msm-fixes)

BUG=chromium:1415129
TEST=boot wormdingler

Change-Id: If2e8077fc35442fa45eceeff166ac27191c8513d
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4286763
Commit-Queue: Chia-I Wu <olv@google.com>
Reviewed-by: Chia-I Wu <olv@google.com>
Auto-Submit: Rob Clark <robdclark@chromium.org>
Tested-by: Rob Clark <robdclark@chromium.org>
Commit-Queue: Rob Clark <robdclark@chromium.org>
Reviewed-by: Sean Paul <sean@poorly.run>

[modify] https://crrev.com/895e82fb798ff9e97cf154f3c29aa2328831bb92/drivers/gpu/drm/msm/msm_gem_submit.c


### lm...@gmail.com (2023-04-04)

Hi, friendly ping. I see the patch has been merged, maybe this issue can be marked as fix and close?

### gr...@chromium.org (2023-04-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-04)

[Empty comment from Monorail migration]

### al...@google.com (2023-04-11)

Which kernel configs need to be enabled for this to be reachable?

### ro...@chromium.org (2023-04-11)

> Which kernel configs need to be enabled for this to be reachable?

CONFIG_DRM_MSM

### al...@google.com (2023-04-12)

Just a note: that is enabled on qualcomm devices.

### ha...@google.com (2023-04-24)

Is this demonstrably exploitable on a ChromeOS device?

### pa...@chromium.org (2023-04-25)

I think the path to exploitation would start with a compromised renderer, or a compromised VM, and from there to the GPU process. (And then, on particular hardware.)

I would therefore call this Medium severity, but I could be argued to Low.

### wf...@chromium.org (2023-04-27)

This is a memory corruption in GPU allowing a sandbox escape so should be High sev.

### am...@google.com (2023-04-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-04-28)

Congratulations! The VRP Panel has decided to award you $15,000 for this report + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-04-29)

[Empty comment from Monorail migration]

### lm...@gmail.com (2023-05-19)

Hi, similar to https://crbug.com/chromium/1406165#c44, https://crbug.com/chromium/1415129#c45, I have provided poc in https://crbug.com/chromium/1415129#c4.

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-05-25)

Hello, the Chrome VRP has reassessed this issue and has determined the current reward is sufficient for this report and misses the bar for consideration as a high quality reports as this issue lacks a stack trace demonstrating the UAF and there is no analysis or demonstration of the security impact to users or how this bug could be used as part of an exploit chain.

### [Deleted User] (2023-07-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-07-11)

This issue was migrated from crbug.com/chromium/1415129?no_tracker_redirect=1

[Multiple monorail components: Internals>GPU>VendorSpecific, OS>Security]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063040)*
