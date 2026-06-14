# UAF in indexeddb  IndexedDBDatabase::RequestComplete

| Field | Value |
|-------|-------|
| **Issue ID** | [40094312](https://issues.chromium.org/issues/40094312) |
| **Status** | New |
| **Severity** | S4-Minimal |
| **Priority** | P0 |
| **Component** | Blink>Storage>IndexedDB |
| **Platforms** | Android, Linux, Mac, ChromeOS |
| **Reporter** | cd...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2019-03-17 |
| **Bounty** | $10,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36

Steps to reproduce the problem:
1. download and unzip the release asan chromium :asan-linux-release-639779 
2. Set up a webserver and put poc.html 
3. Run ./chrome  crash.html 

What is the expected behavior?

What went wrong?
Can stably get UAF crash.
I test it both in 75.0.3731.0 and  75.0.3736.0 asan version.

Did this work before? N/A 

Chrome version: 75.0.3731.0  Channel: n/a
OS Version: 16.04
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### wf...@chromium.org (2019-03-18)

Thank you for your report. I am triaging this. cdsrc2016@: have you also verified this on the latest trunk or is r639779 latest rev this reproduces on?

[Monorail components: Blink>Storage>IndexedDB]

### cl...@chromium.org (2019-03-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6565848690065408.

### wf...@chromium.org (2019-03-18)

On face value, given Chrome versions supplied in #0, this looks like a pri-0 critical sandbox escape. Setting flags until we know otherwise.

Will continue triage in parallel. dmurph - can you also take a look at this bug?

### cl...@chromium.org (2019-03-18)

Detailed report: <https://clusterfuzz.com/testcase?key=6565848690065408>

Job Type: linux\_asan\_chrome\_mp  

Platform Id: linux

Crash Type: Heap-use-after-free READ 8  

Crash Address: 0x6140004c9fb0  

Crash State:  

content::IndexedDBDatabase::DeleteRequest::DoDelete  

void base::internal::InvokeHelper<true, void>::MakeItSo<void  

base::internal::Invoker<base::internal::BindState<content::DisjointRangeLockMana

Sanitizer: address (ASAN)

Recommended Security Severity: High

Reproducer Testcase: <https://clusterfuzz.com/download?testcase_id=6565848690065408>

See <https://github.com/google/clusterfuzz-tools> for instructions to reproduce this bug locally.

**Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days we've been seeing this crash frequently. If you are unable to reproduce this, please try a speculative fix based on the crash stacktrace in the report. The fix can be verified by looking at the crash statistics in the report, a day after the fix is deployed. We will auto-close the bug if the crash is not seen for 14 days.**

The recommended severity (Security\_Severity-High) is different from what was assigned to the bug. Please double check the accuracy of the assigned severity.

### wf...@chromium.org (2019-03-18)

could this be https://chromium-review.googlesource.com/c/chromium/src/+/1506552 ? it's in the regression range and makes changes to this area of code.

### oc...@google.com (2019-03-19)

+markbrand, who is actively working on a Mojo fuzzer.

### cd...@gmail.com (2019-03-19)

Hi wfh@, i'd verified this on 639779. Besides, 641473 is also affected.

### cd...@gmail.com (2019-03-19)

Here is the simple analysis, hope it helps.


Perhaps it caused by re-using the ScopesLockManager.
When delete a database,the indexed_db_factory_impl will create a new scoped_ref IndexedDBDatabase, and pass the scoped_refptr to the DeleteRequest.
So the ref_count_ of this fresh IndexedDBDatabase now is 2 .

In src/content/browser/indexed_db/indexed_db_factory_impl.cc
void IndexedDBFactoryImpl::DeleteDatabase(...){
 ...
scoped_refptr<IndexedDBDatabase> database;            <----ref_count_ = 1
  std::tie(database, s) = IndexedDBDatabase::Create(
      name, backing_store.get(), this,
      std::make_unique<IndexedDBMetadataCoding>(), unique_identifier,
      backing_store->lock_manager());
...
}

In content/browser/indexed_db/indexed_db_database.cc
void IndexedDBDatabase::DeleteDatabase(
    scoped_refptr<IndexedDBCallbacks> callbacks,
    bool force_close) {
  AppendRequest(std::make_unique<DeleteRequest>(this, callbacks));  <---ref_count_ = 2 and append the request to pending_requests_ and start perform();
  ...
}


The next function Perform() acquires a lock and pass the DeleteRequest::DoDelete function to lock_manager_. Under normal condition, this request(we called request_one) will sucess and the callback will run directly. But if we add opendatabase and some other operation into the indexedDB.deleteDatabase's onsuccess callback function, it will acquire the same lock before the request_one acquires  and let request_one  be failed .

In content/browser/indexed_db/scopes/disjoint_range_lock_manager.cc
bool DisjointRangeLockManager::AcquireLock(
    ScopeLockRequest request,
    LockAquiredCallback acquired_callback) {
  ...
  if (lock.CanBeAcquired(request.type)) {
  ...
  } else {
    // The lock cannot be acquired now, so we put it on the queue which will
    // grant the given callback the lock when it is acquired in the future in
    // the |LockReleased| method.
    lock.queue.emplace_back(request.type, std::move(acquired_callback));  <----- if CanBeAcquired failed , acquired_callback will not run 
  }
  return true;
}

Then the lock_manager will push the request_one's acquired_callback funciont(DeleteRequest::DoDelete) into the lock's queue and DeleteRequest::DoDelete will not run until the next DisjointRangeLockManager::LockReleased called.

After that,when progress comes back to IndexedDBFactoryImpl::DeleteDatabase, it will set database = nullptr, which leads the ref_count_--.Now ref_count_ = 1.

Once the the next DisjointRangeLockManager::LockReleased called, the remaining callback in lock's queue will run and go into RequestComplete.This call reset
the active_request_ , releases it's member db_ and now ref_count_ = 0. At this point , the fresh IndexedDBDatabase is freed.

In content/browser/indexed_db/indexed_db_database.cc:
void IndexedDBDatabase::RequestComplete(ConnectionRequest* request) {
  DCHECK_EQ(request, active_request_.get());
  active_request_.reset();          <----release active_request_ and free its member db_, so ref_count_-- again then free IndexedDBDatabase.

  if (!pending_requests_.empty())   <----pending_requests_ is the member of freed IndexedDBDatabase. UAF happened.
    ProcessRequestQueue();
}

Once access to its member pending_requests_, UAF happened.







### sh...@chromium.org (2019-03-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-19)

This is a critical security issue. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-03-19)

