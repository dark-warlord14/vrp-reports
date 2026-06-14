# Security: Failed Debug Check in src/compiler/verifier.cc, line 121

| Field | Value |
|-------|-------|
| **Issue ID** | [40094379](https://issues.chromium.org/issues/40094379) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows |
| **Reporter** | tm...@acu.edu |
| **Assignee** | ja...@chromium.org |
| **Created** | 2019-03-26 |
| **Bounty** | $3,000.00 |

## Description

Note: Not super familiar with v8, so this might not be a security issue.

**VULNERABILITY DETAILS**  

A debug check fails when running either of the attached scripts. This was found with Fuzzilli (<https://github.com/googleprojectzero/fuzzilli>)

**VERSION**  

v8 Master branch, Commit 33fa605a865173dd606f2edf2547596996617b44  

Found on: Ubuntu 16.04

**REPRODUCTION CASE**  

Using Fuzzilli's provided build script & patch (Found in the above repo under "Targets"), I built d8 and then ran the following:

./d8 --allow-natives-syntax testcase1.js

Asan build trace below (Non symbolized):

[COV] no shared memory bitmap available, skipping  

[COV] edge counters initialized. Shared memory: (null) with 557815 edges

# 

# Fatal error in ../../src/compiler/verifier.cc, line 121

# Debug check failed: effect\_edges > 0 (0 vs. 0).

# 

# 

# 

#FailureMessage Object: 0x7fa464736c60  

==== C stack trace ===============================

```
/home/test/Desktop/v8/v8/out/asanFuzzbuild/d8(backtrace+0x5b [0x55903a60feeb]  
/home/test/Desktop/v8/v8/out/asanFuzzbuild/d8(+0x1208c02) [0x55903a83ec02]  
/home/test/Desktop/v8/v8/out/asanFuzzbuild/d8(+0x1203b9f) [0x55903a839b9f]  
/home/test/Desktop/v8/v8/out/asanFuzzbuild/d8(+0x11f0a12) [0x55903a826a12]  
/home/test/Desktop/v8/v8/out/asanFuzzbuild/d8(+0x11f01ff) [0x55903a8261ff]  
/home/test/Desktop/v8/v8/out/asanFuzzbuild/d8(+0x1ef60b9) [0x55903b52c0b9]  
/home/test/Desktop/v8/v8/out/asanFuzzbuild/d8(+0x1f03b8f) [0x55903b539b8f]  
/home/test/Desktop/v8/v8/out/asanFuzzbuild/d8(+0x16f80f7) [0x55903ad2e0f7]  
/home/test/Desktop/v8/v8/out/asanFuzzbuild/d8(+0x16f380b) [0x55903ad2980b]  
/home/test/Desktop/v8/v8/out/asanFuzzbuild/d8(+0x16f3389) [0x55903ad29389]  
/home/test/Desktop/v8/v8/out/asanFuzzbuild/d8(+0x1592d62) [0x55903abc8d62]  
/home/test/Desktop/v8/v8/out/asanFuzzbuild/d8(+0x15a3a44) [0x55903abd9a44]  
/home/test/Desktop/v8/v8/out/asanFuzzbuild/d8(+0x15a734a) [0x55903abdd34a]  
/home/test/Desktop/v8/v8/out/asanFuzzbuild/d8(+0x335e25b) [0x55903c99425b]  
/home/test/Desktop/v8/v8/out/asanFuzzbuild/d8(+0x335d58c) [0x55903c99358c]  
/home/test/Desktop/v8/v8/out/asanFuzzbuild/d8(+0x44b9d60) [0x55903daefd60]  

```

Received signal 4 ILL\_ILLOPN 55903a832980  

Illegal instruction (core dumped)

## Attachments

- [testcase1.js](attachments/testcase1.js) (text/plain, 1.2 KB)
- [testcase2.js](attachments/testcase2.js) (text/plain, 922 B)
- [liveBuildCrash.js](attachments/liveBuildCrash.js) (text/plain, 925 B)

## Timeline

### ke...@chromium.org (2019-03-26)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### ha...@chromium.org (2019-03-26)

[Empty comment from Monorail migration]

[Monorail components: -Blink>JavaScript Blink>JavaScript>Compiler]

### tm...@acu.edu (2019-03-27)

v8 Git commit compiled with: a2dfb40e1c18fae1c378490c982b41f589dafddb

Compiling command: tools/dev/gm.py x64.debug

The attached liveBuildCrash.js crashes on the latest v8 master repo *WITHOUT* the fuzilli patch.

Debug backtrace below:


#
# Fatal error in ../../src/compiler/verifier.cc, line 121
# Debug check failed: effect_edges > 0 (0 vs. 0).
#
#
#
#FailureMessage Object: 0x7fff40d15de0
==== C stack trace ===============================

    /home/test/Desktop/nonFuzilliv8/v8/v8/out/x64.debug/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1e) [0x7fe60704ce6e]
    /home/test/Desktop/nonFuzilliv8/v8/v8/out/x64.debug/libv8_libplatform.so(+0x30567) [0x7fe606ff1567]
    /home/test/Desktop/nonFuzilliv8/v8/v8/out/x64.debug/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x218) [0x7fe60703afb8]
    /home/test/Desktop/nonFuzilliv8/v8/v8/out/x64.debug/libv8_libbase.so(+0x349fc) [0x7fe60703a9fc]
    /home/test/Desktop/nonFuzilliv8/v8/v8/out/x64.debug/libv8_libbase.so(V8_Dcheck(char const*, int, char const*)+0x32) [0x7fe60703b092]
    /home/test/Desktop/nonFuzilliv8/v8/v8/out/x64.debug/libv8.so(v8::internal::compiler::Verifier::Visitor::Check(v8::internal::compiler::Node*, v8::internal::compiler::AllNodes const&)+0x2a4) [0x7fe605d3d964]
    /home/test/Desktop/nonFuzilliv8/v8/v8/out/x64.debug/libv8.so(v8::internal::compiler::Verifier::Run(v8::internal::compiler::Graph*, v8::internal::compiler::Verifier::Typing, v8::internal::compiler::Verifier::CheckInputs, v8::internal::compiler::Verifier::CodeType)+0x1a4) [0x7fe605d44784]
    /home/test/Desktop/nonFuzilliv8/v8/v8/out/x64.debug/libv8.so(v8::internal::compiler::VerifyGraphPhase::Run(v8::internal::compiler::PipelineData*, v8::internal::Zone*, bool, bool)+0x9c) [0x7fe605ca27ec]
    /home/test/Desktop/nonFuzilliv8/v8/v8/out/x64.debug/libv8.so(void v8::internal::compiler::PipelineImpl::Run<v8::internal::compiler::VerifyGraphPhase, bool>(bool&&)+0x71) [0x7fe605c9de21]
    /home/test/Desktop/nonFuzilliv8/v8/v8/out/x64.debug/libv8.so(v8::internal::compiler::PipelineImpl::RunPrintAndVerify(char const*, bool)+0x7f) [0x7fe605c961df]
    /home/test/Desktop/nonFuzilliv8/v8/v8/out/x64.debug/libv8.so(v8::internal::compiler::PipelineImpl::OptimizeGraph(v8::internal::compiler::Linkage*)+0x108) [0x7fe605c94c78]
    /home/test/Desktop/nonFuzilliv8/v8/v8/out/x64.debug/libv8.so(v8::internal::compiler::PipelineCompilationJob::ExecuteJobImpl()+0x1a0) [0x7fe605c94ae0]
    /home/test/Desktop/nonFuzilliv8/v8/v8/out/x64.debug/libv8.so(v8::internal::OptimizedCompilationJob::ExecuteJob()+0xd3) [0x7fe605a442f3]
    /home/test/Desktop/nonFuzilliv8/v8/v8/out/x64.debug/libv8.so(+0x11c0b5c) [0x7fe605a4eb5c]
    /home/test/Desktop/nonFuzilliv8/v8/v8/out/x64.debug/libv8.so(+0x11b9c85) [0x7fe605a47c85]
    /home/test/Desktop/nonFuzilliv8/v8/v8/out/x64.debug/libv8.so(v8::internal::Compiler::CompileOptimized(v8::internal::Handle<v8::internal::JSFunction>, v8::internal::ConcurrencyMode)+0xdd) [0x7fe605a482ed]
    /home/test/Desktop/nonFuzilliv8/v8/v8/out/x64.debug/libv8.so(+0x1ad049e) [0x7fe60635e49e]
    /home/test/Desktop/nonFuzilliv8/v8/v8/out/x64.debug/libv8.so(v8::internal::Runtime_CompileOptimized_NotConcurrent(int, unsigned long*, v8::internal::Isolate*)+0x117) [0x7fe60635e197]
    /home/test/Desktop/nonFuzilliv8/v8/v8/out/x64.debug/libv8.so(+0x215a100) [0x7fe6069e8100]
