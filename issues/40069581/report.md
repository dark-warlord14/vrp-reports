# Security: heap-use-after-free in vkr_ring_start

| Field | Value |
|-------|-------|
| **Issue ID** | [40069581](https://issues.chromium.org/issues/40069581) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | fi...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-08-15 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

```
static void  
vkr_dispatch_vkCreateRingMESA(struct vn_dispatch_context \*dispatch,  
                              struct vn_command_vkCreateRingMESA \*args)  
{  
   struct vkr_context \*ctx = dispatch->data;  
   const VkRingCreateInfoMESA \*info = args->pCreateInfo;  
  
   const struct vkr_resource \*res = vkr_context_get_resource(ctx, info->resourceId);  
   if (!res) {  
      vkr_context_set_fatal(ctx);  
      return;  
   }  
  
   struct vkr_ring_layout layout;  
   if (!vkr_ring_layout_init(&layout, res, info)) {  
      vkr_log("vkCreateRingMESA supplied with invalid buffer layout parameters");  
      vkr_context_set_fatal(ctx);  
      return;  
   }  
  
   struct vkr_ring \*ring = vkr_ring_create(&layout, ctx, info->idleTimeout);  
   if (!ring) {  
      vkr_context_set_fatal(ctx);  
      return;  
   }  
  
   ring->id = args->ring;  
  
   mtx_lock(&ctx->ring_mutex);  
   list_addtail(&ring->head, &ctx->rings);	<----- ring could be found, after it has been added to list  
   mtx_unlock(&ctx->ring_mutex);  
   const VkRingMonitorInfoMESA \*monitor_info =  
      vkr_find_struct(info->pNext, VK_STRUCTURE_TYPE_RING_MONITOR_INFO_MESA);  
   if (monitor_info) {  
      if (!monitor_info->maxReportingPeriodMicroseconds) {  
         vkr_log("invalid ring reporting period");  
         vkr_context_set_fatal(ctx);  
         return;  
      }  
  
      /\* Start the ring monitoring thread or update the reporting rate of the running  
       \* thread to the smallest maxReportingPeriodMicroseconds recieved so far, and wake  
       \* it to begin reporting at the faster rate before the first driver check occurs.  
       \*/  
      if (!ctx->ring_monitor.started) {  
         if (!vkr_context_ring_monitor_init(  
                ctx, monitor_info->maxReportingPeriodMicroseconds)) {  
            vkr_context_set_fatal(ctx);  
            return;  
         }  
      } else if (monitor_info->maxReportingPeriodMicroseconds <  
                 ctx->ring_monitor.report_period_us) {  
         mtx_lock(&ctx->ring_monitor.mutex);  
         ctx->ring_monitor.report_period_us =  
            monitor_info->maxReportingPeriodMicroseconds;  
         cnd_signal(&ctx->ring_monitor.cond);  
         mtx_unlock(&ctx->ring_monitor.mutex);  
      }  
  
      ring->monitor = true;  
   }  
  
   vkr_ring_start(ring);		<----- start a new thread, there is a race between here and list_addtail to free the ring.  
}  

```

**VERSION**  

Operating System: Chromebook, ChromeOS 113.0.5672.134  

Component: virglrenderer used in crosvm

IMPACT  

Prerequisite: Run as guest app in guest vm  

Impact: heap-use-after-free in virgl\_render\_server

**REPRODUCTION CASE**  

apply the patch to extend time window, and rebuild virgl.

diff --git a/src/venus/vkr\_transport.c b/src/venus/vkr\_transport.c  

index 89a45e49..eb0f0322 100644  

--- a/src/venus/vkr\_transport.c  

+++ b/src/venus/vkr\_transport.c  

@@ -244,7 +244,7 @@ vkr\_dispatch\_vkCreateRingMESA(struct vn\_dispatch\_context \*dispatch,

```
   ring->monitor = true;  
}  

```


- sleep(1);  
  
  vkr\_ring\_start(ring);  
  
  }

1. Start termia with vulkan enable via command: vmc start --enable-gpu --enable-vulkan termina
2. Copy & Compile the poc.c in termina
3. Run the poc

PATCH

diff --git a/src/venus/vkr\_transport.c b/src/venus/vkr\_transport.c  

index 89a45e49..733d4ff4 100644  

--- a/src/venus/vkr\_transport.c  

+++ b/src/venus/vkr\_transport.c  

@@ -210,10 +210,6 @@ vkr\_dispatch\_vkCreateRingMESA(struct vn\_dispatch\_context \*dispatch,

```
ring->id = args->ring;  

```

- mtx\_lock(&ctx->ring\_mutex);
- list\_addtail(&ring->head, &ctx->rings);
- mtx\_unlock(&ctx->ring\_mutex);
- const VkRingMonitorInfoMESA \*monitor\_info =  
  
  vkr\_find\_struct(info->pNext, VK\_STRUCTURE\_TYPE\_RING\_MONITOR\_INFO\_MESA);  
  
  if (monitor\_info) {  
  
  @@ -244,8 +240,11 @@ vkr\_dispatch\_vkCreateRingMESA(struct vn\_dispatch\_context \*dispatch,
  
  ```
   ring->monitor = true;  
  
  ```
  
  }
  
  vkr\_ring\_start(ring);


- mtx\_lock(&ctx->ring\_mutex);
- list\_addtail(&ring->head, &ctx->rings);
- mtx\_unlock(&ctx->ring\_mutex);  
  
  }

static void

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: virgl\_render\_server  

Crash State: heap-use-after-free

**CREDIT INFORMATION**  

Reporter credit: rinngo

## Attachments

- [crash.log](attachments/crash.log) (text/plain, 4.7 KB)
- [poc.c](attachments/poc.c) (text/plain, 5.9 KB)

## Timeline

### fi...@gmail.com (2023-08-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-15)

[Empty comment from Monorail migration]

### an...@chromium.org (2023-08-16)

[Empty comment from Monorail migration]

### ch...@google.com (2023-08-16)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/296157063). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

[Monorail blocking: b/296157063]

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### fi...@gmail.com (2023-08-22)

BISECT

The bug was introduced by this commit cf743a06fff3664a97a943e87803706a33fdc901(vkr: split out vkr_transport.[ch])

### ch...@google.com (2023-09-21)

Verified by 

jadmanski@google.com.
Exploitability: PoC supplied which triggers the UaF behavior.

Privileges and Capabilities: Potential for privilege escalation.

Origin of fix: Not known upstream until reported by the reporter. Reporter provided patch.

Mitigations: Not considered mitigated.

Severity assessment: High. There's no immediate demonstration in the PoC that you could promote this into ACE but since this behavior can be externally triggered it is plausible.

### [Deleted User] (2023-09-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-09-26)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-10)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-18)

Congratulations rinngo! 
The VRP Panel has decided to award you $5000 for this report. 
A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in discovering and reporting this issue to us -- great work! 
Please be mindful that previous reward decisions made by the Chrome VRP should not be considered precedent for potential future ChromeOS VRP reward amounts or decisions

### am...@google.com (2023-10-23)

[Empty comment from Monorail migration]

### gm...@google.com (2023-10-25)

[Empty comment from Monorail migration]

### rz...@google.com (2023-10-27)

Fix being evaluated as part of https://chromium-review.googlesource.com/q/topic:%22b-299481133%22

### rz...@google.com (2023-12-18)

All the fixed from above topic landed.

### [Deleted User] (2023-12-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-12-28)

This issue was migrated from crbug.com/chromium/1472943?no_tracker_redirect=1

[Monorail blocking: b/296157063]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40069581)*
