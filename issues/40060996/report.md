# Security: Heap-use-after-free in UnusedSitePermissionsService::UpdateUnusedPermissionsAsync

| Field | Value |
|-------|-------|
| **Issue ID** | [40060996](https://issues.chromium.org/issues/40060996) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Permissions |
| **Platforms** | Linux |
| **Reporter** | me...@gmail.com |
| **Assignee** | du...@chromium.org |
| **Created** | 2022-09-16 |
| **Bounty** | $1,000.00 |

## Description

**Steps to reproduce the problem:**  

repro:

1. apply the change.diff and compile chromium with ASAN
2. run `./chrome --user-data-dir=/tmp/noexist --enable-features=RecordPermissionExpirationTimestamps`
3. open a new profile then close it

**Problem Description:**  

This is introduced by commit eb9b044bcbd96458ba15f743d34b9c67401f8188

In function `UpdateUnusedPermissionsAsync`, it will post a `Unretained(this)` to threadpool, if this is deleted before the callback is running, UAF occurs.

Because the `Unretaiend(this)` is bound to Profile, so we need to close browser to trigger this problem.  

Furthermore, due to the small time window of the threadpool, I patch the code to let callback run slowly.

```
void UnusedSitePermissionsService::UpdateUnusedPermissionsAsync(  
    base::RepeatingClosure callback) {  
  DCHECK_CURRENTLY_ON(content::BrowserThread::UI);  
  base::ThreadPool::PostTaskAndReplyWithResult(  
      FROM_HERE, {base::TaskPriority::BEST_EFFORT},  
      base::BindOnce(&UnusedSitePermissionsService::GetUnusedPermissionsMap,  
                     base::Unretained(this)),  
      base::BindOnce(  
          &UnusedSitePermissionsService::OnUnusedPermissionsMapRetrieved,  
          AsWeakPtr(), std::move(callback)));  
}  

```

For patch, you could change `Unreatained(this)` to a WeakPtr

```
void UnusedSitePermissionsService::UpdateUnusedPermissionsAsync(  
    base::RepeatingClosure callback) {  
  DCHECK_CURRENTLY_ON(content::BrowserThread::UI);  
  base::ThreadPool::PostTaskAndReplyWithResult(  
      FROM_HERE, {base::TaskPriority::BEST_EFFORT},  
      base::BindOnce(&UnusedSitePermissionsService::GetUnusedPermissionsMap,  
-                     base::Unretained(this)),  
+                     AsWeakPtr()),  
      base::BindOnce(  
          &UnusedSitePermissionsService::OnUnusedPermissionsMapRetrieved,  
          AsWeakPtr(), std::move(callback)));  
}  
  
[1] https://source.chromium.org/chromium/chromium/src/+/main:components/permissions/unused_site_permissions_service.cc;l=79;drc=eb9b044bcbd96458ba15f743d34b9c67401f8188;bpv=0;bpt=0  
  
**Additional Comments:**   
  
  
**Chrome version: **  **Channel: ** Not sure  
  
**OS:** Linux

```

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 48.2 KB)
- [poc.webm](attachments/poc.webm) (video/webm, 1.2 MB)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2022-09-16)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-09-16)

Note: Patch just introduces a sleep which makes the condition more likely.
Assigning per reported bisect of  eb9b044bcbd96458ba15f743d34b9c67401f8188, dullweber - please take a look or re-assign as appropriate.
eb9b044bcbd96458ba15f743d34b9c67401f8188 is very recent, trunk churn but in the vicinity of the expected m017 branch, setting accordingly.

[Monorail components: Internals>Permissions]

### [Deleted User] (2022-09-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-16)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-17)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### du...@google.com (2022-09-19)

Thanks for the report!

The code is currently not enabled on any channel so it doesn't require RBS. 
I'm think a WeakPtr can't be used here because the function returns a value which is not allowed with WeakPtrs. 
Also WeakPtrs can not be used across threads. https://source.chromium.org/chromium/chromium/src/+/main:base/memory/weak_ptr.h;l=50;drc=e4622aaeccea84652488d1822c28c78b7115684f

I was planning to add a CancelableTaskTracker but I'm not sure if this actually helps since the call is happening across threads. Maybe making the method a static function and passing in a ScopedPtr for HostContentSettingsMap would work or just running as a low priority task on the UI thread.





### me...@gmail.com (2022-09-19)

Thank you for your reply! I just noticed that WeakPtr is useless here, sorry!

### [Deleted User] (2022-09-19)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### du...@google.com (2022-09-20)

[Empty comment from Monorail migration]

### du...@chromium.org (2022-09-20)

Created a patch: https://crrev.com/c/3904906

### du...@chromium.org (2022-09-21)

