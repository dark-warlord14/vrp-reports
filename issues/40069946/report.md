# Security: Heap buffer overflow write due to bound check missing

| Field | Value |
|-------|-------|
| **Issue ID** | [40069946](https://issues.chromium.org/issues/40069946) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | bu...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-08-18 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**

When handling the VIRGL\_CCMD\_GET\_MEMORY\_INFO command, `vrend_renderer_get_meminfo` function will be invoked(<https://source.chromium.org/chromiumos/_/chromium/chromiumos/third_party/virglrenderer/+/master:src/vrend_renderer.c;l=12974>  

). Specifically, it directly assigns `res->iov->iov_base` to `info` without any check at the point[1]. If `res->iov` is a NULL-pointer, it causes the NULL-pointer-Dereference issue. And if `res->iov` is not NULL, it will write the vals to the buffer `iov->base` at the point[2-7]. There is no check whether `res->iov->iov_len` is enough for writing. So Heap buffer Out-of-bound-Write can occur.

```
void vrend_renderer_get_meminfo(struct vrend_context \*ctx, uint32_t res_handle)  
{  
   struct vrend_resource \*res;  
   struct virgl_memory_info \*info;  
  
   res = vrend_renderer_ctx_res_lookup(ctx, res_handle);  
   if (!res) {  
      vrend_report_context_error(ctx, VIRGL_ERROR_CTX_ILLEGAL_RESOURCE, res_handle);  
      return;  
   }  
  
   info = (struct virgl_memory_info \*)res->iov->iov_base; // [1]  
  
   if (has_feature(feat_nvx_gpu_memory_info)) {  
         GLint i;  
         glGetIntegerv(GL_GPU_MEMORY_INFO_DEDICATED_VIDMEM_NVX, &i);  
         info->total_device_memory = i; // [2]  
         glGetIntegerv(GL_GPU_MEMORY_INFO_TOTAL_AVAILABLE_MEMORY_NVX, &i);  
         info->total_staging_memory = i - info->total_device_memory; // [3]  
         glGetIntegerv(GL_GPU_MEMORY_INFO_EVICTION_COUNT_NVX, &i);  
         info->nr_device_memory_evictions = i; // [4]  
         glGetIntegerv(GL_GPU_MEMORY_INFO_EVICTED_MEMORY_NVX, &i);  
         info->device_memory_evicted = i; // [5]  
      }  
  
   if (has_feature(feat_ati_meminfo)) {  
      GLint i[4];  
      glGetIntegerv(GL_VBO_FREE_MEMORY_ATI, i);  
      info->avail_device_memory = i[0];  // [6]  
      info->avail_staging_memory = i[2]; // [7]  
   }  
}  

```

**VERSION**

virglrenderer-0.10.4 and all the releases of CrOS are affected.

BISECT

<https://source.chromium.org/chromiumos/_/chromium/chromiumos/third_party/virglrenderer/+/f390c4d6733677dc04730c6b2a3216b20ad33d2f>

**REPRODUCTION CASE**

1. Put the test\_oob.c into test/fuzzer, apply the build.diff and build the test
2. Run the test\_oob bin. The ASAN log can be like:

=================================================================  

==205758==ERROR: AddressSanitizer: SEGV on unknown address 0x000000000000 (pc 0x7f5b360c7416 bp 0x000000000539 sp 0x7ffc5e6600f0 T0)  

==205758==The signal is caused by a READ memory access.  

==205758==Hint: address points to the zero page.  

#0 0x7f5b360c7416 in vrend\_renderer\_get\_meminfo (/tmp/virglrenderer/build/tests/fuzzer/../../src/libvirglrenderer.so.1+0x2e416)  

#1 0x7f5b360af902 in vrend\_decode\_get\_memory\_info (/tmp/virglrenderer/build/tests/fuzzer/../../src/libvirglrenderer.so.1+0x16902)  

#2 0x7f5b360adada in vrend\_decode\_ctx\_submit\_cmd (/tmp/virglrenderer/build/tests/fuzzer/../../src/libvirglrenderer.so.1+0x14ada)  

#3 0x4c8954 in main (/tmp/virglrenderer/build/tests/fuzzer/test\_oob+0x4c8954)  

#4 0x7f5b35bde082 in \_\_libc\_start\_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16  

#5 0x41c31d in \_start (/tmp/virglrenderer/build/tests/fuzzer/test\_oob+0x41c31d)

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: SEGV (/tmp/virglrenderer/build/tests/fuzzer/../../src/libvirglrenderer.so.1+0x2e416) in vrend\_renderer\_get\_meminfo  

==205758==ABORTING

PATCH

I think the following patch can fix the issue:

diff --git a/src/vrend\_renderer.c b/src/vrend\_renderer.c  

index d8ffec8..04f25ad 100644  

--- a/src/vrend\_renderer.c  

+++ b/src/vrend\_renderer.c  

@@ -13062,6 +13062,11 @@ void vrend\_renderer\_get\_meminfo(struct vrend\_context \*ctx, uint32\_t res\_handle)  

return;  

}

