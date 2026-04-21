# Security: UAF in vrend_renderer_pipe_resource_set_type

| Field | Value |
|-------|-------|
| **Issue ID** | [40063894](https://issues.chromium.org/issues/40063894) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU |
| **Platforms** | ChromeOS |
| **Reporter** | fi...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-04-04 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**

res can be added to ctx->untyped\_resources multiple times by calling vrend\_renderer\_attach\_res\_ctx multiple times.

```
void vrend_renderer_attach_res_ctx(struct vrend_context \*ctx,  
                                   struct virgl_resource \*res)  
{  
   if (!res->pipe_resource) {  
      /\* move the last untyped resource from cache to list \*/  
      if (unlikely(ctx->untyped_resource_cache)) {  
         struct virgl_resource \*last = ctx->untyped_resource_cache;  
         struct vrend_untyped_resource \*wrapper = malloc(sizeof(\*wrapper));  
         if (wrapper) {  
            wrapper->resource = last;  
            list_add(&wrapper->head, &ctx->untyped_resources);    <------ res added to list  
         } else {  
            vrend_printf("dropping attached resource %d due to OOM\n", last->res_id);  
         }  
      }  
  
      ctx->untyped_resource_cache = res;  
      /\* defer to vrend_renderer_pipe_resource_set_type \*/  
      return;  
   }  
  
   vrend_ctx_resource_insert(ctx->res_hash,  
                             res->res_id,  
                             (struct vrend_resource \*)res->pipe_resource);  
}  

```

vrend\_renderer\_detach\_res\_ctx(from virgl\_renderer\_resource\_unref) only unlink the first added res

```
void vrend_renderer_detach_res_ctx(struct vrend_context \*ctx,  
                                   struct virgl_resource \*res)  
{  
   if (!res->pipe_resource) {  
      if (ctx->untyped_resource_cache == res) {  
         ctx->untyped_resource_cache = NULL;  
      } else {  
         struct vrend_untyped_resource \*iter;  
         LIST_FOR_EACH_ENTRY(iter, &ctx->untyped_resources, head) {  
            if (iter->resource == res) {  
               list_del(&iter->head);     <------ only list_del the first added res, then break out  
               free(iter);  
               break;  
            }  
         }  
      }  
  
      return;  
   }  
  
   vrend_ctx_resource_remove(ctx->res_hash, res->res_id);  
}  

```

Lead to dangling pointer in ctx->untyped\_resources, UAF in vrend\_renderer\_pipe\_resource\_set\_type

```
int  
vrend_renderer_pipe_resource_set_type(struct vrend_context \*ctx,  
                                      uint32_t res_id,  
                                      const struct vrend_renderer_resource_set_type_args \*args)  
{  
   struct virgl_resource \*res = NULL;  
  
   /\* look up the untyped resource \*/  
   if (ctx->untyped_resource_cache &&  
       ctx->untyped_resource_cache->res_id == res_id) {  
      res = ctx->untyped_resource_cache;  
      ctx->untyped_resource_cache = NULL;  
   } else {  
      /\* cache miss \*/  
      struct vrend_untyped_resource \*iter;  
      LIST_FOR_EACH_ENTRY(iter, &ctx->untyped_resources, head) {  
         if (iter->resource->res_id == res_id) {      <------ UAF  
            res = iter->resource;  
            list_del(&iter->head);  
            free(iter);  
            break;  
         }  
      }  
   }  
  
   /\* either a bad res_id or the resource is already typed \*/  
   if (!res) {  
      if (vrend_renderer_ctx_res_lookup(ctx, res_id))  
         return 0;  
  
      vrend_report_context_error(ctx, VIRGL_ERROR_CTX_ILLEGAL_RESOURCE, res_id);  
      return EINVAL;  
   }  

```

**VERSION**

virglrenderer-0.10.4

Patch

```
diff --git a/src/vrend_renderer.c b/src/vrend_renderer.c  
index 59238137..6d1d467d 100644  
--- a/src/vrend_renderer.c  
+++ b/src/vrend_renderer.c  
@@ -12023,7 +12023,6 @@ void vrend_renderer_detach_res_ctx(struct vrend_context \*ctx,  
             if (iter->resource == res) {  
                list_del(&iter->head);  
                free(iter);  
-               break;  
             }  
          }  
       }  

```

**REPRODUCTION CASE**

1. Compile the virgl\_fuzzer.c with -fsanitize=address
2. ./virgl\_fuzzer test

**CREDIT INFORMATION**

Reporter credit: rinngo & n3m41ess

## Attachments

- [virgl_fuzzer.c](attachments/virgl_fuzzer.c) (text/plain, 6.9 KB)
- [test](attachments/test) (text/plain, 69 B)
- [asan.log](attachments/asan.log) (text/plain, 5.7 KB)

## Timeline

### [Deleted User] (2023-04-04)

[Empty comment from Monorail migration]

### an...@chromium.org (2023-04-04)

[Empty comment from Monorail migration]

### st...@google.com (2023-04-04)

Hi there, 

Thanks for filing this report. We'e created a tracking bug to follow this issue which you can follow along at https://issuetracker.google.com/issues/276909550. Feel free to follow up if you have issues with access.

### ch...@google.com (2023-04-12)

[Empty comment from Monorail migration]

### ch...@google.com (2023-04-20)

Fix merged upstream yesterday and into ChromeOS this morning with https://chromium-review.googlesource.com/c/chromiumos/overlays/chromiumos-overlay/+/4444021.

Thanks again for the report!

### [Deleted User] (2023-04-20)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-20)

[Empty comment from Monorail migration]

### pa...@chromium.org (2023-04-25)

As in https://bugs.chromium.org/p/chromium/issues/detail?id=1430323, I think this is Medium, too.

[Monorail components: Internals>GPU]

### fi...@gmail.com (2023-04-28)

Could you please tell me why this is noly medium severity? Shouldn't VM escape be high severity?

### ch...@google.com (2023-05-02)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### jo...@chromium.org (2023-05-30)

This allows for escaping the VM so marking as severity high.

### al...@google.com (2023-06-07)

[Empty comment from Monorail migration]

[Monorail blocked-on: b/276909550]

### am...@google.com (2023-06-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-09)

Congratulations on another one! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-06-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-07-27)

This issue was migrated from crbug.com/chromium/1430381?no_tracker_redirect=1

[Monorail blocked-on: b/276909550]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063894)*
