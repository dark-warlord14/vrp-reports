# Security: Race Condition UAF in evdi_gem_create

| Field | Value |
|-------|-------|
| **Issue ID** | [40063655](https://issues.chromium.org/issues/40063655) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | OS>Packages |
| **Platforms** | ChromeOS |
| **Reporter** | lm...@gmail.com |
| **Assignee** | ro...@google.com |
| **Created** | 2023-03-18 |
| **Bounty** | $11,000.00 |

## Description

**VULNERABILITY DETAILS**

The root cause of this issue is similar to <https://crbug.com/chromium/1400037>, race condition UAF.

ioctl$DRM\_IOCTL\_MODE\_CREATE\_DUMB will call \*drm\_mode\_create\_dumb\_ioctl\* to crate \*drm\_gem\_object\*. If the gpu driver is evdi, it will finally call \*evdi\_dumb\_create\* which will call \*evdi\_gem\_create\*.

It will create a \*evdi\_gem\_object\* obj[1], which reference count is one. And register it as a handle via \*drm\_gem\_handle\_create\*, if \*drm\_gem\_handle\_create\* succeeds, the reference count will be two, and the obj can be deleted by ioctl$DRM\_IOCTL\_GEM\_CLOSE. Afterwards the reference count will be decreased by \*drm\_gem\_object\_put[\_unlocked]\*[3]. But after \*drm\_gem\_object\_put[\_unlocked]\*, it will be accessed again[4]. So there is a race condition Use-After-Free, if ioctl$DRM\_IOCTL\_GEM\_CLOSE is called before the obj is accessed again. \*drm\_gem\_object\_put[\_unlocked]\* should be the last thing to do, after that we should not access the obj again.

```
static int  
evdi_gem_create(struct drm_file \*file,  
    struct drm_device \*dev, uint64_t size, uint32_t \*handle_p)  
{  
  struct evdi_gem_object \*obj;  
  int ret;  
  u32 handle;  
  
  size = roundup(size, PAGE_SIZE);  
  
  obj = evdi_gem_alloc_object(dev, size);                   // [1]  
  if (obj == NULL)  
    return -ENOMEM;  
  
  ret = drm_gem_handle_create(file, &obj->base, &handle);   // [2]  
  if (ret) {  
    drm_gem_object_release(&obj->base);  
    kfree(obj);  
    return ret;  
  }  
#if KERNEL_VERSION(5, 9, 0) <= LINUX_VERSION_CODE || defined(EL8)  
  drm_gem_object_put(&obj->base);  
#else  
  drm_gem_object_put_unlocked(&obj->base);                  // [3]  
#endif  
  obj->allow_sw_cursor_rect_updates = evdi_was_called_by_mutter();    // [4]  
  \*handle_p = handle;  
  return 0;  
}  

```

[1] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.15/drivers/gpu/drm/evdi/evdi_gem.c;drc=21e8975e1cdd80e1e0d92df30469862425d8dd12;l=133>  

[2] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.15/drivers/gpu/drm/evdi/evdi_gem.c;drc=21e8975e1cdd80e1e0d92df30469862425d8dd12;l=137>  

[3] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.15/drivers/gpu/drm/evdi/evdi_gem.c;drc=21e8975e1cdd80e1e0d92df30469862425d8dd12;l=146>  

[4] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.15/drivers/gpu/drm/evdi/evdi_gem.c;drc=21e8975e1cdd80e1e0d92df30469862425d8dd12;l=148>

evdi\_gem\_create |  

drm\_gem\_handle\_create[2] | drm\_gem\_close\_ioctl  

drm\_gem\_object\_put\_unlocked[3] | drm\_gem\_object\_put <--- free  

obj->allow\_sw\_cursor\_rect\_updates <---------UAF

**VERSION**  

Operating System: ChromiumOS Kernel 5.15 stable + dev

**REPRODUCTION CASE**  

This issue is discovered by manual code review, I will try to construct a poc to reproduce it.

BISECT  

<https://source.chromium.org/chromiumos/_/chromium/chromiumos/third_party/kernel/+/3d6ddf1e7bb622fb4bb8a0c79380a98a7b69c35b>

FIX PATCH SUGGESTION  

I think the follwing patch should fix the problem.

```
diff --git a/drivers/gpu/drm/evdi/evdi_gem.c b/drivers/gpu/drm/evdi/evdi_gem.c  
index 424c19758c65..b0e7aac20a6c 100644  
--- a/drivers/gpu/drm/evdi/evdi_gem.c  
+++ b/drivers/gpu/drm/evdi/evdi_gem.c  
@@ -140,12 +140,12 @@ evdi_gem_create(struct drm_file \*file,  
                kfree(obj);  
                return ret;  
        }  
+       obj->allow_sw_cursor_rect_updates = evdi_was_called_by_mutter();  
 #if KERNEL_VERSION(5, 9, 0) <= LINUX_VERSION_CODE || defined(EL8)  
        drm_gem_object_put(&obj->base);  
 #else  
        drm_gem_object_put_unlocked(&obj->base);  
 #endif  
-       obj->allow_sw_cursor_rect_updates = evdi_was_called_by_mutter();  
        \*handle_p = handle;  
        return 0;  
 }  

```

## Attachments

- [poc.c](attachments/poc.c) (text/plain, 1.5 KB)
- [virtio_kasan.log](attachments/virtio_kasan.log) (text/plain, 4.3 KB)

## Timeline

### [Deleted User] (2023-03-18)

[Empty comment from Monorail migration]

### lm...@gmail.com (2023-03-18)

Here is the poc.

### ts...@chromium.org (2023-03-20)

[Empty comment from Monorail migration]

### ha...@google.com (2023-03-21)

groek@ could you please have a look to see if this is actionable

[Monorail components: OS>Packages]

### gr...@chromium.org (2023-03-21)

Similar to the other evdi problem.


### gr...@chromium.org (2023-03-21)

Rob, please let me know if you are not the right owner for this.

### gr...@chromium.org (2023-03-21)

[Empty comment from Monorail migration]

### lu...@synaptics.com (2023-03-22)

Does this poc is working?
I am running it on Ubuntu 22.04  and I don't have any crash.

To my knowledge this is unlikely since evdi_gem_object can't be freed as evdi_gem_create function didn't finished yet.
This function behaves in similar way as inboxed generic shmem gem implementation.
Please see drm_gem_shmem_create_with_handle https://elixir.bootlin.com/linux/latest/source/drivers/gpu/drm/drm_gem_shmem_helper.c#L417

If this is some kind of contest then please CC me when poc is working I will gladly fix it :)


