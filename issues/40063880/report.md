# Security: UAF in sampler_state

| Field | Value |
|-------|-------|
| **Issue ID** | [40063880](https://issues.chromium.org/issues/40063880) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | fi...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-04-03 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**

state will be assigned to sampler\_state in vrend\_bind\_sampler\_states.

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
  
      ctx->sub->sampler_state[shader_type][start_slot + i] = state;             <------ state is assigned to sampler_state  
      ctx->sub->sampler_views_dirty[shader_type] |= (1 << (start_slot + i));  
   }  
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

Lead to dangling pointer in sampler\_state.

**VERSION**

virglrenderer-0.10.4

**REPRODUCTION CASE**

1. Apply the patch diff.txt(which just access sampler\_state, make reproduction easier)
2. Compile tests with -fsanitize=address
3. ./virgl\_fuzzer test

**CREDIT INFORMATION**

Reporter credit: rinngo

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 4.7 KB)
- [diff.txt](attachments/diff.txt) (text/plain, 887 B)
- [test](attachments/test) (text/plain, 81 B)

## Timeline

### [Deleted User] (2023-04-03)

[Empty comment from Monorail migration]

### mp...@chromium.org (2023-04-04)

[Empty comment from Monorail migration]

### st...@google.com (2023-04-04)

[Empty comment from Monorail migration]

### st...@google.com (2023-04-04)

Hi there, 

Thanks for filing this report. We'e created a tracking bug to follow this issue which you can follow along at https://issuetracker.google.com/issues/276905181. Feel free to follow up if you have issues with access.

### ch...@google.com (2023-04-12)

[Empty comment from Monorail migration]

### ch...@google.com (2023-04-24)

[Empty comment from Monorail migration]

[Monorail blocking: b/276905181]

### ch...@google.com (2023-04-24)

Upstream bug filled under:  https://gitlab.freedesktop.org/virgl/virglrenderer/-/issues/327

### ch...@google.com (2023-04-27)

The fix has merged upstream: https://gitlab.freedesktop.org/virgl/virglrenderer/-/merge_requests/1094

crrev/c/4479770 has brought it to CrOS side

### ch...@google.com (2023-04-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-27)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-02)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-02)

Marked as low: 
Low severity vulnerabilities are usually bugs that would normally be a higher severity, but which have extreme mitigating factors or highly limited scope."

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### jo...@chromium.org (2023-05-30)

VM escape is security severity high. Mitigations inside of the VM don't affect severity.

### st...@google.com (2023-06-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-03)

This bug is a regression and does not impact stable or extended stable.Removing incorrectly added Release- labels.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2023-06-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-09)

Congratulations rinngo! The VRP Panel has decided to award you $10,000 for this high quality report. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-06-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-08-03)

This issue was migrated from crbug.com/chromium/1430089?no_tracker_redirect=1

[Monorail blocking: b/276905181]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063880)*