- if (!res->iov || res->iov->iov\_len < sizeof(struct virgl\_memory\_info)) {
- ```
   vrend_report_context_error(ctx, VIRGL_ERROR_CTX_ILLEGAL_RESOURCE, res_handle);  
  
  ```
- ```
   return;  
  
  ```
- }
- info = (struct virgl\_memory\_info \*)res->iov->iov\_base;

## Attachments

- [build.diff](attachments/build.diff) (text/plain, 559 B)
- [npd_asan.txt](attachments/npd_asan.txt) (text/plain, 1.2 KB)
- [patch.diff](attachments/patch.diff) (text/plain, 514 B)
- [test_oob.c](attachments/test_oob.c) (text/plain, 6.9 KB)

## Timeline

### [Deleted User] (2023-08-18)

[Empty comment from Monorail migration]

### jd...@chromium.org (2023-08-18)

[Empty comment from Monorail migration]

### je...@google.com (2023-08-19)

apology, have an OOF sick situation, so will be slow in response for the next few days.

### je...@google.com (2023-08-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-19)

[Empty comment from Monorail migration]

### st...@google.com (2023-08-23)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/297252189). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

### ch...@google.com (2023-09-15)

CLs: Pending:​crrev/c/4852807, crrev/c/4854628      crrev/c/4854628
Project: chromiumos/overlays/chromiumos-overlay
Branch: release-R118-15604.B

commit 53998bba1cd5622f5b59ae3754821f3e75ee5d5a
Author: Juston Li <justonli@google.com>
Date:   Fri Sep 08 20:27:36 2023

    virglrenderer: backport fix for IOV check
   
       commit b91e7b417672878d4d56dda4aadbd61310a16f2b
       Author: Gert Wollny <gert.wollny@collabora.com>
       Date:   Wed Sep 6 07:37:12 2023 +0200
   
          vrend: check IOV and its size before writing to it
   
    BUG=b:297252189, b:299481133
    TEST=sudo emerge-brya virglrenderer
   
    Change-Id: I6494055cf31231e0fe3a931ad40211dd5dca1ca3
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/overlays/chromiumos-overlay/+/4854628
    Reviewed-by: Yiwei Zhang <zzyiwei@chromium.org>
    Tested-by: Juston Li <justonli@google.com>
    Commit-Queue: Juston Li <justonli@google.com>

A       media-libs/virglrenderer/files/0008-UPSTREAM-vrend-check-IOV-and-its-size-before-writing.patch
M       media-libs/virglrenderer/virglrenderer-0.8.2-r248.ebuild
M       media-libs/virglrenderer/virglrenderer-9999.ebuild

https://chromium-review.googlesource.com/4854628
19:11
19:11
CLs: Merged:​<none>      crrev/c/4854628
CLs: Pending:​crrev/c/4854628      <none>


Exploitability - Reporter ran virgl_fuzzer and uploaded the ASAN trace to show the crash. (No POC showing the OOB write in virglrenderer).
Privileges and Capabilities - No sandbox escape. Exploit targets within the VM
Origin of fix - This is initially reported by the reporter of this bug. Also fixed by the suggested fix by the reporter
Mitigations - VM escapes are low possibility so this is considered highly mitigated.
Severity assessment - Heap OOB write in the crosvm is considered high severity. Not critical because there isn't any VM escape. Not lower because of code execution in the VM.

### [Deleted User] (2023-09-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-15)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-09-26)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-10)

This bug is a regression and does not impact stable or extended stable.Removing incorrectly added Release- labels.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-10-16)

[Empty comment from Monorail migration]

[Monorail blocking: b/297252189]

### ch...@google.com (2023-10-18)

Congratulations! 
The VRP Panel has decided to award you $7000 for this report. 
A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in discovering and reporting this issue to us -- great work! 
Please be mindful that previous reward decisions made by the Chrome VRP should not be considered precedent for potential future ChromeOS VRP reward amounts or decisions

### am...@google.com (2023-10-23)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-12-22)

This issue was migrated from crbug.com/chromium/1473956?no_tracker_redirect=1

[Monorail blocking: b/297252189]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40069946)*
