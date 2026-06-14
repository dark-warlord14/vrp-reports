# UAF In ProcessManager

| Field | Value |
|-------|-------|
| **Issue ID** | [40050562](https://issues.chromium.org/issues/40050562) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux |
| **Reporter** | le...@gmail.com |
| **Assignee** | la...@chromium.org |
| **Created** | 2019-10-29 |
| **Bounty** | $7,500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36

Steps to reproduce the problem:
1. Load the attached extension (or any other extension which contains background.service_worker in manifest.json).
2. Visit the popup.html page(or other extension's page) through clicking the extension (or page redirection).
3. Close the Browser.

What is the expected behavior?

What went wrong?
When the browser process is closed, call ProcessManager::RemoveObserver through RemoveAll to clean it up. Which is happened after ~ProcessManager().

Did this work before? N/A 

Chrome version:   Channel: n/a
OS Version: 
Flash Version:

## Attachments

- [asan](attachments/asan) (text/plain, 48.6 KB)
- [Sample_extension.zip](attachments/Sample_extension.zip) (application/octet-stream, 10.1 MB)
- [Sample_extension2.zip](attachments/Sample_extension2.zip) (application/octet-stream, 10.2 MB)
- [extension.png](attachments/extension.png) (image/png, 426.2 KB)
- [patch](attachments/patch) (text/plain, 972 B)

## Timeline

### le...@gmail.com (2019-10-29)

It may cause sandbox escape without RCE.

### li...@chromium.org (2019-10-30)

Haven't confirmed since I'm unable to load the extension due to policy. rdevlin.cronin or someone else on the extensions team, would you be able to help take a look? Thanks!

[Monorail components: Platform>Extensions]

### le...@gmail.com (2019-10-31)

I could load it by loading unpacked extension in extension developer mode.

### ka...@chromium.org (2019-10-31)

If this is only relevant for extensions with background.service_worker, then this crash should not be on Stable. Assigning to Istiaque since this is SW related.

### sh...@chromium.org (2019-11-12)

lazyboy: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@chromium.org (2019-11-22)

I can't reproduce this with the sample extension in https://crbug.com/chromium/1019161#c0, or with a simple extension with background.service_worker in manifest.json, and popup.

I see all ProcessManager::RemoveObserver calls happening before ProcessManager destruction on browser shutdown.

@leecraso, can you provide some hint on reproducing the problem?

### le...@gmail.com (2019-11-23)

You can try this new version. And it will trigger this DCHECK now: https://cs.chromium.org/chromium/src/extensions/browser/service_worker_task_queue.cc?rcl=61bf24c519a55962f6adc4881e4d59a9c594ffc3&l=174.

### la...@chromium.org (2019-11-26)

Thanks for you reply @leecraso, I'll take a look at that issue.

To clarify though: this isn't doing use-after-free based on the original report?

### le...@gmail.com (2019-11-26)

I think I made a mistake. I triggered the UAF in https://crbug.com/chromium/1019161#c0 by "Simple_extension2", but I uploaded the wrong file. "Simple_extension2" could trigger this UAF before (now also works), but "Simple_extension" cannot.

### sh...@chromium.org (2019-12-10)

lazyboy: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-12-28)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### le...@gmail.com (2020-02-17)

It seems like a long time has passed and the bug still exist in the latest version.
Can you reproduce it now or what can I do for you? ;)

### le...@gmail.com (2020-02-18)

The reason seems to be the ServiceWorkerTaskQueue[1] service which is registered[2] when the extension was added was destructed[3] later than the ProcessManager service. ~ServiceWorkerTaskQueue() will eventually call RemoveObserver and trigger UAF.

[1]https://cs.chromium.org/chromium/src/extensions/browser/task_queue_util.cc?g=0&l=80&rcl=ac01b946b29269c04e5e499137bfdd7238379a83
[2]https://cs.chromium.org/chromium/src/components/keyed_service/core/keyed_service_factory.cc?l=80&rcl=131fe11afea739154e72f430a80aa5db6fc18b6d
[3]https://cs.chromium.org/chromium/src/components/keyed_service/core/keyed_service_factory.cc?l=97&rcl=131fe11afea739154e72f430a80aa5db6fc18b6d

### le...@gmail.com (2020-02-18)

From `ServiceWorkerTaskQueue` to `RemoveObserver`[1-6]:
The PendingTask[3] with `OpenChannelParams` appears to be the key reason.

