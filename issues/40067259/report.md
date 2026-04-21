# Race Condition UAF in DRM_IOCTL_MODE_ATOMIC

| Field | Value |
|-------|-------|
| **Issue ID** | [40067259](https://issues.chromium.org/issues/40067259) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | sh...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-07-12 |
| **Bounty** | $750.00 |

## Description

**Steps to reproduce the problem:**  

\*\*REPRODUCTION CASE\*\*  

I can't access it properly because the card0 is so high occupied sorry for not reproducing it.

**Problem Description:**  

I caught the same kasan message multiple times in fuzz but disappointingly did not keep the poc so I decided to analyze it statically . In the ioctl$DRM\_IOCTL\_MODE\_ATOMIC function there is a controlled flags it calls the drm\_atomic\_nonblocking\_commit function [2] to create an asynchronous queue. [2] eventually calls the drm\_atomic\_helper\_commit function where [4] is creating the asynchronous execution function commit\_work, the kasan message points to this and it tells me that there is use-after-free in the drm\_atomic\_helper\_wait\_for\_vblanks function. Eventually I found the problem, at created struct drm\_atomic\_state in [1] and assigned dev to state->dev [3] then when execution finished ioctl$DRM\_IOCTL\_MODE\_ATOMIC exited, state->ref == 1 would not be freed. However, if Race Condition to release dev early, [6] in the asynchronous execution function commit\_work will be problematic, dev will become a dangling pointer, and use of dev will result in use-after-free. dev is not used until the drm\_atomic\_helper\_wait\_for\_vblanks function, so the kasan message will point here.

```
int drm_mode_atomic_ioctl(struct drm_device \*dev,  
			  void \*data, struct drm_file \*file_priv)  
{  
	...  
  
	state = drm_atomic_state_alloc(dev);		// [1]  
	if (!state)   
		return -ENOMEM;  
    ...  
  
	if (arg->flags & DRM_MODE_ATOMIC_TEST_ONLY) {  
		ret = drm_atomic_check_only(state);  
	} else if (arg->flags & DRM_MODE_ATOMIC_NONBLOCK) {  
		ret = drm_atomic_nonblocking_commit(state);		// 	[2]  
	} else {  
		ret = drm_atomic_commit(state);		  
	}  
  
	...  
  
	drm_atomic_state_put(state);					// state->ref == 1   
        ...  
}  
int  
drm_atomic_state_init(struct drm_device \*dev, struct drm_atomic_state \*state)  
{  
       ...  
	state->planes = kcalloc(dev->mode_config.num_total_plane,  
				sizeof(\*state->planes), GFP_KERNEL);  
	if (!state->planes)  
		goto fail;  
  
	state->dev = dev;				// [3]  
  
	...  
}  
int drm_atomic_helper_commit(struct drm_device \*dev,  
			     struct drm_atomic_state \*state,  
			     bool nonblock)  
{  
     ...  
	INIT_WORK(&state->commit_work, commit_work);		// [4]  
	...  
          
    drm_atomic_state_get(state);		// state->ref==2  
	if (nonblock)  
		queue_work(system_unbound_wq, &state->commit_work);  
	else  
		commit_tail(state);  
  
}  
static void commit_tail(struct drm_atomic_state \*old_state)  
{  
    ...  
	  
	else  
		drm_atomic_helper_commit_tail(old_state);		// [5]  
	...  
}  
void drm_atomic_helper_commit_tail(struct drm_atomic_state \*old_state)  
{  
	struct drm_device \*dev = old_state->dev;			// [6]  
         ...  
	drm_atomic_helper_wait_for_vblanks(dev, old_state);		// [7]  
	...  
}  
void  
drm_atomic_helper_wait_for_vblanks(struct drm_device \*dev,  
		struct drm_atomic_state \*old_state)  
{  
	...  
		ret = wait_event_timeout(dev->vblank[i].queue,		// [8] use-after-free  
				old_state->crtcs[i].last_vblank_count !=  
					drm_crtc_vblank_count(crtc),  
				msecs_to_jiffies(100));  
	...  
}  
thread0                             thread1  
drm_mode_atomic_ioctl       |  
  drm_atomic_helper_commit  |  
   queue_work               |  
                            |         close  
                            |          drm_dev_release  
   commit_tail              |  
    drm_atomic_helper_wait_for_vblanks |   
      dev->vblank[i].queue  // uaf     |  
[1] https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v6.1/drivers/gpu/drm/drm_atomic_uapi.c;l=1338  
[2] https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v6.1/drivers/gpu/drm/drm_atomic_uapi.c;l=1428  
[3] https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v6.1/drivers/gpu/drm/drm_atomic.c;l=143  
[4] https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v6.1/drivers/gpu/drm/drm_atomic_helper.c;l=1963  
[5] https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v6.1/drivers/gpu/drm/drm_atomic_helper.c;l=1771  
[6] https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v6.1/drivers/gpu/drm/drm_atomic_helper.c;l=1682  
[7] https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v6.1/drivers/gpu/drm/drm_atomic_helper.c;l=1582  
[8] https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v6.1/drivers/gpu/drm/drm_atomic_helper.c;l=1613  
  
\*\*VERSION\*\*  
Operating System: ChromiumOS Kernel v6.1 stable + dev  
  
\*\*FIX PATCH SUGGESTION\*\*  
I think the follwing patch should fix the problem.  
  
Two fixes come to mind:  
1.Removed non-blocking functions to prevent use-after-free vulnerabilities due to race conditions  
2.Added a judgment on dev usage to drm_atomic_helper_wait_for_vblanks to prevent usage after release.  
  
**Additional Comments:**   
  
  
**Chrome version: ** 114.0.0.0 **Channel: ** Stable  
  
**OS:** Chrome OS

```

## Attachments

- [kasan.txt](attachments/kasan.txt) (text/plain, 3.9 KB)
- [1-diff.diff](attachments/1-diff.diff) (text/plain, 1.3 KB)
- [2-diff.diff](attachments/2-diff.diff) (text/plain, 1.1 KB)

## Timeline

### [Deleted User] (2023-07-12)

[Empty comment from Monorail migration]

### da...@chromium.org (2023-07-12)

[Empty comment from Monorail migration]

### ch...@google.com (2023-07-13)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/291021772). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

[Monorail blocking: b/291021772]

### [Deleted User] (2023-07-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-16)

[Empty comment from Monorail migration]

### ch...@google.com (2023-08-04)

fix is merged in v5.4, v5.10, v5.10-arcvm, and was pulled into v5.15 and v6.1 via stable tree. If needed I can cherry-pick back to v4.19 and v4.14. Although I think the only way this could be triggered on a chromebook would require physical access (ie. unplugging a udl/evdi display)

### [Deleted User] (2023-08-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-04)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-11-15)

Congratulations! 
The VRP Panel has decided to award you $750 for this report. 
A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in discovering and reporting this issue to us -- great work! 
Please be mindful that previous reward decisions made by the Chrome VRP should not be considered precedent for potential future ChromeOS VRP reward amounts or decisions.

### am...@google.com (2023-11-18)

[Empty comment from Monorail migration]

### is...@google.com (2023-11-18)

This issue was migrated from crbug.com/chromium/1464137?no_tracker_redirect=1

[Monorail blocking: b/291021772]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40067259)*