The RecordPermissionExpirationTimestamps feature is disabled by default and not controlled through an entry in chrome://flags so security impact can be reduced to None.

Since the use-after-free can only be triggered through browser shutdown, the severity can be reduced to medium: "Bugs that would normally be rated at a higher severity level with unusual mitigating factors may be rated as medium severity"

### du...@google.com (2022-09-21)

[Empty comment from Monorail migration]

### du...@chromium.org (2022-09-21)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-09-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d69947e4db8d214b02eb5541a52594830288e854

commit d69947e4db8d214b02eb5541a52594830288e854
Author: Christian Dullweber <dullweber@chromium.org>
Date: Wed Sep 21 17:14:38 2022

Safety check: Fix use-after-free in UnusedPermissionService

Ensure that GetUnusedPermissionsMap does not access any shared state
when it is running on a background thread by passing in dependencies
directly and turning it into a simple function.

Bug: 1364492
Change-Id: I186ab7372c85b3c0291aef4dc650be80c66860b2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3904906
Reviewed-by: Side YILMAZ <sideyilmaz@chromium.org>
Reviewed-by: Illia Klimov <elklm@chromium.org>
Commit-Queue: Christian Dullweber <dullweber@chromium.org>
Reviewed-by: Illia Klimov <elklm@google.com>
Cr-Commit-Position: refs/heads/main@{#1049706}

[modify] https://crrev.com/d69947e4db8d214b02eb5541a52594830288e854/chrome/browser/permissions/unused_site_permissions_service_browsertest.cc
[modify] https://crrev.com/d69947e4db8d214b02eb5541a52594830288e854/components/permissions/unused_site_permissions_service.h
[modify] https://crrev.com/d69947e4db8d214b02eb5541a52594830288e854/components/permissions/unused_site_permissions_service.cc
[modify] https://crrev.com/d69947e4db8d214b02eb5541a52594830288e854/components/permissions/unused_site_permissions_service_unittest.cc


### du...@chromium.org (2022-09-22)

Requesting to fix the above CL to M107 to fix a security issue

### hc...@google.com (2022-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-22)

Merge approved: your change passed merge requirements and is auto-approved for M107. Please go ahead and merge the CL to branch 5304 (refs/branch-heads/5304) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), eakpobaro (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-22)

[Empty comment from Monorail migration]

### du...@google.com (2022-09-23)

Change is ready but I can't submit it because some bots have problems with applying the patch: https://crrev.com/c/3909400
I already tried to rebase but it tells me that I'm up to date


### gi...@appspot.gserviceaccount.com (2022-09-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5ac46a2d300c07d68522379aaf584eca00b8d9fb

commit 5ac46a2d300c07d68522379aaf584eca00b8d9fb
Author: Christian Dullweber <dullweber@chromium.org>
Date: Fri Sep 23 17:49:26 2022

Safety check: Fix use-after-free in UnusedPermissionService

Ensure that GetUnusedPermissionsMap does not access any shared state
when it is running on a background thread by passing in dependencies
directly and turning it into a simple function.

(cherry picked from commit d69947e4db8d214b02eb5541a52594830288e854)

Bug: 1364492
Change-Id: I186ab7372c85b3c0291aef4dc650be80c66860b2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3904906
Reviewed-by: Side YILMAZ <sideyilmaz@chromium.org>
Reviewed-by: Illia Klimov <elklm@chromium.org>
Commit-Queue: Christian Dullweber <dullweber@chromium.org>
Reviewed-by: Illia Klimov <elklm@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1049706}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3909400
Cr-Commit-Position: refs/branch-heads/5304@{#117}
Cr-Branched-From: 5d7b1fc9cb7103d9c82eed647cf4be38cf09738b-refs/heads/main@{#1047731}

[modify] https://crrev.com/5ac46a2d300c07d68522379aaf584eca00b8d9fb/chrome/browser/permissions/unused_site_permissions_service_browsertest.cc
[modify] https://crrev.com/5ac46a2d300c07d68522379aaf584eca00b8d9fb/components/permissions/unused_site_permissions_service.h
[modify] https://crrev.com/5ac46a2d300c07d68522379aaf584eca00b8d9fb/components/permissions/unused_site_permissions_service.cc
[modify] https://crrev.com/5ac46a2d300c07d68522379aaf584eca00b8d9fb/components/permissions/unused_site_permissions_service_unittest.cc


### am...@google.com (2022-10-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-10-14)

Congratulations on another one this week! The VRP Panel has decided to award you $1,000 for this report of a heavily mitigated security issue. Thank you for your efforts in finding and reporting this issue to us! 

### me...@gmail.com (2022-10-14)

[Comment Deleted]

### am...@google.com (2022-10-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1364492?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1365262, crbug.com/chromium/1365794]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060996)*