### lm...@gmail.com (2023-03-22)

Hi, this issue is a race condition problem, may be not easy to reproduce. Could you add some msleep after drm_gem_handle_create to expand the time window? Sorry I don't have a evdi environment, but the poc is similar to the poc of virtio, I think it should work.

Here is a very similar issue, and please check the virtio_kasan.log which contains the virtio UAF stack.
https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4150632

### lm...@gmail.com (2023-03-23)

[Comment Deleted]

### lu...@synaptics.com (2023-03-23)

Great catch. Let me check it, I will prepare patches for it.

### lu...@synaptics.com (2023-03-24)

The poc app also revealed leak of shmem baked buffer memory that was holded by evdi_gem_object, this was leading to rapid running out of memory.

I am preparing fixes for ChromeOS and evdi on github.
Rob, Groeck what is the procedure with releaseing such security issues?
Should we port that fixes to stable and beta branch as well?

regards
Łukasz Spintzyk

### lu...@synaptics.com (2023-03-24)

Since predictive gem handle caused so many troubles, maybe it should be randomized. But this is something for kernel mailing list I guess.

### gr...@google.com (2023-03-24)

#12: Yes, we should apply the patch to R112. Do we have a matching bug in buganizer ? We'll need to ask for permission to commit into R112.


### [Deleted User] (2023-03-24)

[Empty comment from Monorail migration]

### lu...@synaptics.com (2023-03-27)

#14 I have raised issue in internal bug tracker.
https://partnerissuetracker.corp.google.com/issues/275049376

### lu...@synaptics.com (2023-03-28)

Hi Rob, groeck 
Please review.

