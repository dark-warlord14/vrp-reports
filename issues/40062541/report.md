# Security: Race Condition Double Free in adreno_set_param

| Field | Value |
|-------|-------|
| **Issue ID** | [40062541](https://issues.chromium.org/issues/40062541) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P4 |
| **Component** | Internals>GPU>VendorSpecific |
| **Platforms** | ChromeOS |
| **Reporter** | lm...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2023-01-07 |
| **Bounty** | $21,000.00 |

## Description

**VULNERABILITY DETAILS**

ioctl$MSM\_SET\_PARAM will call \*msm\_ioctl\_set\_param\* to set param. The real code logic is implemented in the \*adreno\_set\_param\* function. If the \*param\* is \*MSM\_PARAM\_COMM\*, \*ctx->comm\* will be freed[1]. There is no lock. So if \*adreno\_set\_param\* is called with \*MSM\_PARAM\_COMM\* twice in the same time, there will be a race condition double free(two threads call \*ioctl$MSM\_SET\_PARAM\* in the same time). The root case of this issue is that \*adreno\_set\_param\* is not locked properly.

```
static int msm_ioctl_set_param(struct drm_device \*dev, void \*data,  
		struct drm_file \*file)  
{  
	struct msm_drm_private \*priv = dev->dev_private;  
	struct drm_msm_param \*args = data;  
	struct msm_gpu \*gpu;  
  
	if ((args->pipe != MSM_PIPE_3D0) || (args->pad != 0))  
		return -EINVAL;  
  
	gpu = priv->gpu;  
  
	if (!gpu)  
		return -ENXIO;  
  
	return gpu->funcs->set_param(gpu, file->driver_priv,  
				     args->param, args->value, args->len);  
}  
  
static const struct adreno_gpu_funcs funcs = {  
	.base = {  
		.get_param = adreno_get_param,  
		.set_param = adreno_set_param,  
		.hw_init = a6xx_hw_init,  
		.pm_suspend = a6xx_pm_suspend,  
		.pm_resume = a6xx_pm_resume,  
		.recover = a6xx_recover,  
		.submit = a6xx_submit,  
		.active_ring = a6xx_active_ring,  
		.irq = a6xx_irq,  
		.destroy = a6xx_destroy,  
#if defined(CONFIG_DRM_MSM_GPU_STATE)  
		.show = a6xx_show,  
#endif  
		.gpu_busy = a6xx_gpu_busy,  
		.gpu_get_freq = a6xx_gmu_get_freq,  
		.gpu_set_freq = a6xx_gpu_set_freq,  
#if defined(CONFIG_DRM_MSM_GPU_STATE)  
		.gpu_state_get = a6xx_gpu_state_get,  
		.gpu_state_put = a6xx_gpu_state_put,  
#endif  
		.create_address_space = a6xx_create_address_space,  
		.create_private_address_space = a6xx_create_private_address_space,  
		.get_rptr = a6xx_get_rptr,  
	},  
	.get_timestamp = a6xx_get_timestamp,  
};  

```
```
int adreno_set_param(struct msm_gpu \*gpu, struct msm_file_private \*ctx,  
		     uint32_t param, uint64_t value, uint32_t len)  
{  
	switch (param) {  
	case MSM_PARAM_COMM:  
	case MSM_PARAM_CMDLINE:  
		/\* kstrdup_quotable_cmdline() limits to PAGE_SIZE, so  
		 \* that should be a reasonable upper bound  
		 \*/  
		if (len > PAGE_SIZE)  
			return -EINVAL;  
		break;  
	default:  
		if (len != 0)  
			return -EINVAL;  
	}  
  
	switch (param) {  
	case MSM_PARAM_COMM:  
	case MSM_PARAM_CMDLINE: {  
		char \*str, \*\*paramp;  
  
		str = kmalloc(len + 1, GFP_KERNEL);  
		if (!str)  
			return -ENOMEM;  
  
		if (copy_from_user(str, u64_to_user_ptr(value), len)) {  
			kfree(str);  
			return -EFAULT;  
		}  
  
		/\* Ensure string is null terminated: \*/  
		str[len] = '\0';  
  
		if (param == MSM_PARAM_COMM) {  
			paramp = &ctx->comm;  
		} else {  
			paramp = &ctx->cmdline;  
		}  
  
		kfree(\*paramp);		// [1]  
		\*paramp = str;  
  
		return 0;  
	}  
	case MSM_PARAM_SYSPROF:  
		if (!capable(CAP_SYS_ADMIN))  
			return -EPERM;  
		return msm_file_private_set_sysprof(ctx, gpu, value);  
	default:  
		DBG("%s: invalid param: %u", gpu->name, param);  
		return -EINVAL;  
	}  
}  

```

[1] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/upstream/drivers/gpu/drm/msm/adreno/adreno_gpu.c;drc=133a14afb9c2d651523102e1659a851b708b619a;l=360>

**VERSION**  

Operating System: ChromiumOS Kernel 5.15.81 stable + dev

**REPRODUCTION CASE**  

\*\*It needs to be reproduced in real devices, with specific gpu. Sorry I don't have a chromebook with that gpu. If there is any problem with the poc, please feel free to contact me.\*\*

1. Compile the poc.
2. Run poc in ChromiumOS system. (please make sure current user is in video group. it needs the privilege to access drm to trigger this bug).

FIX PATCH SUGGESTION  

I think the follwing patch should fix the problem.

```
diff --git a/drivers/gpu/drm/msm/adreno/adreno_gpu.c b/drivers/gpu/drm/msm/adreno/adreno_gpu.c  
index 9e32096d9fda..f89117dee0b9 100644  
--- a/drivers/gpu/drm/msm/adreno/adreno_gpu.c  
+++ b/drivers/gpu/drm/msm/adreno/adreno_gpu.c  
@@ -351,6 +351,7 @@ int adreno_set_param(struct msm_gpu \*gpu, struct msm_file_private \*ctx,  
                /\* Ensure string is null terminated: \*/  
                str[len] = '\0';  
  
+               mutex_lock(&gpu->lock);  
                if (param == MSM_PARAM_COMM) {  
                        paramp = &ctx->comm;  
                } else {  
@@ -359,6 +360,7 @@ int adreno_set_param(struct msm_gpu \*gpu, struct msm_file_private \*ctx,  
  
                kfree(\*paramp);  
                \*paramp = str;  
+               mutex_unlock(&gpu->lock);  
  
                return 0;  
        }  

```

## Attachments

- [poc.c](attachments/poc.c) (text/plain, 1.7 KB)

## Timeline

### lm...@gmail.com (2023-01-07)

msm_ioctl_set_param         |     msm_ioctl_set_param
    adreno_set_param          |         adreno_set_param
        kfree                           |             kfree	<---- double free

### [Deleted User] (2023-01-07)

[Empty comment from Monorail migration]

### lm...@gmail.com (2023-01-08)

Here is the poc. Sorry for the late.

### da...@chromium.org (2023-01-09)

=> chromeos triage

### th...@google.com (2023-01-10)

[Empty comment from Monorail migration]

[Monorail components: Internals>GPU>VendorSpecific]

### th...@google.com (2023-01-10)

[Empty comment from Monorail migration]

### co...@system.gserviceaccount.com (2023-01-10)

[Empty comment from Monorail migration]

[Monorail mergedinto: b/265027086]

### co...@system.gserviceaccount.com (2023-01-10)

Copybara migrated this issue to http://issuetracker.google.com/265027086. Please discontinue use of this issue.

### th...@google.com (2023-01-10)

[Empty comment from Monorail migration]

### ro...@chromium.org (2023-01-10)

https://patchwork.freedesktop.org/series/112641/

### [Deleted User] (2023-01-11)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-01-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/4c19f3e06d49bf490fd17fbe055587902bde2d62

commit 4c19f3e06d49bf490fd17fbe055587902bde2d62
Author: Rob Clark <robdclark@chromium.org>
Date: Tue Jan 10 21:28:59 2023

FROMGIT: drm/msm/gpu: Fix potential double-free

If userspace was calling the MSM_SET_PARAM ioctl on multiple threads to
set the COMM or CMDLINE param, it could trigger a race causing the
previous value to be kfree'd multiple times.  Fix this by serializing on
the gpu lock.

Signed-off-by: Rob Clark <robdclark@chromium.org>
Fixes: d4726d770068 ("drm/msm: Add a way to override processes comm/cmdline")
Patchwork: https://patchwork.freedesktop.org/patch/517778/
Link: https://lore.kernel.org/r/20230110212903.1925878-1-robdclark@gmail.com
(cherry picked from commit a66f1efcf748febea7758c4c3c8b5bc5294949ef
 https://gitlab.freedesktop.org/drm/msm.git msm-fixes)

BUG=chromium:1405568
TEST=Boot test wormdingler

Change-Id: I5a9f6f742067da1e631d88d65c1d4a3bedb65dc5
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4157712
Auto-Submit: Rob Clark <robdclark@chromium.org>
Tested-by: Rob Clark <robdclark@chromium.org>
Reviewed-by: Sean Paul <sean@poorly.run>
Commit-Queue: Chia-I Wu <olv@google.com>
Reviewed-by: Chia-I Wu <olv@google.com>
Commit-Queue: Rob Clark <robdclark@chromium.org>

[modify] https://crrev.com/4c19f3e06d49bf490fd17fbe055587902bde2d62/drivers/gpu/drm/msm/adreno/adreno_gpu.c
[modify] https://crrev.com/4c19f3e06d49bf490fd17fbe055587902bde2d62/drivers/gpu/drm/msm/msm_gpu.c
[modify] https://crrev.com/4c19f3e06d49bf490fd17fbe055587902bde2d62/drivers/gpu/drm/msm/msm_gpu.h


### ro...@chromium.org (2023-01-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-12)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), ceb (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-12)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ro...@google.com (2023-01-12)

for both questionnaires:

> 1. Why does your merge fit within the merge criteria for these milestones?

security fix

> 2. What changes specifically would you like to merge? Please link to Gerrit.

https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4157712

> 3. Have the changes been released and tested on canary?

yes

> 4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

no

> 5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

n/a

> 6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

no


### ma...@google.com (2023-01-12)

Merge approved, M109.

Category: Security fix

### gi...@appspot.gserviceaccount.com (2023-01-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/89aabe014a6d0c9b7dd6c5d32b8f18e7b9fe8e1c

commit 89aabe014a6d0c9b7dd6c5d32b8f18e7b9fe8e1c
Author: Rob Clark <robdclark@chromium.org>
Date: Tue Jan 10 21:28:59 2023

FROMGIT: drm/msm/gpu: Fix potential double-free

If userspace was calling the MSM_SET_PARAM ioctl on multiple threads to
set the COMM or CMDLINE param, it could trigger a race causing the
previous value to be kfree'd multiple times.  Fix this by serializing on
the gpu lock.

Signed-off-by: Rob Clark <robdclark@chromium.org>
Fixes: d4726d770068 ("drm/msm: Add a way to override processes comm/cmdline")
Patchwork: https://patchwork.freedesktop.org/patch/517778/
Link: https://lore.kernel.org/r/20230110212903.1925878-1-robdclark@gmail.com
(cherry picked from commit a66f1efcf748febea7758c4c3c8b5bc5294949ef
 https://gitlab.freedesktop.org/drm/msm.git msm-fixes)

BUG=chromium:1405568
TEST=Boot test wormdingler

Change-Id: I5a9f6f742067da1e631d88d65c1d4a3bedb65dc5
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4157712
Auto-Submit: Rob Clark <robdclark@chromium.org>
Tested-by: Rob Clark <robdclark@chromium.org>
Reviewed-by: Sean Paul <sean@poorly.run>
Commit-Queue: Chia-I Wu <olv@google.com>
Reviewed-by: Chia-I Wu <olv@google.com>
Commit-Queue: Rob Clark <robdclark@chromium.org>
(cherry picked from commit 4c19f3e06d49bf490fd17fbe055587902bde2d62)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4162993
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>

[modify] https://crrev.com/89aabe014a6d0c9b7dd6c5d32b8f18e7b9fe8e1c/drivers/gpu/drm/msm/adreno/adreno_gpu.c
[modify] https://crrev.com/89aabe014a6d0c9b7dd6c5d32b8f18e7b9fe8e1c/drivers/gpu/drm/msm/msm_gpu.c
[modify] https://crrev.com/89aabe014a6d0c9b7dd6c5d32b8f18e7b9fe8e1c/drivers/gpu/drm/msm/msm_gpu.h


### ce...@google.com (2023-01-13)

Merge approved for M-110.

Merge Category: Security Fix.

### gi...@appspot.gserviceaccount.com (2023-01-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/1c829161463d0b5c9906b6ce07e12b4a89008e51

commit 1c829161463d0b5c9906b6ce07e12b4a89008e51
Author: Rob Clark <robdclark@chromium.org>
Date: Tue Jan 10 21:28:59 2023

FROMGIT: drm/msm/gpu: Fix potential double-free

If userspace was calling the MSM_SET_PARAM ioctl on multiple threads to
set the COMM or CMDLINE param, it could trigger a race causing the
previous value to be kfree'd multiple times.  Fix this by serializing on
the gpu lock.

Signed-off-by: Rob Clark <robdclark@chromium.org>
Fixes: d4726d770068 ("drm/msm: Add a way to override processes comm/cmdline")
Patchwork: https://patchwork.freedesktop.org/patch/517778/
Link: https://lore.kernel.org/r/20230110212903.1925878-1-robdclark@gmail.com
(cherry picked from commit a66f1efcf748febea7758c4c3c8b5bc5294949ef
 https://gitlab.freedesktop.org/drm/msm.git msm-fixes)

BUG=chromium:1405568
TEST=Boot test wormdingler

Change-Id: I5a9f6f742067da1e631d88d65c1d4a3bedb65dc5
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4157712
Auto-Submit: Rob Clark <robdclark@chromium.org>
Tested-by: Rob Clark <robdclark@chromium.org>
Reviewed-by: Sean Paul <sean@poorly.run>
Commit-Queue: Chia-I Wu <olv@google.com>
Reviewed-by: Chia-I Wu <olv@google.com>
Commit-Queue: Rob Clark <robdclark@chromium.org>
(cherry picked from commit 4c19f3e06d49bf490fd17fbe055587902bde2d62)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4162995
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>

[modify] https://crrev.com/1c829161463d0b5c9906b6ce07e12b4a89008e51/drivers/gpu/drm/msm/adreno/adreno_gpu.c
[modify] https://crrev.com/1c829161463d0b5c9906b6ce07e12b4a89008e51/drivers/gpu/drm/msm/msm_gpu.c
[modify] https://crrev.com/1c829161463d0b5c9906b6ce07e12b4a89008e51/drivers/gpu/drm/msm/msm_gpu.h


### ro...@chromium.org (2023-01-13)

all the cherry-picks have landed so marking as fixed

### [Deleted User] (2023-01-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-14)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-01-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/cea46aa1be6aff1d8fc13f08b28bf1cd49ab9bd8

commit cea46aa1be6aff1d8fc13f08b28bf1cd49ab9bd8
Author: Rob Clark <robdclark@chromium.org>
Date: Tue Jan 10 21:28:59 2023

FROMGIT: drm/msm/gpu: Fix potential double-free

If userspace was calling the MSM_SET_PARAM ioctl on multiple threads to
set the COMM or CMDLINE param, it could trigger a race causing the
previous value to be kfree'd multiple times.  Fix this by serializing on
the gpu lock.

Signed-off-by: Rob Clark <robdclark@chromium.org>
Fixes: d4726d770068 ("drm/msm: Add a way to override processes comm/cmdline")
Patchwork: https://patchwork.freedesktop.org/patch/517778/
Link: https://lore.kernel.org/r/20230110212903.1925878-1-robdclark@gmail.com
(cherry picked from commit a66f1efcf748febea7758c4c3c8b5bc5294949ef
 https://gitlab.freedesktop.org/drm/msm.git msm-fixes)

BUG=chromium:1405568
TEST=Boot test wormdingler

Change-Id: I5a9f6f742067da1e631d88d65c1d4a3bedb65dc5
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4157712
Auto-Submit: Rob Clark <robdclark@chromium.org>
Tested-by: Rob Clark <robdclark@chromium.org>
Reviewed-by: Sean Paul <sean@poorly.run>
Commit-Queue: Chia-I Wu <olv@google.com>
Reviewed-by: Chia-I Wu <olv@google.com>
Commit-Queue: Rob Clark <robdclark@chromium.org>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4169801
Tested-by: Tzung-Bi Shih <tzungbi@chromium.org>
Commit-Queue: Tzung-Bi Shih <tzungbi@chromium.org>
Reviewed-by: Rob Clark <robdclark@chromium.org>

[modify] https://crrev.com/cea46aa1be6aff1d8fc13f08b28bf1cd49ab9bd8/drivers/gpu/drm/msm/adreno/adreno_gpu.c
[modify] https://crrev.com/cea46aa1be6aff1d8fc13f08b28bf1cd49ab9bd8/drivers/gpu/drm/msm/msm_gpu.c
[modify] https://crrev.com/cea46aa1be6aff1d8fc13f08b28bf1cd49ab9bd8/drivers/gpu/drm/msm/msm_gpu.h


### [Deleted User] (2023-01-16)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ro...@chromium.org (2023-01-19)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-02-03)

Congratulations on another one! The VRP Panel has decided to award you $20,000 for this report + $1,000 patch bonus. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-02-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### is...@google.com (2023-05-24)

This issue was migrated from crbug.com/chromium/1405568?no_tracker_redirect=1

[Monorail mergedinto: b/265027086]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062541)*