[1]https://cs.chromium.org/chromium/src/extensions/browser/service_worker_task_queue.cc?g=0&l=175&rcl=9987ca89e90d02f4c31ed1fdb21eac6125da0f70
[2]https://cs.chromium.org/chromium/src/extensions/browser/lazy_context_task_queue.h?l=53&rcl=8269a093f20adb3283259f9de27dc76e6d40cf25
[3]https://cs.chromium.org/chromium/src/extensions/browser/api/messaging/message_service.cc?l=812&rcl=7af52f528296fca3a9ffece07a2a2787545901ef
[4]https://cs.chromium.org/chromium/src/extensions/browser/api/messaging/message_service.cc?g=0&l=116&rcl=7af52f528296fca3a9ffece07a2a2787545901ef
[5]https://cs.chromium.org/chromium/src/extensions/browser/api/messaging/extension_message_port.h?g=0&l=171&rcl=221e64585cf6cbba56375dfc97b8de31062de0c4
[6]https://cs.chromium.org/chromium/src/extensions/browser/api/messaging/extension_message_port.cc?l=99&rcl=221e64585cf6cbba56375dfc97b8de31062de0c4

### le...@gmail.com (2020-02-19)

Recommended Fix: Add the edge of `ServiceWorkerTaskQueue` to `ProcessManager` in the profile dependency graph.

### cr...@chromium.org (2020-03-06)

karandeepb@: lazyboy@ seems unresponsive.  Can you re-triage and help find an owner?  (It's listed as high severity, so it's important for us to make progress on it.)  Thanks!

### rd...@chromium.org (2020-03-07)

[Empty comment from Monorail migration]

### ad...@google.com (2020-03-09)

Adding dbertoni@ for visibility since karandeepb@ says he may know stuff about this area.

### rd...@chromium.org (2020-03-09)

dbertoni's OOO at the moment.

Karan, do you think you have enough context to make progress on this, or do you need someone else to take it over?

### la...@chromium.org (2020-03-09)

Going to start looking at this today, sorry for this fell through after I last looked at it.

### ad...@google.com (2020-03-13)

lazyboy@, any news? Thanks!

### la...@chromium.org (2020-03-13)

I think I have a fix, but still working on writing test for it.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-03-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/43949bf791c4aca647073cada91a423684e04a6c

commit 43949bf791c4aca647073cada91a423684e04a6c
Author: Istiaque Ahmed <lazyboy@chromium.org>
Date: Fri Mar 20 04:42:08 2020

[Extensions] Fix couple of ProcessManager UaF issues

Worker can legitimately fail to start, this CL clears worker's
PendingTasks when that happens.

In addition to this, this CL makes ServiceWorkerTaskQueue
factory dependent on ProcessManager factory as pending tasks
can call out to ProcessManager
(courtesy of https://crbug.com/1019161#c16) upon
ServiceWorkerTaskQueue's destruction.

This CL adds a test for this ensuring a worker's pending_tasks_
is cleared when start worker failure is seen. The test rejects a
service worker's install event to trigger the failure.

Bug: 1019161
Test: See bug description for repro steps
Change-Id: I384ec0d2830f07fb3b50632ee806e77fd33b7dcb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2103306
Commit-Queue: Istiaque Ahmed <lazyboy@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#751925}

[modify] https://crrev.com/43949bf791c4aca647073cada91a423684e04a6c/chrome/browser/extensions/service_worker_apitest.cc
[modify] https://crrev.com/43949bf791c4aca647073cada91a423684e04a6c/extensions/browser/service_worker_task_queue.cc
[modify] https://crrev.com/43949bf791c4aca647073cada91a423684e04a6c/extensions/browser/service_worker_task_queue.h
[modify] https://crrev.com/43949bf791c4aca647073cada91a423684e04a6c/extensions/browser/service_worker_task_queue_factory.cc


### le...@gmail.com (2020-03-25)

Well done, I think it has been fixed. Will it be merged into M80?

### la...@chromium.org (2020-03-25)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-26)

Requesting merge to stable M80 because latest trunk commit (751925) appears to be after stable branch point (989).

Requesting merge to beta M81 because latest trunk commit (751925) appears to be after beta branch point (737173).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-03-26)

This bug requires manual review: We are only 11 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@chromium.org (2020-03-26)

