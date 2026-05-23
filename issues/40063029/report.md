# Security: Possible UAF in PinManager::NotifyDelete

| Field | Value |
|-------|-------|
| **Issue ID** | [40063029](https://issues.chromium.org/issues/40063029) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Shell |
| **Platforms** | ChromeOS |
| **Reporter** | zh...@gmail.com |
| **Assignee** | ha...@google.com |
| **Created** | 2023-02-11 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

Precondition: bulk-pinning is enabled.

When deleting a directory recursively in DriveFS, function drive::internal::DeleteOperation::Delete will post a task to UI thread from IO thread. The task has a bound raw pointer to PinManager [0].

```
void Delete() {  
  base::File::Error error = base::DeletePathRecursively(path_)  
                                ? base::File::FILE_OK  
                                : base::File::FILE_ERROR_FAILED;  
  if (error == base::File::FILE_OK && drive_) {  
    using drivefs::pinning::PinManager;  
    if (PinManager\* const pin_manager = drive_->GetPinManager()) {  
      // TODO(b/267225898): Local delete events are currently not sent via  
      // DriveFS, so for now notify the `PinManager` for local deletes.  
      content::GetUIThreadTaskRunner({})->PostTask(          // <---- [0]  
          FROM_HERE, base::BindOnce(&PinManager::NotifyDelete,  
                                    base::Unretained(pin_manager),  
                                    PinManager::Id(stable_id_), drive_path_));  
    }  
  }  
  
  ...  
}  

```

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ash/drive/fileapi/drivefs_async_file_util.cc;l=239-242;drc=b7fcea93b3ee24beb19e0bb2a5fbde4f83b484d1>

This is unsafe because every time DriveFS mounted, PinManager instance would be recreated in |DriveIntegrationService::OnMounted| [1]. The previous PinManager instance might get destroyed before the scheduled task is executed. As a result, `PinManager::NotifyDelete` would access freed memory.

```
void DriveIntegrationService::OnMounted(const base::FilePath& mount_path) {  
  ...  
  
  if (ash::features::IsDriveFsBulkPinningEnabled()) {  
    pin_manager_ = std::make_unique<drivefs::pinning::PinManager>(  
        profile_->GetPath(), GetDriveFsInterface());          // <---- [1]  
  }  
}  

```

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ash/drive/drive_integration_service.cc;l=1082;drc=3ddb2d68ccf2ff0f5b11064ad9ca58ba9ebe49bd>

<https://source.chromium.org/chromium/chromium/src/+/main:chromeos/ash/components/drivefs/drivefs_pin_manager.cc;l=841-853;drc=aac51605c2403af35ddf6f73d47c860a0ba4e5ba>

After some digging around in the source code, it looks like the DriveFS can be remounted.

1. Settings page -> Files -> Disconnect Google Drive account, toggle this option several times will cause DriveFS remounted.
2. In the webui chrome://drive-internals/, run chrome.send("restartDrive") in console or click "Restart Drive" button.

**VERSION**  

Chrome Version: head  

Operating System: ChromeOS  

CL: <https://chromium-review.googlesource.com/c/chromium/src/+/4216533>

**REPRODUCTION CASE**  

This problem was found by code review and DriveFS is not avaiable for me. However, I think following steps can reproduce the problem reliably.

1. Apply drivefs\_async\_file\_util.patch, which adds sleep(10) in the DeleteOperation::Delete function running on IO thread
2. Visit the attach test.html page, click and select a directory from DriveFS. Or delete a test directory in drive fs manually.
3. In 10 seconds, open page chrome://drive-internals/, run chrome.send("restartDrive") in console or click "Restart Drive" button.
4. Wait the task run and UAF.

Steps without patch, may not work:

1. Open page chrome://drive-internals/, run in console: f = function() { chrome.send('restartDrive'); setTimeout(f, 1000);}; f()
2. Visit the attach test.html page, click and select a directory from DriveFS.

## Attachments

- [test.html](attachments/test.html) (text/plain, 614 B)
- [drivefs_async_file_util.patch](attachments/drivefs_async_file_util.patch) (text/plain, 745 B)

## Timeline

### [Deleted User] (2023-02-11)

[Empty comment from Monorail migration]

### zh...@gmail.com (2023-02-11)

Addition information: run chromeos with --enable-features=DriveFsBulkPinning which enable bulk-pinning feature.

### zh...@gmail.com (2023-02-14)

[Empty comment from Monorail migration]

### zh...@gmail.com (2023-02-21)

Hi François Degro, 
It seems that Ben was OoO, could you please take a look? 

### fd...@chromium.org (2023-02-21)

Thanks for the report. I'm going to look at it.

### gi...@appspot.gserviceaccount.com (2023-02-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/37c460626a81e6b42a3a6e1dbe997557cb0fc959

commit 37c460626a81e6b42a3a6e1dbe997557cb0fc959
Author: François Degros <fdegros@chromium.org>
Date: Tue Feb 21 05:35:44 2023

PinManager: Use WeakPtr<PinManager> in DeleteOperation.

BUG=chromium:1415008
TEST=Manual testing

Change-Id: Ib756a393e22493da6a6a210ae3f29e6a124a9ebb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4274026
Reviewed-by: Marcello Salomao <msalomao@google.com>
Commit-Queue: Marcello Salomao <msalomao@google.com>
Commit-Queue: François Degros <fdegros@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1107599}

