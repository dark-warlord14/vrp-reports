# Security:OOB read in vrend_set_single_image_view

| Field | Value |
|-------|-------|
| **Issue ID** | [40064307](https://issues.chromium.org/issues/40064307) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>Internals |
| **Platforms** | ChromeOS |
| **Reporter** | fi...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-05-01 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**

OOB read in vrend\_set\_single\_image\_view.

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
      iview->texture = res;  
      iview->vformat = format;  
      iview->format = tex_conv_table[format].internalformat;	<----- format is under control, can be very big.  
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

virglrenderer: virglrenderer-0.10.4  

ChromeOS: 112.0.5615.134

**REPRODUCTION CASE**

1. Compile the virgl\_fuzzer.c with -fsanitize=address
2. ./virgl\_fuzzer

**CREDIT INFORMATION**

Reporter credit: rinngo

## Attachments

- [virgl_fuzzer.c](attachments/virgl_fuzzer.c) (text/plain, 7.0 KB)

## Timeline

### fi...@gmail.com (2023-05-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-01)

[Empty comment from Monorail migration]

### pg...@google.com (2023-05-01)

[Empty comment from Monorail migration]

### pa...@chromium.org (2023-05-01)

Do you have an AddressSanitizer crash log?

### pa...@chromium.org (2023-05-01)

[Empty comment from Monorail migration]

[Monorail components: Internals>GPU>Internals]

### ry...@chromium.org (2023-05-01)

Thank you for the report.

Security team: Can we please have this migrated to buganizer, where we can track it properly? See b/279716976 for an example.

### ry...@chromium.org (2023-05-01)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-02)

[Empty comment from Monorail migration]

[Monorail blocking: b/280383444]

### ch...@google.com (2023-05-02)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/280383444 ). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on

### [Deleted User] (2023-05-02)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-09)

Fixed by https://gitlab.freedesktop.org/virgl/virglrenderer/-/merge_requests/1106

The change has flown to ChromeOS side via https://chromium-review.googlesource.com/c/chromiumos/overlays/chromiumos-overlay/+/4506977, and landed in virglrenderer-0.8.2-r211.ebuild.

Backport cl for fixing the bug: crrev/c/4511774

### [Deleted User] (2023-05-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-09)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### jo...@chromium.org (2023-05-30)

OOB read is severity medium.

### am...@google.com (2023-06-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-09)

Congratulations, rinngo on yet another one! The VRP Panel has decided to award you $2,000 for this report of an out-of-bounds read / information disclosure. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-06-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-08-15)

This issue was migrated from crbug.com/chromium/1441417?no_tracker_redirect=1

[Monorail blocking: b/280383444]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064307)*
