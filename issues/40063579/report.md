# Security: Race Condition UAF in radeon_gem_set_domain_ioctl

| Field | Value |
|-------|-------|
| **Issue ID** | [40063579](https://issues.chromium.org/issues/40063579) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>GPU>VendorSpecific |
| **Platforms** | ChromeOS |
| **Reporter** | lm...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2023-03-14 |
| **Bounty** | $250.00 |

## Description

**VULNERABILITY DETAILS**

The root cause of this issue is similar to <https://crbug.com/chromium/1400113>, race condition UAF.

ioctl$RADEON\_GEM\_SET\_DOMAIN will call \*radeon\_gem\_set\_domain\_ioctl\* function[1] to set domain. \*gobj\* is obtained via \*drm\_gem\_object\_lookup\*[1], which reference count will be two(one for filp->object\_idr, and another one added in \*drm\_gem\_object\_lookup\* for \*gobj\*). \*robj\* is converted from \*gobj\* via \*gem\_to\_radeon\_bo\*[2]. Then \*gobj\* is put via \*drm\_gem\_object\_put\*, and the reference count will be one. There will be a race contion UAF, if \*radeon\_gem\_object\_free\*(\*robj\* will be freed[6]) is called after release the lock[4], and before \*radeon\_gem\_handle\_lockup\*[5].

```
int radeon_gem_set_domain_ioctl(struct drm_device \*dev, void \*data,  
        struct drm_file \*filp)  
{  
  /\* transition the BO to a domain -  
   \* just validate the BO into a certain domain \*/  
  struct radeon_device \*rdev = dev->dev_private;  
  struct drm_radeon_gem_set_domain \*args = data;  
  struct drm_gem_object \*gobj;  
  struct radeon_bo \*robj;  
  int r;  
  
  /\* for now if someone requests domain CPU -  
   \* just make sure the buffer is finished with \*/  
  down_read(&rdev->exclusive_lock);  
  
  /\* just do a BO wait for now \*/  
  gobj = drm_gem_object_lookup(filp, args->handle);   // [1]  
  if (gobj == NULL) {  
    up_read(&rdev->exclusive_lock);  
    return -ENOENT;  
  }  
  robj = gem_to_radeon_bo(gobj);                  // [2]  
  
  r = radeon_gem_set_domain(gobj, args->read_domains, args->write_domain);  
  
  drm_gem_object_put(gobj);                     // [3]  
  up_read(&rdev->exclusive_lock);               // [4]  
  r = radeon_gem_handle_lockup(robj->rdev, r);    // [5]  
  return r;  
}  
  
static void radeon_gem_object_free(struct drm_gem_object \*gobj)  
{  
  struct radeon_bo \*robj = gem_to_radeon_bo(gobj);  
  
  if (robj) {  
    radeon_mn_unregister(robj);  
    radeon_bo_unref(&robj);   // [6]  
  }  
}  

```

[1] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.15/drivers/gpu/drm/radeon/radeon_gem.c;drc=22058040e0b6e1a490fe0d0af150519bfe01773e;l=470>  

[2] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.15/drivers/gpu/drm/radeon/radeon_gem.c;drc=22058040e0b6e1a490fe0d0af150519bfe01773e;l=475>  

[3] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.15/drivers/gpu/drm/radeon/radeon_gem.c;drc=22058040e0b6e1a490fe0d0af150519bfe01773e;l=479>  

[4] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.15/drivers/gpu/drm/radeon/radeon_gem.c;drc=22058040e0b6e1a490fe0d0af150519bfe01773e;l=480>  

[5] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.15/drivers/gpu/drm/radeon/radeon_gem.c;drc=22058040e0b6e1a490fe0d0af150519bfe01773e;l=481>  

[6] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.15/drivers/gpu/drm/radeon/radeon_gem.c;drc=22058040e0b6e1a490fe0d0af150519bfe01773e;l=90>

**VERSION**  

Operating System: ChromiumOS Kernel 5.15 stable + dev

**REPRODUCTION CASE**  

This issue is discovered by manual code review, I will try to construct a poc to reproduce it.

BISECT  

<https://source.chromium.org/chromiumos/_/chromium/chromiumos/third_party/kernel/+/6c6f478370eccfbfafbdc6fc55c0def03e58f124>

FIX PATCH SUGGESTION  

I think the follwing patch should fix the problem.

```
diff --git a/drivers/gpu/drm/radeon/radeon_gem.c b/drivers/gpu/drm/radeon/radeon_gem.c  
index 261fcbae88d7..9e7c2680c8f1 100644  
--- a/drivers/gpu/drm/radeon/radeon_gem.c  
+++ b/drivers/gpu/drm/radeon/radeon_gem.c  
@@ -478,7 +478,7 @@ int radeon_gem_set_domain_ioctl(struct drm_device \*dev, void \*data,  
   
        drm_gem_object_put(gobj);  
        up_read(&rdev->exclusive_lock);  
-       r = radeon_gem_handle_lockup(robj->rdev, r);  
+       r = radeon_gem_handle_lockup(rdev, r);  
        return r;  
 }  

```

## Attachments

- [poc.c](attachments/poc.c) (text/plain, 1.5 KB)

## Timeline

### [Deleted User] (2023-03-14)

[Empty comment from Monorail migration]

### lm...@gmail.com (2023-03-14)

Here is the poc, and the timeline. I found that maybe there is nothing to do with rdev->exclusive_lock, I check the free path, it would not hold this lock.

radeon_gem_set_domain_ioctl			|
	drm_gem_object_lookup			|
									|		drm_gem_close_ioctl
									|			drm_gem_object_put
		drm_gem_object_put			|
			radeon_gem_object_free
		radeon_gem_handle_lockup <---- UAF

### ts...@chromium.org (2023-03-14)

Over to ChromeOS sheriff rotation.

### th...@google.com (2023-03-20)

[Empty comment from Monorail migration]

[Monorail components: Internals>GPU>VendorSpecific]

### [Deleted User] (2023-03-24)

[Empty comment from Monorail migration]

### lm...@gmail.com (2023-05-10)

Hi, friendly ping. Is there any updates?

### lm...@gmail.com (2023-05-10)

Looks like Lenovo 300e Chromebook is using AMD Radeon GPU.

https://psref.lenovo.com/syspool/Sys/PDF/Lenovo/Lenovo_300e_Chromebook_2nd_Gen_AST/Lenovo_300e_Chromebook_2nd_Gen_AST_Spec.pdf

### ro...@chromium.org (2023-05-10)

I believe the kernel driver used is the newer drm/amdgpu

### lm...@gmail.com (2023-05-11)

Hello, I'm a bit confused. I would be very grateful if you could answer the following questions.

1. Does the Lenovo 300e Chromebook is using v5.10 or v5.15 kernel?
2. I see the Graphics is AMD Radeon R4 Graphics, so shouldn’t it use a drm/radeon driver?

Thanks.

### ro...@chromium.org (2023-05-12)

drm/radeon is used for older amd/ati GPUs.  Everything Southern Islands (SI) and later uses amdgpu.  There are no chromebooks which use an old enough amd to use drm/radeon.

### lm...@gmail.com (2023-05-15)

Thank you very much for your answer! 

### ro...@google.com (2023-05-23)

@lm0963hack@gmail.com Please report this bug upstream so it can get fixed. When fixed upstream please let us know so we can close the bug. If we close it sooner it will become public before a fix is available.

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### lm...@gmail.com (2023-05-27)

Hi, re #12, sure, I have sent a patch to upstream.

### ch...@google.com (2023-07-26)

Dear lm0963hack@gmail.com ,

Do you have already updates on the patch? 

### ch...@google.com (2023-08-10)

Friendly Ping....any updates here?

### ch...@google.com (2023-09-15)

Final ping...any updates?

### lm...@gmail.com (2023-09-15)

Hi, I'm very sorry, I missed these messages. I have sent a patch to upstream months ago, https://lore.kernel.org/all/20230526123753.16160-1-lm0963hack@gmail.com/

### ch...@google.com (2023-09-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-29)

[Empty comment from Monorail migration]

### ro...@google.com (2023-12-13)

Looks like this fell through the cracks in terms of panel review, our apologies.

Although there are no chromebooks which use an old enough amd to use drm/radeon to be impacted, we appreciate you getting the patch upstream.

### ch...@google.com (2023-12-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-14)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2023-12-15)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-05)

This issue was migrated from crbug.com/chromium/1424264?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063579)*
