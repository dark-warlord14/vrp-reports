# Security: Use-After-Free in safe_browsing::ExtensionTelemetryPersister::InitHelper

| Field | Value |
|-------|-------|
| **Issue ID** | [40059914](https://issues.chromium.org/issues/40059914) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Linux |
| **Reporter** | et...@gmail.com |
| **Assignee** | ps...@google.com |
| **Created** | 2022-06-10 |
| **Bounty** | $10,000.00 |

## Description

**Steps to reproduce the problem:**  

[0] Download linux-release\_asan-linux-release-1012365.zip from <https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-release-1012377.zip?generation=1654763766078992&alt=media>

[1] python3 -m http.server 8000

[2] Settings→Security→Safe Browsing→enable Enhanced protection

[3] Make sure the folder `/tmp/xxx/CRXTelemetry` is big enough or deep enough that it takes a long time to delete it.(\*\*Note that this is only to increase the race window, you can also add sleep in the InitHelper to omit this step, please apply repro\_vuln.diff patch\*\*)

[3] Run: `/path/to/linux-release_asan-linux-release-1012365/asan-linux-release-1012365/chrome-wrapper --user-data-dir=/tmp/xxx --enable-features=SafeBrowsingExtensionTelemetry,SafeBrowsingExtensionTelemetryPersistence http://127.0.0.1:8000/poc.html`

If all goes well, you should see a browser close the moment it is opened, then trigger the UAF.  

You can also adjust the poc to set the SetTimeout

Note that this vulnerability function is not only called when the browser is opened, you can trigger it by enabling Enhanced protection.  

Also similar usages in this file have bugs, please read on for bug reports, they happen in many different places.  

I also triggered another vulnerability and provided ASAN.（ref: asan\_write\_report.txt)  

Here are just the steps to reproduce the vulnerable functions that are easiest to trigger.

**Problem Description:**  

[0] ExtensionTelemetryPersister is owned by ExtensionTelemetryService, which derived from KeyedSerive, and will be release after the browser closed.

[1] The InitHelper task with weak\_factory\_.GetWeakPtr() is posted to ThreadPool (a separate sequence) in ExtensionTelemetryPersister::PersisterInit，but WeakPtrs are \*\*not\*\* safe to use across multiple threads.

[2] ExtensionTelemetryPersister may be destroyed on the UI thread while InitHelper is running，because InitHelper will perform some file IO operations, such as the recursive deletion of the old\_dir directory here(eg: if --user-data-dir=/tmp/xxx, then old\_dir is /tmp/xxx/CRXTelemetry).

[3] Since ExtensionTelemetryPersister has been released at this time, accessing write\_index\_ will trigger UAF.

```
class ExtensionTelemetryService : public KeyedService { //-->[0]  
	...  
	std::unique_ptr<safe_browsing::ExtensionTelemetryPersister> persister_;  
}  
...  
void ExtensionTelemetryService::SetEnabled(bool enable) {  
	...  
	if (base::FeatureList::IsEnabled(kExtensionTelemetryPersistence)) {  
	    persister_ = std::make_unique<ExtensionTelemetryPersister>(kMaxNumFilesPersisted, profile_); //--->[0]  
}  

```
```
void ExtensionTelemetryPersister::PersisterInit() {  
  base::ThreadPool::PostTask(  
      FROM_HERE, base::MayBlock(),  
      base::BindOnce(&ExtensionTelemetryPersister::InitHelper,  
                     weak_factory_.GetWeakPtr())); //--->[1]  
}  

```
```
void ExtensionTelemetryPersister::InitHelper() {  
  // TODO(https://crbug.com/1325864): Remove old directory clean up code after  
  // launch.  
  base::FilePath old_dir;  
  if (base::PathService::Get(chrome::DIR_USER_DATA, &old_dir)) {  
    old_dir = old_dir.AppendASCII("CRXTelemetry");  
    if (base::DirectoryExists(old_dir)) {  
      base::DeletePathRecursively(old_dir); //--->[2]  
    }  
  }  
  write_index_ = kInitialWriteIndex;//--->[3]  
  ...  
}  

```

