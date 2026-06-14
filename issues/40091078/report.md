# Security: Crash with JavaScript RegExp subclassing

| Field | Value |
|-------|-------|
| **Issue ID** | [40091078](https://issues.chromium.org/issues/40091078) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | pe...@gmail.com |
| **Assignee** | jg...@chromium.org |
| **Created** | 2018-04-12 |
| **Bounty** | $1,500.00 |

## Description

**VULNERABILITY DETAILS**

Executing the following JavaScript will cause a browser tab to crash.

```
class MyRegExp extends RegExp {  
  exec(str) {  
    const r = super.exec.call(this, str);  
    r[0] = 0; // Value could be changed to something arbitrary  
    return r;  
  }  
}  
  
'a'.match(new MyRegExp('.', 'g'));  

```

I believe the issue is because a code assumption is being broken:  

<https://cs.chromium.org/chromium/src/v8/src/builtins/builtins-regexp-gen.cc?l=1878-1879&rcl=fc27a8d63c94c91ede18fce3246fbba7aec54262>

`r[0]` is assumed to be string object because it passed the "BranchIfFastRegExpResult" verification. Unfortunately it isn't and I believe this ends up with an arbitrary load:

<https://cs.chromium.org/chromium/src/v8/src/builtins/builtins-regexp-gen.cc?l=1879-1881&rcl=fc27a8d63c94c91ede18fce3246fbba7aec54262>  

<https://cs.chromium.org/chromium/src/v8/src/builtins/builtins-regexp-gen.cc?l=1904&rcl=fc27a8d63c94c91ede18fce3246fbba7aec54262>  

<https://cs.chromium.org/chromium/src/v8/src/builtins/builtins-regexp-gen.cc?l=1912&rcl=fc27a8d63c94c91ede18fce3246fbba7aec54262>  

<https://cs.chromium.org/chromium/src/v8/src/code-stub-assembler.cc?l=1642-1647&rcl=fc27a8d63c94c91ede18fce3246fbba7aec54262>

Although I don't think it's possible to get actual value of the load, you could detect whether it is a particular value or not (smi zero) depending on down stream side effects (regexp.lastIndex was incremented or not).

**VERSION**  

Chrome Version: stable (65.0.3325.181), also verified on dev (67.0.3394.0) and latest version of Node.js (9.11.1)  

Operating System: Mac OS X High Sierra 10.13.3

**REPRODUCTION CASE**

```
class MyRegExp extends RegExp {  
  exec(str) {  
    const r = super.exec.call(this, str);  
    r[0] = 0; // Value could be changed to something arbitrary  
    return r;  
  }  
}  
  
'a'.match(new MyRegExp('.', 'g'));  

```

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash ID: crash/9beff3f332dcbf6a

## Timeline

### cl...@chromium.org (2018-04-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4949311713181696.

### cl...@chromium.org (2018-04-12)

Detailed report: https://clusterfuzz.com/testcase?key=4949311713181696

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Null-dereference READ
Crash Address: 0x00000000000f
Crash State:
  v8::internal::Invoke
  v8::internal::Execution::Call
  v8::Script::Run
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=523898:523900

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4949311713181696

See https://github.com/google/clusterfuzz-tools for more information.

### cl...@chromium.org (2018-04-12)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript]

### is...@chromium.org (2018-04-12)

[Empty comment from Monorail migration]

### jg...@chromium.org (2018-04-12)

Thanks, Peter already has a fix in flight here: https://crrev.com/c/1009325.

### bu...@chromium.org (2018-04-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/7bdbe77a3fa38ed8df0813323f116f0dff86c4f9

commit 7bdbe77a3fa38ed8df0813323f116f0dff86c4f9
Author: peterwmwong <peter.wm.wong@gmail.com>
Date: Thu Apr 12 14:54:54 2018

[builtins] Fix missing ToString in RegExp.p.match

It is not safe to assume the first match is a string just
because the RegExp result is fast.

Bug: chromium:831943
Change-Id: Idd40f8b75312f0be54f45f626dc017339033abc6
Reviewed-on: https://chromium-review.googlesource.com/1009325
Reviewed-by: Jakob Gruber <jgruber@chromium.org>
Commit-Queue: Peter Wong <peter.wm.wong@gmail.com>
Cr-Commit-Position: refs/heads/master@{#52578}
[modify] https://crrev.com/7bdbe77a3fa38ed8df0813323f116f0dff86c4f9/src/builtins/builtins-regexp-gen.cc
[add] https://crrev.com/7bdbe77a3fa38ed8df0813323f116f0dff86c4f9/test/mjsunit/regress/regress-crbug-831943.js


### jg...@chromium.org (2018-04-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-12)

This bug requires manual review: We don't branch M67 until 2018-04-12.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-04-12)

This bug requires manual review: We are only 4 days from stable.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), josafat@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jg...@chromium.org (2018-04-12)

#6 fixes a possible OOB read present since 57, originally introduced in:

=====================ORIGINAL COMMIT START===================
commit 4e7571a5a9bb8563ae93e0aff48c08bead765b14
Author: jgruber <jgruber@chromium.org>
Date:   Tue Nov 29 01:02:48 2016 -0800

    [regexp] Migrate @@match to TurboFan
    
    Microbenchmarks show a 4x improvement on the fast path and 2.5x improvement on
    the slow path when compared to the CPP builtin implementation.
    
    Compared to the old JS implementation, the fast path is 20% faster and the slow
    path 35% slower.
    
    BUG=v8:5339,v8:5562
    
    Review-Url: https://codereview.chromium.org/2527963002
    Cr-Commit-Position: refs/heads/master@{#41338}
=====================ORIGINAL COMMIT END=====================
2.) General information:
Is LKGR:         True
Is on Canary:    2937
First V8 branch: 5.7.100 (Might not be the rolled version)

### ab...@chromium.org (2018-04-12)

which OS is this impacting?

### pe...@gmail.com (2018-04-12)

abdulsyed@,

I've verified this crashes on Windows 10, MacOS X High Sierra and Android 8.1.0.
As far as I can tell by the code, all operating systems would be impacted.

### go...@chromium.org (2018-04-12)

Apply all OSs per https://crbug.com/chromium/831943#c12.

### sh...@chromium.org (2018-04-13)

[Empty comment from Monorail migration]

### ab...@chromium.org (2018-04-13)

+ awhalley@ - thoughts on taking this for M66 vs waiting until 67 from a security perspective?

### aw...@google.com (2018-04-13)

I'm OK waiting to 67

### aw...@google.com (2018-04-13)

[Empty comment from Monorail migration]

### go...@chromium.org (2018-04-13)

awhalley@, pls do M67 merge review. Thank you.

### aw...@google.com (2018-04-13)

good for 67

### go...@chromium.org (2018-04-13)

Approving merge to M67 branch 3396 based on https://crbug.com/chromium/831943#c19. Please merge ASAP. Thank you.

### go...@chromium.org (2018-04-15)

Pls merge your change to M67 branch 3396 by 1:00 PM PT Monday (04/16/18) so we can pick it up for next M67 dev release. Thank you.

### bu...@chromium.org (2018-04-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/9a443d2aea5764e41fbf8417ad3885da923f38ae

commit 9a443d2aea5764e41fbf8417ad3885da923f38ae
Author: peterwmwong <peter.wm.wong@gmail.com>
Date: Mon Apr 16 06:52:05 2018

Merged: [builtins] Fix missing ToString in RegExp.p.match

It is not safe to assume the first match is a string just
because the RegExp result is fast.

NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true

Bug: chromium:831943
Change-Id: Idd40f8b75312f0be54f45f626dc017339033abc6
Reviewed-on: https://chromium-review.googlesource.com/1009325
Reviewed-by: Jakob Gruber <jgruber@chromium.org>
Commit-Queue: Peter Wong <peter.wm.wong@gmail.com>
Cr-Original-Commit-Position: refs/heads/master@{#52578}(cherry picked from commit 7bdbe77a3fa38ed8df0813323f116f0dff86c4f9)
Reviewed-on: https://chromium-review.googlesource.com/1013578
Commit-Queue: Jakob Gruber <jgruber@chromium.org>
Cr-Commit-Position: refs/branch-heads/6.7@{#12}
Cr-Branched-From: 8457e810efd34381448d51d93f50079cf1f6a812-refs/heads/6.7.288@{#2}
Cr-Branched-From: e921be5c4f2c6407936bde750992dedbf47c1016-refs/heads/master@{#52547}
[modify] https://crrev.com/9a443d2aea5764e41fbf8417ad3885da923f38ae/src/builtins/builtins-regexp-gen.cc
[add] https://crrev.com/9a443d2aea5764e41fbf8417ad3885da923f38ae/test/mjsunit/regress/regress-crbug-831943.js


### jg...@chromium.org (2018-04-16)

Removing Merge-Review-66 as per #16, thanks everyone.

### go...@chromium.org (2018-04-16)

Per https://crbug.com/chromium/831943#c22, this is already merged to M67. If nothing is pending, pls remove "Merge-Approved-67" label. Thank you. 

### jg...@chromium.org (2018-04-16)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-16)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-04-18)

ClusterFuzz has detected this issue as fixed in range 550886:550887.

Detailed report: https://clusterfuzz.com/testcase?key=4949311713181696

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Null-dereference READ
Crash Address: 0x00000000000f
Crash State:
  v8::internal::Invoke
  v8::internal::Execution::Call
  v8::Script::Run
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=523898:523900
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=550886:550887

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4949311713181696

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2018-04-18)

ClusterFuzz testcase 4949311713181696 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### aw...@chromium.org (2018-04-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-04-20)

Many thanks, peter.wm.wong@!  The Chrome VRP panel decided to award $1,000 for the bug report, and a $500 bonus because you supplied the fix.  A member of our finance team will be in touch to arrange payment.  Also, how would you like to be credited in Chrome release notes? Cheers!

### aw...@chromium.org (2018-04-20)

[Empty comment from Monorail migration]

### pe...@gmail.com (2018-04-21)

awhalley@ Wow! You can credit me as "Peter Wong". Thanks!

### ro...@chromium.org (2018-05-18)

CC'ing Zuojian from UC Browser

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### is...@google.com (2019-06-27)

This issue was migrated from crbug.com/chromium/831943?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091078)*
