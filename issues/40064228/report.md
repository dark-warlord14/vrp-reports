# Security: heap-use-after-free in vrend_set_single_image_view

| Field | Value |
|-------|-------|
| **Issue ID** | [40064228](https://issues.chromium.org/issues/40064228) |
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

**VULNERABILITY DETAILS**

Similar to [crbug.com/1433506](https://crbug.com/1433506), heap-use-after-free in vrend\_set\_single\_image\_view

```
void vrend_set_single_image_view(struct vrend_context \*ctx,  
                                 uint32_t shader_type,  
                                 uint32_t index,  
                                 uint32_t format, uint32_t access,  
                                 uint32_t layer_offset, uint32_t level_size,  
                                 uint32_t handle)  
{  
   struct vrend_image_view \*iview = &ctx->sub->image_views[shader_type][index];  
   struct vrend_resource \*res;  
  
   if (handle) {  
      if (!has_feature(feat_images))  
         return;  
  
      res = vrend_renderer_ctx_res_lookup(ctx, handle);  
      if (!res) {  
         vrend_report_context_error(ctx, VIRGL_ERROR_CTX_ILLEGAL_RESOURCE, handle);  
         return;  
      }  
      iview->texture = res;		<----- should use vrend_resource_reference  
      iview->vformat = format;  
      iview->format = tex_conv_table[format].internalformat;  
      iview->access = access;  
      iview->u.buf.offset = layer_offset;  
      iview->u.buf.size = level_size;  
      ctx->sub->images_used_mask[shader_type] |= (1u << index);  
   } else {  
      iview->texture = NULL;  
      iview->format = 0;  
      ctx->sub->images_used_mask[shader_type] &= ~(1u << index);  
   }  
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

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/279716976). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on.

[Monorail blocking: b/279716976]

### [Deleted User] (2023-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-26)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-10)

Marked as fixed.
Created a b/281583205 for following up adding test cases in our own test suite. We can close this bug for now as it's already fixed.

### [Deleted User] (2023-05-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-10)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### jo...@chromium.org (2023-05-30)

Mitigations inside the VM are not relevant for severity.

### am...@google.com (2023-06-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-09)

Congratulations, rinngo! The VRP Panel has decided to award you $5,000 for this report. The reward amount based on the lack of stack trace and some of the evidence to help demonstrate the security issue being reported as expected for reports of baseline quality. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-06-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-08-16)

This issue was migrated from crbug.com/chromium/1440006?no_tracker_redirect=1

[Monorail blocking: b/279716976]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064228)*
