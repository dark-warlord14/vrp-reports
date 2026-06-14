# Heap-use-after-free in syncer::SyncBackupManager::Init

| Field | Value |
|-------|-------|
| **Issue ID** | [40080080](https://issues.chromium.org/issues/40080080) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Unknown |
| **Reporter** | cl...@chromium.org |
| **Assignee** | [Deleted User] |
| **Created** | 2014-07-20 |
| **Bounty** | $1,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5764891220639744

Fuzzer: Attekett_surku_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x6150003faab0
Crash State:
  - crash stack -
  syncer::SyncBackupManager::Init
  browser_sync::SyncBackendHostCore::DoInitialize
  - free stack -
  browser_sync::SyncBackendHostCore::DoDestroySyncManager
  browser_sync::SyncBackendHostCore::OnInitializationComplete
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94AXMmZH4vt5es4ok3F_Etbq6tgEON2Gz9dGGafIRGNANQVlCqdH7FsXJ3pcvJkNXvjU05S0_aoifXcYg03CY_9IUDh2We3Rjs6_vWdsnTtGoB5hjBK2rYACZseGZi7NDZcSGxUEj_cdGot1MWIE5ilel0gAw

Filer: aarya@google.com

## Timeline

### in...@chromium.org (2014-07-20)

Looks like regression from http://src.chromium.org/viewvc/chrome?view=revision&revision=283840

### in...@chromium.org (2014-07-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-07-20)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5335067603763200

Fuzzer: Therealholden_worker
Job Type: Linux_msan_chrome

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  - crash stack -
  syncer::SyncBackupManager::Init
  browser_sync::SyncBackendHostCore::DoInitialize
  base::internal::Invoker<2, base::internal::BindState<base::internal::Runnab
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94s9lsgsCCzvm044Xrr603Bo3yMrsq_X1PHPhHN3a2_Kgo2yOoJiLp3zOV7vos7ATPV5BCqnZUxtlKxl9Ie1V9LBhint235a6rFoknnT5YftXzwjokunfeX7g1wFhpzLKt-T-nnXWcszPnmFrxIaelFGJJbxw

Additional requirements: Requires Interaction Gestures
Filer: inferno@chromium.org

### cl...@chromium.org (2014-07-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-07-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-07-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-07-22)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### [Deleted User] (2014-07-22)

I think it's unlikely to be related to r283840.  That was a refactoring patch.  I can think of two possible alternative explanations, though.

First, I'm guessing that we don't usually sign in to sync before running ClusterFuzz.  If that's the case, then we've probably never instantiated a SyncManager while under a ClusterFuzz test until recently.  With Haitao's changes to backup and restore, we now instantiate a SyncManager where we didn't before.  It's possible this has exposed pre-existing bugs.

The other possibility is that this bug is new and was introduced in the backup and restore feature.  I think the feature includes some new SyncManager start up and shut down logic, so there could be a problem with that new code.

I'll take a look and see if I can narrow down the cause.

### [Deleted User] (2014-07-22)

I have a hunch this is related to https://crbug.com/chromium/388948.  Revision r281416 tried to fix that issue by changing a bunch of the initialization failure handling logic.  

The ClusterFuzz test was run against r284327.  Maybe r281416 introduced a regression?

This is not my area of expertise.  Assigning to Haitao because he'll probably be able to diagnose the issue faster than I would.

### [Deleted User] (2014-07-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-07-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-07-23)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-07-24)

------------------------------------------------------------------
r285229 | haitaol@chromium.org | 2014-07-24T13:34:49.363064Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/sync/internal_api/sync_rollback_manager_base_unittest.cc?r1=285229&r2=285228&pathrev=285229
   M http://src.chromium.org/viewvc/chrome/trunk/src/sync/internal_api/sync_rollback_manager_base.cc?r1=285229&r2=285228&pathrev=285229
   M http://src.chromium.org/viewvc/chrome/trunk/src/sync/internal_api/sync_backup_manager.cc?r1=285229&r2=285228&pathrev=285229
   M http://src.chromium.org/viewvc/chrome/trunk/src/sync/internal_api/sync_rollback_manager_base.h?r1=285229&r2=285228&pathrev=285229
   M http://src.chromium.org/viewvc/chrome/trunk/src/sync/internal_api/sync_rollback_manager.cc?r1=285229&r2=285228&pathrev=285229

Fix use-after-free in sync backup/rollback manager.

Shouldn't use member variable if initialization fails because
SyncBackendHostCore would destroy sync manager when receiving
failure notification.

BUG=395410

Review URL: https://codereview.chromium.org/407093009
-----------------------------------------------------------------

### bu...@chromium.org (2014-07-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ff2f683f3cd8fa8cb594f94b5af813f25ba34f42

commit ff2f683f3cd8fa8cb594f94b5af813f25ba34f42
Author: haitaol@chromium.org <haitaol@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Thu Jul 24 13:34:49 2014

Fix use-after-free in sync backup/rollback manager.

Shouldn't use member variable if initialization fails because
SyncBackendHostCore would destroy sync manager when receiving
failure notification.

BUG=395410

Review URL: https://codereview.chromium.org/407093009

git-svn-id: svn://svn.chromium.org/chrome/trunk/src@285229 0039d316-1c4b-4281-b951-d872f2087c98



### [Deleted User] (2014-07-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-07-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2014-07-25)

merge approved for m37 branch 2062

### bu...@chromium.org (2014-07-25)

------------------------------------------------------------------
r285665 | haitaol@chromium.org | 2014-07-25T20:38:44.442542Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/sync/internal_api/sync_rollback_manager.cc?r1=285665&r2=285664&pathrev=285665
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/sync/internal_api/sync_rollback_manager_base_unittest.cc?r1=285665&r2=285664&pathrev=285665
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/sync/internal_api/sync_rollback_manager_base.cc?r1=285665&r2=285664&pathrev=285665
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/sync/internal_api/sync_backup_manager.cc?r1=285665&r2=285664&pathrev=285665
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/sync/internal_api/sync_rollback_manager_base.h?r1=285665&r2=285664&pathrev=285665

Merge 285229 "Fix use-after-free in sync backup/rollback manager."

> Fix use-after-free in sync backup/rollback manager.
> 
> Shouldn't use member variable if initialization fails because
> SyncBackendHostCore would destroy sync manager when receiving
> failure notification.
> 
> BUG=395410
> 
> Review URL: https://codereview.chromium.org/407093009

TBR=haitaol@chromium.org

Review URL: https://codereview.chromium.org/417273003
-----------------------------------------------------------------

### bu...@chromium.org (2014-07-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8e6fa57a97443e33d9679f6bad6f16f272cdea0b

commit 8e6fa57a97443e33d9679f6bad6f16f272cdea0b
Author: haitaol@chromium.org <haitaol@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Fri Jul 25 20:38:44 2014

Merge 285229 "Fix use-after-free in sync backup/rollback manager."

> Fix use-after-free in sync backup/rollback manager.
> 
> Shouldn't use member variable if initialization fails because
> SyncBackendHostCore would destroy sync manager when receiving
> failure notification.
> 
> BUG=395410
> 
> Review URL: https://codereview.chromium.org/407093009

TBR=haitaol@chromium.org

Review URL: https://codereview.chromium.org/417273003

git-svn-id: svn://svn.chromium.org/chrome/branches/2062/src@285665 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-07-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/aa41c8209a18509e3e4b537434b1f518cfd848ac

commit aa41c8209a18509e3e4b537434b1f518cfd848ac
Author: haitaol@chromium.org <haitaol@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Fri Jul 25 21:51:12 2014

Revert 285665 "Merge 285229 "Fix use-after-free in sync backup/r..."

> Merge 285229 "Fix use-after-free in sync backup/rollback manager."
> 
> > Fix use-after-free in sync backup/rollback manager.
> > 
> > Shouldn't use member variable if initialization fails because
> > SyncBackendHostCore would destroy sync manager when receiving
> > failure notification.
> > 
> > BUG=395410
> > 
> > Review URL: https://codereview.chromium.org/407093009
> 
> TBR=haitaol@chromium.org
> 
> Review URL: https://codereview.chromium.org/417273003

TBR=haitaol@chromium.org

Review URL: https://codereview.chromium.org/420713006

git-svn-id: svn://svn.chromium.org/chrome/branches/2062/src@285692 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-07-25)

------------------------------------------------------------------
r285692 | haitaol@chromium.org | 2014-07-25T21:51:12.489528Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/sync/internal_api/sync_rollback_manager_base.cc?r1=285692&r2=285691&pathrev=285692
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/sync/internal_api/sync_backup_manager.cc?r1=285692&r2=285691&pathrev=285692
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/sync/internal_api/sync_rollback_manager_base.h?r1=285692&r2=285691&pathrev=285692
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/sync/internal_api/sync_rollback_manager.cc?r1=285692&r2=285691&pathrev=285692
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/sync/internal_api/sync_rollback_manager_base_unittest.cc?r1=285692&r2=285691&pathrev=285692

Revert 285665 "Merge 285229 "Fix use-after-free in sync backup/r..."

> Merge 285229 "Fix use-after-free in sync backup/rollback manager."
> 
> > Fix use-after-free in sync backup/rollback manager.
> > 
> > Shouldn't use member variable if initialization fails because
> > SyncBackendHostCore would destroy sync manager when receiving
> > failure notification.
> > 
> > BUG=395410
> > 
> > Review URL: https://codereview.chromium.org/407093009
> 
> TBR=haitaol@chromium.org
> 
> Review URL: https://codereview.chromium.org/417273003

TBR=haitaol@chromium.org

Review URL: https://codereview.chromium.org/420713006
-----------------------------------------------------------------

### bu...@chromium.org (2014-07-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2ef962fb17bbc3b87a9a92f10910c38edeca3c44

commit 2ef962fb17bbc3b87a9a92f10910c38edeca3c44
Author: haitaol@chromium.org <haitaol@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Fri Jul 25 22:02:18 2014

Merge 285229 "Fix use-after-free in sync backup/rollback manager."

> Fix use-after-free in sync backup/rollback manager.
> 
> Shouldn't use member variable if initialization fails because
> SyncBackendHostCore would destroy sync manager when receiving
> failure notification.
> 
> BUG=395410
> 
> Review URL: https://codereview.chromium.org/407093009

TBR=haitaol@chromium.org

Review URL: https://codereview.chromium.org/423503004

git-svn-id: svn://svn.chromium.org/chrome/branches/2062/src@285698 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-07-25)

------------------------------------------------------------------
r285698 | haitaol@chromium.org | 2014-07-25T22:02:18.117430Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/sync/internal_api/sync_backup_manager.cc?r1=285698&r2=285697&pathrev=285698
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/sync/internal_api/sync_rollback_manager_base.h?r1=285698&r2=285697&pathrev=285698
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/sync/internal_api/sync_rollback_manager.cc?r1=285698&r2=285697&pathrev=285698
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/sync/internal_api/sync_rollback_manager_base_unittest.cc?r1=285698&r2=285697&pathrev=285698
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/sync/internal_api/sync_rollback_manager_base.cc?r1=285698&r2=285697&pathrev=285698

Merge 285229 "Fix use-after-free in sync backup/rollback manager."

> Fix use-after-free in sync backup/rollback manager.
> 
> Shouldn't use member variable if initialization fails because
> SyncBackendHostCore would destroy sync manager when receiving
> failure notification.
> 
> BUG=395410
> 
> Review URL: https://codereview.chromium.org/407093009

TBR=haitaol@chromium.org

Review URL: https://codereview.chromium.org/423503004
-----------------------------------------------------------------

### mb...@chromium.org (2014-08-28)

attekett, therealholden: This was a bit of an unusual case. This crash didn't show up for any of our fuzzers, but it did with both of yours. We decided to issue a $1000 reward to each of you.

Thanks for the fuzzer contributions!

### ti...@chromium.org (2014-09-18)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-09-18)

Note to future self: Paying 2 x $1000 for this bug.

### ti...@google.com (2014-10-07)

therealholden: Processing via our e-payment system can take a few weeks, but reward should be on its way to you. Thanks again for your help!

### ti...@google.com (2014-10-07)

attekett: Processing via our e-payment system can take a few weeks, but reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2014-10-30)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/395410?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080080)*
