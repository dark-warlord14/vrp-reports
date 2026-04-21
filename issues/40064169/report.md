# Security: out-of-bounds access in tgsi_scan_shader

| Field | Value |
|-------|-------|
| **Issue ID** | [40064169](https://issues.chromium.org/issues/40064169) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | fi...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-04-23 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**

out-of-bounds access in tgsi\_scan\_shader.

```
if (fullinst->Instruction.Opcode == TGSI_OPCODE_INTERP_CENTROID ||  
                fullinst->Instruction.Opcode == TGSI_OPCODE_INTERP_OFFSET ||  
                fullinst->Instruction.Opcode == TGSI_OPCODE_INTERP_SAMPLE) {  
               const struct tgsi_full_src_register \*src0 = &fullinst->Src[0];  
               unsigned input;  
  
               if (src0->Register.Indirect && src0->Indirect.ArrayID)  
                  input = info->input_array_first[src0->Indirect.ArrayID];  
               else  
                  input = src0->Register.Index;  
  
               /\* For the INTERP opcodes, the interpolation is always  
                \* PERSPECTIVE unless LINEAR is specified.  
                \*/  
               switch (info->input_interpolate[input]) {    <----- input is very big, with no check  
               case TGSI_INTERPOLATE_COLOR:  
               case TGSI_INTERPOLATE_CONSTANT:  
               case TGSI_INTERPOLATE_PERSPECTIVE:  

```

**VERSION**

virglrenderer: virglrenderer-0.10.4  

ChromeOS: 112.0.5615.134

**REPRODUCTION CASE**

1. Compile the tests with -fsanitize=address
2. ./virgl\_fuzzer test

**CREDIT INFORMATION**

Reporter credit: rinngo

## Attachments

- [crash.txt](attachments/crash.txt) (text/plain, 2.8 KB)
- [test](attachments/test) (text/plain, 616 B)
- [log](attachments/log) (text/plain, 3.0 KB)
- [test](attachments/test) (text/plain, 616 B)

## Timeline

### [Deleted User] (2023-04-23)

[Empty comment from Monorail migration]

### za...@google.com (2023-04-24)

Hi chmiel@, this is a similar out of bounds issue, can you please take a look, thanks! 

### za...@google.com (2023-04-24)

[Empty comment from Monorail migration]

### za...@google.com (2023-04-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-25)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fi...@gmail.com (2023-04-27)

Any updates on this? Will this report be worked on in the Buganizer system?

### ch...@google.com (2023-04-27)

So sorry for the delay and many thanks for the heads-up! 

Your report will be worked on in the Buganizer system ( link: https://issuetracker.google.com/issues/279888165 ). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on.

[Monorail blocking: b/279888165]

### [Deleted User] (2023-05-06)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-09)

Fixed by https://gitlab.freedesktop.org/virgl/virglrenderer/-/merge_requests/1105 a day ago and it has flown to ChromeOS side via https://chromium-review.googlesource.com/c/chromiumos/overlays/chromiumos-overlay/+/4502435, and landed in virglrenderer-0.8.2-r210.ebuild.

Backport cl for fixing the bug: crrev/c/4511774

### [Deleted User] (2023-05-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-09)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-23)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-23)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M113. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M114. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [113, 114].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-05-25)

Hello, rinngo. Thank you for this report. Based on the information provided, this issue appears to result in an oob read that result in only functional implications and does not appear to result in any security consequences. If can demonstrate security implications for this issue, we'd be happy to reconsider and reassess for a potential VRP reward. 

### [Deleted User] (2023-05-26)

This is sufficiently serious that it should be merged to other stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M113. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M114. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M115. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [113, 114, 115].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-27)

This is sufficiently serious that it should be merged to other stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M113. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M114. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M115. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [113, 114, 115].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-28)

This is sufficiently serious that it should be merged to other stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M113. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M114. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M115. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [113, 114, 115].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fi...@gmail.com (2023-05-29)

const struct tgsi_full_src_register *src0 = &fullinst->Src[0];
unsigned input;

if (src0->Register.Indirect && src0->Indirect.ArrayID)
   input = info->input_array_first[src0->Indirect.ArrayID];
else
   input = src0->Register.Index;         <----- input comes from src0->Register.Index

for (i = 0; i < fullinst->Instruction.NumSrcRegs; i++) {
   const struct tgsi_full_src_register *src =
      &fullinst->Src[i];
   int ind = src->Register.Index;        <----- ind also comes from src0->Register.Index

   /* Mark which inputs are effectively used */
   if (src->Register.File == TGSI_FILE_INPUT) {
      unsigned usage_mask;
      usage_mask = tgsi_util_get_inst_usage_mask(fullinst, i);
      if (src->Register.Indirect) {
         for (ind = 0; ind < info->num_inputs; ++ind) {
            info->input_usage_mask[ind] |= usage_mask;
         }
      } else {
         assert(ind >= 0);
         assert(ind < PIPE_MAX_SHADER_INPUTS);
         info->input_usage_mask[ind] |= usage_mask;       <----- oob write


git checkout c94ac5bd2a23, and after limiting the range of input (to avoid reporting ASAN in advance), you can see that oob write is triggered.
switch (info->input_interpolate[input & 0]) {


### [Deleted User] (2023-05-29)

This is sufficiently serious that it should be merged to other stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M113. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M114. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M115. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [113, 114, 115].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-30)

This is sufficiently serious that it should be merged to other stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M113. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M114. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M115. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [113, 114, 115].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dg...@google.com (2023-05-30)

 chmiel@ - does this issue need to be merged to other milestones? If yes, will those be handled in b/ ?

### am...@chromium.org (2023-06-01)

[Empty comment from Monorail migration]

### am...@google.com (2023-06-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-01)

Thank you for providing additional analysis and demonstration in https://crbug.com/chromium/1436049#c20, rinngo! The Chrome VRP Panel has decided to award you $7,000 for this report. Thank you for your effort and reporting this issue to us! 

### am...@google.com (2023-06-02)

[Empty comment from Monorail migration]

### dg...@google.com (2023-06-12)

Already backported to M115 here:  b/279888165

### [Deleted User] (2023-08-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1436049?no_tracker_redirect=1

[Monorail blocking: b/279888165]

### am...@chromium.org (2024-02-04)

[post-migration issue tracker security validation] removing old merge review/approval labels for old, migrated ChromeOS issues to remove them from the Chrome security merge review queue in the interim of these issues being moved to the appropriate ChromeOS Google issue tracker component

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064169)*
