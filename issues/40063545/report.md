# Security: OOB Access in intel_pxp_sm_ioctl_mark_session_in_play

| Field | Value |
|-------|-------|
| **Issue ID** | [40063545](https://issues.chromium.org/issues/40063545) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>GPU>VendorSpecific |
| **Platforms** | ChromeOS |
| **Reporter** | lm...@gmail.com |
| **Assignee** | ju...@chromium.org |
| **Created** | 2023-03-11 |
| **Bounty** | $16,000.00 |

## Description

**VULNERABILITY DETAILS**

IOCTL$I915\_PXP\_OPS will call i915\_pxp\_ops\_ioctl to handle pxp ioctls. if \*pxp\_ops->action\* is DOWNSTREAM\_DRM\_I915\_PXP\_ACTION\_SET\_SESSION\_STATUS, it will call \*pxp\_set\_session\_status\*. \*params\* is copied from userspace[1], which means \*params\* is under user control, including \*params.pxp\_tag\*. If \*params.req\_session\_state\* is \*DOWNSTREAM\_DRM\_I915\_PXP\_REQ\_SESSION\_IN\_PLAY\*, it will call \*intel\_pxp\_sm\_ioctl\_mark\_session\_in\_play\*[2] with \*params.pxp\_tag\*. There is no check about the \*session\_id\*(\*params.pxp\_tag\*) in \*intel\_pxp\_sm\_ioctl\_mark\_session\_in\_play\*, and will cause out of bounds read/write.

```
static int pxp_set_session_status(struct intel_pxp \*pxp,  
				  struct downstream_drm_i915_pxp_ops \*pxp_ops,  
				  struct drm_file \*drmfile)  
{  
	struct downstream_drm_i915_pxp_set_session_status_params params;  
	struct downstream_drm_i915_pxp_set_session_status_params __user \*uparams =  
		u64_to_user_ptr(pxp_ops->params);  
	int ret = 0;  
  
	if (copy_from_user(&params, uparams, sizeof(params)) != 0)		// [1]  
		return -EFAULT;  
  
	switch (params.req_session_state) {  
	case DOWNSTREAM_DRM_I915_PXP_REQ_SESSION_ID_INIT:  
		ret = intel_pxp_sm_ioctl_reserve_session(pxp, drmfile,  
							 params.session_mode,  
							 &params.pxp_tag);  
		break;  
	case DOWNSTREAM_DRM_I915_PXP_REQ_SESSION_IN_PLAY:  
		ret = intel_pxp_sm_ioctl_mark_session_in_play(pxp, drmfile,  
							      params.pxp_tag);					// [2]  
		break;  
	case DOWNSTREAM_DRM_I915_PXP_REQ_SESSION_TERMINATE:  
		ret = intel_pxp_sm_ioctl_terminate_session(pxp, drmfile,  
							   params.pxp_tag);  
		break;  
	default:  
		ret = -EINVAL;  
	}  
  
	if (ret >= 0) {  
		pxp_ops->status = ret;  
  
		if (copy_to_user(uparams, &params, sizeof(params)))  
			ret = -EFAULT;  
		else  
			ret = 0;  
	}  
  
	return ret;  
}  
  
int intel_pxp_sm_ioctl_mark_session_in_play(struct intel_pxp \*pxp,  
					    struct drm_file \*drmfile,  
					    u32 session_id)  
{  
	lockdep_assert_held(&pxp->session_mutex);  
  
	if (!pxp->hwdrm_sessions[session_id])						// [3]  
		return -EINVAL;  
  
	if (pxp->hwdrm_sessions[session_id]->drmfile != drmfile)  
		return -EPERM;  
  
	pxp->hwdrm_sessions[session_id]->is_valid = true;  
  
	return 0;  
}  

```

[1] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.15/drivers/gpu/drm/i915/pxp/intel_pxp.c;drc=bf2e50dad9f01012f624d90344cba3337861a5e7;l=387>  

[2] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.15/drivers/gpu/drm/i915/pxp/intel_pxp.c;drc=bf2e50dad9f01012f624d90344cba3337861a5e7;l=397>  

[3] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.15/drivers/gpu/drm/i915/pxp/intel_pxp_session.c;drc=bf2e50dad9f01012f624d90344cba3337861a5e7;l=299>

**VERSION**  

Operating System: ChromiumOS Kernel 5.15 stable + dev

**REPRODUCTION CASE**  

This issue is discovered by manual code review, I will try to construct a poc to reproduce it.

Bisect  

<https://source.chromium.org/chromiumos/_/chromium/chromiumos/third_party/kernel/+/4ee107d70597cc94b1c48ecf2b5629232955f32b>

FIX PATCH SUGGESTION  

I think the follwing patch should fix the problem.

```
diff --git a/drivers/gpu/drm/i915/pxp/intel_pxp_session.c b/drivers/gpu/drm/i915/pxp/intel_pxp_session.c  
index 63d33c225a5a..54c4a63f05ef 100644  
--- a/drivers/gpu/drm/i915/pxp/intel_pxp_session.c  
+++ b/drivers/gpu/drm/i915/pxp/intel_pxp_session.c  
@@ -296,6 +296,8 @@ int intel_pxp_sm_ioctl_mark_session_in_play(struct intel_pxp \*pxp,  
 {  
        lockdep_assert_held(&pxp->session_mutex);  
   
+       session_id = session_id & DOWNSTREAM_DRM_I915_PXP_TAG_SESSION_ID_MASK;  
+  
        if (!pxp->hwdrm_sessions[session_id])  
                return -EINVAL;  

```

## Attachments

- [poc.c](attachments/poc.c) (text/plain, 3.2 KB)
- [poc.c](attachments/poc.c) (text/plain, 3.2 KB)

## Timeline

### [Deleted User] (2023-03-11)

[Empty comment from Monorail migration]

### lm...@gmail.com (2023-03-11)

Here is the poc.

### ma...@chromium.org (2023-03-13)

[Empty comment from Monorail migration]

### en...@google.com (2023-03-14)

Thank you for the report.
Assigning to roxabee@ while we decide on an official course of action for upstream kernel bug reports.

### lm...@gmail.com (2023-03-15)

Hi, it seems downstream driver instead of upstream. I didn't see the intel_pxp_sm_ioctl_mark_session_in_play function in upstream kernel.

### [Deleted User] (2023-03-19)

[Empty comment from Monorail migration]

### lm...@gmail.com (2023-03-27)

Hi, friendly ping. Is there any updates?

### lm...@gmail.com (2023-05-14)

Hi, friendly ping. Is there any updates? 

### ro...@chromium.org (2023-05-14)

@robdclark@chromium.org can you please confirm if intel_pxp_sm_ioctl_mark_session_in_play function is somehow only present in ChromeOS and not upstream. 

Otherwise lm0963hack@gmail.com will need to report directly to Intel and we will wait for the Intel fix.



### lm...@gmail.com (2023-05-18)

Hi, friendly ping. Is there any updates?

### ro...@chromium.org (2023-05-18)

[Empty comment from Monorail migration]

### ju...@chromium.org (2023-05-18)

@roxabee@chromium.org Yes, this code is downstream only and only found in Chrome OS afaik. Chrome OS kernels 5.4+ have these downstream patches.

### ro...@google.com (2023-05-18)

lm0963hack@gmail.com sorry for the delay. You are right. This bug is in code that Intel contributes to ChromeOS kernel to support a closed source user space driver (and will not be accepted upstream). We will go ahead and fix it ourselves v. asking Intel to contribute the fix but we do need to run the fix past Intel so there may be a delay in the fix. 

### ro...@google.com (2023-05-18)

[Empty comment from Monorail migration]

[Monorail components: Internals>GPU>VendorSpecific]

### ro...@google.com (2023-05-18)

[Empty comment from Monorail migration]

### ro...@google.com (2023-05-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-18)

[Empty comment from Monorail migration]

### ju...@chromium.org (2023-05-18)

@lm0963hack@gmail.com

Working with Intel maintainers to review the suggested patch. Will keep progress updated.

Also were you able to construct the reproduction poc?

### lm...@gmail.com (2023-05-19)

Hi, I have submitted the poc, please check https://crbug.com/chromium/1423627#c2. I also upload it here.

### [Deleted User] (2023-05-22)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-25)

[Empty comment from Monorail migration]

### lm...@gmail.com (2023-05-25)

Hi, one detail I want to add is that this vulnerability can not only lead to oob read, but also cause oob write, so it is possible to achieve kernel code execution by relying on this vulnerability individual

int intel_pxp_sm_ioctl_mark_session_in_play(struct intel_pxp *pxp,
					    struct drm_file *drmfile,
					    u32 session_id)
{
	lockdep_assert_held(&pxp->session_mutex);

	if (!pxp->hwdrm_sessions[session_id])						// oob read
		return -EINVAL;

	if (pxp->hwdrm_sessions[session_id]->drmfile != drmfile)
		return -EPERM;

	pxp->hwdrm_sessions[session_id]->is_valid = true;            // oob write

	return 0;
}

### ju...@chromium.org (2023-05-25)

So turn's out our branches were out of sync and Intel's tree already has a bounds check here.
Additionally though, they've now made a change so the masking is more consistent.

I've posted CL's for affected kernels:
5.4:  https://crrev.com/c/4567078
5.10:  https://crrev.com/c/4567077
5.15:  https://crrev.com/c/4567079

### gi...@appspot.gserviceaccount.com (2023-05-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/d8391479e9f1c5809ef751f979804e8a26c5508e

commit d8391479e9f1c5809ef751f979804e8a26c5508e
Author: Alan Previn <alan.previn.teres.alexis@intel.com>
Date: Thu May 25 18:45:45 2023

CHROMIUM: drm/i915/pxp: Validate pxp_tag inputs in PXP_OPS ioctls

The functions intel_pxp_sm_ioctl_mark_session_in_play
and intel_pxp_sm_ioctl_terminate_session take in the
session_id via the user provided pxp_tag param.

However, they are not comprehensively extracting and
validating the session_id bit-field.

Add that validation step - extract the bitmask at the
caller and inside those functions, check it against
INTEL_PXP_MAX_HWDRM_SESSIONS.

Signed-off-by: Alan Previn <alan.previn.teres.alexis@intel.com>
Fixes: 6609cf02b5fe ("CHROMIUM: drm/i915/pxp: Implement ioctl actions to manage a user session")

BUG=chromium:1423627
TEST=cros_workon --board=volteer start chromeos-kernel-5_4
     sudo emerge-volteer chromeos-kernel-5_4
UPSTREAM-TASK=b:185364793

Change-Id: Ia803265922a41eaa31c861663dfa2af358bd5a73
Signed-off-by: Juston Li <justonli@google.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4567078
Reviewed-by: Jeffrey Kardatzke <jkardatzke@google.com>

[modify] https://crrev.com/d8391479e9f1c5809ef751f979804e8a26c5508e/drivers/gpu/drm/i915/pxp/intel_pxp.c
[modify] https://crrev.com/d8391479e9f1c5809ef751f979804e8a26c5508e/drivers/gpu/drm/i915/pxp/intel_pxp_session.c
[modify] https://crrev.com/d8391479e9f1c5809ef751f979804e8a26c5508e/drivers/gpu/drm/i915/pxp/intel_pxp_session.h


### gi...@appspot.gserviceaccount.com (2023-05-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/371cfb79a47ad9d99ec5aaa424893a190d7ea909

commit 371cfb79a47ad9d99ec5aaa424893a190d7ea909
Author: Alan Previn <alan.previn.teres.alexis@intel.com>
Date: Thu May 25 18:45:45 2023

CHROMIUM: drm/i915/pxp: Validate pxp_tag inputs in PXP_OPS ioctls

The functions intel_pxp_sm_ioctl_mark_session_in_play
and intel_pxp_sm_ioctl_terminate_session take in the
session_id via the user provided pxp_tag param.

However, they are not comprehensively extracting and
validating the session_id bit-field.

Add that validation step - extract the bitmask at the
caller and inside those functions, check it against
INTEL_PXP_MAX_HWDRM_SESSIONS.

Signed-off-by: Alan Previn <alan.previn.teres.alexis@intel.com>
Fixes: 0087fc6db81c ("CHROMIUM: drm/i915/pxp: Implement ioctl actions to manage a user session")

BUG=chromium:1423627
TEST=cros_workon --board=brya start chromeos-kernel-5_10
     sudo emerge-brya chromeos-kernel-5_10
UPSTREAM-TASK=b:185364793

Change-Id: Ia803265922a41eaa31c861663dfa2af358bd5a73
Signed-off-by: Juston Li <justonli@google.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4567077
Reviewed-by: Jeffrey Kardatzke <jkardatzke@google.com>

[modify] https://crrev.com/371cfb79a47ad9d99ec5aaa424893a190d7ea909/drivers/gpu/drm/i915/pxp/intel_pxp.c
[modify] https://crrev.com/371cfb79a47ad9d99ec5aaa424893a190d7ea909/drivers/gpu/drm/i915/pxp/intel_pxp_session.c
[modify] https://crrev.com/371cfb79a47ad9d99ec5aaa424893a190d7ea909/drivers/gpu/drm/i915/pxp/intel_pxp_session.h


### gi...@appspot.gserviceaccount.com (2023-05-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/caaec6ca2f093ff67a24d65b496006ed1fefbb25

commit caaec6ca2f093ff67a24d65b496006ed1fefbb25
Author: Alan Previn <alan.previn.teres.alexis@intel.com>
Date: Thu May 25 18:45:45 2023

CHROMIUM: drm/i915/pxp: Validate pxp_tag inputs in PXP_OPS ioctls

The functions intel_pxp_sm_ioctl_mark_session_in_play
and intel_pxp_sm_ioctl_terminate_session take in the
session_id via the user provided pxp_tag param.

However, they are not comprehensively extracting and
validating the session_id bit-field.

Add that validation step - extract the bitmask at the
caller and inside those functions, check it against
INTEL_PXP_MAX_HWDRM_SESSIONS.

Signed-off-by: Alan Previn <alan.previn.teres.alexis@intel.com>
Fixes: 4ee107d70597 ("CHROMIUM: drm/i915/pxp: Implement ioctl actions to manage a user session")

BUG=chromium:1423627
TEST=cros_workon --board=nissa start chromeos-kernel-5_15
     sudo emerge-nissa chromeos-kernel-5_15
UPSTREAM-TASK=b:185364793

Change-Id: Ia803265922a41eaa31c861663dfa2af358bd5a73
Signed-off-by: Juston Li <justonli@google.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4567079
Reviewed-by: Jeffrey Kardatzke <jkardatzke@google.com>

[modify] https://crrev.com/caaec6ca2f093ff67a24d65b496006ed1fefbb25/drivers/gpu/drm/i915/pxp/intel_pxp.c
[modify] https://crrev.com/caaec6ca2f093ff67a24d65b496006ed1fefbb25/drivers/gpu/drm/i915/pxp/intel_pxp_session.c
[modify] https://crrev.com/caaec6ca2f093ff67a24d65b496006ed1fefbb25/drivers/gpu/drm/i915/pxp/intel_pxp_session.h


### [Deleted User] (2023-06-09)

justonli: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ju...@google.com (2023-06-12)

Fixes have landed in R116-15479.0.0

### [Deleted User] (2023-06-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-12)

[Empty comment from Monorail migration]

### jo...@chromium.org (2023-06-13)

[Empty comment from Monorail migration]

### jo...@chromium.org (2023-06-13)

[Empty comment from Monorail migration]

### am...@google.com (2023-06-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-24)

Congratulations! The VRP Panel has decided to award you $10,000 for this report of a GPU OOB RW. Thank you for your efforts and reporting this issue to us. 

### lm...@gmail.com (2023-06-26)

Hi, thank you very much for the bounty, but I have some doubts, this bounty amount is lower than the baseline report, can you please point out the deficiencies in this report?

### am...@google.com (2023-06-26)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-06-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/2b20658c45e6e48b462b1eff56a365f8867e4baf

commit 2b20658c45e6e48b462b1eff56a365f8867e4baf
Author: Srihari Uttanur <srihari.uttanur@intel.corp-partner.google.com>
Date: Tue Jun 20 06:52:13 2023

CHROMIUM: drm/i915/pxp: Validate pxp_tag inputs in PXP_OPS ioctls

The functions intel_pxp_sm_ioctl_query_pxp_tag take in the
session_id via the user provided pxp_tag param.

However, they are not comprehensively extracting and
validating the session_id bit-field.

Add that validation step - extract the bitmask at the
caller and inside those functions, check it against
INTEL_PXP_MAX_HWDRM_SESSIONS.

Signed-off-by: Alan Previn <alan.previn.teres.alexis@intel.com>
Fixes: 6609cf02b5fe ("CHROMIUM: drm/i915/pxp: Implement ioctl actions to manage a user session")

BUG=chromium:1423627, b:284492421, b:287203832
TEST=cros_workon --board=volteer start chromeos-kernel-5_4
     sudo emerge-volteer chromeos-kernel-5_4
UPSTREAM-TASK=b:185364793

Change-Id: I3bc10a8c716517a2cd1647b511e86a4b4a5ccf9d
Signed-off-by: Srihari Uttanur <srihari.uttanur@intel.corp-partner.google.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4627799
Commit-Queue: Drew Davenport <ddavenport@chromium.org>
Reviewed-by: Juston Li <justonli@google.com>
Reviewed-by: Drew Davenport <ddavenport@chromium.org>
Tested-by: Santosh Kumar Avati <santosh.kumar.avati@intel.com>

[modify] https://crrev.com/2b20658c45e6e48b462b1eff56a365f8867e4baf/drivers/gpu/drm/i915/pxp/intel_pxp_session.c


### gi...@appspot.gserviceaccount.com (2023-06-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/e38226e8d67d8007e2ba383b0a1ea7a8b84d9982

commit e38226e8d67d8007e2ba383b0a1ea7a8b84d9982
Author: Srihari Uttanur <srihari.uttanur@intel.corp-partner.google.com>
Date: Tue Jun 20 06:52:13 2023

CHROMIUM: drm/i915/pxp: Validate pxp_tag inputs in PXP_OPS ioctls

The functions intel_pxp_sm_ioctl_query_pxp_tag take in the
session_id via the user provided pxp_tag param.

However, they are not comprehensively extracting and
validating the session_id bit-field.

Add that validation step - extract the bitmask at the
caller and inside those functions, check it against
INTEL_PXP_MAX_HWDRM_SESSIONS.

Signed-off-by: Alan Previn <alan.previn.teres.alexis@intel.com>
Fixes: 6609cf02b5fe ("CHROMIUM: drm/i915/pxp: Implement ioctl actions to manage a user session")

BUG=chromium:1423627, b:284492421, b:287203832
TEST=cros_workon --board=brya start chromeos-kernel-5_10
     sudo emerge-brya chromeos-kernel-5_10
UPSTREAM-TASK=b:185364793

Change-Id: I3bc10a8c716517a2cd1647b511e86a4b4a5ccf9d
Signed-off-by: Srihari Uttanur <srihari.uttanur@intel.corp-partner.google.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4627800
Reviewed-by: Juston Li <justonli@google.com>
Tested-by: Santosh Kumar Avati <santosh.kumar.avati@intel.com>
Commit-Queue: Drew Davenport <ddavenport@chromium.org>
Reviewed-by: Drew Davenport <ddavenport@chromium.org>

[modify] https://crrev.com/e38226e8d67d8007e2ba383b0a1ea7a8b84d9982/drivers/gpu/drm/i915/pxp/intel_pxp_session.c


### gi...@appspot.gserviceaccount.com (2023-06-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/c4c8a083bf40681d588e79ec498c25b9d6e6c169

commit c4c8a083bf40681d588e79ec498c25b9d6e6c169
Author: Srihari Uttanur <srihari.uttanur@intel.corp-partner.google.com>
Date: Tue Jun 20 06:52:13 2023

CHROMIUM: drm/i915/pxp: Validate pxp_tag inputs in PXP_OPS ioctls

The functions intel_pxp_sm_ioctl_query_pxp_tag take in the
session_id via the user provided pxp_tag param.

However, they are not comprehensively extracting and
validating the session_id bit-field.

Add that validation step - extract the bitmask at the
caller and inside those functions, check it against
INTEL_PXP_MAX_HWDRM_SESSIONS.

Signed-off-by: Alan Previn <alan.previn.teres.alexis@intel.com>
Fixes: 6609cf02b5fe ("CHROMIUM: drm/i915/pxp: Implement ioctl actions to manage a user session")

BUG=chromium:1423627, b:284492421, b:287203832
TEST=cros_workon --board=nissa start chromeos-kernel-5_15
     sudo emerge-nissa chromeos-kernel-5_15
UPSTREAM-TASK=b:185364793

Change-Id: I3bc10a8c716517a2cd1647b511e86a4b4a5ccf9d
Signed-off-by: Srihari Uttanur <srihari.uttanur@intel.corp-partner.google.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4622321
Commit-Queue: Drew Davenport <ddavenport@chromium.org>
Tested-by: Altaf Basha <altaf.basha@intel.com>
Reviewed-by: Drew Davenport <ddavenport@chromium.org>
Reviewed-by: Juston Li <justonli@google.com>

[modify] https://crrev.com/c4c8a083bf40681d588e79ec498c25b9d6e6c169/drivers/gpu/drm/i915/pxp/intel_pxp_session.c


### am...@chromium.org (2023-08-08)

Hi, thanks for reaching out to request a response to your question. Re: c#36. This issue is in the Intel i915 GFX driver and and was assessed to result in OOB memory access in the GPU process. 
The reward amount decided upon for this issue is the reward amount for baseline reports for security issues resulting in GPU process memory corruption. 


### am...@chromium.org (2023-08-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-16)

We have reassessed this issue based on that it OOB memory access is indeed in the kernel rather than the GPU process. Based on this we have decided to award you an additional $5,000 + $1,000 bisect bonus. Thanks for your patience for this to be reassessed and allowing us time to make it right! 

### [Deleted User] (2023-09-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-09-18)

This issue was migrated from crbug.com/chromium/1423627?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063545)*