[0] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/safe_browsing/extension_telemetry/extension_telemetry_service.h;l=127;drc=2e15a0e74d1dfcd7a8f6f71b2fc5eea6019cbe25>

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/safe_browsing/extension_telemetry/extension_telemetry_persister.cc;l=77;drc=2e15a0e74d1dfcd7a8f6f71b2fc5eea6019cbe25>

[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/safe_browsing/extension_telemetry/extension_telemetry_persister.cc;l=127;drc=2e15a0e74d1dfcd7a8f6f71b2fc5eea6019cbe25>

[3] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/safe_browsing/extension_telemetry/extension_telemetry_persister.cc;l=130;drc=2e15a0e74d1dfcd7a8f6f71b2fc5eea6019cbe25>

**Additional Comments:**

1. ExtensionTelemetryPersister::ClearPersistedFiles
2. ExtensionTelemetryPersister::ReadReport
3. ExtensionTelemetryPersister::WriteReport

These functions also use the TaskRunner based thread pool , which has similar vulnerabilities and should be fixed as well.

An asan log of ExtensionTelemetryPersister::WriteReport is attached here as additional proof. refer to asan\_write\_report.txt

\*\*Since this has multiple paths that could lead to different UAFs, this could be a serious bug, please fix it soon.\*\*

\*\*Chrome version: \*\* 104.0.5095.0 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 75 B)
- [asan.txt](attachments/asan.txt) (text/plain, 16.5 KB)
- [asan_write_report.txt](attachments/asan_write_report.txt) (text/plain, 18.9 KB)
- [repro1.mp4](attachments/repro1.mp4) (video/mp4, 8.9 MB)
- [repro.mp4](attachments/repro.mp4) (video/mp4, 10.9 MB)
- [repro_vuln.diff](attachments/repro_vuln.diff) (text/plain, 646 B)

## Timeline

### et...@gmail.com (2022-06-10)

Add attachments, including a symbol asan reproduction video, and a vulnerability reproduce patch (add sleep in bug function)

### dt...@chromium.org (2022-06-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-10)

[Empty comment from Monorail migration]

### et...@gmail.com (2022-06-11)

[0] The introduction of this vulnerability occurred in this commit on 2022.3.24
https://source.chromium.org/chromium/chromium/src/+/973a635d30a6ed39b32b4ad2083fad599a4fa686

[1] Interestingly, this module seems to have been fixed once with the race condition UAF, but not completely.
https://source.chromium.org/chromium/chromium/src/+/da02810424c82178d61a5a054ea55a06cff75064

[2] And in this submission on 2022.5.24, the read and write file operations in the thread pool were introduced, which greatly increased the race window and greatly increased the probability of UAF triggering on slow CPUs.
https://source.chromium.org/chromium/chromium/src/+/fa2556d6e43c9db1f568b8e83607eebfbb787c98

### et...@gmail.com (2022-06-11)

[Comment Deleted]

### et...@gmail.com (2022-06-11)

In addition, here I will explain the UAF in ExtensionTelemetryPersister::WriteReport additionally. Since you have fixed a race condition UAF in SaveFile[1], I will not explain more about this race window. I believe it is possible.

