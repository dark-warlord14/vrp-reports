# Heap-use-after-free in ash::WindowSelector::ContentsChanged

| Field | Value |
|-------|-------|
| **Issue ID** | [40083457](https://issues.chromium.org/issues/40083457) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ns...@chromium.org |
| **Created** | 2015-12-26 |
| **Bounty** | $1,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6063352922505216

Fuzzer: cdiehl_peach
Job Type: linux_asan_chrome_chromeos
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60c000152568
Crash State:
  ash::WindowSelector::ContentsChanged
  views::Textfield::UpdateAfterChange
  views::Textfield::ConfirmCompositionText
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_chromeos&range=359893:360003

Minimized Testcase (72.96 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96LgBy9kD6oXT_tnUqOvhsPZ5vzUG6HL_tdPVDdi-IEf-51Y0cIqfc_gvN1TjYykA29x84dLrbaXe9fHW9YS0waKh0QfMx3t29k9pHjVu3enqPUCAOxvRZ220OhAFlFnyvOlczLS8eqSR3tV8heEKr6YUf1xT3UNXjytiYpWq6GUQOsyLs

Additional requirements: Requires Gestures

Filer: inferno

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### in...@chromium.org (2015-12-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-12-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-12-27)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### in...@chromium.org (2015-12-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-10)

nsatragno@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2016-01-13)

ClusterFuzz has detected this issue as fixed in range 368734:368790.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6063352922505216

Fuzzer: cdiehl_peach
Job Type: linux_asan_chrome_chromeos
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60c000152568
Crash State:
  ash::WindowSelector::ContentsChanged
  views::Textfield::UpdateAfterChange
  views::Textfield::ConfirmCompositionText
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_chromeos&range=359893:360003
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_chromeos&range=368734:368790

Minimized Testcase (72.96 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96LgBy9kD6oXT_tnUqOvhsPZ5vzUG6HL_tdPVDdi-IEf-51Y0cIqfc_gvN1TjYykA29x84dLrbaXe9fHW9YS0waKh0QfMx3t29k9pHjVu3enqPUCAOxvRZ220OhAFlFnyvOlczLS8eqSR3tV8heEKr6YUf1xT3UNXjytiYpWq6GUQOsyLs

Additional requirements: Requires Gestures

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2016-01-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-25)

nsatragno@: Uh oh! This issue is still open and hasn't been updated in the last 28 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ns...@chromium.org (2016-02-01)

clusterfuzz is reporting the issue as fixed. Can we close this?

### in...@chromium.org (2016-02-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2016-02-04)

Why: reward-ineligible ?

### in...@chromium.org (2016-02-04)

My bad, i closed it in wrong status. Fixing tags.

### cl...@chromium.org (2016-02-04)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### [Deleted User] (2016-02-18)

[Comment Deleted]

### in...@chromium.org (2016-02-18)

This should be go in the next reward panel. Tim, can you add it in docs please.

### ti...@google.com (2016-02-29)

#17: Yes - will add to this week's reward panel. No merge required as fixed before M49 branch @ 369907.

### [Deleted User] (2016-04-04)

[Comment Deleted]

### sh...@chromium.org (2016-05-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2016-05-17)

[Comment Deleted]

### ti...@google.com (2016-06-21)

As discussed via email - $1,000 for this report. Thanks again!

### ti...@google.com (2016-06-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/572404?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083457)*
