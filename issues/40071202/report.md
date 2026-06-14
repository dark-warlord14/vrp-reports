# Security: heap-use-after-free in vrend_destroy_surface

| Field | Value |
|-------|-------|
| **Issue ID** | [40071202](https://issues.chromium.org/issues/40071202) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | fi...@gmail.com |
| **Assignee** | st...@google.com |
| **Created** | 2023-09-02 |
| **Bounty** | $4,000.00 |

## Description

**VULNERABILITY DETAILS**

```
int vrend_create_surface(struct vrend_context \*ctx,  
                         uint32_t handle,  
                         uint32_t res_handle, uint32_t format,  
                         uint32_t val0, uint32_t val1,  
                         uint32_t nr_samples)  
{  
   struct vrend_surface \*surf;  
   struct vrend_resource \*res;  
   uint32_t ret_handle;  
  
   if (format >= PIPE_FORMAT_COUNT) {  
      return EINVAL;  
   }  
  
   res = vrend_renderer_ctx_res_lookup(ctx, res_handle);  
   if (!res) {  
      vrend_report_context_error(ctx, VIRGL_ERROR_CTX_ILLEGAL_RESOURCE, res_handle);  
      return EINVAL;  
   }  
  
   surf = CALLOC_STRUCT(vrend_surface);  
   if (!surf)  
      return ENOMEM;  
  
   surf->res_handle = res_handle;  
   surf->format = format;  
  
   ......   <----- skip  
  
   pipe_reference_init(&surf->reference, 1);  
  
   vrend_resource_reference(&surf->texture, res);           <----- Increase reference count res.base.reference.count  
  
   ret_handle = vrend_renderer_object_insert(ctx, surf, handle, VIRGL_OBJECT_SURFACE);  
   if (ret_handle == 0) {  
      FREE(surf);                <----- Should decrement the reference count res.base.reference.count here, but it doesn't  
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

index 72dab234..ea2a1a15 100644  

--- a/src/vrend\_renderer.c  

+++ b/src/vrend\_renderer.c  

@@ -2341,6 +2341,7 @@ int vrend\_create\_surface(struct vrend\_context \*ctx,

```
ret_handle = vrend_renderer_object_insert(ctx, surf, handle, VIRGL_OBJECT_SURFACE);  
if (ret_handle == 0) {  

```

- ```
   vrend_resource_reference(&surf->texture, NULL);  
   FREE(surf);  
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

another virGL issue, setting OS=Chrome, over to ChromeOS security for triage 

### st...@google.com (2023-09-07)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/299481611). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

### ch...@google.com (2023-09-14)

Exploitability - Fuzzer shows the use-after-free is reachable.

Privileges and Capabilities - No sandbox escape or privilege escalation. Causes process crash.

Origin of fix - The issue is reported by the reporter to ChormeOs and to the upstream. Reporter also suggested a patch.

Mitigations - Use after free in a sandboxed environment

Severity assessment - why not higher : Doesn't escape the sandbox also no code execution, why not lower: remotely exploitable use after free

### [Deleted User] (2023-09-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-14)

[Empty comment from Monorail migration]

### ch...@google.com (2023-09-19)

[Empty comment from Monorail migration]

[Monorail blocking: b/299481611]

### ch...@google.com (2023-09-19)

Exploitability - Fuzzer shows the use-after-free is reachable.

Privileges and Capabilities - No sandbox escape or privilege escalation. Causes process crash.

Origin of fix - The issue is reported by the reporter to ChormeOs and to the upstream. Reporter also suggested a patch.

Mitigations - Use after free in a sandboxed environment

Severity assessment - why not higher : Doesn't escape the sandbox also no code execution, why not lower: remotely exploitable use after free

### am...@chromium.org (2023-09-26)

[Empty comment from Monorail migration]

### ch...@google.com (2023-12-12)

[Empty comment from Monorail migration]

### am...@google.com (2023-12-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-12-21)

This issue was migrated from crbug.com/chromium/1478446?no_tracker_redirect=1

[Monorail blocking: b/299481611]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40071202)*
