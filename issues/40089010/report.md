# Security: V8 JIT escape analysis bug

| Field | Value |
|-------|-------|
| **Issue ID** | [40089010](https://issues.chromium.org/issues/40089010) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Android, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | jo...@microsoft.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2017-09-14 |
| **Bounty** | $7,500.00 |

## Description

Tested on:
	Chrome (Windows x64) stable & beta channel as of 9/14/2017 (V8 version 6.1.534.32)
	(bug also applies to other architectures and operating systems)

Small test case:
	var f = function()
	{
		var o = { a: {}, b: { ba: { baa: 0, bab: [] }, bb: {}, bc: { bca: {bcaa: 0, bcab: 0, bcac: this} } } };
		o.b.bc.bca.bcab = 0;
		o.b.bb.bba = Array.prototype.slice.apply(o.b.ba.bab);
	};
	while(true) f(f);

Observed behavior:
	In our tests, the test case resulted in one of multiple possible failures:
		- a crash upon dereferencing an invalid pointer
		- a call to V8_Fatal in MaybeHandle::Check
		- a "TypeError: Array.prototype.slice called on null or undefined" esception being thrown despite o.b.ba.bab always being an array

Causes:
	Meeting certain conditions can cause the escape analysis pass in the V8 JIT to optimize away the initialization of certain local variables in the final JITed code, which results in the behavior observed above. This can be turned into very powerful primitives by playing around with object o's internal layout as well as member variable types. These primitives include:
		- leaking the address of arbitrary objects
		- reading memory from arbitrary addresses
		- interpreting arbitrary attacker-controlled pointers as javascript objects
	With these primitives in hand, writing an exploit which achieves arbitrary code execution within the renderer process is trivial, partly thanks to the availability of RWX pages.
	A full, reliable remote code execution exploit for this bug is available upon request.


## Timeline

### cl...@chromium.org (2017-09-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5269842000347136.

### cl...@chromium.org (2017-09-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4797254937608192.

### me...@chromium.org (2017-09-14)

Thank you for the report. We would certainly love to see the full exploit, so please feel free to attach it to this bug.

adamk: Can you please take a look? 

[Monorail components: Blink>JavaScript>Compiler]

### ad...@chromium.org (2017-09-14)

Looking now.

### ad...@chromium.org (2017-09-14)

This doesn't reproduce at tip-of-tree (at least, not quickly, and when this test fails it fails very quickly from my experimentation).

From a bisect, it looks like it was fixed by the new escape analysis implementation, turned on in 40a9eabc44204c353dce4bec08e8bd87b3fc0cc7. ASsigning to tebbi@ for further analysis.

### ad...@chromium.org (2017-09-14)

In a debug build, this consistently hits a DCHECK failure:

#
# Fatal error in ../../src/compiler/escape-analysis-reducer.cc, line 399
# Check failed: !escape_analysis_->IsVirtual(node).
#

#0  v8::base::OS::Abort () at ../../src/base/platform/platform-posix.cc:248
#1  0x00007f66fddce647 in V8_Fatal (file=0x7f66fd5f3a85 "../../src/compiler/escape-analysis-reducer.cc", line=399, 
    format=0x7f66fd5ce035 "Check failed: %s.") at ../../src/base/logging.cc:126
#2  0x00007f66fc77d2c5 in v8::internal::compiler::EscapeAnalysisReducer::VerifyReplacement (this=0x7ffd4bcd77c8)
    at ../../src/compiler/escape-analysis-reducer.cc:399
#3  0x00007f66fc9484e3 in v8::internal::compiler::EscapeAnalysisPhase::Run (this=0x7ffd4bcd7860, data=0x55ea1818f958, 
    temp_zone=0x55ea1817d9c0) at ../../src/compiler/pipeline.cc:1125
#4  0x00007f66fc93dc54 in v8::internal::compiler::PipelineImpl::Run<v8::internal::compiler::EscapeAnalysisPhase> (this=0x55ea1818fac0)
    at ../../src/compiler/pipeline.cc:849
