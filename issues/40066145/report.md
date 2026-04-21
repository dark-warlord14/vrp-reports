# Race Condition UAF in amdgpu_cs_wait_fences_ioctl

| Field | Value |
|-------|-------|
| **Issue ID** | [40066145](https://issues.chromium.org/issues/40066145) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | sh...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-06-21 |
| **Bounty** | $1,000.00 |

## Description

**Steps to reproduce the problem:**  

VULNERABILITY DETAILS

**Problem Description:**  

ioctl$DRM\_IOCTL\_AMDGPU\_WAIT\_FENCES will call \*\*amdgpu\_cs\_wait\_all\_fences\*\* . in amdgpu\_cs\_wait\_all\_fences , it will call \*\*amdgpu\_cs\_get\_fence\*\* to get a \*\*struct dma\_fence\*\* object , as a handle which can be deleted by dma\_fence\_put [3] ,and afterwards decrease refcount of it. But after decrease the refcount, it will access the fence->error [4]. So there is race condition Use-After-Free.

```
static int amdgpu_cs_wait_all_fences(struct amdgpu_device \*adev,  
				     struct drm_file \*filp,  
				     union drm_amdgpu_wait_fences \*wait,  
				     struct drm_amdgpu_fence \*fences)  
{  
	uint32_t fence_count = wait->in.fence_count;  
	unsigned int i;  
	long r = 1;  
  
	for (i = 0; i < fence_count; i++) {  
		struct dma_fence \*fence;  
		unsigned long timeout = amdgpu_gem_timeout(wait->in.timeout_ns);  
  
		fence = amdgpu_cs_get_fence(adev, filp, &fences[i]);		// [1]  
		if (IS_ERR(fence))  
			return PTR_ERR(fence);  
		else if (!fence)  
			continue;  
  
		r = dma_fence_wait_timeout(fence, true, timeout);  
		dma_fence_put(fence);										// [2]  
		if (r < 0)  
			return r;  
  
		if (r == 0)  
			break;  
  
		if (fence->error)											// [4]  
			return fence->error;  
	}  
    ...  
}  
  
static void dma_fence_array_release(struct dma_fence \*fence)  
{  
	struct dma_fence_array \*array = to_dma_fence_array(fence);  
	unsigned i;  
  
	for (i = 0; i < array->num_fences; ++i)  
		dma_fence_put(array->fences[i]);							// [3]  
  
	kfree(array->fences);  
	dma_fence_free(fence);											  
}  

```
```
  thread1									thread2  

amdgpu_cs_wait_all_fences			        |  

```

​ amdgpu\_cs\_get\_fence |

​ | close

​ | dma\_fence\_array\_release

​ dma\_fence\_put |

​ fence->error <--- uaf |

[1] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/upstream/drivers/gpu/drm/amd/amdgpu/amdgpu_cs.c;l=1607>

\*\*VERSION\*\*  

Operating System: ChromiumOS Kernel upstream stable + dev

\*\*REPRODUCTION CASE\*\*  

\*\*It needs to be reproduced in real devices, with Intel gpu. Sorry I don't have a chromebook with Intel gpu. If there is any problem with the poc, please feel free to contact me.\*\*

FIX PATCH SUGGESTION  

I think the follwing patch should fix the problem.

```
static int amdgpu_cs_wait_all_fences(struct amdgpu_device \*adev,  
				     struct drm_file \*filp,  
				     union drm_amdgpu_wait_fences \*wait,  
				     struct drm_amdgpu_fence \*fences)  
{  
	...  
  
		r = dma_fence_wait_timeout(fence, true, timeout);  
-		dma_fence_put(fence);		  
		if (r < 0)  
			return r;  
  
		if (r == 0)  
			break;  
  
		if (fence->error){  
+			dma_fence_put(fence);  
			return fence->error;  
		}  
			  
	}  
  
	memset(wait, 0, sizeof(\*wait));  
	wait->out.status = (r > 0);  
  
	return 0;  
}  

```

**Additional Comments:**

\*\*Chrome version: \*\* 113.0.0.0 \*\*Channel: \*\* Stable

**OS:** Chrome OS

## Timeline

### [Deleted User] (2023-06-21)

[Empty comment from Monorail migration]

### xi...@chromium.org (2023-06-21)

=> chromeos triage

### ch...@google.com (2023-06-22)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/288369230). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

[Monorail blocking: b/288369230]

### [Deleted User] (2023-06-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-23)

[Empty comment from Monorail migration]

### ch...@google.com (2023-08-01)

Project: chromiumos/third_party/kernel
Branch: chromeos-5.10

commit 1d6a7002652f71ce61777da46117a420bc76eaff
Author: shanzhulig <shanzhulig@gmail.com>
Date:   Tue Jun 27 18:10:47 2023

    UPSTREAM: drm/amdgpu: Fix potential fence use-after-free v2
   
    fence Decrements the reference count before exiting.
    Avoid Race Vulnerabilities for fence use-after-free.
   
    v2 (chk): actually fix the use after free and not just move it.
   
    Signed-off-by: shanzhulig <shanzhulig@gmail.com>
    Signed-off-by: Christian König <christian.koenig@amd.com>
    Reviewed-by: Alex Deucher <alexander.deucher@amd.com>
    Signed-off-by: Alex Deucher <alexander.deucher@amd.com>
    (cherry picked from commit 2e54154b9f27262efd0cb4f903cc7d5ad1fe9628)
   
    BUG=b:288369230
    TEST=None
   
    Signed-off-by: Rob Clark <robdclark@chromium.org>
    Change-Id: If8ae657b674ff81d0939554f507236dd188c277a
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4717858
    Reviewed-by: Stéphane Marchesin <marcheu@chromium.org>
    Reviewed-by: Sean Paul <sean@poorly.run>
    Reviewed-by: Chia-I Wu <olv@google.com>

M       drivers/gpu/drm/amd/amdgpu/amdgpu_cs.c

https://chromium-review.googlesource.com/4717858
19:50
19:50
CLs: Merged:​crrev/c/4717859, crrev/c/4718805, crrev/c/4718806      crrev/c/4717858, crrev/c/4717859, crrev/c/4718805, crrev/c/4718806
CLs: Pending:​crrev/c/4717858      <none>

### [Deleted User] (2023-08-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-01)

[Empty comment from Monorail migration]

### jo...@chromium.org (2023-08-22)

[Empty comment from Monorail migration]

### ch...@google.com (2023-09-19)

Exploitability - Explain why/why not the bug is reachable and/or exploitable For example, if a bug mentions a race, details are needed about how easy that race would be to achieve / can the attack retry infinite times to win the race, etc..

This is a use-after-free that allows reading a value the size of an int. The attacker must win a race to read this value, but there’s nothing preventing retrying that race condition.

Privileges and Capabilities - Identify which process is exploited and where code execution potentially can be achieved if the attacker can break out of that process, and explain why

This was in a GPU driver.

Origin of fix - Is the issue already known upstream, fixed by work from a previously known or reported issue, provided by the reporter, or any other information that would be relevant toward reward eligibility

The reporter, shanzhulig@gmail.com, created an upstream patch. This was then merged using the UPSTREAM tag to impacted branches.

Mitigations - Detail any regarding mitigation considerations (we're run across a few comments, such as "we considered this issue to be highly mitigated" without explanation)

Not applicable.

Severity assessment - why not higher, why not lower

This is S2, or Medium severity, because it’s a read but only requires winning a retriable race to exploit.

### am...@chromium.org (2023-09-26)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-12)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-12)

Congratulations shanzhulig@gmail.com! 
The VRP Panel has decided to award you $1000 for this report. 
A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in discovering and reporting this issue to us -- great work! 
Please be mindful that previous reward decisions made by the Chrome VRP should not be considered precedent for potential future ChromeOS VRP reward amounts or decisions.

### ch...@google.com (2023-10-12)

[Empty comment from Monorail migration]

### am...@google.com (2023-10-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-11-07)

This issue was migrated from crbug.com/chromium/1456561?no_tracker_redirect=1

[Monorail blocking: b/288369230]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40066145)*
