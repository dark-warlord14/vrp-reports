# Security: OOB read in TGSI_OPCODE_EMIT

| Field | Value |
|-------|-------|
| **Issue ID** | [40070037](https://issues.chromium.org/issues/40070037) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | ph...@gmail.com |
| **Assignee** | st...@google.com |
| **Created** | 2023-08-20 |
| **Bounty** | $1,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

OOB read in TGSI\_OPCODE\_EMIT.  

In parse\_register\_bracket

```
   else {  
      if (!parse_int( &ctx->cur, &index )) {  
         report_error( ctx, "Expected literal integer" );  
         return FALSE;  
      }  
      brackets->index = index;       <-----  index is controlable and can be big value   
      brackets->ind_file = TGSI_FILE_NULL;  
      brackets->ind_index = 0;  
   }  

```

After that in iter\_instruction

```
case TGSI_OPCODE_EMIT: {  
      struct immed \*imd = &ctx->imm[(inst->Src[0].Register.Index)];   <----- OOB here  
      if (ctx->so && ctx->key->gs_present)  
         emit_so_movs(ctx, &ctx->glsl_strbufs, &ctx->has_clipvertex_so);  
      if (ctx->cfg->has_cull_distance && ctx->key->gs.emit_clip_distance)  
         emit_clip_dist_movs(ctx, &ctx->glsl_strbufs);  
      emit_prescale(&ctx->glsl_strbufs);  
      if (imd->val[inst->Src[0].Register.SwizzleX].ui > 0) {  
         ctx->shader_req_bits |= SHADER_REQ_GPU_SHADER5;  
         emit_buff(&ctx->glsl_strbufs, "EmitStreamVertex(%d);\n", imd->val[inst->Src[0].Register.SwizzleX].ui);  
      } else  
         emit_buf(&ctx->glsl_strbufs, "EmitVertex();\n");  
      break;  
   }  

```

Backtrace

```
./tests/fuzzer/virgl_fuzzer ~/cmin  
INFO: Running with entropic power schedule (0xFF, 100).  
INFO: Seed: 2972891151  
INFO: Loaded 1 modules   (29 inline 8-bit counters): 29 [0x55acf0e01058, 0x55acf0e01075),  
INFO: Loaded 1 PC tables (29 PCs): 29 [0x55acf0e01078,0x55acf0e01248),  
./tests/fuzzer/virgl_fuzzer: Running 1 inputs 1 time(s) each.  
Running: /home/zx/cmin  
UndefinedBehaviorSanitizer:DEADLYSIGNAL  
==523119==ERROR: UndefinedBehaviorSanitizer: SEGV on unknown address 0x7ffd2c845c30 (pc 0x7ff7b7b8a301 bp 0x7ffd2c811020 sp 0x7ffd2c8104b0 T523119)  
==523119==The signal is caused by a READ memory access.  
    #0 0x7ff7b7b8a301 in iter_instruction /home/zx/w/gg/virgl/build/../src/vrend_shader.c:5940:55  
    #1 0x7ff7b7bbc548 in tgsi_iterate_shader /home/zx/w/gg/virgl/build/../src/gallium/auxiliary/tgsi/tgsi_iterate.c:54:18  
    #2 0x7ff7b7b86618 in vrend_convert_shader /home/zx/w/gg/virgl/build/../src/vrend_shader.c:8143:11  
    #3 0x7ff7b7b7f695 in vrend_shader_create /home/zx/w/gg/virgl/build/../src/vrend_renderer.c:4263:18  
    #4 0x7ff7b7b69c0e in vrend_shader_select /home/zx/w/gg/virgl/build/../src/vrend_renderer.c:4313:11  
    #5 0x7ff7b7b64314 in vrend_finish_shader /home/zx/w/gg/virgl/build/../src/vrend_renderer.c:4356:11  
    #6 0x7ff7b7b64114 in vrend_create_shader /home/zx/w/gg/virgl/build/../src/vrend_renderer.c:4491:11  
    #7 0x7ff7b7b5dd4d in vrend_decode_create_shader /home/zx/w/gg/virgl/build/../src/vrend_decode.c:129:10  
    #8 0x7ff7b7b59e86 in vrend_decode_create_object /home/zx/w/gg/virgl/build/../src/vrend_decode.c:774:13  
    #9 0x7ff7b7b59bc4 in vrend_decode_ctx_submit_cmd /home/zx/w/gg/virgl/build/../src/vrend_decode.c:1936:13  
    #10 0x7ff7b7b55e53 in virgl_renderer_submit_cmd /home/zx/w/gg/virgl/build/../src/virglrenderer.c:289:11  
    #11 0x55acf0ddd13c in FuzzMode1 /home/zx/w/gg/virgl/build/../tests/fuzzer/virgl_fuzzer.c:227:4  
    #12 0x55acf0ddcfbb in LLVMFuzzerTestOneInput /home/zx/w/gg/virgl/build/../tests/fuzzer/virgl_fuzzer.c:246:4  
    #13 0x55acf0d9a5b3 in fuzzer::Fuzzer::ExecuteCallback(unsigned char const\*, unsigned long) (/home/zx/w/gg/virgl/build/tests/fuzzer/virgl_fuzzer+0x265b3) (BuildId: fb6b532b739232014e7aac2786d4ccf2802d8af8)  
    #14 0x55acf0d8432f in fuzzer::RunOneTest(fuzzer::Fuzzer\*, char const\*, unsigned long) (/home/zx/w/gg/virgl/build/tests/fuzzer/virgl_fuzzer+0x1032f) (BuildId: fb6b532b739232014e7aac2786d4ccf2802d8af8)  
    #15 0x55acf0d8a086 in fuzzer::FuzzerDriver(int\*, char\*\*\*, int (\*)(unsigned char const\*, unsigned long)) (/home/zx/w/gg/virgl/build/tests/fuzzer/virgl_fuzzer+0x16086) (BuildId: fb6b532b739232014e7aac2786d4ccf2802d8af8)  
    #16 0x55acf0db3ea2 in main (/home/zx/w/gg/virgl/build/tests/fuzzer/virgl_fuzzer+0x3fea2) (BuildId: fb6b532b739232014e7aac2786d4ccf2802d8af8)  
    #17 0x7ff7b7629d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16  
    #18 0x7ff7b7629e3f in __libc_start_main csu/../csu/libc-start.c:392:3  
    #19 0x55acf0d7ebf4 in _start (/home/zx/w/gg/virgl/build/tests/fuzzer/virgl_fuzzer+0xabf4) (BuildId: fb6b532b739232014e7aac2786d4ccf2802d8af8)  
  
UndefinedBehaviorSanitizer can not provide additional info.  
SUMMARY: UndefinedBehaviorSanitizer: SEGV /home/zx/w/gg/virgl/build/../src/vrend_shader.c:5940:55 in iter_instruction  
==523119==ABORTING  

```

**VERSION**  

virglrenderer: [HEAD]  

**Operating System: [Please indicate OS, version, and service pack level]**

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug, or any personal or confidential information.**

**Please attach files directly, not in zip or other archive formats, and if**  

**you've created a demonstration site please also attach the files needed to**  

**reproduce the demonstration locally.**

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: [zx]

## Attachments

- [crash](attachments/crash) (text/plain, 216 B)

## Timeline

### [Deleted User] (2023-08-20)

[Empty comment from Monorail migration]

### jd...@chromium.org (2023-08-21)

-> ChromeOS

### st...@google.com (2023-08-23)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/297255937). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

### st...@google.com (2023-08-23)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-24)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-07)

stannor: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-09-15)