This was applied to 4.4, 4.14, 4.19, 5.4, 5.10 and 5.15 kernels here:
https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4373673
https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4373675
https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377239
https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377241
https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377243
https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377245
https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377246




### gi...@appspot.gserviceaccount.com (2023-03-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/81899cc5f3a065849ebd6d2e022bae71b9dca41c

commit 81899cc5f3a065849ebd6d2e022bae71b9dca41c
Author: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Date: Fri Mar 24 09:07:32 2023

CHROMIUM: drm/evdi: Fix memory leak in evdi_gem_object

This fixes shmem backed buffer leak on free of evdi_gem_object.

BUG=b:275049376,chromium:1425637
TEST=Tested on wide range of chromebooks

Change-Id: I15f2614a5e0c22c10bfdab0ef0a308122ce2b8ba
Signed-off-by: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377239
Commit-Queue: Guenter Roeck <groeck@chromium.org>
Reviewed-by: Guenter Roeck <groeck@chromium.org>
Tested-by: Guenter Roeck <groeck@chromium.org>

[modify] https://crrev.com/81899cc5f3a065849ebd6d2e022bae71b9dca41c/drivers/gpu/drm/evdi/evdi_gem.c


### gi...@appspot.gserviceaccount.com (2023-03-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/320afb1f8996e8d70858432239b11823b58f6e7a

commit 320afb1f8996e8d70858432239b11823b58f6e7a
Author: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Date: Fri Mar 24 09:50:51 2023

CHROMIUM: drm/evdi: Access drm_gem_object before decreasing ref-count to prevent UAF

BUG=b:275049376,chromium:1425637
TEST=Tested on wide range of chromebooks

Change-Id: Ia3e45ee8dc54f5ddbd7490f5aec86d21014744df
Signed-off-by: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377246
Commit-Queue: Guenter Roeck <groeck@chromium.org>
Reviewed-by: Guenter Roeck <groeck@chromium.org>
Tested-by: Guenter Roeck <groeck@chromium.org>

[modify] https://crrev.com/320afb1f8996e8d70858432239b11823b58f6e7a/drivers/gpu/drm/evdi/evdi_gem.c


### gi...@appspot.gserviceaccount.com (2023-03-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/2998a61e96e89b1e928bc72685198022d9a03541

commit 2998a61e96e89b1e928bc72685198022d9a03541
Author: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Date: Fri Mar 24 09:48:25 2023

CHROMIUM: drm/evdi: Fix memory leak in evdi_gem_object

This fixes shmem backed buffer leak on free of evdi_gem_object.

BUG=b:275049376,chromium:1425637
TEST=Tested on wide range of chromebooks

Change-Id: I1acb80d9b96a6ceaa4b07302eef75eba9d8f931c
Signed-off-by: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377245
Tested-by: Guenter Roeck <groeck@chromium.org>
Reviewed-by: Guenter Roeck <groeck@chromium.org>
Commit-Queue: Guenter Roeck <groeck@chromium.org>

[modify] https://crrev.com/2998a61e96e89b1e928bc72685198022d9a03541/drivers/gpu/drm/evdi/evdi_gem.c


### gi...@appspot.gserviceaccount.com (2023-03-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/e24762aee48f2efcd7437c27ccd18f17b3e818b0

commit e24762aee48f2efcd7437c27ccd18f17b3e818b0
Author: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Date: Fri Mar 24 09:44:30 2023

CHROMIUM: drm/evdi: Fix memory leak in evdi_gem_object

This fixes shmem backed buffer leak on free of evdi_gem_object.

BUG=b:275049376,chromium:1425637
TEST=Tested on wide range of chromebooks

Change-Id: I59cd97e9c68181492df3544ebc10376213a1ee9c
Signed-off-by: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377243
Commit-Queue: Guenter Roeck <groeck@chromium.org>
Tested-by: Guenter Roeck <groeck@chromium.org>
Reviewed-by: Guenter Roeck <groeck@chromium.org>

[modify] https://crrev.com/e24762aee48f2efcd7437c27ccd18f17b3e818b0/drivers/gpu/drm/evdi/evdi_gem.c