Many thanks leecraso@ for you inputs to this issue! Did you check this on canary? (https://crbug.com/chromium/1019161#c26)

### le...@gmail.com (2020-03-27)

I'm sorry I only checked this fix on the latest trunk build of Chromium.

### ad...@google.com (2020-03-27)

lazyboy@ WDYT about merging this back to M80/M81? As a high severity security bug we'd normally merge this back, but only if you're extremely confident in the stability and correctness of the fix. Sheriffbot wants you to answer the questions in https://crbug.com/chromium/1019161#c30 but I'm more interested in your opinions about whether this is safe.

### la...@chromium.org (2020-03-28)

@adetaylor, I'd think the fix is safe.
However, the test I've added for this became flaky (crbug.com/1063476) for some not-so-directly related parts, and got disabled afterwards and 
then I've resubmitted fix (https://chromium-review.googlesource.com/c/chromium/src/+/2119208) for that flakiness.

### ad...@chromium.org (2020-03-28)

OK - in that case approving merge to M80 (branch 3987) and M81 (branch 4044). Please ensure there are no crash signatures in this area from canary/dev first.

### la...@chromium.org (2020-03-28)

OK, thanks, I'm looking into dev/83.0.4093.3 [1] and canary/83.0.4097.0 [2] top crashers, as I haven't heard about any crashes specific to the CL, I wasn't hoping to find anything related.

Let me know if I need to look somewhere else.

In the process of merging ~now, there's a compile issue which on the surface doesn't seem complicated: https://ci.chromium.org/p/chromium/builders/try-m81/linux-rel/47?


[1] 
https://crash.corp.google.com/browse?q=product_name%3D%27Chrome%27+AND+product.Version%3D%2783.0.4093.3%27#samplereports:45,productname:1000,productversion:30,magicsignature:100,magicsignature2:50,stablesignature:50,magicsignaturesorted:50

[2]
https://crash.corp.google.com/browse?q=product_name%3D%27Chrome%27+AND+product.Version%3D%2783.0.4097.0%27#samplereports:45,productname:1000,productversion:30,magicsignature:100,magicsignature2:50,stablesignature:50,magicsignaturesorted:50

### la...@chromium.org (2020-03-28)

Updates below as I go through merge process:

M81 merge seems OK with small conflict that seems safe to perform.
CL: https://chromium-review.googlesource.com/c/chromium/src/+/2125621/
Conflict resolution diff (safe):
https://chromium-review.googlesource.com/c/chromium/src/+/2125621/5..6

M80 merge seems a bit involved, it's not as safe as previous one, I'll keep this for the record, but won't CQ/merge this without looking further.
CL: https://chromium-review.googlesource.com/c/chromium/src/+/2125690/
Conflict resolution diff (not as safe)
https://chromium-review.googlesource.com/c/chromium/src/+/2125690/3..4

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-03-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9e150ec7eb5a30e78f63e3509a38a6ee4d0db153

commit 9e150ec7eb5a30e78f63e3509a38a6ee4d0db153
Author: Istiaque Ahmed <lazyboy@chromium.org>
Date: Sat Mar 28 08:57:07 2020

[M81] [Extensions] Fix couple of ProcessManager UaF issues

Worker can legitimately fail to start, this CL clears worker's
PendingTasks when that happens.

In addition to this, this CL makes ServiceWorkerTaskQueue
factory dependent on ProcessManager factory as pending tasks
can call out to ProcessManager
(courtesy of https://crbug.com/1019161#c16) upon
ServiceWorkerTaskQueue's destruction.

This CL adds a test for this ensuring a worker's pending_tasks_
is cleared when start worker failure is seen. The test rejects a
service worker's install event to trigger the failure.

(cherry picked from commit 43949bf791c4aca647073cada91a423684e04a6c)

Bug: 1019161
Test: See bug description for repro steps
Change-Id: I384ec0d2830f07fb3b50632ee806e77fd33b7dcb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2103306
Commit-Queue: Istiaque Ahmed <lazyboy@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#751925}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2125621
Reviewed-by: Istiaque Ahmed <lazyboy@chromium.org>
Cr-Commit-Position: refs/branch-heads/4044@{#866}
Cr-Branched-From: a6d9daf149a473ceea37f629c41d4527bf2055bd-refs/heads/master@{#737173}

[modify] https://crrev.com/9e150ec7eb5a30e78f63e3509a38a6ee4d0db153/chrome/browser/extensions/service_worker_apitest.cc
[modify] https://crrev.com/9e150ec7eb5a30e78f63e3509a38a6ee4d0db153/extensions/browser/service_worker_task_queue.cc
[modify] https://crrev.com/9e150ec7eb5a30e78f63e3509a38a6ee4d0db153/extensions/browser/service_worker_task_queue.h
[modify] https://crrev.com/9e150ec7eb5a30e78f63e3509a38a6ee4d0db153/extensions/browser/service_worker_task_queue_factory.cc


### ad...@chromium.org (2020-03-28)

OK, thank you. We don't want to accept any stability risk into M80 no matter how vanishingly small, so let's not proceed with the merge to M80. Thanks for digging into it though.

### na...@google.com (2020-03-30)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-04-01)

lazyboy@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### na...@google.com (2020-04-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-04-01)

Congrats! 

The Panel decided to award $7,500 for this report!

### na...@google.com (2020-04-01)

[Empty comment from Monorail migration]

### ad...@google.com (2020-04-04)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-04-04)

[Empty comment from Monorail migration]

### le...@gmail.com (2020-04-04)

Many thanks! Reporter credit: "Leecraso and Guang Gong of Alpha Lab, Qihoo 360".

### ad...@google.com (2020-04-07)

[Empty comment from Monorail migration]

### le...@gmail.com (2020-04-08)

Sorry to bother, but could you please help me to change my credit info from now on? 

### ad...@chromium.org (2020-04-08)

Done, as discussed via e-mail. Thanks for e-mailing directly, I had missed your comment https://crbug.com/chromium/1019161#c47.

### ad...@chromium.org (2020-04-14)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1019161?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050562)*
