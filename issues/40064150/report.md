# Security: stack-buffer-overflow in prepare_so_movs

| Field | Value |
|-------|-------|
| **Issue ID** | [40064150](https://issues.chromium.org/issues/40064150) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | fi...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-04-21 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**

register\_index is set in vrend\_decode\_create\_shader with no check.

```
static int vrend_decode_create_shader(struct vrend_context \*ctx,  
                                      const uint32_t \*buf,  
                                      uint32_t handle,  
                                      uint16_t length)  
{  
   struct pipe_stream_output_info so_info;  
   uint i;  
   int ret;  
   uint32_t shader_offset, req_local_mem = 0;  
   unsigned num_tokens, num_so_outputs, offlen;  
   const uint8_t \*shd_text;  
   uint32_t type;  
  
   if (length < VIRGL_OBJ_SHADER_HDR_SIZE(0))  
      return EINVAL;  
  
   type = get_buf_entry(buf, VIRGL_OBJ_SHADER_TYPE);  
   num_tokens = get_buf_entry(buf, VIRGL_OBJ_SHADER_NUM_TOKENS);  
   offlen = get_buf_entry(buf, VIRGL_OBJ_SHADER_OFFSET);  
  
   if (type == PIPE_SHADER_COMPUTE) {  
      req_local_mem = get_buf_entry(buf, VIRGL_OBJ_SHADER_SO_NUM_OUTPUTS);  
      num_so_outputs = 0;  
   } else {  
      num_so_outputs = get_buf_entry(buf, VIRGL_OBJ_SHADER_SO_NUM_OUTPUTS);  
      if (length < VIRGL_OBJ_SHADER_HDR_SIZE(num_so_outputs))  
         return EINVAL;  
  
      if (num_so_outputs > PIPE_MAX_SO_OUTPUTS)  
         return EINVAL;  
   }  
  
   shader_offset = 6;  
   if (num_so_outputs) {  
      so_info.num_outputs = num_so_outputs;  
      if (so_info.num_outputs) {  
         for (i = 0; i < 4; i++)  
            so_info.stride[i] = get_buf_entry(buf, VIRGL_OBJ_SHADER_SO_STRIDE(i));  
         for (i = 0; i < so_info.num_outputs; i++) {  
            uint32_t tmp = get_buf_entry(buf, VIRGL_OBJ_SHADER_SO_OUTPUT0(i));  
  
            so_info.output[i].register_index = tmp & 0xff;     <----- maxium number is 0xff  
            so_info.output[i].start_component = (tmp >> 8) & 0x3;  
            so_info.output[i].num_components = (tmp >> 10) & 0x7;  
            so_info.output[i].output_buffer = (tmp >> 13) & 0x7;  
            so_info.output[i].dst_offset = (tmp >> 16) & 0xffff;  
            tmp = get_buf_entry(buf, VIRGL_OBJ_SHADER_SO_OUTPUT0_SO(i));  
            so_info.output[i].stream = (tmp & 0x3);  
            so_info.output[i].need_temp = so_info.output[i].num_components < 4;  
         }  
  
         for (i = 0; i < so_info.num_outputs - 1; i++) {  
            for (unsigned j = i + 1; j < so_info.num_outputs; j++) {  
               so_info.output[j].need_temp |=  
                     (so_info.output[i].register_index == so_info.output[j].register_index);  
            }  
         }  
      }  
      shader_offset += 4 + (2 \* num_so_outputs);  
   } else  
     memset(&so_info, 0, sizeof(so_info));  
  
   shd_text = get_buf_ptr(buf, shader_offset);  
   ret = vrend_create_shader(ctx, handle, &so_info, req_local_mem, (const char \*)shd_text, offlen, num_tokens, type, length - shader_offset + 1);  
  
   return ret;  
}  

```

output is an array of size 64.

```
static void prepare_so_movs(struct dump_ctx \*ctx)  
{  
   uint32_t i;  
   for (i = 0; i < ctx->so->num_outputs; i++) {  
      ctx->write_so_outputs[i] = true;  
      if (ctx->so->output[i].start_component != 0)  
         continue;  
      if (ctx->so->output[i].num_components != 4)  
         continue;  
      if (ctx->outputs[ctx->so->output[i].register_index].name == TGSI_SEMANTIC_CLIPDIST)    <----- stack buffer overflow  
         continue;  
      if (ctx->outputs[ctx->so->output[i].register_index].name == TGSI_SEMANTIC_POSITION)  
         continue;  
  
      ctx->outputs[ctx->so->output[i].register_index].stream = ctx->so->output[i].stream;  
      if (ctx->prog_type == TGSI_PROCESSOR_GEOMETRY && ctx->so->output[i].stream)  
         ctx->shader_req_bits |= SHADER_REQ_GPU_SHADER5;  
  
      ctx->write_so_outputs[i] = false;  
   }  
}  

```

**VERSION**

virglrenderer-0.10.4

**REPRODUCTION CASE**

1. Compile tests with -fsanitize=address
2. ./virgl\_fuzzer

**CREDIT INFORMATION**

Reporter credit: rinngo

## Attachments

- [test](attachments/test) (text/plain, 684 B)
- deleted (application/octet-stream, 0 B)
- [crash.log](attachments/crash.log) (text/plain, 3.6 KB)

## Timeline

### [Deleted User] (2023-04-21)

[Empty comment from Monorail migration]

### fi...@gmail.com (2023-04-21)

[Empty comment from Monorail migration]

### za...@google.com (2023-04-24)

Stack overflow is not considered a security vulnerability[1], so I am removing the security bug tag. 

However, it might still be a bug, I am looping in graphics/virgl team for visibility. Hi ryanneph@ can you please help triage this bug and feel free to reassign. Thanks. 

[1] https://chromium.googlesource.com/chromium/src/+/main/docs/security/faq.md#are-stack-overflows-considered-security-bugs

[Monorail components: Internals>Preload]

### ry...@google.com (2023-04-24)

Hi zackhan@google.com, can you please migrate this bug to Buganizer, as has been done for previous instances of these types of reports (e.g. b/278654908)?

That ensures we include the issue in our normal triage process and address it ASAP.

### fi...@gmail.com (2023-04-24)

[Comment Deleted]

### fi...@gmail.com (2023-04-24)

> The only exception is if an attacker can jump over the guard pages allocated by the operating system and avoid accessing them

register_index is under control, can be very big. It can override other variables, and I have a heap-use-after-free crash dump caused by it.

### fi...@gmail.com (2023-04-25)

I think there is some misunderstanding here. The bug here is stack buffer overflow, not stack overflow.

https://en.wikipedia.org/wiki/Stack_overflow

https://en.wikipedia.org/wiki/Stack_buffer_overflow

### fi...@gmail.com (2023-04-26)

Hi zackhan@google.com, this should be a security bug. Could you please fowarded it to chmiel?

### fi...@gmail.com (2023-04-27)

Just want to clarify that it would result in an out-of-bounds write here `ctx->outputs[ctx->so->output[i].register_index].stream = ctx->so->output[i].stream;`, not just an out-of-bounds read.

Will this report be worked on in the Buganizer system?

### ch...@google.com (2023-04-27)

[Empty comment from Monorail migration]

[Monorail blocking: b/279896905]
[Monorail components: -Internals>Preload]

### ch...@google.com (2023-04-27)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/279896905). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on.

### ch...@google.com (2023-05-03)

Sorry for coming to this mirror of the issue a bit later. We have, in fact, been tracking this already in a confidential upstream issue: https://gitlab.freedesktop.org/virgl/virglrenderer/-/issues/330 and it has since been fixed upstream and has flowed into ChromeOS with crrev/c/4479770.

I'll mark this as closed and track the M114 backport in b/279784764.

Thanks for the report!

### ch...@google.com (2023-05-03)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-03)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-04)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### jo...@chromium.org (2023-05-30)

[Empty comment from Monorail migration]

### am...@google.com (2023-06-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-16)

Congratulations rinngo! The VRP Panel has decided to award you $7,000 for this virgl memory corruption bug in a sandboxed process. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-06-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-08-09)

This issue was migrated from crbug.com/chromium/1435422?no_tracker_redirect=1

[Monorail blocking: b/279896905]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064150)*
