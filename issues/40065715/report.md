# Security: OOB in evdi_gem_fault

| Field | Value |
|-------|-------|
| **Issue ID** | [40065715](https://issues.chromium.org/issues/40065715) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-06-13 |
| **Bounty** | $1,500.00 |

## Description

**VULNERABILITY DETAILS**

Same as <https://labs.bluefrostsecurity.de/blog/cve-2023-2008.html>

[0] page\_offset does not check whether it is larger than obj->size,and will cause OOB [1],which can cause any physical address to read and write.  

This vulnerability seems to be relatively easy to escalate privileges.

vm\_fault\_t evdi\_gem\_fault(struct vm\_fault \*vmf)  

{  

struct vm\_area\_struct \*vma = vmf->vma;  

struct evdi\_gem\_object \*obj = to\_evdi\_bo(vma->vm\_private\_data);  

struct page \*page;  

unsigned int page\_offset;  

int ret = 0;

```
page_offset = (vmf->address - vma->vm_start) >> PAGE_SHIFT; //[0]  

if (!obj->pages)  
	return VM_FAULT_SIGBUS;  

page = obj->pages[page_offset]; //[1]  
ret = vm_insert_page(vma, vmf->address, page);  
switch (ret) {  
case -EAGAIN:  
case 0:  
case -ERESTARTSYS:  
	return VM_FAULT_NOPAGE;  
case -ENOMEM:  
	return VM_FAULT_OOM;  
default:  
	return VM_FAULT_SIGBUS;  
}  
return VM_FAULT_SIGBUS;  

```

}

**VERSION**  

Operating System: ChromiumOS Kernel 5.10,5.15 etc

**REPRODUCTION CASE**  

In construction, it should be relatively easy.

PATCH SUGGESTION

See drm\_gem\_shmem\_fault function code

static vm\_fault\_t drm\_gem\_shmem\_fault(struct vm\_fault \*vmf)  

{  

struct vm\_area\_struct \*vma = vmf->vma;  

struct drm\_gem\_object \*obj = vma->vm\_private\_data;  

struct drm\_gem\_shmem\_object \*shmem = to\_drm\_gem\_shmem\_obj(obj);  

loff\_t num\_pages = obj->size >> PAGE\_SHIFT;  

vm\_fault\_t ret;  

struct page \*page;  

pgoff\_t page\_offset;

```
/\* We don't use vmf->pgoff since that has the fake offset \*/  
page_offset = (vmf->address - vma->vm_start) >> PAGE_SHIFT;  

mutex_lock(&shmem->pages_lock);  

if (page_offset >= num_pages ||  
    WARN_ON_ONCE(!shmem->pages) ||  
    shmem->madv < 0) {  
	ret = VM_FAULT_SIGBUS;  
} else {  
	page = shmem->pages[page_offset];  

	ret = vmf_insert_page(vma, vmf->address, page);  
}  

mutex_unlock(&shmem->pages_lock);  

return ret;  

```

}

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.10/drivers/gpu/drm/drm_gem_shmem_helper.c;l=539>

```
--- a/evdi_gem.c	2023-06-13 15:19:17.179983985 +0800  
+++ b/evdi_gem.c	2023-06-13 15:22:02.646018129 +0800  
@@ -203,13 +203,14 @@  
 	struct vm_area_struct \*vma = vmf->vma;  
 #endif  
 	struct evdi_gem_object \*obj = to_evdi_bo(vma->vm_private_data);  
+	loff_t num_pages = obj->size >> PAGE_SHIFT;  
 	struct page \*page;  
 	unsigned int page_offset;  
 	int ret = 0;  
   
 	page_offset = (vmf->address - vma->vm_start) >> PAGE_SHIFT;  
   
-	if (!obj->pages)  
+	if (!obj->pages || page_offset >= num_pages)  
 		return VM_FAULT_SIGBUS;  
   
 	page = obj->pages[page_offset];  
  
  

```

## Timeline

### [Deleted User] (2023-06-13)

[Empty comment from Monorail migration]

### ha...@gmail.com (2023-06-13)

Patch

```
--- a/evdi_gem.c	2023-06-13 15:19:17.179983985 +0800
+++ b/evdi_gem.c	2023-06-13 15:22:02.646018129 +0800
@@ -203,13 +203,14 @@
 	struct vm_area_struct *vma = vmf->vma;
 #endif
 	struct evdi_gem_object *obj = to_evdi_bo(vma->vm_private_data);
+	loff_t num_pages = obj->base.size >> PAGE_SHIFT;
 	struct page *page;
 	unsigned int page_offset;
 	int ret = 0;
 
 	page_offset = (vmf->address - vma->vm_start) >> PAGE_SHIFT;
 
-	if (!obj->pages)
+	if (!obj->pages || page_offset >= num_pages)
 		return VM_FAULT_SIGBUS;
 
 	page = obj->pages[page_offset];


```

### dc...@chromium.org (2023-06-13)

This looks like a kernel driver, so the CrOS security team should triage this.

### ch...@google.com (2023-06-14)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/287203840). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

[Monorail blocking: b/287203840]

### [Deleted User] (2023-06-14)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-09)

Verified by 
ChromeOS-security-vm-rotation@google.com.
20:53
Status:​Fixed      Verified
Exploitability - Direct array access without a bound check.
Privileges and Capabilities - A page object is retrieved in a potential OOB location and later write into a virtual memory area (vma) through vm_insert_page() call. Escalation of privilege is possible.
Origin of fix - From the reporter.
Mitigations - Added boundary check before read.
Severity assessment - Medium. OOB read and write is of severity High, but since there is no PoC demonstrating the manipulation of function input to cause the OOB read/write. This merits severity Medium - memory corruption and manipulation not exposed through public interface or required other bugs to exploit together.

### [Deleted User] (2023-10-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-09)

[Empty comment from Monorail migration]

### ch...@google.com (2023-11-15)

Congratulations! 
The VRP Panel has decided to award you $1500 for this report. 
A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in discovering and reporting this issue to us -- great work! 
Please be mindful that previous reward decisions made by the Chrome VRP should not be considered precedent for potential future ChromeOS VRP reward amounts or decisions.

### am...@google.com (2023-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-15)

This issue was migrated from crbug.com/chromium/1454371?no_tracker_redirect=1

[Monorail blocking: b/287203840]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065715)*
