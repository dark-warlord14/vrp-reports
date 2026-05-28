# Security: Heap-use-after-free in ScreenAIService::TriggerProcessingNextTaskInQueue

| Field | Value |
|-------|-------|
| **Issue ID** | [40063799](https://issues.chromium.org/issues/40063799) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | UI>Accessibility, UI>Accessibility>MachineIntelligence |
| **Platforms** | Linux, Windows |
| **Reporter** | me...@gmail.com |
| **Assignee** | rh...@chromium.org |
| **Created** | 2023-03-28 |
| **Bounty** | $11,000.00 |

## Description

**Steps to reproduce the problem:**  

commit at c0af71a4700da1dbf7749d62142ff4c416d027ff

1. apply change.diff and compile chromium with ASAN
2. start a HTTP server at the folder of poc.html
3. run `./chrome --user-data-dir=/tmp/noexist --enable-features=PdfOcr --no-sandbox http://127.0.0.1:8605/poc.html`
4. wait until crash

Note that `--no-sandbox` is used to symbolize the ASAN log.

**Problem Description:**

1. Analysis

In `ScreenAIService::TriggerProcessingNextTaskInQueue`[1], it will use ThreadPool to post a task with `Unretained(this)`, although the comment says that this is safe, but actually this is wrong.  

We could add a delay in the task to easily trigger the UAF cased by deleted of `this`.

```
void ScreenAIService::TriggerProcessingNextTaskInQueue() {  
  if (!library_) {  
    return;  
  }  
  // Sending `this` unretained is safe as `helper_task_runner_` belongs to  
  // `this`.  
  helper_task_runner_->PostTask(  
      FROM_HERE, base::BindOnce(&ScreenAIService::ProcessNextTaskInQueue,  
                                base::Unretained(this)));  
}  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:components/services/screen_ai/screen_ai_service_impl.cc;l=353;bpv=1;bpt=0;drc=c0af71a4700da1dbf7749d62142ff4c416d027ff>

2. Bisect

This UAF is introduce by this commit: c0af71a4700da1dbf7749d62142ff4c416d027ff  

<https://chromium-review.googlesource.com/c/chromium/src/+/4086548>

3. Suggested Patch

I think you should make `ScreenAIService::ProcessNextTaskInQueue` be a static function to avoid this UAF

**Additional Comments:**

\*\*Chrome version: \*\* \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [change.txt](attachments/change.txt) (text/plain, 530 B)
- [asan.txt](attachments/asan.txt) (text/plain, 27.7 KB)
- [poc.html](attachments/poc.html) (text/plain, 835 B)
- deleted (application/octet-stream, 0 B)
- [copy_mojo_js_bindings.py](attachments/copy_mojo_js_bindings.py) (text/plain, 514 B)

## Timeline

### [Deleted User] (2023-03-28)

[Empty comment from Monorail migration]

### me...@gmail.com (2023-03-28)

Update the step: 


1. apply change.diff and compile chromium with ASAN 
2. copy the mojoJS file: `python copy_mojo_js_bindings.py /path/to/chromium/gen/`
3. start a HTTP server at the folder of poc.html and mojoJS 
4. run `./chrome --user-data-dir=/tmp/noexist --enable-blink-features=MojoJS --enable-features=PdfOcr --no-sandbox http://127.0.0.1:8605/poc.html`
5. wait until crash



upload  the attachments


### me...@gmail.com (2023-03-28)

Python script used to copy mojoJS file.

It seems that this screen Ai function needs to download some library, if you can't repro, please retry and check your network.

### mp...@chromium.org (2023-03-29)

rhalavati@ please take a look. I haven't yet reproduced this but I'm pretty sure it's a real UAF and so you may want to get started on a fix. In the meantime can you advise on where ScreenAI is enabled (i.e. is it running in experiments, can it be enabled via prefs or settings?)?

I think this is likely triggerable from a normal, uncompromised renderer which would make this critical severity.

The suggested patch probably won't work, but you can probably just switch back to WeakPtr.

### [Deleted User] (2023-03-29)

[Empty comment from Monorail migration]

### mp...@chromium.org (2023-03-29)

[Empty comment from Monorail migration]

[Monorail components: UI>Accessibility UI>Accessibility>MachineIntelligence]

### rh...@chromium.org (2023-03-29)

[Empty comment from Monorail migration]

### rh...@chromium.org (2023-03-29)

PDF OCR does not have any enabled experiment yet, but main content extraction feature has an experiment running in 50% Canary and Dev.

Should I revert the CL in case I don't find a quick fix?

### gi...@appspot.gserviceaccount.com (2023-03-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b446c02c9e94e0ee0c891b234815b3b761f135ca

commit b446c02c9e94e0ee0c891b234815b3b761f135ca
Author: Ramin Halavati <rhalavati@chromium.org>
Date: Wed Mar 29 15:36:36 2023

Revert "Add task cancellation function to Screen AI service."

This reverts commit c0af71a4700da1dbf7749d62142ff4c416d027ff.

Reason for revert: crbug.com/1428440

Original change's description:
> Add task cancellation function to Screen AI service.
>
> A new function is added to make it possible to request cancelation of
> all queued Main Content Extraction requests.
> Also Main Content Extraction request function is updated to return a
> 'status' that indicates whether the request is processed without any
> problem or failed or canceled.
>
> AX-Relnotes: n/a
> Bug: 1278249
> Change-Id: Iee067670bc11d50678acb48bd476d3f83226ddc0
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4086548
> Reviewed-by: Alex Gough <ajgo@chromium.org>
> Commit-Queue: Ramin Halavati <rhalavati@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1122265}

