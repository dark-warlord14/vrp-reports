# Security: heap-use-after-free in vrend_set_uniform_buffer

| Field | Value |
|-------|-------|
| **Issue ID** | [40064227](https://issues.chromium.org/issues/40064227) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | fi...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-04-25 |
| **Bounty** | $5,000.00 |

## Description

Similar to [crbug.com/1433506](https://crbug.com/1433506), heap-use-after-free in vrend\_set\_uniform\_buffer

```
void vrend_set_uniform_buffer(struct vrend_context \*ctx,  
                              uint32_t shader,  
                              uint32_t index,  
                              uint32_t offset,  
                              uint32_t length,  
                              uint32_t res_handle)  
{  
   struct vrend_resource \*res;  
  
   struct pipe_constant_buffer \*cbs = &ctx->sub->cbs[shader][index];  
   const uint32_t mask = 1u << index;  
  
   if (res_handle) {  
      res = vrend_renderer_ctx_res_lookup(ctx, res_handle);  
  
      if (!res) {  
         vrend_report_context_error(ctx, VIRGL_ERROR_CTX_ILLEGAL_RESOURCE, res_handle);  
         return;  
      }  
      cbs->buffer = (struct pipe_resource \*)res;	<----- should use vrend_resource_reference  
      cbs->buffer_offset = offset;  
      cbs->buffer_size = length;  
      ctx->sub->const_bufs_used_mask[shader] |= mask;  
   } else {  
      cbs->buffer = NULL;  
      cbs->buffer_offset = 0;  
      cbs->buffer_size = 0;  
      ctx->sub->const_bufs_used_mask[shader] &= ~mask;  
   }  
   ctx->sub->const_bufs_dirty[shader] |= mask;  
}  

```

**VERSION**

virglrenderer-0.10.4  

ChromeOS: 112.0.5615.134

**CREDIT INFORMATION**

Reporter credit: rinngo

## Timeline

### [Deleted User] (2023-04-25)

[Empty comment from Monorail migration]

### ad...@google.com (2023-04-26)

[Empty comment from Monorail migration]

### ch...@google.com (2023-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-26)

[Empty comment from Monorail migration]

### ch...@google.com (2023-04-26)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/279717160). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on.

[Monorail blocking: b/279717160]

### [Deleted User] (2023-04-26)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-09)

The change has flown to ChromeOS side via https://chromium-review.googlesource.com/c/chromiumos/overlays/chromiumos-overlay/+/4506977, and landed in virglrenderer-0.8.2-r211.ebuild.

Backport cl for fixing the bug: crrev/c/4511774

### [Deleted User] (2023-05-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-09)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### jo...@chromium.org (2023-05-30)

[Empty comment from Monorail migration]

### am...@google.com (2023-06-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-09)

Congratulations once again, rinngo! The VRP Panel has decided to award you $5,000 for this report. The reward amount based on the lack of stack trace and some of the evidence to help demonstrate the security issue being reported as expected for reports of baseline quality. Thank you for your efforts and reporting this issue to us!

### am...@google.com (2023-06-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-08-15)

This issue was migrated from crbug.com/chromium/1440005?no_tracker_redirect=1

[Monorail blocking: b/279717160]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064227)*
