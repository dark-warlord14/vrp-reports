# AddressSanitizer: heap-use-after-free in blink::NetworkStateNotifier::NotifyObserversOnTaskRunner

| Field | Value |
|-------|-------|
| **Issue ID** | [40058195](https://issues.chromium.org/issues/40058195) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Network |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | dm...@gmail.com |
| **Assignee** | yo...@chromium.org |
| **Created** | 2021-12-10 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0

Steps to reproduce the problem:
1. Open attached NetworkStateNotifier-heap-use-after-free.html in Chromium ("./Chromium --user-data-dir=/tmp/temporary-test-dir NetworkStateNotifier-heap-use-after-free.html")
2. Wait until iframe loaded and turn off network.
3. Wait until window.print will be triggered and you will see your printed page.
4. Turn on network and wait until network is connected.
5. Dismiss print dialog.
6. Check terminal for ASAN Crash Report.

Additionally, I attach video with reproduce.

What is the expected behavior?
No heap-use-after-free on notifying network observers if iframe with observer was been removed.

What went wrong?
Suspected reason of crash: User able to delete iframe on "offline" event (or "online" event), observer of this window is freed, but pointer to observer of this iframe still alive when user trigger new event.

Check attached ASAN log for details.

Did this work before? N/A 

Chrome version: 98.0.4737.0 (Developer Build) (x86_64)  Channel: n/a
OS Version: OS X 10.15

## Attachments

- [NetworkStateNotifier-heap-use-after-free.html](attachments/NetworkStateNotifier-heap-use-after-free.html) (text/plain, 637 B)
- [ChromiumUseAfterFreeInNetworkStateNotifier.mp4](attachments/ChromiumUseAfterFreeInNetworkStateNotifier.mp4) (video/mp4, 5.9 MB)
- [NetworkStateNotifier-heap-use-after-free.txt](attachments/NetworkStateNotifier-heap-use-after-free.txt) (text/plain, 28.8 KB)
- [fix.diff](attachments/fix.diff) (text/plain, 1.2 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 28.1 KB)
- [bt.txt](attachments/bt.txt) (text/plain, 4.0 KB)

## Timeline

### [Deleted User] (2021-12-10)

[Empty comment from Monorail migration]

### dm...@gmail.com (2021-12-10)

ASAN Log:

### dm...@gmail.com (2021-12-11)

Hello again,

I found a possible way to fix this vulnerability + fix CHECK in CollectZeroedObservers method. See attached "fix.diff". This works with latest code of Chromium. This will need tests and additional validation, so, it's proposed fix of general vulnerability.

P.S.: I can not be sure if it's correct fix, because not familiar with Chromium Coding Standards, but submit this for further review.

P.P.S.: I describe invalid reason of crash in primary report. Sorry.

Thanks.

### do...@chromium.org (2021-12-13)

Thanks for the report and proposed patch. :) Do you mind attaching the full stack trace that you get?

+jkarlin/yhirano from the previous https://crbug.com/chromium/1170148 which seems similar to this. Can you take a look please?



[Monorail components: Blink>Network]

### [Deleted User] (2021-12-13)

[Empty comment from Monorail migration]

### dm...@gmail.com (2021-12-13)

I attach backtrace from LLDB and report from ASAN to this comment. Do you need any additional information?

Thanks.

### do...@chromium.org (2021-12-13)

Thanks very much - that should be enough for the team to go by. :)

### [Deleted User] (2021-12-13)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-13)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-24)

jkarlin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-03)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-13)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-24)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-07)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-17)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-28)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-02)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-12)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-23)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### th...@chromium.org (2022-06-10)

Security marshal here. jkarlin@, are there any updates on this ticket?

### jk...@chromium.org (2022-06-10)

Assigning to Yutaka as I believe this is related to https://bugs.chromium.org/p/chromium/issues/detail?id=1170148, but should be verified.

### ts...@chromium.org (2022-07-20)

yhirano - friendly ping, any progress on this old bug?
visiedo - alternatively, is there someone else on the team that might have time to look at this?
Thanks!

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### yh...@chromium.org (2022-09-30)

Sorry for the long silence. Releasing this as I'm leaving the team.

### vi...@chromium.org (2022-11-17)

I couldn't reproduce the crash on:

Chrome Version: 107.0.5304.110 (Official Build) (x86_64)
OS Version: OSX 12.6.1

Chrome Version: 108.0.5359.48 (Official Build) beta (x86_64)
OS Version: OSX 12.6.1

Could you confirm if this is still an issue? 


### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### mp...@chromium.org (2023-01-09)

OP, can you confirm if this is still reproducing for you?

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### vi...@chromium.org (2023-02-15)

[Empty comment from Monorail migration]

### yo...@chromium.org (2023-02-17)

[Empty comment from Monorail migration]

### ad...@google.com (2023-02-28)

(I am a bot: this is an auto-cc on a security bug)