### gi...@appspot.gserviceaccount.com (2023-03-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/5987d629f5675cee58acad7433a45dd73e0c7ec2

commit 5987d629f5675cee58acad7433a45dd73e0c7ec2
Author: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Date: Fri Mar 24 09:39:35 2023

CHROMIUM: drm/evdi: Fix memory leak in evdi_gem_object

This fixes shmem backed buffer leak on free of evdi_gem_object.

BUG=b:275049376,chromium:1425637
TEST=Tested on wide range of chromebooks

Change-Id: I4285ebec3ddc135f10de337a575d1320ee626138
Signed-off-by: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377241
Reviewed-by: Guenter Roeck <groeck@chromium.org>
Tested-by: Guenter Roeck <groeck@chromium.org>
Commit-Queue: Guenter Roeck <groeck@chromium.org>

[modify] https://crrev.com/5987d629f5675cee58acad7433a45dd73e0c7ec2/drivers/gpu/drm/evdi/evdi_gem.c


### gi...@appspot.gserviceaccount.com (2023-04-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/783b488e4611b2759e11b15e4170b036b565fb17

commit 783b488e4611b2759e11b15e4170b036b565fb17
Author: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Date: Fri Mar 24 09:07:32 2023

CHROMIUM: drm/evdi: Fix memory leak in evdi_gem_object

This fixes shmem backed buffer leak on free of evdi_gem_object.

BUG=b:275049376,chromium:1425637
TEST=Tested on wide range of chromebooks

Change-Id: I15f2614a5e0c22c10bfdab0ef0a308122ce2b8ba
Signed-off-by: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4373675
Tested-by: Guenter Roeck <groeck@chromium.org>
Reviewed-by: Guenter Roeck <groeck@chromium.org>

[modify] https://crrev.com/783b488e4611b2759e11b15e4170b036b565fb17/drivers/gpu/drm/evdi/evdi_gem.c


### gi...@appspot.gserviceaccount.com (2023-04-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/1bda071e56e4058488f7269d2faa9a0a303f918e

commit 1bda071e56e4058488f7269d2faa9a0a303f918e
Author: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Date: Fri Mar 24 09:50:51 2023

CHROMIUM: drm/evdi: Access drm_gem_object before decreasing ref-count to prevent UAF

BUG=b:275049376,chromium:1425637
TEST=Tested on wide range of chromebooks
UPSTREAM-TASK=b:275865175

Change-Id: Id7854d993e314dfe1debcd1f9a507a4abb7fb749
Signed-off-by: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377246
Commit-Queue: Guenter Roeck <groeck@chromium.org>
Reviewed-by: Guenter Roeck <groeck@chromium.org>
Tested-by: Guenter Roeck <groeck@chromium.org>
(cherry picked from commit 320afb1f8996e8d70858432239b11823b58f6e7a)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4384507

[modify] https://crrev.com/1bda071e56e4058488f7269d2faa9a0a303f918e/drivers/gpu/drm/evdi/evdi_gem.c


### gi...@appspot.gserviceaccount.com (2023-04-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/13816a4bfbe821500403d79086c415e0e649ba15

commit 13816a4bfbe821500403d79086c415e0e649ba15
Author: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Date: Fri Mar 24 09:48:25 2023

CHROMIUM: drm/evdi: Fix memory leak in evdi_gem_object

This fixes shmem backed buffer leak on free of evdi_gem_object.

BUG=b:275049376,chromium:1425637
TEST=Tested on wide range of chromebooks
UPSTREAM-TASK=b:275865175

Change-Id: I1def1a490e88a8cc9b38db817015be7f6e0387a4
Signed-off-by: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377245
Tested-by: Guenter Roeck <groeck@chromium.org>
Reviewed-by: Guenter Roeck <groeck@chromium.org>
Commit-Queue: Guenter Roeck <groeck@chromium.org>
(cherry picked from commit 2998a61e96e89b1e928bc72685198022d9a03541)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4384506

[modify] https://crrev.com/13816a4bfbe821500403d79086c415e0e649ba15/drivers/gpu/drm/evdi/evdi_gem.c