Received signal 4 ILL_ILLOPN 7fe60704a581
Illegal instruction (core dumped)


### cl...@chromium.org (2019-03-28)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5960563577454592.

### cl...@chromium.org (2019-03-28)

Testcase 5960563577454592 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5960563577454592.

### dr...@chromium.org (2019-03-28)

I wasn't able to reproduce this bug, and neither was ClusterFuzz. jarin@ - were you able to make any progress on this?

### tm...@acu.edu (2019-03-28)

Apologies, I forgot to add the --allow-natives-syntax flag (IE: ./d8 --allow-natives-syntax liveBuildCrash.js) was needed to reproduce with the liveBuildCrash.js POC. I can also recompile v8 to a different commit if that makes it easier to reproduce. 

### ja...@chromium.org (2019-03-28)

It does repro for me. Working on a fix.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-03-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/1ec7ffedc85a1868a25b758147d8acc0c398bd72

commit 1ec7ffedc85a1868a25b758147d8acc0c398bd72
Author: Jaroslav Sevcik <jarin@chromium.org>
Date: Fri Mar 29 08:52:20 2019

[turbofan] Make sure nodes are killed on replacement

In reducers, we should avoid reductions of the form

  ReduceWithValue(node, replacement)
  return Replace(node)

because such reduction does not kill the original node, so it may
become subject to resurrection from some side table (in the bug
referenced below it was load elimination's side table). Instead,
we should use

  ReduceWithValue(node, replacement)
  return Replace(replacement)

Bug: chromium:945644
Change-Id: Id210efe0d214a53241392d30b7f0eee8e7515e2a
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1545229
Reviewed-by: Sigurd Schneider <sigurds@chromium.org>
Commit-Queue: Jaroslav Sevcik <jarin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#60517}
[modify] https://crrev.com/1ec7ffedc85a1868a25b758147d8acc0c398bd72/src/compiler/typed-optimization.cc
[add] https://crrev.com/1ec7ffedc85a1868a25b758147d8acc0c398bd72/test/mjsunit/compiler/regress-945644.js


### ja...@chromium.org (2019-03-29)

[Empty comment from Monorail migration]

### ja...@chromium.org (2019-03-29)

This fix should be merged back to at least beta (after it is some time in Canary). It is likely a security bug because we create an invalid graph, but I have not figured how exactly this would be exploited.

### sh...@chromium.org (2019-03-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-29)

This bug requires manual review: M74 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), dgagnon@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-03-29)