CLs: Pending:​crrev/c/4852805, crrev/c/4854626      crrev/c/4854626
Project: chromiumos/overlays/chromiumos-overlay
Branch: release-R118-15604.B

commit 9cf0f5990e78e5d692587a5b3bf9dc0b2230b092
Author: Juston Li <justonli@google.com>
Date:   Fri Sep 08 20:22:50 2023

    virglrenderer: backport fix for shader index
   
       commit d4ed2cf1c9b33f092c08a09e1f47f6cfb8dffe8a
       Author: Gert Wollny <gert.wollny@collabora.com>
       Date:   Tue Sep 5 10:27:31 2023 +0200
   
          shader: check register index when accessing immediate array
   
    BUG=b:297255937, b:299481133
    TEST=sudo emerge-brya virglrenderer
   
    Change-Id: Iaffb3b9491fc840c72b76ff038d9d5e49fdeafb0
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/overlays/chromiumos-overlay/+/4854626
    Reviewed-by: Yiwei Zhang <zzyiwei@chromium.org>
    Commit-Queue: Juston Li <justonli@google.com>
    Tested-by: Juston Li <justonli@google.com>

A       media-libs/virglrenderer/files/0005-UPSTREAM-shader-check-register-index-when-accessing-.patch
M       media-libs/virglrenderer/virglrenderer-0.8.2-r246.ebuild
M       media-libs/virglrenderer/virglrenderer-9999.ebuild

https://chromium-review.googlesource.com/4854626
19:11
19:11
CLs: Merged:​<none>      crrev/c/4854626
CLs: Pending:​crrev/c/4854626      <none>




Exploitability - Reporter ran virgl_fuzzer and uploaded the bactrace to show the crash.
Privileges and Capabilities - No VM escape.
Origin of fix - This is initially reported by the reporter of this bug. No fix suggested by the reporter.
Mitigations - VM escapes are low possibility so this is considered highly mitigated.
Severity assessment - Heap OOB read in the crosvm. Not higher because there isn't any VM escape.

### [Deleted User] (2023-09-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-15)

[Empty comment from Monorail migration]

### ch...@google.com (2023-09-19)

[Empty comment from Monorail migration]

[Monorail blocking: b/297255937]

### ch...@google.com (2023-09-19)

Exploitability - Reporter ran virgl_fuzzer and uploaded the bactrace to show the crash.
Privileges and Capabilities - No VM escape.
Origin of fix - This is initially reported by the reporter of this bug. No fix suggested by the reporter.
Mitigations - VM escapes are low possibility so this is considered highly mitigated.
Severity assessment - Heap OOB read in the crosvm. Not higher because there isn't any VM escape.

### am...@chromium.org (2023-09-26)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-05)

Congratulations zx! 
The VRP Panel has decided to award you $1000 for this report. 
A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in discovering and reporting this issue to us -- great work! 
Please be mindful that previous reward decisions made by the Chrome VRP should not be considered precedent for potential future ChromeOS VRP reward amounts or decisions.

### ch...@google.com (2023-10-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-10)

This bug is a regression and does not impact stable or extended stable.Removing incorrectly added Release- labels.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-12-22)

This issue was migrated from crbug.com/chromium/1474235?no_tracker_redirect=1

[Monorail blocking: b/297255937]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40070037)*