### gi...@appspot.gserviceaccount.com (2023-04-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/d935e5d60d7fe34836148705a4902453167eb61c

commit d935e5d60d7fe34836148705a4902453167eb61c
Author: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Date: Fri Mar 24 09:44:30 2023

CHROMIUM: drm/evdi: Fix memory leak in evdi_gem_object

This fixes shmem backed buffer leak on free of evdi_gem_object.

BUG=b:275049376,chromium:1425637
TEST=Tested on wide range of chromebooks
UPSTREAM-TASK=b:275865175

Change-Id: I53912f126b202062666062ca1b00cc8e668ae8f2
Signed-off-by: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377243
Commit-Queue: Guenter Roeck <groeck@chromium.org>
Tested-by: Guenter Roeck <groeck@chromium.org>
Reviewed-by: Guenter Roeck <groeck@chromium.org>
(cherry picked from commit e24762aee48f2efcd7437c27ccd18f17b3e818b0)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4384504

[modify] https://crrev.com/d935e5d60d7fe34836148705a4902453167eb61c/drivers/gpu/drm/evdi/evdi_gem.c


### gi...@appspot.gserviceaccount.com (2023-04-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/50457f3103decea569e119ad8783790aacacfc95

commit 50457f3103decea569e119ad8783790aacacfc95
Author: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Date: Fri Mar 24 09:07:32 2023

CHROMIUM: drm/evdi: Fix memory leak in evdi_gem_object

This fixes shmem backed buffer leak on free of evdi_gem_object.

BUG=b:275049376,chromium:1425637
TEST=Tested on wide range of chromebooks
UPSTREAM-TASK=b:275865175

Change-Id: Id1b0756d2253b404ecd803bd8ca02c6cd573f8b5
Signed-off-by: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4373675
Tested-by: Guenter Roeck <groeck@chromium.org>
Reviewed-by: Guenter Roeck <groeck@chromium.org>
(cherry picked from commit 783b488e4611b2759e11b15e4170b036b565fb17)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4392567
Commit-Queue: Guenter Roeck <groeck@chromium.org>

[modify] https://crrev.com/50457f3103decea569e119ad8783790aacacfc95/drivers/gpu/drm/evdi/evdi_gem.c


### gi...@appspot.gserviceaccount.com (2023-04-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/e5b61cf936e0192081bf0f902a0be2205f515d89

commit e5b61cf936e0192081bf0f902a0be2205f515d89
Author: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Date: Fri Mar 24 09:07:32 2023

CHROMIUM: drm/evdi: Fix memory leak in evdi_gem_object

This fixes shmem backed buffer leak on free of evdi_gem_object.

BUG=b:275049376,chromium:1425637
TEST=Tested on wide range of chromebooks
UPSTREAM-TASK=b:275049376

Change-Id: I044e357960efa49679c2158e593f06118a239529
Signed-off-by: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377239
Commit-Queue: Guenter Roeck <groeck@chromium.org>
Reviewed-by: Guenter Roeck <groeck@chromium.org>
Tested-by: Guenter Roeck <groeck@chromium.org>
(cherry picked from commit 81899cc5f3a065849ebd6d2e022bae71b9dca41c)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4384220

[modify] https://crrev.com/e5b61cf936e0192081bf0f902a0be2205f515d89/drivers/gpu/drm/evdi/evdi_gem.c


### gi...@appspot.gserviceaccount.com (2023-04-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/53d130a909144942d9e36131609da8dc0389318a

commit 53d130a909144942d9e36131609da8dc0389318a
Author: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Date: Fri Mar 24 09:39:35 2023

CHROMIUM: drm/evdi: Fix memory leak in evdi_gem_object

This fixes shmem backed buffer leak on free of evdi_gem_object.

BUG=b:275049376,chromium:1425637
TEST=Tested on wide range of chromebooks
UPSTREAM-TASK=b:275865175

Change-Id: Id1fd037023267c1ea06e9ea13e884a8cdb5fb388
Signed-off-by: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377241
Reviewed-by: Guenter Roeck <groeck@chromium.org>
Tested-by: Guenter Roeck <groeck@chromium.org>
Commit-Queue: Guenter Roeck <groeck@chromium.org>
(cherry picked from commit 5987d629f5675cee58acad7433a45dd73e0c7ec2)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4384222

