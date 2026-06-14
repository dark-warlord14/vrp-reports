# Fatal error in ../../v8/src/compiler/representation-change.cc, line 1055

| Field | Value |
|-------|-------|
| **Issue ID** | [40088378](https://issues.chromium.org/issues/40088378) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Windows |
| **Reporter** | mg...@gmail.com |
| **Assignee** | te...@chromium.org |
| **Created** | 2017-07-17 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0

Steps to reproduce the problem:
Unfortunately I could not isolate the problem for an easy repro.
I have a JS app of around 3mb minified and the browser crashes at what seem to be random times (I suppose whenever it decides to optimize the problematic function)

What is the expected behavior?
not crash

What went wrong?
Fatal error in ../../v8/src/compiler/representation-change.cc, line 1055
RepresentationChangerError: node #812:Phi of kRepFloat64 (Number) cannot be changed to kRepWord32

STACK_TEXT:  
0x0
v8_libbase!v8::base::OS::Abort+0x11
v8_libbase!V8_Fatal+0x91
v8!v8::internal::compiler::RepresentationChanger::TypeError+0x1d9
v8!v8::internal::compiler::RepresentationChanger::GetWord32RepresentationFor+0x18d
v8!v8::internal::compiler::RepresentationChanger::GetRepresentationFor+0x28d
v8!v8::internal::compiler::RepresentationSelector::ConvertInput+0x19d
v8!v8::internal::compiler::RepresentationSelector::VisitPhi+0x12c
v8!v8::internal::compiler::RepresentationSelector::VisitNode+0x31f
v8!v8::internal::compiler::RepresentationSelector::Run+0x4ea
v8!v8::internal::compiler::SimplifiedLowering::LowerAllNodes+0x4c
v8!v8::internal::compiler::PipelineImpl::Run<v8::internal::compiler::SimplifiedLoweringPhase>+0x70
v8!v8::internal::compiler::PipelineImpl::OptimizeGraph+0x29f
v8!v8::internal::compiler::PipelineCompilationJob::ExecuteJobImpl+0x20
v8!v8::internal::CompilationJob::ExecuteJob+0x1a3
v8!v8::internal::OptimizingCompileDispatcher::CompileTask::Run+0x110
gin!base::internal::FunctorTraits<void (__cdecl v8::Task::*)(void) __ptr64,void>::Invoke<v8::Task * __ptr64>+0x1a
gin!base::internal::InvokeHelper<0,void>::MakeItSo<void (__cdecl v8::Task::*const & __ptr64)(void) __ptr64,v8::Task * __ptr64>+0x37
gin!base::internal::Invoker<base::internal::BindState<void (__cdecl v8::Task::*)(void) __ptr64,base::internal::OwnedWrapper<v8::Task> >,void __cdecl(void)>::RunImpl<void (__cdecl v8::Task::*const & __ptr64)(void) __ptr64,std::tuple<base::internal::OwnedWrapper<v8::Task> > const & __ptr64,0>+0x49
gin!base::internal::Invoker<base::internal::BindState<void (__cdecl v8::Task::*)(void) __ptr64,base::internal::OwnedWrapper<v8::Task> >,void __cdecl(void)>::Run+0x33
base!base::Callback<void __cdecl(void),0,0>::Run+0x40
base!base::debug::TaskAnnotator::RunTask+0x2fd
base!base::internal::TaskTracker::PerformRunTask+0x74b
base!base::internal::TaskTracker::RunNextTask+0x1ea
base!base::internal::SchedulerWorker::Thread::ThreadMain+0x4b9
base!base::`anonymous namespace'::ThreadFunc+0x131
KERNEL32!BaseThreadInitThunk+0x14
ntdll!RtlUserThreadStart+0x21

Did this work before? N/A 

Chrome version: 61.0.3158.0  Channel: canary
OS Version: 10.0
Flash Version: Shockwave Flash 25.0 r0

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### mg...@gmail.com (2017-07-17)

minidump file create with windbg x64

### dt...@chromium.org (2017-07-17)

[Empty comment from Monorail migration]

[Monorail components: -Blink Blink>JavaScript]

### aj...@chromium.org (2017-07-19)

Cc'ing 	jarin@ for help in further investigation and if this is related to https://crbug.com/chromium/741225.

[Monorail components: -Blink>JavaScript Blink>JavaScript>Compiler]

### ja...@chromium.org (2017-07-19)

Without some kind of repro, it will be hard to make progress here. Are you sure you can share some repro instructions?



### mg...@gmail.com (2017-07-19)

[Comment Deleted]

### ja...@chromium.org (2017-07-19)

[Empty comment from Monorail migration]

### ja...@chromium.org (2017-07-19)

Thank you for the repro! I could reproduce the issue locally. We should have a fix ready soon.

### ja...@chromium.org (2017-07-20)

[Empty comment from Monorail migration]

### ha...@chromium.org (2017-07-20)

[Empty comment from Monorail migration]

### ha...@chromium.org (2017-07-20)

[Empty comment from Monorail migration]

### ha...@chromium.org (2017-07-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-07-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-07-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/a224eff455632df89377748421a23be47a5278e8

commit a224eff455632df89377748421a23be47a5278e8
Author: Tobias Tebbi <tebbi@chromium.org>
Date: Thu Jul 20 13:04:02 2017

[turbofan] escape analysis: fix typing of new phi nodes

Bug: chromium:744584
Change-Id: Ie25c2ba63e4764f359de38e53c2f3f3222877e0e
Reviewed-on: https://chromium-review.googlesource.com/577690
Reviewed-by: Jaroslav Sevcik <jarin@chromium.org>
Commit-Queue: Tobias Tebbi <tebbi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#46792}
[modify] https://crrev.com/a224eff455632df89377748421a23be47a5278e8/src/compiler/escape-analysis.cc
[add] https://crrev.com/a224eff455632df89377748421a23be47a5278e8/test/mjsunit/compiler/escape-analysis-phi-type-2.js
[add] https://crrev.com/a224eff455632df89377748421a23be47a5278e8/test/mjsunit/compiler/escape-analysis-phi-type.js


### te...@chromium.org (2017-07-21)

This is a Turbofan compiler bug that allows arbitrary out-of-bounds memory access. The patch is safe to back-merge.

### sh...@chromium.org (2017-07-21)

This bug requires manual review: We are only 3 days from stable.
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), josafat@(ChromeOS), bustamante@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### te...@chromium.org (2017-07-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-07-21)

[Empty comment from Monorail migration]

### ha...@chromium.org (2017-07-24)

Let's wait (2 days) for some proper Canary coverage. The branch cut obfuscates the stability data a little bit.

If everything is fine, we should merge it back to 6.0 and 6.1

### mg...@gmail.com (2017-07-24)

For my part, I can confirm the bug as fixed. Thank you.

### aw...@google.com (2017-07-24)

[Empty comment from Monorail migration]

### go...@chromium.org (2017-07-26)

Please merge your change to M61 branch #3163 before 4: 00 PM PT, Wednesday (07/26) in order to make it to last M61 dev release. Thank you.

### bu...@chromium.org (2017-07-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/81ccc6e1f31b6f7bcef19eeff321c56d947ba935

commit 81ccc6e1f31b6f7bcef19eeff321c56d947ba935
Author: Tobias Tebbi <tebbi@chromium.org>
Date: Wed Jul 26 12:40:37 2017

Merged: [turbofan] escape analysis: fix typing of new phi nodes

Revision: a224eff455632df89377748421a23be47a5278e8

BUG=chromium:744584
LOG=N
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=jarin@chromium.org

Change-Id: I3f3ec437c780a615b98767345b5eb88a05c2b0e6
Reviewed-on: https://chromium-review.googlesource.com/586329
Reviewed-by: Jaroslav Sevcik <jarin@chromium.org>
Commit-Queue: Tobias Tebbi <tebbi@chromium.org>
Cr-Commit-Position: refs/branch-heads/6.1@{#20}
Cr-Branched-From: 1bf2e10ddb194d4c2871a87a4732613419de892d-refs/heads/6.1.534@{#1}
Cr-Branched-From: e825c4318eb2065ffdf9044aa6a5278635c36427-refs/heads/master@{#46746}
[modify] https://crrev.com/81ccc6e1f31b6f7bcef19eeff321c56d947ba935/src/compiler/escape-analysis.cc
[add] https://crrev.com/81ccc6e1f31b6f7bcef19eeff321c56d947ba935/test/mjsunit/compiler/escape-analysis-phi-type-2.js
[add] https://crrev.com/81ccc6e1f31b6f7bcef19eeff321c56d947ba935/test/mjsunit/compiler/escape-analysis-phi-type.js


### go...@chromium.org (2017-07-26)

Pls merge you change to M61 branch 3163 by 5:00 PM today, Wednesday if possible so we can take it in for next week M61 last dev release. Thank you.

### bu...@chromium.org (2017-07-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/2f2f9be7727eac23248fd91a776959d51de6b7c6

commit 2f2f9be7727eac23248fd91a776959d51de6b7c6
Author: Tobias Tebbi <tebbi@chromium.org>
Date: Thu Jul 27 08:04:29 2017

Merged: [turbofan] escape analysis: fix typing of new phi nodes

Revision: a224eff455632df89377748421a23be47a5278e8

BUG=chromium:744584
LOG=N
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=jarin@chromium.org

Change-Id: I5007d4062878fa2586c5d9e85a264c19be056afb
Reviewed-on: https://chromium-review.googlesource.com/586530
Reviewed-by: Jaroslav Sevcik <jarin@chromium.org>
Cr-Commit-Position: refs/branch-heads/6.0@{#95}
Cr-Branched-From: 97dbf624a5eeffb3a8df36d24cdb2a883137385f-refs/heads/6.0.286@{#1}
Cr-Branched-From: 12e6f1cb5cd9616da7b9d4a7655c088778a6d415-refs/heads/master@{#45439}
[modify] https://crrev.com/2f2f9be7727eac23248fd91a776959d51de6b7c6/src/compiler/escape-analysis.cc
[add] https://crrev.com/2f2f9be7727eac23248fd91a776959d51de6b7c6/test/mjsunit/compiler/escape-analysis-phi-type-2.js
[add] https://crrev.com/2f2f9be7727eac23248fd91a776959d51de6b7c6/test/mjsunit/compiler/escape-analysis-phi-type.js


### sh...@chromium.org (2017-07-27)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-07-27)

Per https://crbug.com/chromium/744584#c22, this is already merged to M61. So removing "Merge-Approved-61" label. Thank you.

### sh...@chromium.org (2017-07-31)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### te...@chromium.org (2017-07-31)

Already merged to M60.

### aw...@chromium.org (2017-07-31)

[Empty comment from Monorail migration]

### aw...@google.com (2017-07-31)

Congratulations mgiova@! The VRP panel decided to award $3,000 for this report!  A member of our finance team will be in touch shortly to arrange payment. Cheers!

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************


### aw...@chromium.org (2017-07-31)

[Empty comment from Monorail migration]

### aw...@google.com (2017-09-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-09-06)

[Empty comment from Monorail migration]

### of...@google.com (2017-10-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/744584?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-07)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/chrome-blintz-user-guide

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088378)*
