# Security: UAF in VIRTGPU_RESOURCE_CREATE and VIRTGPU_RESOURCE_CREATE_BLOB

| Field | Value |
|-------|-------|
| **Issue ID** | [40062161](https://issues.chromium.org/issues/40062161) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | OS>Packages |
| **Platforms** | ChromeOS |
| **Reporter** | lm...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2022-12-10 |
| **Bounty** | $21,000.00 |

## Description

**VULNERABILITY DETAILS**

ioctl$DRM\_IOCTL\_VIRTGPU\_RESOURCE\_CREATE will register \*virtio\_gpu\_object\*[1] (created in \*virtio\_gpu\_object\_create\*[2]) as a handle which can be deleted by ioctl$DRM\_IOCTL\_GEM\_CLOSE, and afterwards decrease refcount of it. But after decrease the refcount, it will access the \*virtio\_gpu\_object\* again [4]. So there is race condition Use-After-Free.

```
static int virtio_gpu_resource_create_ioctl(struct drm_device \*dev, void \*data,  
              struct drm_file \*file)  
{  
  ......  
  
  ret = virtio_gpu_object_create(vgdev, &params, &qobj, fence); // [2]  
  dma_fence_put(&fence->f);  
  if (ret < 0)  
    return ret;  
  obj = &qobj->base.base;  
  
  ret = drm_gem_handle_create(file, obj, &handle);  // [1]  
  if (ret) {  
    drm_gem_object_release(obj);  
    return ret;  
  }  
  drm_gem_object_put(obj);  // [3]  
  
  rc->res_handle = qobj->hw_res_handle; /\* similiar to a VM address \*/  // [4] Use-After-Free  
  rc->bo_handle = handle;  
  return 0;  
}  
  

```

[1] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/upstream/drivers/gpu/drm/virtio/virtgpu_ioctl.c;drc=b3dc7c176a65d6cf871cf00ba6c31214ea609dbf;l=356>  

[2] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/upstream/drivers/gpu/drm/virtio/virtgpu_ioctl.c;drc=b3dc7c176a65d6cf871cf00ba6c31214ea609dbf;l=350>  

[3] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/upstream/drivers/gpu/drm/virtio/virtgpu_ioctl.c;drc=b3dc7c176a65d6cf871cf00ba6c31214ea609dbf;l=361>  

[4] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/upstream/drivers/gpu/drm/virtio/virtgpu_ioctl.c;drc=b3dc7c176a65d6cf871cf00ba6c31214ea609dbf;l=363>

**VERSION**  

Operating System: ChromiumOS Kernel 5.15.81 stable + dev

**REPRODUCTION CASE**  

\*\*Because it is a race condition, please apply the patch to stably reproduce the bug. The patch itself has nothing to do with the bug, just adds msleep.\*\*

1. Compile poc with command `gcc poc.c -pthread -o poc`.
2. Run poc in ChromiumOS system. (please make sure current user is in video group. it needs the privilege to access drm to trigger this bug).

FIX PATCH SUGGESTION  

I think the follwing patch should fix the problem.

```
diff --git a/drivers/gpu/drm/virtio/virtgpu_ioctl.c b/drivers/gpu/drm/virtio/virtgpu_ioctl.c  
index 2099255ed893..0b472b1e266e 100644  
--- a/drivers/gpu/drm/virtio/virtgpu_ioctl.c  
+++ b/drivers/gpu/drm/virtio/virtgpu_ioctl.c  
@@ -33,6 +33,7 @@  
 #include <drm/virtgpu_drm.h>  
   
 #include "virtgpu_drv.h"  
+#include <linux/delay.h>  
   
 #define VIRTGPU_BLOB_FLAG_USE_MASK (VIRTGPU_BLOB_FLAG_USE_MAPPABLE | \  
                                    VIRTGPU_BLOB_FLAG_USE_SHAREABLE | \  
@@ -358,9 +359,9 @@ static int virtio_gpu_resource_create_ioctl(struct drm_device \*dev, void \*data,  
                drm_gem_object_release(obj);  
                return ret;  
        }  
+       rc->res_handle = qobj->hw_res_handle; /\* similiar to a VM address \*/  
        drm_gem_object_put(obj);  
   
-       rc->res_handle = qobj->hw_res_handle; /\* similiar to a VM address \*/  
        rc->bo_handle = handle;  
        return 0;  
 }  

```

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: chromiumos kernel  

Crash State: see asan.log for details

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 4.3 KB)
- [patch.diff](attachments/patch.diff) (text/plain, 864 B)
- [poc.c](attachments/poc.c) (text/plain, 1.9 KB)

## Timeline

### lm...@gmail.com (2022-12-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-10)

[Empty comment from Monorail migration]

### ad...@google.com (2022-12-10)

[Empty comment from Monorail migration]

### le...@google.com (2022-12-12)

