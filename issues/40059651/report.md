# AddressSanitizer: heap-use-after-free __memory/unique_ptr.h:312:28 in mojo::Connector::HandleError(b

| Field | Value |
|-------|-------|
| **Issue ID** | [40059651](https://issues.chromium.org/issues/40059651) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>Storage>IndexedDB |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | ar...@chromium.org |
| **Created** | 2022-05-12 |
| **Bounty** | $21,000.00 |

## Description

**Steps to reproduce the problem:**  

The problem was found by my fuzzer running on CF(CC Security team for access permission <https://clusterfuzz.com/testcase-detail/4657073883381760,https://clusterfuzz.com/testcase-detail/6355298952609792>),  

But it cannot be reproduced stably, CF may not automatically report.  

By manual review, it is found that the window time triggered by the vulnerability is very short, so it cannot be reproduced stably.

**Problem Description:**  

Type of crash  

browser process(Sandbox escape)

#Analysis

1. IndexedDBContextImpl has quota\_client\_receiver\_, quota\_client\_receiver\_ constructor and executes on idb\_task\_runner\_(ThreadPoolForeg) thread AT[1]
2. In the function Bind AT[1], StartReceiving will be called, and the callback function will be set when the connection error occurs AT[2]. Although MultiplexRouter is a thread-safe reference count object, but here use of Unretained to pass this causes the reference count not be incremented correctly.
3. QuotaContext destructing will cause IndexedDBContextImpl destructing, which will eventually cause quota\_client\_receiver\_ to be freed as well, causing UAF

```
//content/browser/indexed_db/indexed_db_context_impl.cc:214  
IndexedDBContextImpl::IndexedDBContextImpl(  
    const base::FilePath& base_data_path,  
    scoped_refptr<storage::QuotaManagerProxy> quota_manager_proxy,  
    base::Clock\* clock,  
    mojo::PendingRemote<storage::mojom::BlobStorageContext>  
        blob_storage_context,  
    mojo::PendingRemote<storage::mojom::FileSystemAccessContext>  
  
  // This is safe because the IndexedDBContextImpl must be destructed on the  
  // IDBTaskRunner, and this task will always happen before that.  
  idb_task_runner_->PostTask(  
      FROM_HERE,  
      base::BindOnce(  
          [](mojo::Remote<storage::mojom::BlobStorageContext>\*  
                 blob_storage_context,  
             mojo::Remote<storage::mojom::FileSystemAccessContext>\*  
                 file_system_access_context,  
             mojo::Receiver<storage::mojom::QuotaClient>\* quota_client_receiver,  
             mojo::PendingRemote<storage::mojom::BlobStorageContext>  
                 pending_blob_storage_context,  
             mojo::PendingRemote<storage::mojom::FileSystemAccessContext>  
                 pending_file_system_access_context,  
             mojo::PendingReceiver<storage::mojom::QuotaClient>  
                 quota_client_pending_receiver) {  
            quota_client_receiver->Bind(										<<[1]  
                std::move(quota_client_pending_receiver));  
            if (pending_blob_storage_context) {  
              blob_storage_context->Bind(  
                  std::move(pending_blob_storage_context));  
            }  
            if (pending_file_system_access_context) {  
              file_system_access_context->Bind(  
                  std::move(pending_file_system_access_context));  
            }  
          },  
          &blob_storage_context_, &file_system_access_context_,  
          &quota_client_receiver_, std::move(blob_storage_context),  
          std::move(file_system_access_context),  
          std::move(quota_client_receiver)));  
}  
  
//mojo/public/cpp/bindings/lib/multiplex_router.cc:402  
void MultiplexRouter::StartReceiving() {  
  connector_.set_connection_error_handler(  
      base::BindOnce(&MultiplexRouter::OnPipeConnectionError,  
                     base::Unretained(this), false /\* force_async_dispatch \*/));		<<[2]  
  
  // Always participate in sync handle watching in multi-interface mode,  
  // because even if it doesn't expect sync requests during sync handle  
  // watching, it may still need to dispatch messages to associated endpoints  
  // on a different sequence.  
  const bool allow_woken_up_by_others =  
      config_ == SINGLE_INTERFACE_WITH_SYNC_METHODS ||  
      config_ == MULTI_INTERFACE;  
  
  DETACH_FROM_SEQUENCE(sequence_checker_);  
  connector_.StartReceiving(task_runner_, allow_woken_up_by_others);  
}  
  
//  
QuotaContext::~QuotaContext() {  
  DCHECK_CURRENTLY_ON(BrowserThread::IO);  
}  

```

#Patch  

My fix is to pass this directly  

<https://chromium-review.googlesource.com/c/chromium/src/+/3641789/>

**Additional Comments:**

\*\*Chrome version: \*\* 102.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Windows

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 18.5 KB)
- [asan2.txt](attachments/asan2.txt) (text/plain, 26.6 KB)
- [39aed4b.diff](attachments/39aed4b.diff) (text/plain, 979 B)

## Timeline

### dt...@chromium.org (2022-05-12)

[Empty comment from Monorail migration]

[Monorail components: Blink>Storage>IndexedDB]

### [Deleted User] (2022-05-12)

[Empty comment from Monorail migration]

### wf...@chromium.org (2022-05-12)

Thanks for your report, does this need lsan to reproduce or does it also occur under asan? I can only access test case 6355298952609792 not the other one.

I agree with your analysis, and thank you for your fix.

I'm adding some indexedDB folks. Since this is renderer accessible it looks like a critical. it's not clear to me how QuotaContext gets destructed though and whether this is a shutdown crash or not. Can you provide any further detail on that?

### wf...@chromium.org (2022-05-12)

adding a few more indexeddb owners.

### re...@chromium.org (2022-05-12)

I think the fundamental bug here is that the comment in the IndexedDBContextImpl constructor is incorrect. It says,

  // This is safe because the IndexedDBContextImpl must be destructed on the
  // IDBTaskRunner, and this task will always happen before that.

It is not true that this class will always be destroyed on the IDBTaskRunner thread because since it is a reference counted object, whatever thread owns the last reference is the one where it will be destroyed. There is a DCHECK which asserts this assumption but nothing about the architecture which prevents it.

I think the short-term solution is to modify the callback passed to idb_task_runner_ so it doesn't make assumptions about lifetimes. Longer-term we should migrate away from having objects like IndexedDBContextImpl have ownership passed between threads and instead break it into two objects, each of which are only owned references by a single thread. base::SequenceBound can help with this.

### ar...@chromium.org (2022-05-12)

Got it, I can get a fix in soon

### dm...@chromium.org (2022-05-12)

[Empty comment from Monorail migration]

### ar...@chromium.org (2022-05-12)

Does this look like the fix you were envisioning: https://chromium-review.googlesource.com/c/chromium/src/+/3645544

I'm not sure how to verify; also the fix you linked (https://chromium-review.googlesource.com/c/chromium/src/+/3641789/) is empty

### wf...@chromium.org (2022-05-12)

[Empty comment from Monorail migration]

### wf...@chromium.org (2022-05-12)

This seems to have been around a while. Setting foundin label.

### ar...@chromium.org (2022-05-12)

I should be able to pick this change into M102 without conflict as well

### [Deleted User] (2022-05-12)

[Empty comment from Monorail migration]

### re...@chromium.org (2022-05-12)

I'm adding Ken here because while the code in IndexedDBContextImpl is a problem I want to make sure that there isn't also an issue in MultiplexRouter. I think the base::Unretained() in StartReceiving() is safe and the problem is that because of the IndexedDBContextImpl bug we're in memory corruption territory that just so happens to make MultiplexRouter do something weird.

### re...@chromium.org (2022-05-13)

The change arichiv@ is working on should fix the potential use-after-free in the lambda from the IndexedDBContextImpl constructor but it doesn't fix the actual bug which triggered this by violating the assumption that IndexedDBContextImpl is always destroyed on the IDB sequence. That issue was introduced by https://chromium-review.googlesource.com/c/chromium/src/+/2594289 when we stopped having this class be RefCountedDeleteOnSequence.

Thinking about that, I think I understand why this crash shows up in MultiplexRouter. By having a mojo::Remote or mojo::Receiver which is bound on the IDB thread (by that lamba) but gets destroyed on the main thread (because of the referencing counting issue) we trigger the intentional thread-unsafety inside these Mojo classes which makes that base::Unretained() a safe assumption.

Reporter, does your reproduction case trigger any DCHECKs? We should be catching these broken sequence assumptions in a number of places.

### m....@gmail.com (2022-05-13)

CF does have a check failure case.

CHECK failure
IDBTaskRunner()->RunsTasksInCurrentSequence() in indexed_db_context_impl.cc
content::IndexedDBContextImpl::~IndexedDBContextImpl
content::IndexedDBContextImpl::~IndexedDBContextImpl

### ar...@chromium.org (2022-05-13)

Requesting merge of https://chromium-review.googlesource.com/c/chromium/src/+/3646994 for M102, it's a version of the use-after-free fix in https://chromium-review.googlesource.com/c/chromium/src/+/3645544 (for M103)

### [Deleted User] (2022-05-13)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ar...@chromium.org (2022-05-13)

1) This is a use-after-free security fix. The window in which it can be hit is narrow so this was not previously detected until a report by an outside researcher.
2) https://chromium-review.googlesource.com/c/chromium/src/+/3646994
3) The version of this change for M103 is landing now: https://chromium-review.googlesource.com/c/chromium/src/+/3645544, after the weekend we should know if there are any canary issues (before the M102 stable cut 5/17)
4) No
5) N/A
6) This issue seems to only be reproducible via a fuzzer, and not reliably (see comments by m.cooolie@gmail.com above)

