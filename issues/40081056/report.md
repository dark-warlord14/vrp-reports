# Use-of-uninitialized-value in ucnv_io_getConverterName_52

| Field | Value |
|-------|-------|
| **Issue ID** | [40081056](https://issues.chromium.org/issues/40081056) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Internationalization |
| **Reporter** | cl...@chromium.org |
| **Assignee** | js...@chromium.org |
| **Created** | 2014-12-22 |
| **Bounty** | $1,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5273829290016768

Fuzzer: Attekett_surku_fuzzer
Job Type: Linux_msan_chrome

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  ucnv_io_getConverterName_52
  ucnv_loadSharedData_52
  ucnv_createConverter_52
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=284099:284275

Minimized Testcase (0.02 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96Pbord3ACRAEqkN1OVf-IKuX1kLPRG_WG5XOSd-QC3-sPCEMCFAwRlz28Ta92U_CAsRcVhXEuJHWPCrQgn9pdUH7PL7G4YmEMukF-Z8oSxZmi7wx2tFIbhH70T2BRmJrkZvH8LV6O7QmkM_TFo0IK9S-2rcw
<?xml encoding="x"


Filer: inferno

## Timeline

### in...@chromium.org (2014-12-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-22)

[Empty comment from Monorail migration]

### rs...@chromium.org (2014-12-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-13)

jshin@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-02-03)

jshin@: Uh oh! This issue is still open and hasn't been updated in the last 42 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-02-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-24)

jshin@: Uh oh! This issue is still open and hasn't been updated in the last 63 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-03-06)

ClusterFuzz has detected this issue as fixed in range 317790:319224.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5273829290016768

Fuzzer: Attekett_surku_fuzzer
Job Type: Linux_msan_chrome

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  ucnv_io_getConverterName_52
  ucnv_loadSharedData_52
  ucnv_createConverter_52
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=284099:284275
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=317790:319224

Minimized Testcase (0.02 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96Pbord3ACRAEqkN1OVf-IKuX1kLPRG_WG5XOSd-QC3-sPCEMCFAwRlz28Ta92U_CAsRcVhXEuJHWPCrQgn9pdUH7PL7G4YmEMukF-Z8oSxZmi7wx2tFIbhH70T2BRmJrkZvH8LV6O7QmkM_TFo0IK9S-2rcw
<?xml encoding="x"

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2015-03-06)

ClusterFuzz has detected this issue as fixed in range 317790:319224.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5273829290016768

Fuzzer: Attekett_surku_fuzzer
Job Type: Linux_msan_chrome

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  ucnv_io_getConverterName_52
  ucnv_loadSharedData_52
  ucnv_createConverter_52
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=284099:284275
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=317790:319224

Minimized Testcase (0.02 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96Pbord3ACRAEqkN1OVf-IKuX1kLPRG_WG5XOSd-QC3-sPCEMCFAwRlz28Ta92U_CAsRcVhXEuJHWPCrQgn9pdUH7PL7G4YmEMukF-Z8oSxZmi7wx2tFIbhH70T2BRmJrkZvH8LV6O7QmkM_TFo0IK9S-2rcw
<?xml encoding="x"

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2015-03-18)

jshin@: Uh oh! This issue is still open and hasn't been updated in the last 85 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-04-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-08)

jshin@: Uh oh! This issue is still open and hasn't been updated in the last 106 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-04-30)

jshin@: Uh oh! This issue is still open and hasn't been updated in the last 128 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ti...@google.com (2015-05-07)

@jshin - CF believes that this fixed - is there an associated change?

### js...@chromium.org (2015-05-18)

https://crbug.com/chromium/444573#c8 (detecting this as fixed) is perhaps false. clusterfuzz is likely to regard this as fixed because it does not see any ucnv_foo_52 in the stack (as opposed to ucnv_foo_54 due to an ICU version upgrade from ICU 52 to 54). 

There's a change that ICU 54 fixed this problem, but the change window given in https://crbug.com/chromium/444573#c8 does not include the ICU version upgrade. 

I can't identify any uninitialized variable following through the stack trace in ICU 52. I'll build a msan build and see what's going on. 


### in...@chromium.org (2015-05-18)

It is not fixed. Jorge did a redo and it says Fixed:No. CF understands changes in stack frames and wont say fixed based on that. I think repro is just flaky, so try stuff manually to see how to fix.

Redo: jorgelo@chromium.org
Clusterfuzz-linux-high-end-0043: Fixed testing started in r330355 [2015-05-18 11:09:31]
Clusterfuzz-linux-high-end-0043: Fixed testing completed [0:01:58]

### jo...@chromium.org (2015-05-18)

Yeah, we agree this is not fixed. Jungshik will try to repro manually.

### mb...@chromium.org (2015-05-21)

From icu/source/common/ucnv_io.cpp:742:

            /*
             * After the first unsuccess converter lookup, check to see if
             * the name begins with 'x-'. If it does, strip it off and try
             * again.  This behaviour is similar to how ICU4J does it.
             */
            if (aliasTmp[0] == 'x' || aliasTmp[1] == '-') { // <-- Shouldn't that be &&?
                aliasTmp = aliasTmp+2;
            } else {
                break;
            }

Verified locally that this fixes the issue.

### jo...@chromium.org (2015-05-21)

Jungshik, what do you think?

### mb...@chromium.org (2015-05-22)

[Empty comment from Monorail migration]

### js...@chromium.org (2015-05-26)

re https://crbug.com/chromium/444573#c15:

"There's a change that ICU 54 fixed this problem" ; s/change/chance/  

 The lines in question has NOT changed for 4 years so that it's more than certain that this issue has not been fixed by ICU 54. 

Thanks, mbarbella@. 
Just filed 
http://bugs.icu-project.org/trac/ticket/11696  (unaccessible because it's marked as sensitive. I added  mbarbella's patch to the bug. ) 

jorgelo@ : I got back my Linux box late last week and have built a msan build. I'll verify mbarbella's change.

### js...@chromium.org (2015-05-26)

Just verified that mbarbella's change fixed the issue. 

I'll make a patch. 


### js...@chromium.org (2015-05-26)

https://codereview.chromium.org/1145963004 : CL up. 

Will start with ToT and then make a merge request to 44 and 43 branches. 


### jo...@chromium.org (2015-05-26)

Thanks!

### bu...@chromium.org (2015-05-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/deps/icu.git/+/f1ad7f9ba957571dc692ea3e187612c685615e19

commit f1ad7f9ba957571dc692ea3e187612c685615e19
Author: Jungshik Shin <jshin@chromium.org>
Date: Tue May 26 19:34:51 2015

Properly handle a converter name starting with "x-"

A fix by mbarbella@.

BUG=444573
TEST=See the bug
R=inferno@chromium.org, mbarbella@chromium.org

Review URL: https://codereview.chromium.org/1145963004

[modify] http://crrev.com/f1ad7f9ba957571dc692ea3e187612c685615e19/README.chromium
[add] http://crrev.com/f1ad7f9ba957571dc692ea3e187612c685615e19/patches/ucnv_name.patch
[modify] http://crrev.com/f1ad7f9ba957571dc692ea3e187612c685615e19/source/common/ucnv_io.cpp


### in...@chromium.org (2015-05-26)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-05-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/886e691e17018818b7fc0978bcbe9a85436b506c

commit 886e691e17018818b7fc0978bcbe9a85436b506c
Author: jshin <jshin@chromium.org>
Date: Tue May 26 21:16:07 2015

Roll ICU from 5788e2736b3bc to f1ad7f9ba957

Summary of changes available at:
 https://chromium.googlesource.com/chromium/deps/icu/+log/5788e27..f1ad7f9

BUG=444573
TEST=See the bug
TBR=inferno

Review URL: https://codereview.chromium.org/1157143002

Cr-Commit-Position: refs/heads/master@{#331437}

[modify] http://crrev.com/886e691e17018818b7fc0978bcbe9a85436b506c/DEPS


### js...@chromium.org (2015-05-26)

I'll ask for merge to 44 once we have a nightly build with this change. After that, I'll ask for merge to 43. 


### cl...@chromium.org (2015-05-26)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-05-27)

ClusterFuzz has detected this issue as fixed in range 331388:331444.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5273829290016768

Fuzzer: Attekett_surku_fuzzer
Job Type: Linux_msan_chrome

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  ucnv_io_getConverterName_52
  ucnv_loadSharedData_52
  ucnv_createConverter_52
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=284099:284275
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=331388:331444

Minimized Testcase (0.02 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96Pbord3ACRAEqkN1OVf-IKuX1kLPRG_WG5XOSd-QC3-sPCEMCFAwRlz28Ta92U_CAsRcVhXEuJHWPCrQgn9pdUH7PL7G4YmEMukF-Z8oSxZmi7wx2tFIbhH70T2BRmJrkZvH8LV6O7QmkM_TFo0IK9S-2rcw
<?xml encoding="x"

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### js...@chromium.org (2015-05-28)

Requesting for merge to 44. 

What's to merge is https://codereview.chromium.org/1145963004 (note that the actual change is 1 liner replacing "||" with "&&" ). 

At least four canary builds went out (45.0.2414.[0-2], 45.0.2415.0 ) without a known issue reported attributed to this change (afaict). 



### pe...@google.com (2015-05-28)

Approved for M44 (branch: 2403)

### bu...@chromium.org (2015-05-28)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=74127

------------------------------------------------------------------
r74127 | jungshik@google.com | 2015-05-28T20:35:13.355615Z

-----------------------------------------------------------------

### js...@chromium.org (2015-05-29)

Requesting merge to M43 branch. 


### js...@chromium.org (2015-05-29)

Again: 
what's to merge is https://codereview.chromium.org/1145963004 (note that the actual change is 1 liner replacing "||" with "&&" ).

It'll be done by making a m43 branch to third_party/icu and merging the above change to that branch. [1]  After that, third_party/icu will be rolled to that revision in buildspec for M43 (DEPS roll). 

[1] https://codereview.chromium.org/1162053002

### in...@chromium.org (2015-05-29)

Since this is medium severity, this does not need merging to m43.

### js...@chromium.org (2015-05-29)

Ok. Then, I'm removing M43 label as well as M43-Merge-Request.  

### mb...@chromium.org (2015-07-16)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-07-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-08-17)

Congrats: $500 for the bug + $500 for CF.

### ti...@google.com (2015-08-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-09-01)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-09-10)

Processing via our e-payment system takes ~7 days, but the reward should be on its way to you. Thanks again for your help!

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

This issue was migrated from crbug.com/chromium/444573?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081056)*