[Empty comment from Monorail migration]

[Monorail components: OS>Packages]

### ad...@google.com (2022-12-12)

leonwinter@ hello! The OS-Linux label here means that this affects Chrome on the Linux platform, which isn't correct. Putting this back to affecting just ChromeOS.

### le...@google.com (2022-12-12)

[Empty comment from Monorail migration]

### jo...@chromium.org (2022-12-14)

P1 since it's a protection domain bypass (non-root to kernel.)

### aa...@google.com (2022-12-20)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-20)

[Empty comment from Monorail migration]

### aa...@google.com (2022-12-20)

[Empty comment from Monorail migration]

### aa...@google.com (2022-12-20)

[Empty comment from Monorail migration]

### gr...@chromium.org (2022-12-20)

[Empty comment from Monorail migration]

### ro...@chromium.org (2022-12-20)

fwiw, already posted https://patchwork.freedesktop.org/patch/515312/?series=112030&rev=2 if someone wants to pick that into v5.10 and v5.10-arcvm kernel (I am out until next week)

### aa...@google.com (2022-12-21)

We're discussing internally how to best process these upstream kernel issues. Tentatively assigning this to roxabee@ for further triage.

### [Deleted User] (2022-12-21)

[Empty comment from Monorail migration]

### aa...@google.com (2022-12-21)

[Empty comment from Monorail migration]

### lm...@gmail.com (2023-01-09)

Hi, friendly pin, is there any updates?

### gi...@appspot.gserviceaccount.com (2023-01-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/5dc8ff0e03cba0c961cecaf22c277ae90744035f

commit 5dc8ff0e03cba0c961cecaf22c277ae90744035f
Author: Rob Clark <robdclark@chromium.org>
Date: Fri Dec 16 23:33:55 2022

FROMGIT: drm/virtio: Fix GEM handle creation UAF

Userspace can guess the handle value and try to race GEM object creation
with handle close, resulting in a use-after-free if we dereference the
object after dropping the handle's reference.  For that reason, dropping
the handle's reference must be done *after* we are done dereferencing
the object.