Here I explain task_runner_ [0], since task_runner_ is created by ThreadPool::CreateSequencedTaskRunner, task_runner_->PostTask will post a task to the thread pool.
The possible question here is TaskShutdownBehavior::CONTINUE_ON_SHUTDOWN, according to [this documentation](https://source.chromium.org/chromium/chromium/src/+/main:docs/shutdown.md#step-3-joining-other-threads)
-->
```
ThreadPool shutdown starts. At this point, no new SKIP_ON_SHUTDOWN or CONTINUE_ON_SHUTDOWN task can start running (they are deleted without running). The main thread blocks until all SKIP_ON_SHUTDOWN tasks that started running prior to ThreadPool shutdown start are complete, and all BLOCK_SHUTDOWN tasks are complete (irrespective of whether they were posted before or after ThreadPool shutdown start). When no more SKIP_ON_SHUTDOWN is running and no more BLOCK_SHUTDOWN task is queued or running, the main thread is unblocked and ThreadPool shutdown is considered complete. Note: CONTINUE_ON_SHUTDOWN tasks that started before ThreadPool shutdown may still be running.
```

Only the task of SKIP_ON_SHUTDOWN will block the ThreadPool shutdown. If there is only the ExtensionTelemetryPersister::SaveFile CONTINUE_ON_SHUTDOWN task in the thread pool, then even if the ExtensionTelemetryPersister::SaveFile is running, the ThreadPool will shut down, which will not cause the UAF to be triggered.

So here I send a large number of SKIP_ON_SHUTDOWN tasks to other thread pool task runner. At this time, the thread pool includes the SKIP_ON_SHUTDOWN task and the ExtensionTelemetryPersister::SaveFile CONTINUE_ON_SHUTDOWN task. At this time, the shutdown of the thread pool is blocked, thus ensuring that the UAF can be triggered.

```
ExtensionTelemetryPersister::ExtensionTelemetryPersister(int max_num_files,
                                                         Profile* profile)
    : profile_(profile), max_num_files_(max_num_files) {
  // Shutdown behavior is CONTINUE_ON_SHUTDOWN to ensure tasks
  // are run on the threads they were called on.
  task_runner_ = base::ThreadPool::CreateSequencedTaskRunner( //---->[0]
      {base::MayBlock(), base::TaskPriority::BEST_EFFORT,
       base::TaskShutdownBehavior::CONTINUE_ON_SHUTDOWN});
}


void ExtensionTelemetryPersister::WriteReport(const std::string write_string) {
  if (initialization_complete_ && !is_shut_down_) {
    task_runner_->PostTask( //--->[0]
        FROM_HERE,
        base::BindOnce(&ExtensionTelemetryPersister::SaveFile,//--->[1]
                       weak_factory_.GetWeakPtr(), std::move(write_string)));
  }
}

void ExtensionTelemetryPersister::SaveFile(std::string write_string) {//---->[1]
  if (!base::DirectoryExists(dir_path_)) { 
    base::CreateDirectory(dir_path_);
    write_index_ = kInitialWriteIndex;
    read_index_ = kInitialReadIndex;
  }
  base::FilePath path = dir_path_.AppendASCII(
      ("CRXTelemetry_" + base::NumberToString(write_index_)));
  bool success = base::WriteFile(path, write_string);
  if (success) {
    write_index_++;
    if (write_index_ - 1 > read_index_)
      read_index_ = write_index_ - 1;
    if (write_index_ >= max_num_files_)
      write_index_ = 0;
  }
  RecordWriteResult(success);
}
```



### ye...@google.com (2022-06-13)

Thanks for your report! Assigning the severity as critical because extension telemetry runs in the browser.
psarouthakis@ please take a look, the reporter highlighted some commits that introduced this bug.

[Monorail components: Services>Safebrowsing]

### [Deleted User] (2022-06-13)

[Empty comment from Monorail migration]

### ye...@google.com (2022-06-13)

Messed up FoundIn, should be 102 as the change was introduced in March.

### [Deleted User] (2022-06-13)

[Empty comment from Monorail migration]

### an...@google.com (2022-06-13)

[Empty comment from Monorail migration]

### ye...@google.com (2022-06-13)

Changing this to high severity, users would have to set a few flags and the PoC uses window.close().

### [Deleted User] (2022-06-14)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ps...@google.com (2022-06-15)

[Empty comment from Monorail migration]

### an...@chromium.org (2022-06-15)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-06-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a8c9672ab894bf904cef2ff5c18dd3e077456b2b

commit a8c9672ab894bf904cef2ff5c18dd3e077456b2b
Author: Adam Psarouthakis <psarouthakis@google.com>
Date: Tue Jun 28 16:56:48 2022

Fix Use-After-Free in Persister

Fixed the use of weak factory pointers trying to access destroyed
objects on different threads. The fix involves using SequenceBound
on the object to ensure that the tasks the object are running and
the object itself are running on the same thread.

Bug: 1335316
Change-Id: I3efa2c900aa6b0cf7bfcd7f92799c4fb4a3d20d8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3715835
Reviewed-by: Xinghui Lu <xinghuilu@chromium.org>
Commit-Queue: Adam Psarouthakis <psarouthakis@google.com>
Cr-Commit-Position: refs/heads/main@{#1018734}

[modify] https://crrev.com/a8c9672ab894bf904cef2ff5c18dd3e077456b2b/chrome/browser/safe_browsing/extension_telemetry/extension_telemetry_persister_unittest.cc
[modify] https://crrev.com/a8c9672ab894bf904cef2ff5c18dd3e077456b2b/chrome/browser/safe_browsing/extension_telemetry/extension_telemetry_persister.h
[modify] https://crrev.com/a8c9672ab894bf904cef2ff5c18dd3e077456b2b/chrome/browser/safe_browsing/extension_telemetry/extension_telemetry_persister.cc
[modify] https://crrev.com/a8c9672ab894bf904cef2ff5c18dd3e077456b2b/chrome/browser/safe_browsing/extension_telemetry/extension_telemetry_service.cc
[modify] https://crrev.com/a8c9672ab894bf904cef2ff5c18dd3e077456b2b/chrome/browser/safe_browsing/extension_telemetry/extension_telemetry_service.h
[modify] https://crrev.com/a8c9672ab894bf904cef2ff5c18dd3e077456b2b/chrome/browser/safe_browsing/extension_telemetry/extension_telemetry_service_unittest.cc


### ps...@google.com (2022-06-29)

[Empty comment from Monorail migration]

### ps...@google.com (2022-06-29)

https://chromium-review.googlesource.com/c/chromium/src/+/3715835

This CL switched the the persister from using its own task runner, to utilizing sequence bound to ensure that the posted tasks and the persister object are always on the same thread. 

### [Deleted User] (2022-06-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-29)

Requesting merge to extended stable M102 because latest trunk commit (1018734) appears to be after extended stable branch point (992738).

Requesting merge to stable M103 because latest trunk commit (1018734) appears to be after stable branch point (1002911).

Requesting merge to beta M104 because latest trunk commit (1018734) appears to be after beta branch point (1012729).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-29)

Merge review required: M104 is already shipping to beta.

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
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-29)