#5  0x00007f66fc9362c6 in v8::internal::compiler::PipelineImpl::OptimizeGraph (this=0x55ea1818fac0, linkage=0x55ea1818fb88)
    at ../../src/compiler/pipeline.cc:1743
#6  0x00007f66fc93619c in v8::internal::compiler::PipelineCompilationJob::ExecuteJobImpl (this=0x55ea1818f7b0)
    at ../../src/compiler/pipeline.cc:684
#7  0x00007f66fc679e67 in v8::internal::CompilationJob::ExecuteJob (this=0x55ea1818f7b0) at ../../src/compiler.cc:134
#8  0x00007f66fc6814ae in v8::internal::(anonymous namespace)::GetOptimizedCodeNow (job=0x55ea1818f7b0) at ../../src/compiler.cc:707
#9  0x00007f66fc67c372 in v8::internal::(anonymous namespace)::GetOptimizedCode (function=..., 
    mode=v8::internal::ConcurrencyMode::kNotConcurrent, osr_ast_id=..., osr_frame=0x7ffd4bcd81d0) at ../../src/compiler.cc:897
#10 0x00007f66fc67fe0d in v8::internal::Compiler::GetOptimizedCodeForOSR (function=..., osr_ast_id=..., osr_frame=0x7ffd4bcd81d0)
    at ../../src/compiler.cc:1682
#11 0x00007f66fd0ac9f5 in v8::internal::__RT_impl_Runtime_CompileForOnStackReplacement (args=..., isolate=0x55ea1811f560)
    at ../../src/runtime/runtime-compiler.cc:324
#12 0x00007f66fd0ac2d0 in v8::internal::Runtime_CompileForOnStackReplacement (args_length=1, args_object=0x7ffd4bcd84c8, 
    isolate=0x55ea1811f560) at ../../src/runtime/runtime-compiler.cc:294


### ad...@chromium.org (2017-09-14)

[Empty comment from Monorail migration]

### ad...@chromium.org (2017-09-14)

Looks like tebbi is OOO, assigning to jarin@ for handling in MUC.

### wf...@chromium.org (2017-09-15)

Additional information from reporter - http://shortn/_AZDYahmQ1t

### cl...@chromium.org (2017-09-15)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4816435858898944.

### cl...@chromium.org (2017-09-15)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5699773595385856.

### in...@chromium.org (2017-09-15)

Reuploaded using the actual debug job type, please remember to use linux_asan_d8_dbg for d8 debug job type.

### ja...@chromium.org (2017-09-15)

This is a bug in the old escape analysis that we have completely rewritten since then. The good news is that this is fixed by the new escape analysis, the bad news is that the old escape analysis is gone, so there is no way to fix bugs in it. The only reliable way seems to be disabling the escape analysis in 6.1.

The new escape analysis has been enabled by 