### gi...@appspot.gserviceaccount.com (2022-05-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9d8104567e1ede06e86a7ffe40e5d5bf359ae6d1

commit 9d8104567e1ede06e86a7ffe40e5d5bf359ae6d1
Author: Ari Chivukula <arichiv@chromium.org>
Date: Fri May 13 03:07:20 2022

[IndexedDB] Use-After-Free Fix

We can't guarantee order in the task the constructor dispatches the same
way we could before due to all the async changes. Let's be sure all the
objects exist before using them now. Long term, we need to address
ownership of the idb context.

Bug: 1324864, 1218100
Change-Id: Id5753297a4c966432028a1e7e063c5f1bed6f619
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3645544
Auto-Submit: Ari Chivukula <arichiv@chromium.org>
Quick-Run: Ari Chivukula <arichiv@chromium.org>
Reviewed-by: Ayu Ishii <ayui@chromium.org>
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Commit-Queue: Ari Chivukula <arichiv@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1002978}

[modify] https://crrev.com/9d8104567e1ede06e86a7ffe40e5d5bf359ae6d1/content/browser/indexed_db/indexed_db_context_impl.cc
[modify] https://crrev.com/9d8104567e1ede06e86a7ffe40e5d5bf359ae6d1/content/browser/indexed_db/indexed_db_context_impl.h


