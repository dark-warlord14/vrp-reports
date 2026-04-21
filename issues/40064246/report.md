# Security: heap-use-after-free in vrend_apply_sampler_state

| Field | Value |
|-------|-------|
| **Issue ID** | [40064246](https://issues.chromium.org/issues/40064246) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | fi...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-04-27 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**

Commit 0ece392fa5ff doesn't really fix the heap-use-after-free bug. It can be easily bypassed.

```
void vrend_bind_sampler_states(struct vrend_context \*ctx,  
                               enum pipe_shader_type shader_type,  
                               uint32_t start_slot,  
                               uint32_t num_states,  
                               const uint32_t \*handles)  
{  
   uint32_t i;  
   struct vrend_sampler_state \*state;  
  
   if (shader_type >= PIPE_SHADER_TYPES) {  
      vrend_report_context_error(ctx, VIRGL_ERROR_CTX_ILLEGAL_CMD_BUFFER, shader_type);  
      return;  
   }  
  
   if (num_states > PIPE_MAX_SAMPLERS ||  
       start_slot > (PIPE_MAX_SAMPLERS - num_states)) {  
      vrend_report_context_error(ctx, VIRGL_ERROR_CTX_ILLEGAL_CMD_BUFFER, num_states);  
      return;  
   }  
  
   ctx->sub->num_sampler_states[shader_type] = num_states;  
  
   for (i = 0; i < num_states; i++) {  
      if (handles[i] == 0)  
         state = NULL;  
      else  
         state = vrend_object_lookup(ctx->sub->object_hash, handles[i], VIRGL_OBJECT_SAMPLER_STATE);  
  
      if (!state && handles[i])  
         vrend_printf("Failed to bind sampler state (handle=%d)\n", handles[i]);  
  
      if (state)  
         state->sub_ctx = ctx->sub;  
      ctx->sub->sampler_state[shader_type][start_slot + i] = state;   <----- this makes the commit invalid  
      ctx->sub->sampler_views_dirty[shader_type] |= (1 << (start_slot + i));  
   }  
}  

```

**VERSION**

virglrenderer: virglrenderer-0.10.4  

ChromeOS: 112.0.5615.134

Patch:

```
diff --git a/src/vrend_renderer.c b/src/vrend_renderer.c  
index e6888c01..84c6053d 100644  
--- a/src/vrend_renderer.c  
+++ b/src/vrend_renderer.c  
@@ -681,8 +681,6 @@ struct vrend_sub_context {  
    uint32_t const_bufs_used_mask[PIPE_SHADER_TYPES];  
    uint32_t const_bufs_dirty[PIPE_SHADER_TYPES];  
   
-   int num_sampler_states[PIPE_SHADER_TYPES];  
-  
    uint32_t sampler_views_dirty[PIPE_SHADER_TYPES];  
    int32_t texture_levels[PIPE_SHADER_TYPES][PIPE_MAX_SAMPLERS];  
    int32_t n_samplers[PIPE_SHADER_TYPES];  
@@ -2404,12 +2402,10 @@ static void vrend_destroy_sampler_state_object(void \*obj_ptr)  
       for (enum pipe_shader_type shader_type = PIPE_SHADER_VERTEX;  
            shader_type < PIPE_SHADER_TYPES;  
            shader_type++) {  
-         uint32_t num_sampler_states = sub_ctx->num_sampler_states[shader_type];  
          bool found = false;  
-         for (uint32_t sampler = 0; sampler < num_sampler_states; sampler++) {  
+         for (uint32_t sampler = 0; sampler < PIPE_MAX_SAMPLERS; sampler++) {  
             if (sub_ctx->sampler_state[shader_type][sampler] == state) {  
                sub_ctx->sampler_state[shader_type][sampler] = NULL;  
-               sub_ctx->num_sampler_states[shader_type]--;  
                sub_ctx->sampler_views_dirty[shader_type] |= (1u << sampler);  
                found = true;  
             } else if (found) {  
@@ -6687,8 +6683,6 @@ void vrend_bind_sampler_states(struct vrend_context \*ctx,  
       return;  
    }  
   
-   ctx->sub->num_sampler_states[shader_type] = num_states;  
-  
    for (i = 0; i < num_states; i++) {  
       if (handles[i] == 0)  
          state = NULL;  

```

**REPRODUCTION CASE**

1. Compile the tests with -fsanitize=address
2. ./virgl\_fuzzer test

**CREDIT INFORMATION**

Reporter credit: rinngo

## Attachments

- [virgl_fuzzer.c](attachments/virgl_fuzzer.c) (text/plain, 7.2 KB)
- [test](attachments/test) (text/plain, 260 B)

## Timeline

### [Deleted User] (2023-04-27)

[Empty comment from Monorail migration]

### ad...@google.com (2023-04-27)

[Empty comment from Monorail migration]

### ch...@google.com (2023-04-27)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/279889570). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on.

[Monorail blocking: b/279889570]

### ch...@google.com (2023-05-09)

Fixed by https://gitlab.freedesktop.org/virgl/virglrenderer/-/merge_requests/1107 

This has been fixed upstream and merged into ChromeOS with crrev/c/4500793

Backport cl for fixing the bug: crrev/c/4511774

### ch...@google.com (2023-05-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-09)

[Empty comment from Monorail migration]

### am...@google.com (2023-05-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-05-18)

Congratulations on another one, rinngo! The VRP Panel has decided to award you $7,000 for this report of a security bug in VirGL renderer which runs in a sandboxed process on ChromeOS. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-05-19)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-05-24)

Hello rinngo, we consider attachments/POCs included with reports to be an integral part of the report (https://g.co/chrome/vrp), so I've undeleted them. Please refrain from deleting them again in the future. Thank you. 

### [Deleted User] (2023-08-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-08-15)

This issue was migrated from crbug.com/chromium/1440653?no_tracker_redirect=1

[Monorail blocking: b/279889570]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064246)*