commit 40a9eabc44204c353dce4bec08e8bd87b3fc0cc7
Author: Tobias Tebbi <tebbi@chromium.org>
Date:   Tue Aug 1 10:10:24 2017 +0200

    Reland "[turbofan] enable new implementation of escape analysis"
    
    This is a reland of a6c3f143740b34622a89b3824391dc42b9ad2d22
    Original change's description:
    > [turbofan] enable new implementation of escape analysis
    >
    > Bug:
    > Change-Id: I0218ab67bf391deb8f1b1b78811643eb84745b7c
    > Reviewed-on: https://chromium-review.googlesource.com/595508
    > Reviewed-by: Jaroslav Sevcik <jarin@chromium.org>
    > Commit-Queue: Tobias Tebbi <tebbi@chromium.org>
    > Cr-Commit-Position: refs/heads/master@{#47032}
    
    Change-Id: Ide3d11f4b25eae2bbcaca9fc3cdb983d73ba846c
    Reviewed-on: https://chromium-review.googlesource.com/599827
    Reviewed-by: Jaroslav Sevcik <jarin@chromium.org>
    Commit-Queue: Tobias Tebbi <tebbi@chromium.org>
    Cr-Commit-Position: refs/heads/master@{#47121}

### mv...@chromium.org (2017-09-15)

Thanks for the look, Jaro...

### ha...@chromium.org (2017-09-15)

Adding ofrobots to judge the impact on node.js

### of...@google.com (2017-09-15)

AFAICT, security impact to Node.js should be low as this isn't remotely exploitable for Node.

### ha...@chromium.org (2017-09-15)

[Empty comment from Monorail migration]

### ha...@chromium.org (2017-09-15)

[Empty comment from Monorail migration]

### ha...@chromium.org (2017-09-15)

Background:
In 6.1 we have an old, removed implementation of Escape Analysis active. We replaced this implementation with a new one starting 6.2. Repairing the old one in 6.1 is not feasible especially as we can't test it on Canary anymore.

The current plan:
1.) Switch off (the new) Escape Analysis of on master to test alternative code path without Escape Analysis
2.) Analyse impact on Monday and switch off Escape Analysis in 6.1 too
3.) Switch Escape Analysis back on on master



### ja...@chromium.org (2017-09-15)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-09-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/2b15425b0c131869dbd5c9c486d402b6b911fca4

commit 2b15425b0c131869dbd5c9c486d402b6b911fca4
Author: Jaroslav Sevcik <jarin@chromium.org>
Date: Fri Sep 15 10:59:26 2017

[turbofan] Temporarily turn off escape analysis.

Bug: chromium:765433
Change-Id: Iecc9540f6305bc24a0a5210c149b55403b9ce09d
Reviewed-on: https://chromium-review.googlesource.com/667106
Reviewed-by: Michael Starzinger <mstarzinger@chromium.org>
Commit-Queue: Jaroslav Sevcik <jarin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#48032}
[modify] https://crrev.com/2b15425b0c131869dbd5c9c486d402b6b911fca4/src/flag-definitions.h


### ja...@chromium.org (2017-09-15)

A bit more background:

The problem here is too aggressive pruning of escape analysis replacement reductions. Here is an example that roughly illustrates the problem:

o0 = { f : 42 }
o1 = { g : o0 }
a = load(o1, "g")
return load(a, "f")


After we analyze the code for escapes, we try to replace the loads with the contents of the variable that represents the field. 

If we first visit load 'b', we do not do anything (because it does not load from a non-escaping allocation, but from a load), and mark it as visited (EscapeAnalysisReducer::fully_reduced_). 

Later, when we replace load a by o0, the load b will be rewritten to load(o0, "f"). Since load b was marked as visited, we will not reduce it further to 42, but instead keep it as a load. This means that we will load from object o0, which was already marked as non-escaping, and the code for the allocation and initialization was removed from the effect chain. As a result, we will load from uninitialized memory.



### go...@chromium.org (2017-09-15)

+awhalley@ (Security TPM)

### go...@chromium.org (2017-09-15)

+ hablich@ (V8 TPM)

### go...@chromium.org (2017-09-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-09-15)

Tracking this for M62, though a candidate for a 61 merge if there's a respin after it's had bake time.

### me...@chromium.org (2017-09-15)

[Empty comment from Monorail migration]

### ad...@chromium.org (2017-09-15)

