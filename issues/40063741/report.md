# Security: Error Path Double Free in __i915_gem_ttm_object_init

| Field | Value |
|-------|-------|
| **Issue ID** | [40063741](https://issues.chromium.org/issues/40063741) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU |
| **Platforms** | ChromeOS |
| **Reporter** | lm...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-03-24 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

ioctl$I915\_GEM\_CREATE\_EXT will call \*i915\_gem\_create\_ext\_ioctl\* to create \*drm\_i915\_gem\_object\*. If the type of \*intel\_memory\_region\* is \*INTEL\_MEMORY\_SYSTEM\*, it will call \*\_\_i915\_gem\_ttm\_object\_init\*[1]. \*\_\_i915\_gem\_ttm\_object\_init\* will call \*ttm\_bo\_init\_reserved\*[2] to init the bo object with \*i915\_ttm\_bo\_destroy\* as destroy. If \*ttm\_resource\_alloc\* failed, \*ttm\_bo\_put\*[3] will be called to release the bo object, and \*i915\_ttm\_bo\_destroy\*[4] will be called. \*\_\_i915\_gem\_free\_object\*[5] is called in \*i915\_ttm\_bo\_destroy\*, and \*obj->mm.placements\* is freed[6]. But after \*\_\_i915\_gem\_ttm\_object\_init\* return, \*obj->mm.placements\* will be freed again[7], causing double free.

```
static struct drm_i915_gem_object \*  
__i915_gem_object_create_user_ext(struct drm_i915_private \*i915, u64 size,  
				  struct intel_memory_region \*\*placements,  
				  unsigned int n_placements,  
				  unsigned int ext_flags)  
{  
	struct intel_memory_region \*mr = placements[0];  
	struct drm_i915_gem_object \*obj;  
	unsigned int flags;  
	int ret;  
  
	i915_gem_flush_free_objects(i915);  
  
	size = round_up(size, object_max_page_size(placements, n_placements));  
	if (size == 0)  
		return ERR_PTR(-EINVAL);  
  
	/\* For most of the ABI (e.g. mmap) we think in system pages \*/  
	GEM_BUG_ON(!IS_ALIGNED(size, PAGE_SIZE));  
  
	if (i915_gem_object_size_2big(size))  
		return ERR_PTR(-E2BIG);  
  
	obj = i915_gem_object_alloc();  
	if (!obj)  
		return ERR_PTR(-ENOMEM);  
  
	ret = object_set_placements(obj, placements, n_placements);  
	if (ret)  
		goto object_free;  
  
	/\*  
	 \* I915_BO_ALLOC_USER will make sure the object is cleared before  
	 \* any user access.  
	 \*/  
	flags = I915_BO_ALLOC_USER;  
  
	ret = mr->ops->init_object(mr, obj, size, 0, flags);			// [1]  
	if (ret)  
		goto object_free;  
  
	GEM_BUG_ON(size != obj->base.size);  
  
	/\* Add any flag set by create_ext options \*/  
	obj->flags |= ext_flags;  
  
	trace_i915_gem_object_create(obj);  
	return obj;  
  
object_free:  
	if (obj->mm.n_placements > 1)  
		kfree(obj->mm.placements);									// [7]  
	i915_gem_object_free(obj);  
	return ERR_PTR(ret);  
}  
  
int __i915_gem_ttm_object_init(struct intel_memory_region \*mem,  
			       struct drm_i915_gem_object \*obj,  
			       resource_size_t size,  
			       resource_size_t page_size,  
			       unsigned int flags)  
{  
	static struct lock_class_key lock_class;  
	struct drm_i915_private \*i915 = mem->i915;  
	struct ttm_operation_ctx ctx = {  
		.interruptible = true,  
		.no_wait_gpu = false,  
	};  
	enum ttm_bo_type bo_type;  
	int ret;  
  
	drm_gem_private_object_init(&i915->drm, &obj->base, size);  
	i915_gem_object_init(obj, &i915_gem_ttm_obj_ops, &lock_class, flags);  
	i915_gem_object_init_memory_region(obj, mem);  
	i915_gem_object_make_unshrinkable(obj);  
	INIT_RADIX_TREE(&obj->ttm.get_io_page.radix, GFP_KERNEL | __GFP_NOWARN);  
	mutex_init(&obj->ttm.get_io_page.lock);  
	bo_type = (obj->flags & I915_BO_ALLOC_USER) ? ttm_bo_type_device :  
		ttm_bo_type_kernel;  
  
	obj->base.vma_node.driver_private = i915_gem_to_ttm(obj);  
  
	/\* Forcing the page size is kernel internal only \*/  
	GEM_BUG_ON(page_size && obj->mm.n_placements);  
  
	/\*  
	 \* If this function fails, it will call the destructor, but  
	 \* our caller still owns the object. So no freeing in the  
	 \* destructor until obj->ttm.created is true.  
	 \* Similarly, in delayed_destroy, we can't call ttm_bo_put()  
	 \* until successful initialization.  
	 \*/  
	ret = ttm_bo_init_reserved(&i915->bdev, i915_gem_to_ttm(obj), size,  
				   bo_type, &i915_sys_placement,  
				   page_size >> PAGE_SHIFT,  
				   &ctx, NULL, NULL, i915_ttm_bo_destroy);				// [2]  
	if (ret)  
		return i915_ttm_err_to_gem(ret);  
  
	obj->ttm.created = true;  
	i915_ttm_adjust_domains_after_move(obj);  
	i915_ttm_adjust_gem_after_move(obj);  
	i915_gem_object_unlock(obj);  
  
	return 0;  
}  
  
int ttm_bo_init_reserved(struct ttm_device \*bdev,  
			 struct ttm_buffer_object \*bo,  
			 size_t size,  
			 enum ttm_bo_type type,  
			 struct ttm_placement \*placement,  
			 uint32_t page_alignment,  
			 struct ttm_operation_ctx \*ctx,  
			 struct sg_table \*sg,  
			 struct dma_resv \*resv,  
			 void (\*destroy) (struct ttm_buffer_object \*))  
{  
	static const struct ttm_place sys_mem = { .mem_type = TTM_PL_SYSTEM };  
	bool locked;  
	int ret;  
  
	bo->destroy = destroy ? destroy : ttm_bo_default_destroy;  
  
	kref_init(&bo->kref);  
	INIT_LIST_HEAD(&bo->lru);  
	INIT_LIST_HEAD(&bo->ddestroy);  
	bo->bdev = bdev;  
	bo->type = type;  
	bo->page_alignment = page_alignment;  
	bo->moving = NULL;  
	bo->pin_count = 0;  
	bo->sg = sg;  
	if (resv) {  
		bo->base.resv = resv;  
		dma_resv_assert_held(bo->base.resv);  
	} else {  
		bo->base.resv = &bo->base._resv;  
	}  
	atomic_inc(&ttm_glob.bo_count);  
  
	ret = ttm_resource_alloc(bo, &sys_mem, &bo->resource);  
	if (unlikely(ret)) {  
		ttm_bo_put(bo);												// [3]  
		return ret;  
	}  
  
	/\*  
	 \* For ttm_bo_type_device buffers, allocate  
	 \* address space from the device.  
	 \*/  
	if (bo->type == ttm_bo_type_device ||  
	    bo->type == ttm_bo_type_sg)  
		ret = drm_vma_offset_add(bdev->vma_manager, &bo->base.vma_node,  
					 bo->resource->num_pages);  
  
	/\* passed reservation objects should already be locked,  
	 \* since otherwise lockdep will be angered in radeon.  
	 \*/  
	if (!resv) {  
		locked = dma_resv_trylock(bo->base.resv);  
		WARN_ON(!locked);  
	}  
  
	if (likely(!ret))  
		ret = ttm_bo_validate(bo, placement, ctx);  
  
	if (unlikely(ret)) {  
		if (!resv)  
			ttm_bo_unreserve(bo);  
  
		ttm_bo_put(bo);  
		return ret;  
	}  
  
	ttm_bo_move_to_lru_tail_unlocked(bo);  
  
	return ret;  
}  
  
static void ttm_bo_release(struct kref \*kref)  
{  
	struct ttm_buffer_object \*bo =  
	    container_of(kref, struct ttm_buffer_object, kref);  
	struct ttm_device \*bdev = bo->bdev;  
	int ret;  
  
	WARN_ON_ONCE(bo->pin_count);  
  
	if (!bo->deleted) {  
		ret = ttm_bo_individualize_resv(bo);  
		if (ret) {  
			/\* Last resort, if we fail to allocate memory for the  
			 \* fences block for the BO to become idle  
			 \*/  
			dma_resv_wait_timeout(bo->base.resv, true, false,  
					      30 \* HZ);  
		}  
  
		if (bo->bdev->funcs->release_notify)  
			bo->bdev->funcs->release_notify(bo);  
  
		drm_vma_offset_remove(bdev->vma_manager, &bo->base.vma_node);  
		ttm_mem_io_free(bdev, bo->resource);  
	}  
  
	if (!dma_resv_test_signaled(bo->base.resv, true) ||  
	    !dma_resv_trylock(bo->base.resv)) {  
		/\* The BO is not idle, resurrect it for delayed destroy \*/  
		ttm_bo_flush_all_fences(bo);  
		bo->deleted = true;  
  
		spin_lock(&bo->bdev->lru_lock);  
  
		/\*  
		 \* Make pinned bos immediately available to  
		 \* shrinkers, now that they are queued for  
		 \* destruction.  
		 \*  
		 \* FIXME: QXL is triggering this. Can be removed when the  
		 \* driver is fixed.  
		 \*/  
		if (bo->pin_count) {  
			bo->pin_count = 0;  
			ttm_bo_move_to_lru_tail(bo, bo->resource, NULL);  
		}  
  
		kref_init(&bo->kref);  
		list_add_tail(&bo->ddestroy, &bdev->ddestroy);  
		spin_unlock(&bo->bdev->lru_lock);  
  
		schedule_delayed_work(&bdev->wq,  
				      ((HZ / 100) < 1) ? 1 : HZ / 100);  
		return;  
	}  
  
	spin_lock(&bo->bdev->lru_lock);  
	ttm_bo_del_from_lru(bo);  
	list_del(&bo->ddestroy);  
	spin_unlock(&bo->bdev->lru_lock);  
  
	ttm_bo_cleanup_memtype_use(bo);  
	dma_resv_unlock(bo->base.resv);  
  
	atomic_dec(&ttm_glob.bo_count);  
	dma_fence_put(bo->moving);  
	bo->destroy(bo);												// [4]  
}  
  
void i915_ttm_bo_destroy(struct ttm_buffer_object \*bo)  
{  
	struct drm_i915_gem_object \*obj = i915_ttm_to_gem(bo);  
  
	i915_ttm_backup_free(obj);  
  
	/\* This releases all gem object bindings to the backend. \*/  
	__i915_gem_free_object(obj);									// [5]  
  
	i915_gem_object_release_memory_region(obj);  
	mutex_destroy(&obj->ttm.get_io_page.lock);  
  
	if (obj->ttm.created)  
		call_rcu(&obj->rcu, __i915_gem_free_object_rcu);  
}  
  
void __i915_gem_free_object(struct drm_i915_gem_object \*obj)  
{  
	trace_i915_gem_object_destroy(obj);  
  
	if (!list_empty(&obj->vma.list)) {  
		struct i915_vma \*vma;  
  
		/\*  
		 \* Note that the vma keeps an object reference while  
		 \* it is active, so it \*should\* not sleep while we  
		 \* destroy it. Our debug code errs insits it \*might\*.  
		 \* For the moment, play along.  
		 \*/  
		spin_lock(&obj->vma.lock);  
		while ((vma = list_first_entry_or_null(&obj->vma.list,  
						       struct i915_vma,  
						       obj_link))) {  
			GEM_BUG_ON(vma->obj != obj);  
			spin_unlock(&obj->vma.lock);  
  
			__i915_vma_put(vma);  
  
			spin_lock(&obj->vma.lock);  
		}  
		spin_unlock(&obj->vma.lock);  
	}  
  
	__i915_gem_object_free_mmaps(obj);  
  
	GEM_BUG_ON(!list_empty(&obj->lut_list));  
  
	atomic_set(&obj->mm.pages_pin_count, 0);  
	__i915_gem_object_put_pages(obj);  
	GEM_BUG_ON(i915_gem_object_has_pages(obj));  
	bitmap_free(obj->bit_17);  
  
	if (obj->base.import_attach)  
		drm_prime_gem_destroy(&obj->base, NULL);  
  
	drm_gem_free_mmap_offset(&obj->base);  
  
	if (obj->ops->release)  
		obj->ops->release(obj);  
  
	if (obj->mm.n_placements > 1)  
		kfree(obj->mm.placements);									// [6]  
  
	if (obj->shares_resv_from)  
		i915_vm_resv_put(obj->shares_resv_from);  
}  

```

[1] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.10/drivers/gpu/drm/i915/gem/i915_gem_create.c;drc=68177cb357da8fbac8bccb37274de421cb9b2c5d;l=123>  

[2] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.10/drivers/gpu/drm/i915/gem/i915_gem_ttm.c;drc=6bc831189bf119dfb8e7c4a1d03d47b6e39cb6a2;l=967>  

[3] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.10/drivers/gpu/drm/ttm/ttm_bo.c;drc=cfdcfd1a727794a2e1f979945b839ad285e6395d;l=1035>  

[4] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.10/drivers/gpu/drm/ttm/ttm_bo.c;drc=cfdcfd1a727794a2e1f979945b839ad285e6395d;l=468>  

[5] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.10/drivers/gpu/drm/i915/gem/i915_gem_ttm.c;drc=6bc831189bf119dfb8e7c4a1d03d47b6e39cb6a2;l=910>  

[6] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.10/drivers/gpu/drm/i915/gem/i915_gem_object.c;drc=0b3177871457f026f37d623ff76f370cc88dbd16;l=253>  

[7] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.10/drivers/gpu/drm/i915/gem/i915_gem_create.c;drc=68177cb357da8fbac8bccb37274de421cb9b2c5d;l=137>

**VERSION**  

Operating System: ChromiumOS Kernel 5.10 stable + dev

**REPRODUCTION CASE**  

This issue is discovered by manual code review, I will try to construct a poc to reproduce it.

BISECT  

<https://source.chromium.org/chromiumos/_/chromium/chromiumos/third_party/kernel/+/d5f0b6b8a98bd964a69c8b77513577a7b74e61e9>

FIX PATCH SUGGESTION  

I think the follwing patch should fix the problem.

```
diff --git a/drivers/gpu/drm/i915/gem/i915_gem_ttm.c b/drivers/gpu/drm/i915/gem/i915_gem_ttm.c  
index f6e3cc76b277..464c4e25d934 100644  
--- a/drivers/gpu/drm/i915/gem/i915_gem_ttm.c  
+++ b/drivers/gpu/drm/i915/gem/i915_gem_ttm.c  
@@ -906,14 +906,15 @@ void i915_ttm_bo_destroy(struct ttm_buffer_object \*bo)  
   
        i915_ttm_backup_free(obj);  
   
-       /\* This releases all gem object bindings to the backend. \*/  
-       __i915_gem_free_object(obj);  
-  
        i915_gem_object_release_memory_region(obj);  
        mutex_destroy(&obj->ttm.get_io_page.lock);  
   
        if (obj->ttm.created)  
+       {  
+               /\* This releases all gem object bindings to the backend. \*/  
+               __i915_gem_free_object(obj);  
                call_rcu(&obj->rcu, __i915_gem_free_object_rcu);  
+       }  
 }  

```

RELATE LINK

<https://www.spinics.net/lists/stable-commits/msg285902.html>

## Timeline

### [Deleted User] (2023-03-24)

[Empty comment from Monorail migration]

### hc...@google.com (2023-03-24)

Moving to ChromeOS queue

### ch...@google.com (2023-03-24)

Your report will be worked on in the Buganizer system ( link: https://issuetracker.google.com/issues/275067118 ). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on.

[Monorail blocking: b/275067118]

### [Deleted User] (2023-03-24)

[Empty comment from Monorail migration]

### ch...@google.com (2023-04-18)

Marked as fixed because of linked buganizer https://crbug.com/chromium/1427353#c10:

It looks like upstream commit 068396bb21c ("drm/i915/ttm: Rework object initialization slightly") addresses this problem. That patch is already present in chromeos-5.15, and it applies cleanly to chromeos-5.10. I'll submit a CL while the process here plays out.

Also https://crbug.com/chromium/1427353#c12:
Since patch was already present in 5.15 (and now applied to 5.10) closing this.

### ch...@google.com (2023-04-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-20)

[Empty comment from Monorail migration]

### pa...@chromium.org (2023-04-25)

Thank you once again for the report, analysis, and patch!

Given the preconditions in ChromeOS, this looks like Medium to me. (Kernel double free could very well be higher severity in general, but in a ChromeOS context I think this applies: https://chromium.googlesource.com/chromiumos/docs/+/master/security_severity_guidelines.md#Medium-Severity, "...potentially harmful when combined with other bugs." You have to pop a renderer and get into the GPU process first. Which of course is possible.)

[Monorail components: Internals>GPU]

### al...@google.com (2023-04-27)

Does this require root or is an open device fd good enough?

### lm...@gmail.com (2023-04-28)

An open device fd is good enough. It is same as https://crbug.com/chromium/1415129.

### jo...@chromium.org (2023-05-23)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-23)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2023-06-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-01)

Thank you for this report! As this issue was previously known and fixed well before the time of this report. We'd like to extended to you this $1,000 thank you reward since this reported helped ensure that the upstream patch was merged into ChromeOS! 

### am...@google.com (2023-06-03)

[Empty comment from Monorail migration]

### lm...@gmail.com (2023-06-05)

Hi, did you know about the missing patch before I reported it to you? This report (https://crbug.com/chromium/1357303) is also missing the patch, but rewarded $7k, please reconsider the bounty. Thanks.

### am...@chromium.org (2023-06-05)

Hello, yes we knew about the patch was already present in one of the ChromeOS builds / versions as per https://crbug.com/chromium/1427353#c10 in the buganizer issue and we did know about or have access to the patch at the time of the report in https://crbug.com/chromium/1357303. This reward amount has been determined as sufficient for this issue and instance. 

### lm...@gmail.com (2023-06-06)

Hi, The patch was released in upstream kernel in 2022. You guys only patched on 5.15, not on 5.10, If I hadn't reported this to you guys, you might have missed the patch on 5.10 entirely. By the way, both of these report are missing patch, why the difference in rewards so much?

### al...@google.com (2023-06-07)

If this bug hadn't been known upstream and your report led to both an upstream fix and and us picking the fixes it would deserve a bigger reward than a report like this where we missed cherry-picking the fix to one of the kernel branches.

### [Deleted User] (2023-07-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-07-26)

This issue was migrated from crbug.com/chromium/1427353?no_tracker_redirect=1

[Monorail blocking: b/275067118]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063741)*
