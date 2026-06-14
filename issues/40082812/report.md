# Bad-cast to util from Document;JS_Define.h:165:13

| Field | Value |
|-------|-------|
| **Issue ID** | [40082812](https://issues.chromium.org/issues/40082812) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ts...@chromium.org |
| **Created** | 2015-09-07 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6109475780427776

Fuzzer: attekett_surku_fuzzer
Job Type: linux_cfi_chrome
Platform Id: linux

Crash Type: Bad-cast
Crash Address: 0x7f4e3209f670
Crash State:
  Bad-cast to util from Document
  JS_Define.h:165:13
  

Minimized Testcase (15.39 Kb): https://cluster-fuzz.appspot.com/download/AMIfv974Yx0v8shdnwh4BusIILt-zrX1z3a5keHn5gOTaXAY6MTC9nJmGlg8XhN7JeI5ktbykJ27qj_gLAUYuwEHec-56TI91sbVFpo5Jk9idbfdqbqfOvhXM1UVa5xRzQoMEhuc7zEthb_cKSpnEfI1H7cwu3eOMQ

Filer: aarya

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### aa...@google.com (2015-09-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-09-07)

[Empty comment from Monorail migration]

### th...@chromium.org (2015-09-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-09-07)

[Empty comment from Monorail migration]

### ts...@chromium.org (2015-09-08)

Oh, joy. Looks like static methods are playing fast and loose with the type of the object they invoke methods against, relying instead that the object won't be touched in any manner.  

Let me see if I cant' clean this up.  There's gonna be a lot of these reports.

### kc...@chromium.org (2015-09-09)

[Empty comment from Monorail migration]

### th...@chromium.org (2015-09-18)

Ping. Don't forget about this one.

### ts...@chromium.org (2015-09-18)

Waiting on separate email thread about v8's |apply|.
Basically, this is 
  util.byteToChar.apply(this, ["bleen"]);

and we need to guard against v8 handing us arbitrary objects to these native methods.

### kr...@chromium.org (2015-09-22)

tsepez: any updates?

This is one of two hard blockers for Control Flow Integrity launch on Linux.

### ts...@chromium.org (2015-09-22)

https://codereview.chromium.org/1353193004/ is where the discussion is happening.

### cl...@chromium.org (2015-10-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-10-07)

tsepez@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ts...@chromium.org (2015-10-07)

Should be fixed by 158e335.  Kicking off redo on CF to see if it still (intermittently) hits it.

### cl...@chromium.org (2015-10-07)

ClusterFuzz has detected this issue as fixed in range 350936:350990.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6109475780427776

Fuzzer: attekett_surku_fuzzer
Job Type: linux_cfi_chrome
Platform Id: linux

Crash Type: Bad-cast
Crash Address: 0x7f4e3209f670
Crash State:
  Bad-cast to util from Document
  JS_Define.h:165:13
  
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_cfi_chrome&range=350936:350990

Minimized Testcase (15.39 Kb): https://cluster-fuzz.appspot.com/download/AMIfv974Yx0v8shdnwh4BusIILt-zrX1z3a5keHn5gOTaXAY6MTC9nJmGlg8XhN7JeI5ktbykJ27qj_gLAUYuwEHec-56TI91sbVFpo5Jk9idbfdqbqfOvhXM1UVa5xRzQoMEhuc7zEthb_cKSpnEfI1H7cwu3eOMQ

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### ts...@chromium.org (2015-10-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-10-07)

ClusterFuzz has detected this issue as fixed in range 350936:350990.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6109475780427776

Fuzzer: attekett_surku_fuzzer
Job Type: linux_cfi_chrome
Platform Id: linux

Crash Type: Bad-cast
Crash Address: 0x7f4e3209f670
Crash State:
  Bad-cast to util from Document
  JS_Define.h:165:13
  
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_cfi_chrome&range=350936:350990

Minimized Testcase (15.39 Kb): https://cluster-fuzz.appspot.com/download/AMIfv974Yx0v8shdnwh4BusIILt-zrX1z3a5keHn5gOTaXAY6MTC9nJmGlg8XhN7JeI5ktbykJ27qj_gLAUYuwEHec-56TI91sbVFpo5Jk9idbfdqbqfOvhXM1UVa5xRzQoMEhuc7zEthb_cKSpnEfI1H7cwu3eOMQ

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### cl...@chromium.org (2015-10-07)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-10-12)

Once this bakes in M-47 beta for a while, please merge request to M-46 to see if we can ride a M-46 patch release.

### th...@chromium.org (2015-10-12)

tsepez: Do you want me to take care of the merge?

### ts...@chromium.org (2015-10-12)

Yes, thanks!

### th...@chromium.org (2015-10-13)

Looks like there's nothing to merge for M47. The fix landed before the M47 branch point. So merging to M46 only.

### th...@chromium.org (2015-10-13)

Actually, it requires a DEPS roll.

### th...@chromium.org (2015-10-13)

And ignore https://crbug.com/chromium/529012#c22. I was looking at the wrong branch. @_@

### ti...@google.com (2015-10-14)

[Automated comment] Request affecting a post-stable build (M46), manual review required.

### ti...@chromium.org (2015-10-15)

M46 Stable has launched, and for post stable we only consider safe merges on critical Security/ Stability/ Critical regressions.
I'm concerned this requires a DEPS roll and how safe it is. Can you pls add user impact to help better understand the issue and the risk? Thanks.

### th...@chromium.org (2015-10-15)

git cherry-pick -x 158e335717efba9dce3aa6f6d1e31ed884e1f59e

onto the 2490 branch results in a lot of conflicts. I've not looked at how much work it will actually take to merge to M46. Tom, WDYT?

### ti...@chromium.org (2015-10-19)

given the merge isn't safe, we'll have to punt it.

### th...@chromium.org (2015-11-05)

[Empty comment from Monorail migration]

### th...@chromium.org (2015-11-06)

Actually, this is already on the 2526 branch. We're all good here.

### ti...@google.com (2015-11-23)

Updating labels.

### ti...@google.com (2015-12-01)

Hey Atte - $3500 for this report ($3000 + $500 Clusterfuzz bonus). Thanks as always - I'll start payment later this week.

### kc...@chromium.org (2015-12-11)

[Empty comment from Monorail migration]

### ti...@google.com (2015-12-14)

[Empty comment from Monorail migration]

### ti...@google.com (2016-01-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-13)

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

This issue was migrated from crbug.com/chromium/529012?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082812)*