+awhalley@ (Security TPM)

### aw...@google.com (2019-03-19)

Hi dmurph@ - could you ACK when you see this? We're currently treating this as a blocker for this week's Beta promotion.

### dm...@chromium.org (2019-03-19)

ACK

### go...@chromium.org (2019-03-19)

+ TPMS as this is blocking M74 Beta release on Thursday.

### dm...@chromium.org (2019-03-19)

Strangely, I can't repro. But I have a fix.

### go...@chromium.org (2019-03-19)

Thank you dmurph@. Pls land the fix to trunk ASAP.

### dm...@chromium.org (2019-03-19)

It's almost through the CQ
https://chromium-review.googlesource.com/c/chromium/src/+/1531013

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-03-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0cc616126030a9102233ec1e0ca5e5f5aa8ea180

commit 0cc616126030a9102233ec1e0ca5e5f5aa8ea180
Author: Daniel Murphy <dmurph@chromium.org>
Date: Tue Mar 19 20:24:37 2019

[IndexedDB] Prevent UAF during PendingRequest execution

R=cmp@chromium.org

Bug: 942898
Change-Id: Ib33c59bae0e1691549ff33866cc44a09559a5a0b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1531013
Commit-Queue: Daniel Murphy <dmurph@chromium.org>
Reviewed-by: Chase Phillips <cmp@chromium.org>
Cr-Commit-Position: refs/heads/master@{#642156}
[modify] https://crrev.com/0cc616126030a9102233ec1e0ca5e5f5aa8ea180/content/browser/indexed_db/indexed_db_database.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-03-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b2fb108c4836500e569b1474308bacb534f0af36

commit b2fb108c4836500e569b1474308bacb534f0af36
Author: Daniel Murphy <dmurph@chromium.org>
Date: Tue Mar 19 20:26:58 2019

[IndexedDB] Prevent UAF during PendingRequest execution

R=​cmp@chromium.org

Bug: 942898
Change-Id: Ib33c59bae0e1691549ff33866cc44a09559a5a0b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1531287
Reviewed-by: Daniel Murphy <dmurph@chromium.org>
Cr-Commit-Position: refs/branch-heads/3738@{#9}
Cr-Branched-From: ddf870ba8d01cd04357db9ae6a480d75a7e2f398-refs/heads/master@{#641783}
[modify] https://crrev.com/b2fb108c4836500e569b1474308bacb534f0af36/content/browser/indexed_db/indexed_db_database.cc


### go...@chromium.org (2019-03-19)

Thank you dmurph@. Triggering new canary for Android and Desktop from branch 3738.

### go...@chromium.org (2019-03-19)

Canary version  75.0.3738.4 just got triggered which includes merge listed at #19. 

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-03-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/434bec199aae7a5430cb4754714ed2ddc9babf12

commit 434bec199aae7a5430cb4754714ed2ddc9babf12
Author: Daniel Murphy <dmurph@chromium.org>
Date: Tue Mar 19 23:56:06 2019

[IndexedDB] Prevent UAF during PendingRequest execution

R=​cmp@chromium.org

Bug: 942898
Change-Id: Ib33c59bae0e1691549ff33866cc44a09559a5a0b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1531013
Commit-Queue: Daniel Murphy <dmurph@chromium.org>
Reviewed-by: Chase Phillips <cmp@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#642156}(cherry picked from commit 0cc616126030a9102233ec1e0ca5e5f5aa8ea180)
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1531699
Reviewed-by: Krishna Govind <govind@chromium.org>
Cr-Commit-Position: refs/branch-heads/3729@{#290}
Cr-Branched-From: d4a8972e30b604f090aeda5dfff68386ae656267-refs/heads/master@{#638880}
[modify] https://crrev.com/434bec199aae7a5430cb4754714ed2ddc9babf12/content/browser/indexed_db/indexed_db_database.cc


### cr...@appspot.gserviceaccount.com (2019-03-19)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/434bec199aae7a5430cb4754714ed2ddc9babf12

Commit: 434bec199aae7a5430cb4754714ed2ddc9babf12
Author: dmurph@chromium.org
Commiter: govind@chromium.org
Date: 2019-03-19 23:56:06 +0000 UTC

[IndexedDB] Prevent UAF during PendingRequest execution

R=​cmp@chromium.org

Bug: 942898
Change-Id: Ib33c59bae0e1691549ff33866cc44a09559a5a0b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1531013
Commit-Queue: Daniel Murphy <dmurph@chromium.org>
Reviewed-by: Chase Phillips <cmp@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#642156}(cherry picked from commit 0cc616126030a9102233ec1e0ca5e5f5aa8ea180)
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1531699
Reviewed-by: Krishna Govind <govind@chromium.org>
Cr-Commit-Position: refs/branch-heads/3729@{#290}
Cr-Branched-From: d4a8972e30b604f090aeda5dfff68386ae656267-refs/heads/master@{#638880}

### go...@chromium.org (2019-03-20)

I merged the change to M74 branch 3729 without canary coverage just in case if we decide to get beta qualification tonight. Per chat with dmurph@, change is very safe. 

### sh...@chromium.org (2019-03-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-20)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2019-03-20)

ClusterFuzz has detected this issue as fixed in range 642148:642166.

Detailed report: https://clusterfuzz.com/testcase?key=6565848690065408

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6140004c9fb0
Crash State:
  content::IndexedDBDatabase::DeleteRequest::DoDelete
  void base::internal::InvokeHelper<true, void>::MakeItSo<void
  base::internal::Invoker<base::internal::BindState<content::DisjointRangeLockMana
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=638348:638354
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=642148:642166

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6565848690065408

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2019-03-20)

ClusterFuzz testcase 6565848690065408 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2019-03-21)

[Empty comment from Monorail migration]

### na...@google.com (2019-03-25)

[Empty comment from Monorail migration]

### na...@google.com (2019-03-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-03-26)

Congrats! The Panel decided to reward $10,000 for this report. 

### na...@google.com (2019-03-26)

[Empty comment from Monorail migration]

### na...@google.com (2019-03-26)

[Empty comment from Monorail migration]

### cd...@gmail.com (2019-03-27)

Thanks a lot for the reward :)

### aw...@google.com (2019-04-05)

[Empty comment from Monorail migration]

### aw...@google.com (2019-06-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@chromium.org (2020-01-07)

dmurph@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### wi...@gmail.com (2021-06-10)

Now, can we still have the crash.html?

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/942898?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094312)*