Signed-off-by: Rob Clark <robdclark@chromium.org>
Reviewed-by: Chia-I Wu <olvaffe@gmail.com>
Fixes: 62fb7a5e1096 ("virtio-gpu: add 3d/virgl support")
Cc: stable@vger.kernel.org
Signed-off-by: Dmitry Osipenko <dmitry.osipenko@collabora.com>
Link: https://patchwork.freedesktop.org/patch/msgid/20221216233355.542197-2-robdclark@gmail.com
(cherry picked from commit 52531258318ed59a2dc5a43df2eaf0eb1d65438e
 git://anongit.freedesktop.org/drm/drm-misc drm-misc-fixes)

BUG=chromium:1400037
TEST=None

Change-Id: I9ad3c7412c0fe0d3cdab6a98b31de36aa1bc8bc9
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4150632
Reviewed-by: Sean Paul <sean@poorly.run>
Auto-Submit: Rob Clark <robdclark@chromium.org>
Commit-Queue: Chia-I Wu <olv@google.com>
Reviewed-by: Chia-I Wu <olv@google.com>
Tested-by: Rob Clark <robdclark@chromium.org>

[modify] https://crrev.com/5dc8ff0e03cba0c961cecaf22c277ae90744035f/drivers/gpu/drm/virtio/virtgpu_ioctl.c


### gi...@appspot.gserviceaccount.com (2023-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/840f66d8f68e2bb7c458bf2b9b35580b01f6cdde

commit 840f66d8f68e2bb7c458bf2b9b35580b01f6cdde
Author: Rob Clark <robdclark@chromium.org>
Date: Fri Dec 16 23:33:55 2022

FROMGIT: drm/virtio: Fix GEM handle creation UAF

Userspace can guess the handle value and try to race GEM object creation
with handle close, resulting in a use-after-free if we dereference the
object after dropping the handle's reference.  For that reason, dropping
the handle's reference must be done *after* we are done dereferencing
the object.

Signed-off-by: Rob Clark <robdclark@chromium.org>
Reviewed-by: Chia-I Wu <olvaffe@gmail.com>
Fixes: 62fb7a5e1096 ("virtio-gpu: add 3d/virgl support")
Cc: stable@vger.kernel.org
Signed-off-by: Dmitry Osipenko <dmitry.osipenko@collabora.com>
Link: https://patchwork.freedesktop.org/patch/msgid/20221216233355.542197-2-robdclark@gmail.com
(cherry picked from commit 52531258318ed59a2dc5a43df2eaf0eb1d65438e
 git://anongit.freedesktop.org/drm/drm-misc drm-misc-fixes)

BUG=chromium:1400037
TEST=None

Change-Id: I9ad3c7412c0fe0d3cdab6a98b31de36aa1bc8bc9
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4150632
Reviewed-by: Sean Paul <sean@poorly.run>
Auto-Submit: Rob Clark <robdclark@chromium.org>
Commit-Queue: Chia-I Wu <olv@google.com>
Reviewed-by: Chia-I Wu <olv@google.com>
Tested-by: Rob Clark <robdclark@chromium.org>
(cherry picked from commit 5dc8ff0e03cba0c961cecaf22c277ae90744035f)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4151179
Commit-Queue: Rob Clark <robdclark@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>

[modify] https://crrev.com/840f66d8f68e2bb7c458bf2b9b35580b01f6cdde/drivers/gpu/drm/virtio/virtgpu_ioctl.c


### gi...@appspot.gserviceaccount.com (2023-01-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/dab51e00495a8678d39b97e49f5a43946147dbff

commit dab51e00495a8678d39b97e49f5a43946147dbff
Author: Rob Clark <robdclark@chromium.org>
Date: Fri Dec 16 23:33:55 2022

FROMGIT: drm/virtio: Fix GEM handle creation UAF

Userspace can guess the handle value and try to race GEM object creation
with handle close, resulting in a use-after-free if we dereference the
object after dropping the handle's reference.  For that reason, dropping
the handle's reference must be done *after* we are done dereferencing
the object.

Signed-off-by: Rob Clark <robdclark@chromium.org>
Reviewed-by: Chia-I Wu <olvaffe@gmail.com>
Fixes: 62fb7a5e1096 ("virtio-gpu: add 3d/virgl support")
Cc: stable@vger.kernel.org
Signed-off-by: Dmitry Osipenko <dmitry.osipenko@collabora.com>
Link: https://patchwork.freedesktop.org/patch/msgid/20221216233355.542197-2-robdclark@gmail.com
(cherry picked from commit 52531258318ed59a2dc5a43df2eaf0eb1d65438e
 git://anongit.freedesktop.org/drm/drm-misc drm-misc-fixes)

BUG=chromium:1400037
TEST=None

Change-Id: I9ad3c7412c0fe0d3cdab6a98b31de36aa1bc8bc9
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4150632
Reviewed-by: Sean Paul <sean@poorly.run>
Auto-Submit: Rob Clark <robdclark@chromium.org>
Commit-Queue: Chia-I Wu <olv@google.com>
Reviewed-by: Chia-I Wu <olv@google.com>
Tested-by: Rob Clark <robdclark@chromium.org>
(cherry picked from commit 5dc8ff0e03cba0c961cecaf22c277ae90744035f)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4151180
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Rob Clark <robdclark@chromium.org>

[modify] https://crrev.com/dab51e00495a8678d39b97e49f5a43946147dbff/drivers/gpu/drm/virtio/virtgpu_ioctl.c


### ro...@chromium.org (2023-01-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-15)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-01-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/380dda452497972ce7b72919780d749f2439cda4

commit 380dda452497972ce7b72919780d749f2439cda4
Author: Rob Clark <robdclark@chromium.org>
Date: Fri Dec 16 23:33:55 2022

UPSTREAM: drm/virtio: Fix GEM handle creation UAF

Userspace can guess the handle value and try to race GEM object creation
with handle close, resulting in a use-after-free if we dereference the
object after dropping the handle's reference.  For that reason, dropping
the handle's reference must be done *after* we are done dereferencing
the object.

Signed-off-by: Rob Clark <robdclark@chromium.org>
Reviewed-by: Chia-I Wu <olvaffe@gmail.com>
Fixes: 62fb7a5e1096 ("virtio-gpu: add 3d/virgl support")
Cc: stable@vger.kernel.org
Signed-off-by: Dmitry Osipenko <dmitry.osipenko@collabora.com>
Link: https://patchwork.freedesktop.org/patch/msgid/20221216233355.542197-2-robdclark@gmail.com
(cherry picked from commit 52531258318ed59a2dc5a43df2eaf0eb1d65438e)

BUG=chromium:1400037
TEST=None

Change-Id: I9ad3c7412c0fe0d3cdab6a98b31de36aa1bc8bc9
Signed-off-by: Tzung-Bi Shih <tzungbi@chromium.org>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4169797
Reviewed-by: Stéphane Marchesin <marcheu@chromium.org>
Reviewed-by: Sean Paul <sean@poorly.run>

[modify] https://crrev.com/380dda452497972ce7b72919780d749f2439cda4/drivers/gpu/drm/virtio/virtgpu_ioctl.c


### am...@google.com (2023-02-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-02-03)

Congratulations! The VRP Panel has decided to award you $20,000 for this report + $1,000 patch bonus. Thank you for your efforts in discovering and reporting this issue to us -- nice work! 

### am...@google.com (2023-02-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### is...@google.com (2023-05-24)

This issue was migrated from crbug.com/chromium/1400037?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1400039]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062161)*