[modify] https://crrev.com/37c460626a81e6b42a3a6e1dbe997557cb0fc959/chrome/browser/ash/drive/fileapi/drivefs_async_file_util.cc
[modify] https://crrev.com/37c460626a81e6b42a3a6e1dbe997557cb0fc959/chromeos/ash/components/drivefs/drivefs_pin_manager.h


### zh...@gmail.com (2023-02-21)

Thanks for the quick fix. I noticed that there was an unresolved comment from Marcello: https://chromium-review.googlesource.com/c/chromium/src/+/4274026/comment/a79ba32c_21556256/. AFAIK, I think we can avoid Marcello's concern by post task bounding with profile_ instead of pin_manager_. For example, https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ash/smb_client/fileapi/smbfs_async_file_util.cc;l=115-117;drc=02e49e5898180f197b59994ba71f45fb9d1c884c .

My fix suggestion, hasn't compiled yet, hope it help :)

diff --git a/chrome/browser/ash/drive/fileapi/drivefs_async_file_util.cc b/chrome/browser/ash/drive/fileapi/drivefs_async_file_util.cc
index 39792533268d3..9eff3a81ce85c 100644
--- a/chrome/browser/ash/drive/fileapi/drivefs_async_file_util.cc
+++ b/chrome/browser/ash/drive/fileapi/drivefs_async_file_util.cc
@@ -235,15 +235,12 @@ class DeleteOperation {
 
     if (deleted) {
       VLOG(1) << "Deleted '" << path_ << "'";
-      DCHECK(drive_);
-      if (PinManager* const pin_manager = drive_->GetPinManager()) {
-        // TODO(b/267225898): Local delete events are currently not sent via
-        // DriveFS, so for now notify the `PinManager` for local deletes.
-        content::GetUIThreadTaskRunner({})->PostTask(
-            FROM_HERE,
-            base::BindOnce(&PinManager::NotifyDelete, pin_manager->GetWeakPtr(),
-                           id_, drive_path_));
-      }
+      // TODO(b/267225898): Local delete events are currently not sent via
+      // DriveFS, so for now notify the `PinManager` for local deletes.
+      content::GetUIThreadTaskRunner({})->PostTask(
+          FROM_HERE,
+          base::BindOnce(&DeleteOperation::NotifyPinManagerDeleteOnUIThread,
+                         profile_, id_, drive_path_));
     } else {
       LOG(ERROR) << "Cannot delete '" << path_ << "'";
     }
@@ -255,6 +252,17 @@ class DeleteOperation {
     origin_task_runner_->DeleteSoon(FROM_HERE, this);
   }
 
+  static void NotifyPinManagerDeleteOnUIThread(
+      Profile* profile,
+      PinManager::Id id,
+      const base::FilePath& drive_path) {
+    auto drive = drive::util::GetIntegrationServiceByProfile(profile);
+    DCHECK(drive);
+    if (PinManager* const pin_manager = drive->GetPinManager()) {
+      pin_manager->NotifyDelete(id, drive_path);
+    }
+  }
+
   Profile* const profile_;
   const base::FilePath path_;
   base::FilePath drive_path_;


### fd...@chromium.org (2023-02-21)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-02-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3ebc8d4f78ee65fbded8518ae908424d83f3a70b

commit 3ebc8d4f78ee65fbded8518ae908424d83f3a70b
Author: François Degros <fdegros@chromium.org>
Date: Wed Feb 22 03:59:57 2023

DriveFsAsyncFileUtil: Ensure PinManager is retrieved in UI thread

BUG=chromium:1415008
TEST=Manual testing

Change-Id: I2251240df4a1afafe53db93de3d8a4c02f5c8644
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4279063
Commit-Queue: François Degros <fdegros@chromium.org>
Reviewed-by: Marcello Salomao <msalomao@google.com>
Cr-Commit-Position: refs/heads/main@{#1108153}

[modify] https://crrev.com/3ebc8d4f78ee65fbded8518ae908424d83f3a70b/chrome/browser/ash/drive/drive_integration_service.cc
[modify] https://crrev.com/3ebc8d4f78ee65fbded8518ae908424d83f3a70b/chrome/browser/ash/drive/drive_integration_service.h
[modify] https://crrev.com/3ebc8d4f78ee65fbded8518ae908424d83f3a70b/chrome/browser/ash/drive/fileapi/drivefs_async_file_util.cc


### fd...@chromium.org (2023-02-22)

[Empty comment from Monorail migration]

### fd...@chromium.org (2023-02-22)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-02-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/79d5a4156eec068441d69c51025567f96b6b129f

commit 79d5a4156eec068441d69c51025567f96b6b129f
Author: François Degros <fdegros@chromium.org>
Date: Wed Feb 22 07:52:09 2023

DriveFsAsyncFileUtil: Use RefCounted operations

This simplifies and automates memory management, by avoiding a bunch of
base::Unretained(this).

BUG=chromium:1415008
TEST=Manual testing

Change-Id: I1068826124da7277105f29fefc850ba044c22413
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4278913
Reviewed-by: Marcello Salomao <msalomao@google.com>
Commit-Queue: François Degros <fdegros@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1108201}

[modify] https://crrev.com/79d5a4156eec068441d69c51025567f96b6b129f/chrome/browser/ash/drive/fileapi/drivefs_async_file_util.cc


### [Deleted User] (2023-02-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-22)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-02-24)

removing incorrect SI label 

### am...@chromium.org (2023-02-24)

adding ChromeOS security to verify security severity 

### am...@chromium.org (2023-02-24)

[Comment Deleted]

### am...@chromium.org (2023-02-24)

[Empty comment from Monorail migration]

[Monorail components: UI>Shell]

### am...@chromium.org (2023-02-24)

Hello Chaobin Zhang (OP), when submitting security bugs, thanks for your attempts to assist here, but please do not endeavor to add and adjust security labels. All security bugs should go through security triage by the appropriate security team. Security labels impact our security and release processes and should be set by Chrome browser or ChromeOS security sheriffs. Thank you for your assistance!

### zh...@gmail.com (2023-02-24)

Oops, that's my fault. Thank you for your reminder, I will pay attention next time. 

### ha...@google.com (2023-02-24)

Looks like a typical memory corruption issue. Will try to reproduce this.

Looks like the feature is behind the flags as well. 

The reporter provides a bisect. Marking it as medium security based on the guidelines.  (May turn it down to low if I cannot reporoduce)

Impact - None because the bug is only preset in ToT. 112 branch happened just yesterday.






### ha...@google.com (2023-02-27)

Talked to the developer. There is no way the feature could have been enabled by the user and the feature itself is under development. If anything,  I would categorize this as a highly mitigated UAF right now,  I would say. Therefore, moving it to a low severity bug. 

### am...@google.com (2023-03-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-02)

Congratulations Chaobin Zhang! The VRP Panel has decided to award you $1,000 for this report of a highly mitigated bug. Thank you for your efforts and reporting this issue to us! 

### zh...@gmail.com (2023-03-03)

Thanks for the reward! 

### am...@google.com (2023-03-03)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-05-31)

This issue was migrated from crbug.com/chromium/1415008?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063029)*
