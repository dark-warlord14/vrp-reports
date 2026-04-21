# Security: SEGV on emit_ios_generic_outputs

| Field | Value |
|-------|-------|
| **Issue ID** | [40065011](https://issues.chromium.org/issues/40065011) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | fi...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-05-30 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**

```
static void  
emit_ios_generic_outputs(const struct dump_ctx \*ctx,  
                         struct vrend_glsl_strbufs \*glsl_strbufs,  
                         struct vrend_generic_ios \*generic_ios,  
                         struct vrend_texcoord_ios \*texcoord_ios,  
                         uint8_t front_back_color_emitted_flags[],  
                         bool \*force_color_two_side,  
                         const can_emit_generic_callback can_emit_generic)  
{  
   uint32_t i;  
   uint64_t fc_emitted = 0;  
   uint64_t bc_emitted = 0;  
  
   char buffer[64];  
   struct vrend_strbuf buf;  
   strbuf_alloc_fixed(&buf, buffer, sizeof(buffer));  
  
   for (i = 0; i < ctx->num_outputs; i++) {  
  
      if (!ctx->outputs[i].glsl_predefined_no_emit) {  
         /\* GS stream outputs are handled separately \*/  
         if (!can_emit_generic(&ctx->outputs[i]))  
            continue;  
  
         /\* It is save to use buf here even though it is declared outside the loop, because  
          \* when written it is reset, and the content is used within the iteration \*/  
         const char \*prefix = get_interpolator_prefix(&buf, ctx->cfg, &ctx->outputs[i],  
                                                      &ctx->key->fs_info, ctx->key->flatshade);  
  
         if (ctx->outputs[i].name == TGSI_SEMANTIC_COLOR) {  
            front_back_color_emitted_flags[ctx->outputs[i].sid] |= FRONT_COLOR_EMITTED;  
            fc_emitted |= 1ull << ctx->outputs[i].sid;  
         }  
  
         if (ctx->outputs[i].name == TGSI_SEMANTIC_BCOLOR) {  
            front_back_color_emitted_flags[ctx->outputs[i].sid] |= BACK_COLOR_EMITTED;		<----- sid is under control without check, oob read/write  
            bc_emitted |= 1ull << ctx->outputs[i].sid;  

```

**VERSION**  

Operating System: Chromebook, ChromeOS 113.0.5672.134  

Component: virglrenderer used in crosvm

IMPACT  

Prerequisite: Run as guest app in guest vm  

Impact: Code execution in the virtio-gpu device process of crossvm

**REPRODUCTION CASE**  

Compile virglrenderer with ASAN enable  

./virgl\_fuzzer test

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: virtio-gpu device process  

Crash State: out-of-bounds read/write

**CREDIT INFORMATION**  

Reporter credit: rinngo

## Attachments

- [test](attachments/test) (text/plain, 576 B)
- [dump.log](attachments/dump.log) (text/plain, 1.8 KB)

## Timeline

### fi...@gmail.com (2023-05-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-30)

[Empty comment from Monorail migration]

### ct...@chromium.org (2023-05-31)

Passing to ChromeOS for triage as this looks to be in crosvm.

### st...@google.com (2023-06-01)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/285407579). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

### st...@google.com (2023-06-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-02)

[Empty comment from Monorail migration]

### ch...@google.com (2023-06-12)

[Empty comment from Monorail migration]

[Monorail blocked-on: b/285407579]

### ch...@google.com (2023-06-12)

[Empty comment from Monorail migration]

### ch...@google.com (2023-06-14)

The fix has landed in ChromeOS this morning with https://chromium-review.googlesource.com/c/chromiumos/overlays/chromiumos-overlay/+/4610520.

### [Deleted User] (2023-06-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-14)

[Empty comment from Monorail migration]

### ch...@google.com (2023-08-01)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-18)

Congratulations, rinngo! The VRP Panel has decided to award you $7,000 for this report of a OOB memory access in a sandboxed process. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2023-08-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-09-20)

This issue was migrated from crbug.com/chromium/1449895?no_tracker_redirect=1

[Monorail blocked-on: b/285407579]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065011)*
