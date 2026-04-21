# Security: DoS due to check missing

| Field | Value |
|-------|-------|
| **Issue ID** | [40070322](https://issues.chromium.org/issues/40070322) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | bu...@gmail.com |
| **Assignee** | st...@google.com |
| **Created** | 2023-08-23 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

The function `vrend_inject_tcs` can be invoked when injecting a TCS(<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/virglrenderer/src/vrend_renderer.c;l=5406>). Specifically, a new shader is allocated at the point[1]. However, it does not check whether the allocation succeeds. It leads to crash due to NULL-Pointer-Deference. The fuzzer occasionally found this issue.

```
static  
void vrend_inject_tcs(struct vrend_sub_context \*sub_ctx, int vertices_per_patch)  
{  
   struct pipe_stream_output_info so_info;  
  
   memset(&so_info, 0, sizeof(so_info));  
   struct vrend_shader_selector \*sel = vrend_create_shader_state(&so_info,  
                                                                 false, PIPE_SHADER_TESS_CTRL);  
   struct vrend_shader \*shader;  
   shader = CALLOC_STRUCT(vrend_shader); // [1]  
   vrend_fill_shader_key(sub_ctx, sel, &shader->key);  
     
   shader->sel = sel;  
   // ...  

```

**VERSION**

virglrenderer-0.10.4 and all the releases of CrOS are affected.

BISECT

The function is added by this commit(<https://source.chromium.org/chromiumos/_/chromium/chromiumos/third_party/virglrenderer/+/faf23ce917c15bc36d10f76512789edc73893a5e>).

PATCH

I think the following patch can fix the issue:

diff --git a/src/vrend\_renderer.c b/src/vrend\_renderer.c  

index d8ffec8..7a1f0d5 100644  

--- a/src/vrend\_renderer.c  

+++ b/src/vrend\_renderer.c  

@@ -5417,8 +5417,8 @@ static void vrend\_draw\_bind\_objects(struct vrend\_sub\_context \*sub\_ctx, bool new\_  

vrend\_set\_active\_pipeline\_stage(sub\_ctx->prog, PIPE\_SHADER\_FRAGMENT);  

}

-static  

-void vrend\_inject\_tcs(struct vrend\_sub\_context \*sub\_ctx, int vertices\_per\_patch)  

+static bool  

+vrend\_inject\_tcs(struct vrend\_sub\_context \*sub\_ctx, int vertices\_per\_patch)  

{  

struct pipe\_stream\_output\_info so\_info;

@@ -5427,6 +5427,9 @@ void vrend\_inject\_tcs(struct vrend\_sub\_context \*sub\_ctx, int vertices\_per\_patch)  

false, PIPE\_SHADER\_TESS\_CTRL);  

struct vrend\_shader \*shader;  

shader = CALLOC\_STRUCT(vrend\_shader);

- if (!shader) {
- ```
   return false;  
  
  ```
- }  
  
  vrend\_fill\_shader\_key(sub\_ctx, sel, &shader->key);
  
  shader->sel = sel;  
  
  @@ -5441,7 +5444,7 @@ void vrend\_inject\_tcs(struct vrend\_sub\_context \*sub\_ctx, int vertices\_per\_patch)  
  
  FREE(shader);  
  
  vrend\_report\_context\_error(sub\_ctx->parent, VIRGL\_ERROR\_CTX\_ILLEGAL\_SHADER, sel->type);  
  
  vrend\_destroy\_shader\_selector(sel);

- ```
   return;  
  
  ```

- ```
   return false;  
  
  ```
  
  }  
  
  // Need to add inject the selected shader to the shader selector and then the code below  
  
  // can continue  
  
  @@ -5450,6 +5453,7 @@ void vrend\_inject\_tcs(struct vrend\_sub\_context \*sub\_ctx, int vertices\_per\_patch)  
  
  sub\_ctx->shaders[PIPE\_SHADER\_TESS\_CTRL] = sel;
  
  vrend\_compile\_shader(sub\_ctx, shader);
- return true;  
  
  }

