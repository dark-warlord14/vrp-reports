# DCHECK failure in current_ == next_ in node.h

| Field | Value |
|-------|-------|
| **Issue ID** | [40090214](https://issues.chromium.org/issues/40090214) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Compiler |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ja...@chromium.org |
| **Created** | 2018-01-17 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=5874775150034944

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  current_ == next_ in node.h
  v8::internal::compiler::Node::Uses::const_iterator::operator++
  v8::internal::compiler::DeadCodeElimination::ReduceLoopOrMerge
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=47073:47074

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5874775150034944

Issue filed automatically.

See https://github.com/google/clusterfuzz-tools for more information.

## Timeline

### cl...@chromium.org (2018-01-17)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript>Compiler]

### cl...@chromium.org (2018-01-17)

Automatically adding ccs based on suspected regression changelists:

[Turbofan] New DCHECK to ensure no use is mutated when iterating through them by alexandret@google.com - https://chromium.googlesource.com/v8/v8/+/47a15c62936dd71dff0b3906b60c43a4ea25031d

If this is incorrect, please apply the Test-Predator-Wrong-CLs label.

### sh...@chromium.org (2018-01-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-01-17)

Alexandre is not a member any more.
Jaro, can you take a look at this? You reviewed the CL which introduced the DCHECK.

### np...@chromium.org (2018-01-20)

[Empty comment from Monorail migration]

### np...@chromium.org (2018-01-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-01-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/b71133245c24149786942793ce3fa1462e9b02d9

commit b71133245c24149786942793ce3fa1462e9b02d9
Author: Jaroslav Sevcik <jarin@chromium.org>
Date: Tue Jan 23 17:07:57 2018

[turbofan] Fix dead loop exit removal.

This delays removing dead loop's loop exits after we iterate all uses of
the loop. That way, we avoid mutating the use collection while iterating
it.

Bug: chromium:803022
Change-Id: I17462dd82c3cb78f2f630e5db81d8ccdcc517d83
Reviewed-on: https://chromium-review.googlesource.com/878329
Reviewed-by: Michael Stanton <mvstanton@chromium.org>
Commit-Queue: Jaroslav Sevcik <jarin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#50813}
[modify] https://crrev.com/b71133245c24149786942793ce3fa1462e9b02d9/src/compiler/dead-code-elimination.cc
[add] https://crrev.com/b71133245c24149786942793ce3fa1462e9b02d9/test/mjsunit/compiler/regress-803022.js


### cl...@chromium.org (2018-01-24)

ClusterFuzz has detected this issue as fixed in range 50812:50813.

Detailed report: https://clusterfuzz.com/testcase?key=5874775150034944

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  current_ == next_ in node.h
  v8::internal::compiler::Node::Uses::const_iterator::operator++
  v8::internal::compiler::DeadCodeElimination::ReduceLoopOrMerge
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=47073:47074
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=50812:50813

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5874775150034944

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2018-01-24)

ClusterFuzz testcase 5874775150034944 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### aw...@chromium.org (2018-02-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-02-06)

Hi decoder - this one wasn't also hit by internal fuzzers!  $3,000 for the bug and $500 fuzzer bonus.  Thanks!

### aw...@chromium.org (2018-02-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-16)

This bug requires manual review: M66 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), josafat@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2018-03-19)

Seems like the fix landed in Jan, before branch for 66. No merge needed. 

### aw...@google.com (2018-04-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-05-02)

This issue was migrated from crbug.com/chromium/803022?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript, Blink>JavaScript>Compiler]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-07)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/chrome-blintz-user-guide

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090214)*
