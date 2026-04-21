# Security: V8: Fatal error in ../../src/objects/property-array-inl.h

| Field | Value |
|-------|-------|
| **Issue ID** | [40070732](https://issues.chromium.org/issues/40070732) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sw...@gmail.com |
| **Assignee** | ol...@chromium.org |
| **Created** | 2023-08-28 |
| **Bounty** | $7,000.00 |

## Description

deleted

## Attachments

- [aaa.js](attachments/aaa.js) (text/plain, 529 B)

## Timeline

### [Deleted User] (2023-08-28)

[Empty comment from Monorail migration]

### sw...@gmail.com (2023-08-28)

REPRODUCTION CASE (Update):

latest d8-asan debug windows version:https://www.googleapis.com/download/storage/v1/b/v8-asan/o/win64-debug%2Fd8-asan-win64-debug-v8-component-89635.zip?generation=1693119826785030&alt=media

run:
.\d8.exe --jit-fuzzing  --assert-types aaa.js

crash info:
```
#
# Fatal error in ..\..\src\objects\property-array-inl.h, line 57
# Debug check failed: static_cast<unsigned>(index) < static_cast<unsigned>(this->length(kAcquireLoad)) (2 vs. 2).
#
#
#
#FailureMessage Object: 000001E000C5B040
==== C stack trace ===============================

        v8::base::debug::StackTrace::StackTrace [0x00007FF73942DB43+35] (C:\b\s\w\ir\cache\builder\v8\src\base\debug\stack_trace_win.cc:173)
        v8::platform::`anonymous namespace'::PrintStackTrace [0x00007FF7392D0D9D+349] (C:\b\s\w\ir\cache\builder\v8\src\libplatform\default-platform.cc:28)
        V8_Fatal [0x00007FF7392B73AD+525] (C:\b\s\w\ir\cache\builder\v8\src\base\logging.cc:164)
        v8::base::`anonymous namespace'::DefaultDcheckHandler [0x00007FF7392B67B8+40] (C:\b\s\w\ir\cache\builder\v8\src\base\logging.cc:57)
        v8::internal::PropertyArray::set [0x00007FF734977E6F+927] (C:\b\s\w\ir\cache\builder\v8\src\objects\property-array-inl.h:56)
        v8::internal::`anonymous namespace'::MigrateFastToFast [0x00007FF73562F285+23205] (C:\b\s\w\ir\cache\builder\v8\src\objects\js-objects.cc:3198)
        v8::internal::JSObject::MigrateToMap [0x00007FF735623E06+1846] (C:\b\s\w\ir\cache\builder\v8\src\objects\js-objects.cc:3478)
        v8::internal::LookupIterator::ApplyTransitionToDataProperty [0x00007FF7358FC80D+5901] (C:\b\s\w\ir\cache\builder\v8\src\objects\lookup.cc:672)
        v8::internal::Object::TransitionAndWriteDataProperty [0x00007FF735A85B6E+462] (C:\b\s\w\ir\cache\builder\v8\src\objects\objects.cc:2655)
        v8::internal::Object::AddDataProperty [0x00007FF735A82E90+5776] (C:\b\s\w\ir\cache\builder\v8\src\objects\objects.cc:2637)
        v8::internal::JSObject::DefineOwnPropertyIgnoreAttributes [0x00007FF7355E4AB4+1620] (C:\b\s\w\ir\cache\builder\v8\src\objects\js-objects.cc:3775)
        v8::internal::__RT_impl_Runtime_DefineKeyedOwnPropertyInLiteral [0x00007FF73621855F+6095] (C:\b\s\w\ir\cache\builder\v8\src\runtime\runtime-object.cc:1164)
        v8::internal::Runtime_DefineKeyedOwnPropertyInLiteral [0x00007FF73621611C+572] (C:\b\s\w\ir\cache\builder\v8\src\runtime\runtime-object.cc:1114)
        Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit [0x00007FF73979CFBA+58]
        (No symbol) [0x00007FF799704686]
```

### cl...@chromium.org (2023-08-29)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6519177042657280.

### cl...@chromium.org (2023-08-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-08-29)

Detailed Report: https://clusterfuzz.com/testcase?key=6519177042657280

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  static_cast<unsigned>(index) < static_cast<unsigned>(this->length(kAcquireLoad))
  v8::internal::PropertyArray::set
  v8::internal::MigrateFastToFast
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=89062:89063

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6519177042657280

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2023-08-29)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript>Runtime]

### cl...@chromium.org (2023-08-29)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/793922fb00cdf505bcbe477de8bcb7d2b9463c51 (Reland "[maglev] Enable by default on desktop").

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### vi...@chromium.org (2023-08-29)

This seems to be an issue with Maglev calling CloneObjectIC. The returned object is bogus, then setting a property crashes.

### vi...@chromium.org (2023-08-29)

Smaller repro:

```
function mk(x) {
    const o = { a: 0 };
    o.b = x;
    return o;
}

const x = mk();
x.a = {};
mk(0);

function foo() {
    const o1 = {
        ...x,
        c: {},
        [{}]: 0,
    };
    const o2 = {
        __proto__: x,
        c: undefined,
    };
}

%PrepareFunctionForOptimization(foo);
foo(); // CloneIC goes mono
foo(); // CloneIC goes poly
// %OptimizeMaglevOnNextCall(foo);
%OptimizeFunctionOnNextCall(foo);
foo(); // CloneIC creates a bogus object with wrong property array size.
```

### ol...@chromium.org (2023-08-29)

thanks for triaging. fix is coming.

### ol...@chromium.org (2023-08-29)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-08-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/d0dc4fcd0112a640a3c629c48fe790c3fa76bb3c

commit d0dc4fcd0112a640a3c629c48fe790c3fa76bb3c
Author: Olivier Flückiger <olivf@chromium.org>
Date: Tue Aug 29 14:12:46 2023

[ic] Prevent clone ic fastcase on properties size mismatch

The clone ic blindly copies the properties backing store, thus source
and target map better have the same sized backing store.

Bug: chromium:1476373
Change-Id: Iecb173aa638ebae95e7ac6bcb30274c4a37f20d9
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4823163
Commit-Queue: Olivier Flückiger <olivf@chromium.org>
Auto-Submit: Olivier Flückiger <olivf@chromium.org>
Commit-Queue: Leszek Swirski <leszeks@chromium.org>
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Cr-Commit-Position: refs/heads/main@{#89683}

[modify] https://crrev.com/d0dc4fcd0112a640a3c629c48fe790c3fa76bb3c/src/ic/ic.cc


### [Deleted User] (2023-08-29)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-29)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ol...@chromium.org (2023-08-29)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-29)

Thank you for the fix! Marking the bug as fixed (fix = work completed on main and may need merges. This then lets the automation route the bugs to the right places)

### cl...@chromium.org (2023-08-30)

ClusterFuzz testcase 6519177042657280 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=89682:89683

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2023-08-30)

Merge review required: M117 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: harrysouders (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-30)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-31)

Merge approved for M117! Please merge to the appropriate v8 branch by Thursday Aug 31 EOD (MTV time) to get this into M117's stable cut!

### pg...@google.com (2023-08-31)

Setting OSes liberally - if any platform is certainly not impacted, please feel free to remove!

### gi...@appspot.gserviceaccount.com (2023-08-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/7ab19060b4c30cf00b3b09f28d4126110dc32d34

commit 7ab19060b4c30cf00b3b09f28d4126110dc32d34
Author: Olivier Flückiger <olivf@chromium.org>
Date: Tue Aug 29 14:12:46 2023

Merged: [ic] Prevent clone ic fastcase on properties size mismatch

The clone ic blindly copies the properties backing store, thus source
and target map better have the same sized backing store.

Bug: chromium:1476373
(cherry picked from commit d0dc4fcd0112a640a3c629c48fe790c3fa76bb3c)

Change-Id: I134f9ff42b637541674a2fad03208cb723244e85
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4828324
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Auto-Submit: Olivier Flückiger <olivf@chromium.org>
Commit-Queue: Leszek Swirski <leszeks@chromium.org>
Cr-Commit-Position: refs/branch-heads/11.7@{#22}
Cr-Branched-From: fe608691065e23ae83720392bf61a59e8166bee6-refs/heads/11.7.439@{#1}
Cr-Branched-From: aeb45525398afa173aa91fcf83eb6341c83850ea-refs/heads/main@{#89415}

[modify] https://crrev.com/7ab19060b4c30cf00b3b09f28d4126110dc32d34/src/ic/ic.cc


### [Deleted User] (2023-08-31)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ol...@chromium.org (2023-08-31)

sorry I am not sure I understand what "Was this issue a regression for the milestone it was found in?" is supposed to mean. it's an issue for the 117 milestone, where it was found in. but not for 114 where it was not found in. so I guess the answer is no?

### is...@chromium.org (2023-09-04)

I guess in the context of "LTS Milestone M114" the answers should be:
1. No
2. Yes

### [Deleted User] (2023-09-04)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ol...@chromium.org (2023-09-04)

[Empty comment from Monorail migration]

### vo...@google.com (2023-09-05)

Recent regression - not applicable to LTS branches.

### am...@chromium.org (2023-09-11)

[Description Changed]

### am...@google.com (2023-09-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-14)

Congratulations Zhenjiang Zhao! The VPR Panel has decided to award you $7,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-09-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1476373?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40070732)*