Merge review required: M103 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-29)

Merge review required: M102 is already shipping to stable.

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

### ps...@google.com (2022-06-30)

Commits: https://chromium-review.googlesource.com/c/chromium/src/+/3715835

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
  My changes will prevent crashes present in the Extension Telemetry Service which is planned to release in 104
2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/chromium/src/+/3715835
3. Have the changes been released and tested on canary?
Not the changes in the gerrit I linked above. But they have been locally tested and verified and worked as expected.
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
Yes it is a new feature and yes it is behind a finch flag
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
N/A
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
N/A. Testing is covered by automated tests.

One other note is that this bug was first identify in code that dates back to 102, however the finch flag prevents any users running 102 and 103 releases from touching the code. 104 is the only branch currently in the release pipeline will have users experiencing the Extension Telemetry Persister

### ps...@google.com (2022-07-01)

[Comment Deleted]

### ps...@google.com (2022-07-01)

I have monitored Canary since the merge of the CL to ensure that no unexpected crashes occurred and built a local canary branch to test ensuring the bug mentioned in this ticket does not occur. This bug was an edge case which should not affect any of the ExtensionTelemetryServices metrics for performance.  All the code related to the bug is also protected by a finch flag.

### ps...@google.com (2022-07-06)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-07-06)

Congratulations! The VRP Panel has decided to award you $10,000 for this report. The reward amount was decided upon due to the tight preconditions to trigger this issue and also being a shutdown bug; however this a very thorough and detailed report, providing exceptional analysis and clear demonstration of this issue. Thank you for your efforts and reporting this issue to us - great work! 

### et...@gmail.com (2022-07-07)

thanks :)

### ps...@google.com (2022-07-07)

