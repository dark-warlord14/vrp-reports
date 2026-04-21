# AddressSanitizer: heap-use-after-free storage::QuotaDatabase::CreateBucketInternal quota_database.cc

| Field | Value |
|-------|-------|
| **Issue ID** | [40059717](https://issues.chromium.org/issues/40059717) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage>Quota |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | es...@chromium.org |
| **Created** | 2022-05-22 |
| **Bounty** | $15,000.00 |

## Description

**Steps to reproduce the problem:**  

#Reproduce  

The problem was found by my fuzzer running on CF(CC Security team for access permission <https://clusterfuzz.com/testcase-detail/5374017724940288>),  

But it cannot be reproduced stably, CF may not automatically report.  

After manual analysis, the root cause of the vulnerability is clearly understood.

#Type of crash  

browser process(Sandbox escape)

**Problem Description:**  

#Analysis

1. QuotaManagerImpl is a RefCountedDeleteOnSequence[2] object and owns QuotaDatabase[3]
2. When QuotaManagerImpl::UpdateOrCreateBucket is called[0], he will call PostTaskAndReplyWithResultForDBThread, and finally put the task on db\_runner\_ to execute, but here the this pointer is passed using Unretained
3. db\_runner\_ is a thread pool for sequence execution, but and QuotaManagerImpl objects may be freed in other threads, causing UAF

```
//https://source.chromium.org/chromium/chromium/src/+/main:storage/browser/quota/quota_manager_impl.cc;drc=8d0a6f910d77d336e80d1b68f523835a324fe451;l=1049  
void QuotaManagerImpl::UpdateOrCreateBucket(  
    const BucketInitParams& bucket_params,  
    base::OnceCallback<void(QuotaErrorOr<BucketInfo>)> callback) {  
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);  
  DCHECK(callback);  
  EnsureDatabaseOpened();  
  
  if (db_disabled_) {  
    std::move(callback).Run(QuotaError::kDatabaseError);  
    return;  
  }  
  PostTaskAndReplyWithResultForDBThread(  
      base::BindOnce(  
          [](const BucketInitParams& params, QuotaDatabase\* database) {  
            DCHECK(database);  
            return database->UpdateOrCreateBucket(params);							<<[0]  
          },  
          bucket_params),  
      base::BindOnce(&QuotaManagerImpl::DidGetBucket,  
                     weak_factory_.GetWeakPtr(), std::move(callback)));  
}  
  
//https://source.chromium.org/chromium/chromium/src/+/main:storage/browser/quota/quota_manager_impl.cc;drc=8d0a6f910d77d336e80d1b68f523835a324fe451;l=2952  
template <typename ValueType>  
void QuotaManagerImpl::PostTaskAndReplyWithResultForDBThread(  
    base::OnceCallback<QuotaErrorOr<ValueType>(QuotaDatabase\*)> task,  
    base::OnceCallback<void(QuotaErrorOr<ValueType>)> reply,  
    const base::Location& from_here,  
    bool is_bootstrap_task) {  
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);  
  DCHECK(task);  
  DCHECK(reply);  
  // Deleting manager will post another task to DB sequence to delete  
  // |database_|, therefore we can be sure that database_ is alive when this  
  // task runs.  
  
  if (!is_bootstrap_task && is_bootstrapping_database_) {  
    database_callbacks_.push_back(base::BindOnce(  
        &QuotaManagerImpl::PostTaskAndReplyWithResultForDBThread<ValueType>,  
        weak_factory_.GetWeakPtr(), std::move(task), std::move(reply),  
        from_here, is_bootstrap_task));  
    return;  
  }  
  
  base::PostTaskAndReplyWithResult(  
      db_runner_.get(), from_here,  
      base::BindOnce(std::move(task), base::Unretained(database_.get())),			<<[1]  
      std::move(reply));  
}  
  
//https://source.chromium.org/chromium/chromium/src/+/main:storage/browser/quota/quota_manager_impl.h;drc=8d0a6f910d77d336e80d1b68f523835a324fe451;l=128  
class COMPONENT_EXPORT(STORAGE_BROWSER) QuotaManagerImpl  
    : public QuotaTaskObserver,  
      public QuotaEvictionHandler,  
      public base::RefCountedDeleteOnSequence<QuotaManagerImpl>,					<<[2]  
      public storage::mojom::QuotaInternalsHandler {  
 public:  
 ...CUT...  
  absl::optional<blink::StorageKey>  
      storage_key_for_pending_storage_pressure_callback_;  
  scoped_refptr<base::SingleThreadTaskRunner> io_thread_;  
  scoped_refptr<base::SequencedTaskRunner> db_runner_;  
  mutable std::unique_ptr<QuotaDatabase> database_;									<<[3]  
  
//https://source.chromium.org/chromium/chromium/src/+/main:storage/browser/quota/quota_manager_impl.cc;drc=8d0a6f910d77d336e80d1b68f523835a324fe451;l=1000  
QuotaManagerImpl::QuotaManagerImpl(  
    bool is_incognito,  
    const base::FilePath& profile_path,  
    scoped_refptr<base::SingleThreadTaskRunner> io_thread,  
    base::RepeatingClosure quota_change_callback,  
    scoped_refptr<SpecialStoragePolicy> special_storage_policy,  
    const GetQuotaSettingsFunc& get_settings_function)  
    : RefCountedDeleteOnSequence<QuotaManagerImpl>(io_thread),  
      is_incognito_(is_incognito),  
      profile_path_(profile_path),  
      proxy_(base::MakeRefCounted<QuotaManagerProxy>(this,  
                                                     io_thread,  
                                                     profile_path)),  
      io_thread_(std::move(io_thread)),  
      db_runner_(base::ThreadPool::CreateSequencedTaskRunner(						<<[4]  
          {base::MayBlock(), base::TaskPriority::USER_VISIBLE,  
           base::TaskShutdownBehavior::BLOCK_SHUTDOWN})),  
      get_settings_function_(get_settings_function),  

```

**Additional Comments:**  

#Patch  

My fix is not to use weak\_factory\_ in the QuotaManagerImpl::UpdateOrCreateBucket function, but to use the this pointer directly to increase the QuotaManagerImpl object reference count to ensure that the object will not be released. I don't think this is the best solution, but it's relatively clear.

```
diff --git a/storage/browser/quota/quota_manager_impl.cc b/storage/browser/quota/quota_manager_impl.cc  
index 3ba2906..aa4556f 100644  
--- a/storage/browser/quota/quota_manager_impl.cc  
+++ b/storage/browser/quota/quota_manager_impl.cc  
@@ -1062,7 +1062,7 @@  
           },  
           bucket_params),  
       base::BindOnce(&QuotaManagerImpl::DidGetBucketCheckExpiration,  
-                     weak_factory_.GetWeakPtr(), bucket_params,  
+                     this, bucket_params,  
                      std::move(callback)));  
 }  

```

\*\*Chrome version: \*\* 102.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Windows

## Attachments

- [patch.diff](attachments/patch.diff) (text/plain, 817 B)
- [asan.txt](attachments/asan.txt) (text/plain, 24.5 KB)

## Timeline

### dt...@chromium.org (2022-05-24)

[Empty comment from Monorail migration]

[Monorail components: Blink>Storage>Quota]

### [Deleted User] (2022-05-24)

[Empty comment from Monorail migration]

### dr...@chromium.org (2022-05-24)

For triage purposes, can you elaborate a little on what your fuzzer is doing? You call this a sandbox escape, does that mean that you have assumed arbitrary code execution in the renderer process? (This assumption is the difference between Critical severity and High severity, so I'd like to double check)

### m....@gmail.com (2022-05-25)

As I said, this is reported by the fuzzer running on clusterfuzz, which can trigger sbx directly, without the need for a compromised rendering process.
All info is here https://clusterfuzz.com/testcase-detail/5374017724940288

### dr...@chromium.org (2022-05-25)

The clusterfuzz test case does not give very much detail on what interface is being fuzzed, and because the case is unminimized, just gives 140 KB of randomly-generated javascript. That doesn't give a lot of insight into how the problem is being triggered. If you are able to create a minimal test case, that would be extremely useful, as I'm not able to manually reproduce this. Since Clusterfuzz can't reproduce it reliably, and I can't reproduce it except at one revision, marking FoundIn for that revision (M104).

As far as I can tell, this is a shutdown bug, since the QuotaManagerImpl won't be destroyed until the associated BrowserContext is. This makes it a High Severity bug. If that does not match your analysis, let me know. 

ayui@, asully@ - can you take a look?

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### ay...@chromium.org (2022-05-25)

Thanks for the report m.cooolie@gmail.com.
Is there a stack trace of the crash you can provide?

Unable to see the clusterfuzz testcase yet, but put in a request to gain access.

### es...@chromium.org (2022-05-25)

For the one callsite that is described in the initial report, this code is disabled (behind a flag). It seems that there are other callsites for PostTaskAndReplyWithResultForDBThread that could potentially run afoul of this, so if the weak ptr usage is indeed the culprit we need to change many callsites.

I don't fully understand the report though. Based on my reading of the code, it seems that deletion of QuotaManagerImpl::database_ is handled correctly because it's deleted by a task posted to db_runner_.

### m....@gmail.com (2022-05-26)

re https://crbug.com/chromium/1327927#c08 

### [Deleted User] (2022-05-26)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-26)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-26)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### es...@chromium.org (2022-05-26)

Daniel can you make sure the labels are appropriate given that this code is only available behind a disabled feature flag.

### es...@chromium.org (2022-05-26)

ah, thanks for the asan stack. I see the issue, it's QuotaDatabase::clock_. The code described in the original report is not a problem.

### es...@chromium.org (2022-05-26)

[Empty comment from Monorail migration]

### dr...@chromium.org (2022-05-27)

Just double-checking: is the problematic code disabled by default? I want to make sure #14 didn't mean your opinion changed on that.

### es...@chromium.org (2022-05-27)

No, it is not disabled by default. It impacts head. The culprit is: Commit d415a005... initially landed in 104.0.5078.0

### dr...@chromium.org (2022-05-27)

Excellent, thank you. The labels are all accurate in that case then.

### gi...@appspot.gserviceaccount.com (2022-05-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7c0e03fe41af2d503987f1315f10198056e633c9

commit 7c0e03fe41af2d503987f1315f10198056e633c9
Author: Evan Stade <estade@chromium.org>
Date: Tue May 31 18:08:14 2022

Quota: fix test clock UAF.

Bug: 1327927
Change-Id: I48daf26328770ba8169d7c03af6b8b1c6997bfae
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3670130
Reviewed-by: Daniel Rubery <drubery@chromium.org>
Commit-Queue: Evan Stade <estade@chromium.org>
Reviewed-by: Ayu Ishii <ayui@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1009173}

[modify] https://crrev.com/7c0e03fe41af2d503987f1315f10198056e633c9/storage/browser/quota/quota_manager_impl.cc
[modify] https://crrev.com/7c0e03fe41af2d503987f1315f10198056e633c9/storage/browser/quota/quota_database.h
[modify] https://crrev.com/7c0e03fe41af2d503987f1315f10198056e633c9/storage/browser/quota/quota_manager_unittest.cc
[modify] https://crrev.com/7c0e03fe41af2d503987f1315f10198056e633c9/storage/browser/quota/quota_database_unittest.cc
[modify] https://crrev.com/7c0e03fe41af2d503987f1315f10198056e633c9/storage/browser/quota/quota_manager_impl.h
[modify] https://crrev.com/7c0e03fe41af2d503987f1315f10198056e633c9/storage/browser/quota/quota_database_migrations_unittest.cc
[modify] https://crrev.com/7c0e03fe41af2d503987f1315f10198056e633c9/storage/browser/quota/quota_database.cc


### es...@chromium.org (2022-06-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-11)

Not requesting merge to dev (M104) because latest trunk commit (1009173) appears to be prior to dev branch point (1012729). If this is incorrect, please replace the Merge-NA-104 label with Merge-Request-104. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-06-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-06-16)

Congratulations! The VRP Panel has decided to award you $15,000 for this report + $1k fuzzer bonus. Thank you for your efforts and reporting this issue to us! Nice work! 

### am...@google.com (2022-06-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1327927?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059717)*
