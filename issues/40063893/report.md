# Security: UAF in vrend_update_stencil_state

| Field | Value |
|-------|-------|
| **Issue ID** | [40063893](https://issues.chromium.org/issues/40063893) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>Internals |
| **Platforms** | ChromeOS |
| **Reporter** | fi...@gmail.com |
| **Assignee** | st...@google.com |
| **Created** | 2023-04-04 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**

state will be assigned to dsa in vrend\_object\_bind\_dsa.

```
void vrend_object_bind_dsa(struct vrend_context \*ctx,  
                           uint32_t handle)  
{  
   struct pipe_depth_stencil_alpha_state \*state;  
  
   if (handle == 0) {  
      memset(&ctx->sub->dsa_state, 0, sizeof(ctx->sub->dsa_state));  
      ctx->sub->dsa = NULL;  
      ctx->sub->stencil_state_dirty = true;  
      ctx->sub->shader_dirty = true;  
      vrend_hw_emit_dsa(ctx);  
      return;  
   }  
  
   state = vrend_object_lookup(ctx->sub->object_hash, handle, VIRGL_OBJECT_DSA);  
   if (!state) {  
      vrend_report_context_error(ctx, VIRGL_ERROR_CTX_ILLEGAL_HANDLE, handle);  
      return;  
   }  
  
   if (ctx->sub->dsa != state) {  
      ctx->sub->stencil_state_dirty = true;  
      ctx->sub->shader_dirty = true;  
   }  
   ctx->sub->dsa_state = \*state;  
   ctx->sub->dsa = state;         <------ state is assigned to dsa  
  
   if (ctx->sub->sysvalue_data.alpha_ref_val != state->alpha.ref_value) {  
      ctx->sub->sysvalue_data.alpha_ref_val = state->alpha.ref_value;  
      ctx->sub->sysvalue_data_cookie++;  
   }  
  
   vrend_hw_emit_dsa(ctx);  
}  
  

```

state can be freed in free\_object(from vrend\_decode\_destroy\_object)

```
static void free_object(void \*value)  
{  
   struct vrend_object \*obj = value;  
  
   if (obj_types[obj->type].unref)  
      obj_types[obj->type].unref(obj->data);  
   else {  
      /\* for objects with no callback just free them \*/  
      free(obj->data);  
   }  
  
   free(obj);           <------ state will be freed  
}  

```

Lead to dangling pointer in dsa. UAF in vrend\_update\_stencil\_state.

```
void vrend_update_stencil_state(struct vrend_sub_context \*sub_ctx)  
{  
   struct pipe_depth_stencil_alpha_state \*state = sub_ctx->dsa;  
   int i;  
   if (!state)  
      return;  
  
   if (!state->stencil[1].enabled) {        <------ UAF  
      if (state->stencil[0].enabled) {  
         vrend_stencil_test_enable(sub_ctx, true);  
  
         glStencilOp(translate_stencil_op(state->stencil[0].fail_op),  
                     translate_stencil_op(state->stencil[0].zfail_op),  
                     translate_stencil_op(state->stencil[0].zpass_op));  
  
         glStencilFunc(GL_NEVER + state->stencil[0].func,  
                       sub_ctx->stencil_refs[0],  
                       state->stencil[0].valuemask);  
         glStencilMask(state->stencil[0].writemask);  
      } else  
         vrend_stencil_test_enable(sub_ctx, false);  
   } else {  
      vrend_stencil_test_enable(sub_ctx, true);  
  
      for (i = 0; i < 2; i++) {  
         GLenum face = (i == 1) ? GL_BACK : GL_FRONT;  
         glStencilOpSeparate(face,  
                             translate_stencil_op(state->stencil[i].fail_op),  
                             translate_stencil_op(state->stencil[i].zfail_op),  
                             translate_stencil_op(state->stencil[i].zpass_op));  
  
         glStencilFuncSeparate(face, GL_NEVER + state->stencil[i].func,  
                               sub_ctx->stencil_refs[i],  
                               state->stencil[i].valuemask);  
         glStencilMaskSeparate(face, state->stencil[i].writemask);  
      }  
   }  
   sub_ctx->stencil_state_dirty = false;  
}  

```

**VERSION**

virglrenderer-0.10.4

**REPRODUCTION CASE**

1. Compile tests with -fsanitize=address
2. ./virgl\_fuzzer test

**CREDIT INFORMATION**

Reporter credit: rinngo

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 4.6 KB)
- [test](attachments/test) (text/plain, 77 B)

## Timeline

### [Deleted User] (2023-04-04)

[Empty comment from Monorail migration]

### mp...@chromium.org (2023-04-04)

[Empty comment from Monorail migration]

### st...@google.com (2023-04-04)

Hi there, 

Thanks for filing this report. We'e created a tracking bug to follow this issue which you can follow along at https://issuetracker.google.com/issues/276905942. Feel free to follow up if you have issues with access.

### ch...@google.com (2023-04-12)

[Empty comment from Monorail migration]

### ch...@google.com (2023-04-21)

A fix has been merged upstream: https://gitlab.freedesktop.org/virgl/virglrenderer/-/merge_requests/1084

I'll close this issue after this flows into ChromeOS with https://chromium-review.googlesource.com/c/chromiumos/overlays/chromiumos-overlay/+/4454009


Marked as fixed.
https://chromium-review.googlesource.com/c/chromiumos/overlays/chromiumos-overlay/+/4454009 has merged.

The fix will be in the next (~1 day) developer build of ChromeOS, and should naturally be included in M114.

### [Deleted User] (2023-04-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-21)

[Empty comment from Monorail migration]

### pa...@chromium.org (2023-04-25)

I agree this is Medium.

[Monorail components: Internals>GPU>Internals]

### fi...@gmail.com (2023-04-26)

[Comment Deleted]

### am...@google.com (2023-04-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-04-28)

Congratulations! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us. 

### fi...@gmail.com (2023-04-28)

Why this only award $7,000? According to the vrp page, VM escape should be $20,000. And could anyone explain why this is only medium severity?

### am...@chromium.org (2023-04-28)

Hello, the VRP rules do not have a reward amount for a VM escape. $20k reward amounts are consistent with a sandbox escape. This vm escape provides movement to a sandboxed process in Chrome OS and an exploit to provide privilege escalation would still be required to allow for any sort of arbitrary code execution on the host. 

### fi...@gmail.com (2023-04-28)

> Escaping the Linux on Chromebooks environment (aka Crostini) to compromise Chrome OS platform components.
Yes, it should be a sandbox escape, shouldn’t this report fit this description? 

https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules#sandbox-escapes

### am...@chromium.org (2023-04-28)

There is no demonstration of compromise of OS platform components such as to directly impact the host. If you can provide that, we would be most interested. This appears to be a bug that could be used in such as chain but does not result in a sandbox escape in and off itself. 

### am...@google.com (2023-04-29)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-07-28)

This issue was migrated from crbug.com/chromium/1430323?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063893)*
