# Security: Chrome OS : Multiple bugs in cros_gralloc

| Field | Value |
|-------|-------|
| **Issue ID** | [40066572](https://issues.chromium.org/issues/40066572) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | pi...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-06-28 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

cros\_gralloc is chrome os implementation of Android gralloc for arcvm, it will in gralloc.cros.so inside arcvm.  

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/platform/minigbm/cros_gralloc/>

gralloc is for android graphics allocation,usually different Android gpu platforms(for example, qcom and mali) have their own gralloc implementation. cros\_gralloc is the implementation for arcvm platform to adapt different chromebook gpu platforms.

The core structure in gralloc is the gralloc handle, for cros\_gralloc the handle is struct cros\_gralloc\_handle:  

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/platform/minigbm/cros_gralloc/cros_gralloc_handle.h;drc=21f9c36f0fc8755ab47751e6253754410c5640ca;l=16>

On android, GraphicBuffer object is the wrapper of gralloc handle, GraphicBuffer can transfer from one process to other processes by binder, for example pack GraphicBuffer objects in android Bundle, see my bug report of Mali gralloc:  

<https://bugs.chromium.org/p/chromium/issues/detail?id=1283033>

So the attack scenario is untrusted app can fake the cros\_gralloc\_handle in the GraphicBuffer object, other processes like system\_server and surfaceflinger will import the cros\_gralloc\_handle when recved GraphicBuffer through binder, if the import flow of cros\_gralloc doesn't check the fields of cros\_gralloc\_handle well, will cause vulnerabilities.

cros\_gralloc\_driver::retain is the entry of handle importing, after review the code, I found below problems:  

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/platform/minigbm/cros_gralloc/cros_gralloc_driver.cc;drc=3940cbd8833c2334eddddf386c778c513ec299a0;l=345>

Problem 1, doesn't check hnd\_->num\_planes when importing handle, may cause oob access

For example, in cros\_gralloc\_buffer::lock, it will cause oob write / oob read:  

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/platform/minigbm/cros_gralloc/cros_gralloc_buffer.cc;drc=21f9c36f0fc8755ab47751e6253754410c5640ca;l=161>

```
for (uint32_t plane = 0; plane < hnd_->num_planes; plane++)  
	addr[plane] = static_cast<uint8_t \*>(vaddr) + drv_bo_get_plane_offset(bo_, plane);  

```

Problem 2, cros\_gralloc\_convert\_handle doesn't validate the handle from binder is a valid cros\_gralloc\_handle  

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/platform/minigbm/cros_gralloc/cros_gralloc_helpers.cc;drc=29aeabedfa4514dbdec3a27dc8262d6e12589730;l=154>

cros\_gralloc\_handle\_t cros\_gralloc\_convert\_handle(buffer\_handle\_t handle)  

{  

auto hnd = reinterpret\_cast<cros\_gralloc\_handle\_t>(handle); <---------- directly cast to cros\_gralloc\_handle\_t  

if (!hnd || hnd->magic != cros\_gralloc\_magic)  

return nullptr;

```
return hnd;  

```

}

For example, if the numFds and numInts are not match the cros\_gralloc\_handle's numFds and numInts, when using fds of the imported handle, the fd value is not transformed by the binder driver, so can fake arbitrary process's fds to impact files of the process.

I write a sample patch for you to reference:

diff --git a/cros\_gralloc/cros\_gralloc\_helpers.cc b/cros\_gralloc/cros\_gralloc\_helpers.cc  

index 8c86c66..5e887cb 100644  

--- a/cros\_gralloc/cros\_gralloc\_helpers.cc  

+++ b/cros\_gralloc/cros\_gralloc\_helpers.cc  

@@ -153,8 +153,19 @@ uint32\_t cros\_gralloc\_convert\_map\_usage(uint64\_t usage)

cros\_gralloc\_handle\_t cros\_gralloc\_convert\_handle(buffer\_handle\_t handle)  

{

- ```
    if (!handle)  
  
  ```
- ```
            return nullptr;  
  
  ```
- ```
    if (sizeof(native_handle_t) + (sizeof(int) \* (handle->numFds + handle->numInts)) != sizeof(struct cros_gralloc_handle))  
  
  ```
- ```
            return nullptr;  
  
  ```
- ```
    auto hnd = reinterpret_cast<cros_gralloc_handle_t>(handle);  
  
  ```

- ```
    if (!hnd || hnd->magic != cros_gralloc_magic)  
  
  ```

- ```
    if (hnd->magic != cros_gralloc_magic)  
  
  ```
- ```
            return nullptr;  
  
  ```
- ```
    // if hnd->reserved_region_size == 0, numFds is DRV_MAX_FDS - 1  
  
  ```
- ```
    // if hnd->reserved_region_size > 0, numFds is DRV_MAX_FDS  
  
  ```
- ```
    if (hnd->num_planes > DRV_MAX_PLANES || hnd->numFds != (DRV_MAX_FDS - !hnd->reserved_region_size))  
            return nullptr;  
  
    return hnd;  
  
  ```

**CREDIT INFORMATION**

Reporter credit: [lovepink]

## Timeline

### [Deleted User] (2023-06-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-06-28)

setting OS == Chrome so this can be visible in the ChromeOS security queue 
cc'ing leonwinter@ -- current CrOS security sheriff 

### pi...@gmail.com (2023-06-29)

Update the sample patch, by review the handle allocate logic:
https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/platform/minigbm/cros_gralloc/cros_gralloc_driver.cc;drc=3940cbd8833c2334eddddf386c778c513ec299a0;l=266

diff --git a/cros_gralloc/cros_gralloc_helpers.cc b/cros_gralloc/cros_gralloc_helpers.cc
index 8c86c66..ea53640 100644
--- a/cros_gralloc/cros_gralloc_helpers.cc
+++ b/cros_gralloc/cros_gralloc_helpers.cc
@@ -153,8 +153,19 @@ uint32_t cros_gralloc_convert_map_usage(uint64_t usage)

 cros_gralloc_handle_t cros_gralloc_convert_handle(buffer_handle_t handle)
 {
+       if (!handle)
+               return nullptr;
+
+       if (sizeof(native_handle_t) + (sizeof(int) * (handle->numFds + handle->numInts)) != sizeof(struct cros_gralloc_handle))
+               return nullptr;
+
        auto hnd = reinterpret_cast<cros_gralloc_handle_t>(handle);
-       if (!hnd || hnd->magic != cros_gralloc_magic)
+       if (hnd->magic != cros_gralloc_magic)
+               return nullptr;
+
+       // if hnd->reserved_region_size == 0, numFds is num_planes
+       // if hnd->reserved_region_size > 0, numFds is num_planes + 1
+       if (hnd->num_planes > DRV_MAX_PLANES || hnd->numFds != (hnd->num_planes + !!hnd->reserved_region_size))
                return nullptr;

        return hnd;


### ch...@google.com (2023-06-29)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/289303132). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

[Monorail blocking: b/289303132]

### [Deleted User] (2023-07-17)

[Empty comment from Monorail migration]

### ch...@google.com (2023-08-01)

Project: chromiumos/platform/minigbm
Branch: main

commit a13a4ccde31a5bc539ec30c88d7a1fcc3fdc9573
Author: dawnhan <dawnhan@google.com>
Date:   Mon Jul 10 16:13:50 2023

    minigbm: add some validation check in cros_gralloc
   
    1. Check if the buffer handle
       - Validate if the handle is null or not
       - Check the size of the handle to make sure it will not cause oob read/write
    2. Check num_planes to make sure it matches with numFds
    3. Created b/291606090 for the follow up about updating cros_gralloc_driver level api to take cros_gralloc_handle_t
   
    BUG=b:289303132
    TEST=patch the change on rvc-arc and tested with ARCVM
   
    Change-Id: Id03ec45f928fe6db62bb1722ee0dbc6c8831fd46
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/platform/minigbm/+/4674736
    Reviewed-by: Yiwei Zhang <zzyiwei@chromium.org>
    Commit-Queue: Dawn Han <dawnhan@google.com>
    Tested-by: Dawn Han <dawnhan@google.com>

M       cros_gralloc/cros_gralloc_helpers.cc
M       cros_gralloc/gralloc0/gralloc0.cc

https://chromium-review.googlesource.com/4674736
09:14
09:14
CLs: Merged:​<none>      crrev/c/4674736
CLs: Pending:​crrev/c/4674736      <none>

### [Deleted User] (2023-08-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-01)

[Empty comment from Monorail migration]

### st...@google.com (2023-08-29)

[Empty comment from Monorail migration]

### ch...@google.com (2023-09-19)

Exploitability - Explain why/why not the bug is reachable and/or exploitable For example, if a bug mentions a race, details are needed about how easy that race would be to achieve / can the attack retry infinite times to win the race, etc..

The bug requires tricking the user into installing a malicious android app. The app needs to then exploit some file descriptors which may affect other apps or the android framework. There is no evidence of crossing a VM boundary, but this may cause some denial of service in other apps.

Privileges and Capabilities - Identify which process is exploited and where code execution potentially can be achieved if the attacker can break out of that process, and explain why

The ARCVM process can potentially be exploited after the android app install and run. May affect other apps but will not affect anything outside of the VM process.

Origin of fix - Is the issue already known upstream, fixed by work from a previously known or reported issue, provided by the reporter, or any other information that would be relevant toward reward eligibility

The issue is in arcvm code and was fixed.

Mitigations - Detail any regarding mitigation considerations (we're run across a few comments, such as "we considered this issue to be highly mitigated" without explanation)

User needs to be tricked into installing a malicious app. No VM boundary is crossed here.

Severity assessment - why not higher, why not lower

Low Severity - this one is highly limited in scope when combined with user being tricked and no VM boundary being crossed.

Why not Medium Severity? There is no evidence that this can be used in combination of other bugs to cause any harm.

Why not No Severity/ Impact? File Descriptors can potentially leak some information, therefore making it a potential security issue..

### ch...@google.com (2023-09-19)

[Empty comment from Monorail migration]

### pi...@gmail.com (2023-09-19)

I don't agree above assessment.

#14 and #16 both emphasized cross VM boundary or not, I think you don't understand the Android risks, Android VM is like an Android phone, contains many user data and sensitive APPs, like payment app, social media app etc, chromebook android vm will encounter risks which android phones have.

So, please consider, if android SYSTEM privilege compromised, user security will not impacted? User security will get big impact.

I think needs more experienced android security engineer to assess this bug if you still don't understand.

And consider this virt gpu bug, this bug only can possiblely compromise vm kernel to root, also no cross VM boundary: https://bugs.chromium.org/p/chromium/issues/detail?id=1400037 ,

Android SYSTEM privilege is half god of android userspace, one bug impact System privilege in Android VRP usually got High severity, for this bug on chromebook, I only can agree Medium severity.

And, your "Origin of fix" part is not good also, this part means to know if reporter firstly report this bug and trigger the fix.

### am...@chromium.org (2023-09-26)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-05)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-05)

Congratulations lovepink! 
The VRP Panel has decided to award you $1000 for this report. 
A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in discovering and reporting this issue to us -- great work! 
Please be mindful that previous reward decisions made by the Chrome VRP should not be considered precedent for potential future ChromeOS VRP reward amounts or decisions.

### [Deleted User] (2023-10-05)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-11-07)

This issue was migrated from crbug.com/chromium/1458807?no_tracker_redirect=1

[Monorail blocking: b/289303132]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40066572)*
