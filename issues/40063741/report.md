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
  
ioctl$I915_GEM_CREATE_EXT will call \*i915_gem_create_ext_ioctl\* to create \*drm_i915_gem_object\*. If the type of \*intel_memory_region\* is \*INTEL_MEMORY_SYSTEM\*, it will call \*__i915_gem_ttm_object_init\*[1]. \*__i915_gem_ttm_object_init\* will call \*ttm_bo_in

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063741)*
