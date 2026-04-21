# Security: heap-use-after-free in vrend_draw_bind_abo_shader

| Field | Value |
|-------|-------|
| **Issue ID** | [40064067](https://issues.chromium.org/issues/40064067) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | fi...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-04-16 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**

res will be assigned to ctx->sub->abo[index]->res in vrend\_set\_single\_abo without taking reference.

```
void vrend_set_single_abo(struct vrend_context \*ctx,  
                          uint32_t index,  
                          uint32_t offset, uint32_t length,  
                          uint32_t handle)  
{  
   struct vrend_abo \*abo = &ctx->sub->abo[index];  
   struct vrend_resource \*res;  
  
   if (!has_feature(feat_atomic_counters))  
      return;  
  
   if (handle) {  
      res = vrend_renderer_ctx_res_lookup(ctx, handle);  
      if (!res) {  
         vrend_report_context_error(ctx, VIRGL_ERROR_CTX_ILLEGAL_RESOURCE, handle);  
         return;  
      }  
      abo->res = res;      <----- here  
      abo->buffer_offset = offset;  
      abo->buffer_size = length;  
      ctx->sub->abo_used_mask |= (1u << index);  
   } else {  
      abo->res = 0;  
      abo->buffer_offset = 0;  
      abo->buffer_size = 0;  
      ctx->sub->abo_used_mask &= ~(1u << index);  
   }  
}  

```

res can be freed by virgl\_renderer\_resource\_unref, resulting in uaf in vrend\_draw\_bind\_abo\_shader

```
static void vrend_draw_bind_abo_shader(struct vrend_sub_context \*sub_ctx)  
{  
   uint32_t mask;  
   struct vrend_abo \*abo;  
   struct vrend_resource \*res;  
   int i;  
  
   if (!has_feature(feat_atomic_counters))  
      return;  
  
   mask = sub_ctx->abo_used_mask;  
   while (mask) {  
      i = u_bit_scan(&mask);  
  
      abo = &sub_ctx->abo[i];  
      res = (struct vrend_resource \*)abo->res;      <----- here  
      glBindBufferRange(GL_ATOMIC_COUNTER_BUFFER, i, res->id,  
                        abo->buffer_offset, abo->buffer_size);  
   }  
}  

```

**VERSION**

virglrenderer-0.10.4

**REPRODUCTION CASE**

1. Compile virgl\_fuzzer.c with -fsanitize=address
2. ./virgl\_fuzzer

**CREDIT INFORMATION**

Reporter credit: rinngo

## Attachments

- [crash.log](attachments/crash.log) (text/plain, 5.9 KB)
- [virgl_fuzzer.c](attachments/virgl_fuzzer.c) (text/plain, 7.8 KB)

## Timeline

### fi...@gmail.com (2023-04-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-16)

[Empty comment from Monorail migration]

### jd...@chromium.org (2023-04-17)

[Empty comment from Monorail migration]

### ch...@google.com (2023-04-18)

Your report will be worked on in the Buganizer system ( link: https://issuetracker.google.com/issues/278654908 ). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on.

[Monorail blocking: b/278654908]

### ch...@google.com (2023-04-18)

Dear reporter, can you please provide the linked FoundIn ChromeOS Version for this bug?

### ch...@google.com (2023-04-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-18)

[Empty comment from Monorail migration]

### ch...@google.com (2023-04-27)

Fix has landed upstream ---> Upstream bug is https://gitlab.freedesktop.org/virgl/virglrenderer/-/issues/326

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

in upstream virgl renderer, does not receive a chrome release label 

### ma...@google.com (2023-05-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-15)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-19)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### jo...@chromium.org (2023-05-30)

Mitigations inside the VM are not considered as part of severity.

### [Deleted User] (2023-05-30)

LTS Milestone M108

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-05-31)

[Empty comment from Monorail migration]

### rz...@google.com (2023-05-31)

Hi, I'm checking if the fix should be backmerged to 108-LTS, could I get cc'd on http://b/278654908 to check the CLs?

### st...@google.com (2023-06-02)

[Empty comment from Monorail migration]

### am...@google.com (2023-06-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-09)

Congratulations again, rinngo! The VRP Panel has decided to award you $7,000 for this report. Thank you for your effort and reporting this issue to us!

### am...@google.com (2023-06-09)

[Empty comment from Monorail migration]

### rz...@google.com (2023-06-15)

The changed code diverged too much and the fixes aren't applicable to 108.

### [Deleted User] (2023-08-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1433506?no_tracker_redirect=1

[Monorail blocking: b/278654908]

### pe...@google.com (2024-10-28)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-11-01)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064067)*
