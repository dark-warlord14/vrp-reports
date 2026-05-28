# Security: Type confusion in VisitFindNonDefaultConstructorOrConstruct of Maglev

| Field | Value |
|-------|-------|
| **Issue ID** | [40067530](https://issues.chromium.org/issues/40067530) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m-...@github.com |
| **Assignee** | ve...@chromium.org |
| **Created** | 2023-07-17 |
| **Bounty** | $21,000.00 |

## Description

Vulnerability Details

In the maglev implementation of `VisitFindNonDefaultConstructorOrConstruct`, if `new_target` is a constant function, then the object will be constructed directly using the `initial_map` of `new_target` [1], [2].

```
void MaglevGraphBuilder::VisitFindNonDefaultConstructorOrConstruct() {  
  ...  
          compiler::OptionalHeapObjectRef new_target_function =  
              TryGetConstant(new_target);  
          if (kind == FunctionKind::kDefaultBaseConstructor) {  
            ValueNode\* object;  
            if (new_target_function && new_target_function->IsJSFunction()) {  
              object = BuildAllocateFastObject(  
                  FastObject(new_target_function->AsJSFunction(), zone(),  
                             broker()),  
                  AllocationType::kYoung);  

```

This, however, has a couple of problems. First, when passing `new_target` to `FastObject`, it does not check whether `new_target` actually has an `initial_map`. If `new_target` is `Proxy`, then it will try to use the `initial_map` field [3] in the corresponding `JSFunctionData`. For functions that does not have an `initial_map`, this would be null and so this would only result in a NULL pointer dereference, rather than a security issue.

A more serious issue is that, `BuildAllocateFastObject` does not check whether the `constructor` field of `initial_map` is the same as the `target` function. The implementation in `FastNewObject` bails out to `Runtime::kNewObject` when `target` and the constructor of `new_target` differs [4], which calls `JSObject::New` and then calls `JSFunction::GetDerivedMap` to create the correct `initial_map` [5] to create the object.

This results in the object created by the maglev implementation to have an inconsistent object layout and map, which causes type confusion.

1. <https://source.chromium.org/chromium/chromium/src/+/ecca8fb3876014c0c5f245df70d7e45e07711e69:v8/src/maglev/maglev-graph-builder.cc;l=5384;bpv=0>
2. <https://source.chromium.org/chromium/chromium/src/+/ecca8fb3876014c0c5f245df70d7e45e07711e69:v8/src/maglev/maglev-graph-builder.cc;l=8024;bpv=0>
3. <https://source.chromium.org/chromium/chromium/src/+/9fa308f2af6566a1feabf5bafef0240cfc6cce33:v8/src/compiler/heap-refs.cc;l=498>
4. <https://source.chromium.org/chromium/chromium/src/+/9fa308f2af6566a1feabf5bafef0240cfc6cce33:v8/src/builtins/builtins-constructor-gen.cc;l=313;bpv=0;bpt=0>
5. <https://source.chromium.org/chromium/chromium/src/+/a328097ef1d47f51e76917b80110863037f4f744:v8/src/objects/js-objects.cc;l=2392;bpv=1;bpt=0>

Thank you very much for your help and please let me know if there is anything I can help. The issue appears to be introduced in this commit: <https://source.chromium.org/chromium/_/chromium/v8/v8.git/+/fdc017c89bf910e16f1fa5c6c16022e9e019c6a1> and the earliest release that contains it seems to be 115.

Man Yue Mo of GitHub Security Lab

**REPRODUCTION CASE**

To reproduce the issue, run the attached `super_ctor.js` with `d8`. Note that although the flag `--maglev` is needed in standalone d8, production Chrome has enabled maglev in 114 and passed this flag to the renderer, so this is not a behind flag feature:

```
./d8 --maglev super_ctor.js  

```

This creates a `Function` object with incorrect object memory layout and crashes the renderer. The `proxy.js` file demonstrates the NULL pointer dereference crash that was mentioned in the report.

**VERSION**  

Chrome version: d8 main branch commit 4c11841 and version 11.5.150.16 (which is used in the early stable release of Chrome)  

Operating System: Ubuntu 22.04  

**CREDIT INFORMATION**  

Reporter credit: Man Yue Mo of GitHub Security Lab

## Attachments

- [super_ctor.js](attachments/super_ctor.js) (text/plain, 275 B)
- [proxy.js](attachments/proxy.js) (text/plain, 219 B)
- [exploit.js](attachments/exploit.js) (text/plain, 4.3 KB)

## Timeline

### [Deleted User] (2023-07-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-07-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5949794280996864.

### cl...@chromium.org (2023-07-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5255424099680256.

### cl...@chromium.org (2023-07-17)

[Empty comment from Monorail migration]

### bo...@google.com (2023-07-17)

ClusterFuzz confirms reproducibility, so I'm setting provisional values for security flags. 

Routing to on-duty V8 security sheriff for further assessment. 

[Monorail components: Blink>JavaScript>Compiler>Turbofan]

### [Deleted User] (2023-07-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-07-17)

Detailed Report: https://clusterfuzz.com/testcase?key=5255424099680256

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: CHECK failure
Crash Address: 
Crash State:
  (data_) != nullptr in heap-refs.h
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=87738:87739

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5255424099680256

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### [Deleted User] (2023-07-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-07-17)

Detailed Report: https://clusterfuzz.com/testcase?key=5949794280996864

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  kCanBeWeak || (!IsSmi() == HAS_STRONG_HEAP_OBJECT_TAG(ptr_)) in tagged-impl.h
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=87738:87739

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5949794280996864

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### [Deleted User] (2023-07-17)

[Empty comment from Monorail migration]

### is...@chromium.org (2023-07-18)

Thank you for the report! Assigning to the culprit CL author.

[Monorail components: -Blink>JavaScript>Compiler>Turbofan Blink>JavaScript>Compiler>Maglev]

### ve...@chromium.org (2023-07-18)

Doh. Thanks for the report! Fixing in https://chromium-review.googlesource.com/c/v8/v8/+/4694007

### gi...@appspot.gserviceaccount.com (2023-07-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/ed93bef7ab786d5367c2ae7882922c23aa0eda64

commit ed93bef7ab786d5367c2ae7882922c23aa0eda64
Author: Toon Verwaest <verwaest@chromium.org>
Date: Tue Jul 18 13:48:29 2023

[maglev] Fix default constructor instantiation

The new.target may not be in the correct state for fast instantiation.

Bug: v8:7700, chromium:1465326
Change-Id: I09f92576c0b5573e902ae3b2210a7b5fdbd1e415
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4694007
Commit-Queue: Toon Verwaest <verwaest@chromium.org>
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Cr-Commit-Position: refs/heads/main@{#89006}

[modify] https://crrev.com/ed93bef7ab786d5367c2ae7882922c23aa0eda64/src/maglev/maglev-graph-builder.h
[add] https://crrev.com/ed93bef7ab786d5367c2ae7882922c23aa0eda64/test/mjsunit/maglev/regress/regress-crbug-1465326.js
[modify] https://crrev.com/ed93bef7ab786d5367c2ae7882922c23aa0eda64/src/maglev/maglev-graph-builder.cc


### [Deleted User] (2023-07-18)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### m-...@github.com (2023-07-19)

Thanks. The patch looks good, although it may be good to withhold regression tests until after the release for security issues. Please find attached an exploit that uses this vulnerability to run shell code in d8. It is tested on version 11.5.150.16 of d8:
```
./d8 --maglev exploit.js
oobDblAddr: 421e9
oobDblArr new length: 256
oobDblAddr2: 42251
oobObjAddr: 42299
func Addr: 19bf6d
code Addr: 19eb79
maglev Addr: e000d900 55d6
$ 
```

### ve...@chromium.org (2023-07-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-19)

[Empty comment from Monorail migration]

### ve...@chromium.org (2023-07-19)

Thanks for verifying! Nice little exploit :-)

### [Deleted User] (2023-07-19)

Merge review required: M116 is already shipping to beta.

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
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-19)