### [Deleted User] (2022-05-13)

[Empty comment from Monorail migration]

### ay...@chromium.org (2022-05-13)

[Empty comment from Monorail migration]

### me...@chromium.org (2022-05-13)

I don't think the fix actually fixes the use-after-free? It might make it harder to exploit, but if the assumption that IndexedDBContextImpl is always destroyed on the IDB task runner is violated, that also makes any usage of weak_ptr_factory_ no longer valid as the weak pointers will no longer be destroyed on the IDB task runner either, so it is still possible to have a non-null weak ptr while IndexedDBContextImpl has already been destroyed/is in the process of being destroyed.

### ar...@chromium.org (2022-05-13)

I agree, the change I made just restores the level of correctness from before I migrated storage key to bucket locator. The underlying issue my changes exposed was outlined here: https://bugs.chromium.org/p/chromium/issues/detail?id=1324864#c14

### ar...@chromium.org (2022-05-13)

[Empty comment from Monorail migration]

### ay...@chromium.org (2022-05-13)

While analyzing the stack trace w/ mek, noticed there is something calling a method that ends up calling GetOrCreateBucket with a callback that is bound to the scoped_refptr<IndexedDBContextImpl>. QuotaManager then gets shutdown before the callback is invoked. The suspicion there is that when the callback is not run, the callback is destroyed on the wrong task runner.

Fixing this here https://crrev.com/c/3646864 
Probably will also need to merge request this into 102/103

### gi...@appspot.gserviceaccount.com (2022-05-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c4289d209bb85bf8dccba87386b714f9414bbaea

commit c4289d209bb85bf8dccba87386b714f9414bbaea
Author: Ayu Ishii <ayui@chromium.org>
Date: Fri May 13 22:25:19 2022

Quota: Use BindPostTask in QuotaManagerProxy

This change updates QuotaManagerProxy to use
base::BindPostTask to ensure callbacks are run or
destroyed on the specified task runner. The main difference
between the existing logic is that if the callback
is never run, it may not be destroyed on the correct task
runner. base::BindPostTask makes sure this doesn't happen.

Bug: 1324864
Change-Id: Ifd123031309e29a22761b8aa88ef2a216ad45c70
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3646864
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Commit-Queue: Ayu Ishii <ayui@chromium.org>
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1003354}

