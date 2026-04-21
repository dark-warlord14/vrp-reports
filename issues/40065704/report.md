# Security: Out of bound in intel_pxp_sm_ioctl_query_pxp_tag

| Field | Value |
|-------|-------|
| **Issue ID** | [40065704](https://issues.chromium.org/issues/40065704) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | yq...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-06-13 |
| **Bounty** | $1,250.00 |

## Description

**VULNERABILITY DETAILS**

There are already similar points patched, but some places are not patched.  

<https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4567077>

i915\_pxp\_ops\_ioctl will call pxp\_query\_tag,and pxp\_query\_tag will call intel\_pxp\_sm\_ioctl\_query\_pxp\_tag,it does not valid the \*params.pxp\_tag\* at[0],finally cause oob in [1].

```
int i915_pxp_ops_ioctl(struct drm_device \*dev, void \*data, struct drm_file \*drmfile)  
{  
	int ret = 0;  
	struct downstream_drm_i915_pxp_ops \*pxp_ops = data;  
	struct drm_i915_private \*i915 = to_i915(dev);  
	struct intel_pxp \*pxp = &i915->gt0.pxp;  
	intel_wakeref_t wakeref;  
  
	if (!intel_pxp_is_enabled(pxp))  
		return -ENODEV;  
  
	wakeref = intel_runtime_pm_get_if_in_use(&i915->runtime_pm);  
	if (!wakeref) {  
		drm_dbg(&i915->drm, "pxp ioctl blocked due to state in suspend\n");  
		pxp_ops->status = DOWNSTREAM_DRM_I915_PXP_OP_STATUS_SESSION_NOT_AVAILABLE;  
		return 0;  
	}  
	if (pxp->hw_state_invalidated) {  
		drm_dbg(&i915->drm, "pxp ioctl retry required due to state attacked\n");  
		pxp_ops->status = DOWNSTREAM_DRM_I915_PXP_OP_STATUS_RETRY_REQUIRED;  
		goto out_unlock;  
	}  
  
	if (!intel_pxp_is_active(pxp)) {  
		ret = intel_pxp_start(pxp);  
		if (ret)  
			goto out_pm;  
	}  
  
	mutex_lock(&pxp->session_mutex);  
  
	switch (pxp_ops->action) {  
	case DOWNSTREAM_DRM_I915_PXP_ACTION_SET_SESSION_STATUS:  
		ret = pxp_set_session_status(pxp, pxp_ops, drmfile);  
		break;  
	case DOWNSTREAM_DRM_I915_PXP_ACTION_TEE_IO_MESSAGE:  
		ret = pxp_send_tee_msg(pxp, pxp_ops, drmfile);  
		break;  
	case DOWNSTREAM_DRM_I915_PXP_ACTION_QUERY_PXP_TAG:  
		ret = pxp_query_tag(pxp, pxp_ops);  
		break;  
	default:  
		ret = -EINVAL;  
		break;  
	}  
  
out_unlock:  
	mutex_unlock(&pxp->session_mutex);  
out_pm:  
	intel_runtime_pm_put(&i915->runtime_pm, wakeref);  
  
	return ret;  
}  
  
  
static int pxp_query_tag(struct intel_pxp \*pxp, struct downstream_drm_i915_pxp_ops \*pxp_ops)  
{  
	struct downstream_drm_i915_pxp_query_tag params;  
	struct downstream_drm_i915_pxp_query_tag __user \*uparams =  
		u64_to_user_ptr(pxp_ops->params);  
	int ret = 0;  
  
	if (copy_from_user(&params, uparams, sizeof(params)) != 0)  
		return -EFAULT;  
  
	ret = intel_pxp_sm_ioctl_query_pxp_tag(pxp, &params.session_is_alive,  
					       &params.pxp_tag);  
	if (ret >= 0) {  
		pxp_ops->status = ret;  
  
		if (copy_to_user(uparams, &params, sizeof(params)))  
			ret = -EFAULT;  
		else  
			ret = 0;  
	}  
  
	return ret;  
}  
  
  
  
  
int intel_pxp_sm_ioctl_query_pxp_tag(struct intel_pxp \*pxp,  
				     u32 \*session_is_alive, u32 \*pxp_tag)  
{  
	int session_id = 0;  
  
	if (!session_is_alive || !pxp_tag)  
		return -EINVAL;  
  
	session_id = \*pxp_tag & DOWNSTREAM_DRM_I915_PXP_TAG_SESSION_ID_MASK;  //[0]  
  
	if (!pxp->hwdrm_sessions[session_id]) {   //[1]  
		\*pxp_tag = 0;  
		\*session_is_alive = 0;  
		return 0;  
	}  
  
	\*pxp_tag = pxp->hwdrm_sessions[session_id]->tag;  
  
	if (session_is_alive)  
		\*session_is_alive = pxp->hwdrm_sessions[session_id]->is_valid;  
  
	return 0;  
}  

```

**VERSION**  

Operating System: ChromiumOS Kernel 5.10,5.15 etc

**REPRODUCTION CASE**  

This issue is discovered by manual code review, I will try to construct a poc to reproduce it.

Bisect  

<https://source.chromium.org/chromiumos/_/chromium/chromiumos/third_party/kernel/+/da89ac8bda63476039e0cdf5f6860e1d301e740e>

PATCH SUGGESTION

```
--- a/intel_pxp_session.c	2023-06-13 10:23:56.039052115 +0800  
+++ b/intel_pxp_session.c	2023-06-13 10:24:55.740103371 +0800  
@@ -269,6 +269,9 @@ int intel_pxp_sm_ioctl_query_pxp_tag(str  
 		return -EINVAL;  
   
 	session_id = \*pxp_tag & DOWNSTREAM_DRM_I915_PXP_TAG_SESSION_ID_MASK;  
+	  
+	if (session_id >= INTEL_PXP_MAX_HWDRM_SESSIONS)  
+		return -EINVAL;  
   
 	if (!pxp->hwdrm_sessions[session_id]) {  
 		\*pxp_tag = 0;  
  
  

```

## Attachments

- [poc.c](attachments/poc.c) (text/plain, 3.0 KB)

## Timeline

### [Deleted User] (2023-06-13)

[Empty comment from Monorail migration]

### yq...@gmail.com (2023-06-13)

[Empty comment from Monorail migration]

### dc...@chromium.org (2023-06-13)

[Empty comment from Monorail migration]

### ch...@google.com (2023-06-14)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/287203832). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

[Monorail blocking: b/287203832]

### [Deleted User] (2023-06-14)

[Empty comment from Monorail migration]

### ch...@google.com (2023-07-17)

Project: chromiumos/third_party/kernel
Branch: chromeos-5.15

commit c4c8a083bf40681d588e79ec498c25b9d6e6c169
Author: Srihari Uttanur <srihari.uttanur@intel.corp-partner.google.com>
Date:   Mon Jun 19 23:52:13 2023

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

M       drivers/gpu/drm/i915/pxp/intel_pxp_session.c

https://chromium-review.googlesource.com/4622321
09:59
09:59
CLs: Merged:​crrev/c/4627799, crrev/c/4627800      crrev/c/4622321, crrev/c/4627799, crrev/c/4627800
CLs: Pending:​crrev/c/4622321      <none>

### [Deleted User] (2023-07-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-17)

[Empty comment from Monorail migration]

### ch...@google.com (2023-08-01)

[Empty comment from Monorail migration]

### ch...@google.com (2023-09-19)

"Exploitability - Explain why/why not the bug is reachable and/or exploitable For example, if a bug mentions a race, details are needed about how easy that race would be to achieve / can the attack retry infinite times to win the race, etc.."

The bug is reachable in the kernel code. Seems to be no race condition involved here. The malicious user needs root shell to issue ioctl

Privileges and Capabilities - Identify which process is exploited and where code execution potentially can be achieved if the attacker can break out of that process, and explain why

The issue is in the GPU driver code and the attacker needs root shell to issue IOCTL. No evidence of breakout here as the bug is in the query tag function which just performs a read.

Origin of fix - Is the issue already known upstream, fixed by work from a previously known or reported issue, provided by the reporter, or any other information that would be relevant toward reward eligibility

The fix was discovered in parallel wuth upstream and was being worked on in the previous bug: crbug.com/1423627. The fix did land a few days after the reporter updated the bug. There could be potential race here as in who reported first, etc.

Mitigations - Detail any regarding mitigation considerations (we're run across a few comments, such as "we considered this issue to be highly mitigated" without explanation)

User does need root shell to execute, but that would be it.

Severity assessment - why not higher, why not lower

Medium Severity -- OOB read in kernel process at pxp->hwdrm_sessions[session_id] This can be used in "potential memory corruption exploit"

Why not High Severity? Only evidence of read nothing to write here. Does not allow any protection bypass, etc by itself

Why not Low Severity? There are not many mitigation present here.

### am...@chromium.org (2023-09-26)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-05)

Congratulations yqsun1997@gmail.com! 
The VRP Panel has decided to award you $1250 for this report. 
A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in discovering and reporting this issue to us -- great work! 
Please be mindful that previous reward decisions made by the Chrome VRP should not be considered precedent for potential future ChromeOS VRP reward amounts or decisions.

### ch...@google.com (2023-10-05)

Dear yqsun1997@gmail.com,
Do you have a ChromeOS VRP preferred name for credit (mentioned in the release notes)?

### yq...@gmail.com (2023-10-05)

[Comment Deleted]

### ch...@google.com (2023-10-05)

Dear qsun1997@gmail.com,

Can you please ask in the main bug https://issuetracker.google.com/issues/287203832

### am...@chromium.org (2023-10-11)

This issue is lacking a reward-$amount label, updating accordingly. 
chmiel@ in the future, please ensure all ChromeOS bugs updated with reward-unpaid also include a reward-$amount label. Without it, the automation to send reward information to finance will result in an error. Thank you! 

### am...@google.com (2023-10-11)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-12)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-12)

[Empty comment from Monorail migration]

### yq...@gmail.com (2023-10-22)

[Comment Deleted]

### [Deleted User] (2023-10-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### st...@google.com (2023-11-07)

Updating this to reflect the correct reward amount. Thanks for your report!

### am...@google.com (2023-11-11)

[Empty comment from Monorail migration]

### is...@google.com (2023-11-11)

This issue was migrated from crbug.com/chromium/1454328?no_tracker_redirect=1

[Monorail blocking: b/287203832]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065704)*
