# Stack-buffer-overflow in sandbox::BrokerServicesBase::SpawnTarget

| Field | Value |
|-------|-------|
| **Issue ID** | [40082048](https://issues.chromium.org/issues/40082048) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@chromium.org |
| **Assignee** | an...@chromium.org |
| **Created** | 2015-05-09 |
| **Bounty** | $2,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4857074056429568

Fuzzer: Therealholden_worker
Job Type: Windows_asan_chrome

Crash Type: Stack-buffer-overflow WRITE 4
Crash Address: 0x0cb7d608
Crash State:
  sandbox::BrokerServicesBase::SpawnTarget
  content::StartSandboxedProcess
  content::ChildProcessLauncher::DidLaunch
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_chrome&range=329019:329042

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv955nG7d1IJ0yuGDTB0kpvKHnjzDpR55zy1kGI8kKclgf9BObBoOC3mA6-wyuR47IyYvtsgCgfQNK7gOdlKnWww1HrO-8ypAvZDZo-x1xGTunyE-l2JJ7-7JZb-PrpDy-75Nb_AxFGf7E_4XRwBU2jKkhx1N2g


Additional requirements: Requires HTTP

Filer: inferno

## Timeline

### in...@chromium.org (2015-05-09)

Author: ananta 
Component: chromium
Changelist: https://chromium.googlesource.com/chromium/src//+/5d498ac79386ec8155fb2a768541e2b4b18c7d49
Time: Sat May 09 04:19:56 2015
File sandbox_win.cc is changed in this cl (and is part of stack frame #1, "content::StartSandboxedProcess")
Minimum distance from crash line to modified line: 45. (file: sandbox_win.cc, crashed on: 743, modified: 698).


### in...@chromium.org (2015-05-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-10)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### an...@chromium.org (2015-05-11)

I will look at this tomorrow

### bu...@chromium.org (2015-05-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a6ddf97af304f1aa7e88e28473e593e2c08c9157

commit a6ddf97af304f1aa7e88e28473e593e2c08c9157
Author: ananta <ananta@chromium.org>
Date: Mon May 11 23:45:55 2015

Fix a stack overflow in the windows sandbox SpawnTarget function.

This was caused by my recent change to allow handles other than STDOUT and STDERR to be shared
with the target. Reason for the crash was copying additional handles to the HANDLE array which had
space for 2 handles only.

Fix is to use scoped_ptr instead and allocate appropriate space for all handles being shared.

BUG=486434
R=cpu

Review URL: https://codereview.chromium.org/1128903006

Cr-Commit-Position: refs/heads/master@{#329276}

[modify] http://crrev.com/a6ddf97af304f1aa7e88e28473e593e2c08c9157/sandbox/win/src/broker_services.cc


### an...@chromium.org (2015-05-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-12)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-05-15)

ClusterFuzz has detected this issue as potentially fixed, but it appears to be flaky.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4857074056429568

Fuzzer: Therealholden_worker
Job Type: Windows_asan_chrome

Crash Type: Stack-buffer-overflow WRITE 4
Crash Address: 0x0cb7d608
Crash State:
  sandbox::BrokerServicesBase::SpawnTarget
  content::StartSandboxedProcess
  content::ChildProcessLauncher::DidLaunch
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_chrome&range=329019:329042

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv955nG7d1IJ0yuGDTB0kpvKHnjzDpR55zy1kGI8kKclgf9BObBoOC3mA6-wyuR47IyYvtsgCgfQNK7gOdlKnWww1HrO-8ypAvZDZo-x1xGTunyE-l2JJ7-7JZb-PrpDy-75Nb_AxFGf7E_4XRwBU2jKkhx1N2g


Additional requirements: Requires HTTP

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### ti...@google.com (2015-06-14)

Congrats - $2,500 for this report. ($2000 for the bug + $500 ClusterFuzz bonus) 

We'll start payment via our new process, which should take 1-2 weeks. That 1-2 week period payment time frame starts from when you see the "reward-inprocess" label on this bug.

Merge not required - regressed and fixed on trunk before M44 branch @ 330231

### ti...@google.com (2015-06-25)

Reward being paid via our new process - you should receive payment within 2 weeks.

### ti...@google.com (2015-07-24)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

(Note: sorry for the delay here - it turns out in the new payment system, these payments were waiting for a second approval from me).

### cl...@chromium.org (2015-08-18)

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

This issue was migrated from crbug.com/chromium/486434?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082048)*