@@ -5483,7 +5487,8 @@ vrend\_select\_program(struct vrend\_sub\_context \*sub\_ctx, ubyte vertices\_per\_patch  

vrend\_shader\_select(sub\_ctx, shaders[PIPE\_SHADER\_TESS\_CTRL], &tcs\_dirty);  

else if (vrend\_state.use\_gles && shaders[PIPE\_SHADER\_TESS\_EVAL]) {  

VREND\_DEBUG(dbg\_shader, sub\_ctx->parent, "Need to inject a TCS\n");

- ```
   vrend_inject_tcs(sub_ctx, vertices_per_patch);  
  
  ```

- ```
   if (!vrend_inject_tcs(sub_ctx, vertices_per_patch))  
  
  ```
- ```
      goto fail;  
  
   vrend_shader_select(sub_ctx, shaders[PIPE_SHADER_VERTEX], &vs_dirty);  
  
  ```
  }  
  
  @@ -5505,7 +5510,8 @@ vrend\_select\_program(struct vrend\_sub\_context \*sub\_ctx, ubyte vertices\_per\_patch  
  
  vrend\_shader\_select(sub\_ctx, shaders[PIPE\_SHADER\_TESS\_CTRL], &tcs\_dirty);  
  
  else if (vrend\_state.use\_gles && shaders[PIPE\_SHADER\_TESS\_EVAL]) {  
  
  VREND\_DEBUG(dbg\_shader, sub\_ctx->parent, "Need to inject a TCS\n");

- ```
   vrend_inject_tcs(sub_ctx, vertices_per_patch);  
  
  ```

- ```
   if (!vrend_inject_tcs(sub_ctx, vertices_per_patch))  
  
  ```
- ```
      goto fail;  
  
  ```
  }  
  
  sub\_ctx->drawing = true;  
  
  vrend\_shader\_select(sub\_ctx, shaders[PIPE\_SHADER\_VERTEX], &vs\_dirty);

## Attachments

- [patch.diff](attachments/patch.diff) (text/plain, 2.7 KB)

## Timeline

### [Deleted User] (2023-08-23)

[Empty comment from Monorail migration]

### hc...@google.com (2023-08-23)

[Empty comment from Monorail migration]

### st...@google.com (2023-08-28)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/297916221). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

### [Deleted User] (2023-08-29)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-12)

stannor: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-09-18)

[Empty comment from Monorail migration]

[Monorail blocking: b/97916221]

### ch...@google.com (2023-09-18)

[Empty comment from Monorail migration]

[Monorail blocking: b/297916221]

### [Deleted User] (2023-09-27)

stannor: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-10-10)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-10)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-10)

Verified by 

jadmanski@google.com.
Exploitability: Crash is triggerable by fuzzer.

Privileges and Capabilities: No sandbox escape or execution, crash-only.

Origin of fix: Not known upstream until reported by the reporter. Reporter provided patch

Mitigations: Crash -> denial-of-service only, which is generally not considered a security vulnerability.

Severity assessment: Low. In general we don't actually considered a crash only bug to be a security bug, but given the ability to trigger a crash across a boundary we can still consider this to be a low one.

### [Deleted User] (2023-10-10)

This bug is a regression and does not impact stable or extended stable.Removing incorrectly added Release- labels.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-10)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-16)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-18)

Congratulations! 
The VRP Panel has decided to award you $500 for this report. 
A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in discovering and reporting this issue to us -- great work! 
Please be mindful that previous reward decisions made by the Chrome VRP should not be considered precedent for potential future ChromeOS VRP reward amounts or decisions

### am...@google.com (2023-10-23)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-16)

This issue was migrated from crbug.com/chromium/1475224?no_tracker_redirect=1

[Monorail blocking: b/297916221]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40070322)*