Merge review required: M115 is already shipping to stable.

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
Owners: govind (Android), govind (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2023-07-19)

ClusterFuzz testcase 5949794280996864 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=89005:89006

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### ve...@chromium.org (2023-07-19)

1. Yes: security fix
2. https://chromium-review.googlesource.com/c/v8/v8/+/4694007
3. Not on canary yet. Rolled into chrome at 171985
4. Yes, V8Maglev
5. N/A
6. No 

### [Deleted User] (2023-07-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-19)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-07-19)

maglev was launch in 114 so this should also be backmerged to 114, which is now Extended Stable, at the appropriate time
since this fix just landed <24 hours ago, going to defer merge review until tomorrow 

### [Deleted User] (2023-07-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-20)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=1465326&entry.364066060=External&entry.958145677=Android&entry.958145677=Chrome&entry.958145677=Fuchsia&entry.958145677=Linux&entry.958145677=Mac&entry.958145677=Windows&entry.958145677=Lacros&entry.763880440=Extended&entry.1678852700=High&entry.763402679=Blink>JavaScript>Compiler>Maglev&entry.975983575=verwaest@chromium.org Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### m-...@github.com (2023-07-20)

amyressler@ Even though maglev was launched in 114, I believe the bug was introduced in 115, (I just checked that the latest release of 114, which used 11.4.183.25, does not contain the bug) so there's probably no need to backmerge to 114.

