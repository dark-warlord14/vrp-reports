# DCHECK failure in V8_EXTERNAL_CODE_SPACE_BOOL implies !IsCodeSpaceObject(object) in mark-compact.c

| Field | Value |
|-------|-------|
| **Issue ID** | [40818663](https://issues.chromium.org/issues/40818663) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P4 |
| **Component** | Blink>JavaScript |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | is...@chromium.org |
| **Created** | 2022-01-26 |
| **Bounty** | $6,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=6525770746626048

Fuzzer: decoder_langfuzz
Job Type: linux_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  V8_EXTERNAL_CODE_SPACE_BOOL implies !IsCodeSpaceObject(object) in mark-compact.c
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_d8_dbg&range=78773:78774

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6525770746626048

Issue filed automatically.

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Timeline

### cl...@chromium.org (2022-01-26)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/fd608d18b59eaaafa8928fe49fc7624f31bcccfa ([ext-code-space] Enable external code space on x64 and desktop arm64).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### [Deleted User] (2022-01-26)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-01-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/590dddbd1bc841fd8b083d8863a11706acf2d933

commit 590dddbd1bc841fd8b083d8863a11706acf2d933
Author: Igor Sheludko <ishell@chromium.org>
Date: Thu Jan 27 12:55:43 2022

[ext-code-space][heap] Fix EvacuateRecordOnlyVisitor

... which was using incorrect cage base value for reading map field.

Drive-by: fix CodeDataContainer verifier - the value returned by
code().InstructionStart() might not always be equal to cached code
entry point value when shared pointer compression cage is enabled.

Bug: v8:11880, chromium:1291299
Change-Id: I1338717095a9a1ad2c056f0af0181eabaef88431
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3420308
Reviewed-by: Dominik Inführ <dinfuehr@chromium.org>
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Cr-Commit-Position: refs/heads/main@{#78815}

[modify] https://crrev.com/590dddbd1bc841fd8b083d8863a11706acf2d933/src/diagnostics/objects-debug.cc
[modify] https://crrev.com/590dddbd1bc841fd8b083d8863a11706acf2d933/src/heap/mark-compact.cc


### is...@chromium.org (2022-01-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-01-27)

ClusterFuzz testcase 6525770746626048 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_d8_dbg&range=78775:78776

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2022-01-27)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-27)

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M99. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@chromium.org (2022-01-27)

Nothing has to be merged to M99 because the external code space is disabled there.

### is...@chromium.org (2022-01-27)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-31)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-31)

Congratulations! The VRP Panel has decided to award you $5,000 for this report + $1,000 fuzzer bonus. Thank you for your contributions to Chrome Fuzzing!! 

### am...@google.com (2022-04-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-05-05)

This issue was migrated from crbug.com/chromium/1291299?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40818663)*