Bug: 1278249,1428440
Change-Id: I1b712d67cb489ac9fc5ce12783aad1fa1ca18923
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4381724
Commit-Queue: Ramin Halavati <rhalavati@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Reviewed-by: Will Harris <wfh@chromium.org>
Reviewed-by: Abigail Klein <abigailbklein@google.com>
Cr-Commit-Position: refs/heads/main@{#1123607}

[modify] https://crrev.com/b446c02c9e94e0ee0c891b234815b3b761f135ca/components/services/screen_ai/screen_ai_library_wrapper.cc
[modify] https://crrev.com/b446c02c9e94e0ee0c891b234815b3b761f135ca/components/services/screen_ai/BUILD.gn
[modify] https://crrev.com/b446c02c9e94e0ee0c891b234815b3b761f135ca/components/services/screen_ai/screen_ai_service_impl.cc
[modify] https://crrev.com/b446c02c9e94e0ee0c891b234815b3b761f135ca/components/services/screen_ai/public/mojom/screen_ai_service.mojom
[modify] https://crrev.com/b446c02c9e94e0ee0c891b234815b3b761f135ca/chrome/renderer/accessibility/ax_tree_distiller.cc
[modify] https://crrev.com/b446c02c9e94e0ee0c891b234815b3b761f135ca/components/services/screen_ai/screen_ai_library_wrapper.h
[delete] https://crrev.com/97b49f0c42b2121a72a504ad9f39d53920eddb56/components/services/screen_ai/tasks_queue.h
[modify] https://crrev.com/b446c02c9e94e0ee0c891b234815b3b761f135ca/components/services/screen_ai/screen_ai_service_impl.h
[modify] https://crrev.com/b446c02c9e94e0ee0c891b234815b3b761f135ca/components/services/screen_ai/screen_ai_service_impl_unittest.cc
[modify] https://crrev.com/b446c02c9e94e0ee0c891b234815b3b761f135ca/chrome/renderer/accessibility/ax_tree_distiller.h
[modify] https://crrev.com/b446c02c9e94e0ee0c891b234815b3b761f135ca/chrome/renderer/accessibility/read_anything_app_controller.cc
[delete] https://crrev.com/97b49f0c42b2121a72a504ad9f39d53920eddb56/components/services/screen_ai/tasks_queue.cc


### rh...@chromium.org (2023-03-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-29)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rh...@chromium.org (2023-03-29)

Reverted as I couldn't make the WeakPtr work with two task sequencers, and the issue had to be fixed fast.


### aj...@google.com (2023-03-29)

Marking Fixed as the security issue is now resolved - further work can happen on another issue.

### aj...@google.com (2023-03-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-30)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-04)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2023-04-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-04-13)

Congratulations on another one, Krace! The VRP Panel has decided to award you $10,000 for this report + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us -- great work! 

### am...@google.com (2023-04-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-27)

Not requesting merge to dev (M114) because latest trunk commit (1122265) appears to be prior to dev branch point (1135570). If this is incorrect, please replace the Merge-NA-114 label with Merge-Request-114. If other changes are required to fix this bug completely, please request a merge if necessary.

Merge review required: a reverted commit was detected after the merge request.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-04-27)

revert allowing this issue to be considered fixed was landed on 114, same as regression was introduced, no merge needed here 

### [Deleted User] (2023-07-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@alesandroortiz.com (2023-07-06)

Can the attachments please be restored? Curious how the PoC works.

### wx...@gmail.com (2023-07-06)

优秀👍👍

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1428440?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Accessibility, UI>Accessibility>MachineIntelligence]
[Monorail components added to Component Tags custom field.]

### ni...@google.com (2024-06-11)

marking verrified per comment 24

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063799)*