Hello srinivassista@google.com,
I was wondering if you could take a look at this merge request. https://crbug.com/chromium/1335316#c25 and #27 answer the requested merge questions. 

### am...@chromium.org (2022-07-07)

Hi Adam, thanks for pinging us. I put merge reviews on hold given this was originally a release freeze week and we were working around the release plans for the emergency release that went out on Monday and beta follow up from that. Merge approved for 104, please merge this fix to branch 5112 at your earliest convenience. 

### [Deleted User] (2022-07-07)

Merge review required: M104 is already shipping to beta.

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
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-07)

Follow up qq, I've noticed in https://crbug.com/chromium/1335316#c28 the merge labels for stable 103 and extended stable 102 have been removed. Is there a complexity or other concern with merging this back. AIUI, this code is shipping to some stable users via Finch experimentation. If that is correct, we should definitely consider merging back this fix to ES and stable for the next planned security respins on 19 July. 

### ps...@google.com (2022-07-07)

Thanks for the review! We planned to only merging back to 104 as that is the earliest the code would be released. The Extension Telemetry Service has a finch experiment but only beta/dev/canary users are included currently. After the code is merged the GCL file that controls the finch experiment will be updated to ensure that only users with 104+ chrome versions are being served content which will prevent this issue on any 102/103 releases crashing anymore.

### ps...@google.com (2022-07-07)

I should also mention that users in the current beta finch experiment group cannot experience the bug as the persistence code is guarded behind an additional finch flag that is only open to Dev/Canary channels at the moment. 

### am...@google.com (2022-07-08)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-08)

Thank you for the context. Leaving this as just to be merged/merge approved to M104 then. Thanks! 

### [Deleted User] (2022-07-11)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-07-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d11e4dbffae12e134f28c23c8650db756b5d0e80

commit d11e4dbffae12e134f28c23c8650db756b5d0e80
Author: Adam Psarouthakis <psarouthakis@google.com>
Date: Mon Jul 11 22:43:52 2022

[104]Fix Use-After-Free in Persister

Fixed the use of weak factory pointers trying to access destroyed
objects on different threads. The fix involves using SequenceBound
on the object to ensure that the tasks the object are running and
the object itself are running on the same thread.

(cherry picked from commit a8c9672ab894bf904cef2ff5c18dd3e077456b2b)

Bug: 1335316
Change-Id: I3efa2c900aa6b0cf7bfcd7f92799c4fb4a3d20d8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3715835
Reviewed-by: Xinghui Lu <xinghuilu@chromium.org>
Commit-Queue: Adam Psarouthakis <psarouthakis@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1018734}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3738780
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Xinghui Lu <xinghuilu@chromium.org>
Auto-Submit: Adam Psarouthakis <psarouthakis@google.com>
Cr-Commit-Position: refs/branch-heads/5112@{#788}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[modify] https://crrev.com/d11e4dbffae12e134f28c23c8650db756b5d0e80/chrome/browser/safe_browsing/extension_telemetry/extension_telemetry_persister_unittest.cc
[modify] https://crrev.com/d11e4dbffae12e134f28c23c8650db756b5d0e80/chrome/browser/safe_browsing/extension_telemetry/extension_telemetry_persister.h
[modify] https://crrev.com/d11e4dbffae12e134f28c23c8650db756b5d0e80/chrome/browser/safe_browsing/extension_telemetry/extension_telemetry_persister.cc
[modify] https://crrev.com/d11e4dbffae12e134f28c23c8650db756b5d0e80/chrome/browser/safe_browsing/extension_telemetry/extension_telemetry_service.cc
[modify] https://crrev.com/d11e4dbffae12e134f28c23c8650db756b5d0e80/chrome/browser/safe_browsing/extension_telemetry/extension_telemetry_service.h
[modify] https://crrev.com/d11e4dbffae12e134f28c23c8650db756b5d0e80/chrome/browser/safe_browsing/extension_telemetry/extension_telemetry_service_unittest.cc


### am...@chromium.org (2022-08-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-02)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1335316?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059914)*
