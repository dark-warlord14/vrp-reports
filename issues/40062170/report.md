# Security: Race Condition UAF in panfrost_ioctl_create_bo

| Field | Value |
|-------|-------|
| **Issue ID** | [40062170](https://issues.chromium.org/issues/40062170) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | OS>Packages |
| **Platforms** | ChromeOS |
| **Reporter** | lm...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2022-12-11 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**

It is another bug which root case is similar to <https://crbug.com/chromium/1400037> which I submitted earlier. Still a race condition uaf.

ioctl$DRM\_IOCTL\_PANFROST\_CREATE\_BO will call \*panfrost\_gem\_create\_with\_handle\* function[1] to register \*panfrost\_gem\_object\*[2] (created in \*drm\_gem\_shmem\_create\*[3]) as a handle which can be deleted by ioctl$DRM\_IOCTL\_GEM\_CLOSE, and afterwards decrease refcount of it[4]. But after decrease the refcount, it will access the \*panfrost\_gem\_object\* again[5]. So there is a race condition Use-After-Free.

```
static int panfrost_ioctl_create_bo(struct drm_device \*dev, void \*data,  
    struct drm_file \*file)  
{  
  struct panfrost_file_priv \*priv = file->driver_priv;  
  struct panfrost_gem_object \*bo;  
  struct drm_panfrost_create_bo \*args = data;  
  struct panfrost_gem_mapping \*mapping;  
  
  if (!args->size || args->pad ||  
      (args->flags & ~(PANFROST_BO_NOEXEC | PANFROST_BO_HEAP)))  
    return -EINVAL;  
  
  /\* Heaps should never be executable \*/  
  if ((args->flags & PANFROST_BO_HEAP) &&  
      !(args->flags & PANFROST_BO_NOEXEC))  
    return -EINVAL;  
  
  bo = panfrost_gem_create_with_handle(file, dev, args->size, args->flags,  
               &args->handle);    // [1]  
  if (IS_ERR(bo))  
    return PTR_ERR(bo);  
  
  mapping = panfrost_gem_mapping_get(bo, priv);   // [5]  
  if (!mapping) {  
    drm_gem_object_put(&bo->base.base);  
    return -EINVAL;  
  }  
  
  args->offset = mapping->mmnode.start << PAGE_SHIFT;  
  panfrost_gem_mapping_put(mapping);  
  
  return 0;  
}  

```
```
struct panfrost_gem_object \*  
panfrost_gem_create_with_handle(struct drm_file \*file_priv,  
        struct drm_device \*dev, size_t size,  
        u32 flags,  
        uint32_t \*handle)  
{  
  int ret;  
  struct drm_gem_shmem_object \*shmem;  
  struct panfrost_gem_object \*bo;  
  
  /\* Round up heap allocations to 2MB to keep fault handling simple \*/  
  if (flags & PANFROST_BO_HEAP)  
    size = roundup(size, SZ_2M);  
  
  shmem = drm_gem_shmem_create(dev, size);      // [3]  
  if (IS_ERR(shmem))  
    return ERR_CAST(shmem);  
  
  bo = to_panfrost_bo(&shmem->base);  
  bo->noexec = !!(flags & PANFROST_BO_NOEXEC);  
  bo->is_heap = !!(flags & PANFROST_BO_HEAP);  
  
  /\*  
   \* Allocate an id of idr table where the obj is registered  
   \* and handle has the id what user can see.  
   \*/  
  ret = drm_gem_handle_create(file_priv, &shmem->base, handle);   // [2]  
  /\* drop reference from allocate - handle holds it now. \*/  
  drm_gem_object_put(&shmem->base);       // [4]  
  if (ret)  
    return ERR_PTR(ret);  
  
  return bo;  
}  

```

[1] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/upstream/drivers/gpu/drm/panfrost/panfrost_drv.c;drc=3c197a6778dbde9e0dffa060524d4a9213c28156;l=95>  

[2] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/upstream/drivers/gpu/drm/panfrost/panfrost_gem.c;drc=d315bdbfebd517cf5efabf666c8099e027ef666f;l=263>  

[3] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/upstream/drivers/gpu/drm/panfrost/panfrost_gem.c;drc=d315bdbfebd517cf5efabf666c8099e027ef666f;l=251>  

[4] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/upstream/drivers/gpu/drm/panfrost/panfrost_gem.c;drc=d315bdbfebd517cf5efabf666c8099e027ef666f;l=265>  

[5] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/upstream/drivers/gpu/drm/panfrost/panfrost_drv.c;drc=3c197a6778dbde9e0dffa060524d4a9213c28156;l=100>

**VERSION**  

Operating System: ChromiumOS Kernel 5.15.81 stable + dev

**REPRODUCTION CASE**  

\*\*Because it is a race condition, please add some msleep before and after drm\_gem\_object\_put[4] to stably reproduce the bug. \*\*  

\*\*Real ARM Mail series GPU devices are required to trigger the bug. Because the bug is in the panfrost driver. \*\*

1. Compile poc.
2. Run poc in ChromiumOS system. (please make sure current user is in video group. it needs the privilege to access drm to trigger this bug).

FIX PATCH SUGGESTION  

I think the follwing patch should fix the problem.

```
diff --git a/drivers/gpu/drm/panfrost/panfrost_drv.c b/drivers/gpu/drm/panfrost/panfrost_drv.c  
index 84c7f9afd60b..b9aaae0d153c 100644  
--- a/drivers/gpu/drm/panfrost/panfrost_drv.c  
+++ b/drivers/gpu/drm/panfrost/panfrost_drv.c  
@@ -98,6 +98,7 @@ static int panfrost_ioctl_create_bo(struct drm_device \*dev, void \*data,  
                return PTR_ERR(bo);  
   
        mapping = panfrost_gem_mapping_get(bo, priv);  
+       drm_gem_object_put(&bo->base.base);  
        if (!mapping) {  
                drm_gem_object_put(&bo->base.base);  
                return -EINVAL;  
diff --git a/drivers/gpu/drm/panfrost/panfrost_gem.c b/drivers/gpu/drm/panfrost/panfrost_gem.c  
index 293e799e2fe8..03b2c8a4a349 100644  
--- a/drivers/gpu/drm/panfrost/panfrost_gem.c  
+++ b/drivers/gpu/drm/panfrost/panfrost_gem.c  
@@ -262,9 +262,11 @@ panfrost_gem_create_with_handle(struct drm_file \*file_priv,  
         \*/  
        ret = drm_gem_handle_create(file_priv, &shmem->base, handle);  
        /\* drop reference from allocate - handle holds it now. \*/  
-       drm_gem_object_put(&shmem->base);  
        if (ret)  
+       {  
+               drm_gem_object_put(&shmem->base);  
                return ERR_PTR(ret);  
+       }  
   
        return bo;  
 }  

```

## Attachments

- [panfrost_ioctl_create_bo_race_condition_uaf.c](attachments/panfrost_ioctl_create_bo_race_condition_uaf.c) (text/plain, 1.3 KB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2022-12-11)

[Empty comment from Monorail migration]

### ad...@google.com (2022-12-11)

[Empty comment from Monorail migration]

### le...@google.com (2022-12-12)

[Empty comment from Monorail migration]

[Monorail components: OS>Packages]

### ad...@google.com (2022-12-12)

leonwinter@ hello! The OS-Linux label here means that this affects Chrome on the Linux platform, which isn't correct. Putting this back to affecting just ChromeOS.

### le...@google.com (2022-12-12)

Hi adetaylor@, the files are present in upstream Linux:
https://github.com/torvalds/linux/blob/master/drivers/gpu/drm/panfrost/panfrost_drv.c
https://github.com/torvalds/linux/blob/master/drivers/gpu/drm/panfrost/panfrost_gem.c

### le...@google.com (2022-12-12)

[Empty comment from Monorail migration]

### le...@google.com (2022-12-12)

[Empty comment from Monorail migration]

### jo...@chromium.org (2022-12-14)

[Empty comment from Monorail migration]

[Monorail blocked-on: b/262449744]

### jo...@chromium.org (2022-12-14)

P1 since it's a protection domain bypass (non-root to kernel.)

### [Deleted User] (2022-12-14)

[Empty comment from Monorail migration]

### aa...@google.com (2022-12-21)

We're discussing internally how to best process these upstream kernel issues. Tentatively assigning this to roxabee@ for further triage.

### aa...@google.com (2022-12-21)

[Empty comment from Monorail migration]

### ro...@google.com (2023-01-03)

I believe this was fixed. @robdclark@google.com to confirm fix and close if appropriate.

Note putting this as found in 108 but may not be reachable if hardware not present.

### [Deleted User] (2023-01-03)

[Empty comment from Monorail migration]

### ro...@chromium.org (2023-01-03)

re: https://crbug.com/chromium/1400113#c13, yes fixed now (panfrost disabled in all kernels, plus upstream fix landed in v5.15 kernel for good measure.

### lm...@gmail.com (2023-01-04)

re: https://crbug.com/chromium/1400113#c15, hi, sir, I see that the panfrost is used in arm64 architecture. what do you mean *panfrost disabled in all kernels*? Are you going to disable panfrost? Looking forward to your reply, thanks.

https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/upstream/chromeos/config/chromeos/arm64/chromiumos-arm64.flavour.config;drc=784398b9f90d3c3059a1c0fc05dee55fbab6959f;l=57

### ro...@chromium.org (2023-01-04)

it is already disabled in our production kernels, the link you gave is not used for production devices (just for enabling regression testing with upstream kernels)

### lm...@gmail.com (2023-01-04)

re: https://crbug.com/chromium/1400113#c17, hi, sir, I checked the configuration file under Chromebook. The latest version still has the panfrost config. And I compiled the latest chromiumos, the panfrost config is there too. Please check out the attachments.

### lm...@gmail.com (2023-01-04)

Oh, I see the disable panfrost commit, which did not picked into chromiumos yet, so I missed it. Thank you for your explanation.

### [Deleted User] (2023-01-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-04)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-04)

[Empty comment from Monorail migration]

### ro...@chromium.org (2023-01-04)

re: https://crbug.com/chromium/1400113#c18 https://crbug.com/chromium/1400113#c19,  now it is cherry-picked for M110 and M109 branches so you should see it showing up on M109 and later shortly

### am...@google.com (2023-01-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-12)

Congratulations! The VRP Panel has decided to award you $20,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. In the interim, please let us know what name/tag/identifier you would like us to use in acknowledging you for this finding. 
Thank you for your efforts in discovering and reporting this issue to us -- great work! 

### am...@google.com (2023-01-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1400113?no_tracker_redirect=1

[Monorail blocked-on: b/262449744]
[Monorail mergedwith: crbug.com/chromium/1400114]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062170)*
