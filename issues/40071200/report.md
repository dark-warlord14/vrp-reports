# Security: heap-use-after-free in vrend_destroy_sampler_view

| Field | Value |
|-------|-------|
| **Issue ID** | [40071200](https://issues.chromium.org/issues/40071200) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | fi...@gmail.com |
| **Assignee** | st...@google.com |
| **Created** | 2023-09-02 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

```
int vrend_create_sampler_view(struct vrend_context \*ctx,  
                              uint32_t handle,  
                              uint32_t res_handle, uint32_t format,  
                              uint32_t val0, uint32_t val1, uint32_t swizzle_packed)  
{  
   struct vrend_sampler_view \*view;  
   struct vrend_resource \*res;  
   int ret_handle;  
   enum pipe_swizzle swizzle[4];  
  
   res = vrend_renderer_ctx_res_lookup(ctx, res_handle);  
   if (!res) {  
      vrend_report_context_error(ctx, VIRGL_ERROR_CTX_ILLEGAL_RESOURCE, res_handle);  
      return EINVAL;  
   }  
  
   view = CALLOC_STRUCT(vrend_sampler_view);  
   if (!view)  
      return ENOMEM;  
  
   pipe_reference_init(&view->reference, 1);  
   view->format = format & 0xffffff;  
  
   ......   <----- skip  
  
   vrend_resource_reference(&view->texture, res);       <----- Increase reference count res.base.reference.count  
  
   ......   <----- skip  
  
   ret_handle = vrend_renderer_object_insert(ctx, view, handle, VIRGL_OBJECT_SAMPLER_VIEW);  
   if (ret_handle == 0) {  
      FREE(view);                <----- Should decrement the reference count res.base.reference.count here, but it doesn't  
      return ENOMEM;  
   }  
   return 0;  
}  

```

**VERSION**  

Operating System: Chromebook, ChromeOS 116.0.5845.120  

Component: virglrenderer used in crosvm

IMPACT  

Prerequisite: Run as guest app in guest vm  

Impact: heap-use-after-free in crosvm

BISECT  

The bug was introduced by this commit 03e3116a7513be5ab8256d25fbca2c35ba48c9ae(import latest renderer code)

PATCH  

diff --git a/src/vrend\_renderer.c b/src/vrend\_renderer.c  

index 72dab234..8443daf3 100644  

--- a/src/vrend\_renderer.c  

+++ b/src/vrend\_renderer.c  

@@ -2813,6 +2813,7 @@ int vrend\_create\_sampler\_view(struct vrend\_context \*ctx,

```
ret_handle = vrend_renderer_object_insert(ctx, view, handle, VIRGL_OBJECT_SAMPLER_VIEW);  
if (ret_handle == 0) {  

```

- ```
   vrend_resource_reference(&view->texture, NULL);  
   FREE(view);  
   return ENOMEM;  
  
  ```
  }

**REPRODUCTION CASE**

1. Compile virgl\_fuzzer(x86, 32bit) with assert enbaled(-Db\_ndebug=false), and asan disabled
2. run virgl\_fuzzer

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: crosvm  

Crash State: heap-use-after-free

**CREDIT INFORMATION**  

Reporter credit: rinngo

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 6.4 KB)
- [virgl_fuzzer.c](attachments/virgl_fuzzer.c) (text/plain, 7.5 KB)

## Timeline

### [Deleted User] (2023-09-02)

[Empty comment from Monorail migration]

### fi...@gmail.com (2023-09-02)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-09-05)

setting OS=Chrome, over to ChromeOS security team for triage 

### st...@google.com (2023-09-07)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/299469526). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

### st...@google.com (2023-09-07)

[Empty comment from Monorail migration]

### ch...@google.com (2023-09-18)

[Empty comment from Monorail migration]

[Monorail blocking: b/299469526]

### [Deleted User] (2023-09-21)

stannor: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-06)

stannor: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-10-23)

Verified by 
ChromeOS-security-vm-rotation@google.com.
Exploitability: PoC supplied which triggers the UaF behavior.

Privileges and Capabilities: Potential for privilege escalation.

Origin of fix: Not known upstream until reported by the reporter. Reporter provided patch.

Mitigations: Not considered mitigated.

Severity assessment: High. There's no immediate demonstration in the PoC that you could use as a root chain.

### [Deleted User] (2023-10-23)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-23)

[Empty comment from Monorail migration]

### ch...@google.com (2023-11-30)

[Empty comment from Monorail migration]

### am...@google.com (2023-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-29)

This issue was migrated from crbug.com/chromium/1478443?no_tracker_redirect=1

[Monorail blocking: b/299469526]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40071200)*
