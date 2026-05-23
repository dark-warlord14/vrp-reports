# Security: v8 Debug check failed: target_inobject < GetInObjectProperties().

| Field | Value |
|-------|-------|
| **Issue ID** | [40058061](https://issues.chromium.org/issues/40058061) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Turbofan |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | h4...@gmail.com |
| **Assignee** | jg...@chromium.org |
| **Created** | 2021-11-29 |
| **Bounty** | $5,000.00 |

## Description

uname -a
Linux work-VirtualBox 5.11.0-27-generic #29~20.04.1-Ubuntu SMP Wed Aug 11 15:58:17 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux

git checkout main
git pull

git log
commit de058e5497418388973d753a9b143da78e20bf1b (HEAD -> main, origin/main, origin/HEAD)
Author: Milad Fa <mfarazma@redhat.com>
Date:   Fri Nov 26 09:22:06 2021 -0500

    cppgc: Fix compilation error on gcc
    
    Fixing a dcheck compilation error missed by
    https://crrev.com/c/3302850
    
    Change-Id: I98c7394cbe64d99647656aebd175c8321f53c2de
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3300927
    Reviewed-by: Omer Katz <omerkatz@chromium.org>
    Commit-Queue: Milad Fa <mfarazma@redhat.com>
    Cr-Commit-Position: refs/heads/main@{#78112}

commit 7b1b62e56ec3978b8c5dee8cdc67437af5b28c3d


cat args.gn:
is_asan = true
symbol_level = 2
v8_enable_backtrace = true
is_debug = false
dcheck_always_on = true
v8_static_library = true
v8_enable_slow_dchecks = true
v8_enable_v8_checks = true
v8_enable_verify_heap = true
v8_enable_verify_csa = true
sanitizer_coverage_flags = "trace-pc-guard"
target_cpu = "x64"

 
./d8 -v
V8 version 9.8.0 (candidate)

About how to repro, this is not a bug that can be triggered stably. Execute the following script and it will crash after about 1-2 minutes:
python popen_repro.py ./d8_release_main map.cc.poc 

2021-11-29 10:12:25.602528
2021-11-29 10:12:26.168198
2021-11-29 10:12:26.712019
2021-11-29 10:12:27.222073
2021-11-29 10:12:27.785948
2021-11-29 10:12:28.303449
2021-11-29 10:12:28.810231


#
# Fatal error in ../../src/objects/map.cc, line 506
# Debug check failed: target_inobject < GetInObjectProperties().
#
#
#
#FailureMessage Object: 0x7fcb43ab4860
==== C stack trace ===============================

    ./d8_repro_main(__interceptor_backtrace+0x5b) [0x55917bcafaeb]
    ./d8_repro_main(v8::base::debug::StackTrace::StackTrace()+0x22) [0x55917bf55632]
    ./d8_repro_main(+0x1db26ef) [0x55917bf526ef]
    ./d8_repro_main(V8_Fatal(char const*, int, char const*, ...)+0x297) [0x55917bf38267]
    ./d8_repro_main(+0x1d96f6f) [0x55917bf36f6f]
    ./d8_repro_main(v8::internal::Map::InstancesNeedRewriting(v8::internal::Map, int, int, int, int*, v8::internal::ConcurrencyMode) const+0x54e) [0x55917d8c770e]
    ./d8_repro_main(v8::internal::Map::InstancesNeedRewriting(v8::internal::Map, v8::internal::ConcurrencyMode) const+0x365) [0x55917d8c6c65]
    ./d8_repro_main(v8::internal::Map::FindElementsKindTransitionedMap(v8::internal::Isolate*, std::__1::vector<v8::internal::Handle<v8::internal::Map>, std::__1::allocator<v8::internal::Handle<v8::internal::Map> > > const&, v8::internal::ConcurrencyMode)+0x6af) [0x55917d8cfaaf]
    ./d8_repro_main(v8::internal::compiler::JSHeapBroker::ProcessFeedbackMapsForElementAccess(v8::internal::ZoneVector<v8::internal::compiler::MapRef>&, v8::internal::compiler::KeyedAccessMode const&, v8::internal::FeedbackSlotKind)+0x7d6) [0x55917f800b96]
    ./d8_repro_main(v8::internal::compiler::JSHeapBroker::ReadFeedbackForPropertyAccess(v8::internal::compiler::FeedbackSource const&, v8::internal::compiler::AccessMode, v8::base::Optional<v8::internal::compiler::NameRef>)+0x19f2) [0x55917f7fed72]
    ./d8_repro_main(v8::internal::compiler::JSHeapBroker::GetFeedbackForPropertyAccess(v8::internal::compiler::FeedbackSource const&, v8::internal::compiler::AccessMode, v8::base::Optional<v8::internal::compiler::NameRef>)+0x1ca) [0x55917f80967a]
    ./d8_repro_main(v8::internal::compiler::JSNativeContextSpecialization::ReducePropertyAccess(v8::internal::compiler::Node*, v8::internal::compiler::Node*, v8::base::Optional<v8::internal::compiler::NameRef>, v8::internal::compiler::Node*, v8::internal::compiler::FeedbackSource const&, v8::internal::compiler::AccessMode)+0x555) [0x55917fdd5c55]
    ./d8_repro_main(v8::internal::compiler::JSNativeContextSpecialization::ReduceJSStoreProperty(v8::internal::compiler::Node*)+0x346) [0x55917fdbc706]
    ./d8_repro_main(v8::internal::compiler::GraphReducer::Reduce(v8::internal::compiler::Node*)+0x3ba) [0x55917fc0122a]
    ./d8_repro_main(v8::internal::compiler::GraphReducer::ReduceTop()+0x693) [0x55917fc00433]
    ./d8_repro_main(v8::internal::compiler::GraphReducer::ReduceNode(v8::internal::compiler::Node*)+0x124) [0x55917fbff064]
    ./d8_repro_main(v8::internal::compiler::InliningPhase::Run(v8::internal::compiler::PipelineData*, v8::internal::Zone*)+0x1dcd) [0x55917f67e8ed]
    ./d8_repro_main(void v8::internal::compiler::PipelineImpl::Run<v8::internal::compiler::InliningPhase>()+0x218) [0x55917f6411c8]
    ./d8_repro_main(v8::internal::compiler::PipelineImpl::CreateGraph()+0x2d4) [0x55917f634aa4]
    ./d8_repro_main(v8::internal::compiler::PipelineCompilationJob::ExecuteJobImpl(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x108) [0x55917f635318]
    ./d8_repro_main(v8::internal::OptimizedCompilationJob::ExecuteJob(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x236) [0x55917c374056]
    ./d8_repro_main(v8::internal::OptimizingCompileDispatcher::CompileNext(v8::internal::OptimizedCompilationJob*, v8::internal::LocalIsolate*)+0x5c) [0x55917c619d3c]
    ./d8_repro_main(v8::internal::OptimizingCompileDispatcher::CompileTask::RunInternal()+0x647) [0x55917c622357]
    ./d8_repro_main(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0x95) [0x55917bf78a95]
    ./d8_repro_main(+0x1dacd09) [0x55917bf4cd09]
    /lib/x86_64-linux-gnu/libpthread.so.0(+0x9609) [0x7fcb47dac609]
    /lib/x86_64-linux-gnu/libc.so.6(clone+0x43) [0x7fcb47b5e293]
Trace/breakpoint trap (core dumped)


## Attachments

- [map.cc.poc](attachments/map.cc.poc) (application/octet-stream, 2.0 KB)
- [popen_repro.py](attachments/popen_repro.py) (text/plain, 630 B)

## Timeline

### [Deleted User] (2021-11-29)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-11-29)

I’m unable to reproduce this.

jgruber: Can you take a look?

[Monorail components: Blink>JavaScript>Compiler]

### cl...@chromium.org (2021-11-29)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6464647575961600.

### jg...@chromium.org (2021-11-30)

From the backtrace, looks like a concurrent-inlining race at https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/map.cc;l=483;drc=c1d62d8428875969cdc66dade8090d8863b2561e, callsite https://source.chromium.org/chromium/chromium/src/+/main:v8/src/compiler/js-heap-broker.cc;l=904;drc=c1d62d8428875969cdc66dade8090d8863b2561e.

[Monorail components: -Blink>JavaScript>Compiler Blink>JavaScript>Compiler>Turbofan]

### jg...@chromium.org (2021-11-30)

I suspect this is not a security bug since immediately after the DCHECK we'd return:

  DCHECK(target_number_of_fields >= *old_number_of_fields);
  if (target_number_of_fields != *old_number_of_fields) return true;

Thus lowering prio.

I'm not sure I can get to this soon, anybody got space to pick this up? Setting a NextAction so we don't forget.

### do...@chromium.org (2021-12-08)

Sheriff ping: can someone please pick this up and finalise the investigation?

### me...@chromium.org (2021-12-14)

mvstanton: Could you PTAL or reassign as appropriate? Thanks.

### me...@chromium.org (2021-12-14)

[Empty comment from Monorail migration]

### me...@chromium.org (2021-12-16)

Adjusting labels based on https://crbug.com/chromium/1274445#c5.

### dr...@chromium.org (2022-01-07)

Chrome security sheriff here. mvstanton@ - are we now confident this isn't a security bug? If so, we can get it out of the security queue.

### te...@chromium.org (2022-01-10)

Reassigning to jgruber@ since mvstanton@ has left Google.

### jg...@chromium.org (2022-01-11)

[Empty comment from Monorail migration]

### jg...@chromium.org (2022-01-11)

I'll have another quick look at this today.

### jg...@chromium.org (2022-01-11)

Adding the reporter of the duped issue in #13.

### jg...@chromium.org (2022-01-11)

Reiterating my impression that this is not a security issue. If the DCHECK at https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/map.cc;l=485;drc=83fd7137dcf236a57a447904c082db821ce98779 fails, the next line returns `true`, i.e. the instances *do* need rewriting. In that case, the map candidate is skipped in https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/map.cc;l=908;drc=83fd7137dcf236a57a447904c082db821ce98779.

+cc Map expert ishell.

I'm tending towards dropping security labels but will wait for Igor's thoughts.

### jg...@chromium.org (2022-01-11)

Just realized that I misread the failing DCHECK in https://crbug.com/chromium/1274445#c4; it's actually 

DCHECK(target_inobject < GetInObjectProperties());

https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/map.cc;l=508;drc=83fd7137dcf236a57a447904c082db821ce98779

that is failing. Back to square one..

### jg...@chromium.org (2022-01-11)

Igor points out:

- ShrinkInstanceSize protects set_instance_size for each map individually (https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/map-updater.cc;l=433;drc=83fd7137dcf236a57a447904c082db821ce98779)
- but InstancesNeedRewriting expects a value relation between two maps (https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/map.cc;l=508;drc=83fd7137dcf236a57a447904c082db821ce98779).
- The fix is likely to exclusively lock the MapUpdater lock in CompleteInobjectSlackTracking (https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/map.cc;l=2159;drc=83fd7137dcf236a57a447904c082db821ce98779).

### gi...@appspot.gserviceaccount.com (2022-01-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/4b8d04897cba70cac45eea33d78fa2354dfe2bd7

commit 4b8d04897cba70cac45eea33d78fa2354dfe2bd7
Author: Jakob Gruber <jgruber@chromium.org>
Date: Thu Jan 13 07:01:37 2022

[maps] Lock map_updater_access in CompleteInobjectSlackTracking

CompleteInobjectSlackTracking potentially shrinks multiple maps, and
the relation between these maps should be preserved in a concurrent
environment. Thus it is not enough to make each modification
atomically, but all related map modifications must be within a
critical section.

We do this by locking the map_updater_access mutex
CompleteInobjectSlackTracking, and hence moving the function to the
MapUpdater class.

Bug: chromium:1274445,v8:7990
Change-Id: If99bb8b55e03180128ee397d845fa4c269c4241e
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3379819
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Commit-Queue: Jakob Gruber <jgruber@chromium.org>
Cr-Commit-Position: refs/heads/main@{#78597}

[modify] https://crrev.com/4b8d04897cba70cac45eea33d78fa2354dfe2bd7/src/objects/map.cc
[modify] https://crrev.com/4b8d04897cba70cac45eea33d78fa2354dfe2bd7/test/cctest/test-api.cc
[modify] https://crrev.com/4b8d04897cba70cac45eea33d78fa2354dfe2bd7/src/objects/map-updater.cc
[modify] https://crrev.com/4b8d04897cba70cac45eea33d78fa2354dfe2bd7/src/runtime/runtime-test.cc
[modify] https://crrev.com/4b8d04897cba70cac45eea33d78fa2354dfe2bd7/src/runtime/runtime-object.cc
[modify] https://crrev.com/4b8d04897cba70cac45eea33d78fa2354dfe2bd7/src/objects/map-updater.h
[modify] https://crrev.com/4b8d04897cba70cac45eea33d78fa2354dfe2bd7/src/objects/map-inl.h
[modify] https://crrev.com/4b8d04897cba70cac45eea33d78fa2354dfe2bd7/src/objects/js-function-inl.h
[modify] https://crrev.com/4b8d04897cba70cac45eea33d78fa2354dfe2bd7/src/objects/map.h


### jg...@chromium.org (2022-01-13)

Requesting merge of #19 once we have canary coverage.

### [Deleted User] (2022-01-13)

Merge rejected: M98 is already shipping to beta and this issue is marked as a Pri-2, Pri-3, or Type-Feature.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jg...@chromium.org (2022-01-13)

Updating priority and labels, re-requesting merge. Re-setting security impact since confusion around object shapes is usually delicate. Concurrent inlining is already enabled on stable.

### vi...@gmail.com (2022-01-13)

I　think the security impact is not none. because this   may be lead to type confusion

### ct...@chromium.org (2022-01-13)

> Re-setting security impact since confusion around object shapes is usually delicate.

Current security sheriff here: conservatively setting this as Severity-High in case this could be used to get code execution.

### ct...@chromium.org (2022-01-13)

And setting all Blink/V8 OS labels.

### [Deleted User] (2022-01-13)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-14)

Updating this issue as fixed based on fix CL + merge request. In the future, for security bug merges, once the fix CL is landed, please update the bug as Fixed so the bot can add the appropriate merge review labels. As this is a high-severity bug fix, it should be merged into all current release channels when appropriate to do so. 

As this fix landed <24 hours ago, going to give it a bit more bake time before approving. Please let me know if there are any issues or concerns with this. Thank you! 

### [Deleted User] (2022-01-14)

Merge review required: M98 is already shipping to beta.

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-14)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https%3A//docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform%3Fusp%3Dpp_url%26entry.307501673%3D%7B%7D%26entry.364066060%3D%7B%7D%7B%7D%26entry.763880440%3D%7B%7D%26entry.1678852700%3D%7B%7D%26entry.763402679%3D%7B%7D%26entry.975983575%3D%7B%7D Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@google.com (2022-01-14)

Please use this link for the post mortem, thanks!

https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.975983575=jgruber@chromium.org&entry.307501673=1274445&entry.958145677=Android&entry.958145677=Chrome&entry.958145677=Fuchsia&entry.958145677=Linux&entry.958145677=Mac&entry.958145677=Windows&entry.958145677=Lacros&entry.364066060=External&entry.763880440=Extended&entry.1678852700=High&entry.763402679=Blink%3EJavaScript%3ECompiler%3ETurbofan

### [Deleted User] (2022-01-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-14)

[Empty comment from Monorail migration]

### jg...@chromium.org (2022-01-17)

The fix is not yet on canary (https://chromiumdash.appspot.com/commit/4b8d04897cba70cac45eea33d78fa2354dfe2bd7) so waiting one more day.

1. Yes
2. crrev.com/c/3379819
3. Not yet, see above.
4. No
5. N/A
6. N/A

### jg...@chromium.org (2022-01-17)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-20)

Congratulations, h2ck@ the VRP Panel has decided to award you $5000 for this report. A member of our finance team will be in touch soon to arrange payment. In the meantime, please let us know the name/handle/identifier you would like us to use for acknowledging you for this issue. 
Thank you again for your efforts and great work! 

### am...@chromium.org (2022-01-21)

m98 merge approved, please go ahead and merge this fix to the appropriate V8 branch for M98 before (11am PST) Tuesday, 25 January 2021, so this fix can be included in the stable cut of M98 -- thank you 

### go...@chromium.org (2022-01-21)

Please merge your change to M98 branch 4758 ASAP. Thank you. 

### am...@google.com (2022-01-22)

[Empty comment from Monorail migration]

### h4...@gmail.com (2022-01-24)

please use "rax of the Group0x58" as acknowledgments, thanks.

### gi...@appspot.gserviceaccount.com (2022-01-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/27bc67f761e613adf5143cb2de3d86685b1f2519

commit 27bc67f761e613adf5143cb2de3d86685b1f2519
Author: Jakob Gruber <jgruber@chromium.org>
Date: Thu Jan 13 07:01:37 2022

Merged: [maps] Lock map_updater_access in CompleteInobjectSlackTracking

CompleteInobjectSlackTracking potentially shrinks multiple maps, and
the relation between these maps should be preserved in a concurrent
environment. Thus it is not enough to make each modification
atomically, but all related map modifications must be within a
critical section.

We do this by locking the map_updater_access mutex
CompleteInobjectSlackTracking, and hence moving the function to the
MapUpdater class.

(cherry picked from commit 4b8d04897cba70cac45eea33d78fa2354dfe2bd7)

No-Try: true
No-Presubmit: true
No-Treechecks: true
Bug: chromium:1274445,v8:7990
Change-Id: If99bb8b55e03180128ee397d845fa4c269c4241e
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3379819
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Commit-Queue: Jakob Gruber <jgruber@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#78597}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3406537
Cr-Commit-Position: refs/branch-heads/9.8@{#16}
Cr-Branched-From: e218afa8473132b56a9e1532be7920dd130aeb7e-refs/heads/9.8.177@{#1}
Cr-Branched-From: 86ebfc969cde382122a4d429f2380f06175ea2a8-refs/heads/main@{#78312}

[modify] https://crrev.com/27bc67f761e613adf5143cb2de3d86685b1f2519/src/objects/map.cc
[modify] https://crrev.com/27bc67f761e613adf5143cb2de3d86685b1f2519/test/cctest/test-api.cc
[modify] https://crrev.com/27bc67f761e613adf5143cb2de3d86685b1f2519/src/objects/map-updater.cc
[modify] https://crrev.com/27bc67f761e613adf5143cb2de3d86685b1f2519/src/runtime/runtime-test.cc
[modify] https://crrev.com/27bc67f761e613adf5143cb2de3d86685b1f2519/src/runtime/runtime-object.cc
[modify] https://crrev.com/27bc67f761e613adf5143cb2de3d86685b1f2519/src/objects/map-inl.h
[modify] https://crrev.com/27bc67f761e613adf5143cb2de3d86685b1f2519/src/objects/map-updater.h
[modify] https://crrev.com/27bc67f761e613adf5143cb2de3d86685b1f2519/src/objects/js-function-inl.h
[modify] https://crrev.com/27bc67f761e613adf5143cb2de3d86685b1f2519/src/objects/map.h


### jg...@chromium.org (2022-01-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-31)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### is...@google.com (2022-07-21)

This issue was migrated from crbug.com/chromium/1274445?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1285150]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058061)*
