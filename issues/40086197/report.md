# Crash in v8::internal::Simulator::DecodeType2

| Field | Value |
|-------|-------|
| **Issue ID** | [40086197](https://issues.chromium.org/issues/40086197) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Linux |
| **Reporter** | de...@googlemail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2016-12-12 |
| **Bounty** | $3,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5916664546983936

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8_ignition_v8_arm_dbg
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0xffffffff
Crash State:
  v8::internal::Simulator::DecodeType2
  v8::internal::Simulator::InstructionDecode
  v8::internal::Simulator::CallInternal
  
Recommended Security Severity: Medium

Regressed: V8: r41057:41058

Minimized Testcase (7.56 Kb): https://cluster-fuzz.appspot.com/download/AMIfv948WJpUb9kKH9TmQs8nvK8kZOTD5ZJKOAyA0BmnaR0yjOo4vXUjYZhHOvsUm9KJY336Bsymu3uyWVJZTWvUfuNf9OV3EwNsuFt5NpgtOAl-fpS6pnLyCpDAi3qKb0ElPfqGSBJW1HGcY8QW2NB-pCst9PasXQ?testcase_id=5916664546983936

Issue manually filed by: ishell

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### is...@chromium.org (2016-12-12)

CF points to b8c2035f261f904c3424a46894d4a76036363df2

### bm...@chromium.org (2016-12-12)

Jaro, can you take a look? Seems like loop peeling triggered some bug. You can ask Rodolph if they can help with this one once you have a repro and it looks like it's an ARM bug.

[Monorail components: -Blink>JavaScript Blink>JavaScript>Compiler]

### ja...@chromium.org (2016-12-12)

I am on it. It is a bug in representation changer when we introduced the split between the tagged pointer and smi.

### ja...@chromium.org (2016-12-12)

Apparently, conversion from bit to tagged pointer is a no-op :-)

### bu...@chromium.org (2016-12-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/d024df4d22eb69904bfd29c7716ff0f2c16f5d18

commit d024df4d22eb69904bfd29c7716ff0f2c16f5d18
Author: jarin <jarin@chromium.org>
Date: Mon Dec 12 09:36:27 2016

[turbofan] Fix representation change from bit to tagged pointer.

BUG=chromium:673244

Review-Url: https://codereview.chromium.org/2568053002
Cr-Commit-Position: refs/heads/master@{#41634}

[modify] https://crrev.com/d024df4d22eb69904bfd29c7716ff0f2c16f5d18/src/compiler/representation-change.cc
[add] https://crrev.com/d024df4d22eb69904bfd29c7716ff0f2c16f5d18/test/mjsunit/compiler/regress-673244.js


### sh...@chromium.org (2016-12-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-12-13)

ClusterFuzz has detected this issue as fixed in range 41633:41634.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5916664546983936

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8_ignition_v8_arm_dbg
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0xffffffff
Crash State:
  v8::internal::Simulator::DecodeType2
  v8::internal::Simulator::InstructionDecode
  v8::internal::Simulator::CallInternal
  
Recommended Security Severity: Medium

Regressed: V8: r41057:41058
Fixed: V8: r41633:41634

Minimized Testcase (7.56 Kb): https://cluster-fuzz.appspot.com/download/AMIfv948WJpUb9kKH9TmQs8nvK8kZOTD5ZJKOAyA0BmnaR0yjOo4vXUjYZhHOvsUm9KJY336Bsymu3uyWVJZTWvUfuNf9OV3EwNsuFt5NpgtOAl-fpS6pnLyCpDAi3qKb0ElPfqGSBJW1HGcY8QW2NB-pCst9PasXQ?testcase_id=5916664546983936

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2016-12-13)

ClusterFuzz testcase 5916664546983936 is verified as fixed, so closing issue.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2016-12-13)

[Empty comment from Monorail migration]

### aw...@google.com (2016-12-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-15)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-12-15)

Your change meets the bar and is auto-approved for M56 (branch: 2924)

### sh...@chromium.org (2016-12-19)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-12-23)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2017-01-09)

[Empty comment from Monorail migration]

### aw...@google.com (2017-01-10)

$3,000 for this find :-)

### aw...@chromium.org (2017-01-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-02-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/bd54aa2c9039a141b09d2456f8d7297ae3f5baf8

commit bd54aa2c9039a141b09d2456f8d7297ae3f5baf8
Author: Jaroslav Sevcik <jarin@chromium.org>
Date: Thu Feb 09 12:16:50 2017

Merged: [turbofan] Fix representation change from bit to tagged pointer.

Revision: d024df4d22eb69904bfd29c7716ff0f2c16f5d18

BUG=chromium:673244
LOG=N
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=bmeurer@chromium.org
TBR=bmeurer@chromium.org

Review-Url: https://codereview.chromium.org/2684593007 .
Cr-Commit-Position: refs/branch-heads/5.6@{#112}
Cr-Branched-From: bdd3886218dfe76e8560eb8a18401942452ae859-refs/heads/5.6.326@{#1}
Cr-Branched-From: 879f6599eee6e1dfcbe9a24bf688b261c03e9558-refs/heads/master@{#41014}

[modify] https://crrev.com/bd54aa2c9039a141b09d2456f8d7297ae3f5baf8/src/compiler/representation-change.cc
[add] https://crrev.com/bd54aa2c9039a141b09d2456f8d7297ae3f5baf8/test/mjsunit/compiler/regress-673244.js


### ha...@chromium.org (2017-03-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-03-21)

This issue was migrated from crbug.com/chromium/673244?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-07)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/chrome-blintz-user-guide

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086197)*
