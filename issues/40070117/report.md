# Security: Out-of-Bound Write due to bound check missing

| Field | Value |
|-------|-------|
| **Issue ID** | [40070117](https://issues.chromium.org/issues/40070117) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | bu...@gmail.com |
| **Assignee** | st...@google.com |
| **Created** | 2023-08-21 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

When converting the IR of TGSI, `vrend_convert_shader` function will be invoked(<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/virglrenderer/src/vrend_shader.c;l=8048>). The `iterate_declaration` function is set at the point[1]. Subsequently, the callback funtion is invoked at the point[2].

```
bool vrend_convert_shader(const struct vrend_context \*rctx,  
                          const struct vrend_shader_cfg \*cfg,  
                          const struct tgsi_token \*tokens,  
                          uint32_t req_local_mem,  
                          const struct vrend_shader_key \*key,  
                          struct vrend_shader_info \*sinfo,  
                          struct vrend_variable_shader_info \*var_sinfo,  
                          struct vrend_strarray \*shader)  
{  
   struct dump_ctx ctx;  
   boolean bret;  
  
   memset(&ctx, 0, sizeof(struct dump_ctx));  
   ctx.cfg = cfg;  
  
   /\* First pass to deal with edge cases. \*/  
   ctx.iter.iterate_declaration = iter_decls; // [1]  
   ctx.iter.iterate_instruction = analyze_instruction;  
   ctx.ssbo_first_binding = UINT32_MAX;  
   bret = tgsi_iterate_shader(tokens, &ctx.iter); // [2]  

```

So function `iter_decls`(<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/virglrenderer/src/vrend_shader.c;l=1146>) will be called. Specifically, there is no check at the point[3] and the length of array `inputs` is 64(See the point[4]). So the Out-of-Bound Write can occur at the point[5-7]. Btw, since it's not linear overwrite, it's highly exploitable.

```
struct dump_ctx {  
   struct tgsi_iterate_context iter;  
   const struct vrend_shader_cfg \*cfg;  
   struct tgsi_shader_info info;  
   enum tgsi_processor_type prog_type;  
   int size;  
   struct vrend_glsl_strbufs glsl_strbufs;  
   uint instno;  
  
   struct vrend_strbuf src_bufs[TGSI_FULL_MAX_SRC_REGISTERS];  
   struct vrend_strbuf dst_bufs[TGSI_FULL_MAX_DST_REGISTERS];  
  
   uint64_t interp_input_mask;  
   uint32_t num_inputs;  
   uint32_t attrib_input_mask;  
   struct vrend_shader_io inputs[64]; // [4]  
   uint32_t num_outputs;  
// ...  
  
static boolean  
iter_decls(struct tgsi_iterate_context \*iter,  
           struct tgsi_full_declaration \*decl)  
{  
   struct dump_ctx \*ctx = (struct dump_ctx \*)iter;  
   switch (decl->Declaration.File) {  
   case TGSI_FILE_INPUT:  
      /\* Tag used semantic fog inputs \*/  
      if (decl->Semantic.Name == TGSI_SEMANTIC_FOG) {  
         ctx->fog_input_mask |= (1 << decl->Semantic.Index);  
      }  
  
      if (ctx->prog_type == TGSI_PROCESSOR_FRAGMENT) {  
         for (uint32_t j = 0; j < ctx->num_inputs; j++) {  
            if (ctx->inputs[j].name == decl->Semantic.Name &&  
                ctx->inputs[j].sid == decl->Semantic.Index &&  
                ctx->inputs[j].first == decl->Range.First)  
                  return true;  
         }  
         ctx->inputs[ctx->num_inputs].name = decl->Semantic.Name; // [5]  
         ctx->inputs[ctx->num_inputs].first = decl->Range.First; // [6]  
         ctx->inputs[ctx->num_inputs].last = decl->Range.Last; // [7]  
         ctx->num_inputs++; // [3]  
      }  
      break;  
// ...  

```

**VERSION**

virglrenderer-0.10.4 and all the releases of CrOS are affected.

BISECT

<https://source.chromium.org/chromiumos/_/chromium/chromiumos/third_party/virglrenderer/+/bb76c1aec7e85487a2276014eab07db02c971e23>

**REPRODUCTION CASE**

1. The evil fragment is in the `evil_frag.txt`. Using it to create a shader can trigger the issue.
2. You can use the `log_helper.diff` to identify this issue clearly. The log shoud be like:

```
Bug detect!  
Bug detect!  
Bug detect!  
Bug detect!  
...  

```

PATCH

I think the following patch can fix the issue:

diff --git a/src/vrend\_shader.c b/src/vrend\_shader.c  

index d9d6c85..238882b 100644  

--- a/src/vrend\_shader.c  

+++ b/src/vrend\_shader.c  

@@ -1155,6 +1155,10 @@ iter\_decls(struct tgsi\_iterate\_context \*iter,  

}

```
   if (ctx->prog_type == TGSI_PROCESSOR_FRAGMENT) {  

```

- ```
      if (ctx->num_inputs >= 64) {  
  
  ```
- ```
         return false;  
  
  ```
- ```
      }  
      for (uint32_t j = 0; j < ctx->num_inputs; j++) {  
         if (ctx->inputs[j].name == decl->Semantic.Name &&  
             ctx->inputs[j].sid == decl->Semantic.Index &&  
  
  ```

## Attachments

- [evil_frag.txt](attachments/evil_frag.txt) (text/plain, 3.0 KB)
- [log_helper.diff](attachments/log_helper.diff) (text/plain, 543 B)
- deleted (application/octet-stream, 0 B)
- [patch.diff](attachments/patch.diff) (text/plain, 553 B)

## Timeline

### [Deleted User] (2023-08-21)

[Empty comment from Monorail migration]

### jd...@chromium.org (2023-08-21)

-> ChromeOS

### bu...@gmail.com (2023-08-22)

Sorry, I uploaded the old patch.diff. The correct one is:

diff --git a/src/vrend_shader.c b/src/vrend_shader.c
index d9d6c85..238882b 100644
--- a/src/vrend_shader.c
+++ b/src/vrend_shader.c
@@ -1155,6 +1155,10 @@ iter_decls(struct tgsi_iterate_context *iter,
       }
 
       if (ctx->prog_type == TGSI_PROCESSOR_FRAGMENT) {
+         if (ctx->num_inputs >= ARRAY_SIZE(ctx->inputs)) {
+            return false;
+         }
          for (uint32_t j = 0; j < ctx->num_inputs; j++) {
             if (ctx->inputs[j].name == decl->Semantic.Name &&
                 ctx->inputs[j].sid == decl->Semantic.Index &&


### st...@google.com (2023-08-23)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/297260373). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.


### bu...@gmail.com (2023-08-25)

I got a little confused. Why the Priority of this issue is 3, the other is 1.

### ch...@google.com (2023-09-18)

[Empty comment from Monorail migration]

[Monorail blocking: b/297260373]

### ch...@google.com (2023-10-24)

Verified by 
ChromeOS-security-vm-rotation@google.com.

Exploitability: The bug is using a shader. Does not have an ASAN trace or clear instructions on creating a shader.

Privileges and Capabilities: The out of bounds write is written within the vm but can be used to escape.

Origin of fix: Not known upstream until reported by the reporter

Mitigations: Currently within sandbox, but that is not a mitigation in OOB write.

Severity Assessment: High. Memory corruption that is directly triggerable given the right circumstances. Not critical since this cannot be exploited remotely. Not medium since this can be used for vm escape and is accessible on surface

Note: No ASAN provided or clear instructions for reproducing but if all works as expected this is a high

### [Deleted User] (2023-10-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-24)

[Empty comment from Monorail migration]

### ch...@google.com (2023-12-06)

[Empty comment from Monorail migration]

### am...@google.com (2023-12-08)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-30)

This issue was migrated from crbug.com/chromium/1474415?no_tracker_redirect=1

[Monorail blocking: b/297260373]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40070117)*