[modify] https://crrev.com/53d130a909144942d9e36131609da8dc0389318a/drivers/gpu/drm/evdi/evdi_gem.c


### gi...@appspot.gserviceaccount.com (2023-04-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/9799d3cf8bba0a0a94c9f4e43ea31c676d0316a4

commit 9799d3cf8bba0a0a94c9f4e43ea31c676d0316a4
Author: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Date: Fri Mar 24 09:07:32 2023

CHROMIUM: drm/evdi: Fix memory leak in evdi_gem_object

This fixes shmem backed buffer leak on free of evdi_gem_object.

BUG=b:275049376,chromium:1425637
TEST=Tested on wide range of chromebooks
UPSTREAM-TASK=b:275748739

Change-Id: Ifad54ca30635c8c4824ac8f6ccca7c74eb4cc93c
Signed-off-by: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4373675
Tested-by: Guenter Roeck <groeck@chromium.org>
Reviewed-by: Guenter Roeck <groeck@chromium.org>
(cherry picked from commit 783b488e4611b2759e11b15e4170b036b565fb17)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4392569
Commit-Queue: Guenter Roeck <groeck@chromium.org>

[modify] https://crrev.com/9799d3cf8bba0a0a94c9f4e43ea31c676d0316a4/drivers/gpu/drm/evdi/evdi_gem.c


### gi...@appspot.gserviceaccount.com (2023-04-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/f49060490d5796f47402b847753ca228aac80959

commit f49060490d5796f47402b847753ca228aac80959
Author: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Date: Fri Mar 24 09:44:30 2023

CHROMIUM: drm/evdi: Fix memory leak in evdi_gem_object

This fixes shmem backed buffer leak on free of evdi_gem_object.

BUG=b:275049376,chromium:1425637
TEST=Tested on wide range of chromebooks
UPSTREAM-TASK=b:275748739

Change-Id: I3a59a622b1a79f046894199c318587d31e12e723
Signed-off-by: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377243
Commit-Queue: Guenter Roeck <groeck@chromium.org>
Tested-by: Guenter Roeck <groeck@chromium.org>
Reviewed-by: Guenter Roeck <groeck@chromium.org>
(cherry picked from commit e24762aee48f2efcd7437c27ccd18f17b3e818b0)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4384215

[modify] https://crrev.com/f49060490d5796f47402b847753ca228aac80959/drivers/gpu/drm/evdi/evdi_gem.c


### gi...@appspot.gserviceaccount.com (2023-04-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/15dd0dbd1d96314517c43335bbda1dfe2a3ec3ef

commit 15dd0dbd1d96314517c43335bbda1dfe2a3ec3ef
Author: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Date: Fri Mar 24 09:50:51 2023

CHROMIUM: drm/evdi: Access drm_gem_object before decreasing ref-count to prevent UAF

BUG=b:275049376,chromium:1425637
TEST=Tested on wide range of chromebooks
UPSTREAM-TASK=b:275748739

Change-Id: I45721d4bc91f7bf9f841c1dfc17ba9eb5f9c7922
Signed-off-by: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377246
Commit-Queue: Guenter Roeck <groeck@chromium.org>
Reviewed-by: Guenter Roeck <groeck@chromium.org>
Tested-by: Guenter Roeck <groeck@chromium.org>
(cherry picked from commit 320afb1f8996e8d70858432239b11823b58f6e7a)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4384218

[modify] https://crrev.com/15dd0dbd1d96314517c43335bbda1dfe2a3ec3ef/drivers/gpu/drm/evdi/evdi_gem.c


### gi...@appspot.gserviceaccount.com (2023-04-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/6436580484bd8034b6f626d14de194728f34d992

commit 6436580484bd8034b6f626d14de194728f34d992
Author: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Date: Fri Mar 24 09:48:25 2023

CHROMIUM: drm/evdi: Fix memory leak in evdi_gem_object

This fixes shmem backed buffer leak on free of evdi_gem_object.