This does not affect M62 (see #19 for the summary).

### aw...@chromium.org (2017-09-15)

ah, sorry for not spotted, thanks adamk@ Removing ReleaseBlock-Stable

### me...@chromium.org (2017-09-15)

Upgrading to Severity-Critical (https://crbug.com/chromium/765433#c9 contains the full chain)

### wf...@chromium.org (2017-09-15)

The v8 bug is High as execution is contained within the renderer sandbox. the PoC demonstrates what can be done with arbitrary code execution from renderer but does not demonstrate any new sandbox escape.

### sh...@chromium.org (2017-09-16)

[Empty comment from Monorail migration]

### ja...@chromium.org (2017-09-18)

[Empty comment from Monorail migration]

### ja...@chromium.org (2017-09-18)

We should merge the "fix" to 6.1 - Canary experiment with escape analysis off looks good, turning off escape analysis is low risk. (We have turned off escape analysis several times before without any problems.)

There are some performance implications, mostly affecting benchmarks and some ES6 heavy code.

### ha...@chromium.org (2017-09-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-09-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/a503d626788aa142551180ab802c488a5a3e9227

commit a503d626788aa142551180ab802c488a5a3e9227
Author: Jaroslav Sevcik <jarin@chromium.org>
Date: Mon Sep 18 10:58:06 2017

Merged: [turbofan] Temporarily turn off escape analysis.

Revision: 2b15425b0c131869dbd5c9c486d402b6b911fca4

BUG=chromium:765433
LOG=N
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=hablich@chromium.org

Change-Id: Iae7a44d2441f51d51423fba9b9c46367937cdad7
Reviewed-on: https://chromium-review.googlesource.com/670563
Reviewed-by: Michael Hablich <hablich@chromium.org>
Cr-Commit-Position: refs/branch-heads/6.1@{#80}
Cr-Branched-From: 1bf2e10ddb194d4c2871a87a4732613419de892d-refs/heads/6.1.534@{#1}
Cr-Branched-From: e825c4318eb2065ffdf9044aa6a5278635c36427-refs/heads/master@{#46746}
[modify] https://crrev.com/a503d626788aa142551180ab802c488a5a3e9227/src/flag-definitions.h


### ja...@chromium.org (2017-09-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-09-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/d6ff08223bab0a0ca8b5c8413b13f87257cf1a58

commit d6ff08223bab0a0ca8b5c8413b13f87257cf1a58
Author: Jaroslav Sevcik <jarin@chromium.org>
Date: Mon Sep 18 12:16:36 2017

Revert "[turbofan] Temporarily turn off escape analysis."

This reverts commit 2b15425b0c131869dbd5c9c486d402b6b911fca4.

Reason for revert: Re-enabling escape analysis after merging the flag change to 6.1.

Original change's description:
> [turbofan] Temporarily turn off escape analysis.
> 
> Bug: chromium:765433
> Change-Id: Iecc9540f6305bc24a0a5210c149b55403b9ce09d
> Reviewed-on: https://chromium-review.googlesource.com/667106
> Reviewed-by: Michael Starzinger <mstarzinger@chromium.org>
> Commit-Queue: Jaroslav Sevcik <jarin@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#48032}

TBR=mstarzinger@chromium.org,jarin@chromium.org

# Not skipping CQ checks because original CL landed > 1 day ago.

Bug: chromium:765433
Change-Id: Icac44fd76e2965df1e143700941b628ea7a69166
Reviewed-on: https://chromium-review.googlesource.com/670864
Reviewed-by: Jaroslav Sevcik <jarin@chromium.org>
Commit-Queue: Jaroslav Sevcik <jarin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#48064}
[modify] https://crrev.com/d6ff08223bab0a0ca8b5c8413b13f87257cf1a58/src/flag-definitions.h


### sh...@chromium.org (2017-09-18)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2017-09-18)

Thanks for the merges. We won't be re-spinning M61 for this, but it will be picked up if we respin for another reason.

### bm...@chromium.org (2017-09-18)

Note: If Node 8 is going for 6.1, we should definitely turn on escape analysis there.

### aw...@chromium.org (2017-09-18)

[Empty comment from Monorail migration]

### ja...@chromium.org (2017-09-19)

#41 What do you mean, exactly? Do you have a fix for the bug? Even if you have, how do you test the fix?

### sh...@chromium.org (2017-09-19)

[Empty comment from Monorail migration]

### as...@chromium.org (2017-09-21)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-09-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### ma...@chromium.org (2017-09-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-10-11)

[Empty comment from Monorail migration]

### aw...@google.com (2017-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### in...@chromium.org (2018-02-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/765433?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/808483]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089010)*