[modify] https://crrev.com/c4289d209bb85bf8dccba87386b714f9414bbaea/storage/browser/quota/quota_manager_proxy.cc


### am...@chromium.org (2022-05-14)

Marking this as Fixed based on the secondary CL in https://crbug.com/chromium/1324864#c26.
Thank you for landing this fix so quickly given the severity. For future reference, once the fix is landed resolving the security issue, please update the bug as fixed and refrain from manually requesting merges. Sheriffbot will update with appropriate merge review labels based on when the fix was landed. :) 

Since the fix with the full mitigation just landed, this will need to be reviewed on Monday so there can be sufficient canary coverage and stability check time. M102 stable cut is Tuesday, so as long as there are no issues exhibited from these fixes over the weekend, both fixes should be able to be merged to 102 Monday in time before Tuesday's 102 stable cut. 

Please let me know if there are any issues or concerns. 

### [Deleted User] (2022-05-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-14)

Merge approved: your change passed merge requirements and is auto-approved for M103. Please go ahead and merge the CL to branch 5060 (refs/branch-heads/5060) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-05-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/30be2a150c828d080679f0cbce5fc2a310375688

commit 30be2a150c828d080679f0cbce5fc2a310375688
Author: Ari Chivukula <arichiv@chromium.org>
Date: Sun May 15 02:49:42 2022

{M103 PICK} [IndexedDB] Use-After-Free Fix

We can't guarantee order in the task the constructor dispatches the same
way we could before due to all the async changes. Let's be sure all the
objects exist before using them now. Long term, we need to address
ownership of the idb context.

(cherry picked from commit 9d8104567e1ede06e86a7ffe40e5d5bf359ae6d1)