+adetaylor@ (Security TPM) for M74 merge review.

### ad...@chromium.org (2019-03-29)

Agreed, merge for M74 (noting jarin@'s comment we should wait for it to run in canary for a period).

### go...@chromium.org (2019-03-29)

Please update bug with canary result on Monday.

### tm...@acu.edu (2019-04-01)

Per https://crbug.com/chromium/945644#c11, I'm not sure how this would be exploited either. I've played around with various nodes but haven't been successful so far. 

### ab...@google.com (2019-04-02)

branch:3729

### aw...@chromium.org (2019-04-03)

[Empty comment from Monorail migration]

### go...@chromium.org (2019-04-07)

Please merge you change to M74 branch 3729 ASAP so we can pick it up for this week beta release. Thank you.

### ja...@chromium.org (2019-04-08)

This has been already merged to M74, not sure why the bug has not picked this up:

commit babb052d1823cdb7931d3e7f7d938e62cb8c0646
Author: Jaroslav Sevcik <jarin@chromium.org>
Date:   Wed Apr 3 06:58:24 2019 +0200

    Merged: [turbofan] Make sure nodes are killed on replacement
    
    Revision: 1ec7ffedc85a1868a25b758147d8acc0c398bd72
    
    BUG=chromium:945644
    LOG=N
    NOTRY=true
    NOPRESUBMIT=true
    NOTREECHECKS=true
    R=bmeurer@chromium.org
    
    Change-Id: Icd4967f015e704ce56cc20539faf62c0e53abba2
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1549170
    Reviewed-by: Benedikt Meurer <bmeurer@chromium.org>
    Cr-Commit-Position: refs/branch-heads/7.4@{#37}
    Cr-Branched-From: 3e8a733af17a7812eba188dad612be503bd45c57-refs/heads/7.4.288@{#1}
    Cr-Branched-From: d077f9b5ad92b23fe4366a9bdce319a71cd1a2c5-refs/heads/master@{#60039}


### go...@chromium.org (2019-04-08)

If it is already merged to M74, pls remove "Merge-Approved-74" label and apply "Merge-Approved-7.4" label. Thank you.

### sh...@chromium.org (2019-04-08)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-04-09)

Pls merge your change to M74 branch 3729 ASAP so we can pick it up for this week beta release. Thank you.

### ja...@chromium.org (2019-04-09)

[Empty comment from Monorail migration]

### na...@google.com (2019-04-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-04-10)

Congrats! The Panel decided to reward $3,000 for this report. 

Please add how you would like to be credited in our release notes and a member from our finance team will be in touch shortly. 

### na...@google.com (2019-04-10)

[Empty comment from Monorail migration]

### tm...@acu.edu (2019-04-10)

Thanks! 

I’d like credit to be to: @TimGMichaud of Leviathan Security Group. 

### aw...@google.com (2019-04-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-04-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-26)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@chromium.org (2019-05-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-14)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ne...@chromium.org (2020-07-14)

Merged according to https://bugs.chromium.org/p/chromium/issues/detail?id=945644#c25

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/945644?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/947920]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094379)*