### ad...@google.com (2023-02-28)

(I am a bot: this is an auto-cc on a security bug)

### gi...@appspot.gserviceaccount.com (2023-03-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9c3ac3d9ceea60ad946b807f8661fce2588d2056

commit 9c3ac3d9ceea60ad946b807f8661fce2588d2056
Author: Yoichi Osato <yoichio@chromium.org>
Date: Wed Mar 01 06:38:58 2023

Call each NetworkStateObserver separately.

NetworkStateNotifier used to have NetworkStateObserver list as
HashMap<SingleThreadTaskRunner*, Vector<NetworkStateObserver*>> and
call each observer on a taskrunner sequentially.
That caused race condition and use-after-free: what if an observer
calls wait and other observer removes all?
We also should not guarantee the order of registering observers is
kept as notification order: each observer should not depend on others.

To fix that, this patch reconstructs the structure to
HashMap<NetworkStateObserver*, SingleThreadTaskRunner*> and call each
observer on each taskrunner separately.
This implementation follows base/observer_list_threadsafe.h except
the taskrunner is given by the caller.

Fixed: 1278708
Change-Id: Iff5d0008d5b0d98caa5931e2806db3ffc52be6fa
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4280021
Reviewed-by: Kent Tamura <tkent@chromium.org>
Commit-Queue: Yoichi Osato <yoichio@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1111448}

[modify] https://crrev.com/9c3ac3d9ceea60ad946b807f8661fce2588d2056/third_party/blink/renderer/platform/network/network_state_notifier_test.cc
[modify] https://crrev.com/9c3ac3d9ceea60ad946b807f8661fce2588d2056/third_party/blink/renderer/platform/network/network_state_notifier.h
[modify] https://crrev.com/9c3ac3d9ceea60ad946b807f8661fce2588d2056/third_party/blink/renderer/platform/network/network_state_notifier.cc


### [Deleted User] (2023-03-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-08)

The bot skipped merge requests on this one; at a minimum this should be merged to M112; labeling accordingly to get into merge review queue
Also, so we can evaluate potential backmerge to M111/Stable and M110/Extended. 

### [Deleted User] (2023-03-08)

Merge approved: your change passed merge requirements and is auto-approved for M112. Please go ahead and merge the CL to branch 5615 (refs/branch-heads/5615) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), govind (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-03-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ed61a53c254818af3bc072d6052026640fdc4240

commit ed61a53c254818af3bc072d6052026640fdc4240
Author: Yoichi Osato <yoichio@chromium.org>
Date: Thu Mar 09 05:37:01 2023

Call each NetworkStateObserver separately.

NetworkStateNotifier used to have NetworkStateObserver list as
HashMap<SingleThreadTaskRunner*, Vector<NetworkStateObserver*>> and
call each observer on a taskrunner sequentially.
That caused race condition and use-after-free: what if an observer
calls wait and other observer removes all?
We also should not guarantee the order of registering observers is
kept as notification order: each observer should not depend on others.

To fix that, this patch reconstructs the structure to
HashMap<NetworkStateObserver*, SingleThreadTaskRunner*> and call each
observer on each taskrunner separately.
This implementation follows base/observer_list_threadsafe.h except
the taskrunner is given by the caller.

(cherry picked from commit 9c3ac3d9ceea60ad946b807f8661fce2588d2056)

Fixed: 1278708
Change-Id: Iff5d0008d5b0d98caa5931e2806db3ffc52be6fa
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4280021
Reviewed-by: Kent Tamura <tkent@chromium.org>
Commit-Queue: Yoichi Osato <yoichio@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1111448}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4323457
Auto-Submit: Yoichi Osato <yoichio@chromium.org>
Reviewed-by: Yoichi Osato <yoichio@chromium.org>
Commit-Queue: Kent Tamura <tkent@chromium.org>
Cr-Commit-Position: refs/branch-heads/5615@{#307}
Cr-Branched-From: 9c6408ef696e83a9936b82bbead3d41c93c82ee4-refs/heads/main@{#1109224}

[modify] https://crrev.com/ed61a53c254818af3bc072d6052026640fdc4240/third_party/blink/renderer/platform/network/network_state_notifier_test.cc
[modify] https://crrev.com/ed61a53c254818af3bc072d6052026640fdc4240/third_party/blink/renderer/platform/network/network_state_notifier.h
[modify] https://crrev.com/ed61a53c254818af3bc072d6052026640fdc4240/third_party/blink/renderer/platform/network/network_state_notifier.cc


### am...@google.com (2023-03-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-09)

Congratulations! The VRP Panel has decided to award you $2,000 for this report of a moderately mitigated security bug. Thank you for your efforts and reporting this issue to us!  

### am...@google.com (2023-03-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-31)

[Empty comment from Monorail migration]

### pg...@google.com (2023-04-04)

[Empty comment from Monorail migration]

### pg...@google.com (2023-04-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1278708?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058195)*