BUG=b:275049376,chromium:1425637
TEST=Tested on wide range of chromebooks
UPSTREAM-TASK=b:275748739

Change-Id: Ice9ad6de16808a6013904a7bd07eb1082207bb0b
Signed-off-by: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377245
Tested-by: Guenter Roeck <groeck@chromium.org>
Reviewed-by: Guenter Roeck <groeck@chromium.org>
Commit-Queue: Guenter Roeck <groeck@chromium.org>
(cherry picked from commit 2998a61e96e89b1e928bc72685198022d9a03541)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4384217

[modify] https://crrev.com/6436580484bd8034b6f626d14de194728f34d992/drivers/gpu/drm/evdi/evdi_gem.c


### gi...@appspot.gserviceaccount.com (2023-04-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/da0c1392f4b02cc0b817e80a988ed9aa7ec8ab64

commit da0c1392f4b02cc0b817e80a988ed9aa7ec8ab64
Author: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Date: Fri Mar 24 09:07:32 2023

CHROMIUM: drm/evdi: Fix memory leak in evdi_gem_object

This fixes shmem backed buffer leak on free of evdi_gem_object.

BUG=b:275049376,chromium:1425637
TEST=Tested on wide range of chromebooks
UPSTREAM-TASK=b:275748739

Change-Id: Ia830e92d33edbbbbcb3c5dd557933ffd9be84d52
Signed-off-by: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377239
Commit-Queue: Guenter Roeck <groeck@chromium.org>
Reviewed-by: Guenter Roeck <groeck@chromium.org>
Tested-by: Guenter Roeck <groeck@chromium.org>
(cherry picked from commit 81899cc5f3a065849ebd6d2e022bae71b9dca41c)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4384211

[modify] https://crrev.com/da0c1392f4b02cc0b817e80a988ed9aa7ec8ab64/drivers/gpu/drm/evdi/evdi_gem.c


### gi...@appspot.gserviceaccount.com (2023-04-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/f6b1b68997aadd6ac60ebe68e98c6c32e6aa30ee

commit f6b1b68997aadd6ac60ebe68e98c6c32e6aa30ee
Author: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Date: Fri Mar 24 09:39:35 2023

CHROMIUM: drm/evdi: Fix memory leak in evdi_gem_object

This fixes shmem backed buffer leak on free of evdi_gem_object.

BUG=b:275049376,chromium:1425637
TEST=Tested on wide range of chromebooks
UPSTREAM-TASK=b:275748739

Change-Id: Ib9d004ba1e8046a3d0e017ae5f3bc1c21f9943b3
Signed-off-by: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377241
Reviewed-by: Guenter Roeck <groeck@chromium.org>
Tested-by: Guenter Roeck <groeck@chromium.org>
Commit-Queue: Guenter Roeck <groeck@chromium.org>
(cherry picked from commit 5987d629f5675cee58acad7433a45dd73e0c7ec2)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4384213

[modify] https://crrev.com/f6b1b68997aadd6ac60ebe68e98c6c32e6aa30ee/drivers/gpu/drm/evdi/evdi_gem.c


### lm...@gmail.com (2023-04-20)

Hello, maybe this can be marked as fixed and close?

### lu...@synaptics.com (2023-04-20)

This is fixed and can be closed.

### lm...@gmail.com (2023-05-08)

Hi, friendly ping. I see the patch has been merged, maybe this issue can be marked as fixed and close?

### ro...@google.com (2023-05-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-10)

[Empty comment from Monorail migration]

### al...@google.com (2023-05-17)

[Empty comment from Monorail migration]

[Monorail blocked-on: b/275049376]

### ch...@google.com (2023-05-19)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### jo...@chromium.org (2023-05-30)

Userspace -> Kernel using GPU driver is a protection domain bypass, P1, severity high.

### am...@google.com (2023-06-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-09)

Congratulations! The VRP Panel has decided to award you $10,000 for this mildly mitigated (by race condition) security bug + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-06-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-08-16)

This issue was migrated from crbug.com/chromium/1425637?no_tracker_redirect=1

[Monorail blocked-on: b/275049376]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063655)*
