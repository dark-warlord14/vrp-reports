# Security:stack buffer overflow in set_stream_out_varyings

| Field | Value |
|-------|-------|
| **Issue ID** | [40064062](https://issues.chromium.org/issues/40064062) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | fi...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-04-15 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**

varyings is an array with the size of PIPE\_MAX\_SHADER\_OUTPUTS\*2. varyings is continuously written in set\_stream\_out\_varyings without any check, resulting in stack buffer overflow.

```
static void set_stream_out_varyings(ASSERTED struct vrend_sub_context \*sub_ctx,  
                                    int prog_id,  
                                    struct vrend_shader_info \*sinfo)  
{  
   struct pipe_stream_output_info \*so = &sinfo->so_info;  
   char \*varyings[PIPE_MAX_SHADER_OUTPUTS\*2];  
   int j;  
   uint i, n_outputs = 0;  
   int last_buffer = 0;  
   char \*start_skip;  
   int buf_offset = 0;  
   int skip;  
   if (!so->num_outputs)  
      return;  
  
   VREND_DEBUG_EXT(dbg_shader_streamout, sub_ctx->parent, dump_stream_out(so));  
  
   for (i = 0; i < so->num_outputs; i++) {  
      if (last_buffer != so->output[i].output_buffer) {  
  
         skip = so->stride[last_buffer] - buf_offset;  
         while (skip) {  
            start_skip = get_skip_str(&skip);  
            if (start_skip)  
               varyings[n_outputs++] = start_skip;    <----- here  
         }  
         for (j = last_buffer; j < so->output[i].output_buffer; j++)  
            varyings[n_outputs++] = strdup("gl_NextBuffer");  
         last_buffer = so->output[i].output_buffer;  
         buf_offset = 0;  
      }  
  
      skip = so->output[i].dst_offset - buf_offset;  
      while (skip) {  
         start_skip = get_skip_str(&skip);  
         if (start_skip)  
            varyings[n_outputs++] = start_skip;  
      }  
      buf_offset = so->output[i].dst_offset;  
  
      buf_offset += so->output[i].num_components;  
      if (sinfo->so_names[i])  
         varyings[n_outputs++] = strdup(sinfo->so_names[i]);  
   }  
  
   skip = so->stride[last_buffer] - buf_offset;  
   while (skip) {  
      start_skip = get_skip_str(&skip);  
      if (start_skip)  
         varyings[n_outputs++] = start_skip;  
   }  
  
   glTransformFeedbackVaryings(prog_id, n_outputs,  
                               (const GLchar \*\*)varyings, GL_INTERLEAVED_ATTRIBS_EXT);  
  
   for (i = 0; i < n_outputs; i++)  
      if (varyings[i])  
         free(varyings[i]);  
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

- [crash.log](attachments/crash.log) (text/plain, 3.9 KB)
- [test](attachments/test) (text/plain, 112 B)

## Timeline

### [Deleted User] (2023-04-15)

[Empty comment from Monorail migration]

### jd...@chromium.org (2023-04-17)

[Empty comment from Monorail migration]

### ch...@google.com (2023-04-18)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/278656586). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on.

[Monorail blocking: b/278656586]

### ch...@google.com (2023-04-18)

Dear reporter, can you please provide the linked FoundIn ChromeOS Version for this bug?

### ch...@google.com (2023-04-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-18)

[Empty comment from Monorail migration]

### ch...@google.com (2023-04-27)

The fix has landed upstream and should flow into ChromeOS when https://chromium-review.googlesource.com/c/chromiumos/overlays/chromiumos-overlay/+/4465809 merges.

crrev/c/4479770 has brought it to CrOS side. 

### [Deleted User] (2023-04-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-27)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-27)

This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M112. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M113. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M114. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [112, 113, 114].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-28)

This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M112. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M113. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M114. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [112, 113, 114].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-29)

This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M112. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M113. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M114. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [112, 113, 114].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-01)

This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M112. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M113. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M114. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [112, 113, 114].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-02)

Low severity vulnerabilities are usually bugs that would normally be a higher severity, but which have extreme mitigating factors or highly limited scope."

### ch...@google.com (2023-05-03)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-05-05)

this issue is the upstream virgl renderer project, would not receive a chrome release label


### ma...@google.com (2023-05-11)

Per b/278656586 this is not needed in 113.  Dropping labels

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### jo...@chromium.org (2023-05-30)

Per updated guidelines, mitigations inside the VM don't affect severity.

### [Deleted User] (2023-05-30)

LTS Milestone M108

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-05-31)

Hi, I'm checking if the fix should be backmerged to 108-LTS, could I get cc'd on http://b/278656586 to check the CLs?


### st...@google.com (2023-06-02)

[Empty comment from Monorail migration]

### am...@google.com (2023-06-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-09)

Congratulations on yet another one, rinngo! The VRP Panel has decided to award you $7,000 for this report. Thank you for your effort and reporting this issue to us!

### am...@google.com (2023-06-09)

[Empty comment from Monorail migration]

### rz...@google.com (2023-06-15)

The changed code diverged too much and the fixes aren't applicable to 108.

### rz...@google.com (2023-06-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1433468?no_tracker_redirect=1

[Monorail blocking: b/278656586]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064062)*
