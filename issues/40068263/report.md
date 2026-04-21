# Security: heap-use-after-free in vkr_context_submit_fence

| Field | Value |
|-------|-------|
| **Issue ID** | [40068263](https://issues.chromium.org/issues/40068263) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | fi...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-07-28 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**

The vulnerability exists in the venus implementation of virglrenderer, which serves as the vulkan backend of crosvm and can be used to escape the vm through this.

Call vkr\_dispatch\_vkGetDeviceQueue2 multiple times with different ringIdx. ctx->sync\_queues[1]=ctx->sync\_queues[2]=queue.

```
static void  
vkr_dispatch_vkGetDeviceQueue2(struct vn_dispatch_context \*dispatch,  
                               struct vn_command_vkGetDeviceQueue2 \*args)  
{  
   struct vkr_context \*ctx = dispatch->data;  
  
   struct vkr_device \*dev = vkr_device_from_handle(args->device);  
  
   struct vkr_queue \*queue = vkr_device_lookup_queue(dev, args->pQueueInfo->flags,  
                                                     args->pQueueInfo->queueFamilyIndex,  
                                                     args->pQueueInfo->queueIndex);  
   if (!queue) {  
      vkr_context_set_fatal(ctx);  
      return;  
   }  
  
   const VkDeviceQueueTimelineInfoMESA \*timeline_info = vkr_find_struct(  
      args->pQueueInfo->pNext, VK_STRUCTURE_TYPE_DEVICE_QUEUE_TIMELINE_INFO_MESA);  
   if (timeline_info) {  
      if (timeline_info->ringIdx == 0 ||  
          timeline_info->ringIdx >= ARRAY_SIZE(ctx->sync_queues)) {  
         vkr_log("invalid ring_idx %d", timeline_info->ringIdx);  
         vkr_context_set_fatal(ctx);  
         return;  
      }  
  
      if (ctx->sync_queues[timeline_info->ringIdx]) {  
         vkr_log("sync_queue %d already bound", timeline_info->ringIdx);  
         vkr_context_set_fatal(ctx);  
         return;  
      }  
  
      queue->ring_idx = timeline_info->ringIdx;         <----- queue->ring_idx=1, queue->ring_idx=2  
      ctx->sync_queues[timeline_info->ringIdx] = queue;     <----- ctx->sync_queues[1]=ctx->sync_queues[2]=queue  
   }  
  
   const vkr_object_id id =  
      vkr_cs_handle_load_id((const void \*\*)args->pQueue, VK_OBJECT_TYPE_QUEUE);  
   vkr_queue_assign_object_id(ctx, queue, id);  
}  

```

When destroy queue, it will only set ctx->sync\_queues[2]=NULL

```
void  
vkr_queue_destroy(struct vkr_context \*ctx, struct vkr_queue \*queue)  
{  
   vkr_queue_sync_thread_fini(queue);  
  
   list_del(&queue->base.track_head);  
  
   mtx_destroy(&queue->vk_mutex);  
  
   if (queue->ring_idx > 0)  
      ctx->sync_queues[queue->ring_idx] = NULL;   <----- queue->ring_idx=2, ctx->sync_queues[2]=NULL, dangling pointer in ctx->sync_queues[1]  
  
   if (queue->base.id)  
      vkr_context_remove_object(ctx, &queue->base);  
   else  
      free(queue);  
}  

```

**VERSION**  

Operating System: Chromebook, ChromeOS 113.0.5672.134  

Component: virglrenderer used in crosvm

IMPACT  

Prerequisite: Run as guest app in guest vm  

Impact: heap-use-after-free in virgl\_render\_server

**REPRODUCTION CASE**

1. Start termia with vulkan enable via command: vmc start --enable-gpu --enable-vulkan termina
2. Copy & Compile the poc.c in termina
3. Run the poc

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: virgl\_render\_server  

Crash State: heap-use-after-free

**CREDIT INFORMATION**  

Reporter credit: rinngo

## Attachments

- [poc.c](attachments/poc.c) (text/plain, 6.1 KB)
- [asan.dump](attachments/asan.dump) (application/octet-stream, 4.1 KB)

## Timeline

### [Deleted User] (2023-07-28)

[Empty comment from Monorail migration]

### th...@chromium.org (2023-07-28)

[Empty comment from Monorail migration]

### fi...@gmail.com (2023-07-29)

[Empty comment from Monorail migration]

### ch...@google.com (2023-07-31)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/293819003). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

[Monorail blocking: b/293819003]

### [Deleted User] (2023-07-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-31)

[Empty comment from Monorail migration]

### ch...@google.com (2023-08-17)

Marked as fixed.
Closing because fix landed in crrev/c/4766168.

### [Deleted User] (2023-08-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-17)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-09-26)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-26)

Congratulations! 
The VRP Panel has decided to award you $2000 for this report. 
A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in discovering and reporting this issue to us -- great work! 
Please be mindful that previous reward decisions made by the Chrome VRP should not be considered precedent for potential future ChromeOS VRP reward amounts or decisions.

### ch...@google.com (2023-10-26)

[Empty comment from Monorail migration]

### fi...@gmail.com (2023-10-26)

Why this High Severity only gets reward 2000?

### ch...@google.com (2023-10-26)

Please follow up in https://issuetracker.google.com/issues/293819003

### am...@google.com (2023-10-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-11-23)

This issue was migrated from crbug.com/chromium/1468442?no_tracker_redirect=1

[Monorail blocking: b/293819003]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40068263)*
