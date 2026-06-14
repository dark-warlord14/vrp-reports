# Heap-use-after-free in content::ServiceWorkerScriptCacheMap::NotifyFinishedCaching

| Field | Value |
|-------|-------|
| **Issue ID** | [40081168](https://issues.chromium.org/issues/40081168) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@chromium.org |
| **Assignee** | mi...@chromium.org |
| **Created** | 2015-01-12 |
| **Bounty** | $2,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6175432910045184

Fuzzer: Therealholden_worker
Job Type: Windows_asan_chrome

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x0344b80c
Crash State:
  content::ServiceWorkerScriptCacheMap::NotifyFinishedCaching
  content::ServiceWorkerWriteToCacheJob::Kill
  net::URLRequest::DoCancel
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv948aX6ZU7Krr-jQmQsHf1QqEsj8uwhVzcMTuSA94rarVGCS5ZAp5zMJgGARecjC2v1g2cD2wpb_vEaTEONXl33J1flY2T_RSj98oSDDD-7GUvUTVW7cPrzTqnFBzw8Wer7CCDNc4Nin1PNzHkcQhTJgwIFhSA


Additional requirements: Requires HTTP

Filer: inferno

## Timeline

### in...@chromium.org (2015-01-12)

Author: michaeln@chromium.org
Component: chromium
Changelist: https://chromium.googlesource.com/chromium/src//+/b54ef54a60dbd6b730292204ca51c006d5bf2a14
Time: Sat May 17 18:22:14 2014
The CL last changed line 72 of file service_worker_write_to_cache_job.cc, which is stack frame 1.

### in...@chromium.org (2015-01-12)

[Empty comment from Monorail migration]

### mi...@chromium.org (2015-01-12)

the fuzzer is so awesome

### cl...@chromium.org (2015-01-12)

[Empty comment from Monorail migration]

### mi...@chromium.org (2015-01-13)

Clearly ServiceWorkerScriptCacheMap needs to test for !context_, but I don't understand how neglecting to do so results in a use-after-free? Since context_is a WeakPtr<> I would expect it to result in a nullptr access?

### in...@chromium.org (2015-01-13)

The allocation stack (3rd one) usually gives an idea on the object freed. looks to be this one.

new ServiceWorkerContextCore(user_data_directory,
                                                   stores_task_runner,
                                                   database_task_manager.Pass(),
                                                   disk_cache_thread,
                                                   quota_manager_proxy,
                                                   special_storage_policy,
                                                   observer_list_.get(),
                                                   this)

### mi...@chromium.org (2015-01-13)

[Empty comment from Monorail migration]

### mi...@chromium.org (2015-01-13)

> ServiceWorkerContextCore

Sure, but context_ is a weakptr<> and the getter looks like this...

T* get() const { return ref_.is_valid() ? ptr_ : NULL; }

If the context is deleted, the ServiceWorkerScriptCacheMap class should have no way to reach its former address.

### mb...@chromium.org (2015-01-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-01-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/55f7c1cace6d82a071bccf8a465944c5e63a3e2a

commit 55f7c1cace6d82a071bccf8a465944c5e63a3e2a
Author: michaeln <michaeln@chromium.org>
Date: Tue Jan 13 19:32:07 2015

Add a context_ null check needed in case of DeleteAndStartOver.

BUG=448082

Review URL: https://codereview.chromium.org/798883005

Cr-Commit-Position: refs/heads/master@{#311308}

[modify] http://crrev.com/55f7c1cace6d82a071bccf8a465944c5e63a3e2a/content/browser/service_worker/service_worker_script_cache_map.cc


### in...@chromium.org (2015-01-13)

Michael, were you able to reproduce this use-after-free/any crash at all with the testcase ? Since this was one-time-crasher, CF can't verify.

### cl...@chromium.org (2015-01-13)

[Empty comment from Monorail migration]

### mi...@chromium.org (2015-01-13)

No. I ran it locally and it didn't repo at all (didn't DeleteAndStartOver which has to happen for this bug to manifest). The change submitted definitely fixes a bug, but I'm wondering if its really the bug found by CF (see https://crbug.com/chromium/448082#c8).

### in...@chromium.org (2015-01-25)

have seen a new stack since then, assuming fixed.

### cl...@chromium.org (2015-01-26)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-02-17)

Merge Requested to M41 (branch 2272). 

### pe...@google.com (2015-02-17)

[Automated comment] Less than 2 weeks to go before stable on M41, manual review required.

### pe...@chromium.org (2015-02-18)

Merge approved for M41 branch 2272.

### pe...@chromium.org (2015-02-20)

Note: M41 stable cut happens in days, and you're approved for merge.  Get it in there!  (Let me know if you need any help, or aren't confident.)vvvvvvvvvv

### mi...@chromium.org (2015-02-21)

oh, thanx for the ping, I'm setting up to work with branches now!

### bu...@chromium.org (2015-02-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0b01d654e688415abcbb35c9999dae0353ef00bc

commit 0b01d654e688415abcbb35c9999dae0353ef00bc
Author: Michael Nordman <michaeln@google.com>
Date: Sat Feb 21 01:00:16 2015

Add a context_ null check needed in case of DeleteAndStartOver.

BUG=448082

Review URL: https://codereview.chromium.org/798883005

Cr-Commit-Position: refs/heads/master@{#311308}
(cherry picked from commit 55f7c1cace6d82a071bccf8a465944c5e63a3e2a)

Review URL: https://codereview.chromium.org/949603002

Cr-Commit-Position: refs/branch-heads/2272@{#350}
Cr-Branched-From: 827a380cfdb31aa54c8d56e63ce2c3fd8c3ba4d4-refs/heads/master@{#310958}

[modify] http://crrev.com/0b01d654e688415abcbb35c9999dae0353ef00bc/content/browser/service_worker/service_worker_script_cache_map.cc


### ti...@google.com (2015-02-26)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-03)

Congrats - $2500 for this report as well.

Notes from reward panel: $2000 for this report +$500 ClusterFuzz bonus.

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-17)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2015-05-04)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/448082?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081168)*
