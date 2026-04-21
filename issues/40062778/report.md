# Security: Race Condition Double Free in i915_gem_set_tiling_ioctl

| Field | Value |
|-------|-------|
| **Issue ID** | [40062778](https://issues.chromium.org/issues/40062778) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Internals>GPU>Internals |
| **Platforms** | ChromeOS |
| **Reporter** | lm...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2023-01-24 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**

The root case of this bug is similar to the <https://crbug.com/chromium/1405568> which I submitted earlier.

ioctl$I915\_GEM\_SET\_TILING will call \*i915\_gem\_set\_tiling\_ioctl\* to set tiling\_mode and stride. The main logic is in \*i915\_gem\_object\_set\_tiling\*. If \*tiling\* is \*I915\_TILING\_NONE\*, it will free \*obj->bit\_17\*[1]. There is no lock between the bitmap\_free[1] and the NULL assignment[2]. So if \*i915\_gem\_set\_tiling\_ioctl\* is called twice in the same time(two threads call \*ioctl$I915\_GEM\_SET\_TILING\* in the same time), there will be a race condition double free. The root cause of this bug is that \*i915\_gem\_object\_set\_tiling\* is not locked properly.

```
int  
i915_gem_object_set_tiling(struct drm_i915_gem_object \*obj,  
			   unsigned int tiling, unsigned int stride)  
{  
	struct drm_i915_private \*i915 = to_i915(obj->base.dev);  
	struct i915_vma \*vma;  
	int err;  
  
	/\* Make sure we don't cross-contaminate obj->tiling_and_stride \*/  
	BUILD_BUG_ON(I915_TILING_LAST & STRIDE_MASK);  
  
	GEM_BUG_ON(!i915_tiling_ok(obj, tiling, stride));  
	GEM_BUG_ON(!stride ^ (tiling == I915_TILING_NONE));  
  
	if ((tiling | stride) == obj->tiling_and_stride)  
		return 0;  
  
	if (i915_gem_object_is_framebuffer(obj))  
		return -EBUSY;  
  
	/\* We need to rebind the object if its current allocation  
	 \* no longer meets the alignment restrictions for its new  
	 \* tiling mode. Otherwise we can just leave it alone, but  
	 \* need to ensure that any fence register is updated before  
	 \* the next fenced (either through the GTT or by the BLT unit  
	 \* on older GPUs) access.  
	 \*  
	 \* After updating the tiling parameters, we then flag whether  
	 \* we need to update an associated fence register. Note this  
	 \* has to also include the unfenced register the GPU uses  
	 \* whilst executing a fenced command for an untiled object.  
	 \*/  
  
	i915_gem_object_lock(obj, NULL);  
	if (i915_gem_object_is_framebuffer(obj)) {  
		i915_gem_object_unlock(obj);  
		return -EBUSY;  
	}  
  
	err = i915_gem_object_fence_prepare(obj, tiling, stride);  
	if (err) {  
		i915_gem_object_unlock(obj);  
		return err;  
	}  
  
	/\* If the memory has unknown (i.e. varying) swizzling, we pin the  
	 \* pages to prevent them being swapped out and causing corruption  
	 \* due to the change in swizzling.  
	 \*/  
	if (i915_gem_object_has_pages(obj) &&  
	    obj->mm.madv == I915_MADV_WILLNEED &&  
	    i915->gem_quirks & GEM_QUIRK_PIN_SWIZZLED_PAGES) {  
		if (tiling == I915_TILING_NONE) {  
			GEM_BUG_ON(!i915_gem_object_has_tiling_quirk(obj));  
			i915_gem_object_clear_tiling_quirk(obj);  
			i915_gem_object_make_shrinkable(obj);  
		}  
		if (!i915_gem_object_is_tiled(obj)) {  
			GEM_BUG_ON(i915_gem_object_has_tiling_quirk(obj));  
			i915_gem_object_make_unshrinkable(obj);  
			i915_gem_object_set_tiling_quirk(obj);  
		}  
	}  
  
	spin_lock(&obj->vma.lock);  
	for_each_ggtt_vma(vma, obj) {  
		vma->fence_size =  
			i915_gem_fence_size(i915, vma->size, tiling, stride);  
		vma->fence_alignment =  
			i915_gem_fence_alignment(i915,  
						 vma->size, tiling, stride);  
  
		if (vma->fence)  
			vma->fence->dirty = true;  
	}  
	spin_unlock(&obj->vma.lock);  
  
	obj->tiling_and_stride = tiling | stride;  
	i915_gem_object_unlock(obj);  
  
	/\* Force the fence to be reacquired for GTT access \*/  
	i915_gem_object_release_mmap_gtt(obj);  
  
	/\* Try to preallocate memory required to save swizzling on put-pages \*/  
	if (i915_gem_object_needs_bit17_swizzle(obj)) {  
		if (!obj->bit_17) {  
			obj->bit_17 = bitmap_zalloc(obj->base.size >> PAGE_SHIFT,  
						    GFP_KERNEL);  
		}  
	} else {  
		bitmap_free(obj->bit_17);		// [1]  
		obj->bit_17 = NULL;		// [2]  
	}  
  
	return 0;  
}  

```

i915\_gem\_set\_tiling\_ioctl | i915\_gem\_set\_tiling\_ioctl  

i915\_gem\_object\_set\_tiling | i915\_gem\_object\_set\_tiling  

bitmap\_free[1] | bitmap\_free[1] <--- double free

[1] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/upstream/drivers/gpu/drm/i915/gem/i915_gem_tiling.c;drc=95086cb969b2cb8abe4984457f219ec70d24052e;l=320>  

[2] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/upstream/drivers/gpu/drm/i915/gem/i915_gem_tiling.c;drc=95086cb969b2cb8abe4984457f219ec70d24052e;l=321>

**VERSION**  

Operating System: ChromiumOS Kernel 5.15.81 stable + dev

**REPRODUCTION CASE**  

\*\*It needs to be reproduced in real devices, with specific gpu. Sorry I don't have a chromebook with that gpu. If there is any problem with the poc, please feel free to contact me.\*\*

1. Compile poc.
2. Run poc in ChromiumOS system. (please make sure current user is in video group. it needs the privilege to access drm to trigger this bug).

FIX PATCH SUGGESTION  

I think the follwing patch should fix the problem.

```
diff --git a/drivers/gpu/drm/i915/gem/i915_gem_tiling.c b/drivers/gpu/drm/i915/gem/i915_gem_tiling.c  
index fd42b89b7162..35f088045f95 100644  
--- a/drivers/gpu/drm/i915/gem/i915_gem_tiling.c  
+++ b/drivers/gpu/drm/i915/gem/i915_gem_tiling.c  
@@ -310,6 +310,7 @@ i915_gem_object_set_tiling(struct drm_i915_gem_object \*obj,  
        /\* Force the fence to be reacquired for GTT access \*/  
        i915_gem_object_release_mmap_gtt(obj);  
   
+       i915_gem_object_lock(obj, NULL);  
        /\* Try to preallocate memory required to save swizzling on put-pages \*/  
        if (i915_gem_object_needs_bit17_swizzle(obj)) {  
                if (!obj->bit_17) {  
@@ -320,6 +321,7 @@ i915_gem_object_set_tiling(struct drm_i915_gem_object \*obj,  
                bitmap_free(obj->bit_17);  
                obj->bit_17 = NULL;  
        }  
+       i915_gem_object_unlock(obj);  
   
        return 0;  
 }  

```

## Attachments

- [poc.c](attachments/poc.c) (text/plain, 1.7 KB)

## Timeline

### [Deleted User] (2023-01-24)

[Empty comment from Monorail migration]

### rs...@chromium.org (2023-01-24)

[Empty comment from Monorail migration]

### lz...@google.com (2023-01-26)

[Empty comment from Monorail migration]

[Monorail components: Internals>GPU>Internals]

### ro...@chromium.org (2023-01-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-27)

[Empty comment from Monorail migration]

### ro...@chromium.org (2023-01-27)

https://patchwork.freedesktop.org/series/113448/

### gi...@appspot.gserviceaccount.com (2023-02-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/df09c4ace891fe88d1ca75bf83422abb729ac972

commit df09c4ace891fe88d1ca75bf83422abb729ac972
Author: Rob Clark <robdclark@chromium.org>
Date: Fri Jan 27 20:05:31 2023

FROMGIT: drm/i915: Fix potential bit_17 double-free

A userspace with multiple threads racing I915_GEM_SET_TILING to set the
tiling to I915_TILING_NONE could trigger a double free of the bit_17
bitmask.  (Or conversely leak memory on the transition to tiled.)  Move
allocation/free'ing of the bitmask within the section protected by the
obj lock.

Signed-off-by: Rob Clark <robdclark@chromium.org>
Fixes: 2850748ef876 ("drm/i915: Pull i915_vma_pin under the vm->mutex")
Cc: <stable@vger.kernel.org> # v5.5+
[tursulin: Correct fixes tag and added cc stable.]
Reviewed-by: Tvrtko Ursulin <tvrtko.ursulin@intel.com>
Signed-off-by: Tvrtko Ursulin <tvrtko.ursulin@intel.com>
Link: https://patchwork.freedesktop.org/patch/msgid/20230127200550.3531984-1-robdclark@gmail.com
(cherry picked from commit 10e0cbaaf1104f449d695c80bcacf930dcd3c42e
 git://anongit.freedesktop.org/drm-intel drm-intel-gt-next)

BUG=chromium:1409761
TEST=None

Change-Id: I99007d387bf9df97250e8b7b8d4ae9d1c9fcb4c3
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4203289
Auto-Submit: Rob Clark <robdclark@chromium.org>
Commit-Queue: Rob Clark <robdclark@chromium.org>
Reviewed-by: Matt Turner <msturner@google.com>
Reviewed-by: Sean Paul <sean@poorly.run>
Tested-by: Rob Clark <robdclark@chromium.org>

[modify] https://crrev.com/df09c4ace891fe88d1ca75bf83422abb729ac972/drivers/gpu/drm/i915/gem/i915_gem_tiling.c


### gi...@appspot.gserviceaccount.com (2023-02-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/a44d1b69a20585acced7b4e2b0662064aab02b07

commit a44d1b69a20585acced7b4e2b0662064aab02b07
Author: Rob Clark <robdclark@chromium.org>
Date: Fri Jan 27 20:05:31 2023

FROMGIT: drm/i915: Fix potential bit_17 double-free

A userspace with multiple threads racing I915_GEM_SET_TILING to set the
tiling to I915_TILING_NONE could trigger a double free of the bit_17
bitmask.  (Or conversely leak memory on the transition to tiled.)  Move
allocation/free'ing of the bitmask within the section protected by the
obj lock.

Signed-off-by: Rob Clark <robdclark@chromium.org>
Fixes: 2850748ef876 ("drm/i915: Pull i915_vma_pin under the vm->mutex")
Cc: <stable@vger.kernel.org> # v5.5+
[tursulin: Correct fixes tag and added cc stable.]
Reviewed-by: Tvrtko Ursulin <tvrtko.ursulin@intel.com>
Signed-off-by: Tvrtko Ursulin <tvrtko.ursulin@intel.com>
Link: https://patchwork.freedesktop.org/patch/msgid/20230127200550.3531984-1-robdclark@gmail.com
(cherry picked from commit 10e0cbaaf1104f449d695c80bcacf930dcd3c42e
 git://anongit.freedesktop.org/drm-intel drm-intel-gt-next)

BUG=chromium:1409761
TEST=None

Change-Id: I99007d387bf9df97250e8b7b8d4ae9d1c9fcb4c3
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4203289
Auto-Submit: Rob Clark <robdclark@chromium.org>
Commit-Queue: Rob Clark <robdclark@chromium.org>
Reviewed-by: Matt Turner <msturner@google.com>
Reviewed-by: Sean Paul <sean@poorly.run>
Tested-by: Rob Clark <robdclark@chromium.org>
(cherry picked from commit df09c4ace891fe88d1ca75bf83422abb729ac972)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4220091
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>

[modify] https://crrev.com/a44d1b69a20585acced7b4e2b0662064aab02b07/drivers/gpu/drm/i915/gem/i915_gem_tiling.c


### gi...@appspot.gserviceaccount.com (2023-02-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/3acbf7117e82316a250bcaa5882a3aef8db8264d

commit 3acbf7117e82316a250bcaa5882a3aef8db8264d
Author: Rob Clark <robdclark@chromium.org>
Date: Fri Jan 27 20:05:31 2023

BACKPORT: FROMGIT: drm/i915: Fix potential bit_17 double-free

A userspace with multiple threads racing I915_GEM_SET_TILING to set the
tiling to I915_TILING_NONE could trigger a double free of the bit_17
bitmask.  (Or conversely leak memory on the transition to tiled.)  Move
allocation/free'ing of the bitmask within the section protected by the
obj lock.

Signed-off-by: Rob Clark <robdclark@chromium.org>
Fixes: 2850748ef876 ("drm/i915: Pull i915_vma_pin under the vm->mutex")
Cc: <stable@vger.kernel.org> # v5.5+
[tursulin: Correct fixes tag and added cc stable.]
Reviewed-by: Tvrtko Ursulin <tvrtko.ursulin@intel.com>
Signed-off-by: Tvrtko Ursulin <tvrtko.ursulin@intel.com>
Link: https://patchwork.freedesktop.org/patch/msgid/20230127200550.3531984-1-robdclark@gmail.com
(cherry picked from commit 10e0cbaaf1104f449d695c80bcacf930dcd3c42e
 git://anongit.freedesktop.org/drm-intel drm-intel-gt-next)

BUG=chromium:1409761
TEST=None

Change-Id: I99007d387bf9df97250e8b7b8d4ae9d1c9fcb4c3
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4220092
Reviewed-by: Matt Turner <msturner@google.com>
Auto-Submit: Rob Clark <robdclark@chromium.org>
Commit-Queue: Rob Clark <robdclark@chromium.org>
Tested-by: Rob Clark <robdclark@chromium.org>

[modify] https://crrev.com/3acbf7117e82316a250bcaa5882a3aef8db8264d/drivers/gpu/drm/i915/gem/i915_gem_tiling.c


### ro...@chromium.org (2023-02-08)

all the cherry-picks have landed

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-02-17)

Congratulations on another one! The VRP Panel has decided to award you $20,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-02-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-08-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/224d7ed82b277fd98236b74b087e70f0180fc97e

commit 224d7ed82b277fd98236b74b087e70f0180fc97e
Author: Rob Clark <robdclark@chromium.org>
Date: Fri Jan 27 20:05:31 2023

BACKPORT: FROMGIT: drm/i915: Fix potential bit_17 double-free

A userspace with multiple threads racing I915_GEM_SET_TILING to set the
tiling to I915_TILING_NONE could trigger a double free of the bit_17
bitmask.  (Or conversely leak memory on the transition to tiled.)  Move
allocation/free'ing of the bitmask within the section protected by the
obj lock.

Signed-off-by: Rob Clark <robdclark@chromium.org>
Fixes: 2850748ef876 ("drm/i915: Pull i915_vma_pin under the vm->mutex")
Cc: <stable@vger.kernel.org> # v5.5+
[tursulin: Correct fixes tag and added cc stable.]
Reviewed-by: Tvrtko Ursulin <tvrtko.ursulin@intel.com>
Signed-off-by: Tvrtko Ursulin <tvrtko.ursulin@intel.com>
Link: https://patchwork.freedesktop.org/patch/msgid/20230127200550.3531984-1-robdclark@gmail.com
(cherry picked from commit 10e0cbaaf1104f449d695c80bcacf930dcd3c42e
 git://anongit.freedesktop.org/drm-intel drm-intel-gt-next)

BUG=chromium:1409761, b:294321642
TEST=None

Change-Id: I99007d387bf9df97250e8b7b8d4ae9d1c9fcb4c3
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4220092
Reviewed-by: Matt Turner <msturner@google.com>
Auto-Submit: Rob Clark <robdclark@chromium.org>
Commit-Queue: Rob Clark <robdclark@chromium.org>
Tested-by: Rob Clark <robdclark@chromium.org>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4794597
Commit-Queue: Matt Turner <msturner@google.com>

[modify] https://crrev.com/224d7ed82b277fd98236b74b087e70f0180fc97e/drivers/gpu/drm/i915/i915_gem_tiling.c


### gi...@appspot.gserviceaccount.com (2023-08-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/1b667a6f03f580caa800d3ccb686cbd570fcc04f

commit 1b667a6f03f580caa800d3ccb686cbd570fcc04f
Author: Rob Clark <robdclark@chromium.org>
Date: Fri Jan 27 20:05:31 2023

BACKPORT: FROMGIT: drm/i915: Fix potential bit_17 double-free

A userspace with multiple threads racing I915_GEM_SET_TILING to set the
tiling to I915_TILING_NONE could trigger a double free of the bit_17
bitmask.  (Or conversely leak memory on the transition to tiled.)  Move
allocation/free'ing of the bitmask within the section protected by the
obj lock.

Signed-off-by: Rob Clark <robdclark@chromium.org>
Fixes: 2850748ef876 ("drm/i915: Pull i915_vma_pin under the vm->mutex")
Cc: <stable@vger.kernel.org> # v5.5+
[tursulin: Correct fixes tag and added cc stable.]
Reviewed-by: Tvrtko Ursulin <tvrtko.ursulin@intel.com>
Signed-off-by: Tvrtko Ursulin <tvrtko.ursulin@intel.com>
Link: https://patchwork.freedesktop.org/patch/msgid/20230127200550.3531984-1-robdclark@gmail.com
(cherry picked from commit 10e0cbaaf1104f449d695c80bcacf930dcd3c42e
 git://anongit.freedesktop.org/drm-intel drm-intel-gt-next)

BUG=chromium:1409761, b:294321642
TEST=None

Change-Id: I99007d387bf9df97250e8b7b8d4ae9d1c9fcb4c3
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4220092
Reviewed-by: Matt Turner <msturner@google.com>
Auto-Submit: Rob Clark <robdclark@chromium.org>
Commit-Queue: Rob Clark <robdclark@chromium.org>
Tested-by: Rob Clark <robdclark@chromium.org>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4794596
Commit-Queue: Matt Turner <msturner@google.com>

[modify] https://crrev.com/1b667a6f03f580caa800d3ccb686cbd570fcc04f/drivers/gpu/drm/i915/i915_gem_tiling.c


### is...@google.com (2023-08-18)

This issue was migrated from crbug.com/chromium/1409761?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062778)*