### ve...@chromium.org (2023-07-20)

Indeed, I only asked for a backmerge to 115 and later because it was introduced in 115.

### am...@chromium.org (2023-07-21)

Thank you both Man Yu Mo and verwaest@ for letting me know this issue only goes back as far as 114. This issue was triaged as FoundIn-114 so I thought that Clusterfuzz made a undue change. 

M116 and M115 merges approved, please merge to 11.6-lkgr and 11.5-lkgr respectively at your earliest convenience so this fix can be included in the next 116/Beta and 115/Stable updates next week 

### gi...@appspot.gserviceaccount.com (2023-07-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/d15afca328ff671ff5990c38561f319bac1537b3

commit d15afca328ff671ff5990c38561f319bac1537b3
Author: Toon Verwaest <verwaest@chromium.org>
Date: Tue Jul 18 13:48:29 2023

Merged: [maglev] Fix default constructor instantiation

The new.target may not be in the correct state for fast instantiation.

(cherry picked from commit ed93bef7ab786d5367c2ae7882922c23aa0eda64)

Bug: v8:7700, chromium:1465326
Change-Id: I09f92576c0b5573e902ae3b2210a7b5fdbd1e415
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4694007
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4711048
Commit-Queue: Toon Verwaest <verwaest@chromium.org>
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Cr-Commit-Position: refs/branch-heads/11.5@{#37}
Cr-Branched-From: 0c4044b7336787781646e48b2f98f0c7d1b400a5-refs/heads/11.5.150@{#1}
Cr-Branched-From: b71d3038a7d99c79e1c21239e8ae07da5fc8c90b-refs/heads/main@{#87781}

[modify] https://crrev.com/d15afca328ff671ff5990c38561f319bac1537b3/src/maglev/maglev-graph-builder.h
[add] https://crrev.com/d15afca328ff671ff5990c38561f319bac1537b3/test/mjsunit/maglev/regress/regress-crbug-1465326.js
[modify] https://crrev.com/d15afca328ff671ff5990c38561f319bac1537b3/src/maglev/maglev-graph-builder.cc


### [Deleted User] (2023-07-24)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-07-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/896deb576574f1dd27d6dccc025fa6ac4b4c5ba7

commit 896deb576574f1dd27d6dccc025fa6ac4b4c5ba7
Author: Toon Verwaest <verwaest@chromium.org>
Date: Tue Jul 18 13:48:29 2023

Merged: [maglev] Fix default constructor instantiation

The new.target may not be in the correct state for fast instantiation.

(cherry picked from commit ed93bef7ab786d5367c2ae7882922c23aa0eda64)

Bug: v8:7700, chromium:1465326
Change-Id: I09f92576c0b5573e902ae3b2210a7b5fdbd1e415
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4694007
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4711047
Auto-Submit: Toon Verwaest <verwaest@chromium.org>
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Commit-Queue: Leszek Swirski <leszeks@chromium.org>
Cr-Commit-Position: refs/branch-heads/11.6@{#20}
Cr-Branched-From: e29c028f391389a7a60ee37097e3ca9e396d6fa4-refs/heads/11.6.189@{#3}
Cr-Branched-From: 95cbef20e2aa556a1ea75431a48b36c4de6b9934-refs/heads/main@{#88340}

[modify] https://crrev.com/896deb576574f1dd27d6dccc025fa6ac4b4c5ba7/src/maglev/maglev-graph-builder.h
[add] https://crrev.com/896deb576574f1dd27d6dccc025fa6ac4b4c5ba7/test/mjsunit/maglev/regress/regress-crbug-1465326.js
[modify] https://crrev.com/896deb576574f1dd27d6dccc025fa6ac4b4c5ba7/src/maglev/maglev-graph-builder.cc


### gi...@appspot.gserviceaccount.com (2023-07-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4b5d3ab5d6fe5b71e40d77e8f4df3f0659c4833c

commit 4b5d3ab5d6fe5b71e40d77e8f4df3f0659c4833c
Author: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Date: Mon Jul 24 14:43:22 2023

Roll v8 11.5 from b78fc4345a6e to 34340db35ab9 (2 revisions)

https://chromium.googlesource.com/v8/v8.git/+log/b78fc4345a6e..34340db35ab9

2023-07-24 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.5.150.19
2023-07-24 verwaest@chromium.org Merged: [maglev] Fix default constructor instantiation

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/v8-11-5-chromium-m115
Please CC liviurau@google.com,v8-waterfall-sheriff@grotations.appspotmail.com,vahl@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in v8 11.5: https://bugs.chromium.org/p/v8/issues/entry
To file a bug in Chromium m115: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1465326
Tbr: v8-waterfall-sheriff@grotations.appspotmail.com
Change-Id: I2242c968b4908c6c95d2e9bee8a4ac097b20b875
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4711227
Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5790@{#1811}
Cr-Branched-From: 1d71a337b1f6e707a13ae074dca1e2c34905eb9f-refs/heads/main@{#1148114}

[modify] https://crrev.com/4b5d3ab5d6fe5b71e40d77e8f4df3f0659c4833c/DEPS


### gi...@appspot.gserviceaccount.com (2023-07-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bde5ec76f634de6b36b9975061244b9ac18b608c

commit bde5ec76f634de6b36b9975061244b9ac18b608c
Author: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Date: Mon Jul 24 17:44:14 2023

Roll v8 11.6 from aed1c67f1f98 to dc8603588d80 (2 revisions)

https://chromium.googlesource.com/v8/v8.git/+log/aed1c67f1f98..dc8603588d80

2023-07-24 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.6.189.13
2023-07-24 verwaest@chromium.org Merged: [maglev] Fix default constructor instantiation

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/v8-11-6-chromium-m116
Please CC liviurau@google.com,v8-waterfall-sheriff@grotations.appspotmail.com,vahl@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in v8 11.6: https://bugs.chromium.org/p/v8/issues/entry
To file a bug in Chromium m116: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1465326
Tbr: v8-waterfall-sheriff@grotations.appspotmail.com
Change-Id: I98ceaddc5a0ac513424650a11111c3dc21d5e78b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4711530
Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5845@{#752}
Cr-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}

[modify] https://crrev.com/bde5ec76f634de6b36b9975061244b9ac18b608c/DEPS


### vo...@google.com (2023-07-25)

Not applicable to M108 LTS, since the issue was introduced in M115 according to the report.

### vo...@google.com (2023-07-26)

[Empty comment from Monorail migration]

### am...@google.com (2023-07-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-07-27)

Congratulations Man Yue Mo! The VRP Panel has decided to award you $20,000 for this report + V8 exploit bonus + $1,000 bisect bonus. Thank you for your efforts in discovering and reporting this issue and exploit to us -- great work! 

### m-...@github.com (2023-07-28)

amyressler@ Thank you very much. I would like to denote the reward please. Thanks.

### am...@chromium.org (2023-07-28)

Thank you for the heads-up and for choosing to donate your reward. I'll aim to get you the donation info early next week. 

### rz...@google.com (2023-07-31)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-08-01)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-02)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-08-02)

As per request (c#40), this reward has been processed for donation. The reward amount has been doubled and information for donating the reward has been sent. Thank you again for your report and choosing to donate this reward! 

### pg...@google.com (2023-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1465326?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40067530)*
