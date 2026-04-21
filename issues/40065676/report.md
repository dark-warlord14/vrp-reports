# Security: heap-buffer-overflow in vkr_dispatch_vkAllocateMemory

| Field | Value |
|-------|-------|
| **Issue ID** | [40065676](https://issues.chromium.org/issues/40065676) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | fi...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-06-12 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

```
static inline void  
vn_decode_VkMemoryAllocateInfo_self_temp(struct vn_cs_decoder \*dec, VkMemoryAllocateInfo \*val)  
{  
    /\* skip val->{sType,pNext} \*/  
    vn_decode_VkDeviceSize(dec, &val->allocationSize);  
    vn_decode_uint32_t(dec, &val->memoryTypeIndex);            <----- memoryTypeIndex is under contrl with no check  
}  

```
```
static void  
vkr_dispatch_vkAllocateMemory(struct vn_dispatch_context \*dispatch,  
                              struct vn_command_vkAllocateMemory \*args)  
{  
   struct vkr_context \*ctx = dispatch->data;  
   struct vkr_device \*dev = vkr_device_from_handle(args->device);  
   struct vkr_physical_device \*physical_dev = dev->physical_device;  
   VkBaseInStructure \*prev_of_res_info = NULL;  
   VkImportMemoryResourceInfoMESA \*res_info = NULL;  
   VkImportMemoryFdInfoKHR local_import_info = { .fd = -1 };  
   VkExportMemoryAllocateInfo \*export_info = vkr_find_struct(  
      args->pAllocateInfo->pNext, VK_STRUCTURE_TYPE_EXPORT_MEMORY_ALLOCATE_INFO);  
   const bool no_dma_buf_export =  
      !export_info ||  
      !(export_info->handleTypes & VK_EXTERNAL_MEMORY_HANDLE_TYPE_DMA_BUF_BIT_EXT);  
   struct vkr_device_memory \*mem = NULL;  
   const uint32_t mem_type_index = args->pAllocateInfo->memoryTypeIndex;  
   const uint32_t property_flags =  
      physical_dev->memory_properties.memoryTypes[mem_type_index].propertyFlags;        <----- heap-buffer-overflow  
   uint32_t valid_fd_types = 0;  
   struct gbm_bo \*gbm_bo = NULL;  

```

**VERSION**  

Operating System: Chromebook, ChromeOS 113.0.5672.134  

Component: virglrenderer used in crosvm

IMPACT  

Prerequisite: Run as guest app in guest vm  

Impact: heap-buffer-overflow in virgl\_render\_server

**REPRODUCTION CASE**

1. Start termia with vulkan enable via command: vmc start --enable-gpu --enable-vulkan termina
2. Copy & Compile the poc.c in termina
3. Run the poc

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: virgl\_render\_server  

Crash State: heap-buffer-overflow

**CREDIT INFORMATION**  

Reporter credit: rinngo

## Attachments

- [crash.log](attachments/crash.log) (text/plain, 3.3 KB)
- [poc.c](attachments/poc.c) (text/plain, 5.5 KB)

## Timeline

### fi...@gmail.com (2023-06-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-12)

[Empty comment from Monorail migration]

### dc...@chromium.org (2023-06-13)

[Empty comment from Monorail migration]

### ch...@google.com (2023-06-14)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/287203828). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

[Monorail blocking: b/287203828]

### [Deleted User] (2023-06-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-14)

[Empty comment from Monorail migration]

### ch...@google.com (2023-06-15)

Marked as fixed.
Fix has been brought to cros in crrev/c/4617151.

https://gitlab.freedesktop.org/virgl/virglrenderer/-/merge_requests/1161

### [Deleted User] (2023-06-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-15)

[Empty comment from Monorail migration]

### ch...@google.com (2023-08-01)

[Empty comment from Monorail migration]

### ch...@google.com (2023-09-19)

Exploitability - Explain why/why not the bug is reachable and/or exploitable For example, if a bug mentions a race, details are needed about how easy that race would be to achieve / can the attack retry infinite times to win the race, etc..

The bug is the result of unvalidated attacker-controlled values---no race is needed. The attacker needs code execution on the guest OS.

Privileges and Capabilities - Identify which process is exploited and where code execution potentially can be achieved if the attacker can break out of that process, and explain why Origin of fix - Is the issue already known upstream, fixed by work from a previously known or reported issue, provided by the reporter, or any other information that would be relevant toward reward eligibility

The attack starts out in a termina process running on a guest OS and ends up reaching memory corruption bugs in virglrenderer, a host process running in a crosvm virtual-device sandbox.

Mitigations - Detail any regarding mitigation considerations (we're run across a few comments, such as "we considered this issue to be highly mitigated" without explanation)

crosvm device processes run with a fairly restrictive sandbox, but in the virglrenderer case have complete access to guest memory.

EDIT: since this is in venus the mapped memory is limited

Severity assessment - why not higher, why not lower

Severity high because this amounts to a VM escape. We could potentially consider this medium because of the strength of the crosvm device sandbox and this only really being useful as either a privilege escalation inside the guest or in conjunction with other bugs.

This is not a critical severity issue because the attacker already needs to be able to run arbitrary code inside the guest OS (this might also be a good argument to drop this to medium since the attacker would need to either convince the user to cooperate or need another bug; i.e. this doesn't introduce a remote attack vector).

This is not a low severity issue because it is a VM escape and bugs that cross security boundaries are classified as high severity.

### [Deleted User] (2023-09-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-09-26)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-05)

Congratulations rinngo! 
The VRP Panel has decided to award you $1000 for this report. 
A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in discovering and reporting this issue to us -- great work! 
Please be mindful that previous reward decisions made by the Chrome VRP should not be considered precedent for potential future ChromeOS VRP reward amounts or decisions.

### am...@google.com (2023-10-11)

[Empty comment from Monorail migration]

### is...@google.com (2023-10-11)

This issue was migrated from crbug.com/chromium/1454097?no_tracker_redirect=1

[Monorail blocking: b/287203828]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065676)*