Bug: 1324864, 1218100
Change-Id: Id5753297a4c966432028a1e7e063c5f1bed6f619
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3645544
Auto-Submit: Ari Chivukula <arichiv@chromium.org>
Quick-Run: Ari Chivukula <arichiv@chromium.org>
Reviewed-by: Ayu Ishii <ayui@chromium.org>
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Commit-Queue: Ari Chivukula <arichiv@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1002978}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3647910
Cr-Commit-Position: refs/branch-heads/5060@{#11}
Cr-Branched-From: b83393d0f4038aeaf67f970a024d8101df7348d1-refs/heads/main@{#1002911}

[modify] https://crrev.com/30be2a150c828d080679f0cbce5fc2a310375688/content/browser/indexed_db/indexed_db_context_impl.cc
[modify] https://crrev.com/30be2a150c828d080679f0cbce5fc2a310375688/content/browser/indexed_db/indexed_db_context_impl.h


### gi...@appspot.gserviceaccount.com (2022-05-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5a3f3336d3c61f710b91a0e5955735d5f5bb1332

commit 5a3f3336d3c61f710b91a0e5955735d5f5bb1332
Author: Ayu Ishii <ayui@chromium.org>
Date: Mon May 16 20:15:46 2022

[103] Quota: Use BindPostTask in QuotaManagerProxy

This change updates QuotaManagerProxy to use
base::BindPostTask to ensure callbacks are run or
destroyed on the specified task runner. The main difference
between the existing logic is that if the callback
is never run, it may not be destroyed on the correct task
runner. base::BindPostTask makes sure this doesn't happen.

Bug: 1324864
Change-Id: Ifd123031309e29a22761b8aa88ef2a216ad45c70
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3647916
Auto-Submit: Ayu Ishii <ayui@chromium.org>
Reviewed-by: Austin Sullivan <asully@chromium.org>
Commit-Queue: Austin Sullivan <asully@chromium.org>
Cr-Commit-Position: refs/branch-heads/5060@{#28}
Cr-Branched-From: b83393d0f4038aeaf67f970a024d8101df7348d1-refs/heads/main@{#1002911}

[modify] https://crrev.com/5a3f3336d3c61f710b91a0e5955735d5f5bb1332/storage/browser/quota/quota_manager_proxy.cc


### sr...@google.com (2022-05-17)

Merge approved for M102 branch: pls refer to go/chrome-branches for info

Please merge asap to M102 before 2pm PST today for RC cut, also make sure there is no issues on canary with this change and it is safe to merge.

### gi...@appspot.gserviceaccount.com (2022-05-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/21139756239bdcc79779320bb7f950b240169f40

commit 21139756239bdcc79779320bb7f950b240169f40
Author: Ari Chivukula <arichiv@chromium.org>
Date: Tue May 17 18:17:07 2022

{M102 PICK} [IndexedDB] Use-After-Free Fix

We can't guarantee order in the task the constructor dispatches the same
way we could before due to all the async changes. Let's be sure all the
objects exist before using them now. Long term, we need to address
ownership of the idb context.

Bug: 1324864, 1218100
Change-Id: Id5753297a4c966432028a1e7e063c5f1bed6f619
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3646994
Reviewed-by: Ayu Ishii <ayui@chromium.org>
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Cr-Commit-Position: refs/branch-heads/5005@{#812}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/21139756239bdcc79779320bb7f950b240169f40/content/browser/indexed_db/indexed_db_context_impl.cc
[modify] https://crrev.com/21139756239bdcc79779320bb7f950b240169f40/content/browser/indexed_db/indexed_db_context_impl.h


### gi...@appspot.gserviceaccount.com (2022-05-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/dbe72c6ad41a655fc0993c80e280e403aabf7c1a

commit dbe72c6ad41a655fc0993c80e280e403aabf7c1a
Author: Ayu Ishii <ayui@chromium.org>
Date: Tue May 17 18:26:17 2022

[102] Quota: Use BindPostTask in QuotaManagerProxy

This change updates QuotaManagerProxy to use
base::BindPostTask to ensure callbacks are run or
destroyed on the specified task runner. The main difference
between the existing logic is that if the callback
is never run, it may not be destroyed on the correct task
runner. base::BindPostTask makes sure this doesn't happen.

Bug: 1324864
Change-Id: I5bc27b26458e454f50709ddc5f9d71d2e9f6a3f2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3648495
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Commit-Queue: Ayu Ishii <ayui@chromium.org>
Cr-Commit-Position: refs/branch-heads/5005@{#813}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/dbe72c6ad41a655fc0993c80e280e403aabf7c1a/storage/browser/quota/quota_manager_proxy.cc


### am...@chromium.org (2022-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### gm...@google.com (2022-05-25)

[Empty comment from Monorail migration]

### rz...@google.com (2022-05-26)

[Empty comment from Monorail migration]

### rz...@google.com (2022-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-26)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-05-26)

1. Just https://crrev.com/c/3669025
2. Low, a few naming conflicts in the changed files
3. 102, 103
4. Yes

### gm...@google.com (2022-05-26)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-05-27)

Congratulations! The VRP Panel has decided to award you $20,000 for this report + $1,000 fuzzer bonus. Thank you for your efforts in reporting this issue to us and great work! 

### gi...@appspot.gserviceaccount.com (2022-05-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/64a9ef9bc2830a16429edcbc5f8f3571dcc4b4c0

commit 64a9ef9bc2830a16429edcbc5f8f3571dcc4b4c0
Author: Ari Chivukula <arichiv@chromium.org>
Date: Fri May 27 14:51:55 2022

[M96-LTS][IndexedDB] Use-After-Free Fix

M96 merge issues:
  indexed_db_context_impl.h:
    Conflicting naming/signature for BindIndexedDB* function.

  indexed_db_context_impl.cc:
    IndexedDBContextImpl::SetForceKeepSessionState(),
    IndexedDBContextImpl::Shutdown()
      Conflicting PostTask parameters, kept M96 version.

We can't guarantee order in the task the constructor dispatches the same
way we could before due to all the async changes. Let's be sure all the
objects exist before using them now. Long term, we need to address
ownership of the idb context.

(cherry picked from commit 9d8104567e1ede06e86a7ffe40e5d5bf359ae6d1)

Bug: 1324864, 1218100
Change-Id: Id5753297a4c966432028a1e7e063c5f1bed6f619
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3645544
Auto-Submit: Ari Chivukula <arichiv@chromium.org>
Quick-Run: Ari Chivukula <arichiv@chromium.org>
Commit-Queue: Ari Chivukula <arichiv@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1002978}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3669025
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Simon Hangl <simonha@google.com>
Owners-Override: Simon Hangl <simonha@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1639}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/64a9ef9bc2830a16429edcbc5f8f3571dcc4b4c0/content/browser/indexed_db/indexed_db_context_impl.cc
[modify] https://crrev.com/64a9ef9bc2830a16429edcbc5f8f3571dcc4b4c0/content/browser/indexed_db/indexed_db_context_impl.h


### rz...@google.com (2022-05-30)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-31)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-08-20)

This issue was migrated from crbug.com/chromium/1324864?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059651)*
