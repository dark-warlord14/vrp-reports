# v8 crash on map-check

| Field | Value |
|-------|-------|
| **Issue ID** | [40094529](https://issues.chromium.org/issues/40094529) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Compiler |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | yn...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2019-04-07 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36

Steps to reproduce the problem:
1. 
2. 
3. 

What is the expected behavior?

What went wrong?
poc:

function v0(v2, v3){
    Object.defineProperty(v2, 'length', { writable: v3 });
}
function v4(v6, v7) {
    try {
        var v9 = [];
        var v11 = v6.bind();
        v11(v9, v7);
        v11.__proto__ = v9;
        var v12 = {};
        v12.__proto__ = v9;
        v9.__proto__ = 13.37;
        v12.unshift(3);
    } catch (e) {
        v9[0] = 1.1;
        return v9[0];
    }
}
v4(v0, false);
v4(v0, false);
%OptimizeFunctionOnNextCall(v0);
%OptimizeFunctionOnNextCall(v4);
v4(v0, false);

v8 output:

#
# Fatal error in ../../src/compiler/compilation-dependencies.cc, line 102
# Debug check failed: map_.is_stable().
#
#
#
#FailureMessage Object: 00000062F7FFB1F8
==== C stack trace ===============================

        v8::base::debug::StackTrace::StackTrace [0x00007FF894727B4C+44] (D:\Work\Browser\Chrome\yngwei_v8\v8\src\base\debug\stack_trace_win.cc:173)
        v8::platform::`anonymous namespace'::PrintStackTrace [0x00007FF87DC5D2E4+36] (D:\Work\Browser\Chrome\yngwei_v8\v8\src\libplatform\default-platform.cc:27)
        V8_Fatal [0x00007FF8947111A5+277] (D:\Work\Browser\Chrome\yngwei_v8\v8\src\base\logging.cc:170)
        v8::base::`anonymous namespace'::DefaultDcheckHandler [0x00007FF894710B0C+44] (D:\Work\Browser\Chrome\yngwei_v8\v8\src\base\logging.cc:56)
        V8_Dcheck [0x00007FF894711286+54] (D:\Work\Browser\Chrome\yngwei_v8\v8\src\base\logging.cc:176)
        v8::internal::compiler::StableMapDependency::StableMapDependency [0x00007FF84225F54D+141] (D:\Work\Browser\Chrome\yngwei_v8\v8\src\compiler\compilation-dependencies.cc:102)
        v8::internal::compiler::CompilationDependencies::DependOnStableMap [0x00007FF84225F440+112] (D:\Work\Browser\Chrome\yngwei_v8\v8\src\compiler\compilation-dependencies.cc:367)
        v8::internal::compiler::`anonymous namespace'::DependOnStablePrototypeChain [0x00007FF842262067+263] (D:\Work\Browser\Chrome\yngwei_v8\v8\src\compiler\compilation-dependencies.cc:545)
        v8::internal::compiler::CompilationDependencies::DependOnStablePrototypeChains<std::vector<v8::internal::Handle<v8::internal::Map>,std::allocator<v8::internal::Handle<v8::internal::Map> > > > [0x00007FF842261E51+529] (D:\Work\Browser\Chrome\yngwei_v8\v8\src\compiler\compilation-dependencies.cc:556)
        v8::internal::compiler::JSNativeContextSpecialization::BuildPropertyLoad [0x00007FF8423CFA7B+555] (D:\Work\Browser\Chrome\yngwei_v8\v8\src\compiler\js-native-context-specialization.cc:2214)
        v8::internal::compiler::JSNativeContextSpecialization::BuildPropertyAccess [0x00007FF8423C40C5+517] (D:\Work\Browser\Chrome\yngwei_v8\v8\src\compiler\js-native-context-specialization.cc:2262)
        v8::internal::compiler::JSNativeContextSpecialization::ReduceNamedAccess [0x00007FF8423C25E0+2880] (D:\Work\Browser\Chrome\yngwei_v8\v8\src\compiler\js-native-context-specialization.cc:1182)
        v8::internal::compiler::JSNativeContextSpecialization::ReduceNamedAccessFromNexus [0x00007FF8423C4D99+1017] (D:\Work\Browser\Chrome\yngwei_v8\v8\src\compiler\js-native-context-specialization.cc:1376)
        v8::internal::compiler::JSNativeContextSpecialization::ReduceJSLoadNamed [0x00007FF8423BC91C+1836] (D:\Work\Browser\Chrome\yngwei_v8\v8\src\compiler\js-native-context-specialization.cc:1426)
        v8::internal::compiler::JSNativeContextSpecialization::Reduce [0x00007FF8423B7559+441] (D:\Work\Browser\Chrome\yngwei_v8\v8\src\compiler\js-native-context-specialization.cc:105)
        v8::internal::compiler::GraphReducer::Reduce [0x00007FF8422D40D8+312] (D:\Work\Browser\Chrome\yngwei_v8\v8\src\compiler\graph-reducer.cc:85)
        v8::internal::compiler::GraphReducer::ReduceTop [0x00007FF8422D3BA4+788] (D:\Work\Browser\Chrome\yngwei_v8\v8\src\compiler\graph-reducer.cc:153)
        v8::internal::compiler::GraphReducer::ReduceNode [0x00007FF8422D3568+232] (D:\Work\Browser\Chrome\yngwei_v8\v8\src\compiler\graph-reducer.cc:57)
        v8::internal::compiler::GraphReducer::ReduceGraph [0x00007FF8422D3F7D+45] (D:\Work\Browser\Chrome\yngwei_v8\v8\src\compiler\graph-reducer.cc:78)
        v8::internal::compiler::InliningPhase::Run [0x00007FF8424D02FB+2075] (D:\Work\Browser\Chrome\yngwei_v8\v8\src\compiler\pipeline.cc:1167)
        v8::internal::compiler::PipelineImpl::Run<v8::internal::compiler::InliningPhase> [0x00007FF8424BC630+96] (D:\Work\Browser\Chrome\yngwei_v8\v8\src\compiler\pipeline.cc:1063)
        v8::internal::compiler::PipelineImpl::CreateGraph [0x00007FF8424B9B9F+719] (D:\Work\Browser\Chrome\yngwei_v8\v8\src\compiler\pipeline.cc:2007)
        v8::internal::compiler::PipelineCompilationJob::PrepareJobImpl [0x00007FF8424B9551+1473] (D:\Work\Browser\Chrome\yngwei_v8\v8\src\compiler\pipeline.cc:975)
        v8::internal::OptimizedCompilationJob::PrepareJob [0x00007FF84209092B+843] (D:\Work\Browser\Chrome\yngwei_v8\v8\src\compiler.cc:218)
        v8::internal::`anonymous namespace'::GetOptimizedCodeNow [0x00007FF8420A6403+387] (D:\Work\Browser\Chrome\yngwei_v8\v8\src\compiler.cc:720)
        v8::internal::`anonymous namespace'::GetOptimizedCode [0x00007FF8420975FC+3500] (D:\Work\Browser\Chrome\yngwei_v8\v8\src\compiler.cc:889)
        v8::internal::Compiler::CompileOptimized [0x00007FF842097F29+313] (D:\Work\Browser\Chrome\yngwei_v8\v8\src\compiler.cc:1449)
        v8::internal::__RT_impl_Runtime_CompileOptimized_NotConcurrent [0x00007FF842FB4578+456] (D:\Work\Browser\Chrome\yngwei_v8\v8\src\runtime\runtime-compiler.cc:90)
        v8::internal::Runtime_CompileOptimized_NotConcurrent [0x00007FF842FB4192+338] (D:\Work\Browser\Chrome\yngwei_v8\v8\src\runtime\runtime-compiler.cc:82)
        Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit [0x00007FF84393D864+68]

Did this work before? N/A 

Chrome version: 73.0.3683.86  Channel: n/a
OS Version: 10.0
Flash Version:

## Timeline

### cl...@chromium.org (2019-04-08)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4756671346900992.

### mb...@chromium.org (2019-04-08)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### cl...@chromium.org (2019-04-08)

Detailed report: https://clusterfuzz.com/testcase?key=4756671346900992

Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  map_.is_stable() in compilation-dependencies.cc
  StableMapDependency
  v8::internal::compiler::CompilationDependencies::DependOnStableMap
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=38716:38717

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4756671346900992

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

### cl...@chromium.org (2019-04-08)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript>Compiler]

### cl...@chromium.org (2019-04-08)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/49c14f63ef1ea94b8d7b5a9dfe939b2dbc02e42e (Replace DumpBacktrace with Chromium's StackTrace implementation.).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### mb...@chromium.org (2019-04-08)

I'm assuming that isn't the correct culprit.

jarin: Would you mind taking a look at this one as well? Feel free to remove Type-Bug-Security if it doesn't seem like a security issue.

### ja...@chromium.org (2019-04-08)

We really need to run Fuzzilli on ClusterFuzz...

### ja...@chromium.org (2019-04-08)

Smaller repro:

var a = [];
Object.defineProperty(a, 'length', { writable: false });

function f() {
  var o = { __proto__ : a };
  o.push;
}

f();
f();
%OptimizeFunctionOnNextCall(f);
a[0] = 1.1;
f();

### ja...@chromium.org (2019-04-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-04-10)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-04-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/5ef88462f9ea36537933d9c10d2f6652982aa689

commit 5ef88462f9ea36537933d9c10d2f6652982aa689
Author: Jaroslav Sevcik <jarin@chromium.org>
Date: Wed Apr 10 14:30:57 2019

Avoid making maps unstable in keyed store IC.

If the runtime does not transition in keyed store IC miss handler,
avoid generating transitioning handler since this could make
the receiver map non-stable. (The optimizing compiler does not like
non-stable fast prototype maps.)

Bug: chromium:950328
Change-Id: I113880d2033518e3eb8fd11df1599e56a67d7fd0
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1559867
Commit-Queue: Jaroslav Sevcik <jarin@chromium.org>
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Reviewed-by: Benedikt Meurer <bmeurer@chromium.org>
Cr-Commit-Position: refs/heads/master@{#60752}
[modify] https://crrev.com/5ef88462f9ea36537933d9c10d2f6652982aa689/src/compiler/access-info.cc
[modify] https://crrev.com/5ef88462f9ea36537933d9c10d2f6652982aa689/src/ic/ic.cc
[add] https://crrev.com/5ef88462f9ea36537933d9c10d2f6652982aa689/test/mjsunit/regress/regress-950328.js


### cl...@chromium.org (2019-04-10)

ClusterFuzz testcase 5663108038262784 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### na...@google.com (2019-04-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-04-11)

ClusterFuzz has detected this issue as fixed in range 60751:60752.

Detailed report: https://clusterfuzz.com/testcase?key=4756671346900992

Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  map_.is_stable() in compilation-dependencies.cc
  StableMapDependency
  v8::internal::compiler::CompilationDependencies::DependOnStableMap
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=38716:38717
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=60751:60752

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4756671346900992

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### sh...@chromium.org (2019-04-11)

[Empty comment from Monorail migration]

### ad...@google.com (2019-05-01)

jarin@ I am setting a security_impact and security_severity label and expanding the affected platforms just to keep the nag-bots happy. Feel free to adjust severity/platforms as you wish.

### sh...@chromium.org (2019-05-02)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-05-02)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-05-02)

Not requesting merge to M74 because latest trunk commit (60752) appears to be prior to beta branch point (638880). If this is incorrect, please replace the Merge-na label with Merge-Request-74. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yn...@gmail.com (2019-05-04)

Can this get a cve number?

### pa...@chromium.org (2019-05-06)

The Panel needs more information re: the security impact of this report

### aw...@google.com (2019-06-04)

[Empty comment from Monorail migration]

### aw...@google.com (2019-06-04)

yngweijs@, yep this will get a CVE issued very shortly. Also, how would you like to be credited in our release notes?

### yn...@gmail.com (2019-06-04)

Thank you very much, please credit yngwei(JiaWei, Yin) of IIE Varas and sakura of Tecent Xuanwu Lab

### aw...@chromium.org (2019-06-04)

[Empty comment from Monorail migration]

### in...@chromium.org (2019-06-19)

[Empty comment from Monorail migration]

### in...@chromium.org (2019-06-19)

Jarin@, can you please triage for security severity.

### in...@chromium.org (2019-06-19)

Please add severity label and change status back to Fixed.

### ja...@chromium.org (2019-06-21)

I think you can get arbitrary reads and writes with this.

### ja...@chromium.org (2019-06-21)

[Empty comment from Monorail migration]

### yn...@gmail.com (2019-06-27)

Can I get a reward for this?

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### yn...@gmail.com (2019-07-16)

This is found with Fuzzilli @sealo

### na...@google.com (2019-07-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-07-17)

Congrats! The Panel decided to reward $3,000 for this report!

### yn...@gmail.com (2019-07-18)

Thank you very much!

### na...@google.com (2019-07-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/950328?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript, Blink>JavaScript>Compiler]
[Monorail mergedwith: crbug.com/chromium/950259]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094529)*
